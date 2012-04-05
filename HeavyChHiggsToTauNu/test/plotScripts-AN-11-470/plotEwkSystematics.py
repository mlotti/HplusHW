#!/usr/bin/env python

######################################################################
#
# This plot script is for inspecting the signal contamination in embedded MC.
# within the signal analysis. The corresponding python job
# configurations is
# * signalAnalysis_cfg.py with "doPat=1 tauEmbeddingInput=1"
# for embedding+signal analysis
#
# The development script is plotTauEmbeddingSignalAnalysisManySignalContamination
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

baseline = "signalAnalysisCaloMet60TEff"
plusJES = baseline + "JESPlus03eta02METPlus00"
minusJES = baseline + "JESMinus03eta02METPlus00"
analysisSig = "signalAnalysisGenuineTau"

counters = "Counters/weighted"

weight = "weightPileup*weightTrigger"
weightBTagging = weight+"*weightBTagging"
treeDraw = dataset.TreeDraw(baseline+"/tree", weight=weight)

metCut = "(met_p4.Et() > 50)"
bTaggingCut = "passedBTagging"
deltaPhi160Cut = "(acos( (tau_p4.Px()*met_p4.Px()+tau_p4.Py()*met_p4.Py())/(tau_p4.Pt()*met_p4.Et()) )*57.3 <= 160)"
deltaPhi130Cut = "(acos( (tau_p4.Px()*met_p4.Px()+tau_p4.Py()*met_p4.Py())/(tau_p4.Pt()*met_p4.Et()) )*57.3 <= 130)"

def main():
    dirEmbs = ["."] + [os.path.join("..", d) for d in tauEmbedding.dirEmbs[1:]]
    dirSig = "../"+tauEmbedding.dirSig

    datasetsEmb = tauEmbedding.DatasetsMany(dirEmbs, baseline+"Counters")
    datasetsSig = dataset.getDatasetsFromMulticrabCfg(cfgfile=dirSig+"/multicrab.cfg", counters=analysisSig+"Counters")
    datasetsSig.updateNAllEventsToPUWeighted()

    # Remove signal and W3jets
    datasetsEmb.remove(filter(lambda name: "HplusTB" in name, datasetsEmb.getAllDatasetNames()))
    datasetsEmb.remove(filter(lambda name: "TTToHplus" in name, datasetsEmb.getAllDatasetNames()))
    datasetsEmb.remove(filter(lambda name: "W3Jets" in name, datasetsEmb.getAllDatasetNames()))

    del plots._datasetMerge["WW"]
    datasetsEmb.forEach(plots.mergeRenameReorderForDataMC)
    datasetsEmb.setLumiFromData()
    plots.mergeRenameReorderForDataMC(datasetsSig)

    style = tdrstyle.TDRStyle()
    histograms.createLegend.moveDefaults(dx=-0.32, dh=-0.15)
    tauEmbedding.normalize=True
    tauEmbedding.era = "Run2011A"

    def mergeEWK(datasets):
        datasets.merge("EWKMC", ["WJets", "TTJets", "DYJetsToLL", "SingleTop", "Diboson", "WW"], keepSources=True)
        #datasets.merge("EWKMC", ["WJets", "TTJets"], keepSources=True)
    mergeEWK(datasetsSig)
    datasetsEmb.forEach(mergeEWK)
    datasetsResidual = tauEmbedding.DatasetsResidual(datasetsEmb, datasetsSig, baseline, analysisSig, ["DYJetsToLL", "WW"], totalNames=["Data", "EWKMC"])

    # JES plots
    jesAnalyses = [
        ("Baseline", baseline),
        ("Plus", plusJES),
        ("Minus", minusJES)
        ]
    doPlot(datasetsEmb, jesAnalyses, "transverseMass", "mt_variated_btagging", "Without #Delta#phi(#tau jet, E_{T}^{miss}) cut")
    doPlot(datasetsEmb, jesAnalyses, "transverseMassAfterDeltaPhi160", "mt_variated_deltaPhi160", "#Delta#phi(#tau jet, E_{T}^{miss}) < 160^{o}")
    doPlot(datasetsEmb, jesAnalyses, "transverseMassAfterDeltaPhi130", "mt_variated_deltaPhi130", "#Delta#phi(#tau jet, E_{T}^{miss}) < 130^{o}")

    for step in [
        "btagging",
        "deltaPhiTauMET<160",
        "deltaPhiTauMET<130"
        ]:
        print
        doCounters(datasetsResidual, jesAnalyses, step)


