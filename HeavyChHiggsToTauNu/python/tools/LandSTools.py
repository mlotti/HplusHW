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

lepHybridOptions = "-M Hybrid --bQuickEstimateInitialLimit 0"
lepHybridToys = 50
lepHybridRmin = "0"
lepHybridRmax = "0.09"

lhcHybridOptions = "-M Hybrid --freq --ExpectationHints Asymptotic --scanRs 1 --PLalgorithm Migrad --maximumFunctionCallsInAFit 500000 --minuitSTRATEGY 1"
lhcHybridToysCLsb = 300
lhcHybridToysCLb = 150
lhcHybridRmin = "0"
lhcHybridRmax = "1"

lhcAsymptoticOptions = "-M Asymptotic --maximumFunctionCallsInAFit 500000"
lhcAsymptoticRmin = "0"
lhcAsymptoticRmax = "1"

defaultOptions = lepHybridOptions
defaultNumberOfJobs = 20

defaultFirstSeed = 1000

allMassPoints = ["80", "100", "120", "140", "150", "155", "160"]
defaultMassPoints = ["120"]

# Patterns of input files, %s denotes the place of the mass
taujetsDatacardPattern = "lands_datacard_hplushadronic_m%s.txt"
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

def generateMultiCrab(massPoints=defaultMassPoints,
                      datacardPatterns=defaultDatacardPatterns,
                      rootfilePatterns=defaultRootfilePatterns,
                      clsType=None,
                      numberOfJobs=None,
                      crabScheduler="arc",
                      crabOptions={},
                      postfix=""
                      ):
    cls = clsType
    if clsType == None:
        cls = LEPType()

    njobs = ValuePerMass(_ifNotNoneElse(numberOfJobs, defaultNumberOfJobs))

    lands = MultiCrabLandS(massPoints, datacardPatterns, rootfilePatterns, cls)
    lands.createMultiCrabDir(postfix)
    lands.copyLandsInputFiles()
    lands.writeLandsScripts()
    lands.writeCrabCfg(crabScheduler, crabOptions)
    lands.writeMultiCrabCfg(njobs)
    lands.printInstruction()

def produceLHCAsymptotic(massPoints=defaultMassPoints,
                         datacardPatterns=defaultDatacardPatterns,
                         rootfilePatterns=defaultRootfilePatterns,
                         clsType = None,
                         postfix=""
                         ):

    cls = clsType
    if clsType == None:
        cls = LHCTypeAsymptotic()

    lands = MultiCrabLandS(massPoints, datacardPatterns, rootfilePatterns, cls)
    lands.createMultiCrabDir(postfix)
    lands.copyLandsInputFiles()
    lands.writeLandsScripts()
    lands.runLandSForAsymptotic()

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
        clsConfig = self.clsType.getConfiguration()
        if clsConfig != None:
            self.configuration["clsConfig"] = clsConfig

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
        prefix = "LandSMultiCrab"
        if len(postfix) > 0:
            prefix += "_"+postfix
	self.dirname = multicrab.createTaskDir(prefix=prefix)
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
            inputFiles = [exe]+self.datacards[mass]
            if len(self.rootfiles) > 0:
                inputFiles += self.rootfiles[mass]
            self.clsType.writeMultiCrabConfig(fOUT, mass, inputFiles, numberOfJobs.getValue(mass))
            fOUT.write("\n\n")

        f = open(os.path.join(self.dirname, "configuration.json"), "wb")
        json.dump(self.configuration, f, sort_keys=True, indent=2)
        f.close()

    def printInstruction(self):
	print "Multicrab cfg created. Type"
        print "cd",self.dirname,"&& multicrab -create"


    def runLandSForAsymptotic(self):
        print "Running LandS for asymptotic limits, saving results to %s" % self.dirname
        f = open(os.path.join(self.dirname, "configuration.json"), "wb")
        json.dump(self.configuration, f, sort_keys=True, indent=2)
        f.close()

        results = ResultContainer(self.dirname)
        for mass in self.massPoints:
            results.append(self.clsType.runLandS(mass))
            print "Processed mass point %s" % mass
        print

        results.print2()
        fname = results.saveJson()
        print "Wrote results to %s" % fname

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

