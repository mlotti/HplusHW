## \package CommonLimitTools
# Python interface common for LandS and Combine and running them with multicrab
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

import os
import re
import sys
import glob
import stat
import json
import time
import random
import shutil
import subprocess

from optparse import OptionParser
import HiggsAnalysis.NtupleAnalysis.tools.multicrab as multicrab
#import multicrabWorkflows
import HiggsAnalysis.NtupleAnalysis.tools.git as git
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux


class GeneralSettings():
    def __init__(self, directory, masspoints):
        self.datacardPatterns = {}
        self.rootfilePatterns = {}
        self.massPoints = {}

        ## Pattern for tau+jets datacard files (%s denotes the place of the software string and the mass)
        self.datacardPatterns[LimitProcessType.TAUJETS] = "%s_datacard_hplushadronic_m%s.txt"
        ## Pattern for tau+jets shape files (%s denotes the place of the software string and the mass)
        self.rootfilePatterns[LimitProcessType.TAUJETS] = "%s_histograms_hplushadronic_m%s.root"

        ## Default number of first random number seed in the jobs
        self.defaultFirstSeed = 1000
        ## Default number of crab jobs
        self.defaultNumberOfJobs = 20

        # Obtain software Id and string
        (mySoftwareId, mySoftwareString) = getSoftware(directory)
        self.setSoftware(mySoftwareString)
        self.softwareId = mySoftwareId

        # Obtain mass points
#        if len(masspoints) == 0:
#            print "Auto-detecting mass points"
        for key,value in self.datacardPatterns.iteritems():
            if len(masspoints) == 0:
                self.massPoints[key] = obtainMassPoints(value, directory)
            else:
                self.massPoints[key] = masspoints

    def setSoftware(self, software):
        for key in self.datacardPatterns:
            self.datacardPatterns[key] = self.datacardPatterns[key]%(software,"%s")
        for key in self.rootfilePatterns:
            self.rootfilePatterns[key] = self.rootfilePatterns[key]%(software,"%s")
        print "Limit calculation software set to: %s"%software

    def checkPatterns(self):
        for key in self.datacardPatterns:
            if self.datacardPatterns[key].count("%s") > 1:
                raise Exception("You forgot to call setSoftware()!")
        for key in self.rootfilePatterns:
            if self.rootfilePatterns[key].count("%s") > 1:
                raise Exception("You forgot to call setSoftware()!")

    def getDatacardPattern(self, limitProcessType):
        self.checkPatterns()
        return self.datacardPatterns[limitProcessType]

    def getRootfilePattern(self, limitProcessType):
        self.checkPatterns()
        return self.rootfilePatterns[limitProcessType]

    def getDatacardName(self, limitProcessType, mass):
        self.checkPatterns()
        return self.datacardPatterns[limitProcessType]%mass

    def getRootfileName(self, mass):
        self.checkPatterns()
        return self.rootfilePatterns[limitProcessType]%mass

    def getFirstSeed(self):
        return self.defaultFirstSeed

    def getNumberOfGridJobs(self):
        return self.defaultNumberOfJobs

    def isLands(self):
        return self.softwareId == LimitSoftwareType.LANDS

    def isCombine(self):
        return self.softwareId == LimitSoftwareType.COMBINE

    def getMassPoints(self, limitProcessType):
        return self.massPoints[limitProcessType]

class LimitSoftwareType:
    LANDS = 0
    COMBINE = 1

class LimitProcessType:
    TAUJETS = 0

## Returns the software to which the datacards are compatible to
def getSoftware(directory="."):
    mySoftware = {}
    mySoftware[LimitSoftwareType.LANDS] = "lands"
    mySoftware[LimitSoftwareType.COMBINE] = "combine"
    myDir = directory
    if directory == None:
        myDir = "."
    elif isinstance(directory,list):
        myDir = directory[0]

    myList = os.listdir(myDir)
    for item in myList:
        for key,value in mySoftware.iteritems():
            if item.endswith(".txt") and "%s_datacard"%value in item:
                print "Datacards for limit calculation software '%s' auto-detected"%value
                return (key,value)
              
    
    print "Automatic detection of limit calculation software failed! Assuming combine :)"
    return (LimitSoftwareType.COMBINE, mySoftware[LimitSoftwareType.COMBINE])
    
