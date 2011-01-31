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
    hltMetCut = cms.untracked.double(30.0),
)
from HiggsAnalysis.HeavyChHiggsToTauNu.TriggerEmulationEfficiency_cfi import *

import HiggsAnalysis.HeavyChHiggsToTauNu.HChTauIDFactorization_cfi as factorizationParams
tauSelectionBase = cms.untracked.PSet(
    # Operating mode options: 'standard', 'factorized', 'antitautag', 'antiisolatedtau'
    operatingMode = cms.untracked.string("standard"), # Standard tau ID (Tau candidate selection + tau ID applied)
#    operatingMode = cms.untracked.string("factorized"), # Tau candidate selection applied, tau ID factorized
#    operatingMode = cms.untracked.string("antitautag"), # Tau candidate selection applied, required prong cut, anti-isolation, and anti-rtau
#    operatingMode = cms.untracked.string("antiisolatedtau"), # Tau candidate selection applied, required prong cut and anti-isolation
    src = cms.untracked.InputTag("selectedPatTausShrinkingConePFTauTauTriggerMatched"),
    selection = cms.untracked.string(""),
    ptCut = cms.untracked.double(30), # jet pt > value
    etaCut = cms.untracked.double(2.4), # jet |eta| < value
    leadingTrackPtCut = cms.untracked.double(20), # ldg. track > value
    rtauCut = cms.untracked.double(0.8), # rtau > value
    antiRtauCut = cms.untracked.double(0.4), # rtau < value
    invMassCut = cms.untracked.double(999.), # m(vis.tau) < value; FIXME has no effect in TauSelection.cc 
    nprongs = cms.untracked.uint32(1), # not used at the moment FIXME: has no effect in TauSelection.cc
    factorization = factorizationParams.tauIDFactorizationParameters
)

tauSelectionCaloTauCutBased = tauSelectionBase.clone()
tauSelectionCaloTauCutBased.src = cms.untracked.InputTag("selectedPatTausCaloRecoTauTauTriggerMatched")
tauSelectionCaloTauCutBased.selection = cms.untracked.string("CaloTauCutBased")

tauSelectionShrinkingConeCutBased = tauSelectionBase.clone()
tauSelectionShrinkingConeCutBased.src = cms.untracked.InputTag("selectedPatTausShrinkingConePFTauTauTriggerMatched")
tauSelectionShrinkingConeCutBased.selection = cms.untracked.string("ShrinkingConePFTauCutBased")

tauSelectionShrinkingConeTaNCBased = tauSelectionBase.clone()
tauSelectionShrinkingConeTaNCBased.src = cms.untracked.InputTag("selectedPatTausShrinkingConePFTauTauTriggerMatched")
tauSelectionShrinkingConeTaNCBased.selection = cms.untracked.string("ShrinkingConePFTauTaNCBased")

tauSelectionHPSTauBased = tauSelectionBase.clone()
tauSelectionHPSTauBased.src = cms.untracked.InputTag("selectedPatTausHpsPFTauTauTriggerMatched")
tauSelectionHPSTauBased.selection = cms.untracked.string("HPSTauBased")

tauSelectionCombinedHPSTaNCTauBased = tauSelectionBase.clone()
tauSelectionCombinedHPSTaNCTauBased.src = cms.untracked.InputTag("selectedPatTausHpsTancPFTauTauTriggerMatched")
tauSelectionCombinedHPSTaNCTauBased.selection = cms.untracked.string("CombinedHPSTaNCTauBased")


#tauSelection = tauSelectionShrinkingConeCutBased
#tauSelection = tauSelectionShrinkingConeTaNCBased
#tauSelection = tauSelectionCaloTauCutBased
tauSelection = tauSelectionHPSTauBased
#tauSelection = tauSelectionCombinedHPSTaNCTauBased

jetSelection = cms.untracked.PSet(
    #src = cms.untracked.InputTag("selectedPatJets"),       # Calo jets
    #src = cms.untracked.InputTag("selectedPatJetsAK5JPT"), # JPT jets 
    src = cms.untracked.InputTag("selectedPatJetsAK5PF"),  # PF jets
    src_met = cms.untracked.InputTag("patMETsPF"), # calo MET 
    cleanTauDR = cms.untracked.double(0.5), #no change
    ptCut = cms.untracked.double(30),
    etaCut = cms.untracked.double(2.4),
    minNumber = cms.untracked.uint32(3),
    METCut = cms.untracked.double(60.0)
)

MET = cms.untracked.PSet(
    # src = cms.untracked.InputTag("patMETs"), # calo MET
    src = cms.untracked.InputTag("patMETsPF"), # PF MET
    #src = cms.untracked.InputTag("patMETsTC"), # tc MET
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


# Functions
from HiggsAnalysis.HeavyChHiggsToTauNu.HChTools import addAnalysisArray
def setTauSelection(module, val):
    module.tauSelection = val
def addTauIdAnalyses(process, prefix, module, commonSequence, additionalCounters):
    addAnalysisArray(process, prefix, module, setTauSelection,
    values = [tauSelectionShrinkingConeCutBased,
              tauSelectionShrinkingConeTaNCBased,
              tauSelectionCaloTauCutBased,
              tauSelectionHPSTauBased,
              tauSelectionCombinedHPSTaNCTauBased],
    names = ["TauSelectionShrinkingConeCutBased",
             "TauSelectionShrinkingConeTaNCBased",
             "TauSelectionCaloTauCutBased",
             "TauSelectionHPSTauBased",
             "TauSelectionCombinedHPSTaNCBased"],
    preSequence = commonSequence,
    additionalCounters = additionalCounters)

