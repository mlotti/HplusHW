import FWCore.ParameterSet.Config as cms

# Prefix all modules/sequences with the base name of the file, first
# letter lowercased (skimSignalTriggerJetsChs in this case)

# Provide the skimming sequence with the base name + Sequence
# (skimSignalTriggerJetsChsSequence in this case)

skimSignalTriggerJetsChsJets = cms.EDFilter("PATJetSelector",
    src = cms.InputTag("selectedPatJetsPFlowChs"),
    cut = cms.string("pt() > 10 && abs(eta()) < 2.5")
)
skimSignalTriggerJetsChsJetsFilter = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("skimSignalTriggerJetsChsJets"),
    minNumber = cms.uint32(4)
)
skimSignalTriggerJetsChsJetsCount = cms.EDProducer("EventCountProducer")


skimSignalTriggerJetsChsSequence = cms.Sequence(
    skimSignalTriggerJetsChsJets *
    skimSignalTriggerJetsChsJetsFilter *
    skimSignalTriggerJetsChsJetsCount
)

counters = [
    "skimSignalTriggerJetsChsJetsCount"
]
