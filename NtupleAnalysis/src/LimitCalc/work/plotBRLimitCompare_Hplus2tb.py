#!/usr/bin/env python
'''
DESCRIPTION:
Script for comparing exlusion limits from same channel but different cuts or measurements, 
or even for comparing exclusion limits of different channels.


USAGE:
cd HiggsAnalysis/NtupleAnalysis/src/LimitCalc/work
plotBRLimitCompare_Hplus2tb.py 


EXAMPLES:
./plotBRLimitCompare_Hplus2tb.py  [opts]
./plotBRLimitCompare_Hplus2tb.py --url --logY --gridX --gridY --cutLine 500 --yMin 0.01
./plotBRLimitCompare_Hplus2tb.py --url --logY --gridX --gridY --cutLine 500 --yMin 0.01 --name h2tb
./plotBRLimitCompare_Hplus2tb.py --url --logY --gridX --gridY --cutLine 500 --yMin 0.3 --yMax 10 --name h2tb 
./plotBRLimitCompare_Hplus2tb.py --logY --gridX --gridY --relative --cutLine 500 --cutLineY 1
./plotBRLimitCompare_Hplus2tb.py --logY --gridX --gridY --relative --url
./plotBRLimitCompare_Hplus2tb.py --logY --gridX --gridY --relative --url --yMax 10

LAST USED:
./plotBRLimitCompare_Hplus2tb.py --logY --gridX --gridY --relative --url --xMax 1000

'''
#================================================================================================
# Import modules
#================================================================================================
import os
import getpass
import sys
import glob
import json
import array
import copy
from optparse import OptionParser

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.styles as styles
import HiggsAnalysis.LimitCalc.limit as limit
import HiggsAnalysis.NtupleAnalysis.tools.ShellStyles as ShellStyles

#================================================================================================
# Global definitions
#================================================================================================
xPos      = 0.53
xPosLeg   = xPos
xPosText  = xPos
styleList = [styles.Style(24, ROOT.kBlack)] + styles.getStyles()


#================================================================================================
# Function definition
#================================================================================================
def Verbose(msg, printHeader=False):
    '''
    Calls Print() only if verbose options is set to true.
    '''
    if not opts.verbose:
        return
    Print(msg, printHeader)
    return

def Print(msg, printHeader=True):
    '''
    Simple print function. If verbose option is enabled prints, otherwise does nothing.
    '''
    fName = __file__.split("/")[-1]
    if printHeader:
        print "=== ", fName
    print "\t", msg
    return

def main():

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    style.setGridX(opts.gridX)
    style.setGridY(opts.gridY)
    # style.setGridX(opts.logX)
    # style.setGridY(opts.logY)

    # Set text mode
    histograms.cmsTextMode = histograms.CMSMode.PRELIMINARY
    # histograms.cmsTextMode = histograms.CMSMode.NONE

    # Definitions
    savePath = opts.saveDir
    if opts.url:
        savePath = opts.saveDir.replace("/afs/cern.ch/user/a/attikis/public/html", "https://cmsdoc.cern.ch/~%s" % getpass.getuser())

    # Do the Resolved H->tb fully hadronic final state comparison
    if 1:
        opts.name = "stat"
        # myList1   = GetHexoListStat19Mar2018()
        myList1   = GetStatOnlyListMar2018()
        doCompare(opts.name, myList1)

    if 0:
        opts.name = "syst"
        myList1   = GetHexoListSyst19Mar2018()
        doCompare(opts.name, myList1)

    # Do all H->tb fully hadronic final states comparison
    if 0:
        opts.name = "all"
        myList2   = GetAllFinalStatesList()
        myList2.extend(GetHexoListStat19Mar2018())
        doCompare(opts.name, myList2)

    # Inform user and exit
    Print("All plots saved under directory %s" % (ShellStyles.NoteStyle() + savePath + ShellStyles.NormalStyle()), True)    
    return

