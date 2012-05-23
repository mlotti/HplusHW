#!/usr/bin/env python

import sys
import json
import array

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots

import plotBRLimit as brlimit
import mkBrLimits_processTanbPlots as tanb

tanbMax = 60
mu = 200
forPaper = False
#forPaper = True

unit = "GeV/c^{2}"
if forPaper:
    unit = "GeV"

def main():
    limits = brlimit.BRLimits()

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    if forPaper:
        histograms.cmsTextMode = histograms.CMSMode.PAPER

    # Get BR limits
    graphs = {}
    obs = limits.observedGraph()
    graphs["obs"] = obs
    graphs["exp"] = limits.expectedGraph()
    graphs["exp1"] = limits.expectedBandGraph(sigma=1)
    graphs["exp2"] = limits.expectedBandGraph(sigma=2)

    # Remove m=80
    for gr in graphs.values():
        tanb.cleanGraph(gr, minX=100)

    # Get theory uncertainties on observed
    obs_th_plus = tanb.getObservedPlus(obs);   obs_th_plus.SetName("ObservedTheoryPlus")
    obs_th_minus = tanb.getObservedMinus(obs); obs_th_minus.SetName("ObservedTheoryMinus")
    for gr in [obs_th_plus, obs_th_minus]:
        gr.SetLineWidth(3)
        gr.SetLineStyle(5)
#        gr.SetLineStyle(9)
    graphs["obs_th_plus"] = obs_th_plus
    graphs["obs_th_minus"] = obs_th_minus

    # Interpret in MSSM
    mu = 200

    for key in graphs.keys():
        removeNotValid = not (key in ["exp1", "exp2"])
        graphs[key] = tanb.graphToTanBeta(graphs[key], mu, removeNotValid)

    doPlot("limitsTanb_mh", graphs, limits, "m_{H^{+}} (%s)"%unit)
    
    for gr in graphs.values():
        tanb.graphToMa(gr)

    doPlot("limitsTanb_ma", graphs, limits, "m_{A} (%s)"%unit)


    # Mu variations
    mus = [1000, 200, -200, -1000]
    muGraphs = [(tanb.graphToTanBeta(obs, m), m) for m in mus]

    def muStyle(h, markerStyle, lineStyle, color):
        rh = h.getRootHisto()
        rh.SetMarkerStyle(markerStyle)
        rh.SetMarkerColor(color)
        rh.SetLineStyle(lineStyle)
        rh.SetLineColor(color)
        rh.SetLineWidth(504)
        rh.SetFillStyle(3005)

    st = [lambda h: muStyle(h, 21, 1, 4),
          lambda h: muStyle(h, 20, 1, 1),
          lambda h: muStyle(h, 20, 2, 1),
          lambda h: muStyle(h, 21, 2, 4)]
    doPlotMu("limitsTanb_mus_mh", muGraphs, st, limits, "m_{H^{+}} (%s)"%unit)

    for gr, mu in muGraphs:
        tanb.graphToMa(gr)
    doPlotMu("limitsTanb_mus_ma", muGraphs, st, limits, "m_{A} (%s)"%unit)

def doPlot(name, graphs, limits, xlabel):
    obs = graphs["obs"]
    excluded = ROOT.TGraph(obs)
    excluded.SetName("ExcludedArea")
    excluded.SetFillColor(ROOT.kGray)
    excluded.SetPoint(excluded.GetN(), obs.GetX()[obs.GetN()-1], tanbMax)
    excluded.SetPoint(excluded.GetN(), obs.GetX()[0], tanbMax)
    excluded.SetFillColor(ROOT.kGray)
    excluded.SetFillStyle(3354)
    excluded.SetLineWidth(0)
    excluded.SetLineColor(ROOT.kWhite)

    plot = plots.PlotBase([
            histograms.HistoGraph(graphs["obs"], "Observed", drawStyle="PL", legendStyle="lp"),
            histograms.HistoGraph(graphs["obs_th_plus"], "ObservedPlus", drawStyle="L", legendStyle="l"),
            histograms.HistoGraph(graphs["obs_th_minus"], "ObservedMinus", drawStyle="L"),
            histograms.HistoGraph(excluded, "Excluded", drawStyle="F", legendStyle="f"),
            histograms.HistoGraph(graphs["exp"], "Expected", drawStyle="L"),
            histograms.HistoGraph(graphs["exp1"], "Expected1", drawStyle="F", legendStyle="fl"),
            histograms.HistoGraph(graphs["exp2"], "Expected2", drawStyle="F", legendStyle="fl"),
            ])

    plot.histoMgr.setHistoLegendLabelMany({
            "ObservedPlus": "Observed #pm1#sigma (th.)",
            "ObservedMinus": None,
            "Expected": None,
            "Expected1": "Expected median #pm 1#sigma",
            "Expected2": "Expected median #pm 2#sigma"
            })
    plot.setLegend(histograms.createLegend(0.57, 0.155, 0.87, 0.355))

    plot.createFrame(name, opts={"ymin": 0, "ymax": tanbMax})
    plot.frame.GetXaxis().SetTitle(xlabel)
    plot.frame.GetYaxis().SetTitle("tan(#beta)")

    plot.draw()

    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    histograms.addLuminosityText(x=None, y=None, lumi=limits.getLuminosity())

    size = 20
    x = 0.2
    histograms.addText(x, 0.9, "t #rightarrow H^{+}b, H^{+} #rightarrow #tau#nu", size=size)
    histograms.addText(x, 0.863, limits.getFinalstateText(), size=size)
    histograms.addText(x, 0.815, "MSSM m_{h}^{max}", size=size)
    histograms.addText(x, 0.775, "BR(H^{+} #rightarrow #tau#nu) = 1", size=size)
    histograms.addText(x, 0.735, "#mu=200 GeV", size=size)

    plot.save()

def doPlotMu(name, graphs, styleList, limits, xlabel):
    objs = []
    ll = {}
    for gr, mu in graphs:
        objs.append(histograms.HistoGraph(gr, "Obs%d"%mu, drawStyle="LP", legendStyle="lp"))
        ll["Obs%d"%mu] = "Observed, #mu=%d GeV/c^{2}" % mu

    plot = plots.PlotBase(objs)
    plot.histoMgr.forEachHisto(styles.Generator(styleList))
    plot.histoMgr.setHistoLegendLabelMany(ll)
    plot.setLegend(histograms.moveLegend(histograms.createLegend(0.57, 0.155, 0.87, 0.355), dx=-0.1))

    plot.createFrame(name, opts={"ymin": 0, "ymax": tanbMax})
    plot.frame.GetXaxis().SetTitle(xlabel)
    plot.frame.GetYaxis().SetTitle("tan(#beta)")

    plot.draw()

    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    histograms.addLuminosityText(x=None, y=None, lumi=limits.getLuminosity())

    size = 20
    x = 0.2
    histograms.addText(x, 0.9, "t #rightarrow H^{+}b, H^{+} #rightarrow #tau#nu", size=size)
    histograms.addText(x, 0.863, limits.getFinalstateText(), size=size)
    histograms.addText(x, 0.815, "MSSM m_{h}^{max}", size=size)
    histograms.addText(x, 0.775, "BR(H^{+} #rightarrow #tau#nu) = 1", size=size)

    plot.save()


if __name__ == "__main__":
    main()
