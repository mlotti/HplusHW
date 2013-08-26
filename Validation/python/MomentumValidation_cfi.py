import FWCore.ParameterSet.Config as cms

MomentumValidation = cms.EDAnalyzer('MomentumValidation',
    src = cms.InputTag("hpsPFTauProducer")
)
