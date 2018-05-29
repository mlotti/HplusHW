#!/usr/bin/env python
'''
DESCRIPTION:
https://twiki.cern.ch/twiki/bin/view/CMS/HPlus2tbHadronicResolvedQA2018


USAGE:
./plotMC_TopPtReweighting.py -m <pseudo_mcrab> [opts]


EXAMPLES:
./plotMC_TopPtReweighting.py -m TopRecoAnalysis_180524_PtReweighting


LAST USED:
./plotMC_TopPtReweighting.py -m TopRecoAnalysis_180524_PtReweighting --url -n --eight
./plotMC_TopPtReweighting.py -m TopRecoAnalysis_180524_PtReweighting --url -n

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


def main(opts):

    optModes = [""]

    if opts.optMode != None:
        optModes = [opts.optMode]

    # For-loop: All optimisation modes
    for opt in optModes:
        opts.optMode = opt

        dir = opts.mcrab
        lastdir = dir.split("/")[-1]
        dir = dir + "/"+lastdir.replace("_PtReweighting","")

        #TopRecoAnalysis_180524_PtReweighting/
        # Setup & configure the dataset manager 
        datasetsMgr_Mcrab905_noTopPtRew = GetDatasetsFromDir_second(opts, dir+"_Mcrab905_noTopPtRew")
        datasetsMgr_Mcrab905_noTopPtRew.updateNAllEventsToPUWeighted()
        datasetsMgr_Mcrab905_noTopPtRew.loadLuminosities() # from lumi.json

        datasetsMgr_Mcrab905_TopPtRew = GetDatasetsFromDir_second(opts, dir+"_Mcrab905_TopPtRew")
        datasetsMgr_Mcrab905_TopPtRew.updateNAllEventsToPUWeighted()
        datasetsMgr_Mcrab905_TopPtRew.loadLuminosities() # from lumi.json

        datasetsMgr_Mcrab644_noTopPtRew = GetDatasetsFromDir_second(opts, dir+"_Mcrab644_noTopPtRew")
        datasetsMgr_Mcrab644_noTopPtRew.updateNAllEventsToPUWeighted()
        datasetsMgr_Mcrab644_noTopPtRew.loadLuminosities() # from lumi.json

        datasetsMgr_Mcrab644_TopPtRew = GetDatasetsFromDir_second(opts, dir+"_Mcrab644_TopPtRew")
        datasetsMgr_Mcrab644_TopPtRew.updateNAllEventsToPUWeighted()
        datasetsMgr_Mcrab644_TopPtRew.loadLuminosities() # from lumi.json

        if opts.verbose:
            datasetsMgr_Mcrab644_TopPtRew.PrintCrossSections()
            datasetsMgr_Mcrab644_TopPtRew.PrintLuminosities()

        # Set/Overwrite cross-sections
        for d in datasetsMgr_Mcrab644_TopPtRew.getAllDatasets():
            if "TT" in d.getName():
                datasetsMgr_Mcrab644_TopPtRew.getDataset(d.getName()).setCrossSection(1.0)
                datasetsMgr_Mcrab644_noTopPtRew.getDataset(d.getName()).setCrossSection(1.0)
                datasetsMgr_Mcrab905_TopPtRew.getDataset(d.getName()).setCrossSection(1.0)
                datasetsMgr_Mcrab905_noTopPtRew.getDataset(d.getName()).setCrossSection(1.0)

            else:
                datasetsMgr_Mcrab644_TopPtRew.remove(d.getName())
                datasetsMgr_Mcrab644_noTopPtRew.remove(d.getName())
                datasetsMgr_Mcrab905_TopPtRew.remove(d.getName())
                datasetsMgr_Mcrab905_noTopPtRew.remove(d.getName())
                
        # Determine integrated Lumi before removing data
        if "Data" in datasetsMgr_Mcrab644_TopPtRew.getAllDatasetNames():
            opts.intLumi = datasetsMgr.getDataset("Data").getLuminosity()
        else:
            opts.intLumi = 35920

        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        plots.mergeRenameReorderForDataMC(datasetsMgr_Mcrab644_TopPtRew) 
        plots.mergeRenameReorderForDataMC(datasetsMgr_Mcrab644_noTopPtRew) 
        plots.mergeRenameReorderForDataMC(datasetsMgr_Mcrab905_TopPtRew) 
        plots.mergeRenameReorderForDataMC(datasetsMgr_Mcrab905_noTopPtRew) 

        # Re-order datasets
        datasetOrder = []
        for d in datasetsMgr_Mcrab644_TopPtRew.getAllDatasets():
            datasetOrder.append(d.getName())

        # Print dataset information
        datasetsMgr_Mcrab644_TopPtRew.PrintInfo()

        # Apply TDR style
        style = tdrstyle.TDRStyle()
        style.setGridX(False)
        style.setGridY(False)

        # Do the histograms
        PlotHistograms(datasetsMgr_Mcrab644_TopPtRew, datasetsMgr_Mcrab644_noTopPtRew, datasetsMgr_Mcrab905_TopPtRew, datasetsMgr_Mcrab905_noTopPtRew)

        #Print("All plots saved under directory %s" % (ShellStyles.NoteStyle() + aux.convertToURL(opts.saveDir, opts.url) + ShellStyles.NormalStyle()), True)
    return

def getHistos(datasetsMgr, histoName):

    h1 = datasetsMgr.getDataset("Data").getDatasetRootHisto(histoName)
    h1.setName("Data")

    h2 = datasetsMgr.getDataset("EWK").getDatasetRootHisto(histoName)
    h2.setName("EWK")
    return [h1, h2]

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
        Print(saveNameURL, i==0)
        plot.saveAs(saveName, formats=saveFormats)
    return

def PlotHistograms(datasetsMgr_Mcrab644_TopPtRew, datasetsMgr_Mcrab644_noTopPtRew, datasetsMgr_Mcrab905_TopPtRew, datasetsMgr_Mcrab905_noTopPtRew):

    # Definitions
    kwargs = {}
    histos = []

    # For-loop: All histos in list
    dName =  "TT"

    # Multicrab *644, top pt reweighting:
    p0 = plots.MCPlot(datasetsMgr_Mcrab644_TopPtRew, "Analysis_/TopQuarkPt", normalizeToLumi=opts.intLumi, saveFormats=[], **kwargs)
    h_Mcrab644_TopPtRew = p0.histoMgr.getHisto(dName).getRootHisto().Clone("Mcrab644-ptRew")
    histos.append(h_Mcrab644_TopPtRew)

    # Multicrab *644, no top pt reweighting:
    p1 = plots.MCPlot(datasetsMgr_Mcrab644_noTopPtRew, "Analysis_/TopQuarkPt", normalizeToLumi=opts.intLumi, saveFormats=[], **kwargs)
    h_Mcrab644_noTopPtRew = p1.histoMgr.getHisto(dName).getRootHisto().Clone("Mcrab644-noptRew")
    histos.append(h_Mcrab644_noTopPtRew)

    # Multicrab *905, top pt reweighting:
    p2 = plots.MCPlot(datasetsMgr_Mcrab905_TopPtRew, "Analysis_/TopQuarkPt", normalizeToLumi=opts.intLumi, saveFormats=[], **kwargs)
    h_Mcrab905_TopPtRew = p2.histoMgr.getHisto(dName).getRootHisto().Clone("Mcrab905-ptRew")
    histos.append(h_Mcrab905_TopPtRew)

    # Multicrab *905, no top pt reweighting:
    p3 = plots.MCPlot(datasetsMgr_Mcrab905_noTopPtRew, "Analysis_/TopQuarkPt", normalizeToLumi=opts.intLumi, saveFormats=[], **kwargs)
    h_Mcrab905_noTopPtRew = p3.histoMgr.getHisto(dName).getRootHisto().Clone("Mcrab905-noptRew")
    histos.append(h_Mcrab905_noTopPtRew)

    # Normalise histos
    for h in histos:
        if opts.normaliseToOne:
            h = h.Scale(1/h.Integral())

    # Make comparison plot
    if opts.eight:
        p = plots.ComparisonManyPlot(h_Mcrab905_TopPtRew, [ h_Mcrab905_noTopPtRew], saveFormats=[])
    else:
        p = plots.ComparisonManyPlot(h_Mcrab644_TopPtRew, [h_Mcrab644_noTopPtRew], saveFormats=[])
    p.setLuminosity(opts.intLumi)

    # Overwite signal style?
    if opts.eight:
        p.histoMgr.forHisto("Mcrab905-ptRew"  , styles.getABCDStyle("SR"))
        p.histoMgr.forHisto("Mcrab905-noptRew", styles.getABCDStyle("VR"))
    else:
        p.histoMgr.forHisto("Mcrab644-ptRew"  , styles.getABCDStyle("SR"))
        p.histoMgr.forHisto("Mcrab644-noptRew", styles.getABCDStyle("VR"))
        
    # Set draw style
    if opts.eight:
        p.histoMgr.setHistoDrawStyle("Mcrab905-noptRew", "HIST")
        p.histoMgr.setHistoDrawStyle("Mcrab905-ptRew", "AP")
    else:
        p.histoMgr.setHistoDrawStyle("Mcrab644-noptRew", "HIST")
        p.histoMgr.setHistoDrawStyle("Mcrab644-ptRew", "AP")

    # Set legend style
    if opts.eight:
        p.histoMgr.setHistoLegendStyle("Mcrab905-noptRew", "F")
        p.histoMgr.setHistoLegendStyle("Mcrab905-ptRew", "LP")
    else:
        p.histoMgr.setHistoLegendStyle("Mcrab644-noptRew", "F")
        p.histoMgr.setHistoLegendStyle("Mcrab644-ptRew", "LP")

    if opts.eight:
        p.histoMgr.setHistoLegendLabelMany({
                "Mcrab905-ptRew"           : "p_{T} reweight (8 TeV)",
                "Mcrab905-noptRew"         : "Default",
                })
    else:
        p.histoMgr.setHistoLegendLabelMany({
                "Mcrab644-ptRew"           : "p_{T} reweight (13 TeV)",
                "Mcrab644-noptRew"         : "Default",
                })
    
    
    # Draw customised plot
    if opts.eight:
        saveName = "TopQuarkPt_PtReweight_8TeV"
    else:
        saveName = "TopQuarkPt_PtReweight_13TeV"
    _units   = "GeV/c"
    _leg     = {"x1": 0.55, "y1": 0.75, "x2": 0.85, "y2": 0.87}

    if opts.normaliseToOne:
        yLabel = "Arbitrary Units / %0.0f " + _units
    else:
        yLabel = "Events / %0.0f " + _units

    plots.drawPlot(p, 
                   saveName,
                   xlabel            = "generated top p_{T} (%s)" % (_units),
                   ylabel            = yLabel,
                   log               = False,
                   rebinX            = 2,
                   cmsExtraText      = "Preliminary",
                   ratio             = True,
                   ratioType         = "errorPropagation", #"errorScale", "binomial"
                   divideByBinWidth  =  False,
                   ratioErrorOptions = {"numeratorStatSyst": False, "denominatorStatSyst": True},
                   ratioMoveLegend   =  {"dx": +0.21, "dy": 0.03, "dh": -0.08},
                   ratioYlabel       = "Ratio ",
                   createLegend      = _leg,
                   opts              = {"xmin": 0.0, "xmax": 800.0, "ymin": 0.0, "ymaxfactor": 1.2},
                   opts2             = {"ymin": 0.6, "ymax": 1.4},
                   cutBox            = {"cutValue": 0.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
                   )

    # Save plot in all formats    
    savePath = os.path.join(opts.saveDir, opts.optMode)
    SavePlot(p, saveName, savePath) 
    return


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
        Print(saveNameURL, i==0)
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
    SEARCHMODE   = "80to1000"
    DATAERA      = "Run2016"
    OPTMODE      = ""
    BATCHMODE    = True
    INTLUMI      = -1.0
    URL          = False
    VERBOSE      = False
    EIGHTTEV     = False
    NORMALISE    = False
    ANALYSISNAME = "TopRecoAnalysis"
    SAVEDIR      = "/publicweb/%s/%s/%s" % (getpass.getuser()[0], getpass.getuser(), ANALYSISNAME)


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

    parser.add_option("--eight", dest="eight", action="store_true", default=EIGHTTEV,
                      help="Do 8 TeV instead of 13 TeV ? [default: %s]" % EIGHTTEV)

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
        raw_input("=== plotMC_InvMassSmearing.py: Press any key to quit ROOT ...")
