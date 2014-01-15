#!/usr/bin/env python

# Script docstrings
'''
Usage:
./fileName.py

Permissions: 
chmod +x fileName.py

Description:
This script is for plotting/analysing histograms of the Invariant 
Mass (or any other class if needed), as first implemented by Stefan 
Richter. It has dependency on the auxiliary file InvMassHistoHelper.py in 
which the declaration and beautification of histograms such as binning
axis labels/ranges and cutlines are defined. More documentation can be 
found inside the InvMassHistoHelper file itself.

First the User should edit the InvMassHistoHelper.py auxiliary file and append to the 
lists "TH1List" and "TH2List" the TH1 and TH2 histograms he want to be plotted.
All supported histograms have well-tested options so first attempt to use as they
are before changing something. For example, the line:
TH1List.append(HiggsMassPositiveDiscriminant)
means that the TH1List now included the histogram HiggsMassPositiveDiscriminant. 
Also, the line:
TH2List.append(TransMassVsInvMass)
means the the TH2List now included the histogram TransMassVsInvMass.

Then, in the section "Define options and declarations" below one must set their user-defined 
parameters such as path for multicrab directory, BR(H->tau), datasets to be used etc. 

Once these are set we move finally to the main function in which was is to be plotted is defined 
in the line:
    doPlots(datasets, TH1List, [], signifPlotsDir)
The method doPlots requires the datasets to be used, one list of TH1 histograms (TH1List) and one list
of TH2 histograms (TH2List). The last argument is a string list containing the cut directions to be 
considered for significance plots. For example, passing the string list
    signifPlotsDir = [">", "<"]
to the method means that both the > and < cut direction (as well as bin-significance) plots will be created.
If the string list that is passed is empty (i.e. []) then no significance plot is done.

(Default) Options:
-h, --help show help message and exit
-b : run in batch mode without graphics
-x : exit on exception
  -e expression: request execution of the given C++ expression  -n : do not execute logon and logoff macros as specified in .rootrc
-q : exit after processing command line macro files
-l : do not show splash screen
dir : if dir is a valid directory cd to it before executing

-?      : print usage
-h      : print usage
--help  : print usage
-config : print ./configure options
-memstat : run with memory usage monitoring

Author:
Alexandros Attikis

'''

######################################################################
# All imported modules
######################################################################
# System modules
import sys
import array
import math
import ROOT
from ROOT import gStyle
from ROOT import gPad
from ROOT import TGaxis

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
from InvMassHistoHelper import *

######################################################################
# Define options and declarations
######################################################################
# Global Definitions
BR_tH          = 0.01
BR_Htaunu      = 1.0
hplusMass      = 160
signalMass     = str(hplusMass)
signalMasses   = ["80", "90", "100", "120", "140", "150", "160"] #155
yMinRatio      = 0.0
yMaxRatio      = 2.0
yMaxFactor     = 2
yMaxFactorLog  = 100

# Define the path of the multicrab directory here
mcrabDir        = "/mnt/flustre/attikis/InvMass/Test" #/mnt/flustre/attikis/InvMass/FullHPlusMass_Run2012_131112_144044/

# Define data era to be used
# myDataEra      = "Run2011AB" #"Run2011A", "Run2011B"
myDataEra      = "Run2012ABCD" #"Run2012C", "Run2012D", "Run2012AB" "Run2012ABC", "Run2012ABCD" (NO standalone 2012A or 2012B)

# Datasets to consider
datasetsToKeep  = ["TTJets", "WJets", "DYJetsToLL", "SingleTop", "Diboson", "TTToHplus_M" + signalMass]
#datasetsToKeep  = ["Data", "WJets", "TTJets", "DYJetsToLL", "SingleTop", "Diboson", "TTToHplus_M" + signalMass]
#datasetsToKeep  = ["Data", "QCD", "WJets", "TTJets", "DYJetsToLL", "SingleTop", "Diboson", "TTToHplus_M" + signalMass]
#datasetsToKeep  = ["EWK MC"]

#[TTJets_FullLept_TuneZ2star_Summer12]
#[TTJets_SemiLept_TuneZ2star_Summer12]
#[TTJets_Hadronic_TuneZ2star_ext_Summer12]

