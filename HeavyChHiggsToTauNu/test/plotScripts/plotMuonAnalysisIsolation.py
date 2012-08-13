#!/usr/bin/env python

######################################################################
#
# This plot script is for analysing the isolation in the muon
# selection part of the EWK background measurement. The corresponding
# python job configuration is tauEmbedding/muonAnalysis_cfg.py.
#
# Author: Matti Kortelainen
#
######################################################################

import sys
import array
import re

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import plotMuonAnalysis as muonAnalysis

plotStyles = [
    styles.Style(26, ROOT.kBlue),
    styles.Style(27, ROOT.kRed),

    styles.Style(ROOT.kFullSquare, ROOT.kGreen+2),
    styles.Style(ROOT.kOpenSquare, ROOT.kMagenta+3),

    styles.Style(ROOT.kFullCircle, ROOT.kYellow+2),
    styles.Style(ROOT.kOpenCircle, ROOT.kOrange+9),

    styles.Style(34, ROOT.kMagenta),
    styles.Style(ROOT.kFullTriangleUp, ROOT.kCyan-5),
    styles.Style(ROOT.kFullTriangleDown, ROOT.kOrange+3),
    ]

def main():
#    weight = ""
    weight = "VertexWeight"
#    weight = "PileupWeight"

#    mainAnalysis = "muonSelectionPFPt40Met20NJets3"
    mainAnalysis = "muonSelectionPFPt40Met20NJets3%s" % weight
    tauIsoAnalyses = [
#        "muonSelectionPFPt40Met20NJets3%sIsoTauVLoose" % weight,
#        "muonSelectionPFPt40Met20NJets3%sIsoTauLoose" % weight,
#        "muonSelectionPFPt40Met20NJets3%sIsoTauMedium" % weight,
#        "muonSelectionPFPt40Met20NJets3%sIsoTauTight" % weight,
#        "muonSelectionPFPt40Met20NJets3%sIsoTauLikeTight" % weight,
#        "muonSelectionPFPt40Met20NJets3%sIsoTauLikeTightSc015" % weight,
#        "muonSelectionPFPt40Met20NJets3%sIsoTauLikeTightSc02" % weight,
        "muonSelectionPFPt40Met20NJets3%sIsoTauLikeTightIc04" % weight,
#        "muonSelectionPFPt40Met20NJets3%sIsoTauLikeTightSc015Ic04" % weight,
#        "muonSelectionPFPt40Met20NJets3%sIsoTauLikeTightSc02Ic04" % weight,
#        "muonSelectionPFPt40Met20NJets3%sIsoTauLikeMedium" % weight,
#        "muonSelectionPFPt40Met20NJets3%sIsoTauLikeLoose" % weight,
#        "muonSelectionPFPt40Met20NJets3%sIsoTauLikeVLoose" % weight,
        ]

    signals = ["TTJets",
               "WJets",
#               "SingleTop",
#               "DYJetsToLL", "Diboson"
               ]
    backgrounds = ["QCD_Pt20_MuEnriched",
#                   "DYJetsToLL", "Diboson"
                   ]

    sel = muonAnalysis.Selections(mainAnalysis)
    selection = sel.selectionJet

    datasets = dataset.getDatasetsFromMulticrabCfg(counters=mainAnalysis+"countAnalyzer")
    datasets.updateNAllEventsToPUWeighted()
    datasets.loadLuminosities()
