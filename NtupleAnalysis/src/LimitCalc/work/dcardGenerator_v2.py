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
./dcardGenerator.py -x <input-datacard> -d <pseudo-multicrab-dir> [opts]


LAST USED:
./dcardGenerator_v2.py -x dcardHplus2tb_2016Data.py -d limits2016/ --ht2b


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
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux
from HiggsAnalysis.NtupleAnalysis.tools.ShellStyles import *
import HiggsAnalysis.NtupleAnalysis.tools.multicrab as multicrab


#================================================================================================
# Function definition
#================================================================================================
def PrintOptions(moduleSelector):
    nEras       = len(moduleSelector.getSelectedEras())
    nModes      = len(moduleSelector.getSelectedSearchModes())
    nOptModes   = len(moduleSelector.getSelectedOptimizationModes())
    nDatacards  = nEras*nModes*nOptModes

    msg  = "Producing %d set(s) of datacards" % (nDatacards)
    msg += " [%d era(s) x %d search mode(s) x %d optimization mode(s)]" % (nEras, nModes, nOptModes)
    Verbose(HighlightAltStyle() + msg + NormalStyle())
    return

def PrintDsetInfo(signalDsetCreator, bkg1DsetCreator, bkg2DsetCreator, verbose=False):
    if not verbose:
        return
    
    Print("Signal dataset dir is %s" % (signalDsetCreator.getBaseDirectory()), True)
    for d in signalDsetCreator.getDatasetNames():
        Verbose(d, False)

    Print("Bkg1 dataset dir is %s" % (bkg1DsetCreator.getBaseDirectory()), False)
    for d in bkg1DsetCreator.getDatasetNames():
        Verbose(d, False)

    Print("Bkg2 dataset dir is %s" % (bkg2DsetCreator.getBaseDirectory()), False)
    for d in bkg2DsetCreator.getDatasetNames():
        Verbose(d, False)
    return

def SetModuleSelectorSources(moduleSelector, primaryLabel, primaryDsetCreator, secondaryLabel, secondaryDsetCreator, tertiaryLabel, tertiaryDsetCreator, opts):

    moduleSelector.setPrimarySource(primaryLabel, primaryDsetCreator)
    mySources = [primaryLabel]

    if secondaryDsetCreator != None:
        moduleSelector.addOtherSource(secondaryLabel, secondaryDsetCreator)
        mySources.append(secondaryLabel)

    if tertiaryDsetCreator != None:
        moduleSelector.addOtherSource(tertiaryLabel, tertiaryDsetCreator)
        mySources.append(tertiaryLabel)

    Verbose("Added %i sources to the module selector with labels: %s" % (len(mySources), ", ".join(mySources)), True)
    moduleSelector.doSelect(opts, printSelections=opts.verbose)
    moduleSelector.closeFiles()
    return


def CheckOptions(config):
    '''
    Check various options defined in the config (=opts.datacard) and warns user if some flags
    are disabled
    '''
    msgs = []
    if not config.OptionIncludeSystematics:
        msg = NoteStyle() + "Skipping of shape systematics has been forced (flag OptionIncludeSystematics in the datacard file)"
        msgs.append(msg)

    if not config.OptionDoControlPlots:
        msg = NoteStyle() + "Skipping of data-driven control plot generation been forced (flag OptionDoControlPlots in the datacard file)"
        msgs.append(msg)

    if not config.BlindAnalysis:
        msg = ErrorStyle() + "Unblinding analysis results forced been forced (flag BlindAnalysis in the datacard file)"
        msgs.append(msg)

    if len(msgs) < 1:
        return

    # Print all warnings!
    for i, m in enumerate(msgs, 1):
        Print(m + NormalStyle(), i==1)
    return

def getSignalDsetCreator(multicrabPaths, signalLabel, mcrabInfoOutput):
    signalDsetCreator = getDsetCreator(signalLabel, multicrabPaths.getSignalPath(), mcrabInfoOutput)
    if multicrabPaths.getSignalPath() == "":
        msg = ErrorLabel() + " Signal analysis multicrab directory not found!"
        raise Exception(msg)
    return signalDsetCreator

