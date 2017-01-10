#!/usr/bin/env python

import sys
import os
from optparse import OptionParser
import math
import array

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import HiggsAnalysis.LimitCalc.DatacardReader as DatacardReader
import HiggsAnalysis.LimitCalc.CommonLimitTools as limitTools
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux
import HiggsAnalysis.NtupleAnalysis.tools.styles as styles

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

    def drawAllInOne(self, myAllShapeNuisances, luminosity):
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
        if len(self._ratioPlotList) == 0:
            print "No ratioplots in list! Cannot draw all-in-one plot!"
            return
        o = self._ratioPlotList[0].getFrame2()
        myEmptyPlot = aux.Clone(o) # Keep the clone if it is needed to draw the x axis
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
#            plot.SetMinimum(0.001)
#            plot.SetMaximum(1.999)
            plot.SetMinimum(0.601)
            plot.SetMaximum(1.399)
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
            myHeight = 0.08
            if i == 0:
                myHeight = myHeight*float(_cBodyHeight) / float(_cHeaderHeight+_cBodyHeight)
            elif i == myMaxSize-1:
                myHeight = (myHeight*float(_cBodyHeight)+float(_cFooterHeight)) / float(_cFooterHeight +_cBodyHeight)
            histograms.addText(x=0.93, y=myHeight, text=self._dsetName, size=30, align="right")
            # Header labels
            if i == 0:
                histograms.addStandardTexts(lumi=luminosity, cmsTextPosition="outframe")
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

def customizeMarker(p):
    for h in p.ratioHistoMgr.getHistos():
        if h.getName() == "BackgroundStatError":
            continue

        h.setDrawStyle("P")
        th1 = h.getRootHisto()
        th1.SetMarkerSize(2)
        th1.SetMarkerStyle(34) # or 2?
        th1.SetMarkerColor(th1.GetLineColor())
        #th1.SetLineWidth(0)
        # I have no idea why "P" above is not enough...
        #for i in xrange(1, th1.GetNbinsX()+1):
        #    th1.SetBinError(i, 0)
        # th1 is no longer a th1 but instead a TGraphAsymmErrors object
        for i in xrange(0, th1.GetN()):
            th1.SetPointEYhigh(i, 0)
            th1.SetPointEYlow(i, 0)

