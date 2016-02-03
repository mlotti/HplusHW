#!/usr/bin/env python

dataEras = ["2015"]
#dataEras = ["2015B","2015C"]
searchModes = ["80to1000"]

from HiggsAnalysis.NtupleAnalysis.main import Process, PSet, Analyzer
process = Process("CorrelationAnalysis")

import sys
if len(sys.argv) < 2:
    print "Usage: ./CorrelationAnalysis.py <path-to-multicrab-directory>"
    sys.exit(0)
process.addDatasetsFromMulticrab(sys.argv[1])

# Add config
from HiggsAnalysis.NtupleAnalysis.parameters.signalAnalysisParameters import allSelections
# Enable genuine tau histograms for common plots (needed for calculating N_QCD)
allSelections.CommonPlots.enableGenuineTauHistograms = True
# Set splitting of phase space (first bin is below first edge value and last bin is above last edge value)
#allSelections.CommonPlots.histogramSplitting = [
#    PSet(label="tauPt", binLowEdges=[60.0, 70.0, 80.0, 100.0, 120.0], useAbsoluteValues=False),
#  ]


allSelections.TauSelection.rtau = 0.0
allSelections.TauSelection.prongs = 1
allSelections.TauSelection.againstElectronDiscr = "againstElectronLooseMVA5"
allSelections.TauSelection.againstMuonDiscr = "againstMuonLoose3"

allSelections.AngularCutsCollinear.cutValueJet1 = 0.0
allSelections.AngularCutsCollinear.cutValueJet2 = 0.0
allSelections.AngularCutsCollinear.cutValueJet3 = 0.0
allSelections.AngularCutsCollinear.cutValueJet4 = 0.0
allSelections.JetSelection.jetType = "JetsPuppi"
#allSelections.BJetSelection.numberOfBJetsCutValue = 0
#allSelections.BJetSelection.numberOfBJetsCutDirection = "=="
#allSelections.BJetSelection.bjetDiscrWorkingPoint = "Loose"
allSelections.METSelection.METCutValue = 80.0
allSelections.METSelection.METType = "MET_Puppi"
#allSelections.AngularCutsCollinear.cutValueJet1 = 40.0
#allSelections.AngularCutsCollinear.cutValueJet2 = 40.0
#allSelections.AngularCutsCollinear.cutValueJet3 = 40.0
#allSelections.AngularCutsCollinear.cutValueJet4 = 40.0
#allSelections.BJetSelection.bjetDiscrWorkingPoint = "Tight"
allSelections.AngularCutsBackToBack.cutValueJet1 = 40.0
allSelections.AngularCutsBackToBack.cutValueJet2 = 40.0
allSelections.AngularCutsBackToBack.cutValueJet3 = 40.0
allSelections.AngularCutsBackToBack.cutValueJet4 = 40.0

#allSelections.BJetSelection.bjetDiscrWorkingPoint = "Tight"
#allSelections.BJetSelection.numberOfBJetsCutValue = 2
#allSelections.BJetSelection.numberOfBJetsCutDirection = "==" # options: ==, !=, <, <=, >, >=             

# Build analysis modules
from HiggsAnalysis.NtupleAnalysis.AnalysisBuilder import AnalysisBuilder
builder = AnalysisBuilder("CorrelationAnalysis", 
                          dataEras,
                          searchModes,
                          #### Options ####
                          usePUreweighting=True,
                      
                               #doSystematicVariations=True,
                          )
#builder.addVariation()
builder.build(process, allSelections)

# Pick events
#process.addOptions(EventSaver = PSet(enabled = True,pickEvents = True))

# Run the analysis
if "proof" in sys.argv:
    process.run(proof=True)
else:
    process.run()

# Run the analysis with PROOF
# By default it uses all cores, but you can give proofWorkers=<N> as a parameter

