#!/usr/bin/env python
'''
Description:
This scipt plots the TH1 histograms that compare EWK with QCD shapes, 
for Baseline and Inverted analysis modes.

For the definition of the counter class see:
HiggsAnalysis/NtupleAnalysis/scripts

For more counter tricks and optios see also:
HiggsAnalysis/NtupleAnalysis/scripts/hplusPrintCounters.py

Usage:
./plotFakeB_Fit.py -m <pseudo_mcrab_directory> [opts]
c
Examples:
./plotFakeB_Fit.py -m /uscms_data/d3/aattikis/workspace/pseudo-multicrab/FakeBMeasurement_170701_084855_NBJetsCutVar_AllSamples --mergeEWK -e "QCD|Charged" -o "OptNumberOfBJetsCutDirection>=ChiSqrCutValue100NumberOfBJetsCutValue1"
./plotFakeB_Fit.py -m /uscms_data/d3/aattikis/workspace/pseudo-multicrab/FakeBMeasurement_170630_045528_IsGenuineBEventBugFix_TopChiSqrVar --mergeEWK -o OptChiSqrCutValue100 -e "QCD|Charged"
./plotFakeB_Fit.py -m /uscms_data/d3/aattikis/workspace/pseudo-multicrab/FakeBMeasurement_170627_124436_BJetsGE2_TopChiSqrVar_AllSamples --mergeEWK -o "OptChiSqrCutValue100p0" -e "QCD|Charged"

Fit options:
https://root.cern.ch/root/htmldoc/guides/users-guide/FittingHistograms.html#the-th1fit-method
"0" Fit, store function but do not draw (needed since we re-draw the fit customised!)
"E" Better error estimation using MINOS technique
"R" Use the range specified in the function range
"B" Use this option when you want to fix one or more parameters and the fitting function is a predefined one, 
    like polN, expo, landau, gaus. Note that in case of pre-defined functions some default initial values and limits are set.
"L" Use log likelihood method (default is chi-square method). To be used when the histogram represents counts
"W" Set all weights to 1 for non empty bins; ignore error bars
"M" Improve fit results, by using the IMPROVE algorithm of TMinuit.
"Q" To suppress output (Quiet Mode)
"S" To return fit results (see "HLTausAnalysis/NtupleAnalysis/src/Auxiliary/src/HistoTools.C")
'''

#================================================================================================ 
# Imports
#================================================================================================ 
import sys
import math
import copy
import os
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
import HiggsAnalysis.FakeBMeasurement.QCDNormalization as QCDNormalization

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
    return ["TT", "WJetsToQQ_HT_600ToInf", "DYJetsToQQHT", "SingleTop"]#, "TTWJetsToQQ", "TTZToQQ", "Diboson", "TTTT"]
    #return ["TT"]


