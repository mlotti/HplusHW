import multicrabDatasetsCommon as common

def addPU(datasets, name, data):
    cfg = {}
    cfg.update(datasets[name])
    cfg["dataVersion"] = "38XredigiPU"
    cfg["data"] = data
    datasets[name+"_PU"] = cfg

def addTo(datasets):
    add = lambda x,y: addPU(datasets, x, y)

    # Signal
    add("TTToHplusBWB_M90", {
            "RECO": {
                "datasetpath": "/TTToHplusBWB_M-90_7TeV-pythia6-tauola/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/GEN-SIM-RECO",
                "number_of_jobs": 20, # Adjusted for PATtuple file size
            },
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-90_7TeV-pythia6-tauola/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/AODSIM",
                "number_of_jobs": 20,
            },
            })
    add("TTToHplusBWB_M100", {
            "RECO": {
                "datasetpath": "/TTToHplusBWB_M-100_7TeV-pythia6-tauola/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/GEN-SIM-RECO",
                "number_of_jobs": 20, # Adjusted for PATtuple file size
            },
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-100_7TeV-pythia6-tauola/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/AODSIM",
                "number_of_jobs": 20,
            },
            })
    add("TTToHplusBWB_M120", {
            "RECO": {
                "datasetpath": "/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/GEN-SIM-RECO",
                "number_of_jobs": 20, # Adjusted for PATtuple file size
            },
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/AODSIM",
                "number_of_jobs": 20,
            },
            })
    add("TTToHplusBWB_M140", {
            "RECO": {
                "datasetpath": "/TTToHplusBWB_M-140_7TeV-pythia6-tauola/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/GEN-sIM-RECO",
                "number_of_jobs": 20, # Adjusted for PATtuple file size
            },
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-140_7TeV-pythia6-tauola/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/AODSIM",
                "number_of_jobs": 20,
            },
            })
    add("TTToHplusBWB_M160", {
            "RECO": {
                "datasetpath": "/TTToHplusBWB_M-160_7TeV-pythia6-tauola/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/GEN-SIM-RECO",
                "number_of_jobs": 20, # Adjusted for PATtuple file size
            },
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-160_7TeV-pythia6-tauola/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/AODSIM",
                "number_of_jobs": 20,
            },
            })

    # QCD
    add("QCD_Pt30to50_Fall10", {
            "RECO": {
                "datasetpath": "/QCD_Pt_30to50_TuneZ2_7TeV_pythia6/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/GEN-SIM-RECO",
                "number_of_jobs": 150, # Adjusted for PATtuple file size
            },
            "AOD": {
                "datasetpath": "/QCD_Pt_30to50_TuneZ2_7TeV_pythia6/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/AODSIM",
                "number_of_jobs": 150,
            },
            })
    add("QCD_Pt50to80_Fall10", {
            "RECO": {
                "datasetpath": "/QCD_Pt_50to80_TuneZ2_7TeV_pythia6/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/GEN-SIM-RECO",
                "number_of_jobs": 150, # Adjusted for PATtuple file size
            },
            "AOD": {
                "datasetpath": "/QCD_Pt_50to80_TuneZ2_7TeV_pythia6/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/AODSIM",
                "number_of_jobs": 150,
            },
            })
    add("QCD_Pt80to120_Fall10", {
            "RECO": {
                "datasetpath": "/QCD_Pt_80to120_TuneZ2_7TeV_pythia6/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/GEN-SIM-RECO",
                "number_of_jobs": 150, # Adjusted for PATtuple file size
            },
            "AOD": {
                "datasetpath": "/QCD_Pt_80to120_TuneZ2_7TeV_pythia6/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/AODSIM",
                "number_of_jobs": 150,
            },
            })
    add("QCD_Pt120to170_Fall10", {
            "RECO": {
                "datasetpath": "/QCD_Pt_120to170_TuneZ2_7TeV_pythia6/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/GEN-SIM-RECO",
                "number_of_jobs": 150, # Adjusted for PATtuple file size
            },
            "AOD": {
                "datasetpath": "/QCD_Pt_120to170_TuneZ2_7TeV_pythia6/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/AODSIM",
                "number_of_jobs": 150,
            },
            })
    add("QCD_Pt170to300_Fall10", {
            "RECO": {
                "datasetpath": "/QCD_Pt_170to300_TuneZ2_7TeV_pythia6/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/GEN-SIM-RECO",
                "number_of_jobs": 150, # Adjusted for PATtuple file size
            },
            "AOD": {
                "datasetpath": "/QCD_Pt_170to300_TuneZ2_7TeV_pythia6/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/AODSIM",
                "number_of_jobs": 150,
            },
            })
    add("QCD_Pt300to470_Fall10", {
            "RECO": {
                "datasetpath": "/QCD_Pt_300to470_TuneZ2_7TeV_pythia6/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/GEN-SIM-RECO",
                "number_of_jobs": 150, # Adjusted for PATtuple file size
            },
            })


    # Electroweak
    add("TTJets", {
            "RECO": {
                "datasetpath": "/TTJets_TuneZ2_7TeV-madgraph-tauola/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/GEN-SIM-RECO",
                "number_of_jobs": 100, # Adjusted for PATtuple file size
            },
            "AOD": {
                "datasetpath": "/TTJets_TuneZ2_7TeV-madgraph-tauola/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/AODSIM",
                "number_of_jobs": 100,
            },
            })
    add("WJets_Fall10", {
            "RECO": {
                "datasetpath": "/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/AODSIM",
                "number_of_jobs": 1000, # Adjusted for PATtuple file size
                "use_server": 1,
            },
            "AOD": {
                "datasetpath": "/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/AODSIM",
                "number_of_jobs": 1000,
                "use_server": 1,
            },
            })


    # Backgrounds for electroweak background measurement
    add("QCD_Pt20_MuEnriched", {
            "RECO": {
                "datasetpath": "/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/GEN-SIM-RECO",
                "number_of_jobs": 200, # Adjusted for PAT on the fly
            },
            "AOD": {
                "datasetpath": "/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/AODSIM",
                "number_of_jobs": 200,
            },
            })
    add("DYJetsToLL", {
            "RECO": {
                "datasetpath": "/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/GEN-SIM-RECO",
                "number_of_jobs": 15, # Adjusted for PAT on the fly
            },
            "AOD": {
                "datasetpath": "/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/AODSIM",
                "number_of_jobs": 15,
            },
            })
    add("TToBLNu_s-channel", {
            "RECO": {
                "datasetpath": "/TToBLNu_TuneZ2_s-channel_7TeV-madgraph/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/GEN-SIM-RECO",
                "number_of_jobs": 10, # Adjusted for PAT on the fly
            },
            "AOD": {
                "datasetpath": "/TToBLNu_TuneZ2_s-channel_7TeV-madgraph/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/AODSIM",
                "number_of_jobs": 10,
            },
            })
    add("TToBLNu_t-channel", {
            "RECO": {
                "datasetpath": "/TToBLNu_TuneZ2_t-channel_7TeV-madgraph/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/GEN-SIM-RECO",
                "number_of_jobs": 10, # Adjusted for PAT on the fly
            },
            "AOD": {
                "datasetpath": "/TToBLNu_TuneZ2_t-channel_7TeV-madgraph/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/AODSIM",
                "number_of_jobs": 10,
            },
            })
    add("TToBLNu_tW-channel", {
            "RECO": {
                "datasetpath": "/TToBLNu_TuneZ2_tW-channel_7TeV-madgraph/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/GEN-SIM-RECO",
                "number_of_jobs": 10, # Adjusted for PAT on the fly
            },
            "AOD": {
                "datasetpath": "/TToBLNu_TuneZ2_tW-channel_7TeV-madgraph/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/AODSIM",
                "number_of_jobs": 10,
            },
            })

