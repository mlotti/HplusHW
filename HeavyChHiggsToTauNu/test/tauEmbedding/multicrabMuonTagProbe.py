#!/usr/bin/env python

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab import *

multicrab = Multicrab("../crab_analysis.cfg", "muonTagProbe_cfg.py", lumiMaskDir="..")

aodDatasets = [
    "SingleMu_160431-161016_Prompt", # HLT_Mu20_v1
    "SingleMu_162803-163261_Prompt", # HLT_Mu20_v1 (new)
    "SingleMu_163270-163869_Prompt", # HLT_Mu24_v2

    "DYJetsToLL_M50_TuneZ2_Spring11",
]


multicrab.extendDatasets("AOD", aodDatasets)
multicrab.appendLineAll("GRID.maxtarballsize = 15")
multicrab.appendLineAll("CMSSW.output_file = histograms.root")

numberOfJobs = {
#    "Mu_146428-147116_Dec22": 5,
    "SingleMu_160431-161016_Prompt": 4,
    "SingleMu_162803-163261_Prompt": 8,
    "SingleMu_163270-163869_Prompt": 10,
    
    "DYJetsToLL_M50_TuneZ2_Spring11": 20,
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
