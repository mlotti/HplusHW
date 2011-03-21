import multicrabDatasetsCommon as common

datasets = {
    # Signal WH
    "TTToHplusBWB_M150_Spring11": {
        "dataVersion": "311Xredigi",
        "crossSection": -1, # not calculated yet!
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-150_7TeV-pythia6-tauola/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 35, # Adjusted for PATtuple file size
            },
        }
    },
    "TTToHplusBWB_M155_Spring11": {
        "dataVersion": "311Xredigi",
        "crossSection": -1, # not calculated yet!
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-155_7TeV-pythia6-tauola/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 35, # Adjusted for PATtuple file size
            },
        }
    },

    # Signal HH
    "TToHplusBHminusB_M80_Spring11": {
        "dataVersion": "311Xredigi",
        "crossSection": -1, # not calculated yet!
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBHminusB_M-80_7TeV-pythia6-tauola/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 35, # Adjusted for PATtuple file size
            },
        }
    },
    "TToHplusBHminusB_M100_Spring11": {
        "dataVersion": "311Xredigi",
        "crossSection": -1, # not calculated yet!
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBHminusB_M-100_7TeV-pythia6-tauola/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 35, # Adjusted for PATtuple file size
            },
        }
    },
    "TToHplusBHminusB_M120_Spring11": {
        "dataVersion": "311Xredigi",
        "crossSection": -1, # not calculated yet!
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBHminusB_M-120_7TeV-pythia6-tauola/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 35, # Adjusted for PATtuple file size
            },
        }
    },
    "TToHplusBHminusB_M140_Spring11": {
        "dataVersion": "311Xredigi",
        "crossSection": -1, # not calculated yet!
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBHminusB_M-140_7TeV-pythia6-tauola/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 35, # Adjusted for PATtuple file size
            },
        }
    },
    "TToHplusBHminusB_M150_Spring11": {
        "dataVersion": "311Xredigi",
        "crossSection": -1, # not calculated yet!
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBHminusB_M-150_7TeV-pythia6-tauola/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 35, # Adjusted for PATtuple file size
            },
        }
    },
    "TToHplusBHminusB_M155_Spring11": {
        "dataVersion": "311Xredigi",
        "crossSection": -1, # not calculated yet!
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBHminusB_M-155_7TeV-pythia6-tauola/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 35, # Adjusted for PATtuple file size
            },
        }
    },
    "TToHplusBHminusB_M160_Spring11": {
        "dataVersion": "311Xredigi",
        "crossSection": -1, # not calculated yet!
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBHminusB_M-160_7TeV-pythia6-tauola/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 35, # Adjusted for PATtuple file size
            },
        }
    },

    # QCD backgrounds
    # Cross sections are from https://twiki.cern.ch/twiki/bin/view/CMS/ReProcessingWinter2010
    "QCD_Pt170to300_TuneZ2_Winter10": {
        "dataVersion": "311Xredigi",
        "crossSection": 2.426e+04,
        "data": {
            "AOD": {
                "datasetpath": "/QCD_Pt_170to300_TuneZ2_7TeV_pythia6/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 450, # Adjusted for PATtuple file size
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
                "number_of_jobs": 300, # Adjusted for PATtuple file size
            },
        },
    }, 
    "TToBLNu_s-channel_TuneZ2_Spring11": {
        "dataVersion": "311Xredigi",
        "crossSection": 4.6*0.32442,
        "data": {
            "AOD": {
                "datasetpath": "/TToBLNu_TuneZ2_s-channel_7TeV-madgraph/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 110, # Adjusted for PATtuple file size
            },
        },
    },
    "TToBLNu_t-channel_TuneZ2_Spring11": {
        "dataVersion": "311Xredigi",
        "crossSection": 63*0.32442,
        "data": {
            "AOD": {
                "datasetpath": "/TToBLNu_TuneZ2_t-channel_7TeV-madgraph/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 110, # Adjusted for PATtuple file size
            },
        },
    },
    "TToBLNu_tW-channel_TuneZ2_Spring11": {
        "dataVersion": "311Xredigi",
        "crossSection": 10.6,
        "data": {
            "AOD": {
                "datasetpath": "/TToBLNu_TuneZ2_tW-channel_7TeV-madgraph/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 100, # Adjusted for PATtuple file size
            },
        },
    },
    "DYJetsToLL_M50_TuneZ2_Spring11": { # Z+jets
        "dataVersion": "311Xredigi",
        "crossSection": 2800,
        "data": {
            "AOD": {
                "datasetpath": "/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/Winter10-E7TeV_ProbDist_2010Data_BX156_START39_V8-v1/AODSIM",
                "number_of_jobs": 450, # Adjusted for PATtuple file size
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
                "number_of_jobs": 200, # Adjusted for PATtuple file size
            },
        },
    },
    "WZ_TuneZ2_Spring11": {
        "dataVersion": "311Xredigi",
        "crossSection": 18,
        "data": {
            "AOD": {
                "datasetpath": "/WZtoAnything_TuneZ2_7TeV-pythia6-tauola/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 250, # Adjusted for PATtuple file size
            },
        },
    },
    "ZZ_TuneZ2_Spring11": {
        "dataVersion": "311Xredigi",
        "crossSection": 5.9,
        "data": {
            "AOD": {
                "datasetpath": "/ZZtoAnything_TuneZ2_7TeV-pythia6-tauola/Spring11-PU_S1_START311_V1G1-v1/AODSIM",
                "number_of_jobs": 250, # Adjusted for PATtuple file size
            },
        },
    },
}
