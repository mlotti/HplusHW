#!/usr/bin/env python

import os
import sys
import glob
import shutil
import tarfile
from optparse import OptionParser

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab

def main(opts, args):
    workdir = os.getcwd()

    crabdirs = multicrab.getTaskDirectories(opts)
    for d in crabdirs:
        print "Making export pack of %s"%d

        # Create the tar archive
        filename = "%s_export.tgz"%d
        tar = tarfile.open(filename, mode="w:gz")

        # Check if everything is ok
        if not os.path.exists(d+"/lumi.json"):
            print "... Could not find lumi.json, if you wish to include it, run hplusLumiCalc.py"
	else:
            tar.add("%s/lumi.json"%d)
        for f in ["%s/*py"%d, "%s/*cfg"%d, "%s/*/res/histograms-*root"%d]:
            list = glob.glob(f)
            for i in list:
                print "  adding file ",i
                tar.add(i)
        tar.close()
        print "Written file %s"%filename

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options] [crab task dirs]\n\nCRAB task directories can be given either as the last arguments.")
    multicrab.addOptions(parser)

    (opts, args) = parser.parse_args()
    opts.dirs.extend(args)
    sys.exit(main(opts, args))

