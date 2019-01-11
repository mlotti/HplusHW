#!/usr/bin/env python

from HiggsAnalysis.NtupleAnalysis.main import PSet
import HiggsAnalysis.NtupleAnalysis.parameters.scaleFactors as scaleFactors

##########
## General parameters
##########

##########
## Trigger
##########

trg = PSet(
  # No need to specify version numbers, they are automatically scanned in range 1--100 (remove the '_v' suffix)
#  TautriggerEfficiencyJsonName = "tauLegTriggerEfficiency_2016_fit.json",
#  METtriggerEfficiencyJsonName = "metLegTriggerEfficiency_2016_MET90_fit.json",
#  L1ETM = 80,
  triggerOR = ["HLT_IsoMu24","HLT_IsoTkMu24"
               ],
  triggerOR2 = [
                ],
)


##########
## MET filter
##########

metFilter = PSet(
  discriminators = [#"hbheNoiseTokenRun2Loose", # Loose is recommended
#                    "hbheIsoNoiseToken", # under scrutiny
                    "Flag_HBHENoiseFilter",
                    "Flag_HBHENoiseIsoFilter",
                    "Flag_EcalDeadCellTriggerPrimitiveFilter",
#                    "Flag_CSCTightHaloFilter",
                    "Flag_eeBadScFilter",
                    "Flag_goodVertices",
                    "Flag_globalTightHalo2016Filter",
                    "badPFMuonFilter",
                    "badChargedCandidateFilter"]
)

##########
## Electron veto
##########

eVeto = PSet(
    electronPtCut = 15.0,
    electronEtaCut = 2.1,
#            electronID = "mvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp90", # highest (wp90) for vetoing (2012: wp95)
    electronID = "cutBasedElectronID_Spring15_25ns_V1_standalone_veto",
    electronIDType    = "MVA",  # options: "default", "MVA"
    electronMVA       = "ElectronMVAEstimatorRun2Spring16GeneralPurposeV1Values",
    electronMVACut    = "Loose",
    electronIsolation = "veto", # loosest possible for vetoing ("veto"), "tight" for selecting
    electronIsolType  = "mini", # options: "mini", "default"
)

##########
## Muon
##########

muonSelection = PSet(
  applyTriggerMatching = True,
   triggerMatchingCone = 0.1,   # DeltaR for matching offline tau with trigger tau
             muonPtCut = 26, #26.0,
            muonEtaCut = 2.4,
                muonID = "muIDTight", # options: muIDLoose, muIDMedium, muIDTight
         muonIsolation = "tight", #"tight", # for selecting, not vetoing
	muonIsolType   = "mini",      # options: "mini", "default" 
)


##########
## Tau
##########

tauSelection = PSet(
  applyTriggerMatching = False,
   triggerMatchingCone = 0.1,   # DeltaR for matching offline tau with trigger tau
              tauPtCut = 24.0,
             tauEtaCut = 2.1,
        tauLdgTrkPtCut = 10.0,
                prongs = 1,    # options: 1, 2, 3, 12, 13, 23, 123 or -1 (all)
                  rtau = 0.0,   # to disable set to 0.0
  againstElectronDiscr = "againstElectronLooseMVA6",
      againstMuonDiscr = "againstMuonLoose3",
        isolationDiscr = "byLooseCombinedIsolationDeltaBetaCorr3Hits", #"byMediumIsolationMVArun2v1DBnewDMwLT",
)

##########
## tau identification scale factors
##########

scaleFactors.assignTauIdentificationSF(tauSelection)

##########
## tau misidentification scale factor
##########

scaleFactors.assignTauMisidentificationSF(tauSelection, "eToTau", "full", "nominal")
scaleFactors.assignTauMisidentificationSF(tauSelection, "muToTau", "full", "nominal")
scaleFactors.assignTauMisidentificationSF(tauSelection, "jetToTau", "full", "nominal")


##########
## Jet selection
##########

jetSelection = PSet(
               jetType  = "Jets", # options: Jets (AK4PFCHS), JetsPuppi (AK4Puppi)
              jetPtCuts = [25.0],
             jetEtaCuts = [2.1],
     tauMatchingDeltaR  = 0.4,
  numberOfJetsCutValue  = 2,
  numberOfJetsCutDirection = ">=", # options: ==, !=, <, <=, >, >=
            jetIDDiscr = "IDloose", # options: IDloose, IDtight, IDtightLeptonVeto
          jetPUIDDiscr = "", # does not work at the moment 
            HTCutValue = 0.0,
    HTCutDirection     = ">=",
            JTCutValue = 0.0,
    JTCutDirection     = ">=",
           MHTCutValue = 0.0,
    MHTCutDirection    = ">=",
)

##########
## b-jet selection
##########

bjetSelection = PSet(
    triggerMatchingApply= False,
    triggerMatchingCone = 0.0,  # DeltaR for matching offline bjet with trigger::TriggerBjet 
              jetPtCuts = [30.0],
             jetEtaCuts = [2.1],
             bjetDiscr  = "pfCombinedInclusiveSecondaryVertexV2BJetTags", # default
#             bjetDiscr  = "pfCombinedMVAV2BJetTags", # use this for MVA b-tagging
 bjetDiscrWorkingPoint  = "Medium", #optimal for CSVv2
# bjetDiscrWorkingPoint  = "Tight", #optimal for CMVAv2
 numberOfBJetsCutValue  = 1,
 numberOfBJetsCutDirection = ">=", # options: ==, !=, <, <=, >, >=
)

scaleFactors.setupBtagSFInformation(btagPset=bjetSelection,
                                    btagPayloadFilename="CSVv2.csv",
                                    #btagPayloadFilename="cMVAv2_Moriond17_B_H.csv", # use this for MVA b-tagging
                                    #btagEfficiencyFilename="btageff_TTJets.json",
                                    #btagEfficiencyFilename="btageff_WJetsHT.json",
                                    #btagEfficiencyFilename="btageff_hybrid.json",
                                    #btagEfficiencyFilename="btageff_hybrid_HToTB.json",
                                    btagEfficiencyFilename="btageff_Hybrid_TT+WJetsHT.json", # use with taunu analysis and WJetsHT samples
                                    direction="nominal"
)


##########
## MET selection
##########

metSelection = PSet(
           METCutValue = 30.0,
       METCutDirection = ">", # options: ==, !=, <, <=, >, >=
  METSignificanceCutValue = -1000.0,
  METSignificanceCutDirection = ">", # options: ==, !=, <, <=, >, >=
               METType = "MET_Type1", # options: MET_Type1, MET_Type1_NoHF, MET_Puppi, GenMET, L1MET, HLTMET, CaloMET
   applyPhiCorrections = False  # FIXME: no effect yet
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
    Trigger             = trg,
    METFilter 		= metFilter,
    ElectronSelection 	= eVeto,
    MuonSelection 	= muonSelection,
    TauSelection	= tauSelection,
    JetSelection	= jetSelection,
    BJetSelection 	= bjetSelection,
    METSelection        = metSelection,
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
