#!/usr/bin/env python

######################################################################
# All imported modules
######################################################################
# System modules
import sys
# ROOT modules
import ROOT
from ROOT import gStyle
# HPlus modules
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.cutstring import * # And, Not, Or
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
# Script-specific modules
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.QCDHistoHelper as Helper

######################################################################
# User options and global definitions
######################################################################
myValidDataEras = ["Run2011A", "Run2011B", "Run2011AB"]
myTailKillers   = ["ZeroPlus", "LoosePlus", "MediumPlus", "TightPlus"]
bBatchMode      = True
bAddLumiText    = True
sLegStyle       = "P"
sDrawStyle      = "EP"
yMinRatio       = 0.0
yMaxRatio       = 2.0
yMaxFactor      = 1.5
yMinLog         = 1E-01
yMinLogNorm     = 1E-04
yMaxFactorLog   = 5

myRootFilePath  = "info/QCDMeasurementFactorisedInfo.root" 
ROOT.gROOT.SetBatch(bBatchMode)

######################################################################
# Function declarations
######################################################################
def main():

    ##################
    # Mt shapes
    ##################
    MtShapesStdSelList = Helper.GetMtShapeHistoNames(sMyLeg="StandardSelections")
    doHistos(MtShapesStdSelList, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "MtShape_StdSel", bNormalizeToOne = False)    

    MtShapesLeg1List   = Helper.GetMtShapeHistoNames(sMyLeg="Leg1")
    doHistos(MtShapesLeg1List, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "MtShape_Leg1", bNormalizeToOne = False)

    MtShapesLeg2List   = Helper.GetMtShapeHistoNames(sMyLeg="Leg2")
    doHistos(MtShapesLeg2List, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "MtShape_Leg2", bNormalizeToOne = False)    

    # Closure test
    doHistosCompare(MtShapesStdSelList + MtShapesLeg2List, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "ClosureTest_Mt", bNormalizeToOne=True, bRatio=True, bInvertRatio=False)

    # Closure tests (bin)
    binList = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10] #bin 0 = underflow, bin 10 = overflow
    for index in binList:
        MtBinShapesStdSelList = Helper.GetMtBinShapeHistoNames(lBinList = [index], sMyLeg="StandardSelections")
        MtBinShapesLeg2List   = Helper.GetMtBinShapeHistoNames(lBinList = [index], sMyLeg="Leg2")
        doHistosCompare(MtBinShapesStdSelList + MtBinShapesLeg2List, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "ClosureTest_Mt_Bin" + str(index), bNormalizeToOne = True, bRatio=True, bInvertRatio=False)


    ##################
    # MET shapes
    ##################
    MetShapesStdSelList  = Helper.GetMetShapeHistoNames(sMyLeg="")
    doHistos(MetShapesStdSelList, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "MetShape_StdSel", bNormalizeToOne = False)

    #MetShapesLeg1List    = Helper.GetMetShapeHistoNames(sMyLeg="AfterLeg1")
    #doHistos(MetShapesLeg1List, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "MetShape_Leg1", bNormalizeToOne = False)    

    MetShapesLeg2List    = Helper.GetMetShapeHistoNames(sMyLeg="AfterLeg2")
    doHistos(MetShapesLeg2List, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "MetShape_Leg2", bNormalizeToOne = False)

    # Closure test
    doHistosCompare(MetShapesStdSelList + MetShapesLeg2List, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "ClosureTest_Met", bNormalizeToOne = True, bRatio=True, bInvertRatio=False)

    # Closure tests (bin)
    binList = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  #bin 0 = underflow, bin 10 = overflow
    for index in binList:
        MetBinShapesStdSelList = Helper.GetMetBinShapeHistoNames(lBinList = [index], sMyLeg="")
        MetBinShapesLeg2List   = Helper.GetMetBinShapeHistoNames(lBinList = [index], sMyLeg="AfterLeg2")
        doHistosCompare(MetBinShapesStdSelList + MetBinShapesLeg2List, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "ClosureTest_Met_Bin" + str(index), bNormalizeToOne = True, bRatio=True, bInvertRatio=False)
        

    return

