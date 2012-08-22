#!/usr/bin/env python

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab import *

multicrab = Multicrab("../crab_analysis.cfg", "muonTagProbe_cfg.py", lumiMaskDir="..")

# patDatasets = [
#     "SingleMu_160431-163261_May10",  # HLT_Mu20_v1
#     "SingleMu_163270-163869_May10",  # HLT_Mu24_v2
#     "SingleMu_165088-165633_Prompt", # HLT_Mu30_v3
#     "SingleMu_165970-166150_Prompt", # HLT_Mu30_v3
#     "SingleMu_166161-166164_Prompt", # HLT_Mu40_v1
#     "SingleMu_166346-166346_Prompt", # HLT_Mu40_v2
#     "SingleMu_166374-166967_Prompt", # HLT_Mu40_v1
#     "SingleMu_167039-167043_Prompt", # HLT_Mu40_v1
#     "SingleMu_167078-167913_Prompt", # HLT_Mu40_v3
#     "SingleMu_170722-172619_Aug05",  # HLT_Mu40_v5
#     "SingleMu_172620-173198_Prompt", # HLT_Mu40_v5
#     "SingleMu_173236-173692_Prompt", # HLT_Mu40_eta2p1_v1

#     "DYJetsToLL_M50_TuneZ2_Summer11",
# ]

# List of AOD datasets for input, together of the triggers whose efficiency we are to measure
aodDatasets = [
    "SingleMu_160431-163261_2011A_Nov08", # HLT_Mu20_v1
    "SingleMu_163270-163869_2011A_Nov08", # HLT_Mu24_v2
    "SingleMu_165088-165633_2011A_Nov08", # HLT_Mu30_v3
    "SingleMu_165970-166150_2011A_Nov08", # HLT_Mu30_v3
    "SingleMu_166161-166164_2011A_Nov08", # HLT_Mu40_v1
    "SingleMu_166346-166346_2011A_Nov08", # HLT_Mu40_v2
    "SingleMu_166374-166967_2011A_Nov08", # HLT_Mu40_v1
    "SingleMu_167039-167043_2011A_Nov08", # HLT_Mu40_v1
    "SingleMu_167078-167913_2011A_Nov08", # HLT_Mu40_v3
    "SingleMu_170722-172619_2011A_Nov08", # HLT_Mu40_v5
    "SingleMu_172620-173198_2011A_Nov08", # HLT_Mu40_v5
    "SingleMu_173236-173692_2011A_Nov08", # HLT_Mu40_eta2p1_v1
    "SingleMu_175860-176469_2011B_Nov19", # HLT_Mu40_eta2p1_v1
    "SingleMu_176545-177053_2011B_Nov19", # HLT_Mu40_eta2p1_v1
    "SingleMu_177074-177452_2011B_Nov19", # HLT_Mu40_eta2p1_v1
    "SingleMu_177718-178380_2011B_Nov19", # HLT_Mu40_eta2p1_v1
    "SingleMu_178420-178866_2011B_Nov19", # HLT_Mu40_eta2p1_v4
    "SingleMu_178871-179889_2011B_Nov19", # HLT_Mu40_eta2p1_v4
    "SingleMu_179959-180252_2011B_Nov19", # HLT_Mu40_eta2p1_v5
]

# List of triggers we use to trigger the events for the Tag&Probe study
triggers = {
    "SingleMu_160431-163261_2011A_Nov08": "HLT_IsoMu12_v1",
    "SingleMu_163270-163869_2011A_Nov08": "HLT_IsoMu17_v6",
    "SingleMu_165088-165633_2011A_Nov08": "HLT_IsoMu17_v8",
    "SingleMu_165970-166150_2011A_Nov08": "HLT_IsoMu24_v5",
    "SingleMu_166161-166164_2011A_Nov08": "HLT_IsoMu24_v5",
    "SingleMu_166346-166346_2011A_Nov08": "HLT_IsoMu24_v6",
    "SingleMu_166374-166967_2011A_Nov08": "HLT_IsoMu24_v5",
    "SingleMu_167039-167043_2011A_Nov08": "HLT_IsoMu24_v5",
    "SingleMu_167078-167913_2011A_Nov08": "HLT_IsoMu24_v7",
    "SingleMu_170722-172619_2011A_Nov08": "HLT_IsoMu24_v8",
    "SingleMu_172620-173198_2011A_Nov08": "HLT_IsoMu24_v8",
    "SingleMu_173236-173692_2011A_Nov08": "HLT_IsoMu30_eta2p1_v3",
    "SingleMu_175860-176469_2011B_Nov19": "HLT_IsoMu30_eta2p1_v3",
    "SingleMu_176545-177053_2011B_Nov19": "HLT_IsoMu30_eta2p1_v3",
    "SingleMu_177074-177452_2011B_Nov19": "HLT_IsoMu30_eta2p1_v3",
    "SingleMu_177718-178380_2011B_Nov19": "HLT_IsoMu30_eta2p1_v3",
    "SingleMu_178420-178866_2011B_Nov19": "HLT_IsoMu30_eta2p1_v6",
    "SingleMu_178871-179889_2011B_Nov19": "HLT_IsoMu30_eta2p1_v6",
    "SingleMu_179959-180252_2011B_Nov19": "HLT_IsoMu30_eta2p1_v7",

    "DYJetsToLL_M50_TuneZ2_Fall11": "HLT_IsoMu30_eta2p1_v3"
}

# These are if we have pattuples as an input, I guess for AOD the numbers of jobs in multicrabDatasets* are more appropriate
numberOfJobs = {
    # "SingleMu_160431-163261_May10":    5,
    # "SingleMu_163270-163869_May10":    5,
    # "SingleMu_165088-165633_Prompt":   4,
    # "SingleMu_165970-166150_Prompt":   2,
    # "SingleMu_166374-166967_Prompt":  10,
    # "SingleMu_167039-167043_Prompt":   1,
    # "SingleMu_167078-167913_Prompt":   6,
    # "SingleMu_170722-172619_Aug05":    6,
    # "SingleMu_172620-173198_Prompt":   7,
    # "SingleMu_173236-173692_Prompt":   4,
    # "DYJetsToLL_M50_TuneZ2_Summer11": 24,
}

# Hack to change the lumiMask
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrabDatasets as multicrabDatasets
for dataset in aodDatasets:
    if not "SingleMu" in dataset: # is data?
        continue
    multicrabDatasets.datasets[dataset]["data"]["AOD"]["lumiMask"] = "Nov08ReReco"

#multicrab.extendDatasets("pattuple_v19", patDatasets)
multicrab.extendDatasets("AOD", aodDatasets)
multicrab.appendArgAll("doPat=1")
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
#multicrab.extendBlackWhiteListAll("ce_white_list", ["jade-cms.hip.fi"])

prefix="multicrab_tagprobe"
#configOnly=True
configOnly=False

multicrab.createTasks(prefix=prefix, configOnly=configOnly)
