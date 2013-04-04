#!/usr/bin/env python

######################################################################
#
# Plot QCD purity as a function of tau pt
#
# 25032013/S.Lehti
#
######################################################################

analysis = "signalAnalysisInvertedTau"

searchMode = "Light"
#searchMode = "Heavy"

#dataEra = "Run2011A"
#dataEra = "Run2011B"
dataEra = "Run2012ABCD"

HISTONAMES = []
#HISTONAMES.append("SelectedTau_pT_AfterTauID")
#HISTONAMES.append("SelectedInvertedTauAfterCuts")
#HISTONAMES.append("SelectedTau_pT_AfterMetCut")
#HISTONAMES.append("Inverted/SelectedTau_pT_AfterRtauCut")
###HISTONAMES.append("Inverted/SelectedTau_pT_AfterTauVeto")
#HISTONAMES.append("Inverted/SelectedTau_pT_AfterJetCut")
#HISTONAMES.append("Inverted/SelectedTau_pT_AfterMetCut")
#HISTONAMES.append("Inverted/SelectedTau_pT_AfterBtagging")
#HISTONAMES.append("Inverted/SelectedTau_pT_AfterBveto")
#HISTONAMES.append("Inverted/SelectedTau_pT_AfterBvetoPhiCuts")
#HISTONAMES.append("Inverted/SelectedTau_pT_AfterDeltaPhiJet1Cut")
#HISTONAMES.append("Inverted/SelectedTau_pT_AfterDeltaPhiJet12Cut")
HISTONAMES.append("Inverted/SelectedTau_pT_AfterDeltaPhiJet123Cut")
#HISTONAMES.append("Inverted/SelectedTau_pT_AfterDeltaPhiJetsAgainstTTCut")


import ROOT
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots

import sys
import array
import re

def usage():
    print
    print "### Usage:   ",sys.argv[0],"<multicrab dir>"
    print
    sys.exit()
    
def main():

    if len(sys.argv) < 2:
        usage()

    dirs = []
    dirs.append(sys.argv[1])

        
    datasets = dataset.getDatasetsFromMulticrabDirs(dirs,dataEra=dataEra, searchMode=searchMode, analysisName=analysis)
    datasets.loadLuminosities()
    datasets.updateNAllEventsToPUWeighted()

    plots.mergeRenameReorderForDataMC(datasets)

    datasets.merge("EWK", [
                    "TTJets",
                    "WJets",
                    "DYJetsToLL",
                    "SingleTop",
                    "Diboson"
                    ])
    style = tdrstyle.TDRStyle()

    plot = plots.PlotBase()

    legends = {}
    name_re = re.compile("SelectedTau_pT_(?P<name>\S+)")
    for i,histo in enumerate(HISTONAMES):
        plot.histoMgr.appendHisto(purityGraph(i,datasets,histo))
        name = histo
        match = name_re.search(histo)
        if match:
            name = match.group("name")
        #legends["Purity%s"%i] = name
        #legends["Purity%s"%i] = "#Delta#phi cuts and cut against tt+jets"
        #legends["Purity%s"%i] = "#Delta#phi(jet1, MET) cut"
        #legends["Purity%s"%i] = "After isolated #tau-jet veto"
        legends["Purity%s"%i] = "After b-jet veto"        
    plot.createFrame("purity", opts={"xmin": 40,"xmax": 300, "ymin": 0.0, "ymax": 1.1})
    plot.frame.GetXaxis().SetTitle("p_{T}^{#tau jet} (GeV/c)")
    plot.frame.GetYaxis().SetTitle("QCD purity")

    
    plot.histoMgr.setHistoLegendLabelMany(legends)
    plot.setLegend(histograms.createLegend(0.2, 0.8, 0.8, 0.95))

    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    histograms.addLuminosityText(x=None, y=None, lumi=datasets.getDataset("Data").getLuminosity())

    plot.draw()
    plot.save()
            
def purityGraph(i,datasets,histo):
    inverted = plots.DataMCPlot(datasets, histo)
    inverted.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
    
    invertedData = inverted.histoMgr.getHisto("Data").getRootHisto().Clone(histo)
    invertedEWK  = inverted.histoMgr.getHisto("EWK").getRootHisto().Clone(histo)

    numerator = invertedData.Clone()
    numerator.SetName("numerator")
    numerator.Add(invertedEWK,-1)

    denominator = invertedData.Clone()
    denominator.SetName("denominator")


    purity = ROOT.TEfficiency(numerator,denominator)
    purity.SetStatisticOption(ROOT.TEfficiency.kFNormal)

    
    purity2 = invertedData.Clone("mt")
    purity2.Add(invertedEWK,-1)
    purity2.Divide(invertedData)
    
    canvas73 = ROOT.TCanvas("canvas73","",500,500)
    purity2.SetMinimum(0)
    purity2.SetMaximum(2)
    purity2.SetMarkerColor(4)
    purity2.SetMarkerSize(1)
    purity2.SetMarkerStyle(20)
    purity2.SetFillColor(4)
    purity2.Draw("EP")
    canvas73.Print("purityTest.png")
                   
    canvas74 = ROOT.TCanvas("canvas74","",500,500)
#    invertedData.SetMinimum(0)
#    invertedData.SetMaximum(2)
    canvas74.SetLogy()
    invertedData.SetMarkerColor(4)
    invertedData.SetMarkerSize(1)
    invertedData.SetMarkerStyle(20)
    invertedData.SetFillColor(4)
    invertedData.Draw("EP")
    canvas74.Print("invertedData.png")

    canvas75 = ROOT.TCanvas("canvas75","",500,500)
#    invertedData.SetMinimum(0)
#    invertedData.SetMaximum(2)
    canvas75.SetLogy()
    invertedEWK.SetMarkerColor(4)
    invertedEWK.SetMarkerSize(1)
    invertedEWK.SetMarkerStyle(20)
    invertedEWK.SetFillColor(4)
    invertedEWK.Draw("EP")
    canvas75.Print("invertedEWK.png")

    
    collection = ROOT.TObjArray()
    collection.Add(purity)

    weights = []
    weights.append(1)

    defaults = {"drawStyle": "EP","legendStyle": "p"}

    purityGraph = ROOT.TEfficiency.Combine(collection,"",len(weights),array.array("d",weights))
    purityGraph.SetMarkerStyle(20+i)
    purityGraph.SetMarkerColor(2+i)
    
    return histograms.Histo(purityGraph, "Purity%s"%i, **defaults)
    
if __name__ == "__main__":
    main()
