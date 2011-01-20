import multicrabDatasetsCommon as common

datasets = {
    # Signal
    # "TTToHplusBWB_M90": {
    #     "dataVersion": ,
    #     "crossSection": 16.442915,
    #     "data": {
    #         "AOD": {
    #             "datasetpath": ,
    #             "number_of_jobs": 20,
    #         },
    #     }
    # },
    # "TTToHplusBWB_M100": {
    #     "dataVersion": ,
    #     "crossSection": 14.057857,
    #     "data": {
    #         "AOD": {
    #             "datasetpath": ,
    #             "number_of_jobs": 20,
    #         },
    #     }
    # },
    # "TTToHplusBWB_M120": {
    #     "dataVersion": ,
    #     "crossSection": 8.984715,
    #     "data": {
    #         "AOD": {
    #             "datasetpath": ,
    #             "number_of_jobs": 20,
    #         },
    #     }
    # },
    # "TTToHplusBWB_M140": {
    #     "dataVersion": ,
    #     "crossSection": 4.223402,
    #     "data": {
    #         "AOD": {
    #             "datasetpath": ,
    #             "number_of_jobs": 20,
    #         },
    #     }
    # },
    # "TTToHplusBWB_M160": {
    #     "dataVersion": ,
    #     "crossSection": 0.811493,
    #     "data": {
    #         "AOD": {
    #             "datasetpath": ,
    #             "number_of_jobs": 20,
    #         },
    #     }
    # },

    # QCD Winter10
    "QCD_Pt30to50_TuneZ2_Winter10": {
        "dataVersion": "39Xredigi",
        "crossSection": 5.312e+07,
        "data": {
            "AOD": {
                "datasetpath": "/QCD_Pt_30to50_TuneZ2_7TeV_pythia6/Winter10-E7TeV_ProbDist_2010Data_BX156_START39_V8-v1/AODSIM",
                "number_of_jobs": 450, # Adjusted for PATtuple file size
            },
            "pattuple_v8": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt_30to50_TuneZ2_7TeV_pythia6/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_pattuple_v8-399e3794c630ab5bd4c05a030cfeb22a/USER",
                "number_of_jobs": 10
            },
        },
    },
    # "QCD_Pt50to80_TuneZ2_Winter10": {
    #     "dataVersion":  "39Xredigi",
    #     "crossSection": 6.359e+06,
    #     "data": {
    #         "AOD": {
    #             "datasetpath": 
    #             "number_of_jobs": 150,
    #         },
    #     },
    # },
    "QCD_Pt80to120_TuneZ2_Winter10": {
        "dataVersion": "39Xredigi",
        "crossSection": 7.843e+05,
        "data": {
            "AOD": {
                "datasetpath": "/QCD_Pt_80to120_TuneZ2_7TeV_pythia6/Winter10-E7TeV_ProbDist_2010Data_BX156_START39_V8-v1/AODSIM",
                "number_of_jobs": 450, # Adjusted for PATtuple file size
            },
            "pattuple_v8": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt_80to120_TuneZ2_7TeV_pythia6/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_pattuple_v8-399e3794c630ab5bd4c05a030cfeb22a/USER",
                "number_of_jobs": 10
            },
        },
    },
    "QCD_Pt120to170_TuneZ2_Winter10": {
        "dataVersion": "39Xredigi",
        "crossSection": 1.151e+05,
        "data": {
            "AOD": {
                "datasetpath": "/QCD_Pt_120to170_TuneZ2_7TeV_pythia6/Winter10-E7TeV_ProbDist_2010Data_BX156_START39_V8-v1/AODSIM",
                "number_of_jobs": 450, # Adjusted for PATtuple file size
            },
            "pattuple_v8": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt_120to170_TuneZ2_7TeV_pythia6/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_pattuple_v8-399e3794c630ab5bd4c05a030cfeb22a/USER",
                "number_of_jobs": 10
            },
        },
    },
    "QCD_Pt170to300_TuneZ2_Winter10": {
        "dataVersion": "39Xredigi",
        "crossSection": 2.426e+04,
        "data": {
            "AOD": {
                "datasetpath": "/QCD_Pt_170to300_TuneZ2_7TeV_pythia6/Winter10-E7TeV_ProbDist_2010Data_BX156_START39_V8-v1/AODSIM",
                "number_of_jobs": 450, # Adjusted for PATtuple file size
            },
            "pattuple_v8": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt_170to300_TuneZ2_7TeV_pythia6/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_pattuple_v8-399e3794c630ab5bd4c05a030cfeb22a/USER",
                "number_of_jobs": 10
            },
        },
    },
    "QCD_Pt300to470_TuneZ2_Winter10": {
        "dataVersion": "39Xredigi",
        "crossSection": 1.168e+03,
        "data": {
            "AOD": {
                "datasetpath": "/QCD_Pt_300to470_TuneZ2_7TeV_pythia6/Winter10-E7TeV_ProbDist_2010Data_BX156_START39_V8-v1/AODSIM",
                "number_of_jobs": 450 # Adjusted for PATtuple file size
            },
            "pattuple_v8": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt_300to470_TuneZ2_7TeV_pythia6/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_pattuple_v8-399e3794c630ab5bd4c05a030cfeb22a/USER",
                "number_of_jobs": 10
            },
        },
    },


    # # Electroweak (Winter10)
    "TTJets_TuneZ2_Winter10": {
        "dataVersion": "39Xredigi",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTJets_TuneZ2_7TeV-madgraph-tauola/Winter10-E7TeV_ProbDist_2010Data_BX156_START39_V8-v1/AODSIM",
                "number_of_jobs": 400,
            },
            "pattuple_v8": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTJets_TuneZ2_7TeV-madgraph-tauola/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_pattuple_v8-399e3794c630ab5bd4c05a030cfeb22a/USER",
                "number_of_jobs": 5
            },
        },
    }, 
    "TTJets_TuneD6T_Winter10": {
        "dataVersion": "39Xredigi",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTJets_TuneD6T_7TeV-madgraph-tauola/Winter10-E7TeV_ProbDist_2010Data_BX156_START39_V8-v1/AODSIM",
                "number_of_jobs": 400,
            },
            "pattuple_v8": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTJets_TuneD6T_7TeV-madgraph-tauola/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_pattuple_v8-399e3794c630ab5bd4c05a030cfeb22a/USER",
                "number_of_jobs": 5
            },
        },
    },
    "WJets_TuneZ2_Winter10_noPU": {
        "dataVersion": "39Xredigi",
        "crossSection": 24640,
        "data": {
            "AOD": {
                "datasetpath": "/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/Winter10-START39_V8-v1/AODSIM",
                "number_of_jobs": 1500, # Adjusted for PATtuple file
                                        # size. CRAB doesn't really
                                        # create this many jobs, but
                                        # the large number seems to be
                                        # needed to get enough jobs
                "use_server": 1,
            },
            "pattuple_v8": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/local-Winter10_START39_V8_v1_AODSIM_pattuple_v8-399e3794c630ab5bd4c05a030cfeb22a/USER",
                "number_of_jobs": 60
            },
        },
    },
    "WJets_TuneD6T_Winter10": {
        "dataVersion": "39Xredigi",
        "crossSection": 24380,
        "data": {
            "AOD": {
                "datasetpath": "/WJetsToLNu_TuneD6T_7TeV-madgraph-tauola/Winter10-E7TeV_ProbDist_2010Data_BX156_START39_V8-v1/AODSIM",
                "number_of_jobs": 1500, # Adjusted for PATtuple file size
                "use_server": 1,
            },
            "pattuple_v8": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WJetsToLNu_TuneD6T_7TeV-madgraph-tauola/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_pattuple_v8-399e3794c630ab5bd4c05a030cfeb22a/USER",
                "number_of_jobs": 60
            },
        },
    },


    # # Backgrounds for electroweak background measurement (Fall10)
    "QCD_Pt20_MuEnriched_TuneZ2_Winter10": {
        "dataVersion": "39Xredigi",
        "crossSection": 296600000.*0.0002855,
        "data": {
            "AOD": {
                "datasetpath": "/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/Winter10-E7TeV_ProbDist_2010Data_BX156_START39_V8-v1/AODSIM",
                "number_of_jobs": 200,  # Adjusted for PAT on the fly
            }
        },
    },
    "DYJetsToLL_TuneZ2_Winter10": { # Z+jets
        "dataVersion":
        "crossSection": 2321,
        "data": {
            "AOD": {
                "datasetpath": "/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/Winter10-E7TeV_ProbDist_2010Data_BX156_START39_V8-v1/AODSIM",
                "number_of_jobs": 15,
            }
        },
    },
    "DYJetsToLL_TuneZ2_Winter10_noPU": { # Z+jets
        "dataVersion":
        "crossSection": 2321,
        "data": {
            "AOD": {
                "datasetpath": "/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/Winter10-START39_V8-v2/AODSIM",
                "number_of_jobs": 15,
            }
        },
    },
    # "TToBLNu_s-channel": {
    #     "dataVersion": 
    #     "crossSection": 0.99,
    #     "data": {
    #         "AOD": {
    #             "datasetpath":
    #             "number_of_jobs": 10, # Adjusted for PAT on the fly
    #         }
    #     },
    # },
    # "TToBLNu_t-channel": {
    #     "dataVersion":
    #     "crossSection": 63./3.,
    #     "data": {
    #         "AOD": {
    #             "datasetpath":
    #             "number_of_jobs": 10, # Adjusted for PAT on the fly
    #         }
    #     },
    # },
    # "TToBLNu_tW-channel": {
    #     "dataVersion":
    #     "crossSection": 10.56,
    #     "data": {
    #         "AOD": {
    #             "datasetpath":
    #             "number_of_jobs": 10, # Adjusted for PAT on the fly
    #         },
    #     },
    # },
}
