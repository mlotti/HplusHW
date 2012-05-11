#!/usr/bin/env python

import sys
import json
import array

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots

import plotBRLimit as brlimit
import mkBrLimits_processTanbPlots as tanb

tanbMax = 60
mu = 200
#forPaper = False
forPaper = True

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
    graphs["obs"] = limits.observedGraph()
    graphs["exp"] = limits.expectedGraph()
    graphs["exp1"] = limits.expectedGraph(sigma=1)
    graphs["exp2"] = limits.expectedGraph(sigma=2)

    # Remove m=80
    for gr in graphs.values():
        tanb.cleanGraph(gr, minX=100)

    # Get theory uncertainties on observed
    obs_th_plus = tanb.getObservedPlus(graphs["obs"]);   obs_th_plus.SetName("ObservedTheoryPlus")
    obs_th_minus = tanb.getObservedMinus(graphs["obs"]); obs_th_minus.SetName("ObservedTheoryMinus")
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


def doPlot(name, graphs, limits, xlabel):
    obs = graphs["obs"]
    excluded = ROOT.TGraph(obs)
    excluded.SetFillColor(ROOT.kGray)
    excluded.SetPoint(obs.GetN(), obs.GetX()[obs.GetN()-1], 2*tanbMax)
    excluded.SetPoint(obs.GetN(), obs.GetX()[0], 2*tanbMax)
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



if __name__ == "__main__":
    main()
