#!/usr/bin/env python
'''

Usage (single plot):
./plotHistograms.py -m <pseudo_mcrab_directory> <jsonfile>

Usage (multiple plots):
./plotHistograms.py -m <pseudo_mcrab_directory> json/AfterAllSelections/*.json
or
./plotHistograms.py -m <pseudo_mcrab_directory> json/AfterAllSelections/*.json json/AfterStandardSelections/*.json


Last Used:
./plotHistograms.py -m Hplus2tbAnalysis_161128_082955/ json/AfterAllSelections/BjetPt.json
or
./plotHistograms.py -m Hplus2tbAnalysis_161128_082955/ json/AfterAllSelections/*.json
or
./plotHistograms.py -m Hplus2tbAnalysis_161128_082955/ json/AfterAllSelections/*/*.json
'''

#================================================================================================
# Imports
#================================================================================================
import os
import sys
from optparse import OptionParser
import getpass
import socket
import json

import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.styles as styles
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux

import ROOT

#================================================================================================
# Main
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
    Verbose("Luminosity = %s (pb)" % (lumi), True )
    return lumi


def GetDatasetsFromDir(opts, json):
    Verbose("Getting datasets")
    
    if len(json["samples"])<1:
        Print("No samples defined in the JSON file. Exit", True)
        print __doc__
        sys.exit()
    else:
        return dataset.getDatasetsFromMulticrabDirs([opts.mcrab], 
                                                    dataEra=json["dataEra"],
                                                    searchMode=json["searchMode"],
                                                    analysisName=json["analysis"],
                                                    includeOnlyTasks="|".join(json["samples"]),
                                                    optimizationMode=json["optMode"])
    
def Plot(jsonfile, opts):
    Verbose("Plotting")

    with open(os.path.abspath(jsonfile)) as jfile:
        j = json.load(jfile)

        Print("Plotting %s in %s" % (j["title"], j["saveDir"]), True)

        # Setup the style
        style = tdrstyle.TDRStyle()
        style.setGridX(j["gridX"]=="True")
        style.setGridY(j["gridY"]=="True")
    
        # Set ROOT batch mode boolean
        ROOT.gROOT.SetBatch(opts.batchMode)

        # Setup & configure the dataset manager
        datasetsMgr = GetDatasetsFromDir(opts, j)
        datasetsMgr.loadLuminosities()
        datasetsMgr.updateNAllEventsToPUWeighted()
        if opts.verbose:
            datasetsMgr.PrintCrossSections()
            datasetsMgr.PrintLuminosities()

        # Set/Overwrite cross-sections
        for d in datasetsMgr.getAllDatasets():
            if "ChargedHiggs" in d.getName():
                datasetsMgr.getDataset(d.getName()).setCrossSection(1.0)

        # Merge histograms (see NtupleAnalysis/python/tools/plots.py)
        plots.mergeRenameReorderForDataMC(datasetsMgr)

        # Print dataset information
        datasetsMgr.PrintInfo()

        # Get Integrated Luminosity
        lumi = GetLumi(datasetsMgr)
        
        # Plot the histogram
        DataMCPlot(datasetsMgr, j)
        return


