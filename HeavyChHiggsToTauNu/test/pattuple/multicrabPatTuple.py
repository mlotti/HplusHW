#!/usr/bin/env python

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab import *

multicrab = Multicrab("crab_pat.cfg")

multicrab.addDatasets(
#    "AOD",
    "RECO",
    [
        # Data
#        "BTau_141950-144114",
#        "BTau_146240-148107",
#        "BTau_148108-148864",
        # Signal MC
#        "TTToHpmToTauNu_M90",
#        "TTToHpmToTauNu_M100",
#        "TTToHpmToTauNu_M120",
#        "TTbar_Htaunu_M140",
#        "TTbar_Htaunu_M160",
        # Signal Fall10 MC
#        "TTToHplusBWB_M90",
#        "TTToHplusBWB_M100",
#        "TTToHplusBWB_M120",
#        "TTToHplusBWB_M140",
#        "TTToHplusBWB_M160",
        # Background MC
#        "QCD_Pt30to50",
#        "QCD_Pt50to80",
#        "QCD_Pt80to120",
#        "QCD_Pt120to170",
#        "QCD_Pt170to230",
#        "QCD_Pt230to300",
#        "QCD_Pt30to50_Fall10",
#        "QCD_Pt50to80_Fall10",
#        "QCD_Pt80to120_Fall10",
#        "QCD_Pt120to170_Fall10",
#        "QCD_Pt170to300_Fall10",
#        "TTbar",
#        "TTbarJets",
#        "WJets",
        ])

multicrab.setDataLumiMask("../Cert_132440-149442_7TeV_StreamExpress_Collisions10_JSON.txt")

#multicrab.modifyLumisPerJobAll(lambda nlumis: nlumis*0.5)
#multicrab.modifyNumberOfJobsAll(lambda njobs: njobs*2)

def addOutputName(dataset):
    path = dataset.getDatasetPath().split("/")
    name = path[2].replace("-", "_")
    name += "_"+path[3]
    #name += "_pattuple_v6_1"
    name += "_pattuple_v6_1b"

    dataset.addLine("USER.publish_data_name = "+name)
multicrab.forEachDataset(addOutputName)

# For collision data stageout from US doesn't seem to be a problem
def blacklistUS(dataset):
    if dataset.isMC():
        dataset.addBlackWhiteList("se_black_list", ["T2_US"])
multicrab.forEachDataset(blacklistUS)

# Many failures with 60307 and 70500 from T2_UK_London_Brunel for
# pattuple_v6_1 while the similar jobs stageout fine in other T2s
multicrab.addBlackWhiteListAll("se_black_list", ["T2_UK_London_Brunel"])

multicrab.createTasks()
#multicrab.createTasks(configOnly=True)
