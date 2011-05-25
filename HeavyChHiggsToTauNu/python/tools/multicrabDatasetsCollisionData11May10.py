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
                "number_of_jobs": 80, # Adjusted for PATtuple file size
                "lumiMask": "May10ReReco"
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
                "number_of_jobs": 200,
                "lumiMask": "May10ReReco"
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
