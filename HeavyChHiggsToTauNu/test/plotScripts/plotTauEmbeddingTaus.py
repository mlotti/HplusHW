#!/usr/bin/env python

import os
import re
from array import array

import ROOT
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles

ROOT.gROOT.SetBatch(True)

#histograms.textDefaults.setEnergyDefaults(x=0.17)
#histograms.textDefaults.setCmsPreliminaryDefaults(x=0.6)

createLegend = histograms.createLegend
createLegend.setDefaults(x1=0.5, y1=0.8, y2=0.9,
                         textSize=0.03,
                         borderSize=0)

#embeddingDir = "multicrab_analysis_110328_175023"
embeddingDir = "multicrab_analysis_110407_161105"
#tauDir = "multicrab_analysisTau_110328_175424"
tauDir = "multicrab_analysisTau_110407_132703"


embeddingAnalysis = "EmbeddingAnalyzer"
#embeddingAnalysis = "EmbeddingAnalyzer/matched"
#tauAnalysis = "GenPt30Eta21TauAnalyzer/matched"
#tauAnalysis = "Jets3GenPt30Eta21TauAnalyzer/matched"
tauAnalysis = "Jets3GenPt30Eta21TauAnalyzer"


embeddingData = True
embeddingData = False
mcSample = "WJets"
#mcSample = "TTJets"

dataLabel = "Data"
mcLabel = plots._legendLabels[mcSample]+" MC"

saveFormats = [
    ".png",
#    ".eps",
#    ".C",
]

def main():
    # Datasets
    datasetsEmbedding = dataset.getDatasetsFromMulticrabCfg(cfgfile=embeddingDir+"/multicrab.cfg", counters=None)
    datasetsTau = dataset.getDatasetsFromMulticrabCfg(cfgfile=tauDir+"/multicrab.cfg", counters=None)

    datasetsEmbedding.loadLuminosities()
    plots.mergeRenameReorderForDataMC(datasetsEmbedding)
    plots.mergeRenameReorderForDataMC(datasetsTau)

    if embeddingData:
        datasetsEmbedding.selectAndReorder(["Data"])
    else:
        datasetsEmbedding.selectAndReorder([mcSample])
    datasetsTau.selectAndReorder([mcSample])

    # Style
    style = tdrstyle.TDRStyle()
    
    def createMuonTauPlot(nameMuon, nameTau):
        return MuonTauPlot(datasetsEmbedding, datasetsTau, embeddingAnalysis, tauAnalysis, nameMuon, nameTau)

    def createTauPlot(nameTau):
        return TauPlot(datasetsEmbedding, datasetsTau, embeddingAnalysis, tauAnalysis, nameTau)

    # Plots
    plotPt(createMuonTauPlot("Muon_Pt", "GenTau_Pt"), opts={"xmin":30, "ymin":5e-4})
    plotPt(createTauPlot("Tau_Pt"))

    plotEta(createMuonTauPlot("Muon_Eta", "GenTau_Eta"), opts={"xmin":-2.1, "xmax": 2.1})
    plotEta(createTauPlot("Tau_Eta"), opts={"xmin":-2.4, "xmax":2.4})

    plotPhi(createMuonTauPlot("Muon_Phi", "GenTau_Phi"))
    plotPhi(createTauPlot("Tau_Phi"))


class MuonTauPlot(plots.ComparisonPlot):
    def __init__(self, datasets, datasetsTau, directory, directoryTau, name, nameTau):
        h = datasets.getDatasetRootHistos(directory+"/"+name)[0]
        h.setName(name+"Embedded")
        hTau = datasetsTau.getDatasetRootHistos(directoryTau+"/"+nameTau)[0]
        hTau.setName(nameTau+"Tau")
        plots.ComparisonPlot.__init__(self, h, hTau, saveFormats=saveFormats)

        self.histoMgr.normalizeToOne()
        self.histoMgr.forEachHisto(styles.generator())

        self.embeddingAnalysis = directory.replace("/", "_")
        self.tauAnalysis = directoryTau.replace("/", "_")

        self.plotName = mcSample+"_"+self.embeddingAnalysis+"_"+name+"_"+self.tauAnalysis+"_"+nameTau
        self.ratioLabel = "Selected #mu/gen #tau"

        label = dataLabel
        if not embeddingData:
            label = mcLabel

        self.histoMgr.setHistoLegendLabelMany({name+"Embedded": "Selected #mu (%s)"%label,
                                               nameTau+"Tau": "Gen #tau (%s)"%mcLabel})

