import FWCore.ParameterSet.Config as cms

hpsTauSelection =  "pt() > 15 && abs(eta()) < 2.5"
hpsTauSelection += " && tauID('decayModeFinding') > 0.5"
####hpsTauSelection += " && tauID('byLooseIsolation') > 0.5"
hpsTauSelection += " && tauID('againstElectronLoose') > 0.5"
hpsTauSelection += " && tauID('againstMuonLoose') > 0.5"

muonSelection =  "isGlobalMuon() && isTrackerMuon()"
muonSelection += "&& pt() > 15 & abs(eta()) < 2.5 "
####muonSelection += "&& innerTrack().numberOfValidHits() > 10"
muonSelection += "&& track().hitPattern().trackerLayersWithMeasurement > 5" 
####muonSelection += "&& innerTrack().hitPattern().pixelLayersWithMeasurement() >= 1"
muonSelection += "&& innerTrack().hitPattern().numberOfValidPixelHits() > 0"
####muonSelection += "&& numberOfMatches() > 1"
muonSelection += "&& numberOfMatchedStations() > 1"
muonSelection += "&& globalTrack().normalizedChi2() < 10.0"
muonSelection += "&& globalTrack().hitPattern().numberOfValidMuonHits() > 0"

muTauPairs = cms.EDProducer("DeltaRMinCandCombiner",
    decay = cms.string('selectedPatMuons@+ selectedPatTaus@-'),
    checkCharge = cms.bool(False),
    cut = cms.string(''),
    name = cms.string('muTauCandidates'),
    deltaRMin = cms.double(0.7)
)

def customize(process):
    process.mutauSequence = addMuTauSelection(process)
    process.path += process.mutauSequence
    
def addMuTauSelection(process):
    process.selectedPatTaus.cut = hpsTauSelection
    process.selectedPatMuons.cut = muonSelection  

    process.zmutauAllEvents = cms.EDProducer("EventCountProducer")

    process.selectedTauFilter = cms.EDFilter("CandViewCountFilter",
        src = cms.InputTag("selectedPatTaus"),
        minNumber = cms.uint32(1),
    )
    process.selectedMuonFilter = cms.EDFilter("CandViewCountFilter",
        src = cms.InputTag("selectedPatMuons"),
        minNumber = cms.uint32(1),
    )

    process.muTauPairs = muTauPairs.clone()
    process.muTauPairsFilter = cms.EDFilter("CandViewCountFilter",
        src = cms.InputTag('muTauPairs'),
        minNumber = cms.uint32(1),
    )

    process.zmutauSelectedEvents = cms.EDProducer("EventCountProducer")
    
    return cms.Sequence(
        process.zmutauAllEvents +
        process.selectedTauFilter +
        process.selectedMuonFilter +
        process.muTauPairs +
        process.muTauPairsFilter +
        process.zmutauSelectedEvents
    )

def getSelectionCounters():
    return ["zmutauAllEvents",
            "zmutauSelectedEvents"]
