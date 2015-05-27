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

#optMode = "OptQCDTailKillerZeroPlus"
#optMode = "OptQCDTailKillerLoosePlus"
#optMode = "OptQCDTailKillerMediumPlus"
optMode = "OptQCDTailKillerTightPlus"

#optMode = ""


#dataEra = "Run2011A"
#dataEra = "Run2011B"
dataEra = "Run2011AB"

print "dataEra"

sysError = 0.1

includeEWKscale = False
EWKscale = 0.6

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

#    print "Int.Lumi",datasets.getDataset("Data").getLuminosity()

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
    # Remove QCD
    datasets.remove(filter(lambda name: "QCD" in name, datasets.getAllDatasetNames()))

    
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
            plot = plots.MCPlot(datasets, name, normalizeToLumi=mcOnlyLumi, **kwargs)
        else:
            plot = plots.DataMCPlot(datasets, name, **kwargs)
        plot.histoMgr.removeHisto("EWK")
        return plot
 
    controlPlots(datasets)

    transverseMass2(createPlot("BaseLine/MTBaseLineTauIdAllCutsTailKiller"), "transverseMass", rebin=10, ratio=False,log=False, opts={"xmax": 400,"ymaxfactor": 1.1}, textFunction=lambda: addMassBRText(x=0.35, y=0.87))
   # transverseMass2(createPlot("Inverted/MTInvertedTauIdSoftBtaggingTK"), "transverseMassSoftBtag_Inv", rebin=10, ratio=False,log=False, opts={"xmax": 400,"ymaxfactor": 1.1}, textFunction=lambda: addMassBRText(x=0.35, y=0.87))
    transverseMass2(createPlot("BaseLine/MTBaseLineTauIdSoftBtaggingTK"), "transverseMassSoftBtag_Baseline", rebin=10, ratio=False,log=False, opts={"xmax": 400,"ymaxfactor": 1.1}, textFunction=lambda: addMassBRText(x=0.35, y=0.87))  
    drawPlot(createPlot("Inverted/MET_InvertedTauIdBvetoCollinear"), "MET_InvertedTauIdBvetoCollinear", xlabel="MET (GeV)",  rebin=5, log=True,  ylabel="Events", ratio=True, opts={ "xmax": 400}, textFunction=lambda: addMassBRText(x=0.4, y=0.87))
    drawPlot(createPlot("BaseLine/MET_BaseLineTauIdBvetoCollinear"), "MET_BaseLineTauIdBvetoCollinear", xlabel="MET (GeV)",  rebin=10, log=True,  ylabel="Events", ratio=True, opts={ "xmax": 400}, textFunction=lambda: addMassBRText(x=0.4, y=0.87))
     
    drawPlot(createPlot("BaseLine/MET_BaseLineTauIdJets"), "MET_BaseLineTauIdJets", xlabel="MET (GeV)",  rebin=10, log=True,  ylabel="Events", ratio=True, opts={ "xmax": 400}, textFunction=lambda: addMassBRText(x=0.4, y=0.87))
    drawPlot(createPlot("BaseLine/MET_BaseLineTauIdBveto"), "MET_BaseLineTauIdBveto", xlabel="MET (GeV)",  rebin=10, log=True,  ylabel="Events", ratio=True, opts={ "xmax": 400}, textFunction=lambda: addMassBRText(x=0.4, y=0.87))
    drawPlot(createPlot("Inverted/MET_InvertedTauIdBveto"), "MET_InvertedTauIdBveto", xlabel="MET (GeV)",  rebin=5, log=True,  ylabel="Events", ratio=True, opts={ "xmax": 400}, textFunction=lambda: addMassBRText(x=0.4, y=0.87))
    drawPlot(createPlot("Inverted/MET_InvertedTauIdJets"), "MET_InvertedTauIdJets", xlabel="MET (GeV)",  rebin=5, log=True,  ylabel="Events", ratio=True, opts={ "xmax": 400}, textFunction=lambda: addMassBRText(x=0.4, y=0.87))

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
    closureBveto = []
    closureBvetoTailKiller = []
    closureBtag = []
    closureBtagTailKiller = []
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
    hmtPhivetoNortt = []
    hmetBtagging = []
    hmetBveto = []
    closureAfterJets = []
    closureAfterJetsTailKiller = []
    NoBtaggingTailKiller = []
    hmtBvetoTailKiller = []
    hmtbSoft = []
    closureBvetoNoMetCutTailKiller = []
    invertedNoScale = []
    
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
        mtEvents = mt_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        invertedNoScale.append(mtEvents)
        mt.Scale(normData[ptbin])
    
        
        mtEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MTInvertedAllCutsTailKiller"+ptbin)])
        #mtEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("MTInvertedTauIdPhi"+ptbin)])
        mtEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mtEWK_tmp._setLegendStyles()
        mtEWK_tmp._setLegendLabels()
        mtEWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mtEWK = mtEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        mtEWK.Scale(normEWK[ptbin])
        if includeEWKscale:
            mtEWK.Scale(EWKscale)
        mt.Add(mtEWK, -1)
        mtTailKiller.append(mt)

        ### ---- mt for b tagging factorisation --------------
        ##  mt with factorised b tagging, WITH MET CUT
        mtfac_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MTInvertedNoBtaggingTailKiller"+ptbin)])
        mtfac_tmp._setLegendStyles()
        mtfac_tmp._setLegendLabels()
        mtfac_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtfac_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mtfac = mtfac_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        mtNoBtaggingTailKiller = mtfac_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        ## Normalisation factorised!!!!!!!
        mtfac.Scale(normFactorisedData[ptbin])
        mtfac.Scale(normData[ptbin])
        mtNoBtaggingTailKiller.Scale(normData[ptbin])
        
#        hmtfac.append(mt)        
        mtfacEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MTInvertedNoBtaggingTailKiller"+ptbin)])
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
        
        mtNoBtaggingTailKillerEWK = mtfacEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()        
        mtNoBtaggingTailKillerEWK.Scale(normData[ptbin])       
        mtNoBtaggingTailKiller.Add(mtNoBtaggingTailKillerEWK, -1)
        NoBtaggingTailKiller.append(mtNoBtaggingTailKiller)

        
        # ----------mt after SOFT b tagging, for closure test ---------------
        mtbSoft_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MTInvertedTauIdSoftBtaggingTK"+ptbin)])
        mtbSoft_tmp._setLegendStyles()
        mtbSoft_tmp._setLegendLabels()
        mtbSoft_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtbSoft_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mtbSoft = mtbSoft_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        mtbSoft.Scale(normData[ptbin])
#        hmt.append(mt)        
        mtbSoftEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MTInvertedTauIdSoftBtaggingTK"+ptbin)])
        mtbSoftEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mtbSoftEWK_tmp._setLegendStyles()
        mtbSoftEWK_tmp._setLegendLabels()
        mtbSoftEWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtbSoftEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mtbSoftEWK = mtbSoftEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        mtbSoftEWK.Scale(normEWK[ptbin])
        mtbSoft.Add(mtbSoftEWK, -1)
        hmtbSoft.append(mtbSoft)
       
        # ----------mt after b tagging, no deltaPhi cuts ---------------
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

        # --------- mt after deltaPhi(tau,Met) cut ------------
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


 #######################   
                
        ## mt, no b tagging,  no MET cut, for closure test
        afterJets_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MTInvertedTauIdJet"+ptbin)])
        afterJets_tmp._setLegendStyles()
        afterJets_tmp._setLegendLabels()
        afterJets_tmp.histoMgr.setHistoDrawStyleAll("P") 
        afterJets_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        afterJets = afterJets_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        afterJets.Scale(normData[ptbin])
        
        afterJetsEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MTInvertedTauIdJet"+ptbin)])
        afterJetsEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        afterJetsEWK_tmp._setLegendStyles()
        afterJetsEWK_tmp._setLegendLabels()
        afterJetsEWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
        afterJetsEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        afterJetsEWK = afterJetsEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        afterJetsEWK.Scale(normEWK[ptbin])
        afterJets.Add(afterJetsEWK, -1)
        closureAfterJets.append(afterJets)


        ## mt, no b tagging,  no MET cut, TailKiller, for closure test
        afterJetsTailKiller_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MTInvertedTauIdJetTailKiller"+ptbin)])
        afterJetsTailKiller_tmp._setLegendStyles()
        afterJetsTailKiller_tmp._setLegendLabels()
        afterJetsTailKiller_tmp.histoMgr.setHistoDrawStyleAll("P") 
        afterJetsTailKiller_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        afterJetsTailKiller = afterJetsTailKiller_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        afterJetsTailKiller.Scale(normData[ptbin])
        
        afterJetsTailKillerEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MTInvertedTauIdJetTailKiller"+ptbin)])
        afterJetsTailKillerEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        afterJetsTailKillerEWK_tmp._setLegendStyles()
        afterJetsTailKillerEWK_tmp._setLegendLabels()
        afterJetsTailKillerEWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
        afterJetsTailKillerEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        afterJetsTailKillerEWK = afterJetsTailKillerEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        afterJetsTailKillerEWK.Scale(normEWK[ptbin])
        afterJetsTailKiller.Add(afterJetsTailKillerEWK, -1)
        closureAfterJetsTailKiller.append(afterJetsTailKiller)

 #######################   
                
        ## mt with b veto cut no MET cut
        #mtv_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MTInvertedTauIdBvetoNoMetCut"+ptbin)])
        mtv_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MTInvertedTauIdBveto"+ptbin)])
        mtv_tmp._setLegendStyles()
        mtv_tmp._setLegendLabels()
        mtv_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtv_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mtv = mtv_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        mtv.Scale(normData[ptbin])
#        hmt.append(mt)        
       # mtEWKv_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MTInvertedTauIdBvetoNoMetCut"+ptbin)])
        mtEWKv_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MTInvertedTauIdBveto"+ptbin)])
        mtEWKv_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mtEWKv_tmp._setLegendStyles()
        mtEWKv_tmp._setLegendLabels()
        mtEWKv_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtEWKv_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mtEWKv = mtEWKv_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        mtEWKv.Scale(normEWK[ptbin])
        mtv.Add(mtEWKv, -1)
        closureBveto.append(mtv)
#        hmt.append(mt)

