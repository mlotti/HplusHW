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
ROOT.gROOT.SetBatch(True)

from ROOT import *
import math
import sys
import copy
import re


import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect

# Configuration
analysis = "signalAnalysis"
#analysis = "signalOptimisation"
#analysis = "signalAnalysisJESMinus03eta02METMinus10"
#analysis = "EWKFakeTauAnalysisJESMinus03eta02METMinus10"
#analysis = "signalOptimisation/QCDAnalysisVariation_tauPt40_rtau0_btag2_METcut60_FakeMETCut0"
#analysis = "signalAnalysisTauSelectionHPSTightTauBased2"
#analysis = "signalAnalysisBtaggingTest2"
counters = analysis+"Counters/weighted"

treeDraw = dataset.TreeDraw(analysis+"/tree", weight="weightPileup*weightTrigger*weightPrescale")

#QCDfromData = True
QCDfromData = False
deltaPhi180 = False
deltaPhi160 = False
deltaPhi130 = True
btagging = False

# main function
def main():
    # Read the datasets
    datasets = dataset.getDatasetsFromMulticrabCfg(counters=counters)
    datasets.loadLuminosities()

    # Take QCD from data
    datasetsQCD = None

    if QCDfromData:

        datasetsQCD = dataset.getDatasetsFromMulticrabCfg(cfgfile="/home/rkinnune/signalAnalysis/CMSSW_4_2_8_patch2/src/HiggsAnalysis/HeavyChHiggsToTauNu/test/multicrab_111123_132128/multicrab.cfg", counters=counters)
        datasetsQCD.loadLuminosities()
        print "QCDfromData", QCDfromData
        datasetsQCD.mergeData()
        datasetsQCD.remove(datasetsQCD.getMCDatasetNames())
        datasetsQCD.rename("Data", "QCD")
    
#Rtau =0
#    datasetsSignal = dataset.getDatasetsFromMulticrabCfg(cfgfile="/home/rkinnune/signalAnalysis/CMSSW_4_2_5/src/HiggsAnalysis/HeavyChHiggsToTauNu/test/multicrab_110804_104313/multicrab.cfg", counters=counters)

#    datasetsSignal.selectAndReorder(["HplusTB_M200_Summer11"])
#    datasetsSignal = dataset.getDatasetsFromMulticrabCfg(cfgfile="/home/rkinnune/signalAnalysis/CMSSW_4_2_4_patch1/src/HiggsAnalysis/HeavyChHiggsToTauNu/test/multicrab_110622_112321/multicrab.cfg", counters=counters)
    #datasetsSignal = dataset.getDatasetsFromMulticrabCfg(cfgfile="/home/rkinnune/signalAnalysis/CMSSW_4_1_5/src/HiggsAnalysis/HeavyChHiggsToTauNu/test/Signal_v11f_scaledb_424/multicrab.cfg", counters=counters)

    #datasetsSignal.selectAndReorder(["TTToHplusBWB_M120_Summer11", "TTToHplusBHminusB_M120_Summer11"])
    #datasetsSignal.renameMany({"TTToHplusBWB_M120_Summer11" :"TTToHplusBWB_M120_Spring11",
    #                           "TTToHplusBHminusB_M120_Summer11": "TTToHplusBHminusB_M120_Spring11"})
    #datasets.extend(datasetsSignal)

    plots.mergeRenameReorderForDataMC(datasets)

    print "Int.Lumi",datasets.getDataset("Data").getLuminosity()

    # Remove signals other than M120
    datasets.remove(filter(lambda name: "TTToHplus" in name and not "M80" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "HplusTB" in name, datasets.getAllDatasetNames()))

    datasets_lands = datasets.deepCopy()

    # Set the signal cross sections to the ttbar for datasets for lands
    xsect.setHplusCrossSectionsToTop(datasets_lands)

    # Set the signal cross sections to a given BR(t->H), BR(h->taunu)
    xsect.setHplusCrossSectionsToBR(datasets, br_tH=0.05, br_Htaunu=1)

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
    # Create the plot objects and pass them to the formatting
    # functions to be formatted, drawn and saved to files


    deltaPhi2(plots.DataMCPlot(datasets, analysis+"/deltaPhi"), "DeltaPhiTauMet", rebin=10)
    deltaPhi2(plots.DataMCPlot(datasets, analysis+"/FakeMETVeto/Closest_DeltaPhi_of_MET_and_selected_jets"), "DeltaPhiJetMet")


    # Set temporarily the signal cross sections to a value from MSSM
#    xsect.setHplusCrossSections(datasets, tanbeta=20, mu=200)
#    datasets.getDataset("TTToHplusBHminusB_M120").setCrossSection(0.2*165)
#    datasets.getDataset("TTToHplusBWB_M120").setCrossSection(0.2*165)

####################
    datasets_tm = datasets
#    datasets_tm = datasets.deepCopy()
#    xsect.setHplusCrossSectionsToBR(datasets, br_tH=0.2, br_Htaunu=1)
#    xsect.setHplusCrossSectionsToBR(datasets_tm, br_tH=0.2, br_Htaunu=1)
#    datasets_tm.merge("TTToHplus_M120", ["TTToHplusBWB_M120", "TTToHplusBHminusB_M120"])


    topMassFit(datasets)

    
def doCounters(datasets):
    eventCounter = counter.EventCounter(datasets)

    # append row from the tree to the main counter
    eventCounter.getMainCounter().appendRow("MET > 70", treeDraw.clone(selection="met_p4.Et() > 70"))

    eventCounter.normalizeMCByLuminosity()
#    eventCounter.normalizeMCToLuminosity(73)
    print "============================================================"
    print "Main counter (MC normalized by collision data luminosity)"
    print eventCounter.getMainCounterTable().format()

#    print eventCounter.getSubCounterTable("GlobalMuon_ID").format()

    print eventCounter.getSubCounterTable("tauIDTauSelection").format()
    print eventCounter.getSubCounterTable("TauIDPassedEvt::tauID_HPSTight").format()
#    print eventCounter.getSubCounterTable("TauIDPassedJets::tauID_HPSTight").format()
    print eventCounter.getSubCounterTable("b-tagging").format()
    print eventCounter.getSubCounterTable("Jet selection").format()
    print eventCounter.getSubCounterTable("Jet main").format()    

    
#    latexFormat = counter.TableFormatConTeXtTABLE(counter.CellFormatTeX(valueFormat="%.2f"))
#    print eventCounter.getMainCounterTable().format(latexFormat)


#def vertexComparison(datasets):
#    signal = "TTToHplusBWB_M80_Summer11"
#    background = "TTToHplusBWB_M80_Summer11"
#    rtauGen(plots.ComparisonPlot(datasets.getDataset(signal).getDatasetRootHisto(analysis+"/verticesBeforeWeight"),
#                                 datasets.getDataset(background).getDatasetRootHisto(analysis+"/verticesAfterWeight")),
#            "vertices_H120")



def Gaussian(x,par):
    return par[0]*TMath.Gaus(x[0],par[1],par[2],1)    

def topMassFit(datasets):
    
    ## After standard cuts
    topmass = plots.PlotBase([datasets.getDataset("TTToHplus_M80").getDatasetRootHisto(analysis+"/BjetSelection/MassTopTop_matchJets")])
    wmass = plots.PlotBase([datasets.getDataset("TTToHplus_M80").getDatasetRootHisto(analysis+"/BjetSelection/MassW_matchJets")])

    chi2Min = plots.PlotBase([datasets.getDataset("TTToHplus_M80").getDatasetRootHisto(analysis+"/TopChiSelection/Chi2Min")])
    topSignal = plots.PlotBase([datasets.getDataset("TTToHplus_M80").getDatasetRootHisto(analysis+"/TopChiSelection/TopMass")])    
    topSignalAll = plots.PlotBase([datasets.getDataset("TTToHplus_M80").getDatasetRootHisto(analysis+"/TopChiSelection/TopMass")])
    topSignalMatch = plots.PlotBase([datasets.getDataset("TTToHplus_M80").getDatasetRootHisto(analysis+"/TopChiSelection/TopMass_fullMatch")])
    wSignal = plots.PlotBase([datasets.getDataset("TTToHplus_M80").getDatasetRootHisto(analysis+"/TopChiSelection/WMassChiCut")])
    wSignalAll = plots.PlotBase([datasets.getDataset("TTToHplus_M80").getDatasetRootHisto(analysis+"/TopChiSelection/WMass")])
    wSignalMatch = plots.PlotBase([datasets.getDataset("TTToHplus_M80").getDatasetRootHisto(analysis+"/TopChiSelection/WMass_fullMatch")])
    toptt = plots.PlotBase([datasets.getDataset("TTJets").getDatasetRootHisto(analysis+"/TopChiSelection/TopMass")])
    topWjet = plots.PlotBase([datasets.getDataset("WJets").getDatasetRootHisto(analysis+"/TopChiSelection/TopMass")])
    topSingle = plots.PlotBase([datasets.getDataset("SingleTop").getDatasetRootHisto(analysis+"/TopChiSelection/TopMass")])
    topDibos = plots.PlotBase([datasets.getDataset("Diboson").getDatasetRootHisto(analysis+"/TopChiSelection/TopMass")])
    wtt = plots.PlotBase([datasets.getDataset("TTJets").getDatasetRootHisto(analysis+"/TopChiSelection/WMass")])
    wWjet = plots.PlotBase([datasets.getDataset("WJets").getDatasetRootHisto(analysis+"/TopChiSelection/WMass")])
    wSingle = plots.PlotBase([datasets.getDataset("SingleTop").getDatasetRootHisto(analysis+"/TopChiSelection/WMass")])
    wDibos = plots.PlotBase([datasets.getDataset("Diboson").getDatasetRootHisto(analysis+"/TopChiSelection/WMass")])
    topSignal2 = plots.PlotBase([datasets.getDataset("TTToHplus_M80").getDatasetRootHisto(analysis+"/TopWithBSelection/TopMass")])
    toptt2 = plots.PlotBase([datasets.getDataset("TTJets").getDatasetRootHisto(analysis+"/TopWithBSelection/TopMass")])
    topWjet2 = plots.PlotBase([datasets.getDataset("WJets").getDatasetRootHisto(analysis+"/TopWithBSelection/TopMass")])
    topSingle2 = plots.PlotBase([datasets.getDataset("SingleTop").getDatasetRootHisto(analysis+"/TopWithBSelection/TopMass")])
    topDibos2 = plots.PlotBase([datasets.getDataset("Diboson").getDatasetRootHisto(analysis+"/TopWithBSelection/TopMass")])
    wSignal2 = plots.PlotBase([datasets.getDataset("TTToHplus_M80").getDatasetRootHisto(analysis+"/TopWithBSelection/WMass")])
    wtt2 = plots.PlotBase([datasets.getDataset("TTJets").getDatasetRootHisto(analysis+"/TopWithBSelection/WMass")])
    wWjet2 = plots.PlotBase([datasets.getDataset("WJets").getDatasetRootHisto(analysis+"/TopWithBSelection/WMass")])
    wSingle2 = plots.PlotBase([datasets.getDataset("SingleTop").getDatasetRootHisto(analysis+"/TopWithBSelection/WMass")])
    wDibos2 = plots.PlotBase([datasets.getDataset("Diboson").getDatasetRootHisto(analysis+"/TopWithBSelection/WMass")]) 
    ## plots for jet selection
    deltaTauB = plots.PlotBase([datasets.getDataset("TTToHplus_M80").getDatasetRootHisto(analysis+"/BjetSelection/DeltaTauB")])
    deltaMin = plots.PlotBase([datasets.getDataset("TTToHplus_M80").getDatasetRootHisto(analysis+"/BjetSelection/DeltaMinTauB")])
    deltaMinTrue = plots.PlotBase([datasets.getDataset("TTToHplus_M80").getDatasetRootHisto(analysis+"/BjetSelection/DeltaMinTauBTrue")])
    deltaMax = plots.PlotBase([datasets.getDataset("TTToHplus_M80").getDatasetRootHisto(analysis+"/BjetSelection/DeltaMaxTauB")])
    deltaMaxTrue = plots.PlotBase([datasets.getDataset("TTToHplus_M80").getDatasetRootHisto(analysis+"/BjetSelection/DeltaMaxTopBTrue")])
    
    ptBtauSide = plots.PlotBase([datasets.getDataset("TTToHplus_M80").getDatasetRootHisto(analysis+"/BjetSelection/PtBjetTauSide")])
    ptBtopSide = plots.PlotBase([datasets.getDataset("TTToHplus_M80").getDatasetRootHisto(analysis+"/BjetSelection/PtBjetTopSide")])
    ptBtauSideTrue = plots.PlotBase([datasets.getDataset("TTToHplus_M80").getDatasetRootHisto(analysis+"/BjetSelection/PtBjetTauSideTrue")])
    ptBtopSideTrue = plots.PlotBase([datasets.getDataset("TTToHplus_M80").getDatasetRootHisto(analysis+"/BjetSelection/PtBjetTopSideTrue")])
    pttoptopMatch = plots.PlotBase([datasets.getDataset("TTToHplus_M80").getDatasetRootHisto(analysis+"/BjetSelection/PtTopTop_matchJets")])
    pttoptauMatch = plots.PlotBase([datasets.getDataset("TTToHplus_M80").getDatasetRootHisto(analysis+"/BjetSelection/PtTopHiggs_matchJets")])

    topmass_ptmax = plots.PlotBase([datasets.getDataset("TTToHplus_M80").getDatasetRootHisto(analysis+"/TopSelection/TopMass")])
    topmass_ptmaxMatch = plots.PlotBase([datasets.getDataset("TTToHplus_M80").getDatasetRootHisto(analysis+"/TopSelection/TopMass_fullMatch")])
    wmass_ptmax = plots.PlotBase([datasets.getDataset("TTToHplus_M80").getDatasetRootHisto(analysis+"/TopSelection/WMass")])
    wmass_ptmaxMatch = plots.PlotBase([datasets.getDataset("TTToHplus_M80").getDatasetRootHisto(analysis+"/TopSelection/WMass_fullMatch")])
    topPttt = plots.PlotBase([datasets.getDataset("TTJets").getDatasetRootHisto(analysis+"/TopSelection/TopMass")])
    topPtWjet = plots.PlotBase([datasets.getDataset("WJets").getDatasetRootHisto(analysis+"/TopSelection/TopMass")])
    topPtSingle = plots.PlotBase([datasets.getDataset("SingleTop").getDatasetRootHisto(analysis+"/TopSelection/TopMass")])
    topPtDibos = plots.PlotBase([datasets.getDataset("Diboson").getDatasetRootHisto(analysis+"/TopSelection/TopMass")])

    
    chi2Min.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    topmass_ptmax.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    topmass_ptmaxMatch.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    wmass_ptmax.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    wmass_ptmaxMatch.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())

    topPttt.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    topPtWjet.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    topPtSingle.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    topPtDibos.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())  
    
    wSignal.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    wSignalAll.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    wSignalMatch.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())

    topSignal.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    topmass.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    wmass.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())

    wSignal.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    
    topSignal.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    wSignal2.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    topSignalAll.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity()) 
    topSignalMatch.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    toptt.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    topWjet.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    topSingle.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    topDibos.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    wtt.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    wWjet.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    wSingle.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    wDibos.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    wtt2.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    wWjet2.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    wSingle2.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    wDibos2.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    topSignal2.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    toptt2.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    topWjet2.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    topSingle2.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    topDibos2.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())

    deltaTauB.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    deltaMin.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    deltaMinTrue.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    deltaMaxTrue.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity()) 
    deltaMax.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    ptBtauSide.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    ptBtopSide.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    ptBtauSideTrue.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    ptBtopSideTrue.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    pttoptopMatch.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    pttoptauMatch.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    
    
