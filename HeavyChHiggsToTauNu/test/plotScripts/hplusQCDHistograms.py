#!/usr/bin/env python

######################################################################
# All imported modules
######################################################################
# System modules
import sys
import math
import array
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
bBatchMode           = True
myDataEra            = "Run2011A"
myTailKillerScenario = "TailKillerLoose"
myRootFilesDir       = "/Users/attikis/my_work/cms/lxplus/QCDfactorisedResults_datacards_130506_202100/"
myRootFilesSubDir    = "datacards_130507_114747_myDummyTestName_TransverseMass_"+myDataEra+"_Light_OptQCD"+myTailKillerScenario+"_QCDfact_MCEWK/"
myRootFilePath       = "info/QCDMeasurementFactorisedInfo.root"
myPath               = myRootFilesDir + myRootFilesSubDir + myRootFilePath

ROOT.gROOT.SetBatch(bBatchMode)

######################################################################
# Function declarations
######################################################################
def main():
    
    # Get all histos to be plotted from QCDHistoHelper module
    HistoList = QCDHistoHelper.GetHistoList()
    
    # Plot all histos appended to the HistoList in QCDHistoHelper using a user-defined QCD factorisation scheme
    doHistos(HistoList, myPath, QCDscheme = "Full_factorisation")
    doHistos(HistoList, myPath, QCDscheme = "Contraction_TauPt")
    doHistos(HistoList, myPath, QCDscheme = "Contraction_TauEta")
    doHistos(HistoList, myPath, QCDscheme = "Contraction_Nvtx")

    return

######################################################################
def getLumi(myDataEra):

    myDataEras   = ["Run2011A", "Run2011B", "Run2011AB"]

    # Check if user-defined data-era is allowed
    if myDataEra == "Run2011A":
        myLumi            = 2311.191 #(pb)
    elif myDataEra == "Run2011B":
        myLumi            = 2739 #(pb)
    elif myDataEra == "Run2011AB":
        myLumi            = 5050.191 #(pb)
    else:
        print "*** ERROR: Invalid data-era selected. Please select one of the following:\n    %s" %(myDataEras)
        sys.exit()
    return myLumi

######################################################################
def doHistos(HistoList, myPath, QCDscheme):
                
    # Firsly, check that custom-defined data-era is valid and get corresponding integrated luminosity (only used for addind lumi text)
    myLumi = getLumi(myDataEra)

    # Define a list of all available factorisation options. 
    myFactorisationSchemes  = ["Full_factorisation", "Contraction_TauPt", "Contraction_TauEta", "Contraction_Nvtx"]
    if QCDscheme not in myFactorisationSchemes:
        print "*** ERROR: Invalid QCD factorisation scheme selected. Please select one of the following:\n    %s" %(myFactorisationSchemes)
        sys.exit()

    # Plot all histograms defined in the HistoList
    print "\n*** Opening ROOT file:\n    \"%s\"" % (myPath)
    f = ROOT.TFile.Open(myPath)

    print "*** There are \"%s\" histograms in the plotting queue (QCDscheme = \"%s\"):" % (len(HistoList), QCDscheme)
    for h in HistoList:
        hName    = QCDscheme + "/" + h.name
        histo    = f.Get(hName)
        saveName = "QCD_" + myDataEra + "_" +QCDscheme+"_%s" % (h.name)
        xLabel   = h.xLabel
        yLabel   = h.yLabel
        xMin     = h.xMin
        xMax     = h.xMax
        bLogX    = h.bLogX
        yMin     = h.yMin
        yMax     = h.yMax
        bLogY    = h.bLogY
        legendLabel = h.legendLabel
        
        print "    Processing histogram with name \"%s\"" % (hName)
        # Create the plots
        p = createPlot(histo, myLumi, legendLabel)
        
        # Draw the plots
        drawPlot = plots.PlotDrawer(log=bLogY, addLuminosityText=True, opts={"ymin": yMin, "ymax": yMax}, optsLog={"ymin": yMin, "ymax": yMax})
        drawPlot(p, saveName, xlabel=xLabel, ylabel=yLabel, customizeBeforeDraw=setLabelOption)

    return
######################################################################
def setLabelOption(p):
   
    # See: http://root.cern.ch/root/htmldoc/TAxis.html#TAxis:LabelsOption
    p.getFrame().GetXaxis().LabelsOption("v") #"h", "v" "d" "u"
    
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
