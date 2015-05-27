#!/usr/bin/env python

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

analysis = "signalAnalysis"
counters = analysis+"/counters"
dataEra = "Run2011AB"

treeDraw = dataset.TreeDraw(analysis+"/tree", weight="weightPileup")

def main():
    datasets = dataset.getDatasetsFromMulticrabCfg(counters=counters, dataEra=dataEra)
    datasets.updateNAllEventsToPUWeighted()
    datasets.loadLuminosities()
    
#    datasets.getDataset("HplusTB_M180_Fall11").setCrossSection(0.363)
#    datasets.getDataset("HplusTB_M190_Fall11").setCrossSection(0.2666)
    datasets.getDataset("HplusTB_M200_Fall11").setCrossSection(0.1915)
#    datasets.getDataset("HplusTB_M250_Fall11").setCrossSection(0.051)
#    datasets.getDataset("HplusTB_M300_Fall11").setCrossSection(0.0213)
    
    plots.mergeRenameReorderForDataMC(datasets)
    print "Int.Lumi",datasets.getDataset("Data").getLuminosity()
#    datasets.remove(filter(lambda name: "TTToHplus" in name and not "M120" in name, datasets.getAllDatasetNames()))
#    datasets.remove(filter(lambda name: "HplusTB" in name, datasets.getAllDatasetNames()))
    
    style = tdrstyle.TDRStyle()




#    datasets3 = dataset.getDatasetsFromMulticrabCfg(cfgfile="/home/rkinnune/signalAnalysis/CMSSW_4_4_4/src/HiggsAnalysis/HeavyChHiggsToTauNu/test/multicrab_120607_075512/multicrab.cfg", counters=counters)
#    datasets3.updateNAllEventsToPUWeighted()
#    datasets3.loadLuminosities()
#    plots.mergeRenameReorderForDataMC(datasets3)
#    datasets2.selectAndReorder(["TTJets_TuneZ2_Fall11","TTToHplusBWB_M120_Fall11"])
#    datasets2.rename("TTJets_TuneZ2_Fall11","TTJets2")
#    datasets2.rename("TTToHplusBWB_M120_Fall11","TTToHplusBWB_M120_2")     
#    datasets.extend(datasets2)     

#    plot(datasets, datasets2, datasets3)
    
    plot(datasets)
    printCounters(datasets)





