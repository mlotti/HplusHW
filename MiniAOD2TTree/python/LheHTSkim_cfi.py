import FWCore.ParameterSet.Config as cms

lheHTskim = cms.EDFilter("LheHTSkim",
    src   = cms.InputTag("externalLHEProducer"),
    HTmin = cms.double(0.),
    HTmax = cms.double(70.)
)
