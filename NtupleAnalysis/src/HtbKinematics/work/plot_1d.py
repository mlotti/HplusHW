#!/usr/bin/env python
'''
Description:
Generate all TH1 generated from the Kinematics analyzer (GEN-level info).

Usage:
./plot_1d.py -m <pseudo_mcrab> [opts]

Examples:
./plot_1d.py -m <peudo_mcrab> -o "" --url --normaliseToOne

Last Used:
./plot_1d.py -m HtbKinematics_StdSelections_TopCut100_AllSelections_NoTrgMatch__H2Cut0p5_NoTopMassCut_170905_105432 --url --normaliseToOne

'''

#================================================================================================ 
# Imports
#================================================================================================ 
import sys
import math
import copy
import os
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

def natural_sort_key(s):
    _nsre = re.compile('([0-9]+)')
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(_nsre, s)]   

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
    

def GetAllDatasetsFromDir(opts):
    datasets = dataset.getDatasetsFromMulticrabDirs([opts.mcrab],
                                                    dataEra=opts.dataEra,
                                                    searchMode=opts.searchMode,
                                                    analysisName=opts.analysisName,
                                                    optimizationMode=opts.optMode)
    return datasets

def main(opts, signalMass):

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
        datasetsMgr = GetDatasetsFromDir(opts)
        datasetsMgr.updateNAllEventsToPUWeighted()
        datasetsMgr.loadLuminosities() # from lumi.json
        if opts.verbose:
            datasetsMgr.PrintCrossSections()
            datasetsMgr.PrintLuminosities()

        # Set/Overwrite cross-sections
        for d in datasetsMgr.getAllDatasets():
            if d.getName() in signalMass:
                # print "*** Setting cross-section for %s to 1pb " % (d.getName())
                datasetsMgr.getDataset(d.getName()).setCrossSection(1.0)
            else:
                # print "*** Removing dataset ", d.getName()
                datasetsMgr.remove(d.getName())

        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        plots.mergeRenameReorderForDataMC(datasetsMgr) 
        
        # Print dataset information
        datasetsMgr.PrintInfo()

        # Re-order datasets in ascending mass 
        newOrder = []
        for i, d in enumerate(datasetsMgr.getAllDatasetNames()):
            newOrder.append(d)
        newOrder.sort(key=natural_sort_key)
        datasetsMgr.selectAndReorder(newOrder)

        # Apply TDR style
        style = tdrstyle.TDRStyle()
        style.setOptStat(True)
        style.setGridX(True)
        style.setGridY(True)

        # Do the topSelection histos
        folder     = opts.folder
        histoPaths = []
        histoList  = datasetsMgr.getDataset(datasetsMgr.getAllDatasetNames()[0]).getDirectoryContent(folder)
        hList      = [h for h in histoList if "_Vs_" not in h]
        histoPaths = [os.path.join(folder, h) for h in hList]
        for h in histoPaths:
            PlotMC(datasetsMgr, h, opts.intLumi)
    return


