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
#counters = analysis+"Counters/weighted"

searchMode = "Light"
#searchMode = "Heavy"



#dataEra = "Run2011A"
#dataEra = "Run2011B"
dataEra = "Run2011AB"

#optMode = "OptQCDTailKillerZeroPlus"
optMode = "OptQCDTailKillerLoosePlus"
#optMode = "OptQCDTailKillerMediumPlus"
#optMode = "OptQCDTailKillerTightPlus"

#optMode = "OptMET60TopNoneQCDTailKillerTightPlus"
#optMode = "OptMET80QCDTailKillerLoosePlus"
#optMode = "OptBdiscr02"
#optMode = ""

# main function
def main():
    # Read the datasets
    #datasets = dataset.getDatasetsFromMulticrabCfg(counters=counters)
    datasets = dataset.getDatasetsFromMulticrabCfg(analysisName=analysis, searchMode=searchMode, dataEra=dataEra, optimizationMode=optMode)
    datasets.updateNAllEventsToPUWeighted()    
    datasets.loadLuminosities()

    plots.mergeRenameReorderForDataMC(datasets)

    # Remove signals other than M120
###    datasets.remove(filter(lambda name: "TTToHplus" in name and not "M120" in name, datasets.getAllDatasetNames()))
    #datasets.remove(filter(lambda name: "HplusTB" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "TTToHplusBHminusB" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "TTToHplus" in name, datasets.getAllDatasetNames()))    
    # Set the signal cross sections to a given BR(t->H), BR(h->taunu)
    xsect.setHplusCrossSectionsToBR(datasets, br_tH=0.05, br_Htaunu=1)

    # Set the signal cross sections to a value from MSSM
#    xsect.setHplusCrossSectionsToMSSM(datasets, tanbeta=20, mu=200)

