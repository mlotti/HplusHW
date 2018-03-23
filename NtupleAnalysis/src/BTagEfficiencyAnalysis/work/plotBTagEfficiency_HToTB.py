#!/usr/bin/env python
'''
DESCRIPTION:
Script that plots the "probability for passing btagging" for 
a) b-jets (b->b)
b) c-jets (c->b)
c) gluon or light-quark jets (guds->b)
as a function of the jet pT


USAGE:
./plotBTagEfficiency_HToTB.py -m <pseudo_mcrab_directory> [opts]


EXAMPLES:
./plotBTagEfficiency_HToTB.py -m BTagEfficiencyAnalysis_HadronFlavour_171115_100257 
./plotBTagEfficiency_HToTB.py -m BTagEfficiencyAnalysis_HadronFlavour_171115_100257 --url --error 0.1 --gridX -e "QCD_HT50to100|QCD_HT100to200|QCD_HT200to300"
./plotBTagEfficiency_HToTB.py -m BTagEfficiencyAnalysis_HadronFlavour_171115_100257 --url --error 0.1 --gridX --gridY -e "QCD_HT50to100|QCD_HT100to200|QCD_HT200to300"
./plotBTagEfficiency_HToTB.py -m BTagEfficiencyAnalysis_180313_104047 --error 0.1 --gridX --gridY -e "QCD_HT50to100|QCD_HT100to200|QCD_HT200to300|WJets" --url

LAST USED:
./plotBTagEfficiency_HToTB.py -m /uscms_data/d3/aattikis/workspace/pseudo-multicrab/BTagEfficiencyAnalysis/multicrab_Hplus2tbAnalysis_v8030_20180223T0905/BTagEfficiencyAnalysis_180313_104047 --error 0.1 --gridX --gridY --url

'''

#================================================================================================ 
# Imports
#================================================================================================ 
import os
import sys
import array
import json
from optparse import OptionParser
import getpass

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.styles as styles
import HiggsAnalysis.NtupleAnalysis.tools.ShellStyles as ShellStyles
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux
import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.analysisModuleSelector as analysisModuleSelector

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

def findModuleNames(multicrabdir, prefix):
    items = os.listdir(multicrabdir)
    for i in items:
        if os.path.isdir(os.path.join(multicrabdir, i)):
            path = ""
            if os.path.exists(os.path.join(multicrabdir, i, "res")):
                path = os.path.join(multicrabdir, i, "res")
            elif os.path.exists(os.path.join(multicrabdir, i, "results")):
                path = os.path.join(multicrabdir, i, "results")
            # Find root file
            newitems = os.listdir(path)
            rootFile = None
            for j in newitems:
                if j.startswith("histograms-") and j.endswith(".root"):
                    rootFile = j
            if rootFile != None:
                f = ROOT.TFile.Open(os.path.join(path, rootFile), "r")
                myList = []
                for key in f.GetListOfKeys():
                    if key.GetClassName() == "TDirectoryFile" and key.ReadObj().GetName().startswith(prefix):
                        myList.append(key.ReadObj().GetName())
                f.Close()
                return myList
    return []

