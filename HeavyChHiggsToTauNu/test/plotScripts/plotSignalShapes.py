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

# Set here the names of the histograms you want to access
histoNameList = ["shapeTransverseMass",
                 "shapeInvariantMass",
                 "ForDataDrivenCtrlPlots/SelectedTau_pT_AfterMtSelections",
                 "ForDataDrivenCtrlPlots/METAfterMtSelections"]

lightMassSamples = ["TTToHplusBWB_M80",
                    "TTToHplusBWB_M120",
                    "TTToHplusBWB_M160",
                    ]
heavyMassSamples = ["HplusTB_M180",
                    "HplusTB_M220",
                    "HplusTB_M300",
                    #"HplusTB_M600",
                    ]

optionRemoveStatUncert = True

def doSinglePlot(histograms, myDir, histoName, luminosity, suffix):
    plot = plots.PlotBase(histograms)
    plot.setLuminosity(luminosity)
    plot.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetLineWidth(3))
    mySplit = histoName.split("/")
    histoNameShort = mySplit[len(mySplit)-1]
    myPlotName = "%s/signalShapes_%s_%s"%(myDir, suffix, histoNameShort)
    print myPlotName
    myParams = {}
    myParams["ylabel"] = "Events"
    if histoName.startswith("shape"):
        myParams["log"] = False
    else:
        myParams["log"] = True
    #myParams["opts2"] = {"ymin": 0.0, "ymax":2.0}
    #myParams["opts"] = {"ymin": 0.0, "ymax":1.0}
    #myParams["ratio"] = True
    #myParams["ratioType"] = "errorScale"
    #myParams["ratioYlabel"] = "Var./Nom."
    myParams["cmsText"] = "CMS simulation"
    myParams["addLuminosityText"] = True
    myParams["moveLegend"] = {"dx": -0.05, "dy": 0.0}
    #myParams["createLegend"] = None
    #myParams["divideByBinWidth"] = True
    plots.drawPlot(plot, myPlotName, **myParams)

def getPlots(opts, histoName, dsetMgr, myDir, luminosity, myHistograms, samples):
    def handleOverflow(h):
        h.SetBinContent(1, h.GetBinContent(0)+h.GetBinContent(1))
        h.SetBinError(1, math.sqrt(h.GetBinContent(0)**2 + h.GetBinContent(1)**2))
        h.SetBinContent(h.GetNbinsX()+1, h.GetBinContent(h.GetNbinsX()+1)+h.GetBinContent(h.GetNbinsX()+2))
        h.SetBinError(h.GetNbinsX()+1, math.sqrt(h.GetBinError(h.GetNbinsX()+1)**2 + h.GetBinError(h.GetNbinsX()+2)**2))
        h.SetBinContent(0, 0.0)
        h.SetBinError(0, 0.0)
        h.SetBinContent(h.GetNbinsX()+2, 0.0)
        h.SetBinError(h.GetNbinsX()+2, 0.0)

    for sample in samples:
        dseth = dsetMgr.getDataset(sample).getDatasetRootHisto(histoName)
        dseth.normalizeToLuminosity(luminosity)
        h = dseth.getHistogram()
        # Get short name
        mySplit = histoName.split("/")
        histoNameShort = mySplit[len(mySplit)-1]
        # Rebin and handle overflow
        if histoName.startswith("shape"):
            h = h.Rebin(2)
        #myBinning = systematics.getBinningForPlot(histoNameShort)
        #myArray = array.array("d",myBinning)
        #h = h.Rebin(len(myBinning)-1,"",myArray)
        handleOverflow(h)
        # Plot
        h.SetLineColor(styles.styles[len(myHistograms)].color)
        h.SetMarkerColor(styles.styles[len(myHistograms)].color)
        h.SetMarkerStyle(styles.styles[len(myHistograms)].marker)

        # Remove stat uncert
        if optionRemoveStatUncert:
            for i in range(1, h.GetNbinsX()+1):
                h.SetBinError(i, 0.0)

        myMass = sample.split("_")
        histo = histograms.Histo(h, "H^{+}, m=%s"%myMass[len(myMass)-1].replace("M",""), drawStyle="", legendStyle="lp")
        myHistograms.append(histo)

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
            for optimizationMode in myModuleSelector.getSelectedOptimizationModes():
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
                            # Construct info string of module
            myModuleInfoString = "%s_%s_%s"%(era, searchMode, optimizationMode)
            # Make a directory for output
            myDir = "signalShapes_%s"%myModuleInfoString
            createOutputdirectory(myDir)
            for histoName in histoNameList:
                print HighlightStyle()+"Module:",myModuleInfoString,"histogram:",histoName,NormalStyle()
                # Run light mass plots
                myHistograms = []
                getPlots(opts, histoName, dsetMgr, myDir, myLuminosity, myHistograms, lightMassSamples)
                doSinglePlot(myHistograms, myDir, histoName, myLuminosity, "Light")
                # Run heavy mass plots
                myHistograms = []
                getPlots(opts, histoName, dsetMgr, myDir, myLuminosity, myHistograms, heavyMassSamples)
                doSinglePlot(myHistograms, myDir, histoName, myLuminosity, "Heavy")
