import FWCore.ParameterSet.Config as cms

  
from Configuration.Generator.PythiaUESettings_cfi import *

TauolaNoPolar = cms.PSet(
    UseTauolaPolarization = cms.bool(False)
)
TauolaPolar = cms.PSet(
   UseTauolaPolarization = cms.bool(True)
)

### Tighten the muon selection (but no isolation yet)
tightenedMuons = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag("tightMuons"),
    cut = cms.string(
        "abs(eta()) < 2.1"
        # chi2<10 && globalTrack().hitPattern().numberOfValidMuonHits() > 0
        "&& muonID('GlobalMuonPromptTight')"
        "&& numberOfMatchedStations() > 1"
        "&& abs(dB()) < 0.2" 
        "&& innerTrack().hitPattern().numberOfValidPixelHits() > 0"
        "&& track().hitPattern().trackerLayersWithMeasurement() > 8"
    )
)
tightenedMuonsFilter = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("tightenedMuons"),
    minNumber = cms.uint32(1)
)
tightenedMuonsCount = cms.EDProducer("EventCountProducer")

### Muon isolation step

#tauEmbeddingMuons = cms.EDFilter("HPlusSmallestRelIsoPATMuonViewSelector",
#    src = cms.InputTag("tightenedMuons"),
#    filter = cms.bool(False),
#    maxNumber = cms.uint32(1)
#)
import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.customisations as customisations
tightenedMuonsWithIso = customisations.constructMuonIsolationOnTheFly("tightenedMuons", embedPrefix="embeddingStep_")

### Trigger matching
## Matching is added in pf_customize.py
tightenedMuonsMatched = cms.EDProducer("HPlusMuonTriggerMatchSelector",
   src = cms.InputTag("tightenedMuonsWithIso"),
   patTriggerEventSrc = cms.InputTag("patTriggerEvent"),
   deltaR = cms.double(0.1),
   filterNames = cms.vstring("dummy"),
   enabled = cms.bool(False)
)
tightenedMuonsMatchedFilter = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("tightenedMuonsMatched"),
    minNumber = cms.uint32(1)
)
tightenedMuonsMatchedCount = cms.EDProducer("EventCountProducer")

# MuScleFit correction
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/MuScleFitCorrections2012
muscleCorrectedMuons = cms.EDProducer("MuScleFitPATMuonCorrector", 
    src = cms.InputTag("tightenedMuonsMatched"),
    debug = cms.bool(False), 
    identifier = cms.string("DUMMY"),
    applySmearing = cms.bool(False), 
    fakeSmearing = cms.bool(False)
)
# Must do all pt-dependent selections here because of momentum correction
tauEmbeddingMuons = cms.EDProducer("HPlusPATMuonTunePCorrector",
    src = cms.InputTag("muscleCorrectedMuons"),
    originalSrc = cms.InputTag("tightenedMuonsMatched"),
    finalizeId = cms.bool(True),
    idMaxChi2 = cms.double(10.0),
    idMaxPtError = cms.double(0.03),
    idCut = cms.string("pt() > 41 && chargedHadronIso()/pt() < 0.1"), # <--- This is the current isolation
#    idCut = cms.string("(userFloat('embeddingStep_pfChargedHadrons') + max(userFloat('embeddingStep_pfPhotons')-0.5*userFloat('embeddingStep_pfPUChargedHadrons'), 0)) < 2") 
#    idCut = cms.string("(userInt('byTightIc04ChargedOccupancy') + userInt('byTightIc04GammaOccupancy')) == 0")
)
tauEmbeddingMuonsFilter = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("tauEmbeddingMuons"),
    minNumber = cms.uint32(1),
)
tauEmbeddingMuonsCount = cms.EDProducer("EventCountProducer")
tauEmbeddingMuonsOneFilter = cms.EDFilter("PATCandViewCountFilter",
    src = cms.InputTag("tauEmbeddingMuons"),
    minNumber = cms.uint32(1),
    maxNumber = cms.uint32(1),
)
tauEmbeddingMuonsOneCount = cms.EDProducer("EventCountProducer")

