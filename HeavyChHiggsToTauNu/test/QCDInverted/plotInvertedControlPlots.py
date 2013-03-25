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
    datasets.remove(filter(lambda name: "Hplus_taunu_t-channel" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "Hplus_taunu_tW-channel" in name, datasets.getAllDatasetNames()))
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

# write histograms to file
def writeTransverseMass(datasets_lands):
    mt = plots.DataMCPlot(datasets_lands, "transverseMass")
    mt.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
    f = ROOT.TFile.Open(output, "RECREATE")
    mt_data = mt.histoMgr.getHisto("Data").getRootHisto().Clone("mt_data")
    mt_data.SetDirectory(f)
    mt_hw = mt.histoMgr.getHisto("TTToHplusBWB_M120").getRootHisto().Clone("mt_hw")
    mt_hw.SetDirectory(f)
    mt_hh = mt.histoMgr.getHisto("TTToHplusBHminusB_M120").getRootHisto().Clone("mt_hh")
    mt_hh.SetDirectory(f)
    f.Write()
    f.Close()


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


try:   
    from QCDInvertedBtaggingToBvetoAfterMetFactors  import *
except ImportError:   
    print
    print "    WARNING, QCDInvertedBtaggingToBvetoAfterMetFactors.py not found!"
    print

    
try:  
    from QCDInvertedBtaggingtoBvetoFactors import *
except ImportError:   
    print
    print "    WARNING, QCDInvertedBtaggingtoBvetoFactors.py not found!"
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
    
    normBtagToBveto = {}
    normBtagToBvetoEWK = {}
    print "-------------------"
#    print "btaggingFactors ", btaggingToBvetoAfterMetFactors
    print "-------------------"
    norm_inc = QCDInvertedNormalization["inclusive"]
    normEWK_inc = QCDInvertedNormalization["inclusiveEWK"]    
    normFactorised_inc = norm_inc  * btaggingFactors["inclusive"]
    normFactorisedEWK_inc = normEWK_inc * btaggingFactors["inclusive"]

    normBtagToBveto_inc = norm_inc  * btaggingFactors["inclusive"]
    normBtagToBvetoEWK_inc = normEWK_inc * btaggingFactors["inclusive"]
    
    for bin in ptbins: 
        normData[bin] = QCDInvertedNormalization[bin]
        normEWK[bin] = QCDInvertedNormalization[bin+"EWK"]
        normFactorisedData[bin] = QCDInvertedNormalization[bin] *  btaggingFactors[bin]
        normFactorisedEWK[bin] = QCDInvertedNormalization[bin+"EWK"] * btaggingFactors[bin]
        #normBtagToBveto[bin] = QCDInvertedNormalization[bin] *  btaggingToBvetoFactors[bin]
        #normBtagToBvetoEWK[bin] = QCDInvertedNormalization[bin+"EWK"] * btaggingToBvetoFactors[bin]
        normBtagToBveto[bin] = QCDInvertedNormalization[bin] *  btaggingToBvetoAfterMetFactors[bin]
        normBtagToBvetoEWK[bin] = QCDInvertedNormalization[bin+"EWK"] * btaggingToBvetoAfterMetFactors[bin]
    print "inclusive norm", norm_inc,normEWK_inc
    print "norm factors", normData
    print "norm factors EWK", normEWK
    
    print "inclusive factorised norm", normFactorised_inc,normFactorisedEWK_inc
    print "norm factors factorised", normFactorisedData
    print "norm factors EWK factorised", normFactorisedEWK
    
    print "inclusive BtagToBveto  norm", normBtagToBveto_inc,normBtagToBvetoEWK_inc
    print "norm factors BtagToBveto ", normBtagToBveto
    print "norm factors EWK BtagToBveto ", normBtagToBvetoEWK
    
             
    return normData,normEWK,normFactorisedData,normFactorisedEWK,normBtagToBveto,normBtagToBvetoEWK


def normalisationInclusive():
 
    norm_inc = QCDInvertedNormalization["inclusive"]
    normEWK_inc = QCDInvertedNormalization["inclusiveEWK"]
              
    print "inclusive norm", norm_inc,normEWK_inc       
    return norm_inc,normEWK_inc 


def controlPlots(datasets):
    
    normData,normEWK,normFactorisedData,normFactorisedEWK,normBtagToBveto,normBtagToBvetoEWK=normalisation()
    norm_inc,normEWK_inc = normalisationInclusive()


    hmt = []
    hmtb = [] 
    hmtv = []
    hmtPhiv = []
    hmet = []
    hdeltaPhi = []
    hmass = []
    hbjet = []
    hjetmet = []
    hjetmetphi = [] 
    hjet = []
    hphi2 = []
    hMHTJet1phi = []
    hmtph = []
    hmtphj1= []
    hmtphj2= []
    hmtremovett = []
    hmtfac = []
    hmtvetoNor= []
    hmtPhivetoNor = []
    
## histograms in bins, normalisation and substraction of EWK contribution
    ## mt with 2dim deltaPhi cut
    for ptbin in ptbins:
        mt_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MTInvertedSecondDeltaPhiCut"+ptbin)])
        #mt_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("MTInvertedTauIdPhi"+ptbin)])
        mt_tmp._setLegendStyles()
        mt_tmp._setLegendLabels()
        mt_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mt_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mt = mt_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        mt.Scale(normData[ptbin])
#        hmt.append(mt)        
        mtEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MTInvertedSecondDeltaPhiCut"+ptbin)])
        #mtEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("MTInvertedTauIdPhi"+ptbin)])
        mtEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mtEWK_tmp._setLegendStyles()
        mtEWK_tmp._setLegendLabels()
        mtEWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mtEWK = mtEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        mtEWK.Scale(normEWK[ptbin])
        mt.Add(mtEWK, -1)
        hmt.append(mt)

        ##  mt with factorised b tagging
        mtfac_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MTInvertedNoBtaggingDphiCuts"+ptbin)])
        mtfac_tmp._setLegendStyles()
        mtfac_tmp._setLegendLabels()
        mtfac_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtfac_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mtfac = mtfac_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        mtfac.Scale(normFactorisedData[ptbin])
        mtfac.Scale(normData[ptbin])
        
#        hmtfac.append(mt)        
        mtfacEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MTInvertedNoBtaggingDphiCuts"+ptbin)])
        mtfacEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mtfacEWK_tmp._setLegendStyles()
        mtfacEWK_tmp._setLegendLabels()
        mtfacEWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtfacEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mtfacEWK = mtfacEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        mtfacEWK.Scale(normFactorisedEWK[ptbin])
        mtfac.Add(mtfacEWK, -1)
#        mtfac.Add(mtEWK, -1)        
        hmtfac.append(mtfac)

        
        # mt after b tagging, no deltaPhi cuts
        mtb_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MTInvertedTauIdBtag"+ptbin)])
        mtb_tmp._setLegendStyles()
        mtb_tmp._setLegendLabels()
        mtb_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtb_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mtb = mtb_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        mtb.Scale(normData[ptbin])
#        hmt.append(mt)        
        mtbEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MTInvertedTauIdBtag"+ptbin)])
        mtbEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mtbEWK_tmp._setLegendStyles()
        mtbEWK_tmp._setLegendLabels()
        mtbEWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtbEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mtbEWK = mtbEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        mtbEWK.Scale(normEWK[ptbin])
        mtb.Add(mtbEWK, -1)
        hmtb.append(mtb)

        # mt after deltaPhi cut
        mtph_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MTInvertedTauIdJetDphi"+ptbin)])
        mtph_tmp._setLegendStyles()
        mtph_tmp._setLegendLabels()
        mtph_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtph_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mtph = mtph_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        mtph.Scale(normData[ptbin])
#        hmt.append(mt)        
        mtphEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MTInvertedTauIdJetDphi"+ptbin)])
        mtphEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mtphEWK_tmp._setLegendStyles()
        mtphEWK_tmp._setLegendLabels()
        mtphEWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtphEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mtphEWK = mtphEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        mtphEWK.Scale(normEWK[ptbin])
        mtph.Add(mtphEWK, -1)
        hmtph.append(mtph)

        # mt after deltaphi vs MHTjet1 cut
        mtphj1_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MTInvertedFirstDeltaPhiCut"+ptbin)])
        #mtphj1_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("MTInvertedTauIdMet"+ptbin)])
        mtphj1_tmp._setLegendStyles()
        mtphj1_tmp._setLegendLabels()
        mtphj1_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtphj1_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mtphj1 = mtphj1_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        mtphj1.Scale(normData[ptbin])
#        hmt.append(mt)        
        mtphj1EWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MTInvertedFirstDeltaPhiCut"+ptbin)])
        #mtphj1EWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("MTInvertedTauIdMet"+ptbin)])
        mtphj1EWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mtphj1EWK_tmp._setLegendStyles()
        mtphj1EWK_tmp._setLegendLabels()
        mtphj1EWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtphj1EWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mtphj1EWK = mtphj1EWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        mtphj1EWK.Scale(normEWK[ptbin])
        mtphj1.Add(mtphj1EWK, -1)
        hmtphj1.append(mtphj1)

        
        # mt after all cuts
        mtphj2_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MTInvertedThirdDeltaPhiCut"+ptbin)])
#        mtphj2_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("MTInvertedTauIdTopMass"+ptbin)])
        mtphj2_tmp._setLegendStyles()
        mtphj2_tmp._setLegendLabels()
        mtphj2_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtphj2_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mtphj2 = mtphj2_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        mtphj2.Scale(normData[ptbin])
#        hmt.append(mt)        
        mtphj2EWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MTInvertedThirdDeltaPhiCut"+ptbin)])
       # mtphj2EWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("MTInvertedTauIdTopMass"+ptbin)])
        mtphj2EWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mtphj2EWK_tmp._setLegendStyles()
        mtphj2EWK_tmp._setLegendLabels()
        mtphj2EWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtphj2EWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mtphj2EWK = mtphj2EWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        mtphj2EWK.Scale(normEWK[ptbin])
        mtphj2.Add(mtphj2EWK, -1)
        hmtphj2.append(mtphj2)

#######################
       # mt with cut against tt
        mtremovett_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MTInvertedAgainstTTCut"+ptbin)])
#        mtphj2_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("MTInvertedTauIdTopMass"+ptbin)])
        mtremovett_tmp._setLegendStyles()
        mtremovett_tmp._setLegendLabels()
        mtremovett_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtremovett_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mtremovett = mtremovett_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        mtremovett.Scale(normData[ptbin])
#        hmt.append(mt)        
        mtremovettEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MTInvertedAgainstTTCut"+ptbin)])
       # mtphj2EWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("MTInvertedTauIdTopMass"+ptbin)])
        mtremovettEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mtremovettEWK_tmp._setLegendStyles()
        mtremovettEWK_tmp._setLegendLabels()
        mtremovettEWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtremovettEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mtremovettEWK = mtremovettEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        mtremovettEWK.Scale(normEWK[ptbin])
        mtremovett.Add(mtremovettEWK, -1)
        hmtremovett.append(mtremovett)
 #######################   
                
        ## mt with b veto cut
        mtv_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MTInvertedTauIdBveto"+ptbin)])
        mtv_tmp._setLegendStyles()
        mtv_tmp._setLegendLabels()
        mtv_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtv_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mtv = mtv_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        mtv.Scale(normData[ptbin])
#        hmt.append(mt)        
        mtEWKv_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MTInvertedTauIdBveto"+ptbin)])
        mtEWKv_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mtEWKv_tmp._setLegendStyles()
        mtEWKv_tmp._setLegendLabels()
        mtEWKv_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtEWKv_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mtEWKv = mtEWKv_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        mtEWKv.Scale(normEWK[ptbin])
        mtv.Add(mtEWKv, -1)
        hmtv.append(mtv)
#        hmt.append(mt)
# mt b veto with Dphi cut 
        mtPhiv_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MTInvertedTauIdBvetoDphi"+ptbin)])
        mtPhiv_tmp._setLegendStyles()
        mtPhiv_tmp._setLegendLabels()
        mtPhiv_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtPhiv_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mtPhiv = mtPhiv_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        mtPhiv.Scale(normData[ptbin])
        mtPhiEWKv_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MTInvertedTauIdBvetoDphi"+ptbin)])
        mtPhiEWKv_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mtPhiEWKv_tmp._setLegendStyles()
        mtPhiEWKv_tmp._setLegendLabels()
        mtPhiEWKv_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtPhiEWKv_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mtPhiEWKv = mtPhiEWKv_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        mtPhiEWKv.Scale(normEWK[ptbin])
        mtPhiv.Add(mtPhiEWKv, -1)
        hmtPhiv.append(mtPhiv)


 #######################   
                
        ## mt with b veto cut and NORMALISATION
        mtveto_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MTInvertedTauIdBveto"+ptbin)])
        mtveto_tmp._setLegendStyles()
        mtveto_tmp._setLegendLabels()
        mtveto_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtveto_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mtvetoNor = mtveto_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        mtvetoNor.Scale(normBtagToBveto[ptbin])
        ## test!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! normalize with 0.138
