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


#dataEra = "Run2012C"
#
#dataEra = "Run2012D"
#dataEra = "Run2012AB"

#dataEra = "Run2012AB"
dataEra = "Run2012ABCD"

#dataEra = "Run2011AB"


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

        #datasetsQCD = dataset.getDatasetsFromMulticrabCfg(cfgfile="/home/rkinnune/signalAnalysis/CMSSW_4_2_8_patch2/src/HiggsAnalysis/HeavyChHiggsToTauNu/test/multicrab_111123_132128/multicrab.cfg", counters=counters)
        datasetsQCD = dataset.getDatasetsFromMulticrabCfg(cfgfile="/afs/cern.ch/work/e/epekkari/DataDrivenFakeTaus/CMSSW_5_3_9_patch3/src/HiggsAnalysis/HeavyChHiggsToTauNu/test/multicrab_140526_122821/multicrab.cfg")
        datasetsQCD.loadLuminosities()
        print "QCDfromData", QCDfromData
        datasetsQCD.mergeData()
        datasetsQCD.remove(datasetsQCD.getMCDatasetNames())
        datasetsQCD.rename("Data", "QCD")
    

    #for d in datasets.getAllDatasets():
    #    print d.getName()
    #print "-------"            
    #plots.mergeRenameReorderForDataMC(datasets)

