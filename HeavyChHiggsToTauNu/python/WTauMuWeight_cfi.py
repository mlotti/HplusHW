import FWCore.ParameterSet.Config as cms

wtaumuWeight = cms.EDProducer("HPlusWTauMuWeightProducer",
    muonSrc = cms.InputTag("tauEmbeddingMuons"),
    formula = cms.string("1-(%s/(x^%s))" % ("8.866647", "1.292683")),
    variationAmount = cms.double(0.012), # +- 1.2 %
    alias = cms.string("wtaumuWeight"),
    enabled = cms.bool(True),
    variationEnabled = cms.bool(False),
)
