#! /usr/bin/env python

import sys
import HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.DataCardGenerator as DataCard
    
def usage():
    print 
    print "### Usage:   datacardGenerator.py <datacardfile>\n"
    print 
    sys.exit()

def main():

    if len(sys.argv) == 1:
        usage()

    datacardgenerator = DataCard.DataCardGenerator(sys.argv[1])
    datacardgenerator.generate()

if __name__ == "__main__":
    main()
