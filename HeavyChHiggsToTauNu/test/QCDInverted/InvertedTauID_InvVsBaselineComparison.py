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
import array  

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect

from InvertedTauID import *

ReBinning = True

def main():
    if len(sys.argv) < 2:
        usage()

    dirs = []
    dirs.append(sys.argv[1])
    
    # Create all datasets from a multicrab task
    datasets = dataset.getDatasetsFromMulticrabDirs(dirs,counters=counters) 
#    datasets = dataset.getDatasetsFromMulticrabCfg(counters=counters)

    # As we use weighted counters for MC normalisation, we have to
    # update the all event count to a separately defined value because
    # the analysis job uses skimmed pattuple as an input
    datasets.updateNAllEventsToPUWeighted()

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

    metBase = plots.DataMCPlot(datasets, analysis+"/MET_BaseLineTauIdBtag")
    metInver = plots.DataMCPlot(datasets, analysis+"/MET_InvertedTauIdBtag")

    # Rebin before subtracting
    metBase.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
    metInver.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
    
    metInverted_data = metInver.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdBtag")
    metInverted_EWK = metInver.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MET_InvertedTauIdBtag") 
    metBase_data = metBase.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_BaselineTauIdBtag")
    metBase_EWK = metBase.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MET_BaselineTauIdBtag")

    if ReBinning:
        rebinfactor = 1.3
        histobins = []
        histobins.append(0)
        histobins.append(1)
        i = 1
        while histobins[len(histobins)-1] < 400:
            edge = histobins[i] + (histobins[i]-histobins[i-1])*rebinfactor
            histobins.append(edge)
            i += 1
            print histobins
            
        metBase_data = metBase_data.Rebin(len(histobins)-1,"",array.array("d", histobins))
        metInverted_data = metInverted_data.Rebin(len(histobins)-1,"",array.array("d", histobins))
        metBase_EWK = metBase_EWK.Rebin(len(histobins)-1,"",array.array("d", histobins))
        metInverted_EWK = metInverted_EWK.Rebin(len(histobins)-1,"",array.array("d", histobins))
    
 

    metBase_data.SetTitle("Data: BaseLine TauID")
    metInverted_data.SetTitle("Data: Inverted TauID")
    metBase_QCD = metBase_data.Clone("QCD")
    metBase_QCD.Add(metBase_EWK,-1)
    metBase_QCD.SetTitle("Data - EWK MC: BaseLine TauID")

    invertedQCD.setLabel("BaseVsInverted")
    invertedQCD.comparison(metInverted_data,metBase_data)
    invertedQCD.setLabel("BaseMinusEWKVsInverted")
    invertedQCD.comparison(metInverted_data,metBase_QCD)

    invertedQCD.cutefficiency(metInverted_data,metBase_QCD)

if __name__ == "__main__":
    main()
