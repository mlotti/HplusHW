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



class Plotter:
    def __init__(self, datasets, plotDir, lumi):
        self.datasets = datasets
        self.plotDir = plotDir
        self.lumi = lumi

        if not os.path.exists(plotDir):
            os.mkdir(plotDir)

        self.x = 0.45
        self.y = 0.35
        self.size = 17
        self.dy = 0.035

    def setLegends(self, legend1, legend2):
        self.legend1 = legend1
        self.legend2 = legend2

    def setTextPos(self,x,y,size,dy):
        self.x    = x
        self.y    = y
        self.size = size
        self.dy   = dy

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

	    if d.GetEntries() == 0:
		continue

            for i in range(1,d.GetNbinsX()+1):
                print "    bin",i,n.GetBinContent(i),d.GetBinContent(i)
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

    def getStatOption(self):
        return self.statOption

    def getEfficiency(self,datasets,varexp,num,denom):

#        statOption = ROOT.TEfficiency.kBUniform
        self.statOption = ROOT.TEfficiency.kFNormal

#        print "check getEfficiency"                                                                                                        
        print "    varexp",varexp
        print "    num",num
        print "    denom",denom

        first = True
        isData = False
#        collection = ROOT.TObjArray()
#        weights = []

        for dataset in datasets:
            #print "check dataset",dataset.name
            if first:
                isData = dataset.isData()

#            tree = dataset.getRootHisto("TTEffTree")[0]
            tree = dataset.createRootChain("TTEffTree")[0]

            if tree.GetEntries() == 0:
                continue

            tree.Draw(varexp, num, "goff e")
            n = tree.GetHistogram().Clone()

            tree.Draw(varexp, denom, "goff e")
            d = tree.GetHistogram().Clone()
            print dataset.getName(),"n=",n.GetEntries(),"d=",d.GetEntries()

            if d.GetEntries() == 0:
                continue

            eff = ROOT.TEfficiency(n, d)
            eff.SetStatisticOption(self.statOption)

            weight = 1
            if dataset.isMC():
                weight = dataset.getCrossSection()
                for i in range(1,d.GetNbinsX()+1):
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
            teff.SetStatisticOption(self.statOption)
            for i in range(1,td.GetNbinsX()+1):
                if td.GetBinContent(i) > 0:
                    print "    bin",i,td.GetBinLowEdge(i),tn.GetBinContent(i),td.GetBinContent(i),tn.GetBinContent(i)/td.GetBinContent(i)
                else:
                    print "    bin",i,td.GetBinLowEdge(i),tn.GetBinContent(i),td.GetBinContent(i)
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
        for i in range(1,n+1):
            x.append(h.GetBinLowEdge(i)+0.5*h.GetBinWidth(i))
            xerrl.append(0.5*h.GetBinWidth(i))
            xerrh.append(0.5*h.GetBinWidth(i))
            y.append(tefficiency.GetEfficiency(i))
            yerrl.append(tefficiency.GetEfficiencyErrorLow(i))
            # ugly hack to prevent error going above 1
            errUp = tefficiency.GetEfficiencyErrorUp(i)
            if y[-1] == 1.0:
                errUp = 0
            yerrh.append(errUp)
        return ROOT.TGraphAsymmErrors(n,array.array("d",x),
                                        array.array("d",y),
                                        array.array("d",xerrl),
                                        array.array("d",xerrh),
                                        array.array("d",yerrl),
                                        array.array("d",yerrh))

    def getVariable(self,datasets,varexp,selection):
        retHisto = 0
        for dataset in datasets:
            tree = dataset.createRootChain("TTEffTree")[0]

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
        dataset2 = self.datasets.getMCDatasets()
        if self.dataVsMc == 3:
            dataset2 = dataset1
        if self.dataVsMc == 4:
            dataset1 = dataset2

        if self.dataVsMc == 1 or self.dataVsMc == 2 or self.dataVsMc == 4:
            if weight2 == None:
                dataset1 = dataset2
            else:
                num2   = "%s*%s*(%s)" % (weight2, "topPtWeight", num2)
                denom2 = "%s*%s*(%s)" % (weight2, "topPtWeight", denom2)

        if self.dataVsMc == 4:
            if not weight2 == None:
                num1   = "%s*%s*(%s)" % (weight2, "topPtWeight", num1)
                denom1 = "%s*%s*(%s)" % (weight2, "topPtWeight", denom1)

