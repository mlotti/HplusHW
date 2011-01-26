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
# 39X
#
########
        # Data (tau)
#        "BTau_141956-144114_Dec22", # HLT_SingleIsoTau20_Trk5
#        "BTau_146428-148058_Dec22", # HLT_SingleIsoTau20_Trk15_MET20
#        "BTau_148822-149182_Dec22", # HLT_SingleIsoTau20_Trk15_MET25_v3
#        "BTau_149291-149294_Dec22", # HLT_SingleIsoTau20_Trk15_MET25_v4

        # Data (Jet)
#        "JetMETTau_136035-141881_Dec22",
#        "JetMET_141956-144114_Dec22",
#        "Jet_146428-148058_Dec22",

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
#        "WJets_TuneZ2_Winter10_noPU",

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

reco_re = re.compile("(?P<reco>Reco_v\d+_[^_]+_)")

def addOutputName(dataset):
    path = dataset.getDatasetPath().split("/")
    name = path[2].replace("-", "_")
    name += "_"+path[3]
    name += "_pattuple_v9"

    # Add the begin run in the dataset name to the publish name in
    # order to distinguish pattuple datasets from the same PD
    if dataset.isData():
        frun = dataset.getName().split("_")[1].split("-")[0]
        m = reco_re.search(name)
        name = reco_re.sub(m.group("reco")+frun+"_", name)

    dataset.appendLine("USER.publish_data_name = "+name)
multicrab.forEachDataset(addOutputName)

# For collision data stageout from US doesn't seem to be a problem
#allowUS = ["TT", "TTJets", "TTToHplusBWB_M90", "TTToHplusBWB_M100", "TTToHplusBWB_M120", "TTToHplusBWB_M140", "TTToHplusBWB_M160"]
#def blacklistUS(dataset):
#    if dataset.isMC() and not dataset.getName() in allowUS:
#        dataset.extendBlackWhiteList("se_black_list", ["T2_US"])
#multicrab.forEachDataset(blacklistUS)

# Many failures with 60307 and 70500 from T2_UK_London_Brunel for
# pattuple_v6_1 while the similar jobs stageout fine in other T2s
multicrab.extendBlackWhiteListAll("se_black_list", ["T2_UK_London_Brunel"])

# Create multicrab task configuration and run 'multicrab -create'
multicrab.createTasks()

# Create task configuration only
#multicrab.createTasks(configOnly=True)
