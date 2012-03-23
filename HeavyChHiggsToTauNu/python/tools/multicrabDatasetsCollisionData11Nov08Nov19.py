## \package multicrabDatasetsCollisionData11Prompt
#
# Dataset definitions for Run2011 A Nov 08 rereco with 44x
#
# \see multicrab

import multicrabDatasetsCommon as common

## Dataset definitions
datasets = {
    # Single tau + MET
    "Tau_160431-167913_2011A_Nov08": {
        "dataVersion": "44Xdata",
        "args": {"triggerThrow": 0}, # needed for OR of triggers in separate run ranges
        "triggerOR": [
            "HLT_IsoPFTau35_Trk20_MET45_v1", # 160431-161176
            "HLT_IsoPFTau35_Trk20_MET45_v2", # 161216-163261
            "HLT_IsoPFTau35_Trk20_MET45_v4", # 163270-163869
            "HLT_IsoPFTau35_Trk20_MET45_v6", # 165088-165633
            "HLT_IsoPFTau35_Trk20_MET60_v2", # 165970-166164, 166374-167043
            "HLT_IsoPFTau35_Trk20_MET60_v3", # 166346
            "HLT_IsoPFTau35_Trk20_MET60_v4", # 167078-167913
        ],
        "runs": (160431, 167913),
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011A-08Nov2011-v1/AOD",
                "number_of_jobs": 300, # was 350+200+350
                "lumiMask": "DCSONLY11"
            },
        }
    },
    # break of range because of trigger eff. boundary
    "Tau_170722-173198_2011A_Nov08": {
        "dataVersion": "44Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_MET60_v6",
        "runs": (170722, 173198), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011A-08Nov2011-v1/AOD",
                "number_of_jobs": 70, # was 110+110
                "lumiMask": "DCSONLY11"
            },
        }
    },
    # break of range because of trigger eff. boundary
    "Tau_173236-173692_2011A_Nov08": {
        "dataVersion": "44Xdata",
        "trigger": "HLT_MediumIsoPFTau35_Trk20_MET60_v1",
        "runs": (173236, 173692), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011A-08Nov2011-v1/AOD",
                "number_of_jobs": 30, # was 90
                "lumiMask": "DCSONLY11"
            },
        }
    },
    # 2011 B
    "Tau_175860-180252_2011B_Nov19": {
        "dataVersion": "44Xdata",
        "args": {"triggerThrow": 0}, # needed for OR of triggers in separate run ranges
        "triggerOR": [
            "HLT_MediumIsoPFTau35_Trk20_MET60_v1", # 175860-178380
            "HLT_MediumIsoPFTau35_Trk20_MET60_v5", # 178420-179889
            "HLT_MediumIsoPFTau35_Trk20_MET60_v6", # 179959-180252
        ],
        "runs": (175860, 180252), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011B-19Nov2011-v1/AOD",
                "number_of_jobs": 300, # was 400+230+250
                "lumiMask": "DCSONLY11"
            },
        }
    },

    # Single tau (control)
    "Tau_Single_165970-167913_2011A_Nov08": {
        "dataVersion": "44Xdata",
        "args": {"triggerThrow": 0}, # needed for OR of triggers in separate run ranges
        "triggerOR": [
            "HLT_IsoPFTau35_Trk20_v2", # 165970-166164, 166374-167043
            "HLT_IsoPFTau35_Trk20_v3", # 166346-166346
            "HLT_IsoPFTau35_Trk20_v4", # 167078-167913
        ],
        "runs": (165970, 167913), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011A-08Nov2011-v1/AOD",
                "number_of_jobs": 300, # use same number of jobs like for tau+met
                "lumiMask": "DCSONLY11"
            },
        }
    },
    "Tau_Single_170722-173198_2011A_Nov08": {
        "dataVersion": "44Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_v6",
        "runs": (170722, 173198), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011A-08Nov2011-v1/AOD",
                "number_of_jobs": 70,
                "lumiMask": "DCSONLY11"
            },
        }
    },
    "Tau_Single_173236-173692_2011A_Nov08": {
        "dataVersion": "44Xdata",
        "trigger": "HLT_MediumIsoPFTau35_Trk20_v1",
        "runs": (173236, 173692), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011A-08Nov2011-v1/AOD",
                "number_of_jobs": 30,
                "lumiMask": "DCSONLY11"
            },
        }
    },
    "Tau_Single_175832-177452_2011B_Nov19": {
        "dataVersion": "44Xdata",
        "args": {"triggerThrow": 0}, # needed for OR of triggers in separate run ranges
        "triggerOR": [
            "HLT_MediumIsoPFTau35_Trk20_v1", #175832-178380
            "HLT_MediumIsoPFTau35_Trk20_v5", #178420-179889
            "HLT_MediumIsoPFTau35_Trk20_v6", #179959-180252
        ],
        "runs": (175832, 177452), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011B-19Nov2011-v1/AOD",
                "number_of_jobs": 400, # was 400
                "lumiMask": "DCSONLY11"
            },
        }
    },

    # Single Mu
    "SingleMu_160431-163261_2011A_Nov08": {
        "dataVersion": "44Xdata",
        "args": {"doTauHLTMatching": 0},
        "triggerOR": [
            "HLT_Mu20_v1", "HLT_IsoMu12_v1", # not prescaled
            "HLT_Mu15_v2", # prescaled
            ],
        "runs": (160431, 163261),
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-08Nov2011-v1/AOD",
                "number_of_jobs": 1000, # Adjusted for PATtuple file size (~430 in reality)
                "lumiMask": "DCSONLY11"
            },
        }
    }, 
   "SingleMu_163270-163869_2011A_Nov08": {
        "dataVersion": "44Xdata",
        "args": {"doTauHLTMatching": 0},
        "triggerOR": [
            "HLT_Mu24_v2", "HLT_IsoMu17_v6", # not prescaled
            "HLT_Mu15_v3", "HLT_Mu20_v2", "HLT_IsoMu15_v6", # prescaled
            ],
        "runs": (163270, 163869),
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-08Nov2011-v1/AOD",
                "number_of_jobs": 1000, # Adjusted for PATtuple file size (~390 in reality)
                "lumiMask": "DCSONLY11"
            },
        },
    },
    "SingleMu_165088-165633_2011A_Nov08": {
        "dataVersion": "44Xdata",
        "args": {"doTauHLTMatching": 0},
        "triggerOR": [
            "HLT_Mu30_v3", "HLT_IsoMu17_v8", # not prescaled
            "HLT_Mu15_v4", "HLT_Mu20_v3", "HLT_Mu24_v3", "HLT_IsoMu15_v8", # prescaled
            ],
        "runs": (165088, 165633), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-08Nov2011-v1/AOD",
                "number_of_jobs": 490, # Adjusted for PATtuple file size (~200 in reality)
                "lumiMask": "DCSONLY11"
            },
        }
    },
    "SingleMu_165970-166150_2011A_Nov08": {
        "dataVersion": "44Xdata",
        "args": {"doTauHLTMatching": 0},
        "triggerOR": [
            "HLT_Mu30_v3", "HLT_IsoMu24_v5", # not prescaled
            "HLT_Mu15_v4", "HLT_Mu20_v3", "HLT_Mu24_v3", "HLT_IsoMu15_v9", "HLT_IsoMu17_v9", # prescaled
            ],
        "runs": (165970, 166150), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-08Nov2011-v1/AOD",
                "number_of_jobs": 490, # Adjusted for PATtuple file size (~160 in reality)
                "lumiMask": "DCSONLY11"
            },
        }
    },
    "SingleMu_166161-166164_2011A_Nov08": {
        "dataVersion": "44Xdata",
        "args": {"doTauHLTMatching": 0},
        "triggerOR": [
            "HLT_Mu40_v1", "HLT_IsoMu24_v5", # not prescaled
            "HLT_Mu15_v4", "HLT_Mu20_v3", "HLT_Mu24_v3", "HLT_Mu30_v3", "HLT_IsoMu15_v9", "HLT_IsoMu17_v9", # prescaled
            ],
        "runs": (166161, 166164), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-08Nov2011-v1/AOD",
                "number_of_jobs": 20, # Adjusted for PATtuple file size (~10 in reality)
                "lumiMask": "DCSONLY11"
            },
        }
    },
    "SingleMu_166346-166346_2011A_Nov08": {
        "dataVersion": "44Xdata",
        "args": {"doTauHLTMatching": 0},
        "triggerOR": [
            "HLT_Mu40_v2", "HLT_IsoMu24_v6", # not prescaled
            "HLT_Mu15_v5", "HLT_Mu20_v4", "HLT_Mu24_v4", "HLT_Mu30_v4", "HLT_IsoMu15_v10", "HLT_IsoMu17_v10", # prescaled
            ],
        "runs": (166346, 166346), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-08Nov2011-v1/AOD",
                "number_of_jobs": 20, # Adjusted for PATtuple file size (~10 in reality)
                "lumiMask": "DCSONLY11"
            },
        }
    },
    "SingleMu_166374-166967_2011A_Nov08": {
        "dataVersion": "44Xdata",
        "args": {"doTauHLTMatching": 0},
        "triggerOR": [
            "HLT_Mu40_v1", "HLT_IsoMu24_v5", # not prescaled
            "HLT_Mu15_v4", "HLT_Mu20_v3", "HLT_Mu24_v3", "HLT_Mu30_v3", "HLT_IsoMu15_v9", "HLT_IsoMu17_v9", # prescaled
            ],
        "runs": (166374, 166967), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-08Nov2011-v1/AOD",
                "number_of_jobs": 1000, # Adjusted for PATtuple file size (~380 in reality)
                "lumiMask": "DCSONLY11"
            },
        }
    },
    "SingleMu_167039-167043_2011A_Nov08": {
        "dataVersion": "44Xdata",
        "args": {"doTauHLTMatching": 0},
        "triggerOR": [
            "HLT_Mu40_v1", "HLT_IsoMu24_v5", "HLT_IsoMu20_eta2p1_v1", # not prescaled
            "HLT_Mu15_v4", "HLT_Mu20_v3", "HLT_Mu24_v3", "HLT_Mu30_v3", "HLT_IsoMu15_v9", "HLT_IsoMu17_v9", "HLT_IsoMu17_eta2p1_v1", # prescaled
            ],
        "runs": (167039, 167043), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-08Nov2011-v1/AOD",
                "number_of_jobs": 1000, # Adjusted for PATtuple file size (~40 in reality)
                "lumiMask": "DCSONLY11"
            },
        }
    },
    "SingleMu_167078-167913_2011A_Nov08": {
        "dataVersion": "44Xdata",
        "args": {"doTauHLTMatching": 0},
        "triggerOR": [
            "HLT_Mu40_v3", "HLT_IsoMu24_v7", "HLT_IsoMu20_eta2p1_v1", # not prescaled
            "HLT_Mu15_v6", "HLT_Mu20_v5", "HLT_Mu24_v5", "HLT_Mu30_v5", "HLT_IsoMu15_v11", "HLT_IsoMu17_v11", "HLT_IsoMu17_eta2p1_v1", # prescaled
            ],
        "runs": (167078, 167913), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-08Nov2011-v1/AOD",
                "number_of_jobs": 1000, # Adjusted for PATtuple file size (~330 in reality)
                "lumiMask": "DCSONLY11"
            },
        }
    },
    "SingleMu_170722-172619_2011A_Nov08": {
        "dataVersion": "44Xdata",
        "args": {"doTauHLTMatching": 0},
        "triggerOR": [
            "HLT_Mu40_v5", "HLT_IsoMu24_v8", # not prescaled
            "HLT_Mu15_v8", "HLT_Mu20_v7", "HLT_Mu24_v7", "HLT_Mu30_v7", "HLT_IsoMu15_v13", "HLT_IsoMu17_v13", # prescaled
            ],
        "runs": (170722, 172619),
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-08Nov2011-v1/AOD",
                "number_of_jobs": 490, # Adjusted for PATtuple file size
                "lumiMask": "DCSONLY11"
            },
        }
    },
    "SingleMu_172620-173198_2011A_Nov08": {
        "dataVersion": "44Xdata",
        "args": {"doTauHLTMatching": 0},
        "triggerOR": [
            "HLT_Mu40_v5", "HLT_IsoMu24_v8", # not prescaled
            "HLT_Mu15_v8", "HLT_Mu20_v7", "HLT_Mu24_v7", "HLT_Mu30_v7", "HLT_IsoMu15_v13", "HLT_IsoMu17_v13", # prescaled
            ],
        "runs": (172620, 173198), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-DCSONLY11-v6/AOD",
                "number_of_jobs": 1000, # Adjusted for PATtuple file size (~330 in reality)
                "lumiMask": "DCSONLY11"
            },
        }
    },
    "SingleMu_173236-173692_2011A_Nov08": {
        "dataVersion": "44Xdata",
        "args": {"doTauHLTMatching": 0},
        "triggerOR": [
            "HLT_Mu40_eta2p1_v1", "HLT_IsoMu30_eta2p1_v3", # not prescaled
            "HLT_Mu15_v9", "HLT_Mu20_v8", "HLT_Mu24_v8", "HLT_Mu30_v8", "HLT_Mu40_v6", "HLT_Mu24_eta2p1_v1", "HLT_Mu30_eta2p1_v1",
            "HLT_IsoMu17_v14", "HLT_IsoMu20_v9", "HLT_IsoMu24_v9", "HLT_IsoMu24_eta2p1_v3", # prescaled
            ],
        "runs": (173236, 173692), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-DCSONLY11-v6/AOD",
                "number_of_jobs": 1000, # Adjusted for PATtuple file size (~330 in reality)
                "lumiMask": "DCSONLY11"
            },
        }
    },
    "SingleMu_175860-176469_2011B_Nov19": {
        "dataVersion": "44Xdata",
        "args": {"doTauHLTMatching": 0},
        "triggerOR": [
            "HLT_Mu40_eta2p1_v1", "HLT_IsoMu30_eta2p1_v3", # not prescaled
            "HLT_Mu15_v9", "HLT_Mu20_v8", "HLT_Mu24_v8", "HLT_Mu30_v8", "HLT_Mu40_v6", "HLT_Mu24_eta2p1_v1", "HLT_Mu30_eta2p1_v1",
            "HLT_IsoMu15_v14", "HLT_IsoMu17_v14", "HLT_IsoMu20_v9", "HLT_IsoMu24_v9", "HLT_IsoMu15_eta2p1_v1", "HLT_IsoMu24_eta2p1_v3", # prescaled
            ],
        "runs": (175860, 176469), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011B-19Nov2011-v1/AOD",
                "number_of_jobs": 490, # Adjusted for PATtuple file size
                "lumiMask": "DCSONLY11"
            },
        }
    },
    "SingleMu_176545-177053_2011B_Nov19": { # split because of much data (in the boundary of /cdaq/physics/Run2011/3e33/v2.3/HLT/V2 and /cdaq/physics/Run2011/3e33/v3.0/HLT/V2)
        "dataVersion": "44Xdata",
        "args": {"doTauHLTMatching": 0},
        "triggerOR": [
            "HLT_Mu40_eta2p1_v1", "HLT_IsoMu30_eta2p1_v3", # not prescaled
            "HLT_Mu15_v9", "HLT_Mu20_v8", "HLT_Mu24_v8", "HLT_Mu30_v8", "HLT_Mu40_v6", "HLT_Mu24_eta2p1_v1", "HLT_Mu30_eta2p1_v1",
            "HLT_IsoMu15_v14", "HLT_IsoMu17_v14", "HLT_IsoMu20_v9", "HLT_IsoMu24_v9", "HLT_IsoMu15_eta2p1_v1", "HLT_IsoMu24_eta2p1_v3", # prescaled
            ],
        "runs": (176545, 177053), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011B-19Nov2011-v1/AOD",
                "number_of_jobs": 490, # Adjusted for PATtuple file size
                "lumiMask": "DCSONLY11"
            },
        }
    },
    "SingleMu_177074-177452_2011B_Nov19": { # split because of much data (in the boundary of /cdaq/physics/Run2011/3e33/v3.1/HLT/V1 and /cdaq/physics/Run2011/3e33/v4.0/HLT/V2)
        "dataVersion": "44Xdata",
        "args": {"doTauHLTMatching": 0},
        "triggerOR": [
            "HLT_Mu40_eta2p1_v1", "HLT_IsoMu30_eta2p1_v3", # not prescaled
            "HLT_Mu15_v9", "HLT_Mu20_v8", "HLT_Mu24_v8", "HLT_Mu30_v8", "HLT_Mu40_v6", "HLT_Mu24_eta2p1_v1", "HLT_Mu30_eta2p1_v1",
            "HLT_IsoMu15_v14", "HLT_IsoMu17_v14", "HLT_IsoMu20_v9", "HLT_IsoMu24_v9", "HLT_IsoMu15_eta2p1_v1", "HLT_IsoMu24_eta2p1_v3", # prescaled
            ],
        "runs": (177074, 177452), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011B-19Nov2011-v1/AOD",
                "number_of_jobs": 440, # Adjusted for PATtuple file size
                "lumiMask": "DCSONLY11"
            },
        }
    },
    "SingleMu_177718-178380_2011B_Nov19": {
        "dataVersion": "44Xdata",
        "args": {"doTauHLTMatching": 0},
        "triggerOR": [
            "HLT_Mu40_eta2p1_v1", "HLT_IsoMu30_eta2p1_v3", # not prescaled
            "HLT_Mu15_v9", "HLT_Mu20_v8", "HLT_Mu24_v8", "HLT_Mu30_v8", "HLT_Mu40_v6", "HLT_Mu24_eta2p1_v1", "HLT_Mu30_eta2p1_v1",
            "HLT_IsoMu15_v14", "HLT_IsoMu17_v14", "HLT_IsoMu20_v9", "HLT_IsoMu24_v9", "HLT_IsoMu15_eta2p1_v1", "HLT_IsoMu24_eta2p1_v3", # prescaled
            ],
        "runs": (177718, 178380), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011B-19Nov2011-v1/AOD",
                "number_of_jobs": 490, # Adjusted for PATtuple file size
                "lumiMask": "DCSONLY11"
            },
        }
    },
    "SingleMu_178420-178866_2011B_Nov19": { # split because of too much data (in the middle of /cdaq/physics/Run2011/5e33/v1.4/HLT/V5, splitting at the boundaries did not make sense)
        "dataVersion": "44Xdata",
        "args": {"doTauHLTMatching": 0},
        "triggerOR": [
            "HLT_Mu40_eta2p1_v4", "HLT_IsoMu30_eta2p1_v6", # not prescaled
            "HLT_Mu15_v12", "HLT_Mu20_v11", "HLT_Mu24_v11", "HLT_Mu30_v11", "HLT_Mu40_v9",
            "HLT_IsoMu15_v17", "HLT_IsoMu20_v12", "HLT_IsoMu24_v12", "HLT_IsoMu15_eta2p1_v4", "HLT_IsoMu24_eta2p1_v6", # prescaled
            ],
        "runs": (178420, 178866), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011B-19Nov2011-v1/AOD",
                "number_of_jobs": 500,  # Adjusted for PATtuple file size
                "lumiMask": "DCSONLY11"
            },
        }
    },
    "SingleMu_178871-179889_2011B_Nov19": { # split because of too much data (in the middle of /cdaq/physics/Run2011/5e33/v1.4/HLT/V5, splitting at the boundaries did not make sense)
        "dataVersion": "44Xdata",
        "args": {"doTauHLTMatching": 0},
        "triggerOR": [
            "HLT_Mu40_eta2p1_v4", "HLT_IsoMu30_eta2p1_v6", # not prescaled
            "HLT_Mu15_v12", "HLT_Mu20_v11", "HLT_Mu24_v11", "HLT_Mu30_v11", "HLT_Mu40_v9", 
            "HLT_IsoMu15_v17", "HLT_IsoMu20_v12", "HLT_IsoMu24_v12", "HLT_IsoMu15_eta2p1_v4", "HLT_IsoMu24_eta2p1_v6", # prescaled
            ],
        "runs": (178871, 179889), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011B-19Nov2011-v1/AOD",
                "number_of_jobs": 500,  # Adjusted for PATtuple file size
                "lumiMask": "DCSONLY11"
            },
        }
    },
    "SingleMu_179959-180252_2011B_Nov19": { # split because of too much data (in the middle of /cdaq/physics/Run2011/5e33/v1.4/HLT/V5, splitting at the boundaries did not make sense)
        "dataVersion": "44Xdata",
        "args": {"doTauHLTMatching": 0},
        "triggerOR": [
            "HLT_Mu40_eta2p1_v5", "HLT_IsoMu30_eta2p1_v7", # not prescaled
            "HLT_Mu15_v13", "HLT_Mu20_v12", "HLT_Mu24_v12", "HLT_Mu30_v12", "HLT_Mu40_v10",
            "HLT_IsoMu15_v18", "HLT_IsoMu20_v13", "HLT_IsoMu24_v13", "HLT_IsoMu15_eta2p1_v5", "HLT_IsoMu24_eta2p1_v7", # prescaled
            ],
        "runs": (179959, 180252), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011B-19Nov2011-v1/AOD",
                "number_of_jobs": 300,  # Adjusted for PATtuple file size
                "lumiMask": "DCSONLY11"
            },
        }
    },


    # Single Mu for tau embedding skims
    "SingleMu_Mu_160431-163261_2011A_Nov08": {
        "dataVersion": "44Xdata",
        "trigger": "HLT_Mu20_v1",
        "runs": (160431, 163261),
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-08Nov2011-v1/AOD",
                "number_of_jobs": 120, # Adjusted for skim file size
                "lumiMask": "DCSONLY11"
            },
        }
    }, 
    "SingleMu_Mu_163270-163869_2011A_Nov08": {
        "dataVersion": "44Xdata",
        "trigger": "HLT_Mu24_v2",
        "runs": (163270, 163869),
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-08Nov2011-v1/AOD",
                "number_of_jobs": 140, # Adjusted for skim file size
                "lumiMask": "May10ReReco"
            },
        },
    },

    "SingleMu_Mu_165088-166150_2011A_Nov08": {
        "dataVersion": "44Xdata",
        "trigger": "HLT_Mu30_v3",
        "runs": (165088, 166150), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-08Nov2011-v1/AOD",
                "number_of_jobs": 490, # Adjusted for skim file size
                "lumiMask": "DCSONLY11"
            },
        }
    },
    "SingleMu_Mu_165103-165103_2011A_Nov08": {
        "dataVersion": "44Xdata",
        "trigger": "HLT_Mu30_v3",
        "runs": (165103, 165103), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-08Nov2011-v1/AOD",
                "number_of_jobs": 1, # Adjusted for skim file size
                "lumiMask": "DCSONLY11WedDiff"
            },
        }
    },
    "SingleMu_Mu_166161-166164_2011A_Nov08": {
        "dataVersion": "44Xdata",
        "trigger": "HLT_Mu40_v1",
        "runs": (166161, 166164), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-08Nov2011-v1/AOD",
                "number_of_jobs": 2, # Adjusted for skim file size
                "lumiMask": "DCSONLY11"
            },
        }
    },
    "SingleMu_Mu_166346-166346_2011A_Nov08": {
        "dataVersion": "44Xdata",
        "trigger": "HLT_Mu40_v2",
        "runs": (166346, 166346), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-08Nov2011-v1/AOD",
                "number_of_jobs": 2, # Adjusted for skim file size
                "lumiMask": "DCSONLY11"
            },
        }
    },
    "SingleMu_Mu_166374-167043_2011A_Nov08": {
        "dataVersion": "44Xdata",
        "trigger": "HLT_Mu40_v1",
        "runs": (166374, 167043), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-08Nov2011-v1/AOD",
                "number_of_jobs": 300, # Adjusted for skim file size
                "lumiMask": "DCSONLY11"
            },
        }
    },
    "SingleMu_Mu_167078-167913_2011A_Nov08": {
        "dataVersion": "44Xdata",
        "trigger": "HLT_Mu40_v3",
        "runs": (167078, 167913), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-08Nov2011-v1/AOD",
                "number_of_jobs": 230, # Adjusted for skim file size
                "lumiMask": "DCSONLY11"
            },
        }
    },
    "SingleMu_Mu_170722-172619_2011A_Nov08": {
        "dataVersion": "44Xdata",
        "trigger": "HLT_Mu40_v5",
        "runs": (170722, 172619),
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-08Nov2011-v1/AOD",
                "number_of_jobs": 200,
                "lumiMask": "DCSONLY11"
            },
        }
    },
    "SingleMu_Mu_172620-173198_2011A_Nov08": {
        "dataVersion": "44Xdata",
        "trigger": "HLT_Mu40_v5",
        "runs": (172620, 173198), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-08Nov2011-v1/AOD",
                "number_of_jobs": 230, # Adjusted for skim file size
                "lumiMask": "DCSONLY11"
            },
        }
    },
    "SingleMu_Mu_173236-173692_2011A_Nov08": {
        "dataVersion": "44Xdata",
        "trigger": "HLT_Mu40_eta2p1_v1",
        "runs": (173236, 173692), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-08Nov2011-v1/AOD",
                "number_of_jobs": 120, # Adjusted for skim file size
                "lumiMask": "DCSONLY11"
            },
        }
    },
    "SingleMu_Mu_175860-177452_2011B_Nov19": {
        "dataVersion": "44Xdata",
        "trigger": "HLT_Mu40_eta2p1_v1",
        "runs": (175860, 177452), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011B-19Nov2011-v1/AOD",
                "number_of_jobs": 480, # Adjusted for skim file size
                "lumiMask": "DCSONLY11"
            },
        }
    },
    "SingleMu_Mu_177718-177878_2011B_Nov19": {
        "dataVersion": "44Xdata",
        "trigger": "HLT_Mu40_eta2p1_v1",
        "runs": (177718, 177878), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011B-19Nov2011-v1/AOD",
                "number_of_jobs": 300, # Adjusted for skim file size
                "lumiMask": "DCSONLY11"
            },
        }
    },
    "SingleMu_Mu_178420-179889_2011B_Nov19": {
        "dataVersion": "44Xdata",
        "trigger": "HLT_Mu40_eta2p1_v4",
        "runs": (178420, 179889), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011B-19Nov2011-v1/AOD",
                "number_of_jobs": 300, # Adjusted for skim file size
                "lumiMask": "DCSONLY11"
            },
        }
    },
    "SingleMu_Mu_179959-180252_2011B_Nov19": {
        "dataVersion": "44Xdata",
        "trigger": "HLT_Mu40_eta2p1_v5",
        "runs": (179959, 180252), # This is prompt RECO, so check the run range again when running!
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011B-19Nov2011-v1/AOD",
                "number_of_jobs": 60, # Adjusted for skim file size
                "lumiMask": "DCSONLY11"
            },
        }
    },
}
