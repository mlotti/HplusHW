import multicrabDatasetsCommon as common

datasets = {
    # Signal
    "TTToHplusBWB_M90_Winter10": {
        "dataVersion": "39Xredigi",
        "crossSection": 16.442915,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-90_7TeV-pythia6-tauola/Winter10-E7TeV_ProbDist_2010Data_BX156_START39_V8-v1/AODSIM",
                "number_of_jobs": 20,
            },
            "pattuple_v9": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-90_7TeV-pythia6-tauola/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_pattuple_v9-c2f22ab9ac43296d989acccdef834e2a/USER",
                "number_of_jobs": 1
            },
        }
    },
    "TTToHplusBWB_M100_Winter10": {
        "dataVersion": "39Xredigi",
        "crossSection": 14.057857,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-100_7TeV-pythia6-tauola/Winter10-E7TeV_ProbDist_2010Data_BX156_START39_V8-v1/AODSIM",
                "number_of_jobs": 20,
            },
            "pattuple_v9": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-100_7TeV-pythia6-tauola/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_pattuple_v9b-c2f22ab9ac43296d989acccdef834e2a/USER",
                "number_of_jobs": 1
            },
        }
    },
    "TTToHplusBWB_M120_Winter10": {
        "dataVersion": "39Xredigi",
        "crossSection": 8.984715,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Winter10-E7TeV_ProbDist_2010Data_BX156_START39_V8-v1/AODSIM",
                "number_of_jobs": 20,
            },
            "pattuple_v9": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-120_7TeV-pythia6-tauola/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_pattuple_v9-c2f22ab9ac43296d989acccdef834e2a/USER",
                "number_of_jobs": 1
            },
        }
    },
    "TTToHplusBWB_M140_Winter10": {
        "dataVersion": "39Xredigi",
        "crossSection": 4.223402,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-140_7TeV-pythia6-tauola/Winter10-E7TeV_ProbDist_2010Data_BX156_START39_V8-v1/AODSIM",
                "number_of_jobs": 20,
            },
            "pattuple_v9": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-140_7TeV-pythia6-tauola/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_pattuple_v9-c2f22ab9ac43296d989acccdef834e2a/USER",
                "number_of_jobs": 1
            },
        }
    },
    "TTToHplusBWB_M160_Winter10": {
        "dataVersion": "39Xredigi",
        "crossSection": 0.811493,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-160_7TeV-pythia6-tauola/Winter10-E7TeV_ProbDist_2010Data_BX156_START39_V8-v1/AODSIM",
                "number_of_jobs": 20,
            },
            "pattuple_v9": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-160_7TeV-pythia6-tauola/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_pattuple_v9b-c2f22ab9ac43296d989acccdef834e2a/USER",
                "number_of_jobs": 1
            },
        }
    },

    # QCD Winter10
    "QCD_Pt30to50_TuneZ2_Winter10": {
        "dataVersion": "39Xredigi",
        "crossSection": 5.312e+07,
        "data": {
            "AOD": {
                "datasetpath": "/QCD_Pt_30to50_TuneZ2_7TeV_pythia6/Winter10-E7TeV_ProbDist_2010Data_BX156_START39_V8-v1/AODSIM",
                "number_of_jobs": 450, # Adjusted for PATtuple file size
            },
            "pattuple_v9": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt_30to50_TuneZ2_7TeV_pythia6/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_pattuple_v9-c2f22ab9ac43296d989acccdef834e2a/USER",
                "number_of_jobs": 15
            },
        },
    },
    "QCD_Pt50to80_TuneZ2_Winter10": {
        "dataVersion":  "39Xredigi",
        "crossSection": 6.359e+06,
        "data": {
            "AOD": {
                "datasetpath": "/QCD_Pt_50to80_TuneZ2_7TeV_pythia6/Winter10-E7TeV_ProbDist_2010Data_BX156_START39_V8-v1/AODSIM",
                "number_of_jobs": 450,
            },
        },
    },
    "QCD_Pt80to120_TuneZ2_Winter10": {
        "dataVersion": "39Xredigi",
        "crossSection": 7.843e+05,
        "data": {
            "AOD": {
                "datasetpath": "/QCD_Pt_80to120_TuneZ2_7TeV_pythia6/Winter10-E7TeV_ProbDist_2010Data_BX156_START39_V8-v1/AODSIM",
                "number_of_jobs": 450, # Adjusted for PATtuple file size
            },
            "pattuple_v9": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt_80to120_TuneZ2_7TeV_pythia6/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_pattuple_v9-c2f22ab9ac43296d989acccdef834e2a/USER",
                "number_of_jobs": 15
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
            "pattuple_v9": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt_120to170_TuneZ2_7TeV_pythia6/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_pattuple_v9-c2f22ab9ac43296d989acccdef834e2a/USER",
                "number_of_jobs": 15
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
            "pattuple_v9": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt_170to300_TuneZ2_7TeV_pythia6/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_pattuple_v9-c2f22ab9ac43296d989acccdef834e2a/USER",
                "number_of_jobs": 15
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
            "pattuple_v9": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt_300to470_TuneZ2_7TeV_pythia6/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_pattuple_v9-c2f22ab9ac43296d989acccdef834e2a/USER",
                "number_of_jobs": 15
            },
        },
    },


    # Electroweak MadGraph
    "TTJets_TuneZ2_Winter10": {
        "dataVersion": "39Xredigi",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTJets_TuneZ2_7TeV-madgraph-tauola/Winter10-E7TeV_ProbDist_2010Data_BX156_START39_V8-v1/AODSIM",
                "number_of_jobs": 400,
            },
            "pattuple_v9": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTJets_TuneZ2_7TeV-madgraph-tauola/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_pattuple_v9-c2f22ab9ac43296d989acccdef834e2a/USER",
                "number_of_jobs": 6
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
            "pattuple_v9": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTJets_TuneD6T_7TeV-madgraph-tauola/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_pattuple_v9-c2f22ab9ac43296d989acccdef834e2a/USER",
                "number_of_jobs": 6
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
            "pattuple_v9": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/local-Winter10_START39_V8_v1_AODSIM_pattuple_v9-c2f22ab9ac43296d989acccdef834e2a/USER",
                "number_of_jobs": 60
            },
        },
    },
    "WJets_TuneZ2_Winter10": {
        "dataVersion": "39Xredigi",
        "crossSection": 24640,
        "data": {
            "AOD": {
                "datasetpath": "/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/Winter10-E7TeV_ProbDist_2011Flat_BX156_START39_V8-v1/AODSIM",
                "number_of_jobs": 1500, # Adjusted for PATtuple file
                                        # size. CRAB doesn't really
                                        # create this many jobs, but
                                        # the large number seems to be
                                        # needed to get enough jobs
                "use_server": 1,
            },
            "pattuple_v9": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/local-Winter10_E7TeV_ProbDist_2011Flat_BX156_START39_V8_v1_AODSIM_pattuple_v9-c2f22ab9ac43296d989acccdef834e2a/USER",
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
            "pattuple_v9": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WJetsToLNu_TuneD6T_7TeV-madgraph-tauola/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_pattuple_v9-c2f22ab9ac43296d989acccdef834e2a/USER",
                "number_of_jobs": 60
            },
        },
    },
    # Electroweak Alpgen
    "W2Jets_ptW0to100_TuneZ2_Winter10": {
        "dataVersion": "39Xredigi",
        "crossSection": 9.434e+02,
        "data": {
            "AOD": {
                "datasetpath": "/W2Jets_ptW-0to100_TuneZ2_7TeV-alpgen-tauola/Winter10-E7TeV_ProbDist_2010Data_BX156_START39_V8-v1/AODSIM",
                "number_of_jobs": 150, # Adjusted for PATtuple file size
            },
            "pattuple_v9": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/W2Jets_ptW-100to300_TuneZ2_7TeV-alpgen-tauola/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_pattuple_v9-c2f22ab9ac43296d989acccdef834e2a/USER",
                "number_of_jobs": 10
            },
        },
    },
    "W2Jets_ptW100to300_TuneZ2_Winter10": {
        "dataVersion": "39Xredigi",
        "crossSection": 6.718e+01,
        "data": {
            "AOD": {
                "datasetpath": "/W2Jets_ptW-100to300_TuneZ2_7TeV-alpgen-tauola/Winter10-E7TeV_ProbDist_2010Data_BX156_START39_V8-v1/AODSIM",
                "number_of_jobs": 150, # Adjusted for PATtuple file size
            },
            "pattuple_v9": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/W2Jets_ptW-100to300_TuneZ2_7TeV-alpgen-tauola/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_pattuple_v9-c2f22ab9ac43296d989acccdef834e2a/USER",
                "number_of_jobs": 8
            },
        },
    },
    "W3Jets_ptW0to100_TuneZ2_Winter10": {
        "dataVersion": "39Xredigi",
        "crossSection": 2.087e+02,
        "data": {
            "AOD": {
                "datasetpath": "/W3Jets_ptW-0to100_TuneZ2_7TeV-alpgen-tauola/Winter10-E7TeV_ProbDist_2010Data_BX156_START39_V8-v1/AODSIM",
                "number_of_jobs": 130, # Adjusted for PATtuple file size
            },
            "pattuple_v9": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/W3Jets_ptW-0to100_TuneZ2_7TeV-alpgen-tauola/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_pattuple_v9-c2f22ab9ac43296d989acccdef834e2a/USER",
                "number_of_jobs": 5
            },
        },
    },
    "W3Jets_ptW100to300_TuneZ2_Winter10": {
        "dataVersion": "39Xredigi",
        "crossSection": 3.243e+01,
        "data": {
            "AOD": {
                "datasetpath": "/W3Jets_ptW-100to300_TuneZ2_7TeV-alpgen-tauola/Winter10-E7TeV_ProbDist_2010Data_BX156_START39_V8-v1/AODSIM",
                "number_of_jobs": 30, # Adjusted for PATtuple file size
            },
            "pattuple_v9": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/W3Jets_ptW-100to300_TuneZ2_7TeV-alpgen-tauola/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_pattuple_v9-c2f22ab9ac43296d989acccdef834e2a/USER",
                "number_of_jobs": 2
            },
        },
    },
    "W4Jets_ptW0to100_TuneZ2_Winter10": {
        "dataVersion": "39Xredigi",
        "crossSection": 2.087e+02,
        "data": {
            "AOD": {
                "datasetpath": "/W4Jets_ptW-0to100_TuneZ2_7TeV-alpgen-tauola/Winter10-E7TeV_ProbDist_2010Data_BX156_START39_V8-v1/AODSIM",
                "number_of_jobs": 20, # Adjusted for PATtuple file size
            },
            "pattuple_v9": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/W4Jets_ptW-0to100_TuneZ2_7TeV-alpgen-tauola/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_pattuple_v9-c2f22ab9ac43296d989acccdef834e2a/USER",
                "number_of_jobs": 1
            },
        },
    },
    "W4Jets_ptW100to300_TuneZ2_Winter10": {
        "dataVersion": "39Xredigi",
        "crossSection": 1.138e+01,
        "data": {
            "AOD": {
                "datasetpath": "/W4Jets_ptW-100to300_TuneZ2_7TeV-alpgen-tauola/Winter10-E7TeV_ProbDist_2010Data_BX156_START39_V8-v1/AODSIM",
                "number_of_jobs": 15, # Adjusted for PATtuple file size
            },
            "pattuple_v9": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/W4Jets_ptW-100to300_TuneZ2_7TeV-alpgen-tauola/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_pattuple_v9-c2f22ab9ac43296d989acccdef834e2a/USER",
                "number_of_jobs": 1
            },
        },
    },


    # Backgrounds for electroweak background measurement (Fall10)
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
        "dataVersion": "39Xredigi",
        "crossSection": 2321,
        "data": {
            "AOD": {
                "datasetpath": "/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/Winter10-E7TeV_ProbDist_2010Data_BX156_START39_V8-v1/AODSIM",
                "number_of_jobs": 15,
            }
        },
    },
    "DYJetsToLL_TuneZ2_Winter10_noPU": { # Z+jets
        "dataVersion":" 39Xredigi",
        "crossSection": 2321,
        "data": {
            "AOD": {
                "datasetpath": "/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/Winter10-START39_V8-v2/AODSIM",
                "number_of_jobs": 15,
            }
        },
    },
    "TToBLNu_s-channel_Winter10": {
        "dataVersion": "39Xredigi",
        "crossSection": 0.99,
        "data": {
            "AOD": {
                "datasetpath": "/TToBLNu_TuneZ2_s-channel_7TeV-madgraph/Winter10-E7TeV_ProbDist_2010Data_BX156_START39_V8-v1/AODSIM",
                "number_of_jobs": 10, # Adjusted for PAT on the fly
            }
        },
    },
    "TToBLNu_t-channel_Winter10": {
        "dataVersion": "39Xredigi",
        "crossSection": 63./3.,
        "data": {
            "AOD": {
                "datasetpath": "/TToBLNu_TuneZ2_t-channel_7TeV-madgraph/Winter10-E7TeV_ProbDist_2010Data_BX156_START39_V8-v1/AODSIM",
                "number_of_jobs": 10, # Adjusted for PAT on the fly
            }
        },
    },
    "TToBLNu_tW-channel_Winter10": {
        "dataVersion": "39Xredigi",
        "crossSection": 10.56,
        "data": {
            "AOD": {
                "datasetpath": "/TToBLNu_TuneZ2_tW-channel_7TeV-madgraph/Winter10-E7TeV_ProbDist_2010Data_BX156_START39_V8-v1/AODSIM",
                "number_of_jobs": 10, # Adjusted for PAT on the fly
            },
        },
    },
}
