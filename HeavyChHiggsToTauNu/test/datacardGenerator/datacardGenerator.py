#! /usr/bin/env python

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

import HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.MulticrabPathFinder as PathFinder
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.analysisModuleSelector import *
import HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.DataCardGenerator as DataCard
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.aux import load_module
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShellStyles import *
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShapeHistoModifier import *
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab

def getDsetCreator(label, mcrabPath, mcrabInfoOutput, enabledStatus=True):
    if enabledStatus:
        if mcrabPath == "":
            mcrabInfoOutput.append("- %s: not present"%(label))
            print "- %s: not present"%(label)
        else:
            mcrabInfoOutput.append("- %s: multicrab dir found (%s)"%(label,mcrabPath))
            print "- %s%s: multicrab dir found%s (%s)"%(HighlightStyle(),label,NormalStyle(),mcrabPath)
            return dataset.readFromMulticrabCfg(directory=mcrabPath)
    else:
        mcrabInfoOutput.append("- %s: not considered"%(label))
        print "- %s: not considered"%(label)
    return None

def main(opts, moduleSelector, multipleDirs):
    print CaptionStyle()+"*** Datacard generator ***"+NormalStyle()+"\n"
    #gc.set_debug(gc.DEBUG_LEAK | gc.DEBUG_STATS)
    #gc.set_debug(gc.DEBUG_STATS)
    #ROOT.SetMemoryPolicy(ROOT.kMemoryStrict)
    #gc.set_debug(gc.DEBUG_STATS)
    print "Loading datacard:",opts.datacard
    os.system("python %s"%opts.datacard) # Catch any errors in the input datacard
    config = load_module(opts.datacard)
    # Replace source directory if necessary
    if multipleDirs != None:
        config.Path = multipleDirs
    print "Input directory:",config.Path

    # If user insisted on certain QCD method on command line, produce datacards only for that QCD method
    # Otherwise produce cards for all QCD methods
    myQCDMethods = [DataCard.DatacardQCDMethod.FACTORISED, DataCard.DatacardQCDMethod.INVERTED]
    if opts.useQCDfactorised:
        myQCDMethods = [DataCard.DatacardQCDMethod.FACTORISED]
    elif opts.useQCDinverted:
        myQCDMethods = [DataCard.DatacardQCDMethod.INVERTED]

    # Obtain dataset creators (also check multicrab directory existence)
    print "\nChecking input multicrab directory presence:"
    multicrabPaths = PathFinder.MulticrabPathFinder(config.Path)
    mcrabInfoOutput = []
    mcrabInfoOutput.append("Input directories:")

    signalDsetCreator = getDsetCreator("Signal analysis", multicrabPaths.getSignalPath(), mcrabInfoOutput)
    embeddingDsetCreator = None
    if config.OptionReplaceEmbeddingByMC:
        mcrabInfoOutput.append("- Embedding: estimated from signal analysis MC")
        print "- %sWarning:%s Embedding: estimated from signal analysis MC"%(WarningStyle(),NormalStyle())
    else:
        embeddingDsetCreator = getDsetCreator("Embedding", multicrabPaths.getEWKPath(), mcrabInfoOutput, not config.OptionReplaceEmbeddingByMC)
    qcdFactorisedDsetCreator = getDsetCreator("QCD factorised", multicrabPaths.getQCDFactorisedPath(), mcrabInfoOutput, DataCard.DatacardQCDMethod.FACTORISED in myQCDMethods)
    if qcdFactorisedDsetCreator == None and not opts.useQCDinverted:
        myQCDMethods.remove(DataCard.DatacardQCDMethod.FACTORISED)
    qcdInvertedDsetCreator = getDsetCreator("QCD inverted", multicrabPaths.getQCDInvertedPath(), mcrabInfoOutput, DataCard.DatacardQCDMethod.INVERTED in myQCDMethods)
    if qcdInvertedDsetCreator == None and not opts.useQCDfactorised:
        myQCDMethods.remove(DataCard.DatacardQCDMethod.INVERTED)

    # Require existence of signal analysis and one QCD measurement
    if signalDsetCreator == None:
        raise Exception(ErrorStyle()+"Error:"+NormalStyle()+" Signal analysis multicrab directory not found!")
    if len(myQCDMethods) == 0:
        raise Exception(ErrorStyle()+"Error:"+NormalStyle()+" QCD measurement (factorised and/or inverted) not found!")

    # Check options that are affecting the validity of the results
    if not config.OptionIncludeSystematics:
        print "\n%sWarning%s: skipping of shape systematics has been forced (flag OptionIncludeSystematics in the datacard file)"%(WarningStyle(),NormalStyle())
    if not config.OptionDoControlPlots:
        print "\n%sWarning%s: skipping of data driven control plot generation been forced (flag OptionDoControlPlots in the datacard file)"%(WarningStyle(),NormalStyle())

    # Find list of available eras, search modes, and optimization modes common for all multicrab directories
    moduleSelector.setPrimarySource("Signal analysis", signalDsetCreator)
    if embeddingDsetCreator != None:
        moduleSelector.addOtherSource("Embedding", embeddingDsetCreator)
    if qcdFactorisedDsetCreator != None:
        moduleSelector.addOtherSource("QCD factorised", qcdFactorisedDsetCreator)
    if qcdInvertedDsetCreator != None:
        moduleSelector.addOtherSource("QCD inverted", qcdInvertedDsetCreator)
    moduleSelector.doSelect(opts)
    moduleSelector.closeFiles()

    # Separate light and heavy masses if they are not separated
    mySearchModeList = moduleSelector.getSelectedSearchModes()
    if ("Light" not in mySearchModeList and len(config.LightMassPoints) > 0 and len(config.HeavyMassPoints) > 0) or \
       ("Heavy" not in mySearchModeList and len(config.HeavyMassPoints) > 0 and len(config.LightMassPoints) > 0):
        mySearchModeList.append(mySearchModeList[0])

    # Summarise the consequences of the user choises
    myDatacardCount = len(moduleSelector.getSelectedEras())*len(moduleSelector.getSelectedSearchModes())*len(moduleSelector.getSelectedOptimizationModes())*len(myQCDMethods)
    print "\nProducing %s%d sets of datacards%s (%d era(s) x %d search mode(s) x %d optimization mode(s) x %d QCD measurement(s))\n"%(HighlightStyle(),myDatacardCount,NormalStyle(),len(moduleSelector.getSelectedEras()),len(moduleSelector.getSelectedSearchModes()),len(moduleSelector.getSelectedOptimizationModes()),len(myQCDMethods))
    # Produce datacards
    myCounter = 0
    myStartTime = time.time()
    myOriginalName = config.DataCardName
    myOutputDirectories = []
    for qcdMethod in myQCDMethods:
        for era in moduleSelector.getSelectedEras():
            mySearchModeCounter = 0
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
                mySearchModeCounter += 1
                for optimizationMode in moduleSelector.getSelectedOptimizationModes():
                    ROOT.gROOT.CloseFiles()
                    ROOT.gROOT.GetListOfCanvases().Delete()
                    # After these, three histograms are still left in memory
                    # Worst memory leak seems to come from storing and not freeing the main counters
                    # Create the dataset creator managers separately for each module
                    signalDsetCreator = getDsetCreator("Signal analysis", multicrabPaths.getSignalPath(), mcrabInfoOutput)
                    embeddingDsetCreator = None
                    if config.OptionReplaceEmbeddingByMC:
                        mcrabInfoOutput.append("- Embedding: estimated from signal analysis MC")
                        print "- %sWarning:%s Embedding: estimated from signal analysis MC"%(WarningStyle(),NormalStyle())
                    else:
                        embeddingDsetCreator = getDsetCreator("Embedding", multicrabPaths.getEWKPath(), mcrabInfoOutput, not config.OptionReplaceEmbeddingByMC)
                    myQCDDsetCreator = None
                    if qcdMethod == DataCard.DatacardQCDMethod.FACTORISED:
                        myQCDDsetCreator = getDsetCreator("QCD factorised", multicrabPaths.getQCDFactorisedPath(), mcrabInfoOutput, DataCard.DatacardQCDMethod.FACTORISED in myQCDMethods)
                        if myQCDDsetCreator == None:
                            raise Exception(ErrorLabel()+"Could not find factorised QCD pseudomulticrab!"+NormalStyle())
                    elif qcdMethod == DataCard.DatacardQCDMethod.INVERTED:
                        myQCDDsetCreator = getDsetCreator("QCD inverted", multicrabPaths.getQCDInvertedPath(), mcrabInfoOutput, DataCard.DatacardQCDMethod.INVERTED in myQCDMethods)
                        if myQCDDsetCreator == None:
                            raise Exception(ErrorLabel()+"Could not find inverted QCD pseudomulticrab!"+NormalStyle())
                    # Print progress info
                    myCounter += 1
                    print "%sProducing datacard %d/%d ...%s\n"%(CaptionStyle(),myCounter,myDatacardCount,NormalStyle())
                    # Create the generator, check config file contents
                    dcgen = DataCard.DataCardGenerator(opts, config, qcdMethod)
                    # Tweak to provide the correct datasetMgrCreator to the generator
                    if qcdMethod == DataCard.DatacardQCDMethod.FACTORISED:
                        print "era=%s%s%s, searchMode=%s%s%s, optimizationMode=%s%s%s, QCD method=%sfactorised%s\n"%(HighlightStyle(),era,NormalStyle(),HighlightStyle(),searchMode,NormalStyle(),HighlightStyle(),optimizationMode,NormalStyle(),HighlightStyle(),NormalStyle())
                    elif qcdMethod == DataCard.DatacardQCDMethod.INVERTED:
                        print "era=%s%s%s, searchMode=%s%s%s, optimizationMode=%s%s%s, QCD method=%sinverted%s\n"%(HighlightStyle(),era,NormalStyle(),HighlightStyle(),searchMode,NormalStyle(),HighlightStyle(),optimizationMode,NormalStyle(),HighlightStyle(),NormalStyle())
                    dcgen.setDsetMgrCreators(signalDsetCreator,embeddingDsetCreator,myQCDDsetCreator)
                    # Do the heavy stuff
                    myOutputDirectories.append(dcgen.doDatacard(era,searchMode,optimizationMode,mcrabInfoOutput))
    print "\nDatacard generator is done."
    myEndTime = time.time()
    print "Running took on average %.1f s / datacard (total elapsed time: %.1f s)"%((myEndTime-myStartTime)/float(myDatacardCount), (myEndTime-myStartTime))
    # Generate plots for systematics
    if opts.systAnalysis:
        for d in myOutputDirectories:
            print "\nGenerating systematics plots for",d
            os.chdir(d)
            os.system("../../brlimit/plotShapes.py")
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
    for d in myOutputDirectories:
        fTar.add(d)
    fTar.close()
    print "Created archive of results directories to: %s%s%s"%(HighlightStyle(),myFilename,NormalStyle())
    #gc.collect()
    #ROOT.SetMemoryPolicy( ROOT.kMemoryHeuristics)
    #memoryDump()

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

