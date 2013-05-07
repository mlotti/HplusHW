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

optMode = "OptQCDTailKillerLoose"
#optMode = ""


#dataEra = "Run2011A"
#dataEra = "Run2011B"
dataEra = "Run2011AB"

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


    mtTailKiller = []

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


    
## histograms in bins, normalisation and substraction of EWK contribution
    ## mt with 2dim deltaPhi cut
    for ptbin in ptbins:
        ## -------------   mt with tailkiller -----------
        mt_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MTInvertedAllCutsTailKiller"+ptbin)])
        #mt_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("MTInvertedTauIdPhi"+ptbin)])
        mt_tmp._setLegendStyles()
        mt_tmp._setLegendLabels()
        mt_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mt_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mt = mt_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        mt.Scale(normData[ptbin])
#        hmt.append(mt)        
        mtEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MTInvertedAllCutsTailKiller"+ptbin)])
        #mtEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("MTInvertedTauIdPhi"+ptbin)])
        mtEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mtEWK_tmp._setLegendStyles()
        mtEWK_tmp._setLegendLabels()
        mtEWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mtEWK = mtEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        mtEWK.Scale(normEWK[ptbin])
        mt.Add(mtEWK, -1)
        mtTailKiller.append(mt)
        
        ### MET
        mmt_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MET_InvertedTauIdJets"+ptbin)])
        mmt_tmp._setLegendStyles()
        mmt_tmp._setLegendLabels()
        mmt_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mmt_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(4))
        mmt = mmt_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        mmt.Scale(normData[ptbin])
#        hmt.append(mt)

        mmtEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MET_InvertedTauIdJets"+ptbin)])
        mmtEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mmtEWK_tmp._setLegendStyles()
        mmtEWK_tmp._setLegendLabels()
        mmtEWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mmtEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(4))
        mmtEWK = mmtEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        mmtEWK.Scale(normEWK[ptbin])
        mmt.Add(mmtEWK, -1)
        hmet.append(mmt)

        #### deltaPhi
        fmt_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/DeltaPhiInverted"+ptbin)])
        fmt_tmp._setLegendStyles()
        fmt_tmp._setLegendLabels()
        fmt_tmp.histoMgr.setHistoDrawStyleAll("P") 
        fmt_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
        fmt = fmt_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        fmt.Scale(normData[ptbin])
#        hmt.append(mt)        
        fmtEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/DeltaPhiInverted"+ptbin)])
        fmtEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        fmtEWK_tmp._setLegendStyles()
        fmtEWK_tmp._setLegendLabels()
        fmtEWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
        fmtEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
        fmtEWK = fmtEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        fmtEWK.Scale(normEWK[ptbin])
        fmt.Add(fmtEWK, -1)
        hdeltaPhi.append(fmt)

        ###### Higgs mass
#        hmt_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/HiggsMass")])

        hmt_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/HiggsMass"+ptbin)])
        hmt_tmp._setLegendStyles()
        hmt_tmp._setLegendLabels()
        hmt_tmp.histoMgr.setHistoDrawStyleAll("P") 
        hmt_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))
        mass = hmt_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        mass.Scale(normData[ptbin])
#        hmt.append(mt)
#        hmtEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/HiggsMass4050")])
        hmtEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/HiggsMass"+ptbin)])
        hmtEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        hmtEWK_tmp._setLegendStyles()
        hmtEWK_tmp._setLegendLabels()
        hmtEWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
        hmtEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))
        massEWK = hmtEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        massEWK.Scale(normEWK[ptbin])
        mass.Add(massEWK, -1)
        hmass.append(mass)

## N bjets
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

## N jets
        jmt_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/NJetInvertedTauId"+ptbin)])
        jmt_tmp._setLegendStyles()
        jmt_tmp._setLegendLabels()
        jmt_tmp.histoMgr.setHistoDrawStyleAll("P") 
        jmt_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))
        jmt = jmt_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        jmt.Scale(normData[ptbin])
