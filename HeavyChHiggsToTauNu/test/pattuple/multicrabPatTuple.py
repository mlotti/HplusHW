#!/usr/bin/env python

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab import *

multicrab = Multicrab("crab_pat.cfg")

multicrab.addDatasets(
#    "AOD",
    "RECO",
    [
        # Data
#        "BTau_141950-144114", # HLT_SingleIsoTau20_Trk5
#        "BTau_146240-148107", # HLT_SingleIsoTau20_Trk15_MET20
#        "BTau_148108-149182", # HLT_SingleIsoTau20_Trk15_MET25_v3
#        "BTau_149291-149442", # HLT_SingleIsoTau20_Trk15_MET25_v4
        # Signal Fall10 MC
#        "TTToHplusBWB_M90",
#        "TTToHplusBWB_M100",
#        "TTToHplusBWB_M120",
#        "TTToHplusBWB_M140",
#        "TTToHplusBWB_M160",
        # Signal MC
#        "TTToHpmToTauNu_M90",
#        "TTToHpmToTauNu_M100",
#        "TTToHpmToTauNu_M120",
#        "TTbar_Htaunu_M140",
#        "TTbar_Htaunu_M160",
        # Background Fall10 MC
#        "QCD_Pt30to50_Fall10",
#        "QCD_Pt50to80_Fall10",
#        "QCD_Pt80to120_Fall10",
#        "QCD_Pt120to170_Fall10",
#        "QCD_Pt170to300_Fall10",
#        "TT",
#        "TTJets",
        # Background MC
#        "QCD_Pt30to50",
#        "QCD_Pt50to80",
#        "QCD_Pt80to120",
#        "QCD_Pt120to170",
#        "QCD_Pt170to230",
#        "QCD_Pt230to300",
#        "TTbar",
#        "TTbarJets",
#        "WJets",
        ])

# The recommendation is to use different lists for the Sep17ReReco and
# Run2010B_PromptReco, see e.g.
# https://hypernews.cern.ch/HyperNews/CMS/get/physics-validation/1011.html
multicrab.setDataLumiMask("../Cert_132440-149442_7TeV_StreamExpress_Collisions10_JSON_v3.txt")
multicrab.getDataset("BTau_141950-144114").setLumiMask("../Cert_132440-144114_7TeV_Sep17ReReco_Collisions10_JSON.txt")

# local_stage_out doesn't work due to denied permission because we're
# writing to /store/group/local ...
#multicrab.addLineAll("USER.local_stage_out=1")

#multicrab.modifyLumisPerJobAll(lambda nlumis: nlumis*0.5)
#multicrab.modifyNumberOfJobsAll(lambda njobs: njobs*2)

def addOutputName(dataset):
    path = dataset.getDatasetPath().split("/")
    name = path[2].replace("-", "_")
    name += "_"+path[3]
    name += "_pattuple_v6_1"

    dataset.addLine("USER.publish_data_name = "+name)
multicrab.forEachDataset(addOutputName)

# For collision data stageout from US doesn't seem to be a problem
allowUS = ["TT", "TTJets"]
def blacklistUS(dataset):
    if dataset.isMC() and not dataset.getName() in allowUS:
        dataset.addBlackWhiteList("se_black_list", ["T2_US"])
multicrab.forEachDataset(blacklistUS)

# Many failures with 60307 and 70500 from T2_UK_London_Brunel for
# pattuple_v6_1 while the similar jobs stageout fine in other T2s
multicrab.addBlackWhiteListAll("se_black_list", ["T2_UK_London_Brunel"])

multicrab.createTasks()
#multicrab.createTasks(configOnly=True)
