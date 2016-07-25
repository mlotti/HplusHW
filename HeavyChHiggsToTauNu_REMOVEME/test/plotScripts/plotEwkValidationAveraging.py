#!/usr/bin/env python

######################################################################
#
# This plot script is for comparing the embedded MC and normal MC
# within signal analysis. The corresponding python job
# configurations are
# * signalAnalysis_cfg.py with "tauEmbeddingInput=1"
# for embedded signal analysis
#
# Authors: Matti Kortelainen
#
######################################################################

import os
import re
import array
import math
from optparse import OptionParser

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tauEmbedding as tauEmbedding

analysisEmb = "signalAnalysis"
dataEra = "Run2012ABCD"

myStyles = [styles.getDataStyle()]
for st in styles.getStyles():
    myStyles.append(st)
    #myStyles.append(styles.StyleCompound([st, styles.StyleLine(lineStyle=2)]))

def main():
    dirAve = "."
    # dirSeeds = []
    # inputInfoPath = os.path.join(dirAve, "inputInfo.txt")
    # f = open(inputInfoPath)
    # input_re = re.compile("Embedded input directory: (?P<dir>\S+)")
    # for line in f:
    #     m = input_re.search(line)
    #     if m:
    #         dirSeeds.append(os.path.join("..", m.group("dir")))
    # f.close()
    # if len(dirSeeds) == 0:
    #     raise Exception("Found 0 input directories from %s" % inputInfoPath)

    parser = OptionParser(usage="Usage: %prog seed0 [seed1 ...]")
    #parser.add_option("-s", "--seed", dest="dirSeeds", default=[], action="append"
    #                  help="Path to pseudo-multicrab with a single seed (can be given multiple times)")

    (opts, args) = parser.parse_args()
    if len(args) == 0:
        parser.error("No seed pseudo-multicrab directories were given")

#    dirSeeds = [
##        "../embedding_140509_100532",
##        "../embedding_seedTest1_140508_154221",
##        "../embedding_seedTest2_140508_154540",
##        "../embedding_seedTest3_140508_155055",
##        "../embedding_seedTest4_140508_155742"
#        "../embedding_mc_tightPlus_140512_160900",
#        "../embedding_mc_seedTest1_140807_084326"
#        ]
    dirSeeds = args

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    histograms.createLegend.moveDefaults(dx=-0.02)
    histograms.uncertaintyMode.set(histograms.uncertaintyMode.StatOnly)
    histograms.createLegendRatio.moveDefaults(dh=-0.1, dx=-0.53)
    plots._legendLabels["BackgroundStatError"] = "Avg. stat. unc."

    for optMode in [
#        "OptQCDTailKillerZeroPlus",

        "OptQCDTailKillerLoosePlus",
#        "OptQCDTailKillerMediumPlus",
        "OptQCDTailKillerTightPlus",

#        "OptQCDTailKillerVeryTightPlus",
#            None
        ]:
        datasetsAve = dataset.getDatasetsFromMulticrabCfg(directory=dirAve, dataEra=dataEra, analysisName=analysisEmb, optimizationMode=optMode)
        datasetsSeeds = [
            dataset.getDatasetsFromMulticrabCfg(directory=d, dataEra=dataEra, analysisName=analysisEmb, optimizationMode=optMode) for d in dirSeeds
            ]
        doDataset(datasetsAve, datasetsSeeds, optMode)
        datasetsAve.close()
        for d in datasetsSeeds:
            d.close()

        tauEmbedding.writeToFile(optMode+"_average", "input.txt", ("Average: %s\n" % os.getcwd()) + "\n".join(["Seed: "+s for s in dirSeeds]))


drawPlotCommon = plots.PlotDrawer(ylabel="Events / %.0f", stackMCHistograms=False, log=True, addMCUncertainty=True,
                                  ratio=True, ratioType="errorScale", ratioCreateLegend=True,
                                  addLuminosityText=True)

def doDataset(datasetsAve, datasetsSeeds, optMode):
    ds = [datasetsAve]+datasetsSeeds

    for d in ds:
        d.updateNAllEventsToPUWeighted()
        plots.mergeRenameReorderForDataMC(d)

    plotter = tauEmbedding.CommonPlotter(optMode+"_average", "average", drawPlotCommon)

    doPlots(datasetsAve, datasetsSeeds, "Data", plotter)
