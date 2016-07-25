#!/usr/bin/env python

######################################################################
#
# This plot script is for comparing the embedded MC and normal MC
# within signal analysis. The corresponding python job
# configurations are
# * tauAnalysis_cfg.py
# * signalAnalysis_cfg.py with "tauEmbeddingInput=1"
# * signalAnalysis_cfg.py with "doTauEmbeddingLikePreselection=1"
# for embedded signal analysis, and normal signal analysis,
# respectively
#
# The development scripts are
# * plotTauEmbeddingMcTauMcMany
# * plotTauEmbeddingMcSignalAnalysisMcMany
#
# Authors: Matti Kortelainen
#
######################################################################

import os
import array
import math
import json
from optparse import OptionParser

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.cutstring import * # And, Not, Or
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tauEmbedding as tauEmbedding
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.aux as aux
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.systematics as systematics
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.OrderedDict as OrderedDict

analysisEmb = "signalAnalysis"
#analysisSig = "signalAnalysisTauEmbeddingLikePreselection"
analysisSig = "signalAnalysisGenuineTauTriggered"

dataEra = "Run2012ABCD"
#optMode = None
#optMode = "OptQCDTailKillerLoosePlus"

systematicsSigMC = dataset.Systematics(shapes=[
    "SystVarL1ETMMC",
    "SystVarTauTrgMC"
]) #additionalNormalizations={"foo": 0.1}) # just to test that syst is working also for normal
systematicsEmbMC = dataset.Systematics(shapes=[
    "SystVarMuonIdDataEff",
    "SystVarMuonTrgDataEff",
    "SystVarWTauMu",
    "SystVarEmbMTWeight",
], additionalNormalizations = {
    "CaloMETApproximation": 0.12
})

def main():
    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("--dirSig", dest="dirSig", default=None,
                      help="Path to signalAnalysisGenTau multicrab directory")
    parser.add_option("--nortau", dest="nortau", default=False, action="store_true",
                      help="Is Rtau cut disabled?")
    parser.add_option("--notrigger", dest="notrigger", default=False, action="store_true",
                      help="Is tau+MET trigger disabled?")
    parser.add_option("--dofit", dest="dofit", default=False, action="store_true",
                      help="Do the fit on mT slope on ttbar?")

    (opts, args) = parser.parse_args()
    if opts.dirSig is None:
        parser.error("--dirSig missing")

    dirEmb = "."
    dirSig = opts.dirSig

    global analysisSig, systematicsSigMC
    if opts.notrigger:
        analysisSig = analysisSig.replace("Triggered", "")
        systematicsSigMC = dataset.Systematics()

    # Apply TDR style
    style = tdrstyle.TDRStyle()

    styles.styles[1] = styles.StyleCompound([styles.styles[1], styles.StyleMarker(markerStyle=25)])

    histograms.cmsTextMode = histograms.CMSMode.SIMULATION_PRELIMINARY
#    histograms.cmsTextMode = histograms.CMSMode.SIMULATION
#    histograms.cmsTextMode = histograms.CMSMode.SIMULATION_UNPUBLISHED
#    histograms.cmsTextMode = histograms.CMSMode.UNPUBLISHED
    #histograms.createLegend.setDefaults(y1=0.93, y2=0.75, x1=0.52, x2=0.93)
    histograms.createLegend.setDefaults(textSize=0.04)
    histograms.createLegend.moveDefaults(dx=-0.25, dh=-0.2, dy=-0.12)

    histograms.createLegendRatio.setDefaults(ncolumns=2, textSize=0.08, columnSeparation=0.6)
    histograms.createLegendRatio.moveDefaults(dx=-0.48, dh=-0.1, dw=0.25)

    if opts.dofit:
        histograms.uncertaintyMode.set(histograms.uncertaintyMode.StatOnly)
        histograms.createLegendRatio.moveDefaults(dw=-0.25)
        plots._legendLabels["BackgroundStatError"] = "Emb. stat. unc."
        plots._legendLabels["BackgroundStatSystError"] = "Emb. stat.#oplussyst. unc."
    else:
        histograms.uncertaintyMode.set(histograms.uncertaintyMode.StatAndSyst)
