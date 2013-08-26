#!/usr/bin/env python

import os
import sys
from optparse import OptionParser

import ROOT
ROOT.gROOT.SetBatch(True)


def main(opts, files):
    format = "  %-40s -> %s"
    for f in files:
        if not os.path.exists(f):
            raise Exception("File %s doens't exist!" % f)

        print "File %s, tree %s" % (f, opts.tree)
        print format % ("Alias", "Branch")

        backup = ROOT.gErrorIgnoreLevel
        ROOT.gErrorIgnoreLevel = ROOT.kError
        tf = ROOT.TFile.Open(f)
        ROOT.gErrorIgnoreLevel = backup

        tree = tf.Get(opts.tree)
        aliases = [(tn.GetName(), tn.GetTitle()) for tn in tree.GetListOfAliases()]
        aliases.sort()
        for (alias, branch) in aliases:
            print format % (alias, branch)
        tf.Close()

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options] file1 [file2 ...]")
    parser.add_option("-t", "--tree", dest="tree", default="Events",
                      help="Name of tree to use (default: 'Events')")
    (opts, args) = parser.parse_args()
    if len(args) == 0:
        parser.error("At least one file required")
    main(opts, args)
