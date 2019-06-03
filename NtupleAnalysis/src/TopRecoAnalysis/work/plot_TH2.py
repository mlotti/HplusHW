#!/usr/bin/env python
'''
Description:
Script for plotting TH2 histograms only.

Usage:


Examples:
./plot_TH2.py -m Hplus2tbAnalysis_3bjets40_MVA0p80_MVA0p80_TopMassCutOff600GeV_180112_023556 --folder ForDataDrivenCtrlPlots --gridX --gridY --dataset ChargedHiggs_HplusTB_HplusToTB_M_1000 --normalizeToLumi --logZ 
./plot_TH2.py -m Hplus2tbAnalysis_3bjets40_MVA0p80_MVA0p80_TopMassCutOff600GeV_180112_023556 --folder ForDataDrivenCtrlPlots --gridX --gridY --dataset TT --normalizeToOne --logZ 
./plot_TH2.py -m Hplus2tbAnalysis_3bjets40_MVA0p80_MVA0p80_TopMassCutOff600GeV_180112_023556 --folder ForDataDrivenCtrlPlots --gridX --gridY --dataset QCD --normalizeByCrossSection --logZ 
./plot_TH2.py -m Hplus2tbAnalysis_3bjets40_MVA0p80_MVA0p80_TopMassCutOff600GeV_180112_023556 --folder ForDataDrivenCtrlPlots --dataset TT --gridX --gridY --logY --logX
./plot_TH2.py -m Hplus2tbAnalysis_3bjets40_MVA0p80_MVA0p80_TopMassCutOff600GeV_180112_023556 --folder ForDataDrivenCtrlPlots --gridX --gridY --dataset QCD --normalizeToLumi --logZ --intLumi 100000

Last Used:
./plot_TH2.py -m Hplus2tbAnalysis_3bjets40_MVA0p80_MVA0p80_TopMassCutOff600GeV_180112_023556 --folder ForDataDrivenCtrlPlots --gridX --gridY --dataset QCD --normalizeToLumi --logZ 

'''

#================================================================================================ 
# Imports
#================================================================================================ 
import sys
import math
import copy
import os
import array
import re
from optparse import OptionParser

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
import HiggsAnalysis.NtupleAnalysis.tools.ShellStyles as ShellStyles

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
    Print(msg, printHeader)
    return


def rchop(myString, endString):
  if myString.endswith(endString):
    return myString[:-len(endString)]
  return myString


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


def GetListOfEwkDatasets():
    Verbose("Getting list of EWK datasets")
    return  ["TT", "WJetsToQQ_HT_600ToInf", "SingleTop", "DYJetsToQQHT", "TTZToQQ",  "TTWJetsToQQ", "Diboson", "TTTT"]


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
    

