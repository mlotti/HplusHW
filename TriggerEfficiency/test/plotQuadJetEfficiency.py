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
pythonWriter = PythonWriter("metLegEfficiency")

def usage():
    print "\n"
    print "### Usage:   "+sys.argv[0]+" <multicrab dir>\n"
    print "\n"
    sys.exit()

analysis = "analysis"
counters = analysis+"/counters"

def main():
    if len(sys.argv) < 2:
        usage()

    datasets = dataset.getDatasetsFromMulticrabCfg(cfgfile=os.path.join(sys.argv[1], "multicrab.cfg"), weightedCounters=False, includeOnlyTasks="SingleMu_")
    datasetsMC = dataset.getDatasetsFromMulticrabCfg(cfgfile=os.path.join(sys.argv[1], "multicrab.cfg"), weightedCounters=False, excludeTasks="SingleMu_")

    datasets.extend(datasetsMC)
#    datasets.remove(filter(lambda name: "WJets" in name, datasets.getAllDatasetNames()))

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
#    puWeights.append("pileupWeight_2012A.C")
#    puWeights.append("pileupWeight_2012B.C")
#    puWeights.append("pileupWeight_2012C.C")
#    puWeights.append("pileupWeight_2012D.C")
    puWeights.append("pileupWeight_2012ABCD.C")

    puWeightPath = "src/HiggsAnalysis/TriggerEfficiency/test"

    offlineTauSelection = "PFTauPt > 41 && abs(PFTauEta) < 2.1"
    offlineSelection = "Sum$(%s) >= 1"%offlineTauSelection
    offlineSelection = And(offlineSelection,"Sum$(PFJetPt > 0) >= 3+Sum$(%s && PFTauJetMinDR < 0.5)"%offlineTauSelection)
#    offlineSelection += "&& PFTau_againstElectronMVA > 0.5 && PFTau_againstMuonTight > 0.5"
#    offlineSelection += "&& PFTau_decayModeFinding > 0.5"
#    offlineSelection += "&& PFTau_byMediumCombinedIsolationDeltaBetaCorr > 0.5"
#    offlineSelection += "&& hPlusGlobalElectronVetoFilter > 0.5 && hPlusGlobalMuonVetoFilter > 0.5"

    offlineSelections = []
    offlineSelections.append(namedselection("metLegEfficiency",offlineSelection))

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
#                doPlots(datasets,selection=selection,dataVsMc=1,pyScenario=pyScenario)
                doPlots(datasets,selection=selection,dataVsMc=2,pyScenario=pyScenario)
    pythonWriter.write("metLegTriggerEfficiency2012_cff.py")

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
        label = "L1_SingleTauJet52 OR L1_SingleJet68 + HLT_IsoPFTau35_Trk20_MET45 (Run2011A)"
        runs = "run >= 160404 && run <= 167913"
        runsText = "160404-167913"
        offlineTriggerData = "HLT_IsoPFTau35_Trk20_v2 || HLT_IsoPFTau35_Trk20_v3 || HLT_IsoPFTau35_Trk20_v4 || HLT_IsoPFTau35_Trk20_v6"
        offlineTriggerMc = "HLT_MediumIsoPFTau35_Trk20_v1"

    elif pyScenario== "2011AB": # Whole 2011 data                                                                                   
        lumi = 5094.834
        label = "Dummy"
