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

    etabTop = plots.PlotBase([datasets.getDataset("HplusTB_M200").getDatasetRootHisto(analysis+"/GenParticleAnalysis/genBquark_FromTop_Eta_ptcut")])
    etabNoTop = plots.PlotBase([datasets.getDataset("HplusTB_M200").getDatasetRootHisto(analysis+"/GenParticleAnalysis/genBquark_NotFromTop_Eta_ptcut")])

 
    etabTop.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    etabNoTop.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())

   
    ptbTop = plots.PlotBase([datasets.getDataset("HplusTB_M200").getDatasetRootHisto(analysis+"/GenParticleAnalysis/genBquark_FromTop_Pt_etacut")])
    ptbNoTop = plots.PlotBase([datasets.getDataset("HplusTB_M200").getDatasetRootHisto(analysis+"/GenParticleAnalysis/genBquark_NotFromTop_Pt_etacut")])
 
    
    ptbTop.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    ptbNoTop.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())

    etabTop._setLegendStyles()
    etabTop._setLegendLabels()
    etabTop.histoMgr.setHistoDrawStyleAll("P")
    etabTop.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))    
    hetabTop = etabTop.histoMgr.getHisto("HplusTB_M200").getRootHisto().Clone(analysis+"/GenParticleAnalysis/genBquark_FromTop_Eta_ptcut")

    etabNoTop._setLegendStyles()
    etabNoTop._setLegendLabels()
    etabNoTop.histoMgr.setHistoDrawStyleAll("P")
    etabNoTop.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))    
    hetabNoTop = etabNoTop.histoMgr.getHisto("HplusTB_M200").getRootHisto().Clone(analysis+"/GenParticleAnalysis/genBquark_NotFromTop_Eta_ptcut")


    ptbTop._setLegendStyles()
    ptbTop._setLegendLabels()
    ptbTop.histoMgr.setHistoDrawStyleAll("P")
    ptbTop.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))    
    hptbTop = ptbTop.histoMgr.getHisto("HplusTB_M200").getRootHisto().Clone(analysis+"/GenParticleAnalysis/genBquark_FromTop_Pt_etacut")

    ptbNoTop._setLegendStyles()
    ptbNoTop._setLegendLabels()
    ptbNoTop.histoMgr.setHistoDrawStyleAll("P")
    ptbNoTop.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))    
    hptbNoTop = ptbNoTop.histoMgr.getHisto("HplusTB_M200").getRootHisto().Clone(analysis+"/GenParticleAnalysis/genBquark_NotFromTop_Pt_etacut")

  
    
    canvas4 = ROOT.TCanvas("canvas4","",500,500)
