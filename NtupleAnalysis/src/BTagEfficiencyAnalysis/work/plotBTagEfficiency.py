#!/usr/bin/env python

import os
import sys
import array
import json
from optparse import OptionParser

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.styles as styles
import HiggsAnalysis.NtupleAnalysis.tools.ShellStyles as shellStyles
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.analysisModuleSelector as analysisModuleSelector


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

def findProperBinning(hPassed, hAll, binEdges, errorlevel, binIndex=0, minWidth=0):
    #print "***",binIndex,minWidth,binEdges
    # Obtain minimum bin for skipping zero bins 
    myMinBinIndex = binIndex
    if binIndex == -1:
        myMinBinIndex = 999
        for k in range(1, hPassed.GetNbinsX()+1):
            if hAll.GetBinContent(k) > 0:
                myMinBinIndex = min(k,myMinBinIndex)
        for k in range(0,myMinBinIndex-1):
            #print "initial remove:",binEdges[0]
            binEdges.remove(binEdges[0])
    # Calculate efficiency curve
    tmpContents = []
    for k in range(0, hPassed.GetNbinsX()+2):
        a = hAll.GetBinContent(k)
        b = hPassed.GetBinContent(k)
        tmpContents.append(b)
        if b > a:
            hPassed.SetBinContent(k,a)
    #print "AAA"
    backup = ROOT.gErrorIgnoreLevel
    ROOT.gErrorIgnoreLevel = ROOT.kWarning
    hEff = ROOT.TEfficiency(hPassed.Clone(), hAll.Clone())
    hEff.SetStatisticOption(ROOT.TEfficiency.kFNormal) # using normal approximation because histograms are weighted
    ROOT.gErrorIgnoreLevel = backup
    #hEff.SetWeight(1.0)
    #print "BBB"
    for k in range(0, hPassed.GetNbinsX()+2):
        hPassed.SetBinContent(k,tmpContents[k])
    # Check if uncertainty is in the given bin
    for k in range(myMinBinIndex, hPassed.GetNbinsX()-1):
        deltaLow = 1.0
        deltaHigh = 1.0
        if hEff.GetEfficiency(k+1) > 0.0:
            deltaLow = hEff.GetEfficiencyErrorLow(k+1)/hEff.GetEfficiency(k+1)
            deltaHigh = hEff.GetEfficiencyErrorUp(k+1)/hEff.GetEfficiency(k+1)
        #print "idx",k,hPassed.GetXaxis().GetBinLowEdge(k),deltaLow,deltaHigh
        #print "PPP",k,hAll.GetBinContent(k+1),hPassed.GetBinContent(k+1),hEff.GetEfficiency(k),deltaLow,deltaHigh
        #print "*",k+1,hPassed.GetXaxis().GetBinWidth(k+1),minWidth
        if max(deltaLow,deltaHigh) > float(errorlevel) or hPassed.GetXaxis().GetBinWidth(k+1) < minWidth-0.1:
            # merge to next bin and rebin
            #print "remove",hPassed.GetXaxis().GetBinLowEdge(k+1), binEdges
            binEdges.remove(hPassed.GetXaxis().GetBinLowEdge(k+2))
            myArray = array.array("d", binEdges)
            hAllNew = hAll.Rebin(len(myArray)-1, "", myArray)
            hPassedNew = hPassed.Rebin(len(myArray)-1, "", myArray)
            w = hPassedNew.GetXaxis().GetBinWidth(k+1)
            if w > minWidth:
                minWidth = w
                #print "setting",minWidth, hPassed.GetXaxis().GetBinLowEdge(k+1), hPassed.GetXaxis().GetBinUpEdge(k+1)
            return findProperBinning(hPassedNew, hAllNew, binEdges, errorlevel, k, minWidth)
    return (hPassed, hAll)

def treatNegativeBins(h):
    for i in range(h.GetNbinsX()+2):
        if h.GetBinContent(i) < 0.0:
            h.SetBinContent(i, 0.0)

