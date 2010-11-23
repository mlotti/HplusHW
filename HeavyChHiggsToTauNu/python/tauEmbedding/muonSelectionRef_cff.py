import FWCore.ParameterSet.Config as cms

# References for muon selection:
# https://twiki.cern.ch/twiki/bin/view/CMS/WorkBookPATExampleTopQuarks
# https://twiki.cern.ch/twiki/bin/view/CMS/TopLeptonPlusJetsRefSel_mu

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


goodJets = cms.EDFilter("PATJetSelector",
    src = cms.InputTag("selectedPatJets"),
    cut = cms.string("pt() > 30 && abs(eta()) < 2.4")
)
goodJetFilter = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("goodJets"),
    minNumber = cms.uint32(3)
)
muonSelectionJets = cms.EDProducer("EventCountProducer")

from PhysicsTools.PatAlgos.cleaningLayer1.muonCleaner_cfi import *
tauEmbeddingMuons = cleanPatMuons.clone(
    preselection = 
    "isGlobalMuon() && isTrackerMuon()"
    "&& pt() > 40 && abs(eta()) < 2.1"
    "&& muonID('GlobalMuonPromptTight')"
    "&& innerTrack().numberOfValidHits() > 10"
    "&& innerTrack().hitPattern().pixelLayersWithMeasurement() >= 1"
    "&& numberOfMatches() > 1"
    "&& abs(dB()) < 0.02"
    "&& (isolationR03().emEt+isolationR03().hadEt+isolationR03().sumPt)/pt() < 0.05",
    checkOverlaps = cms.PSet(
        jets = cms.PSet(
            src                 = cms.InputTag("goodJets"),
            algorithm           = cms.string("byDeltaR"),
            preselection        = cms.string(""),
            deltaR              = cms.double(0.3),
            checkRecoComponents = cms.bool(False),
            pairCut             = cms.string(""),
            requireNoOverlaps   = cms.bool(True),
        )
    )
)
tauEmbeddingMuonsZ = cms.EDProducer("HPlusCandViewPtrVertexZSelector",
    src = cms.InputTag("tauEmbeddingMuons"),
    vertexSrc = cms.InputTag("muonGoodPrimaryVertex"),
    maxZ = cms.double(1.0)
)
tauEmbeddingMuonsFilter = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("tauEmbeddingMuonsZ"),
    minNumber = cms.uint32(1)
)
muonSelectionMuons = cms.EDProducer("EventCountProducer")


from PhysicsTools.PatAlgos.selectionLayer1.muonSelector_cfi import *
vetoMuons = selectedPatMuons.clone(
    src = "selectedPatMuons",
    cut =
    "isGlobalMuon && pt > 10. && abs(eta) < 2.5"
    "&& (isolationR03().emEt+isolationR03().hadEt+isolationR03().sumPt)/pt() < 0.2"
)
vetoMuonsFilter = cms.EDFilter("PATCandViewCountFilter",
    src = cms.InputTag("vetoMuons"),
    minNumber = cms.uint32(1), # vetoMuons include also tauEmbeddingMuons
    maxNumber = cms.uint32(1)
)
muonSelectionMuonVeto = cms.EDProducer("EventCountProducer")

from PhysicsTools.PatAlgos.selectionLayer1.electronSelector_cfi import *
vetoElectrons = selectedPatElectrons.clone(
    src = cms.InputTag("selectedPatElectrons"),
    cut = cms.string("et() > 15 && abs(eta()) < 2.5 && (dr03TkSumPt()+dr03EcalRecHitSumEt()+dr03HcalTowerSumEt())/et() < 0.2")
)
vetoElectronsFilter = cms.EDFilter("PATCandViewCountFilter",
    src = cms.InputTag("vetoElectrons"),
    minNumber = cms.uint32(0),
    maxNumber = cms.uint32(0)
)
muonSelectionElectronVeto = cms.EDProducer("EventCountProducer")

muonSelectionSequence = cms.Sequence(
    muonSelectionAllEvents
    * muonTrigger * muonSelectionTriggered
    * muonFirstPrimaryVertex * muonGoodPrimaryVertex * muonPrimaryVertexFilter * muonSelectionPrimaryVertex
    * goodJets      * goodJetFilter * muonSelectionJets
    * tauEmbeddingMuons    * tauEmbeddingMuonsZ    * tauEmbeddingMuonsFilter * muonSelectionMuons
    * vetoMuons     * vetoMuonsFilter * muonSelectionMuonVeto
    * vetoElectrons * vetoElectronsFilter * muonSelectionElectronVeto
)
