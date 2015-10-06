#!/usr/bin/env python

import os
import re
import glob

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import LimitCalc.limit as limit

name_re = re.compile("plot_m(?P<mass>\d+)_(?P<name>[^.]+)\.root")

def main():
    # Apply TDR style
    style = tdrstyle.TDRStyle()

    files = glob.glob("plot_m*.root")
    for f in files:
        doPlot(f)
#        break


def doPlot(rootfile):
    f = ROOT.TFile.Open(rootfile)
    basename = rootfile.replace(".root", "")
    match = name_re.search(rootfile)
    if not match:
        raise Exception("Assert: the file name regex did not match")
    mass = match.group("mass")
    name = match.group("name")

    canvas = f.Get("c1")

    primitives = canvas.GetListOfPrimitives()
    # Suppress the warning message of missing dictionary for some iterator
    backup = ROOT.gErrorIgnoreLevel
    ROOT.gErrorIgnoreLevel = ROOT.kError
    primiter = primitives.MakeIterator()
    ROOT.gErrorIgnoreLevel = backup

    graph = None
    expoFit = None
    lines = []

    obj = primiter.Next()
    while obj:
#        print obj, obj.GetName()
        if isinstance(obj, ROOT.TGraph):
            if graph != None:
                raise Exception("Assert: graph was already found")
            graph = obj
        elif isinstance(obj, ROOT.TF1):
            if expoFit != None:
                raise Exception("Assert: expoFit was already found")
            expoFit = obj
        elif isinstance(obj, ROOT.TLine):
            lines.append(obj)

        obj = primiter.Next()

    if graph == None:
        raise Exception("Assert: did not find any TGraph")
    if expoFit == None:
        raise Exception("Assert: did not find any TF1")

    plot = plots.PlotBase([
            histograms.HistoGraph(graph, "CLs", drawStyle="PE")
            ])
    plot.createFrame(basename, opts={"xmin": 0, "ymin": 0, "ymaxfactor": 1.1,
                                     "xmaxlist": [0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.15, 0.2]
                                     })
    plot.frame.GetXaxis().SetTitle("#mu")
    plot.frame.GetXaxis().SetNdivisions(1005)
    plot.frame.GetYaxis().SetTitle("CL_{s}")

    expoFit.SetLineColor(ROOT.kBlue-9)
    # skip the vertical non-solid lines
    lines = filter(lambda l: l.GetLineStyle() == 1 or l.GetX1() != l.GetX2(), lines)

    plot.prependPlotObject(expoFit)
    for l in lines:
        plot.appendPlotObject(l)

    plot.draw()

    labelName = {"observed": "Observed",
                 "median": "Expected median",
                 "1sigma": "Expected +1#sigma",
                 "2sigma": "Expected +2#sigma",
                 "-1sigma": "Expected .1#sigma",
                 "-2sigma": "Expected -2#sigma"}[name]

    size = 20
    x = 0.62
    histograms.addText(x, 0.85, "m_{H^{+}} = %s %s" % (mass, limit.massUnit()), size=size)
    histograms.addText(x, 0.81, labelName, size=size)

    plot.save()

    f.Close()
    f.Delete()


if __name__ == "__main__":
    main()
