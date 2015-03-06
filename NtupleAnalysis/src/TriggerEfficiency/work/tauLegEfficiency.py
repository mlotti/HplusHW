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

leg     = "taulegSelection"
binning = [20, 30, 40, 50, 60, 70, 80, 100, 120, 140, 160, 180, 200]
xLabel  = "#tau-jet p_{T} (GeV/c)"
yLabel  = "HLT tau efficiency"

process.addAnalyzer("Efficiency2012D", Analyzer("TriggerEfficiency",
    offlineSelection = leg,
    binning = binning,
    xLabel  = xLabel,
    yLabel  = yLabel,
    dataera = "2012D",
    lumi    = 7274,
    runMin  = 202807,
    runMax  = 208686,
    sample1 = "data",
    sample2 = "mc",
    controlTriggers1 = [
        "HLT_IsoMu15_eta2p1_L1ETM20_v7",
    ],
    controlTriggers2 = [
        "HLT_IsoMu15_eta2p1_L1ETM20_v5"
    ],
    signalTriggers1 = [
        "HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v10"
    ],
    signalTriggers2 = [               
        "HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v6"
    ],
))

process.addAnalyzer("Efficiency2012ABCD", Analyzer("TriggerEfficiency",
    offlineSelection = leg,
    binning = binning,
    xLabel  = xLabel,
    yLabel  = yLabel,
    dataera = "2012ABCD",
    lumi    = 19296,
    runMin  = 190456,
    runMax  = 208686,
    sample1 = "data",
    sample2 = "mc",
    controlTriggers1 = [
        "HLT_IsoMu15_eta2p1_L1ETM20_v3",
        "HLT_IsoMu15_eta2p1_L1ETM20_v4",
        "HLT_IsoMu15_eta2p1_L1ETM20_v5",
        "HLT_IsoMu15_eta2p1_L1ETM20_v6",
        "HLT_IsoMu15_eta2p1_L1ETM20_v7",
    ],
    controlTriggers2 = [
        "HLT_IsoMu15_eta2p1_L1ETM20_v5"
    ],
    signalTriggers1 = [
        "HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v2",
        "HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v4",
        "HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v6",
        "HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v7",
        "HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v9",
        "HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v10"
    ],
    signalTriggers2 = [
        "HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v6"
    ],
))

# Run the analysis
process.run()

# Run the analysis with PROOF
# By default it uses all cores, but you can give proofWorkers=<N> as a parameter
#process.run(proof=True)
