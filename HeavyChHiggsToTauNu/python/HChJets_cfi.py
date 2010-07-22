import FWCore.ParameterSet.Config as cms

jets  = cms.EDFilter('HPlusJets',
    CollectionName = cms.InputTag("selectedPatJets"),
    Discriminators = cms.VInputTag(
        cms.InputTag("trackCountingHighPurBJetTags"),
        cms.InputTag("trackCountingHighEffBJetTags")
    )
)

JPTJets = cms.EDFilter('HPlusJets',
    CollectionName = cms.InputTag("selectedPatJetsAK5JPT"),
    Discriminators = cms.VInputTag(
	cms.InputTag("trackCountingHighPurBJetTagsAK5JPT"),
	cms.InputTag("trackCountingHighEffBJetTagsAK5JPT")
    )
)

HChJets = cms.Sequence( jets * JPTJets )

def extendEventContent(content, process):
    name = process.name_()
    content.extend(["keep *_jets_*_"+name,
                    "keep *_JPTJets_*_"+name])
    return content
