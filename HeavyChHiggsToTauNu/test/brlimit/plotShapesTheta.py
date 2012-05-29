#!/usr/bin/env python

import re

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots

def main():
    # Apply TDR style
    style = tdrstyle.TDRStyle()
    histograms.createLegend.moveDefaults(dx=-0.1, dh=-0.15)

#    thetas = [0, 0.5, 1, 1.5]
    thetas = [0, -0.5, -1, -1.5]
#    thetas = [0, 1, -1]

#    doPlot(80)
#    doPlot(100)
#    doPlot(120)
#    doPlot(140)
    doPlot(150, "HW150_1", 7, thetas)
    doPlot(155, "HW155_1", 7, thetas)
    doPlot(160, "HW160_1", 7, thetas)

def doPlot(mass, name, nuisance, thetas):
    f = ROOT.TFile.Open("lands_histograms_hplushadronic_m%d.root" % mass)

    h = f.Get(name)
    hUp = f.Get("%s_%dUp" % (name, nuisance))
    hDown = f.Get("%s_%dDown" % (name, nuisance))

    shapes = []
    ll = {}
    for i, theta in enumerate(thetas):
        morphed = doShape(h, hUp, hDown, theta)
        shapes.append(histograms.Histo(morphed, "Theta%d" % i, drawStyle="HIST", legendStyle="l"))
        ll["Theta%d" % i] = "#theta=%.2f (%.1f)" % (theta, _integral(morphed))

    plot = plots.PlotBase(shapes)
    plot.histoMgr.forEachHisto(styles.generator())
    plot.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetLineWidth(3))
    plot.histoMgr.setHistoLegendLabelMany(ll)
    plot.setLegend(histograms.createLegend())
    
    plot.createFrame("shape_theta_%s_syst%d_m%d" % (name, nuisance, mass))
    plot.frame.GetXaxis().SetTitle("m_{T} (GeV)")
    plot.frame.GetYaxis().SetTitle("Rate")

    plot.draw()

    x = 0.6
    size = 20
    histograms.addText(x, 0.70, "Sample %s" % name, size=size)
    histograms.addText(x, 0.65, "Nuisance %d" % nuisance, size=size)
    histograms.addText(x, 0.60, "m_{H^{+}}=%d GeV" % mass, size=size)        

    plot.save()

    f.Close()

def _integral(h):
    return h.Integral()
    #    return h.Integral(0, h.GetNbinsX()+1)

def doShape(h, hUp, hDown, theta):
    ret = h.Clone(h.GetName()+"_cloned")

    for bin in xrange(1, h.GetNbinsX()+1):
        ret.SetBinContent(bin, shapeQ(h.GetBinContent(bin), hUp.GetBinContent(bin), hDown.GetBinContent(bin), theta))

    return ret

def shapeQ(nominal, up, down, theta):
    if abs(theta) < 1:
        a = theta*(theta+1)/2
        b = -theta*theta
        c = theta*(theta-1)/2
    else:
        a = max(theta, 0)
        b = -abs(theta)
        c = max(-theta, 0)

    return nominal + (a*up + b*nominal + c*down)

if __name__ == "__main__":
    main()