#    print "Int.Lumi",datasets.getDataset("Data").getLuminosity()

    # Remove signals other than M120
    datasets.remove(filter(lambda name: "TTToHplus" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "HplusTB" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "Hplus_taunu_t-channel" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "Hplus_taunu_tW-channel" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "TTJets_SemiLept" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "TTJets_FullLept" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "TTJets_Hadronic" in name, datasets.getAllDatasetNames()))

    plots.mergeRenameReorderForDataMC(datasets)
    
    datasets.merge("EWK", ["WJets", "DYJetsToLL", "SingleTop", "Diboson", "TTJets"], keepSources=True)
    datasets.remove(filter(lambda name: "W2Jets" in name, datasets.getAllDatasetNames()))        
    datasets.remove(filter(lambda name: "W3Jets" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "W4Jets" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "Hplus_taunu_s-channel" in name, datasets.getAllDatasetNames()))
    # Remove QCD
    #datasets.remove(filter(lambda name: "QCD" in name, datasets.getAllDatasetNames()))

    
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
 
    #controlPlots(datasets)

    datasetsQCD = dataset.getDatasetsFromMulticrabCfg(cfgfile="/afs/cern.ch/work/e/epekkari/DataDrivenFakeTaus/CMSSW_5_3_9_patch3/src/HiggsAnalysis/HeavyChHiggsToTauNu/test/multicrab_140526_122821/multicrab.cfg")
    datasetsQCD.loadLuminosities()
    print "QCDfromData", QCDfromData
    datasetsQCD.mergeData()
    datasetsQCD.remove(datasetsQCD.getMCDatasetNames())
    datasetsQCD.rename("Data", "QCD")
        
    if True:
        #transversemass
        transverseMass2(createPlot("baseline/MTBaselineTauIdAfterBackToBackCuts/MTBaselineTauIdAfterBackToBackCutsInclusive"), "transverseMass", rebin=5, ratio=False,log=False, opts={"xmax": 400,"ymaxfactor": 1.1}, textFunction=lambda: addMassBRText(x=0.35, y=0.87))
        transverseMass2(createPlot("baseline/MTBaselineTauIdAfterMetPlusSoftBtaggingPlusBackToBackCuts/MTBaselineTauIdAfterMetPlusSoftBtaggingPlusBackToBackCutsInclusive"), "transverseMassSoftBtagging", rebin=5, ratio=False,log=False, opts={"xmax": 400,"ymaxfactor": 1.1}, textFunction=lambda: addMassBRText(x=0.35, y=0.87))
        
        drawPlot(createPlot("baseline/INVMASSBaselineTauIdAfterCollinearCutsPlusBackToBackCuts/INVMASSBaselineTauIdAfterCollinearCutsPlusBackToBackCutsInclusive"), "InvariantMass", rebin=2, log=False,  xlabel="m_{H^{/pm}} )GerV)", ylabel="Events", ratio=True, opts={ "xmax": 400}, textFunction=lambda: addMassBRText(x=0.4, y=0.87))

        #!!!
        #drawPlot(replaceQCDfromData(createPlot("baseline/METBaselineTauIdAfterJets/METBaselineTauIdAfterJetsInclusive"), datasetsQCD, "baseline/METBaselineTauIdAfterJets/METBaselineTauIdAfterJetsInclusive"), "METBaseLineTauIdAfterJets", xlabel="MET (GeV)",  rebin=10, log=True, ylabel="Events", ratio=True, opts={ "xmax": 400}, textFunction=lambda: addMassBRText(x=0.4, y=0.87))

        drawPlot(createPlot("baseline/METBaselineTauIdAfterJets/METBaselineTauIdAfterJetsInclusive"), "METBaseLineTauIdAfterJets", xlabel="MET (GeV)",  rebin=10, log=True, ylabel="Events", ratio=True, opts={ "xmax": 400}, textFunction=lambda: addMassBRText(x=0.4, y=0.87))
        
        drawPlot(createPlot("baseline/METBaselineTauIdAfterCollinearCuts/METBaselineTauIdAfterCollinearCutsInclusive"), "METBaseLineTauIdAfterCollinearCuts", xlabel="MET (GeV)",  rebin=10, log=True,  ylabel="Events", ratio=True, opts={ "xmax": 400}, textFunction=lambda: addMassBRText(x=0.4, y=0.87))                 
        drawPlot(createPlot("baseline/METBaselineTauIdAfterCollinearCutsPlusBveto/METBaselineTauIdAfterCollinearCutsPlusBvetoInclusive"), "METBaseLineTauIdAfterCollinearCutsBveto", xlabel="MET (GeV)",  rebin=10, log=True,  ylabel="Events", ratio=True, opts={"xmax": 400}, textFunction=lambda: addMassBRText(x=0.4, y=0.87))
                 
        drawPlot(createPlot("Inverted/METInvertedTauIdAfterJets/METInvertedTauIdAfterJetsInclusive"), "METInvertedTauIdAfterJets", xlabel="MET (GeV)",  rebin=10, log=True,  ylabel="Events", ratio=True, opts={ "xmax": 400}, textFunction=lambda: addMassBRText(x=0.4, y=0.87))
                 
        drawPlot(createPlot("Inverted/METInvertedTauIdAfterCollinearCuts/METInvertedTauIdAfterCollinearCutsInclusive"), "METInvertedTauIdAfterCollinearCuts", xlabel="MET (GeV)",  rebin=10, log=True,  ylabel="Events", ratio=True, opts={ "xmax": 400}, textFunction=lambda: addMassBRText(x=0.4, y=0.87))
                 
        drawPlot(createPlot("Inverted/METInvertedTauIdAfterCollinearCutsPlusBveto/METInvertedTauIdAfterCollinearCutsPlusBvetoInclusive"), "METInvertedTauIdAfterCollinearCutsBveto", xlabel="MET (GeV)",  rebin=10, log=True,  ylabel="Events", ratio=True, opts={"xmax": 400}, textFunction=lambda: addMassBRText(x=0.4, y=0.87))
                 

    '''
    drawPlot(createPlot("BaseLine/QCDTailKillerJet0BackToBackBaseline"), "QCDTailKillerJet0BackToBackBaseline",  rebin=5,log=False,  xlabel="#sqrt{(180^{o}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{1},MET)^{2}}(^{o})", ylabel="Events", ratio=False, opts={"ymin": 0, "xmax": 260}, textFunction=lambda: addMassBRText(x=0.2, y=0.5), moveLegend={"dx": -0.5,"dy": 0.02})
    drawPlot(createPlot("BaseLine/QCDTailKillerJet1BackToBackBaseline"), "QCDTailKillerJet1BackToBackBaseline",  rebin=5,log=False,  xlabel="#sqrt{(180^{o}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{2},MET)^{2}}(^{o})", ylabel="Events", ratio=False, opts={"ymin": 0, "xmax": 260}, textFunction=lambda: addMassBRText(x=0.4, y=0.87))
    drawPlot(createPlot("BaseLine/QCDTailKillerJet2BackToBackBaseline"), "QCDTailKillerJet2BackToBackBaseline",  rebin=5, log=False,  xlabel="#sqrt{(180^{o}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{3},MET)^{2}} (^{o})", ylabel="Events", ratio=False, opts={"ymin": 0, "xmax": 260}, textFunction=lambda: addMassBRText(x=0.4, y=0.87))
    drawPlot(createPlot("BaseLine/QCDTailKillerJet0CollinearBaseline"), "CDTailKillerJet0CollinearBaseline",  rebin=5,log=False,  xlabel="#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{o}-#Delta#phi(jet_{1},MET))^{1}}(^{o})", ylabel="Events", ratio=False, opts={"ymin": 0, "xmax": 260}, textFunction=lambda: addMassBRText(x=0.4, y=0.87))
    drawPlot(createPlot("BaseLine/QCDTailKillerJet1CollinearBaseline"), "CDTailKillerJet1CollinearBaseline",  rebin=5,log=False,  xlabel="#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{o}-#Delta#phi(jet_{2},MET))^{2}}(^{o})", ylabel="Events", ratio=False, opts={"ymin": 0, "xmax": 260}, textFunction=lambda: addMassBRText(x=0.4, y=0.87))
    drawPlot(createPlot("BaseLine/QCDTailKillerJet2CollinearBaseline"), "CDTailKillerJet2CollinearBaseline",  rebin=5,log=False,  xlabel="#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{o}-#Delta#phi(jet_{2},MET))^{3}}(^{o})", ylabel="Events", ratio=False, opts={"ymin": 0, "xmax": 260}, textFunction=lambda: addMassBRText(x=0.4, y=0.87), moveLegend={"dx": -0.5,"dy": 0.02})
    '''

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


