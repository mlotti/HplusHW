import multicrabDatasetsCommon as common

datasets = {
    # Single tau
    "Tau_160404-161176_Prompt": {
        "dataVersion": "41Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_MET45_v1",
        "runs": (160404, 161176), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011A-PromptReco-v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 60, # Adjusted for PATtuple file size
                "lumiMask": "DCSOnly"
            },
        }
    },
    "Tau_161216-161312_Prompt": {
        "dataVersion": "41Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_MET45_v2",
        "runs": (161216, 161312), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011A-PromptReco-v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 20, # Adjusted for PATtuple file size
                "lumiMask": "DCSOnly"
            },
        }
    },

    # Tau + jets
    "TauPlusX_160404-161312_Prompt": {
        "dataVersion": "41Xdata",
        "trigger": "HLT_QuadJet40_IsoPFTau40_v1",
        "runs": (160404, 161312), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/TauPlusX/Run2011A-PromptReco-v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 100, # Adjusted for PATtuple file size
                "lumiMask": "DCSOnly"
            },
        }
    },
}
