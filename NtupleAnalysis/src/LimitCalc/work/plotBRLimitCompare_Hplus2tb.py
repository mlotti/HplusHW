#!/usr/bin/env python
'''
DESCRIPTION:
Script for comparing exlusion limits from same channel but different cuts or measurements, or even for comparing exclusion limits of different channels.


INSTRUCTIONS:


USAGE:
cd HiggsAnalysis/NtupleAnalysis/src/LimitCalc/work
plotBRLimitCompare_Hplus2tb.py 


EXAMPLES:
./plotBRLimitCompare_Hplus2tb.py  [opts]


LAST USED:
./plotBRLimitCompare_Hplus2tb.py --url --logy --gridX --gridY --cutLine 500 --yMin 0.01
./plotBRLimitCompare_Hplus2tb.py --url --logy --gridX --gridY --cutLine 500 --yMin 0.01 --name h2tb

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
from optparse import OptionParser

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.styles as styles
import HiggsAnalysis.LimitCalc.limit as limit

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

def main(opts, args):

    # Take care of options
    if opts.name == None:
        opts.name = "limitsBr"

    if opts.saveDir =="":
        opts.saveDir = os.getcwd()

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    histograms.cmsTextMode = histograms.CMSMode.NONE
    
    # Do the plots
    compareH2tb(opts)
    return

def compareH2tb(opts):
    
    # Define list iwth label-path mappings
    myList1 = [
        ("Nominal"                    , "*datacards_default_170827_075947_noLumi/CombineResults_taujets_*"),
        ("Nominal (Lumi)"             , "*datacards_default_170827_075947/CombineResults_taujets_*"),
        ("150 < m_{t} < 210 GeV/c^{2}", "*datacards_TopMass150to210_170914_163638_noLumi/CombineResults_taujets_*"),
        ("Perfect JER (TopReco)"     , "*_LdgTetrajetMass_Run2016_80to1000_GenJets_noLumi/CombineResults_taujets_*"),
        # ("Boosted Top (Approx.)"   , "*datacards_combine_MIT_approximate/CombineResults_taujets_*"),
        # ("Single Lepton (Approx.)" , "*datacards_combine_SingleLepton_approximate/CombineResults_taujets_*"),
        ]

    myList2 = [
        ("Nominal"                    , "*datacards_default_170827_075947_noLumi/CombineResults_taujets_*"),
        ("Boosted Top (Approx.)"   , "*datacards_combine_MIT_approximate/CombineResults_taujets_*"),
        ("Single Lepton (Approx.)" , "*datacards_combine_SingleLepton_approximate/CombineResults_taujets_*"),
        ]


    # Now do the plots
    doCompare(opts.name, myList1, opts)

    opts.saveDir += "/AllFinalStates"
    opts.name = opts.name + "2"
    doCompare(opts.name, myList2, opts)
    return

def _ifNotNone(value, default):
    if value is None:
        return default
    return value

def doCompare(name, compareList, gOpts, **kwargs):
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

        Print("Picked %s" % directory, True)
        limits.append(limit.BRLimits(directory, excludeMassPoints=["155"]))

    # Do the plot
    doPlotSigmaBands(limits, legendLabels, gOpts.name)

    # Define the graph lists
    observedList = [l.observedGraph() for l in limits]
    expectedList = [l.expectedGraph() for l in limits]
    
    doPlot(limits, legendLabels, expectedList, gOpts.name + "_expectedMedian", limit.BRlimit, myOpts = gOpts, plotLabel="Expected median")
    if gOpts.unblinded:
        doPlot(limits, legendLabels, observedList, gOpts.name + "_observed", limit.BRlimit, myOpts = gOpts, plotLabel="Observed")

    if gOpts.relative:
        nLimits = len(limits)
        # For-loop: All limits
        for i in range(1, nLimits):
            limits[i].divideByLimit(limits[0])

        # Set reference values to 1
        for j in range(0, len(limits[0].expectedMedian)):
            limits[0].expectedMedian[j] = 1.0
            limits[0].expectedMinus2[j] = 1.0
            limits[0].expectedMinus1[j] = 1.0
            limits[0].expectedPlus2[j]  = 1.0
            limits[0].expectedPlus1[j]  = 1.0
            limits[0].observed[j]       = 1.0

        # Do the relative plot
        doPlot(limits, legendLabels, expectedList, gOpts.name + "_expectedMedianRelative", gOpts.relativeYlabel, myOpts = gOpts, plotLabel="Expected median")
        Print("Skipping +-1 and 2 sigma plots for --relative", True)
        sys.exit()

    if gOpts.relativePairs:
        if len(limits) % 2 != 0:
            Print("Number of limits is not even!", True)
            sys.exit(1)

        divPoint = len(limits) / 2
        denoms   = limits[:divPoint]
        numers   = limits[divPoint:]

        # For-loop: All division points
        for i in xrange(0, divPoint):
            numers[i].divideByLimit(denoms[i])
        
        expectedNumersList = [l.expectedGraph() for l in numers]
        doPlot(numers, legendLabels[:divPoint], gexpectedNumersList, gOpts.name + "_expectedMedianRelative", gOpts.relativeYlabel, plotLabel="Expected median")
        Print("Skipping +-1 and 2 sigma plots for --relativePairs", True)
        sys.exit()

    legendLabels2 = legendLabels + [None]*len(legendLabels)

    doPlot(limits, legendLabels2,
           [limit.divideGraph(l.expectedGraph(sigma=+1), l.expectedGraph()) for l in limits] +
           [limit.divideGraph(l.expectedGraph(sigma=-1), l.expectedGraph()) for l in limits],
           gOpts.name + "_expectedSigma1Relative", 
           "Expected #pm1#sigma / median", 
           myOpts = gOpts,
           plotLabel="Expected #pm1#sigma / median")

    doPlot(limits, legendLabels2,
           [limit.divideGraph(l.expectedGraph(sigma=+2), l.expectedGraph()) for l in limits] +
           [limit.divideGraph(l.expectedGraph(sigma=-2), l.expectedGraph()) for l in limits],
           gOpts.name + "_expectedSigma2Relative", 
           "Expected #pm2#sigma / median", 
           myOpts = gOpts,
           plotLabel="Expected #pm2#sigma / median")

    doPlot(limits, legendLabels2,
           [l.expectedGraph(sigma=+1) for l in limits] +
           [l.expectedGraph(sigma=-1) for l in limits],
           gOpts.name + "_expectedSigma1", "Expected #pm1#sigma", 
           myOpts = gOpts,
           plotLabel="Expexted #pm1sigma")

    doPlot(limits, legendLabels2,
           [l.expectedGraph(sigma=+2) for l in limits] +
           [l.expectedGraph(sigma=-2) for l in limits],
           gOpts.name + "_expectedSigma2", "Expected #pm2#sigma", 
           myOpts = gOpts,
           plotLabel="Expected #pm2sigma")
    return


def doPlot(limits, legendLabels, graphs, name, ylabel, myOpts={}, plotLabel=None):
    
    # Define lists & dictionaries
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
        r.SetLineStyle(1)
        return

    # Apply style and set label
    plot.histoMgr.forEachHisto(sty)
    plot.histoMgr.setHistoLegendLabelMany(ll)

    # Create & set legend
    nGraphs = len(graphs)
    # If sigma bands are drawn each legegend entry is plotted twice. Correct this in the count
    if "Sigma1" in name or "Sigma2" in name:
        nGraphs = nGraphs/2.0
    legend = getLegend(nGraphs, limit, myOpts, xPosLeg)
    plot.setLegend(legend)

    # Determine save name, minimum and maximum of y-axis
    ymin, ymax, saveName = getYMinMaxAndName(limits, name, myOpts)
    if myOpts.yMin == -1:
        myOpts.yMin = ymin
    if myOpts.yMax == -1:
        myOpts.yMax = ymax

    # Create the frame and set axes titles
    plot.createFrame(saveName, opts={"ymin": myOpts.yMin, "ymax": myOpts.yMax})
    
    # Add cut line?
    if myOpts.cutLine > 0:
        kwargs = {"greaterThan": True}
        plot.addCutBoxAndLine(cutValue=myOpts.cutLine, fillColor=ROOT.kRed, box=False, line=True, **kwargs)
    
    # Set axes titles
    plot.frame.GetXaxis().SetTitle(limit.mHplus())
    plot.frame.GetYaxis().SetTitle(ylabel)

    # Enable/Disable logscale for axes 
    ROOT.gPad.SetLogy(myOpts.logy)
    ROOT.gPad.SetLogx(myOpts.logx)

    # Enable grids in x and y?
    plot.getPad().SetGridx(myOpts.gridX)
    plot.getPad().SetGridy(myOpts.gridY)

    # Draw and add text
    plot.draw()
    plot.setLuminosity(limits[0].getLuminosity())
    plot.addStandardTexts(cmsTextPosition="outframe")
    addPhysicsText(histograms, limit, x=xPosText)

    # Save plots and return
    SavePlot(plot, saveName, myOpts)
    return

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

def getLegend(nPlots, limit, opts, xLeg1):
    dy = (nPlots-3)*0.15
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

def doPlotSigmaBands(limits, legendLabels, saveName):
    # Adjust save name
    saveName += "_sigmaBands"

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
    # If sigma bands are drawn each legegend entry is plotted twice. Correct this in the count
    if "Sigma1" in name or "Sigma2" in name:
        nGraphs = nGraphs/2.0
    legend = getLegend(nGraphs, limit, gOpts, xPosLeg)
    plot.setLegend(legend)

    # Determine save name, minimum and maximum of y-axis
    ymin, ymax, saveName = getYMinMaxAndName(limits, saveName, gOpts)
    if gOpts.yMin == -1:
        gOpts.yMin = ymin
    if gOpts.yMax == -1:
        gOpts.yMax = ymax

    # Create the frame and set axes titles
    plot.createFrame(saveName, opts={"ymin": gOpts.yMin, "ymax": gOpts.yMax})

    # Add cut line?
    if gOpts.cutLine > 0:
        kwargs = {"greaterThan": True}
        plot.addCutBoxAndLine(cutValue=gOpts.cutLine, fillColor=ROOT.kRed, box=False, line=True, **kwargs)
    
    # Set axes titles
    plot.frame.GetXaxis().SetTitle(limit.mHplus())
    plot.frame.GetYaxis().SetTitle(limit.BRlimit)

    # Enable/Disable logscale for axes 
    ROOT.gPad.SetLogy(gOpts.logy)
    ROOT.gPad.SetLogx(gOpts.logx)

    # Enable grids in x and y?
    plot.getPad().SetGridx(gOpts.gridX)
    plot.getPad().SetGridy(gOpts.gridY)

    # Draw the plot with standard texts
    plot.draw()
    plot.addStandardTexts(cmsTextPosition="outframe")
    plot.setLuminosity(limits[0].getLuminosity())
    addPhysicsText(histograms, limit, x=xPosText)

    # Save the plots & return
    SavePlot(plot, saveName, gOpts, [".png", ".pdf"])
    return

def getYMinMaxAndName(limits, name, opts, minIsMedian=False):
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
        
    if opts.logy:
        name += "_logy"
        ymax *= 2
    else:
        ymin =  0.0
        ymax *= 1.2

    if opts.logx:
        name += "_logx"
    return ymin, ymax, name

def SavePlot(plot, plotName, opts, saveFormats = [".png", ".pdf"]):
    # Check that path exists
    if not os.path.exists(opts.saveDir):
        os.makedirs(opts.saveDir)

    # Create the name under which plot will be saved
    saveName = os.path.join(opts.saveDir, plotName.replace("/", "_"))

    # For-loop: All save formats
    for i, ext in enumerate(saveFormats):
        saveNameURL = saveName + ext
        saveNameURL = saveNameURL.replace("/afs/cern.ch/user/a/attikis/public/html", "https://cmsdoc.cern.ch/~%s" % getpass.getuser())
        if i==0:
            print "=== plotBRLimitCompare_Hpluts2tb.py:"

        if opts.url:
            print "\t", saveNameURL
        else:
            print "\t", saveName + ext
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
    MINY        = -1
    MAXY        = -1
    CUTLINE     = 0
    RELATIVE    = False
    RELPAIRS    = False
    VERBOSE     = False
    UNBLINDED   = False

    parser = OptionParser(usage="Usage: %prog [options]", add_help_option=True, conflict_handler="resolve")

    parser.add_option("-v", "--verbose", dest="verbose", default=VERBOSE, action="store_true",
                      help="Verbose mode for debugging purposes [default: %s]" % (VERBOSE) )
    
    parser.add_option("--unblinded", dest="unblinded", default=UNBLINDED, action="store_true",
                      help="Enable unblined mode and thus also produced observed limits [default: %s]" % (UNBLINDED) )

    parser.add_option("--relative", dest="relative", action="store_true", default=RELATIVE, 
                      help="Do comparison relative to the first item [default: %s]" % (RELATIVE) )

    parser.add_option("--relativePairs", dest="relativePairs", action="store_true", default=RELPAIRS, 
                      help="Do multiple relative comparisons. The list of input directories is halved, the first half is the denominator and the second half is the numerator [default: %s]" % (RELPAIRS) )

    parser.add_option("--name", dest="name", type="string", default=None,
                      help="Name of the output plot")

    parser.add_option("--ymax", dest="ymax", type="float", default=None, 
                      help="Maximum y-axis value for regular plots")

    parser.add_option("--relativeYmax", dest="relativeYmax", type="float", default=None, 
                      help="Maximum y-value for relative plots")
    
    parser.add_option("--relativeYlabel", dest="relativeYlabel", default="Expected limit vs. nominal", 
                      help="Y-axis title for relative plots")

    parser.add_option("--url", dest="url", action="store_true", default=URL,
                      help="Don't print the actual save path the plots are saved, but print the URL instead [default: %s]" % URL)

    parser.add_option("--saveDir", dest="saveDir", type="string", default=SAVEDIR,
                      help="Directory where all plots will be saved [default: %s]" % SAVEDIR)

    parser.add_option("--logx", dest="logx", action="store_true", default=LOGX,
                      help="Plot x-axis (mass) as logarithmic [default: %s]" % (LOGX) )
    
    parser.add_option("--logy", dest="logy", action="store_true", default=LOGY,
                      help="Plot y-axis (exlusion limit) as logarithmic [default: %s]" % (LOGY) )
    
    parser.add_option("--gridX", dest="gridX", default=GRIDX, action="store_true",
                      help="Enable the grid for the x-axis [default: %s]" % (GRIDX) )

    parser.add_option("--gridY", dest="gridY", default=GRIDY, action="store_true",
                      help="Enable the grid for the y-axis [default: %s]" % (GRIDY) )

    parser.add_option("--yMin", dest="yMin", default=MINY, type="float",
                      help="Overwrite automaticly calculated minimum value of y-axis [default: %s]" % (MINY) )
    
    parser.add_option("--yMax", dest="yMax", default=MAXY, type="float",
                      help="Overwrite automaticly calculated maximum value of y-axis [default: %s]" % (MAXY) )

    parser.add_option("--cutLine", dest="cutLine", type="int", default=CUTLINE,
                      help="Number of digits (precision) to print/save limit results [default: %s]" % (CUTLINE) )

    (gOpts, args) = parser.parse_args()

    main(gOpts, args)
