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
import os

import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
#import HiggsAnalysis.NtupleAnalysis.tools.styles as styles
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.crosssection as xsect
import HiggsAnalysis.NtupleAnalysis.tools.multicrabConsistencyCheck as consistencyCheck
import HiggsAnalysis.QCDMeasurement.QCDNormalization as QCDNormalization
import HiggsAnalysis.NtupleAnalysis.tools.analysisModuleSelector as analysisModuleSelector
import HiggsAnalysis.NtupleAnalysis.tools.ShellStyles as ShellStyles

#==== Set analysis, data era, and search mode
analysis = "QCDMeasurement"

#==== Set rebin factor for normalization plots 
# Histograms are generated with 1 GeV bin width, i.e. putting 10 here means 
# that the fit is done on 10 GeV bins
_rebinFactor = 10 
#_rebinFactor = 20 # changing to this can solve fitting problems by smoothing fluctuations

print "Analysis name:", analysis

selectOnlyBins = []#["Inclusive"] #["1"]

def usage():
    print "\n"
    print "### Usage:   QCDMeasurementNormalization.py <multicrab dir>\n"
    print "\n"
    sys.exit()

def treatNegativeBins(h, label):
    # Convert negative bins to zero but leave errors intact
    for k in range(0, h.GetNbinsX()+2):
        if h.GetBinContent(k) < 0.0:
            print "histogram '%s': converted in bin %d a negative value (%f) to zero."%(label, k, h.GetBinContent(k))
            h.SetBinContent(k, 0.0)

