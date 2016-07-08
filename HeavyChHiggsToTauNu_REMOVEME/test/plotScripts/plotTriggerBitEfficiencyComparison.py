#!/usr/bin/env python

######################################################################
#
# This plot script is for comparing the trigger bit and weighting
# events with measured trigger efficiency. The python job
# configuration is signalAnalysis_cfg.py.
#
# Authors: Matti Kortelainen
#
######################################################################

import os
import array
import math

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.aux as aux

mcLumi = 20000.
era = "Run2012ABCD"

def main():
    effDir = "../multicrab_aodAnalysis_taumet_v53_3_131015_122226_triggerTestEff"
    bitDir = "."

    datasets = aux.MultiObject()
    datasets.add("eff", dataset.getDatasetsFromMulticrabCfg(directory=effDir, dataEra=era))
    datasets.add("bit", dataset.getDatasetsFromMulticrabCfg(directory=bitDir, dataEra=era))

    datasets.forEach(plots.mergeRenameReorderForDataMC)

    style = tdrstyle.TDRStyle()
    histograms.cmsTextMode = histograms.CMSMode.SIMULATION
    histograms.createLegend.setDefaults(y1=0.93, y2=0.8, x1=0.82, x2=0.93)
    histograms.createLegend.moveDefaults(dx=-0.05)
    plots._plotStyles["Ratio"].extend([styles.StyleMarker(markerColor=ROOT.kRed),
                                       styles.StyleLine(lineColor=ROOT.kRed)])
    plots._plotStyles["RatioLine"].extend([styles.StyleLine(lineColor=ROOT.kBlack)])

    plots.drawPlot.setDefaults(addLuminosityText=True)

    doPlots(*(datasets.getDataset("TTJets")))

def doPlots(effDataset, bitDataset):
    #print effDataset.files[0].GetName(), bitDataset.files[0].GetName()
    datasets = aux.MultiObject()
    datasets.add("eff", effDataset)
    datasets.add("bit", bitDataset)

    def doStyle(h, color):
        th = h.getRootHisto()
        th.SetLineColor(color)
        th.SetLineWidth(3)

    global plotIndex
    plotIndex = 1
    def createDrawPlot(name, **kwargs):
        drhs = datasets.getDatasetRootHisto(name)
        drhs[0].setName("Efficiency")
        drhs[1].setName("Bit")

        p = plots.ComparisonPlot(drhs[0], drhs[1])
        p.setEnergy(datasets.getEnergy())
        p.histoMgr.normalizeMCToLuminosity(mcLumi)
        p.histoMgr.forHisto("Efficiency", lambda h: doStyle(h, ROOT.kRed))
        p.histoMgr.forHisto("Bit", lambda h: doStyle(h, ROOT.kBlack))

        p.appendPlotObject(histograms.PlotText(0.8, 0.75, effDataset.getName(), size=17))

        global plotIndex
        filename = "%02d_%s" % (plotIndex, name.replace("/", "_"))
        plotIndex += 1

        plots.drawPlot(p, filename, ratio=True, ratioType="errorScale", ratioYlabel="Efficiency/Bit", **kwargs)

    ylabel1 = "Events / %.0f"
    ylabel2 = "Events / %.0f-%.0f"
    plots.drawPlot.setDefaults(ylabel=ylabel1)
    
    mtBinning = range(0, 100, 20) + [100, 125, 150, 175, 200, 400]

    steps = ["MET"]
    def createDrawCommonPlot(path, **kwargs):
        for step in steps:
            createDrawPlot(path%step, **kwargs)

    createDrawCommonPlot("CommonPlots/AtEveryStep/%s/tau_pT", xlabel="#tau p_{T}, GeV/c", rebinToWidthX=20)
    createDrawCommonPlot("CommonPlots/AtEveryStep/%s/MET_MET", rebinToWidthX=20)

    createDrawPlot("shapeTransverseMass", rebin=mtBinning, ylabel=ylabel2)
    createDrawPlot("shapeInvariantMass", rebin=4)

if __name__ == "__main__":
    main()
