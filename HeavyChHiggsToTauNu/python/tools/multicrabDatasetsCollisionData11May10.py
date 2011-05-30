import multicrabDatasetsCommon as common

datasets = {
    # Single tau + MET
    "Tau_160404-161176_May10": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_MET45_v1",
        "runs": (0, 0), #
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011A-May10ReReco-v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 15, # Adjusted for PATtuple file size
                "lumiMask": "May10ReReco"
            },
        }
    },
    "Tau_161216-163261_May10": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_MET45_v2",
        "runs": (0, 163261),
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011A-May10ReReco-v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 80, # Adjusted for PATtuple file size
                "lumiMask": "May10ReReco"
            },
        },
    },
    "Tau_163269-?_May10": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_MET45_v4",
        "runs": (0, 0),
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
    "SingleMu_160404-163261_May10": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_Mu20_v1",
        "runs": (0, 0),
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-May10ReReco-v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 60, # Adjusted for PATtuple file size
                "lumiMask": "May10ReReco"
            },
        }
    },
    "SingleMu_163269-?_May10": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_Mu24_v2",
        "runs": (0, 0),
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
