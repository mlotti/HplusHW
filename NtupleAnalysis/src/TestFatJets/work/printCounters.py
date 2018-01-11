#!/usr/bin/env python
'''
Description:
Scipt that print most relevant counters for FakeBMeasurement.cc class. 

For the definition of the counter class see:
HiggsAnalysis/NtupleAnalysis/scripts

For more counter tricks and optios see also:
HiggsAnalysis/NtupleAnalysis/scripts/hplusPrintCounters.py

Usage:
./printCounters.py -m <pseudo-multicrab_dir> [opts]

Commonly Used Commands:
./printCounters.py -m <pseudo-multicrab_dir> --fractionEWK --mergeEWK --valueFormat %.2f --latex
./printCounters.py -m <pseudo-multicrab_dir> --mergeEWK --valueFormat %.0f --latex

Examples:
./printCounters.py -m <multicrab_dir> -i "JetHT|TT"
./printCounters.py -m <multicrab_dir> --format %.3f --latex
./printCounters.py -m <multicrab_dir> --format %.3f --precision 3 --mergeEWK
./printCounters.py -m <multicrab_dir> --format %.3f --precision 3 --mergeEWK --latex -s
./printCounters.py -m <multicrab_dir> --format %.3f --precision 3 --mergeEWK --latex -s --histoLevel Debug
./printCounters.py -m <multicrab_dir> --mcOnly --intLumi 100000
./printCounters.py -m <multicrab_dir> --fractionEWK
./printCounters.py -m <multicrab_dir> --subcounters
./printCounters.py -m <multicrab_dir> -i "2016B|TTTT"
./printCounters.py -m <multicrab_dir> -e "2016B|TTTT"
./printCounters.py -m <multicrab_dir> --latex
./printCounters.py -m <multicrab_dir> --valueFormat %.2f
./printCounters.py -m <multicrab_dir> --withPrecision 3
./printCounters.py -m <multicrab_dir> --valueOnly
./printCounters.py -m <multicrab_dir> --uncertaintyFormat %.2f
./printCounters.py -m <multicrab_dir> --uncertaintyPrecision 4

Last Used:
./printCounters.py -m Hplus2tbAnalysis_StdSelections_TopCut100_AllSelections_NoTrgMatch_TopCut10_H2Cut0p5_170827_075947 --valueFormat %.3f --withPrecision 3 -e "QCD|M_"
./printCounters.py -m Hplus2tbAnalysis_StdSelections_TopCut100_AllSelections_NoTrgMatch_TopCut10_H2Cut0p5_170827_075947 --valueFormat %.3f --withPrecision 3 --mergeEWK
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
    Print(msg, printHeader)
    return


def GetLumi(datasetsMgr):
    Verbose("Determining Integrated Luminosity")
    
    lumi = 0.0
    for d in datasetsMgr.getAllDatasets():
        if d.isMC():
            continue
        else:
            lumi += d.getLuminosity()
    Verbose("Luminosity = %s (pb)" % (lumi), True)
    return lumi


    # Only keep selected rows
def GetRowNameLaTeXDict():
    Verbose("Creating row-name dictionary (oldname->new name)")
    mapping = {
        "Passed trigger"                      : "Trigger",
        "passed METFilter selection ()"       : "MET filter",
        "Passed PV"                           : "PV",
        "passed e selection (Veto)"           : "\lE{\pm} Veto",
        "passed mu selection (Veto)"          : "\lMu{\pm} Veto",
        "Passed tau selection (Veto)"         : "\lTauJet Veto",
        "passed jet selection ()"             : "Jets",
        "Baseline: passed b-jet selection"    : "Baseline: \\bJets",
        "Baseline: b tag SF"                  : "Baseline: \\bJets SF",
        "passed topology selection (Baseline)": "Baseline: Topology",
        "passed top selection (Baseline)"     : "Baseline: Top",
        "Baseline: selected events"           : "Baseline: Selected",
        "Baseline: passed b-jet veto"         : "Baseline: \\bJets",
        "Baseline: b tag SF"                  : "Baseline: \\bJets SF",
        "passed topology selection (Baseline)": "Baseline: Topology",
        "passed top selection (Baseline)"     : "Baseline: Top",
        "Baseline: selected events"           : "Baseline: Selected",
        }
    return mapping


def GetListOfEwkDatasets():
    Verbose("Getting list of EWK datasets")
    #return ["TT", "DYJetsToQQHT", "TTWJetsToQQ", "WJetsToQQ_HT_600ToInf", "SingleTop", "Diboson", "TTZToQQ", "TTTT"]
    return ["TT", "WJetsToQQ_HT_600ToInf", "DYJetsToQQHT", "SingleTop", "TTWJetsToQQ", "TTZToQQ", "Diboson", "TTTT"]


def GetDatasetsFromDir(opts):
    Verbose("Getting datasets")
    
    if (not opts.includeOnlyTasks and not opts.excludeTasks):
        datasets = dataset.getDatasetsFromMulticrabDirs([opts.mcrab],
                                                        dataEra=opts.dataEra,
                                                        searchMode=opts.searchMode, 
                                                        analysisName=opts.analysisName)
    elif (opts.includeOnlyTasks):
        datasets = dataset.getDatasetsFromMulticrabDirs([opts.mcrab],
                                                        dataEra=opts.dataEra,
                                                        searchMode=opts.searchMode,
                                                        analysisName=opts.analysisName,
                                                        includeOnlyTasks=opts.includeOnlyTasks)
    elif (opts.excludeTasks):
        datasets = dataset.getDatasetsFromMulticrabDirs([opts.mcrab],
                                                        dataEra=opts.dataEra,
                                                        searchMode=opts.searchMode,
                                                        analysisName=opts.analysisName,
                                                        excludeTasks=opts.excludeTasks)
    else:
        raise Exception("This should never be reached")
    return datasets
    

def main(opts):
    Verbose("main function")

    comparisonList = ["AfterStdSelections"]

    # Setup & configure the dataset manager 
    datasetsMgr = GetDatasetsFromDir(opts)
    datasetsMgr.updateNAllEventsToPUWeighted()
    datasetsMgr.loadLuminosities() # from lumi.json
    if opts.verbose:
        datasetsMgr.PrintCrossSections()
        datasetsMgr.PrintLuminosities()

    # Check multicrab consistency
    # consistencyCheck.checkConsistencyStandalone(dirs[0],datasets,name="CorrelationAnalysis")

    # Custom Filtering of datasets 
    # datasetsMgr.remove(filter(lambda name: "HplusTB" in name and not "M_500" in name, datasetsMgr.getAllDatasetNames()))
    # datasetsMgr.remove(filter(lambda name: "ST" in name, datasetsMgr.getAllDatasetNames()))
               
    # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
    plots.mergeRenameReorderForDataMC(datasetsMgr)
   
    # Print dataset information
    datasetsMgr.PrintInfo()

    # Re-order datasets
    newOrder = ["Data"] #, "TT", "DYJetsToQQHT", "TTWJetsToQQ", "WJetsToQQ_HT_600ToInf", "SingleTop", "Diboson", "TTZToQQ", "TTTT"]
    newOrder.extend(GetListOfEwkDatasets())
    if opts.mcOnly:
        newOrder.remove("Data")
    #datasetsMgr.selectAndReorder(newOrder)

    # Merge EWK samples (done later on)
    #if opts.mergeEWK:
    #    datasetsMgr.merge("EWK", GetListOfEwkDatasets())

    # Do default counters
    doCounters(datasetsMgr)

    return


def doCounters(datasetsMgr):
    '''
    Print values for counters and sub-counters (if -s option is invoked)

    Options:
    --latex (The table formatting is in LaTeX instead of plain text)
    --format (The table value-format of strings)
    --precision (The table value-precision)
    --mergeEWK (Merge all EWK samples into a single sample called EWK)
    -i (List of datasets in mcrab to include)
    -e (List of datasets in mcrab to exclude)
    '''
    Verbose("Doing the counters")

    # Definitions
    eventCounter = counter.EventCounter(datasetsMgr)
    ewkDatasets  = GetListOfEwkDatasets()

    # Normalize MC samples accordingly
    if opts.mcOnly and opts.intLumi>-1.0:
        eventCounter.normalizeMCToLuminosity(opts.intLumi)
    else:
        eventCounter.normalizeMCByLuminosity()
        # eventCounter.normalizeMCByCrossSection()

    # Construct the table
    mainTable = eventCounter.getMainCounterTable()

    # Only keep selected rows
    rows = [
        #"ttree: skimCounterAll",
        #"ttree: skimCounterPassed",
        #"Base::AllEvents", 
        #"Base::PUReweighting",
        #"Base::Prescale", 
        #"Base::Weighted events with top pT",
        #"Base::Weighted events for exclusive samples",
        "All events",
        "Passed trigger",
        "passed METFilter selection ()",
        "Passed PV",
        "passed e selection (Veto)",
        "passed mu selection (Veto)",
        "Passed tau selection (Veto)",
        #"Passed tau selection and genuine (Veto)",
        "passed jet selection ()",
        "passed b-jet selection ()",
        #"passed light-jet selection ()",
        #"Baseline: passed b-jet selection",
        "passed b-jet selection",
        "b tag SF",
        #"passed MET selection (Baseline)",
        "passed topology selection (Baseline)",
        "passed top selection (Baseline)",
        "selected events",
        "passed b-jet veto",
        "b tag SF",
        #"passed MET selection (Baseline)",
        "passed topology selection (Baseline)",
        "passed top selection (Baseline)",
        "selected events"
        ]

    Print("Print only custom rows!", True)
    if 0:
        mainTable.keepOnlyRows(rows)

    # Get number of rows/columns
    nRows    = mainTable.getNrows()
    nColumns = mainTable.getNcolumns()

    # Merge EWK into a new column
    if opts.mergeEWK:
        mainTable.insertColumn(nColumns, counter.sumColumn("EWK", [mainTable.getColumn(name=name) for name in ewkDatasets]))

    # Additional column (through inter-column operations)
    if opts.mergeEWK:
        mainTable.insertColumn(mainTable.getNcolumns(), counter.subtractColumn("Data-EWK", mainTable.getColumn(name="Data"), mainTable.getColumn(name="EWK") ) )
        mainTable.insertColumn(mainTable.getNcolumns(), counter.divideColumn("QCD Purity", mainTable.getColumn(name="Data-EWK"), mainTable.getColumn(name="Data") ) )
        # Convert "QCD Purity" from Fraction to Percent (%)
        mainTable.getColumn(name="QCD Purity").multiply(100)
    
    # Define which columns to keep
    columnsToKeep = ["Data", "EWK", "QCD Purity"]
    
    if opts.fractionEWK:
        columnsToKeep = [] # columnsToKeep = ["Data", "EWK"]
        for d in  GetListOfEwkDatasets():
            columnName = d + "/EWK"
            mainTable.insertColumn(mainTable.getNcolumns(), counter.divideColumn(columnName, mainTable.getColumn(name=d), mainTable.getColumn(name="EWK") ) )
            # Convert EWK Fraction to EWK Percent (%)
            mainTable.getColumn(name=columnName).multiply(100)
            columnsToKeep.append(columnName)

    # Remove all columns that are not needed
    if opts.mergeEWK:
        mainTable.keepOnlyColumns(columnsToKeep)
    
    # Optional: Produce table in Text or LaTeX format?
    if opts.latex:
        mainTable.renameRows(GetRowNameLaTeXDict())
        cellFormat = counter.TableFormatLaTeX(counter.CellFormatTeX(valueOnly = opts.valueOnly, 
                                                                    valueFormat = opts.valueFormat, 
                                                                    withPrecision = opts.withPrecision,
                                                                    uncertaintyFormat = opts.uncertaintyFormat, 
                                                                    uncertaintyPrecision = opts.uncertaintyPrecision))

    else:
        cellFormat = counter.TableFormatText(cellFormat=counter.CellFormatText(valueOnly = opts.valueOnly, 
                                                                               valueFormat = opts.valueFormat, 
                                                                               withPrecision = opts.withPrecision, 
                                                                               uncertaintyFormat = opts.uncertaintyFormat, 
                                                                               uncertaintyPrecision = opts.uncertaintyPrecision))
    print mainTable.format(cellFormat)

    # Do sub-counters?
    subcounters = [
        "bjet selection ()",
        "e selection (Veto)",
        "jet selection ()",
        #"light-jet selection ()", 
        "METFilter selection",
        "METFilter selection ()", 
        "mu selection (Veto)", 
        "tau selection (Veto)",
        "top selection (Baseline)",
        "top selection (Baseline)",
        "topology selection (Baseline)",
        "topology selection (Baseline)"
        ]

    if opts.subcounters:
        for sc in subcounters:
            Print("\nSub-counter \"%s\"" % (sc), False)
            print eventCounter.getSubCounterTable(sc).format(cellFormat)
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
    ANALYSISNAME    = "Hplus2tbAnalysis" #"FakeBMeasurement"
    DATAERA         = "Run2016"
    SEARCHMODE      = "80to1000"
    VALUEFORMAT     = "%.6f"
    UNCERTFORMAT    = VALUEFORMAT
    UNCERTPRECISION = 4
    WITHPRECISION   = None #2 
    VALUEONLY       = True
    INTLUMI         = -1.0
    SUBCOUNTERS     = False
    LATEX           = False
    MCONLY          = False
    MERGEEWK        = False
    FRACTIONEWK     = False
    SAVEDIR         = "" #"/publicweb/a/aattikis/FakeBMeasurement/"
    VERBOSE         = False
    
    # Define the available script options
    parser = OptionParser(usage="Usage: %prog [options]")

    parser.add_option("-m", "--mcrab", dest="mcrab", action="store", 
                      help="Path to the multicrab directory for input")

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

    parser.add_option("--fractionEWK", dest="fractionEWK", action="store_true", default=FRACTIONEWK, 
                      help="The contribution of each sample to the total EWK  will also be calculated [default: %s]" % FRACTIONEWK)

    parser.add_option("--saveDir", dest="saveDir", type="string", default=SAVEDIR, 
                      help="Directory where all pltos will be saved [default: %s]" % SAVEDIR)
    
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=VERBOSE, 
                      help="Enables verbose mode (for debugging purposes) [default: %s]" % VERBOSE)

    parser.add_option("-s", "--subcounters", dest="subcounters", action="store_true", default=SUBCOUNTERS, 
                      help="Print also the sub-counters [default: %s]" % SUBCOUNTERS)

    parser.add_option("-i", "--includeOnlyTasks", dest="includeOnlyTasks", action="store", 
                      help="List of datasets in mcrab to include")

    parser.add_option("-e", "--excludeTasks", dest="excludeTasks", action="store", 
                      help="List of datasets in mcrab to exclude")

    parser.add_option("--latex", dest="latex", action="store_true", default=LATEX,
                      help="The table formatting is in LaTeX instead of plain text (ready for generation)  [default: %s]" % (LATEX) )
    
    parser.add_option("--valueFormat", dest="valueFormat", default=VALUEFORMAT,
                      help="The format string for float values [default: %s]" % (VALUEFORMAT) )

    parser.add_option("--withPrecision", dest="withPrecision", type=int, default=WITHPRECISION,
                      help="Number of digits in uncertainty to report the value and uncertainty. If specified, overrides valueFormat, uncertaintyFormat, and uncertaintyPrecision [default: %s]" % (WITHPRECISION) )

    parser.add_option("--valueOnly", dest="valueOnly", action="store_true", default=VALUEONLY,
                      help="Boolean, format the value only? (enable to disable the printing statistical errors [default: %s]" % (VALUEONLY) )

    parser.add_option("--uncertaintyFormat", dest="uncertaintyFormat", default=UNCERTFORMAT,
                      help="Format string for uncertainties [default: %s]" % (UNCERTFORMAT) )

    parser.add_option("--uncertaintyPrecision", dest="uncertaintyPrecision", default=UNCERTPRECISION,
                      help="Number of digits to use for comparing if the lower and upper uncertainties are equal [default: %s]" % (UNCERTPRECISION) )

    (opts, parseArgs) = parser.parse_args()

    # Require at least two arguments (script-name, path to multicrab)
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    if opts.mcrab == None:
        Print("Not enough arguments passed to script execution. Printing docstring & EXIT.")
        parser.print_help()
        # print __doc__
        sys.exit(1)

    if opts.mcOnly:
        if opts.intLumi<0:
            Print("In order to use only MC samples you must provide a value for integrate lumi through --intLumi <value>")
            sys.exit(1)
    
    if  opts.fractionEWK and not opts.mergeEWK:
        Print("In order to use --fractionEWK the --mergeEWK optionm must also be called.")
        #opts.mergeEWK = True
        sys.exit(1)
              
            
    # Call the main function
    main(opts)
