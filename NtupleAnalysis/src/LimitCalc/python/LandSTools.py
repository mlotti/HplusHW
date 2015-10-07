## \package LandSTools
# Python interface for running LandS with multicrab
#
# The interface for casual user is provided by the functions
# generateMultiCrab() (for LEP-CLs and LHC-CLs) and
# produceLHCAsymptotic (for LHC-CLs asymptotic).
#
# The multicrab configuration generation saves various parameters to
# taskdir/configuration.json, to be used in by landsMergeHistograms.py
# script. The script uses tools from this module, which write the
# limit results to taskdir/limits.json. I preferred simple text format
# over ROOT files due to the ability to read/modify the result files
# easily. Since the amount of information in the result file is
# relatively small, the performance penalty should be negligible.

import HiggsAnalysis.LimitCalc..CommonLimitTools as commonLimitTools

import os
import re
import sys
import glob
import json
import time
import random
import shutil
import subprocess


import multicrab
import multicrabWorkflows
import git
import aux

## The LandS CVS tag to be used
LandS_tag = "HEAD" # 28.01.2014: this is the only available, where shape bug in H+ has been fixed
#LandS_tag = "t3-06-05" # Given by Mingshui 15.8.2012 at 11:56 EEST
#LandS_tag	    = "HEAD" # Recommended by Mingshui 10.5.2012 at 23:23:22 EEST
#LandS_tag           = "V3-04-01_eps" # this one is in the Tapio's scripts
#LandS_tag           = "t3-04-13"

## Common command-line options to LandS
#
# These options are common for all CLs flavours, channels, and mass
# points. At the moment the only such option is the physics model.
commonOptionsBrLimit  = "--PhysicsModel ChargedHiggs"
commonOptionsSigmaBrLimit  = ""

## Default command-line options for LEP-CLs
lepHybridOptions = "-M Hybrid --bQuickEstimateInitialLimit 0"
## Default number of toys for expected limits for LEP-CLs
lepHybridToys = 50
## Default "Rmin" parameter for LEP-CLs
lepHybridRmin = "0"
## Default "Rmax" parameter for LEP-CLs
lepHybridRmax = "0.09"


## Command-line options with Minos minimizer LHC-CLs (hybrid) (needed for some mass points of combination)
lhcHybridOptionsMinos = "-M Hybrid --freq --scanRs 1 --maximumFunctionCallsInAFit 500000 --minuitSTRATEGY 1"
## Default command-line options for LHC-CLs (hybrid)
lhcHybridOptions = lhcHybridOptionsMinos + "  --PLalgorithm Migrad"
## Default number of toys for CLsb for LHC-CLs (hybrid)
lhcHybridToysCLsb = 600 
#300
## Default number of toys for CLb for LHC-CLs (hybrid)
lhcHybridToysCLb = 300 
#150
## Default "Rmin" parameter for LHC-CLs (hybrid)
lhcHybridRmin = "0"
## Default "Rmax" parameter for LHC-CLs (hybrid)
lhcHybridRmax = "40" 
# 1

## Default command line options for LHC-CLs (asymptotic, observed limit)
lhcAsymptoticOptionsObserved = "-M Asymptotic --maximumFunctionCallsInAFit 500000"
## Default command line options for LHC-CLs (asymptotic, expected limit)
lhcAsymptoticOptionsExpected = lhcAsymptoticOptionsObserved + " --PLalgorithm Migrad"
## Default "Rmin" parameter for LHC-CLs (asymptotic)
lhcAsymptoticRmin = "0"
## Default "Rmax" parameter for LHC-CLs (asymptotic)
lhcAsymptoticRmax = "1"

## Default options are LEP-CLs
defaultOptions = lepHybridOptions
## Default number of crab jobs
defaultNumberOfJobs = 20

# FIXME: migrate theses if necessary to tools/CommonLimitTools.py
## Pattern for mu+tau datacard files (%s denotes the place of the mass)
mutauDatacardPattern = "datacard_m%s_mutau_miso_20mar12.txt"
## Pattern for e+tau datacard files (%s denotes the place of the mass)
etauDatacardPattern = "datacard_m%s_etau_miso_20mar12.txt"
## Pattern for e+mu datacard files (%s denotes the place of the mass)
emuDatacardPattern = "datacard_m%s_emu_nobtag_20mar12.txt"

## Deduces from directory listing the mass point list
def obtainMassPoints(pattern):
    commonLimitTools.obtainMassPoints(pattern)

def readLuminosityFromDatacard(myPath, filename):
    commonLimitTools.readLuminosityFromDatacard(myPath, filename)

## Returns true if mass list contains only heavy H+
def isHeavyHiggs(massList):
    commonLimitTools.isHeavyHiggs(massList)

## Returns true if mass list contains only light H+
def isLightHiggs(massList):
    commonLimitTools.isLightHiggs(massList)

## Generate multicrab configuration for LEP-CLs or LHC-CLs (hybrid)
# \param opts               optparse.OptionParser object, constructed with createOptionParser()
# \param massPoints         List of mass points to calculate the limit for
#                           (list of strings)
# \param datacardPatterns   List of datacard patterns to include in the
#                           limit calculation (list of strings, each
#                           string should have '%s' to denote the
#                           position of the mass)
# \param rootfilePatterns   List of shape ROOT file patterns to include
#                           in the limit calculation (list of strings,
#                           each string should have '%s' to denote the
#                           position of the mass)
# \param clsType            Object defining the CLs flavour (should be either
#                           LEPType, or LHCType). If None, the default
#                           (LEPType) is used
# \param numberOfJobs       Number of crab jobs. Can be a number, which is
#                           then used for all mass points, or a
#                           dictionary to have mass-specific numbers
#                           of jobs. See ValuePerMass for more
#                           information of the dictionary. If None,
#                           the default value (defaultNumberOfJobs) is
#                           used.
# \param crabScheduler      CRAB scheduler to use (default is arc, if you
#                           want to submit from lxplus, use "glite").
#                           In principle it should be possible to
#                           submit to LSF with a proper scheduler.
# \param crabOptions        Dictionary for specifying additional CRAB
#                           options. The keys correspond to the
#                           sections in crab.cfg. The values are lists
#                           containing lines to be appended to the
#                           section.
# \param postfix            String to be added to the multicrab task directory
#                           name
#
# The CLs-flavour specific options are controlled by the constructors
# of LEPType and LHCType classes.
def generateMultiCrab(opts,
                      directory,
                      massPoints,
                      datacardPatterns,
                      rootfilePatterns,
                      clsType=None,
                      numberOfJobs=None,
                      crabScheduler="arc",
                      crabOptions={},
                      postfix=""
                      ):
    cls = clsType
    if clsType == None:
        cls = LEPType()

    print "Computing limits with %s CLs flavour" % cls.nameHuman()
    print "Computing limits with LandS version %s" % landsInstall.getVersion()

    njobs = aux.ValuePerMass(aux.ifNotNoneElse(numberOfJobs, defaultNumberOfJobs))

    landsObjects = []

    lands = MultiCrabLandS(opts, directory, massPoints, datacardPatterns, rootfilePatterns, cls)
    lands.createMultiCrabDir(postfix)
    lands.copyInputFiles()
    lands.writeScripts()
    lands.writeCrabCfg(crabScheduler, crabOptions, ["lands.out"])
    lands.writeMultiCrabCfg(njobs)

    landsObjects.append(lands)

    if opts.multicrabCreate:
        for lands in landsObjects:
            lands.createMultiCrab()

    for lands in landsObjects:
        if len(landsObjects) > 1:
            print
        lands.printInstruction()