#        mtvetoNor.Scale(normData[ptbin])
#        mtvetoNor.Scale(0.17)
#        hmt.append(mt)        
        mtEWKveto_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MTInvertedTauIdBveto"+ptbin)])
        mtEWKveto_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mtEWKveto_tmp._setLegendStyles()
        mtEWKveto_tmp._setLegendLabels()
        mtEWKveto_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtEWKveto_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mtEWKvetoNor = mtEWKveto_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        mtEWKvetoNor.Scale(normBtagToBvetoEWK[ptbin])
#        mtEWKvetoNor.Scale(normEWK[ptbin])
#        mtEWKvetoNor.Scale(0.5576)
        mtvetoNor.Add(mtEWKvetoNor, -1)
        hmtvetoNor.append(mtvetoNor)
#        hmt.append(mt)

# mt b veto with Dphi cut 
        mtPhiveto_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MTInvertedTauIdBvetoDphi"+ptbin)])
        mtPhiveto_tmp._setLegendStyles()
        mtPhiveto_tmp._setLegendLabels()
        mtPhiveto_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtPhiveto_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mtPhivetoNor = mtPhiveto_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        mtPhivetoNor.Scale(normBtagToBveto[ptbin])
#        mtPhivetoNor.Scale(normData[ptbin])
#        mtPhivetoNor.Scale(0.17)

        
        mtPhiEWKveto_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MTInvertedTauIdBvetoDphi"+ptbin)])
        mtPhiEWKveto_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mtPhiEWKveto_tmp._setLegendStyles()
        mtPhiEWKveto_tmp._setLegendLabels()
        mtPhiEWKveto_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtPhiEWKveto_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mtPhiEWKvetoNor = mtPhiEWKveto_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        mtPhiEWKvetoNor.Scale(normBtagToBvetoEWK[ptbin])
#        mtPhiEWKvetoNor.Scale(normEWK[ptbin])
#        mtPhiEWKvetoNor.Scale(0.5576)
        mtPhivetoNor.Add(mtPhiEWKvetoNor, -1)
        hmtPhivetoNor.append(mtPhivetoNor)  
########################################
        
        ### MET
        mmt_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MET_InvertedTauIdJets"+ptbin)])
        mmt_tmp._setLegendStyles()
        mmt_tmp._setLegendLabels()
        mmt_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mmt_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))
        mmt = mmt_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        mmt.Scale(normData[ptbin])
#        hmt.append(mt)

#        mmtEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("MTInvertedTauIdPhi"+ptbin)])
        mmtEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MET_InvertedTauIdJets"+ptbin)])
        mmtEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mmtEWK_tmp._setLegendStyles()
        mmtEWK_tmp._setLegendLabels()
        mmtEWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mmtEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))
        mmtEWK = mmtEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        mmtEWK.Scale(normEWK[ptbin])
        mmt.Add(mmtEWK, -1)
        hmet.append(mmt)

        #### deltaPhi
        fmt_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/DeltaPhiInverted"+ptbin)])
        fmt_tmp._setLegendStyles()
        fmt_tmp._setLegendLabels()
        fmt_tmp.histoMgr.setHistoDrawStyleAll("P") 
        fmt_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))
        fmt = fmt_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        fmt.Scale(normData[ptbin])
#        hmt.append(mt)        
        fmtEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/DeltaPhiInverted"+ptbin)])
        fmtEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        fmtEWK_tmp._setLegendStyles()
        fmtEWK_tmp._setLegendLabels()
        fmtEWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
        fmtEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))
        fmtEWK = fmtEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        fmtEWK.Scale(normEWK[ptbin])
        fmt.Add(fmtEWK, -1)
        hdeltaPhi.append(fmt)

        ###### Higgs mass
        hmt_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/HiggsMass4050")])

#        hmt_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("HiggsMass"+ptbin)])
        hmt_tmp._setLegendStyles()
        hmt_tmp._setLegendLabels()
        hmt_tmp.histoMgr.setHistoDrawStyleAll("P") 
        hmt_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))
        mass = hmt_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        mass.Scale(normData[ptbin])
#        hmt.append(mt)
        hmtEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/HiggsMass4050")])
#        hmtEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("HiggsMass"+ptbin)])
        hmtEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        hmtEWK_tmp._setLegendStyles()
        hmtEWK_tmp._setLegendLabels()
        hmtEWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
        hmtEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))
        massEWK = hmtEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        massEWK.Scale(normEWK[ptbin])
        mass.Add(massEWK, -1)
        hmass.append(mass)

        bmt_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/NBInvertedTauIdJet"+ptbin)])
        bmt_tmp._setLegendStyles()
        bmt_tmp._setLegendLabels()
        bmt_tmp.histoMgr.setHistoDrawStyleAll("P") 
        bmt_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))
        bmt = bmt_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        bmt.Scale(normData[ptbin])
#        hmt.append(mt)        
        bmtEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/NBInvertedTauIdJet"+ptbin)])
        bmtEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        bmtEWK_tmp._setLegendStyles()
        bmtEWK_tmp._setLegendLabels()
        bmtEWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
        bmtEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))
        bmtEWK = bmtEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        bmtEWK.Scale(normEWK[ptbin])
        bmt.Add(bmtEWK, -1)
        hbjet.append(bmt)


        jmt_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/NJetInvertedTauId"+ptbin)])
        jmt_tmp._setLegendStyles()
        jmt_tmp._setLegendLabels()
        jmt_tmp.histoMgr.setHistoDrawStyleAll("P") 
        jmt_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))
        jmt = jmt_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        jmt.Scale(normData[ptbin])
#        hmt.append(mt)        
        jmtEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/NJetInvertedTauId"+ptbin)])
        jmtEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        jmtEWK_tmp._setLegendStyles()
        jmtEWK_tmp._setLegendLabels()
        jmtEWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
        jmtEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))
        jmtEWK = jmtEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        jmtEWK.Scale(normEWK[ptbin])
        jmt.Add(jmtEWK, -1)
        hjet.append(jmt)

        
        jmmt_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/NJetInvertedTauIdMet"+ptbin)])
        jmmt_tmp._setLegendStyles()
        jmmt_tmp._setLegendLabels()
        jmmt_tmp.histoMgr.setHistoDrawStyleAll("P") 
        jmmt_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))
        jmmt = jmmt_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        jmmt.Scale(normData[ptbin])
#        hmt.append(mt)        
        jmmtEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/NJetInvertedTauIdMet"+ptbin)])
        jmmtEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        jmmtEWK_tmp._setLegendStyles()
        jmmtEWK_tmp._setLegendLabels()
        jmmtEWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
        jmmtEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))
        jmmtEWK = jmmtEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        jmmtEWK.Scale(normEWK[ptbin])
        jmmt.Add(jmmtEWK, -1)
        hjetmet.append(jmmt)


        if True:
            # DeltaPhi Vs DeltaPhiMHTJet1Inverted
            MHTJet1phi_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/DeltaPhiVsDeltaPhiMETJet1"+ptbin)])
            MHTJet1phi_tmp._setLegendStyles()
            MHTJet1phi_tmp._setLegendLabels()
            MHTJet1phi_tmp.histoMgr.setHistoDrawStyleAll("P") 
            MHTJet1phi_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))
            MHTJet1phi = MHTJet1phi_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
            MHTJet1phi.Scale(normData[ptbin])
            #        hmt.append(mt)        
            MHTJet1phiEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/DeltaPhiVsDeltaPhiMETJet1"+ptbin)])
            MHTJet1phiEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
            MHTJet1phiEWK_tmp._setLegendStyles()
            MHTJet1phiEWK_tmp._setLegendLabels()
            MHTJet1phiEWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
            MHTJet1phiEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))
            MHTJet1phiEWK = MHTJet1phiEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
            MHTJet1phiEWK.Scale(normEWK[ptbin])
            MHTJet1phi.Add(MHTJet1phiEWK, -1)
            hMHTJet1phi.append(MHTJet1phi)
            
## sum histo bins     
    hmtSum = hmt[0].Clone("mtSum")
    hmtSum.SetName("transverseMass")
    hmtSum.SetTitle("Inverted tau ID")
    hmtSum.Reset()
    print "check hmtsum",hmtSum.GetEntries()
    for histo in hmt:
        hmtSum.Add(histo)  
    print "Integral with bins - EWK = ",hmtSum.Integral()
#    print "Integral inclusive  = ",hmt.Integral()

# mt with factorisation
    mtFactorised = hmtfac[0].Clone("mtSum")
    mtFactorised.SetName("transverseMass")
    mtFactorised.SetTitle("Inverted tau ID")
    mtFactorised.Reset()
    print "check mtFactorised",mtFactorised.GetEntries()
    for histo in hmtfac:
        mtFactorised.Add(histo)  
    print "Integral with bins - EWK = ",mtFactorised.Integral()

# mt with btagging, no deltaPhi cuts
    hmtSumb = hmtb[0].Clone("mtSumb")
    hmtSumb.SetName("transverseMassBtag")
    hmtSumb.SetTitle("Inverted tau ID")
    hmtSumb.Reset()
    print "check hmtsum",hmtSum.GetEntries()
    for histo in hmtb:
        hmtSumb.Add(histo)  
    print "Integral with bins - EWK = ",hmtSumb.Integral()
#    print "Integral inclusive  = ",hmt.Integral()


    hmtvSum = hmtv[0].Clone("mtVetoSum")
    hmtvSum.SetName("transverseMassBveto")
    hmtvSum.SetTitle("Inverted tau ID")
    hmtvSum.Reset()
    print "check hmtsum B veto",hmtvSum.GetEntries()
    for histo in hmtv:
        hmtvSum.Add(histo)  
    print "Integral with bins Bveto - EWK  = ",hmtvSum.Integral()

    hmtPhivSum = hmtPhiv[0].Clone("mtPhiVetoSum")
    hmtPhivSum.SetName("transverseMassBveto")
    hmtPhivSum.SetTitle("Inverted tau ID")
    hmtPhivSum.Reset()
    print "check hmtsum phi cutB veto",hmtPhivSum.GetEntries()
    for histo in hmtPhiv:
        hmtPhivSum.Add(histo)  
    print "Integral with bins phi cut Bveto - EWK  = ",hmtPhivSum.Integral()

## mt with bveto normalised
    mtvetoNor = hmtvetoNor[0].Clone("mtVetoSum")
    mtvetoNor.SetName("transverseMassBvetoNor")
    mtvetoNor.SetTitle("Inverted tau ID")
    mtvetoNor.Reset()
    print "check hmtsum B veto norm",mtvetoNor.GetEntries()
    for histo in hmtvetoNor:
        mtvetoNor.Add(histo)  
    print "Integral with bins Bveto normalised- EWK  = ",mtvetoNor.Integral()

