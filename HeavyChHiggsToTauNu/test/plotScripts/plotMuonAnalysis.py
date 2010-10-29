#!/usr/bin/env python

import ROOT
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset import *
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms import *
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter import *
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle import *
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles

legendLabels = {
    "Data":                  "Data",
    "TTbar":                 "t#bar{t}",
    "TTbarJets":             "t#bar{t}+jets",
    "WJets":                 "W+jets",
    "ZJets":                 "Z+jets",
    "QCD_Pt15to30_Fall10":   "QCD, 15 < #hat{p}_T < 30",
    "QCD_Pt30to50_Fall10":   "QCD, 30 < #hat{p}_T < 50",
    "QCD_Pt50to80_Fall10":   "QCD, 50 < #hat{p}_T < 80",
    "QCD_Pt80to120_Fall10":  "QCD, 80 < #hat{p}_T < 120",
    "QCD_Pt120to170_Fall10": "QCD, 120 < #hat{p}_T < 170",
    "QCD_Pt170to300_Fall10": "QCD, 170 < #hat{p}_T < 300"}

ROOT.gROOT.SetBatch(True)

QCDdetails = False
#QCDdetails = True

#lastSelection = "h11_JetSelection"
#lastMultip = "h11_Multiplicity"

lastSelection = "h12_METCut"
lastMultip = "h12_Multiplicity"



style = TDRStyle()
datasets = getDatasetsFromMulticrabCfg(counters="countAnalyzer")

datasetsQCD = None
if QCDdetails:
    datasetsQCD = getDatasetsFromMulticrabCfg(counters="countAnalyzer")
    datasetsQCD.selectAndReorder(["QCD_Pt15to30_Fall10",
                                  "QCD_Pt30to50_Fall10",
                                  "QCD_Pt50to80_Fall10",
                                  "QCD_Pt80to120_Fall10",
                                  "QCD_Pt120to170_Fall10",
                                  "QCD_Pt170to300_Fall10"
                                  ])

#datasets.remove(["SingleTop_sChannel", "SingleTop_tChannel", "SingleTop_tWChannel"])
# datasets = getDatasetsFromCrabDirs(["Mu_140042-144114",
#                                     "WJets", "TTbarJets", "ZJets",
#                                     "QCD_Pt120to170_Fall10", "QCD_Pt170to300_Fall10",
#                                     "QCD_Pt30to50_Fall10", "QCD_Pt50to80_Fall10",
#                                     "QCD_Pt80to120_Fall10"], counters="countAnalyzer")
#datasets.getDataset("Mu_140042-144114").setLuminosity(2126184.794/1e6) # ub^-1 -> pb^-1
#datasets.getDataset("Mu_146240-147116").setLuminosity(4390660.197/1e6)
#datasets.getDataset("Mu_147196-148058").setLuminosity(7618294.554/1e6)
datasets.getDataset("Mu_135821-144114").setLuminosity(1763049.941/1e6) # ub^-1 -> pb^-1
datasets.getDataset("Mu_146240-147116").setLuminosity(4390660.197/1e6)
datasets.getDataset("Mu_147196-148058").setLuminosity(7618294.554/1e6)
#datasets.remove(["Mu_146240-147116", "Mu_147196-148058"])
datasets.mergeData()
datasets.merge("QCD", ["QCD_Pt15to30_Fall10", "QCD_Pt30to50_Fall10", "QCD_Pt50to80_Fall10",
                       "QCD_Pt80to120_Fall10", "QCD_Pt120to170_Fall10", "QCD_Pt170to300_Fall10"])
datasets.merge("Single t", ["SingleTop_sChannel", "SingleTop_tChannel", "SingleTop_tWChannel"])

class Histo:
    def __init__(self, datasets, name, lumi=None):
        self.histos = HistoSet(datasets, name)
        #print "\n".join(histos.getDatasetNames())

        if lumi == None:
            self.histos.normalizeMCByLuminosity()
        else:
            self.histos.normalizeMCToLuminosity(lumi)

        self.histos.setHistoLegendLabels(legendLabels)

        hasData = self.histos.hasHisto("Data")

        self.histos.setHistoLegendStyleAll("F")
        if hasData:
            self.histos.setHistoLegendStyle("Data", "p")

        self.histos.forEachMCHisto(styles.generator(fill=True))
        if hasData:
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

# After muon selection (h10_ElectronVeto)
h = Histo(datasets, "h10_Multiplicity/jets_multiplicity")
h.histos.stackMCHistograms()
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