ptbins = ["0","1","2","3","4","5","6","7"]
#ptbins = ["1","2","3","4","5","6","7","8","9","10"]    
#ptbins = ['taup_Tlt50', 'taup_Teq50to60', 'taup_Teq60to70', 'taup_Teq70to80', 'taup_Teq80to100', 'taup_Teq100to120', 'taup_Teq120to150', 'taup_Tgt150', 'Inclusive']


def normalisation():

    normData = {}
    normEWK = {}


 
    print "-------------------"
#    norm_inc = QCDInvertedNormalization["inclusive"]
#    normEWK_inc = QCDInvertedNormalization["inclusiveEWK"]    

    for bin in ptbins:
        print QCDInvertedNormalization[bin]
        normData[bin] = QCDInvertedNormalization[bin]
        normEWK[bin] = QCDInvertedNormalization[bin+"EWK"]

    #print "inclusive norm", norm_inc,normEWK_inc
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
    #norm_inc,normEWK_inc = normalisationInclusive()


    mtAllCuts = []
    mtAllCutsBaseline = []
    mtAfterMetCut = []
    mtAfterMetCutBaseline = []
    mtAfterMetPlusSoftBtagging = []
    mtAfterMetPlusSoftBtaggingBaseline = []
    mtAfterMetPlusBveto = []
    mtAfterMetPlusBvetoBaseline = []
    mtAfterCollinearCuts = []
    mtAfterCollinearCutsBaseline = []
    invertedNoScale = []
  
    
