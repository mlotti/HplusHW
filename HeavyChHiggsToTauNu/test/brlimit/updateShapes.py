#!/usr/bin/env python

import ROOT
ROOT.gROOT.SetBatch(True)

def main():
#    update(80)
#    update(100)
#    update(120)
#    update(140)
#    update(150)
    update(155)
#    update(160)

def update(mass):
    f = ROOT.TFile.Open("lands_histograms_hplushadronic_m%d.root" % mass, "UPDATE")

#    cloneHisto(f, "QCD", 12)
#    cloneHisto(f, "EWK_Tau", 19)
#    cloneHisto(f, "HH%d_1"%mass, 17)
#    cloneHisto(f, "HW%d_1"%mass, 18)

    alterHisto(f, "HH%d_1"%mass, 7)
    alterHisto(f, "HW%d_1"%mass, 7)

    f.Close()

# for shapeStat
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

# Set variations by hand
def alterHisto(f, name, index):
    h = f.Get(name)
    hUp = f.Get(name+"_%dUp" % index)
    hDown = f.Get(name+"_%dDown" % index)

    bins = range(6, 10)
    varyUp = 1.1
    varyDown = 0.9

    for bin in bins:
        print "Modifying bin %d, low edge %.0f" % (bin, h.GetBinLowEdge(bin))
        nominal = h.GetBinContent(bin)
        if hUp.GetBinContent(bin) > nominal:
            hUp.SetBinContent(bin, nominal* varyUp)
            hDown.SetBinContent(bin, nominal* varyDown)
        else:
            hUp.SetBinContent(bin, nominal* varyDown)
            hDown.SetBinContent(bin, nominal* varyUp)

    hUp.Write(hUp.GetName(), ROOT.TObject.kWriteDelete)
    hDown.Write(hDown.GetName(), ROOT.TObject.kWriteDelete)


if __name__ == "__main__":
    main()
