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
weight = ""
#weight = "VertexWeight"
#weight = "PileupWeight"

#analysis = "caloMetEfficiency%sh00_h01_All" % weight
#afterCut = "caloMetEfficiency%sh02_h02_CaloMet45" % weight
#afterCut = "caloMetEfficiency%sh03_h02_CaloMet60" % weight
#counters = "caloMetEfficiency%scountAnalyzer/weighted" % weight
analysis = "metNtuple"
#counters = "metNtupleCounters/weighted"
counters = "metNtupleCounters"

#cutText = "Calo E_{T}^{miss} > 45 GeV"
#cutText = "Calo E_{T}^{miss} > 60 GeV"

runRegion = 1
#runRegion = 2
mcDataDefinition = True
#mcDataDefinition = False

runsData = {
    1: "165088-167913",
    2: "170722-173692",
}
runs = runsData[runRegion]

plotStyles = [
    styles.dataStyle,
    styles.mcStyle
    ]
# main function
def main():
    # Read the datasets
    datasets = dataset.getDatasetsFromMulticrabCfg(counters=counters)
    if runRegion == 1:
        datasets.remove([
                "SingleMu_Mu_170722-172619_Aug05",
                "SingleMu_Mu_172620-173198_Prompt",
                "SingleMu_Mu_173236-173692_Prompt"
                ])
    elif runRegion == 2:
        datasets.remove([
                "SingleMu_Mu_160431-163261_May10",
                "SingleMu_Mu_163270-163869_May10",
                "SingleMu_Mu_165088-166150_Prompt",
                "SingleMu_Mu_166161-166164_Prompt",
                "SingleMu_Mu_166346-166346_Prompt",
                "SingleMu_Mu_166374-167043_Prompt",
                "SingleMu_Mu_167078-167913_Prompt"
                ])
    else:
        raise Exception("Unsupported run region %d" % runRegion)

    datasets.remove([
#        "SingleMu_160431-163261_May10",
#        "SingleMu_163270-163869_May10",
#        "SingleMu_165088-166150_Prompt",
#        "SingleMu_166161-166164_Prompt",
#        "SingleMu_166346-166346_Prompt",
#        "SingleMu_166374-167043_Prompt",
#        "SingleMu_167078-167784_Prompt",
#        "SingleMu_167786-167913_Prompt_Wed",
#        "DYJetsToLL_M50_TuneZ2_Summer11",
#        "QCD_Pt20_MuEnriched_TuneZ2_Summer11",
#        "TTJets_TuneZ2_Summer11",
#        "WJets_TuneZ2_Summer11",
        ])
    datasets.loadLuminosities()

    dataNames = datasets.getDataDatasetNames()
    datasets.mergeData()

    bins = range(0, 170, 10) + [180, 200, 250, 300, 400]
    th1 = ROOT.TH1D("foo", "foo", len(bins)-1, array.array("d", bins))
    #th1 = ROOT.TH1D("foo", "foo", 40, 0, 400)

    binning=">>tmp(40,0,400)"
    #binning=binningDist
    binningEff=">>foo"
    treeDraw = dataset.TreeDraw(analysis+"/tree",
                                #weight="weightPileup",
                                varexp="pfMet.Et()"+binning)

    # Apply TDR style
    style = tdrstyle.TDRStyle()

    print "Runs", runs
    passed = treeDraw.clone(selection="caloMetNoHF.Et() > 60")
    commonText = "CaloMETnoHF > 60 GeV"
    dataText = None
    mcText = None
    if runRegion == 1:
        #printEfficienciesCalo(datasets, treeDraw.clone(varexp="caloMetNoHF.Et()"+binning))
        pass
    elif runRegion == 2:
        passedData = treeDraw.clone(selection="l1Met.Et() > 30 && caloMet.Et() > 60")
        cut = "L1 MET > 30 & CaloMET > 60 GeV"
        if mcDataDefinition:
            passed = passedData
            commonText = cut
        else:
            dataText = cut
            mcText = commonText
            tmp = {}
            for name in dataNames:
                tmp[name] = passedData

            passed = dataset.TreeDrawCompound(passed, tmp)
            #passed = dataset.TreeDrawCompound(passedData)
            #passed = passedData
        #passed = treeDraw.clone(selection="l1Met.Et() > 30 && caloMetNoHF.Et() > 60")

    printEfficienciesPF(datasets, pathAll=treeDraw.clone(), pathPassed=passed.clone(), bin=0)
    printEfficienciesPF(datasets, pathAll=treeDraw.clone(), pathPassed=passed.clone(), bin=5)
    printEfficienciesPF(datasets, pathAll=treeDraw.clone(), pathPassed=passed.clone())
    plotTurnOn(datasets,
               pathAll=treeDraw.clone(varexp="pfMet.Et()"+binningEff),
               pathPassed=passed.clone(varexp="pfMet.Et()"+binningEff),
               commonText=commonText,
               dataText=dataText,
               mcText=mcText,
               )

    #plotTurnOn(datasets, pathAll=analysis+"/pfmet_et", pathPassed=afterCut+"/pfmet_et")

    plots.mergeRenameReorderForDataMC(datasets)
    datasets.remove("TTToHplusBWB_M120")

    # Set the signal cross sections to the ttbar
