#!/usr/bin/env python

import re

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab import *

#step = "skim"
#step = "generation"
#step = "embedding"
#step = "analysis"
#step = "analysisTau"
step = "signalAnalysis"

config = {"skim":           {"input": "AOD",                        "config": "muonSkim_cfg.py", "output": "skim.root"},
          "generation":     {"input": "tauembedding_skim_v8",       "config": "embed_HLT.py",    "output": "embedded_HLT.root"},
          "embedding":      {"input": "tauembedding_generation_v8", "config": "embed_RECO.py",   "output": "embedded_RECO.root"},
          "analysis":       {"input": "tauembedding_embedding_v6_2",  "config": "embeddingAnalysis_cfg.py"},
          "analysisTau":    {"input": "pattuple_v9",                "config": "tauAnalysis_cfg.py"},
          "signalAnalysis": {"input": "tauembedding_embedding_v6_2",  "config": "../signalAnalysis_cfg.py"},
          }

crabcfg = "crab.cfg"
if step in ["analysis", "analysisTau", "signalAnalysis"]:
    crabcfg = "../crab_analysis.cfg"


multicrab = Multicrab(crabcfg, config[step]["config"], lumiMaskDir="..")

datasets = [
    # Data
    "Mu_136035-144114_Dec22", # HLT_Mu9
    "Mu_146428-147116_Dec22", # HLT_Mu9
    "Mu_147196-149294_Dec22", # HLT_Mu15_v1
    # Signal MC
    "TTJets_TuneZ2_Winter10",
#    "TTJets_TuneD6T_Winter10",
    "WJets_TuneZ2_Winter10",
    #"WJets_TuneZ2_Winter10_noPU",
#    "WJets_TuneD6T_Winter10",
    # Background MC
    "QCD_Pt20_MuEnriched_TuneZ2_Winter10",
    "DYJetsToLL_M50_TuneZ2_Winter10",
    "TToBLNu_s-channel_TuneZ2_Winter10",
    "TToBLNu_t-channel_TuneZ2_Winter10",
    "TToBLNu_tW-channel_TuneZ2_Winter10",
    "WW_TuneZ2_Winter10",
    "WZ_TuneZ2_Winter10",
    "ZZ_TuneZ2_Winter10",
    # For testing
    "TTToHplusBWB_M120_Winter10"
    ]

multicrab.extendDatasets(config[step]["input"], datasets)

multicrab.appendLineAll("GRID.maxtarballsize = 15")
#if step != "skim":
#    multicrab.extendBlackWhiteListAll("ce_white_list", ["jade-cms.hip.fi"])


path_re = re.compile("_tauembedding_.*")
tauname = "_tauembedding_%s_v8_1" % step

reco_re = re.compile("(?P<reco>Reco_v\d+_[^_]+_)")

skimNjobs = {
    "WJets_TuneZ2_Winter10": 400,
    "WJets_TuneZ2_Winter10_noPU": 100,
    "WJets_TuneD6T_Winter10": 400,
    "TTJets_TuneZ2_Winter10": 400,
    "TTJets_TunedD6TWinter10": 400,
    "QCD_Pt20_MuEnriched_TuneZ2_Winter10": 400,
    "DYJetsToLL_M50_TuneZ2_Winter10": 30,
    "TToBLNu_s-channel_TuneZ2_Winter10": 100,
    "TToBLNu_t-channel_TuneZ2_Winter10": 100,
    "TToBLNu_tW-channel_TuneZ2_Winter10": 100,
    "WW_TuneZ2_Winter10": 100,
    "WZ_TuneZ2_Winter10": 100,
    "ZZ_TuneZ2_Winter10": 100,
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

    if dataset.isData() and step in ["generation", "embedding"]:
        dataset.appendArg("overrideBeamSpot=1")

    if step == "skim":
        try:
            dataset.setNumberOfJobs(skimNjobs[dataset.getName()])
        except KeyError:
            pass

        #if config[step]["input"] == "AOD":
        #    dataset.extendBlackWhiteList("se_white_list", ["T2_FI_HIP"])
        dataset.useServer(False)

    dataset.appendLine("USER.publish_data_name = "+name)
    dataset.appendLine("CMSSW.output_file = "+config[step]["output"])

def modifyAnalysis(dataset):
    if step == "signalAnalysis":
        dataset.appendArg("tauEmbeddingInput=1")
        dataset.appendArg("doPat=1")
#    if step == "analysisTau":
#        if dataset.getName() == "WJets":
#            dataset.setNumberOfJobs(100)


if step in ["analysis", "analysisTau","signalAnalysis"]:
    multicrab.appendLineAll("CMSSW.output_file = histograms.root")
    multicrab.forEachDataset(modifyAnalysis)
else:
    multicrab.forEachDataset(modify)

prefix = "multicrab_"+step

multicrab.createTasks(prefix=prefix)
#multicrab.createTasks(configOnly=True,prefix=prefix)
