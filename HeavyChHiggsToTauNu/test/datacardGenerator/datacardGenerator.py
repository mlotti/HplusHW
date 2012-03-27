#! /usr/bin/env python

import sys

import HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.MulticrabPathFinder as PathFinder
import HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.DataCardGenerator as DataCard

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.aux import load_module
    
def usage():
    print 
    print "### Usage:   datacardGenerator.py <datacardfile>\n"
    print 
    sys.exit()

def main():

    if len(sys.argv) == 1:
        usage()

    config = load_module(sys.argv[1])

    multicrabPaths = PathFinder.MulticrabPathFinder(config)

    datacardgenerator = DataCard.DataCardGenerator(config)

    if multicrabPaths.getQCDFactorizedExists():
        datacardgenerator.generate(multicrabPaths.getQCDFactorizedPaths())

    if multicrabPaths.getQCDInvertedExists():
        datacardgenerator.generate(multicrabPaths.getQCDInvertedPaths())


if __name__ == "__main__":
    main()
