import FWCore.ParameterSet.Config as cms

from HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff import MET as defaultMETSelection
hPlusMETPtrSelectorFilter = cms.EDFilter("HPlusMETPtrSelectorFilter",
	metSelection = defaultMETSelection
)
