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

####from PythonWriter import PythonWriter
####pythonWriter = PythonWriter()

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

    datasets = dataset.getDatasetsFromMulticrabCfg(cfgfile=os.path.join(sys.argv[1], "multicrab.cfg"), counters=counters, doEraReplace=False, weightedCounters=False,
                                                   includeOnlyTasks="Tau_")
    datasetsMC = dataset.getDatasetsFromMulticrabCfg(cfgfile=os.path.join(sys.argv[1], "multicrab.cfg"), counters=counters, doEraReplace=False, weightedCounters=False,
                                                     excludeTasks="Tau_")

    datasets.extend(datasetsMC)
#    sys.exit(0)

#    datasets.mergeData()

    style = tdrstyle.TDRStyle()

    puWeights = []
    puWeights.append("pileupWeight_2011AB.C")
#    puWeights.append("pileupWeight_2011A.C")
#    puWeights.append("pileupWeight_2011B.C")

    puWeightPath = "src/HiggsAnalysis/TriggerEfficiency/test"

    offlineTauSelection = "PFTauPt > 41 && abs(PFTauEta) < 2.1"
    offlineSelection = "Sum$(%s) >= 1"%offlineTauSelection
    offlineSelection = And(offlineSelection,"Sum$(PFJetPt > 0) >= 3+Sum$(%s && PFTauJetMinDR < 0.5)"%offlineTauSelection)

    offlineSelections = []
    offlineSelections.append(namedselection("lightHPlusMET",offlineSelection))

    pu_re = re.compile("pileupWeight_(?P<scenario>(\S+))\.C")
    for puWeight in puWeights:
        pyScenario = pu_re.search(puWeight)
        match = pu_re.search(puWeight)
        if match:
            pyScenario = match.group("scenario")

            if pyScenario != "Unweighted":
                ROOT.gROOT.Clear()
                ROOT.gROOT.Reset()
                macroPath = os.path.join(os.environ["PWD"], puWeight+"+")
                macroPath = macroPath.replace("../src/","")
                macroPath = macroPath.replace("HiggsAnalysis/TriggerEfficiency/test/../../../","")

                ROOT.gROOT.LoadMacro(macroPath)

            for selection in offlineSelections:

####                pythonWriter.SaveOfflineSelection(selection)

                doPlots(datasets,selection=selection,dataVsMc=True,pyScenario=pyScenario)

####    pythonWriter.write("tauLegTriggerEfficiency2012_cff.py")

def namedselection(name,selection):
    namedSelection = []
    namedSelection.append(name)
    namedSelection.append(selection)
    return namedSelection

def doPlots(datasets,selection, dataVsMc=True, pyScenario="Unweighted"):
    ### Offline selection definition
    selectionName    = selection[0]
    offlineSelection = selection[1]

    if pyScenario== "2011A": # May10+Prompt-v4 (160431-167913)                                                                     
        lumi = 1197
        label = "L1_SingleTauJet52 OR L1_SingleJet68 + HLT_IsoPFTau35_Trk20_MET45 (Run2011A)"
        runs = "run >= 160404 && run <= 167913"
        runsText = "160404-167913"
        offlineTriggerData = "HLT_IsoPFTau35_Trk20_v2 || HLT_IsoPFTau35_Trk20_v3 || HLT_IsoPFTau35_Trk20_v4 || HLT_IsoPFTau35_Trk20_v6"

    elif pyScenario== "2011AB": # Whole 2011 data                                                                                   
        lumi = 5094.834
        label = "Dummy"
        runs = "run >= 160404 && run <= 180252"
        runsText = "160404-180252"
        offlineTriggerData = "(HLT_IsoPFTau35_Trk20_v2 || HLT_IsoPFTau35_Trk20_v3 || HLT_IsoPFTau35_Trk20_v4 || HLT_IsoPFTau35_Trk20_v6)"
        offlineTriggerData += "|| (HLT_MediumIsoPFTau35_Trk20_v1 || HLT_MediumIsoPFTau35_Trk20_v5 || HLT_MediumIsoPFTau35_Trk20_v6)"

    else:
        raise Exception("Invalid run range %s" % pyScenario)

    offlineTriggerData = "(%s) && %s" % (offlineTriggerData, runs)
    offlineTriggerMc = "HLT_MediumIsoPFTau35_Trk20_v1"

