#! /usr/bin/env python

import os
import sys
from optparse import OptionParser

import LimitCalcDatacardReader as DatacardReader
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShellStyles import *


def findDirList(directory):
    myFoundList = []
    myList = os.listdir(directory)
    for l in myList:
        myDir = os.path.join(directory,l)
        if os.path.isdir(myDir):
            if l.startswith("datacards_combine_"):
                myFoundList.append(myDir)
            else:
                myFoundList.extend(myDir)
    return myFoundList

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]",add_help_option=True,conflict_handler="resolve")
    parser.add_option("-d", "--dir", dest="directoryList", action="append", help="Print more information")
    parser.add_option("-r", dest="recursive", action="store_true", default=False, help="Recurse subdirectories")
    (opts, args) = parser.parse_args()

    dirs = opts.directoryList
    if dirs == None:
        dirs = ["."]

    
    if opts.recursive:
        allDirs = []
        for d in dirs:
            if os.path.exists(d):
                if d.startswith("datacards_combine_"):
                    allDirs.append(d)
                else:
                    allDirs.extend(findDirList(d))
            else:
                raise Exception("The directory '%s' does not exist! Check your command line parameters!"%d)
        dirs = allDirs[:]

    nTests = 0
    nMassPoints = 0
    nDirs = 0
    for d in dirs:
        (a,b) = DatacardReader.validateDatacards(d)
        nTests += a
        nMassPoints += b
        nDirs += 1

    print "\nDatacard consistency checks passed"
    print ".. checked %d datacards in %d directories"%(nMassPoints, nDirs)
    print ".. passed %d unit tests"%nTests
