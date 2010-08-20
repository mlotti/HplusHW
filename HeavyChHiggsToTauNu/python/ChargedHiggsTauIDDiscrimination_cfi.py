import FWCore.ParameterSet.Config as cms
import copy

from RecoTauTag.RecoTau.PFRecoTauQualityCuts_cfi import *
hplusTrackQualityCuts = PFTauQualityCuts.clone()
hplusTrackQualityCuts.maxTrackChi2 = cms.double(10.)
hplusTrackQualityCuts.minTrackHits = cms.uint32(8)

from RecoTauTag.RecoTau.PFRecoTauDiscriminationByLeadingTrackFinding_cfi import *
def hplusTauDiscriminationByLeadingTrackFinding(tau):
    DiscriminationByLeadingTrackFinding = pfRecoTauDiscriminationByLeadingTrackFinding.clone()
    DiscriminationByLeadingTrackFinding.PFTauProducer = cms.InputTag(tau+'Producer')
    return DiscriminationByLeadingTrackFinding

from RecoTauTag.RecoTau.PFRecoTauDiscriminationByLeadingTrackPtCut_cfi import *
def hplusTauDiscriminationByLeadingTrackPtCut(tau):
    DiscriminationByLeadingTrackPtCut = pfRecoTauDiscriminationByLeadingTrackPtCut.clone()
    DiscriminationByLeadingTrackPtCut.PFTauProducer = cms.InputTag(tau+'Producer')
    DiscriminationByLeadingTrackPtCut.MinPtLeadingObject = cms.double(20.0)
    DiscriminationByLeadingTrackPtCut.qualityCuts = hplusTrackQualityCuts
    return DiscriminationByLeadingTrackPtCut

from RecoTauTag.RecoTau.PFRecoTauDiscriminationByCharge_cfi import *
def hplusTauDiscriminationByCharge(tau):
    DiscriminationByCharge = pfRecoTauDiscriminationByCharge.clone()
    DiscriminationByCharge.PFTauProducer = cms.InputTag(tau+'Producer')
    return DiscriminationByCharge

from RecoTauTag.RecoTau.PFRecoTauDiscriminationByECALIsolation_cfi import *
def hplusTauDiscriminationByECALIsolation(tau):
    DiscriminationByECALIsolation = pfRecoTauDiscriminationByECALIsolation.clone()
    DiscriminationByECALIsolation.PFTauProducer = cms.InputTag(tau+'Producer')
    DiscriminationByECALIsolation.Prediscriminants.leadTrack.Producer = cms.InputTag(tau+'DiscriminationByLeadingTrackFinding')
    return DiscriminationByECALIsolation

from RecoTauTag.RecoTau.PFRecoTauDiscriminationAgainstElectron_cfi import *
def hplusTauDiscriminationAgainstElectron(tau):
    DiscriminationAgainstElectron = pfRecoTauDiscriminationAgainstElectron.clone()
    DiscriminationAgainstElectron.PFTauProducer = cms.InputTag(tau+'Producer')
    DiscriminationAgainstElectron.Prediscriminants.leadPion.Producer = cms.InputTag(tau+'DiscriminationByLeadingTrackFinding')
    return DiscriminationAgainstElectron

from HiggsAnalysis.HeavyChHiggsToTauNu.PFRecoTauDiscriminationByTauPolarization_cfi import *
def hplusTauDiscriminationByTauPolarization(tau):
    DiscriminationByTauPolarization = pfRecoTauDiscriminationByTauPolarization.clone()
    DiscriminationByTauPolarization.PFTauProducer = cms.InputTag(tau+'Producer')
    DiscriminationByTauPolarization.Prediscriminants.leadTrack.Producer = cms.InputTag(tau+'DiscriminationByLeadingTrackFinding')
    return DiscriminationByTauPolarization

from HiggsAnalysis.HeavyChHiggsToTauNu.PFRecoTauDiscriminationByNProngs_cfi import *
def hplusTauDiscriminationByNProngs(tau):
    DiscriminationByNProngs = pfRecoTauDiscriminationByNProngs.clone()
    DiscriminationByNProngs.PFTauProducer = cms.InputTag(tau+'Producer')
    DiscriminationByNProngs.Prediscriminants.leadTrack.Producer = cms.InputTag(tau+'DiscriminationByLeadingTrackFinding')
    return DiscriminationByNProngs

