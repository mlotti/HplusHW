import FWCore.ParameterSet.Config as cms

def tauIDSourcesCont(pset,tau):
    pset.HChTauIDtauPolarizationCont 	= cms.InputTag(tau+"HplusTauDiscriminationByTauPolarizationCont")
    pset.HChTauIDDeltaECont		= cms.InputTag(tau+"HplusTauDiscriminationByDeltaECont")
    pset.HChTauIDInvMassCont           	= cms.InputTag(tau+"HplusTauDiscriminationByInvMassCont")
    pset.HChTauIDFlightPathSignifCont  	= cms.InputTag(tau+"HplusTauDiscriminationByFlightPathSignifCont")
    pset.HChTauIDnProngsCont           	= cms.InputTag(tau+"HplusTauDiscriminationByNProngsCont")

