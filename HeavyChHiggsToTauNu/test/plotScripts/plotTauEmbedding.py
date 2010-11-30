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

textDefaults.setEnergyDefaults(x=0.17)
textDefaults.setCmsPreliminaryDefaults(x=0.6)

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
        self.canvas.SaveAs(".eps")
        ROOT.gErrorIgnoreLevel = backup

def muonTau(an, q):
    rebin = 2
    xlabel = "p_{T} (GeV/c)"
    ylabel = "Number of MC events / %d.0 GeV/c" % rebin
    

    if q == "Eta":
        rebin = 1
        xlabel = "#eta"
        ylabel = "Number of MC events / 0.1"
    elif q == "Phi":
        rebin = 1
        xlabel = "#phi"
        ylabel = "Number of MC events / 0.1"

    an_name = an.replace("/", "_")
    h = Histo(datasets, [an+"/tau"+q, an+"/muon"+q])
    h.histos.forEachHisto(lambda h: h.Rebin(2))
    h.histos.setHistoLegendLabels({"muon"+q: "#mu", "tau"+q: "#tau"})
    h.createFrame(an_name+"_muonTau"+q, yfactor=1.2)
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.setLegend(createLegend(y1=0.8))
    h.draw()
    addCmsPreliminaryText()
    addEnergyText()
    h.save()

    if q == "Pt":
        h.createFrame(an_name+"_muonTau"+q+"_log", ymin=0.1, yfactor=2)
        h.frame.GetXaxis().SetTitle(xlabel)
        h.frame.GetYaxis().SetTitle(ylabel)
        h.setLegend(createLegend(y1=0.8))
        ROOT.gPad.SetLogy(True)
        h.draw()
        addCmsPreliminaryText()
        addEnergyText()
        h.save()

    xmin, ymin = 0, 0
    xmax, ymax = 200, 200
    label = "p_{T}^{%s} (GeV/c)"
    if q == "Eta":
        xmin, ymin = -2.5, -2.5
        xmax, ymax = 2.5, 2.5
        label = "#eta_{%s}"
    elif q == "Phi":
        xmin, ymin = -3.5, -3.5
        xmax, ymax = 3.5, 3.5
        label = "#phi_{%s}"

    style.setWide(True)
    h = Histo(datasets, [an+"/muonTau"+q])
    h.histos.forEachHisto(lambda h: h.Rebin2D(rebin, rebin))
    h.createFrame(an_name+"_muonTau"+q+"2D", xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax)
    h.frame.GetXaxis().SetTitle(label%"#mu")
    h.frame.GetYaxis().SetTitle(label%"#tau")
    h.histos.setHistoDrawStyleAll("COLZ")
    h.draw()
    updatePaletteStyle(h.histos.getHistoList()[0])
    addCmsPreliminaryText()
    addEnergyText()
    h.save()
    style.setWide(False)

def tauNuGen(an, q):
    rebin = 2
    xlabel = "p_{T} (GeV/c)"
    ylabel = "Number of MC events / %d.0 GeV/c" % rebin
    

    if q == "Eta":
        rebin = 1
        xlabel = "#eta"
        ylabel = "Number of MC events / 0.1"
    elif q == "Phi":
        rebin = 1
        xlabel = "#phi"
        ylabel = "Number of MC events / 0.1"

    an_name = an.replace("/", "_")

    h = Histo(datasets, [an+"/tauGen"+q, an+"/nuGen"+q])
    h.histos.forEachHisto(lambda h: h.Rebin(2))
    h.histos.setHistoLegendLabels({"tauGen"+q: "Gen #tau", "nuGen"+q: "Gen #nu_{#tau}"})
    h.createFrame(an_name+"_tauNuGen"+q, yfactor=1.2)
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.setLegend(createLegend(y1=0.8))
    h.draw()
    addCmsPreliminaryText()
    addEnergyText()
    h.save()

    xmin, ymin = 0, 0
    xmax, ymax = 200, 200
    label = "p_{T}^{%s} (GeV/c)"
    if q == "Eta":
        xmin, ymin = -2.5, -2.5
        xmax, ymax = 2.5, 2.5
        label = "#eta_{%s}"
    elif q == "Phi":
        xmin, ymin = -3.5, -3.5
        xmax, ymax = 3.5, 3.5
        label = "#phi_{%s}"

    style.setWide(True)
    h = Histo(datasets, [an+"/tauNuGen"+q])
    h.histos.forEachHisto(lambda h: h.Rebin2D(rebin, rebin))
    h.createFrame(an_name+"_tauNuGen"+q+"2D", xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax)
    h.frame.GetXaxis().SetTitle(label%"#mu")
    h.frame.GetYaxis().SetTitle(label%"#tau")
    h.histos.setHistoDrawStyleAll("COLZ")
    h.draw()
    updatePaletteStyle(h.histos.getHistoList()[0])
    addCmsPreliminaryText()
    addEnergyText()
    h.save()
    style.setWide(False)

