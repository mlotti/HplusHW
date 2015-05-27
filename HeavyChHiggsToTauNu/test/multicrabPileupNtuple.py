#!/usr/bin/env python

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab import *


multicrab = Multicrab("crab_analysis.cfg", "pileupNtuple_cfg.py")

datasets_44X = [
    # MC Signal (WH)
    "TTToHplusBWB_M80_Fall11",
    "TTToHplusBWB_M90_Fall11",
    "TTToHplusBWB_M100_Fall11",
    "TTToHplusBWB_M120_Fall11",
    "TTToHplusBWB_M140_Fall11",
    "TTToHplusBWB_M150_Fall11",
    "TTToHplusBWB_M155_Fall11",
    "TTToHplusBWB_M160_Fall11",

    # MC Signal (HH)
    "TTToHplusBHminusB_M80_Fall11",
    "TTToHplusBHminusB_M90_Fall11",
    "TTToHplusBHminusB_M100_Fall11",
    "TTToHplusBHminusB_M120_Fall11",
    "TTToHplusBHminusB_M140_Fall11",
    "TTToHplusBHminusB_M150_Fall11",
    "TTToHplusBHminusB_M155_Fall11",
    "TTToHplusBHminusB_M160_Fall11",

    # MC Signal (heavy H+ from process pp->tbH+)
    "HplusTB_M180_Fall11",
    "HplusTB_M190_Fall11",
    "HplusTB_M200_Fall11",
    "HplusTB_M220_Fall11",
    "HplusTB_M250_Fall11",
    "HplusTB_M300_Fall11",

    # MC Background
    "QCD_Pt30to50_TuneZ2_Fall11",
    "QCD_Pt50to80_TuneZ2_Fall11",
    "QCD_Pt80to120_TuneZ2_Fall11",
    "QCD_Pt120to170_TuneZ2_Fall11",
    "QCD_Pt170to300_TuneZ2_Fall11",
    "QCD_Pt300to470_TuneZ2_Fall11",
    "QCD_Pt20_MuEnriched_TuneZ2_Fall11",
    "TTJets_TuneZ2_Fall11",
    "WJets_TuneZ2_Fall11",
    "W1Jets_TuneZ2_Fall11",
    "W2Jets_TuneZ2_Fall11",
    "W3Jets_TuneZ2_Fall11",
    "W3Jets_TuneZ2_v2_Fall11",
    "W4Jets_TuneZ2_Fall11",
    "DYJetsToLL_M50_TuneZ2_Fall11",
    "T_t-channel_TuneZ2_Fall11",
    "Tbar_t-channel_TuneZ2_Fall11",
    "T_tW-channel_TuneZ2_Fall11",
    "Tbar_tW-channel_TuneZ2_Fall11",
    "T_s-channel_TuneZ2_Fall11",
    "Tbar_s-channel_TuneZ2_Fall11",
    "WW_TuneZ2_Fall11",
    "WZ_TuneZ2_Fall11",
    "ZZ_TuneZ2_Fall11",
]

