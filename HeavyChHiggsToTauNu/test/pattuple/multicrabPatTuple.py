#!/usr/bin/env python

import re

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab import *
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.certifiedLumi as lumi

multicrab = Multicrab("crab_pat.cfg", lumiMaskDir="..")

multicrab.extendDatasets(
    "AOD",
#    "RECO",
    [
########
#
# 41X
#
########
    # Data
# With DCSOnly json
#    "Tau_160404-161176_Prompt", # HLT_IsoPFTau35_Trk20_MET45_v1
#    "Tau_161216-161312_Prompt", # HLT_IsoPFTau35_Trk20_MET45_v2
#    "TauPlusX_160404-161312_Prompt" # HLT_QuadJet40_IsoPFTau40_v1
# With certified json
#        "Tau_160431-161016_Prompt", # HLT_IsoPFTau35_Trk20_MET45_v1
#        "Tau_162803-163261_Prompt", # HLT_IsoPFTau35_Trk20_MET45_v2
#        "Tau_163270-163369_Prompt", # HLT_IsoPFTau35_Trk20_MET45_v4

#        "TauPlusX_160431-161016_Prompt", # HLT_QuadJet40_IsoPFTau40_v1
#        "TauPlusX_162803-163261_Prompt", # HLT_QuadJet40_IsoPFTau40_v1
#        "TauPlusX_163270-163369_Prompt", # HLT_QuadJet40_IsoPFTau40_v3

########
#
# 311X
#
########
        # Signal MC (WH)
#        "TTToHplusBWB_M80_Spring11",
#        "TTToHplusBWB_M90_Spring11",
#        "TTToHplusBWB_M100_Spring11",
#        "TTToHplusBWB_M120_Spring11",
#        "TTToHplusBWB_M140_Spring11",
#        "TTToHplusBWB_M150_Spring11",
#        "TTToHplusBWB_M155_Spring11",
#        "TTToHplusBWB_M160_Spring11",
        # (HH)
#        "TTToHplusBHminusB_M80_Spring11",
#        "TTToHplusBHminusB_M100_Spring11",
#        "TTToHplusBHminusB_M120_Spring11",
#        "TTToHplusBHminusB_M140_Spring11",
#        "TTToHplusBHminusB_M150_Spring11",
#        "TTToHplusBHminusB_M155_Spring11",
#        "TTToHplusBHminusB_M160_Spring11",

        # Background MC
#        "QCD_Pt30to50_TuneZ2_Spring11",
#        "QCD_Pt50to80_TuneZ2_Spring11",
#        "QCD_Pt80to120_TuneZ2_Spring11",
#        "QCD_Pt120to170_TuneZ2_Spring11",
#        "QCD_Pt170to300_TuneZ2_Spring11",
#        "QCD_Pt300to470_TuneZ2_Spring11",
#        "TTJets_TuneZ2_Spring11",
#        "WJets_TuneZ2_Spring11"
#        "TToBLNu_s-channel_TuneZ2_Spring11",
#        "TToBLNu_t-channel_TuneZ2_Spring11",
#        "TToBLNu_tW-channel_TuneZ2_Spring11",
#        "DYJetsToLL_M50_TuneZ2_Spring11",
#        "WW_TuneZ2_Spring11",
#        "WZ_TuneZ2_Spring11",
#        "ZZ_TuneZ2_Spring11",

########
#
# 39X
#
########
        # Data (Tau)
#        "JetMETTau_Tau_136035-139975_Dec22", # HLT_SingleLooseIsoTau20
#        "JetMETTau_Tau_140058-141881_Dec22", # HLT_SingleLooseIsoTau20_Trk5
#        "BTau_141956-144114_Dec22", # HLT_SingleIsoTau20_Trk5
#        "BTau_146428-148058_Dec22", # HLT_SingleIsoTau20_Trk15_MET20
#        "BTau_148822-149182_Dec22", # HLT_SingleIsoTau20_Trk15_MET25_v3
#        "BTau_149291-149294_Dec22", # HLT_SingleIsoTau20_Trk15_MET25_v4

        # Data (QuadJet)
#        "JetMETTau_QuadJet_136035-141881_Dec22", # HLT_QuadJet15U
#        "JetMET_QuadJet_141956-144114_Dec22",    # HLT_QuadJet15U
#        "Jet_QuadJet_146428-147116_Dec22",       # HLT_QuadJet25U
#        "MultiJet_QuadJet_147196-148058_Dec22",  # HLT_QuadJet25U_v2
#        "MultiJet_QuadJet_148819-149442_Dec22",  # HLT_QuadJet25U_v3

        # Data (Jet)
#        "JetMETTau_Jet_136035-141881_Dec22", # HLT_Jet30U
#        "JetMET_141956-144114_Dec22",        # HLT_Jet30U
#        "Jet_146428-148058_Dec22",           # HLT_Jet30U
#        "Jet_148822-149294_Dec22",           # HLT_Jet30U_v3

        # Signal MC
#        "TTToHplusBWB_M90_Winter10",
#        "TTToHplusBWB_M100_Winter10",
#        "TTToHplusBWB_M120_Winter10",
#        "TTToHplusBWB_M140_Winter10",
#        "TTToHplusBWB_M160_Winter10",

        # Background MC
#        "QCD_Pt30to50_TuneZ2_Winter10",
#        "QCD_Pt50to80_TuneZ2_Winter10",
#        "QCD_Pt80to120_TuneZ2_Winter10",
#        "QCD_Pt120to170_TuneZ2_Winter10",
#        "QCD_Pt170to300_TuneZ2_Winter10",
#        "QCD_Pt300to470_TuneZ2_Winter10",
#        "TTJets_TuneD6T_Winter10",
#        "TTJets_TuneZ2_Winter10",
#        "WJets_TuneD6T_Winter10",
#        "WJets_TuneZ2_Winter10",
#        "WJets_TuneZ2_Winter10_noPU",
#        "DYJetsToLL_M10to50_TuneD6T_Winter10",
#        "DYJetsToLL_M50_TuneD6T_Winter10",
#        "DYJetsToLL_M50_TuneZ2_Winter10",
#        "TToBLNu_s-channel_Winter10",
#        "TToBLNu_t-channel_Winter10",
#        "TToBLNu_tW-channel_Winter10"
#        "W2Jets_ptW0to100_TuneZ2_Winter10",
#        "W2Jets_ptW100to300_TuneZ2_Winter10",
#        "W3Jets_ptW0to100_TuneZ2_Winter10",
#        "W3Jets_ptW100to300_TuneZ2_Winter10",
#        "W4Jets_ptW0to100_TuneZ2_Winter10",
#        "W4Jets_ptW100to300_TuneZ2_Winter10",
#        "WW_TuneZ2_Winter10",
#        "WZ_TuneZ2_Winter10",
#        "ZZ_TuneZ2_Winter10",
          
########
#
# 38X
#
########
        # Data (Tau)
#        "BTau_141950-144114_Nov4", # HLT_SingleIsoTau20_Trk5
#        "BTau_146240-148107_Nov4", # HLT_SingleIsoTau20_Trk15_MET20
#        "BTau_148108-149182_Nov4", # HLT_SingleIsoTau20_Trk15_MET25_v3
#        "BTau_149291-149442_Nov4", # HLT_SingleIsoTau20_Trk15_MET25_v4
        # Data (Jet)
#        "JetMETTau_136033-141887_Nov4", # HLT_Jet30U
#        "JetMET_141950-144114_Nov4",    # HLT_Jet30U
#        "Jet_146240-148058_Nov4",       # HLT_Jet30U
        # Signal Fall10 MC
#        "TTToHplusBWB_M90_Fall10",
#        "TTToHplusBWB_M100_Fall10",
#        "TTToHplusBWB_M120_Fall10",
#        "TTToHplusBWB_M140_Fall10",
#        "TTToHplusBWB_M160_Fall10",
        # Signal MC
#        "TTToHpmToTauNu_M90_Spring10",
#        "TTToHpmToTauNu_M100_Spring10",
#        "TTToHpmToTauNu_M120_Spring10",
#        "TTbar_Htaunu_M140_Spring10",
#        "TTbar_Htaunu_M160_Spring10",
        # Background Fall10 MC
#        "QCD_Pt30to50_TuneZ2_Fall10",
#        "QCD_Pt50to80_TuneZ2_Fall10",
#        "QCD_Pt80to120_TuneZ2_Fall10",
#        "QCD_Pt120to170_TuneZ2_Fall10",
#        "QCD_Pt170to300_TuneZ2_Fall10",
#        "TT_TuneZ2_Fall10",
#        "TTJets_TuneZ2_Fall10",
#        "WJets_TuneZ2_Fall10"
        # Background MC
#        "QCD_Pt30to50_Summer10",
#        "QCD_Pt50to80_Summer10",
#        "QCD_Pt80to120_Summer10",
#        "QCD_Pt120to170_Summer10",
#        "QCD_Pt170to230_Summer10",
#        "QCD_Pt230to300_Summer10",
#        "TTbar_Summer10",
#        "TTbarJets_Summer10",
#        "WJets_Summer10",
        ])