def GetHistoKwargs(histoName):
    '''
    '''
    Verbose("Creating a map of histoName <-> kwargs")

    _opts = {}


    # Definitions
    #_opts   = {"ymin": 1e0, "ymaxfactor": 2.0}
    _opts["xmax"] = 1500.0
    _rebinX = 1
    _units  = "GeV/c^{2}"

    # Define plotting options
    kwargs = {
        "xlabel"      : "m_{jjb} (%s)" % (_units),
        "ylabel"      : "Arbitrary Units / %s" % (_units),
        "log"         : False,
        "opts"        : _opts,
        "opts2"       : {"ymin": 0.0, "ymax": 2.0},
        "rebinX"      : 1,
        "ratio"       : False, 
        "cutBox"      : {"cutValue": 173.21, "fillColor": 16, "box": False, "line": True, "greaterThan": True},
        "cmsExtraText": "Preliminary",
        "ratioYlabel" : "Ratio",
        "ratioInvert" : False, 
        "addCmsText"  : True,
        "createLegend": {"x1": 0.62, "y1": 0.78, "x2": 0.92, "y2": 0.92},
        }
    return kwargs


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
    Verbose("main function")

    #optModes = ["", "OptChiSqrCutValue40", "OptChiSqrCutValue60", "OptChiSqrCutValue80", "OptChiSqrCutValue100", "OptChiSqrCutValue120", "OptChiSqrCutValue140"]
    #optModes = ["", "OptChiSqrCutValue50", "OptChiSqrCutValue100", "OptChiSqrCutValue150", "OptChiSqrCutValue200"]
    #optModes = ["", "OptChiSqrCutValue50p0", "OptChiSqrCutValue100p0", "OptChiSqrCutValue200p0"]
    optModes = ["OptChiSqrCutValue50p0", "OptChiSqrCutValue100p0"]

    if opts.optMode != None:
        optModes = [opts.optMode]

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

        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        plots.mergeRenameReorderForDataMC(datasetsMgr) 
        
        # Remove datasets
        datasetsMgr.remove(filter(lambda name: "QCD" in name, datasetsMgr.getAllDatasetNames()))
        datasetsMgr.remove(filter(lambda name: "QCD-b" in name, datasetsMgr.getAllDatasetNames()))
        datasetsMgr.remove(filter(lambda name: "Charged" in name, datasetsMgr.getAllDatasetNames()))
        
        # Re-order datasets (different for inverted than default=baseline)
        newOrder = ["Data"]
        newOrder.extend(GetListOfEwkDatasets())
        datasetsMgr.selectAndReorder(newOrder)

        # Set/Overwrite cross-sections
        for d in datasetsMgr.getAllDatasets():
            if "ChargedHiggs" in d.getName():
                datasetsMgr.getDataset(d.getName()).setCrossSection(1.0)

        # Sanity check
        if not opts.mergeEWK:
            Print("Cannot draw the histograms without the option --mergeEWK. Exit", True)
            sys.exit()

        # Merge EWK samples
        datasetsMgr.merge("EWK", GetListOfEwkDatasets())
        #plots._plotStyles["EWK"] = styles.getAltEWKStyle()
            
        # Print dataset information
        datasetsMgr.PrintInfo()
        
        # Apply TDR style
        style = tdrstyle.TDRStyle()
        style.setOptStat(True)
        
        # Do the fit
        hName  = "%s/%s_TopMassReco_LdgTrijetM_AfterAllSelections"
        PlotAndFitTemplates(datasetsMgr, hName, opts)
    return


def getHistos(datasetsMgr, hName):
    Verbose("getHistos()", True)

    baseline = "topSelection_Baseline/"
    inverted = "topSelection_Inverted/"

    h1 = datasetsMgr.getDataset("Data").getDatasetRootHisto(baseline+histoName)
    h1.setName("Baseline-Data")

    h2 = datasetsMgr.getDataset("EWK").getDatasetRootHisto(baseline+histoName)
    h2.setName("Baseline-EWK")

    h3 = datasetsMgr.getDataset("Data").getDatasetRootHisto(inverted+histoName)
    h3.setName("Inverted-Data")

    h4 = datasetsMgr.getDataset("EWK").getDatasetRootHisto(baseline+histoName)
    h4.setName("Inverted-EWK")
    return [h1, h2, h3, h4]


def getHisto(datasetsMgr, datasetName, histoName, analysisType):
    Verbose("getHisto()", True)

    h1 = datasetsMgr.getDataset(datasetName).getDatasetRootHisto(histoName)
    h1.setName(analysisType + "-" + datasetName)
    return h1


