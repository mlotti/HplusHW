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
#analysis = "signalAnalysisInvertedTauOptQCDTailKillerLoose"
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
dataEra = "Run2011AB"

optMode = "OptQCDTailKillerLoose"

optMode = "OptQCDTailKillerLoose"

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
    datasets = dataset.getDatasetsFromMulticrabDirs(dirs,dataEra=dataEra, searchMode=searchMode, analysisName=analysis, optimizationMode=optMode) 
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
 
    invertedPurities(datasets)



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


def invertedPurities(datasets):
    
    normData,normEWK,normFactorisedData,normFactorisedEWK=normalisation()
    norm_inc,normEWK_inc = normalisationInclusive()

    noDphi = []
    noDphiEWK = []
    Dphi160 = []
    DphiEWK160 = []
    DphiAll = []
    DphiEWKAll = []
    DphiAllremovett = []
    DphiEWKAllremovett = []
    DphiJet1=[]
    DphiEWKJet1=[]
    DphiJet2=[]
    DphiEWKJet2=[]
    hmt = []
    hmtb = [] 
    hmtv = []
    hmtPhiv = []
    hmet = []
    hmetQCD = []
    hmetEWK = []
    hjetmet = []
    hjetmetphi = [] 
    hMHTJet1phi = []
    hmtph = []
    hmtphj1= []
    hmtphj2= []
    hmtremovett = []
    DphiEWKAllbveto= []
    DphiAllbveto= []
    purityMet= []
    purityErrMet= []
    purityMtRemovett = []
    purityErrMtRemovett = []
    purityMtFirstDeltaPhiCut = []
    purityErrMtFirstDeltaPhiCut = []
    purityMtThirdDeltaPhiCut = []
    purityErrMtThirdDeltaPhiCut = [] 
    purityMtSecondDeltaPhiCut = []
    purityErrMtSecondDeltaPhiCut = []
    purityMtDeltaPhiCut = []
    purityErrMtDeltaPhiCut = []
    purityMtAfterBtagging = []
    purityErrMtAfterBtagging = []
    purityMTInvertedTauIdBvetoDphi = []
    purityErrMTInvertedTauIdBvetoDphi = []
    
## histograms in bins, normalisation and substraction of EWK contribution
    ## mt with 2dim deltaPhi cut
    for ptbin in ptbins:
        mt_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MTInvertedSecondDeltaPhiCut"+ptbin)])
        mt_tmp._setLegendStyles()
        mt_tmp._setLegendLabels()
        mt_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mt_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
        mt = mt_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
#        mt.Scale(normData[ptbin])
        DphiJet2.append(mt)
        
        mtEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MTInvertedSecondDeltaPhiCut"+ptbin)])
        mtEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mtEWK_tmp._setLegendStyles()
        mtEWK_tmp._setLegendLabels()
        mtEWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
        mtEWK = mtEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
#        mtEWK.Scale(normEWK[ptbin])
#        mt.Add(mtEWK, -1)
#        hmt.append(mt)
        DphiEWKJet2.append(mtEWK)
        
        purity = -999
        error = -999
        if mt.Integral() > 0:
            purity = (mt.Integral() - mtEWK.Integral())/ mt.Integral()
            error = sqrt(purity*(1-purity)/mt.Integral())
            purityMtSecondDeltaPhiCut.append(purity)
            purityErrMtSecondDeltaPhiCut.append(error)                         
#        print " pt bin ", ptbin, " purity Mt Second Delta Phi Cut    = ",purity, " error ",error

############################################        
               
        # mt after b tagging
        mtb_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MTInvertedTauIdBtag"+ptbin)])
        mtb_tmp._setLegendStyles()
        mtb_tmp._setLegendLabels()
        mtb_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtb_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
        mtb = mtb_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
#        mtb.Scale(normData[ptbin])
        hmt.append(mtb)
        noDphi.append(mtb)
        
        mtbEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MTInvertedTauIdBtag"+ptbin)])
        mtbEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mtbEWK_tmp._setLegendStyles()
        mtbEWK_tmp._setLegendLabels()
        mtbEWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtbEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
        mtbEWK = mtbEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
#        mtbEWK.Scale(normEWK[ptbin])
        mtb.Add(mtbEWK, -1)
        hmtb.append(mtb)
        noDphiEWK.append(mtbEWK)

       
        purity = -999
        error = -999
        if mtb.Integral() > 0:
            purity = (mtb.Integral() - mtbEWK.Integral())/ mtb.Integral()
            error = sqrt(purity*(1-purity)/mtb.Integral())
            purityMtAfterBtagging.append(purity)
            purityErrMtAfterBtagging.append(error)                         