#        runs = "run >= 160404 && run <= 180252"
#        runsText = "160404-180252"
        runs = "run >= 170722 && run <= 180252"
        runsText = "170722-180252"
        offlineTriggerData = "(HLT_IsoPFTau35_Trk20_v2 || HLT_IsoPFTau35_Trk20_v3 || HLT_IsoPFTau35_Trk20_v4 || HLT_IsoPFTau35_Trk20_v6)"
        offlineTriggerData += "|| (HLT_MediumIsoPFTau35_Trk20_v1 || HLT_MediumIsoPFTau35_Trk20_v5 || HLT_MediumIsoPFTau35_Trk20_v6)"
        offlineTriggerMc = "HLT_MediumIsoPFTau35_Trk20_v1"

    elif pyScenario== "2012A":

        lumi = 697.308
        label = "Dummy"
        runs = "run >= 190456 && run <= 193621"
        runsText = "190456-193621"
        offlineTriggerData = "HLT_LooseIsoPFTau35_Trk20_Prong1_v2 || HLT_LooseIsoPFTau35_Trk20_Prong1_v3 || HLT_LooseIsoPFTau35_Trk20_Prong1_v4"
        offlineTriggerMc = "HLT_LooseIsoPFTau35_Trk20_Prong1_v6"

        l1TriggerName1 = "ETM36 OR ETM40"
        hltTriggerName1 = "LooseIsoPFTau35_Trk20_Prong1"

    elif pyScenario== "2012B":

        lumi = 4430
        label = "Dummy"
        runs = "run >= 193833 && run <= 196531"
        runsText = "193833-196531"
        offlineTriggerData = "HLT_LooseIsoPFTau35_Trk20_Prong1_v6"
        offlineTriggerMc = "HLT_LooseIsoPFTau35_Trk20_Prong1_v6"

        l1TriggerName1 = "ETM36 OR ETM40"
        hltTriggerName1 = "LooseIsoPFTau35_Trk20_Prong1"

    elif pyScenario== "2012C":

        lumi = 6892
        label = "Dummy"
        runs = "run >= 198022 && run <= 203742"
        runsText = "198022-203742"
        offlineTriggerData = "HLT_LooseIsoPFTau35_Trk20_Prong1_v7 || HLT_LooseIsoPFTau35_Trk20_Prong1_v9 || HLT_LooseIsoPFTau35_Trk20_Prong1_v10"
        offlineTriggerMc = "HLT_LooseIsoPFTau35_Trk20_Prong1_v6"

        l1TriggerName1 = "ETM36 OR ETM40"
        hltTriggerName1 = "LooseIsoPFTau35_Trk20_Prong1"

    elif pyScenario== "2012D":

        lumi = 7274
        label = "Dummy"
        runs = "run >= 203777 && run <= 208686"
        runsText = "203777-208686"
        offlineTriggerData = "HLT_LooseIsoPFTau35_Trk20_Prong1_v10"
        offlineTriggerMc = "HLT_LooseIsoPFTau35_Trk20_Prong1_v6"

        l1TriggerName1 = "ETM36 OR ETM40"
        hltTriggerName1 = "LooseIsoPFTau35_Trk20_Prong1"


    elif pyScenario== "2012ABCD":

        lumi = 19296
        label = "Dummy"
        runs = "run >= 190456 && run <= 208686"
        runsText = "190456-208686"
        offlineTriggerData = "HLT_LooseIsoPFTau35_Trk20_Prong1_v2 || HLT_LooseIsoPFTau35_Trk20_Prong1_v3 || HLT_LooseIsoPFTau35_Trk20_Prong1_v4 || HLT_LooseIsoPFTau35_Trk20_Prong1_v6 || HLT_LooseIsoPFTau35_Trk20_Prong1_v7 || HLT_LooseIsoPFTau35_Trk20_Prong1_v9 || HLT_LooseIsoPFTau35_Trk20_Prong1_v10"
        offlineTriggerMc = "HLT_LooseIsoPFTau35_Trk20_Prong1_v6"

        l1TriggerName1 = "ETM36 OR ETM40"
        hltTriggerName1 = "LooseIsoPFTau35_Trk20_Prong1"

    else:
        raise Exception("Invalid run range %s" % pyScenario)

    offlineTriggerData = "(%s) && %s" % (offlineTriggerData, runs)
#    offlineTriggerMc = "HLT_MediumIsoPFTau35_Trk20_v1"

#    offlineSelection1 = And(offlineSelection,offlineTriggerMc)
#    offlineSelection2 = And(offlineSelection,offlineTriggerData)

    L1ETMCut   = 36
    CaloMETCut = 60

    if pyScenario[:4] == "2012":
        CaloMETCut = 70
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


    plotDir = "METLeg"
