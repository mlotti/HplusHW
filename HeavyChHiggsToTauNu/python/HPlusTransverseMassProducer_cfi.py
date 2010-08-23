import FWCore.ParameterSet.Config as cms

transverseMass = cms.EDProducer("HPlusTransverseMassProducer",
    tauSrc = cms.InputTag("selectedPatTaus"),
    metSrc = cms.InputTag("patMETs"),
    tauMass = cms.double(1.777)
)
