import FWCore.ParameterSet.Config as cms

import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
hPlusGlobalElectronVetoFilter = cms.EDFilter("HPlusGlobalElectronVetoFilter",
	GlobalElectronVeto = param.GlobalElectronVeto,
        filter = cms.bool(True),
)
