## \package CombineTools
# Python interface for running Combine with multicrab
#
# The interface for casual user is provided by the functions
# generateMultiCrab() (for LEP-CLs and LHC-CLs) and
# produceLHCAsymptotic (for LHC-CLs asymptotic).
#
# The multicrab configuration generation saves various parameters to
# taskdir/configuration.json, to be used in by combineMergeHistograms.py
# script. The script uses tools from this module, which write the
# limit results to taskdir/limits.json. I preferred simple text format
# over ROOT files due to the ability to read/modify the result files
# easily. Since the amount of information in the result file is
# relatively small, the performance penalty should be negligible.

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.CommonLimitTools as commonLimitTools


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
import array

import ROOT

## The Combine git tag to be used (see https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideHiggsAnalysisCombinedLimit)
Combine_tag = "V03-05-00" # 06.02.2014
validCMSSWversions = ["CMSSW_6_1_1"]
## Common command-line options to Combine

## Command line options for creating Combine workspace
workspacePattern = "combineWorkspaceM%s.root"
workspaceOptionsBrLimitTemplate = "text2workspace.py %s -P HiggsAnalysis.CombinedLimit.ChargedHiggs:brChargedHiggs -o %s"%("%s",workspacePattern)
workspaceOptionsSigmaBrLimit    = "text2workspace.py %s -o combineWorkspaceM%s.root"%("%s",workspacePattern)

## Command line options for running Combine
#asymptoticLimit = "combine -M Asymptotic --picky"
#asymptoticLimitOptionExpectedOnly = " --run expected"

#hybridLimit = "combine -M HybridNew --freq --hintMethod Asymptotic" # --testStat LHC

## Default number of crab jobs
defaultNumberOfJobs = 20


## Default command line options for LHC-CLs (asymptotic, observed limit)
lhcAsymptoticOptionsObserved = "-M Asymptotic --picky -v 2 --rAbsAcc 0.00001"
## Default command line options for LHC-CLs (asymptotic, expected limit)
lhcAsymptoticOptionsBlinded = lhcAsymptoticOptionsObserved + " --run blind"
## Default "Rmin" parameter for LHC-CLs (asymptotic)
lhcAsymptoticRminSigmaBr = "0.001" # pb
lhcAsymptoticRminBrLimit = "0.0" # plain number
## Default "Rmax" parameter for LHC-CLs (asymptotic)
lhcAsymptoticRmaxSigmaBr = "1.0" # pb
lhcAsymptoticRmaxBrLimit = "0.03" # plain number

## Default command line options for observed significance
lhcFreqSignificanceObserved = "-M ProfileLikelihood --significance --scanPoints 1000"
lhcFreqSignificanceExpected = lhcFreqSignificanceObserved + " -t -1 --toysFreq"
lhcFreqSignificanceExpectedSignalSigmaBr = "0.1" # pb
lhcFreqSignificanceExpectedSignalBrLimit = "0.01" # %
lhcFreqRmaxSigmaBr = "1.0" # pb
lhcFreqRmaxBrLimit = "0.1" # %


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

#class ParseLandsOutput:
#def parseLandsMLOutput(outputFileName):


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

## Run Combine for the LHC-CLs asymptotic limit
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
                         postfix="",
                         returnResult=False
                         ):

    cls = clsType
    if clsType == None:
        cls = LHCTypeAsymptotic(opts.brlimit, opts.sigmabrlimit)

    print "Computing limits with %s CLs flavour" % cls.nameHuman()
    print "Computing limits with Combine version %s" % Combine_tag

    mcc = MultiCrabCombine(opts, directory, massPoints, datacardPatterns, rootfilePatterns, cls)
    mcc.createMultiCrabDir(postfix)
    mcc.copyInputFiles()
    mcc.writeScripts()
    mcc.runCombineForAsymptotic(returnResult=returnResult)