## histograms in bins, normalisation and substraction of EWK contribution
    ## mt with 2dim deltaPhi cut
    for ptbin in ptbins:
        ## -------------   mt with all cuts -----------
    
        mt_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MTInvertedTauIdAfterBackToBackCuts/MTInvertedTauIdAfterBackToBackCuts"+ptbin)])
        mt_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))
        mt = mt_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        mtEvents = mt_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        invertedNoScale.append(mtEvents)
        mt.Scale(normData[ptbin])
    
        
        mtEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MTInvertedTauIdAfterBackToBackCuts/MTInvertedTauIdAfterBackToBackCuts"+ptbin)])
        mtEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mtEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))
        mtEWK = mtEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        mtEWK.Scale(normEWK[ptbin])
        if includeEWKscale:
            mtEWK.Scale(EWKscale)
        mt.Add(mtEWK, -1)
        mtAllCuts.append(mt)
        
        ## baseline
        mt_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("baseline/MTBaselineTauIdAfterBackToBackCuts/MTBaselineTauIdAfterBackToBackCuts"+ptbin)])
        mt_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))
        mtBaseline = mt_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
           
        mtEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("baseline/MTBaselineTauIdAfterBackToBackCuts/MTBaselineTauIdAfterBackToBackCuts"+ptbin)])
        mtEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mtEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))
        mtEWKBaseline = mtEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        mtBaseline.Add(mtEWKBaseline, -1)
        mtAllCutsBaseline.append(mtBaseline)


#################################################
        
        ### ---- mt after met cut
        mtfac_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MTInvertedTauIdAfterMetPlusBackToBackCuts/MTInvertedTauIdAfterMetPlusBackToBackCuts"+ptbin)])
        mtfac_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))
        mtfac = mtfac_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        mtNoBtaggingTailKiller = mtfac_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        mtNoBtaggingTailKiller.Scale(normData[ptbin])
              
        mtfacEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MTInvertedTauIdAfterMetPlusBackToBackCuts/MTInvertedTauIdAfterMetPlusBackToBackCuts"+ptbin)])
        mtfacEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mtfacEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))
        mtNoBtaggingTailKillerEWK = mtfacEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()        
        mtNoBtaggingTailKillerEWK.Scale(normEWK[ptbin])       
        mtNoBtaggingTailKiller.Add(mtNoBtaggingTailKillerEWK, -1)
        mtAfterMetCut.append(mtNoBtaggingTailKiller)
        
        ### ---- mt after met cut baseline
        mtfac_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("baseline/MTBaselineTauIdAfterMetPlusBackToBackCuts/MTBaselineTauIdAfterMetPlusBackToBackCuts"+ptbin)])
        mtfac_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))
        mtfac = mtfac_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        mtNoBtaggingTailKillerBaseline = mtfac_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
              
        mtfacEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("baseline/MTBaselineTauIdAfterMetPlusBackToBackCuts/MTBaselineTauIdAfterMetPlusBackToBackCuts"+ptbin)])
        mtfacEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mtfacEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))
        mtNoBtaggingTailKillerEWK = mtfacEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()             
        mtNoBtaggingTailKillerBaseline.Add(mtNoBtaggingTailKillerEWK, -1)
        mtAfterMetCutBaseline.append(mtNoBtaggingTailKillerBaseline)

 ########################################################       
        
        # ----------mt after SOFT b tagging ---------------
        mtbSoft_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MTInvertedTauIdAfterMetPlusSoftBtaggingPlusBackToBackCuts/MTInvertedTauIdAfterMetPlusSoftBtaggingPlusBackToBackCuts"+ptbin)])
        mtbSoft_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))
        mtbSoft = mtbSoft_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        mtbSoft.Scale(normData[ptbin])
       
        mtbSoftEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MTInvertedTauIdAfterMetPlusSoftBtaggingPlusBackToBackCuts/MTInvertedTauIdAfterMetPlusSoftBtaggingPlusBackToBackCuts"+ptbin)])
        mtbSoftEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mtbSoftEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))
        mtbSoftEWK = mtbSoftEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        mtbSoftEWK.Scale(normEWK[ptbin])
        mtbSoft.Add(mtbSoftEWK, -1)
        mtAfterMetPlusSoftBtagging.append(mtbSoft)
       
        # ----------mt after SOFT b tagging baseline ---------------
        mtbSoft_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("baseline/MTBaselineTauIdAfterMetPlusSoftBtaggingPlusBackToBackCuts/MTBaselineTauIdAfterMetPlusSoftBtaggingPlusBackToBackCuts"+ptbin)])
        mtbSoft_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))
        mtbSoftBaseline = mtbSoft_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
       
        mtbSoftEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("baseline/MTBaselineTauIdAfterMetPlusSoftBtaggingPlusBackToBackCuts/MTBaselineTauIdAfterMetPlusSoftBtaggingPlusBackToBackCuts"+ptbin)])
        mtbSoftEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mtbSoftEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))
        mtbSoftEWKBaseline = mtbSoftEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        mtbSoftBaseline.Add(mtbSoftEWKBaseline, -1)
        mtAfterMetPlusSoftBtaggingBaseline.append(mtbSoftBaseline)
       

 ########################################################  

