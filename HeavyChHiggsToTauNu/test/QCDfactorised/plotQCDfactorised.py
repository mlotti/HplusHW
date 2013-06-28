#!/usr/bin/env python

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True
import math
import sys
import os
from optparse import OptionParser

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.analysisModuleSelector import *
from HiggsAnalysis.HeavyChHiggsToTauNu.qcdCommon.dataDrivenQCDCount import *
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShapeHistoModifier import *

myHistoSpecs = { "bins": 13,
                 "rangeMin": 0.0,
                 "rangeMax": 500.0,
                 #"variableBinSizeLowEdges": [], # if an empty list is given, then uniform bin width is used
                 "variableBinSizeLowEdges": [0,20,40,60,80,100,120,140,160,200,250,300,400], # if an empty list is given, then uniform bin width is used
                 "xtitle": "Transverse mass / GeV",
                 "ytitle": "Events" }


def doPurityPlots(opts, dsetMgr, moduleInfoString, myDir, luminosity):
    # Set here the names of the histograms you want to access
    histoNameList = ["QCDfactorised/MtAfterStandardSelections",
                     "QCDfactorised/MtAfterLeg1",
                     "QCDfactorised/MtAfterLeg2",
                     "shapeTransverseMass" # should be the same as mt after leg 1
                    ]

    for histoName in histoNameList:
        print histoName
        myQCDShape = DataDrivenQCDShape(dsetMgr, "Data", "EWK", histoName, luminosity)
        # Get integrated purity
        myIntegratedPurity = myQCDShape.getIntegratedPurity()
        print "Module: %s / histogram %s : integrated purity = %f +- %f"%(moduleInfoString, histoName, myIntegratedPurity.value(), myIntegratedPurity.uncertainty())
        # Get purity as function of splitted phase space bin
        hPurityBySplittedBin = myQCDShape.getPurityHisto()
        # Get integrated purity as function of the shape bins
        hPurityByFinalShapeBin = myQCDShape.getIntegratedPurityForShapeHisto(myHistoSpecs)

        # Do plotting - this needs to be edited to use tdr style ...
        c1 = ROOT.TCanvas()
        c1.Draw()
        hPurityBySplittedBin.Draw()
        c1.Print("%s/purityBySplittedBin_%s_%s.png"%(myDir, histoName.replace("/","_"), moduleInfoString))
        c2 = ROOT.TCanvas()
        c2.Draw()
        hPurityByFinalShapeBin.Draw()
        c2.Print("%s/purityByFinalShapeBin_%s_%s.png"%(myDir, histoName.replace("/","_"), moduleInfoString))
    print HighlightStyle()+"doPurityPlots is ready"+NormalStyle()

