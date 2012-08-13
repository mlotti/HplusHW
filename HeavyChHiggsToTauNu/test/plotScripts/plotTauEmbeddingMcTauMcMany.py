#!/usr/bin/env python

######################################################################
#
# This plot script is for comparing the embedded MC to normal MC
# within the tau ID. The corresponding python job
# configurations are
# * embeddingAnalysis_cfg.py
# * tauAnalysis_cfg.py
#
# Author: Matti Kortelainen
#
######################################################################

import math, array, os

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.cutstring import * # And, Not, Or
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tauEmbedding as tauEmbedding
import plotTauEmbeddingTau as tauPlot
import produceTauEmbeddingResult as result
import plotTauEmbeddingTauMany as tauPlotMany

analysisEmb = "tauNtuple"
analysisSig = "tauNtuple"

dirSig = "../multicrab_analysisTau_111202_144918"

weight = "weightPileup_Run2011A"

def main():
    tauDirEmbs = ["."] + [os.path.join("..", d) for d in tauEmbedding.tauDirEmbs[1:]]
    tauDirSig = "../"+tauEmbedding.tauDirSig

    datasetsEmb = tauEmbedding.DatasetsMany(tauDirEmbs, analysisEmb+"Counters", normalizeMCByLuminosity=True)
    datasetsSig = dataset.getDatasetsFromMulticrabCfg(cfgfile=tauDirSig+"/multicrab.cfg", counters=analysisSig+"Counters")
    datasetsSig.updateNAllEventsToPUWeighted()

    datasetsEmb.forEach(plots.mergeRenameReorderForDataMC)
    datasetsEmb.setLumiFromData()
    plots.mergeRenameReorderForDataMC(datasetsSig)

    def mergeEWK(datasets):
        datasets.merge("EWKMC", ["WJets", "TTJets"], keepSources=True)
        #datasets.merge("EWKMC", ["WJets", "TTJets", "DYJetsToLL", "SingleTop", "Diboson"], keepSources=True)
    mergeEWK(datasetsSig)
    datasetsEmb.forEach(mergeEWK)
    plots._legendLabels["EWKMC"] = "EWK"

    style = tdrstyle.TDRStyle()
    histograms.createLegend.setDefaults(y1=0.93, y2=0.75, x1=0.52, x2=0.93)
    
    tauEmbedding.normalize = True
    tauEmbedding.era = "Run2011A"

    def dop(datasetName):
        doPlots(datasetsEmb, datasetsSig, datasetName)
#        doCounters(datasetsEmb, datasetsSig, datasetName)
        print "%s done" % datasetName
    dop("TTJets")
    dop("WJets")
    dop("DYJetsToLL")
    dop("SingleTop")
    dop("Diboson")
    dop("EWKMC")

