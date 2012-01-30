#!/usr/bin/env python

######################################################################
#
# This plot script is for inspecting the effect of averaging in
# embedded data and embedded MC. The corresponding python job
# configurations is
# * signalAnalysis_cfg.py with "doPat=1 tauEmbeddingInput=1"
# for embedding+signal analysis
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
import plotTauEmbeddingSignalAnalysis as tauEmbedding
import produceTauEmbeddingResult as result

analysisEmb = "signalAnalysisCaloMet60TEff"

counters = "Counters/weighted"
#counters = "Counters"

def main():
    dirEmbs = ["."] + [os.path.join("..", d) for d in result.dirEmbs[1:]]
#    dirEmbs = dirEmbs[0:2]

    tauEmbedding.normalize=True
    tauEmbedding.era = "Run2011A"

    table = counter.CounterTable()

    for i, d in enumerate(dirEmbs):
        datasets = dataset.getDatasetsFromMulticrabCfg(cfgfile=d+"/multicrab.cfg", counters=analysisEmb+"Counters")
        row = doCounters(datasets)
        row.setName("Embedding %d" % i)
        table.appendRow(row)

    arows = []
    arows.append(counter.meanRow(table))
    arows.append(counter.maxRow(table))
    arows.append(counter.minRow(table))
    for r in arows:
        table.appendRow(r)

    cellFormat = counter.TableFormatText(counter.CellFormatTeX(valueFormat='%.3f'))
    print "DeltaPhi < 160"
    print
    print table.format(cellFormat)

def doCounters(datasets):
    datasets.loadLuminosities()
    plots.mergeRenameReorderForDataMC(datasets)

    datasets.remove(filter(lambda name: "HplusTB" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "TTToHplus" in name, datasets.getAllDatasetNames()))

    eventCounter = counter.EventCounter(datasets, counters=analysisEmb+counters)
    eventCounter.normalizeMCByLuminosity()
    tauEmbedding.scaleNormalization(eventCounter)

    mainTable = eventCounter.getMainCounterTable()

    ewkDatasets = ["WJets", "TTJets", "DYJetsToLL", "SingleTop", "Diboson"]
    def ewkSum(table):
        table.insertColumn(1, counter.sumColumn("EWKMCsum", [table.getColumn(name=name) for name in ewkDatasets]))

    ewkSum(mainTable)
    return mainTable.getRow(name="deltaPhiTauMET<160")




if __name__ == "__main__":
    main()

