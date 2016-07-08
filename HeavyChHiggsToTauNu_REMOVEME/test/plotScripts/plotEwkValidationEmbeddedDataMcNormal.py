#!/usr/bin/env python

######################################################################
#
# This plot script is for comparing the embedded data + residual MC,
# embedded MC + residual MC, and normal MC within the signal analysis.
# The corresponding python job
# configurations are
# * signalAnalysis_cfg.py with "doPat=1 tauEmbeddingInput=1"
# * signalAnalysis_cfg.py with "doTauEmbeddingLikePreselection=1"
# for embedding+signal analysis and signal analysis, respectively
#
# The development scripts are
# * plotTauEmbeddingMcSignalAnalysisMcMany
# * plotTauEmbeddingSignalAnalysisMany
#
# Authors: Matti Kortelainen
#
######################################################################

import os
import array
import math
import copy
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

analysisEmb = "signalAnalysis"
analysisSig = "signalAnalysisGenuineTauTriggered" # require that the selected tau is genuine, valid comparison after njets

dataEra = "Run2012ABCD"

class SystematicsSigMC:
    def __init__(self):
        self._systematics = dataset.Systematics(shapes=[
            "SystVarL1ETMMC",
            "SystVarTauTrgMC",
            "SystVarJES",
            "SystVarJER",
            "SystVarMET",
            "SystVarBTagSF",
            "SystVarPUWeight",
            "SystVarTopPtWeight",
        ], additionalNormalizations = {
            "LeptonVeto": systematics.getLeptonVetoUncertainty("Dummy").getUncertaintyMax(),
            "Luminosity": systematics.getLuminosityUncertainty().getUncertaintyMax()
        })
        self._cache = {}

    def histogram(self, dsetName, name):
        if not dsetName in self._cache:
            cl = self._systematics.clone()
            cl.append(additionalNormalizations = {"CrossSection": systematics.getCrossSectionUncertainty(dsetName).getUncertaintyMax()})
            self._cache[dsetName] = cl

        return self._cache[dsetName].histogram(name)
systematicsSigMC = SystematicsSigMC()

systematicsEmbData = dataset.Systematics(shapes=[
    "SystVarMuonIdDataEff",
    "SystVarMuonTrgDataEff",
    "SystVarWTauMu",
    "SystVarEmbMTWeight",
], additionalNormalizations = {
    "CaloMETApproximation": 0.12,
    "QCDContamination": 0.02,
})


plotStyles = styles.styles[0:2]
plotStyles[0] = styles.StyleCompound([plotStyles[0], styles.StyleMarker(markerStyle=21, markerSize=1.2)])

def main():
    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("--dirSig", dest="dirSig", default=None,
                      help="Path to signalAnalysisGenTau multicrab directory")

    (opts, args) = parser.parse_args()
    if opts.dirSig is None:
        parser.error("--dirSig missing")

    dirEmb = "."
    dirSig = opts.dirSig

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    #histograms.createLegend.setDefaults(y1=0.93, y2=0.75, x1=0.52, x2=0.93)
#    histograms.createLegend.moveDefaults(dx=-0.1, dh=-0.2)
#    histograms.createLegend.moveDefaults(dx=-0.15, dy=-0.01, dh=+0.05)
#    histograms.uncertaintyMode.set(histograms.uncertaintyMode.StatOnly)
    histograms.uncertaintyMode.set(histograms.uncertaintyMode.StatAndSyst)
#    histograms.createLegendRatio.moveDefaults(dh=-0.1, dx=-0.53)
#    histograms.createLegendRatio.moveDefaults(dx=-0.08)
    histograms.createLegend.setDefaults(textSize=0.04)
    histograms.createLegend.moveDefaults(dx=-0.25, dh=0.1)#, dh=-0.05) # QCD removed

    histograms.createLegendRatio.setDefaults(ncolumns=2, textSize=0.08, columnSeparation=0.3)
    histograms.createLegendRatio.moveDefaults(dx=-0.35, dh=-0.1, dw=0.25)

#    plots._legendLabels["BackgroundStatError"] = "Norm. stat. unc."
    plots._legendLabels["BackgroundStatError"] = "Sim. stat. unc" #"Norm. stat. unc."
    plots._legendLabels["BackgroundStatSystError"] = "Sim. stat.#oplussyst. unc." # "Norm. stat.#oplussyst. unc."

    plots._legendLabels["Data"] = "Embedded data"

    for optMode in [
#        "OptQCDTailKillerNoCuts",
        "OptQCDTailKillerLoosePlus",
#        "OptQCDTailKillerMediumPlus",
#        "OptQCDTailKillerTightPlus",
#            None
    ]:
        datasetsEmb = dataset.getDatasetsFromMulticrabCfg(directory=dirEmb, dataEra=dataEra, analysisName=analysisEmb, optimizationMode=optMode)
        datasetsSig = dataset.getDatasetsFromMulticrabCfg(directory=dirSig, dataEra=dataEra, analysisName=analysisSig, optimizationMode=optMode)
        doDataset(datasetsEmb, datasetsSig, optMode)
        datasetsEmb.close()
        datasetsSig.close()

        tauEmbedding.writeToFile(optMode+"_embdatasigmc", "input.txt", "Embedded: %s\nSignal analysis (GenTau): %s\n" % (os.getcwd(), dirSig))


