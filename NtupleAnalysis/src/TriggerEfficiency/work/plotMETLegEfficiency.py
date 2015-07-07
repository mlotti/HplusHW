#!/usr/bin/env python

import os
import sys
import ROOT
import array

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms

from plotTauLegEfficiency import getEfficiency,convert2TGraph,Print

ROOT.gROOT.SetBatch(True)
plotDir = "METLeg2015"

formats = [".png"]

def usage():
    print "\n"
    print "### Usage:   "+sys.argv[0]+" <multicrab dir>\n"
    print "\n"
    sys.exit()

def main():

    if len(sys.argv) < 2:
        usage()

    paths = [sys.argv[1]]

    analysis = "METLeg_2015A_MET80"
    datasets = dataset.getDatasetsFromMulticrabDirs(paths,analysisName=analysis)
    for d in datasets.getAllDatasets():
        print d.getName()
    style = tdrstyle.TDRStyle()

    dataset1 = datasets.getDataDatasets()
    dataset2 = datasets.getMCDatasets()

    eff1_MET80 = getEfficiency(dataset1)
    eff2_MET80 = getEfficiency(dataset2)

    styles.dataStyle.apply(eff1_MET80)
    styles.mcStyle.apply(eff2_MET80)
    eff1_MET80.SetMarkerSize(1)
    eff2_MET80.SetMarkerSize(1.5)

    p = plots.ComparisonPlot(histograms.HistoGraph(eff1_MET80, "eff1_MET80", "p", "P"),
                             histograms.HistoGraph(eff2_MET80, "eff2_MET80", "p", "P"))

    opts = {"ymin": 0, "ymax": 1.1}
    opts2 = {"ymin": 0.5, "ymax": 1.5}
    moveLegend = {"dx": -0.55, "dy": -0.15}

    name = "DataVsMC_L1HLTMET_PFMET_MET80"

    legend1 = "Data"
    legend2 = "MC"
    p.histoMgr.setHistoLegendLabelMany({"eff1_MET80": legend1, "eff2_MET80": legend2})

    p.createFrame(os.path.join(plotDir, name), createRatio=True, opts=opts, opts2=opts2)
    p.setLegend(histograms.moveLegend(histograms.createLegend(y1=0.8), **moveLegend))

    p.getFrame().GetYaxis().SetTitle("L1+HLT MET efficiency")
    p.getFrame().GetXaxis().SetTitle("MET Type 1 (GeV)")
    p.getFrame2().GetYaxis().SetTitle("Ratio")
    p.getFrame2().GetYaxis().SetTitleOffset(1.6)

    p.draw()
    lumi = 0.0
    histograms.addStandardTexts(lumi=lumi)

    if not os.path.exists(plotDir):
        os.mkdir(plotDir)
    p.save(formats)


    #### MET120

    analysis = "METLeg_2015A_MET120"
    datasets = dataset.getDatasetsFromMulticrabDirs(paths,analysisName=analysis)
    for d in datasets.getAllDatasets():
        print d.getName()
    style = tdrstyle.TDRStyle()

    dataset1 = datasets.getDataDatasets()
    dataset2 = datasets.getMCDatasets()

    eff1_MET120 = getEfficiency(dataset1)
    eff2_MET120 = getEfficiency(dataset2)

    styles.dataStyle.apply(eff1_MET120)
    styles.mcStyle.apply(eff2_MET120)
    eff1_MET120.SetMarkerSize(1)
    eff2_MET120.SetMarkerSize(1.5)

    p = plots.ComparisonPlot(histograms.HistoGraph(eff1_MET120, "eff1_MET120", "p", "P"),
                             histograms.HistoGraph(eff2_MET120, "eff2_MET120", "p", "P"))

    opts = {"ymin": 0, "ymax": 1.1}
    opts2 = {"ymin": 0.5, "ymax": 1.5}
    moveLegend = {"dx": -0.55, "dy": -0.15}

    name = "DataVsMC_L1HLTMET_PFMET_MET120"

    legend1 = "Data"
    legend2 = "MC"
    p.histoMgr.setHistoLegendLabelMany({"eff1_MET120": legend1, "eff2_MET120": legend2})

    p.createFrame(os.path.join(plotDir, name), createRatio=True, opts=opts, opts2=opts2)
    p.setLegend(histograms.moveLegend(histograms.createLegend(y1=0.8), **moveLegend))

    p.getFrame().GetYaxis().SetTitle("L1+HLT MET efficiency")
    p.getFrame().GetXaxis().SetTitle("MET Type 1 (GeV)")
    p.getFrame2().GetYaxis().SetTitle("Ratio")
    p.getFrame2().GetYaxis().SetTitleOffset(1.6)

    p.draw()
    lumi = 0.0
    histograms.addStandardTexts(lumi=lumi)

    if not os.path.exists(plotDir):
        os.mkdir(plotDir)
    p.save(formats)


    # CaloMET

    #### MET80

    analysisc = "METLeg_2015A_CaloMET_MET80"
    datasetsc = dataset.getDatasetsFromMulticrabDirs(paths,analysisName=analysisc)

    style = tdrstyle.TDRStyle()

    dataset1c = datasetsc.getDataDatasets()
    dataset2c = datasetsc.getMCDatasets()

    eff1c_MET80 = getEfficiency(dataset1c)
    eff2c_MET80 = getEfficiency(dataset2c)

    styles.dataStyle.apply(eff1c_MET80)
    styles.mcStyle.apply(eff1c_MET80)
    eff1c_MET80.SetMarkerSize(1)
    eff2c_MET80.SetMarkerSize(1.5)

    p = plots.ComparisonPlot(histograms.HistoGraph(eff2_MET80, "eff2_MET80", "p", "P"),
                             histograms.HistoGraph(eff2c_MET80, "eff2c_MET80", "p", "P"))

    namec = "MC_TrgBinVsCaloMET80_L1HLTMET_PFMET"

    legend1c = "MC, trigger bin"
    legend2c = "MC, CaloMET > 80"
    p.histoMgr.setHistoLegendLabelMany({"eff2_MET80": legend1c, "eff2c_MET80": legend2c})

    p.createFrame(os.path.join(plotDir, namec), createRatio=True, opts=opts, opts2=opts2)
    p.setLegend(histograms.moveLegend(histograms.createLegend(y1=0.8), **moveLegend))

    p.getFrame().GetYaxis().SetTitle("L1+HLT MET efficiency")
    p.getFrame().GetXaxis().SetTitle("MET Type 1 (GeV)")
    p.getFrame2().GetYaxis().SetTitle("Ratio")
    p.getFrame2().GetYaxis().SetTitleOffset(1.6)

    p.draw()
    lumi = 0.0
    histograms.addStandardTexts(lumi=lumi)

    if not os.path.exists(plotDir):
        os.mkdir(plotDir)
    p.save(formats)


    #### MET120 

    analysisc = "METLeg_2015A_CaloMET_MET120"
    datasetsc = dataset.getDatasetsFromMulticrabDirs(paths,analysisName=analysisc)

    style = tdrstyle.TDRStyle()

    dataset1c = datasetsc.getDataDatasets()
    dataset2c = datasetsc.getMCDatasets()

    eff1c_MET120 = getEfficiency(dataset1c)
    eff2c_MET120 = getEfficiency(dataset2c)

    styles.dataStyle.apply(eff1c_MET120)
    styles.mcStyle.apply(eff1c_MET120)
    eff1c_MET120.SetMarkerSize(1)
    eff2c_MET120.SetMarkerSize(1.5)

    p = plots.ComparisonPlot(histograms.HistoGraph(eff2_MET120, "eff2_MET120", "p", "P"),
                             histograms.HistoGraph(eff2c_MET120, "eff2c_MET120", "p", "P"))

    namec = "MC_TrgBinVsCaloMET120_L1HLTMET_PFMET"

    legend1c = "MC, trigger bin"
    legend2c = "MC, CaloMET > 120"
    p.histoMgr.setHistoLegendLabelMany({"eff2_MET120": legend1c, "eff2c_MET120": legend2c})

    p.createFrame(os.path.join(plotDir, namec), createRatio=True, opts=opts, opts2=opts2)
    p.setLegend(histograms.moveLegend(histograms.createLegend(y1=0.8), **moveLegend))

    p.getFrame().GetYaxis().SetTitle("L1+HLT MET efficiency")
    p.getFrame().GetXaxis().SetTitle("MET Type 1 (GeV)")
    p.getFrame2().GetYaxis().SetTitle("Ratio")
    p.getFrame2().GetYaxis().SetTitleOffset(1.6)

    p.draw()
    lumi = 0.0
    histograms.addStandardTexts(lumi=lumi)

    if not os.path.exists(plotDir):
        os.mkdir(plotDir)
    p.save(formats)

if __name__ == "__main__":
    main()
