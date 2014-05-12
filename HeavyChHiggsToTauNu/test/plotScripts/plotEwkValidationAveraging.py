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
    dirAve = "."
    # dirSeeds = []
    # inputInfoPath = os.path.join(dirAve, "inputInfo.txt")
    # f = open(inputInfoPath)
    # input_re = re.compile("Embedded input directory: (?P<dir>\S+)")
    # for line in f:
    #     m = input_re.search(line)
    #     if m:
    #         dirSeeds.append(os.path.join("..", m.group("dir")))
    # f.close()
    # if len(dirSeeds) == 0:
    #     raise Exception("Found 0 input directories from %s" % inputInfoPath)
    dirSeeds = [
#        "../embedding_mc_140327_122732",
#        "../embedding_seedTest1_140326_114053",
#        "../embedding_seedTest2_140414_121814",
#        "../embedding_seedTest3_140414_122132",
#        "../embedding_seedTest4_140414_122827",
        "../embedding_140509_100532",
        "../embedding_seedTest1_140508_154221",
        "../embedding_seedTest2_140508_154540",
        "../embedding_seedTest3_140508_155055",
        "../embedding_seedTest4_140508_155742"
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
        datasetsAve = dataset.getDatasetsFromMulticrabCfg(directory=dirAve, dataEra=dataEra, analysisName=analysisEmb, optimizationMode=optMode)
        datasetsSeeds = [
            dataset.getDatasetsFromMulticrabCfg(directory=d, dataEra=dataEra, analysisName=analysisEmb, optimizationMode=optMode) for d in dirSeeds
            ]
        doDataset(datasetsAve, datasetsSeeds, optMode)
        datasetsAve.close()
        for d in datasetsSeeds:
            d.close()

drawPlotCommon = plots.PlotDrawer(ylabel="Events / %.0f", stackMCHistograms=False, log=True, addMCUncertainty=True,
                                  ratio=True, ratioType="errorScale", ratioCreateLegend=True,
                                  addLuminosityText=True)

def doDataset(datasetsAve, datasetsSeeds, optMode):
    ds = [datasetsAve]+datasetsSeeds

    for d in ds:
        d.updateNAllEventsToPUWeighted()
        plots.mergeRenameReorderForDataMC(d)

    plotter = tauEmbedding.CommonPlotter(optMode, "average", drawPlotCommon)

    doPlots(datasetsAve, datasetsSeeds, "Data", plotter)


def doPlots(datasetsAve, datasetsSeeds, datasetName, plotter):
    dsetAve = datasetsAve.getDataset(datasetName)
    dsetSeeds = [d.getDataset(datasetName) for d in datasetsSeeds]
    lumi = datasetsAve.getDataset("Data").getLuminosity()

    addEventCounts = False

    def createPlot(name):
        drhAve = dsetAve.getDatasetRootHisto(name)
        drhAve.setName("Average")
        drhSeeds = []
        for i, d in enumerate(dsetSeeds):
            drh = d.getDatasetRootHisto(name)
            drh.setName("Seed %d" % i)
            drhSeeds.append(drh)

        p = plots.ComparisonManyPlot(drhAve, drhSeeds)
        p.setLuminosity(lumi)
        legLabel = plots._legendLabels.get(datasetName, datasetName)
        leg = "Average "+legLabel
        if addEventCounts:
            leg += " ("+tauEmbedding.strIntegral(drhAve.getHistogram())+")"
        p.histoMgr.setHistoLegendLabelMany({"Average": leg})
        for i, drh in enumerate(drhSeeds):
            leg = ("Seed %d "%i)+legLabel
            if addEventCounts:
                leg += " ("+tauEmbedding.strIntegral(drh.getHistogram())+")"
            p.histoMgr.setHistoLegendLabelMany({"Seed %d"%i: leg})
        p.histoMgr.forEachHisto(styles.Generator(styles=myStyles))

        p.setDrawOptions(ratioYlabel="Seed/Average")
        return p

    plotter.plot(datasetName, createPlot)


if __name__ == "__main__":
    main()

