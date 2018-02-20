#!/usr/bin/env python
'''
DESCRIPTION:
This is the swiss pocket knife for running Lands/Combine on large array of datacards


INSTRUCTIONS:


USAGE:
cd datacards_test4b/CombineResults_taujets_170913_192047
../../plotBRLimit_Hplus2tb.py 


EXAMPLES:
../../plotBRLimit_Hplus2tb.py [opts]
../../plotBRLimit_Hplus2tb.py --excludedArea --cutLine 500 --gridX --gridY
../../plotBRLimit_Hplus2tb.py --excludedArea --cutLine 500 --gridX --gridY --yMin 1e-3 --settings Default
../../plotBRLimit_Hplus2tb.py --excludedArea --cutLine 500 --gridX --gridY --yMin 1e-3 --settings NoLumi
../../../plotBRLimit_Hplus2tb.py --excludedArea --cutLine 500 --gridX --gridY --yMin 1e-3 --settings Default --url
../../../plotBRLimit_Hplus2tb.py --excludedArea --cutLine 500 --gridX --gridY --yMin 1e-3 --yMax 10 --settings NoLumi


LAST USED:
../../../plotBRLimit_Hplus2tb.py --excludedArea --gridX --gridY --settings NoLumi --yMin 1e-1

'''

#================================================================================================
# Import modules
#================================================================================================
import os
import getpass
import sys
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


def main(opts):
    if opts.saveDir =="":
        opts.saveDir = os.getcwd()

    # Assume by default that the observed limit should be blinded
    if not opts.unblinded:
        msg="Working in BLINDED mode, i.e. I will not tell you the observed limit before you say please ..."
        Print(msg, True)
    limits = limit.BRLimits()

    # Enable OpenGL
    if opts.excludedArea:
        ROOT.gEnv.SetValue("OpenGL.CanvasPreferGL", 1)

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    if not limits.isHeavyStatus:
        # Give more space for four digits on the y axis labels
        style.tdrStyle.SetPadLeftMargin(0.19)
        style.tdrStyle.SetTitleYOffset(1.6)

    # Set the paper mode
    if opts.paper:
        histograms.cmsTextMode = histograms.CMSMode.PAPER
    # Set the paper mode
    if opts.unpublished:
        histograms.cmsTextMode = histograms.CMSMode.UNPUBLISHED
    # Use BR symbol for H+ decay channel with subscript or parentheses?
    if opts.parentheses:
        limit.useParentheses()
    
    # Do the limit plots
    doBRlimit(limits, opts.unblinded, opts, logy=False)
    doBRlimit(limits, opts.unblinded, opts, logy=True)
    doLimitError(limits, opts.unblinded)

    # Print the Limits
    limits.printLimits(unblindedStatus=opts.unblinded, nDigits=opts.digits)
    # limits.print2(unblindedStatus=opts.unblinded)
    
    # Save the Limits in a LaTeX table file
    limits.saveAsLatexTable(unblindedStatus=opts.unblinded, nDigits=opts.digits)
    return


