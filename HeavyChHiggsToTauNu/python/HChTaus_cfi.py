import FWCore.ParameterSet.Config as cms

def tauIDSources(tau):
    pset = cms.PSet(
        leadingTrackFinding            = cms.InputTag(tau+"DiscriminationByLeadingTrackFinding"),
        leadingTrackPtCut              = cms.InputTag(tau+"DiscriminationByLeadingTrackPtCut"),
        leadingPionPtCut               = cms.InputTag(tau+"DiscriminationByLeadingPionPtCut"),
        trackIsolation                 = cms.InputTag(tau+"DiscriminationByTrackIsolation"),
        trackIsolationUsingLeadingPion = cms.InputTag(tau+"DiscriminationByTrackIsolationUsingLeadingPion"),
        ecalIsolation                  = cms.InputTag(tau+"DiscriminationByECALIsolation"),
        ecalIsolationUsingLeadingPion  = cms.InputTag(tau+"DiscriminationByECALIsolationUsingLeadingPion"),
        byIsolation                    = cms.InputTag(tau+"DiscriminationByIsolation"),
        byIsolationUsingLeadingPion    = cms.InputTag(tau+"DiscriminationByIsolationUsingLeadingPion"),
        againstElectron                = cms.InputTag(tau+"DiscriminationAgainstElectron"),
        againstMuon                    = cms.InputTag(tau+"DiscriminationAgainstMuon"),

#	decayModeIndex		       = cms.InputTag(tau+"DecayModeIndexProducer"),
#	taNC                           = cms.InputTag(tau+"DiscriminationByTaNC"),
#	taNCfrHalfPercent              = cms.InputTag(tau+"DiscriminationByTaNCfrHalfPercent"),
#	taNCfrOnePercent               = cms.InputTag(tau+"DiscriminationByTaNCfrOnePercent"),
#	taNCfrQuarterPercent           = cms.InputTag(tau+"DiscriminationByTaNCfrQuarterPercent"),
#	taNCfrTenthPercent             = cms.InputTag(tau+"DiscriminationByTaNCfrTenthPercent"),

        HChTauIDleadingTrackPtCut      = cms.InputTag(tau+"HplusTauDiscriminationByLeadingTrackPtCut"),
        HChTauIDcharge                 = cms.InputTag(tau+"HplusTauDiscriminationByCharge"),
        HChTauIDtauPolarization        = cms.InputTag(tau+"HplusTauDiscriminationByTauPolarization"),
        HChTauIDnProngs                = cms.InputTag(tau+"HplusTauDiscriminationByNProngs"),
	HChTauID                       = cms.InputTag(tau+"HplusTauDiscrimination")
    )
    if(tau=="shrinkingConePFTau"):
        pset = cms.PSet(
	        leadingTrackFinding            = cms.InputTag(tau+"DiscriminationByLeadingTrackFinding"),
	       	leadingTrackPtCut              = cms.InputTag(tau+"DiscriminationByLeadingTrackPtCut"),
	        leadingPionPtCut               = cms.InputTag(tau+"DiscriminationByLeadingPionPtCut"),
	        trackIsolation                 = cms.InputTag(tau+"DiscriminationByTrackIsolation"),	
	        trackIsolationUsingLeadingPion = cms.InputTag(tau+"DiscriminationByTrackIsolationUsingLeadingPion"),
	        ecalIsolation                  = cms.InputTag(tau+"DiscriminationByECALIsolation"),
	        ecalIsolationUsingLeadingPion  = cms.InputTag(tau+"DiscriminationByECALIsolationUsingLeadingPion"),
	        byIsolation                    = cms.InputTag(tau+"DiscriminationByIsolation"),
	        byIsolationUsingLeadingPion    = cms.InputTag(tau+"DiscriminationByIsolationUsingLeadingPion"),
	        againstElectron                = cms.InputTag(tau+"DiscriminationAgainstElectron"),
	        againstMuon                    = cms.InputTag(tau+"DiscriminationAgainstMuon"),

	        HChTauIDleadingTrackPtCut      = cms.InputTag(tau+"HplusTauDiscriminationByLeadingTrackPtCut"),
	        HChTauIDcharge                 = cms.InputTag(tau+"HplusTauDiscriminationByCharge"),
	        HChTauIDtauPolarization        = cms.InputTag(tau+"HplusTauDiscriminationByTauPolarization"),
	        HChTauIDnProngs                = cms.InputTag(tau+"HplusTauDiscriminationByNProngs"),
	        HChTauID                       = cms.InputTag(tau+"HplusTauDiscrimination"),

	        decayModeIndex                 = cms.InputTag(tau+"DecayModeIndexProducer"),
	        taNC                           = cms.InputTag(tau+"DiscriminationByTaNC"),
	        taNCfrHalfPercent              = cms.InputTag(tau+"DiscriminationByTaNCfrHalfPercent"),
	        taNCfrOnePercent               = cms.InputTag(tau+"DiscriminationByTaNCfrOnePercent"),
	        taNCfrQuarterPercent           = cms.InputTag(tau+"DiscriminationByTaNCfrQuarterPercent"),
	        taNCfrTenthPercent             = cms.InputTag(tau+"DiscriminationByTaNCfrTenthPercent")
                )


    return pset


