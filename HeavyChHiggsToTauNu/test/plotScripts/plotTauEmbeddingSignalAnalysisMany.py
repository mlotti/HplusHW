#!/usr/bin/env python

######################################################################
#
# This plot script is for comparing the embedded data to embedded MC
# within the signal analysis. The corresponding python job
# configurations are
# * signalAnalysis_cfg.py with "doPat=1 tauEmbeddingInput=1"
# * signalAnalysis_cfg.py
# for embedding+signal analysis and signal analysis, respectively
#
# Authors: Matti Kortelainen
#
######################################################################

import os
import array
import math

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.cutstring import * # And, Not, Or
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tauEmbedding as tauEmbedding
import produceTauEmbeddingResult as result
import plotTauEmbeddingSignalAnalysis as tauEmbeddingPlot

#analysisEmb = "signalAnalysis"
#analysisEmb = "signalAnalysisCaloMet60"
analysisEmb = "signalAnalysisCaloMet60TEff"
analysisSig = "signalAnalysisGenuineTau"

counters = "Counters/weighted"
#counters = "Counters"

weight = "weightPileup*weightTrigger"
weightBTagging = weight+"*weightBTagging"
treeDraw = dataset.TreeDraw(analysisEmb+"/tree", weight=weight)

caloMetCut = "(tecalomet_p4.Et() > 60)"
caloMetNoHFCut = "(tecalometNoHF_p4.Et() > 60)"
metCut = "(met_p4.Et() > 50)"
bTaggingCut = "passedBTagging"
deltaPhi160Cut = "(acos( (tau_p4.Px()*met_p4.Px()+tau_p4.Py()*met_p4.Py())/(tau_p4.Pt()*met_p4.Et()) )*57.3 <= 160)"
deltaPhi130Cut = "(acos( (tau_p4.Px()*met_p4.Px()+tau_p4.Py()*met_p4.Py())/(tau_p4.Pt()*met_p4.Et()) )*57.3 <= 130)"
deltaPhi90Cut = "(acos( (tau_p4.Px()*met_p4.Px()+tau_p4.Py()*met_p4.Py())/(tau_p4.Pt()*met_p4.Et()) )*57.3 <= 90)"

def main():
    dirEmbs = ["."] + [os.path.join("..", d) for d in tauEmbedding.dirEmbs[1:]]
    dirSig = "../"+tauEmbedding.dirSig
  
    datasetsEmb = tauEmbedding.DatasetsMany(dirEmbs, analysisEmb+"Counters", normalizeMCByLuminosity=True)
    datasetsSig = dataset.getDatasetsFromMulticrabCfg(cfgfile=dirSig+"/multicrab.cfg", counters=analysisSig+"Counters")
    datasetsSig.updateNAllEventsToPUWeighted()

    datasetsEmb.remove(filter(lambda name: "HplusTB" in name, datasetsEmb.getAllDatasetNames()))
    datasetsEmb.remove(filter(lambda name: "TTToHplus" in name, datasetsEmb.getAllDatasetNames()))

    del plots._datasetMerge["WW"]
#    del plots._datasetMerge["WZ"]
#    del plots._datasetMerge["ZZ"]

    datasetsEmb.forEach(plots.mergeRenameReorderForDataMC)
    datasetsEmb.setLumiFromData()
    plots.mergeRenameReorderForDataMC(datasetsSig)

    style = tdrstyle.TDRStyle()
    histograms.createLegend.moveDefaults(dx=-0.04)
    datasetsEmb.remove(["W3Jets"])
    datasetsEmb.remove(["QCD_Pt20_MuEnriched"])
    #plots._legendLabels["QCD_Pt20_MuEnriched"] = "QCD"
    histograms.createLegend.moveDefaults(dh=-0.05)
    #histograms.createLegend.moveDefaults(dx=-0.18, dy=0.05, dh=-0.05)

    tauEmbedding.normalize=True
    #tauEmbedding.normalize=False
    tauEmbedding.era = "Run2011A"

    def mergeEWK(datasets):
        datasets.merge("EWKMC", ["WJets", "TTJets", "DYJetsToLL", "SingleTop", "Diboson", "WW"], keepSources=True)
        #datasets.merge("EWKMC", ["WJets", "TTJets"], keepSources=True)
    mergeEWK(datasetsSig)
    datasetsEmb.forEach(mergeEWK)

    datasetsEmbCorrected = result.DatasetsDYCorrection(datasetsEmb, datasetsSig, analysisEmb, analysisSig)
    datasetsResidual = tauEmbedding.DatasetsResidual(datasetsEmb, datasetsSig, analysisEmb, analysisSig, ["DYJetsToLL", "WW"], totalNames=["Data", "EWKMC"])

