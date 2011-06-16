#!/usr/bin/env python

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab import *

multicrab = Multicrab("crab_analysis.cfg", "signalAnalysis_cfg.py")

# Select the pattuple version to use as an input
pattupleVersion = "pattuple_v13"


# Change this to true if you want to run the PAT on the fly (for
# datasets where no pattuples are produced, or for testing something
# where information not stored in pattuples is needed). 
runPatOnTheFly = False
#runPatOnTheFly = True
if runPatOnTheFly:
    pattupleVersion = "AOD"


# Uncomment below the datasets you want to process
# The dataset definitions are in python/tools/multicrabDatasets.py
multicrab.extendDatasets(pattupleVersion,
    [
        #### 42X data and MC
        # Data: single tau (control trigger)
#        "Tau_Single_165970-166164_Prompt",   # HLT_IsoPFTau35_Trk20_v2
#        "Tau_Single_166346-166346_Prompt",   # HLT_IsoPFTau35_Trk20_v3
#        "Tau_Single_166374-166502_Prompt",   # HLT_IsoPFTau35_Trk20_v2
        
        # Data: single tau + MET
        "Tau_160431-161176_May10",  # HLT_IsoPFTau35_Trk20_MET45_v1  
        "Tau_161217-163261_May10",  # HLT_IsoPFTau35_Trk20_MET45_v2
        "Tau_163270-163869_May10",  # HLT_IsoPFTau35_Trk20_MET45_v4
        "Tau_165088-165633_Prompt", # HLT_IsoPFTau35_Trk20_MET45_v6
        "Tau_165970-166164_Prompt", # HLT_IsoPFTau35_Trk20_MET60_v2
        "Tau_166346-166346_Prompt", # HLT_IsoPFTau35_Trk20_MET60_v3
        "Tau_166374-166502_Prompt", # HLT_IsoPFTau35_Trk20_MET60_v2

        
        # MC Signal (WH)
        "TTToHplusBWB_M80_Summer11",
        "TTToHplusBWB_M90_Summer11",
        "TTToHplusBWB_M100_Summer11",
        "TTToHplusBWB_M120_Summer11",
        "TTToHplusBWB_M140_Summer11",
        "TTToHplusBWB_M150_Summer11",
        "TTToHplusBWB_M155_Summer11",
        "TTToHplusBWB_M160_Summer11",

        # MC Signal (HH)
        "TTToHplusBHminusB_M80_Summer11",
        "TTToHplusBHminusB_M100_Summer11",
        "TTToHplusBHminusB_M120_Summer11",
        "TTToHplusBHminusB_M140_Summer11",
        "TTToHplusBHminusB_M150_Summer11",
        "TTToHplusBHminusB_M155_Summer11",
        "TTToHplusBHminusB_M160_Summer11",

        # MC Background
        "QCD_Pt30to50_TuneZ2_Summer11",
        "QCD_Pt50to80_TuneZ2_Summer11",
        "QCD_Pt80to120_TuneZ2_Summer11",
        "QCD_Pt120to170_TuneZ2_Summer11",
        "QCD_Pt170to300_TuneZ2_Summer11",
        "QCD_Pt300to470_TuneZ2_Summer11",
        "TT_TuneZ2_Summer11",
        "WToTauNu_TuneZ2_Summer11",
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
multicrab.createTasks(configOnly=True)

# Genenerate configuration and create the crab tasks
#multicrab.createTasks()

# Create a custom multicrab task directory (SignalAnalysis_xxxxxx_yyyyyy)
#multicrab.createTasks(prefix="SignalAnalysis")