# mt b veto with Dphi cut 
        #mtPhiv_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MTInvertedTauIdBvetoNoMetCutTailKiller"+ptbin)])
        mtPhiv_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MTInvertedTauIdBvetoTailKiller"+ptbin)])
        mtPhiv_tmp._setLegendStyles()
        mtPhiv_tmp._setLegendLabels()
        mtPhiv_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtPhiv_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mtPhiv = mtPhiv_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        mtPhiv.Scale(normData[ptbin])
        #mtPhiEWKv_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MTInvertedTauIdBvetoNoMetCutTailKiller"+ptbin)])
        mtPhiEWKv_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MTInvertedTauIdBvetoTailKiller"+ptbin)])
        mtPhiEWKv_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mtPhiEWKv_tmp._setLegendStyles()
        mtPhiEWKv_tmp._setLegendLabels()
        mtPhiEWKv_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtPhiEWKv_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mtPhiEWKv = mtPhiEWKv_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        mtPhiEWKv.Scale(normEWK[ptbin])
        mtPhiv.Add(mtPhiEWKv, -1)
        closureBvetoTailKiller.append(mtPhiv)

        
# b veto no met cut  
        mtPhiv_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MTInvertedTauIdBvetoNoMetCutTailKiller"+ptbin)])
        ##mtPhiv_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MTInvertedTauIdBvetoTailKiller"+ptbin)])
        mtPhiv_tmp._setLegendStyles()
        mtPhiv_tmp._setLegendLabels()
        mtPhiv_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtPhiv_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mtPhiv = mtPhiv_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        mtPhiv.Scale(normData[ptbin])
        mtPhiEWKv_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MTInvertedTauIdBvetoNoMetCutTailKiller"+ptbin)])
        ##mtPhiEWKv_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MTInvertedTauIdBvetoTailKiller"+ptbin)])
        mtPhiEWKv_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mtPhiEWKv_tmp._setLegendStyles()
        mtPhiEWKv_tmp._setLegendLabels()
        mtPhiEWKv_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtPhiEWKv_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mtPhiEWKv = mtPhiEWKv_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        mtPhiEWKv.Scale(normEWK[ptbin])
        mtPhiv.Add(mtPhiEWKv, -1)
        closureBvetoNoMetCutTailKiller.append(mtPhiv)

#######################   
                
        ## mt with b tagging cut no MET cut
        mtvbb_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MTInvertedTauIdBtagNoMetCut"+ptbin)])
        mtvbb_tmp._setLegendStyles()
        mtvbb_tmp._setLegendLabels()
        mtvbb_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtvbb_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mtvbb = mtvbb_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        mtvbb.Scale(normData[ptbin])
#        hmt.append(mt)        
        mtEWKvbb_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MTInvertedTauIdBtagNoMetCut"+ptbin)])
        mtEWKvbb_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mtEWKvbb_tmp._setLegendStyles()
        mtEWKvbb_tmp._setLegendLabels()
        mtEWKvbb_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtEWKvbb_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mtEWKvbb = mtEWKvbb_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        mtEWKvbb.Scale(normEWK[ptbin])
        mtvbb.Add(mtEWKvbb, -1)
        closureBtag.append(mtvbb)
#        hmt.append(mt)

# mt b veto with Dphi cut 
        #mtPhivbb_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MTInvertedTauIdBtagNoMetCutTailKiller"+ptbin)])
        mtPhivbb_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MTInvertedTauIdBtagNoMetCut"+ptbin)])
        mtPhivbb_tmp._setLegendStyles()
        mtPhivbb_tmp._setLegendLabels()
        mtPhivbb_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtPhivbb_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mtPhivbb = mtPhivbb_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        mtPhivbb.Scale(normData[ptbin])
        #mtPhiEWKvbb_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MTInvertedTauIdBtagNoMetCutTailKiller"+ptbin)])
        mtPhiEWKvbb_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MTInvertedTauIdBtagNoMetCut"+ptbin)])
        mtPhiEWKvbb_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mtPhiEWKvbb_tmp._setLegendStyles()
        mtPhiEWKvbb_tmp._setLegendLabels()
        mtPhiEWKvbb_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtPhiEWKvbb_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mtPhiEWKvbb = mtPhiEWKvbb_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        mtPhiEWKvbb.Scale(normEWK[ptbin])
        mtPhivbb.Add(mtPhiEWKvbb, -1)
        closureBtagTailKiller.append(mtPhivbb)


 #######################   
                
        ## mt with b veto cut and NORMALISATION
        mtveto_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MTInvertedTauIdBveto"+ptbin)])
        mtveto_tmp._setLegendStyles()
        mtveto_tmp._setLegendLabels()
        mtveto_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtveto_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mtvetoNor = mtveto_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        ## normalisation bveto !!!!!!!
        mtvetoNor.Scale(normBtagToBveto[ptbin])
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
        mtPhiveto_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MTInvertedTauIdBvetoTailKiller"+ptbin)])
        mtPhiveto_tmp._setLegendStyles()
        mtPhiveto_tmp._setLegendLabels()
        mtPhiveto_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtPhiveto_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mtPhivetoNor = mtPhiveto_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        mtBvetoTailKiller = mtPhiveto_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        ## normalisation bveto !!!!!!!
        mtPhivetoNor.Scale(normBtagToBveto[ptbin])
        mtBvetoTailKiller.Scale(normData[ptbin])

        
        mtPhiEWKveto_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MTInvertedTauIdBvetoTailKiller"+ptbin)])
        mtPhiEWKveto_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mtPhiEWKveto_tmp._setLegendStyles()
        mtPhiEWKveto_tmp._setLegendLabels()
        mtPhiEWKveto_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mtPhiEWKveto_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
        mtPhiEWKvetoNor  = mtPhiEWKveto_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        mtBvetoTailKillerEWK  = mtPhiEWKveto_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        mtPhiEWKvetoNor.Scale(normBtagToBvetoEWK[ptbin])
        mtBvetoTailKillerEWK.Scale(normEWK[ptbin])

        mtPhivetoNor.Add(mtPhiEWKvetoNor, -1)
        hmtPhivetoNor.append(mtPhivetoNor)
        
        mtBvetoTailKiller.Add(mtBvetoTailKillerEWK, -1)   
        hmtBvetoTailKiller.append(mtBvetoTailKiller)        
 
  

        
########################################
        
        ### MET
        mmt_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MET_InvertedTauIdJets"+ptbin)])
        mmt_tmp._setLegendStyles()
        mmt_tmp._setLegendLabels()
        mmt_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mmt_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))
        mmt = mmt_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        #print "Data MET jets in bins",mmt.GetEntries()
        mmt.Scale(normData[ptbin])
#        hmt.append(mt)

        mmtEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MET_InvertedTauIdJets"+ptbin)])
        mmtEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mmtEWK_tmp._setLegendStyles()
        mmtEWK_tmp._setLegendLabels()
        mmtEWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mmtEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))
        mmtEWK = mmtEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        #print "EWK MET jets in bins",mmtEWK.GetEntries()
        mmtEWK.Scale(normEWK[ptbin])
        mmt.Add(mmtEWK, -1)
        hmet.append(mmt)
        
        ### MET with B tagging
        mmtbtag_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MET_InvertedTauIdBtag"+ptbin)])
        mmtbtag_tmp._setLegendStyles()
        mmtbtag_tmp._setLegendLabels()
        mmtbtag_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mmtbtag_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))
        mmtbtag = mmtbtag_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        mmtbtag.Scale(normData[ptbin])
#        hmt.append(mt)

        mmtbtagEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MET_InvertedTauIdBtag"+ptbin)])
        mmtbtagEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mmtbtagEWK_tmp._setLegendStyles()
        mmtbtagEWK_tmp._setLegendLabels()
        mmtbtagEWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mmtbtagEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))
        mmtbtagEWK = mmtbtagEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        mmtbtagEWK.Scale(normEWK[ptbin])
        mmtbtag.Add(mmtbtagEWK, -1)
        hmetBtagging.append(mmtbtag)
        
       ### MET with B veto
        mmtbveto_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MET_InvertedTauIdBveto"+ptbin)])
        mmtbveto_tmp._setLegendStyles()
        mmtbveto_tmp._setLegendLabels()
        mmtbveto_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mmtbveto_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))
        mmtbveto = mmtbveto_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        print "Data MET bveto in bins",mmtbveto.Integral()
        mmtbveto.Scale(normData[ptbin])
        #        hmt.append(m


        
        mmtbvetoEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MET_InvertedTauIdBveto"+ptbin)])
        mmtbvetoEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mmtbvetoEWK_tmp._setLegendStyles()
        mmtbvetoEWK_tmp._setLegendLabels()
        mmtbvetoEWK_tmp.histoMgr.setHistoDrawStyleAll("P") 
        mmtbvetoEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))
        mmtbvetoEWK = mmtbvetoEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        print "EWK MET bveto in bins",mmtbvetoEWK.Integral()
        mmtbvetoEWK.Scale(normEWK[ptbin])
        mmtbveto.Add(mmtbvetoEWK, -1)
        hmetBveto.append(mmtbveto)

        
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




    events = invertedNoScale[0].Clone("inv")
    events.SetName("inv")
    events.SetTitle("Inverted tau ID")
    events.Reset()
    print "check events in inverted ",events.GetEntries()
    for histo in invertedNoScale:
        events.Add(histo)  
    print "Integral: inverted events with TailKiller = ",events.Integral()
 
    hmtSum = mtTailKiller[0].Clone("mtSum")
    hmtSum.SetName("transverseMass")
    hmtSum.SetTitle("Inverted tau ID")
    hmtSum.Reset()
    print "check hmtsum",hmtSum.GetEntries()
    for histo in mtTailKiller:
        hmtSum.Add(histo)  
    print "Integral: TailKiller cut- EWK = ",hmtSum.Integral()
 
# mt with factorisation, no b tagging, met cut
    mtFactorised = hmtfac[0].Clone("mtSum")
    mtFactorised.SetName("transverseMass")
    mtFactorised.SetTitle("Inverted tau ID")
    mtFactorised.Reset()
    print "check mtFactorised",mtFactorised.GetEntries()
    for histo in hmtfac:
        mtFactorised.Add(histo)  
    print "Integral with bins factorised - EWK = ",mtFactorised.Integral()

    

# mt with SOFT btagging
    mtbSoft = hmtbSoft[0].Clone("mthmtbSoft")
    mtbSoft.SetName("transverseMassBtag")
    mtbSoft.SetTitle("Inverted tau ID")
    mtbSoft.Reset()
