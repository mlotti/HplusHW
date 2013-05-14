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
bNormalizeToOne = True
bCustomRange    = False
sDataEra        = "Run2011AB"
sLegStyle       = "EP" 
sDrawStyle      = "EP" #"AP" "EP" "HIST9"
myRootFilePath  = "info/QCDMeasurementFactorisedInfo.root" 

######################################################################
# Global definitions
######################################################################
myQCDschemes    = ["TauPt", "TauEta", "Nvtx", "Full"]
myErrorTypes    = ["StatAndSyst", "StatOnly"]
myValidDataEras = ["Run2011A", "Run2011B", "Run2011AB"]
#myTailKillers   = ["ZeroPlus", "LoosePlus", "MediumPlus", "TightPlus"]
myTailKillers   = ["LoosePlus", "MediumPlus", "TightPlus"]

ROOT.gROOT.SetBatch(bBatchMode)

######################################################################
# Function declarations
######################################################################
def main():
    
    # Get all histos to be plotted from QCDHistoHelper module
    MtShapesList = HistoHelper.GetMtShapeHistoNames()
    NqcdList     = HistoHelper.GetNQcdHistoNames()

    # Superimpos plots in the HistoList on one canvas
    doHistosCompare(MtShapesList, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", saveNameExtension = "")
    doHistosCompare(NqcdList, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", saveNameExtension = "")

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
        print "*** Opening ROOT file:\n    \"%s\"" % (myPath)
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
def doHistosCompare(HistoList, myPath, QCDscheme, ErrorType, saveNameExtension):
                
    # Check the current working directory name for a valid data-era
    myDataEra = sDataEra

    # Get the integrated luminosity of the data-era (only used for addind lumi text)
    myLumi = getLumi(myDataEra)

    # Check that the user-defined options are valid
    checkUserOptions(QCDscheme, ErrorType)

    # Get the directories under current working directory. These are my tailKillerPaths
    myDirsDict = {}
    for dirName in os.walk('.').next()[1]: 
        if ("_" + sDataEra  + "_") not in dirName:
            continue
        else:
            for tailKiller in myTailKillers:
                if tailKiller not in dirName:
                    continue
                else:
                    myDirsDict[tailKiller] = dirName

    counter = 1
    for tailKiller in myDirsDict.keys():
        dirName = myDirsDict[tailKiller]
        
        print "\n*** Processing Tail-Killer scenario \"%s\"" % (tailKiller)
        rootFile = getRootFile(dirName + "/" + myPath)

        # Plot all histograms defined in the HistoList    
        print "*** There are \"%s\" histogram(s) in the plotting queue (QCDscheme = \"%s\"):" % (len(HistoList), QCDscheme)
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
            logX     = h.bLogX
            yMin     = h.yMin
            yMax     = h.yMax
            logY     = h.bLogY
            legendLabel = tailKiller # = h.legendLabel

            # Create and draw the plots
            if counter == 1:
                p = createPlot(histo, myLumi, legendLabel)
            else:
                h = histograms.Histo(setHistoStyle(histo, counter), legendLabel, sDrawStyle, sDrawStyle)
                histograms.Histo(h, histoName, sDrawStyle, sDrawStyle)
                p.histoMgr.appendHisto(h)
                                    
            # Increment counter
            counter = counter + 1

    if bNormalizeToOne == True:
        p.histoMgr.forEachHisto(lambda h: dataset._normalizeToOne(h.getRootHisto()))
        drawPlot = plots.PlotDrawer(log=bLogY, addLuminosityText=True, opts={"ymaxfactor": 1.5}, optsLog={"ymax": 1.0})
    else:
        if bCustomRange == True:
            drawPlot = plots.PlotDrawer(log=logY, addLuminosityText=True, opts={"ymin": yMin, "ymax": yMax}, optsLog={"ymin": yMin, "ymax": yMax})
        else:
            drawPlot = plots.PlotDrawer(log=bLogY, addLuminosityText=True, opts={"ymaxfactor": 1.5}, optsLog={"ymaxfactor": 10})
                
    # Save the plots
    saveName = saveName.replace("Leg1", "MetLeg").replace("Leg2", "TauLeg").replace("leg1", "MetLeg").replace("leg2", "TauLeg")
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

    if counter > 12:
        counter = 0
    
    myColours = [ROOT.kRed+1, ROOT.kOrange+1, ROOT.kGreen+3, ROOT.kAzure+1, ROOT.kViolet+1, ROOT.kMagenta+1, 
                 ROOT.kRed-7, ROOT.kOrange-7, ROOT.kGreen-5, ROOT.kAzure-7,  ROOT.kViolet-7, ROOT.kMagenta-7]

    myMarkerStyles = [ROOT.kStar, ROOT.kFullCircle, ROOT.kFullSquare, ROOT.kFullTriangleUp, ROOT.kFullTriangleDown, 
                ROOT.kOpenCircle, ROOT.kOpenSquare, ROOT.kOpenTriangleUp, ROOT.kCircle, ROOT.kOpenCross, ROOT.kDot, ROOT.kPlus]

    myLineStyles = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] #[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2]

    histo.SetMarkerColor(myColours[counter])
    histo.SetMarkerColor(myColours[counter])
    histo.SetMarkerStyle(myMarkerStyles[counter])
    histo.SetMarkerSize(1.2)

    histo.SetLineColor(myColours[counter])
    histo.SetFillStyle(3001)
    histo.SetFillColor(myColours[counter])
    histo.SetLineStyle(myLineStyles[counter]);
    histo.SetLineWidth(2);
    
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