## Class to generate (LEP-CLs, LHC-CLs) multicrab configuration, or run (LHC-CLs asymptotic) LandS
#
# The class is not intended to be used directly by casual user, but
# from generateMultiCrab() and produceLHCAsymptotic()
class MultiCrabCombine(commonLimitTools.LimitMultiCrabBase):
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
        self.exe = "combine"
        self.configuration["Combine_tag"] = Combine_tag

    ## Create the multicrab task directory
    #
    # \param postfix   Additional string to be included in the directory name
    def createMultiCrabDir(self, postfix):
        prefix = "CombineMultiCrab"
        self._createMultiCrabDir(prefix, postfix)

    ## Run Combine for the asymptotic limit
    #
    # This is so fast at the moment that using crab jobs for that
    # would be waste of resources and everybodys time.
    def runCombineForAsymptotic(self, returnResult=False):
        if not returnResult:
            print "Running Combine for asymptotic limits, saving results to %s" % self.dirname
        f = open(os.path.join(self.dirname, "configuration.json"), "wb")
        json.dump(self.configuration, f, sort_keys=True, indent=2)
        f.close()

        results = commonLimitTools.ResultContainer(self.opts.unblinded, self.dirname)
        for mass in self.massPoints:
            myResult = self.clsType.runCombine(mass)
            if myResult.failed:
                if not returnResult:
                    print "Fit failed for mass point %s, skipping ..." % mass
            else:
                results.append(myResult)
                if not returnResult:
                    print "Processed successfully mass point %s" % mass
        if not returnResult:
            print
            results.print2()
            fname = results.saveJson()
            print "Wrote results to %s" % fname
        else:
            return results

## Adds to the commands list the necessary commands and returns the input datacard name
#
# \brlimit               Boolean, set to true to calculate Br limit on light charged Higgs
# \param mass            String for the mass point
# \param datacardFiles   List of strings for datacard file names of the mass point
# \param commands        List of strings of the commands to run Combine
def _addCombinePreparationCommands(brlimit,datacardFiles,mass,commands):
    # Join datacards if necessary
    myInputName = datacardFiles[0]
    if len(datacardFiles) > 1:
        myInputName = "combinedCardsM%s.txt"%mass
        commands.append("combineCards.py %s > %s"%(" ".join(map(str,datacardFiles)),myInputName))
    # Create workspace with light H+ physics model, if necessary
    if brlimit:
        myNewInputName = "workspaceM%s.root"%mass
        commands.append("text2workspace.py %s -P HiggsAnalysis.CombinedLimit.ChargedHiggs:brChargedHiggs -o %s"%(myInputName,myNewInputName))
        myInputName = myNewInputName
    return myInputName

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
    #
    # Note: if you add any parameters to the constructor, add the
    # parameters to the clone() method correspondingly.
    def __init__(self, opts, optionsObservedAndExpected=None, optionsBlinded=None, rMin=None, rMax=None):
        self.opts = opts
        self.brlimit = opts.brlimit
        self.sigmabrlimit = opts.sigmabrlimit

        self.optionsObservedAndExpected = aux.ValuePerMass(aux.ifNotNoneElse(optionsObservedAndExpected, lhcAsymptoticOptionsObserved))
        self.optionsBlinded = aux.ValuePerMass(aux.ifNotNoneElse(optionsBlinded, lhcAsymptoticOptionsBlinded))
        if self.brlimit:
            self.rMin = aux.ValuePerMass(aux.ifNotNoneElse(rMin, lhcAsymptoticRminBrLimit))
            self.rMax = aux.ValuePerMass(aux.ifNotNoneElse(rMax, lhcAsymptoticRmaxBrLimit))
        elif self.sigmabrlimit:
            self.rMin = aux.ValuePerMass(aux.ifNotNoneElse(rMin, lhcAsymptoticRminSigmaBr))
            self.rMax = aux.ValuePerMass(aux.ifNotNoneElse(rMax, lhcAsymptoticRmaxSigmaBr))

        self.obsAndExpScripts = {}
        self.blindedScripts = {}
        self.mlfitScripts = {}
        self.significanceScripts = {}

    ## Return the name of the CLs flavour (for serialization to configuration.json)
    def name(self):
        return "LHCAsymptotic"

    ## Return human-readable name of the CLs flavour
    def nameHuman(self):
        return "LHC-type asymptotic"

    ## Get the configuration dictionary for serialization.
    #
    # LHC-type asymptotic CLs does not need any specific information to be stored
    def getConfiguration(self):
        return None

    ## Clone the object, possibly overriding some options
    #
    # \param kwargs   Keyword arguments, can be any of the arguments of
    #                 __init__(), with the same meaning.
    def clone(self, **kwargs):
        args = aux.updateArgs(kwargs, self, ["opts", "optionsObservedAndExpected", "optionsBlinded", "rMin", "rMax"])
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
        if self.opts.unblinded:
            self._createObsAndExp(mass, datacardFiles)
        else:
            self._createBlinded(mass, datacardFiles)
        if self.opts.significance:
            self._createSignificance(mass, datacardFiles)

    ## Create the observed and expected job script for a single mass point
    #
    # \param mass            String for the mass point
    # \param datacardFiles   List of strings for datacard file names of the mass point
    def _createObsAndExp(self, mass, datacardFiles):
        fileName = "runCombine_LHCasy_ObsAndExp_m" + mass
        opts = ""
        opts += " " + self.optionsObservedAndExpected.getValue(mass)
        opts += " --rMin %s"%self.rMin.getValue(mass)
        opts += " --rMax %s"%self.rMax.getValue(mass)
        opts += " -m %s"%mass
        opts += " -n obs_m%s"%mass
