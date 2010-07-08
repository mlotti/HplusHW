import FWCore.ParameterSet.Config as cms

#from HiggsAnalysis.HeavyChHiggsToTauNu.ChargedHiggsTauIDDiscrimination_cfi import fixedConeHplusTauDiscrimination

fixedConeTauIDSources = cms.PSet(
    # configure many IDs as InputTag <someName> = <someTag>
    # you can comment out those you don't want to save some
    # disk space
    leadingTrackFinding = cms.InputTag("fixedConePFTauDiscriminationByLeadingTrackFinding"),
    leadingTrackPtCut = cms.InputTag("fixedConePFTauDiscriminationByLeadingTrackPtCut"),
    leadingPionPtCut = cms.InputTag("fixedConePFTauDiscriminationByLeadingPionPtCut"),
    trackIsolation = cms.InputTag("fixedConePFTauDiscriminationByTrackIsolation"),
    trackIsolationUsingLeadingPion = cms.InputTag("fixedConePFTauDiscriminationByTrackIsolationUsingLeadingPion"),
    ecalIsolation = cms.InputTag("fixedConePFTauDiscriminationByECALIsolation"),
    ecalIsolationUsingLeadingPion = cms.InputTag("fixedConePFTauDiscriminationByECALIsolationUsingLeadingPion"),
    byIsolation = cms.InputTag("fixedConePFTauDiscriminationByIsolation"),
    byIsolationUsingLeadingPion = cms.InputTag("fixedConePFTauDiscriminationByIsolationUsingLeadingPion"),
    againstElectron = cms.InputTag("fixedConePFTauDiscriminationAgainstElectron"),
    againstMuon = cms.InputTag("fixedConePFTauDiscriminationAgainstMuon"),
    HChTauID = cms.InputTag("fixedConeHplusTauDiscrimination")
)

fixedConePFTaus = cms.EDFilter('HPlusTaus',
    CollectionName = cms.InputTag("selectedPatTaus"),
    Discriminators = cms.VInputTag(
	cms.InputTag("byIsolation"),
	cms.InputTag("HChTauID")
    )
)

HChTaus = cms.Sequence( fixedConePFTaus )
