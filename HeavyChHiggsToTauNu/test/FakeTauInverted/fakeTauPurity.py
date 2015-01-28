#!/usr/bin/env python

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True
import math
import array
import sys
import os
from optparse import OptionParser

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.aux as aux
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.systematics as systematics
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.analysisModuleSelector import *
from HiggsAnalysis.HeavyChHiggsToTauNu.qcdCommon.dataDrivenQCDCount import *
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShellStyles import *

# Set here the names of the histograms you want to access
#histoNameList = ["shapeTransverseMass",
#                 "shapeInvariantMass",
#                 "ForDataDrivenCtrlPlots/SelectedTau_pT_AfterMtSelections"]
histoNameList = ["shapeTransverseMass", "shapeEWKGenuineTausTransverseMass"]

def doSinglePlot(histograms, myDir, histoName, luminosity):
    plot = plots.PlotBase(histograms)
    plot.setLuminosity(luminosity)
    plot.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetLineWidth(3))
    mySplit = histoName.split("/")
    histoName = mySplit[len(mySplit)-1]
    myPlotName = "%s/QCDInv_Purity_%s"%(myDir, histoName)
    print myPlotName
    myParams = {}
    if "EWKGenuineTaus" in histoName:
        myParams["ylabel"] = "Fake #tau purity"
        myParams["moveLegend"] = {"dx": -0.05, "dy": -0.46}
    else:
        myParams["ylabel"] = "QCD purity"
        myParams["moveLegend"] = {"dx": -0.05, "dy": 0.0}
    myParams["log"] = False
    #myParams["opts2"] = {"ymin": 0.0, "ymax":2.0}
    myParams["opts"] = {"ymin": 0.0, "ymax":1.2}
    #myParams["ratio"] = True
    #myParams["ratioType"] = "errorScale"
    #myParams["ratioYlabel"] = "Var./Nom."
    #myParams["cmsText"] = "CMS"
    myParams["addLuminosityText"] = True
    #myParams["createLegend"] = None
    #myParams["divideByBinWidth"] = True
    myParams["errorBarsX"] = True
    plots.drawPlot(plot, myPlotName, **myParams)

def doPurityPlots(opts, histoName, dsetMgr, moduleInfoString, myDir, luminosity, myShapePurityHistograms):
    def handleOverflow(h):
        h.SetBinContent(1, h.GetBinContent(0)+h.GetBinContent(1))
        h.SetBinError(1, math.sqrt(h.GetBinContent(0)**2 + h.GetBinContent(1)**2))
        h.SetBinContent(h.GetNbinsX()+1, h.GetBinContent(h.GetNbinsX()+1)+h.GetBinContent(h.GetNbinsX()+2))
        h.SetBinError(h.GetNbinsX()+1, math.sqrt(h.GetBinError(h.GetNbinsX()+1)**2 + h.GetBinError(h.GetNbinsX()+2)**2))
        h.SetBinContent(0, 0.0)
        h.SetBinError(0, 0.0)
        h.SetBinContent(h.GetNbinsX()+2, 0.0)
        h.SetBinError(h.GetNbinsX()+2, 0.0)

    myQCDShape = DataDrivenQCDShape(dsetMgr, "Data", "EWK", histoName, luminosity)
    mySplit = histoName.split("/")
    histoName = mySplit[len(mySplit)-1]
    # Get data and EWK histograms
    hData = myQCDShape.getIntegratedDataHisto()
    hEWK = myQCDShape.getIntegratedEwkHisto()
    # Rebin and handle overflow
    if "EWKGenuineTaus" in histoName:
        myBinning = [0,20,40,60,80,100,120,140,160,200,300,700]
    else:
        myBinning = systematics.getBinningForPlot(histoName) #(histoName.replace("EWKGenuineTaus",""))
    myArray = array.array("d",myBinning)
    hData = hData.Rebin(len(myBinning)-1,"",myArray)
    hEWK = hEWK.Rebin(len(myBinning)-1,"",myArray)
    handleOverflow(hData)
    handleOverflow(hEWK)
    # Create purity histo
    hPurity = aux.Clone(hData)
    hPurity.Reset()
    # Calculate purity
    for i in xrange(1, hPurity.GetNbinsX()+1):
        myPurity = 0.0
        myUncert = 0.0
        nData = hData.GetBinContent(i)
        nEWK = hEWK.GetBinContent(i)
        if (nData > 0.0):
            myPurity = (nData - nEWK) / nData
            if myPurity < 0.0:
                myPurity = 0.0
                myUncert = 0.0
            else:
                myUncert = sqrt(myPurity * (1.0-myPurity) / nData) # Assume binomial error
        hPurity.SetBinContent(i, myPurity)
        hPurity.SetBinError(i, myUncert)
    # Find out tail killer scenario
    myScenario = ""
    if "QCDTailKillerLoose" in moduleInfoString:
        myScenario = "Loose"
    elif "QCDTailKillerMedium" in moduleInfoString:
        myScenario = "Medium"
    if "QCDTailKillerTight" in moduleInfoString:
        myScenario = "Tight"
    myScenario += " R_{bb}^{min.}"
    # Make histogram
    hPurity.SetLineColor(styles.styles[len(myShapePurityHistograms)].color)
    hPurity.SetMarkerColor(styles.styles[len(myShapePurityHistograms)].color)
    hPurity.SetMarkerStyle(styles.styles[len(myShapePurityHistograms)].marker)
    # Plot
    histo = histograms.Histo(hPurity, myScenario, drawStyle="", legendStyle="lp")
    myShapePurityHistograms.append(histo)

