import multicrabDatasetsCommon as common

datasets = {
    # Signal MC
    "TTToHpmToTauNu_M90": {
        "dataVersion": "35X",
        "crossSection": 16.442915,
        "data": {
            "RECO": {
                "datasetpath": "/TTToHpmToTauNu_M-90_7TeV-pythia6-tauola/Spring10-START3X_V26-v1/GEN-SIM-RECO",
                "number_of_jobs": 40
            },
            "AOD": {
                "fallback": "RECO",
            },
            "pattuple_v3": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHpmToTauNu_M-90_7TeV-pythia6-tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3-1c883eb3798701ca362caa0e5457977b/USER",
                "number_of_jobs": 4
            },
            "pattuple_v6": {
                "dbs_url": common.pattuple_dbs,
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
                "number_of_jobs": 4,
            },
            "AOD": {
                "fallback": "RECO",
            },
            "pattuple_v3": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHpmToTauNu_M-100_7TeV-pythia6-tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3-1c883eb3798701ca362caa0e5457977b/USER",
                "number_of_jobs": 1
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
                "number_of_jobs": 4,
            },
            "AOD": {
                "fallback": "RECO",
            },
            "pattuple_v3": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHpmToTauNu_M-120_7TeV-pythia6-tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3-1c883eb3798701ca362caa0e5457977b/USER",
                "number_of_jobs": 1
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
                "number_of_jobs": 4,
            },
            "AOD": {
                "fallback": "RECO",
            },
            "pattuple_v3": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTbar_Htaunu_M140/local-Spring10_START3X_V26_S09_v1_GEN-SIM-RECO-pattuple_v3-302407b8f1cbc62b8079a153c5ccc8bf/USER",
                "number_of_jobs": 1
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
                "number_of_jobs": 4,
            },
            "AOD": {
                "fallback": "RECO",
            },
            "pattuple_v3": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTbar_Htaunu_M160/local-Spring10_START3X_V26_S09_v1_GEN-SIM-RECO-pattuple_v3-302407b8f1cbc62b8079a153c5ccc8bf/USER",
                "number_of_jobs": 1
            },
            "pattuple_v6": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTbar_Htaunu_M160/local-Spring10_START3X_V26_S09_v1_GEN-SIM-RECO_pattuple_v6_1-d218fa5d37dadfdf66e47c6123dae86a/USER",
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
                "number_of_jobs": 60
            },
            "AOD": {
                "datasetpath": "/QCD_Pt-30to50_7TeV-pythia8/Summer10-START36_V10_S09-v2/AODSIM",
                "number_of_jobs": 60,
                "se_white_list": ["T2_FI_HIP"]
            },
            "pattuple_v3": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt-30to50_7TeV-pythia8/local-Summer10_START36_V10_S09_v2_AODSIM-pattuple_v3-350234694fe4ac3e4a7c59f3d58cf538/USER",
                "number_of_jobs": 3
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
                "number_of_jobs": 60
            },
            "AOD": {
                "datasetpath": "/QCD_Pt-50to80_7TeV-pythia8/Summer10-START36_V10_S09-v1/AODSIM",
                "number_of_jobs": 50,
                "se_white_list": ["T2_FI_HIP"]
            },
            "pattuple_v3": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt-50to80_7TeV-pythia8/local-Summer10_START36_V10_S09_v1_AODSIM-pattuple_v3-350234694fe4ac3e4a7c59f3d58cf538/USER",
                "number_of_jobs": 2
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
                "number_of_jobs": 60
            },
            "AOD": {
                "datasetpath": "/QCD_Pt-80to120_7TeV-pythia8/Summer10-START36_V10_S09-v1/AODSIM",
                "number_of_jobs": 60,
                "se_white_list": ["T2_FI_HIP"]
            },
            "pattuple_v3": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt-80to120_7TeV-pythia8/local-Summer10_START36_V10_S09_v1_AODSIM-pattuple_v3-350234694fe4ac3e4a7c59f3d58cf538/USER",
                "number_of_jobs": 3
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
                "number_of_jobs": 60
            },
            "AOD": {
                "datasetpath": "/QCD_Pt-120to170_7TeV-pythia8/Summer10-START36_V10_S09-v1/AODSIM",
                "number_of_jobs": 60,
                "se_white_list": ["T2_FI_HIP"]
            },
            "pattuple_v3": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt-120to170_7TeV-pythia8/local-Summer10_START36_V10_S09_v1_AODSIM-pattuple_v3-350234694fe4ac3e4a7c59f3d58cf538/USER",
                "number_of_jobs": 2
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
                "number_of_jobs": 60
            },
            "AOD": {
                "datasetpath": "/QCD_Pt-170to230_7TeV-pythia8/Summer10-START36_V10_S09-v2/AODSIM",
                "number_of_jobs": 60,
                "se_white_list": ["T2_FI_HIP"]
            },
            "pattuple_v3": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt-170to230_7TeV-pythia8/local-Summer10_START36_V10_S09_v2_AODSIM-pattuple_v3-350234694fe4ac3e4a7c59f3d58cf538/USER",
                "number_of_jobs": 2
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
                "number_of_jobs": 70
            },
            "AOD": {
                "datasetpath": "/QCD_Pt-230to300_7TeV-pythia8/Summer10-START36_V10_S09-v2/AODSIM",
                "number_of_jobs": 60,
                "se_white_list": ["T2_FI_HIP"]
            },
            "pattuple_v3": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt-230to300_7TeV-pythia8/local-Summer10_START36_V10_S09_v2_AODSIM-pattuple_v3-350234694fe4ac3e4a7c59f3d58cf538/USER",
                "number_of_jobs": 2
            },
            "pattuple_v6": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt-230to300_7TeV-pythia8/local-Summer10_START36_V10_S09_v2_GEN-SIM-RECO_pattuple_v6_1-2366fe480375ff6f751e0b7e8ec70b52/USER",
                "number_of_jobs": 2
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
                "number_of_jobs": 50
            },
            "AOD": {
                "datasetpath": "/TTbar/Summer10-START36_V9_S09-v1/AODSIM",
                "number_of_jobs": 50,
            },
            "pattuple_v3": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTbar/local-Summer10_START36_V9_S09_v1_AODSIM-pattuple_v3-350234694fe4ac3e4a7c59f3d58cf538/USER",
                "number_of_jobs": 3
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
                "number_of_jobs": 120
            },
            "AOD": {
                "datasetpath": "/TTbarJets_Tauola-madgraph/Summer10-START36_V9_S09-v1/AODSIM",
                "number_of_jobs": 60,
                "se_white_list": ["T2_FI_HIP"]
            },
            "pattuple_v3": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTbarJets_Tauola-madgraph/local-Summer10_START36_V9_S09_v1_AODSIM-pattuple_v3-350234694fe4ac3e4a7c59f3d58cf538/USER",
                "number_of_jobs": 6
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
                "number_of_jobs": 490
            },
            "AOD": {
                "datasetpath": "/WJets_7TeV-madgraph-tauola/Summer10-START36_V9_S09-v1/AODSIM",
                "number_of_jobs": 350,
                "se_white_list": ["T2_FI_HIP"]
            },
            "pattuple_v3": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WJets_7TeV-madgraph-tauola/local-Summer10_START36_V9_S09_v1_AODSIM-pattuple_v3-350234694fe4ac3e4a7c59f3d58cf538/USER",
                "number_of_jobs": 40
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
                "number_of_jobs": 15,
            }
        },
    },
    "SingleTop_sChannel": {
        "dataVersion": "37X",
        "crossSection": 0.99,
        "data": {
            "RECO": {
                "datasetpath": "/SingleTop_sChannel-madgraph/Summer10-START37_V5_S09-v1/GEN-SIM-RECO",
                "number_of_jobs": 10,
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
                "number_of_jobs": 15,
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
                "number_of_jobs": 10,
            },
            "AOD": {
                "fallback": "RECO"
            }
        },
    },
}
