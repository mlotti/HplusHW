import FWCore.ParameterSet.Config as cms

skim = cms.EDFilter("TauLegSkim",
    TriggerResults = cms.InputTag("TriggerResults::HLT"),
    HLTPaths       = cms.vstring("HLT_IsoMu16_eta2p1_MET30_v",
                                 "HLT_IsoMu18_v",
                                 "HLT_IsoMu20_v",
                                 "HLT_IsoMu22_v"
    ),
    TauCollection  = cms.InputTag("slimmedTaus"),
    TauDiscriminators = cms.vstring(
	"decayModeFinding",
	"byLooseCombinedIsolationDeltaBetaCorr3Hits"
    ),
    TauPtCut       = cms.double(15),
    TauEtaCut      = cms.double(2.4),
    MuonCollection = cms.InputTag("slimmedMuons"),
    MuonDiscriminators = cms.vstring(""),
    MuonPtCut      = cms.double(15),
    MuonEtaCut     = cms.double(2.4),
    GenWeights     = cms.VPSet()
)