# Define some boolears
bBatchMode        = True
bPrintPSet        = True
bAddMCUncertainty = True
bStackHistos      = True

######################################################################
# Other
######################################################################
multicrabPath  = mcrabDir
ROOT.gROOT.SetBatch(bBatchMode)

######################################################################
# Function declaration
######################################################################
def main():

    # Print some info here
    print "*** NOTE:"
    print "%sMulticrab dir used: \"%s\"" % (" "*0, multicrabPath)
    
    # Get the desired datasets 
    datasets = getDatasets(multicrabPath, myDataEra)
    
    # Define the signifiance plots directional cut
    #signifPlotsDir = [">", "<"]
    signifPlotsDir = []

    # Plot desired histograms
    # doPlots(datasets, TH1List, TH2List, signifPlotsDir)
    doPlots(datasets, TH1List, [], signifPlotsDir)
    # doPlots(datasets, [], TH2List, signifPlotsDir)
    
    # Alternative way:
    # myHistos = []
    #myHistos.append(HiggsMass) #HiggsMass histo is defined in the InvMassHistoHelper.py auxiliary file
    # doPlots(datasets, myHistos, [], signifPlotsDir)

    return

######################################################################
def doPlots(datasets, TH1List, TH2List, signifCutDirection):
    
    nTH1 = len(TH1List)
    nTH2 = len(TH2List)
    nDatasets     = len(datasets.getAllDatasetNames())
    nDataDatasets = len(datasets.getDataDatasets())
    nMCDatasets   = len(datasets.getMCDatasets())

    if nTH1 > 0:
        print "*** There are %s TH1 histogram(s) in the plotting queue:" % (nTH1)
        # for h in TH1List:
            #print "%s\"%s\"" % (" "*4, h.name)
        doTH1Plots(datasets, TH1List, signifCutDirection)

    if nTH2 > 0:
        print "*** There are %s TH2 histogram(s) in the plotting queue:" % (nTH2)
        if nDatasets > 1:
            print "%sWARNING! There are more than 1 datasets enabled. Skipping all TH2 histogram(s)" % (" "*0)
        else:
            for h in TH2List:
                print "%s\"%s\"" % (" "*4, h.name)
            doTH2Plots(datasets, TH2List)

    return

######################################################################
def getDatasets(multicrabPath, myDataEra):

    # Get the ROOT files for all datasets, merge datasets and reorder them
    datasets = dataset.getDatasetsFromMulticrabCfg(directory=multicrabPath, dataEra=myDataEra)
    #print "%sAvailable datasets:\n    %s" % (" "*0, datasets.getAllDatasetNames())
    
    # Print PSets used in ROOT-file generation
    if bPrintPSet:
        #print "*** Printing PSets for dataset \"%s\"" % ("TTToHplusBHminusB_M120_Fall11")
        #print datasets.getDataset("TTToHplusBHminusB_M120_Fall11").getParameterSet()
        psets = datasets.getSelections()
        f = open("PSets.txt", "w")
        f.write(psets)
        f.close()

    # Take care of PU weighting, luminosity, signal merging etc... of the datatasets
    print "\n*** Datasets:"
    manageDatasets(datasets)

    # Print the dataset information for sanity checks
    print "="*70
    datasets.printInfo()
    print "="*70

    # Do sanity checks before returning the datasets object
    nDatasets     = len(datasets.getAllDatasetNames())
    nDataDatasets = len(datasets.getDataDatasets())
    nMCDatasets   = len(datasets.getMCDatasets())
    if nDatasets > 0:
        return datasets
    else:
        print "%sERROR! There are zero (0) datasets. Check your settings. " % (" "*0)
        sys.exit()

