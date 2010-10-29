import FWCore.ParameterSet.Config as cms

# https://twiki.cern.ch/twiki/bin/viewauth/CMS/Collisions2010Recipes#Good_Vertex_selection
# This is from rev. 1.4 of DPGAnalysis/Skims/python/GoodVertex_cfg.py
goodPrimaryVertices = cms.EDFilter("VertexSelector",
    filter = cms.bool(False),
    src = cms.InputTag("offlinePrimaryVertices"),
    cut = cms.string("!isFake && ndof > 4 && abs(z) < 24.0 && position.rho < 2.0")
)
