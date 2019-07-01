import FWCore.ParameterSet.Config as cms

skim = cms.EDFilter("Hplus2hwAnalysisSkim",
    TriggerResults = cms.InputTag("TriggerResults::HLT"),
    HLTPaths	   = cms.vstring(
        "HLT_IsoMu24_v",
	"HLT_IsoTkMu24_v",
	"HLT_Ele27_eta2p1_WPTight_Gsf_v"
    ),

    src   = cms.InputTag("externalLHEProducer"),

    JetCollection	= cms.InputTag("slimmedJets"),

    METCollection	= cms.InputTag("slimmedMETs"),

    MuonCollection	= cms.InputTag("slimmedMuons"),
    NMuons 		= cms.int32(1),

    ElectronCollection	= cms.InputTag("slimmedElectrons"),

    TauCollection	= cms.InputTag("slimmedTaus"),
    NTaus		= cms.int32(2),
    )
