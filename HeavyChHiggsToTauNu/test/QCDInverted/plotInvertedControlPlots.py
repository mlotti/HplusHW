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

## for mT distributions 
deltaPhi180 = False
deltaPhi160 = True
deltaPhi130 = False
topmass = False  ## with top mass cut

btagFactorisation = False  # works with deltaPhi180=True

# other distributions
deltaPhiDistribution = False
numberOfBjets = False
HiggsMass = False
HiggsMassPhi140 = False

lastPtBin150 = False
lastPtBin120 = True

mcOnly = False
#mcOnly = True
mcOnlyLumi = 5000 # pb

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

   

 
    mtComparison(datasets)

def doCounters(datasets):
    eventCounter = counter.EventCounter(datasets)
    
    ewkDatasets = [
        "WJets", "TTJets",
        "DYJetsToLL", "SingleTop", "Diboson"
        ]

    # append row from the tree to the main counter
#    eventCounter.getMainCounter().appendRow("MET > 70", treeDraw.clone(selection="met_p4.Et() > 70"))

    eventCounter.normalizeMCByLuminosity()
#    eventCounter.normalizeMCToLuminosity(73)
    print "============================================================"
    print "Main counter (MC normalized by collision data luminosity)"
    mainTable = eventCounter.getMainCounterTable()
#    mainTable.insertColumn(2, counter.sumColumn("EWKMCsum", [mainTable.getColumn(name=name) for name in ewkDatasets]))
   # Default
#    cellFormat = counter.TableFormatText()
    # No uncertainties
    cellFormat = counter.TableFormatText(cellFormat=counter.CellFormatText(valueOnly=True))
    print mainTable.format(cellFormat)



#    print eventCounter.getSubCounterTable("GlobalMuon_ID").format()

#    print eventCounter.getSubCounterTable("tauIDTauSelection").format()
#    print eventCounter.getSubCounterTable("TauIDPassedEvt::tauID_HPSTight").format()
#    print eventCounter.getSubCounterTable("TauIDPassedJets::tauID_HPSTight").format()
    print eventCounter.getSubCounterTable("b-tagging").format(cellFormat)
    print eventCounter.getSubCounterTable("Jet selection").format(cellFormat)
    print eventCounter.getSubCounterTable("Jet main").format(cellFormat)    
#    print eventCounter.getSubCounterTable("VetoTauSelection").format(cellFormat)
#    print eventCounter.getSubCounterTable("top").format(cellFormat)
    
    
#    latexFormat = counter.TableFormatConTeXtTABLE(counter.CellFormatTeX(valueFormat="%.2f"))
#    print eventCounter.getMainCounterTable().format(latexFormat)


#def vertexComparison(datasets):
#    signal = "TTToHplusBWB_M120_Summer11"
#    background = "TTToHplusBWB_M120_Summer11"
#    rtauGen(plots.ComparisonPlot(datasets.getDataset(signal).getDatasetRootHisto(analysis+"/verticesBeforeWeight"),
#                                 datasets.getDataset(background).getDatasetRootHisto(analysis+"/verticesAfterWeight")),
#            "vertices_H120")

try:
    from QCDInvertedNormalizationFactors import *
    norm_inc = QCDInvertedNormalization["inclusive"]
    norm_4050 = QCDInvertedNormalization["4050"]
    norm_5060 = QCDInvertedNormalization["5060"]        
    norm_6070 = QCDInvertedNormalization["6070"]
    norm_7080 = QCDInvertedNormalization["7080"]
    norm_80100 = QCDInvertedNormalization["80100"]
    norm_100120 = QCDInvertedNormalization["100120"]
    if lastPtBin150: 
        norm_120150 = QCDInvertedNormalization["120150"]
        norm_150 = QCDInvertedNormalization["150"]
    if lastPtBin120: 
        norm_120 = QCDInvertedNormalization["120"]
    print "inclusive norm", norm_inc
    print "norm factors", norm_4050,norm_5060,norm_6070,norm_7080,norm_80100,norm_100120,norm_120

    
    from QCDInvertedBtaggingFactors import *
    btag_inc = btaggingFactors["inclusive"]
    btag_4050 = btaggingFactors["4050"]
    btag_5060 = btaggingFactors["5060"]        
    btag_6070 = btaggingFactors["6070"]
    btag_7080 = btaggingFactors["7080"]
    btag_80100 = btaggingFactors["80100"]
    btag_100120 = btaggingFactors["100120"]
    if lastPtBin150: 
        btag_120150 = btaggingFactors["120150"]
        btag_150 = btaggingFactors["150"]
    if lastPtBin120: 
        btag_120 = btaggingFactors["120"]
    print "inclusive b tag eff",btag_inc
    print "btag efficiencies",btag_4050,btag_5060,btag_6070,btag_7080,btag_80100,btag_100120,btag_120


    if (btagFactorisation):
        norm_inc = norm_inc * btag_inc
        norm_4050 = norm_4050 * btag_4050
        norm_5060 = norm_5060 * btag_5060
        norm_6070 = norm_6070 * btag_6070
        norm_7080 = norm_7080 * btag_7080
        norm_80100 = norm_80100 * btag_80100
        norm_100120 = norm_100120 * btag_100120
        norm_120 = norm_120 * btag_120
        
        print "inclusive norm with b tagging", norm_inc
        print "norm factors with b tagging ", norm_4050,norm_5060,norm_6070,norm_7080,norm_80100,norm_100120,norm_120


            
except ImportError:   
    print
    print "    WARNING, QCDInvertedNormalizationFactors.py not found!"
    print "    Run script InvertedTauID_Normalization.py to generate QCDInvertedNormalizationFactors.py"
    print
###    sys.exit()
    

        
###########################################
    ### Normalised mt and dphi distribution
def mtComparison(datasets):
    
    ## After standard cuts

        
    if (deltaPhi180):
        mt4050 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdBtag4050")])
        mt5060 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdBtag5060")])
        mt6070 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdBtag6070")])
        mt7080 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdBtag7080")])
        mt80100 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdBtag80100")])
        mt100120 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdBtag100120")])
        if lastPtBin150: 
            mt120150 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdBtag120150")])
            mt150 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdBtag150")])
        if lastPtBin120: 
            mt120 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdBtag120")])
        mt = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdBtag")])
        
        mtBaseline = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTBaseLineTauIdBtag")])
        mtEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MTBaseLineTauIdBtag")])

   
    if (topmass):
        mt4050 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdTopMass4050")])
        mt5060 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdTopMass5060")])
        mt6070 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdTopMass6070")])
        mt7080 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdTopMass7080")])
        mt80100 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdTopMass80100")])
        mt100120 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdTopMass100120")])
        if lastPtBin150:
            mt120150 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdTopMass120150")])
            mt150 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdTopMass150")])
        if lastPtBin120:
           mt120 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdTopMass120")])                
        mt = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdTopMass")])
        mtBaseline = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTBaseLineTauIdBtag")])
        mtEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MTBaseLineTauIdBtag")])


   

