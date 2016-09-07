#!/usr/bin/env python

from HiggsAnalysis.NtupleAnalysis.main import Process, PSet, Analyzer
import HiggsAnalysis.NtupleAnalysis.parameters.signalAnalysisParameters as signalAnalysis

import re

#process = Process(outputPrefix="metLegEfficiency")

# Example of adding a dataset which has its files defined in data/<dataset_name>.txt file
#process.addDatasets(["TTbar_HBWB_HToTauNu_M_160_13TeV_pythia6"])

# Example of adding datasets from a multicrab directory
import sys
if len(sys.argv) != 2:
    print "Usage: ./exampleAnalysis.py <path-to-multicrab-directory>"
    sys.exit(0)
#process.addDatasetsFromMulticrab(sys.argv[1])

leg     = "metlegSelection"
binning = [20, 30, 40, 50, 60, 70, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300]
xLabel  = "Type1 MET (GeV)"
yLabel  = "Level-1 + HLT MET efficiency"

## Example of adding an analyzer
#process.addAnalyzer("test", Analyzer("TriggerEfficiency",
#    offlineSelection = "metlegSelection",
#    binning = [20, 30, 40, 50, 60, 70, 80, 100, 120, 140, 160, 180, 200],
#    xLabel = "Type1 MET (GeV)",
#    yLabel = "Level-1 + HLT MET efficiency" 
#))

import HiggsAnalysis.NtupleAnalysis.tools.aux as aux

eras = {}
eras["2016D"]     = "Tau_Run2016D"
eras["2016E"]     = "Tau_Run2016E"
eras["2016MET80"] = "Tau_Run2016B|Tau_Run2016C|Tau_Run2016D_PromptReco_v2_276315_276437"
eras["2016ICHEP"] = "Tau_Run2016B|Tau_Run2016C|Tau_Run2016D"
eras["2016"]      = "Tau_Run2016"

runmin = -1
runmax = -1

#from tauLegEfficiency import getDatasetsForEras
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

def createAnalyzer(dataVersion,era,onlineSelection = "MET80"):
    useCaloMET = False
    if "CaloMET" in era:
        useCaloMET = True
        era = era[:-8]

    a = Analyzer("TriggerEfficiency",
        name = era,
        Trigger = PSet(
            triggerOR  = [],
            triggerOR2 = []
        ),
        usePileupWeights = True,
#        usePileupWeights = False,
        onlineSelection = onlineSelection,
        offlineSelection = leg,
        TauSelection      = signalAnalysis.tauSelection,
#        TauSelection = PSet(
#            discriminators = ["byLooseCombinedIsolationDeltaBetaCorr3Hits",
#                             "againstMuonTight3",
#                             "againstElectronMediumMVA5"],
#        ),
        ElectronSelection = signalAnalysis.eVeto,
        MuonSelection     = signalAnalysis.muVeto,
        JetSelection      = signalAnalysis.jetSelection,
        BJetSelection     = signalAnalysis.bjetSelection,
        binning = binning,
        xLabel  = xLabel,
        yLabel  = yLabel,
    )
#    a.TauSelection.applyTriggerMatching = False
    a.JetSelection.numberOfJetsCutValue = 3
