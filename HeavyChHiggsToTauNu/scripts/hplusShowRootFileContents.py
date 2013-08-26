#!/usr/bin/env python

import os, sys
import ROOT
from optparse import OptionParser

def showSubdirectoryContents(directory, path, level):
    if opts.treelevel and level <= 0:
        print "Directory "+path
    myTotalCount = 0
    # Loop over keys in file
    for i in range(0, directory.GetNkeys()):
        myKey = directory.GetListOfKeys().At(i)
        # Check if key is a folder
        if myKey.IsFolder():
            mySubpath = path+myKey.GetTitle()+"/"
            mySubdir = directory.GetDirectory(mySubpath)
            myTotalCount += showSubdirectoryContents(mySubdir, mySubpath, level+1)
        else:
            myTotalCount += myKey.GetNbytes()
            if opts.treelevel and level <= 0:
                print "  %.3f kB %s %s"%(float(myKey.GetNbytes()) / 1024.0, myKey.GetClassName(), myKey.GetName())
    if opts.treelevel and level <= 1:
        print "%.3f k (total of directory %s)\n"%(float(myTotalCount) / 1024.0, path)
    return myTotalCount

def showRootFileContents(opts):
    for filename in opts.filename:
        # Open file
        myFile = ROOT.TFile.Open(filename)
        if myFile.IsZombie():
            print "Error opening file",myFilename
            sys.exit()
        mySubDir = myFile.GetDirectory("/")
        myTotalCount = showSubdirectoryContents(mySubDir, "/", 0)
        print "\n%.3f kB (File total size)\n"%(float(myTotalCount) / 1024.0)

if __name__ == "__main__" :
    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("-i", dest="filename", action="append", help="name of root file")
    parser.add_option("--treelevel", dest="treelevel", action="store_true", default=False, help="Do not enter directories")
    (opts, args) = parser.parse_args()

    # Check that proper arguments were given
    mystatus = True
    if opts.filename == None:
        print "Missing source for multicrab directories (--mdir)!\n"
        mystatus = False
    if not mystatus:
        parser.print_help()
        sys.exit()

    # Arguments are ok, proceed to run
    showRootFileContents(opts)