#    print "check hmtsum",hmtSum.GetEntries()
    for histo in hmtbSoft:
        mtbSoft.Add(histo)  
    print "Integral: after SOFT B tagging - EWK = ",mtbSoft.Integral()

    
# mt with btagging, no deltaPhi cuts
    hmtSumb = hmtb[0].Clone("mtSumb")
    hmtSumb.SetName("transverseMassBtag")
    hmtSumb.SetTitle("Inverted tau ID")
    hmtSumb.Reset()
#    print "check hmtsum",hmtSum.GetEntries()
    for histo in hmtb:
        hmtSumb.Add(histo)  
    print "Integral: after B tagging - EWK = ",hmtSumb.Integral()


## B veto for closure test With Met cut   
    hClosureBvetoNoMetCutTailKiller = closureBvetoNoMetCutTailKiller[0].Clone("hClosureBvetoNoMet")
    hClosureBvetoNoMetCutTailKiller.SetName("transverseMassBveto")
    hClosureBvetoNoMetCutTailKiller.SetTitle("Inverted tau ID")
    hClosureBvetoNoMetCutTailKiller.Reset()
#    print "check hmtsum B veto",hClosureBvetoNoMetCutTailKiller.GetEntries()
    for histo in closureBvetoNoMetCutTailKiller:
        hClosureBvetoNoMetCutTailKiller.Add(histo)  
    print "Integral: Bveto - EWK  with No met cut = ",hClosureBvetoNoMetCutTailKiller.Integral()

## B veto for closure test With Met cut   
    hClosureBvetoMetCutTailKiller = hmtBvetoTailKiller[0].Clone("hClosureBveto")
    hClosureBvetoMetCutTailKiller.SetName("transverseMassBveto")
    hClosureBvetoMetCutTailKiller.SetTitle("Inverted tau ID")
    hClosureBvetoMetCutTailKiller.Reset()
#    print "check hmtsum B veto",hClosureBvetoMetCutTailKiller.GetEntries()
    for histo in hmtBvetoTailKiller:
        hClosureBvetoMetCutTailKiller.Add(histo)  
    print "Integral: Bveto - EWK  with met cut = ",hClosureBvetoMetCutTailKiller.Integral()

    
## B veto for closure test no Met cut   
    hClosureBveto = closureBveto[0].Clone("hClosureBveto")
    hClosureBveto.SetName("transverseMassBveto")
    hClosureBveto.SetTitle("Inverted tau ID")
    hClosureBveto.Reset()
#    print "check hmtsum B veto",hClosureBveto.GetEntries()
    for histo in closureBveto:
        hClosureBveto.Add(histo)  
    print "Integral: Bveto - EWK  = ",hClosureBveto.Integral()
        
## B veto for closure test tailKiller  no Met cut NO MET CUT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
    hClosureBvetoTailKiller = closureBvetoTailKiller[0].Clone("hClosureBvetoTailKiller")
    hClosureBvetoTailKiller.SetName("transverseMassBveto")
    hClosureBvetoTailKiller.SetTitle("Inverted tau ID")
    hClosureBvetoTailKiller.Reset()
    print "check hmtsum B veto",hClosureBvetoTailKiller.GetEntries()
    for histo in closureBvetoTailKiller:
        hClosureBvetoTailKiller.Add(histo)  
    print "Integral: Bveto - EWK  = ",hClosureBvetoTailKiller.Integral()


## B tag for closure test no Met cut   
    hClosureBtag = closureBtag[0].Clone("hClosureBtag")
    hClosureBtag.SetName("transverseMassBveto")
    hClosureBtag.SetTitle("Inverted tau ID")
    hClosureBtag.Reset()
    print "check hmtsum B veto",hClosureBtag.GetEntries()
    for histo in closureBtag:
        hClosureBtag.Add(histo)  
    print "Integral: Bveto - EWK  = ",hClosureBtag.Integral()
    
## B tag for closure test tailKiller  no Met cut 
    hClosureBtagTailKiller = closureBtagTailKiller[0].Clone("hClosureBtagTailKiller")
    hClosureBtagTailKiller.SetName("transverseMassBveto")
    hClosureBtagTailKiller.SetTitle("Inverted tau ID")
    hClosureBtagTailKiller.Reset()
#    print "check hmtsum B tag hClosureBtagTailKiller ",hClosureBtagTailKiller.GetEntries()
    for histo in closureBtagTailKiller:
        hClosureBtagTailKiller.Add(histo)  
    print "Integral: Btag - EWK  = ",hClosureBtagTailKiller.Integral()


## no btagging,   with Met cut 
    hNoBtaggingTailKiller = NoBtaggingTailKiller[0].Clone("hClosureNoBtag")
    hNoBtaggingTailKiller.SetName("transverseMassNoBtagging")
    hNoBtaggingTailKiller.SetTitle("Inverted tau ID")
    hNoBtaggingTailKiller.Reset()
#    print "check hmtsum after jets",hClosureAfterJets.GetEntries()
    for histo in NoBtaggingTailKiller:
        hNoBtaggingTailKiller.Add(histo)  
    print "Integral: no btag - EWK  = ",hNoBtaggingTailKiller.Integral()

    
## no met cut, no btagging,   no Met cut 
    hClosureAfterJets = closureAfterJets[0].Clone("hClosureAfterJets")
    hClosureAfterJets.SetName("transverseMassNoMetCutNoBtagging")
    hClosureAfterJets.SetTitle("Inverted tau ID")
    hClosureAfterJets.Reset()
#    print "check hmtsum after jets",hClosureAfterJets.GetEntries()
    for histo in closureAfterJets:
        hClosureAfterJets.Add(histo)  
    print "Integral: no btag, no met cut - EWK  = ",hClosureAfterJets.Integral()
    
## no met cut, no btagging,  test tailKiller  no Met cut 
    hClosureAfterJetsTailKiller = closureAfterJetsTailKiller[0].Clone("hClosureAfterJetsTailKiller")
    hClosureAfterJetsTailKiller.SetName("transverseMassNoMetCutNoBtagging")
    hClosureAfterJetsTailKiller.SetTitle("Inverted tau ID")
    hClosureAfterJetsTailKiller.Reset()
 #   print "check hmtsum after jets tail killer",hClosureAfterJetsTailKiller.GetEntries()
    for histo in closureAfterJetsTailKiller:
        hClosureAfterJetsTailKiller.Add(histo)  
    print "Integral: no btag, no met cut, tailkiller - EWK  = ",hClosureAfterJetsTailKiller.Integral()
    
###############################################
## mt with bveto normalised
    mtvetoNor = hmtvetoNor[0].Clone("mtVetoSum")
    mtvetoNor.SetName("transverseMassBvetoNor")
    mtvetoNor.SetTitle("Inverted tau ID")
    mtvetoNor.Reset()
    print "check hmtsum B veto norm",mtvetoNor.GetEntries()
    for histo in hmtvetoNor:
        mtvetoNor.Add(histo)  
    print "Integral:  Bveto normalised- EWK  = ",mtvetoNor.Integral()

## mt with bveto normalised, deltaPhi cuts
    mtPhivetoNor = hmtPhivetoNor[0].Clone("mtVetoSum")
    mtPhivetoNor.SetName("transverseMassBvetoNor")
    mtPhivetoNor.SetTitle("Inverted tau ID")
    mtPhivetoNor.Reset()
    print "check hmtsum B veto norm",mtPhivetoNor.GetEntries()
    for histo in hmtPhivetoNor:
        mtPhivetoNor.Add(histo)  
    print "Integral: Bveto Phi normalised- EWK  = ",mtPhivetoNor.Integral()


    met = hmet[0].Clone("met")
    met.SetName("MET")
    met.SetTitle("Inverted tau Met")
    met.Reset()
    print "check met",met.GetEntries()
    for histo in hmet:
        met.Add(histo)
        
    metBtagging = hmetBtagging[0].Clone("metBtagging")
    metBtagging.SetName("METBtagging")
    metBtagging.SetTitle("Inverted tau Met")
    metBtagging.Reset()
    print "check metBtagging ",metBtagging.GetEntries()
    for histo in hmetBtagging:
        metBtagging.Add(histo)

    metBveto = hmetBveto[0].Clone("metBveto")
    metBveto.SetName("METBveto")
    metBveto.SetTitle("Inverted tau Met")
    metBveto.Reset()
    print "check met Bveto",metBveto.GetEntries()
    for histo in hmetBveto:
        metBveto.Add(histo)

        
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

    if False:    
        MHTJet1phi = hMHTJet1phi[0].Clone("deltaphiMHTJet1")
        MHTJet1phi.SetName("deltaphiMHTJet1")
        MHTJet1phi.SetTitle("Inverted tau deltaphi vs deltaphiMHTJet1 ")
        MHTJet1phi.Reset()
        print "check jetmetphi",MHTJet1phi.GetEntries()
        for histo in hMHTJet1phi:
            MHTJet1phi.Add(histo)

    # mt with standard dphi cut
    mtDphiCut = hmtph[0].Clone("mt")
    mtDphiCut.SetName("mtDeltaPhi")
    mtDphiCut.SetTitle("Inverted tau  mt DeltaPhi cut")
    mtDphiCut.Reset()
    print "check jetmetphi",mtDphiCut.GetEntries()
    for histo in hmtph:
        mtDphiCut.Add(histo)
    print "Integral: Standard Dphi cut- EWK  = ",mtDphiCut.Integral()
   
 
 ################## Control Plots and comparison with baseline(data-EWK) 

 ## mt baseline, plots and EWK substraction
            
 
    closureBaselineNoMetBveto = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("BaseLine/MTBaseLineTauIdNoMetBveto")])
    closureBaselineNoMetBvetoTailKiller = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("BaseLine/MTBaseLineTauIdNoMetBvetoTailKiller")])
