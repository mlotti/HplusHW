#!/usr/bin/env python
'''
INSTRUCTIONS:
The required minimum input is a multiCRAB directory with at least one dataset. If successfull
a pseudo multiCRAB with name "analysis_YYMMDD_HHMMSS/" will be created, inside which each
dataset has its own directory with the results (ROOT files with histograms). These can be later
used as input to plotting scripts to get the desired results.

USAGE:
./run.py -m <path-to-multicrab-directory> -n 10 -e "Keyword1|Keyword2|Keyword3"

Example:
./run.py -m <path-to-multicrab-directory> --analysisType HToTB
./run.py -m <path-to-multicrab-directory> -n 1000 -e "Charged"
./run.py -m <path-to-multicrab-directory> -n 1000 -i "QCD|TT|WJets"

ROOT:
The available ROOT options for the Error-Ignore-Level are (const Int_t):
        kUnset    =  -1
        kPrint    =   0
        kInfo     =   1000
        kWarning  =   2000
        kError    =   3000
        kBreak    =   4000

HistoLevel:
For the histogramAmbientLevel each DEEPER level is a SUBSET of the rest. 
For example "kDebug" will include all kDebug histos but also kInformative, kVital, kSystematics, and kNever.  
Setting histogramAmbientLevel=kSystematics will include kSystematics AND kNever.
    1. kNever = 0,
    2. kSystematics,
    3. kVital,
    4. kInformative,
    5. kDebug,
    6. kNumberOfLevels
'''

#================================================================================================
# Imports
#================================================================================================
import sys
from optparse import OptionParser

from HiggsAnalysis.NtupleAnalysis.main import Process, PSet, Analyzer
from HiggsAnalysis.NtupleAnalysis.AnalysisBuilder import AnalysisBuilder


import ROOT
    
#================================================================================================
# Options
#================================================================================================
prefix      = "BTagEfficiencyAnalysis"
postfix     = ""
dataEras    = ["2016"]
searchModes = ["80to1000"]

ROOT.gErrorIgnoreLevel = 0 


#================================================================================================
# Function Definition
#================================================================================================
def Verbose(msg, printHeader=False):
    if not opts.verbose:
        return

    if printHeader:
        print "=== run.py:"

    if msg !="":
        print "\t", msg
    return


def Print(msg, printHeader=True):
    if printHeader:
        print "=== run.py:"

    if msg !="":
        print "\t", msg
    return


def AskUser(msg, printHeader=False):
    '''
    Prompts user for keyboard feedback to a certain question.
    Returns true if keystroke is \"y\", false otherwise.
    '''
    Verbose("AskUser()", printHeader)

    keystroke = raw_input("=== run.py:\n\t" +  msg + " (y/n): ")
    if (keystroke.lower()) == "y":
        return
    elif (keystroke.lower()) == "n":
        Print("EXIT!", True)
        sys.exit()
    else:
        AskUser(msg)