#        print " pt bin ", ptbin, " purity Mt After Btagging    = ",purity, " error ",error 


############################################

        # mt after deltaPhi cut
        mtph_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MTInvertedTauIdJetDphi"+ptbin)])
        mtph_tmp._setLegendStyles()
        mtph_tmp._setLegendLabels()
        mtph_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtph_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
        mtph = mtph_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
#        mtph.Scale(normData[ptbin])
#        hmt.append(mt)
        Dphi160.append(mtph) 
        mtphEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MTInvertedTauIdJetDphi"+ptbin)])
        mtphEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mtphEWK_tmp._setLegendStyles()
        mtphEWK_tmp._setLegendLabels()
        mtphEWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtphEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
        mtphEWK = mtphEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
#        mtphEWK.Scale(normEWK[ptbin])
#        mtph.Add(mtphEWK, -1)
#        hmtph.append(mtph)
        DphiEWK160.append(mtphEWK) 
        purity = -999
        error = -999
        if mtph.Integral() > 0:
            purity = (mtph.Integral() - mtphEWK.Integral())/ mtph.Integral()
            error = sqrt(purity*(1-purity)/mtph.Integral())
            purityMtDeltaPhiCut.append(purity)
            purityErrMtDeltaPhiCut.append(error)                         
#        print " pt bin ", ptbin, " purity Mt DeltaPhi Cut    = ",purity, " error ",error 


############################################


        # mt after deltaphi vs MHTjet1 cut
        mtphj1_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MTInvertedFirstDeltaPhiCut"+ptbin)])
        #mtphj1_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("MTInvertedTauIdMet"+ptbin)])
        mtphj1_tmp._setLegendStyles()
        mtphj1_tmp._setLegendLabels()
        mtphj1_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtphj1_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
        mtphj1 = mtphj1_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
#        mtphj1.Scale(normData[ptbin])
        DphiJet1.append(mtphj1)
        
        mtphj1EWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MTInvertedFirstDeltaPhiCut"+ptbin)])
        #mtphj1EWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("MTInvertedTauIdMet"+ptbin)])
        mtphj1EWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mtphj1EWK_tmp._setLegendStyles()
        mtphj1EWK_tmp._setLegendLabels()
        mtphj1EWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtphj1EWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
        mtphj1EWK = mtphj1EWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
#        mtphj1EWK.Scale(normEWK[ptbin])
#        mtphj1.Add(mtphj1EWK, -1)
#        hmtphj1.append(mtphj1)
        DphiEWKJet1.append(mtphj1EWK)
 
        purity = -999
        error = -999
        if mtphj1.Integral() > 0:
            purity = (mtphj1.Integral() - mtphj1EWK.Integral())/ mtphj1.Integral()
            error = sqrt(purity*(1-purity)/mtphj1.Integral())
            purityMtFirstDeltaPhiCut.append(purity)
            purityErrMtFirstDeltaPhiCut.append(error)                         
#        print " pt bin ", ptbin, " purity Mt First Delta Phi Cut    = ",purity, " error ",error 


############################################
        
        # mt after all cuts
        mtphj2_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MTInvertedThirdDeltaPhiCut"+ptbin)])
        mtphj2_tmp._setLegendStyles()
        mtphj2_tmp._setLegendLabels()
        mtphj2_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtphj2_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
        mtphj2 = mtphj2_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
#        mtphj2.Scale(normData[ptbin])
#        hmt.append(mt)
        DphiAll.append(mtphj2)
        mtphj2EWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MTInvertedThirdDeltaPhiCut"+ptbin)])
        mtphj2EWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mtphj2EWK_tmp._setLegendStyles()
        mtphj2EWK_tmp._setLegendLabels()
        mtphj2EWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtphj2EWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
        mtphj2EWK = mtphj2EWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
#        mtphj2EWK.Scale(normEWK[ptbin])
#        mtphj2.Add(mtphj2EWK, -1)
#        hmtphj2.append(mtphj2)
        DphiEWKAll.append(mtphj2EWK)
        
        purity = -999
        error = -999
        if mtphj2.Integral() > 0:
            purity = (mtphj2.Integral() - mtphj2EWK.Integral())/ mtphj2.Integral()
            error = sqrt(purity*(1-purity)/mtphj2.Integral())
            purityMtThirdDeltaPhiCut.append(purity)
            purityErrMtThirdDeltaPhiCut.append(error)                         
 #       print " pt bin ", ptbin, " purity Mt Third Delta Phi Cut    = ",purity, " error ",error 

        