#    datasets.remove(["SingleMu_163270-163869_Prompt", "SingleMu_162803-163261_Prompt", "SingleMu_160431-161016_Prompt"])

    datasets41x = dataset.getDatasetsFromMulticrabCfg(cfgfile="/home/mkortela/hplus/CMSSW_4_1_5/src/HiggsAnalysis/HeavyChHiggsToTauNu/test/tauEmbedding/multicrab_muonAnalysis_chargedGamma_110617_002143/multicrab.cfg", counters=mainAnalysis+"countAnalyzer")
    datasets41x.updateNAllEventsToPUWeighted()
    datasets41x.selectAndReorder(["TToBLNu_s-channel_TuneZ2_Spring11", "TToBLNu_t-channel_TuneZ2_Spring11", "TToBLNu_tW-channel_TuneZ2_Spring11",
                                  "WW_TuneZ2_Spring11", "WZ_TuneZ2_Spring11", "ZZ_TuneZ2_Spring11"])
    datasets.extend(datasets41x)

    plots.mergeRenameReorderForDataMC(datasets)

    style = tdrstyle.TDRStyle()

    histograms.createLegend.moveDefaults(dx=-0.15, dy=0.1, dh=-0.1)

    # QCD fraction for the continuous isolation variables
    prefix = selection+"_"
    isoPassed = []
    isoNames = ["sumIsoRel", "pfSumIsoRel"]
    #isoNames = ["sumIsoRelFull", "pfSumIsoRelFull"]
    additionalIsoNames = ["tauTightIso", "tauMediumIso", "tauLooseIso", "tauVLooseIso",
                          "tauTightSc015Iso",# "tauTightSc02Iso",
                          "tauTightIc04Iso", "tauTightSc015Ic04Iso",# "tauTightSc02Ic04Iso",
                          "tauTightIc04SumPtIso", "tauTightIc04MaxPtIso",
                          "tauTightIc04ChargedIso", "tauTightIc04GammaIso",
                          ]
    for iso in isoNames+additionalIsoNames:
        isoPassed.append(muonAnalysis.muonIso(plots.DataMCPlot(datasets, selection+"/muon_"+iso), prefix, iso, rebin=5, opts={"ymin": 1e-1}))

        for tauIso in tauIsoAnalyses:
            tmp = muonAnalysis.Selections(tauIso).selectionJet
            muonAnalysis.muonIso(plots.DataMCPlot(datasets, tmp+"/muon_"+iso), tmp+"_", iso)

    for iso in additionalIsoNames:
        opts = {"ymin": 1e-1}
        rebin = 1
        ratio = False
        if iso in ["tauTightIc04Iso", "tauTightIso"]:
            opts["xmax"] = 50
            opts["ymax"] = 5e4
            ratio = True
        elif iso in ["tauTightIc04ChargedIso", "tauTightIc04GammaIso"]:
            opts["xmax"] = 30
            opts["ymax"] = 5e4
            ratio = True
        elif "Pt" in iso:
            rebin = 5
        muonAnalysis.muonIso(plots.DataMCPlot(datasets, selection+"/muon_"+iso), prefix, iso, rebin=rebin, opts=opts, ratio=ratio)

    isoPlot = muonAnalysis.PlotIso(isoPassed, isoNames)
    muonAnalysis.muonIsoQcd(isoPlot, prefix)

    # Get the tau isolation values
    s_count = {}
    b_count = {}
    sum_count = {}
    for isoAnalysis in [mainAnalysis]+tauIsoAnalyses:
        dsets = dataset.getDatasetsFromMulticrabCfg(counters=isoAnalysis+"countAnalyzer")
        dsets.updateNAllEventsToPUWeighted()
        dsets.loadLuminosities()
        plots.mergeRenameReorderForDataMC(dsets)
        dsets.merge("Signal2", signals)
        dsets.merge("Background2", backgrounds)
        stmp = dsets.getDataset("Signal2").deepCopy()
        btmp = dsets.getDataset("Background2").deepCopy()
        dsets.merge("MCSum", dsets.getMCDatasetNames())

        stmp.setName("Signal")
        btmp.setName("Background")
        dsets.append(stmp)
        dsets.append(btmp)

        ec = counter.EventCounter(dsets)
        ec.normalizeMCByCrossSection()
        tbl = ec.getMainCounterTable()
        idx = tbl.getColumn(name="Signal").getRowNames().index(isoAnalysis+"countJetMultiplicityCut")
        sc = tbl.getColumn(name="Signal").getCount(idx).value()
        bc = tbl.getColumn(name="Background").getCount(idx).value()
        sumc = tbl.getColumn(name="MCSum").getCount(idx).value()

        s_count[isoAnalysis] = sc
        b_count[isoAnalysis] = bc
        sum_count[isoAnalysis] = sumc


    s_eff = {}
    b_rej = {}
    b_frac = {}
    for isoAnalysis in tauIsoAnalyses:
        s_eff[isoAnalysis] = s_count[isoAnalysis]/s_count[mainAnalysis]
        b_rej[isoAnalysis] = 1 - b_count[isoAnalysis]/b_count[mainAnalysis]
        b_frac[isoAnalysis] = b_count[isoAnalysis]/sum_count[isoAnalysis]

        print s_eff[isoAnalysis], b_rej[isoAnalysis], b_frac[isoAnalysis]

    # Plot the ROC
    datasets.merge("Signal", signals)
    datasets.merge("Background", backgrounds)
