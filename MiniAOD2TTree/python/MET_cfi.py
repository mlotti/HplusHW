import FWCore.ParameterSet.Config as cms

METs = cms.VPSet(
    cms.PSet(
        branchname = cms.untracked.string("MET_Type1"),
        src = cms.InputTag("slimmedMETs")
    ),
)
