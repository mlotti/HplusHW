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

#HISTONAME = "shapeTransverseMass"
histoNameList = ["shapeTransverseMass", "shapeEWKGenuineTausTransverseMass"]

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

try:
    import QCDInvertedNormalizationFactorsFilteredEWKFakeTaus
except ImportError:
    print
    print "    WARNING, QCDInvertedNormalizationFactorsFilteredEWKFakeTaus.py not found!"
    print "    Run script InvertedTauID_Normalization.py to generate QCDInvertedNormalizationFactorsFilteredEWKFakeTaus.py"
    print 

def main(argv):

    dirs = []
    if len(sys.argv) < 2:
	usage()

    dirs.append(sys.argv[1])

    QCDInvertedNormalization = QCDInvertedNormalizationFactors.QCDInvertedNormalization
    QCDInvertedNormalizationFilteredEWKFakeTaus = QCDInvertedNormalizationFactorsFilteredEWKFakeTaus.QCDInvertedNormalization
    analysis = "signalAnalysisInvertedTau"
    optModes = []
    #optModes.append("OptQCDTailKillerZeroPlus")
    optModes.append("OptQCDTailKillerLoosePlus") 
    optModes.append("OptQCDTailKillerMediumPlus") 
    optModes.append("OptQCDTailKillerTightPlus") 
    #optModes.append("OptQCDTailKillerVeryTightPlus")
    #optModes.append("OnlyGenuineMCTausFalse")
    #optModes.append("OnlyGenuineMCTausTrue")

    for optMode in optModes:
        plot = plots.PlotBase()
        color = 1

        dirs_signal = ["../../SignalAnalysis_140605_143702/"]
        datasets_signal = dataset.getDatasetsFromMulticrabDirs(dirs_signal,dataEra=dataEra,  searchMode=searchMode, analysisName=analysis.replace("InvertedTau",""), optimizationMode=optMode)
        
        datasets_signal.updateNAllEventsToPUWeighted()
        datasets_signal.loadLuminosities()
        
        datasets_signal.remove(filter(lambda name: "TTToHplus" in name, datasets_signal.getAllDatasetNames()))
        datasets_signal.remove(filter(lambda name: "HplusTB" in name, datasets_signal.getAllDatasetNames()))
        datasets_signal.remove(filter(lambda name: "Hplus_taunu_t-channel" in name, datasets_signal.getAllDatasetNames()))
        datasets_signal.remove(filter(lambda name: "Hplus_taunu_tW-channel" in name, datasets_signal.getAllDatasetNames()))
        datasets_signal.remove(filter(lambda name: "TTJets_SemiLept" in name, datasets_signal.getAllDatasetNames()))
        datasets_signal.remove(filter(lambda name: "TTJets_FullLept" in name, datasets_signal.getAllDatasetNames()))
        datasets_signal.remove(filter(lambda name: "TTJets_Hadronic" in name, datasets_signal.getAllDatasetNames()))
        
        plots.mergeRenameReorderForDataMC(datasets_signal)
        
        datasets_signal.merge("EWK", [
            "TTJets",
            "WJets",
            "DYJetsToLL",
            "SingleTop",
            "Diboson"
            ])
        
        mtplot_signalfaketaus = plots.DataMCPlot(datasets_signal, "shapeEWKFakeTausTransverseMass")
        mt_signalfaketaus = mtplot_signalfaketaus.histoMgr.getHisto("EWK").getRootHisto().Clone("shapeEWKFakeTausTransverseMass")
        
        for HISTONAME in histoNameList:
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

            histonames = datasets.getDataset("Data").getDirectoryContent(HISTONAME)

            bins = []
            for histoname in histonames:
                binname = histoname.replace(HISTONAME,"")
                if not binname == "Inclusive":
                    bins.append(binname)

            invjet_name = "MTInvertedTauIdAfterAllSelectionsPlusJetFakeTau"
            basejet_name = "MTBaselineTauIdAfterAllSelectionsPlusJetFakeTau"

            for i,bin in enumerate(bins):
                mtplot = plots.DataMCPlot(datasets, HISTONAME+"/"+HISTONAME+bin)

                if i == 0:
                    mt = mtplot.histoMgr.getHisto("Data").getRootHisto().Clone(HISTONAME+"/"+HISTONAME+bin)
                    mt_ewk = mtplot.histoMgr.getHisto("EWK").getRootHisto().Clone(HISTONAME+"/"+HISTONAME+bin)
                    
                    if HISTONAME == "shapeEWKGenuineTausTransverseMass":
                        legendName = "Data-driven Fake Taus"
                    else:
                        legendName = "Simulated Fake Taus"
                    legendName = legendName.replace("Plus","")
                    mt.SetName(legendName)
                    mt.SetLineColor(color)
                    mt.Add(mt_ewk,-1)
                    
                    if HISTONAME == "shapeEWKGenuineTausTransverseMass":
                        mt.Scale(QCDInvertedNormalizationFilteredEWKFakeTaus[str(i)])
                    else:
                        mt.Scale(QCDInvertedNormalization[str(i)])
                    color += 1
                    if color == 5:
                        color += 1
                else:
                    h = mtplot.histoMgr.getHisto("Data").getRootHisto().Clone(HISTONAME+"/"+HISTONAME+bin)
                    mt_ewk = mtplot.histoMgr.getHisto("EWK").getRootHisto().Clone(HISTONAME+"/"+HISTONAME+bin)
                    h.Add(mt_ewk,-1)
                    if HISTONAME == "shapeEWKGenuineTausTransverseMass":
                        h.Scale(QCDInvertedNormalizationFilteredEWKFakeTaus[str(i)])
                    else:
                        h.Scale(QCDInvertedNormalization[str(i)])
                    mt.Add(h)
            if HISTONAME == "shapeTransverseMass":
                mt.Add(mt_signalfaketaus)

            
            plot.histoMgr.appendHisto(histograms.Histo(mt,mt.GetName()))
            
            style = tdrstyle.TDRStyle()

        #plot.createFrame("mt")
        #plot.createFrame(HISTONAME.replace("shape","final"))
        plot.createFrame(optMode.replace("Opt","Mt_DataDrivenVsMC_"))
        moveLegend={"dx": -0.3,"dy": 0.}
        plot.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))


        histograms.addText(0.65, 0.20, optMode.replace("OptQCDTailKiller","R_{BB} ").replace("Plus",""), 25)
        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        lumi=datasets.getDataset("Data").getLuminosity()
        histograms.addLuminosityText(x=None, y=None, lumi=lumi)

        plot.draw()
        plot.save()

if __name__ == "__main__":
    main(sys.argv)