def _ifNotNoneElse(value, default):
    if value == None:
        return default
    return value

class ValuePerMass:
    def __init__(self, dictionary):
        self.values = {}
        if isinstance(dictionary, dict):
            self.values.update(dictionary)
            self.default = self.values["default"]
            del self.values["default"]
        elif isinstance(dictionary, ValuePerMass):
            self.values.update(dictionary.values)
            self.default = dictionary.default
        else:
            self.default = dictionary

    def forEachValue(self, function):
        function(self.default)
        for value in self.values.values():
            function(value)

    def getValue(self, mass):
        return self.values.get(mass, self.default)

    def serialize(self):
        ret = {"default": self.default}
        ret.update(self.values)
        return ret

class LEPType:
    def __init__(self, options=lepHybridOptions, toysPerJob=None, firstSeed=defaultFirstSeed, rMin=None, rMax=None):
        self.options = options
        self.firstSeed = firstSeed
        self.toysPerJob = ValuePerMass(_ifNotNoneElse(toysPerJob, lepHybridToys))
        self.rMin = ValuePerMass(_ifNotNoneElse(rMin, lepHybridRmin))
        self.rMax = ValuePerMass(_ifNotNoneElse(rMax, lepHybridRmax))

        self.expScripts = {}
        self.obsScripts = {}

    def name(self):
        return "LEP"

    def getConfiguration(self):
        return None

    def clone(self, **kwargs):
        args = _updateArgs(kwargs, self, ["options", "toysPerJob", "firstSeed", "rMin", "rMax"])
        return LEPType(**args)

    def setDirectory(self, dirname):
        self.dirname = dirname
        
    def createScripts(self, mass, datacardFiles):
        self._createObs(mass, datacardFiles)
        self._createExp(mass, datacardFiles)

    def _createObs(self, mass, datacardFiles):
        fileName = "runLandS_Observed_m" + mass
        opts = commonOptions + " " + self.options + " --initialRmin %s --initialRmax %s" % (self.rMin.getValue(mass), self.rMax.getValue(mass))
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
        _writeScript(os.path.join(self.dirname, fileName), "\n".join(command)+"\n")
        self.obsScripts[mass] = fileName

    def _createExp(self, mass, datacardFiles):
        fileName = "runLandS_Expected_m" + mass
        opts = commonOptions + " " + self.options + " --initialRmin %s --initialRmax %s" % (self.rMin.getValue(mass), self.rMax.getValue(mass))
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
        output.write("CMSSW.output_file = lands.out,split_m%sHybrid_limitbands.root,split_m%sHybrid_limits_tree.root\n" % (mass, mass))

    def getResult(self, path, mass, clsConfig):
        result = Result(mass)
        self._parseObserved(result, path, mass)
        self._parseExpected(result, path, mass)
        return result

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

    def _runLandSForMerge(self, resDir, mergedFilename, mass):
        targetFile = os.path.join(resDir, mergedFilename)
        if os.path.exists(targetFile):
            return True

        exe = findOrInstallLandS()
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