## Deduces from directory listing the mass point list
def obtainMassPoints(pattern, directory):
    mass_re = re.compile(pattern%"(?P<mass>\S+)")
    myDir = directory
    if myDir == None:
        myDir = "."
    elif isinstance(directory, list):
        myDir = directory[0]
    myList = os.listdir(myDir)
    myMasses = []
    for item in myList:
        match = mass_re.search(item)
        if match:
            myMass = match.group("mass")
            if not myMass in myMasses:
                myMasses.append(myMass)
    myMasses.sort()
    return myMasses

## Reads luminosity from a datacard and returns it
def readLuminosityFromDatacard(myPath, filename):
    lumi_re = re.compile("luminosity=\s*(?P<lumi>\d+\.\d+)")
    fname = os.path.join(myPath, filename)
    f = open(fname)
    myLuminosity = None
    for line in f:
        match = lumi_re.search(line)
        if match:
            #self.lumi = str(1000*float(match.group("lumi"))) # 1/fb -> 1/pb
            # Nowadays the luminosity is in 1/pb
            myLuminosity = match.group("lumi")
            f.close()
            return myLuminosity
    print "Did not find luminosity information from '%s', using 0" % fname
    return 0.0

## Returns true if mass list contains only heavy H+
def isHeavyHiggs(massList):
    for m in massList:
        if int(m) < 175:
            return False
    return True

## Returns true if mass list contains only light H+
def isLightHiggs(massList):
    for m in massList:
        if int(m) > 175:
            return False
    return True

## Create OptionParser, and add common LandS options to OptionParser object
#
# \param lepDefault     Boolean for the default value of --lep switch (if None, switch is not added)
# \param lhcDefault     Boolean for the default value of --lhc switch (if None, switch is not added)
# \param lhcasyDefault  Boolean for the default value of --lhcasy switch (if None, switch is not added)
#
# \return optparse.OptionParser object
def createOptionParser(lepDefault=None, lhcDefault=None, lhcasyDefault=None, fullOptions=True):
    parser = OptionParser(usage="Usage: %prog [options]")

    # Switches for different CLs flavours, the interpretation of these
    # is in the generate* scripts (i.e. in the caller responsibility)
    if lepDefault != None:
        parser.add_option("--lep", dest="lepType", default=lepDefault, action="store_true",
                          help="Use hybrid LEP-CLs (default %s)" % str(lepDefault))
    if lhcDefault != None:
        parser.add_option("--lhc", dest="lhcType", default=lhcDefault, action="store_true",
                          help="Use hybrid LHC-CLs (default %s)" % str(lhcDefault))
    if lhcasyDefault != None:
        parser.add_option("--lhcasy", dest="lhcTypeAsymptotic", default=lhcasyDefault, action="store_true",
                          help="Use asymptotic LHC-CLs (default %s)" % str(lhcasyDefault))

    # Mu parameter selection
    parser.add_option("--brlimit", dest="brlimit", action="store_true", default=False, help="Calculate limit on Br(t->bH+)")
    parser.add_option("--sigmabrlimit", dest="sigmabrlimit", action="store_true", default=True, help="Calculate limit on sigma(H+)xBr(t->bH+)")

    # Datacard directories
    parser.add_option("-d", "--dir", dest="dirs", type="string", action="append", default=[],
                      help="Datacard directories to create the LandS MultiCrab tasks into (default: use the working directory")
    if fullOptions:
        parser.add_option("-m", "--mass", dest="masspoints", type="string", action="append", default=[],
                          help="Mass points to be considered (if none are specified, mass points are auto-detected")
        parser.add_option("--create", dest="multicrabCreate", action="store_true", default=False,
                          help="Run 'multicrab -create' for each multicrab task directory")

    parser.add_option("--final", dest="unblinded", action="store_true", default=False,
                      help="Do not set to true unless you know what you are doing and have permission to do so")

    parser.add_option("--significance", dest="significance", action="store_true", default=False,
                      help="Run also expected (and with --final also observed) significance")

    parser.add_option("--mlfit", dest="nomlfit", action="store_false", default=True,
                      help="Disable ML fit")
    parser.add_option("--nolimit", dest="limit", action="store_false", default=True,
                      help="Disable limit calculation (for e.g. just ML fit or significance)")
    parser.add_option("--rmin", dest="rmin", action="store", default=None,
                      help="minimum r parameter for finding limit")
    parser.add_option("--rmax", dest="rmax", action="store", default=None,
                      help="maximum r parameter for finding limit")

    parser.add_option("--injectSignal", dest="injectSignal", action="store_true", default=False,
                      help="Inject signal (implied by --injectSignalBRTop and --injectSignalBRHplus)")
    parser.add_option("--injectSignalBRTop", dest="injectSignalBRTop", type="string", default="0.0",
                      help="Inject signal with this BR(t -> H+)")
    parser.add_option("--injectSignalBRHplus", dest="injectSignalBRHplus", type="string", default="0.0",
                      help="Inject signal with this BR(H+ -> tau)")
    parser.add_option("--injectSignalMass", dest="injectSignalMass", type="string", default=None,
                      help="Inject signal with this mass")
    parser.add_option("--injectNumberToys", dest="injectNumberToys", type="int", default=100,
                      help="Number of toys per job for signal injection")
    parser.add_option("--injectNumberJobs", dest="injectNumberJobs", type="int", default=10,
                      help="Number of jobs per mass point for signal injection")

    return parser