## mt with bveto normalised, deltaPhi cuts
    mtPhivetoNor = hmtPhivetoNor[0].Clone("mtVetoSum")
    mtPhivetoNor.SetName("transverseMassBvetoNor")
    mtPhivetoNor.SetTitle("Inverted tau ID")
    mtPhivetoNor.Reset()
    print "check hmtsum B veto norm",mtPhivetoNor.GetEntries()
    for histo in hmtPhivetoNor:
        mtPhivetoNor.Add(histo)  
    print "Integral with bins Bveto Phi normalised- EWK  = ",mtPhivetoNor.Integral()

    
    Againsttt = hmtremovett[0].Clone("mtremovett")
    Againsttt.SetName("transverseMassAgainstTTcut")
    Againsttt.SetTitle("Inverted tau ID")
    Againsttt.Reset()
    print "check hmtsum phi cutB veto",Againsttt.GetEntries()
    for histo in hmtremovett:
        Againsttt.Add(histo)  
    print "Integral with bins phi cut against tt - EWK  = ",Againsttt.Integral()

    met = hmet[0].Clone("met")
    met.SetName("MET")
    met.SetTitle("Inverted tau Met")
    met.Reset()
    print "check met",met.GetEntries()
    for histo in hmet:
        met.Add(histo)
  
    DeltaPhi = hdeltaPhi[0].Clone("deltaPhi")
    DeltaPhi.SetName("deltaPhi")
    DeltaPhi.SetTitle("Inverted tau hdeltaPhi")
    DeltaPhi.Reset()
    print "check hdeltaPhi",DeltaPhi.GetEntries()
    for histo in hdeltaPhi:
        DeltaPhi.Add(histo)
        
    higgsMass = hmass[0].Clone("higgsMass")
    higgsMass.SetName("FullMass")
    higgsMass.SetTitle("Inverted tau higgsMass")
    higgsMass.Reset()
    print "check higgsMass",higgsMass.GetEntries()
    for histo in hmass:
        higgsMass.Add(histo)


    bjet = hbjet[0].Clone("bjet")
    bjet.SetName("NBjets")
    bjet.SetTitle("Inverted tau bjet")
    bjet.Reset()
    print "check bjet",bjet.GetEntries()
    for histo in hbjet:
        bjet.Add(histo)  

    jet = hjet[0].Clone("jet")
    jet.SetName("Njets")
    jet.SetTitle("Inverted tau jet")
    jet.Reset()
    print "check jet",jet.GetEntries()
    for histo in hjet:
        jet.Add(histo)
        

    bjet = hbjet[0].Clone("bjet")
    bjet.SetName("NBjets")
    bjet.SetTitle("Inverted tau bjet")
    bjet.Reset()
    print "check bjet",bjet.GetEntries()
    for histo in hbjet:
        bjet.Add(histo)  

    jetmet = hjetmet[0].Clone("jetmet")
    jetmet.SetName("NjetsAfterMET")
    jetmet.SetTitle("Inverted tau jet after Met")
    jetmet.Reset()
    print "check jetmet",jetmet.GetEntries()
    for histo in hjetmet:
        jetmet.Add(histo)
    if False:
        
        jetmetphi = hjetmetphi[0].Clone("jetmetphi")
        jetmetphi.SetName("DeltaPhiJetMet")
        jetmetphi.SetTitle("Inverted tau deltaphi jet-met")
        jetmetphi.Reset()
        print "check jetmetphi",jetmetphi.GetEntries()
        for histo in hjetmetphi:
            jetmetphi.Add(histo) 

            DeltaPhiJetMet = hphi2[0].Clone("DeltaPhi2")
            DeltaPhiJetMet.SetName("DeltaPhiJetMetVsTauMet")
            DeltaPhiJetMet.SetTitle("Inverted tau deltaphi jet-met vs tau-met")
            DeltaPhiJetMet.Reset()
            print "check jetmetphi",DeltaPhiJetMet.GetEntries()
            for histo in hphi2:
                DeltaPhiJetMet.Add(histo)

    if True:    
        MHTJet1phi = hMHTJet1phi[0].Clone("deltaphiMHTJet1")
        MHTJet1phi.SetName("deltaphiMHTJet1")
        MHTJet1phi.SetTitle("Inverted tau deltaphi vs deltaphiMHTJet1 ")
        MHTJet1phi.Reset()
        print "check jetmetphi",MHTJet1phi.GetEntries()
        for histo in hMHTJet1phi:
            MHTJet1phi.Add(histo)
    
    mtDphiCut = hmtph[0].Clone("mt")
    mtDphiCut.SetName("mtDeltaPhi")
    mtDphiCut.SetTitle("Inverted tau  mt DeltaPhi cut")
    mtDphiCut.Reset()
    print "check jetmetphi",mtDphiCut.GetEntries()
    for histo in hmtph:
        mtDphiCut.Add(histo)
        
    mtHMTjet1Cut = hmtphj1[0].Clone("mtj1")
    mtHMTjet1Cut.SetName("mtDeltaPhiJet1Cut")
    mtHMTjet1Cut.SetTitle("Inverted tau  mt DeltaPhi cut")
    mtHMTjet1Cut.Reset()
    print "check mtHMTjet1Cut ",mtHMTjet1Cut.GetEntries()
    for histo in hmtphj1:
        mtHMTjet1Cut.Add(histo)

    mtHMTjet2Cut = hmtphj2[0].Clone("mtj2")
    mtHMTjet2Cut.SetName("mtDeltaPhiJet2Cut")
    mtHMTjet2Cut.SetTitle("Inverted tau  mt DeltaPhi cut")
    mtHMTjet2Cut.Reset()
    print "check mtHMTjet2Cut ",mtHMTjet2Cut.GetEntries()
    for histo in hmtphj2:
        mtHMTjet2Cut.Add(histo)
        
 ################## Control Plots and comparison with baseline(data-EWK) 

 ## mt without pt bins
            
    mt = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MTInvertedThirdDeltaPhiCut")])
    mtBaseline = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("BaseLine/MTBaseLineTauIdPhi")])
    mtvBaseline = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("BaseLine/MTBaseLineTauIdBveto")])
    mtPhivBaseline = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("BaseLine/MTBaseLineTauIdBvetoDphi")]) 
    mtEWKBaseline = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("BaseLine/MTBaseLineTauIdPhi")])
    mtvEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("BaseLine/MTBaseLineTauIdBveto")]) 
    mtPhivEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("BaseLine/MTBaseLineTauIdBvetoDphi")])
#    jmmtpEWKbaseline = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("ClosestDeltaPhiBaseline")])


     
    mtEWKinverted = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MTInvertedThirdDeltaPhiCut")])
    mtEWKinverted.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mtEWKinverted._setLegendStyles()
    mtEWKinverted._setLegendLabels()
    mtEWKinverted.histoMgr.setHistoDrawStyleAll("P")
    mtEWKinverted.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))  
    hmtEWKinverted = mtEWKinverted.histoMgr.getHisto("EWK").getRootHisto().Clone("Inverted/MTInvertedThirdDeltaPhiCut")
    # norm = Norm_overall *(1-QCDfract) (0.034446/0.87 * 0.13 = 0.0051
    hmtEWKinverted.Scale(normEWK_inc)
    
    mt._setLegendStyles()
    mt._setLegendLabels()
    mt.histoMgr.setHistoDrawStyleAll("P")
    mt.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))  
    hmt = mt.histoMgr.getHisto("Data").getRootHisto().Clone("Inverted/MTInvertedTauIdJetPhi")
    hmt.Scale(norm_inc)



    canvas39 = ROOT.TCanvas("canvas39","",500,500)            
    hmt.SetMarkerColor(4)
    hmt.SetMarkerSize(1)
    hmt.SetMarkerStyle(20)
    hmt.SetFillColor(4)
    hmt.Draw("EP")
    
    hmt_subs = hmt.Clone("QCD")
    hmt_subs.Add(hmtEWKinverted,-1)
    hmt_subs.SetMarkerColor(2)
    hmt_subs.SetMarkerSize(1)
    hmt_subs.SetMarkerStyle(21)
    hmt_subs.Draw("same")

    
    tex2 = ROOT.TLatex(0.55,0.85,"Inverted #tau isolation")
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw()    
    marker2 = ROOT.TMarker(0.5,0.865,hmt.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(hmt.GetMarkerColor())
    marker2.SetMarkerSize(0.9*hmt.GetMarkerSize())
    marker2.Draw()
    
    tex9 = ROOT.TLatex(0.55,0.78,"Inverted-EWK") 
    tex9.SetNDC()
    tex9.SetTextSize(20)
    tex9.Draw()
    marker9 = ROOT.TMarker(0.5,0.795,hmt_subs.GetMarkerStyle())
    marker9.SetNDC()
    marker9.SetMarkerColor(hmt_subs.GetMarkerColor())
    marker9.SetMarkerSize(0.9*hmt_subs.GetMarkerSize())
    marker9.Draw()
    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       5.05 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    hmt.GetYaxis().SetTitleOffset(1.5)
    hmt.GetXaxis().SetTitle("m_{T}(#tau jet, MET) (GeV/c^{2})")
    hmt.GetYaxis().SetTitle("Events / 10 GeV/c^{2}")
    canvas39.Print("transverseMassTest.png")
#    canvas32.Print("transverseMass.C")
    print " "
    print "Integral inclusive = ",hmt.Integral()
    print "Integral inclusive - EWK  = ",hmt_subs.Integral()
    print " "

#################################################
 ##  mT with for deltaPhi < 160 
            
    mtBaseline._setLegendStyles()
    mtBaseline._setLegendLabels()
    mtBaseline.histoMgr.setHistoDrawStyleAll("P")
    mtBaseline.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))  
    hmtBaseline = mtBaseline.histoMgr.getHisto("Data").getRootHisto().Clone("BaseLine/MTBaselineTauIdPhi")
    #hmtBaseline = mtBaseline.histoMgr.getHisto("Data").getRootHisto().Clone("MTBaselineTauIdJetPhi") 
   
    mtEWKBaseline.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mtEWKBaseline._setLegendStyles()
    mtEWKBaseline._setLegendLabels()
    mtEWKBaseline.histoMgr.setHistoDrawStyleAll("P")
    mtEWKBaseline.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))  
#    hmtEWK = mtEWK.histoMgr.getHisto("EWK").getRootHisto().Clone("Inverted/MTInvertedSecondDeltaPhiCut")
    hmtEWK = mtEWKBaseline.histoMgr.getHisto("EWK").getRootHisto().Clone("BaseLine/MTBaselineTauIdPhi")
    

    canvas32 = ROOT.TCanvas("canvas32","",500,500)    
    hmtSum.SetMarkerColor(4)
    hmtSum.SetMarkerSize(1)
    hmtSum.SetMarkerStyle(20)
    hmtSum.SetFillColor(4)
    hmtSum.Draw("EP")
    
    hmtBaseline_QCD = hmtBaseline.Clone("QCD")
    hmtBaseline_QCD.Add(hmtEWK,-1)
    hmtBaseline_QCD.SetMarkerColor(2)
    hmtBaseline_QCD.SetMarkerSize(1)
    hmtBaseline_QCD.SetMarkerStyle(21)
#    hmtBaseline_QCD.Draw("same")            

    tex2 = ROOT.TLatex(0.55,0.85,"Inverted #tau isolation")
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw()
    
    #    tex3 = ROOT.TLatex(0.55,0.75,"#Delta#phi(#tau jet, Met) < 160^{o}")
#    tex3 = ROOT.TLatex(0.55,0.75,"2 Dim #Delta#phi cut")
    tex3 = ROOT.TLatex(0.55,0.75,"#Delta#phi(#tau jet,MET) < 120^{o}")
    tex3.SetNDC()
    tex3.SetTextSize(20)
#    tex3.Draw()
    tex5 = ROOT.TLatex(0.55,0.65,"#Delta#phi(MHT,jet1) > 60^{o}")
    tex5.SetNDC()
    tex5.SetTextSize(20)
 #   tex5.Draw()
    tex6 = ROOT.TLatex(0.5,0.75,"#Delta#phi(MET,jet1/2 / #tau jet) cuts")
#    tex6 = ROOT.TLatex(0.55,0.55,"#Delta#phi(MHT,jet2) > 30^{o}")
    tex6.SetNDC()
    tex6.SetTextSize(20)
    tex6.Draw()    
#    tex3 = ROOT.TLatex(0.55,0.75,"#Delta#phi(#tau jet, Met) < 160^{o}")
#    tex3 = ROOT.TLatex(0.55,0.75,"2 Dim #Delta#phi cut")
#    tex3.SetNDC()
#    tex3.SetTextSize(20)
#    tex3.Draw() 
#    marker2 = ROOT.TMarker(0.5,0.865,hmtSum.GetMarkerStyle())
#    marker2.SetNDC()
#    marker2.SetMarkerColor(hmtSum.GetMarkerColor())
#    marker2.SetMarkerSize(0.9*hmtSum.GetMarkerSize())
#    marker2.Draw()
    
    tex9 = ROOT.TLatex(0.55,0.78,"Baseline: Data-EWK") 
    tex9.SetNDC()
    tex9.SetTextSize(20)
#    tex9.Draw()
    marker9 = ROOT.TMarker(0.5,0.795,hmtBaseline_QCD.GetMarkerStyle())
    marker9.SetNDC()
    marker9.SetMarkerColor(hmtBaseline_QCD.GetMarkerColor())
    marker9.SetMarkerSize(0.9*hmtBaseline_QCD.GetMarkerSize())
#    marker9.Draw()
    
#    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       5.05 fb^{-1}       CMS Preliminary ")
    tex4 = ROOT.TLatex(0.2,0.95,"8 TeV       12.2 fb^{-1}       CMS Preliminary ")    
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    hmtSum.GetYaxis().SetTitleOffset(1.5)
    hmtSum.GetXaxis().SetTitle("m_{T}(#tau jet, MET) (GeV/c^{2})")
    hmtSum.GetYaxis().SetTitle("Events / 20 GeV/c^{2}")
