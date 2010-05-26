import FWCore.ParameterSet.Config as cms

from RecoTauTag.RecoTau.PFRecoTauQualityCuts_cfi import *
hplusTrackQualityCuts = PFTauQualityCuts.clone()
hplusTrackQualityCuts.maxTrackChi2 = cms.double(10.)
hplusTrackQualityCuts.minTrackHits = cms.uint32(8)

from RecoTauTag.RecoTau.PFRecoTauDiscriminationByLeadingTrackFinding_cfi import *
pfRecoTauDiscriminationByLeadingTrackFinding.PFTauProducer = cms.InputTag('fixedConePFTauProducer')

from RecoTauTag.RecoTau.PFRecoTauDiscriminationByLeadingTrackPtCut_cfi import *
hplusTauDiscriminationByLeadingTrackPtCut = pfRecoTauDiscriminationByLeadingTrackPtCut.clone()
hplusTauDiscriminationByLeadingTrackPtCut.PFTauProducer = cms.InputTag('fixedConePFTauProducer')
hplusTauDiscriminationByLeadingTrackPtCut.MinPtLeadingObject = cms.double(20.0)
hplusTauDiscriminationByLeadingTrackPtCut.qualityCuts = hplusTrackQualityCuts

from RecoTauTag.RecoTau.PFRecoTauDiscriminationByCharge_cfi import *
pfRecoTauDiscriminationByCharge.PFTauProducer = cms.InputTag('fixedConePFTauProducer')

from RecoTauTag.RecoTau.PFRecoTauDiscriminationByECALIsolation_cfi import *
hplusTauDiscriminationByECALIsolation = pfRecoTauDiscriminationByECALIsolation.clone()
hplusTauDiscriminationByECALIsolation.PFTauProducer = cms.InputTag('fixedConePFTauProducer')

from RecoTauTag.RecoTau.PFRecoTauDiscriminationAgainstElectron_cfi import *
pfRecoTauDiscriminationAgainstElectron.PFTauProducer = cms.InputTag('fixedConePFTauProducer')

hplusTauPrediscriminants = cms.PSet(
    BooleanOperator = cms.string("and"),
    leadingTrack = cms.PSet( 
        Producer = cms.InputTag('hplusTauDiscriminationByLeadingTrackPtCut'),
        cut = cms.double(0.5) 
    ),
    charge = cms.PSet(
        Producer = cms.InputTag('pfRecoTauDiscriminationByCharge'),
        cut = cms.double(0.5)
    ),
    ecalIsolation = cms.PSet(
        Producer = cms.InputTag('hplusTauDiscriminationByECALIsolation'),
        cut = cms.double(0.5)
    ),
    electronVeto = cms.PSet(
        Producer = cms.InputTag('pfRecoTauDiscriminationAgainstElectron'),
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
    pfRecoTauDiscriminationByCharge *
    pfRecoTauDiscriminationByLeadingTrackFinding * # needed by ECALIsolation and AgainstElectron
    hplusTauDiscriminationByECALIsolation *
    pfRecoTauDiscriminationAgainstElectron *
    hplusTauDiscrimination
)

