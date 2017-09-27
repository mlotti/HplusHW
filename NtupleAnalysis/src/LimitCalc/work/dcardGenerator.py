#! /usr/bin/env python
'''
DESCRIPTION:
This is a script for generating datacards to be used by combine (or LimitOMatic) to 
produce exclusion limits.


INSTRUCTIONS:
To run this datacard generator you first need to run your signal analysis (and 
the data-driven backdround estimation) to produce a pseudo-multicrab directory with the
results. The go to HiggsAnalysis/NtupleAnalysis/src/LimitCalc/work and create a new directory
(e.g. "exampleDirectory"). If not already the case, Rename the pseudo-multicrab directory so
that it starts with "SignalAnalysis_" and move it under the "exampleDirectory". 
Set the input paremters (datasets, signal rates, backgound rates, systematics, etc..) for
datacard generation, defined in your template datacard python file 
(e.g. LimitCalc/work/dcardHplustb2017Datacard). Run the datacard generator 
by providing a minimum of two arguments:
1) The datacard python file with all the datacard definitions & settings
2) The pseudo-multicrab directory with all the results


USAGE:
./dcardGenerator.py -x <input-datacard> -d <pseudo-multicrab-dir>


EXAMPLES:
./dcardGenerator.py -x dcardHplustb2017Datacard_v2.py -d example/
(where example contains SignalAnalysis_StdSelections_TopCut100_AllSelections_NoTrgMatch_TopCut10_H2Cut0p5_170827_075947)

'''
#================================================================================================
# Import modules
#================================================================================================
import os
import sys
import imp
from optparse import OptionParser
import gc
import cPickle
import time
import ROOT
ROOT.gROOT.SetBatch(True) # no flashing canvases
ROOT.PyConfig.IgnoreCommandLineOptions = True
import tarfile
import cProfile

import HiggsAnalysis.LimitCalc.MulticrabPathFinder as PathFinder
import HiggsAnalysis.NtupleAnalysis.tools.analysisModuleSelector as analysisModuleSelector
import HiggsAnalysis.LimitCalc.DataCardGenerator as DataCard
import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
from HiggsAnalysis.NtupleAnalysis.tools.aux import load_module
from HiggsAnalysis.NtupleAnalysis.tools.ShellStyles import *
import HiggsAnalysis.NtupleAnalysis.tools.multicrab as multicrab


#================================================================================================
# Function definition
#================================================================================================
def memoryDump():
    dump = open("memory_pickle.txt", 'w')
    for obj in gc.get_objects():
        i = id(obj)
        size = sys.getsizeof(obj, 0)
        #    referrers = [id(o) for o in gc.get_referrers(obj) if hasattr(o, '__class__')]
        referents = [id(o) for o in gc.get_referents(obj) if hasattr(o, '__class__')]
        if hasattr(obj, '__class__'):
            cls = str(obj.__class__)
            cPickle.dump({'id': i, 'class': cls, 'size': size, 'referents': referents}, dump)
    return


def getDsetCreator(label, mcrabPath, mcrabInfoOutput, enabledStatus=True):
    if enabledStatus:
        if mcrabPath == "":
            msg = "%s not present!" % (label) #fixme: application to H2tb?
            mcrabInfoOutput.append(msg)
            Print(WarningLabel() + msg)
        else:
            mcrabInfoOutput.append("- %s: multicrab dir found (%s)" % (label,mcrabPath) )
            msg = "%s multicrab dir found in %s" % (label, mcrabPath)
            Verbose(NoteStyle() + msg + NormalStyle()) # HighlightStyle()
            return dataset.readFromMulticrabCfg(directory=mcrabPath)
    else:
        msg = "%s not considered!" % (label)
        mcrabInfoOutput.append(msg)
        Print(NoteStyle() + msg)
    return None


