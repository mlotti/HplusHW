#!/usr/bin/env python

######################################################################
#
# This plot script is for comparing the embedded MC to normal MC
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

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.cutstring import * # And, Not, Or
import plotTauEmbeddingSignalAnalysis as tauEmbedding
import produceTauEmbeddingResult as result

# Without trigger
#analysisEmb = "signalAnalysis"
#analysisSig = "signalAnalysisTauEmbeddingLikePreselection"

# With trigger
analysisEmb = "signalAnalysisCaloMet60TEff"
#analysisSig = "signalAnalysisTauEmbeddingLikeTriggeredPreselection" # require genuine tau beforehand, valid for all comparisons
analysisSig = "signalAnalysisGenuineTau" # require that the selected tau is genuine, valid comparison after njets

metCut = "(met_p4.Et() > 50)"
bTaggingCut = "passedBTagging"
deltaPhi160Cut = "(acos( (tau_p4.Px()*met_p4.Px()+tau_p4.Py()*met_p4.Py())/(tau_p4.Pt()*met_p4.Et()) )*57.3 <= 160)"
deltaPhi130Cut = "(acos( (tau_p4.Px()*met_p4.Px()+tau_p4.Py()*met_p4.Py())/(tau_p4.Pt()*met_p4.Et()) )*57.3 <= 130)"

weight = "weightPileup*weightTrigger"
#weight = ""
#weightBTagging = weight # don't apply b-tagging scale factor
weightBTagging = weight+"*weightBTagging"

def main():
    dirEmbs = ["."] + [os.path.join("..", d) for d in result.dirEmbs[1:]]
    dirSig = "../"+result.dirSig
    
    datasetsEmb = result.DatasetsMany(dirEmbs, analysisEmb+"Counters", normalizeMCByLuminosity=True)
    datasetsSig = dataset.getDatasetsFromMulticrabCfg(cfgfile=dirSig+"/multicrab.cfg", counters=analysisSig+"Counters")

    datasetsEmb.forEach(lambda mgr: plots.mergeRenameReorderForDataMC(mgr, keepSourcesMC=True))
    datasetsEmb.setLumiFromData()
    plots.mergeRenameReorderForDataMC(datasetsSig, keepSourcesMC=True)

#    del plots._datasetMerge["WW"]
#    del plots._datasetMerge["WZ"]
#    del plots._datasetMerge["ZZ"]

    def mergeEWK(datasets):
        datasets.merge("EWKMC", ["WJets", "TTJets", "DYJetsToLL", "SingleTop", "Diboson", "WW"], keepSources=True)
        #datasets.merge("EWKMC", ["WJets", "TTJets"], keepSources=True)
    mergeEWK(datasetsSig)
    datasetsEmb.forEach(mergeEWK)
    plots._legendLabels["EWKMC"] = "EWK"

    datasetsEmb.remove(filter(lambda name: "TTToHplus" in name, datasetsEmb.getAllDatasetNames()))
    datasetsEmb.remove(filter(lambda name: "HplusTB" in name, datasetsEmb.getAllDatasetNames()))

    style = tdrstyle.TDRStyle()
    ROOT.gStyle.SetEndErrorSize(5)
    histograms.createLegend.setDefaults(y1=0.93, y2=0.75, x1=0.52, x2=0.93)

    tauEmbedding.normalize=True
    tauEmbedding.era = "Run2011A"

    #datasetsEmbCorrected = result.DatasetsDYCorrection(datasetsEmb, datasetsSig, analysisEmb, analysisSig)
    datasetsEmbCorrected = result.DatasetsResidual(datasetsEmb, datasetsSig, analysisEmb, analysisSig, ["DYJetsToLL", "WW"], totalNames=["Data", "EWKMC"])

    def dop(datasetName):
        doPlots(datasetsEmb, datasetsSig, datasetName)
