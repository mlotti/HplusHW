#!/usr/bin/env python

from HiggsAnalysis.NtupleAnalysis.main import Process, PSet, Analyzer

process = Process()
process.addDatasets(["TTbar_HBWB_HToTauNu_M_160_13TeV_pythia6"])
process.addAnalyzer("test", Analyzer("ExampleAnalysis",
                                     tauPtCut = 10
))

process.run()
