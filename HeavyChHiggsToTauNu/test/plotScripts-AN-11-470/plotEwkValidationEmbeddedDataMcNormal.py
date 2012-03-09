#!/usr/bin/env python

######################################################################
#
# This plot script is for comparing the embedded data + residual MC,
# embedded MC + residual MC, and normal MC within the signal analysis.
# The corresponding python job
# configurations are
# * signalAnalysis_cfg.py with "doPat=1 tauEmbeddingInput=1"
# * signalAnalysis_cfg.py
# for embedding+signal analysis and signal analysis, respectively
#
# The development scripts are
# * plotTauEmbeddingMcSignalAnalysisMcMany
# * plotTauEmbeddingSignalAnalysisMany
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

metCut = "(met_p4.Et() > 50)"
bTaggingCut = "passedBTagging"
deltaPhi160Cut = "(acos( (tau_p4.Px()*met_p4.Px()+tau_p4.Py()*met_p4.Py())/(tau_p4.Pt()*met_p4.Et()) )*57.3 <= 160)"
deltaPhi130Cut = "(acos( (tau_p4.Px()*met_p4.Px()+tau_p4.Py()*met_p4.Py())/(tau_p4.Pt()*met_p4.Et()) )*57.3 <= 130)"

weight = "weightPileup*weightTrigger"
weightBTagging = weight+"*weightBTagging"

plotStyles = styles.styles[0:2]
plotStyles[0] = styles.StyleCompound([plotStyles[0], styles.StyleMarker(markerStyle=21, markerSize=1.2)])

def main():
    # Adjust paths such that this script can be run inside the first embedding trial directory
    dirEmbs = ["."] + [os.path.join("..", d) for d in tauEmbedding.dirEmbs[1:]]
    dirSig = "../"+tauEmbedding.dirSig

    # Create the dataset objects
    datasetsEmb = tauEmbedding.DatasetsMany(dirEmbs, analysisEmb+"Counters", normalizeMCByLuminosity=True)
    datasetsSig = dataset.getDatasetsFromMulticrabCfg(cfgfile=dirSig+"/multicrab.cfg", counters=analysisSig+"Counters")

    # Remove signal and W+3jets datasets
    datasetsEmb.remove(filter(lambda name: "HplusTB" in name, datasetsEmb.getAllDatasetNames()))
    datasetsEmb.remove(filter(lambda name: "TTToHplus" in name, datasetsEmb.getAllDatasetNames()))
    datasetsEmb.remove(filter(lambda name: "W3Jets" in name, datasetsEmb.getAllDatasetNames()))

    # Keep WW separately, Diboson is WZ+ZZ
    del plots._datasetMerge["WW"]

    datasetsEmb.forEach(lambda mgr: plots.mergeRenameReorderForDataMC(mgr, keepSourcesMC=True))
    datasetsEmb.setLumiFromData()
    plots.mergeRenameReorderForDataMC(datasetsSig, keepSourcesMC=True)

    # Merge EWK datasets
    def mergeEWK(datasets):
        datasets.merge("EWKMC", ["WJets", "TTJets", "DYJetsToLL", "SingleTop", "Diboson", "WW"], keepSources=True)
#        datasets.merge("EWKMC", ["Diboson", "WW"], keepSources=True)
    mergeEWK(datasetsSig)
    datasetsEmb.forEach(mergeEWK)
    plots._legendLabels["EWKMC"] = "EWK"

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    ROOT.gStyle.SetEndErrorSize(5)
    histograms.createLegend.setDefaults(y1=0.93, y2=0.75, x1=0.52, x2=0.93)
    tauEmbedding.normalize=True
    tauEmbedding.era = "Run2011A"

    # Create datasets with residuals
    # Define DYJetsToLL and WW be the datasets where residuals are calculated
    # Define Data and EWKMC be the datasets to which the residuals are added
    # I.e. Data will be embedded data + res. MC, and EWKMC embedded MC + res. MC
    datasetsEmbCorrected = tauEmbedding.DatasetsResidual(datasetsEmb, datasetsSig, analysisEmb, analysisSig, ["DYJetsToLL", "WW"], totalNames=["Data", "EWKMC"])

    #doPlots(datasetsEmbCorrected, datasetsSig, "EWKMC")
    doCounters(datasetsEmbCorrected, datasetsSig)

