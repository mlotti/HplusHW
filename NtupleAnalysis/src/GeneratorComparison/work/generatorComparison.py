#!/usr/bin/env python

from HiggsAnalysis.NtupleAnalysis.main import Process, PSet, Analyzer

import os

process = Process(outputPrefix="generatorComparison")

# Example of adding a dataset which has its files defined in data/<dataset_name>.txt file
#process.addDatasets(["TTbar_HBWB_HToTauNu_M_160_13TeV_pythia6"])

# Example of adding datasets from a multicrab directory
import sys
if len(sys.argv) != 2:
    print "Usage: ./exampleAnalysis.py <path-to-multicrab-directory>"
    sys.exit(0)

#print sys.argv[1]

process.addDatasetsFromMulticrab(sys.argv[1])

import HiggsAnalysis.NtupleAnalysis.tools.aux as aux
PileupHistogramPath = os.path.join(aux.higgsAnalysisPath(), "NtupleAnalysis", "data", "PUWeights")

process.addAnalyzer("generatorComparison", 
    Analyzer("GeneratorComparison",
        histogramAmbientLevel = "Informative",
        tauPtCut = 41.0,
        tauEtaCut = 2.1,
        bjetEtCut = 30.0,
        bjetEtaCut = 2.4,

        lumi    = 7274,
        runMin  = 202807,
        runMax  = 208686,
    ),
    #includeOnlyTasks="TauPlusX_\S+_2012D_Jan22"
)

# Run the analysis
process.run()


# Run the analysis with PROOF
# By default it uses all cores, but you can give proofWorkers=<N> as a parameter
#process.run(proof=True)