#        hmt.append(mt)        
        jmtEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/NJetInvertedTauId"+ptbin)])
        jmtEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        jmtEWK_tmp._setLegendStyles()
        jmtEWK_tmp._setLegendLabels()
        jmtEWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
        jmtEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))
        jmtEWK = jmtEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        jmtEWK.Scale(normEWK[ptbin])
        jmt.Add(jmtEWK, -1)
        hjet.append(jmt)


        ### N jet after met cut
        jmmt_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/NJetInvertedTauIdMet"+ptbin)])
        jmmt_tmp._setLegendStyles()
        jmmt_tmp._setLegendLabels()
        jmmt_tmp.histoMgr.setHistoDrawStyleAll("P") 
        jmmt_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))
        jmmt = jmmt_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        jmmt.Scale(normData[ptbin])
#        hmt.append(mt)        
        jmmtEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/NJetInvertedTauIdMet"+ptbin)])
        jmmtEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        jmmtEWK_tmp._setLegendStyles()
        jmmtEWK_tmp._setLegendLabels()
        jmmtEWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
        jmmtEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))
        jmmtEWK = jmmtEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        jmmtEWK.Scale(normEWK[ptbin])
        jmmt.Add(jmmtEWK, -1)
        hjetmet.append(jmmt)


## sum histo bins     
    hmtSum = mtTailKiller[0].Clone("mtSum")
    hmtSum.SetName("transverseMass")
    hmtSum.SetTitle("Inverted tau ID")
    hmtSum.Reset()
    print "check hmtsum",hmtSum.GetEntries()
    for histo in mtTailKiller:
        hmtSum.Add(histo)  
    print "Integral: TailKiller cut- EWK = ",hmtSum.Integral()



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
        


    jetmet = hjetmet[0].Clone("jetmet")
    jetmet.SetName("NjetsAfterMET")
    jetmet.SetTitle("Inverted tau jet after Met")
    jetmet.Reset()
    print "check jetmet",jetmet.GetEntries()
    for histo in hjetmet:
        jetmet.Add(histo)


 
 ################## Control Plots and comparison with baseline(data-EWK) 

 ## mt baseline, plots and EWK substraction
            
    mtTailKillerInclusive = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MTInvertedAllCutsTailKiller")])
    
    mtEWKinverted = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MTInvertedAllCutsTailKiller")])
    mtEWKinverted.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mtEWKinverted._setLegendStyles()
    mtEWKinverted._setLegendLabels()
    mtEWKinverted.histoMgr.setHistoDrawStyleAll("P")
    mtEWKinverted.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))  
    hmtEWKinverted = mtEWKinverted.histoMgr.getHisto("EWK").getRootHisto().Clone("Inverted/MTInvertedAllCutsTailKiller")
    hmtEWKinverted.Scale(normEWK_inc)

 
    mtTailKillerInclusive._setLegendStyles()
    mtTailKillerInclusive._setLegendLabels()
    mtTailKillerInclusive.histoMgr.setHistoDrawStyleAll("P")
    mtTailKillerInclusive.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))  
    hmtTailKillerInclusive  = mtTailKillerInclusive.histoMgr.getHisto("Data").getRootHisto().Clone("Inverted/MTInvertedAllCutsTailKiller")
    hmtTailKillerInclusive.Scale(norm_inc)



    canvas39 = ROOT.TCanvas("canvas39","",500,500)            
    hmtTailKillerInclusive.SetMarkerColor(4)
    hmtTailKillerInclusive.SetMarkerSize(1)
    hmtTailKillerInclusive.SetMarkerStyle(20)
    hmtTailKillerInclusive.SetFillColor(4)
    hmtTailKillerInclusive.Draw("EP")
    
    hmt_subs = hmtTailKillerInclusive.Clone("QCD")
    hmt_subs.Add(hmtEWKinverted,-1)
    hmt_subs.SetMarkerColor(2)
    hmt_subs.SetMarkerSize(1)
    hmt_subs.SetMarkerStyle(21)
    hmt_subs.Draw("same")

    
    tex2 = ROOT.TLatex(0.55,0.85,"Inverted #tau isolation")
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw()    
    marker2 = ROOT.TMarker(0.5,0.865,hmtTailKillerInclusive.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(hmtTailKillerInclusive.GetMarkerColor())
    marker2.SetMarkerSize(0.9*hmtTailKillerInclusive.GetMarkerSize())
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
    
    hmtTailKillerInclusive.GetYaxis().SetTitleOffset(1.5)
    hmtTailKillerInclusive.GetXaxis().SetTitle("m_{T}(#tau jet, MET) (GeV/c^{2})")
    hmtTailKillerInclusive.GetYaxis().SetTitle("Events / 10 GeV/c^{2}")
    canvas39.Print("transverseMassInclusive.png")
    canvas39.Print("transverseMassInclusive.C")
    print " "
    print "Integral inclusive, tailKiller = ",hmtTailKillerInclusive.Integral()
    print "Integral inclusive - EWK, tailKiller = ",hmt_subs.Integral()
    print " "

################################################

#####  -------------- Comparison plots --------------------

  
    invertedQCD = InvertedTauID()
    invertedQCD.setLumi(datasets.getDataset("Data").getLuminosity())
          
#################################################
 ##  mT with TailKiller cuts
    mtBaseline = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("BaseLine/MTBaseLineTauIdAllCutsTailKiller")])         
    mtBaseline._setLegendStyles()
    mtBaseline._setLegendLabels()
    mtBaseline.histoMgr.setHistoDrawStyleAll("P")
    mtBaseline.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))  
    hmtBaseline = mtBaseline.histoMgr.getHisto("Data").getRootHisto().Clone("BaseLine/MTBaseLineTauIdAllCutsTailKiller")
    
    mtEWKBaseline = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("BaseLine/MTBaseLineTauIdAllCutsTailKiller")])   
    mtEWKBaseline.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mtEWKBaseline._setLegendStyles()
    mtEWKBaseline._setLegendLabels()
    mtEWKBaseline.histoMgr.setHistoDrawStyleAll("P")
    mtEWKBaseline.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))  
    hmtEWK = mtEWKBaseline.histoMgr.getHisto("EWK").getRootHisto().Clone("BaseLine/MTBaseLineTauIdAllCutsTailKiller")

    
    hmtBaseline_QCD = hmtBaseline.Clone("QCD")
    hmtBaseline_QCD.Add(hmtEWK,-1)

    invertedHisto = hmtSum.Clone("mtSum")
    baselineHisto = hmtBaseline_QCD.Clone("mtBaseline_QCD")
    print "invertedHisto ",invertedHisto.GetEntries()
    print "baselineHisto ",invertedHisto.GetEntries()
    invertedQCD.setLabel("MtInvertedVsBaselineTailKiller")
    invertedQCD.controlPlots(invertedHisto, baselineHisto,"MtInvertedVsBaseLineTailKiller")