def doPlots(datasetsEmb, datasetsSig, datasetName):
    lumi = datasetsEmb.getLuminosity()
    isCorrected = isinstance(datasetsEmb, tauEmbedding.DatasetsResidual)
    postfix = "_residual"
    
    createPlot = tauEmbedding.PlotCreatorMany(analysisEmb, analysisSig, datasetsEmb, datasetsSig, datasetName, plotStyles, addData=True)
    drawPlot = tauEmbedding.PlotDrawerTauEmbeddingEmbeddedNormal(ratio=True, log=True, addLuminosityText=True)
    def createDrawPlot(name, *args, **kwargs):
        p = createPlot(name)
        drawPlot(p, *args, **kwargs)

    prefix = "embdatasigmc"+postfix+"_"+datasetName+"_"

    opts2def = {"ymin": 0, "ymax": 2}
    def drawControlPlot(path, xlabel, rebin=None, opts2=None, **kwargs):
        opts2_ = opts2def
        if opts2 != None:
            opts2_ = opts2
        cargs = {}
        if rebin != None:
            cargs["rebin"] = rebin
        drawPlot(createPlot("ControlPlots/"+path, **cargs), prefix+path, xlabel, opts2=opts2_, **kwargs)

    def update(d1, d2):
        tmp = {}
        tmp.update(d1)
        tmp.update(d2)
        return tmp

    # Control plots
    optsdef = {}
    opts = optsdef
    drawControlPlot("SelectedTau_pT_AfterStandardSelections", "#tau-jet p_{T} (GeV/c)", opts=update(opts, {"xmax": 250}), rebin=2, cutBox={"cutValue": 40, "greaterThan": 40})

    moveLegend = {"dy":-0.6, "dx":-0.2}
    opts = {
        "SingleTop": {"ymax": 1.8}
        }.get(datasetName, {"ymaxfactor": 1.4})
    if datasetName != "TTJets":
        moveLegend = {"dx": -0.32}
    drawControlPlot("SelectedTau_eta_AfterStandardSelections", "#tau-jet #eta", opts=update(opts, {"xmin": -2.2, "xmax": 2.2}), ylabel="Events / %.1f", rebin=4, log=False, moveLegend=moveLegend)

    drawControlPlot("SelectedTau_LeadingTrackPt_AfterStandardSelections", "#tau-jet ldg. charged particle p_{T} (GeV/c)", opts=update(opts, {"xmax": 300}), rebin=2, cutBox={"cutValue": 20, "greaterThan": True})

    opts = {"ymin": 1e-1, "ymaxfactor": 5}
    moveLegend = {"dx": -0.25}
    if datasetName == "Diboson":
        opts["ymin"] = 1e-2
    drawControlPlot("SelectedTau_Rtau_AfterStandardSelections", "R_{#tau} = p^{ldg. charged particle}/p^{#tau jet}", opts=update(opts, {"xmin": 0.65, "xmax": 1.05}), rebin=5, ylabel="Events / %.2f", moveLegend=moveLegend, cutBox={"cutValue":0.7, "greaterThan":True})

    opts = optsdef
    drawControlPlot("Njets_AfterStandardSelections", "Number of jets", ylabel="Events")

    # After Njets
    drawControlPlot("MET", "Uncorrected PF E_{T}^{miss} (GeV)", rebin=5, opts=update(opts, {"xmax": 400}), cutLine=50)

    # after MET
    moveLegend = {
        "WJets": {},
        "DYJetsToLL": {},
        "SingleTop": {},
        "Diboson": {}
        }.get(datasetName, {"dx": -0.23, "dy": -0.5})
    drawControlPlot("NBjets", "Number of selected b jets", opts=update(opts, {"xmax": 6}), ylabel="Events", moveLegend=moveLegend, cutLine=1)

    # Tree cut definitions
    treeDraw = dataset.TreeDraw("dummy", weight=weightBTagging)
    tdDeltaPhi = treeDraw.clone(varexp="acos( (tau_p4.Px()*met_p4.Px()+tau_p4.Py()*met_p4.Py())/(tau_p4.Pt()*met_p4.Et()) )*57.3 >>tmp(18, 0, 180)")
    tdMt = treeDraw.clone(varexp="sqrt(2 * tau_p4.Pt() * met_p4.Et() * (1-cos(tau_p4.Phi()-met_p4.Phi()))) >>tmp(20,0,400)")

    # DeltapPhi
    xlabel = "#Delta#phi(#tau jet, E_{T}^{miss}) (^{o})"
    def customDeltaPhi(h):
        yaxis = h.getFrame().GetYaxis()
        yaxis.SetTitleOffset(0.8*yaxis.GetTitleOffset())
    opts = {
        "WJets": {"ymax": 20},
        "DYJetsToLL": {"ymax": 5},
        "SingleTop": {"ymax": 2},
        "Diboson": {"ymax": 0.6},
        }.get(datasetName, {"ymaxfactor": 1.2})
    opts2 = {
        "WJets": {"ymin": 0, "ymax": 3}
        }.get(datasetName, opts2def)
    drawPlot(createPlot(tdDeltaPhi.clone(selection=And(metCut, bTaggingCut))), prefix+"deltaPhi_3AfterBTagging", xlabel, log=False, opts=opts, opts2=opts2, ylabel="Events / %.0f^{o}", function=customDeltaPhi, moveLegend={"dx":-0.22}, cutLine=[130, 160])


    # After all cuts
    selection = And(metCut, bTaggingCut, deltaPhi160Cut)

    #opts = {"ymaxfactor": 1.4}
    opts = {}

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
        }.get(datasetName, {"ymin": 0, "ymax": 2})
    
    p = createPlot(tdMt.clone(selection=selection))
    p.appendPlotObject(histograms.PlotText(0.6, 0.7, "#Delta#phi(#tau jet, E_{T}^{miss}) < 160^{o}", size=20))
    drawPlot(p, prefix+"transverseMass_4AfterDeltaPhi160", "m_{T}(#tau jet, E_{T}^{miss}) (GeV/c^{2})", opts=opts, opts2=opts2, ylabel="Events / %.0f GeV/c^{2}", log=False)

