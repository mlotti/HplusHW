#!/usr/bin/env python
'''
DESCRIPTION:


USAGE:
./plot_Efficiency_BDT.py -m <pseudo_mcrab> [opts]


EXAMPLES:
./plot_Efficiency_BDT.py -m MyHplusAnalysis_180202_fullSignalQCDtt --folder topbdtSelection_ --url


LAST USED:
./plot_Efficiency_BDT.py -m /uscms_data/d3/skonstan/workspace/pseudo-multicrab/TopRecoAnalysis/BDTcutComparisonPlots_BjetPt40_MassCut400/TopRecoAnalysis_180320_BDT40/ --folder topbdtSelection_ 


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
import array

import ROOT
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
def GetListOfQCDatasets():
    Verbose("Getting list of QCD datasets")
    return [#"QCD_bEnriched_HT200to300",
            #"QCD_bEnriched_HT300to500",
            #"QCD_bEnriched_HT500to700",
            #"QCD_bEnriched_HT700to1000",
            "QCD_HT1000to1500",
            #"QCD_bEnriched_HT1000to1500",
            #"QCD_bEnriched_HT1500to2000",
            #"QCD_bEnriched_HT2000toInf",
            "QCD_HT1500to2000_ext1",
            "QCD_HT2000toInf",
            "QCD_HT2000toInf_ext1",
            "QCD_HT200to300",
            "QCD_HT200to300_ext1",
            "QCD_HT1000to1500_ext1",
            "QCD_HT100to200",
            "QCD_HT1500to2000",
            "QCD_HT500to700_ext1",
            "QCD_HT50to100",
            "QCD_HT700to1000",
            "QCD_HT700to1000_ext1",
            "QCD_HT300to500",
            "QCD_HT300to500_ext1",
            "QCD_HT500to700"
            ]


def GetListOfEwkDatasets():
    Verbose("Getting list of EWK datasets")
    return ["TT", "WJetsToQQ_HT_600ToInf", "DYJetsToQQHT", "SingleTop", "TTWJetsToQQ", "TTZToQQ", "Diboson", "TTTT"]


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
    

def GetDatasetsFromDir_second(opts, useMcrab):
    Verbose("Getting datasets")
    
    if (not opts.includeOnlyTasks and not opts.excludeTasks):
        datasets = dataset.getDatasetsFromMulticrabDirs([useMcrab],
                                                        dataEra=opts.dataEra,
                                                        searchMode=opts.searchMode, 
                                                        analysisName=opts.analysisName,
                                                        optimizationMode=opts.optMode)
    elif (opts.includeOnlyTasks):
        datasets = dataset.getDatasetsFromMulticrabDirs([useMcrab],
                                                        dataEra=opts.dataEra,
                                                        searchMode=opts.searchMode,
                                                        analysisName=opts.analysisName,
                                                        includeOnlyTasks=opts.includeOnlyTasks,
                                                        optimizationMode=opts.optMode)
    elif (opts.excludeTasks):
        datasets = dataset.getDatasetsFromMulticrabDirs([useMcrab],
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
    kwargs     = {
        "xlabel"           : "x-axis",
        "ylabel"           : "Efficiency / ", #/ %.1f ",
        # "rebinX"           : 1,
        "ratioYlabel"      : "Ratio",
        "ratio"            : False,
        "ratioInvert"      : False,
        "stackMCHistograms": False,
        "addMCUncertainty" : False,
        "addLuminosityText": False,
        "addCmsText"       : True,
        "cmsExtraText"     : "Preliminary",
        #"opts"             : {"ymin": 0.0, "ymax": 1.09},
        "opts"             : {"ymin": 0.0, "ymaxfactor": 1.1},
        "opts2"            : {"ymin": 0.6, "ymax": 1.4},
        "log"              : False,
#        "moveLegend"       : {"dx": -0.08, "dy": -0.01, "dh": -0.08},
        "moveLegend"       : {"dx": -0.05, "dy": -0.005, "dh": -0.1},
#        "moveLegend"       : {"dx": -0.57, "dy": -0.007, "dh": -0.18},
        "cutBoxY"          : {"cutValue": 1.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True, "mainCanvas": True, "ratioCanvas": False}
        }

    if "pt" in h:
        units   = "GeV/c"
        xlabel  = "candidate p_{T} (%s)" % (units)
        #myBins  = [0, 100, 150, 200, 250, 300, 400, 500, 800]
        myBins  = [0, 100, 150, 200, 300, 400, 500, 600, 800]
        #myBins  = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800]
        kwargs["cutBox"] = {"cutValue": 100.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
        
        if "topquark" in h:
            #kwargs["moveLegend"] = {"dx": -0.55, "dy": -0.55, "dh": -0.08}
            kwargs["moveLegend"] = {"dx": -0.05, "dy": -0.59, "dh": -0.11}
            xlabel = "generated top p_{T} (%s)" % (units)
        if 0:
            ROOT.gStyle.SetNdivisions(6 + 100*5 + 10000*2, "X")

        if "fake" in h:
            xlabel = "candidate p_{T} (%s)" % (units)
            kwargs["ylabel"] = "Misidentification rate / " #+ units

        if "event" in h:
            #kwargs["moveLegend"] = {"dx": -0.55, "dy": -0.55, "dh": -0.08}
            kwargs["moveLegend"] = {"dx": -0.05, "dy": -0.57, "dh": -0.11}
            myBins  = [0, 100, 200, 300, 400, 500, 800]
        if 0:
            ROOT.gStyle.SetNdivisions(6 + 100*5 + 10000*2, "X")

    kwargs["xlabel"]  = xlabel
    kwargs["ylabel"] += units
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

        dir = opts.mcrab.replace("_BDT85", "_BDT")
        print dir

        datasetsMgr30 = GetDatasetsFromDir_second(opts, dir+"30")
        datasetsMgr30.updateNAllEventsToPUWeighted()
        datasetsMgr30.loadLuminosities() # from lumi.json                                                                                      

        datasetsMgr40 = GetDatasetsFromDir_second(opts, dir+"40")
        datasetsMgr40.updateNAllEventsToPUWeighted()
        datasetsMgr40.loadLuminosities() # from lumi.json                                                                                                                           

        datasetsMgr50 = GetDatasetsFromDir_second(opts, dir+"50")
        datasetsMgr50.updateNAllEventsToPUWeighted()
        datasetsMgr50.loadLuminosities() # from lumi.json                                                                                                                           
 
        datasetsMgr60 = GetDatasetsFromDir_second(opts, dir+"60")
        datasetsMgr60.updateNAllEventsToPUWeighted()
        datasetsMgr60.loadLuminosities() # from lumi.json                                                                                                                               

        datasetsMgr70 = GetDatasetsFromDir_second(opts, dir+"70")
        datasetsMgr70.updateNAllEventsToPUWeighted()
        datasetsMgr70.loadLuminosities() # from lumi.json                                                                                                                               

        datasetsMgr80 = GetDatasetsFromDir_second(opts, dir+"80")
        datasetsMgr80.updateNAllEventsToPUWeighted()
        datasetsMgr80.loadLuminosities() # from lumi.json                                                                                                                               

        datasetsMgr90 = GetDatasetsFromDir_second(opts, dir+"90")
        datasetsMgr90.updateNAllEventsToPUWeighted()
        datasetsMgr90.loadLuminosities() # from lumi.json                                                                                                                               

        datasetsMgr95 = GetDatasetsFromDir_second(opts, dir+"95")
        datasetsMgr95.updateNAllEventsToPUWeighted()
        datasetsMgr95.loadLuminosities() # from lumi.json             

        if opts.verbose:
            datasetsMgr.PrintCrossSections()
            datasetsMgr.PrintLuminosities()

        # Set/Overwrite cross-sections
        for datasetsMgr_ in [datasetsMgr, datasetsMgr30, datasetsMgr40, datasetsMgr50, datasetsMgr60, datasetsMgr70, datasetsMgr80, datasetsMgr90, datasetsMgr95]:
            for d in datasetsMgr_.getAllDatasets():
                if "ChargedHiggs" in d.getName():
                    datasetsMgr_.getDataset(d.getName()).setCrossSection(1.0)
                    #datasetsMgr.getDataset(d.getName()).setCrossSection(1.0)
                    #datasetsMgr50.getDataset(d.getName()).setCrossSection(1.0)
                    #datasetsMgr60.getDataset(d.getName()).setCrossSection(1.0)
                    #datasetsMgr70.getDataset(d.getName()).setCrossSection(1.0)
                    #datasetsMgr80.getDataset(d.getName()).setCrossSection(1.0)
                    #datasetsMgr90.getDataset(d.getName()).setCrossSection(1.0)
                    #datasetsMgr95.getDataset(d.getName()).setCrossSection(1.0)

        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        #plots.mergeRenameReorderForDataMC(datasetsMgr) 
        
        # Print dataset information before removing anything?
        if 0:
            datasetsMgr.PrintInfo()

        # Determine integrated Lumi before removing data
        if "Data" in datasetsMgr.getAllDatasetNames():
            intLumi = datasetsMgr.getDataset("Data").getLuminosity()
        else:
            intLumi = 35920
        # Remove datasets
        filterKeys = ["Data", "TTZToQQ", "TTWJets", "TTTT"]
        #filterKeys = ["Data", "TTZToQQ", "TTWJets", "TTTT"]
        for key in filterKeys:
            datasetsMgr.remove(filter(lambda name: key in name, datasetsMgr.getAllDatasetNames()))
            datasetsMgr30.remove(filter(lambda name: key in name, datasetsMgr30.getAllDatasetNames()))
            datasetsMgr40.remove(filter(lambda name: key in name, datasetsMgr40.getAllDatasetNames()))
            datasetsMgr50.remove(filter(lambda name: key in name, datasetsMgr50.getAllDatasetNames()))
            datasetsMgr60.remove(filter(lambda name: key in name, datasetsMgr60.getAllDatasetNames()))
            datasetsMgr70.remove(filter(lambda name: key in name, datasetsMgr70.getAllDatasetNames()))
            datasetsMgr80.remove(filter(lambda name: key in name, datasetsMgr80.getAllDatasetNames()))
            datasetsMgr90.remove(filter(lambda name: key in name, datasetsMgr90.getAllDatasetNames()))
            datasetsMgr95.remove(filter(lambda name: key in name, datasetsMgr95.getAllDatasetNames()))
        # Re-order datasets
        datasetOrder = []
        for d in datasetsMgr.getAllDatasets():
            if "M_" in d.getName():
                if d not in signalMass:
                    continue
            datasetOrder.append(d.getName())
            
        # Append signal datasets
        for m in signalMass:
            datasetOrder.insert(0, m)
        datasetsMgr.selectAndReorder(datasetOrder)
        datasetsMgr30.selectAndReorder(datasetOrder)
        datasetsMgr40.selectAndReorder(datasetOrder)
        datasetsMgr50.selectAndReorder(datasetOrder)
        datasetsMgr60.selectAndReorder(datasetOrder)
        datasetsMgr70.selectAndReorder(datasetOrder)
        datasetsMgr80.selectAndReorder(datasetOrder)
        datasetsMgr90.selectAndReorder(datasetOrder)
        datasetsMgr95.selectAndReorder(datasetOrder)

        # Print dataset information
        datasetsMgr.PrintInfo()

        # Define the mapping histograms in numerator->denominator pairs

        Numerators = ["AllTopQuarkPt_MatchedBDT",
                      "AllTopQuarkPt_Matched",
                      "EventTrijetPt2T_MatchedBDT",
                      "EventTrijetPt2T_MatchedBDT",
                      "EventTrijetPt2T_MatchedBDT",
                      "AllTopQuarkPt_MatchedBDT",
                      "SelectedTrijetsPt_BjetPassCSVdisc_afterCuts",
                      "TrijetFakePt_BDT",
                      ]
        Denominators = ["AllTopQuarkPt_Matched",
                        "TopQuarkPt",
                        "EventTrijetPt2T_BDT",
                        "EventTrijetPt2T_Matched",
                        "EventTrijetPt2T",
                        "TopQuarkPt",
                        "SelectedTrijetsPt_afterCuts",
                        "TrijetFakePt",
                        ]

        
        if 1:
            datasetsMgr.merge("QCD", GetListOfQCDatasets())
            datasetsMgr30.merge("QCD", GetListOfQCDatasets())
            datasetsMgr40.merge("QCD", GetListOfQCDatasets())
            datasetsMgr50.merge("QCD", GetListOfQCDatasets())
            datasetsMgr60.merge("QCD", GetListOfQCDatasets())
            datasetsMgr70.merge("QCD", GetListOfQCDatasets())
            datasetsMgr80.merge("QCD", GetListOfQCDatasets())
            datasetsMgr90.merge("QCD", GetListOfQCDatasets())
            datasetsMgr95.merge("QCD", GetListOfQCDatasets())
            
            plots._plotStyles["QCD"] = styles.getQCDLineStyle()
        #Background1_Dataset = datasetsMgr.getDataset("QCD")

        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        plots.mergeRenameReorderForDataMC(datasetsMgr) 
        
        # For-loop: All numerator-denominator pairs
        for i in range(len(Numerators)):
            numerator = os.path.join(opts.folder, Numerators[i])
            denominator = os.path.join(opts.folder, Denominators[i])
            PlotEfficiency_comparison(datasetsMgr, datasetsMgr30, datasetsMgr40, datasetsMgr50, datasetsMgr60, datasetsMgr70, datasetsMgr80, datasetsMgr90, datasetsMgr95, numerator, denominator, intLumi)
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
    index   = 0
    _kwargs = GetHistoKwargs(numPath, opts)        

    # For-loop: All datasets
    for dataset in datasetsMgr.getAllDatasets():
        if "Fake" in numPath and "TT" in dataset.getName():
            continue
        # Get the histograms
        #num = dataset.getDatasetRootHisto(numPath).getHistogram()
        #den = dataset.getDatasetRootHisto(denPath).getHistogram()

        n = dataset.getDatasetRootHisto(numPath)
        n.normalizeToLuminosity(intLumi)                                                                                                                       
        num = n.getHistogram()
        d = dataset.getDatasetRootHisto(denPath)
        d.normalizeToLuminosity(intLumi)                                                                                                                       
        den = d.getHistogram()

        
        if "binList" in _kwargs:
            xBins   = _kwargs["binList"]
            nx      = len(xBins)-1
            num     = num.Rebin(nx, "", xBins)
            den     = den.Rebin(nx, "", xBins)

        # Sanity checks
        if den.GetEntries() == 0 or num.GetEntries() == 0:
            continue
        if num.GetEntries() > den.GetEntries():
            continue

        # Remove negative bins and ensure numerator bin <= denominator bin
        CheckNegatives(num, den, True)
        # RemoveNegatives(num)
        # RemoveNegatives(den)
                
        # Sanity check (Histograms are valid and consistent) - Always false!
        # if not ROOT.TEfficiency.CheckConsistency(num, den):
        #    continue

        # Create Efficiency plots with Clopper-Pearson stats
        eff = ROOT.TEfficiency(num, den) # fixme: investigate warnings
        eff.SetStatisticOption(ROOT.TEfficiency.kFCP) #
        # Set the weights - Why is this needed?
        if 0:
            weight = 1
            if dataset.isMC():
                weight = dataset.getCrossSection()
                eff.SetWeight(weight)
                
        # Convert to TGraph
        eff = convert2TGraph(eff)
        # Apply default style (according to dataset name)
        plots._plotStyles[dataset.getName()].apply(eff)

        # Append in list
        myList.append(histograms.HistoGraph(eff, plots._legendLabels[dataset.getName()], "lp", "P"))
            
    # Define save name
    saveName = "Eff_" + numPath.split("/")[-1] + "Over" + denPath.split("/")[-1]

    # Plot the efficiency
    p = plots.PlotBase(datasetRootHistos=myList, saveFormats=[])
    plots.drawPlot(p, saveName, **_kwargs)


    # Save plot in all formats
    savePath = os.path.join(opts.saveDir, numPath.split("/")[0], opts.optMode)
    #savePath = os.path.join(opts.saveDir, numPath.split("/")[0], opts.optMode)
    save_path = savePath + opts.MVAcut
    SavePlot(p, saveName, save_path, saveFormats = [".png", ".pdf", ".C"])
    return



def PlotEfficiency_comparison(datasetsMgr,  datasetsMgr30, datasetsMgr40, datasetsMgr50, datasetsMgr60, datasetsMgr70, datasetsMgr80, datasetsMgr90, datasetsMgr95, numPath, denPath, intLumi):
  
    # Definitions
    myList  = []
    index   = 0
    _kwargs = GetHistoKwargs(numPath, opts)        

    # For-loop: All datasets
    #for dataset in datasetsMgr.getAllDatasets():
    if 1:
        #if "Fake" in numPath:
        #    return
        dataset = datasetsMgr.getDataset("TT")
        dataset30 = datasetsMgr30.getDataset("TT")
        dataset40 = datasetsMgr40.getDataset("TT")
        dataset50 = datasetsMgr50.getDataset("TT")
        dataset60 = datasetsMgr60.getDataset("TT")
        dataset70 = datasetsMgr70.getDataset("TT")
        dataset80 = datasetsMgr80.getDataset("TT")
        dataset90 = datasetsMgr90.getDataset("TT")
        dataset95 = datasetsMgr95.getDataset("TT")

        
        if "Fake" in numPath:
            dataset = datasetsMgr.getDataset("QCD")
            dataset30 = datasetsMgr30.getDataset("QCD")
            dataset40 = datasetsMgr40.getDataset("QCD")
            dataset50 = datasetsMgr50.getDataset("QCD")
            dataset60 = datasetsMgr60.getDataset("QCD")
            dataset70 = datasetsMgr70.getDataset("QCD")
            dataset80 = datasetsMgr80.getDataset("QCD")
            dataset90 = datasetsMgr90.getDataset("QCD")
            dataset95 = datasetsMgr95.getDataset("QCD")

        legend = "BDTG > 0.85"
        legend30 = "BDTG > 0.30"
        legend40 = "BDTG > 0.40"
        legend50 = "BDTG > 0.50"
        legend60 = "BDTG > 0.60"
        legend70 = "BDTG > 0.70"
        legend80 = "BDTG > 0.80"
        legend90 = "BDTG > 0.90"
        legend95 = "BDTG > 0.95"

        styleDef = styles.ttStyle
        style30 = styles.ttStyle #styles.signalStyleHToTB180 
        style40 = styles.signalStyleHToTB500 #800
        style50 = styles.signalStyleHToTB500
        style60 = styles.signalStyleHToTB1000
        style70 = styles.signalStyleHToTB2000
        style80 = styles.signalStyleHToTB300
        style90 = styles.signalStyleHToTB3000
        style95 = styles.signalStyleHToTB200
        
        n = dataset30.getDatasetRootHisto(numPath)
        n.normalizeToLuminosity(intLumi)
        num30 = n.getHistogram()  
        d = dataset30.getDatasetRootHisto(denPath) 
        d.normalizeToLuminosity(intLumi)
        den30 = d.getHistogram()    
        #=========================================                                                 
        n = dataset40.getDatasetRootHisto(numPath)
        n.normalizeToLuminosity(intLumi)
        num40 = n.getHistogram()  
        d = dataset40.getDatasetRootHisto(denPath) 
        d.normalizeToLuminosity(intLumi)
        den40 = d.getHistogram()    
        #=========================================                                                 
        n = dataset.getDatasetRootHisto(numPath)
        n.normalizeToLuminosity(intLumi)
        num = n.getHistogram()  
        d = dataset.getDatasetRootHisto(denPath) 
        d.normalizeToLuminosity(intLumi)
        den = d.getHistogram()    
        #=========================================                                                                 
        n = dataset50.getDatasetRootHisto(numPath)
        n.normalizeToLuminosity(intLumi)
        num50 = n.getHistogram()  
        d = dataset50.getDatasetRootHisto(denPath) 
        d.normalizeToLuminosity(intLumi)
        den50 = d.getHistogram()    
        #=========================================                                                                                                                                   
        n = dataset60.getDatasetRootHisto(numPath)
        n.normalizeToLuminosity(intLumi)
        num60 = n.getHistogram()
        d = dataset60.getDatasetRootHisto(denPath)                                                                                                           
        d.normalizeToLuminosity(intLumi)
        den60 = d.getHistogram()
        #=========================================                                                                                                                 
        n = dataset70.getDatasetRootHisto(numPath)
        n.normalizeToLuminosity(intLumi)
        num70 = n.getHistogram()
        d = dataset70.getDatasetRootHisto(denPath)
        d.normalizeToLuminosity(intLumi)
        den70 = d.getHistogram()
        #=========================================                                                                                                                                    
        n = dataset80.getDatasetRootHisto(numPath)
        n.normalizeToLuminosity(intLumi)                                                                                                                 
        num80 = n.getHistogram()                   
        d = dataset80.getDatasetRootHisto(denPath)
        d.normalizeToLuminosity(intLumi)
        den80 = d.getHistogram()
        #=========================================                                                                                                                                   
        n = dataset90.getDatasetRootHisto(numPath)
        n.normalizeToLuminosity(intLumi)
        num90 = n.getHistogram()
        d = dataset90.getDatasetRootHisto(denPath)
        d.normalizeToLuminosity(intLumi)
        den90 = d.getHistogram() 
        #=========================================                                                                                                                                   
        n = dataset95.getDatasetRootHisto(numPath)
        n.normalizeToLuminosity(intLumi)
        num95 = n.getHistogram()
        d = dataset95.getDatasetRootHisto(denPath)
        d.normalizeToLuminosity(intLumi)
        den95 = d.getHistogram() 
        



        #num = dataset.getDatasetRootHisto(numPath).getHistogram()                
        #den = dataset.getDatasetRootHisto(denPath).getHistogram()  
        #num50 = dataset50.getDatasetRootHisto(numPath).getHistogram()                       
        #den50 = dataset50.getDatasetRootHisto(denPath).getHistogram()  
        #num60 = dataset60.getDatasetRootHisto(numPath).getHistogram()                       
        #den60 = dataset60.getDatasetRootHisto(denPath).getHistogram()  
        #num70 = dataset70.getDatasetRootHisto(numPath).getHistogram()                       
        #den70 = dataset70.getDatasetRootHisto(denPath).getHistogram()  
        #num80 = dataset80.getDatasetRootHisto(numPath).getHistogram()                       
        #den80 = dataset80.getDatasetRootHisto(denPath).getHistogram()  
        #num90 = dataset90.getDatasetRootHisto(numPath).getHistogram()                       
        #den90 = dataset90.getDatasetRootHisto(denPath).getHistogram()  
        #num95 = dataset95.getDatasetRootHisto(numPath).getHistogram()                       
        #den95 = dataset95.getDatasetRootHisto(denPath).getHistogram()  



        if "binList" in _kwargs:
            xBins   = _kwargs["binList"]
            nx      = len(xBins)-1
            num     = num.Rebin(nx, "", xBins)
            den     = den.Rebin(nx, "", xBins)
            num30     = num30.Rebin(nx, "", xBins)
            den30     = den30.Rebin(nx, "", xBins)
            num40     = num40.Rebin(nx, "", xBins)
            den40     = den40.Rebin(nx, "", xBins)
            num50     = num50.Rebin(nx, "", xBins)
            den50     = den50.Rebin(nx, "", xBins)
            num60     = num60.Rebin(nx, "", xBins)
            den60     = den60.Rebin(nx, "", xBins)
            num70     = num70.Rebin(nx, "", xBins)
            den70     = den70.Rebin(nx, "", xBins)
            num80     = num80.Rebin(nx, "", xBins)
            den80     = den80.Rebin(nx, "", xBins)
            num90     = num90.Rebin(nx, "", xBins)
            den90     = den90.Rebin(nx, "", xBins)
            num95     = num95.Rebin(nx, "", xBins)
            den95     = den95.Rebin(nx, "", xBins)


        # Sanity checks
        if den.GetEntries() == 0 or num.GetEntries() == 0:
        #    continue
            return
        if num.GetEntries() > den.GetEntries():
        #    continue
            return


        # Remove negative bins and ensure numerator bin <= denominator bin
        #CheckNegatives(num, den, True)
        #CheckNegatives(num50, den50, True)
        #CheckNegatives(num60, den60, True)
        #CheckNegatives(num70, den70, True)
        #CheckNegatives(num80, den80, True)
        #CheckNegatives(num90, den90, True)
        #CheckNegatives(num95, den95, True)
        # RemoveNegatives(num)
        # RemoveNegatives(den)
                
        # Sanity check (Histograms are valid and consistent) - Always false!
        # if not ROOT.TEfficiency.CheckConsistency(num, den):
        #    continue

        # Create Efficiency plots with Clopper-Pearson stats
        eff85 = ROOT.TEfficiency(num, den) # fixme: investigate warnings
        eff85.SetStatisticOption(ROOT.TEfficiency.kFCP) #

        eff30 = ROOT.TEfficiency(num30, den30) # fixme: investigate warnings
        eff30.SetStatisticOption(ROOT.TEfficiency.kFCP) #

        eff40 = ROOT.TEfficiency(num40, den40) # fixme: investigate warnings
        eff40.SetStatisticOption(ROOT.TEfficiency.kFCP) #

        eff50 = ROOT.TEfficiency(num50, den50) # fixme: investigate warnings
        eff50.SetStatisticOption(ROOT.TEfficiency.kFCP) #

        eff60 = ROOT.TEfficiency(num60, den60) # fixme: investigate warnings
        eff60.SetStatisticOption(ROOT.TEfficiency.kFCP) #

        eff70 = ROOT.TEfficiency(num70, den70) # fixme: investigate warnings
        eff70.SetStatisticOption(ROOT.TEfficiency.kFCP) #

        eff80 = ROOT.TEfficiency(num80, den80) # fixme: investigate warnings
        eff80.SetStatisticOption(ROOT.TEfficiency.kFCP) #

        eff90 = ROOT.TEfficiency(num90, den90) # fixme: investigate warnings
        eff90.SetStatisticOption(ROOT.TEfficiency.kFCP) #

        eff95 = ROOT.TEfficiency(num95, den95) # fixme: investigate warnings
        eff95.SetStatisticOption(ROOT.TEfficiency.kFCP) #

        eff30 = convert2TGraph(eff30)
        eff40 = convert2TGraph(eff40)
        eff50 = convert2TGraph(eff50)
        eff60 = convert2TGraph(eff60)
        eff70 = convert2TGraph(eff70)
        eff80 = convert2TGraph(eff80)
        eff85 = convert2TGraph(eff85)
        eff90 = convert2TGraph(eff90)
        eff95 = convert2TGraph(eff95)
        # Apply default style (according to dataset name)
        #plots._plotStyles[dataset.getName()].apply(eff)
        styleDef.apply(eff85)
        style30.apply(eff30)
        style40.apply(eff40)
        style50.apply(eff50)
        style60.apply(eff60)
        style70.apply(eff70)
        style80.apply(eff80)
        style90.apply(eff90)
        style95.apply(eff95)


        eff50.SetLineStyle(ROOT.kSolid)
        eff50.SetLineWidth(2)
        eff30.SetLineWidth(2)
        eff40.SetLineWidth(2)
        eff60.SetLineWidth(2)
        eff70.SetLineWidth(2)
        eff80.SetLineWidth(2)
        eff85.SetLineWidth(2)
        eff90.SetLineWidth(2)
        eff95.SetLineWidth(2)

        #eff30.SetLineColor(1)

        eff50.SetLineStyle(ROOT.kSolid)
        eff30.SetLineStyle(ROOT.kSolid)
        eff40.SetLineStyle(ROOT.kSolid)
        eff60.SetLineStyle(ROOT.kSolid)
        eff70.SetLineStyle(ROOT.kSolid)
        eff80.SetLineStyle(ROOT.kSolid)
        eff85.SetLineStyle(ROOT.kSolid)
        eff90.SetLineStyle(ROOT.kSolid)
        eff95.SetLineStyle(ROOT.kSolid)


        eff30.SetMarkerStyle(ROOT.kFullTriangleUp)
        eff40.SetMarkerStyle(ROOT.kFullTriangleUp)
        eff50.SetMarkerStyle(ROOT.kFullTriangleUp)
        eff60.SetMarkerStyle(ROOT.kFullTriangleUp)
        eff70.SetMarkerStyle(ROOT.kFullTriangleUp)
        eff80.SetMarkerStyle(ROOT.kFullTriangleUp)
        eff85.SetMarkerStyle(ROOT.kFullTriangleUp)
        eff90.SetMarkerStyle(ROOT.kFullTriangleUp)
        eff95.SetMarkerStyle(ROOT.kFullTriangleUp)
        
        eff30.SetMarkerSize(1.2)
        eff40.SetMarkerSize(1.2)
        eff50.SetMarkerSize(1.2)
        eff60.SetMarkerSize(1.2)
        eff70.SetMarkerSize(1.2)
        eff80.SetMarkerSize(1.2)
        eff85.SetMarkerSize(1.2)
        eff90.SetMarkerSize(1.2)
        eff95.SetMarkerSize(1.2)

        # Append in list
#        myList.append(histograms.HistoGraph(eff, plots._legendLabels["Default"], "lp", "P"))
        myList.append(histograms.HistoGraph(eff30, legend30, "lp", "P"))
        myList.append(histograms.HistoGraph(eff40, legend40, "lp", "P"))
        #myList.append(histograms.HistoGraph(eff50, legend50, "lp", "P"))
        myList.append(histograms.HistoGraph(eff60, legend60, "lp", "P"))
        #myList.append(histograms.HistoGraph(eff70, legend70, "lp", "P"))
        myList.append(histograms.HistoGraph(eff80, legend80, "lp", "P"))
        #myList.append(histograms.HistoGraph(eff85, legend, "lp", "P"))
        myList.append(histograms.HistoGraph(eff90, legend90, "lp", "P"))
        #myList.append(histograms.HistoGraph(eff95, legend95, "lp", "P"))
        
        
    # Define save name
    saveName = "Eff_" + numPath.split("/")[-1] + "Over" + denPath.split("/")[-1]

    # Plot the efficiency
    p = plots.PlotBase(datasetRootHistos=myList, saveFormats=[])
    plots.drawPlot(p, saveName, **_kwargs)

    leg = ROOT.TLegend(0.2, 0.8, 0.81, 0.87)
    leg.SetFillStyle( 0)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    #{"dx": -0.55, "dy": -0.55, "dh": -0.08}
    leg.SetHeader("t#bar{t}")    
    if "Fake" in numPath:
        leg.SetHeader("QCD")

    leg.Draw()
    #moveLegend       =  {"dx": -0.0, "dy": +0.0, "dh": +0.1}
    #moveLegend       = {"dx": -0.1, "dy": +0.0, "dh": +0.1}
    #p.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))


    # Save plot in all formats
    savePath = os.path.join(opts.saveDir, "HplusMasses", numPath.split("/")[0], opts.optMode)
    #savePath = os.path.join(opts.saveDir, numPath.split("/")[0], opts.optMode)
    save_path = savePath + opts.MVAcut
    SavePlot(p, saveName, save_path, saveFormats = [".png", ".pdf", ".C"])
    return



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


def SavePlot(plot, saveName, saveDir, saveFormats = [".png"]):
    # Check that path exists
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)
        
    savePath = os.path.join(saveDir, saveName)

    # For-loop: All save formats
    for i, ext in enumerate(saveFormats):
        saveNameURL = savePath + ext
#        saveNameURL = saveNameURL.replace(opts.saveDir, "http://home.fnal.gov/~%s" % (getpass.getuser()))
        saveNameURL = saveNameURL.replace("/publicweb/%s/%s" % (getpass.getuser()[0], getpass.getuser()), "http://home.fnal.gov/~%s" % (getpass.getuser()))
        #SAVEDIR      = "/publicweb/%s/%s/%s" % (getpass.getuser()[0], getpass.getuser(), ANALYSISNAME)
        if opts.url:
            Print(saveNameURL, i==0)
        else:
            Print(savePath + ext, i==0)
        plot.saveAs(savePath, formats=saveFormats)
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
    ANALYSISNAME = "TopRecoAnalysis"
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
    SAVEDIR      = "/publicweb/%s/%s/%s" % (getpass.getuser()[0], getpass.getuser(), ANALYSISNAME)
    VERBOSE      = False
    HISTOLEVEL   = "Vital" # 'Vital' , 'Informative' , 'Debug'
    NORMALISE    = False
    FOLDER       = "topbdtSelection_"
    MVACUT       = "MVA"

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

    # Sanity check
    allowedMass = [180, 200, 220, 250, 300, 350, 400, 500, 800, 1000, 2000, 3000]
    signalMass = []
    for m in sorted(SIGNALMASS, reverse=True):
        signalMass.append("ChargedHiggs_HplusTB_HplusToTB_M_%.f" % m)

    # Call the main function
    main(opts, signalMass)

    if not opts.batchMode:
        raw_input("=== plot_Efficiency_BDT.py: Press any key to quit ROOT ...")
