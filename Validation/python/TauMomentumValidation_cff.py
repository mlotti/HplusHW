import FWCore.ParameterSet.Config as cms

from HiggsAnalysis.Validation.MomentumValidation_cfi import *

validatePatHPSTau = MomentumValidation.clone()
validatePatHPSTau.src = cms.InputTag("selectedPatTausHpsPFTau")

validatePatHPSTauTriggerMatch = MomentumValidation.clone()
validatePatHPSTauTriggerMatch.src = cms.InputTag("selectedPatTausHpsPFTauTauTriggerMatched")

validatePatHPSTauTriggerMatchCleaned = MomentumValidation.clone()
validatePatHPSTauTriggerMatchCleaned.src = cms.InputTag("selectedPatTausHpsPFTauTauTriggerMatchedAndJetTriggerCleaned")

validateTriggerTaus = MomentumValidation.clone()
validateTriggerTaus.src = cms.InputTag("patTrigger")

TauMomentumValidation = cms.Sequence(
    validatePatHPSTau*
    validatePatHPSTauTriggerMatch*
    validatePatHPSTauTriggerMatchCleaned*
    validateTriggerTaus
)