###### transverse mass
    mt4050 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdPhi4050")])
    mt5060 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdPhi5060")])
    mt6070 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdPhi6070")])
    mt7080 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdPhi7080")])
    mt80100 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdPhi80100")])
    mt100120 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdPhi100120")])
    if lastPtBin150:
        mt120150 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdPhi120150")])
        mt150 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdPhi150")])
    if lastPtBin120:
        mt120 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdPhi120")])
    mt = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdPhi")])
    mtBaseline = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTBaseLineTauIdPhi")])
    mtEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MTBaseLineTauIdPhi")]) 

    mt4050._setLegendStyles()
    mt4050._setLegendLabels()
    mt4050.histoMgr.setHistoDrawStyleAll("P")
    if (numberOfBjets):
        mt4050.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))
    else:
        mt4050.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
    hmt4050 = mt4050.histoMgr.getHisto("Data").getRootHisto().Clone()
    hmtSum2 = hmt4050.Clone("mtSum2")
    print "Integral 4050  = ",hmt4050.Integral()
    hmt4050.Scale(norm_4050) 

    
    mt5060._setLegendStyles()
    mt5060._setLegendLabels()
    mt5060.histoMgr.setHistoDrawStyleAll("P")
    if (numberOfBjets):
        mt5060.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))
    else:
        mt5060.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
    hmt5060 = mt5060.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJetPhi5060")
    hmtSum2.Add(hmt5060)
    print "Integral 5060  = ",hmt5060.Integral()
    hmt5060.Scale(norm_5060) 


    mt6070._setLegendStyles()
    mt6070._setLegendLabels()
    mt6070.histoMgr.setHistoDrawStyleAll("P")
    if (numberOfBjets):
        mt6070.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))
    else:
        mt6070.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))    
    hmt6070 = mt6070.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJetPhi6070")
    hmtSum2.Add(hmt6070)
    print "Integral 6070  = ",hmt6070.Integral()
    hmt6070.Scale(norm_6070) 

    
    mt7080._setLegendStyles()
    mt7080._setLegendLabels()
    mt7080.histoMgr.setHistoDrawStyleAll("P")
    if (numberOfBjets):
        mt7080.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))
    else:
        mt7080.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20)) 
    hmt7080 = mt7080.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJetPhi7080")
    hmtSum2.Add(hmt7080)
    print "Integral 7080  = ",hmt7080.Integral()
    hmt7080.Scale(norm_7080) 

    
    mt80100._setLegendStyles()
    mt80100._setLegendLabels()
    mt80100.histoMgr.setHistoDrawStyleAll("P")
    if (numberOfBjets):
        mt80100.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))
    else:
        mt80100.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20)) 
    hmt80100 = mt80100.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJetPhi80100")
    hmtSum2.Add(hmt80100)
    print "Integral 80100  = ",hmt80100.Integral()
    hmt80100.Scale(norm_80100) 

    
    mt100120._setLegendStyles()
    mt100120._setLegendLabels()
    mt100120.histoMgr.setHistoDrawStyleAll("P")
    if (numberOfBjets):
        mt100120.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))
    else:
        mt100120.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))     
    hmt100120 = mt100120.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJetPhi100120")
    hmtSum2.Add(hmt100120)
    print "Integral 100120  = ",hmt100120.Integral()    
    hmt100120.Scale(norm_100120) 


    if lastPtBin150:    
        mt120150._setLegendStyles()
        mt120150._setLegendLabels()
        mt120150.histoMgr.setHistoDrawStyleAll("P")
        if (numberOfBjets):
            mt120150.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))
        else:
            mt120150.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))      
        hmt120150 = mt120150.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJetPhi120150")
        hmtSum2.Add(hmt120150)
        print "Integral 120150  = ",hmt120150.Integral()
        hmt120150.Scale(norm_120150) 
        
        
        mt150._setLegendStyles()
        mt150._setLegendLabels()
        mt150.histoMgr.setHistoDrawStyleAll("P")
        if (numberOfBjets):
            mt150.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))
        else:
            mt150.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))  
        hmt150 = mt150.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJetPhi150")
        hmtSum2.Add(hmt150)
        print "Integral 150  = ",hmt150.Integral()
        hmt150.Scale(norm_150)
        
    if lastPtBin120:
        mt120._setLegendStyles()
        mt120._setLegendLabels()
        mt120.histoMgr.setHistoDrawStyleAll("P")
        if (numberOfBjets):
            mt120.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))
        else:
            mt120.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))  
        hmt120 = mt120.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJetPhi120")
        hmtSum2.Add(hmt120)
        print "Integral 120  = ",hmt120.Integral()
        hmt120.Scale(norm_120)

 ####################################          
    mt._setLegendStyles()
    mt._setLegendLabels()
    mt.histoMgr.setHistoDrawStyleAll("P")
    if (numberOfBjets):
        mt.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))
    else:
        mt.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))  
    hmt = mt.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJetPhi")
    hmt.Scale(norm_inc)

    
    mtBaseline._setLegendStyles()
    mtBaseline._setLegendLabels()
    mtBaseline.histoMgr.setHistoDrawStyleAll("P")
    mtBaseline.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))  
    hmtBaseline = mtBaseline.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTBaselineTauIdJetPhi")
    
    mtEWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mtEWK._setLegendStyles()
    mtEWK._setLegendLabels()
    mtEWK.histoMgr.setHistoDrawStyleAll("P")
    mtEWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))  
    hmtEWK = mtEWK.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MTBaselineTauIdJetPhi")
    

            
 ####################################   
 
    hmtSum = hmt4050.Clone("mtSum")
    hmtSum.SetName("mtSum")
    hmtSum.SetTitle("Inverted tau ID")
    hmtSum.Add(hmt5060)
    hmtSum.Add(hmt6070)
    hmtSum.Add(hmt7080)
    hmtSum.Add(hmt80100)
    hmtSum.Add(hmt100120)
    if lastPtBin150:
        hmtSum.Add(hmt120150)
        hmtSum.Add(hmt150)
    if lastPtBin120:
        hmtSum.Add(hmt120)        
    print "Integral with bins  = ",hmtSum.Integral()
    print "Integral2 with bins  = ",hmtSum2.Integral()
    print "Integral inclusive  = ",hmt.Integral()    


 ################## Control Plots for Lands
 ## for deltaPhi < 160 for mt shape
            

    canvas32 = ROOT.TCanvas("canvas32","",500,500)
    
    if (numberOfBjets):
        canvas32.SetLogy()
        frame32 = histograms._drawFrame(canvas31, xmin=0, xmax=6, ymin=1, ymax=1e3)
        frame32.Draw()
            
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
    hmtBaseline_QCD.Draw("same")

            

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
    
    hmtSum.GetYaxis().SetTitleOffset(1.5)
    hmtSum.GetXaxis().SetTitle("m_{T}(#tau jet, MET) (GeV/c^{2})")
    hmtSum.GetYaxis().SetTitle("Events / 10 GeV/c^{2}")
    canvas32.Print("transverseMass.png")
    canvas32.Print("transverseMass.C")


