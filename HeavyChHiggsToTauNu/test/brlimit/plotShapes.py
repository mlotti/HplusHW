#!/usr/bin/env python

import sys
import os
from optparse import OptionParser

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.LandSTools as lands
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.aux as aux

# Height settings for the all-in-one ratio plot
_cHeaderHeight = 40
_cBodyHeight = 180
_cFooterHeight = 70

_dirname = "shapeSyst"

class RatioPlotContainer:
    def __init__(self, datasetName):
        self._dsetName = datasetName
        self._ratioPlotList = []
        self._systNameList = []

    def addRatioPlot(self, ratioPlot, systName):
        self._ratioPlotList.append(ratioPlot)
        self._systNameList.append(systName)

    def drawIndividually(self):
        for i in range(0,len(self._systNameList)):
            myPlotName = "shapeSystRatioOnlyIndividual_%s_syst_%s"%(self._dsetName,self._systNameList[i])
            plot = self._ratioPlotList[i]
            backup = ROOT.gErrorIgnoreLevel
            ROOT.gErrorIgnoreLevel = ROOT.kError
            c = ROOT.TCanvas("","",600,240)
            ROOT.gErrorIgnoreLevel = backup
            c.SetLeftMargin(0.12)
            c.SetBottomMargin(0.3)
            plot.getFrame2().GetXaxis().SetTitleOffset(.85)
            plot.getFrame2().GetYaxis().SetLabelSize(26)
            plot.getFrame2().GetYaxis().SetTitleOffset(.36)
            plot.getFrame2().Draw() # Clone needed because otherwise plot.getFrame2() becomes None after Draw()
            plot.ratioHistoMgr.draw()
            plot.ratioLine.Draw("L")
            c.RedrawAxis()
            tb = histograms.PlotText(x=0.18, y=0.82, text=self._systNameList[i], size=30)
            tb.Draw()
            backup = ROOT.gErrorIgnoreLevel
            ROOT.gErrorIgnoreLevel = ROOT.kError
            for suffix in [".png",".C",".eps"]:
                c.Print("%s/%s%s"%(_dirname,myPlotName,suffix))
            ROOT.gErrorIgnoreLevel = backup

    def drawAllInOne(self, myAllShapeNuisances, cmsText, luminosity):
        myMaxSize = len(myAllShapeNuisances)
        # Create pads
        canvasHeight = _cHeaderHeight + _cBodyHeight * myMaxSize + _cFooterHeight
        c = ROOT.TCanvas("","",600,canvasHeight)
        c.Divide(1,myMaxSize)
        myHeightBefore = canvasHeight
        myHeightAfter = canvasHeight
        for i in range(0,myMaxSize):
            myHeightBefore = myHeightAfter
            p = c.cd(i+1)
            myTopMargin = 0.0
            myBottomMargin = 0.0
            if i == 0:
                # Top histogram with header
                myHeightAfter -= _cHeaderHeight + _cBodyHeight
                myTopMargin = float(_cHeaderHeight) / float(_cHeaderHeight+_cBodyHeight)
            elif i == myMaxSize-1:
                # Bottom histogram with x axis label and title
                myHeightAfter -= _cFooterHeight + _cBodyHeight
                myBottomMargin = float(_cFooterHeight) / float(_cFooterHeight+_cBodyHeight)
            else:
                # Middle histogram, only body
                myHeightAfter -= _cBodyHeight
            (xlow, ylow, xup, yup) = [ROOT.Double(x) for x in [0.0]*4]
            p.GetPadPar(xlow, ylow, xup, yup)
            p.SetPad(xlow, float(myHeightAfter)/float(canvasHeight), xup, float(myHeightBefore)/float(canvasHeight))
            p.SetBorderMode(0)
            p.SetFillStyle(4000)
            p.SetTopMargin(myTopMargin)
            p.SetBottomMargin(myBottomMargin)
        # Draw plots
        myEmptyPlot = aux.Clone(self._ratioPlotList[0].getFrame2()) # Keep the clone if it is needed to draw the x axis
        for i in range(0,myMaxSize):
            p = c.cd(i+1)
            # Find plot
            myPlotIndex = None
            for j in range(0,len(self._systNameList)):
                if myAllShapeNuisances[i] == self._systNameList[j]:
                    myPlotIndex = j
            plot = None
            if myPlotIndex != None:
                plot = self._ratioPlotList[myPlotIndex].getFrame2()
            else:
                if i == myMaxSize-1:
                    plot = myEmptyPlot # Use this to draw the x axis
                else:
                    plot = self._ratioPlotList[0].getFrame2() # Only the empty frame matters
            # Draw plot
            if i == myMaxSize-1:
                # Bottom histogram
                plot.GetXaxis().SetTitleOffset(0.6*myMaxSize+0.6) # 6.6/10, 3.6/5
            else:
                plot.GetXaxis().SetTitleSize(0)
                plot.GetXaxis().SetLabelSize(0)
            plot.GetYaxis().SetLabelSize(26)
            plot.GetYaxis().SetTitleOffset(0.34*myMaxSize+0.1) # 3.5/10, 1.8/5
            plot.SetMinimum(0.001)
            plot.SetMaximum(1.999)
            plot.Draw() # Plot frame for every nuisance
            if myPlotIndex != None:
                self._ratioPlotList[myPlotIndex].ratioHistoMgr.draw() # Plot content only if affected
            self._ratioPlotList[0].ratioLine.Draw("L")
            p.RedrawAxis()
            # Labels for shape nuisance and dataset
            myHeight = 0.82
            if i == 0:
                myHeight = myHeight*float(_cBodyHeight) / float(_cHeaderHeight+_cBodyHeight)
            elif i == myMaxSize-1:
                myHeight = (myHeight*float(_cBodyHeight)+float(_cFooterHeight)) / float(_cFooterHeight +_cBodyHeight)
            histograms.addText(x=0.18, y=myHeight, text=myAllShapeNuisances[i], size=30)
            histograms.addText(x=0.93, y=myHeight, text=self._dsetName, size=30, align="right")
            # Header labels
            if i == 0:
                histograms.addEnergyText(y=0.84) # Does the 8 TeV get set properly for 2012?
                histograms.addCmsPreliminaryText(y=0.84, text=cmsText)
                histograms.addLuminosityText(x=None,y=0.84,lumi=luminosity)
            # Labels for non-existing nuisances
            if myPlotIndex == None:
                myHeight = 0.44
                if i == 0:
                    myHeight = myHeight*float(_cBodyHeight) / float(_cHeaderHeight+_cBodyHeight)
                elif i == myMaxSize-1:
                    myHeight = (myHeight*float(_cBodyHeight)+float(_cFooterHeight)) / float(_cFooterHeight +_cBodyHeight)
                histograms.addText(x=0.555, y=myHeight, text="Not affected", size=30, align="center")
        # Save plot
        myPlotName = "shapeSystRatioOnlyAll_%s"%(self._dsetName)
        backup = ROOT.gErrorIgnoreLevel
        ROOT.gErrorIgnoreLevel = ROOT.kError
        for suffix in [".png",".C",".eps"]:
            c.Print("%s/%s%s"%(_dirname,myPlotName,suffix))
        ROOT.gErrorIgnoreLevel = backup

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
            if "Up" in uncName and uncName != "" and not "stat_binByBin" in uncName:
                self._uncertaintyShapes.append(uncName)

    def debug(self):
        print "name =",self._name
        print "uncertainties = %s"%(", ".join(map(str, self._uncertaintyShapes)))

    def doPlot(self, opts, myAllShapeNuisances, f, mass, luminosity):
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
        x = 0.6
        size = 20
        myRatioContainer = RatioPlotContainer(self._name)
        for uncName in self._uncertaintyShapes:
            myShortName = uncName.replace("Up","")[1:]
            print "... uncertainty:",myShortName
            up = f.Get("%s%s"%(self._name,uncName))
            nom = hNominal.Clone()
            down = f.Get("%s%s"%(self._name,uncName.replace("Up","Down")))
            up.SetLineColor(ROOT.kRed)
            nom.SetLineColor(ROOT.kBlack)
            down.SetLineColor(ROOT.kBlue)
            upHisto = histograms.Histo(up, "Up %.1f"%_integral(up), drawStyle="HIST", legendStyle="l")
            downHisto = histograms.Histo(down, "Down %.1f"%_integral(down), drawStyle="HIST", legendStyle="l")
            nomHisto = histograms.Histo(nom, "Nominal %.1f"%_integral(nom), drawStyle="HIST", legendStyle="l")
            plot = plots.ComparisonManyPlot(nomHisto, [upHisto, downHisto])
            plot.setLuminosity(luminosity)
            plot.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetLineWidth(3))
            myPlotName = "%s/shapeSyst_%s_syst%s" % (_dirname, self._name, uncName.replace("Up",""))
            myParams = {}
            myParams["ylabel"] = "Events"
            myParams["log"] = False
            myParams["opts2"] = {"ymin": 0.0, "ymax":2.0}
            myParams["opts"] = {"ymin": 0.0}
            myParams["ratio"] = True
            myParams["ratioType"] = "errorScale"
            myParams["ratioYlabel"] = "Var./Nom."
            myParams["cmsText"] = myCMSText
            myParams["addLuminosityText"] = True
            plots.drawPlot(plot, myPlotName, **myParams)
            myRatioContainer.addRatioPlot(plot, myShortName)
        # Create plots with only the ratio plot
        if opts.individual:
            myRatioContainer.drawIndividually()
        else:
            myRatioContainer.drawAllInOne(myAllShapeNuisances, myCMSText, luminosity)