## Parse OptionParser object
#
# \param parser   optparse.OptionParser object
#
# \return Options object
def parseOptionParser(parser):
    (opts, args) = parser.parse_args()
    if hasattr(opts,"dirs"):
        opts.dirs.extend(args)
        if len(opts.dirs) == 0:
            opts.dirs = ["."]
    # Check options
    n = 0
    s = ""
    if hasattr(opts, "lepType") and opts.lepType:
        s += "  --lep (Hybrid LEP type CLs, discouraged)\n"
        n += 1
    if hasattr(opts, "lhcType") and opts.lhcType:
        s += "  --lhc (Hybrid LHC type CLs, use for final limit, very slow)\n"
        n += 1
    if hasattr(opts, "lhcTypeAsymptotic") and opts.lhcTypeAsymptotic:
        s += "  --lhcasy (Asymptotic LHC type CLs, very quick)\n"
        n += 1
    if n == 0:
        parser.print_help()
        raise Exception("Error: Please specify limit type: \n%s"%s)
    if n > 1:
        parser.print_help()
        raise Exception("Error: Please specify only one limit type: \n%s"%s)
    if opts.brlimit == opts.sigmabrlimit:
        if opts.brlimit:
            opts.sigmabrlimit = False # if --brlimit is true, let it override --sigmabrlimit
#            raise Exception("Error: Please enable only --brlimit or --sigmabrlimit !")
        else:
            opt.sigmabrlimit = True # if not specified, choose --sigmabrlimit
#            raise Exception("Error: Please enable --brlimit or --sigmabrlimit !")
    if float(opts.injectSignalBRTop) > 0 or float(opts.injectSignalBRHplus) > 0:
        opts.injectSignal = True
    if opts.injectSignal:
        if opts.injectSignalMass is None:
            raise Exception("Signal injection enabled with --injectSignal, --injectSignalBRTop --injectSignalBRHplus, but injected mass point not specified with --injectSignalMass")
        opts.nomlfit = True
        opts.limit = False

    return opts

## Class to hold the limit results
class Result:
    ## Constructor
    def __init__(self, mass):
        self.mass                = mass
        self.observed            = None
        self.expected            = None
        self.failed              = False

    ## Check if the result is empty, i.e. no limits has been assigned
    def empty(self):
        return self.observed == None and self.expected == None

