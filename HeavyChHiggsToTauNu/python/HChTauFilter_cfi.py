import FWCore.ParameterSet.Config as cms

import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
hPlusTauPtrSelectorFilter = cms.EDFilter("HPlusTauPtrSelectorFilter",
	tauSelection = param.tauSelection.clone(),
        filter = cms.bool(True),
        eventCounter = param.eventCounter.clone()
)
