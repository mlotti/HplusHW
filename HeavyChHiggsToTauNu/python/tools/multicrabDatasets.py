pattuple_dbs = "http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_01/servlet/DBSServlet"

datasets = {
    ############################################################
    # Collision data
    #
    # BTau PD (for signal analysis)
    "BTau_141950-144114": {
        "dataVersion": "38XdataRun2010A",
        "trigger": "HLT_SingleIsoTau20_Trk5",
        "data": {
            "RECO": {
                "datasetpath": "/BTau/Run2010A-Sep17ReReco_v2/RECO",
                #"datasetpath": "/BTau/Run2010A-Nov4ReReco_v1/RECO",
                "luminosity": 0,
                "lumis_per_job": 100, # Adjusted for PATtuple file size
                "lumiMaskRequired": True
            },
            "AOD": {
                "fallback": "RECO",
                #"datasetpath": "/BTau/Run2010A-Nov4ReReco_v1/AOD",
            },
            "pattuple_v3": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/BTau/local-Run2010A_Sep17ReReco_v2_RECO-pattuple_v3_3-1a3cae4f0de91fe807e595c3536a6777/USER",
                "luminosity": 1.951264571,
                "number_of_jobs": 5
            },
            "pattuple_v6": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/BTau/local-Run2010A_Sep17ReReco_v2_RECO_pattuple_v6_1-b9b1bac3463fc5700035eeb83da514a6/USER",
                "luminosity": 2.139732871,
                "number_of_jobs": 5
            }
        }

    },
    "BTau_146240-147454": {
        "dataVersion": "38XdataRun2010B",
        "trigger": "HLT_SingleIsoTau20_Trk15_MET20",
        "runs": (146240, 147454),
        "data": {
            "pattuple_v3": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/BTau/local-Run2010B_PromptReco_V2_RECO-pattuple_v3_3-ca0cc7472f6f10c326285176dfa5387f/USER",
                "luminosity": 7.390799812,
                "number_of_jobs": 5
            }
        },
    },
    "BTau_146240-148107": {
        "dataVersion": "38XdataRun2010B",
        "trigger": "HLT_SingleIsoTau20_Trk15_MET20",
        "runs": (146240, 148107),
        "data": {
            "RECO": {
                "datasetpath": "/BTau/Run2010B-PromptReco-v2/RECO",
                "luminosity": 0,
                "lumis_per_job": 100, # Adjusted for PATtuple file size
                "lumiMaskRequired": True
            },
            "AOD": {
                "fallback": "RECO",
            },
            "pattuple_v6": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/BTau/local-Run2010B_PromptReco_v2_RECO_pattuple_v6_1-43c3132ebadd44967499e6cca288e3ab/USER",
                "luminosity": 5.899172590,
                "number_of_jobs": 10
            }
        },
    },
    "BTau_148108-148864": {
        "dataVersion": "38XdataRun2010B",
        "trigger": "HLT_SingleIsoTau20_Trk15_MET25_v3",
        "runs": (148108, 148864),
        "data": {
            "pattuple_v6": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/BTau/local-Run2010B_PromptReco_v2_RECO_pattuple_v6_1-87e2c0e398f5cb72e5974e2df0c2a6a6/USER",
                "luminosity": 4.600225784,
                "number_of_jobs": 3
            }
        },
    },
    "BTau_148108-149182": {
        "dataVersion": "38XdataRun2010B",
        "trigger": "HLT_SingleIsoTau20_Trk15_MET25_v3",
        "runs": (148108, 149182),
        "data": {
            "RECO": {
                "datasetpath": "/BTau/Run2010B-PromptReco-v2/RECO",
                "luminosity": 0,
                "lumis_per_job": 30, # Adjusted for PATtuple file size
                "lumiMaskRequired": True
            },
            "AOD": {
                "fallback": "RECO",
            }
        },
    },
    "BTau_149291-149442": {
        "dataVersion": "38XdataRun2010B",
        "trigger": "HLT_SingleIsoTau20_Trk15_MET25_v4",
        "runs": (149291, 149442),
        "data": {
            "RECO": {
                "datasetpath": "/BTau/Run2010B-PromptReco-v2/RECO",
                "luminosity": 0,
                "lumis_per_job": 30, # Adjusted for PATtuple file size
                "lumiMaskRequired": True
            },
            "AOD": {
                "fallback": "RECO",
            }
        },
    },
    # Mu PD (for electroweak background analysis)
    "Mu_135821-144114": {
        "dataVersion": "38XdataRun2010A",
        "trigger": "HLT_Mu9",
        "data": {
            "RECO": {
                "datasetpath": "/Mu/Run2010A-Sep17ReReco_v2/RECO",
                "luminosity": 0,
                "lumis_per_job": 500, # Adjusted for PAT on the fly
                "lumiMaskRequired": True
            },
            "AOD": {
                "fallback": "RECO",
            }
        }
    },
    "Mu_146240-147116": {
        "dataVersion": "38XdataRun2010B",
        "trigger": "HLT_Mu9",
        "runs": (146240, 147116),
        "data": {
            "AOD": {
                "datasetpath": "/Mu/Run2010B-PromptReco-v2/AOD",
                "luminosity": 0,
                "lumis_per_job": 600, # Adjusted for PAT on the fly
                "lumiMaskRequired": True
            }
        }
    },
    "Mu_147196-149442": {
        "dataVersion": "38XdataRun2010B",
        "trigger": "HLT_Mu15_v1",
        "runs": (147196, 149442),
        "data": {
            "AOD": {
                "datasetpath": "/Mu/Run2010B-PromptReco-v2/AOD",
                "luminosity": 0,
                "lumis_per_job": 500, # Adjusted for PAT on the fly
                "lumiMaskRequired": True
            }
        }
    },
    ############################################################
    # Monte Carlo
    #
    # Signal MC
    "TTToHpmToTauNu_M90": {
        "dataVersion": "35X",
        "crossSection": 16.442915,
        "data": {
            "RECO": {
                "datasetpath": "/TTToHpmToTauNu_M-90_7TeV-pythia6-tauola/Spring10-START3X_V26-v1/GEN-SIM-RECO",
                "number_of_jobs": 40 # Adjusted for PATtuple file size
            },
            "AOD": {
                "fallback": "RECO",
            },
            "pattuple_v3": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/TTToHpmToTauNu_M-90_7TeV-pythia6-tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3-1c883eb3798701ca362caa0e5457977b/USER",
                "number_of_jobs": 4
            },
            "pattuple_v6": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/TTToHpmToTauNu_M-90_7TeV-pythia6-tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO_pattuple_v6_1-94799423eedb9d1f02c6c0ed06eb3738/USER",
                "number_of_jobs": 4
            }
        }
    },
    "TTToHpmToTauNu_M100": {
        "dataVersion": "35X",
        "crossSection": 14.057857,
        "data": {
            "RECO": {
                "datasetpath": "/TTToHpmToTauNu_M-100_7TeV-pythia6-tauola/Spring10-START3X_V26-v1/GEN-SIM-RECO",
                "number_of_jobs": 4, # Adjusted for PATtuple file size
            },
            "AOD": {
                "fallback": "RECO",
            },
            "pattuple_v3": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/TTToHpmToTauNu_M-100_7TeV-pythia6-tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3-1c883eb3798701ca362caa0e5457977b/USER",
                "number_of_jobs": 1
            },
            "pattuple_v6": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/TTToHpmToTauNu_M-100_7TeV-pythia6-tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO_pattuple_v6_1-94799423eedb9d1f02c6c0ed06eb3738/USER",
                "number_of_jobs": 1
            }
        }
    },
    "TTToHpmToTauNu_M120": {
        "dataVersion": "35X",
        "crossSection": 8.984715,
        "data": {
            "RECO": {
                "datasetpath": "/TTToHpmToTauNu_M-120_7TeV-pythia6-tauola/Spring10-START3X_V26-v1/GEN-SIM-RECO",
                "number_of_jobs": 4, # Adjusted for PATtuple file size
            },
            "AOD": {
                "fallback": "RECO",
            },
            "pattuple_v3": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/TTToHpmToTauNu_M-120_7TeV-pythia6-tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3-1c883eb3798701ca362caa0e5457977b/USER",
                "number_of_jobs": 1
            },
            "pattuple_v6": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/TTToHpmToTauNu_M-120_7TeV-pythia6-tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO_pattuple_v6_1-94799423eedb9d1f02c6c0ed06eb3738/USER",
                "number_of_jobs": 1
            }
        }
    },
    "TTbar_Htaunu_M140": {
        "dataVersion": "35Xredigi",
        "crossSection": 4.223402,
        "data": {
            "RECO": {
                "datasetpath": "/TTbar_Htaunu_M140/Spring10-START3X_V26_S09-v1/GEN-SIM-RECO",
                "number_of_jobs": 4, # Adjusted for PATtuple file size
            },
            "AOD": {
                "fallback": "RECO",
            },
            "pattuple_v3": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/TTbar_Htaunu_M140/local-Spring10_START3X_V26_S09_v1_GEN-SIM-RECO-pattuple_v3-302407b8f1cbc62b8079a153c5ccc8bf/USER",
                "number_of_jobs": 1
            },
            "pattuple_v6": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/TTbar_Htaunu_M140/local-Spring10_START3X_V26_S09_v1_GEN-SIM-RECO_pattuple_v6_1-d218fa5d37dadfdf66e47c6123dae86a/USER",
                "number_of_jobs": 1
            }
        }
    },
    "TTbar_Htaunu_M160": {
        "dataVersion": "35Xredigi",
        "crossSection": 0.811493,
        "data": {
            "RECO": {
                "datasetpath": "/TTbar_Htaunu_M160/Spring10-START3X_V26_S09-v1/GEN-SIM-RECO",
                "number_of_jobs": 4, # Adjusted for PATtuple file size
            },
            "AOD": {
                "fallback": "RECO",
            },
            "pattuple_v3": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/TTbar_Htaunu_M160/local-Spring10_START3X_V26_S09_v1_GEN-SIM-RECO-pattuple_v3-302407b8f1cbc62b8079a153c5ccc8bf/USER",
                "number_of_jobs": 1
            },
            "pattuple_v6": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/TTbar_Htaunu_M160/local-Spring10_START3X_V26_S09_v1_GEN-SIM-RECO_pattuple_v6_1-d218fa5d37dadfdf66e47c6123dae86a/USER",
                "number_of_jobs": 1
            }
        }
    },
    # Fall 10
    "TTToHplusBWB_M90": {
        "dataVersion": "38Xrelval", # The trigger process was HLT, hence 38Xrelval is suitable here
        "crossSection": 16.442915,
        "data": {
            "RECO": {
                "datasetpath": "/TTToHplusBWB_M-90_7TeV-pythia6-tauola/Fall10-START38_V12-v1/GEN-SIM-RECO",
                "number_of_jobs": 20, # Adjusted for PATtuple file size
            },
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-90_7TeV-pythia6-tauola/Fall10-START38_V12-v1/AODSIM",
                "number_of_jobs": 20,
            },
            "pattuple_v6": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-90_7TeV-pythia6-tauola/local-Fall10_START38_V12_v1_GEN-SIM-RECO_pattuple_v6_1b-78d4b6b79bb86567b5da3e176aad4eb3/USER",
                "number_of_jobs": 1
            },
        }
    },
    "TTToHplusBWB_M100": {
        "dataVersion": "38Xrelval",
        "crossSection": 14.057857,
        "data": {
            "RECO": {
                "datasetpath": "/TTToHplusBWB_M-100_7TeV-pythia6-tauola/Fall10-START38_V12-v1/GEN-SIM-RECO",
                "number_of_jobs": 20, # Adjusted for PATtuple file size
            },
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-100_7TeV-pythia6-tauola/Fall10-START38_V12-v1/AODSIM",
                "number_of_jobs": 20,
            },
            "pattuple_v6": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-100_7TeV-pythia6-tauola/local-Fall10_START38_V12_v1_GEN-SIM-RECO_pattuple_v6_1b-78d4b6b79bb86567b5da3e176aad4eb3/USER",
                "number_of_jobs": 1
            },
        }
    },
    "TTToHplusBWB_M120": {
        "dataVersion": "38Xrelval",
        "crossSection": 8.984715,
        "data": {
            "RECO": {
                "datasetpath": "/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall10-START38_V12-v1/GEN-SIM-RECO",
                "number_of_jobs": 20, # Adjusted for PATtuple file size
            },
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall10-START38_V12-v1/AODSIM",
                "number_of_jobs": 20,
            },
            "pattuple_v6": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-120_7TeV-pythia6-tauola/local-Fall10_START38_V12_v1_GEN-SIM-RECO_pattuple_v6_1b-78d4b6b79bb86567b5da3e176aad4eb3/USER",
                "number_of_jobs": 1
            },
        }
    },
    "TTToHplusBWB_M140": {
        "dataVersion": "38Xrelval",
        "crossSection": 4.223402,
        "data": {
            "RECO": {
                "datasetpath": "/TTToHplusBWB_M-140_7TeV-pythia6-tauola/Fall10-START38_V12-v1/GEN-SIM-RECO",
                "number_of_jobs": 20, # Adjusted for PATtuple file size
            },
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-140_7TeV-pythia6-tauola/Fall10-START38_V12-v1/AODSIM",
                "number_of_jobs": 20,
            },
            "pattuple_v6": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-140_7TeV-pythia6-tauola/local-Fall10_START38_V12_v1_GEN-SIM-RECO_pattuple_v6_1b-78d4b6b79bb86567b5da3e176aad4eb3/USER",
                "number_of_jobs": 1
            },
        }
    },
    "TTToHplusBWB_M160": {
        "dataVersion": "38Xrelval",
        "crossSection": 0.811493,
        "data": {
            "RECO": {
                "datasetpath": "/TTToHplusBWB_M-160_7TeV-pythia6-tauola/Fall10-START38_V12-v1/GEN-SIM-RECO",
                "number_of_jobs": 20, # Adjusted for PATtuple file size
            },
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-160_7TeV-pythia6-tauola/Fall10-START38_V12-v1/AODSIM",
                "number_of_jobs": 20,
            },
            "pattuple_v6": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-160_7TeV-pythia6-tauola/local-Fall10_START38_V12_v1_GEN-SIM-RECO_pattuple_v6_1b-78d4b6b79bb86567b5da3e176aad4eb3/USER",
                "number_of_jobs": 1
            },
        }
    },
    # Background MC

    # QCD Summer10
    "QCD_Pt30to50": {
        "dataVersion": "36X",
        "crossSection": 5.018e+07,
        "data": {
            "RECO": {
                "datasetpath": "/QCD_Pt-30to50_7TeV-pythia8/Summer10-START36_V10_S09-v2/GEN-SIM-RECO",
                "number_of_jobs": 60 # Adjusted for PATtuple file size
            },
            "AOD": {
                "datasetpath": "/QCD_Pt-30to50_7TeV-pythia8/Summer10-START36_V10_S09-v2/AODSIM",
                "number_of_jobs": 60,
                "se_white_list": ["T2_FI_HIP"]
            },
            "pattuple_v3": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/QCD_Pt-30to50_7TeV-pythia8/local-Summer10_START36_V10_S09_v2_AODSIM-pattuple_v3-350234694fe4ac3e4a7c59f3d58cf538/USER",
                "number_of_jobs": 3
            },
            "pattuple_v6": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/QCD_Pt-30to50_7TeV-pythia8/local-Summer10_START36_V10_S09_v2_GEN-SIM-RECO_pattuple_v6_1-2366fe480375ff6f751e0b7e8ec70b52/USER",
                "number_of_jobs": 3
            }
        },
    },
    "QCD_Pt50to80": {
        "dataVersion": "36X",
        "crossSection": 6.035e+06,
        "data": {
            "RECO": {
                "datasetpath": "/QCD_Pt-50to80_7TeV-pythia8/Summer10-START36_V10_S09-v1/GEN-SIM-RECO",
                "number_of_jobs": 60 # Adjusted for PATtuple file size
            },
            "AOD": {
                "datasetpath": "/QCD_Pt-50to80_7TeV-pythia8/Summer10-START36_V10_S09-v1/AODSIM",
                "number_of_jobs": 50,
                "se_white_list": ["T2_FI_HIP"]
            },
            "pattuple_v3": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/QCD_Pt-50to80_7TeV-pythia8/local-Summer10_START36_V10_S09_v1_AODSIM-pattuple_v3-350234694fe4ac3e4a7c59f3d58cf538/USER",
                "number_of_jobs": 2
            },
            "pattuple_v6": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/QCD_Pt-50to80_7TeV-pythia8/local-Summer10_START36_V10_S09_v1_GEN-SIM-RECO_pattuple_v6_1-2366fe480375ff6f751e0b7e8ec70b52/USER",
                "number_of_jobs": 2
            }
        },
    },
    "QCD_Pt80to120": {
        "dataVersion": "36X",
        "crossSection": 7.519e+05,
        "data": {
            "RECO": {
                "datasetpath": "/QCD_Pt-80to120_7TeV-pythia8/Summer10-START36_V10_S09-v1/GEN-SIM-RECO",
                "number_of_jobs": 60 # Adjusted for PATtuple file size
            },
            "AOD": {
                "datasetpath": "/QCD_Pt-80to120_7TeV-pythia8/Summer10-START36_V10_S09-v1/AODSIM",
                "number_of_jobs": 60,
                "se_white_list": ["T2_FI_HIP"]
            },
            "pattuple_v3": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/QCD_Pt-80to120_7TeV-pythia8/local-Summer10_START36_V10_S09_v1_AODSIM-pattuple_v3-350234694fe4ac3e4a7c59f3d58cf538/USER",
                "number_of_jobs": 3
            },
            "pattuple_v6": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/QCD_Pt-80to120_7TeV-pythia8/local-Summer10_START36_V10_S09_v1_GEN-SIM-RECO_pattuple_v6_1-2366fe480375ff6f751e0b7e8ec70b52/USER",
                "number_of_jobs": 3
            }
        },
    },
    "QCD_Pt120to170": {
        "dataVersion": "36X",
        "crossSection": 1.120e+05,
        "data": {
            "RECO": {
                "datasetpath": "/QCD_Pt-120to170_7TeV-pythia8/Summer10-START36_V10_S09-v1/GEN-SIM-RECO",
                "number_of_jobs": 60 # Adjusted for PATtuple file size
            },
            "AOD": {
                "datasetpath": "/QCD_Pt-120to170_7TeV-pythia8/Summer10-START36_V10_S09-v1/AODSIM",
                "number_of_jobs": 60,
                "se_white_list": ["T2_FI_HIP"]
            },
            "pattuple_v3": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/QCD_Pt-120to170_7TeV-pythia8/local-Summer10_START36_V10_S09_v1_AODSIM-pattuple_v3-350234694fe4ac3e4a7c59f3d58cf538/USER",
                "number_of_jobs": 2
            },
            "pattuple_v6": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/QCD_Pt-120to170_7TeV-pythia8/local-Summer10_START36_V10_S09_v1_GEN-SIM-RECO_pattuple_v6_1-2366fe480375ff6f751e0b7e8ec70b52/USER",
                "number_of_jobs": 2
            }
        },
    },
    "QCD_Pt170to230": {
        "dataVersion": "36X",
        "crossSection": 1.994e+04,
        "data": {
            "RECO": {
                "datasetpath": "/QCD_Pt-170to230_7TeV-pythia8/Summer10-START36_V10_S09-v2/GEN-SIM-RECO",
                "number_of_jobs": 60 # Adjusted for PATtuple file size
            },
            "AOD": {
                "datasetpath": "/QCD_Pt-170to230_7TeV-pythia8/Summer10-START36_V10_S09-v2/AODSIM",
                "number_of_jobs": 60,
                "se_white_list": ["T2_FI_HIP"]
            },
            "pattuple_v3": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/QCD_Pt-170to230_7TeV-pythia8/local-Summer10_START36_V10_S09_v2_AODSIM-pattuple_v3-350234694fe4ac3e4a7c59f3d58cf538/USER",
                "number_of_jobs": 2
            },
            "pattuple_v6": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/QCD_Pt-170to230_7TeV-pythia8/local-Summer10_START36_V10_S09_v2_GEN-SIM-RECO_pattuple_v6_1-2366fe480375ff6f751e0b7e8ec70b52/USER",
                "number_of_jobs": 2
            }
        },
    },
    "QCD_Pt230to300": {
        "dataVersion": "36X",
        "crossSection": 4.123e+03,
        "data": {
            "RECO": {
                "datasetpath": "/QCD_Pt-230to300_7TeV-pythia8/Summer10-START36_V10_S09-v2/GEN-SIM-RECO",
                "number_of_jobs": 70 # Adjusted for PATtuple file size
            },
            "AOD": {
                "datasetpath": "/QCD_Pt-230to300_7TeV-pythia8/Summer10-START36_V10_S09-v2/AODSIM",
                "number_of_jobs": 60,
                "se_white_list": ["T2_FI_HIP"]
            },
            "pattuple_v3": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/QCD_Pt-230to300_7TeV-pythia8/local-Summer10_START36_V10_S09_v2_AODSIM-pattuple_v3-350234694fe4ac3e4a7c59f3d58cf538/USER",
                "number_of_jobs": 2
            },
            "pattuple_v6": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/QCD_Pt-230to300_7TeV-pythia8/local-Summer10_START36_V10_S09_v2_GEN-SIM-RECO_pattuple_v6_1-2366fe480375ff6f751e0b7e8ec70b52/USER",
                "number_of_jobs": 2
            }
        },
    },

    # QCD Fall10
    "QCD_Pt30to50_Fall10": {
        "dataVersion": "38X",
        "crossSection": 5.312e+07,
        "data": {
            "RECO": {
                "datasetpath": "/QCD_Pt_30to50_TuneZ2_7TeV_pythia6/Fall10-START38_V12-v1/GEN-SIM-RECO",
                "number_of_jobs": 150 # Adjusted for PATtuple file size
            },
            "AOD": {
                "datasetpath": "/QCD_Pt_30to50_TuneZ2_7TeV_pythia6/Fall10-START38_V12-v1/AODSIM",
                "number_of_jobs": 100,
                "se_white_list": ["T2_FI_HIP"]
            },
            "pattuple_v3": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/QCD_Pt_30to50_TuneZ2_7TeV_pythia6/local-Fall10_START38_V12_v1_AODSIM-pattuple_v3-77a027b4f9e83a8f0edf7612e8721105/USER",
                "number_of_jobs": 10
            },
            "pattuple_v6": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/QCD_Pt_30to50_TuneZ2_7TeV_pythia6/local-Fall10_START38_V12_v1_GEN-SIM-RECO_pattuple_v6_1b-38ae4fe7f537aab1b1e19a9c13e79d63/USER",
                "number_of_jobs": 10
            }
        },
    },
    "QCD_Pt50to80_Fall10": {
        "dataVersion": "38X",
        "crossSection": 6.359e+06,
        "data": {
            "RECO": {
                "datasetpath": "/QCD_Pt_50to80_TuneZ2_7TeV_pythia6/Fall10-START38_V12-v1/GEN-SIM-RECO",
                "number_of_jobs": 150 # Adjusted for PATtuple file size
            },
            "AOD": {
                "datasetpath": "/QCD_Pt_50to80_TuneZ2_7TeV_pythia6/Fall10-START38_V12-v1/AODSIM",
                "number_of_jobs": 100,
                "se_white_list": ["T2_FI_HIP"]
            },
            "pattuple_v3": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/QCD_Pt_50to80_TuneZ2_7TeV_pythia6/local-Fall10_START38_V12_v1_AODSIM-pattuple_v3-77a027b4f9e83a8f0edf7612e8721105/USER",
                "number_of_jobs": 10
            },
            "pattuple_v6": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/QCD_Pt_50to80_TuneZ2_7TeV_pythia6/local-Fall10_START38_V12_v1_GEN-SIM-RECO_pattuple_v6_1b-38ae4fe7f537aab1b1e19a9c13e79d63/USER",
                "number_of_jobs": 10
            },
        },
    },
    "QCD_Pt80to120_Fall10": {
        "dataVersion": "38X",
        "crossSection": 7.843e+05,
        "data": {
            "RECO": {
                "datasetpath": "/QCD_Pt_80to120_TuneZ2_7TeV_pythia6/Fall10-START38_V12-v1/GEN-SIM-RECO",
                "number_of_jobs": 150 # Adjusted for PATtuple file size
            },
            "AOD": {
                "datasetpath": "/QCD_Pt_80to120_TuneZ2_7TeV_pythia6/Fall10-START38_V12-v1/AODSIM",
                "number_of_jobs": 150,
            },
            "pattuple_v3": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/QCD_Pt_80to120_TuneZ2_7TeV_pythia6/local-Fall10_START38_V12_v1_AODSIM-pattuple_v3-77a027b4f9e83a8f0edf7612e8721105/USER",
                "number_of_jobs": 10
            },
            "pattuple_v6": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/QCD_Pt_80to120_TuneZ2_7TeV_pythia6/local-Fall10_START38_V12_v1_GEN-SIM-RECO_pattuple_v6_1-38ae4fe7f537aab1b1e19a9c13e79d63/USER",
                "number_of_jobs": 10
            }
        },
    },
    "QCD_Pt120to170_Fall10": {
        "dataVersion": "38X",
        "crossSection": 1.151e+05,
        "data": {
            "RECO": {
                "datasetpath": "/QCD_Pt_120to170_TuneZ2_7TeV_pythia6/Fall10-START38_V12-v1/GEN-SIM-RECO",
                "number_of_jobs": 150 # Adjusted for PATtuple file size
            },
            "AOD": {
                "datasetpath": "/QCD_Pt_120to170_TuneZ2_7TeV_pythia6/Fall10-START38_V12-v1/AODSIM",
                "number_of_jobs": 100,
                "se_white_list": ["T2_FI_HIP"]
            },
            "pattuple_v3": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/QCD_Pt_120to170_TuneZ2_7TeV_pythia6/local-Fall10_START38_V12_v1_AODSIM-pattuple_v3-77a027b4f9e83a8f0edf7612e8721105/USER",
                "number_of_jobs": 10
            },
            "pattuple_v6": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/QCD_Pt_120to170_TuneZ2_7TeV_pythia6/local-Fall10_START38_V12_v1_GEN-SIM-RECO_pattuple_v6_1b-38ae4fe7f537aab1b1e19a9c13e79d63/USER",
                "number_of_jobs": 10
            }
        },
    },
    "QCD_Pt170to300_Fall10": {
        "dataVersion": "38X",
        "crossSection": 2.426e+04,
        "data": {
            "RECO": {
                "datasetpath": "/QCD_Pt_170to300_TuneZ2_7TeV_pythia6/Fall10-START38_V12-v1/GEN-SIM-RECO",
                "number_of_jobs": 150 # Adjusted for PATtuple file size
            },
            "AOD": {
                "datasetpath": "/QCD_Pt_170to300_TuneZ2_7TeV_pythia6/Fall10-START38_V12-v1/AODSIM",
                "number_of_jobs": 100,
                "se_white_list": ["T2_FI_HIP"]
            },
            "pattuple_v3": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/QCD_Pt_170to300_TuneZ2_7TeV_pythia6/local-Fall10_START38_V12_v1_AODSIM-pattuple_v3-77a027b4f9e83a8f0edf7612e8721105/USER",
                "number_of_jobs": 10
            },
            "pattuple_v6": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/QCD_Pt_170to300_TuneZ2_7TeV_pythia6/local-Fall10_START38_V12_v1_GEN-SIM-RECO_pattuple_v6_1b-38ae4fe7f537aab1b1e19a9c13e79d63/USER",
                "number_of_jobs": 10
            }
        },
    },

    # Electroweak (Summer10)
    "TTbar": {
        "dataVersion": "36X",
        "crossSection": 165,
        "data": {
            "RECO": {
                "datasetpath": "/TTbar/Summer10-START36_V9_S09-v1/GEN-SIM-RECO",
                "number_of_jobs": 50 # Adjusted for PATtuple file size
            },
            "AOD": {
                "datasetpath": "/TTbar/Summer10-START36_V9_S09-v1/AODSIM",
                "number_of_jobs": 50,
            },
            "pattuple_v3": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/TTbar/local-Summer10_START36_V9_S09_v1_AODSIM-pattuple_v3-350234694fe4ac3e4a7c59f3d58cf538/USER",
                "number_of_jobs": 3
            },
            "pattuple_v6": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/TTbar/local-Summer10_START36_V9_S09_v1_GEN-SIM-RECO_pattuple_v6_1b-2366fe480375ff6f751e0b7e8ec70b52/USER",
                "number_of_jobs": 3
            }
        },
    },
    "TTbarJets": {
        "dataVersion": "36X",
        "crossSection": 165,
        "data": {
            "RECO": {
                "datasetpath": "/TTbarJets_Tauola-madgraph/Summer10-START36_V9_S09-v1/GEN-SIM-RECO",
                "number_of_jobs": 120 # Adjusted for PATtuple file size
            },
            "AOD": {
                "datasetpath": "/TTbarJets_Tauola-madgraph/Summer10-START36_V9_S09-v1/AODSIM",
                "number_of_jobs": 60,
                "se_white_list": ["T2_FI_HIP"]
            },
            "pattuple_v3": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/TTbarJets_Tauola-madgraph/local-Summer10_START36_V9_S09_v1_AODSIM-pattuple_v3-350234694fe4ac3e4a7c59f3d58cf538/USER",
                "number_of_jobs": 6
            },
            "pattuple_v6": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/TTbarJets_Tauola-madgraph/local-Summer10_START36_V9_S09_v1_GEN-SIM-RECO_pattuple_v6_1-2366fe480375ff6f751e0b7e8ec70b52/USER",
                "number_of_jobs": 6
            }
        },
    },
    "WJets": {
        "dataVersion": "36X",
        "crossSection": 25090,
        "data": {
            "RECO": {
                "datasetpath": "/WJets_7TeV-madgraph-tauola/Summer10-START36_V9_S09-v1/GEN-SIM-RECO",
                "number_of_jobs": 490 # Adjusted for PATtuple file size
            },
            "AOD": {
                "datasetpath": "/WJets_7TeV-madgraph-tauola/Summer10-START36_V9_S09-v1/AODSIM",
                "number_of_jobs": 350,
                "se_white_list": ["T2_FI_HIP"]
            },
            "pattuple_v3": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/WJets_7TeV-madgraph-tauola/local-Summer10_START36_V9_S09_v1_AODSIM-pattuple_v3-350234694fe4ac3e4a7c59f3d58cf538/USER",
                "number_of_jobs": 40
            },
            "pattuple_v6": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/WJets_7TeV-madgraph-tauola/local-Summer10_START36_V9_S09_v1_GEN-SIM-RECO_pattuple_v6_1-2366fe480375ff6f751e0b7e8ec70b52/USER",
                "number_of_jobs": 40
            },
            "tauembedding_skim_v1": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/WJets_7TeV-madgraph-tauola/local-Summer10_START36_V9_S09_v1_AODSIM_tauembedding_skim_v1-99df8e9f20fb187ff5807dad98f3d61d/USER",
                "number_of_jobs": 10
            }
        },
    },

    # Electroweak (Fall10)
    "TT": {
        "dataVersion": "38Xrelval",
        "crossSection": 165,
        "data": {
            "RECO": {
                "datasetpath": "/TT_TuneZ2_7TeV-pythia6-tauola/Fall10-START38_V12-v1/GEN-SIM-RECO",
                "number_of_jobs": 100 # Adjusted for PATtuple file size
            },
            "AOD": {
                "datasetpath": "/TT_TuneZ2_7TeV-pythia6-tauola/Fall10-START38_V12-v1/AODSIM",
                "number_of_jobs": 100,
            }
        },
    },
    "TTJets": {
        "dataVersion": "38Xrelval",
        "crossSection": 165,
        "data": {
            "RECO": {
                "datasetpath": "/TTJets_TuneZ2_7TeV-madgraph-tauola/Fall10-START38_V12-v2/GEN-SIM-RECO",
                "number_of_jobs": 100 # Adjusted for PATtuple file size
            },
            "AOD": {
                "datasetpath": "/TTJets_TuneZ2_7TeV-madgraph-tauola/Fall10-START38_V12-v2/AODSIM",
                "number_of_jobs": 100,
            }
        },
    },


    # Backgrounds for electroweak background measurement (Fall10)
    "QCD_Pt20_MuEnriched": {
        "dataVersion": "38X",
        "crossSection": 296600000.,
        "data": {
            "RECO": {
                "datasetpath": "/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/Fall10-START38_V12-v1/GEN-SIM-RECO",
                "number_of_jobs": 100, # Adjusted for PAT on the fly
            },
            "AOD": {
                "datasetpath": "/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/Fall10-START38_V12-v1/AODSIM",
                "number_of_jobs": 100,
            }
        },
    },
    "DYJetsToLL": { # Z+jets
        "dataVersion": "38X",
        "crossSection": 2321,
        "data": {
            "RECO": {
                "datasetpath": "/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/Fall10-START38_V12-v2/GEN-SIM-RECO",
                "number_of_jobs": 15, # Adjusted for PAT on the fly
            },
            "AOD": {
                "datasetpath": "/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/Fall10-START38_V12-v2/AODSIM",
                "number_of_jobs": 15,
            }
        },
    },
    "TToBLNu_s-channel": {
        "dataVersion": "38Xrelval",
        "crossSection": 0.99,
        "data": {
            "AOD": {
                "datasetpath": "/TToBLNu_TuneZ2_s-channel_7TeV-madgraph/Fall10-START38_V12-v1/AODSIM",
                "number_of_jobs": 10, # Adjusted for PAT on the fly
            }
        },
    },
    "TToBLNu_t-channel": {
        "dataVersion": "38Xrelval",
        "crossSection": 63./3.,
        "data": {
            "AOD": {
                "datasetpath": "/TToBLNu_TuneZ2_t-channel_7TeV-madgraph/Fall10-START38_V12-v2/AODSIM",
                "number_of_jobs": 10, # Adjusted for PAT on the fly
            }
        },
    },
    "TToBLNu_tW-channel": {
        "dataVersion": "38Xrelval",
        "crossSection": 10.56,
        "data": {
            "RECO": {
                "datasetpath": "/TToBLNu_TuneZ2_tW-channel_7TeV-madgraph/Fall10-START38_V12-v2/GEN-SIM-RECO",
                "number_of_jobs": 10, # Adjusted for PAT on the fly
            },
            "AOD": {
                "fallback": "RECO",
            },
        },
    },


    # Backgrounds for electroweak background measurement (Summer10)
    "ZJets": {
        "dataVersion": "37X",
        "crossSection": 2400,
        "data": {
            "AOD": {
                "datasetpath": "/ZJets-madgraph/Summer10-START37_V5_S09-v1/AODSIM",
                "number_of_jobs": 15, # Adjusted for PAT on the fly
            }
        },
    },
    "SingleTop_sChannel": {
        "dataVersion": "37X",
        "crossSection": 0.99,
        "data": {
            "RECO": {
                "datasetpath": "/SingleTop_sChannel-madgraph/Summer10-START37_V5_S09-v1/GEN-SIM-RECO",
                "number_of_jobs": 10, # Adjusted for PAT on the fly
            },
            "AOD": {
                "fallback": "RECO"
            }
        },
    },
    "SingleTop_tChannel": {
        "dataVersion": "37X",
        "crossSection": 20.16,
        "data": {
            "RECO": {
                "datasetpath": "/SingleTop_tChannel-madgraph/Summer10-START37_V5_S09-v1/GEN-SIM-RECO",
                "number_of_jobs": 15, # Adjusted for PAT on the fly
            },
            "AOD": {
                "fallback": "RECO"
            }
        },
    },
    "SingleTop_tWChannel": {
        "dataVersion": "37X",
        "crossSection": 10.56,
        "data": {
            "RECO": {
                "datasetpath": "/SingleTop_tWChannel-madgraph/Summer10-START37_V5_S09-v1/GEN-SIM-RECO",
                "number_of_jobs": 10, # Adjusted for PAT on the fly
            },
            "AOD": {
                "fallback": "RECO"
            }
        },
    },
}
