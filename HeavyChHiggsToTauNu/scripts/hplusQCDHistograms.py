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
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.QCDHistoHelper

######################################################################
# User options
######################################################################
bBatchMode      = True
bCustomRange    = False
myRootFilePath  = "info/QCDMeasurementFactorisedInfo.root" 

######################################################################
# Global definitions
######################################################################
myQCDschemes    = ["TauPt", "TauEta", "Nvtx", "Full"]
myErrorTypes    = ["StatAndSyst", "StatOnly"]
myValidDataEras = ["Run2011A", "Run2011B", "Run2011AB"]

ROOT.gROOT.SetBatch(bBatchMode)

#To do:
#1 Normalize to unity option
#2 plot comparison from different paths
#3 mT Closure test
#4 MET clouser test

######################################################################
# Function declarations
######################################################################
def main():
    
    # Get all histos to be plotted from QCDHistoHelper module
    #HistoList = QCDHistoHelper.GetEntireHistoList()
    
    # Create a specific histogram list to be plotted
    HistoList = QCDHistoHelper.GetMtShapeBinHistoNames()
    
    # Plot all histos appended to the HistoList, using a user-defined QCD factorisation scheme and ErrorType
    #doHistos(HistoList, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", saveNameExtension = "")

    # Plot superimposed plots
    doHistosCompare(HistoList, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", saveNameExtension = "")

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
def doHistos(HistoList, myPath, QCDscheme, ErrorType, saveNameExtension):
                
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

        saveName = myDataEra + "_" + histoName + saveNameExtension
        saveName = saveName.replace("/", "__")
        xLabel   = h.xLabel
        yLabel   = h.yLabel
        xMin     = h.xMin
        xMax     = h.xMax
        bLogX    = h.bLogX
        yMin     = h.yMin
        yMax     = h.yMax
        bLogY    = h.bLogY
        legendLabel = h.legendLabel
        
        # Create and draw the plots
        p = createPlot(histo, myLumi, legendLabel)
        if bCustomRange == True:
            drawPlot = plots.PlotDrawer(log=bLogY, addLuminosityText=True, opts={"ymin": yMin, "ymax": yMax}, optsLog={"ymin": yMin, "ymax": yMax})
        else:
            drawPlot = plots.PlotDrawer(addLuminosityText=True)

        # Save the plots
        saveName = saveName.replace("Leg1", "MetLeg").replace("Leg2", "TauLeg").replace("leg1", "MetLeg").replace("leg2", "TauLeg")
        drawPlot(p, saveName, xlabel=xLabel, ylabel=yLabel, customizeBeforeDraw=setLabelOption)
        print "    \"%s\"" % (saveName)

    return

######################################################################
def doHistosCompare(HistoList, myPath, QCDscheme, ErrorType, saveNameExtension):
                
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
    counter = 1
    for h in HistoList:
        folderName = "Contraction_" + QCDscheme
        histoName  = h.name.replace("*QcdScheme*", QCDscheme).replace("*ErrorType*", ErrorType)
        # Temporary quick-fix to naming difference
        if "Shape_" in histoName:
            histoName = histoName.replace("StatAndSyst", "fullUncert").replace("StatOnly", "statUncert") 
        pathName   = folderName + "/" + histoName
        histo      = getHisto(rootFile, pathName)

        saveName = myDataEra + "_" + histoName + saveNameExtension
        saveName = saveName.replace("/", "__")
        xLabel   = h.xLabel
        yLabel   = h.yLabel
        xMin     = h.xMin
        xMax     = h.xMax
        bLogX    = h.bLogX
        yMin     = h.yMin
        yMax     = h.yMax
        bLogY    = h.bLogY
        legendLabel = h.legendLabel
        
        # Create and draw the plots
        if counter == 1:
            p = createPlot(histo, myLumi, legendLabel)
        else:
            h = histograms.Histo(setHistoStyle(histo, counter, counter), legendLabel, "P", "P")
            histograms.Histo(h, histoName, "P", "P")
            p.histoMgr.appendHisto(h)

        if bCustomRange == True:
            drawPlot = plots.PlotDrawer(log=bLogY, addLuminosityText=True, opts={"ymin": yMin, "ymax": yMax}, optsLog={"ymin": yMin, "ymax": yMax})
        else:
            drawPlot = plots.PlotDrawer(addLuminosityText=True)

        # Increment counter
        counter = counter + 1

    # Save the plots
    saveName = saveName.replace("Leg1", "MetLeg").replace("Leg2", "TauLeg").replace("leg1", "MetLeg").replace("leg2", "TauLeg")
    drawPlot(p, saveName, xlabel=xLabel, ylabel=yLabel, customizeBeforeDraw=setLabelOption)
    print "    \"%s\"" % (saveName)

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
def setHistoStyle(histo, colourCode, styleCode):
    
    myColours = [ROOT.kRed+1, ROOT.kOrange+1, ROOT.kGreen+3, ROOT.kAzure+1, ROOT.kViolet+1, ROOT.kMagenta+1, 
                 ROOT.kRed-7, ROOT.kOrange-7, ROOT.kGreen-5, ROOT.kAzure-7,  ROOT.kViolet-7, ROOT.kMagenta-7]

    myStyles = [ROOT.kDot, ROOT.kPlus, ROOT.kStar, ROOT.kCircle, ROOT.kFullCircle, ROOT.kFullSquare, ROOT.kFullTriangleUp, ROOT.kFullTriangleDown, 
                ROOT.kOpenCircle, ROOT.kOpenSquare, ROOT.kOpenTriangleUp, ROOT.kOpenCross]

    histo.SetMarkerColor(myColours[colourCode])
    histo.SetLineColor(myColours[colourCode])
    histo.SetMarkerColor(myColours[colourCode])
    histo.SetMarkerStyle(myStyles[styleCode])
    histo.SetMarkerSize(1.2)

    return histo

######################################################################
def createPlot(histo, myLumi, legendLabel, **kwargs):

    # Set the TDR style
    style = tdrstyle.TDRStyle()

    if isinstance(histo, ROOT.TH1):
        defaults = {"legendStyle": "EP", "drawStyle": "EP"}
        defaults.update(kwargs)
        histo.GetZaxis().SetTitle("")
        p = plots.PlotBase([histograms.Histo(histo, legendLabel, **defaults)])
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
