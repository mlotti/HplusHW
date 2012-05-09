#!/usr/bin/env python

import os
import re
import sys
import glob
import random
import shutil
import subprocess
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab

#LandS_tag           = "t3-04-13"
LandS_tag	    = "HEAD"
#LandS_options       = "--PhysicsModel ChargedHiggs  -M Hybrid --bQuickEstimateInitialLimit 0 --initialRmin 0.01 --initialRmax 0.05"
LandS_options       = "--PhysicsModel ChargedHiggs  -M Hybrid --bQuickEstimateInitialLimit 0 --initialRmin 0. --initialRmax 0.09"
#LandS_options       = "--PhysicsModel ChargedHiggs  -M Hybrid --bQuickEstimateInitialLimit 0 --initialRmin 0. --initialRmax 0.09 --tH 40000"
#LandS_options       = "--PhysicsModel ChargedHiggs  -M Hybrid --bQuickEstimateInitialLimit 0 --initialRmin 0. --initialRmax 0.15"
#LandS_nToysPerJob   = 10
#LandS_nToysPerJob   = 50
#number_of_jobs      = 20	# used only for making the expected limits, making the observed limits does not need splitting 
#LandS_nToysPerJob   = 25
#number_of_jobs      = 40
#LandS_nToysPerJob   = 10
#number_of_jobs      = 100
LandS_nToysPerJob   = 50
number_of_jobs      = 200
#LandS_nToysPerJob   = 25
#number_of_jobs      = 400
#LandS_nToysPerJob   = 100
#number_of_jobs      = 400
LandSDataCardNaming = "lands_datacard_hplushadronic_m"
LandSRootFileNaming = "lands_histograms_hplushadronic_m"
scheduler = "arc"
#scheduler = "glite"

#startSeed = 1000
startSeed = 2000

postfix = "toys10k_50toys_200jobs"
#postfix += "_LSFdatacardorder"
postfix += "_HIPdatacardorder"
postfix += "_seed%d" % startSeed

massPoints = ["160"]

datacard_hadr_re = re.compile(LandSDataCardNaming+"(?P<mass>\d+)\.txt$")
datacards_re = [
    datacard_hadr_re,
    re.compile("datacard_m(?P<mass>\d+)_etau_miso_20mar12.txt"),
    re.compile("datacard_m(?P<mass>\d+)_mutau_miso_20mar12.txt"),
    re.compile("datacard_m(?P<mass>\d+)_emu_nobtag_20mar12.txt"),
]

# Patterns of input files, %s denotes the place of the mass
datacard_patterns = [
    LandSDataCardNaming+"%s.txt",
    "datacard_m%s_emu_nobtag_20mar12.txt",
    "datacard_m%s_etau_miso_20mar12.txt",
    "datacard_m%s_mutau_miso_20mar12.txt",
    ]
datacard_patterns = [datacard_patterns[i] for i in [3, 1, 0, 2]] # order in my first crab tests

rootfile_patterns = [
    LandSRootFileNaming+"%s.root"
]

script_re   = re.compile("runLandS_(?P<label>(Observed|Expected)_m)(?P<mass>\d+)")
luminosity_re = re.compile("luminosity=[\S| ]*(?P<lumi>\d+\.\d+)")

class MultiCrabLandS:
    def __init__(self):

        self.exe = which("lands.exe")
        if self.exe == None:
	    self.exe = install_lands()

        self.datacards = {}
        self.rootfiles = {}
        self.scripts   = []

        for mass in massPoints:
            for dc in datacard_patterns:
                fname = dc % mass
                if not os.path.isfile(fname):
                    raise Exception("Datacard file '%s' does not exist!" % fname)

                multicrab._addToDictList(self.datacards, mass, fname)

            for rf in rootfile_patterns:
                fname = rf % mass
                if not os.path.isfile(fname):
                    raise Exception("ROOT file (for shapes) '%s' does not exist!" % fname)

                multicrab._addToDictList(self.rootfiles, mass, fname)

        if len(self.datacards) == 0:
	    print "No LandS datacards found in this directory!"
	    print "Naming convention for datacards:",LandSDataCardNaming
	    print "Naming convention for rootfiles:",LandSRootFileNaming
	    sys.exit()

    def CreateMultiCrabDir(self):
	self.dirname = multicrab.createTaskDir(prefix="LandSMultiCrab", postfix=postfix)

    def CopyLandsInputFiles(self):
        for d in [self.datacards, self.rootfiles]:
            for mass, files in d.iteritems():
                for f in files:
                    shutil.copy(f, self.dirname)
        shutil.copy(self.exe, self.dirname)        

    def writeLandsScripts(self):
        for mass, datacardFiles in self.datacards.iteritems():
	    self.writeObs(mass, datacardFiles)
	    self.writeExp(mass, datacardFiles)

    def writeObs(self, mass, datacardFiles):
        outFileName = "runLandS_Observed_m" + mass
        command = [
            "#!/bin/sh",
            "",
            "SEED=$(expr %d + $1)" % startSeed,
            'echo "LandSSeed=$SEED"',
            "",
            "./lands.exe " + LandS_options + " --seed $SEED -d " + " ".join(datacardFiles) + "| tail -5 >& lands.out",
            ""
            "cat lands.out"
            ]
        self.writeCard(outFileName, "\n".join(command)+"\n")

    def writeExp(self, mass, datacardFiles):
