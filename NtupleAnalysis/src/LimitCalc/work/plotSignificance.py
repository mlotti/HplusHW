#!/usr/bin/env python

import os
import sys
import json
from optparse import OptionParser

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.styles as styles
import HiggsAnalysis.LimitCalc.limit as limit

def main(opts):
    if not opts.unblinded:
        print "Working in BLINDED mode, i.e. I will not tell you the observed significance before you say please ..."

    signif = limit.SignificanceData()
    lumi = None
    if os.path.exists("limits.json"):
        f = open("limits.json")
        data = json.load(f)
        f.close()
        lumi = float(data["luminosity"])

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    histograms.createLegend.moveDefaults(dh=-0.4, dy=-0.2)

    doPlot(opts, signif, lumi)
    doPlot(opts, signif, lumi, pvalue=True)

drawPlot = plots.PlotDrawer(xlabel="m_{H^{+}} (GeV)", cmsTextPosition="outFrame")

def doPlot(opts, signif, lumi, pvalue=False):
    grObs = None
    histos = []
    if opts.unblinded:
        grObs = signif.observedGraph(pvalue)
        histos.append(histograms.HistoGraph(grObs, "Observed", drawStyle="LP"))
    grExp = signif.expectedGraph(pvalue)
    histos.append(histograms.HistoGraph(grExp, "Expected", drawStyle="L"))

    expData = "#it{B}#times#it{B}=%s %%" % signif.lightExpectedSignal()
    if signif.isHeavyStatus():
        expData = "#sigma#times#it{B}=%s pb" % signif.heavyExpectedSignal()

    plot = plots.PlotBase(histos)
    plot.setLuminosity(lumi)
    if pvalue:
        plot.histoMgr.setHistoLegendLabelMany({
            "Expected": "Expected p-value",
            "Observed": "Observed p-value"
        })
        plot.appendPlotObject(histograms.PlotText(0.6, 0.68, expData, size=18))
        drawPlot(plot, "pvalue", ylabel="P-value", log=True, moveLegend={"dx": -0.2}, opts={"ymin": 1e-10, "ymax": 1})
    else:
        plot.histoMgr.setHistoLegendLabelMany({
            "Expected": "Expected significance",
            "Observed": "Observed significance"
        })
        plot.appendPlotObject(histograms.PlotText(0.2, 0.68, expData, size=18))
        drawPlot(plot, "significance", ylabel="Significance", moveLegend={"dx": -0.55})

    

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("--unblinded", dest="unblinded", default=False, action="store_true",
                      help="Enable unblined mode")
    (opts, args) = parser.parse_args()
    main(opts)
