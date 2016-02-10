import FWCore.ParameterSet.Config as cms

skim = cms.EDFilter("SignalAnalysisSkim",
    TriggerResults = cms.InputTag("TriggerResults::HLT"),
    HLTPaths       = cms.vstring(
	"HLT_LooseIsoPFTau50_Trk30_eta2p1_MET80_v",
        "HLT_LooseIsoPFTau50_Trk30_eta2p1_MET80_JetIdCleaned_v",
        "HLT_LooseIsoPFTau50_Trk30_eta2p1_MET120_v",
        "HLT_LooseIsoPFTau50_Trk30_eta2p1_MET120_JetIdCleaned_v",
    ),
    # Taus
    JetCollection  = cms.InputTag("slimmedTaus"),
    TauPtCut       = cms.float(50.0),
    TauEtaCut      = cms.float(2.1),
    TauLdgTrkPtCut = cms.float(15.0),

    # Jets
    JetCollection  = cms.InputTag("slimmedJets"),
    JetUserFloats  = cms.vstring(
	"pileupJetId:fullDiscriminant",
    ),
    JetEtCut       = cms.float(20),
    JetEtaCut      = cms.float(2.4),
    NJets          = cms.int32(4),
)