#	seed = self.randomSeed()
        outFileName = "runLandS_Expected_m" + mass
        command = [
            "#!/bin/sh",
            "",
            "SEED=$(expr %d + $1)" % startSeed,
            'echo "LandSSeed=$SEED"',
            "",
            "./lands.exe %s -n split_m%s --doExpectation 1 -t %d --seed $SEED -d %s | tail -5 > lands.out" % (LandS_options, mass, LandS_nToysPerJob, " ".join(datacardFiles)),
            "",
            "cat lands.out",
            ]


        self.writeCard(outFileName, "\n".join(command)+"\n")
        # command = "./lands.exe " + LandS_options + " --doExpectation 1 -t " + str(LandS_nToysPerJob) + " --seed " + str(seed) + " -d " + " ".join(datacardFiles) + "| tail -5 >& lands.out && cat lands.out && echo 'LandSSeed='" + str(seed)
        # self.writeCard(outFileName, command)

    def writeCard(self, filename,command):
        fOUT = open(self.dirname+"/"+filename,'w')
        fOUT.write(command)
        fOUT.close()
        os.system("chmod +x "+self.dirname+"/"+filename)
        self.scripts.append(filename)

    def writeCrabCfg(self):
	filename = self.dirname+"/crab.cfg"
	fOUT = open(filename,'w')
	fOUT.write("[CRAB]\n")
        fOUT.write("jobtype                 = cmssw\n")
        fOUT.write("scheduler               = %s\n" % scheduler)
        fOUT.write("use_server              = 0\n")
        fOUT.write("\n")
        fOUT.write("[CMSSW]\n")
        fOUT.write("datasetpath             = none\n")
        fOUT.write("pset                    = none\n")
        fOUT.write("number_of_jobs          = 1\n")
        fOUT.write("output_file             = lands.out\n")
        fOUT.write("\n")
        fOUT.write("[USER]\n")
        fOUT.write("return_data             = 1\n")
        fOUT.write("copy_data               = 0\n")
        fOUT.write("\n")
	fOUT.close()

    def writeMultiCrabCfg(self):
	filename = self.dirname+"/multicrab.cfg"
        fOUT = open(filename,'w')
        fOUT.write("[COMMON]\n")
        fOUT.write("CRAB.use_server              = 0\n")
	fOUT.write("CMSSW.datasetpath            = none\n")
	fOUT.write("CMSSW.pset                   = none\n")
        fOUT.write("GRID.ce_white_list           = jade-cms.hip.fi\n")
        fOUT.write("\n")
    
        for i, script in enumerate(self.scripts):
	    match = script_re.search(script)
	    if match:
	        label = match.group("label")
		mass  = match.group("mass")
                datacards = ",".join(self.datacards[mass])
                rootfiles = ",".join(self.rootfiles[mass])
                exe = self.exe.split("/")[-1]
		fOUT.write("[" + label + str(mass) + "]\n")
		fOUT.write("USER.return_data             = 1\n")
		fOUT.write("USER.copy_data               = 0\n")
	    	fOUT.write("USER.script_exe              = " + script + "\n")
	    	fOUT.write("USER.additional_input_files  = " + datacards + "," + exe + "," + rootfiles + "\n")
		if label.find("Expected") == 0:
                    #fdc = self.datacards[mass][0]
                    fdc = "split_m%s" % mass
                    output_files = [
                        fdc + "_limitbands.root",
                        fdc + "_limits_tree.root"
                        ]
