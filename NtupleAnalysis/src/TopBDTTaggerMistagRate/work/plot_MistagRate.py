#!/usr/bin/env python
'''
DESCRIPTION:


USAGE:
./plot_Efficiency.py -m <pseudo_mcrab> [opts]


EXAMPLES:
./plot_MistagRate.py -m TopBDTTaggerMistagRate_180603_JetPt100_40_40_40_1bjet_HT500/ --folder TopBDTTagger_QCDMistagRate

LAST USD:
./plot_MistagRate.py -m TopBDTTaggerMistagRate_180603_JetPt100_40_40_40_1bjet_HT500/ --folder TopBDTTagger_QCDMistagRate


STATISTICS OPTIONS:
https://iktp.tu-dresden.de/~nbarros/doc/root/TEfficiency.html
statOption = ROOT.TEfficiency.kFCP       # Clopper-Pearson
statOption = ROOT.TEfficiency.kFNormal   # Normal Approximation
statOption = ROOT.TEfficiency.kFWilson   # Wilson
statOption = ROOT.TEfficiency.kFAC       # Agresti-Coull
statOption = ROOT.TEfficiency.kFFC       # Feldman-Cousins
statOption = ROOT.TEfficiency.kBJeffrey # Jeffrey
statOption = ROOT.TEfficiency.kBUniform # Uniform Prior
statOption = ROOT.TEfficiency.kBayesian # Custom Prior
'''
#================================================================================================ 
# Imports
#================================================================================================ 
import sys
import math
import copy
import os
from optparse import OptionParser

import getpass

import ROOT
import array

ROOT.gROOT.SetBatch(True)
from ROOT import *

import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.counter as counter
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.styles as styles
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.crosssection as xsect
import HiggsAnalysis.NtupleAnalysis.tools.multicrabConsistencyCheck as consistencyCheck
import HiggsAnalysis.NtupleAnalysis.tools.ShellStyles as ShellStyles
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux

from PythonWriter import PythonWriter
pythonWriter = PythonWriter()
# Ignore Runtime warnings: Base category for warnings about dubious runtime features.
import warnings
warnings.filterwarnings("ignore")

ROOT.gErrorIgnoreLevel = ROOT.kError
#================================================================================================ 
# Function Definition
#================================================================================================ 
def Print(msg, printHeader=False):
    fName = __file__.split("/")[-1]
    if printHeader==True:
        print "=== ", fName
        print "\t", msg
    else:
        print "\t", msg
    return

def Verbose(msg, printHeader=True, verbose=False):
    if not opts.verbose:
        return
    aux.Print(msg, printHeader)
    return

def GetLumi(datasetsMgr):
    Verbose("Determininig Integrated Luminosity")
    
    lumi = 0.0
    for d in datasetsMgr.getAllDatasets():
        if d.isMC():
            continue
        else:
            lumi += d.getLuminosity()
    Verbose("Luminosity = %s (pb)" % (lumi), True)
    return lumi

#def GetListOfQCDatasets():
#    Verbose("Getting list of QCD datasets")
#    return ["QCD_HT1000to1500", "QCD_HT1500to2000","QCD_HT2000toInf","QCD_HT300to500","QCD_HT500to700","QCD_HT700to1000"]
def GetRunRange(datasetsMgr):
    '''                                                                                                                                                                                                                 
    '''
    minRunRange = None
    maxRunRange = None
    nDataDatasets = len(datasetsMgr.getDataDatasets())

    # For-loop: All datasets                                                                                                                                                                                            
    for i, d in enumerate(datasetsMgr.getDataDatasets(), 1):
        if i == 1:
            minRunRange = d.getName().split("_")[-2]
        if i == nDataDatasets:
            maxRunRange = d.getName().split("_")[-1]
        runRange = d.getName().split("_")[-2] + " - " + d.getName().split("_")[-1]
        #runRange = d.getName()+ " - " + d.getName()
        Verbose("Dataset   = %s" % (d.getName()), i==1)
        Verbose("Run Range = %s" % (runRange), False)
        
    runRange = minRunRange + " - " + maxRunRange
    Verbose("Run Range = %s - %s" % (minRunRange, maxRunRange), True)
    return minRunRange, maxRunRange, runRange


