import FWCore.ParameterSet.Config as cms

# Prefix all modules/sequences with the base name of the file, first
# letter lowercased (skimFourJets in this case)

# Provide the skimming sequence with the base name + Sequence
# (skimFourJetsSequence in this case)

skimFourJetsJets = cms.EDFilter("PATJetSelector",
    src = cms.InputTag("selectedPatJetsPFlow"),
    cut = cms.string("pt() > 10 && abs(eta()) < 2.5")
)
skimFourJetsJetsFilter = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("skimFourJetsJets"),
    minNumber = cms.uint32(4)
)
skimFourJetsJetsCount = cms.EDProducer("EventCountProducer")


skimFourJetsSequence = cms.Sequence(
    skimFourJetsJets *
    skimFourJetsJetsFilter *
    skimFourJetsJetsCount
)

counters = [
    "skimFourJetsJetsCount"
]
