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

from plotTauLegEfficiency import getEfficiency,convert2TGraph

ROOT.gROOT.SetBatch(True)
plotDir = "METLeg2012"

def usage():
    print "\n"
    print "### Usage:   "+sys.argv[0]+" <multicrab dir>\n"
    print "\n"
    sys.exit()

def main():

    if len(sys.argv) < 2:
        usage()

    paths = [sys.argv[1]]

#    analysis = "METLeg_2012D"
    analysis = "METLeg_2012ABCD"
    datasets = dataset.getDatasetsFromMulticrabDirs(paths,analysisName=analysis)
    for d in datasets.getAllDatasets():
        print d.getName()
    style = tdrstyle.TDRStyle()

    dataset1 = datasets.getDataDatasets()
    dataset2 = datasets.getMCDatasets()

    eff1 = getEfficiency(dataset1)
    eff2 = getEfficiency(dataset2)

    styles.dataStyle.apply(eff1)
    styles.mcStyle.apply(eff2)
    eff1.SetMarkerSize(1)
    eff2.SetMarkerSize(1.5)

    p = plots.ComparisonPlot(histograms.HistoGraph(eff1, "eff1", "p", "P"),
                             histograms.HistoGraph(eff2, "eff2", "p", "P"))

    opts = {"ymin": 0, "ymax": 1.1}
    opts2 = {"ymin": 0.5, "ymax": 1.5}
    moveLegend = {"dx": -0.55, "dy": -0.15}

    name = "DataVsMC_L1HLTMET_PFMET"

    legend1 = "Data"
    legend2 = "MC"
    p.histoMgr.setHistoLegendLabelMany({"eff1": legend1, "eff2": legend2})

    p.createFrame(os.path.join(plotDir, name), createRatio=True, opts=opts, opts2=opts2)
    p.setLegend(histograms.moveLegend(histograms.createLegend(y1=0.8), **moveLegend))

    p.getFrame().GetYaxis().SetTitle("L1+HLT MET efficiency")
    p.getFrame().GetXaxis().SetTitle("MET Type 1 (GeV)")
    p.getFrame2().GetYaxis().SetTitle("Ratio")
    p.getFrame2().GetYaxis().SetTitleOffset(1.6)

    p.draw()
    lumi = 19769.954
    histograms.addStandardTexts(lumi=lumi)

    if not os.path.exists(plotDir):
        os.mkdir(plotDir)
    p.save()



    # CaloMET

    analysisc = "METLeg_2012ABCD_CaloMET"
    datasetsc = dataset.getDatasetsFromMulticrabDirs(paths,analysisName=analysisc)

    style = tdrstyle.TDRStyle()

    dataset1c = datasetsc.getDataDatasets()
    dataset2c = datasetsc.getMCDatasets()

    eff1c = getEfficiency(dataset1c)
    eff2c = getEfficiency(dataset2c)

    styles.dataStyle.apply(eff1c)
    styles.mcStyle.apply(eff1c)
    eff1c.SetMarkerSize(1)
    eff2c.SetMarkerSize(1.5)

    p = plots.ComparisonPlot(histograms.HistoGraph(eff1, "eff1", "p", "P"),
                             histograms.HistoGraph(eff1c, "eff1c", "p", "P"))

    #opts = {"ymin": 0, "ymax": 1.1}
    #opts2 = {"ymin": 0.5, "ymax": 1.5}
    #moveLegend = {"dx": -0.55, "dy": -0.1}
    namec = "Data_TrgBinVsCaloMET_L1HLTMET_PFMET"

    legend1c = "Data, trigger bin"
    legend2c = "Data, CaloMET > 70"
    p.histoMgr.setHistoLegendLabelMany({"eff1": legend1c, "eff1c": legend2c})

    p.createFrame(os.path.join(plotDir, namec), createRatio=True, opts=opts, opts2=opts2)
    p.setLegend(histograms.moveLegend(histograms.createLegend(y1=0.8), **moveLegend))

    p.getFrame().GetYaxis().SetTitle("L1+HLT MET efficiency")
    p.getFrame().GetXaxis().SetTitle("MET Type 1 (GeV)")
    p.getFrame2().GetYaxis().SetTitle("Ratio")
    p.getFrame2().GetYaxis().SetTitleOffset(1.6)

    p.draw()
    lumi = 19769.954
    histograms.addStandardTexts(lumi=lumi)
    #histograms.addCmsPreliminaryText()
    #histograms.addEnergyText(s="%s TeV"%dataset2[0].info["energy"])
    #histograms.addLuminosityText(None, None, lumi)

    if not os.path.exists(plotDir):
        os.mkdir(plotDir)
    p.save()

if __name__ == "__main__":
    main()
