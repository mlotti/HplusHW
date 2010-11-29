#!/usr/bin/env python

import os
from array import array

import ROOT
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset import *
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms import *
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle import *
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles

ROOT.gROOT.SetBatch(True)

style = TDRStyle()
style.setPalettePretty()

datasets = None
if os.path.exists("histograms.root"):
    datasets = getDatasetsFromRootFiles([("Test", "histograms.root")], counters=None)
else:
    datasets = getDatasetsFromMulticrabCfg(counters="countAnalyzer")

def getHisto(datasets, path, name, func=None):
    h = HistoSet(datasets, path)
    h = h.createHistogramObjects()[0]
    h.setName(name)
    h.setLegendLabel(name)
    if func != None:
        func(h)
    return h

class Histo:
    def __init__(self, datasets, paths):
        self.histos = HistoSetImpl([])

        for p in paths:
            name = p.split("/")[-1]
            self.histos.append(getHisto(datasets, p, name))

        self.histos.forEachHisto(styles.generator())

    def createFrame(self, plotname, **kwargs):
        (self.canvas, self.frame) = self.histos.createCanvasFrame(plotname, **kwargs)

    def setLegend(self, legend):
        self.legend = legend
        self.histos.addToLegend(legend)

    def draw(self):
        self.histos.draw()
        if hasattr(self, "legend"):
            self.legend.Draw()

    def save(self):
        backup = ROOT.gErrorIgnoreLevel
        ROOT.gErrorIgnoreLevel = ROOT.kWarning
        self.canvas.SaveAs(".png")
        ROOT.gErrorIgnoreLevel = backup

def muonTau(an, q):
    an_name = an.replace("/", "_")
    h = Histo(datasets, [an+"/tau"+q, an+"/muon"+q])
    h.histos.setHistoLegendLabels({"muon"+q: "#mu", "tau"+q: "#tau"})
    h.createFrame(an_name+"_muonTau"+q)
    h.frame.GetXaxis().SetTitle("p_{T} (GeV/c)")
    h.frame.GetYaxis().SetTitle("# entries / 1.0 GeV/c")
    h.setLegend(createLegend(y1=0.8))
    h.draw()
    h.save()

def muonTauIso(an):
    an_name = an.replace("/", "_")

    style.setWide(True)
    h = Histo(datasets, [an+"/muonIsoTrkTauPtSum"])
    h.createFrame(an_name+"_muonIsoTrkTauPtSum", xmax=30, ymax=100)
    h.frame.GetXaxis().SetTitle("#mu tracker isolation #Sigma p_{T} (GeV/c)")
    h.frame.GetYaxis().SetTitle("#tau isolation charged cand #Sigma p_{T} (GeV/c)")
    h.histos.setHistoDrawStyleAll("COLZ")
    h.draw()
    h.save()
    style.setWide(False)

    #style.setWide(True)
    #h = Histo(datasets, [an+"/muonIsoTrkTauPtSumRel"])
    #h.createFrame(an_name+"_muonIsoTrkTauPtSumRel")
    #h.frame.GetXaxis().SetTitle("#mu trk isol. #Sigma p_{T}/p^{#mu}_{T}")
    #h.frame.GetYaxis().SetTitle("#tau isol. chrg cand #Sigma p_{T}/p^{#tau}_{T}")
    #h.histos.setHistoDrawStyleAll("COLZ")
    #h.draw()
    #h.save()
    #style.setWide(False)

    style.setWide(True)
    h = Histo(datasets, [an+"/muonIsoTauPtSumRel"])
    h.createFrame(an_name+"_muonIsoTauPtSumRel", xmax=0.5, ymax=20)
    h.frame.GetXaxis().SetTitle("#mu rel. iso")
    h.frame.GetYaxis().SetTitle("#tau isol. chrg cand #Sigma p_{T}/p^{#tau}_{T}")
    h.histos.setHistoDrawStyleAll("COLZ")
    h.draw()
    h.save()
    style.setWide(False)


