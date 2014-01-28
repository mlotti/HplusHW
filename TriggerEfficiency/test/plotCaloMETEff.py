#!/usr/bin/env python

import sys
import os
import array

import ROOT
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots

from Plotter import Plotter


dataEra = "Run2011AB"
#dataEra = "Run2012ABCD"
searchMode = "Light"

energy = "7"
lumi = 5094.834
caloMETCut = "60"
if dataEra.find("2012") > -1:
    energy = "8"
    lumi = 887.501000+4440.000000+6843.000000+281.454000+7318.000000
    caloMETCut = "70"

analysis_d = "signalAnalysisMIdEffTrgEffWTauMuTEff"
analysis_n = "signalAnalysisMIdEffTrgEffWTauMuTEffCaloMet"+caloMETCut


def usage():
    print
    print "### Usage:   ",os.path.basename(sys.argv[0])," <embedding multicrab>"
    print
    sys.exit()

def main():

    if len(sys.argv) < 2:
        usage()

    datasets_d = dataset.getDatasetsFromMulticrabCfg(directory=sys.argv[1], analysisName=analysis_d, dataEra=dataEra, weightedCounters=False)
    datasets_n = dataset.getDatasetsFromMulticrabCfg(directory=sys.argv[1], analysisName=analysis_n, dataEra=dataEra, weightedCounters=False)

    datasets_d.updateNAllEventsToPUWeighted()
    datasets_d.loadLuminosities()
    datasets_n.updateNAllEventsToPUWeighted()
    datasets_n.loadLuminosities()

    plots.mergeRenameReorderForDataMC(datasets_d)
    plots.mergeRenameReorderForDataMC(datasets_n)

    for d in datasets_n.getAllDatasetNames():
        print d

    datasets_d.merge("MC", [
            "TTJets",
            "WJets",
            "DYJetsToLL",
            "SingleTop",
            "Diboson",
            "QCD_Pt20_MuEnriched"
            ])
    datasets_n.merge("MC", [
            "TTJets",
            "WJets",
            "DYJetsToLL",
            "SingleTop",
            "Diboson",
            "QCD_Pt20_MuEnriched"
            ])

    style = tdrstyle.TDRStyle()

    histo1 = "MET/met"
    metplot_d = plots.DataMCPlot(datasets_d, histo1)
    metplot_n = plots.DataMCPlot(datasets_n, histo1)

    den1 = metplot_d.histoMgr.getHisto("Data").getRootHisto().Clone(histo1)
    num1 = metplot_n.histoMgr.getHisto("Data").getRootHisto().Clone(histo1)
    den2 = metplot_d.histoMgr.getHisto("MC").getRootHisto().Clone(histo1)
    num2 = metplot_n.histoMgr.getHisto("MC").getRootHisto().Clone(histo1)

    ptbins = [0, 20, 30, 40, 50, 60, 70, 80, 100, 120, 140, 160, 180]
    den1 = den1.Rebin(len(ptbins)-1,"",array.array("d", ptbins))
    num1 = num1.Rebin(len(ptbins)-1,"",array.array("d", ptbins))
    den2 = den2.Rebin(len(ptbins)-1,"",array.array("d", ptbins))
    num2 = num2.Rebin(len(ptbins)-1,"",array.array("d", ptbins))

    """
    canvas = ROOT.TCanvas("canvas","",500,500)
    canvas.Divide(2,2)
    canvas.cd(1)
    num1.Draw()
    canvas.cd(2)
    num2.Draw()
    canvas.cd(3)
    den1.Draw() 
    canvas.cd(4)
    den2.Draw()
    canvas.Print("calomet.png")
    """
    eff1 = ROOT.TEfficiency(num1,den1)
    eff2 = ROOT.TEfficiency(num2,den2)

    plotDir = "CaloMET"+dataEra
    plotter = Plotter("",plotDir,lumi)

    graph1 = plotter.convert2TGraph(eff1)
    graph2 = plotter.convert2TGraph(eff2)

    styles.dataStyle.apply(eff1)
    styles.mcStyle.apply(eff2)
    graph1.SetMarkerSize(1)
    graph2.SetMarkerSize(1.5)
    graph2.SetMarkerStyle(21)
    graph2.SetMarkerColor(2)
        
    p = plots.ComparisonPlot(histograms.HistoGraph(graph1, "eff1", "p", "P"),
                             histograms.HistoGraph(graph2, "eff2", "p", "P"))
        
    p.histoMgr.setHistoLegendLabelMany({"eff1": "Data, CaloMET>"+caloMETCut, "eff2": "MC, CaloMET>"+caloMETCut})
          
    opts = {}
    opts_ = {"ymin": 0, "ymax": 1.1}
    opts_.update(opts)
            
    opts2_ = {"ymin": 0.5, "ymax": 1.5}

    moveLegend={}
    moveLegend_ = {"dx": -0.55}
    moveLegend_.update(moveLegend)

    plotter._common("calometEff", p, xlabel="MET (GeV)", ylabel="CaloMET>"+caloMETCut+" efficiency", ratio=True, energy = energy, opts=opts_, opts2=opts2_, moveLegend=moveLegend_)

    p.getFrame2().GetYaxis().SetTitle("Ratio")
    p.save()

    print "\nPlotDir",plotDir

if __name__ == "__main__":
    main()