def GetBoostedStatOnly():
    myList = [
        # Other final states
        ("H^{+}#rightarrow tb (boosted, 19-Dec-17)" , "limits2018/datacards_combine_MIT_approximate_19Dec2017/CombineResults_taujets_*"),
        ("H^{+}#rightarrow tb (boosted, 19-Mar-18)" , "limits2018/datacards_combine_MIT_approximate_19Mar2018/CombineResults_taujets_*"),
        ]
    return myList

def GetStatOnlyListMar2018():
    myDirs = {}
    myDirs["b3Pt30_MVAm0p40to0p40_QGLR0p5_NoFatJetVeto_StatOnly"]  = "mH180to1000_b3Pt30_MVAm0p40to0p40_QGLRGE0p5_NoFatJetVeto_StatOnly_180321_133930/"
    myDirs["b3Pt30_MVAm0p40to0p40_NoFatJetVeto_StatOnly"]  = "mH180to1000_b3Pt30_MVAm0p40to0p40_NoFatJetVeto_StatOnly_180320_130704/"
    myDirs["b3Pt30_MVA0p00to0p60_NoFatJetVeto_StatOnly"]   = "mH180to1000_b3Pt30_MVA0p00to0p60_NoFatJetVeto_StatOnly_180321_103154/"
    myDirs["b3Pt30_MVA0p50to0p80_NoFatJetVeto_StatOnly"]   = "mH180to1000_b3Pt30_MVA0p50to0p80_StatOnly_180321_103541/"
    myDirs["b3Pt40_MVA0p40_NoFatJetVeto_StatOnly"]         = "mH180to3000_b3Pt40_MVA0p40_NoFatJetVeto_StatOnly_180319_051408/"
    myDirs["b3Pt40_MVA0p40_FatJetVeto450_StatOnly"]        = "mH180to3000_b3Pt40_MVA0p40_FatJetVeto450_StatOnly_180319_052727/"
    myDirs["b3Pt40_MVA0p40_FatJetVeto500_StatOnly"]        = "mH180to3000_b3Pt40_MVA0p40_FatJetVeto500_StatOnly_180319_052958/"
    for k in myDirs:
        myDirs[k] = "limits2018/datacards_Hplus2tb_13TeV_EraRun2016_Search80to1000_OptNominal_limits2016_DataDriven_" + myDirs[k]

    myList = [
        # Kolosova
        ("b30, BDT > 0.40 (QGLR #geq 0.5)", myDirs["b3Pt30_MVAm0p40to0p40_QGLR0p5_NoFatJetVeto_StatOnly"] + "CombineResults*"),
        ("b30, BDT > 0.40", myDirs["b3Pt30_MVAm0p40to0p40_NoFatJetVeto_StatOnly"] + "CombineResults*"),
        ("b30, BDT > 0.60", myDirs["b3Pt30_MVA0p00to0p60_NoFatJetVeto_StatOnly"] + "CombineResults*"),
        ("b30, BDT > 0.80", myDirs["b3Pt30_MVA0p50to0p80_NoFatJetVeto_StatOnly"] + "CombineResults*"),
        #
        ("BDT > 0.40", myDirs["b3Pt40_MVA0p40_NoFatJetVeto_StatOnly"] + "CombineResults*"),
        #("BDT > 0.40 (Fatjet < 450 GeV)", myDirs["b3Pt40_MVA0p40_FatJetVeto450_StatOnly"] + "CombineResults*"),
        #("BDT > 0.40 (Fatjet < 500 GeV)", myDirs["b3Pt40_MVA0p40_FatJetVeto500_StatOnly"] + "CombineResults*"),
        ]
    myList.extend(GetBoostedStatOnly())
    return myList


