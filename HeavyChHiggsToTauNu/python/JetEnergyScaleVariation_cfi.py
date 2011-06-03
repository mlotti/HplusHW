import FWCore.ParameterSet.Config as cms

jesVariation = cms.EDProducer("JetEnergyScaleVariation",
    tauSrc = cms.InputTag("selectedPatTausShrinkingConePFTauTauTriggerMatched"),
    jetSrc = cms.InputTag("selectedPatJets"),
    metSrc = cms.InputTag("patMETs"),
    JESVariation = cms.double(0.03), # use sign, +/-
    JESEtaVariation = cms.double(0.02), # takes the sign from JESVariation
    unclusteredMETVariation = cms.double(0.10), # use sign, +/-
    jetVariationMode = cms.string("all"), # all, onlyTauMatching, onlyNoTauMatching
    tauJetMatchingDR = cms.double(0.5)
)
