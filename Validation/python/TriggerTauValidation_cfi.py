import FWCore.ParameterSet.Config as cms

TriggerTauValidation = cms.EDAnalyzer('TriggerObjectValidation',
    src = cms.InputTag("hltTriggerSummaryAOD"),
    id  = cms.int32(15)
)