def findProperBinning(hPassed, hAll, binEdges, errorlevel, binIndex=0, minWidth=0):
    # Obtain minimum bin for skipping zero bins 
    myMinBinIndex = binIndex
    if binIndex == -1:
        myMinBinIndex = 999

        # For-loop: All x-axis bins
        for k in range(1, hPassed.GetNbinsX()+1):
            if hAll.GetBinContent(k) > 0:
                myMinBinIndex = min(k,myMinBinIndex)

        # For-loop: Minimum bin edges
        for k in range(0, myMinBinIndex-1):
            binEdges.remove(binEdges[0])

    # Calculate efficiency curve
    tmpContents = []
    # For-loop: All x-axis bins
    for k in range(0, hPassed.GetNbinsX()+2):
        a = hAll.GetBinContent(k)
        b = hPassed.GetBinContent(k)
        tmpContents.append(b)
        if b > a:
            hPassed.SetBinContent(k, a)

    # Save current ROOT ignore verbosity level
    backup = ROOT.gErrorIgnoreLevel
    if opts.muteROOT:
        ROOT.gErrorIgnoreLevel = ROOT.kError
    else:
        ROOT.gErrorIgnoreLevel = ROOT.kWarning

    # Creating efficiency histos
    hEff = ROOT.TEfficiency(hPassed.Clone(), hAll.Clone())

    # Use normal approximation because histograms are weighted
    hEff.SetStatisticOption(ROOT.TEfficiency.kFNormal)

    # Unmute ROOT?
    if not opts.muteROOT:
        ROOT.gErrorIgnoreLevel = backup
    #hEff.SetWeight(1.0)
    
    # For-loop: All x-axis bins
    for k in range(0, hPassed.GetNbinsX()+2):
        hPassed.SetBinContent(k,tmpContents[k])

    # Check if uncertainty is in the given bin
    for k in range(myMinBinIndex, hPassed.GetNbinsX()-1):
        deltaLow = 1.0
        deltaHigh = 1.0
        if hEff.GetEfficiency(k+1) > 0.0:
            deltaLow = hEff.GetEfficiencyErrorLow(k+1)/hEff.GetEfficiency(k+1)
            deltaHigh = hEff.GetEfficiencyErrorUp(k+1)/hEff.GetEfficiency(k+1)

        if max(deltaLow,deltaHigh) > float(errorlevel) or hPassed.GetXaxis().GetBinWidth(k+1) < minWidth-0.1:
            binEdges.remove(hPassed.GetXaxis().GetBinLowEdge(k+2))
            myArray = array.array("d", binEdges)
            hAllNew = hAll.Rebin(len(myArray)-1, "", myArray)
            hPassedNew = hPassed.Rebin(len(myArray)-1, "", myArray)
            w = hPassedNew.GetXaxis().GetBinWidth(k+1)
            if w > minWidth:
                minWidth = w
                #print "setting",minWidth, hPassed.GetXaxis().GetBinLowEdge(k+1), hPassed.GetXaxis().GetBinUpEdge(k+1)
            return findProperBinning(hPassedNew, hAllNew, binEdges, errorlevel, k, minWidth)
    return (hPassed, hAll)

def treatNegativeBins(h):
    for i in range(h.GetNbinsX()+2):
        if h.GetBinContent(i) < 0.0:
            h.SetBinContent(i, 0.0)
    return

