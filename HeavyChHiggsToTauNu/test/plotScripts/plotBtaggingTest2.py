#!/usr/bin/env python

import ROOT,sys
ROOT.gROOT.SetBatch(True)

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
    plots.mergeWHandHH(datasets)
    print "Int.Lumi",datasets.getDataset("Data").getLuminosity()

    style = tdrstyle.TDRStyle()

    plot(datasets)
#    printCounters(datasets)

def plot(datasets):

    datasetName = "TTJets"
#    datasetName = "QCD"
    
    den_selection = "jets_p4.Pt()>30 && jets_flavour == 2"
#    den_selection = "jets_p4.Pt()>30"
    num_selection = den_selection + "&&jets_btag>3.3"

    ds = datasets.getDataset(datasetName)
    den = ds.getDatasetRootHisto(treeDraw.clone(varexp="jets_p4.Pt()>>dist1(100,0.,500.)", selection=den_selection)).getHistogram()
    num = ds.getDatasetRootHisto(treeDraw.clone(varexp="jets_p4.Pt()>>dist2(100,0.,500.)", selection=num_selection)).getHistogram()

    canvas = ROOT.TCanvas("canvas","",500,700)
    canvas.Divide(1,3)

    canvas.cd(1)
    den.Draw()

    canvas.cd(2)
    num.Draw()

    canvas.cd(3)

#    eff = ROOT.TEfficiency(num,den)
    eff = num.Clone()
    eff.Divide(den)
    eff.Draw()

    canvas.Print("canvas.C")


    plot = plots.PlotBase()
    plot.histoMgr.appendHisto(histograms.Histo(eff,eff.GetName()))
    plot.createFrame("BtaggingEff", opts={"ymin": 0.1, "ymaxfactor": 2.})

    plot.frame.GetXaxis().SetTitle("jet E_{T} (GeV)")
    plot.frame.GetYaxis().SetTitle("B-tagging eff.")

    histograms.addText(0.2, 0.8, "MC: "+datasetName, 25)
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()

    plot.draw()
    plot.save()

def printCounters(datasets):
    eventCounter = counter.EventCounter(datasets)
    eventCounter.normalizeMCByLuminosity()
    print "============================================================"
    print "Main counter (MC normalized by collision data luminosity)"
    print eventCounter.getMainCounterTable().format()

if __name__ == "__main__":
    main()
