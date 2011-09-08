import FWCore.ParameterSet.Config as cms

from HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff import tauSelection as defaultTauSelection
hPlusTauPtrSelectorFilter = cms.EDFilter("HPlusTauPtrSelectorFilter",
	tauSelection = defaultTauSelection,
        filter = cms.bool(True),
)
