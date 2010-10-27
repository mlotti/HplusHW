#!/usr/bin/env python

###########################################################################
#
# This script is only intended as an example, please do NOT modify it.
# For example, start from scratch and look here for help, or make a
# copy of it and modify the copy (including removing all unnecessary
# code).
#
###########################################################################


import ROOT
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms import *
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle import *
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles

legendLabels = {
    "Data":                  "Data",
    "TTbar":                 "t#bar{t}",
    "TTbarJets":             "t#bar{t}+jets",
    "WJets":                 "W+jets",
    "ZJets":                 "Z+jets",
    "QCD_Pt30to50_Fall10":   "QCD, 30 < #hat{p}_T < 50",
    "QCD_Pt50to80_Fall10":   "QCD, 50 < #hat{p}_T < 80",
    "QCD_Pt80to120_Fall10":  "QCD, 80 < #hat{p}_T < 120",
    "QCD_Pt120to170_Fall10": "QCD, 120 < #hat{p}_T < 170",
    "QCD_Pt170to3+0_Fall10": "QCD, 170 < #hat{p}_T < 300"}


ROOT.gROOT.SetBatch(True)
style = TDRStyle()
datasets = getDatasetsFromMulticrabCfg(counters="countAnalyzer")
datasetsQCD = getDatasetsFromMulticrabCfg(counters="countAnalyzer")
datasetsQCD.selectAndReorder(["QCD_Pt30to50_Fall10",
                              "QCD_Pt50to80_Fall10",
                              "QCD_Pt80to120_Fall10",
                              "QCD_Pt120to170_Fall10",
                              "QCD_Pt170to3+0_Fall10"
                              ])
#datasets.remove(["SingleTop_sChannel", "SingleTop_tChannel", "SingleTop_tWChannel"])
# datasets = getDatasetsFromCrabDirs(["Mu_140042-144114",
#                                     "WJets", "TTbarJets", "ZJets",
#                                     "QCD_Pt120to170_Fall10", "QCD_Pt170to300_Fall10",
#                                     "QCD_Pt30to50_Fall10", "QCD_Pt50to80_Fall10",
#                                     "QCD_Pt80to120_Fall10"], counters="countAnalyzer")
                                    

class Histo:
    def __init__(self, datasets, name):
        self.histos = datasets.getHistoSet(name)
        #print "\n".join(histos.getDatasetNames())

        self.histos.getDataset("Mu_140042-144114").setLuminosity(3068636.598/1e6) # ub^-1 -> pb^-1
        self.histos.getDataset("Mu_146240-147116").setLuminosity(3879919.235/1e6)

        self.histos.mergeDataDatasets()

        self.histos.normalizeMCByLuminosity()

        self.histos.mergeDatasets("QCD", ["QCD_Pt15to30_Fall10", "QCD_Pt30to50_Fall10", "QCD_Pt50to80_Fall10",
                                          "QCD_Pt80to120_Fall10", "QCD_Pt120to170_Fall10", "QCD_Pt170to300_Fall10"])
        self.histos.mergeDatasets("Single t", ["SingleTop_sChannel", "SingleTop_tChannel", "SingleTop_tWChannel"])

        self.histos.setHistoLegendLabels(legendLabels)

        self.histos.setHistoLegendStyleAll("F")
        self.histos.setHistoLegendStyle("Data", "p")

        self.histos.forEachMCHisto(styles.generator(fill=True))
        styles.getDataStyle()(self.histos.getHisto("Data"))

        self.histos.setHistoDrawStyle("Data", "EP")

    def createFrame(self, plotname, xmin=None, xmax=None, ymin=None, ymax=None):
        (self.canvas, self.frame) = self.histos.createCanvasFrame(plotname, xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax)

    def addLegend(self, legend):
        self.legend = legend
        self.histos.addToLegend(legend)

    def draw(self):
        self.histos.draw()
        self.legend.Draw()

    def save(self):
        self.canvas.SaveAs(".png")
        #self.canvas.SaveAs(".eps")
        #self.canvas.SaveAs(".C")


# After muon selection
h = Histo(datasets, "h06_Multiplicity/jets_multiplicity")
h.histos.stackMCDatasets()
h.createFrame("njets", ymin=0.1, ymax=1e6)
h.frame.GetXaxis().SetTitle("Jet multiplicity")
h.frame.GetYaxis().SetTitle("Number of events")
h.addLegend(createLegend(0.7, 0.5, 0.9, 0.8))
ROOT.gPad.SetLogy(True)
h.draw()
addCmsPreliminaryText()
addEnergyText(x=0.3, y=0.85)
h.histos.addLuminosityText()
h.save()

# After muon selection + jet multip. cut
h = Histo(datasets, "h07_Multiplicity/jets_multiplicity")
h.histos.stackMCDatasets()
h.createFrame("njets_afternjetcut", xmin=3)
h.frame.GetXaxis().SetTitle("Jet multiplicity")
h.frame.GetYaxis().SetTitle("Number of events")
h.addLegend(createLegend(0.7, 0.5, 0.9, 0.8))
#ROOT.gPad.SetLogy(True)
h.draw()
addCmsPreliminaryText()
addEnergyText(x=0.3, y=0.85)
h.histos.addLuminosityText()
h.save()


