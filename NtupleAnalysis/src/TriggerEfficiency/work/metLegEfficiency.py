#!/usr/bin/env python

from HiggsAnalysis.NtupleAnalysis.main import Process, PSet, Analyzer

process = Process()

# Example of adding a dataset which has its files defined in data/<dataset_name>.txt file
#process.addDatasets(["TTbar_HBWB_HToTauNu_M_160_13TeV_pythia6"])

# Example of adding datasets from a multicrab directory
import sys
if len(sys.argv) != 2:
    print "Usage: ./exampleAnalysis.py <path-to-multicrab-directory>"
    sys.exit(0)
process.addDatasetsFromMulticrab(sys.argv[1])

# Example of adding an analyzer
process.addAnalyzer("test", Analyzer("TriggerEfficiency",
    offlineSelection = "metlegSelection",
    binning = [20, 30, 40, 50, 60, 70, 80, 100, 120, 140, 160, 180, 200],
    xLabel = "Type1 MET (GeV)",
    yLabel = "Level-1 + HLT MET efficiency" 
))

# Run the analysis
process.run()

# Run the analysis with PROOF
# By default it uses all cores, but you can give proofWorkers=<N> as a parameter
#process.run(proof=True)
