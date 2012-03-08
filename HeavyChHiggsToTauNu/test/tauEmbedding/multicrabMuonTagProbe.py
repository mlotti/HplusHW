#!/usr/bin/env python

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab import *

multicrab = Multicrab("../crab_analysis.cfg", "muonTagProbe_cfg.py", lumiMaskDir="..")

patDatasets = [
    "SingleMu_160431-163261_May10",  # HLT_Mu20_v1
    "SingleMu_163270-163869_May10",  # HLT_Mu24_v2
    "SingleMu_165088-165633_Prompt", # HLT_Mu30_v3
    "SingleMu_165970-166150_Prompt", # HLT_Mu30_v3
    "SingleMu_166161-166164_Prompt", # HLT_Mu40_v1
    "SingleMu_166346-166346_Prompt", # HLT_Mu40_v2
    "SingleMu_166374-166967_Prompt", # HLT_Mu40_v1
    "SingleMu_167039-167043_Prompt", # HLT_Mu40_v1
    "SingleMu_167078-167913_Prompt", # HLT_Mu40_v3
    "SingleMu_170722-172619_Aug05",  # HLT_Mu40_v5
    "SingleMu_172620-173198_Prompt", # HLT_Mu40_v5
    "SingleMu_173236-173692_Prompt", # HLT_Mu40_eta2p1_v1

    "DYJetsToLL_M50_TuneZ2_Summer11",
]

triggers = {
    "SingleMu_160431-163261_May10":  "HLT_IsoMu12_v1", 
    "SingleMu_163270-163869_May10":  "HLT_IsoMu17_v6", 
    "SingleMu_165088-165633_Prompt": "HLT_IsoMu17_v8",
    "SingleMu_165970-166150_Prompt": "HLT_IsoMu24_v5",
    "SingleMu_166161-166164_Prompt": "HLT_IsoMu24_v5",
    "SingleMu_166346-166346_Prompt": "HLT_IsoMu24_v6",
    "SingleMu_166374-166967_Prompt": "HLT_IsoMu24_v5",
    "SingleMu_167039-167043_Prompt": "HLT_IsoMu24_v5",
    "SingleMu_167078-167913_Prompt": "HLT_IsoMu24_v7",
    "SingleMu_170722-172619_Aug05":  "HLT_IsoMu24_v8",
    "SingleMu_172620-173198_Prompt": "HLT_IsoMu24_v8",
    "SingleMu_173236-173692_Prompt": "HLT_IsoMu30_eta2p1_v3",

    "DYJetsToLL_M50_TuneZ2_Summer11": "HLT_IsoMu12_v1",
}
numberOfJobs = {
    "SingleMu_160431-163261_May10":    5,
    "SingleMu_163270-163869_May10":    5,
    "SingleMu_165088-165633_Prompt":   4,
    "SingleMu_165970-166150_Prompt":   2,
    "SingleMu_166374-166967_Prompt":  10,
    "SingleMu_167039-167043_Prompt":   1,
    "SingleMu_167078-167913_Prompt":   6,
    "SingleMu_170722-172619_Aug05":    6,
    "SingleMu_172620-173198_Prompt":   7,
    "SingleMu_173236-173692_Prompt":   4,
    "DYJetsToLL_M50_TuneZ2_Summer11": 24,
}

multicrab.extendDatasets("pattuple_v19", patDatasets)
multicrab.appendLineAll("GRID.maxtarballsize = 15")

def modify(dataset):
    dataset.setTrigger("trigger", triggers[dataset.getName()])
    try:
        njobs = numberOfJobs[dataset.getName()]
        dataset.setNumberOfJobs(njobs)
    except KeyError:
        pass

multicrab.forEachDataset(modify)
multicrab.appendLineAll("CMSSW.output_file = histograms.root")
multicrab.extendBlackWhiteListAll("ce_white_list", ["jade-cms.hip.fi"])

prefix="multicrab_tagprobe"

multicrab.createTasks(prefix=prefix)
#multicrab.createTasks(configOnly=True, prefix=prefix)