def GetHistoKwargs(histo, opts):
    '''
    Dictionary with 
    key   = histogramName
    value = kwargs
    '''
    
    if opts.normaliseToOne:
        yLabel = "Arbitrary Units"
    else:
        yLabel = "Events"
    logY       = False
    yMaxFactor = 1.2

    # Create with default values
    kwargs = {
        "xlabel"           : "x-label",
        "ylabel"           : yLabel,
        "rebinX"           : 1,
        "rebinY"           : 1,
        "ratioYlabel"      : "Data/MC",
        "ratio"            : True, 
        "stackMCHistograms": True,
        "ratioInvert"      : False, 
        "addMCUncertainty" : False, 
        "addLuminosityText": True,
        "addCmsText"       : True,
        "cmsExtraText"     : "Preliminary",
        "opts"             : {"ymin": 0.0, "ymaxfactor": yMaxFactor},
        "opts2"            : {"ymin": 0.0, "ymax": 2.0},
        "log"              : logY,
        "moveLegend"       : {"dx": -0.1, "dy": 0.0, "dh": -0.1},
        "cutBox"           : {"cutValue": 0.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
        }

    ROOT.gStyle.SetNdivisions(10, "X")
    if "genHT" in histo:
        units            = "GeV"
        format           = "%0.0f " + units
        kwargs["xlabel"] = "H_{T} (%s)" % units
        kwargs["ylabel"] = yLabel + "/ %s " % format
        kwargs["opts"]   = {"xmin": 500.0, "xmax": 2000.0}
        kwargs["log"]    = True
        ROOT.gStyle.SetNdivisions(10, "X")
    elif histo.lower().endswith("met_et"):
        units            = "GeV"
        format           = "%0.0f " + units
        kwargs["xlabel"] = "E_{T}^{miss} (%s)" % units
        kwargs["ylabel"] = yLabel + "/ %s " % format
        kwargs["opts"]   = {"xmin": 0.0, "xmax": 300.0}
        kwargs["log"]    = True
    elif histo.lower().endswith("_n"):
        units            = ""
        format           = "%0.0f " + units
        kwargs["xlabel"] = "multiplicity"
        kwargs["ylabel"] = yLabel + " / %.1f " +  units
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +16.0}
    elif histo.lower().endswith("_pt"):
        units            = "GeV/c"
        format           = " / %0.0f " + units
        kwargs["xlabel"] = "p_{T} (%s)" % units
        kwargs["ylabel"] = yLabel + format
        kwargs["cutBox"] = {"cutValue": 40.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +400.0}
        if "1" in histo:
            kwargs["opts"]   = {"xmin": 0.0, "xmax": +800.0}
        elif "2" in histo:
            kwargs["opts"]   = {"xmin": 0.0, "xmax": +500.0}
        elif "3" in histo:
            kwargs["opts"]   = {"xmin": 0.0, "xmax": +400.0}
        elif "4" in histo:
            kwargs["opts"]   = {"xmin": 0.0, "xmax": +300.0}
        elif "5" in histo:
            kwargs["opts"]   = {"xmin": 0.0, "xmax": +250.0}
        elif "6" in histo:
            kwargs["opts"]   = {"xmin": 0.0, "xmax": +200.0}
        else:
            pass

        if "gbb_BQuark" in histo:
            kwargs["opts"]   = {"xmin": 0.0, "xmax": +300.0}
        if "gtt_tbW_Wqq" in histo:
            kwargs["opts"]   = {"xmin": 0.0, "xmax": +500.0}
        if "tbH_BQuark" in histo or "tbH_HPlus" in histo or "tbH_TQuark" in histo:
            kwargs["log"]    = True
            
    elif histo.lower().endswith("_eta"):
        units            = ""
        kwargs["xlabel"] = "#eta"
        kwargs["ylabel"] = yLabel + " / %.1f " + units
        kwargs["cutBox"] = {"cutValue": 0.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        kwargs["opts"]   = {"xmin": -5.0, "xmax": +5.0}
        kwargs["log"]    = True
    elif histo.lower().endswith("_rap"):
        units            = ""
        kwargs["xlabel"] = "#omega"
        kwargs["ylabel"] = yLabel + " / %.1f " + units
        kwargs["cutBox"] = {"cutValue": 0.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        kwargs["opts"]   = {"xmin": -5.0, "xmax": +5.0}
        kwargs["log"]    = True
    elif histo.lower().endswith("_phi"):
        units            = "rads"
        kwargs["xlabel"] = "#phi (%s)" % units
        kwargs["ylabel"] = yLabel + "/ %.1f " + units
    elif histo.lower().endswith("_mass"):
        units            = "GeV/c^{2}"
        format           = "%0.0f " + units
        kwargs["xlabel"] = "mass (%s)" % units
        kwargs["ylabel"] = yLabel + " / %.1f " +  units
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +500.0}
        kwargs["log"]    = True
        if "MaxDiJetMass" in histo:
            kwargs["opts"]   = {"xmin": 0.0, "xmax": +3000.0}
            ROOT.gStyle.SetNdivisions(8, "X")
        if "tt_mass" in histo.lower():
            kwargs["opts"]   = {"xmin": 0.0, "xmax": +3000.0}
            ROOT.gStyle.SetNdivisions(8, "X")
    elif histo.lower().endswith("_deta"):        
        units            = ""
        kwargs["xlabel"] = "#Delta#eta"
        kwargs["ylabel"] = yLabel + " / %.1f " + units
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +10.0}
        kwargs["log"]    = True
    elif histo.lower().endswith("_dphi"):
        units            = "rads"
        kwargs["xlabel"] = "#Delta#phi"
        kwargs["ylabel"] = yLabel + " / %.1f " + units
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +3.2}
        kwargs["log"]    = False
    elif  histo.lower().endswith("_drap"):
        units            = ""
        kwargs["xlabel"] = "#Delta#omega"
        kwargs["ylabel"] = yLabel + " / %.1f " + units
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +10.0}
        kwargs["log"]    = True
    elif histo.lower().endswith("_dr"):
        units            = ""
        kwargs["xlabel"] = "#DeltaR"
        kwargs["ylabel"] = yLabel + " / %.1f " + units
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +10.0}
        kwargs["log"]    = True
    elif  histo.lower().endswith("_drrap"):
        units            = ""
        kwargs["xlabel"] = "#DeltaR_{#omega}"
        kwargs["ylabel"] = yLabel + " / %.1f " + units
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +10.0}
        kwargs["log"]    = True
    else:
        units = ""
        kwargs["ylabel"] = yLabel + " / %.0f " + units

    # General Options
    if opts.normaliseToOne:
        yMin = 1e-4
    else:
        yMin = 1e0

    if kwargs["log"] == True:
        yMaxFactor = 2
    else:
        yMaxFactor = 1.2

    # Finalise and return
    kwargs["opts"]["ymaxfactor"] = yMaxFactor
    kwargs["opts"]["ymin"]       = yMin
    return kwargs
  