#######################
       # mt with cut against tt
        mtremovett_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MTInvertedAgainstTTCut"+ptbin)])
        mtremovett_tmp._setLegendStyles()
        mtremovett_tmp._setLegendLabels()
        mtremovett_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtremovett_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
        mtremovett = mtremovett_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
#        mtremovett.Scale(normData[ptbin])
        DphiAllremovett.append(mtremovett) 
     
        mtremovettEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MTInvertedAgainstTTCut"+ptbin)])
        mtremovettEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mtremovettEWK_tmp._setLegendStyles()
        mtremovettEWK_tmp._setLegendLabels()
        mtremovettEWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtremovettEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
        mtremovettEWK = mtremovettEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
#        mtremovettEWK.Scale(normEWK[ptbin])
#        mtremovett.Add(mtremovettEWK, -1)
#        hmtremovett.append(mtremovett)
        DphiEWKAllremovett.append(mtremovettEWK) 
        purity = -999
        error = -999
        if  mtremovett.Integral() > 0:
            purity = (mtremovett.Integral() - mtremovettEWK.Integral())/ mtremovett.Integral()
            error = sqrt(purity*(1-purity)/mtremovett.Integral())
            purityMtRemovett.append(purity)
            purityErrMtRemovett.append(error)                         
            print "mtremovett.Integral() ",mtremovett.Integral(), " mmtEWK.Integral() ",   mtremovettEWK.Integral()      

 #######################   
        

        
        ### MET
        mmt_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MET_InvertedTauIdJets"+ptbin)])
        mmt_tmp._setLegendStyles()
        mmt_tmp._setLegendLabels()
        mmt_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mmt_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
        mmt = mmt_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
##        mmt.Scale(normData[ptbin])
        hmet.append(mmt)
        
        mmtEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MET_InvertedTauIdJets"+ptbin)])
        mmtEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mmtEWK_tmp._setLegendStyles()
        mmtEWK_tmp._setLegendLabels()
        mmtEWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mmtEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
        mmtEWK = mmtEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
##        mmtEWK.Scale(normEWK[ptbin])
        mmt.Add(mmtEWK, -1)
        hmetQCD.append(mmt)
        hmetEWK.append(mmtEWK)

        
        purity = -999
        error = -999
        if mmt.Integral() > 0:
            purity = (mmt.Integral() - mmtEWK.Integral())/ mmt.Integral()
            error = sqrt(purity*(1-purity)/mmt.Integral())
            purityMet.append(purity)
            purityErrMet.append(error)
##            print "mmt.Integral() ",mmt.Integral(), " mmtEWK.Integral() ",   mmtEWK.Integral()




############################################
        
        # mt after all cuts
        mtphj2_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MTInvertedTauIdBvetoDphi"+ptbin)])
        mtphj2_tmp._setLegendStyles()
        mtphj2_tmp._setLegendLabels()
        mtphj2_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtphj2_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
        mtphj2 = mtphj2_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
#        mtphj2.Scale(normData[ptbin])
#        hmt.append(mt)
        DphiAllbveto.append(mtphj2)
        mtphj2EWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MTInvertedTauIdBvetoDphi"+ptbin)])
        mtphj2EWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mtphj2EWK_tmp._setLegendStyles()
        mtphj2EWK_tmp._setLegendLabels()
        mtphj2EWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtphj2EWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
        mtphj2EWK = mtphj2EWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
#        mtphj2EWK.Scale(normEWK[ptbin])
#        mtphj2.Add(mtphj2EWK, -1)
#        hmtphj2.append(mtphj2)
        DphiEWKAllbveto.append(mtphj2EWK)
        
        purity = -999
        error = -999
        if mtphj2.Integral() > 0:
            purity = (mtphj2.Integral() - mtphj2EWK.Integral())/ mtphj2.Integral()
            error = sqrt(purity*(1-purity)/mtphj2.Integral())
            purityMTInvertedTauIdBvetoDphi.append(purity)
            purityErrMTInvertedTauIdBvetoDphi.append(error)                         
 #       print " pt bin ", ptbin, " purity Mt Third Delta Phi Cut    = ",purity, " error ",error 



    print " "        
    print " purity met   = ",purityMet, " error ",purityErrMet
    print " purity Mt no DeltaPhi Cuts    = ",purityMtAfterBtagging, " error ",purityErrMtAfterBtagging
    print " purity Mt DeltaPhi160 Cut    = ",purityMtDeltaPhiCut, " error ",purityErrMtDeltaPhiCut
    print " purity Mt First DeltaPhi Cut    = ",purityMtFirstDeltaPhiCut, " error ",purityErrMtFirstDeltaPhiCut
    print " purity Mt Second DeltaPhi Cut    = ",purityMtSecondDeltaPhiCut, " error ",purityErrMtSecondDeltaPhiCut 
    print " purity Mt Third Delta Phi Cut    = ",purityMtThirdDeltaPhiCut, " error ",purityErrMtThirdDeltaPhiCut
    print " purity Mt b veto deltaPhi Cuts    = ",purityMTInvertedTauIdBvetoDphi, " error ",purityErrMTInvertedTauIdBvetoDphi
    print " purity Mt Remove tt    = ",purityMtRemovett, " error ",purityErrMtRemovett



    invertedQCD = InvertedTauID()
    invertedQCD.setLumi(datasets.getDataset("Data").getLuminosity())


