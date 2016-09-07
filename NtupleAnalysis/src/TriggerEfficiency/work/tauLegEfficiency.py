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
binning = [20, 30, 40, 50, 60, 80, 100, 120, 200]
xLabel  = "#tau-jet p_{T} (GeV/c)"
yLabel  = "HLT tau efficiency"

import HiggsAnalysis.NtupleAnalysis.tools.aux as aux

eras = {}
eras["2016B"] = "SingleMuon_Run2016B"
eras["2016C"] = "SingleMuon_Run2016C"
eras["2016D"] = "SingleMuon_Run2016D"
eras["2016E"] = "SingleMuon_Run2016E"
eras["2016ICHEP"] = "SingleMuon_Run2016B|SingleMuon_Run2016C|SingleMuon_Run2016D"
eras["2016HIP"] = "SingleMuon_Run2016B|SingleMuon_Run2016C|SingleMuon_Run2016D|SingleMuon_Run2016E|SingleMuon_Run2016F_PromptReco_v1_277816_278800"
eras["2016HIPFIXED"] = "SingleMuon_Run2016F_PromptReco_v1_278801_278808|SingleMuon_Run2016G"

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
            discriminators = ["Muons_TrgMatch_IsoMu16_eta2p1"],
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
            a.Trigger.triggerOR = ["HLT_IsoMu16_eta2p1_MET30_JetIdCleaned_v1","HLT_IsoMu16_eta2p1_MET30_JetIdCleaned_vx"]
            a.Trigger.triggerOR2= ["HLT_IsoMu16_eta2p1_MET30_JetIdCleaned_LooseIsoPFTau50_Trk30_eta2p1_v1","HLT_IsoMu16_eta2p1_MET30_JetIdCleaned_LooseIsoPFTau50_Trk30_eta2p1_vx"]
#            a.Trigger.triggerOR = ["HLT_IsoMu20_eta2p1_v2"]
#            a.Trigger.triggerOR2 = ["HLT_IsoMu17_eta2p1_LooseIsoPFTau20_v2"]
        if era == "2015D":
            a.Trigger.triggerOR = ["HLT_IsoMu16_eta2p1_MET30_JetIdCleaned_v2",
                                   "HLT_IsoMu16_eta2p1_MET30_JetIdCleaned_v3",
                                   "HLT_IsoMu16_eta2p1_MET30_JetIdCleaned_vx",
                                   "HLT_IsoMu16_eta2p1_MET30_v1",
                                   "HLT_IsoMu16_eta2p1_MET30_vx"]
            a.Trigger.triggerOR2= ["HLT_IsoMu16_eta2p1_MET30_JetIdCleaned_LooseIsoPFTau50_Trk30_eta2p1_v2",
                                   "HLT_IsoMu16_eta2p1_MET30_JetIdCleaned_LooseIsoPFTau50_Trk30_eta2p1_v3",
                                   "HLT_IsoMu16_eta2p1_MET30_JetIdCleaned_LooseIsoPFTau50_Trk30_eta2p1_vx",
                                   "HLT_IsoMu16_eta2p1_MET30_LooseIsoPFTau50_Trk30_eta2p1_v1",
                                   "HLT_IsoMu16_eta2p1_MET30_LooseIsoPFTau50_Trk30_eta2p1_vx"]
        if era == "2015CD":
            a.Trigger.triggerOR = ["HLT_IsoMu16_eta2p1_MET30_JetIdCleaned_v1",
                                   "HLT_IsoMu16_eta2p1_MET30_JetIdCleaned_v2",
                                   "HLT_IsoMu16_eta2p1_MET30_JetIdCleaned_v3",
                                   "HLT_IsoMu16_eta2p1_MET30_v1"]
            a.Trigger.triggerOR2= ["HLT_IsoMu16_eta2p1_MET30_JetIdCleaned_LooseIsoPFTau50_Trk30_eta2p1_v1",
                                   "HLT_IsoMu16_eta2p1_MET30_JetIdCleaned_LooseIsoPFTau50_Trk30_eta2p1_v2",
                                   "HLT_IsoMu16_eta2p1_MET30_JetIdCleaned_LooseIsoPFTau50_Trk30_eta2p1_v3",
                                   "HLT_IsoMu16_eta2p1_MET30_LooseIsoPFTau50_Trk30_eta2p1_v1"]
        if "2016" in era:
            a.Trigger.triggerOR = ["HLT_IsoMu16_eta2p1_MET30_vx"]
            a.Trigger.triggerOR2= ["HLT_IsoMu16_eta2p1_MET30_LooseIsoPFTau50_Trk30_eta2p1_vx"]

        if era == "2016ICHEP":
            a.Trigger.triggerOR = ["HLT_IsoMu16_eta2p1_MET30_vx"]
            a.Trigger.triggerOR2= ["HLT_IsoMu16_eta2p1_MET30_LooseIsoPFTau50_Trk30_eta2p1_vx"]
                                    