#######################################

## MET       
    mmtBaseline = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("BaseLine/MET_BaseLineTauIdJets")])
    mmtEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("BaseLine/MET_BaseLineTauIdJets")])        
   
    mmtBaseline._setLegendStyles()
    mmtBaseline._setLegendLabels()
    mmtBaseline.histoMgr.setHistoDrawStyleAll("P")
    mmtBaseline.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(4))  
    hmmtBaseline = mmtBaseline.histoMgr.getHisto("Data").getRootHisto().Clone("BaseLine/MTBaseLineTauIdJets")
    
    mmtEWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mmtEWK._setLegendStyles()
    mmtEWK._setLegendLabels()
    mmtEWK.histoMgr.setHistoDrawStyleAll("P")
    mmtEWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(4))  
    hmmtEWK = mmtEWK.histoMgr.getHisto("EWK").getRootHisto().Clone("BaseLine/MTBaselineTauIdJets")

    hmet_QCD = hmmtBaseline.Clone("QCD")
    hmet_QCD.Add(hmmtEWK,-1)
    
    invertedHisto = met.Clone("met")
    baselineHisto = hmet_QCD.Clone("met_QCD")    
    print "invertedHisto ",invertedHisto.GetEntries()
    print "baselineHisto ",invertedHisto.GetEntries()
    invertedQCD.setLabel("MetInvertedVsBaselineTailKiller")
    invertedQCD.controlPlots(invertedHisto, baselineHisto,"MetInvertedVsBaselineTailKiller")
