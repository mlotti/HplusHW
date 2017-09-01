#!/usr/bin/env python
'''
Description:
Script for plotting TH2 plots

Useful Link:
https://nixtricks.wordpress.com/2011/03/03/simple-loops-in-csh-ortcsh/

Usage:
./plot_Kinematics2d.py -m <pseudo_mcrab_directory> [opts]

Examples:
./plot_Kinematics2d.py -m Kinematics_FullStats_170831_085353 --url --mergeEWK -e "JetHT"

Last Used:
./plot_Kinematics2d.py -m Kinematics_FullStats_170831_085353 --url --mergeEWK -e "JetHT"

Obsolete:
foreach x ( 180 200 220 250 300 350 400 500 800 1000 2000 3000 )
./plot_Kinematics2d.py -m Hplus2tbAnalysis_StdSelections_TopCut100_AllSelections_NoTrgMatch_TopCut10_H2Cut0p5_170826_073257/ -i M_$x --url
end

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

#================================================================================================ 
# Function Definition
#================================================================================================ 
def GetLumi(datasetsMgr):
    '''
    '''
    lumi = 0.0
    for d in datasetsMgr.getAllDatasets():
        if d.isMC():
            continue
        else:
            #print "dataset = %s, lumi = %s" % (d.getName(), lumi)
            lumi += d.getLuminosity()
    #print "Luminosity = %s (pb)" % (lumi), True)
    return lumi

def GetListOfEwkDatasets():
    return  ["TT", "WJetsToQQ_HT_600ToInf", "SingleTop", "DYJetsToQQHT", "TTZToQQ",  "TTWJetsToQQ", "Diboson", "TTTT"]

def GetDatasetsFromDir(opts):
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

def GetAllDatasetsFromDir(opts):
    datasets = dataset.getDatasetsFromMulticrabDirs([opts.mcrab],
                                                    dataEra=opts.dataEra,
                                                    searchMode=opts.searchMode, 
                                                    analysisName=opts.analysisName,
                                                    optimizationMode=opts.optMode)
    return datasets
    
def main(opts):

    optModes = [""]
    if opts.optMode != None:
        optModes = [opts.optMode]
        
    # For-loop: All optimisation modes
    for opt in optModes:
        opts.optMode = opt

        # Quick and dirty way to get total int lumi
        allDatasetsMgr = GetAllDatasetsFromDir(opts)
        allDatasetsMgr.updateNAllEventsToPUWeighted()
        allDatasetsMgr.loadLuminosities() # from lumi.json
        plots.mergeRenameReorderForDataMC(allDatasetsMgr) 
        opts.intLumi = GetLumi(allDatasetsMgr)

        # Setup & configure the dataset manager 
        datasetsMgr    = GetDatasetsFromDir(opts)
        datasetsMgr.updateNAllEventsToPUWeighted()
        datasetsMgr.loadLuminosities() # from lumi.json

        # Set/Overwrite cross-sections
        for d in datasetsMgr.getAllDatasets():
            if "ChargedHiggs" in d.getName():
                datasetsMgr.getDataset(d.getName()).setCrossSection(1.0) # ATLAS 13 TeV H->tb exclusion limits
            
        if opts.verbose:
            datasetsMgr.PrintCrossSections()
            datasetsMgr.PrintLuminosities()

        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        plots.mergeRenameReorderForDataMC(datasetsMgr) 

        # Print dataset information
        datasetsMgr.PrintInfo()

        # Merge EWK samples
        if opts.mergeEWK:
            datasetsMgr.merge("EWK", GetListOfEwkDatasets())
            plots._plotStyles["EWK"] = styles.getAltEWKStyle()

        # Apply TDR style
        style = tdrstyle.TDRStyle()
        style.setOptStat(True)
        style.setWide(True, 0.15)
        # style.setPadRightMargin()#0.13)

        # Do 2D histos
        histoNames  = []
        saveFormats = [".png"] #[".C", ".png", ".pdf"]
        histoList   = datasetsMgr.getDataset(datasetsMgr.getAllDatasetNames()[0]).getDirectoryContent(opts.folder)
        histoPaths  = [opts.folder +"/" + h for h in histoList]
        histoKwargs = GetHistoKwargs(histoPaths)

        # Axes divisions!
        ROOT.gStyle.SetNdivisions(5, "X")
        ROOT.gStyle.SetNdivisions(5, "Y")

        # For-loop: All datasets
        for d in datasetsMgr.getAllDatasetNames():
            # For-loop: All histogram
            for histoName in histoPaths:
                Plot2d(datasetsMgr, d, histoName, histoKwargs[histoName], opts)
                for o in gROOT.GetListOfCanvases():
                    # print o.GetName()
                    o.SetName(o.GetName() + "_" + d)

    return

def GetHistoKwargs(histoList):
    '''
    Dictionary with 
    key   = histogramName
    value = kwargs
    '''
    
    histoKwargs = {}
    
    # Defaults
    logX        = False
    rebinX      = 1
    labelX      = "m_{jjb} p_{T} (GeV/c)"
    logY        = False
    gridX       = True
    rebinY      = 1
    labelY      = "m_{jj} p_{T} (GeV/c)"
    gridY       = True
    _moveLegend = {"dx": -0.1, "dy": -0.01, "dh": 0.1}
    xMin        =   0
    xMax        =  10
    yMin        =   0
    yMax        =  10
    zMin        =   1
    zMax        = 1e5
    normToOne   = True

    kwargs = {
        "xlabel"           : labelX,
        "ylabel"           : labelY,
        "rebinX"           : 1,
        "rebinY"           : 1,
        "normalizeToOne"   : normToOne,
        "stackMCHistograms": False,
        "addMCUncertainty" : False,
        "addLuminosityText": True, #(not normToOne),
        "addCmsText"       : True,
        "cmsExtraText"     : "Preliminary",
        "logX"             : logX,
        "logY"             : logY,
        "moveLegend"       : _moveLegend,
        "gridX"            : gridX,
        "gridY"            : gridY,
        "xmin"             : xMin,
        "xmax"             : xMax,
        "ymin"             : yMin,
        "ymax"             : yMax,
        "zmin"             : zMin,
        "zmax"             : zMax,        
        }
    
    for h in histoList:

        if "TH2_S_Vs_Y" in h:
            pass
        if "TH2_BQuarkPair_dRMin_Eta1_Vs_Eta2" in h:
            pass
        if "TH2_BQuarkPair_dRMin_Phi1_Vs_Phi2" in h:
            pass
        if "TH2_BQuarkPair_dRMin_Pt1_Vs_Pt2" in h:
            pass
        if "TH2_BQuarkPair_dRMin_dEta_Vs_dPhi" in h:
            pass
        if "TH2_Jet1Jet2_dEta_Vs_Jet3Jet4_dEta" in h:
            pass
        if "TH2_Jet1Jet2_dPhi_Vs_Jet3Jet4_dPhi" in h:
            pass
        if "TH2_Jet1Jet2_dEta_Vs_Jet1Jet2_Mass" in h:
            pass
        if "TH2_Jet3Jet4_dEta_Vs_Jet3Jet4_Mass" in h:
            pass
        if "TH2_MaxDiJetMass_dEta_Vs_dPhi" in h:
            pass
        if "TH2_MaxDiJetMass_dRap_Vs_dPhi" in h:
            pass
        if "BQuark1_BQuark2_dEta_Vs_dPhi" in h:
            print "*"*100
            kwargs["xmax"] = 5
        if "TH2_BQuark1_BQuark3_dEta_Vs_dPhi" in h:
            pass
        if "TH2_BQuark1_BQuark4_dEta_Vs_dPhi" in h:
            pass
        if "TH2_BQuark2_BQuark3_dEta_Vs_dPhi" in h:
            pass
        if "TH2_BQuark2_BQuark4_dEta_Vs_dPhi" in h:
            pass
        if "TH2_BQuark3_BQuark4_dEta_Vs_dPhi" in h:
            pass
        histoKwargs[h] = kwargs
    return histoKwargs
    
def GetHisto(datasetsMgr, dataset, histoName):
    h = datasetsMgr.getDataset(dataset).getDatasetRootHisto(histoName)
    return h

def Plot2d(datasetsMgr, dataset, histoName, kwargs, opts):
    '''
    '''
    # Definitions
    saveName = histoName.replace("/", "_")
    
    # Get Histos for the plotter object
    refHisto = GetHisto(datasetsMgr, dataset, histoName)

    # Create the plotting object
    p = plots.PlotBase(datasetRootHistos=[refHisto], saveFormats=kwargs.get("saveFormats"))
    p.histoMgr.normalizeMCToLuminosity(opts.intLumi)

    # Customise axes (before drawing histo)    
    if 0:
        p.histoMgr.forEachHisto(lambda h: h.getRootHisto().GetXaxis().SetTitle(kwargs.get("xlabel")))
        p.histoMgr.forEachHisto(lambda h: h.getRootHisto().GetYaxis().SetTitle(kwargs.get("ylabel")))
    p.histoMgr.forEachHisto(lambda h: h.getRootHisto().RebinX(kwargs.get("rebinX")))
    p.histoMgr.forEachHisto(lambda h: h.getRootHisto().RebinY(kwargs.get("rebinY")))

    # Create a frame                                                                                                                                                             
    fOpts = {"ymin": 0.0, "ymaxfactor": 1.0}
    p.createFrame(saveName, opts=fOpts)
        
    # SetLog
    SetLogAndGrid(p, **kwargs)

    # Add cut line/box
    if 1:
        _kwargs = { "lessThan": True}
        p.addCutBoxAndLine(cutValue=400.0, fillColor=ROOT.kGray, box=False, line=True, **_kwargs)
        p.addCutBoxAndLineY(cutValue=200.0, fillColor=ROOT.kGray, box=False, line=True, **_kwargs)

    # Customise Legend
    moveLegend = {"dx": -0.1, "dy": +0.0, "dh": -0.1}
    p.setLegend(histograms.moveLegend(histograms.createLegend(), **kwargs.get("moveLegend")))
    p.removeLegend()

    # Customise histogram (after frame is created)
    p.histoMgr.forEachHisto(lambda h: h.getRootHisto().GetZaxis().SetTitle("Events"))
    p.histoMgr.forEachHisto(lambda h: h.getRootHisto().GetZaxis().SetTitleOffset(1.4))
    #ROOT.gPad.RedrawAxis()

    p.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetMinimum(kwargs.get("zmin")))    
    #p.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetMaximum(kwargs.get("zmax")))

    # Drawing style    
    p.histoMgr.setHistoDrawStyle(dataset, "COLZ")
    p.histoMgr.setHistoDrawStyleAll("COLZ")

    # The lines below do nothing since the Legend is disabled
    if 0:
        p.histoMgr.setHistoLegendStyle(dataset, "F")
        if "FakeB" in dataset:
            p.histoMgr.setHistoLegendLabelMany({
                    dataset: "QCD (Data)",
                    })
        if dataset == "QCD":
            p.histoMgr.setHistoLegendLabelMany({
                    dataset: "QCD (MC)",
                    })
            
    # Draw the plot
    p.draw()

    # Add canvas text
    if kwargs.get("addLuminosityText"):
        histograms.addStandardTexts(lumi=opts.intLumi)
    else:
        histograms.addStandardTexts()

    # Add dataset name on the canvas
    if dataset == "QCD":
        histograms.addText(0.17, 0.88, "QCD (H_{T} binned)", 27)
    else:
        histograms.addText(0.17, 0.88, plots._legendLabels[dataset], 27)

    # Save the plots
    SavePlot(p, saveName, os.path.join(opts.saveDir, opts.analysisName, opts.folder, dataset, opts.optMode) )
    return

def HasKeys(keyList, **kwargs):
    for key in keyList:
        if key not in kwargs:
            raise Exception("Could not find the keyword \"%s\" in kwargs" % (key) )
    return 

def SetLogAndGrid(p, **kwargs):
    '''
    '''
    HasKeys(["logX", "logY", "gridX", "gridY"], **kwargs)
    ratio = kwargs.get("createRatio")
    logX  = kwargs.get("logX")
    logY  = kwargs.get("logY")
    logZ  = kwargs.get("logZ")
    gridX = kwargs.get("gridX")
    gridY = kwargs.get("gridY")

    if ratio:
        p.getPad1().SetLogx(logX)
        p.getPad1().SetLogy(logY)
        p.getPad2().SetLogx(logX)
        p.getPad2().SetLogy(logY)
        p.getPad1().SetGridx(gridX)
        p.getPad1().SetGridy(gridY)
        p.getPad2().SetGridx(gridX)
        p.getPad2().SetGridy(gridY)
    else:
        p.getPad().SetLogx(logX)
        p.getPad().SetLogy(logY)
        if logZ != None:
            p.getPad().SetLogz(logZ)
        p.getPad().SetGridx(gridX)
        p.getPad().SetGridy(gridY)
    return

def SavePlot(plot, plotName, saveDir, saveFormats = [".png"]):
    # Check that path exists
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)

    # Create the name under which plot will be saved
    saveName = os.path.join(saveDir, plotName.replace("/", "_"))

    # For-loop: All save formats
    for i, ext in enumerate(saveFormats):
        saveNameURL = saveName + ext
        saveNameURL = saveNameURL.replace("/publicweb/a/aattikis/", "http://home.fnal.gov/~aattikis/")
        if i==0:
            print "=== plot_Kinematics2d.py:"

        if opts.url:
            print "\t", saveNameURL
        else:
            print "\t", saveName + ext
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
    ANALYSISNAME = "Kinematics"
    SEARCHMODE   = "80to1000"
    DATAERA      = "Run2016"
    OPTMODE      = None
    BATCHMODE    = True
    PRECISION    = 3
    INTLUMI      = -1.0
    SUBCOUNTERS  = False
    LATEX        = False
    MERGEEWK     = False
    URL          = False
    NOERROR      = True
    SAVEDIR      = "/publicweb/a/aattikis/"
    VERBOSE      = False
    HISTOLEVEL   = "Vital" # 'Vital' , 'Informative' , 'Debug' 
    FOLDER       = "TH2"
    NORMALISE    = False

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

    parser.add_option("--folder", dest="folder", action="store", default = FOLDER,
                      help="ROOT file folder under which all histograms to be plotted are located [default: %s]" % (FOLDER) )

    parser.add_option("-i", "--includeOnlyTasks", dest="includeOnlyTasks", action="store", 
                      help="List of datasets in mcrab to include")

    parser.add_option("-e", "--excludeTasks", dest="excludeTasks", action="store", 
                      help="List of datasets in mcrab to exclude")

    parser.add_option("-n", "--normaliseToOne", dest="normaliseToOne", action="store_true",
                      help="Normalise the histograms to one? [default: %s]" % (NORMALISE) )
    #"normalizeToOne", "normalizeByCrossSection", "normalizeToLumi"

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
        raw_input("=== plot_Kinematics2d.py: Press any key to quit ROOT ...")