######################################################################
def manageDatasets(datasets):
    
    # Since (by default) we use weighted counters, and the analysis job inputs are normally skims (as are "v44_4" and "v53_1"), need to update events to PU weighted
    print "%sUpdating events to PU weighted:" % (" "*0)
    datasets.updateNAllEventsToPUWeighted()

    # Determine number of Data/MC datasets present
    nDataDatasets   = len(datasets.getDataDatasets())
    nMCDatasets     = len(datasets.getMCDatasets())
    nDatasetsToKeep = len(datasetsToKeep)

    # Sanity check
    if nDatasetsToKeep < 1:
        print "%sERROR! There are zero (0) datasets." % (" "*0)
        sys.exit()

    # Determine luminosity and between canvas "Lumi" or "Simulation" text
    if nDataDatasets < 1:
        histograms.cmsTextMode = histograms.CMSMode.SIMULATION
    else:
        datasets.loadLuminosities()

    # Merge and rename datasets
    #print "%sDefault merging of dataset components:" % (" "*0)
    plots.mergeRenameReorderForDataMC(datasets)

    # Set signal xSectio and BR, and merge WH and HH
    print "%sSetting signal cross sections, using BR(t->bH+)=%s and BR(H+ -> tau+ nu)=%s" % (" "*0, BR_tH, BR_Htaunu)
    xsect.setHplusCrossSectionsToBR(datasets, BR_tH, BR_Htaunu)
    plots.mergeWHandHH(datasets) # Must be done after setting the cross section

    # Remove all datasets except those passed as a list
    datasets = getCustomDatasets(datasets, datasetsToKeep)

    # Finally, set TDR as the default style
    style = tdrstyle.TDRStyle()

    return datasets

######################################################################
def getWJetsDatasetList():
    return ["W1Jets_TuneZ2_Fall11", "W2Jets_TuneZ2_Fall11", "W3Jets_TuneZ2_v2_Fall11", "W4Jets_TuneZ2_Fall11"]

######################################################################
def getWJetsExclusiveDatasetList():
    return ["W1Jets_TuneZ2_Fall11", "W2Jets_TuneZ2_Fall11", "W3Jets_TuneZ2_v2_Fall11", "W4Jets_TuneZ2_Fall11"]

######################################################################
def getWJetsInclusiveDatasetList():
    return ["WJets_TuneZ2_Fall11"]

######################################################################
def getCustomDatasets(datasets, datasetsToKeep):
    
    # First determine whether to merge EWK MC or not
    if "EWK MC" in datasetsToKeep:
        mergeEwkMc(datasets)

    # Now, remove all datasets which are not defined in the user-defined dataset list
    #print "%sRemoving all datasets except: %s" % (" "*0, datasetsToKeep)
    for dataset in datasets.getAllDatasetNames():
        if dataset not in datasetsToKeep:
            #print "%sRemoving %s"  % (" "*0, dataset)
            datasets.remove(dataset)
        else:
            continue

    # Finally, customise the signal legend (if signal is present)
    if "TTToHplus_M" in datasets.getAllDatasetNames():
        plots._legendLabels["TTToHplus_M"+signalMass] = "m_{H^{#pm}} = " + signalMass + " GeV/c^{2}"

    return datasets

######################################################################
def mergeEwkMc(datasets):
    
    print "%sMerging EWK MC" %(" "*0)
    datasets.merge("EWK MC", ["WJets", "TTJets", "DYJetsToLL", "SingleTop", "Diboson"], keepSources=False)
    plots._plotStyles["EWK MC"] = styles.ttStyle

    return #datasets

######################################################################
def getCustomLumi(dataEra):
    
    myLumi = -1.0

    if dataEra == "Run2011A":
        myLumi = 2311.191 
    elif dataEra == "Run2011B":
        myLumi = 2739 
    elif dataEra == "Run2011AB":
        myLumi = 5050.191
    elif dataEra == "Run2012C":
        myLumi = 7027.603
    elif dataEra == "Run2012D":
        myLumi = 7369.0
    elif dataEra == "Run2012AB":
        myLumi = 5288.225
    elif dataEra == "Run2012ABC":
        myLumi = 12315.828
    elif dataEra == "Run2012ABCD":
        myLumi = 19684.828
    else:
        print "*** getCustomLumi(dataEra): Invalid data-era (%s). " (dataEra)
        sys.exit()

    return myLumi

######################################################################
def createTH1Plot(datasets, name, **kwargs):
    
    # Copy arguments to a new dictionary
    args = {}
    args.update(kwargs)
    
    # Proceed differently for Stacking and No-Stacking of plots
    if len(datasets.getDataDatasets())==0:
        args["normalizeToLumi"] = getCustomLumi(myDataEra)

    p = plots.DataMCPlot(datasets, name, **args)
    p.setDefaultStyles()

    if not bStackHistos:
        p.histoMgr.setHistoDrawStyleAll("P")
        p.histoMgr.setHistoLegendStyleAll("P")
    
    return p

