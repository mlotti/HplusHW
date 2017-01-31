#!/usr/bin/env python
'''
Description:

Usage:
hplusPrintCounters.py --mainCounterOnly  <pseudo-multicrab-dir>
or 
cd <pseudo-multicrab-dir> && hplusPrintCounters.py hplusPrintCounters.py --mainCounterOnly
            
Usage (advanced):
hplusPrintCounters.py --mainCounterOnly --noinfo --verbose --weighted --dataEra "Run2016" --mergeData
hplusPrintCounters.py --dataEra "Run2016" --printInfo --mode "events" --mergeForDataMC --weighted
hplusPrintCounters.py --dataEra "Run2016" --printInfo --mode "eff" --mergeForDataMC
hplusPrintCounters.py --dataEra "Run2016" --printInfo --mergeForDataMC --mode "events" --weighted --includeTasks "QCD_Pt|TT_ext3|ZJets|Run2016G|Run2016F_PromptReco_v1_278801_278808" --mainCounterOnly


Useful Links:
https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsChFullyHadronic
'''

#================================================================================================
# Import Modules
#================================================================================================  
import os
import sys
import glob
import re
from optparse import OptionParser

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

import HiggsAnalysis.NtupleAnalysis.tools.multicrab as multicrab
import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import HiggsAnalysis.NtupleAnalysis.tools.counter as counter
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots


#================================================================================================
# Function Definition
#================================================================================================
def Verbose(msg, printHeader=False):
    '''
    Calls Print() only if verbose options is set to true.
    '''
    if not opts.verbose:
        return
    Print(msg, printHeader)
    return


def Print(msg, printHeader=True):
    '''
    Simple print function. If verbose option is enabled prints, otherwise does nothing.
    '''
    fName = __file__.split("/")[-1]
    if printHeader==True:
        print "=== ", fName
        print "\t", msg
    else:
        print "\t", msg
    return


def GetRegularExpression(arg):
    Verbose("GetRegularExpression()", True)
    if isinstance(arg, basestring):
        arg = [arg]
    return [re.compile(a) for a in arg]


def FilterDatasets(datasetsMgr, opts):
    Verbose("FiltereDatasets()", True)

    # Optional: Apply include/exclude datasets
    for d in datasetsMgr.getAllDatasets():

        # Exclude datasets
        if opts.excludeTasks != "":
            exclude = GetRegularExpression(opts.excludeTasks)
            for e_re in exclude:
                if e_re.search(d.getName()):
                    datasetsMgr.remove(d.getName())

        # Include datasets
        if opts.includeTasks != "":
            include = GetRegularExpression(opts.includeTasks)
            for i_re in include:
                if i_re.search(d.getName()):
                    pass
                else:
                    datasetsMgr.remove(d.getName())
    return datasetsMgr


