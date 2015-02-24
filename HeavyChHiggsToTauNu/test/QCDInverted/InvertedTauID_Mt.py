#!/usr/bin/env python

import ROOT
ROOT.gROOT.SetBatch(True)
from ROOT import *
import math
import sys
import os
import re

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
    print
    print "### Usage:   ",os.path.basename(sys.argv[0])," <multicrab dir>"
    print
    sys.exit()

try:
    import QCDInvertedNormalizationFactors
except ImportError:
    print
    print "    WARNING, QCDInvertedNormalizationFactors.py not found!"
    print "    Run script InvertedTauID_Normalization.py to generate QCDInvertedNormalizationFactors.py"
    print 

def sort(normdict):

    eq_re = re.compile("taup_Teq(?P<value>\d+)to")
    lt_re = re.compile("taup_Tlt(?P<value>\d+)")
    gt_re = re.compile("taup_Tgt(?P<value>\d+)")

    binmap = {}
    value = 0
    for bin in normdict.keys():
        match = eq_re.search(bin)
        if match:
            value = int(match.group("value"))
            binmap[value] = bin
            continue
        match = lt_re.search(bin)
        if match:
            value = int(match.group("value")) - 1
            binmap[value] = bin
            continue
        match = gt_re.search(bin)
        if match:
            value = int(match.group("value")) + 1
            binmap[value] = bin
            continue

    i = 0
    retdict = {}
    for bin in sorted(binmap.keys()):
        retdict[i] = normdict[binmap[bin]]
        i += 1

    return retdict

def main(argv):

    dirs = []
    if len(sys.argv) < 2:
	usage()

    dirs.append(sys.argv[1])

    QCDInvertedNormalization = sort(QCDInvertedNormalizationFactors.QCDInvertedNormalization)

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
                mt.Scale(QCDInvertedNormalization[i])
                color += 1
                if color == 5:
                    color += 1
            else:
                h = mtplot.histoMgr.getHisto("Data").getRootHisto().Clone(HISTONAME+"/"+HISTONAME+bin)
                h.Scale(QCDInvertedNormalization[i])
                mt.Add(h)
 
        plot.histoMgr.appendHisto(histograms.Histo(mt,mt.GetName()))

    style = tdrstyle.TDRStyle()

    plot.createFrame("mt")
    moveLegend={"dx": -0.15,"dy": 0.}
    plot.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))

    plot.setLuminosity(datasets.getDataset("Data").getLuminosity())
    plot.addStandardTexts()

    plot.draw()
    plot.save()

if __name__ == "__main__":
    main(sys.argv)
