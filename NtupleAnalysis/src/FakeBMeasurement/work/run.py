#!/usr/bin/env python
'''
INSTRUCTIONS:


USAGE:
./run.py -m <multicrab_directory> -i "Keyword1|Keyword2|Keyword3"
or
./run.py -m <multicrab_directory> -e "Keyword1|Keyword2|Keyword3" -n 100


Example:
./run.py -m <multicrab_directory> -i "TT|ST_|2016B" -n -1
./run.py -m <multicrab_directory> -n 100 -h Vital

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
prefix      = "FakeBMeasurement"
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
    #from HiggsAnalysis.NtupleAnalysis.parameters.signalAnalysisParameters import obtainAnalysisSuffix
    #process = Process("QCDMeasurement"+obtainAnalysisSuffix(sys.argv))
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
        #myBlackList = [] #QCD_bEnriched"] #["ChargedHiggs", "QCD-b"]
        myBlackList = ["M_800", "M_400", "M_350", "M_3000", "M_300", "M_250", "M_220","M_2000","M_200", "M_180","M_1000", "QCD_b"]
        Print("Adding all datasets from multiCRAB directory %s except %s" % (opts.mcrab, (",".join(myBlackList))) )
        Print("Vertex reweighting is done according to the chosen data era (%s)" % (",".join(dataEras)) )
        # process.addDatasetsFromMulticrab(opts.mcrab, blacklist=myBlackList)
        if len(myBlackList) > 0:
            regex = "|".join(myBlackList)
            process.addDatasetsFromMulticrab(opts.mcrab, excludeTasks=regex)
        else:
            process.addDatasetsFromMulticrab(opts.mcrab)

    # ================================================================================================
    # Overwrite Default Settings
    # ================================================================================================
    from HiggsAnalysis.NtupleAnalysis.parameters.hplus2tbAnalysis import allSelections

    allSelections.verbose                     = opts.verbose
    allSelections.histogramAmbientLevel       = opts.histoLevel
    allSelections.BJetSelection.jetPtCuts     = [40.0, 30.0]
    # allSelections.Trigger.triggerOR           = ["HLT_PFHT400_SixJet30", #Prescale 110 at inst. lumi 1.35E+34
    #                                              "HLT_PFHT450_SixJet40", #Prescale  26 at inst. lumi 1.35E+34]

    # ================================================================================================
    # Command Line Options
    # ================================================================================================ 
    # from HiggsAnalysis.NtupleAnalysis.parameters.signalAnalysisParameters import applyAnalysisCommandLineOptions
    # applyAnalysisCommandLineOptions(sys.argv, allSelections)
    

    # ================================================================================================
    # Build analysis modules
    # ================================================================================================
    PrintOptions(opts)
    builder = AnalysisBuilder(prefix,
                              dataEras,
                              searchModes,
                              usePUreweighting       = opts.usePUreweighting,
                              useTopPtReweighting    = opts.useTopPtReweighting,
                              doSystematicVariations = opts.doSystematics)

    # Add variations (e.g. for optimisation)
    # builder.addVariation("FakeBMeasurement.prelimTopFitChiSqrCutValue", [100, 20])
    # builder.addVariation("FakeBMeasurement.prelimTopFitChiSqrCutDirection", ["<=", "==", ">="])
    # builder.addVariation("FakeBMeasurement.numberOfBJetsCutValue", [0, 1])
    # builder.addVariation("FakeBMeasurement.numberOfBJetsCutDirection", ["=="])
    # builder.addVariation("FakeBMeasurement.numberOfBJetsCutDirection", ["<=", "==", ">="])
    # builder.addVariation("FakeBMeasurement.numberOfInvertedBJetsCutValue", [0, 1])
    builder.addVariation("FakeBMeasurement.numberOfInvertedBJetsCutValue", [1])
    # builder.addVariation("FakeBMeasurement.numberOfInvertedBJetsCutDirection", [">="])
    # builder.addVariation("FakeBMeasurement.invertedBJetDiscr", "")
    # builder.addVariation("FakeBMeasurement.invertedBJetDiscrWorkingPoint", "Loose")
    builder.addVariation("FakeBMeasurement.invertedBJetsSortType", ["Random", "DescendingBDiscriminator"])
    builder.addVariation("FakeBMeasurement.invertedBJetsDiscrMaxCutValue", [1.0, 0.80, 0.75])
    
    # builder.addVariation("TopSelection.ChiSqrCutValue", [100])
    # builder.addVariation("Trigger.triggerOR", [["HLT_PFHT450_SixJet40_BTagCSV_p056"]])
    # builder.addVariation("Trigger.triggerOR", [["HLT_PFHT450_SixJet40"], ["HLT_PFHT400_SixJet30"]])
    # builder.addVariation("TopologySelection.FoxWolframMomentCutValue", [0.5, 0.7])
    # builder.addVariation(".triggerOR", [["HLT_PFHT400_SixJet30_DoubleBTagCSV_p056"], ["HLT_PFHT450_SixJet40_BTagCSV_p056"]])
    
    # Build the builder
    builder.build(process, allSelections)
    
    # ================================================================================================
    # Example of adding an analyzer whose configuration depends on dataVersion
    # ================================================================================================
    # def createAnalyzer(dataVersion):
    # a = Analyzer("ExampleAnalysis")
    # if dataVersion.isMC():
    # a.tauPtCut = 10
    # else:
    # a.tauPtCut = 20
    # return a
    # process.addAnalyzer("test2", createAnalyzer)
    
    # ================================================================================================
    # Pick events
    # ================================================================================================
    # process.addOptions(EventSaver = PSet(enabled = True,pickEvents = True))

    # ================================================================================================
    # Run the analysis
    # ================================================================================================
    # Run the analysis with PROOF? You can give proofWorkers=<N> as a parameter
    if opts.jCores:
        Print("Running process with PROOF (proofWorkes=%s)" % ( str(opts.jCores) ) )
        process.run(proof=True, proofWorkers=opts.jCores)
    else:
        Print("Running process (no PROOF)")
        process.run()

    return

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
    table.append( msgAlign.format("jCores", opts.jCores, "") )
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
    VERBOSE       = False
    NEVTS         = -1
    HISTOLEVEL    = "Debug" # 'Never', 'Systematics', 'Vital', 'Informative', 'Debug'
    PUREWEIGHT    = True
    TOPPTREWEIGHT = True
    DOSYSTEMATICS = False

    parser = OptionParser(usage="Usage: %prog [options]" , add_help_option=False,conflict_handler="resolve")
    parser.add_option("-m", "--mcrab", dest="mcrab", action="store", 
                      help="Path to the multicrab directory for input")

    parser.add_option("-j", "--jCores", dest="jCores", action="store", type=int, 
                      help="Number of CPU cores (PROOF workes) to use. (default: all available)")

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

    (opts, args) = parser.parse_args()

    if opts.mcrab == None:
        raise Exception("Please provide input multicrab directory with -m")

    allowedLevels = ['Never', 'Systematics', 'Vital', 'Informative', 'Debug']
    if opts.histoLevel not in allowedLevels:
        raise Exception("Invalid ambient histogram level \"%s\"! Valid options are: %s" % (opts.histoLevel, ", ".join(allowedLevels)))
    
    main()
