#!/usr/bin/env python

######################################################################
#
# This plot script is for comparing the use of the full
# mass of the charged Higgs boson to the use of the transverse mass
# in the signal analysis.
#
# ???The corresponding python job
# ???configuration is signalAnalysis_cfg.py with "doPat=1
# ???tauEmbeddingInput=1" command line arguments.
#
# Author: Stefan Richter
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
analysis = "signalAnalysisRun2011AB"
#analysis = "signalAnalysisInvertedTau"
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
deltaPhi160 = False
deltaPhi130 = False
topmass = False  ## with top mass cut

btagFactorisation = False  # works with deltaPhi180=True

# other distributions
deltaPhiDistribution = False
numberOfBjets = True
HiggsMass = True
HiggsMassPhi140 = True

lastPtBin150 = False
lastPtBin120 = True

mcOnly = False
#mcOnly = True
mcOnlyLumi = 5000 # pb #?

#dataEra = "Run2011A"
#dataEra = "Run2011B"
dataEra = "Run2011AB"


def usage():
    print "\n"
    print "### Usage:   plotSignalAnalysisFullMass.py <multicrab dir>\n"
    print "\n"
    sys.exit()

# main function
def main():

    if len(sys.argv) < 2:
        usage()

    dirs = []
    dirs.append(sys.argv[1])

    # Read the datasets
    datasets = dataset.getDatasetsFromMulticrabDirs(dirs,counters=counters, dataEra=dataEra, analysisBaseName="signalAnalysisFullMass")
    datasets.loadLuminosities()
    datasets.updateNAllEventsToPUWeighted()

    plots.mergeRenameReorderForDataMC(datasets)

    print "Int.Lumi",datasets.getDataset("Data").getLuminosity()

    # Remove signals other than M120
    datasets.remove(filter(lambda name: "TTToHplus" in name and not "M120" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "HplusTB" in name, datasets.getAllDatasetNames()))
    datasets.merge("EWK", ["WJets", "DYJetsToLL", "SingleTop", "Diboson","TTJets"], keepSources=True)
    datasets.remove(filter(lambda name: "W2Jets" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "W3Jets" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "W4Jets" in name, datasets.getAllDatasetNames()))
    
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

# Write histograms to file
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

   

   
 

####################
    datasets_tm = datasets
#    datasets_tm = datasets.deepCopy()
#    xsect.setHplusCrossSectionsToBR(datasets, br_tH=0.2, br_Htaunu=1)
#    xsect.setHplusCrossSectionsToBR(datasets_tm, br_tH=0.2, br_Htaunu=1)
#    datasets_tm.merge("TTToHplus_M120", ["TTToHplusBWB_M120", "TTToHplusBHminusB_M120"])


    transverseMass2(plots.DataMCPlot(datasets_tm, analysis+"/MTInvertedTauIdJet4050"), "MTInvertedTauIdJet4050", rebin=20)
    transverseMass2(plots.DataMCPlot(datasets_tm, analysis+"/MTInvertedTauIdJet5060"), "MTInvertedTauIdJet5060", rebin=20)
    transverseMass2(plots.DataMCPlot(datasets_tm, analysis+"/MTInvertedTauIdJet6070"), "MTInvertedTauIdJet6070", rebin=20)
    transverseMass2(plots.DataMCPlot(datasets_tm, analysis+"/MTInvertedTauIdJet7080"), "MTInvertedTauIdJet7080", rebin=20)
    transverseMass2(plots.DataMCPlot(datasets_tm, analysis+"/MTInvertedTauIdJet80100"), "MTInvertedTauIdJet80100", rebin=20)
    transverseMass2(plots.DataMCPlot(datasets_tm, analysis+"/MTInvertedTauIdJet100120"), "MTInvertedTauIdJet100120", rebin=20)
    if lastPtBin150: 
        transverseMass2(plots.DataMCPlot(datasets_tm, analysis+"/MTInvertedTauIdJet120150"), "MTInvertedTauIdJet120150", rebin=20)
        transverseMass2(plots.DataMCPlot(datasets_tm, analysis+"/MTInvertedTauIdJet150"), "MTInvertedTauIdJet150", rebin=20)
    if lastPtBin120: 
        transverseMass2(plots.DataMCPlot(datasets_tm, analysis+"/MTInvertedTauIdJet150"), "MTInvertedTauIdJet120", rebin=20)
                
    transverseMass2(plots.DataMCPlot(datasets_tm, analysis+"/MTInvertedTauIdJet"), "MTInvertedTauIdJet", rebin=20)
    transverseMass2(plots.DataMCPlot(datasets_tm, analysis+"/MTInvertedTauIdPhi"), "MTInvertedTauIdPhi", rebin=20)
#    transverseMass2(plots.DataMCPlot(datasets_tm, analysis+"/MTInvertedTauIdMet"), "MTInvertedTauIdMet", rebin=10)  

    transverseMass2(plots.DataMCPlot(datasets, analysis+"/transverseMass"), "transverseMass", rebin=5, ratio = True)
    path = analysis+"/transverseMass"
    transverseMass2(plots.DataMCPlot(datasets, path), "transverseMass", rebin=5)
    if QCDfromData:
        plot = replaceQCDfromData(plots.DataMCPlot(datasets, path), datasetsQCD, path)
        transverseMass2(plot, "transverseMass", rebin=20)

        
#    drawPlot(createPlot("GlobalElectronVeto/GlobalElectronPt_identified"), "electronPt", rebin=10, xlabel="p_{T}^{electron} (GeV/c)", ylabel="Identified electrons / %.0f GeV/c", ratio=False,  opts={"xmax": 250,"xmin": 0, "ymaxfactor": 2}, textFunction=lambda: addMassBRText(x=0.4, y=0.87), cutLine=15)

    drawPlot(createPlot("SelectedTau_pT_AfterCuts"), "SelectedTau_pT_AfterCuts", rebin=1, xlabel="p_{T}^{#tau jet} (GeV/c)", ylabel="#tau jets / %.0f GeV/c", ratio=False,  opts={"xmax": 250,"xmin": 0, "ymaxfactor": 2}, textFunction=lambda: addMassBRText(x=0.4, y=0.87), cutLine=15)
    
    jetPt(plots.DataMCPlot(datasets, analysis+"/SelectedTau_pT_AfterCuts"), "SelectedTau_pT_AfterCuts", rebin=5, ratio = True)
    jetEta(plots.DataMCPlot(datasets, analysis+"/SelectedTau_eta_AfterCuts"), "SelectedTau_eta_AfterCuts", rebin=10, ratio = True)
    jetEta(plots.DataMCPlot(datasets, analysis+"/SelectedTau_eta_BackToBack"), "SelectedTau_eta_BackToBack", rebin=10, ratio = True)
    jetEta(plots.DataMCPlot(datasets, analysis+"/SelectedTau_eta_NoBackToBack"), "SelectedTau_eta_NoBackToBack", rebin=10, ratio = True) 
    jetEta(plots.DataMCPlot(datasets, analysis+"/SelectedTau_eta_Collinear"), "SelectedTau_eta_Collinear", rebin=10, ratio = True) 


    
#    tauPt(createPlot("SelectedTau_pT_AfterCuts"), "SelectedTau_pT_AfterCuts", rebin=5, ratio=False, opts={"xmax": 300, "ymaxfactor": 2}, textFunction=lambda: addMassBRText(x=0.31, y=0.22)) 

    jetPt(plots.DataMCPlot(datasets, analysis+"/JetSelection/jet_pt"), "jetPt", rebin=5, ratio = True)
    jetEta(plots.DataMCPlot(datasets, analysis+"/JetSelection/jet_eta"), "jetEta", rebin=5, ratio = True)
    jetPhi(plots.DataMCPlot(datasets, analysis+"/JetSelection/jet_phi"), "jetPhi", rebin=5, ratio = True)
    numberOfJets(plots.DataMCPlot(datasets, analysis+"/JetSelection/NumberOfSelectedJets"), "NumberOfJets", ratio = True)
    jetEMFraction(plots.DataMCPlot(datasets, analysis+"/JetSelection/jetMaxEMFraction"), "jetMaxEMFraction", rebin=10)
    jetEMFraction(plots.DataMCPlot(datasets, analysis+"/JetSelection/jetEMFraction"), "jetEMFraction", rebin=20)
#    jetEMFraction(plots.DataMCPlot(datasets, analysis+"/JetSelection/chargedJetEMFraction"), "chargedJetEMFraction", rebin=20)
   
    jetPt(plots.DataMCPlot(datasets, analysis+"/Btagging/bjet_pt"), "bjetPt", rebin=5, ratio = True)
    jetEta(plots.DataMCPlot(datasets, analysis+"/Btagging/bjet_eta"), "bjetEta", rebin=5, ratio = True)
    numberOfJets(plots.DataMCPlot(datasets, analysis+"/Btagging/NumberOfBtaggedJets"), "NumberOfBJets", ratio = True)


# Electron veto
    drawPlot(createPlot("GlobalElectronVeto/GlobalElectronPt_identified"), "electronPt", rebin=3, xlabel="p_{T}^{electron} (GeV/c)", ylabel="Identified electrons / %.0f GeV/c", ratio=False,  opts={"xmax": 250,"xmin": 0, "ymaxfactor": 2}, textFunction=lambda: addMassBRText(x=0.4, y=0.87), cutLine=15)
    drawPlot(createPlot("GlobalElectronVeto/GlobalElectronEta_identified"), "electronEta", rebin=3, xlabel="#eta^{electron}", ylabel="Identified electrons / %.1f", ratio=False, opts={"xmin": -3,"ymin": 0.1, "xmax": 3, "ymaxfactor": 10}, moveLegend={"dy":0.01, "dx":-0.07, "dh":-0.06}, textFunction=lambda: addMassBRText(x=0.3, y=0.87), cutLine=[-2.5, 2.5])
#    drawPlot(createPlot("GlobalMuonVeto/NumberOfSelectedElectrons"), "NumberOfSelectedElectrons", rebin=1, xlabel="N^{selected electrons}", ylabel="Selected electrons", ratio=False,  opts={"ymaxfactor": 2,"xmax": 10}, textFunction=lambda: addMassBRText(x=0.35, y=0.9))
   
    # Muon veto
    drawPlot(createPlot("GlobalMuonVeto/GlobalMuonPt_identified_eta"), "muonPt", rebin=1, xlabel="p_{T}^{muon} (GeV/c)", ylabel="Identified muons / %.0f GeV/c", ratio=False,  opts={"ymaxfactor": 2,"xmax": 250,"xmin": 0}, textFunction=lambda: addMassBRText(x=0.35, y=0.9), cutLine=15)
#    drawPlot(createPlot("GlobalMuonVeto/NumberOfSelectedMuons"), "NumberOfSelectedMuons", rebin=1, xlabel="N^{selected muons}", ylabel="Selected muons", ratio=False,  opts={"ymaxfactor": 2,"xmax": 10}, textFunction=lambda: addMassBRText(x=0.35, y=0.9))
    drawPlot(createPlot("GlobalMuonVeto/GlobalMuonEta_identified"), "muonEta", rebin=3, xlabel="#eta^{muon}", ylabel="Identified muons / %.1f", ratio=False, opts={"xmin": -3,"ymin": 0.1, "xmax": 3, "ymaxfactor": 20}, moveLegend={"dy":0.01, "dx":-0.07, "dh":-0.06}, textFunction=lambda: addMassBRText(x=0.30, y=0.87), cutLine=[-2.5, 2.5])
    
#    jetPt(plots.DataMCPlot(datasets, analysis+"/GlobalElectronVeto/GlobalElectronPt"), "electronPt", ratio = True)
#    jetEta(plots.DataMCPlot(datasets, analysis+"/GlobalElectronVeto/GlobalElectronEta"), "electronEta", ratio = True)
    
#    jetPt(plots.DataMCPlot(datasets, analysis+"/GlobalMuonVeto/GlobalMuonPt"), "muonPt", ratio = True)
#    jetEta(plots.DataMCPlot(datasets, analysis+"/GlobalMuonVeto/GlobalMuonEta"), "muonEta", ratio = True)
    
    topMass(plots.DataMCPlot(datasets, analysis+"/TopSelection/jjbMass"), "jjbMass", rebin=10)
    topMass(plots.DataMCPlot(datasets, analysis+"/TopChiSelection/TopMass"), "topMass_chi", rebin=10)

     # Delta phi

    deltaPhi2(plots.DataMCPlot(datasets, analysis+"/deltaPhi"), "DeltaPhiTauMet", rebin=15)
    deltaPhi2(plots.DataMCPlot(datasets, analysis+"/FakeMETVeto/Closest_DeltaPhi_of_MET_and_selected_jets"), "DeltaPhiJetMet", rebin=5)

