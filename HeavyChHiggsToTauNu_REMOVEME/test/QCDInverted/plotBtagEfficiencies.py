#!/usr/bin/env python

######################################################################
#
# This plot script is for comparing the embedded data to embedding MC
# within the signal analysis. The corresponding python job
# configuration is signalAnalysis_cfg.py with "doPat=1
# tauEmbeddingInput=1" command line arguments.
#
# Authors: Ritva Kinnunen, Matti Kortelainen
#
######################################################################

import ROOT
from ROOT import *
import sys,os
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetPalette(1)
from array import array
from math import fabs
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.FindFirstBinAbove import * 
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.bayes import * 
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.myArrays import *
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect
from InvertedTauID import *

# Configuration
analysis = "signalAnalysisInvertedTau"
#analysis = "signalOptimisation"
#analysis = "signalAnalysisJESMinus03eta02METMinus10"
#analysis = "EWKFakeTauAnalysisJESMinus03eta02METMinus10"
#analysis = "signalOptimisation/QCDAnalysisVariation_tauPt40_rtau0_btag2_METcut60_FakeMETCut0"
#analysis = "signalAnalysisTauSelectionHPSTightTauBased2"
#analysis = "signalAnalysisBtaggingTest2"
counters = analysis+"/counters"

treeDraw = dataset.TreeDraw(analysis+"/tree", weight="weightPileup*weightTrigger*weightPrescale")

#QCDfromData = True
QCDfromData = False

lastPtBin150 = False
lastPtBin120 = True

mcOnly = False
#mcOnly = True
mcOnlyLumi = 5000 # pb

searchMode = "Light"
#searchMode = "Heavy"


#dataEra = "Run2011A"
#dataEra = "Run2011B"

dataEra = "Run2012ABCD"


print "dataEra"

def usage():
    print "\n"
    print "### Usage:   plotSignalAnalysisInverted.py <multicrab dir>\n"
    print "\n"
    sys.exit()

# main function
def main():

    if len(sys.argv) < 2:
        usage()

    dirs = []
    dirs.append(sys.argv[1])

    # Read the datasets
#    datasets = dataset.getDatasetsFromMulticrabDirs(dirs,counters=counters, dataEra=dataEra, analysisBaseName="signalAnalysisInvertedTau")
    datasets = dataset.getDatasetsFromMulticrabDirs(dirs,dataEra=dataEra, searchMode=searchMode, analysisName=analysis) 
#    datasets = dataset.getDatasetsFromMulticrabDirs(dirs,counters=counters)
#    datasets = dataset.getDatasetsFromMulticrabCfg(counters=counters, dataEra=dataEra)
#    datasets.updateNAllEventsToPUWeighted()
    datasets.loadLuminosities()
    datasets.updateNAllEventsToPUWeighted()

    
    # Take QCD from data
    datasetsQCD = None

    if QCDfromData:

        datasetsQCD = dataset.getDatasetsFromMulticrabCfg(cfgfile="/home/rkinnune/signalAnalysis/CMSSW_4_2_8_patch2/src/HiggsAnalysis/HeavyChHiggsToTauNu/test/multicrab_111123_132128/multicrab.cfg", counters=counters)
        datasetsQCD.loadLuminosities()
        print "QCDfromData", QCDfromData
        datasetsQCD.mergeData()
        datasetsQCD.remove(datasetsQCD.getMCDatasetNames())
        datasetsQCD.rename("Data", "QCD")
    


    plots.mergeRenameReorderForDataMC(datasets)

    print "Int.Lumi",datasets.getDataset("Data").getLuminosity()

    # Remove signals other than M120
    datasets.remove(filter(lambda name: "TTToHplus" in name and not "M120" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "HplusTB" in name, datasets.getAllDatasetNames()))
    datasets.merge("EWK", ["WJets", "DYJetsToLL", "SingleTop", "Diboson","TTJets"], keepSources=True)
    datasets.remove(filter(lambda name: "W2Jets" in name, datasets.getAllDatasetNames()))        
    datasets.remove(filter(lambda name: "W3Jets" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "W4Jets" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "Hplus_taunu_s-channel" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "Hplus_taunu_t-channel" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "Hplus_taunu_tW-channel" in name, datasets.getAllDatasetNames()))
    datasets_lands = datasets.deepCopy()

    # Set the signal cross sections to the ttbar for datasets for lands
