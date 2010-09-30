import FWCore.ParameterSet.Config as cms
#import copy

from RecoTauTag.RecoTau.PFRecoTauDiscriminationByTauPolarization_cfi import *
from RecoTauTag.RecoTau.PFRecoTauDiscriminationByDeltaE_cfi import *
from RecoTauTag.RecoTau.PFRecoTauDiscriminationByInvMass_cfi import *
from RecoTauTag.RecoTau.PFRecoTauDiscriminationByFlightPathSignificance_cfi import *
from RecoTauTag.RecoTau.PFRecoTauDiscriminationByNProngs_cfi import *

from HiggsAnalysis.HeavyChHiggsToTauNu.PFRecoTauDiscriminationForChargedHiggs_cfi import addDiscriminator

def addDiscriminatorSequenceCont(process, tau):
    lst = []

    lst.append(addDiscriminator(process, tau, "DiscriminationByTauPolarizationCont",
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
#        addDiscriminatorSequenceCont(process, "fixedConeHighEffPFTau") * # not availabel in all datasets!
        addDiscriminatorSequenceCont(process, "shrinkingConePFTau")
    )

    return process.hplusTauDiscriminationSequenceCont