def doDataset(datasetsEmb, datasetsSig, optMode):
    datasetsSig.updateNAllEventsToPUWeighted()
    datasetsEmb.updateNAllEventsToPUWeighted()

    plots.mergeRenameReorderForDataMC(datasetsEmb)
    plots.mergeRenameReorderForDataMC(datasetsSig)

    plotter = tauEmbedding.CommonPlotter(optMode+"_embdatasigmc", "embdatasigmc", drawPlotCommon)
    doPlots(datasetsEmb, datasetsSig, plotter, optMode)

drawPlotCommon = plots.PlotDrawer(ylabel="Events / %.0f", stackMCHistograms=True, log=True, addMCUncertainty=True,
                                  opts2={"ymin": 0, "ymax": 2},
                                  ratio=True, ratioType="errorScale", ratioCreateLegend=True, ratioYlabel="Data/Sim.",
                                  addLuminosityText=True)

def doPlots(datasetsEmb, datasetsSig, plotter, optMode):
    lumi = datasetsEmb.getDataset("Data").getLuminosity()

    def createPlot(name):
        drhData = datasetsEmb.getDataset("Data").getDatasetRootHisto(systematicsEmbData.histogram(name))
        drhMCs = [d.getDatasetRootHisto(systematicsSigMC.histogram(d.getName(), name)) for d in datasetsSig.getMCDatasets()]

        p = plots.DataMCPlot2([drhData]+drhMCs)
        p.histoMgr.normalizeMCToLuminosity(lumi)
        # by default pseudo-datasets lead to MC histograms, for these
        # plots we want to treat Data as data
        p.histoMgr.getHisto("Data").setIsDataMC(True, False)
        p.setDefaultStyles()
        return p

    def addDataStatSyst(p):
        dataStatSyst = p.histoMgr.getHisto("Data").getRootHistoWithUncertainties().getSystematicUncertaintyGraph(addStatistical=True)
        for i in xrange(0, dataStatSyst.GetN()):
            dataStatSyst.SetPointEXhigh(i, 0)
            dataStatSyst.SetPointEXlow(i, 0)
        p.appendPlotObject(histograms.HistoGraph(dataStatSyst, "DataStatSyst", legendStyle=None, drawStyle="[]"))
    drawPlotCommon.setDefaults(customizeBeforeDraw=addDataStatSyst)

    custom = {
        "Njets_AfterStandardSelections": {"moveLegend": {"dx": 0.1, "dy": 0}},
        "NBjets": {"moveLegend": {"dx": 0.1, "dy": 0}},
        "MET": {"moveLegend": {"dx": 0.1, "dy": 0}},
        "ImprovedDeltaPhiCutsBackToBackMinimum": {"moveLegend": {"dx": -0.3, "dy": -0.4}},
        "Njets_AfterMtSelections": {"moveLegend": {"dx": -0.3, "dy": -0.3}},
        "METAfterMtSelections": {"moveLegend": {"dx": 0.15, "dy": 0}},
        "NBJetsAfterMtSelections": {"moveLegend": {"dx": 0.1}},
        "BJetPtAfterMtSelections": {"moveLegend": {"dx": 0.1}},
        "BtagDiscriminatorAfterMtSelections": {"moveLegend": {"dx": -0.3, "dy": 0}},
        "ImprovedDeltaPhiCutsCollinearMinimumAfterMtSelections": {"moveLegend": {"dx": 0, "dy": 0}},
        "shapeTransverseMass": {"moveLegend": {"dy": -0.12}},
        "shapeTransverseMass_log": {"moveLegend": {"dy": -0.12}},
    }

    plotter.plot(None, createPlot, custom)


######################################## OLD STUFF

