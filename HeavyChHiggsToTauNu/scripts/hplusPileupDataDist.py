#!/usr/bin/env python

# https://twiki.cern.ch/twiki/bin/view/CMS/PileupReweighting
# https://twiki.cern.ch/twiki/bin/view/CMS/LumiCalc#How_to_use_script_estimatePileup

# estimatePileup.py --saveRuns --nowarning -i foo.txt --maxPileupBin 50 pileup.root

import sys
from optparse import OptionParser

import ROOT
ROOT.gROOT.SetBatch(True)

#print len([0.0698146584,0.0698146584,0.0698146584,0.0698146584,0.0698146584,0.0698146584,0.0698146584,0.0698146584,0.0698146584,0.0698146584,0.0698146584,0.0630151648,0.0526654164,0.0402754482,0.0292988928,0.0194384503,0.0122016783,0.007207042,0.004003637,0.0020278322,0.0010739954,0.0004595759,0.0002229748,0.0001028162,4.58337152809607E-05])

def main(opts):
    f = ROOT.TFile.Open(opts.file)
    histo = f.Get("pileup")

    n = opts.max
    if n < 0:
        n = histo.GetNbinsX()

    npu_data = []
    for npu in xrange(0, n):
        npu_data.append(histo.GetBinContent(histo.GetXaxis().FindBin(npu)))

    print "dataDist = cms.vdouble(%s)" % ", ".join(["%.8f" % x for x in npu_data])

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("-f", dest="file", type="string",
                      help="Input ROOT file produced with estimatePileup.py")
    parser.add_option("-n", dest="max", default=25,
                      help="Print distibution up to N PU interactions (default: 25, i.e. Summer1; use -1 for all )")

    (opts, args) = parser.parse_args()
    sys.exit(main(opts))