###    plots.mergeWHandHH(datasets) # merging of WH and HH signals must be done after setting the cross section

    style = tdrstyle.TDRStyle()
    eventCounter = counter.EventCounter(datasets)    
    #eventCounter = counter.EventCounter(datasets, counters=counters)
    eventCounter.normalizeMCByCrossSection()
    mainTable = eventCounter.getMainCounterTable()
    cellFormat = counter.TableFormatText(cellFormat=counter.CellFormatText(valueOnly=True))
    print mainTable.format(cellFormat)

    #eventCounterUnweighted = counter.EventCounter(datasets, mainCounterOnly=True, counters="counters")
    #eventCounterUnweighted.normalizeMCByCrossSection()
    #mainTableUnweighted = eventCounterUnweighted.getMainCounterTable()
    #print mainTableUnweighted.format(cellFormat)
    
    signalDatasets = [
        "HplusTB_M180",
        "HplusTB_M190",
        "HplusTB_M200",
        "HplusTB_M220",
        "HplusTB_M250",
        "HplusTB_M300",
        #"HplusTB_M400",
        #"HplusTB_M500",
        #"HplusTB_M600",
        #"TTToHplusBWB_M80",
        #"TTToHplusBWB_M90",
        #"TTToHplusBWB_M100",
        #"TTToHplusBWB_M120",
        #"TTToHplusBWB_M140",
        #"TTToHplusBWB_M150",
        #"TTToHplusBWB_M155",
        #"TTToHplusBWB_M160", 
        ]
    allName = "Trigger and HLT_MET cut"

    cuts = [
        #"Offline selection begins",
        "Trigger and HLT_MET cut",
        "primary vertex",
        "taus == 1",
        "tau trigger scale factor",
        "electron veto",
        "muon veto",
        "njets",
        "QCD tail killer collinear",
        "MET",
        "btagging",
        "btagging scale factor",
        "QCD tail killer back-to-back"
        ]

    xvalues = [180, 190, 200, 220, 250, 300]
    #xvalues = [80, 90, 100, 120, 140, 150, 155, 160]
    xerrs = [0]*len(xvalues)
    yvalues = {}
    yerrs = {}
    for cut in cuts:
        yvalues[cut] = []
        yerrs[cut] = []
    for name in signalDatasets:
        column = mainTable.getColumn(name=name)
        #columnUnweighted = mainTableUnweighted.getColumn(name=name)

        # Get the counts (returned objects are of type dataset.Count,
        # and have both value and uncertainty
        #allCount = column.getCount(column.getRowNames().index("Trigger and HLT_MET cut"))
        # Somewhat weird way to get total cross section via unweighted counters
        #rowNames = column.getRowNames()
        #if "allEvents" in rowNames:
        #    allCount = columnUnweighted.getCount(rowNames.index("allEvents"))
        #else:
        #    # Hack needed because non-triggered signal pattuples do not have allEvents counter!
        #    allCount = columnUnweighted.getCount(rowNames.index("primaryVertexAllEvents"))
        #dset = datasets.getDataset(name)
        #allCount.multiply(dataset.Count(dset.getNAllEvents()/dset.getNAllEventsUnweighted()))
        allCount = dataset.Count(datasets.getDataset(name).getCrossSection(), 0)

        for cut in cuts:
            cutCount = column.getCount(column.getRowNames().index(cut))
            eff = cutCount.clone()
            eff.divide(allCount) # N(cut) / N(all)
            if column.getRowNames().index(cut) == 9: ## btagging             
                print cut,eff.value()
            yvalues[cut].append(eff.value())
            yerrs[cut].append(eff.uncertainty())

    def createErrors(cutname):
        gr = ROOT.TGraphErrors(len(xvalues), array.array("d", xvalues), array.array("d", yvalues[cutname]),
                               array.array("d", xerrs), array.array("d", yerrs[cutname]))
        gr.SetMarkerStyle(24)
        gr.SetMarkerColor(2)
        gr.SetMarkerSize(0.9)
        gr.SetLineStyle(1)
        gr.SetLineWidth(2)
        return gr

    #gtrig = createErrors("primary vertex")
    gtrig = createErrors("Trigger and HLT_MET cut")
    print gtrig
    gtrig.SetLineColor(38)
    gtrig.SetMarkerColor(38)
    gtrig.SetMarkerStyle(20)
    gtrig.SetLineStyle(2)
    gtrig.SetMarkerSize(2)
    
    gtau = createErrors("taus == 1")
    gtau.SetLineColor(2)
    gtau.SetMarkerColor(2)
    gtau.SetMarkerStyle(20)
    gtau.SetMarkerSize(2)
    gtau.SetLineStyle(3)  
    #gtau = createErrors("trigger scale factor")
    
    gveto = createErrors("muon veto")
    gveto.SetLineColor(1)
    gveto.SetMarkerColor(1)
    gveto.SetMarkerStyle(21)
    gveto.SetMarkerSize(2)
    gveto.SetLineStyle(4) 
    gjets = createErrors("njets")
    gjets.SetLineColor(4)
    gjets.SetMarkerColor(4)
    gjets.SetMarkerStyle(22)
    gjets.SetMarkerSize(2)
    gjets.SetLineStyle(1)
    gcoll = createErrors("QCD tail killer collinear")
    gcoll.SetLineColor(6)
    gcoll.SetMarkerColor(6)
    gcoll.SetMarkerStyle(26)
    gcoll.SetMarkerSize(2)
    gcoll.SetLineStyle(2) 
    gmet = createErrors("MET")
    gmet.SetLineColor(1)
    gmet.SetMarkerColor(1)
    gmet.SetMarkerStyle(24)
    gmet.SetMarkerSize(2)
    gmet.SetLineStyle(5) 
    gbtag = createErrors("btagging")
    gbtag.SetLineColor(2)
    gbtag.SetMarkerColor(2)
    gbtag.SetMarkerStyle(25)
    gbtag.SetMarkerSize(2)
    gbtag.SetLineStyle(6)
    print gbtag
    gback = createErrors("QCD tail killer back-to-back")
    gback.SetLineColor(7)
    gback.SetMarkerColor(7)
    gback.SetMarkerStyle(23)
    gback.SetMarkerSize(2)
    gback.SetLineStyle(1)
    #gtau = createErrors("trigger scale factor")

                        
    glist = [gtrig, gtau, gveto, gjets, gcoll, gmet, gbtag, gback]
    
    opts = {"xmin": 175, "xmax": 310, "ymin": 0.001}
    canvasFrame = histograms.CanvasFrame([histograms.HistoGraph(g, "", "") for g in glist], "SignalEfficiency", **opts)
    canvasFrame.frame.GetYaxis().SetTitle("Selection efficiency")
    canvasFrame.frame.GetXaxis().SetTitle("m_{H^{#pm}} (GeV/c^{2})")
    canvasFrame.canvas.SetLogy(True)
    canvasFrame.frame.Draw()

    for gr in glist:
        gr.Draw("PC same")
    
    histograms.addStandardTexts()

    legend2 = histograms.createLegend(x1=0.5, y1=0.7, x2=0.9, y2=0.85)

    legend2.AddEntry(gtrig,"Trigger", "lp"); 
    legend2.AddEntry(gtau, "Loose #tau identification", "lp"); 
    legend2.AddEntry(gveto ,"lepton vetoes", "lp"); 
    legend2.AddEntry(gjets ,"3 jets", "lp"); 
    legend2.Draw()
    
    legend = histograms.createLegend(x1=0.35, y1=0.15, x2=0.7, y2=0.3)
    legend.AddEntry(gcoll ,"QCD tail killer collinear", "lp"); 
    legend.AddEntry(gmet,"MET > 60 GeV", "lp")
    legend.AddEntry(gbtag,"b tagging ", "lp")
    legend.AddEntry(gback ,"QCD tail killer back-to-back: Tight", "lp"); 
    legend.Draw()    
    canvasFrame.canvas.SaveAs(".png")
    canvasFrame.canvas.SaveAs(".C")
    canvasFrame.canvas.SaveAs(".eps")
    
# Call the main function if the script is executed (i.e. not imported)
if __name__ == "__main__":
    main()
