#!/usr/bin/env python

from HiggsAnalysis.NtupleAnalysis.main import PSet

#====== General parameters
histoLevel = "Debug"  # Options: Systematics, Vital, Informative, Debug

#====== Trigger
trg = PSet(
  # No need to specify version numbers, they are automatically scanned in range 1--100 (remove the '_v' suffix)
  triggerOR = ["HLT_LooseIsoPFTau50_Trk30_eta2p1_MET80",
               "HLT_LooseIsoPFTau50_Trk30_eta2p1_MET80_JetIdCleaned",
               "HLT_LooseIsoPFTau50_Trk30_eta2p1_MET120",
               "HLT_LooseIsoPFTau50_Trk30_eta2p1_MET120_JetIdCleaned",
               #"HLT_LooseIsoPFTau50_Trk30_eta2p1_MET120",
               #"HLT_LooseIsoPFTau35_Trk20_Prong1_MET70",HLT_LooseIsoPFTau50_Trk30_eta2p1_MET120_v1
               ],
  triggerOR2 = [],
)

#====== MET filter
metFilter = PSet(
  # Note: HBHE filter is applied at ttree generation level
  discriminators = ["CSCTightHaloFilter",
                    "eeBadScFilter",
                    "goodVertices"]
)

#====== Tau selection
tauSelection = PSet(
  applyTriggerMatching = True,
   triggerMatchingCone = 0.1,   # DeltaR for matching offline tau with trigger tau
              tauPtCut = 51.0,
             tauEtaCut = 2.1,
        tauLdgTrkPtCut = 10.0,
                prongs = 13,    # options: 1, 3, 13 (both 1 and 3) or -1 (all)
                  rtau = 0.7,
    invertTauIsolation = False, # set to true to invert isolation (for QCD measurement)
  againstElectronDiscr = "againstElectronTightMVA5",
      againstMuonDiscr = "againstMuonTight3",
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
 
#====== Angular cuts / collinear
angularCutsCollinear = PSet(
       nConsideredJets = 3,    # Number of highest-pt jets to consider (excluding jet corresponding to tau)
enableOptimizationPlots = True, # 2D histograms for optimizing angular cuts
        cutValueJet1 = 40.0,   # Cut value in degrees (circular cut)
        cutValueJet2 = 40.0,   # Cut value in degrees (circular cut)
        cutValueJet3 = 40.0,   # Cut value in degrees (circular cut)
        cutValueJet4 = 40.0,   # Cut value in degrees (circular cut)
)
 
#====== B-jet selection
bjetSelection = PSet(
             #bjetDiscr = "combinedInclusiveSecondaryVertexV2BJetTags",
             bjetDiscr = "pfCombinedInclusiveSecondaryVertexV2BJetTags",
 bjetDiscrWorkingPoint = "Tight",
 numberOfBJetsCutValue = 1,
 numberOfBJetsCutDirection = ">=", # options: ==, !=, <, <=, >, >=
)

#====== MET selection
metSelection = PSet(
           METCutValue = 80.0,
       METCutDirection = ">", # options: ==, !=, <, <=, >, >=
               METType = "type1MET", # options: GenMET, L1MET, CaloMET, type1MET
   applyPhiCorrections = False  # FIXME: no effect yet
)

#====== Angular cuts / back-to-back
angularCutsBackToBack = PSet(
       nConsideredJets = 3,    # Number of highest-pt jets to consider (excluding jet corresponding to tau)
enableOptimizationPlots = True, # 2D histograms for optimizing angular cuts
        cutValueJet1 = 60.0,   # Cut value in degrees (circular cut)
        cutValueJet2 = 60.0,   # Cut value in degrees (circular cut)
        cutValueJet3 = 60.0,   # Cut value in degrees (circular cut)
        cutValueJet4 = 60.0,   # Cut value in degrees (circular cut)
)

#====== Common plots options
commonPlotsOptions = PSet(
  # Splitting of histograms as function of one or more parameters
  # Example: histogramSplitting = [PSet(label="tauPt", binLowEdges=[60, 70, 80, 100, 120], useAbsoluteValues=False)],
  histogramSplitting = [],
  # By default, inclusive (i.e. fake tau+genuine tau) and fake tau histograms are produced. Set to true to also produce genuine tau histograms (Note: will slow down running and enlarge resulting files).
  enableGenuineTauHistograms = False, 
  # Bin settings (final bin setting done in datacardGenerator, there also variable bin width is supported)
       nVerticesBins = PSet(nBins=100, axisMin=0., axisMax=100.),
              ptBins = PSet(nBins=50, axisMin=0., axisMax=500.),
             etaBins = PSet(nBins=60, axisMin=-3.0, axisMax=3.0),
             phiBins = PSet(nBins=72, axisMin=-3.1415926, axisMax=3.1415926),
        deltaPhiBins = PSet(nBins=18, axisMin=0., axisMax=180.), # used in 2D plots, i.e. putting high number of bins here will cause troubles
            rtauBins = PSet(nBins=55, axisMin=0., axisMax=1.1),
           njetsBins = PSet(nBins=20, axisMin=0., axisMax=20.),
             metBins = PSet(nBins=80, axisMin=0., axisMax=800.),
       bjetDiscrBins = PSet(nBins=20, axisMin=-1.0, axisMax=1.0),
   angularCuts1DBins = PSet(nBins=52, axisMin=0., axisMax=260.),
         topMassBins = PSet(nBins=60, axisMin=0., axisMax=600.),
           WMassBins = PSet(nBins=60, axisMin=0., axisMax=300.),
              mtBins = PSet(nBins=160, axisMin=0., axisMax=800.), # 5 GeV bin width for tail fitter
         invmassBins = PSet(nBins=50, axisMin=0., axisMax=500.),
)

#====== Build all selections group
allSelections = PSet(
 histogramAmbientLevel = histoLevel,
               Trigger = trg,
             METFilter = metFilter,
          TauSelection = tauSelection,
     ElectronSelection = eVeto,
         MuonSelection = muVeto,
          JetSelection = jetSelection,
  AngularCutsCollinear = angularCutsCollinear,
         BJetSelection = bjetSelection,
          METSelection = metSelection,
 AngularCutsBackToBack = angularCutsBackToBack,
           CommonPlots = commonPlotsOptions,
)