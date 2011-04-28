import multicrabDatasetsCommon as common

datasets = {
    ############################################################
    # Collision data
    #
    # BTau PD (for signal analysis)
    "JetMETTau_Tau_136035-139975_Dec22": {
        "dataVersion": "39Xdata",
        "trigger": "HLT_SingleLooseIsoTau20",
        "runs": (136035, 139975), # The real range for this trigger (from Run Registry and the Dec22 JSON file)
        "data": {
            "AOD": {
                "datasetpath": "/JetMETTau/Run2010A-Dec22ReReco_v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 300, # Adjusted for PATtuple file size
                "lumiMask": "Dec22ReReco"
            },
            "pattuple_v9_1": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/JetMETTau/local-Run2010A_Dec22ReReco_v1_AOD_Tau_pattuple_v9_1-4e2fa0cbfe0cf1221a0673f448298393/USER",
                "luminosity": 0.085524691,
                "number_of_jobs": 4
            },
            "pattuple_v9": {
                "fallback": "pattuple_v9_1"
            }
        }
    },
    "JetMETTau_Tau_140058-141881_Dec22": {
        "dataVersion": "39Xdata",
        "trigger": "HLT_SingleLooseIsoTau20_Trk5",
        "runs": (140058, 141881), # The real range for this trigger (from Run Registry and the Dec22 JSON file)
        "data": {
            "AOD": {
                "datasetpath": "/JetMETTau/Run2010A-Dec22ReReco_v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 300, # Adjusted for PATtuple file size
                "lumiMask": "Dec22ReReco"
            },
            "pattuple_v9_1": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/JetMETTau/local-Run2010A_Dec22ReReco_v1_AOD_Tau_pattuple_v9_1-7b621476048eefc450e74b1a3fe9ad51/USER",
                "luminosity": 0.198967175,
                "number_of_jobs": 6
            },
            "pattuple_v9": {
                "fallback": "pattuple_v9_1"
            }
        }
    },
    "BTau_141956-144114_Dec22": {
        "dataVersion": "39Xdata",
        "trigger": "HLT_SingleIsoTau20_Trk5",
        "runs": (141956, 144114), # The real range for this trigger (from Run Registry and the Dec22 JSON file)
        "data": {
            "AOD": {
                "datasetpath": "/BTau/Run2010A-Dec22ReReco_v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 1000, # Adjusted for PATtuple file size
                "use_server": 1,
                "lumiMask": "Dec22ReReco"
            },
            "pattuple_v9_1": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/BTau/local-Run2010A_Dec22ReReco_v1_AOD_141956_pattuple_v9_1-8fa92c7e2c071a3e7e6f47b50c02a015/USER",
                "luminosity": 2.846183931,
                "number_of_jobs": 30
            },
            "pattuple_v9": {
                "fallback": "pattuple_v9_1"
            }
        }
    },
    "BTau_146428-148058_Dec22": {
        "dataVersion": "39Xdata",
        "trigger": "HLT_SingleIsoTau20_Trk15_MET20",
        "runs": (146428, 148058), # The real range for this trigger (from Run Registry and the Dec22 JSON file)
        "data": {
            "AOD": {
                "datasetpath": "/BTau/Run2010B-Dec22ReReco_v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 490, # Adjusted for PATtuple file size
                "lumiMask": "Dec22ReReco"
            },
            "pattuple_v9_1": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/BTau/local-Run2010B_Dec22ReReco_v1_AOD_146428_pattuple_v9-3a013f41a0c4ff6fc1143af634d9ef19/USER",
                "luminosity": 14.484590862,
                "number_of_jobs": 20
            },
            "pattuple_v9": {
                "fallback": "pattuple_v9_1"
            },
            "pattuple_v10_1": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/BTau/local-Run2010B_Dec22ReReco_v1_AOD_146428_pattuple_v10_1b-c4ea815147b859c202ad50a9425ec5e1/USER",
                "luminosity": 14.448978,
                "number_of_jobs": 20
            },
            "pattuple_v10": {
                "fallback": "pattuple_v10_1"
            }
        }
    },
    "BTau_148822-149182_Dec22": {
        "dataVersion": "39Xdata",
        "trigger": "HLT_SingleIsoTau20_Trk15_MET25_v3",
        "runs": (148822, 149182), # The real range for this trigger (from Run Registry and the Dec22 JSON file)
        "data": {
            "AOD": {
                "datasetpath": "/BTau/Run2010B-Dec22ReReco_v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 450, # Adjusted for PATtuple file size
                "lumiMask": "Dec22ReReco"
            },
            "pattuple_v9_1": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/BTau/local-Run2010B_Dec22ReReco_v1_AOD_148822_pattuple_v9-9bdd93eeac3a09280bc73f406326390f/USER",
                "luminosity": 16.084022481,
                "number_of_jobs": 10
            },
            "pattuple_v9": {
                "fallback": "pattuple_v9_1"
            },
            "pattuple_v10_1": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/BTau/local-Run2010B_Dec22ReReco_v1_AOD_148822_pattuple_v10_1b-825f9f3a2228e308bb923d3925115592/USER",
                "luminosity": 16.084022,
                "number_of_jobs": 10
            },
            "pattuple_v10": {
                "fallback": "pattuple_v10_1"
            },
        }
    },
    "BTau_149291-149294_Dec22": {
        "dataVersion": "39Xdata",
        "trigger": "HLT_SingleIsoTau20_Trk15_MET25_v4",
        "runs": (149291, 149294), # The real range for this trigger (from Run Registry and the Dec22 JSON file)
        "data": {
            "AOD": {
                "datasetpath": "/BTau/Run2010B-Dec22ReReco_v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 60, # Adjusted for PATtuple file size
                "lumiMask": "Dec22ReReco"
            },
            "pattuple_v9_1": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/BTau/local-Run2010B_Dec22ReReco_v1_AOD_149291_pattuple_v9-46b2fb8e054eedee742fb578c3681cd6/USER",
                "luminosity": 2.270373344,
                "number_of_jobs": 2
            },
            "pattuple_v9": {
                "fallback": "pattuple_v9_1"
            },
            "pattuple_v10_1": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/BTau/local-Run2010B_Dec22ReReco_v1_AOD_149291_pattuple_v10_1b-79566228a8278608a71cc48012464cce/USER",
                "luminosity": 2.270373,
                "number_of_jobs": 2
            },
            "pattuple_v10": {
                "fallback": "pattuple_v10_1"
            },
        }
    },

    "BTau_141950-144114_Nov4": {
        "dataVersion": "38Xdata",
        "trigger": "HLT_SingleIsoTau20_Trk5",
        "data": {
            "pattuple_v6_3": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/BTau/local-Run2010A_Nov4ReReco_v1_RECO_pattuple_v6_3-dfc6d27ce5aa60b808b4a2bcd34b7c86/USER",
                "luminosity": 2.799065107,
                "number_of_jobs": 20
            },
            "pattuple_v6": {
                "fallback": "pattuple_v6_3"
            }
        }

    },
    "BTau_146240-148107_Nov4": {
        "dataVersion": "38Xdata",
        "trigger": "HLT_SingleIsoTau20_Trk15_MET20",
        "runs": (146240, 148107),
        "data": {
            "RECO": {
                "datasetpath": "/BTau/Run2010B-Nov4ReReco_v1/RECO",
                "luminosity": 0,
                "lumis_per_job": 50, # Adjusted for PATtuple file size
                "lumiMask": "Nov4ReReco"
            },
            "AOD": {
                "datasetpath": "/BTau/Run2010B-Nov4ReReco_v1/AOD",
                "luminosity": 0,
                "lumis_per_job": 50,
                "lumiMask": "Nov4ReReco"
            },
            "pattuple_v6_3": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/BTau/local-Run2010B_Nov4ReReco_v1_RECO_pattuple_v6_3-ba8b03606ed700d03389442a6378453f/USER",
                "luminosity": 14.527814041,
                "number_of_jobs": 20
            },
            "pattuple_v6": {
                "fallback": "pattuple_v6_3"
            }
        },
    },
    "BTau_148108-149182_Nov4": {
        "dataVersion": "38Xdata",
        "trigger": "HLT_SingleIsoTau20_Trk15_MET25_v3",
        "runs": (148108, 149182),
        "data": {
            "RECO": {
                "datasetpath": "/BTau/Run2010B-Nov4ReReco_v1/RECO",
                "luminosity": 0,
                "lumis_per_job": 15, # Adjusted for PATtuple file size
                "lumiMask": "Nov4ReReco"
            },
            "AOD": {
                "datasetpath": "/BTau/Run2010B-Nov4ReReco_v1/AOD",
                "luminosity": 0,
                "lumis_per_job": 15,
                "lumiMask": "Nov4ReReco"
            },
            "pattuple_v6_3": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/BTau/local-Run2010B_Nov4ReReco_v1_RECO_pattuple_v6_3-9e6b3ce3f61ebd1c080721235dd644e5/USER",
                "luminosity": 16.166113934,
                "number_of_jobs": 10
            },
            "pattuple_v6": {
                "fallback": "pattuple_v6_3"
            }
        },
    },
    "BTau_149291-149442_Nov4": {
        "dataVersion": "38Xdata",
        "trigger": "HLT_SingleIsoTau20_Trk15_MET25_v4",
        "runs": (149291, 149442),
        "data": {
            "RECO": {
                "datasetpath": "/BTau/Run2010B-Nov4ReReco_v1/RECO",
                "luminosity": 0,
                "lumis_per_job": 20, # Adjusted for PATtuple file size
                "lumiMask": "Nov4ReReco"
            },
            "AOD": {
                "datasetpath": "/BTau/Run2010B-Nov4ReReco_v1/AOD",
                "luminosity": 0,
                "lumis_per_job": 20,
                "lumiMask": "Nov4ReReco"
            },
            "pattuple_v6_3": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/BTau/local-Run2010B_Nov4ReReco_v1_RECO_pattuple_v6_3-ae876897d946fa7a17cf73f63fd66244/USER",
                "luminosity": 2.270540967,
                "number_of_jobs": 2
            },
            "pattuple_v6": {
                "fallback": "pattuple_v6_3"
            }
        },
    },

    # Jet PD (for QCD background analysis"
    "JetMETTau_Jet_136035-141881_Dec22": {
        "dataVersion": "39Xdata",
        "trigger": "HLT_Jet30U",
        "runs": (136035, 141881), # The real range for this trigger (from Run Registry and the Dec22 JSON file)
        "data": {
            "AOD": {
                "datasetpath": "/JetMETTau/Run2010A-Dec22ReReco_v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 100, # Adjusted for PATtuple
                "lumiMask": "Dec22ReReco"
            },
            "pattuple_v9_1": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/JetMETTau/local-Run2010A_Dec22ReReco_v1_AOD_Jet_pattuple_v9_1-7530ef6ad2e2f18191ca644614b1b027/USER",
                "luminosity": .284491865,
                "number_of_jobs": 10
            },
            "pattuple_v9": {
                "fallback": "pattuple_v9_1"
            }
        }
    },
    "JetMET_141956-144114_Dec22": {
        "dataVersion": "39Xdata",
        "trigger": "HLT_Jet30U",
        "runs": (141956, 144114), # The real range for this trigger (from Run Registry and the Dec22 JSON file)
        "data": {
            "AOD": {
                "datasetpath": "/JetMET/Run2010A-Dec22ReReco_v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 300, # Adjusted for PATtuple
                "lumiMask": "Dec22ReReco"
            },
            "pattuple_v9_1": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/JetMET/local-Run2010A_Dec22ReReco_v1_AOD_141956_pattuple_v9_1-7530ef6ad2e2f18191ca644614b1b027/USER",
                "luminosity": 2.846183931,
                "number_of_jobs": 20
            },
            "pattuple_v9": {
                "fallback": "pattuple_v9_1"
            }
        }
    },
    "Jet_146428-148058_Dec22": {
        "dataVersion": "39Xdata",
        "trigger": "HLT_Jet30U",
        "runs": (146428, 148058), # The real range for this trigger (from Run Registry and the Dec22 JSON file)
        "data": {
            "AOD": {
                "datasetpath": "/Jet/Run2010B-Dec22ReReco_v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 40, # Adjusted for PATtuple
                "lumiMask": "Dec22ReReco"
            },
            "pattuple_v9_1": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Jet/local-Run2010B_Dec22ReReco_v1_AOD_146428_pattuple_v9_1-7530ef6ad2e2f18191ca644614b1b027/USER",
                "luminosity": 14.517746074,
                "number_of_jobs": 2
            },
            "pattuple_v9": {
                "fallback": "pattuple_v9_1"
            }
        }
    },
    "Jet_148822-149294_Dec22": {
        "dataVersion": "39Xdata",
        "trigger": "HLT_Jet30U_v3",
        "runs": (148822, 149294), # The real range for this trigger (from Run Registry and the Dec22 JSON file)
        "data": {
            "AOD": {
                "datasetpath": "/Jet/Run2010B-Dec22ReReco_v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 20, # Adjusted for PATtuple
                "lumiMask": "Dec22ReReco"
            },
            "pattuple_v9_1": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Jet/local-Run2010B_Dec22ReReco_v1_AOD_148822_pattuple_v9_1-f27709779cfd23143641ea67ab8bfc68/USER",
                "luminosity": 18.435676673,
                "number_of_jobs": 1
            },
            "pattuple_v9": {
                "fallback": "pattuple_v9_1"
            }
        }
    },

    "JetMETTau_136033-141887_Nov4": { # first run actually 135821, but lumi list starts from this one
        "dataVersion": "38Xdata",
        "trigger": "HLT_Jet30U",
        "data": {
            "RECO": {
                "datasetpath": "/JetMETTau/Run2010A-Nov4ReReco_v1/RECO",
                "luminosity": 0,
                "number_of_jobs": 100, # Adjusted for PATtuple
                "lumiMask": "Nov4ReReco"
            },
            "pattuple_v6_4": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/JetMETTau/local-Run2010A_Nov4ReReco_v1_RECO_pattuple_v6_4-4c46839dc2dbfe33eac25fb0510aaca6/USER",
                "luminosity": .284734728,
                "number_of_jobs": 10 # 1.7M events
            },
            "pattuple_v6": {
                "fallback": "pattuple_v6_4"
            }
        }
    },
    "JetMET_141950-144114_Nov4": {
        "dataVersion": "38Xdata",
        "trigger": "HLT_Jet30U",
        "data": {
            "RECO": {
                "datasetpath": "/JetMET/Run2010A-Nov4ReReco_v1/RECO",
                "luminosity": 0,
                "number_of_jobs": 300, # Adjusted for PATtuple
                "lumiMask": "Nov4ReReco"
            },
            "pattuple_v6_4": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/JetMET/local-Run2010A_Nov4ReReco_v1_RECO_pattuple_v6_4-4c46839dc2dbfe33eac25fb0510aaca6/USER",
                "luminosity": 2.895797321,
                "number_of_jobs": 20 # 2.9M events
            },
            "pattuple_v6": {
                "fallback": "pattuple_v6_4"
            }
        }
    },
    "Jet_146240-148058_Nov4": { # last run really 149442, but last run with HLT_Jet30U is this one
        "dataVersion": "38Xdata",
        "trigger": "HLT_Jet30U",
        "runs": (146240, 148058),
        "data": {
            "RECO": {
                "datasetpath": "/Jet/Run2010B-Nov4ReReco_v1/RECO",
                "luminosity": 0,
                "number_of_jobs": 40, # Adjusted for PATtuple
                "lumiMask": "Nov4ReReco"
            },
            "pattuple_v6_4": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Jet/local-Run2010B_Nov4ReReco_v1_RECO_pattuple_v6_4-4c46839dc2dbfe33eac25fb0510aaca6/USER",
                "luminosity": 14.527814041,
                "number_of_jobs": 4
            },
            "pattuple_v6": {
                "fallback": "pattuple_v6_4"
            }
        }
    },

    # For QyadJet trigger
    "JetMETTau_QuadJet_136035-141881_Dec22": {
        "dataVersion": "39Xdata",
        "trigger": "HLT_QuadJet15U",
        "runs": (136035, 141881), # The real range for this trigger (from Run Registry and the Dec22 JSON file)
        "data": {
            "AOD": {
                "datasetpath": "/JetMETTau/Run2010A-Dec22ReReco_v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 50, # Adjusted for PATtuple
                "lumiMask": "Dec22ReReco"
            },
        }
    },
    "JetMET_QuadJet_141956-144114_Dec22": {
        "dataVersion": "39Xdata",
        "trigger": "HLT_QuadJet15U",
        "runs": (141956, 144114), # The real range for this trigger (from Run Registry and the Dec22 JSON file)
        "data": {
            "AOD": {
                "datasetpath": "/JetMET/Run2010A-Dec22ReReco_v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 50, # Adjusted for PATtuple
                "lumiMask": "Dec22ReReco"
            },
        }
    },
    "Jet_QuadJet_146428-147116_Dec22": {
        "dataVersion": "39Xdata",
        "trigger": "HLT_QuadJet25U",
        "runs": (146428, 147116), # The real range for this trigger (from Run Registry and the Dec22 JSON file)
        "data": {
            "AOD": {
                "datasetpath": "/Jet/Run2010B-Dec22ReReco_v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 40, # Adjusted for PATtuple
                "lumiMask": "Dec22ReReco"
            },
        }
    },
    "MultiJet_QuadJet_147196-148058_Dec22": {
        "dataVersion": "39Xdata",
        "trigger": "HLT_QuadJet25U_v2",
        "runs": (147196, 148058), # The real range for this trigger (from Run Registry and the Dec22 JSON file)
        "data": {
            "AOD": {
                "datasetpath": "/MultiJet/Run2010B-Dec22ReReco_v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 40, # Adjusted for PATtuple
                "lumiMask": "Dec22ReReco"
            },
        }
    },
    "MultiJet_QuadJet_148819-149442_Dec22": {
        "dataVersion": "39Xdata",
        "trigger": "HLT_QuadJet25U_v3",
        "runs": (148819, 149442), # The real range for this trigger (from Run Registry and the Dec22 JSON file)
        "data": {
            "AOD": {
                "datasetpath": "/MultiJet/Run2010B-Dec22ReReco_v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 40, # Adjusted for PATtuple
                "lumiMask": "Dec22ReReco"
            },
        }
    },


    # For QuadJet trigger
    "JetMETTau_QuadJet_136035-141881_Dec22": {
        "dataVersion": "39Xdata",
        "trigger": "HLT_QuadJet15U",
        "runs": (136035, 141881), # The real range for this trigger (from Run Registry and the Dec22 JSON file)
        "data": {
            "AOD": {
                "datasetpath": "/JetMETTau/Run2010A-Dec22ReReco_v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 20, # Adjusted for PATtuple
                "lumiMask": "Dec22ReReco"
            },
        }
    },
    "JetMET_QuadJet_141956-144114_Dec22": {
        "dataVersion": "39Xdata",
        "trigger": "HLT_QuadJet15U",
        "runs": (141956, 144114), # The real range for this trigger (from Run Registry and the Dec22 JSON file)
        "data": {
            "AOD": {
                "datasetpath": "/JetMET/Run2010A-Dec22ReReco_v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 200, # Adjusted for PATtuple
                "lumiMask": "Dec22ReReco"
            },
        }
    },
    "Jet_QuadJet_146428-147116_Dec22": {
        "dataVersion": "39Xdata",
        "trigger": "HLT_QuadJet25U",
        "runs": (146428, 147116), # The real range for this trigger (from Run Registry and the Dec22 JSON file)
        "data": {
            "AOD": {
                "datasetpath": "/Jet/Run2010B-Dec22ReReco_v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 40, # Adjusted for PATtuple
                "lumiMask": "Dec22ReReco"
            },
        }
    },
    "MultiJet_QuadJet_147196-148058_Dec22": {
        "dataVersion": "39Xdata",
        "trigger": "HLT_QuadJet25U_v2",
        "runs": (147196, 148058), # The real range for this trigger (from Run Registry and the Dec22 JSON file)
        "data": {
            "AOD": {
                "datasetpath": "/MultiJet/Run2010B-Dec22ReReco_v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 80, # Adjusted for PATtuple
                "lumiMask": "Dec22ReReco"
            },
        }
    },
    "MultiJet_QuadJet_148819-149442_Dec22": {
        "dataVersion": "39Xdata",
        "trigger": "HLT_QuadJet25U_v3",
        "runs": (148819, 149442), # The real range for this trigger (from Run Registry and the Dec22 JSON file)
        "data": {
            "AOD": {
                "datasetpath": "/MultiJet/Run2010B-Dec22ReReco_v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 100, # Adjusted for PATtuple
                "lumiMask": "Dec22ReReco"
            },
        }
    },


    # Mu PD (for electroweak background analysis)
    "Mu_135821-144114_Nov4": { # needed to keep tau embedding happy
        "dataVersion": "38Xdata",
        "trigger": "HLT_Mu9",
        "data": {}
    },
    "Mu_146240-147116_Nov4": { # needed to keep tau embedding happy
        "dataVersion": "38Xdata",
        "trigger": "HLT_Mu9",
        "data": {}
    },
    "Mu_147196-149442_Nov4": { # needed to keep tau embedding happy
        "dataVersion": "38Xdata",
        "trigger": "HLT_Mu15_v1",
        "data": {}
    },
    "Mu_136035-144114_Dec22": {
        "dataVersion": "39Xdata",
        "trigger": "HLT_Mu9",
        "runs": (136035, 144114), # The real range for this trigger (from Run Registry and the Dec22 JSON file)
        "data": {
            "AOD": {
                "datasetpath": "/Mu/Run2010A-Dec22ReReco_v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 80, # Adjusted for PAT on the fly
                "lumiMask": "Dec22ReReco"
            },
        }
    },
    "Mu_146428-147116_Dec22": {
        "dataVersion": "39Xdata",
        "trigger": "HLT_Mu9",
        "runs": (146428, 147116), # The real range for this trigger (from Run Registry and the Dec22 JSON file)
        "data": {
            "AOD": {
                "datasetpath": "/Mu/Run2010B-Dec22ReReco_v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 50, # Adjusted for PAT on the fly
                "lumiMask": "Dec22ReReco"
            },
        }
    },
    "Mu_147196-149294_Dec22": {
        "dataVersion": "39Xdata",
        "trigger": "HLT_Mu15_v1",
        "runs": (147196, 149294), # The real range for this trigger (from Run Registry and the Dec22 JSON file)
        "data": {
            "AOD": {
                "datasetpath": "/Mu/Run2010B-Dec22ReReco_v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 50, # Adjusted for PAT on the fly
                "lumiMask": "Dec22ReReco"
            },
        }
    },
}
