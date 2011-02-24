import FWCore.ParameterSet.Config as cms

PrimaryVertexValidation = cms.EDAnalyzer('TriggerObjectValidation',
    BeamSpot	  = cms.InputTag("offlineBeamSpot"),
    PrimaryVertex = cms.InputTag("offlinePrimaryVertices")
)