#    deltaPhi2(createPlot("TauEmbeddingAnalysis_afterTauId_DeltaPhi"))
#    deltaPhi2(createPlot("deltaPhi"), "DeltaPhiTauMet", rebin=10, moveLegend={"dx":-0.21}, textFunction=lambda: addMassBRText(x=0.2, y=0.87), cutLine=[160, 130])
#    deltaPhi2(createPlot("FakeMETVeto/Closest_DeltaPhi_of_MET_and_selected_jets"), "DeltaPhiJetMet")
    
    transverseMass2(plots.DataMCPlot(datasets, analysis+"/FullHiggsMass/HiggsMass"), "HiggsMass", rebin=10)
  
#    drawPlot(createPlot("FullHiggsMass/HiggsMass"), "HiggsMass", rebin=2, log=False,xlabel="m_{Higgs} (GeV/c^{2})", ylabel="Events / %.0f GeV", opts={"xmax": 400})
    
    met2(plots.DataMCPlot(datasets, analysis+"/MET_BaseLineTauIdJets"), "MET_BaseLineTauIdJets", rebin=20, ratio = True)
    met2(plots.DataMCPlot(datasets, analysis+"/MET_InvertedTauIdJets"), "MET_InvertedTauIdJets", rebin=20, ratio = True)
    met2(plots.DataMCPlot(datasets, analysis+"/MET_BaseLineTauIdBtag"), "MET_BaseLineTauIdBtag", rebin=20, ratio = True)
    met2(plots.DataMCPlot(datasets, analysis+"/MET_InvertedTauIdBtag"), "MET_InvertedTauIdBtag", rebin=20, ratio = True)
    met2(plots.DataMCPlot(datasets, analysis+"/MET_BaseLineTauIdBtagDphi"), "MET_BaseLineTauIdBtagDphi", rebin=20, ratio = True)
    met2(plots.DataMCPlot(datasets, analysis+"/MET_InvertedTauIdBtagDphi"), "MET_InvertedTauIdBtagDphi", rebin=20, ratio = True)
#    met2(plots.DataMCPlot(datasets, analysis+"/MET_InvertedTauIdAllCuts"), "MET_InvertedTauIdAllCuts", rebin=10)   
#    met2(plots.DataMCPlot(datasets, analysis+"/MET_BaseLineTauIdAllCuts"), "MET_BaseLineTauIdAllCuts", rebin=10)
#    met2(plots.DataMCPlot(datasets, analysis+"/MET_InvertedTauIdAllCuts"), "MET_InvertedTauIdAllCuts", rebin=10)    
    
    pasJuly = "met_p4.Et() > 70 && Max$(jets_btag) > 1.7"
#    topMass(plots.DataMCPlot(datasets, treeDraw.clone(varexp="topreco_p4.M()>>dist(20,0,800)", selection=pasJuly)), "topMass", rebin=1)

#    met2(plots.DataMCPlot(datasets, treeDraw.clone(varexp="met_p4.Et()>>dist(20,0,400)")), "metRaw", rebin=1)
#    met2(plots.DataMCPlot(datasets, treeDraw.clone(varexp="metType1_p4.Et()>>dist(20,0,400)")), "metType1", rebin=1)

#    mt = "sqrt(2 * tau_p4.Pt() * met_p4.Et() * (1-cos(tau_p4.Phi()-met_p4.Phi())))"
#    transverseMass2(plots.DataMCPlot(datasets, treeDraw.clone(varexp=mt+">>dist(40,0,400)", selection=pasJuly)), "transverseMass_metRaw", rebin=1)
#    transverseMass2(plots.DataMCPlot(datasets, treeDraw.clone(varexp=mt.replace("met", "metType1")+">>dist(40,0,400)", selection=pasJuly.replace("met", "metType1"))), "transverseMass_metType1", rebin=1)

#    genComparison(datasets)
#    zMassComparison(datasets)
#    topMassComparison(datasets)
#    topPtComparison(datasets) 
#    vertexComparison(datasets)

    mtTest(datasets)
    mtBtagTest(datasets)
    BtagEfficiencies(datasets) 
    mtComparison(datasets)
    metComparison(datasets)
    purityJets(datasets)  
    purityBveto(datasets)
    purityBtag(datasets)
    purityDeltaPhi(datasets)
    
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
    cellFormat = counter.TableFormatText(cellFormat=counter.CellFormatText(valueOnly=False))
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
    
def mtTest(datasets):
    
    ## After standard cut
    mtTauVeto = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/transverseMassBeforeVeto")])
    mtLeptonVeto = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/transverseMassAfterVeto")])
    mtNoMet = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/transverseMassNoMet")])
    mtNoMetBtag = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/transverseMassNoMetBtag")])
    mtMet = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdJet")])
    mtBtag = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdBtag")])
    mtDeltaPhi = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdPhi")])
    
    mtTauVeto.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mtLeptonVeto.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mtNoMet.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mtMet.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mtBtag.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mtDeltaPhi.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())

    
    mtTauVeto._setLegendStyles()
    mtTauVeto._setLegendLabels()
    mtTauVeto.histoMgr.setHistoDrawStyleAll("P")
    mtTauVeto.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))
    hmtTauVeto = mtTauVeto.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/transverseMassBeforeVeto")
    
    mtLeptonVeto._setLegendStyles()
    mtLeptonVeto._setLegendLabels()
    mtLeptonVeto.histoMgr.setHistoDrawStyleAll("P")
    mtLeptonVeto.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))
    hmtLeptonVeto = mtLeptonVeto.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/transverseMassAfterVeto")
    
    mtNoMet._setLegendStyles()
    mtNoMet._setLegendLabels()
    mtNoMet.histoMgr.setHistoDrawStyleAll("P")
    mtNoMet.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))
    hmtNoMet = mtNoMet.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/transverseMassNoMet")
    
    mtNoMetBtag._setLegendStyles()
    mtNoMetBtag._setLegendLabels()
    mtNoMetBtag.histoMgr.setHistoDrawStyleAll("P")
    mtNoMetBtag.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))
    hmtNoMetBtag = mtNoMetBtag.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/transverseMassNoMetBtag")

    mtMet._setLegendStyles()
    mtMet._setLegendLabels()
    mtMet.histoMgr.setHistoDrawStyleAll("P")
    mtMet.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))
    hmtMet = mtMet.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJet")

    mtBtag._setLegendStyles()
    mtBtag._setLegendLabels()
    mtBtag.histoMgr.setHistoDrawStyleAll("P")
    mtBtag.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))
    hmtBtag = mtBtag.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdBtag")

    mtDeltaPhi._setLegendStyles()
    mtDeltaPhi._setLegendLabels()
    mtDeltaPhi.histoMgr.setHistoDrawStyleAll("P")
    mtDeltaPhi.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))
    hmtDeltaPhi = mtDeltaPhi.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdPhi")
    
    
    canvas30 = ROOT.TCanvas("canvas30","",500,500)
    canvas30.SetLogy()
#    hmtData.SetMaximum(120.0)
    hmtTauVeto.SetMarkerColor(4)
    hmtTauVeto.SetMarkerSize(1)
    hmtTauVeto.SetMarkerStyle(22)
#    hmtTauVeto.Draw("EP")
     
    hmtLeptonVeto.SetMarkerColor(6)
    hmtLeptonVeto.SetMarkerSize(1)
    hmtLeptonVeto.SetMarkerStyle(24)
    hmtLeptonVeto.SetFillColor(4)
#    hmtLeptonVeto.Draw("same")
    
    hmtNoMet.SetMarkerColor(6)
    hmtNoMet.SetMarkerSize(1)
    hmtNoMet.SetMarkerStyle(22)
    hmtNoMet.SetFillColor(4)
    hmtNoMet.Draw("EP")

    hmtNoMetBtag.SetMarkerColor(7)
    hmtNoMetBtag.SetMarkerSize(1)
    hmtNoMetBtag.SetMarkerStyle(21)
    hmtNoMetBtag.SetFillColor(4)
    hmtNoMetBtag.Draw("same")

    hmtMet.SetMarkerColor(1)
    hmtMet.SetMarkerSize(1)
    hmtMet.SetMarkerStyle(23)
    hmtMet.SetFillColor(4)
    hmtMet.Draw("same")

    
    hmtBtag.SetMarkerColor(4)
    hmtBtag.SetMarkerSize(1)
    hmtBtag.SetMarkerStyle(24)
    hmtBtag.SetFillColor(4)
    hmtBtag.Draw("same")
    
    hmtDeltaPhi.SetMarkerColor(2)
    hmtDeltaPhi.SetMarkerSize(1)
    hmtDeltaPhi.SetMarkerStyle(20)
    hmtDeltaPhi.SetFillColor(4)
    hmtDeltaPhi.Draw("same")

                        
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       5.05 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    tex5 = ROOT.TLatex(0.5,0.8,"After MET cut")
    tex5.SetNDC()
    tex5.SetTextSize(20)
#    tex5.Draw()
        
    hmtTauVeto.GetYaxis().SetTitle("Events / 10 GeV/c^{2}")
    hmtNoMet.GetYaxis().SetTitle("Events / 10 GeV/c^{2}")
#    hmt.GetYaxis().SetTitleSize(20.0)
    hmtTauVeto.GetYaxis().SetTitleOffset(1.5)
    hmtTauVeto.GetXaxis().SetTitle("m_{T}(#tau jet, MET) (GeV/c^{2})")

    tex1 = ROOT.TLatex(0.65,0.7,"#tau veto ")
    tex1.SetNDC()
    tex1.SetTextSize(23)
#    tex1.Draw()    
    marker1 = ROOT.TMarker(0.6,0.715,hmtTauVeto.GetMarkerStyle())
#    marker1 = ROOT.TMarker(0.25,0.415,hmt.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(hmtTauVeto.GetMarkerColor())
    marker1.SetMarkerSize(0.9*hmtTauVeto.GetMarkerSize())
#    marker1.Draw()
    
    tex2 = ROOT.TLatex(0.65,0.6,"lepton veto")
    tex2.SetNDC()
    tex2.SetTextSize(23)
#    tex2.Draw()    
    marker2 = ROOT.TMarker(0.6,0.615,hmtNoMet.GetMarkerStyle())
#    marker1 = ROOT.TMarker(0.25,0.415,hmt.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(hmtNoMet.GetMarkerColor())
    marker2.SetMarkerSize(0.9*hmtNoMet.GetMarkerSize())
#    marker2.Draw()

    tex3 = ROOT.TLatex(0.63,0.9,"jets, no MET cut")
    tex3.SetNDC()
    tex3.SetTextSize(16)
    tex3.Draw()    
    marker3 = ROOT.TMarker(0.6,0.91,hmtNoMet.GetMarkerStyle())
#    marker1 = ROOT.TMarker(0.25,0.415,hmt.GetMarkerStyle())
    marker3.SetNDC()
    marker3.SetMarkerColor(hmtNoMet.GetMarkerColor())
    marker3.SetMarkerSize(0.9*hmtNoMet.GetMarkerSize())
    marker3.Draw()
    
    tex6 = ROOT.TLatex(0.63,0.85,"b tagging, no MET cut")
    tex6.SetNDC()
    tex6.SetTextSize(16)
    tex6.Draw()    
    marker6 = ROOT.TMarker(0.6,0.86,hmtNoMetBtag.GetMarkerStyle())
#    marker1 = ROOT.TMarker(0.25,0.415,hmt.GetMarkerStyle())
    marker6.SetNDC()
    marker6.SetMarkerColor(hmtNoMetBtag.GetMarkerColor())
    marker6.SetMarkerSize(0.9*hmtNoMetBtag.GetMarkerSize())
    marker6.Draw()
    
    tex7 = ROOT.TLatex(0.63,0.80,"MET cut")
    tex7.SetNDC()
    tex7.SetTextSize(16)
    tex7.Draw()    
    marker7 = ROOT.TMarker(0.6,0.81,hmtMet.GetMarkerStyle())
