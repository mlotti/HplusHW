#!/usr/bin/env python

from HiggsAnalysis.NtupleAnalysis.main import PSet
import HiggsAnalysis.NtupleAnalysis.parameters.scaleFactors as scaleFactors

#================================================================================================
# General parameters
#================================================================================================
verbose               = True
histogramAmbientLevel = "Debug"  # Options: Systematics, Vital, Informative, Debug

#================================================================================================
# Trigger
#================================================================================================
trigger = PSet(
    triggerOR = [
        "HLT_PFHT400_SixJet30_DoubleBTagCSV_p056", # scanned in range _v1--_v100 (=>remove the '_v' suffix)
        "HLT_PFHT450_SixJet40_BTagCSV_p056",       # scanned in range _v1--_v100 (=>remove the '_v' suffix)
        #"HLT_PFHT400_SixJet30", #Prescale 110 at inst. lumi 1.35E+34
        #"HLT_PFHT450_SixJet40", #Prescale 26 at inst. lumi 1.35E+34
        ],
    triggerOR2 = [],
    )


#================================================================================================
# Tau selection (sync with HToTauNu analysis)
#================================================================================================
tauSelection = PSet(
    applyTriggerMatching = False,
    triggerMatchingCone  =   0.1, # DeltaR for matching offline tau with trigger tau
    tauPtCut             =  20.0, #
    tauEtaCut            =   2.3, #
    tauLdgTrkPtCut       =   0.0, #
    prongs               =  -1,   # options: 1, 2, 3, 12, 13, 23, 123 or -1 (all)
    rtau                 =   0.0, # to disable set to 0.0
    againstElectronDiscr = "againstElectronTightMVA6",
    againstMuonDiscr     = "againstMuonLoose3",
    isolationDiscr       = "byLooseCombinedIsolationDeltaBetaCorr3Hits",
    )

# HToTauNu (fixme: crashes if i disable ..)
if 1:
    # tau identification scale factors
    scaleFactors.assignTauIdentificationSF(tauSelection)
    # tau misidentification scale factorss
    scaleFactors.assignTauMisidentificationSF(tauSelection, "eToTau", "full", "nominal")
    scaleFactors.assignTauMisidentificationSF(tauSelection, "muToTau", "full", "nominal")
    scaleFactors.assignTauMisidentificationSF(tauSelection, "jetToTau", "full", "nominal")
    # tau trigger SF
    scaleFactors.assignTauTriggerSF(tauSelection, "nominal")

