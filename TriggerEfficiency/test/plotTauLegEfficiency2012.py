#!/usr/bin/env python

######################################################################
#
# The ntuple files should come from the TTEff2 code
#
# Needs ROOT >= 5.30 (for TEfficiency)
#
# Author: Matti Kortelainen
# Modified 18052012/S.Lehti
# Modified 20062012/S.Lehti
#
######################################################################

import os
import array
import re
import sys

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
from Plotter import Plotter

#highPurity = True 
highPurity = False


pythonWriter = PythonWriter("tauLegEfficiency")

def usage():
    print "\n"
    print "### Usage:   "+sys.argv[0]+" <multicrab dir>\n"
    print "\n"
    sys.exit()

analysis = "analysis"
counters = analysis+"/counters"

plotDir = "TauLeg2012"


def main():
    if len(sys.argv) < 2:
        usage()

    pythonWriter.setInput(sys.argv[1])

#    datasets = dataset.getDatasetsFromMulticrabCfg(cfgfile=os.path.join(sys.argv[1], "multicrab.cfg"), weightedCounters=False)
    datasets = dataset.getDatasetsFromMulticrabCfg(cfgfile=os.path.join(sys.argv[1], "multicrab.cfg"), weightedCounters=False, includeOnlyTasks="TauPlusX_")
    datasetsDYMC = dataset.getDatasetsFromMulticrabCfg(cfgfile=os.path.join(sys.argv[1], "multicrab.cfg"), weightedCounters=False, includeOnlyTasks="DYToTauTau_")
    datasetsMC = dataset.getDatasetsFromMulticrabCfg(cfgfile=os.path.join(sys.argv[1], "multicrab.cfg"), weightedCounters=False, excludeTasks="TauPlusX_|DYToTauTau_")

    if highPurity:
        datasets.extend(datasetsDYMC)
    else:
        datasets.extend(datasetsMC)

    for d in datasets.getAllDatasets():
        #print d.name
        d.info["energy"] = "8"
    xsect.setBackgroundCrossSections(datasets,doWNJetsWeighting=False)
    datasets.loadLuminosities()

