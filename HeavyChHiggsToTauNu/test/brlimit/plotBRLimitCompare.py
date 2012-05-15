#!/usr/bin/env python

import sys
import glob
import json
import array

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles

import plotBRLimit as brlimit

def main():
    # Apply TDR style
    style = tdrstyle.TDRStyle()

    compareTauJets()

def compareTauJets():
    doCompare("taujets", [
            # (name, dir)
            ("LHC-CLs", "LandS*taujets_lhc_*"),
            ("LHC-CLs (asymp)", "LandS*taujets_lhcasy_*"),
            ("LEP-CLs", "LandS*taujets_lep_*"),
            ])

    doCompare("emu", [
            # (name, dir)
            ("LHC-CLs", "LandS*emu_lhc_*"),
            ("LHC-CLs (asymp)", "LandS*emu_lhcasy_*"),
            ("LEP-CLs", "LandS*emu_lep_*"),
            ])

    doCompare("mutau", [
            # (name, dir)
            ("LHC-CLs", "LandS*mutau_lhc_*"),
            ("LHC-CLs (asymp)", "LandS*mutau_lhcasy_*"),
            ("LEP-CLs", "LandS*mutau_lep_*"),
            ])


styleList = [styles.Style(24, ROOT.kBlack)] + styles.getStyles()

def doCompare(name, compareList):
    legendLabels = []
    limits = []
    for label, path in compareList:
        legendLabels.append(label)
        dirs = glob.glob(path)
        dirs.sort()
        if len(dirs) == 0:
            raise Exception("No directories for pattern '%s'" % path)
        directory = dirs[-1]
        print "Picked %s" % directory
        limits.append(brlimit.BRLimits(directory))

    doPlot2(limits, legendLabels, name)

    ymax = limits[0].getFinalstateYmax()
    doPlot(limits, legendLabels, [l.observedGraph() for l in limits],
           name+"_observed", "95% CL limit for BR(t#rightarrow bH^{+})", opts={"ymax": ymax})

    doPlot(limits, legendLabels, [l.expectedGraph() for l in limits],
           name+"_expectedMedian", "95% CL limit for BR(t#rightarrow bH^{+})", opts={"ymax": ymax})

    legendLabels2 = legendLabels + [None]*len(legendLabels)

    doPlot(limits, legendLabels2,
           [brlimit.divideGraph(l.expectedGraph(sigma=+1), l.expectedGraph()) for l in limits] +
           [brlimit.divideGraph(l.expectedGraph(sigma=-1), l.expectedGraph()) for l in limits],
           name+"_expectedSigma1Relative", "Expected #pm1#sigma / median", opts={"ymaxfactor": 1.2})

    doPlot(limits, legendLabels2,
           [brlimit.divideGraph(l.expectedGraph(sigma=+2), l.expectedGraph()) for l in limits] +
           [brlimit.divideGraph(l.expectedGraph(sigma=-2), l.expectedGraph()) for l in limits],
           name+"_expectedSigma2Relative", "Expected #pm2#sigma / median", opts={"ymaxfactor": 1.2})

    doPlot(limits, legendLabels2,
           [l.expectedGraph(sigma=+1) for l in limits] +
           [l.expectedGraph(sigma=-1) for l in limits],
           name+"_expectedSigma1", "Expected #pm1#sigma", opts={"ymax": ymax})

    doPlot(limits, legendLabels2,
           [l.expectedGraph(sigma=+2) for l in limits] +
           [l.expectedGraph(sigma=-2) for l in limits],
           name+"_expectedSigma2", "Expected #pm2#sigma", opts={"ymax": ymax})

    # doPlot(limits, legendLabels,
    #        [brlimit.divideGraph(l.expectedGraph(sigma=+1), l.expectedGraph()) for l in limits]
    #        name+"_expectedSigma1Plus", "Expected +1#sigma / median", opts={"ymaxfactor": 1.2})

    # doPlot(limits, legendLabels,
    #        [brlimit.divideGraph(l.expectedGraph(sigma=+2), l.expectedGraph()) for l in limits]
    #        name+"_expectedSigma2Plus", "Expected +2#sigma / median", opts={"ymaxfactor": 1.2})

    # doPlot(limits, legendLabels,
    #        [brlimit.divideGraph(l.expectedGraph(sigma=-1), l.expectedGraph()) for l in limits],
    #        name+"_expectedSigma1Minus", "Expected -1#sigma / median", opts={"ymaxfactor": 1.2})

    # doPlot(limits, legendLabels,
    #        [brlimit.divideGraph(l.expectedGraph(sigma=-2), l.expectedGraph()) for l in limits],
    #        name+"_expectedSigma2Minus", "Expected -2#sigma / median", opts={"ymaxfactor": 1.2})


