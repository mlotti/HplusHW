#!/usr/bin/env python

# a script for plotting any histogram in the analysis results
# input:
#     - result dir containing at least signalAnalysis and QCDAnalysis 
#       pseudomulticrabs (same input as for the datacard generator)
#     - json file containing descriptions for the plotting
# 02122016/S.Lehti

import os
import sys
import re
import json

import HiggsAnalysis.LimitCalc.MulticrabPathFinder as PathFinder
import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms

import ROOT
ROOT.gROOT.SetBatch(True)

formats = [".pdf",".png"]
plotDir = "Plots"

def usage():
    print
    print "### Usage:  ",sys.argv[0],"<resultdir containing at least signalAnalysis and QCD pseudomulticrab> <histogram-json>"
    print
    sys.exit()


def str2bool(dictIn):
    dictOut = {}
    for d in dictIn.keys():
        dictOut[d] = dictIn[d]
        if isinstance(dictOut[d],str) and (dictOut[d]).lower() == "true":
            dictOut[d] = True
        if isinstance(dictOut[d],str) and (dictOut[d]).lower() == "false":
            dictOut[d] = False
    return dictOut
    

def plot(resultdir,jsonfile):
    with open(os.path.abspath(jsonfile)) as jfile:
        j = json.load(jfile)
        print "Plotting",j["title"],"in",resultdir

        if "outputdir" in j:
            global plotDir
            plotDir = j["outputdir"]
        multicrabPaths = PathFinder.MulticrabPathFinder(resultdir)


        paths = []
        if os.path.exists(multicrabPaths.getSignalPath()):
            paths.append(multicrabPaths.getSignalPath())
        if os.path.exists(multicrabPaths.getQCDInvertedPath()):
            paths.append(multicrabPaths.getQCDInvertedPath())
        if os.path.exists(multicrabPaths.getEWKPath()):
            paths.append(multicrabPaths.getEWKPath())

        datasets = dataset.getDatasetsFromMulticrabDirs(paths)

        datasets.loadLuminosities()
        style = tdrstyle.TDRStyle()
        plots.mergeRenameReorderForDataMC(datasets)

        alldsets = datasets.getAllDatasets()
        print "Merged datasets"
        for d in alldsets:
            print "       ",d.getName()

        lumi = 0.0
        for d in datasets.getDataDatasets():
            print "luminosity",d.getName(),d.getLuminosity()
            lumi += d.getLuminosity()
        print "luminosity, sum",lumi

        if len(j["samples"])>0:
           for s in j["samples"]:
               h = datasets.getDataset(s).getDatasetRootHisto(j["histogram"]).getHistogram()
               name = j["histogram"]+s
               plotgraph([h],lumi,j,name)

def plotgraph(histolist,lumi,j,name=""):

    name = os.path.basename(name)

    p = plots.DataMCPlot2(histolist)
    opts = {}
    if "opts" in j:
        opts = j["opts"]
    opts2 = {}
    if "opts2" in j:
        opts2 = j["opts2"]
    opts  = str2bool(opts)
    opts2 = str2bool(opts2)

    p.createFrame(os.path.join(plotDir, name), opts=opts, opts2=opts2)
    if "xlabel" in j:
        p.getFrame().GetXaxis().SetTitle(j["xlabel"])
    if "ylabel" in j:
        p.getFrame().GetYaxis().SetTitle(j["ylabel"])
    if "drawStyle" in j:
        p.histoMgr.setHistoDrawStyleAll(j["drawStyle"])
    if "rebinx" in j:
        p.histoMgr.forEachHisto(lambda h: h.getRootHisto().RebinX(j["rebinx"]))
    if "rebiny" in j:
        p.histoMgr.forEachHisto(lambda h: h.getRootHisto().RebinY(j["rebiny"]))
    if "markerStyle" in j:
        p.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetMarkerStyle(j["markerStyle"]))
    if "markerColor" in j:
        p.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetMarkerColor(j["markerColor"]))
    if "markerSize" in j:
        p.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetMarkerSize(j["markerSize"]))

    p.draw()

    histograms.addStandardTexts(lumi=lumi)

    if not os.path.exists(plotDir):
        os.mkdir(plotDir)
    p.save(formats)
    print "Saved plot",os.path.join(plotDir, name)






def main():

    resultdir = os.getcwd()
    jsonfiles = []
    for arg in sys.argv[1:]:
        if not os.path.exists(arg):
            continue
        if os.path.isdir(arg):
            resultdir = arg
            continue
        with open(os.path.abspath(arg)) as jsonfile:
            try:
                json.load(jsonfile)
                jsonfiles.append(arg)
            except ValueError, e:
                print "Problem loading json file",arg,", please check the file"
                sys.exit()

    if len(jsonfiles) == 0:
        usage()

    for j in jsonfiles:
        plot(resultdir,j)

if __name__ == "__main__":
    main()