#    datasets.mergeData()
#    datasets.merge("MC", ["DYToTauTau"], keepSources=True)

    style = tdrstyle.TDRStyle()

    histograms.createLegend.moveDefaults(dh=-0.2)

    puWeights = []
    puWeights.append("pileupWeight_2012ABCD.C")
    puWeights.append("pileupWeight_2012ABC.C")
    puWeights.append("pileupWeight_2012AB.C")
    puWeights.append("pileupWeight_2012A.C")
    puWeights.append("pileupWeight_2012B.C")
    puWeights.append("pileupWeight_2012C.C")
    puWeights.append("pileupWeight_2012D.C")
    puWeights.append("pileupWeight_Unweighted.C")

    puWeightPath = "src/HiggsAnalysis/TriggerEfficiency/test"


    global plotDir
    if highPurity:
        dataset._optionDefaults["input"] = "histograms-*-highpurity.root"
        plotDir += "_highPurity"
    else:
        dataset._optionDefaults["input"] = "histograms-*-lowpurity.root"
        plotDir += "_lowPurity"
    

    ### Offline selection definition
    """
    offlineSelection = "PFTauPt > 20 && abs(PFTauEta) < 2.1"
    offlineSelection += "&& PFTauLeadChargedHadrCandPt > 20"
    offlineSelection += "&& PFTauProng == 1"
#    offlineSelection += "&& PFTau_againstElectronMedium > 0.5 && PFTau_againstMuonTight > 0.5"
    offlineSelection += "&& PFTau_againstElectronMVA > 0.5 && PFTau_againstMuonTight > 0.5"
#    offlineSelection += "&& byTightIsolation > 0.5"
#    offlineSelection += "&& byVLooseCombinedIsolationDeltaBetaCorr > 0.5"
#    offlineSelection += "&& byLooseCombinedIsolationDeltaBetaCorr > 0.5"
    offlineSelection += "&& PFTau_byMediumCombinedIsolationDeltaBetaCorr > 0.5"
    offlineSelection += "&& MuonTauInvMass < 80"
    """
    tauIDdiscriminators           = []
    againstMuonDiscriminators     = []
    againstElectronDiscriminators = []

    tauIDdiscriminators.append("byLooseCombinedIsolationDeltaBetaCorr3Hits")
    tauIDdiscriminators.append("byMediumCombinedIsolationDeltaBetaCorr3Hits")
    tauIDdiscriminators.append("byTightCombinedIsolationDeltaBetaCorr3Hits")

    againstMuonDiscriminators.append("againstMuonMedium2")
    againstMuonDiscriminators.append("againstMuonTight2")

    againstElectronDiscriminators.append("againstElectronMediumMVA3")
    againstElectronDiscriminators.append("againstElectronTightMVA3")
    againstElectronDiscriminators.append("againstElectronVTightMVA3")

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

                if highPurity:
                    # (p4+k4).M() = sqrt(2*|p3||k3|-2*p3 dot k3)
                    muTauInvMass = "sqrt(2*(sqrt(MuonPt*TMath::Cos(MuonPhi)*MuonPt*TMath::Cos(MuonPhi)+MuonPt*TMath::Sin(MuonPhi)*MuonPt*TMath::Sin(MuonPhi)+MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta)))*MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta))))*sqrt(PFTauPt*TMath::Cos(PFTauPhi)*PFTauPt*TMath::Cos(PFTauPhi)+PFTauPt*TMath::Sin(PFTauPhi)*PFTauPt*TMath::Sin(PFTauPhi)+PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta)))*PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta))))-MuonPt*TMath::Cos(MuonPhi)*PFTauPt*TMath::Cos(PFTauPhi)-MuonPt*TMath::Sin(MuonPhi)*PFTauPt*TMath::Sin(PFTauPhi)-MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta)))*PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta)))))"
                    offlineSelectionHPlus += "&& "+muTauInvMass+" < 80"
                    muMetMt = "sqrt( 2 * MuonPt * PFMET_ET * (1-cos(MuonPhi-PFMET_phi)) )"
                    muMetMtCut = "&& "+muMetMt+" < 40"
                    offlineSelectionHPlus += muMetMtCut
    
                offlineSelection = offlineSelectionHPlus
                """
                offlineSelectionMediumMedium = offlineSelectionHPlusBase
                offlineSelectionMediumMedium+= "&& PFTau_againstElectronMedium > 0.5"
                offlineSelectionMediumMedium+= "&& PFTau_byMediumCombinedIsolationDeltaBetaCorr > 0.5"

                offlineSelectionMediumMVA = offlineSelectionHPlusBase
                offlineSelectionMediumMVA+= "&& PFTau_againstElectronMVA > 0.5"
                offlineSelectionMediumMVA+= "&& PFTau_byMediumCombinedIsolationDeltaBetaCorr > 0.5"

                offlineSelectionLooseMedium = offlineSelectionHPlusBase
                offlineSelectionLooseMedium+= "&& PFTau_againstElectronMedium > 0.5"
                offlineSelectionLooseMedium+= "&& PFTau_byLooseCombinedIsolationDeltaBetaCorr > 0.5"

                offlineSelectionLooseMVA = offlineSelectionHPlusBase
                offlineSelectionLooseMVA+= "&& PFTau_againstElectronMVA > 0.5"
                offlineSelectionLooseMVA+= "&& PFTau_byLooseCombinedIsolationDeltaBetaCorr > 0.5"

                #### W(taunu)H(bb) analysis Segala, Zenz, Narain

                offlineSelectionWtaunuHbb = "PFTauPt > 20 && abs(PFTauEta) < 2.1"
                offlineSelectionWtaunuHbb += "&& PFTauLeadChargedHadrCandPt > 20"
                offlineSelectionWtaunuHbb += "&& PFTau_againstElectronLoose > 0.5 && PFTau_againstMuonTight > 0.5"
                offlineSelectionWtaunuHbb += "&& PFTau_byLooseCombinedIsolationDeltaBetaCorr > 0.5"
                offlineSelectionWtaunuHbb += "&& PFTau_decayModeFinding > 0.5"
                """

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
                doPlots(datasets,selection=selection,pyScenario=pyScenario)

    pythonWriter.write(os.path.join(plotDir,"tauLegTriggerEfficiency2012_cff.py"))

def namedselection(name,selection):
    namedSelection = []
    namedSelection.append(name)
    namedSelection.append(selection)
    return namedSelection

