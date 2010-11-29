import FWCore.ParameterSet.Config as cms

# WARNING: the trigger path is modified in signalAnalysis_cfg.py depending on
# the data version
trigger = cms.untracked.PSet(
    src = cms.untracked.InputTag("patTriggerEvent"),
    triggers = cms.untracked.vstring("HLT_SingleIsoTau20_Trk5",
                                     "HLT_SingleIsoTau20_Trk15_MET20",
                                     "HLT_SingleIsoTau20_Trk15_MET25_v3",
                                     "HLT_SingleIsoTau20_Trk15_MET25_v4"
    ),
    hltMetCut = cms.untracked.double(20.0),
)
#TriggerMETEmulation = cms.untracked.PSet(
#    src = cms.untracked.InputTag("patMETs"), # calo MET
#    metEmulationCut = cms.untracked.double(30.0)
#)

useFactorizedTauID = cms.untracked.bool(True) # FIXME: set to false

import HiggsAnalysis.HeavyChHiggsToTauNu.HChTauIDFactorization_cfi as factorizationParams
tauSelectionBase = cms.untracked.PSet(
    src = cms.untracked.InputTag("blahblahblah"),
    selection = cms.untracked.string(""),
    ptCut = cms.untracked.double(30),
    etaCut = cms.untracked.double(2.4), #no change
    leadingTrackPtCut = cms.untracked.double(20),
    rtauCut = cms.untracked.double(0.8), #no change
    invMassCut = cms.untracked.double(999.), #no change
    nprongs = cms.untracked.uint32(1), # not used at the moment FIXME: use it in TauSelection.cc
    factorization = factorizationParams.tauIDFactorizationParameters
)

#tauSelectionFactorized = tauSelection.clone()
#tauSelectionFactorized.extend(factorizationParams)

# Reco CaloTau
tauSelectionCaloTauCutBasedJESPlus05 = tauSelectionBase.clone()
tauSelectionCaloTauCutBasedJESPlus05.src = cms.untracked.InputTag("JESPlus05CaloRecoTau")
tauSelectionCaloTauCutBasedJESPlus05.selection = cms.untracked.string("CaloTauCutBased")
#
tauSelectionCaloTauCutBasedJESMinus05 = tauSelectionBase.clone()
tauSelectionCaloTauCutBasedJESMinus05.src = cms.untracked.InputTag("JESMinus05CaloRecoTau")
tauSelectionCaloTauCutBasedJESMinus05.selection = cms.untracked.string("CaloTauCutBased")
# PF Shrinking Cone
tauSelectionShrinkingConeCutBasedJESPlus05 = tauSelectionBase.clone()
tauSelectionShrinkingConeCutBasedJESPlus05.src = cms.untracked.InputTag("JESPlus05ShrinkingConePFTau")
tauSelectionShrinkingConeCutBasedJESPlus05.selection = cms.untracked.string("ShrinkingConePFTauCutBased")
#
tauSelectionShrinkingConeCutBasedJESMinus05 = tauSelectionBase.clone()
tauSelectionShrinkingConeCutBasedJESMinus05.src = cms.untracked.InputTag("JESMinus05ShrinkingConePFTau")
tauSelectionShrinkingConeCutBasedJESMinus05.selection = cms.untracked.string("ShrinkingConePFTauCutBased")
# TaNC
tauSelectionShrinkingConeTaNCBasedJESPlus05 = tauSelectionBase.clone()
tauSelectionShrinkingConeTaNCBasedJESPlus05.src = cms.untracked.InputTag("JESPlus05ShrinkingConeTaNC")
tauSelectionShrinkingConeTaNCBasedJESPlus05.selection = cms.untracked.string("ShrinkingConePFTauTaNCBased")
#
tauSelectionShrinkingConeTaNCBasedJESMinus05 = tauSelectionBase.clone()
tauSelectionShrinkingConeTaNCBasedJESMinus05.src = cms.untracked.InputTag("JESMinus05ShrinkingConeTaNC")
tauSelectionShrinkingConeTaNCBasedJESMinus05.selection = cms.untracked.string("ShrinkingConePFTauTaNCBased")
# HPS
tauSelectionHPSTauBasedJESPlus05 = tauSelectionBase.clone()
tauSelectionHPSTauBasedJESPlus05.src = cms.untracked.InputTag("JESPlus05HPS")
tauSelectionHPSTauBasedJESPlus05.selection = cms.untracked.string("HPSTauBased")
#
tauSelectionHPSTauBasedJESMinus05 = tauSelectionBase.clone()
tauSelectionHPSTauBasedJESMinus05.src = cms.untracked.InputTag("JESMinus05HPS")
tauSelectionHPSTauBasedJESMinus05.selection = cms.untracked.string("HPSTauBased")

