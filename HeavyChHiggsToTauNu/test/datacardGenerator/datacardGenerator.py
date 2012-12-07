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
    print CaptionStyle()+"*** Datacard generator ***"+NormalStyle()+"\n"
    #gc.set_debug(gc.DEBUG_LEAK | gc.DEBUG_STATS)
    #gc.set_debug(gc.DEBUG_STATS)
    #ROOT.SetMemoryPolicy(ROOT.kMemoryStrict)
    #gc.set_debug(gc.DEBUG_STATS)
    print "Loading datacard:",opts.datacard
    config = load_module(opts.datacard)

    # If user insisted on certain QCD method on command line, produce datacards only for that QCD method
    # Otherwise produce cards for all QCD methods
    myQCDMethods = [DataCard.DatacardQCDMethod.FACTORISED, DataCard.DatacardQCDMethod.INVERTED]
    if opts.useQCDfactorised:
        myQCDMethods = [DataCard.DatacardQCDMethod.FACTORISED]
    elif opts.useQCDinverted:
        myQCDMethods = [DataCard.DatacardQCDMethod.INVERTED]

    # Check multicrab directory existence
    # Find also list of eras and variations for which to produce datacards
    print "\nChecking input multicrab directory presence:"
    multicrabPaths = PathFinder.MulticrabPathFinder(config.Path)
    myEras = []
    myModules = []
    if config.SignalAnalysis != None:
        myEras,myModules = obtainErasAndModules(multicrabPaths.getSignalPath())
        print "- %ssignal analysis: found%s (%s)"%(HighlightStyle(),NormalStyle(),multicrabPaths.getSignalPath())
    else:
        raise Exception(ErrorStyle()+"Error:"+NormalStyle()+" you have not specified SignalAnalysis in the datacard!")
    if config.OptionReplaceEmbeddingByMC:
        print "- %sembedding: estimated from signal analysis MC%s"%(WarningStyle(),NormalStyle())
    else:
        if config.EmbeddingAnalysis != None:
            myEmbeddingEras,myEmbeddingModules = obtainErasAndModules(multicrabPaths.getEWKPath())
            myEmbeddingEras,myEmbeddingModules = checkEraAndVariationMatching(myEras,myModules,myQCDEras,myQCDFactList,"Embedding")
            print "- %sembedding: found%s (%s)"%(HighlightStyle(),NormalStyle(),multicrabPaths.getEWKPath())
        else:
            print "- embedding: not considered or not present"
    if DataCard.DatacardQCDMethod.FACTORISED in myQCDMethods:
        if config.QCDFactorisedAnalysis != None:
            myQCDEras,myQCDFactList = obtainErasAndModules(multicrabPaths.getQCDFactorisedPath())
            myEras,myModules = checkEraAndVariationMatching(myEras,myModules,myQCDEras,myQCDFactList,"QCD factorised")
            print "- %sQCD factorised: found%s (%s)"%(HighlightStyle(),NormalStyle(),multicrabPaths.getQCDFactorisedPath())
        else:
            print "- QCD factorised: not considered or not present"
    else:
        print "- QCD factorised: not considered or not present"
    if DataCard.DatacardQCDMethod.INVERTED in myQCDMethods:
        if config.QCDInvertedAnalysis != None:
            myQCDEras,myQCDInvList = obtainErasAndModules(multicrabPaths.getQCDInvertedPath())
            myEras,myModules = checkEraAndVariationMatching(myEras,myModules,myQCDEras,myQCDInvList,"QCD inverted")
            print "- %sQCD inverted: found%s (%s)"%(HighlightStyle(),NormalStyle(),multicrabPaths.getQCDInvertedPath())
        else:
            print "- QCD inverted: not considered or not present"
    else:
        print "- QCD inverted: not considered or not present"

    # Check options that are affecting the validity of the results
    if not config.OptionIncludeSystematics:
        print WarningStyle()+"\nWarning: skipping of shape systematics has been forced (flag OptionIncludeSystematics in the datacard file)",NormalStyle()
    if not config.OptionDoControlPlots:
        print WarningStyle()+"\nWarning: skipping of data driven control plot generation been forced (flag OptionDoControlPlots in the datacard file)"+NormalStyle()

    # Print era list and determine which ones are selected
    mySelectedEras = []
    print "\nAvailable eras found: (use -e to add, for example: -e Run2011A -e Run2011B)"
    if opts.eraId == None:
        print "(you did not ask for specific era(s) so by default all possibilities will be considered...)"
    for era in myEras:
        if era == "":
            print HighlightStyle()+"--> (default unspecified era, will be used automatically)"+NormalStyle()
            mySelectedEras.append("")
        else:
            if opts.eraId != None:
                if era in opts.eraId:
                    print HighlightStyle()+"--> %s"%(era)+NormalStyle()
                    mySelectedEras.append(era)
                else:
                    print "    %s"%(era)
            else:
                print HighlightStyle()+"--> %s"%(era)+NormalStyle()
                mySelectedEras.append(era)
    # Print variation list and determine which ones are selected
    mySelectedVariations = []
    print "\nAvailable variations found: (use -v to add by index number, for example -v 0 -v 3)"
    if opts.variationId == None:
        print "(you did not ask for specific variation(s) so by default all possibilities will be considered...)"
    for i in range(0,len(myModules)):
        if myModules[i] == "":
            print HighlightStyle()+"--> (default module)"%i+NormalStyle()
            mySelectedVariations.append("")
        else:
            if opts.variationId != None:
                if i in opts.VariationId:
                    print HighlightStyle()+"--> %d: %s"%(i,myModules[i])+NormalStyle()
                    mySelectedVariations.append(myModules[i])
                else:
                    print "    %d: %s"%(i,myModules[i])
            else:
                print HighlightStyle()+"--> %d: %s"%(i,myModules[i])+NormalStyle()
                mySelectedVariations.append(myModules[i])
    if opts.listVariations == True:
        sys.exit()
    # Check that the command line options for eras and variations make sense
    if opts.eraId != None:
        for era in opts.eraId:
            if not era in myEras:
                raise Exception(ErrorStyle()+"Error:"+NormalStyle()+" you asked for era '%s' which is not available in all of the multicrab directories!"%(era))
    if opts.variationId != None:
        for variation in opts.variationId:
            if not variation in myVariations:
                raise Exception(ErrorStyle()+"Error:"+NormalStyle()+" you asked for variation '%s' which is not available in all of the multicrab directories!"%(variation))
    # Summarise the consequences of the user choises
    myDatacardCount = len(mySelectedEras)*len(mySelectedVariations)*len(myQCDMethods)
    print "\nProducing %s%d sets of datacards%s (%d era(s) x %d variation(s) x %d QCD measurement(s))\n"%(HighlightStyle(),myDatacardCount,NormalStyle(),len(mySelectedEras),len(mySelectedVariations),len(myQCDMethods))

    # Produce datacards
    myCounter = 0
    for method in myQCDMethods:
        for module in mySelectedVariations:
            for era in mySelectedEras:
                myCounter += 1
                print CaptionStyle()+"Producing datacard %d/%d ..."%(myCounter,myDatacardCount)+NormalStyle()+"\n"
                DataCard.DataCardGenerator(config,opts,method,era,module)
    print "\nDatacard generator is done."

    #gc.collect()
    #ROOT.SetMemoryPolicy( ROOT.kMemoryHeuristics)
    #memoryDump()