#    xsect.setHplusCrossSectionsToTop(datasets_lands)

    # Set the signal cross sections to a given BR(t->H), BR(h->taunu)
    xsect.setHplusCrossSectionsToBR(datasets, br_tH=0.01, br_Htaunu=1)

    # Set the signal cross sections to a value from MSSM
#    xsect.setHplusCrossSectionsToMSSM(datasets, tanbeta=20, mu=200)

    plots.mergeWHandHH(datasets) # merging of WH and HH signals must be done after setting the cross section


    # Apply TDR style
    style = tdrstyle.TDRStyle()

    # Create plots
    doPlots(datasets)

    # Write mt histograms to ROOT file
#    writeTransverseMass(datasets_lands)

    # Print counters
    doCounters(datasets)




def doPlots(datasets):
    def createPlot(name, **kwargs):
        if mcOnly:
            return plots.MCPlot(datasets, name, normalizeToLumi=mcOnlyLumi, **kwargs)
        else:
            return plots.DataMCPlot(datasets, name, **kwargs)
 
    controlPlots(datasets)



def doCounters(datasets):
    eventCounter = counter.EventCounter(datasets)
    
    ewkDatasets = [
        "WJets", "TTJets",
        "DYJetsToLL", "SingleTop", "Diboson"
        ]


    eventCounter.normalizeMCByLuminosity()
#    eventCounter.normalizeMCToLuminosity(73)
    print "============================================================"
    print "Main counter (MC normalized by collision data luminosity)"
    mainTable = eventCounter.getMainCounterTable()
    # No uncertainties
    cellFormat = counter.TableFormatText(cellFormat=counter.CellFormatText(valueOnly=True))
    print mainTable.format(cellFormat)

    print eventCounter.getSubCounterTable("b-tagging").format(cellFormat)
    print eventCounter.getSubCounterTable("Jet selection").format(cellFormat)
    print eventCounter.getSubCounterTable("Jet main").format(cellFormat)    

try:
    from QCDInvertedNormalizationFactors import *
except ImportError:   
    print
    print "    WARNING, QCDInvertedNormalizationFactors.py not found!"
    print "    Run script InvertedTauID_Normalization.py to generate QCDInvertedNormalizationFactors.py"
    print


try:  
    from QCDInvertedBtaggingFactors import *
except ImportError:   
    print
    print "    WARNING, QCDInvertedBtaggingFactors.py not found!"
    print

    
 
    
ptbins = [
    "4050",
    "5060",
    "6070",
    "7080",
    "80100",
    "100120",
    "120",
    ]


def normalisation():

    normData = {}
    normEWK = {}

    normFactorisedData = {}
    normFactorisedEWK = {}
    
    norm_inc = QCDInvertedNormalization["inclusive"]
    normEWK_inc = QCDInvertedNormalization["inclusiveEWK"]    
    normFactorised_inc = norm_inc  * btaggingFactors["inclusive"]
    normFactorisedEWK_inc = normEWK_inc * btaggingFactors["inclusive"]
    
    for bin in ptbins: 
        normData[bin] = QCDInvertedNormalization[bin]
        normEWK[bin] = QCDInvertedNormalization[bin+"EWK"]
        normFactorisedData[bin] = QCDInvertedNormalization[bin] *  btaggingFactors[bin]
        normFactorisedEWK[bin] = QCDInvertedNormalization[bin+"EWK"] * btaggingFactors[bin]
    print "inclusive norm", norm_inc,normEWK_inc
    print "norm factors", normData
    print "norm factors EWK", normEWK
    
    print "inclusive factorised norm", normFactorised_inc,normFactorisedEWK_inc
    print "norm factors factorised", normFactorisedData
    print "norm factors EWK factorised", normFactorisedEWK
             
    return normData,normEWK,normFactorisedData,normFactorisedEWK


def normalisationInclusive():
 
    norm_inc = QCDInvertedNormalization["inclusive"]
    normEWK_inc = QCDInvertedNormalization["inclusiveEWK"]
              
    print "inclusive norm", norm_inc,normEWK_inc       
    return norm_inc,normEWK_inc 


