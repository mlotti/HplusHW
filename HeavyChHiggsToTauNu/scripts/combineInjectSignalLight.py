#!/usr/bin/env python

import os
import re
import math
from optparse import OptionParser

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

# Copied from TailFitter, should not import anything because has to be run on CE
# Return info of column names from datacard file
def parseColumnNames(lines):
    for l in lines:
        mySplit = l.split()
        if mySplit[0] == "process":
            return mySplit[1:]
    raise Exception("This line should never be reached")


def scaleHH(h, brtop, brh):
    h.Scale(brtop**2 * brh**2)

def scaleWH(h, brtop, brh):
    h.Scale( 2*(1-brtop)*brtop * brh )

def scaleWW(h, brtop, brh):
    h.Scale( (1-brtop)**2)


def getFromSignal(fsig, name):
    re_sig = re.compile("\d+")
    re_name = re.compile(re_sig.sub("\d+", name))
    keys = fsig.GetListOfKeys()
    for k in keys:
        m = re_name.match(k.GetName())
        if m:
            return k.ReadObj()
    raise Exception("Did not find signal histogram from file %s with regex %s" % (fsig.GetName(), re_name.pattern))

def main(opts):
    for o in ["inputDatacard", "inputRoot", "inputRootSignal"]:
        fname = getattr(opts, o)
        if not os.path.exists(fname):
            raise Exception("--%s file %s does not exist" % (o, fname))

    f = open(opts.inputDatacard)
    datacardLines = f.readlines()
    columnNames = parseColumnNames(datacardLines)
    f.close()

    f = ROOT.TFile.Open(opts.inputRoot)
    fsig = ROOT.TFile.Open(opts.inputRootSignal)
    hobs = f.Get("data_obs").Clone()
    hobs.SetDirectory(0)
    hsum = hobs.Clone("hsum")
    hsum.SetDirectory(0)
    for i in xrange(0, hsum.GetNbinsX()+2):
        hsum.SetBinContent(i, 0)
        hsum.SetBinError(i, 0)

    print "BR(t->H+) %.4f, BR(H+->tau nu) %.4f" % (opts.brtop, opts.brh)
    for name in columnNames:
        h = f.Get(name)
        tag = name[0:2]
        if tag == "HH":
            h = getFromSignal(fsig, name)
            scaleHH(h, opts.brtop, opts.brh)
        elif tag in ["HW", "WH"]:
            h = getFromSignal(fsig, name)
            scaleWH(h, opts.brtop, opts.brh)
        elif tag == "tt":
            scaleWW(h, opts.brtop, opts.brh)
        hsum.Add(h)
    fsig.Close()

    # Randomize
    if opts.toys:
        print "Using seed %d" % opts.seed
        rnd = ROOT.TRandom3()
        rnd.SetSeed(opts.seed)
        for i in xrange(1, hsum.GetNbinsX()+1):
            value = rnd.Poisson(hsum.GetBinContent(i))
            hobs.SetBinContent(i, value)
            hobs.SetBinError(i, math.sqrt(value))
    else:
        print "Not using toys, rounding bins to nearest integer"
        for i in xrange(1, hsum.GetNbinsX()+1):
            value = round(hsum.GetBinContent(i))
            hobs.SetBinContent(i, value)
            hobs.SetBinError(i, math.sqrt(value))

    # Make sure the integral is integer
    if hobs.Integral() != 0:
        hobs.Scale( ROOT.TMath.Nint(hobs.Integral()) / hobs.Integral() )

    nevents = int(hobs.Integral())
    print "Original N(events) %.2f, randomized %.2f" % (int(hsum.Integral()), int(hobs.Integral()))

    # Write result
    fout = ROOT.TFile.Open(opts.outputRoot, "RECREATE")
    keys = f.GetListOfKeys()
    for key in keys:
        if key.GetName() == "data_obs":
            hobs.SetDirectory(fout)
            hobs.Write()
            continue
        if key.GetName() == "data_obs_fineBinning":
            continue
        o = key.ReadObj()
        fout.cd()
        newo = o.Clone()
        newo.Write()
        newo.Delete()

    fout.Close()
    f.Close()

    fout = open(opts.outputDatacard, "w")
    for line in datacardLines:
        if "observation" in line:
            line = "observation    %d\n" % nevents
        fout.write(line)
    fout.close()

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("-s", dest="seed", type="int", default=12345,
                      help="Seed for random number generator")
    parser.add_option("--notoys", dest="toys", default=True, action="store_false",
                      help="Do not generate poisson toys, just plain background+signal (i.e. more or less the Asimov dataset)")
    parser.add_option("--brtop", dest="brtop", type="float", default=0.0,
                      help="BR(top -> b H+")
    parser.add_option("--brh", dest="brh", type="float", default=0.0,
                      help="BR(H+ -> tau nu")
    parser.add_option("--inputDatacard", dest="inputDatacard", type="string", default=None,
                      help="Input datacard")
    parser.add_option("--inputRoot", dest="inputRoot", type="string", default=None,
                      help="Input ROOT file")
    parser.add_option("--inputRootSignal", dest="inputRootSignal", type="string", default=None,
                      help="Input ROOT file for the signal to be injected")
    parser.add_option("--outputDatacard", dest="outputDatacard", type="string", default=None,
                      help="Output datacard")
    parser.add_option("--outputRoot", dest="outputRoot", type="string", default=None,
                      help="Output ROOT file")
    (opts, args) = parser.parse_args()

    if opts.inputDatacard is None:
        parser.error("--inputDatacard missing")
    if opts.inputRoot is None:
        parser.error("--inputRoot missing")
    if opts.inputRootSignal is None:
        parser.error("--inputRootSignal missing")
    if opts.outputDatacard is None:
        parser.error("--outputDatacard missing")
    if opts.outputRoot is None:
        parser.error("--outputRoot missing")

    main(opts)