#    doPlots(datasetsEmb)
    #doPlots(datasetsEmbCorrected)
#    doPlotsWTauMu(datasetsEmb, "TTJets", True)
#    doPlotsWTauMu(datasetsEmb, "TTJets", False)

#    doCounters(datasetsEmb)
    #doCounters(datasetsEmbCorrected)

    doCountersResidual(datasetsResidual)

    #doCountersOld(datasetsEmb)

def doPlotsWTauMu(datasetsEmb, name, btag=True):
    
    if btag:
        selection = And(metCut, bTaggingCut, deltaPhi130Cut)
        treeDraw = dataset.TreeDraw(analysisEmb+"/tree", weight="weightPileup*weightTrigger*weightBTagging")
    else:
        selection = And(metCut, deltaPhi130Cut)
        treeDraw = dataset.TreeDraw(analysisEmb+"/tree", weight="weightPileup*weightTrigger")
    tdMt = treeDraw.clone(varexp="sqrt(2 * tau_p4.Pt() * met_p4.Et() * (1-cos(tau_p4.Phi()-met_p4.Phi()))) >>tmp(20,0,400)")

    (hall, tmp) = datasetsEmb.getHistogram(name, tdMt.clone(selection=selection))
    (hpure, tmp) = datasetsEmb.getHistogram(name, tdMt.clone(selection=And(selection, "abs(temuon_mother_pdgid) == 24")))

    tdEff = tdMt.clone(weight="", varexp=tdMt.varexp.replace("tmp", "tmpeff"))
    heff = datasetsEmb.getEfficiency(name, tdEff.clone(selection=And(selection, "abs(temuon_mother_pdgid) == 24")), tdEff.clone(selection=selection))

    hall.SetName("All")
    hpure.SetName("Pure")

    nall = hall.Integral(0, hall.GetNbinsX())
    npure = hpure.Integral(0, hall.GetNbinsX())

    print {True: "Btagging", False: "NoBTag"}[btag], npure/nall, (1-npure/nall)*100

    p = plots.ComparisonPlot(hall, hpure)
    p.histoMgr.setHistoLegendLabelMany({
            "All": "All muons",
            "Pure": "W#rightarrow#mu"
            })
    p.histoMgr.forEachHisto(styles.generator())
    if btag:
        fname = "transverseMass_4AfterDeltaPhi160_wtaumu_"+name
    else:
        fname = "transverseMass_4AfterDeltaPhi160NoBTag_wtaumu_"+name

    hallErr = hall.Clone("AllError")
    hallErr.SetFillColor(ROOT.kBlue-7)
    hallErr.SetFillStyle(3004)
    hallErr.SetMarkerSize(0)
    p.prependPlotObject(hallErr, "E2")

    hpureErr = hpure.Clone("PureErr")
    hpureErr.SetFillColor(ROOT.kRed-7)
    hpureErr.SetFillStyle(3005)
    hpureErr.SetMarkerSize(0)
    p.prependPlotObject(hpureErr, "E2")

    p.createFrame(fname, createRatio=True, opts2={"ymin": 0.9, "ymax": 1.05})
    styles.getDataStyle().apply(heff)
    p.setRatios([heff])
    xmin = p.frame.GetXaxis().GetXmin()
    xmax = p.frame.GetXaxis().GetXmax()
    val = 1-0.038479
    l = ROOT.TLine(xmin, val, xmax, val)
    l.SetLineWidth(2)
    l.SetLineColor(ROOT.kBlue)
    l.SetLineStyle(4)
    p.prependPlotObjectToRatio(l)
    p.appendPlotObjectToRatio(histograms.PlotText(0.65, 0.61, "1-0.038", size=18, color=ROOT.kBlue))
    p.getFrame2().GetYaxis().SetTitle("W#rightarrow#mu fraction")

    p.setLegend(histograms.moveLegend(histograms.createLegend()))
    tmp = hpureErr.Clone("tmp")
    tmp.SetFillColor(ROOT.kBlack)
    tmp.SetFillStyle(3013)
    tmp.SetLineColor(ROOT.kWhite)
    p.legend.AddEntry(tmp, "Stat. unc.", "F")

    p.frame.GetXaxis().SetTitle("m_{T}(#tau jet, E_{T}^{miss}) (GeV/c^{2})")
    p.frame.GetYaxis().SetTitle("Events / %.0f GeV/c^{2}" % p.binWidth())
    p.appendPlotObject(histograms.PlotText(0.5, 0.9, plots._legendLabels.get(name, name), size=18))
    p.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    p.save()

