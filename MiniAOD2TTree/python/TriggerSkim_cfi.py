import FWCore.ParameterSet.Config as cms

trgskim = cms.EDFilter("TriggerSkim",
    TriggerResults = cms.InputTag("TriggerResults::HLT"),
    HLTPaths       = cms.vstring("HLT_IsoMu20_v"),
    GenWeights     = cms.VPSet()
)
