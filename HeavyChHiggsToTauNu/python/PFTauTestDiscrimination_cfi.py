import FWCore.ParameterSet.Config as cms
#import copy

from RecoTauTag.RecoTau.PFRecoTauDiscriminationByIsolationChargedPtSum_cfi import *

from RecoTauTag.RecoTau.PFRecoTauDiscriminationForChargedHiggs_cfi import addDiscriminator

def addTestDiscriminatorSequence(process, tau):
    lst = []

    lst.append(addDiscriminator(process, tau, "DiscriminationByIsolationChargedPtSum",
                                pfRecoTauDiscriminationByIsolationChargedSumPt.clone(
				)))
    lst[-1].Prediscriminants.leadPion.Producer = cms.InputTag(tau+'DiscriminationByLeadingTrackFinding')

    sequence = cms.Sequence()
    for m in lst:
        sequence *= m

    process.__setattr__(tau+"HplusTestDiscriminationSequence", sequence)

    return sequence


def addPFTauTestDiscriminationSequence(process):
    process.PFTauTestDiscriminationSequence = cms.Sequence(
#        addTestDiscriminatorSequence(process, "fixedConePFTau") *
        addTestDiscriminatorSequence(process, "shrinkingConePFTau")
    )

    return process.PFTauTestDiscriminationSequence