def doPlot(opts,mass,nameList,luminosity,rootFilePattern):
    f = ROOT.TFile.Open(rootFilePattern%mass)

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
            else:
                shapes.append(myPreviousKey)
        # Store old key
        myPreviousSplitList = splitList
        myPreviousKey = key.GetName()
        # Advance to next
        key = diriter.Next()

    # Obtain list of all shape nuisances
    myAllShapeNuisances = []
    for d in datasets:
        for s in d._uncertaintyShapes:
            myCleanS = s.replace("Up","")[1:]
            if not myCleanS in myAllShapeNuisances:
                myAllShapeNuisances.append(myCleanS)

    ## Do the actual plots
    for d in datasets:
        #d.debug()
        d.doPlot(opts,myAllShapeNuisances,f,mass,luminosity)
    # Close the file
    f.Close()

def _integral(h):
    return h.Integral()
    #    return h.Integral(0, h.GetNbinsX()+1)

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]",add_help_option=False,conflict_handler="resolve")
    parser.add_option("-h", "--help", dest="helpStatus", action="store_true", default=False, help="Show this help message and exit")
    parser.add_option("--individual", dest="individual", action="store_true", default=False, help="Generates individual plots for shape ratios instead of one large plot")
    (opts, args) = parser.parse_args()
    if opts.helpStatus:
        parser.print_help()
        sys.exit()

    # Create directory for plots
    if not os.path.exists(_dirname):
        os.mkdir(_dirname)
    # Apply TDR style
    style = tdrstyle.TDRStyle()
    histograms.createLegend.moveDefaults(dx=-0.1, dh=-0.15)
    # Find out the mass points
    myDatacardPattern = lands.taujetsDatacardPattern
    myRootFilePattern = lands.taujetsRootfilePattern
    if not os.path.exists(myDatacardPattern):
        myDatacardPattern = myDatacardPattern.replace("lands","combine")
        myRootFilePattern = myRootFilePattern.replace("lands","combine")
    massPoints = lands.obtainMassPoints(myRootFilePattern)
    print "The following masses are considered:",massPoints
    nameList = []
    for m in massPoints:
        # Obtain luminosity from datacard
        myLuminosity = float(lands.readLuminosityFromDatacard(".",myDatacardPattern%m))
        # Do plots
        doPlot(opts,int(m),nameList,myLuminosity,myRootFilePattern)
