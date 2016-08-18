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
import plotAux as plotAux

import ROOT

#================================================================================================
# Variable Definition
#================================================================================================
analysis    = "Kinematics"
#myPath      = "/Users/attikis/latex/talks/post_doc.git/HPlus/HIG-XY-XYZ/2016/Kinematics_16August2016/figures/signal/"
myPath      = None
massPoint   = "200"

kwargs      = {
    #"refDataset"     : "QCD",
    "refDataset"     : "ChargedHiggs_HplusTB_HplusToTB_M_%s" % (massPoint),
    "saveFormats"    : [".png"],# ".pdf"],
    "normalizeTo"    : "XSection",
    "createRatio"    : False,    
    "drawStyle"      : "LP", 
    "legendStyle"    : "lp", # "does not work for drawStyle = "HIST" 
}

hNames   = ["counters/weighted/Branching",
            "counters/weighted/Preselections"]


#================================================================================================
# Main
#================================================================================================
def main():

    style    = tdrstyle.TDRStyle()
    savePath = myPath

    # Set ROOT batch mode boolean
    ROOT.gROOT.SetBatch(parseOpts.batchMode)
    

    # Get all datasets from the mcrab dir
    datasetsMgr  = GetDatasetsFromDir(parseOpts.mcrab, analysis)


    # Determine Integrated Luminosity (If Data datasets present)
    intLumi = GetLumi(datasetsMgr)
    

    # Remove unwanted datasets
    datasetsMgr.remove(filter(lambda name: "HplusToTB" in name and not "M_%s" % (massPoint) in name, datasetsMgr.getAllDatasetNames()))
    # datasetsMgr.remove(filter(lambda name: "QCD" in name in name, datasetsMgr.getAllDatasetNames()))
    # datasetsMgr.remove(filter(lambda name: not "M_%s" % (massPoint) in name, datasetsMgr.getAllDatasetNames()))
    # datasetsMgr.remove(filter(lambda name: not "QCD" in name, datasetsMgr.getAllDatasetNames()))

    
    # Default merging & ordering: "Data", "QCD", "SingleTop", "Diboson"
    plots.mergeRenameReorderForDataMC(datasetsMgr)

    
    # For-loop: All Histogram names
    for counter, hName in enumerate(hNames):

        # Get the save path
        savePath = GetSavePath(analysis, savePath)

        # Get the save name (according to cut direction)
        saveName = GetSaveName(savePath, hName.replace("/", "_"))


        # Get customised histos
        rootHistos, histos    = GetCustomisedHistos(datasetsMgr, hName, **kwargs)
        refHisto, otherHistos = GetHistosForPlot(histos, rootHistos, **kwargs)

        # Create a comparison plot
        p = plots.ComparisonManyPlot(refHisto, otherHistos)
        

        # Remove negative contributions (BEFORE rebinning)
        RemoveNegativeBins(histos, p)


        # Create a frame
        opts      = {"ymin": 0.0, "ymaxfactor": 1.2}
        ratioOpts = {"ymin": 0.0, "ymax": 2.0}
        p.createFrame(saveName, createRatio=kwargs.get("createRatio"), opts=opts, opts2=ratioOpts)

        
        # Customise Legend
        moveLegend = {"dx": -0.2, "dy": +0.0, "dh": -0.1}
        p.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))
        #p.removeLegend()
        

        # Customise frame
        p.getFrame().GetYaxis().SetTitle( getTitleY(rootHistos[0], **kwargs) )
        #p.setEnergy("13")
        if kwargs.get("createRatio"):
            p.getFrame2().GetYaxis().SetTitle("Ratio")
            p.getFrame2().GetYaxis().SetTitleOffset(1.6)

        #  Draw plots
        p.draw()

        # Customise text
        histograms.addStandardTexts(lumi=intLumi)
        # histograms.addText(0.4, 0.9, "Alexandros Attikis", 17)
        # histograms.addText(0.4, 0.11, "Runs " + datasetsMgr.loadRunRange(), 17)

        
        # Save canvas under custom dir
        if counter == 0:
            Print("Saving plots in %s format(s)" % (len(kwargs.get("saveFormats"))) )
        SavePlotterCanvas(p, saveName, savePath, **kwargs)

    return

