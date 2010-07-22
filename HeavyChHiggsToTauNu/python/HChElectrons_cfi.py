import FWCore.ParameterSet.Config as cms

electrons = cms.EDFilter('HPlusElectrons',
    CollectionName = cms.InputTag("selectedPatElectrons"),
    Discriminators = cms.VInputTag(
#	cms.InputTag("")
    )
)

HChElectrons = cms.Sequence( electrons )

def extendEventContent(content, process):
    content.append("keep *_electrons_*_"+process.name_())
    return content
