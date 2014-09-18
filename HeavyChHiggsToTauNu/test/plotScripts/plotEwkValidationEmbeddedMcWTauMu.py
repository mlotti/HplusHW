#!/usr/bin/env python

######################################################################
#
# This plot script is for comparing the embedded MC and normal MC
# within signal analysis. The corresponding python job
# configurations are
# * tauAnalysis_cfg.py
# * signalAnalysis_cfg.py with "tauEmbeddingInput=1"
# * signalAnalysis_cfg.py with "doTauEmbeddingLikePreselection=1"
# for embedded signal analysis, and normal signal analysis,
# respectively
#
# The development scripts are
# * plotTauEmbeddingMcTauMcMany
# * plotTauEmbeddingMcSignalAnalysisMcMany
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
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.cutstring import * # And, Not, Or
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tauEmbedding as tauEmbedding
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.aux as aux

analysisEmb = "signalAnalysis"
#analysisSig = "signalAnalysisTauEmbeddingLikePreselection"
analysisSig = "signalAnalysis"

dataEra = "Run2012ABCD"
#optMode = None
#optMode = "OptQCDTailKillerLoosePlus"

def main():
#    dirEmb = "../embedding_mc_nooptmodes_140826_094514"
    dirEmb = "../embedding_mc_mtweightedfit_140822_101246"
    dirSig = "."

    for optMode in [
        "OptQCDTailKillerLoosePlus",
#        "OptQCDTailKillerMediumPlus",
#        "OptQCDTailKillerTightPlus",
#            None
        ]:
        datasetsEmb = dataset.getDatasetsFromMulticrabCfg(directory=dirEmb, dataEra=dataEra, analysisName=analysisEmb, optimizationMode=optMode)
        datasetsSig = dataset.getDatasetsFromMulticrabCfg(directory=dirSig, dataEra=dataEra, analysisName=analysisSig, optimizationMode=optMode)
        doDataset(datasetsEmb, datasetsSig, optMode)
        datasetsEmb.close()
        datasetsSig.close()

def doDataset(datasetsEmb, datasetsSig, optMode):
    global ind
    ind = 0

#    datasetsEmb.loadLuminosities() # not needed for pseudo-multicrab

    datasetsEmb.updateNAllEventsToPUWeighted()
    datasetsSig.updateNAllEventsToPUWeighted()

    plots.mergeRenameReorderForDataMC(datasetsEmb)
    plots.mergeRenameReorderForDataMC(datasetsSig)

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    histograms.cmsTextMode = histograms.CMSMode.SIMULATION
    histograms.cmsText[histograms.CMSMode.SIMULATION] = "Simulation"
    #histograms.createLegend.setDefaults(y1=0.93, y2=0.75, x1=0.52, x2=0.93)
    histograms.createLegend.moveDefaults(dx=-0.15, dh=-0.2)
    #histograms.uncertaintyMode.set(histograms.uncertaintyMode.StatOnly)
    #histograms.uncertaintyMode.set(histograms.uncertaintyMode.SystOnly)
    histograms.uncertaintyMode.set(histograms.uncertaintyMode.StatPlusSyst)
    histograms.createLegendRatio.moveDefaults(dh=-0.1, dx=-0.53)
    plots._legendLabels["BackgroundStatError"] = "Truth stat. unc."
    plots._legendLabels["BackgroundStatSystError"] = "Truth stat. unc."
    plots._plotStyles["BackgroundStatSystError"] = plots._plotStyles["BackgroundStatError"]

    plotter = tauEmbedding.CommonPlotter(optMode, "mcembwtaumu", drawPlotCommon)

    def dop(name, addData=False, **kwargs):
        doPlots(datasetsEmb, datasetsSig, name, plotter, optMode, addData, **kwargs)
#        doCounters(datasetsEmb, datasetsSig, name)

    dop("TTJets")