def controlPlots(datasets):
    
    normData,normEWK,normFactorisedData,normFactorisedEWK=normalisation()
    norm_inc,normEWK_inc = normalisationInclusive()



    hmet = []
    hmetb = []
    effArray = []

    effErrArray = []


    hmetbveto = []
    hmtBtag = []
    hmtBveto = []
    hmtNoMetBtag = []
    hmtNoMetBveto = []
    effBvetoArray = []
    effErrBvetoArray = []
    effArrayMt= []
    effErrArrayMt= []

    effArrayMtNoMet= []
    effErrArrayMtNoMet= []
    
## histograms in bins, normalisation and substraction of EWK contribution
    ## mt with 2dim deltaPhi cut
    for ptbin in ptbins:
 
        ### MET
        mmt_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MET_InvertedTauIdJets"+ptbin)])
        mmt_tmp._setLegendStyles()
        mmt_tmp._setLegendLabels()
        mmt_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mmt_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
        mmt = mmt_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        mmt.Scale(normData[ptbin])
#        hmt.append(mt)

        mmtEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MET_InvertedTauIdJets"+ptbin)])
        mmtEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mmtEWK_tmp._setLegendStyles()
        mmtEWK_tmp._setLegendLabels()
        mmtEWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mmtEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
        mmtEWK = mmtEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        mmtEWK.Scale(normEWK[ptbin])
        mmt.Add(mmtEWK, -1)
        hmet.append(mmt)


        ### MET with btagging
        mmtb_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MET_InvertedTauIdBtag"+ptbin)])
        mmtb_tmp._setLegendStyles()
        mmtb_tmp._setLegendLabels()
        mmtb_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mmtb_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
        mmtb = mmtb_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        mmtb.Scale(normData[ptbin])
#        hmt.append(mt)

        mmtbEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MET_InvertedTauIdBtag"+ptbin)])
        mmtbEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mmtbEWK_tmp._setLegendStyles()
        mmtbEWK_tmp._setLegendLabels()
        mmtbEWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mmtbEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
        mmtbEWK = mmtbEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        mmtbEWK.Scale(normEWK[ptbin])
        mmtb.Add(mmtbEWK, -1)        
        hmetb.append(mmtb)

        
        eff = mmtb.Integral()/mmt.Integral()

        ereff = sqrt(eff*(1-eff)/mmt.Integral())
        print " pt bin ", ptbin, " btag efficiency  from MET = ",eff, " error ",ereff
        effArray.append(eff)
        effErrArray.append(ereff)


        
          ### MET with bveto
        mmtbveto_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MET_InvertedTauIdBveto"+ptbin)])
        mmtbveto_tmp._setLegendStyles()
        mmtbveto_tmp._setLegendLabels()
        mmtbveto_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mmtbveto_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
        mmtbveto = mmtbveto_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        mmtbveto.Scale(normData[ptbin])
#        hmt.append(mt)

        mmtbvetoEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MET_InvertedTauIdBveto"+ptbin)])
        mmtbvetoEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mmtbvetoEWK_tmp._setLegendStyles()
        mmtbvetoEWK_tmp._setLegendLabels()
        mmtbvetoEWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mmtbvetoEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
        mmtbvetoEWK = mmtbvetoEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        mmtbvetoEWK.Scale(normEWK[ptbin])
        mmtbveto.Add(mmtbvetoEWK, -1)        
        hmetbveto.append(mmtbveto)

## normalization  mT(btag/bveto)        
        eff = mmtb.Integral()/mmtbveto.Integral()

        ereff = sqrt(eff*(1-eff)/mmtbveto.Integral())
        print " pt bin ", ptbin, " btag/bveto  efficiency from MET   = ",eff, " error ",ereff
        effBvetoArray.append(eff)
        effErrBvetoArray.append(ereff)

