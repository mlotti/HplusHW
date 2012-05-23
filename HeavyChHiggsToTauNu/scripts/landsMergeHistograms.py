#!/usr/bin/env python

import sys
import json
import subprocess
from optparse import OptionParser

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.LandSTools as lands

def main(opts, args):
    # Merge the LandS root files
    print "Merging job ROOT files"
    f = open("configuration.json")
    config = json.load(f)
    f.close()

    # forward parameters
    if opts.delete:
        args.append("--delete")
    if len(opts.filter) > 0:
        args.extend(["--filter", opts.filter])
    for d in opts.dirs:
        args.extend(["-d", d])

    if config["clsType"] == "LEP":
        command = ["hplusMergeHistograms.py", "-i", "split\S+_limits_tree\S*\.root"]+args
    elif config["clsType"] == "LHC":
        command = ["hplusMergeHistograms.py", "-i", "split\S+_m2lnQ\S*\.root"]+args
    else:
        raise Exception("Unsupported clsType '%s' in configuration.json" % config["clsType"])
    if not opts.skipMerge:
        ret = subprocess.call(command)
        if ret != 0:
            raise Exception("hplusMergeHistograms failed with exit code %d, command was\n%s" %(ret, " ".join(command)))

    # Run LandS to do obtain the results
    print "Running LandS for merged expected results"
    result = lands.ParseLandsOutput(".")
    result.print2()
    result.saveJson()

    return 0

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options] -- [options to hplusMergeHistograms]")
    multicrab.addOptions(parser)
    parser.add_option("--skipMerge", dest="skipMerge", default=False, action="store_true",
                      help="Don't run hplusMergeHistograms (i.e. run only LandS for the merged output)")
    parser.add_option("--delete", dest="delete", default=False, action="store_true",
                      help="Delete the source files to save disk space (default is to keep the files)")

    (opts, args) = parser.parse_args()

    sys.exit(main(opts, args))
