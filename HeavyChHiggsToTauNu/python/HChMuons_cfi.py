import FWCore.ParameterSet.Config as cms

muons = cms.EDFilter('HPlusMuons',
    CollectionName = cms.InputTag("selectedPatMuons"),
    Discriminators = cms.VInputTag(
#	cms.InputTag("")
    )
)

HChMuons = cms.Sequence( muons )

def extendEventContent(content, process):
    content.append("keep *_muons_*_"+process.name_())
    return content