################ MET

    mmt4050 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets4050")])
    mmt5060 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets5060")])
    mmt6070 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets6070")])
    mmt7080 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets7080")])
    mmt80100 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets80100")])
    mmt100120 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets100120")])
    if lastPtBin150: 
        mmt120150 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets120150")])
        mmt150 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets150")])
    if lastPtBin120: 
        mmt120 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets120")])
    mmt = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets")])
        
    mmtBaseline = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_BaseLineTauIdJets")])
    mmtEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MET_BaseLineTauIdJets")])        
   


    mmt4050._setLegendStyles()
    mmt4050._setLegendLabels()
    mmt4050.histoMgr.setHistoDrawStyleAll("P")    
    mmt4050.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
    hmmt4050 = mmt4050.histoMgr.getHisto("Data").getRootHisto().Clone()
    hmmt4050.Scale(norm_4050) 

    
    mmt5060._setLegendStyles()
    mmt5060._setLegendLabels()
    mmt5060.histoMgr.setHistoDrawStyleAll("P")
    mmt5060.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
    hmmt5060 = mmt5060.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJetPhi5060")
    hmmt5060.Scale(norm_5060) 


    mmt6070._setLegendStyles()
    mmt6070._setLegendLabels()
    mmt6070.histoMgr.setHistoDrawStyleAll("P")

    mmt6070.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))    
    hmmt6070 = mmt6070.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJetPhi6070")
    hmmt6070.Scale(norm_6070) 

    
    mmt7080._setLegendStyles()
    mmt7080._setLegendLabels()
    mmt7080.histoMgr.setHistoDrawStyleAll("P")
    mmt7080.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20)) 
    hmmt7080 = mmt7080.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJetPhi7080")
    hmmt7080.Scale(norm_7080) 

    
    mmt80100._setLegendStyles()
    mmt80100._setLegendLabels()
    mmt80100.histoMgr.setHistoDrawStyleAll("P")
    mmt80100.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20)) 
    hmmt80100 = mmt80100.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJetPhi80100")
    hmmt80100.Scale(norm_80100) 

    
    mmt100120._setLegendStyles()
    mmt100120._setLegendLabels()
    mmt100120.histoMgr.setHistoDrawStyleAll("P")
    mmt100120.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))     
    hmmt100120 = mmt100120.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJetPhi100120")   
    hmmt100120.Scale(norm_100120) 


    if lastPtBin150:    
        mmt120150._setLegendStyles()
        mmt120150._setLegendLabels()
        mmt120150.histoMgr.setHistoDrawStyleAll("P")
        mmt120150.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))      
        hmmt120150 = mmt120150.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJetPhi120150")
        hmmt120150.Scale(norm_120150) 
        
        
        mmt150._setLegendStyles()
        mmt150._setLegendLabels()
        mmt150.histoMgr.setHistoDrawStyleAll("P")
        mmt150.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))  
        hmmt150 = mmt150.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJetPhi150")
        hmmt150.Scale(norm_150)
        
    if lastPtBin120:
        mmt120._setLegendStyles()
        mmt120._setLegendLabels()
        mmt120.histoMgr.setHistoDrawStyleAll("P")

        mmt120.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))  
        hmmt120 = mmt120.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJetPhi120")
        hmmt120.Scale(norm_120)



    mmtBaseline._setLegendStyles()
    mmtBaseline._setLegendLabels()
    mmtBaseline.histoMgr.setHistoDrawStyleAll("P")
    mmtBaseline.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))  
    hmmtBaseline = mmtBaseline.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTBaselineTauIdJetPhi")
    
    mmtEWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mmtEWK._setLegendStyles()
    mmtEWK._setLegendLabels()
    mmtEWK.histoMgr.setHistoDrawStyleAll("P")
    mmtEWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))  
    hmmtEWK = mmtEWK.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MTBaselineTauIdJetPhi")
    

        
    met = hmmt4050.Clone("mmtSum")
    met.SetName("MET")
    met.SetTitle("Inverted tau ID")
    met.Add(hmmt5060)
    met.Add(hmmt6070)
    met.Add(hmmt7080)
    met.Add(hmmt80100)
    met.Add(hmmt100120)
    if lastPtBin150:
        met.Add(hmmt120150)
        met.Add(hmmt150)
    if lastPtBin120:
        met.Add(hmmt120)        
    print "met Integral  = ",met.Integral()



       
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

    
################ deltaPhi
    fmt4050 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/deltaPhiInverted4050")])
    fmt5060 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/deltaPhiInverted5060")])
    fmt6070 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/deltaPhiInverted6070")])
    fmt7080 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/deltaPhiInverted7080")])
    fmt80100 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/deltaPhiInverted80100")])
    fmt100120 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/deltaPhiInverted100120")])
    if lastPtBin150:
        fmt120150 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/deltaPhiInverted120150")])
        fmt150 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/deltaPhiInverted150")])
    if lastPtBin120:
        fmt120 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/deltaPhiInverted120")])
    fmtBaseline = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/deltaPhiBaseline")])
    fmtEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/deltaPhiBaseline")])        

    fmt4050._setLegendStyles()
    fmt4050._setLegendLabels()
    fmt4050.histoMgr.setHistoDrawStyleAll("P")    
    fmt4050.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
    hfmt4050 = fmt4050.histoMgr.getHisto("Data").getRootHisto().Clone()
    hfmt4050.Scale(norm_4050) 

    
    fmt5060._setLegendStyles()
    fmt5060._setLegendLabels()
    fmt5060.histoMgr.setHistoDrawStyleAll("P")
    fmt5060.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
    hfmt5060 = fmt5060.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJetPhi5060")
    hfmt5060.Scale(norm_5060) 


    fmt6070._setLegendStyles()
    fmt6070._setLegendLabels()
    fmt6070.histoMgr.setHistoDrawStyleAll("P")

    fmt6070.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))    
    hfmt6070 = fmt6070.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJetPhi6070")
    hfmt6070.Scale(norm_6070) 

    
    fmt7080._setLegendStyles()
    fmt7080._setLegendLabels()
    fmt7080.histoMgr.setHistoDrawStyleAll("P")
    fmt7080.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20)) 
    hfmt7080 = fmt7080.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJetPhi7080")
    hfmt7080.Scale(norm_7080) 

    
    fmt80100._setLegendStyles()
    fmt80100._setLegendLabels()
    fmt80100.histoMgr.setHistoDrawStyleAll("P")

    fmt80100.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20)) 
    hfmt80100 = fmt80100.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJetPhi80100")
    hfmt80100.Scale(norm_80100) 

    
    fmt100120._setLegendStyles()
    fmt100120._setLegendLabels()
    fmt100120.histoMgr.setHistoDrawStyleAll("P")

    fmt100120.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))     
    hfmt100120 = fmt100120.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJetPhi100120")   
    hfmt100120.Scale(norm_100120) 


    if lastPtBin150:    
        fmt120150._setLegendStyles()
        fmt120150._setLegendLabels()
        fmt120150.histoMgr.setHistoDrawStyleAll("P")
        fmt120150.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))      
        hfmt120150 = fmt120150.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJetPhi120150")
        hfmt120150.Scale(norm_120150) 
        
        
        fmt150._setLegendStyles()
        fmt150._setLegendLabels()
        fmt150.histoMgr.setHistoDrawStyleAll("P")
        fmt150.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))  
        hfmt150 = fmt150.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJetPhi150")
        hfmt150.Scale(norm_150)
        
    if lastPtBin120:
        fmt120._setLegendStyles()
        fmt120._setLegendLabels()
        fmt120.histoMgr.setHistoDrawStyleAll("P")

        fmt120.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))  
        hfmt120 = fmt120.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJetPhi120")
        hfmt120.Scale(norm_120)
        
    fmtBaseline._setLegendStyles()
    fmtBaseline._setLegendLabels()
    fmtBaseline.histoMgr.setHistoDrawStyleAll("P")
    fmtBaseline.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))  
    hfmtBaseline = fmtBaseline.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTBaselineTauIdJetPhi")
    
    fmtEWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    fmtEWK._setLegendStyles()
    fmtEWK._setLegendLabels()
    fmtEWK.histoMgr.setHistoDrawStyleAll("P")
    fmtEWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))  
    hfmtEWK = fmtEWK.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MTBaselineTauIdJetPhi")
    
        
    DeltaPhi = hfmt4050.Clone("fmtSum")
    DeltaPhi.SetName("DeltaPhi")
    DeltaPhi.SetTitle("Inverted tau ID")
    DeltaPhi.Add(hfmt5060)
    DeltaPhi.Add(hfmt6070)
    DeltaPhi.Add(hfmt7080)
    DeltaPhi.Add(hfmt80100)
    DeltaPhi.Add(hfmt100120)
    if lastPtBin150:
        DeltaPhi.Add(hfmt120150)
        DeltaPhi.Add(hfmt150)
    if lastPtBin120:
        DeltaPhi.Add(hfmt120)        
    print "DeltaPhi Integral  = ",DeltaPhi.Integral()



       
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
    hmt4050 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/HiggsMass4050")])
    hmt5060 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/HiggsMass5060")])
    hmt6070 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/HiggsMass6070")])
    hmt7080 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/HiggMass7080")])
    hmt80100 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/HiggsMass80100")])
    hmt100120 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/HiggsMass100120")])
    if lastPtBin150:
        hmt120150 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/HiggsMass120150")])
        hmt150 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/HiggsMass150")])
    if lastPtBin120: 
        hmt120 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/HiggsMass120")])


    hmt4050._setLegendStyles()
    hmt4050._setLegendLabels()
    hmt4050.histoMgr.setHistoDrawStyleAll("P")    
    hmt4050.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
    hhmt4050 = hmt4050.histoMgr.getHisto("Data").getRootHisto().Clone()
    hhmt4050.Scale(norm_4050) 

    
    hmt5060._setLegendStyles()
    hmt5060._setLegendLabels()
    hmt5060.histoMgr.setHistoDrawStyleAll("P")
    hmt5060.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
    hhmt5060 = hmt5060.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJetPhi5060")
    hhmt5060.Scale(norm_5060) 


    hmt6070._setLegendStyles()
    hmt6070._setLegendLabels()
    hmt6070.histoMgr.setHistoDrawStyleAll("P")

    hmt6070.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))    
    hhmt6070 = hmt6070.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJetPhi6070")
    hhmt6070.Scale(norm_6070) 

    
    hmt7080._setLegendStyles()
    hmt7080._setLegendLabels()
    hmt7080.histoMgr.setHistoDrawStyleAll("P")
    hmt7080.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20)) 
    hhmt7080 = hmt7080.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJetPhi7080")
    hhmt7080.Scale(norm_7080) 

    
    hmt80100._setLegendStyles()
    hmt80100._setLegendLabels()
    hmt80100.histoMgr.setHistoDrawStyleAll("P")

    hmt80100.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20)) 
    hhmt80100 = hmt80100.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJetPhi80100")
    hhmt80100.Scale(norm_80100) 

    
    hmt100120._setLegendStyles()
    hmt100120._setLegendLabels()
    fmt100120.histoMgr.setHistoDrawStyleAll("P")

    hmt100120.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))     
    hhmt100120 = hmt100120.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJetPhi100120")   
    hhmt100120.Scale(norm_100120) 


    if lastPtBin150:    
        hmt120150._setLegendStyles()
        hmt120150._setLegendLabels()
        hmt120150.histoMgr.setHistoDrawStyleAll("P")
        hmt120150.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))      
        hhmt120150 = hmt120150.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJetPhi120150")
        hhmt120150.Scale(norm_120150) 
        
        
        hmt150._setLegendStyles()
        hmt150._setLegendLabels()
        hmt150.histoMgr.setHistoDrawStyleAll("P")
        hmt150.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))  
        hhmt150 = hmt150.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJetPhi150")
        hhmt150.Scale(norm_150)
        
    if lastPtBin120:
        hmt120._setLegendStyles()
        hmt120._setLegendLabels()
        hmt120.histoMgr.setHistoDrawStyleAll("P")

        hmt120.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))  
        hhmt120 = hmt120.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJetPhi120")
        hhmt120.Scale(norm_120)
        
    FullMass = hhmt4050.Clone("hmtSum")
    FullMass.SetName("FullMass")
    FullMass.SetTitle("Inverted tau ID")
    FullMass.Add(hhmt5060)
    FullMass.Add(hhmt6070)
    FullMass.Add(hhmt7080)
    FullMass.Add(hhmt80100)
    FullMass.Add(hhmt100120)
    if lastPtBin150:
        FullMass.Add(hhmt120150)
        FullMass.Add(hhmt150)
    if lastPtBin120:
        FullMass.Add(hhmt120)        
    print "HiggsMass  Integral  = ",FullMass.Integral()

       
    canvas31 = ROOT.TCanvas("canvas31","",500,500)
    FullMass.SetMarkerColor(4)
    FullMass.SetMarkerSize(1)
    FullMass.SetMarkerStyle(20)
    FullMass.SetFillColor(4)
    
    FullMass.Draw("EP")
            
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       5.05 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    
    FullMass.GetXaxis().SetTitle("m_{Higgs} (GeV/c^{2})")
    FullMass.GetYaxis().SetTitle("Events / 20 GeV/c^{2} ")
    canvas31.Print("FullMass.png")
    canvas31.Print("FullMass.C")


