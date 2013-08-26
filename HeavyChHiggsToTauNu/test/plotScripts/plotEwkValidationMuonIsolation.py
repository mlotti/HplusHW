#!/usr/bin/env python

######################################################################
#
# This plot script is for checking the effect of the original muon
# isolation after the embedded tau ID within tau ID and signal
# analysis.
# The corresponding python job configuration is
# * embeddingAnalysis_cfg.py
# Note that the embedding must be done *without* muon isolation for this check.
#
# Authors: Matti Kortelainen
#
######################################################################

import os
import array
import math
import StringIO

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tauEmbedding as tauEmbedding

tauAnalysisEmb = "tauNtuple"

dataEra = "Run2011AB"
dataEra = ""

mcLuminosity = 5049.069000

def main():
    datasets = dataset.getDatasetsFromMulticrabCfg(counters=tauAnalysisEmb+"Counters", weightedCounters=(dataEra!=""))
    if dataEra != "":
        datasets.updateNAllEventsToPUWeighted(era=dataEra)
    plots.mergeRenameReorderForDataMC(datasets)
    
    style = tdrstyle.TDRStyle()
    histograms.cmsTextMode = histograms.CMSMode.SIMULATION
    histograms.cmsText[histograms.CMSMode.SIMULATION] = "Simulation"
    histograms.createLegend.setDefaults(y1=0.93, y2=0.75, x1=0.52, x2=0.93)

    isolations = [
        ("Standard", "standard"),
        ("TauLike", "taulike"),
        ("ChargedHadrRel10", "chargedHadrRel10"),
        ("ChargedHadrRel15", "chargedHadrRel15"),
        ]

    for name, isolation in isolations:
        ntupleCache = dataset.NtupleCache(tauAnalysisEmb+"/tree", "EmbeddingMuonIsolationSelector",
                                          selectorArgs=[tauEmbedding.tauNtuple.weight[dataEra], isolation],
                                          cacheFileName="histogramCache-%s.root" % name,
                                          #maxEvents=100,
                                          #process=False,
                                          )

        for datasetName in ["TTJets"]:
            doPlots(datasets, datasetName, name, ntupleCache)
            doCounters(datasets, datasetName, name, ntupleCache)

def doPlots(datasets, datasetName, selectionName, ntupleCache):
    createPlot = PlotCreator(datasets, datasetName, ntupleCache)

    drawPlot = plots.PlotDrawer(addMCUncertainty=True, log=True, stackMCHistograms=False,
                                ratio=True, ratioInvert=True,
                                optsLog={"ymin": 1e-1}, opts2={"ymin": 0.9, "ymax": 1.02})

    def customize(p):
        p.setRatios([plots._createRatio(p.numeratorRaw, p.denominatorRaw, ytitle="Fraction", isBinomial=True)])
    def createDrawPlot(histo, fname, xlabel, **kwargs):
        p = createPlot(histo)
        drawPlot(p, fname, xlabel, customizeBeforeDraw=customize, **kwargs)

    #opts2def = {"DYJetsToLL": {"ymin":0, "ymax": 1.5}}.get(datasetName, {"ymin": 0.9, "ymax": 1.02})
    #moveLegend = {"DYJetsToLL": {"dx": -0.02}}.get(datasetName, {})
    opts2def = {}
    moveLegend = {}

    if selectionName != "TauLike":
        opts2def["ymin"] = 0.98
        opts2def["ymax"] = 1.005

    prefix = "muiso_"+selectionName+"_"
    postfix = "_"+datasetName

    opts2 = opts2def
    createDrawPlot("tauPt",
             prefix+"TauPt"+postfix, "#tau-jet p_{T} (GeV/c)", ylabel="Events / %.0f GeV/c",
             opts2=opts2, cutLine=40, moveLegend=moveLegend)

    createDrawPlot("tauEta",
             prefix+"TauEta"+postfix, "#tau-jet #eta", ylabel="Events / %.1f",
             opts2=opts2, cutLine=[-2.1, 2.1], moveLegend=moveLegend)

    createDrawPlot("tauPhi",
             prefix+"TauPhi"+postfix, "#tau-jet #phi", ylabel="Events / %.1f",
             opts2=opts2, moveLegend=moveLegend)

    createDrawPlot("tauLeadingTrackPt",
             prefix+"TauLeadingTrackPt"+postfix, "#tau-jet leading ch. cand. p_{T} (GeV/c)", ylabel="Events / %.0f GeV/c",
             opts2=opts2, cutLine=20, moveLegend=moveLegend)

    createDrawPlot("tauRtau",
             prefix+"TauRtau"+postfix, "#tau-jet R_{#tau}", ylabel="Events / %.1f",
             opts2=opts2, cutLine=0.7, moveLegend=moveLegend)

    createDrawPlot("vertexCount",
             prefix+"VertexCount"+postfix, "Number of good PV", ylabel="Events / %.0f",
             opts2=opts2, moveLegend=moveLegend)


