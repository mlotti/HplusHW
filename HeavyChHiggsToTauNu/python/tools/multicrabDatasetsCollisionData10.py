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
        }
    },
    "JetMETTau_Tau_140058-141881_Dec22": {
        "dataVersion": "39Xdata",
        "trigger": "HLT_SingleLooseIsoTau20_Trk5",
        "runs": (140058, 141881), # The real range for this trigger (from Run Registry and the Dec22 JSON file)
        "data": {
        }
    },
    "BTau_141956-144114_Dec22": {
        "dataVersion": "39Xdata",
        "trigger": "HLT_SingleIsoTau20_Trk5",
        "runs": (141956, 144114), # The real range for this trigger (from Run Registry and the Dec22 JSON file)
        "data": {
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
        }
    },
    "JetMET_141956-144114_Dec22": {
        "dataVersion": "39Xdata",
        "trigger": "HLT_Jet30U",
        "runs": (141956, 144114), # The real range for this trigger (from Run Registry and the Dec22 JSON file)
        "data": {
        }
    },
    "Jet_146428-148058_Dec22": {
        "dataVersion": "39Xdata",
        "trigger": "HLT_Jet30U",
        "runs": (146428, 148058), # The real range for this trigger (from Run Registry and the Dec22 JSON file)
        "data": {
        }
    },
    "Jet_148822-149294_Dec22": {
        "dataVersion": "39Xdata",
        "trigger": "HLT_Jet30U_v3",
        "runs": (148822, 149294), # The real range for this trigger (from Run Registry and the Dec22 JSON file)
        "data": {
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
