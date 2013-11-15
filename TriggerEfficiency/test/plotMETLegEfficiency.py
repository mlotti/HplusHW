#!/usr/bin/env python

import ROOT
ROOT.gROOT.SetBatch(True)

import os
import re
import sys
import array


import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.cutstring import * # And, Not, Or

from PythonWriter import PythonWriter
pythonWriter = PythonWriter("metLegTriggerEfficiency2012")
from Plotter import Plotter

METCorrection = ""
#METCorrection = "type1"

def usage():
    print "\n"
    print "### Usage:   "+sys.argv[0]+" <multicrab dir>\n"
    print "\n"
    sys.exit()

analysis = "analysis"
counters = analysis+"/counters"

plotDir = "METLeg2012"
pythonWriter.setPlotDir(plotDir)

def L1ETMCorrection(L1ETM,caloMETnoHF,caloMETnoHFresidualCorrected):
    R = 0.9322
    H = -0.1172+0.0499*ln(caloMETnoHF)
    K = 0.6693

    L1etmScaleCorr = L1ETM*caloMETnoHFresidualCorrected/caloMETnoHF*R
    correctedL1ETM = L1etmScaleCorr + H*(L1etmScaleCorr - K*caloMETnoHF)

    return correctedL1ETM

def main():
    if len(sys.argv) < 2:
        usage()

    pythonWriter.setInput(sys.argv[1])

#    datasets = dataset.getDatasetsFromMulticrabCfg(cfgfile=os.path.join(sys.argv[1], "multicrab.cfg"), weightedCounters=False)
    datasets = dataset.getDatasetsFromMulticrabCfg(cfgfile=os.path.join(sys.argv[1], "multicrab.cfg"), weightedCounters=False, includeOnlyTasks="Tau_|TauParked_")
#    datasets = dataset.getDatasetsFromMulticrabCfg(cfgfile=os.path.join(sys.argv[1], "multicrab.cfg"), counters=counters, doEraReplace=False, weightedCounters=False, includeOnlyTasks="_2012C_")
    datasetsMC = dataset.getDatasetsFromMulticrabCfg(cfgfile=os.path.join(sys.argv[1], "multicrab.cfg"), weightedCounters=False, excludeTasks="Tau_|TauParked_")
#    datasetsMC = dataset.getDatasetsFromMulticrabCfg(cfgfile=os.path.join(sys.argv[1], "multicrab.cfg"), weightedCounters=False, includeOnlyTasks="TTJet")
#    datasetsMC = dataset.getDatasetsFromMulticrabCfg(cfgfile=os.path.join(sys.argv[1], "multicrab.cfg"), weightedCounters=False, includeOnlyTasks="QCD_")
#    datasetsMC = dataset.getDatasetsFromMulticrabCfg(cfgfile=os.path.join(sys.argv[1], "multicrab.cfg"), weightedCounters=False, excludeTasks=["Tau_","TauParked_","QCD_"])
#    datasetsMC = dataset.getDatasetsFromMulticrabCfg(cfgfile=os.path.join(sys.argv[1], "multicrab.cfg"), counters=counters, doEraReplace=False, weightedCounters=False, includeOnlyTasks="QCD_Pt120|QCD_Pt170")

    datasets.extend(datasetsMC)
    datasets.remove(filter(lambda name: "WJets" in name, datasets.getAllDatasetNames()))

    for d in datasets.getAllDatasets():
#        print d.getName()
#        d.info["energy"] = "7"
        d.info["energy"] = "8"
    xsect.setBackgroundCrossSections(datasets,doWNJetsWeighting=False)
    datasets.loadLuminosities()                                                                                                            
#    plots.mergeRenameReorderForDataMC(datasets)

#    datasets.remove(filter(lambda name: "Tau_" in name, datasets.getAllDatasetNames()))

#    for d in datasets.getAllDatasets():
#        print d.getName()


#    datasets.mergeData()

    style = tdrstyle.TDRStyle()

    puWeights = []
