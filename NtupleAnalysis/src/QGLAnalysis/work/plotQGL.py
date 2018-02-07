#!/usr/bin/env python
'''
Description:

Usage:
./plotQGL.py -m <pseudo_mcrab> [opts]

Examples:
./plotQGL.py -m QGLAnalysis_171129_030702/ --url

'''

#================================================================================================ 
# Imports
#================================================================================================ 
import sys
import math
import copy
import json
import os
from optparse import OptionParser

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
# ==============================================================================================


kwargs = {
    "verbose"          : False,
    "dataEra"          : None,
    "searchMode"       : None,
    "analysis"         : "QGLAnalysis",
    "optMode"          : "",
    "savePath"         : None,
    "saveFormats"      : [".pdf"],
    "xlabel"           : None,
    "ylabel"           : "Events",
    "rebinX"           : 2,
    "rebinY"           : 2,
    "xlabelsize"       : None,
    "normalizeToOne"   : True,
    "ratio"            : True,
    "ratioYlabel"      : None,
    "ratioInvert"      : False,
    "addMCUncertainty" : False,
    "addLuminosityText": False,
    "addCmsText"       : True,
    "errorBarsX"       : True,
    "logX"             : False,
    "logY"             : False,
    "gridX"            : True,
    "gridY"            : True,
    "cmsExtraText"     : "Simulation",
    "removeLegend"     : False,
    "moveLegend"       : {"dx": -0.1, "dy": +0.0, "dh": +0.1},
    "cutValue"         : None,
    "cutLine"          : False,
    "cutBox"           : False,
    "cutLessthan"      : False,
    "cutFillColour"    : ROOT.kAzure-4,
    }


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

def GetListOfQCDatasets():
    Verbose("Getting list of QCD datasets")
    return ["QCD_HT1000to1500", "QCD_HT1500to2000","QCD_HT2000toInf","QCD_HT300to500","QCD_HT500to700","QCD_HT700to1000", "QCD_HT100to200", "QCD_HT200to300","QCD_HT50to100"]

def GetListOfEwkDatasets():
    Verbose("Getting list of EWK datasets")
    return ["WJetsToQQ_HT_600ToInf"] #"TT", "WJetsToQQ_HT_600ToInf", "DYJetsToQQHT", "SingleTop", "TTWJetsToQQ", "TTZToQQ", "Diboson", "TTTT"]

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
    

# =========================================================================================================================================
#                                                          MAIN
# =========================================================================================================================================
def main(opts, signalMass):
    
    print "Main Function"

    # Setup & configure the dataset manager 
    datasetsMgr = GetDatasetsFromDir(opts)
    datasetsMgr.updateNAllEventsToPUWeighted()
    
    # Get Luminosity
    datasetsMgr.loadLuminosities()
    
    # Print dataset cross sections
    datasetsMgr.PrintCrossSections()
    # Print luminosities
    datasetsMgr.PrintLuminosities()
        
    
    # Determine integrated Lumi before removing data
    # intLumi = datasetsMgr.getDataset("Data").getLuminosity()
    intLumi = 0
    
    # Remove datasets
    if 1:
        datasetsMgr.remove(filter(lambda name: "TTWJetsToQQ" in name, datasetsMgr.getAllDatasetNames()))
        datasetsMgr.remove(filter(lambda name: "QCD_bEnriched" in name, datasetsMgr.getAllDatasetNames()))
        
    # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
    plots.mergeRenameReorderForDataMC(datasetsMgr) 

        
    # Merge EWK samples
    if opts.mergeEWK:
        datasetsMgr.merge("EWK", GetListOfEwkDatasets())
        plots._plotStyles["EWK"] = styles.getAltEWKStyle()

    # Set plot Styles
    plots._plotStyles["QCD"] = styles.getAltEWKStyle()
    plots._plotStyles["WJetsToQQ_HT_600ToInf"] = styles.getBaselineLineStyle()
    
    # Print dataset information
    datasetsMgr.PrintInfo()
    
    # Apply TDR style
    style = tdrstyle.TDRStyle()
    style.setOptStat(True)
    style.setGridX(True)
    style.setGridY(False)
    
    histos = ["GluonJetsQGL",
              "GluonJetsPt", 
              "GluonJetsN",
             
              "LightJetsQGL",
              "LightJetsPt", 
              "LightJetsN",
              ]
    
    jsonhistos = ["GluonJetsQGL",
                  "LightJetsQGL",
                  ]


    for h in histos:
        
        # Produce & save the plots (inclusive)
        PlotMC(datasetsMgr, h, intLumi)
        
    for h in jsonhistos:
        
        # Produced the plots separately and dump the results in a JSON file
        for dataset in datasetsMgr.getAllDatasets():
            
            JetType = h.split("Jets")[0]
            results = []
            
            dsetHisto = dataset.getDatasetRootHisto(h)
            dsetHisto.normalizeToOne()
            histo = dsetHisto.getHistogram()
            
            for k in range(1, histo.GetNbinsX()+1):
                
                resultObject = {}
                resultObject["Jet"]       = JetType
                resultObject["QGLmin"]    = histo.GetBinLowEdge(k) 
                resultObject["QGLmax"]    = histo.GetBinLowEdge(k)+histo.GetBinWidth(k)
                resultObject["prob"]      = histo.GetBinContent(k)
                resultObject["probError"] = histo.GetBinError(k)
                results.append(resultObject)
                                
            filename = "QGLdiscriminator_%s_%sJets.json"%(dataset.name, JetType)
            with open(filename, 'w') as outfile:
                json.dump(results, outfile)
            
            print "Written results to %s"%filename

                
                

    return