## Create OptionParser, and add common LandS options to OptionParser object
#
# \param lepDefault     Boolean for the default value of --lep switch (if None, switch is not added)
# \param lhcDefault     Boolean for the default value of --lhc switch (if None, switch is not added)
# \param lhcasyDefault  Boolean for the default value of --lhcasy switch (if None, switch is not added)
#
# \return optparse.OptionParser object
def createOptionParser(lepDefault=None, lhcDefault=None, lhcasyDefault=None):
    return commonLimitTools.createOptionParser(lepDefault, lhcDefault, lhcasyDefault)

## Parse OptionParser object
#
# \param parser   optparse.OptionParser object
#
# \return Options object
def parseOptionParser(parser):
    commonLimitTools.parseOptionParser(parser)


## Run LandS for the LHC-CLs asymptotic limit
# \param opts               optparse.OptionParser object, constructed with createOptionParser()
# \param massPoints         List of mass points to calculate the limit for
#                           (list of strings)
# \param datacardPatterns   List of datacard patterns to include in the
#                           limit calculation (list of strings, each
#                           string should have '%s' to denote the
#                           position of the mass)
# \param rootfilePatterns   List of shape ROOT file patterns to include
#                           in the limit calculation (list of strings,
#                           each string should have '%s' to denote the
#                           position of the mass)
# \param clsType            Object defining the CLs flavour (should be
#                           LHCTypeAsymptotic). If None, the default
#                           (LHCTypeAsymptotic) is used
# \param postfix            String to be added to the multicrab task directory
#                           name
#
# The options of LHCTypeAsymptotic are controlled by the constructor.
def produceLHCAsymptotic(opts, directory,
                         massPoints,
                         datacardPatterns,
                         rootfilePatterns,
                         clsType = None,
                         postfix=""
                         ):

    cls = clsType
    if clsType == None:
        cls = LHCTypeAsymptotic(opts.brlimit, opts.sigmabrlimit)

    print "Computing limits with %s CLs flavour" % cls.nameHuman()
    print "Computing limits with LandS version %s" % landsInstall.getVersion()

    lands = MultiCrabLandS(opts, directory, massPoints, datacardPatterns, rootfilePatterns, cls)
    lands.createMultiCrabDir(postfix)
    lands.copyInputFiles()
    lands.writeScripts()
    lands.runLandSForAsymptotic()

## Class to generate (LEP-CLs, LHC-CLs) multicrab configuration, or run (LHC-CLs asymptotic) LandS
#
# The class is not intended to be used directly by casual user, but
# from generateMultiCrab() and produceLHCAsymptotic()
class MultiCrabLandS(commonLimitTools.LimitMultiCrabBase):
    ## Constructor
    #
    # \param directory          Datacard directory
    # \param massPoints         List of mass points to calculate the limit for
    # \param datacardPatterns   List of datacard patterns to include in the
    #                           limit calculation
    # \param rootfilePatterns   List of shape ROOT file patterns to include
    #                           in the limit calculation
    # \param clsType            Object defining the CLs flavour (should be either
    #                           LEPType, or LHCType).
    def __init__(self, opts, directory, massPoints, datacardPatterns, rootfilePatterns, clsType):
        commonLimitTools.LimitMultiCrabBase.__init__(self, opts, directory, massPoints, datacardPatterns, rootfilePatterns, clsType)
        self.exe = landsInstall.findExe()
        self.configuration["landsVersion"] = LandS_tag

    ## Create the multicrab task directory
    #
    # \param postfix   Additional string to be included in the directory name
    def createMultiCrabDir(self, postfix):
        prefix = "LandSMultiCrab"
        self._createMultiCrabDir(prefix, postfix)


    ## Run LandS for the asymptotic limit
    #
    # This is so fast at the moment that using crab jobs for that
    # would be waste of resources and everybodys time.
    def runLandSForAsymptotic(self):
        print "Running LandS for asymptotic limits, saving results to %s" % self.dirname
        f = open(os.path.join(self.dirname, "configuration.json"), "wb")
        json.dump(self.configuration, f, sort_keys=True, indent=2)
        f.close()

        results = commonLimitTools.ResultContainer(self.opts.unblinded, self.dirname)
        for mass in self.massPoints:
            results.append(self.clsType.runLandS(mass))
            print "Processed mass point %s" % mass
        print

        results.print2()
        fname = results.saveJson()
        print "Wrote results to %s" % fname