# mt after met cut and b-jet veto

        mtPhiv_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MTInvertedTauIdAfterMetPlusBvetoPlusBackToBackCuts/MTInvertedTauIdAfterMetPlusBvetoPlusBackToBackCuts"+ptbin)])
        mtPhiv_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))
        mtPhiv = mtPhiv_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        mtPhiv.Scale(normData[ptbin])
       
        mtPhiEWKv_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MTInvertedTauIdAfterMetPlusBvetoPlusBackToBackCuts/MTInvertedTauIdAfterMetPlusBvetoPlusBackToBackCuts"+ptbin)])
        mtPhiEWKv_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mtPhiEWKv_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))
        mtPhiEWKv = mtPhiEWKv_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        mtPhiEWKv.Scale(normEWK[ptbin])
        mtPhiv.Add(mtPhiEWKv, -1)
        mtAfterMetPlusBveto.append(mtPhiv)

        mtPhiv_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("baseline/MTBaselineTauIdAfterMetPlusBvetoPlusBackToBackCuts/MTBaselineTauIdAfterMetPlusBvetoPlusBackToBackCuts"+ptbin)])
        mtPhiv_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))
        mtPhivBaseline = mtPhiv_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
       
        mtPhiEWKv_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("baseline/MTBaselineTauIdAfterMetPlusBvetoPlusBackToBackCuts/MTBaselineTauIdAfterMetPlusBvetoPlusBackToBackCuts"+ptbin)])
        mtPhiEWKv_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mtPhiEWKv_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))
        mtPhiEWKvBaseline = mtPhiEWKv_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        mtPhivBaseline.Add(mtPhiEWKvBaseline, -1)
        mtAfterMetPlusBvetoBaseline.append(mtPhivBaseline)
        
############################################################

        

# mt after jet selection and back-to-back cuts 
        mtj_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MTInvertedTauIdAfterCollinearCutsPlusBackToBackCuts/MTInvertedTauIdAfterCollinearCutsPlusBackToBackCuts"+ptbin)])
        mtj_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))
        mtj = mtj_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        mtj.Scale(normData[ptbin])
        
        mtjEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("Inverted/MTInvertedTauIdAfterCollinearCutsPlusBackToBackCuts/MTInvertedTauIdAfterCollinearCutsPlusBackToBackCuts"+ptbin)])
        mtjEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mtjEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))
        mtjEWK = mtjEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        mtjEWK.Scale(normEWK[ptbin])
        mtj.Add(mtjEWK, -1)
        mtAfterCollinearCuts.append(mtj)
        
# mt after jet selection and back-to-back cuts baseline
        mtj_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("baseline/MTBaselineTauIdAfterCollinearCutsPlusBackToBackCuts/MTBaselineTauIdAfterCollinearCutsPlusBackToBackCuts"+ptbin)])
        mtj_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))
        mtjBaseline = mtj_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
        
        mtjEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("baseline/MTBaselineTauIdAfterCollinearCutsPlusBackToBackCuts/MTBaselineTauIdAfterCollinearCutsPlusBackToBackCuts"+ptbin)])
        mtjEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        mtjEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))
        mtjEWKBaseline = mtjEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        mtjBaseline.Add(mtjEWKBaseline, -1)
        mtAfterCollinearCutsBaseline.append(mtjBaseline)
        

