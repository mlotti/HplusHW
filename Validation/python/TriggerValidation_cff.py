import FWCore.ParameterSet.Config as cms

from HiggsAnalysis.Validation.TriggerTauValidation_cfi import *

TriggerValidation = cms.Sequence(
    TriggerTauValidation
)