def main(opts):

    optModes = [""]

    if opts.optMode != None:
        optModes = [opts.optMode]
        
    # Apply TDR style
    style = tdrstyle.TDRStyle()
    style.setOptStat(False)
    style.setGridX(opts.gridX)
    style.setGridY(opts.gridY)
    style.setLogX(opts.logX)
    style.setLogY(opts.logY)
    style.setLogZ(opts.logZ)
    style.setWide(True, 0.15)
    # style.setPadRightMargin()#0.13)


    # For-loop: All opt Mode
    for opt in optModes:
        opts.optMode = opt

        # Setup & configure the dataset manager 
        datasetsMgr = GetDatasetsFromDir(opts)
        datasetsMgr.updateNAllEventsToPUWeighted()
        datasetsMgr.loadLuminosities() # from lumi.json
        if opts.verbose:
            datasetsMgr.PrintCrossSections()
            datasetsMgr.PrintLuminosities()
            datasetsMgr.PrintInfo()

        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        plots.mergeRenameReorderForDataMC(datasetsMgr) 
        
        # Print merged datasets and MC samples
        if 0:
            datasetsMgr.PrintInfo()

        # Get Luminosity
        if opts.intLumi < 0:
            opts.intLumi = datasetsMgr.getDataset("Data").getLuminosity()
            
        # Merge EWK samples
        if opts.dataset == "EWK":
            datasetsMgr.merge("EWK", GetListOfEwkDatasets())
            plots._plotStyles["EWK"] = styles.getAltEWKStyle()

        # Re-order datasets (different for inverted than default=baseline)
        newOrder = []
        for d in datasetsMgr.getAllDatasets():
            if d.getName() == opts.dataset:
                newOrder.append(d.getName())
        
        # Sanity check on selected dataset
        nDatasets = len(newOrder)
        if nDatasets < 1:
            msg = "Please select a valid dataset. Dataset \"%s\" does not exist!" % (opts.dataset)
            Print(ShellStyles.ErrorStyle() + msg + ShellStyles.NormalStyle(), True)
            datasetsMgr.PrintInfo()
            sys.exit()
        if nDatasets > 1:
            msg = "Please select only 1 valid dataset. Requested %i datasets for plotting!" % (nDatasets)
            Print(ShellStyles.ErrorStyle() + msg + ShellStyles.NormalStyle(), True)
            datasetsMgr.PrintInfo()
            sys.exit()

        # Select only given dataset         
        datasetsMgr.selectAndReorder(newOrder)

        # Print dataset information
        msg = "Plotting for single dataset \"%s\". Integrated luminosity is %.2f 1/fb" % (opts.dataset, opts.intLumi)
        Print(ShellStyles.NoteStyle() + msg + ShellStyles.NormalStyle(), True)
        datasetsMgr.PrintInfo()
            
        # Get list of histogram paths
        folder     = opts.folder
        histoList  = datasetsMgr.getDataset(datasetsMgr.getAllDatasetNames()[0]).getDirectoryContent(folder)
        histoPaths = [os.path.join(folder, h) for h in histoList]

        # For-loop: All histograms
        for h in histoPaths:
            if "Vs" not in h:
                continue
            if "DeltaMass_genH_recoH_Vs_BDT" not in h:
                continue
            Plot2dHistograms(datasetsMgr, h)


        #Marina
        for hName in ["DeltaMass_genH_recoH_Vs_BDT",                 "DeltaMass_genH_recoH_Vs_BDT_matchedBjet", 
                      "DeltaMass_genH_recoH_Vs_BDT_matchedChargedH", "DeltaMass_genH_recoH_Vs_BDT_unmatchedChargedH"]:

            myList = []
            #hName       = "DeltaMass_genH_recoH_Vs_BDT"
            hPath       = os.path.join(opts.folder, hName)
            histo      = GetHisto(datasetsMgr, opts.dataset, hPath, opts.intLumi)
            histo.RebinX(10)
            histo.RebinY(2)
            #print "Number of bins:", histo.GetNbinsX(), histo.GetNbinsY()
            ymin = 0
            ymax = 1
            ybins  = histo.GetNbinsY()
            i = 1
            xerrl = []
            xerrh = []
            yerrl = []
            yerrh = []
            xvalues = []
            yvalues = []
            myProf = []
            while i< ybins:
                tprofile   = ROOT.TProfile(histo.ProfileX("", i, ybins))
                i+=1
                #print histo.GetYaxis().GetBinLowEdge(i), histo.GetYaxis().GetBinLowEdge(ybins), tprofile.GetStdDev(), tprofile.GetStdDevError()
                if histo.GetYaxis().GetBinLowEdge(i) < 0:
                    #histoProf  = convertTProfile2TGraph(tprofile)
                    continue
                x = histo.GetYaxis().GetBinLowEdge(i)+0.5*histo.GetYaxis().GetBinWidth(i)
                if x > 0 and x < 0.1:
                    histoProf  = convertTProfile2TGraph(tprofile)
                xvalues.append(histo.GetYaxis().GetBinLowEdge(i)+0.5*histo.GetYaxis().GetBinWidth(i))
                #print histo.GetYaxis().GetBinLowEdge(i), tprofile.GetStdDev()
                yvalues.append(tprofile.GetStdDev())
                xerrl.append(0.5*histo.GetYaxis().GetBinWidth(i))
                xerrh.append(0.5*histo.GetYaxis().GetBinWidth(i))
                yerrl.append(tprofile.GetStdDevError())
                yerrh.append(tprofile.GetStdDevError())
                tprofile   = ROOT.TProfile(histo.ProfileX("",histo.GetNbinsY()-1, histo.GetNbinsY())) #histo.GetNbinsX()))
                
            #tgraph = ROOT.TGraph(len(xvalues), array.array("d", xvalues), array.array("d", yvalues))

            tgraph     = ROOT.TGraphAsymmErrors(len(xvalues) ,
                                                array.array("d",xvalues),
                                                array.array("d",yvalues),
                                                array.array("d",xerrl),
                                                array.array("d",xerrh),
                                                array.array("d",yerrl),
                                                array.array("d",yerrh))

            #Style = styles.ttStyle
            #plots._plotStyles[opts.dataset].apply(tgraph)
            counter = CounterStyle(opts.dataset)
            styles.markerStyles[counter].apply(tgraph)
            #Style.apply(tgraph)
            legend = opts.dataset
            legend = legend.replace("ChargedHiggs_HplusTB_HplusToTB_M_", "")
            legend = "m_{H^{+}} = "+legend+"GeV/c^{2}"
            myProf.append(histograms.HistoGraph(tgraph, legend, "lp", "P"))

            #myList = [tgraph]
            saveName = "MassRes_"+ hPath.split("/")[-1]
            p_prof = plots.PlotBase(datasetRootHistos=myProf, saveFormats=[])
            _kwargs = {           
                "xlabel"           : "BDTG",
                "ylabel"           : "#sigma(m_{H^{+},gen} - m_{H^{+},reco})", #/ %.1f ",                                                                
                "ratioYlabel"      : "Ratio",
                "ratio"            : False,
                "ratioInvert"      : False,
                "stackMCHistograms": False,
                "addMCUncertainty" : False,
                "addLuminosityText": False,
                "addCmsText"       : True,
                "cmsExtraText"     : "Preliminary",
                #"opts"             : {"ymin": 0.0, "ymax": 1.09},
                "opts"             : {"ymin": 150.0, "ymaxfactor": 1.1},
                "opts2"            : {"ymin": 0.6, "ymax": 1.4},
                "log"              : False,
                "moveLegend"       : {"dx": -0.2, "dy": -0.005, "dh": -0.08},
                "cutBoxY"          : {"cutValue": 1.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True, "mainCanvas": True, "ratioCanvas": False}
                }
            #saveName = saveName + 
            plots.drawPlot(p_prof, saveName, **_kwargs)
            # Save plot in all formats                                                                                                                                                                                       
            savePath = os.path.join(opts.saveDir, "MassRes", opts.optMode)
            #savePath = os.path.join(opts.saveDir, numPath.split("/")[0], opts.optMode)
            save_path = savePath
            SavePlot(p_prof, saveName, save_path, saveFormats = [".png"])



            # Apply default style (according to dataset name)
            plots._plotStyles[opts.dataset].apply(histoProf)
            # Append in list
            myList = []
            myList.append(histograms.HistoGraph(histoProf, plots._legendLabels[opts.dataset], "lp", "P"))

            # Define save name
            saveName = "Prof_" + hPath.split("/")[-1]
            _kwargs = GetHistoKwargs_TH1(hPath, opts)
            p = plots.PlotBase(datasetRootHistos=myList, saveFormats=[])
            plots.drawPlot(p, saveName, **_kwargs)
            ROOT.gStyle.SetNdivisions(10, "X")
            # Save plot in all formats
            SavePlot(p, saveName, os.path.join(opts.saveDir, "MassRes", opts.folder), [".png"])
            #PlotMC(datasetsMgr, histoProf, opts.intLumi)
            #> test = new TH2F("test","",100,0,10,100,0,10);
            #> test2 = new TH1D(test.ProfileX("",0,100));
    return



