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

import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.counter as counter
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.styles as styles
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.crosssection as xsect
import HiggsAnalysis.NtupleAnalysis.tools.multicrabConsistencyCheck as consistencyCheck

from InvertedTauID import *
#dataEra = "Run2015C"
#dataEra = "Run2015D"
#dataEra = "Run2015CD"
dataEra = "Run2015"

searchMode = "80to1000"

def usage():
    print "\n"
    print "### Usage:   InvertedTauID_Normalization_QCDFromData.py <multicrab dir>\n"
    print "\n"
    sys.exit()

def main(argv):
    dirs = []
    if len(sys.argv) < 2:
	usage()

    dirs.append(sys.argv[1])

    comparisonList = ["AfterStdSelections"]
    
    # Create all datasets from a multicrab task
    datasets = dataset.getDatasetsFromMulticrabDirs(dirs,dataEra=dataEra, searchMode=searchMode, analysisName=analysis)
    #print datasets.getDatasetNames()

    #print datasets
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
    #datasets.remove(filter(lambda name: "TTJets_SemiLept" in name, datasets.getAllDatasetNames()))
    #datasets.remove(filter(lambda name: "TTJets_FullLept" in name, datasets.getAllDatasetNames()))
    #datasets.remove(filter(lambda name: "TTJets_Hadronic" in name, datasets.getAllDatasetNames()))
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
    style.setOptStat(True)

    for HISTONAME in comparisonList:
        invertedQCD = InvertedTauID()
        invertedQCD.setLumi(datasets.getDataset("Data").getLuminosity())
        invertedQCD.setInfo([dataEra,searchMode,HISTONAME])

        histonames = datasets.getDataset("Data").getDirectoryContent("ForQCDNormalization/NormalizationMETBaselineTau"+HISTONAME)
        bins = []
        binLabels = []
        for histoname in histonames:
            bins.append(histoname.replace("NormalizationMETBaselineTau"+HISTONAME,""))
            title = datasets.getDataset("Data").getDatasetRootHisto("ForQCDNormalization/NormalizationMETBaselineTau"+HISTONAME+"/"+histoname).getHistogram().GetTitle()
            title = title.replace("METBaseline"+HISTONAME,"")
            title = title.replace("#tau p_{T}","taup_T")
            title = title.replace("#tau eta","taueta")
            title = title.replace("<","lt")
            title = title.replace(">","gt")
            title = title.replace("=","eq")
            title = title.replace("..","to")
            title = title.replace(".","p")
            title = title.replace("/","_")
            binLabels.append(title)
        binLabels = bins # for this data set
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

            metBase = plots.DataMCPlot(datasets, "ForQCDNormalization/NormalizationMETBaselineTau"+HISTONAME+"/NormalizationMETBaselineTau"+HISTONAME+bin)
            metInver = plots.DataMCPlot(datasets, "ForQCDNormalization/NormalizationMETInvertedTau"+HISTONAME+"/NormalizationMETInvertedTau"+HISTONAME+bin)
            # Rebin before subtracting
            RebinFactor = 10
            metBase.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(RebinFactor))
            metInver.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(RebinFactor))

            metInverted_data = metInver.histoMgr.getHisto("Data").getRootHisto().Clone("ForQCDNormalization/NormalizationMETBaselineTau"+HISTONAME+"/NormalizationMETBaselineTau"+HISTONAME+bin)
            metInverted_EWK = metInver.histoMgr.getHisto("EWK").getRootHisto().Clone("ForQCDNormalization/NormalizationMETBaselineTau"+HISTONAME+"/NormalizationMETBaselineTau"+HISTONAME+bin)
            metBase_data = metBase.histoMgr.getHisto("Data").getRootHisto().Clone("ForQCDNormalization/NormalizationMETInvertedTau"+HISTONAME+"/NormalizationMETInvertedTau"+HISTONAME+bin)
            metBase_EWK = metBase.histoMgr.getHisto("EWK").getRootHisto().Clone("ForQCDNormalization/NormalizationMETInvertedTau"+HISTONAME+"/NormalizationMETInvertedTau"+HISTONAME+bin)

            metBase_QCD = metBase_data.Clone("QCD")
            metBase_QCD.Add(metBase_EWK,-1)

            metInverted_QCD = metInverted_data.Clone("QCD")
            metInverted_QCD.Add(metInverted_EWK,-1)

            metInverted_data = addlabels(metInverted_data)
            metInverted_EWK  = addlabels(metInverted_EWK)
            metBase_data     = addlabels(metBase_data)
            metBase_EWK      = addlabels(metBase_EWK)
            metInverted_QCD  = addlabels(metInverted_QCD)

            invertedQCD.plotHisto(metInverted_data,"inverted")
            invertedQCD.plotHisto(metInverted_EWK,"invertedEWK")
            invertedQCD.plotHisto(metBase_data,"baseline")
            invertedQCD.plotHisto(metBase_EWK,"baselineEWK")


            fitOptions = "RB"

            invertedQCD.fitEWK(metInverted_EWK,fitOptions)
            invertedQCD.fitEWK(metBase_EWK,fitOptions)
            invertedQCD.fitQCD(metInverted_QCD,fitOptions)
            invertedQCD.fitData(metBase_data)

            invertedQCD.getNormalization()

        invertedQCD.Summary()
        normalizationFileName = HISTONAME #.replace("TauIdAfterCollinearCuts","")
        if HISTONAME == "TauIdAfterCollinearCutsPlusFilteredEWKFakeTaus":
            normalizationFileName = normalizationFileName.replace("Plus","")
        invertedQCD.WriteNormalizationToFile("QCDInvertedNormalizationFactors" + normalizationFileName + ".py")
        invertedQCD.WriteLatexOutput("fits" + normalizationFileName + ".tex")

def addlabels(histo):
    binwidth = int(histo.GetXaxis().GetBinWidth(1))
    histo.GetXaxis().SetTitle("Type1 PFMET (GeV)")
    histo.GetYaxis().SetTitle("Events / %i GeV"%binwidth)
    histo.GetYaxis().SetTitleOffset(1.5)
    return histo

if __name__ == "__main__":
    main(sys.argv)