def doCounters(datasets, datasetName, selectionName, ntupleCache):
    eventCounter = counter.EventCounter(datasets)
    def isNotThis(name):
        return name != datasetName

    eventCounter.removeColumns(filter(isNotThis, datasets.getAllDatasetNames()))

    counters = "counters/counter"
    if dataEra != "":
        counters = "counters/weighted/counter"
    eventCounter.getMainCounter().appendRows(ntupleCache.histogram(counters))
    table = eventCounter.getMainCounterTable()

    nTauID = table.getCount(colName=datasetName, rowName="Tau ID").clone()
    nMuonIso = table.getCount(colName=datasetName, rowName="Muon isolation").clone()
    nIsoMuTrigger = table.getCount(colName=datasetName, rowName="IsoMu trigger").clone()

    eff = dataset.divideBinomial(nMuonIso, nTauID)
    effTrg = dataset.divideBinomial(nIsoMuTrigger, nMuonIso)

    out = StringIO.StringIO()
    out.write(table.format())
    out.write("\n")
    out.write("Muon isolation/Tau ID        = %.6f + %.6f - %.6f\n" % (eff.value(), eff.uncertaintyHigh(), eff.uncertaintyLow()))
    out.write("IsoMu trigger/Muon isolation = %.6f + %.6f - %.6f\n" % (effTrg.value(), effTrg.uncertaintyHigh(), effTrg.uncertaintyLow()))
    print "Isolation mode", selectionName
    print out.getvalue()

    fname = "counters_muiso_"+selectionName+"_"+datasetName+".txt"
    f = open(fname, "w")
    f.write(out.getvalue())
    f.close()
    print "Printed tau counters to", fname
    out.close()


class PlotCreator:
    def __init__(self, datasets, datasetName, ntupleCache):
        self.datasets = datasets
        self.datasetName = datasetName
        self.ntupleCache = ntupleCache

        self.styles = styles.getStyles()

    ## Function call syntax for creating the plot
    #
    # \param name   Name of the histogram (with embedding analysis path)
    # \param rebin  Rebin
    #
    # \return plots.PlotBase derived object
    def __call__(self, name, rebin=1):
        drh1 = self.datasets.getDataset(self.datasetName).getDatasetRootHisto(self.ntupleCache.histogram(name+"_AfterTauID"))
        drh2 = self.datasets.getDataset(self.datasetName).getDatasetRootHisto(self.ntupleCache.histogram(name+"_AfterMuonIsolation"))

        h1_raw = drh1.getHistogram()
        h2_raw = drh2.getHistogram()
        
        drh1.normalizeToLuminosity(mcLuminosity)
        drh2.normalizeToLuminosity(mcLuminosity)

        h1 = drh1.getHistogram()
        h2 = drh2.getHistogram()
        if rebin > 1:
            h1_raw.Rebin(rebin)
            h2_raw.Rebin(rebin)
            h1.Rebin(rebin)
            h2.Rebin(rebin)

        h1.SetName("TauID")
        h2.SetName("TauIDMuIso")
        sty = self.styles[:]
        p = plots.ComparisonPlot(h1, h2)

        legLabel = plots._legendLabels.get(self.datasetName, self.datasetName)
        legLabel += " sim. "

        p.setLuminosity(mcLuminosity)
        p.histoMgr.setHistoLegendLabelMany({
                "TauID":      "tau ID",
                "TauIDMuIso": "tau ID + mu iso"
                })
        p.histoMgr.forEachHisto(styles.Generator(sty))

        p.numeratorRaw = h2_raw
        p.denominatorRaw = h1_raw
       
        return p


if __name__ == "__main__":
    main()
