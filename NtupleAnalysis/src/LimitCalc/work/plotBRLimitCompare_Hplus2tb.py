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


LAST USED:
./plotBRLimitCompare_Hplus2tb.py --logY --gridX --gridY --relative --url

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
    myList1 = [
        ("H^{+}#rightarrow tb (#chi^{2})", "*limits2017/datacards_default_170827_075947_noLumi/CombineResults_taujets_*"),
        #("p_{T}^{b3}#geq40, BDT#geq0.85"        , "limits2018/datacards_Hplus2tbAnalysis_NewLeptonVeto_PreSel_3bjets40_SigSel_MVA0p85_180126_030205/CombineResults*"),
        #("p_{T}^{b3}#geq40, BDT#geq0.85 (lev1)" , "limits2018/datacards_Hplus2tbAnalysis_NewLeptonVeto_PreSel_3bjets40_SigSel_MVA0p85_180126_030205_level1/CombineResults*"),
        ("p_{T}^{b3}#geq40, BDT#geq0.85 (lev2)" , "limits2018/datacards_Hplus2tbAnalysis_NewLeptonVeto_PreSel_3bjets40_SigSel_MVA0p85_180126_030205_level2/CombineResults*"),
        #("p_{T}^{b3}#geq40, BDT#geq0.85 (lev3)"         , "limits2018/datacards_Hplus2tbAnalysis_NewLeptonVeto_PreSel_3bjets40_SigSel_MVA0p85_180126_030205_level3/CombineResults*"),
        #("p_{T}^{b3}#geq40, BDT#geq0.85 (lev2, BugFix)" , "limits2018/datacards_Hplus2tbAnalysis_PreSel_3CSVv2M_Pt40_SigSel_MVA0p85_180214_074442_level2_MajorBugFix/CombineResults*"),
        ("p_{T}^{b3}#geq40, BDT#geq0.85 (lev2, BugFix)" , "limits2018/datacards_Hplus2tbAnalysis_PreSel_3CSVv2M_Pt40_SigSel_MVA0p85_180214_074442_level2_MajorBugFix_StatOnly/CombineResults*"),
        ]
    opts.name = "h2tb"
    doCompare(opts.name, myList1)

    # Do all H->tb fully hadronic final states comparison
    myList2 = [
        ("H^{+}#rightarrow tb (#chi^{2})", "*limits2017/datacards_default_170827_075947_noLumi/CombineResults_taujets_*"),
        #("H^{+}#rightarrow tb (Fake-b binned)", "limits2018/datacards_Hplus2tbAnalysis_PreSel_3bjets40_SigSel_MVA0p85_180126_030205_level3/CombineResults*"),
        #("H^{+}#rightarrow tb (MC)"           , "limits2018/datacards_NewLeptonVeto_3bjets40_MVA0p85_MVA0p85_TopMassCutOff600GeV_180122_022900/CombineResults*"),
        #("H^{+}#rightarrow tb"                , "limits2018/datacards_Hplus2tbAnalysis_NewLeptonVeto_PreSel_3bjets40_SigSel_MVA0p85_180126_030205_level3/CombineResults*"),
        ("H^{+}#rightarrow tb"                , "limits2018/datacards_Hplus2tbAnalysis_NewLeptonVeto_PreSel_3bjets40_SigSel_MVA0p85_180126_030205_level3/CombineResults*"),
        ("H^{+}#rightarrow tb (BugFix)"       , "limits2018/datacards_Hplus2tbAnalysis_PreSel_3CSVv2M_Pt40_SigSel_MVA0p85_180214_074442_level2_MajorBugFix_StatOnly/CombineResults*"),
        #("H^{+}#rightarrow tb (BugFix, Lumi)" , "limits2018/datacards_Hplus2tbAnalysis_PreSel_3CSVv2M_Pt40_SigSel_MVA0p85_180214_074442_level2_MajorBugFix/CombineResults*"),
        ("H^{+}#rightarrow tb (~boosted)"     , "limits2017/*datacards_combine_MIT_approximate/CombineResults_taujets_*"),
        # ("Single Lepton"                 , "limits2017/*datacards_combine_SingleLepton_approximate/CombineResults_taujets_*"),
        ]

    # Do the second list of plots
    opts.name    = "all"
    doCompare(opts.name, myList2)

    # Inform user and exit
    Print("All plots saved under directory %s" % (ShellStyles.NoteStyle() + savePath + ShellStyles.NormalStyle()), True)    
    return

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
    _opts.yMin    = 0.0
    _opts.yMax    = 2.5
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
    legend = getLegend(nGraphs, limit, xPosLeg)
    plot.setLegend(legend)

    # Determine save name, minimum and maximum of y-axis
    ymin, ymax, saveName = getYMinMaxAndName(limits, name)
    if _opts.yMin == -1:
        _opts.yMin = ymin
    if _opts.yMax == -1:
        _opts.yMax = ymax

    # Create the frame and set axes titles
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

    parser.add_option("--cutLine", dest="cutLine", type="float", default=CUTLINE,
                      help="Add TLine on the x-axis at this value  [default: %s]" % (CUTLINE) )

    parser.add_option("--cutLineY", dest="cutLineY", type="float", default=CUTLINEY,
                      help="Add TLine on the y-axis at this value  [default: %s]" % (CUTLINEY) )

    (opts, args) = parser.parse_args()

    # Save in current working directory?
    if opts.saveDir =="":
        opts.saveDir = os.getcwd()

    main()