#    closureBaselineBvetoMetCut = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("BaseLine/MTBaselineTauIdNoMetBveto")])
#    closureBaselineBvetoMetCutTailKiller = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("BaseLine/MTBaseLineTauIdBvetoTailKiller")])
#    closureBaselineBvetoMetCutTailKillerEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("BaseLine/MTBaseLineTauIdBvetoTailKiller")])
    
    closureBaselineBtag = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("BaseLine/MTBaseLineTauIdNoMetBtag")])
    closureBaselineBtagTailKiller = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("BaseLine/MTBaseLineTauIdNoMetBtagTailKiller")]) 
    closureBaselineBvetoEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("BaseLine/MTBaseLineTauIdNoMetBveto")])
    
    closureBaselineBvetoTailKiller = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("BaseLine/MTBaseLineTauIdBvetoTailKiller")])
    closureBaselineBvetoTailKillerEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("BaseLine/MTBaseLineTauIdBvetoTailKiller")])
    
    closureBaselineBtagEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("BaseLine/MTBaseLineTauIdNoMetBtag")])
    closureBaselineBtagTailKillerEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("BaseLine/MTBaseLineTauIdNoMetBtagTailKiller")])

    closureBaselineNoBtagging = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("BaseLine/MTBaseLineTauIdNoBtagging")])
    closureBaselineNoBtaggingTailKiller = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("BaseLine/MTBaseLineTauIdNoBtaggingTailKiller")])
    closureBaselineNoBtaggingEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("BaseLine/MTBaseLineTauIdNoBtagging")])
    closureBaselineNoBtaggingTailKillerEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("BaseLine/MTBaseLineTauIdNoBtaggingTailKiller")])
    
    closureBaselineNoMetNoBtagging = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("BaseLine/MTBaseLineTauIdNoMetBtagging")])
    closureBaselineNoMetNoBtaggingTailKiller = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("BaseLine/MTBaseLineTauIdNoMetBtaggingTailKiller")])
    closureBaselineNoMetNoBtaggingEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("BaseLine/MTBaseLineTauIdNoMetBtagging")])
    closureBaselineNoMetNoBtaggingTailKillerEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("BaseLine/MTBaseLineTauIdNoMetBtaggingTailKiller")])
    mtEWKBaseline = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("BaseLine/MTBaseLineTauIdAllCutsTailKiller")])
    mtvEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("BaseLine/MTBaseLineTauIdBveto")])            
    mt = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MTInvertedAllCutsTailKiller")]) 
    mtBaseline = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("BaseLine/MTBaseLineTauIdAllCutsTailKiller")])   
    mtPhivEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("BaseLine/MTBaseLineTauIdBvetoTailKiller")])

    
    mtEWKinverted = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MTInvertedAllCutsTailKiller")])
    mtEWKinverted.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mtEWKinverted._setLegendStyles()
    mtEWKinverted._setLegendLabels()
    mtEWKinverted.histoMgr.setHistoDrawStyleAll("P")
    mtEWKinverted.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))  
    hmtEWKinverted = mtEWKinverted.histoMgr.getHisto("EWK").getRootHisto().Clone("Inverted/MTInvertedAllCutsTailKiller")
    # norm = Norm_overall *(1-QCDfract) (0.034446/0.87 * 0.13 = 0.0051
    hmtEWKinverted.Scale(normEWK_inc)

     
    closureBaselineNoMetNoBtagging._setLegendStyles()
    closureBaselineNoMetNoBtagging._setLegendLabels()
    closureBaselineNoMetNoBtagging.histoMgr.setHistoDrawStyleAll("P")
    closureBaselineNoMetNoBtagging.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))  
    hclosureBaselineNoMetNoBtagging = closureBaselineNoMetNoBtagging.histoMgr.getHisto("Data").getRootHisto().Clone("BaseLine/MTBaselineTauIdNoMetBtagging")

    closureBaselineNoMetNoBtaggingTailKiller._setLegendStyles()
    closureBaselineNoMetNoBtaggingTailKiller._setLegendLabels()
    closureBaselineNoMetNoBtaggingTailKiller.histoMgr.setHistoDrawStyleAll("P")
    closureBaselineNoMetNoBtaggingTailKiller.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))  
    hclosureBaselineNoMetNoBtaggingTailKiller = closureBaselineNoMetNoBtaggingTailKiller.histoMgr.getHisto("Data").getRootHisto().Clone("BaseLine/MTBaselineTauIdNoMetBtaggingTailKiller")
    
    closureBaselineNoMetNoBtaggingEWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    closureBaselineNoMetNoBtaggingEWK._setLegendStyles()
    closureBaselineNoMetNoBtaggingEWK._setLegendLabels()
    closureBaselineNoMetNoBtaggingEWK.histoMgr.setHistoDrawStyleAll("P")
    closureBaselineNoMetNoBtaggingEWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))  
    hclosureBaselineNoMetNoBtaggingEWK = closureBaselineNoMetNoBtaggingEWK.histoMgr.getHisto("EWK").getRootHisto().Clone("BaseLine/MTBaselineTauIdNoMetBtagging")

    closureBaselineNoMetNoBtaggingTailKillerEWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    closureBaselineNoMetNoBtaggingTailKillerEWK._setLegendStyles()
    closureBaselineNoMetNoBtaggingTailKillerEWK._setLegendLabels()
    closureBaselineNoMetNoBtaggingTailKillerEWK.histoMgr.setHistoDrawStyleAll("P")
    closureBaselineNoMetNoBtaggingTailKillerEWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))  
    hclosureBaselineNoMetNoBtaggingTailKillerEWK = closureBaselineNoMetNoBtaggingTailKillerEWK.histoMgr.getHisto("EWK").getRootHisto().Clone("BaseLine/MTBaselineTauIdNoMetBtaggingTailKiller")
    
 ## make baseline QCD
    hclosureBaselineNoMetNoBtaggingTailKiller_QCD = hclosureBaselineNoMetNoBtaggingTailKiller.Clone("QCD")
    hclosureBaselineNoMetNoBtaggingTailKiller_QCD.Add(hclosureBaselineNoMetNoBtaggingTailKillerEWK,-1)
    
    closureBaselineNoBtagging._setLegendStyles()
    closureBaselineNoBtagging._setLegendLabels()
    closureBaselineNoBtagging.histoMgr.setHistoDrawStyleAll("P")
    closureBaselineNoBtagging.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))  
    hclosureBaselineNoBtagging = closureBaselineNoBtagging.histoMgr.getHisto("Data").getRootHisto().Clone("BaseLine/MTBaselineTauIdNoBtagging")

    closureBaselineNoBtaggingTailKiller._setLegendStyles()
    closureBaselineNoBtaggingTailKiller._setLegendLabels()
    closureBaselineNoBtaggingTailKiller.histoMgr.setHistoDrawStyleAll("P")
    closureBaselineNoBtaggingTailKiller.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))  
    hclosureBaselineNoBtaggingTailKiller = closureBaselineNoBtaggingTailKiller.histoMgr.getHisto("Data").getRootHisto().Clone("BaseLine/MTBaselineTauIdNoBtaggingTailKiller")
    
    closureBaselineNoBtaggingEWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    closureBaselineNoBtaggingEWK._setLegendStyles()
    closureBaselineNoBtaggingEWK._setLegendLabels()
    closureBaselineNoBtaggingEWK.histoMgr.setHistoDrawStyleAll("P")
    closureBaselineNoBtaggingEWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))  
    hclosureBaselineNoBtaggingEWK = closureBaselineNoBtaggingEWK.histoMgr.getHisto("EWK").getRootHisto().Clone("BaseLine/MTBaselineTauIdNoBtagging")

    closureBaselineNoBtaggingTailKillerEWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    closureBaselineNoBtaggingTailKillerEWK._setLegendStyles()
    closureBaselineNoBtaggingTailKillerEWK._setLegendLabels()
    closureBaselineNoBtaggingTailKillerEWK.histoMgr.setHistoDrawStyleAll("P")
    closureBaselineNoBtaggingTailKillerEWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))  
    hclosureBaselineNoBtaggingTailKillerEWK = closureBaselineNoBtaggingTailKillerEWK.histoMgr.getHisto("EWK").getRootHisto().Clone("BaseLine/MTBaselineTauIdNoBtaggingTailKiller")
    
 ## make baseline QCD
    hclosureBaselineNoBtaggingTailKiller_QCD = hclosureBaselineNoBtaggingTailKiller.Clone("QCD")
    hclosureBaselineNoBtaggingTailKiller_QCD.Add(hclosureBaselineNoBtaggingTailKillerEWK,-1)



    closureBaselineBveto = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("BaseLine/MTBaseLineTauIdNoMetBveto")])   
    closureBaselineBveto.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    closureBaselineBveto._setLegendStyles()
    closureBaselineBveto._setLegendLabels()
    closureBaselineBveto.histoMgr.setHistoDrawStyleAll("P")
    closureBaselineBveto.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))  
    hClosureBaselineBveto = closureBaselineBveto.histoMgr.getHisto("Data").getRootHisto().Clone("BaseLine/MTBaselineTauIdNoMetBveto")


    closureBaselineBvetoEWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    closureBaselineBvetoEWK._setLegendStyles()
    closureBaselineBvetoEWK._setLegendLabels()
    closureBaselineBvetoEWK.histoMgr.setHistoDrawStyleAll("P")
    closureBaselineBvetoEWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))  
    hClosureBaselineBvetoEWK = closureBaselineBvetoEWK.histoMgr.getHisto("EWK").getRootHisto().Clone("BaseLine/MTBaselineTauIdNoMetBveto")

## make baseline QCD
    hClosureBaselineBveto_QCD = hClosureBaselineBveto.Clone("QCD")
    hClosureBaselineBveto_QCD.Add(hClosureBaselineBvetoEWK,-1)

   
    closureBaselineNoMetBvetoTailKiller.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    closureBaselineNoMetBvetoTailKiller._setLegendStyles()
    closureBaselineNoMetBvetoTailKiller._setLegendLabels()
    closureBaselineNoMetBvetoTailKiller.histoMgr.setHistoDrawStyleAll("P")
    closureBaselineNoMetBvetoTailKiller.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))  
    hClosureBaselineNoMetBvetoTailKiller = closureBaselineNoMetBvetoTailKiller.histoMgr.getHisto("Data").getRootHisto().Clone("BaseLine/MTBaselineTauIdNoMetBvetoTailKiller")

    closureBaselineNoMetBvetoTailKillerEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("BaseLine/MTBaseLineTauIdNoMetBvetoTailKiller")])  
    closureBaselineNoMetBvetoTailKillerEWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    closureBaselineNoMetBvetoTailKillerEWK._setLegendStyles()
    closureBaselineNoMetBvetoTailKillerEWK._setLegendLabels()
    closureBaselineNoMetBvetoTailKillerEWK.histoMgr.setHistoDrawStyleAll("P")
    closureBaselineNoMetBvetoTailKillerEWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))  
    hClosureBaselineNoMetBvetoTailKillerEWK = closureBaselineNoMetBvetoTailKillerEWK.histoMgr.getHisto("EWK").getRootHisto().Clone("BaseLine/MTBaselineTauIdNoMetBvetoTailKiller")

    
    hClosureBaselineNoMetBvetoTailKiller_QCD = hClosureBaselineNoMetBvetoTailKiller.Clone("QCD")
    hClosureBaselineNoMetBvetoTailKiller_QCD.Add(hClosureBaselineNoMetBvetoTailKillerEWK,-1)


