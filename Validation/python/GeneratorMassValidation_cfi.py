import FWCore.ParameterSet.Config as cms

generatorMassValidation = cms.EDAnalyzer('GeneratorMassValidation',
    src       = cms.InputTag("genParticles"),
    particles = cms.vint32(23,24)
)
