#!/usr/bin/env python

######################################################################
#
# Plot QCD purity as a function of tau pt
#
# 25032013/S.Lehti
#
######################################################################

analysis = "signalAnalysisInvertedTau"

searchMode = "Light"
#searchMode = "Heavy"

#dataEra = "Run2011A"
#dataEra = "Run2011B"
dataEra = "Run2012ABCD"

binning = [41,50,60,70,80,100,120,150,300]

HISTONAMES = []
HISTONAMES.append("SelectedTau_pT_AfterTauID")
HISTONAMES.append("SelectedTau_pT_AfterMetCut")

import ROOT
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots

import sys
import array
import re

def usage():
    print
    print "### Usage:   ",sys.argv[0],"<multicrab dir>"
    print
    sys.exit()
    
def main():

    if len(sys.argv) < 2:
        usage()

    dirs = []
    dirs.append(sys.argv[1])
        
    datasets = dataset.getDatasetsFromMulticrabDirs(dirs,dataEra=dataEra, searchMode=searchMode, analysisName=analysis)
    datasets.loadLuminosities()
    datasets.updateNAllEventsToPUWeighted()

    plots.mergeRenameReorderForDataMC(datasets)

    datasets.merge("EWK", [
                    "TTJets",
                    "WJets",
                    "DYJetsToLL",
                    "SingleTop",
                    "Diboson"
                    ])
    style = tdrstyle.TDRStyle()

    plot = plots.PlotBase()

    legends = {}
    name_re = re.compile("SelectedTau_pT_(?P<name>\S+)")
    for i,histo in enumerate(HISTONAMES):
        plot.histoMgr.appendHisto(purityGraph(i,datasets,histo))
        name = histo
        match = name_re.search(histo)
        if match:
            name = match.group("name")
        legends["Purity%s"%i] = name

    plot.createFrame("purity", opts={"xmin": 40, "ymin": 0., "ymax": 1.2})
    plot.frame.GetXaxis().SetTitle("tau p_{T} (GeV/c)")
    plot.frame.GetYaxis().SetTitle("Purity")
    plot.setEnergy(datasets.getEnergies())
    plot.setLuminosity(datasets.getDataset("Data").getLuminosity())
    
    plot.histoMgr.setHistoLegendLabelMany(legends)
    plot.setLegend(histograms.createLegend(0.6, 0.3, 0.8, 0.4))

    plot.addStandardTexts()

    plot.draw()
    plot.save()
            
def purityGraph(i,datasets,histo):
    inverted = plots.DataMCPlot(datasets, histo)
#    inverted.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))
    inverted.histoMgr.forEachHisto(lambda h: h.setRootHisto(h.getRootHisto().Rebin(len(binning)-1,h.getRootHisto().GetName(),array.array('d',binning))))
    
    invertedData = inverted.histoMgr.getHisto("Data").getRootHisto().Clone(histo)
    invertedEWK  = inverted.histoMgr.getHisto("EWK").getRootHisto().Clone(histo)

    numerator = invertedData.Clone()
    numerator.SetName("numerator")
    numerator.Add(invertedEWK,-1)
    denominator = invertedData.Clone()
    denominator.SetName("denominator")

    numerator.Divide(denominator)
    purityGraph = ROOT.TGraphAsymmErrors(numerator)

    """
    purity = ROOT.TEfficiency(numerator,denominator)
    purity.SetStatisticOption(ROOT.TEfficiency.kFNormal)

    collection = ROOT.TObjArray()
    collection.Add(purity)

    weights = []
    weights.append(1)

    purityGraph = ROOT.TEfficiency.Combine(collection,"",len(weights),array.array("d",weights))
    """
    purityGraph.SetMarkerStyle(20+i)
    purityGraph.SetMarkerColor(2+i)

    defaults = {"drawStyle": "EP","legendStyle": "p"}
    
    return histograms.Histo(purityGraph, "Purity%s"%i, **defaults)
    
if __name__ == "__main__":
    main()
