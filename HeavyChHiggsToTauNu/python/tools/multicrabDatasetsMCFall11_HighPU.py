## \package multicrabDatasetsMCFall11
#
# Dataset definitions for Fall11 MC production (CMSSW 44x)
#
# \see multicrab

import multicrabDatasetsCommon as common

# For pattuples: ~10kev/job (~20-30 kB/event on average, depending on the process)
# For analysis: ~500kev/job

# Default signal cross section taken the same as ttbar

## Dataset definitions
datasets = {
    # Signal WH
    "TTToHplusBWB_M90_Fall11_HighPU": {
        "dataVersion": "44Xmc_highPU",
        "crossSection": 165,
        "data": {
            "AOD": {
#                "datasetpath": "/TTToHplusBWB_M-90_7TeV-pythia6-tauola/Fall11-E7TeV_Ave23_50ns-v2/AODSIM",
                "datasetpath": "/TTToHplusBWB_M-90_7TeV-pythia6-tauola/Fall11-E7TeV_Ave32_50ns-v2/GEN-SIM-RAW-HLTDEBUG-RECO",
                "number_of_jobs": 42, # Adjusted for PATtuple file size
            },
        }
    },
    "TTToHplusBWB_M160_Fall11_HighPU": {
        "dataVersion": "44Xmc_highPU",
        "crossSection": 165,
        "data": {
            "AOD": {
#                "datasetpath": "/TTToHplusBWB_M-160_7TeV-pythia6-tauola/Fall11-E7TeV_Ave23_50ns-v2/AODSIM",
                "datasetpath": "/TTToHplusBWB_M-160_7TeV-pythia6-tauola/Fall11-E7TeV_Ave32_50ns-v2/GEN-SIM-RAW-HLTDEBUG-RECO",
                "number_of_jobs": 42, # Adjusted for PATtuple file size
            },
        }
    },

    # EWK MadGraph
    # Cross sections from
    # [1] https://twiki.cern.ch/twiki/bin/view/CMS/CrossSections_3XSeries
    # [2] https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSections
    "TTJets_TuneZ2_Fall11_HighPU": {
        "dataVersion": "44Xmc_highPU",
        "crossSection": 165, # [1,2], approx. NNLO
        "args": { "triggerMC": "1" },
# Do not skim jets if one wants to understand full PU effect
#        "skimConfig": ["SkimFourJets_cff", "SkimFourJetsChs_cff"],
        "data": {
            "AOD": {
#                "datasetpath": "/TTJets_TuneZ2_7TeV-madgraph-tauola/Fall11-E7TeV_Ave23_50ns-v1/AODSIM",
                "datasetpath": "/TTJets_TuneZ2_7TeV-madgraph-tauola/Fall11-E7TeV_Ave32_50ns-v2/GEN-SIM-RAW-HLTDEBUG-RECO",
                "number_of_jobs": 141, # Adjusted for PATtuple file size ; expected output max. 31 MB/file
            },
        },
    },

}