################## N bjets
    
    bhmt4050 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/NBInvertedTauIdJet4050")])
    bhmt5060 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/NBInvertedTauIdJet5060")])
    bhmt6070 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/NBInvertedTauIdJet6070")])
    bhmt7080 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/NBInvertedTauIdJet7080")])
    bhmt80100 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/NBInvertedTauIdJet80100")])
    bhmt100120 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/NBInvertedTauIdJet100120")])
    if lastPtBin150: 
        bhmt120150 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/NBInvertedTauIdJet120150")])
        bhmt150 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/NBInvertedTauIdJet150")])
    if lastPtBin120: 
        bhmt120 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/NBInvertedTauIdJet120")])
    bhmt = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/NBInvertedTauIdJet")])
    bhmtBaseline = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/NBBaselineTauIdJet")])
    bhmtEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/NBBaselineTauIdJet")])
 
       
    bhmt4050._setLegendStyles()
    bhmt4050._setLegendLabels()
    bhmt4050.histoMgr.setHistoDrawStyleAll("P")    
    bhmt4050.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))
    hbhmt4050 = bhmt4050.histoMgr.getHisto("Data").getRootHisto().Clone()
    hbhmt4050.Scale(norm_4050) 

    
    bhmt5060._setLegendStyles()
    bhmt5060._setLegendLabels()
    bhmt5060.histoMgr.setHistoDrawStyleAll("P")
    bhmt5060.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))
    hbhmt5060 = bhmt5060.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJetPhi5060")
    hbhmt5060.Scale(norm_5060) 


    bhmt6070._setLegendStyles()
    bhmt6070._setLegendLabels()
    bhmt6070.histoMgr.setHistoDrawStyleAll("P")

    bhmt6070.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))    
    hbhmt6070 = bhmt6070.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJetPhi6070")
    hbhmt6070.Scale(norm_6070) 

    
    bhmt7080._setLegendStyles()
    bhmt7080._setLegendLabels()
    bhmt7080.histoMgr.setHistoDrawStyleAll("P")
    bhmt7080.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1)) 
    hbhmt7080 = bhmt7080.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJetPhi7080")
    hbhmt7080.Scale(norm_7080) 

    
    bhmt80100._setLegendStyles()
    bhmt80100._setLegendLabels()
    bhmt80100.histoMgr.setHistoDrawStyleAll("P")

    bhmt80100.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1)) 
    hbhmt80100 = bhmt80100.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJetPhi80100")
    hbhmt80100.Scale(norm_80100) 

    
    bhmt100120._setLegendStyles()
    bhmt100120._setLegendLabels()
    bhmt100120.histoMgr.setHistoDrawStyleAll("P")

    bhmt100120.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))     
    hbhmt100120 = bhmt100120.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJetPhi100120")   
    hbhmt100120.Scale(norm_100120) 


    if lastPtBin150:    
        bhmt120150._setLegendStyles()
        bhmt120150._setLegendLabels()
        bhmt120150.histoMgr.setHistoDrawStyleAll("P")
        bhmt120150.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))      
        hbhmt120150 = bhmt120150.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJetPhi120150")
        hbhmt120150.Scale(norm_120150) 
        
        
        bhmt150._setLegendStyles()
        bhmt150._setLegendLabels()
        bhmt150.histoMgr.setHistoDrawStyleAll("P")
        bhmt150.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))  
        hbhmt150 = bhmt150.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJetPhi150")
        hbhmt150.Scale(norm_150)
        
    if lastPtBin120:
        bhmt120._setLegendStyles()
        bhmt120._setLegendLabels()
        bhmt120.histoMgr.setHistoDrawStyleAll("P")

        bhmt120.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))  
        hbhmt120 = bhmt120.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJetPhi120")
        hbhmt120.Scale(norm_120)


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
    

        
    NBjets = hbhmt4050.Clone("bhmtSum")
    NBjets.SetName("NBjets")
    NBjets.SetTitle("Inverted tau ID")
    NBjets.Add(hbhmt5060)
    NBjets.Add(hbhmt6070)
    NBjets.Add(hbhmt7080)
    NBjets.Add(hbhmt80100)
    NBjets.Add(hbhmt100120)
    if lastPtBin150:
        NBjets.Add(hbhmt120150)
        NBjets.Add(hbhmt150)
    if lastPtBin120:
        NBjets.Add(hbhmt120)        
    print "NBjets Integral  = ",NBjets.Integral()

       
    canvas33 = ROOT.TCanvas("canvas33","",500,500)
    canvas33.SetLogy()
    frame33 = histograms._drawFrame(canvas33, xmin=0, xmax=6, ymin=1, ymax=1e3)
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

