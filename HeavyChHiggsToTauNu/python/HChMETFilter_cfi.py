import FWCore.ParameterSet.Config as cms

import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
hPlusMETPtrSelectorFilter = cms.EDFilter("HPlusMETPtrSelectorFilter",
	MET = param.MET.clone(),
        tauIsolationDiscriminator = cms.untracked.string(param.tauSelectionBase.isolationDiscriminator.value()),
        histogramAmbientLevel = cms.untracked.string("Debug"),
        eventCounter = param.eventCounter.clone()
)
