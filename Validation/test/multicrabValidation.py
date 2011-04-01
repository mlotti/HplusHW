#!/usr/bin/env python

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab import *

multicrab = Multicrab("crab_analysis.cfg", "validation_cfg.py", lumiMaskDir="../../HeavyChHiggsToTauNu/test")

# Select the pattuple version to use as an input
#pattupleVersion = "pattuple_v6"
pattupleVersion = "pattuple_v9"


# Change this to true if you want to run the PAT on the fly (for
# datasets where no pattuples are produced, or for testing something
# where information not stored in pattuples is needed). 
#runPatOnTheFly = False
#runPatOnTheFly = True
#if runPatOnTheFly:
    # RECO is needed for pre-39X data, for 39X and beyond, AOD is enough
#    pattupleVersion = "AOD"
    #pattupleVersion = "RECO"

# Uncomment below the datasets you want to process
# The dataset definitions are in python/tools/multicrabDatasets.py
# The values of the keys is the number of jobs
datasets = {
    # 41X data and 311X MC
    "Tau_160404-161176_Prompt": 5, # HLT_IsoPFTau35_Trk20_MET45_v1
    "Tau_161216-161312_Prompt": 5, # HLT_IsoPFTau35_Trk20_MET45_v2
    "TauPlusX_160404-161312_Prompt": 10, # HLT_QuadJet40_IsoPFTau40_v1

#    "TTJets_TuneZ2_Spring11": 10,
    "QCD_Pt80to120_TuneZ2_Spring11": 10,
}

multicrab.extendDatasets("AOD", datasets.keys())

def modify(dataset):
    try:
        dataset.setNumberOfJobs(datasets[dataset.getName()])
    except KeyError:
        pass
multicrab.forEachDataset(modify)

# Force all jobs go to jade, in some situations this might speed up
# the analysis (e.g. when there are O(1000) Alice jobs queueing, all
# CMS jobs typically go to korundi).
#if not runPatOnTheFly:
#    multicrab.extendBlackWhiteListAll("ce_white_list", ["jade-cms.hip.fi"])


# If PAT is ran on the fly, add the
# "doPat=1" command line argument for all datasets. In addition it
# could be wise to decrease the number of jobs as the defaults are
# adjusted for the pattuple file size, and when only histograms or
# small ntuples are produced, stageout is not the issue
#if runPatOnTheFly:
#    multicrab.appendArgAll("doPat=1")

    #multicrab.modifyLumisPerJobAll(lambda nlumis: nlumis*2)
    #multicrab.modifyNumberOfJobsAll(lambda njobs: njobs*0.5)

# Generate configuration only
#multicrab.createTasks(configOnly=True)

# Genenerate configuration and create the crab tasks
multicrab.createTasks()
