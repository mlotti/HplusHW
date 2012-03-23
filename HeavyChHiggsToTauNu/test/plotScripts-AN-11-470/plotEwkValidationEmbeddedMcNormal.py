#!/usr/bin/env python

######################################################################
#
# This plot script is for comparing the embedded MC and normal MC
# within tau ID and signal analysis. The corresponding python job
# configurations are
# * embeddingAnalysis_cfg.py
# * tauAnalysis_cfg.py
# * signalAnalysis_cfg.py with "doPat=1 tauEmbeddingInput=1"
# * signalAnalysis_cfg.py
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

counters = "Counters/weighted"

def main():
    tauDirEmbs = [os.path.join("..", d) for d in tauEmbedding.tauDirEmbs]
    tauDirSig = "../"+tauEmbedding.tauDirSig

    dirEmbs = ["."] + [os.path.join("..", d) for d in tauEmbedding.dirEmbs[1:]]
    dirSig = "../"+tauEmbedding.dirSig

#    tauDirEmbs = tauDirEmbs[:2]
#    dirEmbs = dirEmbs[:2]

    tauDatasetsEmb = tauEmbedding.DatasetsMany(tauDirEmbs, tauAnalysisEmb+"Counters", normalizeMCByLuminosity=True)
    tauDatasetsSig = dataset.getDatasetsFromMulticrabCfg(cfgfile=tauDirSig+"/multicrab.cfg", counters=tauAnalysisSig+"Counters")
    datasetsEmb = tauEmbedding.DatasetsMany(dirEmbs, analysisEmb+"Counters", normalizeMCByLuminosity=True)
    datasetsSig = dataset.getDatasetsFromMulticrabCfg(cfgfile=dirSig+"/multicrab.cfg", counters=analysisSig+"Counters")

    tauDatasetsEmb.forEach(plots.mergeRenameReorderForDataMC)
    datasetsEmb.forEach(plots.mergeRenameReorderForDataMC)
    tauDatasetsEmb.setLumiFromData()
    datasetsEmb.setLumiFromData()
    plots.mergeRenameReorderForDataMC(tauDatasetsSig)
    plots.mergeRenameReorderForDataMC(datasetsSig)

    def mergeEWK(datasets):
        datasets.merge("EWKMC", ["WJets", "TTJets", "DYJetsToLL", "SingleTop", "Diboson"], keepSources=True)
    mergeEWK(tauDatasetsSig)
    mergeEWK(datasetsSig)
    tauDatasetsEmb.forEach(mergeEWK)
    datasetsEmb.forEach(mergeEWK)
    plots._legendLabels["EWKMC"] = "EWK"

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    histograms.createLegend.setDefaults(y1=0.93, y2=0.75, x1=0.52, x2=0.93)
    tauEmbedding.normalize = True
    tauEmbedding.era = "Run2011A"

    def dop(name):
        doTauPlots(tauDatasetsEmb, tauDatasetsSig, name)
        doTauCounters(tauDatasetsEmb, tauDatasetsSig, name)
        doPlots(datasetsEmb, datasetsSig, name)
        doCounters(datasetsEmb, datasetsSig, name)

    dop("TTJets")
    dop("WJets")
    dop("DYJetsToLL")
    dop("SingleTop")
    dop("Diboson")


drawPlotCommon = tauEmbedding.PlotDrawerTauEmbeddingEmbeddedNormal(ylabel="Events / %.0f GeV/c", stackMCHistograms=False, log=True, addMCUncertainty=True, ratio=True)