def createOutputdirectory(myDir):
    if os.path.exists(myDir):
        # Remove very old files
        for filename in os.listdir("%s/."%myDir):
            if filename[0:4] == "old_":
                os.remove("%s/%s"%(myDir,filename))
        # Rename remaining files
        for filename in os.listdir("%s/."%myDir):
            os.rename("%s/%s"%(myDir,filename), "%s/old_%s"%(myDir,filename))
    else:
        # Create directory since it does not exist
        os.mkdir(myDir)

if __name__ == "__main__":
    myModuleSelector = AnalysisModuleSelector() # Object for selecting data eras, search modes, and optimization modes

    parser = OptionParser(usage="Usage: %prog [options]",add_help_option=True,conflict_handler="resolve")
    myModuleSelector.addParserOptions(parser)
    parser.add_option("--mdir", dest="multicrabDir", action="store", help="Multicrab directory")

    # Parse options
    (opts, args) = parser.parse_args()

    # Obtain multicrab directory
    myMulticrabDir = "."
    if opts.multicrabDir != None:
        myMulticrabDir = opts.multicrabDir

    # Obtain dsetMgrCreator and register it to module selector
    dsetMgrCreator = dataset.readFromMulticrabCfg(directory=myMulticrabDir)
    myModuleSelector.setPrimarySource("analysis", dsetMgrCreator)
    # Select modules
    myModuleSelector.doSelect(opts)

    # Apply TDR style
    style = tdrstyle.TDRStyle()

    myDisplayStatus = True
    # Loop over era/searchMode/optimizationMode options
    for era in myModuleSelector.getSelectedEras():
        for searchMode in myModuleSelector.getSelectedSearchModes():
            # Construct info string of module
            myModuleInfoString = "%s_%s"%(era, searchMode)
            # Make a directory for output
            myDir = "purityplots_%s"%myModuleInfoString
            createOutputdirectory(myDir)
            for histoName in histoNameList:
                myShapePurityHistograms = []
                print HighlightStyle()+"Module:",myModuleInfoString,"histogram:",histoName,NormalStyle()
                for optimizationMode in myModuleSelector.getSelectedOptimizationModes():
                    if optimizationMode == "OptQCDTailKillerNoCuts":
                        continue
                    # Obtain dataset manager
                    dsetMgr = dsetMgrCreator.createDatasetManager(dataEra=era,searchMode=searchMode,optimizationMode=optimizationMode)
                    # Do the usual normalisation
                    dsetMgr.updateNAllEventsToPUWeighted()
                    dsetMgr.loadLuminosities()
                    plots.mergeRenameReorderForDataMC(dsetMgr)
                    dsetMgr.merge("EWK", [
                                  "TTJets",
                                  "WJets",
                                  "DYJetsToLL",
                                  "SingleTop",
                                  "Diboson"
                                  ])
                    # Obtain luminosity
                    myLuminosity = dsetMgr.getDataset("Data").getLuminosity()
                    # Print info so that user can check that merge went correct
                    if myDisplayStatus:
                        dsetMgr.printDatasetTree()
                        print "Luminosity = %f 1/fb"%(myLuminosity / 1000.0)
                        print
                        myDisplayStatus = False
                    # Run plots
                    doPurityPlots(opts, histoName, dsetMgr, optimizationMode, myDir, myLuminosity, myShapePurityHistograms)
                # Plot
                doSinglePlot(myShapePurityHistograms, myDir, histoName, myLuminosity)
