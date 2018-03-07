#!/usr/bin/env python

from HiggsAnalysis.NtupleAnalysis.main import PSet
import HiggsAnalysis.NtupleAnalysis.parameters.scaleFactors as scaleFactors
import HiggsAnalysis.NtupleAnalysis.parameters.jsonReader as jsonReader
import HiggsAnalysis.NtupleAnalysis.parameters.signalAnalysisParameters as signalAnalysis

#================================================================================================
# General parameters
#================================================================================================
verbose               = True
histogramAmbientLevel = "Debug"  # Options: Systematics, Vital, Informative, Debug

#================================================================================================
# Trigger
#================================================================================================
trigger = signalAnalysis.trigger
trigger.triggerOR.extend("HLT_IsoMu24") 

#================================================================================================
# MET filter
#================================================================================================
metFilter = signalAnalysis.metFilter

#================================================================================================
# Electron veto
#================================================================================================
eVeto = signalAnalysis.eVeto

#================================================================================================
# Muon selection
#================================================================================================
muSelection = signalAnalysis.muVeto
muSelection.muonPtCut = 26.0  # Higher than HLT threshold    
# muSelection.muonID = "muIDMedium"

#================================================================================================
# Tau selection (sync with HToTauNu analysis)
#================================================================================================
tauSelection = signalAnalysis.tauSelection

#================================================================================================
# Jet selection
#================================================================================================
jetSelection = signalAnalysis.jetSelection
jetSelection.HTCutValue = 0.0

#================================================================================================= 
# Fat jet selection
#=================================================================================================
fatjetVeto = signalAnalysis.fatjetVeto

#================================================================================================
# B-jet selection
#================================================================================================
bjetSelection = signalAnalysis.bjetSelection
bjetSelection.jetPtCuts = [40.0, 30.0]
bjetSelection.numberOfBJetsCutValue = 2

#================================================================================================
# Scale Factors
#================================================================================================
scaleFactors.setupBtagSFInformation(btagPset               = bjetSelection,
                                    btagPayloadFilename    = "CSVv2.csv",
                                    btagEfficiencyFilename = "btageff_HToTB.json",
                                    direction              = "nominal")

#=================================================================================================
# QGL selection
#================================================================================================= 
qglrSelection = signalAnalysis.qglrSelection

jsonReader.setupQGLInformation(QGLRPset  = qglrSelection,
                               jsonname_Light  = "QGLdiscriminator_QCD_LightJets.json",
                               jsonname_Gluon  = "QGLdiscriminator_QCD_GluonJets.json")

#================================================================================================
# Topology selection
#================================================================================================
topologySelection = signalAnalysis.topologySelection

#================================================================================================
# Top selection BDT
#================================================================================================
topSelectionBDT = signalAnalysis.topSelectionBDT


#================================================================================================
# MET selection
#================================================================================================
metSelection = signalAnalysis.metSelection

#================================================================================================
# FakeB Measurement Options
#================================================================================================
fakeBBjetSelection = signalAnalysis.fakeBBjetSelection
scaleFactors.setupBtagSFInformation(btagPset               = fakeBBjetSelection,
                                    btagPayloadFilename    = "CSVv2.csv",
                                    btagEfficiencyFilename = "btageff_HToTB.json",
                                    direction              = "nominal")
fakeBMeasurement = signalAnalysis.fakeBMeasurement

#================================================================================================
# Common plots options
#================================================================================================
commonPlotsOptions = signalAnalysis.commonPlotsOptions


#================================================================================================
# Build all selections group
#================================================================================================
allSelections = PSet(
    Verbose               = verbose,
    Trigger               = trigger,
    METFilter             = metFilter,
    ElectronSelection     = eVeto,
    MuonSelection         = muVeto,
    TauSelection          = tauVeto,
    JetSelection          = jetSelection,
    BJetSelection         = bjetSelection,
    METSelection          = metSelection,
    TopSelectionBDT       = topSelectionBDT,
    FatJetSelection       = fatjetVeto,
    FakeBMeasurement      = fakeBMeasurement,
    FakeBBjetSelection    = fakeBBjetSelection,
    CommonPlots           = commonPlotsOptions,
    HistogramAmbientLevel = histogramAmbientLevel,
    QGLRSelection         = qglrSelection,
)
