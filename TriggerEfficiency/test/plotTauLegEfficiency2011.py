#!/usr/bin/env python

######################################################################
#
# The ntuple files should come from the TTEff code
#
# Needs ROOT >= 5.30 (for TEfficiency)
#
# Author: Matti Kortelainen
# Modified 18052012/S.Lehti
# Modified 20062012/S.Lehti
# Modified 12122013/S.Lehti to use the same code as 2012 tau and 2011 and 2012 met legs
#
######################################################################

import os
import array
import re
import sys
from math import sqrt

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.cutstring import * # And, Not, Or

from PythonWriter import PythonWriter
pythonWriter = PythonWriter("tauLegTriggerEfficiency2011")
from Plotter import Plotter

highPurity = True
#highPurity = False

def usage():
    print "\n"
    print "### Usage:   "+sys.argv[0]+" <multicrab dir>\n"
    print "\n"
    sys.exit()

analysis = "analysis"
#counters = analysis+"/counters"                                                                                

plotDir = "TauLeg2011_Test05062014"

def main():
    if len(sys.argv) < 2:
        usage()

    pythonWriter.setInput(sys.argv[1])

    datasets = dataset.getDatasetsFromMulticrabCfg(cfgfile=os.path.join(sys.argv[1], "multicrab.cfg"), weightedCounters=False,
                                                   includeOnlyTasks="SingleMu_")
    datasetsMC = dataset.getDatasetsFromMulticrabCfg(cfgfile=os.path.join(sys.argv[1], "multicrab.cfg"), weightedCounters=False,
                                                     excludeTasks="SingleMu_")
    print datasetsMC.getAllDatasetNames()
    datasetsMC.datasets[0].setCrossSection(1.0)

    datasets.extend(datasetsMC)

    for d in datasets.getAllDatasets():
#        print d.getName()                                                                                                                           
        d.info["energy"] = "7"

    xsect.setBackgroundCrossSections(datasets,doWNJetsWeighting=False)
    datasets.loadLuminosities()

    style = tdrstyle.TDRStyle()

    histograms.createLegend.moveDefaults(dh=-0.18)

    puWeights = []
    puWeights.append("pileupWeight_2011AB.C")
    puWeights.append("pileupWeight_2011A.C")
    puWeights.append("pileupWeight_2011A_RR1.C")
    puWeights.append("pileupWeight_2011A_RR2.C")
    puWeights.append("pileupWeight_2011A_RR3.C")
    puWeights.append("pileupWeight_2011B.C")
#    puWeights.append("pileupWeight_Unweighted.C")

    puWeightPath = "src/HiggsAnalysis/TriggerEfficiency/test"


    global plotDir
    if highPurity:
        dataset._optionDefaults["input"] = "histograms-*-highpurity.root"
        plotDir += "_highPurity"
    else:
        dataset._optionDefaults["input"] = "histograms-*-lowpurity.root"
        plotDir += "_lowPurity"
    pythonWriter.setPlotDir(plotDir)

    ### Offline selection definition
    tauIDdiscriminators           = []
    againstMuonDiscriminators     = []
    againstElectronDiscriminators = []

    tauIDdiscriminators.append("byLooseCombinedIsolationDeltaBetaCorr3Hits")
    tauIDdiscriminators.append("byMediumCombinedIsolationDeltaBetaCorr3Hits")
    tauIDdiscriminators.append("byTightCombinedIsolationDeltaBetaCorr3Hits")
#    tauIDdiscriminators.append("byLooseCombinedIsolationDeltaBetaCorr")

    againstMuonDiscriminators.append("againstMuonMedium2")
    againstMuonDiscriminators.append("againstMuonTight2")
#    againstMuonDiscriminators.append("againstMuonMedium")

    againstElectronDiscriminators.append("againstElectronMediumMVA3")
    againstElectronDiscriminators.append("againstElectronTightMVA3")
    againstElectronDiscriminators.append("againstElectronVTightMVA3")