def doQCDfactorisedResultPlots(opts, dsetMgr, moduleInfoString, myDir, luminosity):
    # Set here the names of the histograms you want to access
    myBasicName = "QCDfactorised/MtAfterStandardSelections"
    myLeg1Name = "QCDfactorised/MtAfterLeg1"
    myLeg2Name = "QCDfactorised/MtAfterLeg2"

    # Obtain QCD shapes
    myBasicShape = DataDrivenQCDShape(dsetMgr, "Data", "EWK", myBasicName, luminosity)
    myLeg1Shape = DataDrivenQCDShape(dsetMgr, "Data", "EWK", myLeg1Name, luminosity)
    myLeg2Shape = DataDrivenQCDShape(dsetMgr, "Data", "EWK", myLeg2Name, luminosity)

    # Calculate final shape in signal region (leg1 * leg2 / basic)
    nSplitBins = myBasicShape.getNumberOfPhaseSpaceSplitBins()
    myModifier = ShapeHistoModifier(myHistoSpecs)
    hTotalQCD = myModifier.createEmptyShapeHistogram("NQCD_Total_%s"%moduleInfoString)
    myBinQCDList = []
    for i in range(0, nSplitBins):
        hBin = myModifier.createEmptyShapeHistogram("NQCD_%s_%s"%(myBasicShape.getPhaseSpaceBinFileFriendlyTitle(i).replace(" ",""), moduleInfoString))
        myBinQCDList.append(hBin)
    for i in range(0, nSplitBins):
        hBasic = myBasicShape.getDataDrivenQCDHistoForSplittedBin(i, myHistoSpecs)
        hLeg1 = myLeg1Shape.getDataDrivenQCDHistoForSplittedBin(i, myHistoSpecs)
        hLeg2 = myLeg2Shape.getDataDrivenQCDHistoForSplittedBin(i, myHistoSpecs)
        for j in range(1,hBasic.GetNbinsX()+1):
            myResult = 0.0
            myStatUncertSquared = 0.0
            if hBasic.GetBinContent(j) > 0.0:
                # Calculate result
                myResult = abs(hLeg1.GetBinContent(j) * hLeg2.GetBinContent(j) / hBasic.GetBinContent(j))
                # Calculate abs. stat. uncert.
                myStatUncertSquared = ((hLeg1.GetBinError(j) * hLeg2.GetBinContent(j))**2 + (hLeg2.GetBinError(j) * hLeg1.GetBinContent(j))**2) / hBasic.GetBinContent(j)**2
                # Treat negative numbers
                if hLeg1.GetBinContent(j) < 0.0 or hLeg2.GetBinContent(j) < 0.0 or hBasic.GetBinContent(j) < 0.0:
                    myResult = -myResult;
            myBinQCDList[i].SetBinContent(j, myResult)
            myBinQCDList[i].SetBinError(j, sqrt(myStatUncertSquared))
            hTotalQCD.SetBinContent(j, hTotalQCD.GetBinContent(j) + myResult)
            hTotalQCD.SetBinError(j, hTotalQCD.GetBinError(j) + myStatUncertSquared) # Sum squared
    # Take square root of uncertainties
    myModifier.finaliseShape(dest=hTotalQCD)
    # Print result
    nQCD = 0.0
    nQCDStatUncert = 0.0
    for i in range(1, hTotalQCD.GetNbinsX()+1):
        nQCD += hTotalQCD.GetBinContent(i)
        nQCDStatUncert += hTotalQCD.GetBinError(i)**2
    nQCDStatUncert = sqrt(nQCDStatUncert)
    # To obtain syst. uncert. for EWK is quite a bit more difficult. Will develop it later.
    print "NQCD = %f +- %f (stat.)"%(nQCD, nQCDStatUncert)

    # Do plotting - this needs to be edited to use tdr style ...
    c1 = ROOT.TCanvas()
    c1.Draw()
    hTotalQCD.Draw()
    c1.Print("%s/QCDShape_total_%s.png"%(myDir, moduleInfoString))
    for i in range(0,len(myBinQCDList)):
        c = ROOT.TCanvas()
        c.Draw()
        myBinQCDList[i].Draw()
        myBinTitle = myBasicShape.getPhaseSpaceBinFileFriendlyTitle(i)
        c.Print("%s/QCDShape_%s_%s.png"%(myDir, myBinTitle, moduleInfoString))
    print HighlightStyle()+"doQCDfactorisedResultPlots is ready"+NormalStyle()

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
    # Add here parser options, if necessary, following line is an example
    #parser.add_option("--showcard", dest="showDatacard", action="store_true", default=False, help="Print datacards also to screen")

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

    myDisplayStatus = True
    # Loop over era/searchMode/optimizationMode options
    for era in myModuleSelector.getSelectedEras():
        for searchMode in myModuleSelector.getSelectedSearchModes():
            for optimizationMode in myModuleSelector.getSelectedOptimizationModes():
                # Construct info string of module
                myModuleInfoString = "%s_%s_%s"%(era, searchMode, optimizationMode)
                print HighlightStyle()+"Module:",myModuleInfoString,NormalStyle()
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
                # Make a directory for output
                myDir = "plots_%s"%myModuleInfoString
                createOutputdirectory(myDir)
                # Obtain luminosity
                myLuminosity = dsetMgr.getDataset("Data").getLuminosity()
                # Print info so that user can check that merge went correct
                if myDisplayStatus:
                    dsetMgr.printDatasetTree()
                    print "Luminosity = %f 1/fb"%(myLuminosity / 1000.0)
                    print
                    myDisplayStatus = False
                # Run plots
                doPurityPlots(opts, dsetMgr, myModuleInfoString, myDir, myLuminosity)
                doQCDfactorisedResultPlots(opts, dsetMgr, myModuleInfoString, myDir, myLuminosity)