#    doPlots(datasetsAve, datasetsSeeds, "TTJets", plotter)


def doPlots(datasetsAve, datasetsSeeds, datasetName, plotter):
    dsetAve = datasetsAve.getDataset(datasetName)
    dsetSeeds = [d.getDataset(datasetName) for d in datasetsSeeds]
    lumi = datasetsAve.getDataset("Data").getLuminosity()

    addEventCounts = False

    compatTests = []
    compatTestsAve = []

    def createPlot(name):
        drhAve = dsetAve.getDatasetRootHisto(name)
        drhAve.setName("Average")
        if drhAve.isMC():
            drhAve.normalizeToLuminosity(lumi)
        drhSeeds = []
        for i, d in enumerate(dsetSeeds):
            drh = d.getDatasetRootHisto(name)
            drh.setName("Seed %d" % i)
            if drh.isMC():
                drh.normalizeToLuminosity(lumi)
            drhSeeds.append(drh)

        if name == "shapeTransverseMass":
            tha = drhAve.getHistogram()
            for i, di in enumerate(drhSeeds):
                thi = di.getHistogram()
                chi2 = tha.Chi2Test(thi, "WW")
                kolmo = tha.KolmogorovTest(thi)
                compatTestsAve.append( ("a+%d" % i, chi2, kolmo) )

                for j in xrange(i+1, len(drhSeeds)):
                    thj = drhSeeds[j].getHistogram()
                    chi2 = thi.Chi2Test(thj, "WW")
                    kolmo = thi.KolmogorovTest(thj)
                    compatTests.append( ("%d+%d" % (i, j), chi2, kolmo) )

        p = plots.ComparisonManyPlot(drhAve, drhSeeds)
        p.setLuminosity(lumi)
        legLabel = plots._legendLabels.get(datasetName, datasetName)
        leg = "Average "+legLabel
        if addEventCounts:
            leg += " ("+tauEmbedding.strIntegral(drhAve.getHistogram())+")"
        p.histoMgr.setHistoLegendLabelMany({"Average": leg})
        for i, drh in enumerate(drhSeeds):
            leg = ("Seed %d "%i)+legLabel
            if addEventCounts:
                leg += " ("+tauEmbedding.strIntegral(drh.getHistogram())+")"
            p.histoMgr.setHistoLegendLabelMany({"Seed %d"%i: leg})
        p.histoMgr.forEachHisto(styles.Generator(styles=myStyles))

        p.setDrawOptions(ratioYlabel="Seed/Average")
        return p

    plotter.plot(datasetName, createPlot)

    print "Chi2-probability and Kolmogorov-probability of all pair-wise comparisons"
    hchi2 = ROOT.TH1F("chi2", "chi2;#chi^{2} probability;Entries", 100, 0, 1)
    hchi2a = ROOT.TH1F("chi2_ave", "chi2;#chi^{2} probability;Entries", 100, 0, 1)
    hkolmo = ROOT.TH1F("kolmogorov", "kolmo;Kolmogorov probability;Entries", 100, 0, 1)
    hkolmoa = ROOT.TH1F("kolmogorov_ave", "kolmo;Kolmogorov probability;Entries", 100, 0, 1)
    for pair, chi2, kolmo in compatTests:
        print "%s: %f %f" % (pair, chi2, kolmo)
        hchi2.Fill(chi2)
        hkolmo.Fill(kolmo)
    for pair, chi2, kolmo in compatTestsAve:
        print "%s: %f %f" % (pair, chi2, kolmo)
        hchi2a.Fill(chi2)
        hkolmoa.Fill(kolmo)

    for th1 in [hchi2, hchi2a, hkolmo, hkolmoa]:
        p = plots.PlotBase([th1])
        p.setLuminosity(lumi)
        plots.drawPlot(p, os.path.join(plotter.getOutputDirectory(), datasetName+"_"+th1.GetName()), ylabel="Entries", createLegend=None)

if __name__ == "__main__":
    main()

