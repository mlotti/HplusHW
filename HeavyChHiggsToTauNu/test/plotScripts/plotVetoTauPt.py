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
counters = analysis+"Counters"

treeDraw = dataset.TreeDraw(analysis+"/tree", weight="weightPileup")

def main():
    datasets = dataset.getDatasetsFromMulticrabCfg(counters=counters)
    datasets.updateNAllEventsToPUWeighted()
    datasets.loadLuminosities()

    plots.mergeRenameReorderForDataMC(datasets)
    print "Int.Lumi",datasets.getDataset("Data").getLuminosity()
#    datasets.remove(filter(lambda name: "TTToHplus" in name and not "M120" in name, datasets.getAllDatasetNames()))
#    datasets.remove(filter(lambda name: "HplusTB" in name, datasets.getAllDatasetNames()))
    
    style = tdrstyle.TDRStyle()

    plot(datasets)
       
    printCounters(datasets)

def plot(datasets):
    ptGenuineTau = plots.PlotBase([datasets.getDataset("TTToHplusBWB_M120").getDatasetRootHisto(analysis+"/VetoTauSelection/SelectedGenuineTauByPt")])
    ptFakeTau = plots.PlotBase([datasets.getDataset("TTToHplusBWB_M120").getDatasetRootHisto(analysis+"/VetoTauSelection/SelectedFakeTauByPt")])    
    
    ptGenuineTau.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    ptFakeTau.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
  
    
    ptGenuineTau._setLegendStyles()
    ptGenuineTau._setLegendLabels()
    ptGenuineTau.histoMgr.setHistoDrawStyleAll("P")
    ptGenuineTau.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))    
    hptGenuineTau = ptGenuineTau.histoMgr.getHisto("TTToHplusBWB_M120").getRootHisto().Clone(analysis+"/VetoTauSelection/SelectedGenuineTauByPt")
    
    ptFakeTau._setLegendStyles()
    ptFakeTau._setLegendLabels()
    ptFakeTau.histoMgr.setHistoDrawStyleAll("P")
    ptFakeTau.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))    
    hptFakeTau = ptFakeTau.histoMgr.getHisto("TTToHplusBWB_M120").getRootHisto().Clone(analysis+"/VetoTauSelection/SelectedFakeTauByPt")  
    
    
    canvas3 = ROOT.TCanvas("canvas3","",500,500)
