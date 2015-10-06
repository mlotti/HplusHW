#!/usr/bin/env python

import NtupleAnalysis.toolshistograms as histograms
import NtupleAnalysis.toolstdrstyle as tdrstyle
#import NtupleAnalysis.toolsstyles as styles
import NtupleAnalysis.toolsplots as plots

import os
import array

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

class XsecEntry:
    def __init__(self, mhp, tanbeta, xsec, uncMinus, uncPlus):
        self.mhp = mhp
        self.tanbeta = tanbeta
        self.xsec = xsec
        self.uncMinus = uncMinus
        self.uncPlus = uncPlus
    
    def isEntry(self, mhp, tanbeta):
        return mhp == self.mhp and tanbeta == self.tanbeta

class DatabaseReader:
    def __init__(self, filename, label):
        self._label = label
        self._results = [] # list of XsecEntry objects
        # Read results
        self._readFromDatabase(filename)
    
    def _readFromDatabase(self, filename):
        f = open(filename)
        if f == None:
            raise Exception("Error: cannot open file '%s' for reading xsection info!"%filename)
        myLines = f.readlines()
        f.close()
        # Store info
        for line in myLines:
            if not line.startswith("#") and len(line) > 3:
                s = line.split()
                if len(s) != 5:
                    raise Exception("Error: wrong format!")
                e = XsecEntry(int(s[0]), float(s[1]), float(s[2]), float(s[3]), float(s[4]))
                self._results.append(e)

    def getXsecGraph(self, tanbeta):
        data = {}
        uncPlus = {}
        uncMinus = {}
        for e in self._results:
            if e.tanbeta == tanbeta:
                data[e.mhp] = e.xsec
                uncPlus[e.mhp] = e.uncPlus
                uncMinus[e.mhp] = e.uncMinus
        g = ROOT.TGraphAsymmErrors(len(data.keys()))
        myKeys = data.keys()
        myKeys.sort()
        i = 0
        for k in myKeys:
            g.SetPoint(i, k, data[k])
            g.SetPointError(i, 0, 0, uncMinus[k], uncPlus[k])
            i += 1
        return g

if __name__ == "__main__":
    style = tdrstyle.TDRStyle()
    myReaders = []
    myReaders.append(DatabaseReader("hplus8tev.txt", "sqrt(s) = 8 TeV"))
    myReaders.append(DatabaseReader("hplus14tev.txt", "sqrt(s) = 14 TeV"))
    # MSSM scenario settings
    tanBetas = [5, 20, 40]
    
    myColors = [ROOT.kBlue, ROOT.kRed]
    myPlotObjects = []
    i = 0
    for r in myReaders:
        i += 1
        j = 0
        for tb in tanBetas:
            j += 1
            g = r.getXsecGraph(tb)
            g.SetLineColor(myColors[i-1])
            g.SetLineWidth(2)
            g.SetMarkerColor(myColors[i-1])
            g.SetMarkerSize(1.6)
            g.SetMarkerStyle(j+19)
            myPlotObjects.append(histograms.HistoGraph(g, "tan#beta=%d"%tb, drawStyle="PL", legendStyle="lp"))
    
    # Add ratio
    gnum = myPlotObjects[0].getRootGraph()
    gdenom = myPlotObjects[len(tanBetas)].getRootGraph()
    hnum = ROOT.TH1F("num","num",gnum.GetN(),gnum.GetX()[0],gnum.GetX()[gnum.GetN()-1])
    hdenom = hnum.Clone("denom")
    for i in range(gnum.GetN()):
        hnum.SetBinContent(i+1, gnum.GetY()[i])
        hnum.SetBinError(i+1, max(gnum.GetErrorYhigh(i), gnum.GetErrorYlow(i)))
        hdenom.SetBinContent(i+1, gdenom.GetY()[i])
        hdenom.SetBinError(i+1, max(gdenom.GetErrorYhigh(i), gdenom.GetErrorYlow(i)))
    gratio = ROOT.TGraphAsymmErrors(hnum,hdenom)
    # Invert
    for i in range(gratio.GetN()):
        gratio.GetY()[i] = 1.0 / gratio.GetY()[i]
        #gratio.SetPointEYhigh(i, 1.0 / gratio.GetErrorYhigh(i))
    gratio.SetLineWidth(3)
    gratioObject = histograms.HistoGraph(gratio, "ratio", drawStyle="L", legendStyle="l")
    
    # Calculate ratio
    
        #print "ratio: m=%d, ratio:%f"%(myPlotObjects[0].getRootGraph().GetX()[i], myPlotObjects[1].getRootGraph().GetY()[i] / myPlotObjects[0].getRootGraph().GetY()[i])
        
        
    # Do plot
    #plot = plots.ComparisonPlot(myPlotObjects[0], myPlotObjects[1])#, saveFormats=[".png", ".pdf", ".C"])
    plot = plots.PlotBase(myPlotObjects, saveFormats=[".png", ".pdf", ".C"])
    name = "mssmXsection"
    #plot.histoMgr.setHistoLegendLabelMany({})
    plot.createFrame(name, opts={"ymin": 8e-4, "ymax": 30, "xmin": 200, "xmax": 600})
    plot.getPad().SetLogy(True)
    plot.frame.GetXaxis().SetTitle("m_{H^{+}}")
    plot.frame.GetYaxis().SetTitle("#sigma (pb)")
    plot.draw()
    # Legend
    x = 0.2
    dy = 0.12
    legend = ROOT.TLegend(x-0.01, 0.60+dy, x+0.40+0.30*(len(tanBetas)>1), 0.80+dy)
    for j in range(len(myReaders)):
        for i in range(len(tanBetas)):
            if i == 0:
                legend.AddEntry("", myReaders[j]._label+":", "")
            else:
                legend.AddEntry("", "", "")
        for i in range(len(tanBetas)):
            legend.AddEntry(myPlotObjects[i+j*len(tanBetas)].getRootGraph(), "tan#beta=%d"%tanBetas[i], "lp")

    legend.SetNColumns(len(tanBetas))
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)
    #legend.SetTextSize(20)
    legend.SetTextColor(ROOT.kBlack)
    legend.Draw()
    #plot.setLegend(legend)
    #plot.draw()
    # Save plot
    histograms.addText(0.18, 0.20, "Values from LHCHXSWG used", size=20)
    histograms.addText(0.18, 0.16, "Note: no SUSY QCD corrections", size=20)
    plot.save()
    print "Created plot %s"%name
    
    plot = plots.PlotBase([gratioObject], saveFormats=[".png", ".pdf", ".C"])
    name = "mssmXsectionRatio"
    plot.createFrame(name, opts={"ymin": 0, "ymax": 10, "xmin": 200, "xmax": 600})
    plot.getPad().SetLogy(False)
    plot.frame.GetXaxis().SetTitle("m_{H^{+}}")
    plot.frame.GetYaxis().SetTitle("#sigma(14 TeV) / #sigma(8 TeV)")
    plot.draw()
    histograms.addText(0.18, 0.20, "Values from LHCHXSWG used", size=20)
    histograms.addText(0.18, 0.16, "Note: no SUSY QCD corrections", size=20)
    plot.save()
    print "Created plot %s"%name

    
