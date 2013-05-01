#! /usr/bin/env python

import os
import sys
import imp
from optparse import OptionParser
import gc
import cPickle
import ROOT

import HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.MulticrabPathFinder as PathFinder
from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.AnalysisModuleSelector import *
import HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.DataCardGenerator as DataCard
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.aux import load_module
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShellStyles import *
from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.ShapeHistoModifier import *
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab

def getDsetCreator(label, mcrabPath, enabledStatus=True):
    if enabledStatus:
        if mcrabPath == "":
            print "- %s: not present"%(label)
        else:
            print "- %s%s: multicrab dir found%s (%s)"%(HighlightStyle(),label,NormalStyle(),mcrabPath)
            return dataset.readFromMulticrabCfg(directory=mcrabPath)
    else:
        print "- %s: not considered"%(label)
    return None

def main(opts, moduleSelector):
    print CaptionStyle()+"*** Datacard generator ***"+NormalStyle()+"\n"
    #gc.set_debug(gc.DEBUG_LEAK | gc.DEBUG_STATS)
    #gc.set_debug(gc.DEBUG_STATS)
    #ROOT.SetMemoryPolicy(ROOT.kMemoryStrict)
    #gc.set_debug(gc.DEBUG_STATS)
    print "Loading datacard:",opts.datacard
    os.system("python %s"%opts.datacard) # Catch any errors in the input datacard
    config = load_module(opts.datacard)

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
    signalDsetCreator = getDsetCreator("Signal analysis", multicrabPaths.getSignalPath())
    embeddingDsetCreator = None
    if config.OptionReplaceEmbeddingByMC:
        print "- %sWarning:%s Embedding: estimated from signal analysis MC"%(WarningStyle(),NormalStyle())
    else:
        getDsetCreator("Embedding", multicrabPaths.getEWKPath(), not config.OptionReplaceEmbeddingByMC)
    qcdFactorisedDsetCreator = getDsetCreator("QCD factorised", multicrabPaths.getQCDFactorisedPath(), DataCard.DatacardQCDMethod.FACTORISED in myQCDMethods)
    if qcdFactorisedDsetCreator == None:
        myQCDMethods.remove(DataCard.DatacardQCDMethod.FACTORISED)
    qcdInvertedDsetCreator = getDsetCreator("QCD inverted", multicrabPaths.getQCDInvertedPath(), DataCard.DatacardQCDMethod.INVERTED in myQCDMethods)
    if qcdInvertedDsetCreator == None:
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

    # Summarise the consequences of the user choises
    myDatacardCount = len(moduleSelector.getSelectedEras())*len(moduleSelector.getSelectedSearchModes())*len(moduleSelector.getSelectedOptimizationModes())*len(myQCDMethods)
    print "\nProducing %s%d sets of datacards%s (%d era(s) x %d search mode(s) x %d optimization mode(s) x %d QCD measurement(s))\n"%(HighlightStyle(),myDatacardCount,NormalStyle(),len(moduleSelector.getSelectedEras()),len(moduleSelector.getSelectedSearchModes()),len(moduleSelector.getSelectedOptimizationModes()),len(myQCDMethods))
    # Produce datacards
    myCounter = 0
    for qcdMethod in myQCDMethods:
        for era in moduleSelector.getSelectedEras():
            for searchMode in moduleSelector.getSelectedSearchModes():
                for optimizationMode in moduleSelector.getSelectedOptimizationModes():
                    myCounter += 1
                    print "%sProducing datacard %d/%d ...%s\n"%(CaptionStyle(),myCounter,myDatacardCount,NormalStyle())
                    # Create the generator, check config file contents
                    dcgen = DataCard.DataCardGenerator(opts, config, qcdMethod)
                    # Tweak to provide the correct datasetMgrCreator to the generator
                    myQCDDsetCreator = None
                    if qcdMethod == DataCard.DatacardQCDMethod.FACTORISED:
                        myQCDDsetCreator = qcdFactorisedDsetCreator
                    elif qcdMethod == DataCard.DatacardQCDMethod.INVERTED:
                        myQCDDsetCreator = qcdInvertedDsetCreator
                    dcgen.setDsetMgrCreators(signalDsetCreator,embeddingDsetCreator,myQCDDsetCreator)
                    # Do the heavy stuff
                    dcgen.doDatacard(era,searchMode,optimizationMode)
    print "\nDatacard generator is done."
    if myDatacardCount > 10:
        print "\n(collecting some garbage before handing the shell back to you)"

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
    #parser.add_option("-e", "--era", dest="eraId", type="string", action="append", help="Evaluate specified eras")
    #parser.add_option("-m", "--searchMode", dest="searchModeId", action="append", help="name of search mode")
    #parser.add_option("-v", "--variation", dest="variationId", type="int", action="append", help="Evaluate specified variations")
    parser.add_option("--showcard", dest="showDatacard", action="store_true", default=False, help="Print datacards also to screen")
    parser.add_option("--QCDfactorised", dest="useQCDfactorised", action="store_true", default=False, help="Use factorised method for QCD measurement")
    parser.add_option("--QCDinverted", dest="useQCDinverted", action="store_true", default=False, help="Use inverted method for QCD measurement")
    parser.add_option("--debugDatasets", dest="debugDatasets", action="store_true", default=False, help="Enable debugging print for datasetMgr contents")
    parser.add_option("--debugConfig", dest="debugConfig", action="store_true", default=False, help="Enable debugging print for config parsing")
    parser.add_option("--debugMining", dest="debugMining", action="store_true", default=False, help="Enable debugging print for data mining")
    parser.add_option("--debugQCD", dest="debugQCD", action="store_true", default=False, help="Enable debugging print for QCD measurement")
    parser.add_option("--debugShapeHistogram", dest="debugShapeHistogram", action="store_true", default=False, help="Debug shape histogram modifying algorithm")
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
    if not myStatus or opts.helpStatus:
        parser.print_help()
        sys.exit()
    # Run main program
    ROOT.gROOT.SetBatch() # no flashing canvases
    main(opts, myModuleSelector)