#    datasets.selectAndReorder(["Signal", "Background"])
    print ", ".join([d.getName() for d in datasets.getAllDatasets()])

    histograms.createLegend.setDefaults(x1=0.2, y1=0.5, x2=0.4, y2=0.8)

    seff = PlotEff(datasets, "Signal", [selection+"/muon_"+iso for iso in isoNames], isoNames)
    beff = PlotEff(datasets, "Background", [selection+"/muon_"+iso for iso in isoNames], isoNames)
    plotEff(seff, prefix)
    plotEff(beff, prefix)

    plot = PlotRoc(datasets)
    plotf = PlotRocFraction(datasets)
    for p in [plot, plotf]:
        for iso in isoNames:
            p.addCurve(selection+"/muon_"+iso, iso)

    for iso in tauIsoAnalyses:
        plot.addPoint(s_eff[iso], b_rej[iso], iso)
        plotf.addPoint(s_eff[iso], b_frac[iso], iso)

    plot.finalize()
    plotf.finalize()

    plotRoc(plot, prefix)

    #plot.pointStyle()
    plotRoc(plot, prefix, postfix="_zoom", #opts={"ymin": 0.97, "ymax": 1.005, "xmin": 0.2, "xmax": 1},
            opts={"ymin": 0.8, "ymax": 1.005, "xmin": 0.2, "xmax": 1},
            moveLegend={"dy":-0.1})
    #plotRoc(plot, prefix, postfix="_zoom2", opts={"xmin": 0.8, "xmax": 1})

    plotRoc(plotf, prefix, opts={"ymax":0.4, "xmax":1.0}, moveLegend={"dy":0.1})
    #plotRoc(plotf, prefix, opts={"ymax":0.1, "xmax":1.0})
    plotRoc(plotf, prefix, log=True, moveLegend={"dy": -0.2})

def getRootHisto(datasets, dname, hname):
    tmp = self.datasets.getDataset(dname).getDatasetRootHisto(hname)
    tmp.normalizeByCrossSection()
    return tmp.getHistogram()

class PlotEff(plots.PlotBase):
    def __init__(self, datasets, dname, names, labels):
        plots.PlotBase.__init__(self, [])

        self.name = dname
        self.ylabel = "Efficiency"

        for hname, label in zip(names, labels):
            dh = datasets.getDataset(dname).getDatasetRootHisto(hname)
            dh.normalizeByCrossSection()
            dh = dataset.DatasetRootHisto(muonAnalysis.dist2eff(dh.getHistogram()), dh.getDataset())
            dh.setName(label)
            self.histoMgr.append(dh)

        self.histoMgr.forEachHisto(styles.generator2(styles.StyleMarker(markerSize=1.5), plotStyles))
        self.histoMgr.setHistoLegendStyleAll("l")


class PlotRocBase(plots.PlotBase):
    def __init__(self, datasets):
        plots.PlotBase.__init__(self, [])
        self.datasets = datasets
        self.pointLabels = []

    def finalize(self):
        def setLabel(histo):
            name = histo.getName()
            scic_re = re.compile("Sc(?P<sig>\d+)(Ic(?P<iso>\d+))?")
            ic_re = re.compile("Ic(?P<iso>\d+)")
            for tauIso in ["VLoose", "Loose", "Medium", "Tight"]:
                if "IsoTau"+tauIso in name:
                    histo.setLegendLabel('Counting iso "'+tauIso+'"')
                    break
                if "IsoTauLike"+tauIso in name:
                    m = scic_re.search(name)
                    sc = "0.1"
                    ic = "0.5"
                    if m:
                        sc = m.group("sig").replace("0", "0.")
                        if m.group("iso"):
                            ic = m.group("iso").replace("0", "0.")
                    else:
                        m = ic_re.search(name)
                        if m:
                            ic = m.group("iso").replace("0", "0.")
                    label = 'Counting iso "'+tauIso + '" %s < DR < %s' % (sc, ic)
                    print label
                    histo.setLegendLabel(label)

        self.histoMgr.setHistoLegendLabelMany({
                "sumIsoRel": "Rel iso",
                "pfSumIsoRel": "PF rel iso",
                "sumIsoRelFull": "Rel iso",
                "pfSumIsoRelFull": "PF rel iso",
                })
        self.histoMgr.forEachHisto(setLabel)

        self.histoMgr.forEachHisto(styles.generator2(styles.StyleMarker(markerSize=1.5), plotStyles))
        self.defaultStyle()

    def defaultStyle(self):
        self.histoMgr.setHistoDrawStyleAll("L")
        self.histoMgr.setHistoLegendStyleAll("l")
        for p in self.pointLabels:
            self.histoMgr.setHistoDrawStyle(p, "P")
            self.histoMgr.setHistoLegendStyle(p, "p")

    def pointStyle(self):
        self.histoMgr.setHistoDrawStyleAll("PL")
        self.histoMgr.setHistoLegendStyleAll("pl")
        for p in self.pointLabels:
            self.histoMgr.setHistoDrawStyle(p, "P")
            self.histoMgr.setHistoLegendStyle(p, "p")