def PlotMC(datasetsMgr, histo, intLumi):

    kwargs = {}
    if opts.normaliseToOne:
        p = plots.MCPlot(datasetsMgr, histo, normalizeToOne=True, saveFormats=[], **kwargs)
    else:
        p = plots.MCPlot(datasetsMgr, histo, normalizeToLumi=intLumi, saveFormats=[], **kwargs)

    # Get histogram<->kwargs dictionary 
    kwargs = GetHistoKwargs(histo, opts)

    # Customise style
    for i, m in enumerate(signalMass):
        massNum = m.rsplit("M_")[-1]
        if i==len(signalMass)-1:
            p.histoMgr.setHistoDrawStyle(m, "HIST")
            p.histoMgr.setHistoLegendStyle(m, "F")
            p.histoMgr.forHisto(m, styles.getSignalStyleHToTB())
            # p.histoMgr.forHisto(m, styles. getSignalfillStyleHToTB())
            # p.histoMgr.forHisto(m, datasetsMgr.getDataset(m).getRootHisto().SetMarkerStyle(6))
            # h = GetRootHisto(datasetsMgr, m, histo)
            # h.SetFillStyle(1001)
            # p.histoMgr.setHistoLegendStyle(dName, "LP")
            h =  datasetsMgr.getDataset(m).getDatasetRootHisto(histo).getHistogram()
            styles.qcdFillStyle.apply(h)
        else:
            p.histoMgr.forHisto(m, styles.getSignalStyleHToTB_M(massNum))
            p.histoMgr.setHistoLegendStyle(m, "LP")

    # Plot customised histogram
    plots.drawPlot(p, 
                   histo,  
                   xlabel       = kwargs.get("xlabel"),
                   ylabel       = kwargs.get("ylabel"),
                   log          = kwargs.get("log"),
                   rebinX       = kwargs.get("rebinX"), 
                   cmsExtraText = "Preliminary", 
                   #createLegend = {"x1": 0.62, "y1": 0.75, "x2": 0.92, "y2": 0.92},
                   moveLegend   = kwargs.get("moveLegend"),
                   opts         = kwargs.get("opts"),
                   opts2        = {"ymin": 0.6, "ymax": 1.4},
                   cutBox       = kwargs.get("cutBox"),
                   )

    # Customise styling
    if 0:
        p.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetLineStyle(ROOT.kSolid))
        p.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetMarkerSize(0))
        p.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetMarkerStyle(6))
    p.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetLineStyle(ROOT.kSolid))

    # Save plot in all formats    
    saveName = histo.split("/")[-1]
    if opts.folder == "":
        savePath = os.path.join(opts.saveDir, opts.optMode)
    else:
        savePath = os.path.join(opts.saveDir, histo.split("/")[0], opts.optMode)
    SavePlot(p, saveName, savePath, [".png", ".pdf"]) 
    return


