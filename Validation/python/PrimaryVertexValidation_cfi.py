import FWCore.ParameterSet.Config as cms

PrimaryVertexValidation = cms.EDAnalyzer('PrimaryVertexValidation',
    BeamSpot	  = cms.InputTag("offlineBeamSpot"),
    PrimaryVertex = cms.InputTag("offlinePrimaryVertices"),
    PixelVertex   = cms.InputTag("pixelVertices")
)
