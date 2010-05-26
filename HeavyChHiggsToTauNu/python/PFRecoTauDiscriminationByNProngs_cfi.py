import FWCore.ParameterSet.Config as cms

from RecoTauTag.RecoTau.PFRecoTauQualityCuts_cfi import *
from RecoTauTag.RecoTau.TauDiscriminatorTools import requireLeadTrack

pfRecoTauDiscriminationByNProngs = cms.EDProducer("PFRecoTauDiscriminationByNProngs",
    PFTauProducer       = cms.InputTag('pfRecoTauProducer'), #tau collection to discriminate

    Prediscriminants    = requireLeadTrack,

    nProngs             = cms.uint32(0), # number of prongs required: 0=1||3, 1, 3

    threeProngSelection = cms.bool(True),    # selection using variables below activated
                                             # for 3-prong taus only, 1-prongs not affected. 
    deltaEmin		= cms.double(-0.15), # used only if threeProngSelection == true
    deltaEmax           = cms.double(1.0),   # used only if threeProngSelection == true
    invMassMin		= cms.double(0.0),   # used only if threeProngSelection == true
    invMassMax          = cms.double(1.4),   # used only if threeProngSelection == true
    flightPathSig	= cms.double(1.5),   # used only if threeProngSelection == true

    qualityCuts         = PFTauQualityCuts,# set the standard quality cuts
    PVProducer          = cms.InputTag('offlinePrimaryVertices'), # needed for quality cuts
)
