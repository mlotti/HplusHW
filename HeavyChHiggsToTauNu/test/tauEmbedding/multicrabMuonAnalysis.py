#!/usr/bin/env python

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab import *

multicrab = Multicrab("../crab_analysis.cfg", "muonAnalysis_cfg.py")

aodDatasets = [
    # Data
    "Mu_135821-144114",
    "Mu_146240-147116",
    "Mu_147196-149442",
    # Signal MC (Fall10)
#    "TT",
    "TTJets",
    # Background MC (Fall10)
    "QCD_Pt20_MuEnriched",
    "DYJetsToLL", # Z+jets
    "TToBLNu_s-channel",
    "TToBLNu_t-channel",
    "TToBLNu_tW-channel",
    # Background MC (Summer10)
#    "ZJets",
#    "SingleTop_sChannel",
#    "SingleTop_tChannel",
#    "SingleTop_tWChannel",
    ]
patDatasets = [
    # Signal MC
#    "TT",
#    "TTJets", # Fall10
    "WJets", # Summer10
    # Background MC
    "QCD_Pt30to50_Fall10",
    "QCD_Pt50to80_Fall10",
    "QCD_Pt80to120_Fall10",
    "QCD_Pt120to170_Fall10",
    "QCD_Pt170to300_Fall10",
]

#usePatTuples = True
usePatTuples = False

if usePatTuples:
    multicrab.addDatasets("pattuple_v6", patDatasets)
else:
    aodDatasets.extend(patDatasets)
multicrab.addDatasets("AOD", aodDatasets)

multicrab.setDataLumiMask("Cert_132440-149442_7TeV_StreamExpress_Collisions10_JSON.txt")

#multicrab.getDataset("TTbarJets").addArg("WDecaySeparate=1")
multicrab.getDataset("TTJets").addArg("WDecaySeparate=1")
multicrab.getDataset("TTJets").setNumberOfJobs(5)
multicrab.getDataset("WJets").addArg("WDecaySeparate=1")
multicrab.getDataset("TToBLNu_s-channel").addArg("WDecaySeparate=1")
multicrab.getDataset("TToBLNu_t-channel").addArg("WDecaySeparate=1")
multicrab.getDataset("TToBLNu_tW-channel").addArg("WDecaySeparate=1")


for name in aodDatasets:
    multicrab.getDataset(name).addArg("doPat=1")

#multicrab.modifyLumisPerJobAll(lambda nlumis: nlumis*0.5)
#multicrab.modifyNumberOfJobsAll(lambda njobs: njobs*2)

#multicrab.createTasks()
multicrab.createTasks(configOnly=True)
