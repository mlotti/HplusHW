import FWCore.ParameterSet.Config as cms
import copy

from HiggsAnalysis.HeavyChHiggsToTauNu.PFRecoTauDiscriminationByTauPolarization_cfi import *
def hplusTauDiscriminationByTauPolarizationCont(tau):
    DiscriminationByTauPolarization = pfRecoTauDiscriminationByTauPolarization.clone()
    DiscriminationByTauPolarization.PFTauProducer = cms.InputTag(tau+'Producer')
    DiscriminationByTauPolarization.BooleanOutput = cms.bool(False)
    DiscriminationByTauPolarization.Prediscriminants.leadTrack.Producer = cms.InputTag(tau+'DiscriminationByLeadingTrackFinding')
    return DiscriminationByTauPolarization

from HiggsAnalysis.HeavyChHiggsToTauNu.PFRecoTauDiscriminationByDeltaE_cfi import *
def hplusTauDiscriminationByDeltaECont(tau):
    DiscriminationByDeltaE = pfRecoTauDiscriminationByDeltaE.clone()
    DiscriminationByDeltaE.PFTauProducer = cms.InputTag(tau+'Producer')
    DiscriminationByDeltaE.BooleanOutput = cms.bool(False)
    DiscriminationByDeltaE.Prediscriminants.leadTrack.Producer = cms.InputTag(tau+'DiscriminationByLeadingTrackFinding')
    return DiscriminationByDeltaE

from HiggsAnalysis.HeavyChHiggsToTauNu.PFRecoTauDiscriminationByInvMass_cfi import *
def hplusTauDiscriminationByInvMassCont(tau):
    DiscriminationByInvMass = pfRecoTauDiscriminationByInvMass.clone()
    DiscriminationByInvMass.PFTauProducer = cms.InputTag(tau+'Producer')
    DiscriminationByInvMass.BooleanOutput = cms.bool(False)
    DiscriminationByInvMass.Prediscriminants.leadTrack.Producer = cms.InputTag(tau+'DiscriminationByLeadingTrackFinding')
    return DiscriminationByInvMass

from HiggsAnalysis.HeavyChHiggsToTauNu.PFRecoTauDiscriminationByFlightPathSignificance_cfi import *
def hplusTauDiscriminationByFlightPathSignificanceCont(tau):
    DiscriminationByFlightPathSignificance = pfRecoTauDiscriminationByFlightPathSignificance.clone()
    DiscriminationByFlightPathSignificance.PFTauProducer = cms.InputTag(tau+'Producer')
    DiscriminationByFlightPathSignificance.BooleanOutput = cms.bool(False)
    DiscriminationByFlightPathSignificance.Prediscriminants.leadTrack.Producer = cms.InputTag(tau+'DiscriminationByLeadingTrackFinding')
    return DiscriminationByFlightPathSignificance

from HiggsAnalysis.HeavyChHiggsToTauNu.PFRecoTauDiscriminationByNProngs_cfi import *
def hplusTauDiscriminationByNProngsCont(tau):
    DiscriminationByNProngs = pfRecoTauDiscriminationByNProngs.clone()
    DiscriminationByNProngs.PFTauProducer = cms.InputTag(tau+'Producer')
    DiscriminationByNProngs.Prediscriminants.leadTrack.Producer = cms.InputTag(tau+'DiscriminationByLeadingTrackFinding')
    DiscriminationByNProngs.BooleanOutput = cms.bool(False)
    DiscriminationByNProngs.nProngs = cms.uint32(0)
    return DiscriminationByNProngs

fixedConePFTauHplusTauDiscriminationByTauPolarizationCont     = hplusTauDiscriminationByTauPolarizationCont("fixedConePFTau")
fixedConePFTauHplusTauDiscriminationByDeltaECont	      = hplusTauDiscriminationByDeltaECont("fixedConePFTau")
fixedConePFTauHplusTauDiscriminationByInvMassCont	      = hplusTauDiscriminationByInvMassCont("fixedConePFTau")
fixedConePFTauHplusTauDiscriminationByFlightPathSignifCont    = hplusTauDiscriminationByFlightPathSignificanceCont("fixedConePFTau")
fixedConePFTauHplusTauDiscriminationByNProngsCont             = hplusTauDiscriminationByNProngsCont("fixedConePFTau")

fixedConePFTauHplusTauDiscriminationSequenceCont = cms.Sequence(
    fixedConePFTauHplusTauDiscriminationByTauPolarizationCont *
    fixedConePFTauHplusTauDiscriminationByDeltaECont *
    fixedConePFTauHplusTauDiscriminationByInvMassCont *
    fixedConePFTauHplusTauDiscriminationByFlightPathSignifCont *
    fixedConePFTauHplusTauDiscriminationByNProngsCont
)

hplusTauContinuousDiscriminationSequence = cms.Sequence(
    fixedConePFTauHplusTauDiscriminationSequenceCont 
)

