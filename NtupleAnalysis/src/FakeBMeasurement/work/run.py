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
import time

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
    # maxEvents["2016"] = 1
    # maxEvents["ZZTo4Q"] = -1
    # maxEvents["ZJetsToQQ_HT600toInf"] = 1
    # maxEvents["WZ_ext1"] = 1
    # maxEvents["WZ"] = 1
    # maxEvents["WWTo4Q"] = 1
    # maxEvents["WJetsToQQ_HT_600ToInf"] = 1
    # maxEvents["TTZToQQ"] = 1
    # maxEvents["TTWJetsToQQ"] = 1
    # maxEvents["TTTT"] = 1
    # maxEvents["TT"] = 1
    # maxEvents["ST_t_channel_top_4f_inclusiveDecays"] = 1
    # maxEvents["ST_t_channel_antitop_4f_inclusiveDecays"] = 1
    # maxEvents["ST_tW_top_5f_inclusiveDecays_ext1"] = 1
    # maxEvents["ST_tW_top_5f_inclusiveDecays"] = 1
    # maxEvents["ST_tW_antitop_5f_inclusiveDecays_ext1"] = 1
    # maxEvents["ST_tW_antitop_5f_inclusiveDecays"] = 1
    # maxEvents["ST_s_channel_4f_InclusiveDecays"] = 1
    # maxEvents["QCD_HT700to1000_ext1"] = 1
    # maxEvents["QCD_HT700to1000"] = 1
    # maxEvents["QCD_HT50to100"] = 1
    # maxEvents["QCD_HT500to700_ext1"] = 1
    # maxEvents["QCD_HT500to700"] = 1
    # maxEvents["QCD_HT300to500_ext1"] = 1
    # maxEvents["QCD_HT300to500"] = 1
    # maxEvents["QCD_HT200to300_ext1"] = 1
    # maxEvents["QCD_HT200to300"] = 1
    # maxEvents["QCD_HT2000toInf_ext1"] = 1
    # maxEvents["QCD_HT2000toInf"] = 1
    # maxEvents["QCD_HT1500to2000_ext1"] = 1
    # maxEvents["QCD_HT1500to2000"] = 1
    # maxEvents["QCD_HT100to200"] = 1
    # maxEvents["QCD_HT1000to1500_ext1"] = 1
    # maxEvents["QCD_HT1000to1500"] = 1
    # maxEvents["JetHT_Run2016H_03Feb2017_ver3_v1_284036_284044"] = 1
    # maxEvents["JetHT_Run2016H_03Feb2017_ver2_v1_281613_284035"] = 1
    # maxEvents["JetHT_Run2016G_03Feb2017_v1_278820_280385"] = 1
    # maxEvents["JetHT_Run2016F_03Feb2017_v1_278801_278808"] = 1
    # maxEvents["JetHT_Run2016F_03Feb2017_v1_277932_278800"] = 1
    # maxEvents["JetHT_Run2016E_03Feb2017_v1_276831_277420"] = 1
    # maxEvents["JetHT_Run2016D_03Feb2017_v1_276315_276811"] = 1
    # maxEvents["JetHT_Run2016C_03Feb2017_v1_275656_276283"] = 1
    # maxEvents["JetHT_Run2016B_03Feb2017_ver2_v2_273150_275376"] = 1
    # maxEvents["DYJetsToQQ_HT180"] = 1
    # maxEvents["ChargedHiggs_HplusTB_HplusToTB_M_500"] = 1
    process = Process(prefix, postfix, maxEvents)

    # ================================================================================================
    # Add the datasets (according to user options)
    # ================================================================================================
    if (opts.includeOnlyTasks):
        Verbose("Adding only dataset %s from multiCRAB directory %s" % (opts.includeOnlyTasks, opts.mcrab))
        process.addDatasetsFromMulticrab(opts.mcrab, includeOnlyTasks=opts.includeOnlyTasks)
    elif (opts.excludeTasks):
        Verbose("Adding all datasets except %s from multiCRAB directory %s" % (opts.excludeTasks, opts.mcrab))
        Print("If collision data are present, then vertex reweighting is done according to the chosen data era (era=2015C, 2015D, 2015) etc...")
        process.addDatasetsFromMulticrab(opts.mcrab, excludeTasks=opts.excludeTasks)
    else:
        myBlackList = ["M_180", "M_200" , "M_220" , "M_250" , "M_300" , "M_350" , "M_400" , "M_500" , "M_650",
                       "M_800", "M_1000", "M_1500", "M_2000", "M_2500", "M_3000", "M_5000", "M_7000", "M_10000", "QCD"]
        Verbose("Adding all datasets from multiCRAB directory %s except %s" % (opts.mcrab, (",".join(myBlackList))) )
        Verbose("Vertex reweighting is done according to the chosen data era (%s)" % (",".join(dataEras)) )
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

    allSelections.verbose = opts.verbose
    allSelections.histogramAmbientLevel = opts.histoLevel

    # Set splitting of phase-space (first bin is below first edge value and last bin is above last edge value)
    allSelections.CommonPlots.histogramSplitting = [        
        ### 2D-binning (Pt, Eta)
        PSet(label="TetrajsetBjetPt", binLowEdges=[55, 110], useAbsoluteValues=False),
        #PSet(label="TetrajsetBjetPt", binLowEdges=[60, 100, 150], useAbsoluteValues=False),
        PSet(label="TetrajetBjetEta", binLowEdges=[0.8, 1.6], useAbsoluteValues=True),
        ### 1D-binning (Eta)
        #PSet(label="TetrajetBjetEta", binLowEdges=[0.4, 0.8, 1.6, 2.0, 2.2], useAbsoluteValues=True),  #AN v4
        ]
    
    # allSelections.BJetSelection.triggerMatchingApply = True # at least 1 trg b-jet matched to offline b-jets
    # allSelections.Trigger.triggerOR = ["HLT_PFHT450_SixJet40_BTagCSV_p056", "HLT_PFJet450"]

    #allSelections.FakeBTopSelectionBDT.LdgTopDefinition = "Pt" # [default: "MVA"] (options: "MVA", "Pt")
    allSelections.FakeBTopSelectionBDT.TopMassLowCutValue     =  0.0   # [default: 0.0] #90.0
    allSelections.FakeBTopSelectionBDT.TopMassLowCutDirection = ">="   # [default: ">="]
    allSelections.FakeBTopSelectionBDT.TopMassUppCutValue     = 600.0  # [default: 600.0] # 250
    allSelections.FakeBTopSelectionBDT.TopMassUppCutDirection = "<="   # [default: "<="]
    allSelections.FakeBTopSelectionBDT.WMassLowCutValue       =   0.0  # [default: 0.0]
    allSelections.FakeBTopSelectionBDT.WMassLowCutDirection   = ">="   # [default: ">="]
    allSelections.FakeBTopSelectionBDT.WMassUppCutValue       = 0.0    # [default: "0.0] # 150.0
    allSelections.FakeBTopSelectionBDT.WMassUppCutDirection   = ">="   # [default: ">="] # "<="
    allSelections.FakeBTopSelectionBDT.CSV_bDiscCutValue      = 0.8484 # [default: 0.8484] # 0.5426
    allSelections.FakeBTopSelectionBDT.CSV_bDiscCutDirection  = ">="   # [default: ">="]
    allSelections.TopSelectionBDT.MVACutValue                 =  0.40  # [default:  0.40]
    allSelections.FakeBTopSelectionBDT.MVACutValue            = -1.00  # [default: -1.00]
    allSelections.FakeBMeasurement.LdgTopMVACutValue          = allSelections.TopSelectionBDT.MVACutValue
    allSelections.FakeBMeasurement.SubldgTopMVACutValue       = allSelections.TopSelectionBDT.MVACutValue
    print "=== run.py: Default parameters overwritten!"
    
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
                              doSystematicVariations = opts.doSystematics,
                              analysisType="HToTB",
                              verbose=opts.verbose)

    # Add variations (e.g. for optimisation)
    # builder.addVariation("BJetSelection.triggerMatchingApply", [True, False]) # At least 1 trg b-jet dR-matched to offline b-jets
    # builder.addVariation("FakeBMeasurement.prelimTopFitChiSqrCutValue", [100, 20])
    # builder.addVariation("FakeBMeasurement.prelimTopFitChiSqrCutDirection", ["<=", "==", ">="])
    # builder.addVariation("FakeBMeasurement.numberOfBJetsCutValue", [0, 1])
    # builder.addVariation("FakeBMeasurement.numberOfBJetsCutDirection", ["=="])
    # builder.addVariation("FakeBMeasurement.numberOfBJetsCutDirection", ["<=", "==", ">="])
    # builder.addVariation("FakeBMeasurement.numberOfInvertedBJetsCutValue", [0, 1])
    # builder.addVariation("FakeBMeasurement.numberOfInvertedBJetsCutDirection", [">="])
    # builder.addVariation("FakeBMeasurement.invertedBJetDiscr", "")
    # builder.addVariation("FakeBMeasurement.invertedBJetDiscrWorkingPoint", "Loose")
    # builder.addVariation("FakeBMeasurement.invertedBJetsSortType", ["Random", "DescendingBDiscriminator"])
    # builder.addVariation("FakeBMeasurement.invertedBJetsDiscrMaxCutValue", [0.82, 0.80, 0.75, 0.70])
    # builder.addVariation("TopSelection.ChiSqrCutValue", [100])
    # builder.addVariation("Trigger.triggerOR", [["HLT_PFHT450_SixJet40"], ["HLT_PFHT400_SixJet30"]])
    # builder.addVariation("TopologySelection.FoxWolframMomentCutValue", [0.5, 0.7])
    # builder.addVariation("Trigger.triggerOR", [["HLT_PFHT400_SixJet30_DoubleBTagCSV_p056"], ["HLT_PFHT450_SixJet40_BTagCSV_p056"]])
    # builder.addVariation("Trigger.triggerOR", [["HLT_PFHT400_SixJet30_DoubleBTagCSV_p056", "HLT_PFHT450_SixJet40_BTagCSV_p056"]])
    
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
    if not opts.verbose:
        return
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

    parser.add_option("--topPt", dest="useTopPtReweighting", action="store_true", default = TOPPTREWEIGHT,
                      help="Do apply top-pt re-weighting (default: %s)" % (TOPPTREWEIGHT) )

    parser.add_option("--doSystematics", dest="doSystematics", action="store_true", default = DOSYSTEMATICS, 
                      help="Do systematics variations  (default: %s)" % (DOSYSTEMATICS) )

    (opts, args) = parser.parse_args()

    if opts.mcrab == None:
        raise Exception("Please provide input multicrab directory with -m")

    allowedLevels = ['Never', 'Systematics', 'Vital', 'Informative', 'Debug']
    if opts.histoLevel not in allowedLevels:
        raise Exception("Invalid ambient histogram level \"%s\"! Valid options are: %s" % (opts.histoLevel, ", ".join(allowedLevels)))
    
    main()
