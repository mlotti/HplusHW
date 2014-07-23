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
    style = tdrstyle.TDRStyle()

    mlfit = limit.MLFitData()

    doBkgFitPlots(mlfit)

def doBkgFitPlots(mlfit):
    firstMass = mlfit.massPoints()[0]

    def createDrawPlot(gr, labels, fname):
        plot = plots.PlotBase([histograms.HistoGraph(gr, "Fitted", drawStyle="P")])
    
        canvasOpts = {}
        if len(labels) > 15:
            canvasOpts["addHeight"] = 0.03*(len(labels)-15)

        plot.createFrame(fname, opts={"ymin": 0, "xmin": -3.2, "xmax": 2.5}, canvasOpts=canvasOpts)
        plot.getFrame().GetXaxis().SetTitle("Fitted value")

        scale = 1
        if "addHeight" in canvasOpts:
            scale = 1/(1+canvasOpts["addHeight"])
            plot.getFrame().GetXaxis().SetTickLength(plot.getFrame().GetXaxis().GetTickLength()*scale)
            plot.getPad().SetBottomMargin(plot.getPad().GetBottomMargin()*scale)
            plot.getPad().SetTopMargin(plot.getPad().GetTopMargin()*scale)

        plot.getPad().SetLeftMargin(plot.getPad().GetRightMargin())
        plot.getPad().Update()
    
        ymin = plot.cf.frame.GetYaxis().GetXmin()
        ymax = plot.cf.frame.GetYaxis().GetXmax()
    
        for xval, color in [(0, ROOT.kRed), (-1, ROOT.kBlue), (1, ROOT.kBlue)]:
            l = ROOT.TLine(xval, ymin, xval, ymax)
            l.SetLineColor(color)
            l.SetLineStyle(ROOT.kDotted)
            l.SetLineWidth(2)
            plot.prependPlotObject(l)
    
        plot.cf.frame.GetYaxis().SetLabelSize(0)
    
        plot.draw()
        histograms.addCmsPreliminaryText(y=1-(1-histograms.textDefaults.getValues("cmsPreliminary", None, None)[1])*scale)
    
        # Intentionally not NDC
        l = ROOT.TLatex()
        l.SetTextFont(l.GetTextFont()-20) # bold->normal
        l.SetTextSize(17)

        x_nuis = -3.0
        x_value = 1.5

        l.DrawLatex(x_nuis, ymax*0.93, "Nuisance parameter")
        l.DrawLatex(x_value, ymax*0.93, "Fitted value")

        for i, label in enumerate(labels):
            y = gr.GetY()[i]-0.3
    
            l.DrawLatex(x_nuis, y, label[:20])
            l.DrawLatex(x_value, y, "%.2f #pm %.2f" % (gr.GetX()[i], gr.GetErrorX(i)))
        
        plot.save()
    

    (gr, labels) = mlfit.fittedGraph(firstMass, backgroundOnly=True)
    createDrawPlot(gr, labels, "mlfit_backgroundOnly")

    try:
        (gr, labels, shapeStatNuisance) = mlfit.fittedGraphShapeStat(firstMass, backgroundOnly=True)
        createDrawPlot(gr, labels, "mlfit_backgroundOnlyShapeStat")
    except Exception, e:
        print "Warning: %s" % str(e)


if __name__ == "__main__":
    main()