### Met
    met = hmet[0].Clone("met")
    met.SetName("MET")
    met.SetTitle("Inverted tau Met")
    met.Reset()
    for histo in hmet:
        met.Add(histo)

    metQCD = hmetQCD[0].Clone("met")
    metQCD.SetName("MET")
    metQCD.SetTitle("Inverted tau Met")
    metQCD.Reset()
    for histo in hmetQCD:
        metQCD.Add(histo)
        
    metEWK = hmetEWK[0].Clone("metewk")
    metEWK.SetName("METewk")
    metEWK.SetTitle("Inverted tau Met")
    metEWK.Reset()
    for histo in hmetEWK:
        metEWK.Add(histo)

   
 ### Mt no DeltaPhi Cuts
    mtNoDphi = noDphi[0].Clone("mt")
    mtNoDphi.SetName("mt")
    mtNoDphi.SetTitle("Inverted tau Mt")
    mtNoDphi.Reset()
    for histo in noDphi:
        mtNoDphi.Add(histo)
        
    mtNoDphiEWK = noDphiEWK[0].Clone("mtewk")
    mtNoDphiEWK.SetName("MTewk")
    mtNoDphiEWK.SetTitle("Inverted tau Met")
    mtNoDphiEWK.Reset()
    for histo in noDphiEWK:
        mtNoDphiEWK.Add(histo)
        
 
 ### Mt DeltaPhi < 160 Cut
    mtDphi160 = Dphi160[0].Clone("mt")
    mtDphi160.SetName("mt")
    mtDphi160.SetTitle("Inverted tau Mt")
    mtDphi160.Reset()
    for histo in Dphi160:
        mtDphi160.Add(histo)
        
    mtDphi160EWK = DphiEWK160[0].Clone("mtewk")
    mtDphi160EWK.SetName("MTewk")
    mtDphi160EWK.SetTitle("Inverted tau Met")
    mtDphi160EWK.Reset()
    for histo in DphiEWK160:
        mtDphi160EWK.Add(histo)


 ### Mt Mt all dphi cuts 
    mtDphiAll = DphiAll[0].Clone("mt")
    mtDphiAll.SetName("mt")
    mtDphiAll.SetTitle("Inverted tau Mt")
    mtDphiAll.Reset()
    for histo in DphiAll:
        mtDphiAll.Add(histo)
        
    mtDphiAllEWK = DphiEWKAll[0].Clone("mtewk")
    mtDphiAllEWK.SetName("MTewk")
    mtDphiAllEWK.SetTitle("Inverted tau Met")
    mtDphiAllEWK.Reset()
    for histo in DphiEWKAll:
        mtDphiAllEWK.Add(histo)


 ### Mt bveto all dphi cuts 
    mtDphiAllbveto = DphiAllbveto[0].Clone("mt")
    mtDphiAllbveto.SetName("mt")
    mtDphiAllbveto.SetTitle("Inverted tau Mt")
    mtDphiAllbveto.Reset()
    for histo in DphiAllbveto:
        mtDphiAllbveto.Add(histo)
        
    mtDphiAllEWKbveto = DphiEWKAllbveto[0].Clone("mtewk")
    mtDphiAllEWKbveto.SetName("MTewk")
    mtDphiAllEWKbveto.SetTitle("Inverted tau Met")
    mtDphiAllEWKbveto.Reset()
    for histo in DphiEWKAllbveto:
        mtDphiAllEWKbveto.Add(histo)

        