#        doCounters(datasetsEmb, datasetsSig, datasetName)
        print "%s done" % datasetName


    doPlots(datasetsEmbCorrected, datasetsSig, "EWKMC", doData=True, postfix="_residual")
    #doCounters(datasetsEmb, datasetsSig, "EWKMC")
    return
    dop("TTJets")
    dop("WJets")
    #dop("W3Jets")
    dop("DYJetsToLL")
    dop("SingleTop")
    dop("Diboson")
    return
    dop("WW")
    dop("WZ")
    dop("ZZ")

    #doPlots(datasetsEmb, datasetsSig, "EWKMC", doData=True, postfix="_data")
    ##doPlots(datasetsEmb, datasetsSig, "Data")

    doPlots(datasetsEmbCorrected, datasetsSig, "EWKMC", postfix="_dycorrected")

def doPlots(datasetsEmb, datasetsSig, datasetName, doData=False, postfix=""):
    lumi = datasetsEmb.getLuminosity()
    isCorrected = isinstance(datasetsEmb, result.DatasetsDYCorrection) or isinstance(datasetsEmb, result.DatasetsResidual)
    
    def createPlot(name, rebin=1, addVariation=False):
        name2Emb = name
        name2Sig = name
        if isinstance(name, basestring):
            name2Emb = analysisEmb+"/"+name
            name2Sig = analysisSig+"/"+name
        else:
            name2Emb = name.clone(tree=analysisEmb+"/tree")
            name2Sig = name.clone(tree=analysisSig+"/tree")

        (emb, embVar) = datasetsEmb.getHistogram(datasetName, name2Emb, rebin)
        sig = datasetsSig.getDataset(datasetName).getDatasetRootHisto(name2Sig)
        sig.normalizeToLuminosity(lumi)
        sig = sig.getHistogram()
        if rebin > 1:
            sig.Rebin(rebin)

        emb.SetName("Embedded")
        sig.SetName("Normal")

        p = None
        sty = None
        if doData:
            (embData, embDataVar) = datasetsEmb.getHistogram("Data", name2Emb, rebin=rebin)
            embData.SetName("EmbeddedData")
            #p = plots.ComparisonManyPlot(embData, [emb, sig])
            p = plots.ComparisonPlot(embData, sig)
            p.histoMgr.setHistoDrawStyle("EmbeddedData", "EP")
            p.histoMgr.setHistoLegendStyle("EmbeddedData", "P")
            p.setLuminosity(lumi)
            sty = [styles.dataStyle, styles.styles[1]]
        else:
            p = plots.ComparisonPlot(emb, sig)
            sty = styles.styles

        legLabel = plots._legendLabels.get(datasetName, datasetName)
        if legLabel != "Data":
            legLabel += " MC"
        residual = ""
        if isCorrected:
            residual =" + res. MC"
        p.histoMgr.setHistoLegendLabelMany({
                "Embedded":     "Embedded " + legLabel,
                "Normal":       "Normal " + legLabel,
                #"EmbeddedData": "Embedded data"+residual,
                "EmbeddedData": "Emb. data"+residual,
                })
        p.histoMgr.forEachHisto(styles.Generator(sty))
        if addVariation:
            if doData:
                if embDataVar != None:
                    plots.copyStyle(p.histoMgr.getHisto("EmbeddedData").getRootHisto(), embDataVar)
                    embDataVar.SetMarkerStyle(2)
                    p.embeddingDataVariation = embDataVar
            else:
                if embVar != None:
                    plots.copyStyle(p.histoMgr.getHisto("Embedded").getRootHisto(), embVar)
                    embVar.SetMarkerStyle(2)
                    p.embeddingVariation = embVar
    
        return p

    def createDrawPlot(name, *args, **kwargs):
        p = createPlot(name)
        drawPlot(p, *args, **kwargs)

    prefix = "mcembsig"
    if doData:
        prefix = "embdatasigmc"
    prefix = prefix+postfix+"_"+datasetName+"_"

    #opts2def = {"DYJetsToLL": {"ymin":0, "ymax": 1.5}}.get(datasetName, {"ymin": 0.5, "ymax": 1.5})
    opts2def = {"ymin": 0, "ymax": 2}
    def drawControlPlot(path, xlabel, rebin=None, opts2=None, **kwargs):
        opts2_ = opts2def
        if opts2 != None:
            opts2_ = opts2
        cargs = {}
        if rebin != None:
            cargs["rebin"] = rebin
        drawPlot(createPlot("ControlPlots/"+path, **cargs), prefix+path, xlabel, opts2=opts2_, **kwargs)

    def update(d1, d2):
        tmp = {}
        tmp.update(d1)
        tmp.update(d2)
        return tmp

    # Control plots
    optsdef = {}
    opts = optsdef
    drawControlPlot("SelectedTau_pT_AfterStandardSelections", "#tau-jet p_{T} (GeV/c)", opts=update(opts, {"xmax": 250}), rebin=2, cutBox={"cutValue": 40, "greaterThan": 40})

    opts = optsdef
    moveLegend = {"dy":-0.6, "dx":-0.2}
    if analysisEmb != "signalAnalysis":
        opts = {
            "SingleTop": {"ymax": 1.8}
            }.get(datasetName, {"ymaxfactor": 1.4})
        if datasetName != "TTJets":
            moveLegend = {"dx": -0.32}
    drawControlPlot("SelectedTau_eta_AfterStandardSelections", "#tau-jet #eta", opts=update(opts, {"xmin": -2.2, "xmax": 2.2}), ylabel="Events / %.1f", rebin=4, log=False, moveLegend=moveLegend)

    drawControlPlot("SelectedTau_phi_AfterStandardSelections", "#tau-jet #phi", rebin=10, ylabel="Events / %.2f", log=False)
    drawControlPlot("SelectedTau_LeadingTrackPt_AfterStandardSelections", "#tau-jet ldg. charged particle p_{T} (GeV/c)", opts=update(opts, {"xmax": 300}), rebin=2, cutBox={"cutValue": 20, "greaterThan": True})

    opts = {"ymin": 1e-1, "ymaxfactor": 5}
    moveLegend = {"dx": -0.3}
    if analysisEmb != "signalAnalysis":
        moveLegend = {"dx": -0.25}
        if datasetName == "Diboson":
            opts["ymin"] = 1e-2
    drawControlPlot("SelectedTau_Rtau_AfterStandardSelections", "R_{#tau} = p^{ldg. charged particle}/p^{#tau jet}", opts=update(opts, {"xmin": 0.65, "xmax": 1.05}), rebin=5, ylabel="Events / %.2f", moveLegend=moveLegend, cutBox={"cutValue":0.7, "greaterThan":True})

    opts = optsdef
    drawControlPlot("Njets_AfterStandardSelections", "Number of jets", ylabel="Events")
    # After Njets
    drawControlPlot("MET", "Uncorrected PF E_{T}^{miss} (GeV)", rebin=5, opts=update(opts, {"xmax": 400}), cutLine=50)


    # after MET
    moveLegend = {"dx": -0.23, "dy": -0.5}
    moveLegend = {
        "WJets": {},
        "DYJetsToLL": {},
        "SingleTop": {},
        "Diboson": {}
        }.get(datasetName, moveLegend)
    drawControlPlot("NBjets", "Number of selected b jets", opts=update(opts, {"xmax": 6}), ylabel="Events", moveLegend=moveLegend, cutLine=1)

    # Tree cut definitions
    treeDraw = dataset.TreeDraw("dummy", weight=weightBTagging)
    tdDeltaPhi = treeDraw.clone(varexp="acos( (tau_p4.Px()*met_p4.Px()+tau_p4.Py()*met_p4.Py())/(tau_p4.Pt()*met_p4.Et()) )*57.3 >>tmp(18, 0, 180)")
    tdMt = treeDraw.clone(varexp="sqrt(2 * tau_p4.Pt() * met_p4.Et() * (1-cos(tau_p4.Phi()-met_p4.Phi()))) >>tmp(20,0,400)")

    # DeltapPhi
    xlabel = "#Delta#phi(#tau jet, E_{T}^{miss}) (^{#circ})"
    def customDeltaPhi(h):
        yaxis = h.getFrame().GetYaxis()
        yaxis.SetTitleOffset(0.8*yaxis.GetTitleOffset())
    opts = {
        "WJets": {"ymax": 35},
        "DYJetsToLL": {"ymax": 12},
        "Diboson": {"ymax": 1},
        }.get(datasetName, {"ymaxfactor": 1.2})
    opts2=opts2def
    if analysisEmb != "signalAnalysis":
        opts = {
            "WJets": {"ymax": 20},
            "DYJetsToLL": {"ymax": 5},
            "SingleTop": {"ymax": 2},
            "Diboson": {"ymax": 0.6},
            }.get(datasetName, {"ymaxfactor": 1.2})
        opts2 = {
            "WJets": {"ymin": 0, "ymax": 3}
            }.get(datasetName, opts2def)
    drawPlot(createPlot(tdDeltaPhi.clone(selection=And(metCut, bTaggingCut))), prefix+"deltaPhi_3AfterBTagging", xlabel, log=False, opts=opts, opts2=opts2, ylabel="Events / %.0f^{#circ}", function=customDeltaPhi, moveLegend={"dx":-0.22}, cutLine=[130, 160])


    # After all cuts
    selection = "&&".join([metCut, bTaggingCut, deltaPhi160Cut])

    #opts = {"ymaxfactor": 1.4}
    opts = {}

    drawPlot(createPlot(treeDraw.clone(varexp="tau_p4.Pt() >>tmp(20,0,200)", selection=selection)), prefix+"selectedTauPt_4AfterDeltaPhi160", "#tau-jet p_{T} (GeV/c)", opts=opts, opts2={"ymin": 0, "ymax": 3})
    drawPlot(createPlot(treeDraw.clone(varexp="met_p4.Pt() >>tmp(16,0,400)", selection=selection)), prefix+"MET_4AfterDeltaPhi160", "E_{T}^{miss} (GeV)", ylabel="Events / %.0f GeV", opts=opts, opts2={"ymin": 0, "ymax": 3})

    opts = {
        "TTJets": {"ymax": 28},
        "SingleTop": {"ymax": 4.5},
        "DYJetsToLL": {"ymax": 18},
        "Diboson": {"ymax": 1.2},
        "WJets": {"ymax": 50},
        }.get(datasetName, {})
    opts2 = {"ymin": 0, "ymax": 2}
    if analysisEmb != "signalAnalysis":
        opts = {
            "EWKMC": {"ymax": 46},
            "TTJets": {"ymax": 12},
            #"WJets": {"ymax": 35},
            "WJets": {"ymax": 25},
            "SingleTop": {"ymax": 2.2},
            "DYJetsToLL": {"ymax": 6.5},
            #"Diboson": {"ymax": 0.9},
            "Diboson": {"ymax": 0.8},
            "W3Jets": {"ymax": 5}
            }.get(datasetName, {})
        opts2 = {
            "TTJets": {"ymin": 0, "ymax": 1.2},
            "Diboson": {"ymin": 0, "ymax": 3.2},
            }.get(datasetName, opts2)
    
    p = createPlot(tdMt.clone(selection=selection))
    p.appendPlotObject(histograms.PlotText(0.5, 0.55, "#Delta#phi(#tau jet, E_{T}^{miss}) < 160^{#circ}", size=20))
    drawPlot(p, prefix+"transverseMass_4AfterDeltaPhi160", "m_{T}(#tau jet, E_{T}^{miss}) (GeV/c^{2})", opts=opts, opts2=opts2, ylabel="Events / %.0f GeV/c^{2}", log=False)



