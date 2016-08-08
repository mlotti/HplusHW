#!/usr/bin/env python

from HiggsAnalysis.NtupleAnalysis.main import PSet
import HiggsAnalysis.NtupleAnalysis.parameters.scaleFactors as scaleFactors

#================================================================================================
# General parameters
#================================================================================================
verbose               = False
histogramAmbientLevel = "Vital"  # Options: Systematics, Vital, Informative, Debug


#================================================================================================
# Trigger
#================================================================================================
trigger = PSet(
  # No need to specify version numbers, they are automatically scanned in range 1--100 (remove the '_v' suffix)
    triggerOR = [
        "HLT_QuadJet45_DoubleBTagCSV_p087_v",
        "HLT_QuadPFJet_VBF_v",
        "HLT_PFHT300_v",
        "HLT_PFHT400_v",
        "HLT_PFHT475_v",
        "HLT_PFHT600_v",
        "HLT_PFHT650_v",
        "HLT_PFHT400_SixJet30_DoubleBTagCSV_p056_v",
        "HLT_PFHT450_SixJet40_BTagCSV_p056_v",
        "HLT_PFHT400_SixJet30_v",
        "HLT_PFHT450_SixJet40_v",
        "HLT_HT200_v",
        "HLT_HT275_v",
        "HLT_HT325_v",
        "HLT_HT425_v",
        "HLT_HT575_v",
        "HLT_HT650_v",
        "HLT_QuadPFJet_BTagCSV_p016_p11_VBF_Mqq200_v",
        "HLT_QuadPFJet_BTagCSV_p016_VBF_Mqq460_v",
        "HLT_QuadPFJet_BTagCSV_p016_p11_VBF_Mqq240_v",
        "HLT_QuadPFJet_BTagCSV_p016_VBF_Mqq500_v",
        "HLT_QuadPFJet_VBF_v",
    ],
  triggerOR2 = [],
)

#================================================================================================
# MET filter
#================================================================================================
metFilter = PSet(
    discriminators = ["hbheNoiseTokenRun2Loose", # Loose is recommended
                      "Flag_HBHENoiseIsoFilter",
                      "Flag_EcalDeadCellTriggerPrimitiveFilter",
                      "Flag_CSCTightHaloFilter",
                      "Flag_eeBadScFilter",
                      "Flag_goodVertices"]
)

#================================================================================================
# Electron veto
#================================================================================================
eVeto = PSet(
    electronPtCut     = 15.0,
    electronEtaCut    = 2.5,
    electronID        = "cutBasedElectronID_Spring15_25ns_V1_standalone_veto",
    electronIsolation = "veto", # loosest possible for vetoing ("veto"), "tight" for selecting
)

#================================================================================================
# Muon veto
#================================================================================================
muVeto = PSet(
    muonPtCut     = 10.0,
    muonEtaCut    = 2.5,
    muonID        = "muIDLoose", # loosest option for vetoing (options: muIDLoose, muIDMedium, muIDTight)
    muonIsolation = "veto",      # loosest possible for vetoing ("veto"), "tight" for selecting
)

#================================================================================================
# Jet selection
#================================================================================================
jetSelection = PSet(
    jetType                  = "Jets", # options: Jets (AK4PFCHS), JetsPuppi (AK4Puppi)
    jetPtCut                 = 30.0,
    jetEtaCut                = 4.7,
    tauMatchingDeltaR        = 0.4,
    numberOfJetsCutValue     = 3,
    numberOfJetsCutDirection = ">=", # options: ==, !=, <, <=, >, >=
    jetIDDiscr               = "IDloose", # options: IDloose, IDtight, IDtightLeptonVeto
    jetPUIDDiscr             = "", # does not work at the moment 
)

