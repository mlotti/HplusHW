#!/usr/bin/env python

######################################################################
#
# This plot script is for comparing the embedded MC and normal MC
# within tau ID and signal analysis. The corresponding python job
# configurations are
# * embeddingAnalysis_cfg.py
# * tauAnalysis_cfg.py
# * signalAnalysis_cfg.py with "doPat=1 tauEmbeddingInput=1"
# * signalAnalysis_cfg.py with "doTauEmbeddingLikePreselection=1"
# for embedding tauID, normal tauID, embedded signal analysis, and
# normal signal analysis, respecitvely
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

tauAnalysisEmb = "tauNtuple"
tauAnalysisSig = "tauNtuple"

analysisEmb = "signalAnalysis"
analysisSig = "signalAnalysisTauEmbeddingLikePreselection"

dataEra = "Run2011AB"

def main():
    tauDirEmbs = [os.path.join("..", d) for d in tauEmbedding.tauDirEmbs]
    tauDirSig = "../"+tauEmbedding.tauDirSig

    dirEmbs = ["."] + [os.path.join("..", d) for d in tauEmbedding.dirEmbs[1:]]
#    dirSig = "../"+tauEmbedding.dirSig
    dirSig = "../"+tauEmbedding.tauDirSig

#    tauDirEmbs = tauDirEmbs[:2]
#    dirEmbs = dirEmbs[:2]

    tauDatasetsEmb = tauEmbedding.DatasetsMany(tauDirEmbs, tauAnalysisEmb+"Counters", normalizeMCByLuminosity=True)
    tauDatasetsSig = dataset.getDatasetsFromMulticrabCfg(cfgfile=tauDirSig+"/multicrab.cfg", counters=tauAnalysisSig+"Counters")
    datasetsEmb = tauEmbedding.DatasetsMany(dirEmbs, analysisEmb+"/counters", normalizeMCByLuminosity=True)
    datasetsSig = dataset.getDatasetsFromMulticrabCfg(cfgfile=dirSig+"/multicrab.cfg", counters=analysisSig+"/counters")

    tauDatasetsSig.updateNAllEventsToPUWeighted()
    datasetsSig.updateNAllEventsToPUWeighted()

    tauDatasetsEmb.forEach(plots.mergeRenameReorderForDataMC)
    datasetsEmb.forEach(plots.mergeRenameReorderForDataMC)
#    tauDatasetsEmb.setLumiFromData()
    datasetsEmb.setLumiFromData()
    tauDatasetsEmb.lumi = datasetsEmb.getLuminosity()
    plots.mergeRenameReorderForDataMC(tauDatasetsSig)
    plots.mergeRenameReorderForDataMC(datasetsSig)

    def mergeEWK(datasets):
        datasets.merge("EWKMC", ["WJets", "TTJets", "DYJetsToLL", "SingleTop", "Diboson"], keepSources=True)
    #mergeEWK(tauDatasetsSig)
    #mergeEWK(datasetsSig)
    #tauDatasetsEmb.forEach(mergeEWK)
    #datasetsEmb.forEach(mergeEWK)
    #plots._legendLabels["EWKMC"] = "EWK"

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    histograms.cmsTextMode = histograms.CMSMode.SIMULATION
    histograms.cmsText[histograms.CMSMode.SIMULATION] = "Simulation"
    histograms.createLegend.setDefaults(y1=0.93, y2=0.75, x1=0.52, x2=0.93)
    tauEmbedding.normalize = True
    tauEmbedding.era = "Run2011AB"

    f = open("datasetInfo.txt", "w")
    f.write("Tau analysis, embedded\n")
    f.write(tauDatasetsEmb.getFirstDatasetManager().formatInfo())
    f.write("\n")
    f.write("Tau analysis, normal\n")
    f.write(tauDatasetsSig.formatInfo())
    f.write("\n")
    f.write("Signal analysis, embedded\n")
    f.write(datasetsEmb.getFirstDatasetManager().formatInfo())
    f.write("\n")
    f.write("Signal analysis, normal\n")
    f.write(datasetsSig.formatInfo())
    f.write("\n")

    
    selectorArgs = [tauEmbedding.tauNtuple.weight[dataEra]]
    #selectorArgs = [""]
    process = True
    #process = False
    maxEvents = -1
    #maxEvents = 100000
    ntupleCacheEmb = dataset.NtupleCache(tauAnalysisEmb+"/tree", "TauAnalysisSelector",
                                         selectorArgs=selectorArgs+[True],
                                         process=process, maxEvents=maxEvents,
                                         cacheFileName="histogramCacheEmb.root"
                                         )
    ntupleCacheSig = dataset.NtupleCache(tauAnalysisEmb+"/tree", "TauAnalysisSelector",
                                         selectorArgs=selectorArgs+[False],
                                         process=process, maxEvents=maxEvents,
                                         cacheFileName="histogramCacheSig.root"
                                         )

    def dop(name):