def doTauPlots(datasetsEmb, datasetsSig, datasetName):
    lumi = datasetsEmb.getLuminosity()

    createPlot = tauEmbedding.PlotCreatorMany(tauAnalysisEmb, tauAnalysisSig, datasetsEmb, datasetsSig, datasetName, styles.getStyles())

    opts2def = {"DYJetsToLL": {"ymin":0, "ymax": 1.5}}.get(datasetName, {"ymin": 0.5, "ymax": 1.5})

    treeDraw = dataset.TreeDraw("dummy", weight=tauEmbedding.tauNtuple.weight[tauEmbedding.era])
    def drawPlot(plot, name, *args, **kwargs):
        drawPlotCommon(plot, "mcembsig_"+datasetName+"_"+name, *args, **kwargs)

    # Decay mode finding
    postfix = "_1AfterDecayModeFindingIsolationPtPre"
    selection = And(*[getattr(tauEmbedding.tauNtuple, cut) for cut in ["decayModeFinding", "tightIsolation", "tauPtPreCut"]])
    opts2 = opts2def
    drawPlot(createPlot(treeDraw.clone(varexp="taus_p4.Eta()>>tmp(25,-2.5,2.5", selection=selection)),
             "tauEta"+postfix, "#tau-jet candidate #eta", ylabel="Events / %.1f", opts={"ymin": 1e-1}, opts2=opts2, moveLegend={"dx": -0.2, "dy": -0.45}, cutLine=[-2.1, 2.1])
    drawPlot(createPlot(treeDraw.clone(varexp="taus_p4.Pt()>>tmp(25,0,250)", selection=selection)),
             "tauPt"+postfix, "#tau-jet candidate p_{T} (GeV/c)", opts2=opts2, cutLine=40)

    # Eta cut
    postfix = "_2AfterEtaCut"
    selection = And(*[getattr(tauEmbedding.tauNtuple, cut) for cut in ["decayModeFinding", "tightIsolation", "tauPtPreCut", "tauEtaCut"]])
    drawPlot(createPlot(treeDraw.clone(varexp="taus_p4.Eta()>>tmp(25,-2.5,2.5", selection=selection)),
             "tauEta"+postfix, "#tau-jet candidate #eta", ylabel="Events / %.1f", opts={"ymin": 1e-1}, opts2=opts2, moveLegend={"dx": -0.2, "dy": -0.45}, cutLine=[-2.1, 2.1])
    drawPlot(createPlot(treeDraw.clone(varexp="taus_p4.Pt()>>tmp(25,0,250)", selection=selection)),
             "tauPt"+postfix, "#tau-jet candidate p_{T} (GeV/c)", opts2=opts2, cutLine=40)

    # Pt cut
    postfix = "_3AfterPtCut"
    selection = And(*[getattr(tauEmbedding.tauNtuple, cut) for cut in ["decayModeFinding", "tightIsolation", "tauEtaCut", "tauPtCut"]])
    drawPlot(createPlot(treeDraw.clone(varexp="taus_p4.Phi()>>tmp(32,-3.2,3.2", selection=selection)),
             "tauPhi"+postfix, "#tau-jet candidate #phi (rad)", ylabel="Events / %.1f", opts={"ymin": 1e-1}, opts2=opts2, moveLegend={"dx": -0.2, "dy": -0.45})
    opts2 = {"Diboson": {"ymin": 0, "ymax": 1.5}}.get(datasetName, opts2def)
    drawPlot(createPlot(treeDraw.clone(varexp="taus_leadPFChargedHadrCand_p4.Pt()>>tmp(25,0,250)", selection=selection)),
             "tauLeadingTrackPt"+postfix, "#tau-jet ldg. charged particle p_{T} (GeV/c)", opts2=opts2, cutLine=20)
    opts2 = opts2def

    # Tau candidate selection
    postfix = "_4AfterTauCandidateSelection"
    selection = tauEmbedding.tauNtuple.tauCandidateSelection
    opts2 = {"EWKMC": {"ymin": 0.5, "ymax": 2}}.get(datasetName, opts2def)
    drawPlot(createPlot(treeDraw.clone(varexp=tauEmbedding.tauNtuple.decayModeExpression, selection=selection)),
             "tauDecayMode"+postfix+"", "", opts={"ymin": 1e-2, "ymaxfactor": 20, "nbins":5}, opts2=opts2,
             #moveLegend={"dy": 0.02, "dh": -0.02},
             customise=tauEmbedding.decayModeCustomize)
    opts2 = opts2def

    # One prong
    postfix = "_5AfterOneProng"
    td = treeDraw.clone(selection=And(*[getattr(tauEmbedding.tauNtuple, cut) for cut in ["tauCandidateSelection", "oneProng"]]))
    #drawPlot(createPlot(td.clone(varexp="taus_p4.Pt()>>tmp(25,0,250)")),
    #         "tauPt"+postfix, "#tau-jet candidate p_{T} (GeV/c)", opts2={"ymin": 0, "ymax": 2})
    #drawPlot(createPlot(td.clone(varexp="taus_p4.P()>>tmp(25,0,250)")),
    #         "tauP"+postfix, "#tau-jet candidate p (GeV/c)", opts2={"ymin": 0, "ymax": 2})
    #drawPlot(createPlot(td.clone(varexp="taus_leadPFChargedHadrCand_p4.Pt()>>tmp(25,0,250)")),
    #         "tauLeadingTrackPt"+postfix, "#tau-jet ldg. charged particle p_{T} (GeV/c)", opts2={"ymin":0, "ymax": 2})
    #drawPlot(createPlot(td.clone(varexp="taus_leadPFChargedHadrCand_p4.P()>>tmp(25,0,250)")),
    #         "tauLeadingTrackP"+postfix, "#tau-jet ldg. charged particle p (GeV/c)", opts2={"ymin":0, "ymax": 2})
    drawPlot(createPlot(td.clone(varexp=tauEmbedding.tauNtuple.rtauExpression+">>tmp(22, 0, 1.1)")),
             "rtau"+postfix, "R_{#tau} = p^{ldg. charged particle}/p^{#tau jet}", ylabel="Events / %.1f", opts={"ymin": 1e-2, "ymaxfactor": 5}, opts2=opts2, moveLegend={"dx":-0.34}, cutLine=0.7)

    # Full ID
    postfix = "_6AfterTauID"
    selection = And(*[getattr(tauEmbedding.tauNtuple, cut) for cut in ["tauCandidateSelection", "tauID"]])
    drawPlot(createPlot(treeDraw.clone(varexp="taus_p4.Pt()>>tmp(25,0,250)", selection=selection)),
             "tauPt"+postfix, "#tau-jet p_{T} (GeV/c)", opts2=opts2)


