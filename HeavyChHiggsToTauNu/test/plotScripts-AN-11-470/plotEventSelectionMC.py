#!/usr/bin/env python

######################################################################
#
# This plot script is for event selection plots with MC backgrounds
#
# Developpment scripts: plotSignalAnalysis.py, plotSignalEfficienciesConseq.py
#
# Authors: Ritva Kinnunen, Matti Kortelainen
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
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect

analysis = "signalAnalysis"
counters = analysis+"Counters/weighted"


def main():
    # Read the datasets
    datasets = dataset.getDatasetsFromMulticrabCfg(counters=counters)
    datasets.loadLuminosities()

    plots.mergeRenameReorderForDataMC(datasets)
    print "Int.Lumi",datasets.getDataset("Data").getLuminosity()

    # Take a deep copy of DatasetManager for all signals
    datasetsAllSignals = datasets.deepCopy()

    # Remove signals other than M120
    datasets.remove(filter(lambda name: "TTToHplus" in name and not "M120" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "HplusTB" in name, datasets.getAllDatasetNames()))

    # Remove QCD
    datasets.remove(filter(lambda name: "QCD" in name, datasets.getAllDatasetNames()))
    histograms.createLegend.moveDefaults(dx=-0.02)
    histograms.createLegend.moveDefaults(dh=-0.03)

    # Set the signal cross sections to a given BR(t->H), BR(h->taunu)
    xsect.setHplusCrossSectionsToBR(datasets, br_tH=0.05, br_Htaunu=1)
    xsect.setHplusCrossSectionsToBR(datasetsAllSignals, br_tH=0.05, br_Htaunu=1)

    plots.mergeWHandHH(datasets) # merging of WH and HH signals must be done after setting the cross section

    # Replace signal dataset with EWK+signal
    # This produces the "bkg+signal" histogram
    # The ttbar cross section is adjusted for the BR(t->H+)
    ttjets2 = datasets.getDataset("TTJets").deepCopy()
    ttjets2.setName("TTJets2")
    ttjets2.setCrossSection(ttjets2.getCrossSection() - datasets.getDataset("TTToHplus_M120").getCrossSection())
    datasets.append(ttjets2)
    datasets.merge("EWKnoTT", ["WJets", "DYJetsToLL", "SingleTop", "Diboson"], keepSources=True)
    datasets.merge("TTToHplus_M120", ["TTToHplus_M120", "EWKnoTT", "TTJets2"])
    plots._legendLabels["TTToHplus_M120"] = "with H^{#pm}#rightarrow#tau^{#pm}#nu"

    # Apply TDR style
    style = tdrstyle.TDRStyle()

    # Create plots
    doPlots(datasets)

    # Print counters
    massPoints = [80, 90, 100, 120, 140, 150, 155, 160]
    doCounters(datasetsAllSignals, massPoints)

    # Signal efficiency plots for WH
#    doEfficiencyPlots(datasetsAllSignals, massPoints)

drawPlot = plots.PlotDrawer(ylabel="Events / %.0f (GeV/c^{2})", log=True, addLuminosityText=True, stackMCHistograms=True, addMCUncertainty=True)

