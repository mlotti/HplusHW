#!/usr/bin/env python

import os
import sys
import json
import array

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles

def main():
    limits = BRLimits()

    # Apply TDR style
    style = tdrstyle.TDRStyle()

    doBRlimit(limits)
    doLimitError(limits)
    limits.print2()

def doBRlimit(limits):
    graphs = []
    gr = limits.observedGraph()
    if gr != None:
        graphs.append(histograms.HistoGraph(gr, "Observed", drawStyle="PL", legendStyle="lp"))
    graphs.extend([
            histograms.HistoGraph(limits.expectedGraph(), "Expected", drawStyle="L"),
            histograms.HistoGraph(limits.expectedBandGraph(sigma=1), "Expected1", drawStyle="F", legendStyle="fl"),
            histograms.HistoGraph(limits.expectedBandGraph(sigma=2), "Expected2", drawStyle="F", legendStyle="fl"),
            ])

    plot = plots.PlotBase(graphs)

    plot.histoMgr.setHistoLegendLabelMany({
            "Expected": None,
            "Expected1": "Expected median #pm 1#sigma",
            "Expected2": "Expected median #pm 2#sigma"
            })
    plot.setLegend(histograms.createLegend(0.48, 0.75, 0.85, 0.92))

    plot.createFrame("limitsBr", opts={"ymin": 0, "ymax": limits.getFinalstateYmax()})
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

def doLimitError(limits):
    expRelErrors = []
    expLabels = {}
    obsRelErrors = []
    obsLabels = {}

    order = [0, 1, -1, 2, -2]
    expErrors = [limits.expectedErrorGraph(sigma=s) for s in order]
    if expErrors[0] != None:
        exps = [limits.expectedGraph(sigma=s) for s in order]
        expRelErrors = [(divideGraph(expErrors[i], exps[i]), "ExpRelErr%d"%i) for i in xrange(len(exps))]
        expLabels = {
            "ExpRelErr0": "Expected median",
            "ExpRelErr1": "Expected +1#sigma",
            "ExpRelErr2": "Expected -1#sigma",
            "ExpRelErr3": "Expected +2#sigma",
            "ExpRelErr4": "Expected -2#sigma",
            }

    obsErr = limits.observedErrorGraph()
    if obsErr != None:
        obs = limits.observedGraph()
        if obs != None:
            obsRelErrors = [(divideGraph(obsErr, obs), "ObsRelErr")]
            obsLabels = {"ObsRelErr": "Observed"}

    if len(expRelErrors) == 0 and len(obsRelErrors) == 0:
        return
        
    plot = plots.PlotBase()
    if len(expRelErrors) > 0:
        plot.histoMgr.extendHistos([histograms.HistoGraph(x[0], x[1], drawStyle="PL", legendStyle="lp") for x in expRelErrors])
        plot.histoMgr.forEachHisto(styles.generator())
        def sty(h):
            r = h.getRootHisto()
            r.SetLineStyle(1)
            r.SetLineWidth(3)
            r.SetMarkerSize(1.4)
        plot.histoMgr.forEachHisto(sty)
        plot.histoMgr.setHistoLegendLabelMany(expLabels)
    if len(obsRelErrors) > 0:
        obsRelErrors[0][0].SetMarkerSize(1.4)
        obsRelErrors[0][0].SetMarkerStyle(25)
        plot.histoMgr.insertHisto(0, histograms.HistoGraph(obsRelErrors[0][0], obsRelErrors[0][1], drawStyle="PL", legendStyle="lp"))
        plot.histoMgr.setHistoLegendLabelMany(obsLabels)

    plot.setLegend(histograms.moveLegend(histograms.createLegend(0.48, 0.75, 0.85, 0.92), dx=0.1, dy=-0.1))

    plot.createFrame("limitsBrRelativeUncertainty", opts={"ymin": 0, "ymaxfactor": 1.5})
    plot.frame.GetXaxis().SetTitle("m_{H^{+}} (GeV)")
    plot.frame.GetYaxis().SetTitle("Uncertainty/limit")

    plot.draw()

    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    histograms.addLuminosityText(x=None, y=None, lumi=limits.getLuminosity())

    size = 20
    x = 0.2
    histograms.addText(x, 0.88, "t #rightarrow H^{+}b, H^{+} #rightarrow #tau#nu", size=size)
    histograms.addText(x, 0.84, limits.getFinalstateText(), size=size)
    histograms.addText(x, 0.79, "BR(H^{+} #rightarrow #tau#nu) = 1", size=size)

    size = 22
    x = 0.55
    histograms.addText(x, 0.88, "Toy MC relative", size=size)
    histograms.addText(x, 0.84, "statistical uncertainty", size=size)

    plot.save()


