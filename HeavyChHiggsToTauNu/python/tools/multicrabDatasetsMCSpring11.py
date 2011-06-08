import multicrabDatasetsCommon as common

# Goal: ~3kev/job

# Default signal cross section taken the same as ttbar

datasets = {
    # Signal WH
    "TTToHplusBWB_M80_Spring11": {
        "dataVersion": "311Xredigi",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-80_7TeV-pythia6-tauola/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 45, # Adjusted for PATtuple file size
            },
            "pattuple_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-80_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v11b-8f83bb72c10133f1e52d950030b925c8/USER",
                "number_of_jobs": 1
            },
        }
    },
    "TTToHplusBWB_M90_Spring11": {
        "dataVersion": "311Xredigi",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-90_7TeV-pythia6-tauola/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 45, # Adjusted for PATtuple file size
            },
            "pattuple_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-90_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v11b-8f83bb72c10133f1e52d950030b925c8/USER",
                "number_of_jobs": 1
            },
        }
    },
    "TTToHplusBWB_M100_Spring11": {
        "dataVersion": "311Xredigi",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-100_7TeV-pythia6-tauola/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 45, # Adjusted for PATtuple file size
            },
            "pattuple_v10": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-100_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v10-7482fea56f5721e68c0db13cc3e1d0fc/USER",
                "number_of_jobs": 1
            },
            "pattuple_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-100_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v11b-8f83bb72c10133f1e52d950030b925c8/USER",
                "number_of_jobs": 1
            },
        }
    },
    "TTToHplusBWB_M120_Spring11": {
        "dataVersion": "311Xredigi",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 45, # Adjusted for PATtuple file size
            },
            "pattuple_v10": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-120_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v10-7482fea56f5721e68c0db13cc3e1d0fc/USER",
                "number_of_jobs": 1
            },
            "pattuple_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-120_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v11b-8f83bb72c10133f1e52d950030b925c8/USER",
                "number_of_jobs": 1
            },
        }
    },
    "TTToHplusBWB_M140_Spring11": {
        "dataVersion": "311Xredigi",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-140_7TeV-pythia6-tauola/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 45, # Adjusted for PATtuple file size
            },
            "pattuple_v10": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-140_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v10-7482fea56f5721e68c0db13cc3e1d0fc/USER",
                "number_of_jobs": 1
            },
            "pattuple_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-140_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v11b-8f83bb72c10133f1e52d950030b925c8/USER",
                "number_of_jobs": 1
            },
        }
    },
    "TTToHplusBWB_M150_Spring11": {
        "dataVersion": "311Xredigi",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-150_7TeV-pythia6-tauola/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 45, # Adjusted for PATtuple file size
            },
            "pattuple_v10": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-150_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v10-7482fea56f5721e68c0db13cc3e1d0fc/USER",
                "number_of_jobs": 1
            },
            "pattuple_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-150_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v11b-8f83bb72c10133f1e52d950030b925c8/USER",
                "number_of_jobs": 1
            },
        }
    },
    "TTToHplusBWB_M155_Spring11": {
        "dataVersion": "311Xredigi",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-155_7TeV-pythia6-tauola/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 45, # Adjusted for PATtuple file size
            },
            "pattuple_v10": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-155_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v10-7482fea56f5721e68c0db13cc3e1d0fc/USER",
                "number_of_jobs": 1
            },
            "pattuple_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-155_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v11b-8f83bb72c10133f1e52d950030b925c8/USER",
                "number_of_jobs": 1
            },
        }
    },
    "TTToHplusBWB_M160_Spring11": {
        "dataVersion": "311Xredigi",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-160_7TeV-pythia6-tauola/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 45, # Adjusted for PATtuple file size
            },
            "pattuple_v10": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-160_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v10-7482fea56f5721e68c0db13cc3e1d0fc/USER",
                "number_of_jobs": 1
            },
            "pattuple_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-160_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v11b-8f83bb72c10133f1e52d950030b925c8/USER",
                "number_of_jobs": 1
            },
        }
    },

    # Signal HH
    "TTToHplusBHminusB_M80_Spring11": {
        "dataVersion": "311Xredigi",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBHminusB_M-80_7TeV-pythia6-tauola/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 45, # Adjusted for PATtuple file size
            },
            "pattuple_v10": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBHminusB_M-80_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v10-7482fea56f5721e68c0db13cc3e1d0fc/USER",
                "number_of_jobs": 1
            },
            "pattuple_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBHminusB_M-80_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v11b-8f83bb72c10133f1e52d950030b925c8/USER",
                "number_of_jobs": 1
            },
        }
    },
    "TTToHplusBHminusB_M100_Spring11": {
        "dataVersion": "311Xredigi",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBHminusB_M-100_7TeV-pythia6-tauola/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 45, # Adjusted for PATtuple file size
            },
            "pattuple_v10": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBHminusB_M-100_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v10-7482fea56f5721e68c0db13cc3e1d0fc/USER",
                "number_of_jobs": 1
            },
            "pattuple_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBHminusB_M-100_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v11b-8f83bb72c10133f1e52d950030b925c8/USER",
                "number_of_jobs": 1
            },
        }
    },
    "TTToHplusBHminusB_M120_Spring11": {
        "dataVersion": "311Xredigi",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBHminusB_M-120_7TeV-pythia6-tauola/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 45, # Adjusted for PATtuple file size
            },
            "pattuple_v10": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBHminusB_M-120_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v10-7482fea56f5721e68c0db13cc3e1d0fc/USER",
                "number_of_jobs": 1
            },
            "pattuple_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBHminusB_M-120_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v11b-8f83bb72c10133f1e52d950030b925c8/USER",
                "number_of_jobs": 1
            },
        }
    },
    "TTToHplusBHminusB_M140_Spring11": {
        "dataVersion": "311Xredigi",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBHminusB_M-140_7TeV-pythia6-tauola/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 45, # Adjusted for PATtuple file size
            },
            "pattuple_v10": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBHminusB_M-140_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v10-7482fea56f5721e68c0db13cc3e1d0fc/USER",
                "number_of_jobs": 1
            },
            "pattuple_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBHminusB_M-140_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v11b-8f83bb72c10133f1e52d950030b925c8/USER",
                "number_of_jobs": 1
            },
        }
    },
    "TTToHplusBHminusB_M150_Spring11": {
        "dataVersion": "311Xredigi",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBHminusB_M-150_7TeV-pythia6-tauola/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 45, # Adjusted for PATtuple file size
            },
            "pattuple_v10": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBHminusB_M-150_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v10-7482fea56f5721e68c0db13cc3e1d0fc/USER",
                "number_of_jobs": 1
            },
            "pattuple_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBHminusB_M-150_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v11b-8f83bb72c10133f1e52d950030b925c8/USER",
                "number_of_jobs": 1
            },
        }
    },
    "TTToHplusBHminusB_M155_Spring11": {
        "dataVersion": "311Xredigi",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBHminusB_M-155_7TeV-pythia6-tauola/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 45, # Adjusted for PATtuple file size
            },
            "pattuple_v10": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBHminusB_M-155_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v10-7482fea56f5721e68c0db13cc3e1d0fc/USER",
                "number_of_jobs": 1
            },
            "pattuple_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBHminusB_M-155_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v11b-8f83bb72c10133f1e52d950030b925c8/USER",
                "number_of_jobs": 1
            },
        }
    },
    "TTToHplusBHminusB_M160_Spring11": {
        "dataVersion": "311Xredigi",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBHminusB_M-160_7TeV-pythia6-tauola/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 45, # Adjusted for PATtuple file size
            },
            "pattuple_v10": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBHminusB_M-160_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v10-7482fea56f5721e68c0db13cc3e1d0fc/USER",
                "number_of_jobs": 1
            },
            "pattuple_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBHminusB_M-160_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v11b-8f83bb72c10133f1e52d950030b925c8/USER",
                "number_of_jobs": 1
            },
        }
    },

    # QCD backgrounds
    # Cross sections are from https://twiki.cern.ch/twiki/bin/view/CMS/ReProcessingWinter2010
    "QCD_Pt0to5_TuneZ2_Spring11": {
        "dataVersion": "311Xredigi",
        "crossSection": 4.844e+10*0.983,
        "data": {
            "AOD": {
                "datasetpath": "/QCD_Pt_0to5_TuneZ2_7TeV_pythia6/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 30, # Adjusted for PATtuple file size
            },
        },
    },
    "QCD_Pt5to15_TuneZ2_Spring11": {
        "dataVersion": "311Xredigi",
        "crossSection": 3.675e+10,
        "data": {
            "AOD": {
                "datasetpath": "/QCD_Pt_5to15_TuneZ2_7TeV_pythia6/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 120, # Adjusted for PATtuple file size
            },
        },
    },
    "QCD_Pt15to30_TuneZ2_Spring11": {
        "dataVersion": "311Xredigi",
        "crossSection": 8.159e+08,
        "data": {
            "AOD": {
                "datasetpath": "/QCD_Pt_15to30_TuneZ2_7TeV_pythia6/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 480, # Adjusted for PATtuple file size
            },
        },
    },
    "QCD_Pt30to50_TuneZ2_Spring11": {
        "dataVersion": "311Xredigi",
        "crossSection": 5.312e+07,
        "data": {
            "AOD": {
                "datasetpath": "/QCD_Pt_30to50_TuneZ2_7TeV_pythia6/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 490, # Adjusted for PATtuple file size
            },
            "pattuple_v10": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt_30to50_TuneZ2_7TeV_pythia6/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v10-7482fea56f5721e68c0db13cc3e1d0fc/USER",
                "number_of_jobs": 16 # for 200 kev/job, ~60 min job
            },
            "pattuple_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt_30to50_TuneZ2_7TeV_pythia6/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v11b-8f83bb72c10133f1e52d950030b925c8/USER",
                "number_of_jobs": 16 # for 200 kev/job, ~60 min job
            },
        },
    },
    "QCD_Pt50to80_TuneZ2_Spring11": {
        "dataVersion":  "311Xredigi",
        "crossSection": 6.359e+06,
        "data": {
            "AOD": {
                "datasetpath": "/QCD_Pt_50to80_TuneZ2_7TeV_pythia6/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 490, # Adjusted for PATtuple file size
            },
            "pattuple_v10": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt_50to80_TuneZ2_7TeV_pythia6/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v10-7482fea56f5721e68c0db13cc3e1d0fc/USER",
                "number_of_jobs": 16 # for 200 kev/job, ~60 min job
            },
            "pattuple_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt_50to80_TuneZ2_7TeV_pythia6/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v11b-8f83bb72c10133f1e52d950030b925c8/USER",
                "number_of_jobs": 16 # for 200 kev/job, ~60 min job
            },
        },
    },
    "QCD_Pt80to120_TuneZ2_Spring11": {
        "dataVersion": "311Xredigi",
        "crossSection": 7.843e+05,
        "data": {
            "AOD": {
                "datasetpath": "/QCD_Pt_80to120_TuneZ2_7TeV_pythia6/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 490, # Adjusted for PATtuple file size
            },
            "pattuple_v10": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt_120to170_TuneZ2_7TeV_pythia6/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v10-7482fea56f5721e68c0db13cc3e1d0fc/USER",
                "number_of_jobs": 16 # for 200 kev/job, ~60 min job
            },
            "pattuple_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt_80to120_TuneZ2_7TeV_pythia6/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v11b-8f83bb72c10133f1e52d950030b925c8/USER",
                "number_of_jobs": 16 # for 200 kev/job, ~60 min job
            },
        },
    },
    "QCD_Pt120to170_TuneZ2_Spring11": {
        "dataVersion": "311Xredigi",
        "crossSection": 1.151e+05,
        "data": {
            "AOD": {
                "datasetpath": "/QCD_Pt_120to170_TuneZ2_7TeV_pythia6/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 490, # Adjusted for PATtuple file size
            },
            "pattuple_v10": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt_120to170_TuneZ2_7TeV_pythia6/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v10-7482fea56f5721e68c0db13cc3e1d0fc/USER",
                "number_of_jobs": 16 # for 200 kev/job, ~60 min job
            },
            "pattuple_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt_120to170_TuneZ2_7TeV_pythia6/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v11b-8f83bb72c10133f1e52d950030b925c8/USER",
                "number_of_jobs": 16 # for 200 kev/job, ~60 min job
            },
        },
    },
    "QCD_Pt170to300_TuneZ2_Spring11": {
        "dataVersion": "311Xredigi",
        "crossSection": 2.426e+04,
        "data": {
            "AOD": {
                "datasetpath": "/QCD_Pt_170to300_TuneZ2_7TeV_pythia6/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 490, # Adjusted for PATtuple file size
            },
            "pattuple_v10": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt_170to300_TuneZ2_7TeV_pythia6/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v10-7482fea56f5721e68c0db13cc3e1d0fc/USER",
                "number_of_jobs": 16 # for 200 kev/job, ~60 min job
            },
            "pattuple_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt_170to300_TuneZ2_7TeV_pythia6/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v11b-8f83bb72c10133f1e52d950030b925c8/USER",
                "number_of_jobs": 16 # for 200 kev/job, ~60 min job
            },
        },
    },
    "QCD_Pt300to470_TuneZ2_Spring11": {
        "dataVersion": "311Xredigi",
        "crossSection": 1.168e+03,
        "data": {
            "AOD": {
                "datasetpath": "/QCD_Pt_300to470_TuneZ2_7TeV_pythia6/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 490 # Adjusted for PATtuple file size
            },
            "pattuple_v10": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt_300to470_TuneZ2_7TeV_pythia6/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v10-7482fea56f5721e68c0db13cc3e1d0fc/USER",
                "number_of_jobs": 16 # for 200 kev/job, ~60 min job
            },
            "pattuple_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt_300to470_TuneZ2_7TeV_pythia6/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v11b-8f83bb72c10133f1e52d950030b925c8/USER",
                "number_of_jobs": 16 # for 200 kev/job, ~60 min job
            },
        },
    },
    

    # EWK MadGraph
    # Cross sections are from https://twiki.cern.ch/twiki/bin/view/CMS/CrossSections_3XSeries
    "TTJets_TuneZ2_Spring11": {
        "dataVersion": "311Xredigi",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTJets_TuneZ2_7TeV-madgraph-tauola/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 450, # Adjusted for PATtuple file size
            },
            "pattuple_v10_test1": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTJets_TuneZ2_7TeV-madgraph-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v10_test1-fc6810ccf564527d387a28a4affcd399/USER",
                "number_of_jobs": 12 # for 100 kev/job, ~30 min job
            },
            "pattuple_v10_test3": {
                "fallback": "pattuple_v10_test1"
            },
            "pattuple_v10": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTJets_TuneZ2_7TeV-madgraph-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v10-7482fea56f5721e68c0db13cc3e1d0fc/USER",
                "number_of_jobs": 6
            },
            "pattuple_v11_test1": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTJets_TuneZ2_7TeV-madgraph-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v11_test1-03dcbf3e1b24d51e48cedb4e0e7cb67e/USER",
                "number_of_jobs": 1
            },
            "pattuple_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTJets_TuneZ2_7TeV-madgraph-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v11b-8f83bb72c10133f1e52d950030b925c8/USER",
                "number_of_jobs": 6
            },
        },
    }, 
    "WJets_TuneZ2_Spring11": {
        "dataVersion": "311Xredigi",
        "crossSection": 28000,
        "data": {
            "AOD": {
                "datasetpath": "/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 2000, # Adjusted for PATtuple file
                                        # size. CRAB doesn't really
                                        # create this many jobs, but
                                        # the large number seems to be
                                        # needed to get enough jobs
                "use_server": 1,
            },
            "pattuple_v10": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v10-7482fea56f5721e68c0db13cc3e1d0fc/USER",
                "number_of_jobs": 50 # 12 M, 1634/2002
            },
            "pattuple_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v11b-8f83bb72c10133f1e52d950030b925c8/USER",
                "number_of_jobs": 60
            },
        },
    },
    "TToBLNu_s-channel_TuneZ2_Spring11": {
        "dataVersion": "311Xredigi",
        "crossSection": 4.6*0.32442,
        "data": {
            "AOD": {
                "datasetpath": "/TToBLNu_TuneZ2_s-channel_7TeV-madgraph/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 150, # Adjusted for PATtuple file size
            },
            "pattuple_v10": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TToBLNu_TuneZ2_s-channel_7TeV-madgraph/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v10-7482fea56f5721e68c0db13cc3e1d0fc/USER",
                "number_of_jobs": 2
            },
            "pattuple_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TToBLNu_TuneZ2_s-channel_7TeV-madgraph/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v11b-8f83bb72c10133f1e52d950030b925c8/USER",
                "number_of_jobs": 2
            },
        },
    },
    "TToBLNu_t-channel_TuneZ2_Spring11": {
        "dataVersion": "311Xredigi",
        "crossSection": 63*0.32442,
        "data": {
            "AOD": {
                "datasetpath": "/TToBLNu_TuneZ2_t-channel_7TeV-madgraph/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 150, # Adjusted for PATtuple file size
            },
            "pattuple_v10": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TToBLNu_TuneZ2_t-channel_7TeV-madgraph/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v10-7482fea56f5721e68c0db13cc3e1d0fc/USER",
                "number_of_jobs": 2
            },
            "pattuple_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TToBLNu_TuneZ2_t-channel_7TeV-madgraph/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v11b-8f83bb72c10133f1e52d950030b925c8/USER",
                "number_of_jobs": 2
            },
        },
    },
    "TToBLNu_tW-channel_TuneZ2_Spring11": {
        "dataVersion": "311Xredigi",
        "crossSection": 10.6,
        "data": {
            "AOD": {
                "datasetpath": "/TToBLNu_TuneZ2_tW-channel_7TeV-madgraph/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 150, # Adjusted for PATtuple file size
            },
            "pattuple_v10": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TToBLNu_TuneZ2_tW-channel_7TeV-madgraph/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v10-7482fea56f5721e68c0db13cc3e1d0fc/USER",
                "number_of_jobs": 2
            },
            "pattuple_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TToBLNu_TuneZ2_tW-channel_7TeV-madgraph/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v11b-8f83bb72c10133f1e52d950030b925c8/USER",
                "number_of_jobs": 2
            },
        },
    },
    "DYJetsToLL_M50_TuneZ2_Spring11": { # Z+jets
        "dataVersion": "311Xredigi",
        "crossSection": 2800,
        "data": {
            "AOD": {
                "datasetpath": "/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 490, # Adjusted for PATtuple file size
            },
            "pattuple_v10": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v10-7482fea56f5721e68c0db13cc3e1d0fc/USER",
                "number_of_jobs": 10
            },
            "pattuple_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v11b-8f83bb72c10133f1e52d950030b925c8/USER",
                "number_of_jobs": 10
            },
        }
    },

    # Diboson pythia
    # Cross sections are from https://twiki.cern.ch/twiki/bin/view/CMS/CrossSections_3XSeries
    "WW_TuneZ2_Spring11": {
        "dataVersion": "311Xredigi",
        "crossSection": 43,
        "data": {
            "AOD": {
                "datasetpath": "/WWtoAnything_TuneZ2_7TeV-pythia6-tauola/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 490, # Adjusted for PATtuple file size
            },
            "pattuple_v10": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WWtoAnything_TuneZ2_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v10-7482fea56f5721e68c0db13cc3e1d0fc/USER",
                "number_of_jobs": 11 # for 200 kev/job, ~60 min job
            },
            "pattuple_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WWtoAnything_TuneZ2_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v11b-8f83bb72c10133f1e52d950030b925c8/USER",
                "number_of_jobs": 11 # for 200 kev/job, ~60 min job
            },
        },
    },
    "WZ_TuneZ2_Spring11": {
        "dataVersion": "311Xredigi",
        "crossSection": 18,
        "data": {
            "AOD": {
                "datasetpath": "/WZtoAnything_TuneZ2_7TeV-pythia6-tauola/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 490, # Adjusted for PATtuple file size
            },
            "pattuple_v10": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WZtoAnything_TuneZ2_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v10-7482fea56f5721e68c0db13cc3e1d0fc/USER",
                "number_of_jobs": 11 # for 200 kev/job, ~60 min job
            },
            "pattuple_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WZtoAnything_TuneZ2_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v11b-8f83bb72c10133f1e52d950030b925c8/USER",
                "number_of_jobs": 11 # for 200 kev/job, ~60 min job
            },
        },
    },
    "ZZ_TuneZ2_Spring11": {
        "dataVersion": "311Xredigi",
        "crossSection": 5.9,
        "data": {
            "AOD": {
                "datasetpath": "/ZZtoAnything_TuneZ2_7TeV-pythia6-tauola/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 490, # Adjusted for PATtuple file size
            },
            "pattuple_v10": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/ZZtoAnything_TuneZ2_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v10-7482fea56f5721e68c0db13cc3e1d0fc/USER",
                "number_of_jobs": 11 # for 200 kev/job, ~60 min job
            },
            "pattuple_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/ZZtoAnything_TuneZ2_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v11b-8f83bb72c10133f1e52d950030b925c8/USER",
                "number_of_jobs": 11 # for 200 kev/job, ~60 min job
            },
        },
    },

    # Backgrounds for electroweak background measurement
    # Cross section is from https://twiki.cern.ch/twiki/bin/view/CMS/ReProcessingWinter2010
    "QCD_Pt20_MuEnriched_TuneZ2_Spring11": {
        "dataVersion": "311Xredigi",
        "crossSection": 296600000.*0.0002855,
        "data": {
            "AOD": {
                "datasetpath": "/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 200,  # Adjusted for PAT on the fly
            }
        },
    },
}
