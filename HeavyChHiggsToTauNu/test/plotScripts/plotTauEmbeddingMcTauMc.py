#!/usr/bin/env python

######################################################################
#
# This plot script is for comparing the embedded MC to normal MC
# within the tau ID. The corresponding python job
# configurations are
# * embeddingAnalysis_cfg.py
# * tauAnalysis_cfg.py
#
# Author: Matti Kortelainen
#
######################################################################

import math, array, os

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect
import plotTauEmbeddingMcSignalAnalysisMc as tauEmbedding
import plotTauEmbeddingTau as tauPlot

analysisEmb = "tauNtuple"
analysisSig = "tauNtuple"

dirEmb = "."
dirSig = "../multicrab_analysisTau_111202_144918"


def main():
    datasetsEmb = dataset.getDatasetsFromMulticrabCfg(cfgfile=dirEmb+"/multicrab.cfg", counters=analysisEmb+"Counters")
    datasetsSig = dataset.getDatasetsFromMulticrabCfg(cfgfile=dirSig+"/multicrab.cfg", counters=analysisSig+"Counters")

    datasetsEmb.loadLuminosities()
    plots.mergeRenameReorderForDataMC(datasetsEmb)
    plots.mergeRenameReorderForDataMC(datasetsSig)

    style = tdrstyle.TDRStyle()
    histograms.createLegend.setDefaults(y1=0.9, y2=0.75, x1=0.6, x2=0.95)

    tauEmbedding.normalize=False
    tauEmbedding.era="Run2011A"

    doPlots(datasetsEmb, datasetsSig, "TTJets")
    doPlots(datasetsEmb, datasetsSig, "WJets")