def getBkgDsetCreators(multicrabPaths, bkg1Label, bkg2Label, fakesFromData, mcrabInfoOutput):
    
    if fakesFromData:
        if opts.h2tb:
            msg = "Fake-b (Genuine-b) will be estimated from data (signal analysis MC)"
            if multicrabPaths.getGenuineBPath() == "" or multicrabPaths.getFakeBPath() == "":
                raise Exception(ErrorStyle() + "Could not find the path for Genuine-b and/or Fake-b datasets" + NormalStyle() )
            bkg1DsetCreator = getDsetCreator(bkg1Label, multicrabPaths.getGenuineBPath(), mcrabInfoOutput, fakesFromData)
            bkg2DsetCreator = getDsetCreator(bkg2Label, multicrabPaths.getFakeBPath()   , mcrabInfoOutput, fakesFromData)
        else:
            msg = "Fake-tau (Genuine-tau) will be estimated from data (signal analysis MC)"
            if multicrabPaths.getEWKPath() == "" or multicrabPaths.getQCDInvertedPath() == "":
                raise Exception(ErrorStyle() + "Could not find the path for Genuine-b and/or Fake-b datasets" + NormalStyle() )
            bkg1DsetCreator = getDsetCreator(bkg1Label, multicrabPaths.getEWKPath()        , mcrabInfoOutput, fakesFromData)  #fixme: santeri check
            bkg2DsetCreator = getDsetCreator(bkg2Label, multicrabPaths.getQCDInvertedPath(), mcrabInfoOutput, fakesFromData)  #fixme: santeri check
    else:
        msg = "QCD and EWK will be estimated from signal analysis MC"
        if multicrabPaths.getSignalPath() == "":
                raise Exception(ErrorStyle() + "Could not find the path for EWK MC and/or QCD MC datasets" + NormalStyle() )
        bkg1DsetCreator = getDsetCreator(bkg1Label, multicrabPaths.getSignalPath(), mcrabInfoOutput, not fakesFromData)  #fixme: santeri check
        bkg2DsetCreator = getDsetCreator(bkg2Label, multicrabPaths.getQCDInvertedPath(), mcrabInfoOutput, not fakesFromData)  #fixme: santeri check
            
    mcrabInfoOutput.append("- " + msg)
    Verbose(NoteStyle() + msg + NormalStyle() )
    return bkg1DsetCreator, bkg2DsetCreator

def GetDatasetLabels(config, fakesFromData, opts):
    signalLabel = "Signal Analysis"
    if fakesFromData:
        if opts.h2tb:
            bkg1Label = "EWK Genuine-b"
            bkg2Label = "Fake-b"
        else:
            bkg1Label = "EWK Genuine-tau"
            bkg2Label = "Fake-tau"
    else:
        bkg1Label = "EWK MC"
        bkg2Label = "QCD MC"
    return signalLabel, bkg1Label, bkg2Label

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

