#!/usr/bin/env python

######################################################################
#
# This plot script is for comparing the embedded data to embedded MC
# within the signal analysis. The corresponding python job
# configurations are
# * signalAnalysis_cfg.py with "doPat=1 tauEmbeddingInput=1"
# * signalAnalysis_cfg.py
# for embedding+signal analysis and signal analysis, respectively
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
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.systematics as systematics

dataEra = "Run2012ABCD"

class SystematicsSigMC:
    def __init__(self):
        self._systematics = dataset.Systematics(shapes=[
            "SystVarJES",
            "SystVarJER",
            "SystVarMET",
            "SystVarBTagSF",
            "SystVarPUWeight",
            "SystVarTopPtWeight",
        ], additionalNormalizations = {
            "LeptonVeto": systematics.getLeptonVetoUncertainty("Dummy").getUncertaintyMax(),
            "Luminosity": systematics.getLuminosityUncertainty().getUncertaintyMax()
        }, applyToDatasets = dataset.Systematics.OnlyForMC
        )
        self._cache = {}

    def histogram(self, dsetName, name):
        if not dsetName in self._cache:
            cl = self._systematics.clone()
            cl.append(additionalNormalizations = {"CrossSection": systematics.getCrossSectionUncertainty(dsetName).getUncertaintyMax()})
            self._cache[dsetName] = cl

        return self._cache[dsetName].histogram(name)
systematicsEmbMC = SystematicsSigMC()

def main():
    # Apply TDR style
    style = tdrstyle.TDRStyle()
    #    histograms.cmsTextMode = histograms.CMSMode.NONE
    #histograms.uncertaintyMode.set(histograms.Uncertainty.StatOnly)
    histograms.uncertaintyMode.set(histograms.uncertaintyMode.StatAndSyst)
    #histograms.createLegend.moveDefaults(dx=-0.15, dh=0.05)#, dh=-0.05) # QCD removed
    histograms.createLegend.setDefaults(textSize=0.04)
    histograms.createLegend.moveDefaults(dx=-0.25, dh=0.1)#, dh=-0.05) # QCD removed

    histograms.createLegendRatio.setDefaults(ncolumns=2, textSize=0.08, columnSeparation=0.3)
    histograms.createLegendRatio.moveDefaults(dx=-0.35, dh=-0.1, dw=0.25)
    plots._legendLabels["BackgroundStatError"] = "Sim. stat. unc."
    plots._legendLabels["BackgroundStatSystError"] = "Sim. stat.#oplussyst. unc."

    legendLabelsSet = False

    for optMode in [
#        "OptQCDTailKillerNoCuts",
        "OptQCDTailKillerLoosePlus",
#        "OptQCDTailKillerMediumPlus",
#        "OptQCDTailKillerTightPlus",
#            None
    ]:
        # Create the dataset objects
        datasetsEmb = dataset.getDatasetsFromMulticrabCfg(dataEra=dataEra, optimizationMode=optMode)

        # Remove signal and W+3jets datasets
        datasetsEmb.remove(filter(lambda name: "HplusTB" in name, datasetsEmb.getAllDatasetNames()))
        datasetsEmb.remove(filter(lambda name: "TTToHplus" in name, datasetsEmb.getAllDatasetNames()))

        datasetsEmb.updateNAllEventsToPUWeighted()
        plots.mergeRenameReorderForDataMC(datasetsEmb)

        doCounters(datasetsEmb, optMode)

        if not legendLabelsSet:
            def trans(n):
                if n[0:2] in ["W+", "Z/"]:
                    return n
                else:
                    return n[0].lower()+n[1:]

            for d in datasetsEmb.getAllDatasetNames():
                oldName = plots._legendLabels.get(d, d)
                plots._legendLabels[d] = "Embedded "+trans(oldName)

            legendLabelsSet = True

        # Remove QCD for plots
        datasetsEmb.remove(["QCD_Pt20_MuEnriched"])
        outputDir = optMode
        if outputDir is not None:
            outputDir += "_embdatamc"
        doPlots(datasetsEmb, outputDir)

        tauEmbedding.writeToFile(outputDir, "input.txt", "Embedded: %s\n" % os.getcwd())

drawPlotCommon = plots.PlotDrawer(ylabel="Events / %.0f", stackMCHistograms=True, log=True, addMCUncertainty=True,
                                  opts2={"ymin": 0, "ymax": 2},
                                  ratio=True, ratioType="errorScale", ratioCreateLegend=True, ratioYlabel="Data/Sim.", ratioErrorOptions={"numeratorStatSyst": False},
                                  addLuminosityText=True)

def doPlots(datasetsEmb, outputDir):
    lumi = datasetsEmb.getDataset("Data").getLuminosity()

    def createPlot(name):
