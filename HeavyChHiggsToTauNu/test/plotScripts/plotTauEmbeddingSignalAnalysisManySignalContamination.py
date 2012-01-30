#!/usr/bin/env python

######################################################################
#
# This plot script is for inspecting the signal contamination in
# embedded MC. The corresponding python job configurations is
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
analysisSig = "signalAnalysisGenuineTau"

counters = "Counters/weighted"
#counters = "Counters"

def main():
    dirEmbs = ["."] + [os.path.join("..", d) for d in result.dirEmbs[1:]]
    dirSig = "../"+result.dirSig

    datasetsEmb = result.DatasetsMany(dirEmbs, analysisEmb+"Counters", normalizeMCByLuminosity=True)
    datasetsSig = dataset.getDatasetsFromMulticrabCfg(cfgfile=dirSig+"/multicrab.cfg", counters=analysisSig+"Counters")

    datasetsEmb.forEach(plots.mergeRenameReorderForDataMC)
    datasetsEmb.setLumiFromData()
    plots.mergeRenameReorderForDataMC(datasetsSig)

    datasetsEmb.remove(filter(lambda name: "HplusTB" in name, datasetsEmb.getAllDatasetNames()))

    def addSignal(datasetMgr):
        xsect.setHplusCrossSectionsToBR(datasetMgr, br_tH=0.03, br_Htaunu=1) # agreed to use 3 % as with QCD
        plots.mergeWHandHH(datasetMgr)

        ttjets2 = datasetMgr.getDataset("TTJets").deepCopy()
        ttjets2.setName("TTJets2")
        ttjets2.setCrossSection(ttjets2.getCrossSection() - datasetMgr.getDataset("TTToHplus_M120").getCrossSection())
        datasetMgr.append(ttjets2)
        datasetMgr.merge("EWKnoTT", ["WJets", "DYJetsToLL", "SingleTop", "Diboson"], keepSources=True)
        datasetMgr.merge("EWKScaled", ["EWKnoTT", "TTJets2"])
        for mass in [80, 100]:
#        for mass in [80, 90, 100, 120, 140, 150, 155, 160]:
            datasetMgr.merge("EWKSignal_M%d"%mass, ["TTToHplus_M%d"%mass, "EWKScaled"], keepSources=True)
    datasetsEmb.forEach(addSignal)

    tauEmbedding.normalize=True
    tauEmbedding.era = "Run2011A"

    doCounters(datasetsEmb)

def doCounters(datasetsEmb):    
    eventCounter = result.EventCounterMany(datasetsEmb, counters=analysisEmb+counters, scaleNormalization=True)

    mainTable = eventCounter.getMainCounterTable()

    ewkDatasets = ["WJets", "TTJets", "DYJetsToLL", "SingleTop", "Diboson"]
    def ewkSum(table):
        table.insertColumn(1, counter.sumColumn("EWKMCsum", [table.getColumn(name=name) for name in ewkDatasets]))

    ewkSum(mainTable)
    cellFormat = counter.TableFormatText(counter.CellFormatTeX(valueFormat='%.3f'))
    print mainTable.format(cellFormat)


if __name__ == "__main__":
    main()