#        doTauPlots(tauDatasetsEmb, tauDatasetsSig, name, ntupleCacheEmb, ntupleCacheSig)
        doTauCounters(tauDatasetsEmb, tauDatasetsSig, name, ntupleCacheEmb, ntupleCacheSig)
        doTauCounters(tauDatasetsEmb, tauDatasetsSig, name, ntupleCacheEmb, ntupleCacheSig, normalizeEmb=False)

#        doPlots(datasetsEmb, datasetsSig, name)
        doCounters(datasetsEmb, datasetsSig, name)
        doCounters(datasetsEmb, datasetsSig, name, normalizeEmb=False)

    dop("TTJets")
#    dop("WJets")
#    dop("DYJetsToLL")
#    dop("SingleTop")
#    dop("Diboson")


drawPlotCommon = tauEmbedding.PlotDrawerTauEmbeddingEmbeddedNormal(ylabel="Events / %.0f GeV/c", stackMCHistograms=False, log=True, addMCUncertainty=True, ratio=True, addLuminosityText=True)

def doTauPlots(datasetsEmb, datasetsSig, datasetName, ntupleCacheEmb, ntupleCacheSig):
    lumi = datasetsEmb.getLuminosity()

    createPlot = tauEmbedding.PlotCreatorMany(tauAnalysisEmb, tauAnalysisSig, datasetsEmb, datasetsSig, datasetName, styles.getStyles(),
                                              ntupleCacheEmb=ntupleCacheEmb, ntupleCacheSig=ntupleCacheSig)

    opts2def = {
        "DYJetsToLL": {"ymin":0, "ymax": 1.5}
        }.get(datasetName, {"ymin": 0.8, "ymax": 1.2})
    moveLegend = {"DYJetsToLL": {"dx": -0.02}}.get(datasetName, {})

    def drawPlot(plot, name, *args, **kwargs):
        drawPlotCommon(plot, "mcembsig_"+datasetName+"_"+name, *args, **kwargs)

    # Decay mode finding
    postfix = "_1AfterDecayModeFindingIsolation"
    opts2 = opts2def
    drawPlot(createPlot(ntupleCacheEmb.histogram("tauEta_AfterDecayModeFindingIsolation")),
             "tauEta"+postfix, "#tau-jet candidate #eta", ylabel="Events / %.1f", opts={"ymin": 1e-1}, opts2=opts2, moveLegend={"dx": -0.2, "dy": -0.45}, cutLine=[-2.1, 2.1])
    drawPlot(createPlot(ntupleCacheEmb.histogram("tauPt_AfterDecayModeFindingIsolation")),
             "tauPt"+postfix, "#tau-jet candidate p_{T} (GeV/c)", opts2=opts2, cutLine=40, moveLegend=moveLegend)
    drawPlot(createPlot(ntupleCacheEmb.histogram("vertexCount_AfterDecayModeFindingIsolation")),
             "vertexCount"+postfix, "Number of good PV", opts2=opts2, ylabel="Events / %.f")

    # Eta cut
    postfix = "_2AfterEtaCut"
    drawPlot(createPlot(ntupleCacheEmb.histogram("tauPt_AfterEtaCutIsolation")),
             "tauPt"+postfix, "#tau-jet candidate p_{T} (GeV/c)", opts2=opts2, cutLine=40, moveLegend=moveLegend)
    drawPlot(createPlot(ntupleCacheEmb.histogram("vertexCount_AfterEtaCutIsolation")),
             "vertexCount"+postfix, "Number of good PV", opts2=opts2, ylabel="Events / %.f")

    # Pt cut
    postfix = "_3AfterPtCut"
    drawPlot(createPlot(ntupleCacheEmb.histogram("tauPhi_AfterPtCutIsolation")),
             "tauPhi"+postfix, "#tau-jet candidate #phi (rad)", ylabel="Events / %.1f", opts={"ymin": 1e-1}, opts2=opts2, moveLegend={"dx": -0.2, "dy": -0.45})
    opts2 = {"Diboson": {"ymin": 0, "ymax": 1.5}}.get(datasetName, opts2def)
    drawPlot(createPlot(ntupleCacheEmb.histogram("tauLeadingTrackPt_AfterPtCutIsolation")),
             "tauLeadingTrackPt"+postfix, "#tau-jet ldg. charged particle p_{T} (GeV/c)", opts2=opts2, cutLine=20, moveLegend=moveLegend)
    opts2 = opts2def
    drawPlot(createPlot(ntupleCacheEmb.histogram("vertexCount_AfterPtCutIsolation")),
             "vertexCount"+postfix, "Number of good PV", opts2=opts2, ylabel="Events / %.f")

    # Tau candidate selection + isolation
    postfix = "_4AfterIsolation"
    opts2 = {"EWKMC": {"ymin": 0.5, "ymax": 2}}.get(datasetName, opts2def)
    drawPlot(createPlot(ntupleCacheEmb.histogram("tauDecayMode_AfterIsolation")),
             "tauDecayMode"+postfix+"", "", opts={"ymin": 1e-2, "ymaxfactor": 20, "nbins":5}, opts2=opts2,
             moveLegend=moveLegend,
             #moveLegend={"dy": 0.02, "dh": -0.02},
             customise=tauEmbedding.decayModeCustomize)
    opts2 = opts2def
    drawPlot(createPlot(ntupleCacheEmb.histogram("vertexCount_AfterIsolation")),
             "vertexCount"+postfix, "Number of good PV", opts2=opts2, ylabel="Events / %.f")

    # One prong
    postfix = "_5AfterOneProng"
    #drawPlot(createPlot(td.clone(varexp="taus_p4.Pt()>>tmp(25,0,250)")),
    #         "tauPt"+postfix, "#tau-jet candidate p_{T} (GeV/c)", opts2={"ymin": 0, "ymax": 2})
    #drawPlot(createPlot(td.clone(varexp="taus_p4.P()>>tmp(25,0,250)")),
    #         "tauP"+postfix, "#tau-jet candidate p (GeV/c)", opts2={"ymin": 0, "ymax": 2})
    #drawPlot(createPlot(td.clone(varexp="taus_leadPFChargedHadrCand_p4.Pt()>>tmp(25,0,250)")),
    #         "tauLeadingTrackPt"+postfix, "#tau-jet ldg. charged particle p_{T} (GeV/c)", opts2={"ymin":0, "ymax": 2})
    #drawPlot(createPlot(td.clone(varexp="taus_leadPFChargedHadrCand_p4.P()>>tmp(25,0,250)")),
    #         "tauLeadingTrackP"+postfix, "#tau-jet ldg. charged particle p (GeV/c)", opts2={"ymin":0, "ymax": 2})
    drawPlot(createPlot(ntupleCacheEmb.histogram("tauRtau_AfterOneProng")),
             "rtau"+postfix, "R_{#tau} = p^{ldg. charged particle}/p^{#tau jet}", ylabel="Events / %.1f", opts={"ymin": 1e-2, "ymaxfactor": 5}, opts2=opts2, moveLegend={"dx":-0.34}, cutLine=0.7)
    drawPlot(createPlot(ntupleCacheEmb.histogram("vertexCount_AfterOneProng")),
             "vertexCount"+postfix, "Number of good PV", opts2=opts2, ylabel="Events / %.f")

    # Full ID
    postfix = "_6AfterTauID"
    drawPlot(createPlot(ntupleCacheEmb.histogram("tauPt_AfterRtau")),
             "tauPt"+postfix, "#tau-jet p_{T} (GeV/c)", opts2=opts2, moveLegend=moveLegend)
    drawPlot(createPlot(ntupleCacheEmb.histogram("vertexCount_AfterRtau")),
             "vertexCount"+postfix, "Number of good PV", opts2=opts2, ylabel="Events / %.f")