def doPlots(datasets):
    def createPlot(name, **kwargs):
        return plots.DataMCPlot(datasets, analysis+"/"+name, **kwargs)

    def addMassBRText(plot, x, y):
        mass = "m_{H^{#pm}} = 120 GeV/c^{2}"
        br = "BR(t #rightarrow bH^{#pm})=0.05"
        size = 20
        separation= 0.04
        plot.appendPlotObject(histograms.PlotText(x, y, mass, size=size))
        plot.appendPlotObject(histograms.PlotText(x, y-separation, br, size=size))

    # Number of vertices (unit area)
    p = createPlot("Vertices/verticesTriggeredAfterWeight", normalizeToOne=True)
    p.appendPlotObject(histograms.PlotText(0.35, 0.9, "Normalized to unit area", size=17))
    drawPlot(p, "verticesAfterWeightTriggered_log", "Number of good vertices", ylabel="Arbitrary units", opts={"ymin": 1e-10, "ymaxfactor": 10, "xmax": 30}, opts2 = {"ymin": 0.5, "ymax": 3})

    # Selected tau jet pt
    p = createPlot("SelectedTau/SelectedTau_pT_AfterTauID")
    addMassBRText(p, x=0.31, y=0.22)
    drawPlot(p, "SelectedTau_pT_AfterTauID", "p_{T}^{#tau jet} (GeV/c)", rebin=10, opts={"xmax": 250})

    # Selected tau jet eta
    p = createPlot("SelectedTau/SelectedTau_eta_AfterTauID")
    addMassBRText(p, x=0.3, y=0.85)
    drawPlot(p, "SelectedTau_eta_AfterTauID", "#eta^{#tau jet}", ylabel="Events / %.1f", rebin=10, opts={"ymin": 1e-1, "ymaxfactor": 40, "xmin": -2.5, "xmax": 2.5}, moveLegend={"dy":0.01, "dh":-0.06})

    # Selected tau jet Rtau (without rtau cut)
    p = createPlot("tauID/TauID_RtauCut")
    addMassBRText(p, x=0.31, y=0.22)
    drawPlot(p, "TauID_Rtau", "R_{#tau} = p^{ldg. charged particle}/p^{#tau jet}", ylabel="Events / %.2f", rebin=2, opts={"ymin": 1e-2, "ymaxfactor": 20, "xmax": 1.1}, moveLegend={"dx": -0.5, "dy": 0.01, "dh": -0.04}, cutLine=0.7)


    # Identified electron pt
    p = createPlot("GlobalElectronVeto/GlobalElectronPt_identified_eta")
    addMassBRText(p, x=0.4, y=0.87)
    drawPlot(p, "electronPt", "p_{T}^{electron} (GeV/c)", rebin=15, ylabel="Identified electrons / %.0f GeV/c", opts={"xmax": 250}, cutLine=15)

    # Identified electron eta
    p = createPlot("GlobalElectronVeto/GlobalElectronEta_identified")
    addMassBRText(p, x=0.3, y=0.87)
    drawPlot(p, "electronEta", "#eta^{electron}", rebin=15, ylabel="Identified electrons / %.1f", opts={"xmin": -3, "xmax": 3, "ymaxfactor": 50}, moveLegend={"dy":0.01, "dx":-0.07, "dh":-0.06}, cutLine=[-2.5, 2.5])


    # Identified muon pt
    p = createPlot("GlobalMuonVeto/GlobalMuonPt_identified_eta")
    addMassBRText(p, x=0.4, y=0.87)
    drawPlot(p, "muonPt", "p_{T}^{muon} (GeV/c)", ylabel="Identified muons / %.0f GeV/c", rebin=3, opts={"xmax": 250}, cutLine=15)

    # Identified muon eta
    p = createPlot("GlobalMuonVeto/GlobalMuonEta_identified")
    addMassBRText(p, x=0.3, y=0.87)
    drawPlot(p, "muonEta", "#eta^{muon}", ylabel="Identified muons / %.1f", rebin=3, opts={"xmin": -3, "xmax": 3, "ymaxfactor": 40}, moveLegend={"dy":0.01, "dx":-0.07, "dh":-0.06}, cutLine=[-2.5, 2.5])


    # Jet pt
    p = createPlot("JetSelection/jet_pt_central")
    addMassBRText(p, x=0.3, y=0.87)
    drawPlot(p, "centralJetPt", "p_{T}^{jet} (GeV/c)", ylabel="Jets / %.0f GeV/c", rebin=5, opts={"xmax": 400}, cutLine=30)

    # Jet eta
    p = createPlot("JetSelection/jet_eta")
    addMassBRText(p, x=0.4, y=0.22)
    drawPlot(p, "jetEta", "#eta^{jet}", ylabel="Jets / %.1f", rebin=4, opts={"ymaxfactor": 110}, moveLegend={"dy":0.01, "dx":-0.2, "dh":-0.06}, cutLine=[-2.4, 2.4])

    # Jet multiplicity
    p = createPlot("JetSelection/NumberOfSelectedJets")
    addMassBRText(p, x=0.67, y=0.6)
    drawPlot(p, "NumberOfJets", "Number of selected jets", ylabel="Events / %.0f", opts={"xmax": 10}, cutLine=3)


    # MET
    p = createPlot("Met")
    addMassBRText(p, x=0.4, y=0.87)
    drawPlot(p, "Met", "Uncorrected PF E_{T}^{miss} (GeV)", rebin=25, ylabel="Events / %.0f GeV", opts={"xmax": 400}, cutLine=50)


    # B jet pt
    p = createPlot("Btagging/bjet_pt")
    addMassBRText(p, x=0.4, y=0.87)
    drawPlot(p, "bjetPt", "p_{T}^{b-tagged jet} (GeV/c)", rebin=15, ylabel="b-tagged jets / %.0f GeV/c", opts={"xmax": 400})

    # B jet eta
    p = createPlot("Btagging/bjet_eta")
    addMassBRText(p, x=0.4, y=0.87)
    drawPlot(p, "bjetEta", "#eta^{b-tagged jet}", ylabel="b-tagged jets / %.1f", rebin=8, opts={"ymaxfactor": 30, "xmin": -2.4, "xmax": 2.4}, moveLegend={"dy":0.01, "dh":-0.06})

    # B jet multiplicity
    p = createPlot("Btagging/NumberOfBtaggedJets")
    addMassBRText(p, x=0.45, y=0.87)
    drawPlot(p, "NumberOfBJets", "Number of selected b jets", ylabel="Events / %.0f", opts={"xmax": 6}, cutLine=1)


    # DeltaPhi
    p = createPlot("deltaPhi")
    addMassBRText(p, x=0.2, y=0.87)
    drawPlot(p, "DeltaPhiTauMet", "#Delta#phi(#tau jet, E_{T}^{miss}) (^{o})", ylabel="Events / %.0f^{o}", rebin=20, opts={"ymaxfactor": 20}, moveLegend={"dx":-0.21}, cutLine=[160, 130])

    # Transverse mass
    p = createPlot("transverseMass")
    addMassBRText(p, x=0.4, y=0.87)
    drawPlot(p, "transverseMass", "m_{T}(#tau jet, E_{T}^{miss}) (GeV/c^{2})", ylabel="Events / %.0f GeV/c^{2}", rebin=20, log=False)

    # Selection flow
    p = createPlot("SignalSelectionFlow")
    addMassBRText(p, 0.4, 0.87)
    def customiseFlow(plot):
        xaxis = plot.getFrame().GetXaxis()
        xaxis.SetBinLabel(1, "Trigger")
        xaxis.SetBinLabel(2, "#tau ID+R_{#tau}")
        xaxis.SetBinLabel(3, "e veto")
        xaxis.SetBinLabel(4, "#mu veto")
        xaxis.SetBinLabel(5, "N_{jets}")
    lastSelection = 4 # mu veto
    drawPlot(p, "SignalSelectionFlow", "", ylabel="Events", opts={"xmax": lastSelection, "ymin": 0.1, "ymaxfactor": 2, "nbins": lastSelection}, customise=customiseFlow)


