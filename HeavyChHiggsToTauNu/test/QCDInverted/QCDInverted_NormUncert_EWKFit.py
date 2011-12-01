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

from QCDInverted_Normalization import *


def main():
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

    ttjets2 = datasets.getDataset("TTJets").deepCopy()
    ttjets2.setCrossSection(ttjets2.getCrossSection()-datasets.getDataset("TTToHplus_M120").getCrossSection())
    print "Set TTJets2 cross section to %f" % ttjets2.getCrossSection()
    ttjets2.setName("TTJets2")
    datasets.append(ttjets2)

    datasets.merge("EWKnott", [
            "WJets",
            "DYJetsToLL",
            "SingleTop",
            "Diboson"
            ])
    tmp = datasets.getDataset("EWKnott").deepCopy()
    tmp.setName("EWKnott2")
    datasets.append(tmp)

    datasets.merge("EWK", [
        "EWKnott",
        "TTJets"
        ])

    # Apply TDR style
    style = tdrstyle.TDRStyle()

    invertedQCD = InvertedTauID()

    metBase = plots.DataMCPlot(datasets, analysis+"/MET_BaseLineTauIdJets")
    metInver = plots.DataMCPlot(datasets, analysis+"/MET_InvertedTauIdJets")  
    # Rebin before subtracting
    metBase.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
    metInver.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
    
    metInverted_data = metInver.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdJets")
    metInverted_EWK = metInver.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MET_InvertedTauIdJets") 
    metBase_data = metBase.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_BaselineTauIdJets")
    metBase_EWK = metBase.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MET_BaselineTauIdJets")

    metBase_QCD = metBase_data.Clone("QCD")
    metBase_QCD.Add(metBase_EWK,-1)

    metBase_EWK.SetTitle("MC EWK")

    invertedQCD.setLabel("InvData")
    invertedQCD.fitQCD(metInverted_data)

    invertedQCD.setLabel("ChiSq")
    invertedQCD.fitEWK(metBase_EWK,"R")
    invertedQCD.fitData(metBase_data)
    normalizationWithChiSq = invertedQCD.getNormalization()

    invertedQCD.setLabel("LogLikelihood")
    invertedQCD.fitEWK(metBase_EWK,"LR")
    invertedQCD.fitData(metBase_data)
    normalizationWithLogLL = invertedQCD.getNormalization()
    
    print "Difference Signal vs no signal in EWK fit",(normalizationWithLogLL - normalizationWithChiSq)/normalizationWithChiSq

if __name__ == "__main__":
    main()
