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

    wh = [
        "TTToHplusBWB_M80",
        "TTToHplusBWB_M90",
        "TTToHplusBWB_M100",
        "TTToHplusBWB_M120",
        "TTToHplusBWB_M140",
        "TTToHplusBWB_M150",
        "TTToHplusBWB_M155",
        "TTToHplusBWB_M160",
        ]
    hh = [
        "TTToHplusBHminusB_M80",
        "TTToHplusBHminusB_M90",
        "TTToHplusBHminusB_M100",
        "TTToHplusBHminusB_M120",
        "TTToHplusBHminusB_M140",
        "TTToHplusBHminusB_M150",
        "TTToHplusBHminusB_M155",
        "TTToHplusBHminusB_M160",
        ]

    doPlots(mainTable, wh, "HW", True)
    doPlots(mainTable, wh, "HW", False)
    doPlots(mainTable, hh, "HH", True)
    doPlots(mainTable, hh, "HH", False)

def doPlots(mainTable, signalDatasets, signalPostfix, consequtive=True):
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
        prevCount = allCount

        for cut in cuts:
            cutCount = column.getCount(column.getRowNames().index(cut))
            eff = cutCount.clone()
            if consequtive:  
                eff.divide(prevCount)
                prevCount = cutCount
            else:
                eff.divide(allCount) # N(cut) / N(all)
        
            yvalues[cut].append(eff.value())
            yerrs[cut].append(eff.uncertainty())

    def createErrors(cutname):
        gr = ROOT.TGraphErrors(len(xvalues), array.array("d", xvalues), array.array("d", yvalues[cutname]),
                               array.array("d", xerrs), array.array("d", yerrs[cutname]))
        gr.SetMarkerStyle(24)
        gr.SetMarkerColor(2)
        gr.SetMarkerSize(2)
        gr.SetLineStyle(1)
        gr.SetLineWidth(4)
        return gr

    def setStyle(gr, lc, ls, ms):
        gr.SetLineColor(lc)
        gr.SetLineStyle(ls)
        gr.SetMarkerColor(lc)
        gr.SetMarkerStyle(ms)

    gtrig = createErrors("Trigger and HLT_MET cut")
    setStyle(gtrig, lc=38, ls=8, ms=20)

    #gtau = createErrors("trigger scale factor")
    gtau = createErrors("taus == 1")
    setStyle(gtau, lc=2, ls=3, ms=21)

    gveto = createErrors("muon veto")
    setStyle(gveto, lc=1, ls=5, ms=22)

    gjets = createErrors("njets")
    setStyle(gjets, lc=4, ls=1, ms=23)

    gmet = createErrors("MET")
    setStyle(gmet, lc=2, ls=2, ms=24)

    gbtag = createErrors("btagging")
    setStyle(gbtag, lc=1, ls=6, ms=24)
                        
    glist = [gtrig, gtau, gveto, gjets, gmet, gbtag]
    
    #opts = {"xmin": 75, "xmax": 165, "ymin": 0.001}
    opts = {"xmin": 75, "xmax": 165, "ymin": 7e-4, "ymax": 2e-1}
    name = "SignalEfficiency"
    if consequtive:
        opts.update({"ymin": 2.5e-2, "ymax": 1.15})
        name += "Conseq"
    name += "_"+signalPostfix

    canvasFrame = histograms.CanvasFrame([histograms.HistoGraph(g, "", "") for g in glist], name, **opts)
    canvasFrame.frame.GetYaxis().SetTitle("Selection efficiency")
    canvasFrame.frame.GetXaxis().SetTitle("m_{H^{#pm}} (GeV/c^{2})")
    canvasFrame.canvas.SetLogy(True)
    canvasFrame.frame.Draw()

    for gr in glist:
        gr.Draw("PL same")
    
    histograms.addEnergyText()
    histograms.addCmsPreliminaryText()

    legend = histograms.createLegend(x1=0.5, y1=0.53, x2=0.85, y2=0.75)
    legend = histograms.moveLegend(legend, dx=-0.3, dy=-0.04)

    legend.AddEntry(gtrig,"Trigger", "lp"); 
    legend.AddEntry(gtau, "#tau-jet identification", "lp"); 
    legend.AddEntry(gveto ,"lepton vetoes", "lp"); 
    legend.AddEntry(gjets ,"3 jets", "lp"); 
    legend.AddEntry(gmet,"E_{T}^{miss} ", "lp")
    legend.AddEntry(gbtag,"b tagging ", "lp")
    legend.Draw()

    process = {    
        "HW": "t#bar{t} #rightarrow W^{+}bH^{-}#bar{b}",
        "HH": "t#bar{t} #rightarrow H^{+}bH^{-}#bar{b}"
        }[signalPostfix]

    histograms.addText(x=legend.GetX1()+0.02, y=legend.GetY2()+0.01,
                       text=process, size=17)

    canvasFrame.canvas.SaveAs(".png")
    canvasFrame.canvas.SaveAs(".C")
    canvasFrame.canvas.SaveAs(".eps")

# Call the main function if the script is executed (i.e. not imported)
if __name__ == "__main__":
    main()