## closure b veto and MEt cut
    closureBaselineBvetoMetCutTailKiller = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("BaseLine/MTBaseLineTauIdBvetoTailKiller")])  
    closureBaselineBvetoMetCutTailKiller.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    closureBaselineBvetoMetCutTailKiller._setLegendStyles()
    closureBaselineBvetoMetCutTailKiller._setLegendLabels()
    closureBaselineBvetoMetCutTailKiller.histoMgr.setHistoDrawStyleAll("P")
    closureBaselineBvetoMetCutTailKiller.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))  
    hClosureBaselineBvetoMetCutTailKiller = closureBaselineBvetoMetCutTailKiller.histoMgr.getHisto("Data").getRootHisto().Clone("BaseLine/MTBaselineTauIdBvetoTailKiller")

    closureBaselineBvetoMetCutTailKillerEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("BaseLine/MTBaseLineTauIdBvetoTailKiller")])
    closureBaselineBvetoMetCutTailKillerEWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    closureBaselineBvetoMetCutTailKillerEWK._setLegendStyles()
    closureBaselineBvetoMetCutTailKillerEWK._setLegendLabels()
    closureBaselineBvetoMetCutTailKillerEWK.histoMgr.setHistoDrawStyleAll("P")
    closureBaselineBvetoMetCutTailKillerEWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))  
    hClosureBaselineBvetoMetCutTailKillerEWK = closureBaselineBvetoMetCutTailKillerEWK.histoMgr.getHisto("EWK").getRootHisto().Clone("BaseLine/MTBaselineTauIdBvetoTailKiller")    
    hClosureBaselineBvetoMetCutTailKiller_QCD = hClosureBaselineBvetoMetCutTailKiller.Clone("QCD")
    hClosureBaselineBvetoMetCutTailKiller_QCD.Add(hClosureBaselineBvetoMetCutTailKillerEWK,-1)


## closure soft b  and MEt cut
    closureBaselineSoftBtaggingTK = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("BaseLine/MTBaseLineTauIdSoftBtaggingTK")])  
#    closureBaselineSoftBtaggingTK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    closureBaselineSoftBtaggingTK._setLegendStyles()
    closureBaselineSoftBtaggingTK._setLegendLabels()
    closureBaselineSoftBtaggingTK.histoMgr.setHistoDrawStyleAll("P")
    closureBaselineSoftBtaggingTK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))  
    hClosureBaselineSoftBtaggingTK = closureBaselineSoftBtaggingTK.histoMgr.getHisto("Data").getRootHisto().Clone("BaseLine/MTBaseLineTauIdSoftBtaggingTK")

    closureBaselineSoftBtaggingTKEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("BaseLine/MTBaseLineTauIdSoftBtaggingTK")])
    closureBaselineSoftBtaggingTKEWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    closureBaselineSoftBtaggingTKEWK._setLegendStyles()
    closureBaselineSoftBtaggingTKEWK._setLegendLabels()
    closureBaselineSoftBtaggingTKEWK.histoMgr.setHistoDrawStyleAll("P")
    closureBaselineSoftBtaggingTKEWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))  
    hClosureBaselineSoftBtaggingTKEWK = closureBaselineSoftBtaggingTKEWK.histoMgr.getHisto("EWK").getRootHisto().Clone("BaseLine/MTBaseLineTauIdSoftBtaggingTK")
    
    hClosureBaselineSoftBtaggingTK_QCD = hClosureBaselineSoftBtaggingTK.Clone("QCD")
    hClosureBaselineSoftBtaggingTK_QCD.Add(hClosureBaselineSoftBtaggingTKEWK,-1)


     
    invertedQCD = InvertedTauID()
    invertedQCD.setLumi(datasets.getDataset("Data").getLuminosity())
      
  

#####  -------------- Comparison plots --------------------
    

# MET efficiency
    Btagging = metBtagging.Clone("metBtagging")
    allMet = met.Clone("met")
    print " met batg",Btagging.GetEntries()
    print "met after tauId ",allMet.GetEntries()
    invertedQCD.setLabel("MetBtaggingEfficiency")
    invertedQCD.efficiency(Btagging, allMet,"MetBtaggingEfficiency")
    
    # MET efficiency
    Bveto = metBveto.Clone("metBveto")
    allMet = met.Clone("met")
    print " met batg",Bveto.GetEntries()
    print "met after tauId ",allMet.GetEntries()
    invertedQCD.setLabel("MetBvetoEfficiency")
    invertedQCD.efficiency(Bveto, allMet,"MetBvetoEfficiency")







#################################################3

#########  toimii
# mt inverted-baseline comparison with bveto and MET CUT, closure
    #bveto_inverted =hClosureBvetoTailKiller.Clone("hmtvSum")
    bveto_inverted = hClosureBvetoMetCutTailKiller.Clone("hmtvSum")
    bveto_baseline = hClosureBaselineBvetoMetCutTailKiller_QCD.Clone("hmtvBaseline_QCD")
    print "bveto_inverted",bveto_inverted.GetEntries()
    print "bveto_baseline ",bveto_baseline.GetEntries()
    invertedQCD.setLabel("BvetoTailKillerClosure")
    invertedQCD.mtComparison(bveto_inverted, bveto_baseline,"BvetoTailKillerClosure",sysError=sysError)
    
# mt inverted-baseline comparison with bveto, closure
    bveto_inverted = hClosureBveto.Clone("hmtvSum")
    bveto_baseline = hClosureBaselineBveto_QCD.Clone("hmtvBaseline_QCD")
    print "bveto_inverted",bveto_inverted.GetEntries()
    print "bveto_baseline ",bveto_baseline.GetEntries()
    invertedQCD.setLabel("MtBvetoInvertedVsBaselineClosure")
    invertedQCD.mtComparison(bveto_inverted, bveto_baseline,"MtBvetoInvertedVsBaselineClosure")



########################################3




        
# mt inverted-baseline comparison with BVETO and deltaPhi cuts, closure, NO MET CUT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    bvetoDphi_inverted = hClosureBvetoNoMetCutTailKiller.Clone("hmtPhivSum")
    bvetoDphi_baseline = hClosureBaselineNoMetBvetoTailKiller_QCD.Clone("hmtPhivBaseline_QCD")
    invertedQCD.setLabel("MtNoMetBvetoInvertedVsBaselineTailKillerClosure")
    invertedQCD.mtComparison(bvetoDphi_inverted, bvetoDphi_baseline,"MtNoMetBvetoInvertedVsBaselineTailKillerClosure",sysError=sysError)
    #invertedQCD.mtComparison(bvetoDphi_inverted, bvetoDphi_baseline,"MtNoMetBvetoInvertedVsBaselineTailKillerClosure")
    
    
################################ 
# mt inverted-baseline comparison, no b tagging, NO MET CUT  and deltaPhi cuts, closure
    afterJets_inverted = hClosureAfterJetsTailKiller.Clone("afterjets")
    afterJets_baseline = hclosureBaselineNoMetNoBtaggingTailKiller_QCD.Clone("afterjets_QCD")
    invertedQCD.setLabel("MtAfterJetsInvertedVsBaselineTailKillerClosure")
    invertedQCD.mtComparison(afterJets_inverted,afterJets_baseline,"MtAfterJetsInvertedVsBaselineTailKillerClosure")
##############################



################################  
# mt inverted-baseline comparison, SOFT b tagging, MET CUT  and TK cuts, closure
    afterJets_inverted = mtbSoft.Clone("mtbSoft")
    afterJets_baseline = hClosureBaselineSoftBtaggingTK_QCD.Clone("mtbSoft_QCD")
    invertedQCD.setLabel("MtSoftBtaggingTKClosure")
    invertedQCD.mtComparison(afterJets_inverted,afterJets_baseline,"MtSoftBtaggingTKClosure")
##############################

    
# mt inverted-baseline comparison, no b tagging, with met cut  and deltaPhi cuts, closure
    afterMet_inverted = hNoBtaggingTailKiller.Clone("afterMet")
    afterMet_baseline = hclosureBaselineNoBtaggingTailKiller_QCD.Clone("aftermet_QCD")
    invertedQCD.setLabel("MtNoBtaggingInvertedVsBaselineTailKillerClosure")
    invertedQCD.mtComparison(afterMet_inverted,afterMet_baseline,"MtNoBtaggingInvertedVsBaselineTailKillerClosure")

    
# mt inverted comparison bveto normalised and  btagging,  no deltaPhi cuts
    btag_inverted = hmtSumb.Clone("mtSumb")
    bvetoNor_inverted = mtvetoNor.Clone("hmtBaseline_QCD")
    invertedQCD.setLabel("MtNormalisedBvetoNoDphiCuts")
    invertedQCD.mtComparison(btag_inverted , bvetoNor_inverted,"MtNormalisedBvetoNoDphiCuts")


# mt inverted comparison bveto normalised and  btagging,  no deltaPhi cuts
    allCuts_inverted = hmtSum.Clone("mtSum") 
    allCuts_inverted.Scale(1./hmtSum.Integral())
    afterMet_inverted = hNoBtaggingTailKiller.Clone("afterMet")
    afterMet_inverted.Scale(1./hNoBtaggingTailKiller.Integral())
    invertedQCD.setLabel("MtBtaggingNoBtaggingInverted")
    invertedQCD.mtComparison(afterMet_inverted, allCuts_inverted,"MtBtaggingNoBtaggingInverted")

# mt plot with TailKiller 
    allCuts_inverted = hmtSum.Clone("mtSum")
    invertedQCD.setLabel("MtWithAllCutsTailKiller")
    invertedQCD.mtComparison(allCuts_inverted, allCuts_inverted,"MtWithAllCutsTailKiller")
    
