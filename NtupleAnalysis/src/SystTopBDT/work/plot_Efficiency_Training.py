#!/usr/bin/env python
'''
DESCRIPTION:


USAGE:
./plot_Efficiency_Training.py -m <pseudo_mcrab> [opts]


EXAMPLES:
./plot_Efficiency_Training.py -m SystTopBDT_180517_TT_Training_DR0p3_DptOverPt0p32/ --folder SystTopBDT_Genuine --url

LAST USD:
./plot_Efficiency_Training.py -m SystTopBDT_180517_TT_Training_DR0p3_DptOverPt0p32/ --folder SystTopBDT_Genuine --url

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
    return ["QCD_bEnriched_HT200to300",
            "QCD_bEnriched_HT300to500",
            "QCD_bEnriched_HT500to700",
            "QCD_bEnriched_HT700to1000",
            "QCD_HT1000to1500",
            "QCD_bEnriched_HT1000to1500",
            "QCD_bEnriched_HT1500to2000",
            "QCD_bEnriched_HT2000toInf",
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
        "ratio"            : True,
        "ratioInvert"      : False,
        "stackMCHistograms": False,
        "addMCUncertainty" : False,
        "addLuminosityText": False,
        "addCmsText"       : True,
        "cmsExtraText"     : "Preliminary",
        #"opts"             : {"ymin": 0.0, "ymax": 1.09},
        "opts"             : {"ymin": 0.0, "ymaxfactor": 1.2},
        "opts2"            : {"ymin": 0.6, "ymax": 1.4},
        "log"              : False,
#        "moveLegend"       : {"dx": -0.08, "dy": -0.01, "dh": -0.08},
        #"moveLegend"       : {"dx": -0.05, "dy": -0.005, "dh": -0.08},
        "moveLegend"       : {"dx": -0.25, "dy": -0.725, "dh": -0.13},
#        "moveLegend"       : {"dx": -0.57, "dy": -0.007, "dh": -0.18},
        "cutBoxY"          : {"cutValue": 1.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True, "mainCanvas": True, "ratioCanvas": False}
        }

    if "pt" in h:
        units   = "GeV/c"
        xlabel  = "candidate p_{T} (%s)" % (units)
        #myBins  = [0, 100, 150, 200, 250, 300, 400, 500, 800]
        myBins  = [0, 100, 150, 200, 300, 400, 500, 600, 900]
        #myBins  = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800]
        kwargs["cutBox"] = {"cutValue": 100.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
        
        if "topquark" in h:
            #kwargs["moveLegend"] = {"dx": -0.55, "dy": -0.55, "dh": -0.08}
            kwargs["moveLegend"] = {"dx": -0.05, "dy": -0.55, "dh": -0.08}
            xlabel = "generated top p_{T} (%s)" % (units)
        if 1:
            ROOT.gStyle.SetNdivisions(6 + 100*5 + 10000*2, "X")

        if "fake" in h:
            xlabel = "candidate p_{T} (%s)" % (units)
            kwargs["ylabel"] = "Misidentification rate / " #+ units

        if "event" in h:
            #kwargs["moveLegend"] = {"dx": -0.55, "dy": -0.55, "dh": -0.08}
            kwargs["moveLegend"] = {"dx": -0.05, "dy": -0.55, "dh": -0.08}
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

        dir = opts.mcrab.replace("_DptOverPt0p32","")
        print dir

        datasetsMgr_DR = GetDatasetsFromDir_second(opts, dir)
        datasetsMgr_DR.updateNAllEventsToPUWeighted()
        datasetsMgr_DR.loadLuminosities() # from lumi.json                                                                                      

        if opts.verbose:
            datasetsMgr.PrintCrossSections()
            datasetsMgr.PrintLuminosities()

        # Set/Overwrite cross-sections
        for datasetsMgr_ in [datasetsMgr, datasetsMgr_DR]:
            for d in datasetsMgr_.getAllDatasets():
                if "ChargedHiggs" in d.getName():
                    datasetsMgr_.getDataset(d.getName()).setCrossSection(1.0)

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
            datasetsMgr_DR.remove(filter(lambda name: key in name, datasetsMgr_DR.getAllDatasetNames()))
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
        datasetsMgr_DR.selectAndReorder(datasetOrder)

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

        
        if 0:
            datasetsMgr.merge("QCD", GetListOfQCDatasets())
            datasetsMgr_DR.merge("QCD", GetListOfQCDatasets())
            
            plots._plotStyles["QCD"] = styles.getQCDLineStyle()
        #Background1_Dataset = datasetsMgr.getDataset("QCD")

        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        plots.mergeRenameReorderForDataMC(datasetsMgr) 
        
        # For-loop: All numerator-denominator pairs
        #for i in range(len(Numerators)):
        if 1:
            numerator = os.path.join(opts.folder, "AfterAllSelections_LeadingTrijet_Pt_SR")
            denominator = os.path.join(opts.folder, "AfterStandardSelections_LeadingTrijet_Pt_SR")
            #PlotEfficiency_comparison(datasetsMgr, datasetsMgr_DR, intLumi)
            PlotEfficiency_comparison(datasetsMgr, numerator, denominator,  datasetsMgr_DR, intLumi)
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
        #if "Fake" in numPath and "TT" in dataset.getName():
        #    continue
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
    savePath = os.path.join(opts.saveDir, "HplusMasses", numPath.split("/")[0], opts.optMode)
    #savePath = os.path.join(opts.saveDir, numPath.split("/")[0], opts.optMode)
    save_path = savePath + opts.MVAcut
    SavePlot(p, saveName, save_path, saveFormats = [".png", ".pdf", ".C"])
    return



def PlotEfficiency_comparison(datasetsMgr, numPath, denPath,  datasetsMgr_DR, intLumi):
  
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
        dataset_DR = datasetsMgr_DR.getDataset("TT")
        
        #if "Fake" in numPath:
        #    dataset = datasetsMgr.getDataset("QCD")
        #    dataset_DR = datasetsMgr_DR.getDataset("QCD")

        legend = "t#bar{t} (#Delta R < 0.30, #Delta p_{T} / p_{T} < 0.32)"
        legend_DR = "t#bar{t} (#Delta R < 0.30)"

        styleDef = styles.ttStyle
        style_DR = styles.signalStyleHToTB500 #800
        
        n = dataset_DR.getDatasetRootHisto(numPath)
        n.normalizeToLuminosity(intLumi)
        num_DR = n.getHistogram()  
        d = dataset_DR.getDatasetRootHisto(denPath) 
        d.normalizeToLuminosity(intLumi)
        den_DR = d.getHistogram()    
        #=========================================                                                 
        n = dataset.getDatasetRootHisto(numPath)
        n.normalizeToLuminosity(intLumi)
        num = n.getHistogram()  
        d = dataset.getDatasetRootHisto(denPath) 
        d.normalizeToLuminosity(intLumi)
        den = d.getHistogram()    
        #=========================================                                                 


        if "binList" in _kwargs:
            xBins   = _kwargs["binList"]
            nx      = len(xBins)-1
            num     = num.Rebin(nx, "", xBins)
            den     = den.Rebin(nx, "", xBins)
            num_DR     = num_DR.Rebin(nx, "", xBins)
            den_DR     = den_DR.Rebin(nx, "", xBins)

        for i in range(1, num.GetNbinsX()+1):
            nbin = num.GetBinContent(i)
            dbin = den.GetBinContent(i)
            nbin_DR = num_DR.GetBinContent(i)
            dbin_DR = den_DR.GetBinContent(i)
            eps = nbin/dbin
            eps_DR = nbin_DR/dbin_DR
            ratio_DR = eps/eps_DR
            if ratio_DR > 1:
                ratio_DR = 1/ratio_DR
            print "bin: ", i, "eps: ", round(eps,5) , "eps_DR: ", round(eps_DR,5)
            print "bin: ", i, "eps/eps_DR: ", (1.0 - round(ratio_DR, 3))*100

        # Sanity checks
        if den.GetEntries() == 0 or num.GetEntries() == 0:
        #    continue
            return
        if num.GetEntries() > den.GetEntries():
        #    continue
            return
                
        # Sanity check (Histograms are valid and consistent) - Always false!
        # if not ROOT.TEfficiency.CheckConsistency(num, den):
        #    continue

        # Create Efficiency plots with Clopper-Pearson stats
        eff = ROOT.TEfficiency(num, den) 
        eff.SetStatisticOption(ROOT.TEfficiency.kFCP) 

        eff_DR = ROOT.TEfficiency(num_DR, den_DR) 
        eff_DR.SetStatisticOption(ROOT.TEfficiency.kFCP) 


        eff = convert2TGraph(eff)
        eff_DR = convert2TGraph(eff_DR)

        # Apply default style (according to dataset name)
        #plots._plotStyles[dataset.getName()].apply(eff)
        
        #styleDef.apply(eff)
        #style_DR.apply(eff_DR)
        
        styles.markerStyles[0].apply(eff)
        styles.markerStyles[1].apply(eff_DR)
        '''
        eff_DR.SetLineStyle(ROOT.kSolid)
        eff.SetLineWidth(2)
        eff_DR.SetLineWidth(2)

        eff.SetLineStyle(ROOT.kSolid)
        eff_DR.SetLineStyle(ROOT.kSolid)

        eff.SetMarkerStyle(ROOT.kFullTriangleUp)
        eff_DR.SetMarkerStyle(ROOT.kFullTriangleUp)
        
        eff.SetMarkerSize(1.2)
        eff_DR.SetMarkerSize(1.2)
        '''
        # Append in list
        myList.append(histograms.HistoGraph(eff, legend, "p", "P"))
        myList.append(histograms.HistoGraph(eff_DR, legend_DR, "p", "P"))
        

    # Save plot in all formats
    #savePath = os.path.join(opts.saveDir, opts.optMode)
    #plots.drawPlot(p, savePath, **_kwargs)
    #SavePlot(p, saveName, savePath, saveFormats = [".png", ".pdf"])

        
        # Define stuff                                                                                                                                                                                          
    numPath  = numPath.replace("AfterAllSelections_","")
    numPath  = numPath.replace("LeadingTrijet_Pt", "LdgTopPt")
    if "Genuine" in numPath:
        TTcateg = "_TTgenuine"
    elif "Fake" in numPath:
        TTcateg = "_TTfake"
    else:
        TTcateg = "_TTinclusive"

    if "SR" in numPath:
        region = "_SR"
    if "VR" in numPath:
        region = "_VR"
    if "CR1" in numPath:
        region = "_CR1"
    if "CR2" in numPath:
        region = "_CR2"

    saveName = "Eff_" + numPath.split("/")[-1] + TTcateg + "_BDTtraining"

    # Plot the efficiency
    p = plots.ComparisonManyPlot(histograms.HistoGraph(eff, legend, "p", "P"), [histograms.HistoGraph(eff_DR, legend_DR, "p", "P")], saveFormats=[".pdf", ".png", ".C"])

    leg = ROOT.TLegend(0.2, 0.8, 0.81, 0.87)
    leg.SetFillStyle( 0)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    #{"dx": -0.55, "dy": -0.55, "dh": -0.08}
    leg.SetHeader("t#bar{t}")    
    #if "Fake" in numPath:
    #    leg.SetHeader("QCD")

    leg.Draw()
    #moveLegend       =  {"dx": -0.0, "dy": +0.0, "dh": +0.1}
    #moveLegend       = {"dx": -0.1, "dy": +0.0, "dh": +0.1}
    #p.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))


    # Save plot in all formats
    savePath = os.path.join(SAVEDIR, "HplusMasses", numPath.split("/")[0], opts.optMode)
    #savePath = os.path.join(opts.saveDir, numPath.split("/")[0], opts.optMode)
    plots.drawPlot(p, SAVEDIR, **_kwargs)
    #leg.Draw()
    SavePlot(p, saveName, SAVEDIR, saveFormats = [".png", ".pdf", ".C"])
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
    ANALYSISNAME = "SystTopBDT"
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
    SAVEDIR      = "/publicweb/%s/%s" % (getpass.getuser()[0], getpass.getuser()) + "/TopSystematics/Efficiencies"
    VERBOSE      = False
    HISTOLEVEL   = "Vital" # 'Vital' , 'Informative' , 'Debug'
    NORMALISE    = False
    FOLDER       = "" #"topSelection_" #"ForDataDrivenCtrlPlots" #"topologySelection_"
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
        raw_input("=== plot_Efficiency.py: Press any key to quit ROOT ...")
