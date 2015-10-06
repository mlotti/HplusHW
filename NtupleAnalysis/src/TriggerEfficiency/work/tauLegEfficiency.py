#!/usr/bin/env python

from HiggsAnalysis.NtupleAnalysis.main import Process, PSet, Analyzer
from HiggsAnalysis.NtupleAnalysis.pileupWeight import pileupWeight

import os
import re

process = Process(outputPrefix="tauLegEfficiency")

# Example of adding a dataset which has its files defined in data/<dataset_name>.txt file
#process.addDatasets(["TTbar_HBWB_HToTauNu_M_160_13TeV_pythia6"])

# Example of adding datasets from a multicrab directory
import sys
if len(sys.argv) != 2:
    print "Usage: ./exampleAnalysis.py <path-to-multicrab-directory>"
    sys.exit(0)
process.addDatasetsFromMulticrab(sys.argv[1],includeOnlyTasks="SingleMuon_Run2015")
process.addDatasetsFromMulticrab(sys.argv[1],includeOnlyTasks="DYJetsToLL_M50")

leg     = "taulegSelection"
#binning = [20, 30, 40, 50, 60, 70, 80, 100, 120, 140, 160, 180, 200]
binning = [20, 30, 40, 50, 60, 90, 200]
xLabel  = "#tau-jet p_{T} (GeV/c)"
yLabel  = "HLT tau efficiency"

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.aux as aux

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

    if era == "2015C":
        lumi = 15.478
        runmin = 253888
        runmax = 254914

    if era == "2015D":
        lumi = 001.2157
        runmin = 257400
        runmax = 257611

    if era == "2015CD":
        lumi = 16.6937
        runmin = 253888
        runmax = 256869

    if lumi == 0:
        print "Unknown era",era,"exiting.."
        sys.exit()

    return lumi,runmin,runmax

def isData(dataVersion):
    dataVersion = str(dataVersion)
    #print type(dataVersion)
    #print dataVersion
    dv_re = re.compile("data")
    match = dv_re.search(dataVersion)
    if match:
        return True
    return False

def createAnalyzer(dataVersion,era):
    a = Analyzer("TriggerEfficiency",
        name = era,
        Trigger = PSet(
            triggerOR  = [],
            triggerOR2 = []
        ),
        PileupWeight = pileupWeight(enabled=False),
        offlineSelection = leg,
        MuonSelection = PSet(
#            discriminators = ["muIDMedium"],
#            discriminators = ["TrgMatch_IsoMu20_eta2p1"],
            discriminators = ["Muons_TrgMatch_IsoMu16_eta2p1"],
        ),
        TauSelection = PSet(
            discriminators = ["byLooseCombinedIsolationDeltaBetaCorr3Hits",
                             "againstMuonTight3",
                             "againstElectronMediumMVA5"],
        ),
        binning = binning,
        xLabel  = xLabel,
        yLabel  = yLabel,
    )

    if isData(dataVersion):
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
        if era == "2015C":
#            a.Trigger.triggerOR = ["HLT_IsoMu16_eta2p1_CaloMET30_v1",
#                                   "HLT_IsoMu16_eta2p1_MET30_JetIdCleaned_v1"]
#            a.Trigger.triggerOR2 = ["HLT_IsoMu16_eta2p1_CaloMET30_LooseIsoPFTau50_Trk30_eta2p1_v1",
#                                    "HLT_IsoMu16_eta2p1_MET30_JetIdCleaned_LooseIsoPFTau50_Trk30_eta2p1_v1"]
            a.Trigger.triggerOR = ["HLT_IsoMu16_eta2p1_MET30_JetIdCleaned_v1"]
            a.Trigger.triggerOR2= ["HLT_IsoMu16_eta2p1_MET30_JetIdCleaned_LooseIsoPFTau50_Trk30_eta2p1_v1"]
#            a.Trigger.triggerOR = ["HLT_IsoMu20_eta2p1_v2"]
#            a.Trigger.triggerOR2 = ["HLT_IsoMu17_eta2p1_LooseIsoPFTau20_v2"]
        if era == "2015D":
            a.Trigger.triggerOR = ["HLT_IsoMu16_eta2p1_MET30_JetIdCleaned_v2"]
            a.Trigger.triggerOR2= ["HLT_IsoMu16_eta2p1_MET30_JetIdCleaned_LooseIsoPFTau50_Trk30_eta2p1_v2"]
        if era == "2015CD":
            a.Trigger.triggerOR = ["HLT_IsoMu16_eta2p1_MET30_JetIdCleaned_v1",
                                   "HLT_IsoMu16_eta2p1_MET30_JetIdCleaned_v2"]
            a.Trigger.triggerOR2= ["HLT_IsoMu16_eta2p1_MET30_JetIdCleaned_LooseIsoPFTau50_Trk30_eta2p1_v1",
                                   "HLT_IsoMu16_eta2p1_MET30_JetIdCleaned_LooseIsoPFTau50_Trk30_eta2p1_v2"]
#            a.Trigger.triggerOR = ["HLT_IsoMu20_eta2p1_v1",
#                                   "HLT_IsoMu20_eta2p1_v2",
#                                   "HLT_IsoMu17_eta2p1_v2"]
#            a.Trigger.triggerOR2= ["HLT_IsoMu17_eta2p1_LooseIsoPFTau20_v1",
#                                   "HLT_IsoMu17_eta2p1_LooseIsoPFTau20_v2"]

        lumi,runmin,runmax = runRange(era)
        a.lumi    = lumi
        a.runMin  = runmin
        a.runMax  = runmax
    else:
        a.Trigger.triggerOR = ["HLT_IsoMu15_eta2p1_L1ETM20_v5"]
        a.Trigger.triggerOR2 = ["HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v6"]
        if era == "2015C" or era == "2015D" or era == "2015CD":
            a.Trigger.triggerOR = ["HLT_IsoMu16_eta2p1_CaloMET30_v1"]
            a.Trigger.triggerOR2 = ["HLT_IsoMu16_eta2p1_CaloMET30_LooseIsoPFTau50_Trk30_eta2p1_v1"]
#            a.Trigger.triggerOR = ["HLT_IsoMu20_eta2p1_v1"]
#            a.Trigger.triggerOR2 = ["HLT_IsoMu17_eta2p1_LooseIsoPFTau20_v1"]

        a.PileupWeight = pileupWeight(
#            data = era,
            data = "2012ABCD", # FIXME
            mc   = "Summer12_S10" # FIXME
        )
    #print "check triggerOR",a.Trigger.triggerOR
    return a

def addAnalyzer(era):
    dv = ["53Xdata22Jan2013","53mcS10"]
    if era == "2015C" or era == "2015D" or era == "2015CD":
        dv = ["74Xdata","74Xmc"]
    process.addAnalyzer("TauLeg_"+era, lambda dv: createAnalyzer(dv, era))

#dv = ["53Xdata22Jan2013","53mcS10"]
#process.addAnalyzer("TauLeg_2012D", lambda dv: createAnalyzer(dv,"2012D"), excludeTasks=["2012A","2012B", "2012C"])
#addAnalyzer("2012ABC")
#addAnalyzer("2012D")
addAnalyzer("2015CD")



# Run the analysis
process.run()


# Run the analysis with PROOF
# By default it uses all cores, but you can give proofWorkers=<N> as a parameter
#process.run(proof=True)