def CounterStyle(datasetName):
    if "ChargedHiggs_HplusTB_HplusToTB_M_" in datasetName:
        HplusMass = datasetName
        HplusMass.replace("ChargedHiggs_HplusTB_HplusToTB_M_", "")
        if "100" in HplusMass:
            return 1
        if "200" in HplusMass:
            return 2
        if "300" in HplusMass:
            return 3
        if "400" in HplusMass:
            return 4
        if "500" in HplusMass:
            return 5
        if "800" in HplusMass:
            return 8

    
def GetHistoKwargs_TH1(histoName, opts):
    h = histoName.lower()
    kwargs     = {
    "xlabel"           : "(m_{H^{+},gen} - m_{H^{+},reco}) (GeV/c^{2})",
        "ylabel"           : "mean (BDTG) ", #/ %.1f ",                                                                                                                                                             
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
        "opts"             : {"xmin": -800, "xmax": 800, "ymin": 0.0, "ymaxfactor": 1.0},
        "opts2"            : {"ymin": 0.6, "ymax": 1.4},
        "log"              : False,
        "moveLegend"       : {"dx": -0.2, "dy": -0.01, "dh": -0.18},
        "cutBoxY"          : {"cutValue": 1.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True, "mainCanvas": True, "ratioCanvas": False}
        }

    kwargs["opts"] =  {"ymin": 0.0, "ymax": 2}
    return kwargs

def PlotMC(datasetsMgr, histo, intLumi):

    kwargs = {}
    if 0:
        p = plots.MCPlot(datasetsMgr, histo, normalizeToOne=True, saveFormats=[], **kwargs)
    else:
        p = plots.MCPlot(datasetsMgr, histo, normalizeToLumi=intLumi, saveFormats=[], **kwargs)

    # Draw the histograms                                                                                                                                                              
    _cutBox = None
    _rebinX = 1
    _format = "%0.0f"
    _xlabel = None
    logY    = False
    _opts   = {"ymin": 1e-3, "ymaxfactor": 1.0}

    _opts["ymin"] = 1e0
    # Customise styling
    p.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetLineStyle(ROOT.kSolid))
        # Customise style                                                                                                                                                                  
    p.histoMgr.forHisto("ChargedHiggs_HplusTB_HplusToTB_M_500", styles.getSignalStyleHToTB_M500)
        
    plots.drawPlot(p,
                   histo,
                   xlabel       = _xlabel,
                   ylabel       = "Arbitrary Units / %s" % (_format),
                   log          = logY,
                   rebinX       = _rebinX, cmsExtraText = "Preliminary",
                   createLegend = {"x1": 0.58, "y1": 0.65, "x2": 0.92, "y2": 0.92},
                   opts         = _opts,
                   opts2        = {"ymin": 0.6, "ymax": 1.4},
                   cutBox       = _cutBox,
                   )

    # Save plot in all formats                                                                                                                                                         
    saveName = histo.split("/")[-1]
    savePath = os.path.join(opts.saveDir, "HplusMasses", histo.split("/")[0], opts.optMode)
    SavePlot(p, saveName, savePath)
    return