def doPlot(limits, legendLabels, graphs, name, ylabel, opts={}):
    hg = []
    ll = {}
    for i in xrange(len(graphs)):
        hg.append(histograms.HistoGraph(graphs[i], "Graph%d"%i, drawStyle="PL", legendStyle="lp"))
        ll["Graph%d"%i] = legendLabels[i]

    plot = plots.PlotBase(hg)
    plot.histoMgr.forEachHisto(styles.Generator(styleList[0:len(limits)]))
    def sty(h):
        r = h.getRootHisto()
        r.SetLineWidth(3)
        r.SetLineStyle(1)
    plot.histoMgr.forEachHisto(sty)
    plot.histoMgr.setHistoLegendLabelMany(ll)
    plot.setLegend(histograms.createLegend(0.48, 0.75, 0.85, 0.92))
    opts_ = {"ymin": 0}
    opts_.update(opts)
    plot.createFrame(name, opts=opts_)

    plot.frame.GetXaxis().SetTitle("m_{H^{+}} (GeV)")
    plot.frame.GetYaxis().SetTitle(ylabel)

    plot.draw()

    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    histograms.addLuminosityText(x=None, y=None, lumi=limits[0].getLuminosity())

    size = 20
    x = 0.2
    histograms.addText(x, 0.88, "t #rightarrow H^{+}b, H^{+} #rightarrow #tau#nu", size=size)
    histograms.addText(x, 0.84, limits[0].getFinalstateText(), size=size)
    histograms.addText(x, 0.79, "BR(H^{+} #rightarrow #tau#nu) = 1", size=size)

    plot.save()

def doPlot2(limits, legendLabels, name):
    graphs = [
        histograms.HistoGraph(limits[0].expectedGraph(), "Expected", drawStyle="L"),
        histograms.HistoGraph(limits[0].expectedBandGraph(sigma=1), "Expected1", drawStyle="F", legendStyle="fl"),
        histograms.HistoGraph(limits[0].expectedBandGraph(sigma=2), "Expected2", drawStyle="F", legendStyle="fl"),
        ]
    graphs[0].getRootHisto().SetLineStyle(1)
    plot = plots.PlotBase(graphs)
    ll = {
        "Expected": None,
        "Expected1": "%s exp. median #pm 1#sigma" % legendLabels[0],
        "Expected2": "%s exp. median #pm 2#sigma" % legendLabels[0],
        }

    stGen = styles.generator()
    for i in xrange(1, len(limits)):
        gr = histograms.HistoGraph(limits[i].expectedGraph(), "Exp%d"%i, drawStyle="L")
        stGen(gr)
        gr.getRootHisto().SetLineWidth(3)
        gr.getRootHisto().SetLineStyle(1)
        plot.histoMgr.insertHisto(len(plot.histoMgr)-2, gr, legendIndex=len(plot.histoMgr))
        ll["Exp%d"%i] = "%s exp. median" % legendLabels[i]

    plot.histoMgr.setHistoLegendLabelMany(ll)
    plot.setLegend(histograms.moveLegend(histograms.createLegend(0.48, 0.75, 0.85, 0.92), dx=-0.02))

    plot.createFrame(name+"_limits", opts={"ymin": 0, "ymax": limits[0].getFinalstateYmax()})
    plot.frame.GetXaxis().SetTitle("m_{H^{+}} (GeV)")
    plot.frame.GetYaxis().SetTitle("95% CL limit for BR(t#rightarrow bH^{+})")

    plot.draw()

    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    histograms.addLuminosityText(x=None, y=None, lumi=limits[0].getLuminosity())

    size = 20
    x = 0.2
    histograms.addText(x, 0.88, "t #rightarrow H^{+}b, H^{+} #rightarrow #tau#nu", size=size)
    histograms.addText(x, 0.84, limits[0].getFinalstateText(), size=size)
    histograms.addText(x, 0.79, "BR(H^{+} #rightarrow #tau#nu) = 1", size=size)

    plot.save()


if __name__ == "__main__":
    main()
