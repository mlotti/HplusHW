#!/usr/bin/env python
'''
INSTRUCTIONS:
The required minimum input is a multiCRAB directory with at least one dataset. If successfull
a pseudo multiCRAB with name "analysis_YYMMDD_HHMMSS/" will be created, inside which each
dataset has its own directory with the results (ROOT files with histograms). These can be later
used as input to plotting scripts to get the desired results.

 USAGE:
 ./runTop.py -m /uscms_data/d3/skonstan/CMSSW_8_0_30/src/HiggsAnalysis/MiniAOD2TTree/test/multicrab_JetTriggers_v8030_20180405T1450 -e "TT_"           
 ./runTop.py -m /uscms_data/d3/skonstan/CMSSW_8_0_30/src/HiggsAnalysis/MiniAOD2TTree/test/multicrab_JetTriggers_v8030_20180405T1450 -e "TT_|Single"    
 
'''

#================================================================================================
# Imports
#================================================================================================
import sys
from optparse import OptionParser
import time

from HiggsAnalysis.NtupleAnalysis.main import Process, PSet, Analyzer
from HiggsAnalysis.NtupleAnalysis.AnalysisBuilder import AnalysisBuilder


import ROOT
    
#================================================================================================
# Options
#================================================================================================
prefix      = "SystTopBDT"
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

    # Save start time (epoch seconds)
    tStart = time.time()
    Verbose("Started @ " + str(tStart), True)

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
    maxEvents = {}
    maxEvents["All"] = opts.nEvts
    process = Process(prefix, postfix, maxEvents)
                
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
        myBlackList = ["QCD_b"
                       "ChargedHiggs_HplusTB_HplusToTB_M_180_ext1", 
                       "ChargedHiggs_HplusTB_HplusToTB_M_200_ext1", 
                       "ChargedHiggs_HplusTB_HplusToTB_M_220_ext1", 
                       "ChargedHiggs_HplusTB_HplusToTB_M_250_ext1", 
                       "ChargedHiggs_HplusTB_HplusToTB_M_300_ext1", 
                       "ChargedHiggs_HplusTB_HplusToTB_M_350_ext1", 
                       "ChargedHiggs_HplusTB_HplusToTB_M_400_ext1", 
                       "ChargedHiggs_HplusTB_HplusToTB_M_500_ext1", 
                       #"ChargedHiggs_HplusTB_HplusToTB_M_650",  #10M events!
                       "ChargedHiggs_HplusTB_HplusToTB_M_800_ext1", 
                       "ChargedHiggs_HplusTB_HplusToTB_M_1000_ext1", 
                       "ChargedHiggs_HplusTB_HplusToTB_M_2000_ext1"
                       "ChargedHiggs_HplusTB_HplusToTB_M_2500_ext1", 
                       "ChargedHiggs_HplusTB_HplusToTB_M_3000_ext1", 
                       # "ChargedHiggs_HplusTB_HplusToTB_M_1000",
                       "ChargedHiggs_HplusTB_HplusToTB_M_1500",   # Speeed things up
                       "ChargedHiggs_HplusTB_HplusToTB_M_2000",   # Speeed things up
                       "ChargedHiggs_HplusTB_HplusToTB_M_2500",   # Speeed things up
                       "ChargedHiggs_HplusTB_HplusToTB_M_3000",   # Speeed things up
                       "ChargedHiggs_HplusTB_HplusToTB_M_5000",   # Speeed things up
                       "ChargedHiggs_HplusTB_HplusToTB_M_7000",   # Speeed things up  
                       "ChargedHiggs_HplusTB_HplusToTB_M_10000",  # Speeed things up
                       ]
        if opts.doSystematics:
            myBlackList.append("QCD")

        Print("Adding all datasets from multiCRAB directory %s" % (opts.mcrab))
        Print("If collision data are present, then vertex reweighting is done according to the chosen data era (era=2015C, 2015D, 2015) etc...")
        regex =  "|".join(myBlackList)
        if len(myBlackList)>0:
            process.addDatasetsFromMulticrab(opts.mcrab, excludeTasks=regex)
        else:
            process.addDatasetsFromMulticrab(opts.mcrab)



    # ================================================================================================
    # Overwrite Default Settings  
    # ================================================================================================
    from HiggsAnalysis.NtupleAnalysis.parameters.jetTriggers import allSelections
    from HiggsAnalysis.NtupleAnalysis.main import PSet
    import HiggsAnalysis.NtupleAnalysis.parameters.scaleFactors as scaleFactors

    allSelections.verbose = opts.verbose
    allSelections.histogramAmbientLevel = opts.histoLevel

    #==========================
    #  Systematics selections
    #==========================
    
    # marina
    allSelections.SystTopBDTSelection.MVACutValue = 0.40
    allSelections.TopSelectionBDT.TopMVACutValue  = 0.40
    
    # BDT MisID SF
    MisIDSF = PSet(
        MisIDSFJsonName = "topMisID_BDTCut0p40.json",
        ApplyMisIDSF    = False, 
        )
    scaleFactors.assignMisIDSF(MisIDSF, "nominal", MisIDSF.MisIDSFJsonName)
    allSelections.MisIDSF = MisIDSF
    
    allSelections.SystTopBDTSelection.MiniIsoCutValue    = 0.1
    allSelections.SystTopBDTSelection.MiniIsoInvCutValue = 0.1
    allSelections.SystTopBDTSelection.METCutValue        = 50.0
    allSelections.SystTopBDTSelection.METInvCutValue     = 20.0
    
    # Muon
    allSelections.MuonSelection.muonPtCut = 30
    
    # Jets
    allSelections.JetSelection.numberOfJetsCutValue = 4
    allSelections.JetSelection.jetPtCuts = [40.0, 40.0, 40.0, 30.0]
        
    # Trigger 
    allSelections.Trigger.triggerOR = ["HLT_Mu50"]

    # Bjets
    allSelections.BJetSelection.jetPtCuts = [40.0, 30.0]
    allSelections.BJetSelection.numberOfBJetsCutValue = 2
    
    # ================================================================================================
    # Add Analysis Variations
    # ================================================================================================
    # selections = allSelections.clone()
    # process.addAnalyzer(prefix, Analyzer(prefix, config=selections, silent=False) ) #trigger passed from selections


    # ================================================================================================
    # Command Line Options
    # ================================================================================================ 
    # from HiggsAnalysis.NtupleAnalysis.parameters.signalAnalysisParameters import applyAnalysisCommandLineOptions
    # applyAnalysisCommandLineOptions(sys.argv, allSelections)

    #================================================================================================
    # Build analysis modules
    #================================================================================================
    PrintOptions(opts)
    builder = AnalysisBuilder(prefix,
                              dataEras,
                              searchModes,
                              usePUreweighting       = opts.usePUreweighting,
                              useTopPtReweighting    = opts.useTopPtReweighting,
                              doSystematicVariations = opts.doSystematics,
                              analysisType="HToTB")

    # Add variations (e.g. for optimisation)
    # builder.addVariation("METSelection.METCutValue", [100,120,140])
    # builder.addVariation("AngularCutsBackToBack.workingPoint", ["Loose","Medium","Tight"])
    # builder.addVariation("BJetSelection.triggerMatchingApply", [False])
    # builder.addVariation("TopSelection.ChiSqrCutValue", [5, 10, 15, 20])

    # Build the builder
    builder.build(process, allSelections)

    # ================================================================================================
    # Example of adding an analyzer whose configuration depends on dataVersion
    # ================================================================================================
    #def createAnalyzer(dataVersion):
    #a = Analyzer("ExampleAnalysis")
    #if dataVersion.isMC():
    #a.tauPtCut = 10
    #else:
    #a.tauPtCut = 20
    #return a
    #process.addAnalyzer("test2", createAnalyzer)

    
    # ================================================================================================
    # Pick events
    # ================================================================================================
    #process.addOptions(EventSaver = PSet(enabled = True,pickEvents = True))
    # ================================================================================================
    # Run the analysis
    # ================================================================================================
    # Run the analysis with PROOF? You can give proofWorkers=<N> as a parameter
    if opts.jCores:
        Print("Running process with PROOF (proofWorkes=%s)" % ( str(opts.jCores) ) )
        process.run(proof=True, proofWorkers=opts.jCores)
    else:
        Print("Running process")
        process.run()

    # Print total time elapsed
    tFinish = time.time()
    dt      = int(tFinish) - int(tStart)
    days    = divmod(dt,86400)      # days
    hours   = divmod(days[1],3600)  # hours
    mins    = divmod(hours[1],60)   # minutes
    secs    = mins[1]               # seconds
    Print("Total elapsed time is %s days, %s hours, %s mins, %s secs" % (days[0], hours[0], mins[0], secs), True)
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
    HISTOLEVEL    = "Debug" #"Informative" #"Debug"
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