#    plotDir += "McFall11"
####    plotDir += "RunRange%s" % pyScenario
    plotDir += str(pyScenario[:4])

    ### Trigger selectiondefinitions                                                                                                
    # Default is for 2011B                                                                                                    
#    l1TriggerName1 = "Jet52_Central"
#    hltTriggerName1 = "MediumIsoPFTau35_Trk20"
    l1TriggerName2 = l1TriggerName1
    hltTriggerName2 = hltTriggerName1

    plotter = Plotter(datasets,plotDir,lumi) # FIXME
    plotter.setLegends(legend1, legend2)
    plotter.setTriggers(dataVsMc, l1TriggerName1, hltTriggerName1, l1TriggerName2, hltTriggerName2, runsText)

    ptbins = [20, 30, 40, 50, 60, 70, 80, 100, 120, 140, 160, 180, 200]
    etabins = [-2.1, -1.05, 0, 1.05, 2.1]
    vtxbins = [0,5,10,15,20,25,30,35]
    ptbins2 = [0, 10, 20, 30, 40, 50, 60, 70, 80, 100, 120, 140, 160, 180, 200]


    prefix = "Data"+pyScenario+"_"
    if dataVsMc == 1:
        prefix+="DataVsMC_"
    if dataVsMc == 2:
        prefix+="DataVsMCCaloTau_"

    mcWeight = None
    if dataVsMc > 0 and pyScenario != "Unweighted":
        mcWeight = "pileupWeight_"+pyScenario+"(MCNPU)"
    print
    print "MC weight",pyScenario
    print

    if pyScenario== "2011AB":
#        num2 = And(denom2,"(HLT_IsoPFTau35_Trk20_MET60_v2 || HLT_IsoPFTau35_Trk20_MET60_v3 || HLT_IsoPFTau35_Trk20_MET60_v4 || HLT_IsoPFTau35_Trk20_MET60_v6 || ((HLT_MediumIsoPFTau35_Trk20_MET60_v1 || HLT_MediumIsoPFTau35_Trk20_MET60_v5 || HLT_MediumIsoPFTau35_Trk20_MET60_v6) && L1MET>30) )")
        num1 = And(denom1,"(HLT_IsoPFTau35_Trk20_MET60_v2 || HLT_IsoPFTau35_Trk20_MET60_v3 || HLT_IsoPFTau35_Trk20_MET60_v4 || HLT_IsoPFTau35_Trk20_MET60_v6 || ((HLT_MediumIsoPFTau35_Trk20_MET60_v1 || HLT_MediumIsoPFTau35_Trk20_MET60_v5 || HLT_MediumIsoPFTau35_Trk20_MET60_v6)) )")
        num2 = And(denom2,"((HLT_IsoPFTau35_Trk20_v2 || HLT_IsoPFTau35_Trk20_v3 || HLT_IsoPFTau35_Trk20_v4 || HLT_IsoPFTau35_Trk20_v6) && CaloMET_ET>60) || ((HLT_MediumIsoPFTau35_Trk20_v1 || HLT_MediumIsoPFTau35_Trk20_v5 || HLT_MediumIsoPFTau35_Trk20_v6) && CaloMET_ET>60 && L1MET>36)")
        if dataVsMc > 0:
            num2 = And(denom1,"HLT_MediumIsoPFTau35_Trk20_MET60_v1")

    if pyScenario== "2012ABCD" or pyScenario== "2012A" or pyScenario== "2012B" or pyScenario== "2012C" or pyScenario== "2012D":
        num1 = And(denom1,"(HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v2 || HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v3 || HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v4 || HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v6 || HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v7 || HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v9 || HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v10)")
        num2 = And(denom2,"CaloMET_ET>%s && L1MET>%s"%(CaloMETCut,L1ETMCut))
        if dataVsMc == 1:
            num2 = And(denom2,"HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v6")
        if dataVsMc == 2:
            num1 = And(denom1,"CaloMET_ET>%s && L1MET>%s"%(CaloMETCut,L1ETMCut))
            num2 = And(denom2,"CaloMET_ET>%s && L1MET>%s"%(CaloMETCut,L1ETMCut))

