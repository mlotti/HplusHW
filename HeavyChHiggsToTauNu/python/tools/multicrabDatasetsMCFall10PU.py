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
            "pattuple_v6_4": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-90_7TeV-pythia6-tauola/local-Fall10_E7TeV_ProbDist_2010Data_BX156_START38_V12_v1_GEN-SIM-RECO_pattuple_v6_4-ec569a29593f1a4b1391204dd7806a3f/USER",
                "number_of_jobs": 1
            },
            "pattuple_v6": {
                "fallback": "pattuple_v6_4"
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
            "pattuple_v6_4": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-100_7TeV-pythia6-tauola/local-Fall10_E7TeV_ProbDist_2010Data_BX156_START38_V12_v1_GEN-SIM-RECO_pattuple_v6_4-ec569a29593f1a4b1391204dd7806a3f/USER",
                "number_of_jobs": 1
            },
            "pattuple_v6": {
                "fallback": "pattuple_v6_4"
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
            "pattuple_v6_4": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-120_7TeV-pythia6-tauola/local-Fall10_E7TeV_ProbDist_2010Data_BX156_START38_V12_v1_GEN-SIM-RECO_pattuple_v6_4-ec569a29593f1a4b1391204dd7806a3f/USER",
                "number_of_jobs": 1
            },
            "pattuple_v6": {
                "fallback": "pattuple_v6_4"
            },
            })
    add("TTToHplusBWB_M140", {
            "RECO": {
                "datasetpath": "/TTToHplusBWB_M-140_7TeV-pythia6-tauola/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/GEN-SIM-RECO",
                "number_of_jobs": 20, # Adjusted for PATtuple file size
            },
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-140_7TeV-pythia6-tauola/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/AODSIM",
                "number_of_jobs": 20,
            },
            "pattuple_v6_4": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-140_7TeV-pythia6-tauola/local-Fall10_E7TeV_ProbDist_2010Data_BX156_START38_V12_v1_GEN-SIM-RECO_pattuple_v6_4-ec569a29593f1a4b1391204dd7806a3f/USER",
                "number_of_jobs": 1
            },
            "pattuple_v6": {
                "fallback": "pattuple_v6_4"
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
            "pattuple_v6_4": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-160_7TeV-pythia6-tauola/local-Fall10_E7TeV_ProbDist_2010Data_BX156_START38_V12_v1_GEN-SIM-RECO_pattuple_v6_4-ec569a29593f1a4b1391204dd7806a3f/USER",
                "number_of_jobs": 1
            },
            "pattuple_v6": {
                "fallback": "pattuple_v6_4"
            },
            })

    # QCD
    add("QCD_Pt30to50_Fall10", {
            "RECO": {
                "datasetpath": "/QCD_Pt_30to50_TuneZ2_7TeV_pythia6/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/GEN-SIM-RECO",
                "number_of_jobs": 450, # Adjusted for PATtuple file size
            },
            "AOD": {
                "datasetpath": "/QCD_Pt_30to50_TuneZ2_7TeV_pythia6/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/AODSIM",
                "number_of_jobs": 450,
            },
            "pattuple_v6_4": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt_30to50_TuneZ2_7TeV_pythia6/local-Fall10_E7TeV_ProbDist_2010Data_BX156_START38_V12_v1_GEN-SIM-RECO_pattuple_v6_4-ec569a29593f1a4b1391204dd7806a3f/USER",
                "number_of_jobs": 10,
            },
            "pattuple_v6": {
                "fallback": "pattuple_v6_4"
            },
            })
    add("QCD_Pt50to80_Fall10", {
            "RECO": {
                "datasetpath": "/QCD_Pt_50to80_TuneZ2_7TeV_pythia6/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/GEN-SIM-RECO",
                "number_of_jobs": 450, # Adjusted for PATtuple file size
            },
            "AOD": {
                "datasetpath": "/QCD_Pt_50to80_TuneZ2_7TeV_pythia6/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/AODSIM",
                "number_of_jobs": 450,
            },
            "pattuple_v6_4": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt_50to80_TuneZ2_7TeV_pythia6/local-Fall10_E7TeV_ProbDist_2010Data_BX156_START38_V12_v1_GEN-SIM-RECO_pattuple_v6_4-ec569a29593f1a4b1391204dd7806a3f/USER",
                "number_of_jobs": 10,
            },
            "pattuple_v6": {
                "fallback": "pattuple_v6_4"
            },
            })
    add("QCD_Pt80to120_Fall10", {
            "RECO": {
                "datasetpath": "/QCD_Pt_80to120_TuneZ2_7TeV_pythia6/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/GEN-SIM-RECO",
                "number_of_jobs": 450, # Adjusted for PATtuple file size
            },
            "AOD": {
                "datasetpath": "/QCD_Pt_80to120_TuneZ2_7TeV_pythia6/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/AODSIM",
                "number_of_jobs": 450,
            },
            "pattuple_v6_4": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt_80to120_TuneZ2_7TeV_pythia6/local-Fall10_E7TeV_ProbDist_2010Data_BX156_START38_V12_v1_GEN-SIM-RECO_pattuple_v6_4-ec569a29593f1a4b1391204dd7806a3f/USER",
                "number_of_jobs": 10,
            },
            "pattuple_v6": {
                "fallback": "pattuple_v6_4"
            },
            })
    add("QCD_Pt120to170_Fall10", {
            "RECO": {
                "datasetpath": "/QCD_Pt_120to170_TuneZ2_7TeV_pythia6/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/GEN-SIM-RECO",
                "number_of_jobs": 450, # Adjusted for PATtuple file size
            },
            "AOD": {
                "datasetpath": "/QCD_Pt_120to170_TuneZ2_7TeV_pythia6/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/AODSIM",
                "number_of_jobs": 450,
            },
            "pattuple_v6_4": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt_120to170_TuneZ2_7TeV_pythia6/local-Fall10_E7TeV_ProbDist_2010Data_BX156_START38_V12_v1_GEN-SIM-RECO_pattuple_v6_4-ec569a29593f1a4b1391204dd7806a3f/USER",
                "number_of_jobs": 10,
            },
            "pattuple_v6": {
                "fallback": "pattuple_v6_4"
            },
            })
    add("QCD_Pt170to300_Fall10", {
            "RECO": {
                "datasetpath": "/QCD_Pt_170to300_TuneZ2_7TeV_pythia6/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/GEN-SIM-RECO",
                "number_of_jobs": 450, # Adjusted for PATtuple file size
            },
            "AOD": {
                "datasetpath": "/QCD_Pt_170to300_TuneZ2_7TeV_pythia6/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/AODSIM",
                "number_of_jobs": 450,
            },
            "pattuple_v6_4": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt_170to300_TuneZ2_7TeV_pythia6/local-Fall10_E7TeV_ProbDist_2010Data_BX156_START38_V12_v1_GEN-SIM-RECO_pattuple_v6_4-ec569a29593f1a4b1391204dd7806a3f/USER",
                "number_of_jobs": 10,
            },
            "pattuple_v6": {
                "fallback": "pattuple_v6_4"
            },
            })


    # Electroweak
    add("TTJets", {
            "RECO": {
                "datasetpath": "/TTJets_TuneZ2_7TeV-madgraph-tauola/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/GEN-SIM-RECO",
                "number_of_jobs": 400, # Adjusted for PATtuple file size
            },
            "AOD": {
                "datasetpath": "/TTJets_TuneZ2_7TeV-madgraph-tauola/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/AODSIM",
                "number_of_jobs": 400,
            },
            "pattuple_v6_4": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTJets_TuneZ2_7TeV-madgraph-tauola/local-Fall10_E7TeV_ProbDist_2010Data_BX156_START38_V12_v1_GEN-SIM-RECO_pattuple_v6_4-ec569a29593f1a4b1391204dd7806a3f/USER",
                "number_of_jobs": 5,
            },
            "pattuple_v6": {
                "fallback": "pattuple_v6_4"
            },
            })
    add("WJets_Fall10", {
            "RECO": {
                "datasetpath": "/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/GEN-SIM-RECO",
                "number_of_jobs": 1500, # Adjusted for PATtuple file size
                "use_server": 1,
            },
            "AOD": {
                "datasetpath": "/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/Fall10-E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/AODSIM",
                "number_of_jobs": 1500,
                "use_server": 1,
            },
            "pattuple_v6_4": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/local-Fall10_E7TeV_ProbDist_2010Data_BX156_START38_V12_v1_GEN-SIM-RECO_pattuple_v6_4-ec569a29593f1a4b1391204dd7806a3f/USER",
                "number_of_jobs": 60,
            },
            "pattuple_v6": {
                "fallback": "pattuple_v6_4"
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