def GetHexoListStat19Mar2018():
    '''
    3 bjets 40, 40, 40
    BDT >= 0.40
    '''
    myDirs = {}
    myDirs["b3Pt40_MVA0p40_NoFatJetVeto_StatOnly"]  = "b3Pt40_MVA0p40_NoFatJetVeto_StatOnly_180319_051408/"
    myDirs["b3Pt40_MVA0p40_NoFatJetVeto"]           = "b3Pt40_MVA0p40_NoFatJetVeto_180319_052022/"
    myDirs["b3Pt40_MVA0p40_FatJetVeto450_StatOnly"] = "b3Pt40_MVA0p40_FatJetVeto450_StatOnly_180319_052727/"
    myDirs["b3Pt40_MVA0p40_FatJetVeto450"]          = "b3Pt40_MVA0p40_FatJetVeto450_180319_052456/"
    myDirs["b3Pt40_MVA0p40_FatJetVeto500_StatOnly"] = "b3Pt40_MVA0p40_FatJetVeto500_StatOnly_180319_052958/"
    myDirs["b3Pt40_MVA0p40_FatJetVeto500"]          = "b3Pt40_MVA0p40_FatJetVeto500_180319_053111/"
    for k in myDirs:
        myDirs[k] = "limits2018/datacards_Hplus2tb_13TeV_EraRun2016_Search80to1000_OptNominal_limits2016_DataDriven_mH180to3000_" + myDirs[k]

    myList = [
        ("BDT > 0.40", myDirs["b3Pt40_MVA0p40_NoFatJetVeto_StatOnly"] + "CombineResults*"),
        #("BDT > 0.40 (Syst.)", myDirs["b3Pt40_MVA0p40_NoFatJetVeto"] + "CombineResults*"),
        ("BDT > 0.40 (Fatjet < 450 GeV)", myDirs["b3Pt40_MVA0p40_FatJetVeto450_StatOnly"] + "CombineResults*"),
        #("BDT > 0.40 (Syst., Fatjet > 450 GeV)", myDirs["b3Pt40_MVA0p40_FatJetVeto450"] + "CombineResults*"),
        ("BDT > 0.40 (Fatjet < 500 GeV)", myDirs["b3Pt40_MVA0p40_FatJetVeto500_StatOnly"] + "CombineResults*"),
        #("BDT > 0.40 (Syst., Fatjet < 500 GeV)", myDirs["b3Pt40_MVA0p40_FatJetVeto500"] + "CombineResults*"),
        #("H^{+}#rightarrow tb (~boosted)"     , "limits2017/*datacards_combine_MIT_approximate/CombineResults_taujets_*"),
        ]
    return myList

def GetHexoListSyst19Mar2018():
    '''
    3 bjets 40, 40, 40
    BDT >= 0.40
    '''
    myDirs = {}
    myDirs["b3Pt40_MVA0p40_NoFatJetVeto_StatOnly"]  = "b3Pt40_MVA0p40_NoFatJetVeto_StatOnly_180319_051408/"
    myDirs["b3Pt40_MVA0p40_NoFatJetVeto"]           = "b3Pt40_MVA0p40_NoFatJetVeto_180319_052022/"
    myDirs["b3Pt40_MVA0p40_FatJetVeto450_StatOnly"] = "b3Pt40_MVA0p40_FatJetVeto450_StatOnly_180319_052727/"
    myDirs["b3Pt40_MVA0p40_FatJetVeto450"]          = "b3Pt40_MVA0p40_FatJetVeto450_180319_052456/"
    myDirs["b3Pt40_MVA0p40_FatJetVeto500_StatOnly"] = "b3Pt40_MVA0p40_FatJetVeto500_StatOnly_180319_052958/"
    myDirs["b3Pt40_MVA0p40_FatJetVeto500"]          = "b3Pt40_MVA0p40_FatJetVeto500_180319_053111/"
    for k in myDirs:
        myDirs[k] = "limits2018/datacards_Hplus2tb_13TeV_EraRun2016_Search80to1000_OptNominal_limits2016_DataDriven_mH180to3000_" + myDirs[k]
    myDirs["b3Pt40T_MVA0p50_NoFatJetVeto"]          = "limits2018/datacards_Hplus2tb_13TeV_EraRun2016_Search80to1000_OptNominal_limits2016_DataDriven_mH180to3000_180321_101617/"

    # Stat. #oplus Syst.
    myList = [
        #("BDT > 0.40", myDirs["b3Pt40_MVA0p40_NoFatJetVeto_StatOnly"] + "CombineResults*"),
        ("BDT > 0.50 (CSVv2-Tight, Syst.)", myDirs["b3Pt40T_MVA0p50_NoFatJetVeto"] + "CombineResults*"),
        #("BDT > 0.40", myDirs["b3Pt40_MVA0p40_NoFatJetVeto_StatOnly"] + "CombineResults*"),
        ("BDT > 0.40 (Syst.)", myDirs["b3Pt40_MVA0p40_NoFatJetVeto"] + "CombineResults*"),
        #("BDT > 0.40 (Fatjet < 450 GeV)", myDirs["b3Pt40_MVA0p40_FatJetVeto450_StatOnly"] + "CombineResults*"),
        ("BDT > 0.40 (Syst., Fatjet < 450 GeV)", myDirs["b3Pt40_MVA0p40_FatJetVeto450"] + "CombineResults*"),
        #("BDT > 0.40 (Fatjet < 500 GeV)", myDirs["b3Pt40_MVA0p40_FatJetVeto500_StatOnly"] + "CombineResults*"),
        ("BDT > 0.40 (Syst., Fatjet < 500 GeV)", myDirs["b3Pt40_MVA0p40_FatJetVeto500"] + "CombineResults*"),
        #
        #("H^{+}#rightarrow tb (~boosted)"     , "limits2017/*datacards_combine_MIT_approximate/CombineResults_taujets_*"),
        ]
    return myList