## mt inverted comparison bveto normalised and  btagging,  with deltaPhi cuts
    btagTailKiller_inverted = hmtSum.Clone("mtSumb")
    bvetoNorTailKiller_inverted = mtPhivetoNor.Clone("hmtBaseline_QCD")
    invertedQCD.setLabel("MtNormalisedBvetoTailKiller")
    invertedQCD.mtComparison(bvetoNorTailKiller_inverted, btagTailKiller_inverted ,"MtNormalisedBvetoTailKiller")


   # mt inverted comparison bveto normalised and  btagging,  no deltaPhi cuts
    btag_inverted = hmtSumb.Clone("mtSumb")
    bvetoNor_inverted = mtvetoNor.Clone("hmtBaseline_QCD")
    invertedQCD.setLabel("MtNormalisedBveto")
    invertedQCD.mtComparison(btag_inverted , bvetoNor_inverted,"MtNormalisedBveto")

   
    bveto_inverted2 = hClosureBveto.Clone("ClosureBveto")
    bveto_inverted2.Scale(1./hClosureBveto.GetMaximum())
    btag_inverted2 = hClosureBtag.Clone("ClosureBtag")
    btag_inverted2.Scale(1./hClosureBtag.GetMaximum())
    invertedQCD.setLabel("MtBvetoBtagInvertedClosure")
    invertedQCD.mtComparison(btag_inverted2 , bveto_inverted2,"MtBvetoBtagInvertedClosure")
#    print "bveto_inverted2",bveto_inverted2.GetEntries()
#    print "btag_inverted2 ",btag_inverted2.GetEntries()

    bvetoTailKiller_inverted = hClosureBvetoTailKiller.Clone("hmtvSum")
    bvetoTailKiller_inverted.Scale(1./hClosureBvetoTailKiller.GetMaximum())
    btagTailKiller_inverted = hClosureBtagTailKiller.Clone("mtSumb")
    print "hClosureBtagTailKiller ",hClosureBtagTailKiller.GetEntries()
#    btagTailKiller_inverted.Scale(1./hClosureBtagTailKiller.GetMaximum())
    invertedQCD.setLabel("MtBvetoBtagInvertedTailKillerClosure")
    invertedQCD.mtComparison(bvetoTailKiller_inverted , btagTailKiller_inverted,"MtBvetoBtagInvertedTailKillerClosure")

    
    afterJetsTailKiller_inverted2 = hClosureAfterJetsTailKiller.Clone("afterjets")
    afterJetsTailKiller_inverted2.Scale(1./hClosureAfterJetsTailKiller.GetMaximum())
    invertedQCD.setLabel("MtNoBtagBtagInvertedTailKillerClosure")
    invertedQCD.mtComparison(afterJetsTailKiller_inverted2, btagTailKiller_inverted,"MtNoBtagBtagInvertedTailKillerClosure")

    
# mt inverted-inverted factorized comparison with btagging and deltaPhi cuts
#    btagDphi_inverted = mtHMTjet2Cut.Clone("mtHMTjet2Cut")
#    btagDphi_factorised =  mtFactorised.Clone("mtFactorised")
#    invertedQCD.setLabel("MtPhiCutBtagInvertedVsFactorised")
#    invertedQCD.mtComparison(btagDphi_inverted, btagDphi_factorised,"MtBtagDphiInvertedVsFactorised")
   
# mt shape comparison bveto vs btag
    btagged_nor = mtFactorised.Clone("mtFactorised")
    btagged_nor.Scale(1./mtFactorised.GetMaximum())
    print "btagged_nor",btagged_nor.GetMaximum()
    
    bveto_nor = hmtPhivSum.Clone("hmtPhivSum")
    bveto_nor.Scale(1./hmtPhivSum.GetMaximum())
    print "bveto_nor",bveto_nor.GetMaximum()

    invertedQCD.setLabel("mtBTagVsBvetoInverted")
    invertedQCD.mtComparison(btagged_nor, bveto_nor,"mtBTagVsBvetoInverted")


# mt inverted no b tagging, no met cut - inverted no met cut, b tagging
    hClosureAfterJetsTailKiller_nor = hClosureAfterJetsTailKiller.Clone("hClosureAfterJetsTailKiller")
    hClosureAfterJetsTailKiller_nor.Scale(1./hClosureAfterJetsTailKiller.GetMaximum())
    print "hClosureAfterJetsTailKiller_nor",bveto_nor.GetMaximum()
    hClosureBtagTailKiller_nor = hClosureBtagTailKiller.Clone("hBtaggingTailKiller")
#    hClosureBtagTailKiller_nor.Scale(1./hClosureBtagTailKiller.GetMaximum())
    invertedQCD.setLabel("MtBtagVsNoBtagNoMetInvertedTailKillerClosure")
    invertedQCD.mtComparison(hClosureAfterJetsTailKiller_nor,hClosureBtagTailKiller_nor,"MtBtagVsNoBtagNoMetInvertedTailKillerClosure")
    
#################  Inclusive plots ###################
    # back-to-back, jet0
    #inverted part
    rJet0BackToBack = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/QCDTailKillerJet0BackToBackInverted")])
    rJet0BackToBack.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))  
    RadiusrJet0BackToBack  = rJet0BackToBack.histoMgr.getHisto("Data").getRootHisto().Clone("Inverted/QCDTailKillerJet0BackToBackInverted")
    RadiusrJet0BackToBack.Scale(norm_inc)

    rJet0BackToBack_EWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/QCDTailKillerJet0BackToBackInverted")])
    rJet0BackToBack_EWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    rJet0BackToBack_EWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))  
    hrJet0BackToBack_EWK = rJet0BackToBack_EWK.histoMgr.getHisto("EWK").getRootHisto().Clone("Inverted/QCDTailKillerJet0BackToBackInverted")
    hrJet0BackToBack_EWK.Scale(normEWK_inc)
    RadiusrJet0BackToBack.Add(hrJet0BackToBack_EWK, -1)

    
   #baseline part
    rJet0BackToBack = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("BaseLine/QCDTailKillerJet0BackToBackBaseline")])
    rJet0BackToBack.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))  
    hrJet0BackToBack_baseline = rJet0BackToBack.histoMgr.getHisto("Data").getRootHisto().Clone("BaseLine/QCDTailKillerJet0BackToBackBaseline")

    rJet0BackToBack_EWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("BaseLine/QCDTailKillerJet0BackToBackBaseline")])
    rJet0BackToBack_EWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    rJet0BackToBack_EWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))  
    hrJet0BackToBack_baseline_EWK = rJet0BackToBack_EWK.histoMgr.getHisto("EWK").getRootHisto().Clone("BaseLine/QCDTailKillerJet0BackToBackBaseline")
    
    RadiusrJet0BackToBack_QCD = hrJet0BackToBack_baseline.Clone("QCD")
    RadiusrJet0BackToBack_QCD.Add(hrJet0BackToBack_baseline_EWK,-1)
    
# TK radius
    radius_inverted = RadiusrJet0BackToBack.Clone("r")
    radius_baseline = RadiusrJet0BackToBack_QCD.Clone("r_QCD")
    invertedQCD.setLabel("RadiusJet0BackToBack")
    invertedQCD.mtComparison(radius_inverted , radius_baseline,"RadiusJet0BackToBack")
    
    # collinear, jet0
    #inverted part
    rJet0BackToBack = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/QCDTailKillerJet0CollinearInverted")])
    rJet0BackToBack.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))  
    RadiusrJet0Collinear  = rJet0BackToBack.histoMgr.getHisto("Data").getRootHisto().Clone("Inverted/QCDTailKillerJet0CollinearInverted")
    RadiusrJet0Collinear.Scale(norm_inc)

    rJet0BackToBack_EWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/QCDTailKillerJet0CollinearInverted")])
    rJet0BackToBack_EWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    rJet0BackToBack_EWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))  
    hrJet0BackToBack_EWK = rJet0BackToBack_EWK.histoMgr.getHisto("EWK").getRootHisto().Clone("Inverted/QCDTailKillerJet0CollinearInverted")
    hrJet0BackToBack_EWK.Scale(normEWK_inc)
    RadiusrJet0Collinear.Add(hrJet0BackToBack_EWK, -1)

    
   #baseline part
    rJet0BackToBack = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("BaseLine/QCDTailKillerJet0CollinearBaseline")])
    rJet0BackToBack.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))  
    hrJet0BackToBack_baseline = rJet0BackToBack.histoMgr.getHisto("Data").getRootHisto().Clone("BaseLine/QCDTailKillerJet0CollinearBaseline")

    rJet0BackToBack_EWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("BaseLine/QCDTailKillerJet0CollinearBaseline")])
    rJet0BackToBack_EWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    rJet0BackToBack_EWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))  
    hrJet0BackToBack_baseline_EWK = rJet0BackToBack_EWK.histoMgr.getHisto("EWK").getRootHisto().Clone("BaseLine/QCDTailKillerJet0CollinearBaseline")
    
    RadiusrJet0Collinear_QCD = hrJet0BackToBack_baseline.Clone("QCD")
    RadiusrJet0Collinear_QCD.Add(hrJet0BackToBack_baseline_EWK,-1)
    
# TK radius
    radius_inverted = RadiusrJet0Collinear.Clone("r")
    radius_baseline = RadiusrJet0Collinear_QCD.Clone("r_QCD")
    invertedQCD.setLabel("RadiusJet0Collinear")
    invertedQCD.mtComparison(radius_inverted , radius_baseline,"RadiusJet0Collinear")



