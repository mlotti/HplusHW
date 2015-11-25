#!/usr/bin/env python

###########################################################################
#
# This script calculates the normalization factors from QCDMeasurementAnalysis
#
###########################################################################

import ROOT
ROOT.gROOT.SetBatch(True)
import math
import sys

import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
#import HiggsAnalysis.NtupleAnalysis.tools.styles as styles
#import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.crosssection as xsect
import HiggsAnalysis.NtupleAnalysis.tools.multicrabConsistencyCheck as consistencyCheck
import HiggsAnalysis.NtupleAnalysis.QCDMeasurement.QCDNormalization as QCDNormalization


#==== Set analysis, data era, and search mode
analysis = "QCDMeasurement"

#dataEra = "Run2015C"
#dataEra = "Run2015D"
#dataEra = "Run2015CD"
dataEra = "Run2015"

searchMode = "80to1000"
print analysis, dataEra, searchMode



def usage():
    print "\n"
    print "### Usage:   InvertedTauID_Normalization.py_QCDandFakeTausFromData <multicrab dir>\n"
    print "\n"
    sys.exit()

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
            "DYJetsToLLHT",
            "SingleTop",
            #"Diboson"
            ])

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    style.setOptStat(True)
    
    for HISTONAME in comparisonList:
        BASELINETAUHISTONAME = "NormalizationMETBaselineTau"+HISTONAME+"/NormalizationMETBaselineTau"+HISTONAME
        INVERTEDTAUHISTONAME = "NormalizationMETInvertedTau"+HISTONAME+"/NormalizationMETInvertedTau"+HISTONAME
        FITMIN = None
        FITMAX = None
      
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
                hDummy = dsetMgr.getDataset("Data").getDatasetRootHisto(COMBINEDHISTODIR+"/"+BASELINETAUHISTONAME+"/"+hname).getHistogram()
                title = hDummy.GetTitle()
                title = title.replace("METBaseline"+HISTONAME,"")
                binLabels.append(QCDNormalization.getModifiedBinLabelString(title))
                if FITMIN == None:
                    FITMIN = hDummy.GetXaxis().GetXmin()
                    FITMAX = hDummy.GetXaxis().GetXmax()
                hDummy.Delete()
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
        manager = QCDNormalization.QCDNormalizationManager(binLabels)
        
        #===== Create templates
        template_EWKFakeTaus_Baseline = manager.createTemplate("EWKFakeTaus_Baseline")
        template_EWKFakeTaus_Inverted = manager.createTemplate("EWKFakeTaus_Inverted")
        template_EWKGenuineTaus_Baseline = manager.createTemplate("EWKGenuineTaus_Baseline")
        template_EWKGenuineTaus_Inverted = manager.createTemplate("EWKGenuineTaus_Inverted")
        template_QCD_Baseline = manager.createTemplate("QCD_Baseline")
        template_QCD_Inverted = manager.createTemplate("QCD_Inverted")
        template_Data_Baseline = manager.createTemplate("Data_Baseline")
        
        #===== Define fit functions and fit parameters
        # The available functions are defined in the FitFunction class in the QCDMeasurement/python/QCDNormalization.py file
        boundary = 100
        template_EWKFakeTaus_Baseline.setFitter(QCDNormalization.FitFunction("EWKFunctionInv", boundary=boundary, norm=1, rejectPoints=1),
                                                FITMIN, FITMAX)
        template_EWKFakeTaus_Baseline.setDefaultFitParam(defaultLowerLimit=[0.5,  90,  30, 0.0001],
                                                         defaultUpperLimit=[ 30, 200, 100,    1.0])
        boundary = 150
        template_EWKGenuineTaus_Baseline.setFitter(QCDNormalization.FitFunction("EWKFunction", boundary=boundary, norm=1, rejectPoints),
                                                   FITMIN, FITMAX)
        template_EWKGenuineTaus_Baseline.setDefaultFitParam(defaultLowerLimit=[0.5,  90, 30, 0.0001],
                                                            defaultUpperLimit=[ 20, 120, 50,    1.0])
        # Note that the same function is used for QCD only and QCD+EWK fakes
        template_QCD_Inverted.setFitter(QCDNormalization.FitFunction("QCDFunction", norm=1), FITMIN, FITMAX)
        template_QCD_Inverted.setDefaultFitParam(defaultLowerLimit=[0.0001, 0.001, 0.1, 0.0,  10, 0.0001, 0.001],
                                                 defaultUpperLimit=[   200,    10,  10, 150, 100,      1, 0.05])
        


        #invertedQCD = InvertedTauID()
        #invertedQCD.setLumi(dsetMgr.getDataset("Data").getLuminosity())
        #invertedQCD.setInfo([dataEra,searchMode,HISTONAME])
        
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
            metInverted_EWK_GenuineTaus = metInver_GenuineTaus.histoMgr.getHisto("EWK").getRootHisto().Clone(GENUINEHISTODIR+"/"+INVERTEDTAUHISTONAME+binStr)
            metInverted_EWK_FakeTaus = metInver_FakeTaus.histoMgr.getHisto("EWK").getRootHisto().Clone(FAKEHISTODIR+"/"+INVERTEDTAUHISTONAME+binStr)
            
            metBase_data = metBase.histoMgr.getHisto("Data").getRootHisto().Clone(COMBINEDHISTODIR+"/"+BASELINETAUHISTONAME+binStr)
            metBase_EWK_GenuineTaus = metBase_GenuineTaus.histoMgr.getHisto("EWK").getRootHisto().Clone(GENUINEHISTODIR+"/"+BASELINETAUHISTONAME+binStr)
            metBase_EWK_FakeTaus = metBase_FakeTaus.histoMgr.getHisto("EWK").getRootHisto().Clone(FAKEHISTODIR+"/"+BASELINETAUHISTONAME+binStr)

            #===== Obtain templates for QCD (subtract MC EWK events from data)
            # QCD from baseline is usable only as a cross check
            #metBase_QCD = metBase_data.Clone("QCD")
            #metBase_QCD.Add(metBase_EWK_GenuineTaus,-1)
            #metBase_QCD.Add(metBase_EWK_FakeTaus,-1)
            #addLabels(metBase_QCD, "QCD, baseline")
            
            metInverted_QCD = metInverted_data.Clone("QCD")
            metInverted_QCD.Add(metInverted_EWK_GenuineTaus,-1)
            metInverted_QCD.Add(metInverted_EWK_FakeTaus,-1)
            
            
            
            
            
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
            fitOptions = "R B" # RBL
            
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


if __name__ == "__main__":
    main(sys.argv)