def PlotAndFitTemplates(datasetsMgr, histoName, opts):
    Verbose("PlotAndFitTemplates()")

    # Definitions
    doFakeB = False
    inclusiveFolder = "ForFakeBMeasurement"
    genuineBFolder  = "ForFakeBMeasurement" + "EWKGenuineB"
    fakeBFolder     = "ForFakeBMeasurement" + "EWKFakeB"

    # Get the histos for all settings
    p1 = plots.DataMCPlot(datasetsMgr, histoName % (inclusiveFolder, "Baseline") )
    p2 = plots.DataMCPlot(datasetsMgr, histoName % (genuineBFolder , "Baseline") )
    p3 = plots.DataMCPlot(datasetsMgr, histoName % (fakeBFolder    , "Baseline") )
    p4 = plots.DataMCPlot(datasetsMgr, histoName % (inclusiveFolder, "Inverted") )
    p5 = plots.DataMCPlot(datasetsMgr, histoName % (genuineBFolder , "Inverted") )
    p6 = plots.DataMCPlot(datasetsMgr, histoName % (fakeBFolder    , "Inverted") )

    # Get the baseline histos
    Data_baseline  = p1.histoMgr.getHisto("Data").getRootHisto().Clone("Baseline_Data")
    FakeB_baseline = p1.histoMgr.getHisto("Data").getRootHisto().Clone("Baseline_FakeB")
    if doFakeB:
        EWKGenuineB_baseline = p2.histoMgr.getHisto("EWK").getRootHisto().Clone("Baseline_EWKGenuineB")
    else:
        EWK_baseline = p1.histoMgr.getHisto("EWK").getRootHisto().Clone("Baseline_EWK")

    # Get the inverted histos
    Data_inverted  = p4.histoMgr.getHisto("Data").getRootHisto().Clone("Inverted_Data")
    FakeB_inverted = p4.histoMgr.getHisto("Data").getRootHisto().Clone("Inverted_FakeB")
    if doFakeB:
        EWKGenuineB_inverted = p5.histoMgr.getHisto("EWK").getRootHisto().Clone("Inverted_EWKGenuineB")
    else:
        EWK_inverted = p4.histoMgr.getHisto("EWK").getRootHisto().Clone("Inverted_EWK")

    # Create FakeB histos: FakeB = (Data - EWK)
    if doFakeB:
        FakeB_baseline.Add(EWKGenuineB_baseline, -1)
        FakeB_inverted.Add(EWKGenuineB_inverted, -1)
    else:
        FakeB_baseline.Add(EWK_baseline, -1)
        FakeB_inverted.Add(EWK_inverted, -1)

    # Normalize histograms to unit area
    if 0:
        FakeB_baseline.Scale(1.0/FakeB_baseline.Integral())
        FakeB_inverted.Scale(1.0/FakeB_inverted.Integral())
        if doFakeB:
            EWKGenuineB_baseline.Scale(1.0/EWKGenuineB_baseline.Integral())    
            EWKGenuineB_inverted.Scale(1.0/EWKGenuineB_inverted.Integral())
        else:
            EWK_baseline.Scale(1.0/EWK_baseline.Integral())    
            EWK_inverted.Scale(1.0/EWK_inverted.Integral())
        
    # Create the final plot object
    if doFakeB:
        compareHistos = [EWKGenuineB_baseline]
    else:
        compareHistos = [EWK_baseline]
    p = plots.ComparisonManyPlot(FakeB_inverted, compareHistos, saveFormats=[])
    p.setLuminosity(GetLumi(datasetsMgr))

    # Apply styles
    p.histoMgr.forHisto("Inverted_FakeB", styles.getFakeBStyle() )
    if doFakeB:
        p.histoMgr.forHisto("Baseline_EWKGenuineB", styles.getAltEWKStyle() )
    else:
        p.histoMgr.forHisto("Baseline_EWK", styles.getAltEWKStyle() )

    # Set draw style
    p.histoMgr.setHistoDrawStyle("Inverted_FakeB", "HIST")
    if doFakeB:
        p.histoMgr.setHistoDrawStyle("Baseline_EWKGenuineB", "AP")
    else:
        p.histoMgr.setHistoDrawStyle("Baseline_EWK", "AP")

    # Set legend style
    p.histoMgr.setHistoLegendStyle("Inverted_FakeB", "F")
    if doFakeB:
        p.histoMgr.setHistoLegendStyle("Baseline_EWKGenuineB", "LP")
    else:
        p.histoMgr.setHistoLegendStyle("Baseline_EWK", "LP")
    # p.histoMgr.setHistoLegendStyleAll("LP")                 

    # Set legend labels
    if doFakeB:
        p.histoMgr.setHistoLegendLabelMany({
                "Baseline_EWKGenuineB": "EWK (GenuineB)",
                "Inverted_FakeB"      : "Fake-b",
                })
    else:
        p.histoMgr.setHistoLegendLabelMany({
                "Baseline_EWK"  : "EWK",
                "Inverted_FakeB": "QCD",
                })

    #=========================================================================================
    # Set Minimizer Options
    #=========================================================================================
    '''
    https://root.cern.ch/root/htmldoc/guides/users-guide/FittingHistograms.html#the-th1fit-method
    https://root.cern.ch/root/html/src/ROOT__Math__MinimizerOptions.h.html#a14deB
    '''
    ROOT.Math.MinimizerOptions.SetDefaultMinimizer("Minuit", "Migrad")
    ROOT.Math.MinimizerOptions.SetDefaultStrategy(2) # Speed = 0, Balance = 1, Robustness = 2
    if 0:
        ROOT.Math.MinimizerOptions.SetDefaultMinimizer("Minuit", "Simplex")
        ROOT.Math.MinimizerOptions.SetDefaultMinimizer("Minuit", "Minimize")
        ROOT.Math.MinimizerOptions.SetDefaultMinimizer("Minuit", "MigradImproved")
        ROOT.Math.MinimizerOptions.SetDefaultMinimizer("Minuit", "Scan")
        ROOT.Math.MinimizerOptions.SetDefaultMinimizer("Minuit", "Seek")
        ROOT.Math.MinimizerOptions.SetDefaultErrorDef(1) #error definition (=1. for getting 1 sigma error for chi2 fits)
        ROOT.Math.MinimizerOptions.SetDefaultMaxFunctionCalls(1000000) # set maximum of function calls
        ROOT.Math.MinimizerOptions.SetDefaultMaxIterations(1000000) # set maximum iterations (one iteration can have many function calls)
        ROOT.Math.MinimizerOptions.SetDefaultPrecision(-1)     # precision in the objective function calculation (value <= 0 means left to default)
        ROOT.Math.MinimizerOptions.SetDefaultPrintLevel(1)     # None = -1, Reduced = 0, Normal = 1, ExtraForProblem = 2, Maximum = 3 
        ROOT.Math.MinimizerOptions.SetDefaultTolerance(1e-03)  # Minuit/Minuit2 converge when the EDM is less a given tolerance. (default 1e-03)
    if 1:
        hLine  = "="*40
        title  = "{:^40}".format("Minimzer Options")
        print "\t", hLine
        print "\t", title
        print "\t", hLine
        minOpt = ROOT.Math.MinimizerOptions()
        minOpt.Print()
        print "\t", hLine, "\n"

    #=========================================================================================
    # Start fit process
    #=========================================================================================
    binLabels = ["Inclusive"]
    moduleInfoString = opts.optMode
    FITMIN  =  80
    FITMAX  = 1000 #1000
    manager = QCDNormalization.QCDNormalizationManagerDefault(binLabels, opts.mcrab, moduleInfoString)

    #=========================================================================================
    # Create templates (EWK fakes, EWK genuine, QCD; data template is created by manager)
    #=========================================================================================
    template_EWKFakeB_Baseline     = manager.createTemplate("EWKFakeB_Baseline")
    template_EWKFakeB_Inverted     = manager.createTemplate("EWKFakeB_Inverted")
    template_EWKInclusive_Baseline = manager.createTemplate("EWKInclusive_Baseline")
    template_EWKInclusive_Inverted = manager.createTemplate("EWKInclusive_Inverted")
    template_FakeB_Baseline        = manager.createTemplate("QCD_Baseline")
    template_FakeB_Inverted        = manager.createTemplate("QCD_Inverted")
        
    #=======================================================================2==================
    # Inclusive EWK
    #=========================================================================================
    par0 = [+3.1000e-04,   0.0,   1.0] # expo_norm
    par1 = [+2.5600e-02,   0.0,   1.0] # expo_a
    par2 = [+7.3000e-01,   0.0,   1.0] # cb_norm 
    par3 = [+1.7580e+02, 150.0, 200.0] # cb_mean
    par4 = [+2.7630e+01, 200.0, 300.0] # cb_sigma
    par5 = [-3.8960e-01,  -1.0,   0.0] # cb_alpha
    par6 = [+2.2040e+01,   0.0,  40.0] # cb_n
    par7 = [+2.1230e+02, 200.0, 250.0] # gaus_mean
    par8 = [+6.6100e+01,  20.0,  80.0] # gaus_sigma
    template_EWKInclusive_Baseline.setFitter(QCDNormalization.FitFunction("EWKFunction", boundary=200, norm=1, rejectPoints=0), FITMIN, FITMAX)
    template_EWKInclusive_Baseline.setDefaultFitParam(defaultInitialValue = [par0[0], par1[0], par2[0], par3[0], par4[0], par5[0], par6[0], par7[0], par8[0]],
                                                      defaultLowerLimit   = [par0[1], par1[1], par2[1], par3[1], par4[1], par5[1], par6[1], par7[1], par8[1]],
                                                      defaultUpperLimit   = [par0[2], par1[2], par2[2], par3[2], par4[2], par5[2], par6[2], par7[2], par8[2]])
                                                      #defaultLowerLimit=[4.2278e-03, -1.0, 0.0, -0.1,  0.0,  0.0, 150.0, 200.0, 30.0],
                                                      #defaultUpperLimit=[4.2278e-03, +0.0, 1.0,  0.0, 50.0, 50.0, 200.0, 250.0, 90.0])
                                                      #defaultLowerLimit=[0.0,  0.0, 0.0, -0.1,  0.0, 150.0,  0.0, 200.0, 30.0],
                                                      #defaultUpperLimit=[1.0, +1.0, 1.0,  0.0, 50.0, 200.0, 50.0, 250.0, 90.0])
                                                      #defaultLowerLimit=[4.2278e-03, -2.5600e-02, 7.3043e-01, -3.8986e-01, 2.3260e+01, 2.7611e+01, 1.7777e+02, 2.1239e+02, 6.6367e+01],
                                                      #defaultUpperLimit=[4.2278e-03, -2.5600e-02, 7.3043e-01, -3.8986e-01, 2.3260e+01, 2.7611e+01, 1.7777e+02, 2.1239e+02, 6.6367e+01])
                                                      #defaultLowerLimit=[0.0, 150.0,  0.0, -5.0, 0.0, 0.0, 150.0,   0.0, 100.0,    0.0],
                                                      #defaultUpperLimit=[1.0, 300.0, 50.0,  0.0, 1.0, 1.0, 200.0, 100.0, 200.0,  100.0])
                                                      #defaultLowerLimit=[0.0, 160.0,   0.0, -1.0, 0.0],
                                                      #defaultUpperLimit=[1.0, 180.0,  60.0,  0.0, 1e6])

    #=========================================================================================
    # Note that the same function is used for QCD only and QCD+EWK fakes
    #=========================================================================================
    par0 = [   0.92 ,   0.0,   1.0] # lognorm_norm
    par1 = [ 229.0  , 180.0, 250.0] # lognorm_mean
    par2 = [   1.5  ,   0.0,   3.0] # lognorm_shape
    par3 = [   0.03 ,   0.0,   1.0] # expo_norm
    par4 = [   0.007,   0.0,   1.0] # expo_a
    par5 = [ 239.0  , 200.0, 300.0] # gaus_mean
    par6 = [  60.0  ,  20.0,  80.0] # gaus_sigma
    template_FakeB_Inverted.setFitter(QCDNormalization.FitFunction("QCDFunction", boundary=350, norm=1), FITMIN, FITMAX)
    template_FakeB_Inverted.setDefaultFitParam(defaultInitialValue = [par0[0], par1[0], par2[0], par3[0], par4[0], par5[0], par6[0]],
                                               defaultLowerLimit   = [par0[1], par1[1], par2[1], par3[1], par4[1], par5[1], par6[1]],
                                               defaultUpperLimit   = [par0[2], par1[2], par2[2], par3[2], par4[2], par5[2], par6[2]]
                                               )
    
    if 0:
        par0 = [   0.92,   0.0,    1.0 ] # lognorm_norm
        par1 = [ 234.4 , 200.0 , 250.0 ] # lognorm_mean
        par2 = [   1.44,   1.0,    2.0 ] # lognorm_shape
        par3 = [ 224.0 , 175.0 , 250.0 ] # gaus_mean
        par4 = [  45.5 ,   0.0 , 100.0 ] # gaus_sigma
        template_FakeB_Inverted.setFitter(QCDNormalization.FitFunction("QCDFunctionAlt", boundary=350, norm=1), FITMIN, FITMAX)
        template_FakeB_Inverted.setDefaultFitParam(defaultInitialValue = None, #[ par0[0], par1[0], par2[0], par3[0], par4[0]],
                                                   #defaultLowerLimit   = [ par0[0], par1[0], par2[0], par3[0], par4[1]],
                                                   #defaultUpperLimit   = [ par0[0], par1[0], par2[0], par3[0], par4[2]]
                                                   defaultLowerLimit   = [ par0[1], par1[1], par2[1], par3[1], par4[1]],
                                                   defaultUpperLimit   = [ par0[2], par1[2], par2[2], par3[2], par4[2]]
                                                   )

    #=========================================================================================
    # Set histograms to the templates
    #=========================================================================================
    if doFakeB:
        template_EWKFakeB_Baseline.setHistogram(EWKGenuineB_baseline, "Inclusive")
        template_EWKFakeB_Inverted.setHistogram(EWKGenuineB_inverted, "Inclusive")
        template_EWKInclusive_Baseline.setHistogram(EWKGenuineB_baseline, "Inclusive")
        template_EWKInclusive_Inverted.setHistogram(EWKGenuineB_inverted, "Inclusive")
    else:
        template_EWKFakeB_Baseline.setHistogram(EWK_baseline, "Inclusive")
        template_EWKFakeB_Inverted.setHistogram(EWK_inverted, "Inclusive")
        template_EWKInclusive_Baseline.setHistogram(EWK_baseline, "Inclusive")
        template_EWKInclusive_Inverted.setHistogram(EWK_inverted, "Inclusive")
    template_FakeB_Baseline.setHistogram(FakeB_baseline, "Inclusive")
    template_FakeB_Inverted.setHistogram(FakeB_inverted, "Inclusive")

    #=========================================================================================
    # Make plots of templates
    #=========================================================================================
    manager.plotTemplates()
    
    #=========================================================================================
    # Fit individual templates to histogram "data_baseline", with custom fit options
    #=========================================================================================
    fitOptions = "R B L W Q 0"

    manager.calculateNormalizationCoefficients(Data_baseline, fitOptions, FITMIN, FITMAX)
            
    # Append analysisType to histogram name
    saveName = "LdgTrijetM_AfterAllSelections"

    # Draw the histograms #alex
    plots.drawPlot(p, saveName, **GetHistoKwargs(histoName) ) #the "**" unpacks the kwargs_ 

    _kwargs = {"lessThan": True}
    p.addCutBoxAndLine(cutValue=173.21, fillColor=ROOT.kRed, box=False, line=True, **_kwargs)

    # Save plot in all formats
    SavePlot(p, saveName, os.path.join(opts.saveDir, "Templates") ) 
    return


