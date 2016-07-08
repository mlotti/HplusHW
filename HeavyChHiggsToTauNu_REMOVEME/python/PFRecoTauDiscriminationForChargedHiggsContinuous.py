import FWCore.ParameterSet.Config as cms

from PFRecoTauDiscriminationForChargedHiggs import addDiscriminator

HChTauIDSourcesCont = [("HChTauIDtauPolarizationCont", "DiscriminationByTauPolarizationCont"),
                       ("HChTauIDDeltaECont", "DiscriminationByDeltaECont"),
                       ("HChTauIDInvMassCont", "DiscriminationByInvMassCont"),
                       ("HChTauIDFlightPathSignifCont", "DiscriminationByFlightPathSignificanceCont"),
                       ("HChTauIDnProngsCont", "DiscriminationByNProngsCont")]

def addDiscriminatorSequenceCont(process, tau, postfix):
    # Import the modules here in order to not to introduce compile
    # time dependency (some of these are not in vanilla 3_9_7)
    import RecoTauTag.RecoTau.PFRecoTauDiscriminationByTauPolarization_cfi as tauPolarization
    import RecoTauTag.RecoTau.PFRecoTauDiscriminationByDeltaE_cfi as deltaE
    import RecoTauTag.RecoTau.PFRecoTauDiscriminationByInvMass_cfi as invMass
    import RecoTauTag.RecoTau.PFRecoTauDiscriminationByFlightPathSignificance_cfi as flightPath
    import RecoTauTag.RecoTau.PFRecoTauDiscriminationByNProngs_cfi as nProngs
    
    leadingTrackFinding = "hpsPFTauDiscriminationByDecayModeFinding"+postfix

    lst = []

    lst.append(addDiscriminator(process, tau, "DiscriminationByTauPolarizationCont"+postfix,
                                tauPolarization.pfRecoTauDiscriminationByTauPolarization.clone(
					BooleanOutput = cms.bool(False)
				)))
    lst[-1].Prediscriminants.leadTrack.Producer = cms.InputTag(leadingTrackFinding)

    lst.append(addDiscriminator(process, tau, "DiscriminationByDeltaECont"+postfix,
                                deltaE.pfRecoTauDiscriminationByDeltaE.clone(
					BooleanOutput = cms.bool(False)
				)))
    lst[-1].Prediscriminants.leadTrack.Producer = cms.InputTag(leadingTrackFinding)

    invMassCont = invMass.pfRecoTauDiscriminationByInvMass.clone()
    del invMassCont.select
    lst.append(addDiscriminator(process, tau, "DiscriminationByInvMassCont"+postfix, invMassCont))
    lst[-1].Prediscriminants.leadTrack.Producer = cms.InputTag(leadingTrackFinding)

    lst.append(addDiscriminator(process, tau, "DiscriminationByFlightPathSignificanceCont"+postfix,
                                flightPath.pfRecoTauDiscriminationByFlightPathSignificance.clone(
                                        BooleanOutput = cms.bool(False)
                                )))
    lst[-1].Prediscriminants.leadTrack.Producer = cms.InputTag(leadingTrackFinding)

    lst.append(addDiscriminator(process, tau, "DiscriminationByNProngsCont"+postfix,
                                nProngs.pfRecoTauDiscriminationByNProngs.clone(
					BooleanOutput = cms.bool(False),
                                  	nProngs       = cms.uint32(0)
                                )))
    lst[-1].Prediscriminants.leadTrack.Producer = cms.InputTag(leadingTrackFinding)

    sequence = cms.Sequence()
    for m in lst:
        sequence *= m

    setattr(process, tau+"HplusDiscriminationSequenceCont"+postfix, sequence)

    return sequence


def addPFTauDiscriminationSequenceForChargedHiggsCont(process, tauAlgos=["hpsPFTau"], postfix=""):
    sequence = cms.Sequence()
    setattr(process, "PFTauDiscriminationSequenceForChargedHiggsCont"+postfix, sequence)
    for algo in tauAlgos:
        sequence *= addDiscriminatorSequenceCont(process, algo, postfix)

    return sequence