######################################################################
def createTH2Plot(datasets, name, **kwargs):

    # Copy arguments to a new dictionary
    args = {}
    args.update(kwargs)

    # Proceed differently for MC-only plots and Data-MC plots
    if len(datasets.getDataDatasets())==0:
        args["normalizeToLumi"] = getCustomLumi(myDataEra)

    p = plots.DataMCPlot(datasets, name, **args)
    p.setDefaultStyles()
    p.histoMgr.setHistoDrawStyleAll("")
    p.histoMgr.setHistoLegendStyleAll("")
    setHistoContours(p, 100)
    p.histoMgr.setHistoDrawStyleAll("COLZ")
    gStyle.SetPalette(1)

    return p

######################################################################
def setHistoContours(p, nContours):

    for h in p.histoMgr.getHistos():
        htmp = h.getRootHisto()
        htmp.SetContour(nContours)
        minEvts = 0.01 #1/100 of an event (MC)
        maxEvts = htmp.GetBinContent(htmp.GetMaximumBin())
        htmp.GetZaxis().SetRangeUser(minEvts, maxEvts)

    return

######################################################################
def getFullSaveName(datasets, histoName, dataEra, bNormalized, bStackedHistos):
    
    saveName = dataEra + "_" + histoName
    saveName = saveName.replace("/", "_")
    
    if "TTToHplus_M"+signalMass in datasets.getAllDatasetNames():
        saveName = saveName + "_M" + signalMass
    
    if bNormalized == True:
        saveName = saveName + "_normalizedToOne"

    if bStackedHistos:
        saveName = saveName + "_Stacked"

    if "TH2" in histoName:
        # Sanity check
        if len(datasets.getAllDatasetNames()) > 1:
            print "ERROR! More than 1 dataset found for a TH2. Unsupported. Exiting ROOT"
            sys.exit()
        else:
            for dataset in datasets.getAllDatasetNames():
                # print "+++ dataset.replace(\" \",\"_\") = ", dataset.replace(" ", "_")
                saveName = saveName + "_" + dataset.replace(" ", "_")

    return saveName

######################################################################
def getCustomisedHisto(datasets, h, bIsTH2):

    if bIsTH2:
        print "*** Disabling bMCUncertainty and bStackHistos for TH2 plots"
        bAddMCUncertainty = False
        bStackHistos      = False
    else:
        bAddMCUncertainty = True
        bStackHistos      = True
        
    # Determine number of Data/MC datasets present
    nDataDatasets = len(datasets.getDataDatasets())
    nMCDatasets   = len(datasets.getMCDatasets())

    # Sanity check for Ratio plot. If no MC datasets are found disable it (overwrite user-defined options)
    if nMCDatasets < 1:
        h.bRatio == False
        #print "%snMCDatasets = %i" % (" "*0, nMCDatasets)
    if h.yMin is not None and h.yMax is not None:
        drawPlot = plots.PlotDrawer(stackMCHistograms=bStackHistos, addMCUncertainty=bAddMCUncertainty, log=h.bLogY, ratio=h.bRatio, addLuminosityText=True, ratioYlabel="Ratio", opts={"ymin": h.yMin, "ymax": h.yMax}, opts2={"ymin": yMinRatio, "ymax": yMaxRatio}, optsLog={"ymin": h.yMin, "ymax": h.yMax})
    else:
        drawPlot = plots.PlotDrawer(stackMCHistograms=bStackHistos, addMCUncertainty=bAddMCUncertainty, log=h.bLogY, ratio=h.bRatio, addLuminosityText=True, ratioYlabel="Ratio", opts={"ymaxfactor": yMaxFactor}, opts2={"ymin": yMinRatio, "ymax": yMaxRatio}, optsLog={"ymin": 1E-01, "ymaxfactor": yMaxFactorLog})        
            
    return drawPlot