def testShapeHistogram():
    # FIXME: Move this code as validate() of the ShapeHistoModifier class
    print "Testing shape histogram modifying algorithm:"
    # Create specification
    ShapeHistogramsDimensions = { "bins": 6,
                              "rangeMin": 0.0,
                              "rangeMax": 400.0,
                              "variableBinSizeLowEdges": [0.0,20.0,40.0,60.0,80.0,120.0], # if an empty list is given, then uniform bin width is used
                              "xtitle": "Transverse mass / GeV",
                              "ytitle": "Events" }
    # Create source histogram
    hSrc = ROOT.TH1F("hsrc","hsrc",40, 0.0, 400.0)
    hSrc.Sumw2()
    for i in range(0,45):
        hSrc.Fill(i*10-.5,i)
    print "Source:"
    for k in range(0,hSrc.GetNbinsX()+2):
        print "  src bin %d = %f +- %f"%(k,hSrc.GetBinContent(k),hSrc.GetBinError(k))
    # Invoke shape histo class
    myShapeHistoModifier = ShapeHistoModifier(histoSpecs=ShapeHistogramsDimensions,debugMode=True)
    # Obtain empty histogram
    h = myShapeHistoModifier.createEmptyShapeHistogram("hello")
    # Add source
    myShapeHistoModifier.addShape(source=hSrc,dest=h)
    print "After adding source:"
    for k in range(0,h.GetNbinsX()+2):
        print "  dest bin %d = %f +- %f"%(k,h.GetBinContent(k),h.GetBinError(k))
    myShapeHistoModifier.subtractShape(source=hSrc,dest=h)
    myShapeHistoModifier.finaliseShape(dest=h)
    print "After subtracting and finalising:"
    for k in range(0,h.GetNbinsX()+2):
        print "  dest bin %d = %f +- %f"%(k,h.GetBinContent(k),h.GetBinError(k))
    sys.exit()