#    canvas4.SetLogy()
#    hmtVetohptIsolEff.SetMaximum(0.1)
    hetabNoTop.SetMaximum(17000)
    hetabNoTop.SetMarkerColor(4)
    hetabNoTop.SetMarkerSize(1)
    hetabNoTop.SetMarkerStyle(24)
    hetabNoTop.Draw("EP")

    
    hetabTop.SetMarkerColor(2)
    hetabTop.SetMarkerSize(1)
    hetabTop.SetMarkerStyle(20)
    hetabTop.Draw("same")

    
    hetabNoTop.GetYaxis().SetTitle("Events")

    hetabNoTop.GetYaxis().SetTitleOffset(2.0)
    hetabNoTop.GetXaxis().SetTitle("#eta^{b quark}")
    
 
    
    tex3 = ROOT.TLatex(0.23,0.9,"b quark from top")
    tex3.SetNDC()
    tex3.SetTextSize(20)
    tex3.Draw()    
    marker3 = ROOT.TMarker(0.2,0.92,hetabTop.GetMarkerStyle())
    marker3.SetNDC()
    marker3.SetMarkerColor(hetabTop.GetMarkerColor())
    marker3.SetMarkerSize(0.9*hetabTop.GetMarkerSize())
    marker3.Draw()

    tex1 = ROOT.TLatex(0.23,0.85,"b quark from hard process ")
    tex1.SetNDC()
    tex1.SetTextSize(20)
    tex1.Draw()    
    marker1 = ROOT.TMarker(0.2,0.87,hetabNoTop.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(hetabNoTop.GetMarkerColor())
    marker1.SetMarkerSize(0.9*hetabNoTop.GetMarkerSize())
    marker1.Draw()
    
    
 

    
    tex4 = ROOT.TLatex(0.2,0.96,"7 TeV                        CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    tex5 = ROOT.TLatex(0.2,0.78,"m_{H^{#pm}} = 200 GeV/c^{2}")
#    tex5 = ROOT.TLatex(0.55,0.85,"tt+jets") 
    tex5.SetNDC()
    tex5.SetTextSize(20)
    tex5.Draw()
    
    tex6 = ROOT.TLatex(0.2,0.72,"p_{T}^{b quark} > 20 GeV/c")
    tex6.SetNDC()
    tex6.SetTextSize(20)
    tex6.Draw()
    
    canvas4.Print("BquarkComparison_eta.png")
    canvas4.Print("BquarkComparison_eta.C")


##################################################

    canvas5 = ROOT.TCanvas("canvas5","",500,500)
    canvas5.SetLogy()
#    hmtVetohptIsolEff.SetMaximum(0.1)
#    hetabTop.SetMinimum(2000)
    hptbNoTop.SetMarkerColor(4)
    hptbNoTop.SetMarkerSize(1)
    hptbNoTop.SetMarkerStyle(24)
    hptbNoTop.Draw("EP")

    
    hptbTop.SetMarkerColor(2)
    hptbTop.SetMarkerSize(1)
    hptbTop.SetMarkerStyle(20)
    hptbTop.Draw("same")

    
    hptbNoTop.GetYaxis().SetTitle("Events")

    hptbNoTop.GetYaxis().SetTitleOffset(2.0)
    hptbNoTop.GetXaxis().SetTitle("p_{T}^{b quark} (GeV/c)")
    
 
    
    tex3 = ROOT.TLatex(0.43,0.85,"b quark from top")
    tex3.SetNDC()
    tex3.SetTextSize(20)
    tex3.Draw()    
    marker3 = ROOT.TMarker(0.4,0.87,hetabTop.GetMarkerStyle())
    marker3.SetNDC()
    marker3.SetMarkerColor(hetabTop.GetMarkerColor())
    marker3.SetMarkerSize(0.9*hetabTop.GetMarkerSize())
    marker3.Draw()

    tex1 = ROOT.TLatex(0.43,0.8,"b quark hard process")
    tex1.SetNDC()
    tex1.SetTextSize(20)
    tex1.Draw()    
    marker1 = ROOT.TMarker(0.4,0.82,hetabNoTop.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(hetabNoTop.GetMarkerColor())
    marker1.SetMarkerSize(0.9*hetabNoTop.GetMarkerSize())
    marker1.Draw()
    
    
 

    
    tex4 = ROOT.TLatex(0.2,0.96,"7 TeV                        CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    tex5 = ROOT.TLatex(0.6,0.7,"m_{H^{#pm}} = 200 GeV/c^{2}")
#    tex5 = ROOT.TLatex(0.55,0.85,"tt+jets") 
    tex5.SetNDC()
    tex5.SetTextSize(20)
    tex5.Draw()
    
    tex6 = ROOT.TLatex(0.6,0.62,"|#eta^{b quark}| < 2.4")
    tex6.SetNDC()
    tex6.SetTextSize(20)
    tex6.Draw()

    
    canvas5.Print("BquarkComparison_pt.png")
    canvas5.Print("BquarkComparison_pt.C")

    
 
 ########################################

 
    
def printCounters(datasets):
    eventCounter = counter.EventCounter(datasets)
    eventCounter.normalizeMCByLuminosity()
    print "============================================================"
    print "Main counter (MC normalized by collision data luminosity)"
    print eventCounter.getMainCounterTable().format()

if __name__ == "__main__":
    main()