def doPlots(datasets, selection, pyScenario="Unweighted"):

    selectionName    = selection[0]
    offlineSelection = selection[1]

    histograms.energyText = "8 TeV"

    offlineTauPt40 = "PFTauPt > 41"

    label = pyScenario

    if pyScenario == "2012A":
        lumi = 697.308
        runMin = 190456
        runMax = 193621
        offlineTriggerData = "(HLT_IsoMu15_eta2p1_L1ETM20_v3 > 0.5 || HLT_IsoMu15_eta2p1_L1ETM20_v4 > 0.5) && MuonPt > 15"
        offlineTriggerMc   = "HLT_IsoMu15_eta2p1_L1ETM20_v5 > 0.5 && MuonPt > 15"
        signalTriggerData  = "(HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v2 > 0.5 || HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v3 > 0.5 || HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v4 > 0.5)"
        signalTriggerMC    = "HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v6 > 0.5"

    elif pyScenario == "2012B":
        lumi = 4428
        runMin = 193834
        runMax = 196531
        offlineTriggerData = "HLT_IsoMu15_eta2p1_L1ETM20_v5 && MuonPt > 15"
        offlineTriggerMc   = "HLT_IsoMu15_eta2p1_L1ETM20_v5 && MuonPt > 15"
        signalTriggerData  = "HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v6"
        signalTriggerMC    = "HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v6 > 0.5"

    elif pyScenario == "2012C":
        lumi = 6892
        runMin = 198022
        runMax = 203742
        offlineTriggerData = "HLT_IsoMu15_eta2p1_L1ETM20_v6 && MuonPt > 15"
        offlineTriggerMc   = "HLT_IsoMu15_eta2p1_L1ETM20_v5 && MuonPt > 15"
        signalTriggerData  = "(HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v7 || HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v9 || HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v10)"
        signalTriggerMC    = "HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v6 > 0.5"

    elif pyScenario == "2012D":
        lumi =  7274
        runMin =202807
        runMax = 208686
        offlineTriggerData = "HLT_IsoMu15_eta2p1_L1ETM20_v7 && MuonPt > 15"
        offlineTriggerMc   = "HLT_IsoMu15_eta2p1_L1ETM20_v5 && MuonPt > 15"
        signalTriggerData  = "HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v10"
        signalTriggerMC    = "HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v6 > 0.5"

    elif pyScenario == "2012AB":
        lumi =  5126
        runMin = 190456
        runMax = 196531
        offlineTriggerData = "(HLT_IsoMu15_eta2p1_L1ETM20_v3 || HLT_IsoMu15_eta2p1_L1ETM20_v4 || HLT_IsoMu15_eta2p1_L1ETM20_v5) && MuonPt > 15"
        offlineTriggerMc   = "HLT_IsoMu15_eta2p1_L1ETM20_v5 && MuonPt > 15"
        signalTriggerData  = "(HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v2 || HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v3 || HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v4 || HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v6)"
        signalTriggerMC    = "HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v6 > 0.5"

    elif pyScenario == "2012ABC":
        lumi =  11736
        runMin = 190456
        runMax = 202585
        offlineTriggerData = "(HLT_IsoMu15_eta2p1_L1ETM20_v3 || HLT_IsoMu15_eta2p1_L1ETM20_v4 || HLT_IsoMu15_eta2p1_L1ETM20_v5 || HLT_IsoMu15_eta2p1_L1ETM20_v6) && MuonPt > 15"
        offlineTriggerMc   = "HLT_IsoMu15_eta2p1_L1ETM20_v5 && MuonPt > 15"
        signalTriggerData  = "(HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v2 || HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v4 || HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v6 || HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v7 || HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v9)"
        signalTriggerMC    = "HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v6 > 0.5"

    elif pyScenario == "2012ABCD":
        lumi =  19296
        runMin = 190456
        runMax = 208686
        offlineTriggerData = "(HLT_IsoMu15_eta2p1_L1ETM20_v3 || HLT_IsoMu15_eta2p1_L1ETM20_v4 || HLT_IsoMu15_eta2p1_L1ETM20_v5 || HLT_IsoMu15_eta2p1_L1ETM20_v6 || HLT_IsoMu15_eta2p1_L1ETM20_v7) && MuonPt > 15"
        offlineTriggerMc   = "HLT_IsoMu15_eta2p1_L1ETM20_v5 && MuonPt > 15"
        signalTriggerData  = "(HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v2 || HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v4 || HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v6 || HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v7 || HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v9 || HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v10)"
        signalTriggerMC    = "HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v6 > 0.5"

    elif pyScenario == "Unweighted":
        lumi =  1
        runMin = 0
        runMax = 999999999
        offlineTriggerMc   = "HLT_IsoMu15_eta2p1_L1ETM20_v5 && MuonPt > 15"
        offlineTriggerData = offlineTriggerMc
        signalTriggerMC    = "HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v6 > 0.5"
        signalTriggerData = signalTriggerMC

    else:
        raise Exception("Invalid run range %s" % pyScenario)

    signalTriggerData += " && PFTau_matchedHLTObject"
    signalTriggerMC   += " && PFTau_matchedHLTObject"

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

    l1TriggerName = ""
    hltTriggerName = "LooseIsoPFTau35_Trk20_Prong1"

    print "Offline selection for 1 (data/highPurity)", offlineSelection1
    print "Offline selection for 2 (MC/lowPurity)", offlineSelection2

