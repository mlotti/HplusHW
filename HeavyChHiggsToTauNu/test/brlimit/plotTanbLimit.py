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

def main():
    limits = brlimit.BRLimits()

    # Apply TDR style
    style = tdrstyle.TDRStyle()

    obs = limits.observedGraph()
    exp = limits.expectedGraph()
    exp1 = limits.expectedGraph(sigma=1)
    exp2 = limits.expectedGraph(sigma=2)

    # Remove m=80
    for gr in [obs, exp, exp1, exp2]:
        tanb.cleanGraph(gr, minX=100)

    mu = 200

    obs = tanb.graphToTanBeta(obs, mu)
    exp = tanb.graphToTanBeta(exp, mu)
    exp1 = tanb.graphToTanBeta(exp1, mu, False)
    exp2 = tanb.graphToTanBeta(exp2, mu, False)

    doPlot("limitsTanb_mh", obs, exp, exp1, exp2, limits, "m_{H^{+}} (GeV)")

    for gr in [obs, exp, exp1, exp2]:
        tanb.graphToMa(gr)

    doPlot("limitsTanb_ma", obs, exp, exp1, exp2, limits, "m_{A} (GeV)")


def doPlot(name, obs, exp, exp1, exp2, limits, xlabel):
    excluded = ROOT.TGraph(obs)
    excluded.SetFillColor(ROOT.kGray)
    excluded.SetPoint(obs.GetN(), obs.GetX()[obs.GetN()-1], 2*tanbMax)
    excluded.SetPoint(obs.GetN(), obs.GetX()[0], 2*tanbMax)
    excluded.SetFillColor(ROOT.kGray)
    excluded.SetFillStyle(3354)
    excluded.SetLineWidth(0)
    excluded.SetLineColor(ROOT.kWhite)

    plot = plots.PlotBase([
            histograms.HistoGraph(obs, "Observed", drawStyle="PL", legendStyle="lp"),
            histograms.HistoGraph(excluded, "Excluded", drawStyle="F", legendStyle="f"),
            histograms.HistoGraph(exp, "Expected", drawStyle="L"),
            histograms.HistoGraph(exp1, "Expected1", drawStyle="F", legendStyle="fl"),
            histograms.HistoGraph(exp2, "Expected2", drawStyle="F", legendStyle="fl"),
            ])

    plot.histoMgr.setHistoLegendLabelMany({
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
