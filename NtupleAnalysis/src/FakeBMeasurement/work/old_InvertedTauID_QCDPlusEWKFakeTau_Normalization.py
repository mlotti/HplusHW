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

from InvertedTauID_QCDPlusEWKFakeTau import *
#dataEra = "Run2011A"
#dataEra = "Run2011B"
dataEra = "Run2012ABCD"


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

    FAKEHISTO = "OnlyEWKFakeTaus"
    GENUINEHISTO = "PlusFilteredEWKFakeTaus"

   
    dirs = []
    if len(sys.argv) < 2:
	usage()

    dirs.append(sys.argv[1])

    
    # Create all datasets from a multicrab task

    datasets = dataset.getDatasetsFromMulticrabDirs(dirs,dataEra=dataEra,  searchMode=searchMode, analysisName="signalAnalysisInvertedTau",optimizationMode="") #no collinear
    #datasets = dataset.getDatasetsFromMulticrabDirs(dirs,dataEra=dataEra,  searchMode=searchMode, analysisName="signalAnalysisInvertedTau",optimizationMode="OptQCDTailKillerLoosePlus") #collinear


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
    datasets.remove(filter(lambda name: "TTJets_SemiLept" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "TTJets_FullLept" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "TTJets_Hadronic" in name, datasets.getAllDatasetNames()))
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

    invertedQCD = InvertedTauID(False)
    invertedQCD.setLumi(datasets.getDataset("Data").getLuminosity())
    invertedQCD.setInfo([dataEra,searchMode,HISTONAME])

    invertedQCD_separatedFakes = InvertedTauID(True)
    invertedQCD_separatedFakes.setLumi(datasets.getDataset("Data").getLuminosity())
    invertedQCD_separatedFakes.setInfo([dataEra,searchMode,HISTONAME])
    
    histonames = datasets.getDataset("Data").getDirectoryContent("baseline/METBaseline"+HISTONAME)
    bins = []
    binLabels = []
    for histoname in histonames:
        bins.append(histoname.replace("METBaseline"+HISTONAME,""))
        title = datasets.getDataset("Data").getDatasetRootHisto("baseline/METBaseline"+HISTONAME+"/"+histoname).getHistogram().GetTitle()
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
    #binLabels = bins # for this data set
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
        invertedQCD_separatedFakes.setLabel(binLabels[i])

        metBase = plots.DataMCPlot(datasets, "baseline/METBaseline"+HISTONAME+"/METBaseline"+HISTONAME+bin)
        metInver = plots.DataMCPlot(datasets, "Inverted/METInverted"+HISTONAME+"/METInverted"+HISTONAME+bin)

        #metBase_EWK = plots.DataMCPlot(datasets, "baseline/METBaseline"+HISTONAME+"/METBaseline"+HISTONAME+bin)
        #metInver_EWK = plots.DataMCPlot(datasets, "Inverted/METInverted"+HISTONAME+"/METInverted"+HISTONAME+bin)
        metBase_GenuineTaus = plots.DataMCPlot(datasets, "baseline/METBaseline"+HISTONAME+GENUINEHISTO+"/METBaseline"+HISTONAME+GENUINEHISTO+bin)
        metInver_GenuineTaus = plots.DataMCPlot(datasets, "Inverted/METInverted"+HISTONAME+GENUINEHISTO+"/METInverted"+HISTONAME+GENUINEHISTO+bin)
        metBase_FakeTaus = plots.DataMCPlot(datasets, "baseline/METBaseline"+HISTONAME+FAKEHISTO+"/METBaseline"+HISTONAME+FAKEHISTO+bin)
        metInver_FakeTaus = plots.DataMCPlot(datasets, "Inverted/METInverted"+HISTONAME+FAKEHISTO+"/METInverted"+HISTONAME+FAKEHISTO+bin)


        # Rebin before subtracting
        
        metBase.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10)) #5
        metInver.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10)) #5
        #metBase_EWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10)) #5         
        #metInver_EWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10)) #5
        metBase_GenuineTaus.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10)) #5
        metInver_GenuineTaus.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10)) #5
        metBase_FakeTaus.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10)) #5
        metInver_FakeTaus.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10)) #5
        
        metInverted_data = metInver.histoMgr.getHisto("Data").getRootHisto().Clone("Inverted/METInverted"+HISTONAME+"/METInverted"+HISTONAME+bin)
        metBase_data = metBase.histoMgr.getHisto("Data").getRootHisto().Clone("baseline/METBaseLine"+HISTONAME+"/METBaseline"+HISTONAME+bin)

        metInverted_EWK = metInver.histoMgr.getHisto("EWK").getRootHisto().Clone("Inverted/METInverted"+HISTONAME+"/METInverted"+HISTONAME+bin)
        metBase_EWK = metBase.histoMgr.getHisto("EWK").getRootHisto().Clone("baseline/METBaseLine"+HISTONAME+"/METBaseline"+HISTONAME+bin)

        metInverted_EWK_GenuineTaus = metInver_GenuineTaus.histoMgr.getHisto("EWK").getRootHisto().Clone("Inverted/METInverted"+HISTONAME+GENUINEHISTO+"/METInverted"+HISTONAME+GENUINEHISTO+bin)
        metBase_EWK_GenuineTaus = metBase_GenuineTaus.histoMgr.getHisto("EWK").getRootHisto().Clone("baseline/METBaseLine"+HISTONAME+GENUINEHISTO+"/METBaseline"+HISTONAME+GENUINEHISTO+bin)

        metInverted_EWK_FakeTaus = metInver_FakeTaus.histoMgr.getHisto("EWK").getRootHisto().Clone("Inverted/METInverted"+HISTONAME+FAKEHISTO+"/METInverted"+HISTONAME+FAKEHISTO+bin)
        metBase_EWK_FakeTaus = metBase_FakeTaus.histoMgr.getHisto("EWK").getRootHisto().Clone("baseline/METBaseLine"+HISTONAME+FAKEHISTO+"/METBaseline"+HISTONAME+FAKEHISTO+bin)

        metBase_QCD = metBase_data.Clone("QCD")
        metBase_QCD.Add(metBase_EWK,-1)
        metInverted_QCD = metInverted_data.Clone("QCD")
        metInverted_QCD.Add(metInverted_EWK,-1)

        metBase_QCD_separatedFakes = metBase_data.Clone("QCD")
        metBase_QCD_separatedFakes.Add(metBase_EWK_GenuineTaus,-1)
        metBase_QCD_separatedFakes.Add(metBase_EWK_FakeTaus,-1)
        metInverted_QCD_separatedFakes = metInverted_data.Clone("QCD")
        metInverted_QCD_separatedFakes.Add(metInverted_EWK_GenuineTaus,-1)
        metInverted_QCD_separatedFakes.Add(metInverted_EWK_FakeTaus,-1)

        metInverted_data = addlabels(metInverted_data)
        metInverted_EWK  = addlabels(metInverted_EWK)
        metInverted_EWK_GenuineTaus  = addlabels(metInverted_EWK_GenuineTaus)
        metInverted_EWK_FakeTaus  = addlabels(metInverted_EWK_FakeTaus)
        
        metBase_data     = addlabels(metBase_data)
        metBase_EWK  = addlabels(metBase_EWK)
        metBase_EWK_GenuineTaus = addlabels(metBase_EWK_GenuineTaus)
        metBase_EWK_FakeTaus = addlabels(metBase_EWK_FakeTaus)

        metInverted_QCD  = addlabels(metInverted_QCD)
        metInverted_QCD_separatedFakes  = addlabels(metInverted_QCD_separatedFakes)
        
        #non-separated

        invertedQCD.plotHisto(metInverted_data,"inverted")
        invertedQCD.plotHisto(metInverted_EWK,"invertedEWK")
        invertedQCD.plotHisto(metBase_data,"baseline")
        invertedQCD.plotHisto(metBase_EWK,"baselineEWK")

        fitOptions = "LRB"

        invertedQCD.fitEWK(metInverted_EWK,fitOptions)
        invertedQCD.fitEWK(metBase_EWK,fitOptions)
        invertedQCD.fitQCD(metInverted_QCD,fitOptions)
        invertedQCD.fitData(metBase_data)

        invertedQCD.getNormalization()

        #separated

        invertedQCD_separatedFakes.plotHisto(metInverted_data,"inverted")
        invertedQCD_separatedFakes.plotHisto(metInverted_EWK_GenuineTaus,"invertedEWKGenuineTaus")
        invertedQCD_separatedFakes.plotHisto(metInverted_EWK_FakeTaus,"invertedEWKFakeTaus")
        
        invertedQCD_separatedFakes.plotHisto(metBase_data,"baseline")
        invertedQCD_separatedFakes.plotHisto(metBase_EWK_GenuineTaus,"baselineEWKGenuineTaus")
        invertedQCD_separatedFakes.plotHisto(metBase_EWK_FakeTaus,"baselineEWKFakeTaus")
        
        invertedQCD_separatedFakes.fitEWK_GenuineTaus(metInverted_EWK_GenuineTaus,fitOptions) 
        invertedQCD_separatedFakes.fitEWK_GenuineTaus(metBase_EWK_GenuineTaus,fitOptions)

        invertedQCD_separatedFakes.fitEWK_FakeTaus(metInverted_EWK_FakeTaus,fitOptions)
        invertedQCD_separatedFakes.fitEWK_FakeTaus(metBase_EWK_FakeTaus,fitOptions)

        invertedQCD_separatedFakes.fitQCD(metInverted_QCD_separatedFakes,fitOptions)
        invertedQCD_separatedFakes.fitData(metBase_data)
        
        invertedQCD_separatedFakes.getNormalization()
        
    invertedQCD.Summary()
    invertedQCD.WriteNormalizationToFile("QCDInvertedNormalizationFactors.py")
    invertedQCD.WriteLatexOutput("fits.tex")
    
    invertedQCD_separatedFakes.Summary()
    invertedQCD_separatedFakes.WriteNormalizationToFile("QCDInvertedNormalizationFactorsSeparatedFakeTaus.py")
    invertedQCD_separatedFakes.WriteLatexOutput("fits_separatedfaketaus.tex")

    mergeNormalizations("QCDInvertedNormalizationFactors.py","QCDInvertedNormalizationFactorsSeparatedFakeTaus.py")

