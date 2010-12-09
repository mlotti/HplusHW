import FWCore.ParameterSet.Config as cms

TriggerEmulationEfficiency = cms.untracked.PSet(
    L1TauSrc            = cms.InputTag("l1extraParticles", "Tau"),
    L1CenSrc            = cms.InputTag("l1extraParticles", "Central"),

    tauSrc              = cms.InputTag("caloTauHLTTauEmu"),

    metSrc              = cms.InputTag("patMETs")	
)
