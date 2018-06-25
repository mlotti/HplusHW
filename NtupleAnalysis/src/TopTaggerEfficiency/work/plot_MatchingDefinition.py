#!/usr/bin/env python
'''
DESCRIPTION:
This scipt is used to investigate the difference in efficiency using different matching definition

USAGE:
./plot_EfficiencySystTop.py -m <pseudo_mcrab> -m2 <pseudo_multicrab2> [opts]


EXAMPLES:
./plot_EfficiencySystTop.py -m TopTaggerEfficiency_180603_SystTop_hadronic_BDTtraining_ptRew13TeV --folder topbdtSelection_ --type partonShower
./plot_EfficiencySystTop.py -m TopTaggerEfficiency_180603_SystTop_hadronic_BDTtraining_ptRew13TeV --folder topbdtSelection_ --type showerScales
./plot_EfficiencySystTop.py -m TopTaggerEfficiency_180603_SystTop_hadronic_BDTtraining_ptRew13TeV --folder topbdtSelection_ --type mTop
./plot_EfficiencySystTop.py -m TopTaggerEfficiency_180608_195638_massCut400_All --folder topbdtSelection_ --type partonShower --url
./plot_EfficiencySystTop.py -m TopTaggerEfficiency_180608_194156_massCut300_All --folder topbdtSelection_ --type partonShower --url
./plot_EfficiencySystTop.py -m TopTaggerEfficiency_180608_200027_massCut1000_All --folder topbdtSelection_ --type colourReconnection


LAST USED: 
./plot_EfficiencySystTop.py -m /uscms_data/d3/mkolosov/workspace/pseudo-multicrab/TopTaggerEfficiency/TopTaggerEfficiency_180608_200027_massCut1000_All --type showerScales 
./plot_EfficiencySystTop. py -m /uscms_data/d3/mkolosov/workspace/pseudo-multicrab/TopTaggerEfficiency/TopTaggerEfficiency_180608_200027_massCut1000_All --type highPtRadiation
./plot_EfficiencySystTop.py -m /uscms_data/d3/mkolosov/workspace/p seudo-multicrab/TopTaggerEfficiency/TopTaggerEfficiency_180608_200027_massCut1000_All --type mTop 
./plot_EfficiencySystTop.py -m /uscms_data/d3/mkolosov/workspace/pseudo-multicrab/TopTaggerEfficien cy/TopTaggerEfficiency_180608_200027_massCut1000_All --type partonShower
./plot_EfficiencySystTop.py -m /uscms_data/d3/mkolosov/workspace/pseudo-multicrab/TopTaggerEfficiency/TopTaggerEfficiency_18 0608_200027_massCut1000_All --type evtGen
./plot_EfficiencySystTop.py -m /uscms_data/d3/mkolosov/workspace/pseudo-multicrab/TopTaggerEfficiency/TopTaggerEfficiency_180608_200027_massCut1000_All --type colourReconnection


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

def GetDatasetsFromDir(opts, mcrab):
    Verbose("Getting datasets")
    
    if (not opts.includeOnlyTasks and not opts.excludeTasks):
        datasets = dataset.getDatasetsFromMulticrabDirs([mcrab],
                                                        dataEra=opts.dataEra,
                                                        searchMode=opts.searchMode, 
                                                        analysisName=opts.analysisName,
                                                        optimizationMode=opts.optMode)
    elif (opts.includeOnlyTasks):
        datasets = dataset.getDatasetsFromMulticrabDirs([mcrab],
                                                        dataEra=opts.dataEra,
                                                        searchMode=opts.searchMode,
                                                        analysisName=opts.analysisName,
                                                        includeOnlyTasks=opts.includeOnlyTasks,
                                                        optimizationMode=opts.optMode)
    elif (opts.excludeTasks):
        datasets = dataset.getDatasetsFromMulticrabDirs([mcrab],
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
    h     = histoName.lower()
    bins  = []
    units = ""
    kwargs     = {
        "xlabel"           : "x-axis",
        "ylabel"           : "Efficiency", #/ %.1f ",
        "ratioYlabel"      : "Ratio ",     #"TT/TT_X",
        "binList"          : [],
        "errorType"        : "errorPropagation", 
        "ratio"            : True,
        "ratioInvert"      : False,
        "stackMCHistograms": False,
        "addMCUncertainty" : False,
        "addLuminosityText": False,
        "addCmsText"       : True,
        "cmsExtraText"     : "Preliminary",
        "opts"             : {"ymin": 0.0, "xmax":600, "ymaxfactor": 1.2},
        "opts2"            : {"ymin": 0.6, "ymax": 1.4},
        "log"              : False,
        "moveLegend"       : {"dx": -0.25, "dy": -0.50, "dh": +0.05*(-4+opts.nDatasets)},  #"dh": +0.18}, 
        "cutBoxY"          : {"cutValue": 1.10, "fillColor": ROOT.kGray+1, "fillStyle": 3001, "box": False, "line": True, "greaterThan": True, "mainCanvas": False, "ratioCanvas": True, "mirror": True}
        }
    
    if "pt" in h:
        ROOT.gStyle.SetNdivisions(6 + 100*5 + 10000*2, "X") 
        units             = "GeV/c"
        kwargs["xlabel"]  = "p_{T} (%s)" % (units)
        bins              = [i for i in range(0, 1000+50, 50)]
        if opts.folder == "topbdtSelection_":
            #bins          = [i for i in range(0, 600+100, 100)] + [800]
            bins              = [0, 100, 150, 200, 300, 400, 500, 600, 900]
        else:
            bins          = []


    if units != "":
        kwargs["ylabel"] += (" / " + units)
    if len(bins) > 0:
        kwargs["binList"] = array.array('d', bins)
    return kwargs


def main(opts):

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    style.setOptStat(False)
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

        # Setup & configure the dataset manager for pseudo-multicrab with default matching definition
        datasetsMgr_default = GetDatasetsFromDir(opts, opts.mcrab)
        datasetsMgr_default.updateNAllEventsToPUWeighted()
        datasetsMgr_default.loadLuminosities()
        
        datasetsMgr_second = GetDatasetsFromDir(opts, opts.mcrab2)
        datasetsMgr_second.updateNAllEventsToPUWeighted()
        datasetsMgr_second.loadLuminosities()
        
        if opts.verbose:
            datasetsMgr_default.PrintCrossSections()
            datasetsMgr_default.PrintLuminosities()

        # Print datasets info summary
        datasetsMgr_default.PrintInfo()
        datasetsMgr_second.PrintInfo()
        
        Numerator = ["AllTopQuarkPt_MatchedBDT",
                     "TrijetFakePt_BDT",
                     "AllTopQuarkPt_MatchedBDT",
                     "AllTopQuarkPt_Matched",
                     ]
        Denominator = ["AllTopQuarkPt_Matched",
                       "TrijetFakePt",
                       "TopQuarkPt",
                       "TopQuarkPt",
                       ]

        eff_def = ["genuineTop",
                   "fakeTop",
                   "inclusiveTop",
                   "matching",
                   ]
        
        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        plots.mergeRenameReorderForDataMC(datasetsMgr_default) 
        plots.mergeRenameReorderForDataMC(datasetsMgr_default)
        
        counter =  0
        opts.nDatasets = len(datasetsMgr_default.getAllDatasets())
        nPlots  = len(Numerator)
        # For-loop: All numerator-denominator pairs

        for i in range(len(Numerator)):
            numerator   = os.path.join(opts.folder, Numerator[i])
            denominator = os.path.join(opts.folder, Denominator[i])
            counter+=1
            msg = "{:<9} {:>3} {:<1} {:<3} {:<50} {:<2} {:<50}".format("Histogram", "%i" % counter, "/", "%s:" % (nPlots), "%s" % (numerator), "/", "%s" % (denominator))
            Print(ShellStyles.SuccessStyle() + msg + ShellStyles.NormalStyle(), counter==1)
            PlotEfficiency(datasetsMgr_default, datasetsMgr_second, numerator, denominator, eff_def[i])
            
    Print("All plots saved under directory %s" % (ShellStyles.NoteStyle() + aux.convertToURL(opts.saveDir, opts.url) + ShellStyles.NormalStyle()), True)
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


def PlotEfficiency(datasetMgr1, datasetMgr2, numPath, denPath, eff_def):  

    # Definitions
    myList      = []
    _kwargs     = GetHistoKwargs(numPath, opts)        
    nx          = 0
    if len(_kwargs["binList"]) > 0:
        xBins   = _kwargs["binList"]
        nx      = len(xBins)-1
    counter     = 0

    dataset1 = datasetMgr1.getDataset("TT")
    dataset2 = datasetMgr2.getDataset("TT")
    
    num1 = dataset1.getDatasetRootHisto(numPath).getHistogram()
    den1 = dataset1.getDatasetRootHisto(denPath).getHistogram()
    
    num2 = dataset2.getDatasetRootHisto(numPath).getHistogram()
    den2 = dataset2.getDatasetRootHisto(denPath).getHistogram()
    
    # Rebin
    num1 = num1.Rebin(nx, "", xBins)
    den1 = den1.Rebin(nx, "", xBins)
    
    num2 = num2.Rebin(nx, "", xBins)
    den2 = den2.Rebin(nx, "", xBins)
    
    # Calculations    
    total1    = den1.Integral(0, den1.GetXaxis().GetNbins()+1)
    selected1 = num1.Integral(0, num1.GetXaxis().GetNbins()+1)
    print "Numerical Efficiency for default matching (1) = ", numPath, dataset1.getName(), ":", round(selected1/total1, 3)
    
    total2    = den2.Integral(0, den2.GetXaxis().GetNbins()+1)
    selected2 = num2.Integral(0, num2.GetXaxis().GetNbins()+1)
    print "Numerical Efficiency for second matching (2) = ", numPath, dataset2.getName(), ":", round(selected2/total2, 3)
        
    # Create Efficiency plots with Clopper-Pearson stats
    eff1 = ROOT.TEfficiency(num1, den1) 
    eff1.SetStatisticOption(ROOT.TEfficiency.kFCP) #FCP
    
    eff2 = ROOT.TEfficiency(num2, den2) 
    eff2.SetStatisticOption(ROOT.TEfficiency.kFCP) #FCP
    
    # Convert to TGraph
    gEff1 = convert2TGraph(eff1)
    gEff2 = convert2TGraph(eff2)
            
    # Apply styles
    styles.ttStyle.apply(gEff1)
    #styles.signalStyleHToTB500.apply(gEff2)
    
    
    legend = "t#bar{t} (#Delta R < 0.30, #Delta p_{T} / p_{T} < 0.32)"
    legend_DR = "t#bar{t} (#Delta R < 0.30)"
    
    Graph1 = histograms.HistoGraph(gEff1, legend, "p", "P")
    Graph2 = histograms.HistoGraph(gEff2, legend_DR, "lp", "P")
    
    # Define stuff
    saveName = "Efficiency_%s_MatchingDefinition_%s" % (eff_def, numPath.split("/")[-1])
   
    # Plot the efficiency
    p = plots.ComparisonManyPlot(Graph1, [Graph2], saveFormats=[])
    savePath = os.path.join(opts.saveDir, opts.optMode)    
    plots.drawPlot(p, savePath, **_kwargs)

    # Save plot in all formats
    SavePlot(p, saveName, savePath, saveFormats = [".png", ".pdf", ".C"])
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


def SavePlot(plot, plotName, saveDir, saveFormats = [".C", ".png", ".pdf"]):
    Verbose("Saving the plot in %s formats: %s" % (len(saveFormats), ", ".join(saveFormats) ) )

     # Check that path exists
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)

    # Create the name under which plot will be saved
    saveName = os.path.join(saveDir, plotName.replace("/", "_"))

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
    ANALYSISNAME = "TopTaggerEfficiency"
    SEARCHMODE   = "80to1000"
    DATAERA      = "Run2016"
    OPTMODE      = ""
    BATCHMODE    = True
    PRECISION    = 3
    INTLUMI      = -1.0
    URL          = False
    SAVEDIR      = None
    VERBOSE      = False
    NORMALISE    = False
    FOLDER       = "topbdtSelection_"
    
    # Define the available script options
    parser = OptionParser(usage="Usage: %prog [options]")

    parser.add_option("-m", "--mcrab", dest="mcrab", action="store", 
                      help="Path to the multicrab directory for input")

    parser.add_option("-s", "--mcrab2", dest="mcrab2", action="store", 
                      help="Path to the second multicrab directory for input")
    
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

    parser.add_option("-n", "--normaliseToOne", dest="normaliseToOne", action="store_true", 
                      help="Normalise the histograms to one? [default: %s]" % (NORMALISE) )

    parser.add_option("--folder", dest="folder", type="string", default = FOLDER,
                      help="ROOT file folder under which all histograms to be plotted are located [default: %s]" % (FOLDER) )

    (opts, parseArgs) = parser.parse_args()

    # Require at least two arguments (script-name, path to multicrab)
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    if opts.mcrab == None or opts.mcrab2 == None:
        Print("Not enough arguments passed to script execution. Printing docstring & EXIT.")
        parser.print_help()
        #print __doc__
        sys.exit(1)

    # Append folder to save directory path
    if opts.saveDir == None:
        opts.saveDir = aux.getSaveDirPath(opts.mcrab, prefix="", postfix="TopTagSystematics")

    # Call the main function
    main(opts)

    if not opts.batchMode:
        raw_input("=== plot_MatchinDefinition.py: Press any key to quit ROOT ...")