def doCounters(datasetsEmb, datasetsSig, datasetName):
    lumi = datasetsEmb.getLuminosity()

    # Counters
    eventCounterEmb = result.EventCounterMany(datasetsEmb, counters=analysisEmb+"Counters/weighted")
    eventCounterSig = counter.EventCounter(datasetsSig, counters=analysisSig+"Counters/weighted")

    def isNotThis(name):
        return name != datasetName

    eventCounterEmb.removeColumns(filter(isNotThis, datasetsEmb.getAllDatasetNames()))
    eventCounterSig.removeColumns(filter(isNotThis, datasetsSig.getAllDatasetNames()))
    eventCounterSig.normalizeMCToLuminosity(lumi)

    tdCount = dataset.TreeDraw("dummy", weight=weightBTagging)
    tdCountMET = tdCount.clone(weight=weight, selection=metCut)
    tdCountBTagging = tdCount.clone(selection=And(metCut, bTaggingCut))
    tdCountDeltaPhi160 = tdCount.clone(selection=And(metCut, bTaggingCut, deltaPhi160Cut))
    tdCountDeltaPhi130 = tdCount.clone(selection=And(metCut, bTaggingCut, deltaPhi130Cut))
    def addRow(name, td):
        tdEmb = td.clone(tree=analysisEmb+"/tree")
        tdSig = td.clone(tree=analysisSig+"/tree")
        eventCounterEmb.mainCounterAppendRow(name, tdEmb)
        eventCounterSig.getMainCounter().appendRow(name, tdSig)

    addRow("JetsForEffs", tdCount.clone(weight=weight))
    addRow("METForEffs", tdCountMET)
    addRow("BTagging (SF)", tdCountBTagging)
    addRow("DeltaPhi < 160", tdCountDeltaPhi160)
    addRow("BTagging (SF) again", tdCountBTagging)
    addRow("DeltaPhi < 130", tdCountDeltaPhi130)

    #effFormat = counter.TableFormatText(counter.CellFormatText(valueFormat='%.4f'))
    #effFormat = counter.TableFormatConTeXtTABLE(counter.CellFormatTeX(valueFormat='%.4f'))
    effFormat = counter.TableFormatText(counter.CellFormatTeX(valueFormat='%.4f'))

    f = open("counters_%s.txt"%datasetName, "w")

    for function, cname in [
        (lambda c: c.getMainCounterTable(), "Main"),
        (lambda c: c.getSubCounterTable("TauIDPassedEvt::tauID_HPSTight"), "Tau")
        ]:
        tableEmb = function(eventCounterEmb)
        tableSig = function(eventCounterSig)

        table = counter.CounterTable()
        col = tableEmb.getColumn(name=datasetName)
        col.setName("Embedded")
        table.appendColumn(col)
        col = tableSig.getColumn(name=datasetName)
        col.setName("Normal")
        table.appendColumn(col)

        f.write("%s counters\n" % cname)
        f.write(table.format())
        f.write("\n")

        if cname == "Main":
            #map(lambda t: t.keepOnlyRows([
            table.keepOnlyRows([
                        "All events",
                        "Trigger and HLT_MET cut",
                        "taus == 1",
                        #"trigger scale factor",
                        "electron veto",
                        "muon veto",
                        "MET",
                        "njets",
                        "btagging",
                        "btagging scale factor",
                        "JetsForEffs",
                        "METForEffs",
                        "BTagging (SF)",
                        "DeltaPhi < 160",
                        "BTagging (SF) again",
                        "DeltaPhi < 130"
                        ])#, [tableEmb, tableSig])
        else:
            #map(lambda t: t.keepOnlyRows([
            table.keepOnlyRows([
                        "AllTauCandidates",
                        "DecayModeFinding",
                        "TauJetPt",
                        "TauJetEta",
                        #"TauLdgTrackExists",
                        "TauLdgTrackPtCut",
                        "TauECALFiducialCutsCracksAndGap",
                        "TauAgainstElectronCut",
                        "TauAgainstMuonCut",
                        #"EMFractionCut",
                        "HPS",
                        "TauOneProngCut",
                        "TauRtauCut",
                        ])#, [tableEmb, tableSig])

        col = table.getColumn(name="Embedded")
        table.insertColumn(1, counter.efficiencyColumn(col.getName()+" eff", col))
        col = table.getColumn(name="Normal")
        table.appendColumn(counter.efficiencyColumn(col.getName()+" eff", col))

        f.write("%s counters\n" % cname)
        f.write(table.format(effFormat))
        f.write("\n\n")
    f.close()

