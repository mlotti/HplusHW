#!/usr/bin/env python

import os
import re
import sys
import datetime

datasets = []
#datasets.append('/TBHp_HToTauNu_M-200_13TeV_pythia6/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM')
#datasets.append('/TTbar_HBWB_HToTauNu_M-160_13TeV_pythia6/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM')
#datasets.append('/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM')
##datasets.append('/QCD_Pt-50to80_TuneZ2star_13TeV_pythia6/Spring14miniaod-PU20bx25_POSTLS170_V5-v2/MINIAODSIM')
#datasets.append('/QCD_Pt-50to80_Tune4C_13TeV_pythia8/Spring14miniaod-castor_PU20bx25_POSTLS170_V5-v1/MINIAODSIM')
#datasets.append('/DYJetsToLL_M-50_13TeV-madgraph-pythia8-tauola_v2/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM')
datasets.append('/ZprimeToTauTau_M-1000_Tune4C_13TeV-pythia8/bluj-ZprimeToTauTau_MiniAOD_GRunV47_v2-6b3acb073896b48a28b982ccc80b3330/USER')

#PSET = "miniAODGEN2TTree_cfg.py"
PSET = "miniAOD2TTree_TauLegSkim_cfg.py"

dataset_re = re.compile("^/(?P<name>\S+?)/")

version = ""
pwd = os.getcwd()
cmssw_re = re.compile("/CMSSW_(?P<version>\S+?)/")
match = cmssw_re.search(pwd)
if match:
    version = match.group("version")
    version = version.replace("_","")
    version = version.replace("pre","p")
    version = version.replace("patch","p")

analysis = "signalAnalysis"
leg_re = re.compile("miniAOD2TTree_(?P<leg>\S+Leg)Skim_cfg.py")
match = leg_re.search(PSET)
if match:
    analysis = match.group("leg")

dirName = "multicrab"
dirName+= "_"+analysis
dirName+= "_v"+version

time = datetime.datetime.now().strftime("%Y%m%dT%H%M")
dirName+= "_" + time

if not os.path.exists(dirName):
    os.mkdir(dirName)

crab_dataset_re = re.compile("config.Data.inputDataset")
crab_requestName_re = re.compile("config.General.requestName")
crab_workArea_re = re.compile("config.General.workArea")
crab_pset_re = re.compile("config.JobType.psetName")
tune_re = re.compile("(?P<name>\S+)_Tune")
tev_re = re.compile("(?P<name>\S+)_13TeV")

for dataset in datasets:
    match = dataset_re.search(dataset)
    if match:
        rName = match.group("name")
	rName = rName.replace("-","")
	tune_match = tune_re.search(rName)
	if tune_match:
	    rName = tune_match.group("name")
        tev_match = tev_re.search(rName)
        if tev_match:
            rName = tev_match.group("name")
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
	    match = crab_pset_re.search(line)
            if match:
                line = "config.JobType.psetName = '"+PSET+"'\n"

            fOUT.write(line)
        fOUT.close()
        fIN.close()

	cmd = "crab submit -c "+outfilepath
	print cmd
	os.system("crab submit "+outfilepath)
	mv = "mv "+os.path.join(dirName,"crab_"+rName)+" "+os.path.join(dirName,rName)
	print mv
	os.system(mv)
