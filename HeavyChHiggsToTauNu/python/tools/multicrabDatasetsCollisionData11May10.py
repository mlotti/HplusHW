import multicrabDatasetsCommon as common

datasets = {
    # Single tau + MET
    "Tau_160431-161176_May10": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_MET45_v1",
        "runs": (160431, 161176), #
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011A-May10ReReco-v1/AOD",
                "number_of_jobs": 15, # Adjusted for PATtuple file size
                "lumiMask": "May10ReReco"
            },
            "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_May10ReReco_v1_AOD_160431_pattuple_v17-377a23a99017553e73fe517f9c607b59/USER",
                "luminosity": 5.884518,
                "number_of_jobs": 1
            },
            "pattuple_v18": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-May10ReReco_v1_AOD_160431_pattuple_v18-344241722cb53b6dc9e6433dfd125850/USER",
                "luminosity": 6.625000,
                "number_of_jobs": 1
            },
        }
    },
    "Tau_161119-161119_May10_Wed": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_MET45_v1",
        "runs": (161119, 161119), #
        "data": {
            "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_May10ReReco_v1_AOD_161119_pattuple_v17-377a23a99017553e73fe517f9c607b59/USER",
                "luminosity": 0.490643,
                "number_of_jobs": 1
            },
        }
    },        
    "Tau_161217-163261_May10": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_MET45_v2",
        "runs": (161217, 163261),
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011A-May10ReReco-v1/AOD",
                "number_of_jobs": 100, # Adjusted for PATtuple file size
                "lumiMask": "May10ReReco"
            },
            "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_May10ReReco_v1_AOD_161217_pattuple_v17-e4cfe64c6b123ecde897f0b19cc05328/USER",
                "luminosity": 38.518306,
                "number_of_jobs": 2
            },
            "pattuple_v18": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-May10ReReco_v1_AOD_161217_pattuple_v18-69a11d04d01ec96141c740547251864b/USER",
                "luminosity": 40.762000,
                "number_of_jobs": 1
            },
        },
    },
    "Tau_163270-163869_May10": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_IsoPFTau35_Trk20_MET45_v4",
        "runs": (163270, 163869),
        "data": {
            "AOD": {
                "datasetpath": "/Tau/Run2011A-May10ReReco-v1/AOD",
                "number_of_jobs": 220,
                "lumiMask": "May10ReReco"
            },
            "pattuple_v17": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-Run2011A_May10ReReco_v1_AOD_163270_pattuple_v17-6d098da292fab19f3d03a84563841e91/USER",
                "luminosity": 159.758105,
                "number_of_jobs": 6
            },
            "pattuple_v18": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tau/local-May10ReReco_v1_AOD_163270_pattuple_v18-62e2e156bbf332fdc6c67ab8a6d7a4f0/USER",
                "luminosity": 167.786000,
                "number_of_jobs": 2
            },
        }
    },

    # Single Mu
    "SingleMu_160431-163261_May10": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_Mu20_v1",
        "runs": (160431, 163261),
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-May10ReReco-v1/AOD",
                "number_of_jobs": 120, # Adjusted for skim file size
                "lumiMask": "May10ReReco"
            },
        }
    }, 
    "SingleMu_161119-161119_May10_Wed": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_Mu20_v1",
        "runs": (161119, 161119),
        "data": {
        }
    },
   "SingleMu_163270-163869_May10": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_Mu24_v2",
        "runs": (163270, 163869),
        "data": {
            "AOD": {
                "datasetpath": "/SingleMu/Run2011A-May10ReReco-v1/AOD",
                "number_of_jobs": 140, # Adjusted for skim file size
                "lumiMask": "May10ReReco"
            },
        },
    },
}
