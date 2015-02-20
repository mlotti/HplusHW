import FWCore.ParameterSet.Config as cms

pfRelIso = "( userIsolation('PfChargedHadronIso') + userIsolation('PfNeutralHadronIso') + userIsolation('PfGammaIso') )/pt()"

selectedPatMuonsHighPurity = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag("selectedPatMuons"),
    cut = cms.string(pfRelIso+" < 0.1")
)

selectedPatMuonsHighPurityFilter = cms.EDFilter("PATCandViewCountFilter",
    src = cms.InputTag("selectedPatMuonsHighPurity"),
    minNumber = cms.uint32(1),
    maxNumber = cms.uint32(1),
)

vetoPatMuonsHighPurity = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag("selectedPatMuons"),
    cut = cms.string("pt() > 15 && abs(eta()) < 2.4 && isGlobalMuon() && "+pfRelIso+" < 0.15")
)                     
vetoPatMuonsHighPurityFilter = cms.EDFilter(
    "PATCandViewCountFilter",
    src = cms.InputTag("vetoPatMuonsHighPurity"),
    minNumber = cms.uint32(0),
    maxNumber = cms.uint32(1), # this corresponds the one in selectedPatMuonsHighPurity
)

selectedPatTausHpsPFTauHighPurity = cms.EDFilter("PATTauSelector",
#    src = cms.InputTag("selectedPatTaus"),
    src = cms.InputTag("selectedPatTausHpsPFTau"),
    cut = cms.string("leadPFChargedHadrCand().isNonnull() && leadPFChargedHadrCand().pt() > 20"
##                     " && tauID('againstElectronMedium') && tauID('againstMuonTight')"
                     " && tauID('decayModeFinding')"
##                   " && tauID('byTightCombinedIsolationDeltaBetaCorr')"
                     " && signalPFChargedHadrCands().size() == 1"
                     )
)
selectedPatTausHpsPFTauHighPurityFilter = cms.EDFilter("PATCandViewCountFilter",
    src = cms.InputTag("selectedPatTausHpsPFTauHighPurity"),
    minNumber = cms.uint32(1),
    maxNumber = cms.uint32(1),
)

import HiggsAnalysis.HeavyChHiggsToTauNu.TauLegZMuTauFilter as zmutau

muTauPairsHighPurity = zmutau.muTauPairs.clone(
    decay = "selectedPatMuonsHighPurity@+ selectedPatTausHpsPFTauHighPurity@-"
)
muTauPairsHighPurityFilter = cms.EDFilter("PATCandViewCountFilter",
    src = cms.InputTag("muTauPairsHighPurity"),
    minNumber = cms.uint32(1),
    maxNumber = cms.uint32(1)
)

highPurityAllEvents      = cms.EDProducer("EventCountProducer")
highPuritySelectedEvents = cms.EDProducer("EventCountProducer")

def getSelectionCounters():
    return ["highPurityAllEvents",
            "highPuritySelectedEvents"]

highPuritySequence = cms.Sequence(
    highPurityAllEvents *    
    selectedPatMuonsHighPurity *
    selectedPatMuonsHighPurityFilter *
    vetoPatMuonsHighPurity *
    vetoPatMuonsHighPurityFilter *
    selectedPatTausHpsPFTauHighPurity *
    selectedPatTausHpsPFTauHighPurityFilter *
    muTauPairsHighPurity *
    muTauPairsHighPurityFilter *
    highPuritySelectedEvents
)
