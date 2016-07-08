#!/usr/bin/env python

import subprocess
import shutil
import time
import sys
import os
import re
from optparse import OptionParser
import ConfigParser
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.aux as aux

def isInRange(opts, j):
    if opts.firstJob >= 0 and j.id < opts.firstJob:
        return False
    if opts.lastJob >= 0 and j.id > opts.lastJob:
        return False
    return True

def main(opts):
    for d in opts.dirs:
        myDir = "%s/res"%d
        if not os.path.exists(myDir):
            raise Exception("Error: Directory '%s' does not exist!"%myDir)
        os.chdir(myDir)
        # Build list of files
        myJobList = []
        # Obtain job numbers with existing output
        for dirname, dirnames, filenames in os.walk("."):
            for fname in filenames:
                if "histograms_" in fname:
                    mySplit = fname.split("_")
                    myNumber = int(mySplit[1])
                    if not myNumber in myJobList:
                        myJobList.append(myNumber)
        # Obtain packs of timed out jobs
        for dirname, dirnames, filenames in os.walk("."):
            for fname in filenames:
		if "out_files_" in fname:
		    mySplit = fname.split("_")
                    myNumber = int(mySplit[2].replace(".tgz",""))
                    if not myNumber in myJobList:
                        print "Recovering and unpacking output of job",myNumber
                        os.system("cp %s ."%os.path.join(dirname,fname))
                        os.system("tar xfz %s"%fname)
                        os.system("rm %s"%fname)
			myJobList.append(myNumber)
        # Look at job list
        myJobList.sort()
        i = 1
        l = 1
        s = "%d"%i
        for k in range(1,len(myJobList)):
            n = myJobList[k]
            if not n == i+1:
                if l > 1:
                    s += "-%d,"%myJobList[k-1]
                else:
                    s += ","
                s += "%d"%n
                l = 1
            else:
                l += 1
            i = n
        if l > 1:
            s += "-%d"%myJobList[len(myJobList)-1]
        else:
            s += ",%d"%myJobList[len(myJobList)-1]
        print "Task %s has histograms for jobs: %s"%(d,s)
    return 0

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options] [crab task dirs]\n\nCRAB task directories can be given either as the last arguments, or with -d.")
    #multicrab.addOptions(parser)
    parser.add_option("-d", dest="dirs", action="append",
                      help="Define task directories to be considered")
    (opts, args) = parser.parse_args()
    #opts.dirs.extend(args)

    sys.exit(main(opts))

