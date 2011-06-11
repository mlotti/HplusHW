import multicrabDatasetsCommon as common

datasets = {
    # Single tau + MET
    "Tau_160431-161016_Prompt": {
        "dataVersion": "41Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_MET45_v1",
        "runs": (160431, 161016), # This is prompt RECO, so check the run range again when running!
        "data": {
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
            "pattuple_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": " /Tau/local-Run2011A_PromptReco_v1_AOD_160431_pattuple_v11b-30bec5347ffdac4381c1a8c0982c0f67/USER",
                "luminosity": 5.064475,
                "number_of_jobs": 1
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
                "number_of_jobs": 1,
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
            "pattuple_v10_3": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v2_AOD_162803_pattuple_v10_3-73cd95539afc8c9780e365506b68ad55/USER",
                "luminosity": 19.877959,
                "number_of_jobs": 1,
            },
            "pattuple_v10": {
                "fallback": "pattuple_v10_3"
            },
            "pattuple_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v2_AOD_162803_pattuple_v11b-3fa3be0859a4d6ac95290d7925e5b48e/USER",
                "luminosity": 26.220099,
                "number_of_jobs": 2,
            },
        },
    },
    "Tau_163270-163369_Prompt": {
        "dataVersion": "41Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_MET45_v4",
        "runs": (163270, 163369), # This is prompt RECO, so check the run range again when running!
        "data": {
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
    "Tau_163270-163757_Prompt": {
        "dataVersion": "41Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_MET45_v4",
        "runs": (163270, 163757), # This is prompt RECO, so check the run range again when running!
        "data": {
            "pattuple_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v2_AOD_163270_pattuple_v11b-0fbacf41641faa252a2bc6c4d4cd404b/USER",
                "luminosity": 121.519197,
                "number_of_jobs": 7,
            },
        },
    },
    "Tau_163758-163869_Prompt": {
        "dataVersion": "41Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_MET45_v4",
        "runs": (163758, 163869), # This is prompt RECO, so check the run range again when running!
        "data": {
            "pattuple_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v2_AOD_163758_pattuple_v11b-0fbacf41641faa252a2bc6c4d4cd404b/USER",
                "luminosity": 38.238908,
                "number_of_jobs": 2,
            },
        }
    },
    ##### 42X starts here
    "Tau_165088-165633_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_MET45_v6",
        "runs": (165088, 165633), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011A-PromptReco-v4/AOD",
                "luminosity": 0,
                "number_of_jobs": 200, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
        }
    },
    "Tau_165970-166502_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_MET60_v2",
        "runs": (165970, 166502), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011A-PromptReco-v4/AOD",
                "luminosity": 0,
                "number_of_jobs": 100, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
        }
    },

    # Single tau (control)
    "Tau_Single_165970-166164_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_v2",
        "runs": (165970, 166502), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011A-PromptReco-v4/AOD",
                "luminosity": 0,
                "number_of_jobs": 50, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
        }
    },


    # Tau + jets
    # FIXME: this is wrong, we shoud use MultiJet PD!
    "TauPlusX_160431-161016_Prompt": {
        "dataVersion": "41Xdata",
        "trigger": "HLT_QuadJet40_IsoPFTau40_v1",
        "runs": (160431, 161016), # This is prompt RECO, so check the run range again when running!
        "data": {
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
    "TauPlusX_163270-163869_Prompt": {
        "dataVersion": "41Xdata",
        "trigger": "HLT_QuadJet40_IsoPFTau40_v3",
        "runs": (163270, 163869), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/TauPlusX/Run2011A-PromptReco-v2/AOD",
                "luminosity": 0,
                "number_of_jobs": 50, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
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
        },
    },
    "SingleMu_163270-163369_Prompt": {
        "dataVersion": "41Xdata",
        "trigger": "HLT_Mu24_v2",
        "runs": (163270, 163369), # This is prompt RECO, so check the run range again when running!
        "data": {
        },
    },
    "SingleMu_163270-163869_Prompt": {
        "dataVersion": "41Xdata",
        "trigger": "HLT_Mu24_v2",
        "runs": (163270, 163869), # This is prompt RECO, so check the run range again when running!
        "data": {
        },
    },
    ### 42X starts here
    "SingleMu_165088-165121_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_Mu30_v3",
        "runs": (165088, 165121), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-PromptReco-v4/AOD",
                "luminosity": 0,
                "number_of_jobs": 20, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
        }
    },
}
