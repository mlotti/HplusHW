import FWCore.ParameterSet.Config as cms

import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
hPlusJetPtrSelectorFilter = cms.EDFilter("HPlusJetPtrSelectorFilter",
	jetSelection = param.jetSelection.clone(),
        tauSrc = cms.untracked.InputTag("patTausHpsPFTauTauTriggerMatched"),
        filter = cms.bool(True),
        throw = cms.bool(True),
        eventCounter = param.eventCounter.clone()
)
