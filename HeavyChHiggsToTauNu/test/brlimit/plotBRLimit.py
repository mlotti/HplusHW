#!/usr/bin/env python

import sys
import json
import array

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots

def main():
    limits = BRLimits()

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    
    plot = plots.PlotBase([
            histograms.HistoGraph(limits.observedGraph(), "Observed", drawStyle="PL", legendStyle="lp"),
            histograms.HistoGraph(limits.expectedGraph(), "Expected", drawStyle="L"),
            histograms.HistoGraph(limits.expectedGraph(sigma=1), "Expected1", drawStyle="F", legendStyle="fl"),
            histograms.HistoGraph(limits.expectedGraph(sigma=2), "Expected2", drawStyle="F", legendStyle="fl"),
            ])

    plot.histoMgr.setHistoLegendLabelMany({
            "Expected": None,
            "Expected1": "Expected median #pm 1#sigma",
            "Expected2": "Expected median #pm 2#sigma"
            })
    plot.setLegend(histograms.createLegend(0.48, 0.75, 0.85, 0.92))

    plot.createFrame("limitsBr", opts={"ymin": 0, "ymax": 0.15})
    plot.frame.GetXaxis().SetTitle("m_{H^{+}} (GeV)")
    plot.frame.GetYaxis().SetTitle("95% CL limit for BR(t#rightarrow bH^{+})")

    plot.draw()

    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    histograms.addLuminosityText(x=None, y=None, lumi=limits.getLuminosity())

    size = 20
    x = 0.2
    histograms.addText(x, 0.88, "t #rightarrow H^{+}b, H^{+} #rightarrow #tau#nu", size=size)
    histograms.addText(x, 0.84, limits.getFinalstateText(), size=size)
    histograms.addText(x, 0.79, "BR(H^{+} #rightarrow #tau#nu) = 1", size=size)

    plot.save()