### selection flow
    selectionFlow = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/SignalSelectionFlow")])
    selectionFlow._setLegendStyles()
    selectionFlow._setLegendLabels()
    selectionFlow.histoMgr.setHistoDrawStyleAll("P")    
    selectionFlow.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))
    hselectionFlow = selectionFlow.histoMgr.getHisto("Data").getRootHisto().Clone()
#    hselectionFlow.Scale(norm_inc) 
    
##########################################################################            
    fOUT = ROOT.TFile.Open("histogramsForLands.root","RECREATE")
    fOUT.cd()
    hmtSum.Write()
    DeltaPhi.Write()
    FullMass.Write()
    NBjets.Write()
    met.Write()
    hselectionFlow.Write()
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

def tauPt(h, name, **kwargs):
    xlabel = "p_{T}^{#tau jet} (GeV/c)"
    drawPlot(h, name, xlabel, **kwargs)

def tauEta(h, name, **kwargs):
    xlabel = "#eta^{#tau jet}"
    ylabel = "Events / %.1f"
    drawPlot(h, name, xlabel, ylabel=ylabel, **kwargs)
    
def tauPhi(h, name, **kwargs):
    xlabel = "#phi^{#tau jet}"
    ylabel = "Events / %.1f"
    drawPlot(h, name, xlabel, ylabel=ylabel, **kwargs)

# Functions below are for plot-specific formattings. They all take the
# plot object as an argument, then apply some formatting to it, draw
# it and finally save it to files.