def doPlot(name, genuineBDataset, fakeBDataset, errorlevel, optimizationMode, lumi):
    btagWP = "CSVv2-" + name.split("_")[-1]
    Verbose("Generating efficiency for discriminator WP \"%s\"" % (btagWP), True)

    # Definitions
    s = optimizationMode.split("BjetDiscrWorkingPoint")
    discrName      = s[0].replace("OptBjetDiscr", "")
    discrWP        = s[1]
    myPartons      = ["B", "C", "Light"]
    myPartonLabels = ["b#rightarrowb", "c#rightarrowb", "guds#rightarrowb"]
    histoObjects   = []
    results        = []
        
    # For-loop: All partons
    for i, parton in enumerate(myPartons, 0):
        counter = i+1
        msg = "{:<9} {:>3} {:<1} {:<3} {:<50}".format("Histogram", "%d" % counter, "/", "%s:" % (len(myPartons)), "%s->b for %s" % (parton.lower(), btagWP))
        Print(ShellStyles.SuccessStyle() + msg + ShellStyles.NormalStyle(), counter==1)
            
        n = "All%sjets" % parton
        if parton == "B":
            dsetHisto = genuineBDataset.getDatasetRootHisto(n)
        elif (parton == "C" or parton == "Light"):
            dsetHisto = fakeBDataset.getDatasetRootHisto(n)
        else:
             raise Exception("This should never be reached")

        dsetHisto.normalizeToLuminosity(lumi)
        hAll = dsetHisto.getHistogram()

        if hAll == None:
            raise Exception("Error: could not find histogram '%s'!"%n)
        treatNegativeBins(hAll)

        n = "Selected%sjets" % parton
        if parton == "B":  
            dsetHisto = genuineBDataset.getDatasetRootHisto(n)

        if (parton == "C" or parton == "G" or parton == "Light"):
            dsetHisto = fakeBDataset.getDatasetRootHisto(n)

        # Normalise to luminosity
        dsetHisto.normalizeToLuminosity(lumi)

        # Get Numerator. Treate -ve bins
        hPassed = dsetHisto.getHistogram()
        if hPassed == None:
            raise Exception("Error: could not find histogram '%s'!"%n)
        treatNegativeBins(hPassed)

        # Find proper binning
        myBinEdges = []
        for k in range(1, hPassed.GetNbinsX()+1):
            if len(myBinEdges) > 0 or hPassed.GetBinContent(k) > 0:
                myBinEdges.append(hPassed.GetXaxis().GetBinLowEdge(k))
        myBinEdges.append(hPassed.GetXaxis().GetBinUpEdge(hPassed.GetNbinsX()))
        myArray    = array.array("d", myBinEdges)
        hAllNew    = hAll.Rebin(len(myArray)-1, "", myArray)
        hPassedNew = hPassed.Rebin(len(myArray)-1, "", myArray)
        (hPassed, hAll) = findProperBinning(hPassedNew, hAllNew, myBinEdges, errorlevel)

        # For-loop: All x-axis bins
        for k in range(hPassed.GetNbinsX()+2):
            # Treat fluctuations
            if hPassed.GetBinContent(k) > hAll.GetBinContent(k):
                hPassed.SetBinContent(k, hAll.GetBinContent(k))

        # Construct efficiency plot
        eff = ROOT.TEfficiency(hPassed, hAll)
        eff.SetStatisticOption(ROOT.TEfficiency.kFNormal)

        # For-loop: All x-axis bins
        for k in range(hPassed.GetNbinsX()):
            resultObject = {}
            resultObject["flavor"]       = parton
            resultObject["ptMin"]        = hPassed.GetXaxis().GetBinLowEdge(k+1)
            resultObject["ptMax"]        = hPassed.GetXaxis().GetBinUpEdge(k+1)
            resultObject["eff"]          = eff.GetEfficiency(k+1)
            resultObject["effUp"]        = eff.GetEfficiencyErrorUp(k+1)
            resultObject["effDown"]      = eff.GetEfficiencyErrorLow(k+1)
            resultObject["discr"]        = discrName
            resultObject["workingPoint"] = discrWP
            results.append(resultObject)

        # Apply style
        styles.styles[i].apply(eff)
        hobj = histograms.HistoEfficiency(eff, myPartonLabels[i], legendStyle="P", drawStyle="P")
        hobj.setIsDataMC(False, True)
        histoObjects.append(hobj)

    # Create the plot
    myPlot = plots.PlotBase(histoObjects, saveFormats=[])
    myPlot.setLuminosity(lumi)
    myPlot.setEnergy("13")
    #myPlot.setDefaultStyles()

    # Add btag WP to canvas
    myPlot.appendPlotObject(histograms.PlotText(0.70, 0.48-0.16, btagWP, bold=True, size=20))

    # Create the plotting object  
    drawPlot = plots.PlotDrawer(ratio=False, addLuminosityText=False, cmsTextPosition="outframe")

    # Create the plotting object
    drawPlot(myPlot, "%s_%s" % ("Hybrid", name), **GetKwargs(name, btagWP, opts))
    
    # Save the plot in custom formats
    SavePlot(myPlot, name, opts.saveDir, saveFormats = [".C", ".png", ".pdf"])
    return results


def GetKwargs(name, btagWP, opts):
    _moveLegend = {"dx": -0.05, "dy": -0.45-0.16, "dh": -0.15}
    logY        = True
    units       = "GeV/c"
    _xLabel     = "p_{T} (%s)" % (units)
    _yLabel     = "efficiency / " + units
    if "Loose" in btagWP:
        yMin    = 1e-2
    elif "Medium" in btagWP:        
        yMin    = 5e-3
    elif "Tight" in btagWP:        
        yMin    = 1e-4
    else:
        yMin    = 1e-2
            

    if opts.logY:
        yMaxF = 1.2 #10
    else:
        yMaxF = 1.2

    _kwargs = {
        "xlabel"           : _xLabel,
        "ylabel"           : _yLabel,
        "log"              : logY,
        "addLuminosityText": False,
        "addCmsText"       : True,
        "cmsExtraText"     : "Simulation",
        "cmsTextPosition"  : "outframe", # options: left, right, outframe
        #"opts"             : {"xmin":  0.0, "ymin": yMin, "ymaxfactor": yMaxF},
        #"opts"             : {"xmin":  0.0, "ymin": yMin, "ymax": 1.0},
        "opts"             : {"ymin": yMin, "ymax": 1.0},
        "opts2"            : {"ymin": 0.59, "ymax": 1.41},
        "moveLegend"       : _moveLegend,
        #"cutBox"           : {"cutValue": 30.0, "fillColor": 16, "box": True, "line": True, "greaterThan": True}
        #"cutBox"           : {"cutValue": 40.0, "fillColor": 16, "box": True, "line": True, "greaterThan": True}
        }
    ROOT.gStyle.SetNdivisions(1108, "X") #n = n1 + 100*n2 + 10000*n3
    return _kwargs