#================================================================================================
# Auxiliary Function Definition
#================================================================================================
def GetSavePath(analysis, savePath):
    if savePath != None:
        return savePath
    user    = getpass.getuser()
    initial = getpass.getuser()[0]
    if "lxplus" in socket.gethostname():
        savePath = "/afs/cern.ch/user/%s/%s/public/html/%s/" % (initial, user, analysis)
    else:
        savePath = "/Users/%s/Desktop/Plots/" % (user)
    return savePath


def GetSaveName(savePath, hName):
    saveName = os.path.join(savePath, hName)
    return saveName


def GetDatasetsFromDir(mcrab, analysis):

    datasetsMgr = dataset.getDatasetsFromMulticrabDirs([mcrab], analysisName=analysis)
    # datasets  = dataset.getDatasetsFromMulticrabDirs([parseOpts.mcrab], analysisName=analysis, includeOnlyTasks="ChargedHiggs_HplusTB_HplusToTB_M_")
    # datasets  = dataset.getDatasetsFromMulticrabDirs([parseOpts.mcrab], analysisName=analysis, excludeTasks="Tau_Run2015C|Tau\S+25ns_Silver$|DYJetsToLL|WJetsToLNu$")
    # datasets  = dataset.getDatasetsMgrFromMulticrabDirs([parseOpts.mcrab], analysisName=analysis, excludeTasks="M_180|M_220|M_250")

    # Inform user of datasets retrieved
    Verbose("Got following datasets from multicrab dir \"%s\"" % mcrab)
    for d in datasetsMgr.getAllDatasets():
        print "\t", d.getName()
    return datasetsMgr


def GetHistosForPlot(histos, rootHistos, **kwargs):
    refHisto     = None
    otherHistos  = []

    # For-loop: histos
    for rh in rootHistos:
        hName = rh.getName()

    # For-loop: histos
    for rh, h in zip(rootHistos, histos):
        #legName = "m_{H^{#pm}} = %s GeV/c^{2}" % (rh.getName().split("_M_")[-1])
        legName = plots._legendLabels[rh.getName()]

        if rh.getName() == kwargs.get("refDataset"):
            refHisto = histograms.Histo(h, legName, kwargs.get("drawStyle"), kwargs.get("legendStyle"))
        else:
            otherHistos.append( histograms.Histo(h, legName, kwargs.get("drawStyle"), kwargs.get("legendStyle")) )
    return refHisto, otherHistos


def GetCustomisedHistos(datasets, hName, **kwargs):
    # Declarations
    rootHistos = []
    histos     = []

    # Get Data or MC datasets
    myDatasets = datasets.getAllDatasets()
    # myDatasets = datasets.getDataDatasets()
    # myDatasets   = datasets.getMCDatasets()

    
    # For-loop: All-Datasets
    for d in myDatasets:
        
        # Build ROOT histos from individual datasets
        h = datasets.getDataset(d.getName()).getDatasetRootHisto(hName)

        # Set the cross-section
        # d.getDataset("TT_ext3").setCrossSection(831.76)        

        # Append to ROOT histos list
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
    

    # For-loop: All root histos
    for rh in rootHistos:
        h = rh.getHistogram()
        plotAux.styleDict[rh.getName()].apply(h)

        # Append the histogram
        histos.append(h)
    
    return rootHistos, histos
        

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


def RemoveNegativeBins(hList, p):
    for h in hList:        
        for i in range(h.GetNbinsX()):
            for j in range(h.GetNbinsY()):
                if h.GetBinContent(i, j) < 0:
                    p.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetBinContent(i, j, 0))
    return


def getTitleY(histo, **kwargs):
    binWidthY = histo.getHistogram().GetXaxis().GetBinWidth(1)

    if binWidthY < 1:
        titleY    = getSymbolY(kwargs.get("normalizeTo")) + " / %0.1f" %  float(binWidthY)
    elif binWidthY < 0.1:
        titleY    = getSymbolY(kwargs.get("normalizeTo")) + " / %0.2f" %  float(binWidthY)
    elif binWidthY < 0.01:
        titleY    = getSymbolY(kwargs.get("normalizeTo")) + " / %0.3f" %  float(binWidthY)
    else:
        titleY    = getSymbolY(kwargs.get("normalizeTo")) + " / %0.0f" %  float(binWidthY)
    return titleY


def getSymbolY(normalizeTo):
    isValidNorm(normalizeTo)
    NormToSymbols = {"One": "Arbitrary Units", "Luminosity": "Events", "": "Arbitrary Units", "XSection": "#sigma [pb]"}
    
    return NormToSymbols[normalizeTo]    

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
        