def doPlot(name, dset, errorlevel, optimizationMode, lumi):
    print shellStyles.HighlightStyle()+"Generating plots for dataset '%s'"%name+shellStyles.NormalStyle()
    s = optimizationMode.split("BjetDiscrWorkingPoint")
    discrName = s[0].replace("OptBjetDiscr","")
    discrWP = s[1]
    
    myPartons = ["B", "C", "G", "Light"]
    myPartonLabels = ["b#rightarrowb", "c#rightarrowb", "g#rightarrowb", "uds#rightarrowb"]
    histoObjects = []
    results = []
    for i in range(len(myPartons)):
        n = "All%sjets"%myPartons[i]
        dsetHisto = dset.getDatasetRootHisto(n)
        dsetHisto.normalizeToLuminosity(lumi)
        hAll = dsetHisto.getHistogram()
        #(hAll, hAllName) = dset.getRootHisto(n)
        if hAll == None:
            raise Exception("Error: could not find histogram '%s'!"%n)
        treatNegativeBins(hAll)
        n = "Selected%sjets"%myPartons[i]
        dsetHisto = dset.getDatasetRootHisto(n)
        dsetHisto.normalizeToLuminosity(lumi)
        hPassed = dsetHisto.getHistogram()
        #(hPassed, hPassedName) = dset.getRootHisto(n)
        if hPassed == None:
            raise Exception("Error: could not find histogram '%s'!"%n)
        treatNegativeBins(hPassed)
        # Find proper binning
        myBinEdges = []
        for k in range(1, hPassed.GetNbinsX()+1):
            if len(myBinEdges) > 0 or hPassed.GetBinContent(k) > 0:
                myBinEdges.append(hPassed.GetXaxis().GetBinLowEdge(k))
        myBinEdges.append(hPassed.GetXaxis().GetBinUpEdge(hPassed.GetNbinsX()))
        myArray = array.array("d", myBinEdges)
        hAllNew = hAll.Rebin(len(myArray)-1, "", myArray)
        hPassedNew = hPassed.Rebin(len(myArray)-1, "", myArray)
        (hPassed, hAll) = findProperBinning(hPassedNew, hAllNew, myBinEdges, errorlevel)
        #print myBinEdges
        # Treat fluctuations
        for k in range(hPassed.GetNbinsX()+2):
            if hPassed.GetBinContent(k) > hAll.GetBinContent(k):
                hPassed.SetBinContent(k, hAll.GetBinContent(k))
        # Construct efficiency plot
        eff = ROOT.TEfficiency(hPassed, hAll)
        eff.SetStatisticOption(ROOT.TEfficiency.kFNormal)
        for k in range(hPassed.GetNbinsX()):
            resultObject = {}
            resultObject["flavor"] = myPartons[i]
            resultObject["ptMin"] = hPassed.GetXaxis().GetBinLowEdge(k+1)
            resultObject["ptMax"] = hPassed.GetXaxis().GetBinUpEdge(k+1)
            resultObject["eff"] = eff.GetEfficiency(k+1)
            resultObject["effUp"] = eff.GetEfficiencyErrorUp(k+1)
            resultObject["effDown"] = eff.GetEfficiencyErrorLow(k+1)
            resultObject["discr"] = discrName
            resultObject["workingPoint"] = discrWP
            results.append(resultObject)
        #gEff = eff.CreateGraph()
        styles.styles[i].apply(eff)
        hobj = histograms.HistoEfficiency(eff, myPartonLabels[i], legendStyle="P", drawStyle="")
        #hobj = histograms.HistoGraph(gEff, myPartonLabels[i], legendStyle="P", drawStyle="")
        hobj.setIsDataMC(False, True)
        histoObjects.append(hobj)
    myPlot = plots.PlotBase(histoObjects)
    #myPlot.setLuminosity(-1) # Do not set 
    myPlot.setEnergy("13")
    #myPlot.setDefaultStyles()
    myParams = {}
    myParams["xlabel"] = "Jet p_{T} (GeV)"
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
    return results

def main():
    style = tdrstyle.TDRStyle()
    # Object for selecting data eras, search modes, and optimization modes
    myModuleSelector = analysisModuleSelector.AnalysisModuleSelector()

    parser = OptionParser(usage="Usage: %prog [options]",add_help_option=True,conflict_handler="resolve")
    myModuleSelector.addParserOptions(parser)
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
    #myNames = findModuleNames(opts.mcrab, "BTagEfficiency")

    # Get dataset managers
    # Obtain dsetMgrCreator and register it to module selector
    dsetMgrCreator = dataset.readFromMulticrabCfg(directory=opts.mcrab)
    myModuleSelector.setPrimarySource("analysis", dsetMgrCreator)
    # Select modules
    myModuleSelector.doSelect(opts)
    myModuleSelector.printSelectedCombinationCount()
    #for n in myNames:
    results = []
    for era in myModuleSelector.getSelectedEras():
        for searchMode in myModuleSelector.getSelectedSearchModes():
            for optimizationMode in myModuleSelector.getSelectedOptimizationModes():
                dsetMgr = dsetMgrCreator.createDatasetManager(dataEra=era,searchMode=searchMode,optimizationMode=optimizationMode)
                #datasets = dataset.getDatasetsFromMulticrabDirs(dirs=[opts.mcrab], analysisName=n)
                dsetMgr.loadLuminosities()
                dsetMgr.updateNAllEventsToPUWeighted()
                plots.mergeRenameReorderForDataMC(dsetMgr)
                lumi = dsetMgr.getDataset("Data").getLuminosity()
                for dset in dsetMgr.getMCDatasets():
                    print dset.name
                    if dset.name.startswith(opts.dataset):
                        results.extend(doPlot("btageff_%s_%s_%s"%(era, searchMode, optimizationMode), dset, opts.errorlevel, optimizationMode, lumi))
                  #dsetMgr.close()
    print "\nFigures generated"
    
    for item in results:
        print item
    
    # Write results to a json file
    filename = "btageff_%s.json"%opts.dataset
    with open(filename, 'w') as outfile:
        json.dump(results, outfile)
    print "Written results to %s"%filename

if __name__ == "__main__":
    main()
