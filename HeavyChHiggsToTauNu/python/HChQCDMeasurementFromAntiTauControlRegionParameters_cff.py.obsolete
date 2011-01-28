import FWCore.ParameterSet.Config as cms

# WARNING: the trigger path is modified in qcdMeasurementByIsolationVeto_cfg.py depending on the data version
trigger = cms.untracked.PSet(
    src = cms.untracked.InputTag("patTriggerEvent"),
    triggers = cms.untracked.vstring("HLT_Jet30U"
                                     ),
    #hltMetCut = cms.untracked.double(20.0),
    hltMetCut = cms.untracked.double(-10.0),
    )
# Required for QCD measurement to remove bias from the fact that signal trigger contains MET cut but Jet30U doesn't.
TriggerMETEmulation = cms.untracked.PSet(
    src = cms.untracked.InputTag("patMETs"), # calo MET
    #metEmulationCut = cms.untracked.double(30.0)
    metEmulationCut = cms.untracked.double(-10.0)
)

#import HiggsAnalysis.HeavyChHiggsToTauNu.HChTauIDFactorization_cfi as factorizationParams

### Define tau selection
tauSelectionBase = cms.untracked.PSet(
    src = cms.untracked.InputTag("myTauCollection"),
    selection = cms.untracked.string(""),
    ptCut = cms.untracked.double(30),
    etaCut = cms.untracked.double(2.4),
    leadingTrackPtCut = cms.untracked.double(20), #To fully disable this remove requirement to ldgTrkExist from TauSelectionByIsolationVeto.cc
)
### Reco CaloTau
tauSelectionCaloTauCutBased = tauSelectionBase.clone()
tauSelectionCaloTauCutBased.src = cms.untracked.InputTag("selectedPatTausCaloRecoTau")
#tauSelectionCaloTauCutBased.src = cms.untracked.InputTag("selectedPatTausCaloRecoTauTauTriggerMatched")
tauSelectionCaloTauCutBased.selection = cms.untracked.string("CaloTauCutBased")
### PF Shrinking Cone
tauSelectionShrinkingConeCutBased = tauSelectionBase.clone()
tauSelectionShrinkingConeCutBased.src = cms.untracked.InputTag("selectedPatTausShrinkingConePFTau")
#tauSelectionShrinkingConeCutBased.src = cms.untracked.InputTag("selectedPatTausShrinkingConePFTauTauTriggerMatched")
tauSelectionShrinkingConeCutBased.selection = cms.untracked.string("ShrinkingConePFTauCutBased")
### TaNC
tauSelectionShrinkingConeTaNCBased = tauSelectionBase.clone()
tauSelectionShrinkingConeTaNCBased.src = cms.untracked.InputTag("selectedPatTausShrinkingConePFTau")
#tauSelectionShrinkingConeTaNCBased.src = cms.untracked.InputTag("selectedPatTausShrinkingConePFTauTauTriggerMatched")
tauSelectionShrinkingConeTaNCBased.selection = cms.untracked.string("ShrinkingConePFTauTaNCBased")
### HPS
tauSelectionHPSTauBased = tauSelectionBase.clone()
tauSelectionHPSTauBased.src = cms.untracked.InputTag("selectedPatTausHpsPFTau")
#tauSelectionHPSTauBased.src = cms.untracked.InputTag("selectedPatTausHpsPFTauTauTriggerMatched")
tauSelectionHPSTauBased.selection = cms.untracked.string("HPSTauBased")

### Select tau-collection to be used
### tauSelection = tauSelectionCaloTauCutBased
### tauSelection = tauSelectionShrinkingConeCutBased
### tauSelection = tauSelectionShrinkingConeTaNCBased
tauSelection = tauSelectionHPSTauBased # only this will be used for QCD measurement (no time for rest)
print "tauSelection.src :", tauSelection.src

### Define jet selection
jetSelection = cms.untracked.PSet(
    #src = cms.untracked.InputTag("selectedPatJets"),       # Calo jets
    #src = cms.untracked.InputTag("selectedPatJetsAK5JPT"), # JPT jets 
    src = cms.untracked.InputTag("selectedPatJetsAK5PF"),  # PF jets
    src_met = cms.untracked.InputTag("patMETsPF"), # pf MET
    cleanTauDR = cms.untracked.double(0.5),
    ptCut = cms.untracked.double(30),
    etaCut = cms.untracked.double(2.4),
    #minNumber = cms.untracked.uint32(3), #original
    minNumber = cms.untracked.uint32(2), #original
    METCut = cms.untracked.double(70.0) # Only used for deltaPhi histogram plotting
)
print "jetSelection.src :", jetSelection.src

### Definre the rest of the event selection: MET, B-tagging, Global e/mu vetoes, fakeMET veto, 
MET = cms.untracked.PSet(
    # src = cms.untracked.InputTag("patMETs"), # calo MET
    # src = cms.untracked.InputTag("patMETsTC"), # tc MET
    src = cms.untracked.InputTag("patMETsPF"), # PF MET
    #METCut = cms.untracked.double(70.0), #original
    METCut = cms.untracked.double(70.0),
    # Direction of MET cut; options are: lowerLimit (i.e. > ) and upperLimit (i.e. < )
    METCutDirection = cms.untracked.string("lowerLimit")
)
print "MET.src :", MET.src

bTagging = cms.untracked.PSet(
    discriminator = cms.untracked.string("trackCountingHighEffBJetTags"),
    discriminatorCut = cms.untracked.double(2.0),
    ptCut = cms.untracked.double(30),
    etaCut = cms.untracked.double(2.4),
    minNumber = cms.untracked.uint32(1)
)
print "bTagging.discriminator :", bTagging.discriminator

GlobalElectronVeto = cms.untracked.PSet(
    ElectronCollectionName = cms.untracked.InputTag("selectedPatElectrons"),
    ElectronSelection = cms.untracked.string("simpleEleId95relIso"),
    ElectronPtCut = cms.untracked.double(20.0),
    ElectronEtaCut = cms.untracked.double(2.5)
)
print "GlobalElectronVeto.ElectronSelection :", GlobalElectronVeto.ElectronSelection

GlobalMuonVeto = cms.untracked.PSet(
    MuonCollectionName = cms.untracked.InputTag("selectedPatMuons"),
    MuonSelection = cms.untracked.string("GlobalMuonPromptTight"),
    MuonPtCut = cms.untracked.double(20.0),
    MuonEtaCut = cms.untracked.double(2.5)
)
print "GlobalMuonVeto.MuonSelection :", GlobalMuonVeto.MuonSelection

fakeMETVeto = cms.untracked.PSet(
  src = MET.src,
  minDeltaPhi = cms.untracked.double(10.0)
)
print "fakeMETVeto.src :", fakeMETVeto.src

