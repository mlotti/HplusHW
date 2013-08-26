import FWCore.ParameterSet.Config as cms

from HiggsAnalysis.Validation.MomentumValidation_cfi import *

validatePatHPSTau = MomentumValidation.clone()
validatePatHPSTau.src = cms.InputTag("selectedPatTausHpsPFTau")

validatePatHPSTauTriggerMatch = MomentumValidation.clone()
validatePatHPSTauTriggerMatch.src = cms.InputTag("selectedPatTausHpsPFTauTauTriggerMatched")

validatePatHPSTauTriggerMatchCleaned = MomentumValidation.clone()
validatePatHPSTauTriggerMatchCleaned.src = cms.InputTag("selectedPatTausHpsPFTauTauTriggerMatchedAndJetTriggerCleaned")

hltTauObjects = cms.EDFilter("PATTriggerObjectStandAloneSelector",
    src = cms.InputTag("patTrigger"),
    cut = cms.string("hasFilterId(84) && hasPathName('HLT_SingleIsoTau20_Trk15_MET25_v4')")
)
validateTriggerTaus = MomentumValidation.clone()
validateTriggerTaus.src = cms.InputTag("hltTauObjects")

TauMomentumValidation = cms.Sequence(
    validatePatHPSTau *
    validatePatHPSTauTriggerMatch *
    validatePatHPSTauTriggerMatchCleaned *
    hltTauObjects *
    validateTriggerTaus
)
