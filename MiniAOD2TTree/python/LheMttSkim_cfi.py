import FWCore.ParameterSet.Config as cms

lheMttskim = cms.EDFilter("LheMttSkim",
    src   = cms.InputTag("externalLHEProducer"),
    Mttmin = cms.double(0.),
    Mttmax = cms.double(700.)
)
