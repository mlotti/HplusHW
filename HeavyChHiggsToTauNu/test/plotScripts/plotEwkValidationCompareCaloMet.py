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
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.systematics as systematics


def main():
    dirNormal = "../multicrab_signalAnalysisGenTauSkim_140814_211711"
    dirEmb = "."

    dsetsNormal = dataset.getDatasetsFromMulticrabCfg(directory=dirNormal, analysisName="signalAnalysisGenuineTau")
    dsetsNormalCut = dataset.getDatasetsFromMulticrabCfg(directory=dirNormal, analysisName="signalAnalysisGenuineTauCaloMet70")
    dsetsEmb = dataset.getDatasetsFromMulticrabCfg(directory=dirEmb, analysisName="signalAnalysisMIdEffTrgEffWTauMu")
    dsetsEmbCut = dataset.getDatasetsFromMulticrabCfg(directory=dirEmb, analysisName="signalAnalysisMIdEffTrgEffWTauMuCaloMet70")

    dsetsNormal.updateNAllEventsToPUWeighted()
    dsetsNormalCut.updateNAllEventsToPUWeighted()
    dsetsEmb.updateNAllEventsToPUWeighted()
    dsetsEmbCut.updateNAllEventsToPUWeighted()

    dsetsEmb.loadLuminosities()
    dsetsEmbCut.loadLuminosities()

    plots.mergeRenameReorderForDataMC(dsetsNormal)
    plots.mergeRenameReorderForDataMC(dsetsNormalCut)
    plots.mergeRenameReorderForDataMC(dsetsEmb)
    plots.mergeRenameReorderForDataMC(dsetsEmbCut)

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    histograms.cmsTextMode = histograms.CMSMode.SIMULATION_PRELIMINARY
    histograms.createLegend.setDefaults(y1=0.93, y2=0.8, x1=0.82, x2=0.93)
    histograms.uncertaintyMode.set(histograms.uncertaintyMode.StatOnly)
    histograms.createLegendRatio.moveDefaults(dx=-0.05, dh=-0.1)
    plots._legendLabels["BackgroundStatError"] = "Norm. stat. unc."

    if not os.path.exists("calometComparison"):
        os.mkdir("calometComparison")

    #doPlots(dsetsNormal.getDataset("TTJets"), dsetsEmb.getDataset("TTJets"), dsetsEmb.getDataset("Data").getLuminosity())
    doEffPlots(dsetsNormalCut.getDataset("TTJets"), dsetsNormal.getDataset("TTJets"), dsetsEmbCut.getDataset("TTJets"), dsetsEmb.getDataset("TTJets"), dsetsEmb.getDataset("Data").getLuminosity())