####            num1 = And(denom2,"HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v6 && L1MET > 52.94")#36/0.68

    hnummet = ROOT.TH1F("hnummet", "hnummet", len(ptbins)-1, array.array("d", ptbins))
    hnumvtx = ROOT.TH1F("hnumvtx", "hnumvtx", len(vtxbins)-1, array.array("d", vtxbins))
    hl1etm = ROOT.TH1F("hl1etm", "hl1etm", len(ptbins2)-1, array.array("d", ptbins2))

####    offlineMet50   = "PFMET_ET > 50"
    offlineMet50   = "PFMETtype1_ET > 50"

    denom1met = And(denom1, offlineMet50)
    denom2met = And(denom2, offlineMet50)
    num1met = And(num1, offlineMet50)
    num2met = And(num2, offlineMet50)

    print num1
    print denom1
    print num2
    print denom2

    efficiency = plotter.plotEfficiency(prefix+"MET", "PFMET_ET>>hnummet", num1, denom1, num2, denom2, mcWeight, xlabel="MET (GeV)",ylabel="HLT MET efficiency",drawText=True,printResults=True)
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


class Plotter:
    def __init__(self, datasets, plotDir, lumi):
        self.datasets = datasets
        self.plotDir = plotDir
        self.lumi = lumi

        if not os.path.exists(plotDir):
            os.mkdir(plotDir)

    def setLegends(self, legend1, legend2):
        self.legend1 = legend1
        self.legend2 = legend2

    def setTriggers(self, dataVsMc, l1TriggerName1, hltTriggerName1, l1TriggerName2, hltTriggerName2, runs):
        self.dataVsMc = dataVsMc
        self.l1TriggerName1 = l1TriggerName1
        self.hltTriggerName1 = hltTriggerName1
        self.l1TriggerName2 = l1TriggerName2
        self.hltTriggerName2 = hltTriggerName2
        self.runs = runs

        if dataVsMc == 0:
            if l1TriggerName1 != l1TriggerName2:
                raise Exception("If dataVsMc is False, l1TriggerName1 and 2 should be same ('%s' != '%s')" % (l1TriggerName1, l1TriggerName2))
            if hltTriggerName1 != hltTriggerName2:
                raise Exception("If dataVsMc is False, hltTriggerName1 and 2 should be same ('%s' != '%s')" % (hltTriggerName1, hltTriggerName2))

    def getEfficiency_old(self,datasets,varexp,num,denom):
#        print "check getEfficiency"
        print "    varexp",varexp
        print "    num",num
        print "    denom",denom
        collection = ROOT.TObjArray()
        weights = []
        for dataset in datasets:
            #print "check dataset",dataset.name
            tree = dataset.getRootHisto("TTEffTree")[0]

            if tree.GetEntries() == 0:
                continue
            tree.Draw(varexp, num, "goff e")
            n = tree.GetHistogram().Clone()

            tree.Draw(varexp, denom, "goff e")
            d = tree.GetHistogram().Clone()
            print dataset.getName(),"n=",n.GetEntries(),"d=",d.GetEntries()
            for i in range(1,d.GetNbinsX()+1):
                print "    bin",i,d.GetBinContent(i)
            eff = ROOT.TEfficiency(n, d)
            eff.SetStatisticOption(ROOT.TEfficiency.kFNormal)
            collection.Add(eff)

            weight = 1
            if dataset.isMC():
                weight = dataset.getCrossSection()
            print "MC weight",weight
            weights.append(ROOT.Double(weight))

        if len(weights) > 1:
            return ROOT.TEfficiency.Combine(collection,"",len(weights),array.array("d",weights)),n,d
        return eff

    def getEfficiency(self,datasets,varexp,num,denom):
#        print "check getEfficiency"                                                                                                        
        print "    varexp",varexp
        print "    num",num
        print "    denom",denom
        teff = ROOT.TEfficiency()
        teff.SetStatisticOption(ROOT.TEfficiency.kFNormal)
        tn = ROOT.TH1F()
        td = ROOT.TH1F()
        first = True
        isData = False
