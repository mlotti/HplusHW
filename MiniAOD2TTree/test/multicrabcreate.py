#!/usr/bin/env python

import os
import re
import sys
import datetime

datasets = []
datasets.append('/TBHp_HToTauNu_M-200_13TeV_pythia6/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM')
datasets.append('/TTbar_HBWB_HToTauNu_M-160_13TeV_pythia6/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM')
datasets.append('/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM')
datasets.append('/QCD_Pt-50to80_TuneZ2star_13TeV_pythia6/Spring14miniaod-PU20bx25_POSTLS170_V5-v2/MINIAODSIM')
datasets.append('/QCD_Pt-50to80_Tune4C_13TeV_pythia8/Spring14miniaod-castor_PU20bx25_POSTLS170_V5-v1/MINIAODSIM')



dataset_re = re.compile("^/(?P<name>\S+?)/")

dirName = "multicrab"
dirName+= "_signalAnalysis"
dirName+= "_v740p9"

time = datetime.datetime.now().strftime("%Y%m%dT%H%M")
dirName+= "_" + time

if not os.path.exists(dirName):
    os.mkdir(dirName)

crab_dataset_re = re.compile("config.Data.inputDataset")
crab_requestName_re = re.compile("config.General.requestName")
crab_workArea_re = re.compile("config.General.workArea")

for dataset in datasets:
    match = dataset_re.search(dataset)
    if match:
        rName = match.group("name")
	rName = rName.replace("-","_")
	#print rName

        fIN = open("crabConfig.py","r")
	outfilepath = os.path.join(dirName,"crabConfig_"+rName+".py")
        fOUT = open(outfilepath,"w")
        for line in fIN:
	    if line[0] == "#":
		continue
	    match = crab_dataset_re.search(line)
	    if match:
		line = "config.Data.inputDataset = '"+dataset+"'\n"
	    match = crab_requestName_re.search(line)
	    if match:
		line = "config.General.requestName = '"+rName+"'\n"
            match = crab_workArea_re.search(line)
	    if match:
		line = "config.General.workArea = '"+dirName+"'\n"
            fOUT.write(line)
        fOUT.close()
        fIN.close()

	cmd = "crab submit -c "+outfilepath
	print cmd
	os.system("crab submit "+outfilepath)

