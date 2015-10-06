#!/usr/bin/env python

import os
import re

import ROOT
ROOT.gROOT.SetBatch(True)

import NtupleAnalysis.toolsdataset as dataset
import NtupleAnalysis.toolshistograms as histograms
import NtupleAnalysis.toolstdrstyle as tdrstyle
import NtupleAnalysis.toolsplots as plots
import NtupleAnalysis.toolsstyles as styles
import LimitCalc.limit as limit

nbins = 100

def main():
    # Apply TDR style
    style = tdrstyle.TDRStyle()

#    listMu("100")
#    doPlot("100", "0.07318")
#    doPlot("100", "0.04953")
#    doPlot("100", "0.06020")
#    doPlot("100", "0.08068")
#    doPlot("120", "0.06020")
#    doPlot("120", "0.04953")
    doPlot("120", "0.04075", "0.04")

def doPlot(mass, mu, mul=None):
    f = openFile(mass)
    tree_obs = f.Get("TESTED_R%s"%mu)
    if not tree_obs:
        print "Did not find TESTED_R%s TTree in file %s" % (mu, f.GetName())
        listMu(mass, f)
        f.Close()
        return

    tree_sb = f.Get("SAMPLING_SB_TESTED_R%s" % mu)
    if not tree_sb:
        raise Exception("Did not find SAMPLING_SB_TESTED_R%s from file %s" % (mu, f.GetName()))
    tree_b = f.Get("SAMPLING_B_TESTED_R%s" % mu)
    if not tree_b:
        raise Exception("Did not find SAMPLING_B_TESTED_R%s from file %s" % (mu, f.GetName()))

    xmin = min(tree_sb.GetMinimum("brT"), tree_b.GetMinimum("brT"))
    xmax = max(tree_sb.GetMaximum("brT"), tree_b.GetMaximum("brT"))
    obsval = tree_obs.GetMinimum("brT")

    # Get the distributions
    tree_sb.Draw("brT >>hsb(%d, %f, %f)" % (nbins, xmin, xmax), "", "goff")
    h_sb = tree_sb.GetHistogram()
    tree_b.Draw("brT >>hb(%d, %f, %f)" % (nbins, xmin, xmax), "", "goff")
    h_b = tree_b.GetHistogram()

    # Set obsval to bin boundary
    obsval_bin = obsval
    for bin in xrange(0, h_sb.GetNbinsX()+1):
        edge = h_sb.GetBinLowEdge(bin)
        if obsval > edge:
            obsval_bin = edge

    # Normalize the distributions to unit area
    dataset._normalizeToOne(h_sb)
    dataset._normalizeToOne(h_b)

    plot = plots.PlotBase([
            histograms.Histo(h_b, "B"),
            histograms.Histo(h_sb, "SB")
            ])
    mulegend = mul
    if mul == None:
        mulegend = mu
    plot.histoMgr.setHistoLegendLabelMany({
            "B":  "f(#tilde{q}_{#mu=%s} | #mu=0, #hat{#bf{#theta}}_{0}^{obs})" % mulegend,
            "SB": "f(#tilde{q}_{#mu=%s} | #mu=%s, #hat{#bf{#theta}}_{#mu=%s}^{obs})" % (mulegend, mulegend, mulegend),
            })
    plot.setLegend(histograms.moveLegend(histograms.createLegend(0.6, 0.8, 0.9, 0.9), dy=0.02, dx=-0.05))
    plot.histoMgr.forEachHisto(styles.generator())

    fname = "teststat_m%s_mu%s" % (mass, mu)
    plot.createFrame(fname.replace(".", "_"), opts={"ymin": 1e-6, "ymaxfactor": 2})
    plot.frame.GetXaxis().SetTitle("Test statistic #tilde{q}_{#mu}")
    plot.frame.GetYaxis().SetTitle("Arbitrary units")
    plot.getPad().SetLogy(True)

    area_sb = h_sb.Clone("AreaSB")
    area_sb.SetFillColor(area_sb.GetLineColor())
    area_sb.SetFillStyle(3005)
    area_sb.SetLineWidth(0)

    area_b = h_b.Clone("AreaB")
    area_b.SetFillColor(area_b.GetLineColor())
    area_b.SetFillStyle(3004)
    area_b.SetLineWidth(0)
    for bin in xrange(0, area_sb.GetNbinsX()+1):
        if area_sb.GetBinLowEdge(bin) < obsval_bin:
            area_sb.SetBinContent(bin, 0)
        if area_b.GetBinLowEdge(bin) >= obsval_bin:
            area_b.SetBinContent(bin, 0)

    plot.appendPlotObject(area_b, "HIST ][")
    plot.appendPlotObject(area_sb, "HIST ][")

    plot.addCutBoxAndLine(box=False, cutValue=obsval_bin)


    plot.draw()

    size = 26
    histograms.addText(0.35, 0.4, "CL_{s+b}", size=size)
    histograms.addText(0.18, 0.4, "1-CL_{b}", size=size)

    size = 20
#    x = obsval_bin/(plot.frame.GetXaxis().GetXmax() - plot.frame.GetXaxis().GetXmin())+0.02
    x = (obsval_bin - plot.getPad().GetX1()) / (plot.getPad().GetX2() - plot.getPad().GetX1())
    x += 0.01
    histograms.addText(x, 0.88, "Observed", size=size)
    histograms.addText(x, 0.85, "value", size=size)

    histograms.addText(0.62, 0.78, "m_{H^{+}} = %s %s" % (mass, limit.massUnit()), size=size)

#    size = 20
#    x = 0.2
#    histograms.addText(x, 0.88, brlimit.process, size=size)
#    histograms.addText(x, 0.84, brlimit._finalstateLabels["taujets"], size=size)
#    histograms.addText(x, 0.79, brlimit.BRassumption, size=size)

    plot.save()

    f.Close()

def openFile(mass):
    fname = os.path.join("Limit_m%s"%mass, "res", "histograms-Limit_m%s.root" % mass)
    f = ROOT.TFile.Open(fname)
    return f

def listMu(mass, openedFile=None):
    if openedFile:
        f = openedFile
    else:
        f = openFile(mass)

    tested_re = re.compile("^TESTED_R(?P<r>\d+\.\d+)$")

    content = f.GetListOfKeys()
    # Suppress the warning message of missing dictionary for some iterator
    backup = ROOT.gErrorIgnoreLevel
    ROOT.gErrorIgnoreLevel = ROOT.kError
    diriter = content.MakeIterator()
    ROOT.gErrorIgnoreLevel = backup

    muvalues = []

    key = diriter.Next()
    while key:
        name = key.GetName()
        
        m = tested_re.search(name)
        if m:
            muvalues.append(m.group("r"))

        key = diriter.Next()

    if not openedFile:
        f.Close()

    print "Available values of mu:"
    print " ".join(muvalues)


if __name__ == "__main__":
    main()
