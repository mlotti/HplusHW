#!/usr/bin/env python

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab import *

multicrab = Multicrab("../crab_analysis.cfg", "muonTagProbe_cfg.py", lumiMaskDir="..")

aodDatasets = [
    # Data
    "Mu_136035-144114_Dec22",
    "Mu_146428-147116_Dec22",
#    "Mu_147196-149294_Dec22"
    # Signal MC
    # Background MC
#    "QCD_Pt20_MuEnriched_TuneZ2_Winter10",
#    "DYJetsToLL_TuneZ2_Winter10",
#    "TToBLNu_s-channel_TuneZ2_Winter10",
#    "TToBLNu_t-channel_TuneZ2_Winter10",
#    "TToBLNu_tW-channel_TuneZ2_Winter10",
    # Signal MC
#    "WJets_TuneZ2_Winter10",
#    "WJets_TuneD6T_Winter10",
#    "TTJets_TuneZ2_Winter10",
#    "TTJets_TuneD6T_Winter10",
]


multicrab.extendDatasets("AOD", aodDatasets)
multicrab.appendLineAll("GRID.maxtarballsize = 15")
multicrab.appendLineAll("CMSSW.output_file = histograms.root")

numberOfJobs = {
    "Mu_146428-147116_Dec22": 5,
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
