#!/usr/bin/env python

######################################################################
#
# This plot script is for analysing the muon selection part of the EWK
# background measurement. The corresponding python job configuration
# is tauEmbedding/muonAnalysis_cfg.py.
#
# Author: Matti Kortelainen
#
######################################################################

import sys
import array

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles

analysis = "muonNtuple"
counters = analysis+"Counters"
countersWeighted = counters+"/weighted"

era = "Run2011AB"

weight = {
    "Run2011A": "weightPileup_Run2011A",
    "Run2011B": "weightPileup_Run2011B",
    "Run2011AB": "weightPileup_Run2011AB",
    }[era]
#weight = ""

mcOnly = True
mcOnly = False
mcLuminosity = 5049.

def main():
    datasets = dataset.getDatasetsFromMulticrabCfg(counters=counters)
    datasets.updateNAllEventsToPUWeighted()

    if era == "Run2011A":
        datasets.remove(filter(lambda name: "2011B_" in name, datasets.getDataDatasetNames()))
    elif era == "Run2011B":
        datasets.remove(filter(lambda name: "2011A_" in name, datasets.getDataDatasetNames()))
    elif era == "Run2011AB":
        pass

    #datasets.remove(datasets.getMCDatasetNames())
    if mcOnly:
        datasets.remove(datasets.getDataDatasetNames())
    else:
        datasets.loadLuminosities()

    #datasetsMC = datasets.deepCopy()
    #datasetsMC.remove(datasets.getDataDatasetNames())
    
    plots.mergeRenameReorderForDataMC(datasets)
    
    styleGenerator = styles.generator(fill=True)

    style = tdrstyle.TDRStyle()
    #histograms.createLegend.moveDefaults(dx=-0.15)
    plots._legendLabels["QCD_Pt20_MuEnriched"] = "QCD"
    histograms.createLegend.moveDefaults(dx=-0.04)

    selections = [
        ("Full", "embedding"),
        ("FullNoIso", "disabled"),
        ("FullStandardIso", "standard")
        ]
    for name, isolation in selections:
        ntupleCache = dataset.NtupleCache(analysis+"/tree", "MuonAnalysisSelector",
                                          selectorArgs=[weight, isolation],
                                          cacheFileName="histogramCache-%s.root" % name,
                                          process=True
                                          )


        doPlots(datasets, name, ntupleCache)
        printCounters(datasets, name, ntupleCache)

#    doPlotsWTauMu(datasets, "TTJets") FIXME
#    doPlotsWTauMu(datasets, "WJets")  FIXME

def doPlots(datasets, selectionName, ntupleCache):
    def createPlot(name, **kwargs):
        args = kwargs.copy()
        if mcOnly:
            args["normalizeToLumi"] = mcLuminosity
        return plots.DataMCPlot(datasets, name, **args)
    drawPlot = plots.PlotDrawer(stackMCHistograms=True, addMCUncertainty=True, log=True, ratio=not mcOnly, addLuminosityText=True,
                                ratioYlabel="Ratio",
                                optsLog={"ymin": 1e-1}, opts2={"ymin": 0, "ymax": 2})


    prefix = era+"_"+selectionName+"_"
    drawPlot(createPlot(ntupleCache.histogram("selectedMuonPt_AfterJetSelection")),
             prefix+"muon_pt_log", "Muon p_{T} (GeV/c)", ylabel="Events / %.0f GeV/c", cutBox={"cutValue":40, "greaterThan":True})

    drawPlot(createPlot(ntupleCache.histogram("uncorrectedMet_AfterJetSelection")),
             prefix+"met_pt_log", "Uncorrected PF E_{T}^{miss} (GeV)", ylabel="Events / %.0f GeV")

    drawPlot(createPlot(ntupleCache.histogram("transverseMassUncorrectedMet_AfterJetSelection")),
             prefix+"mt_log", "m_{T}(#mu, E_{T}^{miss}) (GeV/c^{2})", ylabel="Events / %.0f GeV/c^{2}")

    if "NoIso" in selectionName:
        drawPlot(createPlot(ntupleCache.histogram("selectedMuonChargedHadronEmbIso_AfterJetSelection")),
                 prefix+"chargedHadronIso_log", "Charged hadron #Sigma p_{T} (GeV/c)", ylabel="Events / %.1f GeV/c")
        drawPlot(createPlot(ntupleCache.histogram("selectedMuonPuChargedHadronEmbIso_AfterJetSelection")),
                 prefix+"puChargedHadronIso_log", "Charged hadron #Sigma p_{T} (GeV/c)", ylabel="Events / %.1f GeV/c")
        drawPlot(createPlot(ntupleCache.histogram("selectedMuonNeutralHadronEmbIso_AfterJetSelection")),
                 prefix+"neutralHadronIso_log", "Neutral hadron #Sigma p_{T} (GeV/c)", ylabel="Events / %.1f GeV/c")
        drawPlot(createPlot(ntupleCache.histogram("selectedMuonPhotonEmbIso_AfterJetSelection")),
                 prefix+"photonIso_log", "Photon #Sigma p_{T} (GeV/c)", ylabel="Events / %.1f GeV/c")

        drawPlot(createPlot(ntupleCache.histogram("selectedMuonEmbIso_AfterJetSelection")),
                 prefix+"embeddingIso_log", "Isolation variable (GeV/c)", ylabel="Events / %.1f GeV/c")

        drawPlot(createPlot(ntupleCache.histogram("selectedMuonStdIso_AfterJetSelection")),
                 prefix+"standardIso_log", "Isolation variable", ylabel="Events / %.1f GeV/c")

printed = False
def printCounters(datasets, selectionName, ntupleCache):
    global printed
    if not printed:
        print "============================================================"
        print "Dataset info: "
        datasets.printInfo()
        printed = True


    if len(weight) == 0:
        eventCounter = counter.EventCounter(datasets, counters=counters)
        counterPath = "counters/counter"
    else:
        eventCounter = counter.EventCounter(datasets)
        counterPath = "counters/weighted/counter"

    eventCounter.getMainCounter().appendRows(ntupleCache.histogram(counterPath))

    if mcOnly:
        eventCounter.normalizeMCToLuminosity(mcLuminosity)
    else:
        eventCounter.normalizeMCByLuminosity()

    table = eventCounter.getMainCounterTable()
    mcDatasets = filter(lambda n: n != "Data", table.getColumnNames())
    col = 1
    if mcOnly:
        col = 0
    table.insertColumn(col, counter.sumColumn("MCSum", [table.getColumn(name=name) for name in mcDatasets]))

    cellFormat = counter.TableFormatText(counter.CellFormatText(valueFormat='%.3f'))
#    cellFormat = counter.TableFormatText(counter.CellFormatTeX(valueFormat='%.1f'))
    output = table.format(cellFormat)

    print
    print "########################################"
    print "Selection", selectionName
    print output

    prefix = era+"_"+selectionName+"_counters"
    if len(weight) == 0:
        prefix += "_nonweighted"
    f = open(prefix+".txt", "w")
    f.write(output)
    f.close()
    

if __name__ == "__main__":
    main()