#        plots._legendLabels["BackgroundStatError"] = "Norm. stat. unc."
#        plots._legendLabels["BackgroundStatSystError"] = "Norm. stat.#oplussyst. unc."
        plots._legendLabels["BackgroundStatError"] = "Non-emb. stat. unc."
        plots._legendLabels["BackgroundStatSystError"] = "Non-emb. stat.#oplussyst. unc."
    plots._legendLabels["Data"] = "Embedded data"
    plots._legendLabels["EWKMC"] = "EWK+t#bar{t}"
#    plots._legendLabels["EWKMC"] = "Non-emb. EWK+t#bar{t} with ^{}#tau_{h}"

    postfix =""
    if opts.dofit:
        postfix = "_fit"

    for optMode in [
#        "OptQCDTailKillerNoCuts",
        "OptQCDTailKillerLoosePlus",
#        "OptQCDTailKillerMediumPlus",
#        "OptQCDTailKillerTightPlus",
#            None
        ]:
        datasetsEmb = dataset.getDatasetsFromMulticrabCfg(directory=dirEmb, dataEra=dataEra, analysisName=analysisEmb, optimizationMode=optMode)
        datasetsSig = dataset.getDatasetsFromMulticrabCfg(directory=dirSig, dataEra=dataEra, analysisName=analysisSig, optimizationMode=optMode)
        doDataset(datasetsEmb, datasetsSig, optMode+postfix, opts)
        datasetsEmb.close()
        datasetsSig.close()

        tauEmbedding.writeToFile(optMode+postfix, "input.txt", "Embedded: %s\nSignal analysis (GenTau): %s\n" % (os.getcwd(), dirSig))

def doDataset(datasetsEmb, datasetsSig, outputDir, opts):
    global ind
    ind = 0

#    datasetsEmb.loadLuminosities() # not needed for pseudo-multicrab

    datasetsSig.updateNAllEventsToPUWeighted()
    datasetsEmb.updateNAllEventsToPUWeighted()

    plots.mergeRenameReorderForDataMC(datasetsEmb)
    plots.mergeRenameReorderForDataMC(datasetsSig)

    def mergeEWK(datasets):
        datasets.merge("EWKMC", ["WJets", "TTJets", "DYJetsToLL", "SingleTop", "Diboson"], keepSources=True)
    if not opts.notrigger:
        mergeEWK(datasetsSig)
        mergeEWK(datasetsEmb)

       
    plotter = tauEmbedding.CommonPlotter(outputDir, "mcembsig", drawPlotCommon)

    def dop(name, addData=False, **kwargs):
        doPlots(datasetsEmb, datasetsSig, name, plotter, outputDir, addData, opts, **kwargs)
#        doCounters(datasetsEmb, datasetsSig, name)

    if not opts.notrigger:
        dop("EWKMC") #, addData=True)
    dop("TTJets")
    return
    dop("WJets")
    dop("DYJetsToLL", mtOnly=False)
    dop("SingleTop", mtOnly=False)
    dop("Diboson", mtOnly=False)
#    dop("DYJetsToLL", mtOnly=True)
#    dop("SingleTop", mtOnly=True)
#    dop("Diboson", mtOnly=True)


#drawPlotCommon = tauEmbedding.PlotDrawerTauEmbeddingEmbeddedNormal(ylabel="Events / %.0f GeV", stackMCHistograms=False, log=True, addMCUncertainty=True, ratio=True, addLuminosityText=True)
drawPlotCommon = plots.PlotDrawer(ylabel="Events / %.0f", stackMCHistograms=False, log=True, addMCUncertainty=True,
                                  ratio=True, ratioType="errorScale", ratioCreateLegend=True,
                                  opts2={"ymin": 0, "ymax": 2},
                                  addLuminosityText=True, errorBarsX=True
)

def strIntegral(th1):
    return "%.1f" % aux.th1Integral(th1)

def doPlots(datasetsEmb, datasetsSig, datasetName, plotter, outputDir, addData, opts, mtOnly=False):
    dsetEmb = datasetsEmb.getDataset(datasetName)
    dsetSig = datasetsSig.getDataset(datasetName)
    dsetEmbData = datasetsEmb.getDataset("Data")
    lumi = dsetEmbData.getLuminosity()

    addEventCounts = False
