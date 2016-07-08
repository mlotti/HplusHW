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
    ptSelected = plots.PlotBase([datasets.getDataset("TTJets").getDatasetRootHisto(analysis+"/TauVeto/TauSelection_selected_taus_pt")])
    ptAll = plots.PlotBase([datasets.getDataset("TTJets").getDatasetRootHisto(analysis+"/TauVeto/TauSelection_all_tau_candidates_pt")])
    ptClean = plots.PlotBase([datasets.getDataset("TTJets").getDatasetRootHisto(analysis+"/TauVeto/TauSelection_cleaned_tau_candidates_pt")])
    
    ptSelected.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    ptAll.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    ptClean.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())    
    
    ptSelected._setLegendStyles()
    ptSelected._setLegendLabels()
    ptSelected.histoMgr.setHistoDrawStyleAll("P")
    ptSelected.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))    
    hptSelected = ptSelected.histoMgr.getHisto("TTJets").getRootHisto().Clone(analysis+"/TauVeto/TauSelection_selected_taus_pt")
    
    ptAll._setLegendStyles()
    ptAll._setLegendLabels()
    ptAll.histoMgr.setHistoDrawStyleAll("P")
    ptAll.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))    
    hptAll = ptAll.histoMgr.getHisto("TTJets").getRootHisto().Clone(analysis+"/TauVeto/TauSelection_all_tau_candidates_pt")

    ptClean._setLegendStyles()
    ptClean._setLegendLabels()
    ptClean.histoMgr.setHistoDrawStyleAll("P")
    ptClean.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))    
    hptClean = ptClean.histoMgr.getHisto("TTJets").getRootHisto().Clone(analysis+"/TauVeto/TauSelection_cleaned_tau_candidates_pt")
    
    
    hptEff = hptSelected.Clone("hptSelected")
    hptEff.SetName("hptEff")
    hptEff.SetTitle("TauVetoEff")
    hptEff.Divide(hptAll)
    
    hptIsolEff = hptSelected.Clone("hptSelected")
    hptIsolEff.SetName("hptIsolEff")
    hptIsolEff.SetTitle("TauVetoIsolEff")
    hptIsolEff.Divide(hptClean)

    
    canvas3 = ROOT.TCanvas("canvas3","",500,500)
    canvas3.SetLogy()
    hptIsolEff.SetMaximum(0.08)
    hptIsolEff.SetMinimum(0.001)
    hptIsolEff.SetMarkerColor(4)
    hptIsolEff.SetMarkerSize(1)
    hptIsolEff.SetMarkerStyle(24)
    hptIsolEff.Draw("EP")
    
    hptEff.SetMarkerColor(2)
    hptEff.SetMarkerSize(1)
    hptEff.SetMarkerStyle(25)
    hptEff.Draw("same")
    
    hptIsolEff.GetYaxis().SetTitle("#tau selection efficiency")
    hptIsolEff.GetYaxis().SetTitleOffset(1.5)
    hptIsolEff.GetXaxis().SetTitle("p_{T}^{#tau jet} (GeV)")
    
    tex1 = ROOT.TLatex(0.35,0.3,"Total selection")
    tex1.SetNDC()
    tex1.SetTextSize(20)
    tex1.Draw()    
    marker1 = ROOT.TMarker(0.3,0.31,hptEff.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(hptEff.GetMarkerColor())
    marker1.SetMarkerSize(0.9*hptEff.GetMarkerSize())
    marker1.Draw()   
    tex2 = ROOT.TLatex(0.35,0.25,"Isolation") 
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw()    
    marker2 = ROOT.TMarker(0.3,0.251,hptIsolEff.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(hptIsolEff.GetMarkerColor())
    marker2.SetMarkerSize(0.9*hptIsolEff.GetMarkerSize())
    marker2.Draw()

    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV                        CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
#    tex5 = ROOT.TLatex(0.55,0.9,"Signal, m_{H^{#pm}} = 120 GeV/c^{2}")
    tex5 = ROOT.TLatex(0.65,0.85,"tt+jets") 
    tex5.SetNDC()
    tex5.SetTextSize(20)
    tex5.Draw()
    
    canvas3.Print("TauVetoEff_pt_tt.png")
    canvas3.Print("TauVetoEff_pt_tt.C")

############## signal pt
    ptSelected2 = plots.PlotBase([datasets.getDataset("TTToHplusBWB_M120").getDatasetRootHisto(analysis+"/TauVeto/TauSelection_selected_taus_pt")])
    ptAll2 = plots.PlotBase([datasets.getDataset("TTToHplusBWB_M120").getDatasetRootHisto(analysis+"/TauVeto/TauSelection_all_tau_candidates_pt")])
    ptClean2 = plots.PlotBase([datasets.getDataset("TTToHplusBWB_M120").getDatasetRootHisto(analysis+"/TauVeto/TauSelection_cleaned_tau_candidates_pt")])   
    ptSelected2.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    ptAll2.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    ptClean2.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())    
    
    ptSelected2._setLegendStyles()
    ptSelected2._setLegendLabels()
    ptSelected2.histoMgr.setHistoDrawStyleAll("P")
    ptSelected2.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))    
    hptSelected2 = ptSelected2.histoMgr.getHisto("TTToHplusBWB_M120").getRootHisto().Clone(analysis+"/TauVeto/TauSelection_selected_taus_pt")
    
    ptAll2._setLegendStyles()
    ptAll2._setLegendLabels()
    ptAll2.histoMgr.setHistoDrawStyleAll("P")
    ptAll2.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))    
    hptAll2 = ptAll2.histoMgr.getHisto("TTToHplusBWB_M120").getRootHisto().Clone(analysis+"/TauVeto/TauSelection_all_tau_candidates_pt")

    ptClean2._setLegendStyles()
    ptClean2._setLegendLabels()
    ptClean2.histoMgr.setHistoDrawStyleAll("P")
    ptClean2.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))    
    hptClean2 = ptClean2.histoMgr.getHisto("TTToHplusBWB_M120").getRootHisto().Clone(analysis+"/TauVeto/TauSelection_cleaned_tau_candidates_pt")
    
    
    hptEff2 = hptSelected.Clone("hptSelected2")
    hptEff2.SetName("hptEff2")
    hptEff2.SetTitle("TauVetoEff2")
    hptEff2.Divide(hptAll2)
    
    hptIsolEff2 = hptSelected.Clone("hptSelected2")
    hptIsolEff2.SetName("hptIsolEff2")
    hptIsolEff2.SetTitle("TauVetoIsolEff2")
    hptIsolEff2.Divide(hptClean2)
    
    canvas5 = ROOT.TCanvas("canvas5","",500,500)
    canvas5.SetLogy()
