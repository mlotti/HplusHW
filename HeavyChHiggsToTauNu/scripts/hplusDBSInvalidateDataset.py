#!/usr/bin/env python

import sys
import subprocess

from optparse import OptionParser

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrabDatasetsCommon as common

def main(opts, args):
    for dataset in args:
        #print "Invalidating %s" % dataset
        cmd = ["DBSInvalidateDataset.py", "--DBSURL", opts.dbsurl, "--files", "-d", dataset]
        if opts.test:
            print " ".join(cmd)
            continue

        ret = subprocess.call(cmd)
        if ret != 0:
            print "Command '%s' failed, exiting" % " ".join(cmd)
            return 1

    return 0

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("--DBSURL", dest="dbsurl", default=common.pattuple_dbs_writer,
                      help="DBS writer URL (default: %s)" % common.pattuple_dbs_writer)
    parser.add_option("--test", dest="test", default=False, action="store_true",
                      help="Just test, don't actually invalidate")


    (opts, args) = parser.parse_args()
    sys.exit(main(opts, args))
