#!/usr/bin/env python

######################################################################
#
# This plot script is for comparing the embedded data to embedding MC
# within the tau ID. The corresponding python job
# configuration is embeddingAnalysis_cfg.py
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
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.cutstring import * # And, Not, Or
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tauEmbedding as tauEmbedding


analysis = "tauNtuple"
#dataEra = "Run2011AB"
dataEra = ""

def main():
    # Read the datasets
    datasets = dataset.getDatasetsFromMulticrabCfg(counters=analysis+"Counters", weightedCounters=(dataEra!=""))
    if dataEra != "":
        datasets.updateNAllEventsToPUWeighted(era=dataEra)
    datasets.loadLuminosities()
    plots.mergeRenameReorderForDataMC(datasets)

    # Remove signal
    datasets.remove(filter(lambda name: "TTToHplus" in name, datasets.getAllDatasetNames()))

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    histograms.createLegend.moveDefaults(dx=-0.04)
    plots._legendLabels["QCD_Pt20_MuEnriched"] = "QCD"
    #datasets.remove(["QCD_Pt20_MuEnriched"])
    #histograms.createLegend.moveDefaults(dh=-0.05)

    selectorArgs = [tauEmbedding.tauNtuple.weight[dataEra]]
    ntupleCache = dataset.NtupleCache(analysis+"/tree", "TauAnalysisSelector",
                                      selectorArgs=selectorArgs+[True],
                                      process=False,
                                      #maxEvents=100,
                                      cacheFileName="histogramCacheTauEmb.root"
                                      )
#    doPlots(datasets)
    doCounters(datasets, ntupleCache)

def doPlots(datasets):
    pass

rowNames = [
#    "All events",
    "Pre Pt cut",
    "Decay mode finding",
    "Eta cut",
    "Pt cut",
    "Leading track pt",
    "Against electron",
    "Against muon",
    "Isolation",
    "One prong",
    "Rtau",
]

def doCounters(datasets, ntupleCache):
    # Counters
    eventCounter = counter.EventCounter(datasets)
    mainCounter = eventCounter.getMainCounter();
    counters = "counters/counter"
    if dataEra != "":
        counters = "counters/weighted/counter"
    mainCounter.appendRows(ntupleCache.histogram(counters))

    format = counter.TableFormatText(counter.CellFormatText(valueFormat="%.0f"))

    table = mainCounter.getTable()
    print table.format(format)

    effFormat = counter.TableFormatText(counter.CellFormatText(valueFormat="%.2f", withPrecision=2))

    teffs = mainCounter.constructTEfficiencies(createTEfficiency)
    table = counter.efficiencyTableFromTEfficiencies(teffs, mainCounter.getColumnNames(), rowNames)
    table.multiply(100)
    print table.format(effFormat)

def createTEfficiency(counter):
    bins = len(rowNames)
    passed = ROOT.TH1F("pass", "pass", bins, 0, bins)
    total = ROOT.TH1F("tot", "tot", bins, 0, bins)

    for i, name in enumerate(rowNames):
        bin = i+1
        value = counter.getCountByName(name).value()
        passed.SetBinContent(bin, value)
        if i == 0:
            total.SetBinContent(bin, value)
        total.SetBinContent(bin+1, value)

    return (passed, total)

if __name__ == "__main__":
    main()
