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



    datasets2 = dataset.getDatasetsFromMulticrabCfg(cfgfile="/home/rkinnune/signalAnalysisJune/CMSSW_4_4_4/src/HiggsAnalysis/HeavyChHiggsToTauNu/test/multicrab_120812_204356/multicrab.cfg", counters=counters)
    datasets2.updateNAllEventsToPUWeighted()
    datasets2.loadLuminosities()
    plots.mergeRenameReorderForDataMC(datasets2)


#    datasets3 = dataset.getDatasetsFromMulticrabCfg(cfgfile="/home/rkinnune/signalAnalysis/CMSSW_4_4_4/src/HiggsAnalysis/HeavyChHiggsToTauNu/test/multicrab_120607_075512/multicrab.cfg", counters=counters)
#    datasets3.updateNAllEventsToPUWeighted()
#    datasets3.loadLuminosities()
#    plots.mergeRenameReorderForDataMC(datasets3)
#    datasets2.selectAndReorder(["TTJets_TuneZ2_Fall11","TTToHplusBWB_M120_Fall11"])
#    datasets2.rename("TTJets_TuneZ2_Fall11","TTJets2")
#    datasets2.rename("TTToHplusBWB_M120_Fall11","TTToHplusBWB_M120_2")     
#    datasets.extend(datasets2)     

#    plot(datasets, datasets2, datasets3)
    
    plot(datasets, datasets2)
    printCounters(datasets)





def plot(datasets, datasets2):
    

    mtVeto = plots.PlotBase([datasets2.getDataset("TTJets").getDatasetRootHisto(analysis+"/transverseMass")])
    mtNoVeto = plots.PlotBase([datasets.getDataset("TTJets").getDatasetRootHisto(analysis+"/transverseMass")])
#    mtAntiVeto = plots.PlotBase([datasets3.getDataset("TTJets").getDatasetRootHisto(analysis+"/transverseMass")])
    
    mtVeto.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mtNoVeto.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
#    mtAntiVeto.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
  
    
    mtVeto._setLegendStyles()
    mtVeto._setLegendLabels()
    mtVeto.histoMgr.setHistoDrawStyleAll("P")
    mtVeto.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))    
    hmtVeto = mtVeto.histoMgr.getHisto("TTJets").getRootHisto().Clone(analysis+"/transversemass")
    
    mtNoVeto._setLegendStyles()
    mtNoVeto._setLegendLabels()
    mtNoVeto.histoMgr.setHistoDrawStyleAll("P")
    mtNoVeto.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))    
    hmtNoVeto = mtNoVeto.histoMgr.getHisto("TTJets").getRootHisto().Clone(analysis+"/transversemass")
    
#    mtAntiVeto._setLegendStyles()
#    mtAntiVeto._setLegendLabels()
#    mtAntiVeto.histoMgr.setHistoDrawStyleAll("P")
#    mtAntiVeto.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))    
#    hmtAntiVeto = mtAntiVeto.histoMgr.getHisto("TTJets").getRootHisto().Clone(analysis+"/transversemass")


  
    
    canvas3 = ROOT.TCanvas("canvas3","",500,500)
#    canvas3.SetLogy()
#    hmtVetohptIsolEff.SetMaximum(0.1)
    hmtVeto.SetMinimum(0.01)
    hmtVeto.SetMarkerColor(2)
    hmtVeto.SetMarkerSize(1)
    hmtVeto.SetMarkerStyle(24)
    hmtVeto.Draw("EP")

    
    hmtNoVeto.SetMarkerColor(4)
    hmtNoVeto.SetMarkerSize(1)
    hmtNoVeto.SetMarkerStyle(20)
    hmtNoVeto.Draw("same")
    
#    hmtAntiVeto.SetMarkerColor(4)
#    hmtAntiVeto.SetMarkerSize(1)
#    hmtAntiVeto.SetMarkerStyle(21)
#    hmtAntiVeto.Draw("same")
    
    hmtVeto.GetYaxis().SetTitle("Events / 20 GeV/c^{2}")
    hmtVeto.GetYaxis().SetTitleOffset(1.5)
    hmtVeto.GetXaxis().SetTitle("m_{T}(#tau jet, MET) (GeV/c^{2})")

    tex1 = ROOT.TLatex(0.55,0.7,"No #tau-jet veto")
    tex1.SetNDC()
    tex1.SetTextSize(20)
    tex1.Draw()    
    marker1 = ROOT.TMarker(0.5,0.72,hmtNoVeto.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(hmtNoVeto.GetMarkerColor())
    marker1.SetMarkerSize(0.9*hmtNoVeto.GetMarkerSize())
    marker1.Draw()
    
    
    tex3 = ROOT.TLatex(0.55,0.6,"With #tau-jet veto")
    tex3.SetNDC()
    tex3.SetTextSize(20)
    tex3.Draw()    
    marker3 = ROOT.TMarker(0.5,0.62,hmtVeto.GetMarkerStyle())
    marker3.SetNDC()
    marker3.SetMarkerColor(hmtVeto.GetMarkerColor())
    marker3.SetMarkerSize(0.9*hmtVeto.GetMarkerSize())
    marker3.Draw()
    
#    tex2 = ROOT.TLatex(0.55,0.5,"With additional #tau jets") 
#    tex2.SetNDC()
#    tex2.SetTextSize(20)
#    tex2.Draw()    
#    marker2 = ROOT.TMarker(0.5,0.52,hmtAntiVeto.GetMarkerStyle())
#    marker2.SetNDC()
#    marker2.SetMarkerColor(hmtAntiVeto.GetMarkerColor())
#    marker2.SetMarkerSize(0.9*hmtAntiVeto.GetMarkerSize())
#    marker2.Draw()

    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV                        CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
#    tex5 = ROOT.TLatex(0.55,0.9,"Signal, m_{H^{#pm}} = 120 GeV/c^{2}")
    tex5 = ROOT.TLatex(0.55,0.85,"tt+jets") 
    tex5.SetNDC()
    tex5.SetTextSize(20)
    tex5.Draw()
    
    canvas3.Print("mTtauVeto_tt.png")
    canvas3.Print("mTtauVeto_tt.C")
    
############################################################

    mtVeto2 = plots.PlotBase([datasets2.getDataset("TTToHplusBWB_M120").getDatasetRootHisto(analysis+"/transverseMass")])
    mtNoVeto2 = plots.PlotBase([datasets.getDataset("TTToHplusBWB_M120").getDatasetRootHisto(analysis+"/transverseMass")])
#    mtAntiVeto2 = plots.PlotBase([datasets3.getDataset("TTToHplusBWB_M120").getDatasetRootHisto(analysis+"/transverseMass")])
    
    mtVeto2.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mtNoVeto2.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
#    mtAntiVeto2.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
  
    
    mtVeto2._setLegendStyles()
    mtVeto2._setLegendLabels()
    mtVeto2.histoMgr.setHistoDrawStyleAll("P")
    mtVeto2.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))    
    hmtVeto2 = mtVeto2.histoMgr.getHisto("TTToHplusBWB_M120").getRootHisto().Clone(analysis+"/transversemass")

    mtNoVeto2._setLegendStyles()
    mtNoVeto2._setLegendLabels()
    mtNoVeto2.histoMgr.setHistoDrawStyleAll("P")
    mtNoVeto2.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))    
    hmtNoVeto2 = mtNoVeto2.histoMgr.getHisto("TTToHplusBWB_M120").getRootHisto().Clone(analysis+"/transversemass")
    