def DataMCPlot(datasetsMgr, json):
    Verbose("Creating Data-MC plot")

    # Create the Data-MC Plot
    p = plots.DataMCPlot(datasetsMgr, json["histogram"])
        
    # Label size (optional. Commonly Used in counters)
    xlabelSize = None
    if "xlabelsize" in json:
        xlabelSize = json["xlabelsize"]
    ylabelSize = None
    if "ylabelsize" in json:
        ylabelSize = json["ylabelsize"]

    # Draw a customised plot
    saveName = os.path.join(json["saveDir"], json["title"])
    plots.drawPlot(p, 
                   saveName,                  
                   xlabel            = json["xlabel"], 
                   ylabel            = json["ylabel"],
                   rebinX            = json["rebinX"],
                   rebinY            = json["rebinY"], 
                   ratioYlabel       = json["ratioYlabel"],
                   ratio             = json["ratio"]=="True", 
                   stackMCHistograms = json["stackMCHistograms"]=="True", 
                   ratioInvert       = json["ratioInvert"]=="True",
                   addMCUncertainty  = json["addMCUncertainty"]=="True",
                   addLuminosityText = json["addLuminosityText"]=="True",
                   addCmsText        = json["addCmsText"]=="True",
                   cmsExtraText      = json["cmsExtraText"],
                   opts              = json["opts"],
                   opts2             = json["ratioOpts"], 
                   log               = json["logY"]=="True", 
                   errorBarsX        = json["errorBarsX"]=="True", 
                   moveLegend        = json["moveLegend"],
                   # cutLine           = json["cutValue"], #cannot have this and "cutBox" defined
                   cutBox            = {"cutValue": json["cutValue"], "fillColor": json["cutFillColour"], "box": json["cutBox"]=="True", "line": json["cutLine"]=="True", "greaterThan": json["cutGreaterThan"]=="True"},
                   xlabelsize        = xlabelSize,
                   ylabelsize        = ylabelSize,
                   )
    
    # Remove legend?
    if json["removeLegend"] == "True":
        p.removeLegend()

    # Additional text
    histograms.addText(json["extraText"].get("x"), json["extraText"].get("y"), json["extraText"].get("text"), json["extraText"].get("size") )

    # Save in all formats chosen by user
    saveFormats = json["saveFormats"]
    for i, ext in enumerate(saveFormats):
        Print("%s" % saveName + ext, i==0)
    p.saveAs(saveName, formats=saveFormats)
    return


def main(opts):
    Verbose("main function")

    jsonFiles = []
    # For-loop: All system script arguments
    for arg in sys.argv[1:]:

        # Skip if not a json file
        if ".json" not in arg:
            continue

        # Sanity check - File exists
        if not os.path.exists(arg):
            Print("The JSON file \"%s\" does not seem to be a valid path.. Please check that the file exists. Exit" % (arg), True)
            sys.exit()

        # Load & append json file
        with open(os.path.abspath(arg)) as jsonFile:
            try:
                json.load(jsonFile)
                jsonFiles.append(arg)
            except ValueError, e:
                Print("Problem loading JSON file %s. Please check the file" % (arg))
                sys.exit()

    # Sanity check - At least 1 json file found
    if len(jsonFiles) == 0:
        Print("No JSON files found. Please read the script instructions. Exit", True)
        print __doc__
        sys.exit()    

    # For-loop: All json files
    for j in jsonFiles:
        Print("Processing JSON file \"%s\"" % (j), True)
        Plot(j, opts)    
    return


#================================================================================================
# Main
#================================================================================================
if __name__ == "__main__":

    # Default Settings 
    global opts
    BATCHMODE = True
    VERBOSE   = False

    parser = OptionParser(usage="Usage: %prog [options]" , add_help_option=False,conflict_handler="resolve")

    parser.add_option("-m", "--mcrab", dest="mcrab", action="store", 
                      help="Path to the multicrab directory for input")

    parser.add_option("-b", "--batchMode", dest="batchMode", action="store_false", default=BATCHMODE, 
                      help="Enables batch mode (canvas creation  NOT generates a window) [default: %s]" % BATCHMODE)

    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=VERBOSE, 
                      help="Enables verbose mode (for debugging purposes) [default: %s]" % VERBOSE)

    (opts, parseArgs) = parser.parse_args()

    # Require at least two arguments (script-name, path to multicrab)
    if opts.mcrab == None:
        Print("Not enough arguments passed to script execution. Printing docstring & EXIT.")
        print __doc__
        sys.exit(0)

    # Call the main function
    main(opts)

    if not opts.batchMode:
        raw_input("=== plotHistograms.py: Press any key to quit ROOT ...")
