#!/usr/bin/env python

import os
import re
import sys
import glob
import stat
import json
import random
import shutil
import subprocess

import multicrab
import git

#LandS_tag           = "V3-04-01_eps" # this one is in the Tapio's scripts
#LandS_tag           = "t3-04-13"
LandS_tag	    = "HEAD" # Recommended by Mingshui 10.5.2012 at 23:23:22 EEST

commonOptions  = "--PhysicsModel ChargedHiggs"

lepHybridOptions = "-M Hybrid --bQuickEstimateInitialLimit 0 --initialRmin 0. --initialRmax 0.09"
lepHybridToys = 50

lhcHybridOptions = "-M Hybrid --freq --ExpectationHints Asymptotic --scanRs 1 --freq --PLalgorithm Migrad --rMin 0 --maximumFunctionCallsInAFit 500000 --minuitSTRATEGY 1 --rMax 1"
lhcHybridToysCLsb = 300
lhcHybridToysCLb = 150


defaultOptions = lepHybridOptions
defaultNumberOfJobs = 20

defaultFirstSeed = 1000

allMassPoints = ["80", "100", "120", "140", "150", "155", "160"]
defaultMassPoints = ["120"]

# Patterns of input files, %s denotes the place of the mass
LandSDataCardNaming = "lands_datacard_hplushadronic_m"
taujetsDatacardPattern = LandSDataCardNaming+"%s.txt"
mutauDatacardPattern = "datacard_m%s_mutau_miso_20mar12.txt"
etauDatacardPattern = "datacard_m%s_etau_miso_20mar12.txt"
emuDatacardPattern = "datacard_m%s_emu_nobtag_20mar12.txt"

taujetsRootfilePattern = "lands_histograms_hplushadronic_m%s.root"

defaultDatacardPatterns = [
    taujetsDatacardPattern,
    emuDatacardPattern,
    etauDatacardPattern,
    mutauDatacardPattern
    ]
defaultDatacardPatterns = [defaultDatacardPatterns[i] for i in [3, 1, 0, 2]] # order in my first crab tests

defaultRootfilePatterns = [
    taujetsRootfilePattern
]

datacard_hadr_re = re.compile(LandSDataCardNaming+"(?P<mass>\d+)\.txt$")
script_re   = re.compile("runLandS_(?P<label>(Observed|Expected)_m)(?P<mass>\d+)")
luminosity_re = re.compile("luminosity=[\S| ]*(?P<lumi>\d+\.\d+)")

def generateMultiCrab(massPoints=defaultMassPoints,
                      datacardPatterns=defaultDatacardPatterns,
                      rootfilePatterns=defaultRootfilePatterns,
                      clsType = None,
                      numberOfJobs=defaultNumberOfJobs,
                      crabScheduler="arc",
                      crabOptions={},
                      postfix=""
                      ):
    cls = clsType
    if clsType == None:
        cls = LEPType()

    lands = MultiCrabLandS(massPoints, datacardPatterns, rootfilePatterns, cls)
    lands.createMultiCrabDir(postfix)
    lands.copyLandsInputFiles()
    lands.writeLandsScripts()
    lands.writeCrabCfg(crabScheduler, crabOptions)
    lands.writeMultiCrabCfg(numberOfJobs)
    lands.printInstruction()

       