def doPlots(datasetsEmb, datasetsSig, datasetName):
    lumi = datasetsEmb.getLuminosity()
    
    createPlot = tauEmbedding.PlotCreatorMany(analysisEmb, analysisSig, datasetsEmb, datasetsSig, datasetName, styles.getStyles())
    def drawPlot(plot, name, *args, **kwargs):
        drawPlotCommon(plot, "mcembsig_"+datasetName+"_"+name, *args, **kwargs)
    def createDrawPlot(name, *args, **kwargs):
        p = createPlot(name)
        drawPlot(plot, *args, **kwargs)

    opts2def = {"ymin": 0, "ymax": 2}
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
    drawControlPlot("MET", "Uncorrected PF E_{T}^{miss} (GeV)", rebin=5, opts=update(opts, {"xmax": 400}), cutLine=50)

    # after MET
    moveLegend = {"dx": -0.23, "dy": -0.5}
    moveLegend = {
        "WJets": {},
        "DYJetsToLL": {},
        "SingleTop": {},
        "Diboson": {}
        }.get(datasetName, moveLegend)
    drawControlPlot("NBjets", "Number of selected b jets", opts=update(opts, {"xmax": 6}), ylabel="Events", moveLegend=moveLegend, cutLine=1)

    # Tree cut definitions
    treeDraw = dataset.TreeDraw("dummy", weight=tauEmbedding.signalNtuple.weightBTagging)
    tdDeltaPhi = treeDraw.clone(varexp="%s >>tmp(18, 0, 180)" % tauEmbedding.signalNtuple.deltaPhiExpression)
    tdMt = treeDraw.clone(varexp="%s >>tmp(20,0,400)" % tauEmbedding.signalNtuple.mtExpression)

    # DeltapPhi
    xlabel = "#Delta#phi(#tau jet, E_{T}^{miss}) (^{o})"
    def customDeltaPhi(h):
        yaxis = h.getFrame().GetYaxis()
        yaxis.SetTitleOffset(0.8*yaxis.GetTitleOffset())
    opts = {
        "WJets": {"ymax": 35},
        "DYJetsToLL": {"ymax": 12},
        "Diboson": {"ymax": 1},
        }.get(datasetName, {"ymaxfactor": 1.2})
    opts2=opts2def
    drawPlot(createPlot(tdDeltaPhi.clone(selection=And(tauEmbedding.signalNtuple.metCut, tauEmbedding.signalNtuple.bTaggingCut))), "deltaPhi_3AfterBTagging", xlabel, log=False, opts=opts, opts2=opts2, ylabel="Events / %.0f^{o}", function=customDeltaPhi, moveLegend={"dx":-0.22}, cutLine=[130, 160])

    # Transverse mass
    selection = And(*[tauEmbedding.signalNtuple.metCut, tauEmbedding.signalNtuple.bTaggingCut, tauEmbedding.signalNtuple.deltaPhi160Cut])
    opts = {
        "TTJets": {"ymax": 28},
        "SingleTop": {"ymax": 4.5},
        "DYJetsToLL": {"ymax": 18},
        "Diboson": {"ymax": 1.2},
        "WJets": {"ymax": 50},
        }.get(datasetName, {})
    opts2 = {"ymin": 0, "ymax": 2}
    p = createPlot(tdMt.clone(selection=selection))
    p.appendPlotObject(histograms.PlotText(0.6, 0.7, "#Delta#phi(#tau jet, E_{T}^{miss}) < 160^{o}", size=20))
    drawPlot(p, "transverseMass_4AfterDeltaPhi160", "m_{T}(#tau jet, E_{T}^{miss}) (GeV/c^{2})", opts=opts, opts2=opts2, ylabel="Events / %.0f GeV/c^{2}", log=False)