######################################################################
def doTH1Plots(datasets, TH1List, signifCutDirection=None):

    # Loop over all hName and expressions in the histogram list. Create & Draw plot
    counter=0        
    for h in TH1List:
        print "*** Processing histo", h.name
        hName           = h.name
        units           = h.units
        xLabel          = h.xlabel
        bLogX           = h.bLogX
        binWidthX       = h.binWidthX
        yLabel          = h.ylabel
        bLogY           = h.bLogY
        bRatio          = h.bRatio
        bNormalizeToOne = h.bNormalizeToOne
        xLegMin         = h.xLegMin
        xLegMax         = h.xLegMax
        yLegMin         = h.yLegMin
        yLegMax         = h.yLegMax
        
        # Create customised legend
        histograms.createLegend.setDefaults(x1=xLegMin, x2= xLegMax, y1 = yLegMin, y2=yLegMax)

        # Create the plot
        p = createTH1Plot(datasets, hName, normalizeToOne = bNormalizeToOne)

        xAxis = TGaxis()
        if "Discriminant" in h.name:
            xAxis.SetMaxDigits(3)
        else:
            xAxis.SetMaxDigits(6)

        # Customise the plot
        drawPlot = getCustomisedHisto(datasets, h, False)
        
        # Determine name of file that histos will be saved to according to the user-options
        saveName = getFullSaveName(datasets, histoName="TH1_%s" % (hName), dataEra= myDataEra, bNormalized=bNormalizeToOne, bStackedHistos=bStackHistos)

        # Draw the plot                        
        drawPlot(p, saveName, xlabel=xLabel, ylabel=yLabel, rebinToWidthX=binWidthX, cutLine=getHistoCutLines(h))
        
        if len(signifCutDirection) !=0:
            doBinSignifPlots(p, drawPlot, datasets, h, hName, xLabel, yLabel, saveName)
            for cutDir in signifCutDirection:
                if (cutDir == ">" or cutDir == "<"):
                    doSignifPlots(p, drawPlot, datasets, h, hName, xLabel, yLabel, saveName, cutDir)
    return

######################################################################
def doTH2Plots(datasets, TH2List):
    '''
    def doTH2Plots(datasets, TH2List):
    '''
    # Loop over all hName and expressions in the histogram list. Create & Draw plot
    counter=0        
    for h in TH2List:
        hName      = h.name
        xUnits     = h.xUnits
        yUnits     = h.yUnits
        xLabel     = h.xlabel
        #xMin       = h.xMin
        #xMax       = h.xMax
        bRatio     = h.bRatio
        bLogX      = h.bLogX
        binWidthX  = h.binWidthX
        yLabel     = h.ylabel
        bLogY      = h.bLogY
        binWidthY  = h.binWidthY
        bNormalizeToOne = h.bNormalizeToOne
        xLegMin         = h.xLegMin
        xLegMax         = h.xLegMax
        yLegMin         = h.yLegMin
        yLegMax         = h.yLegMax

        # Determine number of Data/MC datasets present
        nDataDatasets = len(datasets.getDataDatasets())
        nMCDatasets   = len(datasets.getMCDatasets())
        #print "nMCDatasets = ", nMCDatasets

        # Create customised legend
        histograms.createLegend.setDefaults(x1=xLegMin, x2= xLegMax, y1 = yLegMin, y2=yLegMax)

        # Create the plot
        p = createTH2Plot(datasets, hName, normalizeToOne = bNormalizeToOne)

        # Customise the plot
        drawPlot = getCustomisedHisto(datasets, h, True)
        
        # Determine name of file that histos will be saved to according to the user-options
        saveName = getFullSaveName(datasets, histoName="TH2_%s" % (hName), dataEra= myDataEra, bNormalized=bNormalizeToOne, bStackedHistos=bStackHistos)

        # Draw the plot
        drawPlot(p, saveName, xlabel=xLabel, ylabel=yLabel, rebinToWidthX=binWidthX)#, rebinToWidthY=binWidthY)

    return

######################################################################    
def setSignificanceHistoStyle(histo):
    '''
    def setSignificanceHistoStyle(histo):
    '''
    colour = ROOT.kGreen-5
    histo.SetMarkerColor(colour)
    histo.SetLineWidth(2)
    histo.SetLineColor(colour)
    histo.SetMarkerColor(colour)
    histo.SetMarkerStyle(ROOT.kFullCross)
    histo.SetMarkerSize(1.2)
    histo.SetFillColor(0)

    return histo