#################  Inclusive plots ###################
    # back-to-back, jet1
    #inverted part
    rJet0BackToBack = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/QCDTailKillerJet1BackToBackInverted")])
    rJet0BackToBack.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))  
    RadiusrJet1BackToBack  = rJet0BackToBack.histoMgr.getHisto("Data").getRootHisto().Clone("Inverted/QCDTailKillerJet1BackToBackInverted")
    RadiusrJet1BackToBack.Scale(norm_inc)

    rJet0BackToBack_EWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/QCDTailKillerJet1BackToBackInverted")])
    rJet0BackToBack_EWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    rJet0BackToBack_EWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))  
    hrJet0BackToBack_EWK = rJet0BackToBack_EWK.histoMgr.getHisto("EWK").getRootHisto().Clone("Inverted/QCDTailKillerJet1BackToBackInverted")
    hrJet0BackToBack_EWK.Scale(normEWK_inc)
    RadiusrJet1BackToBack.Add(hrJet0BackToBack_EWK, -1)

    
   #baseline part
    rJet0BackToBack = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("BaseLine/QCDTailKillerJet1BackToBackBaseline")])
    rJet0BackToBack.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))  
    hrJet0BackToBack_baseline = rJet0BackToBack.histoMgr.getHisto("Data").getRootHisto().Clone("BaseLine/QCDTailKillerJet1BackToBackBaseline")

    rJet0BackToBack_EWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("BaseLine/QCDTailKillerJet1BackToBackBaseline")])
    rJet0BackToBack_EWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    rJet0BackToBack_EWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))  
    hrJet0BackToBack_baseline_EWK = rJet0BackToBack_EWK.histoMgr.getHisto("EWK").getRootHisto().Clone("BaseLine/QCDTailKillerJet1BackToBackBaseline")
    
    RadiusrJet1BackToBack_QCD = hrJet0BackToBack_baseline.Clone("QCD")
    RadiusrJet1BackToBack_QCD.Add(hrJet0BackToBack_baseline_EWK,-1)
    
# TK radius
    radius_inverted = RadiusrJet1BackToBack.Clone("r")
    radius_baseline = RadiusrJet1BackToBack_QCD.Clone("r_QCD")
    invertedQCD.setLabel("RadiusJet1BackToBack")
    invertedQCD.mtComparison(radius_inverted , radius_baseline,"RadiusJet1BackToBack")


    
    # collinear, jet1
    #inverted part
    rJet0BackToBack = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/QCDTailKillerJet1CollinearInverted")])
    rJet0BackToBack.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))  
    RadiusrJet1Collinear  = rJet0BackToBack.histoMgr.getHisto("Data").getRootHisto().Clone("Inverted/QCDTailKillerJet1CollinearInverted")
    RadiusrJet1Collinear.Scale(norm_inc)

    rJet0BackToBack_EWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/QCDTailKillerJet1CollinearInverted")])
    rJet0BackToBack_EWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    rJet0BackToBack_EWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))  
    hrJet0BackToBack_EWK = rJet0BackToBack_EWK.histoMgr.getHisto("EWK").getRootHisto().Clone("Inverted/QCDTailKillerJet1CollinearInverted")
    hrJet0BackToBack_EWK.Scale(normEWK_inc)
    RadiusrJet1Collinear.Add(hrJet0BackToBack_EWK, -1)

    
   #baseline part
    rJet0BackToBack = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("BaseLine/QCDTailKillerJet1CollinearBaseline")])
    rJet0BackToBack.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))  
    hrJet0BackToBack_baseline = rJet0BackToBack.histoMgr.getHisto("Data").getRootHisto().Clone("BaseLine/QCDTailKillerJet1CollinearBaseline")

    rJet0BackToBack_EWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("BaseLine/QCDTailKillerJet1CollinearBaseline")])
    rJet0BackToBack_EWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    rJet0BackToBack_EWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))  
    hrJet0BackToBack_baseline_EWK = rJet0BackToBack_EWK.histoMgr.getHisto("EWK").getRootHisto().Clone("BaseLine/QCDTailKillerJet1CollinearBaseline")
    
    RadiusrJet1Collinear_QCD = hrJet0BackToBack_baseline.Clone("QCD")
    RadiusrJet1Collinear_QCD.Add(hrJet0BackToBack_baseline_EWK,-1)
    
# TK radius
    radius_inverted = RadiusrJet1Collinear.Clone("r")
    radius_baseline = RadiusrJet1Collinear_QCD.Clone("r_QCD")
    invertedQCD.setLabel("RadiusJet1Collinear")
    invertedQCD.mtComparison(radius_inverted , radius_baseline,"RadiusJet1Collinear")

#################  Inclusive plots ###################
    # back-to-back, jet2
    #inverted part
    rJet0BackToBack = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/QCDTailKillerJet2BackToBackInverted")])
    rJet0BackToBack.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))  
    RadiusrJet2BackToBack  = rJet0BackToBack.histoMgr.getHisto("Data").getRootHisto().Clone("Inverted/QCDTailKillerJet2BackToBackInverted")
    RadiusrJet2BackToBack.Scale(norm_inc)

    rJet0BackToBack_EWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/QCDTailKillerJet2BackToBackInverted")])
    rJet0BackToBack_EWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    rJet0BackToBack_EWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))  
    hrJet0BackToBack_EWK = rJet0BackToBack_EWK.histoMgr.getHisto("EWK").getRootHisto().Clone("Inverted/QCDTailKillerJet2BackToBackInverted")
    hrJet0BackToBack_EWK.Scale(normEWK_inc)
    RadiusrJet2BackToBack.Add(hrJet0BackToBack_EWK, -1)

    
   #baseline part
    rJet0BackToBack = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("BaseLine/QCDTailKillerJet2BackToBackBaseline")])
    rJet0BackToBack.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))  
    hrJet0BackToBack_baseline = rJet0BackToBack.histoMgr.getHisto("Data").getRootHisto().Clone("BaseLine/QCDTailKillerJet2BackToBackBaseline")

    rJet0BackToBack_EWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("BaseLine/QCDTailKillerJet2BackToBackBaseline")])
    rJet0BackToBack_EWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    rJet0BackToBack_EWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))  
    hrJet0BackToBack_baseline_EWK = rJet0BackToBack_EWK.histoMgr.getHisto("EWK").getRootHisto().Clone("BaseLine/QCDTailKillerJet2BackToBackBaseline")
    
    RadiusrJet2BackToBack_QCD = hrJet0BackToBack_baseline.Clone("QCD")
    RadiusrJet2BackToBack_QCD.Add(hrJet0BackToBack_baseline_EWK,-1)
    
# TK radius
    radius_inverted = RadiusrJet2BackToBack.Clone("r")
    radius_baseline = RadiusrJet2BackToBack_QCD.Clone("r_QCD")
    invertedQCD.setLabel("RadiusJet2BackToBack")
    invertedQCD.mtComparison(radius_inverted , radius_baseline,"RadiusJet2BackToBack")
    
    # collinear, jet2
    #inverted part
    rJet0BackToBack = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/QCDTailKillerJet2CollinearInverted")])
    rJet0BackToBack.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))  
    RadiusrJet2Collinear  = rJet0BackToBack.histoMgr.getHisto("Data").getRootHisto().Clone("Inverted/QCDTailKillerJet2CollinearInverted")
    RadiusrJet2Collinear.Scale(norm_inc)

    rJet0BackToBack_EWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/QCDTailKillerJet2CollinearInverted")])
    rJet0BackToBack_EWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    rJet0BackToBack_EWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))  
    hrJet0BackToBack_EWK = rJet0BackToBack_EWK.histoMgr.getHisto("EWK").getRootHisto().Clone("Inverted/QCDTailKillerJet2CollinearInverted")
    hrJet0BackToBack_EWK.Scale(normEWK_inc)
    RadiusrJet2Collinear.Add(hrJet0BackToBack_EWK, -1)

    
   #baseline part
    rJet0BackToBack = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("BaseLine/QCDTailKillerJet2CollinearBaseline")])
    rJet0BackToBack.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))  
    hrJet0BackToBack_baseline = rJet0BackToBack.histoMgr.getHisto("Data").getRootHisto().Clone("BaseLine/QCDTailKillerJet2CollinearBaseline")

    rJet0BackToBack_EWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("BaseLine/QCDTailKillerJet2CollinearBaseline")])
    rJet0BackToBack_EWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    rJet0BackToBack_EWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))  
    hrJet0BackToBack_baseline_EWK = rJet0BackToBack_EWK.histoMgr.getHisto("EWK").getRootHisto().Clone("BaseLine/QCDTailKillerJet2CollinearBaseline")
    
    RadiusrJet2Collinear_QCD = hrJet0BackToBack_baseline.Clone("QCD")
    RadiusrJet2Collinear_QCD.Add(hrJet0BackToBack_baseline_EWK,-1)
    
# TK radius
    radius_inverted = RadiusrJet2Collinear.Clone("r")
    radius_baseline = RadiusrJet2Collinear_QCD.Clone("r_QCD")
    invertedQCD.setLabel("RadiusJet2Collinear")
    invertedQCD.mtComparison(radius_inverted , radius_baseline,"RadiusJet2Collinear")


########################
    
    mt._setLegendStyles()
    mt._setLegendLabels()
    mt.histoMgr.setHistoDrawStyleAll("P")
    mt.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))  
    hmt = mt.histoMgr.getHisto("Data").getRootHisto().Clone("Inverted/MTInvertedAllCutsTailKiller")
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
    canvas39.Print("transverseMassInclusive.png")
    canvas39.Print("transverseMassInclusive.C")
    print " "
    print "Integral inclusive, tailKiller = ",hmt.Integral()
    print "Integral inclusive - EWK, tailKiller = ",hmt_subs.Integral()
    print " "

#################################################
 ##  mT with TailKiller cuts
            
    mtBaseline._setLegendStyles()
    mtBaseline._setLegendLabels()
    mtBaseline.histoMgr.setHistoDrawStyleAll("P")
    mtBaseline.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))  
    hmtBaseline = mtBaseline.histoMgr.getHisto("Data").getRootHisto().Clone("BaseLine/MTBaselineTauIdAllCutsTailKiller")
    #hmtBaseline = mtBaseline.histoMgr.getHisto("Data").getRootHisto().Clone("MTBaselineTauIdJetPhi") 
   
    mtEWKBaseline.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mtEWKBaseline._setLegendStyles()
    mtEWKBaseline._setLegendLabels()
    mtEWKBaseline.histoMgr.setHistoDrawStyleAll("P")
    mtEWKBaseline.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))  
