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

#HISTONAME = "InvertedJetBalance"
#histonameList = ["BaselineJetBalance", "BaselineAllCutsJetBalance"]
#histonameList = ["InvertedJetBalance", "InvertedAllCutsJetBalance"]
#histonameList = ["InvertedJetBalance", "BaselineJetBalance"]
#histonameList = ["InvertedAllCutsJetBalance", "BaselineAllCutsJetBalance"]
histonameList = ["InvertedJetBalance", "BaselineJetBalance", "InvertedAllCutsJetBalance", "BaselineAllCutsJetBalance"]

def usage():
    print
    print "### Usage:   ",os.path.basename(sys.argv[0])," <multicrab dir>"
    print
    sys.exit()

def main(argv):

    dirs = []
    if len(sys.argv) < 2:
	usage()

    dirs.append(sys.argv[1])

    analysis = "signalAnalysisInvertedTau"
    optModes = []
    #optModes.append("")
    #optModes.append("OptQCDTailKillerLoosePlus") 
    #optModes.append("OptQCDTailKillerMediumPlus") 
    optModes.append("OptQCDTailKillerTightPlus") 

    color = 1
    #plot = plots.PlotBase()
    jetRatios = []
    
    for HISTONAME in histonameList:            
        for optMode in optModes:
            plot = plots.PlotBase()
            datasets = dataset.getDatasetsFromMulticrabDirs(dirs,dataEra=dataEra,  searchMode=searchMode, analysisName=analysis, optimizationMode=optMode)

            datasets.updateNAllEventsToPUWeighted()
            datasets.loadLuminosities()

            plots.mergeRenameReorderForDataMC(datasets)

            datasets.merge("EWK", [
                "TTJets",
                "WJets",
                "DYJetsToLL",
                "SingleTop",
                "Diboson"
                ])

            histonames = datasets.getDataset("EWK").getDirectoryContent(HISTONAME)
            mtplot = plots.DataMCPlot(datasets, HISTONAME)
            mt = mtplot.histoMgr.getHisto("EWK").getRootHisto().Clone(HISTONAME)
            #legendName = legendName.replace("Plus","")
            mt.SetName("JetBalance")
            mt.SetLineColor(color)
            if HISTONAME == "InvertedAllCutsJetBalance":
                qinv = mt.GetBinContent(1)
                ginv = mt.GetBinContent(3)
            else:
                qbase = mt.GetBinContent(1)
                gbase = mt.GetBinContent(3)

            jetRatios.append(mt.GetBinContent(1)/(mt.GetBinContent(1)+mt.GetBinContent(3)))
            
            plot.histoMgr.appendHisto(histograms.Histo(mt,mt.GetName()))
            color = color + 1 
            
            style = tdrstyle.TDRStyle()
        
            plot.createFrame(HISTONAME)
        #plot.createFrame(HISTONAME.replace("shape","final"))
        #plot.createFrame(optMode.replace("Opt","Mt_DataDrivenVsMC_"))
        #moveLegend={"dx": -0.3,"dy": 0.}
        #plot.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))

            histograms.addCmsPreliminaryText()
            histograms.addEnergyText()
            lumi=datasets.getDataset("Data").getLuminosity()
            histograms.addLuminosityText(x=None, y=None, lumi=lumi)

            plot.draw()
            plot.save()

    print "Baseline All Cuts",qbase+gbase
    print "Inverted All Cuts",qinv+ginv
    gsf = qinv*gbase/(ginv*qbase)
    #print "Gluon jet SF:", gsf
    #print "Corrected Inverted Jet Balance:", qinv/(qinv+gsf*ginv), ", Baseline Jet Balance:", qbase/(qbase+gbase)
    for i in range(0,len(jetRatios)):
        print histonameList[i],":",jetRatios[i]
    
if __name__ == "__main__":
    main(sys.argv)
