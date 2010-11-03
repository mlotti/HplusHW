import FWCore.ParameterSet.Config as cms

# WARNING: the trigger path is modified in signalAnalysis_cfg.py depending on
# the data version
trigger = cms.untracked.PSet(
    src = cms.untracked.InputTag("patTriggerEvent"),
    trigger = cms.untracked.string("HLT_SingleLooseIsoTau20") # in 36X/35X MC and Run2010A data
#    trigger = cms.untracked.string("HLT_SingleIsoTau20_Trk5_MET20") # in 38X MC and Run2010B data
)
TriggerMETEmulation = cms.untracked.PSet(
    src = cms.untracked.InputTag("patMETs"), # calo MET
    metEmulationCut = cms.untracked.double(30.0)
)

tauSelectionBase = cms.untracked.PSet(
    src = cms.untracked.InputTag("selectedPatTausShrinkingConePFTau"),
    selection = cms.untracked.string(""),
    ptCut = cms.untracked.double(0), # tau-Jet Et will be optimised so don't apply any cut.
    etaCut = cms.untracked.double(2.4),
    leadingTrackPtCut = cms.untracked.double(20), # keep as 20 GeV/c so that we are not biased by different triggers (Lauri)
    rtauCut = cms.untracked.double(0.2),
    invMassCut = cms.untracked.double(1.5)
)
### Copy the tauSelectionBase and overwrite arguments if necessary
# CaloTau
tauSelectionCaloTauCutBased = tauSelectionBase.clone()
tauSelectionCaloTauCutBased.src = cms.untracked.InputTag("selectedPatTausCaloRecoTau")
tauSelectionCaloTauCutBased.selection = cms.untracked.string("CaloTauCutBased")
# PF Shrinking Cone Tau
tauSelectionShrinkingConeCutBased = tauSelectionBase.clone()
tauSelectionShrinkingConeCutBased.src = cms.untracked.InputTag("selectedPatTausShrinkingConePFTau")
tauSelectionShrinkingConeCutBased.selection = cms.untracked.string("ShrinkingConePFTauCutBased")
# TaNC (PF Shrinking Cone based)
tauSelectionShrinkingConeTaNCBased = tauSelectionBase.clone()
tauSelectionShrinkingConeTaNCBased.src = cms.untracked.InputTag("selectedPatTausShrinkingConePFTau")
tauSelectionShrinkingConeTaNCBased.selection = cms.untracked.string("ShrinkingConePFTauTaNCBased")
# HPS (PF Shrinking Cone based)
tauSelectionHPSTauBased = tauSelectionBase.clone()
tauSelectionHPSTauBased.src = cms.untracked.InputTag("selectedPatTausHpsPFTau")
tauSelectionHPSTauBased.selection = cms.untracked.string("HPSTauBased")

#tauSelection = tauSelectionShrinkingConeCutBased
#tauSelection = tauSelectionShrinkingConeTaNCBased
#tauSelection = tauSelectionCaloTauCutBased
tauSelection = tauSelectionHPSTauBased

jetSelection = cms.untracked.PSet(
    src = cms.untracked.InputTag("selectedPatJets"),
#   src = cms.untracked.InputTag("selectedPatJetsAK5PF"),
    src_met = cms.untracked.InputTag("patMETsPF"), # calo MET 
    #src = cms.untracked.InputTag("selectedPatJetsAK5JPT"),
    cleanTauDR = cms.untracked.double(0.5),
    ptCut = cms.untracked.double(30),
    etaCut = cms.untracked.double(2.4),
    minNumber = cms.untracked.uint32(1),
    METCut = cms.untracked.double(0.0)
)

MET = cms.untracked.PSet(
    src = cms.untracked.InputTag("patMETsPF"), # PF MET
    #src = cms.untracked.InputTag("patMETs"), # calo MET
    #src = cms.untracked.InputTag("patMETsTC"), # tc MET
    METCut = cms.untracked.double(0.0)
)

bTagging = cms.untracked.PSet(
    discriminator = cms.untracked.string("trackCountingHighEffBJetTags"),
    discriminatorCut = cms.untracked.double(2.0),
    ptCut = cms.untracked.double(30),
    etaCut = cms.untracked.double(2.4),
    minNumber = cms.untracked.uint32(0)
)

EvtTopology = cms.untracked.PSet(
    #discriminator = cms.untracked.string("test"),
    #discriminatorCut = cms.untracked.double(0.0),
    #alphaT = cms.untracked.double(-5.00)
    alphaT = cms.untracked.double(-5.0)
)

GlobalElectronVeto = cms.untracked.PSet(
    ElectronCollectionName = cms.untracked.InputTag("selectedPatElectrons"),
    ElectronSelection = cms.untracked.string("kTightElectronIdentification"),
    ElectronPtCut = cms.untracked.double(20.0),
    ElectronEtaCut = cms.untracked.double(2.5)
)

GlobalMuonVeto = cms.untracked.PSet(
    MuonCollectionName = cms.untracked.InputTag("selectedPatMuons"),
    MuonSelection = cms.untracked.string("GlobalMuonPromptTight"),
    MuonPtCut = cms.untracked.double(20.0),
    MuonEtaCut = cms.untracked.double(2.5)
)

transverseMassCut = cms.untracked.double(0.0)