def main(argv, dsetMgr, moduleInfoString):
    COMBINEDHISTODIR = "ForQCDNormalization"
    FAKEHISTODIR = "ForQCDNormalizationEWKFakeTaus"
    GENUINEHISTODIR = "ForQCDNormalizationEWKGenuineTaus"
    comparisonList = ["AfterStdSelections"]

    dirs = []
    dirs.append(sys.argv[1])
    
    # Check multicrab consistency
    consistencyCheck.checkConsistencyStandalone(dirs[0],dsetMgr,name="QCD inverted")
   
    # As we use weighted counters for MC normalisation, we have to
    # update the all event count to a separately defined value because
    # the analysis job uses skimmed pattuple as an input
    dsetMgr.updateNAllEventsToPUWeighted()

    # Read integrated luminosities of data dsetMgr from lumi.json
    dsetMgr.loadLuminosities()
    
    print "\Datasets list (initial):\n"
    print dsetMgr.getMCDatasetNames()
    print "\n"

    # Include only 120 mass bin of HW and HH dsetMgr
    dsetMgr.remove(filter(lambda name: "TTToHplus" in name and not "M120" in name, dsetMgr.getAllDatasetNames()))
    dsetMgr.remove(filter(lambda name: "HplusTB" in name, dsetMgr.getAllDatasetNames()))
    dsetMgr.remove(filter(lambda name: "DY2JetsToLL" in name, dsetMgr.getAllDatasetNames()))
    dsetMgr.remove(filter(lambda name: "DY3JetsToLL" in name, dsetMgr.getAllDatasetNames()))
    dsetMgr.remove(filter(lambda name: "DY4JetsToLL" in name, dsetMgr.getAllDatasetNames()))
    dsetMgr.remove(filter(lambda name: "WJetsToLNu_HT" in name, dsetMgr.getAllDatasetNames()))

    print "\Datasets after filter removals:\n"
    print dsetMgr.getMCDatasetNames()
    print "\n"
          
        # Default merging nad ordering of data and MC dsetMgr
    # All data dsetMgr to "Data"
    # All QCD dsetMgr to "QCD"
    # All single top dsetMgr to "SingleTop"
    # WW, WZ, ZZ to "Diboson"
    plots.mergeRenameReorderForDataMC(dsetMgr)

    print "\Datasets after mergeRenameReorderForDataMC:\n"
    print dsetMgr.getMCDatasetNames()
    print "\n"

    # Set BR(t->H) to 0.05, keep BR(H->tau) in 1
    xsect.setHplusCrossSectionsToBR(dsetMgr, br_tH=0.05, br_Htaunu=1)

    # Merge WH and HH dsetMgr to one (for each mass bin)
    plots.mergeWHandHH(dsetMgr)
    # Merge MC EWK samples as one EWK sample
    myMergeList = []
    if "TT" in dsetMgr.getMCDatasetNames():
        myMergeList.append("TT") # Powheg, no neg. weights -> large stats.
    else:
        myMergeList.append("TTJets") # Madgraph with negative weights
        print "Warning: using TTJets as input, but this is suboptimal. Please switch to the TT sample (much more stats.)."

    #myMergeList.append("WJetsHT")
    myMergeList.append("WJets")
    myMergeList.append("DYJetsToLL")

    if "SingleTop" in dsetMgr.getMCDatasetNames():
        myMergeList.append("SingleTop")
    else:
        print "Warning: ignoring single top sample (since merged diboson sample does not exist) ..."


    if "Diboson" in dsetMgr.getMCDatasetNames():
        myMergeList.append("Diboson")
    else:
        print "Warning: ignoring diboson sample (since merged diboson sample does not exist) ..."

    for item in myMergeList:
        if not item in dsetMgr.getMCDatasetNames():
            raise Exception("Error: tried to use dataset '%s' as part of the merged EWK dataset, but the dataset '%s' does not exist!"%(item,item))
    dsetMgr.merge("EWK", myMergeList)

    print "\nFinal dataset list:\n"
    print dsetMgr.getMCDatasetNames()
    print "\n"

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
                print "DEBUG: We are looking for hisrogram "+COMBINEDHISTODIR+"/"+BASELINETAUHISTONAME+binIndex
                hDummy = dsetMgr.getDataset("Data").getDatasetRootHisto(COMBINEDHISTODIR+"/"+BASELINETAUHISTONAME+binIndex).getHistogram()
                title = hDummy.GetTitle()
                title = title.replace("METBaseline"+HISTONAME,"")
                if hDummy.Integral() > 0.0:
                    bins.append(binIndex)
                    if binIndex == "Inclusive":
                        binLabels.append(binIndex)
                    else:
                        binLabels.append(QCDNormalization.getModifiedBinLabelString(title))
                    if FITMIN == None:
                        FITMIN = hDummy.GetXaxis().GetXmin()
                        FITMAX = hDummy.GetXaxis().GetXmax()
                    hDummy.Delete()
                else:
                    print "Skipping bin '%s' (%s) because it has no entries"%(binIndex, QCDNormalization.getModifiedBinLabelString(title))
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
        #manager = QCDNormalization.QCDNormalizationManagerExperimental1(binLabels)
        manager = QCDNormalization.QCDNormalizationManagerDefault(binLabels, dirs[0], moduleInfoString)
        
        #===== Create templates (EWK fakes, EWK genuine, QCD; data template is created by manager)
        template_EWKFakeTaus_Baseline = manager.createTemplate("EWKFakeTaus_Baseline")
        template_EWKFakeTaus_Inverted = manager.createTemplate("EWKFakeTaus_Inverted")
        template_EWKGenuineTaus_Baseline = manager.createTemplate("EWKGenuineTaus_Baseline")
        template_EWKGenuineTaus_Inverted = manager.createTemplate("EWKGenuineTaus_Inverted")
        template_EWKInclusive_Baseline = manager.createTemplate("EWKInclusive_Baseline")
        template_EWKInclusive_Inverted = manager.createTemplate("EWKInclusive_Inverted")
        template_QCD_Baseline = manager.createTemplate("QCD_Baseline")
        template_QCD_Inverted = manager.createTemplate("QCD_Inverted")
        
        #===== Define fit functions and fit parameters
        # The available functions are defined in the FitFunction class in the QCDMeasurement/python/QCDNormalization.py file
        
        # commented out fitter for EWK fake taus, since only the fit on inclusive EWK is used to obtain w_QCD
        #boundary = 100
        #template_EWKFakeTaus_Baseline.setFitter(QCDNormalization.FitFunction("EWKFunctionInv", boundary=boundary, norm=1, rejectPoints=1),
                                                #FITMIN, FITMAX)
        #template_EWKFakeTaus_Baseline.setDefaultFitParam(defaultInitialValue=[10.0, 100, 45,   0.02],
                                                         #defaultLowerLimit=  [ 0.1,  70,  10,  0.001],
                                                         #defaultUpperLimit=  [ 30, 300,  100,    0.1])
        # commented out fitter for EWK genuine taus, since only the fit on inclusive EWK is used to obtain w_QCD
        #boundary = 150
        #template_EWKGenuineTaus_Baseline.setFitter(QCDNormalization.FitFunction("EWKFunction", boundary=boundary, norm=1, rejectPoints=1),
                                                   #FITMIN, FITMAX)
        #template_EWKGenuineTaus_Baseline.setDefaultFitParam(defaultLowerLimit=[0.5,  90, 30, 0.0001],
                                                            #defaultUpperLimit=[ 20, 150, 50,    1.0])
        # Inclusive EWK
        boundary = 150
        template_EWKInclusive_Baseline.setFitter(QCDNormalization.FitFunction("EWKFunction", boundary=boundary, norm=1, rejectPoints=1),
                                                 FITMIN, FITMAX)
        template_EWKInclusive_Baseline.setDefaultFitParam(defaultLowerLimit=[0.5,  90, 30, 0.0001],
                                                          defaultUpperLimit=[ 20, 150, 60,    1.0])

        # Note that the same function is used for QCD only and QCD+EWK fakes
        template_QCD_Inverted.setFitter(QCDNormalization.FitFunction("QCDFunction", norm=1), FITMIN, FITMAX)
