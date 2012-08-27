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



#    datasets2 = dataset.getDatasetsFromMulticrabCfg(cfgfile="/home/rkinnune/signalAnalysisJune/CMSSW_4_4_4/src/HiggsAnalysis/HeavyChHiggsToTauNu/test/multicrab_120812_204356/multicrab.cfg", counters=counters)
#    datasets2.updateNAllEventsToPUWeighted()
#    datasets2.loadLuminosities()
#    plots.mergeRenameReorderForDataMC(datasets2)


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





#def plot(datasets, datasets2):
def plot(datasets):    

    mt = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/transverseMassNoBtagging")])
    mtRtau = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/transverseMassNoBtaggingWithRtau")])
#    mtAntiVeto = plots.PlotBase([datasets3.getDataset("TTJets").getDatasetRootHisto(analysis+"/transverseMass")])


#    mt.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
#    mtRtau.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
#    mtAntiVeto.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
  
    dataset._normalizeToOne(mt.histoMgr.getHisto("Data").getRootHisto())    
    mt._setLegendStyles()
    mt._setLegendLabels()
    mt.histoMgr.setHistoDrawStyleAll("P")
    mt.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))    
    hmt = mt.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/transversemassNoBtagging")

    
    dataset._normalizeToOne(mtRtau.histoMgr.getHisto("Data").getRootHisto())    
    mtRtau._setLegendStyles()
    mtRtau._setLegendLabels()
    mtRtau.histoMgr.setHistoDrawStyleAll("P")
    mtRtau.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))    
    hmtRtau = mtRtau.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/transversemassNoBtaggingWithRtau")
                            

      
    canvas3 = ROOT.TCanvas("canvas3","",500,500)
#    canvas3.SetLogy()
    hmt.SetMaximum(0.4)
#    hmt.SetMinimum(0.01)
    hmt.SetMarkerColor(2)
    hmt.SetMarkerSize(1)
    hmt.SetMarkerStyle(24)
    hmt.SetLineWidth(2)
    hmt.SetLineColor(2)
    hmt.Draw("EP")

    
    hmtRtau.SetMarkerColor(ROOT.kGreen+2)
    hmtRtau.SetMarkerSize(1)
    hmtRtau.SetMarkerStyle(20)
    hmtRtau.SetLineWidth(2)
    hmtRtau.SetLineColor(ROOT.kGreen+2)
    hmtRtau.Draw("same")
    
#    hmtAntiVeto.SetMarkerColor(4)
#    hmtAntiVeto.SetMarkerSize(1)
#    hmtAntiVeto.SetMarkerStyle(21)
#    hmtAntiVeto.Draw("same")
    
    hmt.GetYaxis().SetTitle("Events / 20 GeV/c^{2}")
    hmt.GetYaxis().SetTitleOffset(1.5)
    hmt.GetXaxis().SetTitle("m_{T}(#tau jet, MET) (GeV/c^{2})")

    tex1 = ROOT.TLatex(0.65,0.7,"No Rtau cut")
    tex1.SetNDC()
    tex1.SetTextSize(20)
    tex1.Draw()    
    marker1 = ROOT.TMarker(0.6,0.72,hmt.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(hmt.GetMarkerColor())
    marker1.SetMarkerSize(1.3*hmt.GetMarkerSize())
    marker1.Draw()
    
    
    tex3 = ROOT.TLatex(0.65,0.6,"With Rtau cut")
    tex3.SetNDC()
    tex3.SetTextSize(20)
    tex3.Draw()    
    marker3 = ROOT.TMarker(0.6,0.62,hmtRtau.GetMarkerStyle())
    marker3.SetNDC()
    marker3.SetMarkerColor(hmtRtau.GetMarkerColor())
    marker3.SetMarkerSize(1.3*hmtRtau.GetMarkerSize())
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
    tex5 = ROOT.TLatex(0.55,0.82,"Data") 
    tex5.SetNDC()
    tex5.SetTextSize(25)
    tex5.Draw()
    
    canvas3.Print("mTRtau_data.png")
    canvas3.Print("mTRtau_data.C")
    
 
 
 ########################################

 
    
def printCounters(datasets):
    eventCounter = counter.EventCounter(datasets)
    eventCounter.normalizeMCByLuminosity()
    print "============================================================"
    print "Main counter (MC normalized by collision data luminosity)"
    print eventCounter.getMainCounterTable().format()

if __name__ == "__main__":
    main()
