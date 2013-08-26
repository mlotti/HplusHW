import FWCore.ParameterSet.Config as cms

genBJetFilterBase = cms.EDFilter("HPlusGenBQuarkFilter",
    genParticleSrc = cms.untracked.InputTag("genParticles"),
    bjetNumber = cms.untracked.uint32(0),
    bjetNumberCutDirection = cms.untracked.string("EQ"), # Options are EQ, NEQ, GT, LT, GEQ, LEQ
)

genBJetFilterZeroBQuarks = genBJetFilterBase.clone(
    bjetNumber = cms.untracked.uint32(0),
)

genBJetFilterOneBQuark = genBJetFilterBase.clone(
    bjetNumber = cms.untracked.uint32(1),
)

genBJetFilterTwoBQuarks = genBJetFilterBase.clone(
    bjetNumber = cms.untracked.uint32(2),
)

genBJetFilterThreeOrMoreBQuarks = cms.EDFilter("HPlusGenBQuarkFilter",
    bjetNumber = cms.untracked.uint32(3),
    bjetNumberCutDirection = cms.untracked.string("GEQ"), # Options are EQ, NEQ, GT, LT, GEQ, LEQ
)
