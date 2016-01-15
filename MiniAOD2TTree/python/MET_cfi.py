import FWCore.ParameterSet.Config as cms

METs = cms.VPSet(
    cms.PSet(
        branchname = cms.untracked.string("MET_Type1"),
        src = cms.InputTag("slimmedMETs")
    ),
#    cms.PSet(
#        branchname = cms.untracked.string("MET_Type1_NoHF"),
#        src = cms.InputTag("slimmedMETsNoHF")
#    ),
    cms.PSet(
        branchname = cms.untracked.string("MET_Puppi"),
        src = cms.InputTag("slimmedMETsPuppi")
    ),
)