def oldstuff():
    # Create the dataset objects
    datasetsEmb = tauEmbedding.DatasetsMany(dirEmbs, analysisEmb+"Counters", normalizeMCByLuminosity=True)
    datasetsSig = dataset.getDatasetsFromMulticrabCfg(cfgfile=dirSig+"/multicrab.cfg", counters=analysisSig+"Counters")
    datasetsSig.updateNAllEventsToPUWeighted()

    # Remove signal and W+3jets datasets
    datasetsEmb.remove(filter(lambda name: "HplusTB" in name, datasetsEmb.getAllDatasetNames()))
    datasetsEmb.remove(filter(lambda name: "TTToHplus" in name, datasetsEmb.getAllDatasetNames()))
    datasetsEmb.remove(filter(lambda name: "W3Jets" in name, datasetsEmb.getAllDatasetNames()))

    # Keep WW separately, Diboson is WZ+ZZ
    #del plots._datasetMerge["WW"]

    datasetsEmb.forEach(lambda mgr: plots.mergeRenameReorderForDataMC(mgr, keepSourcesMC=True))
    datasetsEmb.setLumiFromData()
    plots.mergeRenameReorderForDataMC(datasetsSig, keepSourcesMC=True)

    # Merge EWK datasets
    def mergeEWK(datasets):
        datasets.merge("EWKMC", ["WJets", "TTJets", "DYJetsToLL", "SingleTop", "Diboson", "WW"], keepSources=True)
        datasets.merge("EWKMC", ["Diboson", "WW"], keepSources=True)
    mergeEWK(datasetsSig)
    datasetsEmb.forEach(mergeEWK)
    plots._legendLabels["EWKMC"] = "EWK"

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    histograms.cmsTextMode = histograms.CMSMode.NONE
    ROOT.gStyle.SetEndErrorSize(5)
    histograms.createLegend.setDefaults(y1=0.93, y2=0.75, x1=0.49, x2=0.9)
    tauEmbedding.normalize=True
    tauEmbedding.era = "Run2011AB"

    # Create datasets with residuals
    # Define DYJetsToLL and WW be the datasets where residuals are calculated
    # Define Data and EWKMC be the datasets to which the residuals are added
    # I.e. Data will be embedded data + res. MC, and EWKMC embedded MC + res. MC
    datasetsEmbCorrected = tauEmbedding.DatasetsResidual(datasetsEmb, datasetsSig, analysisEmb, analysisSig, ["DYJetsToLL", "WW"], totalNames=["Data", "EWKMC"])

    doPlots(datasetsEmbCorrected, datasetsSig, "EWKMC")
    doCounters(datasetsEmbCorrected, datasetsSig)