#    againstElectronDiscriminators.append("againstElectronMedium")

    offlineSelections = []
    for eleD in againstElectronDiscriminators:
        for muonD in againstMuonDiscriminators:
            for tauD in tauIDdiscriminators:


                ### Offline selection definition (H+)                                                                                                
                offlineTauSelection = "PFTauPt > 20 && abs(PFTauEta) < 2.1"
                offlineTauSelection+= "&& PFTauLeadChargedHadrCandPt > 20"
                offlineTauSelection+= "&& PFTauProng == 1"
                offlineTauSelection+= "&& PFTau_%s > 0.5"%eleD
                offlineTauSelection+= "&& PFTau_%s > 0.5"%muonD
                offlineTauSelection+= "&& PFTau_%s > 0.5"%tauD

                offlineMuonSelection = "MuonPt > 15"
                offlineMuonSelection+= "&& MuonIsGlobalMuon"
                #    offlineMuonSelection+= "&& MuonIso03SumPt < 1"                                                                                  

                offlineSelectionHPlus = "Sum$(%s) == 1 && Sum$(%s) == 1"%(offlineTauSelection,offlineMuonSelection)
                offlineSelectionHPlus = offlineTauSelection #### REMOVE ME

                if highPurity:
                    # (p4+k4).M() = sqrt(2*|p3||k3|-2*p3 dot k3)                                                                                     
                    muTauInvMass = "sqrt(2*(sqrt(MuonPt*TMath::Cos(MuonPhi)*MuonPt*TMath::Cos(MuonPhi)+MuonPt*TMath::Sin(MuonPhi)*MuonPt*TMath::Sin(MuonPhi)+MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta)))*MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta))))*sqrt(PFTauPt*TMath::Cos(PFTauPhi)*PFTauPt*TMath::Cos(PFTauPhi)+PFTauPt*TMath::Sin(PFTauPhi)*PFTauPt*TMath::Sin(PFTauPhi)+PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta)))*PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta))))-MuonPt*TMath::Cos(MuonPhi)*PFTauPt*TMath::Cos(PFTauPhi)-MuonPt*TMath::Sin(MuonPhi)*PFTauPt*TMath::Sin(PFTauPhi)-MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta)))*PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta)))))"
                    offlineSelectionHPlus += "&& "+muTauInvMass+" < 80"
                    muMetMt = "sqrt( 2 * MuonPt * PFMET_ET * (1-cos(MuonPhi-PFMET_phi)) )"
                    muMetMtCut = "&& "+muMetMt+" < 40"
                    offlineSelectionHPlus += muMetMtCut

                offlineSelection = offlineSelectionHPlus
                offlineSelections.append(namedselection(tauD+"_"+muonD+"_"+eleD,offlineSelection))

    pu_re = re.compile("pileupWeight_(?P<scenario>(\S+))\.C")
    for puWeight in puWeights:
        pyScenario = pu_re.search(puWeight)
        match = pu_re.search(puWeight)
        if match:
            pyScenario = match.group("scenario")

            if pyScenario != "Unweighted":
                ROOT.gROOT.Clear()
                ROOT.gROOT.Reset()
                macroPath = os.path.join(os.environ["PWD"], puWeight)
                macroPath = macroPath.replace("../src/","")
                macroPath = macroPath.replace("HiggsAnalysis/TriggerEfficiency/test/../../../","")

                if os.path.exists(macroPath):
                    ROOT.gROOT.LoadMacro(macroPath+"+")
                    print "Loading",macroPath
                else:
                    print macroPath,"not found, exiting.."
                    sys.exit()

            for selection in offlineSelections:

                pythonWriter.SaveOfflineSelection(selection)
                doPlots(datasets,selection=selection,dataVsMc=True,pyScenario=pyScenario)

    pythonWriter.write("tauLegTriggerEfficiency_cff.py")

def namedselection(name,selection):
    namedSelection = []
    namedSelection.append(name)
    namedSelection.append(selection)
    return namedSelection