class DatasetContainer:
    def __init__(self, column, label, nuisances, cardReader):
        self._name = column
        self._label = label
        self._uncertaintyShapes = nuisances
        self._cardReader = cardReader

    def debug(self):
        print "name =",self._name
        print "uncertainties = %s"%(", ".join(map(str, self._uncertaintyShapes)))

    def doPlot(self, opts, myAllShapeNuisances, f, mass, luminosity, signalTable, rebinList=None):
        def rebin(h, rebinList):
            if rebinList == None or h == None:
                return h
            myArray = array.array("d",rebinList)
            hnew = h.Rebin(len(rebinList)-1,h.GetTitle(),myArray)
            h.Delete()
            return hnew
        
        print "Doing plots for:",self._name
        hNominal = f.Get(self._cardReader.getHistoNameForColumn(self._name))
        hNominal = rebin(hNominal, rebinList)
        hNominal.SetFillStyle(0)
        hNominalFine = f.Get(self._cardReader.getHistoNameForColumn(self._name)+"_fineBinning")
        hNominalFine = rebin(hNominalFine, rebinList)
        hNominalHisto = histograms.Histo(hNominal, self._name, drawStyle="HIST")
        # Determine label
        mySignalLabels = ["HH","HW","Hp"]
        mySignalStatus = False
        for l in mySignalLabels:
            if l in self._name:
                mySignalStatus = True
        myMCLabels = ["HH","HW","Hp","MC"]
        myMCStatus = False
        
        for mclab in myMCLabels:
            if mclab in self._name:
                myMCStatus = True
        histograms.cmsTextMode = histograms.CMSMode.PRELIMINARY
        if myMCStatus:
            histograms.cmsTextMode = histograms.CMSMode.SIMULATION_PRELIMINARY
        x = 0.6
        size = 20
        myRatioContainer = RatioPlotContainer(self._label)
        for uncName in self._uncertaintyShapes:
            myShortName = uncName
            print "... uncertainty:",myShortName
            myLongName = self._cardReader.getHistoNameForNuisance(self._name, uncName)
            hup = f.Get("%sUp"%(myLongName))
            hup = rebin(hup, rebinList)
            hup.SetFillStyle(0)
            up = dataset.RootHistoWithUncertainties(hup)
            upFine = f.Get("%sUp_fineBinning"%(myLongName))
            upFine = rebin(upFine, rebinList)
            nom = dataset.RootHistoWithUncertainties(hNominal.Clone())
            nom.makeFlowBinsVisible()
            hdown = f.Get("%sDown"%(myLongName))
            hdown = rebin(hdown, rebinList)
            hdown.SetFillStyle(0)
            down = dataset.RootHistoWithUncertainties(hdown)
            downFine = f.Get("%sDown_fineBinning"%(myLongName))
            downFine = rebin(downFine, rebinList)
            up.getRootHisto().SetLineColor(ROOT.kRed)
            nom.getRootHisto().SetLineColor(ROOT.kBlack)
            down.getRootHisto().SetLineColor(ROOT.kBlue)
            upHisto = histograms.Histo(up, "Up %.1f"%_integral(up.getRootHisto()), drawStyle="HIST", legendStyle="l")
            downHisto = histograms.Histo(down, "Down %.1f"%_integral(down.getRootHisto()), drawStyle="HIST", legendStyle="l")
            nomHisto = histograms.Histo(nom, "Nominal %.1f"%_integral(nom.getRootHisto()), drawStyle="HIST", legendStyle="l")
            # Add fit uncert. as stat uncert.
            for i in range(0,9):
                tailFitUp = f.Get("%s_TailFit_par%dUp"%(myLongName,i))
                tailFitDown = f.Get("%s_TailFit_par%dDown"%(myLongName,i))
                if tailFitUp != None and tailFitDown != None:
                    nom.addShapeUncertaintyFromVariation("%s_TailFit_par%d"%(self._name,i),tailFitUp,tailFitDown)
                    tailFitUp.Delete()
                    tailFitDown.Delete()
            tailfitNames = filter(lambda n: "_TailFit_" in n, nom.getShapeUncertaintyNames())
            nom.setShapeUncertaintiesAsStatistical(tailfitNames)
            # Do plot
            plot = plots.ComparisonManyPlot(nomHisto, [upHisto, downHisto])
            plot.setLuminosity(luminosity)
            plot.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetLineWidth(3))
            myPlotName = "%s/shapeSyst_%s_syst%s" % (_dirname, self._label, uncName.replace("Up",""))
            myParams = {}
            myParams["ylabel"] = "Events"
            myParams["log"] = False
            #myParams["opts2"] = {"ymin": 0.0, "ymax":2.0}
<<<<<<< HEAD
            myParams["opts2"] = {"ymin": 0.0, "ymax":2.0}
            myParams["opts"] = {"ymin": 0.0}
=======
            myParams["opts2"] = {"ymin": 0.7, "ymax":1.3}
            myParams["opts"] = {"ymin": 0.0, "xmax":1000.0}
>>>>>>> public/master
            if opts.logx:
                myParams["opts"] = {"ymin": 10.0, "xmax":5000.0}
                myParams["logx"] = True
            if opts.light:
<<<<<<< HEAD
                myParams["opts"] = {"ymin": 0.0, "xmax":1000.0}
            else:
                myParams["opts"] = {"ymin": 0.0, "xmax":6000.0}
=======
                myParams["opts"] = {"ymin": 0.0, "xmax":500.0}
>>>>>>> public/master
            myParams["ratio"] = True
            myParams["ratioType"] = "errorScale"
            myParams["ratioYlabel"] = "Var./Nom."
            myParams["addLuminosityText"] = True
            myParams["customizeBeforeDraw"] = customizeMarker
            #myParams["ratioErrorOptions"] = {"numeratorStatSyst": False}
            myParams["addMCUncertainty"] = True
            
            plots.drawPlot(plot, myPlotName, **myParams)
            myRatioContainer.addRatioPlot(plot, myShortName)
            # Analyse up and down variation
            if mySignalStatus and upFine != None and downFine != None:
                a = abs(upFine.Integral()/hNominalFine.Integral() - 1.0)
                b = abs(1.0 - downFine.Integral()/hNominalFine.Integral())
                r = a
                if b > a:
                    r = b
                if uncName in signalTable.keys():
                    if r < signalTable[uncName]["min"]:
                        signalTable[uncName]["min"] = r
                    if r > signalTable[uncName]["max"]:
                        signalTable[uncName]["max"] = r
                else:
                    signalTable[uncName] = {}
                    signalTable[uncName]["min"] = r
                    signalTable[uncName]["max"] = r
            
        # Create plots with only the ratio plot
        if opts.individual:
            myRatioContainer.drawIndividually()
        else:
            myRatioContainer.drawAllInOne(myAllShapeNuisances, luminosity)

