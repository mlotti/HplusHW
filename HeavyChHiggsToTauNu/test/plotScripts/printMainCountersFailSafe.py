#!/usr/bin/env python
import sys
import ROOT
ROOT.gROOT.SetBatch(True)

import os
from optparse import OptionParser

def main(opts):
    histoname = "signalAnalysis%s/counters/weighted/counter"%opts.era[0]
    for mydir in opts.dirs:
        histos = []
        rootFile = ROOT.TFile.Open(os.path.join(mydir, "res", "histograms-%s.root"%mydir))
        if rootFile == None:
            raise Exception ("Error: File 'histograms-%s.root' not found!"%mydir)
        h = rootFile.Get(histoname)
        if h == None:
            raise Exception ("Error: histogram '%s' not found!"%histoname)
        print "\n%s\n"%(mydir)
        for i in range(1,h.GetNbinsX()):
            print h.GetXaxis().GetBinLabel(i),",",h.GetBinContent(i),",","+-",",",h.GetBinError(i)

# Call the main function if the script is executed (i.e. not imported)
if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("-d", dest="dirs", action="append", help="name of sample directory inside multicrab dir (multiple directories can be specified with multiple -d arguments)")
    parser.add_option("-v", dest="variation", action="append", help="name of variation")
    parser.add_option("-e", dest="era", action="append", help="name of era")
    (opts, args) = parser.parse_args()

    # Check that proper arguments were given
    mystatus = True
    if opts.dirs == None:
        print "Missing source for sample directories!\n"
        mystatus = False
    if opts.era == None:
        print "Missing specification for era!\n"
        mystatus = False
    if not mystatus:
        parser.print_help()
        sys.exit()

    # Arguments are ok, proceed to run
    main(opts)
