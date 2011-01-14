import FWCore.ParameterSet.Config as cms

muonSelectionAllEvents = cms.EDProducer("EventCountProducer")

from HLTrigger.HLTfilters.triggerResultsFilter_cfi import triggerResultsFilter
muonTrigger = triggerResultsFilter.clone()
muonTrigger.hltResults = cms.InputTag("TriggerResults")
muonTrigger.l1tResults = cms.InputTag("") # dummy
muonTrigger.throw = cms.bool(True)
muonTrigger.triggerConditions = cms.vstring("HLT_Mu9")
muonSelectionTriggered = cms.EDProducer("EventCountProducer")


muonFirstPrimaryVertex = cms.EDProducer(
    "HPlusSelectFirstVertex",
    src = cms.InputTag("offlinePrimaryVertices")
)
muonGoodPrimaryVertex = cms.EDFilter("VertexSelector",
    filter = cms.bool(False),
    src = cms.InputTag("muonFirstPrimaryVertex"),
    cut = cms.string("!isFake && ndof > 4 && abs(z) < 24.0 && position.rho < 2.0")
)
muonPrimaryVertexFilter = cms.EDFilter("VertexCountFilter",
    src = cms.InputTag("muonGoodPrimaryVertex"),
    minNumber = cms.uint32(1),
    maxNumber = cms.uint32(999)
)
muonSelectionPrimaryVertex = cms.EDProducer("EventCountProducer")

tightMuons = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag("selectedPatMuons"),
    cut = cms.string(
    "isGlobalMuon() && isTrackerMuon()"
    "&& pt() > 30 && abs(eta()) < 2.1"
    "&& muonID('GlobalMuonPromptTight')"
    "&& innerTrack().numberOfValidHits() > 10"
    "&& innerTrack().hitPattern().pixelLayersWithMeasurement() >= 1"
    "&& numberOfMatches() > 1"
    "&& abs(dB()) < 0.02"
#    "&& (isolationR03().emEt+isolationR03().hadEt+isolationR03().sumPt)/pt() < 0.05",
    )
)
tightMuonsZ = cms.EDFilter("HPlusPATMuonViewVertexZSelector",
    src = cms.InputTag("tightMuons"),
    vertexSrc = cms.InputTag("muonGoodPrimaryVertex"),
    maxZ = cms.double(1.0)
)
tightMuonsFilter = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("tightMuonsZ"),
    minNumber = cms.uint32(1)
)
tauEmbeddingMuons = cms.EDFilter("HPlusLargestPtPATMuonViewSelector",
    src = cms.InputTag("tightMuonsZ"),
    filter = cms.bool(False),
    maxNumber = cms.uint32(1)
)
muonSelectionMuons = cms.EDProducer("EventCountProducer")


from PhysicsTools.PatAlgos.cleaningLayer1.jetCleaner_cfi import *
goodJets = cleanPatJets.clone(
    src = cms.InputTag("selectedPatJetsAK5PF"),
    preselection = "pt() > 30 && abs(eta()) < 2.4",
    checkOverlaps = cms.PSet(
        muons = cms.PSet(
            src                 = cms.InputTag("tightMuonsZ"),
            algorithm           = cms.string("byDeltaR"),
            preselection        = cms.string(""),
            deltaR              = cms.double(0.1),
            checkRecoComponents = cms.bool(False),
            pairCut             = cms.string(""),
            requireNoOverlaps   = cms.bool(True),
        )
    )
)
goodJetFilter = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("goodJets"),
    minNumber = cms.uint32(3)
)
muonSelectionJets = cms.EDProducer("EventCountProducer")

# goodMet = cms.EDFilter("PATMETSelector",
#     src = cms.InputTag("patMETsPF"),
#     cut = cms.string("et() > 40")
# )
# goodMetFilter = cms.EDFilter("CandViewCountFilter",
#     src = cms.InputTag("goodMet"),
#     minNumber = cms.uint32(1)
# )
# muonSelectionMet = cms.EDProducer("EventCountProducer")



muonSelectionSequence = cms.Sequence(
    muonSelectionAllEvents
    * muonTrigger * muonSelectionTriggered
    * muonFirstPrimaryVertex * muonGoodPrimaryVertex * muonPrimaryVertexFilter * muonSelectionPrimaryVertex
    * tightMuons 
    * tightMuonsZ 
    * tightMuonsFilter
    * tauEmbeddingMuons 
    * muonSelectionMuons
    * goodJets      * goodJetFilter * muonSelectionJets
#    * goodMet       * goodMetFilter * muonSelectionMet
)