class MultiCrabLandS:
    def __init__(self, massPoints, datacardPatterns, rootfilePatterns, clsType):
        self.exe = findOrInstallLandS()
        self.clsType = clsType.clone()

        self.massPoints = massPoints
        self.datacards = {}
        self.rootfiles = {}
        self.scripts   = []

        # this is a dictionary dumped to configuration.json
        self.configuration = {
            "masspoints": massPoints,
            "datacards": datacardPatterns,
            "rootfiles": rootfilePatterns,
            "landsVersion": LandS_tag,
            "codeVersion": git.getCommitId(),
            "clsType": self.clsType.name(),
        }

        for mass in self.massPoints:
            for dc in datacardPatterns:
                fname = dc % mass
                if not os.path.isfile(fname):
                    raise Exception("Datacard file '%s' does not exist!" % fname)

                multicrab._addToDictList(self.datacards, mass, fname)

            for rf in rootfilePatterns:
                fname = rf % mass
                if not os.path.isfile(fname):
                    raise Exception("ROOT file (for shapes) '%s' does not exist!" % fname)

                multicrab._addToDictList(self.rootfiles, mass, fname)

        if len(self.datacards) == 0:
	    print "No LandS datacards found in this directory!"
            print "Mass points:", ", ".join(self.massPoints)
            print "Datacard patterns:", ", ".join(datacardPatterns)
            print "Rootfile patterns:", ", ".join(rootfilePatterns)
	    sys.exit(1)

    def createMultiCrabDir(self, postfix):
	self.dirname = multicrab.createTaskDir(prefix="LandSMultiCrab", postfix=postfix)
        self.clsType.setDirectory(self.dirname)

    def copyLandsInputFiles(self):
        for d in [self.datacards, self.rootfiles]:
            for mass, files in d.iteritems():
                for f in files:
                    shutil.copy(f, self.dirname)
        shutil.copy(self.exe, self.dirname)        

    def writeLandsScripts(self):
        for mass, datacardFiles in self.datacards.iteritems():
            self.clsType.createScripts(mass, datacardFiles)

    def writeCrabCfg(self, crabScheduler, crabOptions):
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
        fOUT.write("output_file             = lands.out\n")
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
            self.clsType.writeMultiCrabConfig(fOUT, mass, [exe]+self.datacards[mass]+self.rootfiles[mass], numberOfJobs)
            fOUT.write("\n\n")

        f = open(os.path.join(self.dirname, "configuration.json"), "wb")
        json.dump(self.configuration, f, sort_keys=True, indent=2)
        f.close()

    def printInstruction(self):
	print "Multicrab cfg created. Type"
        print "cd",self.dirname,"&& multicrab -create"


def _updateArgs(kwargs, obj, names):
    for k in kwargs.keys():
        if not k in names:
            raise Exception("Unknown keyword argument '%s', known arguments are %s" % ", ".join(names))

    args = {}
    for n in names:
        args[n] = kwargs.get(n, getattr(obj, n))
    return args

def _writeScript(filename, content):
    fOUT = open(filename, 'w')
    fOUT.write(content)
    fOUT.close()

    # make the script executable
    st = os.stat(filename)
    os.chmod(filename, st.st_mode | stat.S_IXUSR)


class LEPType:
    def __init__(self, options=lepHybridOptions, toysPerJob=lepHybridToys, firstSeed=defaultFirstSeed):
        self.options = options
        self.toysPerJob = toysPerJob
        self.firstSeed = firstSeed

        self.expScripts = {}
        self.obsScripts = {}

    def name(self):
        return "LEP"

    def clone(self, **kwargs):
        args = _updateArgs(kwargs, self, ["options", "toysPerJob", "firstSeed"])
        return LEPType(**args)

    def setDirectory(self, dirname):
        self.dirname = dirname
        
    def createScripts(self, mass, datacardFiles):
        self._createObs(mass, datacardFiles)
        self._createExp(mass, datacardFiles)

    def _createObs(self, mass, datacardFiles):
        fileName = "runLandS_Observed_m" + mass
        command = [
            "#!/bin/sh",
            "",
            "SEED=$(expr %d + $1)" % self.firstSeed,
            'echo "LandSSeed=$SEED"',
            "",
            "./lands.exe %s %s --seed $SEED -d %s | tail -5 > lands.out" % (commonOptions, self.options, " ".join(datacardFiles)),
            ""
            "cat lands.out"
            ]
        _writeScript(os.path.join(self.dirname, fileName), "\n".join(command)+"\n")
        self.obsScripts[mass] = fileName

    def _createExp(self, mass, datacardFiles):
        fileName = "runLandS_Expected_m" + mass
        command = [
            "#!/bin/sh",
            "",
            "SEED=$(expr %d + $1)" % self.firstSeed,
            'echo "LandSSeed=$SEED"',
            "",
            "./lands.exe %s %s -n split_m%s --doExpectation 1 %s --seed $SEED -d %s | tail -5 > lands.out" % (commonOptions, self.options, mass, self.toysPerJob, " ".join(datacardFiles)),
            "",
            "cat lands.out",
            ]
        _writeScript(os.path.join(self.dirname, fileName), "\n".join(command)+"\n")
        self.expScripts[mass] = fileName
    
    def writeMultiCrabConfig(self, output, mass, inputFiles, numJobs):
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
        output.write("CMSSW.output_file = lands.out,split_m%s_limitbands.root,split_m%s_limits_tree.root\n" % (mass, mass))