def doBRlimit(limits, unblindedStatus, opts, logy=False):
    
    graphs = []
    if unblindedStatus:
        gr = limits.observedGraph()
        if gr != None:
            gr.SetPoint(gr.GetN()-1, gr.GetX()[gr.GetN()-1]-1e-10, gr.GetY()[gr.GetN()-1])
            if opts.excludedArea:
                graphs.append(histograms.HistoGraph(gr, "Observed", drawStyle="PL", legendStyle=None))
                excluded = gr.Clone()
                excluded.SetPoint(excluded.GetN(), excluded.GetX()[excluded.GetN()-1], 0.05)
                excluded.SetPoint(excluded.GetN(), excluded.GetX()[0], 0.05)
                limit.setExcludedStyle(excluded)
                graphs.append(histograms.HistoGraph(excluded, "Excluded", drawStyle="F", legendStyle="lpf", legendLabel="Observed"))
            else:
                graphs.append(histograms.HistoGraph(gr, "Observed", drawStyle="PL", legendStyle="lp"))

    # Add the expected lines
    graphs.extend([
            histograms.HistoGraph(limits.expectedGraph(), "Expected", drawStyle="L"),
            histograms.HistoGraph(limits.expectedBandGraph(sigma=1), "Expected1", drawStyle="F", legendStyle="fl"),
            histograms.HistoGraph(limits.expectedBandGraph(sigma=2), "Expected2", drawStyle="F", legendStyle="fl"),
            ])

    # Plot the TGraphs
    saveFormats = [".png", ".C", ".pdf"]
    if not opts.excludedArea:
        saveFormats.append(".eps")

    plot = plots.PlotBase(graphs, saveFormats=saveFormats)
    plot.setLuminosity(limits.getLuminosity())

    # Customise legend entries
    plot.histoMgr.setHistoLegendLabelMany({
            "Expected" : None,
            "Expected1": "Expected median #pm 1#sigma",
            "Expected2": "Expected median #pm 2#sigma"
            })
    
    # Branching Ratio Assumption
    if 0:
        limit.BRassumption = "Assuming B(H^{+}#rightarrowt#bar{b}) = 1"

    # Create legend
    xPos   = 0.53
    legend = getLegend(limit, opts, xPos)
    plot.setLegend(legend)

    # Get y-min, y-max, and histogram name to be saved as
    ymin, ymax, saveName = getYMinMaxAndName(limits, "limitsBr", logy, opts)
    if opts.yMin != -1:
        ymin = opts.yMin
    if opts.yMax != -1:
        ymax = opts.yMax

    if len(limits.mass) == 1:
        plot.createFrame(saveName, opts={"xmin": limits.mass[0]-5.0, "xmax": limits.mass[0]+5.0, "ymin": ymin, "ymax": ymax})
    else:
        plot.createFrame(saveName, opts={"ymin": ymin, "ymax": ymax})

    # Add cut box?
    if opts.cutLine > 0:
        kwargs = {"greaterThan": True}
        plot.addCutBoxAndLine(cutValue=opts.cutLine, fillColor=ROOT.kRed, box=False, line=True, **kwargs)

    # Set x-axis title
    plot.frame.GetXaxis().SetTitle(limit.mHplus()) 

    if limit.BRassumption != "":
        plot.frame.GetYaxis().SetTitle("95% CL limit for #sigma_{H^{+}} (pb)")
    else:
        plot.frame.GetYaxis().SetTitle(limit.sigmaBRlimit)
        # plot.frame.GetYaxis().SetTitle(limit.BRlimit)

    # Enable/Disable logscale for axes
    if logy:
        plot.getPad().SetLogy(logy)
        plot.getPad().SetLogx(opts.logx)

    # Enable grids in x and y?
    plot.getPad().SetGridx(opts.gridX)
    plot.getPad().SetGridy(opts.gridY)

    # Draw the plot with standard texts
    plot.draw()
    plot.addStandardTexts()
    
    # Add physics-related text on canvas
    addPhysicsText(histograms, limit, x=xPos)
    
    # Save the canvas
    plot.save()

    # Save the plots
    SavePlot(plot, saveName, os.path.join(opts.saveDir, opts.settings) )

    return


def SavePlot(plot, plotName, saveDir, saveFormats = [".png", ".pdf", ".C"]):

    # Check that path exists
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)

    # Create the name under which plot will be saved
    saveName = os.path.join(saveDir, plotName.replace("/", "_"))

    # For-loop: All save formats
    for i, ext in enumerate(saveFormats):
        saveNameURL = saveName + ext
        if "afs" in saveNameURL: #lxplus
            saveNameURL = saveNameURL.replace("/afs/cern.ch/user/a/attikis/public/html/", "https://cmsdoc.cern.ch/~attikis/")
        else: #lpc
            saveNameURL = saveNameURL.replace("/publicweb/a/aattikis/", "http://home.fnal.gov/~aattikis/")
        if i==0:
            print "=== plotBRLimit_Hpluts2tb.py:"

        if opts.url:
            print "\t", saveNameURL
        else:
            print "\t", saveName + ext
        plot.saveAs(saveName, formats=saveFormats)
    return


def getLegend(limit, opts, xLeg1=0.53):
    dy = -0.10
    if limit.BRassumption != "":
        dy -= 0.05

    # Create customised legend
    #xLeg1 = 0.53
    xLeg2 = 0.93
    yLeg1 = 0.78 + dy
    yLeg2 = 0.91 + dy
    if opts.unblinded:
        yLeg2 = 0.92 + dy

    # Adjust legend slightly to visually align with text
    legend = histograms.createLegend(xLeg1*.98, yLeg1, xLeg2, yLeg2) 
    legend.SetMargin(0.17)

    # Make room for the final state text
    if opts.excludedArea:
        legend.SetFillStyle(1001) #legend.SetFillStyle(3001)
    return legend


