import FWCore.ParameterSet.Config as cms

import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
hPlusJetPtrSelectorFilter = cms.EDFilter("HPlusJetPtrSelectorFilter",
	jetSelection = param.jetSelection.clone(),
        tauSrc = cms.untracked.InputTag("patTausHpsPFTauTauTriggerMatched"),
        removeTau = cms.bool(True),
        histogramAmbientLevel = cms.untracked.string("Debug"),
        filter = cms.bool(True),
        throw = cms.bool(True),
        eventCounter = param.eventCounter.clone()
)
# Set Jet PU ID source
param.setJetPUIdSrc(hPlusJetPtrSelectorFilter.jetSelection,"hPlusJetPtrSelectorFilter")
