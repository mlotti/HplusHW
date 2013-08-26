import FWCore.ParameterSet.Config as cms

generatorTauValidation = cms.EDAnalyzer("TauValidation",
    src		    = cms.InputTag("genParticles"),
    tauEtCutForRtau = cms.double(50)
)