#        template_QCD_Inverted.setDefaultFitParam(defaultLowerLimit=[0.0001, 0.001, 0.1, 0.0,  10, 0.0001, 0.001],
#                                                 defaultUpperLimit=[   200,    10,  10, 150, 100,      1, 0.05])
        template_QCD_Inverted.setDefaultFitParam(defaultLowerLimit=[ 30, 0.1, 0.1,  10,  10, 0.00001, 0.001], # new default limits to make fits more stable,
                                                 defaultUpperLimit=[ 130, 20,  20, 200, 200,    0.01,   0.1]) # corresponding to the 7 free param. of the fit function        
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
            for histogram in [hmetBase_data, hmetInverted_data, hmetBase_EWK_GenuineTaus, hmetInverted_EWK_GenuineTaus, hmetBase_EWK_FakeTaus, hmetInverted_EWK_FakeTaus]:
                 histogram.Rebin(_rebinFactor)

            #===== Obtain inclusive EWK histograms
            hmetBase_EWKinclusive = hmetBase_EWK_GenuineTaus.Clone("EWKinclusiveBase")
            hmetBase_EWKinclusive.Add(hmetBase_EWK_FakeTaus, 1.0)
            
            hmetInverted_EWKinclusive = hmetInverted_EWK_GenuineTaus.Clone("EWKinclusiveInv")
            hmetInverted_EWKinclusive.Add(hmetInverted_EWK_FakeTaus, 1.0)
            
            #===== Obtain histograms for QCD (subtract MC EWK events from data)
            # QCD from baseline is usable only as a cross check
            hmetBase_QCD = hmetBase_data.Clone("QCDbase")
            hmetBase_QCD.Add(hmetBase_EWKinclusive,-1)
            
            hmetInverted_QCD = hmetInverted_data.Clone("QCDinv")
            hmetInverted_QCD.Add(hmetInverted_EWKinclusive,-1)
            
            #===== Set histograms to the templates
            template_EWKFakeTaus_Inverted.setHistogram(hmetInverted_EWK_FakeTaus, binLabels[i])
            template_EWKGenuineTaus_Inverted.setHistogram(hmetInverted_EWK_GenuineTaus, binLabels[i])
            template_EWKInclusive_Inverted.setHistogram(hmetInverted_EWKinclusive, binLabels[i])
            template_QCD_Inverted.setHistogram(hmetInverted_QCD, binLabels[i])
            
            template_EWKFakeTaus_Baseline.setHistogram(hmetBase_EWK_FakeTaus, binLabels[i])
            template_EWKGenuineTaus_Baseline.setHistogram(hmetBase_EWK_GenuineTaus, binLabels[i])
            template_EWKInclusive_Baseline.setHistogram(hmetBase_EWKinclusive, binLabels[i])
            template_QCD_Baseline.setHistogram(hmetBase_QCD, binLabels[i])
            
            #===== Make plots of templates
            manager.plotTemplates()
            
            #===== Fit individual templates to data
            fitOptions = "R BLW" # RBLW

            manager.calculateNormalizationCoefficients(hmetBase_data, fitOptions, FITMIN, FITMAX)
            
            #===== Calculate combined normalisation coefficient (f_fakes = w*f_QCD + (1-w)*f_EWKfakes)
            # Obtain histograms
            histoName = "ForDataDrivenCtrlPlots/shapeTransverseMass/shapeTransverseMass"+binStr
            dataMt = plots.DataMCPlot(dsetMgr, histoName).histoMgr.getHisto("Data").getRootHisto().Clone(histoName)
            treatNegativeBins(dataMt, "Data_inverted mT")
            histoName = "ForDataDrivenCtrlPlotsEWKFakeTaus/shapeTransverseMass/shapeTransverseMass"+binStr
            ewkFakeTausMt = plots.DataMCPlot(dsetMgr, histoName).histoMgr.getHisto("EWK").getRootHisto().Clone(histoName)
            treatNegativeBins(ewkFakeTausMt, "ewkFakeTaus_inverted mT")
            histoName = "ForDataDrivenCtrlPlotsEWKGenuineTaus/shapeTransverseMass/shapeTransverseMass"+binStr
            ewkGenuineTausMt = plots.DataMCPlot(dsetMgr, histoName).histoMgr.getHisto("EWK").getRootHisto().Clone(histoName)
            treatNegativeBins(ewkGenuineTausMt, "ewkGenuineTaus_inverted mT")
            qcdMt = dataMt.Clone("QCD")
            qcdMt.Add(ewkFakeTausMt, -1)
            qcdMt.Add(ewkGenuineTausMt, -1)
            treatNegativeBins(qcdMt, "QCD_inverted mT")
            # Do calculation
            manager.calculateCombinedNormalizationCoefficient(qcdMt, ewkFakeTausMt)

        #===== Save normalization
        outFileName = "QCDNormalizationFactors_%s_%s.py"%(HISTONAME, moduleInfoString)
        print argv[1],outFileName
        outFileFullName = os.path.join(argv[1],outFileName)
        manager.writeScaleFactorFile(outFileFullName, moduleInfoString)

