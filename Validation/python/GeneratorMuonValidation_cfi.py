import FWCore.ParameterSet.Config as cms

generatorMuonValidation = cms.EDAnalyzer("MuonValidation",
    src		       = cms.InputTag("genParticles"),
    RecoMuons	       = cms.InputTag("selectedPatMuons"),
    MCRecoMatchingCone = cms.double(0.2)
)
