#!/usr/bin/env python

import sys
import array
from optparse import OptionParser

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.styles as styles
import HiggsAnalysis.LimitCalc..limit as limit

# Example combine command
# combine -M MultiDimFit -n <name> -m <mass> -d workspaceM100.root  --algo=grid --points=10000

def main(opts, args):
    style = tdrstyle.TDRStyle()
    histograms.cmsTextMode = histograms.CMSMode.NONE

    f = ROOT.TFile.Open(args[0])

    tree = f.Get("limit")
    doPlot(tree)

    f.Close()

def doPlot(tree):
#    tree.Draw("BRT:BRH >>htemp(100,0,1, 100,0,1)", "deltaNLL * (deltaNLL < 0.5", "colz goff")
#    sigma1 = ROOT.gDirectory.Get("htemp").Clone("sigma1")

    tree.Draw("BRT:BRH >>htemp(100,0,1, 100,0,1)", "deltaNLL * (deltaNLL <= 2)", "colz")
    sigma2 = ROOT.gDirectory.Get("htemp").Clone("sigma2")
    
    bfBRT = None
    bfBRH = None

    for entry in tree:
        if entry.quantileExpected == 1:
            bfBRT = entry.BRT
            bfBRH = entry.BRH
            break

    print "Best fit B(t->H+) %.8f, B(H+->tau) %.8f" % (bfBRT, bfBRH)

    bestFit = ROOT.TGraph(1, array.array("d", [bfBRH]), array.array("d", [bfBRT]))
    bestFit.SetMarkerStyle(34)
    bestFit.SetMarkerSize(2)
    histos = [
        histograms.HistoGraph(bestFit, "bestFit", drawStyle="P", legendLabel="Best fit", legendStyle="P"),
        histograms.Histo(sigma2, "sigma2", drawStyle="COLZ", legendLabel=None),
    ]

    brt = "#it{B}_{t#rightarrow bH^{+}}"
    brh = "#it{B}_{H^{+}#rightarrow#tau#nu}"
    legend_h = 0.1

    if opts.bxblimit is not None:
        limit_tf = ROOT.TF1("bxblimit", "%s/x"%opts.bxblimit)
        limit_tf.SetLineWidth(2)
        limit_tf.SetLineStyle(2)
        limit_tf.SetLineColor(ROOT.kBlack)
        histos.insert(1, histograms.Histo(limit_tf, "bxblimit", legendLabel="Exp. limit on {brt}#times{brh}\n={limit:.2f}%".format(brt=brt, brh=brh, limit=float(opts.bxblimit)*100)))
        legend_h += 0.03

    plot = plots.PlotBase(histos)

    x = 0.4
    y = 0.87
    dy = 0.05
    plot.appendPlotObject(histograms.PlotText(x, y, "HH: {brt}^{{2}} #times {brh}^{{2}}".format(brt=brt, brh=brh), bold=False, size=20))
    y -= dy
    #plot.appendPlotObject(histograms.PlotText(x, y, "HW: 2(1-{brt}){brt} #times {brh}".format(brt=brt, brh=brh), bold=False, size=20))
    plot.appendPlotObject(histograms.PlotText(x, y, "HW: 2(1-{brt}{brh}){brt}{brh}".format(brt=brt, brh=brh), bold=False, size=20)) # mod1
    y -= dy
    #plot.appendPlotObject(histograms.PlotText(x, y, "WW: (1-{brt})^{{2}}".format(brt=brt), bold=False, size=20))
    plot.appendPlotObject(histograms.PlotText(x, y, "WW: (1-{brt}{brh})^{{2}}".format(brt=brt, brh=brh), bold=False, size=20)) # mod2
    y -= dy*2
    if opts.mass is not None:
        plot.appendPlotObject(histograms.PlotText(x, y, "m_{H^{+}} = %s GeV" % opts.mass, bold=False, size=20))
        y -= dy
    plot.appendPlotObject(histograms.PlotText(x, y, "Fit to bkg-only Asimov dataset", bold=False, size=20))
    
    y -= 0.01
    plots.drawPlot(plot, opts.name, xlabel=brh, ylabel=brt, zlabel="#DeltaLL", zhisto="sigma2",
                   opts={"ymax": 1.0}, createLegend={"x1":x, "y2":y, "x2":x+0.2, "y1":y-legend_h})


if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options] root_file",add_help_option=True,conflict_handler="resolve")
    parser.add_option("--name", dest="name", type="string", default="llscan", help="Name of the output plot")
    parser.add_option("--bxblimit", dest="bxblimit", type="string", default=None, help="BxB limit, if to be drawn")
    parser.add_option("--mass", dest="mass", type="string", default=None, help="H+ mass point")

    (opts, args) = parser.parse_args()

    main(opts, args)
