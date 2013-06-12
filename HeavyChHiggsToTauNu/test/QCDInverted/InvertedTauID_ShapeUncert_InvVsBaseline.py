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

#dataEra = "Run2011A"
#dataEra = "Run2011B"
dataEra = "Run2011AB"

searchMode = "Light"
#searchMode = "Heavy"

def main():

    errorBars = False
    dirs = []
    if len(sys.argv) < 2:
        usage()

    dirs.append(sys.argv[1])
    

    # Create all datasets from a multicrab task
    datasets = dataset.getDatasetsFromMulticrabDirs(dirs,dataEra=dataEra,  searchMode=searchMode, analysisName=analysis) 
#    datasets = dataset.getDatasetsFromMulticrabDirs(dirs, counters=counters, dataEra=dataEra,  analysisBaseName="signalAnalysisInvertedTau")
##    datasets = dataset.getDatasetsFromMulticrabCfg(counters=counters, dataEra=dataEra)

    # As we use weighted counters for MC normalisation, we have to
    # update the all event count to a separately defined value because
    # the analysis job uses skimmed pattuple as an input
    datasets.updateNAllEventsToPUWeighted()

    # Read integrated luminosities of data datasets from lumi.json
    datasets.loadLuminosities()

    # Include only 120 mass bin of HW and HH datasets
    datasets.remove(filter(lambda name: "TTToHplus" in name and not "M120" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "HplusTB" in name, datasets.getAllDatasetNames()))
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
    invertedQCD.useErrorBars(errorBars)

    metBase = plots.DataMCPlot(datasets, "BaseLine/MET_BaseLineTauIdBvetoCollinear")
    metInver = plots.DataMCPlot(datasets, "Inverted/MET_InvertedTauIdBvetoCollinear")
#    metBase = plots.DataMCPlot(datasets, "BaseLine/MET_BaseLineTauIdJetsCollinear")
#    metInver = plots.DataMCPlot(datasets, "Inverted/MET_InvertedTauIdJetsCollinear")
#    metBase = plots.DataMCPlot(datasets, "BaseLine/MET_BaseLineTauIdBveto")
#    metInver = plots.DataMCPlot(datasets, "Inverted/MET_InvertedTauIdBveto") 

    # Rebin before subtracting
    metBase.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))
    metInver.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))
    
#    metInverted_data = metInver.histoMgr.getHisto("Data").getRootHisto().Clone("Inverted/MET_InvertedTauIdBveto")
#    metInverted_EWK = metInver.histoMgr.getHisto("EWK").getRootHisto().Clone("Inverted/MET_InvertedTauIdBveto") 
#    metBase_data = metBase.histoMgr.getHisto("Data").getRootHisto().Clone("BaseLine/MET_BaselineTauIdBveto")
#    metBase_EWK = metBase.histoMgr.getHisto("EWK").getRootHisto().Clone("BaseLine/MET_BaselineTauIdBveto")

    metInverted_data = metInver.histoMgr.getHisto("Data").getRootHisto().Clone("Inverted/MET_InvertedTauIdBvetoCollinear")
    metInverted_EWK = metInver.histoMgr.getHisto("EWK").getRootHisto().Clone("Inverted/MET_InvertedTauIdBvetoCollinear") 
    metBase_data = metBase.histoMgr.getHisto("Data").getRootHisto().Clone("BaseLine/MET_BaselineTauIdBvetoCollinear")
    metBase_EWK = metBase.histoMgr.getHisto("EWK").getRootHisto().Clone("BaseLine/MET_BaselineTauIdBvetoCollinear")
#    metInverted_data = metInver.histoMgr.getHisto("Data").getRootHisto().Clone("Inverted/MET_InvertedTauIdJetsCollinear")
#    metInverted_EWK = metInver.histoMgr.getHisto("EWK").getRootHisto().Clone("Inverted/MET_InvertedTauIdJetsCollinear") 
#    metBase_data = metBase.histoMgr.getHisto("Data").getRootHisto().Clone("BaseLine/MET_BaselineTauIdJetsCollinear")
#    metBase_EWK = metBase.histoMgr.getHisto("EWK").getRootHisto().Clone("BaseLine/MET_BaselineTauIdJetsCollinear")


    metBase_data.SetTitle("Data: BaseLine TauID")
    metInverted_data.SetTitle("Data: Inverted TauID")
    metBase_QCD = metBase_data.Clone("QCD")
    metBase_QCD.Add(metBase_EWK,-1)
    metBase_QCD.SetTitle("Data - EWK MC: BaseLine TauID")

    metInverted_data.GetXaxis().SetTitle("PFMET (GeV)")

    invertedQCD.setLabel("BaseVsInverted")
#    invertedQCD.comparison(metInverted_data,metBase_data)
    invertedQCD.setLabel("BaseMinusEWKVsInverted")
#    invertedQCD.comparison(metInverted_data,metBase_QCD)

    invertedQCD.cutefficiency(metInverted_data,metBase_QCD)

if __name__ == "__main__":
    main()
