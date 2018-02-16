import FWCore.ParameterSet.Config as cms

PUInfo = cms.EDAnalyzer('PUInfo',
    OutputFileName = cms.string("PileUp.root"),
#    PileupSummaryInfoSrc = cms.InputTag("addPileupInfo")
    PileupSummaryInfoSrc = cms.InputTag("slimmedAddPileupInfo"),
    RunOnData = cms.untracked.bool(True)
)

PUInfoPS = cms.EDAnalyzer('PUInfo',
    OutputFileName = cms.string("PileUpPS.root"),
    PileupSummaryInfoSrc = cms.InputTag("offlineSlimmedPrimaryVertices"),
    RunOnData = cms.untracked.bool(True)
)

