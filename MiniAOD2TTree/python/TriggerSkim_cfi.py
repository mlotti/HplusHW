import FWCore.ParameterSet.Config as cms

trgskim = cms.EDFilter("TriggerSkim",
    TriggerResults = cms.InputTag("TriggerResults::HLT"),
    HLTPaths       = cms.vstring("HLT_IsoMu24_v","HLT_Ele27_eta2p1_WPTight_Gsf_v"),
    GenWeights     = cms.VPSet()
)
