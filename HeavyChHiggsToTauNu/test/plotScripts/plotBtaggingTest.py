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
    metCut = "met_p4.Et() > 50"
    tauPtCut = "tau_p4.Pt() > 40"
    jetNumCut = "Sum$(jets_p4.Pt() > 30) >= 3"
    tauLeadingCandPtCut = "tau_leadPFChargedHadrCand_p4.Pt() > 20"
    rtauCut = "tau_leadPFChargedHadrCand_p4.P()/tau_p4.P() > 0.7"
    btag = "jets_btag > 1.7"
    deltaPhiCut = "acos((tau_p4.Px()*met_p4.Px()+tau_p4.Py()*met_p4.Py())/tau_p4.Pt()/met_p4.Et())*57.2958 < 160"
    
    tauSelCut = "tau_p4.Pt() > 40 && tau_leadPFChargedHadrCand_p4.Pt() > 20 && tau_leadPFChargedHadrCand_p4.P()/tau_p4.P() > 0.7"
    tauJetsCut = "tau_p4.Pt() > 40 && tau_leadPFChargedHadrCand_p4.Pt() > 20 && tau_leadPFChargedHadrCand_p4.P()/tau_p4.P() > 0.7 && Sum$(jets_p4.Pt() > 30) >= 3 "
    tauJetsMetCut = "tau_p4.Pt() > 40 && tau_leadPFChargedHadrCand_p4.Pt() > 20 && tau_leadPFChargedHadrCand_p4.P()/tau_p4.P() > 0.7 && Sum$(jets_p4.Pt() > 30) >= 3 && met_p4.Et() > 50"

 
    noTagging = jetNumCut + "&&abs(jets_flavour)==5"    
    btagging = noTagging + "&&jets_btag > 1.7"
    noTaggingLight = jetNumCut + "&&abs(jets_flavour) < 4"    
    btaggingLight = noTaggingLight + "&&jets_btag > 1.7" 
    noTaggingMet = jetNumCut + "&&met_p4.Et() > 50" + "&&abs(jets_flavour)==5"    
    btaggingMet = noTaggingMet + "&&jets_btag > 1.7" 




    
    ###########################################
    
    hpt = plots.DataMCPlot(datasets, treeDraw.clone(varexp="jets_p4.Et()>>dist(25,0,500)", selection=noTagging))
    
    hptt = hpt.histoMgr.getHisto("TTJets").getRootHisto().Clone("TTJets")
#    hptt = hpt.histoMgr.getHisto("TTToHplusBWB_M120").getRootHisto().Clone("TTToHplusBWB_M120")
   # hptt_btag = hptb.histoMgr.getHisto("TTJets").getRootHisto()
    
    hpt.stackMCHistograms()
#    hpt.addMCUncertainty()

# jet Et 
    hpt.createFrameFraction("jetEt", opts={"ymin": 0.0001, "ymaxfactor": 1.1}, opts2={"ymin": 0.01, "ymax": 1.5})
    hpt.setLegend(histograms.createLegend())
    hpt.getPad().SetLogy(True)
    hpt.frame.GetXaxis().SetTitle("Et jet")
    hpt.frame.GetYaxis().SetTitle("Events /%.0f GeV/c" % hpt.binWidth())
    hpt.draw()    
    histograms.addCmsPreliminaryText() 
    histograms.addEnergyText()
    hpt.addLuminosityText()          
    hpt.save()


# jet Et with b tagging
    hptb = plots.DataMCPlot(datasets, treeDraw.clone(varexp="jets_p4.Et()>>dist(25,0,500)", selection=btagging))
    hptb.stackMCHistograms()
    
    hptb.createFrameFraction("jetEt_btag", opts={"ymin": 0.0001, "ymaxfactor": 1.1}, opts2={"ymin": 0.01, "ymax": 1.5})
    hptb.setLegend(histograms.createLegend())
    hptb.getPad().SetLogy(True)
    hptb.frame.GetXaxis().SetTitle("Et jet btag")
    hptb.frame.GetYaxis().SetTitle("Events /%.0f GeV/c" % hptb.binWidth())
    hptb.draw()    
    histograms.addCmsPreliminaryText() 
    histograms.addEnergyText()
    hptb.addLuminosityText()          
    hptb.save()

