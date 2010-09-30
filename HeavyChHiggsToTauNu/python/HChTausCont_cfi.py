import FWCore.ParameterSet.Config as cms

HChTauIDSourcesCont = [("HChTauIDtauPolarizationCont", "DiscriminationByTauPolarizationCont"),
                       ("HChTauIDDeltaECont", "HplusTauDiscriminationByDeltaECont"),
                       ("HChTauIDInvMassCont", "HplusTauDiscriminationByInvMassCont"),
                       ("HChTauIDFlightPathSignifCont", "HplusTauDiscriminationByFlightPathSignificanceCont"),
                       ("HChTauIDnProngsCont", "HplusTauDiscriminationByNProngsCont")]
