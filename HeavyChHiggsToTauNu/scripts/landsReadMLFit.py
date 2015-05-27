#!/usr/bin/env python

import os
import sys
import json
from optparse import OptionParser


import HiggsAnalysis.HeavyChHiggsToTauNu.tools.LandSTools as lands

def main(opts):
    bkg = lands.parseLandsMLOutput(opts.bkg)
    sbkg = lands.parseLandsMLOutput(opts.signal)

    content = {}
    if not opts.truncate and os.path.exists(opts.output):
        f = open(opts.output)
        content = json.load(f)
        f.close()

    content[opts.mass] = {
        "background": bkg,
        "signal+background": sbkg,
    }

    f = open(opts.output, "w")
    json.dump(content, f, sort_keys=True, indent=2)
    f.close()        

    return 0

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("-b", dest="bkg", default=None,
                      help="File with output of background-only fit")
    parser.add_option("-s", dest="signal", default=None,
                      help="File with output of signal+background fit")
    parser.add_option("-m", dest="mass", default=None,
                      help="H+ mass point")
    parser.add_option("-o", dest="output", default=None,
                      help="Output JSON file name (by default the mass point information is updated, see --truncate")
    parser.add_option("--truncate", dest="truncate", default=False, action="store_true",
                      help="Truncate the output JSON file")

    (opts, args) = parser.parse_args()

    if opts.bkg is None:
        parser.error("-b is missing")
    if opts.signal is None:
        parser.error("-s is missing")
    if opts.mass is None:
        parser.error("-m is missing")
    if opts.output is None:
        parser.error("-o is missing")

    sys.exit(main(opts))