#    mt4050._setLegend(histograms.createLegend())


    topmass._setLegendStyles()
    topmass._setLegendLabels()
    topmass.histoMgr.setHistoDrawStyleAll("P")
    topmass.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(3))    
    htopmass = topmass.histoMgr.getHisto("TTToHplus_M80").getRootHisto().Clone(analysis+"/BjetSelection/MassTopTop_matchJets")
    
    wmass._setLegendStyles()
    wmass._setLegendLabels()
    wmass.histoMgr.setHistoDrawStyleAll("P")
    wmass.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(3))    
    hwmass = wmass.histoMgr.getHisto("TTToHplus_M80").getRootHisto().Clone(analysis+"/BjetSelection/MassW_matchJets")




########################################    
    
    canvas = ROOT.TCanvas("canvas","",500,500)
    htopmass.GetYaxis().SetTitle("Events")
    htopmass.GetXaxis().SetTitle("m_{top} (GeV/c^{2})")
#    htopmass.GetYaxis().SetTitleSize(10.0)
#    htopmass.GetXaxis().SetTitleSize(20.0)
    htopmass.Draw()
    histo = htopmass.Clone("histo")
#    rangeMin = htopmass.GetXaxis().GetXmin()
#    rangeMax = htopmass.GetXaxis().GetXmax()
    rangeMin = 145
    rangeMax = 200

    numberOfParameters = 3

#    print "Fit range ",rangeMin, " - ",rangeMax

    class FitFunction:
        def __call__( self, x, par ):
            return Gaussian(x,par)

    theFit = TF1('theFit',FitFunction(),rangeMin,rangeMax,numberOfParameters)
    theFit.SetParLimits(0,1,2000)
    theFit.SetParLimits(1,0,1000)
    theFit.SetParLimits(2,0.1,200)   
