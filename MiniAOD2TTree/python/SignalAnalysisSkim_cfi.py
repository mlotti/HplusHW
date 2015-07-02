import FWCore.ParameterSet.Config as cms

skim = cms.EDFilter("SignalAnalysisSkim",
    TriggerResults = cms.InputTag("TriggerResults::HLT"),
    HLTPaths       = cms.vstring(
	"HLT_LooseIsoPFTau50_Trk30_eta2p1_MET80_v",
	"HLT_LooseIsoPFTau50_Trk30_eta2p1_MET120_v",
    ),
    JetCollection  = cms.InputTag("slimmedJets"),
    JetUserFloats  = cms.vstring(
	"pileupJetId:fullDiscriminant",
    ),
    JetEtCut       = cms.double(20),
    JetEtaCut      = cms.double(2.4),
    NJets          = cms.int32(4),
)
