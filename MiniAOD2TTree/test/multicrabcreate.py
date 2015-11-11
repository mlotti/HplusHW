#!/usr/bin/env python

# Usage: multicrabcreate.py [multicrab-dir-to-be-resubmitted]
# is resubmitting some crab tasks within the multicrab dir, 
# first remove the crab-dir, then run multicrabcreate.py again 
# with the multicrab as an argument.

import os
import re
import sys
import datetime

#PSET = "miniAODGEN2TTree_cfg.py"
#PSET = "miniAOD2TTree_TauLegSkim_cfg.py"
#PSET = "miniAOD2TTree_METLegSkim_cfg.py"
PSET = "miniAOD2TTree_SignalAnalysisSkim_cfg.py"

from datasets import *

datasets = []

tauLegDatasets         = []
tauLegDatasets.extend(datasetsMuonData)
tauLegDatasets.extend(datasetsMiniAODv2_DY)
tauLegDatasets.extend(datasetsMiniAODv2_Top)
tauLegDatasets.extend(datasetsMiniAODv2_WJets)
tauLegDatasets.extend(datasetsMiniAODv2_QCDMuEnriched)
                                                                                                                                                         
metLegDatasets         = []
#metLegDatasets.append(Dataset('/TT_Tune4C_13TeV-pythia8-tauola/bluj-TTbar_MiniAOD_GRunV47_v2-6b3acb073896b48a28b982ccc80b3330/USER','phys03'))
metLegDatasets.extend(datasetsTauData)
#metLegDatasets.extend(datasets25ns)
metLegDatasets.extend(datasetsMiniAODv2_DY)                                                                                                                                                         
metLegDatasets.extend(datasetsMiniAODv2_Top)                                                                                                                                                        
metLegDatasets.extend(datasetsMiniAODv2_WJets)                                                                                                                                                      
metLegDatasets.extend(datasetsMiniAODv2_QCD)

signalAnalysisDatasets = []
signalAnalysisDatasets.extend(datasetsTauData)
signalAnalysisDatasets.extend(datasetsMiniAODv2_DY)
signalAnalysisDatasets.extend(datasetsMiniAODv2_Top)
signalAnalysisDatasets.extend(datasetsMiniAODv2_WJets)
signalAnalysisDatasets.extend(datasetsMiniAODv2_QCD)
signalAnalysisDatasets.extend(datasetsMiniAODv2_Signal)
#signalAnalysisDatasets.extend(datasets25ns)
#signalAnalysisDatasets.extend(datasets25nsSignal)

datadataset_re = re.compile("^/(?P<name>\S+?)/(?P<run>Run\S+?)/")
mcdataset_re = re.compile("^/(?P<name>\S+?)/")

version = ""
pwd = os.getcwd()
cmssw_re = re.compile("/CMSSW_(?P<version>\S+?)/")
match = cmssw_re.search(pwd)
if match:
    version = match.group("version")
    version = version.replace("_","")
    version = version.replace("pre","p")
    version = version.replace("patch","p")

analysis = "SignalAnalysis"
leg_re = re.compile("miniAOD2TTree_(?P<leg>\S+)Skim_cfg.py")
match = leg_re.search(PSET)
if match:
    analysis = match.group("leg")

if analysis == "SignalAnalysis":
    datasets = signalAnalysisDatasets
if analysis == "TauLeg":
    datasets = tauLegDatasets
if analysis == "METLeg":
    datasets = metLegDatasets

dirName = "multicrab"
dirName+= "_"+analysis
dirName+= "_v"+version

bx_re = re.compile("\S+(?P<bx>\d\dns)_\S+")
match = bx_re.search(datasets[0].URL)
if match:
    dirName+= "_"+match.group("bx")

time = datetime.datetime.now().strftime("%Y%m%dT%H%M")
dirName+= "_" + time

if len(sys.argv) == 2 and os.path.exists(sys.argv[1]) and os.path.isdir(sys.argv[1]):
    dirName = sys.argv[1]

if not os.path.exists(dirName):
    os.mkdir(dirName)
    os.system("cp %s %s"%(PSET,dirName))

