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
./plotQCD_Fit.py -m <pseudo_mcrab_directory> [opts]
c
Examples:
./plotQCD_Fit.py -m -m /uscms_data/d3/aattikis/workspace/pseudo-multicrab/FakeBMeasurement_170629_102740_FakeBBugFix_TopChiSqrVar -e "QCD|Charged" --mergeEWK -o OptChiSqrCutValue100
./plotQCD_Fit.py -m /uscms_data/d3/aattikis/workspace/pseudo-multicrab/FakeBMeasurement_170629_102740_FakeBBugFix_TopChiSqrVar --mergeEWK -o OptChiSqrCutValue100 -e "QCD|Charged"
./plotQCD_Fit.py -m /uscms_data/d3/aattikis/workspace/pseudo-multicrab/FakeBMeasurement_170701_084855_NBJetsCutVar_AllSamples --mergeEWK -e "QCD|Charged" -o "OptNumberOfBJetsCutDirection>=ChiSqrCutValue100NumberOfBJetsCutValue1"
./plotQCD_Fit.py -m /uscms_data/d3/aattikis/workspace/pseudo-multicrab/FakeBMeasurement_170630_045528_IsGenuineBEventBugFix_TopChiSqrVar --mergeEWK -o OptChiSqrCutValue100 -e "QCD|Charged"
./plotQCD_Fit.py -m /uscms_data/d3/aattikis/workspace/pseudo-multicrab/FakeBMeasurement_170627_124436_BJetsGE2_TopChiSqrVar_AllSamples --mergeEWK -o "OptChiSqrCutValue100p0" -e "QCD|Charged"

Fit options:
https://root.cern.ch/root/htmldoc/guides/users-guide/FittingHistograms.html#the-th1fit-method
"0" Fit, store function but do not draw (needed since we re-draw the fit customised!)
"E" Better error estimation using MINOS technique
"R" Use the range specified in the function range
"B" Use this option when you want to fix one or more parameters and the fitting function is a predefined one, 
    like polN, expo, landau, gaus. Note that in case of pre-defined functions some default initial values and limits are set.