#        if self.brlimit:
#            opts += " --rAbsAcc 0.00001" # increase accuracy of calculation for br limit
        command = ["#!/bin/sh", ""]
        # Combine cards and prepare workspace for physics model, if necessary
        myInputDatacardName = _addCombinePreparationCommands(self.brlimit, datacardFiles, mass, command)
        # Add command for running combine
        command.append("combine %s -d %s" % (opts, myInputDatacardName))
        aux.writeScript(os.path.join(self.dirname, fileName), "\n".join(command)+"\n")
        self.obsAndExpScripts[mass] = fileName
        self._createMLFit(mass, fileName, myInputDatacardName, blindedMode=False)

    ## Create the expected job script for a single mass point
    #
    # \param mass            String for the mass point
    # \param datacardFiles   List of strings for datacard file names of the mass point
    def _createBlinded(self, mass, datacardFiles):
        fileName = "runCombine_LHCasy_Blinded_m" + mass
        opts = ""
        opts += " " + self.optionsBlinded.getValue(mass)
        opts += " --rMin %s"%self.rMin.getValue(mass)
        opts += " --rMax %s"%self.rMax.getValue(mass)
        opts += " -m %s"%mass
        opts += " -n blinded_m%s"%mass
#        if self.brlimit:
#            opts += " --rAbsAcc 0.00001" # increase accuracy of calculation for br limit
        command = ["#!/bin/sh", ""]
        # Combine cards and prepare workspace for physics model, if necessary
        myInputDatacardName = _addCombinePreparationCommands(self.brlimit, datacardFiles, mass, command)
        # Add command for running combine
        command.append("combine %s -d %s" % (opts, myInputDatacardName))
        aux.writeScript(os.path.join(self.dirname, fileName), "\n".join(command)+"\n")
        self.blindedScripts[mass] = fileName
        self._createMLFit(mass, fileName, myInputDatacardName, blindedMode=True)

    def _createMLFit(self, mass, fileName, datacardName, blindedMode):
        if self.opts.nomlfit:
            print "skipping creation of ML fit scripts, to enable run without --nomlfit"
            return
          
        fname = fileName.replace("runCombine", "runCombineMLFit")
        outputdir = "mlfit_m%s" % mass
        opts = "-M MaxLikelihoodFit"
        opts += " -m %s" % mass
        opts += " --out %s" % outputdir
        # From https://github.com/cms-analysis/HiggsAnalysis-HiggsToTauTau/blob/master/scripts/limit.py
        #opts += " --minimizerAlgo minuit"
        opts += " --robustFit=1 --X-rtd FITTER_NEW_CROSSING_ALGO --minimizerAlgoForMinos=Minuit2 --minimizerToleranceForMinos=0.01 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --minimizerAlgo=Minuit2 --minimizerStrategy=0 --minimizerTolerance=0.001 --cminFallbackAlgo \"Minuit,0:0.001\" --keepFailures" # following options may not suit for us? --preFitValue=1.
        command = ["#!/bin/sh", ""]
        command.append("mkdir -p %s" % outputdir)
        command.append("combine %s %s" % (opts, datacardName))

        opts = "-a"
        if self.brlimit:
            opts += " -p BR"
        opts2 = opts + " -g mlfit_m%s_pulls.png" % mass
        command.append("python %s/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py %s %s/mlfit.root > %s/diffNuisances.txt" % (os.environ["CMSSW_BASE"], opts2, outputdir, outputdir))
        opts += " -A"
        opts2 = opts + " --vtol 1.0 --stol 0.99 --vtol2 2.0 --stol2 0.99" 
        command.append("python %s/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py %s %s/mlfit.root > %s/diffNuisances_largest_pulls.txt" % (os.environ["CMSSW_BASE"], opts2, outputdir, outputdir))
        opts2 = opts + " --vtol 99. --stol 0.50 --vtol2 99. --stol2 0.90" 
        command.append("python %s/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py %s %s/mlfit.root > %s/diffNuisances_largest_constraints.txt" % (os.environ["CMSSW_BASE"], opts2, outputdir, outputdir))
        command.append("combineReadMLFit.py -f %s/diffNuisances.txt -c configuration.json -m %s -o mlfit.json" % (outputdir, mass))
        opts3 = ""
        if blindedMode:
            opts3 = " --bkgonlyfit"
        else:
            opts3 = " --sbfit"
        #if int(mass) > 173:
        #    opts3 += " --heavy"
        command.append("python %s/src/HiggsAnalysis/HeavyChHiggsToTauNu/test/brlimit/plotMLFits.py -m %s %s" % (os.environ["CMSSW_BASE"], mass, opts3))
        
        aux.writeScript(os.path.join(self.dirname, fname), "\n".join(command)+"\n")

        self.mlfitScripts[mass] = fname

    ## Create the observed significance for a single mass point
    #
    # \param mass            String for the mass point
    # \param datacardFiles   List of strings for datacard file names of the mass point
    def _createSignificance(self, mass, datacardFiles):
        if self.opts.unblinded:
            fileName = "runCombineSignif_ObsAndExp_m" + mass
        else:
            fileName = "runCombineSignif_Exp_m" + mass

        opts = " -m %s"%mass
        opts += " -n signif_m%s"%mass
        if self.brlimit:
            opts += " --rMin %s --rMax %s" % (lhcAsymptoticRminBrLimit, lhcFreqRmaxBrLimit)
        else:
            opts += " --rMin %s --rMax %s" % (lhcAsymptoticRminSigmaBr, lhcFreqRmaxSigmaBr)
            
        command = ["#!/bin/sh", ""]
        # Combine cards and prepare workspace for physics model, if necessary
        myInputDatacardName = _addCombinePreparationCommands(self.brlimit, datacardFiles, mass, command)
        # Add command for running combine
        tmpfile = "signif_%s_data.txt" % mass
        # First expected
        optsExpected = lhcFreqSignificanceExpected + opts
        if self.brlimit:
            optsExpected += " --expectSignal %s" % lhcFreqSignificanceExpectedSignalBrLimit
        else:
            optsExpected += " --expectSignal %s" % lhcFreqSignificanceExpectedSignalSigmaBr

        command.append("combine %s -d %s" % (optsExpected, myInputDatacardName))
        command.append("echo '#### PVALUE AFTER THIS LINE ###'")
        command.append("combine %s --pvalue -d %s" % (optsExpected, myInputDatacardName))
        # then observed
        if self.opts.unblinded:
            command.append("echo '#### OBSERVED AFTER THIS LINE ###'")
            optsObserved = lhcFreqSignificanceObserved + opts
            command.append("combine %s -d %s" % (optsObserved, myInputDatacardName))
            command.append("echo '#### PVALUE AFTER THIS LINE ###'")
            command.append("combine %s --pvalue -d %s" % (optsObserved, myInputDatacardName))

        # command.append("combine %s -d %s >%s 2>&1" % (opts, myInputDatacardName, tmpfile))
        # command.append("echo '#### PVALUE AFTER THIS LINE ###' >>%s 2>&1" % tmpfile)
        # # For some reason with combine trying to append truncates...
        # command.append("combine %s -d %s --pvalue >%s_tmp 2>&1" % (opts, myInputDatacardName, tmpfile))
        # command.append("cat %s_tmp >> %s" % (tmpfile, tmpfile))
        # command.append("rm %s_tmp" % tmpfile)
        # command.append("combineReadSignificance.py -f %s -m %s -o significance.json" % (tmpfile, mass))
        aux.writeScript(os.path.join(self.dirname, fileName), "\n".join(command)+"\n")
        self.significanceScripts[mass] = fileName

    ## Run LandS for the observed and expected limits for a single mass point
    #
    # \param mass   String for the mass point
    #
    # \return Result object containing the limits for the mass point
    def runCombine(self, mass):
        result = commonLimitTools.Result(mass)
        if self.opts.limit:
            if self.opts.unblinded:
                self._runObservedAndExpected(result, mass)
            else:
                self._runBlinded(result, mass)
        else:
            print "Skipping limit for mass:", mass
        self._runMLFit(mass)
        self._runSignificance(mass)
        return result

    ## Helper method to run a script
    #
    # \param script      Path to the script to run
    # \param outputfile  Path to a file to store the script output
    #
    # \return The output of the script as a string
    def _run(self, script, outputfile):
        #exe = landsInstall.findExe()
        pwd = os.getcwd()
        os.chdir(self.dirname)

        p = subprocess.Popen(["./"+script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = p.communicate()[0]
        if p.returncode != 0:
            print output
            raise Exception("Combine failed with exit code %d\nCommand: %s" % (p.returncode, script))
        os.chdir(pwd)

        f = open(os.path.join(self.dirname, outputfile), "w")
        f.write(output)
        f.write("\n")
        f.close()

        return output

    ## Extracts the result from combine output
    #
    # \param result  Result object to modify
    # \param mass    Mass
    # \return number of matches found
    def _parseResultFromCombineOutput(self, result, mass):
        # Find combine output root file
        possibleNames = ["higgsCombineobs_m%s.Asymptotic.mH%s.root"%(mass,mass),
                         "higgsCombineblinded_m%s.Asymptotic.mH%s.root"%(mass,mass),
                        ]
        name = None
        for n in possibleNames:
            if os.path.exists(os.path.join(self.dirname,n)):
                name = os.path.join(self.dirname,n)
        if name == None:
            raise Exception("Error: Could not find combine output root file! (checked: %s)"%", ".join(map(str, possibleNames)))
        # Open root file
        f = ROOT.TFile.Open(name)
        myTree = f.Get("limit")
        x = array.array('d', [0])
        myTree.SetBranchAddress("limit",x)
        myResultList = []
        if myTree == None:
            raise Exception("Error: Cannot open TTree in file '%s'!"%name)
        for i in range(0, myTree.GetEntries()):
            myTree.GetEvent(i)
            myResultList.append(x[0])
        f.Close()
        # Store results
        result.expectedMinus2Sigma = myResultList[0]
        result.expectedMinus1Sigma = myResultList[1]
        result.expected = myResultList[2]
        result.expectedPlus1Sigma = myResultList[3]
        result.expectedPlus2Sigma = myResultList[4]
        if len(myResultList) == 6:
            result.observed = myResultList[5]
        return len(myResultList)
        #nMatches = 0
        #lines = output.split("\n")
        #if self.brlimit:
            #obsresult_re = re.compile("Observed Limit: BR < \s*(?P<value>\d+\.\d+)")
        #elif self.sigmabrlimit:
            #obsresult_re = re.compile("Observed Limit: r < \s*(?P<value>\d+\.\d+)")
        #expresult_re = None
        #if self.brlimit:
            #expresult_re = re.compile("Expected \s*(?P<quantile>\d+\.\d+)%: BR < \s*(?P<value>\d+\.\d+)")
        #elif self.sigmabrlimit:
            #expresult_re = re.compile("Expected \s*(?P<quantile>\d+\.\d+)%: r < \s*(?P<value>\d+\.\d+)")
        #myExp = []
        #for line in lines:
            #if line.startswith("Observed"):
                #match = obsresult_re.search(line)
                #if match:
                    #result.observed = match.group("value")
                    #nMatches += 1
            #elif line.startswith("Expected"):
                #match = expresult_re.search(line)
                #if match:
                    #myExp.append(match.group("value"))
                    #nMatches += 1
            #if line.startswith("fail") or line.startswith("Fail"):
                #print line
                #result.failed = True
                #return -1
        #if not len(myExp) == 5:
            #print output
            #raise Exception("Oops, was expecting 5 values for expected")
        #result.expectedMinus2Sigma = myExp[0]
        #result.expectedMinus1Sigma = myExp[1]
        #result.expected = myExp[2]
        #result.expectedPlus1Sigma = myExp[3]
        #result.expectedPlus2Sigma = myExp[4]
        #return nMatches

    ## Run LandS for the observed limit
    #
    # \param result  Result object to modify
    # \param mass    String for the mass point
    def _runObservedAndExpected(self, result, mass):
        script = self.obsAndExpScripts[mass]
        output = self._run(script, "obsAndExp_m%s_output.txt"%mass)
        n = self._parseResultFromCombineOutput(result, mass)
        if n == 6: # 1 obs + 5 exp values
            return result
        if n < 0: # fit failed
            return result
        print output
        raise Exception("Unable to parse the output of command '%s'" % script)

    ## Run LandS for the expected limit
    #
    # \param result  Result object to modify
    # \param mass    String for the mass point
    def _runBlinded(self, result, mass):
        script = self.blindedScripts[mass]
        output = self._run(script, "blinded_m%s_output.txt"%mass)
        n = self._parseResultFromCombineOutput(result, mass)
        
        if n == 5: # 5 exp values
            return result
        if n < 0: # fit failed
            return result

        print output
        raise Exception("Unable to parse the output of command '%s'" % script)

    def _runMLFit(self, mass):
        if mass in self.mlfitScripts.keys():
            script = self.mlfitScripts[mass]
            self._run(script, "mlfit_m_%s_output.txt" % mass)
        else:
            print "Skipping ML fit for mass:",mass

    def _runSignificance(self, mass):
        jsonFile = os.path.join(self.dirname, "significance.json")

        if os.path.exists(jsonFile):
            f = open(jsonFile)
            result = json.load(f)
            f.close()
        else:
            result = {
                "expectedSignalBrLimit": lhcFreqSignificanceExpectedSignalBrLimit,
                "expectedSignalSigmaBr": lhcFreqSignificanceExpectedSignalSigmaBr
            }
        if mass in self.significanceScripts:
            script = self.significanceScripts[mass]
            output = self._run(script, "signif_m_%s_output.txt" % mass)
            result[mass] = parseSignificanceOutput(mass, outputString=output)

        f = open(jsonFile, "w")
        json.dump(result, f, sort_keys=True, indent=2)
        f.close()

def parseDiffNuisancesOutput(outputFileName, configFileName, mass):
    # first read nuisance types from datacards
    f = open(configFileName)
    config = json.load(f)
    f.close()
    datacardFiles = [dc % mass for dc in config["datacards"]]

    nuisanceTypes = {}
    type_re = re.compile("\s*(?P<name>\S+)\s+(?P<type>\S+)\s+[\d-]")
    for dc in datacardFiles:
        f = open(dc)
        # rewind until rate
        for line in f:
            if line[0:4] == "rate":
                break
        for line in f:
            m = type_re.search(line)
            if m:
                aux.addToDictList(nuisanceTypes, m.group("name"), m.group("type"))

    # then read the fit values
    f = open(outputFileName)

    ret_bkg = {}
    ret_sbkg = {}
    ret_rho = {}

    nuisanceNames = []

    num1 = "[+-]\d+.\d+"
    num2 = "\d+.\d+"
    nuis_re = re.compile("(?P<name>\S+)\s+(!|\*)?\s+(?P<bshift>%s),\s+(?P<bunc>%s)\s*(!|\*)?\s+(!|\*)?\s+(?P<sbshift>%s),\s+(?P<sbunc>%s)\s*(!|\*)?\s+(?P<rho>%s)" % (num1, num2, num1, num2, num1))
    for line in f:
        m = nuis_re.search(line)
        if m:
            nuisanceNames.append(m.group("name"))
            nuisanceType = nuisanceTypes.get(m.group("name"), None)
            if nuisanceType is not None and len(nuisanceType) == 1:
                nuisanceType = nuisanceType[0]
            if "statBin" in m.group("name"):
                nuisanceType = "shapeStat"
            if nuisanceType is None:
                nuisanceType = "unknown"
            ret_bkg[m.group("name")] = {"fitted_value": m.group("bshift"),
                                        "fitted_uncertainty": m.group("bunc"),
                                        "type": nuisanceType}
            ret_sbkg[m.group("name")] = {"fitted_value": m.group("sbshift"),
                                         "fitted_uncertainty": m.group("sbunc"),
                                         "type": nuisanceType}
            ret_rho[m.group("name")] = {"value": m.group("rho")}

    f.close()

    ret_bkg["nuisanceParameters"] = nuisanceNames
    ret_sbkg["nuisanceParameters"] = nuisanceNames

    return (ret_bkg, ret_sbkg, ret_rho)

def parseSignificanceOutput(mass, outputFileName=None, outputString=None):
    if outputFileName is None and outputString is None:
        raise Exception("Must give either outputFileName or outputString")
    if outputFileName is not None and outputString is not None:
        raise Exception("Must not give both outputFileName and outputString")

    content = []
    if outputFileName is not None:
        f = open(outputFileName)
        content = f.readlines()
        f.close()
    else:
        content = outputString.split("\n")

    # Read the significance values

    fl = "[+-]?\d+\.?\d*(e[+-]?\d+)?"

    signif_re = re.compile("Significance: (?P<signif>%s)" % fl)
    pvalue_re = re.compile("p-value of background: (?P<pvalue>%s)" % fl)

    signif_exp = None
    pvalue_exp = None
    signif_obs = None
    pvalue_obs = None

    signif = None
    pvalue = None

    def error(message):
        if outputFileName is not None:
            raise Exception("%s from file %s" % (message, outputFileName))
        print "Combine output"
        print outputString
        raise Exception("%s from the combine output (see above)" % message)

    for line in content:
        if "OBSERVED AFTER THIS LINE" in line:
            if signif is None:
                error("Expected significance not found")
            if pvalue is None:
                error("Expected p-value not found")
            signif_exp = signif
            pvalue_exp = pvalue
            signif = None
            pvalue = None

        m = signif_re.search(line)
        if m:
            if signif is not None:
                raise Exception("Significance already found, line %s" % line)
            signif = m.group("signif")
            continue
        m = pvalue_re.search(line)
        if m:
            if pvalue is not None:
                raise Exception("P-value already found, line %s" % line)
            pvalue = m.group("pvalue")

    if signif_exp is None:
        signif_exp = signif
        pvalue_exp = pvalue
    else:
        signif_obs = signif
        pvalue_obs = pvalue

    if signif_exp is None:
        error("Expected significance not found")
    if pvalue_exp is None:
        error("Expected p-value not found")

    ret = {"expected": {"significance": signif_exp,
                        "pvalue": pvalue_exp}}
    if signif_obs is not None:
        if pvalue_obs is None:
            error("Found observed significance but not pvalue")
        ret["observed"] = {"significance": signif_obs,
                           "pvalue": pvalue_obs}

    return ret