#        collection = ROOT.TObjArray()
#        weights = []
        for dataset in datasets:
            if first:
                isData = dataset.isData()

            tree = dataset.getRootHisto("TTEffTree")[0]

            if tree.GetEntries() == 0:
                continue
            tree.Draw(varexp, num, "goff e")
            n = tree.GetHistogram().Clone()

            tree.Draw(varexp, denom, "goff e")
            d = tree.GetHistogram().Clone()
            print dataset.getName(),"n=",n.GetEntries(),"d=",d.GetEntries()

            eff = ROOT.TEfficiency(n, d)
            eff.SetStatisticOption(ROOT.TEfficiency.kFNormal)

            weight = 1
            if dataset.isMC():
                weight = dataset.getCrossSection()
                for i in range(0,d.GetNbinsX()):
                    print "    bin",i,d.GetBinLowEdge(i),n.GetBinContent(i),d.GetBinContent(i)
            eff.SetWeight(weight)
                
            if first:
                teff = eff
                if dataset.isData():
                    tn = n
                    td = d
                first = False
            else:
                teff.Add(eff)
                if dataset.isData():
                    tn.Add(n)
                    td.Add(d)
            #collection.Add(eff)

            #weight = 1
            #if dataset.isMC():
            #    weight = dataset.getCrossSection()
            #print "MC weight",weight
            #weights.append(ROOT.Double(weight))

#        if len(weights) > 1:
#            return ROOT.TEfficiency.Combine(collection,"",len(weights),array.array("d",weights)),n,d
        if isData:
            teff = ROOT.TEfficiency(tn, td)
            teff.SetStatisticOption(ROOT.TEfficiency.kFNormal)
            for i in range(0,td.GetNbinsX()):
                print "    bin",i,td.GetBinLowEdge(i),tn.GetBinContent(i),td.GetBinContent(i),tn.GetBinContent(i)/td.GetBinContent(i)
