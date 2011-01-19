#!/usr/bin/env python

import re

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab import *

step = "skim"
#step = "generation"
#step = "embedding"
#step = "analysis"
#step = "analysisTau"

config = {"skim":       {"input": "RECO",                         "config": "muonSkim_cfg.py", "output": "skim.root"},
          "generation": {"input": "tauembedding_skim_v5",         "config": "embed_HLT.py", "output": "embedded_HLT.root"},
          "embedding":  {"input": "tauembedding_generation_v5",   "config": "embed_RECO.py", "output": "embedded_RECO.root"},
          "analysis":   {"input": "tauembedding_embedding_v5",  "config": "embeddingAnalysis_cfg.py"},
          "analysisTau": {"input": "pattuple_v6",               "config": "tauAnalysis_cfg.py"},
          }

crabcfg = "crab.cfg"
if step in ["analysis", "analysisTau"]:
    crabcfg = "../crab_analysis.cfg"


multicrab = Multicrab(crabcfg, config[step]["config"], lumiMaskDir="..")

datasets = [
    # Data
    "Mu_135821-144114", # HLT_Mu9
    "Mu_146240-147116", # HLT_Mu9
    "Mu_147196-149442", # HLT_Mu15_v1
    # Signal MC
    "TTJets_PU",
    "WJets_Fall10_PU",
    # Background MC
    "QCD_Pt20_MuEnriched_PU",
    "DYJetsToLL_PU",
    "TToBLNu_s-channel_PU",
    "TToBLNu_t-channel_PU",
    "TToBLNu_tW-channel_PU",
    ]

multicrab.extendDatasets(config[step]["input"], datasets)

if step in ["generation", "embedding"]:
    multicrab.appendArgAll("overrideBeamSpot=1")

path_re = re.compile("_tauembedding_.*")
tauname = "_tauembedding_%s_v5" % step

reco_re = re.compile("(?P<reco>Reco_v\d+_[^_]+_)")

skimNlumis = {
    "Mu_135821-144114": 1000
    }

skimNjobs = {
    "WJets_Fall10_PU": 50,
    "TTJets_PY": 20,
    "QCD_Pt20_MuEnriched_PU": 300,
    "DYJetsToLL_PU": 30,
    "TToBLNu_s-channel_PU": 100,
    "TToBLNu_t-channel_PU": 100,
    "TToBLNu_tW-channel_PU": 100,
    }
    

def modify(dataset):
    name = ""

    path = dataset.getDatasetPath().split("/")
    if step == "skim":
        name = path[2].replace("-", "_")
        name += "_"+path[3]
        name += tauname

        if dataset.isData():
            frun = dataset.getName().split("_")[1].split("-")[0]
            m = reco_re.search(name)
            name = reco_re.sub(m.group("reco")+frun+"_", name)

    else:
        name = path_re.sub(tauname, path[2])
        name = name.replace("local-", "")
        dataset.extendBlackWhiteList("ce_white_list", ["jade-cms.hip.fi"])

    if step == "skim":
        try:
            dataset.setNumberOfJobs(skimNjobs[dataset.getName()])
        except KeyError:
            pass
        try:
            dataset.setLumisPerJob(skimNlumis[dataset.getName()])
        except KeyError:
            pass

        #if config[step]["input"] == "AOD":
        #    dataset.extendBlackWhiteList("se_white_list", ["T2_FI_HIP"])
        dataset.useServer(False)

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
