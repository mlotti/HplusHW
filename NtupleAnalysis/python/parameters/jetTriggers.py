#!/usr/bin/env python

from HiggsAnalysis.NtupleAnalysis.main import PSet
import HiggsAnalysis.NtupleAnalysis.parameters.scaleFactors as scaleFactors
import HiggsAnalysis.NtupleAnalysis.parameters.jsonReader as jsonReader
import HiggsAnalysis.NtupleAnalysis.parameters.hplus2tbAnalysis as hplus2tbAnalysis

#================================================================================================
# General parameters
#================================================================================================
verbose               = True
histogramAmbientLevel = "Debug"  # Options: Systematics, Vital, Informative, Debug

#================================================================================================
# Trigger
#================================================================================================
trigger = hplus2tbAnalysis.allSelections.Trigger
trigger.triggerOR.append("HLT_IsoMu24") 

#================================================================================================
# MET filter
#================================================================================================
metFilter = hplus2tbAnalysis.metFilter

#================================================================================================
# Electron veto
#================================================================================================
eVeto = hplus2tbAnalysis.eVeto

#================================================================================================
# Muon selection
#================================================================================================
muSelection = hplus2tbAnalysis.muVeto
muSelection.muonPtCut = 26.0  # Higher than HLT threshold    

#================================================================================================
# Tau selection (sync with HToTauNu analysis)
#================================================================================================
tauVeto = hplus2tbAnalysis.tauVeto

#================================================================================================
# Jet selection
#================================================================================================
jetSelection = hplus2tbAnalysis.jetSelection
jetSelection.HTCutValue = 0.0

#================================================================================================= 
# Fat jet selection
#=================================================================================================
fatjetVeto = hplus2tbAnalysis.fatjetVeto

#================================================================================================
# B-jet selection
#================================================================================================
bjetSelection = hplus2tbAnalysis.bjetSelection
bjetSelection.jetPtCuts = [40.0]
bjetSelection.numberOfBJetsCutValue = 1

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
qglrSelection = hplus2tbAnalysis.qglrSelection

jsonReader.setupQGLInformation(QGLRPset  = qglrSelection,
                               jsonname_Light  = "QGLdiscriminator_QCD_LightJets.json",
                               jsonname_Gluon  = "QGLdiscriminator_QCD_GluonJets.json")

#================================================================================================
# Topology selection
#================================================================================================
#topologySelection = hplus2tbAnalysis.topologySelection

#================================================================================================
# Top selection BDT
#================================================================================================
topSelectionBDT = hplus2tbAnalysis.topSelectionBDT


#================================================================================================
# MET selection
#================================================================================================
metSelection = hplus2tbAnalysis.metSelection

#================================================================================================
# FakeB Measurement Options
#================================================================================================
fakeBBjetSelection = hplus2tbAnalysis.fakeBBjetSelection
scaleFactors.setupBtagSFInformation(btagPset               = fakeBBjetSelection,
                                    btagPayloadFilename    = "CSVv2.csv",
                                    btagEfficiencyFilename = "btageff_HToTB.json",
                                    direction              = "nominal")

fakeBTopSelectionBDT = hplus2tbAnalysis.fakeBTopSelectionBDT

fakeBMeasurement = hplus2tbAnalysis.fakeBMeasurement

systTopBDTSelection = PSet(
    MiniIsoCutValue          = "0.2",
    MiniIsoCutDirection      = "<=",
    MiniIsoInvCutValue       = "0.2",
    MiniIsoInvCutDirection   = ">",
    METCutValue              = "50",
    METCutDirection          = ">=",
    METInvCutValue           = "20",
    METInvCutDirection       = "<",
    MVACutValue              = "0.4",
    MVACutDirection          = ">=",
)

#================================================================================================
# Common plots options
#================================================================================================
commonPlotsOptions = hplus2tbAnalysis.commonPlotsOptions

#================================================================================================
# Build all selections group
#================================================================================================
allSelections = PSet(
    Verbose               = verbose,
    Trigger               = trigger,
    METFilter             = metFilter,
    ElectronSelection     = eVeto,
    MuonSelection         = muSelection,
    TauSelection          = tauVeto,
    JetSelection          = jetSelection,
    BJetSelection         = bjetSelection,
    METSelection          = metSelection,
    TopSelectionBDT       = topSelectionBDT,
    FatJetSelection       = fatjetVeto,
    FakeBMeasurement      = fakeBMeasurement,
    FakeBBjetSelection    = fakeBBjetSelection,
    FakeBTopSelectionBDT  = fakeBTopSelectionBDT,
    CommonPlots           = commonPlotsOptions,
    HistogramAmbientLevel = histogramAmbientLevel,
    QGLRSelection         = qglrSelection,
    SystTopBDTSelection   = systTopBDTSelection,
)