#    a.BJetSelection.bjetDiscrWorkingPoint = "Medium"
    a.BJetSelection.numberOfBJetsCutValue = 1

    if dataVersion.isData():
        a.Trigger.triggerOR = ["HLT_LooseIsoPFTau35_Trk20_Prong1_v2",
                               "HLT_LooseIsoPFTau35_Trk20_Prong1_v3",
                               "HLT_LooseIsoPFTau35_Trk20_Prong1_v4",
                               "HLT_LooseIsoPFTau35_Trk20_Prong1_v6",
                               "HLT_LooseIsoPFTau35_Trk20_Prong1_v7",
                               "HLT_LooseIsoPFTau35_Trk20_Prong1_v9",
                               "HLT_LooseIsoPFTau35_Trk20_Prong1_v10"]
        a.Trigger.triggerOR2 = ["HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v2",
                                "HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v3",
                                "HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v4",
                                "HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v6",
                                "HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v7",
                                "HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v9",
                                "HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v10"]
        if era == "2015C" or era == "2015D" or era == "2015CD":
            a.Trigger.triggerOR = ["HLT_LooseIsoPFTau50_Trk30_eta2p1_v1",
                                   "HLT_LooseIsoPFTau50_Trk30_eta2p1_v2",
                                   "HLT_LooseIsoPFTau50_Trk30_eta2p1_v3",
                                   "HLT_LooseIsoPFTau50_Trk30_eta2p1_vx"]
            a.Trigger.triggerOR2 = ["HLT_LooseIsoPFTau50_Trk30_eta2p1_"+onlineSelection+"_JetIdCleaned_v1",
                                    "HLT_LooseIsoPFTau50_Trk30_eta2p1_"+onlineSelection+"_JetIdCleaned_v2",
                                    "HLT_LooseIsoPFTau50_Trk30_eta2p1_"+onlineSelection+"_v1",
                                    "HLT_LooseIsoPFTau50_Trk30_eta2p1_"+onlineSelection+"_JetIdCleaned_vx",
                                    "HLT_LooseIsoPFTau50_Trk30_eta2p1_"+onlineSelection+"_vx"]
        if "2016" in era:
            a.Trigger.triggerOR = ["HLT_LooseIsoPFTau50_Trk30_eta2p1_vx"]
            a.Trigger.triggerOR2 = ["HLT_LooseIsoPFTau50_Trk30_eta2p1_"+onlineSelection+"_vx"]


#        lumi,runmin,runmax = runRange(era)
#        a.lumi    = lumi
        a.runMin  = runmin
        a.runMax  = runmax
    else:
        a.Trigger.triggerOR = ["HLT_LooseIsoPFTau35_Trk20_Prong1_v6"]
        a.Trigger.triggerOR2 = ["HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v6"]
        if era == "2015C" or era == "2015D" or era == "2015CD" or "2016" in era:
            a.Trigger.triggerOR = ["HLT_LooseIsoPFTau50_Trk30_eta2p1_v1",
                                   "HLT_LooseIsoPFTau50_Trk30_eta2p1_vx"]
            a.Trigger.triggerOR2 = ["HLT_LooseIsoPFTau50_Trk30_eta2p1_"+onlineSelection+"_v1",
                                    "HLT_LooseIsoPFTau50_Trk30_eta2p1_"+onlineSelection+"_vx"]

    if useCaloMET:
        a.Trigger.triggerOR2 = []

    return a

def addAnalyzer(era,onlineSelection):
    process = Process(outputPrefix="metLegEfficiency_"+era)
    process.addDatasetsFromMulticrab(sys.argv[1])
    ds = getDatasetsForEras(process.getDatasets(),eras[era])
    process.setDatasets(ds)
    global runmin,runmax
    runmin,runmax = process.getRuns()
    process.addAnalyzer("METLeg_"+era+"_"+onlineSelection, lambda dv: createAnalyzer(dv, era, onlineSelection))
    process.run()


#addAnalyzer("2012ABCD")
#addAnalyzer("2012D")
#addAnalyzer("2012ABCD_CaloMET")
#addAnalyzer("2015D","MET80")
#addAnalyzer("2016B","MET80")
#addAnalyzer("2016B_CaloMET","MET80")
#addAnalyzer("2016D","MET90")
#addAnalyzer("2016E","MET90")
#addAnalyzer("2016MET80","MET80")
addAnalyzer("2016ICHEP","MET90")
#addAnalyzer("2016","MET90")
#addAnalyzer("2015A","MET120")
#addAnalyzer("2015A_CaloMET","MET120")

# Pick events
#process.addOptions(EventSaver = PSet(enabled = True, pickEvents = True))

# Run the analysis
#process.run()

# Run the analysis with PROOF
# By default it uses all cores, but you can give proofWorkers=<N> as a parameter
#process.run(proof=True)
