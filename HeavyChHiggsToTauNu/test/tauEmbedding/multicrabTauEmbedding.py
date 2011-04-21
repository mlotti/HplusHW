#!/usr/bin/env python

import re

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab import *

#step = "skim"
#step = "generation"
#step = "embedding"
#step = "analysis"
#step = "analysisTau"
#step = "signalAnalysis"
step = "muonAnalysis"

dirPrefix = ""
#dirPrefix = "_TauIdScan"

#pt = "_pt30"
pt = "_pt40"

if step in ["generation", "embedding", "analysis", "signalAnalysis"]:
    dirPrefix += pt

config = {"skim":           {"input": "AOD",                           "config": "muonSkim_cfg.py", "output": "skim.root"},
          "generation":     {"input": "tauembedding_skim_v9",          "config": "embed_HLT.py",    "output": "embedded_HLT.root"},
          "embedding":      {"input": "tauembedding_generation_v9"+pt, "config": "embed_RECO.py",   "output": "embedded_RECO.root"},
          "analysis":       {"input": "tauembedding_embedding_v9"+pt,  "config": "embeddingAnalysis_cfg.py"},
          "analysisTau":    {"input": "pattuple_v10",                  "config": "tauAnalysis_cfg.py"},
          "signalAnalysis": {"input": "tauembedding_embedding_v9"+pt,  "config": "../signalAnalysis_cfg.py"},
          "muonAnalysis":   {"input": "tauembedding_skim_v9",          "config": "muonAnalysisFromSkim_cfg.py"},
          }

crabcfg = "crab.cfg"
if step in ["analysis", "analysisTau", "signalAnalysis", "muonAnalysis"]:
    crabcfg = "../crab_analysis.cfg"


multicrab = Multicrab(crabcfg, config[step]["config"], lumiMaskDir="..")

datasets = [
    # Data
#    "Mu_136035-144114_Dec22", # HLT_Mu9
#    "Mu_146428-147116_Dec22", # HLT_Mu9
#    "Mu_147196-149294_Dec22", # HLT_Mu15_v1
    # Signal MC
    "TTJets_TuneZ2_Spring11",
#    "WJets_TuneZ2_Spring11",
    # Background MC
#    "QCD_Pt20_MuEnriched_TuneZ2_Spring11",
#    "DYJetsToLL_M50_TuneZ2_Spring11",
#    "TToBLNu_s-channel_TuneZ2_Spring11",
#    "TToBLNu_t-channel_TuneZ2_Spring11",
#    "TToBLNu_tW-channel_TuneZ2_Spring11",
#    "WW_TuneZ2_Spring11",
#    "WZ_TuneZ2_Spring11",
#    "ZZ_TuneZ2_Spring11",
    # For testing
#    "TTToHplusBWB_M120_Spring11"
    ]

multicrab.extendDatasets(config[step]["input"], datasets)

multicrab.appendLineAll("GRID.maxtarballsize = 15")
#if step != "skim":
#    multicrab.extendBlackWhiteListAll("ce_white_list", ["jade-cms.hip.fi"])


path_re = re.compile("_tauembedding_.*")
tauname = "_tauembedding_%s_v9" % step
if step in ["generation", "embedding"]:
    tauname += pt

reco_re = re.compile("(?P<reco>Reco_v\d+_[^_]+_)")

skimNjobs = {
    "WJets_TuneZ2_Spring11": 400,
    "TTJets_TuneZ2_Spring11": 400,
    "QCD_Pt20_MuEnriched_TuneZ2_Spring11": 400,
    "DYJetsToLL_M50_TuneZ2_Spring11": 150,
    "TToBLNu_s-channel_TuneZ2_Spring11": 100,
    "TToBLNu_t-channel_TuneZ2_Spring11": 100,
    "TToBLNu_tW-channel_TuneZ2_Spring11": 100,
    "WW_TuneZ2_Spring11": 100,
    "WZ_TuneZ2_Spring11": 100,
    "ZZ_TuneZ2_Spring11": 100,
    }

muonAnalysisNjobs = { # goal: 30k events/job
    "Mu_136035-144114_Dec22": 1,
    "Mu_146428-147116_Dec22": 1,
    "Mu_147196-149294_Dec22": 1,
    "WJets_TuneZ2_Spring11": 2,
    "TTJets_TuneZ2_Spring11": 6,
    "QCD_Pt20_MuEnriched_TuneZ2_Spring11": 10, #?
    "DYJetsToLL_M50_TuneZ2_Spring11": 4,
    "TToBLNu_s-channel_TuneZ2_Spring11": 2,
    "TToBLNu_t-channel_TuneZ2_Spring11": 2,
    "TToBLNu_tW-channel_TuneZ2_Spring11": 2,
    "WW_TuneZ2_Spring11": 3,
    "WZ_TuneZ2_Spring11": 3,
    "ZZ_TuneZ2_Spring11": 3,
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

def modifyMuonAnalysis(dataset):
    try:
        dataset.setNumberOfJobs(muonAnalysisNjobs[dataset.getName()])
    except KeyError:
        pass
    

if step in ["analysis", "analysisTau","signalAnalysis"]:
    multicrab.appendLineAll("CMSSW.output_file = histograms.root")
    multicrab.forEachDataset(modifyAnalysis)
elif step in ["muonAnalysis"]:
    multicrab.appendLineAll("CMSSW.output_file = histograms.root")
    multicrab.forEachDataset(modifyMuonAnalysis)
else:
    multicrab.forEachDataset(modify)

multicrab.extendBlackWhiteListAll("se_black_list", ["T2_UK_London_Brunel", "T2_BE_IIHE", "T2_IN_TIFR"])

prefix = "multicrab_"+step+dirPrefix

multicrab.createTasks(prefix=prefix)
#multicrab.createTasks(configOnly=True,prefix=prefix)
