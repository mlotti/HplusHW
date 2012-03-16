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
    
    hptBEff = hptBtagged.Clone("hptBEff")
    hptBEff.SetName("hptBEff")
    hptBEff.SetTitle("Efficiency B jet")
    hptBEff.Divide(hptB)

    canvas3 = ROOT.TCanvas("canvas3","",500,500)
#    canvas3.SetLogy()
#    hmt.SetMaximum(3.0)
    hptBEff.SetMarkerColor(2)
    hptBEff.SetMarkerSize(1)
    hptBEff.SetMarkerStyle(21)
    hptBEff.Draw("EP")
    
    hptBEff.GetYaxis().SetTitle("Events / 10 GeV/c^{2}")
    hptBEff.GetYaxis().SetTitleOffset(1.5)
    hptBEff.GetXaxis().SetTitle("m_{T}(#tau jet, MET) (GeV/c^{2})")
    
    canvas3.Print("ptBEff.png")
    canvas3.Print("ptBEff.C")

    
    
    metCut = "met_p4.Et() > 50"
    tauPtCut = "tau_p4.Pt() > 40"
    jetNumCut = "Sum$(jets_p4.Pt() > 30) >= 3"
    tauLeadingCandPtCut = "tau_leadPFChargedHadrCand_p4.Pt() > 20"
    rtauCut = "tau_leadPFChargedHadrCand_p4.P()/tau_p4.P() > 0.7"
    btag = "jets_btag > 1.7"
    bjet = "abs(jets_flavour) == 5"
    qjet = "abs(jets_flavour) < 4 || jets_flavour > 20"
    deltaPhiCut = "acos((tau_p4.Px()*met_p4.Px()+tau_p4.Py()*met_p4.Py())/tau_p4.Pt()/met_p4.Et())*57.2958 < 160"
    
    tauSelCut = "tau_p4.Pt() > 40 && tau_leadPFChargedHadrCand_p4.Pt() > 20 && tau_leadPFChargedHadrCand_p4.P()/tau_p4.P() > 0.7"
    tauJetsCut = "tau_p4.Pt() > 40 && tau_leadPFChargedHadrCand_p4.Pt() > 20 && tau_leadPFChargedHadrCand_p4.P()/tau_p4.P() > 0.7 && Sum$(jets_p4.Pt() > 30) >= 3 "
    tauJetsMetCut = "tau_p4.Pt() > 40 && tau_leadPFChargedHadrCand_p4.Pt() > 20 && tau_leadPFChargedHadrCand_p4.P()/tau_p4.P() > 0.7 && Sum$(jets_p4.Pt() > 30) >= 3 && met_p4.Et() > 50"

 
    noTagging = jetNumCut + "&&abs(jets_flavour)==5"    
    btagging = noTagging + "&&jets_btag > 3.3"
    noTaggingLight = jetNumCut + "&&(abs(jets_flavour) < 4 || jets_flavour > 20)"
#    noTaggingLight = jetNumCut + "&&abs(jets_flavour) == 1"
#    noTaggingLight = jetNumCut + "&&abs(jets_flavour) != 5"
    btaggingLight = noTaggingLight + "&&jets_btag > 3.3" 
    noTaggingMet = jetNumCut + "&&met_p4.Et() > 50" + "&&abs(jets_flavour)==5"    
    btaggingMet = noTaggingMet + "&&jets_btag > 3.3" 



###########################################
    
    hpt = plots.DataMCPlot(datasets, treeDraw.clone(varexp="jets_p4.Et()>>dist(25,0,500)", selection=noTagging))
    hptb = plots.DataMCPlot(datasets, treeDraw.clone(varexp="jets_p4.Et()>>dist(25,0,500)", selection=btagging))
    
    hptQ = plots.DataMCPlot(datasets, treeDraw.clone(varexp="jets_p4.Et()>>dist(25,0,500)", selection=noTaggingLight))
    hptbQ = plots.DataMCPlot(datasets, treeDraw.clone(varexp="jets_p4.Et()>>dist(25,0,500)", selection=btaggingLight))
    

##################################################
    #  MET cut comparison  b jets
  # Clone the data one
    hpt120 = hpt.histoMgr.getHisto("TTToHplusBWB_M120").getRootHisto().Clone("TTToHplusBWB_M120")
    hpt120_btag = hptb.histoMgr.getHisto("TTToHplusBWB_M120").getRootHisto().Clone("TTToHplusBWB_M120")
#    hpt120_btag = hptb.histoMgr.getHisto("TTToHplusBWB_M120").getRootHisto()


    canvas9 = ROOT.TCanvas("canvas9","",500,500)
    canvas9.SetLogy()
#    hmt.SetMaximum(3.0)
    hpt120.SetMarkerColor(2)
    hpt120.SetMarkerSize(1)
    hpt120.SetMarkerStyle(21)
    hpt120.SetLineStyle(1)
    hpt120.SetLineWidth(1)
    hpt120.Draw("EP")
    hpt120_btag.SetMarkerColor(4)
    hpt120_btag.SetMarkerSize(1)
    hpt120_btag.SetMarkerStyle(25)
    hpt120_btag.SetLineStyle(1)
    hpt120_btag.SetLineWidth(1)
    hpt120_btag.Draw("same")
    canvas9.Print("test_pt.png")     

    hptt = hpt.histoMgr.getHisto("TTJets").getRootHisto().Clone("TTJets")
    hptt_btag = hptb.histoMgr.getHisto("TTJets").getRootHisto()

    # tagged et / et 
    hpt120_btag.Divide(hpt120)
    hpt120_btag.SetName("btagEff_pt")