#            a.Trigger.triggerOR = ["HLT_IsoMu20_eta2p1_v1",
#                                   "HLT_IsoMu20_eta2p1_v2",
#                                   "HLT_IsoMu17_eta2p1_v2"]
#            a.Trigger.triggerOR2= ["HLT_IsoMu17_eta2p1_LooseIsoPFTau20_v1",
#                                   "HLT_IsoMu17_eta2p1_LooseIsoPFTau20_v2"]

#        runmin,runmax = process.getRuns()
#        a.lumi    = lumi
        a.runMin  = runmin
        a.runMax  = runmax
    else:
        a.Trigger.triggerOR = ["HLT_IsoMu15_eta2p1_L1ETM20_v5"]
        a.Trigger.triggerOR2 = ["HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v6"]
        if era == "2015C" or era == "2015D" or era == "2015CD" or "2016" in era:
            a.Trigger.triggerOR = ["HLT_IsoMu16_eta2p1_CaloMET30_v1",
                                   "HLT_IsoMu16_eta2p1_MET30_vx",
                                   "HLT_IsoMu16_eta2p1_MET30_JetIdCleaned_vx"]
            a.Trigger.triggerOR2 = ["HLT_IsoMu16_eta2p1_CaloMET30_LooseIsoPFTau50_Trk30_eta2p1_v1",
                                    "HLT_IsoMu16_eta2p1_MET30_LooseIsoPFTau50_Trk30_eta2p1_vx",
                                    "HLT_IsoMu16_eta2p1_MET30_JetIdCleaned_LooseIsoPFTau50_Trk30_eta2p1_vx"]
#            a.Trigger.triggerOR = ["HLT_IsoMu20_eta2p1_v1"]
#            a.Trigger.triggerOR2 = ["HLT_IsoMu17_eta2p1_LooseIsoPFTau20_v1"]

    #print "check triggerOR",a.Trigger.triggerOR
    return a

def addAnalyzer(era):
    process = Process(outputPrefix="tauLegEfficiency_"+era)
#    process.setDatasets([])
    process.addDatasetsFromMulticrab(sys.argv[1])
    ds = getDatasetsForEras(process.getDatasets(),eras[era])
    process.setDatasets(ds)
    global runmin,runmax
    runmin,runmax = process.getRuns()
    process.addAnalyzer("TauLeg_"+era, lambda dv: createAnalyzer(dv, era))
#    process.addAnalyzer("TauLeg_"+era, createAnalyzer(dv, era))
    process.run()

#dv = ["53Xdata22Jan2013","53mcS10"]
#process.addAnalyzer("TauLeg_2012D", lambda dv: createAnalyzer(dv,"2012D"), excludeTasks=["2012A","2012B", "2012C"])
#addAnalyzer("2012ABC")
#addAnalyzer("2012D")
#addAnalyzer("2015C")
#addAnalyzer("2015D")
#addAnalyzer("2015CD")
#addAnalyzer("2016B")
#addAnalyzer("2016C")
#addAnalyzer("2016D")
#addAnalyzer("2016E")
addAnalyzer("2016ICHEP")
#addAnalyzer("2016HIP")


# Run the analysis
#process.run()


# Run the analysis with PROOF
# By default it uses all cores, but you can give proofWorkers=<N> as a parameter
#process.run(proof=True)
