#!/usr/bin/env python

import sys
import math
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
    # Assume by default that the observed limit should be blinded
    if not opts.unblinded:
        print "Working in BLINDED mode, i.e. I will not tell you the observed limit before you say please ..."

    limits = limit.BRLimits()

    # Enable OpenGL
    if opts.excludedArea:
        ROOT.gEnv.SetValue("OpenGL.CanvasPreferGL", 1)

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    if not opts.isHeavy:
        # Give more space for four digits on the y axis labels
        style.tdrStyle.SetPadLeftMargin(0.19)
        style.tdrStyle.SetTitleYOffset(1.6)

    # Set the paper mode
    limit.forPaper = True
    if opts.paper:
        histograms.cmsTextMode = histograms.CMSMode.PAPER
    if opts.unpublished:
        histograms.cmsTextMode = histograms.CMSMode.UNPUBLISHED

    if opts.parentheses:
        limit.useParentheses()

    doBRlimit(limits, opts.unblinded, opts)
    doBRlimit(limits, opts.unblinded, opts, log=True)
    doLimitError(limits, opts.unblinded)
    limits.print2(opts.unblinded)
    limits.saveAsLatexTable(opts.unblinded)

def doBRlimit(limits, unblindedStatus, opts, log=False):
    leptonicFS = False
    
    graphs = []
    if unblindedStatus:
        gr = limits.observedGraph()
        if gr != None:
            gr.SetPoint(gr.GetN()-1, gr.GetX()[gr.GetN()-1]-1e-10, gr.GetY()[gr.GetN()-1])
            if opts.excludedArea:
                graphs.append(histograms.HistoGraph(gr, "Observed", drawStyle="PL", legendStyle=None))
                excluded = gr.Clone()
                excluded.SetPoint(excluded.GetN(), excluded.GetX()[excluded.GetN()-1], 0.05)
                excluded.SetPoint(excluded.GetN(), excluded.GetX()[0], 0.05)
                limit.setExcludedStyle(excluded)
                graphs.append(histograms.HistoGraph(excluded, "Excluded", drawStyle="F", legendStyle="lpf", legendLabel="Observed"))
            else:
                graphs.append(histograms.HistoGraph(gr, "Observed", drawStyle="PL", legendStyle="lp"))


    graphs.extend([
            histograms.HistoGraph(limits.expectedGraph(), "Expected", drawStyle="L"),
            histograms.HistoGraph(limits.expectedBandGraph(sigma=1), "Expected1", drawStyle="F", legendStyle="fl"),
            histograms.HistoGraph(limits.expectedBandGraph(sigma=2), "Expected2", drawStyle="F", legendStyle="fl"),
            ])

    saveFormats = [".png", ".C", ".pdf"]
    if not opts.excludedArea:
        saveFormats.append(".eps")
    plot = plots.PlotBase(graphs, saveFormats=saveFormats)
    plot.setLuminosity(limits.getLuminosity())

    plot.histoMgr.setHistoLegendLabelMany({
            "Expected": None,
            "Expected1": "Expected median #pm 1#sigma",
            "Expected2": "Expected median #pm 2#sigma"
            })
    
    dy = -0.1

    limit.BRassumption = ""   
    #limit.BRassumption = "Assuming B(H^{+}#rightarrow#tau^{+}#nu_{#tau}) = 1"
    #limit.BRassumption = "Assuming B(H^{+}#rightarrowt#bar{b}) = 1"
    if limit.BRassumption != "":
        dy -= 0.05
    #if len(limits.getFinalstates()) > 1:
    #    dy -= 0.1
    
    x = 0.51
    x = 0.45
    legend = histograms.createLegend(x, 0.78+dy, x+0.4, 0.92+dy)
    legend.SetMargin(0.17)
    # make room for the final state text
    if opts.excludedArea:
        legend.SetFillStyle(1001)
    plot.setLegend(legend)

    name = "limitsBr"
    ymin = opts.ymin-0.02
    ymax = opts.ymax+0.02 #limits.getFinalstateYmaxBR() # this could be also used, in principle
    if opts.logx:
        name += "_logx"
    if log:
        name += "_log"
        if opts.isHeavy:
            ymin = opts.ymin+1e-3
            ymax = opts.ymax*10.0
        else:
            ymin = opts.ymin+1e-3
            ymax = opts.ymax