### Mt Mt dphi jet1 
    mtDphiJet1 = DphiJet1[0].Clone("mt")
    mtDphiJet1.SetName("mt")
    mtDphiJet1.SetTitle("Inverted tau Mt")
    mtDphiJet1.Reset()
    for histo in DphiJet1:
        mtDphiJet1.Add(histo)
        
    mtDphiEWKJet1 = DphiEWKJet1[0].Clone("mtewk")
    mtDphiEWKJet1.SetName("MTewk")
    mtDphiEWKJet1.SetTitle("Inverted tau Met")
    mtDphiEWKJet1.Reset()
    for histo in DphiEWKJet1:
        mtDphiEWKJet1.Add(histo)
        
### Mt Mt dphi jet2 
    mtDphiJet2 = DphiJet2[0].Clone("mt")
    mtDphiJet2.SetName("mt")
    mtDphiJet2.SetTitle("Inverted tau Mt")
    mtDphiJet2.Reset()
    for histo in DphiJet2:
        mtDphiJet2.Add(histo)
        
    mtDphiEWKJet2 = DphiEWKJet2[0].Clone("mtewk")
    mtDphiEWKJet2.SetName("MTewk")
    mtDphiEWKJet2.SetTitle("Inverted tau Met")
    mtDphiEWKJet2.Reset()
    for histo in DphiEWKJet2:
        mtDphiEWKJet2.Add(histo)
        
### Mt  all dphi + tt cuts 
    mtDphiAllremovett = DphiAllremovett[0].Clone("mt")
    mtDphiAllremovett.SetName("mt")
    mtDphiAllremovett.SetTitle("Inverted tau Mt")
    mtDphiAllremovett.Reset()
    for histo in DphiAllremovett:
        mtDphiAllremovett.Add(histo)
        
    mtDphiAllremovettEWK = DphiEWKAllremovett[0].Clone("mtewk")
    mtDphiAllremovettEWK.SetName("MTewk")
    mtDphiAllremovettEWK.SetTitle("Inverted tau Met")
    mtDphiAllremovettEWK.Reset()
    for histo in DphiEWKAllremovett:
        mtDphiAllremovettEWK.Add(histo)

        

##########################################
  #  met purity
    
    metqcd = metQCD.Clone("metqcd")
    metinv = met.Clone("met")
    invertedQCD.setLabel("MetPurity")
#    invertedQCD.mtComparison(metqcd, metqcd,"MetPurity")
       
##########################################
# mt purity no deltaPhi
    mtQCD = mtNoDphi.Clone("QCD")
    mtQCD.Add(mtNoDphiEWK,-1)
    mtQCD.Divide(mtNoDphi)    
    mtqcd = mtQCD.Clone("mtqcd")
    invertedQCD.setLabel("MtNoDeltaPhiCuts")
    invertedQCD.mtComparison(mtQCD, mtQCD,"MtNoDeltaPhiCuts")
##########################################
# mt purity deltaPhi 160
    mtQCD = mtDphi160.Clone("QCD")
    mtQCD.Add(mtDphi160EWK,-1)
    mtQCD.Divide(mtDphi160)    
    mtqcd = mtQCD.Clone("mtqcd")
    invertedQCD.setLabel("MtDeltaPhi160")
    invertedQCD.mtComparison(mtQCD, mtQCD,"MtDeltaPhi160")
    ##########################################
# mt purity all deltaPhi cuts 
    mtQCD = mtDphiAll.Clone("QCD")
    mtQCD.Add(mtDphiAllEWK,-1)
    mtQCD.Divide(mtDphiAll)    
    mtqcd = mtQCD.Clone("mtqcd")
    invertedQCD.setLabel("MtAllDeltaPhiCuts")
    invertedQCD.mtComparison(mtQCD, mtQCD,"MtAllDeltaPhiCuts")

    ##########################################
# mt bveto purity all deltaPhi cuts
## test
    invertedQCD.setLabel("testMtbveto")
#    invertedQCD.mtComparison(mtDphiAllbveto, mtDphiAllbveto,"testMtbveto")
    invertedQCD.setLabel("testEWKMtbveto")
#    invertedQCD.mtComparison(mtDphiAllEWKbveto, mtDphiAllEWKbveto,"testEWKMtbveto")
    
    mtQCD = mtDphiAllbveto.Clone("QCD")
    mtQCD.Add(mtDphiAllEWKbveto,-1)
    mtQCD.Divide(mtDphiAllbveto)    
    mtqcd = mtQCD.Clone("mtqcd")
    invertedQCD.setLabel("MtbvetoAllDeltaPhiCuts")
    invertedQCD.mtComparison(mtQCD, mtQCD,"MtbvetoAllDeltaPhiCuts")
    ##########################################
