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

#dataEra = "Run2011A"
#dataEra = "Run2011B"
dataEra = "Run2012ABC"

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
    datasets = dataset.getDatasetsFromMulticrabDirs(dirs,counters=counters, dataEra=dataEra, analysisBaseName="signalAnalysisInvertedTau")
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
    xsect.setHplusCrossSectionsToTop(datasets_lands)

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
    mt = plots.DataMCPlot(datasets_lands, analysis+"/transverseMass")
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
            return plots.MCPlot(datasets, analysis+"/"+name, normalizeToLumi=mcOnlyLumi, **kwargs)
        else:
            return plots.DataMCPlot(datasets, analysis+"/"+name, **kwargs)
 
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
 
    norm_inc = QCDInvertedNormalization["inclusive"]
    normEWK_inc = QCDInvertedNormalization["inclusiveEWK"]
    
    for bin in ptbins: 
        normData[bin] = QCDInvertedNormalization[bin]
        normEWK[bin] = QCDInvertedNormalization[bin+"EWK"]
           
    print "inclusive norm", norm_inc,normEWK_inc
    print "norm factors", normData
    print "norm factors EWK", normEWK
       
    return normData,normEWK


def normalisationInclusive():
 
    norm_inc = QCDInvertedNormalization["inclusive"]
    normEWK_inc = QCDInvertedNormalization["inclusiveEWK"]
              
    print "inclusive norm", norm_inc,normEWK_inc       
    return norm_inc,normEWK_inc 


def controlPlots(datasets):
    
    normData,normEWK=normalisation()
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
    
## histograms in bins, normalisation and substraction of EWK contribution
    ## mt with 2dim deltaPhi cut
    for ptbin in ptbins:
        mt_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdPhi"+ptbin)])
        mt_tmp._setLegendStyles()
        mt_tmp._setLegendLabels()
        mt_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mt_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mt = mt_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        mt.Scale(normData[ptbin])
#        hmt.append(mt)        
        mtEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MTInvertedTauIdPhi"+ptbin)])
        mtEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mtEWK_tmp._setLegendStyles()
        mtEWK_tmp._setLegendLabels()
        mtEWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mtEWK = mtEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        mtEWK.Scale(normEWK[ptbin])
        mt.Add(mtEWK, -1)
        hmt.append(mt)

        # mt after b tagging
        mtb_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdBtag"+ptbin)])
        mtb_tmp._setLegendStyles()
        mtb_tmp._setLegendLabels()
        mtb_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtb_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mtb = mtb_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        mtb.Scale(normData[ptbin])
#        hmt.append(mt)        
        mtbEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MTInvertedTauIdBtag"+ptbin)])
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
        mtph_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdJetDphi"+ptbin)])
        mtph_tmp._setLegendStyles()
        mtph_tmp._setLegendLabels()
        mtph_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtph_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mtph = mtph_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        mtph.Scale(normData[ptbin])
#        hmt.append(mt)        
        mtphEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MTInvertedTauIdJetDphi"+ptbin)])
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
        mtphj1_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdMet"+ptbin)])
        mtphj1_tmp._setLegendStyles()
        mtphj1_tmp._setLegendLabels()
        mtphj1_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtphj1_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mtphj1 = mtphj1_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        mtphj1.Scale(normData[ptbin])
#        hmt.append(mt)        
        mtphj1EWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MTInvertedTauIdMet"+ptbin)])
        mtphj1EWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mtphj1EWK_tmp._setLegendStyles()
        mtphj1EWK_tmp._setLegendLabels()
        mtphj1EWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtphj1EWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mtphj1EWK = mtphj1EWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        mtphj1EWK.Scale(normEWK[ptbin])
        mtphj1.Add(mtphj1EWK, -1)
        hmtphj1.append(mtphj1)

        
        # mt after deltaphi vs MHTjet2 cut
        mtphj2_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdTopMass"+ptbin)])
        mtphj2_tmp._setLegendStyles()
        mtphj2_tmp._setLegendLabels()
        mtphj2_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtphj2_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mtphj2 = mtphj2_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        mtphj2.Scale(normData[ptbin])
