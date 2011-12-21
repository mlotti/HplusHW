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

import array

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import plotTauEmbeddingSignalAnalysis as tauEmbedding

#analysisEmb = "signalAnalysis"
#analysisSig = "signalAnalysis"
analysisEmb = "signalAnalysisCaloMet60TEff"
analysisSig = "signalAnalysisGenuineTau"

def main():
    dirEmbs = [
        ".",
        "../multicrab_signalAnalysis_Met50_debug_seedTest1_Run2011A_111216_104833",
        "../multicrab_signalAnalysis_Met50_debug_seedTest2_Run2011A_111216_121911",
#        "../multicrab_signalAnalysis_Met50_v13_2_seedTest1_Run2011A_111219_213247",
#        "../multicrab_signalAnalysis_v13_2_seedTest2_Run2011A_111220_000831",
        ]

#    dirSig = "../../multicrab_compareEmbedding_Run2011A_111201_143238"
    dirSig = "../../multicrab_compareEmbedding_Run2011A_111219_185818"
    
    datasetsEmb = DatasetsMany(dirEmbs, analysisEmb+"Counters")
    datasetsSig = dataset.getDatasetsFromMulticrabCfg(cfgfile=dirSig+"/multicrab.cfg", counters=analysisSig+"Counters")

    datasetsEmb.forEach(plots.mergeRenameReorderForDataMC)
    datasetsEmb.setLumiFromData()
    plots.mergeRenameReorderForDataMC(datasetsSig)

    def mergeEWK(datasets):
        datasets.merge("EWKMC", ["WJets", "TTJets", "DYJetsToLL", "SingleTop", "Diboson"], keepSources=True)
        #datasets.merge("EWKMC", ["WJets", "TTJets"], keepSources=True)
    mergeEWK(datasetsSig)
    datasetsEmb.forEach(mergeEWK)
    plots._legendLabels["EWKMC"] = "EWK MC"

    style = tdrstyle.TDRStyle()
    ROOT.gStyle.SetEndErrorSize(5)
    histograms.createLegend.setDefaults(y1=0.93, y2=0.75, x1=0.52, x2=0.93)

    tauEmbedding.normalize=True
    tauEmbedding.era = "Run2011A"

    #doPlots(datasetsEmb, datasetsSig, "TTJets")
    #doPlots(datasetsEmb, datasetsSig, "WJets")
    #doPlots(datasetsEmb, datasetsSig, "DYJetsToLL")
    #doPlots(datasetsEmb, datasetsSig, "Data")
    #doPlots(datasetsEmb, datasetsSig, "EWKMC")
    #doPlots(datasetsEmb, datasetsSig, "EWKMC", doData=True, postfix="_data")

    doPlotsData(datasetsEmb)

def doPlots(datasetsEmb, datasetsSig, datasetName, doData=False, postfix=""):
    lumi = datasetsEmb.getLumi()
    
    def createPlot(name):
        name2Emb = name
        name2Sig = name
        if isinstance(name, basestring):
            name2Emb = analysisEmb+"/"+name
            name2Sig = analysisSig+"/"+name
        else:
            name2Emb = name.clone(tree=analysisEmb+"/tree")
            name2Sig = name.clone(tree=analysisSig+"/tree")

        (emb, embVar) = datasetsEmb.getHistogram(datasetName, name2Emb)
        sig = datasetsSig.getDataset(datasetName).getDatasetRootHisto(name2Sig)
        sig.normalizeToLuminosity(lumi)
        sig = sig.getHistogram()

        emb.SetName("Embedded")
        sig.SetName("Normal")

        p = None
        sty = None
        if doData:
            (embData, embDataVar) = datasetsEmb.getHistogram("Data", name2Emb)
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

        p.histoMgr.setHistoLegendLabelMany({
                "Embedded":     "Embedded "+plots._legendLabels[datasetName],
                "Normal":       "Normal "+plots._legendLabels[datasetName],
                "EmbeddedData": "Embedded data",
                })
        p.histoMgr.forEachHisto(styles.Generator(sty))
        if doData:
            plots.copyStyle(p.histoMgr.getHisto("EmbeddedData").getRootHisto(), embDataVar)
            embDataVar.SetMarkerStyle(2)
            p.embeddingDataVariation = embDataVar
        else:
            plots.copyStyle(p.histoMgr.getHisto("Embedded").getRootHisto(), embVar)
            embVar.SetMarkerStyle(2)
            p.embeddingVariation = embVar

        return p

    def createDrawPlot(name, *args, **kwargs):
        p = createPlot(name)
        drawPlot(p, *args, **kwargs)

    treeDraw = dataset.TreeDraw("dummy", weight="weightPileup*weightTrigger*weightBTagging")
    tdMt = treeDraw.clone(varexp="sqrt(2 * tau_p4.Pt() * met_p4.Et() * (1-cos(tau_p4.Phi()-met_p4.Phi()))) >>tmp(20,0,400)")

    # After all cuts
    metCut = "(met_p4.Et() > 50)"
    bTaggingCut = "passedBTagging"
    deltaPhi160Cut = "(acos( (tau_p4.Px()*met_p4.Px()+tau_p4.Py()*met_p4.Py())/(tau_p4.Pt()*met_p4.Et()) )*57.3 <= 160)"
    selection = "&&".join([metCut, bTaggingCut, deltaPhi160Cut])
    prefix = "mcembsig_"+datasetName+postfix

    drawPlot(createPlot(treeDraw.clone(varexp="tau_p4.Pt() >>tmp(20,0,200)", selection=selection)), prefix+"_selectedTauPt_4AfterDeltaPhi160", "#tau-jet p_{T} (GeV/c)", opts2={"ymin": 0, "ymax": 3})
    drawPlot(createPlot(treeDraw.clone(varexp="met_p4.Pt() >>tmp(16,0,400)", selection=selection)), prefix+"_MET_4AfterDeltaPhi160", "E_{T}^{miss} (GeV)", ylabel="Events / %.0f GeV", opts2={"ymin": 0, "ymax": 3})
    drawPlot(createPlot(tdMt.clone(selection=selection)), prefix+"_transverseMass_4AfterDeltaPhi160", "m_{T}(#tau jet, E_{T}^{miss}) (GeV/c^{2})", opts2={"ymin": 0, "ymax": 3}, ylabel="Events / %.0f GeV/c^{2}", log=False)


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
        p.setLuminosity(datasetsEmb.getLumi())

        p.histoMgr.forEachHisto(styles.Generator([styles.dataStyle] + styles.styles))
        #p.histoMgr.setHistoDrawStyleAll("P")
        #p.histoMgr.setHistoLegendStyleAll("P")
        p.histoMgr.setHistoDrawStyle("Average", "PE")
        p.histoMgr.setHistoLegendStyle("Average", "P")

        return p

    treeDraw = dataset.TreeDraw("dummy", weight="weightPileup*weightTrigger*weightBTagging")
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

    

