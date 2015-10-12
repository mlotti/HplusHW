#!/usr/bin/env python

import sys

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.styles as styles
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.LimitCalc.limit as limit

tanbMax = 60
mu = 200

def main():
    limits = limit.BRLimits()

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    if limit.forPaper:
        histograms.cmsTextMode = histograms.CMSMode.PAPER

    # Get BR limits
    graphs = {}
    obs = limits.observedGraph()
    myBlindedStatus = True
    for i in xrange(0,obs.GetN()):
        if abs(obs.GetY()[i]) > 0.00001:
            myBlindedStatus = False

    if not myBlindedStatus:
        graphs["obs"] = obs
    graphs["exp"] = limits.expectedGraph()
    graphs["exp1"] = limits.expectedBandGraph(sigma=1)
    graphs["exp2"] = limits.expectedBandGraph(sigma=2)
    # Remove m=80
    for gr in graphs.values():
        limit.cleanGraph(gr, minX=100)

    # Get theory uncertainties on observed
    if not myBlindedStatus:
        obs_th_plus = limit.getObservedPlus(obs)
        obs_th_minus = limit.getObservedMinus(obs)
        for gr in [obs_th_plus, obs_th_minus]:
            gr.SetLineWidth(3)
            gr.SetLineStyle(5)
    #        gr.SetLineStyle(9)
        graphs["obs_th_plus"] = obs_th_plus
        graphs["obs_th_minus"] = obs_th_minus

    # Interpret in MSSM
    global mu
    for key in graphs.keys():
        removeNotValid = not (key in ["exp1", "exp2"])
        graphs[key] = limit.graphToTanBeta(graphs[key], mu, removeNotValid)

    doPlot("limitsTanb_mh", graphs, limits, limit.mHplus())
    
    for gr in graphs.values():
        limit.graphToMa(gr)

    doPlot("limitsTanb_ma", graphs, limits, limit.mA())

    if myBlindedStatus:
        print "Refusing cowardly to do mu variation plots for blinded results"
        return

    # Mu variations
    mus = [1000, 200, -200, -1000]
    muGraphs = [(limit.graphToTanBeta(obs, m), m) for m in mus]

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
    doPlotMu("limitsTanb_mus_mh", muGraphs, st, limits, limit.mHplus())

    for gr, mu in muGraphs:
        limit.graphToMa(gr)
    doPlotMu("limitsTanb_mus_ma", muGraphs, st, limits, limit.mA())

def doPlot(name, graphs, limits, xlabel):
    if "obs" in graphs.keys():
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

    plot = None
    if "obs" in graphs.keys():
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
    else:
        plot = plots.PlotBase([
            histograms.HistoGraph(graphs["exp"], "Expected", drawStyle="L"),
            histograms.HistoGraph(graphs["exp1"], "Expected1", drawStyle="F", legendStyle="fl"),
            histograms.HistoGraph(graphs["exp2"], "Expected2", drawStyle="F", legendStyle="fl"),
        ])
        plot.histoMgr.setHistoLegendLabelMany({
                "Expected": None,
                "Expected1": "Expected median #pm 1#sigma",
                "Expected2": "Expected median #pm 2#sigma"
                })

    plot.setLegend(histograms.createLegend(0.57, 0.155, 0.87, 0.355))

    plot.createFrame(name, opts={"ymin": 0, "ymax": tanbMax})
    plot.frame.GetXaxis().SetTitle(xlabel)
    plot.frame.GetYaxis().SetTitle(limit.tanblimit)

    plot.draw()

    plot.setLuminosity(limits.getLuminosity())
    plot.addStandardTexts()

    size = 20
    x = 0.2
    histograms.addText(x, 0.9, limit.process, size=size)
    histograms.addText(x, 0.863, limits.getFinalstateText(), size=size)
    histograms.addText(x, 0.815, "MSSM m_{h}^{max}", size=size)
    histograms.addText(x, 0.775, limit.BRassumption, size=size)
    histograms.addText(x, 0.735, "#mu=%d %s"%(mu, limit.massUnit()), size=size)

    plot.save()

def doPlotMu(name, graphs, styleList, limits, xlabel):
    objs = []
    ll = {}
    for gr, mu in graphs:
        objs.append(histograms.HistoGraph(gr, "Obs%d"%mu, drawStyle="LP", legendStyle="lp"))
        ll["Obs%d"%mu] = "Observed, #mu=%d %s" % (mu, limit.massUnit())

    plot = plots.PlotBase(objs)
    plot.histoMgr.forEachHisto(styles.Generator(styleList))
    plot.histoMgr.setHistoLegendLabelMany(ll)
    plot.setLegend(histograms.moveLegend(histograms.createLegend(0.57, 0.155, 0.87, 0.355), dx=-0.1))

    plot.createFrame(name, opts={"ymin": 0, "ymax": tanbMax})
    plot.frame.GetXaxis().SetTitle(xlabel)
    plot.frame.GetYaxis().SetTitle(limit.tanblimit)

    plot.draw()

    plot.setLuminosity(limits.getLuminosity())
    plot.addStandardTexts()

    size = 20
    x = 0.2
    histograms.addText(x, 0.9, limit.process, size=size)
    histograms.addText(x, 0.863, limits.getFinalstateText(), size=size)
    histograms.addText(x, 0.815, "MSSM m_{h}^{max}", size=size)
    histograms.addText(x, 0.775, limit.BRassumption, size=size)

    plot.save()


if __name__ == "__main__":
    main()
