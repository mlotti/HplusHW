#!/usr/bin/env python

######################################################################
#
# This plot script is for comparing the embedded data to embedding MC
# within the signal analysis. The corresponding python job
# configuration is signalAnalysis_cfg.py with "doPat=1
# tauEmbeddingInput=1" command line arguments.
#
# Authors: Ritva Kinnunen, Matti Kortelainen
#
######################################################################

import ROOT
ROOT.gROOT.SetBatch(True)
import math
import array

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect

# Configuration
analysis = "signalAnalysis"
#analysis = "signalOptimisation"
#analysis = "signalAnalysisJESMinus03eta02METMinus10"
#analysis = "EWKFakeTauAnalysisJESMinus03eta02METMinus10"
#analysis = "signalOptimisation/QCDAnalysisVariation_tauPt40_rtau0_btag2_METcut60_FakeMETCut0"
#analysis = "signalAnalysisTauSelectionHPSTightTauBased2"
#analysis = "signalAnalysisBtaggingTest2"
counters = analysis+"Counters/weighted"

# main function
def main():
    # Read the datasets
    datasets = dataset.getDatasetsFromMulticrabCfg(counters=counters)
    datasets.loadLuminosities()

    plots.mergeRenameReorderForDataMC(datasets)

    # Remove signals other than M120
###    datasets.remove(filter(lambda name: "TTToHplus" in name and not "M120" in name, datasets.getAllDatasetNames()))
###    datasets.remove(filter(lambda name: "HplusTB" in name, datasets.getAllDatasetNames()))

    # Set the signal cross sections to a given BR(t->H), BR(h->taunu)
    xsect.setHplusCrossSectionsToBR(datasets, br_tH=0.05, br_Htaunu=1)

    # Set the signal cross sections to a value from MSSM
#    xsect.setHplusCrossSectionsToMSSM(datasets, tanbeta=20, mu=200)

###    plots.mergeWHandHH(datasets) # merging of WH and HH signals must be done after setting the cross section

    style = tdrstyle.TDRStyle()

    eventCounter = counter.EventCounter(datasets, counters=counters)
    eventCounter.normalizeMCByCrossSection()
    mainTable = eventCounter.getMainCounterTable()

    signalDatasets = [
        "TTToHplusBWB_M80",
        "TTToHplusBWB_M90",
        "TTToHplusBWB_M100",
        "TTToHplusBWB_M120",
        "TTToHplusBWB_M140",
        "TTToHplusBWB_M150",
        "TTToHplusBWB_M155",
        "TTToHplusBWB_M160",
        ]
    allName = "All events"

    cuts = [
        "Trigger and HLT_MET cut",
        "primary vertex",
        "taus == 1",
        "trigger scale factor",
        "electron veto",
        "muon veto",
        "njets",
        "MET",
        "btagging",
        "btagging scale factor"
        ]

    xvalues = [80, 90, 100, 120, 140, 150, 155, 160]
    xerrs = [0]*len(xvalues)
    yvalues = {}
    yerrs = {}
    for cut in cuts:
        yvalues[cut] = []
        yerrs[cut] = []
    for name in signalDatasets:
        column = mainTable.getColumn(name=name)

        # Get the counts (returned objects are of type dataset.Count,
        # and have both value and uncertainty
        allCount = column.getCount(column.getRowNames().index("All events"))

        for cut in cuts:
            cutCount = column.getCount(column.getRowNames().index(cut))
            eff = cutCount.clone()
            eff.divide(allCount) # N(cut) / N(all)
        
            yvalues[cut].append(eff.value())
            yerrs[cut].append(eff.uncertainty())

    def createErrors(cutname):
        gr = ROOT.TGraphErrors(len(xvalues), array.array("d", xvalues), array.array("d", yvalues[cutname]),
                               array.array("d", xerrs), array.array("d", yerrs[cutname]))
        gr.SetMarkerStyle(24)
        gr.SetMarkerColor(2)
        gr.SetMarkerSize(0.9)
        gr.SetLineStyle(1)
        gr.SetLineWidth(1)
        return gr

    gtrig = createErrors("Trigger and HLT_MET cut")
    gtau = createErrors("taus == 1")
    #gtau = createErrors("trigger scale factor")
    gveto = createErrors("muon veto")
    gjets = createErrors("njets")
    gmet = createErrors("MET")
    gbtag = createErrors("btagging")
    #gtau = createErrors("trigger scale factor")
    gbtag.SetLineColor(1)
                        
    glist = [gtrig, gtau, gjets, gmet, gbtag]
    
    opts = {"xmin": 75, "xmax": 165, "ymin": 0.001}
    canvasFrame = histograms.CanvasFrame([histograms.HistoGraph(g, "", "") for g in glist], "SignalEfficiency", **opts)
    canvasFrame.frame.GetYaxis().SetTitle("Selection efficiency")
    canvasFrame.frame.GetXaxis().SetTitle("m_{H^{#pm}} (GeV/c^{2})")
    canvasFrame.canvas.SetLogy(True)
    canvasFrame.frame.Draw()

    for gr in glist:
        gr.Draw("PC same")
    
    histograms.addEnergyText()
    histograms.addCmsPreliminaryText()

    legend = histograms.createLegend(x1=0.5, y1=0.53, x2=0.85, y2=0.75)

    legend.AddEntry(gtrig,"Trigger", "l"); 
    legend.AddEntry(gtau, "#tau identification", "l"); 
    legend.AddEntry(gveto ,"lepton vetoes", "l"); 
    legend.AddEntry(gjets ,"3 jets", "l"); 
    legend.AddEntry(gmet,"MET ", "l")
    legend.AddEntry(gbtag,"b tagging ", "l")
    legend.Draw()
    
    canvasFrame.canvas.SaveAs(".png")
    canvasFrame.canvas.SaveAs(".C")
    canvasFrame.canvas.SaveAs(".eps")
    
# Call the main function if the script is executed (i.e. not imported)
if __name__ == "__main__":
    main()