#    marker1 = ROOT.TMarker(0.25,0.415,hmt.GetMarkerStyle())
    marker7.SetNDC()
    marker7.SetMarkerColor(hmtMet.GetMarkerColor())
    marker7.SetMarkerSize(0.9*hmtMet.GetMarkerSize())
    marker7.Draw()

    tex8 = ROOT.TLatex(0.63,0.75,"b tagging")
    tex8.SetNDC()
    tex8.SetTextSize(16)
    tex8.Draw()    
    marker8 = ROOT.TMarker(0.6,0.76,hmtBtag.GetMarkerStyle())
#    marker1 = ROOT.TMarker(0.25,0.415,hmt.GetMarkerStyle())
    marker8.SetNDC()
    marker8.SetMarkerColor(hmtBtag.GetMarkerColor())
    marker8.SetMarkerSize(0.9*hmtBtag.GetMarkerSize())
    marker8.Draw()
    
    tex9 = ROOT.TLatex(0.63,0.70,"#Delta#Phi cut")
    tex9.SetNDC()
    tex9.SetTextSize(15)
    tex9.Draw()    
    marker9 = ROOT.TMarker(0.6,0.71,hmtDeltaPhi.GetMarkerStyle())
#    marker1 = ROOT.TMarker(0.25,0.415,hmt.GetMarkerStyle())
    marker9.SetNDC()
    marker9.SetMarkerColor(hmtDeltaPhi.GetMarkerColor())
    marker9.SetMarkerSize(0.9*hmtDeltaPhi.GetMarkerSize())
    marker9.Draw()
    
    canvas30.Print("mt_test.png")
    canvas30.Print("mt_test.C")



def mtBtagTest(datasets):
    
    ## After standard cut

    mtMet = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdJet")])
    mtBtag = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdBtag")])
    mtMet.histoMgr.normalizeToOne()
    mtBtag.histoMgr.normalizeToOne()

    mtMet._setLegendStyles()
    mtMet._setLegendLabels()
    mtMet.histoMgr.setHistoDrawStyleAll("P")
    mtMet.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))
    hmtMet = mtMet.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJet")

    mtBtag._setLegendStyles()
    mtBtag._setLegendLabels()
    mtBtag.histoMgr.setHistoDrawStyleAll("P")
    mtBtag.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))
    hmtBtag = mtBtag.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdBtag")

       
    canvas40 = ROOT.TCanvas("canvas40","",500,500)
    canvas40.SetLogy()
    hmtMet.SetMaximum(0.2)
    hmtMet.SetMarkerColor(2)
    hmtMet.SetMarkerSize(1)
    hmtMet.SetMarkerStyle(23)
    hmtMet.SetFillColor(2)
    hmtMet.Draw()
    
    hmtBtag.SetMarkerColor(4)
    hmtBtag.SetMarkerSize(1)
    hmtBtag.SetMarkerStyle(24)
    hmtBtag.SetFillColor(4)
    hmtBtag.Draw("same")
    
    hmtMet.GetYaxis().SetTitle("Arbitrary normalisation")
    hmtMet.GetYaxis().SetTitleOffset(1.5)
    hmtMet.GetXaxis().SetTitle("m_{T}(#tau jet, MET) (GeV/c^{2})")
    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       5.05 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    tex3 = ROOT.TLatex(0.5,0.85,"Inverted #tau isolation")
    tex3.SetNDC()
    tex3.SetTextSize(22)
    tex3.Draw()
    
    tex7 = ROOT.TLatex(0.28,0.4,"MET cut")
    tex7.SetNDC()
    tex7.SetTextSize(25)
    tex7.Draw()    
    marker7 = ROOT.TMarker(0.25,0.41,hmtMet.GetMarkerStyle())
#    marker1 = ROOT.TMarker(0.25,0.415,hmt.GetMarkerStyle())
    marker7.SetNDC()
    marker7.SetMarkerColor(hmtMet.GetMarkerColor())
    marker7.SetMarkerSize(0.99*hmtMet.GetMarkerSize())
    marker7.Draw()

    tex8 = ROOT.TLatex(0.28,0.3,"MET cut + b tagging")
    tex8.SetNDC()
    tex8.SetTextSize(25)
    tex8.Draw()    
    marker8 = ROOT.TMarker(0.25,0.31,hmtBtag.GetMarkerStyle())
#    marker1 = ROOT.TMarker(0.25,0.415,hmt.GetMarkerStyle())
    marker8.SetNDC()
    marker8.SetMarkerColor(hmtBtag.GetMarkerColor())
    marker8.SetMarkerSize(0.9*hmtBtag.GetMarkerSize())
    marker8.Draw()
    

    canvas40.Print("btagTest_mt.png")
    canvas40.Print("btagTest_mt.C") 

        
###########################################
    ### Normalised mt and dphi distribution
def mtComparison(datasets):
    
    ## After standard cuts
    
    if (btagFactorisation):
        # no b tagging, no deltaPhi cut
        mt4050 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdJet4050")])
        mt5060 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdJet5060")])
        mt6070 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdJet6070")])
        mt7080 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdJet7080")])
        mt80100 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdJet80100")])
        mt100120 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdJet100120")])
        if lastPtBin150: 
            mt120150 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdJet120150")])
            mt150 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdJet150")])
        if lastPtBin120: 
            mt120 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdJet120")])
        mt = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdJet")])
        
        mtBaseline = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTBaseLineTauIdJet")])
        mtEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MTBaseLineTauIdJet")])
        
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

  ## 
    if (deltaPhi130):                        
        mt4050 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdMet4050")])
        mt5060 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdMet5060")])
        mt6070 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdMet6070")])
        mt7080 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdMet7080")])
        mt80100 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdMet80100")])
        mt100120 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdMet100120")])
        mt = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdMet")])
        if lastPtBin150: 
            mt120150 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdMet120150")])
            mt150 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdMet150")])
        if lastPtBin120: 
            mt120 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdMet120")])
        mt = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdMet")])
            
        mtBaseline = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTBaseLineTauIdBtag")])
        mtEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MTBaseLineTauIdBtag")])

    if (numberOfBjets):
        mt4050 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/NBInvertedTauIdJet4050")])
        mt5060 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/NBInvertedTauIdJet5060")])
        mt6070 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/NBInvertedTauIdJet6070")])
        mt7080 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/NBInvertedTauIdJet7080")])
        mt80100 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/NBInvertedTauIdJet80100")])
        mt100120 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/NBInvertedTauIdJet100120")])
        if lastPtBin150: 
            mt120150 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/NBInvertedTauIdJet120150")])
            mt150 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/NBInvertedTauIdJet150")])
        if lastPtBin120: 
            mt120 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/NBInvertedTauIdJet120")])
        mt = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/NBInvertedTauIdJet")])
    
        
   
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

## After deltaPhi < 160 cut
    if (deltaPhi160):
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

        ## deltaPhi distribution
    if (deltaPhiDistribution):
        mt4050 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/deltaPhiInverted4050")])
        mt5060 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/deltaPhiInverted5060")])
        mt6070 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/deltaPhiInverted6070")])
        mt7080 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/deltaPhiInverted7080")])
        mt80100 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/deltaPhiInverted80100")])
        mt100120 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/deltaPhiInverted100120")])
        if lastPtBin150:
            mt120150 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/deltaPhiInverted120150")])
            mt150 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/deltaPhiInverted150")])
        if lastPtBin120:
            mt120 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/deltaPhiInverted120")])
        mt = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/deltaPhiInverted")])
        mtBaseline = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTBaseLineTauIdPhi")])
        mtEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MTBaseLineTauIdPhi")]) 

                ## deltaPhi distribution
    if (HiggsMass):
        mt4050 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/HiggsMass4050")])
        mt5060 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/HiggsMass5060")])
        mt6070 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/HiggsMass6070")])
        mt7080 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/HiggMass7080")])
        mt80100 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/HiggsMass80100")])
        mt100120 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/HiggsMass100120")])
        if lastPtBin150:
            mt120150 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/HiggsMass120150")])
            mt150 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/HiggsMass150")])
        if lastPtBin120: 
            mt120 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/HiggsMass120")])
        mt = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/HiggsMass")])
        mtBaseline = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTBaseLineTauIdPhi")])
        mtEWK = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MTBaseLineTauIdPhi")])

        
    if (HiggsMassPhi140):
        mt4050 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/HiggsMassPhi4050")])
        mt5060 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/HiggsMassPhi5060")])
        mt6070 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/HiggsMassPhi6070")])
        mt7080 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/HiggsMassPhi7080")])
        mt80100 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/HiggsMassPhi80100")])
        mt100120 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/HiggsMassPhi100120")])
        if lastPtBin150:
            mt120150 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/HiggsMassPhi120150")])
            mt150 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/HiggsMassPhi150")])
        if lastPtBin120:
            mt120 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/HiggsMassPhi120")])
        mt = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/HiggsMassPhi")])
        
        mtBaseline = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTBaseLineTauIdPhi")])
        
    if lastPtBin150:
        print " norm factors ",norm_inc,norm_4050,norm_5060,norm_6070,norm_7080,norm_80100,norm_100120,norm_120150,norm_150
    if lastPtBin120:
        print " norm factors ",norm_inc,norm_4050,norm_5060,norm_6070,norm_7080,norm_80100,norm_100120,norm_120

#    mt.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
#    mt4050._setLegend(histograms.createLegend())


    mt4050._setLegendStyles()
    mt4050._setLegendLabels()
    mt4050.histoMgr.setHistoDrawStyleAll("P")
    if (numberOfBjets):
        mt4050.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))
    else:
        mt4050.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
#    hmt4050 = mt4050.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJetPhi4050")
    hmt4050 = mt4050.histoMgr.getHisto("Data").getRootHisto().Clone()
    hmtSum2 = hmt4050.Clone("mtSum2")
    print "Integral 4050  = ",hmt4050.Integral()
    
#    if (btagging):
#        hmt4050.Scale(0.00926618859472)   # btag
    hmt4050.Scale(norm_4050) 
#    else:
#        hmt4050.Scale(0.00903051176553)  # jets
    
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

        
    mt._setLegendStyles()
    mt._setLegendLabels()
    mt.histoMgr.setHistoDrawStyleAll("P")
    if (numberOfBjets):
        mt.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))
    else:
        mt.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))  
    hmt = mt.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJetPhi")
    hmt.Scale(norm_inc)
    
    if False: 
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

        
        
    canvas = ROOT.TCanvas("canvas","",500,500)
    canvas.Divide(3,3)
    canvas.cd(1)
    hmt4050.GetYaxis().SetTitle("Events")
    hmt4050.GetXaxis().SetTitle("m_{T}(#tau jet, MET) (GeV/c^{2})")
    hmt4050.Draw()
    canvas.cd(2)
    hmt5060.Draw()
    canvas.cd(3)
    hmt6070.Draw()
    canvas.cd(4)
    hmt7080.Draw()
    canvas.cd(5)
    hmt80100.Draw()
    canvas.cd(6)
    hmt100120.Draw()
    if lastPtBin150:
        canvas.cd(7)
        hmt120150.Draw()
        canvas.cd(8)
        hmt150.Draw()    
        canvas.cd(9)
        hmtSum.Draw()
    if lastPtBin120:
        canvas.cd(7)
        hmt120.Draw()
        canvas.cd(8)
        hmtSum.Draw()
        
#    canvas.Print("mtComparison_PhiCut.png")
#    if(btagging):
    if(deltaPhi180): 
        canvas.Print("mtComparison.png")
        canvas.Print("mtComparison.C")
    if(numberOfBjets): 
        canvas.Print("NBComparison.png")
        canvas.Print("NBComparison.C") 
    if(deltaPhi160):
        canvas.Print("mtComparison_dphi160.png")
        canvas.Print("mtComparison_dphi160.C")
    if(deltaPhi130):
        canvas.Print("mtComparison_dphi130.png")
        canvas.Print("mtComparison_dphi130.C")
    if(deltaPhiDistribution):
        canvas.Print("deltaPhiInverted.png")
        canvas.Print("deltaPhiInverted.C")
    if(HiggsMass):
        canvas.Print("HiggsMassInverted.png")
        canvas.Print("HiggsMassInverted.C")
        
    if(HiggsMassPhi140):
        canvas.Print("HiggsMassInvertedPhi140.png")
        canvas.Print("HiggsMassInvertedPhi140.C")
    if(topmass):
        canvas.Print("mtComparison_dphi160_topmass.png")
        canvas.Print("mtComparison_dphi160_topmass.C")

        
