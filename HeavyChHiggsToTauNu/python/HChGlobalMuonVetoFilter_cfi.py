import FWCore.ParameterSet.Config as cms

import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
hPlusGlobalMuonVetoFilter = cms.EDFilter("HPlusGlobalMuonVetoFilter",
	GlobalMuonVeto = param.GlobalMuonVeto,
        vertexSrc = cms.InputTag("goodPrimaryVertices"),
        filter = cms.bool(True),
)