def doCounters(datasets, massPoints):
    eventCounter = counter.EventCounter(datasets, counters=counters)
    eventCounter.normalizeMCByLuminosity()

    rows1 = [
        "Trigger and HLT_MET cut",
        "taus == 1",
        "trigger scale factor",
        "electron veto",
        "muon veto",
        "njets",
        "MET"
        ]
    rows2 = [
        "btagging scale factor",
        "deltaPhiTauMET<160",
        "deltaPhiTauMET<130",
        ]

    tableAll = eventCounter.getMainCounterTable()
    tableAll.keepOnlyRows(rows1+rows2)

    tableWH = counter.CounterTable()
    tableHH = counter.CounterTable()
    for mass in massPoints:
        tableWH.appendColumn(tableAll.getColumn(name="TTToHplusBWB_M%d"%mass))
        tableHH.appendColumn(tableAll.getColumn(name="TTToHplusBHminusB_M%d"%mass))

    tableWH2 = tableWH.clone()
    tableWH.keepOnlyRows(rows1)
    tableWH2.keepOnlyRows(rows2)
    tableHH2 = tableHH.clone()
    tableHH.keepOnlyRows(rows1)
    tableHH2.keepOnlyRows(rows2)

    format1 = counter.TableFormatText(counter.CellFormatTeX(valueFormat="%.0f", valueOnly=True))
    format12 = counter.TableFormatText(counter.CellFormatTeX(valueFormat="%.1f", valueOnly=True))
    format2 = counter.TableFormatText(counter.CellFormatTeX(valueFormat="%.2f", withPrecision=1))

    print "tt -> bW bH+"
    print tableWH.format(format1)
    print tableWH2.format(format2)
    
    print
    print
    print "tt -> bH+ bH-"
    print tableHH.format(format12)
    print tableHH2.format(format2)