# mt purity jet1 deltaPhi cuts 
    mtQCD = mtDphiJet1.Clone("QCD")
    mtQCD.Add(mtDphiEWKJet1,-1)
    mtQCD.Divide(mtDphiJet1)    
    mtqcd = mtQCD.Clone("mtqcd")
    invertedQCD.setLabel("MtDeltaPhiJet1Cuts")
    invertedQCD.mtComparison(mtQCD, mtQCD,"MtDeltaPhiJet1Cuts")
    ##########################################
# mt purity jet2 deltaPhi cuts 
    mtQCD = mtDphiJet2.Clone("QCD")
    mtQCD.Add(mtDphiEWKJet2,-1)
    mtQCD.Divide(mtDphiJet2)    
    mtqcd = mtQCD.Clone("mtqcd")
    invertedQCD.setLabel("MtDeltaPhiJet2Cuts")
    invertedQCD.mtComparison(mtQCD, mtQCD,"MtDeltaPhiJet2Cuts")
    ##########################################
# mt purity all deltaPhi cuts and against tt cut
    mtQCD = mtDphiAllremovett.Clone("QCD")
    mtQCD.Add(mtDphiAllremovettEWK,-1)
    mtQCD.Divide(mtDphiAllremovett)    
    mtqcd = mtQCD.Clone("mtqcd")
    invertedQCD.setLabel("MtDeltaPhiAndAgainsttt")
    invertedQCD.mtComparison(mtQCD, mtQCD,"MtDeltaPhiAndAgainsttt")
    
#################################################
 ##  purities as a function of pt tau jet
    
### Create and customise TGraph
    cEff = TCanvas ("MetPurity", "MetPurity", 1)
    cEff.cd()
    ptbin_error = array.array("d",[5, 5, 5, 5, 10, 10 ,30])
    ptbin = array.array("d",[45, 55, 65, 75, 90, 110 ,150])


    
    graph = TGraphErrors(7, ptbin, array.array("d",purityMTInvertedTauIdBvetoDphi),ptbin_error,array.array("d",purityErrMTInvertedTauIdBvetoDphi))    
    graph.SetMaximum(1.0)
    graph.SetMinimum(0.6)
    graph.SetMarkerStyle(kFullCircle)
    graph.SetMarkerColor(kBlue)
    graph.SetMarkerSize(1)
    graph.GetYaxis().SetTitle("QCD purity")
    graph.GetXaxis().SetTitle("p_{T}^{#tau jet} [GeV/c]")
### Re-draw graph and update canvas and gPad
    graph.Draw("AP")
    tex4 = ROOT.TLatex(0.2,0.955,"8 TeV              12.2 fb^{-1}             CMS preliminary")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    tex1 = ROOT.TLatex(0.35,0.35,"B-tagging factorisation")
    tex1.SetNDC()
    tex1.SetTextSize(25)
    tex1.Draw()
    tex2 = ROOT.TLatex(0.35,0.27,"#Delta#phi cuts" )
    tex2.SetNDC()
    tex2.SetTextSize(25)
    tex2.Draw()

    cEff.Update()
    cEff.SaveAs("purityMTInvertedTauIdBvetoDphiBins.png")            

  
    graph = TGraphErrors(7, ptbin, array.array("d",purityMet),ptbin_error,array.array("d",purityErrMet))    
    graph.SetMaximum(1.1)
    graph.SetMinimum(0.8)
    graph.SetMarkerStyle(kFullCircle)
    graph.SetMarkerColor(kBlue)
    graph.SetMarkerSize(1)
    graph.GetYaxis().SetTitle("QCD purity")
    graph.GetXaxis().SetTitle("p_{T}^{#tau jet} [GeV/c]")
### Re-draw graph and update canvas and gPad
    graph.Draw("AP")
    tex4 = ROOT.TLatex(0.2,0.955,"8 TeV              12.2 fb^{-1}             CMS preliminary")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    tex1 = ROOT.TLatex(0.35,0.35,"Inverted #tau jet isolation")
    tex1.SetNDC()
    tex1.SetTextSize(20)
    tex1.Draw()
    tex2 = ROOT.TLatex(0.35,0.3,"at least 3 jets" )
    tex2.SetNDC()
    tex2.SetTextSize(25)
    tex2.Draw()

    cEff.Update()
    cEff.SaveAs("purityMetPtBins.png")            
  