def doPlot(datasetsEmb, analyses, path, name, text):
    histos = []
    legends = {"Plus": "#tau-jet energy scale variated by +3 %",
               "Minus": "#tau-jet energy scale variated by -3 %"}

    for aname, analysis in analyses:
        (rootHisto, tmp) = datasetsEmb.getHistogram("Data", analysis+"/"+path)
        h = histograms.Histo(rootHisto, aname)
        h.setLegendLabel(legends.get(aname, aname))
        h.setDrawStyle("EP")
        h.setLegendStyle("p")
        histos.append(h)

    p = plots.ComparisonManyPlot(histos[0], histos[1:])

    styles.dataStyle(p.histoMgr.getHisto("Baseline"))
    styles.mcStyle(p.histoMgr.getHisto("Plus"))
    styles.mcStyle2(p.histoMgr.getHisto("Minus"))
    p.histoMgr.getHisto("Minus").getRootHisto().SetMarkerSize(2)
    p.setLuminosity(datasetsEmb.getLuminosity())
    p.appendPlotObject(histograms.PlotText(0.5, 0.55, text, size=20))

    plots.drawPlot(p, name, "m_{T}(#tau jet, E_{T}^{miss}) (GeV/c^{2})", ylabel="Events / %d GeV/c^{2}",
                   rebin=20, ratio=True, opts={"ymax": 35}, opts2={"ymax": 2}, addLuminosityText=True)

