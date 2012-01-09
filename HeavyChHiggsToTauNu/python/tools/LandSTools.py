#!/usr/bin/env python

import os
import re
import sys
import random
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab

#LandS_tag           = "t3-04-13"
LandS_tag	    = "HEAD"
LandS_options       = "--PhysicsModel ChargedHiggs  -M Hybrid --bQuickEstimateInitialLimit 0 --initialRmin 0. --initialRmax 0.09"
LandS_nToysPerJob   = 50
number_of_jobs      = 10	# used only for making the expected limits, making the observed limits does not need splitting 
LandSDataCardNaming = "lands_datacard_hplushadronic_m"
LandSRootFileNaming = "lands_histograms_hplushadronic_m"


datacard_re = re.compile(LandSDataCardNaming+"(?P<mass>(\d+))\.txt$")
root_re     = re.compile(LandSRootFileNaming+"(?P<mass>(\d+))\.root$")
script_re   = re.compile("runLandS_(?P<label>(Observed|Expected)_m)(?P<mass>(\d+))")

class MultiCrabLandS:
    def __init__(self):

        self.exe = execute("which lands.exe 2> /dev/null")

        if len(self.exe) == 0:
	    self.exe = install_lands()

        localFiles = execute("ls")
        self.datacards = []
        self.rootfiles = []
        self.scripts   = []
        for file in localFiles:
	    match_root = root_re.search(file)
	    if match_root:
	        self.rootfiles.append(file)
	    match_datacard = datacard_re.search(file)
	    if match_datacard:
	        self.datacards.append(file)

        if len(self.datacards) == 0:
	    print "No LandS datacards found in this directory!"
	    print "Naming convention for datacards:",LandSDataCardNaming
	    print "Naming convention for rootfiles:",LandSRootFileNaming
	    sys.exit()

    def CreateMultiCrabDir(self):
	self.dirname = multicrab.createTaskDir(prefix="LandSMultiCrab")

    def CopyLandsInputFiles(self):
	for file in self.datacards:
	    os.system("cp " + file + " " + self.dirname)
        for file in self.rootfiles:
            os.system("cp " + file + " " + self.dirname)

    def writeLandsScripts(self):
        for datacard in self.datacards:
	    self.writeObs(datacard)
	    self.writeExp(datacard)

    def writeObs(self, datacard):
        match = datacard_re.search(datacard)
        mass = match.group("mass")
        outFileName = "runLandS_Observed_m" + mass
        command = "./lands.exe " + LandS_options + " -d " + datacard + "| tail -5 >& lands.out && cat lands.out" 
        self.writeCard(outFileName,command)

    def writeExp(self, datacard):
        match = datacard_re.search(datacard)
        mass = match.group("mass")
	seed = self.randomSeed()
        outFileName = "runLandS_Expected_m" + mass
        command = "./lands.exe " + LandS_options + " -d " + datacard + " --doExpectation 1 -t " + str(LandS_nToysPerJob) + " --seed " + str(seed) + "| tail -5 >& lands.out && cat lands.out && echo 'LandSSeed='" + str(seed)
        self.writeCard(outFileName,command)

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
        fOUT.write("scheduler               = glite\n")
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
        fOUT.write("\n")
    
        for i, script in enumerate(self.scripts):
	    match = script_re.search(script)
	    if match:
	        label = match.group("label")
		mass  = match.group("mass")
                datacard = self.findDataCard(mass)
		rootfile = self.findRootFile(mass)
		fOUT.write("[" + label + str(mass) + "]\n")
		fOUT.write("USER.return_data             = 1\n")
		fOUT.write("USER.copy_data               = 0\n")
	    	fOUT.write("USER.script_exe              = " + script + "\n")
	    	fOUT.write("USER.additional_input_files  = " + datacard + ", " + self.exe[0] + ", " + rootfile + "\n")
		if label.find("Expected") == 0:
		    fOUT.write("CMSSW.number_of_jobs         = " + str(number_of_jobs) + "\n")
		    fOUT.write("CMSSW.output_file            = lands.out, " + datacard + "_HybridHybrid_limitbands.root, " + datacard + "_HybridHybrid_limits_tree.root, " + datacard + "_Hybrid_freqObsLimit.root\n")
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




class ParseLandsOutput:
    class Result:
	def __init__(self, mass = 0, observed = 0, expected = 0, expectedPlus1Sigma = 0, expectedPlus2Sigma = 0, expectedMinus1Sigma = 0, expectedMinus2Sigma = 0):
	    self.mass		     = mass
	    self.observed            = observed
	    self.expected            = expected
	    self.expectedPlus1Sigma  = expectedPlus1Sigma
	    self.expectedPlus2Sigma  = expectedPlus2Sigma
	    self.expectedMinus1Sigma = expectedMinus1Sigma
	    self.expectedMinus2Sigma = expectedMinus2Sigma

	def Exists(self, result):
	    if self.mass == result.mass:
		return True
	    return False

	def Add(self, result):
	    if self.mass == result.mass:
		if self.observed == 0:
		    self.observed = result.observed
		if self.expected == 0:
		    self.expected            = result.expected
		    self.expectedPlus1Sigma  = result.expectedPlus1Sigma
		    self.expectedPlus2Sigma  = result.expectedPlus2Sigma
		    self.expectedMinus1Sigma = result.expectedMinus1Sigma
		    self.expectedMinus2Sigma = result.expectedMinus2Sigma

	def Print(self):
	    print "Mass = ",self.mass
	    print "    Observed = ",self.observed
	    print "    Expected = ",self.expected
	    print "     +1sigma = ",self.expectedPlus1Sigma," -1sigma = ",self.expectedMinus1Sigma
	    print "     +2sigma = ",self.expectedPlus2Sigma," -2sigma = ",self.expectedMinus2Sigma

    def __init__(self, path):
	self.path = path

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
	    if os.path.isdir(dir):
		match = self.subdir_re.search(dir)
		if match:
		    subdirs.append(dir)
	if len(subdirs) == 0:
	    print "No data found, is the directory '" + path + "' a multicrab dir? Exiting.."
	    sys.exit()

	self.Read(subdirs)

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
	return results1.mass > results2.mass
	
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
	    result = self.Result(mass) # filling the mass
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

#	    exe = execute("which lands.exe")
#	    if len(exe) == 0:
            exe = install_lands()

	    command = "ls "+ dir + "/res"
	    files = execute(command)
	    for file in files:
	        match = self.landsRootFile_re.search(file)
	        if match:
		    fIN = dir + "/res/" + match.group(0)
	            command = exe[0] +" --doExpectation 1 --readLimitsFromFile " + fIN + " >& " + dir + "/res/" + fOUT
	            os.system(command)
		    return

    def ParseExpFile(self, result, dir):
        command = "ls "+ dir + "/res"
        files = execute(command)
        for file in files:
            file_match = self.landsOutFile_re.search(file)
            if file_match:
                fIN = open(dir+"/res/"+file, 'r')
                for line in fIN:
                    result_match = self.landsExpResult_re.search(line)
                    if result_match:
#                        result.expected = result_match.group("mean")
			result.expected = result_match.group("median")
			result.expectedPlus1Sigma  = result_match.group("plus1")
			result.expectedPlus2Sigma  = result_match.group("plus2")
			result.expectedMinus1Sigma = result_match.group("minus1")
			result.expectedMinus2Sigma = result_match.group("minus2")
                fIN.close()
                break
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

                                                                        