def doPlots(datasets,selection, dataVsMc=True, pyScenario="Unweighted"):

    selectionName    = selection[0]
    offlineSelection = selection[1]

    histograms.energyText = "7 TeV"

    offlineTauPt40 = "PFTauPt > 41"

    label = pyScenario

    signalTriggerMC = "L1JetEt > 52 && PFTau_matchedL1 >= 0"                           # L1
    signalTriggerMC+= "&& hasMatchedL2Jet == 1 && L2JetEt > 35"                        # L2
    signalTriggerMC+= "&& L25TauEt > 35 && L25Tau_TrackFinding && L25TauPt > 20"       # L25
    signalTriggerMC+= "&& primaryVertexIsValid && L25TauIsoChargedHadrCandPtMax < 1.0" # L3

    if pyScenario== "2011A_RR1":
        lumi = 1197
        #label = "L1_SingleTauJet52 OR L1_SingleJet68 + HLT_IsoPFTau35_Trk20_MET45 (Run2011A)"
        runMin = 160404
        runMax = 167913
        offlineTriggerData = "((HLT_IsoMu17_v5 || HLT_IsoMu17_v6 || HLT_IsoMu17_v8) && MuonPt > 17)" # runs 160404-165633, unprescaled
        offlineTriggerData += "|| ((HLT_IsoMu17_v9 || HLT_IsoMu17_v11) && MuonPt > 17)"              # runs 165970-167913, PRESCALED
        offlineTriggerMc = "HLT_IsoMu17_v14 && MuonPt > 17"
        signalTriggerData = "((L1JetEt>52 && L1JetIsTau) || (L1JetEt>68 && !L1JetIsTau)) && PFTau_matchedL1 >= 0"
#        signalTriggerData = "(L1TauVeto==0 && L1IsolationRegions_2GeV>=7 && L1JetEt>52) || (!(L1TauVeto==0 && L1IsolationRegions_2GeV>=7) && L1JetEt > 68)"   # L1
        signalTriggerData+= "&& hasMatchedL2Jet == 1 && L2JetEt > 35"         # L2
        signalTriggerData+= "&& L25TauEt > 35 && L25Tau_TrackFinding && L25TauPt > 20" # L25
        signalTriggerData+= "&& primaryVertexIsValid && L25TauIsoChargedHadrCandPtMax < 1.0 && L25TauIsoGammaCandEtMax < 1.5" # L3
        l1TriggerName  = ""
        hltTriggerName = "HLT_IsoPFTau35_Trk20"

    elif pyScenario== "2011A_RR2":
        lumi = 870.119
        #label = "L1_Jet52_Central + HLT_IsoPFTau35_Trk20_MET60 (Run2011A)"
        runMin = 170722
        runMax = 173198
        offlineTriggerData = "HLT_IsoMu17_v13 && MuonPt > 17"# runs 170722-172619, PRESCALED
        offlineTriggerMc = "HLT_IsoMu17_v14 && MuonPt > 17"
        signalTriggerData = "L1JetEt > 52 && PFTau_matchedL1 >= 0"