#    canvas32.Print("transverseMass.png")
#    canvas32.Print("transverseMass.C")
    canvas32.Print("transverseMassDeltaPhiVsMETJet2Cut.png")
    canvas32.Print("transverseMassDeltaPhiVsMETJet2Cut.C")
####################################################
# mt after b tagging
    canvas72 = ROOT.TCanvas("canvas72","",500,500)    
    hmtSumb.SetMarkerColor(4)
    hmtSumb.SetMarkerSize(1)
    hmtSumb.SetMarkerStyle(20)
    hmtSumb.SetFillColor(4)
    hmtSumb.Draw("EP")
               

    tex2 = ROOT.TLatex(0.55,0.85,"Inverted #tau isolation")
    tex2.SetNDC()
    tex2.SetTextSize(20)
#    tex2.Draw()
#    tex3 = ROOT.TLatex(0.55,0.75,"#Delta#phi(#tau jet, Met) < 160^{o}")
#    tex3 = ROOT.TLatex(0.55,0.75,"2 Dim #Delta#phi cut")
    tex3 = ROOT.TLatex(0.55,0.85,"No #Delta#phi cuts")
    tex3.SetNDC()
    tex3.SetTextSize(25)
    tex3.Draw() 
    marker2 = ROOT.TMarker(0.5,0.865,hmtSum.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(hmtSum.GetMarkerColor())
    marker2.SetMarkerSize(0.9*hmtSum.GetMarkerSize())
#    marker2.Draw()
    
    
#    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       5.05 fb^{-1}       CMS Preliminary ")
    tex4 = ROOT.TLatex(0.2,0.95,"8 TeV       12.2 fb^{-1}       CMS Preliminary ")    
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    hmtSumb.GetYaxis().SetTitleOffset(1.5)
    hmtSumb.GetXaxis().SetTitle("m_{T}(#tau jet, MET) (GeV/c^{2})")
    hmtSumb.GetYaxis().SetTitle("Events / 20 GeV/c^{2}")
    canvas72.Print("transverseMassAfterBtagging.png")
    canvas72.Print("transverseMassAfterBtagging.C")

####################################################
### comparison plots

 ##  mT with b tagging
    if False:
        mtBaseline._setLegendStyles()
        mtBaseline._setLegendLabels()
        mtBaseline.histoMgr.setHistoDrawStyleAll("P")
        mtBaseline.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))  
        hmtBaseline = mtBaseline.histoMgr.getHisto("Data").getRootHisto().Clone("BaseLine/MTBaselineTauIdPhi")
        
        mtEWKBaseline.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mtEWKBaseline._setLegendStyles()
        mtEWKBaseline._setLegendLabels()
        mtEWKBaseline.histoMgr.setHistoDrawStyleAll("P")
        mtEWKBaseline.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))  
        hmtEWKBaseline = mtEWKBaseline.histoMgr.getHisto("EWK").getRootHisto().Clone("BaseLine/MTBaselineTauIdPhi") 
 
    ##  mT with b veto 
   
    mtvBaseline._setLegendStyles()
    mtvBaseline._setLegendLabels()
    mtvBaseline.histoMgr.setHistoDrawStyleAll("P")
    mtvBaseline.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))  
    hmtvBaseline = mtvBaseline.histoMgr.getHisto("Data").getRootHisto().Clone("BaseLine/MTBaselineTauIdBveto")
    
    mtvEWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mtvEWK._setLegendStyles()
    mtvEWK._setLegendLabels()
    mtvEWK.histoMgr.setHistoDrawStyleAll("P")
    mtvEWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))  
    hmtvEWK = mtvEWK.histoMgr.getHisto("EWK").getRootHisto().Clone("BaseLine/MTBaselineTauIdBveto") 
 
##  mT with b veto and Dphi cut 
   
    mtPhivBaseline._setLegendStyles()
    mtPhivBaseline._setLegendLabels()
    mtPhivBaseline.histoMgr.setHistoDrawStyleAll("P")
    mtPhivBaseline.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))  
    hmtPhivBaseline = mtPhivBaseline.histoMgr.getHisto("Data").getRootHisto().Clone("BaseLine/MTBaselineTauIdBvetoDphi")
    
    mtPhivEWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mtPhivEWK._setLegendStyles()
    mtPhivEWK._setLegendLabels()
    mtPhivEWK.histoMgr.setHistoDrawStyleAll("P")
    mtPhivEWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))  
    hmtPhivEWK = mtPhivEWK.histoMgr.getHisto("EWK").getRootHisto().Clone("BaseLine/MTBaselineTauIdBvetoDphi")
    
   
        
    invertedQCD = InvertedTauID()
    invertedQCD.setLumi(datasets.getDataset("Data").getLuminosity())
      
    hmtBaseline_QCD = hmtBaseline.Clone("QCD")
    hmtBaseline_QCD.Add(hmtEWK,-1)
    hmtvBaseline_QCD = hmtvBaseline.Clone("QCD")
    hmtvBaseline_QCD.Add(hmtvEWK,-1) 
    hmtPhivBaseline_QCD = hmtPhivBaseline.Clone("QCD")
    hmtPhivBaseline_QCD.Add(hmtPhivEWK,-1)
    
# mt inverted-baseline comparison with bveto 
    bveto_inverted = hmtPhivSum.Clone("hmtvSum")
    bveto_baseline = hmtPhivBaseline_QCD.Clone("hmtvBaseline_QCD")
    invertedQCD.setLabel("MtBvetoInvertedVsBaseline")
    invertedQCD.mtComparison(bveto_inverted, bveto_baseline,"BvetoInvertedVsBaseline")

    
# mt inverted-baseline comparison with bveto and deltaPhi cuts
    bvetoDphi_inverted = hmtPhivSum.Clone("hmtPhivSum")
    bvetoDphi_baseline = hmtPhivBaseline_QCD.Clone("hmtPhivBaseline_QCD")
    invertedQCD.setLabel("MtBvetoDphiInvertedVsBaseline")
    invertedQCD.mtComparison(bvetoDphi_inverted, bvetoDphi_baseline,"MtBvetoDphiInvertedVsBaseline")
    
# mt inverted-baseline comparison with btagging and deltaPhi cuts
    btagDphi_inverted = mtHMTjet2Cut.Clone("mtHMTjet2Cut")
    btagDphi_baseline = hmtBaseline_QCD.Clone("hmtBaseline_QCD")
    invertedQCD.setLabel("MtPhiCutBtagInvertedVsBaseline")
    invertedQCD.mtComparison(btagDphi_inverted, btagDphi_baseline,"MtPhiCutBtagInvertedVsBaseline")


    
# mt inverted comparison bveto normalised and  btagging,  deltaPhi cuts
    btagDphi_inverted = mtHMTjet2Cut.Clone("mtHMTjet2Cut")
    bvetoNorDphi_inverted = mtPhivetoNor.Clone("hmtBaseline_QCD")
    invertedQCD.setLabel("MtPhiCutNormalisedBveto")
    invertedQCD.mtComparison(btagDphi_inverted , bvetoNorDphi_inverted,"MtPhiCutNormalisedBveto")



# mt inverted comparison bveto normalised and  btagging,  no deltaPhi cuts
    btag_inverted = hmtSumb.Clone("mtSumb")
    bvetoNor_inverted = mtvetoNor.Clone("hmtBaseline_QCD")
    invertedQCD.setLabel("MtNormalisedBveto")
    invertedQCD.mtComparison(btag_inverted , bvetoNor_inverted,"MtNormalisedBveto")
    
# mt inverted-inverted factorized comparison with btagging and deltaPhi cuts
    btagDphi_inverted = mtHMTjet2Cut.Clone("mtHMTjet2Cut")
    btagDphi_factorised =  mtFactorised.Clone("mtFactorised")
    invertedQCD.setLabel("MtPhiCutBtagInvertedVsFactorised")
#    invertedQCD.mtComparison(btagDphi_inverted, btagDphi_factorised,"BtagDphiInvertedVsFactorised")
   
