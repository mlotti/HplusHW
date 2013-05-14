#!/usr/bin/env python

######################################################################
# All imported modules
######################################################################
# System modules
import sys
import math
import array
import re
import os
# ROOT modules
import ROOT
from ROOT import gStyle
# HPlus modules
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.cutstring import * # And, Not, Or
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect
# Script-specific modules
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.QCDHistoHelper as HistoHelper

######################################################################
# User options
######################################################################
bBatchMode      = True
bLogY           = False
sLegStyle       = "P" 
sDrawStyle      = "EP" # "AP" "EP" "HIST9"
myRootFilePath  = "info/QCDMeasurementFactorisedInfo.root" 

######################################################################
# Global definitions
######################################################################
myQCDschemes    = ["TauPt", "TauEta", "Nvtx", "Full"]
myErrorTypes    = ["StatAndSyst", "StatOnly"]
myValidDataEras = ["Run2011A", "Run2011B", "Run2011AB"]
myTailKillers   = ["ZeroPlus", "LoosePlus", "MediumPlus", "TightPlus"]

ROOT.gROOT.SetBatch(bBatchMode)

######################################################################
# Function declarations
######################################################################
def main():
    
    # Mt shapes
    MtShapesLeg1List    = HistoHelper.GetMtShapeHistoNames(sMyLeg="Leg1")
    MtShapesLeg2List    = HistoHelper.GetMtShapeHistoNames(sMyLeg="Leg2")
    #doHistos(MtShapesLeg1List, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "MtShape_Leg1", bNormalizeToOne = False)
    #doHistos(MtShapesLeg2List, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "MtShape_Leg2", bNormalizeToOne = False)    
    #doHistosCompare(MtShapesLeg1List + MtShapesLeg2List, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "MtShapes_Leg1_And_Leg2", bNormalizeToOne = True)

    # Closure tests
    binList = [1, 2, 3, 4, 5, 6, 7, 8, 9] 
    for index in binList:
        MtBinShapesStdSelList = HistoHelper.GetMtBinShapeHistoNames(lBinList = [index], sMyLeg="StandardSelections")
        MtBinShapesLeg1List   = HistoHelper.GetMtBinShapeHistoNames(lBinList = [index], sMyLeg="Leg1")
        MtBinShapesLeg2List   = HistoHelper.GetMtBinShapeHistoNames(lBinList = [index], sMyLeg="Leg2")
        doHistosCompare(MtBinShapesStdSelList + MtBinShapesLeg2List  + MtBinShapesLeg1List, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "ClosureTest_Mt_Bin" + str(index), bNormalizeToOne = True)

    return

######################################################################
def getDataEra():

    cwd = os.getcwd()
    myDataEra = None
    
    # Check all valid data-eras
    for era in myValidDataEras:
        if "_" + era + "_" in cwd:
            myDataEra = era
        else:
            continue

    if myDataEra == None:
        print "*** ERROR: Invalid data-era selected. Please select one of the following:\n    %s" %(myValidDataEras)
        sys.exit()
    else:
        return myDataEra

######################################################################
def getLumi(myDataEra):

    # Check if user-defined data-era is allowed
    if myDataEra == "Run2011A":
        myLumi            = 2311.191 #(pb)
    elif myDataEra == "Run2011B":
        myLumi            = 2739 #(pb)
    elif myDataEra == "Run2011AB":
        myLumi            = 5050.191 #(pb)
    else:
        print "*** ERROR: Invalid data-era selected. Please select one of the following:\n    %s" %(myValidDataEras)
        sys.exit()

    return myLumi

######################################################################
def checkUserOptions(QCDscheme, ErrorType):
    
    if QCDscheme not in myQCDschemes:
        print "*** ERROR: Invalid QCD factorisation scheme selected. Please select one of the following:\n    %s" %(myQCDschemes)
        sys.exit()
        
    if ErrorType not in myErrorTypes:
        print "*** ERROR: Invalid Error-Type selected. Please select one of the following:\n    %s" %(myFactorisationSchemes)
        sys.exit()
    
    return

######################################################################
def getRootFile(myPath):

    if os.path.exists(myPath):
        print "\n*** Opening ROOT file:\n    \"%s\"" % (myPath)
        f = ROOT.TFile.Open(myPath)
        return f
    else:
        print "*** ERROR: The path \"%s\" defined for the ROOT file is invalid. Please check the path name." % (myPath)
        sys.exit()

