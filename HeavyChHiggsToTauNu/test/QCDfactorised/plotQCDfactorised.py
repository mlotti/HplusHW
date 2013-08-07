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
from HiggsAnalysis.HeavyChHiggsToTauNu.qcdCommon.systematicsForMetShapeDifference import *
from HiggsAnalysis.HeavyChHiggsToTauNu.qcdFactorised.qcdFactorisedResult import *
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShapeHistoModifier import *

myHistoSpecs = { "bins": 13,
                 "rangeMin": 0.0,
                 "rangeMax": 500.0,
                 #"variableBinSizeLowEdges": [], # if an empty list is given, then uniform bin width is used
                 "variableBinSizeLowEdges": [0,20,40,60,80,100,120,140,160,200,250,300,400], # if an empty list is given, then uniform bin width is used
                 "xtitle": "Transverse mass / GeV",
                 "ytitle": "Events" }

myMETSpecs           = { "bins": 13,
                         "rangeMin": 0.0,
                         "rangeMax": 500.0,
                         #"variableBinSizeLowEdges": [0,20,40,60,80,100,120,140,160,180,200,250,300], # if an empty list is given, then uniform bin width is used
                         "variableBinSizeLowEdges": [0,20,40,60,80,100,120,140,160,180,200,250,300], # if an empty list is given, then uniform bin width is used
                         "xtitle": "E_{T}^{miss}",
                         "ytitle": "Events"}

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
    myResult = QCDFactorisedResult(myBasicShape, myLeg1Shape, myLeg2Shape, myHistoSpecs, moduleInfoString)
    hTotalQCD = myResult.getResultShape().Clone()

    # Do plotting - this needs to be edited to use tdr style ...
    c1 = ROOT.TCanvas()
    c1.Draw()
    hTotalQCD.Draw()
    c1.Print("%s/QCDShape_total_%s.png"%(myDir, moduleInfoString))
    for i in range(0,len(myResult.getNQCDHistograms())):
        c = ROOT.TCanvas()
        c.Draw()
        myResult.getNQCDHistograms()[i].Draw()
        myBinTitle = myBasicShape.getPhaseSpaceBinFileFriendlyTitle(i)
        c.Print("%s/QCDShape_%s_%s.png"%(myDir, myBinTitle, moduleInfoString))

    # Do systematics coming from met shape difference
    # Set here the names of the histograms you want to access
    myCtrlRegionName = "QCDfactorised/MtAfterStandardSelections"
    mySignalRegionName = "QCDfactorised/MtAfterLeg2"
    # Obtain QCD shapes
    myCtrlRegion = DataDrivenQCDShape(dsetMgr, "Data", "EWK", myCtrlRegionName, luminosity)
    mySignalRegion = DataDrivenQCDShape(dsetMgr, "Data", "EWK", mySignalRegionName, luminosity)
    # Calculate
    mySyst = SystematicsForMetShapeDifference(mySignalRegion, myCtrlRegion, myResult.getResultShape(), myHistoSpecs, moduleInfoString)
    print "Evaluated MET shape systematics"
    # Do plotting
    #mySyst
    c2 = ROOT.TCanvas()
    c2.Draw()
    hNominal = myResult.getResultShape().Clone()
    hUp = mySyst.getUpHistogram().Clone()
    hDown = mySyst.getDownHistogram().Clone()
    hNominal.SetLineColor(ROOT.kBlack)
    hUp.SetLineColor(ROOT.kBlue)
    hDown.SetLineColor(ROOT.kRed)
    hNominal.Draw()
    hUp.Draw("same")
    hDown.Draw("same")
    c2.Print("%s/QCDShapeWithMetSyst_%s_%s.png"%(myDir, myBinTitle, moduleInfoString))

    print HighlightStyle()+"doQCDfactorisedResultPlots is ready"+NormalStyle()

def doDataDrivenControlPlot(opts, dsetMgr, moduleInfoString, myDir, luminosity):
    myBasicName = "QCDfactorised/MtAfterStandardSelections"
    myLeg1Name = "QCDfactorised/MtAfterLeg1"
    myLeg2Name = "QCDfactorised/MtAfterLeg2"
    # Obtain QCD shapes
    myBasicShape = DataDrivenQCDShape(dsetMgr, "Data", "EWK", myBasicName, luminosity)
    myLeg1Shape = DataDrivenQCDShape(dsetMgr, "Data", "EWK", myLeg1Name, luminosity)
    myLeg2Shape = DataDrivenQCDShape(dsetMgr, "Data", "EWK", myLeg2Name, luminosity)
    # Obtain control plot (myBasicShape and myLeg2Shape are summed first)
    myPlotContainer = QCDControlPlot(myBasicShape, myLeg1Shape, myLeg2Shape, myMETSpecs, moduleInfoString)

    myBasicName = "QCDfactorised/MtAfterStandardSelections"
    myLeg1Name = "QCDfactorised/MtAfterLeg1"
    myLeg2Name = "QCDfactorised/MtAfterLeg2"
    # Obtain QCD shapes
    myBasicShape = DataDrivenQCDShape(dsetMgr, "Data", "EWK", myBasicName, luminosity)
    myLeg1Shape = DataDrivenQCDShape(dsetMgr, "Data", "EWK", myLeg1Name, luminosity)
    myLeg2Shape = DataDrivenQCDShape(dsetMgr, "Data", "EWK", myLeg2Name, luminosity)
    myPlotContainerVariant = QCDFactorisedResult(myBasicShape, myLeg1Shape, myLeg2Shape, myMETSpecs, moduleInfoString+myLeg1Name.replace("/",""))

    c1 = ROOT.TCanvas()
    c1.Draw()
    hMET1 = myPlotContainer.getResultShape()
    hMET2 = myPlotContainerVariant.getResultShape()
    hMET2.SetLineColor(ROOT.kRed)
    hMET1.Draw()
    hMET2.Draw("same")
    c1.Print("%s/CtrlPlotMETTest_%s.png"%(myDir, moduleInfoString))


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
                #doPurityPlots(opts, dsetMgr, myModuleInfoString, myDir, myLuminosity)
                #doQCDfactorisedResultPlots(opts, dsetMgr, myModuleInfoString, myDir, myLuminosity)
                doDataDrivenControlPlot(opts, dsetMgr, myModuleInfoString, myDir, myLuminosity)
