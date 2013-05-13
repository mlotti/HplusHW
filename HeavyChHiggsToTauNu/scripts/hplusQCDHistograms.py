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
import QCDHistoHelper

######################################################################
# Define options and declarations
######################################################################
bBatchMode      = True
bCustomRange    = False
myRootFilePath  = "info/QCDMeasurementFactorisedInfo.root" 
myValidDataEras = ["Run2011A", "Run2011B", "Run2011AB"]
ROOT.gROOT.SetBatch(bBatchMode)

######################################################################
# Function declarations
######################################################################
def main():
    
    # Get all histos to be plotted from QCDHistoHelper module
    HistoList = QCDHistoHelper.GetHistoList()
    
    # Plot all histos appended to the HistoList in QCDHistoHelper using a user-defined QCD factorisation scheme
    doHistos(HistoList, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", saveNameExtension = "")
    # doHistos(HistoList, myRootFilePath, QCDscheme = "TauEta", ErrorType = "StatAndSyst", saveNameExtension = "")
    # doHistos(HistoList, myRootFilePath, QCDscheme = "Nvtx", ErrorType = "StatAndSyst", saveNameExtension = "") 
    # doHistos(HistoList, myRootFilePath, QCDscheme = "Full", ErrorType = "StatAndSyst", saveNameExtension = "")

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
def doHistos(HistoList, myPath, QCDscheme, ErrorType, saveNameExtension):
                
    # Firsly, check that custom-defined data-era is valid and get corresponding integrated luminosity (only used for addind lumi text)
    myDataEra = getDataEra()
    myLumi    = getLumi(myDataEra)

    # Define a list of all available factorisation options. 
    myFactorisationSchemes  = ["Full", "TauPt", "TauEta", "Nvtx"]
    if QCDscheme not in myFactorisationSchemes:
        print "*** ERROR: Invalid QCD factorisation scheme selected. Please select one of the following:\n    %s" %(myFactorisationSchemes)
        sys.exit()
        
    myErrorTypes = [ "StatAndSyst", "StatOnly"]
    if ErrorType not in myErrorTypes:
        print "*** ERROR: Invalid Error-Type selected. Please select one of the following:\n    %s" %(myFactorisationSchemes)
        sys.exit()


    # Plot all histograms defined in the HistoList
    print "\n*** Opening ROOT file:\n    \"%s\"" % (myPath)
    f = ROOT.TFile.Open(myPath)

    print "*** There are \"%s\" histograms in the plotting queue (QCDscheme = \"%s\"):" % (len(HistoList), QCDscheme)
    for h in HistoList:
        folderName = "Contraction_" + QCDscheme
        histoName  = h.name.replace("*QcdScheme*", QCDscheme).replace("*ErrorType*", ErrorType)
        # Temporary quick-fix to naming difference
        if "Shape_" in histoName:
            histoName = histoName.replace("StatAndSyst", "fullUncert").replace("StatOnly", "statUncert") 

        pathName   = folderName + "/" + histoName
        histo      = f.Get(pathName)
        if not isinstance(histo, ROOT.TH1):
            print "*** ERROR: Histogram \"%s\" is not a ROOT.TH1 instance. Check that its path is correct." %(pathName)
            sys.exit()

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
        
        #print "    Processing histogram with name \"%s\"" % (hName)
        # Create the plots
        p = createPlot(histo, myLumi, legendLabel)
        
        # Draw the plots
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
def setLabelOption(p):
   
    # See: http://root.cern.ch/root/htmldoc/TAxis.html#TAxis:LabelsOption
    if p.getFrame().GetXaxis().GetLabels() == None:
        return
    else:
        p.getFrame().GetXaxis().LabelsOption("u") #"h", "v" "d" "u"
        p.getFrame().GetXaxis().SetLabelSize(15.0) #"h", "v" "d" "u"
        
    return

######################################################################
def createPlot(histo, myLumi, legendLabel, **kwargs):

    # Set the TDR style
    style = tdrstyle.TDRStyle()

    if isinstance(histo, ROOT.TH1):
        defaults = {"legendStyle": "P", "drawStyle": "EP"}
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
