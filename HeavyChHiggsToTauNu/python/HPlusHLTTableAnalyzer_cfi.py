import FWCore.ParameterSet.Config as cms

hltTableAnalyzer = cms.EDAnalyzer("HPlusHLTTableAnalyzer",
    hltProcessName = cms.untracked.string("HLT")
)
