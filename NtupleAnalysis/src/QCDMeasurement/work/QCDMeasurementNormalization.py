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
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.crosssection as xsect
import HiggsAnalysis.NtupleAnalysis.tools.multicrabConsistencyCheck as consistencyCheck
import HiggsAnalysis.QCDMeasurement.QCDNormalization as QCDNormalization


#==== Set analysis, data era, and search mode
analysis = "QCDMeasurement"

#dataEra = "Run2015C"
#dataEra = "Run2015D"
#dataEra = "Run2015CD"
dataEra = "Run2015"

searchMode = "80to1000"
print analysis, dataEra, searchMode

selectOnlyBins = [] #["1"]

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
                binIndex = hname.replace("NormalizationMETBaselineTau"+HISTONAME,"")
                bins.append(binIndex)
                hDummy = dsetMgr.getDataset("Data").getDatasetRootHisto(COMBINEDHISTODIR+"/"+BASELINETAUHISTONAME+binIndex).getHistogram()
                title = hDummy.GetTitle()
                title = title.replace("METBaseline"+HISTONAME,"")
                if binIndex == "Inclusive":
                    binLabels.append(binIndex)
                else:
                    binLabels.append(QCDNormalization.getModifiedBinLabelString(title))
                if FITMIN == None:
                    FITMIN = hDummy.GetXaxis().GetXmin()
                    FITMAX = hDummy.GetXaxis().GetXmax()
                hDummy.Delete()
        print "\nHistogram bins available",bins
        # Select bins by filter
        if len(selectOnlyBins) > 0:
            oldBinLabels = binLabels[:]
            oldBins = bins[:]
            binLabels = []
            bins = []
            for k in selectOnlyBins:
                for i in range(len(oldBinLabels)):
                    if k == oldBinLabels[i] or k == oldBins[i]:
                        binLabels.append(oldBinLabels[i])
                        bins.append(oldBins[i])
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
        
        #===== Create templates (EWK fakes, EWK genuine, QCD; data template is created by manager)
        template_EWKFakeTaus_Baseline = manager.createTemplate("EWKFakeTaus_Baseline")
        template_EWKFakeTaus_Inverted = manager.createTemplate("EWKFakeTaus_Inverted")
        template_EWKGenuineTaus_Baseline = manager.createTemplate("EWKGenuineTaus_Baseline")
        template_EWKGenuineTaus_Inverted = manager.createTemplate("EWKGenuineTaus_Inverted")
        template_QCD_Baseline = manager.createTemplate("QCD_Baseline")
        template_QCD_Inverted = manager.createTemplate("QCD_Inverted")
        manager.setSources(ewkFakeTausSrc="EWKFakeTaus_Baseline", ewkGenuineTausSrc="EWKGenuineTaus_Baseline", qcdSrc="QCD_Inverted")
        
        #===== Define fit functions and fit parameters
        # The available functions are defined in the FitFunction class in the QCDMeasurement/python/QCDNormalization.py file
        boundary = 100
        template_EWKFakeTaus_Baseline.setFitter(QCDNormalization.FitFunction("EWKFunctionInv", boundary=boundary, norm=1, rejectPoints=1),
                                                FITMIN, FITMAX)
        template_EWKFakeTaus_Baseline.setDefaultFitParam(defaultLowerLimit=[0.5,  90,  30, 0.0001],
                                                         defaultUpperLimit=[ 30, 200, 100,    1.0])
        boundary = 150
        template_EWKGenuineTaus_Baseline.setFitter(QCDNormalization.FitFunction("EWKFunction", boundary=boundary, norm=1, rejectPoints=1),
                                                   FITMIN, FITMAX)
        template_EWKGenuineTaus_Baseline.setDefaultFitParam(defaultLowerLimit=[0.5,  90, 30, 0.0001],
                                                            defaultUpperLimit=[ 20, 120, 50,    1.0])
        # Note that the same function is used for QCD only and QCD+EWK fakes
        template_QCD_Inverted.setFitter(QCDNormalization.FitFunction("QCDFunction", norm=1), FITMIN, FITMAX)
        template_QCD_Inverted.setDefaultFitParam(defaultLowerLimit=[0.0001, 0.001, 0.1, 0.0,  10, 0.0001, 0.001],
                                                 defaultUpperLimit=[   200,    10,  10, 150, 100,      1, 0.05])
        
        #===== Loop over tau pT bins
        for i,binStr in enumerate(bins):
            print "\n********************************"
            print "*** Fitting bin %s"%binLabels[i]
            print "********************************\n"

            #===== Reset bin results
            manager.resetBinResults()

            #===== Obtain histograms for normalization
            # Data
            histoName = COMBINEDHISTODIR+"/"+BASELINETAUHISTONAME+binStr
            hmetBase_data = plots.DataMCPlot(dsetMgr, histoName).histoMgr.getHisto("Data").getRootHisto().Clone(histoName)
            histoName = COMBINEDHISTODIR+"/"+INVERTEDTAUHISTONAME+binStr
            hmetInverted_data = plots.DataMCPlot(dsetMgr, histoName).histoMgr.getHisto("Data").getRootHisto().Clone(histoName)

            # EWK genuine taus
            histoName = GENUINEHISTODIR+"/"+BASELINETAUHISTONAME+binStr
            hmetBase_EWK_GenuineTaus = plots.DataMCPlot(dsetMgr, histoName).histoMgr.getHisto("EWK").getRootHisto().Clone(histoName)
            histoName = GENUINEHISTODIR+"/"+INVERTEDTAUHISTONAME+binStr
            hmetInverted_EWK_GenuineTaus = plots.DataMCPlot(dsetMgr, histoName).histoMgr.getHisto("EWK").getRootHisto().Clone(histoName)

            # EWK fake taus
            histoName = FAKEHISTODIR+"/"+BASELINETAUHISTONAME+binStr
            hmetBase_EWK_FakeTaus = plots.DataMCPlot(dsetMgr, histoName).histoMgr.getHisto("EWK").getRootHisto().Clone(histoName)
            histoName = FAKEHISTODIR+"/"+INVERTEDTAUHISTONAME+binStr
            hmetInverted_EWK_FakeTaus = plots.DataMCPlot(dsetMgr, histoName).histoMgr.getHisto("EWK").getRootHisto().Clone(histoName)

            # Finalize histograms by rebinning
            rebinFactor = 2 # Aim for 10 GeV binning
            for histogram in [hmetBase_data, hmetInverted_data, hmetBase_EWK_GenuineTaus, hmetInverted_EWK_GenuineTaus, hmetBase_EWK_FakeTaus, hmetInverted_EWK_FakeTaus]:
                 histogram.Rebin(rebinFactor)
            
            #===== Obtain histograms for QCD (subtract MC EWK events from data)
            # QCD from baseline is usable only as a cross check
            hmetBase_QCD = hmetBase_data.Clone("QCD")
            hmetBase_QCD.Add(hmetBase_EWK_GenuineTaus,-1)
            hmetBase_QCD.Add(hmetBase_EWK_FakeTaus,-1)
            
            hmetInverted_QCD = hmetInverted_data.Clone("QCD")
            hmetInverted_QCD.Add(hmetInverted_EWK_GenuineTaus,-1)
            hmetInverted_QCD.Add(hmetInverted_EWK_FakeTaus,-1)
            
            #===== Set histograms to the templates
            template_EWKFakeTaus_Inverted.setHistogram(hmetInverted_EWK_FakeTaus, binLabels[i])
            template_EWKGenuineTaus_Inverted.setHistogram(hmetInverted_EWK_GenuineTaus, binLabels[i])
            template_QCD_Inverted.setHistogram(hmetInverted_QCD, binLabels[i])
            
            template_EWKFakeTaus_Baseline.setHistogram(hmetBase_EWK_FakeTaus, binLabels[i])
            template_EWKGenuineTaus_Baseline.setHistogram(hmetBase_EWK_GenuineTaus, binLabels[i])
            template_QCD_Baseline.setHistogram(hmetBase_QCD, binLabels[i])
            
            #===== Make plots of templates
            manager.plotTemplates()
            
            #===== Fit individual templates to data
            fitOptions = "R B" # RBL
            manager.fitDataWithQCDAndFakesAndGenuineTaus(hmetBase_data, fitOptions, FITMIN, FITMAX)
            
            

            #===== Calculate normalization
            #invertedQCD.getNormalization()
        
        manager.writeScaleFactorFile("QCDInvertedNormalizationFactorsFilteredEWKFakeTaus.py", analysis, dataEra, searchMode)
        #invertedQCD.Summary()
        #invertedQCD.WriteNormalizationToFile("QCDInvertedNormalizationFactorsFilteredEWKFakeTaus.py")
        #invertedQCD.WriteLatexOutput("fits.tex")


if __name__ == "__main__":
    main(sys.argv)
