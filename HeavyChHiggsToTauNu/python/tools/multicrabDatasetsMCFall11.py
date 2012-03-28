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
            "pattuple_v25": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-100_7TeV-pythia6-tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3_test2_TTToHplusBWB_M80_Fall11-b907d114bdb314991aecc34de5a9eb36/USER",
                "number_of_jobs": 2 # 218200 evt, 15-18 MB / file
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
            "pattuple_v25": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-90_7TeV-pythia6-tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3_test2_TTToHplusBWB_M90_Fall11-b907d114bdb314991aecc34de5a9eb36/USER",
                "number_of_jobs": 2 # 218200 evt
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
            "pattuple_v25": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-100_7TeV-pythia6-tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3_test2_TTToHplusBWB_M100_Fall11-b907d114bdb314991aecc34de5a9eb36/USER",
                "number_of_jobs": 2 # 218200 evt
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
             "pattuple_v25": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-120_7TeV-pythia6-tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3_test2_TTToHplusBWB_M120_Fall11-b907d114bdb314991aecc34de5a9eb36/USER",
                "number_of_jobs": 2 # 218200 evt
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
            "pattuple_v25": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-140_7TeV-pythia6-tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3_test2_TTToHplusBWB_M140_Fall11-b907d114bdb314991aecc34de5a9eb36/USER",
                "number_of_jobs": 2 # 218200 evt
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
            "pattuple_v25": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-150_7TeV-pythia6-tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3_test2_TTToHplusBWB_M150_Fall11-b907d114bdb314991aecc34de5a9eb36/USER",
                "number_of_jobs": 2 # 218900 evt
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
            "pattuple_v25": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-155_7TeV-pythia6-tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3_test2_TTToHplusBWB_M155_Fall11-b907d114bdb314991aecc34de5a9eb36/USER",
                "number_of_jobs": 2 # 218900 evt
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
            "pattuple_v25": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-160_7TeV-pythia6-tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3_test2_TTToHplusBWB_M160_Fall11-b907d114bdb314991aecc34de5a9eb36/USER",
                "number_of_jobs": 2 # 218400 evt
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
            "pattuple_v25": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBHminusB_M-80_7TeV-pythia6-tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3_test2_TTToHplusBHminusB_M80_Fall11-b907d114bdb314991aecc34de5a9eb36/USER",
                "number_of_jobs": 2 # 218400 evt
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
            "pattuple_v25": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBHminusB_M-90_7TeV-pythia6-tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3_test2_TTToHplusBHminusB_M90_Fall11-b907d114bdb314991aecc34de5a9eb36/USER",
                "number_of_jobs": 2 # 218900 evt
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
            "pattuple_v25": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBHminusB_M-100_7TeV-pythia6-tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3_test2_TTToHplusBHminusB_M100_Fall11-b907d114bdb314991aecc34de5a9eb36/USER",
                "number_of_jobs": 2 # 217600 evt
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
            "pattuple_v25": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBHminusB_M-120_7TeV-pythia6-tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3_test2_TTToHplusBHminusB_M120_Fall11-b907d114bdb314991aecc34de5a9eb36/USER",
                "number_of_jobs": 2 # 218800 evt
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
            "pattuple_v25": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBHminusB_M-140_7TeV-pythia6-tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3_test2_TTToHplusBHminusB_M140_Fall11-b907d114bdb314991aecc34de5a9eb36/USER",
                "number_of_jobs": 2 # 218800 evt
            },
        }
    },
    "TTToHplusBHminusB_M150_Fall11": {
        "dataVersion": "44XmcS6",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBHminusB_M-150_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM",
                "number_of_jobs": 50, # Adjusted for PATtuple file size
            },
            "pattuple_v25": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBHminusB_M-150_7TeV-pythia6-tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3_test2_TTToHplusBHminusB_M150_Fall11-b907d114bdb314991aecc34de5a9eb36/USER",
                "number_of_jobs": 2 # 218800 evt
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
            "pattuple_v25": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBHminusB_M-155_7TeV-pythia6-tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3_test2_TTToHplusBHminusB_M155_Fall11-b907d114bdb314991aecc34de5a9eb36/USER",
                "number_of_jobs": 2 # 217400 evt
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
            "pattuple_v25": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBHminusB_M-160_7TeV-pythia6-tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3_test2_TTToHplusBHminusB_M160_Fall11-b907d114bdb314991aecc34de5a9eb36/USER",
                "number_of_jobs": 2 # 220000 evt
            },
        }
    },

    # Signal heavy
    "HplusTB_M180_Fall11": {
        "dataVersion": "44XmcS6",
        "crossSection": 165, # FIXME
        "data": {
            "AOD": {
                "datasetpath": "/HplusTB_M-180_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM",
                "number_of_jobs": 50, # Adjusted for PATtuple file size
            },
            "pattuple_v25": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/HplusTB_M-180_7TeV-pythia6-tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3_test2_HplusTB_M180_Fall11-b907d114bdb314991aecc34de5a9eb36/USER",
                "number_of_jobs": 2 # 210823 evt
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
            "pattuple_v25": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/HplusTB_M-190_7TeV-pythia6-tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3_test2_HplusTB_M190_Fall11-b907d114bdb314991aecc34de5a9eb36/USER",
                "number_of_jobs": 2 # 209075 evt
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
            "pattuple_v25": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/HplusTB_M-200_7TeV-pythia6-tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3_test2_HplusTB_M200_Fall11-b907d114bdb314991aecc34de5a9eb36/USER",
                "number_of_jobs": 2 # 214140 evt
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
            "pattuple_v25": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/HplusTB_M-220_7TeV-pythia6-tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3_test2_HplusTB_M220_Fall11-b907d114bdb314991aecc34de5a9eb36/USER",
                "number_of_jobs": 2 # 199960 evt
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
            "pattuple_v25": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/HplusTB_M-250_7TeV-pythia6-tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3_test2_HplusTB_M250_Fall11-b907d114bdb314991aecc34de5a9eb36/USER",
                "number_of_jobs": 2 # 202450 evt
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
            "pattuple_v25": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/HplusTB_M-300_7TeV-pythia6-tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3_test2_HplusTB_M300_Fall11-b907d114bdb314991aecc34de5a9eb36/USER",
                "number_of_jobs": 2 # 201457 evt
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
            "pattuple_v25": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WW_TuneZ2_7TeV_pythia6_tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3_test2_WW_TuneZ2_Fall11-a776c511e9ef937d92535c43d40d7d9b/USER",
                "number_of_jobs": 3 # 50032 evt
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
            "pattuple_v25": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WZ_TuneZ2_7TeV_pythia6_tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3_test2_WZ_TuneZ2_Fall11-a776c511e9ef937d92535c43d40d7d9b/USER",
                "number_of_jobs": 2 # 44675 evt
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
            "pattuple_v25": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/ZZ_TuneZ2_7TeV_pythia6_tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3_test2_ZZ_TuneZ2_Fall11-a776c511e9ef937d92535c43d40d7d9b/USER",
                "number_of_jobs": 2
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
                "number_of_jobs": 490, # Adjusted for PATtuple file size ; file size 15214; 3938 files, expected output max. 266 MB/file, obs 60 MB / file
            },
            "pattuple_v25": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTJets_TuneZ2_7TeV-madgraph-tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3_test2_TTJets_TuneZ2_Fall11-a776c511e9ef937d92535c43d40d7d9b/USER",
                "number_of_jobs": 70 # 3125473 evt
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
            "pattuple_v25": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3_test2_WJets_TuneZ2_Fall11-a776c511e9ef937d92535c43d40d7d9b/USER",
                "number_of_jobs": 8 # 180088
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
                "number_of_jobs": 300, # Adjusted for PATtuple file size ; expected output max. 38 MB/file, obs 38 MB / file
                #"se_white_list": ["T2_FI_HIP"],
            },
            "pattuple_v25": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/W2Jets_TuneZ2_7TeV-madgraph-tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3_test2_W2Jets_TuneZ2_Fall11-a776c511e9ef937d92535c43d40d7d9b/USER",
                "number_of_jobs": 19 # 267079
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
                "number_of_jobs": 120, # Adjusted for PATtuple file size ; expected output max. 56 MB/file, obs 20-22 MB / file
                #"se_white_list": ["T2_FI_HIP"],
            },
            "pattuple_v25": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/W3Jets_TuneZ2_7TeV-madgraph-tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3_test2_W3Jets_TuneZ2_Fall11-a776c511e9ef937d92535c43d40d7d9b/USER",
                "number_of_jobs": 9 # 185741 evt
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
                "number_of_jobs": 200, # Adjusted for PATtuple file size ; expected output max. 144 MB/file, obs 20-22 MB / file
                #"se_white_list": ["T2_FI_HIP"],
            },
            "pattuple_v25": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/W4Jets_TuneZ2_7TeV-madgraph-tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3_test2_W4Jets_TuneZ2_Fall11-a776c511e9ef937d92535c43d40d7d9b/USER",
                "number_of_jobs": 12 # 580556 
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
                "number_of_jobs": 350, # Adjusted for PATtuple file size ; file size 6945 GB, 1964 files, expected output max. 46 MB/file, obs 40 MB / file
            },
            "pattuple_v25": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3_test2_DYJetsToLL_M50_TuneZ2_Fall11-a776c511e9ef937d92535c43d40d7d9b/USER",
                "number_of_jobs": 3 # 51916 evt
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
                "number_of_jobs": 300, # Adjusted for PATtuple file size ; file size 5900 GB, 1420 files, expected output max. 47 MB/file, obs 21 MB / file
            },
            "pattuple_v25": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/DYJetsToLL_M-10To50_TuneZ2_7TeV-madgraph/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3_test2_DYJetsToLL_M10to50_TuneZ2_Fall11-a776c511e9ef937d92535c43d40d7d9b/USER",
                "number_of_jobs": 1 # 894 evt
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
                "number_of_jobs": 50, # Adjusted for PATtuple file size ; 866 GB, 395 files, expected output max. 47 MB/file, obs 15-20 MB / file
            },
            "pattuple_v25": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/T_TuneZ2_t-channel_7TeV-powheg-tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3_test2_T_t-channel_TuneZ2_Fall11-a776c511e9ef937d92535c43d40d7d9b/USER",
                "number_of_jobs": 1 # 49900 evt
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
                "number_of_jobs": 50, # Adjusted for PATtuple file size, expected output max. 47 MB/file, obs 15-20 MB / file
            },
            "pattuple_v25": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tbar_TuneZ2_t-channel_7TeV-powheg-tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3_test2_Tbar_t-channel_TuneZ2_Fall11-a776c511e9ef937d92535c43d40d7d9b/USER",
                "number_of_jobs": 1 # 23601 evt
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
                "number_of_jobs": 20, # Adjusted for PATtuple file size ; 210 GB, 69 files, expected output max. 28 MB/file, obs 15-20 MB / file
            },
            "pattuple_v25": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/T_TuneZ2_tW-channel-DR_7TeV-powheg-tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3_test2_T_tW-channel_TuneZ2_Fall11-a776c511e9ef937d92535c43d40d7d9b/USER",
                "number_of_jobs": 1 # 36882 evt
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
                "number_of_jobs": 20, # Adjusted for PATtuple file size, expected output max. 15 MB/file, obs 15-20 MB / file
            },
            "pattuple_v25": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tbar_TuneZ2_tW-channel-DR_7TeV-powheg-tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3_test2_Tbar_tW-channel_TuneZ2_Fall11-a776c511e9ef937d92535c43d40d7d9b/USER",
                "number_of_jobs": 1 # 36369 evt
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
                "number_of_jobs": 10, # Adjusted for PATtuple file size ; 59 GB, 19 files, expected output max. 57 MB/file, obs 15-20 MB / file
            },
            "pattuple_v25": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/T_TuneZ2_s-channel_7TeV-powheg-tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3_test2_T_s-channel_TuneZ2_Fall11-a776c511e9ef937d92535c43d40d7d9b/USER",
                "number_of_jobs": 1 # 3618 evt
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
                "number_of_jobs": 10, # Adjusted for PATtuple file size, expected output max. 30 MB/file, obs 15-20 MB / file
            },
            "pattuple_v25": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tbar_TuneZ2_s-channel_7TeV-powheg-tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3_test2_Tbar_s-channel_TuneZ2_Fall11-a776c511e9ef937d92535c43d40d7d9b/USER",
                "number_of_jobs": 1 # 1685 evt
            },
        },
    },

}