######################################################################
def doBinSignifPlots(p, drawPlot, datasets, histo, hName, xLabel, yLabel, saveName):
    '''
    def doBinSignifPlots(p, drawPlot, datasets, histo, hName, xLabel, yLabel, saveName):
    '''

    nDataDatasets = len(datasets.getDataDatasets())
    nMCDatasets   = len(datasets.getMCDatasets())

    if nMCDatasets<1:
        print "*** WARNING: No MC datasets found. Skipping significance plots."
        return

    # Legend and save-name
    histograms.createLegend.setDefaults(x1=0.65, x2= 0.90, y1 = 0.8, y2=0.92)
    saveName = saveName + "_BinSignif"
    saveName = saveName.replace("/", "_")

    MyIntegral = lambda h, bin: h.Integral(bin, bin)
    yLabel = "Significance (bin)"

    ### Setup the histogram text mode and create plot
    histograms.cmsTextMode = histograms.CMSMode.SIMULATION
    p2 = createTH1Plot(datasets, hName, normalizeToOne = False)

    ### Construct an empty histogram (same binning as variable distribution)
    hBinSignif = p.histoMgr.getHisto("TTToHplus_M"+signalMass).getRootHisto().Clone(saveName+"_Clone")
    hBinSignif.Reset()
    nBinsX = hBinSignif.GetNbinsX()
    nBins  = nBinsX+1
    binWidth = p.histoMgr.getHisto("TTToHplus_M"+signalMass).getRootHisto().GetBinWidth(1)
    firstLowEdge = p.histoMgr.getHisto("TTToHplus_M"+signalMass).getRootHisto().GetXaxis().GetBinLowEdge(1) - binWidth/2
    lastUpEdge = p.histoMgr.getHisto("TTToHplus_M"+signalMass).getRootHisto().GetXaxis().GetBinUpEdge(nBinsX) + binWidth/2
    hSignif = ROOT.TH1F(saveName, saveName, nBins, firstLowEdge, lastUpEdge)

    ### Loop over all histogram bins
    for iBin in xrange(0, nBins):
        ### Initialise variables to be used in Significance calculation
        nSignal        = 0
        nBackgr        = 0
        signifError    = 0
        signifValue    = 0
        # Loop over all histograms to determine the number of signal and bkg events to calculate significance
        for htmp in p.histoMgr.getHistos():
            h = htmp.getRootHisto()
            name = htmp.getName()
            if( "Data" in name or "sum_errors" in name ):
                continue
            elif("TTToHplus_M" + signalMass in name):
                #print "*** Signal-Histo = ", (name)
                nSignal = MyIntegral(h, iBin)
            else:
                if name == "StackedMC":
                    hStackedMC = p.histoMgr.getHisto("StackedMC").getRootHisto().Clone("hStackedMC_Clone")
                    for htmp in hStackedMC.GetHists():
                        name = htmp.GetName()
                        if ("MCuncertainty") in name:
                            continue
                        #print "*** Bkg-Histo = ", (name)
                        nBackgr += MyIntegral(htmp, iBin)
                        eBackgr = 0 #FIXME
                else:
                    if ("MCuncertainty") in name:
                        continue
                    #print "*** Bkg-Histo = ", (name)
                    nBackgr += MyIntegral(h, iBin)
                    eBackgr = 0 #FIXME

        if nSignal < 9e-04:
            nSignal = 0.0
        if nBackgr > 0 : #FIXME
            signifValue = math.sqrt( 2*( (nSignal+nBackgr)*math.log(1+(nSignal/nBackgr)) -nSignal) ) #G. Cowan (sysErrorBackgr=0)
            signifError = 0.0001 #FIXME
        else:
            signifValue = 0
            signifError = 0.0001 #FIXME

        if nSignal > 0 and nBackgr > 0:
            # signifErrorSquared = ( (1+2*math.log(1+nSignal/nBackgr)/(2*signifValue) )**2)*nSignal + ( ( (2*math.log(1+nSignal/nBackgr) - 2*nSignal/nBackgr)/(2*signifValue**2) )**2)**nBackgr
            #signifErrorSquared = ((signifValue/nSignal)**2)*nSignal + ((0.5*(signifValue/nBackgr))**2)*nBackgr
            #signifError = math.sqrt(signifErrorSquared)
            signifError = 0.0001
        else: 
            signifError = 0.0001
        #print " nSignal = %s, nBackgr = %s, signifValue = %s, signifError = %s" % (nSignal, nBackgr, signifValue, signifError) #attikis
        #print "*** iBin=%s ; Sig=%s ; S=%s ; B=%s" % (iBin, signifValue, nSignal, nBackgr)
        hBinSignif.SetBinContent(iBin, signifValue)
        hBinSignif.SetBinError(iBin, signifError) 

    # Loop over histograms and remove all histos 
    for htmp in p2.histoMgr.getHistos():
        h = htmp.getRootHisto()
        name = htmp.getName()
        if name == "StackedMC":
            hStackedMC = p.histoMgr.getHisto("StackedMC").getRootHisto().Clone("hStackedMC_Clone")
            for htmp in hStackedMC.GetHists():
                p2.histoMgr.removeHisto(name)
        else:
            p2.histoMgr.removeHisto(name)

    ### Add the significance plots to the histo-manager
    h = histograms.Histo(setSignificanceHistoStyle(hBinSignif), "      m_{H^{#pm}} = " + signalMass + " GeV/c^{2}", "HP", "HP")
    h.setIsDataMC(False, True)
    p2.histoMgr.appendHisto(h) 

    ### Draw the plot with custom options and save

    drawPlot = plots.PlotDrawer(stackMCHistograms=False, addMCUncertainty=False, log=False, ratio=False, addLuminosityText=True, opts={"ymaxfactor": 1.2})
    drawPlot(p2, saveName, xlabel=histo.xlabel, ylabel=yLabel, rebinToWidthX=histo.binWidthX, cutLine= getHistoCutLines(histo))

    return


