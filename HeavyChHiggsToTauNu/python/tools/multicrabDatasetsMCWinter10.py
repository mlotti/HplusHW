import multicrabDatasetsCommon as common

datasets = {

    # Electroweak MadGraph
    # Cross sections are from https://twiki.cern.ch/twiki/bin/view/CMS/CrossSections_3XSeries
    "TTJets_TuneZ2_Winter10": {
        "dataVersion": "39Xredigi",
        "crossSection": 165,
        "tauIDFactorizationMap": "FactorizationMaphistograms_TTJets_TuneZ2_Winter10_cfi",
        "data": {
        },
    }, 
    "TTJets_TuneD6T_Winter10": {
        "dataVersion": "39Xredigi",
        "crossSection": 165,
        "data": {
        },
    },
    "WJets_TuneZ2_Winter10": {
        "dataVersion": "39Xredigi",
        "crossSection": 28000,
        "tauIDFactorizationMap": "FactorizationMaphistograms_WJets_TuneZ2_Winter10_cfi",
        "data": {
        },
    },
    "WJets_TuneD6T_Winter10": {
        "dataVersion": "39Xredigi",
        "crossSection": 28000,
        "data": {
        },
    },
    # Drell-Yan
    "DYJetsToLL_M50_TuneZ2_Winter10": { # Z+jets
        "dataVersion": "39Xredigi",
        "crossSection": 2800,
        "data": {
        }
    },
    # Single top
    "TToBLNu_s-channel_TuneZ2_Winter10": {
        "dataVersion": "39Xredigi",
        "crossSection": 4.6*0.32442,
        "data": {
        },
    },
    "TToBLNu_t-channel_TuneZ2_Winter10": {
        "dataVersion": "39Xredigi",
        "crossSection": 63*0.32442,
        "data": {
        },
    },
    "TToBLNu_tW-channel_TuneZ2_Winter10": {
        "dataVersion": "39Xredigi",
        "crossSection": 10.6,
        "data": {
        },
    },

    # Backgrounds for electroweak background measurement
    # Cross section is from https://twiki.cern.ch/twiki/bin/view/CMS/ReProcessingWinter2010
    "QCD_Pt20_MuEnriched_TuneZ2_Winter10": {
        "dataVersion": "39Xredigi",
        "crossSection": 296600000.*0.0002855,
        "data": {
        },
    },
}
