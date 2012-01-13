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
#styles.mcStyle.styles[0].marker = 34
#styles.mcStyle2.styles[0].marker = ROOT.kFullSquare
plotStyles = [
    styles.dataStyle,
    styles.mcStyle2,
    styles.mcStyle,
    ]

l1met = False # for runs 165970-167913
#l1met = True # for runs 170722-173692

runs = "165970-167913"; lumi = 98.171999999999997+4.2910000000000004+445.12599999999998+243.08099999999999
if l1met:
    runs = "170722-173692"; lumi = 373.25900000000001+412.35899999999998+246.52699999999999
    #runs = "170722-172619"; lumi = 373.25900000000001
    #runs = "172620-173692"; lumi = 412.35899999999998+246.52699999999999

# main function
def main():
    file = ROOT.TFile.Open("histograms-%s.root"%runs)
    tree = file.Get("triggerEfficiency/tree")

    l1Bit = "(L1_SingleTauJet52 || L1_SingleJet68)"
    l1metsel = ""
    if l1met:
        l1metsel = "&& L1MET > 30"

    offlineSelection = "MET >= 0"
    #offlineSelection += "&& MET > 70"
    offlineSelection += "&& ElectronVetoPassed && MuonVetoPassed"
    offlineSelection += "&& JetSelectionPassed && BTaggingPassed"
    caloMetNoHF = "CaloMETnoHF"
    caloMet = "CaloMET"
    if l1met:
        # Handle the bug in the L1 seed of HLT_PFTau35_Trk20, it was
        # supposed to be OR, but it was AND
        # But we don't actully need this, because the events are already triggered by it
#        offlineSelection += "&& Max$(L1TauJet_p4.Et()) > 51 && Max$(L1CenJet_p4.Et()) > 51"
        l1Bit = "L1_Jet52_Central_ETM30"
        pass

    #binning = "(40,0,200)"
    bins = range(0, 60, 10) + range(60, 80, 10) + range(80, 120, 20) + range(120, 200, 40) + [200]
    h = ROOT.TH1F("h1", "h1", len(bins)-1, array.array("d", bins))
    
    tree.Draw("MET>>h1", offlineSelection, "goff")
    pfMET = h.Clone("AllMET")

    tree.Draw("MET>>h1", offlineSelection+"&&"+l1Bit, "goff")
    pfMETL1bit = h.Clone("METL1bit")

    tree.Draw("MET>>h1", offlineSelection+l1metsel, "goff")
    pfMETL1cut = h.Clone("METL1cut")

    tree.Draw("MET>>h1", offlineSelection+"&& TriggerBit", "goff")
    pfMETbit = h.Clone("METbit")

    tree.Draw("MET>>h1", offlineSelection+("&& %s > 60" % caloMetNoHF)+l1metsel, "goff")
    pfMETcutNoHF = h.Clone("METcut")

    tree.Draw("MET>>h1", offlineSelection+("&& %s > 60" % caloMet)+l1metsel, "goff")
    pfMETcut = h.Clone("METcut")

    # Apply TDR style
    style = tdrstyle.TDRStyle()

    #legs = ["MET60 bit", "CaloMETnoHF > 60 GeV", "CaloMET > 60 GeV"]
    #if l1met:
    #    legs = ["L1_ETM30 & MET60 bits", "L1 MET > 30 & CaloMETnoHF > 60 GeV", "L1 MET > 30 & CaloMET > 60 GeV"]
    #plotTurnOn(pfMET, [pfMETbit, pfMETcutNoHF, pfMETcut], legs)

    legs = ["HLT_MET60 bit", "Offline calo E_{T}^{miss} (excl. HF) > 60 GeV"]
    pfMETcut2 = pfMETcutNoHF
    if l1met:
        legs = ["L1_ETM30 & HLT_MET60 bits", "L1 E_{T}^{miss} > 30 & offline calo E_{T}^{miss} (incl. HF) > 60 GeV"]
        pfMETcut2 = pfMETcut
    plotTurnOn(pfMET, [pfMETbit, pfMETcut2], legs)

    plotTurnOn(pfMET, [pfMETL1bit, pfMETL1cut], ["L1_ETM30", "L1 MET > 30"], "calomet_l1bit_turnon")


def plotTurnOn(hall, passed, passedLegends, name="calomet_bit_turnon"):
    graphs = []
    for hpass, leg in zip(passed, passedLegends):
        eff = Eff(hall.GetEntries(), hpass.GetEntries(), leg)
        
        print leg + ": %d/%d = %f + %f - %f" % (eff.passed, eff.all, eff.eff, eff.eff_up, eff.eff_down)

        gr = ROOT.TGraphAsymmErrors(hpass, hall, "cp")
        graphs.append(histograms.HistoGraph(gr, leg, "p", "P"))
    #p = plots.ComparisonManyPlot(graphs[0], graphs[1:]) 
    #p.histoMgr.forEachHisto(styles.generator2(styles.StyleMarker(markerSizes=[1.0, 1.5, 2.0]), plotStyles))
    p = plots.ComparisonPlot(graphs[0], graphs[1])
    p.histoMgr.forEachHisto(styles.generator2(styles.StyleMarker(markerSizes=[1.0, 2.2]), plotStyles))
    p.setLuminosity(lumi)

    p.createFrame(name+"_"+runs, createRatio=True, invertRatio=True,
                  opts1={"xmin":0, "xmax":200, "ymin": 0, "ymax": 1.2},
                  #opts2={"ymin": 0.5, "ymax": 2.0}
                  opts2={"ymin": 0, "ymax": 2.5}
                  )
    p.getFrame2().GetYaxis().SetTitle("Ratio")
    p.setLegend(histograms.moveLegend(histograms.createLegend(y1=0.95, y2=0.85), dx=-0.55, dy=-0.02))
    p.appendPlotObject(histograms.PlotText(0.2, 0.79, "Runs %s"%runs, size=17))
    if not l1met:
        hltMetHF = "excluded from"
    else:
        hltMetHF = "included in"
    p.appendPlotObject(histograms.PlotText(0.2, 0.75, "HF %s HLT E_{T}^{miss}" % hltMetHF, size=17))

    def text():
        l = ROOT.TLatex()
        l.SetNDC()
#        l.SetTextFont(l.GetTextFont()-20) # bold -> normal
        l.SetTextSize(l.GetTextSize()*0.8)
        l.DrawLatex(0.4, 0.4, "Calo E_{T}^{miss} > 45 GeV")
    #common(p, "PF E_{T}^{miss} (GeV)", "Efficiency / %.0f GeV"%hall.GetBinWidth(1), False)#, afterDraw=text)
    common(p, "Uncorrected PF E_{T}^{miss} (GeV)", "Efficiency of E_{T}^{miss} cut")#, afterDraw=text)


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
