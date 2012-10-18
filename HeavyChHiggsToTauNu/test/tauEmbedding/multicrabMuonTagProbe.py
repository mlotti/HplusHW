#!/usr/bin/env python

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab import *

multicrab = Multicrab("../crab_analysis.cfg", "muonTagProbe_cfg.py", lumiMaskDir="..")

# List of AOD datasets for input, together of the triggers whose efficiency we are to measure
datasets = [
    "SingleMu_160431-163261_2011A_Nov08", # HLT_Mu20_v1
    "SingleMu_163270-163869_2011A_Nov08", # HLT_Mu24_v2
    "SingleMu_165088-165633_2011A_Nov08", # HLT_Mu30_v3
    "SingleMu_165970-166150_2011A_Nov08", # HLT_Mu30_v3
    "SingleMu_166161-166164_2011A_Nov08", # HLT_Mu40_v1
    "SingleMu_166346-166346_2011A_Nov08", # HLT_Mu40_v2
    "SingleMu_166374-167043_2011A_Nov08", # HLT_Mu40_v1
    "SingleMu_167078-167913_2011A_Nov08", # HLT_Mu40_v3
    "SingleMu_170722-172619_2011A_Nov08", # HLT_Mu40_v5
    "SingleMu_172620-173198_2011A_Nov08", # HLT_Mu40_v5
    "SingleMu_173236-173692_2011A_Nov08", # HLT_Mu40_eta2p1_v1
    "SingleMu_173693-177452_2011B_Nov19", # HLT_Mu40_eta2p1_v1
    "SingleMu_177453-178380_2011B_Nov19", # HLT_Mu40_eta2p1_v1
    "SingleMu_178411-179889_2011B_Nov19", # HLT_Mu40_eta2p1_v4
    "SingleMu_179942-180371_2011B_Nov19", # HLT_Mu40_eta2p1_v5

    "DYJetsToLL_M50_TuneZ2_Fall11", 
]

multicrab.extendDatasets("muonTagProbe", datasets)
multicrab.appendLineAll("GRID.maxtarballsize = 15")
#multicrab.extendBlackWhiteListAll("ce_white_list", ["jade-cms.hip.fi"])

prefix="multicrab_tagprobe"
#configOnly=True
configOnly=False

multicrab.createTasks(prefix=prefix, configOnly=configOnly)