if __name__ == "__main__":
    myModuleSelector = AnalysisModuleSelector() # Object for selecting data eras, search modes, and optimization modes

    parser = OptionParser(usage="Usage: %prog [options]",add_help_option=False,conflict_handler="resolve")
    parser.add_option("-h", "--help", dest="helpStatus", action="store_true", default=False, help="Show this help message and exit")
    parser.add_option("-x", "--datacard", dest="datacard", action="store", help="Name (incl. path) of the datacard to be used as an input")
    myModuleSelector.addParserOptions(parser)
    parser.add_option("--lands", dest="lands", action="store_true", default=False, help="Generate datacards for LandS")
    parser.add_option("--combine", dest="combine", action="store_true", default=False, help="Generate datacards for Combine")
    parser.add_option("--multipleDirs", dest="multipleDirs", action="store", help="Name of base dir for creating datacards for multiple directories (wildcard is added at the end)")
    parser.add_option("--systAnalysis", dest="systAnalysis", action="store_true", default=False, help="Runs the macro for generating systematic uncertainties plots")
    parser.add_option("--showcard", dest="showDatacard", action="store_true", default=False, help="Print datacards also to screen")
    parser.add_option("--QCDfactorised", dest="useQCDfactorised", action="store_true", default=False, help="Use factorised method for QCD measurement")
    parser.add_option("--QCDinverted", dest="useQCDinverted", action="store_true", default=False, help="Use inverted method for QCD measurement")
    parser.add_option("--debugDatasets", dest="debugDatasets", action="store_true", default=False, help="Enable debugging print for datasetMgr contents")
    parser.add_option("--debugConfig", dest="debugConfig", action="store_true", default=False, help="Enable debugging print for config parsing")
    parser.add_option("--debugMining", dest="debugMining", action="store_true", default=False, help="Enable debugging print for data mining")
    parser.add_option("--debugQCD", dest="debugQCD", action="store_true", default=False, help="Enable debugging print for QCD measurement")
    parser.add_option("--debugShapeHistogram", dest="debugShapeHistogram", action="store_true", default=False, help="Debug shape histogram modifying algorithm")
    parser.add_option("--debugControlPlots", dest="debugControlPlots", action="store_true", default=False, help="Enable debugging print for data-driven control plots")
    parser.add_option("--debugProfiler", dest="debugProfiler", action="store_true", default=False, help="Enable profiler")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=False, help="Print more information")
    (opts, args) = parser.parse_args()

    myStatus = True
    if opts.debugShapeHistogram:
        testShapeHistogram()
    if opts.datacard == None:
        print ErrorStyle()+"Error: Missing datacard!"+NormalStyle()+"\n"
        myStatus = False
    if opts.useQCDfactorised and opts.useQCDinverted:
        print ErrorStyle()+"Error: use either '--QCDfactorised' or '--QCDinverted' (only one can exist in the datacard)"+NormalStyle()
        myStatus = False
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
    if opts.multipleDirs == None:
        if opts.debugProfiler:
            cProfile.run("main(opts, myModuleSelector, multipleDirs=None)")
        else:
            main(opts, myModuleSelector, multipleDirs=None)
        #cProfile.run("main(opts, myModuleSelector, multipleDirs=None)")
    else:
        # Find matching directories
        (head, tail) = os.path.split(opts.multipleDirs)
        myDirList = os.listdir(head)
        for myDir in myDirList:
            if myDir.startswith(tail):
                if opts.debugProfiler:
                    cProfile.run("main(opts, myModuleSelector, multipleDirs=os.path.join(head,myDir))")
                else:
                    main(opts, myModuleSelector, multipleDirs=os.path.join(head,myDir))
