#!/usr/bin/env python

from HiggsAnalysis.NtupleAnalysis.main import PSet

#====== General parameters
histoLevel = "Debug"  # Options: Systematics, Vital, Informative, Debug

#====== Trigger
trg = PSet(
  # No need to specify version numbers, they are automatically scanned in range 1--100
  triggerOR = ["HLT_LooseIsoPFTau50_Trk30_eta2p1_MET120",
               "HLT_LooseIsoPFTau35_Trk20_Prong1_MET70"],
  triggerOR2 = [],
)

#====== Tau selection
tauSelection = PSet(
  applyTriggerMatching = True,
   triggerMatchingCone = 0.1,   # DeltaR for matching offline tau with trigger tau
              tauPtCut = 41.0,
             tauEtaCut = 2.1,
        tauLdgTrkPtCut = 10.0,
                prongs = 13,    # options: 1, 3, 13 (both 1 and 3) or -1 (all)
                  rtau = 0.7,
    invertTauIsolation = False, # set to true to invert isolation (for QCD measurement)
  againstElectronDiscr = "againstElectronTight",
      againstMuonDiscr = "againstMuonMedium",
        isolationDiscr = "byLooseCombinedIsolationDeltaBetaCorr3Hits",
)

#====== Electron veto
eVeto = PSet(
         electronPtCut = 15.0,
        electronEtaCut = 2.5,
        # FIXME: add electron ID and isolation
)

#====== Muon veto
muVeto = PSet(
             muonPtCut = 10.0,
            muonEtaCut = 2.5,
        # FIXME: add muon ID and isolation
)

#====== Jet selection
jetSelection = PSet(
              jetPtCut = 30.0,
             jetEtaCut = 2.5,
     tauMatchingDeltaR = 0.5,
  numberOfJetsCutValue = 3,
  numberOfJetsCutDirection = ">=", # options: ==, !=, <, <=, >, >=
            jetIDDiscr = "",       # FIXME: does not work -> ttree content
           jetPUIDDiscr = "PUIDloose",
)
            
#====== B-jet selection
bjetSelection = PSet(
             bjetDiscr = "combinedInclusiveSecondaryVertexV2BJetTags",
 bjetDiscrWorkingPoint = "Tight",
 numberOfBJetsCutValue = 3,
 numberOfBJetsCutDirection = ">=", # options: ==, !=, <, <=, >, >=
)

#allSelections = (TauSelection=TauSelection,
                 #ElectronSelection,
                 #MuonSelection,
                 #JetSelection,
                 #BJetSelection]

allSelections = PSet(
 histogramAmbientLevel = histoLevel,
               Trigger = trg,
          TauSelection = tauSelection,
     ElectronSelection = eVeto,
         MuonSelection = muVeto,
          JetSelection = jetSelection,
         BJetSelection = bjetSelection,
)