from RecoTauTag.RecoTau.PFRecoTauDiscriminationByTrackIsolation_cfi import *
def hplusTauDiscrimination(tau):
    hplusTauPrediscriminants = cms.PSet(
        BooleanOperator = cms.string("and"),
        leadingTrack = cms.PSet(
            Producer = cms.InputTag(tau+'HplusTauDiscriminationByLeadingTrackPtCut'),
            cut = cms.double(0.5)
        ),
        charge = cms.PSet(
            Producer = cms.InputTag(tau+'HplusTauDiscriminationByCharge'),
            cut = cms.double(0.5)
        ),
        ecalIsolation = cms.PSet(
            Producer = cms.InputTag(tau+'HplusTauDiscriminationByECALIsolation'),
            cut = cms.double(0.5)
        ),
        electronVeto = cms.PSet(
            Producer = cms.InputTag(tau+'HplusTauDiscriminationAgainstElectron'),
            cut = cms.double(0.5)
        ),
        polarization = cms.PSet(
            Producer = cms.InputTag(tau+'HplusTauDiscriminationByTauPolarization'),
            cut = cms.double(0.5)
        ),
        prongs = cms.PSet(
            Producer = cms.InputTag(tau+'HplusTauDiscriminationByNProngs'),
            cut = cms.double(0.5)
        )
    )
    HplusTauDiscrimination = pfRecoTauDiscriminationByTrackIsolation.clone()
    HplusTauDiscrimination.PFTauProducer = cms.InputTag(tau+'Producer')
    HplusTauDiscrimination.Prediscriminants = hplusTauPrediscriminants
    HplusTauDiscrimination.qualityCuts = hplusTrackQualityCuts
    return  HplusTauDiscrimination


fixedConePFTauHplusTauDiscriminationByLeadingTrackFinding = hplusTauDiscriminationByLeadingTrackFinding("fixedConePFTau")
fixedConePFTauHplusTauDiscriminationByLeadingTrackPtCut   = hplusTauDiscriminationByLeadingTrackPtCut("fixedConePFTau")
fixedConePFTauHplusTauDiscriminationByCharge              = hplusTauDiscriminationByCharge("fixedConePFTau")
fixedConePFTauHplusTauDiscriminationByECALIsolation       = hplusTauDiscriminationByECALIsolation("fixedConePFTau")
fixedConePFTauHplusTauDiscriminationAgainstElectron       = hplusTauDiscriminationAgainstElectron("fixedConePFTau")
fixedConePFTauHplusTauDiscriminationByTauPolarization     = hplusTauDiscriminationByTauPolarization("fixedConePFTau")
fixedConePFTauHplusTauDiscriminationByNProngs             = hplusTauDiscriminationByNProngs("fixedConePFTau")
fixedConePFTauHplusTauDiscrimination                      = hplusTauDiscrimination("fixedConePFTau")

fixedConePFTauHplusTauDiscriminationSequence = cms.Sequence(
    fixedConePFTauHplusTauDiscriminationByLeadingTrackPtCut *
    fixedConePFTauHplusTauDiscriminationByCharge *
    fixedConePFTauHplusTauDiscriminationByLeadingTrackFinding *
    fixedConePFTauHplusTauDiscriminationByECALIsolation *
    fixedConePFTauHplusTauDiscriminationAgainstElectron *
    fixedConePFTauHplusTauDiscriminationByTauPolarization *
    fixedConePFTauHplusTauDiscriminationByNProngs *
    fixedConePFTauHplusTauDiscrimination
)

shrinkingConePFTauHplusTauDiscriminationByLeadingTrackFinding = hplusTauDiscriminationByLeadingTrackFinding("shrinkingConePFTau")
shrinkingConePFTauHplusTauDiscriminationByLeadingTrackPtCut   = hplusTauDiscriminationByLeadingTrackPtCut("shrinkingConePFTau")
shrinkingConePFTauHplusTauDiscriminationByCharge              = hplusTauDiscriminationByCharge("shrinkingConePFTau")
shrinkingConePFTauHplusTauDiscriminationByECALIsolation       = hplusTauDiscriminationByECALIsolation("shrinkingConePFTau")
shrinkingConePFTauHplusTauDiscriminationAgainstElectron       = hplusTauDiscriminationAgainstElectron("shrinkingConePFTau")
shrinkingConePFTauHplusTauDiscriminationByTauPolarization     = hplusTauDiscriminationByTauPolarization("shrinkingConePFTau")
shrinkingConePFTauHplusTauDiscriminationByNProngs             = hplusTauDiscriminationByNProngs("shrinkingConePFTau")
shrinkingConePFTauHplusTauDiscrimination                      = hplusTauDiscrimination("shrinkingConePFTau")

shrinkingConePFTauHplusTauDiscriminationSequence = cms.Sequence(
    shrinkingConePFTauHplusTauDiscriminationByLeadingTrackPtCut *
    shrinkingConePFTauHplusTauDiscriminationByCharge *
    shrinkingConePFTauHplusTauDiscriminationByLeadingTrackFinding *
    shrinkingConePFTauHplusTauDiscriminationByECALIsolation *
    shrinkingConePFTauHplusTauDiscriminationAgainstElectron *
    shrinkingConePFTauHplusTauDiscriminationByTauPolarization *
    shrinkingConePFTauHplusTauDiscriminationByNProngs *
    shrinkingConePFTauHplusTauDiscrimination
)

hplusTauDiscriminationSequence = cms.Sequence(
    fixedConePFTauHplusTauDiscriminationSequence *
    shrinkingConePFTauHplusTauDiscriminationSequence
)