## Mt without deltaPhi cuts
    cEff = TCanvas ("MtNoDeltaPhiCutsPurity", "MtNoDeltaPhiCutsPurity", 1)
    cEff.cd()     
    graph = TGraphErrors(7, ptbin, array.array("d",purityMtAfterBtagging),ptbin_error,array.array("d",purityErrMtAfterBtagging))    
    graph.SetMaximum(1.0)
    graph.SetMinimum(0.4)
    graph.SetMarkerStyle(kFullCircle)
    graph.SetMarkerColor(kBlue)
    graph.SetMarkerSize(1)
    graph.GetYaxis().SetTitle("QCD purity")
    graph.GetXaxis().SetTitle("p_{T}^{#tau jet} [GeV]")
### Re-draw graph and update canvas and gPad
    graph.Draw("AP")
    tex4 = ROOT.TLatex(0.2,0.955,"8 TeV              12.2 fb^{-1}             CMS preliminary")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    tex1 = ROOT.TLatex(0.5,0.38,"All selection cuts")
    tex1.SetNDC()
    tex1.SetTextSize(22)
    tex1.Draw()
    tex2 = ROOT.TLatex(0.5,0.3,"no #Delta#phi cuts" )
    tex2.SetNDC()
    tex2.SetTextSize(25)
    tex2.Draw()

    cEff.Update()
    cEff.SaveAs("purityMtNoDeltaPhiCutsBins.png")            
  
## Mt without deltaPhi cuts
    cEff = TCanvas ("MtDeltaPhi160Purity", "MtDeltaPhi160Purity", 1)
    cEff.cd()     
    graph = TGraphErrors(7, ptbin, array.array("d",purityMtDeltaPhiCut),ptbin_error,array.array("d",purityErrMtDeltaPhiCut))    
    graph.SetMaximum(1.0)
    graph.SetMinimum(0.4)
    graph.SetMarkerStyle(kFullCircle)
    graph.SetMarkerColor(kBlue)
    graph.SetMarkerSize(1)
    graph.GetYaxis().SetTitle("QCD purity")
    graph.GetXaxis().SetTitle("p_{T}^{#tau jet} [GeV]")
### Re-draw graph and update canvas and gPad
    graph.Draw("AP")
    tex4 = ROOT.TLatex(0.2,0.955,"8 TeV              12.2 fb^{-1}             CMS preliminary")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    tex1 = ROOT.TLatex(0.5,0.35,"All selection cuts")
    tex1.SetNDC()
    tex1.SetTextSize(24)
    tex1.Draw()
    tex2 = ROOT.TLatex(0.5,0.25,"#Delta#phi(#tau jet,MET) < 160^{o}" )
    tex2.SetNDC()
    tex2.SetTextSize(24)
    tex2.Draw()

    cEff.Update()
    cEff.SaveAs("purityMtDeltaPhi160Bins.png")



## Mt 1st deltaPhi cut
    cEff = TCanvas ("MtFirstDeltaCutPurity", "MtFirstDeltaPhiCutPurity", 1)
    cEff.cd()     
    graph = TGraphErrors(7, ptbin, array.array("d",purityMtFirstDeltaPhiCut),ptbin_error,array.array("d",purityErrMtFirstDeltaPhiCut))    
    graph.SetMaximum(1.0)
    graph.SetMinimum(0.4)
    graph.SetMarkerStyle(kFullCircle)
    graph.SetMarkerColor(kBlue)
    graph.SetMarkerSize(1)
    graph.GetYaxis().SetTitle("QCD purity")
    graph.GetXaxis().SetTitle("p_{T}^{#tau jet} [GeV]")
### Re-draw graph and update canvas and gPad
    graph.Draw("AP")
    tex4 = ROOT.TLatex(0.2,0.955,"8 TeV              12.2 fb^{-1}             CMS preliminary")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    tex1 = ROOT.TLatex(0.4,0.4,"All selection cuts")
    tex1.SetNDC()
    tex1.SetTextSize(24)
    tex1.Draw()
    tex2 = ROOT.TLatex(0.3,0.3,"#Delta#phi(#tau jet,MET) vs #Delta#phi(jet1,MET) cut" )
    tex2.SetNDC()
    tex2.SetTextSize(24)
    tex2.Draw()

    cEff.Update()
    cEff.SaveAs("purityMtFirstDeltaPhiCutBins.png")