## Collection of Result objects
class ResultContainer:
    ## Constructor
    #
    # \param path  Path to the multicrab directory (where configuration.json exists)
    def __init__(self, unblindedStatus, path):
        self.unblindedStatus = unblindedStatus
        self.path = path

        # Read task configuration json file
        configFile = os.path.join(path, "configuration.json")
        if not os.path.exists(configFile):
            raise Exception("Error: Cannot open file '%s'!"%configFile)
        f = open(configFile)
        self.config = json.load(f)
        f.close()

        # Read the luminosity, use tau+jets one if that's available, if not, use the first one
        datacards = self.config["datacards"]
        taujetsDc = None
        for dc in datacards:
            if "hplushadronic" in dc:
                taujetsDc = dc
                break
        if taujetsDc != None:
            self._readLuminosityTaujets(taujetsDc % self.config["masspoints"][0])
        else:
            self._readLuminosityLeptonic(self.config["datacards"][0] % self.config["masspoints"][0])

        self.results = []

    ## Append a result object to the list
    #
    # \param obj   Result object
    def append(self, obj):
        self.results.append(obj)

    ## Read luminosity from a datacard assuming it follows the tau+jets convention
    #
    # \param filename  Name of the datacard file inside the multicrab directory
    def _readLuminosityTaujets(self, filename):
        self.lumi = readLuminosityFromDatacard(self.path, filename)

    ## Read luminosity from a datacard assuming it follows the leptonic convention
    #
    # \param filename  Name of the datacard file inside the multicrab directory
    #
    # \todo This needs to be updated, it get's the scale wrong
    def _readLuminosityLeptonic(self, filename):
        scale_re = re.compile("lumi scale (?P<scale>\S+)")
        lumi_re = re.compile("lumi=(?P<lumi>\S+)")
        scale = None
        lumi = None

        fname = os.path.join(self.path, filename)
        f = open(fname)
        for line in f:
            match = scale_re.search(line)
            if match:
                scale = float(match.group("scale"))
                continue
            match = lumi_re.search(line)
            if match:
                lumi = float(match.group("lumi"))
                break
        f.close()
        if lumi == None:
            #raise Exception("Did not find luminosity information from '%s'" % fname)
            self.lumi = "0.0"
            print "Did not find luminosity information from '%s', assuming 0.0" % fname
            return
        if scale != None:
            lumi *= scale
        self.lumi = str(lumi)

    ## Get the integrated luminosity as a string in 1/pb
    def getLuminosity(self):
        return self.lumi

    ## Print the limits
    def print2(self):
        print ""
        print "                  Expected"
        print "Mass  Observed    Median       -2sigma     -1sigma        +1sigma     +2sigma"
        format = "%3s:  %-9s   %-10s   %-10s  %-10s  %-10s  %-10s"
        massIndex = [(int(self.results[i].mass), i) for i in range(len(self.results))]
        massIndex.sort()
        for mass, index in massIndex:
            result = self.results[index]
            if result.empty():
                continue
            if self.unblindedStatus:
                print format % (result.mass, result.observed, result.expected, result.expectedMinus2Sigma, result.expectedMinus1Sigma, result.expectedPlus1Sigma, result.expectedPlus2Sigma)
            else:
                print format % (result.mass, "BLINDED", result.expected, result.expectedMinus2Sigma, result.expectedMinus1Sigma, result.expectedPlus1Sigma, result.expectedPlus2Sigma)
        print ""

    def getResultString(self,mass):
        for result in self.results:
            if result.mass == mass:
                if self.unblindedStatus:
                    return "%.4f (observed) vs. %.4f (expected median)" % (result.observed, result.expected)
                else:
                    return "%.4f (expected median)" % result.expected
    

    ## Store the results in a limits.json file
    #
    # \param data   Dictionary of additional data to be stored
    def saveJson(self, data={}):
        output = {}
        output.update(data)
        output.update({
                "luminosity": self.getLuminosity(),
                "masspoints": {}
                })

        massIndex = [(int(self.results[i].mass), i) for i in range(len(self.results))]
        massIndex.sort()
        for mass, index in massIndex:
            result = self.results[index]
            if result.empty():
                continue

            if self.unblindedStatus:
                output["masspoints"][result.mass] = {
                    "mass": result.mass,
                    "observed": result.observed,
                    "expected": {
                        "-2sigma": result.expectedMinus2Sigma,
                        "-1sigma": result.expectedMinus1Sigma,
                        "median": result.expected,
                        "+1sigma": result.expectedPlus1Sigma,
                        "+2sigma": result.expectedPlus2Sigma,
                        }
                    }
            else:
                output["masspoints"][result.mass] = {
                    "mass": result.mass,
                    "observed": 0,
                    "expected": {
                        "-2sigma": result.expectedMinus2Sigma,
                        "-1sigma": result.expectedMinus1Sigma,
                        "median": result.expected,
                        "+1sigma": result.expectedPlus1Sigma,
                        "+2sigma": result.expectedPlus2Sigma,
                        }
                    }

            if self.unblindedStatus:
                if hasattr(result, "observedError"):
                    output["masspoints"][result.mass]["observed_error"] = result.observedError
            if hasattr(result, "expectedError"):
                output["masspoints"][result.mass]["expected"].update({
                        "-2sigma_error": result.expectedMinus2SigmaError,
                        "-1sigma_error": result.expectedMinus1SigmaError,
                        "median_error": result.expectedError,
                        "+1sigma_error": result.expectedPlus1SigmaError,
                        "+2sigma_error": result.expectedPlus2SigmaError,
                        })


        fname = os.path.join(self.path, "limits.json")
        f = open(fname, "wb")
        json.dump(output, f, sort_keys=True, indent=2)
        f.close()
        return fname