#================================================================================================
# Setup the main function
#================================================================================================
def main():

    # Require at least two arguments (script-name, path to multicrab)      
    if len(sys.argv) < 2:
        Print("Not enough arguments passed to script execution. Printing docstring & EXIT.")
        print __doc__
        sys.exit(0)
    else:
        pass
        

    # ================================================================================================
    # Setup the process
    # ================================================================================================
    process = Process(prefix, postfix, opts.nEvts)

            
    # ================================================================================================
    # Add the datasets (according to user options)
    # ================================================================================================
    if (opts.includeOnlyTasks):
        Print("Adding only dataset %s from multiCRAB directory %s" % (opts.includeOnlyTasks, opts.mcrab))
        process.addDatasetsFromMulticrab(opts.mcrab, includeOnlyTasks=opts.includeOnlyTasks)
    elif (opts.excludeTasks):
        Print("Adding all datasets except %s from multiCRAB directory %s" % (opts.excludeTasks, opts.mcrab))
        Print("If collision data are present, then vertex reweighting is done according to the chosen data era (era=2015C, 2015D, 2015) etc...")
        process.addDatasetsFromMulticrab(opts.mcrab, excludeTasks=opts.excludeTasks)
    else:
        Print("Adding all datasets from multiCRAB directory %s" % (opts.mcrab))
        Print("If collision data are present, then vertex reweighting is done according to the chosen data era (era=2015C, 2015D, 2015) etc...")
        process.addDatasetsFromMulticrab(opts.mcrab)


    # ================================================================================================
    # Selection customisations
    # ================================================================================================
    if opts.analysisType == "HToTauNu":
        from HiggsAnalysis.NtupleAnalysis.parameters.signalAnalysisParameters import allSelections
        # Disable rtau
        allSelections.TauSelection.prongs = 1
        allSelections.TauSelection.rtau = 0.0
    elif opts.analysisType == "HToTB":
        from HiggsAnalysis.NtupleAnalysis.parameters.hplus2tbAnalysis import allSelections
    else:
        raise Exception("Invalid analysis selection \"%s\"! Valid options are: %s" % (opts.analysisType, ", ".join(allowedAnalysis)))
    
    # Jet cut values
    allSelections.__setattr__("jetPtCutMin", 0.0)
    allSelections.__setattr__("jetPtCutMax", 99990.0)
    allSelections.__setattr__("jetEtaCutMin", -2.5)
    allSelections.__setattr__("jetEtaCutMax", 2.5)
    # for algo in ["combinedInclusiveSecondaryVertexV2BJetTags"]:
    # for wp in ["Loose", "Medium", "Tight"]:
    #    selections = allSelections.clone()
    #    selections.BJetSelection.bjetDiscr = algo
    #    selections.BJetSelection.bjetDiscrWorkingPoint = wp
    #    suffix = "_%s_%s"%(algo,wp)
    #    print "Added analyzer for algo/wp: %s"%suffix
    #    process.addAnalyzer("BTagEfficiency"+suffix, Analyzer("BTagEfficiencyAnalysis", config=selections, silent=False))

    # Set the analysis type
    allSelections.__setattr__("AnalysisType", opts.analysisType)

    # Overwrite verbosity
    allSelections.verbose = opts.verbose

    # Overwrite histo ambient level (Options: Systematics, Vital, Informative, Debug)
    allSelections.histogramAmbientLevel = opts.histoLevel
    
    #================================================================================================
    # Build analysis modules
    #================================================================================================
    PrintOptions(opts)
    builder = AnalysisBuilder(prefix,
                              dataEras,
                              searchModes,
                              #### Options ####
                              usePUreweighting       = opts.usePUreweighting,
                              useTopPtReweighting    = opts.useTopPtReweighting,
                              doSystematicVariations = opts.doSystematics)

    # ================================================================================================
    # Add Analysis Variations
    # ================================================================================================
    builder.addVariation("BJetSelection.bjetDiscr", ["pfCombinedInclusiveSecondaryVertexV2BJetTags"])
    builder.addVariation("BJetSelection.bjetDiscrWorkingPoint", ["Loose", "Medium", "Tight"])

    # ================================================================================================
    # Build the builder
    # ================================================================================================
    builder.build(process, allSelections)

    # ================================================================================================
    # Run the analysis
    # ================================================================================================
    Print("Running process", True)
    process.run()


