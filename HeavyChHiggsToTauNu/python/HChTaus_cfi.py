import FWCore.ParameterSet.Config as cms

fixedConePFTaus = cms.EDFilter('HPlusTaus',
    CollectionName = cms.InputTag("selectedPatTaus"),
    Discriminators = cms.VInputTag(
	cms.InputTag("byIsolation")
    )
)

HChTaus = cms.Sequence( fixedConePFTaus )