#        teff.Draw("ap")
#        return teff.GetPaintedGraph().Clone()
        return self.convert2TGraph(teff)

    def convert2TGraph(self,tefficiency):
        x     = []
        y     = []
        xerrl = []
        xerrh = []
        yerrl = []
        yerrh = []
        h = tefficiency.GetCopyTotalHisto()
        n = h.GetNbinsX()
        for i in range(0,n):
            x.append(h.GetBinLowEdge(i)+0.5*h.GetBinWidth(i))
            xerrl.append(0.5*h.GetBinWidth(i))
            xerrh.append(0.5*h.GetBinWidth(i))
            y.append(tefficiency.GetEfficiency(i))
            yerrl.append(tefficiency.GetEfficiencyErrorLow(i))
            yerrh.append(tefficiency.GetEfficiencyErrorUp(i))
        return ROOT.TGraphAsymmErrors(n,array.array("d",x),
                                        array.array("d",y),
                                        array.array("d",xerrl),
                                        array.array("d",xerrh),
                                        array.array("d",yerrl),
                                        array.array("d",yerrh))

    def getVariable(self,datasets,varexp,selection):
        retHisto = 0
        for dataset in datasets:
            tree = dataset.getRootHisto("TTEffTree")[0]

            if tree.GetEntries() == 0:
                continue

            tree.Draw(varexp, selection, "goff e")
            h = tree.GetHistogram().Clone()
            if dataset.isMC():
                weight = dataset.getCrossSection()
                h.Scale(weight)

            if retHisto == 0:
                retHisto = h
            else:
                retHisto.Add(h)
        retHisto.Scale(1/retHisto.Integral())
        return retHisto

    def plotVariable(self, name, varexp, selection1, selection2, xlabel=None, ylabel=None):
        print "plotVariable selection1",selection1
        print "plotVariable selection2",selection2
        dataset1 = self.datasets.getDataDatasets()
        dataset2 = dataset1
        if self.dataVsMc:
            dataset2 = self.datasets.getMCDatasets()

        h1 = self.getVariable(dataset1,varexp,selection1)
        h2 = self.getVariable(dataset2,varexp,selection2)
        h1.SetName("h1")
        h2.SetName("h2")

        print "check h1",h1.GetEntries()
        print "check h2",h2.GetEntries()

        fOUT = ROOT.TFile.Open("test.root","RECREATE")
        h1.Write()
        h2.Write()
        fOUT.Close()

        p = plots.ComparisonPlot(histograms.HistoGraph(h1, "h1", "p", "P"),
                                 histograms.HistoGraph(h2, "h2", "p", "P"))

        if hasattr(self, "legend1"):
            p.histoMgr.setHistoLegendLabelMany({"h1": self.legend1, "h2": self.legend2})

        p.getFrame2().GetYaxis().SetTitle("Ratio")
        p.save()
        return p

    def plotEfficiency(self, name, varexp, num1, denom1, num2, denom2, weight2=None, xlabel=None, ylabel=None, opts={}, opts2={}, fit=False, fitMin=None, fitMax=None, moveLegend={}, drawText=False, printResults=False):

        dataset1 = self.datasets.getDataDatasets()
        dataset2 = dataset1
        if self.dataVsMc > 0:
            dataset2 = self.datasets.getMCDatasets()

        eff1 = self.getEfficiency(dataset1,varexp, num1, denom1)
        eff2 = self.getEfficiency(dataset2,varexp, num2, denom2)
        print "check1",name
        x = ROOT.Double(0)
        y = ROOT.Double(0)
        styles.dataStyle.apply(eff1)
        styles.mcStyle.apply(eff2)
        eff1.SetMarkerSize(1)
        eff2.SetMarkerSize(1.5)

        p = plots.ComparisonPlot(histograms.HistoGraph(eff1, "eff1", "p", "P"),
                                 histograms.HistoGraph(eff2, "eff2", "p", "P"))

        if hasattr(self, "legend1"):
            p.histoMgr.setHistoLegendLabelMany({"eff1": self.legend1, "eff2": self.legend2})

        opts_ = {"ymin": 0, "ymax": 1.1}
        opts_.update(opts)

        opts2_ = {"ymin": 0.5, "ymax": 1.5}
        opts2_.update(opts2)

        moveLegend_ = {"dx": -0.55}
        moveLegend_.update(moveLegend)

        if fit:
            (fit1, res1) = self._fit("eff1", eff1, fitMin, fitMax)
            (fit2, res2) = self._fit("eff2", eff2, fitMin, fitMax)

            p.prependPlotObject(fit2)
            p.prependPlotObject(fit1)

        self._common(name, p, xlabel, ylabel, ratio=True, energy = dataset2[0].info["energy"], opts=opts_, opts2=opts2_, moveLegend=moveLegend_)
        if drawText and hasattr(self, "l1TriggerName1"):
            x = 0.45
            y = 0.35
            size = 17
            dy = 0.035
            mcColor = eff2.GetMarkerColor()
            if self.dataVsMc:
                if self.l1TriggerName1 == self.l1TriggerName2 and self.hltTriggerName1 == self.hltTriggerName2:
                    histograms.addText(x, y, "Data (runs %s) and MC"%self.runs, size); y -= dy
                    histograms.addText(x, y, "L1:  %s" % self.l1TriggerName1, size); y -= dy
                    histograms.addText(x, y, "HLT: %s" % self.hltTriggerName1, size); y -= dy
                else:
                    histograms.addText(x, y, "Data (runs %s)"%self.runs, size); y -= dy
                    histograms.addText(x, y, "L1:  %s" % self.l1TriggerName1, size); y -= dy
                    histograms.addText(x, y, "HLT: %s" % self.hltTriggerName1, size); y -= dy
                    y -= 0.01
                    histograms.addText(x, y, "MC", size, color=mcColor); y -= dy
                    histograms.addText(x, y, "L1:  %s" % self.l1TriggerName2, size, color=mcColor); y -= dy
                    histograms.addText(x, y, "HLT: %s" % self.hltTriggerName2, size, color=mcColor); y -= dy
            else:
                histograms.addText(x, y, "Data (runs %s)"%self.runs, size); y -= dy
                histograms.addText(x, y, "L1:  %s" % self.l1TriggerName1, size); y -= dy
                histograms.addText(x, y, "HLT: %s" % self.hltTriggerName1, size); y -= dy


        if printResults:

            ratioweighted = 0
            weight = 0
            ratio = p.ratios[0]
            print
