#!/usr/bin/env python
'''

Usage:
./plotTemplate.py -m <pseudo_mcrab_directory>

'''

#================================================================================================
# Imports
#================================================================================================
import os
import sys
from optparse import OptionParser
import getpass
import socket

import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.styles as styles
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux

import ROOT

#================================================================================================
# Variable Definition
#================================================================================================
analysis    = "Kinematics"
#myPath      = "/Users/attikis/latex/talks/post_doc.git/HPlus/HIG-XY-XYZ/2016/Kinematics_xAugust2016/figures/signal/"
myPath      = None
kwargs      = {
    "saveFormats" : [".png"],
    "rebinX"      : 1,
    "rebinY"      : 1,
    "normalizeTo" : "One",
    "binWidthX"   : 0.10, #dev
    "binWidthY"   : 0.20, #dev
    "zMin"        : 1e-5,
    "zMax"        : 0.5e-1,
}

hNames = [
    # "MaxDiJetMass_dEta_Vs_dPhi",
    "MaxDiJetMass_dRap_Vs_dPhi",
    "BQuark1_BQuark2_dEta_Vs_dPhi",
    "BQuark1_BQuark3_dEta_Vs_dPhi",
    "BQuark1_BQuark4_dEta_Vs_dPhi",
    "BQuark2_BQuark3_dEta_Vs_dPhi",
    "BQuark2_BQuark4_dEta_Vs_dPhi",
    "BQuark3_BQuark4_dEta_Vs_dPhi",
    "Jet1Jet2_dEta_Vs_Jet3Jet4_dEta",
    "Jet1Jet2_dPhi_Vs_Jet3Jet4_dPhi",

    "Jet1Jet2_dEta_Vs_Jet1Jet2_Mass",
    "Jet3Jet4_dEta_Vs_Jet3Jet4_Mass",
]

#================================================================================================
# Main
#================================================================================================
def main():

    style    = tdrstyle.TDRStyle()
    #style.setWide(True)
    style.setPaletteMy()
    ROOT.gStyle.SetNumberContours(20)
    # tdrstyle.setDeepSeaPalette()
    # tdrstyle.setRainBowPalette()
    # tdrstyle.setDarkBodyRadiatorPalette()
    # tdrstyle.setGreyScalePalette()
    # tdrstyle.setTwoColorHuePalette()
 
    savePath = myPath
    
    # Set ROOT batch mode boolean
    ROOT.gROOT.SetBatch(parseOpts.batchMode)
    
    # Get all datasets from the mcrab dir
    datasets  = GetDatasetsFromDir(parseOpts.mcrab, analysis)

    # Determine Integrated Luminosity (If Data datasets present)
    intLumi = GetLumi(datasets)
        
                  
    # For-loop: All Histogram names
    for counter, hName in enumerate(hNames):
        if savePath == None:
            savePath = GetSavePath(analysis)
        saveName = os.path.join(savePath, hName)
                

        # Get customised histos
        rootHistos = GetCustomisedHistos(datasets, hName, **kwargs)

        
        # Create a comparison plot
        p = plots.PlotBase(rootHistos, len(kwargs.get("saveFormats")))
        

        # Remove negative contributions (BEFORE rebinnin)
        RemoveNegativeBins(rootHistos[0].getHistogram(), p)


        # Customize
        p.histoMgr.forEachHisto(lambda h: h.getRootHisto().RebinX(kwargs.get("rebinX")))
        p.histoMgr.forEachHisto(lambda h: h.getRootHisto().RebinY(kwargs.get("rebinY")))
        p.histoMgr.setHistoDrawStyleAll("COLZ")        
        # p.histoMgr.forEachHisto(lambda h: h.getRootHisto().GetXaxis().SetRangeUser(1.0, 5.0))
        # p.histoMgr.forEachHisto(lambda h: h.getRootHisto().GetYaxis().SetRangeUser(1.0, 5.0))
        # p.histoMgr.forEachHisto(lambda h: h.getRootHisto().GetZaxis().SetRangeUser(0.0, 0.015))
        p.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetMinimum(kwargs.get("zMin")))
        p.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetMaximum(kwargs.get("zMax")))

        
        # Create a frame
        opts     = {"xmin": 0.0, "ymin": 0.0, "ymaxfactor": 1.0} #"ymax": 3.8}
        fileName = os.path.join(savePath, hName)
        p.createFrame(fileName, **opts)
        # Customise frame
        p.getFrame().GetXaxis().SetTitle( getTitleX(rootHistos[0], **kwargs) )
        p.getFrame().GetYaxis().SetTitle( getTitleY(rootHistos[0], **kwargs) )
        p.getFrame().GetZaxis().SetTitle( getTitleZ(rootHistos[0], **kwargs) ) #dev
        

        # SetLog
        p.getPad().SetLogy(False)
        p.getPad().SetLogx(False)
        p.getPad().SetLogz(True)

        
        # Add cut line/box
        _kwargs = { "lessThan": True}
        p.addCutBoxAndLine(cutValue=5, fillColor=ROOT.kBlue+2, box=False, line=True, **_kwargs)

        
        # Customise Legend
        moveLegend = {"dx": -0.1, "dy": +0.0, "dh": -0.1}
        p.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))
        p.removeLegend()


        # Add MC Uncertainty (Invalid method for a 2-d histogram)
        #p.addMCUncertainty()

        
        #  Draw plots
        p.draw()

        
        # Customise text
        histograms.addStandardTexts(lumi=intLumi)

        
        # Save canvas under custom dir
        if counter == 0:
            Print("Saving plots in %s format(s)" % (len(kwargs.get("saveFormats"))) )
        SavePlotterCanvas(p, saveName, savePath, **kwargs)

    return

