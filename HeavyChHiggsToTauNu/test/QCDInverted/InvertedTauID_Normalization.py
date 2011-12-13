#!/usr/bin/env python

###########################################################################
#
# This script is only intended as an example, please do NOT modify it.
# For example, start from scratch and look here for help, or make a
# copy of it and modify the copy (including removing all unnecessary
# code).
#
###########################################################################

import ROOT
#ROOT.gROOT.SetBatch(True)
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

from InvertedTauID import *

def main():

    HISTONAME = "TauIdJets"
#    HISTONAME = "TauIdBtag"
    
    # Create all datasets from a multicrab task
    datasets = dataset.getDatasetsFromMulticrabCfg(counters=counters)

    # Read integrated luminosities of data datasets from lumi.json
    datasets.loadLuminosities()

    # Include only 120 mass bin of HW and HH datasets
    datasets.remove(filter(lambda name: "TTToHplus" in name and not "M120" in name, datasets.getAllDatasetNames()))

    # Default merging nad ordering of data and MC datasets
    # All data datasets to "Data"
    # All QCD datasets to "QCD"
    # All single top datasets to "SingleTop"
    # WW, WZ, ZZ to "Diboson"
    plots.mergeRenameReorderForDataMC(datasets)

    # Set BR(t->H) to 0.05, keep BR(H->tau) in 1
    xsect.setHplusCrossSectionsToBR(datasets, br_tH=0.05, br_Htaunu=1)

    # Merge WH and HH datasets to one (for each mass bin)
    # TTToHplusBWB_MXXX and TTToHplusBHminusB_MXXX to "TTToHplus_MXXX"
    plots.mergeWHandHH(datasets)

    datasets.merge("EWK", [
	    "TTJets",
            "WJets",
            "DYJetsToLL",
            "SingleTop",
            "Diboson"
            ])

    # Apply TDR style
    style = tdrstyle.TDRStyle()

    invertedQCD = InvertedTauID()
    invertedQCD.setLumi(datasets.getDataset("Data").getLuminosity())

    metBase = plots.DataMCPlot(datasets, analysis+"/MET_BaseLine"+HISTONAME)
    metInver = plots.DataMCPlot(datasets, analysis+"/MET_Inverted"+HISTONAME)  

    # Rebin before subtracting
    metBase.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
    metInver.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
    
    metInverted_data = metInver.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_Inverted"+HISTONAME)
    metInverted_EWK = metInver.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MET_Inverted"+HISTONAME) 
    metBase_data = metBase.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_Baseline"+HISTONAME)
    metBase_EWK = metBase.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MET_Baseline"+HISTONAME)

    metBase_data.SetTitle("Data: BaseLine TauID")
    metInverted_data.SetTitle("Data: Inverted TauID")
    metBase_QCD = metBase_data.Clone("QCD")
    metBase_QCD.Add(metBase_EWK,-1)
    metBase_QCD.SetTitle("Data - EWK MC: BaseLine TauID")

#    invertedQCD.setLabel("BaseVsInverted")
#    invertedQCD.comparison(metInverted_data,metBase_data)
#    invertedQCD.setLabel("BaseMinusEWKVsInverted")
#    invertedQCD.comparison(metInverted_data,metBase_QCD)


    invertedQCD.setLabel("inclusive")
    invertedQCD.plotHisto(metInverted_data,"inverted")
    invertedQCD.plotHisto(metBase_data,"baseline")
    invertedQCD.fitQCD(metInverted_data)
    invertedQCD.fitEWK(metBase_EWK,"LR")  
    invertedQCD.fitData(metBase_data)
    normalizationWithEWK = invertedQCD.getNormalization()

#    bins = ["4050","5060","6070","7080","80100","100120","120150","150"]
#    bins = ["4050","5060","6070","7080","80100","120150","150"]
    bins = []

    for bin in bins:

        metBase = plots.DataMCPlot(datasets, analysis+"/MET_BaseLineTauIdJets"+bin)
        metInver = plots.DataMCPlot(datasets, analysis+"/MET_InvertedTauIdJets"+bin)
        # Rebin before subtracting
        metBase.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
        metInver.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))

        metInverted_data = metInver.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdJets"+bin)
        metInverted_EWK = metInver.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MET_InvertedTauIdJets"+bin)
        metBase_data = metBase.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_BaselineTauIdJets"+bin)
        metBase_EWK = metBase.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MET_BaselineTauIdJets"+bin)

        metBase_QCD = metBase_data.Clone("QCD")
        metBase_QCD.Add(metBase_EWK,-1)

	invertedQCD.setLabel(bin)
#        invertedQCD.comparison(metInverted_data,metBase_QCD)
        invertedQCD.fitQCD(metInverted_data)
        invertedQCD.fitEWK(metBase_EWK)
        invertedQCD.fitData(metBase_data)
        invertedQCD.getNormalization()

    invertedQCD.Summary()


if __name__ == "__main__":
    main()
