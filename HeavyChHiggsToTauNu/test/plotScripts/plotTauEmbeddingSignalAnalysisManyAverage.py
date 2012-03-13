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

def doCounters(dirEmbs):
    datasetsEmb = result.DatasetsMany(dirEmbs, analysisEmb+"Counters", normalizeMCByLuminosity=True)
    datasetsEmb.forEach(plots.mergeRenameReorderForDataMC)
    datasetsEmb.setLumiFromData()

    datasetsEmb.remove(filter(lambda name: "HplusTB" in name, datasetsEmb.getAllDatasetNames()))
    datasetsEmb.remove(filter(lambda name: "TTToHplus" in name, datasetsEmb.getAllDatasetNames()))

    dirEmbs = ["."] + [os.path.join("..", d) for d in result.dirEmbs[1:]]

    eventCounter = result.EventCounterMany(datasetsEmb, counters=analysisEmb+counters, scaleNormalization=True)

    mainTable = eventCounter.getMainCounterTable()

    ewkDatasets = ["WJets", "TTJets", "DYJetsToLL", "SingleTop", "Diboson"]
    def ewkSum(table):
        table.insertColumn(1, counter.sumColumn("EWKMCsum", [table.getColumn(name=name) for name in ewkDatasets]))
    ewkSum(mainTable)

    datasetsEmb.close()
    return mainTable.getRow(name="deltaPhiTauMET<160")


if __name__ == "__main__":
    main()

