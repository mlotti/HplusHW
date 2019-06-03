import FWCore.ParameterSet.Config as cms

PUInfo = cms.EDAnalyzer('PUInfo',
    OutputFileName = cms.string("PileUp.root"),
#    PileupSummaryInfoSrc = cms.InputTag("addPileupInfo")
    PileupSummaryInfoSrc = cms.InputTag("slimmedAddPileupInfo")
)
