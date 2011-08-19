import multicrabDatasetsCommon as common

datasets = {
    # Single tau + MET
    "Tau_170722-172619_Aug05": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_MET60_v6",
        "runs": (170722, 172619),
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011A-05Aug2011-v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 110, # Adjusted for PATtuple file size
                "lumiMask": "Aug05ReReco"
            },
        }
    },

    # Single tau (control)
    "Tau_Single_170722-172619_Aug05": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_v6",
        "runs": (170722, 172619),
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011A-05Aug2011-v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 110, # Adjusted for PATtuple file size
                "lumiMask": "Aug05ReReco"
            },
        }
    },

    # Single Mu
    "SingleMu_170722-172619_Aug05": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_Mu40_v3",
        "runs": (170722, 172619),
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-05Aug2011-v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 110,
                "lumiMask": "Aug05ReReco"
            },
        }
    },
}