#        hmt.append(mt)        
        mtphj2EWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MTInvertedTauIdTopMass"+ptbin)])
        mtphj2EWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mtphj2EWK_tmp._setLegendStyles()
        mtphj2EWK_tmp._setLegendLabels()
        mtphj2EWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtphj2EWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mtphj2EWK = mtphj1EWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        mtphj2EWK.Scale(normEWK[ptbin])
        mtphj2.Add(mtphj2EWK, -1)
        hmtphj2.append(mtphj2)
                
        ## mt with b veto cut
        mtv_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdBvetoDphi"+ptbin)])
        mtv_tmp._setLegendStyles()
        mtv_tmp._setLegendLabels()
        mtv_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtv_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
        mtv = mtv_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        mtv.Scale(normData[ptbin])
#        hmt.append(mt)        
        mtEWKv_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MTInvertedTauIdBvetoDphi"+ptbin)])
        mtEWKv_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mtEWKv_tmp._setLegendStyles()
        mtEWKv_tmp._setLegendLabels()
        mtEWKv_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtEWKv_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
        mtEWKv = mtEWKv_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        mtEWKv.Scale(normEWK[ptbin])
        mtv.Add(mtEWKv, -1)
        hmtv.append(mtv)
#        hmt.append(mt)
# mt b veto with Dphi cut 
        mtPhiv_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdBvetoDphi"+ptbin)])
        mtPhiv_tmp._setLegendStyles()
        mtPhiv_tmp._setLegendLabels()
        mtPhiv_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtPhiv_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
        mtPhiv = mtPhiv_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        mtPhiv.Scale(normData[ptbin])
        mtPhiEWKv_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MTInvertedTauIdBvetoDphi"+ptbin)])
        mtPhiEWKv_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mtPhiEWKv_tmp._setLegendStyles()
        mtPhiEWKv_tmp._setLegendLabels()
        mtPhiEWKv_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtPhiEWKv_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
        mtPhiEWKv = mtPhiEWKv_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        mtPhiEWKv.Scale(normEWK[ptbin])
        mtPhiv.Add(mtPhiEWKv, -1)
        hmtPhiv.append(mtPhiv)       
        ### MET
        mmt_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets"+ptbin)])
        mmt_tmp._setLegendStyles()
        mmt_tmp._setLegendLabels()
        mmt_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mmt_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))
        mmt = mmt_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        mmt.Scale(normData[ptbin])
#        hmt.append(mt)

#        mmtEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MTInvertedTauIdPhi"+ptbin)])
        mmtEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets"+ptbin)])
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
        fmt_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/deltaPhiInverted"+ptbin)])
        fmt_tmp._setLegendStyles()
        fmt_tmp._setLegendLabels()
        fmt_tmp.histoMgr.setHistoDrawStyleAll("P") 
        fmt_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))
        fmt = fmt_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        fmt.Scale(normData[ptbin])
#        hmt.append(mt)        
        fmtEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/deltaPhiInverted"+ptbin)])
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
        hmt_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/HiggsMass4050")])

#        hmt_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/HiggsMass"+ptbin)])
        hmt_tmp._setLegendStyles()
        hmt_tmp._setLegendLabels()
        hmt_tmp.histoMgr.setHistoDrawStyleAll("P") 
        hmt_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))
        mass = hmt_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        mass.Scale(normData[ptbin])
#        hmt.append(mt)
        hmtEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/HiggsMass4050")])
#        hmtEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/HiggsMass"+ptbin)])
        hmtEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        hmtEWK_tmp._setLegendStyles()
        hmtEWK_tmp._setLegendLabels()
        hmtEWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
        hmtEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))
        massEWK = hmtEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        massEWK.Scale(normEWK[ptbin])
        mass.Add(massEWK, -1)
        hmass.append(mass)

        bmt_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/NBInvertedTauIdJet"+ptbin)])
        bmt_tmp._setLegendStyles()
        bmt_tmp._setLegendLabels()
        bmt_tmp.histoMgr.setHistoDrawStyleAll("P") 
        bmt_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))
        bmt = bmt_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        bmt.Scale(normData[ptbin])
