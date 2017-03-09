#!/usr/bin/env python

import os
import sys
import ROOT

import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.styles as styles
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux

from plotTauLegEfficiency import getEfficiency,convert2TGraph,Print

ROOT.gROOT.SetBatch(True)
plotDir = "L1Plots"

formats = [".pdf",".png"]

def usage():
    print "\n"
    print "### Usage:   "+sys.argv[0]+" <multicrab dir>\n"
    print "\n"
    sys.exit()

def main():

    if len(sys.argv) < 2:
        usage()

    analyze()

def fit(name,plot,graph,min,max):
    function = ROOT.TF1("fit"+name, "[0]*x + [1]", min, max);
    #function.SetParameters(1., 50., 1.);
    #function.SetParLimits(0, 0.0, 1.0);
    fitResult = graph.Fit(function, "NRSE+EX0");
    aux.copyStyle(graph, function)
    plot.appendPlotObject(function)
    xval = 55
    yval = function.Eval(xval)
    print "Value at",xval,"=",yval


def analyze(analysis=None):

    paths = [sys.argv[1]]

    datasets = dataset.getDatasetsFromMulticrabDirs(paths)
    analysis = datasets.getAllDatasets()[0].getAnalysisName()

    #datasetsMC = dataset.getDatasetsFromMulticrabDirs(paths,analysisName=analysis,excludeTasks="ZeroBias")


    createRatio = False

    for d in datasets.getAllDatasets():
        print d.getName()
        style = tdrstyle.TDRStyle()

        dataset1 = datasets.getDataDatasets()
        dataset2 = dataset1
        createRatio = False
        #if isinstance(datasetsMC,dataset.DatasetManager):
        #    dataset2 = datasetsMC.getMCDatasets()
        #    createRatio = True

    eff1PU = getEfficiency(dataset1,"NumeratorPU","DenominatorPU")


    namePU = "TauMET_"+analysis+"_nVtx"
    legend1 = "Data"
    legend2 = "Simulation"

    styles.dataStyle.apply(eff1PU)
    eff1PU.SetMarkerSize(1)
    #eff2PU.SetMarkerSize(1.5)

    pPU = plots.PlotBase([histograms.HistoGraph(eff1PU, "eff1", "p", "P")])
    pPU.histoMgr.setHistoLegendLabelMany({"eff1": legend1})

    fit("Data",pPU,eff1PU,5,60)

    opts = {"ymin": 0.000001, "ymax": 0.001}
    opts2 = {"ymin": 0.5, "ymax": 1.5}
    moveLegend = {"dx": -0.5, "dy": -0.1, "dh": -0.1}

    if createRatio:
        pPU.createFrame(os.path.join(plotDir, namePU), createRatio=True, opts=opts, opts2=opts2)
    else:
        pPU.createFrame(os.path.join(plotDir, namePU), opts=opts, opts2=opts2)
    pPU.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))

    pPU.getFrame().GetYaxis().SetTitle("L1 efficiency")
    pPU.getFrame().GetXaxis().SetTitle("pileup")
    if createRatio:
        pPU.getFrame2().GetYaxis().SetTitle("Ratio")
        pPU.getFrame2().GetYaxis().SetTitleOffset(1.6)

    pPU.draw()
    lumi = 0.0
    for d in datasets.getDataDatasets():
        print "luminosity",d.getName(),d.getLuminosity()
        lumi += d.getLuminosity()
    histograms.addStandardTexts(lumi=lumi)

    if not os.path.exists(plotDir):
        os.mkdir(plotDir)
    pPU.save(formats)

    print "Output written in",plotDir

if __name__ == "__main__":
    main()
