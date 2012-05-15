#!/usr/bin/env python

######################################################################
#
# This plot script is for inspecting the effect of averaging in
# embedded data and embedded MC. The corresponding python job
# configurations is
# * signalAnalysis_cfg.py with "doPat=1 tauEmbeddingInput=1"
# for embedding+signal analysis
#
# Development script: plotEwkValidationAverageNtrials
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

dirEmbsWjets = [
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest10_Run2011A_120212_110719",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest11_Run2011A_120212_111201",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest12_Run2011A_120212_111243",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest13_Run2011A_120212_111317",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest14_Run2011A_120212_111351",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest15_Run2011A_120212_111424",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest16_Run2011A_120212_111503",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest17_Run2011A_120212_111536",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest18_Run2011A_120212_111607",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest19_Run2011A_120212_111645",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest20_Run2011A_120212_111810",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest21_Run2011A_120212_111903",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest22_Run2011A_120212_112225",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest23_Run2011A_120212_112258",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest24_Run2011A_120212_112328",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest25_Run2011A_120212_112358",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest26_Run2011A_120212_112430",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest27_Run2011A_120212_112504",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest28_Run2011A_120212_112537",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest29_Run2011A_120212_112610",
]

analysisEmb = "signalAnalysisCaloMet60TEff"
counters = "Counters"

metCut = "(met_p4.Et() > 50)"
bTaggingCut = "passedBTagging"
deltaPhi160Cut = "(acos( (tau_p4.Px()*met_p4.Px()+tau_p4.Py()*met_p4.Py())/(tau_p4.Pt()*met_p4.Et()) )*57.3 <= 160)"

def main():
    # Plots of Data and MC events (tt, Wjets) as a function of trial number
    do(onlyWjets=False, mcEvents=True, normalize=False, formatCounters=False, formatPlots=True)
    do(onlyWjets=True, mcEvents=True, normalize=False, formatCounters=False, formatPlots=True)

    # Table of average, min, and max of all samples (MC normalized)
    do(onlyWjets=False, mcEvents=False, normalize=True, formatCounters=True, formatPlots=False)


def do(onlyWjets, mcEvents, normalize, formatCounters, formatPlots):
    dirEmbs = tauEmbedding.dirEmbs[:]
    if onlyWjets:
        dirEmbs.extend(dirEmbsWjets)
    dirEmbs = ["."] + [os.path.join("..", d) for d in dirEmbs[1:]]
#    dirEmbs = dirEmbs[0:2]

    # Read luminosity
    datasets = dataset.getDatasetsFromMulticrabCfg(cfgfile=dirEmbs[0]+"/multicrab.cfg", counters=analysisEmb+"Counters", weightedCounters=False)
    datasets.loadLuminosities()
    plots.mergeRenameReorderForDataMC(datasets)
    lumi = datasets.getDataset("Data").getLuminosity()


    style = tdrstyle.TDRStyle()

    tauEmbedding.normalize=normalize
    tauEmbedding.era = "Run2011A"

    table = counter.CounterTable()
    for i, d in enumerate(dirEmbs):
        datasets = dataset.getDatasetsFromMulticrabCfg(cfgfile=d+"/multicrab.cfg", counters=analysisEmb+"Counters", weightedCounters=False)
        if onlyWjets:
            datasets.remove(filter(lambda n: n != "WJets_TuneZ2_Summer11", datasets.getAllDatasetNames()))
        else:
            if mcEvents:
                datasets.remove(filter(lambda n: n != "WJets_TuneZ2_Summer11" and n != "TTJets_TuneZ2_Summer11" and not "SingleMu" in n, datasets.getAllDatasetNames()))
            datasets.loadLuminosities()
        datasets.remove(filter(lambda name: "HplusTB" in name, datasets.getAllDatasetNames()))
        datasets.remove(filter(lambda name: "TTToHplus" in name, datasets.getAllDatasetNames()))
        tauEmbedding.updateAllEventsToWeighted(datasets)
        plots.mergeRenameReorderForDataMC(datasets)

        row = doCounters(datasets, onlyWjets, mcEvents, normalize, lumi)
        row.setName("Embedding %d" % i)
        table.appendRow(row)

    if formatPlots:
        doPlots(table, onlyWjets, mcEvents, normalize, lumi)

    if not formatCounters:
        return

    arows = []
    arows.append(counter.meanRow(table))
    arows.extend(counter.meanRowFit(table))
    arows.append(counter.maxRow(table))
    arows.append(counter.minRow(table))
    for r in arows:
        table.appendRow(r)

    print table.format()

    ftable = counter.CounterTable()
    def addRow(name):
        col = table.getColumn(name=name)

        minimum = col.getCount(name="Min")
        maximum = col.getCount(name="Max")
        mean = col.getCount(name="Mean")

        ftable.appendRow(counter.CounterRow(name,
                                            ["Mean", "Minimum", "Maximum"],
                                            [mean, minimum, maximum]))
    addRow("Data")
    addRow("EWKMCsum")
    addRow("TTJets")
    addRow("WJets")
    addRow("DYJetsToLL")
    addRow("SingleTop")
    addRow("Diboson")

    cellFormat2 = counter.TableFormatLaTeX(counter.CellFormatTeX(valueFormat="%.4f", withPrecision=2))
    print ftable.format(cellFormat2)