##    rtauGen(mt4050, "transverseMass_vs_pttau", rebin=20)
    print "Integral with bins  = ",hmtSum.Integral()
    print "Integral2 with bins  = ",hmtSum2.Integral()
    print "Integral inclusive  = ",hmt.Integral()    
############
    canvas2 = ROOT.TCanvas("canvas2","",500,500)   
    hmtSum.Draw()
    hmtSum.GetYaxis().SetTitle("Events")
    hmtSum.GetXaxis().SetTitle("m_{T}(#tau jet, MET) (GeV/c^{2})")
    if (deltaPhi160):
        canvas2.Print("mtSum_PhiCut.png")
    if (deltaPhiDistribution):
        canvas2.Print("deltaPhiInvertedSum.png")

    if (HiggsMass):
        canvas2.Print("HiggsMassSum.png")
    if (HiggsMassPhi140):
        canvas2.Print("HiggsMassSumPhi140.png")
        
############
    if deltaPhi160 or deltaPhi180:
        canvas25 = ROOT.TCanvas("canvas25","",500,500)
        hmtBaseline.SetMarkerColor(1)
        hmtBaseline.SetMarkerSize(1)
        hmtBaseline.SetMarkerStyle(27)
        hmtBaseline.SetFillColor(1)
        #    hmtBaseline.Draw()
        hmtBaseline_QCD = hmtBaseline.Clone("QCD")
        hmtBaseline_QCD.Add(hmtEWK,-1)
        hmtBaseline_QCD.SetMarkerColor(2)
        hmtBaseline_QCD.SetMarkerSize(1)
        hmtBaseline_QCD.SetMarkerStyle(20)
        hmtBaseline_QCD.Draw()
        hmtBaseline.GetYaxis().SetTitle("Events")
        hmtBaseline.GetXaxis().SetTitle("m_{T}(#tau jet, MET) (GeV/c^{2})")
        if (deltaPhi160):
            canvas25.Print("mtBaseline.png")

###########

## for deltaPhi < 160 and 180 (includes baseline)
    if deltaPhi160 or deltaPhi180:
        canvas3 = ROOT.TCanvas("canvas3","",500,500)
        #    canvas3.SetLogy()
        #    hmt.SetMaximum(120.0)
        
        hmtSum.SetMarkerColor(4)
        hmtSum.SetMarkerSize(1)
        hmtSum.SetMarkerStyle(20)
        hmtSum.SetFillColor(4)
        hmtSum.Draw("EP")
        
        hmt.SetMarkerColor(2)
        hmt.SetMarkerSize(1)
        hmt.SetMarkerStyle(21)
        hmt.Draw("same")
        
        #    hmtSum.SetMarkerColor(4)
        #    hmtSum.SetMarkerSize(1)
        #    hmtSum.SetMarkerStyle(20)
        #    hmtSum.SetFillColor(4)
        #    hmtSum.Draw("same")
        
        hmtBaseline.SetMarkerColor(1)
        hmtBaseline.SetMarkerSize(1)
        hmtBaseline.SetMarkerStyle(22)
        hmtBaseline.SetFillColor(1)
#        hmtBaseline.Draw("same")
        hmtBaseline_QCD = hmtBaseline.Clone("QCD")
        hmtBaseline_QCD.Add(hmtEWK,-1)
        hmtBaseline_QCD.SetMarkerColor(1)
        hmtBaseline_QCD.SetMarkerSize(1)
        hmtBaseline_QCD.SetMarkerStyle(22)
        hmtBaseline_QCD.SetFillColor(1)
        hmtBaseline_QCD.Draw("same")
        
        #hmtEWK.SetMarkerColor(7)
        #    hmtEWK.SetMarkerSize(1)
        #    hmtEWK.SetMarkerStyle(23)
        #    hmtEWK.SetFillColor(7)
        #    hmtEWK.Draw("same")
        
        tex1 = ROOT.TLatex(0.65,0.7,"No binning")
        #    tex1 = ROOT.TLatex(0.3,0.4,"No binning")
        tex1.SetNDC()
        tex1.SetTextSize(20)
        tex1.Draw()    
        marker1 = ROOT.TMarker(0.6,0.715,hmt.GetMarkerStyle())
        #    marker1 = ROOT.TMarker(0.25,0.415,hmt.GetMarkerStyle())
        marker1.SetNDC()
        marker1.SetMarkerColor(hmt.GetMarkerColor())
        marker1.SetMarkerSize(0.9*hmt.GetMarkerSize())
        marker1.Draw()
        
        #    tex2 = ROOT.TLatex(0.3,0.3,"With p_{T}^{#tau jet} bins")
        tex2 = ROOT.TLatex(0.65,0.6,"With p_{T}^{#tau jet} bins") 
        tex2.SetNDC()
        tex2.SetTextSize(20)
        tex2.Draw()    
        #    marker2 = ROOT.TMarker(0.25,0.32,hmtSum.GetMarkerStyle())
        marker2 = ROOT.TMarker(0.6,0.615,hmtSum.GetMarkerStyle())
        marker2.SetNDC()
        marker2.SetMarkerColor(hmtSum.GetMarkerColor())
        marker2.SetMarkerSize(0.9*hmtSum.GetMarkerSize())
        marker2.Draw()
        
        tex9 = ROOT.TLatex(0.65,0.5,"Baseline-EWK") 
        tex9.SetNDC()
        tex9.SetTextSize(20)
        tex9.Draw()    
        #    marker2 = ROOT.TMarker(0.25,0.32,hmtBaseline_QCD.GetMarkerStyle())
        marker9 = ROOT.TMarker(0.6,0.515,hmtBaseline_QCD.GetMarkerStyle())
        marker9.SetNDC()
        marker9.SetMarkerColor(hmtSum.GetMarkerColor())
        marker9.SetMarkerSize(0.9*hmtBaseline_QCD.GetMarkerSize())
        marker9.Draw()
        
        tex3 = ROOT.TLatex(0.5,0.85,"With inverted #tau isolation")
        tex3.SetNDC()
        tex3.SetTextSize(20)
        tex3.Draw()
        
        tex5 = ROOT.TLatex(0.5,0.8,"MET > 70 GeV")
        tex5.SetNDC()
        tex5.SetTextSize(20)
        #    tex5.Draw()
        
        if(deltaPhi180):
            tex5 = ROOT.TLatex(0.5,0.8,"#Delta#phi(#tau jet, MET) < 180^{o}")
            tex5.SetNDC()
            tex5.SetTextSize(20)
            tex5.Draw()
        if(deltaPhi130):
            tex5 = ROOT.TLatex(0.5,0.8,"#Delta#phi(#tau jet, MET) < 160^{o}")
            tex5.SetNDC()
            tex5.SetTextSize(20)
            tex5.Draw()
            
        tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       5.05 fb^{-1}       CMS Preliminary ")
        tex4.SetNDC()
        tex4.SetTextSize(20)
        tex4.Draw()
        
        hmtSum.GetYaxis().SetTitle("Events / 10 GeV/c^{2}")
        #    hmt.GetYaxis().SetTitleSize(20.0)
        hmtSum.GetYaxis().SetTitleOffset(1.5)
        hmtSum.GetXaxis().SetTitle("m_{T}(#tau jet, MET) (GeV/c^{2})")
        #    canvas3.Print("mtInverted.png")
        #    canvas3.Print("mtInverted.C")    
        #    canvas3.Print("mtInverted_Met70_log.png")
        #    canvas3.Print("mtInverted_Met70_log.C")
        
        if(deltaPhi180):  
            canvas3.Print("mtInverted_btag.png")
            canvas3.Print("mtInverted_btag.C")

        if(deltaPhi160):
            canvas3.Print("mtInverted_btag_dphi160.png")
            canvas3.Print("mtInverted_btag_dphi160.C")

            
 ## for deltaPhi < 160 for mt shape
    if deltaPhi160:
        canvas32 = ROOT.TCanvas("canvas32","",500,500)
        #    canvas3.SetLogy()
        #    hmt.SetMaximum(120.0)
        
        hmtSum.SetMarkerColor(4)
        hmtSum.SetMarkerSize(1)
        hmtSum.SetMarkerStyle(20)
        hmtSum.SetFillColor(4)
        hmtSum.Draw("EP")
        

        #    tex2 = ROOT.TLatex(0.3,0.3,"With p_{T}^{#tau jet} bins")
        tex2 = ROOT.TLatex(0.65,0.6,"With p_{T}^{#tau jet} bins") 
        tex2.SetNDC()
        tex2.SetTextSize(23)
        tex2.Draw()    
        #    marker2 = ROOT.TMarker(0.25,0.32,hmtSum.GetMarkerStyle())
        marker2 = ROOT.TMarker(0.6,0.615,hmtSum.GetMarkerStyle())
        marker2.SetNDC()
        marker2.SetMarkerColor(hmtSum.GetMarkerColor())
        marker2.SetMarkerSize(0.9*hmtSum.GetMarkerSize())
        marker2.Draw()
        
        tex3 = ROOT.TLatex(0.5,0.85,"With inverted #tau isolation")
        tex3.SetNDC()
        tex3.SetTextSize(20)
        tex3.Draw()
    
            
        tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       5.05 fb^{-1}       CMS Preliminary ")
        tex4.SetNDC()
        tex4.SetTextSize(20)
        tex4.Draw()
        
        hmtSum.GetYaxis().SetTitle("Events / 10 GeV/c^{2}")
        #    hmt.GetYaxis().SetTitleSize(20.0)
        hmtSum.GetYaxis().SetTitleOffset(1.5)
        hmtSum.GetXaxis().SetTitle("m_{T}(#tau jet, MET) (GeV/c^{2})")
        #    canvas3.Print("mtInverted.png")
        #    canvas3.Print("mtInverted.C")    
        #    canvas3.Print("mtInverted_Met70_log.png")
        #    canvas3.Print("mtInverted_Met70_log.C")
        
        if(deltaPhi160):
            canvas32.Print("transverseMass.png")
            canvas32.Print("transverseMass.C")
 