#    offlineSelection1 = And(offlineSelection,offlineTriggerMc)
#    offlineSelection2 = And(offlineSelection,offlineTriggerData)

    if dataVsMc:
        legend1 = "MC, trigger bit"
        legend2 = "Data, trigger bit"
        denom1 = And(offlineSelection,offlineTriggerMc)
        denom2 = And(offlineSelection,offlineTriggerData)
    else:
        legend1 = "Data, CaloMET>60"
        legend2 = "Data, trigger bit"
        denom1 = And(offlineSelection,offlineTriggerData)
        denom2 = denom1


    plotDir = "MET"
    plotDir += "McFall11"
    plotDir += "RunRange%s" % pyScenario

    ### Trigger selectiondefinitions                                                                                                
    # Default is for 2011B                                                                                                    
    l1TriggerName1 = "Jet52_Central"
    hltTriggerName1 = "MediumIsoPFTau35_Trk20"
    l1TriggerName2 = l1TriggerName1
    hltTriggerName2 = hltTriggerName1

    plotter = Plotter(datasets,plotDir,lumi) # FIXME
    plotter.setLegends(legend1, legend2)
    plotter.setTriggers(dataVsMc, l1TriggerName1, hltTriggerName1, l1TriggerName2, hltTriggerName2, runsText)

    ptbins = [20, 30, 40, 50, 60, 70, 80, 100, 120, 140, 160, 180, 200]
    etabins = [-2.1, -1.05, 0, 1.05, 2.1]
    vtxbins = [0,5,10,15,20,25,30,35]

    prefix = "Data"+pyScenario+"_"

    mcWeight = None
    if dataVsMc and pyScenario != "Unweighted":
        mcWeight = "pileupWeight_"+pyScenario+"(MCNPU)"
    print
    print "MC weight",pyScenario
    print

    if pyScenario== "2011AB":
#        num2 = And(denom2,"(HLT_IsoPFTau35_Trk20_MET60_v2 || HLT_IsoPFTau35_Trk20_MET60_v3 || HLT_IsoPFTau35_Trk20_MET60_v4 || HLT_IsoPFTau35_Trk20_MET60_v6 || ((HLT_MediumIsoPFTau35_Trk20_MET60_v1 || HLT_MediumIsoPFTau35_Trk20_MET60_v5 || HLT_MediumIsoPFTau35_Trk20_MET60_v6) && L1MET>30) )")
        num2 = And(denom2,"(HLT_IsoPFTau35_Trk20_MET60_v2 || HLT_IsoPFTau35_Trk20_MET60_v3 || HLT_IsoPFTau35_Trk20_MET60_v4 || HLT_IsoPFTau35_Trk20_MET60_v6 || ((HLT_MediumIsoPFTau35_Trk20_MET60_v1 || HLT_MediumIsoPFTau35_Trk20_MET60_v5 || HLT_MediumIsoPFTau35_Trk20_MET60_v6)) )")
        num1 = And(denom1,"((HLT_IsoPFTau35_Trk20_v2 || HLT_IsoPFTau35_Trk20_v3 || HLT_IsoPFTau35_Trk20_v4 || HLT_IsoPFTau35_Trk20_v6) && CaloMET_ET>60) || ((HLT_MediumIsoPFTau35_Trk20_v1 || HLT_MediumIsoPFTau35_Trk20_v5 || HLT_MediumIsoPFTau35_Trk20_v6) && CaloMET_ET>60 && L1MET>30)")
        if dataVsMc:
            num1 = And(denom1,"HLT_MediumIsoPFTau35_Trk20_MET60_v1")



    hnummet = ROOT.TH1F("hnummet", "hnummet", len(ptbins)-1, array.array("d", ptbins))
    hnumvtx = ROOT.TH1F("hnumvtx", "hnumvtx", len(vtxbins)-1, array.array("d", vtxbins))

    offlineMet50   = "PFMET_ET > 50"

    denom1met = And(denom1, offlineMet50)
    denom2met = And(denom2, offlineMet50)
    num1met = And(num1, offlineMet50)
    num2met = And(num2, offlineMet50)

    plotter.plotEfficiency(prefix+"MET", "PFMET_ET>>hnummet", num1, denom1, num2, denom2, mcWeight, xlabel="MET (GeV)",ylabel="HLT MET efficiency",drawText=True,printResults=True)
    plotter.plotEfficiency(prefix+"Nvtx", "numGoodOfflinePV>>hnumvtx", num1met, denom1met, num2met, denom2met, mcWeight, xlabel="Number of good vertices",printResults=False)

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

        if not dataVsMc:
            if l1TriggerName1 != l1TriggerName2:
                raise Exception("If dataVsMc is False, l1TriggerName1 and 2 should be same ('%s' != '%s')" % (l1TriggerName1, l1TriggerName2))
            if hltTriggerName1 != hltTriggerName2:
                raise Exception("If dataVsMc is False, hltTriggerName1 and 2 should be same ('%s' != '%s')" % (hltTriggerName1, hltTriggerName2))

    def getEfficiency(self,datasets,varexp,num,denom):