def getYMinMaxAndName(limits, name, logy, opts):
    ymin = limits.getYMin()
    ymax = limits.getYMax()

    if logy:
        name += "_logy"
        ymax *= 2
    else:
        ymin =  0.0
        ymax *= 1.2

    if opts.logx:
        name += "_logx"
    return ymin, ymax, name


def addPhysicsText(histograms, limit, x=0.45, y=0.84, size=20):
    '''
    Add physics-process text on canvas
    '''
    # Add process text on canvas
    histograms.addText(x, y+0.04, limit.processHeavyHtb, size=size)

    # Add final-state text
    histograms.addText(x, y, "fully hadronic final state", size=size)

    if 0:
        histograms.addText(x, y, "#tau_{h}+jets and #mu#tau_{h} final states", size=size)
        histograms.addText(x, y, "#tau_{h}+jets final state", size=size)
        histograms.addText(x, y, "#tau_{h}+jets, #mu#tau_{h}, ee, e#mu, #mu#mu final states", size=size)

    if limit.BRassumption != "":
        histograms.addText(x, y-0.05, limit.BRassumption, size=size)
    return


def doLimitError(limits, unblindedStatus):
    expRelErrors = []
    expLabels    = {}
    obsRelErrors = []
    obsLabels    = {}

    order = [0, 1, -1, 2, -2]
    expErrors = [limits.expectedErrorGraph(sigma=s) for s in order]
    if expErrors[0] != None:
        exps = [limits.expectedGraph(sigma=s) for s in order]
        expRelErrors = [(limit.divideGraph(expErrors[i], exps[i]), "ExpRelErr%d"%i) for i in xrange(len(exps))]
        expLabels = {
            "ExpRelErr0": "Expected median",
            "ExpRelErr1": "Expected +1#sigma",
            "ExpRelErr2": "Expected -1#sigma",
            "ExpRelErr3": "Expected +2#sigma",
            "ExpRelErr4": "Expected -2#sigma",
            }

    if unblindedStatus:
        obsErr = limits.observedErrorGraph()
        if obsErr != None:
            obs = limits.observedGraph()
            if obs != None:
                obsRelErrors = [(limit.divideGraph(obsErr, obs), "ObsRelErr")]
                obsLabels = {"ObsRelErr": "Observed"}

    if len(expRelErrors) == 0 and len(obsRelErrors) == 0:
        return

    # Create the plot
    plot = plots.PlotBase()
    if len(expRelErrors) > 0:
        plot.histoMgr.extendHistos([histograms.HistoGraph(x[0], x[1], drawStyle="PL", legendStyle="lp") for x in expRelErrors])
        plot.histoMgr.forEachHisto(styles.generator())
        def sty(h):
            r = h.getRootHisto()
            r.SetLineStyle(1)
            r.SetLineWidth(3)
            r.SetMarkerSize(1.4)
        plot.histoMgr.forEachHisto(sty)
        plot.histoMgr.setHistoLegendLabelMany(expLabels)
    if unblindedStatus:
        if len(obsRelErrors) > 0:
            obsRelErrors[0][0].SetMarkerSize(1.4)
            obsRelErrors[0][0].SetMarkerStyle(25)
            plot.histoMgr.insertHisto(0, histograms.HistoGraph(obsRelErrors[0][0], obsRelErrors[0][1], drawStyle="PL", legendStyle="lp"))
            plot.histoMgr.setHistoLegendLabelMany(obsLabels)

    plot.setLegend(histograms.moveLegend(histograms.createLegend(0.48, 0.75, 0.85, 0.92), dx=0.1, dy=-0.1))

    if len(limits.mass) == 1:
        plot.createFrame("limitsBrRelativeUncertainty", opts={"xmin": limits.mass[0]-5.0, "xmax": limits.mass[0]+5.0,  "ymin": 0, "ymaxfactor": 1.5})
    else:
        plot.createFrame("limitsBrRelativeUncertainty", opts={"ymin": 0, "ymaxfactor": 1.5})
    plot.frame.GetXaxis().SetTitle(limit.mHplus())
    plot.frame.GetYaxis().SetTitle("Uncertainty/limit")

    plot.draw()

    plot.setLuminosity(limits.getLuminosity())
    plot.addStandardTexts()

    size = 20
    x = 0.2
    histograms.addText(x, 0.88, limit.process, size=size)
    histograms.addText(x, 0.84, limits.getFinalstateText(), size=size)
    histograms.addText(x, 0.79, limit.BRassumption, size=size)

    size = 22
    x = 0.55
    histograms.addText(x, 0.88, "Toy MC relative", size=size)
    histograms.addText(x, 0.84, "statistical uncertainty", size=size)

    plot.save()


