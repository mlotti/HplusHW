import FWCore.ParameterSet.Config as cms

TriggerTauValidation = cms.EDAnalyzer('TriggerObjectValidation',
    triggerResults  = cms.InputTag("TriggerResults","HLT"),
    triggerBit      = cms.string("HLT_SingleIsoTau35_Trk15_MET25_v4"),
    triggerObjects  = cms.InputTag("hltTriggerSummaryAOD"),
    triggerObjectId = cms.int32(15)
)
