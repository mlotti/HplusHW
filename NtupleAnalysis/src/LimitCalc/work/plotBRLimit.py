#!/usr/bin/env python

#================================================================================================
# Import modules
#================================================================================================
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
#def Verbose(msg, printHeader=False):
#    '''
#    Calls Print() only if verbose options is set to true.
#    '''
#    if not opts.verbose:
#        return
#    Print(msg, printHeader)
#    return

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
    
    # Do the limit plot
    doBRlimit(limits, opts.unblinded, opts)

    # Do the limit plot (logy)
    doBRlimit(limits, opts.unblinded, opts, log=True)

    # Do the limit error plot
    doLimitError(limits, opts.unblinded)

    # Print the Limits
    limits.printLimits(unblindedStatus=opts.unblinded, nDigits=opts.digits)
    # limits.print2(unblindedStatus=opts.unblinded)
    
    # Save the Limits in a LaTeX table file
    limits.saveAsLatexTable(unblindedStatus=opts.unblinded, nDigits=opts.digits)
    return


def doBRlimit(limits, unblindedStatus, opts, log=False):
    leptonicFS = False
    
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


    graphs.extend([
            histograms.HistoGraph(limits.expectedGraph(), "Expected", drawStyle="L"),
            histograms.HistoGraph(limits.expectedBandGraph(sigma=1), "Expected1", drawStyle="F", legendStyle="fl"),
            histograms.HistoGraph(limits.expectedBandGraph(sigma=2), "Expected2", drawStyle="F", legendStyle="fl"),
            ])

    saveFormats = [".png", ".C", ".pdf"]
    if not opts.excludedArea:
        saveFormats.append(".eps")
    plot = plots.PlotBase(graphs, saveFormats=saveFormats)
    plot.setLuminosity(limits.getLuminosity())

    plot.histoMgr.setHistoLegendLabelMany({
            "Expected": None,
            "Expected1": "Expected median #pm 1#sigma",
            "Expected2": "Expected median #pm 2#sigma"
            })
    
    dy = -0.1

    limit.BRassumption = ""   
    #limit.BRassumption = "Assuming B(H^{+}#rightarrow#tau^{+}#nu_{#tau}) = 1"
    #limit.BRassumption = "Assuming B(H^{+}#rightarrowt#bar{b}) = 1"
    if limit.BRassumption != "":
        dy -= 0.05
    #if len(limits.getFinalstates()) > 1:
    #    dy -= 0.1
    
    # Create legend
    x = 0.51
    x = 0.45
    legend = histograms.createLegend(x, 0.78+dy, x+0.4, 0.92+dy)
    legend.SetMargin(0.17)
    # Make room for the final state text
    if opts.excludedArea:
        legend.SetFillStyle(1001)
    plot.setLegend(legend)

    name = "limitsBr"
    ymin = 0
    ymax = limits.getFinalstateYmaxBR() #fixme: alexandros
    if opts.logx:
        name += "_logx"
    if log:
        name += "_log"
        if limits.isHeavyStatus:
            ymin = 1e-3
            ymax = 10.0
            if limit.BRassumption != "":
                ymax = 10.0
        else:
            ymin = 1e-3
            ymax = 4e-2
    if leptonicFS:
        ymax = 10
    if len(limits.mass) == 1:
        plot.createFrame(name, opts={"xmin": limits.mass[0]-5.0, "xmax": limits.mass[0]+5.0, "ymin": ymin, "ymax": ymax})
    else:
        plot.createFrame(name, opts={"ymin": ymin, "ymax": ymax})

    # Set x-axis title
    plot.frame.GetXaxis().SetTitle(limit.mHplus())

    if limits.isHeavyStatus:
        if limit.BRassumption != "":
            plot.frame.GetYaxis().SetTitle("95% CL limit for #sigma_{H^{+}} (pb)")
        else:            
            plot.frame.GetYaxis().SetTitle(limit.sigmaBRlimit)
    else:
        plot.frame.GetYaxis().SetTitle(limit.BRlimit)

    # Enable/Disable logscale for axes
    if log:
        plot.getPad().SetLogy(log)
    if opts.logx:
        plot.getPad().SetLogx(log)

    # Draw the plot with standard texts
    plot.draw()
    plot.addStandardTexts()

    # Add physics-process text
    size = 20
    x    = 0.51
    x    = 0.45
    process = limit.process
    if limits.isHeavyStatus:
        process = limit.processHeavy
    histograms.addText(x, 0.88, process, size=size)

    # Add final-state text
    # histograms.addText(x, 0.84, limits.getFinalstateText(), size=size) #fixme: alexandros
    histograms.addText(x, 0.84, "fully hadronic final state", size=size) #fixme: alexandros
    # histograms.addText(x, 0.84, "#tau_{h}+jets and #mu#tau_{h} final states", size=size)
    # histograms.addText(x, 0.84, "#tau_{h}+jets final state", size=size)
    # histograms.addText(x, 0.84, "#tau_{h}+jets, #mu#tau_{h}, ee, e#mu, #mu#mu final states", size=size)

    if leptonicFS:
        histograms.addText(x, 0.84, "#mu#tau_{h}, ee, e#mu, #mu#mu final states", size=size)
    if limit.BRassumption != "":
        histograms.addText(x, 0.79, limit.BRassumption, size=size)

    plot.save()
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
    #LOGY        = False
    DIGITS      = 5

    parser = OptionParser(usage="Usage: %prog [options]")

    parser.add_option("-v", "--verbose", dest="verbose", default=VERBOSE, action="store_true",
                      help="Verbose mode for debugging purposes [default: %s]" % (VERBOSE))

    parser.add_option("--unblinded", dest="unblinded", default=UNBLINDED, action="store_true",
                      help="Enable unblined mode [default: %s]" % (UNBLINDED) )

    parser.add_option("--paper", dest="paper", default=PAPER, action="store_true",
                      help="Paper mode [default: %s]" % (PAPER) )

    parser.add_option("--unpub", dest="unpublished", default=UNPUBLISHED, action="store_true",
                      help="Unpublished mode [default: %s]" % (UNPUBLISHED) )

    parser.add_option("--parentheses", dest="parentheses", default=PARENTHESES, action="store_true",
                      help="Use parentheses for sigma and BR [default: %s]" % (PARENTHESES) )

    parser.add_option("--excludedArea", dest="excludedArea", default=EXCLUDEAREA, action="store_true",
                      help="Add excluded area as in MSSM exclusion plots [default: %s]" % (EXCLUDEAREA) )

    parser.add_option("--logx", dest="logx", action="store_true", default=LOGX, 
                      help="Plot x-axis (H+ mass) as logarithmic [default: %s]" % (LOGX) )
    
    #parser.add_option("--logy", dest="logy", action="store_true", default=LOGY,
    #                  help="Plot y-axis (H+ mass) as logarithmic [default: %s]" % (LOGY) )
    
    parser.add_option("--digits", dest="digits", type="int", default=DIGITS,
                      help="Number of digits (precision) to print/save limit results [default: %s]" % (DIGITS) )

    (opts, args) = parser.parse_args()
    main(opts)