def vertexCount(h, prefix="", postfix="", ratio=True):
        xlabel = "Number of good vertices"
        ylabel = "Number of events"

        if h.normalizeToOne:
            ylabel = "A.u."
        

        h.stackMCHistograms()

        stack = h.histoMgr.getHisto("StackedMC")
        #hsum = stack.getSumRootHisto()
        #total = hsum.Integral(0, hsum.GetNbinsX()+1)
        #for rh in stack.getAllRootHistos():
        #    dataset._normalizeToFactor(rh, 1/total)
        #dataset._normalizeToOne(h.histoMgr.getHisto("Data").getRootHisto())

        h.addMCUncertainty()

        opts = {}
        opts_log = {"ymin": 1e-10, "ymaxfactor": 10}
        opts_log.update(opts)

        opts2 = {"ymin": 0.5, "ymax": 3}
        opts2_log = {"ymin": 5e-2, "ymax": 5e2}
        
        h.createFrame(prefix+"vertices"+postfix, opts=opts, createRatio=ratio, opts2=opts2)
        h.frame.GetXaxis().SetTitle(xlabel)
        h.frame.GetYaxis().SetTitle(ylabel)
        h.setLegend(histograms.createLegend())
        h.draw()
        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        #    histograms.addLuminosityText(x=None, y=None, lumi=191.)
        h.histoMgr.addLuminosityText()
        if h.normalizeToOne:
            histograms.addText(0.35, 0.9, "Normalized to unit area", 17)
        h.save()

        h.createFrame(prefix+"vertices"+postfix+"_log", opts=opts_log, createRatio=ratio, opts2=opts2_log)
        h.frame.GetXaxis().SetTitle(xlabel)
        h.frame.GetYaxis().SetTitle(ylabel)
        h.getPad1().SetLogy(True)
        h.getPad2().SetLogy(True)
        h.setLegend(histograms.createLegend())
        h.draw()
        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        #    histograms.addLuminosityText(x=None, y=None, lumi=191.)
        h.histoMgr.addLuminosityText()
        if h.normalizeToOne:
            histograms.addText(0.35, 0.9, "Normalized to unit area", 17)
        h.save()

def rtauGen(h, name, rebin=5, ratio=False):
    #h.setDefaultStyles()
    h.histoMgr.forEachHisto(styles.generator())

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "R_{#tau}"
    if "Mass" in name:
        xlabel = "m (GeV/c^{2})"
    elif "Pt" in name:
        xlabel = "p_{T}(GeV/c)"
    elif "vertices" in name:
        xlabel = "N_{vertices}"
    ylabel = "Events / %.2f" % h.binWidth()

    if "gen" in name:
        kwargs = {"ymin": 0.1, "xmax": 1.1}        
    elif "Pt" in name:
        kwargs = {"ymin": 0.1, "xmax": 400}
    elif "Mass" in name:
        kwargs = {"ymin": 0.1, "xmax": 300}
        
    kwargs = {"ymin": 0.1, "xmax": 300}
#    kwargs["opts"] = {"ymin": 0, "xmax": 14, "ymaxfactor": 1.1}}
    if ratio:
        kwargs["opts2"] = {"ymin": 0.5, "ymax": 1.5}
        kwargs["createRatio"] = True
    name = name+"_log"

    h.createFrame(name, **kwargs)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend(0.2, 0.75, 0.4, 0.9))
    common(h, xlabel, ylabel, addLuminosityText=False)

def selectionFlow(h, name, rebin=1, ratio=False):

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "Cut"    # Tau
    tauPt(createPlot("SelectedTau/SelectedTau_pT_AfterTauID"), "SelectedTau_pT_AfterTauID", rebin=5, ratio=False, opts={"xmax": 300, "ymaxfactor": 2}, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    tauEta(createPlot("SelectedTau/SelectedTau_eta_AfterTauID"),"SelectedTau_eta_AfterTauID", rebin=5, ratio=False, opts={"ymin": 1, "ymaxfactor": 50, "xmin": -2.5, "xmax": 2.5}, moveLegend={"dy":0.01, "dh":-0.06}, textFunction=lambda: addMassBRText(x=0.3, y=0.85))
 
    ylabel = "Events"

    h.stackMCHistograms()
    h.addMCUncertainty()
    scaleMCfromWmunu(h)
    
    opts = {"xmax": 7, "ymin": 0.01, "ymaxfactor": 2}
    opts2 = {"ymin": 0.5, "ymax": 1.5}

    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend(0.7, 0.6, 0.9, 0.9))
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    #h.addLuminosityText()
    h.save()    

def tauCandPt(h, step="", rebin=2):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    ylabel = "Events /%.0f GeV/c" % h.binWidth()   
    xlabel = "p_{T}^{#tau candidate} (GeV/c)"
    opts = {"ymaxfactor": 2}
    
    h.stackMCHistograms()
    h.addMCUncertainty()
    scaleMCfromWmunu(h)
    
    if h.normalizeToOne:
        ylabel = "A.u."
        opts["yminfactor"] = 1e-5
    else:
        opts["ymin"] = 0.001
           

    name = "tauCandidatePt_%s_log" % step
    h.createFrameFraction(name, opts=opts)
    #h.createFrame(name, opts=opts)
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.setLegend(histograms.createLegend())
    h.setLegend(histograms.createLegend(0.7, 0.6, 0.9, 0.9))
    ROOT.gPad.SetLogy(True)
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    #h.addLuminosityText()
    h.save()
    
def tauCandEta(h, step="", rebin=5):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "#eta^{#tau candidate}"
    ylabel = "Events / %.1f" % h.binWidth()
    opts = {"ymaxfactor": 2}
    
    h.stackMCHistograms()
    h.addMCUncertainty()
    scaleMCfromWmunu(h)

    
    if h.normalizeToOne:
        ylabel = "A.u."
        opts["yminfactor"] = 1e-5
    else:
        opts["ymin"] = 0.001
           
#    opts = {"xmax": 2.5,"xmin":-2.5}
#    opts["xmin"] = -2.7
#    opts["xmax"] =  2.7    
    name = "tauCandidateEta_%s_log" % step
#    h.createFrameFraction(name, opts=opts)
    h.createFrame(name, opts=opts)
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.setLegend(histograms.createLegend(0.5, 0.2, 0.7, 0.5))
    ROOT.gPad.SetLogy(True)
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    #h.addLuminosityText()
    h.save()

def tauCandPhi(h, step="", rebin=5):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "#phi^{#tau candidate}"
    ylabel = "Events / %.1f" % h.binWidth()
    opts = {"ymaxfactor": 2}
    
    h.stackMCHistograms()
    h.addMCUncertainty()
    scaleMCfromWmunu(h)

    
    if h.normalizeToOne:
        ylabel = "A.u."
        opts["yminfactor"] = 1e-5
    else:
        opts["ymin"] = 0.01
           

    name = "tauCandidatePhi_%s_log" % step
    h.createFrameFraction(name, opts=opts)
    #h.createFrame(name, opts=opts)
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.setLegend(histograms.createLegend())
    ROOT.gPad.SetLogy(True)
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    #h.addLuminosityText()
    h.save()
    


