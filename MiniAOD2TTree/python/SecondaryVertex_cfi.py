#================================================================================================
# Import modules
#================================================================================================
import FWCore.ParameterSet.Config as cms


SoftBTag = cms.VPSet(
     cms.PSet(
        branchname         = cms.untracked.string("SV"),
        PrimaryVertexSrc   = cms.InputTag("offlineSlimmedPrimaryVertices"),
        SecondaryVertexSrc = cms.InputTag("slimmedSecondaryVertices"), 
        ),
     )



