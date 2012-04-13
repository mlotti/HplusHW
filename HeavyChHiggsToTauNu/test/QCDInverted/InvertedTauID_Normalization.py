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

def usage():
    print "\n"
    print "### Usage:   InvertedTauID_Normalization.py <multicrab dir>\n"
    print "\n"
    sys.exit()

def main(argv):

#    HISTONAME = "TauIdJets"
    HISTONAME = "TauIdBtag"

    dirs = []
    if len(sys.argv) < 2:
	usage()

    dirs.append(sys.argv[1])
    
    # Create all datasets from a multicrab task
#    datasets = dataset.getDatasetsFromMulticrabCfg(counters=counters)
    datasets = dataset.getDatasetsFromMulticrabDirs(dirs,counters=counters)

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



    bins = ["inclusive"]
#    bins = ["4050","5060","6070","7080","80100","100120","120150","150"]
#    bins = ["4050"]


    for bin in bins:

	invertedQCD.setLabel(bin)

	if bin == "inclusive":
	    bin = ""

        metBase = plots.DataMCPlot(datasets, analysis+"/MET_BaseLine"+HISTONAME+bin)
        metInver = plots.DataMCPlot(datasets, analysis+"/MET_Inverted"+HISTONAME+bin)
        # Rebin before subtracting
        metBase.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        metInver.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))

        metInverted_data = metInver.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_Inverted"+HISTONAME+bin)
        metInverted_EWK = metInver.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MET_Inverted"+HISTONAME+bin)
        metBase_data = metBase.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_Baseline"+HISTONAME+bin)
        metBase_EWK = metBase.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MET_Baseline"+HISTONAME+bin)

        metBase_QCD = metBase_data.Clone("QCD")
        metBase_QCD.Add(metBase_EWK,-1)

        invertedQCD.plotHisto(metInverted_data,"inverted")
        invertedQCD.plotHisto(metBase_data,"baseline")
        invertedQCD.fitQCD(metInverted_data)
        invertedQCD.fitEWK(metBase_EWK,"LR")
        invertedQCD.fitData(metBase_data)
        invertedQCD.getNormalization()

    invertedQCD.Summary()
    invertedQCD.WriteNormalizationToFile("QCDInvertedNormalizationFactors.py")


if __name__ == "__main__":
    main(sys.argv)