#        p = plots.DataMCPlot(datasetsEmb, systematicsEmbMC.histogram(name), normalizeToLumi=lumi)
        drhData = datasetsEmb.getDataset("Data").getDatasetRootHisto(name)
        drhMCs = [d.getDatasetRootHisto(systematicsEmbMC.histogram(d.getName(), name)) for d in datasetsEmb.getMCDatasets()]

        p = plots.DataMCPlot2([drhData]+drhMCs)
        p.histoMgr.normalizeMCToLuminosity(lumi)
        # by default pseudo-datasets lead to MC histograms, for these
        # plots we want to treat Data as data
        p.histoMgr.getHisto("Data").setIsDataMC(True, False)
        p.setDefaultStyles()
        return p

    plotter = tauEmbedding.CommonPlotter(outputDir, "embdatamc", drawPlotCommon)
    plotter.plot(None, createPlot, {
#        "NBjets": {"moveLegend": {"dx": -0.4, "dy": -0.45}}
#        "ImprovedDeltaPhiCutsBackToBackMinimumAfterMtSelections": {"moveLegend": 
        "shapeTransverseMass": {"moveLegend": {"dy": -0.12}},
                                #{"dx": -0.3}}, 
        "shapeTransverseMass_log": {"moveLegend": {"dy": -0.12}}#, "ratioMoveLegend": {"dx": -0.3}}
    })
    return


def addMcSum(t):
    allDatasets = ["QCD_Pt20_MuEnriched", "WJets", "TTJets", "DYJetsToLL", "SingleTop", "Diboson"]
    t.insertColumn(1, counter.sumColumn("MCSum", [t.getColumn(name=name) for name in allDatasets]))

def doCounters(datasetsEmb, outputDir):
    eventCounter = counter.EventCounter(datasetsEmb)
    eventCounter.normalizeMCToLuminosity(datasetsEmb.getDataset("Data").getLuminosity())
    table = eventCounter.getMainCounterTable()
    table.keepOnlyRows([
        "Trigger and HLT_MET cut",
        "taus > 0",
        "tau trigger scale factor",
        "electron veto",
        "muon veto",
        "njets",
        "MET trigger scale factor",
        "QCD tail killer collinear",
        "MET",
        "btagging",
        "btagging scale factor",
        "Embedding: mT weight",
        "QCD tail killer back-to-back",
        "Selected events"
    ])
    addMcSum(table)

    cellFormat = counter.TableFormatText(counter.CellFormatTeX(valueFormat='%.4f', withPrecision=2))
    txt = table.format(cellFormat)
    print txt
    d = outputDir
    if d is None:
        d = "."
    if not os.path.exists(d):
        os.makedirs(d)

    f = open(os.path.join(d, "counters.txt"), "w")
    f.write(txt)
    f.write("\n")
    


##    # All embedded events
##    eventCounterAll = counter.EventCounter(datasetsEmb.getFirstDatasetManager(), counters=analysisEmbAll+counters)
##    eventCounterAll.normalizeMCByLuminosity()
##    tableAll = eventCounterAll.getMainCounterTable()
##    tableAll.keepOnlyRows([
##            "All events",
##            ])
##    tableAll.renameRows({"All events": "All embedded events"})
##
##    # Mu eff + Wtau mu
##    eventCounterMuEff = counter.EventCounter(datasetsEmb.getFirstDatasetManager(), counters=analysisEmbNoTauEff+counters)
##    eventCounterMuEff.normalizeMCByLuminosity()
##    tauEmbedding.scaleNormalization(eventCounterMuEff)
##    tableMuEff = eventCounterMuEff.getMainCounterTable()
##    tableMuEff.keepOnlyRows([
##            "All events"
##            ])
##    tableMuEff.renameRows({"All events": "mu eff + Wtaumu"})
##
##    # Event counts after embedding normalization, before tau trigger eff,
##    # switch to calculate uncertainties of the mean of 10 trials
##    eventCounterNoTauEff = tauEmbedding.EventCounterMany(datasetsEmb, counters=analysisEmbNoTauEff+counters)
##    tableNoTauEff = eventCounterNoTauEff.getMainCounterTable()
##    tableNoTauEff.keepOnlyRows([
##            "Trigger and HLT_MET cut",
##            "njets",
##            ])
##    tableNoTauEff.renameRows({"Trigger and HLT_MET cut": "caloMET > 60",
##                              "njets": "tau ID"
##                              })
##
##    # Event counts after tau trigger eff
##    eventCounter = tauEmbedding.EventCounterMany(datasetsEmb, counters=analysisEmb+counters)
##    table = eventCounter.getMainCounterTable()
##    table.keepOnlyRows([
##            "njets",
##            "MET",
##            "btagging scale factor",
##            "DeltaPhi(Tau,MET) upper limit",
##            ])
##    table.renameRows({"njets": "Tau trigger efficiency",
##                      "btagging scale factor": "b tagging"
##                      })
##
##    # Combine the rows to one table
##    result = counter.CounterTable()
##    for tbl in [
##        tableAll,
##        tableMuEff,
##        tableNoTauEff,
##        table
##        ]:
##        for iRow in xrange(tbl.getNrows()):
##            result.appendRow(tbl.getRow(index=iRow))
##
##    addMcSum(result)
##    cellFormat = counter.TableFormatText(counter.CellFormatTeX(valueFormat='%.4f', withPrecision=2))
##
##    print result.format(cellFormat)

if __name__ == "__main__":
    main()