datasets_53X = [
    "TTToHplusBWB_M80_Summer12",
    "TTToHplusBWB_M90_Summer12",
    "TTToHplusBWB_M100_Summer12",
    "TTToHplusBWB_M120_Summer12",
    "TTToHplusBWB_M140_Summer12",
    "TTToHplusBWB_M150_Summer12",
    "TTToHplusBWB_M155_Summer12",
    "TTToHplusBWB_M160_Summer12",

    "TTToHplusBWB_M80_ext_Summer12",
    "TTToHplusBWB_M90_ext_Summer12",
    "TTToHplusBWB_M100_ext_Summer12",
    "TTToHplusBWB_M120_ext_Summer12",
    "TTToHplusBWB_M140_ext_Summer12",
    "TTToHplusBWB_M150_ext_Summer12",
    "TTToHplusBWB_M155_ext_Summer12",
    "TTToHplusBWB_M160_ext_Summer12",

    "TTToHplusBHminusB_M80_Summer12",
    "TTToHplusBHminusB_M90_Summer12",
    "TTToHplusBHminusB_M100_Summer12",
    "TTToHplusBHminusB_M120_Summer12",
    "TTToHplusBHminusB_M140_Summer12",
    "TTToHplusBHminusB_M150_Summer12",
    "TTToHplusBHminusB_M155_Summer12",
    "TTToHplusBHminusB_M160_Summer12",

    "TTToHplusBHminusB_M80_ext_Summer12",
    "TTToHplusBHminusB_M100_ext_Summer12",
    "TTToHplusBHminusB_M120_ext_Summer12",
    "TTToHplusBHminusB_M140_ext_Summer12",
    "TTToHplusBHminusB_M150_ext_Summer12",
    "TTToHplusBHminusB_M155_ext_Summer12",
    "TTToHplusBHminusB_M160_ext_Summer12",

    "Hplus_taunu_t-channel_M80_Summer12",
    "Hplus_taunu_t-channel_M90_Summer12",
    "Hplus_taunu_t-channel_M100_Summer12",
    "Hplus_taunu_t-channel_M120_Summer12",
    "Hplus_taunu_t-channel_M140_Summer12",
    "Hplus_taunu_t-channel_M150_Summer12",
    "Hplus_taunu_t-channel_M155_Summer12",
    "Hplus_taunu_t-channel_M160_Summer12",

    "Hplus_taunu_tW-channel_M80_Summer12",
    "Hplus_taunu_tW-channel_M90_Summer12",
    "Hplus_taunu_tW-channel_M100_Summer12",
    "Hplus_taunu_tW-channel_M120_Summer12",
    "Hplus_taunu_tW-channel_M140_Summer12",
    "Hplus_taunu_tW-channel_M150_Summer12",
    "Hplus_taunu_tW-channel_M155_Summer12",
    "Hplus_taunu_tW-channel_M160_Summer12",

    "Hplus_taunu_s-channel_M80_Summer12",
    "Hplus_taunu_s-channel_M90_Summer12",
    "Hplus_taunu_s-channel_M100_Summer12",
    "Hplus_taunu_s-channel_M120_Summer12",
    "Hplus_taunu_s-channel_M140_Summer12",
    "Hplus_taunu_s-channel_M150_Summer12",
    "Hplus_taunu_s-channel_M155_Summer12",
    "Hplus_taunu_s-channel_M160_Summer12",

    "HplusTB_M180_Summer12",
    "HplusTB_M190_Summer12",
    "HplusTB_M200_Summer12",
    "HplusTB_M220_Summer12",
    "HplusTB_M250_Summer12",
    "HplusTB_M300_Summer12",
    "HplusTB_M400_Summer12",
    "HplusTB_M500_Summer12",
    "HplusTB_M600_Summer12",

    "HplusTB_M180_ext_Summer12",
    "HplusTB_M190_ext_Summer12",
    "HplusTB_M200_ext_Summer12",
    "HplusTB_M220_ext_Summer12",
    "HplusTB_M250_ext_Summer12",
    "HplusTB_M300_ext_Summer12",

    "HplusToTBbar_M180_Summer12",
    "HplusToTBbar_M200_Summer12",
    "HplusToTBbar_M220_Summer12",
    "HplusToTBbar_M240_Summer12",
    "HplusToTBbar_M250_Summer12",
    "HplusToTBbar_M260_Summer12",
    "HplusToTBbar_M280_Summer12",
    "HplusToTBbar_M300_Summer12",
    "HplusToTBbar_M350_Summer12",
    "HplusToTBbar_M400_Summer12",
    "HplusToTBbar_M500_Summer12",
    "HplusToTBbar_M600_Summer12",
    "HplusToTBbar_M700_Summer12",

    "QCD_Pt30to50_TuneZ2star_Summer12",
    "QCD_Pt50to80_TuneZ2star_Summer12",
    "QCD_Pt80to120_TuneZ2star_Summer12",
    "QCD_Pt120to170_TuneZ2star_Summer12",
    "QCD_Pt170to300_TuneZ2star_Summer12",
    "QCD_Pt170to300_TuneZ2star_v2_Summer12",
    "QCD_Pt300to470_TuneZ2star_Summer12",
    "QCD_Pt300to470_TuneZ2star_v2_Summer12",
    "QCD_Pt300to470_TuneZ2star_v3_Summer12",
    "QCD_Pt20_MuEnriched_TuneZ2star_Summer12",
        
    "WW_TuneZ2star_Summer12",
    "WZ_TuneZ2star_Summer12",
    "ZZ_TuneZ2star_Summer12",
    "TTJets_TuneZ2star_Summer12",
    "TTJets_FullLept_TuneZ2star_Summer12",
    "TTJets_SemiLept_TuneZ2star_Summer12",
    "TTJets_Hadronic_TuneZ2star_ext_Summer12",
    "WJets_TuneZ2star_v1_Summer12",
    "WJets_TuneZ2star_v2_Summer12",
    "W1Jets_TuneZ2star_Summer12",
    "W2Jets_TuneZ2star_Summer12",
    "W3Jets_TuneZ2star_Summer12",
    "W4Jets_TuneZ2star_Summer12",
    "DYJetsToLL_M50_TuneZ2star_Summer12",
    "DYJetsToLL_M10to50_TuneZ2star_Summer12",
    "T_t-channel_TuneZ2star_Summer12",
    "Tbar_t-channel_TuneZ2star_Summer12",
    "T_tW-channel_TuneZ2star_Summer12",
    "Tbar_tW-channel_TuneZ2star_Summer12",
    "T_s-channel_TuneZ2star_Summer12",
    "Tbar_s-channel_TuneZ2star_Summer12",
]

# Add the datasest to the multicrab system
#multicrab.extendDatasets("pileupNtuple_44X", datasets_44X)
multicrab.extendDatasets("pileupNtuple_53X", datasets_53X)

multicrab.extendBlackWhiteListAll("se_black_list", defaultSeBlacklist_noStageout)

# Generate configuration only?
configOnly=True
#configOnly=False
# Genenerate configuration and create the crab tasks
multicrab.createTasks(prefix="multicrab_pileupNtuple", configOnly=configOnly)