# mt shape comparison bveto vs btag
    btagged_nor = mtHMTjet2Cut.Clone("mtj2")
    btagged_nor.Scale(1./mtHMTjet2Cut.GetEntries())
    print "btagged_nor",btagged_nor.GetEntries()
    
    bveto_nor = hmtPhivSum.Clone("hmtPhivSum")
    bveto_nor.Scale(1./hmtPhivSum.GetEntries())
    print "bveto_nor",bveto_nor.GetEntries()

    invertedQCD.setLabel("mtBTagVsBvetoInverted")
    invertedQCD.mtComparison(btagged_nor, bveto_nor,"mtBTagVsBvetoInverted")

  
    canvas725 = ROOT.TCanvas("canvas725","",500,500)
    bveto_nor.SetMarkerColor(4)
    bveto_nor.SetMarkerSize(1)
    bveto_nor.SetMarkerStyle(20)
    bveto_nor.SetFillColor(4)
    bveto_nor.Draw("EP")
        
    btagged_nor.SetMarkerColor(2)
    btagged_nor.SetMarkerSize(1)
    btagged_nor.SetMarkerStyle(21)
    btagged_nor.SetFillColor(2)
    btagged_nor.Draw("same")
    
    tex2 = ROOT.TLatex(0.55,0.85,"Inverted #tau isolation")
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw()
#    tex3 = ROOT.TLatex(0.55,0.75,"#Delta#phi(#tau jet, Met) < 160^{o}")
#    tex3 = ROOT.TLatex(0.55,0.75,"2 Dim #Delta#phi cut")
    tex3 = ROOT.TLatex(0.45,0.75,"With b-tagging factorization")
    tex3.SetNDC()
    tex3.SetTextSize(20)
    tex3.Draw() 
    marker2 = ROOT.TMarker(0.4,0.755,mtFactorised.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(mtFactorised.GetMarkerColor())
    marker2.SetMarkerSize(0.9*mtFactorised.GetMarkerSize())
    marker2.Draw()
    tex5 = ROOT.TLatex(0.45,0.65,"No factorization")
    tex5.SetNDC()
    tex5.SetTextSize(20)
    tex5.Draw() 
    marker5 = ROOT.TMarker(0.4,0.655,mtHMTjet2Cut.GetMarkerStyle())
    marker5.SetNDC()
    marker5.SetMarkerColor(mtHMTjet2Cut.GetMarkerColor())
    marker5.SetMarkerSize(0.9*mtHMTjet2Cut.GetMarkerSize())
    marker5.Draw()    
    
#    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       5.05 fb^{-1}       CMS Preliminary ")
    tex4 = ROOT.TLatex(0.2,0.95,"8 TeV       12.2 fb^{-1}       CMS Preliminary ")    
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    bveto_nor.GetYaxis().SetTitleOffset(1.5)
    bveto_nor.GetXaxis().SetTitle("m_{T}(#tau jet, MET) (GeV/c^{2})")
    bveto_nor.GetYaxis().SetTitle("Events / 10 GeV/c^{2}")
    canvas725.Print("transverseMassBvetoBtagInv.png")
    canvas725.Print("transverseMassBvetoBtagInv.C")

    
####################################################
# mt factorised

    canvas720 = ROOT.TCanvas("canvas720","",500,500)    
    mtFactorised.SetMarkerColor(4)
    mtFactorised.SetMarkerSize(1)
    mtFactorised.SetMarkerStyle(20)
    mtFactorised.SetFillColor(4)
    mtFactorised.Draw("EP")
    
 
    
    mtHMTjet2Cut.SetMarkerColor(2)
    mtHMTjet2Cut.SetMarkerSize(1)
    mtHMTjet2Cut.SetMarkerStyle(21)
    mtHMTjet2Cut.SetFillColor(2)
    mtHMTjet2Cut.Draw("same")
    
    tex2 = ROOT.TLatex(0.55,0.85,"Inverted #tau isolation")
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw()
#    tex3 = ROOT.TLatex(0.55,0.75,"#Delta#phi(#tau jet, Met) < 160^{o}")
#    tex3 = ROOT.TLatex(0.55,0.75,"2 Dim #Delta#phi cut")
    tex3 = ROOT.TLatex(0.45,0.75,"With b-tagging factorization")
    tex3.SetNDC()
    tex3.SetTextSize(20)
    tex3.Draw() 
    marker2 = ROOT.TMarker(0.4,0.755,mtFactorised.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(mtFactorised.GetMarkerColor())
    marker2.SetMarkerSize(0.9*mtFactorised.GetMarkerSize())
    marker2.Draw()
    tex5 = ROOT.TLatex(0.45,0.65,"No factorization")
    tex5.SetNDC()
    tex5.SetTextSize(20)
    tex5.Draw() 
    marker5 = ROOT.TMarker(0.4,0.655,mtHMTjet2Cut.GetMarkerStyle())
    marker5.SetNDC()
    marker5.SetMarkerColor(mtHMTjet2Cut.GetMarkerColor())
    marker5.SetMarkerSize(0.9*mtHMTjet2Cut.GetMarkerSize())
    marker5.Draw()    
    
#    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       5.05 fb^{-1}       CMS Preliminary ")
    tex4 = ROOT.TLatex(0.2,0.95,"8 TeV       12.2 fb^{-1}       CMS Preliminary ")    
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    mtFactorised.GetYaxis().SetTitleOffset(1.5)
    mtFactorised.GetXaxis().SetTitle("m_{T}(#tau jet, MET) (GeV/c^{2})")
    mtFactorised.GetYaxis().SetTitle("Events / 10 GeV/c^{2}")
    canvas720.Print("transverseMassFactorised.png")
    canvas720.Print("transverseMassFactorised.C")
        
####################################################
# mt with deltaPhicut
    canvas73 = ROOT.TCanvas("canvas73","",500,500)    
    mtDphiCut.SetMarkerColor(4)
    mtDphiCut.SetMarkerSize(1)
    mtDphiCut.SetMarkerStyle(20)
    mtDphiCut.SetFillColor(4)
    mtDphiCut.Draw("EP")
               

    tex2 = ROOT.TLatex(0.55,0.85,"Inverted #tau isolation")
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw()
#    tex3 = ROOT.TLatex(0.55,0.75,"#Delta#phi(#tau jet, Met) < 160^{o}")
#    tex3 = ROOT.TLatex(0.55,0.75,"2 Dim #Delta#phi cut")
    tex3 = ROOT.TLatex(0.55,0.75,"With #Delta#phi(#tau jet, MET) cut")
    tex3.SetNDC()
    tex3.SetTextSize(20)
    tex3.Draw() 
    marker2 = ROOT.TMarker(0.5,0.865,hmtSum.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(hmtSum.GetMarkerColor())
    marker2.SetMarkerSize(0.9*hmtSum.GetMarkerSize())
#    marker2.Draw()
    
    
#    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       5.05 fb^{-1}       CMS Preliminary ")
    tex4 = ROOT.TLatex(0.2,0.95,"8 TeV       12.2 fb^{-1}       CMS Preliminary ")    
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    mtDphiCut.GetYaxis().SetTitleOffset(1.5)
    mtDphiCut.GetXaxis().SetTitle("m_{T}(#tau jet, MET) (GeV/c^{2})")
    mtDphiCut.GetYaxis().SetTitle("Events / 10 GeV/c^{2}")
    canvas73.Print("transverseMassDeltaPhiCut.png")
    canvas73.Print("transverseMassDeltaPhiCut.C")

 ####################################################
# mt with deltaPhicut vs MHT jet1 cut
    canvas74 = ROOT.TCanvas("canvas74","",500,500)    
    mtHMTjet1Cut.SetMarkerColor(4)
    mtHMTjet1Cut.SetMarkerSize(1)
    mtHMTjet1Cut.SetMarkerStyle(20)
    mtHMTjet1Cut.SetFillColor(4)
    mtHMTjet1Cut.Draw("EP")
               
    tex2 = ROOT.TLatex(0.55,0.85,"Inverted #tau isolation")
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw()
#    tex3 = ROOT.TLatex(0.55,0.75,"#Delta#phi(#tau jet, Met) < 160^{o}")
#    tex3 = ROOT.TLatex(0.55,0.75,"2 Dim #Delta#phi cut")
    tex3 = ROOT.TLatex(0.55,0.75,"#Delta#phi(#tau jet,MET) < 120^{o}")
    tex3.SetNDC()
    tex3.SetTextSize(20)
#    tex3.Draw()
#    tex5 = ROOT.TLatex(0.55,0.65,"#Delta#phi(MHT,jet1) > 60^{o}")
    tex5 = ROOT.TLatex(0.5,0.75,"#Delta#phi(MET,jet1 / #tau jet) cuts")
    tex5.SetNDC()
    tex5.SetTextSize(20)
    tex5.Draw()
    
    marker2 = ROOT.TMarker(0.5,0.865,hmtSum.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(hmtSum.GetMarkerColor())
    marker2.SetMarkerSize(0.9*hmtSum.GetMarkerSize())
#    marker2.Draw()    
#    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       5.05 fb^{-1}       CMS Preliminary ")
    tex4 = ROOT.TLatex(0.2,0.95,"8 TeV       12.2 fb^{-1}       CMS Preliminary ")    
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    mtHMTjet1Cut.GetYaxis().SetTitleOffset(1.5)
    mtHMTjet1Cut.GetXaxis().SetTitle("m_{T}(#tau jet, MET) (GeV/c^{2})")
    mtHMTjet1Cut.GetYaxis().SetTitle("Events / 10 GeV/c^{2}")
    canvas74.Print("transverseMassDeltaPhiVsMETJet1Cut.png")
    canvas74.Print("transverseMassDeltaPhiVsMETJet1Cut.C")


    
 ####################################################
# mt with deltaPhicut vs MHT jet2 cut
    canvas75 = ROOT.TCanvas("canvas75","",500,500)    
    mtHMTjet2Cut.SetMarkerColor(4)
    mtHMTjet2Cut.SetMarkerSize(1)
    mtHMTjet2Cut.SetMarkerStyle(20)
    mtHMTjet2Cut.SetFillColor(4)
    mtHMTjet2Cut.Draw("EP")
               
    tex2 = ROOT.TLatex(0.55,0.85,"Inverted #tau isolation")
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw()
#    tex3 = ROOT.TLatex(0.55,0.75,"#Delta#phi(#tau jet, Met) < 160^{o}")
#    tex3 = ROOT.TLatex(0.55,0.75,"2 Dim #Delta#phi cut")
    tex3 = ROOT.TLatex(0.55,0.75,"#Delta#phi(#tau jet,MET) < 120^{o}")
    tex3.SetNDC()
    tex3.SetTextSize(20)
#    tex3.Draw()
    tex5 = ROOT.TLatex(0.5,0.75,"#Delta#phi(MET,jet / #tau jet) cuts")
    tex5.SetNDC()
    tex5.SetTextSize(20)
    tex5.Draw()
    
    marker2 = ROOT.TMarker(0.5,0.865,hmtSum.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(hmtSum.GetMarkerColor())
    marker2.SetMarkerSize(0.9*hmtSum.GetMarkerSize())
#    marker2.Draw()    
#    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       5.05 fb^{-1}       CMS Preliminary ")
    tex4 = ROOT.TLatex(0.2,0.95,"8 TeV       12.2 fb^{-1}       CMS Preliminary ")    
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    mtHMTjet2Cut.GetYaxis().SetTitleOffset(1.5)
    mtHMTjet2Cut.GetXaxis().SetTitle("m_{T}(#tau jet, MET) (GeV/c^{2})")
    mtHMTjet2Cut.GetYaxis().SetTitle("Events / 20 GeV/c^{2}")

    canvas75.Print("transverseMassDeltaPhiVsMETJetCuts.png")
    canvas75.Print("transverseMassDeltaPhiVsMETJetCuts.C")
       
##############################################################
# mt with deltaPhicut against TT
    canvas751 = ROOT.TCanvas("canvas751","",500,500)    
    Againsttt.SetMarkerColor(4)
    Againsttt.SetMarkerSize(1)
    Againsttt.SetMarkerStyle(20)
    Againsttt.SetFillColor(4)
    Againsttt.Draw("EP")
               
    tex2 = ROOT.TLatex(0.55,0.85,"Inverted #tau isolation")
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw()
#    tex3 = ROOT.TLatex(0.55,0.75,"#Delta#phi(#tau jet, Met) < 160^{o}")
#    tex3 = ROOT.TLatex(0.55,0.75,"2 Dim #Delta#phi cut")
    tex3 = ROOT.TLatex(0.5,0.75,"#Delta#phi(MET,jet / #tau jet) cuts")
    tex3.SetNDC()
    tex3.SetTextSize(20)
    tex3.Draw()
    tex5 = ROOT.TLatex(0.5,0.65,"#Delta#phi cuts against tt")
    tex5.SetNDC()
    tex5.SetTextSize(20)
    tex5.Draw()
    
    marker2 = ROOT.TMarker(0.5,0.865,Againsttt.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(Againsttt.GetMarkerColor())
    marker2.SetMarkerSize(0.9*Againsttt.GetMarkerSize())
#    marker2.Draw()    
#    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       5.05 fb^{-1}       CMS Preliminary ")
    tex4 = ROOT.TLatex(0.2,0.95,"8 TeV       12.2 fb^{-1}       CMS Preliminary ")    
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    Againsttt.GetYaxis().SetTitleOffset(1.5)
    Againsttt.GetXaxis().SetTitle("m_{T}(#tau jet, MET) (GeV/c^{2})")
    Againsttt.GetYaxis().SetTitle("Events / 20 GeV/c^{2}")

    canvas751.Print("transverseMassAgainstTTCut_QCD.png")
    canvas751.Print("transverseMassAgainstTTCut_QCD.C")
       
####################################################    


############


    canvas421 = ROOT.TCanvas("canvas421","",500,500)    
#    hmtPhivSum.SetMaximum(400)
    hmtPhivSum.SetMinimum(-20)
    
    hmtPhivSum.SetMarkerColor(4)
    hmtPhivSum.SetMarkerSize(1)
    hmtPhivSum.SetMarkerStyle(20)
    hmtPhivSum.SetFillColor(4)
    hmtPhivSum.Draw("EP")
    
    hmtPhivBaseline_QCD = hmtPhivBaseline.Clone("QCD")
    hmtPhivBaseline_QCD.Add(hmtvEWK,-1)
    hmtPhivBaseline_QCD.SetMarkerColor(2)
    hmtPhivBaseline_QCD.SetMarkerSize(1)
    hmtPhivBaseline_QCD.SetMarkerStyle(21)
    hmtPhivBaseline_QCD.Draw("same")            

             
    tex2 = ROOT.TLatex(0.55,0.85,"Inverted #tau isolation")
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw()    
    marker2 = ROOT.TMarker(0.5,0.865,hmtSum.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(hmtSum.GetMarkerColor())
    marker2.SetMarkerSize(0.9*hmtSum.GetMarkerSize())
    marker2.Draw()
    tex9 = ROOT.TLatex(0.55,0.78,"Baseline: Data-EWK") 
    tex9.SetNDC()
    tex9.SetTextSize(20)
    tex9.Draw()
    marker9 = ROOT.TMarker(0.5,0.795,hmtBaseline_QCD.GetMarkerStyle())
    marker9.SetNDC()
    marker9.SetMarkerColor(hmtBaseline_QCD.GetMarkerColor())
    marker9.SetMarkerSize(0.9*hmtBaseline_QCD.GetMarkerSize())
    marker9.Draw()
    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       5.05 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    hmtPhivSum.GetYaxis().SetTitleOffset(1.5)
    hmtPhivSum.GetXaxis().SetTitle("m_{T}(#tau jet, MET) (GeV/c^{2})")
    hmtPhivSum.GetYaxis().SetTitle("Events / 10 GeV/c^{2}")
    canvas421.Print("transverseMassBvetoPhiCuts.png")
    canvas421.Print("transverseMassBvetoPhiCuts.C")
############


    canvas42 = ROOT.TCanvas("canvas42","",500,500)    
    hmtvSum.SetMaximum(400)
    hmtvSum.SetMinimum(-20)
    
    hmtvSum.SetMarkerColor(4)
    hmtvSum.SetMarkerSize(1)
    hmtvSum.SetMarkerStyle(20)
    hmtvSum.SetFillColor(4)
    hmtvSum.Draw("EP")
    
    hmtvBaseline_QCD = hmtvBaseline.Clone("QCD")
    hmtvBaseline_QCD.Add(hmtvEWK,-1)
    hmtvBaseline_QCD.SetMarkerColor(2)
    hmtvBaseline_QCD.SetMarkerSize(1)
    hmtvBaseline_QCD.SetMarkerStyle(21)
    hmtvBaseline_QCD.Draw("same")            

             
    tex2 = ROOT.TLatex(0.55,0.85,"Inverted #tau isolation")
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw()    
    marker2 = ROOT.TMarker(0.5,0.865,hmtSum.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(hmtSum.GetMarkerColor())
    marker2.SetMarkerSize(0.9*hmtSum.GetMarkerSize())
    marker2.Draw()
    tex9 = ROOT.TLatex(0.55,0.78,"Baseline: Data-EWK") 
    tex9.SetNDC()
    tex9.SetTextSize(20)
    tex9.Draw()
    marker9 = ROOT.TMarker(0.5,0.795,hmtBaseline_QCD.GetMarkerStyle())
    marker9.SetNDC()
    marker9.SetMarkerColor(hmtBaseline_QCD.GetMarkerColor())
    marker9.SetMarkerSize(0.9*hmtBaseline_QCD.GetMarkerSize())
    marker9.Draw()
    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       5.05 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    hmtvSum.GetYaxis().SetTitleOffset(1.5)
    hmtvSum.GetXaxis().SetTitle("m_{T}(#tau jet, MET) (GeV/c^{2})")
    hmtvSum.GetYaxis().SetTitle("Events / 10 GeV/c^{2}")
    canvas42.Print("transverseMassBveto.png")
    canvas42.Print("transverseMassBveto.C")
    
    
################ MET

    mmt = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MET_InvertedTauIdJets")])        
    mmtBaseline = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("BaseLine/MET_BaseLineTauIdJets")])
    mmtEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("BaseLine/MET_BaseLineTauIdJets")])        
   
    mmtBaseline._setLegendStyles()
    mmtBaseline._setLegendLabels()
    mmtBaseline.histoMgr.setHistoDrawStyleAll("P")
    mmtBaseline.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(4))  
    hmmtBaseline = mmtBaseline.histoMgr.getHisto("Data").getRootHisto().Clone("BaseLine/MTBaselineTauIdJetPhi")
    
    mmtEWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mmtEWK._setLegendStyles()
    mmtEWK._setLegendLabels()
    mmtEWK.histoMgr.setHistoDrawStyleAll("P")
    mmtEWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(4))  
    hmmtEWK = mmtEWK.histoMgr.getHisto("EWK").getRootHisto().Clone("BaseLine/MTBaselineTauIdJetPhi")
    

       
    canvas34 = ROOT.TCanvas("canvas34","",500,500)
    canvas34.SetLogy()
    met.SetMarkerColor(4)
    met.SetMarkerSize(1)
    met.SetMarkerStyle(20)
    met.SetFillColor(4)    
    met.Draw("EP")
    
    hmmtBaseline_QCD = hmmtBaseline.Clone("QCD")
    hmmtBaseline_QCD.Add(hmmtEWK,-1)
    hmmtBaseline_QCD.SetMarkerColor(2)
    hmmtBaseline_QCD.SetMarkerSize(1)
    hmmtBaseline_QCD.SetMarkerStyle(21)
    hmmtBaseline_QCD.Draw("same")

            
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       5.05 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    tex2 = ROOT.TLatex(0.55,0.85,"Inverted #tau isolation")
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw()    
    marker2 = ROOT.TMarker(0.5,0.865,met.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(met.GetMarkerColor())
    marker2.SetMarkerSize(0.9*met.GetMarkerSize())
    marker2.Draw()
    
    tex9 = ROOT.TLatex(0.55,0.78,"Baseline: Data-EWK") 
    tex9.SetNDC()
    tex9.SetTextSize(20)
    tex9.Draw()
    marker9 = ROOT.TMarker(0.5,0.795,hmmtBaseline_QCD.GetMarkerStyle())
    marker9.SetNDC()
    marker9.SetMarkerColor(hmmtBaseline_QCD.GetMarkerColor())
    marker9.SetMarkerSize(0.9*hmmtBaseline_QCD.GetMarkerSize())
    marker9.Draw()
        
    met.GetXaxis().SetTitle("MET (GeV)")
    met.GetYaxis().SetTitle("Events / 20 GeV")
    canvas34.Print("MET.png")
    canvas34.Print("MET.C")

#############

    ###  deltaPhi
    fmtBaseline = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("BaseLine/deltaPhiBaseline")])
    fmtEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("BaseLine/deltaPhiBaseline")])        


    fmtBaseline._setLegendStyles()
    fmtBaseline._setLegendLabels()
    fmtBaseline.histoMgr.setHistoDrawStyleAll("P")
    fmtBaseline.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))  
    hfmtBaseline = fmtBaseline.histoMgr.getHisto("Data").getRootHisto().Clone("BaseLine/MTBaselineTauIdJetPhi")
    
    fmtEWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    fmtEWK._setLegendStyles()
    fmtEWK._setLegendLabels()
    fmtEWK.histoMgr.setHistoDrawStyleAll("P")
    fmtEWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))  
    hfmtEWK = fmtEWK.histoMgr.getHisto("EWK").getRootHisto().Clone("BaseLine/MTBaselineTauIdJetPhi")
    

       
    canvas30 = ROOT.TCanvas("canvas30","",500,500)
    DeltaPhi.SetMarkerColor(4)
    DeltaPhi.SetMarkerSize(1)
    DeltaPhi.SetMarkerStyle(20)
    DeltaPhi.SetFillColor(4)    
    DeltaPhi.Draw("EP")
    
    DeltaPhi_QCD = hfmtBaseline.Clone("QCD")
    DeltaPhi_QCD.Add(hfmtEWK,-1)
    DeltaPhi_QCD.SetMarkerColor(2)
    DeltaPhi_QCD.SetMarkerSize(1)
    DeltaPhi_QCD.SetMarkerStyle(21)
    DeltaPhi_QCD.Draw("same")
    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       5.05 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    tex2 = ROOT.TLatex(0.55,0.85,"Inverted #tau isolation")
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw()    
    marker2 = ROOT.TMarker(0.5,0.865,DeltaPhi.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(DeltaPhi.GetMarkerColor())
    marker2.SetMarkerSize(0.9*DeltaPhi.GetMarkerSize())
    marker2.Draw()
    
    tex9 = ROOT.TLatex(0.55,0.78,"Baseline: Data-EWK") 
    tex9.SetNDC()
    tex9.SetTextSize(20)
    tex9.Draw()
    marker9 = ROOT.TMarker(0.5,0.795,DeltaPhi_QCD.GetMarkerStyle())
    marker9.SetNDC()
    marker9.SetMarkerColor(DeltaPhi_QCD.GetMarkerColor())
    marker9.SetMarkerSize(0.9*DeltaPhi_QCD.GetMarkerSize())
    marker9.Draw()
            
    
    DeltaPhi.GetXaxis().SetTitle("#Delta#phi(#tau jet, MET) (^{o})")
    DeltaPhi.GetYaxis().SetTitle("Events / 10^{o}")
    canvas30.Print("DeltaPhi.png")
    canvas30.Print("DeltaPhi.C")

    
################ Higgs mass
        
    canvas31 = ROOT.TCanvas("canvas31","",500,500)
    higgsMass.SetMarkerColor(4)
    higgsMass.SetMarkerSize(1)
    higgsMass.SetMarkerStyle(20)
    higgsMass.SetFillColor(4)
    
    higgsMass.Draw("EP")
            
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       5.05 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    
    higgsMass.GetXaxis().SetTitle("m_{Higgs} (GeV/c^{2})")
    higgsMass.GetYaxis().SetTitle("Events / 20 GeV/c^{2} ")
    canvas31.Print("FullMass.png")
    canvas31.Print("FullMass.C")

################ deltaphi jet-Met
    if False:
        canvas51 = ROOT.TCanvas("canvas51","",500,500)
        
        jetmetphi.SetMarkerColor(4)
        jetmetphi.SetMarkerSize(1)
        jetmetphi.SetFillColor(4)   
        jetmetphi.Draw("EP")
        
        tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       5.05 fb^{-1}       CMS Preliminary ")
        tex4.SetNDC()
        tex4.SetTextSize(20)
        tex4.Draw()
        
        
        jetmetphi.GetXaxis().SetTitle("#Delta#Phi(jet,MET) (deg)")
        jetmetphi.GetYaxis().SetTitle("Events ")
        canvas51.Print("DeltaPhiJetMet.png")
        canvas51.Print("DeltaPhiJetMet.C")

######## deltaPhi(jet,Met) vs deltaPhi(tau,Met)       
        canvas52 = ROOT.TCanvas("canvas52","",500,500)

        DeltaPhiJetMet.RebinX(5)
        DeltaPhiJetMet.RebinY(5)
        DeltaPhiJetMet.SetMarkerColor(4)
        DeltaPhiJetMet.SetMarkerSize(1)
        DeltaPhiJetMet.SetMarkerStyle(20)
        DeltaPhiJetMet.SetFillColor(4)    
        DeltaPhiJetMet.Draw("colz")
        
        tex4 = ROOT.TLatex(0.2,0.95,"8 TeV       12 fb^{-1}       CMS Preliminary ")
        tex4.SetNDC()
        tex4.SetTextSize(20)
        tex4.Draw()
        tex1 = ROOT.TLatex(0.55,0.88,"QCD with inverted #tau isolation") 
        tex1.SetNDC()
        tex1.SetTextSize(15)
        tex1.Draw()
        
        DeltaPhiJetMet.GetXaxis().SetTitle("#Delta#phi(#tau jet,MET) (deg)")
        DeltaPhiJetMet.GetYaxis().SetTitle("#Delta#phi(jet,MET) (deg) ")
        canvas52.Print("DeltaPhiJetMetVSTauMet.png")
        canvas52.Print("DeltaPhiJetMetVSTauMet.C")
        
    if True:
######## hMHTJet1phi deltaPhi(jet,Met) vs hMHTJet1phi deltaPhi(tau,Met)       
        canvas82 = ROOT.TCanvas("canvas82","",500,500)
        
#        MHTJet1phi.RebinX(5)
#        MHTJet1phi.RebinY(5)
        MHTJet1phi.SetMarkerColor(4)
        MHTJet1phi.SetMarkerSize(1)
        MHTJet1phi.SetMarkerStyle(20)
        MHTJet1phi.SetFillColor(4)    
        MHTJet1phi.Draw("colz")
        
        tex4 = ROOT.TLatex(0.2,0.95,"8 TeV       12 fb^{-1}       CMS Preliminary ")
        tex4.SetNDC()
        tex4.SetTextSize(20)
        tex4.Draw()
        tex1 = ROOT.TLatex(0.55,0.88,"QCD with inverted #tau isolation") 
        tex1.SetNDC()
        tex1.SetTextSize(15)
        tex1.Draw()
        
        MHTJet1phi.GetXaxis().SetTitle("#Delta#phi(jet1,MHT) (deg)")
        MHTJet1phi.GetYaxis().SetTitle("Events ")
        canvas82.Print("DeltaPhiMETjet1.png")
        canvas82.Print("DeltaPhiMETjet1.C")

    
######## deltaPhi(jet,Met) vs deltaPhi(tau,Met) after 2dim cut
    if True:    
        phi2AfterCut = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/DeltaPhiVsDeltaPhiMETJet2AfterCut")])
        phi2AfterCut._setLegendStyles()
        phi2AfterCut._setLegendLabels()
        phi2AfterCut.histoMgr.setHistoDrawStyleAll("P") 
        phi2AfterCut.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))
        hphi2AfterCut = phi2AfterCut.histoMgr.getHisto("Data").getRootHisto().Clone()
        
        
        canvas55 = ROOT.TCanvas("canvas55","",500,500)
        
        hphi2AfterCut.RebinX(5)
        hphi2AfterCut.RebinY(5)
        hphi2AfterCut.SetMarkerColor(4)
        hphi2AfterCut.SetMarkerSize(1)
        hphi2AfterCut.SetMarkerStyle(20)
        hphi2AfterCut.SetFillColor(4)    
        hphi2AfterCut.Draw("colz")
        
        tex4 = ROOT.TLatex(0.2,0.95,"8 TeV       12 fb^{-1}       CMS Preliminary ")
        tex4.SetNDC()
        tex4.SetTextSize(20)
        tex4.Draw()
        tex1 = ROOT.TLatex(0.55,0.88,"QCD with inverted #tau isolation") 
        tex1.SetNDC()
        tex1.SetTextSize(15)
        tex1.Draw()
        
        hphi2AfterCut.GetXaxis().SetTitle("#Delta#phi(#tau jet,MET) (deg)")
        hphi2AfterCut.GetYaxis().SetTitle("#Delta#phi(jet,MET) (deg) ")
        canvas55.Print("DeltaPhiAfterJet1Cut.png")
        canvas55.Print("DeltaPhiAfterJet1Cut.C")


        
