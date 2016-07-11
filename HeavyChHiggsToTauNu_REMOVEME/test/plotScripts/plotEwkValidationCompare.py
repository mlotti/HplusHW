#!/usr/bin/env python

######################################################################
#
# This plot script is for comparing the embedded MC and normal MC
# within signal analysis. The corresponding python job
# configurations are
# * signalAnalysis_cfg.py with "tauEmbeddingInput=1"
# for embedded signal analysis
#
# Authors: Matti Kortelainen
#
######################################################################

import os
import re
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
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tauEmbedding as tauEmbedding

analysisEmb = "signalAnalysis"
dataEra = "Run2012ABCD"

myStyles = [styles.getDataStyle()]
for st in styles.getStyles():
    myStyles.append(st)
    #myStyles.append(styles.StyleCompound([st, styles.StyleLine(lineStyle=2)]))

def main():
    dirSeeds = [
        "embedding_mc_seedTest1_fix_140807_103811",
        "embedding_mc_seedTest1_140807_084326"
        ]

    labels = [
        "Fixed",
        "Current"
        ]

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    histograms.createLegend.moveDefaults(dx=-0.02)
    histograms.uncertaintyMode.set(histograms.uncertaintyMode.StatOnly)
    histograms.createLegendRatio.moveDefaults(dh=-0.1, dx=-0.53)
    plots._legendLabels["BackgroundStatError"] = "Avg. stat. unc."

    for optMode in [
#        "OptQCDTailKillerZeroPlus",

#        "OptQCDTailKillerLoosePlus",
#        "OptQCDTailKillerMediumPlus",
#        "OptQCDTailKillerTightPlus",

#        "OptQCDTailKillerVeryTightPlus",

            None
        ]:
        datasetsSeeds = [
            dataset.getDatasetsFromMulticrabCfg(directory=d, dataEra=dataEra, analysisName=analysisEmb, optimizationMode=optMode) for d in dirSeeds
            ]
        doDataset(datasetsSeeds, optMode, labels)
        for d in datasetsSeeds:
            d.close()

drawPlotCommon = plots.PlotDrawer(ylabel="Events / %.0f", stackMCHistograms=False, log=True, addMCUncertainty=True,
                                  ratio=True, ratioType="errorScale", ratioCreateLegend=True,
                                  addLuminosityText=True)

def doDataset(datasetsSeeds, optMode, labels):
    for d in datasetsSeeds:
        d.updateNAllEventsToPUWeighted()
        plots.mergeRenameReorderForDataMC(d)

    plotter = tauEmbedding.CommonPlotter(optMode, "average", drawPlotCommon)

    doPlots(datasetsSeeds, labels, "Data", plotter)
    doPlots(datasetsSeeds, labels, "TTJets", plotter)


def doPlots(datasetsSeeds, labels, datasetName, plotter):
    dsetSeeds = [d.getDataset(datasetName) for d in datasetsSeeds]
    lumi = datasetsSeeds[0].getDataset("Data").getLuminosity()

    addEventCounts = False
    addEventCounts = True

    def createPlot(name):
        drhSeeds = []
        for i, d in enumerate(dsetSeeds):
            drh = d.getDatasetRootHisto(name)
            drh.setName("Seed %d" % i)
            if drh.isMC():
                drh.normalizeToLuminosity(lumi)
            drhSeeds.append(drh)

        p = plots.ComparisonManyPlot(drhSeeds[0], drhSeeds[1:])
        p.setLuminosity(lumi)
        legLabel = plots._legendLabels.get(datasetName, datasetName)
        for i, drh in enumerate(drhSeeds):
            leg = labels[i]+" "+legLabel
            if addEventCounts:
                leg += " ("+tauEmbedding.strIntegral(drh.getHistogram())+")"
            p.histoMgr.setHistoLegendLabelMany({"Seed %d"%i: leg})
        p.histoMgr.forEachHisto(styles.Generator(styles=myStyles))

        p.setDrawOptions(ratioYlabel="Others/"+labels[0])
        return p

    plotter.plot(datasetName, createPlot)

if __name__ == "__main__":
    main()