#        print "check getEfficiency"
        print "    varexp",varexp
        print "    num",num
        print "    denom",denom
        collection = ROOT.TObjArray()
        weights = []
        for dataset in datasets:

            tree = dataset.createRootChain("analysis/TTEffTree")

            if tree.GetEntries() == 0:
                continue
            tree.Draw(varexp, num, "goff e")
            n = tree.GetHistogram().Clone()

            tree.Draw(varexp, denom, "goff e")
            d = tree.GetHistogram().Clone()
            print dataset.getName(),"n=",n.GetEntries(),"d=",d.GetEntries()
            collection.Add(ROOT.TEfficiency(n, d))

            weight = 1
####            if dataset.isMC():
####                weight = dataset.getCrossSection()
            weights.append(ROOT.Double(weight))

        return ROOT.TEfficiency.Combine(collection,"",len(weights),array.array("d",weights)),n,d

    def plotEfficiency(self, name, varexp, num1, denom1, num2, denom2, weight2=None, xlabel=None, ylabel=None, opts={}, opts2={}, fit=False, fitMin=None, fitMax=None, moveLegend={}, drawText=False, printResults=False):

        dataset2 = self.datasets.getDataDatasets()
        dataset1 = dataset2
        if self.dataVsMc:
            dataset1 = self.datasets.getMCDatasets()

        eff1,n1,d1 = self.getEfficiency(dataset1,varexp, num1, denom1)
        eff2,n2,d2 = self.getEfficiency(dataset2,varexp, num2, denom2)

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

        self._common(name, p, xlabel, ylabel, ratio=True, opts=opts_, opts2=opts2_, moveLegend=moveLegend_)
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
            for bin in xrange(1, n1.GetNbinsX()+1):
                i = bin-1
                print "Bin low edge %.0f" % n1.GetBinLowEdge(bin)
                print "   1: efficiency %.7f +- %.7f" % (eff1.GetY()[i], max(eff1.GetErrorYhigh(i), eff1.GetErrorYlow(i))), "Entries num",n1.GetBinContent(bin),"denom",d1.GetBinContent(bin)
                print "   2: efficiency %.7f +- %.7f" % (eff2.GetY()[i], max(eff2.GetErrorYhigh(i), eff2.GetErrorYlow(i))), "Entries num",n2.GetBinContent(bin),"denom",d2.GetBinContent(bin)
                print "   ratio:        %.7f +- %.7f" % (ratio.getRootGraph().GetY()[i], max(ratio.getRootGraph().GetErrorYhigh(i), ratio.getRootGraph().GetErrorYlow(i)))
                if n1.GetBinLowEdge(bin) >= 41:
                    weight += eff1.GetY()[i]
                    ratioweighted += eff1.GetY()[i]*max(eff1.GetErrorYhigh(i), eff1.GetErrorYlow(i))
            print
            print "Weighted uncert PFTau > 41:", ratioweighted/weight
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

    def _common(self, name, plot, xlabel=None, ylabel=None, ratio=False, opts={}, opts2={}, moveLegend={}):
        plot.createFrame(os.path.join(self.plotDir, name), createRatio=ratio, opts=opts, opts2=opts2)
        if hasattr(self, "legend1"):
            plot.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))

        if xlabel != None:
            plot.frame.GetXaxis().SetTitle(xlabel)
        if ylabel != None:
            plot.frame.GetYaxis().SetTitle(ylabel)

        plot.draw()
        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        histograms.addLuminosityText(None, None, self.lumi)
if __name__ == "__main__":
    main()
