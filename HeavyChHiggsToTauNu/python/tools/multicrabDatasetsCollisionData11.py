import multicrabDatasetsCommon as common

datasets = {
    # Single tau + MET
    "Tau_160404-161176_Prompt": {
        "dataVersion": "41Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_MET45_v1",
        "runs": (160404, 161176), # This is prompt RECO, so check the run range again when running!
        "data": {
            "pattuple_v10_test3": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v1_AOD_160404_pattuple_v10_test3-0afb79e1b4a9efb21952e294fbf97113/USER",
                "luminosity": 10.589643,
                "number_of_jobs": 2
            },
        }
    },
    "Tau_161216-161312_Prompt": {
        "dataVersion": "41Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_MET45_v2",
        "runs": (161216, 161312), # This is prompt RECO, so check the run range again when running!
        "data": {
            "pattuple_v10_test3": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v1_AOD_161216_pattuple_v10_test3-85ec5544f54122dfd23b7a7442771d8e/USER",
                "luminosity": 12.291216,
                "number_of_jobs": 2
            },
        }
    },
    "Tau_160431-161016_Prompt": {
        "dataVersion": "41Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_MET45_v1",
        "runs": (160431, 161016), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011A-PromptReco-v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 15, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
            "pattuple_v10_old": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v1_AOD_160431_pattuple_v10-ecb64a326bff780f833933d40177edb0/USER",
                "luminosity": 4.984615,
                "number_of_jobs": 1
            },
            "pattuple_v10_1": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v1_AOD_160431_pattuple_v10_1-ecb64a326bff780f833933d40177edb0/USER",
                "luminosity": 5.066715,
                "number_of_jobs": 1
            },
            "pattuple_v10_2": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v1_AOD_160431_pattuple_v10_2-ecb64a326bff780f833933d40177edb0/USER",
                "luminosity": 5.066715,
                "number_of_jobs": 1
            },
            "pattuple_v10": {
                "fallback": "pattuple_v10_2"
            },
        }
    },
    "Tau_162803-162828_Prompt": {
        "dataVersion": "41Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_MET45_v2",
        "runs": (162803, 162828), # This is prompt RECO, so check the run range again when running!
        "data": {
            "pattuple_v10_2": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v2_AOD_162803_pattuple_v10_2-73cd95539afc8c9780e365506b68ad55/USER",
                "luminosity": 4.641724,
                "number_of_jobs": 1, # Adjusted for PATtuple file size
            },
            "pattuple_v10": {
                "fallback": "pattuple_v10_2"
            },
        },
    },
    "Tau_162803-163261_Prompt": {
        "dataVersion": "41Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_MET45_v2",
        "runs": (162803, 163261), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011A-PromptReco-v2/AOD",
                "luminosity": 0,
                "number_of_jobs": 80, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
            "pattuple_v10_3": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v2_AOD_162803_pattuple_v10_3-73cd95539afc8c9780e365506b68ad55/USER",
                "luminosity": 19.877959,
                "number_of_jobs": 1, # Adjusted for PATtuple file size
            },
            "pattuple_v10": {
                "fallback": "pattuple_v10_3"
            },
        },
    },
    "Tau_163270-163369_Prompt": {
        "dataVersion": "41Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_MET45_v4",
        "runs": (163270, 163369), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011A-PromptReco-v2/AOD",
                "luminosity": 0,
                "number_of_jobs": 80, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
            "pattuple_v10_3": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v2_AOD_163270_pattuple_v10_3-d0e103e789c30930fd59a0a157f1e833/USER",
                "luminosity": 18.457785,
                "number_of_jobs": 1, # Adjusted for PATtuple file size
            },
            "pattuple_v10": {
                "fallback": "pattuple_v10_3"
            },
        },
    },

    # Tau + jets
    "TauPlusX_160404-161312_Prompt": {
        "dataVersion": "41Xdata",
        "trigger": "HLT_QuadJet40_IsoPFTau40_v1",
        "runs": (160404, 161312), # This is prompt RECO, so check the run range again when running!
        "data": {
            "pattuple_v10_test3": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TauPlusX/local-Run2011A_PromptReco_v1_AOD_160404_pattuple_v10_test3-7ca7b85da23747106d19bca56315fb4a/USER",
                "luminosity": 22.880859,
                "number_of_jobs": 1
            },
        }
    },
    "TauPlusX_160431-161016_Prompt": {
        "dataVersion": "41Xdata",
        "trigger": "HLT_QuadJet40_IsoPFTau40_v1",
        "runs": (160431, 161016), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/TauPlusX/Run2011A-PromptReco-v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 5, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
            "pattuple_v10_old": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TauPlusX/local-Run2011A_PromptReco_v1_AOD_160431_pattuple_v10-7c7e43599bead125d0cad4b457dd8f70/USER",
                "luminosity": 4.984615,
                "number_of_jobs": 1
            },
            "pattuple_v10_1": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TauPlusX/local-Run2011A_PromptReco_v1_AOD_160431_pattuple_v10_1-7c7e43599bead125d0cad4b457dd8f70/USER",
                "luminosity": 5.066715,
                "number_of_jobs": 1
            },
            "pattuple_v10_2": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TauPlusX/local-Run2011A_PromptReco_v1_AOD_160431_pattuple_v10_2-7c7e43599bead125d0cad4b457dd8f70/USER",
                "luminosity": 5.066715,
                "number_of_jobs": 1
            },
            "pattuple_v10": {
                "fallback": "pattuple_v10_2"
            },
        }
    },
    "TauPlusX_162803-162828_Prompt": {
        "dataVersion": "41Xdata",
        "trigger": "HLT_QuadJet40_IsoPFTau40_v1",
        "runs": (162803, 162828), # This is prompt RECO, so check the run range again when running!
        "data": {
            "pattuple_v10_2": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TauPlusX/local-Run2011A_PromptReco_v2_AOD_162803_pattuple_v10_2-7c7e43599bead125d0cad4b457dd8f70/USER",
                "luminosity": 4.641724,
                "number_of_jobs": 1
            },
            "pattuple_v10": {
                "fallback": "pattuple_v10_2"
            },
        }
    },
    "TauPlusX_162803-163261_Prompt": {
        "dataVersion": "41Xdata",
        "trigger": "HLT_QuadJet40_IsoPFTau40_v1",
        "runs": (162803, 163261), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/TauPlusX/Run2011A-PromptReco-v2/AOD",
                "luminosity": 0,
                "number_of_jobs": 5, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
            "pattuple_v10_3": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TauPlusX/local-Run2011A_PromptReco_v2_AOD_162803_pattuple_v10_3-7c7e43599bead125d0cad4b457dd8f70/USER",
                "luminosity": 19.877959,
                "number_of_jobs": 1
            },
            "pattuple_v10": {
                "fallback": "pattuple_v10_3"
            },
        }
    },
    "TauPlusX_163270-163369_Prompt": {
        "dataVersion": "41Xdata",
        "trigger": "HLT_QuadJet40_IsoPFTau40_v3",
        "runs": (163270, 163369), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/TauPlusX/Run2011A-PromptReco-v2/AOD",
                "luminosity": 0,
                "number_of_jobs": 10, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
            "pattuple_v10_3": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TauPlusX/local-Run2011A_PromptReco_v2_AOD_163270_pattuple_v10_3-43a3ea7594c10f26be97ad52a62101c2/USER",
                "luminosity": 18.146641,
                "number_of_jobs": 1
            },
            "pattuple_v10": {
                "fallback": "pattuple_v10_3"
            },
        }
    },

    # Single Mu
    "SingleMu_160431-161016_Prompt": {
        "dataVersion": "41Xdata",
        "trigger": "HLT_Mu20_v1",
        "runs": (160431, 161016), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-PromptReco-v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 20, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
        }
    },
    "SingleMu_162803-162828_Prompt": {
        "dataVersion": "41Xdata",
        "trigger": "HLT_Mu20_v1",
        "runs": (162803, 162828), # This is prompt RECO, so check the run range again when running!
        "data": {
        },
    },
    "SingleMu_162803-163261_Prompt": {
        "dataVersion": "41Xdata",
        "trigger": "HLT_Mu20_v1",
        "runs": (162803, 163261), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-PromptReco-v2/AOD",
                "luminosity": 0,
                "number_of_jobs": 40, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
        },
    },
    "SingleMu_163270-163369_Prompt": {
        "dataVersion": "41Xdata",
        "trigger": "HLT_Mu24_v2",
        "runs": (163270, 163369), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-PromptReco-v2/AOD",
                "luminosity": 0,
                "number_of_jobs": 15, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
        },
    },
}