#    addEventCounts = True

    def getDRH(dset, name, syst):
        if addData:
            return dset.getDatasetRootHisto(name)
        else:
            return dset.getDatasetRootHisto(syst.histogram(name))

    def createPlot(name):
        if mtOnly and "shapeTransverseMass" not in name:
            return None

        drhEmb = getDRH(dsetEmb, name, systematicsEmbMC)
        drhSig = getDRH(dsetSig, name, systematicsSigMC)
        drhEmb.normalizeToLuminosity(lumi)
        drhSig.normalizeToLuminosity(lumi)
        drhEmb.setName("Embedded")
        drhSig.setName("Normal")
        if addData:
            drhEmbData = getDRH(dsetEmbData, name, None)
            drhEmbData.setName("Embedded data")

        if "shapeTransverseMass" in name and "TTJets" in datasetName:
            doScaleFactors(drhSig.getHistogramWithUncertainties(), drhEmb.getHistogramWithUncertainties(), outputDir, opts)

        if addData:
            p = plots.ComparisonManyPlot(drhSig, [drhEmb, drhEmbData])
        else:
            p = plots.ComparisonManyPlot(drhSig, [drhEmb])
        p.setLuminosity(lumi)
        legLabel = plots._legendLabels.get(datasetName, datasetName)
        legEmb = "Embedded "+legLabel
        #legSig = "Normal "+legLabel
        #legSig = legLabel
        legSig = "Non-emb. %s with ^{}#tau_{h}" % legLabel
        if addEventCounts:
            legEmb += " ("+strIntegral(drhEmb.getHistogram())+")"
            legSig += " ("+strIntegral(drhSig.getHistogram())+")"
        p.histoMgr.setHistoLegendLabelMany({
                "Embedded": legEmb,
                "Normal": legSig,
                })
        #p.histoMgr.forEachHisto(styles.generator())
        hemb = p.histoMgr.getHisto("Embedded")
        hemb.setDrawStyle("HIST E")
        hemb.setLegendStyle("L")
        themb = hemb.getRootHisto()
        #styles.ttStyle.apply(themb)
        themb.SetLineColor(ROOT.kBlue)
        themb.SetLineWidth(2)
        themb.SetMarkerColor(themb.GetLineColor())
        themb.SetMarkerSize(0)
        hsig = p.histoMgr.getHisto("Normal")
        hsig.setLegendStyle("F")
        thsig = hsig.getRootHisto()
        thsig.SetFillColor(ROOT.kGray)
        thsig.SetLineColor(thsig.GetFillColor())
        histoOrder = ["Embedded", "Normal"]
        if addData:
            legData = "Embedded data"
            histoOrder.append("Embedded data")
            if addEventCounts:
                legData += " ("+strIntegral(drhEmbData.getHistogram())+")"
            p.histoMgr.setHistoLegendLabelMany({"Embedded data": legData})
            p.histoMgr.forHisto("Embedded data", styles.dataStyle)
            p.histoMgr.setHistoDrawStyle("Embedded data", "EP")
            p.histoMgr.setHistoLegendStyle("Embedded data", "P")
            p.histoMgr.reorderDraw(["Embedded data", "Embedded", "Normal"])
        if opts.dofit:
            p.setDrawOptions(ratioYlabel="Norm./Emb.", ratioInvert=True, ratioType="errorPropagation")
            if "shapeTransverseMass" in name and "TTJets" in datasetName:
                binning = systematics.getBinningForPlot("shapeTransverseMass")
                p.setDrawOptions(customizeBeforeSave=lambda p: doScaleFactorFit(p, outputDir),
                                 rebin=range(0, 160, 20) + binning[binning.index(160):]
                             )
        else:
