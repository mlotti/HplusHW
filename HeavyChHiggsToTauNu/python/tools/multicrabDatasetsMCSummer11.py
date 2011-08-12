import multicrabDatasetsCommon as common

# For pattuples: ~15kev/job (~20 kB/event on average, depending trigger selection efficiency)
# For analysis: ~500kev/job

# Default signal cross section taken the same as ttbar

datasets = {
    # Signal WH
    "TTToHplusBWB_M80_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-80_7TeV-pythia6-tauola/Summer11-PU_S4_START42_V11-v1/AODSIM",
                "number_of_jobs": 20, # Adjusted for PATtuple file size
            },
            "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-80_7TeV-pythia6-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_pattuple_v17-99aef5cefaa1c50bd821f91d13a3f4ca/USER",
                "number_of_jobs": 1
            },
        }
    },
    "TTToHplusBWB_M90_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-90_7TeV-pythia6-tauola/Summer11-PU_S4_START42_V11-v1/AODSIM",
                "number_of_jobs": 20, # Adjusted for PATtuple file size
            },
            "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-90_7TeV-pythia6-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_pattuple_v17-99aef5cefaa1c50bd821f91d13a3f4ca/USER",
                "number_of_jobs": 1
            },
        }
    },
    "TTToHplusBWB_M100_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-100_7TeV-pythia6-tauola/Summer11-PU_S4_START42_V11-v1/AODSIM",
                "number_of_jobs": 20, # Adjusted for PATtuple file size
            },
            "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-100_7TeV-pythia6-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_pattuple_v17-99aef5cefaa1c50bd821f91d13a3f4ca/USER",
                "number_of_jobs": 1
            },
        }
    },
    "TTToHplusBWB_M120_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Summer11-PU_S4_START42_V11-v1/AODSIM",
                "number_of_jobs": 20, # Adjusted for PATtuple file size
            },
            "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-120_7TeV-pythia6-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_pattuple_v17-99aef5cefaa1c50bd821f91d13a3f4ca/USER",
                "number_of_jobs": 1
            },
        }
    },
    "TTToHplusBWB_M140_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-140_7TeV-pythia6-tauola/Summer11-PU_S4_START42_V11-v1/AODSIM",
                "number_of_jobs": 20, # Adjusted for PATtuple file size
            },
            "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-140_7TeV-pythia6-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_pattuple_v17-99aef5cefaa1c50bd821f91d13a3f4ca/USER",
                "number_of_jobs": 1
            },
        }
    },
    "TTToHplusBWB_M150_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-150_7TeV-pythia6-tauola/Summer11-PU_S4_START42_V11-v1/AODSIM",
                "number_of_jobs": 20, # Adjusted for PATtuple file size
            },
            "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-150_7TeV-pythia6-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_pattuple_v17-99aef5cefaa1c50bd821f91d13a3f4ca/USER",
                "number_of_jobs": 1
            },
        }
    },
    "TTToHplusBWB_M155_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-155_7TeV-pythia6-tauola/Summer11-PU_S4_START42_V11-v1/AODSIM",
                "number_of_jobs": 20, # Adjusted for PATtuple file size
            },
            "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-155_7TeV-pythia6-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_pattuple_v17-99aef5cefaa1c50bd821f91d13a3f4ca/USER",
                "number_of_jobs": 1
            },
        }
    },
    "TTToHplusBWB_M160_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-160_7TeV-pythia6-tauola/Summer11-PU_S4_START42_V11-v1/AODSIM",
                "number_of_jobs": 20, # Adjusted for PATtuple file size
            },
            "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-160_7TeV-pythia6-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_pattuple_v17-99aef5cefaa1c50bd821f91d13a3f4ca/USER",
                "number_of_jobs": 1
            },
        }
    },
    # Signal HH
    "TTToHplusBHminusB_M80_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBHminusB_M-80_7TeV-pythia6-tauola/Summer11-PU_S4_START42_V11-v1/AODSIM",
                "number_of_jobs": 20, # Adjusted for PATtuple file size
            },
            "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBHminusB_M-80_7TeV-pythia6-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_pattuple_v17-99aef5cefaa1c50bd821f91d13a3f4ca/USER",
                "number_of_jobs": 1
            },
        }
    },
    "TTToHplusBHminusB_M100_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBHminusB_M-100_7TeV-pythia6-tauola/Summer11-PU_S4_START42_V11-v1/AODSIM",
                "number_of_jobs": 20, # Adjusted for PATtuple file size
            },
            "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBHminusB_M-100_7TeV-pythia6-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_pattuple_v17-99aef5cefaa1c50bd821f91d13a3f4ca/USER",
                "number_of_jobs": 1
            },
        }
    },
    "TTToHplusBHminusB_M120_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBHminusB_M-120_7TeV-pythia6-tauola/Summer11-PU_S4_START42_V11-v1/AODSIM",
                "number_of_jobs": 20, # Adjusted for PATtuple file size
            },
            "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBHminusB_M-120_7TeV-pythia6-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_pattuple_v17-99aef5cefaa1c50bd821f91d13a3f4ca/USER",
                "number_of_jobs": 1
            },
        }
    },
    "TTToHplusBHminusB_M140_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBHminusB_M-140_7TeV-pythia6-tauola/Summer11-PU_S4_START42_V11-v1/AODSIM",
                "number_of_jobs": 20, # Adjusted for PATtuple file size
            },
            "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBHminusB_M-140_7TeV-pythia6-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_pattuple_v17-99aef5cefaa1c50bd821f91d13a3f4ca/USER",
                "number_of_jobs": 1
            },
        }
    },
    "TTToHplusBHminusB_M150_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBHminusB_M-150_7TeV-pythia6-tauola/Summer11-PU_S4_START42_V11-v1/AODSIM",
                "number_of_jobs": 20, # Adjusted for PATtuple file size
            },
            "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBHminusB_M-150_7TeV-pythia6-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_pattuple_v17-99aef5cefaa1c50bd821f91d13a3f4ca/USER",
                "number_of_jobs": 1
            },
        }
    },
    "TTToHplusBHminusB_M155_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBHminusB_M-155_7TeV-pythia6-tauola/Summer11-PU_S4_START42_V11-v1/AODSIM",
                "number_of_jobs": 20, # Adjusted for PATtuple file size
            },
           "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBHminusB_M-155_7TeV-pythia6-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_pattuple_v17-99aef5cefaa1c50bd821f91d13a3f4ca/USER",
                "number_of_jobs": 1
            },
        }
    },
    "TTToHplusBHminusB_M160_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBHminusB_M-160_7TeV-pythia6-tauola/Summer11-PU_S4_START42_V11-v1/AODSIM",
                "number_of_jobs": 20, # Adjusted for PATtuple file size
            },
            "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBHminusB_M-160_7TeV-pythia6-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_pattuple_v17-99aef5cefaa1c50bd821f91d13a3f4ca/USER",
                "number_of_jobs": 1
            },
        }
    },

    # Signal heavy
    "HplusTB_M180_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/HplusTB_M-180_7TeV-pythia6-tauola/Summer11-PU_S4_START42_V11-v1/AODSIM",
                "number_of_jobs": 30, # Adjusted for PATtuple file size
            },
        }
    },
    "HplusTB_M190_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/HplusTB_M-190_7TeV-pythia6-tauola/Summer11-PU_S4_START42_V11-v1/AODSIM",
                "number_of_jobs": 30, # Adjusted for PATtuple file size
            },
            "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/HplusTB_M-190_7TeV-pythia6-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_pattuple_v17-99aef5cefaa1c50bd821f91d13a3f4ca/USER",
                "number_of_jobs": 1
            },
        }
    },
    "HplusTB_M200_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/HplusTB_M-200_7TeV-pythia6-tauola/Summer11-PU_S4_START42_V11-v1/AODSIM",
                "number_of_jobs": 30, # Adjusted for PATtuple file size
            },
            "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/HplusTB_M-200_7TeV-pythia6-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_pattuple_v17-99aef5cefaa1c50bd821f91d13a3f4ca/USER",
                "number_of_jobs": 1
            },
        }
    },
    "HplusTB_M220_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/HplusTB_M-220_7TeV-pythia6-tauola/Summer11-PU_S4_START42_V11-v1/AODSIM",
                "number_of_jobs": 30, # Adjusted for PATtuple file size
            },
            "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/HplusTB_M-220_7TeV-pythia6-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_pattuple_v17-99aef5cefaa1c50bd821f91d13a3f4ca/USER",
                "number_of_jobs": 1
            },
        }
    },
    "HplusTB_M250_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/HplusTB_M-250_7TeV-pythia6-tauola/Summer11-PU_S4_START42_V11-v1/AODSIM",
                "number_of_jobs": 30, # Adjusted for PATtuple file size
            },
            "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/HplusTB_M-250_7TeV-pythia6-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_pattuple_v17-99aef5cefaa1c50bd821f91d13a3f4ca/USER",
                "number_of_jobs": 1
            },
        }
    },
    "HplusTB_M300_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/HplusTB_M-300_7TeV-pythia6-tauola/Summer11-PU_S4_START42_V11-v1/AODSIM",
                "number_of_jobs": 30, # Adjusted for PATtuple file size
            },
            "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/HplusTB_M-300_7TeV-pythia6-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_pattuple_v17-99aef5cefaa1c50bd821f91d13a3f4ca/USER",
                "number_of_jobs": 1
            },
        }
    },

    # QCD backgrounds
    # Cross sections are from https://twiki.cern.ch/twiki/bin/view/CMS/ReProcessingSummer2011
    "QCD_Pt15to30_TuneZ2_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 8.159e+08,
        "data": {
           "AOD": {
               "datasetpath": "/QCD_Pt-15to30_TuneZ2_7TeV_pythia6/Summer11-PU_S3_START42_V11-v2/AODSIM",
               "number_of_jobs": 490, # Adjusted for PATtuple file size
           },
        },
    },
    "QCD_Pt30to50_TuneZ2_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 5.312e+07,
        "data": {
           "AOD": {
               "datasetpath": "/QCD_Pt-30to50_TuneZ2_7TeV_pythia6/Summer11-PU_S3_START42_V11-v2/AODSIM",
               "number_of_jobs": 200, # Adjusted for PATtuple file size
           },
           "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt-30to50_TuneZ2_7TeV_pythia6/local-Summer11_PU_S3_START42_V11_v2_AODSIM_pattuple_v17-99aef5cefaa1c50bd821f91d13a3f4ca/USER",
                "number_of_jobs": 4
            },
        },
    },
    "QCD_Pt50to80_TuneZ2_Summer11": {
        "dataVersion":  "42Xmc",
        "crossSection": 6.359e+06,
        "data": {
           "AOD": {
               "datasetpath": "/QCD_Pt-50to80_TuneZ2_7TeV_pythia6/Summer11-PU_S3_START42_V11-v2/AODSIM",
               "number_of_jobs": 200, # Adjusted for PATtuple file size
           },
           "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt-50to80_TuneZ2_7TeV_pythia6/local-Summer11_PU_S3_START42_V11_v2_AODSIM_pattuple_v17-99aef5cefaa1c50bd821f91d13a3f4ca/USER",
                "number_of_jobs": 4
            },
        },
    },
    "QCD_Pt80to120_TuneZ2_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 7.843e+05,
        "data": {
           "AOD": {
               "datasetpath": "/QCD_Pt-80to120_TuneZ2_7TeV_pythia6/Summer11-PU_S3_START42_V11-v2/AODSIM",
               "number_of_jobs": 250, # Adjusted for PATtuple file size
           },
           "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt-80to120_TuneZ2_7TeV_pythia6/local-Summer11_PU_S3_START42_V11_v2_AODSIM_pattuple_v17-99aef5cefaa1c50bd821f91d13a3f4ca/USER",
                "number_of_jobs": 5
            },
        },
    },
    "QCD_Pt120to170_TuneZ2_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 1.151e+05,
        "data": {
            "AOD": {
                "datasetpath": "/QCD_Pt-120to170_TuneZ2_7TeV_pythia6/Summer11-PU_S3_START42_V11-v2/AODSIM",
                "number_of_jobs": 250, # Adjusted for PATtuple file size
            },
           "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt-120to170_TuneZ2_7TeV_pythia6/local-Summer11_PU_S3_START42_V11_v2_AODSIM_pattuple_v17-99aef5cefaa1c50bd821f91d13a3f4ca/USER",
                "number_of_jobs": 5
            },
        },
    },
    "QCD_Pt170to300_TuneZ2_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 2.426e+04,
        "data": {
            "AOD": {
                "datasetpath": "/QCD_Pt-170to300_TuneZ2_7TeV_pythia6/Summer11-PU_S3_START42_V11-v2/AODSIM",
                "number_of_jobs": 300, # Adjusted for PATtuple file size
            },
           "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt-170to300_TuneZ2_7TeV_pythia6/local-Summer11_PU_S3_START42_V11_v2_AODSIM_pattuple_v17-99aef5cefaa1c50bd821f91d13a3f4ca/USER",
                "number_of_jobs": 5
            },
        },
    },
    "QCD_Pt300to470_TuneZ2_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 1.168e+03,
        "data": {
            "AOD": {
                "datasetpath": "/QCD_Pt-300to470_TuneZ2_7TeV_pythia6/Summer11-PU_S3_START42_V11-v2/AODSIM",
                "number_of_jobs": 450 # Adjusted for PATtuple file size
            },
           "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt-300to470_TuneZ2_7TeV_pythia6/local-Summer11_PU_S3_START42_V11_v2_AODSIM_pattuple_v17-99aef5cefaa1c50bd821f91d13a3f4ca/USER",
                "number_of_jobs": 5
            },
        }
    },
    "QCD_Pt20_MuEnriched_TuneZ2_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 296600000.*0.0002855,
        "data": {
            "AOD": {
                "datasetpath": "/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/Summer11-PU_S4_START42_V11-v1/AODSIM",
                "number_of_jobs": 200,  # Adjusted for PAT on the fly (NOT for PATtuple processing)
            }
        },
    },
    

    # EWK pythia
    # Cross sections (not yet) from https://twiki.cern.ch/twiki/bin/view/CMS/CrossSections_3XSeries
    "TT_TuneZ2_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TT_TuneZ2_7TeV-pythia6-tauola/Summer11-PU_S3_START42_V11-v2/AODSIM",
                "number_of_jobs": 80, # Adjusted for PATtuple file size
            },
        },
    },
    "WToTauNu_TuneZ2_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 7899,
        "data": {
            "AOD": {
                "datasetpath": "/WToTauNu_TuneZ2_7TeV-pythia6-tauola/Summer11-PU_S3_START42_V11-v2/AODSIM",
                "number_of_jobs": 150, # Adjusted for PATtuple file size
            },
        },
    },
    "WToMuNu_TuneZ2_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 7899,
        "data": {
            "AOD": {
                "datasetpath": "/WToMuNu_TuneZ2_7TeV-pythia6/Summer11-PU_S3_START42_V11-v2/AODSIM",
                "number_of_jobs": 150,
            },
        },
    },
    "DYToTauTau_TuneZ2_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 1300,
        "data": {
            "AOD": {
                "datasetpath": "/DYToTauTau_M-20_TuneZ2_7TeV-pythia6-tauola/Summer11-PU_S3_START42_V11-v2/AODSIM",
                "number_of_jobs": 50, # Adjusted for PATtuple file size
            },
        },
    },
    "DYToMuMu_TuneZ2_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 1300,
        "data": {
            "AOD": {
                "datasetpath": "/DYToMuMu_M-20_TuneZ2_7TeV-pythia6-tauola/Summer11-PU_S3_START42_V11-v2/AODSIM",
                "number_of_jobs": 100,
            },
        },
    },
    # Cross sections https://twiki.cern.ch/twiki/bin/view/CMS/CrossSections_3XSeries
    "WW_TuneZ2_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 43,
        "data": {
            "AOD": {
                "datasetpath": "/WW_TuneZ2_7TeV_pythia6_tauola/Summer11-PU_S4_START42_V11-v1/AODSIM",
                "number_of_jobs": 300, # Adjusted for PATtuple file size
            },
        },
    },
    "WZ_TuneZ2_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 18,
        "data": {
            "AOD": {
                "datasetpath": "/WZ_TuneZ2_7TeV_pythia6_tauola/Summer11-PU_S4_START42_V11-v1/AODSIM",
                "number_of_jobs": 300, # Adjusted for PATtuple file size
            },
        },
    },
    "ZZ_TuneZ2_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 5.9,
        "data": {
            "AOD": {
                "datasetpath": "/ZZ_TuneZ2_7TeV_pythia6_tauola/Summer11-PU_S4_START42_V11-v1/AODSIM",
                "number_of_jobs": 300, # Adjusted for PATtuple file size
            },
        },
    },


    # EWK MadGraph
    # Cross sections from
    # [1] https://twiki.cern.ch/twiki/bin/view/CMS/CrossSections_3XSeries
    # [2] https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSections
    "TTJets_TuneZ2_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 165, # [1,2], approx. NNLO
        "data": {
            "AOD": {
                "datasetpath": "/TTJets_TuneZ2_7TeV-madgraph-tauola/Summer11-PU_S4_START42_V11-v1/AODSIM",
                "number_of_jobs": 300, # Adjusted for PATtuple file size
            },
            "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTJets_TuneZ2_7TeV-madgraph-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_pattuple_v17-99aef5cefaa1c50bd821f91d13a3f4ca/USER",
                "number_of_jobs": 10
            },
        },
    },
    "WJets_TuneZ2_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 31314, # [2], NNLO
        "data": {
            "AOD": {
                "datasetpath": "/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/Summer11-PU_S4_START42_V11-v1/AODSIM",
                "number_of_jobs": 2000, # Adjusted for PATtuple file size.
                "use_server": 1,
            },
            "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_pattuple_v17-99aef5cefaa1c50bd821f91d13a3f4ca/USER",
                "number_of_jobs": 30
            },
        },
    },
    "DYJetsToLL_M50_TuneZ2_Summer11": { # Z+jets
        "dataVersion": "42Xmc",
        "crossSection": 3048, # [2], NNLO
        "data": {
            "AOD": {
                "datasetpath": "/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/Summer11-PU_S4_START42_V11-v1/AODSIM",
                "number_of_jobs": 1500, # Adjusted for PATtuple file size
                "use_server": 1,
            },
            "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_pattuple_v17-99aef5cefaa1c50bd821f91d13a3f4ca/USER",
                "number_of_jobs": 50
            },
        }
    },

    # SingleTop Powheg
    # Cross sections from
    # https://twiki.cern.ch/twiki/bin/view/CMS/SingleTopMC2011
    # https://twiki.cern.ch/twiki/bin/view/CMS/SingleTopSigma
    "T_t-channel_TuneZ2_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 41.92,
        "data": {
            "AOD": {
                "datasetpath": "/T_TuneZ2_t-channel_7TeV-powheg-tauola/Summer11-PU_S4_START42_V11-v1/AODSIM",
                "number_of_jobs": 260, # Adjusted for PATtuple file size
            },
        },
    },
    "Tbar_t-channel_TuneZ2_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 22.65,
        "data": {
            "AOD": {
                "datasetpath": "/Tbar_TuneZ2_t-channel_7TeV-powheg-tauola/Summer11-PU_S4_START42_V11-v1/AODSIM",
                "number_of_jobs": 130, # Adjusted for PATtuple file size
            },
        },
    },
    "T_tW-channel_TuneZ2_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 7.87,
        "data": {
            "AOD": {
                "datasetpath": "/T_TuneZ2_tW-channel-DR_7TeV-powheg-tauola/Summer11-PU_S4_START42_V11-v1/AODSIM",
                "number_of_jobs": 60, # Adjusted for PATtuple file size
            },
        },
    },
    "Tbar_tW-channel_TuneZ2_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 7.87,
        "data": {
            "AOD": {
                "datasetpath": "/Tbar_TuneZ2_tW-channel-DR_7TeV-powheg-tauola/Summer11-PU_S4_START42_V11-v1/AODSIM",
                "number_of_jobs": 60, # Adjusted for PATtuple file size
            },
        },
    },
    "T_s-channel_TuneZ2_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 3.19,
        "data": {
            "AOD": {
                "datasetpath": "/T_TuneZ2_s-channel_7TeV-powheg-tauola/Summer11-PU_S4_START42_V11-v1/AODSIM",
                "number_of_jobs": 20, # Adjusted for PATtuple file size
            },
        },
    },
    "Tbar_s-channel_TuneZ2_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 1.44,
        "data": {
            "AOD": {
                "datasetpath": "/Tbar_TuneZ2_s-channel_7TeV-powheg-tauola/Summer11-PU_S4_START42_V11-v1/AODSIM",
                "number_of_jobs": 10, # Adjusted for PATtuple file size
            },
        },
    },

}
