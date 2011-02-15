import FWCore.ParameterSet.Config as cms

def addCaloDiscriminatorSequenceCont(process, tau):
    # Import the modules here in order to not to introduce compile
    # time dependency (some of these are not in vanilla 3_9_7)
    import RecoTauTag.RecoTau.CaloRecoTauDiscriminationByTauPolarization_cfi as tauPolarization
    import RecoTauTag.RecoTau.CaloRecoTauDiscriminationByDeltaE_cfi as deltaE
    import RecoTauTag.RecoTau.CaloRecoTauDiscriminationByInvMass_cfi as invMass
    import RecoTauTag.RecoTau.CaloRecoTauDiscriminationByFlightPathSignificance_cfi as flightPath
    import RecoTauTag.RecoTau.CaloRecoTauDiscriminationByNProngs_cfi as nProngs

    from RecoTauTag.RecoTau.CaloRecoTauDiscriminationForChargedHiggs_cfi import addCaloDiscriminator

    lst = []

    lst.append(addCaloDiscriminator(process, tau, "DiscriminationByTauPolarizationCont",
                                tauPolarization.caloRecoTauDiscriminationByTauPolarization.clone(
					BooleanOutput = cms.bool(False)
				)))
    lst[-1].Prediscriminants.leadTrack.Producer = cms.InputTag(tau+'DiscriminationByLeadingTrackFinding')

    lst.append(addCaloDiscriminator(process, tau, "DiscriminationByDeltaECont",
                                deltaE.caloRecoTauDiscriminationByDeltaE.clone(
					BooleanOutput = cms.bool(False)
				)))
    lst[-1].Prediscriminants.leadTrack.Producer = cms.InputTag(tau+'DiscriminationByLeadingTrackFinding')

    lst.append(addCaloDiscriminator(process, tau, "DiscriminationByInvMassCont",
                                invMass.caloRecoTauDiscriminationByInvMass.clone(
					BooleanOutput = cms.bool(False)
				)))
    lst[-1].Prediscriminants.leadTrack.Producer = cms.InputTag(tau+'DiscriminationByLeadingTrackFinding')

    lst.append(addCaloDiscriminator(process, tau, "DiscriminationByFlightPathSignificanceCont",
                                flightPath.caloRecoTauDiscriminationByFlightPathSignificance.clone(
                                        BooleanOutput = cms.bool(False)
                                )))
    lst[-1].Prediscriminants.leadTrack.Producer = cms.InputTag(tau+'DiscriminationByLeadingTrackFinding')

    lst.append(addCaloDiscriminator(process, tau, "DiscriminationByNProngsCont",
                                nProngs.caloRecoTauDiscriminationByNProngs.clone(
					BooleanOutput = cms.bool(False),
                                  	nProngs       = cms.uint32(0)
                                )))
    lst[-1].Prediscriminants.leadTrack.Producer = cms.InputTag(tau+'DiscriminationByLeadingTrackFinding')

    sequence = cms.Sequence()
    for m in lst:
        sequence *= m

    process.__setattr__(tau+"HplusDiscriminationSequenceCont", sequence)

    return sequence

def addCaloTauDiscriminationSequenceForChargedHiggsCont(process):
    process.CaloTauDiscriminationSequenceForChargedHiggsCont = cms.Sequence(
        addCaloDiscriminatorSequenceCont(process, "caloRecoTau")
    )

    return process.CaloTauDiscriminationSequenceForChargedHiggsCont