def doTauCounters(datasetsEmb, datasetsSig, datasetName):
    lumi = datasetsEmb.getLuminosity()
    treeDraw = dataset.TreeDraw("dummy", weight=tauEmbedding.tauNtuple.weight[tauEmbedding.era])

    eventCounterEmb = tauEmbedding.EventCounterMany(datasetsEmb, counters=tauAnalysisEmb+"Counters")
    eventCounterSig = counter.EventCounter(datasetsSig, counters=tauAnalysisSig+"Counters")

    def isNotThis(name):
        return name != datasetName

    eventCounterEmb.removeColumns(filter(isNotThis, datasetsEmb.getAllDatasetNames()))
    eventCounterSig.removeColumns(filter(isNotThis, datasetsSig.getAllDatasetNames()))
    eventCounterSig.normalizeMCToLuminosity(lumi)

    effFormat = counter.TableFormatLaTeX(counter.CellFormatTeX(valueFormat="%.4f", withPrecision=2))

    tdEmb = treeDraw.clone(tree=tauAnalysisEmb+"/tree")
    tdSig = treeDraw.clone(tree=tauAnalysisSig+"/tree")
    selectionsCumulative = []
    tauSelectionsCumulative = []
    rowNames = []
    def sel(name, selection):
        selectionsCumulative.append(selection)
        sel = selectionsCumulative[:]
        if len(tauSelectionsCumulative) > 0:
            sel += ["Sum$(%s) >= 1" % "&&".join(tauSelectionsCumulative)]
        sel = "&&".join(sel)
        eventCounterEmb.mainCounterAppendRow(name, tdEmb.clone(selection=sel))
        eventCounterSig.getMainCounter().appendRow(name, tdSig.clone(selection=sel))
        rowNames.append(name)
    def tauSel(name, selection):
        tauSelectionsCumulative.append(selection)
        sel = selectionsCumulative[:]
        if len(tauSelectionsCumulative) > 0:
            sel += ["Sum$(%s) >= 1" % "&&".join(tauSelectionsCumulative)]
        sel = "&&".join(sel)
        eventCounterEmb.mainCounterAppendRow(name, tdEmb.clone(selection=sel))
        eventCounterSig.getMainCounter().appendRow(name, tdSig.clone(selection=sel))
        rowNames.append(name)

    sel(">= 1 tau candidate", "Length$(taus_p4) >= 1")
    tauSel("Decay mode finding", tauEmbedding.tauNtuple.decayModeFinding)
    tauSel("pT > 15", "taus_p4.Pt() > 15")
    tauSel("pT > 40", tauEmbedding.tauNtuple.tauPtCut)
    tauSel("eta < 2.1", tauEmbedding.tauNtuple.tauEtaCut)
    tauSel("leading track pT > 20", tauEmbedding.tauNtuple.tauLeadPt)
    tauSel("ECAL fiducial", tauEmbedding.tauNtuple.ecalFiducial)
    tauSel("againstElectron", tauEmbedding.tauNtuple.electronRejection)
    tauSel("againstMuon", tauEmbedding.tauNtuple.muonRejection)
    tauSel("isolation", tauEmbedding.tauNtuple.tightIsolation)
    tauSel("oneProng", tauEmbedding.tauNtuple.oneProng)
    tauSel("Rtau", tauEmbedding.tauNtuple.rtau)
    sel("MET", tauEmbedding.tauNtuple.metSelection)

    table = counter.CounterTable()
    col = eventCounterEmb.getMainCounterTable().getColumn(name=datasetName)
    table.appendColumn(counter.efficiencyColumn("Embedded eff", col))
    col = eventCounterSig.getMainCounterTable().getColumn(name=datasetName)
    table.appendColumn(counter.efficiencyColumn("Normal eff", col))

    embeddingMuonIsolationEff = table.getCount(rowName="tauEmbeddingMuonsCount", colName="Embedded eff")
    embeddingTauIsolationEff = table.getCount(rowName="isolation", colName="Embedded eff")
    embeddingTotalIsolationEff = embeddingMuonIsolationEff.clone()
    embeddingTotalIsolationEff.multiply(embeddingTauIsolationEff)

    # Remove unnecessary rows
    del rowNames[0]
    table.keepOnlyRows(rowNames)
    rowIndex = table.getRowNames().index("isolation")
    table.insertRow(rowIndex, counter.CounterRow("Mu isolation (emb)", ["Embedded eff", "Normal eff"],
                                                 [embeddingMuonIsolationEff, None]))
    table.insertRow(rowIndex+1, counter.CounterRow("Tau isolation (emb)", ["Embedded eff", "Normal eff"],
                                                   [embeddingTauIsolationEff, None]))
    table.setCount2(embeddingTotalIsolationEff, rowName="isolation", colName="Embedded eff")
    table.setCount2(None, rowName="pT > 15", colName="Normal eff")

    #print table.format(effFormat)
    fname = "counters_tau_"+datasetName+".txt"
    f = open(fname, "w")
    f.write(table.format(effFormat))
    f.write("\n")
    f.close()
    print "Printed tau counters to", fname

