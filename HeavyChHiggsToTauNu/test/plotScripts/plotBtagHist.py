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
counters = analysis+"Counters/weighted"

treeDraw = dataset.TreeDraw(analysis+"/tree", weight="weightPileup")

def main():
    datasets = dataset.getDatasetsFromMulticrabCfg(counters=counters)
    datasets.loadLuminosities()

    plots.mergeRenameReorderForDataMC(datasets)
    print "Int.Lumi",datasets.getDataset("Data").getLuminosity()
#    datasets.remove(filter(lambda name: "TTToHplus" in name and not "M120" in name, datasets.getAllDatasetNames()))
#    datasets.remove(filter(lambda name: "HplusTB" in name, datasets.getAllDatasetNames()))
    
    style = tdrstyle.TDRStyle()

    plot(datasets)
       
    printCounters(datasets)

def plot(datasets):
    ptBtagged = plots.PlotBase([datasets.getDataset("TTJets").getDatasetRootHisto(analysis+"/Btagging/realbjet17_pt")])
    ptB = plots.PlotBase([datasets.getDataset("TTJets").getDatasetRootHisto(analysis+"/Btagging/realbjetNotag_pt")])
    etaBtagged = plots.PlotBase([datasets.getDataset("TTJets").getDatasetRootHisto(analysis+"/Btagging/realbjet17_eta")])
    etaB = plots.PlotBase([datasets.getDataset("TTJets").getDatasetRootHisto(analysis+"/Btagging/realbjetNotag_eta")])
    ptQtagged = plots.PlotBase([datasets.getDataset("QCD").getDatasetRootHisto(analysis+"/Btagging/realqjet17_pt")])
    ptQ = plots.PlotBase([datasets.getDataset("QCD").getDatasetRootHisto(analysis+"/Btagging/realqjetNotag_pt")])
    etaQtagged = plots.PlotBase([datasets.getDataset("QCD").getDatasetRootHisto(analysis+"/Btagging/realqjet17_eta")])
    etaQ = plots.PlotBase([datasets.getDataset("QCD").getDatasetRootHisto(analysis+"/Btagging/realqjetNotag_eta")])
    
    ptBtagged.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    ptB.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    etaBtagged.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    etaB.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    ptQtagged.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    ptQ.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    etaQtagged.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    etaQ.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())  

    ptBtagged33 = plots.PlotBase([datasets.getDataset("TTJets").getDatasetRootHisto(analysis+"/Btagging/realbjet33_pt")])
    etaBtagged33 = plots.PlotBase([datasets.getDataset("TTJets").getDatasetRootHisto(analysis+"/Btagging/realbjet33_eta")])
    ptQtagged33 = plots.PlotBase([datasets.getDataset("QCD").getDatasetRootHisto(analysis+"/Btagging/realqjet33_pt")])
    etaQtagged33 = plots.PlotBase([datasets.getDataset("QCD").getDatasetRootHisto(analysis+"/Btagging/realqjet33_eta")])

    
    ptBtagged33.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    etaBtagged33.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    ptQtagged33.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    etaQtagged33.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())



    
    ptBtagged._setLegendStyles()
    ptBtagged._setLegendLabels()
    ptBtagged.histoMgr.setHistoDrawStyleAll("P")
    ptBtagged.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))    
    hptBtagged = ptBtagged.histoMgr.getHisto("TTJets").getRootHisto().Clone(analysis+"/Btagging/realbjet_pt")
    
    ptB._setLegendStyles()
    ptB._setLegendLabels()
    ptB.histoMgr.setHistoDrawStyleAll("P")
    ptB.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))    
    hptB = ptB.histoMgr.getHisto("TTJets").getRootHisto().Clone(analysis+"/Btagging/realbjetNotag_pt")

    ptQtagged._setLegendStyles()
    ptQtagged._setLegendLabels()
    ptQtagged.histoMgr.setHistoDrawStyleAll("P")
    ptQtagged.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))    
    hptQtagged = ptQtagged.histoMgr.getHisto("QCD").getRootHisto().Clone(analysis+"/Btagging/realqjet_pt")
    
    ptQ._setLegendStyles()
    ptQ._setLegendLabels()
    ptQ.histoMgr.setHistoDrawStyleAll("P")
    ptQ.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))    
    hptQ = ptQ.histoMgr.getHisto("QCD").getRootHisto().Clone(analysis+"/Btagging/realqjetNotag_pt")
        
    hptBEff = hptBtagged.Clone("hptBEff")
    hptBEff.SetName("hptBEff")
    hptBEff.SetTitle("Efficiency B jet")
    hptBEff.Divide(hptB)

    hptQEff = hptQtagged.Clone("hptQEff")
    hptQEff.SetName("hptQEff")
    hptQEff.SetTitle("Efficiency Q jet")
    hptQEff.Divide(hptQ)    

    canvas3 = ROOT.TCanvas("canvas3","",500,500)
    canvas3.SetLogy()
    hptBEff.SetMinimum(0.01)
    hptBEff.SetMarkerColor(2)
    hptBEff.SetMarkerSize(1)
    hptBEff.SetMarkerStyle(22)
    hptBEff.Draw("EP")


    hptQEff.SetMarkerColor(4)
    hptQEff.SetMarkerSize(1)
    hptQEff.SetMarkerStyle(24)
    hptQEff.Draw("same")
    
    hptBEff.GetYaxis().SetTitle("B-tagging efficiency")
    hptBEff.GetYaxis().SetTitleOffset(1.5)
    hptBEff.GetXaxis().SetTitle("E_{T}^{jet} (GeV)")
    

    tex1 = ROOT.TLatex(0.45,0.35,"b jets in tt events")
    tex1.SetNDC()
    tex1.SetTextSize(20)
    tex1.Draw()    
    marker1 = ROOT.TMarker(0.42,0.36,hptBEff.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(hptBEff.GetMarkerColor())
    marker1.SetMarkerSize(0.9*hptBEff.GetMarkerSize())
    marker1.Draw()
    
    tex2 = ROOT.TLatex(0.45,0.25,"q or g jets in QCD events") 
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw()    
    marker2 = ROOT.TMarker(0.42,0.26,hptQEff.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(hptQEff.GetMarkerColor())
    marker2.SetMarkerSize(0.9*hptQEff.GetMarkerSize())
    marker2.Draw()
    
    tex5 = ROOT.TLatex(0.2,0.95,"7 TeV                        CMS Preliminary ")
    tex5.SetNDC()
    tex5.SetTextSize(20)
    tex5.Draw()
    
    tex6 = ROOT.TLatex(0.2,0.85,"Discriminator > 1.7")
    tex6.SetNDC()
    tex6.SetTextSize(18)
    tex6.Draw()        

    canvas3.Print("ptBEff_disc17.png")
    canvas3.Print("ptBEff_disc17.C")

    
    ptBtagged33._setLegendStyles()
    ptBtagged33._setLegendLabels()
    ptBtagged33.histoMgr.setHistoDrawStyleAll("P")
    ptBtagged33.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))    
    hptBtagged33 = ptBtagged33.histoMgr.getHisto("TTJets").getRootHisto().Clone(analysis+"/Btagging/realbjet33_pt")
    
    ptQtagged33._setLegendStyles()
    ptQtagged33._setLegendLabels()
    ptQtagged33.histoMgr.setHistoDrawStyleAll("P")
    ptQtagged33.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))    
    hptQtagged33 = ptQtagged33.histoMgr.getHisto("QCD").getRootHisto().Clone(analysis+"/Btagging/realqjet33_pt")
    
        
    hptBEff33 = hptBtagged33.Clone("hptBEff33")
    hptBEff33.SetName("hptBEff33")
    hptBEff33.SetTitle("Efficiency33 B jet")
    hptBEff33.Divide(hptB)

    hptQEff33 = hptQtagged33.Clone("hptQEff33")
    hptQEff33.SetName("hptQEff33")
    hptQEff33.SetTitle("Efficiency33 Q jet")
    hptQEff33.Divide(hptQ)    

    canvas4 = ROOT.TCanvas("canvas4","",500,500)
    canvas4.SetLogy()
    hptBEff33.SetMinimum(0.01)
    hptBEff33.SetMarkerColor(2)
    hptBEff33.SetMarkerSize(1)
    hptBEff33.SetMarkerStyle(22)
    hptBEff33.Draw("EP")


    hptQEff33.SetMarkerColor(4)
    hptQEff33.SetMarkerSize(1)
    hptQEff33.SetMarkerStyle(24)
    hptQEff33.Draw("same")
    
    hptBEff33.GetYaxis().SetTitle("B-tagging efficiency")
    hptBEff33.GetYaxis().SetTitleOffset(1.5)
    hptBEff33.GetXaxis().SetTitle("E_{T}^{jet} (GeV)")
    

    tex1 = ROOT.TLatex(0.45,0.35,"b jets in tt events")
    tex1.SetNDC()
    tex1.SetTextSize(20)
    tex1.Draw()    
    marker1 = ROOT.TMarker(0.42,0.36,hptBEff.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(hptBEff.GetMarkerColor())
    marker1.SetMarkerSize(0.9*hptBEff.GetMarkerSize())
    marker1.Draw()
    
    tex2 = ROOT.TLatex(0.45,0.25,"q or g jets in QCD events") 
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw()    
    marker2 = ROOT.TMarker(0.42,0.26,hptQEff.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(hptQEff.GetMarkerColor())
    marker2.SetMarkerSize(0.9*hptQEff.GetMarkerSize())
    marker2.Draw()
    
    tex5 = ROOT.TLatex(0.2,0.95,"7 TeV                        CMS Preliminary ")
    tex5.SetNDC()
    tex5.SetTextSize(20)
    tex5.Draw()

    
    tex6 = ROOT.TLatex(0.2,0.85,"Discriminator > 3.3")
    tex6.SetNDC()
    tex6.SetTextSize(18)
    tex6.Draw()        

    canvas4.Print("ptBEff_disc33.png")
    canvas4.Print("ptBEff_disc33.C")

    #################################################

   
    
    etaBtagged._setLegendStyles()
    etaBtagged._setLegendLabels()
    etaBtagged.histoMgr.setHistoDrawStyleAll("P")
    etaBtagged.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))    
    hetaBtagged = etaBtagged.histoMgr.getHisto("TTJets").getRootHisto().Clone(analysis+"/Btagging/realbjet_eta")
    
    etaB._setLegendStyles()
    etaB._setLegendLabels()
    etaB.histoMgr.setHistoDrawStyleAll("P")
    etaB.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))    
    hetaB = etaB.histoMgr.getHisto("TTJets").getRootHisto().Clone(analysis+"/Btagging/realbjetNotag_eta")

    etaQtagged._setLegendStyles()
    etaQtagged._setLegendLabels()
    etaQtagged.histoMgr.setHistoDrawStyleAll("P")
    etaQtagged.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))    
    hetaQtagged = etaQtagged.histoMgr.getHisto("QCD").getRootHisto().Clone(analysis+"/Btagging/realqjet_eta")
    
    etaQ._setLegendStyles()
    etaQ._setLegendLabels()
    etaQ.histoMgr.setHistoDrawStyleAll("P")
    etaQ.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))    
    hetaQ = etaQ.histoMgr.getHisto("QCD").getRootHisto().Clone(analysis+"/Btagging/realqjetNotag_eta")
        
    hetaBEff = hetaBtagged.Clone("hetaBEff")
    hetaBEff.SetName("hetaBEff")
    hetaBEff.SetTitle("Efficiency B jet")
    hetaBEff.Divide(hetaB)

    hetaQEff = hetaQtagged.Clone("hptQEff")
    hetaQEff.SetName("hetaQEff")
    hetaQEff.SetTitle("Efficiency Q jet")
    hetaQEff.Divide(hetaQ)    

    canvas5 = ROOT.TCanvas("canvas5","",500,500)
    canvas5.SetLogy()
    hetaBEff.SetMinimum(0.01)
    hetaBEff.SetMarkerColor(2)
    hetaBEff.SetMarkerSize(1)
    hetaBEff.SetMarkerStyle(22)
    hetaBEff.Draw("EP")


    hetaQEff.SetMarkerColor(4)
    hetaQEff.SetMarkerSize(1)
    hetaQEff.SetMarkerStyle(24)
    hetaQEff.Draw("same")
    
    hetaBEff.GetYaxis().SetTitle("B-tagging efficiency")
    hetaBEff.GetYaxis().SetTitleOffset(1.5)
    hetaBEff.GetXaxis().SetTitle("#eta^{jet}")
    

    tex1 = ROOT.TLatex(0.45,0.35,"b jets in tt events")
    tex1.SetNDC()
    tex1.SetTextSize(20)
    tex1.Draw()    
    marker1 = ROOT.TMarker(0.42,0.36,hptBEff.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(hptBEff.GetMarkerColor())
    marker1.SetMarkerSize(0.9*hptBEff.GetMarkerSize())
    marker1.Draw()
    
    tex2 = ROOT.TLatex(0.45,0.25,"q or g jets in QCD events") 
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw()    
    marker2 = ROOT.TMarker(0.42,0.26,hptQEff.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(hptQEff.GetMarkerColor())
    marker2.SetMarkerSize(0.9*hptQEff.GetMarkerSize())
    marker2.Draw()
    
    tex5 = ROOT.TLatex(0.2,0.95,"7 TeV                        CMS Preliminary ")
    tex5.SetNDC()
    tex5.SetTextSize(20)
    tex5.Draw()
    
    tex6 = ROOT.TLatex(0.2,0.85,"Discriminator > 1.7")
    tex6.SetNDC()
    tex6.SetTextSize(18)
    tex6.Draw()        

    canvas5.Print("etaBEff_disc17.png")
    canvas5.Print("etaBEff_disc17.C")

    
    etaBtagged33._setLegendStyles()
    etaBtagged33._setLegendLabels()
    etaBtagged33.histoMgr.setHistoDrawStyleAll("P")
    etaBtagged33.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))    
    hetaBtagged33 = etaBtagged33.histoMgr.getHisto("TTJets").getRootHisto().Clone(analysis+"/Btagging/realbjet33_eta")
    
    etaQtagged33._setLegendStyles()
    etaQtagged33._setLegendLabels()
    etaQtagged33.histoMgr.setHistoDrawStyleAll("P")
    etaQtagged33.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))    
    hetaQtagged33 = etaQtagged33.histoMgr.getHisto("QCD").getRootHisto().Clone(analysis+"/Btagging/realqjet33_eta")
    
        
    hetaBEff33 = hetaBtagged33.Clone("hetaBEff33")
    hetaBEff33.SetName("hptBEff33")
    hetaBEff33.SetTitle("Efficiency33 B jet")
    hetaBEff33.Divide(hetaB)

    hetaQEff33 = hetaQtagged33.Clone("hetaQEff33")
    hetaQEff33.SetName("hetaQEff33")
    hetaQEff33.SetTitle("Efficiency33 Q jet")
    hetaQEff33.Divide(hetaQ)    

    canvas6 = ROOT.TCanvas("canvas6","",500,500)
    canvas6.SetLogy()
    hetaBEff33.SetMinimum(0.01)
    hetaBEff33.SetMarkerColor(2)
    hetaBEff33.SetMarkerSize(1)
    hetaBEff33.SetMarkerStyle(22)
    hetaBEff33.Draw("EP")


    hetaQEff33.SetMarkerColor(4)
    hetaQEff33.SetMarkerSize(1)
    hetaQEff33.SetMarkerStyle(24)
    hetaQEff33.Draw("same")
    
    hetaBEff33.GetYaxis().SetTitle("B-tagging efficiency")
    hetaBEff33.GetYaxis().SetTitleOffset(1.5)
    hetaBEff33.GetXaxis().SetTitle("#eta^{jet}")
    

    tex1 = ROOT.TLatex(0.45,0.55,"b jets in tt events")
    tex1.SetNDC()
    tex1.SetTextSize(20)
    tex1.Draw()    
    marker1 = ROOT.TMarker(0.42,0.56,hptBEff.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(hptBEff.GetMarkerColor())
    marker1.SetMarkerSize(0.9*hptBEff.GetMarkerSize())
    marker1.Draw()
    
    tex2 = ROOT.TLatex(0.25,0.18,"q or g jets in QCD events") 
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw()    
    marker2 = ROOT.TMarker(0.22,0.19,hptQEff.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(hptQEff.GetMarkerColor())
    marker2.SetMarkerSize(0.9*hptQEff.GetMarkerSize())
    marker2.Draw()
    
    tex5 = ROOT.TLatex(0.2,0.95,"7 TeV                        CMS Preliminary ")
    tex5.SetNDC()
    tex5.SetTextSize(20)
    tex5.Draw()

    
    tex6 = ROOT.TLatex(0.2,0.85,"Discriminator > 3.3")
    tex6.SetNDC()
    tex6.SetTextSize(18)
    tex6.Draw()        

    canvas6.Print("etaBEff_disc33.png")
    canvas6.Print("etaBEff_disc33.C")

    
  
def printCounters(datasets):
    eventCounter = counter.EventCounter(datasets)
    eventCounter.normalizeMCByLuminosity()
    print "============================================================"
    print "Main counter (MC normalized by collision data luminosity)"
    print eventCounter.getMainCounterTable().format()

if __name__ == "__main__":
    main()