######## DeltaR_TauMETJet1MET"
    if True:    
        deltaR1 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/DeltaR_TauMETJet1MET")])
        deltaR1._setLegendStyles()
        deltaR1._setLegendLabels()
        deltaR1.histoMgr.setHistoDrawStyleAll("P") 
        deltaR1.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))
        hdeltaR1 = deltaR1.histoMgr.getHisto("Data").getRootHisto().Clone()
        
        
        canvas75 = ROOT.TCanvas("canvas75","",500,500)
    
        hdeltaR1.SetMarkerColor(4)
        hdeltaR1.SetMarkerSize(1)
        hdeltaR1.SetMarkerStyle(20)
        hdeltaR1.SetFillColor(4)    
        hdeltaR1.Draw("colz")
        
        tex4 = ROOT.TLatex(0.2,0.95,"8 TeV       12 fb^{-1}       CMS Preliminary ")
        tex4.SetNDC()
        tex4.SetTextSize(20)
        tex4.Draw()
        tex1 = ROOT.TLatex(0.55,0.88,"QCD with inverted #tau isolation") 
        tex1.SetNDC()
        tex1.SetTextSize(15)
        tex1.Draw()
        
        hdeltaR1.GetXaxis().SetTitle("#Delta R in #Delta#phi(#tau jet,MET) vs #Delta#phi(jet1,MET) plane")
        hdeltaR1.GetYaxis().SetTitle("Events ")
        canvas75.Print("DeltaR_TauMETJet1MET_QCD.png")
        canvas75.Print("DeltaR_TauMETJet1MET_QCD.C")
        