#######################################


    canvas32 = ROOT.TCanvas("canvas32","",500,500)    
    hmtSum.SetMarkerColor(4)
    hmtSum.SetMarkerSize(1)
    hmtSum.SetMarkerStyle(20)
    hmtSum.SetFillColor(4)
    hmtSum.Draw("EP")
    
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

    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       5.05 fb^{-1}       CMS Preliminary ")
#    tex4 = ROOT.TLatex(0.2,0.95,"8 TeV       12.2 fb^{-1}       CMS Preliminary ")    
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    hmtSum.GetYaxis().SetTitleOffset(1.5)
    hmtSum.GetXaxis().SetTitle("m_{T}(#tau jet, MET) (GeV/c^{2})")
    hmtSum.GetYaxis().SetTitle("Events / 20 GeV/c^{2}")
#    canvas32.Print("transverseMass.png")
#    canvas32.Print("transverseMass.C")
    canvas32.Print("transverseMassTailKiller.png")
    canvas32.Print("transverseMassTailKiller.C")

####################################################
#Circle cuts inclusive - EWK
    Rcut_jet1_BackToBack = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("QCDTailKiller/BackToBackSystem/CircleCut_BackToBackJet1")])
    Rcut_jet1_BackToBack._setLegendStyles()
    Rcut_jet1_BackToBack._setLegendLabels()
    Rcut_jet1_BackToBack.histoMgr.setHistoDrawStyleAll("P")
    Rcut_jet1_BackToBack.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))  
    hRcut_jet1_BackToBack = Rcut_jet1_BackToBack.histoMgr.getHisto("Data").getRootHisto().Clone("QCDTailKiller/BackToBackSystem/CircleCut_BackToBackJet1")
    
    Rcut_jet1_BackToBackEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("QCDTailKiller/BackToBackSystem/CircleCut_BackToBackJet1")])   
    Rcut_jet1_BackToBackEWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    Rcut_jet1_BackToBackEWK._setLegendStyles()
    Rcut_jet1_BackToBackEWK._setLegendLabels()
    Rcut_jet1_BackToBackEWK.histoMgr.setHistoDrawStyleAll("P")
    Rcut_jet1_BackToBackEWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))  
    hRcut_jet1_BackToBackEWK = Rcut_jet1_BackToBackEWK.histoMgr.getHisto("EWK").getRootHisto().Clone("QCDTailKiller/BackToBackSystem/CircleCut_BackToBackJet1")
    
    hRcut_jet1_BackToBack_QCD = hRcut_jet1_BackToBack.Clone("QCD")
    hRcut_jet1_BackToBack_QCD.Add(hRcut_jet1_BackToBackEWK,-1)



    canvas390 = ROOT.TCanvas("canvas390","",500,500)            
    hRcut_jet1_BackToBack_QCD.SetMarkerColor(4)
    hRcut_jet1_BackToBack_QCD.SetMarkerSize(1)
    hRcut_jet1_BackToBack_QCD.SetMarkerStyle(20)
    hRcut_jet1_BackToBack_QCD.SetFillColor(4)
    hRcut_jet1_BackToBack_QCD.Draw("EP")
        
    tex9 = ROOT.TLatex(0.2,0.78,"Jet1") 
    tex9.SetNDC()
    tex9.SetTextSize(20)
    tex9.Draw()
    marker9 = ROOT.TMarker(0.5,0.795,hRcut_jet1_BackToBack_QCD.GetMarkerStyle())
    marker9.SetNDC()
    marker9.SetMarkerColor(hRcut_jet1_BackToBack_QCD.GetMarkerColor())
    marker9.SetMarkerSize(0.9*hRcut_jet1_BackToBack_QCD.GetMarkerSize())
