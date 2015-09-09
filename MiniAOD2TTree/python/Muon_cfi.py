import FWCore.ParameterSet.Config as cms

Muons = cms.VPSet(
    cms.PSet(
        branchname = cms.untracked.string("Muons"),
        src = cms.InputTag("slimmedMuons"),
        discriminators = cms.vstring()
    )
)