## with MT distribution 
        if False:  
        ###  no MET cut 
            mmtb_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MTInvertedTauIdBtagNoMetCut"+ptbin)])
            mmtb_tmp._setLegendStyles()
            mmtb_tmp._setLegendLabels()
            mmtb_tmp.histoMgr.setHistoDrawStyleAll("P") 
            mmtb_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
            mmtb = mmtb_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
            mmtb.Scale(normData[ptbin])
            #        hmt.append(mt)
            
            mmtbEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MTInvertedTauIdBtagNoMetCut"+ptbin)])
            mmtbEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
            mmtbEWK_tmp._setLegendStyles()
            mmtbEWK_tmp._setLegendLabels()
            mmtbEWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
            mmtbEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
            mmtbEWK = mmtbEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
            mmtbEWK.Scale(normEWK[ptbin])
            mmtb.Add(mmtbEWK, -1)
            
            hmtNoMetBtag.append(mmtb)

        
          ### MET with bvet
            mmtbveto_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MTInvertedTauIdBvetoNoMetCut"+ptbin)])
            mmtbveto_tmp._setLegendStyles()
            mmtbveto_tmp._setLegendLabels()
            mmtbveto_tmp.histoMgr.setHistoDrawStyleAll("P") 
            mmtbveto_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
            mmtbveto = mmtbveto_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
            mmtbveto.Scale(normData[ptbin])
            #        hmt.append(mt)
            
            mmtbvetoEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MTInvertedTauIdBvetoNoMetCut"+ptbin)])
            mmtbvetoEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
            mmtbvetoEWK_tmp._setLegendStyles()
            mmtbvetoEWK_tmp._setLegendLabels()
            mmtbvetoEWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
            mmtbvetoEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
            mmtbvetoEWK = mmtbvetoEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
            mmtbvetoEWK.Scale(normEWK[ptbin])
            mmtbveto.Add(mmtbvetoEWK, -1)        
            hmtNoMetBveto.append(mmtbveto)
            
## normalization  mT(btag/bveto)        

            eff = mmtb.Integral()/mmtbveto.Integral()
            ereff = sqrt(eff*(1-eff)/mmtbveto.Integral())
            print " pt bin ", ptbin, " btag/bveto  efficiency from mt, no met cut  = ",eff, " error ",ereff
            effArrayMtNoMet.append(eff)
            effErrArrayMtNoMet.append(ereff)


        
#############################################
        ###  with MET cut 
        mmtb_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MTInvertedTauIdBtag"+ptbin)])
        mmtb_tmp._setLegendStyles()
        mmtb_tmp._setLegendLabels()
        mmtb_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mmtb_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
        mmtb = mmtb_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        mmtb.Scale(normData[ptbin])
#        hmt.append(mt)

        mmtbEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MTInvertedTauIdBtag"+ptbin)])
        mmtbEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mmtbEWK_tmp._setLegendStyles()
        mmtbEWK_tmp._setLegendLabels()
        mmtbEWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mmtbEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
        mmtbEWK = mmtbEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        mmtbEWK.Scale(normEWK[ptbin])
        mmtb.Add(mmtbEWK, -1)
        hmtBtag.append(mmtb)

        mmtbveto_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MTInvertedTauIdBveto"+ptbin)])
        mmtbveto_tmp._setLegendStyles()
        mmtbveto_tmp._setLegendLabels()
        mmtbveto_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mmtbveto_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
        mmtbveto = mmtbveto_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        mmtbveto.Scale(normData[ptbin])
#        hmt.append(mt)

        mmtbvetoEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MTInvertedTauIdBveto"+ptbin)])
        mmtbvetoEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mmtbvetoEWK_tmp._setLegendStyles()
        mmtbvetoEWK_tmp._setLegendLabels()
        mmtbvetoEWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mmtbvetoEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
        mmtbvetoEWK = mmtbvetoEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        mmtbvetoEWK.Scale(normEWK[ptbin])
        mmtbveto.Add(mmtbvetoEWK, -1)        
        hmtBveto.append(mmtbveto)

## normalization  mT(btag/bveto)        
        eff = mmtb.Integral()/mmtbveto.Integral()

        ereff = sqrt(eff*(1-eff)/mmtbveto.Integral())
        print " pt bin ", ptbin, " btag/bveto  efficiency from mt  = ",eff, " error ",ereff
        effArrayMt.append(eff)
        effErrArrayMt.append(ereff)


        
## sum histo bins     


    met = hmet[0].Clone("met")
    met.SetName("MET")
    met.SetTitle("Inverted tau Met")
    met.Reset()
    print "check met",met.GetEntries()
    for histo in hmet:
        met.Add(histo)

    metb = hmetb[0].Clone("met")
    metb.SetName("MET")
    metb.SetTitle("Inverted tau Met")
    metb.Reset()
    print "check met btagging",metb.GetEntries()
    for histo in hmetb:
        metb.Add(histo)

    metbveto = hmetbveto[0].Clone("met")
    metbveto.SetName("METbveto")
    metbveto.SetTitle("Inverted tau Met")
    metbveto.Reset()
    print "check met bveto",metbveto.GetEntries()
    for histo in hmetbveto:
        metbveto.Add(histo)