#================================================================================================
# Main Function
#================================================================================================
def main(opts):

    datasetsMgr = None
    # Fixme: This options is currently invalid
    if len(opts.files) > 0:
        datasetsMgr = dataset.getDatasetsFromRootFiles( [(x,x) for x in opts.files], opts=opts, weightedCounters=opts.weighted)
    else:
        # Define the cwd as the multicrab dir containing the ROOT files with the counters
        multicrabDir = os.getcwd()
        
        # For-loop: All arguments passed during script execution
        for d in sys.argv:
            # Look for a directory that exists
            if os.path.exists(d) and os.path.isdir(d):
                multicrabDir = os.path.abspath(d)

        Print("The multicrab directory to be used is %s" % (multicrabDir), True)
        # Get the datasets    
        datasetsMgr = dataset.getDatasetsFromMulticrabDirs([multicrabDir],opts=opts, weightedCounters=opts.weighted)

    # Optional: Apply include/exclude datasets
    datasetsMgr = FilterDatasets(datasetsMgr, opts)
    Print("The tasks to be included are:\n\t%s" % ("\n\t".join(d.getName() for d in datasetsMgr.getAllDatasets())), True)


    # Optional: Print info on Data and MC samples
    if opts.verbose:
        datasetsMgr.PrintCrossSections()
        datasetsMgr.PrintLuminosities()
    
    # Load the luminosities
    if os.path.exists(opts.lumifile):
        datasetsMgr.loadLuminosities(opts.lumifile)

    # Optional: Apply PU-reweighting
    if opts.weighted and opts.PUreweight:
        Print("Updating all events to PU-weighted (opts.weighted=%s, opts.PUreweight=%s)\n" % (opts.weighted, opts.PUreweight), True)
        datasetsMgr.updateNAllEventsToPUWeighted(era=opts.dataEra)
    
    # Optional: Merge data
    Verbose("Merging Data and/or MC datatets (opts.mergeData=%s, opts.mergeData=%s, opts.mergeData=%s)" % (opts.mergeData, opts.mergeMC, opts.mergeForDataMC), True)
    if opts.mergeData:
        datasetsMgr.mergeData()
    if opts.mergeMC:
        datasetsMgr.mergeMC()
    if opts.mergeForDataMC:
        plots.mergeRenameReorderForDataMC(datasetsMgr)

    # Optional: Print dataset info
    if opts.printInfo:
        datasetsMgr.PrintInfo() #datasetsMgr.printInfo()

    # Create the event counter
    eventCounter = counter.EventCounter(datasetsMgr)

    # Proceed differently depending on operation mode (opts.mode= 'events', 'xsect', 'eff')
    quantity = "events"
    if opts.mode == "events":        
        if opts.mergeForDataMC:
            Print("Normalising the MC histograms to the data luminosity (opts.mergeForDataMC=%s)" % (opts.mergeForDataMC) )
            eventCounter.normalizeMCByLuminosity()
        else:
            pass
    elif opts.mode in ["xsect", "xsection", "crosssection", "crossSection", "eff"]:
        if not opts.PUreweight:
            Print("Mode '%s' works only with PU reweighting, which you disabled with --noPUreweight" % opts.mode)
            return 1
        Print("Normalising MC by cross-section (opt.mode=%s)" % opts.mode)
        eventCounter.normalizeMCByCrossSection()
        quantity = "MC by cross section, data by events"
    else:
        Print("Printing mode '%s' doesn't exist! The following ones are available 'events', 'xsect', 'eff'" % opts.mode)
        return 1

    # Optional: Produce table in Text or LaTeX format?
    if opts.latex:
        cellFormat  = counter.CellFormatTeX(valueOnly=opts.valueOnly, valueFormat=opts.format)
        formatFunc = lambda table: table.format(counter.TableFormatLaTeX(cellFormat))
    else:
        cellFormat  = counter.CellFormatText(valueOnly=opts.valueOnly, valueFormat=opts.format)
        formatFunc = lambda table: table.format(counter.TableFormatText(cellFormat))
    csvSplitter = counter.TableSplitter([" +- ", " +", " -"])

    # Optional: Format as comma-separated-variables (csv), presubambly for exporting to a spreadsheet
    if opts.csv:
        formatFunc = lambda table: table.format(counter.TableFormatText(cellFormat, columnSeparator=","), csvSplitter)

    # Optional: Convert to (relative) efficienies
    if opts.mode == "eff":
        if opts.weighted:
            Print("Cannot operate in \"eff\" mode while using weighted counters (opts.mode=\'%s\', opts.weighted=%s)" % (opts.mode, opts.weighted) )
            return 1
        else:            
            Print("Converting to efficiencies (opts.mode=%s)" % (opts.mode) )

        cellFormat = counter.CellFormatText(valueFormat="%.4f", valueOnly=opts.valueOnly)
        if opts.latex:
            formatFunc = lambda table: counter.counterEfficiency(table).format(counter.TableFormatLaTeX(cellFormat))
        else:
            formatFunc = lambda table: counter.counterEfficiency(table).format(counter.TableFormatText(cellFormat))
        quantity = "Cut efficiencies"
        # Optional: Format as comma-separated-variables (csv), presubambly for exporting to a spreadsheet
        if opts.csv:
            formatFunc = lambda table: counter.counterEfficiency(table).format(counter.TableFormatText(cellFormat, columnSeparator=","), csvSplitter)

    # Optional: Print only this sub-counters
    if opts.subCounter is not None:
        msg = "Subcounter %s %s: " % (opts.subCounter, quantity)
        Print(msg, True)
        print formatFunc(eventCounter.getSubCounterTable(opts.subCounter))
        print
        return 0

    # Print the main counters
    hLine = "="*10
    msg = " Main counter %s: " % quantity
    print "\n" + hLine + msg + hLine
    print formatFunc(eventCounter.getMainCounterTable())
    print 

    # Optional: Print sub-counters (only if --mainCounterOnly is not called)
    if not opts.mainCounterOnly:
        names = eventCounter.getSubCounterNames()
        names.sort()
        for name in names:
            hLine = "="*10
            msg = " Subcounter %s %s: " % (name, quantity)
            print "\n" + hLine + msg + hLine
            print formatFunc(eventCounter.getSubCounterTable(name) )

    return 0


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

    # Default Values
    VERBOSE           = False
    WEIGHTED          = False
    PU_REWEIGHT       = True
    MODE              = "events"
    CSV               = False
    MAIN_COUNTER_ONLY = False
    SUB_COUNTER       = None
    FORMAT            = "%.1f"
    LUMI_FILE         = "lumi.json"
    PRINT_INFO        = False
    NO_ERROR          = False
    MERGE_DATA        = False
    MERGE_MC          = False
    MERGE_FOR_DATAMC  = False
    LATEX             = False

    # Built the parser
    parser = OptionParser(usage="Usage: %prog [options] [crab task dirs]\n\nCRAB task directories can be given either as the last arguments, or with -d.")
    multicrab.addOptions(parser)
    dataset.addOptions(parser)
    
    parser.add_option("-v", "--verbose", dest="verbose", default=VERBOSE, action="store_true", 
                      help="Verbose mode for debugging purposes [default: False]")

    parser.add_option("--weighted", dest="weighted", default=WEIGHTED, action="store_true",
                      help="Use weighted counters (i.e. adds '/weighted' to the counter directory path) [default: %s]" % (WEIGHTED) )

    parser.add_option("--noPUreweight", dest="PUreweight", default=PU_REWEIGHT, action="store_false",
                      help="Don't use PU weighted number of all events. Works only with 'events' mode [defaults: %s" % (PU_REWEIGHT) )

    parser.add_option("--mode", "-m", dest="mode", type="string", default=MODE,
                      help="Output mode; available: 'events', 'xsect', 'eff' [default: %s]" % MODE)

    parser.add_option("--csv", dest="csv", action="store_true", default=CSV,
                      help="Print in CSV format [default: %s]" % (CSV) )

