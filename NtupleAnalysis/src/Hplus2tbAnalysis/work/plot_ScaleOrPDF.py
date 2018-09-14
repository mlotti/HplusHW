#!/usr/bin/env python
'''
DESCRIPTION:
Comparison of datasets with different PDF weights.
The first multicrab in the input list is used as the reference multicrab (nominal)
The envelope of the ratio plot should serve as the estimate of the 
Scale/PDF acceptance systematic error associated with the given dataset and this 
specific analysis.

USAGE:
./plot_ScaleOrPDF.py -m <pseudo_mcrab> [opts]


EXAMPLES:
./plot_ScaleOrPDF.py -m Hplus2tbAnalysis_Weight_1,Hplus2tbAnalysis_Weight_2,Hplus2tbAnalysis_Weight_3,Hplus2tbAnalysis_Weight_4,Hplus2tbAnalysis_Weight_6,Hplus2tbAnalysis_Weight_8 --url --prefix QCDScale

./plot_ScaleOrPDF.py -m Hplus2tbAnalysis_Weight_9,Hplus2tbAnalysis_Weight_10,Hplus2tbAnalysis_Weight_12,Hplus2tbAnalysis_Weight_16,Hplus2tbAnalysis_Weight_23,Hplus2tbAnalysis_Weight_27,Hplus2tbAnalysis_Weight_32,Hplus2tbAnalysis_Weight_46,Hplus2tbAnalysis_Weight_59,Hplus2tbAnalysis_Weight_63,Hplus2tbAnalysis_Weight_77,Hplus2tbAnalysis_Weight_80,Hplus2tbAnalysis_Weight_96 --url --prefix PDF --bandValue 1.8


LAST USED:
./plot_ScaleOrPDF.py -m Hplus2tbAnalysis_Weight_9,Hplus2tbAnalysis_Weight_10,Hplus2tbAnalysis_Weight_12,Hplus2tbAnalysis_Weight_16,Hplus2tbAnalysis_Weight_23,Hplus2tbAnalysis_Weight_27,Hplus2tbAnalysis_Weight_32,Hplus2tbAnalysis_Weight_46,Hplus2tbAnalysis_Weight_59,Hplus2tbAnalysis_Weight_63,Hplus2tbAnalysis_Weight_77,Hplus2tbAnalysis_Weight_80,Hplus2tbAnalysis_Weight_96 --url --prefix PDF && ./plot_PDFweights.py -m Hplus2tbAnalysis_Weight_1,Hplus2tbAnalysis_Weight_2,Hplus2tbAnalysis_Weight_3,Hplus2tbAnalysis_Weight_4,Hplus2tbAnalysis_Weight_6,Hplus2tbAnalysis_Weight_8 --url --prefix QCDScale --bandValue 3

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
import HiggsAnalysis.NtupleAnalysis.tools.systematics as systematics
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.crosssection as xsect
import HiggsAnalysis.NtupleAnalysis.tools.multicrabConsistencyCheck as consistencyCheck
import HiggsAnalysis.NtupleAnalysis.tools.ShellStyles as ShellStyles
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux

ROOT.gErrorIgnoreLevel = ROOT.kError
#================================================================================================ 
# Function Definition
#================================================================================================ 
def GetLumi(datasetsMgr):
    
    lumi = 0.0
    for d in datasetsMgr.getAllDatasets():
        if d.isMC():
            continue
        else:
            lumi += d.getLuminosity()
    aux.Verbose("Luminosity = %s (pb)" % (lumi), True)
    return lumi


def GetDatasetsFromDir(opts, i):

    aux.Verbose("multicrab = \"%s\"" % (opts.mcrabs[i]), i==0)

    if (not opts.includeOnlyTasks and not opts.excludeTasks):
        datasets = dataset.getDatasetsFromMulticrabDirs([opts.mcrabs[i]],
                                                        dataEra=opts.dataEra,
                                                        searchMode=opts.searchMode, 
                                                        analysisName=opts.analysisName,
                                                        optimizationMode=opts.optMode)
    elif (opts.includeOnlyTasks):
        datasets = dataset.getDatasetsFromMulticrabDirs([opts.mcrabs[i]],
                                                        dataEra=opts.dataEra,
                                                        searchMode=opts.searchMode,
                                                        analysisName=opts.analysisName,
                                                        includeOnlyTasks=opts.includeOnlyTasks,
                                                        optimizationMode=opts.optMode)
    elif (opts.excludeTasks):
        datasets = dataset.getDatasetsFromMulticrabDirs([opts.mcrabs[i]],
                                                        dataEra=opts.dataEra,
                                                        searchMode=opts.searchMode,
                                                        analysisName=opts.analysisName,
                                                        excludeTasks=opts.excludeTasks,
                                                        optimizationMode=opts.optMode)
    else:
        raise Exception("This should never be reached")
    return datasets
    

def GetHistoKwargs(h, opts):

    units = "GeV" #GeV/c^{2}
    cutY  = 1.0 + opts.bandValue/100.0
    
    if "scale" in opts.prefix.lower():
        dh = 0.05
    elif  "pdf" in opts.prefix.lower():
        dh = 0.25
    else:
        dh = 0.0

    kwargs = {
        "ylabel"           : "< Events / %s > " % units,
        "xlabel"           : "m_{jjbb} (%s)" % units,
        "rebinX"           : systematics._dataDrivenCtrlPlotBinning["LdgTetrajetMass_AfterAllSelections"],
        "rebinY"           : None,
        "ratioYlabel"      : "Ratio ",
        "ratio"            : True,
        "ratioCreateLegend": True,
        "ratioType"        : "errorPropagation", #"errorScale",
        "divideByBinWidth" : True,
        "ratioErrorOptions": {"numeratorStatSyst": False},
        "ratioMoveLegend"  : {"dx": -0.35, "dy": -0.05, "dh": 0.0},
        "ratioInvert"      : False,
        "addMCUncertainty" : False,
        "addLuminosityText": True,
        "addCmsText"       : True,
        "cmsExtraText"     : "Preliminary",
        "opts"             : {"ymin": 1e-2, "ymaxfactor": 2.0},
        "opts2"            : {"ymin": 0.9, "ymax": 1.1},
        "log"              : True,
        "moveLegend"       : {"dx": -0.08, "dy": -0.02, "dh": dh},
        "cutBox"           : {"cutValue": 500.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True},
        "cutBoxY"          : {"cutValue": cutY, "fillColor": ROOT.kBlack, "fillStyle": 3844, "box": False, "line": True, "greaterThan": False, "mainCanvas": False, "ratioCanvas": True, "mirror": True}
        #"cutBoxY"          : {"cutValue": opts.bandValue, "fillColor": ROOT.kBlack, "fillStyle": 3944, "box": True, "line": False, "greaterThan": False, "mainCanvas": False, "ratioCanvas": True, "mirror": True}
        }
    return kwargs


def main(opts):

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    style.setOptStat(False)
    style.setGridX(False)
    style.setGridY(False)

    # Setup & configure the dataset manager 
    datasetsMgr = GetDatasetsFromDir(opts, 0)
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
    if 1:
        plots.mergeRenameReorderForDataMC(datasetsMgr) 

    # Print datasets info summary
    datasetsMgr.PrintInfo()

    # Define the mapping histograms in numerator->denominator pairs
    VariableList = ["TetrajetMass"]

    counter =  0
    opts.nDatasets = len(datasetsMgr.getAllDatasets())
    nPlots  = len(VariableList)*opts.nDatasets

    # For-loop: All datasets
    for dataset in datasetsMgr.getAllDatasets():
        # For-looop: All variables
        for hName in VariableList:
            hPath = os.path.join(opts.folder, hName)

            counter+=1
            msg = "{:<9} {:>3} {:<1} {:<3} {:<50}".format("Histogram", "%i" % counter, "/", "%s:" % (nPlots), "%s" % (dataset.getName()))
            aux.Print(ShellStyles.SuccessStyle() + msg + ShellStyles.NormalStyle(), counter==1)
        
            PlotHistos(dataset.getName(), hPath) # For each dataset: Plot histos from different multicrabs on same canvas

    aux.Print("All plots saved under directory %s" % (ShellStyles.NoteStyle() + aux.convertToURL(opts.saveDir, opts.url) + ShellStyles.NormalStyle()), True)
    return
            

def PlotHistos(datasetName, hPath):


    _kwargs = GetHistoKwargs(hPath, opts)
    datasetsMgr_list = []

    j = 0
    histoList = []

    # For-loop: All pseudo-multicrabs
    while j < len(opts.mcrabs):

        textweight =  opts.mcrabs[j].split("_")[-1]

        dMgr = GetDatasetsFromDir(opts, j)
        dMgr.updateNAllEventsToPUWeighted()
        dMgr.loadLuminosities() # from lumi.json

       # Set/Overwrite cross-sections
        if  "ChargedHiggs" in datasetName:
            dMgr.getDataset(datasetName).setCrossSection(1.0)
                
        # Get dataset
        dataset = dMgr.getDataset(datasetName)

        # Get Histogram from dataset
        histo = dataset.getDatasetRootHisto(hPath).getHistogram()                

        # Set style
        styles.styles[j].apply(histo) 
        
        if (j == 0):
            # refHisto = histograms.Histo(histo, "Nominal", legendStyle = "F", drawStyle="HIST")
            # refHisto.getRootHisto().SetFillStyle(1001)
            # refHisto.getRootHisto().SetFillColor(ROOT.kBlue)
            refHisto = histograms.Histo(histo, "Nominal", legendStyle = "L", drawStyle="HIST")
            refHisto.getRootHisto().SetLineStyle(ROOT.kSolid)
            refHisto.getRootHisto().SetLineWidth(3)
        else:
            text = str(j)
            histoList.append(histograms.Histo(histo, "Weight " + textweight, legendStyle = "LP", drawStyle="AP"))
        j = j + 1

    # Create the plotter object 
    p = plots.ComparisonManyPlot(refHisto, histoList, saveFormats=[])
    p.setLuminosity(opts.intLumi)
    p.setLegendHeader(plots._legendLabels[datasetName])

    # Draw the plots
    plots.drawPlot(p, opts.saveDir, **_kwargs)
    
    # Add text
    if 0:
        histograms.addText(0.65, 0.1, "#\pm %.1f %% band" % (opts.bandValue), 20)

    # Save plot in all formats
    saveName = hPath.split("/")[-1] + "_" + datasetName
    SavePlot(p, saveName, opts.saveDir, saveFormats = [".png", ".pdf", ".C"])
    return

def SavePlot(plot, plotName, saveDir, saveFormats = [".C", ".png", ".pdf"]):

     # Check that path exists
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)

    # Create the name under which plot will be saved
    saveName = os.path.join(saveDir, plotName.replace("/", "_"))

    # For-loop: All save formats
    for i, ext in enumerate(saveFormats):
        saveNameURL = saveName + ext
        saveNameURL = aux.convertToURL(saveNameURL, opts.url)
        aux.Verbose(saveNameURL, i==0)
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
    ANALYSISNAME = "Hplus2tbAnalysis"
    SEARCHMODE   = "80to1000"
    DATAERA      = "Run2016"
    OPTMODE      = ""
    BATCHMODE    = True
    PRECISION    = 3
    INTLUMI      = 35900
    URL          = False
    SAVEDIR      = None
    VERBOSE      = False
    NORMALISE    = False
    FOLDER       = "topSelectionBDT_"
    PREFIX       = ""
    POSTFIX      = ""
    BANDVALUE    = 5.0
        
    # Define the available script options
    parser = OptionParser(usage="Usage: %prog [options]")

    parser.add_option("-m", "--mcrabs", dest="mcrabs", action="store", 
                      help="Path to the multicrab directories for input")

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

    parser.add_option("--prefix", dest="prefix", type="string", default = PREFIX,
                      help="Prefix string to be appended on save directory [default: %s]" % (PREFIX) )

    parser.add_option("--postfix", dest="postfix", type="string", default = POSTFIX,
                      help="Postfix string to be appended on save directory [default: %s]" % (POSTFIX) )

    parser.add_option("--bandValue", dest="bandValue", type="float", default=BANDVALUE,
                      help="Add a symmetric band around 1.0. Value passed should be the percentage (e.g 10 or 5)  [default: %s]" % (BANDVALUE) )

    (opts, parseArgs) = parser.parse_args()

    # Require at least two arguments (script-name, path to multicrab)
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    if len(opts.mcrabs) == 0:
        aux.Print("Not enough arguments passed to script execution. Printing docstring & EXIT.")
        parser.print_help()
        #print __doc__
        sys.exit(1)

    # Store all (comma-separated) pseudomulticrabs in a list
    if opts.mcrabs == None:
        aux.Print("Not enough arguments passed to script execution. Printing docstring & EXIT.")
        parser.print_help()
        sys.exit(1)
    else:
        if "," in opts.mcrabs:
            opts.mcrabs = opts.mcrabs.split(",")    
        else:
            cwd  = os.getcwd()
            dirs = [ name for name in os.listdir(cwd) if os.path.isdir(os.path.join(cwd, name)) ]
            mcrabs = [d for d in dirs if opts.mcrabs in d and "Top" in d]
            opts.mcrabs = mcrabs


    # For-loop: All pseudomulticrab dirs
    for mcrab in opts.mcrabs:
        if not os.path.exists("%s/multicrab.cfg" % mcrab):
            msg = "No pseudo-multicrab directory found at path '%s'! Please check path or specify it with --mcrab!" % (mcrab)
            raise Exception(ShellStyles.ErrorLabel() + msg + ShellStyles.NormalStyle())
        else:
            msg = "Using pseudo-multicrab directory %s" % (ShellStyles.NoteStyle() + mcrab + ShellStyles.NormalStyle())
            aux.Verbose(msg , True)

    # Append folder to save directory path
    if opts.saveDir == None:
        opts.saveDir = aux.getSaveDirPath(opts.mcrabs[0] + "to" + opts.mcrabs[-1].split("_")[-1], prefix=opts.prefix, postfix=opts.postfix)

    # Call the main function
    main(opts)

    if not opts.batchMode:
        raw_input("=== plot_EfficiencySystTop.py: Press any key to quit ROOT ...")
