#!/usr/bin/env python

import os
import sys
from optparse import OptionParser

import ROOT
ROOT.gROOT.SetBatch(True)


def main(opts, f):
    backup = ROOT.gErrorIgnoreLevel
    ROOT.gErrorIgnoreLevel = ROOT.kError
    tf = ROOT.TFile.Open(f)
    ROOT.gErrorIgnoreLevel = backup

    named = tf.Get("%s/parameterSet" % opts.directory)
    print named.GetTitle()

    tf.Close()

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options] file1")
    parser.add_option("-d", "--directory", dest="directory", default="signalAnalysis",
                      help="Directory to look for parameterSet TNamed (default: 'signalAnalysis')")
    (opts, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("Exacly one file required (got %d)"%len(args))
    main(opts, args[0])
