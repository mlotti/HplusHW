#!/usr/bin/env python

######################################################################
#
# Authors: Matti Kortelainen
#
######################################################################

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

# Configuration
analysis = "caloMetEfficiency"
counters = analysis+"Counters"

# main function
def main():
    # Read the datasets
    datasets = dataset.getDatasetsFromMulticrabCfg(counters=counters)
    datasets.loadLuminosities()

    datasets.mergeData()

    printEfficiencies(datasets, analysis+"/caloMet")
    
#    plots.mergeRenameReorderForDataMC(datasets)

    # Set the signal cross sections to the ttbar
    xsect.setHplusCrossSections(datasets, toTop=True)

    # Set the signal cross sections to a value from MSSM
#    xsect.setHplusCrossSections(datasets, tanbeta=20, mu=200)


    # Apply TDR style
    style = tdrstyle.TDRStyle()

    caloMet(plots.DataMCPlot(datasets, analysis+"/caloMet"))


class Eff:
    def __init__(self, all, passed, dataset):
        self.all = all
        self.passed = passed
        self.eff = passed/all
        self.eff_up = ROOT.TEfficiency.ClopperPearson(int(all), int(passed), 0.95, True)
        self.eff_down = ROOT.TEfficiency.ClopperPearson(int(all), int(passed), 0.95, False)
        self.eff_up = self.eff_up - self.eff
        self.eff_down = self.eff - self.eff_down

        a = ROOT.TH1F("hall_"+dataset.getName(), "all", 1, 0, 1)
        a.SetBinContent(1, all)
        p = ROOT.TH1F("hpassed_"+dataset.getName(), "passed", 1, 0, 1)
        p.SetBinContent(1, passed)

        self.effobj = ROOT.TEfficiency(p, a)
        self.effobj.SetStatisticOption(ROOT.TEfficiency.kFCP)
        if dataset.isMC():
            self.effobj.SetWeight(dataset.getCrossSection())

def combineEffs(effList):
    coll = ROOT.TList()
    for o in [x.effobj for x in effList]:
        coll.AddLast(o)
    gr = ROOT.TEfficiency.Combine(coll)
    return (gr.GetY()[0], gr.GetErrorYhigh(0), gr.GetErrorYlow(0))

def printEfficiencies(datasets, path):
    printEfficiency(datasets, path, 46)

def printEfficiency(datasets, path, bin):
    mc_all = 0
    mc_passed = 0
    data_all = 0
    data_passed = 0
#    mc_eff = ROOT.TEfficiency("mc", "mc", 1, 0, 1)
#    mc_eff.SetStatisticOption(ROOT.TEfficiency.kFCP)
    mc_effs = []
    for dataset in datasets.getAllDatasets():
#        print histo.getRootHisto().GetNbinsX(), histo.getXmin(), histo.getXmax()
#        hpass = histograms.dist2pass(histo.getRootHisto(), greaterThan=True)
        hpass = histograms.dist2pass(dataset.getDatasetRootHisto(path).getHistogram(), greaterThan=True)
        all = hpass.GetBinContent(1)
        passed = hpass.GetBinContent(bin)
        cutvalue = hpass.GetBinCenter(bin)
        eff = Eff(all, passed, dataset)
        print "Dataset %s, eff %f + %f - %f" % (dataset.getName(), eff.eff, eff.eff_up, eff.eff_down)
#        print all, passed, cutvalue

#        e = ROOT.TEfficiency("mc"+dataset.getName(), "mc_"+dataset.getName(), 1, 0, 1)
#        e.SetStatisticOption(ROOT.TEfficiency.kFCP)

        if dataset.isMC() and not "TTTo" in dataset.getName():
            mc_all += all
            mc_passed += passed
            mc_effs.append(eff)
        elif dataset.isData():
            data_all += all
            data_passed += passed

    mc_eff = mc_passed/mc_all
    mc_eff_up = ROOT.TEfficiency.ClopperPearson(int(mc_all), int(mc_passed), 0.95, True)
    mc_eff_down = ROOT.TEfficiency.ClopperPearson(int(mc_all), int(mc_passed), 0.95, False)
    mc_eff_up = mc_eff_up-mc_eff
    mc_eff_down = mc_eff-mc_eff_down

    (cmc_eff, cmc_eff_up, cmc_eff_down) = combineEffs(mc_effs)
    cmc_eff_err = max(cmc_eff_up, cmc_eff_down)
    
    data_eff = data_passed/data_all
    data_eff_up = ROOT.TEfficiency.ClopperPearson(int(data_all), int(data_passed), 0.95, True)
    data_eff_down = ROOT.TEfficiency.ClopperPearson(int(data_all), int(data_passed), 0.95, False)
    data_eff_up = data_eff_up-data_eff
    data_eff_down = data_eff-data_eff_down
    data_eff_err = max(data_eff_up, data_eff_down)

    rho = data_eff / cmc_eff
    rho_err = math.sqrt( (data_eff_err/cmc_eff)**2 + (data_eff*cmc_eff_err/(cmc_eff**2))**2)

    print "Cut value %f, bin %d:" % (cutvalue, bin)
#    print "  MC %f/%f = %f + %f - %f" % (mc_all, mc_passed, mc_eff, mc_eff_up, mc_eff_down)
    print "  Comb. MC %f + %f - %f" % (cmc_eff, cmc_eff_up, cmc_eff_down)
    print "  data %f/%f = %f + %f - %f" % (data_all, data_passed, data_eff, data_eff_up, data_eff_down)
    print "  rho = %f \\pm %f" % (rho, rho_err)

def caloMet(h, rebin=10):
    name = h.getRootHistoPath().replace("/", "_")

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "Calo MET (GeV/c^{2})"
    ylabel = "Events / %.0f GeV/c^{2}" % h.binWidth()
    
    h.stackMCHistograms(stackSignal=False)
    h.addMCUncertainty()

    opts = {"xmax": 400, "ymin": 1e-2, "ymaxfactor": 10}

    #h.createFrameFraction(name, opts=opts)
    h.createFrame(name, opts=opts)
    ROOT.gPad.SetLogy(True)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)

def common(h, xlabel, ylabel, addLuminosityText=True):
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    if addLuminosityText:
        h.addLuminosityText()
    h.save()

# Call the main function if the script is executed (i.e. not imported)
if __name__ == "__main__":
    main()