def obtainErasAndModules(taskPath):
    # Initialise black list of words (if these appear in the directory name, the directory will be skipped)
    mySkipList = ["Plus","Minus","configInfo","PUWeightProducer"]
    # Initialise return objects
    myModules = []
    myEras = []
    # Check that path exists
    if not os.path.exists(taskPath):
        return myEras,myModules
    taskDirs = multicrab.getTaskDirectories(None, taskPath+"/multicrab.cfg")
    # take first non-data task and obtain its result histogram
    myRootFile = None
    myTask = ""
    for task in taskDirs:
        myBasename = os.path.basename(task)
        if myBasename.find("2011") < 0 and myBasename.find("2012") < 0: # and len(myTask) == 0:
            myTask = task
    if len(myTask) == 0:
        if len(taskDirs) == 0:
            return myEras,myModules
        myTask = taskDirs[0]
    myFilename = myTask+"/res/histograms-"+os.path.basename(myTask)+".root"
    if os.path.exists(myFilename):
        myRootFile = ROOT.TFile.Open(myFilename)
        # root file is opened, loop over keys to find directories
        for i in range(0, myRootFile.GetNkeys()):
            myKey = myRootFile.GetListOfKeys().At(i)
            if myKey.IsFolder():
                myTitle = myKey.GetTitle()
                # Ignore systematics and architecture directories
                mySkipStatus = False
                for skipItem in mySkipList:
                    if skipItem in myTitle:
                        mySkipStatus = True
                if mySkipStatus:
                    continue
                # Analyse directory name
                # Extract optimisation postfix
                myModuleName = myTitle
                if myTitle.find("Opt") > 0:
                    # Remove prefix
                    myModuleName = myModuleName[myModuleName.find("Opt"):len(myModuleName)]
                else:
                    # Fall back to default
                    myModuleName = ""
                if not myModuleName in myModules:
                    myModules.append(myModuleName)
                # Extract era
                myEraName = myTitle
                if myEraName.find("Run") > 0:
                    myEraName = myEraName[myEraName.find("Run"):len(myEraName)]
                    if myEraName.find("Opt") > 0:
                        myEraName = myEraName[0:myEraName.find("Opt")]
                else:
                    myEraName = ""
                if not myEraName in myEras:
                    myEras.append(myEraName)
        myRootFile.Close()
        return myEras,myModules
    # No root file has been found
    return myEras,myModules

