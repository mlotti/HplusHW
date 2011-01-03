import multicrabDatasetsCommon as common

datasets = {
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
            "pattuple_v6": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHpmToTauNu_M-90_7TeV-pythia6-tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO_pattuple_v6_1-94799423eedb9d1f02c6c0ed06eb3738/USER",
                "number_of_jobs": 4
            },
            "pattuple_v7_test2": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHpmToTauNu_M-90_7TeV-pythia6-tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO_pattuple_v7_test2-fc14f3c26d9a8f9a0fd353fdbd35603a/USER",
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
            "pattuple_v6": {
                "dbs_url": common.pattuple_dbs,
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
            "pattuple_v6": {
                "dbs_url": common.pattuple_dbs,
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
            "pattuple_v6": {
                "dbs_url": common.pattuple_dbs,
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
            "pattuple_v6": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTbar_Htaunu_M160/local-Spring10_START3X_V26_S09_v1_GEN-SIM-RECO_pattuple_v6_1-d218fa5d37dadfdf66e47c6123dae86a/USER",
                "number_of_jobs": 1
            },
            "pattuple_v7_test2": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTbar_Htaunu_M160/local-Spring10_START3X_V26_S09_v1_GEN-SIM-RECO_pattuple_v7_test2-cebce8ef23a98681703cb28b83ff791d/USER",
                "number_of_jobs": 1
            }
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
            "pattuple_v6": {
                "dbs_url": common.pattuple_dbs,
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
            "pattuple_v6": {
                "dbs_url": common.pattuple_dbs,
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
            "pattuple_v6": {
                "dbs_url": common.pattuple_dbs,
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
            "pattuple_v6": {
                "dbs_url": common.pattuple_dbs,
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
            "pattuple_v6": {
                "dbs_url": common.pattuple_dbs,
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
            "pattuple_v6": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt-230to300_7TeV-pythia8/local-Summer10_START36_V10_S09_v2_GEN-SIM-RECO_pattuple_v6_1-2366fe480375ff6f751e0b7e8ec70b52/USER",
                "number_of_jobs": 2
            }
        },
    },
    "QCD_Pt300to380": {
        "dataVersion": "36X",
        "crossSection": 9.593e+02,
        "data": {
            "RECO": {
                "datasetpath": "/QCD_Pt-300to380_7TeV-pythia8/Summer10-START36_V10_S09-v1/GEN-SIM-RECO",
                "number_of_jobs": 40 # Adjusted for PATtuple file size
            },
        },
    },
    "QCD_Pt380to470": {
        "dataVersion": "36X",
        "crossSection": 2.434e+02,
        "data": {
            "RECO": {
                "datasetpath": "/QCD_Pt-380to470_7TeV-pythia8/Summer10-START36_V10_S09-v1/GEN-SIM-RECO",
                "number_of_jobs": 40 # Adjusted for PATtuple file size
            },
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
            "pattuple_v6": {
                "dbs_url": common.pattuple_dbs,
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
            "pattuple_v6": {
                "dbs_url": common.pattuple_dbs,
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
            "pattuple_v6": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WJets_7TeV-madgraph-tauola/local-Summer10_START36_V9_S09_v1_GEN-SIM-RECO_pattuple_v6_1-2366fe480375ff6f751e0b7e8ec70b52/USER",
                "number_of_jobs": 40
            }
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
