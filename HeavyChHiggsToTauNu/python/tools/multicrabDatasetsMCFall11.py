## \package multicrabDatasetsMCFall11
#
# Dataset definitions for Fall11 MC production (CMSSW 44x)
#
# \see multicrab

import multicrabDatasetsCommon as common

# For pattuples: ~10kev/job (~20-30 kB/event on average, depending on the process)
# For analysis: ~500kev/job

# Default signal cross section taken the same as ttbar

## Dataset definitions
datasets = {
    # Signal WH
    "TTToHplusBWB_M80_Fall11": {
        "dataVersion": "44XmcS6",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-100_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM",
                "number_of_jobs": 50, # Adjusted for PATtuple file size;  53 GB, 19 files
            },
        }
    },
    "TTToHplusBWB_M90_Fall11": {
        "dataVersion": "44XmcS6",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-90_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM",
                "number_of_jobs": 50, # Adjusted for PATtuple file size
            },
        }
    },
    "TTToHplusBWB_M100_Fall11": {
        "dataVersion": "44XmcS6",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-100_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM",
                "number_of_jobs": 50, # Adjusted for PATtuple file size
            },
        }
    },
    "TTToHplusBWB_M120_Fall11": {
        "dataVersion": "44XmcS6",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM",
                "number_of_jobs": 50, # Adjusted for PATtuple file size
            },
        }
    },
    "TTToHplusBWB_M140_Fall11": {
        "dataVersion": "44XmcS6",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-140_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM",
                "number_of_jobs": 50, # Adjusted for PATtuple file size
            },
        }
    },
    "TTToHplusBWB_M150_Fall11": {
        "dataVersion": "44XmcS6",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-150_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM",
                "number_of_jobs": 50, # Adjusted for PATtuple file size
            },
        }
    },
    "TTToHplusBWB_M155_Fall11": {
        "dataVersion": "44XmcS6",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-155_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM",
                "number_of_jobs": 50, # Adjusted for PATtuple file size
            },
        }
    },
    "TTToHplusBWB_M160_Fall11": {
        "dataVersion": "44XmcS6",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-160_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM",
                "number_of_jobs": 50, # Adjusted for PATtuple file size
            },
        }
    },
    # Signal HH
    "TTToHplusBHminusB_M80_Fall11": {
        "dataVersion": "44XmcS6",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBHminusB_M-80_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM",
                "number_of_jobs": 50, # Adjusted for PATtuple file size
            },
        }
    },
    "TTToHplusBHminusB_M90_Fall11": {
        "dataVersion": "44XmcS6",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBHminusB_M-90_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM",
                "number_of_jobs": 50, # Adjusted for PATtuple file size
            },
        }
    },
    "TTToHplusBHminusB_M100_Fall11": {
        "dataVersion": "44XmcS6",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBHminusB_M-100_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM",
                "number_of_jobs": 50, # Adjusted for PATtuple file size
            },
        }
    },
    "TTToHplusBHminusB_M120_Fall11": {
        "dataVersion": "44XmcS6",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBHminusB_M-120_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM",
                "number_of_jobs": 50, # Adjusted for PATtuple file size
            },
        }
    },
    "TTToHplusBHminusB_M140_Fall11": {
        "dataVersion": "44XmcS6",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBHminusB_M-140_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM",
                "number_of_jobs": 50, # Adjusted for PATtuple file size
            },
        }
    },
    "TTToHplusBHminusB_M155_Fall11": {
        "dataVersion": "44XmcS6",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBHminusB_M-155_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM",
                "number_of_jobs": 50, # Adjusted for PATtuple file size
            },
        }
    },
    "TTToHplusBHminusB_M160_Fall11": {
        "dataVersion": "44XmcS6",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBHminusB_M-160_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM",
                "number_of_jobs": 50, # Adjusted for PATtuple file size
            },
        }
    },

    # Signal heavy
    "HplusTB_M180_Fall11": {
        "dataVersion": "44XmcS6",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/HplusTB_M-180_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM",
                "number_of_jobs": 50, # Adjusted for PATtuple file size
            },
        }
    },
    "HplusTB_M190_Fall11": {
        "dataVersion": "44XmcS6",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/HplusTB_M-190_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM",
                "number_of_jobs": 50, # Adjusted for PATtuple file size
            },
        }
    },
    "HplusTB_M200_Fall11": {
        "dataVersion": "44XmcS6",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/HplusTB_M-200_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM",
                "number_of_jobs": 50, # Adjusted for PATtuple file size
            },
        }
    },
    "HplusTB_M220_Fall11": {
        "dataVersion": "44XmcS6",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/HplusTB_M-220_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM",
                "number_of_jobs": 50, # Adjusted for PATtuple file size
            },
        }
    },
    "HplusTB_M250_Fall11": {
        "dataVersion": "44XmcS6",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/HplusTB_M-250_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM",
                "number_of_jobs": 50, # Adjusted for PATtuple file size
            },
        }
    },
    "HplusTB_M300_Fall11": {
        "dataVersion": "44XmcS6",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/HplusTB_M-300_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM",
                "number_of_jobs": 50, # Adjusted for PATtuple file size
            },
        }
    },

    # QCD backgrounds
    # Cross sections are from https://twiki.cern.ch/twiki/bin/view/CMS/ReProcessingSummer2011
