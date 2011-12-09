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


import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles

analysisEmb = "signalAnalysis"
analysisSig = "signalAnalysis"

dirEmb = "."
#dirSig = "../../multicrab_compareEmbedding_Run2011A_111117_155815"
#dirSig = "../../multicrab_compareEmbedding_Run2011A_111122_130104"
#dirSig = "../../multicrab_compareEmbedding_Run2011A_111124_154038"
dirSig = "../../multicrab_compareEmbedding_Run2011A_111201_143238"


def main():
    datasetsEmb = dataset.getDatasetsFromMulticrabCfg(cfgfile=dirEmb+"/multicrab.cfg", counters=analysisEmb+"Counters")
    datasetsSig = dataset.getDatasetsFromMulticrabCfg(cfgfile=dirSig+"/multicrab.cfg", counters=analysisSig+"Counters")

    datasetsEmb.loadLuminosities()
    plots.mergeRenameReorderForDataMC(datasetsEmb)
    plots.mergeRenameReorderForDataMC(datasetsSig)

    style = tdrstyle.TDRStyle()
    histograms.createLegend.setDefaults(y1=0.93, y2=0.78, x1=0.6, x2=0.95)

    doPlots(datasetsEmb, datasetsSig, "TTJets")
    doPlots(datasetsEmb, datasetsSig, "WJets")

def doPlots(datasetsEmb, datasetsSig, datasetName):
    lumi = datasetsEmb.getDataset("Data").getLuminosity()

    plots._legendLabels[datasetName+"_Embedded"] = "Embedded "+plots._legendLabels[datasetName]
    plots._legendLabels[datasetName+"_Normal"]   = "Normal "+plots._legendLabels[datasetName]

    def createPlot(name):
        name2Emb = name
        name2Sig = name
        if isinstance(name, basestring):
            name2Emb = analysisEmb+"/"+name
            name2Sig = analysisSig+"/"+name
        else:
            name2Emb = name.clone(tree=analysisEmb+"/tree")
            name2Sig = name.clone(tree=analysisSig+"/tree")
        emb = datasetsEmb.getDataset(datasetName).getDatasetRootHisto(name2Emb)
        emb.setName("Embedded")
        sig = datasetsSig.getDataset(datasetName).getDatasetRootHisto(name2Sig)
        sig.setName("Normal")
        p = plots.ComparisonPlot(emb, sig)
        p.histoMgr.normalizeMCToLuminosity(lumi)
        p.histoMgr.setHistoLegendLabelMany({
                "Embedded": "Embedded "+plots._legendLabels[datasetName],
                "Normal":   "Normal "+plots._legendLabels[datasetName],
                })
        p.histoMgr.forEachHisto(styles.generator())

        return p

    opts2 = {"ymin": 0, "ymax": 2}
    def drawControlPlot(path, xlabel, **kwargs):
        drawPlot(createPlot("ControlPlots/"+path), "mcembsig_"+datasetName+"_"+path, xlabel, opts2=opts2, **kwargs)

    drawControlPlot("SelectedTau_pT_AfterStandardSelections", "#tau-jet p_{T} (GeV/c)", opts={"xmax": 250}, rebin=2, cutBox={"cutValue": 40, "greaterThan": 40})
    drawControlPlot("SelectedTau_eta_AfterStandardSelections", "#tau-jet #eta", opts={"xmin": -2.2, "xmax": 2.2}, ylabel="Events / %.1f", rebin=4, log=False, moveLegend={"dy":-0.6, "dx":-0.2})
    drawControlPlot("SelectedTau_phi_AfterStandardSelections", "#tau-jet #phi", rebin=10, ylabel="Events / %.2f", log=False)
    drawControlPlot("SelectedTau_LeadingTrackPt_AfterStandardSelections", "#tau-jet ldg. charged particle p_{T} (GeV/c)", opts={"xmax": 300}, rebin=2, cutBox={"cutValue": 20, "greaterThan": True})
    drawControlPlot("SelectedTau_Rtau_AfterStandardSelections", "R_{#tau} = p^{ldg. charged particle}/p^{#tau jet}", opts={"xmin": 0.65, "xmax": 1.05, "ymin": 1e-1, "ymaxfactor": 5}, rebin=5, ylabel="Events / %.2f", moveLegend={"dx":-0.3}, cutBox={"cutValue":0.7, "greaterThan":True})
    drawControlPlot("SelectedTau_p_AfterStandardSelections", "#tau-jet p (GeV/c)", rebin=2)
    drawControlPlot("SelectedTau_LeadingTrackP_AfterStandardSelections", "#tau-jet ldg. charged particle p (GeV/c)", rebin=2)
    #drawControlPlot("IdentifiedElectronPt_AfterStandardSelections", "Electron p_{T} (GeV/c)")
    #drawControlPlot("IdentifiedMuonPt_AfterStandardSelections", "Muon p_{T} (GeV/c)")
    drawControlPlot("Njets_AfterStandardSelections", "Number of jets", ylabel="Events")
    drawControlPlot("MET", "Raw PF E_{T}^{miss} (GeV)", rebin=5, opts={"xmax": 400}, cutLine=50)
    drawControlPlot("NBjets", "Number of selected b jets", opts={"xmax": 6}, ylabel="Events", moveLegend={"dx":-0.3, "dy":-0.5}, cutLine=1)

    treeDraw = dataset.TreeDraw("dummy", weight="weightPileup")


    tdDeltaPhi = treeDraw.clone(varexp="acos( (tau_p4.Px()*met_p4.Px()+tau_p4.Py()*met_p4.Py())/(tau_p4.Pt()*met_p4.Et()) )*57.3 >>tmp(18, 0, 180)")
    tdMt = treeDraw.clone(varexp="sqrt(2 * tau_p4.Pt() * met_p4.Et() * (1-cos(tau_p4.Phi()-met_p4.Phi()))) >>tmp(20,0,200)")

    xlabel = "#Delta#phi(#tau, MET) (^{#circ})"
    def customDeltaPhi(h):
        yaxis = h.getFrame().GetYaxis()
        yaxis.SetTitleOffset(0.8*yaxis.GetTitleOffset())
    drawPlot(createPlot(tdDeltaPhi.clone()), "mcembsig_"+datasetName+"_deltaPhi_1AfterTauID", xlabel, log=False, opts2=opts2, ylabel="Events / %.0f^{#circ}", function=customDeltaPhi, moveLegend={"dx":-0.22}, cutLine=[130, 160])

    xlabel = "m_{T} (#tau jet, E_{T}^{miss}) (GeV/c^{2})"
    drawPlot(createPlot(tdMt.clone()), "mcembsig_"+datasetName+"_transverseMass_1AfterTauID", xlabel, opts2=opts2, ylabel="Events / %.0f GeV/c^{2}")


    eventCounterEmb = counter.EventCounter(datasetsEmb, counters=analysisEmb+"Counters")
    eventCounterSig = counter.EventCounter(datasetsSig, counters=analysisSig+"Counters")
    eventCounterEmb.normalizeMCToLuminosity(lumi)
    eventCounterSig.normalizeMCToLuminosity(lumi)

    #effFormat = counter.TableFormatText(counter.CellFormatText(valueFormat='%.4f'))
    #effFormat = counter.TableFormatConTeXtTABLE(counter.CellFormatTeX(valueFormat='%.4f'))
    effFormat = counter.TableFormatText(counter.CellFormatTeX(valueFormat='%.4f'))

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

        print "%s counters" % cname
        print table.format()

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
                        "BTagging",
                        "DeltaPhi < 160",
                        "DeltaPhi < 130"
                        ])#, [tableEmb, tableSig])
        else:
            #map(lambda t: t.keepOnlyRows([
            table.keepOnlyRows([
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
                        ])#, [tableEmb, tableSig])

        col = table.getColumn(name="Embedded")
        table.insertColumn(1, counter.efficiencyColumn(col.getName()+" eff", col))
        col = table.getColumn(name="Normal")
        table.appendColumn(counter.efficiencyColumn(col.getName()+" eff", col))

        print "%s counters" % cname
        print table.format(effFormat)