#            p.setDrawOptions(ratioYlabel="Emb./Norm.")
            p.setDrawOptions(ratioYlabel="Emb./Non-emb.")
        p.histoMgr.reorder(histoOrder)
        return p

    def addEmbStatSyst(p):
        rhwu = p.histoMgr.getHisto("Embedded").getRootHistoWithUncertainties()
        embStatSyst = rhwu.getSystematicUncertaintyGraph(addStatistical=True)
        for i in xrange(0, embStatSyst.GetN()):
            embStatSyst.SetPointEXhigh(i, 0)
            embStatSyst.SetPointEXlow(i, 0)
        aux.copyStyle(rhwu.getRootHisto(), embStatSyst)
        p.appendPlotObject(histograms.HistoGraph(embStatSyst, "EmbStatSyst", legendStyle=None, drawStyle="[]"))
    drawPlotCommon.setDefaults(customizeBeforeDraw=addEmbStatSyst)

    custom = {
        "NBjets": {"moveLegend": {"dx": -0.3, "dy": -0.5}},
        "ImprovedDeltaPhiCutsBackToBackMinimum": {"moveLegend": {"dx": -0.3, "dy": -0.4}},
        "Njets_AfterMtSelections": {"moveLegend": {"dx": -0.3, "dy": -0.4}},
        "BtagDiscriminatorAfterMtSelections": {"moveLegend": {"dx": -0.3}},
        "METAfterMtSelections": {"moveLegend": {"dx": 0}},
        "shapeTransverseMass": {"opts": {"ymax": 4}},
    }
    if opts.nortau:
        for hname in ["SelectedTau_Rtau_AfterStandardSelections", "SelectedTau_Rtau_AfterMtSelections"]:
            binning = systematics._dataDrivenCtrlPlotBinning[hname]
            width = binning[1]-binning[0]
            nbins = int(binning[0] / width)
            systematics._dataDrivenCtrlPlotBinning[hname] = [x*width for x in range(0, nbins)] + binning
            custom[hname] = {"opts": {"xmin": 0}}



    plotter.plot(datasetName, createPlot, custom)

def doScaleFactorFit(p, outputDir):
    histos = filter(lambda h: "shapeTransverseMass" in h.getName() and not "_syst" in h.getName(), p.ratioHistoMgr.getHistos())

    if len(histos) != 1:
        for h in histos:
            print h.getName()
        raise Exception("Expecting 1 ratio histogram, got %d" % len(histos))

    ratio = histos[0]
    fitfunc = ROOT.TF1("sffit", "[0]*x+[1]", 0, 160)
    ratio.getRootHisto().Fit(fitfunc, "NR")
    fitfunc.SetLineColor(ROOT.kBlue)
    fitfunc.SetLineWidth(2)
    p.getPad2().cd()
    fitfunc.Draw("same")

    par0 = fitfunc.GetParameter(0)
    par1 = fitfunc.GetParameter(1)
    histograms.PlotText(0.2, 0.5, "f(x) = p_{0}x + p_{1}", size=17, color=ROOT.kBlue).Draw()
    histograms.PlotText(0.2, 0.35, "p_{0} = %.4g, p_{1} = %.4g" %(par0, par1), size=17, color=ROOT.kBlue).Draw()

    formula = "%.10g*x + %.10g" % (par0, par1)
    errors = "%.5g %.5g" % (fitfunc.GetParError(0)/par0, fitfunc.GetParError(1)/par1)
    tauEmbedding.writeToFile(outputDir, "mtcorrectionfit.txt", "formula %s   relative fit uncertainties %s" % (formula, errors))
    