def plot(datasets):
    

    
############################################################
    mt = plots.PlotBase([datasets.getDataset("TTJets").getDatasetRootHisto(analysis+"/transverseMass")])
    mtMuonNotInTau = plots.PlotBase([datasets.getDataset("TTJets").getDatasetRootHisto(analysis+"/transverseMassMuonNotInTau")])
    mtElectronNotInTau = plots.PlotBase([datasets.getDataset("TTJets").getDatasetRootHisto(analysis+"/transverseMassElectronNotInTau")])
    mtTauNotInTau = plots.PlotBase([datasets.getDataset("TTJets").getDatasetRootHisto(analysis+"/transverseMassTauNotInTau")])
    mtLeptonNotInTau = plots.PlotBase([datasets.getDataset("TTJets").getDatasetRootHisto(analysis+"/transverseMassLeptonNotInTau")])
    mtNoLeptonNotInTau = plots.PlotBase([datasets.getDataset("TTJets").getDatasetRootHisto(analysis+"/transverseMassNoLeptonNotInTau")])
    mtNoLeptonGoodMet = plots.PlotBase([datasets.getDataset("TTJets").getDatasetRootHisto(analysis+"/transverseMassNoLeptonGoodMet")])
    mtNoLeptonGoodMetGoodTau = plots.PlotBase([datasets.getDataset("TTJets").getDatasetRootHisto(analysis+"/transverseMassNoLeptonGoodMetGoodTau")])
    mtTopChiSelection = plots.PlotBase([datasets.getDataset("TTJets").getDatasetRootHisto(analysis+"/transverseMassTopChiSelection")])
    mtWMassSelection = plots.PlotBase([datasets.getDataset("TTJets").getDatasetRootHisto(analysis+"/transverseMassWmassCut")])
    mtTauVeto = plots.PlotBase([datasets.getDataset("TTJets").getDatasetRootHisto(analysis+"/transverseMassTauVeto")])

    mtLeptonRealSignalTau = plots.PlotBase([datasets.getDataset("TTJets").getDatasetRootHisto(analysis+"/transverseMassLeptonRealSignalTau")])
    mtLeptonFakeSignalTau = plots.PlotBase([datasets.getDataset("TTJets").getDatasetRootHisto(analysis+"/transverseMassLeptonFakeSignalTau")])
    mtObservableLeptons = plots.PlotBase([datasets.getDataset("TTJets").getDatasetRootHisto(analysis+"/transverseMassObservableLeptons")])
    mtNoObservableLeptons = plots.PlotBase([datasets.getDataset("TTJets").getDatasetRootHisto(analysis+"/transverseNoMassObservableLeptons")]) 
        
    mt.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mtElectronNotInTau.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mtMuonNotInTau.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mtTauNotInTau.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mtNoLeptonNotInTau.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mtLeptonNotInTau.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mtNoLeptonGoodMet.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mtNoLeptonGoodMetGoodTau.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mtTopChiSelection.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mtWMassSelection.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())    
    mtLeptonRealSignalTau.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mtLeptonFakeSignalTau.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mtObservableLeptons.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mtNoObservableLeptons.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mtTauVeto.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    
    mtMetReso02 = plots.PlotBase([datasets.getDataset("TTJets").getDatasetRootHisto(analysis+"/transverseMassMetReso02")])
    deltaEtMetGenMet = plots.PlotBase([datasets.getDataset("TTJets").getDatasetRootHisto(analysis+"/deltaEtMetGenMet")])
    deltaPhiMetGenMet = plots.PlotBase([datasets.getDataset("TTJets").getDatasetRootHisto(analysis+"/deltaPhiMetGenMet")])  
    deltaEtMetGenMet.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    
    deltaPhiMetGenMet.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mtMetReso02.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())

    mtLeptonRealSignalTau._setLegendStyles()
    mtLeptonRealSignalTau._setLegendLabels()
    mtLeptonRealSignalTau.histoMgr.setHistoDrawStyleAll("P")
    mtLeptonRealSignalTau.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    hmtLeptonRealSignalTau = mtLeptonRealSignalTau.histoMgr.getHisto("TTJets").getRootHisto().Clone(analysis+"/transverseMassLeptonRealSignalTau")

    mtTauVeto._setLegendStyles()
    mtTauVeto._setLegendLabels()
    mtTauVeto.histoMgr.setHistoDrawStyleAll("P")
    mtTauVeto.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    hmtTauVeto = mtTauVeto.histoMgr.getHisto("TTJets").getRootHisto().Clone(analysis+"/transverseMassTauVeto")

    mtLeptonFakeSignalTau._setLegendStyles()
    mtLeptonFakeSignalTau._setLegendLabels()
    mtLeptonFakeSignalTau.histoMgr.setHistoDrawStyleAll("P")
    mtLeptonFakeSignalTau.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    hmtLeptonFakeSignalTau = mtLeptonFakeSignalTau.histoMgr.getHisto("TTJets").getRootHisto().Clone(analysis+"/transverseMassLeptonFakeSignalTau")

    mtObservableLeptons._setLegendStyles()
    mtObservableLeptons._setLegendLabels()
    mtObservableLeptons.histoMgr.setHistoDrawStyleAll("P")
    mtObservableLeptons.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    hmtObservableLeptons = mtObservableLeptons.histoMgr.getHisto("TTJets").getRootHisto().Clone(analysis+"/transverseMassObservableLeptons") 
    
    mtNoObservableLeptons._setLegendStyles()
    mtNoObservableLeptons._setLegendLabels()
    mtNoObservableLeptons.histoMgr.setHistoDrawStyleAll("P")
    mtNoObservableLeptons.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    hmtNoObservableLeptons = mtNoObservableLeptons.histoMgr.getHisto("TTJets").getRootHisto().Clone(analysis+"/transverseNoMassObservableLeptons")
    
    mtTopChiSelection._setLegendStyles()
    mtTopChiSelection._setLegendLabels()
    mtTopChiSelection.histoMgr.setHistoDrawStyleAll("P")
    mtTopChiSelection.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    hmtTopChiSelection = mtTopChiSelection.histoMgr.getHisto("TTJets").getRootHisto().Clone(analysis+"/transverseMassTopChiSelection")

    mtWMassSelection._setLegendStyles()
    mtWMassSelection._setLegendLabels()
    mtWMassSelection.histoMgr.setHistoDrawStyleAll("P")
    mtWMassSelection.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    hmtWMassSelection = mtWMassSelection.histoMgr.getHisto("TTJets").getRootHisto().Clone(analysis+"/transverseMassWmassCut")
        
    mtNoLeptonNotInTau._setLegendStyles()
    mtNoLeptonNotInTau._setLegendLabels()
    mtNoLeptonNotInTau.histoMgr.setHistoDrawStyleAll("P")
    mtNoLeptonNotInTau.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    hmtNoLeptonNotInTau = mtNoLeptonNotInTau.histoMgr.getHisto("TTJets").getRootHisto().Clone(analysis+"/transverseMassNoLeptonNotInTau")
    
    mtNoLeptonGoodMet._setLegendStyles()
    mtNoLeptonGoodMet._setLegendLabels()
    mtNoLeptonGoodMet.histoMgr.setHistoDrawStyleAll("P")
    mtNoLeptonGoodMet.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    hmtNoLeptonGoodMet = mtNoLeptonGoodMet.histoMgr.getHisto("TTJets").getRootHisto().Clone(analysis+"/transverseMassNoLeptonGoogMet")
    
    mtNoLeptonGoodMetGoodTau._setLegendStyles()
    mtNoLeptonGoodMetGoodTau._setLegendLabels()
    mtNoLeptonGoodMetGoodTau.histoMgr.setHistoDrawStyleAll("P")
    mtNoLeptonGoodMetGoodTau.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    hmtNoLeptonGoodMetGoodTau = mtNoLeptonGoodMetGoodTau.histoMgr.getHisto("TTJets").getRootHisto().Clone(analysis+"/transverseMassNoLeptonGoogMetGoodTau")

        
    mtLeptonNotInTau._setLegendStyles()
    mtLeptonNotInTau._setLegendLabels()
    mtLeptonNotInTau.histoMgr.setHistoDrawStyleAll("P")
    mtLeptonNotInTau.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    hmtLeptonNotInTau = mtLeptonNotInTau.histoMgr.getHisto("TTJets").getRootHisto().Clone(analysis+"/transverseMassLeptonNotInTau")
    
    mtMuonNotInTau._setLegendStyles()
    mtMuonNotInTau._setLegendLabels()
    mtMuonNotInTau.histoMgr.setHistoDrawStyleAll("P")
    mtMuonNotInTau.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    hmtMuonNotInTau = mtMuonNotInTau.histoMgr.getHisto("TTJets").getRootHisto().Clone(analysis+"/transverseMassMuonNotInTau")

    
    mtElectronNotInTau._setLegendStyles()
    mtElectronNotInTau._setLegendLabels()
    mtElectronNotInTau.histoMgr.setHistoDrawStyleAll("P")
    mtElectronNotInTau.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    hmtElectronNotInTau = mtElectronNotInTau.histoMgr.getHisto("TTJets").getRootHisto().Clone(analysis+"/transverseMassMuonNotInTau")
    
    mtTauNotInTau._setLegendStyles()
    mtTauNotInTau._setLegendLabels()
    mtTauNotInTau.histoMgr.setHistoDrawStyleAll("P")
    mtTauNotInTau.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    hmtTauNotInTau = mtTauNotInTau.histoMgr.getHisto("TTJets").getRootHisto().Clone(analysis+"/transverseMassTauNotInTau")
    
    mt._setLegendStyles()
    mt._setLegendLabels()
    mt.histoMgr.setHistoDrawStyleAll("P")
    mt.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    hmt = mt.histoMgr.getHisto("TTJets").getRootHisto().Clone(analysis+"/transverseMass")
    
    mtMetReso02._setLegendStyles()
    mtMetReso02._setLegendLabels()
    mtMetReso02.histoMgr.setHistoDrawStyleAll("P")
    mtMetReso02.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    hmtMetReso02 = mtMetReso02.histoMgr.getHisto("TTJets").getRootHisto().Clone(analysis+"/transverseMassmtMetReso02")
    
    deltaEtMetGenMet._setLegendStyles()
    deltaEtMetGenMet._setLegendLabels()
    deltaEtMetGenMet.histoMgr.setHistoDrawStyleAll("P")
    deltaEtMetGenMet.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    hdeltaEtMetGenMet = deltaEtMetGenMet.histoMgr.getHisto("TTJets").getRootHisto().Clone(analysis+"/deltaEtMetGenMet")
  
    deltaPhiMetGenMet._setLegendStyles()
    deltaPhiMetGenMet._setLegendLabels()
    deltaPhiMetGenMet.histoMgr.setHistoDrawStyleAll("P")
    deltaPhiMetGenMet.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    
    hdeltaPhiMetGenMet = deltaPhiMetGenMet.histoMgr.getHisto("TTJets").getRootHisto().Clone(analysis+"/deltaPhiMetGenMet")

