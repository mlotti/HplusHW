import FWCore.ParameterSet.Config as cms

skim = cms.EDFilter("Hplus2tbAnalysisSkim",
    TriggerResults = cms.InputTag("TriggerResults::HLT"),
    HLTPaths       = cms.vstring(
        # #"HLT_QuadPFJet_DoubleBTagCSV_VBF_Mqq200_v",
        # "HLT_QuadPFJet_BTagCSV_p016_p11_VBF_Mqq200_v",
        # "HLT_QuadPFJet_BTagCSV_p016_VBF_Mqq460_v",
        # "HLT_QuadPFJet_BTagCSV_p016_p11_VBF_Mqq240_v",
        # "HLT_QuadPFJet_BTagCSV_p016_VBF_Mqq500_v",
        # "HLT_QuadPFJet_VBF_v",
    ),

    # Jets
    JetCollection  = cms.InputTag("slimmedJets"),
    JetUserFloats  = cms.vstring(
	"pileupJetId:fullDiscriminant",
    ),
    JetEtCut       = cms.double(20),
    JetEtaCut      = cms.double(2.4),
    NJets          = cms.int32(4),
)
