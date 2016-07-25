import FWCore.ParameterSet.Config as cms

metResolutionAnalysis = cms.EDAnalyzer("METResolutionAnalysis",
    recoMETSrc = cms.InputTag("patMETs"),
    mcMETSrc   = cms.InputTag("genMetTrue")
)
