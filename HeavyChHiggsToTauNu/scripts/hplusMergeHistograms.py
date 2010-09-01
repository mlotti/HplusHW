#!/usr/bin/env python

import os
import sys
import glob
import subprocess
import ConfigParser
from optparse import OptionParser

def main(opts, args):

    crabdirs = []
    if len(opts.dirs) == 0:
        mc_ignore = ["MULTICRAB", "COMMON"]
        mc_parser = ConfigParser.ConfigParser()
        mc_parser.read("multicrab.cfg")

        sections = mc_parser.sections()

        for i in mc_ignore:
            sections.remove(i)

        crabdirs = sections
    else:
        crabdirs = opts.dirs

    mergedFiles = []
    for d in crabdirs:
        files = glob.glob(os.path.join(d, "res", opts.input))
        if len(files) == 0:
            continue

        mergeName = os.path.join(d, "res", opts.output % d)
        #cmd = "mergeTFileServiceHistograms -o %s -i %s" % ("histograms-"+d+".root", " ".join(files))
        #print files
        #ret = subprocess.call(["mergeTFileServiceHistograms",
        #                       "-o", mergeName,
        #                       "-i"]+files)
        ret = subprocess.call(["hadd", mergeName]+files) 
        if ret != 0:
            print "Merging failed with exit code %d" % ret
            return 1
        mergedFiles.append(mergeName)

    print "Merged histogram files:"
    for f in mergedFiles:
        print "  %s" % f

    return 0

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("--dir", "-d", dest="dirs", type="string", action="append", default=[],
                      help="CRAB task directory to have the files to merge (default: read multicrab.cfg and use the sections in it)")
    parser.add_option("-i", dest="input", type="string", default="histograms_*.root",
                      help="Pattern for input root files (note: remember to escape * and ? !) (default: 'histograms_*.root')")
    parser.add_option("-o", dest="output", type="string", default="histograms-%s.root",
                      help="Pattern for merged output root files (use '%s' for crab directory name) (default: 'histograms-%s.root')")
    
    (opts, args) = parser.parse_args()

    sys.exit(main(opts, args))
