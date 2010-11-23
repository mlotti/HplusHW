#!/usr/bin/env python

import re

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.certifiedLumi as lumi
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab import *

step = "skim"
#step = "generation"
#step = "embedding"
#step = "analysis"

config = {"skim":       {"input": "AOD",                        "config": "muonSkim_cfg.py", "output": "skim.root"},
          "generation": {"input": "tauembedding_skim_v2",       "config": "embed_HLT.py", "output": "embedded_HLT.root"},
          "embedding":  {"input": "tauembedding_generation_v2", "config": "embed_RECO.py", "output": "embedded_RECO.root"},
          "analysis":   {"input": "tauembedding_embedding_v2",  "config": "embeddingAnalysis_cfg.py"}}

crabcfg = "crab.cfg"
if step == "analysis":
    crabcfg = "../crab_analysis.cfg"


multicrab = Multicrab(crabcfg, config[step]["config"])
         
multicrab.addDatasets(
    config[step]["input"],
    [
        # Data
#        "Mu_135821-144114", # HLT_Mu9
#        "Mu_146240-147116", # HLT_Mu9
#        "Mu_147196-149442", # HLT_Mu15_v1
        # Signal MC
#        "TTbarJets",
        "WJets",
        ])

if step == "skim":
    mask = lumi.getFile("StreamExpress")
    multicrab.setDataLumiMask("../"+mask)
    print "Lumi file", mask
if step in ["generation", "embedding"]:
    multicrab.addArgAll("overrideBeamSpot=1")

path_re = re.compile("_tauembedding_.*")
tauname = "_tauembedding_%s_v3" % step

def modify(dataset):
    name = ""

    path = dataset.getDatasetPath().split("/")
    if step == "skim":
        name = path[2].replace("-", "_")
        name += "_"+path[3]
        name += tauname
    else:
        name = path_re.sub(tauname, path[2])

    if step == "skim":
        if dataset.getName() == "WJets":
            dataset.setNumberOfJobs(50)
            dataset.addBlackWhiteList("se_white_list", ["T2_FI_HIP"])

#    if "Mu_" in dataset.getName():
#        dataset.addArg("overrideBeamSpot=1")

    dataset.addLine("USER.publish_data_name = "+name)
    dataset.addLine("CMSSW.output_file = "+config[step]["output"])

if step != "analysis":
    multicrab.forEachDataset(modify)

multicrab.createTasks()
#multicrab.createTasks(configOnly=True)
