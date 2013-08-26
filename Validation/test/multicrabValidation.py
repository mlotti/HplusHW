#!/usr/bin/env python

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab import *

cfg = "validation_cfg.py"
multicrab = Multicrab("crab_analysis.cfg", cfg, lumiMaskDir="../../HeavyChHiggsToTauNu/test")

# Select the pattuple version to use as an input
pattupleVersion = "pattuple_v18"

#era = "EPS"
era = "Run2011A"

# Change this to true if you want to run the PAT on the fly (for
# datasets where no pattuples are produced, or for testing something
# where information not stored in pattuples is needed). 
runPatOnTheFly = False
#runPatOnTheFly = True
if runPatOnTheFly:
    pattupleVersion = "AOD"


# Uncomment below the datasets you want to process
# The dataset definitions are in python/tools/multicrabDatasets.py

datasetsMC = [
        "TTJets_TuneZ2_Summer11",
        "WJets_TuneZ2_Summer11",
        ]

datasets = []
datasets += datasetsMC

# Add the datasest to the multicrab system
multicrab.extendDatasets(pattupleVersion, datasets)

output = ["output.root"]
if "signalAnalysis" in cfg:
    output.append("pickEvents.txt")
multicrab.addCommonLine("CMSSW.output_file = %s" % ",".join(output))

# Set the era to MC datasets
def setPuEra(dataset):
    if dataset.isMC():
        dataset.appendArg("puWeightEra="+era)
multicrab.forEachDataset(setPuEra)

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
if runPatOnTheFly:
    multicrab.appendArgAll("doPat=1")

    #multicrab.modifyLumisPerJobAll(lambda nlumis: nlumis*2)
    #multicrab.modifyNumberOfJobsAll(lambda njobs: njobs*0.5)

prefix = "multicrab"
if "QCD" in cfg:
    prefix += "_QCD"

# Generate configuration only
#multicrab.createTasks(prefix=prefix, configOnly=True)

# Genenerate configuration and create the crab tasks
multicrab.createTasks(prefix=prefix)
