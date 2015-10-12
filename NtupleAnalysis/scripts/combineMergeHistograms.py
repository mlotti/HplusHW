#!/usr/bin/env python

import os
import sys
import json
import subprocess
from optparse import OptionParser

import HiggsAnalysis.NtupleAnalysis.tools.multicrab as multicrab
import HiggsAnalysis.NtupleAnalysis.tools.LandSTools as lands
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux

def main(opts, args):
    # Merge the combine root files
    f = open("configuration.json")
    config = json.load(f)
    f.close()

    # forward parameters
    if opts.delete:
        args.append("--delete")

    if "clsConfig" in config and "signalInjection" in config["clsConfig"]:
        command = ["hplusMergeHistograms.py", "-i", "higgsCombineinj.*\.root"]+args
    else:
        raise Exception("According to configuration.json, this is not signal injection job. Nothing for combineMergeHistograms.py to do")
    print "Merging job ROOT files"
    ret = subprocess.call(command)
    if ret != 0:
        raise Exception("hplusMergeHistograms failed with exit code %d, command was\n%s" %(ret, " ".join(command)))

    return 0

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options] -- [options to hplusMergeHistograms]")
    multicrab.addOptions(parser)
    parser.add_option("--delete", dest="delete", default=False, action="store_true",
                      help="Delete the source files to save disk space (default is to keep the files)")

    (opts, args) = parser.parse_args()

    sys.exit(main(opts, args))
