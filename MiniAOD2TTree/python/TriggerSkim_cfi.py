import FWCore.ParameterSet.Config as cms

trgskim = cms.EDFilter("TriggerSkim",
    TriggerResults = cms.InputTag("TriggerResults::HLT"),
    HLTPaths       = cms.vstring("HLT_LooseIsoPFTau50_Trk30_eta2p1_v"),
    GenWeights     = cms.VPSet()
)