## with MT

    if False:   
        mtNoMetBtag = hmtNoMetBtag[0].Clone("mt")
        mtNoMetBtag.SetName("MET")
        mtNoMetBtag.SetTitle("Inverted tau Met")
        mtNoMetBtag.Reset()
        print "check MT btagging",mtNoMetBtag.GetEntries()
        for histo in hmtNoMetBtag:
            mtNoMetBtag.Add(histo)
            
            
        mtNoMetBveto = hmtNoMetBveto[0].Clone("mt")
        mtNoMetBveto.SetName("MET")
        mtNoMetBveto.SetTitle("Inverted tau Met")
        mtNoMetBveto.Reset()
        print "check MT bveto",mtNoMetBveto.GetEntries()
        for histo in hmtNoMetBveto:
            mtNoMetBveto.Add(histo)


    mtBtag = hmtBtag[0].Clone("mt")
    mtBtag.SetName("MET")
    mtBtag.SetTitle("Inverted tau Met")
    mtBtag.Reset()
    print "check MT btagging",mtBtag.GetEntries()
    for histo in hmtBtag:
        mtBtag.Add(histo)

    
    mtBveto = hmtBveto[0].Clone("mt")
    mtBveto.SetName("MET")
    mtBveto.SetTitle("Inverted tau Met")
    mtBveto.Reset()
    print "check MT bveto",mtBveto.GetEntries()
    for histo in hmtBveto:
        mtBveto.Add(histo)

        
##########################################
        ## plotting
    invertedQCD = InvertedTauID()
    invertedQCD.setLumi(datasets.getDataset("Data").getLuminosity())
    
###  effisiency as a function of MET
    metWithBtagging = metb.Clone("MET")
    metWithBtagging.Divide(metbveto)
    BtaggingEffVsMet = metWithBtagging.Clone("Eff")
    invertedQCD.setLabel("BtagToBvetoEffVsMet")
    invertedQCD.mtComparison(BtaggingEffVsMet, BtaggingEffVsMet,"BtagToBvetoEffVsMet")


    if False:
   ###  effisiency as a function of MT
        mtWithBtagging = mtNoMetBtag.Clone("MT")
        mtWithBtagging.Divide(mtNoMetBveto)
        BtaggingEffNoMetVsMt = mtWithBtagging.Clone("Eff")
        invertedQCD.setLabel("BtagToBvetoEffNoMetVsMt")
        invertedQCD.mtComparison(BtaggingEffNoMetVsMt, BtaggingEffNoMetVsMt,"BtagToBvetoEffNoMetVsMt")


    ###  effisiency as a function of MT
    mtWithBtagging = mtBtag.Clone("MT")
    mtWithBtagging.Divide(mtBveto)
    BtaggingEffVsMt = mtWithBtagging.Clone("Eff")
    invertedQCD.setLabel("BtagToBvetoEffVsMt")
    invertedQCD.mtComparison(BtaggingEffVsMt, BtaggingEffVsMt,"BtagToBvetoEffVsMt")
    
 # efficiency metb/met
    metbtag = metb.Clone("metb")
    metnobtag = met.Clone("met")
    metbtag.Divide(metnobtag)
    invertedQCD.setLabel("BtagEffVsMet")
    invertedQCD.mtComparison(metbtag, metbtag,"BtagEffVsMet")

  # efficiency metb/metbveto
    metbtag = metb.Clone("metb")
    metbjetveto = metbveto.Clone("met")
    invertedQCD.setLabel("BtagToBvetoEfficiency")
    invertedQCD.mtComparison(metbtag, metbjetveto,"BtagToBvetoEfficiency")

### Create and customise TGraph
    cEff = TCanvas ("Efficiency", "Efficiency", 1)
    cEff.cd()
    ptbin_error = array.array("d",[5, 5, 5, 5, 10, 10 ,30])
    ptbin = array.array("d",[45, 55, 65, 75, 90, 110 ,150])



    if False:
