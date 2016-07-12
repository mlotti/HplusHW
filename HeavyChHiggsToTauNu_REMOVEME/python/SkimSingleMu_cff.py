import FWCore.ParameterSet.Config as cms

# Prefix all modules/sequences with the base name of the file, first
# letter lowercased (skimSingleMu in this case)

# Provide the skimming sequence with the base name + Sequence
# (skimSingleMuSequence in this case)

skimSingleMuMuons = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag("selectedPatMuons"),
    cut = cms.string(
    "isGlobalMuon() && isTrackerMuon()"
    "&& pt() > 12"
    "&& muonID('GlobalMuonPromptTight')"
    "&& innerTrack().numberOfValidHits() > 10"
    "&& innerTrack().hitPattern().pixelLayersWithMeasurement() >= 1"
    "&& numberOfMatches() > 1"
    )
)
skimSingleMuMuonsFilter = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("skimMuons"),
    minNumber = cms.uint32(1)
)
skimSingleMuMuonsCount = cms.EDProducer("EventCountProducer")


skimSingleMuSequence = cms.Sequence(
    skimSingleMuMuons *
    skimSingleMuMuonsFilter *
    skimSingleMuMuonsCount
)

counters = [
    "skimSingleMuMuonsCount"
]