class BRLimits:
    def __init__(self, directory="."):
        resultfile="limits.json"
        configfile="configuration.json"

        f = open(os.path.join(directory, resultfile), "r")
        limits = json.load(f)
        f.close()

        self.lumi = 1000*float(limits["luminosity"]) # 1/fb -> 1/pb

        self.mass = limits["masspoints"].keys()
        self.observed = [limits["masspoints"][m]["observed"] for m in self.mass]
        self.expectedMedian = [limits["masspoints"][m]["expected"]["median"] for m in self.mass]
        self.expectedMinus2 = [limits["masspoints"][m]["expected"]["-2sigma"] for m in self.mass]
        self.expectedMinus1 = [limits["masspoints"][m]["expected"]["-1sigma"] for m in self.mass]
        self.expectedPlus1 = [limits["masspoints"][m]["expected"]["+1sigma"] for m in self.mass]
        self.expectedPlus2 = [limits["masspoints"][m]["expected"]["+2sigma"] for m in self.mass]

        members = ["mass", "observed"] + ["expected"+p for p in ["Median", "Minus2", "Minus1", "Plus1", "Plus2"]]
        for attr in members:
            setattr(self, attr, [float(m) for m in getattr(self, attr)])

        # Sort according to mass
        massIndex = [(self.mass[i], i) for i in range(len(self.mass))]
        massIndex.sort()
        def rearrange(lst):
            return [lst[massIndex[i][1]] for i in xrange(len(massIndex))]
        for attr in members:
            setattr(self, attr, rearrange(getattr(self, attr)))
        

        f = open(os.path.join(directory, configfile), "r")
        config = json.load(f)
        f.close()

        self.finalstates = []
        def hasDatacard(name):
            for datacard in config["datacards"]:
                if name in datacard:
                    return True
            return False

        if hasDatacard("_hplushadronic_"):
            self.finalstates.append("#tau_{h}+jets")
        if hasDatacard("_etau_"):
            self.finalstates.append("e#tau_{h}")
        if hasDatacard("_mutau_"):
            self.finalstates.append("#mu#tau_{h}")
        if hasDatacard("_emu_"):
            self.finalstates.append("e#mu")

    def getLuminosity(self):
        return self.lumi

    def getFinalstates(self):
        return self.finalstates

    def getFinalstateText(self):
        if len(self.finalstates) == 1:
            return "%s final state" % self.finalstates[0]

        ret = ", ".join(self.finalstates[:-1])
        ret += ", and %s final states" % self.finalstates[-1]
        return ret

    def observedGraph(self):
        gr = ROOT.TGraph(len(self.mass),
                         array.array("d", self.mass),
                         array.array("d", self.observed)
                         )
        gr.SetMarkerStyle(21)
        gr.SetMarkerSize(1.5)
        gr.SetMarkerColor(ROOT.kBlack)
        gr.SetLineWidth(3)
        gr.SetLineColor(ROOT.kBlack)
        gr.SetName("Observed")

        return gr

    def expectedGraphNew(self, sigma=0):
        massArray = array.array("d", self.mass)
        massErr = array.array("d", [0]*len(self.mass))
        medianArray = array.array("d", self.expectedMedian)
        if sigma == 0:
            gr = ROOT.TGraph(len(self.mass), massArray, medianArray)
            gr.SetName("Expected")
        elif sigma == 1:
            gr = ROOT.TGraphAsymmErrors(len(self.mass), massArray, medianArray, massErr, massErr,
                                        array.array("d", [self.expectedMedian[i]-self.expectedMinus1[i] for i in xrange(len(self.mass))]),
                                        array.array("d", [self.expectedPlus1[i]-self.expectedMedian[i] for i in xrange(len(self.mass))]))
            gr.SetFillColor(ROOT.kGreen-3)
            gr.SetName("Expected1Sigma")
        elif sigma == 2:
            gr = ROOT.TGraphAsymmErrors(len(self.mass), massArray, medianArray, massErr, massErr,
                                        array.array("d", [self.expectedMedian[i]-self.expectedMinus2[i] for i in xrange(len(self.mass))]),
                                        array.array("d", [self.expectedPlus2[i]-self.expectedMedian[i] for i in xrange(len(self.mass))]))
            gr.SetFillColor(ROOT.kYellow)
            gr.SetName("Expected2Sigma")
        else:
            raise Exception("Invalid value of sigma '%d', valid values are 0,1,2" % sigma)

        gr.SetLineStyle(2)
        gr.SetLineWidth(3)
        gr.SetLineColor(ROOT.kBlack)
        gr.SetMarkerStyle(20)

        return gr

    def expectedGraph(self, sigma=0):
        massArray = array.array("d", self.mass)
        massErr = array.array("d", [0]*len(self.mass))
        medianArray = array.array("d", self.expectedMedian)
        if sigma == 0:
            gr = ROOT.TGraph(len(self.mass), massArray, medianArray)
            gr.SetName("Expected")
        elif sigma == 1:
            tmp1 = self.mass[:]
            tmp1.reverse()
            tmp2 = self.expectedPlus1[:]
            tmp2.reverse()

            gr = ROOT.TGraph(2*len(self.mass),
                             array.array("d", self.mass+tmp1),
                             array.array("d", self.expectedMinus1 + tmp2))

            gr.SetFillColor(ROOT.kGreen-3)
            gr.SetName("Expected1Sigma")
        elif sigma == 2:
            tmp1 = self.mass[:]
            tmp1.reverse()
            tmp2 = self.expectedPlus2[:]
            tmp2.reverse()

#            print self.mass+tmp1
#            print self.expectedMinus2+tmp2

            gr = ROOT.TGraph(2*len(self.mass),
                             array.array("d", self.mass+tmp1),
                             array.array("d", self.expectedMinus2 + tmp2))

            gr.SetFillColor(ROOT.kYellow)
            gr.SetName("Expected2Sigma")
        else:
            raise Exception("Invalid value of sigma '%d', valid values are 0,1,2" % sigma)

        gr.SetLineStyle(2)
        gr.SetLineWidth(3)
        gr.SetLineColor(ROOT.kBlack)
        gr.SetMarkerStyle(20)

        return gr
                                          

                           

if __name__ == "__main__":
    main()
