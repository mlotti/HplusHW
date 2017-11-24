import FWCore.ParameterSet.Config as cms

Muons = cms.VPSet(
    cms.PSet(
        branchname = cms.untracked.string("Muons"),
        src = cms.InputTag("slimmedMuons"),
        # Marina
        rhoSource = cms.InputTag("fixedGridRhoFastjetAll"), # for MiniIsolation calculation
        
        discriminators = cms.vstring(),
        
        # Marina
        pfcands = cms.InputTag("packedPFCandidates"),
    )
)