#    "QCD_Pt120to170_TuneZ2_Fall11": {
#        "dataVersion": "44XmcS6",
#        "crossSection": 1.151e+05,
#        "data": {
#            "AOD": {
#                "datasetpath": "/QCD_Pt-120to170_TuneZ2_7TeV_pythia6/Fall11-PU_S6_START44_V9B-v1/AODSIM",
#                "number_of_jobs": 490, # Adjusted for PATtuple file size
#            },
#        },
#    },
#    "QCD_Pt170to300_TuneZ2_Fall11": {
#        "dataVersion": "44XmcS6",
#        "crossSection": 2.426e+04,
#        "data": {
#            "AOD": {
#                "datasetpath": "/QCD_Pt-170to300_TuneZ2_7TeV_pythia6/Fall11-PU_S6_START44_V9B-v1/AODSIM",
#                "number_of_jobs": 490, # Adjusted for PATtuple file size
#            },
#        },
#    },
#    "QCD_Pt300to470_TuneZ2_Fall11": {
#        "dataVersion": "44XmcS6",
#        "crossSection": 1.168e+03,
#        "data": {
#            "AOD": {
#                "datasetpath": "/QCD_Pt-300to470_TuneZ2_7TeV_pythia6/Fall11-PU_S6_START44_V9B-v1/AODSIM",
#                "number_of_jobs": 490 # Adjusted for PATtuple file size
#            },
#        }
#    },

    # EWK pythia
    # Cross sections https://twiki.cern.ch/twiki/bin/view/CMS/CrossSections_3XSeries
    "WW_TuneZ2_Fall11": {
        "dataVersion": "44XmcS6",
        "crossSection": 43,
        "args": { "triggerMC": "1" },
        "skimConfig": ["SkimFourJets_cff", "SkimFourJetsChs_cff"],
        "data": {
            "AOD": {
                "datasetpath": "/WW_TuneZ2_7TeV_pythia6_tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM",
                "number_of_jobs": 50, # Adjusted for PATtuple file size; file size 890 GB, 252-275 files, expected output max. 185 MB/file
            },
        },
    },
    "WZ_TuneZ2_Fall11": {
        "dataVersion": "44XmcS6",
        "crossSection": 18.2,
        "args": { "triggerMC": "1" },
        "skimConfig": ["SkimFourJets_cff", "SkimFourJetsChs_cff"],
        "data": {
            "AOD": {
                "datasetpath": "/WZ_TuneZ2_7TeV_pythia6_tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM",
                "number_of_jobs": 50, # Adjusted for PATtuple file size, expected output max. 185 MB/file
            },
        },
    },
    "ZZ_TuneZ2_Fall11": {
        "dataVersion": "44XmcS6",
        "crossSection": 5.9,
        "args": { "triggerMC": "1" },
        "skimConfig": ["SkimFourJets_cff", "SkimFourJetsChs_cff"],
        "data": {
            "AOD": {
                "datasetpath": "/ZZ_TuneZ2_7TeV_pythia6_tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM",
                "number_of_jobs": 50, # Adjusted for PATtuple file size, expected output max. 185 MB/file
            },
        },
    },

    # EWK MadGraph
    # Cross sections from
    # [1] https://twiki.cern.ch/twiki/bin/view/CMS/CrossSections_3XSeries
    # [2] https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSections
    "TTJets_TuneZ2_Fall11": {
        "dataVersion": "44XmcS6",
        "crossSection": 165, # [1,2], approx. NNLO
        "args": { "triggerMC": "1" },
        "skimConfig": ["SkimFourJets_cff", "SkimFourJetsChs_cff"],
        "data": {
            "AOD": {
                "datasetpath": "/TTJets_TuneZ2_7TeV-madgraph-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM",
                "number_of_jobs": 490, # Adjusted for PATtuple file size ; file size 15214; 3938 files, expected output max. 266 MB/file
            },
        },
    },
    "WJets_TuneZ2_Fall11": {
        "dataVersion": "44XmcS6",
        "crossSection": 31314, # [2], NNLO
        "args": { "triggerMC": "1" },
        "skimConfig": ["SkimFourJets_cff", "SkimFourJetsChs_cff"],
        "data": {
            "AOD": {
                "datasetpath": "/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM",
                "number_of_jobs": 490, # Adjusted for PATtuple file size ; file size 16000 GB, 4500 files, expected output max. 37 MB/file
                #"se_white_list": ["T2_FI_HIP"],
            },
        },
    },
    "W2Jets_TuneZ2_Fall11": {
        "dataVersion": "44XmcS6",
        "crossSection": 1, # FIXME
        "args": { "triggerMC": "1" },
        "skimConfig": ["SkimFourJets_cff", "SkimFourJetsChs_cff"],
        "data": {
            "AOD": {
                "datasetpath": "/W2Jets_TuneZ2_7TeV-madgraph-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM",
                "number_of_jobs": 300, # Adjusted for PATtuple file size ; expected output max. 38 MB/file
                #"se_white_list": ["T2_FI_HIP"],
            },
        },
    },
    "W3Jets_TuneZ2_Fall11": {
        "dataVersion": "44XmcS6",
        "crossSection": 1, # FIXME
        "args": { "triggerMC": "1" },
        "skimConfig": ["SkimFourJets_cff", "SkimFourJetsChs_cff"],
        "data": {
            "AOD": {
                "datasetpath": "/W3Jets_TuneZ2_7TeV-madgraph-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM",
                "number_of_jobs": 120, # Adjusted for PATtuple file size ; expected output max. 56 MB/file
                #"se_white_list": ["T2_FI_HIP"],
            },
        },
    },
    "W4Jets_TuneZ2_Fall11": {
        "dataVersion": "44XmcS6",
        "crossSection": 1, # FIXME
        "args": { "triggerMC": "1" },
        "skimConfig": ["SkimFourJets_cff", "SkimFourJetsChs_cff"],
        "data": {
            "AOD": {
                "datasetpath": "/W4Jets_TuneZ2_7TeV-madgraph-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM",
                "number_of_jobs": 200, # Adjusted for PATtuple file size ; expected output max. 144 MB/file
                #"se_white_list": ["T2_FI_HIP"],
            },
        },
    },
    "DYJetsToLL_M50_TuneZ2_Fall11": { # Z+jets
        "dataVersion": "44XmcS6",
        "crossSection": 3048, # [2], NNLO
        "args": { "triggerMC": "1" },
        "skimConfig": ["SkimFourJets_cff", "SkimFourJetsChs_cff"],
        "data": {
            "AOD": {
                "datasetpath": "/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM",
                "number_of_jobs": 350, # Adjusted for PATtuple file size ; file size 6945 GB, 1964 files, expected output max. 46 MB/file
            },
        }
    },
    "DYJetsToLL_M10to50_TuneZ2_Fall11": { # Z+jets
        "dataVersion": "44XmcS6",
        "crossSection": 9611, # Madgraph gives this number
        "args": { "triggerMC": "1" },
        "skimConfig": ["SkimFourJets_cff", "SkimFourJetsChs_cff"],
        "data": {
            "AOD": {
                "datasetpath": "/DYJetsToLL_M-10To50_TuneZ2_7TeV-madgraph/Fall11-PU_S6_START44_V9B-v1/AODSIM",
                "number_of_jobs": 300, # Adjusted for PATtuple file size ; file size 5900 GB, 1420 files, expected output max. 47 MB/file
            },
        }
    },


    # SingleTop Powheg
    # Cross sections from
    # https://twiki.cern.ch/twiki/bin/view/CMS/SingleTopMC2011
    # https://twiki.cern.ch/twiki/bin/view/CMS/SingleTopSigma
    "T_t-channel_TuneZ2_Fall11": {
        "dataVersion": "44XmcS6",
        "crossSection": 41.92,
        "args": { "triggerMC": "1" },
        "skimConfig": ["SkimFourJets_cff", "SkimFourJetsChs_cff"],
        "data": {
            "AOD": {
                "datasetpath": "/T_TuneZ2_t-channel_7TeV-powheg-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM",
                "number_of_jobs": 50, # Adjusted for PATtuple file size ; 866 GB, 395 files, expected output max. 47 MB/file
            },
        },
    },
    "Tbar_t-channel_TuneZ2_Fall11": {
        "dataVersion": "44XmcS6",
        "crossSection": 22.65,
        "args": { "triggerMC": "1" },
        "skimConfig": ["SkimFourJets_cff", "SkimFourJetsChs_cff"],
        "data": {
            "AOD": {
                "datasetpath": "/Tbar_TuneZ2_t-channel_7TeV-powheg-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM",
                "number_of_jobs": 50, # Adjusted for PATtuple file size, expected output max. 47 MB/file
            },
        },
    },
    "T_tW-channel_TuneZ2_Fall11": {
        "dataVersion": "44XmcS6",
        "crossSection": 7.87,
        "args": { "triggerMC": "1" },
        "skimConfig": ["SkimFourJets_cff", "SkimFourJetsChs_cff"],
        "data": {
            "AOD": {
                "datasetpath": "/T_TuneZ2_tW-channel-DR_7TeV-powheg-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM",
                "number_of_jobs": 20, # Adjusted for PATtuple file size ; 210 GB, 69 files, expected output max. 28 MB/file
            },
        },
    },
    "Tbar_tW-channel_TuneZ2_Fall11": {
        "dataVersion": "44XmcS6",
        "crossSection": 7.87,
        "args": { "triggerMC": "1" },
        "skimConfig": ["SkimFourJets_cff", "SkimFourJetsChs_cff"],
        "data": {
            "AOD": {
                "datasetpath": "/Tbar_TuneZ2_tW-channel-DR_7TeV-powheg-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM",
                "number_of_jobs": 20, # Adjusted for PATtuple file size, expected output max. 15 MB/file
            },
        },
    },
    "T_s-channel_TuneZ2_Fall11": {
        "dataVersion": "44XmcS6",
        "crossSection": 3.19,
        "args": { "triggerMC": "1" },
        "skimConfig": ["SkimFourJets_cff", "SkimFourJetsChs_cff"],
        "data": {
            "AOD": {
                "datasetpath": "/T_TuneZ2_s-channel_7TeV-powheg-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM",
                "number_of_jobs": 10, # Adjusted for PATtuple file size ; 59 GB, 19 files, expected output max. 57 MB/file
            },
        },
    },
    "Tbar_s-channel_TuneZ2_Fall11": {
        "dataVersion": "44XmcS6",
        "crossSection": 1.44,
        "args": { "triggerMC": "1" },
        "skimConfig": ["SkimFourJets_cff", "SkimFourJetsChs_cff"],
        "data": {
            "AOD": {
                "datasetpath": "/Tbar_TuneZ2_s-channel_7TeV-powheg-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM",
                "number_of_jobs": 10, # Adjusted for PATtuple file size, expected output max. 30 MB/file
            },
        },
    },

}