def _ifNotNone(value, default):
    if value is None:
        return default
    return value

def doCompare(name, compareList, **kwargs):
    # Define lists
    legendLabels = []
    limits       = []

    # For-loop: All label-path pairs
    for label, path in compareList:
        legendLabels.append(label)
        dirs = glob.glob(path)
        dirs.sort()

        if len(dirs) == 0:
            raise Exception("No directories for pattern '%s'" % path)
        directory = dirs[-1]
        
        Verbose("Picked %s" % directory, True)
        limits.append(limit.BRLimits(directory, excludeMassPoints=["155"]))

    # ================================================================================================================
    # Do the sigma bands
    # ================================================================================================================
    Verbose("Creating the sigma-bands plots", True)
    _opts = copy.deepcopy(opts)
    doPlotSigmaBands(limits, legendLabels, opts.name + "_sigmaBands", _opts)

    # ================================================================================================================
    # Do expected
    # ================================================================================================================
    Verbose("Creating the expected plots", True)
    observedList = [l.observedGraph() for l in limits]
    expectedList = [l.expectedGraph() for l in limits]

    # 1) Expected: Median +/- 1,2 sigma
    doPlot(limits, legendLabels, expectedList, opts.name + "_median", limit.BRlimit, _opts, yTitle="Expected Sigma Bands")

    # 2) Expected: +/- 1 sigma
    list1 = [l.expectedGraph(sigma=+1) for l in limits]
    list2 = [l.expectedGraph(sigma=-1) for l in limits]
    exp1sigmaList = list1 + list2
    legendLabels2 = legendLabels + [None]*len(legendLabels)
    doPlot(limits, legendLabels2, exp1sigmaList, opts.name + "_sigma1", "Expected #pm1#sigma", _opts, yTitle="Expected #pm1sigma")

    # 3) Expected: +/- 2 sigma
    list1 = [l.expectedGraph(sigma=+2) for l in limits]
    list2 = [l.expectedGraph(sigma=-2) for l in limits]
    exp2sigmaList = list1 + list2
    doPlot(limits, legendLabels2, exp2sigmaList, opts.name + "_sigma2", "Expected #pm2#sigma", _opts, yTitle="Expected #pm2sigma")

    # ================================================================================================================
    # Do the observed plots
    # ================================================================================================================
    Verbose("Creating the observed plots", True)
    if opts.unblinded:
        doPlot(limits, legendLabels, observedList, opts.name, limit.BRlimit, _opts, yTitle="Observed")

    # ================================================================================================================
    # Do the relative plots
    # ================================================================================================================
    Verbose("Creating the relative plots", True)
    if not opts.relative:
        return
    # Overwrite some settings
    _opts.yMin    = +0.5 #0.0
    _opts.yMax    = -1.0 #2.5
    _opts.logY    = False

    # 1) Relative: median
    relLimits    = GetRelativeLimits(limits)
    expectedList = [l.expectedGraph() for l in relLimits]
    doPlot(relLimits, legendLabels, expectedList, opts.name + "_medianRelative", opts.relativeYlabel, _opts, yTitle="Expected median")

    # 2) Relative: (expected 1 sigma) / (median)
    list1 = [limit.divideGraph(l.expectedGraph(sigma=+1), l.expectedGraph()) for l in limits]
    list2 = [limit.divideGraph(l.expectedGraph(sigma=-1), l.expectedGraph()) for l in limits]
    sigma1List = list1 + list2
    doPlot(limits, legendLabels2, sigma1List, opts.name + "_sigma1Relative", "Expected #pm1#sigma / median", _opts, yTitle="Expected #pm1#sigma / median")

    # 3) Relative: (expected 2 sigma) / (median)
    list1 = [limit.divideGraph(l.expectedGraph(sigma=+2), l.expectedGraph()) for l in limits]
    list2 = [limit.divideGraph(l.expectedGraph(sigma=-2), l.expectedGraph()) for l in limits]
    sigma2List = list1 + list2
    doPlot(limits, legendLabels2, sigma2List, opts.name + "_sigma2Relative", "Expected #pm2#sigma / median", _opts, yTitle="Expected #pm2#sigma / median")
    return

