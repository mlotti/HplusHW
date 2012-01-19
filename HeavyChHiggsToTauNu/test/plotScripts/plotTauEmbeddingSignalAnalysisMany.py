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
import plotTauEmbeddingSignalAnalysis as tauEmbedding
import produceTauEmbeddingResult as result

#analysisEmb = "signalAnalysis"
analysisEmb = "signalAnalysisCaloMet60TEff"
analysisSig = "signalAnalysisGenuineTau"

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
    dirEmbs = ["."] + [os.path.join("..", d) for d in result.dirEmbs[1:]]
    dirSig = "../"+result.dirSig
    
    datasetsEmb = result.DatasetsMany(dirEmbs, analysisEmb+"Counters")
    datasetsSig = dataset.getDatasetsFromMulticrabCfg(cfgfile=dirSig+"/multicrab.cfg", counters=analysisSig+"Counters")

    datasetsEmb.forEach(plots.mergeRenameReorderForDataMC)
    datasetsEmb.setLumiFromData()
    plots.mergeRenameReorderForDataMC(datasetsSig)

    style = tdrstyle.TDRStyle()
    histograms.createLegend.moveDefaults(dx=-0.04)
    datasetsEmb.remove(["QCD_Pt20_MuEnriched"])
    #plots._legendLabels["QCD_Pt20_MuEnriched"] = "QCD"
    histograms.createLegend.moveDefaults(dh=-0.05)
    #histograms.createLegend.moveDefaults(dx=-0.18, dy=0.05, dh=-0.05)

    tauEmbedding.normalize=True
    tauEmbedding.era = "Run2011A"

    datasetsEmbCorrected = result.DatasetsDYCorrection(datasetsEmb, datasetsSig, analysisEmb, analysisSig)

    doPlots(datasetsEmb)
    doPlots(datasetsEmbCorrected)

    doCounters(datasetsEmb)
    #doCounters(datasetsEmbCorrected)

    #doCountersOld(datasetsEmb)


def drawPlot(*args, **kwargs):
    tauEmbedding.drawPlot(*args, normalize=False, **kwargs)

def doPlots(datasetsEmb):
    datasetNames = datasetsEmb.getAllDatasetNames()
    isCorrected = isinstance(datasetsEmb, result.DatasetsDYCorrection)

    def createPlot(name, dyx=0.67, dyy=0.64):
        rootHistos = []
        for datasetName in datasetNames:
            (histo, tmp) = datasetsEmb.getHistogram(datasetName, name)
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

    treeDraw = dataset.TreeDraw(analysisEmb+"/tree", weight="weightPileup*weightTrigger*weightBTagging")
    tdMt = treeDraw.clone(varexp="sqrt(2 * tau_p4.Pt() * met_p4.Et() * (1-cos(tau_p4.Phi()-met_p4.Phi()))) >>tmp(20,0,400)")

    metCut = "(met_p4.Et() > 50)"
    bTaggingCut = "passedBTagging"
    deltaPhi160Cut = "(acos( (tau_p4.Px()*met_p4.Px()+tau_p4.Py()*met_p4.Py())/(tau_p4.Pt()*met_p4.Et()) )*57.3 <= 160)"
    selection = "&&".join([metCut, bTaggingCut, deltaPhi160Cut])

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
        eventCounter = result.EventCounterDYCorrection(datasetsEmb, counters=analysisEmb+"Counters/weighted")
    else:
        eventCounter = result.EventCounterMany(datasetsEmb, counters=analysisEmb+"Counters/weighted")

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

    mainTable = eventCounter.getMainCounterTable()

    ewkDatasets = ["WJets", "TTJets", "DYJetsToLL", "SingleTop", "Diboson"]
    def ewkSum(table):
        table.insertColumn(1, counter.sumColumn("EWKMCsum", [table.getColumn(name=name) for name in ewkDatasets]))
    ewkSum(mainTable)
    cellFormat = counter.TableFormatText(counter.CellFormatTeX(valueFormat='%.3f'))
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
