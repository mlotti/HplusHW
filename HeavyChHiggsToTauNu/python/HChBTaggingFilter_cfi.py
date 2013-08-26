import FWCore.ParameterSet.Config as cms

import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
hPlusBTaggingPtrSelectorFilter = cms.EDFilter("HPlusBTaggingPtrSelectorFilter",
    btagging = param.bTagging.clone(),
    jetSrc = cms.InputTag("insert_collection_name_here"),
    histogramAmbientLevel = cms.untracked.string("Debug"),
    filter = cms.bool(True),
    throw = cms.untracked.bool(True),
    eventCounter = param.eventCounter.clone()
)
