#! /usr/bin/env python

import os
import sys
import imp
from optparse import OptionParser
import gc
import cPickle
import ROOT

import HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.MulticrabPathFinder as PathFinder
import HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.DataCardGenerator as DataCard
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.aux import load_module
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShellStyles import *
from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.ShapeHistoModifier import *
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab

def main(opts):
    #gc.set_debug(gc.DEBUG_LEAK | gc.DEBUG_STATS)
    #gc.set_debug(gc.DEBUG_STATS)
    #ROOT.SetMemoryPolicy(ROOT.kMemoryStrict)
    #gc.set_debug(gc.DEBUG_STATS)
    print "Loading datacard:", opts.datacard
    config = load_module(opts.datacard)

    # If user insisted on certain QCD method on command line, produce datacards only for that QCD method
    # Otherwise produce cards for all QCD methods
    myQCDMethods = [DataCard.DatacardQCDMethod.FACTORISED, DataCard.DatacardQCDMethod.INVERTED]
    if opts.useQCDfactorised:
        myQCDMethods = [DataCard.DatacardQCDMethod.FACTORISED]
    elif opts.useQCDinverted:
        myQCDMethods = [DataCard.DatacardQCDMethod.INVERTED]

    # Find list of optimisation jobs, if they exist
    multicrabPaths = PathFinder.MulticrabPathFinder(config.Path)
    myModules = []
    if config.SignalAnalysis != None:
        myModules = obtainOptimisationVariationList(multicrabPaths.getSignalPath())
    if config.QCDFactorisedAnalysis != None:
        myQCDFactList = obtainOptimisationVariationList(multicrabPaths.getQCDFactorisedPath())
        if len(myModules) == 0:
            myModules.extend(myQCDFactList)
    if config.QCDInvertedAnalysis != None:
        myQCDInvList = obtainOptimisationVariationList(multicrabPaths.getQCDInvertedPath())
        if len(myModules) == 0:
            myModules.extend(myQCDInvList)
    # Print module list, if asked
    if opts.listVariations == True:
        print "Available modules found (use -v to add by index number)"
        for i in range(0,len(myModules)):
            if myModules[i] == None:
                print "  %d: (default module)"%i
            else:
                print "  %d: %s"%(i,myModules[i])
        sys.exit()

    # Select variations from modules
    myVariations = []
    if opts.variationId != None:
        for varid in opts.variationId:
            if varid < len(myModules):
                myVariations.append(myModules[varid])
            else:
                print "List of available variations:"
                for i in range(0,len(myModules)):
                    if myModules[i] == None:
                        print "  %d: (default module)"%i
                    else:
                        print "  %d: %s"%(i,myModules[i])
                    raise Exception(ErrorStyle()+"Error:"+NormalStyle()+" you asked for variation %d, which is not available (see above list)!")
    else:
        myVariations.extend(myModules)
    # Print info about selected variations
    print CaptionStyle()+"*** Datacard generator ***"+NormalStyle()+"\n"
    print "Cards will be generaged for following variations (use -v to add a variation by its index number)"
    for v in myVariations:
        if v == None:
            print "  (default module)"
        else:
            print "  "+v
    print "Altogether %d variations\n"%len(myVariations)
    # Produce cards
    myCounter = 0
    for method in myQCDMethods:
        for module in myVariations:
            myCounter += 1
            print "\n"+HighlightStyle()+"Variation %d/%d ..."%(myCounter,len(myVariations))+NormalStyle()+"\n"
            if method == DataCard.DatacardQCDMethod.FACTORISED:
                if module != None:
                    if module not in myQCDFactList:
                        print "Module '"+module+"' exists in signal analysis but not in QCD factorised, skipping ..."
                        print myQCDFactList
                    else:
                        DataCard.DataCardGenerator(config,opts,method,module)
                else:
                    DataCard.DataCardGenerator(config,opts,method,None)
            if method == DataCard.DatacardQCDMethod.INVERTED:
                if module != None:
                    if module not in myQCDInvList:
                        print "Module '"+module+"' exists in signal analysis but not in QCD inverted, skipping ..."
                    else:
                        DataCard.DataCardGenerator(config,opts,method,module)
                else:
                    DataCard.DataCardGenerator(config,opts,method,None)
    print "\nDatacard generator is done."

    #gc.collect()
    #ROOT.SetMemoryPolicy( ROOT.kMemoryHeuristics)
    #memoryDump()

def obtainOptimisationVariationList(taskPath):
    if not os.path.exists(taskPath):
        return []
    taskDirs = multicrab.getTaskDirectories(None, taskPath+"/multicrab.cfg")
    # take first task and obtain its result histogram
    myRootFile = None
    for task in taskDirs:
        myFilename = task+"/res/histograms-"+os.path.basename(task)+".root"
        if os.path.exists(myFilename):
            myRootFile = ROOT.TFile.Open(myFilename)
            # root file is opened, loop over keys to find directories
            myModules = []
            for i in range(0, myRootFile.GetNkeys()):
                myKey = myRootFile.GetListOfKeys().At(i)
                if myKey.IsFolder():
                    # Ignore systematics directories
                    myTitle = myKey.GetTitle()
                    if not "Plus" in myTitle and not "Minus" in myTitle and not "configInfo" in myTitle:
                        myName = myTitle
                        if myTitle.find("Opt") > 0:
                            # Remove prefix
                            myName = myTitle[myTitle.find("Opt"):len(myTitle)]
                        else:
                            # Fall back to default
                            myName = None
                        myModules.append(myName)
            myRootFile.Close()
            return myModules
    # No root file has been found
    return []

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
    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("-x", "--datacard", dest="datacard", action="store", help="Name (incl. path) of the datacard to be used as an input")
    parser.add_option("-l", "--listVariations", dest="listVariations", action="store_true", default=False, help="Print a list of available variations")
    parser.add_option("--showcard", dest="showDatacard", action="store_true", default=False, help="Print datacards also to screen")
    parser.add_option("--QCDfactorised", dest="useQCDfactorised", action="store_true", default=False, help="Use factorised method for QCD measurement")
    parser.add_option("--QCDinverted", dest="useQCDinverted", action="store_true", default=False, help="Use inverted method for QCD measurement")
    parser.add_option("--debugConfig", dest="debugConfig", action="store_true", default=False, help="Enable debugging print for config parsing")
    parser.add_option("--debugMining", dest="debugMining", action="store_true", default=False, help="Enable debugging print for data mining")
    parser.add_option("--debugQCD", dest="debugQCD", action="store_true", default=False, help="Enable debugging print for QCD measurement")
    parser.add_option("--debugShapeHistogram", dest="debugShapeHistogram", action="store_true", default=False, help="Debug shape histogram modifying algorithm")
    parser.add_option("-v", "--variation", dest="variationId", type="int", action="append", help="Evaluates specified variations")
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
    if not myStatus:
        parser.print_help()
        sys.exit()
    # Run main program
    ROOT.gROOT.SetBatch() # no flashing canvases
    main(opts)