if __name__ == "__main__":

    # Default Values
    VERBOSE     = False
    UNBLINDED   = False
    PAPER       = False
    UNPUBLISHED = False
    PARENTHESES = False
    EXCLUDEAREA = False
    LOGX        = False
    DIGITS      = 5
    CUTLINE     = 0
    GRIDX       = False
    GRIDY       = False
    MINY        = -1
    MAXY        = -1
    SETTINGS    = ""
    SAVEDIR     = "/afs/cern.ch/user/%s/%s/public/html/Combine" % (getpass.getuser()[0], getpass.getuser())
    URL         = False

    parser = OptionParser(usage="Usage: %prog [options]")

    parser.add_option("-v", "--verbose", dest="verbose", default=VERBOSE, action="store_true",
                      help="Verbose mode for debugging purposes [default: %s]" % (VERBOSE))

    parser.add_option("--unblinded", dest="unblinded", default=UNBLINDED, action="store_true",
                      help="Enable unblined mode [default: %s]" % (UNBLINDED) )

    parser.add_option("--paper", dest="paper", default=PAPER, action="store_true",
                      help="Paper mode [default: %s]" % (PAPER) )

    parser.add_option("--url", dest="url", action="store_true", default=URL,
                      help="Don't print the actual save path the plots are saved, but print the URL instead [default: %s]" % URL)
    
    parser.add_option("--unpub", dest="unpublished", default=UNPUBLISHED, action="store_true",
                      help="Unpublished mode [default: %s]" % (UNPUBLISHED) )

    parser.add_option("--parentheses", dest="parentheses", default=PARENTHESES, action="store_true",
                      help="Use parentheses for sigma and BR [default: %s]" % (PARENTHESES) )

    parser.add_option("--excludedArea", dest="excludedArea", default=EXCLUDEAREA, action="store_true",
                      help="Add excluded area as in MSSM exclusion plots [default: %s]" % (EXCLUDEAREA) )

    parser.add_option("--logx", dest="logx", action="store_true", default=LOGX, 
                      help="Plot x-axis (H+ mass) as logarithmic [default: %s]" % (LOGX) )
    
    parser.add_option("--digits", dest="digits", type="int", default=DIGITS,
                      help="Number of digits (precision) to print/save limit results [default: %s]" % (DIGITS) )

    parser.add_option("--cutLine", dest="cutLine", type="int", default=CUTLINE,
                      help="Number of digits (precision) to print/save limit results [default: %s]" % (CUTLINE) )

    parser.add_option("--gridX", dest="gridX", default=GRIDX, action="store_true",
                      help="Enable the grid for the x-axis [default: %s]" % (GRIDX) )

    parser.add_option("--gridY", dest="gridY", default=GRIDY, action="store_true",
                      help="Enable the grid for the y-axis [default: %s]" % (GRIDY) )

    parser.add_option("--yMin", dest="yMin", default=MINY, type="float",
                      help="Overwrite automaticly calculated minimum value of y-axis [default: %s]" % (MINY) )

    parser.add_option("--yMax", dest="yMax", default=MAXY, type="float",
                      help="Overwrite automaticly calculated maximum value of y-axis [default: %s]" % (MAXY) )

    parser.add_option("--settings", dest="settings", type="string", default=SETTINGS,
                      help="Sub-directory describing additional settings used when creating the limits (e.g. no lumi) [default: %s]" % SETTINGS) 

    parser.add_option("--saveDir", dest="saveDir", type="string", default=SAVEDIR,
                      help="Directory where all plots will be saved [default: %s]" % SAVEDIR)

    (opts, args) = parser.parse_args()

    main(opts)
    
