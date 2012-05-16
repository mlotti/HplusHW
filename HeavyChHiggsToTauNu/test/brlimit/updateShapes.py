#!/usr/bin/env python

import ROOT
ROOT.gROOT.SetBatch(True)

def main():
    update(80)
    update(100)
    update(120)
    update(140)
    update(150)
    update(155)
    update(160)


def update(mass):
    f = ROOT.TFile.Open("lands_histograms_hplushadronic_m%d.root" % mass, "UPDATE")

#    cloneHisto(f, "QCD", 12)
#    cloneHisto(f, "EWK_Tau", 19)
    cloneHisto(f, "HH%d_1"%mass, 17)
    cloneHisto(f, "HW%d_1"%mass, 18)

    f.Close()

def cloneHisto(f, name, index):
    h = f.Get(name)
    hUp = h.Clone("%s_%dUp" % (name, index))
    hDown = h.Clone("%s_%dDown" % (name, index))

    for bin in xrange(0, h.GetNbinsX()+1):
        val = h.GetBinContent(bin)
        err = h.GetBinError(bin)
        hUp.SetBinContent(bin, val+err)
        hUp.SetBinError(bin, 0)
        hDown.SetBinContent(bin, max(val-err, 0))
        hDown.SetBinError(bin, 0)

    hUp.Write()
    hDown.Write()


if __name__ == "__main__":
    main()