#================================================================================================
# MET filter
#================================================================================================
metFilter = PSet(
    discriminators = [
        "hbheNoiseTokenRun2Loose", # Loose is recommended
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
    muonPtCut         = 10.0,
    muonEtaCut        = 2.5,
    muonID            = "muIDLoose", # loosest option for vetoing (options: muIDLoose, muIDMedium, muIDTight)
    muonIsolation     = "veto",      # loosest possible for vetoing ("veto"), "tight" for selecting
)

#================================================================================================
# Jet selection
#================================================================================================
jetSelection = PSet(
    jetType                  = "Jets",    # options: Jets (AK4PFCHS), JetsPuppi (AK4Puppi)
    jetPtCuts                = [40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 30.0],
    jetEtaCuts               = [2.4],
    numberOfJetsCutValue     = 7,
    numberOfJetsCutDirection = ">=",      # options: ==, !=, <, <=, >, >=
    jetIDDiscr               = "IDloose", # options: IDloose, IDtight, IDtightLeptonVeto
    jetPUIDDiscr             = "",        # does not work at the moment 
    tauMatchingDeltaR        = 0.4,
    HTCutValue               = 500.0,
    HTCutDirection           = ">=",
    JTCutValue               = 0.0,
    JTCutDirection           = ">=",
    MHTCutValue              = 0.0,
    MHTCutDirection          = ">=",
)

#================================================================================================
# B-jet selection
#================================================================================================
bjetSelection = PSet(
    triggerMatchingApply      = False,
    triggerMatchingCone       = 0.1,  # DeltaR for matching offline bjet with trigger::TriggerBjet
    jetPtCuts                 = [40.0, 40.0, 30.0],
    jetEtaCuts                = [2.4],
    bjetDiscr                 = "pfCombinedInclusiveSecondaryVertexV2BJetTags",
    bjetDiscrWorkingPoint     = "Medium",
    numberOfBJetsCutValue     = 3,
    numberOfBJetsCutDirection = ">=", # options: ==, !=, <, <=, >, >=
)

scaleFactors.setupBtagSFInformation(btagPset               = bjetSelection, 
                                    btagPayloadFilename    = "CSVv2.csv",
                                    #btagEfficiencyFilename = "btageff_hybrid.json", #old
                                    btagEfficiencyFilename = "btageff_hybrid_HToTB.json",
                                    direction              = "nominal")

#================================================================================================
# Light-Jet selection
#================================================================================================
if 0:
    ljetSelection = PSet(
        jetPtCut                 = 40.0,
        jetEtaCut                = 2.4,
        numberOfJetsCutValue     = 0,
        numberOfJetsCutDirection = ">=",      # options: ==, !=, <, <=, >, >=
        bjetMatchingDeltaR       = 0.1,
        )

#================================================================================================
# MET selection
#================================================================================================
metSelection = PSet(
    METCutValue                 = -1000.0,
    METCutDirection             = ">",         # options: ==, !=, <, <=, >, >=
    METSignificanceCutValue     = -1000.0,
    METSignificanceCutDirection = ">",         # options: ==, !=, <, <=, >, >=
    METType                     = "MET_Type1", # options: MET_Type1, MET_Type1_NoHF, MET_Puppi, GenMET, L1MET, HLTMET, CaloMET
    applyPhiCorrections          = False
    )

#================================================================================================
# Topology selection
#================================================================================================
topologySelection = PSet(
    SphericityCutValue           = 100.0,   # 0.0 <= S <= 1.0
    SphericityCutDirection       = "<=",    # options: ==, !=, <, <=, >, >=
    AplanarityCutValue           = 100.0,   # 0.0 <= A <= 0.5
    AplanarityCutDirection       = "<=",  
    PlanarityCutValue            = 100.0,   # 0.0 <= P <= 0.5
    PlanarityCutDirection        = "<=",  
    CircularityCutValue          = 100.0,   # 0.0 <= C <= 0.5
    CircularityCutDirection      = "<=",  
    Y23CutValue                  = 100.0,   # 0.0 <= y23 <= 0.25
    Y23CutDirection              = "<=",  
    CparameterCutValue           = 100.0,   # 0.0 <= C <= 1.0
    CparameterCutDirection       = "<=", 
    DparameterCutValue           = 100.0,   # 0.0 <= D <= 1.0
    DparameterCutDirection       = "<=",  
    FoxWolframMomentCutValue     =   0.5,   # 0.0 <= H2 <= 1.0
    FoxWolframMomentCutDirection = "<=", 
    AlphaTCutValue               = 1000.0,  # 0.0 <= alphaT ~ 2.0 (alphaT->0.5 for perfectly balanced events)
    AlphaTCutDirection           = "<=", 
    CentralityCutValue           = 100.0,   # 0.0 <= Centrality ~ 1.0
    CentralityCutDirection       = "<=",
)


#================================================================================================
# Top selection
#================================================================================================
topSelection = PSet(
    ChiSqrCutValue     = 10.0,
    ChiSqrCutDirection =  "<",   # options: ==, !=, <, <=, >, >=
    LowLdgTrijetMassCutValue      = 150.0,
    LowLdgTrijetMassCutDirection  = ">=",
    HighLdgTrijetMassCutValue      = 210.0,
    HighLdgTrijetMassCutDirection  = "<=",
    MassW              = 80.385,
    DiJetSigma         = 10.2,
    TriJetSigma        = 27.2,
    MaxJetsToUseInFit  = 8,
    MaxBJetsToUseInFit = 3,
    # Distance cut
    dijetWithMaxDR_tetrajetBjet_dR_min          =  0.0, # Disable: 0.0, Default: +3.0
    dijetWithMaxDR_tetrajetBjet_dR_yIntercept   = -1.0, # Disable:-1.0, Default: +4.0
    dijetWithMaxDR_tetrajetBjet_dR_slopeCoeff   =  0.0, # Disable: 0.0, Default: -1.0
    # Angular cut
    dijetWithMaxDR_tetrajetBjet_dPhi_min        = +2.5, # Disable: 0.0, Default: +2.5
    dijetWithMaxDR_tetrajetBjet_dPhi_yIntercept = +3.0, # Disable:-1.0, Default: +3.0
    dijetWithMaxDR_tetrajetBjet_dPhi_slopeCoeff = -1.0, # Disable: 0.0, Default: -1.0
)


#================================================================================================
# MET trigger SF
#================================================================================================
if 0:
    scaleFactors.assignMETTriggerSF(metSelection, bjetSelection.bjetDiscrWorkingPoint, "nominal")


#================================================================================================
# FakeB Measurement Options
#================================================================================================
fakeBMeasurement = PSet(
    prelimTopFitChiSqrCutValue        = 100.0,
    prelimTopFitChiSqrCutDirection    =  "<",   # options: ==, !=, <, <=, >, >=
    numberOfBJetsCutValue             = 2,
    numberOfBJetsCutDirection         = ">=", # options: ==, !=, <, <=, >, >=
    numberOfInvertedBJetsCutValue     = 0,
    numberOfInvertedBJetsCutDirection = ">=", # options: ==, !=, <, <=, >, >=
    invertedBJetDiscr                 = bjetSelection.bjetDiscr,
    invertedBJetWorkingPoint          = "Loose",
    )


#================================================================================================
# Common plots options
#================================================================================================
commonPlotsOptions = PSet(
    histogramSplitting         = [],    # Splitting of histograms as function of one or more parameters
    enableGenuineBHistograms   = False,
    enablePUDependencyPlots    = True,  # Enable/Disable some debug-level plots
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
    topMassBins       = PSet(nBins = 300, axisMin =  0.0, axisMax = 1500.0), # 5 GeV bin width 
    wMassBins         = PSet(nBins = 200, axisMin =  0.0, axisMax = 1000.0), # 5 GeV bin width 
    mtBins            = PSet(nBins = 800, axisMin =  0.0, axisMax = 4000.0), # 5 GeV bin width
    invMassBins       = PSet(nBins = 800, axisMin =  0.0, axisMax = 4000.0), # 5 GeV bin width    
)

#================================================================================================
# Build all selections group
#================================================================================================
allSelections = PSet(
    BJetSelection         = bjetSelection,
    CommonPlots           = commonPlotsOptions,
    ElectronSelection     = eVeto,
    HistogramAmbientLevel = histogramAmbientLevel,
    JetSelection          = jetSelection,
    TauSelection          = tauSelection,
    METFilter             = metFilter,
    METSelection          = metSelection,
    TopologySelection     = topologySelection,
    TopSelection          = topSelection,
    MuonSelection         = muVeto,
    Trigger               = trigger,
    Verbose               = verbose,
    FakeBMeasurement      = fakeBMeasurement,
)