### Jet selection finalization
# Currently done as a part of the analysis job
# tightenedJets = cms.EDFilter("PATJetSelector",
#     src = cms.InputTag("selectedPatJets"),
#     cut = cms.string(
#     "pt() > 30 && abs(eta()) < 2.4"
#     "&& numberOfDaughters() > 1 && chargedEmEnergyFraction() < 0.99"
#     "&& neutralHadronEnergyFraction() < 0.99 && neutralEmEnergyFraction < 0.99"
#     "&& chargedHadronEnergyFraction() > 0 && chargedMultiplicity() > 0" # eta < 2.4, so don't need the requirement here
#     ),
#     checkOverlaps = cms.PSet(
#         muons = cms.PSet(
#             src                 = cms.InputTag("tauEmbeddingMuons"),
#             algorithm           = cms.string("byDeltaR"),
#             preselection        = cms.string(""),
#             deltaR              = cms.double(0.1),
#             checkRecoComponents = cms.bool(False),
#             pairCut             = cms.string(""),
#             requireNoOverlaps   = cms.bool(True),
#         )
#     )
# )
# tightenedJetsFilter = cms.EDFilter("CandViewCountFilter",
#     src = cms.InputTag("tightenedJets"),
#     minNumber = cms.uint32(3)
# )
# tightenedJetsCount = cms.EDProducer("EventCountProducer")


adaptedMuonsFromWmunu = cms.EDProducer("HPlusMuonMetAdapter",
   muonSrc = cms.untracked.InputTag("tauEmbeddingMuons"),
   metSrc = cms.untracked.InputTag("pfMet")
)


dimuonsGlobal = cms.EDProducer('ZmumuPFEmbedder',
    tracks = cms.InputTag("generalTracks"),
    selectedMuons = cms.InputTag("tauEmbeddingMuons"),
)

filterEmptyEv = cms.EDFilter("EmptyEventsFilter",
    target =  cms.untracked.int32(1),
    src = cms.untracked.InputTag("generator")
)

muonSelectionCounters = [ "tightenedMuonsCount", 
                          "tightenedMuonsMatchedCount",
                          "tauEmbeddingMuonsCount", "tauEmbeddingMuonsOneCount",
#                          "tightenedJetsCount"
                          ]

# Avoid compilation error when TauAnalysis/MCEmbeddingTools is missing
try:
    from TauAnalysis.MCEmbeddingTools.MCParticleReplacer_cfi import *
    newSource.algorithm = "ZTauTau"

    # See https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideTauolaInterface for mdtau parameter
    newSource.ZTauTau.TauolaOptions.InputCards.mdtau = cms.int32(0) # for all decay modes
    #newSource.ZTauTau.TauolaOptions.InputCards.mdtau = cms.int32(230) # for hadronic modes
    newSource.ZTauTau.minVisibleTransverseMomentum = cms.untracked.string("")
    newSource.ZTauTau.transformationMode = cms.untracked.int32(3)

    generator = newSource.clone()
    generator.src = cms.InputTag("adaptedMuonsFromWmunu")

    ProductionFilterSequence = cms.Sequence(
        tightenedMuons *
        tightenedMuonsFilter *
        tightenedMuonsCount *
        tightenedMuonsWithIso *
        tightenedMuonsMatched *
        tightenedMuonsMatchedFilter *
        tightenedMuonsMatchedCount *
        muscleCorrectedMuons *
        tauEmbeddingMuons *
        tauEmbeddingMuonsFilter *
        tauEmbeddingMuonsCount *
        tauEmbeddingMuonsOneFilter *
        tauEmbeddingMuonsOneCount *
#        tightenedJets *
#        tightenedJetsFilter *
#        tightenedJetsCount *
        adaptedMuonsFromWmunu *
        dimuonsGlobal * 
        generator * 
        filterEmptyEv
    )
except ImportError:
    print
    print "  TauAnalysis/MCEmbeddingTools package is missing"
    print
    pass

