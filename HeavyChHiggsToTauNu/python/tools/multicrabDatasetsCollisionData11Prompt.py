import multicrabDatasetsCommon as common

datasets = {
    # Single tau + MET
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
            "pattuple_v18": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v4_AOD_165088_pattuple_v18-68faa0f802ec7fdcb65798edde8320e0/USER",
                "luminosity": 138.377000,
                "number_of_jobs": 2,
            },
        }
    },
    "Tau_165970-166164_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_MET60_v2",
        "runs": (165970, 166164), # This is prompt RECO, so check the run range again when running!
        "data": {
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
            "pattuple_v18": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v4_AOD_166374_pattuple_v18-76121191f925a13de2aa415b27ca9123/USER",
                "luminosity": 445.101000,
                "number_of_jobs": 2,
            },
        }
    },
    "Tau_167078-167913_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_MET60_v4",
        "runs": (167078, 167913), # This is prompt RECO, so check the run range again when running!
        "data": {
            "pattuple_v18": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_PromptReco_v4_AOD_167078_pattuple_v18-15a242972125149d3b1ef8cac53549e8/USER",
                "luminosity": 244.913000,
                "number_of_jobs": 1,
            },
        }
    },
    "Tau_165970-167913_Prompt": {
        "dataVersion": "42Xdata",
        "args": {"triggerThrow": 0}, # needed for OR of triggers in separate run ranges
        "triggerOR": [
            "HLT_IsoPFTau35_Trk20_MET60_v2", # 165970-166164, 166374-167043
            "HLT_IsoPFTau35_Trk20_MET60_v3", # 166346
            "HLT_IsoPFTau35_Trk20_MET60_v4", # 167078-167913
        ],
        "runs": (165970, 167913), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011A-PromptReco-v4/AOD",
                "number_of_jobs": 350, # Adjusted for PATtuple file size
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
    "Tau_178420-179411_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_MediumIsoPFTau35_Trk20_MET60_v5",
        "runs": (178420, 179411), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011B-PromptReco-v1/AOD",
                "number_of_jobs": 140, # Adjusted for PATtuple file size
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
    "Tau_Single_167078-167913_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_v4",
        "runs": (167078, 167913), # This is prompt RECO, so check the run range again when running!
        "data": {
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
    "Tau_Single_165970-167913_Prompt": {
        "dataVersion": "42Xdata",
        "args": {"triggerThrow": 0}, # needed for OR of triggers in separate run ranges
        "triggerOR": [
            "HLT_IsoPFTau35_Trk20_v2", # 165970-166164, 166374-167043
            "HLT_IsoPFTau35_Trk20_v3", # 166346-166346
            "HLT_IsoPFTau35_Trk20_v4", # 167078-167913
        ],
        "runs": (165970, 167913), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011A-PromptReco-v4/AOD",
                "number_of_jobs": 350, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
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
    "Tau_Single_177718-178380_Prompt": { # this split is only to have less than 500 jobs
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
    "Tau_Single_178420-179411_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_MediumIsoPFTau35_Trk20_v5",
        "runs": (178420, 179411), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011B-PromptReco-v1/AOD",
                "number_of_jobs": 140, # Adjusted for PATtuple file size
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
                "number_of_jobs": 490, # Adjusted for PATtuple file size (~200 in reality)
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
                "number_of_jobs": 490, # Adjusted for PATtuple file size (~160 in reality)
                "lumiMask": "PromptReco"
            },
        }
    },
    "SingleMu_166161-166164_Prompt": {
        "dataVersion": "42Xdata",
        "args": {"doTauHLTMatching": 0},
        "triggerOR": [
            "HLT_Mu40_v1", "HLT_IsoMu24_v5", # not prescaled
            "HLT_Mu15_v4", "HLT_Mu20_v3", "HLT_Mu24_v3", "HLT_Mu30_v3", "HLT_IsoMu15_v9", "HLT_IsoMu17_v9", # prescaled
            ],
        "runs": (166161, 166164), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-PromptReco-v4/AOD",
                "number_of_jobs": 20, # Adjusted for PATtuple file size (~10 in reality)
                "lumiMask": "PromptReco"
            },
        }
    },
    "SingleMu_166346-166346_Prompt": {
        "dataVersion": "42Xdata",
        "args": {"doTauHLTMatching": 0},
        "triggerOR": [
            "HLT_Mu40_v2", "HLT_IsoMu24_v6", # not prescaled
            "HLT_Mu15_v5", "HLT_Mu20_v4", "HLT_Mu24_v4", "HLT_Mu30_v4", "HLT_IsoMu15_v10", "HLT_IsoMu17_v10", # prescaled
            ],
        "runs": (166346, 166346), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-PromptReco-v4/AOD",
                "number_of_jobs": 20, # Adjusted for PATtuple file size (~10 in reality)
                "lumiMask": "PromptReco"
            },
        }
    },
    "SingleMu_166374-166967_Prompt": {
        "dataVersion": "42Xdata",
        "args": {"doTauHLTMatching": 0},
        "triggerOR": [
            "HLT_Mu40_v1", "HLT_IsoMu24_v5", # not prescaled
            "HLT_Mu15_v4", "HLT_Mu20_v3", "HLT_Mu24_v3", "HLT_Mu30_v3", "HLT_IsoMu15_v9", "HLT_IsoMu17_v9", # prescaled
            ],
        "runs": (166374, 166967), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-PromptReco-v4/AOD",
                "number_of_jobs": 1000, # Adjusted for PATtuple file size (~380 in reality)
                "lumiMask": "PromptReco"
            },
        }
    },
    "SingleMu_167039-167043_Prompt": {
        "dataVersion": "42Xdata",
        "args": {"doTauHLTMatching": 0},
        "triggerOR": [
            "HLT_Mu40_v1", "HLT_IsoMu24_v5", "HLT_IsoMu20_eta2p1_v1", # not prescaled
            "HLT_Mu15_v4", "HLT_Mu20_v3", "HLT_Mu24_v3", "HLT_Mu30_v3", "HLT_IsoMu15_v9", "HLT_IsoMu17_v9", "HLT_IsoMu17_eta2p1_v1", # prescaled
            ],
        "runs": (167039, 167043), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-PromptReco-v4/AOD",
                "number_of_jobs": 1000, # Adjusted for PATtuple file size (~40 in reality)
                "lumiMask": "PromptReco"
            },
        }
    },
    "SingleMu_167078-167913_Prompt": {
        "dataVersion": "42Xdata",
        "args": {"doTauHLTMatching": 0},
        "triggerOR": [
            "HLT_Mu40_v3", "HLT_IsoMu24_v7", "HLT_IsoMu20_eta2p1_v1", # not prescaled
            "HLT_Mu15_v6", "HLT_Mu20_v5", "HLT_Mu24_v5", "HLT_Mu30_v5", "HLT_IsoMu15_v11", "HLT_IsoMu17_v11", "HLT_IsoMu17_eta2p1_v1", # prescaled
            ],
        "runs": (167078, 167913), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-PromptReco-v4/AOD",
                "number_of_jobs": 1000, # Adjusted for PATtuple file size (~330 in reality)
                "lumiMask": "PromptReco"
            },
        }
    },
    "SingleMu_172620-173198_Prompt": {
        "dataVersion": "42Xdata",
        "args": {"doTauHLTMatching": 0},
        "triggerOR": [
            "HLT_Mu40_v5", "HLT_IsoMu24_v8", # not prescaled
            "HLT_Mu15_v8", "HLT_Mu20_v7", "HLT_Mu24_v7", "HLT_Mu30_v7", "HLT_IsoMu15_v13", "HLT_IsoMu17_v13", # prescaled
            ],
        "runs": (172620, 173198), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-PromptReco-v6/AOD",
                "number_of_jobs": 1000, # Adjusted for PATtuple file size (~330 in reality)
                "lumiMask": "PromptReco"
            },
        }
    },
    "SingleMu_173236-173692_Prompt": {
        "dataVersion": "42Xdata",
        "args": {"doTauHLTMatching": 0},
        "triggerOR": [
            "HLT_Mu40_eta2p1_v1", "HLT_IsoMu30_eta2p1_v3", # not prescaled
            "HLT_Mu15_v9", "HLT_Mu20_v8", "HLT_Mu24_v8", "HLT_Mu30_v8", "HLT_Mu40_v6", "HLT_Mu24_eta2p1_v1", "HLT_Mu30_eta2p1_v1",
            "HLT_IsoMu17_v14", "HLT_IsoMu20_v9", "HLT_IsoMu24_v9", "HLT_IsoMu24_eta2p1_v3", # prescaled
            ],
        "runs": (173236, 173692), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-PromptReco-v6/AOD",
                "number_of_jobs": 1000, # Adjusted for PATtuple file size (~330 in reality)
                "lumiMask": "PromptReco"
            },
        }
    },
    "SingleMu_175860-176469_Prompt": {
        "dataVersion": "42Xdata",
        "args": {"doTauHLTMatching": 0},
        "triggerOR": [
            "HLT_Mu40_eta2p1_v1", "HLT_IsoMu30_eta2p1_v3", # not prescaled
            "HLT_Mu15_v9", "HLT_Mu20_v8", "HLT_Mu24_v8", "HLT_Mu30_v8", "HLT_Mu40_v6", "HLT_Mu24_eta2p1_v1", "HLT_Mu30_eta2p1_v1",
            "HLT_IsoMu15_v14", "HLT_IsoMu17_v14", "HLT_IsoMu20_v9", "HLT_IsoMu24_v9", "HLT_IsoMu15_eta2p1_v1", "HLT_IsoMu24_eta2p1_v3", # prescaled
            ],
        "runs": (175860, 176469), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011B-PromptReco-v1/AOD",
                "number_of_jobs": 490, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
        }
    },
    "SingleMu_176545-177053_Prompt": { # split because of much data (in the boundary of /cdaq/physics/Run2011/3e33/v2.3/HLT/V2 and /cdaq/physics/Run2011/3e33/v3.0/HLT/V2)
        "dataVersion": "42Xdata",
        "args": {"doTauHLTMatching": 0},
        "triggerOR": [
            "HLT_Mu40_eta2p1_v1", "HLT_IsoMu30_eta2p1_v3", # not prescaled
            "HLT_Mu15_v9", "HLT_Mu20_v8", "HLT_Mu24_v8", "HLT_Mu30_v8", "HLT_Mu40_v6", "HLT_Mu24_eta2p1_v1", "HLT_Mu30_eta2p1_v1",
            "HLT_IsoMu15_v14", "HLT_IsoMu17_v14", "HLT_IsoMu20_v9", "HLT_IsoMu24_v9", "HLT_IsoMu15_eta2p1_v1", "HLT_IsoMu24_eta2p1_v3", # prescaled
            ],
        "runs": (176545, 177053), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011B-PromptReco-v1/AOD",
                "number_of_jobs": 490, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
        }
    },
    "SingleMu_177074-177452_Prompt": { # split because of much data (in the boundary of /cdaq/physics/Run2011/3e33/v3.1/HLT/V1 and /cdaq/physics/Run2011/3e33/v4.0/HLT/V2)
        "dataVersion": "42Xdata",
        "args": {"doTauHLTMatching": 0},
        "triggerOR": [
            "HLT_Mu40_eta2p1_v1", "HLT_IsoMu30_eta2p1_v3", # not prescaled
            "HLT_Mu15_v9", "HLT_Mu20_v8", "HLT_Mu24_v8", "HLT_Mu30_v8", "HLT_Mu40_v6", "HLT_Mu24_eta2p1_v1", "HLT_Mu30_eta2p1_v1",
            "HLT_IsoMu15_v14", "HLT_IsoMu17_v14", "HLT_IsoMu20_v9", "HLT_IsoMu24_v9", "HLT_IsoMu15_eta2p1_v1", "HLT_IsoMu24_eta2p1_v3", # prescaled
            ],
        "runs": (177074, 177452), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011B-PromptReco-v1/AOD",
                "number_of_jobs": 440, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
        }
    },
    "SingleMu_177718-178380_Prompt": {
        "dataVersion": "42Xdata",
        "args": {"doTauHLTMatching": 0},
        "triggerOR": [
            "HLT_Mu40_eta2p1_v1", "HLT_IsoMu30_eta2p1_v3", # not prescaled
            "HLT_Mu15_v9", "HLT_Mu20_v8", "HLT_Mu24_v8", "HLT_Mu30_v8", "HLT_Mu40_v6", "HLT_Mu24_eta2p1_v1", "HLT_Mu30_eta2p1_v1",
            "HLT_IsoMu15_v14", "HLT_IsoMu17_v14", "HLT_IsoMu20_v9", "HLT_IsoMu24_v9", "HLT_IsoMu15_eta2p1_v1", "HLT_IsoMu24_eta2p1_v3", # prescaled
            ],
        "runs": (177718, 178380), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011B-PromptReco-v1/AOD",
                "number_of_jobs": 490, # Adjusted for PATtuple file size
                "lumiMask": "PromptReco"
            },
        }
    },
    "SingleMu_178420-179411_Prompt": {
        "dataVersion": "42Xdata",
        "args": {"doTauHLTMatching": 0},
        "triggerOR": [
            "HLT_Mu40_eta2p1_v4", "HLT_IsoMu30_eta2p1_v6", # not prescaled
            "HLT_Mu15_v12", "HLT_Mu20_v11", "HLT_Mu24_v11", "HLT_Mu30_v11", "HLT_Mu40_v9", 
            "HLT_IsoMu15_v17", "HLT_IsoMu20_v12", "HLT_IsoMu24_v12", "HLT_IsoMu15_eta2p1_v4", "HLT_IsoMu24_eta2p1_v6", # prescaled
            ],
        "runs": (178420, 179411), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011B-PromptReco-v1/AOD",
                "number_of_jobs": 600,  # Adjusted for PATtuple file size
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
    "SingleMu_Mu_178420-179411_Prompt": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_Mu40_eta2p1_v4",
        "runs": (178420, 179411), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011B-PromptReco-v1/AOD",
                "number_of_jobs": 190, # Adjusted for skim file size
                "lumiMask": "PromptReco"
            },
        }
    },
}