# Remove eras and variations that are not possible
def checkEraAndVariationMatching(eras,variations,testEras,testVariations,label):
    myEras = []
    myVariations = []
    # Check that eras are possible
    for era in eras:
        if era in testEras:
            myEras.append(era)
        else:
            print "Not possible to evaluate era '%s', because it is missing from %s."%(era,label)
    # Check that variations are possible
    for variation in variations:
        if variation in testVariations:
            myVariations.append(variation)
        else:
            print "Not possible to evaluate era '%s', because it is missing from %s."%(era,label)
    # Return
    return myEras,myVariations

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
    print ErrorStyle()+"Error: This git branch contains old version of datacard generator. Use 2012 branch instead!"+NormalStyle()+"\n"
    sys.exit()

    parser = OptionParser(usage="Usage: %prog [options]",add_help_option=False,conflict_handler="resolve")
    parser.add_option("-h", "--help", dest="helpStatus", action="store_true", default=False, help="Show this help message and exit")
    parser.add_option("-x", "--datacard", dest="datacard", action="store", help="Name (incl. path) of the datacard to be used as an input")
    parser.add_option("-l", "--listVariations", dest="listVariations", action="store_true", default=False, help="Print a list of available variations")
    parser.add_option("-e", "--era", dest="eraId", type="string", action="append", help="Evaluate specified eras")
    parser.add_option("-v", "--variation", dest="variationId", type="int", action="append", help="Evaluate specified variations")
    parser.add_option("--showcard", dest="showDatacard", action="store_true", default=False, help="Print datacards also to screen")
    parser.add_option("--QCDfactorised", dest="useQCDfactorised", action="store_true", default=False, help="Use factorised method for QCD measurement")
    parser.add_option("--QCDinverted", dest="useQCDinverted", action="store_true", default=False, help="Use inverted method for QCD measurement")
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
    main(opts)
