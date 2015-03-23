#!/usr/bin/env python

from HiggsAnalysis.NtupleAnalysis.main import Process, PSet, Analyzer
from HiggsAnalysis.NtupleAnalysis.pileupWeight import pileupWeight

import os

process = Process(outputPrefix="tauLegEfficiency")

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

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.aux as aux
PileupHistogramPath = os.path.join(aux.higgsAnalysisPath(), "NtupleAnalysis", "data", "PUWeights")

def runRange(era):
    lumi   = 0
    runmin = 0
    runmax = 0
    if era == "2012ABC":
        lumi   =  11736  
        runmin = 190456
        runmax = 202585

    if era == "2012D":
        lumi   = 7274
        runmin = 202807
        runmax = 208686

    if lumi == 0:
        print "Unknown era",era,"exiting.."
        sys.exit()

    return lumi,runmin,runmax

def createAnalyzer(dataVersion,era):
    a = Analyzer("TriggerEfficiency",
        Trigger = PSet(
            triggerOR  = [],
            triggerOR2 = []
        ),
        offlineSelection = leg,
        TauSelection = PSet(
            discriminators = ["byLooseCombinedIsolationDeltaBetaCorr3Hits",
                             "againstMuonTight2",
                             "againstElectronMediumMVA3"],
        ),
        binning = binning,
        xLabel  = xLabel,
        yLabel  = yLabel,
    )

    if dataVersion.isData():
        a.Trigger.triggerOR = ["HLT_IsoMu15_eta2p1_L1ETM20_v3",
                               "HLT_IsoMu15_eta2p1_L1ETM20_v4",
                               "HLT_IsoMu15_eta2p1_L1ETM20_v5",
                               "HLT_IsoMu15_eta2p1_L1ETM20_v6",
                               "HLT_IsoMu15_eta2p1_L1ETM20_v7"]
        a.Trigger.triggerOR2 = ["HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v2",
                                "HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v4",
                                "HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v6",
                                "HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v7",
                                "HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v9",
                                "HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v10"]
        lumi,runmin,runmax = runRange(era)
        a.lumi    = lumi
        a.runMin  = runmin
        a.runMax  = runmax
    else:
        a.Trigger.triggerOR = ["HLT_IsoMu15_eta2p1_L1ETM20_v5"]
        a.Trigger.triggerOR2 = ["HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v6"]
        a.PileUpWeight = PSet(
            path = PileupHistogramPath,
            data = era,
            mc   = "Summer12_S10"
        )

    return a

def addAnalyzer(era):
    dv = ["53Xdata22Jan2013","53mcS10"]
    process.addAnalyzer("TauLeg_"+era, lambda dv: createAnalyzer(dv, era))

#dv = ["53Xdata22Jan2013","53mcS10"]
#process.addAnalyzer("TauLeg_2012D", lambda dv: createAnalyzer(dv,"2012D"), excludeTasks=["2012A","2012B", "2012C"])
addAnalyzer("2012ABC")
addAnalyzer("2012D")

"""
process.addAnalyzer("TauLeg_2012D_data", 
    Analyzer("TriggerEfficiency",
        Trigger = PSet(
            triggerOR  = ["HLT_IsoMu15_eta2p1_L1ETM20_v7"],
            triggerOR2 = ["HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v10"]
        ),
        PileupWeight = pileupWeight(enabled=False),
        offlineSelection = leg,
        TauSelection = PSet(
            discriminators = ["byLooseCombinedIsolationDeltaBetaCorr3Hits",
                             "againstMuonTight2",
                             "againstElectronMediumMVA3"],
        ),
        binning = binning,
        xLabel  = xLabel,
        yLabel  = yLabel,
        lumi    = 7274,
        runMin  = 202807,
        runMax  = 208686,
    ),
    includeOnlyTasks="TauPlusX_\S+_2012D_Jan22"
)

process.addAnalyzer("TauLeg_2012D_mc", 
    Analyzer("TriggerEfficiency",
        Trigger = PSet(
            triggerOR  = ["HLT_IsoMu15_eta2p1_L1ETM20_v5"],
            triggerOR2 = ["HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v6"]
        ),
        PileupWeight = pileupWeight(
            data = "2012D",
            mc   = "Summer12_S10"
        ),
        offlineSelection = leg,
        TauSelection = PSet(
            discriminators = ["byLooseCombinedIsolationDeltaBetaCorr3Hits",
                             "againstMuonTight2",
                             "againstElectronMediumMVA3"],
        ),
        binning = binning,
        xLabel  = xLabel,
        yLabel  = yLabel,
    ),
    excludeTasks="TauPlusX_"
)

process.addAnalyzer("TauLeg_2012D_mc_NOPU",
    Analyzer("TriggerEfficiency",
        Trigger = PSet(
            triggerOR  = ["HLT_IsoMu15_eta2p1_L1ETM20_v5"],
            triggerOR2 = ["HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v6"]
        ),
        PileupWeight = pileupWeight(enabled=False),
        offlineSelection = leg,
        TauSelection = PSet(
            discriminators = ["byLooseCombinedIsolationDeltaBetaCorr3Hits",
                             "againstMuonTight2",
                             "againstElectronMediumMVA3"],
        ),
        binning = binning,
        xLabel  = xLabel,
        yLabel  = yLabel,
    ),
    excludeTasks="TauPlusX_"
)
"""
"""
process.addAnalyzer("TauLeg_2012ABCD_data",
    Analyzer("TriggerEfficiency",
        Trigger = PSet(
            triggerOR  = ["HLT_IsoMu15_eta2p1_L1ETM20_v3",
                          "HLT_IsoMu15_eta2p1_L1ETM20_v4",
                          "HLT_IsoMu15_eta2p1_L1ETM20_v5",
                          "HLT_IsoMu15_eta2p1_L1ETM20_v6",
                          "HLT_IsoMu15_eta2p1_L1ETM20_v7"],
            triggerOR2 = ["HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v2",
                          "HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v4",
                          "HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v6",
                          "HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v7",
                          "HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v9",
                          "HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v10"],
        ),
        offlineSelection = leg,
        binning = binning,
        xLabel  = xLabel,
        yLabel  = yLabel,
        dataera = "2012ABCD",
        lumi    = 19296,
        runMin  = 190456,
        runMax  = 208686,
        sample  = "data",
    ),
    includeOnlyTasks="TauPlusX_"
)
process.addAnalyzer("TauLeg_2012ABCD_mc",
    Analyzer("TriggerEfficiency",
        Trigger = PSet(
            triggerOR  = ["HLT_IsoMu15_eta2p1_L1ETM20_v5"],
            triggerOR2 = ["HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v6"]
        ),
        offlineSelection = leg,
        binning = binning,
        xLabel  = xLabel,
        yLabel  = yLabel,
        dataera = "2012ABCD",
        lumi    = 19296,
        runMin  = 190456,
        runMax  = 208686,
        sample  = "mc",
    ),
    excludeTasks="TauPlusX_"
)
"""
# Run the analysis
process.run()


# Run the analysis with PROOF
# By default it uses all cores, but you can give proofWorkers=<N> as a parameter
#process.run(proof=True)