#    if leptonicFS:
#        ymax = 10
    if len(limits.mass) == 1:
        plot.createFrame(name, opts={"xmin": limits.mass[0]-5.0, "xmax": limits.mass[0]+5.0, "ymin": ymin, "ymax": ymax})
    else:
        plot.createFrame(name, opts={"ymin": ymin, "ymax": ymax})
    plot.frame.GetXaxis().SetTitle(limit.mHplus())
    if opts.isHeavy:
        if limit.BRassumption != "":
            plot.frame.GetYaxis().SetTitle("95% CL limit for #sigma_{H^{+}} (pb)")
        else:
            plot.frame.GetYaxis().SetTitle(limit.sigmaBRlimit)
    else:
        plot.frame.GetYaxis().SetTitle(limit.BRlimit)

    if log:
        plot.getPad().SetLogy(log)
    if opts.logx:
        plot.getPad().SetLogx(log)

    plot.draw()
    plot.addStandardTexts()

    size = 20
    x = 0.51
    x = 0.45
    process = limit.process
    if opts.isHeavy:
        process = limit.processHeavy
    histograms.addText(x, 0.88, process, size=size)
    histograms.addText(x, 0.84, limits.getFinalstateText(), size=size)
    #histograms.addText(x, 0.84, "#tau_{h}+jets final state", size=size)
    #histograms.addText(x, 0.84, "#tau_{h}+jets and #mu#tau_{h} final states", size=size)
    #histograms.addText(x, 0.84, "#tau_{h}+jets, #mu#tau_{h}, ee, e#mu, #mu#mu final states", size=size)
    if leptonicFS:
        histograms.addText(x, 0.84, "#mu#tau_{h}, ee, e#mu, #mu#mu final states", size=size)
    if limit.BRassumption != "":
        histograms.addText(x, 0.79, limit.BRassumption, size=size)

    plot.save()

def doLimitError(limits,unblindedStatus):
    expRelErrors = []
    expLabels = {}
    obsRelErrors = []
    obsLabels = {}

    order = [0, 1, -1, 2, -2]
    expErrors = [limits.expectedErrorGraph(sigma=s) for s in order]
    if expErrors[0] != None:
        exps = [limits.expectedGraph(sigma=s) for s in order]
        expRelErrors = [(limit.divideGraph(expErrors[i], exps[i]), "ExpRelErr%d"%i) for i in xrange(len(exps))]
        expLabels = {
            "ExpRelErr0": "Expected median",
            "ExpRelErr1": "Expected +1#sigma",
            "ExpRelErr2": "Expected -1#sigma",
            "ExpRelErr3": "Expected +2#sigma",
            "ExpRelErr4": "Expected -2#sigma",
            }

    if unblindedStatus:
        obsErr = limits.observedErrorGraph()
        if obsErr != None:
            obs = limits.observedGraph()
            if obs != None:
                obsRelErrors = [(limit.divideGraph(obsErr, obs), "ObsRelErr")]
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
    if unblindedStatus:
        if len(obsRelErrors) > 0:
            obsRelErrors[0][0].SetMarkerSize(1.4)
            obsRelErrors[0][0].SetMarkerStyle(25)
            plot.histoMgr.insertHisto(0, histograms.HistoGraph(obsRelErrors[0][0], obsRelErrors[0][1], drawStyle="PL", legendStyle="lp"))
            plot.histoMgr.setHistoLegendLabelMany(obsLabels)

    plot.setLegend(histograms.moveLegend(histograms.createLegend(0.48, 0.75, 0.85, 0.92), dx=0.1, dy=-0.1))

    if len(limits.mass) == 1:
        plot.createFrame("limitsBrRelativeUncertainty", opts={"xmin": limits.mass[0]-5.0, "xmax": limits.mass[0]+5.0,  "ymin": 0, "ymaxfactor": 1.5})
    else:
        plot.createFrame("limitsBrRelativeUncertainty", opts={"ymin": 0, "ymaxfactor": 1.5})
    plot.frame.GetXaxis().SetTitle(limit.mHplus())
    plot.frame.GetYaxis().SetTitle("Uncertainty/limit")

    plot.draw()

    plot.setLuminosity(limits.getLuminosity())
    plot.addStandardTexts()

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


if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("--unblinded", dest="unblinded", default=False, action="store_true",
                      help="Enable unblined mode")
    parser.add_option("--paper", dest="paper", default=False, action="store_true",
                      help="Paper mode")
    parser.add_option("--unpub", dest="unpublished", default=False, action="store_true",
                      help="Unpublished mode")
    parser.add_option("--parentheses", dest="parentheses", default=False, action="store_true",
                      help="Use parentheses for sigma and BR")
    parser.add_option("--excludedArea", dest="excludedArea", default=False, action="store_true",
                      help="Add excluded area as in MSSM exclusion plots")
    parser.add_option("--logx", dest="logx", action="store_true", default=False, 
                      help="Plot x-axis (H+ mass) as logarithmic")     
    parser.add_option("--heavy", dest="isHeavy", action="store_true", default=False, 
                      help="Label y axis as sigma x BR (for heavy H+)")     
    parser.add_option("--ymin", type="float", dest="ymin", action="store", default=0.0, 
                      help="Minimum of y axis (default: 0.0)")     
    parser.add_option("--ymax", type="float", dest="ymax", action="store", default=1.0, 
                      help="Minimum of y axis (default: 1.0)")     
                     
    (opts, args) = parser.parse_args()
    main(opts)