class LHCType:
    def __init__(self, options=lhcHybridOptions, toysCLsb=None, toysCLb=None, firstSeed=defaultFirstSeed, vR=None, rMin=None, rMax=None, scanRmin=None, scanRmax=None):
        self.options = lhcHybridOptions
        self.firstSeed = firstSeed

        self.toysCLsb = ValuePerMass(_ifNotNoneElse(toysCLsb, lhcHybridToysCLsb))
        self.toysCLb = ValuePerMass(_ifNotNoneElse(toysCLb, lhcHybridToysCLb))

        def assertvR(value):
            if value != None and len(value) != 2:
                raise Exception("vR should be pair (min, max), got length %d: %s" % (len(value), str(value)))
        self.vR = ValuePerMass(vR)
        self.vR.forEachValue(assertvR)

        self.rMin = ValuePerMass(_ifNotNoneElse(rMin, lhcHybridRmin))
        self.rMax = ValuePerMass(_ifNotNoneElse(rMax, lhcHybridRmax))

        self.scanRmin = ValuePerMass(scanRmin)
        self.scanRmax = ValuePerMass(scanRmax)
        self.configuration = {}
        self.configuration["scanRmin"] = self.scanRmin.serialize()
        self.configuration["scanRmax"] = self.scanRmax.serialize()

        self.scripts = {}

    def name(self):
        return "LHC"

    def getConfiguration(self):
        return self.configuration

    def clone(self, **kwargs):
        args = _updateArgs(kwargs, self, ["options", "toysCLsb", "toysCLb", "firstSeed", "vR", "rMin", "rMax", "scanRmin", "scanRmax"])
        return LHCType(**args)

    def setDirectory(self, dirname):
        self.dirname = dirname

    def createScripts(self, mass, datacardFiles):
        filename = "runLandS_m%s" % mass
        opts = commonOptions + " " + self.options + " --rMin %s --rMax %s" % (self.rMin.getValue(mass), self.rMax.getValue(mass))
        vR = self.vR.getValue(mass)
        if vR != None:
            opts += " -vR [%s,%s,x1.05]" % vR
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

        _writeScript(os.path.join(self.dirname, filename), "\n".join(command)+"\n")
        self.scripts[mass] = filename

    def writeMultiCrabConfig(self, output, mass, inputFiles, numJobs):
        output.write("[Limit_m%s]\n" % mass)
        output.write("USER.script_exe = %s\n" % self.scripts[mass])
        output.write("USER.additional_input_files = %s\n" % ",".join(inputFiles))
        output.write("CMSSW.number_of_jobs = %d\n" % numJobs)
        output.write("CMSSW.output_file = lands.out,split_m%s_m2lnQ.root\n" % mass)

    def getResult(self, path, mass, clsConfig):
        result = Result(mass)

        rootFile = os.path.join(path, "Limit_m%s"%mass, "res", "histograms-Limit_m%s.root"%mass)
        if not os.path.exists(rootFile):
            print "Merged root file '%s' does not exist, did you run landsMergeHistograms.py?" % rootFile
            return result

        fitScript = os.path.join(findOrInstallLandS(directory=True), "test", "fitRvsCLs.C")
        if not os.path.exists(fitScript):
            raise Exception("Did not find fit script '%s'" % fitScript)
        rootCommand = ["root", "-l", "-n", "-b", fitScript+"+"]
        p = subprocess.Popen(rootCommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        commands = []

        if clsConfig != None and "scanRmin" in clsConfig:
            scanRmin = ValuePerMass(clsConfig["scanRmin"])
            val = scanRmin.getValue(mass)
            if val != None:
                commands.append("scanRmin = %s" % val)
        if clsConfig != None and "scanRmax" in clsConfig:
            scanRmax = ValuePerMass(clsConfig["scanRmax"])
            val = scanRmax.getValue(mass)
            if val != None:
                commands.append("scanRmax = %s" % val)
        commands.extend([
            'run("%s", "plot_m%s")' % (rootFile, mass),
#            'run("%s", "plot_m%s", "bands", -1, 1)' % (rootFile, mass), # for debug output of the script
            ".q"
            ])
        output = p.communicate("\n".join(commands)+"\n")[0]
#        print output
        f = open(os.path.join(path, "fitRvsCLs_m%s_output.txt"%mass), "w")
        f.write(" ".join(rootCommand)+"\n\n")
        f.write("\n".join(commands)+"\n\n")
        f.write(output)
        f.write("\n")
        f.close()

        lines = output.split("\n")
        lines.reverse()
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

class LHCTypeAsymptotic:
    def __init__(self, options=lhcAsymptoticOptions, rMin=None, rMax=None, vR=None):
        self.options = options
        self.rMin = ValuePerMass(_ifNotNoneElse(rMin, lhcAsymptoticRmin))
        self.rMax = ValuePerMass(_ifNotNoneElse(rMax, lhcAsymptoticRmax))

        def assertvR(value):
            if value != None and len(value) != 2:
                raise Exception("vR should be pair (min, max), got length %d: %s" % (len(value), str(value)))
        self.vR = ValuePerMass(vR)
        self.vR.forEachValue(assertvR)

        self.obsScripts = {}
        self.expScripts = {}

    def name(self):
        return "LHCAsymptotic"

    def getConfiguration(self):
        return None

    def clone(self, **kwargs):
        args = _updateArgs(kwargs, self, ["options", "rMin", "rMax", "vR"])
        return LHCTypeAsymptotic(**args)

    def setDirectory(self, dirname):
        self.dirname = dirname

    def createScripts(self, mass, datacardFiles):
        self._createObs(mass, datacardFiles)
        self._createExp(mass, datacardFiles)

    def _createObs(self, mass, datacardFiles):
        fileName = "runLandS_Observed_m" + mass
        opts = commonOptions + " " + self.options + " --rMin %s --rMax %s" % (self.rMin.getValue(mass), self.rMax.getValue(mass))
        vR = self.vR.getValue(mass)
        if vR != None:
            opts += " -vR [%s,%s,x1.05]" % vR

        command = [
            "#!/bin/sh",
            "",
            "./lands.exe %s --minuitSTRATEGY 1 -n obs_m%s -d %s" % (opts, mass, " ".join(datacardFiles)),
            ]
        _writeScript(os.path.join(self.dirname, fileName), "\n".join(command)+"\n")
        self.obsScripts[mass] = fileName

    def _createExp(self, mass, datacardFiles):
        fileName = "runLandS_Expected_m" + mass
        opts = commonOptions + " " + self.options + " --rMin %s --rMax %s" % (self.rMin.getValue(mass), self.rMax.getValue(mass))
        vR = self.vR.getValue(mass)
        if vR != None:
            opts += " -vR [%s,%s,x1.05]" % vR

        command = [
            "#!/bin/sh",
            "",
            "./lands.exe %s --minuitSTRATEGY 2 --PLalgorithm Migrad -n exp_m%s -D asimov_b -d %s" % (opts, mass, " ".join(datacardFiles)),
            ]
        _writeScript(os.path.join(self.dirname, fileName), "\n".join(command)+"\n")
        self.expScripts[mass] = fileName

    def runLandS(self, mass):
        result = Result(mass)
        self._runObserved(result, mass)
        self._runExpected(result, mass)
        return result

    def _run(self, script, outputfile):
        exe = findOrInstallLandS()
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

class Result:
    def __init__(self, mass = None, observed = None, expected = None, expectedPlus1Sigma = None, expectedPlus2Sigma = None, expectedMinus1Sigma = None, expectedMinus2Sigma = None):
        self.mass                = mass
        self.observed            = observed
        self.expected            = expected
        self.expectedPlus1Sigma  = expectedPlus1Sigma
        self.expectedPlus2Sigma  = expectedPlus2Sigma
        self.expectedMinus1Sigma = expectedMinus1Sigma
        self.expectedMinus2Sigma = expectedMinus2Sigma

    def toFloat(self):
        for attr in ["mass", "observed", "expected", "expectedPlus1Sigma", "expectedPlus2Sigma", "expectedMinus1Sigma", "expectedMinus2Sigma"]:
            setattr(self, attr, float(getattr(self, attr)))

    def empty(self):
        return self.observed == None and self.expected == None


    def Exists(self, result):
        if self.mass == result.mass:
            return True
        return False
        
    def Add(self, result):
        if self.mass == result.mass:
            if self.observed == None:
                self.observed = result.observed
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


class ResultContainer:
    def __init__(self, path):
        self.path = path

        # Read task configuration json file
        configFile = os.path.join(path, "configuration.json")
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
            self.readLuminosityTaujets(taujetsDc % self.config["masspoints"][0])
        else:
            self.readLuminosityLeptonic(self.config["datacards"][0] % self.config["masspoints"][0])

        self.results = []

    def append(self, obj):
        self.results.append(obj)

    def readLuminosityTaujets(self, filename):
        lumi_re = re.compile("luminosity=[\S| ]*(?P<lumi>\d+\.\d+)")
        fname = os.path.join(self.path, filename)
        f = open(fname)
        for line in f:
            match = lumi_re.search(line)
            if match:
                self.lumi = str(1000*float(match.group("lumi"))) # 1/fb -> 1/pb
                f.close()
                return
        raise Exception("Did not find luminosity information from '%s'" % fname)

    def readLuminosityLeptonic(self, filename):
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
            raise Exception("Did not find luminosity information from '%s'" % fname)
        if scale != None:
            lumi *= scale
        self.lumi = str(lumi)

    def getLuminosity(self):
        return self.lumi

    def print2(self):
        print
        print "                  Expected"
        print "Mass  Observed    Median       -2sigma     -1sigma     +1sigma     +2sigma"
        format = "%3s:  %-9s   %-10s   %-10s  %-10s  %-10s  %-10s"
        massIndex = [(int(self.results[i].mass), i) for i in range(len(self.results))]
        massIndex.sort()
        for mass, index in massIndex:
            result = self.results[index]
            if result.empty():
                continue
            print format % (result.mass, result.observed, result.expected, result.expectedMinus2Sigma, result.expectedMinus1Sigma, result.expectedPlus1Sigma, result.expectedPlus2Sigma)
        print
    
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
        self.results = ResultContainer(self.path)
        try:
            clsConfig = self.config["clsConfig"]
        except KeyError:
            clsConfig = None
        for mass in self.config["masspoints"]:
            self.results.append(self.clsType.getResult(self.path, mass, clsConfig))
            print "Processed mass point %s" % mass


#	self.subdir_re         = re.compile("(?P<label>(Expected|Observed)_m)(?P<mass>(\d*$))")
#	self.landsRootFile_re  = re.compile("histograms-Expected_m(?P<mass>(\d*))\.root$")
#	self.landsOutFile_re   = re.compile("lands(?P<label>(\S*|_merged))\.out$")
#	self.landsObsResult_re = re.compile("= (?P<value>\d+\.\d+)\s+\+/-\s+(?P<error>\d+\.\S+)")
#	self.landsExpResult_re = re.compile("BANDS    (?P<minus2>(\d*\.\d*))(    )(?P<minus1>(\d*\.\d*))(    )(?P<mean>(\d*\.\d*))(    )(?P<plus1>(\d*\.\d*))(    )(?P<plus2>(\d*\.\d*))(    )(?P<median>(\d*\.\d*))")

    def getLuminosity(self):
	return self.results.getLuminosity()

    def Print(self):
	for result in self.results.results:
	    result.Print()

    def Save(self, dOUT):
	outputFileNaming = "output_lands_datacard_hplushadronic_m"

	if not os.isdir(dOUT):
            os.mkdir(dOUT)

	print "Saving in",dOUT
	for result in self.results.results:
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
        self.results.print2()

    def saveJson(self):
        fname = self.results.saveJson()
        print "Wrote results to %s" % fname

    def Data(self):
	return self.results.results


def findOrInstallLandS(directory=False):
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

        if directory:
            return landsDirAbs
        else:
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

        if directory:
            return landsDirAbs
        else:
            return landsExe