#        hmt.append(mt)        
        bmtEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/NBInvertedTauIdJet"+ptbin)])
        bmtEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        bmtEWK_tmp._setLegendStyles()
        bmtEWK_tmp._setLegendLabels()
        bmtEWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
        bmtEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))
        bmtEWK = bmtEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        bmtEWK.Scale(normEWK[ptbin])
        bmt.Add(bmtEWK, -1)
        hbjet.append(bmt)


        jmt_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/NJetInvertedTauIdJet"+ptbin)])
        jmt_tmp._setLegendStyles()
        jmt_tmp._setLegendLabels()
        jmt_tmp.histoMgr.setHistoDrawStyleAll("P") 
        jmt_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))
        jmt = jmt_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        jmt.Scale(normData[ptbin])
#        hmt.append(mt)        
        jmtEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/NJetInvertedTauIdJet"+ptbin)])
        jmtEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        jmtEWK_tmp._setLegendStyles()
        jmtEWK_tmp._setLegendLabels()
        jmtEWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
        jmtEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))
        jmtEWK = jmtEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        jmtEWK.Scale(normEWK[ptbin])
        jmt.Add(jmtEWK, -1)
        hjet.append(jmt)

        
        jmmt_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/NJetInvertedTauIdJetMet"+ptbin)])
        jmmt_tmp._setLegendStyles()
        jmmt_tmp._setLegendLabels()
        jmmt_tmp.histoMgr.setHistoDrawStyleAll("P") 
        jmmt_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))
        jmmt = jmmt_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        jmmt.Scale(normData[ptbin])
#        hmt.append(mt)        
        jmmtEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/NJetInvertedTauIdJetMet"+ptbin)])
        jmmtEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        jmmtEWK_tmp._setLegendStyles()
        jmmtEWK_tmp._setLegendLabels()
        jmmtEWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
        jmmtEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))
        jmmtEWK = jmmtEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        jmmtEWK.Scale(normEWK[ptbin])
        jmmt.Add(jmmtEWK, -1)
        hjetmet.append(jmmt)
        
        jmmtp_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/ClosestDeltaPhiInverted"+ptbin)])
        jmmtp_tmp._setLegendStyles()
        jmmtp_tmp._setLegendLabels()
        jmmtp_tmp.histoMgr.setHistoDrawStyleAll("P") 
        jmmtp_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))
        jmmtp = jmmtp_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        jmmtp.Scale(normData[ptbin])
#        hmt.append(mt)        
        jmmtpEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/ClosestDeltaPhiInverted"+ptbin)])
        jmmtpEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        jmmtpEWK_tmp._setLegendStyles()
        jmmtpEWK_tmp._setLegendLabels()
        jmmtpEWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
        jmmtpEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))
        jmmtpEWK = jmmtpEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        jmmtpEWK.Scale(normEWK[ptbin])
        jmmtp.Add(jmmtpEWK, -1)
        hjetmetphi.append(jmmtp)


        phi2_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/ClosestDeltaPhiTauVSMetInverted"+ptbin)])
        phi2_tmp._setLegendStyles()
        phi2_tmp._setLegendLabels()
        phi2_tmp.histoMgr.setHistoDrawStyleAll("P") 
        phi2_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))
        phi2 = phi2_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        phi2.Scale(normData[ptbin])
#        hmt.append(mt)        
        phi2EWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/ClosestDeltaPhiTauVSMetInverted"+ptbin)])
        phi2EWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        phi2EWK_tmp._setLegendStyles()
        phi2EWK_tmp._setLegendLabels()
        phi2EWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
        phi2EWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))
        phi2EWK = phi2EWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        phi2EWK.Scale(normEWK[ptbin])
        phi2.Add(phi2EWK, -1)
        hphi2.append(phi2)

        if True:
            # DeltaPhi Vs DeltaPhiMHTJet1Inverted
            MHTJet1phi_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/DeltaPhiMHTJet1Inverted"+ptbin)])
            MHTJet1phi_tmp._setLegendStyles()
            MHTJet1phi_tmp._setLegendLabels()
            MHTJet1phi_tmp.histoMgr.setHistoDrawStyleAll("P") 
            MHTJet1phi_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))
            MHTJet1phi = MHTJet1phi_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
            MHTJet1phi.Scale(normData[ptbin])
            #        hmt.append(mt)        
            MHTJet1phiEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/DeltaPhiMHTJet1Inverted"+ptbin)])
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
            
    mt = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdPhi")])
    mtBaseline = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTBaseLineTauIdPhi")])
    mtvBaseline = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTBaseLineTauIdBveto")])
    mtPhivBaseline = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTBaseLineTauIdBvetoDphi")]) 
    mtEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MTBaseLineTauIdPhi")])
    mtvEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MTBaseLineTauIdBveto")]) 
    mtPhivEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MTBaseLineTauIdBvetoDphi")])
