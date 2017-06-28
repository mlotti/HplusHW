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
./plotFit.py -m <pseudo_mcrab_directory> [opts]

Examples:
./plotFit.py -m /uscms_data/d3/aattikis/workspace/pseudo-multicrab/FakeBMeasurement_170602_235941_BJetsEE2_TopChiSqrVar_H2Var --mergeEWK --histoLevel Vital
./plotFit.py -m /uscms_data/d3/aattikis/workspace/pseudo-multicrab/FakeBMeasurement_170619_020728_BJetsGE2_TopChiSqrVar_AllSamples --mergeEWK -o "OptChiSqrCutValue140" -e "QCD-b|Charged"

Fit options:
https://root.cern.ch/root/htmldoc/guides/users-guide/FittingHistograms.html#the-th1fit-method
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

    if "mass" in histoName.lower():
        _format = "%0.0f GeV/c^{2}"
        _rebin  = 1
        _logY   = False
        _cutBox = {"cutValue": 173.21, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        #_opts["xmax"] = 800.0
    else:
        raise Exception("The kwargs have not been prepared for the histogram with name \"%s\"." % (histoName) )

    # Customise options (main pad) for with/whitout logY scale 
    if _logY:
        _opts["ymin"] = 1e-5
        _opts["ymaxfactor"] = 5
    else:
        _opts["ymin"] = 0.0
        _opts["ymaxfactor"] = 1.2

    # Define plotting options    
    kwargs = {"ylabel"      : "Arbitrary Units / %s" % (_format),
              "log"         : _logY,
              "opts"        : _opts,
              "opts2"       : {"ymin": 0.0, "ymax": 2.0},
              "rebinX"      : _rebin,
              "ratio"       : False, 
              "cutBox"      : _cutBox,
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
    optModes = ["OptChiSqrCutValue100"]
    if opts.optMode != None:
        optModes = [opts.Mode]

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
        newOrder = ["Data"] #, "TT", "DYJetsToQQHT", "TTWJetsToQQ", "WJetsToQQ_HT_600ToInf", "SingleTop", "Diboson", "TTZToQQ", "TTTT"]
        newOrder.extend(GetListOfEwkDatasets())
        datasetsMgr.selectAndReorder(newOrder)

        # Set/Overwrite cross-sections
        for d in datasetsMgr.getAllDatasets():
            if "ChargedHiggs" in d.getName():
                datasetsMgr.getDataset(d.getName()).setCrossSection(1.0)

        # Merge EWK samples
        if opts.mergeEWK:
            datasetsMgr.merge("EWK", GetListOfEwkDatasets())
            plots._plotStyles["EWK"] = styles.getAltEWKStyle()
        else:
            Print("Cannot draw the histograms without the option --mergeEWK. Exit", True)
            sys.exit()
            
        # Print dataset information
        datasetsMgr.PrintInfo()
        
        # Apply TDR style
        style = tdrstyle.TDRStyle()
        style.setOptStat(True)
        
        # Do the fit
        hName = "topSelection_Baseline/LdgTrijetMass_After" #"topSelection_Baseline/LdgTrijetMass_Before"
        PlotAndFitTemplates(datasetsMgr, hName.split("/")[-1], True, opts)
        
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


def PlotAndFitTemplates(datasetsMgr, histoName, addQcdBaseline, opts):
    Verbose("PlotAndFitTemplates()")

    # Create comparison plot
    p1 = plots.ComparisonPlot(
        getHisto(datasetsMgr, "Data", "topSelection_Baseline/%s" % histoName, "Baseline"),
        getHisto(datasetsMgr, "EWK" , "topSelection_Baseline/%s" % histoName, "Baseline")
        )
    p1.histoMgr.normalizeMCToLuminosity(datasetsMgr.getDataset("Data").getLuminosity())

    p2 = plots.ComparisonPlot(
        getHisto(datasetsMgr, "Data", "topSelection_Inverted/%s" % histoName, "Inverted"),
        getHisto(datasetsMgr, "EWK" , "topSelection_Inverted/%s" % histoName, "Inverted")
        )
    p2.histoMgr.normalizeMCToLuminosity(datasetsMgr.getDataset("Data").getLuminosity())


    # Get Baseline histos
    Data_baseline = p1.histoMgr.getHisto("Baseline-Data").getRootHisto().Clone("Baseline_Data")
    EWK_baseline  = p1.histoMgr.getHisto("Baseline-EWK").getRootHisto().Clone("Baseline_EWK")
    QCD_baseline  = p1.histoMgr.getHisto("Baseline-Data").getRootHisto().Clone("Baseline_QCD")

    # Get Inverted histos
    Data_inverted = p2.histoMgr.getHisto("Inverted-Data").getRootHisto().Clone("Inverted_Data")
    EWK_inverted  = p2.histoMgr.getHisto("Inverted-EWK").getRootHisto().Clone("Inverted_EWK")
    QCD_inverted  = p2.histoMgr.getHisto("Inverted-Data").getRootHisto().Clone("Inverted_QCD")

    # Create QCD histos: QCD = Data-EWK
    QCD_baseline.Add(EWK_baseline, -1)
    QCD_inverted.Add(EWK_inverted, -1)

    # Normalize histograms to unit area
    if 0:
        EWK_baseline.Scale(1.0/EWK_baseline.Integral())    
        EWK_inverted.Scale(1.0/EWK_inverted.Integral())
        QCD_baseline.Scale(1.0/QCD_baseline.Integral())
        QCD_inverted.Scale(1.0/QCD_inverted.Integral())
        
    # Create the final plot object
    if addQcdBaseline:
        compareHistos = [EWK_baseline, QCD_baseline]
    else:
        compareHistos = [EWK_baseline]
    p = plots.ComparisonManyPlot(QCD_inverted, compareHistos, saveFormats=[])
    p.setLuminosity(GetLumi(datasetsMgr))


    #=========================================================================================
    # Start Fit process
    #=========================================================================================
    binLabels = ["Inclusive"]
    moduleInfoString = opts.optMode
    FITMIN = 0
    FITMAX = 1500

    manager = QCDNormalization.QCDNormalizationManagerDefault(binLabels, opts.mcrab, moduleInfoString)

    #=========================================================================================
    # Create templates (EWK fakes, EWK genuine, QCD; data template is created by manager)
    #=========================================================================================
    template_EWKFakeB_Baseline     = manager.createTemplate("EWKFakeB_Baseline")
    template_EWKFakeB_Inverted     = manager.createTemplate("EWKFakeB_Inverted")
    template_EWKInclusive_Baseline = manager.createTemplate("EWKInclusive_Baseline")
    template_EWKInclusive_Inverted = manager.createTemplate("EWKInclusive_Inverted")
    template_QCD_Baseline          = manager.createTemplate("QCD_Baseline")
    template_QCD_Inverted          = manager.createTemplate("QCD_Inverted")
        
    #=========================================================================================
    # Inclusive EWK
    #=========================================================================================
    # par[0]*ROOT.Math.crystalball_function(x[0], par[1], par[2], par[3], par[4]) +
    # par[5]*ROOT.TMath.BreitWigner(x[0], par[6], par[7]) +
    # (1-par[0]-par[5])*ROOT.TMath.Landau(x[0], par[8], par[9])

    template_EWKInclusive_Baseline.setFitter(QCDNormalization.FitFunction("EWKFunction", boundary=200, norm=1, rejectPoints=0), FITMIN, FITMAX)
    #template_EWKInclusive_Baseline.setFitter(QCDNormalization.FitFunction("EWKFunction", boundary=200, norm=1, rejectPoints=0), FITMIN, 800)
    template_EWKInclusive_Baseline.setDefaultFitParam(defaultInitialValue=None,
                                                      #                   p0   p1     p2     p3     p4   p5    p6    p7      p8      p9
                                                      defaultLowerLimit=[0.0, 150.0,  0.0, -5.0, 0.0, 0.0, 150.0,   0.0, 100.0,    0.0],
                                                      defaultUpperLimit=[1.0, 300.0, 50.0,  0.0, 1.0, 1.0, 200.0, 100.0, 200.0,  100.0])
                                                      #defaultLowerLimit=[0.0, 160.0,   0.0, -1.0, 0.0],
                                                      #defaultUpperLimit=[1.0, 180.0,  60.0,  0.0, 1e6])

    #=========================================================================================
    # Note that the same function is used for QCD only and QCD+EWK fakes
    #=========================================================================================
    #par[0]*ROOT.Math.lognormal_pdf(x[0], par[1], par[2]) + par[3]*ROOT.TMath.Exp(-x[0]*par[4]) + (1-par[0]-par[3])*ROOT.TMath.Gaus(x[0], par[5], part[6])
    
    # 0 =   0.8489  for coeff of lognorm
    # 1 =   1.42978 for logshape
    # 2 = 238.546   for logmean
    #
    # 3 =   0.047   for coeff of exp
    # 4 =  -0.0048  for exp
    #
    # 5 =  45.486   for gaus sigma
    # 6 = 204.6     for gaus mean

    #my lognormal is of the form:
    #lognorm(x,m0,k) = exp{-[log(x/m0)]^2/[2*log(k)]^2}/sqrt[2pi*log(k)*x]
    #and differs than the Math::lognormal_pdf parametrization which takes as arguments lognormal(x,m,s,x0)
    #where m = log(m0) and s=log(k)
    #TMath::LogNormal  return Math::lognormal_pdf
    #my exponential is   exp(x*a)  so the sign comes from the fit
    #and my gaussian is exp[-0.5*mean*mean/(sigma*sigma)]

    # Double_t LogNormal(x, sigma, theta = 0, m = 1)

    #template_QCD_Inverted.setFitter(QCDNormalization.FitFunction("QCDFunction", boundary=350, norm=1), FITMIN, FITMAX)
    template_QCD_Inverted.setFitter(QCDNormalization.FitFunction("QCDFunction", boundary=350, norm=1), 100, 800)
    template_QCD_Inverted.setDefaultFitParam(defaultInitialValue=None,
                                             defaultLowerLimit=[0.0, 0.0, 200.0, 0.0, -0.1, 200.0,  0.0],
                                             defaultUpperLimit=[1.0, 2.0, 400.0, 0.1, +0.0, 300.0, 60.0])


    #=========================================================================================
    # Set histograms to the templates
    #=========================================================================================
    template_EWKFakeB_Baseline.setHistogram(EWK_baseline, "Inclusive")
    template_EWKFakeB_Inverted.setHistogram(EWK_inverted, "Inclusive")
    template_EWKInclusive_Baseline.setHistogram(EWK_baseline, "Inclusive")
    template_EWKInclusive_Inverted.setHistogram(EWK_inverted, "Inclusive")
    template_QCD_Baseline.setHistogram(QCD_baseline, "Inclusive")
    template_QCD_Inverted.setHistogram(QCD_inverted, "Inclusive")

    #=========================================================================================
    # Make plots of templates
    #=========================================================================================
    manager.plotTemplates()
    
    #=========================================================================================
    # Fit individual templates to histogram "data_baseline", with custom fit options
    #=========================================================================================
    fitOptions = "R B L W M Q"
    manager.calculateNormalizationCoefficients(Data_baseline, fitOptions, FITMIN, FITMAX)
            
    # Append analysisType to histogram name
    saveName = histoName

    # Draw the histograms #alex
    plots.drawPlot(p, saveName, **GetHistoKwargs(histoName) ) #the "**" unpacks the kwargs_ 

    _kwargs = {"lessThan": True}
    p.addCutBoxAndLine(cutValue=173.21, fillColor=ROOT.kRed, box=False, line=True, **_kwargs)

    # Save plot in all formats
    #SavePlot(p, saveName, os.path.join(opts.saveDir, "Templates") ) 
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