######################################################################
def doHistos(HistoList, myPath, QCDscheme, ErrorType, mySaveName, bNormalizeToOne):
                
    # Determine the Tail-Killer scenario 
    myTailKiller = Helper.getTailKillerFromDir(myTailKillers)

    # Check the current working directory name for a valid data-era
    myDataEra = Helper.getDataEra(myValidDataEras)

    # Get the integrated luminosity of the data-era (only used for addind lumi text)
    myLumi = Helper.getLumi(myDataEra)

    # Check that the user-defined options are valid
    Helper.checkUserOptions(QCDscheme, ErrorType)

    # Get the ROOT file
    rootFile = Helper.getRootFile(myPath)

    # Plot all histograms defined in the HistoList    
    print "*** There are \"%s\" histogram(s) in the plotting queue (QCDscheme = \"%s\" , Tail-Killer = \"%s\"):" % (len(HistoList), QCDscheme, myTailKiller)
    for h in HistoList:

        pathName, histoName  = Helper.getHistoNameAndPath(QCDscheme, ErrorType, h)
        histo                = Helper.getHisto(rootFile, pathName)
        saveName             = Helper.getFullSaveName(myDataEra, myTailKiller, bNormalizeToOne, mySaveName)

        # Get histogram attributes as defined in QCDHistoHelper.py
        xLabel   = h.xLabel
        yLabel   = h.yLabel
        xMin     = h.xMin
        xMax     = h.xMax
        logX     = h.bLogX
        yMin     = h.yMin
        yMax     = h.yMax
        logY     = h.bLogY
        legendLabel = h.legendLabel
        
        # Create and draw the plots
        print "    Creating  \"%s\"" % (histoName)
        p = Helper.createPlot(histo, myLumi, legendLabel, sLegStyle, sDrawStyle)

        if bNormalizeToOne == True:
            p.histoMgr.forEachHisto(lambda h: dataset._normalizeToOne(h.getRootHisto()))
            yMinLog == yMinLogNorm
            saveName = saveName + "_normalizedToOne"

        # Customize the plots
        drawPlot = Helper.customizePlot(logY, bAddLumiText, False, False, "Ratio", yMin, yMax, yMaxFactor, yMinRatio, yMaxRatio, yMinLog, yMaxFactorLog)

        # Save the plots
        saveName = saveName.replace("Leg1", "MetLeg").replace("Leg2", "TauLeg").replace("leg1", "MetLeg").replace("leg2", "TauLeg").replace("After","")
        drawPlot(p, saveName, xlabel=xLabel, ylabel=yLabel, customizeBeforeDraw=Helper.setLabelOption)
        print "*** Saved \"%s\"\n" % (saveName)

    return

######################################################################
def doHistosCompare(HistoList, myPath, QCDscheme, ErrorType, mySaveName, bNormalizeToOne, bRatio, bInvertRatio):
                
    # Determine the Tail-Killer scenario 
    myTailKiller = Helper.getTailKillerFromDir(myTailKillers)

    # Check the current working directory name for a valid data-era
    myDataEra = Helper.getDataEra(myValidDataEras)

    # Get the integrated luminosity of the data-era (only used for addind lumi text)
    myLumi = Helper.getLumi(myDataEra)

    # Check that the user-defined options are valid
    Helper.checkUserOptions(QCDscheme, ErrorType)

    # Get the ROOT file
    rootFile = Helper.getRootFile(myPath)

    # Plot all histograms defined in the HistoList    
    print "*** There are \"%s\" histogram(s) in the plotting queue (QCDscheme = \"%s\" , Tail-Killer = \"%s\"):" % (len(HistoList), QCDscheme, myTailKiller)
    counter = 0
    for h in HistoList:

        pathName, histoName  = Helper.getHistoNameAndPath(QCDscheme, ErrorType, h)
        histo                = Helper.getHisto(rootFile, pathName)
        saveName             = Helper.getFullSaveName(myDataEra, myTailKiller, bNormalizeToOne, mySaveName)

        # Get histogram attributes as defined in QCDHistoHelper.py
        xLabel   = h.xLabel
        yLabel   = h.yLabel
        xMin     = h.xMin
        xMax     = h.xMax
        logX     = h.bLogX
        yMin     = h.yMin
        yMax     = h.yMax
        logY     = h.bLogY
        legendLabel = h.legendLabel
        legendHeader = h.legendHeader
        
        # Create and draw the plots
        if counter == 0:
            print "    Creating  \"%s\"" % (histoName)
            p = Helper.createPlot(histo, myLumi, legendLabel, sLegStyle, sDrawStyle)
            h = histograms.Histo(Helper.setHistoStyle(histo, counter), legendLabel, sLegStyle, sDrawStyle)
        else:
            if len(HistoList) <= 2:
                h = histograms.Histo(Helper.setHistoStyle(histo, counter), legendLabel, "f", "HIST")
            else:
                h = histograms.Histo(Helper.setHistoStyle(histo, counter), legendLabel, sLegStyle, sDrawStyle)
            histograms.Histo(h, histoName, sLegStyle, sDrawStyle)
            print "    Appending \"%s\"" % (histoName)
            p.histoMgr.appendHisto(h)

        if bNormalizeToOne == True:
            p.histoMgr.forEachHisto(lambda h: dataset._normalizeToOne(h.getRootHisto()))
            yMinLog = yMinLogNorm

        # Customize the plots
        drawPlot = Helper.customizePlot(logY, bAddLumiText, bRatio, bInvertRatio, "Ratio", yMin, yMax, yMaxFactor, yMinRatio, yMaxRatio, yMinLog, yMaxFactorLog)            

        # Increment counter
        counter = counter + 1

    # Save the plots
    if legendHeader is not None:
        drawPlot(p, saveName, xlabel=xLabel, ylabel=yLabel, customizeBeforeDraw=lambda plot: plot.legend.SetHeader(legendHeader))
    else:
        drawPlot(p, saveName, xlabel=xLabel, ylabel=yLabel, customizeBeforeDraw=Helper.setLabelOption)
    print "*** Saved canvas as \"%s\"\n" % (saveName)

    return 

######################################################################
if __name__ == "__main__":

    main()

    if not bBatchMode:
        raw_input("*** DONE! Press \"ENTER\" key exit session: ")

######################################################################