def tauPt(h, name, rebin=5, ratio=False):
#    name = flipName(h.getRootHistoPath())

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "p_{T}^{#tau jet} (GeV/c)"
    ylabel = "Events / %.0f GeV/c" % h.binWidth()

    h.stackMCHistograms()
#    h.addMCUncertainty()
    scaleMCfromWmunu(h)
    
    opts = {"ymin": 0.0001, "ymaxfactor": 2}
    opts2 = {"ymin": 0.5, "ymax": 1.5}
#    name = "selectedTauPt"
#    name = name+"_log"
    #h.createFrameFraction(name, opts=opts)
#    h.createFrame(name, opts=opts)
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend(0.7, 0.6, 0.9, 0.9))
    common(h, xlabel, ylabel)
    
def tauEta(h, name, rebin=5, ratio=False):
#    name = flipName(h.getRootHistoPath())

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "#eta^{#tau jet}"
    ylabel = "Events"

    h.stackMCHistograms()
#    h.addMCUncertainty()
    scaleMCfromWmunu(h)

    
    opts = {"ymin": 0.01, "ymaxfactor": 2}
    opts2 = {"ymin": 0.5, "ymax": 1.5}
#    name = "selectedTauEta"
#    name = name+"_log"
    #h.createFrameFraction(name, opts=opts)
#    h.createFrame(name, opts=opts)
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend(0.7, 0.6, 0.9, 0.9))
    common(h, xlabel, ylabel)
    
def tauPhi(h, name, rebin=10, ratio=False):
    name = flipName(h.getRootHistoPath())

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "#phi^{#tau jet}"
    ylabel = "Events"

    h.stackMCHistograms()
#    h.addMCUncertainty()
    scaleMCfromWmunu(h)
    
    opts = {"ymin": 0.01, "ymaxfactor": 2}
    opts2 = {"ymin": 0.5, "ymax": 1.5}
#    name = "selectedTauPhi"
#    name = name+"_log"
    #h.createFrameFraction(name, opts=opts)
#    h.createFrame(name, opts=opts)
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend(0.7, 0.3, 0.9, 0.6))
    common(h, xlabel, ylabel)
    
def leadingTrack(h, rebin=5, ratio=True):
    name = flipName(h.getRootHistoPath())

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "p_{T}^{leading track} (GeV/c)"
    ylabel = "Events / %.0f GeV/c" % h.binWidth()

    h.stackMCHistograms()
    h.addMCUncertainty()
    scaleMCfromWmunu(h)
    
    opts = {"ymin": 0.001,"xmin": 10.0, "ymaxfactor": 5}
    name = "leadingTrackPt"
#    name = name+"_log"
    #h.createFrameFraction(name, opts=opts)
    h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)

def rtau(h, name, rebin=15, ratio=False):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "R_{#tau}"
    ylabel = "Events / %.2f" % h.binWidth()

    h.stackMCHistograms()
    h.addMCUncertainty()
    scaleMCfromWmunu(h)
    
    opts = {"ymin": 0.001,"xmax": 1.1, "ymaxfactor": 5}
    opts2 = {"ymin": 0.5, "ymax": 1.5}
    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
#    h.createFrame(name, opts=opts)
    #h.createFrameFraction(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend(0.2, 0.68, 0.4, 0.93))
    common(h, xlabel, ylabel)


def met(h, rebin=20, ratio=False):
    name = flipName(h.getRootHistoPath())

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "MET (GeV)"
#    if "embedding" in name:
#        xlabel = "Embedded "+xlabel
#    elif "original" in name:
#        xlabel = "Original "+xlabel
    
    ylabel = "Events / %.0f GeV" % h.binWidth()

    scaleMCfromWmunu(h)
    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.001, "ymaxfactor": 2}
    opts2 = {"ymin": 0.5, "ymax": 1.5}

    name = "MET"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)


    
def met2(h, name, rebin=30, ratio=True):
#    name = h.getRootHistoPath()
#    name = "met"

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
#    xlabel = "MET (GeV)"
#    if "embedding" in name:
#        xlabel = "Embedded "+xlabel
#    elif "original" in name:
#        xlabel = "Original "+xlabel
    ylabel = "Events / %.0f GeV" % h.binWidth()
    xlabel = "E_{T}^{miss} (GeV)"
    
    scaleMCfromWmunu(h)
    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.01, "ymaxfactor": 2}
    opts2 = {"ymin": 0.0, "ymax": 2.5}

    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend(0.65, 0.55, 0.9, 0.9))
    common(h, xlabel, ylabel)



def deltaPhi(h, rebin=40, ratio=False):
    name = flipName(h.getRootHistoPath())

    particle = "#tau jet"
    if "Original" in name:
        particle = "#mu"

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "#Delta#phi(%s, MET) (rad)" % particle
    ylabel = "Events / %.2f rad" % h.binWidth()
    
    scaleMCfromWmunu(h)    
    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.001, "ymaxfactor": 2}
    opts2 = {"ymin": 0.5, "ymax": 1.5}
    
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
    #h.createFrameFraction(name)
    h.createFrame(name)
#    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend(0.2, 0.6, 0.4, 0.9))
    common(h, xlabel, ylabel)


#def deltaPhi2(h, name, **kwargs):
#    xlabel = "#Delta#phi(#tau jet, E_{T}^{miss})^{#circ}"
#    ylabel = "Events / %.0f^{#circ}"
#drawPlot(h, name, xlabel, ylabel=ylabel, **kwargs)

    
def deltaPhi2(h, name, rebin=2):
#    name = flipName(h.getRootHistoPath())
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))

#    particle = "jet"
#    if "taus" in name:
#        particle = "jet,#tau"
    xlabel = "#Delta#phi(#tau jet, MET)^{0}"
    ylabel = "Events / %.2f deg" % h.binWidth()
    
    scaleMCfromWmunu(h)      
    h.stackMCHistograms()
    h.addMCUncertainty()
    
#    name = "deltaPhiMetJet"
    #h.createFrameFraction(name)
#    h.createFrame(name)
    opts = {"ymin": 0.001, "ymaxfactor": 2}
    h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend(0.2, 0.3, 0.4, 0.5))
    common(h, xlabel, ylabel)


        
    
def transverseMass(h, rebin=20):
    name = flipName(h.getRootHistoPath())

    particle = ""
    if "Original" in name:
        particle = "#mu"
        name = name.replace("TransverseMass", "Mt")
    else:
        particle = "#tau jet"
        name = name.replace("TransverseMass", "Mt")

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "m_{T}(%s, MET) (GeV/c^{2})" % particle
    ylabel = "Events / %.2f GeV/c^{2}" % h.binWidth()
    
    scaleMCfromWmunu(h)     
    h.stackMCSignalHistograms()
    h.stackMCHistograms(stackSignal=False)#stackSignal=True)
    h.addMCUncertainty()

    opts = {"xmax": 200}

    #h.createFrameFraction(name, opts=opts)
    h.createFrame(name, opts=opts)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)
    
