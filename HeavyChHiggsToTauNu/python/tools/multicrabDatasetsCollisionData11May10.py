import multicrabDatasetsCommon as common

datasets = {
    # Single tau + MET
    "Tau_160431-161176_May10": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_MET45_v1",
        "runs": (160431, 161176), #
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011A-May10ReReco-v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 15, # Adjusted for PATtuple file size
                "lumiMask": "May10ReReco"
            },
            "pattuple_v13_test1": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_May10ReReco_v1_AOD_160431_pattuple_v13_test1-4b4a75d9ac041a0a4d66f94ae4d63d28/USER",
                "luminosity": 5.884518,
                "number_of_jobs": 1
            },
            "pattuple_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_May10ReReco_v1_AOD_160431_pattuple_v13-4b4a75d9ac041a0a4d66f94ae4d63d28/USER",
                "luminosity": 5.884518,
                "number_of_jobs": 1
            },
        }
    },
    "Tau_161217-163261_May10": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_MET45_v2",
        "runs": (161217, 163261),
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011A-May10ReReco-v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 100, # Adjusted for PATtuple file size
                "lumiMask": "May10ReReco"
            },
            "pattuple_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_May10ReReco_v1_AOD_161217_pattuple_v13-612b93c0d939e947e4b67c54ba0c3c1c/USER",
                "luminosity": 38.518306,
                "number_of_jobs": 2
            },
        },
    },
    "Tau_163270-163869_May10": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_MET45_v4",
        "runs": (163270, 163869),
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011A-May10ReReco-v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 220,
                "lumiMask": "May10ReReco"
            },
            "pattuple_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_May10ReReco_v1_AOD_163270_pattuple_v13-e8dac75be42860b9ddfa13bd162b3b7f/USER",
                "luminosity": 159.758105,
                "number_of_jobs": 6
            },
        }
    },

    # Single Mu
    "SingleMu_160431-163261_May10": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_Mu20_v1",
        "runs": (160431, 163261),
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-May10ReReco-v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 60, # Adjusted for PATtuple file size
                "lumiMask": "May10ReReco"
            },
        }
    },
    "SingleMu_163270-163869_May10": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_Mu24_v2",
        "runs": (163270, 163869),
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-May10ReReco-v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 40, # Adjusted for PATtuple file size
                "lumiMask": "May10ReReco"
            },
        },
    },
}