#    parser.add_option("--format", "-f", dest="format", type="string", default="text",
#                      help="Output format; available: 'text' (default: 'text')")

    parser.add_option("--mainCounterOnly", dest="mainCounterOnly", action="store_true", default=MAIN_COUNTER_ONLY,
                      help="By default the main counter and the subcounters are all printed. With this option only the main counter is printed [default: %s]" % (MAIN_COUNTER_ONLY) )

    parser.add_option("--subCounter", dest="subCounter", type="string", default=SUB_COUNTER,
                      help="If given, print only this subcounter [default: %s]" % (SUB_COUNTER) )

    parser.add_option("--format", dest="format", default=FORMAT,
                       help="Value format string [default: %s]" % (FORMAT) )

    parser.add_option("--lumifile", dest="lumifile", type="string", default=LUMI_FILE,
                      help="The JSON file to contain the dataset integrated luminosities [default: %s]" % (LUMI_FILE) )

    parser.add_option("--printInfo", dest="printInfo", action="store_true", default=PRINT_INFO,
                      help="Print the dataset info [default: %s]" % (PRINT_INFO) )

    parser.add_option("--noerror", dest="valueOnly", action="store_true", default=NO_ERROR,
                      help="Don't print statistical errors [default: %s]" % (NO_ERROR) )

    parser.add_option("--mergeData", dest="mergeData", action="store_true", default=MERGE_DATA,
                      help="Merge all data datasets [default: %s]" % (MERGE_DATA) )

    parser.add_option("--mergeMC", dest="mergeMC", action="store_true", default=MERGE_MC,
                      help="Merge all MC datasets into a single dataset [default: %s]" % (MERGE_MC) )

    parser.add_option("--mergeForDataMC", dest="mergeForDataMC", action="store_true", default=MERGE_FOR_DATAMC,
                      help="Merge all Data and MC datasets ala Data/MC plots [default: %s]" % (MERGE_FOR_DATAMC) )

    parser.add_option("--latex", dest="latex", action="store_true", default=LATEX,
                      help="The table formatting is in LaTeX instead of plain text (ready for generation)  [default: %s]" % (LATEX) )

    parser.add_option("--includeTasks", dest="includeTasks", default="", type="string", 
                      help="Only perform action for this dataset(s) [default: \"\"]")

    parser.add_option("--excludeTasks", dest="excludeTasks", default="", type="string", 
                      help="Exclude this dataset(s) from action [default: \"\"]")


    (opts, args) = parser.parse_args()
    opts.dirs.extend(args)
    sys.exit(main(opts))