## Mt 2nd deltaPhi cut
    cEff = TCanvas ("MtSecondDeltaCutPurity", "MtFirstSecondPhiCutPurity", 1)
    cEff.cd()     
    graph = TGraphErrors(7, ptbin, array.array("d",purityMtSecondDeltaPhiCut),ptbin_error,array.array("d",purityErrMtSecondDeltaPhiCut))    
    graph.SetMaximum(1.0)
    graph.SetMinimum(0.4)
    graph.SetMarkerStyle(kFullCircle)
    graph.SetMarkerColor(kBlue)
    graph.SetMarkerSize(1)
    graph.GetYaxis().SetTitle("QCD purity")
    graph.GetXaxis().SetTitle("p_{T}^{#tau jet} [GeV]")
### Re-draw graph and update canvas and gPad
    graph.Draw("AP")
    tex4 = ROOT.TLatex(0.2,0.955,"8 TeV              12.2 fb^{-1}             CMS preliminary")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    tex1 = ROOT.TLatex(0.2,0.88,"All selection cuts")
    tex1.SetNDC()
    tex1.SetTextSize(22)
    tex1.Draw()
    tex2 = ROOT.TLatex(0.2,0.8,"#Delta#phi(#tau jet,MET) vs #Delta#phi(jet1/2,MET) cuts" )
    tex2.SetNDC()
    tex2.SetTextSize(24)
    tex2.Draw()

    cEff.Update()
    cEff.SaveAs("purityMtSecondDeltaPhiCutBins.png")



    ## Mt 2nd deltaPhi cut
    cEff = TCanvas ("MtThirdDeltaCutPurity", "MtThirdDeltaPhiCutPurity", 1)
    cEff.cd()     
    graph = TGraphErrors(7, ptbin, array.array("d",purityMtThirdDeltaPhiCut),ptbin_error,array.array("d",purityErrMtThirdDeltaPhiCut                            ))    
    graph.SetMaximum(1.0)
    graph.SetMinimum(0.4)
    graph.SetMarkerStyle(kFullCircle)
    graph.SetMarkerColor(kBlue)
    graph.SetMarkerSize(1)
    graph.GetYaxis().SetTitle("QCD purity")
    graph.GetXaxis().SetTitle("p_{T}^{#tau jet} [GeV]")
### Re-draw graph and update canvas and gPad
    graph.Draw("AP")
    tex4 = ROOT.TLatex(0.2,0.955,"8 TeV              12.2 fb^{-1}             CMS preliminary")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    tex1 = ROOT.TLatex(0.2,0.88, "All selection cuts")
    tex1.SetNDC()
    tex1.SetTextSize(22)
    tex1.Draw()
    tex2 = ROOT.TLatex(0.2,0.8,"#Delta#phi(#tau jet,MET) vs #Delta#phi(jet1/2/3,MET) cuts" )
    tex2.SetNDC()
    tex2.SetTextSize(24)
    tex2.Draw()

    cEff.Update()
    cEff.SaveAs("purityMtThirdDeltaPhiCutBins.png")

    
    ## Mt deltaPhi cuts and against tt
    cEff = TCanvas ("MtMtRemovettPurity", "MtMtRemovettPurity", 1)
    cEff.cd()     
    graph = TGraphErrors(7, ptbin, array.array("d",purityMtRemovett),ptbin_error,array.array("d",purityErrMtRemovett))    
    graph.SetMaximum(1.0)
    graph.SetMinimum(0.4)
    graph.SetMarkerStyle(kFullCircle)
    graph.SetMarkerColor(kBlue)
    graph.SetMarkerSize(1)
    graph.GetYaxis().SetTitle("QCD purity")
    graph.GetXaxis().SetTitle("p_{T}^{#tau jet} [GeV]")
### Re-draw graph and update canvas and gPad
    graph.Draw("AP")
    tex4 = ROOT.TLatex(0.2,0.955,"8 TeV              12.2 fb^{-1}             CMS preliminary")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    tex1 = ROOT.TLatex(0.2,0.88, "All selection cuts ")
    tex1.SetNDC()
    tex1.SetTextSize(22)
    tex1.Draw()
    tex2 = ROOT.TLatex(0.2,0.8,"#Delta#phi(#tau jet,MET) vs #Delta#phi(jet1/2/3,MET) cuts" )
    tex2.SetNDC()
    tex2.SetTextSize(22)
    tex2.Draw()
    tex3 = ROOT.TLatex(0.2,0.72,"#Delta#phi cut against tt+jets" )
    tex3.SetNDC()
    tex3.SetTextSize(22)
    tex3.Draw()
    
    cEff.Update()
    cEff.SaveAs("purityMtAgainstttCutBins.png")


        
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