def doPlotsData(datasetsEmb):
    def createPlot(name):
        name2Emb = name

        if isinstance(name, basestring):
            name2Emb = analysisEmb+"/"+name
        else:
            name2Emb = name.clone(tree=analysisEmb+"/tree")

        (embData, embDataVar) = datasetsEmb.getHistogram("Data", name2Emb)
        embHistos = datasetsEmb.getHistograms("Data", name2Emb)

        p = plots.ComparisonManyPlot(embData, embHistos)
        p.setLuminosity(datasetsEmb.getLuminosity())

        p.histoMgr.forEachHisto(styles.Generator([styles.dataStyle] + styles.styles))
        #p.histoMgr.setHistoDrawStyleAll("P")
        #p.histoMgr.setHistoLegendStyleAll("P")
        p.histoMgr.setHistoDrawStyle("Average", "PE")
        p.histoMgr.setHistoLegendStyle("Average", "P")

        return p

    treeDraw = dataset.TreeDraw("dummy", weight=weightBTagging)
    tdMt = treeDraw.clone(varexp="sqrt(2 * tau_p4.Pt() * met_p4.Et() * (1-cos(tau_p4.Phi()-met_p4.Phi()))) >>tmp(20,0,400)")

    # After all cuts
    metCut = "(met_p4.Et() > 50)"
    bTaggingCut = "passedBTagging"
    deltaPhi160Cut = "(acos( (tau_p4.Px()*met_p4.Px()+tau_p4.Py()*met_p4.Py())/(tau_p4.Pt()*met_p4.Et()) )*57.3 <= 160)"
    selection = "&&".join([metCut, bTaggingCut, deltaPhi160Cut])
    prefix = "mcembsig_data"