#    jmmtpEWKbaseline = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/ClosestDeltaPhiBaseline")])
  

     
    mtEWKinverted = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MTInvertedTauIdPhi")])
    mtEWKinverted.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mtEWKinverted._setLegendStyles()
    mtEWKinverted._setLegendLabels()
    mtEWKinverted.histoMgr.setHistoDrawStyleAll("P")
    mtEWKinverted.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))  
    hmtEWKinverted = mtEWKinverted.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MTInvertedTauIdJetPhi")
    # norm = Norm_overall *(1-QCDfract) (0.034446/0.87 * 0.13 = 0.0051
    hmtEWKinverted.Scale(normEWK_inc)
    
    mt._setLegendStyles()
    mt._setLegendLabels()
    mt.histoMgr.setHistoDrawStyleAll("P")
    mt.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))  
    hmt = mt.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJetPhi")
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
    hmtBaseline = mtBaseline.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTBaselineTauIdJetPhi")
    
    mtEWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mtEWK._setLegendStyles()
    mtEWK._setLegendLabels()
    mtEWK.histoMgr.setHistoDrawStyleAll("P")
    mtEWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))  
    hmtEWK = mtEWK.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MTBaselineTauIdJetPhi")
    

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
    tex6 = ROOT.TLatex(0.55,0.55,"#Delta#phi(MHT,jet2) > 30^{o}")
    tex6.SetNDC()
    tex6.SetTextSize(20)
#    tex6.Draw()    
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
    hmtSum.GetYaxis().SetTitle("Events / 10 GeV/c^{2}")
    canvas32.Print("transverseMass.png")
    canvas32.Print("transverseMass.C")

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
    tex2.Draw()
#    tex3 = ROOT.TLatex(0.55,0.75,"#Delta#phi(#tau jet, Met) < 160^{o}")
#    tex3 = ROOT.TLatex(0.55,0.75,"2 Dim #Delta#phi cut")
    tex3 = ROOT.TLatex(0.55,0.75,"No #Delta#phi cut")
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
    
    hmtSumb.GetYaxis().SetTitleOffset(1.5)
    hmtSumb.GetXaxis().SetTitle("m_{T}(#tau jet, MET) (GeV/c^{2})")
    hmtSumb.GetYaxis().SetTitle("Events / 10 GeV/c^{2}")
    canvas72.Print("transverseMassAfterBtagging.png")
    canvas72.Print("transverseMassAfterBtagging.C")

    
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
    tex3.Draw()
    tex5 = ROOT.TLatex(0.55,0.65,"#Delta#phi(MHT,jet1) > 60^{o}")
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
    canvas74.Print("transverseMassDeltaPhiVsHMTJet1Cut.png")
    canvas74.Print("transverseMassDeltaPhiVsHMTJet1Cut.C")


    
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
    tex5 = ROOT.TLatex(0.55,0.65,"#Delta#phi(MHT,jet2) > 60^{o}")
    tex5.SetNDC()
    tex5.SetTextSize(20)
#    tex5.Draw()
    
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
    mtHMTjet2Cut.GetYaxis().SetTitle("Events / 10 GeV/c^{2}")
    canvas75.Print("transverseMassDeltaPhiVsHMTJet2Cut.png")
    canvas75.Print("transverseMassDeltaPhiVsHMTJet2Cut.C")
        
