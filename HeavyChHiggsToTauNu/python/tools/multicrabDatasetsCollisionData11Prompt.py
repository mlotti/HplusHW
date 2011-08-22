import multicrabDatasetsCommon as common

datasets = {
    # Single tau + MET
    "Tau_160431-161016_Prompt": {
        "dataVersion": "41Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_MET45_v1",
        "runs": (160431, 161016), # This is prompt RECO, so check the run range again when running!
        "data": {
            "pattuple_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": " /Tau/local-Run2011A_PromptReco_v1_AOD_160431_pattuple_v11b-30bec5347ffdac4381c1a8c0982c0f67/USER",
                "luminosity": 5.064475,
                "number_of_jobs": 1
            },
        }
    },
    "Tau_162803-163261_Prompt": {
        "dataVersion": "41Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_MET45_v2",
        "runs": (162803, 163261), # This is prompt RECO, so check the run range again when running!
        "data": {
            "pattuple_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v2_AOD_162803_pattuple_v11b-3fa3be0859a4d6ac95290d7925e5b48e/USER",
                "luminosity": 26.220099,
                "number_of_jobs": 2,
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
            "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v4_AOD_165088_pattuple_v17-88e7da0ca8e64fa806b2941f116acbf5/USER",
                "luminosity": 133.26997598200001,
                "number_of_jobs": 8,
            },
        }
    },
    "Tau_165103-165103_Prompt_Wed": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_MET45_v6",
        "runs": (165103, 165103), # This is prompt RECO, so check the run range again when running!
        "data": {
            "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v4_AOD_165103_pattuple_v17-88e7da0ca8e64fa806b2941f116acbf5/USER",
                "luminosity": 0.000176,
                "number_of_jobs": 1,
            },
        }
    },
    "Tau_165970-166164_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_MET60_v2",
        "runs": (165970, 166164), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011A-PromptReco-v4/AOD",
                "luminosity": 0,
                "number_of_jobs": 100, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
            "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v4_AOD_165970_pattuple_v17-b1b6e1ef7d022a15760998ee2f0cd38b/USER",
                "luminosity": 94.672079,
                "number_of_jobs": 1,
            },
        }
    },
    "Tau_166346-166346_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_MET60_v3",
        "runs": (166346, 166346), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011A-PromptReco-v4/AOD",
                "luminosity": 0,
                "number_of_jobs": 10, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
            "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v4_AOD_166346_pattuple_v17-7c45e9a505fd663ef2b8b9a70d817ba2/USER",
                "luminosity": 4.153168,
                "number_of_jobs": 1,
            },
        }
    },
    "Tau_166374-167043_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_MET60_v2",
        "runs": (166374, 167043), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011A-PromptReco-v4/AOD",
                "luminosity": 0,
                "number_of_jobs": 180, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
            "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v4_AOD_166374_pattuple_v17-b1b6e1ef7d022a15760998ee2f0cd38b/USER",
                "luminosity": 424.330775,
                "number_of_jobs": 4,
            },
        }
    },
    "Tau_167078-167784_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_MET60_v4",
        "runs": (167078, 167784), # This is prompt RECO, so check the run range again when running!
        "data": {
            "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v4_AOD_167078_pattuple_v17-da16291615a20543c7b27d5bed242048/USER",
                "luminosity": 115.617591172,
                "number_of_jobs": 2,
            },
        }
    },
    "Tau_167786-167913_Prompt_Wed": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_MET60_v4",
        "runs": (167786, 167913), # This is prompt RECO, so check the run range again when running!
        "data": {
            "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v4_AOD_167786_pattuple_v17-da16291615a20543c7b27d5bed242048/USER",
                "luminosity": 105.026041,
                "number_of_jobs": 2,
            },
        }
    },
    "Tau_167078-167913_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_MET60_v4",
        "runs": (167078, 167913), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011A-PromptReco-v4/AOD",
                "luminosity": 0,
                "number_of_jobs": 60, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
        }
    },
    "Tau_172620-173198_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_MET60_v6",
        "runs": (172620, 173198), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011A-PromptReco-v6/AOD",
                "luminosity": 0,
                "number_of_jobs": 110, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
        }
    },
    "Tau_173236-173243_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_MediumIsoPFTau35_Trk20_MET60_v1",
        "runs": (173236, 173243), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011A-PromptReco-v6/AOD",
                "luminosity": 0,
                "number_of_jobs": 15, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
        }
    },

    # Single tau (control)
    "Tau_Single_165970-166164_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_v2",
        "runs": (165970, 166164), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011A-PromptReco-v4/AOD",
                "luminosity": 0,
                "number_of_jobs": 40, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
            "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v4_AOD_Single_165970_pattuple_v17_1-966d1f43c0a18025a0c612a0382d30e9/USER",
                "luminosity": 94.672079,
                "number_of_jobs": 1,
            },
        }
    },
    "Tau_Single_166346-166346_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_v3",
        "runs": (166346, 166346), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011A-PromptReco-v4/AOD",
                "luminosity": 0,
                "number_of_jobs": 40, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
            "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v4_AOD_Single_166346_pattuple_v17_1-2356c1cf8147598f6ed0b1a5f80be4e2/USER",
                "luminosity": 4.153168,
                "number_of_jobs": 1,
            },
        }
    },
    "Tau_Single_166374-167043_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_v2",
        "runs": (166374, 167043), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011A-PromptReco-v4/AOD",
                "luminosity": 0,
                "number_of_jobs": 180, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
            "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v4_AOD_Single_166374_pattuple_v17_1-966d1f43c0a18025a0c612a0382d30e9/USER",
                "luminosity": 424.330775,
                "number_of_jobs": 2,
            },
        }
    },
    "Tau_Single_167078-167784_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_v4",
        "runs": (167078, 167784), # This is prompt RECO, so check the run range again when running!
        "data": {
            "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v4_AOD_Single_167078_pattuple_v17_1-5ac48e003cbdad1c6c78ae464438a5c1/USER",
                "luminosity": 115.617591,
                "number_of_jobs": 1,
            },
        }
    },
    "Tau_Single_167786-167913_Prompt_Wed": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_v4",
        "runs": (167786, 167913), # This is prompt RECO, so check the run range again when running!
        "data": {
            "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v4_AOD_Single_167786_pattuple_v17_1-5ac48e003cbdad1c6c78ae464438a5c1/USER",
                "luminosity": 105.026041,
                "number_of_jobs": 2,
            },
        }
    },
    "Tau_Single_167078-167913_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_v4",
        "runs": (167078, 167913), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011A-PromptReco-v4/AOD",
                "luminosity": 0,
                "number_of_jobs": 60, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
        }
    },
    "Tau_Single_172620-173243_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_v6",
        "runs": (172620, 173243), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011A-PromptReco-v6/AOD",
                "luminosity": 0,
                "number_of_jobs": 110, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
        }
    },
    "Tau_Single_173236-173243_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_MediumIsoPFTau35_Trk20_v1",
        "runs": (173236, 173243), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011A-PromptReco-v6/AOD",
                "luminosity": 0,
                "number_of_jobs": 15, # Adjusted for PATtuple file size
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
        }
    },
    "TauPlusX_162803-162828_Prompt": {
        "dataVersion": "41Xdata",
        "trigger": "HLT_QuadJet40_IsoPFTau40_v1",
        "runs": (162803, 162828), # This is prompt RECO, so check the run range again when running!
        "data": {
        }
    },
    "TauPlusX_162803-163261_Prompt": {
        "dataVersion": "41Xdata",
        "trigger": "HLT_QuadJet40_IsoPFTau40_v1",
        "runs": (162803, 163261), # This is prompt RECO, so check the run range again when running!
        "data": {
        }
    },
    "TauPlusX_163270-163369_Prompt": {
        "dataVersion": "41Xdata",
        "trigger": "HLT_QuadJet40_IsoPFTau40_v3",
        "runs": (163270, 163369), # This is prompt RECO, so check the run range again when running!
        "data": {
        }
    },
    "TauPlusX_163270-163869_Prompt": {
        "dataVersion": "41Xdata",
        "trigger": "HLT_QuadJet40_IsoPFTau40_v3",
        "runs": (163270, 163869), # This is prompt RECO, so check the run range again when running!
        "data": {
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
    "SingleMu_165088-166150_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_Mu30_v3",
        "runs": (165088, 166150), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-PromptReco-v4/AOD",
                "luminosity": 0,
                "number_of_jobs": 170, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
        }
    },
    "SingleMu_165103-165103_Prompt_Wed": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_Mu30_v3",
        "runs": (165103, 165103), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-PromptReco-v4/AOD",
                "luminosity": 0,
                "number_of_jobs": 1, # Adjusted for PATtuple file size
                "lumiMask": "PromptRecoWedDiff"
            },
        }
    },
    "SingleMu_166161-166164_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_Mu40_v1",
        "runs": (166161, 166164), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-PromptReco-v4/AOD",
                "luminosity": 0,
                "number_of_jobs": 2, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
        }
    },
    "SingleMu_166346-166346_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_Mu40_v2",
        "runs": (166346, 166346), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-PromptReco-v4/AOD",
                "luminosity": 0,
                "number_of_jobs": 2, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
        }
    },
    "SingleMu_166374-167043_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_Mu40_v1",
        "runs": (166374, 167043), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-PromptReco-v4/AOD",
                "luminosity": 0,
                "number_of_jobs": 190, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
        }
    },
    "SingleMu_167078-167784_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_Mu40_v3",
        "runs": (167078, 167784), # This is prompt RECO, so check the run range again when running!
        "data": {
        }
    },
    "SingleMu_167786-167913_Prompt_Wed": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_Mu40_v3",
        "runs": (167786, 167913), # This is prompt RECO, so check the run range again when running!
        "data": {
        }
    },
    "SingleMu_167078-167913_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_Mu40_v3",
        "runs": (167078, 167913), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-PromptReco-v4/AOD",
                "luminosity": 0,
                "number_of_jobs": 26, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
        }
    },
    "SingleMu_172620-173198_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_Mu40_v5",
        "runs": (172620, 173198), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-PromptReco-v6/AOD",
                "luminosity": 0,
                "number_of_jobs": 110, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
        }
    },
    "SingleMu_173236-173243_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_Mu40_eta2p1_v1",
        "runs": (173236, 173243), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-PromptReco-v6/AOD",
                "luminosity": 0,
                "number_of_jobs": 15, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
        }
    },
}
