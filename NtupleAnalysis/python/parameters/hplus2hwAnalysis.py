#!/usr/bin/env python

from HiggsAnalysis.NtupleAnalysis.main import PSet
import HiggsAnalysis.NtupleAnalysis.parameters.scaleFactors as scaleFactors

##########
## General parameters
##########


##########
## Muon
##########

muonSelection = PSet(
             muonPtCut = 23.0,
            muonEtaCut = 2.1,
                muonID = "muIDMedium", # options: muIDLoose, muIDMedium, muIDTight
         muonIsolation = "tight", # for selecting, not vetoing
	muonIsolType   = "mini",      # options: "mini", "default" 
)


##########
## Tau
##########

tauSelection = PSet(
#  applyTriggerMatching = True,
#   triggerMatchingCone = 0.1,   # DeltaR for matching offline tau with trigger tau
              tauPtCut = 20.0,
             tauEtaCut = 2.1,
#        tauLdgTrkPtCut = 10.0,
#                prongs = 13,    # options: 1, 2, 3, 12, 13, 23, 123 or -1 (all)
#                prongs = 1,    # options: 1, 2, 3, 12, 13, 23, 123 or -1 (all)
#                  rtau = 0.75,   # to disable set to 0.0
#  againstElectronDiscr = "againstElectronLooseMVA6",
#  againstElectronDiscr = "",
#      againstMuonDiscr = "againstMuonLoose3",
#        isolationDiscr = "byMediumIsolationMVA3oldDMwLT",
#        isolationDiscr = "byLooseCombinedIsolationDeltaBetaCorr3Hits",
)

##########
## Common plots options
##########

commonPlotsOptions = PSet(
    histogramSplitting         = [],    # Splitting of histograms as function of one or more parameters
    enableGenuineBHistograms   = False,
    enablePUDependencyPlots    = False,  # Enable/Disable some debug-level plots
   # Bin settings (final bin setting done in datacardGenerator, there also variable bin width is supported)
    nVerticesBins     = PSet(nBins = 100, axisMin =  0.0, axisMax =  100.0),
    ptBins            = PSet(nBins =  50, axisMin =  0.0, axisMax =  500.0),
    etaBins           = PSet(nBins =  50, axisMin = -5.0, axisMax =    5.0),
    phiBins           = PSet(nBins =  64, axisMin = -3.2, axisMax =    3.2),
    deltaEtaBins      = PSet(nBins = 100, axisMin =  0.0, axisMax =   10.0),
    deltaPhiBins      = PSet(nBins =  32, axisMin =  0.0, axisMax =    3.2),
    deltaRBins        = PSet(nBins =  50, axisMin =  0.0, axisMax =   10.0),
    rtauBins          = PSet(nBins =  55, axisMin =  0.0, axisMax =    1.1), # HToTauNu
    njetsBins         = PSet(nBins =  18, axisMin =  0.0, axisMax =   18.0),
    metBins           = PSet(nBins =  80, axisMin =  0.0, axisMax =  400.0), #  5 GeV bin width
    htBins            = PSet(nBins = 500, axisMin =  0.0, axisMax = 5000.0), # 10 GeV bin width 
    bjetDiscrBins     = PSet(nBins = 120, axisMin =  0.0, axisMax =    1.2),
    angularCuts1DBins = PSet(nBins =  52, axisMin =  0.0, axisMax =  260.0), 
    topMassBins       = PSet(nBins = 300, axisMin =  0.0, axisMax = 1500.0), #  5 GeV bin width 
    wMassBins         = PSet(nBins = 200, axisMin =  0.0, axisMax = 1000.0), #  5 GeV bin width 
    mtBins            = PSet(nBins = 800, axisMin =  0.0, axisMax = 4000.0), #  5 GeV bin width
    invMassBins       = PSet(nBins = 200, axisMin =  0.0, axisMax = 4000.0), # 20 GeV bin width    
)

##########
## All selections
##########

allSelections = PSet(
    MuonSelection 	= muonSelection,
    TauSelection	= tauSelection,
    CommonPlots         = commonPlotsOptions,
)


#====== Build all selections group
#allSelections = PSet(
# histogramAmbientLevel = histoLevel,
#               Trigger = trg,
#             METFilter = metFilter,
#          TauSelection = tauSelection,
#     ElectronSelection = eVeto,
#         MuonSelection = muVeto,
#      MuonForEmbedding = muForEmbedding,
#          JetSelection = jetSelection,
#  AngularCutsCollinear = angularCutsCollinear,
#         BJetSelection = bjetSelection,
#          METSelection = metSelection,
# AngularCutsBackToBack = angularCutsBackToBack,
#       JetCorrelations = jetCorrelations,
#           CommonPlots = commonPlotsOptions,
#)
