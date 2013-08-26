import FWCore.ParameterSet.Config as cms

from RecoTauTag.RecoTau.PFRecoTauDiscriminationByIsolationChargedPtSum_cfi import *
from RecoTauTag.RecoTau.PFRecoTauDiscriminationByIsolation_cfi import *
from RecoTauTag.RecoTau.PFRecoTauDiscriminationAgainstElectron_cfi import *
from RecoTauTag.RecoTau.PFRecoTauQualityCuts_cfi import *

TestTauIDSources = [("byIsolationChargedPtSum", "DiscriminationByIsolationChargedPtSum"),
                    ("byIsolation05", "DiscriminationByIsolation05"),
                    ("byIsolation06", "DiscriminationByIsolation06"),
                    ("byIsolation07", "DiscriminationByIsolation07"),
                    ("byIsolation08", "DiscriminationByIsolation08"),
                    ("byIsolation09", "DiscriminationByIsolation09"),
                    ("againstElectronWithCrack", "DiscriminationAgainstElectronWithCrack")
]

PFTauQualityCuts05 = PFTauQualityCuts.clone()
PFTauQualityCuts05.isolationQualityCuts.minTrackPt = cms.double(0.5)

PFTauQualityCuts06 = PFTauQualityCuts.clone()
PFTauQualityCuts06.isolationQualityCuts.minTrackPt = cms.double(0.6)

PFTauQualityCuts07 = PFTauQualityCuts.clone()
PFTauQualityCuts07.isolationQualityCuts.minTrackPt = cms.double(0.7)

PFTauQualityCuts08 = PFTauQualityCuts.clone()
PFTauQualityCuts08.isolationQualityCuts.minTrackPt = cms.double(0.8)

PFTauQualityCuts09 = PFTauQualityCuts.clone()
PFTauQualityCuts09.isolationQualityCuts.minTrackPt = cms.double(0.9)

from PFRecoTauDiscriminationForChargedHiggs import addDiscriminator
def addTestDiscriminatorSequence(process, tau, postfix):
    leadingTrackFinding = "hpsPFTauDiscriminationByDecayModeFinding"+postfix

    lst = []

    lst.append(addDiscriminator(process, tau, "DiscriminationByIsolationChargedPtSum"+postfix,
                                pfRecoTauDiscriminationByIsolationChargedSumPt.clone(
				)))
    lst[-1].Prediscriminants.leadPion.Producer = cms.InputTag(leadingTrackFinding)

    lst.append(addDiscriminator(process, tau, "DiscriminationByIsolation05"+postfix,
                                pfRecoTauDiscriminationByIsolation.clone(
					qualityCuts = PFTauQualityCuts05
                                )))
    lst[-1].Prediscriminants.leadTrack.Producer = cms.InputTag(leadingTrackFinding)

    lst.append(addDiscriminator(process, tau, "DiscriminationByIsolation06"+postfix,
                                pfRecoTauDiscriminationByIsolation.clone(
                                        qualityCuts = PFTauQualityCuts06
                                )))
    lst[-1].Prediscriminants.leadTrack.Producer = cms.InputTag(leadingTrackFinding)

    lst.append(addDiscriminator(process, tau, "DiscriminationByIsolation07"+postfix,
                                pfRecoTauDiscriminationByIsolation.clone(
                                        qualityCuts = PFTauQualityCuts07
                                )))
    lst[-1].Prediscriminants.leadTrack.Producer = cms.InputTag(leadingTrackFinding)

    lst.append(addDiscriminator(process, tau, "DiscriminationByIsolation08"+postfix,
                                pfRecoTauDiscriminationByIsolation.clone(
                                        qualityCuts = PFTauQualityCuts08
                                )))
    lst[-1].Prediscriminants.leadTrack.Producer = cms.InputTag(leadingTrackFinding)

    lst.append(addDiscriminator(process, tau, "DiscriminationByIsolation09"+postfix,
                                pfRecoTauDiscriminationByIsolation.clone(
                                        qualityCuts = PFTauQualityCuts09
                                )))
    lst[-1].Prediscriminants.leadTrack.Producer = cms.InputTag(leadingTrackFinding)


    lst.append(addDiscriminator(process, tau, "DiscriminationAgainstElectronWithCrack"+postfix,
                                pfRecoTauDiscriminationAgainstElectron.clone(
                                    ApplyCut_EcalCrackCut = True,
                                )))
    lst[-1].Prediscriminants.leadTrack.Producer = cms.InputTag(leadingTrackFinding)

    sequence = cms.Sequence()
    for m in lst:
        sequence *= m

    setattr(process, tau+"HplusTestDiscriminationSequence"+postfix, sequence)

    return sequence


def addPFTauTestDiscriminationSequence(process, tauAlgos=["hpsPFTau"], postfix=""):
    sequence = cms.Sequence()
    setattr(process, "PFTauTestDiscriminationSequence"+postfix, sequence)
    for algo in tauAlgos:
        sequence *= addTestDiscriminatorSequence(process, algo, postfix)

    return sequence