def doPlots(datasetsEmb, datasetsSig, datasetName):
    lumi = datasetsEmb.getDataset("Data").getLuminosity()

    plots._legendLabels[datasetName+"_Embedded"] = "Embedded "+plots._legendLabels[datasetName]
    plots._legendLabels[datasetName+"_Normal"]   = "Normal "+plots._legendLabels[datasetName]

    def createPlot(name):
        name2Emb = name
        name2Sig = name
        if isinstance(name, basestring):
            name2Emb = analysisEmb+"/"+name
            name2Sig = analysisSig+"/"+name
        else:
            name2Emb = name.clone(tree=analysisEmb+"/tree")
            name2Sig = name.clone(tree=analysisSig+"/tree")
        emb = datasetsEmb.getDataset(datasetName).getDatasetRootHisto(name2Emb)
        emb.setName("Embedded")
        sig = datasetsSig.getDataset(datasetName).getDatasetRootHisto(name2Sig)
        sig.setName("Normal")
        p = plots.ComparisonPlot(emb, sig)
        p.histoMgr.normalizeMCToLuminosity(lumi)
        p.histoMgr.setHistoLegendLabelMany({
                "Embedded": "Embedded "+plots._legendLabels[datasetName],
                "Normal":   "Normal "+plots._legendLabels[datasetName],
                })
        p.histoMgr.forEachHisto(styles.generator())

        return p

    treeDraw = dataset.TreeDraw("dummy")

    opts2 = {"ymin": 0, "ymax": 2}
    def drawPlot(plot, name, *args, **kwargs):
        tauEmbedding.drawPlot(plot, "mcembsig_"+datasetName+"_"+name, *args, **kwargs)

    # Decay mode finding
    td=treeDraw.clone(selection="&&".join([tauPlot.decayModeFinding, tauPlot.tightIsolation]))
    postfix = "_1AfterDecayModeFindingIsolation"
    drawPlot(createPlot(td.clone(varexp="taus_p4.Pt()>>tmp(25,0,250)")),
             "tauPt"+postfix, "#tau-jet candidate p_{T} (GeV/c)", cutLine=40)
    drawPlot(createPlot(td.clone(varexp="taus_decayMode>>tmp(16,0,16)")),
             "tauDecayMode"+postfix+"_check", "", opts={"nbins":16}, opts2={"ymin":0.9, "ymax":1.4}, function=tauPlot.decayModeCheckCustomize)
    drawPlot(createPlot(td.clone(varexp=tauPlot.decayModeExp)),
             "tauDecayMode"+postfix+"", "", opts={"ymin": 1, "ymaxfactor": 20, "nbins":5}, opts2={"ymin":0.9, "ymax":1.4}, moveLegend={"dy": 0.02, "dh": -0.02}, function=tauPlot.decayModeCustomize)

    # Pt
    postfix = "_2AfterPtCut"
    td=treeDraw.clone(selection="&&".join([tauPlot.decayModeFinding, tauPlot.tightIsolation, tauPlot.tauPtCut]))
    drawPlot(createPlot(td.clone(varexp=tauPlot.decayModeExp)),
             "tauDecayMode"+postfix+"", "", opts={"ymin": 1, "ymaxfactor": 20, "nbins":5}, opts2={"ymin":0.9, "ymax":1.4}, moveLegend={"dy": 0.02, "dh": -0.02}, function=tauPlot.decayModeCustomize)
    drawPlot(createPlot(td.clone(varexp="taus_p4.Eta()>>tmp(25,-2.5,2.5")),
             "tauEta"+postfix, "#tau-jet candidate #eta", ylabel="Events / %.1f", opts={"ymin": 1e-1}, moveLegend={"dx": -0.2, "dy": -0.45}, cutLine=[-2.1, 2.1])
    drawPlot(createPlot(td.clone(varexp="taus_p4.Phi()>>tmp(32,-3.2,3.2")),
             "tauPhi"+postfix, "#tau-jet candidate #phi (rad)", ylabel="Events / %.1f", opts={"ymin": 1e-1}, moveLegend={"dx": -0.2, "dy": -0.45})


    # Eta
    td=treeDraw.clone(selection="&&".join([tauPlot.decayModeFinding, tauPlot.tightIsolation, tauPlot.tauPtCut, tauPlot.tauEtaCut]))
    postfix = "_3AfterEtaCut"
    drawPlot(createPlot(td.clone(varexp="taus_leadPFChargedHadrCand_p4.Pt()>>tmp(25,0,250)")),
             "tauLeadingTrackPt"+postfix, "#tau-jet ldg. charged particle p_{T} (GeV/c)", opts2={"ymin":0, "ymax": 2}, cutLine=20)

    # Tau candidate selection
    td=treeDraw.clone(selection=tauPlot.tauCandidateSelection)
    postfix = "_4AfterTauCandidateSelection"
    drawPlot(createPlot(td.clone(varexp=tauPlot.decayModeExp)),
             "tauDecayMode"+postfix+"", "", opts={"ymin": 1e-2, "ymaxfactor": 20, "nbins":5}, opts2={"ymin":0, "ymax":2}, moveLegend={"dy": 0.02, "dh": -0.02}, function=tauPlot.decayModeCustomize)

    # Isolation + one prong
    td = treeDraw.clone(selection="&&".join([tauPlot.tauCandidateSelection, tauPlot.oneProng]))
    postfix = "_5AfterOneProng"
    drawPlot(createPlot(td.clone(varexp="taus_p4.Pt()>>tmp(25,0,250)")),
             "tauPt"+postfix, "#tau-jet candidate p_{T} (GeV/c)", opts2={"ymin": 0, "ymax": 2})
    drawPlot(createPlot(td.clone(varexp="taus_p4.P()>>tmp(25,0,250)")),
             "tauP"+postfix, "#tau-jet candidate p (GeV/c)", opts2={"ymin": 0, "ymax": 2})
    drawPlot(createPlot(td.clone(varexp="taus_leadPFChargedHadrCand_p4.Pt()>>tmp(25,0,250)")),
             "tauLeadingTrackPt"+postfix, "#tau-jet ldg. charged particle p_{T} (GeV/c)", opts2={"ymin":0, "ymax": 2})
    drawPlot(createPlot(td.clone(varexp="taus_leadPFChargedHadrCand_p4.P()>>tmp(25,0,250)")),
             "tauLeadingTrackP"+postfix, "#tau-jet ldg. charged particle p (GeV/c)", opts2={"ymin":0, "ymax": 2})
    drawPlot(createPlot(td.clone(varexp=tauPlot.rtauExp+">>tmp(22, 0, 1.1)")),
             "rtau"+postfix, "R_{#tau} = p^{ldg. charged particle}/p^{#tau jet}", ylabel="Events / %.1f", opts={"ymin": 1e-2, "ymaxfactor": 5}, moveLegend={"dx":-0.4}, cutLine=0.7)

    # Full id
    td = treeDraw.clone(selection="&&".join([tauPlot.tauCandidateSelection, tauPlot.tauID]))
    postfix = "_6AfterTauID"
    drawPlot(createPlot(td.clone(varexp=tauPlot.decayModeExp)),
             "tauDecayMode"+postfix+"", "", opts={"ymin": 1e-2, "ymaxfactor": 20, "nbins":5}, opts2={"ymin":0, "ymax":3}, moveLegend={"dy": 0.02, "dh": -0.02}, function=tauPlot.decayModeCustomize)

    


if __name__ == "__main__":
    main()
