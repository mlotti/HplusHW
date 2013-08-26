#!/usr/bin/env python

import re

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots

def main():
    # Apply TDR style
    style = tdrstyle.TDRStyle()
    histograms.createLegend.moveDefaults(dx=-0.1, dh=-0.15)

    doPlot(80)
    doPlot(100)
    doPlot(120)
    doPlot(140)
    doPlot(150)
    doPlot(155)
    doPlot(160)

def doPlot(mass):
    f = ROOT.TFile.Open("lands_histograms_hplushadronic_m%d.root" % mass)

    content = f.GetListOfKeys()
    # Suppress the warning message of missing dictionary for some iterator
    backup = ROOT.gErrorIgnoreLevel
    ROOT.gErrorIgnoreLevel = ROOT.kError
    diriter = content.MakeIterator()
    ROOT.gErrorIgnoreLevel = backup

    up_re = re.compile("^(?P<name>\S+)_(?P<num>\d+)Up$")

    shapes = []

    key = diriter.Next()
    while key:
        name = key.GetName()
        match = up_re.search(name)
        if match:
            shapes.append( (match.group("name"), int(match.group("num"))) )

        key = diriter.Next()

    data = f.Get("data_obs")
    plot = plots.PlotBase([histograms.Histo(data, "Data", drawStyle="HIST")])
    plot.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetLineWidth(3))
    plot.createFrame("shape_data_m%d" % mass, opts={"ymin": 0})
    plot.frame.GetXaxis().SetTitle("m_{T} (GeV)")
    plot.frame.GetYaxis().SetTitle("Rate")

    plot.draw()

    x = 0.6
    size = 20
    histograms.addText(x, 0.70, "Data %.1f" % _integral(data), size=size)
    histograms.addText(x, 0.65, "m_{H^{+}}=%d GeV" % mass, size=size)        

    plot.save()
    

    for name, num in shapes:
        up = f.Get(name+"_%dUp"%num)
        nom = f.Get(name)
        down = f.Get(name+"_%dDown"%num)
        up.SetLineColor(ROOT.kBlue)
        nom.SetLineColor(ROOT.kBlack)
        down.SetLineColor(ROOT.kRed)
        plot = plots.PlotBase([
                histograms.Histo(up, "Up %.1f"%_integral(up), drawStyle="HIST", legendStyle="l"),
                histograms.Histo(nom, "Nominal %.1f"%_integral(nom), drawStyle="HIST", legendStyle="l"),
                histograms.Histo(down, "Down %.1f"%_integral(down), drawStyle="HIST", legendStyle="l")
                ])
        plot.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetLineWidth(3))
        plot.setLegend(histograms.createLegend())
        plot.createFrame("shape_%s_syst%d_m%d" % (name, num, mass), opts={"ymin": 0})
        plot.frame.GetXaxis().SetTitle("m_{T} (GeV)")
        plot.frame.GetYaxis().SetTitle("Rate")

        plot.draw()

        histograms.addText(x, 0.70, "Sample %s" % name, size=size)
        histograms.addText(x, 0.65, "Nuisance %d" % num, size=size)
        histograms.addText(x, 0.60, "m_{H^{+}}=%d GeV" % mass, size=size)        

        plot.save()


    f.Close()

def _integral(h):
    return h.Integral()
    #    return h.Integral(0, h.GetNbinsX()+1)

if __name__ == "__main__":
    main()