def doCounters(datasetsEmb, datasetsSig, datasetName):
    lumi = datasetsEmb.getLuminosity()

    # Counters
    eventCounterEmb = tauEmbedding.EventCounterMany(datasetsEmb, counters=analysisEmb+"Counters/weighted")
    eventCounterSig = counter.EventCounter(datasetsSig, counters=analysisSig+"Counters/weighted")

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

    addRow("JetsForEffs", tdCount.clone(weight=tauEmbedding.signalNtuple.weight))
    addRow("METForEffs", tdCountMET)
    addRow("BTagging (SF)", tdCountBTagging)
    addRow("DeltaPhi < 160", tdCountDeltaPhi160)
    addRow("BTagging (SF) again", tdCountBTagging)
    addRow("DeltaPhi < 130", tdCountDeltaPhi130)

    table = counter.CounterTable()
    col = eventCounterEmb.getMainCounterTable().getColumn(name=datasetName)
    table.appendColumn(counter.efficiencyColumn("Embedded eff", col))
    col = eventCounterSig.getMainCounterTable().getColumn(name=datasetName)
    table.appendColumn(counter.efficiencyColumn("Normal eff", col))

    table.keepOnlyRows(["btagging", "METForEffs", "BTagging (SF)", "DeltaPhi < 160", "DeltaPhi < 130"])
    row = table.getRow(name="btagging")
    table.removeRow(name="btagging")
    table.insertRow(1, row)
    table.renameRows({
            "METForEffs": "MET > 50",
            "btagging": "b tagging",
            "BTagging (SF)": "b tagging with SF (w.r.t MET)",
            "DeltaPhi < 130": "DeltaPhi < 130 (w.r.t. btagSF)"
            })

    effFormat = counter.TableFormatText(counter.CellFormatTeX(valueFormat='%.4f', withPrecision=2))

#    print table.format(effFormat)

    fname = "counters_selections_%s.txt"%datasetName
    f = open(fname, "w")
    f.write(table.format(effFormat))
    f.close()
    print "Printed selection counters to", fname

if __name__ == "__main__":
    main()