def tauGenMass(an):
    an_name = an.replace("/", "_")

    h = Histo(datasets, [an+"/tauGenMass", an+"/tauGenDecayMass"])
    h.histos.setHistoLegendLabels({"tauGenMass": "#tau",
                                   "tauGenDecayMass": "#tau decays"})
    h.createFrame(an_name+"_tauGenMass")
    h.frame.GetXaxis().SetTitle("M (GeV/c^{2})")
    h.frame.GetYaxis().SetTitle("Number of MC events / 0.02")
    h.draw()
    addCmsPreliminaryText()
    addEnergyText()
    h.save()

def muonTauIso(an):
    an_name = an.replace("/", "_")

    style.setWide(True)
    h = Histo(datasets, [an+"/muonIsoTrkTauPtSum"])
    h.createFrame(an_name+"_muonIsoTrkTauPtSum", xmax=25, ymax=80)
    h.frame.GetXaxis().SetTitle("#mu tracker isolation #Sigma p_{T} (GeV/c)")
    h.frame.GetYaxis().SetTitle("#tau isolation charged cand #Sigma p_{T} (GeV/c)")
    h.histos.setHistoDrawStyleAll("COLZ")
    h.draw()
    addCmsPreliminaryText()
    addEnergyText()
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
    h.createFrame(an_name+"_muonIsoTauPtSumRel", xmax=0.5, ymax=10)
    h.frame.GetXaxis().SetTitle("#mu rel. iso")
    h.frame.GetYaxis().SetTitle("#tau isol. chrg cand #Sigma p_{T}/p^{#tau}_{T}")
    h.histos.setHistoDrawStyleAll("COLZ")
    h.draw()
    addCmsPreliminaryText()
    addEnergyText()
    h.save()
    style.setWide(False)


def muonTauDR(an):
    rebin = 1
    ylabel = "Number of MC events / %.2f" % (0.01*rebin)

    an_name = an.replace("/", "_")
    h = Histo(datasets, [an+"/muonTauDR"])
    h.histos.forEachHisto(lambda h: h.Rebin(rebin))
    h.createFrame(an_name+"_muonTauDR", ymin=0.1, yfactor=2, xmax=1)
    h.frame.GetXaxis().SetTitle("#DeltaR(#mu, #tau)")
    h.frame.GetYaxis().SetTitle(ylabel)
    ROOT.gPad.SetLogy(True)
    h.draw()
    addCmsPreliminaryText()
    addEnergyText()
    h.save()

    h = Histo(datasets, [an+"/muonTauLdgDR"])
    h.histos.forEachHisto(lambda h: h.Rebin(rebin))
    h.createFrame(an_name+"_muonTauLdgDR", ymin=0.1, yfactor=2, xmax=1)
    h.frame.GetXaxis().SetTitle("#DeltaR(#mu, #tau ldg cand)")
    h.frame.GetYaxis().SetTitle(ylabel)
    ROOT.gPad.SetLogy(True)
    h.draw()
    addCmsPreliminaryText()
    addEnergyText()
    h.save()

def met(an, t="Met", q=""):
    #rebin = 1
    rebin = 2
    #rebin = 5

    ylabel = "Number of MC events / %d.0 GeV" % rebin

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
    addCmsPreliminaryText()
    addEnergyText()
    h.save()

    if t == "Met" and q == "":
        h = Histo(datasets, [an+"/"+t+"OriginalAfterCut"+q])
        h.histos.forEachHisto(lambda h: h.Rebin(rebin))
        h.createFrame(an_name+"_MetOriginalAfterCut")
        h.frame.GetXaxis().SetTitle("#mu+jets "+xlabel)
        h.frame.GetYaxis().SetTitle(ylabel)
        h.draw()
        addCmsPreliminaryText()
        addEnergyText()
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
    addCmsPreliminaryText()
    addEnergyText()
    h.save()
    style.setWide(False)


