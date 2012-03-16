#!/usr/bin/env python

######################################################################
#
# This plot script is for inspecting the signal contamination in embedded MC.
# within the signal analysis. The corresponding python job
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
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tauEmbedding as tauEmbedding

analysisEmb = "signalAnalysisCaloMet60TEff"
counters = "Counters/weighted"
signal_br_tH = 0.03 # agreed to use 3 % as with QCD

def main():
    # Adjust paths such that this script can be run inside the first embedding trial directory
    dirEmbs = ["."] + [os.path.join("..", d) for d in tauEmbedding.dirEmbs[1:]]

    # Create the dataset objects
    datasetsEmb = tauEmbedding.DatasetsMany(dirEmbs, analysisEmb+"Counters", normalizeMCByLuminosity=True)

    datasetsEmb.forEach(plots.mergeRenameReorderForDataMC)
    datasetsEmb.setLumiFromData()


    # Remove W+3jets
    datasetsEmb.remove(filter(lambda name: "W3Jets" in name, datasetsEmb.getAllDatasetNames()))

    # Add EWK+tt scaled down with BR(t->H+) (EWKScaled)
    def addSignal(datasetMgr):
        xsect.setHplusCrossSectionsToBR(datasetMgr, br_tH=signal_br_tH, br_Htaunu=1) 
        plots.mergeWHandHH(datasetMgr)

        ttjets2 = datasetMgr.getDataset("TTJets").deepCopy()
        ttjets2.setName("TTJets2")
        ttjets2.setCrossSection(ttjets2.getCrossSection() - datasetMgr.getDataset("TTToHplus_M120").getCrossSection())
        datasetMgr.append(ttjets2)
        datasetMgr.merge("EWKnoTT", ["WJets", "DYJetsToLL", "SingleTop", "Diboson"], keepSources=True)
        datasetMgr.merge("EWKScaled", ["EWKnoTT", "TTJets2"])
        datasetMgr.merge("EWKMC", ["WJets", "TTJets", "DYJetsToLL", "SingleTop", "Diboson"])
    datasetsEmb.forEach(addSignal)

    tauEmbedding.normalize=True
    tauEmbedding.era = "Run2011A"

    doCounters(datasetsEmb)


def doCounters(datasetsEmb):
    eventCounter = tauEmbedding.EventCounterMany(datasetsEmb, counters=analysisEmb+counters, normalize=True)

    #row = "btagging scale factor"
    row = "deltaPhiTauMET<160"
    #row = "deltaPhiTauMET<130"
    table = eventCounter.getMainCounterTable()
    table.keepOnlyRows([row])

    result = counter.CounterTable()
    def addRow(name, newktt, nsignal):
        fraction = None
        if nsignal != None:
            fraction = nsignal.clone()
            total = nsignal.clone()
            total.add(newktt)
            fraction.divide(total)
            fraction.multiply(dataset.Count(100))
        result.appendRow(counter.CounterRow(name, ["EWK+tt events", "Signal events", "Signal fraction (\%)"], [newktt, nsignal, fraction]))
    addRow("No signal", table.getCount(irow=0, colName="EWKMC"), None)
    ewkWithSignal = table.getCount(irow=0, colName="EWKScaled")
    for mass in [80, 90, 100, 120, 140, 150, 155, 160]:
        addRow("H+ M%d"%mass, ewkWithSignal, table.getCount(irow=0, colName="TTToHplus_M%d"%mass))

    #cellFormat = counter.TableFormatLaTeX(counter.CellFormatTeX(valueFormat='%.3f'))
    cellFormat = counter.TableFormatLaTeX(counter.CellFormatTeX(valueFormat='%.4f', withPrecision=2))
    print result.format(cellFormat)
    

if __name__ == "__main__":
    main()
