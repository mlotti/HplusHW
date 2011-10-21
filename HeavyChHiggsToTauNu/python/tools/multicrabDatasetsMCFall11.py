import multicrabDatasetsCommon as common

# For pattuples: ~10kev/job (~20-30 kB/event on average, depending on the process)
# For analysis: ~500kev/job

# Default signal cross section taken the same as ttbar
datasets = {
    # Signal WH
    "TTToHplusBWB_M90_Fall11": {
        "dataVersion": "42XmcS6",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-90_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
                "number_of_jobs": 25, # Adjusted for PATtuple file size
            },
        }
    },
    "TTToHplusBWB_M120_Fall11": {
        "dataVersion": "42XmcS6",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
                "number_of_jobs": 25, # Adjusted for PATtuple file size
            },
        }
    },
    "TTToHplusBWB_M140_Fall11": {
        "dataVersion": "42XmcS6",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-140_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
                "number_of_jobs": 25, # Adjusted for PATtuple file size
            },
        }
    },
    "TTToHplusBWB_M155_Fall11": {
        "dataVersion": "42XmcS6",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-155_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
                "number_of_jobs": 25, # Adjusted for PATtuple file size
            },
        }
    },
    "TTToHplusBWB_M160_Fall11": {
        "dataVersion": "42XmcS6",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-160_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
                "number_of_jobs": 25, # Adjusted for PATtuple file size
            },
        }
    },
    # Signal HH
    "TTToHplusBHminusB_M80_Fall11": {
        "dataVersion": "42XmcS6",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBHminusB_M-80_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
                "number_of_jobs": 25, # Adjusted for PATtuple file size
            },
        }
    },
    "TTToHplusBHminusB_M140_Fall11": {
        "dataVersion": "42XmcS6",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBHminusB_M-140_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
                "number_of_jobs": 25, # Adjusted for PATtuple file size
            },
        }
    },
    "TTToHplusBHminusB_M160_Fall11": {
        "dataVersion": "42XmcS6",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBHminusB_M-160_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
                "number_of_jobs": 25, # Adjusted for PATtuple file size
            },
        }
    },

    # Signal heavy
    "HplusTB_M180_Fall11": {
        "dataVersion": "42XmcS6",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/HplusTB_M-180_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
                "number_of_jobs": 25, # Adjusted for PATtuple file size
            },
        }
    },
    "HplusTB_M190_Fall11": {
        "dataVersion": "42XmcS6",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/HplusTB_M-190_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
                "number_of_jobs": 25, # Adjusted for PATtuple file size
            },
        }
    },
    "HplusTB_M250_Fall11": {
        "dataVersion": "42XmcS6",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/HplusTB_M-250_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
                "number_of_jobs": 25, # Adjusted for PATtuple file size
            },
        }
    },
    "HplusTB_M300_Fall11": {
        "dataVersion": "42XmcS6",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/HplusTB_M-300_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
                "number_of_jobs": 25, # Adjusted for PATtuple file size
            },
        }
    },

    # QCD backgrounds
    # Cross sections are from https://twiki.cern.ch/twiki/bin/view/CMS/ReProcessingSummer2011
    "QCD_Pt120to170_TuneZ2_Fall11": {
        "dataVersion": "42XmcS6",
        "crossSection": 1.151e+05,
        "data": {
            "AOD": {
                "datasetpath": "/QCD_Pt-120to170_TuneZ2_7TeV_pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
                "number_of_jobs": 490, # Adjusted for PATtuple file size
            },
        },
    },
    "QCD_Pt300to470_TuneZ2_Fall11": {
        "dataVersion": "42XmcS6",
        "crossSection": 1.168e+03,
        "data": {
            "AOD": {
                "datasetpath": "/QCD_Pt-300to470_TuneZ2_7TeV_pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
                "number_of_jobs": 490 # Adjusted for PATtuple file size
            },
        }
    },


    # EWK pythia
    # Cross sections https://twiki.cern.ch/twiki/bin/view/CMS/CrossSections_3XSeries
    "WZ_TuneZ2_Fall11": {
        "dataVersion": "42XmcS6",
        "crossSection": 18.2,
        "data": {
            "AOD": {
                "datasetpath": "/WZ_TuneZ2_7TeV_pythia6_tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
                "number_of_jobs": 450, # Adjusted for PATtuple file size
            },
        },
    },
    "ZZ_TuneZ2_Fall11": {
        "dataVersion": "42XmcS6",
        "crossSection": 5.9,
        "data": {
            "AOD": {
                "datasetpath": "/ZZ_TuneZ2_7TeV_pythia6_tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
                "number_of_jobs": 300, # Adjusted for PATtuple file size
            },
        },
    },

    # EWK MadGraph
    # Cross sections from
    # [1] https://twiki.cern.ch/twiki/bin/view/CMS/CrossSections_3XSeries
    # [2] https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSections
    "WJets_TuneZ2_Fall11": {
        "dataVersion": "42XmcS6",
        "crossSection": 31314, # [2], NNLO
        "data": {
            "AOD": {
                "datasetpath": "/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
                "number_of_jobs": None, # Adjusted for PATtuple file size. FIXME: check the number of jobs
                #"use_server": 1,
                #"se_white_list": ["T2_FI_HIP"],
            },
        },
    },


    # SingleTop Powheg
    # Cross sections from
    # https://twiki.cern.ch/twiki/bin/view/CMS/SingleTopMC2011
    # https://twiki.cern.ch/twiki/bin/view/CMS/SingleTopSigma
    "T_tW-channel_TuneZ2_Fall11": {
        "dataVersion": "42XmcS6",
        "crossSection": 7.87,
        "data": {
            "AOD": {
                "datasetpath": "/T_TuneZ2_tW-channel-DR_7TeV-powheg-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
                "number_of_jobs": 80, # Adjusted for PATtuple file size
            },
        },
    },

}