#!/usr/bin/env python

import os
import sys
import glob
import shutil
import tarfile
import subprocess
from optparse import OptionParser

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab

def main(opts, args):
    workdir = os.getcwd()

    crabdirs = multicrab.getTaskDirectories(opts)
    for d in crabdirs:
        # Run crab -report
        if opts.report:
            multicrab.checkCrabInPath()
            cmd = ["crab", "-report", "-c", d]
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            output = p.communicate()[0]
            ret = p.returncode
            if ret != 0:
                print "Call to 'crab -report -d %s' failed with return value %d" % (d, ret)
                print output
                return 1

        if os.path.exists(os.path.join(d, "task.tar.gz")):
            print "Skipping %s, task.tar.gz already exists" % d
            continue

        # Go to task directory (in order to get the paths in the archive correctly easily)
        os.chdir(d)

        # Remove default.tgz
        tmp = os.path.join("share", "default.tgz")
        if os.path.exists(tmp):
            os.remove(tmp)

        # Create the tar archive
        tar = tarfile.open("task.tar.gz", mode="w:gz")
        files = []
        for f in ["CMSSW_*.std*", "crab_fjr_*.xml", "Submission_*", "Watchdog_*.log*"]:
            files.extend(glob.glob(os.path.join("res", f)))
        
        files.extend(["job", "log", "share"])

        #print "\n".join(files)

        for f in files:
            if os.path.exists(f):
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
                try:
                    os.remove(f)
                except OSError, e:
                    print "Warning: failed to remove %s: %s" % (f, str(e))
            elif os.path.isdir(f):
                #print "rm -fR "+f
                try:
                    shutil.rmtree(f)
                except OSError, e:
                    print "Warning: failed to remove %s: %s" % (f, str(e))
            else:
                print "Not removing "+f
        print "Compacted", d

        os.chdir(workdir)

    return 0

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options] [crab task dirs]\n\nCRAB task directories can be given either as the last arguments, or with -d.")
    multicrab.addOptions(parser)
    parser.add_option("--noreport", dest="report", action="store_false", default=True,
                      help="Do not run 'crab -report'.")

    (opts, args) = parser.parse_args()
    opts.dirs.extend(args)
    sys.exit(main(opts, args))

