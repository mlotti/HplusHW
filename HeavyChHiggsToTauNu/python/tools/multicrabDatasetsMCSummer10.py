import multicrabDatasetsCommon as common

datasets = {
    # Signal MC
    "TTToHpmToTauNu_M90_Spring10": {
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
        }
    },
    "TTToHpmToTauNu_M100_Spring10": {
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
        }
    },
    "TTToHpmToTauNu_M120_Spring10": {
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
        }
    },
    "TTbar_Htaunu_M140_Spring10": {
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
        }
    },
    "TTbar_Htaunu_M160_Spring10": {
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
        }
    },

    # Background MC

    # QCD Summer10
    "QCD_Pt30to50_Summer10": {
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
        },
    },
    "QCD_Pt50to80_Summer10": {
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
        },
    },
    "QCD_Pt80to120_Summer10": {
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
        },
    },
    "QCD_Pt120to170_Summer10": {
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
        },
    },
    "QCD_Pt170to230_Summer10": {
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
        },
    },
    "QCD_Pt230to300_Summer10": {
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
        },
    },
    "QCD_Pt300to380_Summer10": {
        "dataVersion": "36X",
        "crossSection": 9.593e+02,
        "data": {
            "RECO": {
                "datasetpath": "/QCD_Pt-300to380_7TeV-pythia8/Summer10-START36_V10_S09-v1/GEN-SIM-RECO",
                "number_of_jobs": 40 # Adjusted for PATtuple file size
            },
        },
    },
    "QCD_Pt380to470_Summer10": {
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
    "TTbar_Summer10": {
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
        },
    },
    "TTbarJets_Summer10": {
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
        },
    },
    "WJets_Summer10": {
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
        },
    },

    # Backgrounds for electroweak background measurement (Summer10)
    "ZJets_Summer10": {
        "dataVersion": "37X",
        "crossSection": 2400,
        "data": {
            "AOD": {
                "datasetpath": "/ZJets-madgraph/Summer10-START37_V5_S09-v1/AODSIM",
                "number_of_jobs": 15, # Adjusted for PAT on the fly
            }
        },
    },
    "SingleTop_sChannel_Summer10": {
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
    "SingleTop_tChannel_Summer10": {
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
    "SingleTop_tWChannel_Summer10": {
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