#    gStyle.SetOptFit(0)
    
    htopmass.Fit(theFit,"LR")          
    theFit.SetRange(rangeMin,rangeMax)
    theFit.SetLineStyle(1)
    theFit.SetLineWidth(2)  
    theFit.Draw("same")
    tex4 = ROOT.TLatex(0.2,0.95,"CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    tex2 = ROOT.TLatex(0.6,0.7,"tt->tbH^{#pm}") 
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw()
    tex3 = ROOT.TLatex(0.6,0.6,"m_{H^{#pm}} = 120 GeV/c^{2}") 
    tex3.SetNDC()
    tex3.SetTextSize(20)
    tex3.Draw()
    tex5 = ROOT.TLatex(0.6,0.5,"Matched jets") 
    tex5.SetNDC()
    tex5.SetTextSize(20)
    tex5.Draw()
    print "Fit range ",rangeMin, " - ",rangeMax    
    canvas.Print("topMassFit_Chi2.png")

    

###########

    canvas2 = ROOT.TCanvas("canvas2","",500,500)
    hwmass.GetYaxis().SetTitle("Events")
    hwmass.GetXaxis().SetTitle("m_{W} (GeV/c^{2})")
    hwmass.Draw()
    histo2 = hwmass.Clone("histo")
#    rangeMin = htopmass.GetXaxis().GetXmin()
#    rangeMax = htopmass.GetXaxis().GetXmax()
    rangeMin = 60
    rangeMax = 105

    numberOfParameters = 3

#    print "Fit range ",rangeMin, " - ",rangeMax

    class FitFunction:
        def __call__( self, x, par ):
            return Gaussian(x,par)

    theFit = TF1('theFit',FitFunction(),rangeMin,rangeMax,numberOfParameters)
    theFit.SetParLimits(0,1,2000)
    theFit.SetParLimits(1,0,1000)
    theFit.SetParLimits(2,0.1,200)   
#    gStyle.SetOptFit(0)
    
    hwmass.Fit(theFit,"LR")          
    theFit.SetRange(rangeMin,rangeMax)
    theFit.SetLineStyle(1)
    theFit.SetLineWidth(2) 
    theFit.Draw("same")
    tex4 = ROOT.TLatex(0.2,0.95,"CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    tex2 = ROOT.TLatex(0.6,0.7,"tt->tbH^{#pm}") 
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw()
    tex3 = ROOT.TLatex(0.6,0.6,"m_{H^{#pm}} = 120 GeV/c^{2}") 
    tex3.SetNDC()
    tex3.SetTextSize(20)
    tex3.Draw()
    tex5 = ROOT.TLatex(0.6,0.5,"Matched jets") 
    tex5.SetNDC()
    tex5.SetTextSize(20)
    tex5.Draw()
    print "Fit range ",rangeMin, " - ",rangeMax    
    canvas2.Print("wMassFit_Chi2.png")



#############################

    
    # plot top mass chi2
    chi2Min._setLegendStyles()
    chi2Min._setLegendLabels()
    chi2Min.histoMgr.setHistoDrawStyleAll("P")
    chi2Min.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    hchi2Min = chi2Min.histoMgr.getHisto("TTToHplus_M80").getRootHisto().Clone(analysis+"/TopChiSelection/Chi2Min")
    topSignal._setLegendStyles()
    topSignal._setLegendLabels()
    topSignal.histoMgr.setHistoDrawStyleAll("P")
    topSignal.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    htopSignal = topSignal.histoMgr.getHisto("TTToHplus_M80").getRootHisto().Clone(analysis+"/TopChiSelection/TopMass")
    topSignalAll._setLegendStyles()
    topSignalAll._setLegendLabels()
    topSignalAll.histoMgr.setHistoDrawStyleAll("P")
    topSignalAll.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    htopSignalAll = topSignalAll.histoMgr.getHisto("TTToHplus_M80").getRootHisto().Clone(analysis+"/TopChiSelection/TopMass")
    topSignalMatch._setLegendStyles()
    topSignalMatch._setLegendLabels()
    topSignalMatch.histoMgr.setHistoDrawStyleAll("P")
    topSignalMatch.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    htopSignalMatch = topSignalMatch.histoMgr.getHisto("TTToHplus_M80").getRootHisto().Clone(analysis+"/TopChiSelection/TopMass_fullMatch")
     # plot W mass chi2
    wSignal._setLegendStyles()
    wSignal._setLegendLabels()
    wSignal.histoMgr.setHistoDrawStyleAll("P")
    wSignal.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    hwSignal = wSignal.histoMgr.getHisto("TTToHplus_M80").getRootHisto().Clone(analysis+"/TopChiSelection/WMass")
    wSignalAll._setLegendStyles()
    wSignalAll._setLegendLabels()
    wSignalAll.histoMgr.setHistoDrawStyleAll("P")
    wSignalAll.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    hwSignalAll = wSignalAll.histoMgr.getHisto("TTToHplus_M80").getRootHisto().Clone(analysis+"/TopChiSelection/WMass")
    wSignalMatch._setLegendStyles()
    wSignalMatch._setLegendLabels()
    wSignalMatch.histoMgr.setHistoDrawStyleAll("P")
    wSignalMatch.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    hwSignalMatch = wSignalMatch.histoMgr.getHisto("TTToHplus_M80").getRootHisto().Clone(analysis+"/TopChiSelection/WMass_fullMatch")
               
    toptt._setLegendStyles()
    toptt._setLegendLabels()
    toptt.histoMgr.setHistoDrawStyleAll("P")
    toptt.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    htoptt = toptt.histoMgr.getHisto("TTJets").getRootHisto().Clone(analysis+"/TopChiSelection/TopMass")
    topWjet._setLegendStyles()
    topWjet._setLegendLabels()
    topWjet.histoMgr.setHistoDrawStyleAll("P")
    topWjet.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    htopWjet = topWjet.histoMgr.getHisto("WJets").getRootHisto().Clone(analysis+"/TopChiSelection/TopMass")
    topSingle._setLegendStyles()
    topSingle._setLegendLabels()
    topSingle.histoMgr.setHistoDrawStyleAll("P")
    topSingle.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    htopSingle = topSingle.histoMgr.getHisto("SingleTop").getRootHisto().Clone(analysis+"/TopChiSelection/TopMass")
    topDibos._setLegendStyles()
    topDibos._setLegendLabels() 
    topDibos.histoMgr.setHistoDrawStyleAll("P")
    topDibos.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    htopDibos = topDibos.histoMgr.getHisto("Diboson").getRootHisto().Clone(analysis+"/TopChiSelection/TopMass")
    
    wtt._setLegendStyles()
    wtt._setLegendLabels()
    wtt.histoMgr.setHistoDrawStyleAll("P")
    wtt.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    hwtt = wtt.histoMgr.getHisto("TTJets").getRootHisto().Clone(analysis+"/TopChiSelection/WMass")
    wWjet._setLegendStyles()
    wWjet._setLegendLabels()
    wWjet.histoMgr.setHistoDrawStyleAll("P")
    wWjet.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    hwWjet = wWjet.histoMgr.getHisto("WJets").getRootHisto().Clone(analysis+"/TopChiSelection/WMass")
    wSingle._setLegendStyles()
    wSingle._setLegendLabels()
    wSingle.histoMgr.setHistoDrawStyleAll("P")
    wSingle.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    hwSingle = wSingle.histoMgr.getHisto("SingleTop").getRootHisto().Clone(analysis+"/TopChiSelection/WMass")
    wDibos._setLegendStyles()
    wDibos._setLegendLabels() 
    wDibos.histoMgr.setHistoDrawStyleAll("P")
    wDibos.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    hwDibos = wDibos.histoMgr.getHisto("Diboson").getRootHisto().Clone(analysis+"/TopChiSelection/WMass")

    htopBg = htoptt.Clone("bgSum")
#    hmtSum.SetName("mtSum")
#    hmtSum.SetTitle("Inverted tau ID")
    htopBg.Add(htopWjet)
    htopBg.Add(htopSingle)
    htopBg.Add(htopDibos)

    htopSB = htopBg.Clone("SoverBG")
    htopSB.Add(htopSignal)
    
    canvas4 = ROOT.TCanvas("canvas4","",500,500)
#    canvas4.SetLogy()
#    htopSB.SetMinimum(0.1)
    htopSB.SetMarkerColor(2)
    htopSB.SetMarkerSize(1)
    htopSB.SetMarkerStyle(24)
    htopSB.Draw("EP")
    
    htopBg.SetMarkerColor(4)
    htopBg.SetMarkerSize(1)
    htopBg.SetMarkerStyle(20)
    htopBg.SetFillColor(4)
    htopBg.Draw("same")
    
    htopSB.GetYaxis().SetTitle("Events / 10 GeV/c^{2}")
#    hmt.GetYaxis().SetTitleSize(20.0)
    htopSB.GetYaxis().SetTitleOffset(1.5)
    htopSB.GetXaxis().SetTitle("m_{top} (GeV/c^{2})")
    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       2.18 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    marker1 = ROOT.TMarker(0.6,0.815,htopSB.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(htopSB.GetMarkerColor())
    marker1.SetMarkerSize(0.9*htopSB.GetMarkerSize())
    marker1.Draw()
    tex1 = ROOT.TLatex(0.62,0.8,"Signal + tt and EW Bg") 
    tex1.SetNDC()
    tex1.SetTextSize(15)
    tex1.Draw() 
    marker2 = ROOT.TMarker(0.6,0.715,htopBg.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(htopBg.GetMarkerColor())
    marker2.SetMarkerSize(0.9*htopBg.GetMarkerSize())
    marker2.Draw()
    tex2 = ROOT.TLatex(0.62,0.7,"tt and EW Background") 
    tex2.SetNDC()
    tex2.SetTextSize(15)
    tex2.Draw() 
    
    canvas4.Print("topMass_Chi2.png")

    ########################
    ### top mass with full match
    
    canvasm4 = ROOT.TCanvas("canvasm4","",500,500)
#    canvasm4.SetLogy()
#    htopSB.SetMinimum(0.1)
    htopSignal.SetMarkerColor(2)
    htopSignal.SetMarkerSize(1)
    htopSignal.SetMarkerStyle(24)
    htopSignal.Draw("EP")
    
    htopSignalMatch.SetMarkerColor(4)
    htopSignalMatch.SetMarkerSize(1)
    htopSignalMatch.SetMarkerStyle(20)
    htopSignalMatch.SetFillColor(4)
    htopSignalMatch.Draw("same")
    
    htopSignal.GetYaxis().SetTitle("Events / 10 GeV/c^{2}")
#    hmt.GetYaxis().SetTitleSize(20.0)
    htopSignal.GetYaxis().SetTitleOffset(1.5)
    htopSignal.GetXaxis().SetTitle("m_{top} (GeV/c^{2})")
    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       2.18 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    tex5 = ROOT.TLatex(0.6,0.8,"Signal, m_{H^{#pm}}= 120 GeV/c^{2}") 
    tex5.SetNDC()
    tex5.SetTextSize(15)
    tex5.Draw()   
    marker1 = ROOT.TMarker(0.6,0.715,htopSignal.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(htopSignal.GetMarkerColor())
    marker1.SetMarkerSize(0.9*htopSignal.GetMarkerSize())
    marker1.Draw()
    tex1 = ROOT.TLatex(0.62,0.7,"All combinations") 
    tex1.SetNDC()
    tex1.SetTextSize(20)
    tex1.Draw() 
    marker2 = ROOT.TMarker(0.6,0.615,htopSignalMatch.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(htopSignalMatch.GetMarkerColor())
    marker2.SetMarkerSize(0.9*htopSignalMatch.GetMarkerSize())
    marker2.Draw()
    tex2 = ROOT.TLatex(0.62,0.6,"Matching jets") 
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw() 
    
    canvasm4.Print("topMass_Chi2_match.png")

    ############# Chi2min
    canvasm8 = ROOT.TCanvas("canvasm8","",500,500)
#    canvasm4.SetLogy()
#    htopSB.SetMinimum(0.1)
    hchi2Min.SetMarkerColor(4)
    hchi2Min.SetMarkerSize(1)
    hchi2Min.SetMarkerStyle(24)
    hchi2Min.Draw("EP")

    
    hchi2Min.GetYaxis().SetTitle("Events ")
#    hmt.GetYaxis().SetTitleSize(20.0)
    hchi2Min.GetYaxis().SetTitleOffset(1.5)
    hchi2Min.GetXaxis().SetTitle("min(#chi^{2})")
    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       2.18 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    tex5 = ROOT.TLatex(0.5,0.8,"Signal, m_{H^{#pm}}= 120 GeV/c^{2}") 
    tex5.SetNDC()
    tex5.SetTextSize(20)
    tex5.Draw()   
    
    
    canvasm8.Print("chi2Min.png")

    
 ### top mass with and without chi cut
    
    canvasm5 = ROOT.TCanvas("canvasm5","",500,500)
#    canvasm5.SetLogy()
#    htopSB.SetMinimum(0.1)
    htopSignalAll.SetMarkerColor(2)
    htopSignalAll.SetMarkerSize(1)
    htopSignalAll.SetMarkerStyle(21)
    htopSignalAll.Draw("EP")
    
    htopSignal.SetMarkerColor(4)
    htopSignal.SetMarkerSize(1)
    htopSignal.SetMarkerStyle(20)
    htopSignal.SetFillColor(4)
    htopSignal.Draw("same")
    
    htopSignalAll.GetYaxis().SetTitle("Events / 10 GeV/c^{2}")
#    hmt.GetYaxis().SetTitleSize(20.0)
    htopSignalAll.GetYaxis().SetTitleOffset(1.5)
    htopSignalAll.GetXaxis().SetTitle("m_{top} (GeV/c^{2})")
    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       2.18 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    tex5 = ROOT.TLatex(0.6,0.8,"Signal, m_{H^{#pm}}= 120 GeV/c^{2}") 
    tex5.SetNDC()
    tex5.SetTextSize(15)
    tex5.Draw()   
    marker1 = ROOT.TMarker(0.6,0.715,htopSignalAll.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(htopSignalAll.GetMarkerColor())
    marker1.SetMarkerSize(0.9*htopSignalAll.GetMarkerSize())
    marker1.Draw()
    tex1 = ROOT.TLatex(0.62,0.7,"No #chi^{2} cut") 
    tex1.SetNDC()
    tex1.SetTextSize(20)
    tex1.Draw() 
    marker2 = ROOT.TMarker(0.6,0.615,htopSignal.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(htopSignal.GetMarkerColor())
    marker2.SetMarkerSize(0.9*htopSignal.GetMarkerSize())
    marker2.Draw()
    tex2 = ROOT.TLatex(0.62,0.6,"#chi^{2} < 5 ") 
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw() 
    
    canvasm5.Print("topMass_Chi2_comparison.png")
    
################################################3
#########  W plots with Chi2 
    hwBg = hwtt.Clone("bgSum")
#    hmtSum.SetName("mtSum")
#    hmtSum.SetTitle("Inverted tau ID")
    hwBg.Add(htopWjet)
    hwBg.Add(htopSingle)
    hwBg.Add(htopDibos)

    hwSB = hwBg.Clone("SoverBG")
    hwSB.Add(hwSignal)
    
    canvasw4 = ROOT.TCanvas("canvasw4","",500,500)
#    canvasw4.SetLogy()
#    htopSB.SetMinimum(0.1)
    hwSB.SetMarkerColor(2)
    hwSB.SetMarkerSize(1)
    hwSB.SetMarkerStyle(24)
    hwSB.Draw("EP")
    
    hwBg.SetMarkerColor(4)
    hwBg.SetMarkerSize(1)
    hwBg.SetMarkerStyle(20)
    hwBg.SetFillColor(4)
    hwBg.Draw("same")
    
    hwSB.GetYaxis().SetTitle("Events / 10 GeV/c^{2}")
#    hmt.GetYaxis().SetTitleSize(20.0)
    hwSB.GetYaxis().SetTitleOffset(1.5)
    hwSB.GetXaxis().SetTitle("m_{W} (GeV/c^{2})")
    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       2.18 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    marker1 = ROOT.TMarker(0.6,0.815,hwSB.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(hwSB.GetMarkerColor())
    marker1.SetMarkerSize(0.9*hwSB.GetMarkerSize())
    marker1.Draw()
    tex1 = ROOT.TLatex(0.62,0.8,"Signal + tt and EW Bg") 
    tex1.SetNDC()
    tex1.SetTextSize(15)
    tex1.Draw() 
    marker2 = ROOT.TMarker(0.6,0.715,hwBg.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(hwBg.GetMarkerColor())
    marker2.SetMarkerSize(0.9*hwBg.GetMarkerSize())
    marker2.Draw()
    tex2 = ROOT.TLatex(0.62,0.7,"tt and EW Background") 
    tex2.SetNDC()
    tex2.SetTextSize(15)
    tex2.Draw() 
    
    canvasw4.Print("WMass_Chi2.png")

    ########################
    ### W mass with full match
    
    canvasmw4 = ROOT.TCanvas("canvasmw4","",500,500)
#    canvasmw4.SetLogy()
#    htopSB.SetMinimum(0.1)
    hwSignal.SetMarkerColor(2)
    hwSignal.SetMarkerSize(1)
    hwSignal.SetMarkerStyle(24)
    hwSignal.Draw("EP")
    
    hwSignalMatch.SetMarkerColor(4)
    hwSignalMatch.SetMarkerSize(1)
    hwSignalMatch.SetMarkerStyle(20)
    hwSignalMatch.SetFillColor(4)
    hwSignalMatch.Draw("same")
    
    hwSignal.GetYaxis().SetTitle("Events / 10 GeV/c^{2}")
#    hmt.GetYaxis().SetTitleSize(20.0)
    hwSignal.GetYaxis().SetTitleOffset(1.5)
    hwSignal.GetXaxis().SetTitle("m_{W} (GeV/c^{2})")
    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       2.18 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    tex5 = ROOT.TLatex(0.6,0.8,"Signal, m_{H^{#pm}}= 120 GeV/c^{2}") 
    tex5.SetNDC()
    tex5.SetTextSize(15)
    tex5.Draw()   
    marker1 = ROOT.TMarker(0.6,0.715,hwSignal.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(hwSignal.GetMarkerColor())
    marker1.SetMarkerSize(0.9*hwSignal.GetMarkerSize())
    marker1.Draw()
    tex1 = ROOT.TLatex(0.62,0.7,"All combinations") 
    tex1.SetNDC()
    tex1.SetTextSize(20)
    tex1.Draw() 
    marker2 = ROOT.TMarker(0.6,0.615,hwSignalMatch.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(hwSignalMatch.GetMarkerColor())
    marker2.SetMarkerSize(0.9*hwSignalMatch.GetMarkerSize())
    marker2.Draw()
    tex2 = ROOT.TLatex(0.62,0.6,"Matching jets") 
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw() 
    
    canvasmw4.Print("WMass_Chi2_match.png")
    
 ### top mass with and without chi cut
    
    canvasmw5 = ROOT.TCanvas("canvasmw5","",500,500)
#    canvasmw5.SetLogy()
#    htopSB.SetMinimum(0.1)
    hwSignalAll.SetMarkerColor(2)
    hwSignalAll.SetMarkerSize(1)
    hwSignalAll.SetMarkerStyle(24)
    hwSignalAll.Draw("EP")
    
    hwSignal.SetMarkerColor(4)
    hwSignal.SetMarkerSize(1)
    hwSignal.SetMarkerStyle(20)
    hwSignal.SetFillColor(4)
    hwSignal.Draw("same")
    
    hwSignalAll.GetYaxis().SetTitle("Events / 10 GeV/c^{2}")
#    hmt.GetYaxis().SetTitleSize(20.0)
    hwSignalAll.GetYaxis().SetTitleOffset(1.5)
    hwSignalAll.GetXaxis().SetTitle("m_{W} (GeV/c^{2})")
    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       2.18 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    tex5 = ROOT.TLatex(0.6,0.8,"Signal, m_{H^{#pm}}= 120 GeV/c^{2}") 
    tex5.SetNDC()
    tex5.SetTextSize(15)
    tex5.Draw()   
    marker1 = ROOT.TMarker(0.6,0.715,hwSignalAll.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(hwSignalAll.GetMarkerColor())
    marker1.SetMarkerSize(0.9*hwSignalAll.GetMarkerSize())
    marker1.Draw()
    tex1 = ROOT.TLatex(0.62,0.7,"No #chi^{2} cut") 
    tex1.SetNDC()
    tex1.SetTextSize(20)
    tex1.Draw() 
    marker2 = ROOT.TMarker(0.6,0.615,hwSignal.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(hwSignal.GetMarkerColor())
    marker2.SetMarkerSize(0.9*hwSignal.GetMarkerSize())

    marker2.Draw()
    tex2 = ROOT.TLatex(0.62,0.6,"#chi^{2} < 5 ") 
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw() 
    
    canvasmw5.Print("WMass_Chi2_comparison.png")
 
#############################
    # plot top mass with B sel
    topSignal2._setLegendStyles()
    topSignal2._setLegendLabels()
    topSignal2.histoMgr.setHistoDrawStyleAll("P")
    topSignal2.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    htopSignal2= topSignal2.histoMgr.getHisto("TTToHplus_M80").getRootHisto().Clone(analysis+"/TopWithBSelection/TopMass")
    toptt2._setLegendStyles()
    toptt2._setLegendLabels()
    toptt2.histoMgr.setHistoDrawStyleAll("P")
    toptt2.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    htoptt2 = toptt2.histoMgr.getHisto("TTJets").getRootHisto().Clone(analysis+"/TopWithBSelection/TopMass")
    topWjet2._setLegendStyles()
    topWjet2._setLegendLabels()
    topWjet2.histoMgr.setHistoDrawStyleAll("P")
    topWjet2.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    htopWjet2 = topWjet2.histoMgr.getHisto("WJets").getRootHisto().Clone(analysis+"/TopWithBSelection/TopMass")
    topSingle2._setLegendStyles()
    topSingle2._setLegendLabels()
    topSingle2.histoMgr.setHistoDrawStyleAll("P")
    topSingle2.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    htopSingle2 = topSingle2.histoMgr.getHisto("SingleTop").getRootHisto().Clone(analysis+"/TopWithBSelection/TopMass")
    topDibos2._setLegendStyles()
    topDibos2._setLegendLabels() 
    topDibos2.histoMgr.setHistoDrawStyleAll("P")
    topDibos2.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    htopDibos2 = topDibos2.histoMgr.getHisto("Diboson").getRootHisto().Clone(analysis+"/TopWithBSelection/TopMass")

    htopBg2 = htoptt2.Clone("bgSum")
#    hmtSum.SetName("mtSum")
#    hmtSum.SetTitle("Inverted tau ID")
    htopBg2.Add(htopWjet2)
    htopBg2.Add(htopSingle2)
    htopBg2.Add(htopDibos2)

    htopSB2 = htopBg2.Clone("SoverBG")
    htopSB2.Add(htopSignal2)

        
    canvas7 = ROOT.TCanvas("canvas7","",500,500)
#    canvas7.SetLogy()
#    htopSB.SetMinimum(0.1)
    htopSB2.SetMarkerColor(2)
    htopSB2.SetMarkerSize(1)
    htopSB2.SetMarkerStyle(24)
    htopSB2.Draw("EP")
    
    htopBg2.SetMarkerColor(4)
    htopBg2.SetMarkerSize(1)
    htopBg2.SetMarkerStyle(20)
    htopBg2.SetFillColor(4)
    htopBg2.Draw("same")
    
    htopSB2.GetYaxis().SetTitle("Events / 10 GeV/c^{2}")
#    hmt.GetYaxis().SetTitleSize(20.0)
    htopSB2.GetYaxis().SetTitleOffset(1.5)
    htopSB2.GetXaxis().SetTitle("m_{top} (GeV/c^{2})")
    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       2.18 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    marker1 = ROOT.TMarker(0.6,0.815,htopSB2.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(htopSB2.GetMarkerColor())
    marker1.SetMarkerSize(0.9*htopSB2.GetMarkerSize())
    marker1.Draw()
    tex1 = ROOT.TLatex(0.62,0.8,"Signal + tt and EW Bg") 
    tex1.SetNDC()
    tex1.SetTextSize(15)
    tex1.Draw() 
    marker2 = ROOT.TMarker(0.6,0.715,htopBg2.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(htopBg2.GetMarkerColor())
    marker2.SetMarkerSize(0.9*htopBg2.GetMarkerSize())
    marker2.Draw()
    tex2 = ROOT.TLatex(0.62,0.7,"tt and EW Background") 
    tex2.SetNDC()
    tex2.SetTextSize(15)
    tex2.Draw() 
    
    canvas7.Print("topMass_WithBsel.png")



########## W mass with B sel

    wSignal2._setLegendStyles()
    wSignal2._setLegendLabels()
    wSignal2.histoMgr.setHistoDrawStyleAll("P")
    wSignal2.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    hwSignal2= wSignal2.histoMgr.getHisto("TTToHplus_M80").getRootHisto().Clone(analysis+"/TopWithBSelection/WMass")
    wtt2._setLegendStyles()
    wtt2._setLegendLabels()
    wtt2.histoMgr.setHistoDrawStyleAll("P")
    wtt2.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    hwtt2 = wtt2.histoMgr.getHisto("TTJets").getRootHisto().Clone(analysis+"/TopWithBSelection/WMass")
    wWjet2._setLegendStyles()
    wWjet2._setLegendLabels()
    wWjet2.histoMgr.setHistoDrawStyleAll("P")
    wWjet2.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    hwWjet2 = wWjet2.histoMgr.getHisto("WJets").getRootHisto().Clone(analysis+"/TopWithBSelection/WMass")
    wSingle2._setLegendStyles()
    wSingle2._setLegendLabels()
    wSingle2.histoMgr.setHistoDrawStyleAll("P")
    wSingle2.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    hwSingle2 = wSingle2.histoMgr.getHisto("SingleTop").getRootHisto().Clone(analysis+"/TopWithBSelection/WMass")
    wDibos2._setLegendStyles()
    wDibos2._setLegendLabels() 
    wDibos2.histoMgr.setHistoDrawStyleAll("P")
    wDibos2.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    hwDibos2 = wDibos2.histoMgr.getHisto("Diboson").getRootHisto().Clone(analysis+"/TopWithBSelection/WMass")

    hwBg2 = hwtt2.Clone("bgSum")
#    hmtSum.SetName("mtSum")
#    hmtSum.SetTitle("Inverted tau ID")
    hwBg2.Add(hwWjet2)
    hwBg2.Add(hwSingle2)
    hwBg2.Add(hwDibos2)

    hwSB2 = hwBg2.Clone("SoverBG")
    hwSB2.Add(hwSignal2)

        
    canvas9 = ROOT.TCanvas("canvas9","",500,500)
#    canvas7.SetLogy()
#    htopSB.SetMinimum(0.1)
    hwSB2.SetMarkerColor(2)
    hwSB2.SetMarkerSize(1)
    hwSB2.SetMarkerStyle(24)
    hwSB2.Draw("EP")
    
    hwBg2.SetMarkerColor(4)
    hwBg2.SetMarkerSize(1)
    hwBg2.SetMarkerStyle(20)
    hwBg2.SetFillColor(4)
    hwBg2.Draw("same")
    
    hwSB2.GetYaxis().SetTitle("Events / 10 GeV/c^{2}")
#    hmt.GetYaxis().SetTitleSize(20.0)
    hwSB2.GetYaxis().SetTitleOffset(1.5)
    hwSB2.GetXaxis().SetTitle("m_{W} (GeV/c^{2})")
    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       2.18 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    marker1 = ROOT.TMarker(0.6,0.815,hwSB2.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(hwSB2.GetMarkerColor())
    marker1.SetMarkerSize(0.9*hwSB2.GetMarkerSize())
    marker1.Draw()
   
    tex1 = ROOT.TLatex(0.62,0.8,"Signal + tt and EW Bg")  
    tex1.SetNDC()
    tex1.SetTextSize(15)
    tex1.Draw() 
    marker2 = ROOT.TMarker(0.6,0.715,hwBg2.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(hwBg2.GetMarkerColor())
    marker2.SetMarkerSize(0.9*hwBg2.GetMarkerSize())
    marker2.Draw()
    tex2 = ROOT.TLatex(0.62,0.7,"tt and EW Background") 
    tex2.SetNDC()
    tex2.SetTextSize(15)
    tex2.Draw() 
    
    canvas9.Print("wMass_WithBsel.png")





#################################################    
    canvas6 = ROOT.TCanvas("canvas6","",500,500)
#    canvas6.SetLogy()
#    htopSB.SetMinimum(0.1)
    htopSignal.SetMarkerColor(2)
    htopSignal.SetMarkerSize(1)
    htopSignal.SetMarkerStyle(21)
    htopSignal.Draw("EP")
    
    htoptt.SetMarkerColor(4)
    htoptt.SetMarkerSize(1)
    htoptt.SetMarkerStyle(24)
    htoptt.SetFillColor(4)
    htoptt.Draw("same")

    htopWjet.SetMarkerColor(1)
    htopWjet.SetMarkerSize(1)
    htopWjet.SetMarkerStyle(22)
    htopWjet.SetFillColor(1)
    htopWjet.Draw("same")
    
    htopSingle.SetMarkerColor(6)
    htopSingle.SetMarkerSize(1)
    htopSingle.SetMarkerStyle(23)
    htopSingle.SetFillColor(6)
    htopSingle.Draw("same")
    
    htopDibos.SetMarkerColor(7)
    htopDibos.SetMarkerSize(1)
    htopDibos.SetMarkerStyle(20)
    htopDibos.SetFillColor(7)
    htopDibos.Draw("same")

    htopSignal.GetYaxis().SetTitle("Events / 10 GeV/c^{2}")
#    hmt.GetYaxis().SetTitleSize(20.0)
    htopSignal.GetYaxis().SetTitleOffset(1.5)
    htopSignal.GetXaxis().SetTitle("m_{top} (GeV/c^{2})")
    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       2.18 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    marker1 = ROOT.TMarker(0.6,0.815,htopSignal.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(htopSignal.GetMarkerColor())
    marker1.SetMarkerSize(0.9*htopSignal.GetMarkerSize())
    marker1.Draw()
    tex1 = ROOT.TLatex(0.62,0.8,"Signal") 
    tex1.SetNDC()
    tex1.SetTextSize(20)
    tex1.Draw() 
    marker2 = ROOT.TMarker(0.6,0.755,htoptt.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(htoptt.GetMarkerColor())
    marker2.SetMarkerSize(0.9*htoptt.GetMarkerSize())
    marker2.Draw()
    tex2 = ROOT.TLatex(0.62,0.75,"tt ") 
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw() 
    marker3 = ROOT.TMarker(0.6,0.715,htopWjet.GetMarkerStyle())
    marker3.SetNDC()
    marker3.SetMarkerColor(htopWjet.GetMarkerColor())
    marker3.SetMarkerSize(0.9*htopWjet.GetMarkerSize())
    marker3.Draw()
    tex3 = ROOT.TLatex(0.62,0.7,"Wjet") 
    tex3.SetNDC()
    tex3.SetTextSize(20)
    tex3.Draw() 
    marker5 = ROOT.TMarker(0.6,0.655,htopSingle.GetMarkerStyle())
    marker5.SetNDC()
    marker5.SetMarkerColor(htopSingle.GetMarkerColor())
    marker5.SetMarkerSize(0.9*htopSingle.GetMarkerSize())
    marker5.Draw()
    tex5 = ROOT.TLatex(0.62,0.65,"Single top") 
    tex5.SetNDC()
    tex5.SetTextSize(20)
    tex5.Draw()
    marker6 = ROOT.TMarker(0.6,0.605,htopDibos.GetMarkerStyle())
    marker6.SetNDC()
    marker6.SetMarkerColor(htopDibos.GetMarkerColor())
    marker6.SetMarkerSize(0.9*htopDibos.GetMarkerSize())
    marker6.Draw()
    tex6 = ROOT.TLatex(0.62,0.6,"Di boson") 
    tex6.SetNDC()
    tex6.SetTextSize(20)
    tex6.Draw()
       
    canvas6.Print("topMass_Chi2_all.png")


    

#######################################################    
    canvas4 = ROOT.TCanvas("canvas4","",500,500)
#    canvas4.SetLogy()
#    htopSB.SetMinimum(0.1)
    htopSB.SetMarkerColor(2)
    htopSB.SetMarkerSize(1)
    htopSB.SetMarkerStyle(24)
    htopSB.Draw("EP")
    
    htopBg.SetMarkerColor(4)
    htopBg.SetMarkerSize(1)
    htopBg.SetMarkerStyle(20)
    htopBg.SetFillColor(4)
    htopBg.Draw("same")
    
    htopSB.GetYaxis().SetTitle("Events / 10 GeV/c^{2}")
#    hmt.GetYaxis().SetTitleSize(20.0)
    htopSB.GetYaxis().SetTitleOffset(1.5)
    htopSB.GetXaxis().SetTitle("m_{top} (GeV/c^{2})")
    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       2.18 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    marker1 = ROOT.TMarker(0.6,0.815,htopSB.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(htopSB.GetMarkerColor())
    marker1.SetMarkerSize(0.9*htopSB.GetMarkerSize())
    marker1.Draw()
    tex1 = ROOT.TLatex(0.62,0.8,"Signal + tt and EW Bg") 
    tex1.SetNDC()
    tex1.SetTextSize(15)
    tex1.Draw() 
    marker2 = ROOT.TMarker(0.6,0.715,htopBg.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(htopBg.GetMarkerColor())
    marker2.SetMarkerSize(0.9*htopBg.GetMarkerSize())
    marker2.Draw()
    tex2 = ROOT.TLatex(0.62,0.7,"tt and EW Background") 
    tex2.SetNDC()
    tex2.SetTextSize(15)
    tex2.Draw() 
    
    canvas4.Print("topMass_Chi2.png")


        
##  write histograms to file
#def writeTransverseMass(datasets_lands):
#    f = ROOT.TFile.Open(output, "RECREATE")
#    hmtSum.SetDirectory(f)
#    f.Write()
#    f.Close()
##########################################################

# plots for selected jets
    ptBtauSide._setLegendStyles()
    ptBtauSide._setLegendLabels()
    ptBtauSide.histoMgr.setHistoDrawStyleAll("P")
    ptBtauSide.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    hptBtauSide = ptBtauSide.histoMgr.getHisto("TTToHplus_M80").getRootHisto().Clone(analysis+"/BjetSelection/PtBjetTauSide")
    ptBtopSide._setLegendStyles()
    ptBtopSide._setLegendLabels()
    ptBtopSide.histoMgr.setHistoDrawStyleAll("P")
    ptBtopSide.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    hptBtopSide = ptBtopSide.histoMgr.getHisto("TTToHplus_M80").getRootHisto().Clone(analysis+"/BjetSelection/PtBjetTopSide")
    ptBtauSideTrue._setLegendStyles()
    ptBtauSideTrue._setLegendLabels()
    ptBtauSideTrue.histoMgr.setHistoDrawStyleAll("P")
    ptBtauSideTrue.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    hptBtauSideTrue = ptBtauSideTrue.histoMgr.getHisto("TTToHplus_M80").getRootHisto().Clone(analysis+"/BjetSelection/PtBjetTauSideTrue")
    ptBtopSideTrue._setLegendStyles()
    ptBtopSideTrue._setLegendLabels()
    ptBtopSideTrue.histoMgr.setHistoDrawStyleAll("P")
    ptBtopSideTrue.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    hptBtopSideTrue = ptBtopSideTrue.histoMgr.getHisto("TTToHplus_M80").getRootHisto().Clone(analysis+"/BjetSelection/PtBjetTopSideTrue")

    deltaTauB._setLegendStyles()
    deltaTauB._setLegendLabels()
    deltaTauB.histoMgr.setHistoDrawStyleAll("P")
    deltaTauB.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    hdeltaTauB = deltaTauB.histoMgr.getHisto("TTToHplus_M80").getRootHisto().Clone(analysis+"/BjetSelection/DeltaTauB")
    deltaMin._setLegendStyles()
    deltaMin._setLegendLabels()
    deltaMin.histoMgr.setHistoDrawStyleAll("P")
    deltaMin.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    hdeltaMin = deltaMin.histoMgr.getHisto("TTToHplus_M80").getRootHisto().Clone(analysis+"/BjetSelection/DeltaMinTauB")
    
    deltaMax._setLegendStyles()
    deltaMax._setLegendLabels()
    deltaMax.histoMgr.setHistoDrawStyleAll("P")
    deltaMax.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    hdeltaMax = deltaMax.histoMgr.getHisto("TTToHplus_M80").getRootHisto().Clone(analysis+"/BjetSelection/DeltaMaxTauB")
    
    deltaMinTrue._setLegendStyles()
    deltaMinTrue._setLegendLabels()
    deltaMinTrue.histoMgr.setHistoDrawStyleAll("P")
    deltaMinTrue.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    hdeltaMinTrue = deltaMinTrue.histoMgr.getHisto("TTToHplus_M80").getRootHisto().Clone(analysis+"/BjetSelection/DeltaMinTauBTrue")
    
    deltaMaxTrue._setLegendStyles()
    deltaMaxTrue._setLegendLabels()
    deltaMaxTrue.histoMgr.setHistoDrawStyleAll("P")
    deltaMaxTrue.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    hdeltaMaxTrue = deltaMaxTrue.histoMgr.getHisto("TTToHplus_M80").getRootHisto().Clone(analysis+"/BjetSelection/DeltaMaxTopBTrue")
    
    pttoptopMatch._setLegendStyles()
    pttoptopMatch._setLegendLabels()
    pttoptopMatch.histoMgr.setHistoDrawStyleAll("P")
    pttoptopMatch.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    hpttoptopMatch = pttoptopMatch.histoMgr.getHisto("TTToHplus_M80").getRootHisto().Clone(analysis+"/BjetSelection/PtTopTop_matchJets")
    pttoptauMatch._setLegendStyles()
    pttoptauMatch._setLegendLabels()
    pttoptauMatch.histoMgr.setHistoDrawStyleAll("P")
    pttoptauMatch.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    hpttoptauMatch = pttoptauMatch.histoMgr.getHisto("TTToHplus_M80").getRootHisto().Clone(analysis+"/BjetSelection/PtTopHiggs_matchJets")


#######################################################    
    canvasj4 = ROOT.TCanvas("canvasj4","",500,500)
#    canvasj4.SetLogy()
    hptBtauSide.SetMaximum(40.0)
    hptBtauSide.SetMarkerColor(2)
    hptBtauSide.SetMarkerSize(1)
    hptBtauSide.SetMarkerStyle(24)
    hptBtauSide.Draw("EP")
    
    hptBtopSide.SetMarkerColor(4)
    hptBtopSide.SetMarkerSize(1)
    hptBtopSide.SetMarkerStyle(20)
    hptBtopSide.SetFillColor(4)
    hptBtopSide.Draw("same")
    
    hptBtauSide.GetYaxis().SetTitle("Events / 10 GeV/c^{2}")
#    hmt.GetYaxis().SetTitleSize(20.0)
    hptBtauSide.GetYaxis().SetTitleOffset(1.5)
    hptBtauSide.GetXaxis().SetTitle("E_{T}^{b jet} (GeV)")
    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       2.18 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    marker1 = ROOT.TMarker(0.6,0.815,hptBtauSide.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(hptBtauSide.GetMarkerColor())
    marker1.SetMarkerSize(0.9*hptBtauSide.GetMarkerSize())
    marker1.Draw()
    tex1 = ROOT.TLatex(0.62,0.8,"#tau side") 
    tex1.SetNDC()
    tex1.SetTextSize(25)
    tex1.Draw() 
    marker2 = ROOT.TMarker(0.6,0.715,hptBtopSide.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(hptBtopSide.GetMarkerColor())
    marker2.SetMarkerSize(0.9*hptBtopSide.GetMarkerSize())
    marker2.Draw()
    tex2 = ROOT.TLatex(0.62,0.7,"top side") 
    tex2.SetNDC()
    tex2.SetTextSize(25)
    tex2.Draw() 
    
    canvasj4.Print("pt_selectedBjet.png")

    
    canvasj4 = ROOT.TCanvas("canvasj9","",500,500)
#    canvasj9.SetLogy()
#    hptBtauSideTrue.SetMaximum(60.0)
    hptBtauSideTrue.SetMarkerColor(2)
    hptBtauSideTrue.SetMarkerSize(1)
    hptBtauSideTrue.SetMarkerStyle(24)
    hptBtauSideTrue.Draw("EP")
    
    hptBtopSideTrue.SetMarkerColor(4)
    hptBtopSideTrue.SetMarkerSize(1)
    hptBtopSideTrue.SetMarkerStyle(20)
    hptBtopSideTrue.SetFillColor(4)
    hptBtopSideTrue.Draw("same")
    
    hptBtauSideTrue.GetYaxis().SetTitle("Events / 10 GeV/c^{2}")
#    hmt.GetYaxis().SetTitleSize(20.0)
    hptBtauSideTrue.GetYaxis().SetTitleOffset(1.5)
    hptBtauSideTrue.GetXaxis().SetTitle("E_{T}^{b jet} (GeV)")
    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       2.18 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    marker1 = ROOT.TMarker(0.6,0.815,hptBtauSideTrue.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(hptBtauSideTrue.GetMarkerColor())
    marker1.SetMarkerSize(0.9*hptBtauSideTrue.GetMarkerSize())
    marker1.Draw()
    tex1 = ROOT.TLatex(0.62,0.8,"#tau side") 
    tex1.SetNDC()
    tex1.SetTextSize(25)
    tex1.Draw() 
    marker2 = ROOT.TMarker(0.6,0.715,hptBtopSideTrue.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(hptBtopSideTrue.GetMarkerColor())
    marker2.SetMarkerSize(0.9*hptBtopSideTrue.GetMarkerSize())
    marker2.Draw()
    tex2 = ROOT.TLatex(0.62,0.7,"top side") 
    tex2.SetNDC()
    tex2.SetTextSize(25)
    tex2.Draw() 
    
    canvasj9.Print("pt_matchedBjets.png")
     
    canvasj1 = ROOT.TCanvas("canvasj1","",500,500)
#    canvasj1.SetLogy()
#    htopSB.SetMinimum(0.1)
    hptBtauSide.SetMarkerColor(2)
    hptBtauSide.SetMarkerSize(1)
    hptBtauSide.SetMarkerStyle(24)
    hptBtauSide.Draw("EP")
    
    hptBtauSideTrue.SetMarkerColor(4)
    hptBtauSideTrue.SetMarkerSize(1)
    hptBtauSideTrue.SetMarkerStyle(20)
    hptBtauSideTrue.SetFillColor(4)
    hptBtauSideTrue.Draw("same")
    
    hptBtauSide.GetYaxis().SetTitle("Events / 10 GeV/c^{2}")
#    hmt.GetYaxis().SetTitleSize(20.0)
    hptBtauSide.GetYaxis().SetTitleOffset(1.5)
    hptBtauSide.GetXaxis().SetTitle("E_{T}^{b jet} (GeV)")
    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       2.18 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    marker1 = ROOT.TMarker(0.5,0.815,hptBtauSide.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(hptBtauSide.GetMarkerColor())
    marker1.SetMarkerSize(0.9*hptBtauSide.GetMarkerSize())
    marker1.Draw()
    tex1 = ROOT.TLatex(0.52,0.8,"#tau side b jet") 
    tex1.SetNDC()
    tex1.SetTextSize(20)
    tex1.Draw() 
    marker2 = ROOT.TMarker(0.5,0.715,hptBtauSideTrue.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(hptBtauSideTrue.GetMarkerColor())
    marker2.SetMarkerSize(0.9*hptBtauSideTrue.GetMarkerSize())
    marker2.Draw()
    tex2 = ROOT.TLatex(0.52,0.7,"mathing #tau-side b jet") 
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw() 
    
    canvasj1.Print("pt_BjetTauSide.png")

    
    canvasj2 = ROOT.TCanvas("canvasj2","",500,500)
#    canvasj2.SetLogy()
#    htopSB.SetMinimum(0.1)
    hptBtopSide.SetMarkerColor(2)
    hptBtopSide.SetMarkerSize(1)
    hptBtopSide.SetMarkerStyle(24)
    hptBtopSide.Draw("EP")
    
    hptBtopSideTrue.SetMarkerColor(4)
    hptBtopSideTrue.SetMarkerSize(1)
    hptBtopSideTrue.SetMarkerStyle(20)
    hptBtopSideTrue.SetFillColor(4)
    hptBtopSideTrue.Draw("same")
    
    hptBtopSide.GetYaxis().SetTitle("Events / 10 GeV/c^{2}")
#    hmt.GetYaxis().SetTitleSize(20.0)
    hptBtopSide.GetYaxis().SetTitleOffset(1.5)
    hptBtopSide.GetXaxis().SetTitle("E_{T}^{b jet} (GeV)")
    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       2.18 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    marker1 = ROOT.TMarker(0.5,0.815,hptBtopSide.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(hptBtopSide.GetMarkerColor())
    marker1.SetMarkerSize(0.9*hptBtopSide.GetMarkerSize())
    marker1.Draw()
    tex1 = ROOT.TLatex(0.52,0.8,"top side b jet") 
    tex1.SetNDC()
    tex1.SetTextSize(20)
    tex1.Draw() 
    marker2 = ROOT.TMarker(0.5,0.715,hptBtopSideTrue.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(hptBtopSideTrue.GetMarkerColor())
    marker2.SetMarkerSize(0.9*hptBtopSideTrue.GetMarkerSize())
    marker2.Draw()
    tex2 = ROOT.TLatex(0.52,0.7,"mathing top-side b jet") 
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw() 
    
    canvasj2.Print("pt_BjetTopSide.png")

      
    canvasj5 = ROOT.TCanvas("canvasj5","",500,500)
#    canvasj5.SetLogy()
#    htopSB.SetMinimum(0.1)
    hdeltaTauB.SetMarkerColor(2)
    hdeltaTauB.SetMarkerSize(1)
    hdeltaTauB.SetMarkerStyle(24)
    hdeltaTauB.Draw("EP")
    
    hdeltaMinTrue.SetMarkerColor(4)
    hdeltaMinTrue.SetMarkerSize(1)
    hdeltaMinTrue.SetMarkerStyle(20)
    hdeltaMinTrue.SetFillColor(4)
    hdeltaMinTrue.Draw("same")

    hdeltaMaxTrue.SetMarkerColor(kGreen+2)
    hdeltaMaxTrue.SetMarkerSize(1)
    hdeltaMaxTrue.SetMarkerStyle(21)
    hdeltaMaxTrue.SetFillColor(4)
    hdeltaMaxTrue.Draw("same")
    
    hdeltaTauB.GetYaxis().SetTitle("Events ")
#    hmt.GetYaxis().SetTitleSize(20.0)
    hdeltaTauB.GetYaxis().SetTitleOffset(1.5)
    hdeltaTauB.GetXaxis().SetTitle("#DeltaR(#tau jet,b jet)")
    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       2.18 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    marker1 = ROOT.TMarker(0.63,0.61,hdeltaTauB.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(hdeltaTauB.GetMarkerColor())
    marker1.SetMarkerSize(0.9*hdeltaTauB.GetMarkerSize())
    marker1.Draw()
    tex1 = ROOT.TLatex(0.65,0.6,"all b jets") 
    tex1.SetNDC()
    tex1.SetTextSize(15)
    tex1.Draw() 
    marker2 = ROOT.TMarker(0.63,0.56,hdeltaMinTrue.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(hdeltaMinTrue.GetMarkerColor())
    marker2.SetMarkerSize(0.9*hdeltaMinTrue.GetMarkerSize())
    marker2.Draw()
    tex2 = ROOT.TLatex(0.65,0.55,"matching #tau-side b jet") 
    tex2.SetNDC()
    tex2.SetTextSize(15)
    tex2.Draw() 
    marker3 = ROOT.TMarker(0.63,0.51,hdeltaMaxTrue.GetMarkerStyle())
    marker3.SetNDC()
    marker3.SetMarkerColor(hdeltaMaxTrue.GetMarkerColor())
    marker3.SetMarkerSize(0.9*hdeltaMaxTrue.GetMarkerSize())
    marker3.Draw()
    tex3 = ROOT.TLatex(0.65,0.5,"mathing top-side b jet") 
    tex3.SetNDC()
    tex3.SetTextSize(15)
    tex3.Draw()     
    canvasj5.Print("deltaRmatched.png")

    canvasj6 = ROOT.TCanvas("canvasj6","",500,500)
#    canvasj5.SetLogy()
    hpttoptauMatch.SetMaximum(50.0)
    hpttoptauMatch.SetMarkerColor(2)
    hpttoptauMatch.SetMarkerSize(1)
    hpttoptauMatch.SetMarkerStyle(24)
    hpttoptauMatch.Draw("EP")
    
    hpttoptopMatch.SetMarkerColor(4)
    hpttoptopMatch.SetMarkerSize(1)
    hpttoptopMatch.SetMarkerStyle(20)
    hpttoptopMatch.SetFillColor(4)
    hpttoptopMatch.Draw("same")
    
    hpttoptauMatch.GetYaxis().SetTitle("Events / 10 GeV/c^{2}")
#    hmt.GetYaxis().SetTitleSize(20.0)
    hpttoptauMatch.GetYaxis().SetTitleOffset(1.5)
    hpttoptauMatch.GetXaxis().SetTitle("p_{T}^{top} (GeV)")
    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       2.18 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    tex6 = ROOT.TLatex(0.52,0.85,"Matched jets") 
    tex6.SetNDC()
    tex6.SetTextSize(20)
    tex6.Draw()    
    marker1 = ROOT.TMarker(0.6,0.785,hpttoptauMatch.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(hpttoptauMatch.GetMarkerColor())
    marker1.SetMarkerSize(0.9*hpttoptauMatch.GetMarkerSize())
    marker1.Draw()
    tex1 = ROOT.TLatex(0.62,0.78,"#tau-side b jet") 
    tex1.SetNDC()
    tex1.SetTextSize(20)
    tex1.Draw() 
    marker2 = ROOT.TMarker(0.6,0.715,hpttoptopMatch.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(hpttoptopMatch.GetMarkerColor())
    marker2.SetMarkerSize(0.9*hpttoptopMatch.GetMarkerSize())
    marker2.Draw()
    tex2 = ROOT.TLatex(0.62,0.7,"top-side b jet") 
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw() 
    
    canvasj6.Print("pttop_matched.png")


# plots for ptmax selection
    topmass_ptmax._setLegendStyles()
    topmass_ptmax._setLegendLabels()
    topmass_ptmax.histoMgr.setHistoDrawStyleAll("P")
    topmass_ptmax.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    htopmass_ptmax = topmass_ptmax.histoMgr.getHisto("TTToHplus_M80").getRootHisto().Clone(analysis+"/TopSelection/TopMass")
    
    topmass_ptmaxMatch._setLegendStyles()
    topmass_ptmaxMatch._setLegendLabels()
    topmass_ptmaxMatch.histoMgr.setHistoDrawStyleAll("P")
    topmass_ptmaxMatch.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    htopmass_ptmaxMatch = topmass_ptmaxMatch.histoMgr.getHisto("TTToHplus_M80").getRootHisto().Clone(analysis+"/TopSelection/TopMass_fullMatch")
    
    wmass_ptmax._setLegendStyles()
    wmass_ptmax._setLegendLabels()
    wmass_ptmax.histoMgr.setHistoDrawStyleAll("P")
    wmass_ptmax.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    hwmass_ptmax = wmass_ptmax.histoMgr.getHisto("TTToHplus_M80").getRootHisto().Clone(analysis+"/TopSelection/WMass")
    
    wmass_ptmaxMatch._setLegendStyles()
    wmass_ptmaxMatch._setLegendLabels()
    wmass_ptmaxMatch.histoMgr.setHistoDrawStyleAll("P")
    wmass_ptmaxMatch.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    hwmass_ptmaxMatch = wmass_ptmaxMatch.histoMgr.getHisto("TTToHplus_M80").getRootHisto().Clone(analysis+"/TopSelection/WMass_fullMatch")       

    topPttt._setLegendStyles()
    topPttt._setLegendLabels()
    topPttt.histoMgr.setHistoDrawStyleAll("P")
    topPttt.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    htopPttt = topPttt.histoMgr.getHisto("TTJets").getRootHisto().Clone(analysis+"/TopSelection/TopMass")

    topPtWjet._setLegendStyles()
    topPtWjet._setLegendLabels()
    topPtWjet.histoMgr.setHistoDrawStyleAll("P")
    topPtWjet.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    htopPtWjet = topPtWjet.histoMgr.getHisto("WJets").getRootHisto().Clone(analysis+"/TopSelection/TopMass")

    topPtSingle._setLegendStyles()
    topPtSingle._setLegendLabels()
    topPtSingle.histoMgr.setHistoDrawStyleAll("P")
    topPtSingle.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    htopPtSingle = topPtSingle.histoMgr.getHisto("SingleTop").getRootHisto().Clone(analysis+"/TopSelection/TopMass")

    topPtDibos._setLegendStyles()
    topPtDibos._setLegendLabels()
    topPtDibos.histoMgr.setHistoDrawStyleAll("P")
    topPtDibos.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    htopPtDibos = topPtDibos.histoMgr.getHisto("Diboson").getRootHisto().Clone(analysis+"/TopSelection/TopMass")


    
    canvasp4 = ROOT.TCanvas("canvasp4","",500,500)
#    canvasp4.SetLogy()
#    htopSB.SetMinimum(0.1)
    htopmass_ptmax.SetMarkerColor(2)
    htopmass_ptmax.SetMarkerSize(1)
    htopmass_ptmax.SetMarkerStyle(24)
    htopmass_ptmax.Draw("EP")
    
    htopmass_ptmaxMatch.SetMarkerColor(4)
    htopmass_ptmaxMatch.SetMarkerSize(1)
    htopmass_ptmaxMatch.SetMarkerStyle(20)
    htopmass_ptmaxMatch.SetFillColor(4)
    htopmass_ptmaxMatch.Draw("same")
    
    htopmass_ptmax.GetYaxis().SetTitle("Events / 10 GeV/c^{2}")
#    hmt.GetYaxis().SetTitleSize(20.0)
    htopmass_ptmax.GetYaxis().SetTitleOffset(1.5)
    htopmass_ptmax.GetXaxis().SetTitle("m_{top} (GeV/c^{2})")
    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       2.18 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    tex5 = ROOT.TLatex(0.6,0.8,"Signal, m_{H^{#pm}}= 120 GeV/c^{2}") 
    tex5.SetNDC()
    tex5.SetTextSize(15)
    tex5.Draw()   
    marker1 = ROOT.TMarker(0.6,0.715,htopmass_ptmax.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(htopmass_ptmax.GetMarkerColor())
    marker1.SetMarkerSize(0.9*htopmass_ptmax.GetMarkerSize())
    marker1.Draw()
    tex1 = ROOT.TLatex(0.62,0.7,"All combinations") 
    tex1.SetNDC()
    tex1.SetTextSize(20)
    tex1.Draw() 
    marker2 = ROOT.TMarker(0.6,0.615,htopmass_ptmaxMatch.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(htopmass_ptmaxMatch.GetMarkerColor())
    marker2.SetMarkerSize(0.9*htopmass_ptmaxMatch.GetMarkerSize())
    marker2.Draw()
    tex2 = ROOT.TLatex(0.62,0.6,"Matching jets") 
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw()     
    canvasp4.Print("topMass_ptmax_match.png")
    
    canvasp3 = ROOT.TCanvas("canvasp3","",500,500)
#    canvasp4.SetLogy()
#    htopSB.SetMinimum(0.1)
    hwmass_ptmax.SetMarkerColor(2)
    hwmass_ptmax.SetMarkerSize(1)
    hwmass_ptmax.SetMarkerStyle(24)
    hwmass_ptmax.Draw("EP")
    
    hwmass_ptmaxMatch.SetMarkerColor(4)
    hwmass_ptmaxMatch.SetMarkerSize(1)
    hwmass_ptmaxMatch.SetMarkerStyle(20)
    hwmass_ptmaxMatch.SetFillColor(4)
    hwmass_ptmaxMatch.Draw("same")
    
    hwmass_ptmax.GetYaxis().SetTitle("Events / 10 GeV/c^{2}")
#    hmt.GetYaxis().SetTitleSize(20.0)
    hwmass_ptmax.GetYaxis().SetTitleOffset(1.5)
    hwmass_ptmax.GetXaxis().SetTitle("m_{W} (GeV/c^{2})")
    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       2.18 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    tex5 = ROOT.TLatex(0.6,0.8,"Signal, m_{H^{#pm}}= 120 GeV/c^{2}") 
    tex5.SetNDC()
    tex5.SetTextSize(15)
    tex5.Draw()   
    marker1 = ROOT.TMarker(0.6,0.715,hwmass_ptmax.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(hwmass_ptmax.GetMarkerColor())
    marker1.SetMarkerSize(0.9*hwmass_ptmax.GetMarkerSize())
    marker1.Draw()
    tex1 = ROOT.TLatex(0.62,0.7,"All combinations") 
    tex1.SetNDC()
    tex1.SetTextSize(20)
    tex1.Draw() 
    marker2 = ROOT.TMarker(0.6,0.615,hwmass_ptmaxMatch.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(hwmass_ptmaxMatch.GetMarkerColor())
    marker2.SetMarkerSize(0.9*hwmass_ptmaxMatch.GetMarkerSize())
    marker2.Draw()
    tex2 = ROOT.TLatex(0.62,0.6,"Matching jets") 
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw() 
    
    canvasp3.Print("wMass_ptmax_match.png")
    
    canvasp6 = ROOT.TCanvas("canvasp6","",500,500)
#    canvas6.SetLogy()
#    htopSB.SetMinimum(0.1)
    htopmass_ptmax.SetMarkerColor(2)
    htopmass_ptmax.SetMarkerSize(1)
    htopmass_ptmax.SetMarkerStyle(21)
    htopmass_ptmax.Draw("EP")
    
    htopPttt.SetMarkerColor(4)
    htopPttt.SetMarkerSize(1)
    htopPttt.SetMarkerStyle(24)
    htopPttt.SetFillColor(4)
    htopPttt.Draw("same")

    htopPtWjet.SetMarkerColor(1)
    htopPtWjet.SetMarkerSize(1)
    htopPtWjet.SetMarkerStyle(22)
    htopPtWjet.SetFillColor(1)
    htopPtWjet.Draw("same")
    
    htopPtSingle.SetMarkerColor(6)
    htopPtSingle.SetMarkerSize(1)
    htopPtSingle.SetMarkerStyle(23)
    htopPtSingle.SetFillColor(6)
    htopPtSingle.Draw("same")
    
    htopPtDibos.SetMarkerColor(7)
    htopPtDibos.SetMarkerSize(1)
    htopPtDibos.SetMarkerStyle(20)
    htopPtDibos.SetFillColor(7)
    htopPtDibos.Draw("same")

    htopmass_ptmax.GetYaxis().SetTitle("Events / 10 GeV/c^{2}")
#    hmt.GetYaxis().SetTitleSize(20.0)
    htopmass_ptmax.GetYaxis().SetTitleOffset(1.5)
    htopmass_ptmax.GetXaxis().SetTitle("m_{top} (GeV/c^{2})")
    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       2.18 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    marker1 = ROOT.TMarker(0.6,0.815,htopmass_ptmax.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(htopmass_ptmax.GetMarkerColor())
    marker1.SetMarkerSize(0.9*htopmass_ptmax.GetMarkerSize())
    marker1.Draw()
    tex1 = ROOT.TLatex(0.62,0.8,"Signal") 
    tex1.SetNDC()
    tex1.SetTextSize(20)
    tex1.Draw() 
    marker2 = ROOT.TMarker(0.6,0.755,htopPttt.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(htopPttt.GetMarkerColor())
    marker2.SetMarkerSize(0.9*htopPttt.GetMarkerSize())
    marker2.Draw()
    tex2 = ROOT.TLatex(0.62,0.75,"tt ") 
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw() 
    marker3 = ROOT.TMarker(0.6,0.715,htopPtWjet.GetMarkerStyle())
    marker3.SetNDC()
    marker3.SetMarkerColor(htopPtWjet.GetMarkerColor())
    marker3.SetMarkerSize(0.9*htopPtWjet.GetMarkerSize())
    marker3.Draw()
    tex3 = ROOT.TLatex(0.62,0.7,"Wjet") 
    tex3.SetNDC()
    tex3.SetTextSize(20)
    tex3.Draw() 
    marker5 = ROOT.TMarker(0.6,0.655,htopPtSingle.GetMarkerStyle())
    marker5.SetNDC()
    marker5.SetMarkerColor(htopPtSingle.GetMarkerColor())
    marker5.SetMarkerSize(0.9*htopPtSingle.GetMarkerSize())
    marker5.Draw()
    tex5 = ROOT.TLatex(0.62,0.65,"Single top") 
    tex5.SetNDC()
    tex5.SetTextSize(20)
    tex5.Draw()
    marker6 = ROOT.TMarker(0.6,0.605,htopPtDibos.GetMarkerStyle())
    marker6.SetNDC()
    marker6.SetMarkerColor(htopPtDibos.GetMarkerColor())
    marker6.SetMarkerSize(0.9*htopPtDibos.GetMarkerSize())
    marker6.Draw()
    tex6 = ROOT.TLatex(0.62,0.6,"Di boson") 
    tex6.SetNDC()
    tex6.SetTextSize(20)
    tex6.Draw()
       
    canvasp6.Print("topMass_ptmax_all.png")


    htopPtBg = htopPttt.Clone("bgSum")
#    hmtSum.SetName("mtSum")
#    hmtSum.SetTitle("Inverted tau ID")
    htopPtBg.Add(htopPtWjet)
    htopPtBg.Add(htopPtSingle)
    htopPtBg.Add(htopPtDibos)

    htopPtSB = htopPtBg.Clone("SoverBG")
    htopPtSB.Add(htopmass_ptmax)

        
    canvasp7 = ROOT.TCanvas("canvasp7","",500,500)
#    canvas7.SetLogy()
#    htopSB.SetMinimum(0.1)
    htopPtSB.SetMarkerColor(2)
    htopPtSB.SetMarkerSize(1)
    htopPtSB.SetMarkerStyle(24)
    htopPtSB.Draw("EP")
    
    htopPtBg.SetMarkerColor(4)
    htopPtBg.SetMarkerSize(1)
    htopPtBg.SetMarkerStyle(20)
    htopPtBg.SetFillColor(4)
    htopPtBg.Draw("same")
    
    htopPtSB.GetYaxis().SetTitle("Events / 10 GeV/c^{2}")
#    hmt.GetYaxis().SetTitleSize(20.0)
    htopPtSB.GetYaxis().SetTitleOffset(1.5)
    htopPtSB.GetXaxis().SetTitle("m_{top} (GeV/c^{2})")
    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       2.18 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    marker1 = ROOT.TMarker(0.6,0.815,htopPtSB.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(htopPtSB.GetMarkerColor())
    marker1.SetMarkerSize(0.9*htopPtSB.GetMarkerSize())
    marker1.Draw()
    tex1 = ROOT.TLatex(0.62,0.8,"Signal + tt and EW Bg") 
    tex1.SetNDC()
    tex1.SetTextSize(15)
    tex1.Draw() 
    marker2 = ROOT.TMarker(0.6,0.715,htopPtBg.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(htopPtBg.GetMarkerColor())
    marker2.SetMarkerSize(0.9*htopPtBg.GetMarkerSize())
    marker2.Draw()
    tex2 = ROOT.TLatex(0.62,0.7,"tt and EW Background") 
    tex2.SetNDC()
    tex2.SetTextSize(15)
    tex2.Draw() 
    
    canvasp7.Print("topMassSB_ptmax.png")

    
##################################
##################################
    # plot gen particles
    
    drTopSide = plots.PlotBase([datasets.getDataset("TTToHplus_M80").getDatasetRootHisto(analysis+"/GenParticleAnalysis/genBquark_FromTopSide_DeltaRTau")])
    drHiggsSide = plots.PlotBase([datasets.getDataset("TTToHplus_M80").getDatasetRootHisto(analysis+"/GenParticleAnalysis/genBquark_FromHiggsSide_DeltaRTau")])

    drTopSide.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    drHiggsSide.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())

    drTopSide._setLegendStyles()
    drTopSide._setLegendLabels()
    drTopSide.histoMgr.setHistoDrawStyleAll("P")
    drTopSide.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))    
    hdrTopSide = drTopSide.histoMgr.getHisto("TTToHplus_M80").getRootHisto().Clone(analysis+"/GenParticleAnalysis/genBquark_FromTopSide_DeltaRTau")
    drHiggsSide._setLegendStyles()
    drHiggsSide._setLegendLabels()
    drHiggsSide.histoMgr.setHistoDrawStyleAll("P")
    drHiggsSide.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))    
    hdrHiggsSide = drHiggsSide.histoMgr.getHisto("TTToHplus_M80").getRootHisto().Clone(analysis+"/GenParticleAnalysis/genBquark_FromHiggsSide_DeltaRTau")    


    
    canvasg1 = ROOT.TCanvas("canvasg1","",500,500)
#    canvasg1.SetLogy()
#    htopSB.SetMinimum(0.1)
    hdrTopSide.SetMarkerColor(2)
    hdrTopSide.SetMarkerSize(1)
    hdrTopSide.SetMarkerStyle(24)
    hdrTopSide.Draw("EP")
    
    hdrHiggsSide.SetMarkerColor(4)
    hdrHiggsSide.SetMarkerSize(1)
    hdrHiggsSide.SetMarkerStyle(20)
    hdrHiggsSide.SetFillColor(4)
    hdrHiggsSide.Draw("same")
    
    hdrTopSide.GetYaxis().SetTitle("Events")
#    hmt.GetYaxis().SetTitleSize(20.0)
    hdrTopSide.GetYaxis().SetTitleOffset(1.5)
    hdrTopSide.GetXaxis().SetTitle("#DeltaR(#tau jet, b quark)")
    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       2.18 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    marker1 = ROOT.TMarker(0.6,0.815,hdrTopSide.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(hdrTopSide.GetMarkerColor())
    marker1.SetMarkerSize(0.9*hdrTopSide.GetMarkerSize())
    marker1.Draw()
    tex1 = ROOT.TLatex(0.62,0.8,"b from t -> bW") 
    tex1.SetNDC()
    tex1.SetTextSize(20)
    tex1.Draw() 
    marker2 = ROOT.TMarker(0.6,0.715,hdrHiggsSide.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(hdrHiggsSide.GetMarkerColor())
    marker2.SetMarkerSize(0.9*hdrHiggsSide.GetMarkerSize())
    marker2.Draw()
    tex2 = ROOT.TLatex(0.62,0.7,"b from t -> bH^{+}") 
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw() 
    
    canvasg1.Print("deltaRtaubquark.png")

## pt of b quarks
    ptTopSide = plots.PlotBase([datasets.getDataset("TTToHplus_M80").getDatasetRootHisto(analysis+"/GenParticleAnalysis/genBquark_FromTopSide_Pt")])
    ptHiggsSide = plots.PlotBase([datasets.getDataset("TTToHplus_M80").getDatasetRootHisto(analysis+"/GenParticleAnalysis/genBquark_FromHiggsSide_Pt")])

    ptTopSide.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    ptHiggsSide.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())

    ptTopSide._setLegendStyles()
    ptTopSide._setLegendLabels()
    ptTopSide.histoMgr.setHistoDrawStyleAll("P")
    ptTopSide.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))    
    hptTopSide = ptTopSide.histoMgr.getHisto("TTToHplus_M80").getRootHisto().Clone(analysis+"/GenParticleAnalysis/genBquark_FromTopSide_Pt")
    ptHiggsSide._setLegendStyles()
    ptHiggsSide._setLegendLabels()
    ptHiggsSide.histoMgr.setHistoDrawStyleAll("P")
    ptHiggsSide.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))    
    hptHiggsSide = ptHiggsSide.histoMgr.getHisto("TTToHplus_M80").getRootHisto().Clone(analysis+"/GenParticleAnalysis/genBquark_FromHiggsSide_Pt")    
    
    canvasg2 = ROOT.TCanvas("canvasg2","",500,500)
    canvasg2.SetLogy()
    hptTopSide.SetMaximum(2000)
    hptTopSide.SetMarkerColor(2)
    hptTopSide.SetMarkerSize(1)
    hptTopSide.SetMarkerStyle(24)
    hptTopSide.Draw("EP")
    
    hptHiggsSide.SetMarkerColor(4)
    hptHiggsSide.SetMarkerSize(1)
    hptHiggsSide.SetMarkerStyle(20)
    hptHiggsSide.SetFillColor(4)
    hptHiggsSide.Draw("same")
    
    hptTopSide.GetYaxis().SetTitle("Events")
#    hmt.GetYaxis().SetTitleSize(20.0)
    hptTopSide.GetYaxis().SetTitleOffset(1.5)
    hptTopSide.GetXaxis().SetTitle("p_{T}^{b quark} (GeV/c)")
    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       2.18 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    marker1 = ROOT.TMarker(0.6,0.815,hptTopSide.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(hptTopSide.GetMarkerColor())
    marker1.SetMarkerSize(0.9*hptTopSide.GetMarkerSize())
    marker1.Draw()
    tex1 = ROOT.TLatex(0.62,0.8,"b from t -> bW") 
    tex1.SetNDC()
    tex1.SetTextSize(20)
    tex1.Draw() 
    marker2 = ROOT.TMarker(0.6,0.715,hptHiggsSide.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(hptHiggsSide.GetMarkerColor())
    marker2.SetMarkerSize(0.9*hptHiggsSide.GetMarkerSize())
    marker2.Draw()
    tex2 = ROOT.TLatex(0.62,0.7,"b from t -> bH^{+}") 
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw() 
    
    canvasg2.Print("gen_ptBquarks_log.png")

    
#############################################
## eta of b quarks
    etaTopSide = plots.PlotBase([datasets.getDataset("TTToHplus_M80").getDatasetRootHisto(analysis+"/GenParticleAnalysis/genBquark_FromTopSide_Eta")])
    etaHiggsSide = plots.PlotBase([datasets.getDataset("TTToHplus_M80").getDatasetRootHisto(analysis+"/GenParticleAnalysis/genBquark_FromHiggsSide_Eta")])

    etaTopSide.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    etaHiggsSide.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())

    etaTopSide._setLegendStyles()
    etaTopSide._setLegendLabels()
    etaTopSide.histoMgr.setHistoDrawStyleAll("P")
    etaTopSide.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))    
    hetaTopSide = etaTopSide.histoMgr.getHisto("TTToHplus_M80").getRootHisto().Clone(analysis+"/GenParticleAnalysis/genBquark_FromTopSide_Eta")
    etaHiggsSide._setLegendStyles()
    etaHiggsSide._setLegendLabels()
    etaHiggsSide.histoMgr.setHistoDrawStyleAll("P")
    etaHiggsSide.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))    
    hetaHiggsSide = etaHiggsSide.histoMgr.getHisto("TTToHplus_M80").getRootHisto().Clone(analysis+"/GenParticleAnalysis/genBquark_FromHiggsSide_Eta")    
    
    canvasg3 = ROOT.TCanvas("canvasg3","",500,500)
#    canvasg3.SetLogy()
#    htopSB.SetMinimum(0.1)
    hetaTopSide.SetMarkerColor(2)
    hetaTopSide.SetMarkerSize(1)
    hetaTopSide.SetMarkerStyle(24)
    hetaTopSide.Draw("EP")
    
    hetaHiggsSide.SetMarkerColor(4)
    hetaHiggsSide.SetMarkerSize(1)
    hetaHiggsSide.SetMarkerStyle(20)
    hetaHiggsSide.SetFillColor(4)
    hetaHiggsSide.Draw("same")
    
    hetaTopSide.GetYaxis().SetTitle("Events")
#    hmt.GetYaxis().SetTitleSize(20.0)
    hetaTopSide.GetYaxis().SetTitleOffset(1.5)
    hetaTopSide.GetXaxis().SetTitle("#eta^{b quark}")
    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       2.18 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    marker1 = ROOT.TMarker(0.2,0.815,hetaTopSide.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(hetaTopSide.GetMarkerColor())
    marker1.SetMarkerSize(0.9*hetaTopSide.GetMarkerSize())
    marker1.Draw()
    tex1 = ROOT.TLatex(0.22,0.8,"b from t -> bW") 
    tex1.SetNDC()
    tex1.SetTextSize(20)
    tex1.Draw() 
    marker2 = ROOT.TMarker(0.2,0.715,hetaHiggsSide.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(hetaHiggsSide.GetMarkerColor())
    marker2.SetMarkerSize(0.9*hetaHiggsSide.GetMarkerSize())
    marker2.Draw()
    tex2 = ROOT.TLatex(0.22,0.7,"b from t -> bH^{+}") 
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw() 
    
    canvasg3.Print("gen_etaBquarks.png")

    
#####################################################

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
    normalization = 0.00606 * 0.86
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

# Common formatting
def common(h, xlabel, ylabel, addLuminosityText=True):
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    if addLuminosityText:
        h.addLuminosityText()
    h.save()

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
    xlabel = "Cut"
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
    
# Call the main function if the script is executed (i.e. not imported)
if __name__ == "__main__":
    main()
