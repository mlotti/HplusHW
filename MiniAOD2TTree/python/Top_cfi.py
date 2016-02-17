import FWCore.ParameterSet.Config as cms

Top = cms.VPSet(
    cms.PSet(
        branchname = cms.untracked.string("Top"),
        src = cms.InputTag("caTopTagInfosPAT"),
    )
)