############################################################
 
## end of loop
        
### sum and plot        

    invertedQCD = InvertedTauID()
    invertedQCD.setLumi(datasets.getDataset("Data").getLuminosity())
      

    events = invertedNoScale[0].Clone("inv")
    events.SetName("inv")
    events.SetTitle("Inverted tau ID")
    events.Reset()
    print "check events in inverted ",events.GetEntries()
    for histo in invertedNoScale:
        events.Add(histo)  
    print "All unormalised events - EWK = ",events.Integral()
    
 ## mt with all cuts
    hAllCuts = mtAllCuts[0].Clone("mtSum")
    hAllCuts.SetName("transverseMass")
    hAllCuts.SetTitle("Inverted tau ID")
    hAllCuts.Reset()
    for histo in mtAllCuts:
        hAllCuts.Add(histo)  
    print "All events with all cuts - EWK evets= ",hAllCuts.Integral()
    
    hAllCutsBaseline = mtAllCutsBaseline[0].Clone("mtSumBaseline")
    hAllCutsBaseline.SetName("transverseMass")
    hAllCutsBaseline.SetTitle("Inverted tau ID")
    hAllCutsBaseline.Reset()
    for histo in mtAllCutsBaseline:
        hAllCutsBaseline.Add(histo)  
    print "Baseline QCD events with all cuts = ",hAllCutsBaseline.Integral()
 
#    mtvEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("BaseLine/MTBaseLineTauIdBveto")])            
#    mt = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("Inverted/MTInvertedAllCutsTailKiller")]) 
#    mtBaseline = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("BaseLine/MTBaseLineTauIdAllCutsTailKiller")])   


    '''
 ##  mT baseline with TailKiller cut
    mtBaseline = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto("BaseLine/MTBaseLineTauIdAllCutsTailKiller")])            
    mtBaseline._setLegendStyles()
    mtBaseline._setLegendLabels()
    mtBaseline.histoMgr.setHistoDrawStyleAll("P")
    mtBaseline.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))  
    hmtBaseline = mtBaseline.histoMgr.getHisto("Data").getRootHisto().Clone("BaseLine/MTBaselineTauIdAllCutsTailKiller")

    mtEWKBaseline = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto("BaseLine/MTBaseLineTauIdAllCutsTailKiller")])   
    mtEWKBaseline.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mtEWKBaseline._setLegendStyles()
    mtEWKBaseline._setLegendLabels()
    mtEWKBaseline.histoMgr.setHistoDrawStyleAll("P")
    mtEWKBaseline.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))  
    hmtEWK = mtEWKBaseline.histoMgr.getHisto("EWK").getRootHisto().Clone("BaseLine/MTBaselineTauIdAllCutsTailKiller")
    
    hmtBaseline_QCD = hmtBaseline.Clone("QCD")
    hmtBaseline_QCD.Add(hmtEWK,-1)   

    
#    invertedQCD.mtComparison(bveto_inverted, bveto_baseline,"BvetoTailKillerClosure")
    '''    
    