def doPlots(datasetsEmb, datasetsSig, datasetName):
    lumi = datasetsEmb.getLuminosity()
    
    createPlot = tauEmbedding.PlotCreatorMany(analysisEmb, analysisSig, datasetsEmb, datasetsSig, datasetName, styles.getStyles())
    def drawPlot(plot, name, *args, **kwargs):
        drawPlotCommon(plot, "mcembsig_"+datasetName+"_"+name, *args, **kwargs)
    def createDrawPlot(name, *args, **kwargs):
        p = createPlot(name)
        drawPlot(plot, *args, **kwargs)

    opts2def = {"ymin": 0.8, "ymax": 1.2}
    def drawControlPlot(path, xlabel, rebin=None, opts2=None, **kwargs):
        opts2_ = opts2def
        if opts2 != None:
            opts_ = opts2
        cargs = {}
        if rebin != None:
            cargs["rebin"] = rebin
        drawPlot(createPlot("ControlPlots/"+path, **cargs), path, xlabel, opts2=opts2_, **kwargs)

    def update(d1, d2):
        tmp = {}
        tmp.update(d1)
        tmp.update(d2)
        return tmp

    # Control plots
    optsdef = {}
    opts = optsdef

    # After Njets
    moveLegend = {"DYJetsToLL": {"dx": -0.02}}.get(datasetName, {})
    drawControlPlot("MET",
                    #"Uncorrected PF E_{T}^{miss} (GeV)",
                    "Type I PF E_{T}^{miss} (GeV)",
                    rebin=5, opts=update(opts, {"xmax": 400}), cutLine=50, moveLegend=moveLegend)

    # after MET
    moveLegend = {"dx": -0.23, "dy": -0.5}
    moveLegend = {
        "WJets": {},
        "DYJetsToLL": {"dx": -0.02},
        "SingleTop": {},
        "Diboson": {}
        }.get(datasetName, moveLegend)
    drawControlPlot("NBjets", "Number of selected b jets", opts=update(opts, {"xmax": 6}), ylabel="Events", moveLegend=moveLegend, cutLine=1)

    # DeltapPhi
    xlabel = "#Delta#phi(#tau jet, E_{T}^{miss}) (^{o})"
    def customDeltaPhi(h):
        yaxis = h.getFrame().GetYaxis()
        yaxis.SetTitleOffset(0.8*yaxis.GetTitleOffset())
    opts = {
#        "WJets": {"ymax": 35},
#        "DYJetsToLL": {"ymax": 12},
#        "Diboson": {"ymax": 1},
        }.get(datasetName, {"ymaxfactor": 1.2})
    opts2=opts2def
    moveLegend = {
        "DYJetsToLL": {"dx": -0.24},
        }.get(datasetName, {"dx":-0.22})
    drawPlot(createPlot("deltaPhi"), "deltaPhi_3AfterBTagging", xlabel, log=False, opts=opts, opts2=opts2, rebin=10,
             ylabel="Events / %.0f^{o}", function=customDeltaPhi, moveLegend=moveLegend, cutLine=[160])

    # Transverse mass
    opts = {
#        "TTJets": {"ymax": 28},
#        "SingleTop": {"ymax": 4.5},
#        "DYJetsToLL": {"ymax": 18},
#        "Diboson": {"ymax": 1.2},
#        "WJets": {"ymax": 50},
        }.get(datasetName, {})
    opts["xmax"] = 300
    #opts2 = {"ymin": 0, "ymax": 2}
    moveLegend = {"DYJetsToLL": {"dx": -0.02}}.get(datasetName, {})
    p = createPlot("transverseMass")
    #p.appendPlotObject(histograms.PlotText(0.6, 0.7, "#Delta#phi(#tau jet, E_{T}^{miss}) < 160^{o}", size=20))
    drawPlot(p, "transverseMass_4AfterDeltaPhi", "m_{T}(#tau jet, E_{T}^{miss}) (GeV/c^{2})", opts=opts, opts2=opts2, rebin=10, ylabel="Events / %.0f GeV/c^{2}", log=False, moveLegend=moveLegend)


def doTauCounters(datasetsEmb, datasetsSig, datasetName, ntupleCacheEmb, ntupleCacheSig, normalizeEmb=True):
    lumi = datasetsEmb.getLuminosity()

    # Take unweighted counters for embedded, to get a handle on the muon isolation efficiency
    eventCounterEmb = tauEmbedding.EventCounterMany(datasetsEmb, counters=tauAnalysisEmb+"Counters", normalize=normalizeEmb)
    eventCounterSig = counter.EventCounter(datasetsSig, counters=tauAnalysisEmb+"Counters")

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

    postfix = ""
    if not normalizeEmb:
        postfix="_notEmbNormalized"

    effFormat = counter.TableFormatLaTeX(counter.CellFormatTeX(valueFormat="%.4f", withPrecision=2))
    countFormat = counter.TableFormatText(counter.CellFormatText(valueFormat="%.4f"), columnSeparator="  ;")

    fname = "counters_tau_"+datasetName+postfix+".txt"
    f = open(fname, "w")
    f.write(table.format(countFormat))
    f.write("\n")
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
