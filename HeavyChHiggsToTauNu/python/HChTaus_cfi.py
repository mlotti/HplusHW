import FWCore.ParameterSet.Config as cms

HChTauIDSources = [("HChTauIDleadingTrackPtCut", "HplusTauDiscriminationByLeadingTrackPtCut"),
                   ("HChTauIDcharge", "DiscriminationByCharge"),
                   ("HChTauIDtauPolarization", "DiscriminationByTauPolarization"),
                   ("HChTauIDDeltaE", "DiscriminationByDeltaE"),
                   ("HChTauIDInvMass", "DiscriminationByInvMass"),
                   ("HChTauIDFlightPathSignif", "DiscriminationByFlightPathSignificance"),
                   ("HChTauID1Prong", "HplusTauDiscriminationBy1Prong"),
                   ("HChTauID3Prongs", "HplusTauDiscriminationBy3Prongs"),
                   ("HChTauID3ProngCombined", "HplusTauDiscriminationBy3ProngCombined"),
                   ("HChTauID1or3Prongs", "HplusTauDiscriminationBy1or3Prongs"),
                   ("HChTauID", "HplusTauDiscrimination")]

def extendEventContent(content, process):
    content.append("keep *_fixedConePFTaus_*_"+process.name_())
    content.append("keep *_shrinkingConePFTaus_*_"+process.name_())
    return content