######################################################################
def doSignifPlots(p, drawPlot, datasets, histo, hName, xLabel, yLabel, saveName, cutDir):
    '''
    def doSignifPlots(p, drawPlot, datasets, histo, hName, xLabel, yLabel, saveName, CutDir):
    '''

    nDataDatasets = len(datasets.getDataDatasets())
    nMCDatasets   = len(datasets.getMCDatasets())

    if nMCDatasets<1:
        print "*** WARNING: No MC datasets found. Skipping significance plots."
        return

    if cutDir == "<":
        saveName = saveName + "_SignifLessThan"
        saveName = saveName.replace("/", "_")
        MyIntegral = lambda h, bin: h.Integral(0, bin)
    elif cutDir == ">":
        saveName = saveName + "_SignifGreaterThan"
        saveName = saveName.replace("/", "_")
        MyIntegral = lambda h, bin: h.Integral(bin, nBins)
    else:
        print "%sERROR! Unsupported cut-direction string %s used. Exiting ROOT" % (cutDir)
        sys.exit()
    yLabel = "Significance" + "(" + cutDir + ")"

    # Legend and save-name
    histograms.createLegend.setDefaults(x1=0.65, x2= 0.90, y1 = 0.8, y2=0.92)

    ### Setup the histogram text mode and create plot
    histograms.cmsTextMode = histograms.CMSMode.SIMULATION
    p2 = createTH1Plot(datasets, hName, normalizeToOne = False)

    ### Construct an empty histogram (same binning as variable distribution)
    hBinSignif = p.histoMgr.getHisto("TTToHplus_M"+signalMass).getRootHisto().Clone(saveName+"_Clone")
    hBinSignif.Reset()
    nBinsX = hBinSignif.GetNbinsX()
    nBins  = nBinsX+1

    ### Loop over all histogram bins
    for iBin in xrange(0, nBins):
        ### Initialise variables to be used in Significance calculation
        nSignal        = 0
        nBackgr        = 0
        signifError    = 0
        signifValue    = 0
        # Loop over all histograms to determine the number of signal and bkg events to calculate significance
        for htmp in p.histoMgr.getHistos():
            h = htmp.getRootHisto()
            name = htmp.getName()
            if( "Data" in name or "sum_errors" in name ):
                continue
            elif("TTToHplus_M" + signalMass in name):
                #print "*** Signal-Histo = ", (name)
                nSignal = MyIntegral(h, iBin)
            else:
                if name == "StackedMC":
                    hStackedMC = p.histoMgr.getHisto("StackedMC").getRootHisto().Clone("hStackedMC_Clone")
                    for htmp in hStackedMC.GetHists():
                        name = htmp.GetName()
                        if ("MCuncertainty") in name:
                            continue
                        #print "*** Bkg-Histo = ", (name)
                        nBackgr += MyIntegral(htmp, iBin)
                        eBackgr = 0 #FIXME
                else:
                    if ("MCuncertainty") in name:
                        continue
                    #print "*** Bkg-Histo = ", (name)
                    nBackgr += MyIntegral(h, iBin)
                    eBackgr = 0 #FIXME

        if nSignal < 9e-04:
            nSignal = 0.0
        if nBackgr > 0 : #FIXME
            signifValue = math.sqrt( 2*( (nSignal+nBackgr)*math.log(1+(nSignal/nBackgr)) -nSignal) ) #G. Cowan (sysErrorBackgr=0)
            signifError = 0.0001 #FIXME
        else:
            signifValue = 0
            signifError = 0.0001 #FIXME

        # Calculate error on significance
        if nSignal > 0 and nBackgr > 0:
            #signifErrorSquared = ( (1+2*math.log(1+nSignal/nBackgr)/(2*signifValue) )**2)*nSignal + ( ( (2*math.log(1+nSignal/nBackgr) - 2*nSignal/nBackgr)/(2*signifValue**2) )**2)**nBackgr
            #signifErrorSquared = ((signifValue/nSignal)**2)*nSignal + ((0.5*(signifValue/nBackgr))**2)*nBackgr
            #signifError = math.sqrt(signifErrorSquared)
            signifError = 0.0001
        else: 
            signifError = 0.0001
        #print " nSignal = %s, nBackgr = %s, signifValue = %s, signifError = %s" % (nSignal, nBackgr, signifValue, signifError) #attikis
        #print "*** iBin=%s ; Sig=%s ; S=%s ; B=%s" % (iBin, signifValue, nSignal, nBackgr)
        hBinSignif.SetBinContent(iBin, signifValue)
        hBinSignif.SetBinError(iBin, signifError) 

    # Loop over histograms and remove all histos 
    for htmp in p2.histoMgr.getHistos():
        h = htmp.getRootHisto()
        name = htmp.getName()
        if name == "StackedMC":
            hStackedMC = p.histoMgr.getHisto("StackedMC").getRootHisto().Clone("hStackedMC_Clone")
            for htmp in hStackedMC.GetHists():
                p2.histoMgr.removeHisto(name)
        else:
            p2.histoMgr.removeHisto(name)

    ### Add the significance plots to the histo-manager
    h = histograms.Histo(setSignificanceHistoStyle(hBinSignif), "      m_{H^{#pm}} = " + signalMass + " GeV/c^{2}", "HP", "HP")
    h.setIsDataMC(False, True)
    p2.histoMgr.appendHisto(h) 

    ### Draw the plot with custom options and save
    drawPlot = plots.PlotDrawer(stackMCHistograms=False, addMCUncertainty=False, log=False, ratio=False, addLuminosityText=True, opts={"ymaxfactor": 1.2})
    drawPlot(p2, saveName, xlabel=histo.xlabel, ylabel=yLabel, rebinToWidthX=histo.binWidthX, cutLine= getHistoCutLines(histo))

    return

######################################################################
def getHistoCutLines(h):

    if h.cutLines == None:
        return None
    else:
        # Replace 0.0 in cutLines with actual signal mass - Dirty trick
        for i in range(0, len(h.cutLines)):
            if h.cutLines[i] == 0.0:
                h.cutLines[i] = hplusMass
                break
            else:
                continue 
    return h.cutLines
    

######################################################################
if __name__ == "__main__":

    main()

    if not bBatchMode:
        raw_input("\n*** DONE! Press \"ENTER\" key exit session: ")

######################################################################