def Verbose(msg, printHeader=False):
    '''
    Calls Print() only if verbose options is set to true
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
    if printHeader:
        print "=== ", fName
    print "\t", msg
    return


def PrintEraModeOptQCDMethod(era, searchMode, optimizationMode, qcd):
    align = "{:<20} {:<2} {:<20} "
    msgs   = []
    msgs.append(align.format("era", ":", era) )
    msgs.append(align.format("searchMode", ":", searchMode) )
    msgs.append(align.format("optimizationMode", ":", optimizationMode) )
    msgs.append(align.format("QCD method", ":", qcd))
    for i, msg in enumerate(msgs, 1):
        Print(msg, i==1)
    return


def main(opts, moduleSelector, multipleDirs):
    #Print(CaptionStyle() + "*** Datacard generator ***" + NormalStyle() + "\n")

    # Definitions
    signalLabel = "Signal analysis"
    ewkLabel    = "Embedding"
    qcdInvLabel = "QCD inverted"

    #gc.set_debug(gc.DEBUG_LEAK | gc.DEBUG_STATS)
    #gc.set_debug(gc.DEBUG_STATS)
    #ROOT.SetMemoryPolicy(ROOT.kMemoryStrict)
    #gc.set_debug(gc.DEBUG_STATS)
    Verbose("Loading datacard \"%s\"" % (opts.datacard) )

    # Catch any errors in the input datacard
    os.system("python %s" % opts.datacard)
    config = load_module(opts.datacard)

    # Replace source directory if necessary
    if multipleDirs != None:
        config.Path = multipleDirs
    Verbose("Input directory is \"%s\"" % (config.Path) )

    # If user insisted on certain QCD method on command line, produce datacards only for that QCD method
    # Otherwise produce cards for all QCD methods
    myQCDMethods = [DataCard.DatacardQCDMethod.INVERTED, DataCard.DatacardQCDMethod.MC]

    # Obtain dataset creators (also check multicrab directory existence)
    Verbose("Checking input multicrab directory presence")
    multicrabPaths  = PathFinder.MulticrabPathFinder(config.Path)
    mcrabInfoOutput = []
    mcrabInfoOutput.append("Input directories:")

    signalDsetCreator = getDsetCreator(signalLabel, multicrabPaths.getSignalPath(), mcrabInfoOutput)
    embeddingDsetCreator = None
    if not config.OptionGenuineTauBackgroundSource == "DataDriven":
        mcrabInfoOutput.append("- Embedding will be estimated from signal analysis MC")
        Verbose(WarningLabel() + "Embedding will be estimated from signal analysis MC" + NormalStyle() )
    else:
        multicrabPaths.getEWKPath()
        if multicrabPaths.getEWKPath() == "":
            raise Exception(ErrorLabel()+"You asked for data driven EWK+tt with taus, but no corresponding multicrab was found!")
        embeddingDsetCreator = getDsetCreator(ewkLabel, multicrabPaths.getEWKPath(), mcrabInfoOutput)
    qcdInvertedDsetCreator = getDsetCreator(qcdInvLabel, multicrabPaths.getQCDInvertedPath(), mcrabInfoOutput, DataCard.DatacardQCDMethod.INVERTED in myQCDMethods)

    if qcdInvertedDsetCreator == None:
        myQCDMethods.remove(DataCard.DatacardQCDMethod.INVERTED)
    else:
        myQCDMethods.remove(DataCard.DatacardQCDMethod.MC)

    # Require existence of signal analysis and one QCD measurement
    if signalDsetCreator == None:
        msg = ErrorLabel() + " Signal analysis multicrab directory not found!"
        raise Exception(msg)
    if len(myQCDMethods) == 0:
        msg = " QCD measurement (factorised and/or inverted) not found!"
        Print(WarningLabel() + msg)

    # Check options that are affecting the validity of the results
    if not config.OptionIncludeSystematics:
        msg = " Skipping of shape systematics has been forced (flag OptionIncludeSystematics in the datacard file)"
        Print(WarningLabel() + msg)
    if not config.OptionDoControlPlots:
        msg = " Skipping of data-driven control plot generation been forced (flag OptionDoControlPlots in the datacard file)"
        Print(WarningLabel() + msg)

    # Find list of available eras, search modes, and optimization modes common for all multicrab directories
    Verbose("Find list of available eras, search modes, and optimization modes common for all multicrab directories", True)
    moduleSelector.setPrimarySource("Signal analysis", signalDsetCreator)
    if embeddingDsetCreator != None:
        moduleSelector.addOtherSource("Embedding", embeddingDsetCreator)

    #if qcdFactorisedDsetCreator != None:
        #moduleSelector.addOtherSource("QCD factorised", qcdFactorisedDsetCreator)

    if qcdInvertedDsetCreator != None:
        moduleSelector.addOtherSource("QCD inverted", qcdInvertedDsetCreator)

    moduleSelector.doSelect(opts, printSelections=opts.verbose) # alex: prints out selected eras, modes, optimisation
    moduleSelector.closeFiles()

    # Separate light and heavy masses if they are not separated
    mySearchModeList = moduleSelector.getSelectedSearchModes()
    if ("Light" not in mySearchModeList and len(config.LightMassPoints) > 0 and len(config.HeavyMassPoints) > 0) or \
       ("Heavy" not in mySearchModeList and len(config.HeavyMassPoints) > 0 and len(config.LightMassPoints) > 0):
        mySearchModeList.append(mySearchModeList[0])

    # Summarise the consequences of the user choises
    nEras       = len(moduleSelector.getSelectedEras())
    nModes      = len(moduleSelector.getSelectedSearchModes())
    nOptModes   = len(moduleSelector.getSelectedOptimizationModes())
    nQCDMethods = len(myQCDMethods)
    nDatacards  = nEras*nModes*nOptModes*nQCDMethods
    msg  = "Producing %d set(s) of datacards" % (nDatacards)
    msg += " [%d era(s) x %d search mode(s) x %d optimization mode(s) x %d QCD measurement(s)]" % (nEras, nModes, nOptModes, nQCDMethods)
    Print(HighlightAltStyle() + msg + NormalStyle()) #NoteStyle()

    # Produce datacards
    myCounter = 0
    myStartTime = time.time()
    myOriginalName = config.DataCardName
    myOutputDirectories = []


    # For-loop: QCD methods
    for qcdMethod in myQCDMethods:

        # For-loop: Data eras
        for era in moduleSelector.getSelectedEras():
            mySearchModeCounter = 0

            # For-loop: Search modes
            for searchMode in mySearchModeList:
                # Separate light and heavy mass points into their own subdirectories
                if len(mySearchModeList) > 1:
                    if mySearchModeList[0] == mySearchModeList[1]:
                        if mySearchModeCounter == 0:
                            config.MassPoints = config.LightMassPoints
                            config.DataCardName = myOriginalName + "_LightHplus"
                        elif mySearchModeCounter == 1:
                            config.MassPoints = config.HeavyMassPoints
                            config.DataCardName = myOriginalName + "_HeavyHplus"

                # print config.MassPoints
                mySearchModeCounter += 1
                # For-loop: Optimization modes
                for optimizationMode in moduleSelector.getSelectedOptimizationModes():
                    if hasattr(ROOT.gROOT, "CloseFiles"):
                        ROOT.gROOT.CloseFiles()
                    ROOT.gROOT.GetListOfCanvases().Delete()

                    # After these, three histograms are still left in memory
                    # Worst memory leak seems to come from storing and not freeing the main counters
                    # Create the dataset creator managers separately for each module
                    signalDsetCreator = getDsetCreator(signalLabel, multicrabPaths.getSignalPath(), mcrabInfoOutput)
                    embeddingDsetCreator = None
                    if not config.OptionGenuineTauBackgroundSource == "DataDriven":
                        mcrabInfoOutput.append("- Embedding will be estimated from signal analysis MC")
                        msg = "Embedding will be estimated from signal analysis MC"
                        Verbose(WarningLabel() + msg) #fixme: is this obsolete?
                    else:
                        embeddingDsetCreator = getDsetCreator(ewkLabel, multicrabPaths.getEWKPath(), mcrabInfoOutput)
                    myQCDDsetCreator = None

                    # if qcdMethod == DataCard.DatacardQCDMethod.FACTORISED:
                    #     enabled = DataCard.DatacardQCDMethod.FACTORISED in myQCDMethods
                    #     myQCDDsetCreator = getDsetCreator("QCD factorised", multicrabPaths.getQCDFactorisedPath(), mcrabInfoOutput, enabled)
                    #     if myQCDDsetCreator == None:
                    #         raise Exception(ErrorLabel()+"Could not find factorised QCD pseudomulticrab!"+NormalStyle())

                    if qcdMethod == DataCard.DatacardQCDMethod.INVERTED:
                        enabled = DataCard.DatacardQCDMethod.INVERTED in myQCDMethods
                        myQCDDsetCreator = getDsetCreator(qcdInvLabel, multicrabPaths.getQCDInvertedPath(), mcrabInfoOutput, enabled)
                        if myQCDDsetCreator == None:
                            msg = "Could not find inverted QCD pseudomulticrab"
                            raise Exception(ErrorLabel() + msg +NormalStyle())

                    Verbose("Create the datacard generator & check config file contents")
                    dcgen = DataCard.DataCardGenerator(opts, config, qcdMethod, verbose=opts.verbose)

                    # Tweak to provide the correct datasetMgrCreator to the generator
                    qcd = "Unset"
                    if qcdMethod == DataCard.DatacardQCDMethod.FACTORISED:                        
                        qcd = "factorised"
                    elif qcdMethod == DataCard.DatacardQCDMethod.INVERTED:
                        qcd = "inverted"

                    # Print settings to user
                    PrintEraModeOptQCDMethod(era, searchMode, optimizationMode, qcd)

                    #Print("era=%s, searchMode=%s, optimizationMode=%s, QCD method=%s" % (era, searchMode, optimizationMode, qcd))
                    dcgen.setDsetMgrCreators(signalDsetCreator,embeddingDsetCreator,myQCDDsetCreator)

                    # Print progress info
                    myCounter += 1
                    msg = "Producing datacard %d/%d" % (myCounter, nDatacards)
                    Print(HighlightAltStyle() + msg + NormalStyle()) #CaptionStyle

                    # Do the heavy stuff
                    myDir = dcgen.doDatacard(era,searchMode, optimizationMode, mcrabInfoOutput)
                    myOutputDirectories.append(myDir)

                    # Do tail fit for heavy H+ if asked
                    if opts.dotailfit:
                        Print("Performing tail fit for heavy H+ ...")
                        myHeavyStatus = True
                        for m in config.MassPoints:
                            if m < 175:
                                myHeavyStatus = False
                        if myHeavyStatus:
                            Print("Doing tail fit ...")
                            os.chdir(myDir)
                            os.system("../dcardTailFitter.py -x ../dcardTailFitSettings.py")
                            os.chdir("..")

    Verbose("Datacard generator is done!")

    # Timing calculations
    myEndTime = time.time()
    myTotTime = (myEndTime-myStartTime)
    myAvgTime = (myTotTime)/float(nDatacards)
    Verbose("Running took on average %.1f s per datacard (elapsed time = %.1f s,  datacards = %d) " % (myAvgTime, myTotTime, nDatacards) )
    
    # Generate plots for systematics
    if opts.systAnalysis:
        for d in myOutputDirectories:
            Print("Generating systematics plots for %s" (d) )
            os.chdir(d)
            os.system("../plotShapes.py")
            os.chdir("..")

    # Make tar file
    myTimestamp = time.strftime("%y%m%d_%H%M%S", time.gmtime(time.time()))
    myLimitCode = None
    if opts.lands:
        myLimitCode = "lands"
    elif opts.combine:
        myLimitCode = "combine"
    myFilename = "datacards_%s_archive_%s.tgz"%(myLimitCode,myTimestamp)
    fTar = tarfile.open(myFilename, mode="w:gz")
    
    # For-loop: All output dirs
    for d in myOutputDirectories:
        fTar.add(d)
    fTar.close()

    msg = "Created archive of results directories to "
    Print(msg + SuccessStyle() + myFilename + NormalStyle())

    #gc.collect()
    #ROOT.SetMemoryPolicy( ROOT.kMemoryHeuristics)
    #memoryDump()
    

if __name__ == "__main__":

    # Default Values
    HELP          = False
    LANDS         = False
    COMBINE       = True
    SYSTANALYSIS  = False
    SHAPESENSITIV = False
    SHOWCARD      = False
    TAILFIT       = False
    DATASETDEBUG  = False
    CONFIGDEBUG   = False
    MININGDEBUG   = False
    QCDDEBUG      = False
    SHAPEDEBUG    = False
    CTRLPLOTDEBUG = False
    PROFILERDEBUG = False
    VERBOSE       = False

    # Object for selecting data eras, search modes, and optimization modes
    myModuleSelector = analysisModuleSelector.AnalysisModuleSelector() 

    parser = OptionParser(usage="Usage: %prog [options]", add_help_option=False, conflict_handler="resolve")

    parser.add_option("-h", "--help", dest="helpStatus", action="store_true", default=HELP, 
                      help="Show this help message and exit [default: %s]" % HELP)

    parser.add_option("-x", "--datacard", dest="datacard", action="store", 
                      help="Name (incl. path) of the datacard to be used as an input")

    myModuleSelector.addParserOptions(parser)

    parser.add_option("--lands", dest="lands", action="store_true", default=LANDS, 
                      help="Generate datacards for LandS (not supported) [default: %s]" % (LANDS) )

    parser.add_option("--combine", dest="combine", action="store_true", default=COMBINE,
                      help="Generate datacards for Combine [default=%s]" % (COMBINE) )

    parser.add_option("-d", "--dir", dest="directories", action="append", 
                      help="Name of directories for creating datacards for multiple directories")

    parser.add_option("--systAnalysis", dest="systAnalysis", action="store_true", default=SYSTANALYSIS, 
                      help="Runs the macro for generating systematic uncertainties plots [default: %s]" % (SYSTANALYSIS) )

    parser.add_option("--testShapeSensitivity", dest="testShapeSensitivity", action="store_true", default=SHAPESENSITIV,
                      help="Creates datacards for varying each shape nuisance up and down by 1 sigma [default: %s]" % (SHAPESENSITIV) )

    parser.add_option("--showcard", dest="showDatacard", action="store_true", default=SHOWCARD, 
                      help="Print datacards also to screen [default: %s]" % (SHOWCARD) )

    parser.add_option("--tailfit", dest="dotailfit", action="store_true", default=TAILFIT, 
                      help="Runs the tail fitter for heavy H+ after the cards are done [default: %s]" % (TAILFIT) )

    parser.add_option("--debugDatasets", dest="debugDatasets", action="store_true", default=DATASETDEBUG, 
                      help="Enable debugging print for datasetMgr contents [default: %s]" % (DATASETDEBUG) )

    parser.add_option("--debugConfig", dest="debugConfig", action="store_true", default=CONFIGDEBUG,
                      help="Enable debugging print for config parsing [default: %s]" % (CONFIGDEBUG) )
    
    parser.add_option("--debugMining", dest="debugMining", action="store_true", default=MININGDEBUG, 
                      help="Enable debugging print for data mining [default: %s]" % (MININGDEBUG) )
    
    parser.add_option("--debugQCD", dest="debugQCD", action="store_true", default=QCDDEBUG, 
                      help="Enable debugging print for QCD measurement [default: %s]" % (QCDDEBUG) )

    parser.add_option("--debugShapeHistogram", dest="debugShapeHistogram", action="store_true", default=SHAPEDEBUG,
                      help="Debug shape histogram modifying algorithm [default: %s]" % (SHAPEDEBUG) )

    parser.add_option("--debugControlPlots", dest="debugControlPlots", action="store_true", default=CTRLPLOTDEBUG,
                      help="Enable debugging print for data-driven control plots [default: %s]" % (CTRLPLOTDEBUG) )

    parser.add_option("--debugProfiler", dest="debugProfiler", action="store_true", default=PROFILERDEBUG,
                      help="Enable profiler [default: %s]" % (PROFILERDEBUG) )

    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=VERBOSE,
                      help="Print more information [default: %s]" % (VERBOSE) )

    #parser.add_option("--QCDfactorised", dest="useQCDfactorised", action="store_true", default=False, 
    #                  help="Use factorised method for QCD measurement")

    #parser.add_option("--QCDinverted", dest="useQCDinverted", action="store_true", default=False, 
    #                  help="Use inverted method for QCD measurement")

    (opts, args) = parser.parse_args()

    myStatus = True
    if opts.debugShapeHistogram:
        testShapeHistogram()
    if opts.datacard == None:
        print ErrorStyle()+"Error: Missing datacard!"+NormalStyle()+"\n"
        myStatus = False
    #if opts.useQCDfactorised and opts.useQCDinverted:
    #    print ErrorStyle()+"Error: use either '--QCDfactorised' or '--QCDinverted' (only one can exist in the datacard)"+NormalStyle()
    #    myStatus = False
    if not opts.lands and not opts.combine:
        print ErrorStyle()+"Error: use either '--lands' or '--combine' to indicate which type of cards to generate!"+NormalStyle()
        myStatus = False
    if opts.lands and opts.combine:
        print ErrorStyle()+"Error: use either '--lands' or '--combine' to indicate which type of cards to generate (not both)!"+NormalStyle()
        myStatus = False
    if not myStatus or opts.helpStatus:
        parser.print_help()
        sys.exit()
    # Run main program
    if opts.directories == None or len(opts.directories) == 0:
        if opts.debugProfiler:
            cProfile.run("main(opts, myModuleSelector, multipleDirs=None)")
        else:
            main(opts, myModuleSelector, multipleDirs=None)
        #cProfile.run("main(opts, myModuleSelector, multipleDirs=None)")
    else:
        # Find matching directories
        myDirList = os.listdir(".")
        for item in opts.directories:
            if not item in myDirList:
                raise Exception("Error: Could not find directory '%s'!"%item)
            if opts.debugProfiler:
                cProfile.run("main(opts, myModuleSelector, multipleDirs=item)")
            else:
                main(opts, myModuleSelector, multipleDirs=item)
