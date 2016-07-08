import FWCore.ParameterSet.Config as cms

PickEvents = cms.EDAnalyzer("PickEventsDumper",
    FileName = cms.untracked.string("pickEvents.txt")
)