## Base class to generate (LEP-CLs, LHC-CLs) multicrab configuration, or run (LHC-CLs asymptotic)
#
# The class is not intended to be used directly by casual user, but
# from generateMultiCrab() and produceLHCAsymptotic()
class LimitMultiCrabBase:
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
        self.opts = opts
        self.datacardDirectory = directory
        self.massPoints = massPoints
        self.datacardPatterns = datacardPatterns
        self.rootfilePatterns = rootfilePatterns
        self.clsType = clsType.clone()
        self.jobsCreated = False
        self.datacards = {}
        self.rootfiles = {}
        self.scripts   = []
        self.configuration = {}

        if not os.path.isdir(directory):
            raise Exception("Datacard directory '%s' does not exist" % directory)

        # this is a dictionary dumped to configuration.json
        self.configuration = {
            "masspoints": massPoints,
            "datacards": datacardPatterns,
            "rootfiles": rootfilePatterns,
            "codeVersion": git.getCommitId(),
            "clsType": self.clsType.name(),
        }
        clsConfig = self.clsType.getConfiguration(self.configuration)
        if clsConfig != None:
            self.configuration["clsConfig"] = clsConfig

        for mass in self.massPoints:
            for dc in datacardPatterns:
                fname = None
                if "%s" in dc:
                    fname = os.path.join(self.datacardDirectory, dc % mass)
                else:
                    fname = os.path.join(self.datacardDirectory, dc)
                if not os.path.isfile(fname):
                    raise Exception("Datacard file '%s' does not exist!" % fname)

                aux.addToDictList(self.datacards, mass, fname)

            for rf in rootfilePatterns:
                if rf != None:
                    rfname = None
                    if "%s" in rf:
                        rfname = os.path.join(self.datacardDirectory, rf % mass)
                    else:
                        rfname = os.path.join(self.datacardDirectory, rf)
                    if not os.path.isfile(rfname):
#                        raise Exception("ROOT file (for shapes) '%s' does not exist!" % rfname)
                        print("\033[91mWarning:  ROOT file (for shapes) '%s' does not exist!\033[00m" % rfname)
                    aux.addToDictList(self.rootfiles, mass, rfname)

    ## Create the multicrab task directory
    #
    # \param postfix   Additional string to be included in the directory name
    def _createMultiCrabDir(self, prefix, postfix):
        if len(postfix) > 0:
            prefix += "_"+postfix
        self.dirname = multicrab.createTaskDir(prefix=prefix, path=self.datacardDirectory)
        self.clsType.setDirectory(self.dirname)

    ## Copy input files for LandS/Combine (datacards, rootfiles) to the multicrab directory
    def copyInputFiles(self):
        for d in [self.datacards, self.rootfiles]:
            for mass, files in d.iteritems():
                for f in files:
                    if os.path.isfile(f):
                        shutil.copy(f, self.dirname)
