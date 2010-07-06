import FWCore.ParameterSet.Config as cms

JPTJets = cms.EDFilter('HPlusJets',
    CollectionName = cms.InputTag("selectedPatJetsAK5JPT"),
    Discriminators = cms.VInputTag(
	cms.InputTag("trackCountingHighPurBJetTagsAK5JPT"),
	cms.InputTag("trackCountingHighEffBJetTagsAK5JPT")
    )
)

HChJets = cms.Sequence( JPTJets )

