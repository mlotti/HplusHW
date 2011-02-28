import FWCore.ParameterSet.Config as cms

# WARNING: the trigger path is modified in signalAnalysis_cfg.py depending on
# the data version
trigger = cms.untracked.PSet(
    src = cms.untracked.InputTag("patTriggerEvent"),
    triggers = cms.untracked.vstring("HLT_SingleLooseIsoTau20",
                                     "HLT_SingleLooseIsoTau20_Trk5",
                                     "HLT_SingleIsoTau20_Trk5",
                                     "HLT_SingleIsoTau20_Trk15_MET20",
                                     "HLT_SingleIsoTau20_Trk15_MET25_v3",
                                     "HLT_SingleIsoTau20_Trk15_MET25_v4"
    ),
    hltMetCut = cms.untracked.double(45.0),
)
from HiggsAnalysis.HeavyChHiggsToTauNu.TriggerEmulationEfficiency_cfi import *

primaryVertexSelection = cms.untracked.PSet(
    src = cms.untracked.InputTag("selectedPrimaryVertex"),
    enabled = cms.untracked.bool(True)
)

# Tau ID factorization map
import HiggsAnalysis.HeavyChHiggsToTauNu.HChTauIDFactorization_cfi as factorizationParams

# Default tau selection
tauSelectionBase = cms.untracked.PSet(
    # Operating mode options: 'standard', 'factorized', 'antitautag', 'antiisolatedtau'
    operatingMode = cms.untracked.string("standard"), # Standard tau ID (Tau candidate selection + tau ID applied)
#    operatingMode = cms.untracked.string("factorized"), # Tau candidate selection applied, tau ID factorized
#    operatingMode = cms.untracked.string("antitautag"), # Tau candidate selection applied, required prong cut, anti-isolation, and anti-rtau
#    operatingMode = cms.untracked.string("antiisolatedtau"), # Tau candidate selection applied, required prong cut and anti-isolation
    src = cms.untracked.InputTag("selectedPatTausShrinkingConePFTauTauTriggerMatched"),
    selection = cms.untracked.string(""),
    ptCut = cms.untracked.double(30), # jet pt > value
    etaCut = cms.untracked.double(2.3), # jet |eta| < value
    leadingTrackPtCut = cms.untracked.double(20), # ldg. track > value
    rtauCut = cms.untracked.double(0.8), # rtau > value
    antiRtauCut = cms.untracked.double(0.4), # rtau < value
    invMassCut = cms.untracked.double(999.), # m(vis.tau) < value; FIXME has no effect in TauSelection.cc 
    nprongs = cms.untracked.uint32(1), # not used at the moment FIXME: has no effect in TauSelection.cc
    factorization = factorizationParams.tauIDFactorizationParameters
)

tauSelectionCaloTauCutBased = tauSelectionBase.clone(
    src = "selectedPatTausCaloRecoTauTauTriggerMatched",
    selection = "CaloTauCutBased"
)

tauSelectionShrinkingConeCutBased = tauSelectionBase.clone(
    src = "selectedPatTausShrinkingConePFTauTauTriggerMatched",
    selection = "ShrinkingConePFTauCutBased"
)

tauSelectionShrinkingConeTaNCBased = tauSelectionBase.clone(
    src = "selectedPatTausShrinkingConePFTauTauTriggerMatched",
    selection = "ShrinkingConePFTauTaNCBased"
)

tauSelectionHPSTauBased = tauSelectionBase.clone(
    src = "selectedPatTausHpsPFTauTauTriggerMatched",
    selection = "HPSTauBased"
)

tauSelectionHPSMediumTauBased = tauSelectionBase.clone(
    src = "selectedPatTausHpsPFTauTauTriggerMatched",
    selection = "HPSMediumTauBased"
)

tauSelectionCombinedHPSTaNCTauBased = tauSelectionBase.clone(
    src = "selectedPatTausHpsTancPFTauTauTriggerMatched",
    selection = "CombinedHPSTaNCTauBased"
)


tauSelections = [tauSelectionCaloTauCutBased,
                 tauSelectionShrinkingConeCutBased,
                 tauSelectionShrinkingConeTaNCBased,
                 tauSelectionHPSTauBased,
                 tauSelectionHPSMediumTauBased,
                 tauSelectionCombinedHPSTaNCTauBased]
tauSelectionNames = ["TauSelectionCaloTauCutBased",
                     "TauSelectionShrinkingConeCutBased",
                     "TauSelectionShrinkingConeTaNCBased",
                     "TauSelectionHPSTightTauBased",
                     "TauSelectionHPSMediumTauBased",
                     "TauSelectionCombinedHPSTaNCBased"]