class LHCType:
    def __init__(self, options=lhcHybridOptions, toysCLsb=lhcHybridToysCLsb, toysCLb=lhcHybridToysCLb, firstSeed=defaultFirstSeed):
        self.options = lhcHybridOptions
        self.toysCLsb = toysCLsb
        self.toysCLb = toysCLb
        self.firstSeed = firstSeed

        self.scripts = {}

    def name(self):
        return "LEP"

    def clone(self, **kwargs):
        args = _updateArgs(kwargs, self, ["options", "toysCLsb", "toysCLb", "firstSeed"])
        return LHCType(**args)

    def setDirectory(self, dirname):
        self.dirname = dirname

    def createScripts(self, mass, datacardFiles):
        filename = "runLandS_m%s" % mass
        command = [
            "#!/bin/sh",
            "",
            "SEED=$(expr %d + $1)" % self.firstSeed,
            'echo "LandSSeed=$SEED"',
            "",
            "./lands.exe %s %s --seed $SEED -d %s | tail -5 > lands.out" % (commonOptions, self.options, " ".join(datacardFiles)),
            ""
            "cat lands.out"
            ]

        _writeScript(os.path.join(self.dirname, filename), "\n".join(command)+"\n")
        self.scripts[mass] = filename

    def writeMultiCrabConfig(self, output, mass, inputFiles, numJobs):
        output.write("[Mass_%s]\n" % mass)
        output.write("USER.script_exe = %s\n" % self.scripts[mass])
        output.write("USER.additional_input_files = %s\n" % ",".join(inputFiles))
        output.write("CMSSW.number_of_jobs = %d\n" % numJobs)
        output.write("CMSSW.output_file = lands.out,split_m%s_m2lnQ.root\n" % mass)


class Result:
    def __init__(self, mass = None, observed = None, observedError = None, expected = None, expectedPlus1Sigma = None, expectedPlus2Sigma = None, expectedMinus1Sigma = None, expectedMinus2Sigma = None):
        self.mass                = mass
        self.observed            = observed
        self.observedError       = observedError
        self.expected            = expected
        self.expectedPlus1Sigma  = expectedPlus1Sigma
        self.expectedPlus2Sigma  = expectedPlus2Sigma
        self.expectedMinus1Sigma = expectedMinus1Sigma
        self.expectedMinus2Sigma = expectedMinus2Sigma

    def toFloat(self):
        for attr in ["mass", "observed", "expected", "expectedPlus1Sigma", "expectedPlus2Sigma", "expectedMinus1Sigma", "expectedMinus2Sigma"]:
            setattr(self, attr, float(getattr(self, attr)))
        

    def Exists(self, result):
        if self.mass == result.mass:
            return True
        return False
        
    def Add(self, result):
        if self.mass == result.mass:
            if self.observed == None:
                self.observed = result.observed
                self.observedError = result.observedError
            if self.expected == None:
                self.expected            = result.expected
                self.expectedPlus1Sigma  = result.expectedPlus1Sigma
                self.expectedPlus2Sigma  = result.expectedPlus2Sigma
                self.expectedMinus1Sigma = result.expectedMinus1Sigma
                self.expectedMinus2Sigma = result.expectedMinus2Sigma
  
    def Print(self):
        print "Mass = ",self.mass
        print "    Observed = ",self.observed
        print "    Expected = ",self.expected
        print "     -1sigma = ",self.expectedMinus1Sigma," +1sigma = ",self.expectedPlus1Sigma
        print "     -2sigma = ",self.expectedMinus2Sigma," +2sigma = ",self.expectedPlus2Sigma
#        print "     +1sigma = ",self.expectedPlus1Sigma," -1sigma = ",self.expectedMinus1Sigma
#        print "     +2sigma = ",self.expectedPlus2Sigma," -2sigma = ",self.expectedMinus2Sigma


def ConvertToErrorBands(result):
    return Result(float(result.mass),
                  float(result.observed),
                  float(result.expected),
                  float(result.expectedPlus1Sigma) - float(result.expected),
                  float(result.expectedPlus2Sigma) - float(result.expected), 
                  float(result.expected) - float(result.expectedMinus1Sigma),
                  float(result.expected) - float(result.expectedMinus2Sigma))

class ParseLandsOutput:
    def __init__(self, path):
	self.path = path
	self.lumi = 0

	self.results = []
	self.subdir_re         = re.compile("(?P<label>(Expected|Observed)_m)(?P<mass>(\d*$))")
	self.landsRootFile_re  = re.compile("histograms-Expected_m(?P<mass>(\d*))\.root$")
	self.landsOutFile_re   = re.compile("lands(?P<label>(\S*|_merged))\.out$")
	self.landsObsResult_re = re.compile("= (?P<value>\d+\.\d+)\s+\+/-\s+(?P<error>\d+\.\S+)")
