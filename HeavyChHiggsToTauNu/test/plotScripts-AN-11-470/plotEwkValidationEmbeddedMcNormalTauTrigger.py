#!/usr/bin/env python

######################################################################
#
# This plot script is for comparing the embedded MC and normal MC
# withinsignal analysis and tau trigger. The corresponding python job
# configurations are
# * signalAnalysis_cfg.py with "doPat=1 tauEmbeddingInput=1"
# * signalAnalysis_cfg.py
# for embedding tauID, normal tauID, embedded signal analysis, and
# normal signal analysis, respecitvely
#
# The development scripts are
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

analysisEmb = "signalAnalysisCaloMet60TEff"
analysisSig = "signalAnalysisGenuineTau" # require that the selected tau is genuine, valid comparison after njets

counters = "Counters/weighted"

def main():
    dirEmbs = ["."] + [os.path.join("..", d) for d in tauEmbedding.dirEmbs[1:]]
    dirSig = "../"+tauEmbedding.dirSig
#    dirEmbs = dirEmbs[:2]

    datasetsEmb = tauEmbedding.DatasetsMany(dirEmbs, analysisEmb+"Counters", normalizeMCByLuminosity=True)
    datasetsSig = dataset.getDatasetsFromMulticrabCfg(cfgfile=dirSig+"/multicrab.cfg", counters=analysisSig+"Counters")

    datasetsEmb.forEach(plots.mergeRenameReorderForDataMC)
    datasetsEmb.setLumiFromData()
    plots.mergeRenameReorderForDataMC(datasetsSig)

    def mergeEWK(datasets):
        datasets.merge("EWKMC", ["WJets", "TTJets", "DYJetsToLL", "SingleTop", "Diboson"], keepSources=True)
    mergeEWK(datasetsSig)
    datasetsEmb.forEach(mergeEWK)
    plots._legendLabels["EWKMC"] = "EWK"

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    histograms.createLegend.setDefaults(y1=0.93, y2=0.75, x1=0.52, x2=0.93)
    tauEmbedding.normalize = True
    tauEmbedding.era = "Run2011A"

    table = counter.CounterTable()

    def dop(name):
        doPlots(datasetsEmb, datasetsSig, name)
        tbl = doCounters(datasetsEmb, datasetsSig, name)
        for icol in xrange(tbl.getNcolumns()):
            table.appendColumn(tbl.getColumn(icol))

    dop("TTJets")
    dop("WJets")
    dop("DYJetsToLL")
    dop("SingleTop")
    dop("Diboson")

    cellFormat = counter.TableFormatLaTeX(counter.CellFormatTeX(valueFormat='%.4f', withPrecision=2))
    print table.format(cellFormat)



drawPlotCommon = tauEmbedding.PlotDrawerTauEmbeddingEmbeddedNormal(ylabel="Events / %.0f GeV/c", stackMCHistograms=False, log=True, addMCUncertainty=True, ratio=True)

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
    drawControlPlot("SelectedTau_pT_AfterStandardSelections", "#tau-jet p_{T} (GeV/c)", opts=update(opts, {"xmax": 250}), rebin=2, cutBox={"cutValue": 40, "greaterThan": 40})
        
    opts = {
        "SingleTop": {"ymax": 1.8}
        }.get(datasetName, {"ymaxfactor": 1.4})
    moveLegend = {"dy":-0.6, "dx":-0.2}
    if datasetName != "TTJets":
        moveLegend = {"dx": -0.32}
    drawControlPlot("SelectedTau_eta_AfterStandardSelections", "#tau-jet #eta", opts=update(opts, {"xmin": -2.2, "xmax": 2.2}), ylabel="Events / %.1f", rebin=4, log=False, moveLegend=moveLegend)

    drawControlPlot("SelectedTau_LeadingTrackPt_AfterStandardSelections", "#tau-jet ldg. charged particle p_{T} (GeV/c)", opts=update(opts, {"xmax": 300}), rebin=2, cutBox={"cutValue": 20, "greaterThan": True})

    opts = {"ymin": 1e-1, "ymaxfactor": 5}
    if datasetName == "Diboson":
        opts["ymin"] = 1e-2
    moveLegend = {"dx": -0.25}
    drawControlPlot("SelectedTau_Rtau_AfterStandardSelections", "R_{#tau} = p^{ldg. charged particle}/p^{#tau jet}", opts=update(opts, {"xmin": 0.65, "xmax": 1.05}), rebin=5, ylabel="Events / %.2f", moveLegend=moveLegend, cutBox={"cutValue":0.7, "greaterThan":True})

    opts = optsdef
    drawControlPlot("Njets_AfterStandardSelections", "Number of jets", ylabel="Events")

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

    opts2=opts2def
    opts = {
        "WJets": {"ymax": 20},
        "DYJetsToLL": {"ymax": 5},
        "SingleTop": {"ymax": 2},
        "Diboson": {"ymax": 0.6},
        }.get(datasetName, {"ymaxfactor": 1.2})
    opts2 = {
        "WJets": {"ymin": 0, "ymax": 3}
        }.get(datasetName, opts2def)
    drawPlot(createPlot(tdDeltaPhi.clone(selection=And(tauEmbedding.signalNtuple.metCut, tauEmbedding.signalNtuple.bTaggingCut))), "deltaPhi_3AfterBTagging", xlabel, log=False, opts=opts, opts2=opts2, ylabel="Events / %.0f^{o}", function=customDeltaPhi, moveLegend={"dx":-0.22}, cutLine=[130, 160])
    
    # Transverse mass
    selection = And(*[tauEmbedding.signalNtuple.metCut, tauEmbedding.signalNtuple.bTaggingCut, tauEmbedding.signalNtuple.deltaPhi160Cut])
    opts = {
        "EWKMC": {"ymax": 40},
        "TTJets": {"ymax": 12},
        #"WJets": {"ymax": 35},
        "WJets": {"ymax": 25},
        "SingleTop": {"ymax": 2.2},
        "DYJetsToLL": {"ymax": 6.5},
        #"Diboson": {"ymax": 0.9},
        "Diboson": {"ymax": 0.8},
        "W3Jets": {"ymax": 5}
        }.get(datasetName, {})
    opts2 = {
        "TTJets": {"ymin": 0, "ymax": 1.2},
        "Diboson": {"ymin": 0, "ymax": 3.2},
        }.get(datasetName, opts2)

    p = createPlot(tdMt.clone(selection=selection))
    p.appendPlotObject(histograms.PlotText(0.6, 0.7, "#Delta#phi(#tau jet, E_{T}^{miss}) < 160^{o}", size=20))
    drawPlot(p, "transverseMass_4AfterDeltaPhi160", "m_{T}(#tau jet, E_{T}^{miss}) (GeV/c^{2})", opts=opts, opts2=opts2, ylabel="Events / %.0f GeV/c^{2}", log=False)


    
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

    tableEmb = eventCounterEmb.getMainCounterTable()
    tableSig = eventCounterSig.getMainCounterTable()

    table = counter.CounterTable()
    col = tableEmb.getColumn(name=datasetName)
    col.setName(datasetName+" emb")
    table.appendColumn(col)
    col = tableSig.getColumn(name=datasetName)
    col.setName(datasetName+" norm")
    table.appendColumn(col)

    table.keepOnlyRows([
            "njets",
            "MET",
            "btagging",
            "btagging scale factor",
            "deltaPhiTauMET<160",
            "deltaPhiTauMET<130",
            ])
    table.renameRows({"njets": "tau ID"})

    return table

if __name__ == "__main__":
    main()