#    puWeights.append("pileupWeight_2011AB.C")
#    puWeights.append("pileupWeight_2011A.C")
#    puWeights.append("pileupWeight_2011B.C")

    puWeights.append("pileupWeight_2012A.C")
    puWeights.append("pileupWeight_2012B.C")
    puWeights.append("pileupWeight_2012C.C")
    puWeights.append("pileupWeight_2012D.C")
    puWeights.append("pileupWeight_2012AB.C")
    puWeights.append("pileupWeight_2012ABC.C")
    puWeights.append("pileupWeight_2012ABCD.C")
    puWeights.append("pileupWeight_Unweighted.C")

    puWeightPath = "src/HiggsAnalysis/TriggerEfficiency/test"

    """
    offlineTauSelection = "PFTauPt > 41 && abs(PFTauEta) < 2.1"
    
    offlineTauSelection += "&& PFTauLeadChargedHadrCandPt > 20"
    offlineTauSelection += "&& PFTauProng == 1"
    offlineTauSelection += "&& PFTau_decayModeFinding > 0.5"
#    offlineTauSelection += "&& PFTau_byMediumCombinedIsolationDeltaBetaCorr3Hits > 0.5"
    offlineTauSelection += "&& PFTau_byLooseCombinedIsolationDeltaBetaCorr3Hits > 0.5"
#    offlineTauSelection += "&& PFTau_byVLooseCombinedIsolationDeltaBetaCorr > 0.5"
#    offlineTauSelection += "&& PFTau_byLooseCombinedIsolationDeltaBetaCorr > 0.5"
#    offlineTauSelection += "&& PFTau_byMediumCombinedIsolationDeltaBetaCorr > 0.5"
#    offlineTauSelection += "&& PFTau_byLooseIsolationMVA2 > 0.5"
#    offlineTauSelection += "&& PFTau_byMediumIsolationMVA2 > 0.5"
    offlineTauSelection += "&& PFTau_againstElectronMediumMVA3 > 0.5 && PFTau_againstMuonTight2 > 0.5"

    offlineJetSelection = "PFJetPt > 0"
#    offlineJetSelection+= "&& PFJetPUIDloose"
#    offlineJetSelection+= "&& PFJetPUIDmedium"
    offlineJetSelection+= "&& PFJetPUIDtight"

    offlineSelection = "Sum$(%s) >= 1"%offlineTauSelection
    offlineSelection = And(offlineSelection,"Sum$(%s) >= 3+Sum$(%s && PFTauJetMinDR < 0.5)"%(offlineJetSelection,offlineTauSelection))
    offlineSelection += "&& hPlusGlobalElectronVetoFilter > 0.5 && hPlusGlobalMuonVetoFilter > 0.5"

    offlineSelections = []
    offlineSelections.append(namedselection("metLegEfficiency",offlineSelection))
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
                offlineTauSelection = "PFTauPt > 41 && abs(PFTauEta) < 2.1"
                offlineTauSelection += "&& PFTauLeadChargedHadrCandPt > 20"
                offlineTauSelection += "&& PFTauProng == 1"
                offlineTauSelection += "&& PFTau_decayModeFinding > 0.5"
                offlineTauSelection+= "&& PFTau_%s > 0.5"%eleD
                offlineTauSelection+= "&& PFTau_%s > 0.5"%muonD
                offlineTauSelection+= "&& PFTau_%s > 0.5"%tauD

                offlineJetSelection = "PFJetPt > 0"
                #    offlineJetSelection+= "&& PFJetPUIDloose"
                #    offlineJetSelection+= "&& PFJetPUIDmedium"
                offlineJetSelection+= "&& PFJetPUIDtight"

                offlineSelection = "Sum$(%s) >= 1"%offlineTauSelection
                offlineSelection = And(offlineSelection,"Sum$(%s) >= 3+Sum$(%s && PFTauJetMinDR < 0.5)"%(offlineJetSelection,offlineTauSelection))
                offlineSelection += "&& hPlusGlobalElectronVetoFilter > 0.5 && hPlusGlobalMuonVetoFilter > 0.5"

                if len(againstElectronDiscriminators) + len(againstMuonDiscriminators) + len(tauIDdiscriminators) > 3:
                    offlineSelections.append(namedselection(tauD+"_"+muonD+"_"+eleD,offlineSelection))
                else:
                    offlineSelections.append(namedselection("loose",offlineSelection))


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

#                doPlots(datasets,selection=selection,dataVsMc=0,pyScenario=pyScenario)
                doPlots(datasets,selection=selection,dataVsMc=1,pyScenario=pyScenario)
#                doPlots(datasets,selection=selection,dataVsMc=2,pyScenario=pyScenario)
    pythonWriter.write("metLegTriggerEfficiency2011_cff.py")

def namedselection(name,selection):
    namedSelection = []
    namedSelection.append(name)
    namedSelection.append(selection)
    return namedSelection

def doPlots(datasets,selection, dataVsMc, pyScenario="Unweighted"):
    ### Offline selection definition
    selectionName    = selection[0]
    offlineSelection = selection[1]

    l1TriggerName1 = "Jet52_Central"
    hltTriggerName1 = "MediumIsoPFTau35_Trk20"

    if pyScenario== "2011A": # May10+Prompt-v4 (160431-167913)                                                                     
        lumi = 1197
        runs = "run >= 160404 && run <= 167913"
        runsText = "160404-167913"
        offlineTriggerData = "HLT_IsoPFTau35_Trk20_v2 || HLT_IsoPFTau35_Trk20_v3 || HLT_IsoPFTau35_Trk20_v4 || HLT_IsoPFTau35_Trk20_v6"
        offlineTriggerMc = "HLT_MediumIsoPFTau35_Trk20_v1"

    elif pyScenario== "2011AB": # Whole 2011 data                                                                                   
        lumi = 5094.834
#        runs = "run >= 160404 && run <= 180252"
#        runsText = "160404-180252"
#        runs = "run >= 170722 && run <= 180252"
#        runsText = "170722-180252"
	runs = "run >= 160431 && run <= 180252" # start run for embedding needs.. 15112013/SL
	runsText = "160431-180252"
        offlineTriggerData = "(HLT_IsoPFTau35_Trk20_v2 || HLT_IsoPFTau35_Trk20_v3 || HLT_IsoPFTau35_Trk20_v4 || HLT_IsoPFTau35_Trk20_v6)"
        offlineTriggerData += "|| (HLT_MediumIsoPFTau35_Trk20_v1 || HLT_MediumIsoPFTau35_Trk20_v5 || HLT_MediumIsoPFTau35_Trk20_v6)"
        offlineTriggerMc = "HLT_MediumIsoPFTau35_Trk20_v1"

    elif pyScenario== "2012A":

        lumi = 887.501000
        runs = "run >= 190456 && run <= 193621"
        runsText = "190456-193621"
        offlineTriggerData = "HLT_LooseIsoPFTau35_Trk20_Prong1_v2 || HLT_LooseIsoPFTau35_Trk20_Prong1_v3 || HLT_LooseIsoPFTau35_Trk20_Prong1_v4"
        offlineTriggerMc = "HLT_LooseIsoPFTau35_Trk20_Prong1_v6"

    elif pyScenario== "2012B":

        lumi = 4440.000000
        runs = "run >= 193833 && run <= 196531"
        runsText = "193833-196531"
        offlineTriggerData = "HLT_LooseIsoPFTau35_Trk20_Prong1_v6"
        offlineTriggerMc = "HLT_LooseIsoPFTau35_Trk20_Prong1_v6"

    elif pyScenario== "2012C":

        lumi = 6843.000000+281.454000
        runs = "run >= 198022 && run <= 203742"
        runsText = "198022-203742"
        offlineTriggerData = "HLT_LooseIsoPFTau35_Trk20_Prong1_v7 || HLT_LooseIsoPFTau35_Trk20_Prong1_v9 || HLT_LooseIsoPFTau35_Trk20_Prong1_v10"
        offlineTriggerMc = "HLT_LooseIsoPFTau35_Trk20_Prong1_v6"

    elif pyScenario== "2012D":

        lumi = 7318.000000
        runs = "run >= 203777 && run <= 208686"
        runsText = "203777-208686"
        offlineTriggerData = "HLT_LooseIsoPFTau35_Trk20_Prong1_v10"
        offlineTriggerMc = "HLT_LooseIsoPFTau35_Trk20_Prong1_v6"

    elif pyScenario== "2012AB":

        lumi = 887.501000+4440.000000
        runs = "run >= 190456 && run <= 196531"
        runsText = "190456-196531"
        offlineTriggerData = "HLT_LooseIsoPFTau35_Trk20_Prong1_v2 || HLT_LooseIsoPFTau35_Trk20_Prong1_v3 || HLT_LooseIsoPFTau35_Trk20_Prong1_v4 || HLT_LooseIsoPFTau35_Trk20_Prong1_v6"
        offlineTriggerMc = "HLT_LooseIsoPFTau35_Trk20_Prong1_v6"

    elif pyScenario== "2012ABC":

        lumi = 887.501000+4440.000000+6843.000000
        runs = "run >= 190456 && run <= 203742"
        runsText = "190456-203742"
        offlineTriggerData = "HLT_LooseIsoPFTau35_Trk20_Prong1_v2 || HLT_LooseIsoPFTau35_Trk20_Prong1_v3 || HLT_LooseIsoPFTau35_Trk20_Prong1_v4 || HLT_LooseIsoPFTau35_Trk20_Prong1_v6 || HLT_LooseIsoPFTau35_Trk20_Prong1_v7 || HLT_LooseIsoPFTau35_Trk20_Prong1_v9 || HLT_LooseIsoPFTau35_Trk20_Prong1_v10"
        offlineTriggerMc = "HLT_LooseIsoPFTau35_Trk20_Prong1_v6"

    elif pyScenario== "2012ABCD":

        lumi = 887.501000+4440.000000+6843.000000+281.454000+7318.000000
        runs = "run >= 190456 && run <= 208686"
        runsText = "190456-208686"
        offlineTriggerData = "HLT_LooseIsoPFTau35_Trk20_Prong1_v2 || HLT_LooseIsoPFTau35_Trk20_Prong1_v3 || HLT_LooseIsoPFTau35_Trk20_Prong1_v4 || HLT_LooseIsoPFTau35_Trk20_Prong1_v6 || HLT_LooseIsoPFTau35_Trk20_Prong1_v7 || HLT_LooseIsoPFTau35_Trk20_Prong1_v9 || HLT_LooseIsoPFTau35_Trk20_Prong1_v10"
        offlineTriggerMc = "HLT_LooseIsoPFTau35_Trk20_Prong1_v6"

    elif pyScenario == "Unweighted":

        lumi =  1
        runs = ""
        runsText = ""
        offlineTriggerMc = "HLT_LooseIsoPFTau35_Trk20_Prong1_v6"
        offlineTriggerData = offlineTriggerMc

    else:
        raise Exception("Invalid run range %s" % pyScenario)

    if not runs == "": 
        offlineTriggerData = "(%s) && %s" % (offlineTriggerData, runs)
#    offlineTriggerMc = "HLT_MediumIsoPFTau35_Trk20_v1"

#    offlineSelection1 = And(offlineSelection,offlineTriggerMc)
#    offlineSelection2 = And(offlineSelection,offlineTriggerData)

    L1ETMCut   = 40
    CaloMETCut = 60

    offlineSelection = And(offlineSelection,"L1MET>%s"%L1ETMCut)

    label = pyScenario

    if pyScenario[:4] == "2012":
        CaloMETCut = 70
        l1TriggerName1 = "ETM40"
        hltTriggerName1 = "LooseIsoPFTau35_Trk20_Prong1"

    if dataVsMc == 1:
        legend1 = "Data, trigger bit"
        legend2 = "MC, trigger bit"
        denom1 = And(offlineSelection,offlineTriggerData)
        denom2 = And(offlineSelection,offlineTriggerMc)
    elif dataVsMc == 2:
        legend1 = "Data, CaloMET>%s"%CaloMETCut
        legend2 = "MC, CaloMET>%s"%CaloMETCut
        denom1 = And(offlineSelection,offlineTriggerData)
        denom2 = And(offlineSelection,offlineTriggerMc)
    else:
        legend2 = "Data, CaloMET>%s"%CaloMETCut
        legend1 = "Data, trigger bit"
        denom1 = And(offlineSelection,offlineTriggerData)
        denom2 = denom1


#    plotDir = "METLeg"
#    plotDir += "McFall11"
####    plotDir += "RunRange%s" % pyScenario
#    plotDir += str(pyScenario[:4])

    ### Trigger selectiondefinitions                                                                                                
    # Default is for 2011B                                                                                                    
#    l1TriggerName1 = "Jet52_Central"
#    hltTriggerName1 = "MediumIsoPFTau35_Trk20"
    l1TriggerName2 = l1TriggerName1
    hltTriggerName2 = hltTriggerName1

    plotter = Plotter(datasets,plotDir,lumi) # FIXME
    plotter.setLegends(legend1, legend2)
    plotter.setTextPos(0.2,0.9,17,0.045)
    plotter.setTriggers(dataVsMc, l1TriggerName1, hltTriggerName1, l1TriggerName2, hltTriggerName2, runsText)

    ptbins  = [0, 20, 30, 40, 50, 60, 70, 80, 100, 120, 140, 160, 180, 200]
    etabins = [-2.1, -1.05, 0, 1.05, 2.1]
    vtxbins = [0,5,10,15,20,25,30,35]
    ptbins2 = [0, 10, 20, 30, 40, 50, 60, 70, 80, 100, 120, 140, 160, 180, 200]


    prefix = "Data"+pyScenario+"_"
    if dataVsMc == 1:
        prefix+="DataVsMC_"
    if dataVsMc == 2:
        prefix+="DataVsMCCaloMET_"
    prefix+=selectionName+"_"

    mcWeight = None
    if dataVsMc > 0 and pyScenario != "Unweighted":
        mcWeight = "pileupWeight_"+pyScenario+"(MCNPU)"
    print
    print "MC weight",pyScenario
    print

    """
    if pyScenario== "2011AB":