"L" Use log likelihood method (default is chi-square method). To be used when the histogram represents counts
"W" Set all weights to 1 for non empty bins; ignore error bars
"M" More. Improve fit results, by using the IMPROVE algorithm of TMinuit.
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
    _opts   = {"ymin": 1e0, "ymaxfactor": 1.2}
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
        style.setGridX(False)
        style.setGridY(False)
        
        # Do the fit on the histo after ALL selections (incl. topology cuts)
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
    if doFakeB:
        ewkFolder = genuineBFolder
        bkgName   = "FakeB"
    else:
        ewkFolder = inclusiveFolder
        bkgName   = "QCD"

    # Create the plotters
    p1 = plots.DataMCPlot(datasetsMgr, histoName % (inclusiveFolder, "Baseline") )
    p2 = plots.DataMCPlot(datasetsMgr, histoName % (ewkFolder      , "Baseline") )
    p3 = plots.DataMCPlot(datasetsMgr, histoName % (inclusiveFolder, "Inverted") )
    p4 = plots.DataMCPlot(datasetsMgr, histoName % (ewkFolder      , "Inverted") )

    # Get the histograms
    Data_baseline  = p1.histoMgr.getHisto("Data").getRootHisto().Clone("Baseline Data") #also legend entry name
    FakeB_baseline = p1.histoMgr.getHisto("Data").getRootHisto().Clone("Baseline " + bkgName)
    EWK_baseline   = p2.histoMgr.getHisto("EWK").getRootHisto().Clone("Baseline EWK")
    Data_inverted  = p3.histoMgr.getHisto("Data").getRootHisto().Clone("Inverted Data")
    FakeB_inverted = p3.histoMgr.getHisto("Data").getRootHisto().Clone("Inverted " + bkgName)
    EWK_inverted   = p4.histoMgr.getHisto("EWK").getRootHisto().Clone("Inverted EWK")

    # Create FakeB histos: FakeB = (Data - EWK)
    FakeB_baseline.Add(EWK_baseline, -1)
    FakeB_inverted.Add(EWK_inverted, -1)

    # Create the final plot object
    compareHistos = [EWK_baseline]
    p = plots.ComparisonManyPlot(FakeB_inverted, compareHistos, saveFormats=[])
    p.setLuminosity(GetLumi(datasetsMgr))

    # Apply styles
    p.histoMgr.forHisto("Inverted " + bkgName, styles.getFakeBStyle() )
    p.histoMgr.forHisto("Baseline EWK", styles.getAltEWKStyle() )

    # Set draw style
    p.histoMgr.setHistoDrawStyle("Inverted " + bkgName, "P")
    p.histoMgr.setHistoDrawStyle("Baseline EWK", "AP")

    # Set legend style
    p.histoMgr.setHistoLegendStyle("Inverted " + bkgName, "P")
    p.histoMgr.setHistoLegendStyle("Baseline EWK" , "LP")
    # p.histoMgr.setHistoLegendStyleAll("LP")

    # Set legend labels
    if doFakeB:
        p.histoMgr.setHistoLegendLabelMany({
                "Baseline EWKGenuineB": "EWK (GenuineB)",
                "Inverted FakeB"      : "Fake-b",
                })
    else:
        p.histoMgr.setHistoLegendLabelMany({
                "Baseline EWK"       : "EWK",
                "Inverted " + bkgName: "QCD",
                })

    #=========================================================================================
    # Set Minimizer Options
    #=========================================================================================
    '''
    https://root.cern.ch/root/htmldoc/guides/users-guide/FittingHistograms.html#the-th1fit-method
    https://root.cern.ch/root/html/src/ROOT__Math__MinimizerOptions.h.html#a14deB
    '''
    if 0:
        ROOT.Math.MinimizerOptions.SetDefaultMinimizer("Minuit", "Migrad")
        ROOT.Math.MinimizerOptions.SetDefaultStrategy(2) # Speed = 0, Balance = 1, Robustness = 2
        ROOT.Math.MinimizerOptions.SetDefaultMaxFunctionCalls(5000) # set maximum of function calls
        ROOT.Math.MinimizerOptions.SetDefaultMaxIterations(5000) # set maximum iterations (one iteration can have many function calls)
    if 0:
        ROOT.Math.MinimizerOptions.SetDefaultMinimizer("Minuit", "Simplex")
        ROOT.Math.MinimizerOptions.SetDefaultMinimizer("Minuit", "Minimize")
        ROOT.Math.MinimizerOptions.SetDefaultMinimizer("Minuit", "MigradImproved")
        ROOT.Math.MinimizerOptions.SetDefaultMinimizer("Minuit", "Scan")
        ROOT.Math.MinimizerOptions.SetDefaultMinimizer("Minuit", "Seek")
        ROOT.Math.MinimizerOptions.SetDefaultErrorDef(1) # error definition (=1. for getting 1 sigma error for chi2 fits)
        ROOT.Math.MinimizerOptions.SetDefaultMaxFunctionCalls(1000000) # set maximum of function calls
        ROOT.Math.MinimizerOptions.SetDefaultMaxIterations(1000000) # set maximum iterations (one iteration can have many function calls)
        ROOT.Math.MinimizerOptions.SetDefaultPrecision(-1) # precision in the objective function calculation (value <= 0 means left to default)
        ROOT.Math.MinimizerOptions.SetDefaultPrintLevel(1) # None = -1, Reduced = 0, Normal = 1, ExtraForProblem = 2, Maximum = 3 
        ROOT.Math.MinimizerOptions.SetDefaultTolerance(1e-03)  # Minuit/Minuit2 converge when the EDM is less a given tolerance. (default 1e-03)
    if 1:
        hLine  = "="*45
        title  = "{:^45}".format("Minimzer Options")
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
    FITMIN    =   80
    FITMAX    = 1000
    #moduleInfoString = opts.dataEra + "_" + opts.searchMode + "_" + opts.optMode
    moduleInfoString = opts.optMode

    #=========================================================================================
    # Create templates (EWK fakes, EWK genuine, QCD; data template is created by manager)
    #=========================================================================================
    manager = QCDNormalization.QCDNormalizationManagerDefault(binLabels, opts.mcrab, moduleInfoString)
    template_EWKFakeB_Baseline     = manager.createTemplate("EWKFakeB_Baseline")
    template_EWKFakeB_Inverted     = manager.createTemplate("EWKFakeB_Inverted")
    template_EWKInclusive_Baseline = manager.createTemplate("EWKInclusive_Baseline")
    template_EWKInclusive_Inverted = manager.createTemplate("EWKInclusive_Inverted")
    template_FakeB_Baseline        = manager.createTemplate("QCD_Baseline")
    template_FakeB_Inverted        = manager.createTemplate("QCD_Inverted")
        
    #======================================================================2==================
    # EWK
    #=========================================================================================
    par0 = [+7.1817e-01,   0.0,   1.0] # cb_norm 
    par1 = [+1.7684e+02, 150.0, 200.0] # cb_mean
    par2 = [+2.7287e+01,  20.0,  40.0] # cb_sigma (fixed for chiSq=2)
    par3 = [-3.9174e-01,  -0.5,   0.0] # cb_alpha (fixed for chiSq=2)
    par4 = [+2.5104e+01,   0.0,  50.0] # cb_n
    par5 = [+7.4724e-05,   0.0,   1.0] # expo_norm
    par6 = [-4.6848e-02,  -1.0,   0.0] # expo_a
    par7 = [+2.1672e+02, 200.0, 250.0] # gaus_mean (fixed for chiSq=2)
    par8 = [+6.3201e+01,  20.0,  80.0] # gaus_sigma

    template_EWKInclusive_Baseline.setFitter(QCDNormalization.FitFunction("EWKFunction", boundary=0, norm=1, rejectPoints=0), FITMIN, FITMAX)
    template_EWKInclusive_Baseline.setDefaultFitParam(defaultInitialValue = None,
                                                      defaultLowerLimit   = [par0[1], par1[1], par2[0], par3[0], par4[1], par5[1], par6[1], par7[0], par8[1]],
                                                      defaultUpperLimit   = [par0[2], par1[2], par2[0], par3[0], par4[2], par5[2], par6[2], par7[0], par8[2]])

    #=========================================================================================
    # FakeB/QCD
    #=========================================================================================
    par0 = [8.9743e-01,   0.0 ,    1.0] # lognorm_norm
    par1 = [2.3242e+02, 300.0 , 1000.0] # lognorm_mean
    par2 = [1.4300e+00,   0.5,    10.0] # lognorm_shape
    par3 = [2.2589e+02, 100.0 ,  500.0] # gaus_mean
    par4 = [4.5060e+01,   0.0 ,  100.0] # gaus_sigma
    
    template_FakeB_Inverted.setFitter(QCDNormalization.FitFunction("QCDFunctionAlt", boundary=0, norm=1, rejectPoints=0), FITMIN, FITMAX)
    template_FakeB_Inverted.setDefaultFitParam(defaultInitialValue = None,
                                               defaultLowerLimit   = [par0[1], par1[1], par2[1], par3[1], par4[1] ],
                                               defaultUpperLimit   = [par0[2], par1[2], par2[2], par3[2], par4[2] ])    
        
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
    fitOptions = "R B L W 0 Q M"
    manager.calculateNormalizationCoefficients(Data_baseline, fitOptions, FITMIN, FITMAX)
    
    # Only for when the measurement is done in bins
    fileName = os.path.join(opts.mcrab, "QCDInvertedNormalizationFactors%s.py"% ( getModuleInfoString(opts) ) )
    manager.writeNormFactorFile(fileName, opts)
    
    if 0:
        # Append analysisType to histogram name
        saveName = "LdgTrijetM_AfterAllSelections"
        
        # Draw the histograms
        plots.drawPlot(p, saveName, **GetHistoKwargs(histoName) ) #the "**" unpacks the kwargs_ 

        # Save plot in all formats
        SavePlot(p, saveName, os.path.join(opts.saveDir, "Fit") ) 
    return


def getModuleInfoString(opts):
    moduleInfoString = "_%s_%s" % (opts.dataEra, opts.searchMode)
    if opts.optMode != None:
        moduleInfoString += "_%s" % (opts.optMode)
    return moduleInfoString


def replaceQCDFromData(datasetMgr, datasetQCDdata):
    names = datasetMgr.getAllDatasetNames()
    index = names.index("QCD")
    names.pop(index)
    names.insert(index, datasetQCDdata.getName())
    datasetMgr.remove("QCD")
    datasetMgr.append(datasetQCDdata)
    datasetMgr.selectAndReorder(names)

def SavePlot(plot, plotName, saveDir, saveFormats = [".png", ".pdf"]):
    Verbose("Saving the plot in %s formats: %s" % (len(saveFormats), ", ".join(saveFormats) ) )

     # Check that path exists
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)

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