#================================================================================================
# B-jet selection
#================================================================================================
bjetSelection = PSet(
    jetPtCut                  = 30.0,
    jetEtaCut                 = 2.5,
    bjetDiscr                 = "pfCombinedInclusiveSecondaryVertexV2BJetTags",
    bjetDiscrWorkingPoint     = "Loose",
    numberOfBJetsCutValue     = 1,
    numberOfBJetsCutDirection = ">=", # options: ==, !=, <, <=, >, >=
)
scaleFactors.setupBtagSFInformation(btagPset               = bjetSelection, 
                                    btagPayloadFilename    = "CSVv2.csv",
                                    btagEfficiencyFilename = "btageff_hybrid.json",
                                    direction              = "nominal")

#================================================================================================
# MET selection
#================================================================================================
metSelection = PSet(
    METCutValue                 = 100.0,
    METCutDirection             = ">", # options: ==, !=, <, <=, >, >=
    METSignificanceCutValue     = -1000.0,
    METSignificanceCutDirection = ">", # options: ==, !=, <, <=, >, >=
    METType                     = "MET_Type1", # options: MET_Type1, MET_Type1_NoHF, MET_Puppi, GenMET, L1MET, HLTMET, CaloMET
    applyPhiCorrections          = False
)

#================================================================================================
# MET trigger SF
#================================================================================================
scaleFactors.assignMETTriggerSF(metSelection, bjetSelection.bjetDiscrWorkingPoint, "nominal")


#================================================================================================
# Common plots options
#================================================================================================
commonPlotsOptions = PSet(
    # Splitting of histograms as function of one or more parameters
    # Example: histogramSplitting = [PSet(label="tauPt", binLowEdges=[60, 70, 80, 100, 120], useAbsoluteValues=False)],
    histogramSplitting = [],
    # By default, inclusive (i.e. fake tau+genuine tau) and fake tau histograms are produced. Set to true to also produce genuine tau histograms
    enableGenuineTauHistograms = False, 
    # Bin settings (final bin setting done in datacardGenerator, there also variable bin width is supported)
    nVerticesBins     = PSet(nBins = 60, axisMin =  0.0, axisMax=  60.0),
    ptBins            = PSet(nBins = 50, axisMin =  0.0, axisMax= 500.0),
    etaBins           = PSet(nBins = 60, axisMin = -3.0, axisMax=   3.0),
    phiBins           = PSet(nBins = 72, axisMin = -3.1415926, axisMax=3.1415926),
    deltaPhiBins      = PSet(nBins = 18, axisMin =  0.0, axisMax = 180.0), # used in 2D plots, i.e. putting high number of bins here will cause troubles
    rtauBins          = PSet(nBins = 55, axisMin =  0.0, axisMax =   1.1),
    njetsBins         = PSet(nBins = 20, axisMin =  0.0, axisMax =  20.0),
    metBins           = PSet(nBins = 80, axisMin =  0.0, axisMax = 800.0), # please use 10 GeV bin width because of QCD measurement
    bjetDiscrBins     = PSet(nBins = 20, axisMin = -1.0, axisMax =   1.0),
    angularCuts1DBins = PSet(nBins = 52, axisMin =  0.0, axisMax = 260.0),
    topMassBins       = PSet(nBins = 60, axisMin =  0.0, axisMax = 600.0),
    WMassBins         = PSet(nBins = 60, axisMin =  0.0, axisMax = 300.0),
    mtBins            = PSet(nBins =160, axisMin =  0.0, axisMax = 800.0), # 5 GeV bin width for tail fitter
    invmassBins       = PSet(nBins = 50, axisMin =  0.0, axisMax = 500.0),    
    enablePUDependencyPlots = True, # Enable/Disable some debug-level plots
)

#================================================================================================
# Build all selections group
#================================================================================================
allSelections = PSet(
    BJetSelection         = bjetSelection,
    CommonPlots           = commonPlotsOptions,
    ElectronSelection     = eVeto,
    JetSelection          = jetSelection,
    METFilter             = metFilter,
    METSelection          = metSelection,
    MuonSelection         = muVeto,
    Trigger               = trigger,
    HistogramAmbientLevel = histogramAmbientLevel,
    Verbose               = verbose,
)