#    xsect.setHplusCrossSections(datasets, toTop=True)

    # Set the signal cross sections to a value from MSSM
#    xsect.setHplusCrossSections(datasets, tanbeta=20, mu=200)

    l1Met(plots.DataMCPlot(datasets, treeDraw.clone(varexp="l1Met.Et()"+binning)), "caloMetNoHF")
    caloMet(plots.DataMCPlot(datasets, treeDraw.clone(varexp="caloMetNoHF.Et()"+binning)), "caloMetNoHF")
    caloMet(plots.DataMCPlot(datasets, treeDraw.clone(varexp="caloMet.Et()"+binning)), "caloMet")
    pfMet(plots.DataMCPlot(datasets, treeDraw.clone(varexp="pfMet.Et()"+binning)), "pfMet")

    #caloMet(plots.DataMCPlot(datasets, analysis+"/calomet_et"))
    #caloMet(plots.DataMCPlot(datasets, analysis+"/calometNoHF_et"))
    #pfMet(plots.DataMCPlot(datasets, analysis+"/pfmet_et"))


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

class HistoEff:
    def __init__(self, all, passed, dataset):
        self.effobj = ROOT.TEfficiency(passed, all)
        self.effobj.SetStatisticOption(ROOT.TEfficiency.kFCP)
        if dataset.isMC():
            self.effobj.SetWeight(dataset.getCrossSection())

def combineEffs(effList):
    gr = combineHistoEffs(effList)
    return (gr.GetY()[0], gr.GetErrorYhigh(0), gr.GetErrorYlow(0))

def combineHistoEffs(effList):
    coll = ROOT.TList()
    for o in [x.effobj for x in effList]:
        coll.AddLast(o)
    gr = ROOT.TEfficiency.Combine(coll)
    return gr

def getFromCalo(dataset, path, bin):
    hpass = histograms.dist2pass(dataset.getDatasetRootHisto(path).getHistogram(), greaterThan=True)
    all = hpass.GetBinContent(1)
    passed = hpass.GetBinContent(bin)
    cutvalue = hpass.GetBinCenter(bin)
    return (all, passed, cutvalue)

def getFromPF(dataset, pathAll, pathPassed, bin):
    hall = histograms.dist2pass(dataset.getDatasetRootHisto(pathAll).getHistogram(), greaterThan=True)
    hpassed= histograms.dist2pass(dataset.getDatasetRootHisto(pathPassed).getHistogram(), greaterThan=True)
    all = hall.GetBinContent(bin)
    passed = hpassed.GetBinContent(bin)
    cutvalue = hpassed.GetBinCenter(bin)
    if abs(cutvalue-hall.GetBinCenter(bin)) > 1e-4:
        raise Exception("Internal error, cutvalue %f, hall.GetBinCenter(bin) %f" % (cutvalue, hall.GetBinCenter(bin)))
    return (all, passed, cutvalue)

def printEfficienciesCalo(datasets, path):
    print "Efficiencies of calo MET > 60 cut"
    #bin = 61
    bin = 7
    printEfficiency(datasets, bin, lambda d, b: getFromCalo(d, path, b))
    print

def printEfficienciesPF(datasets, pathAll, pathPassed, bin=8):
    print "Efficiencies in a certain PF MET region"
    #bin = 71
    printEfficiency(datasets, bin, lambda d, b: getFromPF(d, pathAll, pathPassed, b))
    print

def printEfficiency(datasets, bin, function):
    backup = ROOT.gErrorIgnoreLevel
    ROOT.gErrorIgnoreLevel = ROOT.kError

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

#        hpass = histograms.dist2pass(dataset.getDatasetRootHisto(path).getHistogram(), greaterThan=True)
#        all = hpass.GetBinContent(1)
#        passed = hpass.GetBinContent(bin)
#        cutvalue = hpass.GetBinCenter(bin)
        (all, passed, cutvalue) = function(dataset, bin)
        eff = Eff(all, passed, dataset)
        print "Dataset %-35s, eff %f + %f - %f" % (dataset.getName(), eff.eff, eff.eff_up, eff.eff_down)
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
    print "  scale factor = %f \\pm %f" % (rho, rho_err)

    ROOT.gErrorIgnoreLevel = backup