def doCounters(datasetsEmbResidual, jesAnalyses, step):
    datasetsEmb = datasetsEmbResidual.datasetsEmb
    # Hardcoded uncertainties, values taken elsewhere
    unc_tauID = 0.06
    unc_wtaumu = 0.007
    unc_mueff = 0.005

    # QCD MET+btagging efficiency
    qcdEff = 0.11

    result = counter.CounterTable()
    def addRow(name, value):
        value = value.clone()
        value.multiply(dataset.Count(100))
        result.appendRow(counter.CounterRow(name, ["Uncertainty (\%)"], [value]))

    print "Step %s" % step

    # Trigger

    # In the bins of tau pT where the trigger efficiency was measured,
    # obtain for each run region (with different efficiency
    # measurement) the number of events in each bin (multiplied with
    # the trigger efficiency), and the total absolute uncertainty.
    # Then sum the number of events, and quadratically the absolute
    # uncertainty. Final relative uncertainty is then absolute
    # uncertainty/number of events.
    bins = [40, 50, 60, 80]
    tauPtPrototype = ROOT.TH1F("tauPtTrigger", "Tau pt", len(bins)-1, array.array("d", bins))
    tdCount = treeDraw.clone(tree=baseline+"/tree")
    td = ({
        "btagging": tdCount.clone(selection=And(metCut, bTaggingCut)),
        "deltaPhiTauMET<160": tdCount.clone(selection=And(metCut, bTaggingCut, deltaPhi160Cut)),
        "deltaPhiTauMET<130": tdCount.clone(selection=And(metCut, bTaggingCut, deltaPhi130Cut)),
        }[step]).clone(varexp="tau_p4.Pt() >>tauPtTrigger")
    runs = [
        "(160431 <= run && run <= 167913)",
        "(170722 <= run && run <= 173198)",
        "(173236 <= run && run <= 173692)",
        #"(160431 <= run && run <= 173692)",
        ]
    NallSum = 0
    NSum = 0
    absUncSquareSum = 0
    for runRegion in runs:
        t = td.clone(selection=And(td.selection, runRegion))
        (th1all, tmp) = datasetsEmb.getHistogram("Data", t.clone(weight="")) # Nall
        (th1, tmp) = datasetsEmb.getHistogram("Data", t.clone(weight="weightTrigger")) # Nevents
        (th1unc, tmp) = datasetsEmb.getHistogram("Data", t.clone(weight="weightTriggerAbsUnc")) # uncertainty

        Nall = th1all.Integral(0, th1all.GetNbinsX()+1)
        N = th1.Integral(0, th1.GetNbinsX()+1)
        absUnc = tauEmbedding.squareSum(th1unc)
        relUnc = 0
        if N > 0:
            relUnc = math.sqrt(absUnc) / N

        NallSum += Nall
        NSum += N
        absUncSquareSum += absUnc

        
        print "Trigger runs %s: Nall = %.2f, N = %.2f, abs. unc. %.2f, rel. unc. %.3f" % (runRegion, Nall, N, absUnc, relUnc)
    absUnc = math.sqrt(absUncSquareSum)
    relUnc = absUnc/NSum
    print "Trigger total: Nall = %.2f, N = %.2f, abs. unc. %.2f, rel. unc. %.3f" % (NallSum, NSum, absUnc, relUnc)
    addRow("Trigger efficiency", dataset.Count(relUnc))

    # Tau ID
    addRow("Tau ID", dataset.Count(unc_tauID))

    # JES
    # Obtain the counts for baseline, and plus/minus variations, take
    # the largest deviation from the baseline, calculate the relative
    # uncertainty as deviation/baseline
    values = {}
    for name, analysis in jesAnalyses:
        c = datasetsEmb.getCounter("Data", analysis+counters+"/counter")
        c.setName(name)
        tmp = counter.CounterTable()
        tmp.appendColumn(c)
        col = tmp.getColumn(name=name)
        count = col.getCount(name=step)
        values[name] = count.value()
        values[name+"Unc"] = count.uncertainty()
    plusDiff = abs(values["Baseline"] - values["Plus"])
    minusDiff = abs(values["Baseline"] - values["Minus"])
    maxDiff = max(plusDiff, minusDiff)
    rel = maxDiff / values["Baseline"]
    print "JES baseline %.2f, plus %.2f, minus %.2f, rel. unc. %.2f" % (values["Baseline"], values["Plus"], values["Minus"], rel*100)
    addRow("Tau energy scale", dataset.Count(rel))

    # stat. unc.
    addRow("Control sample stat. uncertainty", dataset.Count(values["BaselineUnc"] / values["Baseline"]))

    # W->tau->mu fraction
    addRow("Fraction of W->tau->mu events", dataset.Count(unc_wtaumu))

    # QCD contamination
    eventCounter = tauEmbedding.EventCounterResidual(datasetsEmbResidual, counters=baseline+counters)
    table = eventCounter.getMainCounterTable()
    count = "njets"
    qcdCount = table.getCount(rowName="njets", colName="QCD_Pt20_MuEnriched")
    ewkCount = table.getCount(rowName=step, colName="EWKMC")
    qcdOrig = qcdCount.value()
    qcdCount.multiply(dataset.Count(qcdEff))
    qcdFraction = qcdCount.clone()
    qcdFraction.divide(ewkCount)
    print "QCD contamination: NQCD after njets %.1f, x eff %.2f, EWK events %.1f, fraction %.3f" % (qcdOrig, qcdCount.value(), ewkCount.value(), qcdFraction.value())
    addRow("QCD contamination", qcdFraction)

    # Mu selection efficiency
    addRow("Muon trigger and identification", dataset.Count(unc_mueff))
    
    cellFormat = counter.TableFormatLaTeX(counter.CellFormatTeX(valueFormat='%.1f', valueOnly=True))
    print result.format(cellFormat)
                         

if __name__ == "__main__":
    main()