def drawPlot(*args, **kwargs):
    tauEmbedding.drawPlot(normalize=False, *args, **kwargs)

def doPlots(datasetsEmb):
    datasetNames = datasetsEmb.getAllDatasetNames()
    isCorrected = isinstance(datasetsEmb, result.DatasetsDYCorrection)

    def createPlot(name, dyx=0.67, dyy=0.64):
        name2 = name
        if isinstance(name, basestring):
            name2 = analysisEmb+"/"+name

        rootHistos = []
        for datasetName in datasetNames:
            (histo, tmp) = datasetsEmb.getHistogram(datasetName, name2)
            histo.SetName(datasetName)
            rootHistos.append(histo)

        p = plots.DataMCPlot2(rootHistos)
        histos = p.histoMgr.getHistos()
        for h in histos:
            if h.getName() == "Data":
                h.setIsDataMC(True, False)
            else:
                h.setIsDataMC(False, True)
        p.setLuminosity(datasetsEmb.getLuminosity())
        p.setDefaultStyles()
        if isCorrected:
            p.appendPlotObject(histograms.PlotText(dyx, dyy, "DY correction applied", size=15))
        return p


    prefix = "embdatamc_"
    opts2 = {"ymin": 0, "ymax": 2}
    # Control plots
    def drawControlPlot(path, xlabel, **kwargs):
        drawPlot(createPlot("ControlPlots/"+path), prefix+path, xlabel, opts2=opts2, **kwargs)

    drawControlPlot("SelectedTau_pT_AfterStandardSelections", "#tau-jet p_{T} (GeV/c)", opts={"xmax": 250}, rebin=2, cutBox={"cutValue": 40, "greaterThan": True})
    drawControlPlot("SelectedTau_eta_AfterStandardSelections", "#tau-jet #eta", opts={"xmin": -2.2, "xmax": 2.2}, ylabel="Events / %.1f", rebin=4, moveLegend={"dy":-0.52, "dx":-0.2})
    drawControlPlot("SelectedTau_phi_AfterStandardSelections", "#tau-jet #phi", rebin=10, ylabel="Events / %.2f")
    drawControlPlot("SelectedTau_LeadingTrackPt_AfterStandardSelections", "#tau-jet ldg. charged particle p_{T} (GeV/c)", opts={"xmax": 250}, rebin=2, cutBox={"cutValue": 20, "greaterThan": True})
    drawControlPlot("SelectedTau_Rtau_AfterStandardSelections", "R_{#tau} = p^{ldg. charged particle}/p^{#tau jet}", opts={"xmin": 0.65, "xmax": 1.05, "ymin": 1e-1, "ymaxfactor": 10}, rebin=5, ylabel="Events / %.2f", moveLegend={"dx":-0.4, "dy": 0.01, "dh": -0.03}, cutBox={"cutValue":0.7, "greaterThan":True})
    #drawControlPlot("SelectedTau_p_AfterStandardSelections", "#tau-jet p (GeV/c)", rebin=2)
    #drawControlPlot("SelectedTau_LeadingTrackP_AfterStandardSelections", "#tau-jet ldg. charged particle p (GeV/c)", rebin=2)
    #drawControlPlot("IdentifiedElectronPt_AfterStandardSelections", "Electron p_{T} (GeV/c)")
    #drawControlPlot("IdentifiedMuonPt_AfterStandardSelections", "Muon p_{T} (GeV/c)")
    #drawControlPlot("Njets_AfterStandardSelections", "Number of jets", ylabel="Events")

    drawControlPlot("MET", "Uncorrected PF E_{T}^{miss} (GeV)", rebin=5, opts={"xmax": 400}, cutLine=50)
    # After MET
    drawControlPlot("NBjets", "Number of selected b jets", opts={"xmax": 6}, ylabel="Events", cutLine=1)

    treeDraw = dataset.TreeDraw(analysisEmb+"/tree", weight="weightPileup*weightTrigger")
    tdMet = treeDraw.clone(varexp="met_p4.Phi() >> tmp(16, -3.2, 3.2)")
    drawPlot(createPlot(tdMet.clone()), prefix+"METPhi_1AfterTauID", "\MET #phi", log=False, ylabel="Events / %.1f", opts={"ymaxfactor": 2}, opts2={"ymin": 0, "ymax": 2})


    # After b-tagging
    treeDraw = treeDraw.clone(weight="weightPileup*weightTrigger*weightBTagging")
    tdMt = treeDraw.clone(varexp="sqrt(2 * tau_p4.Pt() * met_p4.Et() * (1-cos(tau_p4.Phi()-met_p4.Phi()))) >>tmp(20,0,400)")
    tdDeltaPhi = treeDraw.clone(varexp="acos( (tau_p4.Px()*met_p4.Px()+tau_p4.Py()*met_p4.Py())/(tau_p4.Pt()*met_p4.Et()) )*57.3 >>tmp(18, 0, 180)")

    metCut = "(met_p4.Et() > 50)"
    bTaggingCut = "passedBTagging"
    deltaPhi160Cut = "(acos( (tau_p4.Px()*met_p4.Px()+tau_p4.Py()*met_p4.Py())/(tau_p4.Pt()*met_p4.Et()) )*57.3 <= 160)"
    deltaPhi130Cut = "(acos( (tau_p4.Px()*met_p4.Px()+tau_p4.Py()*met_p4.Py())/(tau_p4.Pt()*met_p4.Et()) )*57.3 <= 130)"

    # DeltapPhi
    def customDeltaPhi(h):
        yaxis = h.getFrame().GetYaxis()
        yaxis.SetTitleOffset(0.8*yaxis.GetTitleOffset())
    drawPlot(createPlot(tdDeltaPhi.clone(selection=And(metCut, bTaggingCut))), prefix+"deltaPhi_3AfterBTagging", "#Delta#phi(#tau jet, E_{T}^{miss}) (^{o})", log=False, opts={"ymax": 30}, opts2=opts2, ylabel="Events / %.0f^{o}", function=customDeltaPhi, moveLegend={"dx": -0.22}, cutLine=[130, 160])

    # mT
    for name, label, selection in [
        ("3AfterBTagging", "Without #Delta#phi(#tau jet, E_{T}^{miss}) cut", [metCut, bTaggingCut]),
        ("4AfterDeltaPhi160", "#Delta#phi(#tau jet, E_{T}^{miss}) < 160^{o}", [metCut, bTaggingCut, deltaPhi160Cut]),
        ("5AfterDeltaPhi130", "#Delta#phi(#tau jet, E_{T}^{miss}) < 130^{o}", [metCut, bTaggingCut, deltaPhi130Cut])]:

        p = createPlot(tdMt.clone(selection=And(*selection)))
        h = p.histoMgr.getHisto("Data").getRootHisto()
        s = ""
        for bin in xrange(1, h.GetNbinsX()+1):
            val = h.GetBinContent(bin)
            err = h.GetBinError(bin)
            if val != 0:
                s += "%.2f " % (err/val*100)
            else:
                s += "0 "
        print "%s rel. stat. unc. %s" % (name, s)
                
        p.appendPlotObject(histograms.PlotText(0.5, 0.62, label, size=20))
        drawPlot(p, prefix+"transverseMass_"+name, "m_{T}(#tau jet, E_{T}^{miss}) (GeV/c^{2})", opts={"ymax": 32}, opts2=opts2, ylabel="Events / %.0f GeV/c^{2}", log=False)

    return

    prefix = "avg10"
    if isCorrected:
        prefix += "_dycorrected"

    
    opts2 = {"ymin": 0, "ymax": 3}

    drawPlot(createPlot(treeDraw.clone(varexp="tau_p4.Pt() >>tmp(20,0,200)", selection=selection)), prefix+"_selectedTauPt_4AfterDeltaPhi160", "#tau-jet p_{T} (GeV/c)", opts2=opts2)
    drawPlot(createPlot(treeDraw.clone(varexp="met_p4.Pt() >>tmp(16,0,400)", selection=selection)), prefix+"_MET_4AfterDeltaPhi160", "E_{T}^{miss} (GeV)", ylabel="Events / %.0f GeV", opts2=opts2)

    #opts = {"ymaxfactor": 1.2}
    opts = {"ymax": 40}
    p = createPlot(tdMt.clone(selection=selection))
    addAN = False
    if addAN:
        mtAN = ROOT.TH1F("mt_AN", "mt_AN", 20, 0, 400)
        mtAN.SetDirectory(0)
        mtAN.SetBinContent(1,27.70106)
        mtAN.SetBinContent(2,15.93031)
        mtAN.SetBinContent(3,11.06969)
        mtAN.SetBinContent(4,4.613092)
        mtAN.SetBinContent(5,5.13239)
        mtAN.SetBinContent(6,3.998591)
        mtAN.SetBinContent(7,1.497308)
        mtAN.SetBinContent(9,0.7270167)
        mtAN.SetBinError(1,5.035656)
        mtAN.SetBinError(2,3.771818)
        mtAN.SetBinError(3,3.058925)
        mtAN.SetBinError(4,2.107709)
        mtAN.SetBinError(5,2.15077)
        mtAN.SetBinError(6,2.023928)
        mtAN.SetBinError(7,1.090971)
        mtAN.SetBinError(9,0.7270168)
        styles.mcStyle2.apply(mtAN)
        h = histograms.Histo(mtAN, "Data in AN v4", "p", "EP")
        h.setIsDataMC(False, False)
        p.histoMgr.insertHisto(1, h, legendIndex=1)
        p.setDataDatasetNames(["Data", h.getName()])
    drawPlot(p, prefix+"_transverseMass_4AfterDeltaPhi160", "m_{T}(#tau jet, E_{T}^{miss}) (GeV/c^{2})", opts=opts, opts2=opts2, ylabel="Events / %.0f GeV/c^{2}", log=False)
            