def doPlot(limits, legendLabels, graphs, name, ylabel, _opts={}, yTitle=None):
    
    # Definitions
    hg = []
    ll = {}
    nGraphs = len(graphs)

    # For-loop: All HistoGraphs
    for i in xrange(nGraphs):
        hg.append(histograms.HistoGraph(graphs[i], "Graph%d"%i, drawStyle="PL", legendStyle="lp"))
        ll["Graph%d" % (i) ] = legendLabels[i]

    # Create a plot-base object
    plot = plots.PlotBase(hg)
    plot.histoMgr.forEachHisto(styles.Generator(styleList[0:len(limits)]))
    def sty(h):
        r = h.getRootHisto()
        r.SetLineWidth(3)
        r.SetLineStyle(ROOT.kSolid)
        return

    # Apply style and set label
    plot.histoMgr.forEachHisto(sty)
    plot.histoMgr.setHistoLegendLabelMany(ll)

    # Create & set legend
    nGraphs = len(graphs)
    # If sigma bands are drawn each legend entry is plotted twice. Correct this in the count
    if "Sigma1" in name or "Sigma2" in name:
        nGraphs = nGraphs/2.0
    #legend = getLegend(nGraphs, limit, xPosLeg)
    legend = getLegend(nGraphs, limit, 0.35) #iro
    plot.setLegend(legend)

    # Determine save name, minimum and maximum of y-axis
    ymin, ymax, saveName = getYMinMaxAndName(limits, name)
    if _opts.yMin == -1:
        _opts.yMin = ymin
    if _opts.yMax == -1:
        _opts.yMax = ymax

    # Create the frame and set axes titles
    if _opts.xMax != -1:
        plot.createFrame(saveName, opts={"xmax": _opts.xMax, "ymin": _opts.yMin, "ymax": _opts.yMax})
        if _opts.xMin != -1:
            plot.createFrame(saveName, opts={"xmin": _opts.xMin, "xmax": _opts.xMax, "ymin": _opts.yMin, "ymax": _opts.yMax})
    else:
        plot.createFrame(saveName, opts={"ymin": _opts.yMin, "ymax": _opts.yMax})
    
    # Add cut line?
    if opts.cutLine != 999.9:
        kwargs = {"greaterThan": True}
        plot.addCutBoxAndLine(cutValue=_opts.cutLine, fillColor=ROOT.kRed, box=False, line=True, **kwargs)
    if opts.cutLineY != 999.9:
        kwargs = {"greaterThan": True, "mainCanvas": True, "ratioCanvas": False}
        plot.addCutBoxAndLineY(cutValue=_opts.cutLineY, fillColor=ROOT.kRed, box=False, line=True, **kwargs)
    
    # Set axes titles
    plot.frame.GetXaxis().SetTitle(limit.mHplus())
    plot.frame.GetYaxis().SetTitle(ylabel)

    # Enable/Disable logscale for axes 
    ROOT.gPad.SetLogy(_opts.logY)
    ROOT.gPad.SetLogx(_opts.logX)

    # Draw and add text
    plot.draw()
    plot.setLuminosity(limits[0].getLuminosity())
    plot.addStandardTexts(cmsTextPosition="outframe")
    addPhysicsText(histograms, limit, x=xPosText)

    # Save plots and return
    SavePlot(plot, _opts.saveDir, saveName, [".png"])#, ".pdf"])
    return

