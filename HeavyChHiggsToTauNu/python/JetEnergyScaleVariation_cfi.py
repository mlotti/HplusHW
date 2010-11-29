import FWCore.ParameterSet.Config as cms

jesVariation = cms.EDProducer("JetEnergyScaleVariation",
    tauSrc = cms.InputTag("selectedPatTausShrinkingConePFTauTauTriggerMatched"),
    jetSrc = cms.InputTag("selectedPatJets"),
    metSrc = cms.InputTag("patMETs"),
    JESVariation = cms.double("0.05") # use sign, +/-
)

JESPlus05 = jesVariation.clone()
JESPlus05.JESVariation = cms.double("0.05")

JESMinus05 = jesVariation.clone()
JESMinus05.JESVariation = cms.double("-0.05")

JESsequence = cms.Sequence(JESPlus05 * JESMinus05)
