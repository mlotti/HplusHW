import multicrabDatasetsCommon as common

datasets = {
    ############################################################
    # Collision data
    #
    # BTau PD (for signal analysis)
    "BTau_141950-144114": {
        "dataVersion": "38XdataRun2010A",
        "trigger": "HLT_SingleIsoTau20_Trk5",
        "data": {
            "RECO": {
                "datasetpath": "/BTau/Run2010A-Sep17ReReco_v2/RECO",
                #"datasetpath": "/BTau/Run2010A-Nov4ReReco_v1/RECO",
                "luminosity": 0,
                "lumis_per_job": 100, # Adjusted for PATtuple file size
                "lumiMaskRequired": True
            },
            "AOD": {
                "fallback": "RECO",
                #"datasetpath": "/BTau/Run2010A-Nov4ReReco_v1/AOD",
            },
            "pattuple_v3": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/BTau/local-Run2010A_Sep17ReReco_v2_RECO-pattuple_v3_3-1a3cae4f0de91fe807e595c3536a6777/USER",
                "luminosity": 1.951264571,
                "number_of_jobs": 5
            },
            "pattuple_v6": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/BTau/local-Run2010A_Sep17ReReco_v2_RECO_pattuple_v6_1-b9b1bac3463fc5700035eeb83da514a6/USER",
                "luminosity": 2.139732871,
                "number_of_jobs": 5
            }
        }

    },
    "BTau_146240-147454": {
        "dataVersion": "38XdataRun2010B",
        "trigger": "HLT_SingleIsoTau20_Trk15_MET20",
        "runs": (146240, 147454),
        "data": {
            "pattuple_v3": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/BTau/local-Run2010B_PromptReco_V2_RECO-pattuple_v3_3-ca0cc7472f6f10c326285176dfa5387f/USER",
                "luminosity": 7.390799812,
                "number_of_jobs": 5
            }
        },
    },
    "BTau_146240-148107": {
        "dataVersion": "38XdataRun2010B",
        "trigger": "HLT_SingleIsoTau20_Trk15_MET20",
        "runs": (146240, 148107),
        "data": {
            "RECO": {
                "datasetpath": "/BTau/Run2010B-PromptReco-v2/RECO",
                "luminosity": 0,
                "lumis_per_job": 100, # Adjusted for PATtuple file size
                "lumiMaskRequired": True
            },
            "AOD": {
                "fallback": "RECO",
            },
            "pattuple_v6": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/BTau/local-Run2010B_PromptReco_v2_RECO_pattuple_v6_1-43c3132ebadd44967499e6cca288e3ab/USER",
                "luminosity": 5.899172590,
                "number_of_jobs": 10
            }
        },
    },
    "BTau_148108-148864": {
        "dataVersion": "38XdataRun2010B",
        "trigger": "HLT_SingleIsoTau20_Trk15_MET25_v3",
        "runs": (148108, 148864),
        "data": {
            "pattuple_v6": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/BTau/local-Run2010B_PromptReco_v2_RECO_pattuple_v6_1-87e2c0e398f5cb72e5974e2df0c2a6a6/USER",
                "luminosity": 4.600225784,
                "number_of_jobs": 3
            }
        },
    },
    "BTau_148108-149182": {
        "dataVersion": "38XdataRun2010B",
        "trigger": "HLT_SingleIsoTau20_Trk15_MET25_v3",
        "runs": (148108, 149182),
        "data": {
            "RECO": {
                "datasetpath": "/BTau/Run2010B-PromptReco-v2/RECO",
                "luminosity": 0,
                "lumis_per_job": 30, # Adjusted for PATtuple file size
                "lumiMaskRequired": True
            },
            "AOD": {
                "fallback": "RECO",
            }
        },
    },
    "BTau_149291-149442": {
        "dataVersion": "38XdataRun2010B",
        "trigger": "HLT_SingleIsoTau20_Trk15_MET25_v4",
        "runs": (149291, 149442),
        "data": {
            "RECO": {
                "datasetpath": "/BTau/Run2010B-PromptReco-v2/RECO",
                "luminosity": 0,
                "lumis_per_job": 30, # Adjusted for PATtuple file size
                "lumiMaskRequired": True
            },
            "AOD": {
                "fallback": "RECO",
            }
        },
    },


    # Mu PD (for electroweak background analysis)
    "Mu_135821-144114": {
        "dataVersion": "38XdataRun2010A",
        "trigger": "HLT_Mu9",
        "data": {
            "RECO": {
                "datasetpath": "/Mu/Run2010A-Sep17ReReco_v2/RECO",
                "luminosity": 0,
                "lumis_per_job": 500, # Adjusted for PAT on the fly
                "lumiMaskRequired": True
            },
            "AOD": {
                "fallback": "RECO",
            }
        }
    },
    "Mu_146240-147116": {
        "dataVersion": "38XdataRun2010B",
        "trigger": "HLT_Mu9",
        "runs": (146240, 147116),
        "data": {
            "AOD": {
                "datasetpath": "/Mu/Run2010B-PromptReco-v2/AOD",
                "luminosity": 0,
                "lumis_per_job": 600, # Adjusted for PAT on the fly
                "lumiMaskRequired": True
            }
        }
    },
    "Mu_147196-148058": {
        "dataVersion": "38XdataRun2010B",
        "trigger": "HLT_Mu15_v1",
        "runs": (147116, 148058),
        "data": {
            "AOD": {
                "datasetpath": "/Mu/Run2010B-PromptReco-v2/AOD",
                "luminosity": 0,
                "lumis_per_job": 500, # Adjusted for PAT on the fly
                "lumiMaskRequired": True
            }
        }
    },
}
