#!/usr/bin/env python

import sys

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.limit as limit

def main():
    limits = limit.BRLimits()

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    # Set the paper mode
    #limit.forPaper = True
    if limit.forPaper:
        histograms.cmsTextMode = histograms.CMSMode.PAPER

    doBRlimit(limits)
    doLimitError(limits)
    limits.print2()

def doBRlimit(limits):
    graphs = []
    gr = limits.observedGraph()
    if gr != None:
        graphs.append(histograms.HistoGraph(gr, "Observed", drawStyle="PL", legendStyle="lp"))
    graphs.extend([
            histograms.HistoGraph(limits.expectedGraph(), "Expected", drawStyle="L"),
            histograms.HistoGraph(limits.expectedBandGraph(sigma=1), "Expected1", drawStyle="F", legendStyle="fl"),
            histograms.HistoGraph(limits.expectedBandGraph(sigma=2), "Expected2", drawStyle="F", legendStyle="fl"),
            ])

    plot = plots.PlotBase(graphs)

    plot.histoMgr.setHistoLegendLabelMany({
            "Expected": None,
            "Expected1": "Expected median #pm 1#sigma",
            "Expected2": "Expected median #pm 2#sigma"
            })
    legend = histograms.createLegend(0.48, 0.75, 0.85, 0.92)
    if len(limits.getFinalstates()) > 1:
        legend = histograms.moveLegend(legend, dy=-0.1)
    plot.setLegend(legend)

    plot.createFrame("limitsBr", opts={"ymin": 0, "ymax": limits.getFinalstateYmaxBR()})
    plot.frame.GetXaxis().SetTitle(limit.mHplus())
    plot.frame.GetYaxis().SetTitle(limit.BRlimit)

    plot.draw()

    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    histograms.addLuminosityText(x=None, y=None, lumi=limits.getLuminosity())

    size = 20
    x = 0.2
    histograms.addText(x, 0.88, limit.process, size=size)
    histograms.addText(x, 0.84, limits.getFinalstateText(), size=size)
    histograms.addText(x, 0.79, limit.BRassumption, size=size)

    plot.save()

def doLimitError(limits):
    expRelErrors = []
    expLabels = {}
    obsRelErrors = []
    obsLabels = {}

    order = [0, 1, -1, 2, -2]
    expErrors = [limits.expectedErrorGraph(sigma=s) for s in order]
    if expErrors[0] != None:
        exps = [limits.expectedGraph(sigma=s) for s in order]
        expRelErrors = [(divideGraph(expErrors[i], exps[i]), "ExpRelErr%d"%i) for i in xrange(len(exps))]
        expLabels = {
            "ExpRelErr0": "Expected median",
            "ExpRelErr1": "Expected +1#sigma",
            "ExpRelErr2": "Expected -1#sigma",
            "ExpRelErr3": "Expected +2#sigma",
            "ExpRelErr4": "Expected -2#sigma",
            }

    obsErr = limits.observedErrorGraph()
    if obsErr != None:
        obs = limits.observedGraph()
        if obs != None:
            obsRelErrors = [(divideGraph(obsErr, obs), "ObsRelErr")]
            obsLabels = {"ObsRelErr": "Observed"}

    if len(expRelErrors) == 0 and len(obsRelErrors) == 0:
        return
        
    plot = plots.PlotBase()
    if len(expRelErrors) > 0:
        plot.histoMgr.extendHistos([histograms.HistoGraph(x[0], x[1], drawStyle="PL", legendStyle="lp") for x in expRelErrors])
        plot.histoMgr.forEachHisto(styles.generator())
        def sty(h):
            r = h.getRootHisto()
            r.SetLineStyle(1)
            r.SetLineWidth(3)
            r.SetMarkerSize(1.4)
        plot.histoMgr.forEachHisto(sty)
        plot.histoMgr.setHistoLegendLabelMany(expLabels)
    if len(obsRelErrors) > 0:
        obsRelErrors[0][0].SetMarkerSize(1.4)
        obsRelErrors[0][0].SetMarkerStyle(25)
        plot.histoMgr.insertHisto(0, histograms.HistoGraph(obsRelErrors[0][0], obsRelErrors[0][1], drawStyle="PL", legendStyle="lp"))
        plot.histoMgr.setHistoLegendLabelMany(obsLabels)

    plot.setLegend(histograms.moveLegend(histograms.createLegend(0.48, 0.75, 0.85, 0.92), dx=0.1, dy=-0.1))

    plot.createFrame("limitsBrRelativeUncertainty", opts={"ymin": 0, "ymaxfactor": 1.5})
    plot.frame.GetXaxis().SetTitle(limit.mHplus())
    plot.frame.GetYaxis().SetTitle("Uncertainty/limit")

    plot.draw()

    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    histograms.addLuminosityText(x=None, y=None, lumi=limits.getLuminosity())

    size = 20
    x = 0.2
    histograms.addText(x, 0.88, limit.process, size=size)
    histograms.addText(x, 0.84, limits.getFinalstateText(), size=size)
    histograms.addText(x, 0.79, limit.BRassumption, size=size)

    size = 22
    x = 0.55
    histograms.addText(x, 0.88, "Toy MC relative", size=size)
    histograms.addText(x, 0.84, "statistical uncertainty", size=size)

    plot.save()


def divideGraph(num, denom):
    gr = ROOT.TGraph(num)
    for i in xrange(gr.GetN()):
        y = denom.GetY()[i]
        val = 0
        if y != 0:
            val = gr.GetY()[i]/y
        gr.SetPoint(i, gr.GetX()[i], val)
    return gr


                          

if __name__ == "__main__":
    main()