def convertTProfile2TGraph(tprofile):
    x     = []
    y     = []
    xerrl = []
    xerrh = []
    yerrl = []
    yerrh = []
    h = tprofile #.GetCopyTotalHisto()
    n = h.GetNbinsX()
    for i in range(1,n+1):
        #print tprofile.GetBinContent(i)
        x.append(h.GetBinLowEdge(i)+0.5*h.GetBinWidth(i))
        xerrl.append(0.5*h.GetBinWidth(i))
        xerrh.append(0.5*h.GetBinWidth(i))
        y.append(tprofile.GetBinContent(i))
        yerrl.append(tprofile.GetBinErrorLow(i))
        # ugly hack to prevent error going above 1
        errUp = tprofile.GetBinErrorUp(i)
        if y[-1] == 1.0:
            errUp = 0
        yerrh.append(errUp)
    return ROOT.TGraphAsymmErrors(n,array.array("d",x),
                                  array.array("d",y),
                                  array.array("d",xerrl),
                                  array.array("d",xerrh),
                                  array.array("d",yerrl),
                                  array.array("d",yerrh))


def GetHisto(datasetsMgr, dataset, hName, intLumi):
    n = datasetsMgr.getDataset(dataset).getDatasetRootHisto(hName)
    n.normalizeToLuminosity(intLumi)
    #n.normalizeToOne()
    histo = n.getHistogram()
    return histo


def GetHistoKwargs(h, opts):

    # Defaults
    xMin  =   0
    if opts.logX:
        yMin    =  1e0
    xMax  = 800
    yMin  =   0
    yMax  = 800
    if opts.logY:
        yMin    =  1
    yMaxF       = 10
    zMin        =  0
    zMax        = None
    zLabel      = "z-axis"
    if opts.normalizeToLumi:
        zLabel  = "Events"
        zMin    = 1e-3
    elif opts.normalizeByCrossSection:
        zLabel  = "#sigma (pb)"
        #zMin    = 0 #1e-3
    elif opts.normalizeToOne:
        zLabel  = "Arbitrary Units"
    else:
        zLabel = "Unknown"
