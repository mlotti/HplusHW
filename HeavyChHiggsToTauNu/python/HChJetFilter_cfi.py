import FWCore.ParameterSet.Config as cms

from HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff import jetSelection
hPlusJetPtrSelectorFilter = cms.EDFilter("HPlusJetPtrSelectorFilter",
	jetSelection = jetSelection.clone(),
        tauSrc = cms.untracked.InputTag("selectedPatTausHpsPFTauTauTriggerMatched"),
        filter = cms.bool(True),
)