def GetRelativeLimits(limits):
    
    # Create relative limits by copying limits
    relLimits  = copy.deepcopy(limits)
    massPoints = len(relLimits[0].expectedMedian)

    # For-loop: All limits
    for i in range(1, len(relLimits) ):
        relLimits[i].divideByLimit(relLimits[0])
        
    # For-loop: All mass points 
    for j in range(0, massPoints):
        relLimits[0].expectedMedian[j] = 1.0
        relLimits[0].expectedMinus2[j] = 1.0
        relLimits[0].expectedMinus1[j] = 1.0
        relLimits[0].expectedPlus2[j]  = 1.0
        relLimits[0].expectedPlus1[j]  = 1.0
        relLimits[0].observed[j]       = 1.0
    return relLimits

        
def addPhysicsText(histograms, limit, x=0.45, y=0.84, size=20):
    '''
    Add physics-process text on canvas
    '''
    # Add process text on canvas
    histograms.addText(x, y+0.04, limit.processHeavyHtb, size=size)

    # Add final-state text
    histograms.addText(x, y, "fully hadronic final state", size=size)

    if limit.BRassumption != "":
        histograms.addText(x, y-0.05, limit.BRassumption, size=size)
    return

def getLegend(nPlots, limit, xLeg1):
    if nPlots < 3:
        nPlots = 3
    dy = (nPlots-3)*0.03
    # Create customised legend
    xLeg2 = 0.93
    yLeg1 = 0.66 - dy
    yLeg2 = 0.82

    # Adjust legend slightly to visually align with text
    legend = histograms.createLegend(xLeg1*.98, yLeg1, xLeg2, yLeg2)
    legend.SetMargin(0.17)

    # Make room for the final state text
    if 0: #opts.excludedArea:
        legend.SetFillStyle(1001)
    return legend

