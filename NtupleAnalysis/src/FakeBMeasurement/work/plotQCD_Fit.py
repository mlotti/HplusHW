#!/usr/bin/env python
'''
Description:
This script produces QCD normalization factors by running a fitting script.
The steps followed are the following:
1) The user defines the histograms to be used as templates. Two are needed:
   a) Baseline EWK (MC)
   b) Inverted QCD (Data)
This will be used in the fitting processes to extract the templates for:
   a) EWK
   b) QCD
This step gives us the two fitted templates:
   a) fit_EWKInclusive_Baseline_Inclusive.png
   b) fit_QCD_Inverted_Inclusive.png

2) The two extracted templates (from fits) are then used to fit on "Baseline Data" 
(our Signal Region) as a linear combination with the fraction of QCD (f) as the only 
free parameter of the fit:
N = fQCD + (1-f)EWK
This step gives us the final fit and the fit parameter:
   a) finalFit_Inclusive.png 
   b) finalFit_Inclusive_log.png
   c) f = Fraction of QCD Events

In addition to the above, the normalisation factor is also extrated:
   a) R = nQCDBaseline / nQCDInverted
   b) R = nFakeBaseline / nFakeInverted 
where the later is not used in any way (HToTauNu legacy)
These normalisation factor are saved under:
   <pseudo_mcrab_directory> QCDInvertedNormalizationFactors_Run2016_80to1000.py
in an automatically-generated python class. 

This file/class is later used (read) by the makeInvertedPseudoMulticrab.py in order to normalise
properly the "Control-Region" data.


Usage:
./plotQCD_Fit.py -m <pseudo_mcrab_directory> [opts]


Examples:
./plotQCD_Fit.py -m FakeBMeasurement_SignalTriggers_NoTrgMatch_StdSelections_TopCut_AllSelections_TopCut10_170725_030408/ --url -o ""


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
ROOT.gErrorIgnoreLevel = ROOT.kFatal #kPrint = 0,  kInfo = 1000, kWarning = 2000, kError = 3000, kBreak = 4000, kSysError = 5000, kFatal = 6000
from ROOT import *

import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.counter as counter
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.styles as styles
import HiggsAnalysis.NtupleAnalysis.tools.ShellStyles as ShellStyles
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
    return ["TT", "WJetsToQQ_HT_600ToInf", "DYJetsToQQHT", "SingleTop", "TTWJetsToQQ", "TTZToQQ", "Diboson", "TTTT"]

def GetHistoKwargs(histoName):
    '''
    '''
    Verbose("Creating a map of histoName <-> kwargs")

    _opts = {}


    # Definitions
    _opts         = {"ymin": 1e0, "ymaxfactor": 1.2}
    _rebinX       = 1
    _units        = "GeV/c^{2}"
    _opts["xmax"] = 1000.0

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
    
def getHisto(datasetsMgr, datasetName, histoName, analysisType):
    Verbose("getHisto()", True)

    h1 = datasetsMgr.getDataset(datasetName).getDatasetRootHisto(histoName)
    h1.setName(analysisType + "-" + datasetName)
    return h1

def getModuleInfoString(opts):
    moduleInfoString = "_%s_%s" % (opts.dataEra, opts.searchMode)
    if len(opts.optMode) > 0:
        moduleInfoString += "_%s" % (opts.optMode)
    return moduleInfoString

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
def main(opts):
    Verbose("main function")

    #optModes = ["", "OptChiSqrCutValue40", "OptChiSqrCutValue60", "OptChiSqrCutValue80", "OptChiSqrCutValue100", "OptChiSqrCutValue120", "OptChiSqrCutValue140"]
    optModes = [""]

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
            
        # Get the PSets:
        thePSets = datasetsMgr.getDataset("TT").getParameterSet()
        if 0:
            Print("Printing the PSet:\n" + thePSets, True)
            sys.exit()

        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        plots.mergeRenameReorderForDataMC(datasetsMgr) 
        
        # Remove datasets
        removeList = ["QCD", "QCD-b", "Charged"]
        for d in removeList:
            datasetsMgr.remove(filter(lambda name: d in name, datasetsMgr.getAllDatasetNames()))
        if 0:
            datasetsMgr.PrintInfo()
        
        # Re-order datasets (different for inverted than default=baseline)
        newOrder = ["Data"]
        newOrder.extend(GetListOfEwkDatasets())
        datasetsMgr.selectAndReorder(newOrder)

        # Merge EWK samples
        datasetsMgr.merge("EWK", GetListOfEwkDatasets())
            
        # Print dataset information
        datasetsMgr.PrintInfo()

        # Apply TDR style
        style = tdrstyle.TDRStyle()
        style.setOptStat(True)
        style.setGridX(False)
        style.setGridY(False)
        
        # Do the fit on the histo after ALL selections (incl. topology cuts)
        folderName = "ForFakeBNormalization"
        histoName  = "LdgTrijetMass_AfterStandardSelections"
        PlotAndFitTemplates(datasetsMgr, histoName, folderName, opts)
    return

def PlotAndFitTemplates(datasetsMgr, histoName, inclusiveFolder, opts):
    Verbose("PlotAndFitTemplates()")

    # Variable definition
    bkgName         = "QCD"
    genuineBFolder  = inclusiveFolder + "EWKGenuineB"
    fakeBFolder     = inclusiveFolder + "EWKFakeB"
    baselineHisto   = "%s/%s" % (inclusiveFolder, "Baseline_" + histoName)
    invertedHisto   = "%s/%s" % (inclusiveFolder, "Inverted_" + histoName)

    # Create the histograms
    pBaseline  = plots.DataMCPlot(datasetsMgr, baselineHisto)
    pInverted  = plots.DataMCPlot(datasetsMgr, invertedHisto)
            
    # Get the desired histograms (Baseline)
    Data_baseline  = pBaseline.histoMgr.getHisto("Data").getRootHisto().Clone("Baseline Data") #also legend entry name
    FakeB_baseline = pBaseline.histoMgr.getHisto("Data").getRootHisto().Clone("Baseline " + bkgName)
    EWK_baseline   = pBaseline.histoMgr.getHisto("EWK").getRootHisto().Clone("Baseline EWK")

    # Get the desired histograms (Inverted)
    # Data_inverted  = pInverted.histoMgr.getHisto("Data").getRootHisto().Clone("Inverted Data") #not needed
    FakeB_inverted = pInverted.histoMgr.getHisto("Data").getRootHisto().Clone("Inverted " + bkgName)
    EWK_inverted   = pInverted.histoMgr.getHisto("EWK").getRootHisto().Clone("Inverted EWK")

    # Subtact EWK-M Cfrom Data (QCD = Data - EWK)
    FakeB_baseline.Add(EWK_baseline, -1)
    FakeB_inverted.Add(EWK_inverted, -1)

    # Rebin the EWK-MC histo (significant fit improvement - opposite effect for QCD fit)
    EWK_baseline.RebinX(2)
    EWK_inverted.RebinX(2)

    # No need to normalise
    if 0:
        EWK_baseline.Scale(1/EWK_baseline.Integral())
        FakeB_inverted.Scale(1/FakeB_inverted.Integral())

    # Create the final plot object
    compareHistos = [EWK_baseline]
    p = plots.ComparisonManyPlot(FakeB_inverted, compareHistos, saveFormats=[])

    # Apply styles
    p.histoMgr.forHisto("Inverted " + bkgName, styles.getFakeBStyle() )
    p.histoMgr.forHisto("Baseline EWK", styles.getAltEWKStyle() )

    # Set draw style
    p.histoMgr.setHistoDrawStyle("Inverted " + bkgName, "P")
    p.histoMgr.setHistoDrawStyle("Baseline EWK", "AP")

    # Set legend style
    p.histoMgr.setHistoLegendStyle("Inverted " + bkgName, "P")
    p.histoMgr.setHistoLegendStyle("Baseline EWK" , "LP")

    # Set legend labels
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
        ROOT.Math.MinimizerOptions.SetDefaultStrategy(1) # Speed = 0, Balance = 1, Robustness = 2
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
        title  = "{:^45}".format("Minimizer Options")
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
    moduleInfoString = opts.optMode #opts.dataEra + "_" + opts.searchMode + "_" + opts.optMode

    #=========================================================================================
    # Create templates (EWK fakes, EWK genuine, QCD; data template is created by manager)
    #=========================================================================================
    manager = QCDNormalization.QCDNormalizationManagerDefault(binLabels, opts.mcrab, moduleInfoString)

    Print("Creating the normalization templates with appropriate template names", True)
    template_EWKFakeB_Baseline     = manager.createTemplate("EWKFakeB_Baseline") #fixme-unused
    template_EWKFakeB_Inverted     = manager.createTemplate("EWKFakeB_Inverted") #fixme-unused

    template_EWKInclusive_Baseline = manager.createTemplate("EWKInclusive_Baseline")
    template_EWKInclusive_Inverted = manager.createTemplate("EWKInclusive_Inverted")
    
    template_FakeB_Baseline        = manager.createTemplate("QCD_Baseline")
    template_FakeB_Inverted        = manager.createTemplate("QCD_Inverted")

    #========================================================================================
    # EWK
    #=========================================================================================
    '''
    Optimal fit (Chi2/D.O.F = 3.2)
    FITMIN  ;  80
    FITMAX  : 800
    BinWidth:  10 GeV/c^2
    par3    : -3.9174e-01 (fixed)
    '''
    Print("Setting the fit-function to the EWK template", False)
    FITMIN_EWK =  80 
    FITMAX_EWK = 800 
    par0 = [+7.1817e-01,   0.0,   1.0] # cb_norm 
    par1 = [+1.7684e+02, 150.0, 200.0] # cb_mean
    par2 = [+2.7287e+01,  20.0,  40.0] # cb_sigma (fixed for chiSq=2)
    par3 = [-3.9174e-01,  -1.0,   0.0] # cb_alpha (fixed for chiSq=2)
    par4 = [+2.5104e+01,   0.0,  50.0] # cb_n
    par5 = [+7.4724e-05,   0.0,   1.0] # expo_norm
    par6 = [-4.6848e-02,  -1.0,   0.0] # expo_a
    par7 = [+2.1672e+02, 200.0, 250.0] # gaus_mean (fixed for chiSq=2)
    par8 = [+6.3201e+01,  20.0,  80.0] # gaus_sigma
    template_EWKInclusive_Baseline.setFitter(QCDNormalization.FitFunction("EWKFunction", boundary=0, norm=1, rejectPoints=0), FITMIN_EWK, FITMAX_EWK)
    template_EWKInclusive_Baseline.setDefaultFitParam(defaultInitialValue = None,
                                                      defaultLowerLimit   = [par0[1], par1[1], par2[1], par3[0], par4[1], par5[1], par6[1], par7[1], par8[1]],
                                                      defaultUpperLimit   = [par0[2], par1[2], par2[2], par3[0], par4[2], par5[2], par6[2], par7[2], par8[2]])

    #=========================================================================================
    # QCD
    #=========================================================================================
    '''
    Optimal fit (Chi2/D.O.F = 25.6)
    FITMIN  :   80
    FITMAX  : 1000
    BinWidth:  5 GeV/c^2
    '''
    Print("Setting the fit-function to the QCD template", False)
    FITMIN_QCD =   80
    FITMAX_QCD = 1000
    bPtochos   = False
    if bPtochos:
        par0 = [9.55e-01,   0.0 ,    1.0] # lognorm_norm
        par1 = [2.33e+02,   0.0 , 1000.0] # lognorm_mean
        par2 = [1.44e+00,   0.5 ,   10.0] # lognorm_shape
        par3 = [2.2e-03 ,   0.0 ,    1.0] # exp_const
        par4 = [-6.2e-03,  -1.0 ,    0.0] # exp_coeff
        par5 = [2.17e+02, 200.0 ,  250.0] # gaus_mean
        par6 = [3.08e+01,   0.0 ,  100.0] # gaus_sigma
        template_FakeB_Inverted.setFitter(QCDNormalization.FitFunction("QCDFunction", boundary=0, norm=1, rejectPoints=0), FITMIN_QCD, FITMAX_QCD)
        template_FakeB_Inverted.setDefaultFitParam(defaultInitialValue = [par0[0], par1[0], par2[0], par3[0], par4[0] , par5[0], par6[0] ],
                                                   defaultLowerLimit   = [par0[1], par1[1], par2[1], par3[1], par4[1] , par5[1], par6[1] ],
                                                   defaultUpperLimit   = [par0[2], par1[2], par2[2], par3[2], par4[2] , par5[2], par6[2] ])
    else:
        par0 = [8.9743e-01,   0.0 ,    1.0] # lognorm_norm
        par1 = [2.3242e+02, 200.0 , 1000.0] # lognorm_mean
        par2 = [1.4300e+00,   0.5,    10.0] # lognorm_shape
        par3 = [2.2589e+02, 100.0 ,  500.0] # gaus_mean
        par4 = [4.5060e+01,   0.0 ,  100.0] # gaus_sigma
        template_FakeB_Inverted.setFitter(QCDNormalization.FitFunction("QCDFunctionAlt", boundary=0, norm=1, rejectPoints=0), FITMIN_QCD, FITMAX_QCD)
        template_FakeB_Inverted.setDefaultFitParam(defaultInitialValue = [par0[0], par1[0], par2[0], par3[0], par4[0] ],
                                                   defaultLowerLimit   = [par0[1], par1[1], par2[1], par3[1], par4[1] ],
                                                   defaultUpperLimit   = [par0[2], par1[2], par2[2], par3[2], par4[2] ])    
        
    #=========================================================================================
    # Set histograms to the templates
    #=========================================================================================
    Print("Adding the appropriate histogram to each of the the templates", False)
    template_EWKFakeB_Baseline.setHistogram(EWK_baseline, "Inclusive") #fixme
    template_EWKFakeB_Inverted.setHistogram(EWK_inverted, "Inclusive") #fixme

    template_EWKInclusive_Baseline.setHistogram(EWK_baseline, "Inclusive")
    template_EWKInclusive_Inverted.setHistogram(EWK_inverted, "Inclusive")

    template_FakeB_Baseline.setHistogram(FakeB_baseline, "Inclusive")
    template_FakeB_Inverted.setHistogram(FakeB_inverted, "Inclusive")

    #=========================================================================================
    # Fit individual templates to histogram "Data_baseline", with custom fit options
    #=========================================================================================
    fitOptions  = "R L W 0 Q" #"R B L W 0 Q M"
    FITMIN_DATA =   80
    FITMAX_DATA = 1000
    manager.calculateNormalizationCoefficients(Data_baseline, fitOptions, FITMIN_DATA, FITMAX_DATA)
    
    Verbose("Write the normalisation factors to a python file", True)
    fileName = os.path.join(opts.mcrab, "QCDInvertedNormalizationFactors%s.py"% ( getModuleInfoString(opts) ) )
    manager.writeNormFactorFile(fileName, opts)
    
    # Not really needed to plot the histograms again
    if 1:
        saveName = fileName.replace("/", "_").replace(".py", "")

        # Draw the histograms
        plots.drawPlot(p, saveName, **GetHistoKwargs(histoName) ) #the "**" unpacks the kwargs_ 

        # Save plot in all formats
        SavePlot(p, saveName, os.path.join(opts.saveDir, "Fit") ) 
    return

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
    MERGEEWK     = True
    URL          = True
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

    # Sanity check
    if opts.mcrab == None:
        Print("Not enough arguments passed to script execution. Printing docstring & EXIT.")
        parser.print_help()
        #print __doc__
        sys.exit(1)

    # Sanity check
    if not opts.mergeEWK:
        Print("Cannot draw the histograms without the option --mergeEWK. Exit", True)
        sys.exit()

    # Call the main function
    main(opts)

    if not opts.batchMode:
        raw_input("=== plotHistograms.py: Press any key to quit ROOT ...")