#    cutBox      = {"cutValue": 400.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True} #box = True works
#    cutBoxY     = {"cutValue": 200.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True,
    cutBox      = {"cutValue": -1.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True} #box = True works
    cutBoxY     = {"cutValue": -1.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True,

                   "mainCanvas": True, "ratioCanvas": False} # box = True not working
    kwargs = {
        "stackMCHistograms": False,
        "addMCUncertainty" : False,
        "addLuminosityText": opts.normalizeToLumi,
        "addCmsText"       : True,
        "cmsExtraText"     : "  Preliminary",
        "xmin"             : xMin,
        "xmax"             : xMax,
        "ymin"             : yMin,
        "zmin"             : zMin,
        "zmax"             : zMax,
        "cutBox"           : cutBox,
        "cutBoxY"          : cutBoxY,
        "moveLegend"       : {"dx": -2.0, "dy": 0.0, "dh": -100.0}, #hack to remove legend (tmp)
        "zlabel"           : zLabel
        }

    if "LdgTrijetPt_Vs_LdgTrijetDijetPt" in h:
        kwargs["rebinX"]  = 2
        kwargs["rebinY"]  = 2

        units             = "(GeV/c)"
        kwargs["xlabel"]  = "p_{T}^{top} " + units
        kwargs["ylabel"]  = "p_{T}^{W} " + units
        kwargs["cutBox"]  = cutBox
        kwargs["cutBoxY"] = cutBoxY
        kwargs["rebinX"]  = 1
        kwargs["rebinY"]  = 1
        kwargs["opts"]    = {"xmin": 0.0, "xmax": +800.0, "ymin": yMin, "ymax": yMax} #, "ymaxfactor": yMaxF}
        #if  "AfterStandardSelections" in h:
        #if  "AfterAllSelections" in h:
        ROOT.gStyle.SetNdivisions(8, "X")
        ROOT.gStyle.SetNdivisions(8, "Y")
        
    if "SubldgTrijetPt_Vs_SubldgTrijetDijetPt" in h:
        kwargs["rebinX"]  = 2
        kwargs["rebinY"]  = 2

        units             = "(GeV/c)"
        kwargs["xlabel"]  = "p_{T}^{top} " + units
        kwargs["ylabel"]  = "p_{T}^{W} " + units
        kwargs["cutBox"]  = cutBox
        kwargs["cutBoxY"] = cutBoxY
        kwargs["rebinX"]  = 1
        kwargs["rebinY"]  = 1
        kwargs["opts"]    = {"xmin": 0.0, "xmax": +800.0, "ymin": yMin, "ymax": yMax} #, "ymaxfactor": yMaxF}
        # if  "AfterStandardSelections" in h:
        # if  "AfterAllSelections" in h:
        ROOT.gStyle.SetNdivisions(8, "X")
        ROOT.gStyle.SetNdivisions(8, "Y")


    if "TrijetJets_DeltaRmax_Vs_BDT" in h:
        kwargs["rebinX"]  = 2
        kwargs["rebinY"]  = 2
        kwargs["xlabel"]  = "#Delta R_{max}"
        kwargs["ylabel"]  = "BDTG"
        kwargs["opts"]    = {"xmin": 0.0, "xmax": +3.5, "ymin": 0.79, "ymax": 1.0}
        cutBox      = {"cutValue": 0.8, "fillColor": 16, "box": False, "line": True, "greaterThan": True} #box = True works
        cutBoxY     = {"cutValue": 0.8, "fillColor": 16, "box": False, "line": True, "greaterThan": True,
                       
                       "mainCanvas": True, "ratioCanvas": False} # box = True not working
        kwargs["cutBox"]  = cutBox
        kwargs["cutBoxY"] = cutBoxY
        ROOT.gStyle.SetNdivisions(10, "X")
        ROOT.gStyle.SetNdivisions(20, "Y")

    if "TrijetJets_DeltaRmin_Vs_BDT" in h:
        kwargs["rebinX"]  = 2
        kwargs["rebinY"]  = 2

        kwargs["xlabel"]  = "#Delta R_{min}"
        kwargs["ylabel"]  = "BDTG"
        kwargs["opts"]    = {"xmin": 0.0, "xmax": +2.5, "ymin": 0.79, "ymax": 1.0}
        cutBox      = {"cutValue": 0.8, "fillColor": 16, "box": False, "line": True, "greaterThan": True} #box = True works
        cutBoxY     = {"cutValue": 0.8, "fillColor": 16, "box": False, "line": True, "greaterThan": True,
                       
                       "mainCanvas": True, "ratioCanvas": False} # box = True not working
        kwargs["cutBox"]  = cutBox
        kwargs["cutBoxY"] = cutBoxY
        ROOT.gStyle.SetNdivisions(10, "X")
        ROOT.gStyle.SetNdivisions(20, "Y")

    if "TrijetJets_DeltaRmax_Vs_Pt" in h:
        kwargs["rebinX"]  = 2
        kwargs["rebinY"]  = 2

        units             = "(GeV/c)"
        kwargs["xlabel"]  = "#Delta R_{max}"
        kwargs["ylabel"]  = "p_{T,top}"+units
        kwargs["opts"]    = {"xmin": 0.0, "xmax": +3.5, "ymin": 0.0, "ymax": 600}
        cutBox      = {"cutValue": 0.8, "fillColor": 16, "box": False, "line": True, "greaterThan": True} #box = True works
        cutBoxY     = {"cutValue": 400, "fillColor": 16, "box": False, "line": True, "greaterThan": True,
                       
                       "mainCanvas": True, "ratioCanvas": False} # box = True not working
        kwargs["cutBox"]  = cutBox
        kwargs["cutBoxY"] = cutBoxY
        ROOT.gStyle.SetNdivisions(10, "X")
        ROOT.gStyle.SetNdivisions(10, "Y")

    if "TrijetJets_DeltaRmin_Vs_Pt" in h:
        kwargs["rebinX"]  = 2
        kwargs["rebinY"]  = 2
        units             = "(GeV/c)"
        kwargs["xlabel"]  = "#Delta R_{min}"
        kwargs["ylabel"]  = "P_{T,top}"+units
        kwargs["opts"]    = {"xmin": 0.0, "xmax": +2.5, "ymin": 0.0, "ymax": 600}
        cutBox      = {"cutValue": 0.8, "fillColor": 16, "box": False, "line": True, "greaterThan": True} #box = True works
        cutBoxY     = {"cutValue": 400, "fillColor": 16, "box": False, "line": True, "greaterThan": True,
                       
                       "mainCanvas": True, "ratioCanvas": False} # box = True not working
        kwargs["cutBox"]  = cutBox
        kwargs["cutBoxY"] = cutBoxY
        ROOT.gStyle.SetNdivisions(10, "X")
        ROOT.gStyle.SetNdivisions(10, "Y")

    if "TrijetPt_Vs_TetrajetBjetPt" in h:
        kwargs["rebinX"]  = 2
        kwargs["rebinY"]  = 2
        units             = "(GeV/c)"
        kwargs["xlabel"]  = "p_{T,top}"+units
        kwargs["ylabel"]  = "P_{T,b_{free}^{ldg}}"+units
        kwargs["opts"]    = {"xmin": 0.0, "xmax": 650, "ymin": 0.0, "ymax": 650}
        cutBox      = {"cutValue": 400, "fillColor": 16, "box": False, "line": True, "greaterThan": True} #box = True works
        cutBoxY     = {"cutValue": 0, "fillColor": 16, "box": False, "line": False, "greaterThan": True,
                       
                       "mainCanvas": True, "ratioCanvas": False} # box = True not working
        kwargs["cutBox"]  = cutBox
        kwargs["cutBoxY"] = cutBoxY
        ROOT.gStyle.SetNdivisions(10, "X")
        ROOT.gStyle.SetNdivisions(10, "Y")

    if "TrijetDijetPt_Vs_TetrajetBjetPt" in h:
        kwargs["rebinX"]  = 2
        kwargs["rebinY"]  = 2
        units             = "(GeV/c)"
        kwargs["xlabel"]  = "p_{T,W}"+units
        kwargs["ylabel"]  = "P_{T,b_{free}^{ldg}}"+units
        kwargs["opts"]    = {"xmin": 0.0, "xmax": 650, "ymin": 0.0, "ymax": 650}
        ROOT.gStyle.SetNdivisions(10, "X")
        ROOT.gStyle.SetNdivisions(10, "Y")

    if "DeltaR_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet" in h:
        kwargs["xlabel"]  = "#Delta R(Top^{ldg}, b_{free}^{ldg})"
        kwargs["ylabel"]  = "#Delta R(Top^{sbldg}, b_{free}^{ldg})"
        kwargs["rebinX"]  = 2
        kwargs["rebinY"]  = 2
        kwargs["opts"]    = {"xmin": 0.0, "xmax": 6, "ymin": 0.0, "ymax": 6}
        ROOT.gStyle.SetNdivisions(10, "X")
        ROOT.gStyle.SetNdivisions(10, "Y")

    if "DeltaEta_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet" in h:
        kwargs["xlabel"]  = "#Delta #eta (Top^{ldg}, b_{free}^{ldg})"
        kwargs["ylabel"]  = "#Delta #eta (Top^{sbldg}, b_{free}^{ldg})"
        kwargs["rebinX"]  = 4
        kwargs["rebinY"]  = 4
        kwargs["opts"]    = {"xmin": 0.0, "xmax": 6, "ymin": 0.0, "ymax": 6}
        ROOT.gStyle.SetNdivisions(10, "X")
        ROOT.gStyle.SetNdivisions(10, "Y")

    if "DeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet" in h:
        kwargs["xlabel"]  = "#Delta #phi (Top^{ldg}, b_{free}^{ldg})"
        kwargs["ylabel"]  = "#Delta #phi (Top^{sbldg}, b_{free}^{ldg})"
        kwargs["rebinX"]  = 1
        kwargs["rebinY"]  = 1
        kwargs["opts"]    = {"xmin": 0.0, "xmax": 3.15, "ymin": 0.0, "ymax": 3.15}
        ROOT.gStyle.SetNdivisions(10, "X")
        ROOT.gStyle.SetNdivisions(10, "Y")

    if "DeltaY_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet" in h:
        kwargs["xlabel"]  = "#Delta Y(Top^{ldg}, b_{free}^{ldg})"
        kwargs["ylabel"]  = "#Delta Y(Top^{sbldg}, b_{free}^{ldg})"
        kwargs["rebinX"]  = 2
        kwargs["rebinY"]  = 2
        kwargs["opts"]    = {"xmin": 0.0, "xmax": 4.5, "ymin": 0.0, "ymax": 4.5}
        ROOT.gStyle.SetNdivisions(10, "X")
        ROOT.gStyle.SetNdivisions(10, "Y")


    if "DeltaPhi_LdgTrijet_TetrajetBjet_Vs_TetrajetPt" in h:
        kwargs["rebinX"]  = 2
        kwargs["rebinY"]  = 2
        units             = "(GeV/c)"
        kwargs["xlabel"]  = "#Delta #phi(Top^{ldg}, b_{free}^{ldg})"
        kwargs["ylabel"]  = "p_{T}^{jjbb} " + units
        cutBox      = {"cutValue": 0.8, "fillColor": 16, "box": False, "line": True, "greaterThan": True} #box = True works
        cutBoxY     = {"cutValue": 0, "fillColor": 16, "box": False, "line": False, "greaterThan": True,
                       
                       "mainCanvas": True, "ratioCanvas": False} # box = True not working
        kwargs["cutBox"]  = cutBox
        kwargs["cutBoxY"] = cutBoxY
        kwargs["opts"]    = {"xmin": 0.0, "xmax": +3.15, "ymin": 0, "ymax": 900} #, "ymaxfactor": yMaxF}
        #if  "AfterStandardSelections" in h:
        #if  "AfterAllSelections" in h:
        ROOT.gStyle.SetNdivisions(8, "X")
        ROOT.gStyle.SetNdivisions(8, "Y")


    if "TrijetCountVsBDTcuts" in h:
        kwargs["xlabel"]  = "BDTG cut value"
        kwargs["ylabel"]  = "Trijet multiplicity -  after BDTG cut"
        cutBox      = {"cutValue": 0.85, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        cutBoxY     = {"cutValue": 2, "fillColor": 16, "box": False, "line": True, "greaterThan": True,
                       "mainCanvas": True, "ratioCanvas": False} # box = True not working                
        kwargs["cutBox"]  = cutBox
        kwargs["cutBoxY"] = cutBoxY
        kwargs["opts"]    = {"xmin": -1.0, "xmax": +1.0, "ymin": 0, "ymax": 120} #, "ymaxfactor": yMaxF}          


    if "TrijetMult_Vs_BDTcut" in h:
        kwargs["xlabel"]  = "BDTG cut value"
        kwargs["ylabel"]  = "Trijet multiplicity -  after BDTG cut"
        cutBox      = {"cutValue": 0.85, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        cutBoxY     = {"cutValue": 2, "fillColor": 16, "box": False, "line": True, "greaterThan": True,
                       "mainCanvas": True, "ratioCanvas": False} # box = True not working                
        kwargs["cutBox"]  = cutBox
        kwargs["cutBoxY"] = cutBoxY
        kwargs["opts"]    = {"xmin": -1.0, "xmax": +1.0, "ymin": 0, "ymax": 5} #, "ymaxfactor": yMaxF}          

    if "DeltaMass_genH_recoH_Vs_BDT" in h:
        kwargs["rebinX"]  = 10
        kwargs["rebinY"]  = 2
        kwargs["zmin"]    = 1e-3
        kwargs["ylabel"]  = "BDTG cut value"
        kwargs["xlabel"]  = "#Delta M(H^{+}_{gen} - H^{+}_{reco})"
        cutBox      = {"cutValue": 0.85, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
        cutBoxY     = {"cutValue": 2, "fillColor": 16, "box": False, "line": False, "greaterThan": True,
                       "mainCanvas": True, "ratioCanvas": False} # box = True not working                
        kwargs["cutBox"]  = cutBox
        kwargs["cutBoxY"] = cutBoxY
        kwargs["opts"]    = {"ymin": 0.0, "ymax": +1.0, "xmin": -800, "xmax": 800} #, "ymaxfactor": yMaxF}          
        ROOT.gStyle.SetNdivisions(10, "X")
    return kwargs
    

def Plot2dHistograms(datasetsMgr, histoName):
    Verbose("Plotting Data-MC Histograms")

    # Get Histogram name and its kwargs
    saveName = histoName.rsplit("/")[-1]
    kwargs   = GetHistoKwargs(saveName, opts)

    # Create the 2d plot
    if opts.dataset == "Data":
        p = plots.DataMCPlot(datasetsMgr, histoName, saveFormats=[])
    else:
        if opts.normalizeToLumi:
            p = plots.MCPlot(datasetsMgr, histoName, normalizeToLumi=opts.intLumi)
        elif opts.normalizeByCrossSection:
            p = plots.MCPlot(datasetsMgr, histoName, normalizeByCrossSection=True, **{})
        elif opts.normalizeToOne:
            p = plots.MCPlot(datasetsMgr, histoName, normalizeToOne=True, **{})
        else:
            raise Exception("One of the options --normalizeToOne, --normalizeByCrossSection, --normalizeToLumi must be enabled (set to \"True\").")
            
    # Customise z-axis
    p.histoMgr.forEachHisto(lambda h: h.getRootHisto().GetZaxis().SetTitle(kwargs["zlabel"]))
    p.histoMgr.forEachHisto(lambda h: h.getRootHisto().GetZaxis().SetTitleOffset(1.3))
    if kwargs.get("zmin") != None:
        zMin = float(kwargs.get("zmin"))
        p.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetMinimum(zMin))
    if kwargs.get("zmax") != None:
        zMax = float(kwargs.get("zmax"))
        p.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetMaximum(zMax))

    # Drawing style    
    p.histoMgr.setHistoDrawStyleAll("COLZ")

    # Add dataset name on canvas
    p.appendPlotObject(histograms.PlotText(0.18, 0.88, plots._legendLabels[opts.dataset], bold=True, size=22))

    # Draw the plot
    plots.drawPlot(p, saveName, **kwargs) #the "**" unpacks the kwargs_ dictionary

    # Save the plots in custom list of saveFormats
    SavePlot(p, saveName, os.path.join(opts.saveDir, opts.optMode, opts.folder), [".png"])#, ".pdf"] )
    return


def HasKeys(keyList, **kwargs):
    for key in keyList:
        if key not in kwargs:
            raise Exception("Could not find the keyword \"%s\" in kwargs" % (key) )
    return 


def SavePlot(plot, plotName, saveDir, saveFormats = [".png"]):
    Verbose("Saving the plot in %s formats: %s" % (len(saveFormats), ", ".join(saveFormats) ) )
    # Check that path exists
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)

    # Create the name under which plot will be saved
    name = plotName.replace("/", "_").replace(" ", "").replace("(", "").replace(")", "") 
    saveName = os.path.join(saveDir, name)
    # For-loop: All save formats
    for i, ext in enumerate(saveFormats):
        saveNameURL = saveName + ext
        saveNameURL = saveNameURL.replace(opts.saveDir, "http://home.fnal.gov/~%s/" % (getpass.getuser()))
        if opts.url:
            Print(saveNameURL, i==0)
        else:
            Print(saveName + ext, i==0)
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
    ANALYSISNAME = "TopRecoAnalysis"
    SEARCHMODE   = "80to1000"
    DATAERA      = "Run2016"
    OPTMODE      = None
    BATCHMODE    = True
    GRIDX        = False
    GRIDY        = False
    LOGX         = False
    LOGY         = False
    LOGZ         = False
    URL          = False
    SAVEDIR      = "/publicweb/%s/%s/%s" % (getpass.getuser()[0], getpass.getuser(), ANALYSISNAME)
    VERBOSE      = False
    FOLDER       = "topbdtSelection_" #"topbdtSelection_" #jetSelection_
    DATASET      = "Data"
    INTLUMI      = -1.0
    NORM2ONE     = False
    NORM2XSEC    = False
    NORM2LUMI    = False

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

    parser.add_option("--searchMode", dest="searchMode", type="string", default=SEARCHMODE,
                      help="Override default searchMode [default: %s]" % SEARCHMODE)

    parser.add_option("--dataEra", dest="dataEra", type="string", default=DATAERA, 
                      help="Override default dataEra [default: %s]" % DATAERA)

    parser.add_option("--gridX", dest="gridX", action="store_true", default=GRIDX, 
                      help="Enable the x-axis grid lines [default: %s]" % GRIDX)

    parser.add_option("--gridY", dest="gridY", action="store_true", default=GRIDY, 
                      help="Enable the y-axis grid lines [default: %s]" % GRIDY)

    parser.add_option("--logX", dest="logX", action="store_true", default=LOGX, 
                      help="Set x-axis to logarithm scale [default: %s]" % LOGX)

    parser.add_option("--logY", dest="logY", action="store_true", default=LOGY,
                      help="Set y-axis to logarithm scale [default: %s]" % LOGY)

    parser.add_option("--logZ", dest="logZ", action="store_true", default=LOGZ,
                      help="Set z-axis to logarithm scale [default: %s]" % LOGZ)

    parser.add_option("--saveDir", dest="saveDir", type="string", default=SAVEDIR, 
                      help="Directory where all pltos will be saved [default: %s]" % SAVEDIR)

    parser.add_option("--url", dest="url", action="store_true", default=URL, 
                      help="Don't print the actual save path the histogram is saved, but print the URL instead [default: %s]" % URL)
    
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=VERBOSE, 
                      help="Enables verbose mode (for debugging purposes) [default: %s]" % VERBOSE)

    parser.add_option("-i", "--includeOnlyTasks", dest="includeOnlyTasks", action="store", 
                      help="List of datasets in mcrab to include")

    parser.add_option("-e", "--excludeTasks", dest="excludeTasks", action="store", 
                      help="List of datasets in mcrab to exclude")

    parser.add_option("--folder", dest="folder", type="string", default = FOLDER,
                      help="ROOT file folder under which all histograms to be plotted are located [default: %s]" % (FOLDER) )

    parser.add_option("--dataset", dest="dataset", default = DATASET,
                      help="Dataset to draw (only 1 allowed in 2D) [default: %s]" % (DATASET) )

    parser.add_option("--intLumi", dest="intLumi", type=float, default=INTLUMI,
                      help="Override the integrated lumi [default: %s]" % INTLUMI)

    parser.add_option("--normalizeToOne", dest="normalizeToOne", action="store_true", default=NORM2ONE,
                      help="Normalise plot to one [default: %s]" % NORM2ONE)

    parser.add_option("--normalizeByCrossSection", dest="normalizeByCrossSection", action="store_true", default=NORM2XSEC,
                      help="Normalise plot by cross-section [default: %s]" % NORM2XSEC)

    parser.add_option("--normalizeToLumi", dest="normalizeToLumi", action="store_true", default=NORM2LUMI,
                      help="Normalise plot to luminosity [default: %s]" % NORM2LUMI)

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
    else:
        mcrabDir = rchop(opts.mcrab, "/")
        if len(mcrabDir.split("/")) > 1:
            mcrabDir = mcrabDir.split("/")[-1]#:]
        opts.saveDir += opts.dataset

    if opts.normalizeToOne == False and opts.normalizeByCrossSection == False and opts.normalizeToLumi == False:
        raise Exception("One of the options --normalizeToOne, --normalizeByCrossSection, --normalizeToLumi must be enabled (set to \"True\").")


    # Sanity check
    allowedFolders = ["counters", "counters/weighted", "PUDependency", "Weighting", 
                      "eSelection_Veto", "muSelection_Veto", "tauSelection_Veto",
                      "ForDataDrivenCtrlPlotsEWKFakeB", "ForDataDrivenCtrlPlotsEWKGenuineB",
                      "jetSelection_", "bjetSelection_", "metSelection_", 
                      "topologySelection_", "topbdtSelection_", "ForDataDrivenCtrlPlots", "TopAnalysisTH2", "TopAnalysisTH2True", "TopAnalysisTH2False", "topbdtSelectionTH2_", "AnalysisTH2_"]

    if opts.folder not in allowedFolders:
        Print("Invalid folder \"%s\"! Please select one of the following:" % (opts.folder), True)
        for m in allowedFolders:
            Print(m, False)
        sys.exit()

    # Call the main function
    main(opts)

    if not opts.batchMode:
        raw_input("=== plotDataMC_ControlPlots.py: Press any key to quit ROOT ...")