## Definition of the LEP-type CLs (with hybrid treatment of nuisance parameters)
#
# The method itself is described in the CMS-NOTE-2011-005 appendix A.1.2
#
# Calculating limits involves one job for observed limit and N jobs
# for the expected limits for one mass point. A crab task is created
# for both (separately). For the expected limits, the output root
# files are merged, and then LandS is ran one time for the merged root
# file. This is taken care of with the \a landsMergeHistograms.py
# script.
class LEPType:
    ## Constructor
    #
    # \param options     Command line options for LandS. String,
    #                    dictionary (see ValuePerMass), or None for
    #                    default (lepHybridOptions)
    # \param toysPerJob  Number of toys per job for expected limits
    #                    (\a -t parameter). Number, dictionary (see
    #                    ValuePerMass), or None for default
    #                    (lepHybridToys)
    # \param firstSeed   First random number seed for the jobs (actually
    #                    first seed is firstSeed+1).
    # \param rMin        The \a --initialRmin parameter for LandS. String,
    #                    dictionary (see ValuePerMass), or None for
    #                    default (lepHybridRmin)
    # \param rMax        The \a --initialRmax parameter for LandS. String,
    #                    dictionary (see ValuePerMass), or None for
    #                    default (lepHybridRmax)
    #
    # Note: if you add any parameters to the constructor, add the
    # parameters to the clone() method correspondingly.
    def __init__(self, brlimit=True, sigmabrlimit=False, options=None, toysPerJob=None, firstSeed=1000, rMin=None, rMax=None):
        self.brlimit = brlimit
        self.sigmabrlimit = sigmabrlimit
        self.options = ValuePerMass(aux.ifNotNoneElse(options, lepHybridOptions))
        self.firstSeed = firstSeed
        self.toysPerJob = aux.ValuePerMass(aux.ifNotNoneElse(toysPerJob, lepHybridToys))
        self.rMin = aux.ValuePerMass(aux.ifNotNoneElse(rMin, lepHybridRmin))
        self.rMax = aux.ValuePerMass(aux.ifNotNoneElse(rMax, lepHybridRmax))

        self.expScripts = {}
        self.obsScripts = {}

    ## Return the name of the CLs flavour (for serialization to configuration.json)
    def name(self):
        return "LEP"

    ## Return human-readable name of the CLs flavour
    def nameHuman(self):
        return "LEP-type hybrid"

    ## Get the configuration dictionary for serialization.
    #
    # LEP-type CLs does not need any specific information to be stored
    def getConfiguration(self, mcconf):
        return None

    ## Clone the object, possibly overriding some options
    #
    # \param kwargs   Keyword arguments, can be any of the arguments of
    #                 __init__(), with the same meaning.
    def clone(self, **kwargs):
        args = aux.updateArgs(kwargs, self, ["options", "toysPerJob", "firstSeed", "rMin", "rMax"])
        return LEPType(**args)

    ## Set the multicrab directory path
    # \param dirname   Path to the multicrab directory
    def setDirectory(self, dirname):
        self.dirname = dirname

    ## Create the job scripts for a single mass point
    #
    # \param mass            String for the mass point
    # \param datacardFiles   List of strings for datacard file names of the mass point
    def createScripts(self, mass, datacardFiles):
        self._createObs(mass, datacardFiles)
        self._createExp(mass, datacardFiles)

    ## Create the observed job script for a single mass point
    #
    # \param mass            String for the mass point
    # \param datacardFiles   List of strings for datacard file names of the mass point
    def _createObs(self, mass, datacardFiles):
        fileName = "runLandS_Observed_m" + mass
        opts = ""
        if self.brlimit:
            opts += commonOptionsBrLimit
        if self.sigmabrlimit:
            opts += commonOptionsSigmaBrLimit
        opts += " " + self.options.getValue(mass) + " --initialRmin %s --initialRmax %s" % (self.rMin.getValue(mass), self.rMax.getValue(mass))
        command = [
            "#!/bin/sh",
            "",
            "SEED=$(expr %d + $1)" % self.firstSeed,
            'echo "LandSSeed=$SEED"',
            "",
            "./lands.exe %s --seed $SEED -d %s | tail -5 > lands.out" % (opts, " ".join(datacardFiles)),
            ""
            "cat lands.out"
            ]
        aux.writeScript(os.path.join(self.dirname, fileName), "\n".join(command)+"\n")
        self.obsScripts[mass] = fileName

    ## Create the expected job script for a single mass point
    #
    # \param mass            String for the mass point
    # \param datacardFiles   List of strings for datacard file names of the mass point
    def _createExp(self, mass, datacardFiles):
        fileName = "runLandS_Expected_m" + mass
        opts = ""
        if self.brlimit:
            opts += commonOptionsBrLimit
        if self.sigmabrlimit:
            opts += commonOptionsSigmaBrLimit
        opts = " " + self.options.getValue(mass) + " --initialRmin %s --initialRmax %s" % (self.rMin.getValue(mass), self.rMax.getValue(mass))
        command = [
            "#!/bin/sh",
            "",
            "SEED=$(expr %d + $1)" % self.firstSeed,
            'echo "LandSSeed=$SEED"',
            "",
            "./lands.exe %s -n split_m%s --doExpectation 1 -t %s --seed $SEED -d %s | tail -5 > lands.out" % (opts, mass, self.toysPerJob, " ".join(datacardFiles)),
            "",
            "cat lands.out",
            ]
        aux.writeScript(os.path.join(self.dirname, fileName), "\n".join(command)+"\n")
        self.expScripts[mass] = fileName

    ## Write the multicrab configuration snippet of a single mass point
    #
    # \param output      Output stream to write the contents
    # \param mass        String for the mass point
    # \param inputFiles  List of strings for the (additional) input files to pack in the crab job
    # \param numJobs     Number of jobs for the expected task
    def writeMultiCrabConfig(self, opts, output, mass, inputFiles, numJobs):
        if opts.unblinded:
            output.write("[Observed_m%s]\n" % mass)
            output.write("USER.script_exe = %s\n" % self.obsScripts[mass])
            output.write("USER.additional_input_files = %s\n" % ",".join(inputFiles))
            output.write("CMSSW.number_of_jobs = 1\n")
            output.write("CMSSW.output_file = lands.out\n")
            output.write("\n")

        output.write("[Expected_m%s]\n" % mass)
        output.write("USER.script_exe = %s\n" % self.expScripts[mass])
        output.write("USER.additional_input_files = %s\n" % ",".join(inputFiles))
        output.write("CMSSW.number_of_jobs = %d\n" % numJobs)
        output.write("CMSSW.output_file = lands.out,split_m%sHybrid_limitbands.root,split_m%sHybrid_limits_tree.root\n" % (mass, mass))

    ## Construct the Result object for a single mass point
    #
    # \param path       Path to the multicrab directory
    # \param mass       String for the mass point
    # \param clsConfig  Dictionary of the CLs-flavour-specific
    #                   configuration (stored in configuration.json).
    #                   Not used by LEPType, but needed for consistent
    #                   interface
    #
    # \return Result object containing the limits for the mass point
    def getResult(self, path, mass, clsConfig, unblindedStatus=False):
        result = commonLimitTools.Result(mass)
        if unblindedStatus:
            self._parseObserved(result, path, mass)
        self._parseExpected(result, path, mass)
        return result

    ## Read the observed limit and insert to the Result
    #
    # \param result  Result object to modify
    # \param path    Path to the multicrab directory
    # \param mass    String for the mass point
    #
    # Reads the result from the lands.out file (which is fine since
    # there is only one job for observed limit)
    def _parseObserved(self, result, path, mass):
        landsOutFiles = glob.glob(os.path.join(path, "Observed_m%s"%mass, "res", "lands_*.out"))
        if len(landsOutFiles) == 0:
            return
        if len(landsOutFiles) != 1:
            raise Exception("Expected exactly 1 LandS output file, got %d" % len(landsOutFiles))

        result_re = re.compile("= (?P<value>\d+\.\d+)\s+\+/-\s+(?P<error>\d+\.\S+)")
        f = open(landsOutFiles[0])
        for line in f:
            match = result_re.search(line)
            if match:
                result.observed = match.group("value")
                result.observedError =match.group("error")
                f.close()
                return
        raise Exception("Unable to parse observed result from '%s'" % landsOutFiles[0])

    ## Read the expected limits and insert to the Result
    #
    # \param result  Result object to modify
    # \param path    Path to the multicrab directory
    # \param mass    String for the mass point
    #
    # Runds LandS for the merged root file, and reads the expected
    # limits (median, +-1/2sigma) from the output. LandS is run only
    # if the merged output file does not exist
    def _parseExpected(self, result, path, mass):
        mergedFilename = "lands_merged.out"
        crabRes = os.path.join(path, "Expected_m%s"%mass, "res")
        fileExists = self._runLandSForMerge(crabRes, mergedFilename, mass)
        if not fileExists:
            return

        fname = os.path.join(crabRes, mergedFilename)
        f = open(fname)
        result_re = re.compile("BANDS\s+(?P<minus2>\d+\.\d+)\s+(?P<minus1>\d+\.\d+)\s+(?P<mean>\d+\.\d+)\s+(?P<plus1>\d+\.\d+)\s+(?P<plus2>\d+\.\d+)\s+(?P<median>\d+\.\d+)")
        for line in f:
            match = result_re.search(line)
            if match:
		result.expected = match.group("median")
		result.expectedPlus1Sigma  = match.group("plus1")
		result.expectedPlus2Sigma  = match.group("plus2")
		result.expectedMinus1Sigma = match.group("minus1")
		result.expectedMinus2Sigma = match.group("minus2")
                f.close()
                return

        raise Exception("Unable to parse expected result from '%s'" % fname)

    ## Run LandS for the merged root file
    #
    # \param resDir           Path to the \a res directory of the crab task
    # \param mergedfilename   Name of the merged root file in the \a resDir
    # \param mass             String for the mass point
    #
    # \return True, if the result file exists (either before or after
    #         the merge), False, if LandS failed for any reason
    def _runLandSForMerge(self, resDir, mergedFilename, mass):
        targetFile = os.path.join(resDir, mergedFilename)
        if os.path.exists(targetFile):
            return True

        exe = landsInstall.findExe()
        rootFile = os.path.join(resDir, "histograms-Expected_m%s.root" % mass)
        if not os.path.exists(rootFile):
            print "Merged root file '%s' does not exist, did you run landsMergeHistograms.py?" % rootFile
            return False

        cmd = [exe, "--doExpectation", "1", "--readLimitsFromFile", rootFile]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = p.communicate()[0]
        if p.returncode != 1:
            raise Exception("Call to '%s' failed with exit code %d" % (" ".join(cmd), p.returncode))
        f = open(targetFile, "w")
        f.write(output)
        f.write("\n")
        f.close()
        return True