####################################################    
##  mT with b veto 
   
    mtvBaseline._setLegendStyles()
    mtvBaseline._setLegendLabels()
    mtvBaseline.histoMgr.setHistoDrawStyleAll("P")
    mtvBaseline.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))  
    hmtvBaseline = mtvBaseline.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTBaselineTauIdBveto")
    
    mtvEWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mtvEWK._setLegendStyles()
    mtvEWK._setLegendLabels()
    mtvEWK.histoMgr.setHistoDrawStyleAll("P")
    mtvEWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))  
    hmtvEWK = mtvEWK.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MTBaselineTauIdBveto")
    
   

    
    hmtvBaseline_QCD = hmtvBaseline.Clone("QCD")
    hmtvBaseline_QCD.Add(hmtvEWK,-1)
          
    invertedQCD = InvertedTauID()
    invertedQCD.setLumi(datasets.getDataset("Data").getLuminosity())
#    invertedQCD.useErrorBars(errorBars)
    invertedQCD.setLabel("MtBVeto")
    invertedQCD.comparison(hmtvSum,hmtvBaseline_QCD, -1)   
    
##  mT with b veto and Dphi cut 
   
    mtPhivBaseline._setLegendStyles()
    mtPhivBaseline._setLegendLabels()
    mtPhivBaseline.histoMgr.setHistoDrawStyleAll("P")
    mtPhivBaseline.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))  
    hmtPhivBaseline = mtPhivBaseline.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTBaselineTauIdBvetoDphi")
    
    mtPhivEWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mtPhivEWK._setLegendStyles()
    mtPhivEWK._setLegendLabels()
    mtPhivEWK.histoMgr.setHistoDrawStyleAll("P")
    mtPhivEWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))  
    hmtPhivEWK = mtPhivEWK.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MTBaselineTauIdBvetoDphi")
    
   

    
    hmtPhivBaseline_QCD = hmtPhivBaseline.Clone("QCD")
    hmtPhivBaseline_QCD.Add(hmtPhivEWK,-1)
          
    invertedQCD = InvertedTauID()
    invertedQCD.setLumi(datasets.getDataset("Data").getLuminosity())
#    invertedQCD.useErrorBars(errorBars)
    invertedQCD.setLabel("MtPhiBVeto")
    invertedQCD.comparison(hmtPhivSum,hmtPhivBaseline_QCD, -1)   
    
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

    mmt = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets")])        
    mmtBaseline = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_BaseLineTauIdJets")])
    mmtEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MET_BaseLineTauIdJets")])        
   
    mmtBaseline._setLegendStyles()
    mmtBaseline._setLegendLabels()
    mmtBaseline.histoMgr.setHistoDrawStyleAll("P")
    mmtBaseline.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(4))  
    hmmtBaseline = mmtBaseline.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTBaselineTauIdJetPhi")
    
    mmtEWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mmtEWK._setLegendStyles()
    mmtEWK._setLegendLabels()
    mmtEWK.histoMgr.setHistoDrawStyleAll("P")
    mmtEWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(4))  
    hmmtEWK = mmtEWK.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MTBaselineTauIdJetPhi")
    

       
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
    fmtBaseline = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/deltaPhiBaseline")])
    fmtEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/deltaPhiBaseline")])        


    fmtBaseline._setLegendStyles()
    fmtBaseline._setLegendLabels()
    fmtBaseline.histoMgr.setHistoDrawStyleAll("P")
    fmtBaseline.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))  
    hfmtBaseline = fmtBaseline.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTBaselineTauIdJetPhi")
    
    fmtEWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    fmtEWK._setLegendStyles()
    fmtEWK._setLegendLabels()
    fmtEWK.histoMgr.setHistoDrawStyleAll("P")
    fmtEWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))  
    hfmtEWK = fmtEWK.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MTBaselineTauIdJetPhi")
    

       
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
        canvas82.Print("DeltaPhiMHTjet1.png")
        canvas82.Print("DeltaPhiMHTjet1.C")

    
######## deltaPhi(jet,Met) vs deltaPhi(tau,Met) after 2dim cut
    if True:    
        phi2AfterCut = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/ClosestDeltaPhiTauVSMetInvertedAfterCut")])
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
        canvas55.Print("DeltaPhiJetMetVSTauMetAfterCut.png")
        canvas55.Print("DeltaPhiJetMetVSTauMetAfterCut.C")       

######## deltaPhi(jet,Met) vs deltaPhi(tau,Met) after 2dim cut
        
    phi2AfterCut2 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/DeltaPhiVsDeltaPhiMHTJet1Inverted")])
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
    hphi2AfterCut2.GetYaxis().SetTitle("#Delta#phi(jet1,MHT) (deg) ")
    canvas56.Print("DeltaPhiVSdeltaPhiMHTjet1.png")
    canvas56.Print("DeltaPhiVSdeltaPhiMHTjet1.C")
    