#    marker9.Draw()
    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       5.05 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    

    canvas390.Print("CircleCut_BackToBackJet1.png")
    canvas390.Print("CircleCut_BackToBackJet1.C")

    ####################
    Rcut_jet2_BackToBack = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("QCDTailKiller/BackToBackSystem/CircleCut_BackToBackJet2")])
    Rcut_jet2_BackToBack._setLegendStyles()
    Rcut_jet2_BackToBack._setLegendLabels()
    Rcut_jet2_BackToBack.histoMgr.setHistoDrawStyleAll("P")
    Rcut_jet2_BackToBack.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))  
    hRcut_jet2_BackToBack = Rcut_jet2_BackToBack.histoMgr.getHisto("Data").getRootHisto().Clone("QCDTailKiller/BackToBackSystem/CircleCut_BackToBackJet2")
    
    Rcut_jet2_BackToBackEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("QCDTailKiller/BackToBackSystem/CircleCut_BackToBackJet2")])   
    Rcut_jet2_BackToBackEWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    Rcut_jet2_BackToBackEWK._setLegendStyles()
    Rcut_jet2_BackToBackEWK._setLegendLabels()
    Rcut_jet2_BackToBackEWK.histoMgr.setHistoDrawStyleAll("P")
    Rcut_jet2_BackToBackEWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))  
    hRcut_jet2_BackToBackEWK = Rcut_jet2_BackToBackEWK.histoMgr.getHisto("EWK").getRootHisto().Clone("QCDTailKiller/BackToBackSystem/CircleCut_BackToBackJet2")
    
    hRcut_jet2_BackToBack_QCD = hRcut_jet2_BackToBack.Clone("QCD")
    hRcut_jet2_BackToBack_QCD.Add(hRcut_jet2_BackToBackEWK,-1)



    canvas3900 = ROOT.TCanvas("canvas3900","",500,500)            
    hRcut_jet2_BackToBack_QCD.SetMarkerColor(4)
    hRcut_jet2_BackToBack_QCD.SetMarkerSize(1)
    hRcut_jet2_BackToBack_QCD.SetMarkerStyle(20)
    hRcut_jet2_BackToBack_QCD.SetFillColor(4)
    hRcut_jet2_BackToBack_QCD.Draw("EP")
        
    tex9 = ROOT.TLatex(0.6,0.78,"Jet2") 
    tex9.SetNDC()
    tex9.SetTextSize(20)
    tex9.Draw()
    marker9 = ROOT.TMarker(0.5,0.795,hRcut_jet2_BackToBack_QCD.GetMarkerStyle())
    marker9.SetNDC()
    marker9.SetMarkerColor(hRcut_jet2_BackToBack_QCD.GetMarkerColor())
    marker9.SetMarkerSize(0.9*hRcut_jet2_BackToBack_QCD.GetMarkerSize())
#    marker9.Draw()
    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       5.05 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    hRcut_jet2_BackToBack_QCD.GetYaxis().SetTitleOffset(1.5)
#    hRcut_jet2_BackToBack_QCD.GetXaxis().SetTitle("CircleCut_BackToBackJet1")
    hRcut_jet2_BackToBack_QCD.GetYaxis().SetTitle("Events")
    canvas3900.Print("CircleCut_BackToBackJet2.png")
    canvas3900.Print("CircleCut_BackToBackJet2.C")
    
  ####################
    Rcut_jet3_BackToBack = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("QCDTailKiller/BackToBackSystem/CircleCut_BackToBackJet3")])
    Rcut_jet3_BackToBack._setLegendStyles()
    Rcut_jet3_BackToBack._setLegendLabels()
    Rcut_jet3_BackToBack.histoMgr.setHistoDrawStyleAll("P")
    Rcut_jet3_BackToBack.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))  
    hRcut_jet3_BackToBack = Rcut_jet3_BackToBack.histoMgr.getHisto("Data").getRootHisto().Clone("QCDTailKiller/BackToBackSystem/CircleCut_BackToBackJet3")
    
    Rcut_jet3_BackToBackEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("QCDTailKiller/BackToBackSystem/CircleCut_BackToBackJet3")])   
    Rcut_jet3_BackToBackEWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    Rcut_jet3_BackToBackEWK._setLegendStyles()
    Rcut_jet3_BackToBackEWK._setLegendLabels()
    Rcut_jet3_BackToBackEWK.histoMgr.setHistoDrawStyleAll("P")
    Rcut_jet3_BackToBackEWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))  
    hRcut_jet3_BackToBackEWK = Rcut_jet3_BackToBackEWK.histoMgr.getHisto("EWK").getRootHisto().Clone("QCDTailKiller/BackToBackSystem/CircleCut_BackToBackJet3")
    
    hRcut_jet3_BackToBack_QCD = hRcut_jet3_BackToBack.Clone("QCD")
    hRcut_jet3_BackToBack_QCD.Add(hRcut_jet3_BackToBackEWK,-1)



    canvas3901 = ROOT.TCanvas("canvas3901","",500,500)            
    hRcut_jet3_BackToBack_QCD.SetMarkerColor(4)
    hRcut_jet3_BackToBack_QCD.SetMarkerSize(1)
    hRcut_jet3_BackToBack_QCD.SetMarkerStyle(20)
    hRcut_jet3_BackToBack_QCD.SetFillColor(4)
    hRcut_jet3_BackToBack_QCD.Draw("EP")
        
    tex9 = ROOT.TLatex(0.2,0.78,"Jet3") 
    tex9.SetNDC()
    tex9.SetTextSize(20)
    tex9.Draw()
    marker9 = ROOT.TMarker(0.5,0.795,hRcut_jet3_BackToBack_QCD.GetMarkerStyle())
    marker9.SetNDC()
    marker9.SetMarkerColor(hRcut_jet3_BackToBack_QCD.GetMarkerColor())
    marker9.SetMarkerSize(0.9*hRcut_jet3_BackToBack_QCD.GetMarkerSize())
