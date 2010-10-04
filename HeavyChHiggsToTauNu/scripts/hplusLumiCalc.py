#!/usr/bin/env python

import os
import sys
import glob
import subprocess
from optparse import OptionParser

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab

# lumiCalc.py usage taken from
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/LumiCalc

def main(opts, args):
    crabdirs = multicrab.getTaskDirectories(opts)

    mergedFiles = []
    for d in crabdirs:
        json = os.path.join(d, "res", "lumiSummary.json")
        print
        print "================================================================================"
        print "Dataset %s:" % d
        ret = subprocess.call(["lumiCalc.py", "-c", "frontier://LumiProd/CMS_LUMI_PROD", "-i", json, "--nowarning", "overview"])
        if ret != 0:
            print "Call to lumiCalc.py failed with return call %d" % ret
            return 1
    return 0

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]")
    multicrab.addOptions(parser)
    
    (opts, args) = parser.parse_args()

    sys.exit(main(opts, args))