def SavePlot(plot, plotName, saveDir, saveFormats = [".png", ".pdf"]):
    Verbose("Saving the plot in %s formats: %s" % (len(saveFormats), ", ".join(saveFormats) ) )

    # Create the name under which plot will be saved
    saveName = os.path.join(saveDir, plotName.replace("/", "_"))

    # For-loop: All save formats
    for i, ext in enumerate(saveFormats):
        saveNameURL = saveName + ext
        saveNameURL = saveNameURL.replace("/publicweb/a/aattikis/", "http://home.fnal.gov/~aattikis/")
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
    ANALYSISNAME = "FakeBMeasurement"
    SEARCHMODE   = "80to1000"
    DATAERA      = "Run2016"
    OPTMODE      = None
    BATCHMODE    = True
    PRECISION    = 3
    INTLUMI      = -1.0
    SUBCOUNTERS  = False
    LATEX        = False
    MCONLY       = False
    MERGEEWK     = False
    URL          = False
    NOERROR      = True
    SAVEDIR      = "/publicweb/a/aattikis/FakeBMeasurement/"
    VERBOSE      = False
    HISTOLEVEL   = "Vital" # 'Vital' , 'Informative' , 'Debug'

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

    parser.add_option("--mcOnly", dest="mcOnly", action="store_true", default=MCONLY,
                      help="Plot only MC info [default: %s]" % MCONLY)

    parser.add_option("--intLumi", dest="intLumi", type=float, default=INTLUMI,
                      help="Override the integrated lumi [default: %s]" % INTLUMI)

    parser.add_option("--searchMode", dest="searchMode", type="string", default=SEARCHMODE,
                      help="Override default searchMode [default: %s]" % SEARCHMODE)

    parser.add_option("--dataEra", dest="dataEra", type="string", default=DATAERA, 
                      help="Override default dataEra [default: %s]" % DATAERA)

    parser.add_option("--mergeEWK", dest="mergeEWK", action="store_true", default=MERGEEWK, 
                      help="Merge all EWK samples into a single sample called \"EWK\" [default: %s]" % MERGEEWK)

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

    # Call the main function
    main(opts)

    if not opts.batchMode:
        raw_input("=== plotHistograms.py: Press any key to quit ROOT ...")
