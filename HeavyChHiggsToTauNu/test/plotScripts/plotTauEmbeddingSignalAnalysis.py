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

# main function
def main():
    # Read the datasets
    datasets = dataset.getDatasetsFromMulticrabCfg(counters=counters)
    datasets.remove(["WJets_TuneD6T_Winter10", "TTJets_TuneD6T_Winter10","TTToHplusBWB_M120_Winter10"])
    datasets.loadLuminosities()
    plots.mergeRenameReorderForDataMC(datasets)

    # Apply TDR style
    style = tdrstyle.TDRStyle()

    # Create the plot objects and pass them to the formatting
    # functions to be formatted, drawn and saved to files
    tauPt(plots.DataMCPlot(datasets, analysis+"/TauEmbeddingAnalysis_afterTauId_selectedTauPt"), ratio=True)
    tauEta(plots.DataMCPlot(datasets, analysis+"/TauEmbeddingAnalysis_afterTauId_selectedTauEta"), ratio=True)
    tauPhi(plots.DataMCPlot(datasets, analysis+"/TauEmbeddingAnalysis_afterTauId_selectedTauPhi"), ratio=True)
    leadingTrack(plots.DataMCPlot(datasets, analysis+"/TauEmbeddingAnalysis_afterTauId_leadPFChargedHadrPt"), ratio=True)
    rtau(plots.DataMCPlot(datasets, analysis+"/TauID_RtauCut"), "TauIdRtau_afterTauId")

    muonPt(plots.DataMCPlot(datasets, analysis+"/TauEmbeddingAnalysis_begin_originalMuonPt"), ratio=True)
    muonPt(plots.DataMCPlot(datasets, analysis+"/TauEmbeddingAnalysis_afterTauId_originalMuonPt"), ratio=True)
    muonPt(plots.DataMCPlot(datasets, analysis+"/TauEmbeddingAnalysis_afterMetCut_originalMuonPt"), ratio=True)
    
    muonEta(plots.DataMCPlot(datasets, analysis+"/TauEmbeddingAnalysis_begin_originalMuonEta"), ratio=True)
    muonEta(plots.DataMCPlot(datasets, analysis+"/TauEmbeddingAnalysis_afterTauId_originalMuonEta"), ratio=True)
    muonEta(plots.DataMCPlot(datasets, analysis+"/TauEmbeddingAnalysis_afterMetCut_originalMuonEta"), ratio=True)

    met(plots.DataMCPlot(datasets, analysis+"/TauEmbeddingAnalysis_begin_originalMet"), ratio=True)
    met(plots.DataMCPlot(datasets, analysis+"/TauEmbeddingAnalysis_afterTauId_originalMet"), ratio=True)
    met(plots.DataMCPlot(datasets, analysis+"/TauEmbeddingAnalysis_afterTauId_embeddingMet"), ratio=True)
    met(plots.DataMCPlot(datasets, analysis+"/TauEmbeddingAnalysis_begin_embeddingMet"), ratio=True)

    deltaPhi(plots.DataMCPlot(datasets, analysis+"/TauEmbeddingAnalysis_afterTauId_DeltaPhi"))
    deltaPhi(plots.DataMCPlot(datasets, analysis+"/TauEmbeddingAnalysis_afterTauId_DeltaPhiOriginal"))

    transverseMass(plots.DataMCPlot(datasets, analysis+"/TauEmbeddingAnalysis_afterTauId_TransverseMass"))
    transverseMass(plots.DataMCPlot(datasets, analysis+"/TauEmbeddingAnalysis_afterTauId_TransverseMassOriginal"))

    jetPt(plots.DataMCPlot(datasets, analysis+"/jet_pt"), "jetPt")
    jetEta(plots.DataMCPlot(datasets, analysis+"/jet_eta"), "jetEta")
    jetPhi(plots.DataMCPlot(datasets, analysis+"/jet_phi"), "jetPhi")
    numberOfJets(plots.DataMCPlot(datasets, analysis+"/NumberOfSelectedJets"), "NumberOfJets")

    jetPt(plots.DataMCPlot(datasets, analysis+"/bjet_pt"), "bjetPt", rebin=10)
    jetEta(plots.DataMCPlot(datasets, analysis+"/bjet_eta"), "bjetEta", rebin=10)
#    jetPhi(plots.DataMCPlot(datasets, analysis+"/bjet_phi"), "bjetPhi", rebin=10)
    numberOfJets(plots.DataMCPlot(datasets, analysis+"/NumberOfBtaggedJets"), "NumberOfBJets")

# Helper function to flip the last two parts of the histogram name
# e.g. ..._afterTauId_DeltaPhi -> DeltaPhi_afterTauId
def flipName(name):
    tmp = name.split("_")
    return tmp[-1] + "_" + tmp[-2]

# Common formatting
def common(h, xlabel, ylabel):
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    h.addLuminosityText()
    h.save()

# Functions below are for plot-specific formattings. They all take the
# plot object as an argument, then apply some formatting to it, draw
# it and finally save it to files.
def tauPt(h, rebin=5, ratio=True):
    name = flipName(h.getRootHistoPath())

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "#p_{T}^{#tau jet} (GeV/c)"
    ylabel = "Events / %.0f GeV/c" % h.binWidth()

    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.01, "ymaxfactor": 2}
    opts2 = {"ymin": 0.5, "ymax": 1.5}
    name = name+"_log"
    #h.createFrameFraction(name, opts=opts)
#    h.createFrame(name, opts=opts)
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)
    