def doScaleFactors(histoSig, histoEmb, outputDir, opts):
    binning = systematics._dataDrivenCtrlPlotBinning["shapeTransverseMass"]
    histoSig.Rebin(len(binning)-1, "newsig", array.array("d", binning))
    histoEmb.Rebin(len(binning)-1, "newemb", array.array("d", binning))

    grSig = histoSig.getSystematicUncertaintyGraph()
    grEmb = histoEmb.getSystematicUncertaintyGraph()

    hSig = histoSig.getRootHisto()
    hEmb = histoEmb.getRootHisto()

    scaleFactors = []
    scaleFactors_stat = []

    identities = []

    def equal(a, b):
        if a == 0.0:
            return b == 0.0
        return abs((a-b)/a) < 0.0001

    for i in xrange(0, grSig.GetN()):
        lowEdge = grSig.GetX()[i]-grSig.GetErrorXlow(i)

        sig_val = grSig.GetY()[i]
        sig_err_up = grSig.GetErrorYhigh(i)
        sig_err_down = grSig.GetErrorYlow(i)
        emb_val = grEmb.GetY()[i]
        emb_err_up = grEmb.GetErrorYhigh(i)
        emb_err_down = grEmb.GetErrorYlow(i)

        # Employ count
        cemb = dataset.Count(emb_val, emb_err_up, emb_err_down)
        csig = dataset.Count(sig_val, sig_err_up, sig_err_down)
        csig.divide(cemb)

        cemb_stat = dataset.Count(hEmb.GetBinContent(i+1), hEmb.GetBinError(i+1))
        csig_stat = dataset.Count(hSig.GetBinContent(i+1), hSig.GetBinError(i+1))
        csig_stat.divide(cemb_stat)

        if not equal(lowEdge, hEmb.GetBinLowEdge(i+1)):
            raise Exception("Low edges not equal (%.10g vs %.10g)" % (lowEdge, hEmb.GetBinLowEdge(i+1)))
        if not equal(csig.value(), csig_stat.value()):
            raise Exception("Values not equal (%.10g vs %.10g)" % (csig.value(), csig_stat.value()))

        print "bin %.1f, sf %.7f +%.7f -%.7f (stat +-%.7f)" % (lowEdge, csig.value(), csig.uncertainty(), csig.systUncertainty(), csig_stat.uncertainty())

        d = OrderedDict.OrderedDict()
        d["mt"] = lowEdge
        d["efficiency"] = csig.value()
        d["uncertaintyPlus"] = csig.uncertainty()
        d["uncertaintyMinus"] = csig.systUncertainty()
        scaleFactors.append(d)
        d = OrderedDict.OrderedDict()
        d["mt"] = lowEdge
        d["efficiency"] = csig.value()
        d["uncertaintyPlus"] = csig_stat.uncertainty()
        d["uncertaintyMinus"] = csig_stat.uncertainty()
        scaleFactors_stat.append(d)
        d = OrderedDict.OrderedDict()
        d["mt"] = lowEdge
        d["efficiency"] = 1.0
        d["uncertaintyPlus"] = 0.0
        d["uncertaintyMinus"] = 0.0
        identities.append(d)

    par = OrderedDict.OrderedDict()
    par2 = OrderedDict.OrderedDict()
    par2["firstRun"] = 1 # to support also dataEfficiency in MC
    par2["lastRun"] = 208686
    par2["luminosity"] = 1 # dummy value, not used for anything
    par2["bins"] = scaleFactors
    par["Run2012ABCD"] = par2
    par2 = OrderedDict.OrderedDict()
    par2["firstRun"] = 1 # to support also dataEfficiency in MC
    par2["lastRun"] = 208686
    par2["luminosity"] = 1 # dummy value, not used for anything
    par2["bins"] = scaleFactors_stat
    par["Run2012ABCD_statOnly"] = par2

    ret = OrderedDict.OrderedDict()
    ret["_multicrab_embedded"] = os.getcwd()
    ret["_multicrab_signalAnalysisGenTau"] = opts.dirSig

    ret["dataParameters"] = par

    ret["mcParameters"] = {"Run2012ABCD": {"bins": identities}}

    tauEmbedding.writeToFile(outputDir, "embedding_mt_weight.json", json.dumps(ret, indent=2))

    