#    canvas3.SetLogy()
#    hptIsolEff.SetMaximum(0.1)
#    hptIsolEff.SetMinimum(0.002)
    hptGenuineTau.SetMarkerColor(4)
    hptGenuineTau.SetMarkerSize(1)
    hptGenuineTau.SetMarkerStyle(24)
    hptGenuineTau.Draw("EP")
    
    hptFakeTau.SetMarkerColor(2)
    hptFakeTau.SetMarkerSize(1)
    hptFakeTau.SetMarkerStyle(25)
    hptFakeTau.Draw("same")
    
    hptGenuineTau.GetYaxis().SetTitle("#tau jets / 25 GeV/c")
    hptGenuineTau.GetYaxis().SetTitleOffset(1.5)
    hptGenuineTau.GetXaxis().SetTitle("p_{T}^{#tau jet} (GeV/c)")
    
    tex1 = ROOT.TLatex(0.55,0.6,"Genuine #tau jets")
    tex1.SetNDC()
    tex1.SetTextSize(20)
    tex1.Draw()    
    marker1 = ROOT.TMarker(0.5,0.61,hptGenuineTau.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(hptGenuineTau.GetMarkerColor())
    marker1.SetMarkerSize(0.9*hptGenuineTau.GetMarkerSize())
    marker1.Draw()
    
    tex2 = ROOT.TLatex(0.55,0.55,"Fake #tau jets") 
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw()    
    marker2 = ROOT.TMarker(0.5,0.551,hptFakeTau.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(hptFakeTau.GetMarkerColor())
    marker2.SetMarkerSize(0.9*hptFakeTau.GetMarkerSize())
    marker2.Draw()

    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV                        CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    tex5 = ROOT.TLatex(0.55,0.8,"Signal, m_{H^{#pm}} = 120 GeV/c^{2}")
#    tex5 = ROOT.TLatex(0.55,0.9,"tt+jets") 
    tex5.SetNDC()
    tex5.SetTextSize(18)
    tex5.Draw()
    
    canvas3.Print("PtVetoTaus_h120.png")
    canvas3.Print("PtVetoTaus_h120.C")


   
    ptGenuineTautt = plots.PlotBase([datasets.getDataset("TTJets").getDatasetRootHisto(analysis+"/VetoTauSelection/SelectedGenuineTauByPt")])
    ptFakeTautt = plots.PlotBase([datasets.getDataset("TTJets").getDatasetRootHisto(analysis+"/VetoTauSelection/SelectedFakeTauByPt")])    
    
    ptGenuineTautt.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    ptFakeTautt.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
  
    
    ptGenuineTautt._setLegendStyles()
    ptGenuineTautt._setLegendLabels()
    ptGenuineTautt.histoMgr.setHistoDrawStyleAll("P")
    ptGenuineTautt.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))    
    hptGenuineTautt = ptGenuineTautt.histoMgr.getHisto("TTJets").getRootHisto().Clone(analysis+"/VetoTauSelection/SelectedGenuineTauByPt")
    
    ptFakeTautt._setLegendStyles()
    ptFakeTautt._setLegendLabels()
    ptFakeTautt.histoMgr.setHistoDrawStyleAll("P")
    ptFakeTautt.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))    
    hptFakeTautt = ptFakeTautt.histoMgr.getHisto("TTJets").getRootHisto().Clone(analysis+"/VetoTauSelection/SelectedFakeTauByPt")  
    
    
    canvas4 = ROOT.TCanvas("canvas4","",500,500)
#    canvas3.SetLogy()
    hptGenuineTautt.SetMaximum(10.0)
#    hptIsolEff.SetMinimum(0.002)
    hptGenuineTautt.SetMarkerColor(4)
    hptGenuineTautt.SetMarkerSize(1)
    hptGenuineTautt.SetMarkerStyle(24)
    hptGenuineTautt.Draw("EP")
    
    hptFakeTautt.SetMarkerColor(2)
    hptFakeTautt.SetMarkerSize(1)
    hptFakeTautt.SetMarkerStyle(25)
    hptFakeTautt.Draw("same")
    
    hptGenuineTautt.GetYaxis().SetTitle("#tau jets / 25 GeV/c")
    hptGenuineTautt.GetYaxis().SetTitleOffset(1.5)
    hptGenuineTautt.GetXaxis().SetTitle("p_{T}^{#tau jet} (GeV/c)")
    
    tex1 = ROOT.TLatex(0.55,0.7,"Genuine #tau jets")
    tex1.SetNDC()
    tex1.SetTextSize(20)
    tex1.Draw()    
    marker1 = ROOT.TMarker(0.5,0.71,hptGenuineTautt.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(hptGenuineTautt.GetMarkerColor())
    marker1.SetMarkerSize(0.9*hptGenuineTautt.GetMarkerSize())
    marker1.Draw()
    
    tex2 = ROOT.TLatex(0.55,0.6,"Fake #tau jets") 
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw()    
    marker2 = ROOT.TMarker(0.5,0.61,hptFakeTautt.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(hptFakeTautt.GetMarkerColor())
    marker2.SetMarkerSize(0.9*hptFakeTautt.GetMarkerSize())
    marker2.Draw()

    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV                        CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
#    tex5 = ROOT.TLatex(0.55,0.8,"Signal, m_{H^{#pm}} = 120 GeV/c^{2}")
    tex5 = ROOT.TLatex(0.55,0.8,"tt+jets") 
    tex5.SetNDC()
    tex5.SetTextSize(18)
    tex5.Draw()
    
    canvas4.Print("PtVetoTaus_tt.png")
    canvas4.Print("PtVetoTaus_tt.C")




    etaGenuineTautt = plots.PlotBase([datasets.getDataset("TTJets").getDatasetRootHisto(analysis+"/VetoTauSelection/SelectedGenuineTauByEta")])
    etaFakeTautt = plots.PlotBase([datasets.getDataset("TTJets").getDatasetRootHisto(analysis+"/VetoTauSelection/SelectedFakeTauByEta")])    
    
    etaGenuineTautt.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    etaFakeTautt.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
  
    
    etaGenuineTautt._setLegendStyles()
    etaGenuineTautt._setLegendLabels()
    etaGenuineTautt.histoMgr.setHistoDrawStyleAll("P")
    etaGenuineTautt.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))    
    hetaGenuineTautt = etaGenuineTautt.histoMgr.getHisto("TTJets").getRootHisto().Clone(analysis+"/VetoTauSelection/SelectedGenuineTauByEta")
    
    etaFakeTautt._setLegendStyles()
    etaFakeTautt._setLegendLabels()
    etaFakeTautt.histoMgr.setHistoDrawStyleAll("P")
    etaFakeTautt.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))    
    hetaFakeTautt = etaFakeTautt.histoMgr.getHisto("TTJets").getRootHisto().Clone(analysis+"/VetoTauSelection/SelectedFakeTauByEta")  
    
    
    canvas5 = ROOT.TCanvas("canvas5","",500,500)