def doCounters(datasetsEmb):
    isCorrected = isinstance(datasetsEmb, result.DatasetsDYCorrection)
    if isCorrected:
        eventCounter = result.EventCounterDYCorrection(datasetsEmb, counters=analysisEmb+counters)
    else:
        scaleNormalization = analysisEmb != "signalAnalysis"
        eventCounter = tauEmbedding.EventCounterMany(datasetsEmb, counters=analysisEmb+counters, normalize=scaleNormalization)

    # Add counts
    sels = []
    tdCount = treeDraw.clone(weight=weightBTagging)
    tdCountMET = tdCount.clone(weight=weight, selection="&&".join(sels+[metCut]))
    tdCountBTagging = tdCount.clone(selection="&&".join(sels+[metCut, bTaggingCut]))
    tdCountDeltaPhi160 = tdCount.clone(selection="&&".join(sels+[metCut, bTaggingCut, deltaPhi160Cut]))
    tdCountDeltaPhi130 = tdCount.clone(selection="&&".join(sels+[metCut, bTaggingCut, deltaPhi130Cut]))
    tdCountDeltaPhi90 = tdCount.clone(selection="&&".join(sels+[metCut, bTaggingCut, deltaPhi90Cut]))
    eventCounter.mainCounterAppendRow("JetsForEffs", tdCount.clone(weight=weight, selection="&&".join(sels)))
    eventCounter.mainCounterAppendRow("METForEffs", tdCountMET)
    eventCounter.mainCounterAppendRow("BTagging", tdCountBTagging)
    eventCounter.mainCounterAppendRow("DeltaPhi < 160", tdCountDeltaPhi160)
    eventCounter.mainCounterAppendRow("DeltaPhi < 130", tdCountDeltaPhi130)
    eventCounter.mainCounterAppendRow("DeltaPhi < 90", tdCountDeltaPhi90)

    if not isCorrected:
        td1 = tdCount.clone(selection=metCut+"&&"+bTaggingCut+"&& (tecalometNoHF_p4.Pt() > 60)")
        td2 = tdCount.clone(selection=metCut+"&&"+bTaggingCut+"&& (tecalomet_p4.Pt() > 60)")
        td3 = dataset.TreeDrawCompound(td1, {
                "SingleMu_Mu_170722-172619_Aug05": td2,
                "SingleMu_Mu_172620-173198_Prompt": td2,
                "SingleMu_Mu_173236-173692_Prompt": td2,
                })
        eventCounter.mainCounterAppendRow("BTagging+CaloMetNoHF", td1)
        eventCounter.mainCounterAppendRow("BTagging+CaloMet", td2)
        eventCounter.mainCounterAppendRow("BTagging+CaloMet(NoHF)", td3)

    #(mainTable, mainTableChi2) = eventCounter.getMainCounterTableFit()
    mainTable = eventCounter.getMainCounterTable()

    ewkDatasets = ["WJets", "TTJets", "DYJetsToLL", "SingleTop", "Diboson"]
    allDatasets = None
    if "QCD_Pt20_MuEnriched" in datasetsEmb.getAllDatasetNames():
        allDatasets = ["QCD_Pt20_MuEnriched"]+ewkDatasets
    def ewkSum(table):
        table.insertColumn(1, counter.sumColumn("EWKMCsum", [table.getColumn(name=name) for name in ewkDatasets]))
        if allDatasets != None:
            table.insertColumn(2, counter.sumColumn("MCSum", [table.getColumn(name=name) for name in allDatasets]))
    ewkSum(mainTable)
    cellFormat = counter.TableFormatText(counter.CellFormatTeX(valueFormat='%.3f'))
    #print mainTableChi2.format(cellFormat)
    print mainTable.format(cellFormat)

    tauTable = eventCounter.getSubCounterTable("TauIDPassedEvt::tauID_HPSTight")
    ewkSum(tauTable)
    print tauTable.format(cellFormat)

    # Efficiencies
    mainTable.keepOnlyRows([
            "All events",
            "Trigger and HLT_MET cut",
            "taus == 1",
#            "trigger scale factor",
            "electron veto",
            "muon veto",
            "MET",
            "njets",
            "btagging",
            "btagging scale factor",
            "JetsForEffs",
            "METForEffs",
            "BTagging",
            "DeltaPhi < 160",
            "DeltaPhi < 130"
            ])
    tauTable.keepOnlyRows([
            "AllTauCandidates",
            "DecayModeFinding",
            "TauJetPt",
            "TauJetEta",
            "TauLdgTrackExists",
            "TauLdgTrackPtCut",
            "TauECALFiducialCutsCracksAndGap",
            "TauAgainstElectronCut",
            "TauAgainstMuonCut",
            #"EMFractionCut",
            "HPS",
            "TauOneProngCut",
            "TauRtauCut",
            ])

    effFormat = counter.TableFormatText(counter.CellFormatTeX(valueFormat='%.4f'))
    #effFormat = counter.TableFormatConTeXtTABLE(counter.CellFormatTeX(valueFormat='%.4f'))
    for name, table in [("Main", mainTable), ("Tau ID", tauTable)]:
        effTable = counter.CounterTable()
        col = table.getColumn(name="Data")
        effTable.appendColumn(col)
        effTable.appendColumn(counter.efficiencyColumn(col.getName()+" eff", col))
        col = table.getColumn(name="EWKMCsum")
        effTable.appendColumn(col)
        effTable.appendColumn(counter.efficiencyColumn(col.getName()+" eff", col))
        print "%s counter efficiencies" % name
        print effTable.format(effFormat)


    if isCorrected:
        return

    print "Trigger uncertainties"
    bins = [40, 50, 60, 80]
    tauPtPrototype = ROOT.TH1F("tauPtTrigger", "Tau pt", len(bins)-1, array.array("d", bins))
    runs = [
        "(160431 <= run && run <= 167913)",
        "(170722 <= run && run <= 173198)",
        "(173236 <= run && run <= 173692)",
        #"(160431 <= run && run <= 173692)",
        ]
    for name, td in [
        ("BTagging", tdCountBTagging),
        ("DeltaPhi160", tdCountDeltaPhi160),
        ("DeltaPhi130", tdCountDeltaPhi130),
        ("DeltaPhi90", tdCountDeltaPhi90)
        ]:
        t = td.clone(varexp="tau_p4.Pt() >>tauPtTrigger")
        
        NallSum = 0
        NSum = 0
        absUncSquareSum = 0

        for runRegion in runs:
            #neventsPlot = createPlot(dataset.treeDrawToNumEntries(t.clone(weight="weightTrigger")))
            #uncertaintyPlot = createPlot(dataset.treeDrawToNumEntries(t.clone(weight="weightTriggerAbsUnc*weightTriggerAbsUnc/(weightTrigger*weightTrigger)")))
            tmp = t.clone(selection=t.selection+"&&"+runRegion)
            (th1all, gr) = datasetsEmb.getHistogram("Data", tmp.clone(weight="")) # Nall
            (th1, gr) = datasetsEmb.getHistogram("Data", tmp.clone(weight="weightTrigger")) # Nevents
            (th12, gr) = datasetsEmb.getHistogram("Data", tmp.clone(weight="weightTriggerAbsUnc")) # uncertainty

            Nall = th1all.Integral(0, th1all.GetNbinsX()+1)
            N = th1.Integral(0, th1.GetNbinsX()+1)
            #absSum2 = th12.Integral(0, th12.GetNbinsX()+1)
            #absUnc = math.sqrt(absSum2)
            #absUnc = th12.Integral(0, 2)
            NallSum += Nall
            NSum += N
            absUnc = tauEmbedding.squareSum(th12)
            absUncSquareSum += absUnc
            absUnc = math.sqrt(absUnc)
            relUnc = 0
            if N > 0:
                relUnc = absUnc/N

            print "%-15s for runs %s Nall = %.2f, N = %.2f, absolute uncertainty %.2f, relative uncertainty %.4f" % (name, runRegion, Nall, N, absUnc, relUnc)


        absUnc = math.sqrt(absUncSquareSum)
        relUnc = absUnc/NSum

        print "%-15s Nall = %.2f, N = %.2f, absolute uncertainty %.2f, relative uncertainty %.4f" % (name, NallSum, NSum, absUnc, relUnc)
        print


