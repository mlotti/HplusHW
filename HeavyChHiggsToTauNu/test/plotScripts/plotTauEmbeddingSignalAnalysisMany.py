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

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import plotTauEmbeddingSignalAnalysis as tauEmbedding
import produceTauEmbeddingResult as result

#analysisEmb = "signalAnalysis"
analysisEmb = "signalAnalysisCaloMet60TEff"
analysisSig = "signalAnalysisGenuineTau"

def main():
    dirEmbs = ["."] + [os.path.join("..", d) for d in result.dirEmbs[1:]]
    dirSig = "../"+result.dirSig
    
    datasetsEmb = result.DatasetsMany(dirEmbs, analysisEmb+"Counters")
    datasetsSig = dataset.getDatasetsFromMulticrabCfg(cfgfile=dirSig+"/multicrab.cfg", counters=analysisSig+"Counters")

    datasetsEmb.forEach(plots.mergeRenameReorderForDataMC)
    datasetsEmb.setLumiFromData()
    plots.mergeRenameReorderForDataMC(datasetsSig)

    style = tdrstyle.TDRStyle()
    histograms.createLegend.moveDefaults(dx=-0.04)
    datasetsEmb.remove(["QCD_Pt20_MuEnriched"])
    #plots._legendLabels["QCD_Pt20_MuEnriched"] = "QCD"
    histograms.createLegend.moveDefaults(dh=-0.05)
    #histograms.createLegend.moveDefaults(dx=-0.18, dy=0.05, dh=-0.05)

    tauEmbedding.normalize=True
    tauEmbedding.era = "Run2011A"

    datasetsEmbCorrected = result.DatasetsDYCorrection(datasetsEmb, datasetsSig, analysisEmb, analysisSig)

    doPlots(datasetsEmb)
    doPlots(datasetsEmbCorrected)

    #doCounters(datasetsEmb)
    doCounters(datasetsEmbCorrected)


def drawPlot(*args, **kwargs):
    tauEmbedding.drawPlot(*args, normalize=False, **kwargs)

def doPlots(datasetsEmb):
    datasetNames = datasetsEmb.getAllDatasetNames()
    isCorrected = isinstance(datasetsEmb, result.DatasetsDYCorrection)

    def createPlot(name, dyx=0.67, dyy=0.64):
        rootHistos = []
        for datasetName in datasetNames:
            (histo, tmp) = datasetsEmb.getHistogram(datasetName, name)
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
        if isCorrected:
            p.appendPlotObject(histograms.PlotText(dyx, dyy, "DY correction applied", size=15))
        return p

    treeDraw = dataset.TreeDraw(analysisEmb+"/tree", weight="weightPileup*weightTrigger*weightBTagging")
    tdMt = treeDraw.clone(varexp="sqrt(2 * tau_p4.Pt() * met_p4.Et() * (1-cos(tau_p4.Phi()-met_p4.Phi()))) >>tmp(20,0,400)")

    metCut = "(met_p4.Et() > 50)"
    bTaggingCut = "passedBTagging"
    deltaPhi160Cut = "(acos( (tau_p4.Px()*met_p4.Px()+tau_p4.Py()*met_p4.Py())/(tau_p4.Pt()*met_p4.Et()) )*57.3 <= 160)"
    selection = "&&".join([metCut, bTaggingCut, deltaPhi160Cut])

    prefix = "avg10"
    if isCorrected:
        prefix += "_dycorrected"

    
    opts2 = {"ymin": 0, "ymax": 3}

    drawPlot(createPlot(treeDraw.clone(varexp="tau_p4.Pt() >>tmp(20,0,200)", selection=selection)), prefix+"_selectedTauPt_4AfterDeltaPhi160", "#tau-jet p_{T} (GeV/c)", opts2=opts2)
    drawPlot(createPlot(treeDraw.clone(varexp="met_p4.Pt() >>tmp(16,0,400)", selection=selection)), prefix+"_MET_4AfterDeltaPhi160", "E_{T}^{miss} (GeV)", ylabel="Events / %.0f GeV", opts2=opts2)

    #opts = {"ymaxfactor": 1.2}
    opts = {"ymax": 40}
    drawPlot(createPlot(tdMt.clone(selection=selection)), prefix+"_transverseMass_4AfterDeltaPhi160", "m_{T}(#tau jet, E_{T}^{miss}) (GeV/c^{2})", opts=opts, opts2=opts2, ylabel="Events / %.0f GeV/c^{2}", log=False)
            

def doCounters(datasetsEmb, counterName="counter"):
    datasetNames = datasetsEmb.getAllDatasetNames()

    table = counter.CounterTable()
    for name in datasetNames:
        table.appendColumn(datasetsEmb.getCounter(name, analysisEmb+"Counters/weighted/"+counterName))

    ewkDatasets = ["WJets", "TTJets", "DYJetsToLL", "SingleTop", "Diboson"]
    table.insertColumn(2, counter.sumColumn("EWKMCsum", [table.getColumn(name=name) for name in ewkDatasets]))

    print "============================================================"
    if isinstance(datasetsEmb, result.DatasetsDYCorrection):
        print "DY correction applied"

    cellFormat = counter.TableFormatText(counter.CellFormatTeX(valueFormat='%.3f'))
    print table.format(cellFormat)


if __name__ == "__main__":
    main()