# jet Et with b tagging and tau Et cut
    hptmetb = plots.DataMCPlot(datasets, treeDraw.clone(varexp="jets_p4.Et()>>dist(25,0,500)", selection=btaggingMet))
    hptmet = plots.DataMCPlot(datasets, treeDraw.clone(varexp="jets_p4.Et()>>dist(25,0,500)", selection=noTaggingMet))

  # Clone the data one
    hptmet120 = hptmet.histoMgr.getHisto("TTToHplusBWB_M120").getRootHisto().Clone("TTToHplusBWB_M120")
    hptmet120_btag = hptmetb.histoMgr.getHisto("TTToHplusBWB_M120").getRootHisto()
    # tagged et / et 
    hptmet120_btag.Divide(hptmet120)
    hptmet120_btag.SetName("btagEff_pt_metcut")


    canvas3 = ROOT.TCanvas("canvas3","",500,500)
    canvas3.SetLogy()
#    hmt.SetMaximum(3.0)
    hpt120_btag.SetMarkerColor(2)
    hpt120_btag.SetMarkerSize(1)
    hpt120_btag.SetMarkerStyle(21)
    hpt120_btag.SetLineStyle(1)
    hpt120_btag.SetLineWidth(1)
    hpt120_btag.Draw("EP")
     
    hptmet120_btag.SetMarkerColor(4)
    hptmet120_btag.SetMarkerSize(1)
    hptmet120_btag.SetMarkerStyle(22)
    hptmet120_btag.SetLineStyle(1)
    hptmet120_btag.SetLineColor(4)
    hptmet120_btag.SetLineWidth(1)
    hptmet120_btag.Draw("same")
    
    hpt120_btag.GetYaxis().SetTitle("B-tagging efficiency")
