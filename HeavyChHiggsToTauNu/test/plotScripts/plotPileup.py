#!/usr/bin/env python

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles



def main():
    datasets = dataset.getDatasetsFromMulticrabCfg(weightedCounters=False)
    datasets.loadLuminosities()

    #mc = "WJets"
    mc = "QCD"
    data = "2010"
    #data = "2011"

#    maxVtx = 15
    maxVtx = 20

    if data == "2010":
        datasets.remove(filter(lambda name: "Prompt" in name, datasets.getAllDatasetNames()))
    elif data == "2011":
        datasets.remove(filter(lambda name: "Dec22" in name, datasets.getAllDatasetNames()))

    plots.mergeRenameReorderForDataMC(datasets)

    style = tdrstyle.TDRStyle()

    if mc == "QCD":
        datasets.remove(["WJets"])
    elif mc == "WJets":
        datasets.remove(["QCD"])
    
    h = histograms.HistoManager(datasets, "signalAnalysis/verticesBeforeWeight")
    h.normalizeToOne()

    h.forEachMCHisto(styles.generator())
    h.forHisto("Data", styles.getDataStyle())
    h.setHistoDrawStyle("Data", "EP")
    h.setHistoLegendStyle("Data", "p")

    cf = histograms.CanvasFrame(h, "vertex_%s_%s" % (data, mc), xmax=maxVtx)
    cf.frame.GetXaxis().SetTitle("N(vtx)")
    cf.frame.GetYaxis().SetTitle("A.u.")

    legend = histograms.createLegend()
    h.addToLegend(legend)
    h.draw()
    legend.Draw()

    cf.canvas.SaveAs(".png")
    cf.canvas.SaveAs(".eps")
    cf.canvas.SaveAs(".C")

    # Weight

    dataHisto = h.getHisto("Data").getRootHisto()
    mcHisto = h.getHisto(mc).getRootHisto()

    # For normalization, see https://twiki.cern.ch/twiki/bin/view/CMS/PileupReweighting
    weightHisto = dataHisto.Clone("weights")
    weightHisto.Divide(mcHisto)
    print "Weight histo integral", weightHisto.Integral()
    #weightHisto.Scale(1/dataHisto.Integral())
    #weightHisto.Scale(1/weightHisto.Integral())
    print "Weight histo integral", weightHisto.Integral()
    print "Sum of [weight*prob]", sum([weightHisto.GetBinContent(bin)*mcHisto.GetBinContent(bin) for bin in xrange(1, weightHisto.GetNbinsX())])

    print "weights = cms.vdouble(%s)" % ", ".join(["%.8f" % weightHisto.GetBinContent(bin) for bin in xrange(1, min(maxVtx, weightHisto.GetNbinsX())+1)])

    h = histograms.HistoManager(datasetRootHistos=[])
    h.appendHisto(histograms.Histo(weightHisto, "Weight", "", "HIST"))
    h.forEachHisto(styles.generator())

    cf = histograms.CanvasFrame(h, "vertex_weight_%s_%s" % (data, mc), xmax=maxVtx)
    cf.frame.GetXaxis().SetTitle("N(vtx)")
    cf.frame.GetYaxis().SetTitle("Weight")

    h.draw()

    cf.canvas.SaveAs(".png")
    cf.canvas.SaveAs(".eps")
    cf.canvas.SaveAs(".C")


if __name__ == "__main__":
    main()
