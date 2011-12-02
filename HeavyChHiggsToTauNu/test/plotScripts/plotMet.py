#!/usr/bin/env python

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect

analysis = "signalAnalysis"
counters = analysis+"Counters/weighted"

def main():
    datasets = dataset.getDatasetsFromMulticrabCfg(counters=counters)
#    datasets.loadLuminosities()
    datasets.remove(filter(lambda name: "TTToHplus" in name and not "M120" in name, datasets.getAllDatasetNames()))
    plots.mergeRenameReorderForDataMC(datasets)
    xsect.setHplusCrossSectionsToBR(datasets, br_tH=0.05, br_Htaunu=1)
    plots.mergeWHandHH(datasets)

    style = tdrstyle.TDRStyle()
    td = dataset.TreeDraw(analysis+"/tree", weight="weightPileup*weightTrigger*weightPrescale", 
                          selection="genMet_p4.Et() > 20"
#                          selection="genMet_p4.Et() > 20 && jets_p4@.size() >= 1"
#                          selection="genMet_p4.Et() > 20 && jets_p4@.size() >= 2"
#                          selection="genMet_p4.Et() > 20 && jets_p4@.size() >= 3"
                          )

    kwargs = {}
    kwargs["normalizeToLumi"] = 1150

    dist=">>dist(25,0,5)"
    for q in ["Et", "X", "Y", "Phi"]:
        rawRes = plots.DataMCPlot(datasets, td.clone(varexp="met_p4.%s()/genMet_p4.%s() %s" % (q, q, dist)), **kwargs)
        type1Res = plots.DataMCPlot(datasets, td.clone(varexp="metType1_p4.%s()/genMet_p4.%s() %s" % (q, q, dist)), **kwargs)
        #type1Res = plots.DataMCPlot(datasets, td.clone(varexp="tcMet_p4.%s()/genMet_p4.%s() %s" % (q, q, dist)), normalizeToLumi=1150)

        compare(rawRes, type1Res, q, "TTJets")
#        compare(rawRes, type1Res, q, "WJets")
#        compare(rawRes, type1Res, q, "TTToHplus_M120")

def compare(raw, type1, quantity, name):
    rawTh1 = raw.histoMgr.getHisto(name).getRootHisto().Clone("Raw")
    type1Th1 = type1.histoMgr.getHisto(name).getRootHisto().Clone("Type1")

    styles.dataStyle.apply(rawTh1)
    styles.mcStyle.apply(type1Th1)

    plot = plots.ComparisonPlot(
        histograms.Histo(rawTh1, "Raw"),
        histograms.Histo(type1Th1, "Type 1")
        )
    q = " "+quantity
    if quantity == "Et":
        q = ""

    plot.setLegend(histograms.moveLegend(histograms.createLegend(), dh=0.15))
    plot.createFrame("metres_%s_%s" % (name, quantity))
    plot.frame.GetXaxis().SetTitle("MET%s/genMET%s" % (q, q))
    plot.frame.GetYaxis().SetTitle("Events / %.2f" % raw.binWidth())
    plot.draw()
    l = ROOT.TLatex()
    l.SetNDC()
    x = 0.5
    y = 0.7
    dy = 0.05
    l.DrawLatex(x, y, name); y -= dy
    l.SetTextSize(l.GetTextSize()*0.7)
    l.SetTextColor(rawTh1.GetLineColor())
    l.DrawLatex(x, y, "Raw mean %.2f, stddev %.2f" % (rawTh1.GetMean(), rawTh1.GetRMS())); y -= dy
    l.SetTextColor(type1Th1.GetLineColor())
    l.DrawLatex(x, y, "Type 1 mean %.2f, stddev %.2f" % (type1Th1.GetMean(), type1Th1.GetRMS())); y -= dy

    plot.save()


if __name__ == "__main__":
    main()
