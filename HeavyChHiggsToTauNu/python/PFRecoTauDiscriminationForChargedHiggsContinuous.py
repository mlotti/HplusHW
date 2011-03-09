import FWCore.ParameterSet.Config as cms

def addDiscriminatorSequenceCont(process, tau):
    # Import the modules here in order to not to introduce compile
    # time dependency (some of these are not in vanilla 3_9_7)
    import RecoTauTag.RecoTau.PFRecoTauDiscriminationByTauPolarization_cfi as tauPolarization
    import RecoTauTag.RecoTau.PFRecoTauDiscriminationByDeltaE_cfi as deltaE
    import RecoTauTag.RecoTau.PFRecoTauDiscriminationByInvMass_cfi as invMass
    import RecoTauTag.RecoTau.PFRecoTauDiscriminationByFlightPathSignificance_cfi as flightPath
    import RecoTauTag.RecoTau.PFRecoTauDiscriminationByNProngs_cfi as nProngs
    
    from RecoTauTag.RecoTau.PFRecoTauDiscriminationForChargedHiggs_cfi import addDiscriminator

    leadingTrackFinding = tau+"DiscriminationByLeadingTrackFinding"
    if tau == "hpsPFTau":
        leadingTrackFinding = tau+"DiscriminationByDecayModeFinding"

    lst = []

    lst.append(addDiscriminator(process, tau, "DiscriminationByTauPolarizationCont",
                                tauPolarization.pfRecoTauDiscriminationByTauPolarization.clone(
					BooleanOutput = cms.bool(False)
				)))
    lst[-1].Prediscriminants.leadTrack.Producer = cms.InputTag(leadingTrackFinding)

    lst.append(addDiscriminator(process, tau, "DiscriminationByDeltaECont",
                                deltaE.pfRecoTauDiscriminationByDeltaE.clone(
					BooleanOutput = cms.bool(False)
				)))
    lst[-1].Prediscriminants.leadTrack.Producer = cms.InputTag(leadingTrackFinding)

    invMassCont = invMass.pfRecoTauDiscriminationByInvMass.clone()
    del invMassCont.select
    lst.append(addDiscriminator(process, tau, "DiscriminationByInvMassCont", invMassCont))
    lst[-1].Prediscriminants.leadTrack.Producer = cms.InputTag(leadingTrackFinding)

    lst.append(addDiscriminator(process, tau, "DiscriminationByFlightPathSignificanceCont",
                                flightPath.pfRecoTauDiscriminationByFlightPathSignificance.clone(
                                        BooleanOutput = cms.bool(False)
                                )))
    lst[-1].Prediscriminants.leadTrack.Producer = cms.InputTag(leadingTrackFinding)

    lst.append(addDiscriminator(process, tau, "DiscriminationByNProngsCont",
                                nProngs.pfRecoTauDiscriminationByNProngs.clone(
					BooleanOutput = cms.bool(False),
                                  	nProngs       = cms.uint32(0)
                                )))
    lst[-1].Prediscriminants.leadTrack.Producer = cms.InputTag(leadingTrackFinding)

    sequence = cms.Sequence()
    for m in lst:
        sequence *= m

    process.__setattr__(tau+"HplusDiscriminationSequenceCont", sequence)

    return sequence


def addPFTauDiscriminationSequenceForChargedHiggsCont(process, tauAlgos=["shrinkingConePFTau"]):
    process.PFTauDiscriminationSequenceForChargedHiggsCont = cms.Sequence()
    for algo in tauAlgos:
        process.PFTauDiscriminationSequenceForChargedHiggsCont *= addDiscriminatorSequenceCont(process, algo)

    return process.PFTauDiscriminationSequenceForChargedHiggsCont
