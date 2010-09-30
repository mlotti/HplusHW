import FWCore.ParameterSet.Config as cms

HChTauIDSourcesCont = [("HChTauIDtauPolarizationCont", "DiscriminationByTauPolarizationCont"),
                       ("HChTauIDDeltaECont", "HplusTauDiscriminationByDeltaECont"),
                       ("HChTauIDInvMassCont", "DiscriminationByInvMassCont"),
                       ("HChTauIDFlightPathSignifCont", "DiscriminationByFlightPathSignificanceCont"),
                       ("HChTauIDnProngsCont", "HplusTauDiscriminationByNProngsCont")]