def doTauCounters(datasetsEmb, datasetsSig, datasetName, ntupleCacheEmb, ntupleCacheSig, normalizeEmb=True):
    lumi = datasetsEmb.getLuminosity()

    # Take unweighted counters for embedded, to get a handle on the muon isolation efficiency
    eventCounterEmb = tauEmbedding.EventCounterMany(datasetsEmb, counters="/"+tauAnalysisEmb+"Counters", normalize=normalizeEmb)
    eventCounterSig = counter.EventCounter(datasetsSig, counters="/"+tauAnalysisEmb+"Counters")

    def isNotThis(name):
        return name != datasetName

    eventCounterEmb.removeColumns(filter(isNotThis, datasetsEmb.getAllDatasetNames()))
    eventCounterSig.removeColumns(filter(isNotThis, datasetsSig.getAllDatasetNames()))

    eventCounterEmb.mainCounterAppendRows(ntupleCacheEmb.histogram("counters/weighted/counter"))
    eventCounterSig.getMainCounter().appendRows(ntupleCacheSig.histogram("counters/weighted/counter"))

    eventCounterSig.normalizeMCToLuminosity(lumi)

    table = counter.CounterTable()
    col = eventCounterEmb.getMainCounterTable().getColumn(name=datasetName)
    col.setName("Embedded")
    table.appendColumn(col)
    col = eventCounterSig.getMainCounterTable().getColumn(name=datasetName)
    col.setName("Normal")
    table.appendColumn(col)

    lastCountEmb = table.getCount(colName="Embedded", irow=table.getNrows()-1)
    lastCountNormal = table.getCount(colName="Normal", irow=table.getNrows()-1)

    postfix = ""
    if not normalizeEmb:
        postfix="_notEmbNormalized"

    effFormat = counter.TableFormatLaTeX(counter.CellFormatTeX(valueFormat="%.4f", withPrecision=2))
    countFormat = counter.TableFormatText(counter.CellFormatText(valueFormat="%.4f"),
                                          #columnSeparator="  ;"
                                          )

    fname = "counters_tau_"+datasetName+postfix+".txt"
    f = open(fname, "w")
    f.write(table.format(countFormat))
    f.write("\n")

    try:
        ratio = lastCountNormal.clone()
        ratio.divide(lastCountEmb)
        f.write("Normal/embedded = %.4f +- %.4f\n\n" % (ratio.value(), ratio.uncertainty()))
    except ZeroDivisionError:
        pass

    f.close()
    print "Printed tau counters to", fname
    
    if not normalizeEmb:
        return

    tableEff = counter.CounterTable()
    tableEff.appendColumn(counter.efficiencyColumn("Embedded eff", table.getColumn(name="Embedded")))
    tableEff.appendColumn(counter.efficiencyColumn("Normal eff", table.getColumn(name="Normal")))

    embeddingMuonIsolationEff = tableEff.getCount(rowName="tauEmbeddingMuonsCount", colName="Embedded eff")
    embeddingTauIsolationEff = tableEff.getCount(rowName="Isolation", colName="Embedded eff")
    embeddingTotalIsolationEff = embeddingMuonIsolationEff.clone()
    embeddingTotalIsolationEff.multiply(embeddingTauIsolationEff)

    # Remove unnecessary rows
    rowNames = [
#        "All events",
        "Decay mode finding",
        "Eta cut",
        "Pt cut",
        "Leading track pt",
        "Against electron",
        "Against muon",
        "Isolation",
        "One prong",
        "Rtau",
    ]
    tableEff.keepOnlyRows(rowNames)
    rowIndex = tableEff.getRowNames().index("Isolation")
    tableEff.insertRow(rowIndex, counter.CounterRow("Mu isolation (emb)", ["Embedded eff", "Normal eff"],
                                                    [embeddingMuonIsolationEff, None]))
    tableEff.insertRow(rowIndex+1, counter.CounterRow("Tau isolation (emb)", ["Embedded eff", "Normal eff"],
                                                      [embeddingTauIsolationEff, None]))
    tableEff.setCount2(embeddingTotalIsolationEff, rowName="Isolation", colName="Embedded eff")
    #tableEff.setCount2(None, rowName="pT > 15", colName="Normal eff")

    #print table.format(effFormat)
    fname = "counters_tau_"+datasetName+"_eff.txt"
    f = open(fname, "w")
    f.write(tableEff.format(effFormat))
    f.write("\n")
    f.close()
    print "Printed tau efficiencies to", fname