######## DeltaR_TauMETJet2MET"
    if True:    
        deltaR2 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/DeltaR_TauMETJet2MET")])
        deltaR2._setLegendStyles()
        deltaR2._setLegendLabels()
        deltaR2.histoMgr.setHistoDrawStyleAll("P") 
        deltaR2.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))
        hdeltaR2 = deltaR2.histoMgr.getHisto("Data").getRootHisto().Clone()
        
        
        canvas76 = ROOT.TCanvas("canvas76","",500,500)
    
        hdeltaR2.SetMarkerColor(4)
        hdeltaR2.SetMarkerSize(1)
        hdeltaR2.SetMarkerStyle(20)
        hdeltaR2.SetFillColor(4)    
        hdeltaR2.Draw("colz")
        
        tex4 = ROOT.TLatex(0.2,0.95,"8 TeV       12 fb^{-1}       CMS Preliminary ")
        tex4.SetNDC()
        tex4.SetTextSize(20)
        tex4.Draw()
        tex1 = ROOT.TLatex(0.55,0.88,"QCD with inverted #tau isolation") 
        tex1.SetNDC()
        tex1.SetTextSize(15)
        tex1.Draw()
        
        hdeltaR2.GetXaxis().SetTitle("#Delta R in #Delta#phi(#tau jet,MET) vs #Delta#phi(jet2,MET) plane")
        hdeltaR2.GetYaxis().SetTitle("Events ")
        canvas76.Print("DeltaR_TauMETJet2MET_QCD.png")
        canvas76.Print("DeltaR_TauMETJet2MET_QCD.C")

######## DeltaR_TauMETJet3MET"
    if True:    
        deltaR3 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/DeltaR_TauMETJet3MET")])
        deltaR3._setLegendStyles()
        deltaR3._setLegendLabels()
        deltaR3.histoMgr.setHistoDrawStyleAll("P") 
        deltaR3.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))
        hdeltaR3 = deltaR3.histoMgr.getHisto("Data").getRootHisto().Clone()
        
        
        canvas77 = ROOT.TCanvas("canvas77","",500,500)
    
        hdeltaR3.SetMarkerColor(4)
        hdeltaR3.SetMarkerSize(1)
        hdeltaR3.SetMarkerStyle(20)
        hdeltaR3.SetFillColor(4)    
        hdeltaR3.Draw("colz")
        
        tex4 = ROOT.TLatex(0.2,0.95,"8 TeV       12 fb^{-1}       CMS Preliminary ")
        tex4.SetNDC()
        tex4.SetTextSize(20)
        tex4.Draw()
        tex1 = ROOT.TLatex(0.55,0.88,"QCD with inverted #tau isolation") 
        tex1.SetNDC()
        tex1.SetTextSize(15)
        tex1.Draw()
        
        hdeltaR3.GetXaxis().SetTitle("#Delta R in #Delta#phi(#tau jet,MET) vs #Delta#phi(jet3,MET) plane")
        hdeltaR3.GetYaxis().SetTitle("Events ")
        canvas77.Print("DeltaR_TauMETJet3MET_QCD.png")
        canvas77.Print("DeltaR_TauMETJet3MET_QCD.C")



        ######## DeltaR_TauMETJet4MET"
    if True:    
        deltaR4 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/DeltaR_TauMETJet4MET")])
        deltaR4._setLegendStyles()
        deltaR4._setLegendLabels()
        deltaR4.histoMgr.setHistoDrawStyleAll("P") 
        deltaR4.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))
        hdeltaR4 = deltaR4.histoMgr.getHisto("Data").getRootHisto().Clone()
        
        
        canvas78 = ROOT.TCanvas("canvas78","",500,500)
    
        hdeltaR4.SetMarkerColor(4)
        hdeltaR4.SetMarkerSize(1)
        hdeltaR4.SetMarkerStyle(20)
        hdeltaR4.SetFillColor(4)    
        hdeltaR4.Draw("colz")
        
        tex4 = ROOT.TLatex(0.2,0.95,"8 TeV       12 fb^{-1}       CMS Preliminary ")
        tex4.SetNDC()
        tex4.SetTextSize(20)
        tex4.Draw()
        tex1 = ROOT.TLatex(0.55,0.88,"QCD with inverted #tau isolation") 
        tex1.SetNDC()
        tex1.SetTextSize(15)
        tex1.Draw()
        
        hdeltaR4.GetXaxis().SetTitle("#Delta R in #Delta#phi(#tau jet,MET) vs #Delta#phi(jet4,MET) plane")
        hdeltaR4.GetYaxis().SetTitle("Events ")
        canvas78.Print("DeltaR_TauMETJet4MET_QCD.png")
        canvas78.Print("DeltaR_TauMETJet4MET_QCD.C")    
        
######## deltaPhi(jet,Met) vs deltaPhi(tau,Met) after 2dim cut
        
    phi2AfterCut2 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/DeltaPhiVsDeltaPhiMETJet1")])
    phi2AfterCut2._setLegendStyles()
    phi2AfterCut2._setLegendLabels()
    phi2AfterCut2.histoMgr.setHistoDrawStyleAll("P")
    phi2AfterCut2.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))
    hphi2AfterCut2 = phi2AfterCut2.histoMgr.getHisto("Data").getRootHisto().Clone()
    
    
    canvas56 = ROOT.TCanvas("canvas56","",500,500)
    
    hphi2AfterCut2.RebinX(5)
    hphi2AfterCut2.RebinY(5)
    hphi2AfterCut2.SetMarkerColor(4)
    hphi2AfterCut2.SetMarkerSize(1)
    hphi2AfterCut2.SetMarkerStyle(20)
    hphi2AfterCut2.SetFillColor(4)
    hphi2AfterCut2.Draw("colz")
    
    tex4 = ROOT.TLatex(0.2,0.95,"8 TeV       12 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    tex1 = ROOT.TLatex(0.55,0.88,"QCD with inverted #tau isolation")
    tex1.SetNDC()
    tex1.SetTextSize(15)
    tex1.Draw()
    
    hphi2AfterCut2.GetXaxis().SetTitle("#Delta#phi(#tau jet,MET) (deg)")
    hphi2AfterCut2.GetYaxis().SetTitle("#Delta#phi(jet1,MET) (deg) ")
    canvas56.Print("DeltaPhiVSdeltaPhiMETjet1.png")
    canvas56.Print("DeltaPhiVSdeltaPhiMETjet1.C")
    
######## deltaPhi(jet,Met) vs deltaPhi(tau,Met) after 2dim cut

    phi2AfterCut3 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/DeltaPhiVsDeltaPhiMETJet2")])
    phi2AfterCut3._setLegendStyles()
    phi2AfterCut3._setLegendLabels()
    phi2AfterCut3.histoMgr.setHistoDrawStyleAll("P")
    phi2AfterCut3.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))
    hphi2AfterCut3 = phi2AfterCut3.histoMgr.getHisto("Data").getRootHisto().Clone()


    canvas57 = ROOT.TCanvas("canvas56","",500,500)

    hphi2AfterCut3.RebinX(5)
    hphi2AfterCut3.RebinY(5)
    hphi2AfterCut3.SetMarkerColor(4)
    hphi2AfterCut3.SetMarkerSize(1)
    hphi2AfterCut3.SetMarkerStyle(20)
    hphi2AfterCut3.SetFillColor(4)
    hphi2AfterCut3.Draw("colz")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    tex1 = ROOT.TLatex(0.55,0.88,"QCD with inverted #tau isolation")
    tex1.SetNDC()
    tex1.SetTextSize(15)
    tex1.Draw()
    
    hphi2AfterCut3.GetXaxis().SetTitle("#Delta#phi(#tau jet,MET) (deg)")
    hphi2AfterCut3.GetYaxis().SetTitle("#Delta#phi(jet2,MET) (deg) ")
    canvas57.Print("DeltaPhiVSdeltaPhiMETjet2.png")
    canvas57.Print("DeltaPhiVSdeltaPhiMETjet2.C")

    
    ######## deltaPhi(jet,Met) vs deltaPhi(tau,Met) after 2dim cut

    phi2AfterCut4 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/DeltaPhiVsDeltaPhiMETJet3")])
    phi2AfterCut4._setLegendStyles()
    phi2AfterCut4._setLegendLabels()
    phi2AfterCut4.histoMgr.setHistoDrawStyleAll("P")
    phi2AfterCut4.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))
    hphi2AfterCut4 = phi2AfterCut4.histoMgr.getHisto("Data").getRootHisto().Clone()
    
    
    canvas58 = ROOT.TCanvas("canvas58","",500,500)
    
    hphi2AfterCut4.RebinX(5)
    hphi2AfterCut4.RebinY(5)
    hphi2AfterCut4.SetMarkerColor(4)
    hphi2AfterCut4.SetMarkerSize(1)
    hphi2AfterCut4.SetMarkerStyle(20)
    hphi2AfterCut4.SetFillColor(4)
    hphi2AfterCut4.Draw("colz")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    tex1 = ROOT.TLatex(0.55,0.88,"QCD with inverted #tau isolation")
    tex1.SetNDC()
    tex1.SetTextSize(15)
    tex1.Draw()
    
    hphi2AfterCut4.GetXaxis().SetTitle("#Delta#phi(#tau jet,MET) (deg)")
    hphi2AfterCut4.GetYaxis().SetTitle("#Delta#phi(jet3,MET) (deg) ")
    canvas58.Print("DeltaPhiVSdeltaPhiMETjet3.png")
    canvas58.Print("DeltaPhiVSdeltaPhiMETjet3.C")
    
######## deltaPhi(jet4,Met) vs deltaPhi(tau,MET) after 2dim cut
    if True:
        phiTauMHT = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/DeltaPhiVsDeltaPhiMETJet4")])
        phiTauMHT._setLegendStyles()
        phiTauMHT._setLegendLabels()
        phiTauMHT.histoMgr.setHistoDrawStyleAll("P")
        phiTauMHT.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))
        hphiTauMHT = phiTauMHT.histoMgr.getHisto("Data").getRootHisto().Clone()
        
        
        canvas59 = ROOT.TCanvas("canvas59","",500,500)
        
        hphiTauMHT.RebinX(5)
        hphiTauMHT.RebinY(5)
        hphiTauMHT.SetMarkerColor(4)
        hphiTauMHT.SetMarkerSize(1)
        hphiTauMHT.SetMarkerStyle(20)
        hphiTauMHT.SetFillColor(4)
        hphiTauMHT.Draw("colz")
        tex4.SetNDC()
        tex4.SetTextSize(20)
        tex4.Draw()
        tex1 = ROOT.TLatex(0.55,0.88,"QCD with inverted #tau isolation")
        tex1.SetNDC()
        tex1.SetTextSize(15)
        tex1.Draw()
        
        hphiTauMHT.GetXaxis().SetTitle("#Delta#phi(#tau jet,MET) (deg)")
        hphiTauMHT.GetYaxis().SetTitle("#Delta#phi(jet4,MET) (deg) ")
        canvas59.Print("DeltaPhiVSdeltaPhiMETjet4.png")
        canvas59.Print("DeltaPhiVSdeltaPhiMETjet4.C")                                                                                                    
