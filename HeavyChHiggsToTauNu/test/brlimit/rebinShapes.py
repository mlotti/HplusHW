#!/usr/bin/env python

import array

import ROOT
ROOT.gROOT.SetBatch(True)

rebin = 2
rebin = range(0, 200, 20) + [200, 400]

def main():
    print "Rebinning with", rebin

    update(80)
    update(100)
    update(120)
    update(140)
    update(150)
    update(155)
    update(160)

def update(mass):
    f = ROOT.TFile.Open("lands_histograms_hplushadronic_m%d.root" % mass, "UPDATE")

    content = f.GetListOfKeys()
    # Suppress the warning message of missing dictionary for some iterator
    backup = ROOT.gErrorIgnoreLevel
    ROOT.gErrorIgnoreLevel = ROOT.kError
    diriter = content.MakeIterator()
    ROOT.gErrorIgnoreLevel = backup

    key = diriter.Next()
    while key:
        process(key.ReadObj(), rebin)
        key = diriter.Next()

    f.Close()
    print "Processed mass point %d" % mass

def process(histo, rebin):
    # Protection against extra content
    if isinstance(histo, ROOT.TH2):
        return
    if isinstance(rebin, list):
        h = histo.Rebin(len(rebin)-1, histo.GetName(), array.array("d", rebin))
    else:
        h = histo.Rebin(rebin)
    if h:
        h.Write(histo.GetName(), ROOT.TObject.kWriteDelete)

if __name__ == "__main__":
    main()