#    hmtEWK = mtEWK.histoMgr.getHisto("EWK").getRootHisto().Clone("Inverted/MTInvertedAllCutsTailKiller")
    hmtEWK = mtEWKBaseline.histoMgr.getHisto("EWK").getRootHisto().Clone("BaseLine/MTBaselineTauIdAllCutsTailKiller")
    
    hmtBaseline_QCD = hmtBaseline.Clone("QCD")
    hmtBaseline_QCD.Add(hmtEWK,-1)    

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
    
    hmt.GetYaxis().SetTitleOffset(1.5)
    hmt.GetXaxis().SetTitle("CircleCut_BackToBackJet1")
    hmt.GetYaxis().SetTitle("Events")
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
    
    hmt.GetYaxis().SetTitleOffset(1.5)
    hmt.GetXaxis().SetTitle("CircleCut_CollinearJet1")
    hmt.GetYaxis().SetTitle("Events")
    canvas391.Print("CircleCut_CollinearJet1.png")
    canvas391.Print("CircleCut_CollinearJet1.C")

    
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
    
    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       5.05 fb^{-1}       CMS Preliminary ")
#    tex4 = ROOT.TLatex(0.2,0.95,"8 TeV       12.2 fb^{-1}       CMS Preliminary ")    
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    hmtSumb.GetYaxis().SetTitleOffset(1.5)
    hmtSumb.GetXaxis().SetTitle("m_{T}(#tau jet, MET) (GeV/c^{2})")
    hmtSumb.GetYaxis().SetTitle("Events / 20 GeV/c^{2}")
    canvas72.Print("transverseMassAfterBtagging.png")
    canvas72.Print("transverseMassAfterBtagging.C")






########################################################3


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
    marker2 = ROOT.TMarker(0.4,0.755,bveto_nor.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(mtFactorised.GetMarkerColor())
    marker2.SetMarkerSize(0.9*mtFactorised.GetMarkerSize())
    marker2.Draw()
    tex5 = ROOT.TLatex(0.45,0.65,"No factorization")
    tex5.SetNDC()
    tex5.SetTextSize(20)
    tex5.Draw() 
    marker5 = ROOT.TMarker(0.4,0.655,btagged_nor.GetMarkerStyle())
    marker5.SetNDC()
    marker5.SetMarkerColor(btagged_nor.GetMarkerColor())
    marker5.SetMarkerSize(0.9*btagged_nor.GetMarkerSize())
    marker5.Draw()    
    
#    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       5.05 fb^{-1}       CMS Preliminary ")
    tex4 = ROOT.TLatex(0.2,0.95,"8 TeV       12.2 fb^{-1}       CMS Preliminary ")    
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    bveto_nor.GetYaxis().SetTitleOffset(1.5)
    bveto_nor.GetXaxis().SetTitle("m_{T}(#tau jet, MET) (GeV/c^{2})")
    bveto_nor.GetYaxis().SetTitle("Events / 10 GeV/c^{2}")
    canvas725.Print("transverseMassClosureBvetoVsBtagInverted.png")
    canvas725.Print("transverseMassClosureBvetoVsBtagInverted.C")

    
####################################################
# mt factorised

    canvas720 = ROOT.TCanvas("canvas720","",500,500)    
    mtFactorised.SetMarkerColor(4)
    mtFactorised.SetMarkerSize(1)
    mtFactorised.SetMarkerStyle(20)
    mtFactorised.SetFillColor(4)
    mtFactorised.Draw("EP")
    
 
    
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
############


    canvas421 = ROOT.TCanvas("canvas421","",500,500)    
#    hClosureBveto.SetMaximum(500)
    hClosureBveto.SetMinimum(-5)
    
    hClosureBveto.SetMarkerColor(4)
    hClosureBveto.SetMarkerSize(1)
    hClosureBveto.SetMarkerStyle(20)
    hClosureBveto.SetFillColor(4)
    hClosureBveto.Draw("EP")
    

    hClosureBaselineBveto_QCD.SetMarkerColor(2)
    hClosureBaselineBveto_QCD.SetMarkerSize(1)
    hClosureBaselineBveto_QCD.SetMarkerStyle(21)
    hClosureBaselineBveto_QCD.Draw("same")            

             
    tex2 = ROOT.TLatex(0.55,0.85,"Inverted #tau isolation")
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw()    
    marker2 = ROOT.TMarker(0.5,0.865,hClosureBveto.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(hClosureBveto.GetMarkerColor())
    marker2.SetMarkerSize(0.9*hClosureBveto.GetMarkerSize())
    marker2.Draw()
    tex9 = ROOT.TLatex(0.55,0.78,"Baseline: Data-EWK") 
    tex9.SetNDC()
    tex9.SetTextSize(20)
    tex9.Draw()
    marker9 = ROOT.TMarker(0.5,0.795,hClosureBaselineBveto_QCD.GetMarkerStyle())
    marker9.SetNDC()
    marker9.SetMarkerColor(hClosureBaselineBveto_QCD.GetMarkerColor())
    marker9.SetMarkerSize(0.9*hClosureBaselineBveto_QCD.GetMarkerSize())
    marker9.Draw()
    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       5.05 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    hClosureBaselineBveto.GetYaxis().SetTitleOffset(1.5)
    hClosureBaselineBveto.GetXaxis().SetTitle("m_{T}(#tau jet, MET) (GeV/c^{2})")
    hClosureBaselineBveto.GetYaxis().SetTitle("Events / 10 GeV/c^{2}")
    canvas421.Print("transverseMassClosureBveto.png")
    canvas421.Print("transverseMassClosureBveto.C")
############

    if False:
        canvas42   = ROOT.TCanvas("canvas42","",500,500)    
#    hClosureBve toTailKiller.SetMaximum(200)
        hClosureBvetoTailKiller.SetMinimum(-5)
    
        hClosureBvetoTailKiller.SetMarkerColor(4)
        hClosureBvetoTailKiller.SetMarkerSize(1)
        hClosureBvetoTailKiller.SetMarkerStyle(20)
        hClosureBvetoTailKiller.SetFillColor(4)
        hClosureBvetoTailKiller.Draw("EP")
        
        
        hClosureBaselineBvetoTailKiller_QCD.SetMarkerColor(2)
        hClosureBaselineBvetoTailKiller_QCD.SetMarkerSize(1)
        hClosureBaselineBvetoTailKiller_QCD.SetMarkerStyle(21)
        hClosureBaselineBvetoTailKiller_QCD.Draw("same")          
        
        
        tex2 = ROOT.TLatex(0.55,0.85,"Inverted #tau isolation")
        tex2.SetNDC()
        tex2.SetTextSize(20)
        tex2.Draw()    
        marker2 = ROOT.TMarker(0.5,0.865,hClosureBvetoTailKiller.GetMarkerStyle())
        marker2.SetNDC()
        marker2.SetMarkerColor(hClosureBvetoTailKiller.GetMarkerColor())
        marker2.SetMarkerSize(0.9*hClosureBvetoTailKiller.GetMarkerSize())
        marker2.Draw()
        tex9 = ROOT.TLatex(0.55,0.78,"Baseline: Data-EWK") 
        tex9.SetNDC()
        tex9.SetTextSize(20)
        tex9.Draw()
        marker9 = ROOT.TMarker(0.5,0.795,hClosureBaselineBvetoTailKiller_QCD.GetMarkerStyle())
        marker9.SetNDC()
        marker9.SetMarkerColor(hClosureBaselineBvetoTailKiller_QCD.GetMarkerColor())
        marker9.SetMarkerSize(0.9*hClosureBaselineBvetoTailKiller_QCD.GetMarkerSize())
        marker9.Draw()
        
        tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       5.05 fb^{-1}       CMS Preliminary ")
        tex4.SetNDC()
        tex4.SetTextSize(20)
        tex4.Draw()
        
        hClosureBvetoTailKiller.GetYaxis().SetTitleOffset(1.5)
        hClosureBvetoTailKiller.GetXaxis().SetTitle("m_{T}(#tau jet, MET) (GeV/c^{2})")
        hClosureBvetoTailKiller.GetYaxis().SetTitle("Events / 10 GeV/c^{2}")
        canvas42.Print("transverseMassClosureBvetoTailKiller.png")
        canvas42.Print("transverseMassClosureBvetoTailKiller.C")
        
    
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
        
    if False:
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
    if False:    
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


        


        
######## deltaPhi(jet,Met) vs deltaPhi(tau,Met) after 2dim cut
    if False:        
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
    


  
######## deltaPhi(jet4,Met) vs deltaPhi(tau,MET) after 2dim cut
    if False:
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
    bhmtBaseline.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))  
    hbhmtBaseline = bhmtBaseline.histoMgr.getHisto("Data").getRootHisto().Clone("BaseLine/NBBaselineTauIdJet")
    
    bhmtEWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    bhmtEWK._setLegendStyles()
    bhmtEWK._setLegendLabels()
    bhmtEWK.histoMgr.setHistoDrawStyleAll("P")
    bhmtEWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))  
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
    hjBaseline = jBaseline.histoMgr.getHisto("Data").getRootHisto().Clone("BaseLine/NJetBaselineTauIdJet")
    
    jEWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    jEWK._setLegendStyles()
    jEWK._setLegendLabels()
    jEWK.histoMgr.setHistoDrawStyleAll("P")
    jEWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))  
    hjEWK =  jEWK.histoMgr.getHisto("EWK").getRootHisto().Clone("BaseLine/NJetBaselineTauIdJet")

    Njets_QCD = hjBaseline.Clone("QCD")
    Njets_QCD.Add(hjEWK,-1)


          
# Njets
    njet_inverted = Njets.Clone("jet")
    njet_baseline = Njets_QCD.Clone("Baseline_QCD")
    invertedQCD.setLabel("NjetInvertedVsBaseline")
    invertedQCD.mtComparison(njet_inverted, njet_baseline,"NjetInvertedVsBaseline")
    
       
    canvas34 = ROOT.TCanvas("canvas34","",500,500)
    canvas34.SetLogy()
    frame34 = histograms._drawFrame(canvas33, xmin=0, xmax=10, ymin=1, ymax=1e5)
    frame34.Draw()
               
    Njets.SetMarkerColor(4)
    Njets.SetMarkerSize(1)
    Njets.SetMarkerStyle(20)
    Njets.SetFillColor(4)
    Njets.Draw("EP same")


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
    h.addStandardTexts(addLuminosityText=addLuminosityText)
    if textFunction != None:
        textFunction()
    h.save()

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
    
def transverseMass2(h, name, **kwargs):
    xlabel = "m_{T}(#tau jet, E_{T}^{miss}) (GeV/c^{2})" 
    ylabel = "Events / %.0f GeV/c^{2}"

    drawPlot(h, name, xlabel, ylabel=ylabel, **kwargs)
       


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