#    plotDir = "TauLeg"
#    plotDir += str(pyScenario[:4])

    plotter = Plotter(datasets,plotDir,lumi)
    plotter.setLegends(legend1, legend2)
    plotter.setTriggers(True, l1TriggerName, hltTriggerName, l1TriggerName, hltTriggerName, runsText)

#    ptbins = [20, 30, 41, 50, 60, 70, 80, 100, 120, 140, 160, 180, 200, 300, 400, 500]
    ptbins = [20, 25, 29, 33, 37, 41, 45, 50, 55, 60, 70, 80, 100, 150, 200]
#    ptbins = [20, 30, 41, 50, 60, 70, 80, 100, 150]
    etabins = [-2.1, -1.05, 0, 1.05, 2.1]
    vtxbins = [0,5,10,15,20,25,30,35]
#    ptbins2 = [0, 10, 20, 30, 40, 50, 60, 70, 80, 100, 120, 140, 160, 180, 200]

    prefix = "Data"+pyScenario+"_"
    prefix+="DataVsMC_"
    prefix+=selectionName+"_"

    mcWeight = None
    if pyScenario != "Unweighted":
        mcWeight = "pileupWeight_"+pyScenario+"(MCNPU)"
    print
    print "MC weight",pyScenario
    print




    # Distributions
    ROOT.gStyle.SetErrorX(0.5)
    sel1 = offlineSelection1+"&&"+offlineTauPt40
    sel2 = offlineSelection2+"&&"+offlineTauPt40
#    plotter.plotVariable(prefix+"MuonTauVisMass", "MuonTauInvMass>>foo1(9,0,180)", sel1, sel2, mcWeight, xlabel="m(#mu, #tau) (GeV/c^{2}")
#    plotter.plotVariable(prefix+"MuonMetTransverseMass", muMetMt+">>foo2(10,0,100)", sel1, sel2, mcWeight, xlabel="m_{T}(#mu, E_{T}^{miss}) (GeV/c^{2})")
#    plotter.plotVariable(prefix+"N_Vertices", "numGoodOfflinePV>>foo3(35,0,35)", sel1, sel2, xlabel="Number of good vertices")



    # Efficiencies
    hnumpt = ROOT.TH1F("hnumpt", "hnumpt", len(ptbins)-1, array.array("d", ptbins))
    hnumvtx = ROOT.TH1F("hnumvtx", "hnumvtx", len(vtxbins)-1, array.array("d", vtxbins))

    #hnumpt.Sumw2()
    optspt = {"xmin": 20, "xmax": 150}
    xlabel = "#tau-jet p_{T} (GeV/c)"

    # Level-1
    denom1 = offlineSelection1
    denom2 = offlineSelection2

    num1 = And(denom1,triggerSelection1)
    num2 = And(denom2,triggerSelection2)

    efficiency = plotter.plotEfficiency(prefix+"Tau3_L1HLT_PFTauPt", "PFTauPt>>hnumpt", num1, denom1, num2, denom2, mcWeight, opts=optspt, xlabel=xlabel, ylabel="HLT tau efficiency", fit=True, fitMin=20., fitMax=150., drawText=True, printResults=True)
    """
    denom1pt = And(denom1, offlineTauPt40)
    denom2pt = And(denom2, offlineTauPt40)
    num1pt = And(num1, offlineTauPt40)
    num2pt = And(num2, offlineTauPt40)


    effVsNvtx = plotter.plotEfficiency(prefix+"Tau4_L1HLT_NVtx", "numGoodOfflinePV>>hnumvtx", num1pt, denom1pt, num2pt, denom2pt, mcWeight, opts=optspt, xlabel="Number of good vertices", ylabel="Level-1 + HLT tau efficiency", fit=False, drawText=True, printResults=True)    
    """

    #dumpParameters(plotDir,label,runsText,lumi,efficiency)
    pythonWriter.addParameters(selectionName,plotDir,label,runsText,lumi,efficiency)
    pythonWriter.addMCParameters(selectionName,"Summer12_PU_"+pyScenario,efficiency)
    
    print "\nPlotDir",plotDir


if __name__ == "__main__":
    main()
