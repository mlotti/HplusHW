import FWCore.ParameterSet.Config as cms

# Prefix all modules/sequences with the base name of the file, first
# letter lowercased (skimSignalTriggerJets in this case)

# Provide the skimming sequence with the base name + Sequence
# (skimSignalTriggerJetsSequence in this case)

skimSignalTriggerJetsJets = cms.EDFilter("PATJetSelector",
    src = cms.InputTag("selectedPatJetsPFlow"),
    cut = cms.string("pt() > 10 && abs(eta()) < 2.5")
)
skimSignalTriggerJetsJetsFilter = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("skimSignalTriggerJetsJets"),
    minNumber = cms.uint32(4)
)
skimSignalTriggerJetsJetsCount = cms.EDProducer("EventCountProducer")


skimSignalTriggerJetsSequence = cms.Sequence(
    skimSignalTriggerJetsJets *
    skimSignalTriggerJetsJetsFilter *
    skimSignalTriggerJetsJetsCount
)

counters = [
    "skimSignalTriggerJetsJetsCount"
]