def mergeNormalizations(file1, file2):
    outputfilename = "QCDInvertedCombinedNormalizationFactors.py"
    fOUT = open(outputfilename,"w")
    fIN1 = open(file1, "r")
    fIN2 = open(file2, "r")
    
    now = datetime.datetime.now()

    fOUT.write("import sys\n")
    fOUT.write("\n")
    fOUT.write("# Generated on %s,\n"%now.ctime())
    fOUT.write("# normalizations merged from files:\n# " + file1 + " and\n# " + file2 + "\n")
    fOUT.write("\n")

    current = fIN1.readline()
    targetline = "def QCDInvertedNormalizationSafetyCheck(era):\n"
    while current != targetline and current != "":
        current = fIN1.readline()
    fOUT.write(current)
    fOUT.write(fIN1.read())
    fOUT.write("\n")
    
    current = fIN2.readline()
    targetline = file2.replace(".py","").replace("Factors","") + " = {\n"

    while current != targetline and current != "":
        current = fIN2.readline()

    fOUT.write(current)
    fOUT.write(fIN2.read())
    print "Combined normalization factors written in file ", outputfilename
    

def addlabels(histo):
    binwidth = int(histo.GetXaxis().GetBinWidth(1))
    histo.GetXaxis().SetTitle("Type1 PFMET (GeV)")
    histo.GetYaxis().SetTitle("Events / %i GeV"%binwidth)
    histo.GetYaxis().SetTitleOffset(1.5)
    return histo

if __name__ == "__main__":
    main(sys.argv)
