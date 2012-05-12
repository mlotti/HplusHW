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
    doObservedError(limits)
    doExpectedError(limits)

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

    ymax = 0.15
    finalStates = limits.getFinalstates()
    if len(finalStates) == 1:
        if finalStates[0] in ["#mu#tau", "e#tau"]:
            ymax = 0.4
        elif finalStates[0] == "e#mu":
            ymax = 0.8            

    plot.createFrame("limitsBr", opts={"ymin": 0, "ymax": ymax})
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

def doObservedError(limits):
    obs = limits.observedGraph()
    if obs == None:
        return
    obsErr = limits.observedErrorGraph()
    if obsErr == None:
        return

    relErr = divideGraph(obsErr, obs)
    plot = plots.PlotBase([histograms.HistoGraph(relErr, "ObsRelErr", drawStyle="PL")])

    plot.createFrame("limitsBrObservedRelError", opts={"ymin": 0, "ymaxfactor": 1.5})
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

def doExpectedError(limits):
    order = [0, 1, -1, 2, -2]

    expErrors = [limits.expectedErrorGraph(sigma=s) for s in order]
    if expErrors[0] == None:
        return
    exps = [limits.expectedGraph(sigma=s) for s in order]

    relErrors = [divideGraph(expErrors[i], exps[i]) for i in xrange(len(exps))]

    plot = plots.PlotBase([histograms.HistoGraph(relErrors[i], "ExpRelErr%d"%i, drawStyle="PL", legendStyle="lp") for i in xrange(len(exps))])

    plot.histoMgr.setHistoLegendLabelMany({
            "ExpRelErr0": "Median",
            "ExpRelErr1": "+1#sigma",
            "ExpRelErr2": "-1#sigma",
            "ExpRelErr3": "+2#sigma",
            "ExpRelErr4": "-2#sigma",
            })
    plot.setLegend(histograms.moveLegend(histograms.createLegend(0.48, 0.75, 0.85, 0.92), dx=0.1, dy=-0.1))

    plot.histoMgr.forEachHisto(styles.generator())
    def sty(h):
        r = h.getRootHisto()
        r.SetLineStyle(1)
        r.SetLineWidth(3)
        r.SetMarkerSize(1.4)
    plot.histoMgr.forEachHisto(sty)

    plot.createFrame("limitsBrExpectedRelError", opts={"ymin": 0, "ymaxfactor": 1.5})
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
        gr.SetPoint(i, gr.GetX()[i], gr.GetY()[i]/denom.GetY()[i])
    return gr

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
