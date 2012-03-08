## \package multicrabDatasetsMCFall11
#
# Dataset definitions for Fall11 MC production (CMSSW 42X)

import multicrabDatasetsCommon as common

# For pattuples: ~10kev/job (~20-30 kB/event on average, depending on the process)
# For analysis: ~500kev/job

# Default signal cross section taken the same as ttbar

## Dataset definitions
datasets = {
    # Signal WH
    "TTToHplusBWB_M120_Fall11": {
        "dataVersion": "dont_know_yet",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
                "number_of_jobs": 25, # Adjusted for PATtuple file size
            },
        }
    },
    "TTToHplusBWB_M140_Fall11": {
        "dataVersion": "dont_know_yet",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-140_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
                "number_of_jobs": 25, # Adjusted for PATtuple file size
            },
        }
    },
    "TTToHplusBWB_M160_Fall11": {
        "dataVersion": "dont_know_yet",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBWB_M-160_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
                "number_of_jobs": 25, # Adjusted for PATtuple file size
            },
        }
    },
    # Signal HH
    "TTToHplusBHminusB_M80_Fall11": {
        "dataVersion": "dont_know_yet",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBHminusB_M-80_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
                "number_of_jobs": 25, # Adjusted for PATtuple file size
            },
        }
    },
    "TTToHplusBHminusB_M140_Fall11": {
        "dataVersion": "dont_know_yet",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TTToHplusBHminusB_M-140_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
                "number_of_jobs": 25, # Adjusted for PATtuple file size
            },
        }
    },

    # Signal heavy
    "HplusTB_M180_Fall11": {
        "dataVersion": "dont_know_yet",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/HplusTB_M-180_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
                "number_of_jobs": 25, # Adjusted for PATtuple file size
            },
        }
    },


    # Cross sections https://twiki.cern.ch/twiki/bin/view/CMS/CrossSections_3XSeries
    "WZ_TuneZ2_Fall11": {
        "dataVersion": "dont_know_yet",
        "crossSection": 18.2,
        "data": {
            "AOD": {
                "datasetpath": "/WZ_TuneZ2_7TeV_pythia6_tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
                "number_of_jobs": 450, # Adjusted for PATtuple file size
            },
        },
    },
    "ZZ_TuneZ2_Fall11": {
        "dataVersion": "dont_know_yet",
        "crossSection": 5.9,
        "data": {
            "AOD": {
                "datasetpath": "/ZZ_TuneZ2_7TeV_pythia6_tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
                "number_of_jobs": 300, # Adjusted for PATtuple file size
            },
        },
    },


    # SingleTop Powheg
    # Cross sections from
    # https://twiki.cern.ch/twiki/bin/view/CMS/SingleTopMC2011
    # https://twiki.cern.ch/twiki/bin/view/CMS/SingleTopSigma
    "Tbar_tW-channel_TuneZ2_Fall11": {
        "dataVersion": "dont_know_yet",
        "crossSection": 7.87,
        "data": {
            "AOD": {
                "datasetpath": "/Tbar_TuneZ2_tW-channel-DS_7TeV-powheg-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
                "number_of_jobs": 80, # Adjusted for PATtuple file size
            },
        },
    },

}
