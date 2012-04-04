#! /usr/bin/env python

import sys
from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.ConstantExtractor import ConstantExtractor
from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.ExtractorBase import ExtractorMode

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

    c = ConstantExtractor (mode=ExtractorMode.NUISANCE, exid="TST2", description="test", constantValue=0.123)
    c.printDebugInfo()
    

if __name__ == "__main__":
    main()
