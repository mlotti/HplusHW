import multicrabDatasetsCommon as common

datasets = {
    # Single tau + MET
    "Tau_160404-161176_Prompt": {
        "dataVersion": "41Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_MET45_v1",
        "runs": (160404, 161176), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011A-PromptReco-v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 30, # Adjusted for PATtuple file size
                "lumiMask": "DCSOnly"
            },
            "pattuple_v10_test3": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v1_AOD_160404_pattuple_v10_test3-0afb79e1b4a9efb21952e294fbf97113/USER",
                "luminosity": 10.589643,
                "number_of_jobs": 2
            },
        }
    },
    "Tau_160431-161016_Prompt": {
        "dataVersion": "41Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_MET45_v1",
        "runs": (160431, 1611016), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011A-PromptReco-v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 30, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
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
            "pattuple_v10_test3": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v1_AOD_161216_pattuple_v10_test3-85ec5544f54122dfd23b7a7442771d8e/USER",
                "luminosity": 12.291216,
                "number_of_jobs": 2
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
                "number_of_jobs": 5, # Adjusted for PATtuple file size
                "lumiMask": "DCSOnly"
            },
            "pattuple_v10_test3": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TauPlusX/local-Run2011A_PromptReco_v1_AOD_160404_pattuple_v10_test3-7ca7b85da23747106d19bca56315fb4a/USER",
                "luminosity": 22.880859,
                "number_of_jobs": 1
            },
        }
    },
}