if __name__ == "__main__":
    # Check parameters
    if len(sys.argv) < 2:
        usage()
    # Find out the era/search mode/optimization mode combinations and run each of them
    myModuleSelector = analysisModuleSelector.AnalysisModuleSelector()
    dsetMgrCreator = dataset.readFromMulticrabCfg(directory=sys.argv[1])
    myModuleSelector.setPrimarySource("analysis", dsetMgrCreator)
    myModuleSelector.doSelect(None)
    #myModuleSelector.printSelectedCombinationCount()
    for era in myModuleSelector.getSelectedEras():
        for searchMode in myModuleSelector.getSelectedSearchModes():
            for optimizationMode in myModuleSelector.getSelectedOptimizationModes():
                print ShellStyles.HighlightStyle()+"\nCalculating normalization for module %s/%s/%s%s"%(era, searchMode, optimizationMode, ShellStyles.NormalStyle())
                # Construct info string for the module
                moduleInfoString = "%s_%s"%(era, searchMode)
                if len(optimizationMode) > 0:
                    moduleInfoString += "_%s"%(optimizationMode)
                # Create dataset manager
                dsetMgr = dsetMgrCreator.createDatasetManager(dataEra=era,searchMode=searchMode,optimizationMode=optimizationMode)
                main(sys.argv, dsetMgr, moduleInfoString)
    dsetMgrCreator.close()
