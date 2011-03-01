import FWCore.ParameterSet.Config as cms

def customiseParamForTauEmbedding(param):
    # Change the triggers to muon
    param.trigger.triggers = ["HLT_Mu9",
                              "HLT_Mu15_v1"]
    param.trigger.hltMetCut = -1 # disable

    # Use PatJets and PFMet directly
    param.changeJetCollection(moduleLabel="selectedPatJets") # these are really AK5PF
    param.changeMetCollection(moduleLabel="pfMet") # no PAT object at the moment

    # Use the muons where the original muon is removed in global muon veto
    param.GlobalMuonVeto.MuonCollectionName.setModuleLabel("selectedPatMuonsEmbeddingMuonCleaned")

    # Use the taus matched to the original muon in tau selections
    postfix = "TauEmbeddingMuonMatched"
    param.setAllTauSelectionSrcSelectedPatTaus()
    param.forEachTauSelection(lambda x: x.src.setModuleLabel(x.src.getModuleLabel()+postfix))

    # Remove TCTau
    i = param.tauSelections.index(param.tauSelectionCaloTauCutBased)
    print "Removing %s from the list of tau selections" % param.tauSelectionNames[i]
    del param.tauSelections[i]
    del param.tauSelectionNames[i]

def addTauEmbeddingMuonTaus(process):
    seq = cms.Sequence()

    # Remove the embedding muon from the list of muons, use the rest
    # as an input for the global muon veto
    from PhysicsTools.PatAlgos.cleaningLayer1.muonCleaner_cfi import cleanPatMuons
    process.selectedPatMuonsEmbeddingMuonCleaned = cleanPatMuons.clone(
        src = cms.InputTag("selectedPatMuons"),
        checkOverlaps = cms.PSet(
            muons = cms.PSet(
                src                 = cms.InputTag("tauEmbeddingMuons"),
                algorithm           = cms.string("byDeltaR"),
                preselection        = cms.string(""),
                deltaR              = cms.double(0.1),
                checkRecoComponents = cms.bool(False),
                pairCut             = cms.string(""),
                requireNoOverlaps   = cms.bool(True),
            ),
        )
    )
    seq *= process.selectedPatMuonsEmbeddingMuonCleaned

    # Select the taus matching to the original muon
    prototype = cms.EDProducer("HPlusPATTauCandViewDeltaRSelector",
        src = cms.InputTag("dummy"),
        refSrc = cms.InputTag("tauEmbeddingMuons"),
        deltaR = cms.double(0.1),
    )

    for tau in ["selectedPatTausShrinkingConePFTau", "selectedPatTausHpsPFTau", "selectedPatTausHpsTancPFTau"]:
        m = prototype.clone(
            src = tau
        )
        setattr(process, tau+"TauEmbeddingMuonMatched", m)
        seq *= m

    return seq

    
