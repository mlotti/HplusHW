#!/usr/bin/env python

######################################################################
#
# This plot script is for comparing the embedded MC and normal MC
# within tau ID and signal analysis. The corresponding python job
# configurations are
# * embeddingAnalysis_cfg.py
# * tauAnalysis_cfg.py
# * signalAnalysis_cfg.py with "doPat=1 tauEmbeddingInput=1"
# * signalAnalysis_cfg.py with "doTauEmbeddingLikePreselection=1"
# for embedding tauID, normal tauID, embedded signal analysis, and
# normal signal analysis, respecitvely
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


def main():
    dirNormal = "../multicrab_signalAnalysisGenTauSkim_140127_092222"
    dirEmb = "."

    dsetsNormal = dataset.getDatasetsFromMulticrabCfg(directory=dirNormal, analysisName="signalAnalysisGenuineTau")
    dsetsEmb = dataset.getDatasetsFromMulticrabCfg(directory=dirEmb, analysisName="signalAnalysisMIdEffTrgEffWTauMu")

    dsetsNormal.updateNAllEventsToPUWeighted()
    dsetsEmb.updateNAllEventsToPUWeighted()

    dsetsEmb.loadLuminosities()

    plots.mergeRenameReorderForDataMC(dsetsNormal)
    plots.mergeRenameReorderForDataMC(dsetsEmb)

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    histograms.cmsTextMode = histograms.CMSMode.SIMULATION
    histograms.cmsText[histograms.CMSMode.SIMULATION] = "Simulation"
    histograms.createLegend.setDefaults(y1=0.93, y2=0.8, x1=0.82, x2=0.93)

    doPlots(dsetsNormal.getDataset("TTJets"), dsetsEmb.getDataset("TTJets"), dsetsEmb.getDataset("Data").getLuminosity())

def doPlots(dsetNormal, dsetEmb, lumi):
    def doStyle(h, color):
        th = h.getRootHisto()
        th.SetLineColor(color)
        th.SetLineWidth(3)

    global ind
    ind = 0
    def compare(step):
        path = "CommonPlots/AtEveryStep/%s/MET_Calo" % step
        drhNormal = dsetNormal.getDatasetRootHisto(path)
        drhEmb = dsetEmb.getDatasetRootHisto(path)
    
        drhNormal.setName("Normal ttbar")
        drhEmb.setName("Embedded ttbar")
    
        p = plots.ComparisonPlot(drhNormal, drhEmb)
        p.histoMgr.normalizeMCToLuminosity(lumi)
    
        p.histoMgr.forHisto("Normal ttbar", lambda h: doStyle(h, ROOT.kBlack))
        p.histoMgr.forHisto("Embedded ttbar", lambda h: doStyle(h, ROOT.kRed))
        p.histoMgr.forHisto("Embedded ttbar", lambda h: tauEmbedding.scaleTauBRNormalization(h.getRootHisto()))
    
        global ind
        ind += 1
        bins = range(0, 200, 20) + [200, 250, 300, 500]
        plots.drawPlot(p, "%02d_calomet_%s"%(ind, step), xlabel="Calo MET (GeV)", ylabel="Events / #DeltaMET / %.0f-%.0f GeV",
                       #rebinToWidthX=20,
                       rebin=bins, divideByBinWidth=True,
                       ratio=True, ratioYlabel="Emb./norm.", ratioType="errorScale",
                       opts2={"ymin": 0.5, "ymax": 1.5},
                       addLuminosityText=True, moveLegend={"dx": -0.2})

    for step in [
        "VertexSelection",
        "TauSelection",
        "TauWeight",
        "ElectronVeto",
        "MuonVeto",
        "JetSelection",
        "MET",
        "METPhiCorrected",
        "BTagging",
        "DeltaPhiBackToBack",
        "Selected"]:
        compare(step)

if __name__ == "__main__":
    main()
