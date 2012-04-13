#!/usr/bin/env python

######################################################################
#
# This plot script is for inspecting the effect of averaging in
# embedded data and embedded MC. The corresponding python job
# configurations is
# * signalAnalysis_cfg.py with "doPat=1 tauEmbeddingInput=1"
# for embedding+signal analysis
#
# The development script is plotTauEmbeddingSignalAnalysisAverage.py
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

analysisEmb = "signalAnalysisCaloMet60TEff"

def main():
    dirEmbs = ["."] + [os.path.join("..", d) for d in tauEmbedding.dirEmbs[1:]]
#    dirEmbs = dirEmbs[:2]

    tauEmbedding.normalize=True
    tauEmbedding.era = "Run2011A"
 
    table = counter.CounterTable()
    for i in xrange(len(dirEmbs)):
        tmp = dirEmbs[:]
        del tmp[i]
        row = doCounters(tmp)
        row.setName("Removed embedding %d"%i)
        table.appendRow(row)

    arows = []
    arows.append(counter.meanRow(table))
    arows.append(counter.maxRow(table))
    arows.append(counter.minRow(table))
    arows.append(counter.subtractRow("Max-mean", arows[1], arows[0]))
    arows.append(counter.subtractRow("Mean-min", arows[0], arows[2]))
    for r in arows:
        table.appendRow(r)

    cellFormat = counter.TableFormatText(counter.CellFormatTeX(valueFormat='%.3f'))
    print "DeltaPhi < 160"
    print
    print table.format(cellFormat)
    print
    print

    # Format the table as in AN
    ftable = counter.CounterTable()
    def addRow(name):
        col = table.getColumn(name=name)

        minimum = col.getCount(name="Min")
        maximum = col.getCount(name="Max")

        # Maximum deviation from average
        dev1 = col.getCount(name="Max-mean")
        dev2 = col.getCount(name="Mean-min")
        if dev2.value() > dev1.value():
            dev1 = dev2

        dev1.divide(col.getCount(name="Mean"))
        dev1.multiply(dataset.Count(100))

        ftable.appendRow(counter.CounterRow(name,
                                            ["Minimum", "Maximum", "Largest deviation from average (%)"],
                                            [minimum, maximum, dev1]))

    addRow("Data")
    addRow("EWKMCsum")
    addRow("TTJets")
    addRow("WJets")
    addRow("DYJetsToLL")
    addRow("SingleTop")
    addRow("Diboson")

    cellFormat2 = counter.TableFormatLaTeX(counter.CellFormatTeX(valueFormat="%.4f", withPrecision=2))
    cellFormat2.setColumnFormat(counter.CellFormatTeX(valueFormat="%.1f", valueOnly=True), index=2)
    print ftable.format(cellFormat2)

def doCounters(dirEmbs):
    datasetsEmb = tauEmbedding.DatasetsMany(dirEmbs, analysisEmb+"Counters", normalizeMCByLuminosity=True)
    datasetsEmb.forEach(plots.mergeRenameReorderForDataMC)
    datasetsEmb.setLumiFromData()

    datasetsEmb.remove(filter(lambda name: "HplusTB" in name, datasetsEmb.getAllDatasetNames()))
    datasetsEmb.remove(filter(lambda name: "TTToHplus" in name, datasetsEmb.getAllDatasetNames()))

    eventCounter = tauEmbedding.EventCounterMany(datasetsEmb)

    mainTable = eventCounter.getMainCounterTable()

    ewkDatasets = ["WJets", "TTJets", "DYJetsToLL", "SingleTop", "Diboson"]
    def ewkSum(table):
        table.insertColumn(1, counter.sumColumn("EWKMCsum", [table.getColumn(name=name) for name in ewkDatasets]))
    ewkSum(mainTable)

    datasetsEmb.close()
    return mainTable.getRow(name="deltaPhiTauMET<160")


if __name__ == "__main__":
    main()

