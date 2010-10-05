import FWCore.ParameterSet.Config as cms

HChTauIDSources = [("HChTauIDleadingTrackPtCut", "DiscriminationForChargedHiggsByLeadingTrackPtCut"),
                   ("HChTauIDcharge", "DiscriminationByCharge"),
                   ("HChTauIDtauPolarization", "DiscriminationByTauPolarization"),
                   ("HChTauIDDeltaE", "DiscriminationByDeltaE"),
                   ("HChTauIDInvMass", "DiscriminationByInvMass"),
                   ("HChTauIDFlightPathSignif", "DiscriminationByFlightPathSignificance"),
                   ("HChTauID1Prong", "DiscriminationBy1Prong"),
                   ("HChTauID3Prongs", "DiscriminationBy3Prongs"),
                   ("HChTauID3ProngCombined", "DiscriminationForChargedHiggsBy3ProngCombined"),
                   ("HChTauID1or3Prongs", "DiscriminationForChargedHiggsBy1or3Prongs"),
                   ("HChTauID", "DiscriminationForChargedHiggs")]

def extendEventContent(content, process):
    content.append("keep *_fixedConePFTaus_*_"+process.name_())
    content.append("keep *_shrinkingConePFTaus_*_"+process.name_())
    return content