#    hmt.GetYaxis().SetTitleSize(20.0)
#    data_btag.GetYaxis().SetTitleOffset(1.5)
    hpt120_btag.GetXaxis().SetTitle("E_{T}^{jet} (GeV)")

    tex1 = ROOT.TLatex(0.35,0.8,"No MET cut")
    tex1.SetNDC()
    tex1.SetTextSize(20)
    tex1.Draw()    

    marker1 = ROOT.TMarker(0.3,0.815,hpt120_btag.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(hpt120_btag.GetMarkerColor())
    marker1.SetMarkerSize(0.9*hpt120_btag.GetMarkerSize())
    marker1.Draw()   
    tex2 = ROOT.TLatex(0.35,0.7,"MET > 50 GeV") 
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw()    
    marker2 = ROOT.TMarker(0.3,0.715,hptmet120_btag.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(hptmet120_btag.GetMarkerColor())
    marker2.SetMarkerSize(0.9*hptmet120_btag.GetMarkerSize())
    marker2.Draw()

    
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV                        CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()        
    canvas3.Print("btagEff_pt.png")



##################################################
    #  Higgs mass comparison b jets
   
    hpt80 = hpt.histoMgr.getHisto("TTToHplusBWB_M80").getRootHisto().Clone("TTToHplusBWB_M80")
    hpt80_btag = hptb.histoMgr.getHisto("TTToHplusBWB_M80").getRootHisto()

    # tagged et / et 
    hpt80_btag.Divide(hpt80)
    hpt80_btag.SetName("btagEff80_pt")

    hpt160 = hpt.histoMgr.getHisto("TTToHplusBWB_M160").getRootHisto().Clone("TTToHplusBWB_M160")
    hpt160_btag = hptb.histoMgr.getHisto("TTToHplusBWB_M160").getRootHisto()
    # tagged et / et 
    hpt160_btag.Divide(hpt160)
    hpt160_btag.SetName("btagEff160_pt")


    hpttt = hpt.histoMgr.getHisto("TTJets").getRootHisto().Clone("TTJets")
    hpttt_btag = hptb.histoMgr.getHisto("TTJets").getRootHisto()
    # tagged et / et 
    hpttt_btag.Divide(hpttt)
    hpttt_btag.SetName("btagEfftt_pt")

    canvas5 = ROOT.TCanvas("canvas5","",500,500)
    canvas5.SetLogy()
    hpt120_btag.SetMaximum(2.0)
    hpt120_btag.SetMinimum(0.1)
    hpt120_btag.SetMarkerColor(2)
    hpt120_btag.SetMarkerSize(1)
    hpt120_btag.SetMarkerStyle(21)
    hpt120_btag.SetLineStyle(1)
    hpt120_btag.SetLineWidth(1)
    hpt120_btag.Draw("P")
     
    hpt80_btag.SetMarkerColor(4)
    hpt80_btag.SetMarkerSize(1)
    hpt80_btag.SetMarkerStyle(22)
    hpt80_btag.SetLineStyle(1)
    hpt80_btag.SetLineColor(4)
    hpt80_btag.SetLineWidth(1)
    hpt80_btag.Draw("same")

    hpt160_btag.SetMarkerColor(7)
    hpt160_btag.SetMarkerSize(1)
    hpt160_btag.SetMarkerStyle(25)
    hpt160_btag.SetLineStyle(1)
    hpt160_btag.SetLineColor(7)
    hpt160_btag.SetLineWidth(1)
    hpt160_btag.Draw("same")
    
    hpttt_btag.SetMarkerColor(6)
    hpttt_btag.SetMarkerSize(1)
    hpttt_btag.SetMarkerStyle(24)
    hpttt_btag.SetLineStyle(1)
    hpttt_btag.SetLineColor(6)
    hpttt_btag.SetLineWidth(1)
    hpttt_btag.Draw("same")
    
    hpt120_btag.GetYaxis().SetTitle("B-tagging efficiency")
#    hmt.GetYaxis().SetTitleSize(20.0)
#    data_btag.GetYaxis().SetTitleOffset(1.5)
    hpt120_btag.GetXaxis().SetTitle("E_{T}^{jet} (GeV)")

    tex1 = ROOT.TLatex(0.25,0.5,"m_{H^{#pm}} = 120 GeV/c^{2}")
    tex1.SetNDC()
    tex1.SetTextSize(20)
    tex1.Draw()    
    marker1 = ROOT.TMarker(0.22,0.515,hpt120_btag.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(hpt120_btag.GetMarkerColor())
    marker1.SetMarkerSize(0.9*hpt120_btag.GetMarkerSize())
    marker1.Draw()
    
    tex2 = ROOT.TLatex(0.25,0.45,"m_{H^{#pm}} = 80 GeV/c^{2}") 
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw()    
    marker2 = ROOT.TMarker(0.22,0.455,hpt80_btag.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(hpt80_btag.GetMarkerColor())
    marker2.SetMarkerSize(0.9*hpt80_btag.GetMarkerSize())
    marker2.Draw()
    
    tex3 = ROOT.TLatex(0.25,0.4,"m_{H^{#pm}} = 160 GeV/c^{2}") 
    tex3.SetNDC()
    tex3.SetTextSize(20)
    tex3.Draw()    
    marker3 = ROOT.TMarker(0.22,0.415,hpt160_btag.GetMarkerStyle())
    marker3.SetNDC()
    marker3.SetMarkerColor(hpt160_btag.GetMarkerColor())
    marker3.SetMarkerSize(0.9*hpt160_btag.GetMarkerSize())
    marker3.Draw()

    
    tex4 = ROOT.TLatex(0.25,0.35,"tt") 
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()    
    marker4 = ROOT.TMarker(0.22,0.355,hpttt_btag.GetMarkerStyle())
    marker4.SetNDC()
    marker4.SetMarkerColor(hpttt_btag.GetMarkerColor())
    marker4.SetMarkerSize(0.9*hpttt_btag.GetMarkerSize())
    marker4.Draw()
    
    tex9 = ROOT.TLatex(0.2,0.85,"Discriminator > 3.3 ")
    tex9.SetNDC()
    tex9.SetTextSize(20)
    tex9.Draw() 
    
    tex5 = ROOT.TLatex(0.2,0.95,"7 TeV                        CMS Preliminary ")
    tex5.SetNDC()
    tex5.SetTextSize(20)
    tex5.Draw()        
    canvas5.Print("btagEff33_pt_mH.png")


    
##################################################
    #  Higgs mass comparison Q jets
   
    hpt120Q = hptQ.histoMgr.getHisto("TTToHplusBWB_M120").getRootHisto().Clone("TTToHplusBWB_M120")
    hpt120Q_btag = hptbQ.histoMgr.getHisto("TTToHplusBWB_M120").getRootHisto()

    canvas9b = ROOT.TCanvas("canvas9b","",500,500)
    canvas9b.SetLogy()
#    hmt.SetMaximum(3.0)
    hpt120Q.SetMarkerColor(2)
    hpt120Q.SetMarkerSize(1)
    hpt120Q.SetMarkerStyle(21)
    hpt120Q.SetLineStyle(1)
    hpt120Q.SetLineWidth(1)
    hpt120Q.Draw("EP")
    hpt120Q_btag.SetMarkerColor(4)
    hpt120Q_btag.SetMarkerSize(1)
    hpt120Q_btag.SetMarkerStyle(25)
    hpt120Q_btag.SetLineStyle(1)
    hpt120Q_btag.SetLineWidth(1)
    hpt120Q_btag.Draw("same")
    canvas9b.Print("testQ_pt.png")     
    
     # tagged et / et 
    hpt120Q_btag.Divide(hpt120Q)
    hpt120Q_btag.SetName("btagEff120Q_pt")
   
    hpt80Q = hptQ.histoMgr.getHisto("TTToHplusBWB_M80").getRootHisto().Clone("TTToHplusBWB_M80")
    hpt80Q_btag = hptbQ.histoMgr.getHisto("TTToHplusBWB_M80").getRootHisto()

    # tagged et / et 
    hpt80Q_btag.Divide(hpt80Q)
    hpt80Q_btag.SetName("btagEff80Q_pt")

    hpt160Q = hptQ.histoMgr.getHisto("TTToHplusBWB_M160").getRootHisto().Clone("TTToHplusBWB_M160")
    hpt160Q_btag = hptbQ.histoMgr.getHisto("TTToHplusBWB_M160").getRootHisto()
    # tagged et / et 
    hpt160Q_btag.Divide(hpt160Q)
    hpt160Q_btag.SetName("btagEff160Q_pt")


    hptttQ = hptQ.histoMgr.getHisto("TTJets").getRootHisto().Clone("TTJets")
    hptttQ_btag = hptbQ.histoMgr.getHisto("TTJets").getRootHisto()
    # tagged et / et 
    hptttQ_btag.Divide(hptttQ)
    hptttQ_btag.SetName("btagEffttQ_pt")


    hptWjetQ = hptQ.histoMgr.getHisto("WJets").getRootHisto().Clone("WJets")
    hptWjetQ_btag = hptbQ.histoMgr.getHisto("WJets").getRootHisto()
    # tagged et / et 
    hptWjetQ_btag.Divide(hptWjetQ)
    hptWjetQ_btag.SetName("btagEffWjetQ_pt")

    hptqcdQ = hptQ.histoMgr.getHisto("QCD").getRootHisto().Clone("QCD")
    hptqcdQ_btag = hptbQ.histoMgr.getHisto("QCD").getRootHisto()
    # tagged et / et 
    hptqcdQ_btag.Divide(hptqcdQ)
    hptqcdQ_btag.SetName("btagEffqcdQ_pt")

    
    canvas5q = ROOT.TCanvas("canvas5q","",500,500)
    canvas5q.SetLogy()
    hpt120Q_btag.SetMaximum(0.5)
    hpt120Q_btag.SetMinimum(0.001)
    hpt120Q_btag.SetMarkerColor(2)
    hpt120Q_btag.SetMarkerSize(1)
    hpt120Q_btag.SetMarkerStyle(21)
    hpt120Q_btag.SetLineStyle(1)
    hpt120Q_btag.SetLineWidth(1)
    hpt120Q_btag.Draw("P")
     
    hpt80Q_btag.SetMarkerColor(4)
    hpt80Q_btag.SetMarkerSize(1)
    hpt80Q_btag.SetMarkerStyle(22)
    hpt80Q_btag.SetLineStyle(1)
    hpt80Q_btag.SetLineColor(4)
    hpt80Q_btag.SetLineWidth(1)
#    hpt80Q_btag.Draw("same")

    hpt160Q_btag.SetMarkerColor(7)
    hpt160Q_btag.SetMarkerSize(1)
    hpt160Q_btag.SetMarkerStyle(25)
    hpt160Q_btag.SetLineStyle(1)
    hpt160Q_btag.SetLineColor(7)
    hpt160Q_btag.SetLineWidth(1)
#    hpt160Q_btag.Draw("same")
    
    hptttQ_btag.SetMarkerColor(6)
    hptttQ_btag.SetMarkerSize(1)
    hptttQ_btag.SetMarkerStyle(24)
    hptttQ_btag.SetLineStyle(1)
    hptttQ_btag.SetLineColor(6)
    hptttQ_btag.SetLineWidth(1)
    hptttQ_btag.Draw("same")

    hptWjetQ_btag.SetMarkerColor(4)
    hptWjetQ_btag.SetMarkerSize(1)
    hptWjetQ_btag.SetMarkerStyle(22)
    hptWjetQ_btag.SetLineStyle(1)
    hptWjetQ_btag.SetLineColor(4)
    hptWjetQ_btag.SetLineWidth(1)
    hptWjetQ_btag.Draw("same")

    hptqcdQ_btag.SetMarkerColor(1)
    hptqcdQ_btag.SetMarkerSize(1)
    hptqcdQ_btag.SetMarkerStyle(25)
    hptqcdQ_btag.SetLineStyle(1)
    hptqcdQ_btag.SetLineColor(1)
    hptqcdQ_btag.SetLineWidth(1)
    hptqcdQ_btag.Draw("same")
    
    
    hpt120Q_btag.GetYaxis().SetTitle("B-tagging efficiency")
#    hmt.GetYaxis().SetTitleSize(20.0)
#    data_btag.GetYaxis().SetTitleOffset(1.5)
    hpt120Q_btag.GetXaxis().SetTitle("E_{T}^{jet} (GeV)")

    tex1 = ROOT.TLatex(0.25,0.9,"m_{H^{#pm}} = 120 GeV/c^{2}")
    tex1.SetNDC()
    tex1.SetTextSize(20)
    tex1.Draw()    
    marker1 = ROOT.TMarker(0.22,0.915,hpt120Q_btag.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(hpt120Q_btag.GetMarkerColor())
    marker1.SetMarkerSize(0.9*hpt120Q_btag.GetMarkerSize())
    marker1.Draw()
    
    tex2 = ROOT.TLatex(0.25,0.55,"m_{H^{#pm}} = 80 GeV/c^{2}") 
    tex2.SetNDC()
    tex2.SetTextSize(20)
#    tex2.Draw()    
    marker2 = ROOT.TMarker(0.22,0.555,hpt80Q_btag.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(hpt80Q_btag.GetMarkerColor())
    marker2.SetMarkerSize(0.9*hpt80Q_btag.GetMarkerSize())
#    marker2.Draw()
    
    tex3 = ROOT.TLatex(0.25,0.8,"m_{H^{#pm}} = 160 GeV/c^{2}") 
    tex3.SetNDC()
    tex3.SetTextSize(20)
#    tex3.Draw()    
    marker3 = ROOT.TMarker(0.22,0.815,hpt160Q_btag.GetMarkerStyle())
    marker3.SetNDC()
    marker3.SetMarkerColor(hpt160Q_btag.GetMarkerColor())
    marker3.SetMarkerSize(0.9*hpt160Q_btag.GetMarkerSize())
#    marker3.Draw()

    
    tex4 = ROOT.TLatex(0.25,0.85,"tt") 
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()    
    marker4 = ROOT.TMarker(0.22,0.855,hptttQ_btag.GetMarkerStyle())
    marker4.SetNDC()
    marker4.SetMarkerColor(hptttQ_btag.GetMarkerColor())
    marker4.SetMarkerSize(0.9*hptttQ_btag.GetMarkerSize())
    marker4.Draw()

    tex5 = ROOT.TLatex(0.25,0.8,"Wjets") 
    tex5.SetNDC()
    tex5.SetTextSize(20)
    tex5.Draw()    
    marker5 = ROOT.TMarker(0.22,0.815,hptWjetQ_btag.GetMarkerStyle())
    marker5.SetNDC()
    marker5.SetMarkerColor(hptWjetQ_btag.GetMarkerColor())
    marker5.SetMarkerSize(0.9*hptWjetQ_btag.GetMarkerSize())
    marker5.Draw()

    tex8 = ROOT.TLatex(0.25,0.75,"QCD") 
    tex8.SetNDC()
    tex8.SetTextSize(20)
    tex8.Draw()    
    marker8 = ROOT.TMarker(0.22,0.757,hptqcdQ_btag.GetMarkerStyle())
    marker8.SetNDC()
    marker8.SetMarkerColor(hptqcdQ_btag.GetMarkerColor())
    marker8.SetMarkerSize(0.9*hptqcdQ_btag.GetMarkerSize())
    marker8.Draw()
    
    tex7 = ROOT.TLatex(0.2,0.95,"7 TeV                        CMS Preliminary ")
    tex7.SetNDC()
    tex7.SetTextSize(20)
    tex7.Draw()


    tex9 = ROOT.TLatex(0.3,0.3,"Discriminator > 3.3 ")
    tex9.SetNDC()
    tex9.SetTextSize(20)
    tex9.Draw() 
    canvas5q.Print("QtagEff33_pt_mH.png")


    

########################################################



    heta = plots.DataMCPlot(datasets, treeDraw.clone(varexp="jets_p4.Eta()>>dist(30,-3,3)", selection=noTagging))
    hetab = plots.DataMCPlot(datasets, treeDraw.clone(varexp="jets_p4.Eta()>>dist(30,-3,3)", selection=btagging))
    hetaQ = plots.DataMCPlot(datasets, treeDraw.clone(varexp="jets_p4.Eta()>>dist(30,-3,3)", selection=noTaggingLight))
    hetabQ = plots.DataMCPlot(datasets, treeDraw.clone(varexp="jets_p4.Eta()>>dist(30,-3,3)", selection=btaggingLight))



##################################################
    #  Higgs mass comparison b jets
  
 
    heta120 = heta.histoMgr.getHisto("TTToHplusBWB_M120").getRootHisto().Clone("TTToHplusBWB_M120")
    heta120_btag = hetab.histoMgr.getHisto("TTToHplusBWB_M120").getRootHisto()
    # tagged et / et 
    heta120_btag.Divide(heta120)
    heta120_btag.SetName("btagEff120_eta")

    heta80 = heta.histoMgr.getHisto("TTToHplusBWB_M80").getRootHisto().Clone("TTToHplusBWB_M80")
    heta80_btag = hetab.histoMgr.getHisto("TTToHplusBWB_M80").getRootHisto()

    # tagged et / et 
    heta80_btag.Divide(heta80)
    heta80_btag.SetName("btagEff80_eta")

    heta160 = heta.histoMgr.getHisto("TTToHplusBWB_M160").getRootHisto().Clone("TTToHplusBWB_M160")
    heta160_btag = hetab.histoMgr.getHisto("TTToHplusBWB_M160").getRootHisto()
    # tagged et / et 
    heta160_btag.Divide(heta160)
    heta160_btag.SetName("btagEff160_eta")


    hetatt = heta.histoMgr.getHisto("TTJets").getRootHisto().Clone("TTJets")
    hetatt_btag = hetab.histoMgr.getHisto("TTJets").getRootHisto()
    # tagged et / et 
    hetatt_btag.Divide(hetatt)
    hetatt_btag.SetName("btagEfftt_eta")
    
    hetaWjet = heta.histoMgr.getHisto("WJets").getRootHisto().Clone("WJets")
    hetaWjet_btag = hetab.histoMgr.getHisto("WJets").getRootHisto()
    # tagged et / et 
    hetaWjet_btag.Divide(hetaWjet)
    hetaWjet_btag.SetName("btagEffWjet_eta")

    hetaqcd = heta.histoMgr.getHisto("QCD").getRootHisto().Clone("QCD")
    hetaqcd_btag = hetab.histoMgr.getHisto("QCD").getRootHisto()
    # tagged et / et 
    hetaqcd_btag.Divide(hetaqcd)
    hetaqcd_btag.SetName("btagEffqcd_eta")

    canvas5a = ROOT.TCanvas("canvas5a","",500,500)
    canvas5a.SetLogy()
    heta120_btag.SetMaximum(2.0)
    heta120_btag.SetMinimum(0.1)
    heta120_btag.SetMarkerColor(2)
    heta120_btag.SetMarkerSize(1)
    heta120_btag.SetMarkerStyle(21)
    heta120_btag.SetLineStyle(1)
    heta120_btag.SetLineWidth(1)
    heta120_btag.Draw("P")
     
    heta80_btag.SetMarkerColor(4)
    heta80_btag.SetMarkerSize(1)
    heta80_btag.SetMarkerStyle(22)
    heta80_btag.SetLineStyle(1)
    heta80_btag.SetLineColor(4)
    heta80_btag.SetLineWidth(1)
    heta80_btag.Draw("same")

    heta160_btag.SetMarkerColor(7)
    heta160_btag.SetMarkerSize(1)
    heta160_btag.SetMarkerStyle(25)
    heta160_btag.SetLineStyle(1)
    heta160_btag.SetLineColor(7)
    heta160_btag.SetLineWidth(1)
    heta160_btag.Draw("same")
    
    hetatt_btag.SetMarkerColor(6)
    hetatt_btag.SetMarkerSize(1)
    hetatt_btag.SetMarkerStyle(24)
    hetatt_btag.SetLineStyle(1)
    hetatt_btag.SetLineColor(6)
    hetatt_btag.SetLineWidth(1)
    hetatt_btag.Draw("same")
    
    hetaWjet_btag.SetMarkerColor(4)
    hetaWjet_btag.SetMarkerSize(1)
    hetaWjet_btag.SetMarkerStyle(22)
    hetaWjet_btag.SetLineStyle(1)
    hetaWjet_btag.SetLineColor(4)
    hetaWjet_btag.SetLineWidth(1)
#    hetaWjet_btag.Draw("same")


    hetaqcd_btag.SetMarkerColor(1)
    hetaqcd_btag.SetMarkerSize(1)
    hetaqcd_btag.SetMarkerStyle(25)
    hetaqcd_btag.SetLineStyle(1)
    hetaqcd_btag.SetLineColor(1)
    hetaqcd_btag.SetLineWidth(1)
#    hetaqcd_btag.Draw("same")
    
    heta120_btag.GetYaxis().SetTitle("B-tagging efficiency")
#    hmt.GetYaxis().SetTitleSize(20.0)
#    data_btag.GetYaxis().SetTitleOffset(1.5)
    heta120_btag.GetXaxis().SetTitle("#eta^{jet}")

    tex1 = ROOT.TLatex(0.25,0.9,"m_{H^{#pm}} = 120 GeV/c^{2}")
    tex1.SetNDC()
    tex1.SetTextSize(20)
    tex1.Draw()    
    marker1 = ROOT.TMarker(0.22,0.915,heta120_btag.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(heta120_btag.GetMarkerColor())
    marker1.SetMarkerSize(0.9*heta120_btag.GetMarkerSize())
    marker1.Draw()
    
    tex2 = ROOT.TLatex(0.25,0.85,"m_{H^{#pm}} = 80 GeV/c^{2}") 
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw()    
    marker2 = ROOT.TMarker(0.22,0.855,heta80_btag.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(heta80_btag.GetMarkerColor())
    marker2.SetMarkerSize(0.9*heta80_btag.GetMarkerSize())
    marker2.Draw()
    
    tex3 = ROOT.TLatex(0.25,0.8,"m_{H^{#pm}} = 160 GeV/c^{2}") 
    tex3.SetNDC()
    tex3.SetTextSize(20)
    tex3.Draw()    
    marker3 = ROOT.TMarker(0.22,0.815,heta160_btag.GetMarkerStyle())
    marker3.SetNDC()
    marker3.SetMarkerColor(heta160_btag.GetMarkerColor())
    marker3.SetMarkerSize(0.9*heta160_btag.GetMarkerSize())
    marker3.Draw()

    
    tex4 = ROOT.TLatex(0.25,0.75,"tt") 
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()    
    marker4 = ROOT.TMarker(0.22,0.755,hetatt_btag.GetMarkerStyle())
    marker4.SetNDC()
    marker4.SetMarkerColor(hetatt_btag.GetMarkerColor())
    marker4.SetMarkerSize(0.9*hetatt_btag.GetMarkerSize())
    marker4.Draw()

    tex7 = ROOT.TLatex(0.25,0.8,"Wjet") 
    tex7.SetNDC()
    tex7.SetTextSize(20)
#    tex7.Draw()    
    marker7 = ROOT.TMarker(0.22,0.815,hetaWjet_btag.GetMarkerStyle())
    marker7.SetNDC()
    marker7.SetMarkerColor(hetaWjet_btag.GetMarkerColor())
    marker7.SetMarkerSize(0.9*hetaWjet_btag.GetMarkerSize())
#    marker7.Draw()
    
    tex8 = ROOT.TLatex(0.25,0.75,"QCD") 
    tex8.SetNDC()
    tex8.SetTextSize(20)
#    tex8.Draw()    
    marker8 = ROOT.TMarker(0.22,0.755,hetaqcd_btag.GetMarkerStyle())
    marker8.SetNDC()
    marker8.SetMarkerColor(hetaqcd_btag.GetMarkerColor())
    marker8.SetMarkerSize(0.9*hetaqcd_btag.GetMarkerSize())
#    marker8.Draw()

    tex9 = ROOT.TLatex(0.4,0.3,"Discriminator > 3.3 ")
    tex9.SetNDC()
    tex9.SetTextSize(20)
    tex9.Draw()
    
    tex5 = ROOT.TLatex(0.2,0.95,"7 TeV                        CMS Preliminary ")
    tex5.SetNDC()
    tex5.SetTextSize(20)
    tex5.Draw()        
    canvas5a.Print("btagEff33_eta_mH.png")

#######################################################################
    #  Higgs mass comparison light jets
  
 
    heta120Q = hetaQ.histoMgr.getHisto("TTToHplusBWB_M120").getRootHisto().Clone("TTToHplusBWB_M120")
    heta120Q_btag = hetabQ.histoMgr.getHisto("TTToHplusBWB_M120").getRootHisto()
    heta120Q_btag.Divide(heta120Q)
    heta120Q_btag.SetName("btagEff120Q_eta")
    
    heta80Q = hetaQ.histoMgr.getHisto("TTToHplusBWB_M80").getRootHisto().Clone("TTToHplusBWB_M80")
    heta80Q_btag = hetabQ.histoMgr.getHisto("TTToHplusBWB_M80").getRootHisto()

    # tagged et / et 
    heta80Q_btag.Divide(heta80Q)
    heta80Q_btag.SetName("btagEff80Q_eta")

    heta160Q = hetaQ.histoMgr.getHisto("TTToHplusBWB_M160").getRootHisto().Clone("TTToHplusBWB_M160")
    heta160Q_btag = hetabQ.histoMgr.getHisto("TTToHplusBWB_M160").getRootHisto()
    # tagged et / et 
    heta160Q_btag.Divide(heta160Q)
    heta160Q_btag.SetName("btagEff160Q_eta")


    hetattQ = hetaQ.histoMgr.getHisto("TTJets").getRootHisto().Clone("TTJets")
    hetattQ_btag = hetabQ.histoMgr.getHisto("TTJets").getRootHisto()
    # tagged et / et 
    hetattQ_btag.Divide(hetattQ)
    hetattQ_btag.SetName("btagEffttQ_eta")
    
    hetawjetQ = hetaQ.histoMgr.getHisto("WJets").getRootHisto().Clone("WJets")
    hetawjetQ_btag = hetabQ.histoMgr.getHisto("WJets").getRootHisto()
    # tagged et / et 
    hetawjetQ_btag.Divide(hetawjetQ)
    hetawjetQ_btag.SetName("btagEffwjet_eta")

    hetaqcdQ = hetaQ.histoMgr.getHisto("QCD").getRootHisto().Clone("QCD")
    hetaqcdQ_btag = hetabQ.histoMgr.getHisto("QCD").getRootHisto()
    # tagged et / et 
    hetaqcdQ_btag.Divide(hetaqcdQ)
    hetaqcdQ_btag.SetName("btagEffqcd_eta")

    
    canvas5aq = ROOT.TCanvas("canvas5aq","",500,500)
    canvas5aq.SetLogy()
    heta120Q_btag.SetMinimum(0.001)
    heta120Q_btag.SetMarkerColor(2)
    heta120Q_btag.SetMarkerSize(1)
    heta120Q_btag.SetMarkerStyle(21)
    heta120Q_btag.SetLineStyle(1)
    heta120Q_btag.SetLineWidth(1)
    heta120Q_btag.Draw("P")
     
    heta80Q_btag.SetMarkerColor(4)
    heta80Q_btag.SetMarkerSize(1)
    heta80Q_btag.SetMarkerStyle(22)
    heta80Q_btag.SetLineStyle(1)
    heta80Q_btag.SetLineColor(4)
    heta80Q_btag.SetLineWidth(1)
#    heta80Q_btag.Draw("same")

    heta160Q_btag.SetMarkerColor(7)
    heta160Q_btag.SetMarkerSize(1)
    heta160Q_btag.SetMarkerStyle(25)
    heta160Q_btag.SetLineStyle(1)
    heta160Q_btag.SetLineColor(7)
    heta160Q_btag.SetLineWidth(1)
#    heta160Q_btag.Draw("same")
    
    hetattQ_btag.SetMarkerColor(6)
    hetattQ_btag.SetMarkerSize(1)
    hetattQ_btag.SetMarkerStyle(24)
    hetattQ_btag.SetLineStyle(1)
    hetattQ_btag.SetLineColor(6)
    hetattQ_btag.SetLineWidth(1)
    hetattQ_btag.Draw("same")
    
    hetawjetQ_btag.SetMarkerColor(4)
    hetawjetQ_btag.SetMarkerSize(1)
    hetawjetQ_btag.SetMarkerStyle(22)
    hetawjetQ_btag.SetLineStyle(1)
    hetawjetQ_btag.SetLineColor(4)
    hetawjetQ_btag.SetLineWidth(1)
    hetawjetQ_btag.Draw("same")

    hetaqcdQ_btag.SetMarkerColor(1)
    hetaqcdQ_btag.SetMarkerSize(1)
    hetaqcdQ_btag.SetMarkerStyle(25)
    hetaqcdQ_btag.SetLineStyle(1)
    hetaqcdQ_btag.SetLineColor(1)
    hetaqcdQ_btag.SetLineWidth(1)
    hetaqcdQ_btag.Draw("same")
    
    heta120Q_btag.GetYaxis().SetTitle("B-tagging efficiency")
#    hmt.GetYaxis().SetTitleSize(20.0)
#    data_btag.GetYaxis().SetTitleOffset(1.5)
    heta120Q_btag.GetXaxis().SetTitle("#eta^{jet}")

    tex1 = ROOT.TLatex(0.25,0.9,"m_{H^{#pm}} = 120 GeV/c^{2}")
    tex1.SetNDC()
    tex1.SetTextSize(20)
    tex1.Draw()    
    marker1 = ROOT.TMarker(0.22,0.915,heta120Q_btag.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(heta120Q_btag.GetMarkerColor())
    marker1.SetMarkerSize(0.9*heta120Q_btag.GetMarkerSize())
    marker1.Draw()
    
    tex2 = ROOT.TLatex(0.25,0.85,"m_{H^{#pm}} = 80 GeV/c^{2}") 
    tex2.SetNDC()
    tex2.SetTextSize(20)
#    tex2.Draw()    
    marker2 = ROOT.TMarker(0.22,0.855,heta80Q_btag.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(heta80Q_btag.GetMarkerColor())
    marker2.SetMarkerSize(0.9*heta80Q_btag.GetMarkerSize())
#    marker2.Draw()
    
    tex3 = ROOT.TLatex(0.25,0.8,"m_{H^{#pm}} = 160 GeV/c^{2}") 
    tex3.SetNDC()
    tex3.SetTextSize(20)
#    tex3.Draw()    
    marker3 = ROOT.TMarker(0.22,0.815,heta160Q_btag.GetMarkerStyle())
    marker3.SetNDC()
    marker3.SetMarkerColor(heta160Q_btag.GetMarkerColor())
    marker3.SetMarkerSize(0.9*heta160Q_btag.GetMarkerSize())
#    marker3.Draw()

    
    tex4 = ROOT.TLatex(0.25,0.85,"tt") 
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()    
    marker4 = ROOT.TMarker(0.22,0.855,hetattQ_btag.GetMarkerStyle())
    marker4.SetNDC()
    marker4.SetMarkerColor(hetattQ_btag.GetMarkerColor())
    marker4.SetMarkerSize(0.9*hetattQ_btag.GetMarkerSize())
    marker4.Draw()
    
    tex6 = ROOT.TLatex(0.25,0.8,"Wjets") 
    tex6.SetNDC()
    tex6.SetTextSize(20)
    tex6.Draw()    
    marker6 = ROOT.TMarker(0.22,0.815,hetawjetQ_btag.GetMarkerStyle())
    marker6.SetNDC()
    marker6.SetMarkerColor(hetawjetQ_btag.GetMarkerColor())
    marker6.SetMarkerSize(0.9*hetawjetQ_btag.GetMarkerSize())
    marker6.Draw()


    tex7 = ROOT.TLatex(0.25,0.75,"QCD") 
    tex7.SetNDC()
    tex7.SetTextSize(20)
    tex7.Draw()    
    marker7 = ROOT.TMarker(0.22,0.755,hetaqcdQ_btag.GetMarkerStyle())
    marker7.SetNDC()
    marker7.SetMarkerColor(hetaqcdQ_btag.GetMarkerColor())
    marker7.SetMarkerSize(0.9*hetaqcdQ_btag.GetMarkerSize())
    marker7.Draw()
    
    tex5 = ROOT.TLatex(0.2,0.95,"7 TeV                        CMS Preliminary ")
    tex5.SetNDC()
    tex5.SetTextSize(20)
    tex5.Draw()

    tex9 = ROOT.TLatex(0.4,0.3,"Discriminator > 3.3 ")
    tex9.SetNDC()
    tex9.SetTextSize(20)
    tex9.Draw() 
    canvas5aq.Print("QtagEff33_eta_mH.png")

#######################################################################

    canvas = ROOT.TCanvas("canvas","",500,500)
    hpt120_btag.GetYaxis().SetTitle("B-tagging efficiency")
    hpt120_btag.GetXaxis().SetTitle("p_{T}^{jet} (GeV)")
    hpt120_btag.Draw()
    histo = hpt120_btag.Clone("histo")
#    rangeMin = htopmass.GetXaxis().GetXmin()
#    rangeMax = htopmass.GetXaxis().GetXmax()
    rangeMin = 30
    rangeMax = 500

    numberOfParameters = 3

#    print "Fit range ",rangeMin, " - ",rangeMax

    class FitFunction:
        def __call__( self, x, par ):
#            return exp(par[0] + par[1]*x[0]) 
            return par[0] + par[1]*x[0] + par[2]*x[0]*x[0] 
#            return par[0] + par[1]*x[0] + par[2]*x[0]*x[0] + par[3]*x[0]*x[0]*x[0]

    theFit = TF1('theFit',FitFunction(),rangeMin,rangeMax,numberOfParameters)
    theFit.SetParLimits(0,-20000,20000)
    theFit.SetParLimits(1,-20000,20000)
    theFit.SetParLimits(2,-20000,20000)
    theFit.SetParLimits(3,-20000,20000)   
#    gStyle.SetOptFit(0)
    
    hpt120_btag.Fit(theFit,"LR")          
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
    tex5 = ROOT.TLatex(0.6,0.5,"No MET cut") 
    tex5.SetNDC()
    tex5.SetTextSize(20)
    tex5.Draw()
    print "Fit range ",rangeMin, " - ",rangeMax    
    canvas.Print("jetEtFit.png")
###########################################

    canvas4 = ROOT.TCanvas("canvas4","",500,500)
    canvas4.SetLogy()
#    hmt.SetMaximum(3.0)
    heta120_btag.SetMarkerColor(4)
    heta120_btag.SetMarkerSize(1)
    heta120_btag.SetMarkerStyle(24)
    heta120_btag.SetLineStyle(1)
    heta120_btag.SetLineColor(4)
    heta120_btag.SetLineWidth(1)
    heta120_btag.Draw("EP")

    
    heta120_btag.GetYaxis().SetTitle("B-tagging efficiency")
#    hmt.GetYaxis().SetTitleSize(20.0)
#    data_btag.GetYaxis().SetTitleOffset(1.5)
    heta120_btag.GetXaxis().SetTitle("#eta^{jet} ")   
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV                        CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()        
    canvas4.Print("btagEff_eta.png")


 
 ########################################

 
    
def printCounters(datasets):
    eventCounter = counter.EventCounter(datasets)
    eventCounter.normalizeMCByLuminosity()
    print "============================================================"
    print "Main counter (MC normalized by collision data luminosity)"
    print eventCounter.getMainCounterTable().format()

if __name__ == "__main__":
    main()