#drawPlotCommon = tauEmbedding.PlotDrawerTauEmbeddingEmbeddedNormal(ylabel="Events / %.0f GeV", stackMCHistograms=False, log=True, addMCUncertainty=True, ratio=True, addLuminosityText=True)
drawPlotCommon = plots.PlotDrawer(ylabel="Events / %.0f", stackMCHistograms=False, log=True, addMCUncertainty=True,
                                  ratio=True, ratioType="errorScale", ratioCreateLegend=True,
                                  opts2={"ymin": 0.85, "ymax": 1.15},
                                  addLuminosityText=True)

def strIntegral(th1):
    return "%.1f" % aux.th1Integral(th1)

def doPlots(datasetsEmb, datasetsSig, datasetName, plotter, optMode, addData, mtOnly=False):
    dsetEmb = datasetsEmb.getDataset(datasetName)
    dsetSig = datasetsSig.getDataset(datasetName)
    dsetEmbData = datasetsEmb.getDataset("Data")
    lumi = dsetEmbData.getLuminosity()

    syst = dataset.Systematics(shapes=["SystVarWTauMu"])

    addEventCounts = False
#    addEventCounts = True
    
    def createPlot(name):
        if mtOnly and "shapeTransverseMass" not in name:
            return None

        drhEmb = dsetEmb.getDatasetRootHisto(syst.histogram(name))
        drhSig = dsetSig.getDatasetRootHisto(name)
        drhEmb.normalizeToLuminosity(lumi)
        drhSig.normalizeToLuminosity(lumi)
        drhEmb.setName("Embedded")
        drhSig.setName("Normal")
        if addData:
            drhEmbData = dsetEmbData.getDatasetRootHisto(name)
            drhEmbData.setName("Embedded data")

        if addData:
            p = plots.ComparisonManyPlot(drhSig, [drhEmb, drhEmbData])
        else:
            p = plots.ComparisonManyPlot(drhSig, [drhEmb])
        p.setLuminosity(lumi)

        if True:
            # zero the stat uncertainty 
            th1 = p.histoMgr.getHisto("Embedded").getRootHistoWithUncertainties().getRootHisto()
            for b in xrange(0, th1.GetNbinsX()+1):
                th1.SetBinError(b, 0)

        legLabel = plots._legendLabels.get(datasetName, datasetName)
        #legEmb = "Embedded "+legLabel
        #legSig = "Normal "+legLabel
        legEmb = "W#rightarrow#tau#rightarrow#mu correction"
        legSig = "W#rightarrow#mu truth"
        if addEventCounts:
            legEmb += " ("+strIntegral(drhEmb.getHistogram())+")"
            legSig += " ("+strIntegral(drhSig.getHistogram())+")"
        p.histoMgr.setHistoLegendLabelMany({
                "Embedded": legEmb,
                "Normal": legSig,
                })
        p.histoMgr.forEachHisto(styles.generator())
        if addData:
            p.histoMgr.setHistoLegendLabelMany({"Embedded data": "Embedded data ("+strIntegral(drhEmbData.getHistogram())+")"})
            p.histoMgr.forHisto("Embedded data", styles.dataStyle)
            p.histoMgr.setHistoDrawStyle("Embedded data", "EP")
            p.histoMgr.setHistoLegendStyle("Embedded data", "P")
            p.histoMgr.reorderDraw(["Embedded data"])
        p.setDrawOptions(ratioYlabel="Corr./Truth")
        return p

    plotter.plot(datasetName, createPlot, {
        "NBjets": {"moveLegend": {"dx": -0.4, "dy": -0.45}},
        "shapeTransverseMass": {"moveLegend": {"dy": -0.12}}, #"ratioMoveLegend": {"dx": -0.3}}, 
        "shapeTransverseMass_log": {"moveLegend": {"dy": -0.12}},# "ratioMoveLegend": {"dx": -0.3}}
    })


if __name__ == "__main__":
    main()
