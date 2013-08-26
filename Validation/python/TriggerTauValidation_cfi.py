import FWCore.ParameterSet.Config as cms

TriggerTauValidation = cms.EDAnalyzer('TriggerObjectValidation',
    triggerResults  = cms.InputTag("TriggerResults","","HLT"),
#    triggerResults  = cms.InputTag("TriggerResults","","REDIGI39X"),
    triggerBit      = cms.string("HLT_SingleIsoTau20_Trk15_MET25_v4"),
    triggerObjects  = cms.InputTag("hltTriggerSummaryAOD"),
    triggerObjectId = cms.int32(15),
    hltPathFilter   = cms.InputTag("hltFilterL3TrackIsolationSingleIsoTau20Trk15MET25","","REDIGI39X")
)