def doPlots(datasetsEmb, datasetsSig, datasetName):
    lumi = datasetsEmb.getLuminosity()

    def createPlot(name):
        name2Emb = name
        name2Sig = name
        if isinstance(name, basestring):
            name2Emb = analysisEmb+"/"+name
            name2Sig = analysisSig+"/"+name
        else:
            name2Emb = name.clone(tree=analysisEmb+"/tree")
            name2Sig = name.clone(tree=analysisSig+"/tree")

        (emb, embVar) = datasetsEmb.getHistogram(datasetName, name2Emb)
        sig = datasetsSig.getDataset(datasetName).getDatasetRootHisto(name2Sig)
        sig.normalizeToLuminosity(lumi)
        sig = sig.getHistogram()

        emb.SetName("Embedded")
        sig.SetName("Normal")

        p = plots.ComparisonPlot(emb, sig)
        p.histoMgr.forEachHisto(styles.generator())
        legLabel = plots._legendLabels.get(datasetName, datasetName)+" MC"
        p.histoMgr.setHistoLegendLabelMany({
                "Embedded": "Embedded "+legLabel,
                "Normal":   "Normal "+legLabel
                })

        return p

    treeDraw = dataset.TreeDraw("dummy", weight=weight)

    def drawPlot(plot, name, *args, **kwargs):
        tauEmbedding.drawPlot(plot, "mcembsig_"+datasetName+"_"+name, *args, **kwargs)

    opts2def = {"DYJetsToLL": {"ymin":0, "ymax": 1.5}}.get(datasetName, {"ymin": 0.5, "ymax": 1.5})

    # Decay mode finding
    postfix = "_1AfterDecayModeFindingIsolationPtPre"
    td = treeDraw.clone(selection=And(tauPlot.decayModeFinding, tauPlot.tightIsolation, tauPlot.tauPtPreCut))
    opts2 = opts2def
    drawPlot(createPlot(td.clone(varexp="taus_p4.Eta()>>tmp(25,-2.5,2.5")),
             "tauEta"+postfix, "#tau-jet candidate #eta", ylabel="Events / %.1f", opts={"ymin": 1e-1}, opts2=opts2, moveLegend={"dx": -0.2, "dy": -0.45}, cutLine=[-2.1, 2.1])
    drawPlot(createPlot(td.clone(varexp="taus_p4.Pt()>>tmp(25,0,250)")),
             "tauPt"+postfix, "#tau-jet candidate p_{T} (GeV/c)", opts2=opts2, cutLine=40)

    # Eta cut
    postfix = "_2AfterEtaCut"
    td = treeDraw.clone(selection=And(tauPlot.decayModeFinding, tauPlot.tightIsolation, tauPlot.tauPtPreCut, tauPlot.tauEtaCut))
    drawPlot(createPlot(td.clone(varexp="taus_p4.Eta()>>tmp(25,-2.5,2.5")),
             "tauEta"+postfix, "#tau-jet candidate #eta", ylabel="Events / %.1f", opts={"ymin": 1e-1}, opts2=opts2, moveLegend={"dx": -0.2, "dy": -0.45}, cutLine=[-2.1, 2.1])
    drawPlot(createPlot(td.clone(varexp="taus_p4.Pt()>>tmp(25,0,250)")),
             "tauPt"+postfix, "#tau-jet candidate p_{T} (GeV/c)", opts2=opts2, cutLine=40)

    # Pt cut
    postfix = "_3AfterPtCut"
    td = treeDraw.clone(selection=And(tauPlot.decayModeFinding, tauPlot.tightIsolation, tauPlot.tauEtaCut, tauPlot.tauPtCut))
    drawPlot(createPlot(td.clone(varexp="taus_p4.Phi()>>tmp(32,-3.2,3.2")),
             "tauPhi"+postfix, "#tau-jet candidate #phi (rad)", ylabel="Events / %.1f", opts={"ymin": 1e-1}, opts2=opts2, moveLegend={"dx": -0.2, "dy": -0.45})
    opts2 = {"Diboson": {"ymin": 0, "ymax": 1.5}}.get(datasetName, opts2def)
    drawPlot(createPlot(td.clone(varexp="taus_leadPFChargedHadrCand_p4.Pt()>>tmp(25,0,250)")),
             "tauLeadingTrackPt"+postfix, "#tau-jet ldg. charged particle p_{T} (GeV/c)", opts2=opts2, cutLine=20)
    opts2 = opts2def

    # Tau candidate selection
    postfix = "_4AfterTauCandidateSelection"
    td = treeDraw.clone(selection=tauPlot.tauCandidateSelection)
    opts2 = {"EWKMC": {"ymin": 0.5, "ymax": 2}}.get(datasetName, opts2def)
    drawPlot(createPlot(td.clone(varexp=tauPlot.decayModeExp)),
             "tauDecayMode"+postfix+"", "", opts={"ymin": 1e-2, "ymaxfactor": 20, "nbins":5}, opts2=opts2,
             #moveLegend={"dy": 0.02, "dh": -0.02},
             function=tauPlot.decayModeCustomize)
    opts2 = opts2def

    # One prong
    postfix = "_5AfterOneProng"
    td = treeDraw.clone(selection=And(tauPlot.tauCandidateSelection, tauPlot.oneProng))
    #drawPlot(createPlot(td.clone(varexp="taus_p4.Pt()>>tmp(25,0,250)")),
    #         "tauPt"+postfix, "#tau-jet candidate p_{T} (GeV/c)", opts2={"ymin": 0, "ymax": 2})
    #drawPlot(createPlot(td.clone(varexp="taus_p4.P()>>tmp(25,0,250)")),
    #         "tauP"+postfix, "#tau-jet candidate p (GeV/c)", opts2={"ymin": 0, "ymax": 2})
    #drawPlot(createPlot(td.clone(varexp="taus_leadPFChargedHadrCand_p4.Pt()>>tmp(25,0,250)")),
    #         "tauLeadingTrackPt"+postfix, "#tau-jet ldg. charged particle p_{T} (GeV/c)", opts2={"ymin":0, "ymax": 2})
    #drawPlot(createPlot(td.clone(varexp="taus_leadPFChargedHadrCand_p4.P()>>tmp(25,0,250)")),
    #         "tauLeadingTrackP"+postfix, "#tau-jet ldg. charged particle p (GeV/c)", opts2={"ymin":0, "ymax": 2})
    drawPlot(createPlot(td.clone(varexp=tauPlot.rtauExp+">>tmp(22, 0, 1.1)")),
             "rtau"+postfix, "R_{#tau} = p^{ldg. charged particle}/p^{#tau jet}", ylabel="Events / %.1f", opts={"ymin": 1e-2, "ymaxfactor": 5}, opts2=opts2, moveLegend={"dx":-0.34}, cutLine=0.7)

    # Full ID
    postfix = "_6AfterTauID"
    td = treeDraw.clone(selection=And(tauPlot.tauCandidateSelection, tauPlot.tauID))
    drawPlot(createPlot(td.clone(varexp="taus_p4.Pt()>>tmp(25,0,250)")),
             "tauPt"+postfix, "#tau-jet p_{T} (GeV/c)", opts2=opts2)