# Muon pt after all other cuts
xlabel = "Muon p_{T} (GeV/c)"
ylabel = "Number of muons / 5.0 GeV/c"
h = Histo(datasets, "afterOtherCuts/pt")
h.histos.forEachHisto(lambda h: h.Rebin(5))
h.histos.stackMCDatasets()
h.createFrame("muon_pt")
h.frame.GetXaxis().SetTitle(xlabel)
h.frame.GetYaxis().SetTitle(ylabel)
h.addLegend(createLegend(0.7, 0.5, 0.9, 0.8))
#ROOT.gPad.SetLogy(True)
h.draw()
addCmsPreliminaryText()
addEnergyText(x=0.3, y=0.85)
h.histos.addLuminosityText()
h.save()

# Muon pt after all other cuts
h.createFrame("muon_pt_log", ymin=0.1, ymax=1e3)
h.addLegend(createLegend(0.7, 0.5, 0.9, 0.8))
h.frame.GetXaxis().SetTitle(xlabel)
h.frame.GetYaxis().SetTitle(ylabel)
ROOT.gPad.SetLogy(True)
h.draw()
addCmsPreliminaryText()
addEnergyText(x=0.3, y=0.85)
h.histos.addLuminosityText()
h.save()

# Muon pt after all other cuts
# h = Histo(datasets, "afterOtherCuts/pt")
h.createFrame("muon_pt_cut20", xmin=20, ymax=200)
h.frame.GetXaxis().SetTitle(xlabel)
h.frame.GetYaxis().SetTitle(ylabel)
h.draw()
addCmsPreliminaryText()
addEnergyText(x=0.3, y=0.85)
h.histos.addLuminosityText()
h.save()

# Muon pt after all other cuts
h = Histo(datasets, "h07_JetSelection/muon_pt")
ylabel = "Number of muons / 5.0 GeV/c"
h.histos.forEachHisto(lambda h: h.Rebin(5))
h.histos.stackMCDatasets()
h.createFrame("muon_pt_cut20_2", xmin=20, ymax=200)
h.frame.GetXaxis().SetTitle(xlabel)
h.frame.GetYaxis().SetTitle(ylabel)
h.addLegend(createLegend(0.7, 0.5, 0.9, 0.8))
#ROOT.gPad.SetLogy(True)
h.draw()
addCmsPreliminaryText()
addEnergyText(x=0.3, y=0.85)
h.histos.addLuminosityText()
h.save()

# Muon eta after all other cuts
h = Histo(datasets, "h07_JetSelection/muon_eta")
h.histos.forEachHisto(lambda h: h.Rebin(5))
h.histos.stackMCDatasets()
h.createFrame("muon_eta")
h.frame.GetXaxis().SetTitle("Muon  #eta")
h.frame.GetYaxis().SetTitle("Number of muons / 0.5")
h.addLegend(createLegend(0.7, 0.5, 0.9, 0.8))
#ROOT.gPad.SetLogy(True)
h.draw()
addCmsPreliminaryText()
addEnergyText(x=0.3, y=0.85)
h.histos.addLuminosityText()
h.save()

# Muon isolation after all other cuts
h = Histo(datasets, "h07_JetSelection/muon_relIso")
h.histos.forEachHisto(lambda h: h.Rebin(2))
h.histos.stackMCDatasets()
h.createFrame("muon_reliso", xmax=0.15)
h.frame.GetXaxis().SetTitle("Muon rel. isol. (GeV/c)")
h.frame.GetYaxis().SetTitle("Number of muons / 0.01")
h.addLegend(createLegend(0.7, 0.5, 0.9, 0.8))
#ROOT.gPad.SetLogy(True)
h.draw()
addCmsPreliminaryText()
addEnergyText(x=0.3, y=0.85)
h.histos.addLuminosityText()
h.save()

h.createFrame("muon_reliso_log", xmax=0.15, ymin=0.3, ymax=1000)
h.frame.GetXaxis().SetTitle("Muon rel. isol. (GeV/c)")
h.frame.GetYaxis().SetTitle("Number of muons / 0.01")
h.addLegend(createLegend(0.72, 0.7, 0.92, 0.9))
ROOT.gPad.SetLogy(True)
h.draw()
addCmsPreliminaryText()
addEnergyText(x=0.23, y=0.85)
h.histos.addLuminosityText(x=0.45, y=0.85)
h.save()

# Muon track ip w.r.t. PV
h = Histo(datasets, "h07_JetSelection/muon_trackDB")
h.histos.stackMCDatasets()
h.createFrame("muon_trackdb", xmin=0, xmax=0.2, ymin=0.1, ymax=500)
h.frame.GetXaxis().SetTitle("Muon track d_{0}(PV) (cm)")
h.frame.GetYaxis().SetTitle("Number of muons")
h.addLegend(createLegend(0.7, 0.5, 0.9, 0.8))
ROOT.gPad.SetLogy(True)
h.draw()
addCmsPreliminaryText()
addEnergyText(x=0.3, y=0.85)
h.histos.addLuminosityText()
h.save()