def doCounters(datasets, onlyWjets, mcEvents, normalize, lumi):
    cntr = counters
    if normalize:
        cntr = counters+"/weighted"
    eventCounter = counter.EventCounter(datasets, counters=analysisEmb+cntr)
    if not mcEvents:
        if onlyWjets:
            eventCounter.normalizeMCToLuminosity(lumi)
        else:
            eventCounter.normalizeMCByLuminosity()
    tauEmbedding.scaleNormalization(eventCounter)

    mainTable = eventCounter.getMainCounterTable()

    ewkDatasets = ["WJets", "TTJets", "DYJetsToLL", "SingleTop", "Diboson"]
    def ewkSum(table):
        table.insertColumn(1, counter.sumColumn("EWKMCsum", [table.getColumn(name=name) for name in ewkDatasets]))
    if not onlyWjets and not mcEvents:
        ewkSum(mainTable)

    return mainTable.getRow(name="deltaPhiTauMET<160")

def doPlots(table, onlyWjets, mcEvents, normalize, lumi):
    nrows = table.getNrows()
    function = ROOT.TF1("fitFunction", "[0]") 
    function.SetParameter(0, 0)
    f2 = ROOT.TF1("fitG", "gaus")
    f2.SetLineColor(ROOT.kRed)
    f2.SetLineWidth(2)

    binning = {
        "Data": (8, 60, 100),
        "Diboson": (8, 0, 2),
        "DYJetsToLL": (8, 1, 5),
        "EWKMCsum": (8, 40, 120),
        "SingleTop": (8, 3, 6),
        "TTJets": (10, 25, 35),
        "W3Jets": (10, 6, 11),
        "WJets": (14, 10, 80),
        }
    if onlyWjets:
        binning["WJets"] = (24, 10, 90)
    if not normalize:
        binning["Data"] = (10, 70, 120)
        binning["EWKMCsum"] = (6, 60, 120)
        binning["SingleTop"] = (8, 4, 6)
        binning["TTJets"] = (10, 32, 42)
        binning["W3Jets"] = (12, 6, 12)
        if onlyWjets:
            binning["WJets"] = (10, 20, 60)
    if mcEvents:
        binning["TTJets"] = (12, 320, 440)
        binning["WJets"] = (24, 30, 90)

    for icol in xrange(table.getNcolumns()):
        name = table.getColumnNames()[icol]
        label = plots._legendLabels.get(name, name)
        if name != "Data":
            label += " MC"
        h = ROOT.TH1F(name, name, nrows, 0, nrows)
        h2 = ROOT.TH1F(name+"_dist", name, *(binning.get(name, (10, 0, 100))))
        mean = dataset.Count(0, 0)
        for irow in xrange(nrows):
            count = table.getCount(irow, icol)
            h.SetBinContent(irow+1, count.value())
            h.SetBinError(irow+1, count.uncertainty())
            h2.Fill(count.value())
            mean.add(count)
        mean = dataset.Count(mean.value()/nrows, mean.uncertainty()/nrows)

        h.Fit("fitFunction")

        value = function.GetParameter(0)
        error = function.GetParError(0)

        # function.SetParameters(1., 40., 1.);
        # function.SetParLimits(0, 0.0, 1.0);
        # fitResult = graph.Fit(function, "NRSE+EX0");
        # print "Fit status", fitResult.Status()
        # #fitResult.Print("V");
        # #fitResult.GetCovarianceMatrix().Print();
        # function.SetLineColor(graph.GetMarkerColor());
        # function.SetLineWidth(2);
        function.Draw("same")
        ROOT.gPad.Update()
        stat = h.FindObject("stats")
        if stat:
            stat.SetX1NDC(0.2)
            stat.SetX2NDC(0.44)
            stat.SetY1NDC(0.2)
            stat.SetY2NDC(0.3)
            stat.SetTextColor(ROOT.kRed)
            stat.SetLineColor(ROOT.kRed)
        # return (function, fitResult)

        styles.dataStyle.apply(h)
        p = plots.PlotBase([h])
        p.histoMgr.setHistoDrawStyle(name, "EP")
        p.createFrame("fluctuation_"+name, opts={"ymin": 0, "ymaxfactor": 1.2, "nbins": nrows})
        p.frame.GetXaxis().SetTitle("Embedding trial number")
        ylabel = "MC"
        if name == "Data":
            ylabel = "Data"
        ylabel += " events"
        p.frame.GetYaxis().SetTitle(ylabel)
        step = 1
        start = 0
        if onlyWjets:
            start = 4
            step = 5
        for irow in xrange(start, nrows, step):
            p.frame.GetXaxis().SetBinLabel(irow+1, "%d"%(irow+1))

        xmin = p.frame.GetXaxis().GetXmin()
        xmax = p.frame.GetXaxis().GetXmax()

        leg = histograms.moveLegend(histograms.createLegend(), dx=-0.07, dy=-0.6, dh=-0.15)
        leg.AddEntry(h, "Trial values", "P")

        def createLine(val, st=1, col=ROOT.kRed):
            l = ROOT.TLine(xmin, val, xmax, val)
            l.SetLineWidth(2)
            l.SetLineStyle(st)
            l.SetLineColor(col)
            return l

        fv = createLine(value)
        leg.AddEntry(fv, "Fitted value", "L")
        p.appendPlotObject(fv)
        # fe = createLine(value+error, ROOT.kDashed)
        # leg.AddEntry(fe, "Fit uncertainty", "L")
        # p.appendPlotObject(fe)
        # p.appendPlotObject(createLine(value-error, ROOT.kDashed))
        v = createLine(mean.value(), col=ROOT.kBlue)
        leg.AddEntry(v, "Mean", "L")
        p.appendPlotObject(v)
        ve = createLine(mean.value()+mean.uncertainty(), st=ROOT.kDashed, col=ROOT.kBlue)
        leg.AddEntry(ve, "Mean uncertainty", "L")
        p.appendPlotObject(ve)
        p.appendPlotObject(createLine(mean.value()-mean.uncertainty(), st=ROOT.kDashed, col=ROOT.kBlue))

        p.legend = leg

        p.appendPlotObject(histograms.PlotText(0.48, 0.2, label, size=20))
        p.draw()
        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        if name == "Data":
            histograms.addLuminosityText(None, None, lumi)
        p.save()

        ###############

        f2.SetParameter(1, value)
        h2.Fit("fitG")