def main(opts, moduleSelector, multipleDirs):
    
    # Fixme: Is this used/needed?
    if 0:
        gc.set_debug(gc.DEBUG_LEAK | gc.DEBUG_STATS)
        gc.set_debug(gc.DEBUG_STATS)
        ROOT.SetMemoryPolicy(ROOT.kMemoryStrict)
        gc.set_debug(gc.DEBUG_STATS)

    # Catch any errors in the input datacard
    Verbose("Validating datacard \"%s\"" % (opts.datacard) )
    os.system("python %s" % opts.datacard)

    # Load the datacard
    Verbose("Loading datacard \"%s\"" % (opts.datacard) )
    config = aux.load_module(opts.datacard)

    # Replace source directory if necessary
    if multipleDirs != None:
        config.Path = multipleDirs
    Verbose("Input directory is \"%s\"" % (config.Path) )

    # Obtain dataset creators (also check multicrab directory existence)
    Verbose("Checking input multicrab directory presence")
    multicrabPaths  = PathFinder.MulticrabPathFinder(config.Path, opts.h2tb, opts.verbose)
    mcrabInfoOutput = []
    mcrabInfoOutput.append("Input directories:")
    if opts.verbose:
        multicrabPaths.PrintInfo()

    # Determine dataset labels. Fixme: adopt global names (e.g. fakes, genuine)
    if opts.h2tb:
        fakesFromData = (config.OptionFakeBMeasurementSource == "DataDriven")
    else:
        fakesFromData = (config.OptionGenuineTauBackgroundSource == "DataDriven")
    signalLabel, bkg1Label, bkg2Label = GetDatasetLabels(config, fakesFromData, opts)

    # Create datasets
    Verbose("Creating signal & bkg datasets")
    signalDsetCreator = getSignalDsetCreator(multicrabPaths, signalLabel, mcrabInfoOutput)
    bkg1DsetCreator, bkg2DsetCreator = getBkgDsetCreators(multicrabPaths, bkg1Label, bkg2Label, fakesFromData, mcrabInfoOutput)
    PrintDsetInfo(signalDsetCreator, bkg1DsetCreator, bkg2DsetCreator, opts.verbose) #bkg1 = EWK MC, bkg2 = FakeB if (data-driven==True)

    # Check options that are affecting the validity of the results
    CheckOptions(config)

    # Find list of available eras, search modes, and optimization modes common for all multicrab directories
    Verbose("Find list of available eras, search modes, and optimization modes common for all multicrab directories", True)
    SetModuleSelectorSources(moduleSelector, signalLabel, signalDsetCreator, bkg1Label, bkg1DsetCreator, bkg2Label, bkg2DsetCreator, opts) #fixme: santeri check. bkg1=Genuine, bkg2=Fake
    
    # Summarise the consequences of the user choises
    PrintOptions(moduleSelector)

    # Produce datacards
    myCounter = 0
    myStartTime = time.time()
    myOriginalName = config.DataCardName
    myOutputDirectories = []
    nDatacards = 0
    nEras  = len(moduleSelector.getSelectedEras())
    nModes = len(moduleSelector.getSelectedSearchModes())
    nOpts  = len(moduleSelector.getSelectedOptimizationModes())

    # For-loop: Data eras
    for i, era in enumerate(moduleSelector.getSelectedEras(), 1):        
        msg  = "{:<9} {:>3} {:<1} {:<3} {:<50}".format("Era", "%i" % i, "/", "%s:" % (nEras), era)
        Print(HighlightAltStyle() + msg + NormalStyle(), i==1)

        # For-loop: Search modes
        for j, searchMode in enumerate(moduleSelector.getSelectedSearchModes(), 1):
            msg = "{:<9} {:>3} {:<1} {:<3} {:<50}".format("Mode", "%i" % j, "/", "%s:" % (nModes), searchMode)
            Print(HighlightAltStyle() + msg + NormalStyle(), False)

            # For-loop: Optimization modes            
            for k, optimizationMode in enumerate(moduleSelector.getSelectedOptimizationModes(), 1):
                nDatacards +=1

                msg = "{:<9} {:>3} {:<1} {:<3} {:<50}".format("Opt", "%i" % k, "/", "%s:" % (nOpts), optimizationMode)
                Print(HighlightAltStyle() + msg + NormalStyle(), False)
                
                # FIXME: santeri Crashes!
                #if hasattr(ROOT.gROOT, "CloseFiles"):
                #    ROOT.gROOT.CloseFiles()
                #ROOT.gROOT.GetListOfCanvases().Delete()

                Verbose("Create the datacard generator & check config file contents")
                dcgen = DataCard.DataCardGenerator(opts, config, verbose=opts.verbose, h2tb=opts.h2tb)                 
                dcgen.setDsetMgrCreators(signalDsetCreator, bkg1DsetCreator, bkg2DsetCreator)

                # Do the heavy stuff
                myDir = dcgen.doDatacard(era, searchMode, optimizationMode, mcrabInfoOutput)
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
    myFilename  = "datacards_archive_%s.tgz" % (myTimestamp)
    fTar = tarfile.open(myFilename, mode="w:gz")
    
    # For-loop: All output dirs
    for d in myOutputDirectories:
        fTar.add(d)
    fTar.close()

    msg = "Created archive of results directories to "
    Print(msg + SuccessStyle() + myFilename + NormalStyle())
    
    if 0:
        gc.collect()
        ROOT.SetMemoryPolicy( ROOT.kMemoryHeuristics)
        memoryDump()
    return
    

if __name__ == "__main__":

    # Default Values
    HELP          = False
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
    HToTB         = False

    # Object for selecting data eras, search modes, and optimization modes
    myModuleSelector = analysisModuleSelector.AnalysisModuleSelector() 

    parser = OptionParser(usage="Usage: %prog [options]", add_help_option=False, conflict_handler="resolve")

    parser.add_option("-h", "--help", dest="helpStatus", action="store_true", default=HELP, 
                      help="Show this help message and exit [default: %s]" % HELP)

    parser.add_option("-x", "--datacard", dest="datacard", action="store", 
                      help="Name (incl. path) of the datacard to be used as an input")

    myModuleSelector.addParserOptions(parser)

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

    parser.add_option("--ht2b", dest="h2tb", action="store_true", default=HToTB,
                      help="Flag to indicate that settings should reflect h2tb analysis [default: %s]" % (HToTB) )
    
    (opts, args) = parser.parse_args()

    myStatus = True

    if opts.debugShapeHistogram:
        testShapeHistogram()

    if opts.datacard == None:
        print ErrorStyle()+"Error: Missing datacard!"+NormalStyle()+"\n"
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
        myDirs = os.listdir(".")
        nDirs  = len(opts.directories)
        Verbose("Creating datacards for %i directories" % (nDirs) )

        # For-loop: All directories
        for i, d in enumerate(opts.directories, 1):

            # Remove "/" from end of dir
            d = aux.rchop(d, "/")

            msg   = "{:<9} {:>3} {:<1} {:<3} {:<50}".format("Directory", "%i" % i, "/", "%s:" % (nDirs), d)
            Print(SuccessStyle() + msg + NormalStyle(), i==1)

            if not d in myDirs:
                raise Exception("Error: Could not find directory '%s'!" % (d) )
            if opts.debugProfiler:
                cProfile.run("main(opts, myModuleSelector, multipleDirs=d)")
            else:
                main(opts, myModuleSelector, multipleDirs=d)