### JESPlus05
#tauSelection = tauSelectionShrinkingConeCutBasedJESPlus05
#tauSelection = tauSelectionShrinkingConeTaNCBasedJESPlus05
#tauSelection = tauSelectionCaloTauCutBasedJESPlus05
tauSelection = tauSelectionHPSTauBasedJESPlus05
### JESMinus05
#tauSelection = tauSelectionShrinkingConeCutBasedJESMinus05
#tauSelection = tauSelectionShrinkingConeTaNCBasedJESMinus05
#tauSelection = tauSelectionCaloTauCutBasedJESMinus05
#tauSelection = tauSelectionHPSTauBasedJESMinus05
print "tauSelection.src :", tauSelection.src

jetSelection = cms.untracked.PSet(
    #src = cms.untracked.InputTag("selectedPatJets"),       # Calo jets
    #src = cms.untracked.InputTag("selectedPatJetsAK5JPT"), # JPT jets 
    #src = cms.untracked.InputTag("selectedPatJetsAK5PF"),  # PF jets
    src = tauSelection.src, 
    src_met = tauSelection.src,
    #src_met = cms.untracked.InputTag("patMETsPF"), # calo MET
    cleanTauDR = cms.untracked.double(0.5), #no change
    ptCut = cms.untracked.double(30),
    etaCut = cms.untracked.double(2.4),
    minNumber = cms.untracked.uint32(3),
    METCut = cms.untracked.double(70.0)
)

MET = cms.untracked.PSet(
    # src = cms.untracked.InputTag("patMETs"), # calo MET
    # src = cms.untracked.InputTag("patMETsPF"), # PF MET
    # src = cms.untracked.InputTag("patMETsTC"), # tc MET
    src = tauSelection.src, 
    METCut = cms.untracked.double(70.0)
)

bTagging = cms.untracked.PSet(
    discriminator = cms.untracked.string("trackCountingHighEffBJetTags"),
    discriminatorCut = cms.untracked.double(2.0),
    ptCut = cms.untracked.double(30),
    etaCut = cms.untracked.double(2.4),
    minNumber = cms.untracked.uint32(1)
)

transverseMassCut = cms.untracked.double(100)

EvtTopology = cms.untracked.PSet(
    #discriminator = cms.untracked.string("test"),
    #discriminatorCut = cms.untracked.double(0.0),
    #alphaT = cms.untracked.double(-5.00)
    alphaT = cms.untracked.double(-5.0)
)
GlobalElectronVeto = cms.untracked.PSet(
    ElectronCollectionName = cms.untracked.InputTag("selectedPatElectrons"),
    ElectronSelection = cms.untracked.string("simpleEleId95relIso"),
    ElectronPtCut = cms.untracked.double(20.0),
    ElectronEtaCut = cms.untracked.double(2.5)
)

GlobalMuonVeto = cms.untracked.PSet(
    MuonCollectionName = cms.untracked.InputTag("selectedPatMuons"),
    MuonSelection = cms.untracked.string("GlobalMuonPromptTight"),
    MuonPtCut = cms.untracked.double(20.0),
    MuonEtaCut = cms.untracked.double(2.5)
)

fakeMETVeto = cms.untracked.PSet(
  src = MET.src,
  maxDeltaPhi = cms.untracked.double(999.)
)
