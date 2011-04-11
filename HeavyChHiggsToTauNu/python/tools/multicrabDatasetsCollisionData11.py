import multicrabDatasetsCommon as common

datasets = {
    # Single tau
    "Tau_160329-160853_Prompt": {
        "dataVersion": "41Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_MET45_v1",
        "runs": (160329, 160853), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011A-PromptReco-v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 1, # Adjusted for PATtuple file size
                "lumiMask": "?"
            },
        }
    },

    # Tau + jets
    "TauPlusX_160329-160853_Prompt": {
        "dataVersion": "41Xdata",
        "trigger": "HLT_QuadJet40_IsoPFTau40_v1",
        "runs": (160329, 160853), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/TauPlusX/Run2011A-PromptReco-v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 2, # Adjusted for PATtuple file size
                "lumiMask": "?"
            },
        }
    },
}