# mt plot with all cuts
    allCuts_inverted = hAllCuts.Clone("AllCuts")
    allCuts_baseline = hAllCutsBaseline.Clone("allcuts_QCD")
    invertedQCD.setLabel("AllCuts")
    invertedQCD.mtComparison(allCuts_inverted, allCuts_baseline,"AllCuts")

    '''    
# mt inverted-baseline comparison normal btagging and tailkiller cuts
    allCuts_inverted = hmtSum.Clone("mtSum")
    allCuts_baseline = hmtBaseline_QCD.Clone("hmBaseline_QCD")
    print "normal b tagging inverted ",allCuts_inverted.GetEntries()
    print "normal b tagging baseline ",allCuts_baseline.GetEntries()
    invertedQCD.setLabel("MtAllCutsClosure")
    invertedQCD.mtComparison(allCuts_inverted, allCuts_baseline,"MtAllCutsClosure")
    '''
    '''    
# mt plot with TailKiller 
    allCuts_inverted = hmtSum.Clone("mtSum")
    invertedQCD.setLabel("MtWithAllCutsTailKiller")
    invertedQCD.mtComparison(allCuts_inverted, allCuts_inverted,"MtWithAllCutsTailKiller")

   
# mt plot inverted all cuts  
    invertedQCD.setLabel("MtWithAllCutsTailKiller")
    invertedQCD.mtComparison(allCuts_inverted, allCuts_inverted,"MtWithAllCutsTailKiller")
    '''     
########################################################

    
# mt with SOFT btagging

    hmtAfterMetPlusSoftBtagging = mtAfterMetPlusSoftBtagging[0].Clone("mthmtbSoft")
    hmtAfterMetPlusSoftBtagging.SetName("transverseMassBtag")
    hmtAfterMetPlusSoftBtagging.SetTitle("Inverted tau ID")
    hmtAfterMetPlusSoftBtagging.Reset()
#    print "check hmtsum",hmtSum.GetEntries()
    for histo in mtAfterMetPlusSoftBtagging:
        hmtAfterMetPlusSoftBtagging.Add(histo)  
    print "Integral: after SOFT B tagging - EWK = ",hmtAfterMetPlusSoftBtagging.Integral()
# mt with SOFT btagging baseline
    hmtAfterMetPlusSoftBtaggingBaseline = mtAfterMetPlusSoftBtaggingBaseline[0].Clone("mthmtbSoft")
    hmtAfterMetPlusSoftBtaggingBaseline.SetName("transverseMassBtag")
    hmtAfterMetPlusSoftBtaggingBaseline.SetTitle("Inverted tau ID")
    hmtAfterMetPlusSoftBtaggingBaseline.Reset()
#    print "check hmtsum",hmtSum.GetEntries()
    for histo in mtAfterMetPlusSoftBtaggingBaseline:
        hmtAfterMetPlusSoftBtaggingBaseline.Add(histo)  
    print "Integral Baseline: after SOFT B tagging - EWK = ",hmtAfterMetPlusSoftBtaggingBaseline.Integral()

 
# mt inverted-baseline comparison, SOFT b tagging, MET CUT 
    afterJets_inverted = hmtAfterMetPlusSoftBtagging.Clone("mtbSoft")
    afterJets_baseline = hmtAfterMetPlusSoftBtaggingBaseline.Clone("mtbSoft_QCD")
    invertedQCD.setLabel("AfterMetPlusSoftBtagging")
    invertedQCD.mtComparison(afterJets_inverted,afterJets_baseline,"AfterMetPlusSoftBtagging")

################################




    hmtAfterCollinearCuts = mtAfterCollinearCuts[0].Clone("AfterCollinearCuts")
    hmtAfterCollinearCuts.SetName("transverseMassBtag")
    hmtAfterCollinearCuts.SetTitle("Inverted tau ID")
    hmtAfterCollinearCuts.Reset()
    for histo in mtAfterCollinearCuts:
        hmtAfterCollinearCuts.Add(histo)
    print "Integral: after collinear cuts - EWK = ",hmtAfterCollinearCuts.Integral()

    hmtAfterCollinearCutsBaseline = mtAfterCollinearCutsBaseline[0].Clone("AfterCollinearCutsBaseline")
    hmtAfterCollinearCutsBaseline.SetName("transverseMassBtag")
    hmtAfterCollinearCutsBaseline.SetTitle("Inverted tau ID")
    hmtAfterCollinearCutsBaseline.Reset()
    for histo in mtAfterCollinearCutsBaseline:
        hmtAfterCollinearCutsBaseline.Add(histo)
    print "Integral Baseline : after collinear cuts - EWK = ",hmtAfterCollinearCutsBaseline.Integral()
                                 

    # mt inverted-baseline comparison at coll cuts
    afterJets_inverted = hmtAfterCollinearCuts.Clone("AfterCollinearCuts")
    afterJets_baseline = hmtAfterCollinearCutsBaseline.Clone("AfterCollinearCutsBaseline_QCD")
    invertedQCD.setLabel("AfterCollinearCuts")
    invertedQCD.mtComparison(afterJets_inverted,afterJets_baseline,"AfterCollinearCuts")
         
                                  

