import FWCore.ParameterSet.Config as cms

# Prefix all modules/sequences with the base name of the file, first
# letter lowercased (skimFourJetsChs in this case)

# Provide the skimming sequence with the base name + Sequence
# (skimFourJetsChsSequence in this case)

skimFourJetsChsJets = cms.EDFilter("PATJetSelector",
    src = cms.InputTag("selectedPatJetsPFlowChs"),
    cut = cms.string("pt() > 10 && abs(eta()) < 2.5")
)
skimFourJetsChsJetsFilter = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("skimFourJetsChsJets"),
    minNumber = cms.uint32(4)
)
skimFourJetsChsJetsCount = cms.EDProducer("EventCountProducer")


skimFourJetsChsSequence = cms.Sequence(
    skimFourJetsChsJets *
    skimFourJetsChsJetsFilter *
    skimFourJetsChsJetsCount
)

counters = [
    "skimFourJetsChsJetsCount"
]
