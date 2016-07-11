import FWCore.ParameterSet.Config as cms

import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
hPlusTauPtrSelectorFilter = cms.EDFilter("HPlusTauPtrSelectorFilter",
	tauSelection = param.tauSelection.clone(),
        histogramAmbientLevel = cms.untracked.string("Debug"),
        filter = cms.bool(True),
        eventCounter = param.eventCounter.clone(),
        vertexSrc = cms.InputTag(param.primaryVertexSelection.selectedSrc.value()),
)

hPlusTauSelectorFilter = cms.EDFilter("HPlusTauSelectorFilter",
	tauSelection = param.tauSelection.clone(),
        histogramAmbientLevel = cms.untracked.string("Debug"),
        filter = cms.bool(True),
        eventCounter = param.eventCounter.clone(),
        vertexSrc = cms.InputTag(param.primaryVertexSelection.selectedSrc.value()),
)