class DatasetsMany:
    def __init__(self, dirs, counters):
        self.datasetManagers = []
        for d in dirs:
            datasets = dataset.getDatasetsFromMulticrabCfg(cfgfile=d+"/multicrab.cfg", counters=counters)
            datasets.loadLuminosities()
            self.datasetManagers.append(datasets)

    def forEach(self, function):
        for dm in self.datasetManagers:
            function(dm)

    def setLumiFromData(self):
        self.lumi = self.datasetManagers[0].getDataset("Data").getLuminosity()

    def getLumi(self):
        return self.lumi

    def getHistogram(self, datasetName, name):
        histos = self.getHistograms(datasetName, name)

        histo = histos[0]
        histo_low = histo.Clone(histo.GetName()+"_low")
        histo_high = histo.Clone(histo.GetName()+"_high")
        for h in histos[1:]:
            for bin in xrange(0, histo.GetNbinsX()+2):
                histo.SetBinContent(bin, histo.GetBinContent(bin)+h.GetBinContent(bin))
                histo.SetBinError(bin, histo.GetBinError(bin)+h.GetBinError(bin))

                histo_low.SetBinContent(bin, min(histo_low.GetBinContent(bin), h.GetBinContent(bin)))
                histo_high.SetBinContent(bin, max(histo_high.GetBinContent(bin), h.GetBinContent(bin)))

        for bin in xrange(0, histo.GetNbinsX()+2):
            histo.SetBinContent(bin, histo.GetBinContent(bin)/len(histos))
            histo.SetBinError(bin, histo.GetBinError(bin)/len(histos))

        binCenters = []
        values = []
        errLow = []
        errHigh = []
        for bin in xrange(1, histo.GetNbinsX()+1):
            binCenters.append(histo.GetXaxis().GetBinCenter(bin))
            values.append(histo.GetBinContent(bin))
            errLow.append(histo.GetBinContent(bin) - histo_low.GetBinContent(bin))
            errHigh.append(histo_high.GetBinContent(bin) - histo.GetBinContent(bin))

        gr = ROOT.TGraphAsymmErrors(len(binCenters),
                                    array.array("d", binCenters), array.array("d", values),
                                    array.array("d", [0]*len(binCenters)), array.array("d", [0]*len(binCenters)),
                                    array.array("d", errLow), array.array("d", errHigh))

        histo.SetName("Average")

        return (histo, gr)

    def getHistograms(self, datasetName, name):
        histos = []
        for i, dm in enumerate(self.datasetManagers):
            ds = dm.getDataset(datasetName)
            h = ds.getDatasetRootHisto(name)
            if h.isMC():
                h.normalizeToLuminosity(self.lumi)
            h = histograms.HistoWithDataset(ds, h.getHistogram(), "dummy") # only needed for scaleNormalization()
            tauEmbedding.scaleNormalization(h)
            h = h.getRootHisto()
            h.SetName("Trial %d"%(i+1))
            histos.append(h)

        return histos


def drawPlot(h, name, xlabel, ylabel="Events / %.0f GeV/c", rebin=1, log=True, ratio=True, opts={}, opts2={}, moveLegend={}, cutLine=None, cutBox=None, function=None):
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
    dh = 0
    if hasattr(h, "embeddingVariation"):
        dh += 0.02
    if hasattr(h, "embeddingDataVariation"):
        dh += 0.02
    h.setLegend(histograms.moveLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend),
                                      dh=dh
                                      ))
    tmp = sigErr.Clone("tmp")
    tmp.SetFillColor(ROOT.kBlack)
    tmp.SetFillStyle(3013)
    tmp.SetLineColor(ROOT.kWhite)
    h.legend.AddEntry(tmp, "Stat. unc.", "F")

    if hasattr(h, "embeddingDataVariation"):
        h.legend.AddEntry(h.embeddingDataVariation, "Embedded data min/max", "p")
    if hasattr(h, "embeddingVariation"):
        h.legend.AddEntry(h.embeddingVariation, "Embedded MC min/max", "p")

    common(h, xlabel, ylab, cutLine, cutBox, function)


def drawPlotData(h, name, xlabel, ylabel="Events / %.0f GeV/c", rebin=1, log=True, ratio=True, opts={}, opts2={}, moveLegend={}, cutLine=None, cutBox=None, function=None):
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

    common(h, xlabel, ylab, cutLine, cutBox, function)

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