#tauSelection = tauSelectionShrinkingConeCutBased
#tauSelection = tauSelectionShrinkingConeTaNCBased
#tauSelection = tauSelectionCaloTauCutBased
tauSelection = tauSelectionHPSTauBased
#tauSelection = tauSelectionHPSMediumTauBased
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
    MuonEtaCut = cms.untracked.double(2.5),
    MuonApplyIpz = cms.untracked.bool(False) # Apply IP-z cut
)

InvMassVetoOnJets = cms.untracked.PSet(
    ptCut = cms.untracked.double(30),
    etaCut = cms.untracked.double(2.4),
    #setTrueToUseModule = cms.untracked.bool(False)
    setTrueToUseModule = cms.untracked.bool(True)
)

fakeMETVeto = cms.untracked.PSet(
  src = MET.src,
  minDeltaPhi = cms.untracked.double(5.) # in degrees
)

forwardJetVeto = cms.untracked.PSet(
  src = cms.untracked.InputTag("selectedPatJetsAK5PF"),  # PF jets
  src_met = MET.src,
  ptCut = cms.untracked.double(30),
  etaCut = cms.untracked.double(2.4),
  ForwJetEtCut = cms.untracked.double(10.0),
  ForwJetEtaCut = cms.untracked.double(2.5),
  EtSumRatioCut = cms.untracked.double(0.2)
 )


# Functions
def overrideTriggerFromOptions(options):
    if options.trigger != "":
        trigger.triggers = [options.trigger]

def forEachTauSelection(function):
    for selection in tauSelections:
        function(selection)

def setAllTauSelectionOperatingMode(mode):
    forEachTauSelection(lambda x: x.operatingMode.setValue(mode))

def setAllTauSelectionSrcSelectedPatTaus():
    tauSelectionCaloTauCutBased.src         = "selectedPatTausCaloRecoTau"
    tauSelectionShrinkingConeTaNCBased.src  = "selectedPatTausShrinkingConePFTau"
    tauSelectionShrinkingConeCutBased.src   = "selectedPatTausShrinkingConePFTau"
    tauSelectionHPSTauBased.src             = "selectedPatTausHpsPFTau"
    tauSelectionHPSMediumTauBased.src       = "selectedPatTausHpsPFTau"
    tauSelectionCombinedHPSTaNCTauBased.src = "selectedPatTausHpsTancPFTau"

def setAllTauSelectionSrcSelectedPatTausTriggerMatched():
    tauSelectionCaloTauCutBased.src         = "selectedPatTausCaloRecoTauTauTriggerMatched"
    tauSelectionShrinkingConeTaNCBased.src  = "selectedPatTausShrinkingConePFTauTauTriggerMatched"
    tauSelectionShrinkingConeCutBased.src   = "selectedPatTausShrinkingConePFTauTauTriggerMatched"
    tauSelectionHPSTauBased.src             = "selectedPatTausHpsPFTauTauTriggerMatched"
    tauSelectionHPSMediumTauBased.src       = "selectedPatTausHpsPFTauTauTriggerMatched"
    tauSelectionCombinedHPSTaNCTauBased.src = "selectedPatTausHpsTancPFTauTauTriggerMatched"
    
def setTauIDFactorizationMap(options):
    from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getTauIDFactorizationMap
    myFactorizationFilename = getTauIDFactorizationMap(options)
    tauIDCoefficients = __import__(myFactorizationFilename, fromlist=['dummy'])
    tauSelectionCaloTauCutBased.factorization.factorizationTables = tauIDCoefficients.tauIDFactorizationCoefficients
    tauSelectionShrinkingConeTaNCBased.factorization.factorizationTables = tauIDCoefficients.tauIDFactorizationCoefficients
    tauSelectionShrinkingConeCutBased.factorization.factorizationTables = tauIDCoefficients.tauIDFactorizationCoefficients
    tauSelectionHPSTauBased.factorization.factorizationTables = tauIDCoefficients.tauIDFactorizationCoefficients
    tauSelectionCombinedHPSTaNCTauBased.factorization.factorizationTables = tauIDCoefficients.tauIDFactorizationCoefficients

from HiggsAnalysis.HeavyChHiggsToTauNu.HChTools import addAnalysisArray
def setTauSelection(module, val):
    module.tauSelection = val
def addTauIdAnalyses(process, prefix, module, commonSequence, additionalCounters):
    addAnalysisArray(process, prefix, module, setTauSelection,
                     values = tauSelections, names = tauSelectionNames,
                     preSequence = commonSequence,
                     additionalCounters = additionalCounters)

