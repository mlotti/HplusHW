#!/usr/bin/env python

######################################################################
#
# This plot script is for comparing the embedded data to normal MC
# within the signal analysis. The corresponding python job
# configurations are
# * signalAnalysis_cfg.py with "doPat=1 tauEmbeddingInput=1"
# * signalAnalysis_cfg.py
# for embedding+signal analysis and signal analysis, respectively
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

#embeddingSignalAnalysis = "."
#signalAnalysis = "../../multicrab_110307_141642"
embeddingSignalAnalysis = "multicrab_signalAnalysis_110303_154128"
signalAnalysis = "multicrab_110307_141642"

# main function
def main():
    # Read the datasets
    # Take only TT+W from signal analysis, and data from embedding+signal analysis
    datasetsEmbSig = dataset.getDatasetsFromMulticrabCfg(cfgfile=embeddingSignalAnalysis+"/multicrab.cfg", counters=counters)
    datasetsSig = dataset.getDatasetsFromMulticrabCfg(cfgfile=signalAnalysis+"/multicrab.cfg", counters=counters)

    datasetsEmbSig.loadLuminosities()
    datasetsEmbSig.selectAndReorder(datasetsEmbSig.getDataDatasetNames())
    datasetsSig.selectAndReorder(["TTJets_TuneZ2_Winter10", "WJets_TuneZ2_Winter10"])
    datasets = datasetsEmbSig
    datasets.extend(datasetsSig)

    plots.mergeRenameReorderForDataMC(datasets)

    # Apply TDR style
    style = tdrstyle.TDRStyle()


    met(plots.DataMCPlot(datasets, analysis+"/TauEmbeddingAnalysis_begin_embeddingMet"), step="begin")
    #met(plots.DataMCPlot(datasets, analysis+"/TauEmbeddingAnalysis_begin_embeddingMet", normalizeToOne=True), step="begin2")

# Functions below are for plot-specific formattings. They all take the
# plot object as an argument, then apply some formatting to it, draw
# it and finally save it to files.
def met(h, step="", rebin=5):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "Met (GeV)"
    ylabel = "Events / %.0f GeV" % h.binWidth()
    opts = {"ymaxfactor": 2}
    
    h.stackMCHistograms()
    h.addMCUncertainty()

    if h.normalizeToOne:
        ylabel = "A.u."
        opts["yminfactor"] = 1e-5
    else:
        opts["ymin"] = 0.001
           

    name = "MetSimulateEmbedded_%s_log" % step
    h.createFrameFraction(name, opts=opts)
    #h.createFrame(name, opts=opts)
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.setLegend(histograms.createLegend())
    ROOT.gPad.SetLogy(True)
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    #h.addLuminosityText()
    h.save()

# Call the main function if the script is executed (i.e. not imported)
if __name__ == "__main__":
    main()

