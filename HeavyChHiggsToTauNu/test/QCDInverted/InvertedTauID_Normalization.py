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
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrabConsistencyCheck as consistencyCheck

from InvertedTauID import *
#dataEra = "Run2011A"
#dataEra = "Run2011B"
dataEra = "Run2011AB"


searchMode = "Light"
#searchMode = "Heavy"

def usage():
    print "\n"
    print "### Usage:   InvertedTauID_Normalization.py <multicrab dir>\n"
    print "\n"
    sys.exit()

def main(argv):

#    HISTONAME = "TauIdJets"
#    HISTONAME = "TauIdJetsCollinear"
#    HISTONAME = "TauIdBtag"
#    HISTONAME = "TauIdBvetoCollinear"
#    HISTONAME = "TauIdBveto"
    HISTONAME = "TauIdAfterCollinearCuts"
   
    dirs = []
    if len(sys.argv) < 2:
	usage()

    dirs.append(sys.argv[1])



    
    # Create all datasets from a multicrab task
    # datasets = dataset.getDatasetsFromMulticrabCfg(counters=counters, dataEra=dataEra, analysisBaseName="signalAnalysisInvertedTau")
    #datasets = dataset.getDatasetsFromMulticrabDirs(dirs,counters=counters, dataEra=dataEra, analysisBaseName="signalAnalysisInvertedTau")
    datasets = dataset.getDatasetsFromMulticrabDirs(dirs,dataEra=dataEra,  searchMode=searchMode, analysisName=analysis)
#    datasets = dataset.getDatasetsFromMulticrabDirs(dirs,counters=counters, dataEra=dataEra)
   
    # Check multicrab consistency
    consistencyCheck.checkConsistencyStandalone(dirs[0],datasets,name="QCD inverted")

    # As we use weighted counters for MC normalisation, we have to
    # update the all event count to a separately defined value because
    # the analysis job uses skimmed pattuple as an input
    datasets.updateNAllEventsToPUWeighted()

    # Read integrated luminosities of data datasets from lumi.json
    datasets.loadLuminosities()

    # Include only 120 mass bin of HW and HH datasets
    datasets.remove(filter(lambda name: "TTToHplus" in name and not "M120" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "HplusTB" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "Hplus_taunu_t-channel" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "Hplus_taunu_tW-channel" in name, datasets.getAllDatasetNames()))
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
    invertedQCD.setInfo([dataEra,searchMode,HISTONAME])

    histonames = datasets.getDataset("Data").getDirectoryContent("baseline/METBaseline"+HISTONAME)
    bins = []
    binLabels = []
    for histoname in histonames:
        bins.append(histoname.replace("METBaseline"+HISTONAME,""))
        title = datasets.getDataset("Data").getDatasetRootHisto("baseline/METBaseline"+HISTONAME+"/"+histoname).getHistogram().GetTitle()
        title = title.replace("METBaseline"+HISTONAME,"")
        title = title.replace("#tau p_{T}","taup_T")
        title = title.replace("<","lt")
        title = title.replace(">","gt")
        title = title.replace("=","eq")
        title = title.replace("..","to")
        binLabels.append(title)
        
    print
    print "Histogram bins available",bins

#    bins = ["Inclusive"]
#    bins = ["taup_Tleq50","taup_Teq50to60"]
    print "Using bins              ",bins
    print
    print "Bin labels"
    for i in range(len(binLabels)):
        line = bins[i]
        while len(line) < 10:
            line += " "
        line += ": "+binLabels[i]
        print line
    print

    for i,bin in enumerate(bins):

	invertedQCD.setLabel(binLabels[i])

        metBase = plots.DataMCPlot(datasets, "baseline/METBaseline"+HISTONAME+"/METBaseline"+HISTONAME+bin)
        metInver = plots.DataMCPlot(datasets, "Inverted/METInverted"+HISTONAME+"/METInverted"+HISTONAME+bin)
        # Rebin before subtracting
        metBase.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))
        metInver.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))
        
        metInverted_data = metInver.histoMgr.getHisto("Data").getRootHisto().Clone("Inverted/METInverted"+HISTONAME+"/METInverted"+HISTONAME+bin)
        metInverted_EWK = metInver.histoMgr.getHisto("EWK").getRootHisto().Clone("Inverted/METInverted"+HISTONAME+"/METInverted"+HISTONAME+bin)
        metBase_data = metBase.histoMgr.getHisto("Data").getRootHisto().Clone("Baseline/METBaseLine"+HISTONAME+"/METBaseline"+HISTONAME+bin)
        metBase_EWK = metBase.histoMgr.getHisto("EWK").getRootHisto().Clone("Baseline/METBaseLine"+HISTONAME+"/METBaseline"+HISTONAME+bin)

        metBase_QCD = metBase_data.Clone("QCD")
        metBase_QCD.Add(metBase_EWK,-1)

        metInverted_QCD = metInverted_data.Clone("QCD")
        metInverted_QCD.Add(metInverted_EWK,-1)
        
        invertedQCD.plotHisto(metInverted_data,"inverted")
        invertedQCD.plotHisto(metInverted_EWK,"invertedEWK")
        invertedQCD.plotHisto(metBase_data,"baseline")
        invertedQCD.plotHisto(metBase_EWK,"baselineEWK")

        invertedQCD.fitEWK(metInverted_EWK,"LR")
        invertedQCD.fitEWK(metBase_EWK,"LR")
        invertedQCD.fitQCD(metInverted_QCD)
        invertedQCD.fitData(metBase_data)

        invertedQCD.getNormalization()

    invertedQCD.Summary()
    invertedQCD.WriteNormalizationToFile("QCDInvertedNormalizationFactors.py")
    invertedQCD.WriteLatexOutput("fits.tex")

if __name__ == "__main__":
    main(sys.argv)