def muonTauDR(an):
    rebin = 1
    ylabel = "Number of events / %.2f" % (0.01*rebin)

    an_name = an.replace("/", "_")
    h = Histo(datasets, [an+"/muonTauDR"])
    h.histos.forEachHisto(lambda h: h.Rebin(rebin))
    h.createFrame(an_name+"_muonTauDR", ymin=0.1, yfactor=2, xmax=1)
    h.frame.GetXaxis().SetTitle("#DeltaR(#mu, #tau)")
    h.frame.GetYaxis().SetTitle(ylabel)
    ROOT.gPad.SetLogy(True)
    h.draw()
    h.save()

    h = Histo(datasets, [an+"/muonTauLdgDR"])
    h.histos.forEachHisto(lambda h: h.Rebin(rebin))
    h.createFrame(an_name+"_muonTauLdgDR", ymin=0.1, yfactor=2, xmax=1)
    h.frame.GetXaxis().SetTitle("#DeltaR(#mu, #tau ldg cand)")
    h.frame.GetYaxis().SetTitle(ylabel)
    ROOT.gPad.SetLogy(True)
    h.draw()
    h.save()

def met(an, t="Met", q=""):
    #rebin = 1
    rebin = 2
    #rebin = 5

    ylabel = "Number of events / %d.0 GeV" % rebin

    xlabel = "MET (GeV)"
    if q == "_x":
        xlabel = "MET_{x} (GeV)"
    elif q == "_y":
        xlabel = "MET_{y} (GeV)"

    an_name = an.replace("/", "_")

    h = Histo(datasets, [an+"/"+t+q, an+"/"+t+"Original"+q])
    h.histos.forEachHisto(lambda h: h.Rebin(rebin))
    h.histos.setHistoLegendLabels({t+q: "Embedded", t+"Original"+q: "Original"})
    h.createFrame(an_name+"_"+t+q)
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.setLegend(createLegend(y1=0.8))
    h.draw()
    h.save()

    if t == "Met" and q == "":
        h = Histo(datasets, [an+"/"+t+"OriginalAfterCut"+q])
        h.histos.forEachHisto(lambda h: h.Rebin(rebin))
        h.createFrame(an_name+"_MetOriginalAfterCut")
        h.frame.GetXaxis().SetTitle("#mu+jets "+xlabel)
        h.frame.GetYaxis().SetTitle(ylabel)
        h.draw()
        h.save()
    
    ymin=0
    ymax=200
    xmin=0
    xmax=200

    if q in ["_x", "_y"]:
        ymin = -ymax/2
        ymax = ymax/2
        xmin = -xmax/2
        xmax = xmax/2

    line = ROOT.TGraph(2, array("d", [xmin, xmax]), array("d", [ymin, ymax]))
    line.SetLineStyle(2)
    line.SetLineWidth(2)

    style.setWide(True)
    h = Histo(datasets, [an+"/"+t+"Met"+q])
    h.histos.forEachHisto(lambda h: h.Rebin2D(rebin, rebin))
    h.createFrame(an_name+"_"+t+"Met"+q, xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)
    h.frame.GetXaxis().SetTitle("Original "+xlabel)
    h.frame.GetYaxis().SetTitle("Embedded "+xlabel)
    h.histos.setHistoDrawStyleAll("COLZ")
    h.draw()
    line.Draw("L")
    updatePaletteStyle(h.histos.getHistoList()[0])
    h.save()
    style.setWide(False)


