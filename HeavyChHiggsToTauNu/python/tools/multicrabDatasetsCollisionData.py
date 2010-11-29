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
                "datasetpath": "/BTau/Run2010A-Nov4ReReco_v1/RECO",
                "luminosity": 0,
                "lumis_per_job": 50,
                "lumiMaskRequired": True
            },
            "AOD": {
                "datasetpath": "/BTau/Run2010A-Nov4ReReco_v1/AOD",
                "luminosity": 0,
                "lumis_per_job": 50, # Adjusted for PATtuple file size
                "lumiMaskRequired": True
            },
            "pattuple_v3": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/BTau/local-Run2010A_Sep17ReReco_v2_RECO-pattuple_v3_3-1a3cae4f0de91fe807e595c3536a6777/USER",
                "luminosity": 1.951264571,
                "number_of_jobs": 10
            },
            "pattuple_v6_1": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/BTau/local-Run2010A_Sep17ReReco_v2_RECO_pattuple_v6_1-b9b1bac3463fc5700035eeb83da514a6/USER",
                "luminosity": 2.139732871,
                "number_of_jobs": 10
            },
            "pattuple_v6_2": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/BTau/local-Run2010A_Sep17ReReco_v2_RECO_pattuple_v6_2-b9b1bac3463fc5700035eeb83da514a6/USER",
                "luminosity": 2.027848248,
                "number_of_jobs": 10
            },
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
                "datasetpath": "/BTau/Run2010B-Nov4ReReco_v1/RECO",
                "luminosity": 0,
                "lumis_per_job": 50, # Adjusted for PATtuple file size
                "lumiMaskRequired": True
            },
            "AOD": {
                "datasetpath": "/BTau/Run2010B-Nov4ReReco_v1/AOD",
                "luminosity": 0,
                "lumis_per_job": 50,
                "lumiMaskRequired": True
            },
            "pattuple_v6_1": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/BTau/local-Run2010B_PromptReco_v2_RECO_pattuple_v6_1-43c3132ebadd44967499e6cca288e3ab/USER",
                "luminosity": 5.899172590,
                "number_of_jobs": 10
            },
            "pattuple_v6_2": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/BTau/local-Run2010B_PromptReco_v2_RECO_pattuple_v6_2-43c3132ebadd44967499e6cca288e3ab/USER",
                "luminosity": 5.867011630,
                "number_of_jobs": 10
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
    "BTau_148108-148864": {
        "dataVersion": "38XdataRun2010B",
        "trigger": "HLT_SingleIsoTau20_Trk15_MET25_v3",
        "runs": (148108, 148864),
        "data": {
            "pattuple_v6_1": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/BTau/local-Run2010B_PromptReco_v2_RECO_pattuple_v6_1-87e2c0e398f5cb72e5974e2df0c2a6a6/USER",
                "luminosity": 4.600225784,
                "number_of_jobs": 3
            },
            "pattuple_v6": {
                "fallback": "pattuple_v6_1"
            }
        },
    },
    "BTau_148108-149182": {
        "dataVersion": "38XdataRun2010B",
        "trigger": "HLT_SingleIsoTau20_Trk15_MET25_v3",
        "runs": (148108, 149182),
        "data": {
            "RECO": {
                "datasetpath": "/BTau/Run2010B-Nov4ReReco_v1/RECO",
                "luminosity": 0,
                "lumis_per_job": 15, # Adjusted for PATtuple file size
                "lumiMaskRequired": True
            },
            "AOD": {
                "datasetpath": "/BTau/Run2010B-Nov4ReReco_v1/AOD",
                "luminosity": 0,
                "lumis_per_job": 15,
                "lumiMaskRequired": True
            },
            "pattuple_v6_2": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/BTau/local-Run2010B_PromptReco_v2_RECO_pattuple_v6_2-87e2c0e398f5cb72e5974e2df0c2a6a6/USER",
                "luminosity": 13.821016530,
                "number_of_jobs": 10
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
    "BTau_149291-149442": {
        "dataVersion": "38XdataRun2010B",
        "trigger": "HLT_SingleIsoTau20_Trk15_MET25_v4",
        "runs": (149291, 149442),
        "data": {
            "RECO": {
                "datasetpath": "/BTau/Run2010B-Nov4ReReco_v1/RECO",
                "luminosity": 0,
                "lumis_per_job": 20, # Adjusted for PATtuple file size
                "lumiMaskRequired": True
            },
            "AOD": {
                "datasetpath": "/BTau/Run2010B-Nov4ReReco_v1/AOD",
                "luminosity": 0,
                "lumis_per_job": 20,
                "lumiMaskRequired": True
            },
            "pattuple_v6_2": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/BTau/local-Run2010B_PromptReco_v2_RECO_pattuple_v6_2-377aee71049a82c7ea12a489f5d5e3ef/USER",
                "luminosity": 2.131303202,
                "number_of_jobs": 2
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


    # Mu PD (for electroweak background analysis)
    "Mu_135821-144114": {
        "dataVersion": "38XdataRun2010A",
        "trigger": "HLT_Mu9",
        "data": {
            "RECO": {
                "datasetpath": "/Mu/Run2010A-Nov4ReReco_v1/RECO", # runs 135821-144114
                "luminosity": 0,
                "lumis_per_job": 500, # Adjusted for PAT on the fly
                "lumiMaskRequired": True
            },
            "AOD": {
                "datasetpath": "/Mu/Run2010A-Nov4ReReco_v1/AOD", # runs 135821-144114
                "luminosity": 0,
                "lumis_per_job": 500,
                "lumiMaskRequired": True
            }
        }
    },
    "Mu_146240-147116": {
        "dataVersion": "38XdataRun2010B",
        "trigger": "HLT_Mu9",
        "runs": (146240, 147116),
        "data": {
            "AOD": {
                "datasetpath": "/Mu/Run2010B-Nov4ReReco_v1/AOD",
                "luminosity": 0,
                "lumis_per_job": 600, # Adjusted for PAT on the fly
                "lumiMaskRequired": True
            }
        }
    },
    "Mu_147196-149442": {
        "dataVersion": "38XdataRun2010B",
        "trigger": "HLT_Mu15_v1",
        "runs": (147196, 149442),
        "data": {
            "AOD": {
                "datasetpath": "/Mu/Run2010B-Nov4ReReco_v1/AOD",
                "luminosity": 0,
                "lumis_per_job": 500, # Adjusted for PAT on the fly
                "lumiMaskRequired": True
            }
        }
    },
}