#        num2 = And(denom2,"(HLT_IsoPFTau35_Trk20_MET60_v2 || HLT_IsoPFTau35_Trk20_MET60_v3 || HLT_IsoPFTau35_Trk20_MET60_v4 || HLT_IsoPFTau35_Trk20_MET60_v6 || ((HLT_MediumIsoPFTau35_Trk20_MET60_v1 || HLT_MediumIsoPFTau35_Trk20_MET60_v5 || HLT_MediumIsoPFTau35_Trk20_MET60_v6) && L1MET>30) )")
        num1 = And(denom1,"(HLT_IsoPFTau35_Trk20_MET60_v2 || HLT_IsoPFTau35_Trk20_MET60_v3 || HLT_IsoPFTau35_Trk20_MET60_v4 || HLT_IsoPFTau35_Trk20_MET60_v6 || ((HLT_MediumIsoPFTau35_Trk20_MET60_v1 || HLT_MediumIsoPFTau35_Trk20_MET60_v5 || HLT_MediumIsoPFTau35_Trk20_MET60_v6)) )")
        num2 = And(denom2,"((HLT_IsoPFTau35_Trk20_v2 || HLT_IsoPFTau35_Trk20_v3 || HLT_IsoPFTau35_Trk20_v4 || HLT_IsoPFTau35_Trk20_v6) && CaloMET_ET>60) || ((HLT_MediumIsoPFTau35_Trk20_v1 || HLT_MediumIsoPFTau35_Trk20_v5 || HLT_MediumIsoPFTau35_Trk20_v6) && CaloMET_ET>60 && L1MET>36)")
        if dataVsMc > 0:
            num2 = And(denom1,"HLT_MediumIsoPFTau35_Trk20_MET60_v1")
    """

#    if pyScenario== "2012ABCD" or pyScenario== "2012ABC" or pyScenario== "2012AB" or pyScenario== "2012A" or pyScenario== "2012B" or pyScenario== "2012C" or pyScenario== "2012D":
    num1 = And(denom1,"(HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v2 || HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v3 || HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v4 || HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v6 || HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v7 || HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v9 || HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v10)")
    num2 = And(denom2,"CaloMET_ET>%s && L1MET>%s"%(CaloMETCut,L1ETMCut))
    if dataVsMc == 1:
        num2 = And(denom2,"HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v6 && L1MET>%s"%L1ETMCut)
    if dataVsMc == 2:
        num1 = And(denom1,"CaloMET_ET>%s && L1MET>%s"%(CaloMETCut,L1ETMCut))
        num2 = And(denom2,"CaloMET_ET>%s && L1MET>%s"%(CaloMETCut,L1ETMCut))

####        num2 = And(num2,"L1MET > %s"%(L1ETMCut/0.68))

    if pyScenario == "Unweighted":
        num1 = num2

    hnummet = ROOT.TH1F("hnummet", "hnummet", len(ptbins)-1, array.array("d", ptbins))
    hnumvtx = ROOT.TH1F("hnumvtx", "hnumvtx", len(vtxbins)-1, array.array("d", vtxbins))
    hl1etm = ROOT.TH1F("hl1etm", "hl1etm", len(ptbins2)-1, array.array("d", ptbins2))

    offlineMet50   = "PFMET"+METCorrection+"_ET > 50"

    denom1met = And(denom1, offlineMet50)
    denom2met = And(denom2, offlineMet50)
    num1met = And(num1, offlineMet50)
    num2met = And(num2, offlineMet50)

    print num1
    print denom1
    print num2
    print denom2

    xlabel = "MET (GeV)"
    if not METCorrection == "":
        xlabel = "Type1 MET (GeV)"

    opts2 = {"ymin": 0.0, "ymax": 1.5}

    efficiency = plotter.plotEfficiency(prefix+"MET", "PFMET"+METCorrection+"_ET>>hnummet", num1, denom1, num2, denom2, mcWeight, xlabel=xlabel,ylabel="Level-1 + HLT MET efficiency",opts2=opts2,moveLegend = {"dx": -0.55,"dy": -0.15,"dh": -0.1},drawText=True,printResults=True)
#    plotter.plotEfficiency(prefix+"METtype1", "PFMETtype1_ET>>hnummet", num1, denom1, num2, denom2, mcWeight, xlabel="MET (GeV)",ylabel="HLT MET efficiency",drawText=True,printResults=True)
####    plotter.plotEfficiency(prefix+"Nvtx", "numGoodOfflinePV>>hnumvtx", num1met, denom1met, num2met, denom2met, mcWeight, xlabel="Number of good vertices",printResults=False)

#    plotter.plotVariable(prefix+"L1ETM","L1MET>>hl1etm",denom1,denom2,xlabel="L1_ETM (GeV)",ylabel="Events")
#    plotter.plotVariable(prefix+"L1ETM","0.68*L1MET>>hl1etm",denom1,denom2,xlabel="L1_ETM (GeV)",ylabel="Events")

#    plotter.plotVariable(prefix+"CaloMET_ET","CaloMET_ET>>hl1etm",denom1,denom2,xlabel="CaloMET (GeV)",ylabel="Events")
#    plotter.plotVariable(prefix+"PFMET_ET","PFMET_ET>>hl1etm",denom1,denom2,xlabel="PFMET(RAW) (GeV)",ylabel="Events")
#    plotter.plotVariable(prefix+"PFMETtype1_ET","PFMETtype1_ET>>hl1etm",denom1,denom2,xlabel="PFMET(type1) (GeV)",ylabel="Events")

    pythonWriter.addParameters(selectionName,plotDir,label,runsText,lumi,efficiency)
    pythonWriter.addMCParameters(selectionName,"Summer12_PU_"+pyScenario,efficiency)

    print "\nPlotDir",plotDir


if __name__ == "__main__":
    main()
