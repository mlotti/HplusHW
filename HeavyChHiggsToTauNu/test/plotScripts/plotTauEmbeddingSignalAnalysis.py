#!/usr/bin/env python

######################################################################
#
# This plot script is for comparing the embedded data to embedding MC
# within the signal analysis. The corresponding python job
# configuration is signalAnalysis_cfg.py with "doPat=1
# tauEmbeddingInput=1" command line arguments.
#
# Authors: Ritva Kinnunen, Matti Kortelainen
#
######################################################################

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles

# Configuration
analysis = "signalAnalysis"
#analysis = "signalAnalysisTauSelectionHPSTightTauBased"
counters = analysis+"Counters"

# Read the datasets
datasets = dataset.getDatasetsFromMulticrabCfg(counters=counters)
datasets.remove(["WJets_TuneD6T_Winter10", "TTJets_TuneD6T_Winter10","TTToHplusBWB_M120_Winter10"])
datasets.loadLuminosities()
plots.mergeRenameReorderForDataMC(datasets)

# Apply TDR style
style = tdrstyle.TDRStyle()

def deltaPhi(h, step="", rebin=5):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "#Delta#phi(#tau jet, MET) (rad)"
    ylabel = "Events / %.2f rad" % h.binWidth()
    
    h.stackMCHistograms()
    h.addMCUncertainty()

    name = "DeltaPhi_%s_log" % step
    h.createFrameFraction(name)
    #h.createFrame(name)
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.setLegend(histograms.createLegend())
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    h.addLuminosityText()
    h.save()

deltaPhi(plots.DataMCPlot(datasets, analysis+"/TauEmbeddingAnalysis_afterTauId_DeltaPhi"), step="afterTauId")

