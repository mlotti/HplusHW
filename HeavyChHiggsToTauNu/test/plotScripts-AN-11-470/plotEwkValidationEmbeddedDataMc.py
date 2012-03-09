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
# The development script is plotTauEmbeddingSignalAnalysisMany
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

analysisEmbAll = "signalAnalysis"
analysisEmbNoTauEff = "signalAnalysisCaloMet60"
analysisEmb = "signalAnalysisCaloMet60TEff"

counters = "Counters/weighted"

weight = "weightPileup*weightTrigger"
weightBTagging = weight+"*weightBTagging"

caloMetCut = "(tecalomet_p4.Et() > 60)"
caloMetNoHFCut = "(tecalometNoHF_p4.Et() > 60)"
metCut = "(met_p4.Et() > 50)"
bTaggingCut = "passedBTagging"
deltaPhi160Cut = "(acos( (tau_p4.Px()*met_p4.Px()+tau_p4.Py()*met_p4.Py())/(tau_p4.Pt()*met_p4.Et()) )*57.3 <= 160)"
deltaPhi130Cut = "(acos( (tau_p4.Px()*met_p4.Px()+tau_p4.Py()*met_p4.Py())/(tau_p4.Pt()*met_p4.Et()) )*57.3 <= 130)"

def main():
    # Adjust paths such that this script can be run inside the first embedding trial directory
    dirEmbs = ["."] + [os.path.join("..", d) for d in tauEmbedding.dirEmbs[1:]]

    # Create the dataset objects
    datasetsEmb = tauEmbedding.DatasetsMany(dirEmbs, analysisEmb+"Counters", normalizeMCByLuminosity=True)

    # Remove signal and W+3jets datasets
    datasetsEmb.remove(filter(lambda name: "HplusTB" in name, datasetsEmb.getAllDatasetNames()))
    datasetsEmb.remove(filter(lambda name: "TTToHplus" in name, datasetsEmb.getAllDatasetNames()))
    datasetsEmb.remove(filter(lambda name: "W3Jets" in name, datasetsEmb.getAllDatasetNames()))

    datasetsEmb.forEach(plots.mergeRenameReorderForDataMC)
    datasetsEmb.setLumiFromData()

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    tauEmbedding.normalize=True
    tauEmbedding.era = "Run2011A"

    doCounters(datasetsEmb)

    # Remove QCD for plots
    datasetsEmb.remove(["QCD_Pt20_MuEnriched"])
    histograms.createLegend.moveDefaults(dx=-0.04, dh=-0.05)
    doPlots(datasetsEmb)

def doPlots(datasetsEmb):
    datasetNames = datasetsEmb.getAllDatasetNames()

    def createPlot(name):
        name2 = name
        if isinstance(name, basestring):
            name2 = analysisEmb+"/"+name

        rootHistos = []
        for datasetName in datasetNames:
            (histo, tmp) = datasetsEmb.getHistogram(datasetName, name2)
            histo.SetName(datasetName)
            rootHistos.append(histo)

        p = plots.DataMCPlot2(rootHistos)
        histos = p.histoMgr.getHistos()
        for h in histos:
            if h.getName() == "Data":
                h.setIsDataMC(True, False)
            else:
                h.setIsDataMC(False, True)
        p.setLuminosity(datasetsEmb.getLuminosity())
        p.setDefaultStyles()
        return p

    drawPlot = tauEmbedding.drawPlot
    drawPlot.setDefaults(ratio=True, addLuminosityText=True
                         #normalize=False,
                         )

    prefix = "embdatamc_"
    opts2 = {"ymin": 0, "ymax": 2}
    def drawControlPlot(path, xlabel, **kwargs):
        postfix = ""
        if kwargs.get("log", True):
            postfix = "_log"
        drawPlot(createPlot("ControlPlots/"+path), prefix+path+postfix, xlabel, opts2=opts2, **kwargs)

    # After tau ID
    drawControlPlot("SelectedTau_pT_AfterStandardSelections", "#tau-jet p_{T} (GeV/c)", opts={"xmax": 250}, rebin=2, cutBox={"cutValue": 40, "greaterThan": True})
    drawControlPlot("SelectedTau_eta_AfterStandardSelections", "#tau-jet #eta", opts={"xmin": -2.2, "xmax": 2.2}, ylabel="Events / %.1f", rebin=4, moveLegend={"dy":-0.52, "dx":-0.2})
    drawControlPlot("SelectedTau_LeadingTrackPt_AfterStandardSelections", "#tau-jet ldg. charged particle p_{T} (GeV/c)", opts={"xmax": 250}, rebin=2, cutBox={"cutValue": 20, "greaterThan": True})
    drawControlPlot("SelectedTau_Rtau_AfterStandardSelections", "R_{#tau} = p^{ldg. charged particle}/p^{#tau jet}", opts={"xmin": 0.65, "xmax": 1.05, "ymin": 1e-1, "ymaxfactor": 10}, rebin=5, ylabel="Events / %.2f", moveLegend={"dx":-0.4, "dy": 0.01, "dh": -0.03}, cutBox={"cutValue":0.7, "greaterThan":True})

    drawControlPlot("MET", "Uncorrected PF E_{T}^{miss} (GeV)", rebin=5, opts={"xmax": 400}, cutLine=50)

    # After MET cut
    drawControlPlot("NBjets", "Number of selected b jets", opts={"xmax": 6}, ylabel="Events", cutLine=1)

    # After b tagging
    treeDraw = dataset.TreeDraw(analysisEmb+"/tree", weight=weightBTagging)
    tdMt = treeDraw.clone(varexp="sqrt(2 * tau_p4.Pt() * met_p4.Et() * (1-cos(tau_p4.Phi()-met_p4.Phi()))) >>tmp(20,0,400)")
    tdDeltaPhi = treeDraw.clone(varexp="acos( (tau_p4.Px()*met_p4.Px()+tau_p4.Py()*met_p4.Py())/(tau_p4.Pt()*met_p4.Et()) )*57.3 >>tmp(18, 0, 180)")

    # DeltaPhi
    def customDeltaPhi(h):
        yaxis = h.getFrame().GetYaxis()
        yaxis.SetTitleOffset(0.8*yaxis.GetTitleOffset())
    drawPlot(createPlot(tdDeltaPhi.clone(selection=And(metCut, bTaggingCut))), prefix+"deltaPhi_3AfterBTagging", "#Delta#phi(#tau jet, E_{T}^{miss}) (^{o})", log=False, opts={"ymax": 30}, opts2=opts2, ylabel="Events / %.0f^{o}", function=customDeltaPhi, moveLegend={"dx": -0.22}, cutLine=[130, 160])

    # Transverse mass
    for name, label, selection in [
        ("3AfterBTagging", "Without #Delta#phi(#tau jet, E_{T}^{miss}) cut", [metCut, bTaggingCut]),
        ("4AfterDeltaPhi160", "#Delta#phi(#tau jet, E_{T}^{miss}) < 160^{o}", [metCut, bTaggingCut, deltaPhi160Cut]),
        ("5AfterDeltaPhi130", "#Delta#phi(#tau jet, E_{T}^{miss}) < 130^{o}", [metCut, bTaggingCut, deltaPhi130Cut])]:

        p = createPlot(tdMt.clone(selection=And(*selection)))
        p.appendPlotObject(histograms.PlotText(0.5, 0.62, label, size=20))
        drawPlot(p, prefix+"transverseMass_"+name, "m_{T}(#tau jet, E_{T}^{miss}) (GeV/c^{2})", opts={"ymax": 35}, opts2=opts2, ylabel="Events / %.0f GeV/c^{2}", log=False)



