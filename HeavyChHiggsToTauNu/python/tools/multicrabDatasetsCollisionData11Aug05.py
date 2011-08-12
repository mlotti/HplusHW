import multicrabDatasetsCommon as common

datasets = {
    # Single tau + MET
    "Tau_170826-172619_Aug05": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_MET60_v6",
        "runs": (170826, 172619),
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011A-05Aug2011-v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 80, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
        }
    },

    # Single tau (control)
    "Tau_Single_170826-172619_Aug05": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_v6",
        "runs": (170826, 172619),
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011A-05Aug2011-v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 80, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
        }
    },

    # Single Mu
    "SingleMu_170826-172619_Aug05": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_Mu40_v3",
        "runs": (170826, 172619),
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-05Aug2011-v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 80,
                "lumiMask": "PromptReco"
            },
        }
    },
}
