import FWCore.ParameterSet.Config as cms
#import copy

from HiggsAnalysis.HeavyChHiggsToTauNu.PFRecoTauDiscriminationByTauPolarization_cfi import *
from HiggsAnalysis.HeavyChHiggsToTauNu.PFRecoTauDiscriminationByDeltaE_cfi import *
from HiggsAnalysis.HeavyChHiggsToTauNu.PFRecoTauDiscriminationByInvMass_cfi import *
from HiggsAnalysis.HeavyChHiggsToTauNu.PFRecoTauDiscriminationByFlightPathSignificance_cfi import *
from HiggsAnalysis.HeavyChHiggsToTauNu.PFRecoTauDiscriminationByNProngs_cfi import *

from HiggsAnalysis.HeavyChHiggsToTauNu.ChargedHiggsTauIDDiscrimination_cfi import addDiscriminator

def addDiscriminatorSequenceCont(process, tau):
    lst = []

    lst.append(addDiscriminator(process, tau, "HplusTauDiscriminationByTauPolarizationCont",
                                pfRecoTauDiscriminationByTauPolarization.clone(
					BooleanOutput = cms.bool(False)
				)))
    lst[-1].Prediscriminants.leadTrack.Producer = cms.InputTag(tau+'DiscriminationByLeadingTrackFinding')

    lst.append(addDiscriminator(process, tau, "HplusTauDiscriminationByDeltaECont",
                                pfRecoTauDiscriminationByDeltaE.clone(
					BooleanOutput = cms.bool(False)
				)))
    lst[-1].Prediscriminants.leadTrack.Producer = cms.InputTag(tau+'DiscriminationByLeadingTrackFinding')

    lst.append(addDiscriminator(process, tau, "HplusTauDiscriminationByInvMassCont",
                                pfRecoTauDiscriminationByInvMass.clone(
					BooleanOutput = cms.bool(False)
				)))
    lst[-1].Prediscriminants.leadTrack.Producer = cms.InputTag(tau+'DiscriminationByLeadingTrackFinding')

    lst.append(addDiscriminator(process, tau, "HplusTauDiscriminationByFlightPathSignificanceCont",
                                pfRecoTauDiscriminationByFlightPathSignificance.clone(
                                        BooleanOutput = cms.bool(False)
                                )))
    lst[-1].Prediscriminants.leadTrack.Producer = cms.InputTag(tau+'DiscriminationByLeadingTrackFinding')

    lst.append(addDiscriminator(process, tau, "HplusTauDiscriminationByNProngsCont",
                                pfRecoTauDiscriminationByNProngs.clone(
					BooleanOutput = cms.bool(False),
                                  	nProngs       = cms.uint32(0)
                                )))
    lst[-1].Prediscriminants.leadTrack.Producer = cms.InputTag(tau+'DiscriminationByLeadingTrackFinding')

    sequence = cms.Sequence()
    for m in lst:
        sequence *= m

    process.__setattr__(tau+"HplusDiscriminationSequenceCont", sequence)

    return sequence


def addHplusTauDiscriminationSequenceCont(process):
    process.hplusTauDiscriminationSequenceCont = cms.Sequence(
        addDiscriminatorSequenceCont(process, "fixedConePFTau") *
        addDiscriminatorSequenceCont(process, "fixedConeHighEffPFTau") *
        addDiscriminatorSequenceCont(process, "shrinkingConePFTau")
    )

    return process.hplusTauDiscriminationSequenceCont
