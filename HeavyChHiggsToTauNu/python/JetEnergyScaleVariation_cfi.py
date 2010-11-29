import FWCore.ParameterSet.Config as cms

jesVariation = cms.EDProducer("JetEnergyScaleVariation",
    tauSrc = cms.InputTag("selectedPatTausShrinkingConePFTauTauTriggerMatched"),
    jetSrc = cms.InputTag("selectedPatJets"),
    metSrc = cms.InputTag("patMETs"),
    JESVariation = cms.double("0.05") # use sign, +/-
)

#JESPlus05 = jesVariation.clone()
#JESPlus05.JESVariation = cms.double("0.05")
#
#JESMinus05 = jesVariation.clone()
#JESMinus05.JESVariation = cms.double("-0.05")

# CaloRecoTau
JESPlus05CaloRecoTau = jesVariation.clone()
JESPlus05CaloRecoTau.JESVariation = cms.double("0.05")
JESPlus05CaloRecoTau.tauSrc = cms.InputTag("selectedPatTausCaloRecoTauTauTriggerMatched")

JESMinus05CaloRecoTau = jesVariation.clone()
JESMinus05CaloRecoTau.JESVariation = cms.double("-0.05")
JESMinus05CaloRecoTau.tauSrc = cms.InputTag("selectedPatTausCaloRecoTauTauTriggerMatched")

# PF Shrinking Cone
JESPlus05ShrinkingConePFTau = jesVariation.clone()
JESPlus05ShrinkingConePFTau.JESVariation = cms.double("0.05")
JESPlus05ShrinkingConePFTau.tauSrc = cms.InputTag("selectedPatTausShrinkingConePFTauTauTriggerMatched")

JESMinus05ShrinkingConePFTau = jesVariation.clone()
JESMinus05ShrinkingConePFTau.JESVariation = cms.double("-0.05")
JESMinus05ShrinkingConePFTau.tauSrc = cms.InputTag("selectedPatTausShrinkingConePFTauTauTriggerMatched")

# TaNC
JESPlus05ShrinkingConeTaNC = jesVariation.clone()
JESPlus05ShrinkingConeTaNC.JESVariation = cms.double("0.05")
JESPlus05ShrinkingConeTaNC.tauSrc = cms.InputTag("selectedPatTausShrinkingConePFTauTauTriggerMatched")

JESMinus05ShrinkingConeTaNC = jesVariation.clone()
JESMinus05ShrinkingConeTaNC.JESVariation = cms.double("-0.05")
JESMinus05ShrinkingConeTaNC.tauSrc = cms.InputTag("selectedPatTausShrinkingConePFTauTauTriggerMatched")

# HPS
JESPlus05ShrinkingConeTaNC = jesVariation.clone()
JESPlus05ShrinkingConeTaNC.JESVariation = cms.double("0.05")
JESPlus05ShrinkingConeTaNC.tauSrc = cms.InputTag("selectedPatTausHpsPFTauTauTriggerMatched")

JESMinus05ShrinkingConeTaNC = jesVariation.clone()
JESMinus05ShrinkingConeTaNC.JESVariation = cms.double("-0.05")
JESMinus05ShrinkingConeTaNC.tauSrc = cms.InputTag("selectedPatTausHpsPFTauTauTriggerMatched")


### Define the Sequence
JESsequence = cms.Sequence( JESPlus05CaloRecoTau * JESMinus05CaloRecoTau * JESPlus05ShrinkingConePFTau * JESMinus05ShrinkingConePFTau * JESPlus05ShrinkingConeTaNC * JESMinus05ShrinkingConeTaNC * JESPlus05ShrinkingConeTaNC * JESMinus05ShrinkingConeTaNC )
#JESsequence = cms.Sequence(JESPlus05 * JESMinus05)
