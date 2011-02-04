#!/usr/bin/env python

import ROOT
ROOT.gROOT.SetBatch(True)

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset import *
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms import *
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter import *
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle import *
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles

#prefix = "noIsoNoVetoMetNJets3"
#prefix = "noIsoNoVetoMetPFPt30Met20NJets3JetId"
#prefix = "noMuonNJets3"
#prefix = "topMuJetRefMet"
#prefix = "muonLastNJets3JetId"
prefix = "muonJetMetAnalyzer/"
#prefix = "muonJetMetAnalyzerJetId/"

topMuJetRefMet = [prefix+x for x in [
        "h00_AllMuons",
        "h01_Triggered",
        "h02_PrimaryVertex",
        "h03_GlobalTrackerMuon",
        "h04_MuonKin",
        "h05_MuonJetDR",
        "h06_MuonQuality",
        "h07_MuonIP",
        "h08_MuonIsolation",
        "h09_MuonVertexDiff",
        "h10_MuonVeto",
        "h11_ElectronVeto",
        "h12_JetMultiplicityCut",
        "h13_METCut"]]
topMuJetRefMetAoc = []

noIsoNoVetoMet = [prefix+x for x in [
        "h00_AllMuons",
        "h01_Triggered",
        "h02_PrimaryVertex",
        "h03_GlobalTrackerMuon",
        "h04_MuonKin",
        "h05_MuonJetDR",
        "h06_MuonQuality",
        "h07_MuonIP",
        "h08_MuonVertexDiff",
        "h09_JetMultiplicityCut",
        "h10_METCut"]]
noIsoNoVetoMetAoc = [prefix+"Aoc"+x+"AfterOtherCuts" for x in [
        "h07_MuonLargestPt",
        "h08_JetMultiplicityCut",
        "h09_METCut"]]

noIsoNoVetoMetPF = [prefix+x for x in [
        "h00_AllMuons",
        "h01_Triggered",
        "h02_PrimaryVertex",
        "h03_GlobalTrackerMuon",
        "h04_MuonKin",
        "h05_MuonQuality",
        "h06_MuonIP",
        "h07_MuonVertexDiff",
        "h08_JetMultiplicityCut",
        "h09_METCut"]]
noIsoNoVetoMetPFAoc = [prefix+"Aoc"+x+"AfterOtherCuts" for x in [
        "h06_MuonLargestPt",
        "h07_JetMultiplicityCut",
        "h08_METCut"]]

noMuon = [prefix+x for x in [
        "h00_AllMuons",
        "h01_Triggered",
        "h02_PrimaryVertex",
        "h03_JetMultiplicityCut",
        "h04_METCut"]]
noMuonAoc = []

muonLast = [prefix+x for x in [
        "h00_AllMuons",
        "h01_Triggered",
        "h02_PrimaryVertex",
        "h03_JetMultiplicityCut",
        "h04_MuonJetDR",
        "h05_GlobalTrackerMuon",
        #"h06_MuonKin",
        "h06_MuonEta",
        "h07_MuonPt5",
        "h08_MuonPt10",
        "h09_MuonPt15",
        "h10_MuonPt20",
        "h11_MuonPt25",
        "h12_MuonPt30",
        "h13_MuonPt35",
        "h14_MuonPt40",
        "h15_MuonQuality",
        "h16_MuonIP",
        "h17_MuonVertexDiff",
        "h18_MuonIsolation050",
        "h19_MuonIsolation015",
        "h20_MuonIsolation010",
        "h21_MuonIsolation005",
        "h22_MuonVeto",
        "h23_ElectronVeto"]]
muonLastAoc = []

muonJetMet = [prefix+x for x in [
        "h00_All",
        "h01_JetKinematic", 
        "h02_MuonTight",
        "h03_MuonEta",
        "h04_MuonPt5",
        "h05_MuonPt10",
        "h06_MuonPt15",
        "h07_MuonPt20",
        "h08_MuonPt25",
        "h09_MuonPt30",
        "h10_MuonPt35",
        "h11_MuonPt40"]]
muonJetMetJetId = [prefix+x for x in [
        "h00_All",
        "h01_JetKinematic", 
        "h02_JetId",
        "h03_MuonTight",
        "h04_MuonEta",
        "h05_MuonPt5",
        "h06_MuonPt10",
        "h07_MuonPt15",
        "h07_MuonPt20",
        "h08_MuonPt25",
        "h09_MuonPt30",
        "h10_MuonPt35",
        "h11_MuonPt40"]]
muonJetMetAoc = []
        

selections = noIsoNoVetoMet
selectionsAoc = noIsoNoVetoMetAoc
if "noIsoNoVetoMetPF" in prefix:
    selections = noIsoNoVetoMetPF
    selectionsAoc = noIsoNoVetoMetPFAoc
elif "noMuon" in prefix:
    selections = noMuon
    selectionsAoc = noMuonAoc
elif "topMuJetRefMet" in prefix:
    selections = topMuJetRefMet
    selectionsAoc = topMuJetRefMetAoc
elif "muonLast" in prefix:
    selections = muonLast
    selectionsAco = muonLastAoc
elif "muonJetMet" in prefix:
    if "JetId" in prefix:
        selections = muonJetMetJetId
    else:
        selections = muonJetMet
    selectionsAco = muonJetMetAoc


datasets = getDatasetsFromMulticrabCfg(counters=None)
#datasets.getDataset("Mu_135821-144114").setLuminosity(3051760.115/1e6) # ub^-1 -> pb^-1
#datasets.getDataset("Mu_146240-147116").setLuminosity(4390660.197/1e6)
#datasets.getDataset("Mu_147196-149442").setLuminosity(27384630.974/1e6)

