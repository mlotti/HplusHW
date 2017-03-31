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

from InvertedTauIDWithFakeTaus import *
print analysis
#dataEra = "Run2015C"
#dataEra = "Run2015D"
#dataEra = "Run2015CD"
dataEra = "Run2015"

searchMode = "80to1000"

def usage():
    print "\n"
    print "### Usage:   InvertedTauID_Normalization.py_QCDandFakeTausFromData <multicrab dir>\n"
    print "\n"
    sys.exit()

def formatHistoTitle(title):
    t = title.replace("#tau p_{T}","taup_T")
    t = t.replace("#tau eta","taueta")
    t = t.replace("<","lt")
    t = t.replace(">","gt")
    t = t.replace("=","eq")
    t = t.replace("..","to")
    t = t.replace(".","p")
    t = t.replace("/","_")
    return t

def main(argv):
    COMBINEDHISTODIR = "ForQCDNormalization"
    FAKEHISTODIR = "ForQCDNormalizationEWKFakeTaus"
    GENUINEHISTODIR = "ForQCDNormalizationEWKGenuineTaus"
    comparisonList = ["AfterStdSelections"]

    dirs = []
    if len(sys.argv) < 2:
	usage()

    dirs.append(sys.argv[1])
    
    # Create all dsetMgr from a multicrab task
    dsetMgr = dataset.getDatasetsFromMulticrabDirs(dirs,dataEra=dataEra,  searchMode=searchMode, analysisName=analysis)

    #print dsetMgr
    # Check multicrab consistency
    consistencyCheck.checkConsistencyStandalone(dirs[0],dsetMgr,name="QCD inverted")
   
    # As we use weighted counters for MC normalisation, we have to
    # update the all event count to a separately defined value because
    # the analysis job uses skimmed pattuple as an input
    dsetMgr.updateNAllEventsToPUWeighted()

    # Read integrated luminosities of data dsetMgr from lumi.json
    dsetMgr.loadLuminosities()

    # Include only 120 mass bin of HW and HH dsetMgr
    dsetMgr.remove(filter(lambda name: "TTToHplus" in name and not "M120" in name, dsetMgr.getAllDatasetNames()))
    dsetMgr.remove(filter(lambda name: "HplusTB" in name, dsetMgr.getAllDatasetNames()))
    # Default merging nad ordering of data and MC dsetMgr
    # All data dsetMgr to "Data"
    # All QCD dsetMgr to "QCD"
    # All single top dsetMgr to "SingleTop"
    # WW, WZ, ZZ to "Diboson"
    plots.mergeRenameReorderForDataMC(dsetMgr)

    # Set BR(t->H) to 0.05, keep BR(H->tau) in 1
    xsect.setHplusCrossSectionsToBR(dsetMgr, br_tH=0.05, br_Htaunu=1)

    # Merge WH and HH dsetMgr to one (for each mass bin)
    plots.mergeWHandHH(dsetMgr)

    dsetMgr.merge("EWK", [
	    "TTJets",
            "WJetsHT",
            "DYJetsToLL",
            "SingleTop",
            #"Diboson"
            ])

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    style.setOptStat(True)

    for HISTONAME in comparisonList:
        BASELINETAUHISTONAME = "NormalizationMETBaselineTau"+HISTONAME+"/NormalizationMETBaselineTau"+HISTONAME
        INVERTEDTAUHISTONAME = "NormalizationMETInvertedTau"+HISTONAME+"/NormalizationMETInvertedTau"+HISTONAME
      
        #===== Infer binning information and labels
        histonames = dsetMgr.getDataset("Data").getDirectoryContent(COMBINEDHISTODIR+"/NormalizationMETBaselineTau"+HISTONAME)
        bins = []
        binLabels = []
        if histonames == None:
            # Assume that only inclusive bin exists
            name = COMBINEDHISTODIR+"/NormalizationMETBaselineTau"+HISTONAME
            if not dsetMgr.getDataset("Data").hasRootHisto(name):
                raise Exception("Error: Cannot find histogram or directory of name '%s'!"%name)
            BASELINETAUHISTONAME = "NormalizationMETBaselineTau"+HISTONAME
            INVERTEDTAUHISTONAME = "NormalizationMETInvertedTau"+HISTONAME
            bins = [""]
            binLabels = ["Inclusive"]
        else:
            for hname in histonames:
                bins.append(hname.replace("NormalizationMETBaselineTau"+HISTONAME,""))
                title = dsetMgr.getDataset("Data").getDatasetRootHisto(COMBINEDHISTODIR+"/"+BASELINETAUHISTONAME+"/"+hname).getHistogram().GetTitle()
                title = title.replace("METBaseline"+HISTONAME,"")
                binLabels.append(formatHistoTitle(title))
        
        print "\nHistogram bins available",bins
        print "Using bins              ",bins
        print "\nBin labels"
        for i in range(len(binLabels)):
            line = bins[i]
            while len(line) < 10:
                line += " "
            line += ": "+binLabels[i]
            print line
        print
        
        #===== Initialize normalization calculator
        invertedQCD = InvertedTauID()
        invertedQCD.setLumi(dsetMgr.getDataset("Data").getLuminosity())
        invertedQCD.setInfo([dataEra,searchMode,HISTONAME])
        
        #===== Loop over tau pT bins
        for i,binStr in enumerate(bins):
            print "\n********************************"
            print "*** Fitting bin %s"%binLabels[i]
            print "********************************\n"
            invertedQCD.resetBinResults()
            invertedQCD.setLabel(binLabels[i])

            #===== Obtain histograms for normalization
            metBase = plots.DataMCPlot(dsetMgr, COMBINEDHISTODIR+"/"+BASELINETAUHISTONAME+binStr)
            metInver = plots.DataMCPlot(dsetMgr, COMBINEDHISTODIR+"/"+INVERTEDTAUHISTONAME+binStr)
            metBase_GenuineTaus = plots.DataMCPlot(dsetMgr, GENUINEHISTODIR+"/"+BASELINETAUHISTONAME+binStr)
            metInver_GenuineTaus = plots.DataMCPlot(dsetMgr, GENUINEHISTODIR+"/"+INVERTEDTAUHISTONAME+binStr)
            metBase_FakeTaus = plots.DataMCPlot(dsetMgr, FAKEHISTODIR+"/"+BASELINETAUHISTONAME+binStr)
            metInver_FakeTaus = plots.DataMCPlot(dsetMgr, FAKEHISTODIR+"/"+INVERTEDTAUHISTONAME+binStr)

            #===== Rebin histograms before subtracting
            RebinFactor = 2 # Aim for 10 GeV binning
            metBase.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(RebinFactor))
            metInver.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(RebinFactor))
            metBase_GenuineTaus.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(RebinFactor))
            metInver_GenuineTaus.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(RebinFactor))
            metBase_FakeTaus.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(RebinFactor))
            metInver_FakeTaus.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(RebinFactor))
            
            #===== Obtain templates for data and EWK
            metInverted_data = metInver.histoMgr.getHisto("Data").getRootHisto().Clone(COMBINEDHISTODIR+"/"+INVERTEDTAUHISTONAME+binStr)
            treatHistogram(metInverted_data, "Data, inverted")
            metInverted_EWK_GenuineTaus = metInver_GenuineTaus.histoMgr.getHisto("EWK").getRootHisto().Clone(GENUINEHISTODIR+"/"+INVERTEDTAUHISTONAME+binStr)
            treatHistogram(metInverted_EWK_GenuineTaus, "EWK genuine taus, inverted")
            metInverted_EWK_FakeTaus = metInver_FakeTaus.histoMgr.getHisto("EWK").getRootHisto().Clone(FAKEHISTODIR+"/"+INVERTEDTAUHISTONAME+binStr)
            treatHistogram(metInverted_EWK_FakeTaus, "EWK fake taus, inverted")
            
            metBase_data = metBase.histoMgr.getHisto("Data").getRootHisto().Clone(COMBINEDHISTODIR+"/"+BASELINETAUHISTONAME+binStr)
            treatHistogram(metBase_data, "Data, baseline")
            metBase_EWK_GenuineTaus = metBase_GenuineTaus.histoMgr.getHisto("EWK").getRootHisto().Clone(GENUINEHISTODIR+"/"+BASELINETAUHISTONAME+binStr)
            treatHistogram(metBase_EWK_GenuineTaus, "EWK genuine taus, baseline")
            metBase_EWK_FakeTaus = metBase_FakeTaus.histoMgr.getHisto("EWK").getRootHisto().Clone(FAKEHISTODIR+"/"+BASELINETAUHISTONAME+binStr)
            treatHistogram(metBase_EWK_FakeTaus, "EWK fake taus, baseline")

            #===== Obtain templates for QCD (subtract MC EWK events from data)
            # QCD from baseline is usable only as a cross check
            #metBase_QCD = metBase_data.Clone("QCD")
            #metBase_QCD.Add(metBase_EWK_GenuineTaus,-1)
            #metBase_QCD.Add(metBase_EWK_FakeTaus,-1)
            #addLabels(metBase_QCD, "QCD, baseline")
            
            metInverted_QCD = metInverted_data.Clone("QCD")
            metInverted_QCD.Add(metInverted_EWK_GenuineTaus,-1)
            metInverted_QCD.Add(metInverted_EWK_FakeTaus,-1)
            treatHistogram(metInverted_QCD, "QCD, inverted")
            
            #===== Make plots of templates
            print "\n*** Integrals of plotted templates"
            #invertedQCD.plotHisto(metInverted_data,"template_Data_Inverted")
            #invertedQCD.plotHisto(metInverted_EWK_GenuineTaus,"template_EWKGenuineTaus_Inverted")
            #invertedQCD.plotHisto(metInverted_EWK_FakeTaus,"template_EWKFakeTaus_Inverted")
            invertedQCD.plotHisto(metInverted_QCD,"template_QCD_Inverted")
            invertedQCD.plotHisto(metBase_data,"template_Data_Baseline")
            invertedQCD.plotHisto(metBase_EWK_GenuineTaus,"template_EWKGenuineTaus_Baseline")
            invertedQCD.plotHisto(metBase_EWK_FakeTaus,"template_EWKFakeTaus_Baseline")
            #invertedQCD.plotHisto(metBase_QCD,"template_QCD_Baseline")
            
            #===== Fit individual templates and
            # Fit first templates for QCD, EWK_genuine_taus, and EWK_fake_taus
            # Then fit the shape of those parametrizations to baseline data to obtain normalization coefficients
            fitOptions = "RB"
            
            # Strategy: take EWK templates from baseline and QCD template from inverted; then fit to baseline data
            invertedQCD.fitEWK_GenuineTaus(metInverted_EWK_GenuineTaus,fitOptions)
            invertedQCD.fitEWK_GenuineTaus(metBase_EWK_GenuineTaus,fitOptions)
            invertedQCD.fitEWK_FakeTaus(metInverted_EWK_FakeTaus,fitOptions)
            invertedQCD.fitEWK_FakeTaus(metBase_EWK_FakeTaus,fitOptions)
            invertedQCD.fitQCD(metInverted_QCD,fitOptions)
            invertedQCD.fitData(metBase_data)

            #===== Calculate normalization
            invertedQCD.getNormalization()
            
        invertedQCD.Summary()
        invertedQCD.WriteNormalizationToFile("QCDInvertedNormalizationFactorsFilteredEWKFakeTaus.py")
        invertedQCD.WriteLatexOutput("fits.tex")

def treatHistogram(histo, histoname):
    histo.SetTitle(histoname)
    binwidth = int(histo.GetXaxis().GetBinWidth(1))
    histo.GetXaxis().SetTitle("Type1 PFMET (GeV)")
    histo.GetYaxis().SetTitle("Events / %i GeV"%binwidth)
    histo.GetYaxis().SetTitleOffset(1.5)
    # Set negative bins to zero, but keep bin error like it is for fitting
    for k in range(0, histo.GetNbinsX()+2):
        if histo.GetBinContent(k) < 0.0:
            print "Histogram '%s': Setting negative bin %d content to zero (was %f)"%(histoname, k, histo.GetBinContent(k))
            histo.SetBinContent(k, 0.0)
            

if __name__ == "__main__":
    main(sys.argv)
