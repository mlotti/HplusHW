#!/usr/bin/env python

import sys

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.LandSTools as lands

class DatasetContainer:
    def __init__(self, shapeList):
        self._name = None
        self._uncertaintyShapes = None
        self._distentangleName(shapeList)
        self._distentangleUncertainties(shapeList)

    def _distentangleName(self, shapeList):
        # Find name
        myLength = 0
        if len(shapeList) > 1:
            mySplitList1 = shapeList[0].split("_")
            mySplitList2 = shapeList[1].split("_")
            myStatus = True
            while myStatus and myLength < len(mySplitList1):
                if mySplitList1[myLength] == mySplitList2[myLength]:
                    myLength += 1
                else:
                    myStatus = False
            self._name = "_".join(map(str, mySplitList1[:(myLength)]))
        else:
            self._name = shapeList[0]

    def _distentangleUncertainties(self, shapeList):
        self._uncertaintyShapes = []
        for s in shapeList:
            uncName = s.replace(self._name,"")
            if "Up" in uncName and uncName != "":
                self._uncertaintyShapes.append(uncName)

    def debug(self):
        print "name =",self._name
        print "uncertainties = %s"%(", ".join(map(str, self._uncertaintyShapes)))

    def doPlot(self, f, mass):
        print "Doing plots for:",self._name
        hNominal = f.Get(self._name)
        hNominalHisto = histograms.Histo(hNominal, self._name, drawStyle="HIST")
        # Determine label
        myMCLabels = ["HH","HW","Hplus","MC"]
        myMCStatus = False
        for mclab in myMCLabels:
            if mclab in self._name:
                myMCStatus = True
        myCMSText = "CMS Preliminary"
        if myMCStatus:
            myCMSText = "CMS Simulation"
        #plot = plots.PlotBase(hNominalHisto)
        #plot.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetLineWidth(3))
        #plot.createFrame("shape_data_m%d" % mass, opts={"ymin": 0})
        #plot.frame.GetXaxis().SetTitle("m_{T} (GeV)")
        #plot.frame.GetYaxis().SetTitle("Rate")
        #plot.draw()
        x = 0.6
        size = 20
        #histograms.addText(x, 0.70, "Data %.1f" % _integral(data), size=size)
        #histograms.addText(x, 0.65, "m_{H^{+}}=%d GeV" % mass, size=size)
        #plot.save()
        for uncName in self._uncertaintyShapes:
            print "... uncertainty:",uncName.replace("Up","")
            up = f.Get("%s%s"%(self._name,uncName))
            nom = hNominal.Clone()
            down = f.Get("%s%s"%(self._name,uncName.replace("Up","Down")))
            up.SetLineColor(ROOT.kBlue)
            nom.SetLineColor(ROOT.kBlack)
            down.SetLineColor(ROOT.kRed)
            upHisto = histograms.Histo(up, "Up %.1f"%_integral(up), drawStyle="HIST", legendStyle="l")
            downHisto = histograms.Histo(down, "Down %.1f"%_integral(down), drawStyle="HIST", legendStyle="l")
            nomHisto = histograms.Histo(nom, "Nominal %.1f"%_integral(nom), drawStyle="HIST", legendStyle="l")
            plot = plots.ComparisonManyPlot(nomHisto, [upHisto, downHisto])
            plot.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetLineWidth(3))
            myPlotName = "shape_%s_syst%s" % (self._name, uncName.replace("Up",""))
            myParams = {}
            myParams["ylabel"] = "Events"
            myParams["log"] = False
            myParams["opts2"] = {"ymin": 0.0, "ymax":2.0}
            myParams["opts"] = {"ymin": 0.0}
            myParams["ratio"] = True
            myParams["ratioType"] = "errorScale"
            myParams["ratioYlabel"] = "Var./Nom."
            myParams["cmsText"] = myCMSText
            plots.drawPlot(plot, myPlotName, **myParams)

def doPlot(mass,nameList):
    f = ROOT.TFile.Open(lands.taujetsRootfilePattern%mass)

    content = f.GetListOfKeys()
    # Suppress the warning message of missing dictionary for some iterator
    backup = ROOT.gErrorIgnoreLevel
    ROOT.gErrorIgnoreLevel = ROOT.kError
    diriter = content.MakeIterator()
    ROOT.gErrorIgnoreLevel = backup

    # Find the name stem and the name of the uncertainties
    datasets = []
    shapes = []
    key = diriter.Next()
    myPreviousSplitList = None
    myPreviousKey = None
    while key:
        splitList = key.GetName().split("_")
        if myPreviousSplitList != None:
            shapes.append(myPreviousKey)
            if myPreviousSplitList[0] != splitList[0]:
                # New dataset column
                if not myPreviousKey in ["res.","data_obs"]:
                    shapes.append(myPreviousKey)
                    myDataset = DatasetContainer(shapes)
                    # Make sure that dataset objects are stored for plot making only for unique names
                    if not myDataset._name in nameList:
                        datasets.append(myDataset)
                        nameList.append(myDataset._name)
                shapes = []
        # Store old key
        myPreviousSplitList = splitList
        myPreviousKey = key.GetName()
        # Advance to next
        key = diriter.Next()
    # Do the actual plots
    for d in datasets:
        #d.debug()
        d.doPlot(f,mass)
    # Close the file
    f.Close()

def _integral(h):
    return h.Integral()
    #    return h.Integral(0, h.GetNbinsX()+1)

if __name__ == "__main__":
    # Apply TDR style
    style = tdrstyle.TDRStyle()
    histograms.createLegend.moveDefaults(dx=-0.1, dh=-0.15)
    # Find out the mass points
    massPoints = lands.obtainMassPoints(lands.taujetsRootfilePattern)
    print "The following masses are considered:",massPoints
    nameList = []
    for m in massPoints:
        doPlot(int(m),nameList)
