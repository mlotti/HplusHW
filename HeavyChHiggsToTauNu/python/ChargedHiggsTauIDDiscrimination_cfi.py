import FWCore.ParameterSet.Config as cms
import copy

from RecoTauTag.RecoTau.PFRecoTauQualityCuts_cfi import *
hplusTrackQualityCuts = PFTauQualityCuts.clone()
hplusTrackQualityCuts.maxTrackChi2 = cms.double(10.)
hplusTrackQualityCuts.minTrackHits = cms.uint32(8)

from RecoTauTag.RecoTau.PFRecoTauDiscriminationByLeadingTrackFinding_cfi import *
#pfRecoTauDiscriminationByLeadingTrackFinding.PFTauProducer = cms.InputTag('fixedConePFTauProducer')
#fixedConePFTauDiscriminationByLeadingTrackFinding = copy.deepcopy(pfRecoTauDiscriminationByLeadingTrackFinding)
fixedConePFTauHplusTauDiscriminationByLeadingTrackFinding = pfRecoTauDiscriminationByLeadingTrackFinding.clone()
fixedConePFTauHplusTauDiscriminationByLeadingTrackFinding.PFTauProducer = cms.InputTag('fixedConePFTauProducer')


from RecoTauTag.RecoTau.PFRecoTauDiscriminationByLeadingTrackPtCut_cfi import *
fixedConePFTauHplusTauDiscriminationByLeadingTrackPtCut = pfRecoTauDiscriminationByLeadingTrackPtCut.clone()
fixedConePFTauHplusTauDiscriminationByLeadingTrackPtCut.PFTauProducer = cms.InputTag('fixedConePFTauProducer')
fixedConePFTauHplusTauDiscriminationByLeadingTrackPtCut.MinPtLeadingObject = cms.double(20.0)
fixedConePFTauHplusTauDiscriminationByLeadingTrackPtCut.qualityCuts = hplusTrackQualityCuts

from RecoTauTag.RecoTau.PFRecoTauDiscriminationByCharge_cfi import *
fixedConePFTauHplusTauDiscriminationByCharge = pfRecoTauDiscriminationByCharge.clone()
fixedConePFTauHplusTauDiscriminationByCharge.PFTauProducer = cms.InputTag('fixedConePFTauProducer')

from RecoTauTag.RecoTau.PFRecoTauDiscriminationByECALIsolation_cfi import *
fixedConePFTauHplusTauDiscriminationByECALIsolation = pfRecoTauDiscriminationByECALIsolation.clone()
fixedConePFTauHplusTauDiscriminationByECALIsolation.PFTauProducer = cms.InputTag('fixedConePFTauProducer')
fixedConePFTauHplusTauDiscriminationByECALIsolation.Prediscriminants.leadTrack.Producer = cms.InputTag('fixedConePFTauDiscriminationByLeadingTrackFinding')

from RecoTauTag.RecoTau.PFRecoTauDiscriminationAgainstElectron_cfi import *
#fixedConePFTauDiscriminationAgainstElectron = copy.deepcopy(pfRecoTauDiscriminationAgainstElectron)
fixedConePFTauHplusTauDiscriminationAgainstElectron = pfRecoTauDiscriminationAgainstElectron.clone()
fixedConePFTauHplusTauDiscriminationAgainstElectron.PFTauProducer = cms.InputTag('fixedConePFTauProducer')
fixedConePFTauHplusTauDiscriminationAgainstElectron.Prediscriminants.leadPion.Producer = cms.InputTag('fixedConePFTauDiscriminationByLeadingTrackFinding')

from HiggsAnalysis.HeavyChHiggsToTauNu.PFRecoTauDiscriminationByTauPolarization_cfi import *
fixedConePFTauHplusTauDiscriminationByTauPolarization = pfRecoTauDiscriminationByTauPolarization.clone()
fixedConePFTauHplusTauDiscriminationByTauPolarization.PFTauProducer = cms.InputTag('fixedConePFTauProducer')
fixedConePFTauHplusTauDiscriminationByTauPolarization.Prediscriminants.leadTrack.Producer = cms.InputTag('fixedConePFTauDiscriminationByLeadingTrackFinding')

from HiggsAnalysis.HeavyChHiggsToTauNu.PFRecoTauDiscriminationByNProngs_cfi import *
fixedConePFTauHplusTauDiscriminationByNProngs = pfRecoTauDiscriminationByNProngs.clone()
fixedConePFTauHplusTauDiscriminationByNProngs.PFTauProducer = cms.InputTag('fixedConePFTauProducer')
fixedConePFTauHplusTauDiscriminationByNProngs.Prediscriminants.leadTrack.Producer = cms.InputTag('fixedConePFTauDiscriminationByLeadingTrackFinding')

hplusTauPrediscriminants = cms.PSet(
    BooleanOperator = cms.string("and"),
    leadingTrack = cms.PSet( 
        Producer = cms.InputTag('fixedConePFTauHplusTauDiscriminationByLeadingTrackPtCut'),
        cut = cms.double(0.5) 
    ),
    charge = cms.PSet(
        Producer = cms.InputTag('fixedConePFTauHplusTauDiscriminationByCharge'),
        cut = cms.double(0.5)
    ),
    ecalIsolation = cms.PSet(
        Producer = cms.InputTag('fixedConePFTauHplusTauDiscriminationByECALIsolation'),
        cut = cms.double(0.5)
    ),
    electronVeto = cms.PSet(
        Producer = cms.InputTag('fixedConePFTauHplusTauDiscriminationAgainstElectron'),
        cut = cms.double(0.5)
    ),
    polarization = cms.PSet(
        Producer = cms.InputTag('fixedConePFTauHplusTauDiscriminationByTauPolarization'),
        cut = cms.double(0.5)
    ),
    prongs = cms.PSet(
        Producer = cms.InputTag('fixedConePFTauHplusTauDiscriminationByNProngs'),
        cut = cms.double(0.5)
    )
)

from RecoTauTag.RecoTau.PFRecoTauDiscriminationByTrackIsolation_cfi import *
fixedConePFTauHplusTauDiscrimination = pfRecoTauDiscriminationByTrackIsolation.clone()
fixedConePFTauHplusTauDiscrimination.PFTauProducer = cms.InputTag('fixedConePFTauProducer')
fixedConePFTauHplusTauDiscrimination.Prediscriminants = hplusTauPrediscriminants
fixedConePFTauHplusTauDiscrimination.qualityCuts = hplusTrackQualityCuts


hplusTauDiscriminationSequence = cms.Sequence(
#fixedConePFTauHplusTauDiscriminationSequence = cms.Sequence(
    fixedConePFTauHplusTauDiscriminationByLeadingTrackPtCut *
    fixedConePFTauHplusTauDiscriminationByCharge *
    fixedConePFTauHplusTauDiscriminationByLeadingTrackFinding *
    fixedConePFTauHplusTauDiscriminationByECALIsolation *
    fixedConePFTauHplusTauDiscriminationAgainstElectron *
    fixedConePFTauHplusTauDiscriminationByTauPolarization *
    fixedConePFTauHplusTauDiscriminationByNProngs *
    fixedConePFTauHplusTauDiscrimination
)