#                    else:
#                        print("\033[91mWarning: File '%s' was not copied into result directory, because the file does not exist!\033[00m" % f)
        # Copy exe file only for LandS
        if os.path.exists(self.exe):
            shutil.copy(self.exe, self.dirname)

    ## Write  shell scripts to the multicrab directory
    def writeScripts(self):
        for mass, datacardFiles in self.datacards.iteritems():
            self.clsType.createScripts(mass, datacardFiles)
        if self.opts.unblinded:
            return self.clsType.obsAndExpScripts
        else:
            return self.clsType.blindedScripts

    ## Write crab.cfg to the multicrab directory
    # \param crabScheduler      CRAB scheduler to use
    # \param crabOptions        Dictionary for specifying additional CRAB
    #                           options. The keys correspond to the
    #                           sections in crab.cfg. The values are lists
    #                           containing lines to be appended to the
    #                           section.
    # \param outputFile         list of output files
    def writeCrabCfg(self, crabScheduler, crabOptions, outputFile):
        filename = os.path.join(self.dirname, "crab.cfg")
        fOUT = open(filename,'w')
        fOUT.write("[CRAB]\n")
        fOUT.write("jobtype                 = cmssw\n")
        fOUT.write("scheduler               = %s\n" % crabScheduler)
        fOUT.write("use_server              = 0\n")
        if "CRAB" in crabOptions:
            for line in crabOptions["CRAB"]:
                fOUT.write(line+"\n")
        fOUT.write("\n")

        fOUT.write("[CMSSW]\n")
        fOUT.write("datasetpath             = none\n")
        fOUT.write("pset                    = none\n")
        fOUT.write("number_of_jobs          = 1\n")
        fOUT.write("output_file             = %s\n"%",".join(outputFile))
        if "CMSSW" in crabOptions:
            for line in crabOptions["CMSSW"]:
                fOUT.write(line+"\n")
        fOUT.write("\n")

        fOUT.write("[USER]\n")
        fOUT.write("return_data             = 1\n")
        fOUT.write("copy_data               = 0\n")
        if "USER" in crabOptions:
            for line in crabOptions["USER"]:
                fOUT.write(line+"\n")
        fOUT.write("\n")

        if "GRID" in crabOptions:
            fOUT.write("[GRID]\n")
            for line in crabOptions["GRID"]:
                fOUT.write(line+"\n")
            fOUT.write("\n")

        fOUT.close()

    ## Write multicrab.cfg to the multicrab directory
    #
    # \param numberOfJobs   ValuePerMass object holding the information
    #                       of number of crab jobs (per mass point)
    def writeMultiCrabCfg(self, numberOfJobs):
        filename = os.path.join(self.dirname, "multicrab.cfg")
        fOUT = open(filename,'w')
        fOUT.write("[COMMON]\n")
        fOUT.write("CRAB.use_server              = 0\n")
        fOUT.write("CMSSW.datasetpath            = none\n")
        fOUT.write("CMSSW.pset                   = none\n")
        fOUT.write("\n")

        exe = self.exe.split("/")[-1]
        for mass in self.massPoints:
            inputFiles = [exe]+self.datacards[mass]
            if len(self.rootfiles) > 0:
                inputFiles += self.rootfiles[mass]
            if numberOfJobs != None:
                self.clsType.writeMultiCrabConfig(self.opts, fOUT, mass, inputFiles, numberOfJobs.getValue(mass))
            else:
                self.clsType.writeMultiCrabConfig(self.opts, fOUT, mass, inputFiles, 1)
            fOUT.write("\n\n")

        f = open(os.path.join(self.dirname, "configuration.json"), "wb")
        json.dump(self.configuration, f, sort_keys=True, indent=2)
        f.close()

        print "Wrote multicrab.cfg to %s" % self.dirname

    ## Run 'multicrab create' inside the multicrab directory
    def createMultiCrab(self):
        print "Creating multicrab task %s" % self.dirname
        print
        print "############################################################"
        print
        pwd = os.getcwd()
        os.chdir(self.dirname)
        ret = subprocess.call(["multicrab", "-create"])
        if ret != 0:
            raise Exception("'multicrab -create' failed with exit code %d in directory '%s'" % (ret, self.dirname))
        os.chdir(pwd)
        print
        print "############################################################"
        print

        self.jobsCreated = True

    def printInstruction(self):
        if self.jobsCreated:
            print "Multicrab cfg and jobs created. Type"
            print "cd %s && multicrab -submit" % self.dirname
        else:
            print "Multicrab cfg created. Type"
            print "cd %s && multicrab -create" % self.dirname


#def generateMultiCrab(opts,
                      #massPoints=defaultMassPoints,
                      #datacardPatterns=defaultDatacardPatterns,
                      #rootfilePatterns=defaultRootfilePatterns,
                      #clsType=None,
                      #numberOfJobs=None,
                      #crabScheduler="arc",
                      #crabOptions={},
                      #postfix=""
                      #):
#def produceLHCAsymptotic(opts,
                         #massPoints=defaultMassPoints,
                         #datacardPatterns=defaultDatacardPatterns,
                         #rootfilePatterns=defaultRootfilePatterns,
                         #clsType = None,
                         #postfix=""
                         #):

## Helper class to manage mass-specific configuration values
#class LEPType:
#class LHCType:
#class LHCTypeAsymptotic:
#class ParseLandsOutput:
#def parseLandsMLOutput(outputFileName):
#class LandSInstaller:

