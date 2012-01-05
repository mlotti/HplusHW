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

def main():

    lands = MultiCrabLandS()
    lands.CreateMultiCrabDir()
    lands.CopyLandsInputFiles()
    lands.writeLandsScripts()
    lands.writeCrabCfg()
    lands.writeMultiCrabCfg()
    lands.printInstruction()

class MultiCrabLandS:
    def __init__(self):

        self.exe = execute("which lands.exe")

        if len(self.exe) == 0:
	    self.exe = self.install_lands()

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

    def install_lands(self):
        os.system("cvs co -r " + LandS_tag + " -d LandS UserCode/mschen/LandS")
        os.system("cd LandS && make")
        exe = execute("ls ${PWD}/LandS/test/lands.exe")
        return exe

    def randomSeed(self):
	seed = int(10000000*random.random())
	#print "Random seed",seed
	return seed

    def printInstruction(self):
	print "Multicrab cfg created. Type"
        print "cd",self.dirname,"&& multicrab -create"

def execute(cmd): 
    f = os.popen(cmd)
    ret=[]
    for line in f:
        ret.append(line.replace("\n", ""))
    f.close()
    return ret

    
if __name__ == "__main__":
    main()
