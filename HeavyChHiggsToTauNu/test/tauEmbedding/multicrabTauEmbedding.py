#!/usr/bin/env python

import re

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab import *

step = "skim"
#step = "generation"
#step = "embedding"
#step = "analysis"
#step = "analysisTau"

config = {"skim":       {"input": "RECO",                         "config": "muonSkim_cfg.py", "output": "skim.root"},
          "generation": {"input": "tauembedding_skim_v3",         "config": "embed_HLT.py", "output": "embedded_HLT.root"},
          "embedding":  {"input": "tauembedding_generation_v3",   "config": "embed_RECO.py", "output": "embedded_RECO.root"},
          "analysis":   {"input": "tauembedding_embedding_v3_3",  "config": "embeddingAnalysis_cfg.py"},
          "analysisTau": {"input": "pattuple_v6",               "config": "tauAnalysis_cfg.py"},
          }

crabcfg = "crab.cfg"
if step in ["analysis", "analysisTau"]:
    crabcfg = "../crab_analysis.cfg"


multicrab = Multicrab(crabcfg, config[step]["config"], lumiMaskDir="..")
         
multicrab.extendDatasets(
    config[step]["input"],
    [
        # Data
        "Mu_135821-144114", # HLT_Mu9
        "Mu_146240-147116", # HLT_Mu9
        "Mu_147196-149442", # HLT_Mu15_v1
        # Signal MC
        "TTbar",
        "WJets",
        # Background MC
        "QCD_Pt20_MuEnriched",
        "DYJetsToLL",
        "TToBLNu_s-channel",
        "TToBLNu_t-channel",
        "TToBLNu_tW-channel",
        ])

if step in ["generation", "embedding"]:
    multicrab.appendArgAll("overrideBeamSpot=1")

path_re = re.compile("_tauembedding_.*")
tauname = "_tauembedding_%s_v4" % step

skimNjobs = {
    "Mu_135821-144114": 50,
    "WJets": 50,
    "TTJets": 20,
    "QCD_Pt20_MuEnriched": 200,
    "DYJetsToLL": 30,
    }
    

def modify(dataset):
    name = ""

    path = dataset.getDatasetPath().split("/")
    if step == "skim":
        name = path[2].replace("-", "_")
        name += "_"+path[3]
        name += tauname
    else:
        name = path_re.sub(tauname, path[2])
        name = name.replace("local-", "")

    if step == "skim":
        try:
            dataset.setNumberOfJobs(skimNjobs[dataset.getName()])
        except KeyError:
            pass

        if config[step]["input"] == "AOD":
            dataset.extendBlackWhiteList("se_white_list", ["T2_FI_HIP"])

    dataset.appendLine("USER.publish_data_name = "+name)
    dataset.appendLine("CMSSW.output_file = "+config[step]["output"])

def modifyAnalysis(dataset):
    dataset.extendBlackWhiteList("ce_white_list", ["jade-cms.hip.fi"])
#    if step == "analysisTau":
#        if dataset.getName() == "WJets":
#            dataset.setNumberOfJobs(100)


if step in ["analysis", "analysisTau"]:
    multicrab.forEachDataset(modifyAnalysis)
else:
    multicrab.forEachDataset(modify)

multicrab.createTasks()
#multicrab.createTasks(configOnly=True)
