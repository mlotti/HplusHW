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
counters = analysis+"Counters"

def main():
    datasets = dataset.getDatasetsFromMulticrabCfg(counters=counters)
    datasets.updateNAllEventsToPUWeighted()
    datasets.loadLuminosities()
    datasets.remove(filter(lambda name: "TTToHplus" in name and not "M120" in name, datasets.getAllDatasetNames()))
    plots.mergeRenameReorderForDataMC(datasets)
    xsect.setHplusCrossSectionsToBR(datasets, br_tH=0.05, br_Htaunu=1)
    plots.mergeWHandHH(datasets)

    style = tdrstyle.TDRStyle()

    plot = plots.DataMCPlot(datasets, analysis+"/MET/met")
    plot.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
    
    plot.createFrame("MET", opts={"ymin": 1e-4, "ymaxfactor": 10})
    plot.getPad().SetLogy(True)

    plot.setLegend(histograms.createLegend())

    plot.frame.GetXaxis().SetTitle("MET (GeV)")
    plot.frame.GetYaxis().SetTitle("Number of events")

    plot.draw()
    plot.addLuminosityText()

    plot.save()


if __name__ == "__main__":
    main()