#	self.landsObsResult_re = re.compile("= *(?P<value>(\d*\.\d*))")
	self.landsExpResult_re = re.compile("BANDS    (?P<minus2>(\d*\.\d*))(    )(?P<minus1>(\d*\.\d*))(    )(?P<mean>(\d*\.\d*))(    )(?P<plus1>(\d*\.\d*))(    )(?P<plus2>(\d*\.\d*))(    )(?P<median>(\d*\.\d*))")

	subdirs = []
	dirs = glob.glob(os.path.join(self.path, "*"))
	for dir in dirs:
	    datacard_match = datacard_hadr_re.search(dir)
	    if datacard_match:
		self.ReadLuminosity(dir)
	    if os.path.isdir(dir):
		match = self.subdir_re.search(dir)
		if match:
		    subdirs.append(dir)
	if len(subdirs) == 0:
	    print "No data found, is the directory '" + path + "' a multicrab dir? Exiting.."
	    sys.exit()

	self.Read(subdirs)

    def ReadLuminosity(self, dir):
	if self.lumi == 0:
	    fIN = open(dir,"r")
	    for line in fIN:
		match = luminosity_re.search(line)
		if match:
#		    print line
		    self.lumi = match.group("lumi")
		    return
		print line

    def GetLuminosity(self):
	return self.lumi

    def Read(self,dirs):
	for dir in dirs:
	    if os.path.isdir(dir):
		match = self.subdir_re.search(dir)
		if match:
		    self.AddResult(dir)

	self.Sort()

    def Sort(self):
	i = len(self.results)
	while i > 1:
	    if self.Compare(self.results[i-1],self.results[i-2]):
		self.Swap(i-1,i-2)
	    i = i - 1

    def Compare(self, results1, results2):
	return results1.mass < results2.mass
	
    def Swap(self, i, j):
	tmp = self.results[i]
	self.results[i] = self.results[j]
	self.results[j] = tmp

    def AddResult(self, dir):
        result = self.ReadDir(dir)
        if not self.ResultExists(result):
            self.results.append(result)
        else:
            self.MergeResult(result)

    def ReadDir(self,dir):
	match = self.subdir_re.search(dir)
	if match:
	    mass  = match.group("mass")
	    result = Result(mass) # filling the mass
	    label = match.group("label")
	    if label.find("Observed") == 0:
		result = self.ParseObsFile(result,dir)
	    if label.find("Expected") == 0:
		self.RunLandSFromMergedFile(dir)
	        result = self.ParseExpFile(result,dir)
	    return result

    def ResultExists(self, result):
	for r in self.results:
	    if r.Exists(result):
		return True
	return False

    def MergeResult(self, result):
	for r in self.results:
	    if r.Exists(result):
		r.Add(result)
		return

    def ParseObsFile(self, result, dir):
        files = glob.glob(os.path.join(dir, "res", "*"))
	for file in files:
	    file_match = self.landsOutFile_re.search(file)
	    if file_match:
		fIN = open(file, 'r')
		for line in fIN:
		    result_match = self.landsObsResult_re.search(line)
		    if result_match:
			result.observed = result_match.group("value")
                        result.observedError = result_match.group("error")
                        break
		fIN.close()
		break
	return result

    def RunLandSFromMergedFile(self, dir):
	fOUT = "lands_merged.out"
	if not self.FileExists(dir):

            exe = findOrInstallLandS()

            files = glob.glob(os.path.join(dir, "res", "*"))
	    for file in files:
	        match = self.landsRootFile_re.search(file)
	        if match:
		    fIN = dir + "/res/" + match.group(0)
	            command = exe +" --doExpectation 1 --readLimitsFromFile " + fIN + " > " + dir + "/res/" + fOUT
	            os.system(command)
		    return

    def ParseExpFile(self, result, dir):
        f = os.path.join(dir, "res", "lands_merged.out")
        fIN = open(f)
        for line in fIN:
            result_match = self.landsExpResult_re.search(line)
            if result_match:
