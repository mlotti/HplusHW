#!/usr/bin/env python
'''
Generic scipt that plots TH1 histograms (Data, MC) with the ratio pad enabled.

Usage (single plot):
./plotDataMC.py -m <pseudo_mcrab_directory> <jsonfile> [opts]

Usage (multiple plots):
./plotDataMC.py -m <pseudo_mcrab_directory> json/AfterAllSelections/*.json

Usage (overwrite samples defined in JSON):
./plotDataMC.py -m <pseudo_mcrab_directory> json/AfterAllSelections/*.json -i "JetHT|QCD_H"
./plotDataMC.py -m <pseudo_mcrab_directory> json/AfterAllSelections/*.json -e "QCD_b|Charged"


Last Used:
./plotDataMC.py -m Hplus2tbAnalysis_StdSelections_TopCut100_AllSelections_NoTrgMatch_TopCut10_H2Cut0p5_170810_022933 -o "" -e "Charged|QCD_b|QCD_HT50to100|QCD_HT100to200|FakeB" json/eSelection_Veto/*.json
./plotDataMC.py -m Hplus2tbAnalysis_StdSelections_TopCut100_AllSelections_NoTrgMatch_TopCut10_H2Cut0p5_170810_022933 -o "" -e "Charged|QCD_b|QCD_HT50to100|QCD_HT100to200|FakeB" json/*_Veto/*.json
./plotDataMC.py -m Hplus2tbAnalysis_StdSelections_TopCut100_AllSelections_NoTrgMatch_TopCut10_H2Cut0p5_170810_022933 -o "" -e "Charged|QCD_b|QCD_HT50to100|QCD_HT100to200|FakeB" json/jetSelection/*.json
./plotDataMC.py -m Hplus2tbAnalysis_StdSelections_TopCut100_AllSelections_NoTrgMatch_TopCut10_H2Cut0p5_170810_022933 -o "" -e "Charged|QCD_b|QCD_HT50to100|QCD_HT100to200|FakeB" json/bjetSelection/*
./plotDataMC.py -m Hplus2tbAnalysis_StdSelections_TopCut100_AllSelections_NoTrgMatch_TopCut10_H2Cut0p5_170810_022933 -o "" -e "Charged|QCD_b|QCD_HT50to100|QCD_HT100to200|FakeB" json/topologySelection/*.json

Previously Used:
./plotDataMC.py -m Hplus2tbAnalysis_* json/PUDependency/* -e "Charged|QCD_b|QCD_HT50to100|QCD_HT100to200" 
./plotDataMC.py -m Hplus2tbAnalysis_* json/counters/* -e "Charged|QCD_b|QCD_HT50to100|QCD_HT100to200"
./plotDataMC.py -m Hplus2tbAnalysis_* json/counters/weighted/* -e "Charged|QCD_b|QCD_HT50to100|QCD_HT100to200" 
./plotDataMC.py -m Hplus2tbAnalysis_* json/eSelection_Veto/* -e "Charged|QCD_b|QCD_HT50to100|QCD_HT100to200"
./plotDataMC.py -m Hplus2tbAnalysis_* json/muSelection_Veto/* -e "Charged|QCD_b|QCD_HT50to100|QCD_HT100to200"
./plotDataMC.py -m Hplus2tbAnalysis_* json/tauSelection_Veto/* -e "Charged|QCD_b|QCD_HT50to100|QCD_HT100to200"
./plotDataMC.py -m Hplus2tbAnalysis_* json/jetSelection/* -e "Charged|QCD_b|QCD_HT50to100|QCD_HT100to200"
./plotDataMC.py -m Hplus2tbAnalysis_* json/bjetSelection/* -e "Charged|QCD_b|QCD_HT50to100|QCD_HT100to200"
./plotDataMC.py -m Hplus2tbAnalysis_* json/metSelection/* -e "Charged|QCD_b|QCD_HT50to100|QCD_HT100to200"
./plotDataMC.py -m Hplus2tbAnalysis_* json/topologySelection/* -e "Charged|QCD_b|QCD_HT50to100|QCD_HT100to200"
./plotDataMC.py -m Hplus2tbAnalysis_* json/topSelection/* -e "Charged|QCD_b|QCD_HT50to100|QCD_HT100to200"
./plotDataMC.py -m Hplus2tbAnalysis_* json/AfterStandardSelections/* -e "Charged|QCD_b|QCD_HT50to100|QCD_HT100to200"
./plotDataMC.py -m Hplus2tbAnalysis_* json/AfterAllSelections/* -e "Charged|QCD_b|QCD_HT50to100|QCD_HT100to200"
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

    if opts.optMode == None:
        optMode = json["optMode"]
    else:
        optMode = opts.optMode

    if (opts.includeOnlyTasks):
        return dataset.getDatasetsFromMulticrabDirs([opts.mcrab], 
                                                    dataEra=json["dataEra"],
                                                    searchMode=json["searchMode"],
                                                    analysisName=json["analysis"],
                                                    includeOnlyTasks=opts.includeOnlyTasks,
                                                    optimizationMode=optMode)
    elif (opts.excludeTasks):
        return dataset.getDatasetsFromMulticrabDirs([opts.mcrab], 
                                                    dataEra=json["dataEra"],
                                                    searchMode=json["searchMode"],
                                                    analysisName=json["analysis"],
                                                    excludeTasks=opts.excludeTasks,
                                                    optimizationMode=optMode)
    else:
        #return process.addDatasetsFromMulticrab(opts.mcrab)
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
                                                        optimizationMode=optMode)
        
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


        # Remove all but one signal datasets
        massPoints = ["180", "200", "220", "250", "300", "350", "400", "500", "800", "1000", "2000", "3000"]
        if opts.signal != None:
            massPoints.remove(opts.signal) #keep only 1 mass point        
        for m in massPoints:
                datasetsMgr.remove(filter(lambda name: "M_" + m in name, datasetsMgr.getAllDatasetNames()))

        # Merge histograms (see NtupleAnalysis/python/tools/plots.py)
        plots.mergeRenameReorderForDataMC(datasetsMgr)
        ReorderToShowSignal(datasetsMgr, opts)

        # Print dataset information
        datasetsMgr.PrintInfo()

        # Get Integrated Luminosity
        lumi = GetLumi(datasetsMgr)
        
        # Plot the histogram
        DataMCPlot(datasetsMgr, j)
        return

def DataMCPlot(datasetsMgr, json):
    Verbose("Creating Data-MC plot")

    if opts.saveDir == None:
        saveDir = json["saveDir"]
    else: 
        saveDir = json["saveDir"]

    # Create the Data-MC Plot
    p = plots.DataMCPlot(datasetsMgr, json["histogram"])
        
    # Label size (optional. Commonly Used in counters)
    xlabelSize = None
    if "xlabelsize" in json:
        xlabelSize = json["xlabelsize"]
    ylabelSize = None
    if "ylabelsize" in json:
        ylabelSize = json["ylabelsize"]

    # Draw a customised plot, os.path.join(opts.saveDir, "Fit")
    plots.drawPlot(p, 
                   json["title"], #os.path.join(saveDir, json["title"])
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

    # Save in custom formats
    SavePlot(p, json["title"], os.path.join(saveDir, opts.optMode), json["saveFormats"])
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
        saveNameURL = saveNameURL.replace("/publicweb/a/aattikis/", "http://home.fnal.gov/~aattikis/")
        if opts.url:
            Print(saveNameURL, i==0)
        else:
            Print(saveName + ext, i==0)
        plot.saveAs(saveName, formats=saveFormats)
    return


def ReorderToShowSignal(datasetMgr, opts):
    
    if opts.signal == None:
        return
    signalSample = "ChargedHiggs_HplusTB_HplusToTB_M_" + opts.signal
    # Get list of dataset names
    names = datasetMgr.getAllDatasetNames()

    # Return the index in the list of the first dataset whose name is datasetName
    index = names.index(signalSample)

    # Remove the dataset at the given position in the list, and return it
    names.pop(index)

    # Insert the dataset to the given position  (index) of the list
    names.insert(1, signalSample)

    # Select and reorder Datasets
    datasetMgr.selectAndReorder(names)
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
    global opts
    BATCHMODE = True
    VERBOSE   = False
    OPTMODE   = None
    URL       = True
    SAVEDIR   = None #"/publicweb/a/aattikis/Hplus2tbAnalysis/"
    SIGNAL    = None #"500"

    # Define the available script options
    parser = OptionParser(usage="Usage: %prog [options]" , add_help_option=False,conflict_handler="resolve")

    parser.add_option("-m", "--mcrab", dest="mcrab", action="store", 
                      help="Path to the multicrab directory for input")#, required=True)

    parser.add_option("-o", "--optMode", dest="optMode", type="string", default=OPTMODE, 
                      help="The optimization mode when analysis variation is enabled  [default: %s]" % OPTMODE)

    parser.add_option("-b", "--batchMode", dest="batchMode", action="store_false", default=BATCHMODE, 
                      help="Enables batch mode (canvas creation  NOT generates a window) [default: %s]" % BATCHMODE)

    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=VERBOSE, 
                      help="Enables verbose mode (for debugging purposes) [default: %s]" % VERBOSE)

    parser.add_option("--signal", dest="signal", action="store", type="string", default = SIGNAL,
                      help="Signal mass point to include in plot. (default: %s)" % (SIGNAL))

    parser.add_option("--saveDir", dest="saveDir", type="string", default=SAVEDIR,
                      help="Directory where all pltos will be saved [default: %s]" % SAVEDIR)
    
    parser.add_option("--url", dest="url", action="store_true", default=URL,
                      help="Don't print the actual save path the histogram is saved, but print the URL instead [default: %s]" % URL)
    
    parser.add_option("-i", "--includeOnlyTasks", dest="includeOnlyTasks", action="store", 
                      help="List of datasets in mcrab to include")

    parser.add_option("-e", "--excludeTasks", dest="excludeTasks", action="store", 
                      help="List of datasets in mcrab to exclude")

    (opts, parseArgs) = parser.parse_args()

    # Require at least two arguments (script-name, path to multicrab)
    if opts.mcrab == None:
        Print("Not enough arguments passed to script execution. Printing docstring & EXIT.")
        print __doc__
        sys.exit(0)

    # Call the main function
    main(opts)

    if not opts.batchMode:
        raw_input("=== plotDataMC.py: Press any key to quit ROOT ...")
