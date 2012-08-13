import FWCore.ParameterSet.Config as cms

import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
hPlusMETPtrSelectorFilter = cms.EDFilter("HPlusMETPtrSelectorFilter",
	MET = param.MET.clone(),
        eventCounter = param.eventCounter.clone()
)