# local_stage_out doesn't work due to denied permission because we're
# writing to /store/group/local ...
#multicrab.addLineAll("USER.local_stage_out=1")

multicrab.appendLineAll("GRID.maxtarballsize = 15")
multicrab.appendArgAll("runOnCrab=1")

reco_re = re.compile("(?P<reco>Reco_v\d+_[^_]+_)")
run_re = re.compile("^(?P<pd>[^_]+?)_((?P<trig>[^_]+?)_)?(?P<frun>\d+)-(?P<lrun>\d+)_")

def addOutputName(dataset):
    path = dataset.getDatasetPath().split("/")
    name = path[2].replace("-", "_")
    name += "_"+path[3]
    name += "_pattuple_v11"

    # Add the begin run in the dataset name to the publish name in
    # order to distinguish pattuple datasets from the same PD
    if dataset.isData():
        m = run_re.search(dataset.getName())
        frun = m.group("frun")
        trig = ""
        if m.group("trig"):
            trig = m.group("trig")+"_"

        m = reco_re.search(name)
        name = reco_re.sub(m.group("reco")+trig+frun+"_", name)

    dataset.appendLine("USER.publish_data_name = "+name)
multicrab.forEachDataset(addOutputName)

def addSplitMode(dataset):
    if dataset.isMC():
        dataset.appendLine("CMSSW.total_number_of_events = -1")
    else:
        dataset.appendLine("CMSSW.total_number_of_lumis = -1")
multicrab.forEachDataset(addSplitMode)

# For collision data stageout from US doesn't seem to be a problem
#allowUS = ["TT", "TTJets", "TTToHplusBWB_M90", "TTToHplusBWB_M100", "TTToHplusBWB_M120", "TTToHplusBWB_M140", "TTToHplusBWB_M160"]
#def blacklistUS(dataset):
#    if dataset.isMC() and not dataset.getName() in allowUS:
#        dataset.extendBlackWhiteList("se_black_list", ["T2_US"])
#multicrab.forEachDataset(blacklistUS)

# Many failures with 60307 and 70500 from T2_UK_London_Brunel for
# pattuple_v6_1 while the similar jobs stageout fine in other T2s
multicrab.extendBlackWhiteListAll("se_black_list", defaultSeBlacklist)

# Create multicrab task configuration and run 'multicrab -create'
multicrab.createTasks()

# Create task configuration only
#multicrab.createTasks(configOnly=True)
