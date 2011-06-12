#!/usr/bin/env python

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab import *

multicrab = Multicrab("crab_analysis.cfg", "signalAnalysis_cfg.py")

# Select the pattuple version to use as an input
pattupleVersion = "pattuple_v13_test1"


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
        
        # Data: single tau + MET
        "Tau_160431-161176_May10", # HLT_IsoPFTau35_Trk20_MET45_v1  
        # MC Background
        "QCD_Pt30to50_TuneZ2_Summer11",
        "TT_TuneZ2_Summer11",


        #### 39X/41X data and 311X MC
        # Data: single tau + MET
        # 2010
#        "BTau_141956-144114_Dec22", # HLT_SingleIsoTau20_Trk5;           v11 
#        "BTau_146428-148058_Dec22", # HLT_SingleIsoTau20_Trk15_MET20;    v10, v11
#        "BTau_148822-149182_Dec22", # HLT_SingleIsoTau20_Trk15_MET25_v3; v10, v11
#        "BTau_149291-149294_Dec22", # HLT_SingleIsoTau20_Trk15_MET25_v4; v10, v11
        # 2011
#        "Tau_160431-161016_Prompt", # HLT_IsoPFTau35_Trk20_MET45_v1; v10, v11
#        "Tau_162803-163261_Prompt", # HLT_IsoPFTau35_Trk20_MET45_v2; v10, v11
#        "Tau_163270-163757_Prompt", # HLT_IsoPFTau35_Trk20_MET45_v4; v11
#        "Tau_163758-163869_Prompt", # HLT_IsoPFTau35_Trk20_MET45_v4; v11

        # Data: quadjet
#        "TauPlusX_160431-161016_Prompt", # HLT_QuadJet40_IsoPFTau40_v1; v10
#        "TauPlusX_162803-163261_Prompt", # HLT_QuadJet40_IsoPFTau40_v1; v10
#        "TauPlusX_163270-163369_Prompt", # HLT_QuadJet40_IsoPFTau40_v3; v10

        # MC Signal WH Spring11
#        "TTToHplusBWB_M80_Spring11", # v11
#        "TTToHplusBWB_M90_Spring11", # v11
#        "TTToHplusBWB_M100_Spring11", # v10, v11
#        "TTToHplusBWB_M120_Spring11", # v10, v11
#        "TTToHplusBWB_M140_Spring11", # v10, v11
#        "TTToHplusBWB_M150_Spring11", # v10, v11
#        "TTToHplusBWB_M155_Spring11", # v10, v11
#        "TTToHplusBWB_M160_Spring11", # v10, v11

        # MC Signal HH Spring11
#        "TTToHplusBHminusB_M80_Spring11",  # v10, v11
#        "TTToHplusBHminusB_M100_Spring11", # v10, v11
#        "TTToHplusBHminusB_M120_Spring11", # v10, v11
#        "TTToHplusBHminusB_M140_Spring11", # v10, v11
#        "TTToHplusBHminusB_M150_Spring11", # v10, v11
#        "TTToHplusBHminusB_M155_Spring11", # v10, v11
#        "TTToHplusBHminusB_M160_Spring11", # v10, v11

        # MC Background Spring11
#        "QCD_Pt30to50_TuneZ2_Spring11",       # v10, v11
#        "QCD_Pt50to80_TuneZ2_Spring11",       # v10, v11
#        "QCD_Pt80to120_TuneZ2_Spring11",      # v10, v11
#        "QCD_Pt120to170_TuneZ2_Spring11",     # v10, v11
#        "QCD_Pt170to300_TuneZ2_Spring11",     # v10, v11
#        "QCD_Pt300to470_TuneZ2_Spring11",     # v10, v11
#        "WJets_TuneZ2_Spring11",              # v10, v11
#        "TTJets_TuneZ2_Spring11",             # v10, v11
#        "TToBLNu_s-channel_TuneZ2_Spring11",  # v10, v11
#        "TToBLNu_t-channel_TuneZ2_Spring11",  # v10, v11
#        "TToBLNu_tW-channel_TuneZ2_Spring11", # v10, v11
#        "DYJetsToLL_M50_TuneZ2_Spring11",     # v10, v11
#        "WW_TuneZ2_Spring11",                 # v10, v11
#        "WZ_TuneZ2_Spring11",                 # v10, v11
#        "ZZ_TuneZ2_Spring11",                 # v10, v11

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