def doPlotSigmaBands(limits, legendLabels, saveName, _opts={}):

    # Define graphs to be used
    graphs = [
        histograms.HistoGraph(limits[0].expectedGraph(), "Expected", drawStyle="L"),
        histograms.HistoGraph(limits[0].expectedBandGraph(sigma=1), "Expected1", drawStyle="F", legendStyle="fl"),
        histograms.HistoGraph(limits[0].expectedBandGraph(sigma=2), "Expected2", drawStyle="F", legendStyle="fl"),
        ]

    # Set line style
    graphs[0].getRootHisto().SetLineStyle(ROOT.kSolid)

    # Create plot base object
    plot = plots.PlotBase(graphs)
    ll = {
        "Expected": None,
        "Expected1": "%s #pm 1#sigma" % legendLabels[0],
        "Expected2": "%s #pm 2#sigma" % legendLabels[0],
        #"Expected1": "%s exp. median #pm 1#sigma" % legendLabels[0],
        #"Expected2": "%s exp. median #pm 2#sigma" % legendLabels[0],
        }

    stGen   = styles.generator()
    nLimits = len(limits)

    # For-loop: All limits
    for i in xrange(1, nLimits):
        name = "Exp%d" % i
        gr   = histograms.HistoGraph(limits[i].expectedGraph(), name, drawStyle="L")
        stGen(gr)
        gr.getRootHisto().SetLineWidth(3)
        gr.getRootHisto().SetLineStyle(1)
        plot.histoMgr.insertHisto(len(plot.histoMgr)-2, gr, legendIndex=len(plot.histoMgr))
        ll[name] = "%s" % legendLabels[i]  # "%s exp. median" % legendLabels[i]

    # Set histo labels
    plot.histoMgr.setHistoLegendLabelMany(ll)

    # Create & set legend
    nGraphs = len(graphs)

    # If sigma bands are drawn each legend entry is plotted twice. Correct this in the count
    if "Sigma1" in name or "Sigma2" in name:
        nGraphs = nGraphs/2.0
    legend = getLegend(nGraphs+4, limit, xPosLeg)
    plot.setLegend(legend)

    # Determine save name, minimum and maximum of y-axis
    ymin, ymax, saveName = getYMinMaxAndName(limits, saveName)
    if _opts.yMin == -1:
        _opts.yMin = ymin
    if _opts.yMax == -1:
        _opts.yMax = ymax

    # Create the frame and set axes titles
    plot.createFrame(saveName, opts={"ymin": _opts.yMin, "ymax": _opts.yMax})

    # Add cut line?
    if _opts.cutLine != 999.9:
        kwargs = {"greaterThan": True}
        plot.addCutBoxAndLine(cutValue=_opts.cutLine, fillColor=ROOT.kRed, box=False, line=True, **kwargs)
    if opts.cutLineY != 999.9:
        kwargs = {"greaterThan": True, "mainCanvas": True, "ratioCanvas": False}
        plot.addCutBoxAndLineY(cutValue=_opts.cutLineY, fillColor=ROOT.kRed, box=False, line=True, **kwargs)

    # Set axes titles
    plot.frame.GetXaxis().SetTitle(limit.mHplus())
    plot.frame.GetYaxis().SetTitle(limit.BRlimit)

    # Enable/Disable logscale for axes 
    ROOT.gPad.SetLogy(_opts.logY)
    ROOT.gPad.SetLogx(_opts.logX)

    # Draw the plot with standard texts
    plot.draw()
    plot.addStandardTexts(cmsTextPosition="outframe")
    plot.setLuminosity(limits[0].getLuminosity())
    addPhysicsText(histograms, limit, x=xPosText)

    # Save the plots & return
    SavePlot(plot, _opts.saveDir, saveName, [".png"])#, ".pdf"])
    return

def getYMinMaxAndName(limits, name, minIsMedian=False):
    ymin = 1e6
    ymax = -1e6

    # For-loop: all limits
    for l in limits:
        if minIsMedian:
            _ymin = l.getYMinMedian()
        else:
            _ymin = l.getYMin()
        _ymax = l.getYMax()
        if _ymin < ymin:
            ymin = _ymin
        if _ymax > ymax:
            ymax = _ymax
        
    if opts.logY: #fixme
        name += "_logY"
        ymax *= 2
    else:
        ymin =  0.0
        ymax *= 1.2

    if opts.logX: #fixme
        name += "_logX"
    return ymin, ymax, name

def SavePlot(plot, saveDir, plotName, saveFormats = [".png", ".pdf"]):
    # Check that path exists
    if not os.path.exists(saveDir):#fixme
        os.makedirs(saveDir)

    # Create the name under which plot will be saved
    saveName = os.path.join(saveDir, plotName.replace("/", "_"))#fixme

    # For-loop: All save formats
    for i, ext in enumerate(saveFormats, 1):
        saveNameURL = saveName + ext
        saveNameURL = saveNameURL.replace("/afs/cern.ch/user/a/attikis/public/html", "https://cmsdoc.cern.ch/~%s" % getpass.getuser())
        if opts.url:
            Verbose(saveNameURL, i==1)
        else:
            Verbose(saveName + ext, i==1)
        plot.saveAs(saveName, formats=saveFormats)
    return