def transverseMass2(h,name, rebin=10, ratio=False):
#    name = flipName(h.getRootHistoPath())
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "m_{T}(#tau jet, MET) (GeV/c^{2})" 
    ylabel = "Events / %.0f GeV/c^{2}" % h.binWidth()
    
    scaleMCfromWmunu(h)    
    #h.stackMCSignalHistograms()
    h.stackMCHistograms(stackSignal=False)#stackSignal=True)
    h.addMCUncertainty()
   
#    name = name+"_log"
    opts = {"ymin": 0.001, "ymaxfactor": 2.0,"xmax": 350 }
#    opts = {"xmax": 200 }
    opts2 = {"ymin": 0, "ymax": 3}
    h.createFrame(name, opts=opts, createRatio=ratio, opts2=opts2)
    h.getPad().SetLogy(True)
    if "Higgs" in name:
        h.getPad().SetLogy(False) 
    h.setLegend(histograms.createLegend(0.7, 0.68, 0.9, 0.93))
    common(h, xlabel, ylabel)
       
def jetPt(h, name, rebin=5, ratio=False):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    particle = "jet"
    if "bjet" in name:
        particle = "b jet"
    if "electron" in name:
        particle = "electron"
    if "muon" in name:
        particle = "muon"
#        name = name.replace("jetPt", "bjetPt")

    xlabel = "p_{T}^{%s} (GeV/c)" % particle
#    xlabel = "p_{T}^{muon} (GeV/c)" 
    ylabel = "Events /%.0f GeV/c" % h.binWidth()
    
    scaleMCfromWmunu(h)  
    h.stackMCSignalHistograms()
    h.stackMCHistograms(stackSignal=False)
    h.addMCUncertainty()

    opts = {"ymin": 0.001,"xmax": 400.0, "ymaxfactor": 2}
    opts2 = {"ymin": 0.05, "ymax": 1.5}
    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
#    h.createFrame(name, opts=opts)
    #h.createFrameFraction(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend(0.7, 0.65, 0.9, 0.9))
    common(h, xlabel, ylabel)

    
def jetEta(h, name, rebin=5, ratio=False):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    particle = "jet"
    if "bjet" in name:
        particle = "b jet"
    if "electron" in name:
        particle = "electron"
    if "muon" in name:
        particle = "muon"
    xlabel = "#eta^{%s}" % particle
#    xlabel = "#eta^{muon}"
    ylabel = "Events / %.2f" % h.binWidth()
    
    scaleMCfromWmunu(h)  
    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.01,"xmin": -3.5,"xmax": 3.5, "ymaxfactor": 10}
    opts2 = {"ymin": 0.05, "ymax": 1.5}
    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend(0.7, 0.7, 0.9, 0.95))
#    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)

def jetPhi(h, name, rebin=5, ratio=False):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    particle = "jet"
    if "bjet" in name:
        particle = "bjet"
    xlabel = "#phi^{%s}" % particle
    ylabel = "Events / %.2f" % h.binWidth()
    
    scaleMCfromWmunu(h)  
    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.01, "ymaxfactor": 2.0}
    opts2 = {"ymin": 0.01, "ymax": 1.5}
    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend(0.7, 0.2, 0.9, 0.5))
    common(h, xlabel, ylabel)
    
def jetEMFraction(h, name, rebin=5, ratio=False):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))

    xlabel = "EMfraction in jets" 
    ylabel = "Events / %.2f" % h.binWidth()
    
    scaleMCfromWmunu(h)  
    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.01, "ymaxfactor": 2.0}
    opts2 = {"ymin": 0.01, "ymax": 1.5}
    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend(0.7, 0.6, 0.9, 0.9))
    common(h, xlabel, ylabel)

def numberOfJets(h, name, rebin=1, ratio=False):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    particle = "jet"
    if "Btagged" in name:
        particle = "b jet"
    xlabel = "Number of %ss" % particle
    ylabel = "Events / %.2f" % h.binWidth()
    
    scaleMCfromWmunu(h)
    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.01,"xmax": 7.0, "ymaxfactor": 2.0}
    opts2 = {"ymin": 0.05, "ymax": 1.5}
#    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)

def etSumRatio(h, name, rebin=1, ratio=False):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
#    particle = "jet"
#    if "bjet" in name:
#        particle = "bjet"
#        name = name.replace("jetPt", "bjetPt")

    xlabel = "#Sigma E_{T}^{Forward} / #Sigma E_{T}^{Central}"
    ylabel = "Events /%.0f GeV/c" % h.binWidth()
    
    scaleMCfromWmunu(h)  
    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.0001, "ymaxfactor": 5}
    opts2 = {"ymin": 0.5, "ymax": 1.5}
    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
#    h.createFrame(name, opts=opts)
    #h.createFrameFraction(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)

def tauJetMass(h, name, rebin=1, ratio=False):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
#    particle = "jet"
#    if "bjet" in name:
#        particle = "bjet"
#        name = name.replace("jetPt", "bjetPt")

    xlabel = "#Sigma E_{T}^{Forward} / #Sigma E_{T}^{Central}"
    ylabel = "Events /%.0f GeV/c" % h.binWidth()
    
    scaleMCfromWmunu(h)  
    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.001, "ymaxfactor": 1.5}
    opts2 = {"ymin": 0.01, "ymax": 1.5}
    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
#    h.createFrame(name)
    #h.createFrameFraction(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)



def topMass(h, name, rebin=20, ratio=False):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
#    particle = "jet"
#    if "bjet" in name:
#        particle = "bjet"
#        name = name.replace("jetPt", "bjetPt")

    xlabel = "m_{top} (GeV/c^{2})"
    ylabel = "Events /%.0f GeV/c" % h.binWidth()
    
    scaleMCfromWmunu(h)  
    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.0001, "ymaxfactor": 1.1}
    opts2 = {"ymin": 0.01, "ymax": 1.5}
    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
#    h.createFrame(name)
#    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)

def ptTop(h, name, rebin=10, ratio=False):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
#    particle = "jet"
#    if "bjet" in name:
#        particle = "bjet"
#        name = name.replace("jetPt", "bjetPt")

    xlabel = "p_{T}^{top} (GeV/c)"
    ylabel = "Events /%.0f GeV/c" % h.binWidth()
    
    scaleMCfromWmunu(h)  
    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.0001, "xmax": 500, "ymaxfactor": 1.1}
    opts2 = {"ymin": 0.01, "ymax": 1.5}
    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
#    h.createFrame(name)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)   

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