#                num2   = "%s*(%s)" % (weight2, num2)                                         
#                denom2 = "%s*(%s)" % (weight2, denom2)


        eff1 = self.getEfficiency(dataset1,varexp, num1, denom1)
        eff2 = self.getEfficiency(dataset2,varexp, num2, denom2)

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
            mcColor = eff2.GetMarkerColor()
            x    = self.x
            y    = self.y
            size = self.size
            dy   = self.dy
            if self.dataVsMc:
                if self.l1TriggerName1 == self.l1TriggerName2 and self.hltTriggerName1 == self.hltTriggerName2:
                    histograms.addText(x, y, "Data (runs %s) and MC"%self.runs, size); y -= dy
                    #histograms.addText(x, y, "L1:  %s" % self.l1TriggerName1, size); y -= dy
                    histograms.addText(x, y, "HLT: %s" % self.hltTriggerName1, size); y -= dy
                else:
                    histograms.addText(x, y, "Data (runs %s)"%self.runs, size); y -= dy
                    #histograms.addText(x, y, "L1:  %s" % self.l1TriggerName1, size); y -= dy
                    histograms.addText(x, y, "HLT: %s" % self.hltTriggerName1, size); y -= dy
                    y -= 0.01
                    histograms.addText(x, y, "MC", size, color=mcColor); y -= dy
                    #histograms.addText(x, y, "L1:  %s" % self.l1TriggerName2, size, color=mcColor); y -= dy
                    histograms.addText(x, y, "HLT: %s" % self.hltTriggerName2, size, color=mcColor); y -= dy
            else:
                histograms.addText(x, y, "Data (runs %s)"%self.runs, size); y -= dy
                #histograms.addText(x, y, "L1:  %s" % self.l1TriggerName1, size); y -= dy
                histograms.addText(x, y, "HLT: %s" % self.hltTriggerName1, size); y -= dy


        if printResults:

            ratioweighted = 0
            weight = 0
            ratio = p.ratioHistoMgr.getHistos()[0]
            print
#            for bin in xrange(1, n1.GetNbinsX()+1):
            for i in xrange(1, eff1.GetN()):
#                i = bin-1
#                print "Bin low edge %.0f" % n1.GetBinLowEdge(bin)
                print "Bin low edge %.0f" % (eff1.GetX()[i] - eff1.GetErrorXlow(i))
                print "   1: efficiency %.7f + %.7f - %.7f" % (eff1.GetY()[i], eff1.GetErrorYhigh(i), eff1.GetErrorYlow(i)), "Entries num"#,n1.GetBinContent(bin),"denom",d1.GetBinContent(bin)
                print "   2: efficiency %.7f + %.7f - %.7f" % (eff2.GetY()[i], eff2.GetErrorYhigh(i), eff2.GetErrorYlow(i)), "Entries num"#,n2.GetBinContent(bin),"denom",d2.GetBinContent(bin)
                if eff1.GetY()[i] > 0 and eff2.GetY()[i] > 0:
                    print "   ratio:        %.7f + %.7f - %.7f" % (ratio.getRootGraph().GetY()[i], ratio.getRootGraph().GetErrorYhigh(i), ratio.getRootGraph().GetErrorYlow(i))
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
#        if hasattr(self, "legend1"):
        plot.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))

        if xlabel != None:
            plot.frame.GetXaxis().SetTitle(xlabel)
        if ylabel != None:
            plot.frame.GetYaxis().SetTitle(ylabel)

        plot.draw()
        histograms.addCmsPreliminaryText()
        histograms.addEnergyText(s="%s TeV"%energy)
        histograms.addLuminosityText(None, None, self.lumi)


