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
                "number_of_jobs": 200, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
            "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v4_AOD_165088_pattuple_v17-88e7da0ca8e64fa806b2941f116acbf5/USER",
                "luminosity": 133.26997598200001,
                "number_of_jobs": 8,
            },
            "pattuple_v18": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v4_AOD_165088_pattuple_v18-68faa0f802ec7fdcb65798edde8320e0/USER",
                "luminosity": 138.377000,
                "number_of_jobs": 2,
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
                "number_of_jobs": 100, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
            "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v4_AOD_165970_pattuple_v17-b1b6e1ef7d022a15760998ee2f0cd38b/USER",
                "luminosity": 94.672079,
                "number_of_jobs": 1,
            },
            "pattuple_v18": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v4_AOD_165970_pattuple_v18-76121191f925a13de2aa415b27ca9123/USER",
                "luminosity": 97.575000,
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
                "number_of_jobs": 10, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
            "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v4_AOD_166346_pattuple_v17-7c45e9a505fd663ef2b8b9a70d817ba2/USER",
                "luminosity": 4.153168,
                "number_of_jobs": 1,
            },
            "pattuple_v18": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v4_AOD_166346_pattuple_v18-5d01286b07eac898e76bc9af379febd1/USER",
                "luminosity": 4.263000,
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
                "number_of_jobs": 180, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
            "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v4_AOD_166374_pattuple_v17-b1b6e1ef7d022a15760998ee2f0cd38b/USER",
                "luminosity": 424.330775,
                "number_of_jobs": 4,
            },
            "pattuple_v18": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v4_AOD_166374_pattuple_v18-76121191f925a13de2aa415b27ca9123/USER",
                "luminosity": 445.101000,
                "number_of_jobs": 2,
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
                "number_of_jobs": 60, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
            "pattuple_v18": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v4_AOD_167078_pattuple_v18-15a242972125149d3b1ef8cac53549e8/USER",
                "luminosity": 244.913000,
                "number_of_jobs": 1,
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
                "number_of_jobs": 110, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
            "pattuple_v18": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v6_AOD_172620_pattuple_v18-516e60e4f3f21c17e8f9bca025365e30/USER",
                "luminosity": 409.704000,
                "number_of_jobs": 1,
            },
        }
    },
    "Tau_173236-173692_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_MediumIsoPFTau35_Trk20_MET60_v1",
        "runs": (173236, 173692), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011A-PromptReco-v6/AOD",
                "number_of_jobs": 90, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
            "pattuple_v18": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v6_AOD_173236_pattuple_v18-6c282a9b564868ab3377c4686ed3334d/USER",
                "luminosity": 253.263000,
                "number_of_jobs": 1,
            },
        }
    },
    "Tau_175860-177452_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_MediumIsoPFTau35_Trk20_MET60_v1",
        "runs": (175860, 177452), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011B-PromptReco-v1/AOD",
                "number_of_jobs": 400, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
        }
    },
    "Tau_177718-178380_Prompt": { # this split is only to have less than 500 jobs
        "dataVersion": "42Xdata",
        "trigger": "HLT_MediumIsoPFTau35_Trk20_MET60_v1",
        "runs": (177718, 178380), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011B-PromptReco-v1/AOD",
                "number_of_jobs": 230, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
        }
    },
    "Tau_178420-178479_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_MediumIsoPFTau35_Trk20_MET60_v5",
        "runs": (178420, 178479), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011B-PromptReco-v1/AOD",
                "number_of_jobs": 40, # Adjusted for PATtuple file size
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
                "number_of_jobs": 40, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
            "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v4_AOD_Single_165970_pattuple_v17_1-966d1f43c0a18025a0c612a0382d30e9/USER",
                "luminosity": 94.672079,
                "number_of_jobs": 1,
            },
            "pattuple_v18_0": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v4_AOD_Single_165970_pattuple_v18-a074e5725328b3ec89273a9ce844bc40/USER",
                "luminosity": 97.575000,
                "number_of_jobs": 1,
            },
            "pattuple_v18_1": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-PromptReco_v4_AOD_Single_165970_pattuple_v18_1-fdd51a0468635b24b4e8e11496951f46/USER",
                "number_of_jobs": 1,
            },
            "pattuple_v18": {
                "fallback": "pattuple_v18_1"
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
                "number_of_jobs": 40, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
            "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v4_AOD_Single_166346_pattuple_v17_1-2356c1cf8147598f6ed0b1a5f80be4e2/USER",
                "luminosity": 4.153168,
                "number_of_jobs": 1,
            },
            "pattuple_v18_0": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v4_AOD_Single_166346_pattuple_v18-b8f5408188cfaed2b0815a31b0c35328/USER",
                "luminosity": 4.263000,
                "number_of_jobs": 1,
            },
            "pattuple_v18_1": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-PromptReco_v4_AOD_Single_166346_pattuple_v18_1-143d19c22e1dc04bd1dce09508880f26/USER",
                "number_of_jobs": 1,
            },
            "pattuple_v18": {
                "fallback": "pattuple_v18_1"
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
                "number_of_jobs": 180, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
            "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v4_AOD_Single_166374_pattuple_v17_1-966d1f43c0a18025a0c612a0382d30e9/USER",
                "luminosity": 424.330775,
                "number_of_jobs": 2,
            },
            "pattuple_v18_0": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v4_AOD_Single_166374_pattuple_v18-a074e5725328b3ec89273a9ce844bc40/USER",
                "luminosity": 445.101000,
                "number_of_jobs": 1,
            },
            "pattuple_v18_1": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-PromptReco_v4_AOD_Single_166374_pattuple_v18_1-fdd51a0468635b24b4e8e11496951f46/USER",
                "number_of_jobs": 1,
            },
            "pattuple_v18": {
                "fallback": "pattuple_v18_1"
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
                "number_of_jobs": 60, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
            "pattuple_v18_0": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v4_AOD_Single_167078_pattuple_v18-cfa6d85277f38798ba0a058732e0532a/USER",
                "luminosity": 244.913000,
                "number_of_jobs": 1,
            },
            "pattuple_v18_1": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-PromptReco_v4_AOD_Single_167078_pattuple_v18_1-b9d72f7d08ce2bde010f2a599c37f83b/USER",
                "number_of_jobs": 1,
            },
            "pattuple_v18": {
                "fallback": "pattuple_v18_1"
            },
        }
    },
    "Tau_Single_172620-173198_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_v6",
        "runs": (172620, 173198), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011A-PromptReco-v6/AOD",
                "number_of_jobs": 110, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
            "pattuple_v18_0": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v6_AOD_Single_172620_pattuple_v18_1-94011b60044d698fe5dbd6fe93c7d90b/USER",
                "luminosity": 409.704146,
                "number_of_jobs": 1,
            },
            "pattuple_v18_1": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-PromptReco_v6_AOD_Single_172620_pattuple_v18_1-e7ac736350b7c673637ba90e811c1fee/USER",
                "number_of_jobs": 1,
            },
            "pattuple_v18": {
                "fallback": "pattuple_v18_1"
            },
        }
    },
    "Tau_Single_173236-173692_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_MediumIsoPFTau35_Trk20_v1",
        "runs": (173236, 173692), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011A-PromptReco-v6/AOD",
                "number_of_jobs": 90, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
            "pattuple_v18_0": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v6_AOD_Single_173236_pattuple_v18-8175a7a03b92bf75b3dce339fc4f2ac3/USER",
                "luminosity": 253.263000,
                "number_of_jobs": 1,
            },
            "pattuple_v18_1": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-PromptReco_v6_AOD_Single_173236_pattuple_v18_1-0a73f291926323f98d8a274907cf7f3e/USER",
                "number_of_jobs": 1,
            },
            "pattuple_v18": {
                "fallback": "pattuple_v18_1"
            },
        }
    },
    "Tau_Single_175860-177452_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_MediumIsoPFTau35_Trk20_v1",
        "runs": (175860, 177452), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011B-PromptReco-v1/AOD",
                "number_of_jobs": 400, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
        }
    },
    "Tau_Single_1777180-178380_Prompt": { # this split is only to have less than 500 jobs
        "dataVersion": "42Xdata",
        "trigger": "HLT_MediumIsoPFTau35_Trk20_v1",
        "runs": (177718, 178380), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011B-PromptReco-v1/AOD",
                "number_of_jobs": 230, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
        }
    },
    "Tau_Single_178420-178479_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_MediumIsoPFTau35_Trk20_v5",
        "runs": (178420, 178479), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011B-PromptReco-v1/AOD",
                "number_of_jobs": 40, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
        }
    },

    # Single Mu
    "SingleMu_165088-165633_Prompt": {
        "dataVersion": "42Xdata",
        "args": {"doTauHLTMatching": 0},
        "triggerOR": [
            "HLT_Mu30_v3", "HLT_IsoMu17_v8", # not prescaled
            "HLT_Mu15_v4", "HLT_Mu20_v3", "HLT_Mu24_v3", "HLT_IsoMu15_v8", # prescaled
            ],
        "runs": (165088, 165633), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-PromptReco-v4/AOD",
                "number_of_jobs": 0, # To be adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
        }
    },
    "SingleMu_165970-166150_Prompt": {
        "dataVersion": "42Xdata",
        "args": {"doTauHLTMatching": 0},
        "triggerOR": [
            "HLT_Mu30_v3", "HLT_IsoMu24_v5", # not prescaled
            "HLT_Mu15_v4", "HLT_Mu20_v3", "HLT_Mu24_v3", "HLT_IsoMu15_v9", "HLT_IsoMu17_v9", # prescaled
            ],
        "runs": (165970, 166150), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-PromptReco-v4/AOD",
                "number_of_jobs": 0, # To be adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
        }
    },
    "SingleMu_166161-166164_Prompt": {
        "dataVersion": "42Xdata",
        "triggerOR": [
            "HLT_Mu40_v1", "HLT_IsoMu24_v5", # not prescaled
            "HLT_Mu15_v4", "HLT_Mu20_v3", "HLT_Mu24_v3", "HLT_Mu30_v3", "HLT_IsoMu15_v9", "HLT_IsoMu17_v9", # prescaled
            ],
        "runs": (166161, 166164), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-PromptReco-v4/AOD",
                "number_of_jobs": 0, # To be adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
        }
    },
    "SingleMu_166346-166346_Prompt": {
        "dataVersion": "42Xdata",
        "triggerOR": [
            "HLT_Mu40_v2", "HLT_IsoMu24_v6", # not prescaled
            "HLT_Mu15_v5", "HLT_Mu20_v4", "HLT_Mu24_v3", "HLT_Mu30_v4", "HLT_IsoMu15_v10", "HLT_IsoMu17_v10", # prescaled
            ],
        "runs": (166346, 166346), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-PromptReco-v4/AOD",
                "number_of_jobs": 0, # To be adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
        }
    },
    "SingleMu_166374-166967_Prompt": {
        "dataVersion": "42Xdata",
        "triggerOR": [
            "HLT_Mu40_v1", "HLT_IsoMu24_v5", # not prescaled
            "HLT_Mu15_v4", "HLT_Mu20_v3", "HLT_Mu24_v3", "HLT_Mu30_v3", "HLT_IsoMu15_v9", "HLT_IsoMu17_v9", # prescaled
            ],
        "runs": (166374, 166967), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-PromptReco-v4/AOD",
                "number_of_jobs": 0, # To be adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
        }
    },
    "SingleMu_167039-167043_Prompt": {
        "dataVersion": "42Xdata",
        "triggerOR": [
            "HLT_Mu40_v1", "HLT_IsoMu24_v5", "HLT_IsoMu20_eta2p1_v1", # not prescaled
            "HLT_Mu15_v4", "HLT_Mu20_v3", "HLT_Mu24_v3", "HLT_Mu30_v3", "HLT_IsoMu15_v9", "HLT_IsoMu17_v9", "HLT_IsoMu17_eta2p1_v1", # prescaled
            ],
        "runs": (167039, 167043), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-PromptReco-v4/AOD",
                "number_of_jobs": 0, # To be adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
        }
    },
    "SingleMu_167078-167913_Prompt": {
        "dataVersion": "42Xdata",
        "triggerOR": [
            "HLT_Mu40_v3", "HLT_IsoMu24_v7", "HLT_IsoMu20_eta2p1_v1", # not prescaled
            "HLT_Mu15_v6", "HLT_Mu20_v5", "HLT_Mu24_v5", "HLT_Mu30_v5", "HLT_IsoMu15_v11", "HLT_IsoMu17_v11", "HLT_IsoMu17_eta2p1_v1", # prescaled
            ],
        "runs": (167078, 167913), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-PromptReco-v4/AOD",
                "number_of_jobs": 0, # To be adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
        }
    },
    "SingleMu_172620-173198_Prompt": {
        "dataVersion": "42Xdata",
        "triggerOR": [
            "HLT_Mu40_v5", "HLT_IsoMu24_v8", # not prescaled
            "HLT_Mu15_v8", "HLT_Mu20_v7", "HLT_Mu24_v7", "HLT_Mu30_v7", "HLT_IsoMu15_v13", "HLT_IsoMu17_v13", # prescaled
            ],
        "runs": (172620, 173198), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-PromptReco-v6/AOD",
                "number_of_jobs": 0, # To be adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
        }
    },
    "SingleMu_175860-177452_Prompt": {
        "dataVersion": "42Xdata",
        "runs": (175860, 177452), # This is prompt RECO, so check the run range again when running!
        "triggerOR": [
            "HLT_Mu40_eta2p1_v1", "HLT_IsoMu30_eta2p1_v3", # not prescaled
            "HLT_Mu15_v9", "HLT_Mu20_v8", "HLT_Mu24_v8", "HLT_Mu30_v8", "HLT_Mu40_v6", "HLT_Mu24_eta2p1_v1", "HLT_Mu30_eta2p1_v1",
            "HLT_IsoMu15_v14", "HLT_IsoMu17_v14", "HLT_IsoMu20_v9", "HLT_IsoMu24_v9", "HLT_IsoMu15_eta2p1_v1", "HLT_IsoMu24_eta2p1_v3", # prescaled
            ],
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011B-PromptReco-v1/AOD",
                "number_of_jobs": 0, # To be adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
        }
    },
    "SingleMu_177718-178380_Prompt": {
        "dataVersion": "42Xdata",
        "runs": (177718, 178380), # This is prompt RECO, so check the run range again when running!
        "triggerOR": [
            "HLT_Mu40_eta2p1_v1", "HLT_IsoMu30_eta2p1_v3", # not prescaled
            "HLT_Mu15_v9", "HLT_Mu20_v8", "HLT_Mu24_v8", "HLT_Mu30_v8", "HLT_Mu40_v6", "HLT_Mu24_eta2p1_v1", "HLT_Mu30_eta2p1_v1",
            "HLT_IsoMu15_v14", "HLT_IsoMu17_v14", "HLT_IsoMu20_v9", "HLT_IsoMu24_v9", "HLT_IsoMu15_eta2p1_v1", "HLT_IsoMu24_eta2p1_v3", # prescaled
            ],
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011B-PromptReco-v1/AOD",
                "number_of_jobs": 0, # To be adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
        }
    },
    "SingleMu_178420-178479_Prompt": {
        "dataVersion": "42Xdata",
        "runs": (178420, 178479), # This is prompt RECO, so check the run range again when running!
        "triggerOR": [
            "HLT_Mu40_eta2p1_v4", "HLT_IsoMu30_eta2p1_v6", # not prescaled
            "HLT_Mu15_v12", "HLT_Mu20_v11", "HLT_Mu24_v11", "HLT_Mu30_v11", "HLT_Mu40_v9", 
            "HLT_IsoMu15_v17", "HLT_IsoMu20_v12", "HLT_IsoMu24_v12", "HLT_IsoMu15_eta2p1_v4", "HLT_IsoMu24_eta2p1_v6", # prescaled
            ],
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011B-PromptReco-v1/AOD",
                "number_of_jobs": 0, # To be adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
        }
    },



    # Single Mu for tau embedding skims
    "SingleMu_Mu_165088-166150_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_Mu30_v3",
        "runs": (165088, 166150), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-PromptReco-v4/AOD",
                "number_of_jobs": 490, # Adjusted for skim file size
                "lumiMask": "PromptReco"
            },
        }
    },
    "SingleMu_Mu_165103-165103_Prompt_Wed": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_Mu30_v3",
        "runs": (165103, 165103), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-PromptReco-v4/AOD",
                "number_of_jobs": 1, # Adjusted for skim file size
                "lumiMask": "PromptRecoWedDiff"
            },
        }
    },
    "SingleMu_Mu_166161-166164_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_Mu40_v1",
        "runs": (166161, 166164), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-PromptReco-v4/AOD",
                "number_of_jobs": 2, # Adjusted for skim file size
                "lumiMask": "PromptReco"
            },
        }
    },
    "SingleMu_Mu_166346-166346_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_Mu40_v2",
        "runs": (166346, 166346), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-PromptReco-v4/AOD",
                "number_of_jobs": 2, # Adjusted for skim file size
                "lumiMask": "PromptReco"
            },
        }
    },
    "SingleMu_Mu_166374-167043_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_Mu40_v1",
        "runs": (166374, 167043), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-PromptReco-v4/AOD",
                "number_of_jobs": 300, # Adjusted for skim file size
                "lumiMask": "PromptReco"
            },
        }
    },
    "SingleMu_Mu_167078-167784_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_Mu40_v3",
        "runs": (167078, 167784), # This is prompt RECO, so check the run range again when running!
        "data": {
        }
    },
    "SingleMu_Mu_167786-167913_Prompt_Wed": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_Mu40_v3",
        "runs": (167786, 167913), # This is prompt RECO, so check the run range again when running!
        "data": {
        }
    },
    "SingleMu_Mu_167078-167913_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_Mu40_v3",
        "runs": (167078, 167913), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-PromptReco-v4/AOD",
                "number_of_jobs": 230, # Adjusted for skim file size
                "lumiMask": "PromptReco"
            },
        }
    },
    "SingleMu_Mu_172620-173198_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_Mu40_v5",
        "runs": (172620, 173198), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-PromptReco-v6/AOD",
                "number_of_jobs": 230, # Adjusted for skim file size
                "lumiMask": "PromptReco"
            },
        }
    },
    "SingleMu_Mu_173236-173692_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_Mu40_eta2p1_v1",
        "runs": (173236, 173692), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-PromptReco-v6/AOD",
                "number_of_jobs": 120, # Adjusted for skim file size
                "lumiMask": "PromptReco"
            },
        }
    },
    "SingleMu_Mu_175860-177452_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_Mu40_eta2p1_v1",
        "runs": (175860, 177452), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011B-PromptReco-v1/AOD",
                "number_of_jobs": 480, # Adjusted for skim file size
                "lumiMask": "PromptReco"
            },
        }
    },
    "SingleMu_Mu_177718-177878_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_Mu40_eta2p1_v1",
        "runs": (177718, 177878), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011B-PromptReco-v1/AOD",
                "number_of_jobs": 300, # Adjusted for skim file size
                "lumiMask": "PromptReco"
            },
        }
    },
    "SingleMu_Mu_178420-178479_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_Mu40_eta2p1_v4",
        "runs": (178420, 178479), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011B-PromptReco-v1/AOD",
                "number_of_jobs": 60, # Adjusted for skim file size
                "lumiMask": "PromptReco"
            },
        }
    },
}