class TauPlot(plots.ComparisonPlot):
    def __init__(self, datasets, datasetsTau, directory, directoryTau, name):
        h = datasets.getDatasetRootHistos(directory+"/"+name)[0]
        h.setName(name+"Embedded")
        hTau = datasetsTau.getDatasetRootHistos(directoryTau+"/"+name)[0]
        hTau.setName(name+"Tau")
        plots.ComparisonPlot.__init__(self, h, hTau, saveFormats=saveFormats)

        self.histoMgr.normalizeToOne()
        self.histoMgr.forEachHisto(styles.generator())

        self.embeddingAnalysis = directory.replace("/", "_")
        self.tauAnalysis = directoryTau.replace("/", "_")

        self.plotName = mcSample+"_"+self.embeddingAnalysis+"_"+self.tauAnalysis+"_"+name
        self.ratioLabel = "Embedded/true"

        label = dataLabel
        if not embeddingData:
            label = mcLabel

        self.histoMgr.setHistoLegendLabelMany({name+"Embedded": "Embedded #tau (%s)"%label,
                                               name+"Tau": "True #tau (%s)"%mcLabel})


def plotPt(h, rebin=5, **kwargs):
    plotCommon(h, rebin, "p_{T} (GeV/c)", True, **kwargs)

def plotEta(h, rebin=10, **kwargs):
    opts = {}
    opts.update(kwargs.get("opts", {}))
    opts.setdefault("ymaxfactor", 1.3)
    kwargs["opts"] = opts

    opts2 = {}
    opts2.update(kwargs.get("opts2", {}))
    opts2.setdefault("ymin", 0.8)
    opts2.setdefault("ymax", 1.2)
    kwargs["opts2"] = opts2

    plotCommon(h, rebin, "#eta", False, **kwargs)

def plotPhi(h, rebin=20, **kwargs):
    opts = {}
    opts.update(kwargs.get("opts", {}))
    opts.setdefault("ymaxfactor", 1.3)
    kwargs["opts"] = opts
    
    opts2 = {}
    opts2.update(kwargs.get("opts2", {}))
    opts2.setdefault("ymin", 0.8)
    opts2.setdefault("ymax", 1.2)
    kwargs["opts2"] = opts2

    plotCommon(h, rebin, "#phi", False, **kwargs)

def plotCommon(h, rebin, xlabel, log, opts={}, opts2={}, coverPadOpts={}):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    #h.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetLineWidth(5))
    #h.histoMgr.getHistos()[0].getRootHisto().SetLineStyle(3)
    ylabel = "A.u. / %.2f" % h.binWidth()
    xlabel = xlabel
    opts_ = {}
    opts_.update(opts)
    coverPadOpts_ = {}
    coverPadOpts_.update(coverPadOpts)
    if log:
        if not "ymaxfactor" in opts_:
            opts_["ymaxfactor"] = 2
        if not "yminfactor" in opts_ and not "ymin" in opts_:
            opts_["yminfactor"] = 1e-4
    if not "ymin" in coverPadOpts_:
        coverPadOpts_["ymin"] = 0.278

    name = "TauEmbeddingTaus_%s" % (h.plotName)
    if log:
        name += "_log"
    h.createFrame(name, createRatio=True, opts=opts_, opts2=opts2, coverPadOpts=coverPadOpts_)
    h.getFrame2().GetYaxis().SetTitle(h.ratioLabel)
    h.getFrame2().GetYaxis().SetTitleSize(27) # Absolute size
    h.getFrame2().GetYaxis().SetTitleOffset(2)
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.setLegend(createLegend())
    if log:
        ROOT.gPad.SetLogy(True)
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    #h.addLuminosityText(x=0.5, y=0.3)
    h.save()


if __name__ == "__main__":
    main()