######################################################

## B veto for closure test With Met cut   
    hmtAfterMetPlusBveto = mtAfterMetPlusBveto[0].Clone("hClosureBveto")
    hmtAfterMetPlusBveto.SetName("transverseMassBveto")
    hmtAfterMetPlusBveto.SetTitle("Inverted tau ID")
    hmtAfterMetPlusBveto.Reset()
    for histo in mtAfterMetPlusBveto:
        hmtAfterMetPlusBveto.Add(histo)  
    print "Integral: Bveto - EWK  with met cut = ",hmtAfterMetPlusBveto.Integral()

    hmtAfterMetPlusBvetoBaseline = mtAfterMetPlusBvetoBaseline[0].Clone("hClosureBvetoBaseline")
    hmtAfterMetPlusBvetoBaseline.SetName("transverseMassBveto")
    hmtAfterMetPlusBvetoBaseline.SetTitle("Inverted tau ID")
    hmtAfterMetPlusBvetoBaseline.Reset()
    for histo in mtAfterMetPlusBvetoBaseline:
        hmtAfterMetPlusBvetoBaseline.Add(histo)  
    print "Integral baseline: Bveto - EWK  with met cut = ",hmtAfterMetPlusBvetoBaseline.Integral()

# mt inverted-baseline comparison with bveto and MET CUT, closure
    #bveto_inverted =hClosureBvetoTailKiller.Clone("hmtvSum")
    bveto_inverted = hmtAfterMetPlusBveto.Clone("bveto")
    bveto_baseline = hmtAfterMetPlusBvetoBaseline.Clone("bvetoBaseline_QCD")
    invertedQCD.setLabel("AfterMetPlusBveto")
#    invertedQCD.mtComparison(bveto_inverted, bveto_baseline,"BvetoTailKillerClosure",sysError=sysError)
    invertedQCD.mtComparison(bveto_inverted, bveto_baseline,"AfterMetPlusBveto")
        




########################################################
    
## no btagging,   with Met cut 
    hmtAfterMetCut = mtAfterMetCut[0].Clone("hClosureNoBtag")
    hmtAfterMetCut.SetName("transverseMassNoBtagging")
    hmtAfterMetCut.SetTitle("Inverted tau ID")
    hmtAfterMetCut.Reset()
    for histo in mtAfterMetCut:
        hmtAfterMetCut.Add(histo)  
    print "Integral: no btagging - EWK  = ",hmtAfterMetCut.Integral()
    
    hmtAfterMetCutBaseline = mtAfterMetCutBaseline[0].Clone("hClosureNoBtag")
    hmtAfterMetCutBaseline.SetName("transverseMassNoBtagging")
    hmtAfterMetCutBaseline.SetTitle("Inverted tau ID")
    hmtAfterMetCutBaseline.Reset()
    for histo in mtAfterMetCutBaseline:
        hmtAfterMetCutBaseline.Add(histo)  
    print "Integral baseline: no btagging - EWK  = ",hmtAfterMetCutBaseline.Integral()

# mt inverted-baseline comparison, no b tagging, with met cut, closure
    afterMet_inverted = hmtAfterMetCut.Clone("afterMet")
    afterMet_baseline = hmtAfterMetCutBaseline.Clone("aftermet_QCD")
    invertedQCD.setLabel("AfterMetCut")
    invertedQCD.mtComparison(afterMet_inverted,afterMet_baseline,"AfterMetCut")
    

########################################################   

   




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
    #h.frame.GetXaxis().SetTitleSize()
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
