import FWCore.ParameterSet.Config as cms

genBJetFilterBase = cms.EDFilter("HPlusGenBQuarkFilter",
    genParticleSrc = cms.untracked.InputTag("genParticles"),
    bjetNumber = cms.untracked.uint32(0),
    bjetNumberCutDirection = cms.untracked.string("EQ"), # Options are EQ, NEQ, GT, LT, GEQ, LEQ
)

genBJetFilterZeroBQuarks = genBJetFilterBase.clone(
    bjetNumber = 0,
)

genBJetFilterOneBQuark = genBJetFilterBase.clone(
    bjetNumber = 1,
)

genBJetFilterTwoBQuarks = genBJetFilterBase.clone(
    bjetNumber = 2,
)

genBJetFilterThreeOrMoreBQuarks = genBJetFilterBase.clone(
    bjetNumber = 3,
    bjetNumberCutDirection = "GEQ", # Options are EQ, NEQ, GT, LT, GEQ, LEQ
)
