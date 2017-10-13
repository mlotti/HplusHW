#!/usr/bin/env python

import os
import sys

import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.styles as styles
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux

plotDir = "Plots2015"
formats = [".pdf",".png",".C"]

def usage():
    print "\n"
    print "### Usage:   "+sys.argv[0]+" <multicrab dir>\n"
    print "\n"
    sys.exit()

def removeNegatives(histo):
    for bin in range(histo.GetNbinsX()):
        if histo.GetBinContent(bin) < 0:
            histo.SetBinContent(bin,0.)

def main():

    if len(sys.argv) < 2:
        usage()

    paths = [sys.argv[1]]
    analysis = "Hplus2tbAnalysis"
    hName = "associatedTPt"
    plotname = analysis+"_"+hName


    datasetsHiggs = dataset.getDatasetsFromMulticrabDirs(paths,analysisName=analysis,includeOnlyTasks="ChargedHiggs_HplusTB_HplusToTauB_M_")
    datasetsTT    = dataset.getDatasetsFromMulticrabDirs(paths,analysisName=analysis,includeOnlyTasks="TT")
    datasetsTT.merge("MC", ["TT","TT_ext"], keepSources=True)

    style = tdrstyle.TDRStyle()

    dataset1 = datasetsHiggs.getDataset("ChargedHiggs_HplusTB_HplusToTauB_M_200").getDatasetRootHisto(hName)
    dataset2 = datasetsTT.getDataset("MC").getDatasetRootHisto(hName)
#    dataset1.normalizeToOne()
    dataset2.normalizeToOne()

    histo1 = dataset1.getHistogram()
    histo1.SetMarkerColor(2)
    histo1.SetMarkerStyle(20)
    removeNegatives(histo1)
    histo1.Scale(1./histo1.Integral())

    histo2 = dataset2.getHistogram()
    histo2.SetMarkerColor(4)
    histo2.SetMarkerStyle(21)

    p = plots.ComparisonPlot(histograms.Histo(histo1, "m_{H^{#pm}} = 200 GeV/c^{2}", "p", "P"),
                             histograms.Histo(histo2, "t#bar{t}", "p", "P"))

    opts = {"ymin": 0, "ymax": 0.2}
    opts2 = {"ymin": 0.5, "ymax": 1.5}
    p.createFrame(os.path.join(plotDir, plotname), createRatio=True, opts=opts, opts2=opts2)

    moveLegend = {"dx": -0.2, "dy": -0.1, "dh": -0.1}
    p.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))

    p.getFrame().GetYaxis().SetTitle("Arbitrary units")
    p.getFrame().GetXaxis().SetTitle("Top p_{T} (GeV/c)")
    p.getFrame2().GetYaxis().SetTitle("Ratio")
    p.getFrame2().GetYaxis().SetTitleOffset(1.6)

    p.draw()
    if not os.path.exists(plotDir):
        os.mkdir(plotDir)
    p.save(formats)

if __name__ == "__main__":
    main()
