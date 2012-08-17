import FWCore.ParameterSet.Config as cms

import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
hPlusGlobalMuonVetoFilter = cms.EDFilter("HPlusGlobalMuonVetoFilter",
	GlobalMuonVeto = param.GlobalMuonVeto.clone(),
        vertexSrc = cms.InputTag("selectedPrimaryVertex"),
        filter = cms.bool(True),
        eventCounter = param.eventCounter.clone(),
)