################## N bjets
    
    bhmt = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/NBInvertedTauIdJet")])
    bhmtBaseline = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("BaseLine/NBBaselineTauIdJet")])
    bhmtEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("BaseLine/NBBaselineTauIdJet")])
 
    bhmtBaseline._setLegendStyles()
    bhmtBaseline._setLegendLabels()
    bhmtBaseline.histoMgr.setHistoDrawStyleAll("P")
    bhmtBaseline.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))  
    hbhmtBaseline = bhmtBaseline.histoMgr.getHisto("Data").getRootHisto().Clone("BaseLine/NBBaselineTauIdJet")
    
    bhmtEWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    bhmtEWK._setLegendStyles()
    bhmtEWK._setLegendLabels()
    bhmtEWK.histoMgr.setHistoDrawStyleAll("P")
    bhmtEWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))  
    hbhmtEWK =  bhmtEWK.histoMgr.getHisto("EWK").getRootHisto().Clone("BaseLine/NBBaselineTauIdJet")
    

       
    canvas33 = ROOT.TCanvas("canvas33","",500,500)
    canvas33.SetLogy()
    frame33 = histograms._drawFrame(canvas33, xmin=0, xmax=6, ymin=0.01, ymax=1e4)
    frame33.Draw()
               
    NBjets.SetMarkerColor(4)
    NBjets.SetMarkerSize(1)
    NBjets.SetMarkerStyle(20)
    NBjets.SetFillColor(4)
    NBjets.Draw("EP same")

    NBjets_QCD = hbhmtBaseline.Clone("QCD")
    NBjets_QCD.Add(hbhmtEWK,-1)
    NBjets_QCD.SetMarkerColor(2)
    NBjets_QCD.SetMarkerSize(1)
    NBjets_QCD.SetMarkerStyle(21)
    NBjets_QCD.Draw("same")
    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       5.05 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    tex2 = ROOT.TLatex(0.55,0.85,"Inverted #tau isolation")
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw()    
    marker2 = ROOT.TMarker(0.5,0.865,NBjets.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(NBjets.GetMarkerColor())
    marker2.SetMarkerSize(0.9*NBjets.GetMarkerSize())
    marker2.Draw()
    
    tex9 = ROOT.TLatex(0.55,0.78,"Baseline: Data-EWK") 
    tex9.SetNDC()
    tex9.SetTextSize(20)
    tex9.Draw()
    marker9 = ROOT.TMarker(0.5,0.795,NBjets_QCD.GetMarkerStyle())
    marker9.SetNDC()
    marker9.SetMarkerColor(NBjets_QCD.GetMarkerColor())
    marker9.SetMarkerSize(0.9*NBjets_QCD.GetMarkerSize())
    marker9.Draw()
            
             
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       5.05 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    
    NBjets.GetXaxis().SetTitle("N_{b jets}")
    NBjets.GetYaxis().SetTitle("Events  ")
    canvas33.Print("NBjets.png")
    canvas33.Print("NBjets.C")



################## N jets
      
 
    jBaseline = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("BaseLine/NJetBaselineTauIdJet")])
    jEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("BaseLine/NJetBaselineTauIdJet")])
 
    
    jBaseline._setLegendStyles()
    jBaseline._setLegendLabels()
    jBaseline.histoMgr.setHistoDrawStyleAll("P")
    jBaseline.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))  
    hjBaseline = jBaseline.histoMgr.getHisto("Data").getRootHisto().Clone("BaseLine/NBBaselineTauIdJet")
    
    jEWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    jEWK._setLegendStyles()
    jEWK._setLegendLabels()
    jEWK.histoMgr.setHistoDrawStyleAll("P")
    jEWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))  
    hjEWK =  jEWK.histoMgr.getHisto("EWK").getRootHisto().Clone("BaseLine/NBBaselineTauIdJet")
    

       
    canvas34 = ROOT.TCanvas("canvas34","",500,500)
    canvas34.SetLogy()
    frame34 = histograms._drawFrame(canvas33, xmin=0, xmax=10, ymin=1, ymax=1e5)
    frame34.Draw()
               
    Njets.SetMarkerColor(4)
    Njets.SetMarkerSize(1)
    Njets.SetMarkerStyle(20)
    Njets.SetFillColor(4)
    Njets.Draw("EP same")

    Njets_QCD = hjBaseline.Clone("QCD")
    Njets_QCD.Add(hjEWK,-1)
    Njets_QCD.SetMarkerColor(2)
    Njets_QCD.SetMarkerSize(1)
    Njets_QCD.SetMarkerStyle(21)
    Njets_QCD.Draw("same")
    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       5.05 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    tex2 = ROOT.TLatex(0.55,0.85,"Inverted #tau isolation")
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw()    
    marker2 = ROOT.TMarker(0.5,0.865,Njets.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(Njets.GetMarkerColor())
    marker2.SetMarkerSize(0.9*Njets.GetMarkerSize())
    marker2.Draw()
    
    tex9 = ROOT.TLatex(0.55,0.78,"Baseline: Data-EWK") 
    tex9.SetNDC()
    tex9.SetTextSize(20)
    tex9.Draw()
    marker9 = ROOT.TMarker(0.5,0.795,Njets_QCD.GetMarkerStyle())
    marker9.SetNDC()
    marker9.SetMarkerColor(Njets_QCD.GetMarkerColor())
    marker9.SetMarkerSize(0.9*Njets_QCD.GetMarkerSize())
    
    marker9.Draw()
            
             
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       5.05 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    
    Njets.GetXaxis().SetTitle("N_{jets}")
    Njets.GetYaxis().SetTitle("Events  ")
    canvas34.Print("Njets.png")
    canvas34.Print("Njets.C")

################## N jets after MET
    

    jm = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/NJetInvertedTauIdMet")])
    jmBaseline = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("BaseLine/NJetBaselineTauIdJetMet")])
    jmEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("BaseLine/NJetBaselineTauIdJetMet")])
 
 
    jmBaseline._setLegendStyles()
    jmBaseline._setLegendLabels()
    jmBaseline.histoMgr.setHistoDrawStyleAll("P")
    jmBaseline.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))  
    hjmBaseline = jmBaseline.histoMgr.getHisto("Data").getRootHisto().Clone("Inverted/NBBaselineTauIdJet")
    
    jmEWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    jmEWK._setLegendStyles()
    jmEWK._setLegendLabels()
    jmEWK.histoMgr.setHistoDrawStyleAll("P")
    jmEWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))  
    hjmEWK =  jmEWK.histoMgr.getHisto("EWK").getRootHisto().Clone("NBBaselineTauIdJet")
    

       
    canvas35 = ROOT.TCanvas("canvas35","",500,500)
    canvas35.SetLogy()
    frame35 = histograms._drawFrame(canvas33, xmin=0, xmax=10, ymin=1, ymax=1e4)
    frame35.Draw()
               
    NjetsAfterMET.SetMarkerColor(4)
    NjetsAfterMET.SetMarkerSize(1)
    NjetsAfterMET.SetMarkerStyle(20)
    NjetsAfterMET.SetFillColor(4)
    NjetsAfterMET.Draw("EP same")

    NjetsAfterMET_QCD = hjmBaseline.Clone("QCD")
    NjetsAfterMET_QCD.Add(hjmEWK,-1)
    NjetsAfterMET_QCD.SetMarkerColor(2)
    NjetsAfterMET_QCD.SetMarkerSize(1)
    NjetsAfterMET_QCD.SetMarkerStyle(21)
    NjetsAfterMET_QCD.Draw("same")
    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       5.05 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    tex2 = ROOT.TLatex(0.55,0.85,"Inverted #tau isolation")
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw()    
    marker2 = ROOT.TMarker(0.5,0.865,NjetsAfterMET.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(NjetsAfterMET.GetMarkerColor())
    marker2.SetMarkerSize(0.9*NjetsAfterMET.GetMarkerSize())
    marker2.Draw()
    
    tex9 = ROOT.TLatex(0.55,0.78,"Baseline: Data-EWK") 
    tex9.SetNDC()
    tex9.SetTextSize(20)
    tex9.Draw()
    marker9 = ROOT.TMarker(0.5,0.795,NjetsAfterMET_QCD.GetMarkerStyle())
    marker9.SetNDC()
    marker9.SetMarkerColor(NjetsAfterMET_QCD.GetMarkerColor())
    marker9.SetMarkerSize(0.9*NjetsAfterMET_QCD.GetMarkerSize())
    
    marker9.Draw()
            
             
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       5.05 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    
    NjetsAfterMET.GetXaxis().SetTitle("N_{jets}")
    NjetsAfterMET.GetYaxis().SetTitle("Events  ")
    canvas35.Print("NjetsAfterMET.png")
    canvas35.Print("NjetsAfterMET.C")
    
##########################################################################            
    fOUT = ROOT.TFile.Open("histogramsForLands.root","RECREATE")
    fOUT.cd()
    hmtSum.Write()
    DeltaPhi.Write()
    higgsMass.Write()
    NBjets.Write()
    Njets.Write()
    NjetsAfterMET.Write()
    met.Write()
    fOUT.Close()




##########################################################################




def scaleMC(histo, scale):
    if histo.isMC():
        th1 = histo.getRootHisto()
        th1.Scale(scale)

def scaleMCHistos(h, scale):
    h.histoMgr.forEachHisto(lambda histo: scaleMC(histo, scale))

def scaleMCfromWmunu(h):
    # Data/MC scale factor from AN 2011/053
#    scaleMCHistos(h, 1.736)
    scaleMCHistos(h, 1.0)

def replaceQCDfromData(plot, datasetsQCD, path):
#    normalization = 0.00606 * 0.86
    normalization = 0.025
    drh = datasetsQCD.getDatasetRootHistos(path)
    if len(drh) != 1:
        raise Exception("There should only one DatasetRootHisto, got %d", len(drh))
    histo = histograms.HistoWithDatasetFakeMC(drh[0].getDataset(), drh[0].getHistogram(), drh[0].getName())
    histo.getRootHisto().Scale(normalization)
    plot.histoMgr.replaceHisto("QCD", histo)
    return plot

# Helper function to flip the last two parts of the histogram name
# e.g. ..._afterTauId_DeltaPhi -> DeltaPhi_afterTauId
def flipName(name):
    tmp = name.split("_")
    return tmp[-1] + "_" + tmp[-2]

# Common drawing function
def drawPlot(h, name, xlabel, ylabel="Events / %.0f GeV/c", rebin=1, log=True, addMCUncertainty=True, ratio=False, opts={}, opts2={}, moveLegend={}, textFunction=None, cutLine=None, cutBox=None):
    if cutLine != None and cutBox != None:
        raise Exception("Both cutLine and cutBox were given, only either one can exist")

    if rebin > 1:
        h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    ylab = ylabel
    if "%" in ylabel:
        ylab = ylabel % h.binWidth()


    scaleMCfromWmunu(h)     
#    h.stackMCSignalHistograms()

    h.stackMCHistograms(stackSignal=True)#stackSignal=True)    
#    h.stackMCHistograms()
    
    if addMCUncertainty:
        h.addMCUncertainty()
        
    _opts = {"ymin": 0.01, "ymaxfactor": 2}
    if not log:
        _opts["ymin"] = 0
        _opts["ymaxfactor"] = 1.1
##    _opts2 = {"ymin": 0.5, "ymax": 1.5}
    _opts2 = {"ymin": 0.0, "ymax": 2.0}
    _opts.update(opts)
    _opts2.update(opts2)

    #if log:
    #    name = name + "_log"
    h.createFrame(name, createRatio=ratio, opts=_opts, opts2=_opts2)
    if log:
        h.getPad().SetLogy(log)
    h.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))

    # Add cut line and/or box
    if cutLine != None:
        lst = cutLine
        if not isinstance(lst, list):
            lst = [lst]

        for line in lst:
            h.addCutBoxAndLine(line, box=False, line=True)
    if cutBox != None:
        lst = cutBox
        if not isinstance(lst, list):
            lst = [lst]

        for box in lst:
            h.addCutBoxAndLine(**box)

    common(h, xlabel, ylab, textFunction=textFunction)

# Common formatting
def common(h, xlabel, ylabel, addLuminosityText=True, textFunction=None):
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    if addLuminosityText:
        h.addLuminosityText()
    if textFunction != None:
        textFunction()
    h.save()




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
