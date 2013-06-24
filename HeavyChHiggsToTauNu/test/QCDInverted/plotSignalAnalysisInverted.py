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
#optMode = "OptQCDTailKillerTightPlus"

optMode = ""


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
        mtNoBtaggingTailKillerEWK.Scale(normEWK[ptbin])       
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
 


# mt with SOFT btagging
    mtbSoft = hmtbSoft[0].Clone("mthmtbSoft")
    mtbSoft.SetName("transverseMassBtag")
    mtbSoft.SetTitle("Inverted tau ID")
    mtbSoft.Reset()
#    print "check hmtsum",hmtSum.GetEntries()
    for histo in hmtbSoft:
        mtbSoft.Add(histo)  
    print "Integral: after SOFT B tagging - EWK = ",mtbSoft.Integral()




## B veto for closure test With Met cut   
    hClosureBvetoMetCutTailKiller = hmtBvetoTailKiller[0].Clone("hClosureBveto")
    hClosureBvetoMetCutTailKiller.SetName("transverseMassBveto")
    hClosureBvetoMetCutTailKiller.SetTitle("Inverted tau ID")
    hClosureBvetoMetCutTailKiller.Reset()
#    print "check hmtsum B veto",hClosureBvetoMetCutTailKiller.GetEntries()
    for histo in hmtBvetoTailKiller:
        hClosureBvetoMetCutTailKiller.Add(histo)  
    print "Integral: Bveto - EWK  with met cut = ",hClosureBvetoMetCutTailKiller.Integral()




## no btagging,   with Met cut 
    hNoBtaggingTailKiller = NoBtaggingTailKiller[0].Clone("hClosureNoBtag")
    hNoBtaggingTailKiller.SetName("transverseMassNoBtagging")
    hNoBtaggingTailKiller.SetTitle("Inverted tau ID")
    hNoBtaggingTailKiller.Reset()
#    print "check hmtsum after jets",hClosureAfterJets.GetEntries()
    for histo in NoBtaggingTailKiller:
        hNoBtaggingTailKiller.Add(histo)  
    print "Integral: no btag - EWK  = ",hNoBtaggingTailKiller.Integral()

    

   

   
 
 ################## Control Plots and comparison with baseline(data-EWK) 

 ## mt baseline, plots and EWK substraction
            
    closureBaselineBvetoTailKiller = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("BaseLine/MTBaseLineTauIdBvetoTailKiller")])
    closureBaselineBvetoTailKillerEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("BaseLine/MTBaseLineTauIdBvetoTailKiller")])
    
    mtvEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("BaseLine/MTBaseLineTauIdBveto")])            
    mt = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MTInvertedAllCutsTailKiller")]) 
    mtBaseline = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("BaseLine/MTBaseLineTauIdAllCutsTailKiller")])   
    mtPhivEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("BaseLine/MTBaseLineTauIdBvetoTailKiller")])

  
## closure all selection cuts
    closureBaselineTailKiller = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("BaseLine/MTBaseLineTauIdAllCutsTailKiller")])  
    closureBaselineTailKiller.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    closureBaselineTailKiller._setLegendStyles()
    closureBaselineTailKiller._setLegendLabels()
    closureBaselineTailKiller.histoMgr.setHistoDrawStyleAll("P")
    closureBaselineTailKiller.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))  
    hClosureBaselineTailKiller = closureBaselineTailKiller.histoMgr.getHisto("Data").getRootHisto().Clone("BaseLine//MTBaseLineTauIdAllCutsTailKiller")

    closureBaselineTailKillerEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("BaseLine/MTBaseLineTauIdAllCutsTailKiller")])
    closureBaselineTailKillerEWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    closureBaselineTailKillerEWK._setLegendStyles()
    closureBaselineTailKillerEWK._setLegendLabels()
    closureBaselineTailKillerEWK.histoMgr.setHistoDrawStyleAll("P")
    closureBaselineTailKillerEWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))  
    hClosureBaselineTailKillerEWK = closureBaselineTailKillerEWK.histoMgr.getHisto("EWK").getRootHisto().Clone("BaseLine/MTBaseLineTauIdAllCutsTailKiller")    
    hClosureBaselineTailKiller_QCD = hClosureBaselineTailKiller.Clone("QCD")
    hClosureBaselineTailKiller_QCD.Add(hClosureBaselineTailKillerEWK,-1)

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