def doCounters(datasetsEmb, datasetsSig, datasetName):
    lumi = datasetsEmb.getLuminosity()
    treeDraw = dataset.TreeDraw("dummy", weight=weight)

    # Counters
    eventCounterEmb = result.EventCounterMany(datasetsEmb, counters=analysisEmb+"Counters")
    eventCounterSig = counter.EventCounter(datasetsSig, counters=analysisSig+"Counters")

    def isNotThis(name):
        return name != datasetName

    eventCounterEmb.removeColumns(filter(isNotThis, datasetsEmb.getAllDatasetNames()))
    eventCounterSig.removeColumns(filter(isNotThis, datasetsSig.getAllDatasetNames()))
    eventCounterSig.normalizeMCToLuminosity(lumi)

    #effFormat = counter.TableFormatText(counter.CellFormatText(valueFormat='%.4f'))
    #effFormat = counter.TableFormatConTeXtTABLE(counter.CellFormatTeX(valueFormat='%.4f'))
    effFormat = counter.TableFormatText(counter.CellFormatTeX(valueFormat='%.4f'))

    tdEmb = treeDraw.clone(tree=analysisEmb+"/tree")
    tdSig = treeDraw.clone(tree=analysisSig+"/tree")
    selectionsCumulative = []
    tauSelectionsCumulative = []
    def sel(name, selection):
        selectionsCumulative.append(selection)
        sel = selectionsCumulative[:]
        if len(tauSelectionsCumulative) > 0:
            sel += ["Sum$(%s) >= 1" % "&&".join(tauSelectionsCumulative)]
        sel = "&&".join(sel)
        eventCounterEmb.mainCounterAppendRow(name, tdEmb.clone(selection=sel))
        eventCounterSig.getMainCounter().appendRow(name, tdSig.clone(selection=sel))
    def tauSel(name, selection):
        tauSelectionsCumulative.append(selection)
        sel = selectionsCumulative[:]
        if len(tauSelectionsCumulative) > 0:
            sel += ["Sum$(%s) >= 1" % "&&".join(tauSelectionsCumulative)]
        sel = "&&".join(sel)
        eventCounterEmb.mainCounterAppendRow(name, tdEmb.clone(selection=sel))
        eventCounterSig.getMainCounter().appendRow(name, tdSig.clone(selection=sel))

#    sel("Primary vertex", tauPlot.pvSelection)
    sel(">= 1 tau candidate", "Length$(taus_p4) >= 1")
    tauSel("Decay mode finding", tauPlot.decayModeFinding)
    tauSel("pT > 15", "(taus_p4.Pt() > 15)")
    tauSel("pT > 40", tauPlot.tauPtCut)
    tauSel("eta < 2.1", tauPlot.tauEtaCut)
    tauSel("leading track pT > 20", tauPlot.tauLeadPt)
    tauSel("ECAL fiducial", tauPlot.ecalFiducial)
    tauSel("againstElectron", tauPlot.electronRejection)
    tauSel("againstMuon", tauPlot.muonRejection)
    tauSel("isolation", tauPlot.tightIsolation)
    tauSel("oneProng", tauPlot.oneProng)
    tauSel("Rtau", tauPlot.rtau)
    sel("3 jets", tauPlot.jetEventSelection)
    sel("MET", tauPlot.metSelection)
    sel("btag", tauPlot.btagEventSelection)

    table = counter.CounterTable()
    col = eventCounterEmb.getMainCounterTable().getColumn(name=datasetName)
    col.setName("Embedded")
    table.appendColumn(col)
    col = eventCounterSig.getMainCounterTable().getColumn(name=datasetName)
    col.setName("Normal")
    table.appendColumn(col)

    col = table.getColumn(name="Embedded")
    table.insertColumn(1, counter.efficiencyColumn(col.getName()+" eff", col))
    col = table.getColumn(name="Normal")
    table.appendColumn(counter.efficiencyColumn(col.getName()+" eff", col))

    print "%s counters" % datasetName
    print table.format(effFormat)

    f = open("counters_"+datasetName+".txt", "w")
    f.write(table.format(effFormat))
    f.write("\n")
    f.close()
   

if __name__ == "__main__":
    main()
