#!/usr/bin/env python

import math

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect

analysis = "signalAnalysis"
counters = analysis+"Counters/weighted"

styles.signal80Style.append(styles.StyleLine(lineColor=ROOT.kRed+2))
styles.signal90Style.append(styles.StyleLine(lineColor=ROOT.kGreen+2))
styles.signal100Style.append(styles.StyleLine(lineColor=ROOT.kCyan+2))
styles.signal140Style.append(styles.StyleLine(lineColor=ROOT.kBlue+2))
styles.signal150Style.append(styles.StyleLine(lineColor=ROOT.kMagenta+2))
styles.signal155Style.append(styles.StyleLine(lineColor=ROOT.kViolet+2))
styles.signal160Style.append(styles.StyleLine(lineColor=ROOT.kAzure+2))

def main():
    datasets = dataset.getDatasetsFromMulticrabCfg(counters=counters)

    # remove data datasets
    datasets.remove(filter(lambda name: "Tau_" in name, datasets.getAllDatasetNames()))
    # remove heavy H+ datasets
    datasets.remove(filter(lambda name: "HplusTB" in name, datasets.getAllDatasetNames()))

    plots.mergeRenameReorderForDataMC(datasets)
    xsect.setHplusCrossSectionsToBR(datasets, br_tH=0.05, br_Htaunu=1)
    plots.mergeWHandHH(datasets) # merging of WH and HH signals must be done after setting the cross section

    # Apply TDR style
    style = tdrstyle.TDRStyle()

    # Define variables and cuts
    tauPt = "tau_p4.Pt()"; tauPtCut = tauPt+" > 40"
    tauLeadingCandPt = "tau_leadPFChargedHadrCand_p4.Pt()"; tauLeadingCandPtCut = tauLeadingCandPt+" > 20"

    met = "met_p4.Et()"; metCut = met+" > 70"

    btagMax = "Max$(jets_btag)"; btagCut = btagMax+" > 1.7"
    btagJetNum17 = "Sum$(jets_btag > 1.7"
    btag2ndMax = "MaxIf(kets_btag, jets_btag < Max$(jets_btag))"

    rtau = "tau_leadPFChargedHadrCand_p4.P()/tau_p4.P()"; rtauCut = rtau+" > 0.65"
    mt = "sqrt(2 * tau_p4.Pt() * met_p4.Et() * (1-cos(tau_p4.Phi()-met_p4.Phi())))"; mtCut = mt+" > 80"
    deltaPhi = "acos((tau_p4.Px()*met_p4.Px()+tau_p4.Py()*met_p4.Py())/tau_p4.Pt()/met_p4.Et())*57.2958"; deltaPhiCut = deltaPhi+" < 160"

    npv = "goodPrimaryVertices_n";

    td = dataset.TreeDraw(analysis+"/tree", weight="weightPileup*weightTrigger*weightPrescale")
    lumi = 1145

    def createResult(varexp, selection, weight=None, **kwargs):
        args = {"varexp": varexp, "selection": selection}
        if weight != None:
            args["weight"] = weight
        return Result(datasets, td.clone(**args), normalizeToLumi=lumi, **kwargs)

    # metRes = createResult(met+">>dist(100,0,200)", btagCut, greaterThan=True)
    # metRes.save("met", "MET (GeV)", rebin=10, logy=True, opts={"ymin": 0.01, "ymaxfactor": 10})

    # btagRes = createResult(btagMax+">>dist(80, 0, 8)", metCut, greaterThan=True)
    # btagRes.save("btag", "TCHE", rebin=5, logy=True, opts={"ymin": 0.01, "ymaxfactor": 10})

    # rtauRes = createResult(rtau+">>dist(110,0,1.1)", metCut+"&&"+btagCut, greaterThan=True)
    # rtauRes.save("rtau", "R_{#tau}", rebin=10, logy=True, opts={"ymin": 0.01, "ymaxfactor": 10})

    # mtRes = createResult(mt+">>dist(50,0,200)", metCut+"&&"+btagCut, greaterThan=True)
    # mtRes.save("mt", "M_{T}(#tau, MET) (GeV)", rebin=2, logy=True, opts={"ymin": 0.01, "ymaxfactor": 10})

    # deltaPhiRes = createResult(deltaPhi+">>dist(90,0,180)", metCut+"&&"+btagCut, lessThan=True)
    # deltaPhiRes.save("deltaPhi", "#Delta#Phi(#tau, MET) (#circ)", rebin=5, logy=True, opts={"ymin": 0.01, "ymaxfactor": 10})

    pileupRes = createResult(npv+">>dist(4,1,17)", metCut+"&&"+btagCut, weight="", doPassed=False, lessThan=True)
    pileupRes.save("goodPV", "N(good primary vertices)")