def muonTauMetDeltaPhi(an, t="Met"):
    rebin = 10
    ylabel = "# entries / "
    if rebin == 1:
        ylabel += "0.01"
    elif rebin == 10:
        ylabel += "0.1"

    rebinMet = 5
    ylabelMet = "#entries / %d.0 GeV" % rebinMet

    an_name = an.replace("/", "_")
    h = Histo(datasets, [an+"/muon"+t+"DPhi", an+"/muon"+t+"OriginalDPhi",
                         an+"/tau"+t+"DPhi", an+"/tau"+t+"OriginalDPhi"])
    h.histos.setHistoLegendLabels({"muon"+t+"DPhi": "#Delta#Phi(#mu, MET_{#tau})",
                                   "muon"+t+"OriginalDPhi": "#Delta#Phi(#mu, MET_{#mu})",
                                   "tau"+t+"DPhi": "#Delta#Phi(#tau, MET_{#tau})",
                                   "tau"+t+"OriginalDPhi": "#Delta#Phi(#tau, MET_{#mu})"})
    h.histos.forEachHisto(lambda h: h.Rebin(rebin))
    h.createFrame(an_name+"_muonTau"+t+"DeltaPhi")
    h.frame.GetXaxis().SetTitle("#Delta#phi")
    h.frame.GetYaxis().SetTitle(ylabel)
    h.setLegend(createLegend(y1=0.75))
    h.draw()
    h.save()

    style.setWide(True)
    h = Histo(datasets, [an+"/muon"+t+"OriginalTau"+t+"DPhi"])
    h.histos.forEachHisto(lambda h: h.Rebin2D(rebin, rebin))
    h.createFrame(an_name+"_muonTau"+t+"DeltaPhi2D", xmin=-3.5, ymin=-3.5, xmax=3.5, ymax=3.5)
    h.frame.GetXaxis().SetTitle("#Delta#phi(#mu, MET_{#mu})")
    h.frame.GetYaxis().SetTitle("#Delta#phi(#tau, MET_{#tau})")
    h.histos.setHistoDrawStyleAll("COLZ")
    h.draw()
    updatePaletteStyle(h.histos.getHistoList()[0])
    h.save()
    style.setWide(False)

    #style.setOptStat(1)
    h = Histo(datasets, [an+"/"+t+"OriginalDiff"])
    h.histos.forEachHisto(lambda h: h.Rebin(rebinMet))
    h.histos.forEachHisto(lambda h: h.SetStats(True))
    h.createFrame(an_name+"_"+t+"OriginalDiff", xmin=-100, xmax=200)
    h.frame.GetXaxis().SetTitle("MET_{#tau}-MET_{#mu} (GeV)")
    h.frame.GetYaxis().SetTitle(ylabelMet)
    h.draw()
    #ROOT.gPad.Update()
    #box = h.histos.getHistoList()[0].FindObject("stats")
    #box.SetOptStat("em")
    #box.SetX1NDC(0.8)
    #box.SetX2NDC(0.92)
    #box.SetY1NDC(0.8)
    #box.SetY2NDC(0.92)
    #box.Draw()
    h.save()
    #style.setOptStat(0)

    style.setWide(True)
    h = Histo(datasets, [an+"/muon"+t+"OriginalDPhi"+t+"OriginalDiff"])
    h.histos.forEachHisto(lambda h: h.Rebin2D(rebin, rebinMet))
    h.createFrame(an_name+"_muon"+t+"DeltaPhi"+t+"Diff", xmin=-3.5, ymin=-100, xmax=3.5, ymax=200)
    h.frame.GetXaxis().SetTitle("#Delta#phi(#mu, MET_{#mu})")
    h.frame.GetYaxis().SetTitle("MET_{#tau}-MET_{#mu}")
    h.histos.setHistoDrawStyleAll("COLZ")
    h.draw()
    updatePaletteStyle(h.histos.getHistoList()[0])
    h.save()
    style.setWide(False)



for analysis in [
    "EmbeddingAnalyzer",
#    "tauIdEmbeddingAnalyzer",
#    "tauPtIdEmbeddingAnalyzer"
#    "EmbeddingAnalyzer/matched",
#    "tauIdEmbeddingAnalyzer/matched",
    "tauPtIdEmbeddingAnalyzer/matched"
    ]:
    for q in ["Pt", "Eta", "Phi"]:
        muonTau(analysis, q)
    muonTauDR(analysis)
    muonTauIso(analysis)

    #muonTauMetDeltaPhi(analysis, "Met")
    for t in [
        "Met",
#        "GenMetTrue",
#        "GenMetCalo",
#        "GenMetCaloAndNonPrompt",
#        "GenMetNu"
        ]:
        muonTauMetDeltaPhi(analysis, t)
        for q in [
            "",
#            "_x",
#            "_y"
            ]:
            met(analysis, t=t, q=q)
