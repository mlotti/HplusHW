#!/usr/bin/env python

import os
import sys
import array
from optparse import OptionParser

import NtupleAnalysis.toolsdataset as dataset
import NtupleAnalysis.toolstdrstyle as tdrstyle
import NtupleAnalysis.toolsstyles as styles
import NtupleAnalysis.toolsplots as plots
import NtupleAnalysis.toolshistograms as histograms

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

def findModuleNames(multicrabdir, prefix):
    items = os.listdir(multicrabdir)
    for i in items:
        if os.path.isdir(os.path.join(multicrabdir, i)):
            path = ""
            if os.path.exists(os.path.join(multicrabdir, i, "res")):
                path = os.path.join(multicrabdir, i, "res")
            elif os.path.exists(os.path.join(multicrabdir, i, "results")):
                path = os.path.join(multicrabdir, i, "results")
            # Find root file
            newitems = os.listdir(path)
            rootFile = None
            for j in newitems:
                if j.startswith("histograms-") and j.endswith(".root"):
                    rootFile = j
            if rootFile != None:
                f = ROOT.TFile.Open(os.path.join(path, rootFile), "r")
                myList = []
                for key in f.GetListOfKeys():
                    if key.GetClassName() == "TDirectoryFile" and key.ReadObj().GetName().startswith(prefix):
                        myList.append(key.ReadObj().GetName())
                f.Close()
                return myList
    return []

def findProperBinning(hPassed, hAll, binEdges, errorlevel):
    # Obtain minimum bin for skipping zero bins 
    myMinBinIndex = 999
    for k in range(1, hPassed.GetNbinsX()+1):
        if hAll.GetBinContent(k) > 0:
            myMinBinIndex = min(k,myMinBinIndex)
    for k in range(0,myMinBinIndex-1):
        #print "initial remove:",binEdges[0]
        binEdges.remove(binEdges[0])
    # Calculate efficiency curve
    hEff = ROOT.TEfficiency(hPassed, hAll)
    for k in range(myMinBinIndex, hPassed.GetNbinsX()):
        deltaLow = 1.0
        deltaHigh = 1.0
        if hEff.GetEfficiency(k) > 0.0:
            deltaLow = hEff.GetEfficiencyErrorLow(k)/hEff.GetEfficiency(k)
            deltaHigh = hEff.GetEfficiencyErrorUp(k)/hEff.GetEfficiency(k)
        #print "idx",k,hPassed.GetXaxis().GetBinLowEdge(k),deltaLow,deltaHigh
        if max(deltaLow,deltaHigh) > float(errorlevel):
            # merge to next bin and rebin
            #print "remove",hPassed.GetXaxis().GetBinLowEdge(k+1), binEdges
            binEdges.remove(hPassed.GetXaxis().GetBinLowEdge(k+1))
            myArray = array.array("d", binEdges)
            hAllNew = hAll.Rebin(len(myArray)-1, "", myArray)
            hPassedNew = hPassed.Rebin(len(myArray)-1, "", myArray)
            return findProperBinning(hPassedNew, hAllNew, binEdges, errorlevel)
    return (hPassed, hAll)

def doPlot(name, dset, errorlevel):
    myPartons = ["B", "C", "G", "Light"]
    myPartonLabels = ["b#rightarrowb", "c#rightarrowb", "g#rightarrowb", "uds#rightarrowb"]
    histoObjects = []
    for i in range(len(myPartons)):
        n = "All%sjets"%myPartons[i]
        (hAll, hAllName) = dset.getRootHisto(n)
        if hAll == None:
            raise Exception("Error: could not find histogram '%s'!"%n)
        n = "Selected%sjets"%myPartons[i]
        (hPassed, hPassedName) = dset.getRootHisto(n)
        if hPassed == None:
            raise Exception("Error: could not find histogram '%s'!"%n)
        # Find proper binning
        myBinEdges = []
        for k in range(1, hPassed.GetNbinsX()+1):
            myBinEdges.append(hPassed.GetXaxis().GetBinLowEdge(k))
        myBinEdges.append(hPassed.GetXaxis().GetBinUpEdge(hPassed.GetNbinsX()))
        (hPassed, hAll) = findProperBinning(hPassed, hAll, myBinEdges, errorlevel)
        # Construct efficiency plot
        hEff = ROOT.TEfficiency(hPassed, hAll)
        styles.styles[i].apply(hEff)
        hobj = histograms.HistoEfficiency(hEff, myPartonLabels[i], legendStyle="P", drawStyle="")
        #histograms.HistoGraph(eff2, "eff2", "p", "P")
        hobj.setIsDataMC(False, True)
        histoObjects.append(hobj)
    myPlot = plots.PlotBase(histoObjects)
    #myPlot.setLuminosity(-1) # Do not set 
    myPlot.setEnergy("13")
    #myPlot.setDefaultStyles()
    myParams = {}
    myParams["xlabel"] = "Jet p_{T}, GeV"
    myParams["ylabel"] = "Probability for passing b tagging"
    myParams["log"] = True
    myParams["cmsExtraText"] = "Simulation"
    myParams["cmsTextPosition"] = "outframe" # options: left, right, outframe
    myParams["opts"] = {"ymin": 1e-3, "ymax": 1.0}
    #myParams["opts2"] = {"ymin": 0.5, "ymax":1.5}
    #myParams["moveLegend"] = {"dx": -0.08, "dy": -0.12, "dh": 0.1} # for MC EWK+tt
    #myParams["moveLegend"] = {"dx": -0.15, "dy": -0.12, "dh":0.05} # for data-driven
    myParams["moveLegend"] = {"dx": 0.0, "dy": -0.46} # for data-driven
    
    drawPlot = plots.PlotDrawer(ratio=False, 
                            #stackMCHistograms=False, addMCUncertainty=True,
                            addLuminosityText=False,
                            cmsTextPosition="outframe")
    drawPlot(myPlot, "%s_%s"%(dset.name, name), **myParams)


def main():
    style = tdrstyle.TDRStyle()
    
    parser = OptionParser(usage="Usage: %prog [options]",add_help_option=False,conflict_handler="resolve")
    parser.add_option("-m", "--mcrab", dest="mcrab", action="store", help="Path to the multicrab directory for input")
    parser.add_option("-d", "--dataset", dest="dataset", action="store", help="Name of the dataset to be plotted")
    parser.add_option("-e", "--error", dest="errorlevel", default=0.10, action="store", help="Maximum relative uncertainty per bin (default=10%%)")
    (opts, args) = parser.parse_args()

    if opts.mcrab == None:
        raise Exception("Please provide input multicrab directory with -m")
    if not os.path.exists(opts.mcrab):
        raise Exception("The input root file '%s' does not exist!"%opts.mcrab)
    if opts.dataset == None:
        raise Exception("Please provide dataset name with -d")

    # Find module names
    myNames = findModuleNames(opts.mcrab, "BTagEfficiency")

    # Get dataset managers
    for n in myNames:
        datasets = dataset.getDatasetsFromMulticrabDirs([opts.mcrab], analysisName=n)
        for dset in datasets.getMCDatasets():
            if dset.name.startswith(opts.dataset):
                doPlot(n, dset, opts.errorlevel)

if __name__ == "__main__":
    main()
