import FWCore.ParameterSet.Config as cms

# References for muon selection:
# https://twiki.cern.ch/twiki/bin/view/CMS/WorkBookPATExampleTopQuarks
# https://twiki.cern.ch/twiki/bin/view/CMS/TopLeptonPlusJetsRefSel_mu

goodJets = cms.EDFilter("PATJetSelector",
    src = cms.InputTag("selectedPatJets"),
    cut = cms.string("pt() > 30 && abs(eta()) < 2.4")
)
goodJetFilter = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("goodJets"),
    minNumber = cms.uint32(3)
)

goodMet = cms.EDFilter("PATMETSelector",
    src = cms.InputTag("patMETsPF"),
    cut = cms.string("et() > 40")
)
goodMetFilter = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("goodMet"),
    minNumber = cms.uint32(1)
)

from PhysicsTools.PatAlgos.cleaningLayer1.muonCleaner_cfi import *
tightMuons = cleanPatMuons.clone(
    preselection = 
    "isGlobalMuon() && isTrackerMuon()"
    "&& pt() > 20 && abs(eta()) < 2.1"
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
tightMuonsFilter = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("tightMuons"),
    minNumber = cms.uint32(1)
)

from PhysicsTools.PatAlgos.selectionLayer1.muonSelector_cfi import *
vetoMuons = selectedPatMuons.clone(
    src = "selectedPatMuons",
    cut =
    "isGlobalMuon && pt > 10. && abs(eta) < 2.5"
    "&& (isolationR03().emEt+isolationR03().hadEt+isolationR03().sumPt)/pt() < 0.2"
)
vetoMuonsFilter = cms.EDFilter("PATCandViewCountFilter",
    src = cms.InputTag("vetoMuons"),
    minNumber = cms.uint32(1), # vetoMuons include also tightMuons
    maxNumber = cms.uint32(1)
)

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

muonSelectionSequence = cms.Sequence(
      goodJets#      * goodJetFilter
#    * goodMet       * goodMetFilter
    * tightMuons    * tightMuonsFilter
#    * vetoMuons     * vetoMuonsFilter
#    * vetoElectrons * vetoElectronsFilter
)