def muonTauMetDeltaPhi(an, t="Met"):
    rebin = 10
    ylabel = "Number of MC events / "
    if rebin == 1:
        ylabel += "0.01"
    elif rebin == 10:
        ylabel += "0.1"
    elif rebin == 50:
        ylabel += "0.5"

    rebinMet = 5
    ylabelMet = "Number of MC events / %d.0 GeV" % rebinMet

    an_name = an.replace("/", "_")
    h = Histo(datasets, [
            #an+"/muon"+t+"DPhi",
            an+"/tau"+t+"DPhi",
            an+"/muon"+t+"OriginalDPhi",
            #an+"/tau"+t+"OriginalDPhi"
            ])
    h.histos.setHistoLegendLabels({#"muon"+t+"DPhi": "#Delta#phi(#mu, MET_{#tau})",
                                   "muon"+t+"OriginalDPhi": "#Delta#phi(#mu, MET_{#mu})",
                                   "tau"+t+"DPhi": "#Delta#phi(#tau, MET_{#tau})",
                                   #"tau"+t+"OriginalDPhi": "#Delta#phi(#tau, MET_{#mu})"
                                   })
    h.histos.forEachHisto(lambda h: h.Rebin(rebin))
    h.createFrame(an_name+"_muonTau"+t+"DeltaPhi")
    h.frame.GetXaxis().SetTitle("#Delta#phi")
    h.frame.GetYaxis().SetTitle(ylabel)
    h.setLegend(createLegend(y1=0.75))
    h.draw()
    addCmsPreliminaryText()
    addEnergyText()
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
    addCmsPreliminaryText()
    addEnergyText()
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
    addCmsPreliminaryText()
    addEnergyText()
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
    addCmsPreliminaryText()
    addEnergyText()
    h.save()
    style.setWide(False)

    numEventsAll = h.histos.getHistoList()[0].GetEntries()

    h = Histo(datasets, [
            an+"/muonTauGenNu"+t+"DPhi",
            an+"/muonGenNu"+t+"OriginalDPhi",
            ])
    h.histos.setHistoLegendLabels({"muonTauGenNu"+t+"DPhi": "#Delta#phi(#nu_{#mu}+#nu_{#tau}, MET_{#tau})",
                                   "muonGenNu"+t+"OriginalDPhi": "#Delta#phi(#nu_{#mu}, MET_{#nu})"})
    h.histos.forEachHisto(lambda h: h.Rebin(rebin))
    h.createFrame(an_name+"_muonTauGenNu"+t+"DeltaPhi")
    h.frame.GetXaxis().SetTitle("#Delta#phi")
    h.frame.GetYaxis().SetTitle(ylabel)
    h.setLegend(createLegend(x1=0.6, y1=0.8))
    h.draw()
    addCmsPreliminaryText()
    addEnergyText()
    h.save()

    numEventsGenMu = h.histos.getHistoList()[0].GetEntries()
    print "%s: N(W->munu) / N(all) = %d/%d = %.1f %%" % (an, numEventsGenMu, numEventsAll, numEventsGenMu/numEventsAll*100)
    
    style.setWide(True)
    h = Histo(datasets, [an+"/muonGenNu"+t+"OriginalMuonTauGenNu"+t+"DPhi"])
    h.histos.forEachHisto(lambda h: h.Rebin2D(rebin, rebin))
    h.createFrame(an_name+"_muonTauGenNu"+t+"DeltaPhi2D", xmin=-3.5, ymin=-3.5, xmax=3.5, ymax=3.5)
    h.frame.GetXaxis().SetTitle("#Delta#phi(#nu_{#mu}, MET_{#mu})")
    h.frame.GetYaxis().SetTitle("#Delta#phi(#nu_{#mu}+#nu_{#tau}, MET_{#tau}")
    h.histos.setHistoDrawStyleAll("COLZ")
    h.draw()
    updatePaletteStyle(h.histos.getHistoList()[0])
    addCmsPreliminaryText()
    addEnergyText()
    h.save()
    style.setWide(False)

for analysis in [
    "EmbeddingAnalyzer",
#    "tauIdEmbeddingAnalyzer",
#    "tauPtIdEmbeddingAnalyzer"
    "EmbeddingAnalyzer/matched",
#    "tauIdEmbeddingAnalyzer/matched",
#    "tauPtIdEmbeddingAnalyzer/matched"
    ]:
    for q in ["Pt", "Eta", "Phi"]:
        muonTau(analysis, q)
        tauNuGen(analysis, q)
    muonTauDR(analysis)
    muonTauIso(analysis)
    tauGenMass(analysis)

    #muonTauMetDeltaPhi(analysis, "Met")
    for t in [
        "Met",
        "GenMetTrue",
#        "GenMetCalo",
#        "GenMetCaloAndNonPrompt",
        "GenMetNu"
        ]:
        muonTauMetDeltaPhi(analysis, t)
        for q in [
            "",
#            "_x",
#            "_y"
            ]:
            met(analysis, t=t, q=q)