def addMcSum(t):
    allDatasets = ["QCD_Pt20_MuEnriched", "WJets", "TTJets", "DYJetsToLL", "SingleTop", "Diboson"]
    t.insertColumn(1, counter.sumColumn("MCSum", [t.getColumn(name=name) for name in allDatasets]))

def doCounters(datasetsEmb):

    # All embedded events
    eventCounterAll = counter.EventCounter(datasetsEmb.getFirstDatasetManager(), counters=analysisEmbAll+counters)
    eventCounterAll.normalizeMCByLuminosity()
    tableAll = eventCounterAll.getMainCounterTable()
    tableAll.keepOnlyRows([
            "All events",
            ])
    tableAll.renameRows({"All events": "All embedded events"})

    # Mu eff + Wtau mu
    eventCounterMuEff = counter.EventCounter(datasetsEmb.getFirstDatasetManager(), counters=analysisEmbNoTauEff+counters)
    eventCounterMuEff.normalizeMCByLuminosity()
    tauEmbedding.scaleNormalization(eventCounterMuEff)
    tableMuEff = eventCounterMuEff.getMainCounterTable()
    tableMuEff.keepOnlyRows([
            "All events"
            ])
    tableMuEff.renameRows({"All events": "mu eff + Wtaumu"})

    # Event counts after embedding normalization, before tau trigger eff,
    # switch to calculate uncertainties of the mean of 10 trials
    eventCounterNoTauEff = tauEmbedding.EventCounterMany(datasetsEmb, counters=analysisEmbNoTauEff+counters)
    tableNoTauEff = eventCounterNoTauEff.getMainCounterTable()
    tableNoTauEff.keepOnlyRows([
            "Trigger and HLT_MET cut",
            "njets",
            ])
    tableNoTauEff.renameRows({"Trigger and HLT_MET cut": "caloMET > 60",
                              "njets": "tau ID"
                              })

    # Event counts after tau trigger eff
    eventCounter = tauEmbedding.EventCounterMany(datasetsEmb, counters=analysisEmb+counters)
    table = eventCounter.getMainCounterTable()
    table.keepOnlyRows([
            "njets",
            "MET",
            "btagging scale factor",
            "deltaPhiTauMET<160",
            "deltaPhiTauMET<130"
            ])
    table.renameRows({"njets": "Tau trigger efficiency",
                      "btagging scale factor": "b tagging"
                      })

    # Combine the rows to one table
    result = counter.CounterTable()
    for tbl in [
        tableAll,
        tableMuEff,
        tableNoTauEff,
        table
        ]:
        for iRow in xrange(tbl.getNrows()):
            result.appendRow(tbl.getRow(index=iRow))

    addMcSum(result)
    cellFormat = counter.TableFormatText(counter.CellFormatTeX(valueFormat='%.2f'))

    print result.format(cellFormat)

if __name__ == "__main__":
    main()