#        f2.Draw("same")
        ROOT.gPad.Update()
        stat = h2.FindObject("stats")
        if stat:
            stat.SetX1NDC(0.62)
            stat.SetX2NDC(0.9)
            stat.SetY1NDC(0.7)
            stat.SetY2NDC(0.85)
            stat.SetTextColor(ROOT.kRed)
            stat.SetLineColor(ROOT.kRed)

        styles.dataStyle.apply(h2)
        p = plots.PlotBase([h2])
        p.histoMgr.setHistoDrawStyle(name+"_dist", "HIST")
        p.createFrame("fluctuation_"+name+"_dist", opts={"ymin": 0, "ymaxfactor": 1.4, "nbins": nrows})
        p.frame.GetXaxis().SetTitle(ylabel)
        p.frame.GetYaxis().SetTitle("Occurrances")

        ymin = p.frame.GetYaxis().GetXmin()
        ymax = p.frame.GetYaxis().GetXmax()

        leg = histograms.moveLegend(histograms.createLegend(), dx=-0.07, dy=-0.25, dh=-0.15)
        leg.AddEntry(h2, "Trials", "F")
        leg.AddEntry(f2, "Gaussian fit", "L")

        def createLine2(val, st=1):
            l = ROOT.TLine(val, ymin, val, ymax)
            l.SetLineWidth(1)
            l.SetLineColor(ROOT.kBlue)
            l.SetLineStyle(st)
            return l

        p.appendPlotObject(h2, "FUNC")
        p.appendPlotObject(stat)
        p.appendPlotObject(histograms.PlotText(0.75, 0.88, label, size=20))
        # fv = createLine2(value)
        # leg.AddEntry(fv, "Fit of values", "L")
        # p.appendPlotObject(fv)
        # fe = createLine2(value+error, ROOT.kDashed)
        # leg.AddEntry(fe, "Fit of values unc.", "L")
        # p.appendPlotObject(fe)
        # p.appendPlotObject(createLine2(value-error, ROOT.kDashed))
        p.legend = leg

        p.draw()

        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        p.save()



if __name__ == "__main__":
    main()

