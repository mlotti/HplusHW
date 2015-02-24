import FWCore.ParameterSet.Config as cms

import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
hPlusMETPtrSelectorFilter = cms.EDFilter("HPlusMETPtrSelectorFilter",
	MET = param.MET.clone(),
        vertexSrc = cms.InputTag(param.primaryVertexSelection.selectedSrc.value()),
        tauIsolationDiscriminator = cms.untracked.string(param.tauSelectionBase.isolationDiscriminator.value()),
        histogramAmbientLevel = cms.untracked.string("Debug"),
        eventCounter = param.eventCounter.clone()
)

hPlusMETNoiseFilters = cms.EDFilter("HPlusMETFilters",
	histogramAmbientLevel = cms.untracked.string("Debug"),
	eventCounter = param.eventCounter.clone(),
	metFilters = param.metFilters.clone(),
        filter = cms.bool(True),
)