#    hptIsolEff2.SetMaximum(0.08)
    hptIsolEff2.SetMinimum(0.0001)
    hptIsolEff2.SetMarkerColor(4)
    hptIsolEff2.SetMarkerSize(1)
    hptIsolEff2.SetMarkerStyle(24)
    hptIsolEff2.Draw("EP")
    
    hptEff2.SetMarkerColor(2)
    hptEff2.SetMarkerSize(1)
    hptEff2.SetMarkerStyle(25)
    hptEff2.Draw("same")
    
    hptIsolEff2.GetYaxis().SetTitle("#tau selection efficiency")
    hptIsolEff2.GetYaxis().SetTitleOffset(1.5)
    hptIsolEff2.GetXaxis().SetTitle("p_{T}^{#tau jet} (GeV)")
    
    tex1 = ROOT.TLatex(0.35,0.3,"Total selection")
    tex1.SetNDC()
    tex1.SetTextSize(20)
    tex1.Draw()    
    marker1 = ROOT.TMarker(0.3,0.31,hptEff.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(hptEff.GetMarkerColor())
    marker1.SetMarkerSize(0.9*hptEff.GetMarkerSize())
    marker1.Draw()
    
    tex2 = ROOT.TLatex(0.35,0.25,"Isolation") 
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw()    
    marker2 = ROOT.TMarker(0.3,0.251,hptIsolEff.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(hptIsolEff.GetMarkerColor())
    marker2.SetMarkerSize(0.9*hptIsolEff.GetMarkerSize())
    marker2.Draw()

    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV                        CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    tex5 = ROOT.TLatex(0.45,0.85,"Signal, m_{H^{#pm}} = 120 GeV/c^{2}")
#    tex5 = ROOT.TLatex(0.55,0.9,"tt+jets") 
    tex5.SetNDC()
    tex5.SetTextSize(20)
    tex5.Draw()
    
    canvas5.Print("TauVetoEff_pt_h120.png")
    canvas5.Print("TauVetoEff_pt_h120.C")


###############################
    etaSelected = plots.PlotBase([datasets.getDataset("TTJets").getDatasetRootHisto(analysis+"/TauVeto/TauSelection_selected_taus_eta")])
    etaAll = plots.PlotBase([datasets.getDataset("TTJets").getDatasetRootHisto(analysis+"/TauVeto/TauSelection_all_tau_candidates_eta")])
    etaClean = plots.PlotBase([datasets.getDataset("TTJets").getDatasetRootHisto(analysis+"/TauVeto/TauSelection_cleaned_tau_candidates_eta")])
    
    etaSelected.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    etaAll.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    etaClean.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())    
    
    etaSelected._setLegendStyles()
    etaSelected._setLegendLabels()
    etaSelected.histoMgr.setHistoDrawStyleAll("P")
    etaSelected.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))    
    hetaSelected = etaSelected.histoMgr.getHisto("TTJets").getRootHisto().Clone(analysis+"/TauVeto/TauSelection_selected_taus_eta")
    
    etaAll._setLegendStyles()
    etaAll._setLegendLabels()
    etaAll.histoMgr.setHistoDrawStyleAll("P")
    etaAll.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))    
    hetaAll = etaAll.histoMgr.getHisto("TTJets").getRootHisto().Clone(analysis+"/TauVeto/TauSelection_all_tau_candidates_eta")

    etaClean._setLegendStyles()
    etaClean._setLegendLabels()
    etaClean.histoMgr.setHistoDrawStyleAll("P")
    etaClean.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))    
    hetaClean = etaClean.histoMgr.getHisto("TTJets").getRootHisto().Clone(analysis+"/TauVeto/TauSelection_cleaned_tau_candidates_eta")
    
    
    hetaEff = hetaSelected.Clone("hetaSelected")
    hetaEff.SetName("hetaEff")
    hetaEff.SetTitle("TauVetoEff")
    hetaEff.Divide(hetaAll)

    hetaIsolEff = hetaSelected.Clone("hetaSelected")
    hetaIsolEff.SetName("hetaIsolEff")
    hetaIsolEff.SetTitle("TauVetoIsolEff")
    hetaIsolEff.Divide(hetaClean)

    canvas2 = ROOT.TCanvas("canvas2","",500,500)