#######################################
## no b tagging  and MEt cut 
    closureBaselineNoBtaggingTailKiller = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("BaseLine/MTBaseLineTauIdNoBtaggingTailKiller")])
    closureBaselineNoBtaggingTailKiller._setLegendStyles()
    closureBaselineNoBtaggingTailKiller._setLegendLabels()
    closureBaselineNoBtaggingTailKiller.histoMgr.setHistoDrawStyleAll("P")
    closureBaselineNoBtaggingTailKiller.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))  
    hclosureBaselineNoBtaggingTailKiller = closureBaselineNoBtaggingTailKiller.histoMgr.getHisto("Data").getRootHisto().Clone("BaseLine/MTBaseLineTauIdNoBtaggingTailKiller")
    
    closureBaselineNoBtaggingTailKillerEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("BaseLine/MTBaseLineTauIdNoBtaggingTailKiller")])
    closureBaselineNoBtaggingTailKillerEWK.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    closureBaselineNoBtaggingTailKillerEWK._setLegendStyles()
    closureBaselineNoBtaggingTailKillerEWK._setLegendLabels()
    closureBaselineNoBtaggingTailKillerEWK.histoMgr.setHistoDrawStyleAll("P")
    closureBaselineNoBtaggingTailKillerEWK.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))  
    hclosureBaselineNoBtaggingTailKillerEWK = closureBaselineNoBtaggingTailKillerEWK.histoMgr.getHisto("EWK").getRootHisto().Clone("BaseLine/MTBaseLineTauIdNoBtaggingTailKiller")
    
    hClosureBaselineNoBtaggingTailKiller_QCD = hclosureBaselineNoBtaggingTailKiller.Clone("QCD")
    hClosureBaselineNoBtaggingTailKiller_QCD.Add(hclosureBaselineNoBtaggingTailKillerEWK,-1)

     
    invertedQCD = InvertedTauID()
    invertedQCD.setLumi(datasets.getDataset("Data").getLuminosity())
      
  

#####  -------------- Comparison plots --------------------
    




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
    





################################  
# mt inverted-baseline comparison, SOFT b tagging, MET CUT  and TK cuts, closure
    afterJets_inverted = mtbSoft.Clone("mtbSoft")
    afterJets_baseline = hClosureBaselineSoftBtaggingTK_QCD.Clone("mtbSoft_QCD")
    invertedQCD.setLabel("MtSoftBtaggingTKClosure")
    invertedQCD.mtComparison(afterJets_inverted,afterJets_baseline,"MtSoftBtaggingTKClosure")
##############################

    
# mt inverted-baseline comparison, no b tagging, with met cut, closure
    afterMet_inverted = hNoBtaggingTailKiller.Clone("afterMet")
    afterMet_baseline = hClosureBaselineNoBtaggingTailKiller_QCD.Clone("aftermet_QCD")
    invertedQCD.setLabel("NoBtaggingTailKillerClosure")
    invertedQCD.mtComparison(afterMet_inverted,afterMet_baseline,"NoBtaggingTailKillerClosure")

    


# mt plot with TailKiller 
    allCuts_inverted = hmtSum.Clone("mtSum")
    invertedQCD.setLabel("MtWithAllCutsTailKiller")
    invertedQCD.mtComparison(allCuts_inverted, allCuts_inverted,"MtWithAllCutsTailKiller")
    

# mt plot with TailKiller ans baseline 
    allCuts_inverted = hmtSum.Clone("mtSum")
    allCuts_baseline = hClosureBaselineTailKiller_QCD.Clone("allcuts_QCD")
    invertedQCD.setLabel("MtWithAllCutsTailKillerClosure")
    invertedQCD.mtComparison(allCuts_inverted, allCuts_baseline,"MtWithAllCutsTailKillerClosure")
    
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