class PlotTurnOn(plots.PlotBase):
    def __init__(self):
        plots.PlotBase.__init__(self, [])

    def addGraph(self, gr, name):
        self.histoMgr.appendHisto(histograms.HistoGraph(gr, name, "p", "P"))
    def finalize(self):
        self.histoMgr.forEachHisto(styles.generator2(styles.StyleMarker(markerSize=1.5), plotStyles))

def plotTurnOn(datasets, pathAll, pathPassed, commonText, dataText=None, mcText=None, rebin=1):
    dataLabel = "Data"
    mcLabel = "Simulation"
    if dataText != None and mcText == None:
        raise Exception("mcText must not be None when dataText is not")
    if dataText == None and mcText != None:
        raise Exception("dataText must not be None when mcText is not")
    if dataText != None:
        dataLabel += ": "+dataText
        mcLabel += ": "+mcText

    mc_effs = []
    data_eff_gr = None
    binWidth = None
    luminosity = 0
    for dataset in datasets.getAllDatasets():
        all = dataset.getDatasetRootHisto(pathAll).getHistogram()
        passed = dataset.getDatasetRootHisto(pathPassed).getHistogram()

        if rebin > 1:
            all.Rebin(rebin)
            passed.Rebin(rebin)
        binWidth = all.GetBinWidth(1)

        if dataset.isMC() and not "TTTo" in dataset.getName():
        #if dataset.isMC() and not "TTTo" in dataset.getName() and not "QCD" in dataset.getName():
        #if dataset.isMC() and "QCD" in dataset.getName():
            mc_effs.append(HistoEff(all, passed, dataset))

        elif dataset.isData():
            data_eff_gr = ROOT.TGraphAsymmErrors(passed, all, "cp")
            luminosity += dataset.getLuminosity()

    mc_eff_gr = combineHistoEffs(mc_effs)

    p = plots.ComparisonPlot(
        histograms.HistoGraph(data_eff_gr, "Data", "p", "P"),
        histograms.HistoGraph(mc_eff_gr, "Simulation", "p", "P")
        )
    p.histoMgr.forEachHisto(styles.generator2(styles.StyleMarker(markerSize=1.5), plotStyles))
    p.histoMgr.setHistoLegendLabelMany({
            "Data": dataLabel,
            "Simulation": mcLabel,
            })
    p.setLuminosity(luminosity)
    #p.addGraph(data_eff_gr, "Data")
    #p.addGraph(mc_eff_gr, "Simulation")
    #p.finalize()

    opts = {"ymin": 0.0, "ymax": 1.1}
    opts2 = {"ymin": 0.5, "ymax": 1.5}

    name = "calomet_turnon_"+runs
    if not mcDataDefinition:
        name += "_McSummer11"
    
    p.createFrame(name, createRatio=True, opts=opts, opts2=opts2)
    p.setLegend(histograms.moveLegend(histograms.createLegend(y1=0.95, y2=0.85),
                                      #dx=-0.55, dy=-0.05
                                      dx=-0.44, dy=-0.58
                                      ))

    def text():
        l = ROOT.TLatex()
        l.SetNDC()
#        l.SetTextFont(l.GetTextFont()-20) # bold -> normal
        l.SetTextSize(l.GetTextSize()*0.65)
        #l.DrawLatex(0.35, 0.4, commonText)
        l.DrawLatex(0.48, 0.32, commonText)
    textFunction = text
    if dataText != None:
        textFunction = None
    common(p, "PF E_{T}^{miss} (GeV)", "Efficiency / %.0f GeV"%binWidth, afterDraw=textFunction)

def l1Met(h, name, rebin=1):
    plotMet(h, name, "L1 MET (GeV)", rebin)

def caloMet(h, name, rebin=1):
    plotMet(h, name, "Calo MET (GeV)", rebin)

def pfMet(h, name, rebin=1):
    plotMet(h, name, "PF MET (GeV)", rebin)

def plotMet(h, name, xlabel, rebin):
    if rebin > 1:
        h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))

    ylabel = "Events / %.0f GeV" % h.binWidth()

    h.stackMCHistograms(stackSignal=False)
    h.addMCUncertainty()

    opts = {"ymin": 1e-2, "ymaxfactor": 10}

    #h.createFrameFraction(name, opts=opts)
    h.createFrame(name+"_"+runs, opts=opts)
    ROOT.gPad.SetLogy(True)
    h.setLegend(histograms.moveLegend(histograms.createLegend(), dx=-0.12))
    common(h, xlabel, ylabel)

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
