import FWCore.ParameterSet.Config as cms

Muons = cms.VPSet(
    cms.PSet(
        branchname = cms.untracked.string("Muons"),
        src = cms.InputTag("slimmedMuons"),
        # Marina
        rhoSource = cms.InputTag("fixedGridRhoFastjetCentralNeutral"), # For MiniIsolation
        
        discriminators = cms.vstring(),
        
        # Marina
        pfcands = cms.InputTag("packedPFCandidates"),
    )
)