def doLineStyle(l):
    l.SetLineColor(ROOT.kBlue)
    l.SetLineWidth(2)
    l.SetLineStyle(ROOT.kDotted)
    return l


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
    
        p = plots.ComparisonManyPlot(drhNormal, [drhEmb])
        p.histoMgr.normalizeMCToLuminosity(lumi)
    
        p.histoMgr.forHisto("Normal ttbar", lambda h: doStyle(h, ROOT.kBlack))
        p.histoMgr.forHisto("Embedded ttbar", lambda h: doStyle(h, ROOT.kRed))
        p.histoMgr.forHisto("Embedded ttbar", lambda h: tauEmbedding.scaleTauBRNormalization(h.getRootHisto()))
    
        p.prependPlotObjectToRatio(doLineStyle(ROOT.TLine(0, 1.1, 500, 1.1)))
        p.prependPlotObjectToRatio(doLineStyle(ROOT.TLine(0, 0.9, 500, 0.9)))

        global ind
        ind += 1
        bins = range(0, 200, 20) + [200, 250, 300, 500]
        plots.drawPlot(p, "calometComparison/%02d_calomet_%s"%(ind, step), xlabel="Calo MET (GeV)", ylabel="Events / #DeltaMET / %.0f-%.0f GeV",
                       #rebinToWidthX=20,
                       rebin=bins, divideByBinWidth=True,
                       ratio=True, ratioYlabel="Emb./Norm.", ratioType="errorScale", ratioCreteLegend=True,
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

def doEffPlots(dsetNormalNum, dsetNormalDenom, dsetEmbNum, dsetEmbDenom, lumi):
    def doStyle(h, color, style=None):
        th = h.getRootHisto()
        th.SetLineColor(color)
        th.SetLineWidth(2)
        if style is not None:
            th.SetMarkerColor(color)
            th.SetMarkerStyle(style)
            th.SetMarkerSize(1)

    global ind
    ind = 0
    def compare(step):
        if step is None:
            path = "shapeTransverseMass"
        else:
            path = "CommonPlots/AtEveryStep/%s/MET_MET" % step

        #bins = range(0, 200, 20) + [200, 250, 300, 500]
        bins = systematics.getBinningForPlot("shapeTransverseMass")

        def getTH1(ds):
            drh = ds.getDatasetRootHisto(path)
            drh.normalizeToLuminosity(lumi)
            th1 = drh.getHistogram()
            #th1.Rebin(2)
            #return th1
            return th1.Rebin(len(bins)-1, th1.GetName(), array.array("d", bins))

        th1NormalNum = getTH1(dsetNormalNum)
        th1NormalDenom = getTH1(dsetNormalDenom)

        #print th1NormalNum.Integral(0, th1NormalNum.GetNbinsX()+1), th1NormalDenom.Integral(0, th1NormalDenom.GetNbinsX()+1)

        th1EmbNum = getTH1(dsetEmbNum)
        th1EmbDenom = getTH1(dsetEmbDenom)

        #print th1EmbNum.Integral(0, th1EmbNum.GetNbinsX()+1), th1EmbDenom.Integral(0, th1EmbDenom.GetNbinsX()+1)

        effNormal = ROOT.TGraphAsymmErrors(th1NormalNum, th1NormalDenom, "n")
        effEmb = ROOT.TGraphAsymmErrors(th1EmbNum, th1EmbDenom, "n")

        effNormal.SetName("Normal ttbar")
        effEmb.SetName("Embedded ttbar")

        p = plots.ComparisonManyPlot(effNormal, [effEmb])
        p.setLuminosity(lumi)
        p.histoMgr.forEachHisto(styles.generator())
        #p.histoMgr.forHisto("Normal ttbar", lambda h: doStyle(h, ROOT.kBlack, ROOT.kFullCircle))
        #p.histoMgr.forHisto("Embedded ttbar", lambda h: doStyle(h, ROOT.kRed, ROOT.kFullSquare))
        p.histoMgr.setHistoDrawStyleAll("EP")
        p.histoMgr.setHistoLegendStyleAll("EPL")

        unc1 = 1.12
        unc2 = 0.88
        p.prependPlotObjectToRatio(doLineStyle(ROOT.TLine(0, unc1, bins[-1], unc1)))
        p.prependPlotObjectToRatio(doLineStyle(ROOT.TLine(0, unc2, bins[-1], unc2)))
        p.appendPlotObject(histograms.PlotText(x=0.6, y=0.6, text="CaloMET > 70 GeV", size=20))

        global ind
        ind += 1
        # plots.drawPlot(p, "calometComparison/eff_%02d_calomet_%s"%(ind, step), xlabel="Type I PF MET (GeV)", ylabel="CaloMET cut efficiency",
        #                ratio=True, ratioYlabel="Norm./emb.", ratioType="errorScale",
        #                opts={"xmin": 0, "xmax": 500},
        #                opts2={"ymin": 0.8, "ymax": 1.2},
        #                addLuminosityText=True, moveLegend={"dx": -0.2, "dy": -0.5})


        plots.drawPlot(p, "calometComparison/eff_%d_calomet_shapeTransverseMass"%ind, xlabel="Transverse mass (GeV)", ylabel="CaloMET cut efficiency",
                       ratio=True, ratioYlabel="Emb./Norm.", ratioCreateLegend=True, ratioType="errorScale",
                       opts={"ymax": 1.2},
                       opts2={"ymin": 0.8, "ymax": 1.2},
                       addLuminosityText=True, moveLegend={"dx": -0.2, "dy": -0.5})


        # th1EmbNum.SetName("Numerator")
        # th1EmbDenom.SetName("Denominator")
        # p = plots.ComparisonPlot(th1EmbNum, th1EmbDenom)
        # p.histoMgr.forHisto("Numerator", lambda h: doStyle(h, ROOT.kBlack))
        # p.histoMgr.forHisto("Denominator", lambda h: doStyle(h, ROOT.kRed))
        # plots.drawPlot(p, "effdebug_emb_%02d_%s" %(ind, step), ratio=True)

        # th1NormalNum.SetName("Numerator")
        # th1NormalDenom.SetName("Denominator")
        # p = plots.ComparisonPlot(th1NormalNum, th1NormalDenom)
        # p.histoMgr.forHisto("Numerator", lambda h: doStyle(h, ROOT.kBlack))
        # p.histoMgr.forHisto("Denominator", lambda h: doStyle(h, ROOT.kRed))
        # plots.drawPlot(p, "effdebug_normal_%02d_%s" %(ind, step), ratio=True)


    # for step in [
    #     "JetSelection",
    #     "MET",
    #     "METPhiCorrected",
    #     "BTagging",
    #     "DeltaPhiBackToBack",
    #     "Selected"
    #     ]:
    #     compare(step)
    compare(None)


if __name__ == "__main__":
    main()
