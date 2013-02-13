import FWCore.ParameterSet.Config as cms

import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
hPlusTauPtrSelectorFilter = cms.EDFilter("HPlusTauPtrSelectorFilter",
	tauSelection = param.tauSelection.clone(),
        filter = cms.bool(True),
        eventCounter = param.eventCounter.clone(),
        vertexSrc = cms.InputTag(param.primaryVertexSelection.src.value()),
)

hPlusTauSelectorFilter = cms.EDFilter("HPlusTauSelectorFilter",
	tauSelection = param.tauSelection.clone(),
        filter = cms.bool(True),
        eventCounter = param.eventCounter.clone(),
        vertexSrc = cms.InputTag(param.primaryVertexSelection.src.value()),
)