def tauEta(h, rebin=5, ratio=True):
    name = flipName(h.getRootHistoPath())

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "#eta^{#tau jet}"
    ylabel = "Events"

    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.01, "ymaxfactor": 2}
    opts2 = {"ymin": 0.5, "ymax": 1.5}

    name = name+"_log"
    #h.createFrameFraction(name, opts=opts)
#    h.createFrame(name, opts=opts)
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)
    
def tauPhi(h, rebin=5, ratio=True):
    name = flipName(h.getRootHistoPath())

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "#phi^{#tau jet}"
    ylabel = "Events"

    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.01, "ymaxfactor": 2}
    opts2 = {"ymin": 0.5, "ymax": 1.5}

    name = name+"_log"
    #h.createFrameFraction(name, opts=opts)
#    h.createFrame(name, opts=opts)
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend(0.2, 0.6, 0.4, 0.9))
    common(h, xlabel, ylabel)
    
def leadingTrack(h, rebin=5, ratio=True):
    name = flipName(h.getRootHistoPath())

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "p_{T}^{leading track} (GeV/c)"
    ylabel = "Events / %.0f GeV/c" % h.binWidth()

    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.01, "ymaxfactor": 2}

    name = name+"_log"
    #h.createFrameFraction(name, opts=opts)
    h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)

def rtau(h, name, rebin=2, ratio=True):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "R_{#tau}"
    ylabel = "Events / %.2f" % h.binWidth()

    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.01, "ymaxfactor": 10}
    opts2 = {"ymin": 0.5, "ymax": 1.5}
    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
#    h.createFrame(name, opts=opts)
    #h.createFrameFraction(name, opts=opts)
    h.getPad().SetLogy(True)
    #h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)

def muonPt(h, rebin=5, ratio=False):
    name = flipName(h.getRootHistoPath())

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "p_{T}^{#mu} (GeV/c)"
    ylabel = "Events / %.0f GeV" % h.binWidth()

    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.01, "ymaxfactor": 2}
    opts2 = {"ymin": 0.5, "ymax": 1.5}

    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)
    
def muonEta(h, rebin=5, ratio=False):
    name = flipName(h.getRootHistoPath())

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "#eta^{#mu}"
    ylabel = "Events"

    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.01, "ymaxfactor": 2}
    opts2 = {"ymin": 0.5, "ymax": 1.5}

    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)

def met(h, rebin=20, ratio=True):
    name = flipName(h.getRootHistoPath())

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "MET (GeV)"
    if "embedding" in name:
        xlabel = "Embedded "+xlabel
    elif "original" in name:
        xlabel = "Original "+xlabel
    ylabel = "Events / %.0f GeV" % h.binWidth()

    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.001, "ymaxfactor": 2}
    opts2 = {"ymin": 0.5, "ymax": 1.5}

    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)

def deltaPhi(h, rebin=40):
    name = flipName(h.getRootHistoPath())

    particle = "#tau jet"
    if "Original" in name:
        particle = "#mu"

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "#Delta#phi(%s, MET) (rad)" % particle
    ylabel = "Events / %.2f rad" % h.binWidth()
    
    h.stackMCHistograms()
    h.addMCUncertainty()

    #h.createFrameFraction(name)
    h.createFrame(name)
    h.setLegend(histograms.createLegend(0.2, 0.6, 0.4, 0.9))
    common(h, xlabel, ylabel)

def transverseMass(h, rebin=10):
    name = flipName(h.getRootHistoPath())

    particle = ""
    if "Original" in name:
        particle = "#mu"
        name = name.replace("TransverseMass", "Mt")
    else:
        particle = "#tau jet"
        name = name.replace("TransverseMass", "MtEmbedding")

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "m_{T}(%s, MET) (GeV/c^{2})" % particle
    ylabel = "Events / %.2f GeV/c^{2}" % h.binWidth()
    
    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"xmax": 200}

    #h.createFrameFraction(name, opts=opts)
    h.createFrame(name, opts=opts)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)
    
def jetPt(h, name, rebin=2, ratio=True):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    particle = "jet"
    if "bjet" in name:
        particle = "bjet"
#        name = name.replace("jetPt", "bjetPt")

    xlabel = "p_{T}^{%s} (GeV/c)" % particle
    ylabel = "Events /%.0f GeV/c" % h.binWidth()

    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.01, "ymaxfactor": 10}
    opts2 = {"ymin": 0.5, "ymax": 1.5}
    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
#    h.createFrame(name, opts=opts)
    #h.createFrameFraction(name, opts=opts)
    h.getPad().SetLogy(True)
    #h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)

    
def jetEta(h, name, rebin=2, ratio=True):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    particle = "jet"
    if "bjet" in name:
        particle = "bjet"
    xlabel = "#eta^{%s}" % particle
    ylabel = "Events / %.2f" % h.binWidth()

    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 10.0, "ymaxfactor": 5}
    opts2 = {"ymin": 0.5, "ymax": 1.5}
    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)

def jetPhi(h, name, rebin=2, ratio=True):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    particle = "jet"
    if "bjet" in name:
        particle = "bjet"
    xlabel = "#phi^{%s}" % particle
    ylabel = "Events / %.2f" % h.binWidth()

    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 10.0, "ymaxfactor": 5}
    opts2 = {"ymin": 0.5, "ymax": 1.5}
    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)

def numberOfJets(h, name, rebin=1, ratio=True):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    particle = "jet"
    if "Btagged" in name:
        particle = "bjet"
    xlabel = "Number of %ss" % particle
    ylabel = "Events / %.2f" % h.binWidth()

    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.0, "ymaxfactor": 1.2}
    opts2 = {"ymin": 0.5, "ymax": 1.5}
#    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
#    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)
    
# Call the main function if the script is executed (i.e. not imported)
if __name__ == "__main__":
    main()