###########
## for ofter cuts
    if deltaPhi130 or btagFactorisation or topmass or deltaPhiDistribution or HiggsMass or numberOfBjets:    
        canvas31 = ROOT.TCanvas("canvas31","",500,500)
        if (numberOfBjets):
            canvas31.SetLogy()
        #    hmt.SetMaximum(120.0)
        
        hmtSum.SetMarkerColor(4)
        hmtSum.SetMarkerSize(1)
        hmtSum.SetMarkerStyle(20)
        hmtSum.SetFillColor(4)
        hmtSum.Draw("EP")
        
        hmt.SetMarkerColor(2)
        hmt.SetMarkerSize(1)
        hmt.SetMarkerStyle(21)
        hmt.Draw("same")
        
        #    hmtSum.SetMarkerColor(4)
        #    hmtSum.SetMarkerSize(1)
        #    hmtSum.SetMarkerStyle(20)
        #    hmtSum.SetFillColor(4)
        #    hmtSum.Draw("same")
        
        if deltaPhi130 or btagFactorisation or topmass or HiggsMass or numberOfBjets:
            xpos = 0.6
            xpos2 = 0.5
        if deltaPhiDistribution:
            xpos = 0.3
            xpos2 =0.3
        tex1 = ROOT.TLatex(xpos+0.05,0.7,"No binning")
        #    tex1 = ROOT.TLatex(0.3,0.4,"No binning")
        tex1.SetNDC()
        tex1.SetTextSize(23)
        tex1.Draw()    
        marker1 = ROOT.TMarker(xpos,0.715,hmt.GetMarkerStyle())
        #    marker1 = ROOT.TMarker(0.25,0.415,hmt.GetMarkerStyle())
        marker1.SetNDC()
        marker1.SetMarkerColor(hmt.GetMarkerColor())
        marker1.SetMarkerSize(0.9*hmt.GetMarkerSize())
        marker1.Draw()   
        #    tex2 = ROOT.TLatex(0.3,0.3,"With p_{T}^{#tau jet} bins")
        tex2 = ROOT.TLatex(xpos+0.05,0.6,"With p_{T}^{#tau jet} bins") 
        tex2.SetNDC()
        tex2.SetTextSize(23)
        tex2.Draw()    
        #    marker2 = ROOT.TMarker(0.25,0.32,hmtSum.GetMarkerStyle())
        marker2 = ROOT.TMarker(xpos,0.615,hmtSum.GetMarkerStyle())
        marker2.SetNDC()
        marker2.SetMarkerColor(hmtSum.GetMarkerColor())
        marker2.SetMarkerSize(0.9*hmtSum.GetMarkerSize())
        marker2.Draw()
        
        tex3 = ROOT.TLatex(xpos2,0.88,"Inverted #tau isolation")
        tex3.SetNDC()
        tex3.SetTextSize(20)
        tex3.Draw()
        
        tex5 = ROOT.TLatex(0.5,0.8,"MET > 70 GeV")
        tex5.SetNDC()
        tex5.SetTextSize(20)
        #    tex5.Draw()
        
        if(topmass):
            tex5 = ROOT.TLatex(0.5,0.8,"With top mass cut")
            tex5.SetNDC()
            tex5.SetTextSize(20)
            tex5.Draw()
  
        if(deltaPhi130):
            tex5 = ROOT.TLatex(0.5,0.8,"#Delta#phi(#tau jet, MET) < 130^{o}")
            tex5.SetNDC()
            tex5.SetTextSize(20)
            tex5.Draw()
        if(btagFactorisation):
            tex5 = ROOT.TLatex(0.5,0.8,"Factorised b tagging")
            tex5.SetNDC()
            tex5.SetTextSize(20)
            tex5.Draw()
 
        tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       5.05 fb^{-1}       CMS Preliminary ")
        tex4.SetNDC()
        tex4.SetTextSize(20)
        tex4.Draw()
            
        if deltaPhi130 or topmass or btagFactorisation:            
            hmtSum.GetYaxis().SetTitle("Events / 10 GeV/c^{2}")
            #    hmt.GetYaxis().SetTitleSize(20.0)
            hmtSum.GetYaxis().SetTitleOffset(1.5)
            hmtSum.GetXaxis().SetTitle("m_{T}(#tau jet, MET) (GeV/c^{2})")
        if(deltaPhiDistribution):
            hmtSum.GetXaxis().SetTitle("#Delta#phi(#tau jet, MET) (^{o})")
            hmtSum.GetYaxis().SetTitle("Events / 10^{o}")

        if(numberOfBjets):
            hmtSum.GetXaxis().SetTitle("Number of B-tagged jets")
            hmtSum.GetYaxis().SetTitle("Events")
            canvas31.Print("numberOfBjetsInverted.png")
            canvas31.Print("numberOfBjetsInverted.C") 
        #    canvas3.Print("mtInverted.png")
        #    canvas3.Print("mtInverted.C")    
        #    canvas3.Print("mtInverted_Met70_log.png")
        #    canvas3.Print("mtInverted_Met70_log.C")
        
        if(btagFactorisation):  
            canvas31.Print("mtInverted_btagFactorisation.png")
            canvas31.Print("mtInverted_btagFactorisation.C")        
        if(deltaPhi130):
            canvas31.Print("mtInverted_btag_dphi130.png")
            canvas31.Print("mtInverted_btag_dphi130.C")
        if(topmass):
            canvas31.Print("mtInverted_btag_topmass.png")
            canvas31.Print("mtInverted_btag_topmass.C")  
        if (deltaPhiDistribution):
            canvas31.Print("deltaPhiInverted_btag.png")           
        if (HiggsMass):
            canvas31.Print("HiggsMass_dphi160.png")     

    fName = os.path.join(sys.argv[1],"transverseMassQCDInverted.root")
    fOUT = ROOT.TFile.Open(fName, "RECREATE")
#    fOUT = ROOT.TFile.Open("transverseMassQCDInverted.root", "RECREATE")
#    hmtSum.SetDirectory(fOUT)
    hmt.SetDirectory(fOUT)
    fOUT.Write()
    fOUT.Close()

            
##  write histograms to file
def writeTransverseMass(datasets_lands):
    f = ROOT.TFile.Open(output, "RECREATE")
    hmtSum.SetDirectory(f)
    f.Write()
    f.Close()



    
def BtagEfficiencies(datasets):

    if True:
   ## b tag efficiencies before MET cut 
        met4050 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets4050")])
        met5060 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets5060")])
        met6070 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets6070")])
        met7080 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets7080")])
        met80100 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets80100")])
        met100120 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets100120")])
        if lastPtBin150: 
            met120150 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets120150")])
            met150 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets150")])
        if lastPtBin120:
            met120 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets120")])
        met = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets")])

        
        hmet4050 = met4050.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdJets4050")
        hmet5060 = met5060.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdJets5060")
        hmet6070 = met6070.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdJets6070")
        hmet7080 = met7080.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdJets7080")
        hmet80100 = met80100.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdJets80100")
        hmet100120 = met100120.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdJets100120")
        hmet120 = met120.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdJets120")
        if lastPtBin150:
            hmet120150 = met120150.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdBtag120150")
            hmet150 = met150.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdBtag150")
        if lastPtBin120:
            hmet120 = met120.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdBtag120")
        hmet = met.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdJets")
        
        met4050b = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdBtag4050")])
        met5060b = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdBtag5060")])
        met6070b = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdBtag6070")])
        met7080b = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdBtag7080")])
        met80100b = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdBtag80100")])
        met100120b = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdBtag100120")])
        if lastPtBin150: 
            met120150b = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdBtag120150")])
            met150b = bplots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdBtag150")])
        if lastPtBin120: 
            met120b = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdBtag120")])
        metb = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdBtag")])
               
        
        hmet4050b = met4050b.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdBtag4050")
        hmet5060b = met5060b.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdBtag5060")
        hmet6070b = met6070b.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdBtag6070")
        hmet7080b = met7080b.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdBtag7080")
        hmet80100b = met80100b.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdBtag80100")
        hmet100120b = met100120b.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdBtag100120")
        hmet120b = met120b.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdBtag120")
        if lastPtBin150:
            hmet120150b = met120150b.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdBtag120150")
            hmet150b = met150b.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdBtag150")
        if lastPtBin120:
            hmet120b = met120b.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdBtag120")
        hmetb = metb.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdBtag")

    if False:
   ## b tag efficiencies after MET cut 
        met4050 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdJet4050")])
        met5060 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdJet5060")])
        met6070 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdJet6070")])
        met7080 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdJet7080")])
        met80100 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdJet80100")])
        met100120 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdJet100120")])
        if lastPtBin150: 
            met120150 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdJet120150")])
            met150 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdJet150")])
        if lastPtBin120:
            met120 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdJet120")])
        met = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdJet")])

        
        hmet4050 = met4050.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJet4050")
        hmet5060 = met5060.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJet5060")
        hmet6070 = met6070.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJet6070")
        hmet7080 = met7080.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJet7080")
        hmet80100 = met80100.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJet80100")
        hmet100120 = met100120.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJet100120")
        if lastPtBin150:
            hmet120150 = met120150.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdBtag120150")
            hmet150 = met150.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdBtag150")
        if lastPtBin120:
            hmet120 = met120.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdBtag120")
        hmet = met.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJet")
    
        met4050b = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdBtag4050")])
        met5060b = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdBtag5060")])
        met6070b = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdBtag6070")])
        met7080b = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdBtag7080")])
        met80100b = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdBtag80100")])
        met100120b = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdBtag100120")])
        if lastPtBin150: 
            met120150b = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdBtag120150")])
            met150b = bplots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdBtag150")])
        if lastPtBin120: 
            met120b = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdBtag120")])
        metb = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdBtag")])
               
        
        hmet4050b = met4050b.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdBtag4050")
        hmet5060b = met5060b.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdBtag5060")
        hmet6070b = met6070b.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdBtag6070")
        hmet7080b = met7080b.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdBtag7080")
        hmet80100b = met80100b.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdBtag80100")
        hmet100120b = met100120b.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdBtag100120")
        if lastPtBin150:
            hmet120150b = met120150b.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdBtag120150")
            hmet150b = met150b.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdBtag150")
        if lastPtBin120:
            hmet120b = met120b.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdBtag120")
        hmetb = metb.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdBtag")


    
    p4050 = 0
    p5060 = 0
    p6070 = 0
    p7080 = 0
    p80100 = 0
    p100120 = 0
    p120 = 0
    p150 = 0
    phmet = 0
    p120150 = 0
    er4050 = 0
    er5060 = 0
    er6070 = 0
    er7080 = 0
    er80100 = 0
    er100120 = 0
    er120 = 0
    er150 = 0
    er120150 = 0
    erphmet = 0
    print "btag efficiencies:"  
    if hmet4050.Integral() > 0:
        p4050 = hmet4050b.Integral()/hmet4050.Integral()
        er4050 = sqrt(p4050*(1+p4050)/hmet4050.Integral())
        print "efficiency 4050  = ",hmet4050b.Integral()/hmet4050.Integral(), " error ",er4050
    if hmet5060.Integral() > 0:
        p5060 = hmet5060b.Integral()/hmet5060.Integral()
        er5060 = sqrt(p5060*(1+p5060)/hmet5060.Integral())
        print "efficiency 5060  = ",hmet5060b.Integral()/hmet5060.Integral(), " error ",er5060
    if hmet6070.Integral() > 0:
        p6070 = hmet6070b.Integral()/hmet6070.Integral()
        er6070 = sqrt(p6070*(1+p6070)/hmet6070.Integral()) 
        print "efficiency 6070  = ",hmet6070b.Integral()/hmet6070.Integral(), " error ",er6070
    if hmet7080.Integral() > 0:
        p7080 = hmet7080b.Integral()/hmet7080.Integral()
        er7080 = sqrt(p7080*(1+p7080)/hmet7080.Integral())
        print "efficiency 7080  = ",hmet7080b.Integral()/hmet7080.Integral(), " error ",er7080
    if hmet80100.Integral() > 0:
        p80100 = hmet80100b.Integral()/hmet80100.Integral()
        er80100 = sqrt(p80100*(1+p80100)/hmet80100.Integral())
        print "efficiency 80100  = ",hmet80100b.Integral()/hmet80100.Integral(), " error ",er80100
    if hmet100120.Integral() > 0:
        p100120 = hmet100120b.Integral()/hmet100120.Integral()
        er100120 = sqrt(p100120*(1+p100120)/hmet100120.Integral())
        print "efficiency 100120  = ",hmet100120b.Integral()/hmet100120.Integral(), " error ",er100120
    if lastPtBin150:
        if hmet120150.Integral() > 0:
            p120150 = met120150b.Integral()/met120150.Integral()
            er120150 = sqrt(p120150*(1+p120150)/hmet120150.Integral())
            print "efficiency 120150  = ",hmet120150b.Integral()/hmet120150.Integral(), " error ",er120150
        if hmet150.Integral() > 0:
            p150 = hmet150b.Integral()/hmet150.Integral()
            er150 = sqrt(p150*(1+p150)/hmet150.Integral())
            print "efficiency 150  = ",hmet150b.Integral()/hmet150.Integral(), " error ",er150            
    if lastPtBin120: 
        if hmet120.Integral() > 0:
            p120 = hmet120b.Integral()/hmet120.Integral()
            er120 = sqrt(p120*(1+p120)/hmet120.Integral())
            print "efficiency 120  = ",hmet120b.Integral()/hmet120.Integral(), " error ",er120
    if hmet.Integral() > 0:
        phmet = hmetb.Integral()/hmet.Integral()
        erphmet = sqrt(phmet*(1+phmet)/hmet.Integral()) 
        print "efficiency inclusive  = ",hmetb.Integral()/hmet.Integral(), hmet.Integral(), hmetb.Integral()
 

    fOUT = open("btaggingFactors","w")
    
#    now = datetime.datetime.now()
    
#    fOUT.write("# Generated on %s\n"%now.ctime())
    fOUT.write("# by %s\n"%os.path.basename(sys.argv[0]))
    fOUT.write("\n")
    fOUT.write("btaggingFactors = {\n")
     

    cEff = TCanvas ("QCDMeasurement", "QCDMeasurement", 1)
    cEff.cd()