def significancePoisson(signal, background):
    s = 0
    if background > 0:
        s = math.sqrt(2*((signal+background)*math.log(1+signal/background)-signal))
    return s

class Result:
    def __init__(self, datasets, treeDraw, doPassed=True, **kwargs):
        argsPlot = {}
        argsPass = {}
        for key in kwargs.keys():
            if "normalize" in key:
                argsPlot[key] = kwargs[key]
            elif "Than" in key:
                argsPass[key] = kwargs[key]
            else:
                raise Exception("Unsupported keyword argument %s" % key)

        self.doPassed = doPassed
        self.dist = plots.MCPlot(datasets, treeDraw, **argsPlot)
        self.passed = plots.PlotBase()
        self.sOverB = plots.PlotBase()
        self.significance = plots.PlotBase()

        signalsToRemove = filter(lambda name: plots.isSignal(name) and not "_M120" in name, datasets.getMCDatasetNames())

        # Create the passed (cumulative) histogram
        sumBkgDist = None
        sumBkgPassed = None
        for histo in self.dist.histoMgr.getHistos():
            dist = histo.getRootHisto()
            passed = histograms.dist2pass(dist, **argsPass)
            self.passed.histoMgr.appendHisto(histograms.HistoWithDataset(histo.getDataset(),
                                                              passed,
                                                              histo.getName()))
            if not plots.isSignal(histo.getDataset().getName()):
                if sumBkgDist == None:
                    sumBkgDist = dist.Clone("bkgsum")
                    sumBkgPassed = passed.Clone("bkgsum")
                else:
                    sumBkgDist.Add(dist)
                    sumBkgPassed.Add(passed)

        sumBkg = sumBkgDist
        histos = self.dist.histoMgr.getHistos()
        if doPassed:
            histos = self.passed.histoMgr.getHistos()
            symBkg = symBkgPassed

        # Create S/B histogram
        for histo in histos:
            if plots.isSignal(histo.getDataset().getName()):
                signal = histo.getRootHisto()
                sOverB = signal.Clone("sOverB_"+histo.getName())
                sOverB.Divide(sumBkg)
                self.sOverB.histoMgr.appendHisto(histograms.HistoWithDataset(histo.getDataset(), sOverB, histo.getName()))

                signif = signal.Clone("significance_"+histo.getName())
                for bin in xrange(0, signif.GetNbinsX()+2):
                    signif.SetBinContent(bin, significancePoisson(signif.GetBinContent(bin), sumBkg.GetBinContent(bin)))
                self.significance.histoMgr.appendHisto(histograms.HistoWithDataset(histo.getDataset(), signif, histo.getName()))

        # Format passed and dist
        self.passed.setDefaultStyles()
        mcNames = filter(lambda name: not plots.isSignal(name), datasets.getMCDatasetNames())
        self.passed.histoMgr.forEachHisto(plots.UpdatePlotStyleFill(plots._plotStyles, mcNames))
        self.passed.histoMgr.stackHistograms("StackedMC", mcNames)

        for s in signalsToRemove:
            self.dist.histoMgr.removeHisto(s)
            self.passed.histoMgr.removeHisto(s)

        # Format S/B
        for plot in [self.sOverB, self.significance]:
            plot.setDefaultStyles()
            plot.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetLineStyle(ROOT.kSolid))
            plot.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetLineWidth(2))

    def _common(self, h, name, xlabel, ylabel, logy=False, opts={}):
        _opts = {}
        _opts.update(opts)
        h.createFrame(name, opts=_opts)
        h.getPad().SetLogy(logy)
        h.setLegend(histograms.createLegend())
        h.frame.GetXaxis().SetTitle(xlabel)
        h.frame.GetYaxis().SetTitle(ylabel)
        h.draw()
        h.save()

    def save(self, name, xlabel, rebin=1, logy=False, opts={}):
        self.dist.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
        self.dist.stackMCHistograms()
        self._common(self.dist, name+"_dist", xlabel, "Events", logy, opts)

        self._common(self.passed, name+"_cumulative", "Cut on "+xlabel, "Passed events", logy, opts)

        xlab = xlabel
        if self.doPassed:
            xlab = "Cut on "+xlabel

        self._common(self.sOverB, name+"_sOverB", xlab, "Signal / Background")

        self._common(self.significance, name+"_significance", xlab, "Significance")

if __name__ == "__main__":
    main()
