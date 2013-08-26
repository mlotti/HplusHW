import FWCore.ParameterSet.Config as cms

# https://twiki.cern.ch/twiki/bin/viewauth/CMS/Collisions2010Recipes#Good_Vertex_selection
# This is from rev. 1.4 of DPGAnalysis/Skims/python/GoodVertex_cfg.py
goodPrimaryVertices = cms.EDFilter("VertexSelector",
    filter = cms.bool(False),
    src = cms.InputTag("offlinePrimaryVertices"),
    cut = cms.string("!isFake && ndof > 4 && abs(z) < 24.0 && position.rho < 2.0")
)

goodPrimaryVertices10 = cms.EDFilter("PATPrimaryVertexCleaner",
    src = cms.InputTag("goodPrimaryVertices"),
    minMultiplicity = cms.uint32(0),
    minPtSum = cms.double(10.),
    maxTrackEta = cms.double(1e10),
    maxNormChi2 = cms.double(1e10),
    maxDeltaR = cms.double(1e10),
    maxDeltaZ = cms.double(1e10),
)
