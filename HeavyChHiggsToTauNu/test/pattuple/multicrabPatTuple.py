#!/usr/bin/env python

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab import *

multicrab = Multicrab("crab_pat.cfg")

multicrab.setDatasets([
        # Data
        "BTau_141950-144114",
        "BTau_146240-148107",
        "BTau_148108-148864",
        # Signal MC
        "TTbar_Htaunu_M80",
        "TTToHpmToTauNu_M90",
        "TTToHpmToTauNu_M100",
        "TTToHpmToTauNu_M120",
        "TTbar_Htaunu_M140",
        "TTbar_Htaunu_M160",
        # Background MC
        "QCD_Pt30to50",
        "QCD_Pt50to80",
        "QCD_Pt80to120",
        "QCD_Pt120to170",
        "QCD_Pt170to230",
        "QCD_Pt230to300",
        "QCD_Pt30to50_Fall10",
        "QCD_Pt50to80_Fall10",
        "QCD_Pt80to120_Fall10",
        "QCD_Pt120to170_Fall10",
        "QCD_Pt170to300_Fall10",
        "TTbar",
        "TTbarJets",
        "WJets",
        ])

#multicrab.setDataInput("AOD")
multicrab.setDataInput("RECO")
multicrab.setDataLumiMask("../Cert_132440-148864_7TeV_StreamExpress_Collisions10_JSON.txt")
multicrab.addArgAll("doPat=1")

#multicrab.modifyLumisPerJobAll(lambda nlumis: nlumis*0.5)
#multicrab.modifyNumberOfJobsAll(lambda njobs: njobs*2)

def addOutputName(dataset):
    path = dataset.getDatasetPath().split("/")
    name = path[2].replace("-", "_")
    name += "_"+path[3]
    name += "_pattuple_v7_test1"

    dataset.addLine("USER.publish_data_name = "+name)
multicrab.forEachDataset(addOutputName)

multicrab.createTasks()
#multicrab.createTasks(configOnly=True)