## no MET cut 
        cEff = TCanvas ("btaggingEffNoMet", "btaggingEffNoMet", 1)
        cEff.cd()     
        graph = TGraphErrors(7, ptbin, array.array("d",effArrayMtNoMet),ptbin_error,array.array("d",effErrArrayMtNoMet))    
        graph.SetMaximum(0.25)
        graph.SetMinimum(0.0)
        graph.SetMarkerStyle(kFullCircle)
        graph.SetMarkerColor(kBlue)
        graph.SetMarkerSize(1)
        graph.GetYaxis().SetTitle("N_{b tagged}/N_{b veto}")
        graph.GetXaxis().SetTitle("p_{T}^{#tau jet} [GeV]")
### Re-draw graph and update canvas and gPad
        graph.Draw("AP")
        tex4 = ROOT.TLatex(0.2,0.955,"8 TeV              19.6 fb^{-1}             CMS preliminary")
        tex4.SetNDC()
        tex4.SetTextSize(20)
        tex4.Draw()
        tex1 = ROOT.TLatex(0.2,0.88,"All selection cuts")
        tex1.SetNDC()
        tex1.SetTextSize(22)
        #    tex1.Draw()
        tex2 = ROOT.TLatex(0.5,0.8,"No MET cut" )
        tex2.SetNDC()
        tex2.SetTextSize(24)
        tex2.Draw()

        cEff.Update()
        cEff.SaveAs("btagToBvetoEffNoMetVsPtTau_mt.png")



## with MET cut 
    cEff = TCanvas ("btaggingEff", "btaggingEff", 1)
    cEff.cd()     
    graph = TGraphErrors(7, ptbin, array.array("d",effArrayMt),ptbin_error,array.array("d",effErrArrayMt))    

    graph.SetMaximum(0.25)
    graph.SetMinimum(0.0)
    graph.SetMarkerStyle(kFullCircle)
    graph.SetMarkerColor(kBlue)
    graph.SetMarkerSize(1)
    graph.GetYaxis().SetTitle("N_{b tagged}/N_{b veto}")
    graph.GetXaxis().SetTitle("p_{T}^{#tau jet} [GeV]")
### Re-draw graph and update canvas and gPad
    graph.Draw("AP")


    tex4 = ROOT.TLatex(0.2,0.955,"8 TeV              19.6 fb^{-1}             CMS preliminary")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    tex1 = ROOT.TLatex(0.2,0.88,"All selection cuts")
    tex1.SetNDC()
    tex1.SetTextSize(22)
#    tex1.Draw()
    tex2 = ROOT.TLatex(0.5,0.8,"After MET cut" )
    tex2.SetNDC()
    tex2.SetTextSize(24)
    tex2.Draw()

    cEff.Update()
    cEff.SaveAs("btagToBvetoEffVsPtTau_mt.png")

## no MET cut 
    cEff = TCanvas ("btaggingEffNoMet", "btaggingEffNoMet", 1)
    cEff.cd()     
    graph = TGraphErrors(7, ptbin, array.array("d",effBvetoArray),ptbin_error,array.array("d",effErrBvetoArray))    
    graph.SetMaximum(0.25)

    graph.SetMinimum(0.0)
    graph.SetMarkerStyle(kFullCircle)
    graph.SetMarkerColor(kBlue)
    graph.SetMarkerSize(1)
    graph.GetYaxis().SetTitle("N_{b tagged}/N_{b veto}")
    graph.GetXaxis().SetTitle("p_{T}^{#tau jet} [GeV]")
### Re-draw graph and update canvas and gPad
    graph.Draw("AP")

    tex4 = ROOT.TLatex(0.2,0.955,"8 TeV              19.6 fb^{-1}             CMS preliminary")


    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    tex1 = ROOT.TLatex(0.2,0.88,"All selection cuts")
    tex1.SetNDC()
    tex1.SetTextSize(22)
#    tex1.Draw()
    tex2 = ROOT.TLatex(0.5,0.8,"No MET cut" )
    tex2.SetNDC()
    tex2.SetTextSize(24)
    tex2.Draw()

    cEff.Update()

    cEff.SaveAs("btagToBvetoEffNoMetVsPtTau.png")