#    canvas3.SetLogy()
    hetaEff.SetMaximum(0.12)
    hetaEff.SetMarkerColor(2)
    hetaEff.SetMarkerSize(1)
    hetaEff.SetMarkerStyle(20)
    hetaEff.Draw("EP")
    
    hetaIsolEff.SetMarkerColor(4)
    hetaIsolEff.SetMarkerSize(1)
    hetaIsolEff.SetMarkerStyle(26)
    hetaIsolEff.Draw("same")
    
    hetaEff.GetYaxis().SetTitle("#tau selection efficiency")
    hetaEff.GetYaxis().SetTitleOffset(1.5)
    hetaEff.GetXaxis().SetTitle("#eta_{#tau jet}")
    
#    tex5 = ROOT.TLatex(0.55,0.9,"Signal, m_{H^{#pm}} = 120 GeV/c^{2}")
    tex5 = ROOT.TLatex(0.55,0.9,"tt+jets")
    tex5.SetNDC()
    tex5.SetTextSize(18)
    tex5.Draw()
    
    tex1 = ROOT.TLatex(0.55,0.8,"Total selection")
    tex1.SetNDC()
    tex1.SetTextSize(20)
    tex1.Draw()
    
    marker1 = ROOT.TMarker(0.5,0.715,hetaEff.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(hetaEff.GetMarkerColor())
    marker1.SetMarkerSize(0.9*hetaEff.GetMarkerSize())
    marker1.Draw()   
    tex2 = ROOT.TLatex(0.55,0.7,"Isolation") 
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw()    
    marker2 = ROOT.TMarker(0.5,0.715,hetaIsolEff.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(hetaIsolEff.GetMarkerColor())
    marker2.SetMarkerSize(0.9*hetaIsolEff.GetMarkerSize())
    marker2.Draw()

    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV                        CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    canvas2.Print("TauVetoEff_eta.png")
    canvas2.Print("TauVetoEff_eta.C")  
   

 
 ########################################

 
    
def printCounters(datasets):
    eventCounter = counter.EventCounter(datasets)
    eventCounter.normalizeMCByLuminosity()
    print "============================================================"
    print "Main counter (MC normalized by collision data luminosity)"
    print eventCounter.getMainCounterTable().format()

if __name__ == "__main__":
    main()
