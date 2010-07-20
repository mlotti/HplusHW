import FWCore.ParameterSet.Config as cms

#from PhysicsTools.PatAlgos.triggerLayer1.triggerProducer_cff import *

tauTriggerMatchHLTSingleLooseIsoTau20 = cms.EDFilter( "PATTriggerMatcherDRDPtLessByR",
    src     = cms.InputTag( "cleanPatTaus" ),
    matched = cms.InputTag( "patTrigger" ),
    andOr          = cms.bool( False ),
    filterIdsEnum  = cms.vstring( '*' ),
    filterIds      = cms.vint32( 0 ),
    filterLabels   = cms.vstring( '*' ),
    pathNames      = cms.vstring( 'HLT_SingleLooseIsoTau20' ),
    collectionTags = cms.vstring( '*' ),
    maxDPtRel = cms.double( 0.5 ),
    maxDeltaR = cms.double( 0.5 ),
    resolveAmbiguities    = cms.bool( True ),
    resolveByMatchQuality = cms.bool( False )
)


patTriggerMatcherTau = cms.Sequence(
    tauTriggerMatchHLTSingleLooseIsoTau20
)
