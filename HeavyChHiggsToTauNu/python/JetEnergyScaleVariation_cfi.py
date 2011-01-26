import FWCore.ParameterSet.Config as cms

jesVariation = cms.EDProducer("JetEnergyScaleVariation",
    tauSrc = cms.InputTag("selectedPatTausShrinkingConePFTauTauTriggerMatched"),
    jetSrc = cms.InputTag("selectedPatJets"),
    metSrc = cms.InputTag("patMETs"),
    JESVariation = cms.double(0.05) # use sign, +/-
)