######################################################################
def getHisto(rootFile, pathName):
    
    histo = rootFile.Get(pathName)
    if not isinstance(histo, ROOT.TH1):
        print "*** ERROR: Histogram \"%s\" is not a ROOT.TH1 instance. Check that its path is correct." %(pathName)
        sys.exit()
    else:
        return histo

######################################################################
def doHistos(HistoList, myPath, QCDscheme, ErrorType, mySaveName, bNormalizeToOne):
                
    # Check the current working directory name for a valid data-era
    myDataEra = getDataEra()

    # Get the integrated luminosity of the data-era (only used for addind lumi text)
    myLumi = getLumi(myDataEra)

    # Check that the user-defined options are valid
    checkUserOptions(QCDscheme, ErrorType)

    # Get the ROOT file
    rootFile = getRootFile(myPath)

    # Plot all histograms defined in the HistoList    
    print "*** There are \"%s\" histograms in the plotting queue (QCDscheme = \"%s\"):" % (len(HistoList), QCDscheme)
    for h in HistoList:
        folderName = "Contraction_" + QCDscheme
        histoName  = h.name.replace("*QcdScheme*", QCDscheme).replace("*ErrorType*", ErrorType)
        # Temporary quick-fix to naming difference
        if "Shape_" in histoName:
            histoName = histoName.replace("StatAndSyst", "fullUncert").replace("StatOnly", "statUncert") 
        pathName   = folderName + "/" + histoName
        histo      = getHisto(rootFile, pathName)

        if mySaveName == None:
            saveName = myDataEra + "_" + histoName
        else:
            saveName = myDataEra + "_" + mySaveName

        saveName = saveName.replace("/", "__")
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
        p = createPlot(histo, myLumi, legendLabel)

        if bNormalizeToOne == True:
            p.histoMgr.forEachHisto(lambda h: dataset._normalizeToOne(h.getRootHisto()))
            drawPlot = plots.PlotDrawer(log=logY, addLuminosityText=True, opts={"ymaxfactor": 1.5}, optsLog={"ymax": 1.0})
        else:
            drawPlot = plots.PlotDrawer(log=logY, addLuminosityText=True, opts={"ymin": yMin, "ymax": yMax}, optsLog={"ymin": yMin, "ymax": yMax})
            
        # Save the plots
        saveName = saveName.replace("Leg1", "MetLeg").replace("Leg2", "TauLeg").replace("leg1", "MetLeg").replace("leg2", "TauLeg")
        drawPlot(p, saveName, xlabel=xLabel, ylabel=yLabel, customizeBeforeDraw=setLabelOption)
        print "*** Saved \"%s\"" % (saveName)

    return

######################################################################
def doHistosCompare(HistoList, myPath, QCDscheme, ErrorType, mySaveName, bNormalizeToOne):
                
    # Check the current working directory name for a valid data-era
    myDataEra = getDataEra()

    # Get the integrated luminosity of the data-era (only used for addind lumi text)
    myLumi = getLumi(myDataEra)

    # Check that the user-defined options are valid
    checkUserOptions(QCDscheme, ErrorType)

    # Get the ROOT file
    rootFile = getRootFile(myPath)

    # Plot all histograms defined in the HistoList    
    print "*** There are \"%s\" histograms in the plotting queue (QCDscheme = \"%s\"):" % (len(HistoList), QCDscheme)
    counter = 0
    for h in HistoList:
        folderName = "Contraction_" + QCDscheme
        histoName  = h.name.replace("*QcdScheme*", QCDscheme).replace("*ErrorType*", ErrorType)
        # Temporary quick-fix to naming difference
        if "Shape_" in histoName:
            histoName = histoName.replace("StatAndSyst", "fullUncert").replace("StatOnly", "statUncert") 
        pathName   = folderName + "/" + histoName
        histo      = getHisto(rootFile, pathName)

        if mySaveName == None:
            saveName = myDataEra + "_" + histoName
            saveName = saveName.replace("/", "__")
        else:
            saveName = myDataEra + "_" + mySaveName
        saveName = saveName.replace("Leg1", "MetLeg").replace("Leg2", "TauLeg").replace("leg1", "MetLeg").replace("leg2", "TauLeg")
        xLabel   = h.xLabel
        yLabel   = h.yLabel
        xMin     = h.xMin
        xMax     = h.xMax
        logX    = h.bLogX
        yMin     = h.yMin
        yMax     = h.yMax
        logY    = h.bLogY
        legendLabel = h.legendLabel
        
        # Create and draw the plots
        if counter == 0:
            p = createPlot(histo, myLumi, legendLabel)
            h = histograms.Histo(setHistoStyle(histo, counter), legendLabel, sLegStyle, sDrawStyle)
        else:
            h = histograms.Histo(setHistoStyle(histo, counter), legendLabel, sLegStyle, sDrawStyle)
            #h = histograms.Histo(setHistoStyle(histo, counter), legendLabel, "f", "HIST")
            histograms.Histo(h, histoName, sLegStyle, sDrawStyle)
            p.histoMgr.appendHisto(h)

        if bNormalizeToOne == True:
            p.histoMgr.forEachHisto(lambda h: dataset._normalizeToOne(h.getRootHisto()))
            drawPlot = plots.PlotDrawer(log=logY, addLuminosityText=True, opts={"ymaxfactor": 1.5}, optsLog={"ymax": 1.0})
        else:
            drawPlot = plots.PlotDrawer(log=logY, addLuminosityText=True, opts={"ymin": yMin, "ymax": yMax}, optsLog={"ymin": yMin, "ymax": yMax})

        # Increment counter
        counter = counter + 1

    # Save the plots
    drawPlot(p, saveName, xlabel=xLabel, ylabel=yLabel, customizeBeforeDraw=setLabelOption)
    print "*** Saved \"%s\"" % (saveName)

    return 