### Declare arrays with the QCD pT bins
    if lastPtBin150:
        qcdBin  = array("d",[45, 55, 65, 75, 90, 110, 135, 160])
        qcdBin_down = array("d",[5, 5, 5, 5, 10, 10 , 15, 35])
        qcdBin_up  = array("d",[5, 5, 5, 5, 10, 10 ,15, 50])
        effArray = array("d",[p4050, p5060, p6070, p7080, p80100, p100120, p120150, p150])
        labels = ["4050", "5060", "6070", "7080", "80100", "100120", "120150", "150"]
        effArray_errDown = array("d",[er4050, er5060, er6070, er7080, er80100, er100120, er120150, er150])
        effArray_errUp = array("d",[er4050, er5060, er6070, er7080, er80100, er100120, er120150, er150])
    if lastPtBin120:
        qcdBin  = array("d",[45, 55, 65, 75, 90, 110, 150])
        qcdBin_down = array("d",[5, 5, 5, 5, 10, 10 ,30])
        qcdBin_up  = array("d",[5, 5, 5, 5, 10, 10 ,50])
        effArray = array("d",[p4050, p5060, p6070, p7080, p80100, p100120, p120])
        labels = ["4050", "5060", "6070", "7080", "80100", "100120", "120"]
        effArray_errDown = array("d",[er4050, er5060, er6070, er7080, er80100, er100120, er120])
        effArray_errUp = array("d",[er4050, er5060, er6070, er7080, er80100, er100120,  er120])

    i = 0
    while i < len(effArray):
        line = "    \"" + labels[i] + "\": " + str(effArray[i])
        if i < len(effArray) - 1:
            line += ","
        line += "\n"
        fOUT.write(line)
        i = i + 1
        
    fOUT.write("}\n")
    fOUT.close()
    print "B-tagging efficiensies written in file","btaggingFactors"



    gROOT.LoadMacro("MyGraph.cxx");  
### Create and customise TGraph 
    graph = TGraphAsymmErrors(7, qcdBin, effArray, qcdBin_down,  qcdBin_up, effArray_errDown, effArray_errUp)
    graph.SetMaximum(0.2)
    graph.SetMinimum(0.09)
    graph.SetMarkerStyle(kFullCircle)
    graph.SetMarkerColor(kBlue)

    graph.SetMarkerSize(1)
    graph.GetYaxis().SetTitle("b-tagging efficiency")
    graph.GetXaxis().SetTitle("p_{T}^{#tau jet} [GeV/c]")
### Re-draw graph and update canvas and gPad
    graph.Draw("AP")
    
    tex4 = ROOT.TLatex(0.2,0.955,"7 TeV              5.05 fb^{-1}             CMS preliminary")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    tex1 = ROOT.TLatex(0.6,0.85,"Inverted #tau jet isolation")
    tex1.SetNDC()
    tex1.SetTextSize(20)
    tex1.Draw()
    tex2 = ROOT.TLatex(0.35,0.3,"at least 3 jets")
    tex2.SetNDC()
    tex2.SetTextSize(20)
#    tex2.Draw()

    xpos = 0.5
    tex3 = ROOT.TLatex(xpos+0.05,0.75,"jet selection")
    tex3.SetNDC()
    tex3.SetTextSize(23)
    tex3.Draw()    
    marker3 = ROOT.TMarker(xpos,0.765,graph.GetMarkerStyle())
    marker3.SetNDC()
    marker3.SetMarkerColor(graph.GetMarkerColor())
    marker3.SetMarkerSize(0.9*graph.GetMarkerSize())
    marker3.Draw()
        
    cEff.Update()
    cEff.SaveAs("btagEfficiency.png")
    cEff.SaveAs("btagEfficiency.C")
#######################################################################    


def purityJets(datasets):   
    met4050 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets4050")])
    met5060 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets5060")])
    met6070 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets6070")])
    met7080 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets7080")])
    met80100 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets80100")])
    met100120 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets100120")])
    if lastPtBin150: 
        met120150 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets120150")])
        met150 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets150")])
    if lastPtBin120: 
        met120 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets120")])
    met = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets")])
    met.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
        
    hmet4050 = met4050.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdJets4050")
    hmet5060 = met5060.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdJets5060")
    hmet6070 = met6070.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdJets6070")
    hmet7080 = met7080.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdJets7080")
    hmet80100 = met80100.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdJets80100")
    hmet100120 = met100120.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdJets100120")
    hmet120 = met120.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdJets120")
    hmet = met.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdJets")
    
    met4050b = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets4050")])
    met5060b = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets5060")])
    met6070b = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets6070")])
    met7080b = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets7080")])
    met80100b = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets80100")])
    met100120b = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets100120")])
    if lastPtBin150: 
        met120150b = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets120150")])
        met150b = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets150")])
    if lastPtBin120: 
        met120b = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets120")])
    metb = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets")])

    
    met4050b.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())    
    met5060b.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    met6070b.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    met7080b.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    met80100b.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    met100120b.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    metb.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())    
    if lastPtBin150: 
        met120150b.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        met150b.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    if lastPtBin120:         
        met120b.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
               
    metb.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
     
    hmet4050b = met4050b.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MET_InvertedTauIdJets4050")
    hmet5060b = met5060b.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MET_InvertedTauIdJets5060")
    hmet6070b = met6070b.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MET_InvertedTauIdJets6070")
    hmet7080b = met7080b.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MET_InvertedTauIdJets7080")
    hmet80100b = met80100b.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MET_InvertedTauIdJets80100")
    hmet100120b = met100120b.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MET_InvertedTauIdJets100120")
    hmet120b = met120b.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MET_InvertedTauIdJets120")
    hmetb = metb.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MET_InvertedTauIdJets")


####### Purity as a function of MET

    canvas55 = ROOT.TCanvas("canvas55","",500,500)
    hmet.SetMarkerColor(1)
    hmet.SetMarkerSize(1)
    hmet.SetMarkerStyle(27)
    hmet.SetFillColor(1)
    #    hmet.Draw()
    hmet_QCD = hmet.Clone("QCD")
    hmet_QCD.Add(hmetb,-1)
    hmet_QCD.Divide(hmet)
    hmet_QCD.SetMarkerColor(2)
    hmet_QCD.SetMarkerSize(1)
    hmet_QCD.SetMarkerStyle(20)
    hmet_QCD.Draw()
    hmet.GetYaxis().SetTitle("Events")
    hmet.GetXaxis().SetTitle("m_{T}(#tau jet, MET) (GeV/c^{2})")
    canvas55.Print("Met_purity_jets.png")

###########

    
    p4050 = 0
    p5060 = 0
    p6070 = 0
    p7080 = 0
    p80100 = 0
    p100120 = 0
    p120 = 0
    er4050 = 0
    er5060 = 0
    er6070 = 0
    er7080 = 0
    er80100 = 0
    er100120 = 0
    er120 = 0
    print "Purity after jets:"  
    if hmet4050.Integral() > 0:
        p4050 = (hmet4050.Integral() - hmet4050b.Integral())/hmet4050.Integral()
        er4050 = sqrt(p4050*(1+p4050)/hmet4050.Integral())
        print "purity 4050  = ",(hmet4050.Integral() - hmet4050b.Integral())/hmet4050.Integral(), " error ",er4050
    if hmet5060.Integral() > 0:
        p5060 = (hmet5060.Integral() - hmet5060b.Integral())/hmet5060.Integral()
        er5060 = sqrt(p5060*(1+p5060)/hmet5060.Integral())
        print "purity 5060  = ",(hmet5060.Integral() - hmet5060b.Integral())/hmet5060.Integral(), " error ",er5060
    if hmet6070.Integral() > 0:
        p6070 = (hmet6070.Integral() - hmet6070b.Integral())/hmet6070.Integral()
        er6070 = sqrt(p6070*(1+p6070)/hmet6070.Integral()) 
        print "purity 6070  = ",(hmet6070.Integral() - hmet6070b.Integral())/hmet6070.Integral(), " error ",er6070
    if hmet7080.Integral() > 0:
        p7080 = (hmet7080.Integral() - hmet7080b.Integral())/hmet7080.Integral()
        er7080 = sqrt(p7080*(1+p7080)/hmet7080.Integral())
        print "purity 7080  = ",(hmet7080.Integral() - hmet7080b.Integral())/hmet7080.Integral(), " error ",er7080
    if hmet80100.Integral() > 0:
        p80100 = (hmet80100.Integral() - hmet80100b.Integral())/hmet80100.Integral()
        er80100 = sqrt(p80100*(1+p80100)/hmet80100.Integral())
        print "purity 80100  = ",(hmet80100.Integral()- hmet80100b.Integral())/hmet80100.Integral(), " error ",er80100
    if hmet100120.Integral() > 0:
        p100120 = (hmet100120.Integral() - hmet100120b.Integral())/hmet100120.Integral()
        er100120 = sqrt(p100120*(1+p100120)/hmet100120.Integral())
        print "purity 100120  = ",(hmet100120.Integral() - hmet100120b.Integral())/hmet100120.Integral(), " error ",er100120
    if hmet120.Integral() > 0:
        p120 = (hmet120.Integral() - hmet120b.Integral())/hmet120.Integral()
        er120 = sqrt(p120*(1+p120)/hmet120.Integral())
        print "purity 120  = ",(hmet120.Integral() - hmet120b.Integral())/hmet120.Integral(), " error ",er120
    if hmet.Integral() > 0:
        print "purity inclusive  = ",(hmet.Integral() - hmetb.Integral())/hmet.Integral(), hmet.Integral(), hmetb.Integral()



### Create TCanvas and TGraph with Asymmetric Error Bars using Bayesian Statistical Tools
    cEff = TCanvas ("QCDMeasurement", "QCDMeasurement", 1)
    cEff.cd()

### Declare arrays with the QCD pT bins 
    qcdBin  = array("d",[45, 55, 65, 75, 90, 110, 150])
    qcdBin_down = array("d",[5, 5, 5, 5, 10, 10 ,30])
    qcdBin_up  = array("d",[5, 5, 5, 5, 10, 10 ,50])
    effArray = array("d",[p4050, p5060, p6070, p7080, p80100, p100120, p120])  
    effArray_errDown = array("d",[er4050, er5060, er6070, er7080, er80100, er100120, er120])
    effArray_errUp = array("d",[er4050, er5060, er6070, er7080, er80100, er100120, er120])

    gROOT.LoadMacro("MyGraph.cxx");  
### Create and customise TGraph 
    graph = TGraphAsymmErrors(7, qcdBin, effArray, qcdBin_down,  qcdBin_up, effArray_errDown, effArray_errUp)
    graph.SetMaximum(1.02)
    graph.SetMinimum(0.94)
    graph.SetMarkerStyle(kFullCircle)
    graph.SetMarkerColor(kRed)

    graph.SetMarkerSize(1)
    graph.GetYaxis().SetTitle("QCD purity")
    graph.GetXaxis().SetTitle("p_{T}^{#tau jet} [GeV/c]")
### Re-draw graph and update canvas and gPad
    graph.Draw("AP")
    tex4 = ROOT.TLatex(0.2,0.955,"7 TeV              5.05 fb^{-1}             CMS preliminary")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    tex4 = ROOT.TLatex(0.2,0.955,"7 TeV              5.05 fb^{-1}             CMS preliminary")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    tex1 = ROOT.TLatex(0.35,0.35,"Inverted #tau jet isolation")
    tex1.SetNDC()
    tex1.SetTextSize(20)
    tex1.Draw()
    tex2 = ROOT.TLatex(0.35,0.3,"at least 3 jets")
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw()    
 
    cEff.Update()
    cEff.SaveAs("purityJets.png")
    cEff.SaveAs("purityJets.C")
############################################3


