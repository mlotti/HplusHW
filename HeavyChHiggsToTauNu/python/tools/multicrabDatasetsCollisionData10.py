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
            "pattuple_v9_1": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/BTau/local-Run2010A_Dec22ReReco_v1_AOD_141956_pattuple_v9_1-8fa92c7e2c071a3e7e6f47b50c02a015/USER",
                "luminosity": 2.846183931,
                "number_of_jobs": 30
            },
            "pattuple_v9": {
                "fallback": "pattuple_v9_1"
            },
            "pattuple_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/BTau/local-Run2010A_Dec22ReReco_v1_AOD_141956_pattuple_v11b-b20aa4dd1fd1c459fb67271e0123029e/USER",
                "luminosity": 2.846104,
                "number_of_jobs": 30
            },
        }
    },
    "BTau_146428-148058_Dec22": {
        "dataVersion": "39Xdata",
        "trigger": "HLT_SingleIsoTau20_Trk15_MET20",
        "runs": (146428, 148058), # The real range for this trigger (from Run Registry and the Dec22 JSON file)
        "data": {
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
            },
            "pattuple_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/BTau/local-Run2010B_Dec22ReReco_v1_AOD_146428_pattuple_v11b-75700c75be7f6a8374de48ec67ff8dc8/USER",
                "luminosity": 14.523250,
                "number_of_jobs": 20
            },
        }
    },
    "BTau_148822-149182_Dec22": {
        "dataVersion": "39Xdata",
        "trigger": "HLT_SingleIsoTau20_Trk15_MET25_v3",
        "runs": (148822, 149182), # The real range for this trigger (from Run Registry and the Dec22 JSON file)
        "data": {
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
            "pattuple_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/BTau/local-Run2010B_Dec22ReReco_v1_AOD_148822_pattuple_v11b-43988546d882e8b92cda5441042504d2/USER",
                "luminosity": 16.084022,
                "number_of_jobs": 10
            },
        }
    },
    "BTau_149291-149294_Dec22": {
        "dataVersion": "39Xdata",
        "trigger": "HLT_SingleIsoTau20_Trk15_MET25_v4",
        "runs": (149291, 149294), # The real range for this trigger (from Run Registry and the Dec22 JSON file)
        "data": {
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
            "pattuple_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/BTau/local-Run2010B_Dec22ReReco_v1_AOD_149291_pattuple_v11b-23a75132a46243066ab1a7d1af0bcffa/USER",
                "luminosity": 2.270373,
                "number_of_jobs": 2
            },
        }
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


    # Mu PD (for electroweak background analysis)
    "Mu_136035-144114_Dec22": {
        "dataVersion": "39Xdata",
        "trigger": "HLT_Mu9",
        "runs": (136035, 144114), # The real range for this trigger (from Run Registry and the Dec22 JSON file)
        "data": {
        }
    },
    "Mu_146428-147116_Dec22": {
        "dataVersion": "39Xdata",
        "trigger": "HLT_Mu9",
        "runs": (146428, 147116), # The real range for this trigger (from Run Registry and the Dec22 JSON file)
        "data": {
        }
    },
    "Mu_147196-149294_Dec22": {
        "dataVersion": "39Xdata",
        "trigger": "HLT_Mu15_v1",
        "runs": (147196, 149294), # The real range for this trigger (from Run Registry and the Dec22 JSON file)
        "data": {
        }
    },
}
