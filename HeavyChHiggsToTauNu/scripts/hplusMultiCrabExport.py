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
        taroptions = "w:gz"
        if opts.fullStatus:
            filename = "%s_export_unmerged.tar"%d
            taroptions = "w:"
        tar = tarfile.open(filename, mode="%s"%taroptions)

        # Check if everything is ok
        if not os.path.exists(d+"/lumi.json"):
            print "... Could not find lumi.json, if you wish to include it, run hplusLumiCalc.py"
	else:
            print "  adding file %s/lumi.json"%d
            tar.add("%s/lumi.json"%d)
        if not os.path.exists(d+"/timeReport.txt"):
            print "... Could not find timeReport.txt, if you wish to include it run hplusMultiCrabAnalysis --time >! timeReport.txt"
        else:
            print " adding timeReport.txt"
            tar.add("%s/timeReport.txt"%d)

        if os.path.exists(d+"/codeDiff.txt"):
            tar.add("%s/codeDiff.txt"%d)
        if os.path.exists(d+"/codeStatus.txt"):
            tar.add("%s/codeStatus.txt"%d)
        if os.path.exists(d+"/codeVersion.txt"):
            tar.add("%s/codeVersion.txt"%d)
        for jobdir in glob.glob(d+"/*/job"):
            tar.add(jobdir) 

        if opts.fullStatus:
            for f in ["%s/*py"%d, "%s/*cfg"%d, "%s/*/res/histograms_*root"%d]:
                list = glob.glob(f)
                for i in list:
                    print "  adding file ",i
                    tar.add(i)
        else:
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
    parser.add_option("--full", dest="fullStatus", action="store_true", default=False, help="Store non-merged root files")

    (opts, args) = parser.parse_args()
    opts.dirs.extend(args)
    sys.exit(main(opts, args))

