#!/usr/bin/env python

######################################################################
#
# This plot script is for comparing the embedded MC and normal MC
# within signal analysis. The corresponding python job
# configurations are
# * tauAnalysis_cfg.py
# * signalAnalysis_cfg.py with "tauEmbeddingInput=1"
# * signalAnalysis_cfg.py with "doTauEmbeddingLikePreselection=1"
# for embedded signal analysis, and normal signal analysis,
# respectively
#
# The development scripts are
# * plotTauEmbeddingMcTauMcMany
# * plotTauEmbeddingMcSignalAnalysisMcMany
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
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.aux as aux

analysisEmb = "signalAnalysis"
#analysisSig = "signalAnalysisTauEmbeddingLikePreselection"
analysisSig = "signalAnalysisGenuineTauTriggered"

dataEra = "Run2012ABCD"
#optMode = None
#optMode = "OptQCDTailKillerLoosePlus"

def main():
    dirEmb = "."
#    dirSig = "../multicrab_signalAnalysisGenTau_140206_122901"
#    dirSig = "../multicrab_signalAnalysisGenTau_140211_100710"
#    dirSig = "../multicrab_signalAnalysisGenTau_140217_152148"
#    dirSig = "../multicrab_signalAnalysisGenTau_140326_132754"
    dirSig = "../multicrab_signalAnalysisGenTautightPlus_140512_094945"

    for optMode in [
#        "OptQCDTailKillerLoosePlus",
#        "OptQCDTailKillerMediumPlus",
#        "OptQCDTailKillerTightPlus",
            None
        ]:
        datasetsEmb = dataset.getDatasetsFromMulticrabCfg(directory=dirEmb, dataEra=dataEra, analysisName=analysisEmb, optimizationMode=optMode)
        datasetsSig = dataset.getDatasetsFromMulticrabCfg(directory=dirSig, dataEra=dataEra, analysisName=analysisSig, optimizationMode=optMode)
        doDataset(datasetsEmb, datasetsSig, optMode)
        datasetsEmb.close()
        datasetsSig.close()

def doDataset(datasetsEmb, datasetsSig, optMode):
    global ind
    ind = 0

#    datasetsEmb.loadLuminosities() # not needed for pseudo-multicrab

    datasetsSig.updateNAllEventsToPUWeighted()
    datasetsEmb.updateNAllEventsToPUWeighted()

    plots.mergeRenameReorderForDataMC(datasetsEmb)
    plots.mergeRenameReorderForDataMC(datasetsSig)

    def mergeEWK(datasets):
        datasets.merge("EWKMC", ["WJets", "TTJets", "DYJetsToLL", "SingleTop", "Diboson"], keepSources=True)
    mergeEWK(datasetsSig)
    mergeEWK(datasetsEmb)

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    histograms.cmsTextMode = histograms.CMSMode.SIMULATION
    histograms.cmsText[histograms.CMSMode.SIMULATION] = "Simulation"
    #histograms.createLegend.setDefaults(y1=0.93, y2=0.75, x1=0.52, x2=0.93)
    histograms.createLegend.moveDefaults(dx=-0.1, dh=-0.2)
    histograms.uncertaintyMode.set(histograms.uncertaintyMode.StatOnly)
    histograms.createLegendRatio.moveDefaults(dh=-0.1, dx=-0.53)
    plots._legendLabels["BackgroundStatError"] = "Norm. stat. unc."

    plotter = tauEmbedding.CommonPlotter(optMode, "mcembsig", drawPlotCommon)

    def dop(name, addData=False, **kwargs):
        doPlots(datasetsEmb, datasetsSig, name, plotter, optMode, addData, **kwargs)
#        doCounters(datasetsEmb, datasetsSig, name)

    dop("EWKMC", addData=True)
    dop("TTJets")
    dop("WJets")
    dop("DYJetsToLL", mtOnly=False)
    dop("SingleTop", mtOnly=False)
    dop("Diboson", mtOnly=False)
