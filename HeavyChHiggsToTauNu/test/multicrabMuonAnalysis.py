#!/usr/bin/env python

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab import *

multicrab = Multicrab("crab_analysis.cfg", "muonAnalysis_cfg.py")

aodDatasets = [
    # Data
    "Mu_135821-144114",
    "Mu_146240-147116",
    "Mu_147196-148058",
    # Background MC
    "ZJets",
    "SingleTop_sChannel",
    "SingleTop_tChannel",
    "SingleTop_tWChannel",
    ]
patDatasets = [
    # Signal MC
#    "TTbar",
    "TTbarJets",
    "WJets",
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
    multicrab.addDatasets("pattuple_v3", patDatasets)
else:
    aodDatasets.extend(patDatasets)
multicrab.addDatasets("AOD", aodDatasets)

multicrab.setDataLumiMask("Cert_132440-149442_7TeV_StreamExpress_Collisions10_JSON.txt")


for name in aodDatasets:
    multicrab.getDataset(name).addArg("doPat=1")

#multicrab.modifyLumisPerJobAll(lambda nlumis: nlumis*0.5)
#multicrab.modifyNumberOfJobsAll(lambda njobs: njobs*2)

#multicrab.createTasks()
multicrab.createTasks(configOnly=True)