def divideGraph(num, denom):
    gr = ROOT.TGraph(num)
    for i in xrange(gr.GetN()):
        y = denom.GetY()[i]
        val = 0
        if y != 0:
            val = gr.GetY()[i]/y
        gr.SetPoint(i, gr.GetX()[i], val)
    return gr

_finalstateLabels = {
    "taujets": "#tau_{h}+jets",
    "etau"   : "e#tau_{h}",
    "mutau"  : "#mu#tau_{h}",
    "emu"    : "e#mu",
}

_finalstateYmax = {
    "etau": 0.4,
    "mutau": 0.4,
    "emu": 0.8,
    "default": 0.15,
}

class BRLimits:
    def __init__(self, directory="."):
        resultfile="limits.json"
        configfile="configuration.json"

        f = open(os.path.join(directory, resultfile), "r")
        limits = json.load(f)
        f.close()

        self.lumi = float(limits["luminosity"])

        self.mass = limits["masspoints"].keys()
        members = ["mass"]

        # sort mass
        floatString = [(float(self.mass[i]), self.mass[i]) for i in range(len(self.mass))]
        floatString.sort()
        self.mass = [pair[1] for pair in floatString]

        firstMassPoint = limits["masspoints"][self.mass[0]]

        if "observed" in firstMassPoint:
            self.observed = [limits["masspoints"][m]["observed"] for m in self.mass]
            members.append("observed")
            if "observed_error" in firstMassPoint:
                self.observedError = [limits["masspoints"][m]["observed_error"] for m in self.mass]
                members.append("observedError")

        self.expectedMedian = [limits["masspoints"][m]["expected"]["median"] for m in self.mass]
        self.expectedMinus2 = [limits["masspoints"][m]["expected"]["-2sigma"] for m in self.mass]
        self.expectedMinus1 = [limits["masspoints"][m]["expected"]["-1sigma"] for m in self.mass]
        self.expectedPlus1 = [limits["masspoints"][m]["expected"]["+1sigma"] for m in self.mass]
        self.expectedPlus2 = [limits["masspoints"][m]["expected"]["+2sigma"] for m in self.mass]
        members.extend(["expected"+p for p in ["Median", "Minus2", "Minus1", "Plus1", "Plus2"]])
        if "median_error" in firstMassPoint["expected"]:
            self.expectedMedianError = [limits["masspoints"][m]["expected"]["median_error"] for m in self.mass]
            self.expectedMinus2Error = [limits["masspoints"][m]["expected"]["-2sigma_error"] for m in self.mass]
            self.expectedMinus1Error = [limits["masspoints"][m]["expected"]["-1sigma_error"] for m in self.mass]
            self.expectedPlus1Error = [limits["masspoints"][m]["expected"]["+1sigma_error"] for m in self.mass]
            self.expectedPlus2Error = [limits["masspoints"][m]["expected"]["+2sigma_error"] for m in self.mass]
            members.extend(["expected"+p+"Error" for p in ["Median", "Minus2", "Minus1", "Plus1", "Plus2"]])

        for attr in members:
            setattr(self, attr+"_string", [m for m in getattr(self, attr)])
            setattr(self, attr, [float(m) for m in getattr(self, attr)])

       

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
            self.finalstates.append("taujets")
        if hasDatacard("_etau_"):
            self.finalstates.append("etau")
        if hasDatacard("_mutau_"):
            self.finalstates.append("mutau")
        if hasDatacard("_emu_"):
            self.finalstates.append("emu")

    def getLuminosity(self):
        return self.lumi

    def getFinalstates(self):
        return self.finalstates

    def getFinalstateText(self):
        if len(self.finalstates) == 1:
            return "%s final state" % _finalstateLabels[self.finalstates[0]]

        ret = ", ".join([_finalstateLabels(x) for x in self.finalstates[:-1]])
        ret += ", and %s final states" % _finalstateLabels[self.finalstates[-1]]
        return ret

    def getFinalstateYmax(self):
        if len(self.finalstates) == 1:
            try:
                ymax = _finalstateYmax[self.finalstates[0]]
            except KeyError:
                ymax = _finalstateYmax["default"]
        else:
            ymax = _finalstateYmax["default"]
        return ymax

    def print2(self):
        print
        print "                  Expected"
        print "Mass  Observed    Median       -2sigma     -1sigma     +1sigma     +2sigma"
        format = "%3s:  %-9s   %-10s   %-10s  %-10s  %-10s  %-10s"
        for i in xrange(len(self.mass_string)):
            print format % (self.mass_string[i], self.observed_string[i], self.expectedMedian_string[i], self.expectedMinus2_string[i], self.expectedMinus1_string[i], self.expectedPlus1_string[i], self.expectedPlus2_string[i])
        print

    def observedGraph(self):
        if not hasattr(self, "observed"):
            return None

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

    def observedErrorGraph(self):
        if not hasattr(self, "observedError"):
            return None

        gr = ROOT.TGraph(len(self.mass),
                         array.array("d", self.mass),
                         array.array("d", self.observedError)
                         )
        gr.SetMarkerStyle(21)
        gr.SetMarkerSize(1.5)
        gr.SetMarkerColor(ROOT.kBlack)
        gr.SetLineWidth(3)
        gr.SetLineColor(ROOT.kBlack)
        gr.SetName("ObservedError")

        return gr

    def _expectedGraph(self, postfix, sigma):
        massArray = array.array("d", self.mass)
        massErr = array.array("d", [0]*len(self.mass))
        if sigma == 0:
            gr = ROOT.TGraph(len(self.mass), massArray, array.array("d", getattr(self, "expectedMedian"+postfix)))
            gr.SetName("Expected"+postfix)
        elif sigma == 1:
            gr = ROOT.TGraph(len(self.mass), massArray, array.array("d", getattr(self, "expectedPlus1"+postfix)))
            gr.SetName("ExpectedPlus1Sigma"+postfix)
        elif sigma == -1:
            gr = ROOT.TGraph(len(self.mass), massArray, array.array("d", getattr(self, "expectedMinus1"+postfix)))
            gr.SetName("ExpectedMinus1Sigma"+postfix)
        elif sigma == 2:
            gr = ROOT.TGraph(len(self.mass), massArray, array.array("d", getattr(self, "expectedPlus2"+postfix)))
            gr.SetName("ExpectedPlus2Sigma"+postfix)
        elif sigma == -2:
            gr = ROOT.TGraph(len(self.mass), massArray, array.array("d", getattr(self, "expectedMinus2"+postfix)))
            gr.SetName("ExpectedMinus2Sigma"+postfix)
        else:
            raise Exception("Invalid value of sigma '%d', valid values are 0,1,2" % sigma)

        gr.SetLineStyle(2)
        gr.SetLineWidth(3)
        gr.SetLineColor(ROOT.kBlack)
        gr.SetMarkerStyle(20)

        return gr

    def expectedGraph(self, sigma=0):
        return self._expectedGraph("", sigma)

    def expectedErrorGraph(self, sigma=0):
        if not hasattr(self, "expectedMedianError"):
            return None
        return self._expectedGraph("Error", sigma)

    def expectedBandGraph(self, sigma):
        massArray = array.array("d", self.mass)
        massErr = array.array("d", [0]*len(self.mass))
        if sigma == 1:
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
                                          
    # def expectedGraphNew(self, sigma=0):
    #     massArray = array.array("d", self.mass)
    #     massErr = array.array("d", [0]*len(self.mass))
    #     medianArray = array.array("d", self.expectedMedian)
    #     if sigma == 0:
    #         gr = ROOT.TGraph(len(self.mass), massArray, medianArray)
    #         gr.SetName("Expected")
    #     elif sigma == 1:
    #         gr = ROOT.TGraphAsymmErrors(len(self.mass), massArray, medianArray, massErr, massErr,
    #                                     array.array("d", [self.expectedMedian[i]-self.expectedMinus1[i] for i in xrange(len(self.mass))]),
    #                                     array.array("d", [self.expectedPlus1[i]-self.expectedMedian[i] for i in xrange(len(self.mass))]))
    #         gr.SetFillColor(ROOT.kGreen-3)
    #         gr.SetName("Expected1Sigma")
    #     elif sigma == 2:
    #         gr = ROOT.TGraphAsymmErrors(len(self.mass), massArray, medianArray, massErr, massErr,
    #                                     array.array("d", [self.expectedMedian[i]-self.expectedMinus2[i] for i in xrange(len(self.mass))]),
    #                                     array.array("d", [self.expectedPlus2[i]-self.expectedMedian[i] for i in xrange(len(self.mass))]))
    #         gr.SetFillColor(ROOT.kYellow)
    #         gr.SetName("Expected2Sigma")
    #     else:
    #         raise Exception("Invalid value of sigma '%d', valid values are 0,1,2" % sigma)

    #     gr.SetLineStyle(2)
    #     gr.SetLineWidth(3)
    #     gr.SetLineColor(ROOT.kBlack)
    #     gr.SetMarkerStyle(20)

    #     return gr


                           

if __name__ == "__main__":
    main()
