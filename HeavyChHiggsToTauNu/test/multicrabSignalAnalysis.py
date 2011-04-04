#!/usr/bin/env python

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab import *

multicrab = Multicrab("crab_analysis.cfg", "signalAnalysis_cfg.py")

# Select the pattuple version to use as an input
#pattupleVersion = "pattuple_v6"
#pattupleVersion = "pattuple_v9"
pattupleVersion = "pattuple_v10_test3"


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
        #### 41X data and 311X MC
        # Data: single tau + MET
        "Tau_160404-161176_Prompt", # HLT_IsoPFTau35_Trk20_MET45_v1
        "Tau_161216-161312_Prompt", # HLT_IsoPFTau35_Trk20_MET45_v2

        # Data: quadjet
        "TauPlusX_160404-161312_Prompt", # HLT_QuadJet40_IsoPFTau40_v1

        # MC Background Spring11
        "TTJets_TuneZ2_Spring11",

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

        #### 38X data and MC
        # Data
#        "BTau_141950-144114_Nov4", # v6
#        "BTau_146240-148107_Nov4", # v6
#        "BTau_148108-148864_Nov4", # v6
        # Data for QCD
#        "JetMETTau_136033-141887_Nov4", # v6
#        "JetMET_141950-144114_Nov4",    # v6
#        "Jet_146240-148058_Nov4",       # v6
        # MC Signal Fall10
#        "TTToHplusBWB_M90_Fall10",  # v6
#        "TTToHplusBWB_M100_Fall10", # v6
#        "TTToHplusBWB_M120_Fall10", # v6
#        "TTToHplusBWB_M140_Fall10", # v6
#        "TTToHplusBWB_M160_Fall10", # v6
        # MC Signal Fall10 PU
#        "TTToHplusBWB_M90_Fall10_PU",  # v6
#        "TTToHplusBWB_M100_Fall10_PU", # v6
#        "TTToHplusBWB_M120_Fall10_PU", # v6
#        "TTToHplusBWB_M140_Fall10_PU", # v6
#        "TTToHplusBWB_M160_Fall10_PU", # v6
        # MC Background Fall10
#        "QCD_Pt30to50_Fall10",   # v6
#        "QCD_Pt50to80_Fall10",   # v6
#        "QCD_Pt80to120_Fall10",  # v6
#        "QCD_Pt120to170_Fall10", # v6
#        "QCD_Pt170to300_Fall10", # v6
#        "TTJets",                # v6 
#        "WJets_Fall10",          # v6
        # MC Background Fall10 PU
#        "QCD_Pt30to50_Fall10_PU",   # v6
#        "QCD_Pt50to80_Fall10_PU",   # v6
#        "QCD_Pt80to120_Fall10_PU",  # v6
#        "QCD_Pt120to170_Fall10_PU", # v6
#        "QCD_Pt170to300_Fall10_PU", # v6
#        "TTJets_PU",                # v6 
#        "WJets_Fall10_PU",          # v6

        #### 35X/36X MC
        # MC Signal Spring10
#        "TTToHpmToTauNu_M90_Spring10",  # v6
#        "TTToHpmToTauNu_M100_Spring10", # v6
#        "TTToHpmToTauNu_M120_Spring10", # v6
#        "TTbar_Htaunu_M140_Spring10",   # v6
#        "TTbar_Htaunu_M160_Spring10",   # v6
        # MC Background Summer10
#        "QCD_Pt30to50_Summer10",   # v6
#        "QCD_Pt50to80_Summer10",   # v6
#        "QCD_Pt80to120_Summer10",  # v6
#        "QCD_Pt120to170_Summer10", # v6
#        "QCD_Pt170to230_Summer10", # v6
#        "QCD_Pt230to300_Summer10", # v6
#        "TTbar_Summer10",          # v6
#        "TTbarJets_Summer10",      # v6
#        "WJets_Summer10",          # v6
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
#multicrab.createTasks(configOnly=True)

# Genenerate configuration and create the crab tasks
multicrab.createTasks()

# Create a custom multicrab task directory (SignalAnalysis_xxxxxx_yyyyyy)
#multicrab.createTasks(prefix="SignalAnalysis")
