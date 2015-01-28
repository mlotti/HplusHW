#!/usr/bin/env python

import os
import sys
import json
from optparse import OptionParser

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.limit as limit

def main(opts):
    style = tdrstyle.TDRStyle()

    mlfit = limit.MLFitData()
    lumi=None
    if os.path.exists("limits.json"):
        f = open("limits.json")
        data = json.load(f)
        f.close()
        lumi = float(data["luminosity"])

    doBkgFitPlots(mlfit, lumi, opts)

def doBkgFitPlots(mlfit, lumi, options):
    firstMass = mlfit.massPoints()[0]
    if opts.mass != None:
        firstMass = opts.mass
    else:
        print "Doing plot for mass point %s, to change use -m parameter"%firstMass

    def createDrawPlot(gr, labels, fname):
        plot = plots.PlotBase([histograms.HistoGraph(gr, "Fitted", drawStyle="P")])
        plot.setLuminosity(lumi)
    
        canvasOpts = {}
        if len(labels) > 15:
            canvasOpts["addHeight"] = 0.03*(len(labels)-15)
            canvasOpts["addWidth"] = 0.2

        plot.createFrame(fname, opts={"ymin": 0, "xmin": -4.2, "xmax": 2.5}, canvasOpts=canvasOpts)
        plot.getFrame().GetXaxis().SetTitle("Fitted value")

        scale = 1
        if "addHeight" in canvasOpts:
            scale = 1/(1+canvasOpts["addHeight"])
            plot.getFrame().GetXaxis().SetTickLength(plot.getFrame().GetXaxis().GetTickLength()*scale)
            plot.getPad().SetBottomMargin(plot.getPad().GetBottomMargin()*scale)
            plot.getPad().SetTopMargin(plot.getPad().GetTopMargin()*scale)
        if "addWidth" in canvasOpts:
            scale = 1/(1+canvasOpts["addWidth"])
            #plot.getFrame().GetXaxis().SetTickLength(plot.getFrame().GetXaxis().GetTickLength()*scale)
            plot.getPad().SetRightMargin(0.04)
            plot.getPad().SetLeftMargin(0.04)

        plot.getPad().SetLeftMargin(plot.getPad().GetRightMargin())
        plot.getPad().Update()
    
        ymin = plot.cf.frame.GetYaxis().GetXmin()
        ymax = plot.cf.frame.GetYaxis().GetXmax()
    
        for xval, color in [(0, ROOT.kRed), (-1, ROOT.kBlue), (1, ROOT.kBlue)]:
            l = ROOT.TLine(xval, ymin, xval, ymax)
            l.SetLineColor(color)
            l.SetLineStyle(ROOT.kDotted)
            l.SetLineWidth(2)
            plot.prependPlotObject(l)
    
        plot.cf.frame.GetYaxis().SetLabelSize(0)
    
        plot.draw()
        plot.addStandardTexts(cmsTextPosition="outframe")
    
        # Intentionally not NDC
        l = ROOT.TLatex()
        l.SetTextFont(l.GetTextFont()-20) # bold->normal
        l.SetTextSize(17)

        x_nuis = -4.0
        x_value = 1.5

        l.DrawLatex(x_nuis, ymax*0.93, "Nuisance parameter")
        l.DrawLatex(x_value, ymax*0.93, "Fitted value")

        for i, label in enumerate(labels):
            y = gr.GetY()[i]-0.3
    
            l.DrawLatex(x_nuis, y, label[:40])
            l.DrawLatex(x_value, y, "%.2f #pm %.2f" % (gr.GetX()[i], gr.GetErrorX(i)))
        
        plot.save()
    

    (gr, labels) = mlfit.fittedGraph(firstMass, backgroundOnly=options.bkgonlyfit, signalPlusBackground=options.sbfit, heavyHplusMode=options.heavyhplus)
    myPlotName = "mlfit_m%s"%firstMass
    if options.bkgonlyfit:
        myPlotName += "_bkgonlyfit"
    if options.sbfit:
        myPlotName += "_sbfit"
    if options.heavyhplus:
        myPlotName += "_heavyHpMode"
    
    createDrawPlot(gr, labels, myPlotName)

    (gr, labels, shapeStatNuisance) = mlfit.fittedGraphShapeStat(firstMass, backgroundOnly=options.bkgonlyfit, signalPlusBackground=options.sbfit)
    try:
        (gr, labels, shapeStatNuisance) = mlfit.fittedGraphShapeStat(firstMass, backgroundOnly=options.bkgonlyfit, signalPlusBackground=options.sbfit)
        createDrawPlot(gr, labels, myPlotName+"_ShapeStat")
    except Exception, e:
        print "Warning: %s" % str(e)

_datacardDirPrefix = "datacards_combine"
_limitTaskDirPrefix = "CombineMultiCrab"

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]",add_help_option=False,conflict_handler="resolve")
    parser.add_option("--bkgonlyfit", dest="bkgonlyfit", action="store_true", default=False, help="Background-only fit (default)")
    parser.add_option("--sbfit", dest="sbfit", action="store_true", default=False, help="Signal+background fit")
    parser.add_option("-m", dest="mass", action="store", default=None, help="mass point")
    parser.add_option("-r", dest="recursive", action="store_true", default=False, help="Find datacard directories recursively")
    parser.add_option("--heavy", dest="heavyhplus", action="store_true", default=False, help="Plotting for heavy H+")
    
    (opts, args) = parser.parse_args()
    if not opts.sbfit:
        opts.bkgonlyfit = True

    if opts.recursive:
        # Build list of directories
        myList = os.listdir(".")
        myFilteredList = []
        mySubCount = 0
        for l in myList:
            if l.startswith(_datacardDirPrefix):
                mySubCount += 1
                mySubList = os.listdir(l)
                for s in mySubList:
                    if s.startswith(_limitTaskDirPrefix):
                        myFilteredList.append("%s/%s"%(l,s))
        if mySubCount == 0:
            raise Exception("Could not find datacard directories in this directory!")
        if len(myFilteredList) == 0:
            raise Exception("Could not find job directories for limit calculation in the datacard directories! Did you run the limits yet?")
        for l in myFilteredList:
            print "Running ML fit on directory: %s"%l
            prevDir = os.getcwd()
            os.chdir(l)
            main(opts)
            os.chdir(prevDir)

    else:
        # Assume the script is being run in the working directory 
        main(opts)
