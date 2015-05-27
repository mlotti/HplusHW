import FWCore.ParameterSet.Config as cms

import TopPtWeightSchemes as _schemes

topPtWeight = cms.EDProducer("HPlusTopPtWeightProducer",
    ttGenEventSrc = cms.InputTag("genEvt"),
    alias = cms.string("topPtWeight"),
    enabled = cms.bool(False),
    variationEnabled = cms.bool(False),
    variationDirection = cms.int32(0),
)

for name, values in _schemes.schemes.iteritems():
    setattr(topPtWeight, name, cms.PSet(
            allhadronic = cms.string(values.allhadronic),
            leptonjets = cms.string(values.leptonjets),
            dilepton = cms.string(values.dilepton),
            ))
topPtWeight.scheme = cms.string(_schemes.defaultScheme)


def addTtGenEvent(process, sequence):
    if not hasattr(process, "makeGenEvt"):
        process.load("TopQuarkAnalysis.TopEventProducers.sequences.ttGenEvent_cff")
        process.decaySubset.fillMode = cms.string("kME")
        sequence += process.makeGenEvt
