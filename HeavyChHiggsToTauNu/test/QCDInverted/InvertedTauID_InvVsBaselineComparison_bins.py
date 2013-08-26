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
import array  

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect

from InvertedTauID import *

ReBinning = False

#dataEra = "Run2012ABCD"
#dataEra = "Run2012D"
dataEra = "Run2011B"

searchMode = "Light"
#searchMode = "Heavy"

def usage():
    print "\n"
    print "### Usage:   InvertedTauID_InvVsBaselineComparison.py <multicrab dir>\n"
    print "\n"
    sys.exit()



ptbins = ["1","2","3","4","5","6","7","8","9","10"]



try:
    from QCDInvertedNormalizationFactors import *
except ImportError:   
    print
    print "    WARNING, QCDInvertedNormalizationFactors.py not found!"
    print "    Run script InvertedTauID_Normalization.py to generate QCDInvertedNormalizationFactors.py"
    print

def normalisation():

    normData = {}
    normEWK = {}

    print "-------------------"
#    print "btaggingFactors ", btaggingToBvetoAfterMetFactors
    print "-------------------"
    for bin in ptbins: 
        normData[bin] = QCDInvertedNormalization[bin]
        normEWK[bin] = QCDInvertedNormalization[bin+"EWK"]
 
    print "norm factors", normData
    print "norm factors EWK", normEWK
                 
    return normData,normEWK


def normalisationInclusive():
 
    norm_inc = QCDInvertedNormalization["inclusive"]
    normEWK_inc = QCDInvertedNormalization["inclusiveEWK"]
              
    print "inclusive norm", norm_inc,normEWK_inc       
    return norm_inc,normEWK_inc



def main():
    if len(sys.argv) < 2:
        usage()


#    HISTONAME = "METInvertedTauIdAfterJets"
    HISTONAME = "METInvertedTauIdAfterCollinearCuts"
#    HISTONAME = "MET_InvertedTauIdBveto"
#    HISTONAME = "METInvertedTauIdAfterCollinearCutsPlusBtag"
#    HISTONAME = "METInvertedTauIdAfterCollinearCutsPlusBtag"
#    HISTONAME = "MTInvertedTauIdJet"
#    HISTONAME = "MTInvertedTauIdPhi"

    invertedhisto = HISTONAME
    baselinehisto = HISTONAME.replace("Inverted","BaseLine")

    dirs = []
    if len(sys.argv) < 2:
        usage()

    dirs.append(sys.argv[1])
    
    # Create all datasets from a multicrab task
    #datasets = dataset.getDatasetsFromMulticrabCfg(counters=counters)
    datasets = dataset.getDatasetsFromMulticrabDirs(dirs,dataEra=dataEra,  searchMode=searchMode, analysisName=analysis)
#    datasets = dataset.getDatasetsFromMulticrabDirs(dirs,counters=counters, dataEra=dataEra, analysisBaseName="signalAnalysisInvertedTau" )

    # As we use weighted counters for MC normalisation, we have to
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
            
#        metBase_data = metBase_data.Rebin(len(histobins)-1,   metInverted_EWK = metInver.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/"+invertedhisto) "",array.array("d", histobins))
        metInverted_data = metInverted_data.Rebin(len(histobins)-1,"",array.array("d", histobins))
        metBase_EWK = metBase_EWK.Rebin(len(histobins)-1,"",array.array("d", histobins))
        metInverted_EWK = metInverted_EWK.Rebin(len(histobins)-1,"",array.array("d", histobins))
    
    normData,normEWK=normalisation()

    metInverted = []
    metBaseline = []
    metBaselineQCD = []
    
    for ptbin in ptbins:
        ## inverted
        met_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/METInvertedTauIdAfterCollinearCuts/METInvertedTauIdAfterCollinearCuts"+ptbin)])

        #met_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/"+invertedhisto+ptbin)])
        met_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))
        met = met_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()        
        met.Scale(normData[ptbin])
    
        metEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/METInvertedTauIdAfterCollinearCuts/METInvertedTauIdAfterCollinearCuts"+ptbin)])        
        #metEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/"+invertedhisto+ptbin)])
        metEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        metEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))
        metEWK = metEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        metEWK.Scale(normEWK[ptbin])
        met.Add(metEWK, -1)
        metInverted.append(met) 

## baseline
        met_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("baseline/METBaselineTauIdAfterCollinearCuts/METBaselineTauIdAfterCollinearCuts"+ptbin)])

        #met_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/"+invertedhisto+ptbin)])
        met_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))
        metbaseline = met_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()        
    
        metEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("baseline/METBaselineTauIdAfterCollinearCuts/METBaselineTauIdAfterCollinearCuts"+ptbin)])        
        #metEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/"+invertedhisto+ptbin)])
        metEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        metEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))
        metEWKbaseline = metEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        metBaseline.append(metbaseline)
        metbaseline.Add(metEWKbaseline, -1)
        metBaselineQCD.append(metbaseline)

        
    metInverted_data = metInverted[0].Clone("met")
    metInverted_data.SetName("met")
    metInverted_data.SetTitle("Inverted tau ID")
    metInverted_data.Reset()
    for histo in metInverted:
        metInverted_data.Add(histo)
        
    metBaseline_data = metBaseline[0].Clone("met")
    metBaseline_data.SetName("met")
    metBaseline_data.SetTitle("baseline tau ID")
    metBaseline_data.Reset()
    for histo in metBaseline:
        metBaseline_data.Add(histo)

    metBaseline_QCD = metBaselineQCD[0].Clone("met")
    metBaseline_QCD .SetName("met")
    metBaseline_QCD.SetTitle("baseline tau ID")
    metBaseline_QCD.Reset()
    for histo in metBaselineQCD:
        metBaseline_QCD.Add(histo)

        
    #metBase_data.SetTitle("Data: BaseLine TauID")
    #metInverted_data.SetTitle("Data: Inverted TauID")
    #metBase_QCD = metBase_data.Clone("QCD")

    #metBase_QCD.Add(metBase_EWK,-1)
    #metBase_QCD.SetTitle("Data - EWK MC: BaseLine TauID")

    invertedQCD.setLabel("BaseVsInverted")
    invertedQCD.comparison(metInverted_data,metBaseline_data)
    invertedQCD.setLabel("BaseMinusEWKVsInverted")
    invertedQCD.comparison(metInverted_data,metBaseline_QCD)
    invertedQCD.setLabel("McVsInverted")
#    invertedQCD.comparison(metInverted_data,metInverted_MC)
    invertedQCD.setLabel("EfficiencyBaseMinusEWKVsInverted")
    invertedQCD.cutefficiency(metInverted_data,metBaseline_QCD )


if __name__ == "__main__":
    main()