#    mtAntiVeto2._setLegendStyles()
#    mtAntiVeto2._setLegendLabels()
#    mtAntiVeto2.histoMgr.setHistoDrawStyleAll("P")
#    mtAntiVeto2.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))    
#    hmtAntiVeto2 = mtAntiVeto2.histoMgr.getHisto("TTToHplusBWB_M120").getRootHisto().Clone(analysis+"/transversemass")


  
    
    canvas4 = ROOT.TCanvas("canvas4","",500,500)
#    canvas4.SetLogy()
#    hmtVetohptIsolEff.SetMaximum(0.1)
    hmtVeto2.SetMinimum(0.002)
    hmtVeto2.SetMarkerColor(2)
    hmtVeto2.SetMarkerSize(1)
    hmtVeto2.SetMarkerStyle(24)
    hmtVeto2.Draw("EP")

    hmtNoVeto2.SetMarkerColor(4)
    hmtNoVeto2.SetMarkerSize(1)
    hmtNoVeto2.SetMarkerStyle(20)
    hmtNoVeto2.Draw("same")
    
#    hmtAntiVeto2.SetMarkerColor(4)
#    hmtAntiVeto2.SetMarkerSize(1)
#    hmtAntiVeto2.SetMarkerStyle(21)
#    hmtAntiVeto2.Draw("same")
    
    hmtVeto2.GetYaxis().SetTitle("Events / 20 GeV/c^{2}")

    hmtVeto2.GetYaxis().SetTitleOffset(1.5)
    hmtVeto2.GetXaxis().SetTitle("m_{T}(#tau jet, MET) (GeV/c^{2})")
    
    tex1 = ROOT.TLatex(0.55,0.7,"No #tau-jet veto")
    tex1.SetNDC()
    tex1.SetTextSize(20)
    tex1.Draw()    
    marker1 = ROOT.TMarker(0.5,0.71,hmtNoVeto2.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(hmtNoVeto2.GetMarkerColor())
    marker1.SetMarkerSize(0.9*hmtNoVeto2.GetMarkerSize())
    marker1.Draw()
    
    tex3 = ROOT.TLatex(0.55,0.6,"With #tau-jet veto")
    tex3.SetNDC()
    tex3.SetTextSize(20)
    tex3.Draw()    
    marker3 = ROOT.TMarker(0.5,0.61,hmtVeto2.GetMarkerStyle())
    marker3.SetNDC()
    marker3.SetMarkerColor(hmtVeto2.GetMarkerColor())
    marker3.SetMarkerSize(0.9*hmtVeto2.GetMarkerSize())
    marker3.Draw()  
#    tex2 = ROOT.TLatex(0.55,0.5,"With additional #tau jets") 
#    tex2.SetNDC()
#    tex2.SetTextSize(20)
#    tex2.Draw()    
#    marker2 = ROOT.TMarker(0.5,0.51,hmtAntiVeto2.GetMarkerStyle())
#    marker2.SetNDC()
#    marker2.SetMarkerColor(hmtAntiVeto2.GetMarkerColor())
#    marker2.SetMarkerSize(0.9*hmtAntiVeto2.GetMarkerSize())
#    marker2.Draw()

    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV                        CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    tex5 = ROOT.TLatex(0.5,0.85,"Signal, m_{H^{#pm}} = 120 GeV/c^{2}")
#    tex5 = ROOT.TLatex(0.55,0.85,"tt+jets") 
    tex5.SetNDC()
    tex5.SetTextSize(20)
    tex5.Draw()
    
    canvas4.Print("mTtauVeto_h120.png")
    canvas4.Print("mTtauVeto_h120.C")

  
 
 ########################################

 
    
def printCounters(datasets):
    eventCounter = counter.EventCounter(datasets)
    eventCounter.normalizeMCByLuminosity()
    print "============================================================"
    print "Main counter (MC normalized by collision data luminosity)"
    print eventCounter.getMainCounterTable().format()

if __name__ == "__main__":
    main()