def SavePlot(plot, plotName, saveDir, saveFormats = [".pdf", ".png", ".C"]):
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


def GetPlotName(opts):
    WP   = "NONE"
    if "Loose" in opts.optMode:
        WP = "CSVv2_Loose"
    if "Medium" in opts.optMode:
        WP = "CSVv2_Medium"
    if "Tight" in opts.optMode:
        WP = "CSVv2_Tight"
        
    #name = "btageff_%s_%s_%s" % (opts.dataEra, opts.searchMode, opts.optMode)
    name = "btageff_%s" % (WP)
    return name


def main(opts):

    # Obtain dsetMgrCreator and register it to module selector
    dsetMgrCreator = dataset.readFromMulticrabCfg(directory=opts.mcrab)
    
    # Get list of eras, modes, and optimisation modes
    erasList      = dsetMgrCreator.getDataEras()
    modesList     = dsetMgrCreator.getSearchModes()
    optList       = dsetMgrCreator.getOptimizationModes()
    sysVarList    = dsetMgrCreator.getSystematicVariations()
    sysVarSrcList = dsetMgrCreator.getSystematicVariationSources()

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    style.setGridX(opts.gridX)
    style.setGridY(opts.gridY)
    style.setOptStat(False)

    # If user does not define optimisation mode do all of them
    if opts.optMode == None:
        optModes = optList
    else:
        optModes = [opts.optMode]

    # Define genuineB and fakeB datasets
    mergeMap = {"TT": "GenuineB",
                "QCD_HT50to100"   : "FakeB", #v. poor stats!
                "QCD_HT200to300"  : "FakeB", #v. poor stats!
                "QCD_HT100to200"  : "FakeB", #v. poor stats!
                "QCD_HT200to300"  : "FakeB", #v. poor stats!
                "QCD_HT300to500"  : "FakeB",
                "QCD_HT500to700"  : "FakeB", 
                "QCD_HT700to1000" : "FakeB",
                "QCD_HT1000to1500": "FakeB",
                "QCD_HT1500to2000": "FakeB", 
                "QCD_HT2000toInf" : "FakeB",
                "WJetsToQQ_HT_600ToInf": "FakeB"
                }
    # Definitions
    results  = []

    # For-loop: All optimisation modes
    for index, opt in enumerate(optModes, 1):
        opts.optMode = opt
        
        # Definitions
        genuineB = None
        fakeB    = None

        # Setup & configure the dataset manager
        datasetsMgr = GetDatasetsFromDir(opts)
        datasetsMgr.updateNAllEventsToPUWeighted()
        datasetsMgr.loadLuminosities() # from lumi.json   
        
        # Print datasets info ?
        if opts.verbose:
            datasetsMgr.PrintCrossSections()
            datasetsMgr.PrintLuminosities()

        # Remove unwanted datasets
        removeList = ["QCD_HT50to100", "QCD_HT100to200", "QCD_HT200to300", "QCD_HT200to300_ext1", "WJetsToQQ_HT_600ToInf"]
        for k, d in enumerate(datasetsMgr.getAllDatasets(), 1):
            if d.getName() in removeList:
                datasetsMgr.remove(d.getName())
                Verbose(ShellStyles.ErrorStyle() + "Removing dataset %s" % d.getName() + ShellStyles.NormalStyle(), k==1)
        if index == 1:
            datasetsMgr.PrintInfo()

        # Merge datasets into two groups: Genuine-B and Fake-B
        datasetsMgr.mergeMany(mergeMap, addition=False)
        for d in datasetsMgr.getAllDatasets():
            if d.getName() == "GenuineB":
                genuineB = d
            if d.getName() == "FakeB":
                fakeB = d

        # Merge histograms (see NtupleAnalysis/python/tools/plots.py)
        plots.mergeRenameReorderForDataMC(datasetsMgr)

        # Get integrated luminosity
        intLumi = datasetsMgr.getDataset("Data").getLuminosity()
        datasetsMgr.remove(filter(lambda name: "Data" in name, datasetsMgr.getAllDatasetNames()))
                    
        # Print dataset information
        if index == 1:
            datasetsMgr.PrintInfo()

        # Do the plot
        name = GetPlotName(opts)
        myResults = doPlot(name, genuineB, fakeB, opts.errorlevel, opts.optMode, intLumi) 
        
        # Save results and msgs
        results.extend(myResults)
        
        # For-loop: All points
        if opts.verbose:
            for item in results:
                print item
    
    # Print path of all saved plots
    msg = "All plots saved under directory %s" % (aux.convertToURL(opts.saveDir, opts.url))
    Print(ShellStyles.SuccessStyle() + msg + ShellStyles.NormalStyle(), True)

    # Write results to a json file
    with open(opts.json, 'w') as outfile:
        json.dump(results, outfile)
    msg = "Wrote results to \"%s\"" % (opts.json)
    Print(ShellStyles.SuccessStyle() + msg + ShellStyles.NormalStyle(), True)
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
    ANALYSISNAME = "BTagEfficiencyAnalysis"
    SEARCHMODE   = "80to1000"
    DATAERA      = "Run2016"
    OPTMODE      = None
    GRIDX        = False
    GRIDY        = False
    LOGY         = True
    ERROR        = 0.05 # 5%
    SAVEDIR      = None
    VERBOSE      = False
    BATCHMODE    = True
    URL          = False
    JSON         = "btageff_HToTB.json"
    MUTEROOT     = True

    # Define the available script options
    parser = OptionParser(usage="Usage: %prog [options]")

    parser.add_option("-m", "--mcrab", dest="mcrab", action="store", 
                      help="Path to the multicrab directory for input")

    parser.add_option("-b", "--batchMode", dest="batchMode", action="store_false", default=BATCHMODE, 
                      help="Enables batch mode (canvas creation does NOT generate a window) [default: %s]" % BATCHMODE)

    parser.add_option("--json", dest="json", action="store", default=JSON, 
                      help="Name of the json file to be produced with the b-tag efficiencies as a function of jet pt [default: %s]" % JSON)

    parser.add_option("--analysisName", dest="analysisName", type="string", default=ANALYSISNAME,
                      help="Override default analysisName [default: %s]" % ANALYSISNAME)
    
    parser.add_option("-o", "--optMode", dest="optMode", type="string", default=OPTMODE,
                      help="The optimization mode when analysis variation is enabled  [default: %s]" % OPTMODE)

    parser.add_option("--dataEra", dest="dataEra", type="string", default=DATAERA, 
                      help="Override default dataEra [default: %s]" % DATAERA)

    parser.add_option("--searchMode", dest="searchMode", type="string", default=SEARCHMODE,
                      help="Override default searchMode [default: %s]" % SEARCHMODE)

    parser.add_option("--gridX", dest="gridX", action="store_true", default=GRIDX, 
                      help="Enable the x-axis grid lines [default: %s]" % GRIDX)

    parser.add_option("--gridY", dest="gridY", action="store_true", default=GRIDY, 
                      help="Enable the y-axis grid lines [default: %s]" % GRIDY)

    parser.add_option("--logY", dest="logY", action="store_true", default=LOGY, 
                      help="Set the y-axis to logarithmic scale [default: %s]" % LOGY)

    parser.add_option("--saveDir", dest="saveDir", type="string", default=SAVEDIR, 
                      help="Directory where all pltos will be saved [default: %s]" % SAVEDIR)

    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=VERBOSE, 
                      help="Enables verbose mode (for debugging purposes) [default: %s]" % VERBOSE)

    parser.add_option("--url", dest="url", action="store_true", default=URL, 
                      help="Don't print the actual save path the histogram is saved, but print the URL instead [default: %s]" % URL)

    parser.add_option("-i", "--includeOnlyTasks", dest="includeOnlyTasks", action="store", 
                      help="List of datasets in mcrab to include")

    parser.add_option("-e", "--excludeTasks", dest="excludeTasks", action="store", 
                      help="List of datasets in mcrab to exclude")

    parser.add_option("--error", dest="errorlevel", action="store", default=ERROR,
                      help="Maximum relative uncertainty per bin (default=%s)" %  ERROR)

    parser.add_option("--muteROOT", dest="muteROOT", action="store_true", default=MUTEROOT,
                      help="Disable printing of warning from ROOT (default=%s)" %  MUTEROOT)

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


    if opts.saveDir == None:
        opts.saveDir = aux.getSaveDirPath(opts.mcrab, prefix="", postfix="")

    # Call the main function
    main(opts)

    if not opts.batchMode:
        raw_input("=== plotBTagEfficiency_HToTB.py: Press any key to quit ROOT ...")