#        signalTriggerData = "L1JetEt > 52 && L1MET > 30 && PFTau_matchedL1 >= 0"                      # L1
        signalTriggerData+= "&& hasMatchedL2Jet == 1 && L2JetEt > 35"         # L2
        signalTriggerData+= "&& L25TauEt > 35 && L25Tau_TrackFinding && L25TauPt > 20" # L25
        signalTriggerData+= "&& primaryVertexIsValid && L25TauIsoChargedHadrCandPtMax < 1.0 && L25TauIsoGammaCandEtMax < 1.5" # L3
        l1TriggerName  = ""
        hltTriggerName = "HLT_IsoPFTau35_Trk20"

    elif pyScenario== "2011A_RR3":
        lumi = 265.715
        #label = "L1_Jet52_Central + HLT_MediumIsoPFTau35_Trk20_MET60 (Run2011A)"
        runMin = 173236
        runMax = 175770
        offlineTriggerData = "HLT_IsoMu20_v9 && MuonPt > 20"
        offlineTriggerMc = "HLT_IsoMu17_v14 && MuonPt > 17"
        signalTriggerData = "L1JetEt > 52 && PFTau_matchedL1 >= 0"                      # L1
        signalTriggerData+= "&& hasMatchedL2Jet == 1 && L2JetEt > 35"         # L2
        signalTriggerData+= "&& L25TauEt > 35 && L25Tau_TrackFinding && L25TauPt > 20" # L25
        signalTriggerData+= "&& primaryVertexIsValid && L25TauIsoChargedHadrCandPtMax < 1.0" # L3
        l1TriggerName  = ""
        hltTriggerName = "HLT_MediumIsoPFTau35_Trk20"

    elif pyScenario== "2011A":
        lumi = 2332.834
        runMin = 160404
        runMax = 173692
        offlineTriggerData = "(((HLT_IsoMu17_v5 || HLT_IsoMu17_v6 || HLT_IsoMu17_v8) && MuonPt > 17)"
        offlineTriggerData += "|| ((HLT_IsoMu17_v9 || HLT_IsoMu17_v11) && MuonPt > 17)"
        offlineTriggerData += "|| (HLT_IsoMu17_v13 && MuonPt > 17)"
        offlineTriggerData += "|| (HLT_IsoMu20_v9 && MuonPt > 20))"
        offlineTriggerMc = "HLT_IsoMu17_v14 && MuonPt > 17"
        signalTriggerData = "L1JetEt > 52 && PFTau_matchedL1 >= 0"                      # L1
        signalTriggerData+= "&& hasMatchedL2Jet == 1 && L2JetEt > 35"         # L2
        signalTriggerData+= "&& L25TauEt > 35 && L25Tau_TrackFinding && L25TauPt > 20" # L25
        signalTriggerData+= "&& primaryVertexIsValid && L25TauIsoChargedHadrCandPtMax < 1.0 && L25TauIsoGammaCandEtMax < 1.5" # L3
        l1TriggerName  = ""
        hltTriggerName = "HLT_IsoPFTau35_Trk20"

    elif pyScenario== "2011B": # Run2011B-Tau-PromptSkim-v1 (175860-180252)
        lumi = 2762
        label = "2011B"
####        runMin = 175860 # 2011B
#### Merged runrange 175860-180252 with runrange 173236-175860 to approximate 173236-175860 efficiency with 175860-180252 efficiency.
#### The error should be small. Reason: too low statistics for an efficiency estimate for runrange 173236-175860.
#### 20.6.2012/S.Lehti 
####        runMin = 173236
        runMin = 175832
        runMax = 180252
        offlineTriggerData = "(HLT_IsoMu17_v14 || HLT_IsoMu15_L1ETM20_v3 || HLT_IsoMu15_L1ETM20_v4) && MuonPt > 15"
#HLT_IsoMu17_v14 && MuonPt > 17"
        offlineTriggerMc = "(HLT_IsoMu17_v14 || HLT_IsoMu15_eta2p1_v1) && MuonPt > 17"
        signalTriggerData = "L1JetEt > 52 && PFTau_matchedL1 >= 0"# L1MET > 30"             # L1
        signalTriggerData+= "&& hasMatchedL2Jet == 1 && L2JetEt > 35"                        # L2
        signalTriggerData+= "&& L25TauEt > 35 && L25Tau_TrackFinding && L25TauPt > 20"       # L25
        signalTriggerData+= "&& primaryVertexIsValid && L25TauIsoChargedHadrCandPtMax < 1.0" # L3
        l1TriggerName  = ""
        hltTriggerName = "HLT_MediumIsoPFTau35_Trk20"

    elif pyScenario== "2011AB":
        lumi = 5095
        label = "2011AB"
        runMin = 160404
        runMax = 180252
        offlineTriggerData = "(HLT_IsoMu17_v14 || HLT_IsoMu15_L1ETM20_v3 || HLT_IsoMu15_L1ETM20_v4) && MuonPt > 15"
        offlineTriggerMc = "(HLT_IsoMu17_v14 || HLT_IsoMu15_eta2p1_v1) && MuonPt > 17"
        signalTriggerData = "L1JetEt > 52 && PFTau_matchedL1 >= 0"# L1MET > 30"             # L1                                            
        signalTriggerData+= "&& hasMatchedL2Jet == 1 && L2JetEt > 35"                        # L2                                           
        signalTriggerData+= "&& L25TauEt > 35 && L25Tau_TrackFinding && L25TauPt > 20"       # L25                                          
        signalTriggerData+= "&& primaryVertexIsValid && L25TauIsoChargedHadrCandPtMax < 1.0" # L3                                           
        l1TriggerName  = ""
        hltTriggerName = "HLT_MediumIsoPFTau35_Trk20"

    elif pyScenario == "Unweighted":
        lumi =  1
        runMin = 0
        runMax = 999999999
        offlineTriggerMc = "(HLT_IsoMu17_v14 || HLT_IsoMu15_eta2p1_v1) && MuonPt > 17"
        offlineTriggerData   = offlineTriggerMc
        signalTriggerData = signalTriggerMC
        l1TriggerName  = ""
        hltTriggerName = "HLT_MediumIsoPFTau35_Trk20"

    else:
        raise Exception("Invalid run range %s" % pyScenario)


