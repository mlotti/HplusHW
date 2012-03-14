import FWCore.ParameterSet.Config as cms

skimMuons = cms.EDFilter("PATMuonSelector",
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
skimMuonsFilter = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("skimMuons"),
    minNumber = cms.uint32(1)
)
skimMuonsCount = cms.EDProducer("EventCountProducer")


skimSequence = cms.Sequence(
    skimMuons *
    skimMuonsFilter *
    skimMuonsCount
)

counters = [
    "skimMuonsCount"
]