# def doEfficiencyPlots(datasets, massPoints):
#     eventCounter = counter.EventCounter(datasets, counters=counters)
#     eventCounter.normalizeMCByCrossSection()
#     mainTable = eventCounter.getMainCounterTable()

#     allName = "All events"
#     cuts = [
#         "Trigger and HLT_MET cut",
#         "primary vertex",
#         "taus == 1",
#         "trigger scale factor",
#         "electron veto",
#         "muon veto",
#         "njets",
#         "MET",
#         "btagging",
#         "btagging scale factor"
#         ]

#     xvalues = massPoints
#     xerrs = [0]*len(xvalues)
#     yvalues = {}
#     yerrs = {}
#     for cut in cuts:
#         yvalues[cut] = []
#         yerrs[cut] = []

#     for mass in massPoints:
#         column = mainTable.getColumn(name="TTToHplusBWB_M%d"%mass)

#         prevCount = column.getCount(name=allName)
#         for cut in cuts:
#             count = column.getCount(name=cut)

#             eff = count.clone()
#             eff.divide(prevCount) # count/prevCount
#             prevCount = count

#             yvalues[cut].append(eff.value())
#             yerrs[cut].append(eff.uncertainty())

#     def createGraph(cutname, color, markerStyle):
#         gr = ROOT.TGraphErrors(len(xvalues), array.array("d", xvalues), array.array("d", yvalues[cutname]),
#                                array.array("d", xerrs), array.array("d", yerrs[cutname]))
#         gr.SetMarkerStyle(markerStyle)
#         gr.SetMarkerColor(color)
#         gr.SetMarkerSize(2)
#         gr.SetLineColor(color)
#         gr.SetLineStyle(1)
#         gr.SetLineWidth(4)
#         gr.SetName(cutname)
#         return gr

#     gtrig = createGraph("Trigger and HLT_MET cut", color=38, markerStyle=20)
#     gtau = createGraph("taus == 1", color=2, markerStyle=21)
#     gveto = createGraph("muon veto", color=1, markerStyle=22)
#     gjets = createGraph("njets", color=4, markerStyle=23)
#     gmet = createGraph("MET", color=2, markerStyle=24)
#     gbtag = createGraph("btagging", color=1, markerStyle=25)

#     p = plots.PlotBase([gtrig, gtau, gveto, gjets, gmet, gbtag])
#     p.histoMgr.setHistoLegendLabelMany({
#             "Trigger and HLT_MET cut": "Trigger",
#             "taus == 1":               "#tau identification",
#             "muon veto":               "lepton vetoes",
#             "njets":                   "3 jets",
#             "btagging":                "b tagging"
#             })
#     p.histoMgr.setHistoLegendStyleAll("lp")
#     p.histoMgr.setHistoDrawStyleAll("PC")
#     drawPlot(p, "SignalEfficiencyConseq", "m_{H^{#pm}} (GeV/c^{2})", ylabel="Selection efficiency", addLuminosityText=False, stackMCHistograms=False, addMCUncertainty=False, opts={"xmin": 75, "xmax": 165, "ymin": 0.03, "ymaxfactor": 1.1})


if __name__ == "__main__":
    main()