def doPlotsOld(datasetsEmb, datasetsSig, datasetName):
    lumi = datasetsEmb.getLuminosity()
    isCorrected = isinstance(datasetsEmb, tauEmbedding.DatasetsResidual)
    postfix = "_residual"
    
    createPlot = tauEmbedding.PlotCreatorMany(analysisEmb, analysisSig, datasetsEmb, datasetsSig, datasetName, plotStyles, addData=True)
    drawPlot = tauEmbedding.PlotDrawerTauEmbeddingEmbeddedNormal(ratio=True, log=True, addLuminosityText=True)
    def createDrawPlot(name, *args, **kwargs):
        p = createPlot(name)
        drawPlot(p, *args, **kwargs)

    prefix = "embdatasigmc"+postfix+"_"+datasetName+"_"

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

    moveLegend = {"dy":-0.6, "dx":-0.2}
    opts = {
        "SingleTop": {"ymax": 1.8}
        }.get(datasetName, {"ymaxfactor": 1.4})
    if datasetName != "TTJets":
        moveLegend = {"dx": -0.32}
    drawControlPlot("SelectedTau_eta_AfterStandardSelections", "#tau-jet #eta", opts=update(opts, {"xmin": -2.2, "xmax": 2.2}), ylabel="Events / %.1f", rebin=4, log=False, moveLegend=moveLegend)

    drawControlPlot("SelectedTau_LeadingTrackPt_AfterStandardSelections", "#tau-jet ldg. charged particle p_{T} (GeV/c)", opts=update(opts, {"xmax": 300}), rebin=2, cutBox={"cutValue": 20, "greaterThan": True})

    opts = {"ymin": 1e-1, "ymaxfactor": 5}
    moveLegend = {"dx": -0.22}
    if datasetName == "Diboson":
        opts["ymin"] = 1e-2
    drawControlPlot("SelectedTau_Rtau_AfterStandardSelections", "R_{#tau} = p^{ldg. charged particle}/p^{#tau jet}", opts=update(opts, {"xmin": 0.65, "xmax": 1.05}), rebin=5, ylabel="Events / %.2f", moveLegend=moveLegend, cutBox={"cutValue":0.7, "greaterThan":True})

    opts = optsdef
    drawControlPlot("Njets_AfterStandardSelections", "Number of jets", ylabel="Events")

    # After Njets
    drawControlPlot("MET", "Uncorrected PF E_{T}^{miss} (GeV)", rebin=5, opts=update(opts, {"xmax": 400}), cutLine=50,
                    moveLegend={"dx": -0.2, "dy": -0.55}
                    )

    # after MET
    moveLegend = {
        "WJets": {},
        "DYJetsToLL": {},
        "SingleTop": {},
        "Diboson": {}
        }.get(datasetName, {"dx": -0.2, "dy": -0.5})
    drawControlPlot("NBjets", "Number of selected b jets", opts=update(opts, {"xmax": 6}), ylabel="Events", moveLegend=moveLegend, cutLine=1)

    # Tree cut definitions
    treeDraw = dataset.TreeDraw("dummy", weight=tauEmbedding.signalNtuple.weightBTagging)
    tdMt = treeDraw.clone(varexp="%s >>tmp(15,0,300)" % tauEmbedding.signalNtuple.mtExpression)
    tdDeltaPhi = treeDraw.clone(varexp="%s >>tmp(18, 0, 180)" % tauEmbedding.signalNtuple.deltaPhiExpression)

    # DeltapPhi
    xlabel = "#Delta#phi(#tau jet, E_{T}^{miss}) (^{o})"
    def customDeltaPhi(h):
        yaxis = h.getFrame().GetYaxis()
        yaxis.SetTitleOffset(0.8*yaxis.GetTitleOffset())
    opts = {
        "WJets": {"ymax": 20},
        "DYJetsToLL": {"ymax": 5},
        "SingleTop": {"ymax": 2},
        "Diboson": {"ymax": 0.6},
        }.get(datasetName, {"ymaxfactor": 1.2})
    opts2 = {
        "WJets": {"ymin": 0, "ymax": 3}
        }.get(datasetName, opts2def)
    selection = And(*[getattr(tauEmbedding.signalNtuple, cut) for cut in ["metCut", "bTaggingCut"]])
    drawPlot(createPlot(tdDeltaPhi.clone(selection=selection)), prefix+"deltaPhi_3AfterBTagging", xlabel, log=False, opts=opts, opts2=opts2, ylabel="Events / %.0f^{o}", function=customDeltaPhi, moveLegend={"dx":-0.22}, cutLine=[130, 160])


    # After all cuts
    selection = And(*[getattr(tauEmbedding.signalNtuple, cut) for cut in ["metCut", "bTaggingCut", "deltaPhi160Cut"]])

    #opts = {"ymaxfactor": 1.4}
    opts = {}

    opts = {
        "EWKMC": {"ymax": 40},
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
        }.get(datasetName, {"ymin": 0, "ymax": 2})
    
    p = createPlot(tdMt.clone(selection=selection))
    histograms.cmsTextMode = histograms.CMSMode.PRELIMINARY
    p.appendPlotObject(histograms.PlotText(0.6, 0.7, "#Delta#phi(#tau jet, E_{T}^{miss}) < 160^{o}", size=20))
    drawPlot(p, prefix+"transverseMass_4AfterDeltaPhi160", "m_{T}(#tau jet, E_{T}^{miss}) (GeV/c^{2})", opts=opts, opts2=opts2, ylabel="Events / %.0f GeV/c^{2}", log=False)
    histograms.cmsTextMode = histograms.CMSMode.NONE

def doCounters(datasetsEmb, datasetsSig):
    rows = ["njets", "MET", "btagging scale factor", "deltaPhiTauMET<160", "deltaPhiTauMET<130"]
    residuals = ["DYJetsToLL residual", "WW residual"]

    # Normal MC
    eventCounterNormal = counter.EventCounter(datasetsSig)
    eventCounterNormal.normalizeMCToLuminosity(datasetsEmb.getLuminosity())
    tableNormal = eventCounterNormal.getMainCounterTable()
    tableNormal.keepOnlyRows(rows)

    # Embedded data and MC, residual MC
    eventCounter = tauEmbedding.EventCounterResidual(datasetsEmb)
    table = eventCounter.getMainCounterTable()
    table.keepOnlyRows(rows)

    # Build the result
    result = counter.CounterTable()

    c = table.getColumn(name="Data")
    c.setName("Embedded data")
    result.appendColumn(c)
    #result.appendColumn(table.getColumn(name="EWKMC"))
    for name in residuals:
        result.appendColumn(table.getColumn(name=name))

    result.appendColumn(counter.sumColumn("Emb. data + res. MC", [table.getColumn(name=name) for name in ["Data"]+residuals]))
    result.appendColumn(counter.sumColumn("Emb. MC + res. MC", [table.getColumn(name=name) for name in ["EWKMC"]+residuals]))

    c = tableNormal.getColumn(name="EWKMC")
    c.setName("Normal MC")
    result.appendColumn(c)

    # Final formatting
    result.renameRows({"njets": "tau-jet identification",
                      "btagging scale factor": "b tagging"
                      })

    cellFormat = counter.TableFormatLaTeX(counter.CellFormatTeX(valueFormat='%.4f', withPrecision=2))
    print result.format(cellFormat)

if __name__ == "__main__":
    main()
