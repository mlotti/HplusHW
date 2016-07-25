#!/usr/bin/env python

import sys
import json
from optparse import OptionParser


def main(opts):
    lumiSum = 0

    maxLen = max([len(s) for s in opts.files])

    for fname in opts.files:
        f = open(fname)
        d = json.load(f)
        f.close()

        ls = 0
        for dataset, lumi in d.iteritems():
            ls += lumi
        if len(opts.files) > 1:
            fmt = "%%-%ds %%f pb^-1" % (maxLen+1)
            print fmt % (fname+":", ls)
        lumiSum += ls

    if len(opts.files) > 1:
        print
    print "Total integrated luminosity %f pb^-1" % lumiSum

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("-f", dest="files", type="string", action="append", default=[],
                      help="JSON files containing the luminosities (default: lumi.json)")

    (opts, args) = parser.parse_args()
    if len(opts.files) == 0:
        opts.files = ["lumi.json"]

    sys.exit(main(opts))
