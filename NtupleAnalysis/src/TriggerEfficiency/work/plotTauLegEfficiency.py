#!/usr/bin/env python

import os
import sys
import ROOT
import array

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms

ROOT.gROOT.SetBatch(True)
plotDir = "TauLeg2015"

def usage():
    print "\n"
    print "### Usage:   "+sys.argv[0]+" <multicrab dir>\n"
    print "\n"
    sys.exit()

def getEfficiency(datasets):

    statOption = ROOT.TEfficiency.kFNormal

    first = True
    isData = False

    teff = ROOT.TEfficiency()
    for dataset in datasets:
        n = dataset.getDatasetRootHisto("Numerator").getHistogram()                                               
        d = dataset.getDatasetRootHisto("Denominator").getHistogram()

        checkNegatives(n,d)

#        removeNegatives(n)
#        removeNegatives(d)
        print dataset.getName(),"entries",n.GetEntries(),d.GetEntries()
        print "    bins",n.GetNbinsX(),d.GetNbinsX()
        eff = ROOT.TEfficiency(n,d)
        eff.SetStatisticOption(statOption)

        weight = 1
        if dataset.isMC():
            weight = dataset.getCrossSection()
            for i in range(1,d.GetNbinsX()+1):
                print "    bin",i,d.GetBinLowEdge(i),n.GetBinContent(i),d.GetBinContent(i)
        eff.SetWeight(weight)

        if first:
            teff = eff
            if dataset.isData():
                tn = n
                td = d
            first = False
        else:
            teff.Add(eff)
            if dataset.isData():
                tn.Add(n)
                td.Add(d)
    if isData:
        teff = ROOT.TEfficiency(tn, td)
        teff.SetStatisticOption(self.statOption)

    return convert2TGraph(teff)

def checkNegatives(n,d):
    for i in range(1,n.GetNbinsX()):
        nbin = n.GetBinContent(i)
        dbin = d.GetBinContent(i)
        print "Bin",i,"Numerator=",nbin,", denominator=",dbin
        if nbin > dbin:
            if nbin < dbin*1.005:
                n.SetBinContent(i,dbin)
            else:
#                print "Bin",i,"Numerator=",nbin,", denominator=",dbin
                print "REBIN!",n.GetBinLowEdge(i),"-",n.GetBinLowEdge(i)+n.GetBinWidth(i)
#                sys.exit()
def removeNegatives(histo):
    for bin in range(histo.GetNbinsX()):
        if histo.GetBinContent(bin) < 0:
            histo.SetBinContent(bin,0.)

def convert2TGraph(tefficiency):
    x     = []
    y     = []
    xerrl = []
    xerrh = []
    yerrl = []
    yerrh = []
    h = tefficiency.GetCopyTotalHisto()
    n = h.GetNbinsX()
    for i in range(1,n+1):
        x.append(h.GetBinLowEdge(i)+0.5*h.GetBinWidth(i))
        xerrl.append(0.5*h.GetBinWidth(i))
        xerrh.append(0.5*h.GetBinWidth(i))
        y.append(tefficiency.GetEfficiency(i))
        yerrl.append(tefficiency.GetEfficiencyErrorLow(i))
        # ugly hack to prevent error going above 1                                                                                                              
        errUp = tefficiency.GetEfficiencyErrorUp(i)
        if y[-1] == 1.0:
            errUp = 0
        yerrh.append(errUp)
    return ROOT.TGraphAsymmErrors(n,array.array("d",x),
                                    array.array("d",y),
                                    array.array("d",xerrl),
                                    array.array("d",xerrh),
                                    array.array("d",yerrl),
                                    array.array("d",yerrh))

def Print(graph):
    N = graph.GetN()
    for i in range(N):
        x = ROOT.Double()
        y = ROOT.Double()
        graph.GetPoint(i,x,y)
        print "x,y",x,y

def main():

    if len(sys.argv) < 2:
        usage()

    paths = [sys.argv[1]]

    analysis = "TauLeg_2015CD"
    datasets = dataset.getDatasetsFromMulticrabDirs(paths,analysisName=analysis)
    datasets.loadLuminosities()

    style = tdrstyle.TDRStyle()

    dataset1 = datasets.getDataDatasets()
    dataset2 = datasets.getMCDatasets()

    eff1 = getEfficiency(dataset1)
    eff2 = getEfficiency(dataset2)

    styles.dataStyle.apply(eff1)
    styles.mcStyle.apply(eff2)
    eff1.SetMarkerSize(1)
    eff2.SetMarkerSize(1.5)

    p = plots.ComparisonPlot(histograms.HistoGraph(eff1, "eff1", "p", "P"),
                             histograms.HistoGraph(eff2, "eff2", "p", "P"))

    opts = {"ymin": 0, "ymax": 1.1}
    opts2 = {"ymin": 0.5, "ymax": 1.5}
    moveLegend = {"dx": -0.55, "dy": -0.15, "dh": -0.1}
    name = "DataVsMC_HLTTau_PFTauPt"

    legend1 = "Data"
    legend2 = "MC"
    p.histoMgr.setHistoLegendLabelMany({"eff1": legend1, "eff2": legend2})

    p.createFrame(os.path.join(plotDir, name), createRatio=True, opts=opts, opts2=opts2)
    p.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))

    p.getFrame().GetYaxis().SetTitle("HLT tau efficiency")
    p.getFrame().GetXaxis().SetTitle("#tau-jet p_{T} (GeV/c)")
    p.getFrame2().GetYaxis().SetTitle("Ratio")
    p.getFrame2().GetYaxis().SetTitleOffset(1.6)

    histograms.addText(0.5, 0.6, "LooseIsoPFTau50_Trk30_eta2p1", 17)
    histograms.addText(0.5, 0.53, analysis.split("_")[len(analysis.split("_")) -1], 17)
    histograms.addText(0.5, 0.46, "Runs "+datasets.loadRunRange(), 17)

    p.draw()
    lumi = 0.0
    for d in datasets.getDataDatasets():
        print "luminosity",d.getName(),d.getLuminosity()
        lumi += d.getLuminosity()
    print "luminosity, sum",lumi
    histograms.addStandardTexts(lumi=lumi)

    if not os.path.exists(plotDir):
        os.mkdir(plotDir)
    p.save()

if __name__ == "__main__":
    main()