#    dop("DYJetsToLL", mtOnly=True)
#    dop("SingleTop", mtOnly=True)
#    dop("Diboson", mtOnly=True)


#drawPlotCommon = tauEmbedding.PlotDrawerTauEmbeddingEmbeddedNormal(ylabel="Events / %.0f GeV", stackMCHistograms=False, log=True, addMCUncertainty=True, ratio=True, addLuminosityText=True)
drawPlotCommon = plots.PlotDrawer(ylabel="Events / %.0f", stackMCHistograms=False, log=True, addMCUncertainty=True,
                                  ratio=True, ratioType="errorScale", ratioCreateLegend=True,
                                  addLuminosityText=True)

def strIntegral(th1):
    return "%.1f" % aux.th1Integral(th1)

def doPlots(datasetsEmb, datasetsSig, datasetName, plotter, optMode, addData, mtOnly=False):
    dsetEmb = datasetsEmb.getDataset(datasetName)
    dsetSig = datasetsSig.getDataset(datasetName)
    dsetEmbData = datasetsEmb.getDataset("Data")
    lumi = dsetEmbData.getLuminosity()

    addEventCounts = False
    
    def createPlot(name):
        if mtOnly and "shapeTransverseMass" not in name:
            return None

        drhEmb = dsetEmb.getDatasetRootHisto(name)
        drhSig = dsetSig.getDatasetRootHisto(name)
        drhEmb.normalizeToLuminosity(lumi)
        drhSig.normalizeToLuminosity(lumi)
        drhEmb.setName("Embedded")
        drhSig.setName("Normal")
        if addData:
            drhEmbData = dsetEmbData.getDatasetRootHisto(name)
            drhEmbData.setName("Embedded data")

        if addData:
            p = plots.ComparisonManyPlot(drhSig, [drhEmb, drhEmbData])
        else:
            p = plots.ComparisonManyPlot(drhSig, [drhEmb])
        p.setLuminosity(lumi)
        legLabel = plots._legendLabels.get(datasetName, datasetName)
        legEmb = "Embedded "+legLabel
        legSig = "Normal "+legLabel
        if addEventCounts:
            legEmb += " ("+strIntegral(drhEmb.getHistogram())+")"
            legSig += " ("+strIntegral(drhSig.getHistogram())+")"
        p.histoMgr.setHistoLegendLabelMany({
                "Embedded": legEmb,
                "Normal": legSig,
                })
        p.histoMgr.forEachHisto(styles.generator())
        if addData:
            p.histoMgr.setHistoLegendLabelMany({"Embedded data": "Embedded data ("+strIntegral(drhEmbData.getHistogram())+")"})
            p.histoMgr.forHisto("Embedded data", styles.dataStyle)
            p.histoMgr.setHistoDrawStyle("Embedded data", "EP")
            p.histoMgr.setHistoLegendStyle("Embedded data", "P")
            p.histoMgr.reorderDraw(["Embedded data"])
        p.setDrawOptions(ratioYlabel="Emb./Norm.")
        return p

    plotter.plot(datasetName, createPlot, {
        "NBjets": {"moveLegend": {"dx": -0.4, "dy": -0.45}}
    })