def doPlot(opts,mass,nameList,allShapeNuisances,luminosity,myDatacardPattern,rootFilePattern,signalTable):
    f = ROOT.TFile.Open(rootFilePattern%mass)

    content = f.GetListOfKeys()
    # Suppress the warning message of missing dictionary for some iterator
    backup = ROOT.gErrorIgnoreLevel
    ROOT.gErrorIgnoreLevel = ROOT.kError
    diriter = content.MakeIterator()
    ROOT.gErrorIgnoreLevel = backup

    # Find the datacard and nuisance names
    myCardReader = DatacardReader.DataCardReader(".", mass, myDatacardPattern, rootFilePattern)
    myDatasetNames = myCardReader.getDatasetNames()
    # Find the name stem and the name of the uncertainties
    datasets = []
    shapes = []
    for d in myDatasetNames:
        myLabel = d
        myStatus = not d in nameList
        if d == myDatasetNames[0]:
            myStatus = True
            if not str(mass) in d:
                myLabel = "%sm%d"%(d,mass)
        
        myShapeNuisanceNames = myCardReader.getShapeNuisanceNames(d)
        myFilteredShapeNuisances = []
        for n in myShapeNuisanceNames:
            if not "statBin" in n and not n.endswith("_statUp") and not n.endswith("_statDown"):
                myFilteredShapeNuisances.append(n)
        if myStatus:
            myDataset = DatasetContainer(column=d, label=myLabel, nuisances=myFilteredShapeNuisances, cardReader=myCardReader)
            datasets.append(myDataset)
            nameList.append(d)
        for n in myFilteredShapeNuisances:
            if not n in shapes:
                shapes.append(n)

    rebinList = None
    #rebinList = [0,200,250,300,350,400,450,500,550,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,2000,2100,2200,2300,2400,2500]

    ## Do the actual plots
    for d in datasets:
        #d.debug()
        d.doPlot(opts,shapes,f,mass,luminosity,signalTable,rebinList)
    # Close the file
    f.Close()

def _integral(h):
    return h.Integral()
    #    return h.Integral(0, h.GetNbinsX()+1)

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]",add_help_option=False,conflict_handler="resolve")
    parser.add_option("-h", "--help", dest="helpStatus", action="store_true", default=False, help="Show this help message and exit")
    parser.add_option("--individual", dest="individual", action="store_true", default=False, help="Generates individual plots for shape ratios instead of one large plot")
    parser.add_option("--cardpattern", dest="cardPattern", action="store", default=None, help="Pattern of datacard with MM denoting mass value")
    parser.add_option("--rootfilepattern", dest="rootfilePattern", action="store", default=None, help="Pattern of root file with MM denoting mass value")
    parser.add_option("--logx", dest="logx", action="store_true", default=False, help="Plot x-axis (mT) as logarithmic (good for heavy H+ analysis)")
    parser.add_option("--light", dest="light", action="store_true", default=False, help="Plot x-axis (mT) only up to 500 GeV (good for light H+ analysis)")    
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
    histograms.uncertaintyMode.set(histograms.Uncertainty.StatOnly)
    styles.ratioLineStyle.append(styles.StyleLine(lineColor=13))
    # Find out the mass points
   
    nameList = []
    allShapeNuisances = []
    signalTable = {}
    myDatacardPattern = ""
    myRootfilePattern = ""
    if opts.cardPattern == None:
        mySettings = limitTools.GeneralSettings(".",[])
        myDatacardPattern = mySettings.getDatacardPattern(limitTools.LimitProcessType.TAUJETS)
        myRootfilePattern = mySettings.getRootfilePattern(limitTools.LimitProcessType.TAUJETS)
    else:
        myDatacardPattern = opts.cardPattern.replace("MMM","M%s").replace("MM","%s")
        myRootfilePattern = opts.rootfilePattern.replace("MMM","M%s").replace("MM","%s")
    massPoints = DatacardReader.getMassPointsForDatacardPattern(".", myDatacardPattern)
    print "The following masses are considered:",massPoints
    for m in massPoints:
        # Obtain luminosity from datacard
        myLuminosity = float(limitTools.readLuminosityFromDatacard(".",myDatacardPattern%m))
        # Do plots
        doPlot(opts,int(m),nameList,allShapeNuisances,myLuminosity,myDatacardPattern,myRootfilePattern,signalTable)
    # Print signal table
    print "Max contracted uncertainty for signal:"
    for k in signalTable.keys():
        print "Key: "+str(k)
        print "%s, %.3f--%.3f"%(k, signalTable[k]["min"],signalTable[k]["max"])