#    marker9.Draw()
    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       5.05 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    hRcut_jet3_BackToBack_QCD.GetYaxis().SetTitleOffset(1.5)
###    hRcut_jet3_BackToBack_QCD.GetXaxis().SetTitle("CircleCut_BackToBackJet1")
    hRcut_jet3_BackToBack_QCD.GetYaxis().SetTitle("Events")
    canvas3901.Print("CircleCut_BackToBackJet3.png")
    canvas3901.Print("CircleCut_BackToBackJet3.C")
    ####################
    
    Rcut_jet1_Collinear = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("QCDTailKiller/CollinearSystem/CircleCut_CollinearJet1")])
    Rcut_jet1_Collinear._setLegendStyles()
    Rcut_jet1_Collinear._setLegendLabels()
    Rcut_jet1_Collinear.histoMgr.setHistoDrawStyleAll("P")
    Rcut_jet1_Collinear.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))  
    hRcut_jet1_Collinear = Rcut_jet1_Collinear.histoMgr.getHisto("Data").getRootHisto().Clone("QCDTailKiller/BackToBackSystem/CircleCut_CollinearJet1")
    
    Rcut_jet1_CollinearEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("QCDTailKiller/CollinearSystem/CircleCut_CollinearJet1")])   
    Rcut_jet1_CollinearEWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    Rcut_jet1_CollinearEWK._setLegendStyles()
    Rcut_jet1_CollinearEWK._setLegendLabels()
    Rcut_jet1_CollinearEWK.histoMgr.setHistoDrawStyleAll("P")
    Rcut_jet1_CollinearEWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))  
    hRcut_jet1_CollinearEWK = Rcut_jet1_CollinearEWK.histoMgr.getHisto("EWK").getRootHisto().Clone("QCDTailKiller/BackToBackSystem/CircleCut_CollinearJet1")
    
    hRcut_jet1_Collinear_QCD = hRcut_jet1_Collinear.Clone("QCD")
    hRcut_jet1_Collinear_QCD.Add(hRcut_jet1_CollinearEWK,-1)

    Rcut_jet2_Collinear = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("QCDTailKiller/CollinearSystem/CircleCut_CollinearJet2")])
    Rcut_jet2_Collinear._setLegendStyles()
    Rcut_jet2_Collinear._setLegendLabels()
    Rcut_jet2_Collinear.histoMgr.setHistoDrawStyleAll("P")
    Rcut_jet2_Collinear.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))  
    hRcut_jet2_Collinear = Rcut_jet2_Collinear.histoMgr.getHisto("Data").getRootHisto().Clone("QCDTailKiller/BackToBackSystem/CircleCut_CollinearJet2")
    
    Rcut_jet2_CollinearEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("QCDTailKiller/CollinearSystem/CircleCut_CollinearJet2")])   
    Rcut_jet2_CollinearEWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    Rcut_jet2_CollinearEWK._setLegendStyles()
    Rcut_jet2_CollinearEWK._setLegendLabels()
    Rcut_jet2_CollinearEWK.histoMgr.setHistoDrawStyleAll("P")
    Rcut_jet2_CollinearEWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))  
    hRcut_jet2_CollinearEWK = Rcut_jet2_CollinearEWK.histoMgr.getHisto("EWK").getRootHisto().Clone("QCDTailKiller/BackToBackSystem/CircleCut_CollinearJet2")
    
    hRcut_jet2_Collinear_QCD = hRcut_jet2_Collinear.Clone("QCD")
    hRcut_jet2_Collinear_QCD.Add(hRcut_jet2_CollinearEWK,-1)

    Rcut_jet3_Collinear = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("QCDTailKiller/CollinearSystem/CircleCut_CollinearJet3")])
    Rcut_jet3_Collinear._setLegendStyles()
    Rcut_jet3_Collinear._setLegendLabels()
    Rcut_jet3_Collinear.histoMgr.setHistoDrawStyleAll("P")
    Rcut_jet3_Collinear.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))  
    hRcut_jet3_Collinear = Rcut_jet3_Collinear.histoMgr.getHisto("Data").getRootHisto().Clone("QCDTailKiller/BackToBackSystem/CircleCut_CollinearJet3")
    
    Rcut_jet3_CollinearEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("QCDTailKiller/CollinearSystem/CircleCut_CollinearJet3")])   
    Rcut_jet3_CollinearEWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    Rcut_jet3_CollinearEWK._setLegendStyles()
    Rcut_jet3_CollinearEWK._setLegendLabels()
    Rcut_jet3_CollinearEWK.histoMgr.setHistoDrawStyleAll("P")
    Rcut_jet3_CollinearEWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))  
    hRcut_jet3_CollinearEWK = Rcut_jet3_CollinearEWK.histoMgr.getHisto("EWK").getRootHisto().Clone("QCDTailKiller/BackToBackSystem/CircleCut_CollinearJet3")
    
    hRcut_jet3_Collinear_QCD = hRcut_jet3_Collinear.Clone("QCD")
    hRcut_jet3_Collinear_QCD.Add(hRcut_jet3_CollinearEWK,-1)
    

    canvas390 = ROOT.TCanvas("canvas391","",500,500)            
    hRcut_jet1_Collinear_QCD.SetMarkerColor(2)
    hRcut_jet1_Collinear_QCD.SetMarkerSize(1)
    hRcut_jet1_Collinear_QCD.SetMarkerStyle(20)
    hRcut_jet1_Collinear_QCD.SetFillColor(2)
    hRcut_jet1_Collinear_QCD.Draw("EP")
    
    hRcut_jet2_Collinear_QCD.SetMarkerColor(4)
    hRcut_jet2_Collinear_QCD.SetMarkerSize(1)
    hRcut_jet2_Collinear_QCD.SetMarkerStyle(21)
    hRcut_jet2_Collinear_QCD.SetFillColor(4)
    hRcut_jet2_Collinear_QCD.Draw("same")

    hRcut_jet3_Collinear_QCD.SetMarkerColor(1)
    hRcut_jet3_Collinear_QCD.SetMarkerSize(1)
    hRcut_jet3_Collinear_QCD.SetMarkerStyle(25)
    hRcut_jet3_Collinear_QCD.SetFillColor(1)
    hRcut_jet3_Collinear_QCD.Draw("same")
    
    tex9 = ROOT.TLatex(0.75,0.85,"jet1") 
    tex9.SetNDC()
    tex9.SetTextSize(18)
    tex9.Draw()
    marker9 = ROOT.TMarker(0.73,0.86,hRcut_jet1_Collinear_QCD.GetMarkerStyle())
    marker9.SetNDC()
    marker9.SetMarkerColor(hRcut_jet1_Collinear_QCD.GetMarkerColor())
    marker9.SetMarkerSize(0.9*hRcut_jet1_Collinear_QCD.GetMarkerSize())
    marker9.Draw()


    tex2 = ROOT.TLatex(0.75,0.80,"jet2") 
    tex2.SetNDC()
    tex2.SetTextSize(18)
    tex2.Draw()
    marker2 = ROOT.TMarker(0.73,0.801,hRcut_jet2_Collinear_QCD.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(hRcut_jet2_Collinear_QCD.GetMarkerColor())
    marker2.SetMarkerSize(0.9*hRcut_jet2_Collinear_QCD.GetMarkerSize())
    marker2.Draw()
    
    tex3 = ROOT.TLatex(0.75,0.75,"jet3") 
    tex3.SetNDC()
    tex3.SetTextSize(18)
    tex3.Draw()
    marker3 = ROOT.TMarker(0.73,0.76,hRcut_jet3_Collinear_QCD.GetMarkerStyle())
    marker3.SetNDC()
    marker3.SetMarkerColor(hRcut_jet3_Collinear_QCD.GetMarkerColor())
    marker3.SetMarkerSize(0.9*hRcut_jet3_Collinear_QCD.GetMarkerSize())
    marker3.Draw()
    
    tex6 = ROOT.TLatex(0.2,0.85,"Collinear cuts ")
    tex6.SetNDC()
    tex6.SetTextSize(20)
    tex6.Draw()

    
    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       5.05 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    

    canvas391.Print("CircleCut_CollinearJet1.png")
    canvas391.Print("CircleCut_CollinearJet1.C")

    

       
    canvas34 = ROOT.TCanvas("canvas34","",500,500)
    canvas34.SetLogy()
    met.SetMarkerColor(4)
    met.SetMarkerSize(1)
    met.SetMarkerStyle(20)
    met.SetFillColor(4)    
    met.Draw("EP")
    
 
            
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
    
         
    met.GetXaxis().SetTitle("MET (GeV)")
    met.GetYaxis().SetTitle("Events / 20 GeV")
    canvas34.Print("MET.png")
    canvas34.Print("MET.C")


    

       
    canvas30 = ROOT.TCanvas("canvas30","",500,500)
    DeltaPhi.SetMarkerColor(4)
    DeltaPhi.SetMarkerSize(1)
    DeltaPhi.SetMarkerStyle(20)
    DeltaPhi.SetFillColor(4)    
    DeltaPhi.Draw("EP")
    
     
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

 
    canvas33 = ROOT.TCanvas("canvas33","",500,500)
    canvas33.SetLogy()
    frame33 = histograms._drawFrame(canvas33, xmin=0, xmax=6, ymin=0.01, ymax=1e4)
    frame33.Draw()
               
    NBjets.SetMarkerColor(4)
    NBjets.SetMarkerSize(1)
    NBjets.SetMarkerStyle(20)
    NBjets.SetFillColor(4)
    NBjets.Draw("EP same")

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
    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       5.05 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    
    NBjets.GetXaxis().SetTitle("N_{b jets}")
    NBjets.GetYaxis().SetTitle("Events  ")
    canvas33.Print("NBjets.png")
    canvas33.Print("NBjets.C")






          
# Njets
       
    canvas34 = ROOT.TCanvas("canvas34","",500,500)
    canvas34.SetLogy()
    frame34 = histograms._drawFrame(canvas33, xmin=0, xmax=10, ymin=1, ymax=1e5)
    frame34.Draw()
               
    Njets.SetMarkerColor(4)
    Njets.SetMarkerSize(1)
    Njets.SetMarkerStyle(20)
    Njets.SetFillColor(4)
    Njets.Draw("EP same")

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
    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       5.05 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    
    Njets.GetXaxis().SetTitle("N_{jets}")
    Njets.GetYaxis().SetTitle("Events  ")
    canvas34.Print("Njets.png")
    canvas34.Print("Njets.C")

################## N jets after MET
    
    canvas35 = ROOT.TCanvas("canvas35","",500,500)
    canvas35.SetLogy()
    frame35 = histograms._drawFrame(canvas33, xmin=0, xmax=10, ymin=1, ymax=1e4)
    frame35.Draw()
               
    NjetsAfterMET.SetMarkerColor(4)
    NjetsAfterMET.SetMarkerSize(1)
    NjetsAfterMET.SetMarkerStyle(20)
    NjetsAfterMET.SetFillColor(4)
    NjetsAfterMET.Draw("EP same")

             
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
