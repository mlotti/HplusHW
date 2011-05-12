#!/usr/bin/env python

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab import *

multicrab = Multicrab("crab_analysis.cfg", "signalAnalysis_cfg.py")

# Select the pattuple version to use as an input
#pattupleVersion = "pattuple_v9"
#pattupleVersion = "pattuple_v10"
pattupleVersion = "pattuple_v11"


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
        #### 39X/41X data and 311X MC
        # Data: single tau + MET
        # 2010
#        "BTau_146428-148058_Dec22", # HLT_SingleIsoTau20_Trk15_MET20;    v9, v10
#        "BTau_148822-149182_Dec22", # HLT_SingleIsoTau20_Trk15_MET25_v3; v9, v10
#        "BTau_149291-149294_Dec22", # HLT_SingleIsoTau20_Trk15_MET25_v4; v9, v10
        # 2011
        "Tau_160431-161016_Prompt", # HLT_IsoPFTau35_Trk20_MET45_v1; v10
        "Tau_162803-163261_Prompt", # HLT_IsoPFTau35_Trk20_MET45_v2; v10, v11
        "Tau_163270-163757_Prompt", # HLT_IsoPFTau35_Trk20_MET45_v4; v11

        # Data: quadjet
#        "TauPlusX_160431-161016_Prompt", # HLT_QuadJet40_IsoPFTau40_v1; v10
#        "TauPlusX_162803-163261_Prompt", # HLT_QuadJet40_IsoPFTau40_v1; v10
#        "TauPlusX_163270-163369_Prompt", # HLT_QuadJet40_IsoPFTau40_v3; v10

        # MC Signal WH Spring11
        "TTToHplusBWB_M80_Spring11", # v11
        "TTToHplusBWB_M90_Spring11", # v11
        "TTToHplusBWB_M100_Spring11", # v10, v11
        "TTToHplusBWB_M120_Spring11", # v10, v11
        "TTToHplusBWB_M140_Spring11", # v10, v11
        "TTToHplusBWB_M150_Spring11", # v10, v11
        "TTToHplusBWB_M155_Spring11", # v10, v11
        "TTToHplusBWB_M160_Spring11", # v10, v11

        # MC Signal HH Spring11
        "TTToHplusBHminusB_M80_Spring11",  # v10, v11
        "TTToHplusBHminusB_M100_Spring11", # v10, v11
        "TTToHplusBHminusB_M120_Spring11", # v10, v11
        "TTToHplusBHminusB_M140_Spring11", # v10, v11
        "TTToHplusBHminusB_M150_Spring11", # v10, v11
        "TTToHplusBHminusB_M155_Spring11", # v10, v11
        "TTToHplusBHminusB_M160_Spring11", # v10, v11

        # MC Background Spring11
        "QCD_Pt30to50_TuneZ2_Spring11",       # v10, v11
        "QCD_Pt50to80_TuneZ2_Spring11",       # v10, v11
        "QCD_Pt80to120_TuneZ2_Spring11",      # v10, v11
        "QCD_Pt120to170_TuneZ2_Spring11",     # v10, v11
        "QCD_Pt170to300_TuneZ2_Spring11",     # v10, v11
        "QCD_Pt300to470_TuneZ2_Spring11",     # v10, v11
        "WJets_TuneZ2_Spring11",              # v10, v11
        "TTJets_TuneZ2_Spring11",             # v10, v11
        "TToBLNu_s-channel_TuneZ2_Spring11",  # v10, v11
        "TToBLNu_t-channel_TuneZ2_Spring11",  # v10, v11
        "TToBLNu_tW-channel_TuneZ2_Spring11", # v10, v11
        "DYJetsToLL_M50_TuneZ2_Spring11",     # v10, v11
        "WW_TuneZ2_Spring11",                 # v10, v11
        "WZ_TuneZ2_Spring11",                 # v10, v11
        "ZZ_TuneZ2_Spring11",                 # v10, v11

        #### 39X data and MC
        # Data
#        "JetMETTau_Tau_136035-139975_Dec22", # v9
#        "JetMETTau_Tau_140058-141881_Dec22", # v9
#        "BTau_141956-144114_Dec22",          # v9
#        "BTau_146428-148058_Dec22",          # v9
#        "BTau_148822-149182_Dec22",          # v9
#        "BTau_149291-149294_Dec22",          # v9
        # Data for QCD
#        "JetMETTau_Jet_136035-141881_Dec22", # v9
#        "JetMET_141956-144114_Dec22",        # v9
#        "Jet_146428-148058_Dec22",           # v9
#        "Jet_148822-149294_Dec22",           # v9
        # Data for signal QuadJet (no pattuples, needs runPatOnTheFly=True
#        "JetMETTau_QuadJet_136035-141881_Dec22",
#        "JetMET_QuadJet_141956-144114_Dec22",
#        "Jet_QuadJet_146428-147116_Dec22",
#        "MultiJet_QuadJet_147196-148058_Dec22",
#        "MultiJet_QuadJet_148819-149442_Dec22",
        # MC Signal 10
#        "TTToHplusBWB_M90_Winter10",  # v9
#        "TTToHplusBWB_M100_Winter10", # v9
#        "TTToHplusBWB_M120_Winter10", # v9
#        "TTToHplusBWB_M140_Winter10", # v9
#        "TTToHplusBWB_M160_Winter10", # v9
        # MC Background Winter10
#        "QCD_Pt30to50_TuneZ2_Winter10",   # v9
#        "QCD_Pt50to80_TuneZ2_Winter10",   # v9
#        "QCD_Pt80to120_TuneZ2_Winter10",  # v9
#        "QCD_Pt120to170_TuneZ2_Winter10", # v9
#        "QCD_Pt170to300_TuneZ2_Winter10", # v9
#        "QCD_Pt300to470_TuneZ2_Winter10", # v9
#        "TTJets_TuneZ2_Winter10",         # v9
#        "TTJets_TuneD6T_Winter10",        # v9 
#        "WJets_TuneZ2_Winter10",          # v9
#        "WJets_TuneZ2_Winter10_noPU",     # v9
#        "WJets_TuneD6T_Winter10",         # v9
#        "W2Jets_ptW0to100_TuneZ2_Winter10",   # v9
#        "W2Jets_ptW100to300_TuneZ2_Winter10", # v9
#        "W3Jets_ptW0to100_TuneZ2_Winter10",   # v9
#        "W3Jets_ptW100to300_TuneZ2_Winter10", # v9
#        "W4Jets_ptW0to100_TuneZ2_Winter10",   # v9
#        "W4Jets_ptW100to300_TuneZ2_Winter10", # v9
#        "WW_TuneZ2_Winter10", # v9
#        "WZ_TuneZ2_Winter10", # v9
#        "ZZ_TuneZ2_Winter10", # v9
#        "TToBLNu_s-channel_TuneZ2_Winter10", # v9
#        "TToBLNu_t-channel_TuneZ2_Winter10", # v9
#        "TToBLNu_tW-channel_TuneZ2_Winter10", # v9
#        "DYJetsToLL_M50_TuneZ2_Winter10", # v9
        ])

# Force all jobs go to jade, in some situations this might speed up
# the analysis (e.g. when there are O(1000) Alice jobs queueing, all
# CMS jobs typically go to korundi).
if not runPatOnTheFly:
    multicrab.extendBlackWhiteListAll("ce_white_list", ["jade-cms.hip.fi"])


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