#                    output_files = [dc+"_Hybrid_limitbands.root" for dc in self.datacards[mass]]
#                    output_files.extend([dc+"_Hybrid_limits_tree.root" for dc in self.datacards[mass]])

		    fOUT.write("CMSSW.number_of_jobs         = " + str(number_of_jobs) + "\n")
		    fOUT.write("CMSSW.output_file            = lands.out," + ",".join(output_files) + "\n")
		else:
		    fOUT.write("CMSSW.number_of_jobs         = 1\n")
		    fOUT.write("CMSSW.output_file            = lands.out\n")
	    	fOUT.write("\n")
		fOUT.write("\n")

        fOUT.close()

    def findDataCard(self, mass):
	for datacard in self.datacards:
	    if not datacard.find(mass) == -1:
		return datacard
	print "Datacard matching mass",mass,"not found"
	sys.exit()

    def findRootFile(self, mass):
	for rootfile in self.rootfiles:
            if not rootfile.find(mass) == -1:
                return rootfile
        print "Rootfile matching mass",mass,"not found"
        sys.exit()

    def randomSeed(self):
	seed = int(10000000*random.random())
	#print "Random seed",seed
	return seed

    def printInstruction(self):
	print "Multicrab cfg created. Type"
        print "cd",self.dirname,"&& multicrab -create"

class Result:
    def __init__(self, mass = 0, observed = 0, expected = 0, expectedPlus1Sigma = 0, expectedPlus2Sigma = 0, expectedMinus1Sigma = 0, expectedMinus2Sigma = 0):
        self.mass                = float(mass)
        self.observed            = float(observed)
        self.expected            = float(expected)
        self.expectedPlus1Sigma  = float(expectedPlus1Sigma)
        self.expectedPlus2Sigma  = float(expectedPlus2Sigma)
        self.expectedMinus1Sigma = float(expectedMinus1Sigma)
        self.expectedMinus2Sigma = float(expectedMinus2Sigma)
        
    def Exists(self, result):
        if self.mass == result.mass:
            return True
        return False
        
    def Add(self, result):
        if self.mass == result.mass:
            if self.observed == 0:
                self.observed = float(result.observed)   
            if self.expected == 0:
                self.expected            = float(result.expected)
                self.expectedPlus1Sigma  = float(result.expectedPlus1Sigma)
                self.expectedPlus2Sigma  = float(result.expectedPlus2Sigma)
                self.expectedMinus1Sigma = float(result.expectedMinus1Sigma)
                self.expectedMinus2Sigma = float(result.expectedMinus2Sigma)
  
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
	self.landsOutFile_re   = re.compile("^lands(?P<label>(\S*|_merged))\.out$")
#	self.landsObsResult_re = re.compile("(= )(?P<value>(\d*\.\d*))( +/- )(?P<error>(\d*\.\d*))")
	self.landsObsResult_re = re.compile("= *(?P<value>(\d*\.\d*))")
	self.landsExpResult_re = re.compile("BANDS    (?P<minus2>(\d*\.\d*))(    )(?P<minus1>(\d*\.\d*))(    )(?P<mean>(\d*\.\d*))(    )(?P<plus1>(\d*\.\d*))(    )(?P<plus2>(\d*\.\d*))(    )(?P<median>(\d*\.\d*))")

	subdirs = []
	dirs = execute("ls %s"%self.path)
	for dir in dirs:
	    dir = path + dir
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
		    print line
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
	command = "ls "+ dir + "/res"
        files = execute(command)
	for file in files:
	    file_match = self.landsOutFile_re.search(file)
	    if file_match:
		fIN = open(dir+"/res/"+file, 'r')
		for line in fIN:
		    result_match = self.landsObsResult_re.search(line)
		    if result_match:
			result.observed = result_match.group("value")
		fIN.close()
		break
	return result

    def RunLandSFromMergedFile(self, dir):
	fOUT = "lands_merged.out"
	if not self.FileExists(dir):

	    exe = which("lands.exe")
	    if exe == None:
                exe = install_lands()

	    command = "ls "+ dir + "/res"
	    files = execute(command)
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
        command = "ls "+ dir + "/res"
        files = execute(command)
        found = False
        for file in files:
            file_match = self.landsOutFile_re.search(file)
            if file_match:
                label = file_match.group("label")
                if label == "_merged":
                    found = True
        return found

    def DirExists(self, dir):
	files = execute("ls")
	for file in files:
	    if os.path.isdir(dir):
		if file == dir:
		    return True
	return False

    def Print(self):
	for result in self.results:
	    result.Print()

    def Save(self, dOUT):
	outputFileNaming = "output_lands_datacard_hplushadronic_m"

	if not self.DirExists(dOUT):
	    os.system("mkdir " + dOUT)

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

    def Data(self):
	return self.results

def install_lands():
    exe = execute("ls ${PWD}/LandS/test/lands.exe 2> /dev/null")
    if len(exe) == 0:
        os.system("cvs co -r " + LandS_tag + " -d LandS UserCode/mschen/LandS")
        os.system("cd LandS && make")
        exe = execute("ls ${PWD}/LandS/test/lands.exe 2> /dev/null")
    return exe

def execute(cmd):
    f = os.popen(cmd)
    ret=[]
    for line in f:
        ret.append(line.replace("\n", ""))
    f.close()
    return ret

# http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
def which(program):
    import os
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None