class PlotRoc(PlotRocBase):
    def __init__(self, *args):
        PlotRocBase.__init__(self, *args)
        self.name = "roc"
        self.ylabel = "QCD rejection"

    def addCurve(self, name, label):
        def getHisto(dataset):
            tmp = self.datasets.getDataset(dataset).getDatasetRootHisto(name)
            tmp.normalizeByCrossSection()
            return tmp.getHistogram()
        signalRootHisto = getHisto("Signal")
        bkgRootHisto = getHisto("Background")

        signalEff = muonAnalysis.dist2eff(signalRootHisto)
        bkgRej = muonAnalysis.dist2rej(bkgRootHisto)
#        bkgRej = muonAnalysis.dist2eff(bkgRootHisto)

        signalEffValues = dataset.histoToList(signalEff)
        bkgRejValues = dataset.histoToList(bkgRej)

        roc = ROOT.TGraph(len(signalEffValues), array.array("d", signalEffValues), array.array("d", bkgRejValues))
        self.histoMgr.appendHisto(histograms.HistoGraph(roc, label))

    def addPoint(self, sigeff, bkgrej, label):
        gr = ROOT.TGraph(1, array.array("d", [sigeff]), array.array("d", [bkgrej]))
        self.histoMgr.appendHisto(histograms.HistoGraph(gr, label))
        self.pointLabels.append(label)
                                 
class PlotRocFraction(PlotRocBase):
    def __init__(self, *args):
        PlotRocBase.__init__(self, *args)
        self.name = "rocfraction"
        self.ylabel = "QCD fraction"

    def addCurve(self, name, label):
        def getHisto(dataset):
            tmp = self.datasets.getDataset(dataset).getDatasetRootHisto(name)
            #tmp.normalizeToLuminosity(46)
            tmp.normalizeByCrossSection()
            return tmp.getHistogram()
        signalRootHisto = getHisto("Signal")
        signalEff = muonAnalysis.dist2eff(signalRootHisto)
        signalEffValues = dataset.histoToList(signalEff)

        tmpHistoManager = histograms.HistoManager(self.datasets, name)
        tmpHistoManager.normalizeMCByCrossSection()
        #tmpHistoManager.normalizeMCByLuminosity()
        mcSum = histograms.sumRootHistos([muonAnalysis.getSumOrRootHisto(histo) for histo in filter(lambda h: h.isMC(), tmpHistoManager.getHistos())])
        mcSum = muonAnalysis.dist2pass(mcSum)

        bkgHisto = tmpHistoManager.getHisto("Background")
        bkg = muonAnalysis.getSumOrRootHisto(bkgHisto).Clone(name+"_bkgfraction")
        bkg = muonAnalysis.dist2pass(bkg)
        bkg.Divide(mcSum)
        bkgValues = dataset.histoToList(bkg)

        curve = ROOT.TGraph(len(signalEffValues), array.array("d", signalEffValues), array.array("d", bkgValues))
        self.histoMgr.appendHisto(histograms.HistoGraph(curve, label))

    def addPoint(self, sigeff, bkgfrac, label):
        gr = ROOT.TGraph(1, array.array("d", [sigeff]), array.array("d", [bkgfrac]))
        self.histoMgr.appendHisto(histograms.HistoGraph(gr, label))
        self.pointLabels.append(label)

def plotRoc(h, prefix, postfix="", log=False, opts={}, zoom_opts={}, moveLegend={}):
    args = {"ymin": 0, "ymax": 1.1, "xmin": 0, "xmax": 1.1}
    name = prefix+"isolation_%s"%h.name + postfix
    if log:
        name += "_log"
        args["ymin"] = 1e-3
    args.update(opts)

    h.createFrame(name, **args)
    h.frame.GetXaxis().SetTitle("Non-QCD efficiency")
    h.frame.GetYaxis().SetTitle(h.ylabel)
    if log:
        ROOT.gPad.SetLogy(True)
    h.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))
    h.draw()
    h.save()

def plotEff(h, prefix):
    h.createFrame(prefix+"eff_%s"%h.name)
    h.frame.GetXaxis().SetTitle("Cut on isolation")
    h.frame.GetYaxis().SetTitle(h.ylabel)
    h.setLegend(histograms.moveLegend(histograms.createLegend(), dx=0.55))
    h.draw()
    h.save()
    return


if __name__ == "__main__":
    main()