#================================================================================================
def PrintOptions(opts):
    '''
    '''
    table    = []
    msgAlign = "{:<20} {:<10} {:<10}"
    title    =  msgAlign.format("Option", "Value", "Default")
    hLine    = "="*len(title)
    table.append(hLine)
    table.append(title)
    table.append(hLine)
    #table.append( msgAlign.format("mcrab" , opts.mcrab , "") )
    #table.append( msgAlign.format("jCores", opts.jCores, "") )
    table.append( msgAlign.format("includeOnlyTasks", opts.includeOnlyTasks, "") )
    table.append( msgAlign.format("excludeTasks", opts.excludeTasks, "") )
    table.append( msgAlign.format("nEvts", opts.nEvts, NEVTS) )
    table.append( msgAlign.format("verbose", opts.verbose, VERBOSE) )
    table.append( msgAlign.format("histoLevel", opts.histoLevel, HISTOLEVEL) )
    table.append( msgAlign.format("usePUreweighting", opts.usePUreweighting, PUREWEIGHT) )
    table.append( msgAlign.format("useTopPtReweighting", opts.useTopPtReweighting, TOPPTREWEIGHT) )
    table.append( msgAlign.format("doSystematics", opts.doSystematics, DOSYSTEMATICS) ) 
    table.append( hLine )

    # Print("Will run on multicrab directory %s" % (opts.mcrab), True)     
    for i, line in enumerate(table):
        Print(line, i==0)
    return


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

    # Default Values
    VERBOSE        = False
    NEVTS          = -1
    HISTOLEVEL     = "Debug"
    PUREWEIGHT     = True
    TOPPTREWEIGHT  = False
    DOSYSTEMATICS  = False
    EVENTSELECTION = "HToTauNu"

    parser = OptionParser(usage="Usage: %prog [options]" , add_help_option=False,conflict_handler="resolve")
    parser.add_option("-m", "--mcrab", dest="mcrab", action="store", 
                      help="Path to the multicrab directory for input")

    parser.add_option("-i", "--includeOnlyTasks", dest="includeOnlyTasks", action="store", 
                      help="List of datasets in mcrab to include")

    parser.add_option("-e", "--excludeTasks", dest="excludeTasks", action="store", 
                      help="List of datasets in mcrab to exclude")

    parser.add_option("-n", "--nEvts", dest="nEvts", action="store", type=int, default = NEVTS,
                      help="Number of events to run on (default: %s" % (NEVTS) )

    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default = VERBOSE, 
                      help="Enable verbosity (for debugging) (default: %s)" % (VERBOSE))

    parser.add_option("-h", "--histoLevel", dest="histoLevel", action="store", default = HISTOLEVEL,
                      help="Histogram ambient level (default: %s)" % (HISTOLEVEL))

    parser.add_option("--noPU", dest="usePUreweighting", action="store_false", default = PUREWEIGHT, 
                      help="Do NOT apply Pileup re-weighting (default: %s)" % (PUREWEIGHT) )

    parser.add_option("--noTopPt", dest="useTopPtReweighting", action="store_false", default = TOPPTREWEIGHT, 
                      help="Do NOT apply top-pt re-weighting (default: %s)" % (TOPPTREWEIGHT) )

    parser.add_option("--doSystematics", dest="doSystematics", action="store_true", default = DOSYSTEMATICS, 
                      help="Do systematics variations  (default: %s)" % (DOSYSTEMATICS) )

    parser.add_option("-a","--analysisType", dest="analysisType", action="store", default = EVENTSELECTION,
                      help="Add event selection \"HToTB\" or \"HToTauNu\"  (default: %s)" % (EVENTSELECTION) )

    (opts, args) = parser.parse_args()

    allowedAnalysis = ["HToTB","HToTauNu"]
    if opts.analysisType not in allowedAnalysis:
        raise Exception("Invalid analysis selection \"%s\"! Valid options are: %s" % (opts.analysisType, ", ".join(allowedAnalysis)))
    else:
        msg = "Calculating b-tag SF for analysis-type \"%s\" using multicrab dir \"%s\". Proceed? " % (opts.analysisType, opts.mcrab)
        AskUser(msg, True)

    if opts.mcrab == None:
        raise Exception("Please provide input multicrab directory with -m")

    allowedLevels = ['Never', 'Systematics', 'Vital', 'Informative', 'Debug']
    if opts.histoLevel not in allowedLevels:
        raise Exception("Invalid ambient histogram level \"%s\"! Valid options are: %s" % (opts.histoLevel, ", ".join(allowedLevels)))

    main()