def SavePlot(plot, saveName, saveDir, saveFormats = [".C", ".png", ".pdf"]):
    Verbose("Saving the plot in %s formats: %s" % (len(saveFormats), ", ".join(saveFormats) ) )
    
    # Check that path exists
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)
        
    savePath = os.path.join(saveDir, saveName)

    # For-loop: All save formats
    for i, ext in enumerate(saveFormats):
        saveNameURL = savePath + ext
        saveNameURL = saveNameURL.replace("/publicweb/a/aattikis/", "http://home.fnal.gov/~aattikis/")
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
    ANALYSISNAME = "HtbKinematics"
    SEARCHMODE   = "80to1000"
    DATAERA      = "Run2016"
    OPTMODE      = ""
    BATCHMODE    = True
    PRECISION    = 3
    SIGNALMASS   = [200, 500, 800]#, 1000]
    INTLUMI      = -1.0
    SUBCOUNTERS  = False
    LATEX        = False
    URL          = False
    NOERROR      = True
    SAVEDIR      = "/publicweb/a/aattikis/" + ANALYSISNAME
    VERBOSE      = False
    HISTOLEVEL   = "Vital" # 'Vital' , 'Informative' , 'Debug'
    NORMALISE    = False
    FOLDER       = "TH1" #"TH2"

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
    signalMass  = []
    for m in sorted(SIGNALMASS, reverse=False):
        signalMass.append("ChargedHiggs_HplusTB_HplusToTB_M_%.f" % m)
    
    # Call the main function
    main(opts, signalMass)

    if not opts.batchMode:
        raw_input("=== plot_1d.py: Press any key to quit ROOT ...")