## with MET cut 
    cEff = TCanvas ("btaggingEfficiency", "btaggingEfficiency", 1)
    cEff.cd()     
    graph = TGraphErrors(7, ptbin, array.array("d",effArray),ptbin_error,array.array("d",effErrArray))    
    graph.SetMaximum(0.25)
    graph.SetMinimum(0.0)
    graph.SetMarkerStyle(kFullCircle)
    graph.SetMarkerColor(kBlue)
    graph.SetMarkerSize(1)

    graph.GetYaxis().SetTitle("b-tagging efficiency")

    graph.GetXaxis().SetTitle("p_{T}^{#tau jet} [GeV]")
### Re-draw graph and update canvas and gPad
    graph.Draw("AP")

    tex4 = ROOT.TLatex(0.2,0.955,"8 TeV              19.6 fb^{-1}             CMS preliminary")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()

    tex1 = ROOT.TLatex(0.4,0.85,"Inverted #tau identification")
    tex1.SetNDC()
    tex1.SetTextSize(22)
    tex1.Draw()
    tex2 = ROOT.TLatex(0.4,0.78,"At least 3 jets" )

    tex2.SetNDC()
    tex2.SetTextSize(24)
    tex2.Draw()

    cEff.Update()
    cEff.SaveAs("btaggingEffVsPtTau.png")


##################################3
    
    fOUT = open("btaggingFactors","w")

    #    now = datetime.datetime.now()
    
#    fOUT.write("# Generated on %s\n"%now.ctime())
    fOUT.write("# by %s\n"%os.path.basename(sys.argv[0]))
    fOUT.write("\n")
    fOUT.write("btaggingFactors = {\n")

    i = 0
    while i < len(effArray):
        line = "    \"" + ptbins[i] + "\": " + str(effArray[i])
        if i < len(effArray) - 1:
            line += ","
        line += "\n"
        fOUT.write(line)
        i = i + 1
        
    fOUT.write("}\n")
    fOUT.close()
    print "B-tagging efficiensies written in file","btaggingFactors"    

    

    
    
    fOUT = open("btaggingToBvetoFactors.py","w")

    #    now = datetime.datetime.now()
    
#    fOUT.write("# Generated on %s\n"%now.ctime())
    fOUT.write("# by %s\n"%os.path.basename(sys.argv[0]))
    fOUT.write("\n")
    fOUT.write("btaggingToBvetoFactors = {\n")

    i = 0
    while i < len(effBvetoArray):
        line = "    \"" + ptbins[i] + "\": " + str(effBvetoArray[i])
        if i < len(effBvetoArray) - 1:
            line += ","
        line += "\n"
        fOUT.write(line)
        i = i + 1
        
    fOUT.write("}\n")
    fOUT.close()
    print "BtaggingToBveto efficiensies written in file","btaggingToBvetoFactors"    


    
    fOUT = open("btaggingToBvetoAfterMetFactors.py","w")

    #    now = datetime.datetime.now()
    
#    fOUT.write("# Generated on %s\n"%now.ctime())
    fOUT.write("# by %s\n"%os.path.basename(sys.argv[0]))
    fOUT.write("\n")
    fOUT.write("btaggingToBvetoAfterMetFactors = {\n")

    i = 0
    while i < len(effArrayMt):
        line = "    \"" + ptbins[i] + "\": " + str(effArrayMt[i])
        if i < len(effArrayMt) - 1:
            line += ","
        line += "\n"
        fOUT.write(line)
        i = i + 1
        
    fOUT.write("}\n")
    fOUT.close()
    print "BtaggingToBvetoAfterMet efficiensies written in file","btaggingToBvetoFactors"    
   

    

class AddMassBRText:
    def __init__(self):
        self.mass = 120
        self.br = 0.01
        self.size = 20
        self.separation = 0.04

    def setMass(self, mass):
        self.mass = mass

    def setBR(self, br):
        self.br = br

    def __call__(self, x, y):
        mass = "m_{H^{#pm}} = %d GeV/c^{2}" % self.mass
        br = "BR(t #rightarrow bH^{#pm})=%.2f" % self.br

        histograms.addText(x, y, mass, size=self.size)
        histograms.addText(x, y-self.separation, br, size=self.size)

addMassBRText = AddMassBRText()
    
# Call the main function if the script is executed (i.e. not imported)
if __name__ == "__main__":
    main()