######## deltaPhi(jet,Met) vs deltaPhi(tau,Met) after 2dim cut

    phi2AfterCut3 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/DeltaPhiVsDeltaPhiMHTJet2Inverted")])
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
    hphi2AfterCut3.GetYaxis().SetTitle("#Delta#phi(jet2,MHT) (deg) ")
    canvas57.Print("DeltaPhiVSdeltaPhiMHTjet2.png")
    canvas57.Print("DeltaPhiVSdeltaPhiMHTjet2.C")

    
    ######## deltaPhi(jet,Met) vs deltaPhi(tau,Met) after 2dim cut

    phi2AfterCut4 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/DeltaPhiVsDeltaPhiMHTJet3Inverted")])
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
    hphi2AfterCut4.GetYaxis().SetTitle("#Delta#phi(jet3,MHT) (deg) ")
    canvas58.Print("DeltaPhiVSdeltaPhiMHTjet3.png")
    canvas58.Print("DeltaPhiVSdeltaPhiMHTjet3.C")
    
######## deltaPhi(jet,Met) vs deltaPhi(tau,MHT) after 2dim cut

    phiTauMHT = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/DeltaPhiMHTTauVsDeltaPhiMHTJet1Inverted")])
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
    
    hphiTauMHT.GetXaxis().SetTitle("#Delta#phi(#tau jet,MHT) (deg)")
    hphiTauMHT.GetYaxis().SetTitle("#Delta#phi(jet1,MHT) (deg) ")
    canvas59.Print("DeltaPhiHMTVSdeltaPhiMHTjet1.png")
    canvas59.Print("DeltaPhiHMTVSdeltaPhiMHTjet1.C")                                                                                                    
################## N bjets
    
    bhmt = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/NBInvertedTauIdJet")])
    bhmtBaseline = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/NBBaselineTauIdJet")])
    bhmtEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/NBBaselineTauIdJet")])
 
    bhmtBaseline._setLegendStyles()
    bhmtBaseline._setLegendLabels()
    bhmtBaseline.histoMgr.setHistoDrawStyleAll("P")
    bhmtBaseline.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))  
    hbhmtBaseline = bhmtBaseline.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/NBBaselineTauIdJet")
    
    bhmtEWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    bhmtEWK._setLegendStyles()
    bhmtEWK._setLegendLabels()
    bhmtEWK.histoMgr.setHistoDrawStyleAll("P")
    bhmtEWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))  
    hbhmtEWK =  bhmtEWK.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/NBBaselineTauIdJet")
    

       
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
      
 
    jBaseline = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/NJetBaselineTauIdJet")])
    jEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/NJetBaselineTauIdJet")])
 
    
    jBaseline._setLegendStyles()
    jBaseline._setLegendLabels()
    jBaseline.histoMgr.setHistoDrawStyleAll("P")
    jBaseline.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))  
    hjBaseline = jBaseline.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/NBBaselineTauIdJet")
    
    jEWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    jEWK._setLegendStyles()
    jEWK._setLegendLabels()
    jEWK.histoMgr.setHistoDrawStyleAll("P")
    jEWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))  
    hjEWK =  jEWK.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/NBBaselineTauIdJet")
    

       
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
    

    jm = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/NJetInvertedTauIdJetMet")])
    jmBaseline = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/NJetBaselineTauIdJetMet")])
    jmEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/NJetBaselineTauIdJetMet")])
 
 
    jmBaseline._setLegendStyles()
    jmBaseline._setLegendLabels()
    jmBaseline.histoMgr.setHistoDrawStyleAll("P")
    jmBaseline.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))  
    hjmBaseline = jmBaseline.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/NBBaselineTauIdJet")
    
    jmEWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    jmEWK._setLegendStyles()
    jmEWK._setLegendLabels()
    jmEWK.histoMgr.setHistoDrawStyleAll("P")
    jmEWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))  
    hjmEWK =  jmEWK.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/NBBaselineTauIdJet")
    

       
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
