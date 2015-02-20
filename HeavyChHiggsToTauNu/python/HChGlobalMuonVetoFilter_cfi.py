import FWCore.ParameterSet.Config as cms

import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
hPlusGlobalMuonVetoFilter = cms.EDFilter("HPlusGlobalMuonVetoFilter",
	MuonSelection = param.MuonSelection.clone(),
        vertexSrc = cms.InputTag("selectedPrimaryVertex"),
        histogramAmbientLevel = cms.untracked.string("Debug"),
        filter = cms.bool(True),
        eventCounter = param.eventCounter.clone(),
)
