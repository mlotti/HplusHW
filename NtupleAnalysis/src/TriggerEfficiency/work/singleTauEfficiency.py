#!/usr/bin/env python

from HiggsAnalysis.NtupleAnalysis.main import Process, PSet, Analyzer

import os
import re

#process = Process(outputPrefix="tauLegEfficiency")

# Example of adding a dataset which has its files defined in data/<dataset_name>.txt file
#process.addDatasets(["TTbar_HBWB_HToTauNu_M_160_13TeV_pythia6"])

# Example of adding datasets from a multicrab directory
import sys
if len(sys.argv) != 2:
    print "Usage: ./exampleAnalysis.py <path-to-multicrab-directory>"
    sys.exit(0)

#process.addDatasetsFromMulticrab(sys.argv[1])
#process.addDatasetsFromMulticrab(sys.argv[1],includeOnlyTasks="SingleMuon_Run2015D_PromptReco_v3_246908_260426_25ns$")
#process.addDatasetsFromMulticrab(sys.argv[1],includeOnlyTasks="SingleMuon_Run2015")
#process.addDatasetsFromMulticrab(sys.argv[1],includeOnlyTasks="DYJetsToLL_M50")
#process.addDatasetsFromMulticrab(sys.argv[1],includeOnlyTasks="GluGluHToTauTau_M125")

leg     = "taulegSelection"
#binning = [20, 30, 40, 50, 60, 70, 80, 100, 120, 140, 160, 180, 200]
binning = [20, 30, 40, 50, 60, 80, 100, 120, 200, 300, 400, 500]
xLabel  = "#tau_{h} p_{T} (GeV/c)"
yLabel  = "HLT tau efficiency"

#tauThreshold = "120"
tauThreshold = "140"

import HiggsAnalysis.NtupleAnalysis.tools.aux as aux

eras = {}
eras["2016B"] = "SingleMuon_Run2016B"
eras["2016C"] = "SingleMuon_Run2016C"
eras["2016D"] = "SingleMuon_Run2016D"
eras["2016E"] = "SingleMuon_Run2016E"
eras["2016ICHEP"] = "SingleMuon_Run2016B|SingleMuon_Run2016C|SingleMuon_Run2016D"
eras["2016HIP"] = "SingleMuon_Run2016B|SingleMuon_Run2016C|SingleMuon_Run2016D|SingleMuon_Run2016E|SingleMuon_Run2016F_PromptReco_v1_277816_278800"
eras["2016HIPFIXED"] = "SingleMuon_Run2016F_PromptReco_v1_278801_278808|SingleMuon_Run2016G|SingleMuon_Run2016H"

runmin = -1
runmax = -1

def getDatasetsForEras(dsets,era):
    dset_re = re.compile(era)
    dOUT = []
    for dset in dsets:
        if dset.getDataVersion().isData():
            match = dset_re.search(dset.getName())
            if match:
                dOUT.append(dset)
        else:
            dOUT.append(dset)
    return dOUT

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
        usePileupWeights = True,
        offlineSelection = leg,
        MuonSelection = PSet(
#            discriminators = ["muIDMedium"],
#            discriminators = ["TrgMatch_IsoMu20_eta2p1"],
#            discriminators = ["Muons_TrgMatch_IsoMu16_eta2p1"],
        ),
        TauSelection = PSet(
            discriminators = ["byLooseCombinedIsolationDeltaBetaCorr3Hits",#"byMediumIsolationMVA3newDMwLT",
                              "againstMuonTight3",
                              "againstElectronMediumMVA6"],
            nprongs = 1,
        ),
        binning = binning,
        xLabel  = xLabel,
        yLabel  = yLabel,
    )

    if isData(dataVersion):
        if "2016" in era:
            a.Trigger.triggerOR = ["HLT_IsoMu22_eta2p1_vx"]
            a.Trigger.triggerOR2= ["HLT_VLooseIsoPFTau"+tauThreshold+"_Trk50_eta2p1_vx"]

        a.runMin  = runmin
        a.runMax  = runmax
    else:
        if "2016" in era:
            a.Trigger.triggerOR = ["HLT_IsoMu22_eta2p1_vx"]
            a.Trigger.triggerOR2= ["HLT_VLooseIsoPFTau"+tauThreshold+"_Trk50_eta2p1_vx"]

    return a

def addAnalyzer(era):
    process = Process(outputPrefix="singleTauEfficiency_"+era)
    process.addDatasetsFromMulticrab(sys.argv[1])
    ds = getDatasetsForEras(process.getDatasets(),eras[era])
    process.setDatasets(ds)
    global runmin,runmax
    runmin,runmax = process.getRuns()
    process.addAnalyzer("SingleTau"+tauThreshold+"_"+era, lambda dv: createAnalyzer(dv, era))
    process.run()

#addAnalyzer("2016ICHEP")
#addAnalyzer("2016HIP")
addAnalyzer("2016HIPFIXED")

