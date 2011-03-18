import FWCore.ParameterSet.Config as cms

from RecoTauTag.RecoTau.PFRecoTauDiscriminationByIsolationChargedPtSum_cfi import *
from RecoTauTag.RecoTau.PFRecoTauDiscriminationByIsolation_cfi import *
from RecoTauTag.RecoTau.PFRecoTauDiscriminationAgainstElectron_cfi import *
from RecoTauTag.RecoTau.PFRecoTauQualityCuts_cfi import *

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

def addTestDiscriminatorSequence(process, tau):
    # Import the modules here in order to not to introduce compile
    # time dependency (some of these are not in vanilla 3_9_7)
    from RecoTauTag.RecoTau.PFRecoTauDiscriminationForChargedHiggs_cfi import addDiscriminator

    leadingTrackFinding = tau+"DiscriminationByLeadingTrackFinding"
    if tau == "hpsPFTau":
        leadingTrackFinding = tau+"DiscriminationByDecayModeFinding"

    lst = []

    lst.append(addDiscriminator(process, tau, "DiscriminationByIsolationChargedPtSum",
                                pfRecoTauDiscriminationByIsolationChargedSumPt.clone(
				)))
    lst[-1].Prediscriminants.leadPion.Producer = cms.InputTag(leadingTrackFinding)

    lst.append(addDiscriminator(process, tau, "DiscriminationByIsolation05",
                                pfRecoTauDiscriminationByIsolation.clone(
					qualityCuts = PFTauQualityCuts05
                                )))
    lst[-1].Prediscriminants.leadTrack.Producer = cms.InputTag(leadingTrackFinding)

    lst.append(addDiscriminator(process, tau, "DiscriminationByIsolation06",
                                pfRecoTauDiscriminationByIsolation.clone(
                                        qualityCuts = PFTauQualityCuts06
                                )))
    lst[-1].Prediscriminants.leadTrack.Producer = cms.InputTag(leadingTrackFinding)

    lst.append(addDiscriminator(process, tau, "DiscriminationByIsolation07",
                                pfRecoTauDiscriminationByIsolation.clone(
                                        qualityCuts = PFTauQualityCuts07
                                )))
    lst[-1].Prediscriminants.leadTrack.Producer = cms.InputTag(leadingTrackFinding)

    lst.append(addDiscriminator(process, tau, "DiscriminationByIsolation08",
                                pfRecoTauDiscriminationByIsolation.clone(
                                        qualityCuts = PFTauQualityCuts08
                                )))
    lst[-1].Prediscriminants.leadTrack.Producer = cms.InputTag(leadingTrackFinding)

    lst.append(addDiscriminator(process, tau, "DiscriminationByIsolation09",
                                pfRecoTauDiscriminationByIsolation.clone(
                                        qualityCuts = PFTauQualityCuts09
                                )))
    lst[-1].Prediscriminants.leadTrack.Producer = cms.InputTag(leadingTrackFinding)


    lst.append(addDiscriminator(process, tau, "DiscriminationAgainstElectronWithCrack",
                                pfRecoTauDiscriminationAgainstElectron.clone(
                                    ApplyCut_EcalCrackCut = True,
                                )))
    lst[-1].Prediscriminants.leadTrack.Producer = cms.InputTag(leadingTrackFinding)

    sequence = cms.Sequence()
    for m in lst:
        sequence *= m

    process.__setattr__(tau+"HplusTestDiscriminationSequence", sequence)

    return sequence


def addPFTauTestDiscriminationSequence(process, tauAlgos=["shrinkingConePFTau"]):
    process.PFTauTestDiscriminationSequence = cms.Sequence()
    for algo in tauAlgos:
        process.PFTauTestDiscriminationSequence *= addTestDiscriminatorSequence(process, algo)

    return process.PFTauTestDiscriminationSequence
