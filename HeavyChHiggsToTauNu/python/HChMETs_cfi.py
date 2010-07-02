import FWCore.ParameterSet.Config as cms

MET = cms.EDFilter('HPlusMET',
    CollectionName = cms.InputTag("patMETs"),
    METCut = cms.double(0)
)
PFMET = cms.EDFilter('HPlusMET',
    CollectionName = cms.InputTag("patMETsPF"),
    METCut = cms.double(0)
)
TCMET = cms.EDFilter('HPlusMET',
    CollectionName = cms.InputTag("patMETsTC"),
    METCut = cms.double(0)
)

HChMETs = cms.Sequence( MET * PFMET * TCMET )
#HChMETs = cms.Sequence(PFMET)