#================================================================================================
# Auxiliary Function Definition
#================================================================================================
def RemoveNegativeBins(h, p):
    for i in range(h.GetNbinsX()):
        for j in range(h.GetNbinsY()):
            if h.GetBinContent(i, j) < 0:
                p.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetBinContent(i, j, 0))
    return

                
def GetDatasetsFromDir(mcrab, analysis):

    # datasets = dataset.getDatasetsFromMulticrabDirs([mcrab], analysisName=analysis)
    datasets  = dataset.getDatasetsFromMulticrabDirs([parseOpts.mcrab], analysisName=analysis, includeOnlyTasks="ChargedHiggs_HplusTB_HplusToTB_M_500")
    # datasets  = dataset.getDatasetsFromMulticrabDirs([parseOpts.mcrab], analysisName=analysis, excludeTasks="Tau_Run2015C|Tau\S+25ns_Silver$|DYJetsToLL|WJetsToLNu$")

    # Inform user of datasets retrieved
    Print("Got following datasets from multicrab dir \"%s\"" % mcrab)
    for d in datasets.getAllDatasets():
        print "\t", d.getName()
    return datasets


def GetCustomisedHistos(datasets, hName, **kwargs):
    rootHistos = []

    # Get Data or MC datasets
    myDatasets = datasets.getAllDatasets()
    # myDatasets = datasets.getDataDatasets()
    # myDatasets   = datasets.getMCDatasets()

    # For-loop: All-Datasets
    for d in myDatasets:
        
        # Build ROOT histos from individual datasets
        h = datasets.getDataset(d.getName()).getDatasetRootHisto(hName)
        rootHistos.append(h)
        
    # Normalise ROOT histograms
    for h in rootHistos:
        if kwargs.get("normalizeTo") == "One":
            h.normalizeToOne()
        elif kwargs.get("normalizeTo") == "XSection":
            h.normalizeByCrossSection()
        elif kwargs.get("normalizeTo") == "Luminosity":
            h.normalizeToLumi(intLumi)
        elif kwargs.get("normalizeTo") == "":
            pass
        else:
            isValidNorm(normalizeTo)
    return rootHistos
        

def GetSelfName():
    return __file__.split("/")[-1]


def Print(msg, printHeader=True):
    if printHeader:
        print "=== %s: %s" % (GetSelfName(), msg)
    else:
        print msg 
    return


def Verbose(msg, printHeader=True):
    if not parseOpts.verbose:
        return
    Print (msg, printHeader)
    return


def GetSavePath(analysis):
    user    = getpass.getuser()
    initial = getpass.getuser()[0]
    
    if "lxplus" in socket.gethostname():
        savePath = "/afs/cern.ch/user/%s/%s/public/html/%s/" % (initial, user, analysis)
    else:
        savePath = "/Users/%s/Desktop/Plots/" % (user)
    return savePath


def SavePlotterCanvas(p, saveName, savePath, **kwargs):
    formats  = kwargs.get("saveFormats")
    Verbose("Saving plots in %s format(s)" % (len(formats)) )

    # For-loop: All formats to save file
    for ext in formats:        
        sName = saveName + ext

        # Change print name if saved under html
        if "html" in sName:
            sName = sName.replace("/afs/cern.ch/user/%s/" % (initial), "http://cmsdoc.cern.ch/~")
            sName = sName.replace("%s/public/html/" % (user), "%s/" % (user))

        # Print save name
        print "\t", sName

        # Check if dir exists
        if not os.path.exists(savePath):
            os.mkdir(savePath)

        # Save the plots
        p.save(formats)
    return

        
def GetLumi(datasets):
    '''
    '''
    Print("Determining integrated luminosity from data-datasets")

    intLumi = None
    if len(datasets.getDataDatasets()) == 0:
        return intLumi

    # Load Luminosity JSON file
    datasets.loadLuminosities(fname="lumi.json")

    # Load RUN range
    # runRange = datasets.loadRunRange(fname="runrange.json")

    # For-loop: All Data datasets
    for d in datasets.getDataDatasets():
        print "\tluminosity", d.getName(), d.getLuminosity()
        intLumi += d.getLuminosity()
    print "\tluminosity, sum", intLumi
    return intLumi


