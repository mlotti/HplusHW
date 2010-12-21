import FWCore.ParameterSet.Config as cms

hplusPrescaleWeightProducer = cms.EDProducer("HPlusPrescaleWeightProducer",
    prescaleWeightVerbosityLevel = cms.uint32(1),
    prescaleWeightTriggerResults = cms.InputTag("TriggerResults", "", "HLT"),
    prescaleWeightL1GtTriggerMenuLite = cms.InputTag("l1GtTriggerMenuLite"),
    prescaleWeightHltPaths = cms.vstring(),
    alias = cms.string("prescaleWeight")
)
