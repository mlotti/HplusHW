#!/usr/bin/env python

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.LandSTools import *

def main():

    if len(sys.argv) == 1:
        print "\n"
        print "### Usage:   test.py <multicrabdir>\n"
        print "\n"
        sys.exit()

    path = sys.argv[1]
    if path[len(path)-1] != '/':
        path += "/"

    result = ParseLandsOutput(path)
    result.Print()
    result.Save("outputs")

if __name__ == "__main__":
    main()
