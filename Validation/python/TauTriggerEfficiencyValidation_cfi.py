import FWCore.ParameterSet.Config as cms

TauTriggerEfficiencyValidation = cms.EDAnalyzer('TauTriggerEfficiencyValidation',
    triggerResults    = cms.InputTag("TriggerResults","","HLT"),
    triggerBit        = cms.string("HLT_SingleIsoTau20_Trk15_MET25_v4"),
    triggerObjects    = cms.InputTag("hltTriggerSummaryAOD"),
    triggerObjectId   = cms.int32(15),
    hltPathFilter     = cms.InputTag("hltFilterL3TrackIsolationSingleIsoTau20Trk15MET25","","REDIGI311X"),
    referenceTau      = cms.InputTag("shrinkingConePFTauProducer"),
    referenceTauDiscr = cms.InputTag("shrinkingConePFTauDiscriminationByIsolation"),
    MatchingCone      = cms.double(0.3),
    PrimaryVertex     = cms.InputTag("offlinePrimaryVertices")
)