##################################################
    #  MET cut comparison 
  # Clone the data one
    hpt120 = hpt.histoMgr.getHisto("TTToHplusBWB_M120").getRootHisto().Clone("TTToHplusBWB_M120")
    hpt120_btag = hptb.histoMgr.getHisto("TTToHplusBWB_M120").getRootHisto()

#    hptt = hpt.histoMgr.getHisto("TTJets_TuneZ2_Summer11").getRootHisto().Clone("TTJets_TuneZ2_Summer11")
#    hptt_btag = hptb.histoMgr.getHisto("TTJets_TuneZ2_Summer11").getRootHisto()
#    hptt = hpt.histoMgr.getHisto("TTToHplusBWB_M120").getRootHisto().Clone("TTToHplusBWB_M120")
#    hptt_btag = hptb.histoMgr.getHisto("TTToHplusBWB_M120").getRootHisto()

    
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
    #  Higgs mass comparison 
  
 
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


#    hpttt = hpt.histoMgr.getHisto("TTJets").getRootHisto().Clone("TTJets")
#    hpttt = hpt.histoMgr.getHisto("TTJets").getRootHisto()
    
    hpttt_btag = hptb.histoMgr.getHisto("TTJets").getRootHisto()
#    hpttt = hpt.histoMgr.getHisto("TTToHplusBWB_M160").getRootHisto().Clone("TTToHplusBWB_M160")
#    hpttt_btag = hptb.histoMgr.getHisto("TTToHplusBWB_M160").getRootHisto()
    # tagged et / et 
    hpttt_btag.Divide(hpttt)
    hpttt_btag.SetName("btagEfftt_pt")

    canvas5 = ROOT.TCanvas("canvas5","",500,500)
    canvas5.SetLogy()
    hpt120_btag.SetMaximum(1.5)
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

    tex1 = ROOT.TLatex(0.25,0.8,"m_{H^{#pm}} = 120 GeV/c^{2}")
    tex1.SetNDC()
    tex1.SetTextSize(20)
    tex1.Draw()    
    marker1 = ROOT.TMarker(0.22,0.815,hpt120_btag.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(hpt120_btag.GetMarkerColor())
    marker1.SetMarkerSize(0.9*hpt120_btag.GetMarkerSize())
    marker1.Draw()
    
    tex2 = ROOT.TLatex(0.25,0.75,"m_{H^{#pm}} = 80 GeV/c^{2}") 
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw()    
    marker2 = ROOT.TMarker(0.22,0.755,hpt80_btag.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(hpt80_btag.GetMarkerColor())
    marker2.SetMarkerSize(0.9*hpt80_btag.GetMarkerSize())
    marker2.Draw()
    
    tex3 = ROOT.TLatex(0.25,0.7,"m_{H^{#pm}} = 160 GeV/c^{2}") 
    tex3.SetNDC()
    tex3.SetTextSize(20)
    tex3.Draw()    
    marker3 = ROOT.TMarker(0.22,0.715,hpt160_btag.GetMarkerStyle())
    marker3.SetNDC()
    marker3.SetMarkerColor(hpt160_btag.GetMarkerColor())
    marker3.SetMarkerSize(0.9*hpt160_btag.GetMarkerSize())
    marker3.Draw()

    
    tex4 = ROOT.TLatex(0.25,0.65,"tt") 
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()    
    marker4 = ROOT.TMarker(0.22,0.655,hpttt_btag.GetMarkerStyle())
    marker4.SetNDC()
    marker4.SetMarkerColor(hpttt_btag.GetMarkerColor())
    marker4.SetMarkerSize(0.9*hpttt_btag.GetMarkerSize())
    marker4.Draw()

    
    tex5 = ROOT.TLatex(0.2,0.95,"7 TeV                        CMS Preliminary ")
    tex5.SetNDC()
    tex5.SetTextSize(20)
    tex5.Draw()        
    canvas5.Print("btagEff_pt_mH.png")

#######################################################################

#    canvas = ROOT.TCanvas("canvas","",500,500)
#    hpt120_btag.GetYaxis().SetTitle("B-tagging efficiency")
#    hpt120_btag.GetXaxis().SetTitle("p_{T}^{jet} (GeV)")
#    hpt120_btag.Draw()
#    histo = hpt120_btag.Clone("histo")
##    rangeMin = htopmass.GetXaxis().GetXmin()
##    rangeMax = htopmass.GetXaxis().GetXmax()
#    rangeMin = 30
#    rangeMax = 500

#    numberOfParameters = 3

#    print "Fit range ",rangeMin, " - ",rangeMax

#    class FitFunction:
#        def __call__( self, x, par ):
##            return exp(par[0] + par[1]*x[0]) 
#            return par[0] + par[1]*x[0] + par[2]*x[0]*x[0] 
##            return par[0] + par[1]*x[0] + par[2]*x[0]*x[0] + par[3]*x[0]*x[0]*x[0]

#    theFit = TF1('theFit',FitFunction(),rangeMin,rangeMax,numberOfParameters)
#    theFit.SetParLimits(0,-20000,20000)
#    theFit.SetParLimits(1,-20000,20000)
#    theFit.SetParLimits(2,-20000,20000)
#    theFit.SetParLimits(3,-20000,20000)   
##    gStyle.SetOptFit(0)
    
#    data_btag.Fit(theFit,"LR")          
#    theFit.SetRange(rangeMin,rangeMax)
#    theFit.SetLineStyle(1)
#    theFit.SetLineWidth(2)  
#    theFit.Draw("same")
#    tex4 = ROOT.TLatex(0.2,0.95,"CMS Preliminary ")
#    tex4.SetNDC()
#    tex4.SetTextSize(20)
#    tex4.Draw()
#    tex2 = ROOT.TLatex(0.6,0.7,"tt->tbH^{#pm}") 
#    tex2.SetNDC()
#    tex2.SetTextSize(20)
#    tex2.Draw()
#    tex3 = ROOT.TLatex(0.6,0.6,"m_{H^{#pm}} = 120 GeV/c^{2}") 
#    tex3.SetNDC()
#    tex3.SetTextSize(20)
#    tex3.Draw()
#    tex5 = ROOT.TLatex(0.6,0.5,"No MET cut") 
#    tex5.SetNDC()
#    tex5.SetTextSize(20)
#    tex5.Draw()
#    print "Fit range ",rangeMin, " - ",rangeMax    
#    canvas.Print("jetEtFit.png")

    

########################################################

    
# plot discriminator                              
    histo3 = plots.DataMCPlot(datasets, treeDraw.clone(varexp="jets_btag>>dist(50,-20,20)", selection=noTagging)) 
    #    histo2.histoMgr.forEachHisto(lambda histo: histo.getRootHisto().Rebin(10))
    
    histo3.stackMCHistograms()
    
    histo3.createFrameFraction("b-discriminator", opts={"ymin": 0.0001, "ymaxfactor": 1.1}, opts2={"ymin": 0.01, "ymax": 1.5})
    histo3.setLegend(histograms.createLegend())
    histo3.getPad().SetLogy(True)
    histo3.frame.GetXaxis().SetTitle("b discriminator")
    histo3.frame.GetYaxis().SetTitle("Events")
    histo3.draw()
    histograms.addCmsPreliminaryText() 
    histograms.addEnergyText()
    histo3.addLuminosityText()          
    histo3.save()




    heta = plots.DataMCPlot(datasets, treeDraw.clone(varexp="jets_p4.Eta()>>dist(30,-3,3)", selection=noTagging))
    #    histo2.histoMgr.forEachHisto(lambda histo: histo.getRootHisto().Rebin(10))
    
    heta.stackMCHistograms()
    
    heta.createFrameFraction("jetEta", opts={"ymin": 0.01, "ymaxfactor": 2.0}, opts2={"ymin": 0.01, "ymax": 1.5})
    heta.setLegend(histograms.createLegend())
    heta.getPad().SetLogy(True)
    heta.frame.GetXaxis().SetTitle("#eta^{jet}")
    heta.frame.GetYaxis().SetTitle("Events")
    heta.draw()
    histograms.addCmsPreliminaryText() 
    histograms.addEnergyText()
    heta.addLuminosityText()          
    heta.save()



    hetab = plots.DataMCPlot(datasets, treeDraw.clone(varexp="jets_p4.Eta()>>dist(30,-3,3)", selection=btagging))
    #    histo2.histoMgr.forEachHisto(lambda histo: histo.getRootHisto().Rebin(10))
    
    hetab.stackMCHistograms()
    
    hetab.createFrameFraction("jetEta_btag", opts={"ymin": 0.01, "ymaxfactor": 2.0}, opts2={"ymin": 0.01, "ymax": 1.5})
    hetab.setLegend(histograms.createLegend())
    hetab.getPad().SetLogy(True)
    hetab.frame.GetXaxis().SetTitle("#eta^{b tagged jet}")
    hetab.frame.GetYaxis().SetTitle("Events")
    hetab.draw()
    histograms.addCmsPreliminaryText() 
    histograms.addEnergyText()
    hetab.addLuminosityText()          
    hetab.save()





##################################################
    #  Higgs mass comparison 
  
 
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

    canvas5a = ROOT.TCanvas("canvas5a","",500,500)
    canvas5a.SetLogy()
    heta120_btag.SetMaximum(1.5)
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
    
    heta120_btag.GetYaxis().SetTitle("B-tagging efficiency")
#    hmt.GetYaxis().SetTitleSize(20.0)
#    data_btag.GetYaxis().SetTitleOffset(1.5)
    heta120_btag.GetXaxis().SetTitle("E_{T}^{jet} (GeV)")

    tex1 = ROOT.TLatex(0.25,0.8,"m_{H^{#pm}} = 120 GeV/c^{2}")
    tex1.SetNDC()
    tex1.SetTextSize(20)
    tex1.Draw()    
    marker1 = ROOT.TMarker(0.22,0.815,heta120_btag.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(heta120_btag.GetMarkerColor())
    marker1.SetMarkerSize(0.9*heta120_btag.GetMarkerSize())
    marker1.Draw()
    
    tex2 = ROOT.TLatex(0.25,0.75,"m_{H^{#pm}} = 80 GeV/c^{2}") 
    tex2.SetNDC()
    tex2.SetTextSize(20)
    tex2.Draw()    
    marker2 = ROOT.TMarker(0.22,0.755,heta80_btag.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(heta80_btag.GetMarkerColor())
    marker2.SetMarkerSize(0.9*heta80_btag.GetMarkerSize())
    marker2.Draw()
    
    tex3 = ROOT.TLatex(0.25,0.7,"m_{H^{#pm}} = 160 GeV/c^{2}") 
    tex3.SetNDC()
    tex3.SetTextSize(20)
    tex3.Draw()    
    marker3 = ROOT.TMarker(0.22,0.715,heta160_btag.GetMarkerStyle())
    marker3.SetNDC()
    marker3.SetMarkerColor(heta160_btag.GetMarkerColor())
    marker3.SetMarkerSize(0.9*heta160_btag.GetMarkerSize())
    marker3.Draw()

    
    tex4 = ROOT.TLatex(0.25,0.65,"tt") 
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()    
    marker4 = ROOT.TMarker(0.22,0.655,hetatt_btag.GetMarkerStyle())
    marker4.SetNDC()
    marker4.SetMarkerColor(hetatt_btag.GetMarkerColor())
    marker4.SetMarkerSize(0.9*hetatt_btag.GetMarkerSize())
    marker4.Draw()

    
    tex5 = ROOT.TLatex(0.2,0.95,"7 TeV                        CMS Preliminary ")
    tex5.SetNDC()
    tex5.SetTextSize(20)
    tex5.Draw()        
    canvas5a.Print("btagEff_eta_mH.png")

#######################################################################



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