def patTaus(tau):
    theTaus = cms.EDFilter('HPlusTaus',
        CollectionName = cms.InputTag(tau),
        Discriminators = cms.VInputTag(
            cms.InputTag("againstElectron"),
            cms.InputTag("againstMuon"),
            cms.InputTag("byIsolation"),
            cms.InputTag("byIsolationUsingLeadingPion"),
            cms.InputTag("ecalIsolation"),
            cms.InputTag("ecalIsolationUsingLeadingPion"),
            cms.InputTag("leadingPionPtCut"),
            cms.InputTag("leadingTrackFinding"),
            cms.InputTag("leadingTrackPtCut"),
            cms.InputTag("trackIsolation"),
            cms.InputTag("trackIsolationUsingLeadingPion"),
            cms.InputTag("HChTauID"),
            cms.InputTag("HChTauIDleadingTrackPtCut"),
            cms.InputTag("HChTauIDcharge"),
            cms.InputTag("HChTauIDtauPolarization"),
            cms.InputTag("HChTauIDnProngs"),
#           cms.InputTag("decayModeIndex"),
#           cms.InputTag("taNC"),
#            cms.InputTag("taNCfrHalfPercent"),
#            cms.InputTag("taNCfrOnePercent"),
#            cms.InputTag("taNCfrQuarterPercent"),
#            cms.InputTag("taNCfrTenthPercent")
        )
    )
    if(tau=="shrinkingConePFTau"):
        theTaus.Discriminators.append(cms.InputTag("decayModeIndex"))
	theTaus.Discriminators.append(cms.InputTag("taNC"))
	theTaus.Discriminators.append(cms.InputTag("taNCfrHalfPercent"))
	theTaus.Discriminators.append(cms.InputTag("taNCfrOnePercent"))
	theTaus.Discriminators.append(cms.InputTag("taNCfrQuarterPercent"))
	theTaus.Discriminators.append(cms.InputTag("taNCfrTenthPercent"))

    return theTaus


fixedConeTauIDSources = tauIDSources("fixedConePFTau")
fixedConePFTaus = patTaus("fixedConePFTau")

shrinkingConeTauIDSources = tauIDSources("shrinkingConePFTau")
shrinkingConePFTaus = patTaus("shrinkingConePFTau")


HChTaus = cms.Sequence( fixedConePFTaus )
#HChTaus = cms.Sequence( shrinkingConePFTaus )
#HChTaus = cms.Sequence( 
#    fixedConePFTaus *
#    shrinkingConePFTaus 
#)

def extendEventContent(content, process):
    content.append("keep *_fixedConePFTaus_*_"+process.name_())
    content.append("keep *_shrinkingConePFTaus_*_"+process.name_())
    return content
