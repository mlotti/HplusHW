#!/usr/bin/env python

import sys
import re
import array
import os
import json

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.styles as styles
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.LimitCalc.limit as limit
import HiggsAnalysis.LimitCalc.BRXSDatabaseInterface as BRXSDB

tanbMax = 65

ROOT.gROOT.LoadMacro("LHCHiggsUtils.C")

db = None

def usage():
    print
    print "### Usage:  ",sys.argv[0],"<json file>"
    print
    print "Note that because of transparent colors, the output will be PDF instead of EPS, and you need recent-enough ROOT"
    print
    sys.exit()


def json2graph(jsonlimits):
    graphs = {}
    for k in jsonlimits.keys():
        if k in ["exp2","exp1","obs","exp","Allowed"]:
            points = jsonlimits[k]
            x = array.array("d")
            y = array.array("d")
            for p in points:
                x.append(float(p["x"]))
                y.append(float(p["y"]))
            graph = ROOT.TGraph(len(x),x,y)
            graphs[k] = graph
    return graphs

def xaminmax(jsonlimits):
    xmin = 999
    xmax = -999
    for k in jsonlimits.keys():
        if k in ["exp2","exp1","obs","exp","Allowed"]:
            points = jsonlimits[k]
            for p in points:
                x = float(p["x"])
                if x < xmin:
                    xmin=x
                if x > xmax:
                    xmax = x
            return xmin,xmax
    return None,None

def main():
    if len(sys.argv) == 1:
        usage()


    # Enable OpenGL
    ROOT.gEnv.SetValue("OpenGL.CanvasPreferGL", 1)

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    #if limit.forPaper:
    #    histograms.cmsTextMode = histograms.CMSMode.PAPER
    #histograms.cmsTextMode = histograms.CMSMode.PAPER # tmp
    #histograms.cmsTextMode = histograms.CMSMode.UNPUBLISHED # tmp
    histograms.cmsTextMode = histograms.CMSMode.PRELIMINARY
    limit.forPaper = True # to get GeV without c^2
                                       
        
    jsonfile = sys.argv[1]

    f = open(jsonfile, "r")
    limits = json.load(f)
    f.close()
    
    name           = str(limits["name"])
    scenario       = str(limits["scenario"])
    lumi           = float(limits["luminosity"])
    finalstateText = str(limits["finalStateText"])
    mHplus         = str(limits["mHplus"])
    graphs         = json2graph(limits)
    xmin,xmax      = xaminmax(limits)
    regime = "heavy"
    if xmax < 175:
        regime = "light"
    if xmin < 175 and xmax > 175:
        regime = "combined"
    
    limit.doTanBetaPlotGeneric(name, graphs, lumi, finalstateText, mHplus, scenario, regime=regime)

        
if __name__ == "__main__":
    main()
