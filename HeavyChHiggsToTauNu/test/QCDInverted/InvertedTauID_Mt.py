#!/usr/bin/env python

import ROOT
ROOT.gROOT.SetBatch(True)
from ROOT import *
import math
import sys

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect


#dataEra = "Run2011AB"
dataEra = "Run2012ABCD"


searchMode = "Light"
#searchMode = "Heavy"

HISTONAME = "shapeTransverseMass"

def usage():
    print "\n"
    print "### Usage:   InvertedTauID_Normalization.py <multicrab dir>\n"
    print "\n"
    sys.exit()

def main(argv):

    dirs = []
    if len(sys.argv) < 2:
	usage()

    dirs.append(sys.argv[1])

    analysis = "signalAnalysisInvertedTau"
    optModes = []
    optModes.append("OptQCDTailKillerZeroPlus")
    optModes.append("OptQCDTailKillerLoosePlus") 
    optModes.append("OptQCDTailKillerMediumPlus") 
    optModes.append("OptQCDTailKillerTightPlus") 
    optModes.append("OptQCDTailKillerVeryTightPlus")
                    
    plot = plots.PlotBase()
    color = 1
    for optMode in optModes:
        datasets = dataset.getDatasetsFromMulticrabDirs(dirs,dataEra=dataEra,  searchMode=searchMode, analysisName=analysis, optimizationMode=optMode)
        datasets.updateNAllEventsToPUWeighted()
        datasets.loadLuminosities()

        plots.mergeRenameReorderForDataMC(datasets)

        histonames = datasets.getDataset("Data").getDirectoryContent(HISTONAME)
        bins = []
        for histoname in histonames:
            binname = histoname.replace(HISTONAME,"")
            if not binname == "Inclusive":
                bins.append(binname)


        for i,bin in enumerate(bins):
            mtplot = plots.DataMCPlot(datasets, HISTONAME+"/"+HISTONAME+bin)
            if i == 0:
                mt = mtplot.histoMgr.getHisto("Data").getRootHisto().Clone(HISTONAME+"/"+HISTONAME+bin)
                legendName = optMode.replace("OptQCDTailKiller","R_{BB} ")
                legendName = legendName.replace("Plus","")
                mt.SetName(legendName)
                mt.SetLineColor(color)
                color += 1
                if color == 5:
                    color += 1
            else:
                mt.Add(mtplot.histoMgr.getHisto("Data").getRootHisto().Clone(HISTONAME+"/"+HISTONAME+bin))
 
        plot.histoMgr.appendHisto(histograms.Histo(mt,mt.GetName()))

    style = tdrstyle.TDRStyle()

    plot.createFrame("mt")
    moveLegend={"dx": -0.15,"dy": 0.}
    plot.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))

    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    lumi=datasets.getDataset("Data").getLuminosity()
    histograms.addLuminosityText(x=None, y=None, lumi=lumi)

    plot.draw()
    plot.save()

if __name__ == "__main__":
    main(sys.argv)