#            for bin in xrange(1, n1.GetNbinsX()+1):
            for bin in xrange(1, eff1.GetN()+1):
                i = bin-1
#                print "Bin low edge %.0f" % n1.GetBinLowEdge(bin)
                print "Bin low edge %.0f" % (eff1.GetX()[i] - eff1.GetErrorXlow(i))
                print "   1: efficiency %.7f +- %.7f" % (eff1.GetY()[i], max(eff1.GetErrorYhigh(i), eff1.GetErrorYlow(i))), "Entries num"#,n1.GetBinContent(bin),"denom",d1.GetBinContent(bin)
                print "   2: efficiency %.7f +- %.7f" % (eff2.GetY()[i], max(eff2.GetErrorYhigh(i), eff2.GetErrorYlow(i))), "Entries num"#,n2.GetBinContent(bin),"denom",d2.GetBinContent(bin)
                print "   ratio:        %.7f +- %.7f" % (ratio.getRootGraph().GetY()[i], max(ratio.getRootGraph().GetErrorYhigh(i), ratio.getRootGraph().GetErrorYlow(i)))
                #if n1.GetBinLowEdge(bin) >= 41:
                #    weight += eff1.GetY()[i]
                #    ratioweighted += eff1.GetY()[i]*max(eff1.GetErrorYhigh(i), eff1.GetErrorYlow(i))
            print
#            print "Weighted uncert PFTau > 41:", ratioweighted/weight
            print

        p.getFrame2().GetYaxis().SetTitle("Ratio")
        p.save()
        return p

    def _fit(self, name, graph, min, max, xpos=0):
        function = ROOT.TF1("fit"+name, "0.5*[0]*(1+TMath::Erf( (sqrt(x)-sqrt([1]))/(sqrt(2)*[2]) ))", min, max);
        function.SetParameters(1., 40., 1.);
        function.SetParLimits(0, 0.0, 1.0);
        fitResult = graph.Fit(function, "NRSE+EX0");
        print "Fit status", fitResult.Status()
        #fitResult.Print("V");                                                                                                      
        #fitResult.GetCovarianceMatrix().Print();                                                                                   
        function.SetLineColor(graph.GetMarkerColor());
        function.SetLineWidth(2);
        # function.Draw("same")                                                                                                     
        # ROOT.gPadUpdate();                                                                                                        
        # stat = graph.FindObject("stats");                                                                                         
        # stat.SetX1NDC(stat.GetX1NDC()+xpos);                                                                                      
        # stat.SetX2NDC(stat.GetX2NDC()+xpos);                                                                                      
        # stat.SetTextColor(graph.GetMarkerColor());                                                                                
        # stat.SetLineColor(graph.GetMarkerColor());                                                                                
        return (function, fitResult)

    def _common(self, name, plot, xlabel=None, ylabel=None, ratio=False, energy = 0, opts={}, opts2={}, moveLegend={}):
        plot.createFrame(os.path.join(self.plotDir, name), createRatio=ratio, opts=opts, opts2=opts2)
        if hasattr(self, "legend1"):
            plot.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))

        if xlabel != None:
            plot.frame.GetXaxis().SetTitle(xlabel)
        if ylabel != None:
            plot.frame.GetYaxis().SetTitle(ylabel)

        plot.draw()
        histograms.addCmsPreliminaryText()
        histograms.addEnergyText(s="%s TeV"%energy)
        histograms.addLuminosityText(None, None, self.lumi)

if __name__ == "__main__":
    main()