#    drawPlot(createPlot(treeDraw.clone(varexp="tau_p4.Pt() >>tmp(20,0,200)", selection=selection)), prefix+"_selectedTauPt_4AfterDeltaPhi160", "#tau-jet p_{T} (GeV/c)", opts2={"ymin": 0, "ymax": 3})
#    drawPlot(createPlot(treeDraw.clone(varexp="met_p4.Pt() >>tmp(16,0,400)", selection=selection)), prefix+"_MET_4AfterDeltaPhi160", "E_{T}^{miss} (GeV)", ylabel="Events / %.0f GeV", opts2={"ymin": 0, "ymax": 3})
    drawPlotData(createPlot(tdMt.clone(selection=selection)), prefix+"_transverseMass_4AfterDeltaPhi160", "m_{T}(#tau jet, E_{T}^{miss}) (GeV/c^{2})", opts2={"ymin": 0, "ymax": 3}, ylabel="Events / %.0f GeV/c^{2}", log=False)

def drawPlot(h, name, xlabel, ylabel="Events / %.0f GeV/c", rebin=1, log=True, ratio=True, opts={}, opts2={}, moveLegend={}, **kwargs):
    if rebin > 1:
        h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    ylab = ylabel
    if "%" in ylabel:
        ylab = ylabel % h.binWidth()

    #scaleNormalization(h)
    #h.stackMCHistograms()

    sigErr = h.histoMgr.getHisto("Normal").getRootHisto().Clone("Normal_err")
    sigErr.SetFillColor(ROOT.kRed-7)
    sigErr.SetMarkerSize(0)
    sigErr.SetFillStyle(3005)
    h.prependPlotObject(sigErr, "E2")
    if h.histoMgr.hasHisto("Embedded"):
        embErr = h.histoMgr.getHisto("Embedded").getRootHisto().Clone("Embedded_err")
        embErr.SetFillColor(ROOT.kBlue-7)
        embErr.SetFillStyle(3004)
        embErr.SetMarkerSize(0)
        h.prependPlotObject(embErr, "E2")

    if hasattr(h, "embeddingVariation"):
        h.prependPlotObject(h.embeddingVariation, "[]")
    if hasattr(h, "embeddingDataVariation"):
        h.prependPlotObject(h.embeddingDataVariation, "[]")


    _opts = {"ymin": 0.01, "ymaxfactor": 2}
    if not log:
        _opts["ymin"] = 0
        _opts["ymaxfactor"] = 1.1
    _opts2 = {"ymin": 0.5, "ymax": 1.5}
    _opts.update(opts)
    _opts2.update(opts2)

    if log:
        name = name + "_log"
    h.createFrame(name, createRatio=ratio, opts=_opts, opts2=_opts2)
    h.getPad().SetLogy(log)
    if ratio:
        h.getFrame2().GetYaxis().SetTitle("Ratio")
    #yaxis = h.getFrame2().GetYaxis()
    #yaxis.SetTitleSize(yaxis.GetTitleSize()*0.7)
    #yaxis.SetTitleOffset(yaxis.GetTitleOffset()*1.5)
    h.setLegend(histograms.moveLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend)))
    tmp = sigErr.Clone("tmp")
    tmp.SetFillColor(ROOT.kBlack)
    tmp.SetFillStyle(3013)
    tmp.SetFillStyle(sigErr.GetFillStyle()); tmp.SetFillColor(sigErr.GetFillColor())
    tmp.SetLineColor(ROOT.kWhite)
    h.legend.AddEntry(tmp, "Stat. unc.", "F")

    x = h.legend.GetX1()
    y = h.legend.GetY1()
    x += 0.05; y -= 0.03
    if hasattr(h, "embeddingDataVariation"):
        histograms.addText(x, y, "[  ]", size=17, color=h.embeddingDataVariation.GetMarkerColor()); x += 0.05
        histograms.addText(x, y, "Embedded data min/max", size=17); y-= 0.03
    if hasattr(h, "embeddingVariation"):
        histograms.addText(x, y, "[  ]", size=17, color=h.embeddingVariation.GetMarkerColor()); x += 0.05
        histograms.addText(x, y, "Embedded MC min/max", size=17); y-= 0.03

    #if hasattr(h, "embeddingDataVariation"):
    #    h.legend.AddEntry(h.embeddingDataVariation, "Embedded data min/max", "p")
    #if hasattr(h, "embeddingVariation"):
    #    h.legend.AddEntry(h.embeddingVariation, "Embedded MC min/max", "p")

    common(h, xlabel, ylab, **kwargs)