#    canvas3.SetLogy()
    hetaGenuineTautt.SetMaximum(5.0)
#    hetaGenuineTautt.SetMinimum(0.002)
    hetaGenuineTautt.SetMarkerColor(4)
    hetaGenuineTautt.SetMarkerSize(1)
    hetaGenuineTautt.SetMarkerStyle(24)
    hetaGenuineTautt.Draw("EP")
    
    hetaFakeTautt.SetMarkerColor(2)
    hetaFakeTautt.SetMarkerSize(1)
    hetaFakeTautt.SetMarkerStyle(25)
    hetaFakeTautt.Draw("same")
    
    hetaGenuineTautt.GetYaxis().SetTitle("#tau jets")
    hetaGenuineTautt.GetYaxis().SetTitleOffset(1.5)
    hetaGenuineTautt.GetXaxis().SetTitle("#eta^{#tau jet}")
    
    tex1 = ROOT.TLatex(0.55,0.85,"Genuine #tau jets")
    tex1.SetNDC()
    tex1.SetTextSize(20)
    tex1.Draw()    
    marker1 = ROOT.TMarker(0.5,0.86,hetaGenuineTautt.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(hetaGenuineTautt.GetMarkerColor())
    marker1.SetMarkerSize(0.9*hetaGenuineTautt.GetMarkerSize())
    marker1.Draw()
    
    tex2 = ROOT.TLatex(0.55,0.8,"Fake #tau jets") 
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw()    
    marker2 = ROOT.TMarker(0.5,0.81,hetaFakeTautt.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(hetaFakeTautt.GetMarkerColor())
    marker2.SetMarkerSize(0.9*hetaFakeTautt.GetMarkerSize())
    marker2.Draw()

    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV                        CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
#    tex5 = ROOT.TLatex(0.55,0.8,"Signal, m_{H^{#pm}} = 120 GeV/c^{2}")
    tex5 = ROOT.TLatex(0.2,0.85,"tt+jets") 
    tex5.SetNDC()
    tex5.SetTextSize(18)
    tex5.Draw()
    
    canvas5.Print("EtaVetoTaus_tt.png")
    canvas5.Print("EtaVetoTaus_tt.C")
 
 ########################################

 
    
def printCounters(datasets):
    eventCounter = counter.EventCounter(datasets)
    eventCounter.normalizeMCByLuminosity()
    print "============================================================"
    print "Main counter (MC normalized by collision data luminosity)"
    print eventCounter.getMainCounterTable().format()

if __name__ == "__main__":
    main()