'''
All histogram names:

genMET_Et

MaxDiJetMass_dRrap

genHT_GenParticles
genHT_GenJets

#GenJets_N

MaxDiJetMass_dRap
gtt_tbW_bqq_dRMax_dRap
Htb_tbW_bqq_dRMax_dRap
gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark_dRap
gtt_tbW_BQuark_gtt_tbW_Wqq_Quark_dRap
gtt_TQuark_gtt_tbW_BQuark_dRap
gtt_TQuark_gbb_BQuark_dRap
Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark_dRap
Htb_tbW_BQuark_Htb_tbW_Wqq_Quark_dRap
Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dRap
Htb_BQuark_Htb_tbW_Wqq_Quark_dRap
Htb_BQuark_Htb_tbW_BQuark_dRap
Htb_TQuark_gbb_BQuark_dRap
Htb_TQuark_gtt_TQuark_dRap
Htb_TQuark_Htb_BQuark_dRap
Htb_TQuark_gtt_TQuark_dRap
Htb_TQuark_Htb_BQuark_dRap

genMET_Phi

MaxDiJetMass_dPhi
gtt_tbW_bqq_dRMax_dPhi
Htb_tbW_bqq_dRMax_dPhi
BQuarkPair_dRMin_jet2_dPhi
BQuarkPair_dRMin_jet1_dPhi
BQuarkPair_dRMin_dPhi
gtt_tbW_WBoson_gbb_BQuark_dPhi
gtt_tbW_WBoson_gbb_BQuark_dPhi
gtt_tbW_WBoson_gtt_tbW_BQuark_dPhi
gtt_tbW_WBoson_Htb_tbW_BQuark_dPhi
gtt_tbW_WBoson_Htb_BQuark_dPhi
Htb_tbW_WBoson_gbb_BQuark_dPhi
Htb_tbW_WBoson_gtt_tbW_BQuark_dPhi
Htb_tbW_WBoson_Htb_tbW_BQuark_dPhi
Htb_tbW_WBoson_Htb_BQuark_dPhi
gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark_dPhi
gtt_tbW_BQuark_gtt_tbW_Wqq_Quark_dPhi
gtt_TQuark_gtt_tbW_BQuark_dPhi
gtt_TQuark_gbb_BQuark_dPhi
Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark_dPhi
Htb_tbW_BQuark_Htb_tbW_Wqq_Quark_dPhi
Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dPhi
Htb_BQuark_Htb_tbW_Wqq_Quark_dPhi
Htb_BQuark_Htb_tbW_BQuark_dPhi
Htb_TQuark_gbb_BQuark_dPhi
Htb_TQuark_gtt_TQuark_dPhi
Htb_TQuark_Htb_BQuark_dPhi

MaxDiJetMass_dEta
BQuarkPair_dRMin_jet2_dEta
BQuarkPair_dRMin_jet1_dEta
BQuarkPair_dRMin_dEta
gtt_tbW_WBoson_gbb_BQuark_dEta
gtt_tbW_WBoson_gtt_tbW_BQuark_dEta
gtt_tbW_WBoson_Htb_tbW_BQuark_dEta
gtt_tbW_WBoson_Htb_BQuark_dEta
Htb_tbW_WBoson_gbb_BQuark_dEta
Htb_tbW_WBoson_gtt_tbW_BQuark_dEta
Htb_tbW_WBoson_Htb_tbW_BQuark_dEta
Htb_tbW_WBoson_Htb_BQuark_dEta
gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark_dEta
gtt_tbW_BQuark_gtt_tbW_Wqq_Quark_dEta
gtt_TQuark_gtt_tbW_BQuark_dEta
gtt_TQuark_gbb_BQuark_dEta
Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark_dEta
Htb_tbW_BQuark_Htb_tbW_Wqq_Quark_dEta
Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dEta
Htb_BQuark_Htb_tbW_Wqq_Quark_dEta
Htb_BQuark_Htb_tbW_BQuark_dEta
Htb_TQuark_gbb_BQuark_dEta
Htb_TQuark_gtt_TQuark_dEta
Htb_TQuark_Htb_BQuark_dEta
Htb_tbW_BQuark_Htb_tbW_Wqq_Quark_dEta
Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dEta
Htb_BQuark_Htb_tbW_Wqq_Quark_dEta
Htb_BQuark_Htb_tbW_BQuark_dEta
Htb_TQuark_gbb_BQuark_dEta
Htb_TQuark_gtt_TQuark_dEta
Htb_TQuark_Htb_BQuark_dEta

gtt_tbW_WBoson_gbb_BQuark_dR
MaxDiJetMass_dR
gtt_tbW_bqq_dRMax_dR
Htb_tbW_bqq_dRMax_dR
BQuarkPair_dRMin_jet2_dR
BQuarkPair_dRMin_jet1_dR
BQuarkPair_dRMin_dR
gtt_tbW_WBoson_gtt_tbW_BQuark_dR
gtt_tbW_WBoson_Htb_tbW_BQuark_dR
gtt_tbW_WBoson_Htb_BQuark_dR
Htb_tbW_WBoson_gbb_BQuark_dR
Htb_tbW_WBoson_gtt_tbW_BQuark_dR
Htb_tbW_WBoson_Htb_tbW_BQuark_dR
Htb_tbW_WBoson_Htb_BQuark_dR
gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark_dR
gtt_tbW_BQuark_gtt_tbW_Wqq_Quark_dR
gtt_TQuark_gtt_tbW_BQuark_dR
gtt_TQuark_gbb_BQuark_dR
Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark_dR
Htb_tbW_BQuark_Htb_tbW_Wqq_Quark_dR
Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dR
Htb_BQuark_Htb_tbW_Wqq_Quark_dR
Htb_BQuark_Htb_tbW_BQuark_dR
Htb_TQuark_gbb_BQuark_dR
Htb_TQuark_gtt_TQuark_dR
Htb_TQuark_Htb_BQuark_dR
gtt_tbW_WBoson_gbb_BQuark_dR
gtt_tbW_WBoson_gtt_tbW_BQuark_dR
gtt_tbW_WBoson_Htb_tbW_BQuark_dR
gtt_tbW_WBoson_Htb_BQuark_dR
Htb_tbW_WBoson_gbb_BQuark_dR
Htb_tbW_WBoson_gtt_tbW_BQuark_dR
Htb_tbW_WBoson_Htb_tbW_BQuark_dR
Htb_tbW_WBoson_Htb_BQuark_dR
gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark_dR
gtt_tbW_BQuark_gtt_tbW_Wqq_Quark_dR
gtt_TQuark_gtt_tbW_BQuark_dR
gtt_TQuark_gbb_BQuark_dR
Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark_dR
Htb_tbW_BQuark_Htb_tbW_Wqq_Quark_dR
Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dR
Htb_BQuark_Htb_tbW_Wqq_Quark_dR
Htb_BQuark_Htb_tbW_BQuark_dR
Htb_TQuark_gbb_BQuark_dR
Htb_TQuark_gtt_TQuark_dR
Htb_TQuark_Htb_BQuark_dR

MaxDiJetMass_Rap
tt_Rap
gtt_tbW_bqq_Rap
Htb_tbW_bqq_Rap
Htb_tbW_Wqq_AntiQuark_Rap
Htb_tbW_Wqq_Quark_Rap
gbb_BQuark_Rap
tbH_tbW_BQuark_Rap
tbH_tbW_WBoson_Rap
tbH_BQuark_Rap
tbH_TQuark_Rap
tbH_HPlus_Rap
gtt_tbW_Wqq_AntiQuark_Rap
gtt_tbW_Wqq_Quark_Rap
gtt_tbW_BQuark_Rap
Htb_tbW_Wqq_AntiQuark_Rap
Htb_tbW_Wqq_Quark_Rap
gbb_BQuark_Rap
tbH_tbW_BQuark_Rap
tbH_tbW_WBoson_Rap
tbH_BQuark_Rap
tbH_TQuark_Rap
tbH_HPlus_Rap
gtt_tbW_Wqq_AntiQuark_Rap
gtt_tbW_Wqq_Quark_Rap
gtt_tbW_BQuark_Rap
gtt_tbW_WBoson_Rap
gtt_TQuark_Rap

MaxDiJetMass_Mass
Htb_tbW_bqq_Mass
BQuarkPair_dRMin_Mass
gtt_tbW_bqq_Mass
tt_Mass

MaxDiJetMass_Eta
tt_Eta
BQuark4_Eta
BQuark3_Eta
BQuark2_Eta
BQuark1_Eta
GenJet6_Eta
GenJet5_Eta
GenJet4_Eta
GenJet3_Eta
GenJet2_Eta
GenJet1_Eta
Htb_tbW_Wqq_AntiQuark_Eta
Htb_tbW_Wqq_Quark_Eta
gbb_BQuark_Eta
tbH_tbW_BQuark_Eta
tbH_tbW_WBoson_Eta
tbH_BQuark_Eta
tbH_TQuark_Eta
tbH_HPlus_Eta
gtt_tbW_Wqq_AntiQuark_Eta
gtt_tbW_Wqq_Quark_Eta
gtt_tbW_BQuark_Eta
gtt_tbW_WBoson_Eta
gtt_TQuark_Eta

MaxDiJetMass_Pt
t_Pt
GenJet6_Pt
GenJet5_Pt
GenJet4_Pt
GenJet3_Pt
GenJet2_Pt
GenJet1_Pt
BQuarkPair_dRMin_pT
BQuark4_Pt
BQuark3_Pt
BQuark2_Pt
BQuark1_Pt
Htb_tbW_bqq_Pt
gtt_tbW_bqq_Pt
Htb_tbW_Wqq_AntiQuark_Pt
Htb_tbW_Wqq_Quark_Pt
gbb_BQuark_Pt
tbH_tbW_BQuark_Pt
tbH_tbW_WBoson_Pt
tbH_BQuark_Pt
tbH_TQuark_Pt
tbH_HPlus_Pt
gtt_tbW_Wqq_AntiQuark_Pt
gtt_tbW_Wqq_Quark_Pt
gtt_tbW_BQuark_Pt
gtt_tbW_WBoson_Pt
gtt_TQuark_Pt
'''