def drawPlotData(h, name, xlabel, ylabel="Events / %.0f GeV/c", rebin=1, log=True, ratio=True, opts={}, opts2={}, moveLegend={}, **kwargs):
    if rebin > 1:
        h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    ylab = ylabel
    if "%" in ylabel:
        ylab = ylabel % h.binWidth()

    #scaleNormalization(h)
    #h.stackMCHistograms()

    _opts = {"ymin": 0.01, "ymaxfactor": 2}
    if not log:
        _opts["ymin"] = 0
        _opts["ymaxfactor"] = 1.1
    _opts2 = {"ymin": 0.5, "ymax": 1.5}
    _opts.update(opts)
    _opts2.update(opts2)

    if log:
        name = name + "_log"
    h.createFrame(name, createRatio=ratio, opts=_opts, opts2=_opts2)
    h.getPad().SetLogy(log)
    if ratio:
        h.getFrame2().GetYaxis().SetTitle("Ratio")
    #yaxis = h.getFrame2().GetYaxis()
    #yaxis.SetTitleSize(yaxis.GetTitleSize()*0.7)
    #yaxis.SetTitleOffset(yaxis.GetTitleOffset()*1.5)
    h.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))

    common(h, xlabel, ylab, **kwargs)

def common(h, xlabel, ylabel, cutLine=None, cutBox=None, function=None):
    # Add cut line and/or box
    if cutLine != None:
        lst = cutLine
        if not isinstance(lst, list):
            lst = [lst]

        for line in lst:
            h.addCutBoxAndLine(line, box=False, line=True)
    if cutBox != None:
        lst = cutBox
        if not isinstance(lst, list):
            lst = [lst]

        for box in lst:
            h.addCutBoxAndLine(**box)

    if function != None:
        function(h)

    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    h.addLuminosityText()
    h.save()


if __name__ == "__main__":
    main()