######################################################################
def setLabelOption(p):
   
    # See: http://root.cern.ch/root/htmldoc/TAxis.html#TAxis:LabelsOption
    if p.getFrame().GetXaxis().GetLabels() == None:
        return
    else:
        p.getFrame().GetXaxis().LabelsOption("u") #"h", "v" "d" "u"
        p.getFrame().GetXaxis().SetLabelSize(14.5) #"h", "v" "d" "u"
        
    return

######################################################################    
def setHistoStyle(histo, counter):
    
    # Since the list of supported styles/colours contains 12 entries, if counter goes out of scope it
    if counter > 11:
        counter = 0
        
    myColours = [ROOT.kRed+1, ROOT.kAzure+1, ROOT.kOrange+1, ROOT.kViolet+1, ROOT.kMagenta+1, ROOT.kGreen+3, 
                 ROOT.kRed-7, ROOT.kOrange-7, ROOT.kGreen-5, ROOT.kAzure-7,  ROOT.kViolet-7, ROOT.kMagenta-7]

    myMarkerStyles = [ROOT.kFullCircle, ROOT.kFullSquare, ROOT.kFullTriangleUp, ROOT.kFullTriangleDown, ROOT.kStar, ROOT.kPlus, ROOT.kCircle, 
                      ROOT.kOpenCircle, ROOT.kOpenSquare, ROOT.kOpenTriangleUp, ROOT.kOpenCross, ROOT.kDot]

    myLineStyles = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] #[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2]

    histo.SetMarkerColor(myColours[counter])
    histo.SetMarkerColor(myColours[counter])
    histo.SetMarkerStyle(myMarkerStyles[counter])
    histo.SetMarkerSize(1.2)

    histo.SetLineColor(myColours[counter])
    histo.SetLineStyle(myLineStyles[counter]);
    histo.SetLineWidth(2);

    histo.SetFillStyle(3001)
    histo.SetFillColor(myColours[counter])
    
    return histo

######################################################################
def createPlot(histo, myLumi, legendLabel, **kwargs):

    style = tdrstyle.TDRStyle()

    if isinstance(histo, ROOT.TH1):
        args = {"legendStyle": sLegStyle, "drawStyle": sDrawStyle}
        args.update(kwargs)
        histo.GetZaxis().SetTitle("")
        p = plots.PlotBase([histograms.Histo(histo, legendLabel, **args)])
        p.setLuminosity(myLumi)
        return p
    else:
        print "*** ERROR: Histogram \"%s\" is not a valid instance of a ROOT.TH1" % (histo)
        sys.exit()

######################################################################
if __name__ == "__main__":

    # Call the main function
    main()

    # Keep session alive (otherwise canvases close automatically)
    if not bBatchMode:
        raw_input("*** DONE! Press \"ENTER\" key exit session: ")

######################################################################