def doTauCounters(datasetsEmb, datasetsSig, datasetName, ntupleCacheEmb, ntupleCacheSig, normalizeEmb=True):
    lumi = datasetsEmb.getLuminosity()

    # Take unweighted counters for embedded, to get a handle on the muon isolation efficiency
    eventCounterEmb = tauEmbedding.EventCounterMany(datasetsEmb, counters="/"+tauAnalysisEmb+"Counters", normalize=normalizeEmb)
    eventCounterSig = counter.EventCounter(datasetsSig, counters="/"+tauAnalysisEmb+"Counters")

    def isNotThis(name):
        return name != datasetName

    eventCounterEmb.removeColumns(filter(isNotThis, datasetsEmb.getAllDatasetNames()))
    eventCounterSig.removeColumns(filter(isNotThis, datasetsSig.getAllDatasetNames()))

    eventCounterEmb.mainCounterAppendRows(ntupleCacheEmb.histogram("counters/weighted/counter"))
    eventCounterSig.getMainCounter().appendRows(ntupleCacheSig.histogram("counters/weighted/counter"))

    eventCounterSig.normalizeMCToLuminosity(lumi)

    table = counter.CounterTable()
    col = eventCounterEmb.getMainCounterTable().getColumn(name=datasetName)
    col.setName("Embedded")
    table.appendColumn(col)
    col = eventCounterSig.getMainCounterTable().getColumn(name=datasetName)
    col.setName("Normal")
    table.appendColumn(col)

    lastCountEmb = table.getCount(colName="Embedded", irow=table.getNrows()-1)
    lastCountNormal = table.getCount(colName="Normal", irow=table.getNrows()-1)

    postfix = ""
    if not normalizeEmb:
        postfix="_notEmbNormalized"

    effFormat = counter.TableFormatLaTeX(counter.CellFormatTeX(valueFormat="%.4f", withPrecision=2))
    countFormat = counter.TableFormatText(counter.CellFormatText(valueFormat="%.4f"),
                                          #columnSeparator="  ;"
                                          )

    fname = "counters_tau_"+datasetName+postfix+".txt"
    f = open(fname, "w")
    f.write(table.format(countFormat))
    f.write("\n")

    try:
        ratio = lastCountNormal.clone()
        ratio.divide(lastCountEmb)
        f.write("Normal/embedded = %.4f +- %.4f\n\n" % (ratio.value(), ratio.uncertainty()))
    except ZeroDivisionError:
        pass

    f.close()
    print "Printed tau counters to", fname
    
    if not normalizeEmb:
        return

    tableEff = counter.CounterTable()
    tableEff.appendColumn(counter.efficiencyColumn("Embedded eff", table.getColumn(name="Embedded")))
    tableEff.appendColumn(counter.efficiencyColumn("Normal eff", table.getColumn(name="Normal")))

    embeddingMuonIsolationEff = tableEff.getCount(rowName="tauEmbeddingMuonsCount", colName="Embedded eff")
    embeddingTauIsolationEff = tableEff.getCount(rowName="Isolation", colName="Embedded eff")
    embeddingTotalIsolationEff = embeddingMuonIsolationEff.clone()
    embeddingTotalIsolationEff.multiply(embeddingTauIsolationEff)

    # Remove unnecessary rows
    rowNames = [
#        "All events",
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
    tableEff.keepOnlyRows(rowNames)
    rowIndex = tableEff.getRowNames().index("Isolation")
    tableEff.insertRow(rowIndex, counter.CounterRow("Mu isolation (emb)", ["Embedded eff", "Normal eff"],
                                                    [embeddingMuonIsolationEff, None]))
    tableEff.insertRow(rowIndex+1, counter.CounterRow("Tau isolation (emb)", ["Embedded eff", "Normal eff"],
                                                      [embeddingTauIsolationEff, None]))
    tableEff.setCount2(embeddingTotalIsolationEff, rowName="Isolation", colName="Embedded eff")
    #tableEff.setCount2(None, rowName="pT > 15", colName="Normal eff")

    #print table.format(effFormat)
    fname = "counters_tau_"+datasetName+"_eff.txt"
    f = open(fname, "w")
    f.write(tableEff.format(effFormat))
    f.write("\n")
    f.close()
    print "Printed tau efficiencies to", fname

def doCounters(datasetsEmb, datasetsSig, datasetName, normalizeEmb=True):
    lumi = datasetsEmb.getLuminosity()

    # Counters
    eventCounterEmb = tauEmbedding.EventCounterMany(datasetsEmb, normalize=normalizeEmb) #, counters=analysisEmb+"/counters")
    eventCounterSig = counter.EventCounter(datasetsSig)

    def isNotThis(name):
        return name != datasetName

    eventCounterEmb.removeColumns(filter(isNotThis, datasetsEmb.getAllDatasetNames()))
    eventCounterSig.removeColumns(filter(isNotThis, datasetsSig.getAllDatasetNames()))
    eventCounterSig.normalizeMCToLuminosity(lumi)

    tdCount = dataset.TreeDraw("dummy", weight=tauEmbedding.signalNtuple.weightBTagging)
    tdCountMET = tdCount.clone(weight=tauEmbedding.signalNtuple.weight, selection=tauEmbedding.signalNtuple.metCut)
    tdCountBTagging = tdCount.clone(selection=And(tauEmbedding.signalNtuple.metCut, tauEmbedding.signalNtuple.bTaggingCut))
    tdCountDeltaPhi160 = tdCount.clone(selection=And(tauEmbedding.signalNtuple.metCut, tauEmbedding.signalNtuple.bTaggingCut, tauEmbedding.signalNtuple.deltaPhi160Cut))
    tdCountDeltaPhi130 = tdCount.clone(selection=And(tauEmbedding.signalNtuple.metCut, tauEmbedding.signalNtuple.bTaggingCut, tauEmbedding.signalNtuple.deltaPhi130Cut))
    def addRow(name, td):
        tdEmb = td.clone(tree=analysisEmb+"/tree")
        tdSig = td.clone(tree=analysisSig+"/tree")
        eventCounterEmb.mainCounterAppendRow(name, tdEmb)
        eventCounterSig.getMainCounter().appendRow(name, tdSig)

    # addRow("JetsForEffs", tdCount.clone(weight=tauEmbedding.signalNtuple.weight))
    # addRow("METForEffs", tdCountMET)
    # addRow("BTagging (SF)", tdCountBTagging)
    # addRow("DeltaPhi < 160", tdCountDeltaPhi160)
    # addRow("BTagging (SF) again", tdCountBTagging)
    # addRow("DeltaPhi < 130", tdCountDeltaPhi130)

    table = counter.CounterTable()
    col = eventCounterEmb.getMainCounterTable().getColumn(name=datasetName)
    col.setName("Embedded")
    table.appendColumn(col)
    col = eventCounterSig.getMainCounterTable().getColumn(name=datasetName)
    col.setName("Normal")
    table.appendColumn(col)

    tableTau = counter.CounterTable()
    tmp = "TauIDPassedEvt::TauSelection_HPS"
    col = eventCounterEmb.getSubCounterTable(tmp).getColumn(name=datasetName)
    col.setName("Embedded")
    tableTau.appendColumn(col)
    col = eventCounterSig.getSubCounterTable(tmp).getColumn(name=datasetName)
    col.setName("Normal")
    tableTau.appendColumn(col)

    postfix = ""
    if not normalizeEmb:
        postfix="_notEmbNormalized"

    fname = "counters_selections_%s%s.txt" % (datasetName, postfix)
    f = open(fname, "w")
    f.write(table.format())
    f.write("\n")
    f.write(tableTau.format())
    f.close()
    print "Printed selection counters to", fname

    if not normalizeEmb:
        return


    # Calculate efficiencies
    table.keepOnlyRows(["njets", "MET", "btagging", "btagging scale factor", "DeltaPhi(Tau,MET) upper limit"])
    # btag SF efficiency w.r.t. MET 
    row = table.getRow(name="MET")
    row.setName("METForEff")
    table.insertRow(3, row) 

    tableEff = counter.CounterTable()
    tableEff.appendColumn(counter.efficiencyColumn("Embedded eff", table.getColumn(name="Embedded")))
    tableEff.appendColumn(counter.efficiencyColumn("Normal eff", table.getColumn(name="Normal")))
    tableEff.removeRow(name="METForEff")

    effFormat = counter.TableFormatText(counter.CellFormatTeX(valueFormat='%.4f', withPrecision=2))

#    print table.format(effFormat)

    fname = "counters_selections_%s_eff.txt"%datasetName
    f = open(fname, "w")
    f.write(tableEff.format(effFormat))
    f.close()
    print "Printed selection efficiencies to", fname

if __name__ == "__main__":
    main()
