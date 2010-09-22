import FWCore.ParameterSet.Config as cms

HChTauIDSourcesCont = [("HChTauIDtauPolarizationCont", "HplusTauDiscriminationByTauPolarizationCont"),
                       ("HChTauIDDeltaECont", "HplusTauDiscriminationByDeltaECont"),
                       ("HChTauIDInvMassCont", "HplusTauDiscriminationByInvMassCont"),
                       ("HChTauIDFlightPathSignifCont", "HplusTauDiscriminationByFlightPathSignificanceCont"),
                       ("HChTauIDnProngsCont", "HplusTauDiscriminationByNProngsCont")]
