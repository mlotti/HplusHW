import FWCore.ParameterSet.Config as cms

skim = cms.EDFilter("SignalAnalysisSkim",
    TriggerResults = cms.InputTag("TriggerResults::HLT"),
    HLTPaths       = cms.vstring(
	"HLT_LooseIsoPFTau50_Trk30_eta2p1_MET80_v",
        "HLT_LooseIsoPFTau50_Trk30_eta2p1_MET90_v",
        "HLT_LooseIsoPFTau50_Trk30_eta2p1_MET110_v",
        "HLT_LooseIsoPFTau50_Trk30_eta2p1_MET120_v",
        "HLT_VLooseIsoPFTau120_Trk50_eta2p1_v",
        "HLT_VLooseIsoPFTau140_Trk50_eta2p1_v"
    ),
# FIXME: Temporarily CaloMET to emulate trigger MET leg 09062016/SL
    METCollection  = cms.InputTag("slimmedMETs"),

    # Taus
    TauCollection  = cms.InputTag("slimmedTaus"),
    TauPtCut       = cms.double(45.0),
    TauEtaCut      = cms.double(2.1),
    TauLdgTrkPtCut = cms.double(15.0),

    # Jets
    JetCollection  = cms.InputTag("slimmedJets"),
    JetUserFloats  = cms.vstring(
	"pileupJetId:fullDiscriminant",
    ),
    JetEtCut       = cms.double(20),
    JetEtaCut      = cms.double(5.0),
    NJets          = cms.int32(4),
)