crab_dataset_re = re.compile("config.Data.inputDataset")
crab_requestName_re = re.compile("config.General.requestName")
crab_workArea_re = re.compile("config.General.workArea")
crab_pset_re = re.compile("config.JobType.psetName")
crab_psetParams_re = re.compile("config.JobType.pyCfgParams")
crab_split_re = re.compile("config.Data.splitting")# = 'FileBased'
crab_splitunits_re = re.compile("config.Data.unitsPerJob")

crab_dbs_re = re.compile("config.Data.inputDBS")
tune_re = re.compile("(?P<name>\S+)_Tune")
tev_re = re.compile("(?P<name>\S+)_13TeV")
rr_re = re.compile("Cert_(?P<RunRange>\d+-\d+)_13TeV_PromptReco_Collisions15(?P<BunchSpacing>\S*)_JSON(?P<Silver>(_\S+|))\.")
#rr_re = re.compile("Cert_(?P<RunRange>\d+-\d+)_13TeV_PromptReco_Collisions15(?P<BunchSpacing>\S*)_JSON")
#rr_re = re.compile("Cert_(?P<RunRange>\d+-\d+)_13TeV_PromptReco_Collisions15_(?P<BunchSpacing>\d+ns)_JSON_v")

for dataset in datasets:
    match = mcdataset_re.search(dataset.URL)
    if dataset.isData():
	match = datadataset_re.search(dataset.URL)
    if match:
        rName = match.group("name")
	if dataset.isData():
	    rName+= "_"
	    rName+= match.group("run")
#	rName = rName.replace("-","")
	tune_match = tune_re.search(rName)
	if tune_match:
	    rName = tune_match.group("name")
        tev_match = tev_re.search(rName)
        if tev_match:
            rName = tev_match.group("name")

	if dataset.isData():
	    runrangeMatch = rr_re.search(dataset.lumiMask)
	    if runrangeMatch:
		rr = runrangeMatch.group("RunRange")
		rr = rr.replace("-","_")
		bs = runrangeMatch.group("BunchSpacing")
		rName += "_"+rr+bs
                Ag = runrangeMatch.group("Silver")
                if Ag == "_Silver":
                    rName += Ag
#            s = (dataset.URL).split("/")
#            rName = s[1]+"_"+s[2]

        rName = rName.replace("-","_")

        outfilepath = os.path.join(dirName,"crabConfig_"+rName+".py")

	if not os.path.exists(os.path.join(dirName,rName)):

            fIN = open("crabConfig.py","r")
            fOUT = open(outfilepath,"w")
            for line in fIN:
                if line[0] == "#":
                    continue
                match = crab_dataset_re.search(line)
                if match:
                    line = "config.Data.inputDataset = '"+dataset.URL+"'\n"
        	match = crab_requestName_re.search(line)
                if match:
                    line = "config.General.requestName = '"+rName+"'\n"
                match = crab_workArea_re.search(line)
                if match:
                    line = "config.General.workArea = '"+dirName+"'\n"
                match = crab_pset_re.search(line)
                if match:
                    line = "config.JobType.psetName = '"+PSET+"'\n"
                match = crab_psetParams_re.search(line)
                if match:
                    line = "config.JobType.pyCfgParams = ['dataVersion="+dataset.dataVersion+"']\n"
                match = crab_dbs_re.search(line)
                if match:
                    line = "config.Data.inputDBS = '"+dataset.DBS+"'\n"
                if dataset.isData():
                    match = crab_split_re.search(line)
                    if match:
                        line = "config.Data.splitting = 'LumiBased'\n"
                        line+= "config.Data.lumiMask = '"+dataset.lumiMask+"'\n"
                    match = crab_splitunits_re.search(line)	
                    if match:
                        line = "config.Data.unitsPerJob = 100\n"

                fOUT.write(line)
            fOUT.close()
            fIN.close()

            cmd = "crab submit -c "+outfilepath
            print cmd
            os.system("crab submit "+outfilepath)
            mv = "mv "+os.path.join(dirName,"crab_"+rName)+" "+os.path.join(dirName,rName)
#            print mv
            os.system(mv)
