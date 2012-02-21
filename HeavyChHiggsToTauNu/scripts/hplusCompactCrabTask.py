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
        # Go to task directory (in order to get the paths in the archive correctly easily)
        os.chdir(d)

        # Remove default.tgz
        tmp = os.path.join("share", "default.tgz")
        if os.path.exists(tmp):
            os.remove(tmp)

        # Create the tar archive
        tar = tarfile.open("task.tar.gz", mode="w:gz")
        files = []
        for f in ["CMSSW_*.std*", "crab_fjr_*.xml", "Submission_*"]:
            files.extend(glob.glob(os.path.join("res", f)))
        
        files.extend(["job", "log", "share"])

        #print "\n".join(files)

        for f in files:
            tar.add(f)
        tar.close()

        # Keep share/crab.cfg
        files.remove("share")
        sharefiles = glob.glob(os.path.join("share", "*"))
        sharefiles = filter(lambda x: not "crab.cfg" in x, sharefiles)
        files.extend(sharefiles)

        # Delete the files just added to the archive
        for f in files:
            if os.path.isfile(f):
                #print "rm "+f
                os.remove(f)
            elif os.path.isdir(f):
                #print "rm -fR "+f
                shutil.rmtree(f)
            else:
                print "Not removing "+f
        print "Compacted", d

        os.chdir(workdir)

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]")
    multicrab.addOptions(parser)

    (opts, args) = parser.parse_args()
    sys.exit(main(opts, args))

