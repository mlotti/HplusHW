#!/usr/bin/env python

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab import *

multicrab = Multicrab("crab.cfg", "triggerEfficiency_cfg.py")

# Select the pattuple version to use as an input
pattupleVersion = "pattuple_v17_1"


# Change this to true if you want to run the PAT on the fly (for
# datasets where no pattuples are produced, or for testing something
# where information not stored in pattuples is needed). 
runPatOnTheFly = False
#runPatOnTheFly = True
if runPatOnTheFly:
    # RECO is needed for pre-39X data, for 39X and beyond, AOD is enough
    pattupleVersion = "AOD"
    #pattupleVersion = "RECO"


# Uncomment below the datasets you want to process
# The dataset definitions are in python/tools/multicrabDatasets.py
multicrab.extendDatasets(pattupleVersion,
    [
        #### 42X data and MC
        # Data: single tau (control trigger)
    "Tau_Single_165970-166164_Prompt",
    "Tau_Single_166346-166346_Prompt",
    "Tau_Single_166374-167043_Prompt",
    "Tau_Single_167078-167784_Prompt",
    "Tau_Single_167786-167913_Prompt_Wed",
        # Data: single tau + MET
        ])

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

# Generate configuration only
#multicrab.createTasks(configOnly=True)

# Genenerate configuration and create the crab tasks
multicrab.createTasks()

# Create a custom multicrab task directory (SignalAnalysis_xxxxxx_yyyyyy)
#multicrab.createTasks(prefix="SignalAnalysis")