def GetDatasetsFromDir(opts):
    Verbose("Getting datasets")
    
    if (not opts.includeOnlyTasks and not opts.excludeTasks):
        datasets = dataset.getDatasetsFromMulticrabDirs([opts.mcrab],
                                                        dataEra=opts.dataEra,
                                                        searchMode=opts.searchMode, 
                                                        analysisName=opts.analysisName,
                                                        optimizationMode=opts.optMode)
    elif (opts.includeOnlyTasks):
        datasets = dataset.getDatasetsFromMulticrabDirs([opts.mcrab],
                                                        dataEra=opts.dataEra,
                                                        searchMode=opts.searchMode,
                                                        analysisName=opts.analysisName,
                                                        includeOnlyTasks=opts.includeOnlyTasks,
                                                        optimizationMode=opts.optMode)
    elif (opts.excludeTasks):
        datasets = dataset.getDatasetsFromMulticrabDirs([opts.mcrab],
                                                        dataEra=opts.dataEra,
                                                        searchMode=opts.searchMode,
                                                        analysisName=opts.analysisName,
                                                        excludeTasks=opts.excludeTasks,
                                                        optimizationMode=opts.optMode)
    else:
        raise Exception("This should never be reached")
    return datasets
    

def GetHistoKwargs(histoName, opts):
    '''
    Dictionary with
    key   = histogram name
    value = kwargs
    '''
    h = histoName.lower()
    kwargs = {
        "xlabel"           : "p_{T} (GeV/c)",
        "ylabel"           : "Misidentification rate",
        "ratioYlabel"      : "Data/MC",
        "ratio"            : True,
        "ratioInvert"      : False,
        "ratioType"        : "errorScale",
        "ratioCreateLegend": True,
        "ratioMoveLegend"  : {"dx": -0.51, "dy": 0.03, "dh": -0.08},
        "ratioErrorOptions": {"numeratorStatSyst": False, "denominatorStatSyst": False},
        "errorBarsX"       : True,
        "stackMCHistograms": False,
        "addMCUncertainty" : False,
        "addLuminosityText": False,
        "addCmsText"       : True,
        "cmsExtraText"     : "Preliminary",
        "opts"             : {"ymin": 0.0, "ymaxfactor": 2.0, "xmax" : 600},
        "opts2"            : {"ymin": 0.30, "ymax": 1.70},
        "log"              : False,
        "createLegend"     : {"x1": 0.55, "y1": 0.70, "x2": 0.95, "y2": 0.92},
        }


    #kwargs = copy.deepcopy(_kwargs)
    #Soti Fix Me
    xlabel = "xlabel"
    units = ""
    #kwargs["xlabel"]  = "xlabel"
    #kwargs["ylabel"] += "units"
    myBins  = []
    #myBins  = [0, 100, 150, 200, 300, 400, 500, 600, 800]
    
    if "csv" in h:
        units   = ""
        xlabel  = "CSV"
        kwargs["opts"]   = {"xmin": 0.8, "xmax": 1.0, "ymin": 0.0, "ymaxfactor": 1.2}
        myBins  = [0.8, 0.86, 0.88, 0.90, 0.92, 0.94, 0.96, 0.98, 1.0]
        kwargs["xmin"] = 0.8
        kwargs["xmax"] = 1.0

    elif "mass" in h:
        units   = "GeV/c^{2}"
        xlabel  = "m_{T} (%s)" % (units)
        #myBins  = [0, 50, 100, 150, 200, 250, 300, 400, 500, 600, 800]
        #myBins  = [0, 100, 200, 300, 400, 500, 800]
        myBins  = [0, 100, 200, 300, 400, 500, 600, 800, 1000]
        kwargs["cutBox"] = {"cutValue": 100.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
        if "wmass" in h:
                    myBins  = [0, 20, 40, 60, 80, 100, 150, 200]
                    kwargs["opts"]   = {"xmin": 0, "xmax": 800, "ymin": 0.0, "ymaxfactor": 1.2}

        
    elif "pt" in h:
        units   = "GeV/c"
        xlabel  = "p_{T} (%s)" % (units)
        myBins  = [0, 100, 200, 300, 400, 500, 600]#, 800]
        kwargs["xmax"] = 600
        kwargs["cutBox"] = {"cutValue": 100.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
        kwargs["opts"]   = {"xmin": 0, "xmax": 600, "ymin": 0.0, "ymax": 0.322}

    elif "eta" in h:
        units   = ""
        xlabel  = "#eta"
        kwargs["opts"]   = {"xmin": -10, "xmax": 10, "ymin": 0.0, "ymaxfactor": 1.2}
        kwargs["cutBox"] = {"cutValue": 100.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
        myBins  = [-3.0, -2.5, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
        
    elif "phi" in h:
        units   = ""
        xlabel  = "#phi"
        kwargs["opts"]   = {"xmin": -3.2, "xmax": 3.2, "ymin": 0.0, "ymaxfactor": 1.2}
        kwargs["cutBox"] = {"cutValue": 100.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
        myBins  = [-3.0, -2.0, -1.0,  0.0, 1.0, 2.0, 3.0]
    elif "ht" in h:
        units   = "GeV/c"
        xlabel  = "H_{T} (%s)" % (units)
        myBins  = [0, 300, 400, 500, 600, 800]
        kwargs["cutBox"] = {"cutValue": 100.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
        kwargs["cutBoxY"]= {"cutValue": 1.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True, "mainCanvas": True, "ratioCanvas": False}

    elif "met" in h:
        units   = "GeV/c"
        xlabel  = "E_{T,missing} (%s)" % (units)
        myBins  = [0, 20, 50, 100, 200, 400, 800]
        kwargs["opts"]   = {"xmin": 0, "xmax": 400, "ymin": 0.0, "ymaxfactor": 1.2}
        kwargs["cutBox"] = {"cutValue": 100.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True}

    elif "njets" in h:
        units = ""
        xlabel  = "Jet multiplicity"
        kwargs["opts"]   = {"xmin": 4, "xmax": 14, "ymin": 0.0, "ymaxfactor": 1.2}
        kwargs["cutBox"] = {"cutValue": 100.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True}

    elif "nbjets" in h:
        units = ""
        xlabel  = "B-jet multiplicity"
        kwargs["opts"]   = {"xmin": 2, "xmax": 7, "ymin": 0.0, "ymaxfactor": 1.2}
        kwargs["cutBox"] = {"cutValue": 100.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True}



    kwargs["xlabel"]  = xlabel
    #if units != "":
    #    kwargs["ylabel"] += (" / "+units)


    if len(myBins) > 0:
        kwargs["binList"] = array.array('d', myBins)
    return kwargs


def main(opts, signalMass):

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    style.setOptStat(True)
    style.setGridX(False)
    style.setGridY(False)
    
    # If user does not define optimisation mode do all of them
    if opts.optMode == None:
        if len(optList) < 1:
            optList.append("")
        else:
            pass
        optModes = optList
    else:
        optModes = [opts.optMode]

    # For-loop: All optimisation modes
    for opt in optModes:
        opts.optMode = opt

        # Setup & configure the dataset manager 
        datasetsMgr = GetDatasetsFromDir(opts)
        datasetsMgr.updateNAllEventsToPUWeighted()
        datasetsMgr.loadLuminosities() # from lumi.json

        if opts.verbose:
            datasetsMgr.PrintCrossSections()
            datasetsMgr.PrintLuminosities()

        # Set/Overwrite cross-sections
        for d in datasetsMgr.getAllDatasets():
            if "ChargedHiggs" in d.getName():
                datasetsMgr.getDataset(d.getName()).setCrossSection(1.0)


        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        #plots.mergeRenameReorderForDataMC(datasetsMgr) 

        # Print dataset information before removing anything?
        datasetsMgr.PrintInfo()

        # Determine integrated Lumi before removing data
        if "Data" in datasetsMgr.getAllDatasetNames():
            intLumi = datasetsMgr.getDataset("Data").getLuminosity()
        # Remove datasets
        filterKeys = ["TTW"]
        for key in filterKeys:
            datasetsMgr.remove(filter(lambda name: key in name, datasetsMgr.getAllDatasetNames()))
        else:
            intLumi = 35920
        # Remove datasets
        #filterKeys = ["Data",  "TTZToQQ", "TTWJets", "TTTT", "QCD"]
        #filterKeys = ["Data", "TTZToQQ", "TTWJets", "TTTT"]
        for key in filterKeys:
            datasetsMgr.remove(filter(lambda name: key in name, datasetsMgr.getAllDatasetNames()))
        
        # Re-order datasets
        datasetOrder = []
        haveQCD = False
        for d in datasetsMgr.getAllDatasets():
            if "Charged" in d.getName():
                if d not in signalMass:
                    continue
            if "QCD" in d.getName():
                haveQCD = True
            datasetOrder.append(d.getName())
            
        # Append signal datasets
        for m in signalMass:
            datasetOrder.insert(0, m)
        datasetsMgr.selectAndReorder(datasetOrder)

        # Define the mapping histograms in numerator->denominator pairs
        VariableList = [
            "LdgTop_Pt",
            "Tops_Pt"
            ]
        minRunRange, maxRunRange, runRange = GetRunRange(datasetsMgr)
        print "This is my run range:", minRunRange, maxRunRange, runRange
        #runRange = datasetsMgr.loadRunRange()
        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        plots.mergeRenameReorderForDataMC(datasetsMgr) 
        
        datasets_  = datasetsMgr.getAllDatasets()
        #datasetsMgr.mergeMC()
        dataset_Data = datasetsMgr.getDataDatasets()
        dataset_MC   = datasetsMgr.getMCDatasets()

        # Print dataset information
        datasetsMgr.PrintInfo()


        # For-loop: All numerator-denominator pairs
        counter =  0
        nPlots  = len(VariableList)

        for var in VariableList:
            histoN = "AfterAllSelections_"+var
            histoD = "AfterStandardSelections_"+var
            numerator   = os.path.join(opts.folder, histoN)
            denominator = os.path.join(opts.folder, histoD)

            counter+=1
            msg = "{:<9} {:>3} {:<1} {:<3} {:<50}".format("Histogram", "%i" % counter, "/", "%s:" % (nPlots), "%s" % (var))
            Print(ShellStyles.SuccessStyle() + msg + ShellStyles.NormalStyle(), counter==1)
            
            for dataset in datasets_:

                if dataset.isMC():
                    n = dataset.getDatasetRootHisto(numerator)
                    n.normalizeToLuminosity(intLumi)
                    num = n.getHistogram()
                    d = dataset.getDatasetRootHisto(denominator)
                    d.normalizeToLuminosity(intLumi)
                    den = d.getHistogram()
                    
                else:
                    num = dataset.getDatasetRootHisto(numerator).getHistogram()
                    den = dataset.getDatasetRootHisto(denominator).getHistogram()
                                                            
                x_bins = num.GetXaxis().GetNbins()
                
                i = 1
                while i < x_bins:
                    xvalue = num.GetXaxis().GetBinLowEdge(i)+0.5*num.GetXaxis().GetBinWidth(i)
                    if xvalue < 20:
                        my_bin = i
                    i+=1
                        
                my_xvalue = num.GetXaxis().GetBinUpEdge(my_bin)+0.5*num.GetXaxis().GetBinWidth(my_bin)
                #print "test ", my_bin, my_xvalue
                total = den.Integral(0, x_bins) #my_bin
                selected = num.Integral(0, x_bins) #my_bin
                #print dataset.getName(), ":", selected, " events"
            #PlotEfficiency(datasetsMgr, numerator, denominator, intLumi)
            
            plotName     = "Eff_%s" % (var)
            # Get Efficiency Plots  
            _kwargs  = GetHistoKwargs(var, opts)
            eff_Data = GetEfficiency(datasetsMgr, dataset_Data, numerator, denominator, intLumi)
            eff_MC   = GetEfficiency(datasetsMgr, dataset_MC, numerator, denominator, intLumi)

            # Apply Styles 
            styles.dataStyle.apply(eff_Data)
            styles.qcdStyle.apply(eff_MC)
            # Create the plot
            p = plots.ComparisonPlot(histograms.HistoGraph(eff_Data, "eff_Data", "p", "P"),
                                     histograms.HistoGraph(eff_MC,   "eff_MC"  , "p", "P"),
                                     saveFormats=[])
            # Define the legend entries 
            p.histoMgr.setHistoLegendLabelMany(
                {
                    "eff_Data": "Data",
                    "eff_MC"  : "QCD"
                    }
                )

            # Apply default style (according to dataset name)
            #plots._plotStyles[dataset.getName()].apply(eff_Data)
            # Append in list
            myList = []
            myList.append(histograms.HistoGraph(eff_Data, plots._legendLabels["Data"], "lp", "P"))

            p.setLuminosity(intLumi)
            _kwargs["ratio"] = True
            #_kwargs["ratioInvert"] = True
            _kwargs["cutBoxY"] = {"cutValue": 1.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True, "mainCanvas": True, "ratioCanvas": True}
            plots.drawPlot(p, plotName, **_kwargs)
            # Draw 
            #savePath = os.path.join(opts.saveDir, "MistagRate", opts.optMode)
            #savePath = os.path.join(opts.saveDir, histoN.split("/")[0], opts.optMode)
            savePath = os.path.join(opts.saveDir, opts.optMode)
            SavePlot(p, plotName, savePath, saveFormats = [".png", ".pdf", ".C"])
        

        
    return


def CheckNegatives(hNum, hDen, verbose=False):
    '''
    Checks two histograms (numerator and denominator) bin-by-bin for negative contents.
    If such a bin is is found the content is set to zero.
    Also, for a given bin, if numerator > denominator they are set as equal.
    '''
    table    = []
    txtAlign = "{:<5} {:>20} {:>20}"
    hLine    = "="*50
    table.append(hLine)
    table.append(txtAlign.format("Bin #", "Numerator (8f)", "Denominator (8f)"))
    table.append(hLine)

    # For-loop: All bins in x-axis
    for i in range(1, hNum.GetNbinsX()+1):
        nbin = hNum.GetBinContent(i)
        dbin = hDen.GetBinContent(i)
        table.append(txtAlign.format(i, "%0.8f" % (nbin), "%0.8f" % (dbin) ))

        # Numerator > Denominator
        if nbin > dbin:
            hNum.SetBinContent(i, dbin)

        # Numerator < 0 
        if nbin < 0:
            hNum.SetBinContent(i,0)
            
        # Denominator < 0
        if dbin < 0:
            hNum.SetBinContent(i,0)
            hDen.SetBinContent(i,0)
    return


def RemoveNegatives(histo):
    '''
    Removes negative bins from histograms
    '''
    for binX in range(histo.GetNbinsX()+1):
        if histo.GetBinContent(binX) < 0:
            histo.SetBinContent(binX, 0.0)
    return


def PlotEfficiency(datasetsMgr, numPath, denPath, intLumi):  
    # Definitions
    myList  = []
    myList_MC  = []
    myList_Data = []
    index   = 0
    _kwargs = GetHistoKwargs(numPath, opts)        
    # For-loop: All datasets
    for dataset in datasetsMgr.getAllDatasets():

        if "Fake" in numPath and "TT" in dataset.getName():
            continue
            #dataset = datasetsMgr.getDataset("QCD")
        # Get the histograms
        #num = dataset.getDatasetRootHisto(numPath).getHistogram()
        #den = dataset.getDatasetRootHisto(denPath).getHistogram()

        if dataset.isMC():
            n = dataset.getDatasetRootHisto(numPath)
            n.normalizeToLuminosity(intLumi)                                                                                                                       
            num = n.getHistogram()
            d = dataset.getDatasetRootHisto(denPath)
            d.normalizeToLuminosity(intLumi)                                                                                                                       
            den = d.getHistogram()

        else:
            num = dataset.getDatasetRootHisto(numPath).getHistogram()
            den = dataset.getDatasetRootHisto(denPath).getHistogram()


        total = den.Integral(0, den.GetXaxis().GetNbins()+1)
        selected = num.Integral(0, num.GetXaxis().GetNbins()+1)
        print "Pass :", selected, dataset.getName(), " events"
        print "Numerical Efficiency", numPath, dataset.getName(), ":", round(selected/total, 3)

        if "binList" in _kwargs:
            #if len(_kwargs["binList"]) == 1:
            #    continue
            xBins   = _kwargs["binList"]
            nx      = len(xBins)-1
            num     = num.Rebin(nx, "", xBins)
            den     = den.Rebin(nx, "", xBins)
        elif "Eta" in numPath or "Phi" in numPath:
            num     = num.Rebin(2)
            den     = den.Rebin(2)
        # Sanity checks
        if den.GetEntries() == 0 or num.GetEntries() == 0:
            continue
        if num.GetEntries() > den.GetEntries():
            continue


        # Create Efficiency plots with Clopper-Pearson stats
        eff = ROOT.TEfficiency(num, den) # fixme: investigate warnings
        eff.SetStatisticOption(ROOT.TEfficiency.kFCP) #FCP
                
        # Convert to TGraph
        eff = convert2TGraph(eff)
        # Apply default style (according to dataset name)
        plots._plotStyles[dataset.getName()].apply(eff)

        # Append in list
        myList.append(histograms.HistoGraph(eff, plots._legendLabels[dataset.getName()], "lp", "P"))
        if dataset.isMC():
            eff_MC = eff
            if "QCD" in dataset.getName():
                eff_QCD = eff
            elif "TT" in dataset.getName():
                eff_TT= eff
            myList_MC.append(histograms.HistoGraph(eff, plots._legendLabels[dataset.getName()], "lp", "P"))
        else:
            eff_Data = eff
            plots._plotStyles[dataset.getName()].apply(eff_Data)
            #styles.dataStyle.apply(eff_Data)
            eff_Data.SetMarkerSize(1.2)
            myList_Data.append(histograms.HistoGraph(eff_Data, plots._legendLabels[dataset.getName()], "p", "P"))

    numPath = numPath.replace("AfterAllSelections_","")
    # Define save name
    saveName = "Eff_" + numPath.split("/")[-1]

    # Plot the efficiency
    p = plots.PlotBase(datasetRootHistos=myList, saveFormats=[])
    plots.drawPlot(p, saveName, **_kwargs)

    #p1 = plots.ComparisonManyPlot(histograms.HistoGraph(eff_Data, "data",  drawStyle="AP"), myList_MC, saveFormats=[])
    p1 = plots.ComparisonManyPlot(histograms.HistoGraph(eff_Data, "Data",  drawStyle="P"), 
                                  #[histograms.HistoGraph(eff_QCD, "qcd", drawStyle="P"), 
                                  # histograms.HistoGraph(eff_TT, "tt", drawStyle="P")], saveFormats=[])
                                  myList_MC, saveFormats=[])

    # Save plot in all formats
    savePath = os.path.join(opts.saveDir, "HplusMasses", numPath.split("/")[0], opts.optMode)
    #savePath = os.path.join(opts.saveDir, numPath.split("/")[0], opts.optMode)
    save_path = savePath + opts.MVAcut
    print "save_path", save_path
    # Draw and save the plot                                                                                                                                                     
    p1.setLuminosity(intLumi)
    _kwargs["ratio"] = True
    _kwargs["ratioInvert"] = True
    _kwargs["cutBoxY"] = {"cutValue": 1.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True, "mainCanvas": True, "ratioCanvas": True}
    plots.drawPlot(p1, save_path1, **_kwargs)
    #SavePlot(p, saveName, save_path, saveFormats = [".png", ".pdf"])
    SavePlot(p1, saveName, save_path, saveFormats = [".png", ".pdf", ".C"])
    return


def GetEfficiency(datasetsMgr, datasets, numPath, denPath, intLumi):     
    # Definitions
    myList  = []
    myList_MC  = []
    myList_Data = []
    index   = 0
    _kwargs = GetHistoKwargs(numPath, opts)        
    # For-loop: All datasets
    for dataset in datasets:
        if dataset.isMC():
            n = dataset.getDatasetRootHisto(numPath)
            n.normalizeToLuminosity(intLumi)                                                                                                                       
            num = n.getHistogram()
            d = dataset.getDatasetRootHisto(denPath)
            d.normalizeToLuminosity(intLumi)                                                                                                                       
            den = d.getHistogram()

        else:
            num = dataset.getDatasetRootHisto(numPath).getHistogram()
            den = dataset.getDatasetRootHisto(denPath).getHistogram()


        total = den.Integral(0, den.GetXaxis().GetNbins()+1)
        selected = num.Integral(0, num.GetXaxis().GetNbins()+1)

        print "Numerical Efficiency", numPath, dataset.getName(), ":", round(selected/total, 3)
        print "Pass :", selected, dataset.getName(), " events"
        if "binList" in _kwargs:
            #if len(_kwargs["binList"]) == 1:
            #    continue
            xBins   = _kwargs["binList"]
            nx      = len(xBins)-1
            num     = num.Rebin(nx, "", xBins)
            den     = den.Rebin(nx, "", xBins)
        #elif "Eta" in numPath or "Phi" in numPath:
        #    num     = num.Rebin(2)
        #    den     = den.Rebin(2)
        # Sanity checks
        if den.GetEntries() == 0 or num.GetEntries() == 0:
            continue
        if num.GetEntries() > den.GetEntries():
            continue

        # Create Efficiency plots with Clopper-Pearson stats
        eff = ROOT.TEfficiency(num, den) # fixme: investigate warnings
        eff.SetStatisticOption(ROOT.TEfficiency.kFCP) #FCP
                
        # Convert to TGraph
        eff = convert2TGraph(eff)
    return eff




def convert2TGraph(tefficiency):
    x     = []
    y     = []
    xerrl = []
    xerrh = []
    yerrl = []
    yerrh = []
    h     = tefficiency.GetCopyTotalHisto()
    n     = h.GetNbinsX()

    # For-loop: All bins
    for i in range(1, n+1):
        x.append(h.GetBinLowEdge(i)+0.5*h.GetBinWidth(i))
        xerrl.append(0.5*h.GetBinWidth(i))
        xerrh.append(0.5*h.GetBinWidth(i))
        y.append(tefficiency.GetEfficiency(i))
        yerrl.append(tefficiency.GetEfficiencyErrorLow(i))

        # ugly hack to prevent error going above 1
        errUp = tefficiency.GetEfficiencyErrorUp(i)
        if y[-1] == 1.0:
            errUp = 0
        yerrh.append(errUp)
        
    graph = ROOT.TGraphAsymmErrors(n, array.array("d",x), array.array("d",y),
                                   array.array("d",xerrl), array.array("d",xerrh),
                                   array.array("d",yerrl), array.array("d",yerrh)) 
    return graph


def SavePlot(plot, plotName, saveDir, saveFormats = [".C", ".png", ".pdf"]):
    Verbose("Saving the plot in %s formats: %s" % (len(saveFormats), ", ".join(saveFormats) ) )

     # Check that path exists                                                                                                                                                                               
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)

    # Create the name under which plot will be saved                                                                                                                                                        
    saveName = os.path.join(saveDir, plotName.replace("/", "_"))
    saveName = saveName.replace("(", "_")
    saveName = saveName.replace(")", "")
    saveName = saveName.replace(" ", "")

    # For-loop: All save formats                                                                                                                                                                            
    for i, ext in enumerate(saveFormats):
        saveNameURL = saveName + ext
        saveNameURL = aux.convertToURL(saveNameURL, opts.url)
        Verbose(saveNameURL, i==0)
        plot.saveAs(saveName, formats=saveFormats)
    return

#================================================================================================ 
# Main
#================================================================================================ 
if __name__ == "__main__":
    '''
    https://docs.python.org/3/library/argparse.html
 
    name or flags...: Either a name or a list of option strings, e.g. foo or -f, --foo.
    action..........: The basic type of action to be taken when this argument is encountered at the command line.
    nargs...........: The number of command-line arguments that should be consumed.
    const...........: A constant value required by some action and nargs selections.
    default.........: The value produced if the argument is absent from the command line.
    type............: The type to which the command-line argument should be converted.
    choices.........: A container of the allowable values for the argument.
    required........: Whether or not the command-line option may be omitted (optionals only).
    help............: A brief description of what the argument does.
    metavar.........: A name for the argument in usage messages.
    dest............: The name of the attribute to be added to the object returned by parse_args().
    '''
    
    # Default Settings
    ANALYSISNAME = "TopBDTTaggerMistagRate"
    SEARCHMODE   = "80to1000"
    DATAERA      = "Run2016"
    OPTMODE      = ""
    BATCHMODE    = True
    PRECISION    = 3
    #SIGNALMASS   = [300, 500, 1000]
    SIGNALMASS   = []
    INTLUMI      = -1.0
    SUBCOUNTERS  = False
    LATEX        = False
    URL          = False
    NOERROR      = True
    SAVEDIR      = None #"/publicweb/%s/%s/%s" % (getpass.getuser()[0], getpass.getuser(), ANALYSISNAME)
    VERBOSE      = False
    HISTOLEVEL   = "Vital" # 'Vital' , 'Informative' , 'Debug'
    NORMALISE    = False
    FOLDER       = "" #"topSelection_" #"ForDataDrivenCtrlPlots" #"topologySelection_"
    MVACUT       = "Eff"

    # Define the available script options
    parser = OptionParser(usage="Usage: %prog [options]")

    parser.add_option("-m", "--mcrab", dest="mcrab", action="store", 
                      help="Path to the multicrab directory for input")

    parser.add_option("-o", "--optMode", dest="optMode", type="string", default=OPTMODE, 
                      help="The optimization mode when analysis variation is enabled  [default: %s]" % OPTMODE)

    parser.add_option("-b", "--batchMode", dest="batchMode", action="store_false", default=BATCHMODE, 
                      help="Enables batch mode (canvas creation does NOT generate a window) [default: %s]" % BATCHMODE)

    parser.add_option("--analysisName", dest="analysisName", type="string", default=ANALYSISNAME,
                      help="Override default analysisName [default: %s]" % ANALYSISNAME)

    parser.add_option("--intLumi", dest="intLumi", type=float, default=INTLUMI,
                      help="Override the integrated lumi [default: %s]" % INTLUMI)

    parser.add_option("--searchMode", dest="searchMode", type="string", default=SEARCHMODE,
                      help="Override default searchMode [default: %s]" % SEARCHMODE)

    parser.add_option("--dataEra", dest="dataEra", type="string", default=DATAERA, 
                      help="Override default dataEra [default: %s]" % DATAERA)

    #parser.add_option("--signalMass", dest="signalMass", type=float, default=SIGNALMASS, 
                      #help="Mass value of signal to use [default: %s]" % SIGNALMASS)

    parser.add_option("--saveDir", dest="saveDir", type="string", default=SAVEDIR, 
                      help="Directory where all pltos will be saved [default: %s]" % SAVEDIR)

    parser.add_option("--url", dest="url", action="store_true", default=URL, 
                      help="Don't print the actual save path the histogram is saved, but print the URL instead [default: %s]" % URL)
    
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=VERBOSE, 
                      help="Enables verbose mode (for debugging purposes) [default: %s]" % VERBOSE)

    parser.add_option("--histoLevel", dest="histoLevel", action="store", default = HISTOLEVEL,
                      help="Histogram ambient level (default: %s)" % (HISTOLEVEL))

    parser.add_option("-i", "--includeOnlyTasks", dest="includeOnlyTasks", action="store", 
                      help="List of datasets in mcrab to include")

    parser.add_option("-e", "--excludeTasks", dest="excludeTasks", action="store", 
                      help="List of datasets in mcrab to exclude")

    parser.add_option("-n", "--normaliseToOne", dest="normaliseToOne", action="store_true", 
                      help="Normalise the histograms to one? [default: %s]" % (NORMALISE) )

    parser.add_option("--folder", dest="folder", type="string", default = FOLDER,
                      help="ROOT file folder under which all histograms to be plotted are located [default: %s]" % (FOLDER) )

    parser.add_option("--MVAcut", dest="MVAcut", type="string", default = MVACUT,
                      help="Save plots to directory in respect of the MVA cut value [default: %s]" % (MVACUT) )

    (opts, parseArgs) = parser.parse_args()

    # Require at least two arguments (script-name, path to multicrab)
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    if opts.mcrab == None:
        Print("Not enough arguments passed to script execution. Printing docstring & EXIT.")
        parser.print_help()
        #print __doc__
        sys.exit(1)

    if opts.saveDir == None:
        opts.saveDir = aux.getSaveDirPath(opts.mcrab, prefix="", postfix="")

    # Sanity check
    allowedMass = [180, 200, 220, 250, 300, 350, 400, 500, 800, 1000, 2000, 3000]
    signalMass = []
    for m in sorted(SIGNALMASS, reverse=True):
        signalMass.append("ChargedHiggs_HplusTB_HplusToTB_M_%.f" % m)

    # Call the main function
    main(opts, signalMass)

    if not opts.batchMode:
        raw_input("=== plot_Efficiency.py: Press any key to quit ROOT ...")