#                result.expected = result_match.group("mean")
		result.expected = result_match.group("median")
		result.expectedPlus1Sigma  = result_match.group("plus1")
		result.expectedPlus2Sigma  = result_match.group("plus2")
		result.expectedMinus1Sigma = result_match.group("minus1")
		result.expectedMinus2Sigma = result_match.group("minus2")
        fIN.close()
	return result

    def FileExists(self, dir):
        files = glob.glob(os.path.join(dir, "res", "*"))
        found = False
        for file in files:
            file_match = self.landsOutFile_re.search(file)
            if file_match:
                label = file_match.group("label")
                if label == "_merged":
                    found = True
        return found

    def Print(self):
	for result in self.results:
	    result.Print()

    def Save(self, dOUT):
	outputFileNaming = "output_lands_datacard_hplushadronic_m"

	if not os.isdir(dOUT):
            os.mkdir(dOUT)

	print "Saving in",dOUT
	for result in self.results:
	    fileName = outputFileNaming + result.mass
	    print "    ",fileName
	    fileName = dOUT + "/" + fileName
	    fOUT = open(fileName, 'w')
	    fOUT.write(str(result.observed) + "\n")
	    fOUT.write(str(result.expectedMinus2Sigma) + " " + \
                       str(result.expectedMinus1Sigma) + " " + \
                       str(result.expected) + " " + \
                       str(result.expectedPlus1Sigma) + " " + \
                       str(result.expectedPlus2Sigma))
	    fOUT.close()

    def print2(self):
        print
        print "                  Expected"
        print "Mass  Observed    Median    -2sigma  -1sigma  +1sigma  +2sigma"
        massIndex = [(int(self.results[i].mass), i) for i in range(len(self.results))]
        massIndex.sort()
        for mass, index in massIndex:
            result = self.results[index]
            print "%3s:  %-9s   %6s   %6s  %6s  %6s  %6s" % (result.mass, result.observed, result.expected, result.expectedMinus2Sigma, result.expectedMinus1Sigma, result.expectedPlus1Sigma, result.expectedPlus2Sigma)
        print


    def saveJson(self):
        output = {
            "luminosity": self.GetLuminosity(),
            "masspoints": {}
            }
        massIndex = [(int(self.results[i].mass), i) for i in range(len(self.results))]
        massIndex.sort()
        for mass, index in massIndex:
            result = self.results[index]
            output["masspoints"][result.mass] = {
                "mass": result.mass,
                "observed": result.observed,
                "observed_error": result.observedError,
                "expected": {
                    "-2sigma": result.expectedMinus2Sigma,
                    "-1sigma": result.expectedMinus1Sigma,
                    "median": result.expected,
                    "+1sigma": result.expectedPlus1Sigma,
                    "+2sigma": result.expectedPlus2Sigma,
                    }
                }

        fname = os.path.join(self.path, "limits.json")
        f = open(fname, "wb")
        json.dump(output, f, sort_keys=True, indent=2)
        f.close()
        print "Wrote results to %s" % fname

    def Data(self):
	return self.results

def findOrInstallLandS():
    try:
        cmsswBase = os.environ["CMSSW_BASE"]
    except KeyError:
        raise Exception("Did you 'cmsenv'? I can't find $CMSSW_BASE environment variable")

    brlimitBase = os.path.join(cmsswBase, "src", "HiggsAnalysis", "HeavyChHiggsToTauNu", "test", "brlimit")
    landsDir = "LandS_"+LandS_tag
    landsDirAbs = os.path.join(brlimitBase, landsDir)
    landsExe = os.path.join(landsDirAbs, "test", "lands.exe")
    if os.path.exists(landsDirAbs):
        if not os.path.isfile(landsExe):
            raise Exception("Found LandS directory in '%s', but not lands.exe in '%s'" % (landsDirAbs, landsExe))
        return landsExe
    else:
        pwd = os.getcwd()
        os.chdir(brlimitBase)

        command = ["cvs", "checkout", "-r", LandS_tag, "-d", landsDir, "UserCode/mschen/LandS"]
        ret = subprocess.call(command)
        if ret != 0:
            raise Exception("cvs checkout failed (exit code %d), command '%s'" % (ret, " ".join(command)))
        if not os.path.exists(landsDir):
            raise Exception("cvs checkout failed to create directory '%s' under '%s'" % (brlimitBase, landsDir))

        os.chdir(landsDir)
        ret = subprocess.call(["make", "clean"])
        if ret != 0:
            raise Exception("Compiling LandS failed (exit code %d), command 'make clean'" % ret)
        ret = subprocess.call(["make"])
        if ret != 0:
            raise Exception("Compiling LandS failed (exit code %d), command 'make'" % ret)

        if not os.path.isfile(landsExe):
            raise Exception("After LandS checkout and compilation, the lands.exe is not found in '%s'" % landsExe)

        os.chdir(pwd)

        return landsExe