def doCounters(datasetsEmb, datasetsSig):
    rows = ["njets", "MET", "btagging scale factor", "deltaPhiTauMET<160", "deltaPhiTauMET<130"]
    residuals = ["DYJetsToLL residual", "WW residual"]

    # Normal MC
    eventCounterNormal = counter.EventCounter(datasetsSig, counters=analysisSig+counters)
    eventCounterNormal.normalizeMCToLuminosity(datasetsEmb.getLuminosity())
    tableNormal = eventCounterNormal.getMainCounterTable()
    tableNormal.keepOnlyRows(rows)

    # Embedded data and MC, residual MC
    eventCounter = tauEmbedding.EventCounterResidual(datasetsEmb, counters=analysisEmb+counters)
    table = eventCounter.getMainCounterTable()
    table.keepOnlyRows(rows)

    # Build the result
    result = counter.CounterTable()

    c = table.getColumn(name="Data")
    c.setName("Embedded data")
    result.appendColumn(c)
    #result.appendColumn(table.getColumn(name="EWKMC"))
    for name in residuals:
        result.appendColumn(table.getColumn(name=name))

    result.appendColumn(counter.sumColumn("Emb. data + res. MC", [table.getColumn(name=name) for name in ["Data"]+residuals]))
    result.appendColumn(counter.sumColumn("Emb. MC + res. MC", [table.getColumn(name=name) for name in ["EWKMC"]+residuals]))

    c = tableNormal.getColumn(name="EWKMC")
    c.setName("Normal MC")
    result.appendColumn(c)

    # Final formatting
    result.renameRows({"njets": "tau-jet identification",
                      "btagging scale factor": "b tagging"
                      })

    cellFormat = counter.TableFormatLaTeX(counter.CellFormatTeX(valueFormat='%.2f'))
    print result.format(cellFormat)

if __name__ == "__main__":
    main()
