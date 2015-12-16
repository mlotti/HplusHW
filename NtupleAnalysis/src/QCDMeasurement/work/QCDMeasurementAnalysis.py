#!/usr/bin/env python

dataEras = ["2015"]
#dataEras = ["2015B","2015C"]
searchModes = ["80to1000"]

from HiggsAnalysis.NtupleAnalysis.main import Process, PSet, Analyzer
process = Process("QCDMeasurement")

import sys
if len(sys.argv) < 2:
    print "Usage: ./QCDMeasurementAnalysis.py <path-to-multicrab-directory>"
    sys.exit(0)
process.addDatasetsFromMulticrab(sys.argv[1])

# Add config
from HiggsAnalysis.NtupleAnalysis.parameters.signalAnalysisParameters import allSelections
# Enable genuine tau histograms for common plots (needed for calculating N_QCD)
allSelections.CommonPlots.enableGenuineTauHistograms = True
# Set splitting of phase space (first bin is below first edge value and last bin is above last edge value)
allSelections.CommonPlots.histogramSplitting = [
    PSet(label="tauPt", binLowEdges=[60.0, 70.0, 80.0, 100.0], useAbsoluteValues=False),
  ]

# Build analysis modules
from HiggsAnalysis.NtupleAnalysis.AnalysisBuilder import AnalysisBuilder
builder = AnalysisBuilder("QCDMeasurement", 
                          dataEras,
                          searchModes,
                          #### Options ####
                          usePUreweighting=True,
                          doSystematicVariations=True,
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