# After muon selection + jet multip. cut (h11_JetSelection)
h = Histo(datasets, lastMultip+"/jets_multiplicity")
h.histos.stackMCHistograms()
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
def muonPt(h, prefix=""):
    h.histos.forEachHisto(lambda h: h.Rebin(5))
    h.histos.stackMCHistograms()
    h.createFrame(prefix+"muon_pt")
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.addLegend(createLegend(0.7, 0.5, 0.9, 0.8))
    #ROOT.gPad.SetLogy(True)
    h.draw()
    addCmsPreliminaryText()
    addEnergyText(x=0.3, y=0.85)
    h.histos.addLuminosityText()
    h.save()

    h.createFrame(prefix+"muon_pt_log", ymin=0.1, ymax=1e3)
    h.addLegend(createLegend(0.7, 0.5, 0.9, 0.8))
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    ROOT.gPad.SetLogy(True)
    h.draw()
    addCmsPreliminaryText()
    addEnergyText(x=0.3, y=0.85)
    h.histos.addLuminosityText()
    h.save()

    # h = Histo(datasets, "afterOtherCuts/pt")
    h.createFrame(prefix+"muon_pt_cut20", xmin=20, ymax=200)
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.draw()
    addCmsPreliminaryText()
    addEnergyText(x=0.3, y=0.85)
    h.histos.addLuminosityText()
    h.save()

muonPt(Histo(datasets, "afterOtherCuts/pt"))
if QCDdetails:
    muonPt(Histo(datasetsQCD, "afterOtherCuts/pt", datasets.getDataset("Data").getLuminosity()), "qcd_")

# Muon pt after all other cuts
h = Histo(datasets, lastSelection+"/muon_pt")
ylabel = "Number of muons / 5.0 GeV/c"
h.histos.forEachHisto(lambda h: h.Rebin(5))
h.histos.stackMCHistograms()
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
h = Histo(datasets, lastSelection+"/muon_eta")
h.histos.forEachHisto(lambda h: h.Rebin(5))
h.histos.stackMCHistograms()
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
h = Histo(datasets, lastSelection+"/muon_relIso")
h.histos.forEachHisto(lambda h: h.Rebin(2))
h.histos.stackMCHistograms()
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

# Muon track ip w.r.t. beam spot
h = Histo(datasets, lastSelection+"/muon_trackDB")
h.histos.stackMCHistograms()
h.createFrame("muon_trackdb", xmin=0, xmax=0.2, ymin=0.1, ymax=500)
h.frame.GetXaxis().SetTitle("Muon track d_{0}(Bsp) (cm)")
h.frame.GetYaxis().SetTitle("Number of muons")
h.addLegend(createLegend(0.7, 0.5, 0.9, 0.8))
ROOT.gPad.SetLogy(True)
h.draw()
addCmsPreliminaryText()
addEnergyText(x=0.3, y=0.85)
h.histos.addLuminosityText()
h.save()

# MET
def plotMet(met, selection=lastSelection, prefix="met"):
    rebin = 5
    ylabel = "Number of events / 5.0 GeV"
    xlabel = {"calomet": "Calo MET",
              "pfmet": "PF MET",
              "tcmet": "TC MET"}[met] + " (GeV)"

    h = Histo(datasets, selection+"/%s_et" % met)
    h.histos.forEachHisto(lambda h: h.Rebin(rebin))
    h.histos.stackMCHistograms()
    h.createFrame(prefix+"_"+met, xmax=200)
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.addLegend(createLegend(0.7, 0.5, 0.9, 0.8))
    h.draw()
    addCmsPreliminaryText()
    addEnergyText(x=0.3, y=0.85)
    h.histos.addLuminosityText()
    h.save()

    h.createFrame(prefix+"_"+met+"_log", ymin=0.1, ymax=100, xmax=200)
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.addLegend(createLegend(0.71, 0.5, 0.91, 0.8))
    ROOT.gPad.SetLogy(True)
    h.draw()
    addCmsPreliminaryText()
    addEnergyText(x=0.3, y=0.85)
    h.histos.addLuminosityText()
    h.save()

plotMet("calomet")
plotMet("pfmet")
plotMet("tcmet")

plotMet("pfmet", selection="h11_JetSelection", prefix="met_afterjet")

print "============================================================"
print "Dataset info: "
datasets.printInfo()

eventCounter = EventCounter(datasets)
eventCounter.normalizeMCByLuminosity()

print "============================================================"
print "Main counter (MC normalized by collision data luminosity)"
eventCounter.getMainCounter().printCounter(FloatDecimalFormat(1))


if QCDdetails:
    print "============================================================"
    print "QCD dataset info: "
    datasetsQCD.printInfo()

    eventCounter = EventCounter(datasetsQCD)
    eventCounter.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())

    print "============================================================"
    print "Main counter (MC normalized by collision data luminosity)"
    eventCounter.getMainCounter().printCounter(FloatDecimalFormat(1))

    eventCounter = EventCounter(datasetsQCD)

    print "============================================================"
    print "Main counter (MC events)"
    eventCounter.getMainCounter().printCounter(FloatDecimalFormat(0))
