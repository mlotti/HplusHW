import FWCore.ParameterSet.Config as cms

from HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff import bTagging
hPlusBTaggingPtrSelectorFilter = cms.EDFilter(
    "HPlusBTaggingPtrSelectorFilter",
    btagging = bTagging.clone(),
    jetSrc = cms.InputTag("insert_collection_name_here"),
    filter = cms.bool(True),
    throw = cms.untracked.bool(True)
)