#datasets.getDataset("Mu_135821-144114").setLuminosity(2863224.758/1e6) # ub^-1 -> pb^-1
datasets.getDataset("Mu_146240-147116").setLuminosity(3977060.866/1e6)
#datasets.getDataset("Mu_147196-149442").setLuminosity(27907588.871/1e6)
#datasets.loadLuminosities("lumis.txt")

datasets.mergeData()

styleGenerator = styles.generator(fill=True)

#textDefaults.setCmsPreliminaryDefaults()
textDefaults.setEnergyDefaults(x=0.17)
textDefaults.setLuminosityDefaults(x=0.4, size=0.04)
createLegend.setDefaults(x1=0.65,y1=0.7)

style = TDRStyle()

class Histo:
    def __init__(self, datasets, name, lumi=None):
        self.histos = HistoManager(datasets, name)
        #print "\n".join(histos.getDatasetNames())

        if lumi == None:
            self.histos.normalizeMCByLuminosity()
        else:
            self.histos.normalizeMCToLuminosity(lumi)

        hasData = self.histos.hasHisto("Data")

        styleGenerator.reset()
        self.histos.forEachMCHisto(styleGenerator)
        if hasData:
            styles.getDataStyle()(self.histos.getHisto("Data"))
            self.histos.setHistoDrawStyle("Data", "EP")

    def addMCStatError(self):
        histoData = filter(lambda x: x.isMC(), self.histos.getHistoDataList())
        if len(histoData) == 0:
            # Only data histograms
            return

        ROOT.gStyle.SetErrorX(0.5)
        hse = HistoTotalUncertainty(histoData, "MC Stat. Err.")
        hse.call(styles.getErrorStyle())
        self.histos.append(hse)

    def createFrame(self, plotname, **kwargs):
        cf = CanvasFrame(self.histos, plotname, **kwargs)
        self.canvas = cf.canvas
        self.frame = cf.frame

    def draw(self):
        self.histos.draw()

    def save(self):
        backup = ROOT.gErrorIgnoreLevel
        ROOT.gErrorIgnoreLevel = ROOT.kWarning
        self.canvas.SaveAs(".png")
        #self.canvas.SaveAs(".eps")
        #self.canvas.SaveAs(".C")
        ROOT.gErrorIgnoreLevel = backup

dataLumi = datasets.getDataset("Data").getLuminosity()

# MET
class PlotMet:
    def __init__(self, rebin=2, postfix=""):
        self.rebin = rebin
        self.postfix = postfix
        if len(postfix) > 0:
            self.postfix = "_"+self.postfix
        self.ylabel = "Number of events / %d.0 GeV" % self.rebin
        self.xlabels = {"calomet": "Calo MET",
                        "pfmet": "PF MET",
                        "tcmet": "TC MET"}

        self.ymax = 200
        self.xmax = 300
        self.xmax = 100

    def xlabel(self, met):
        return self.xlabels[met]+" (GeV)"

    def _calculateNumEvents(self, h):
        for pn in [0, 15, 20, 30, 40]:
            pn = PrintNumEvents(pn)
            for name in [d.getName() for d in datasets.getAllDatasets()]:
                h.histos.forHisto(name, lambda h: pn(name, h))
            pn.printQcdFraction()
            print

    def _plotLinear(self, h, selection, met):
        h.createFrame(selection.replace("/", "_")+"_"+met+self.postfix, ymax=self.ymax, xmax=self.xmax)
        h.frame.GetXaxis().SetTitle(self.xlabel(met))
        h.frame.GetYaxis().SetTitle(self.ylabel)
        h.draw()
        addCmsPreliminaryText()
        addEnergyText()
        h.histos.addLuminosityText()
        h.save()

    def _plotLog(self, h, selection, met):
        h.createFrame(selection.replace("/", "_")+"_"+met+"_log"+self.postfix, yminfactor=0.01, yfactor=2, xmax=self.xmax)
        h.frame.GetXaxis().SetTitle(self.xlabel(met))
        h.frame.GetYaxis().SetTitle(self.ylabel)
        ROOT.gPad.SetLogy(True)
        h.draw()
        addCmsPreliminaryText()
        addEnergyText()
        #h.histos.addLuminosityText()
        h.save()

    def _createHisto(self, met, selection, calcNumEvents=False):
        h = Histo(datasets, selection+"/%s_et" % met)
        h.histos.forEachHisto(lambda h: h.Rebin(self.rebin))
        if calcNumEvents:
            self._calculateNumEvents(h)
        h.histos.stackMCHistograms()
        return h

    def plot(self, met, selection, calcNumEvents=False):
        h = self._createHisto(met, selection, calcNumEvents)
        self._plotLinear(h, selection, met)
        self._plotLog(h, selection, met)

    def plotLog(self, met, selection):
        h = self._createHisto(met, selection)
        self._plotLog(h, selection, met)
        
plotMet = PlotMet()
#plotMet.plot("calomet")
#plotMet.plot("pfmet")
#plotMet.plot("tcmet")
#plotMet.plot("pfmet", selection=lastSelectionBeforeMet, calcNumEvents=True)

#for x in selections[:-1]:
for x in selections:
    plotMet.plotLog("pfmet", selection=x)
    #for met in ["calomet", "pfmet", "tcmet"]:
    #    plotMet.plotLog(met, selection=x)

#for rebin in [1, 2, 4, 5, 8, 10, 15, 16, 20]:
#    pm = PlotMet(rebin, postfix="%d"%rebin)
#    for sel in [noIsoNoVetoMet[-3], lastSelectionBeforeMet]:
#        pm.plotLog("pfmet", selection=sel)