def purityBveto(datasets):   
    met4050 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdBveto4050")])
    met5060 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdBveto5060")])
    met6070 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdBveto6070")])
    met7080 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdBveto7080")])
    met80100 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdBveto80100")])
    met100120 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdBveto100120")])
    if lastPtBin150: 
        met120150 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdBveto120150")])
        met150 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdBveto150")])
    if lastPtBin120: 
        met120 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdBveto120")])
    met = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdBveto")])
    met.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
        
    hmet4050 = met4050.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdBveto4050")
    hmet5060 = met5060.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdBveto5060")
    hmet6070 = met6070.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdBveto6070")
    hmet7080 = met7080.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdBveto7080")
    hmet80100 = met80100.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdBveto80100")
    hmet100120 = met100120.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdBveto100120")
    hmet120 = met120.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdBveto120")
    hmet = met.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdBveto")

    
    met4050b = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MET_InvertedTauIdBveto4050")])
    met5060b = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MET_InvertedTauIdBveto5060")])
    met6070b = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MET_InvertedTauIdBveto6070")])
    met7080b = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MET_InvertedTauIdBveto7080")])
    met80100b = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MET_InvertedTauIdBveto80100")])
    met100120b = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MET_InvertedTauIdBveto100120")])
    if lastPtBin150: 
        met120150b = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MET_InvertedTauIdBveto120150")])
        met150b = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MET_InvertedTauIdBveto150")])
    if lastPtBin120: 
        met120b = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MET_InvertedTauIdBveto120")])
    metb = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MET_InvertedTauIdBveto")])

    met4050b.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())    
    met5060b.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    met6070b.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    met7080b.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    met80100b.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    met100120b.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    metb.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())    
    if lastPtBin150: 
        met120150b.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        met150b.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    if lastPtBin120:         
        met120b.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    metb.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))        
  
        
    hmet4050b = met4050b.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MET_InvertedTauIdBveto4050")
    hmet5060b = met5060b.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MET_InvertedTauIdBveto5060")
    hmet6070b = met6070b.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MET_InvertedTauIdBveto6070")
    hmet7080b = met7080b.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MET_InvertedTauIdBveto7080")
    hmet80100b = met80100b.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MET_InvertedTauIdBveto80100")
    hmet100120b = met100120b.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MET_InvertedTauIdBveto100120")
    hmet120b = met120b.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MET_InvertedTauIdBveto120")
    hmetb = metb.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MET_InvertedTauIdBveto")

 ####### Purity as a function of MET

    canvas56 = ROOT.TCanvas("canvas56","",500,500)
    hmet.SetMarkerColor(1)
    hmet.SetMarkerSize(1)
    hmet.SetMarkerStyle(27)
    hmet.SetFillColor(1)
    #    hmet.Draw()
    hmet_QCD = hmet.Clone("QCD")
    hmet_QCD.Add(hmetb,-1)
    hmet_QCD.Divide(hmet)
    hmet_QCD.SetMarkerColor(4)
    hmet_QCD.SetMarkerSize(1)
    hmet_QCD.SetMarkerStyle(20)
    hmet_QCD.Draw()
    hmet.GetYaxis().SetTitle("Events")
    hmet.GetXaxis().SetTitle("MET (GeV)")
    canvas56.Print("Met_purity_bveto.png")            
###########################

    
    p4050 = 0
    p5060 = 0
    p6070 = 0
    p7080 = 0
    p80100 = 0
    p100120 = 0
    p120 = 0
    er4050 = 0
    er5060 = 0
    er6070 = 0
    er7080 = 0
    er80100 = 0
    er100120 = 0
    er120 = 0
    print "Purity after jets+bveto:"  
    if hmet4050.Integral() > 0:
        p4050 = (hmet4050.Integral() - hmet4050b.Integral())/hmet4050.Integral()
        er4050 = sqrt(p4050*(1+p4050)/hmet4050.Integral())
        print "purity 4050  = ",(hmet4050.Integral() - hmet4050b.Integral())/hmet4050.Integral(), " error ",er4050
    if hmet5060.Integral() > 0:
        p5060 = (hmet5060.Integral() - hmet5060b.Integral())/hmet5060.Integral()
        er5060 = sqrt(p5060*(1+p5060)/hmet5060.Integral())
        print "purity 5060  = ",(hmet5060.Integral() - hmet5060b.Integral())/hmet5060.Integral(), " error ",er5060
    if hmet6070.Integral() > 0:
        p6070 = (hmet6070.Integral() - hmet6070b.Integral())/hmet6070.Integral()
        er6070 = sqrt(p6070*(1+p6070)/hmet6070.Integral()) 
        print "purity 6070  = ",(hmet6070.Integral() - hmet6070b.Integral())/hmet6070.Integral(), " error ",er6070
    if hmet7080.Integral() > 0:
        p7080 = (hmet7080.Integral() - hmet7080b.Integral())/hmet7080.Integral()
        er7080 = sqrt(p7080*(1+p7080)/hmet7080.Integral())
        print "purity 7080  = ",(hmet7080.Integral() - hmet7080b.Integral())/hmet7080.Integral(), " error ",er7080
    if hmet80100.Integral() > 0:
        p80100 = (hmet80100.Integral() - hmet80100b.Integral())/hmet80100.Integral()
        er80100 = sqrt(p80100*(1+p80100)/hmet80100.Integral())
        print "purity 80100  = ",(hmet80100.Integral()- hmet80100b.Integral())/hmet80100.Integral(), " error ",er80100
    if hmet100120.Integral() > 0:
        p100120 = (hmet100120.Integral() - hmet100120b.Integral())/hmet100120.Integral()
        er100120 = sqrt(p100120*(1+p100120)/hmet100120.Integral())
        print "purity 100120  = ",(hmet100120.Integral() - hmet100120b.Integral())/hmet100120.Integral(), " error ",er100120
    if hmet120.Integral() > 0:
        p120 = (hmet120.Integral() - hmet120b.Integral())/hmet120.Integral()
        er120 = sqrt(p120*(1+p120)/hmet120.Integral())
        print "purity 120  = ",(hmet120.Integral() - hmet120b.Integral())/hmet120.Integral(), " error ",er120
    if hmet.Integral() > 0:
        print "purity inclusive  = ",(hmet.Integral() - hmetb.Integral())/hmet.Integral(), hmet.Integral(), hmetb.Integral()

### Create TCanvas and TGraph with Asymmetric Error Bars using Bayesian Statistical Tools
    cEff = TCanvas ("QCDMeasurement", "QCDMeasurement", 1)
    cEff.cd()

### Declare arrays with the QCD pT bins 
    qcdBin  = array("d",[45, 55, 65, 75, 90, 110, 150])
    qcdBin_down = array("d",[5, 5, 5, 5, 10, 10 ,30])
    qcdBin_up  = array("d",[5, 5, 5, 5, 10, 10 ,50])
    effArray = array("d",[p4050, p5060, p6070, p7080, p80100, p100120, p120])  
    effArray_errDown = array("d",[er4050, er5060, er6070, er7080, er80100, er100120, er120])
    effArray_errUp = array("d",[er4050, er5060, er6070, er7080, er80100, er100120, er120])

    gROOT.LoadMacro("MyGraph.cxx");  
### Create and customise TGraph 
    graph = TGraphAsymmErrors(7, qcdBin, effArray, qcdBin_down,  qcdBin_up, effArray_errDown, effArray_errUp)
    graph.SetMaximum(1.02)
    graph.SetMinimum(0.94)
    graph.SetMarkerStyle(kFullCircle)
    graph.SetMarkerColor(kRed+1)
    graph.SetMarkerSize(1)
    graph.GetYaxis().SetTitle("QCD purity")
    graph.GetXaxis().SetTitle("p_{T}^{#tau jet} [GeV/c]")
### Re-draw graph and update canvas and gPad
    graph.Draw("AP")

    tex4 = ROOT.TLatex(0.2,0.955,"7 TeV              5.05 fb^{-1}             CMS preliminary")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    tex1 = ROOT.TLatex(0.35,0.35,"Inverted #tau jet isolation")
    tex1.SetNDC()
    tex1.SetTextSize(20)
    tex1.Draw()
    tex2 = ROOT.TLatex(0.35,0.3,"at least 3 jets and b-jet veto")
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw()    


    cEff.Update()
    cEff.SaveAs("purityBveto.png")
    cEff.SaveAs("purityBveto.C")

#########################################################################    
        
def purityBtag(datasets):  
    met4050 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdBtag4050")])
    met5060 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdBtag5060")])
    met6070 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdBtag6070")])
    met7080 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdBtag7080")])
    met80100 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdBtag80100")])
    met100120 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdBtag100120")])
    if lastPtBin150: 
        met120150 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdBtag120150")])
        met150 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdBtag150")])
    if lastPtBin120: 
        met120 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdBtag120")])
    met = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdBtag")])
    met.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))   
        
    hmet4050 = met4050.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdBtag4050")
    hmet5060 = met5060.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdBtag5060")
    hmet6070 = met6070.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdBtag6070")
    hmet7080 = met7080.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdBtag7080")
    hmet80100 = met80100.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdBtag80100")
    hmet100120 = met100120.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdBtag100120")
    hmet120 = met120.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdBtag120")
    hmet = met.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdBtag")
    
    met4050b = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MTInvertedTauIdBtag4050")])
    met5060b = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MTInvertedTauIdBtag5060")])
    met6070b = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MTInvertedTauIdBtag6070")])
    met7080b = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MTInvertedTauIdBtag7080")])
    met80100b = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MTInvertedTauIdBtag80100")])
    met100120b = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MTInvertedTauIdBtag100120")])
    if lastPtBin150: 
        met120150b = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MTInvertedTauIdBtag120150")])
        met150b = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MTInvertedTauIdBtag150")])
    if lastPtBin120: 
        met120b = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MTInvertedTauIdBtag120")])
    metb = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MTInvertedTauIdBtag")])

    met4050b.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())    
    met5060b.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    met6070b.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    met7080b.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    met80100b.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    met100120b.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    metb.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())    
    if lastPtBin150: 
        met120150b.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        met150b.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    if lastPtBin120:         
        met120b.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    metb.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))                 
        
    hmet4050b = met4050b.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MTInvertedTauIdBtag4050")
    hmet5060b = met5060b.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MTInvertedTauIdBtag5060")
    hmet6070b = met6070b.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MTInvertedTauIdBtag6070")
    hmet7080b = met7080b.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MTInvertedTauIdBtag7080")
    hmet80100b = met80100b.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MTInvertedTauIdBtag80100")
    hmet100120b = met100120b.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MTInvertedTauIdBtag100120")
    hmet120b = met120b.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MTInvertedTauIdBtag120")
    hmetb = metb.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MTInvertedTauIdBtag")
    
 ####### Purity as a function of MET

    canvas57 = ROOT.TCanvas("canvas57","",500,500)
    hmet.SetMarkerColor(1)
    hmet.SetMarkerSize(1)
    hmet.SetMarkerStyle(27)
    hmet.SetFillColor(1)
    #    hmet.Draw()
    hmet_QCD = hmet.Clone("QCD")
    hmet_QCD.Add(hmetb,-1)
    hmet_QCD.Divide(hmet)
    hmet_QCD.SetMarkerColor(4)
    hmet_QCD.SetMarkerSize(1)
    hmet_QCD.SetMarkerStyle(20)
    hmet_QCD.Draw()
    hmet.GetYaxis().SetTitle("Events")
    hmet.GetXaxis().SetTitle("MET (GeV)")
    canvas57.Print("Met_purity_btag.png")            
###########################
    
    print "Purity after MET+b tagging:"  
   

        
    p4050 = 0
    p5060 = 0
    p6070 = 0
    p7080 = 0
    p80100 = 0
    p100120 = 0
    p120 = 0
    er4050 = 0
    er5060 = 0
    er6070 = 0
    er7080 = 0
    er80100 = 0
    er100120 = 0
    er120 = 0
    if hmet4050.Integral() > 0:
        p4050 = (hmet4050.Integral() - hmet4050b.Integral())/hmet4050.Integral()
        er4050 = sqrt(p4050*(1+p4050)/hmet4050.Integral())
        print "purity 4050  = ",(hmet4050.Integral() - hmet4050b.Integral())/hmet4050.Integral(), " error ",er4050
    if hmet5060.Integral() > 0:
        p5060 = (hmet5060.Integral() - hmet5060b.Integral())/hmet5060.Integral()
        er5060 = sqrt(p5060*(1+p5060)/hmet5060.Integral())
        print "purity 5060  = ",(hmet5060.Integral() - hmet5060b.Integral())/hmet5060.Integral(), " error ",er5060
    if hmet6070.Integral() > 0:
        p6070 = (hmet6070.Integral() - hmet6070b.Integral())/hmet6070.Integral()
        er6070 = sqrt(p6070*(1+p6070)/hmet6070.Integral()) 
        print "purity 6070  = ",(hmet6070.Integral() - hmet6070b.Integral())/hmet6070.Integral(), " error ",er6070
    if hmet7080.Integral() > 0:
        p7080 = (hmet7080.Integral() - hmet7080b.Integral())/hmet7080.Integral()
        er7080 = sqrt(p7080*(1+p7080)/hmet7080.Integral())
        print "purity 7080  = ",(hmet7080.Integral() - hmet7080b.Integral())/hmet7080.Integral(), " error ",er7080
    if hmet80100.Integral() > 0:
        p80100 = (hmet80100.Integral() - hmet80100b.Integral())/hmet80100.Integral()
        er80100 = sqrt(p80100*(1+p80100)/hmet80100.Integral())
        print "purity 80100  = ",(hmet80100.Integral()- hmet80100b.Integral())/hmet80100.Integral(), " error ",er80100
    if hmet100120.Integral() > 0:
        p100120 = (hmet100120.Integral() - hmet100120b.Integral())/hmet100120.Integral()
        er100120 = sqrt(p100120*(1+p100120)/hmet100120.Integral())
        print "purity 100120  = ",(hmet100120.Integral() - hmet100120b.Integral())/hmet100120.Integral(), " error ",er100120
    if hmet120.Integral() > 0:
        p120 = (hmet120.Integral() - hmet120b.Integral())/hmet120.Integral()
        er120 = sqrt(p120*(1+p120)/hmet120.Integral())
        print "purity 120  = ",(hmet120.Integral() - hmet120b.Integral())/hmet120.Integral(), " error ",er120
    if hmet.Integral() > 0:
        print "purity inclusive  = ",(hmet.Integral() - hmetb.Integral())/hmet.Integral(), hmet.Integral(), hmetb.Integral()