# ------------------------------------------------
#    Plot Histograms
# ------------------------------------------------
def PlotMC(datasetsMgr, histo, intLumi):
    
    kwargs = {}
    p = plots.MCPlot(datasetsMgr, histo, normalizeToOne=True, saveFormats=[], **kwargs)

    # Draw the histograms
    _cutBox = None
    _rebinX = 1
    _format = "%0.01f"
    _xlabel = None
    logY    = False
    _opts   = {"ymin": 1e-3, "ymaxfactor": 1.2}

    if "Pt" in histo:
        if "Gluon" in histo:
            _xlabel = "Gluon Jets p_{T} (GeV)"
        elif "Light" in histo:
            _xlabel = "Light Jets p_{T} (GeV)"

    if "JetsN" in histo:
        if "Gluon" in histo:
            _xlabel = "Gluon Jets Multiplicity"
        elif "Light" in histo:
            _xlabel = "Light Jets Multiplicity"

    


    if "QGL" in histo:
        _opts["xmin"] = 0.0
        _opts["xmax"] = 1.0
        _units  = ""
        _format = "%0.01f " + _units
        if "Gluon" in histo:
            _xlabel = "Gluon Jets QGL"
        elif "Light" in histo:
            _xlabel = "Light Jets QGL"

    # Customise styling
    p.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetLineStyle(ROOT.kSolid))

    # Customise style
    signalM = []
    for m in signalMass:
        signalM.append(m.rsplit("M_")[-1])
    for m in signalM:
        p.histoMgr.forHisto("ChargedHiggs_HplusTB_HplusToTB_M_%s" %m, styles.getSignalStyleHToTB_M(m))

    plots.drawPlot(p, 
                   histo,  
                   xlabel       = _xlabel,
                   ylabel       = "Arbitrary Units",# / %s" % (_format),
                   log          = logY,
                   rebinX       = _rebinX, cmsExtraText = "Preliminary", 
                   createLegend = {"x1": 0.70, "y1": 0.65, "x2": 0.98, "y2": 0.92},
                   opts         = _opts,
                   opts2        = {"ymin": 0.6, "ymax": 1.4},
                   cutBox       = _cutBox,
                   )

    # Save plot in all formats    
    saveName = histo.split("/")[-1]
    savePath = os.path.join(opts.saveDir, "QGL", histo.split("/")[0], opts.optMode)
    SavePlot(p, saveName, savePath) 
    return









def SavePlot(plot, saveName, saveDir, saveFormats = [".pdf"]):
    Verbose("Saving the plot in %s formats: %s" % (len(saveFormats), ", ".join(saveFormats) ) )
    
    # Check that path exists
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)
        
    savePath = os.path.join(saveDir, saveName)

    # For-loop: All save formats
    for i, ext in enumerate(saveFormats):
        saveNameURL = savePath + ext
        saveNameURL = saveNameURL.replace("/publicweb/m/mkolosov/", "http://home.fnal.gov/~mkolosov/")
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
    ANALYSISNAME = "QGLR"
    SEARCHMODE   = "80to1000"
    DATAERA      = "Run2016"
    OPTMODE      = ""
    BATCHMODE    = True
    PRECISION    = 3
    #SIGNALMASS   = [200, 500, 800, 2000]
    SIGNALMASS   = [ ]
#    SIGNALMASS   = [200, 500, 1000]
    INTLUMI      = -1.0
    SUBCOUNTERS  = False
    LATEX        = False
    MERGEEWK     = False
    URL          = False
    NOERROR      = True
    SAVEDIR      = "/publicweb/m/mkolosov/" + ANALYSISNAME
    VERBOSE      = False
    HISTOLEVEL   = "Vital" # 'Vital' , 'Informative' , 'Debug'
    NORMALISE    = False
    FOLDER       = "" #"topSelection_" #"ForDataDrivenCtrlPlots" #"topologySelection_"
    MVACUT       = "MVA"
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

    parser.add_option("--MVAcut", dest="MVAcut", type="string", default = MVACUT,
                      help="Save plots to directory in respect of the MVA cut value [default: %s]" % (MVACUT) )

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
    if opts.mergeEWK:
        Print("Merging EWK samples into a single Datasets \"EWK\"", True)

    # Sanity check
    allowedMass = [180, 200, 220, 250, 300, 350, 400, 500, 800, 1000, 2000, 3000]
    signalMass = []
    for m in sorted(SIGNALMASS, reverse=True):
        signalMass.append("ChargedHiggs_HplusTB_HplusToTB_M_%.f" % m)

    # Call the main function
    main(opts, signalMass)

    if not opts.batchMode:
        raw_input("=== plotMC_HPlusMass.py: Press any key to quit ROOT ...")
