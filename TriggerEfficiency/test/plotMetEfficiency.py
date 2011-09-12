#!/usr/bin/env python

######################################################################
#
# Authors: Matti Kortelainen
#
######################################################################

import math
import array

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect

# Configuration
# No weighting to keep TEfficiency happy
#weight = ""
weight = "VertexWeight"
#weight = "PileupWeight"

analysis = "caloMetEfficiency%sh00_h01_All" % weight
afterCut = "caloMetEfficiency%sh02_h02_CaloMet45" % weight
counters = "caloMetEfficiency%scountAnalyzer" % weight

plotStyles = [
    styles.dataStyle,
    styles.mcStyle
    ]

# main function
def main():
    file = ROOT.TFile.Open("efficiencyTree.root")
    tree = file.Get("triggerEfficiencyAnalyzer/TriggerEfficiencyTree")

    offlineSelection = "MET >= 0"
    #offlineSelection += "&& MET > 70"
    offlineSelection += "&& JetSelectionPassed && BTaggingPassed"
    #binning = "(40,0,200)"
    bins = range(0, 60, 5) + range(60, 80, 10) + range(80, 120, 20) + range(120, 200, 40) + [200]
    h = ROOT.TH1F("h1", "h1", len(bins)-1, array.array("d", bins))
    
    tree.Draw("MET>>h1", offlineSelection, "goff")
    pfMET = h.Clone("AllMET")

    tree.Draw("MET>>h1", offlineSelection+"&& TriggerBit", "goff")
    pfMETbit = h.Clone("METbit")

    tree.Draw("MET>>h1", offlineSelection+"&& CaloMETnoHF > 60", "goff")
    pfMETcut = h.Clone("METcut")

    style = tdrstyle.TDRStyle()
    
    # Apply TDR style
    plotTurnOn(pfMET, [pfMETbit, pfMETcut], ["MET60 bit", "Calo E_{T}^{miss} > 60 GeV"])


def plotTurnOn(hall, passed, passedLegends):
    p = PlotTurnOn()
    
    for hpass, leg in zip(passed, passedLegends):
        eff = Eff(hall.GetEntries(), hpass.GetEntries(), leg)
        
        print leg + ": %d/%d = %f + %f - %f" % (eff.passed, eff.all, eff.eff, eff.eff_up, eff.eff_down)

        p.addGraph(ROOT.TGraphAsymmErrors(hpass, hall, "cp"), leg)
    p.finalize()

    p.createFrame("calomet_bit_turnon", xmin=0, xmax=200)
    p.setLegend(histograms.moveLegend(histograms.createLegend(y1=0.95, y2=0.85), dx=-0.55, dy=-0.05))

    def text():
        l = ROOT.TLatex()
        l.SetNDC()
#        l.SetTextFont(l.GetTextFont()-20) # bold -> normal
        l.SetTextSize(l.GetTextSize()*0.8)
        l.DrawLatex(0.4, 0.4, "Calo E_{T}^{miss} > 45 GeV")
    #common(p, "PF E_{T}^{miss} (GeV)", "Efficiency / %.0f GeV"%hall.GetBinWidth(1), False)#, afterDraw=text)
    common(p, "PF E_{T}^{miss} (GeV)", "Efficiency", False)#, afterDraw=text)


class Eff:
    def __init__(self, all, passed, name):
        self.all = all
        self.passed = passed
        self.eff = passed/all
        self.eff_up = ROOT.TEfficiency.ClopperPearson(int(all), int(passed), 0.95, True)
        self.eff_down = ROOT.TEfficiency.ClopperPearson(int(all), int(passed), 0.95, False)
        self.eff_up = self.eff_up - self.eff
        self.eff_down = self.eff - self.eff_down

        a = ROOT.TH1F("hall_"+name, "all", 1, 0, 1)
        a.SetBinContent(1, all)
        p = ROOT.TH1F("hpassed_"+name, "passed", 1, 0, 1)
        p.SetBinContent(1, passed)

        self.effobj = ROOT.TEfficiency(p, a)
        self.effobj.SetStatisticOption(ROOT.TEfficiency.kFCP)

class HistoEff:
    def __init__(self, all, passed):
        self.effobj = ROOT.TEfficiency(passed, all)
        self.effobj.SetStatisticOption(ROOT.TEfficiency.kFCP)

class PlotTurnOn(plots.PlotBase):
    def __init__(self):
        plots.PlotBase.__init__(self, [])

    def addGraph(self, gr, name):
        self.histoMgr.appendHisto(histograms.HistoGraph(gr, name, "p", "P"))

    def finalize(self):
        self.histoMgr.forEachHisto(styles.generator2(styles.StyleMarker(markerSizes=[1.2, 1.5]), plotStyles))

def common(h, xlabel, ylabel, addLuminosityText=True, afterDraw=None):
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.draw()
    if afterDraw != None:
        afterDraw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    if addLuminosityText:
        h.addLuminosityText()
    h.save()

# Call the main function if the script is executed (i.e. not imported)
if __name__ == "__main__":
    main()
