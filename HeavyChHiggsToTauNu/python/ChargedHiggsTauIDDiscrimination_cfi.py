import FWCore.ParameterSet.Config as cms

from RecoTauTag.RecoTau.PFRecoTauQualityCuts_cfi import *
hplusTrackQualityCuts = PFTauQualityCuts.clone()
hplusTrackQualityCuts.maxTrackChi2 = cms.double(10.)
hplusTrackQualityCuts.minTrackHits = cms.uint32(8)

#from RecoTauTag.RecoTau.TauDiscriminatorTools import noPrediscriminants

from RecoTauTag.RecoTau.PFRecoTauDiscriminationByLeadingTrackPtCut_cfi import *
hplusTauDiscriminationByLeadingTrackPtCut = pfRecoTauDiscriminationByLeadingTrackPtCut.clone()
hplusTauDiscriminationByLeadingTrackPtCut.PFTauProducer = cms.InputTag('fixedConePFTauProducer')
hplusTauDiscriminationByLeadingTrackPtCut.MinPtLeadingObject = cms.double(20.0)
hplusTauDiscriminationByLeadingTrackPtCut.qualityCuts = hplusTrackQualityCuts

hplusTauPrediscriminants = cms.PSet(
    BooleanOperator = cms.string("and"),
    leadingTrack = cms.PSet( 
        Producer = cms.InputTag('hplusTauDiscriminationByLeadingTrackPtCut'),
        cut = cms.double(0.5) 
    )
)

from RecoTauTag.RecoTau.PFRecoTauDiscriminationByTrackIsolation_cfi import *
hplusTauDiscrimination = pfRecoTauDiscriminationByTrackIsolation.clone()
hplusTauDiscrimination.PFTauProducer = cms.InputTag('fixedConePFTauProducer')
hplusTauDiscrimination.Prediscriminants = hplusTauPrediscriminants
hplusTauDiscrimination.qualityCuts = hplusTrackQualityCuts

hplusTauDiscriminationSequence = cms.Sequence(
    hplusTauDiscriminationByLeadingTrackPtCut *
    hplusTauDiscrimination
)

#hplusTauIDDiscrimination = cms.EDProducer("TCRecoTauDiscriminationAlgoComponent",
#        TauProducer = cms.InputTag('pfRecoTauProducer'),
#        Prediscriminants = noPrediscriminants
#)
#
#process.load("RecoTauTag.RecoTau.PFRecoTauDiscriminationByLeadingPionPtCut_cfi")
#from RecoTauTag.RecoTau.TauDiscriminatorTools import noPrediscriminants
#process.thisPFTauDiscriminationByLeadingPionPtCut = cms.EDFilter("PFRecoTauDiscriminationByLeadingObjectPtCut",
#
#    # Tau collection to discriminate
#    PFTauProducer = cms.InputTag('shrinkingConePFTauProducer'),
#
#    # no pre-reqs for this cut
#    Prediscriminants = noPrediscriminants,
#
#    # Allow either charged or neutral PFCandidates to meet this requirement
#    UseOnlyChargedHadrons = cms.bool(False),
#
#    MinPtLeadingObject = cms.double(3.0)
#)