#########################################################    
    canvas12 = ROOT.TCanvas("canvas12","",500,500)
    canvas12.SetLogy()
    hmt.SetMinimum(0.01)
#    hmt.SetMaximum(17000)
    hmt.SetMarkerColor(4)
    hmt.SetMarkerSize(1)
    hmt.SetMarkerStyle(24)
    hmt.Draw("EP")

    
    hmtLeptonRealSignalTau.SetMarkerColor(7)
    hmtLeptonRealSignalTau.SetMarkerSize(1)
    hmtLeptonRealSignalTau.SetMarkerStyle(21)
    hmtLeptonRealSignalTau.Draw("same")

    hmtLeptonFakeSignalTau.SetMarkerColor(2)
    hmtLeptonFakeSignalTau.SetMarkerSize(1)
    hmtLeptonFakeSignalTau.SetMarkerStyle(20)
    hmtLeptonFakeSignalTau.Draw("same")

    
    hmt.GetYaxis().SetTitle("Events")
    hmt.GetYaxis().SetTitleOffset(1.0)
    hmt.GetXaxis().SetTitle("m_{T}(#tau jet, MET) (GeV/c^{2})")
    
 
    
    tex3 = ROOT.TLatex(0.48,0.9,"All selected events")
    tex3.SetNDC()
    tex3.SetTextSize(18)
    tex3.Draw()    
    marker3 = ROOT.TMarker(0.45,0.91,hmt.GetMarkerStyle())
    marker3.SetNDC()
    marker3.SetMarkerColor(hmt.GetMarkerColor())
    marker3.SetMarkerSize(0.9*hmt.GetMarkerSize())
    marker3.Draw()

    tex2 = ROOT.TLatex(0.48,0.85,"Leptons + real signal #tau")
    tex2.SetNDC()
    tex2.SetTextSize(18)
    tex2.Draw()    
    marker2 = ROOT.TMarker(0.45,0.86,hmtLeptonRealSignalTau.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(hmtLeptonRealSignalTau.GetMarkerColor())
    marker2.SetMarkerSize(0.9*hmtLeptonRealSignalTau.GetMarkerSize())
    marker2.Draw()
    
    tex6 = ROOT.TLatex(0.48,0.80,"Leptons + fake signal #tau")
    tex6.SetNDC()
    tex6.SetTextSize(18)
    tex6.Draw()    
    marker6 = ROOT.TMarker(0.45,0.81,hmtLeptonFakeSignalTau.GetMarkerStyle())
    marker6.SetNDC()
    marker6.SetMarkerColor(hmtLeptonFakeSignalTau.GetMarkerColor())
    marker6.SetMarkerSize(0.9*hmtLeptonFakeSignalTau.GetMarkerSize())
    marker6.Draw()   
    
    tex4 = ROOT.TLatex(0.25,0.96,"7 TeV                          CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(18)
    tex4.Draw()
    
#    tex5 = ROOT.TLatex(0.3,0.2,"m_{H^{#pm}} = 200 GeV/c^{2}")
    tex5 = ROOT.TLatex(0.25,0.3,"tt+jets") 
    tex5.SetNDC()
    tex5.SetTextSize(20)
    tex5.Draw()
    
    tex7 = ROOT.TLatex(0.25,0.15,"tan#beta = 30")
    tex7.SetNDC()
    tex7.SetTextSize(20)
#    tex7.Draw()
    
    canvas12.Print("mtTailRealFakeSignalTau_tt.png")
    canvas12.Print("mtTailRealFakeSignalTau_tt.C")


##################################################


    canvas11 = ROOT.TCanvas("canvas11","",500,500)
    canvas11.SetLogy()
    hmt.SetMinimum(0.01)
#    hmt.SetMaximum(17000)
    hmt.SetMarkerColor(4)
    hmt.SetMarkerSize(1)
    hmt.SetMarkerStyle(24)
    hmt.Draw("EP")

    
    hmtObservableLeptons.SetMarkerColor(7)
    hmtObservableLeptons.SetMarkerSize(1)
    hmtObservableLeptons.SetMarkerStyle(21)
    hmtObservableLeptons.Draw("same")

    hmtNoObservableLeptons.SetMarkerColor(2)
    hmtNoObservableLeptons.SetMarkerSize(1)
    hmtNoObservableLeptons.SetMarkerStyle(20)
    hmtNoObservableLeptons.Draw("same")

    
    hmt.GetYaxis().SetTitle("Events")
    hmt.GetYaxis().SetTitleOffset(1.0)
    hmt.GetXaxis().SetTitle("m_{T}(#tau jet, MET) (GeV/c^{2})")
    
 
    
    tex3 = ROOT.TLatex(0.58,0.9,"All selected events")
    tex3.SetNDC()
    tex3.SetTextSize(18)
    tex3.Draw()    
    marker3 = ROOT.TMarker(0.55,0.91,hmt.GetMarkerStyle())
    marker3.SetNDC()
    marker3.SetMarkerColor(hmt.GetMarkerColor())
    marker3.SetMarkerSize(0.9*hmt.GetMarkerSize())
    marker3.Draw()

    tex2 = ROOT.TLatex(0.58,0.85,"Observable leptons")
    tex2.SetNDC()
    tex2.SetTextSize(18)
    tex2.Draw()    
    marker2 = ROOT.TMarker(0.55,0.86,hmtObservableLeptons.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(hmtObservableLeptons.GetMarkerColor())
    marker2.SetMarkerSize(0.9*hmtObservableLeptons.GetMarkerSize())
    marker2.Draw()
    
    tex6 = ROOT.TLatex(0.58,0.80,"No observable lepton ")
    tex6.SetNDC()
    tex6.SetTextSize(18)
    tex6.Draw()    
    marker6 = ROOT.TMarker(0.55,0.81,hmtNoObservableLeptons.GetMarkerStyle())
    marker6.SetNDC()
    marker6.SetMarkerColor(hmtNoObservableLeptons.GetMarkerColor())
    marker6.SetMarkerSize(0.9*hmtNoObservableLeptons.GetMarkerSize())
    marker6.Draw()   
    
    tex4 = ROOT.TLatex(0.25,0.96,"7 TeV                          CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(18)
    tex4.Draw()
    
#    tex5 = ROOT.TLatex(0.3,0.2,"m_{H^{#pm}} = 200 GeV/c^{2}")
    tex5 = ROOT.TLatex(0.25,0.3,"tt+jets") 
    tex5.SetNDC()
    tex5.SetTextSize(20)
    tex5.Draw()
    
    tex7 = ROOT.TLatex(0.25,0.15,"tan#beta = 30")
    tex7.SetNDC()
    tex7.SetTextSize(20)
#    tex7.Draw()
    
    canvas11.Print("mtTailObservableLeptons_tt.png")
    canvas11.Print("mtTailObservableLeptons_tt.C")


##################################################
    
    canvas4 = ROOT.TCanvas("canvas4","",500,500)
    canvas4.SetLogy()
    hmt.SetMinimum(0.01)
#    hmt.SetMaximum(17000)
    hmt.SetMarkerColor(4)
    hmt.SetMarkerSize(1)
    hmt.SetMarkerStyle(24)
    hmt.Draw("EP")

    
    hmtElectronNotInTau.SetMarkerColor(2)
    hmtElectronNotInTau.SetMarkerSize(1)
    hmtElectronNotInTau.SetMarkerStyle(20)
    hmtElectronNotInTau.Draw("same")

    hmtMuonNotInTau.SetMarkerColor(7)
    hmtMuonNotInTau.SetMarkerSize(1)
    hmtMuonNotInTau.SetMarkerStyle(21)
    hmtMuonNotInTau.Draw("same")

    hmtTauNotInTau.SetMarkerColor(6)
    hmtTauNotInTau.SetMarkerSize(1)
    hmtTauNotInTau.SetMarkerStyle(23)
    hmtTauNotInTau.Draw("same")



    hmtSum = hmtTauNotInTau.Clone("mtSum")
    hmtSum.SetName("mtSum")
    hmtSum.SetTitle("associated lepton")
    hmtSum.Add(hmtElectronNotInTau)
    hmtSum.Add(hmtMuonNotInTau)
    
    hmtSum.SetMarkerColor(1)
    hmtSum.SetMarkerSize(1)
    hmtSum.SetMarkerStyle(20)
#    hmtSum.Draw("same")

    
    hmt.GetYaxis().SetTitle("Events")
    hmt.GetYaxis().SetTitleOffset(1.0)
    hmt.GetXaxis().SetTitle("m_{T}(#tau jet, MET) (GeV/c^{2})")
    
 
    
    tex3 = ROOT.TLatex(0.58,0.9,"All selected events")
    tex3.SetNDC()
    tex3.SetTextSize(18)
    tex3.Draw()    
    marker3 = ROOT.TMarker(0.55,0.91,hmt.GetMarkerStyle())
    marker3.SetNDC()
    marker3.SetMarkerColor(hmt.GetMarkerColor())
    marker3.SetMarkerSize(0.9*hmt.GetMarkerSize())
    marker3.Draw()

    tex2 = ROOT.TLatex(0.58,0.85,"associated electron")
    tex2.SetNDC()
    tex2.SetTextSize(18)
    tex2.Draw()    
    marker2 = ROOT.TMarker(0.55,0.86,hmtElectronNotInTau.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(hmtElectronNotInTau.GetMarkerColor())
    marker2.SetMarkerSize(0.9*hmtElectronNotInTau.GetMarkerSize())
    marker2.Draw()
    
    tex6 = ROOT.TLatex(0.58,0.80,"associated muon ")
    tex6.SetNDC()
    tex6.SetTextSize(18)
    tex6.Draw()    
    marker6 = ROOT.TMarker(0.55,0.81,hmtMuonNotInTau.GetMarkerStyle())
    marker6.SetNDC()
    marker6.SetMarkerColor(hmtMuonNotInTau.GetMarkerColor())
    marker6.SetMarkerSize(0.9*hmtMuonNotInTau.GetMarkerSize())
    marker6.Draw()    

    tex1 = ROOT.TLatex(0.58,0.75,"associated hadronic #tau ")
    tex1.SetNDC()
    tex1.SetTextSize(18)
    tex1.Draw()    
    marker1 = ROOT.TMarker(0.55,0.76,hmtTauNotInTau.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(hmtTauNotInTau.GetMarkerColor())
    marker1.SetMarkerSize(0.9*hmtTauNotInTau.GetMarkerSize())
    marker1.Draw()
    
    tex8 = ROOT.TLatex(0.58,0.7,"associated leptons ")
    tex8.SetNDC()
    tex8.SetTextSize(18)
#    tex8.Draw()    
    marker8 = ROOT.TMarker(0.55,0.71,hmtSum.GetMarkerStyle())
    marker8.SetNDC()
    marker8.SetMarkerColor(hmtSum.GetMarkerColor())
    marker8.SetMarkerSize(0.9*hmtSum.GetMarkerSize())
#    marker8.Draw()
    
    tex4 = ROOT.TLatex(0.25,0.96,"7 TeV                          CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(18)
    tex4.Draw()
    
#    tex5 = ROOT.TLatex(0.3,0.2,"m_{H^{#pm}} = 200 GeV/c^{2}")
    tex5 = ROOT.TLatex(0.25,0.3,"tt+jets") 
    tex5.SetNDC()
    tex5.SetTextSize(20)
    tex5.Draw()
    
    tex7 = ROOT.TLatex(0.25,0.15,"tan#beta = 30")
    tex7.SetNDC()
    tex7.SetTextSize(20)
#    tex7.Draw()
    
    canvas4.Print("mtTailComparison_tt.png")
    canvas4.Print("mtTailComparison_tt.C")


##################################################

    canvas5 = ROOT.TCanvas("canvas5","",500,500)
    canvas5.SetLogy()
#    hmtVetohptIsolEff.SetMaximum(0.1)
#    hetabTop.SetMinimum(2000)

    hmt.SetMarkerColor(4)
    hmt.SetMarkerSize(1)
    hmt.SetMarkerStyle(24)
    hmt.Draw("EP")

    hmtMetReso02.SetMarkerColor(1)
    hmtMetReso02.SetMarkerSize(1)
    hmtMetReso02.SetMarkerStyle(22)

    hmtMetReso02.Draw("same")
    
    hmtTauVeto.SetMarkerColor(2)
    hmtTauVeto.SetMarkerSize(1)
    hmtTauVeto.SetMarkerStyle(20)
    hmtTauVeto.Draw("same")
    
     
 
    hmt.GetYaxis().SetTitle("Events")
    hmt.GetYaxis().SetTitleOffset(2.0)
    hmt.GetXaxis().SetTitle("m_{T}(#tau jet, MET) (GeV/c^{2})")
        
    
    
    tex3 = ROOT.TLatex(0.43,0.85,"All events")
    tex3.SetNDC()
    tex3.SetTextSize(20)
    tex3.Draw()    
    marker3 = ROOT.TMarker(0.4,0.87,hmt.GetMarkerStyle())
    marker3.SetNDC()
    marker3.SetMarkerColor(hmt.GetMarkerColor())
    marker3.SetMarkerSize(0.9*hmt.GetMarkerSize())
    marker3.Draw()
    

    
    tex1 = ROOT.TLatex(0.43,0.8,"MET resolution > 0.2")
    tex1.SetNDC()
    tex1.SetTextSize(20)
    tex1.Draw()    
    marker1 = ROOT.TMarker(0.4,0.82,hmtMetReso02.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(hmtMetReso02.GetMarkerColor())
    marker1.SetMarkerSize(0.9*hmtMetReso02.GetMarkerSize())
    marker1.Draw()
    
    tex2 = ROOT.TLatex(0.43,0.75,"#tau-jet veto")
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw()    
    marker2 = ROOT.TMarker(0.4,0.77,hmtTauVeto.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(hmtTauVeto.GetMarkerColor())
    marker2.SetMarkerSize(0.9*hmtTauVeto.GetMarkerSize())
    marker2.Draw()
        
 

    
    tex4 = ROOT.TLatex(0.2,0.96,"7 TeV                        CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
#    tex5 = ROOT.TLatex(0.6,0.7,"m_{H^{#pm}} = 200 GeV/c^{2}")
    tex5 = ROOT.TLatex(0.25,0.3,"tt+jets") 
    tex5.SetNDC()
    tex5.SetTextSize(20)
    tex5.Draw()
    
    tex6 = ROOT.TLatex(0.6,0.62,"|#eta^{b quark}| < 2.4")
    tex6.SetNDC()
    tex6.SetTextSize(20)
#    tex6.Draw()

    
    canvas5.Print("mtMetResoComparison_tt.png")
    canvas5.Print("mtMetResoComparison_tt.C")

 ##################################################

    canvas7 = ROOT.TCanvas("canvas7","",500,500)
    canvas7.SetLogy()
#    hmtVetohptIsolEff.SetMaximum(0.1)
#    hetabTop.SetMinimum(2000)

    hmt.SetMarkerColor(4)
    hmt.SetMarkerSize(1)
    hmt.SetMarkerStyle(24)
    hmt.Draw("EP")
    
    hmtLeptonNotInTau.SetMarkerColor(2)
    hmtLeptonNotInTau.SetMarkerSize(1)
    hmtLeptonNotInTau.SetMarkerStyle(20)
    hmtLeptonNotInTau.Draw("same")
    
    hmtMetReso02.SetMarkerColor(1)
    hmtMetReso02.SetMarkerSize(1)
    hmtMetReso02.SetMarkerStyle(23)
    hmtMetReso02.Draw("same")
    
 
    hmt.GetYaxis().SetTitle("Events")
    hmt.GetYaxis().SetTitleOffset(0.9)
    hmt.GetXaxis().SetTitle("m_{T}(#tau jet, MET) (GeV/c^{2})")
        
    
    
    tex3 = ROOT.TLatex(0.55,0.85,"All events")
    tex3.SetNDC()
    tex3.SetTextSize(20)
    tex3.Draw()    
    marker3 = ROOT.TMarker(0.52,0.86,hmt.GetMarkerStyle())
    marker3.SetNDC()
    marker3.SetMarkerColor(hmt.GetMarkerColor())
    marker3.SetMarkerSize(0.9*hmt.GetMarkerSize())
    marker3.Draw()
    
    tex8 = ROOT.TLatex(0.55,0.80,"associated leptons ")
    tex8.SetNDC()
    tex8.SetTextSize(18)
    tex8.Draw()    
    marker8 = ROOT.TMarker(0.52,0.81,hmtLeptonNotInTau.GetMarkerStyle())
    marker8.SetNDC()
    marker8.SetMarkerColor(hmtLeptonNotInTau.GetMarkerColor())
    marker8.SetMarkerSize(0.9*hmtLeptonNotInTau.GetMarkerSize())
    marker8.Draw()
    
    tex1 = ROOT.TLatex(0.55,0.75,"E_{T}^{miss} resolution > 0.2")
    tex1.SetNDC()
    tex1.SetTextSize(20)
    tex1.Draw()    
    marker1 = ROOT.TMarker(0.52,0.76,hmtMetReso02.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(hmtMetReso02.GetMarkerColor())
    marker1.SetMarkerSize(0.9*hmtMetReso02.GetMarkerSize())
    marker1.Draw()
    
    
 

    
    tex4 = ROOT.TLatex(0.2,0.96,"7 TeV                        CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
#    tex5 = ROOT.TLatex(0.6,0.7,"m_{H^{#pm}} = 200 GeV/c^{2}")
    tex5 = ROOT.TLatex(0.25,0.3,"tt+jets") 
    tex5.SetNDC()
    tex5.SetTextSize(20)
    tex5.Draw()
    
    tex6 = ROOT.TLatex(0.6,0.62,"|#eta^{b quark}| < 2.4")
    tex6.SetNDC()
    tex6.SetTextSize(20)
#    tex6.Draw()

    
    canvas7.Print("mtLeptonMetComparison_tt.png")
    canvas7.Print("mtLeptonMetComparison_tt.C")

    
 ##################################################

    canvas8 = ROOT.TCanvas("canvas8","",500,500)
    canvas8.SetLogy()
#    hmtVetohptIsolEff.SetMaximum(0.1)
#    hetabTop.SetMinimum(2000)

    hmt.SetMarkerColor(4)
    hmt.SetMarkerSize(1)
    hmt.SetMarkerStyle(24)
    hmt.Draw("EP")
    
    hmtNoLeptonNotInTau.SetMarkerColor(2)
    hmtNoLeptonNotInTau.SetMarkerSize(1)
    hmtNoLeptonNotInTau.SetMarkerStyle(20)
    hmtNoLeptonNotInTau.Draw("same")
    
    hmtNoLeptonGoodMet.SetMarkerColor(6)
    hmtNoLeptonGoodMet.SetMarkerSize(1)
    hmtNoLeptonGoodMet.SetMarkerStyle(25)
    hmtNoLeptonGoodMet.Draw("same")
    
    hmtNoLeptonGoodMetGoodTau.SetMarkerColor(1)
    hmtNoLeptonGoodMetGoodTau.SetMarkerSize(1)
    hmtNoLeptonGoodMetGoodTau.SetMarkerStyle(23)
    hmtNoLeptonGoodMetGoodTau.Draw("same")

 
     
    hmt.GetYaxis().SetTitle("Events")
    hmt.GetYaxis().SetTitleOffset(0.9)
    hmt.GetXaxis().SetTitle("m_{T}(#tau jet, MET) (GeV/c^{2})")
        
    
    
    tex3 = ROOT.TLatex(0.55,0.85,"All events")
    tex3.SetNDC()
    tex3.SetTextSize(18)
    tex3.Draw()    
    marker3 = ROOT.TMarker(0.52,0.86,hmt.GetMarkerStyle())
    marker3.SetNDC()
    marker3.SetMarkerColor(hmt.GetMarkerColor())
    marker3.SetMarkerSize(0.9*hmt.GetMarkerSize())
    marker3.Draw()
    
    tex8 = ROOT.TLatex(0.55,0.80,"No associated leptons ")
    tex8.SetNDC()
    tex8.SetTextSize(18)
    tex8.Draw()    
    marker8 = ROOT.TMarker(0.52,0.81,hmtNoLeptonNotInTau.GetMarkerStyle())
    marker8.SetNDC()
    marker8.SetMarkerColor(hmtNoLeptonNotInTau.GetMarkerColor())
    marker8.SetMarkerSize(0.9*hmtNoLeptonNotInTau.GetMarkerSize())
    marker8.Draw()
    
#    tex1 = ROOT.TLatex(0.55,0.75,"No associated leptons and")
    tex1 = ROOT.TLatex(0.55,0.75,"+ E_{T}^{miss} resolution < 0.2")
    tex1.SetNDC()
    tex1.SetTextSize(18)
    tex1.Draw()    
    marker1 = ROOT.TMarker(0.52,0.76,hmtNoLeptonGoodMet.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(hmtNoLeptonGoodMet.GetMarkerColor())
    marker1.SetMarkerSize(0.9*hmtNoLeptonGoodMet.GetMarkerSize())
    marker1.Draw()
    
    tex2 = ROOT.TLatex(0.55,0.70,"+ matched #tau jet")
    tex2.SetNDC()
    tex2.SetTextSize(18)
    tex2.Draw()    
    marker2 = ROOT.TMarker(0.52,0.71,hmtNoLeptonGoodMetGoodTau.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(hmtNoLeptonGoodMetGoodTau.GetMarkerColor())
    marker2.SetMarkerSize(0.9*hmtNoLeptonGoodMetGoodTau.GetMarkerSize())
    marker2.Draw()    
 

    
    tex4 = ROOT.TLatex(0.2,0.96,"7 TeV                        CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
#    tex5 = ROOT.TLatex(0.6,0.7,"m_{H^{#pm}} = 200 GeV/c^{2}")
    tex5 = ROOT.TLatex(0.25,0.3,"tt+jets") 
    tex5.SetNDC()
    tex5.SetTextSize(20)
    tex5.Draw()
    
    tex6 = ROOT.TLatex(0.6,0.62,"|#eta^{b quark}| < 2.4")
    tex6.SetNDC()
    tex6.SetTextSize(20)
#    tex6.Draw()

    
    canvas8.Print("mtNoLeptonsGoodMet_tt.png")
    canvas8.Print("mtNoLeptonsGoodMet_tt.C")
 ##################################################

    canvas9 = ROOT.TCanvas("canvas9","",500,500)
    canvas9.SetLogy()
#    hmtVetohptIsolEff.SetMaximum(0.1)
#    hetabTop.SetMinimum(2000)

    hmt.SetMarkerColor(4)
    hmt.SetMarkerSize(1)
    hmt.SetMarkerStyle(24)
    hmt.Draw("EP")
    
    hmtTopChiSelection.SetMarkerColor(2)
    hmtTopChiSelection.SetMarkerSize(1)
    hmtTopChiSelection.SetMarkerStyle(20)
    hmtTopChiSelection.Draw("same")

    hmtWMassSelection.SetMarkerColor(6)
    hmtWMassSelection.SetMarkerSize(1)
    hmtWMassSelection.SetMarkerStyle(25)
    hmtWMassSelection.Draw("same")

 
     
    hmt.GetYaxis().SetTitle("Events")
    hmt.GetYaxis().SetTitleOffset(0.9)
    hmt.GetXaxis().SetTitle("m_{T}(#tau jet, MET) (GeV/c^{2})")
        
    
    
    tex3 = ROOT.TLatex(0.55,0.85,"All events")
    tex3.SetNDC()
    tex3.SetTextSize(18)
    tex3.Draw()    
    marker3 = ROOT.TMarker(0.52,0.86,hmt.GetMarkerStyle())
    marker3.SetNDC()
    marker3.SetMarkerColor(hmt.GetMarkerColor())
    marker3.SetMarkerSize(0.9*hmt.GetMarkerSize())
    marker3.Draw()
    
    tex8 = ROOT.TLatex(0.55,0.80,"Top mass cut ")
    tex8.SetNDC()
    tex8.SetTextSize(18)
    tex8.Draw()    
    marker8 = ROOT.TMarker(0.52,0.81,hmtTopChiSelection.GetMarkerStyle())
    marker8.SetNDC()
    marker8.SetMarkerColor(hmtTopChiSelection.GetMarkerColor())
    marker8.SetMarkerSize(0.9*hmtTopChiSelection.GetMarkerSize())
    marker8.Draw()
    
    tex1 = ROOT.TLatex(0.55,0.75,"W mass cut")
    tex1.SetNDC()
    tex1.SetTextSize(18)
    tex1.Draw()    
    marker1 = ROOT.TMarker(0.52,0.76,hmtWMassSelection.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(hmtWMassSelection.GetMarkerColor())
    marker1.SetMarkerSize(0.9*hmtWMassSelection.GetMarkerSize())
    marker1.Draw()
    
  
 

    
    tex4 = ROOT.TLatex(0.2,0.96,"7 TeV                        CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
#    tex5 = ROOT.TLatex(0.6,0.7,"m_{H^{#pm}} = 200 GeV/c^{2}")
    tex5 = ROOT.TLatex(0.25,0.3,"tt+jets") 
    tex5.SetNDC()
    tex5.SetTextSize(20)
    tex5.Draw()
    
    tex6 = ROOT.TLatex(0.6,0.62,"|#eta^{b quark}| < 2.4")
    tex6.SetNDC()
    tex6.SetTextSize(20)
#    tex6.Draw()

    
    canvas9.Print("mtTopMassCut_tt.png")
    canvas9.Print("mtTopMassCut_tt.C")
        
##################################################    
##################################################

    canvas6 = ROOT.TCanvas("canvas6","",500,500)
#    canvas6.SetLogy()
#    hmtVetohptIsolEff.SetMaximum(0.1)
#    hetabTop.SetMinimum(2000)

    hdeltaEtMetGenMet.SetMarkerColor(4)
    hdeltaEtMetGenMet.SetMarkerSize(1)
    hdeltaEtMetGenMet.SetMarkerStyle(20)
    hdeltaEtMetGenMet.Draw("EP")

    hdeltaEtMetGenMet.GetYaxis().SetTitle("Events")
    hdeltaEtMetGenMet.GetYaxis().SetTitleOffset(1.0)
    hdeltaEtMetGenMet.GetXaxis().SetTitle("(GenMet - MET)/GenMet")
        
    
    
    tex3 = ROOT.TLatex(0.43,0.85,"All events")
    tex3.SetNDC()
    tex3.SetTextSize(20)
#    tex3.Draw()    
    marker3 = ROOT.TMarker(0.4,0.87,hdeltaEtMetGenMet.GetMarkerStyle())
    marker3.SetNDC()
    marker3.SetMarkerColor(hdeltaEtMetGenMet.GetMarkerColor())
    marker3.SetMarkerSize(0.9*hdeltaEtMetGenMet.GetMarkerSize())
#    marker3.Draw()


 

    
    tex4 = ROOT.TLatex(0.2,0.96,"7 TeV                        CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
#    tex5 = ROOT.TLatex(0.6,0.7,"m_{H^{#pm}} = 200 GeV/c^{2}")
    tex5 = ROOT.TLatex(0.75,0.85,"tt+jets") 
    tex5.SetNDC()
    tex5.SetTextSize(20)
    tex5.Draw()
    
    tex6 = ROOT.TLatex(0.6,0.62,"|#eta^{b quark}| < 2.4")
    tex6.SetNDC()
    tex6.SetTextSize(20)
#    tex6.Draw()

    
    canvas6.Print("metResolution_tt.png")
    canvas6.Print("metResolution_tt.C")

    
  
 ########################################

 
    
def printCounters(datasets):
    eventCounter = counter.EventCounter(datasets)
    eventCounter.normalizeMCByLuminosity()

    ewkDatasets = [
        "WJets", "TTJets",
        "DYJetsToLL", "SingleTop", "Diboson"
        ]


    print "============================================================"
    print "Main counter (MC normalized by collision data luminosity)"
    mainTable = eventCounter.getMainCounterTable()
    mainTable.insertColumn(2, counter.sumColumn("EWKMCsum", [mainTable.getColumn(name=name) for name in ewkDatasets]))
    # Default
#    cellFormat = counter.TableFormatText()
    # No uncertainties
    cellFormat = counter.TableFormatText(cellFormat=counter.CellFormatText(valueOnly=True))
    print mainTable.format(cellFormat)
    print eventCounter.getSubCounterTable("MCinfo for selected events").format(cellFormat)


if __name__ == "__main__":
    main()