if __name__ == "__main__":

    # Default options
    SAVEDIR     = "/afs/cern.ch/user/%s/%s/public/html/Combine" % (getpass.getuser()[0], getpass.getuser())
    URL         = False
    LOGX        = False
    LOGY        = False
    GRIDX       = False
    GRIDY       = False
    MINX        = -1
    MAXX        = -1
    MINY        = -1
    MAXY        = -1
    CUTLINE     = 999.9
    CUTLINEY    = 999.9
    RELATIVE    = False
    RELPAIRS    = False
    VERBOSE     = False
    UNBLINDED   = False
    NAME        = "limitsBr"

    parser = OptionParser(usage="Usage: %prog [options]", add_help_option=True, conflict_handler="resolve")

    parser.add_option("-v", "--verbose", dest="verbose", default=VERBOSE, action="store_true",
                      help="Verbose mode for debugging purposes [default: %s]" % (VERBOSE) )
    
    parser.add_option("--unblinded", dest="unblinded", default=UNBLINDED, action="store_true",
                      help="Enable unblined mode and thus also produced observed limits [default: %s]" % (UNBLINDED) )

    parser.add_option("--relative", dest="relative", action="store_true", default=RELATIVE, 
                      help="Do comparison relative to the first item [default: %s]" % (RELATIVE) )

    parser.add_option("--relativePairs", dest="relativePairs", action="store_true", default=RELPAIRS, 
                      help="Do multiple relative comparisons. The list of input directories is halved, the first half is the denominator and the second half is the numerator [default: %s]" % (RELPAIRS) )

    parser.add_option("--name", dest="name", type="string", default=NAME,
                      help="Name of the output plot [default = %s]" % (NAME))

    parser.add_option("--relativeYmax", dest="relativeYmax", type="float", default=None, 
                      help="Maximum y-value for relative plots")
    
    parser.add_option("--relativeYlabel", dest="relativeYlabel", default="Expected limit vs. nominal", 
                      help="Y-axis title for relative plots")

    parser.add_option("--url", dest="url", action="store_true", default=URL,
                      help="Don't print the actual save path the plots are saved, but print the URL instead [default: %s]" % URL)

    parser.add_option("--saveDir", dest="saveDir", type="string", default=SAVEDIR,
                      help="Directory where all plots will be saved [default: %s]" % SAVEDIR)

    parser.add_option("--logX", dest="logX", action="store_true", default=LOGX,
                      help="Plot x-axis (mass) as logarithmic [default: %s]" % (LOGX) )
    
    parser.add_option("--logY", dest="logY", action="store_true", default=LOGY,
                      help="Plot y-axis (exlusion limit) as logarithmic [default: %s]" % (LOGY) )
    
    parser.add_option("--gridX", dest="gridX", default=GRIDX, action="store_true",
                      help="Enable the grid for the x-axis [default: %s]" % (GRIDX) )

    parser.add_option("--gridY", dest="gridY", default=GRIDY, action="store_true",
                      help="Enable the grid for the y-axis [default: %s]" % (GRIDY) )

    parser.add_option("--yMin", dest="yMin", default=MINY, type="float",
                      help="Overwrite automaticly calculated minimum value of y-axis [default: %s]" % (MINY) )
    
    parser.add_option("--yMax", dest="yMax", default=MAXY, type="float",
                      help="Overwrite automaticly calculated maximum value of y-axis [default: %s]" % (MAXY) )

    parser.add_option("--xMin", dest="xMin", default=MINX, type="float",
                      help="Overwrite minimum value of x-axis [default: %s]" % (MINX) )
    
    parser.add_option("--xMax", dest="xMax", default=MAXX, type="float",
                      help="Overwrite maximum value of x-axis [default: %s]" % (MAXX) )

    parser.add_option("--cutLine", dest="cutLine", type="float", default=CUTLINE,
                      help="Add TLine on the x-axis at this value  [default: %s]" % (CUTLINE) )

    parser.add_option("--cutLineY", dest="cutLineY", type="float", default=CUTLINEY,
                      help="Add TLine on the y-axis at this value  [default: %s]" % (CUTLINEY) )

    (opts, args) = parser.parse_args()

    # Save in current working directory?
    if opts.saveDir =="":
        opts.saveDir = os.getcwd()

    main()
