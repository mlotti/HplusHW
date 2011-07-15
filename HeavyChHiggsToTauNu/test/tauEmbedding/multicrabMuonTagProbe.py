#!/usr/bin/env python

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab import *

multicrab = Multicrab("../crab_analysis.cfg", "muonTagProbe_cfg.py", lumiMaskDir="..")

aodDatasets = [
#    "SingleMu_160431-161016_Prompt", # HLT_Mu20_v1
#    "SingleMu_162803-163261_Prompt", # HLT_Mu20_v1 (new)
#    "SingleMu_163270-163869_Prompt", # HLT_Mu24_v2
#    "DYJetsToLL_M50_TuneZ2_Spring11",

#    "SingleMu_160431-163261_May10", # HLT_Mu20_v1
    "SingleMu_161119-161119_May10_Wed", # HLT_Mu20_v1
#    "SingleMu_163270-163869_May10", # HLT_Mu24_v2
#    "SingleMu_165088-166150_Prompt", # HLT_Mu30_v3
    "SingleMu_165103-165103_Prompt_Wed", # HLT_Mu30_v3
#    "SingleMu_166161-166164_Prompt", # HLT_Mu40_v1
#    "SingleMu_166346-166346_Prompt", # HLT_Mu40_v2
#    "SingleMu_166374-167043_Prompt", # HLT_Mu40_v1
#    "SingleMu_167078-167784_Prompt", # HLT_Mu40_v3
    "SingleMu_167786-167913_Prompt_Wed", # HLT_Mu40_v1

#    "DYJetsToLL_M50_TuneZ2_Summer11",
]


multicrab.extendDatasets("AOD", aodDatasets)
multicrab.appendLineAll("GRID.maxtarballsize = 15")
multicrab.appendLineAll("CMSSW.output_file = histograms.root")

numberOfJobs = {
#    "Mu_146428-147116_Dec22": 5,
#    "SingleMu_160431-161016_Prompt": 4,
#    "SingleMu_162803-163261_Prompt": 8,
#    "SingleMu_163270-163869_Prompt": 10,
#    "DYJetsToLL_M50_TuneZ2_Spring11": 20,

    "SingleMu_160431-163261_May10": 12,
    "SingleMu_163270-163869_May10": 10,
    "SingleMu_165088-166150_Prompt": 10,
    "SingleMu_166161-166164_Prompt": 1,
    "SingleMu_166346-166346_Prompt": 1,
    "SingleMu_166374-167043_Prompt": 20,
    "SingleMu_167078-167784_Prompt": 6,

    "DYJetsToLL_M50_TuneZ2_Summer11": 200,
}

def modify(dataset):
    try:
        njobs = numberOfJobs[dataset.getName()]
        dataset.setNumberOfJobs(njobs)
    except KeyError:
        pass

multicrab.forEachDataset(modify)

prefix="multicrab_tagprobe"

multicrab.createTasks(prefix=prefix)
#multicrab.createTasks(configOnly=True, prefix=prefix)