def doCounters(datasetsEmb, datasetsSig, datasetName, normalizeEmb=True):
    lumi = datasetsEmb.getLuminosity()

    # Counters
    eventCounterEmb = tauEmbedding.EventCounterMany(datasetsEmb, normalize=normalizeEmb) #, counters=analysisEmb+"/counters")
    eventCounterSig = counter.EventCounter(datasetsSig)

    def isNotThis(name):
        return name != datasetName

    eventCounterEmb.removeColumns(filter(isNotThis, datasetsEmb.getAllDatasetNames()))
    eventCounterSig.removeColumns(filter(isNotThis, datasetsSig.getAllDatasetNames()))
    eventCounterSig.normalizeMCToLuminosity(lumi)

    tdCount = dataset.TreeDraw("dummy", weight=tauEmbedding.signalNtuple.weightBTagging)
    tdCountMET = tdCount.clone(weight=tauEmbedding.signalNtuple.weight, selection=tauEmbedding.signalNtuple.metCut)
    tdCountBTagging = tdCount.clone(selection=And(tauEmbedding.signalNtuple.metCut, tauEmbedding.signalNtuple.bTaggingCut))
    tdCountDeltaPhi160 = tdCount.clone(selection=And(tauEmbedding.signalNtuple.metCut, tauEmbedding.signalNtuple.bTaggingCut, tauEmbedding.signalNtuple.deltaPhi160Cut))
    tdCountDeltaPhi130 = tdCount.clone(selection=And(tauEmbedding.signalNtuple.metCut, tauEmbedding.signalNtuple.bTaggingCut, tauEmbedding.signalNtuple.deltaPhi130Cut))
    def addRow(name, td):
        tdEmb = td.clone(tree=analysisEmb+"/tree")
        tdSig = td.clone(tree=analysisSig+"/tree")
        eventCounterEmb.mainCounterAppendRow(name, tdEmb)
        eventCounterSig.getMainCounter().appendRow(name, tdSig)

    # addRow("JetsForEffs", tdCount.clone(weight=tauEmbedding.signalNtuple.weight))
    # addRow("METForEffs", tdCountMET)
    # addRow("BTagging (SF)", tdCountBTagging)
    # addRow("DeltaPhi < 160", tdCountDeltaPhi160)
    # addRow("BTagging (SF) again", tdCountBTagging)
    # addRow("DeltaPhi < 130", tdCountDeltaPhi130)

    table = counter.CounterTable()
    col = eventCounterEmb.getMainCounterTable().getColumn(name=datasetName)
    col.setName("Embedded")
    table.appendColumn(col)
    col = eventCounterSig.getMainCounterTable().getColumn(name=datasetName)
    col.setName("Normal")
    table.appendColumn(col)

    tableTau = counter.CounterTable()
    tmp = "TauIDPassedEvt::TauSelection_HPS"
    col = eventCounterEmb.getSubCounterTable(tmp).getColumn(name=datasetName)
    col.setName("Embedded")
    tableTau.appendColumn(col)
    col = eventCounterSig.getSubCounterTable(tmp).getColumn(name=datasetName)
    col.setName("Normal")
    tableTau.appendColumn(col)

    postfix = ""
    if not normalizeEmb:
        postfix="_notEmbNormalized"

    fname = "counters_selections_%s%s.txt" % (datasetName, postfix)
    f = open(fname, "w")
    f.write(table.format())
    f.write("\n")
    f.write(tableTau.format())
    f.close()
    print "Printed selection counters to", fname

    if not normalizeEmb:
        return


    # Calculate efficiencies
    table.keepOnlyRows(["njets", "MET", "btagging", "btagging scale factor", "DeltaPhi(Tau,MET) upper limit"])
    # btag SF efficiency w.r.t. MET 
    row = table.getRow(name="MET")
    row.setName("METForEff")
    table.insertRow(3, row) 

    tableEff = counter.CounterTable()
    tableEff.appendColumn(counter.efficiencyColumn("Embedded eff", table.getColumn(name="Embedded")))
    tableEff.appendColumn(counter.efficiencyColumn("Normal eff", table.getColumn(name="Normal")))
    tableEff.removeRow(name="METForEff")

    effFormat = counter.TableFormatText(counter.CellFormatTeX(valueFormat='%.4f', withPrecision=2))

#    print table.format(effFormat)

    fname = "counters_selections_%s_eff.txt"%datasetName
    f = open(fname, "w")
    f.write(tableEff.format(effFormat))
    f.close()
    print "Printed selection efficiencies to", fname

if __name__ == "__main__":
    main()
