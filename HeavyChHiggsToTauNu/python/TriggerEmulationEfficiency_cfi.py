import FWCore.ParameterSet.Config as cms

TriggerEmulationEfficiency = cms.untracked.PSet(
    L1TauSrc            = cms.InputTag("l1extraParticles", "Tau"),
    L1CenSrc            = cms.InputTag("l1extraParticles", "Central"),

    tauSrc              = cms.InputTag("caloTauHLTTauEmu"),
    jetSrc              = cms.InputTag("ak5CaloJets"),
    pfjetSrc            = cms.InputTag("selectedPatJetsAK5PF"),
    metSrc              = cms.InputTag("patMETs")	
)