def doCountersResidual(datasetsResidual):
    eventCounter = tauEmbedding.EventCounterResidual(datasetsResidual, counters=analysisEmb+counters)

    mainTable = eventCounter.getMainCounterTable()

    names = ["Data", "DYJetsToLL residual", "WW residual"]
    mainTable.insertColumn(1, counter.sumColumn("Data+residual", [mainTable.getColumn(name=name) for name in names]))

    if "EWKMC" in datasetsResidual.getAllDatasetNames():
        names = ["EWKMC", "DYJetsToLL residual", "WW residual"]
        mainTable.insertColumn(3, counter.sumColumn("EWKMC+residual", [mainTable.getColumn(name=name) for name in names]))

    cellFormat = counter.TableFormatText(counter.CellFormatTeX(valueFormat='%.3f'))
    print mainTable.format(cellFormat)
    

def doCountersOld(datasetsEmb, counterName="counter"):
    datasetNames = datasetsEmb.getAllDatasetNames()

    table = counter.CounterTable()
    for name in datasetNames:
        table.appendColumn(datasetsEmb.getCounter(name, analysisEmb+"Counters/weighted/"+counterName))

    ewkDatasets = ["WJets", "TTJets", "DYJetsToLL", "SingleTop", "Diboson"]
    table.insertColumn(2, counter.sumColumn("EWKMCsum", [table.getColumn(name=name) for name in ewkDatasets]))

    print "============================================================"
    if isinstance(datasetsEmb, result.DatasetsDYCorrection):
        print "DY correction applied"
    cellFormat = counter.TableFormatText(counter.CellFormatTeX(valueFormat='%.3f'))
    print table.format(cellFormat)



if __name__ == "__main__":
    main()
