import FWCore.ParameterSet.Config as cms

skim = cms.EDFilter("Hplus2hwAnalysisSkim",
#    TriggerResults = cms.InputTag("TriggerResults::HLT"),
#    HLTPaths	   = cms.vstring(
#        "HLT_IsoMu22_eta2p1_v"
#    ),

    JetCollection	= cms.InputTag("slimmedJets"),

    METCollection	= cms.InputTag("slimmedMETs"),

    MuonCollection	= cms.InputTag("slimmedMuons"),
    NMuons 		= cms.int32(1),

    TauCollection	= cms.InputTag("slimmedTaus"),
    NTaus		= cms.int32(2),
    )
