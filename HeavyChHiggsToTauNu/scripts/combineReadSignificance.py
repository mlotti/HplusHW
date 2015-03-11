#!/usr/bin/env python

import os
import sys
import json
from optparse import OptionParser


import HiggsAnalysis.HeavyChHiggsToTauNu.tools.CombineTools as combine

def main(opts):
    data = combine.parseSignificanceOutput(opts.mass, outputFileName=opts.file)

    content = {}
    if not opts.truncate and os.path.exists(opts.output):
        f = open(opts.output)
        content = json.load(f)
        f.close()

    content["expectedSignalBrLimit"] = combine.lhcFreqSignificanceExpectedSignalBrLimit
    content["expectedSignalSigmaBr"] = combine.lhcFreqSignificanceExpectedSignalSigmaBr

    content[opts.mass] = data

    f = open(opts.output, "w")
    json.dump(content, f, sort_keys=True, indent=2)
    f.close()        

    return 0

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("-f", dest="file", default=None,
                      help="Path to combine significance output file")
    parser.add_option("-m", dest="mass", default=None,
                      help="H+ mass point")
    parser.add_option("-o", dest="output", default=None,
                      help="Output JSON file name (by default the mass point information is updated, see --truncate")
    parser.add_option("--truncate", dest="truncate", default=False, action="store_true",
                      help="Truncate the output JSON file")

    (opts, args) = parser.parse_args()

    if opts.file is None:
        parser.error("-f is missing")
    if opts.mass is None:
        parser.error("-m is missing")
    if opts.output is None:
        parser.error("-o is missing")

    sys.exit(main(opts))
