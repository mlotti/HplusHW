#!/usr/bin/env python

import os
import sys
import glob
from optparse import OptionParser

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles

import ROOT

def readDatasetDirs(opts, crossSections, datasets):
    taskdirs = multicrab.getTaskDirectories(opts)
    for d in taskdirs:
        files = glob.glob(os.path.join(d, "res", opts.input))
        if len(files) > 1:
            raise Exception("Only one file should match the input (%d matched) for task %s" % (len(files), d))
            return 1
        elif len(files) == 0:
            raise Exception("No files matched to input for task %s" % d)

        datasets.append(counter.readDataset(files[0], opts.counterdir, d, crossSections))

def printList(dataset, dir):
    f = dataset.getTFile()
    directory = None
    if dir == ".":
        directory = f
    else:
        directory = f.Get(dir)

    dirlist = directory.GetListOfKeys()
    diriter = dirlist.MakeIterator()
    key = diriter.Next()

    print "List of directory "+dir
    while key:
        print " ", key.GetName()
        key = diriter.Next()

def drawSavePlot(opts, datasets, plot):
    c = ROOT.TCanvas(plot.replace("/", "_"), "title")

    histos = [d.getTFile().Get(plot) for d in datasets]

    scale = False
    if opts.mode in ["xsect", "xsection", "crosssection", "crossSection"]:
        scale = True

        for i, h in enumerate(histos):
            h.Sumw2() # freeze errors
            h.Scale(datasets[i].getNormFactor())

    ymin = min([h.GetMinimum() for h in histos])
    ymax = max([h.GetMaximum() for h in histos])
    ymax = 1.1*ymax

    xmin = min([h.GetXaxis().GetBinLowEdge(h.GetXaxis().GetFirst()) for h in histos])
    xmax = max([h.GetXaxis().GetBinUpEdge(h.GetXaxis().GetLast()) for h in histos])

    frame = c.DrawFrame(xmin, ymin, xmax, ymax)

    if scale:
        frame.GetYaxis().SetTitle("Cross-section (pb)")
    else:
        frame.GetYaxis().SetTitle("MC Events")

    legendymin = 0.89 - 0.03*len(histos)
    legend = ROOT.TLegend(0.69, legendymin, 0.94, 0.94)
    legend.SetFillColor(ROOT.kWhite)
    legend.SetBorderSize(1)

    for i, h in enumerate(histos):
        styles.applyStyle(h, i)
        legend.AddEntry(h, datasets[i].getName(), "l")

    # Draw the histograms such that the first one is on the top
    histos.reverse()
    for h in histos:
        h.Draw("HIST same")

    legend.Draw()

    for fmt in opts.formats:
        c.SaveAs(fmt)

def main(opts):
    ROOT.gROOT.SetBatch(True)
    
    crossSections = {}
    for o in opts.xsections:
        (name, value) = o.split(":")
        crossSections[name] = float(value)
    
    style = tdrstyle.TDRStyle()

    datasets = []
    if len(opts.files) > 0:
        for f in opts.files:
            datasets.append(counter.readDataset(f, opts.counterdir, f, crossSections))
    else:
        readDatasetDirs(opts, crossSections, datasets)

    if len(datasets) == 0:
        return

    if len(opts.list) > 0:
        printList(datasets[0], opts.list)

    for plot in opts.plots:
        drawSavePlot(opts, datasets, plot)    

    return 0

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]")
    multicrab.addOptions(parser)
    parser.add_option("-i", dest="input", type="string", default="histograms-*.root",
                      help="Pattern for input root files (note: remember to escape * and ? !) (default: 'histograms-*.root')")
    parser.add_option("-f", dest="files", type="string", action="append", default=[],
                      help="Give input ROOT files explicitly, if these are given, multicrab.cfg is not read and -d/-i parameters are ignored")
    parser.add_option("--mode", "-m", dest="mode", type="string", default="events",
                      help="Output mode; available: 'events', 'xsect' (default: 'events')")
    parser.add_option("--xsection", "-x", dest="xsections", type="string", action="append", default=[],
                      help="Override the cross sections in the ROOT file. 'datasetname:xsect' where xsect is the cross section in pb, e.g. 'QCD_Pt170:154'")
    parser.add_option("--counterDir", "-c", dest="counterdir", type="string", default="signalAnalysisCounters",
                      help="TDirectory name containing the counters (default: signalAnalysisCounters")
    parser.add_option("--plot", "-p", dest="plots", type="string", action="append", default=[],
                      help="Path to histogram to plot")
    parser.add_option("--list", "-l", dest="list", type="string", default="",
                      help="List the contents of a directory")
    parser.add_option("--format", dest="formats", type="string", action="append", default=[".eps", ".png"],
                      help="Output file format as understood by ROOT TCanvas::SaveAs() (default: '.eps' and '.png')")
    (opts, args) = parser.parse_args()

    sys.exit(main(opts))