#    signalTriggerData += " && PFTau_matchedHLTObject"
#    signalTriggerMC   += " && PFTau_matchedHLTObject"

    runs = "run >= %i && run <= %i"%(runMin,runMax)
    runsText = "%s-%s"%(runMin,runMax)

    offlineSelection1 = offlineSelection
    offlineSelection2 = offlineSelection

    offlineTriggerData = "(%s) && %s" % (offlineTriggerData, runs)

    offlineSelection1 += "&& "+offlineTriggerData
    offlineSelection2 += "&& "+offlineTriggerMc

    triggerSelection1 = signalTriggerData
    triggerSelection2 = signalTriggerMC

    legend1 = "Data"
    legend2 = "MC"

    print "Offline selection for 1 (data/highPurity)", offlineSelection1
    print "Offline selection for 2 (MC/lowPurity)", offlineSelection2

    plotter = Plotter(datasets,plotDir,lumi)
    plotter.setLegends(legend1, legend2)
    plotter.setTriggers(True, l1TriggerName, hltTriggerName, l1TriggerName, hltTriggerName, runsText)

#    ptbins = [20, 30, 40, 50, 60, 80, 150]
    ptbins = [20, 30, 40, 50, 60, 150]

    prefix = "Data"+pyScenario+"_"
    prefix+="DataVsMC_"
    prefix+=selectionName+"_"

    mcWeight = None
    if pyScenario != "Unweighted":
        mcWeight = "pileupWeight_"+pyScenario+"(MCNPU)"
    print
    print "MC weight",pyScenario
    print

    # Efficiencies
    hnumpt = ROOT.TH1F("hnumpt", "hnumpt", len(ptbins)-1, array.array("d", ptbins))

    optspt = {"xmin": 20, "xmax": 150}
    xlabel = "#tau-jet p_{T} (GeV/c)"

    denom1 = offlineSelection1
    denom2 = offlineSelection2

    num1 = And(denom1,triggerSelection1)
    num2 = And(denom2,triggerSelection2)
    print "check3",triggerSelection1

    print "        denom1 =",denom1
    print "        denom2 =",denom2
    print "        num1   =",num1
    print "        num2   =",num2

    efficiency = plotter.plotEfficiency(prefix+"Tau3_L1HLT_PFTauPt", "PFTauPt>>hnumpt", num1, denom1, num2, denom2, mcWeight, opts=optspt, xlabel=xlabel, ylabel="HLT tau efficiency", fit=True, fitMin=20., fitMax=150., drawText=True, printResults=True)

    pythonWriter.addParameters(selectionName,plotDir,label,runsText,lumi,efficiency)
    pythonWriter.addMCParameters(selectionName,"Fall11_PU_"+pyScenario,efficiency)
    pythonWriter.setStatOption(plotter.statOption)

    print "\nPlotDir",plotDir


if __name__ == "__main__":
    main()
