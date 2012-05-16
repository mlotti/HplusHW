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

    # Produce cards
    for method in myQCDMethods:
        DataCard.DataCardGenerator(config,opts,method)

    print "\nDatacard generator is done."

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
    if not myStatus:
        parser.print_help()
        sys.exit()
    # Run main program
    main(opts)