def getUnitsFormatX(hName):

    VarsToNDecimals = {
        "MaxDiJetMass_dEta_Vs_dPhi"      : "%0.2f",
        "MaxDiJetMass_dRap_Vs_dPhi"      : "%0.2f",
        "BQuark1_BQuark2_dEta_Vs_dPhi"   : "%0.2f",
        "BQuark1_BQuark3_dEta_Vs_dPhi"   : "%0.2f",
        "BQuark1_BQuark4_dEta_Vs_dPhi"   : "%0.2f",
        "BQuark2_BQuark3_dEta_Vs_dPhi"   : "%0.2f",
        "BQuark2_BQuark4_dEta_Vs_dPhi"   : "%0.2f",
        "BQuark3_BQuark4_dEta_Vs_dPhi"   : "%0.2f",
        "Jet1Jet2_dEta_Vs_Jet3Jet4_dEta" : "%0.2f",
        "Jet1Jet2_dPhi_Vs_Jet3Jet4_dPhi" : "%0.2f",
        "Jet1Jet2_dEta_Vs_Jet1Jet2_Mass" : "%0.2f",
        "Jet3Jet4_dEta_Vs_Jet3Jet4_Mass" : "%0.2f",
    }
    
    return VarsToNDecimals[hName]


def getSymbolY(normalizeTo):
    isValidNorm(normalizeTo)
    NormToSymbols = {"One": "Arbitrary Units", "Luminosity": "Events", "": "Arbitrary Units", "XSection": "#sigma [pb]", "": ""}
    
    return NormToSymbols[normalizeTo]
    

def getTitleX(histo, **kwargs):
    binWidthX = histo.getHistogram().GetXaxis().GetBinWidth(1)*kwargs.get("rebinX")
    titleX    = histo.getHistogram().GetXaxis().GetTitle() + " / %s" %  str(binWidthX)
    return titleX


def getTitleY(histo, **kwargs):
    binWidthY = histo.getHistogram().GetYaxis().GetBinWidth(1)*kwargs.get("rebinY")
    titleY    = histo.getHistogram().GetYaxis().GetTitle() + " / %s" %  str(binWidthY)
    return titleY

def getTitleZ(histo, **kwargs):
    titleZ    = getSymbolY(kwargs.get("normalizeTo"))
    return titleZ

    
def isValidNorm(normalizeTo):
    validNorms = ["One", "XSection", "Luminosity", ""]

    if normalizeTo not in validNorms:
        raise Exception("Invalid normalization option \"%s\". Please choose one of the following: %s" % (normalizeTo, "\"" + "\", \"".join(validNorms) ) + "\"")
    return


#================================================================================================
# Main
#================================================================================================
if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]" , add_help_option=False,conflict_handler="resolve")
    parser.add_option("-m", "--mcrab"    , dest="mcrab"    , action="store", help="Path to the multicrab directory for input")
    parser.add_option("-b", "--batchMode", dest="batchMode", action="store_false", default=True, help="Enables batch mode (canvas creation does NOT generates a window)")
    parser.add_option("-v", "--verbose"  , dest="verbose"  , action="store_true", default=False, help="Enables verbose mode (for debugging purposes)")
    (parseOpts, parseArgs) = parser.parse_args()

    # Require at least two arguments (script-name, path to multicrab)
    if parseOpts.mcrab == None:
        Print("Not enough arguments passed to script execution. Printing docstring & EXIT.")
        print __doc__
        sys.exit(0)
    else:
        pass

    # Program execution
    main()

    if not parseOpts.batchMode:
        raw_input("=== plotTemplate.py: Press any key to quit ROOT ...")


#        args = {
#            "xlabel": "x",
#            "ylabel": "y",
#            "zlabel": "z",
#            "xlabelsize": None,
#            "ylabelsize": None,
#            "zhisto": None,
#            "log": False,
#            "ratio": False,
#            "ratioYlabel": None, 
#            "ratioInvert": False,
#            "ratioType": None,
#            #"ratioErrorOptions": 
#            "ratioCreateLegend": True,
#            #"ratioMoveLegend":
#            #"opts":
#            #"optsLog":
#            #"opts2":
#            #"canvasOpts":
#            "backgroundColor": ROOT.kRed,
#            "rebin": 1,
#            "rebinX": 1,
#            "rebinY": 1,
#            "rebinToWidthX": None,
#            "rebinToWidthY": None,
#            "divideByBinWidth": None,
#            "errorBarsX": True,
#            "createLegend": None,
#            #"moveLegend": 
#            #"customizeBeforeFrame":
#            #"customizeBeforeDraw":
#            #"customizeBeforeSave":
#            #"addLuminosityText":
#            "stackMCHistograms": True,
#            "addMCUncertainty": True,
#            "cmsText": True,
#            "cmsExtraText": True,
#            "addCmsText": True,
#            "cmsTextPosition": None,
#            "cmsExtraTextPosition": None,
#        }
#        
#        p.setDrawOptions(**args)