def drawPlot(h, name, xlabel, ylabel="Events / %.0f GeV/c", rebin=1, log=True, ratio=True, opts={}, opts2={}, moveLegend={}, cutLine=None, cutBox=None, function=None):
    if rebin > 1:
        h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    ylab = ylabel
    if "%" in ylabel:
        ylab = ylabel % h.binWidth()

    #scaleNormalization(h)
    #h.stackMCHistograms()

    embErr = h.histoMgr.getHisto("Embedded").getRootHisto().Clone("Embedded_err")
    sigErr = h.histoMgr.getHisto("Normal").getRootHisto().Clone("Normal_err")

    embErr.SetFillColor(ROOT.kBlue-7)
    embErr.SetFillStyle(3004)
    embErr.SetMarkerSize(0)
    sigErr.SetFillColor(ROOT.kRed-7)
    sigErr.SetMarkerSize(0)
    sigErr.SetFillStyle(3005)

    h.prependPlotObject(sigErr, "E2")
    h.prependPlotObject(embErr, "E2")

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
    tmp = embErr.Clone("tmp")
    tmp.SetFillColor(ROOT.kBlack)
    tmp.SetFillStyle(3013)
    tmp.SetLineColor(ROOT.kWhite)
    h.legend.AddEntry(tmp, "Stat. unc.", "F")

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

    common(h, xlabel, ylab)

def common(h, xlabel, ylabel):
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    h.addLuminosityText()
    h.save()

if __name__ == "__main__":
    main()
