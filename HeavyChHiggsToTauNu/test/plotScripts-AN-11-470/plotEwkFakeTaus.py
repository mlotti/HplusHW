#!/usr/bin/env python

######################################################################
#
# This plot script is for fake tau background table
#
#
# Authors: Matti Kortelainen
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
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect

def main():
    # Read the datasets
    datasets = dataset.getDatasetsFromMulticrabCfg()
    datasets.updateNAllEventsToPUWeighted()
    datasets.loadLuminosities()

    plots.mergeRenameReorderForDataMC(datasets)

    # Remove signals
    datasets.remove(filter(lambda name: "TTToHplus" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "HplusTB" in name, datasets.getAllDatasetNames()))

    eventCounter = counter.EventCounter(datasets)
    eventCounter.normalizeMCByLuminosity()

    mainTable = eventCounter.getMainCounterTable()

    mainTable.keepOnlyRows([
            "nonQCDType2:taus == 1",
            "nonQCDType2:electron veto",
            "nonQCDType2:muon veto",
            "nonQCDType2:njets",
            "nonQCDType2:MET",
            "nonQCDType2:btagging",
            "nonQCDType2:deltaphi160",
            "nonQCDType2:deltaphi130"
            ])
    mainTable.removeColumn(name="Data")

    index = mainTable.getRowNames().index("nonQCDType2:MET")
    row = mainTable.getRow(index)
    mainTable.removeRow(index)
    mainTable.insertRow(index+1, row)

    index = mainTable.getColumnNames().index("WJets")
    col = mainTable.getColumn(index)
    mainTable.removeColumn(index)
    mainTable.insertColumn(index+1, col)


    cellFormat = counter.TableFormatLaTeX(counter.CellFormatTeX(valueFormat="%.4f", withPrecision=2))

    print mainTable.format(cellFormat)


if __name__ == "__main__":
    main()
