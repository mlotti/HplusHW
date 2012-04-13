#! /usr/bin/env python

import os
import sys
import imp
from optparse import OptionParser

import HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.MulticrabPathFinder as PathFinder
import HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.DataCardGenerator as DataCard
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.aux import load_module


def main(opts):
    print "Loading datacard:", opts.datacard
    config = load_module(opts.datacard)
    #multicrabPaths = PathFinder.MulticrabPathFinder(config) #FIXME ??? it takes a path, not a config as input
    
    datacardgenerator = DataCard.DataCardGenerator(config)

    #if multicrabPaths.getQCDFactorizedExists():
    #    datacardgenerator.generate(multicrabPaths.getQCDFactorizedPaths())

    #if multicrabPaths.getQCDInvertedExists():
    #    datacardgenerator.generate(multicrabPaths.getQCDInvertedPaths())
    
    #datacardgenerator = DataCard.DataCardGenerator()
    datacardgenerator.generate()

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("-x", "--datacard", dest="datacard", action="store", help="Name (incl. path) of the datacard to be used as an input")
    parser.add_option("--debugConfig", dest="debugConfig", action="store_true", default=False, help="Enable debugging print for config parsing")
    parser.add_option("--debugMining", dest="debugMining", action="store_true", default=False, help="Enable debugging print for data mining")
    parser.add_option("--debugQCD", dest="debugQCD", action="store_true", default=False, help="Enable debugging print for QCD measurement")
    (opts, args) = parser.parse_args()
    
    myStatus = True
    if opts.datacard == None:
        print "Missing datacard!\n"
        myStatus = False
    if not myStatus:
        parser.print_help()
        sys.exit()
 
    # Run main program
    main(opts)