### Create TCanvas and TGraph with Asymmetric Error Bars using Bayesian Statistical Tools
    cEff = TCanvas ("QCDMeasurement", "QCDMeasurement", 1)
    cEff.cd()

### Declare arrays with the QCD pT bins 
    qcdBin  = array("d",[45, 55, 65, 75, 90, 110, 150])
    qcdBin_down = array("d",[5, 5, 5, 5, 10, 10 ,30])
    qcdBin_up  = array("d",[5, 5, 5, 5, 10, 10 ,50])
    effArray = array("d",[p4050, p5060, p6070, p7080, p80100, p100120, p120])  
    effArray_errDown = array("d",[er4050, er5060, er6070, er7080, er80100, er100120, er120])
    effArray_errUp = array("d",[er4050, er5060, er6070, er7080, er80100, er100120, er120])

    
### Create and customise TGraph 
    graph = TGraphAsymmErrors(7, qcdBin, effArray, qcdBin_down,  qcdBin_up, effArray_errDown, effArray_errUp)
    graph.SetMaximum(1.05)
    graph.SetMinimum(0.5)
    graph.SetMarkerStyle(kFullCircle)
    graph.SetMarkerColor(kBlue)
    graph.SetMarkerSize(1)
    graph.GetYaxis().SetTitle("QCD purity")
    graph.GetXaxis().SetTitle("p_{T}^{#tau jet} [GeV/c]")
### Re-draw graph and update canvas and gPad
    graph.Draw("AP")
    tex4 = ROOT.TLatex(0.2,0.955,"7 TeV              5.05 fb^{-1}             CMS preliminary")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    tex1 = ROOT.TLatex(0.35,0.35,"Inverted #tau jet isolation")
    tex1.SetNDC()
    tex1.SetTextSize(20)
    tex1.Draw()
    tex2 = ROOT.TLatex(0.35,0.3,"at least 3 jets and b tagging")
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw()

    cEff.Update()
    cEff.SaveAs("purityBtag.png")


 
def purityDeltaPhi(datasets):  
    met4050 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdPhi4050")])
    met5060 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdPhi5060")])
    met6070 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdPhi6070")])
    met7080 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdPhi7080")])
    met80100 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdPhi80100")])
    met100120 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdPhi100120")])
    if lastPtBin150: 
        met120150 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdPhi120150")])
        met150 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdPhi150")])
    if lastPtBin120: 
        met120 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdPhi120")])
    met = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdPhi")])

        
    hmet4050 = met4050.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdPhi4050")
    hmet5060 = met5060.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdPhi5060")
    hmet6070 = met6070.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdPhi6070")
    hmet7080 = met7080.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdPhi7080")
    hmet80100 = met80100.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdPhi80100")
    hmet100120 = met100120.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdPhi100120")
    hmet120 = met120.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdPhi120")
    hmet = met.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdPhi")
    
    met4050b = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MTInvertedTauIdPhi4050")])
    met5060b = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MTInvertedTauIdPhi5060")])
    met6070b = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MTInvertedTauIdPhi6070")])
    met7080b = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MTInvertedTauIdPhi7080")])
    met80100b = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MTInvertedTauIdPhi80100")])
    met100120b = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MTInvertedTauIdPhi100120")])
    if lastPtBin150: 
        met120150b = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MTInvertedTauIdPhi120150")])
        met150b = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MTInvertedTauIdPhi150")])
    if lastPtBin120: 
        met120b = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MTInvertedTauIdPhi120")])
    metb = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(analysis+"/MTInvertedTauIdPhi")])

    met4050b.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())    
    met5060b.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    met6070b.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    met7080b.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    met80100b.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    met100120b.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    metb.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())    
    if lastPtBin150: 
        met120150b.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        met150b.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    if lastPtBin120:         
        met120b.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
               
        
    hmet4050b = met4050b.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MTInvertedTauIdPhi4050")
    hmet5060b = met5060b.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MTInvertedTauIdPhi5060")
    hmet6070b = met6070b.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MTInvertedTauIdPhi6070")
    hmet7080b = met7080b.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MTInvertedTauIdPhi7080")
    hmet80100b = met80100b.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MTInvertedTauIdPhi80100")
    hmet100120b = met100120b.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MTInvertedTauIdPhi100120")
    hmet120b = met120b.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MTInvertedTauIdPhi120")
    hmetb = metb.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MTInvertedTauIdPhi")
    
    print "Purity after MET + b tagging + deltaPhi:"  

    p4050 = 0
    p5060 = 0
    p6070 = 0
    p7080 = 0
    p80100 = 0
    p100120 = 0
    p120 = 0
    er4050 = 0
    er5060 = 0
    er6070 = 0
    er7080 = 0
    er80100 = 0
    er100120 = 0
    er120 = 0
    
    if hmet4050.Integral() > 0:
        p4050 = (hmet4050.Integral() - hmet4050b.Integral())/hmet4050.Integral()
        er4050 = sqrt(p4050*(1+p4050)/hmet4050.Integral())
        print "purity 4050  = ",(hmet4050.Integral() - hmet4050b.Integral())/hmet4050.Integral(), " error ",er4050
    if hmet5060.Integral() > 0:
        p5060 = (hmet5060.Integral() - hmet5060b.Integral())/hmet5060.Integral()
        er5060 = sqrt(p5060*(1+p5060)/hmet5060.Integral())
        print "purity 5060  = ",(hmet5060.Integral() - hmet5060b.Integral())/hmet5060.Integral(), " error ",er5060
    if hmet6070.Integral() > 0:
        p6070 = (hmet6070.Integral() - hmet6070b.Integral())/hmet6070.Integral()
        er6070 = sqrt(p6070*(1+p6070)/hmet6070.Integral()) 
        print "purity 6070  = ",(hmet6070.Integral() - hmet6070b.Integral())/hmet6070.Integral(), " error ",er6070
    if hmet7080.Integral() > 0:
        p7080 = (hmet7080.Integral() - hmet7080b.Integral())/hmet7080.Integral()
        er7080 = sqrt(p7080*(1+p7080)/hmet7080.Integral())
        print "purity 7080  = ",(hmet7080.Integral() - hmet7080b.Integral())/hmet7080.Integral(), " error ",er7080
    if hmet80100.Integral() > 0:
        p80100 = (hmet80100.Integral() - hmet80100b.Integral())/hmet80100.Integral()
        er80100 = sqrt(p80100*(1+p80100)/hmet80100.Integral())
        print "purity 80100  = ",(hmet80100.Integral()- hmet80100b.Integral())/hmet80100.Integral(), " error ",er80100
    if hmet100120.Integral() > 0:
        p100120 = (hmet100120.Integral() - hmet100120b.Integral())/hmet100120.Integral()
        er100120 = sqrt(p100120*(1+p100120)/hmet100120.Integral())
        print "purity 100120  = ",(hmet100120.Integral() - hmet100120b.Integral())/hmet100120.Integral(), " error ",er100120
    if hmet120.Integral() > 0:
        p120 = (hmet120.Integral() - hmet120b.Integral())/hmet120.Integral()
        er120 = sqrt(p120*(1+p120)/hmet120.Integral())
        print "purity 120  = ",(hmet120.Integral() - hmet120b.Integral())/hmet120.Integral(), " error ",er120
    if hmet.Integral() > 0:
        print "purity inclusive  = ",(hmet.Integral() - hmetb.Integral())/hmet.Integral(), hmet.Integral(), hmetb.Integral()



### Create TCanvas and TGraph with Asymmetric Error Bars using Bayesian Statistical Tools
    cEff = TCanvas ("QCDMeasurement", "QCDMeasurement", 1)
    cEff.cd()

### Declare arrays with the QCD pT bins 
    qcdBin  = array("d",[45, 55, 65, 75, 90, 110, 150])
    qcdBin_down = array("d",[5, 5, 5, 5, 10, 10 ,30])
    qcdBin_up  = array("d",[5, 5, 5, 5, 10, 10 ,50])
    effArray = array("d",[p4050, p5060, p6070, p7080, p80100, p100120, p120])  
    effArray_errDown = array("d",[er4050, er5060, er6070, er7080, er80100, er100120, er120])
    effArray_errUp = array("d",[er4050, er5060, er6070, er7080, er80100, er100120, er120])

    
### Create and customise TGraph 
    graph = TGraphAsymmErrors(7, qcdBin, effArray, qcdBin_down,  qcdBin_up, effArray_errDown, effArray_errUp)
    graph.SetMaximum(1.05)
    graph.SetMinimum(0.5)
    graph.SetMarkerStyle(kFullCircle)
    graph.SetMarkerColor(kGreen+2)
    graph.SetMarkerSize(1)
    graph.GetYaxis().SetTitle("QCD purity")
    graph.GetXaxis().SetTitle("p_{T}^{#tau jet} [GeV/c]")
### Re-draw graph and update canvas and gPad
    graph.Draw("AP")
    tex4 = ROOT.TLatex(0.2,0.955,"7 TeV              5.05 fb^{-1}             CMS preliminary")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    tex1 = ROOT.TLatex(0.35,0.3,"Inverted #tau jet isolation")
    tex1.SetNDC()
    tex1.SetTextSize(20)
    tex1.Draw()
    tex2 = ROOT.TLatex(0.35,0.25,"at least 3 jets, b tagging and #Delta#phi cut")
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw()

    cEff.Update()
    cEff.SaveAs("purityDphi.png")




def metRatio2(datasets):    

    metJets = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets")])
    metBveto = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdBveto")])
    metBtag = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdBtag")])
    metJets.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
    metBveto.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
    metBtag.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
    
    hmetJets = metJets.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdJets")
    hmetBveto = metBveto.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdBveto")
    hmetBtag = metBtag.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdBtag")
        
    iBin = 1
    nBins = hmetJets.GetNbinsX()

    while iBin < nBins:
        value1 = hmetJets.GetBinContent(iBin)
        value2 = hmetBveto.GetBinContent(iBin)
        value3 = hmetBtag.GetBinContent(iBin)
        
#        if value1 < 0:
#            h1.SetBinContent(iBin,0)
        print "bin  = ",iBin,"Met after jets  ",value1,"Met after b veto  ",value2,"Met after b tag  ",value3
        if value1 > 0:
            print "bin  = ",iBin,"Met after jets  ",value2/value1
        iBin = iBin + 1
 

        
          
def metComparison(datasets):
    met = plots.PlotBase([
        datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets4050"),
        datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets5060"),
        datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets6070"),
        datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets7080"),
        datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets80100"),
        datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets100120"),
        datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets120150"),
        datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets150")
        ])
    

#    mt.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    met._setLegendStyles()
    met._setLegendLabels()
    met.histoMgr.setHistoDrawStyleAll("P")
    rtauGen(met, "met_vs_pttau", rebin=10)       

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
        h.addStandardTexts()
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
        h.addStandardTexts()
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
    h.addStandardTexts(addLuminosityText=False)
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
    h.addStandardTexts(addLuminosityText=False)
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
    h.addStandardTexts(addLuminosityText=False)
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
    h.addStandardTexts(addLuminosityText=False)
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