## Definition of the LHC-type CLs (with the frequentist treatment of nuisance parameters)
#
# The method itself is described in the CMS-NOTE-2011-005 section 2.
#
# In this case the crab jobs are needed only for the toy MC for the
# sampling distributions of the test statistic. This toy MC is reused
# for the expected limits. Consequence is that a single crab task of N
# jobs gives the information for both the observed and the expected
# limits. Again the root files must be merged, and this time a root
# macro is run (instead of LandS) to produce the limits. This is taken
# care of with the \a landsMergeHistograms.py script.
class LHCType:
    ## Constructor
    #
    # \param options     Command line options for LandS. String,
    #                    dictionary (see ValuePerMass), or None for
    #                    default (lhcHybridOptions)
    # \param toysCLsb    Number of toys per job for CLsb (\a
    #                    --nToysForCLsb parameter). Number, dictionary
    #                    (see ValuePerMass), or None for default
    #                    (lhcHybridToysCLsb)
    # \param toysCLb     Number of toys per job for CLb (\a
    #                    --nToysForCLb parameter). Number, dictionary
    #                    (see ValuePerMass), or None for default
    #                    (lhcHybridToysCLb)
    # \param firstSeed   First random number seed for the jobs (actually
    #                    first seed is firstSeed+1).
    # \param vR          The \a -vR parameter for LandS. Pair/triple of strings,
    #                    dictionary (see ValuePerMass), or None for
    #                    not to add \a -vR parameter.
    # \param rMin        The \a --rMin parameter for LandS. String,
    #                    dictionary (see ValuePerMass), or None for
    #                    default (lhcHybridRmin)
    # \param rMax        The \a --rMax parameter for LandS. String,
    #                    dictionary (see ValuePerMass), or None for
    #                    default (lhcHybridRmax)
    # \param scanRmin The \a scanRmin parameter for \a fitRvsCLs.C
    #                    macro. String, dictionary (see ValuePerMass),
    #                    or None for not to add the \a scanRmin
    #                    parameter.
    # \param scanRmax    The \a scanRmax parameter for \a fitRvsCLs.C
    #                    macro. String, dictionary (see ValuePerMass),
    #                    or None for not to add the \a scanRmin
    #                    parameter.
    #
    # Note: if you add any parameters to the constructor, add the
    # parameters to the clone() method correspondingly.
    #
    # The \a scanRmin and \a scanRmax parameters are saved to the \a
    # configuration.json file, and can be overridden by editing the
    # file between the multicrab configuration generation and the call
    # to \a landsMergeHistograms.py.
    def __init__(self, brlimit=True, sigmabrlimit=False, options=None, toysCLsb=None, toysCLb=None, firstSeed=1000, vR=None, rMin=None, rMax=None, scanRmin=None, scanRmax=None):
        self.brlimit = brlimit
        self.sigmabrlimit = sigmabrlimit
        self.options = aux.ValuePerMass(aux.ifNotNoneElse(options, lhcHybridOptions))

        self.firstSeed = firstSeed

        self.toysCLsb = aux.ValuePerMass(aux.ifNotNoneElse(toysCLsb, lhcHybridToysCLsb))
        self.toysCLb = aux.ValuePerMass(aux.ifNotNoneElse(toysCLb, lhcHybridToysCLb))

        def assertvR(value):
            if value != None and len(value) != 2 and len(value) != 3:
                raise Exception("vR should be pair (min, max) or triple (min, max, factor), got length %d: %s" % (len(value), str(value)))
        self.vR = aux.ValuePerMass(vR)
        self.vR.forEachValue(assertvR)

        self.rMin = aux.ValuePerMass(aux.ifNotNoneElse(rMin, lhcHybridRmin))
        self.rMax = aux.ValuePerMass(aux.ifNotNoneElse(rMax, lhcHybridRmax))

        self.scanRmin = aux.ValuePerMass(scanRmin)
        self.scanRmax = aux.ValuePerMass(scanRmax)
        self.configuration = {}
        self.configuration["scanRmin"] = self.scanRmin.serialize()
        self.configuration["scanRmax"] = self.scanRmax.serialize()

        self.scripts = {}

    ## Return the name of the CLs flavour (for serialization to configuration.json)
    def name(self):
        return "LHC"

    ## Return human-readable name of the CLs flavour
    def nameHuman(self):
        return "LHC-type hybrid"

    ## Get the configuration dictionary for serialization.
    #
    # For LHC-type CLs the \a scanRmin and \a scanRmax are stored
    def getConfiguration(self, mcconf):
        return self.configuration

    ## Clone the object, possibly overriding some options
    #
    # \param kwargs   Keyword arguments, can be any of the arguments of
    #                 __init__(), with the same meaning.
    def clone(self, **kwargs):
        args = aux.updateArgs(kwargs, self, ["options", "toysCLsb", "toysCLb", "firstSeed", "vR", "rMin", "rMax", "scanRmin", "scanRmax"])
        return LHCType(**args)

    ## Set the multicrab directory path
    #
    # \param dirname   Path to the multicrab directory
    def setDirectory(self, dirname):
        self.dirname = dirname

    ## Create the job script for a single mass point
    #
    # \param mass            String for the mass point
    # \param datacardFiles   List of strings for datacard file names of the mass point
    def createScripts(self, mass, datacardFiles):
        filename = "runLandS_m%s" % mass
        opts = ""
        if self.brlimit:
            opts += commonOptionsBrLimit
        if self.sigmabrlimit:
            opts += commonOptionsSigmaBrLimit
        opts += " " + self.options.getValue(mass) + " --rMin %s --rMax %s" % (self.rMin.getValue(mass), self.rMax.getValue(mass))
        vR = self.vR.getValue(mass)
        if vR == None:
            opts += " --ExpectationHints Asymptotic"
        elif len(vR) == 2:
            opts += " -vR [%s,%s,x1.05]" % vR
        elif len(vR) == 3:
            opts += " -vR [%s,%s,%s]" % vR
        else:
            raise Exception("Assert: len(vR) = %d" % len(vR))
        command = [
            "#!/bin/sh",
            "",
            "SEED=$(expr %d + $1)" % self.firstSeed,
            'echo "LandSSeed=$SEED"',
            "",
            "./lands.exe %s -n split_m%s --nToysForCLsb %d --nToysForCLb %d --seed $SEED -d %s | tee lands.out.tmp" % (opts, mass, self.toysCLsb.getValue(mass), self.toysCLb.getValue(mass), " ".join(datacardFiles)),
            "head -n 50 lands.out.tmp> lands.out",
            "tail -n 5 lands.out.tmp >> lands.out",
            "cat lands.out"
            ]

        aux.writeScript(os.path.join(self.dirname, filename), "\n".join(command)+"\n")
        self.scripts[mass] = filename

        # Produce also scripts for ML fit, they're not run on the grid however
        opts = ""
        if self.brlimit:
            opts += commonOptionsBrLimit
        if self.sigmabrlimit:
            opts += commonOptionsSigmaBrLimit
        opts = " -M MaxLikelihoodFit -v 1"
        b_file = "mlfit_b_m%s_output.txt" % mass
        b_file2 = "mlfit_b_m%s.txt" % mass
        sb_file = "mlfit_sb_m%s_output.txt" % mass
        sb_file2 = "mlfit_sb_m%s.txt" % mass
        command = [
            "#!/bin/sh",
            "",
            "./lands.exe %s -n mlfit_sb_m%s --rMin 0 --rMax 0.2 -d %s > %s 2>&1" % (opts, mass, " ".join(datacardFiles), sb_file),
            "./lands.exe %s -n mlfit_b_m%s --scanRs 1 -vR 0 -d %s > %s 2>&1" % (opts, mass, " ".join(datacardFiles), b_file),
            "tail -n 200 %s | fgrep par > %s" % (b_file, b_file2),
            "fgrep par %s > %s" % (sb_file, sb_file2),
            "landsReadMLFit.py -b %s -s %s -o mlfit.json -m %s" % (b_file, sb_file, mass),
            'echo "ML fit results are in %s and %s, and also in mlfit.json"' % (sb_file2, b_file2)
            ]
        aux.writeScript(os.path.join(self.dirname, "runLandS_m%s_mlfit" % mass), "\n".join(command)+"\n")

        command = [
        ]
        allMlFitPath = os.path.join(self.dirname, "runLandS_mlfits")
        if not os.path.exists(allMlFitPath):
            command.extend([
                    "#!/bin/sh",
                    "",
                    ])
        command.append("./runLandS_m%s_mlfit" % mass)
        aux.writeScript(allMlFitPath, "\n".join(command)+"\n", truncate=False)                
        

    ## Write the multicrab configuration snippet of a single mass point
    #
    # \param output      Output stream to write the contents
    # \param mass        String for the mass point
    # \param inputFiles  List of strings for the (additional) input files to pack in the crab job
    # \param numJobs     Number of jobs for the expected task
    def writeMultiCrabConfig(self, opts, output, mass, inputFiles, numJobs):
        output.write("[Limit_m%s]\n" % mass)
        output.write("USER.script_exe = %s\n" % self.scripts[mass])
        output.write("USER.additional_input_files = %s\n" % ",".join(inputFiles))
        output.write("CMSSW.number_of_jobs = %d\n" % numJobs)
        output.write("CMSSW.output_file = lands.out,split_m%s_m2lnQ.root\n" % mass)

    ## Construct the Result object for a single mass point
    #
    # \param path       Path to the multicrab directory
    # \param mass       String for the mass point
    # \param clsConfig  Dictionary of the CLs-flavour-specific
    #                   configuration (stored in configuration.json).
    #
    # \return Result object containing the limits for the mass point
    #
    # Runs the \a fitRvsCLs.C macro for the merged root file, and
    # reads the observed and expected limits from the output. The
    # script output is also stored in a text file for later referecence.
    def getResult(self, path, mass, clsConfig, unblindedStatus=False):
        result = commonLimitTools.Result(mass)

        rootFile = os.path.join(path, "Limit_m%s"%mass, "res", "histograms-Limit_m%s.root"%mass)
        if not os.path.exists(rootFile):
            print "Merged root file '%s' does not exist, did you run landsMergeHistograms.py?" % rootFile
            return result

        fitScript = os.path.join(landsInstall.findDir(), "test", "fitRvsCLs.C")
        if not os.path.exists(fitScript):
            raise Exception("Did not find fit script '%s'" % fitScript)
        rootCommand = ["root", "-l", "-n", "-b", fitScript+"+"] # Must have the plus, i.e. must be run on jade5 or lxplus5
        p = subprocess.Popen(rootCommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        commands = []

        if clsConfig != None and "scanRmin" in clsConfig:
            scanRmin = aux.ValuePerMass(clsConfig["scanRmin"])
            val = scanRmin.getValue(mass)
            if val != None:
                commands.append("scanRmin = %s" % val)
        if clsConfig != None and "scanRmax" in clsConfig:
            scanRmax = aux.ValuePerMass(clsConfig["scanRmax"])
            val = scanRmax.getValue(mass)
            if val != None:
                commands.append("scanRmax = %s" % val)
        commands.extend([
            'run("%s", "plot_m%s")' % (rootFile, mass),
#            'run("%s", "plot_m%s", "bands", -1, 1)' % (rootFile, mass), # for debug output of the script
            ".q"
            ])
        output = p.communicate("\n".join(commands)+"\n")[0]
        # Dirty hack: apply blinding by removing files for observed
        if not unblindedStatus:
            if os.path.exists("plot_m%s_observed.gif"%mass):
                os.remove("plot_m%s_observed.gif"%mass)
            if os.path.exists("plot_m%s_observed.root"%mass):
                os.remove("plot_m%s_observed.root"%mass)

#        print output
        f = open(os.path.join(path, "fitRvsCLs_m%s_output.txt"%mass), "w")
        f.write(" ".join(rootCommand)+"\n\n")
        f.write("\n".join(commands)+"\n\n")
        f.write(output)
        f.write("\n")
        f.close()
        lines = output.split("\n")
        lines.reverse()
        if "Error in <ACLiC>: Compilation failed!" in output:
            raise Exception("Error: Please run this same script on jade-five or lxplus5 with --skipMerge parameter! Root needs to compile the library for fitRvsCLs.C")
        if "Error" in output:
            print "Encountered an error, here's the full notification:"
            print output

        def res(s):
            return "(?P<%s>[^+]+)\+/-(?P<%se>[^,]+)" % (s, s)
        result_re = re.compile("EXPECTED LIMIT BANDS.+mass=[^:]+:\s*" + res("obs") + ",\s+" +
                               res("m2s") + ",\s+" + res("m1s") + ",\s+" + res("med") + ",\s+" + res("p1s") + ",\s+" + res("p2s"))

        for line in lines:
            match = result_re.search(line)
            if match:
                result.observed = match.group("obs")
                result.observedError = match.group("obse")
                result.expected = match.group("med")
                result.expectedError = match.group("mede")
                result.expectedPlus1Sigma = match.group("p1s")
                result.expectedPlus1SigmaError = match.group("p1se")
                result.expectedPlus2Sigma = match.group("p2s")
                result.expectedPlus2SigmaError = match.group("p2se")
                result.expectedMinus1Sigma = match.group("m1s")
                result.expectedMinus1SigmaError = match.group("m1se")
                result.expectedMinus2Sigma = match.group("m2s")
                result.expectedMinus2SigmaError = match.group("m2se")

        return result

## Definition of the LHC-type CLs (with the asymptotic treatment of nuisance parameters)
#
# The method itself is described in the CMS-NOTE-2011-005 appendix A.1.3.
#
# At the moment running the asymptotic limit is so fast that running
# it via crab would be waste of time and resources from everybodys
# point of view. Instead, the LandS is run at the "multicrab
# configuration generation" stage. To have similar usage to the other
# CLs flavours, the results are stored in a multicrab task directory.
#
# Because no crab is involved, the user interface is different. This
# is achieved with the produceLHCAsymptotic() function instead of the
# generateMultiCrab().
class LHCTypeAsymptotic:
    ## Constructor
    #
    # \param optionsObserved  Command line options for LandS for the
    #                         observed limit. String, dictionary (see
    #                         ValuePerMass), or None for default
    #                         (lhcAsymptoticOptionsObserved)
    # \param optionsExpected  Command line options for LandS for the
    #                         expected limit. String, dictionary (see
    #                         ValuePerMass), or None for default
    #                         (lhcAsymptoticOptionsExpected)
    # \param rMin             The \a --rMin parameter for LandS. String,
    #                         dictionary (see ValuePerMass), or None for
    #                         default (lhcAsymptoticRmin)
    # \param rMax             The \a --rMax parameter for LandS. String,
    #                         dictionary (see ValuePerMass), or None for
    #                         default (lhcAsymptoticRmax)
    # \param vR               The \a -vR parameter for LandS. Pair/triple of strings,
    #                         dictionary (see ValuePerMass), or None for
    #                         not to add \a -vR parameter.
    #
    # Note: if you add any parameters to the constructor, add the
    # parameters to the clone() method correspondingly.
    def __init__(self, brlimit=True, sigmabrlimit=False, optionsObserved=None, optionsExpected=None, rMin=None, rMax=None, vR=None):
        self.brlimit = brlimit
        self.sigmabrlimit = sigmabrlimit
        self.optionsObserved = aux.ValuePerMass(aux.ifNotNoneElse(optionsObserved, lhcAsymptoticOptionsObserved))
        self.optionsExpected = aux.ValuePerMass(aux.ifNotNoneElse(optionsExpected, lhcAsymptoticOptionsExpected))
        self.rMin = aux.ValuePerMass(aux.ifNotNoneElse(rMin, lhcAsymptoticRmin))
        self.rMax = aux.ValuePerMass(aux.ifNotNoneElse(rMax, lhcAsymptoticRmax))

        def assertvR(value):
            if value != None and len(value) != 2 and len(value) != 3:
                raise Exception("vR should be pair (min, max) or triple (min, max, factor), got length %d: %s" % (len(value), str(value)))
        self.vR = aux.ValuePerMass(vR)
        self.vR.forEachValue(assertvR)

        self.obsScripts = {}
        self.expScripts = {}

    ## Return the name of the CLs flavour (for serialization to configuration.json)
    def name(self):
        return "LHCAsymptotic"

    ## Return human-readable name of the CLs flavour
    def nameHuman(self):
        return "LHC-type asymptotic"

    ## Get the configuration dictionary for serialization.
    #
    # LHC-type asymptotic CLs does not need any specific information to be stored
    def getConfiguration(self, mcconf):
        return None

    ## Clone the object, possibly overriding some options
    #
    # \param kwargs   Keyword arguments, can be any of the arguments of
    #                 __init__(), with the same meaning.
    def clone(self, **kwargs):
        args = aux.updateArgs(kwargs, self, ["optionsObserved", "optionsExpected", "rMin", "rMax", "vR"])
        return LHCTypeAsymptotic(**args)

    ## Set the multicrab directory path
    #
    # \param dirname   Path to the multicrab directory
    def setDirectory(self, dirname):
        self.dirname = dirname

    ## Create the job scripts for a single mass point
    #
    # \param mass            String for the mass point
    # \param datacardFiles   List of strings for datacard file names of the mass point
    def createScripts(self, mass, datacardFiles):
        self._createObs(mass, datacardFiles)
        self._createExp(mass, datacardFiles)

    ## Create the observed job script for a single mass point
    #
    # \param mass            String for the mass point
    # \param datacardFiles   List of strings for datacard file names of the mass point
    def _createObs(self, mass, datacardFiles):
        fileName = "runLandS_Observed_m" + mass
        opts = ""
        if self.brlimit:
            opts += commonOptionsBrLimit
        if self.sigmabrlimit:
            opts += commonOptionsSigmaBrLimit
        opts += " " + self.optionsObserved.getValue(mass) + " --rMin %s --rMax %s" % (self.rMin.getValue(mass), self.rMax.getValue(mass))
        vR = self.vR.getValue(mass)
        if vR != None:
            if len(vR) == 2:
                opts += " -vR [%s,%s,x1.05]" % vR
            elif len(vR) == 3:
                opts += " -vR [%s,%s,%s]" % vR
            else:
                raise Exception("Assert: len(vR) = %d" % len(vR))

        command = [
            "#!/bin/sh",
            "",
            "./lands.exe %s --minuitSTRATEGY 1 -n obs_m%s -d %s" % (opts, mass, " ".join(datacardFiles)),
            ]
        aux.writeScript(os.path.join(self.dirname, fileName), "\n".join(command)+"\n")
        self.obsScripts[mass] = fileName

    ## Create the expected job script for a single mass point
    #
    # \param mass            String for the mass point
    # \param datacardFiles   List of strings for datacard file names of the mass point
    def _createExp(self, mass, datacardFiles):
        fileName = "runLandS_Expected_m" + mass
        opts = ""
        if self.brlimit:
            opts += commonOptionsBrLimit
        if self.sigmabrlimit:
            opts += commonOptionsSigmaBrLimit
        opts = " " + self.optionsExpected.getValue(mass) + " --rMin %s --rMax %s" % (self.rMin.getValue(mass), self.rMax.getValue(mass))
        vR = self.vR.getValue(mass)
        if vR != None:
            if len(vR) == 2:
                opts += " -vR [%s,%s,x1.05]" % vR
            elif len(vR) == 3:
                opts += " -vR [%s,%s,%s]" % vR
            else:
                raise Exception("Assert: len(vR) = %d" % len(vR))

        command = [
            "#!/bin/sh",
            "",
            "./lands.exe %s --minuitSTRATEGY 2 -n exp_m%s -D asimov_b -d %s" % (opts, mass, " ".join(datacardFiles)),
            ]
        aux.writeScript(os.path.join(self.dirname, fileName), "\n".join(command)+"\n")
        self.expScripts[mass] = fileName

    ## Run LandS for the observed and expected limits for a single mass point
    #
    # \param mass   String for the mass point
    #
    # \return Result object containing the limits for the mass point
    def runLandS(self, mass):
        result = commonLimitTools.Result(mass)
        self._runObserved(result, mass)
        self._runExpected(result, mass)
        return result

    ## Helper method to run a script
    #
    # \param script      Path to the script to run
    # \param outputfile  Path to a file to store the script output
    #
    # \return The output of the script as a string
    def _run(self, script, outputfile):
        exe = landsInstall.findExe()
        pwd = os.getcwd()
        os.chdir(self.dirname)

        p = subprocess.Popen(["./"+script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = p.communicate()[0]
        if p.returncode != 0:
            print output
            raise Exception("LandS failed with exit code %d\nCommand: %s" % (p.returncode, script))
        os.chdir(pwd)

        f = open(os.path.join(self.dirname, outputfile), "w")
        f.write(output)
        f.write("\n")
        f.close()

        return output

    ## Run LandS for the observed limit
    #
    # \param result  Result object to modify
    # \param mass    String for the mass point
    def _runObserved(self, result, mass):
        script = self.obsScripts[mass]
        output = self._run(script, "obs_m%s_output.txt"%mass)

        result_re = re.compile("Observed Upper Limit .* =\s*(?P<value>\d+\.\d+)")
        lines = output.split("\n")
        lines.reverse()
        for line in lines:
            match = result_re.search(line)
            if match:
                result.observed = match.group("value")
                return result

        print output
        raise Exception("Unable to parse the output of command '%s'" % script)

    ## Run LandS for the expected limit
    #
    # \param result  Result object to modify
    # \param mass    String for the mass point
    def _runExpected(self, result, mass):
        script = self.expScripts[mass]
        output = self._run(script, "exp_m%s_output.txt"%mass)

        result_re = re.compile("BANDS\s+(?P<minus2>\d+\.\d+)\s+(?P<minus1>\d+\.\d+)\s+(?P<mean>\d+\.\d+)\s+(?P<plus1>\d+\.\d+)\s+(?P<plus2>\d+\.\d+)\s+(?P<median>\d+\.\d+)")
        lines = output.split("\n")
        lines.reverse()
        for line in lines:
            match = result_re.search(line)
            if match:
		result.expected = match.group("median")
		result.expectedPlus1Sigma  = match.group("plus1")
		result.expectedPlus2Sigma  = match.group("plus2")
		result.expectedMinus1Sigma = match.group("minus1")
		result.expectedMinus2Sigma = match.group("minus2")
                return result

        print output
        raise Exception("Unable to parse the output of command '%s'" % script)



## Class to parse the limits from LandS output
#
# This is used from \a landsMergeHistograms.py to read the LandS
# output. The limits are stored in \a limits.json file for easier
# subsequent access.
class ParseLandsOutput:
    ## Constructor
    #
    # \param path   Path to the multicrab directory
    def __init__(self, path, unblindedStatus=False):
	self.path = path
	self.lumi = 0

        # Read task configuration json file
        configFile = os.path.join(path, "configuration.json")
        f = open(configFile)
        self.config = json.load(f)
        f.close()

        if self.config["clsType"] == "LEP":
            self.clsType = LEPType()
        elif self.config["clsType"] == "LHC":
            self.clsType = LHCType()
        else:
            raise Exception("Unsupported CLs type '%s' in %s" % (self.config["clsType"], configFile))

        # Read in the results
        self.results = commonLimitTools.ResultContainer(unblindedStatus, self.path)
        try:
            clsConfig = self.config["clsConfig"]
        except KeyError:
            clsConfig = None
        for mass in self.config["masspoints"]:
            self.results.append(self.clsType.getResult(self.path, mass, clsConfig))
            print "Processed mass point %s" % mass


    ## Get the integrated luminosity as a string in 1/pb
    def getLuminosity(self):
	return self.results.getLuminosity()

    ## Print the results
    def print2(self,unblindedStatus=False):
        self.results.print2(unblindedStatus)

    ## Save the results to \a limits.json file
    def saveJson(self):
        fname = self.results.saveJson()
        print "Wrote results to %s" % fname


## Parse the nuisance fit values from LandS ML output
#
# \return dictionary
def parseLandsMLOutput(outputFileName):
    f = open(outputFileName)

    # Skip first lines
    for line in f:
        if "fReadFile: Reading --> rate" in line:
            break

    # Infer nuisance parameter names
    nuisanceNames = []
    nuisanceTypes = []
    nuis_re = re.compile("--> (?P<nuisance>\S+)\s+(?P<type>\S+)\s+\S+")
    for line in f:
        if not "fReadFile" in line:
            break

        m = nuis_re.search(line)
        if m:
            nuisanceNames.append(m.group("nuisance"))
            nuisanceTypes.append(m.group("type"))


    # Read the last set of "par" lines
    parLines = []
    while True:
        # Skip until "par" lines are found
        for line in f:
            if "par" in line and "name" in line and "fitted_value" in line and "input_value"in line:
                break

        # Read "par" lines
        parLinesTmp = []
        for line in f:
            if not "par" in line:
                break
            parLinesTmp.append(line.rstrip())
        if len(parLinesTmp) > 0:
            parLines = parLinesTmp
        else:
            break

    f.close()

    # Parse "par" lines
    num = "-?\d+.\d+"
    par_re = re.compile("par\s+(?P<nuisance>\S+)\s+(?P<fittedvalue>%s) \+/- (?P<fittedunc>%s)\s+(?P<inputvalue>%s) \+/- (?P<inputunc>%s)\s+(?P<startvalue>%s)\s+(?P<dxsin>%s),\s+(?P<soutsin>%s)" % (num, num, num, num, num, num, num))
    values = {
        "nuisanceParameters": nuisanceNames,
    }
    for par in parLines:
        m = par_re.search(par)
        if not m:
            raise Exception("Unable to parse line '%s'" % par)

        type = None
        key = m.group("nuisance")
        subkey = None
        if key == "signal_strength":
            type = key
        else:
            if key not in nuisanceNames:
                for nuis in nuisanceNames:
                    if key[0:len(nuis)] == nuis:
                        subkey = key[len(nuis):]
                        key = nuis
            type = nuisanceTypes[nuisanceNames.index(key)]

        d = {
            "fitted_value": m.group("fittedvalue"),
            "fitted_uncertainty": m.group("fittedunc"),
            "input_value": m.group("inputvalue"),
            "input_uncertainty": m.group("inputunc"),
            "start_value": m.group("startvalue"),
            "dx/s_in": m.group("dxsin"),
            "s_out/s_in": m.group("soutsin"),
            }

        if subkey is None:
            values[key] = d
        else:
            if key in values:
                values[key][subkey] = d
            else:
                values[key] = {subkey: d}

        values[key]["type"] = type

    return values


## Class to contain LandS installation information
#
# Looks for LandS in
# $CMSSW_BASE/src/HiggsAnalysis/HeavyChHiggsToTauNu/test/brlimit. If
# found, return the path. If not found, install LandS and return the
# path. Installation consists of cvs checkout and compilation with make.
class LandSInstaller:
    ## Constructor
    #
    # \param tag   CVS Tag of LandS to checkout
    def __init__(self, tag=LandS_tag):
        self.tag = tag

    ## Get LandS version string
    def getVersion(self):
        if self.tag != "HEAD":
            return self.tag
        landsExe = self.findExe()
        mtime = os.path.getmtime(landsExe)
        mtime = time.localtime(mtime) # seconds -> structure in local time
        return "HEAD (compiled at %s)" % time.strftime("%Y%m%d-%H%M%S", mtime)
        
    ## Get the path to the LandS directory
    def findDir(self):
        brlimitBase = os.path.join(aux.higgsAnalysisPath(), "HeavyChHiggsToTauNu", "test", "brlimit")
        landsDir = "LandS_"+self.tag
        landsDirAbs = os.path.join(brlimitBase, landsDir)
        if not os.path.exists(landsDirAbs):
            pwd = os.getcwd()
            os.chdir(brlimitBase)

            command = ["cvs", "checkout", "-r", LandS_tag, "-d", landsDir, "UserCode/mschen/LandS"]
            ret = subprocess.call(command)
            if ret != 0:
                raise Exception("cvs checkout failed (exit code %d), command '%s'" % (ret, " ".join(command)))
            if not os.path.exists(landsDir):
                raise Exception("cvs checkout failed to create directory '%s' under '%s'" % (brlimitBase, landsDir))
            # Patch - no patch needed
            #os.system("patch -p0 < $CMSSW_BASE/src/HiggsAnalysis/HeavyChHiggsToTauNu/test/brlimit/mypatch")
            # Compile
            if os.environ["HOST"] == "jade.hip.fi":
                print "LandS has been downloaded and patched."
                print "Since you are working on jade, you must now manually do the following:"
                print "1) log on jade-five.hip.fi"
                print "2) cd %s"%landsDirAbs
                print '3) setenv SCRAM_ARCH "slc5_amd64_gcc472"'
                print "4) cmsenv"
                print "5) make -j 4"
                print "If the make is successful (it should be), then return to this terminal and redo this command"
                sys.exit()
            os.chdir(landsDir)
            ret = subprocess.call(["make", "clean"])
            if ret != 0:
                raise Exception("Compiling LandS failed (exit code %d), command 'make clean'" % ret)
            ret = subprocess.call(["make"])
            if ret != 0:
                raise Exception("Compiling LandS failed (exit code %d), command 'make'" % ret)
    
            os.chdir(pwd)
            print
            print "LandS version %s installed at %s" % (self.tag, landsDirAbs)
            print

        return landsDirAbs

    ## Get the path to the lands.exe
    def findExe(self):
        landsDirAbs = self.findDir()
        landsExe = os.path.join(landsDirAbs, "test", "lands.exe")
        if not os.path.isfile(landsExe):
            raise Exception("Found LandS directory '%s', but not lands.exe as '%s'" % (landsDirAbs, landsExe))

        return landsExe

## Object to contain LandS installation information
landsInstall = LandSInstaller()
