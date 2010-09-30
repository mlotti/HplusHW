import FWCore.ParameterSet.Config as cms
#import copy

from RecoTauTag.RecoTau.CaloRecoTauDiscriminationByTauPolarization_cfi import *
from RecoTauTag.RecoTau.CaloRecoTauDiscriminationByDeltaE_cfi import *
from RecoTauTag.RecoTau.CaloRecoTauDiscriminationByInvMass_cfi import *
from RecoTauTag.RecoTau.CaloRecoTauDiscriminationByFlightPathSignificance_cfi import *
from RecoTauTag.RecoTau.CaloRecoTauDiscriminationByNProngs_cfi import *

from HiggsAnalysis.HeavyChHiggsToTauNu.CaloRecoTauDiscriminationForChargedHiggs_cfi import addCaloDiscriminator

def addCaloDiscriminatorSequenceCont(process, tau):
    lst = []

    lst.append(addCaloDiscriminator(process, tau, "DiscriminationByTauPolarizationCont",
                                caloRecoTauDiscriminationByTauPolarization.clone(
					BooleanOutput = cms.bool(False)
				)))
    lst[-1].Prediscriminants.leadTrack.Producer = cms.InputTag(tau+'DiscriminationByLeadingTrackFinding')

    lst.append(addCaloDiscriminator(process, tau, "HplusTauDiscriminationByDeltaECont",
                                caloRecoTauDiscriminationByDeltaE.clone(
					BooleanOutput = cms.bool(False)
				)))
    lst[-1].Prediscriminants.leadTrack.Producer = cms.InputTag(tau+'DiscriminationByLeadingTrackFinding')

    lst.append(addCaloDiscriminator(process, tau, "DiscriminationByInvMassCont",
                                caloRecoTauDiscriminationByInvMass.clone(
					BooleanOutput = cms.bool(False)
				)))
    lst[-1].Prediscriminants.leadTrack.Producer = cms.InputTag(tau+'DiscriminationByLeadingTrackFinding')

    lst.append(addCaloDiscriminator(process, tau, "DiscriminationByFlightPathSignificanceCont",
                                caloRecoTauDiscriminationByFlightPathSignificance.clone(
                                        BooleanOutput = cms.bool(False)
                                )))
    lst[-1].Prediscriminants.leadTrack.Producer = cms.InputTag(tau+'DiscriminationByLeadingTrackFinding')

    lst.append(addCaloDiscriminator(process, tau, "HplusTauDiscriminationByNProngsCont",
                                caloRecoTauDiscriminationByNProngs.clone(
					BooleanOutput = cms.bool(False),
                                  	nProngs       = cms.uint32(0)
                                )))
    lst[-1].Prediscriminants.leadTrack.Producer = cms.InputTag(tau+'DiscriminationByLeadingTrackFinding')

    sequence = cms.Sequence()
    for m in lst:
        sequence *= m

    process.__setattr__(tau+"HplusDiscriminationSequenceCont", sequence)

    return sequence


def addHplusCaloTauDiscriminationSequenceCont(process):
    process.hplusCaloTauDiscriminationSequenceCont = cms.Sequence(
        addCaloDiscriminatorSequenceCont(process, "caloRecoTau")
    )

    return process.hplusCaloTauDiscriminationSequenceCont

