#!/usr/bin/env python

import os
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

def main(opts, args):
    # Apply TDR style
    style = tdrstyle.TDRStyle()
    histograms.cmsTextMode = histograms.CMSMode.NONE

#    compareTauJets(opts)
#    compareLeptonic(opts)
#    compareCombination(opts)
#    compareCombinationSanitychecksLHC(opts)

#    compareTauJetsDeltaPhi(opts)
    compareHplus(opts)
#    compareInjected(opts, args)

def compareTauJets(opts):
    doCompare("taujets", [
            # (name, dir)
            ("LHC-CLs", "LandS*taujets_lhc_*"),
            ("LHC-CLs (asymp)", "LandS*taujets_lhcasy_*"),
            ("LEP-CLs", "LandS*taujets_lep_*"),
            ], opts)

def compareLeptonic(opts):
    doCompare("emu", [
            # (name, dir)
            ("LHC-CLs", "LandS*emu_lhc_*"),
            ("LHC-CLs (asymp)", "LandS*emu_lhcasy_*"),
            ("LEP-CLs", "LandS*emu_lep_*"),
            ], opts)

    doCompare("mutau", [
            # (name, dir)
            ("LHC-CLs", "LandS*mutau_lhc_*"),
            ("LHC-CLs (asymp)", "LandS*mutau_lhcasy_*"),
            ("LEP-CLs", "LandS*mutau_lep_*"),
            ], opts)

    doCompare("etau", [
            # (name, dir)
#            ("LHC-CLs", "LandS*etau_lhc_*"),
            ("LHC-CLs", "LandSMultiCrab_etau_lhc_jobs10_sb_600_b300_120514_151345/"),
            ("LHC-CLs (asymp)", "LandS*etau_lhcasy_*"),
            ("LEP-CLs", "LandS*etau_lep_*"),
            ], opts)

def compareCombination(opts):
    doCompare("combination", [
            # (name, dir)
#            ("LHC-CLs", "LandS*combination_lhc_jobs*"),
            ("LHC-CLs", "LandSMultiCrab_combination_lhc_jobs10_sb300_b150_120514_173610"),
            ("LHC-CLs (asymp)", "LandS*combination_lhcasy_*"),
            ("LEP-CLs", "LandS*combination_lep_*"),
            ], opts)

def compareCombinationSanitychecksLHC(opts):
    doCompare("combination_migrad_vs_minos", [
            # (name, dir)
            ("Migrad", "LandS*combination_lhc_sanitycheck_migrad_*"),
            ("Minos", "LandS*combination_lhc_sanitycheck_minos_*"),
            ], opts)


def compareTauJetsDeltaPhi(opts):
    doCompare("taujets_deltaphi", [
              # (name, dir)
              ("Without #Delta#phi selection", "datacards_220312_123012_fully_hadronic_2011A_MET50_withRtau_NoDeltaPhi_withShapes_shapeStat/LandSMultiCrab_taujets_lhc_*"),
              ("#Delta#phi < 160^{o}", "combination_new/LandS*taujets_lhc_*"),
              ("#Delta#phi < 130^{o}", "datacards_220312_122901_fully_hadronic_2011A_MET50_withRtau_DeltaPhi130_withShapes_shapeStat/LandSMultiCrab_taujets_lhc_*")
              ], opts,
              expectedMedianOpts={"ymax": 0.07},
              expectedSigma1Opts={"ymax": 0.1},
              expectedSigma1RelativeOpts={"ymax": 2.2, "ymin": 0.4},
              expectedSigma2RelativeOpts={"ymax": 3.6, "ymin": 0.3},
              moveLegend={"dh": -0.04}
              )

def compareHplus(opts):
    myOpts = {}
    if opts.lightHplus:
        myList = [
              ("#tau p_{T}>41, E_{T}^{miss}>60, No ang.cuts","*TailKillerNoCuts*nominal*/CombineMultiCrab*"),
              ("#tau p_{T}>41, E_{T}^{miss}>60, Loose ang.cuts","*TailKillerLoose*nominal*/CombineMultiCrab*"),
              ("#tau p_{T}>41, E_{T}^{miss}>60, Tight ang.cuts","*TailKillerTight*nominal*/CombineMultiCrab*"),
              ("#tau p_{T}>50, E_{T}^{miss}>60, Loose ang.cuts","*TailKillerLoose*tau50*/CombineMultiCrab*"),
#              ("#tau p_{T}>50, E_{T}^{miss}>60, Tight ang.cuts","*TailKillerTight*tau50*/CombineMultiCrab*"),
              ("#tau p_{T}>41, E_{T}^{miss}>70, No ang.cuts","*TailKillerNoCuts*met70_*/CombineMultiCrab*"),
              ("#tau p_{T}>41, E_{T}^{miss}>70, Loose ang.cuts","*TailKillerLoose*met70_*/CombineMultiCrab*"),
              ("#tau p_{T}>41, E_{T}^{miss}>70, Tight ang.cuts","*TailKillerTight*met70_*/CombineMultiCrab*"),
              ("#tau p_{T}>41, E_{T}^{miss}>80, No ang.cuts","*TailKillerNoCuts*met80_*/CombineMultiCrab*"),
              ("#tau p_{T}>41, E_{T}^{miss}>80, Loose ang.cuts","*TailKillerLoose*met80_*/CombineMultiCrab*"),
              ("#tau p_{T}>41, E_{T}^{miss}>80, Tight ang.cuts","*TailKillerTight*met80_*/CombineMultiCrab*"),
              ("#tau p_{T}>50, E_{T}^{miss}>80, Loose ang.cuts","*TailKillerLoose*met80tau50_*/CombineMultiCrab*"),
              ("#tau p_{T}>41 no R_{#tau}, E_{T}^{miss}>60, Loose ang.cuts","*TailKillerLoose*nortau_*/CombineMultiCrab*"),
#              ("#tau p_{T}>41 no R_{#tau}, E_{T}^{miss}>60, Tight ang.cuts","*TailKillerTight*nortau_*/CombineMultiCrab*"),
        ]
        myOpts = expectedMedianOpts= {"ymin": 0.001, "ymax":0.02}
    elif opts.heavyHplus:
        myList = [
              ("#tau p_{T}>41, E_{T}^{miss}>60, No ang.cuts","*TailKillerNoCuts*nominal*/CombineMultiCrab*"),
              ("#tau p_{T}>41, E_{T}^{miss}>60, Loose ang.cuts","*TailKillerLoose*nominal*/CombineMultiCrab*"),
              ("#tau p_{T}>41, E_{T}^{miss}>60, Tight ang.cuts","*TailKillerTight*nominal*/CombineMultiCrab*"),
            # ("#tau p_{T}>50, E_{T}^{miss}>60, Loose ang.cuts","*TailKillerLoose*tau50*/CombineMultiCrab*"),
              ("#tau p_{T}>50, E_{T}^{miss}>60, Tight ang.cuts","*TailKillerTight*tau50*/CombineMultiCrab*"),
              ("#tau p_{T}>41, E_{T}^{miss}>70, No ang.cuts","*TailKillerNoCuts*met70_*/CombineMultiCrab*"),
              ("#tau p_{T}>41, E_{T}^{miss}>70, Loose ang.cuts","*TailKillerLoose*met70_*/CombineMultiCrab*"),
              ("#tau p_{T}>41, E_{T}^{miss}>70, Tight ang.cuts","*TailKillerTight*met70_*/CombineMultiCrab*"),
              ("#tau p_{T}>41, E_{T}^{miss}>80, No ang.cuts","*TailKillerNoCuts*met80_*/CombineMultiCrab*"),
              ("#tau p_{T}>41, E_{T}^{miss}>80, Loose ang.cuts","*TailKillerLoose*met80_*/CombineMultiCrab*"),
              ("#tau p_{T}>41, E_{T}^{miss}>80, Tight ang.cuts","*TailKillerTight*met80_*/CombineMultiCrab*"),
            #  ("#tau p_{T}>50, E_{T}^{miss}>80, Loose ang.cuts","*TailKillerLoose*met80tau50_*/CombineMultiCrab*"),
              ("#tau p_{T}>50, E_{T}^{miss}>80, Tight ang.cuts","*TailKillerTight*met80tau50_*/CombineMultiCrab*"),
              ("#tau p_{T}>41 no R_{#tau}, E_{T}^{miss}>60, No ang.cuts","*TailKillerNoCuts*nortau_*/CombineMultiCrab*"),
              ("#tau p_{T}>41 no R_{#tau}, E_{T}^{miss}>60, Loose ang.cuts","*TailKillerLoose*nortau_*/CombineMultiCrab*"),
            # ("#tau p_{T}>41 no R_{#tau}, E_{T}^{miss}>60, Tight ang.cuts","*TailKillerTight*nortau_*/CombineMultiCrab*"),
        ]
        myOpts = expectedMedianOpts= {"ymin": 0.008, "ymax":1.0}
    elif opts.tailFit:
        myList = [
              ("Nominal", "*DataDriven/CombineMultiCrab*"),
              ("50 GeV bin width", "*50GeVBins/CombineMultiCrab*"),
              ("Double tail fit uncert.", "*doublefituncert/CombineMultiCrab*"),
              ("No tail fit uncert.", "*nofituncert/CombineMultiCrab*"),
              ("No syst. uncert.", "*nosystuncert/CombineMultiCrab*"),
        ]
        myOpts = expectedMedianOpts= {"ymin": 0.008, "ymax":1.0}

    doCompare("comparisonDummy", myList, opts,
              moveLegend={"dx":-0.04, "dy": 0.01},
              log=not opts.relative,
              expectedMedianOpts= myOpts,
              )

def compareInjected(opts, args):
    if len(args) == 0:
        print "Please give the list of multicrab directories as arguments"
        sys.exit(1)
    if opts.name is None:
        print "--name argument is missing"
        sys.exit(1)

    lst = []
    for d in args:
        f = open(os.path.join(d, "configuration.json"))
        conf = json.load(f)
        f.close()
        clsconf = conf["clsConfig"]
        label = "No injection"
        if "signalInjection" in clsconf:
            #label = "Injected m=%s, #it{B}(t#rightarrow^{}H^{+})=%s, #it{B}(^{}H^{+}#rightarrow#tau)=%s" % (
            label = "Injected m=%s, #it{B}_{t#rightarrowH^{+}}=%s, #it{B}_{H^{+}#rightarrow#tau}=%s" % (
                clsconf["signalInjection"]["mass"],
                clsconf["signalInjection"]["brTop"],
                clsconf["signalInjection"]["brHplus"])

        lst.append( (label, d) )

    histograms.createLegend.setDefaults(textSize=0.025)

    doCompare(opts.name, lst, opts,
              moveLegend={"dx":-0.04, "dy": 0.01}
              )


styleList = [styles.Style(24, ROOT.kBlack)] + styles.getStyles()

def _ifNotNone(value, default):
    if value is None:
        return default
    return value

def doCompare(name, compareList, opts, **kwargs):
    legendLabels = []
    limits = []
    for label, path in compareList:
        legendLabels.append(label)
        dirs = glob.glob(path)
        dirs.sort()
        if len(dirs) == 0:
            raise Exception("No directories for pattern '%s'" % path)
        directory = dirs[-1]
        print "Picked %s" % directory
        limits.append(limit.BRLimits(directory, excludeMassPoints=["155"]))

    doPlot2(limits, legendLabels, name)

    limitOpts = kwargs.get("limitOpts", {"ymax": _ifNotNone(opts.ymax, limits[0].getFinalstateYmaxBR())})
    expectedSigmaRelativeOpts = kwargs.get("expectedSigmaRelativeOpts", {"ymaxfactor": 1.2})
    moveLegend = kwargs.get("moveLegend", {})

    doPlot(limits, legendLabels, [l.observedGraph() for l in limits],
           name+"_observed", limit.BRlimit, opts=kwargs.get("observedOpts", limitOpts), moveLegend=moveLegend,
           plotLabel="Observed")

    doPlot(limits, legendLabels, [l.expectedGraph() for l in limits],
           name+"_expectedMedian", limit.BRlimit, opts=kwargs.get("expectedMedianOpts", limitOpts), moveLegend=moveLegend, log=kwargs.get("log",False),
           plotLabel="Expected median")

    if opts.relative:
        for i in range(1, len(limits)):
            limits[i].divideByLimit(limits[0])
        # Set reference to 1
        for j in range(0, len(limits[0].expectedMedian)):
            limits[0].expectedMedian[j] = 1.0
            limits[0].expectedMinus2[j] = 1.0
            limits[0].expectedMinus1[j] = 1.0
            limits[0].expectedPlus2[j] = 1.0
            limits[0].expectedPlus1[j] = 1.0
            limits[0].observed[j] = 1.0
        # Set y scale and require it to be linear
        kwargs["expectedMedianOptsRelative"] = {"ymin": 0.5, "ymax": _ifNotNone(opts.relativeYmax, 1.5)}
        kwargs["log"] = False
        doPlot(limits, legendLabels, [l.expectedGraph() for l in limits],
              name+"_expectedMedianRelative", opts.relativeYlabel, opts=kwargs.get("expectedMedianOptsRelative", limitOpts), moveLegend=moveLegend, log=kwargs.get("log",False),
              plotLabel="Expected median")
        print "Skipping +-1 and 2 sigma plots for --relative"
        sys.exit()

    if opts.relativePairs:
        if len(limits) % 2 != 0:
            print "Number of limits is not even!"
            sys.exit(1)
        divPoint = len(limits) / 2
        denoms = limits[:divPoint]
        numers = limits[divPoint:]
        for i in xrange(0, divPoint):
            numers[i].divideByLimit(denoms[i])
        doPlot(numers, legendLabels[:divPoint], [l.expectedGraph() for l in numers],
               name+"_expectedMedianRelative", opts.relativeYlabel, opts={"ymin": 0.5, "ymax": _ifNotNone(opts.relativeYmax, 1.5)},
               plotLabel="Expected median")
        print "Skipping +-1 and 2 sigma plots for --relativePairs"
        sys.exit()

    legendLabels2 = legendLabels + [None]*len(legendLabels)

    doPlot(limits, legendLabels2,
           [limit.divideGraph(l.expectedGraph(sigma=+1), l.expectedGraph()) for l in limits] +
           [limit.divideGraph(l.expectedGraph(sigma=-1), l.expectedGraph()) for l in limits],
           name+"_expectedSigma1Relative", "Expected #pm1#sigma / median", opts=kwargs.get("expectedSigma1RelativeOpts", expectedSigmaRelativeOpts), moveLegend=moveLegend,
           plotLabel="Expected #pm1#sigma / median")

    doPlot(limits, legendLabels2,
           [limit.divideGraph(l.expectedGraph(sigma=+2), l.expectedGraph()) for l in limits] +
           [limit.divideGraph(l.expectedGraph(sigma=-2), l.expectedGraph()) for l in limits],
           name+"_expectedSigma2Relative", "Expected #pm2#sigma / median", opts=kwargs.get("expectedSigma2RelativeOpts", expectedSigmaRelativeOpts), moveLegend=moveLegend,
           plotLabel="Expected #pm2#sigma / median")

    doPlot(limits, legendLabels2,
           [l.expectedGraph(sigma=+1) for l in limits] +
           [l.expectedGraph(sigma=-1) for l in limits],
           name+"_expectedSigma1", "Expected #pm1#sigma", opts=kwargs.get("expectedSigma1Opts", limitOpts), moveLegend=moveLegend,
           plotLabel="Expexted #pm1sigma")

    doPlot(limits, legendLabels2,
           [l.expectedGraph(sigma=+2) for l in limits] +
           [l.expectedGraph(sigma=-2) for l in limits],
           name+"_expectedSigma2", "Expected #pm2#sigma", opts=kwargs.get("expectedSigma2Opts", limitOpts), moveLegend=moveLegend,
           plotLabel="Expected #pm2sigma")

    # doPlot(limits, legendLabels,
    #        [limit.divideGraph(l.expectedGraph(sigma=+1), l.expectedGraph()) for l in limits]
    #        name+"_expectedSigma1Plus", "Expected +1#sigma / median", opts={"ymaxfactor": 1.2})

    # doPlot(limits, legendLabels,
    #        [limit.divideGraph(l.expectedGraph(sigma=+2), l.expectedGraph()) for l in limits]
    #        name+"_expectedSigma2Plus", "Expected +2#sigma / median", opts={"ymaxfactor": 1.2})

    # doPlot(limits, legendLabels,
    #        [limit.divideGraph(l.expectedGraph(sigma=-1), l.expectedGraph()) for l in limits],
    #        name+"_expectedSigma1Minus", "Expected -1#sigma / median", opts={"ymaxfactor": 1.2})

    # doPlot(limits, legendLabels,
    #        [limit.divideGraph(l.expectedGraph(sigma=-2), l.expectedGraph()) for l in limits],
    #        name+"_expectedSigma2Minus", "Expected -2#sigma / median", opts={"ymaxfactor": 1.2})


def doPlot(limits, legendLabels, graphs, name, ylabel, opts={}, plotLabel=None, moveLegend={}, log=False):
    hg = []
    ll = {}
    for i in xrange(len(graphs)):
        hg.append(histograms.HistoGraph(graphs[i], "Graph%d"%i, drawStyle="PL", legendStyle="lp"))
        ll["Graph%d"%i] = legendLabels[i]

    plot = plots.PlotBase(hg)
    plot.histoMgr.forEachHisto(styles.Generator(styleList[0:len(limits)]))
    def sty(h):
        r = h.getRootHisto()
        r.SetLineWidth(3)
        r.SetLineStyle(1)
    plot.histoMgr.forEachHisto(sty)
    plot.histoMgr.setHistoLegendLabelMany(ll)
    legend = histograms.createLegend(0.48, 0.65, 0.85, 0.92)
    if len(limits[0].getFinalstates()) > 1:
        legend = histograms.moveLegend(legend, dy=-0.1)
    if plotLabel:
        legend = histograms.moveLegend(legend, dy=-0.04)
    legend = histograms.moveLegend(legend, **moveLegend)
    plot.setLegend(legend)
    opts_ = {"ymin": 0}
    opts_.update(opts)
    plot.createFrame(name, opts=opts_)

    plot.frame.GetXaxis().SetTitle(limit.mHplus())
    plot.frame.GetYaxis().SetTitle(ylabel)

    ROOT.gPad.SetLogy(log)
    plot.draw()

    plot.setLuminosity(limits[0].getLuminosity())
    plot.addStandardTexts(cmsTextPosition="outframe")

    size = 20
    x = 0.18
    histograms.addText(x, 0.88, limit.process, size=size)
    histograms.addText(x, 0.84, limits[0].getFinalstateText(), size=size)
    histograms.addText(x, 0.79, limit.BRassumption, size=size)
    if plotLabel:
        histograms.addText(legend.GetX1()+0.01, legend.GetY2(), plotLabel, size=size)

    plot.save()

def doPlot2(limits, legendLabels, name):
    graphs = [
        histograms.HistoGraph(limits[0].expectedGraph(), "Expected", drawStyle="L"),
        histograms.HistoGraph(limits[0].expectedBandGraph(sigma=1), "Expected1", drawStyle="F", legendStyle="fl"),
        histograms.HistoGraph(limits[0].expectedBandGraph(sigma=2), "Expected2", drawStyle="F", legendStyle="fl"),
        ]
    graphs[0].getRootHisto().SetLineStyle(1)
    plot = plots.PlotBase(graphs)
    ll = {
        "Expected": None,
        "Expected1": "%s exp. median #pm 1#sigma" % legendLabels[0],
        "Expected2": "%s exp. median #pm 2#sigma" % legendLabels[0],
        }

    stGen = styles.generator()
    for i in xrange(1, len(limits)):
        gr = histograms.HistoGraph(limits[i].expectedGraph(), "Exp%d"%i, drawStyle="L")
        stGen(gr)
        gr.getRootHisto().SetLineWidth(3)
        gr.getRootHisto().SetLineStyle(1)
        plot.histoMgr.insertHisto(len(plot.histoMgr)-2, gr, legendIndex=len(plot.histoMgr))
        ll["Exp%d"%i] = "%s exp. median" % legendLabels[i]

    plot.histoMgr.setHistoLegendLabelMany(ll)

    legend = histograms.moveLegend(histograms.createLegend(0.48, 0.75, 0.85, 0.92), dx=-0.02)
    if len(limits[0].getFinalstates()) > 1:
        legend = histograms.moveLegend(legend, dy=-0.1)
    plot.setLegend(legend)

    plot.createFrame(name+"_limits", opts={"ymin": 0, "ymax": limits[0].getFinalstateYmaxBR()})
    plot.frame.GetXaxis().SetTitle(limit.mHplus())
    plot.frame.GetYaxis().SetTitle(limit.BRlimit)

    plot.draw()

    plot.setLuminosity(limits[0].getLuminosity())
    plot.addStandardTexts(cmsTextPosition="outframe")

    size = 20
    x = 0.2
    histograms.addText(x, 0.88, limit.process, size=size)
    histograms.addText(x, 0.84, limits[0].getFinalstateText(), size=size)
    histograms.addText(x, 0.79, limit.BRassumption, size=size)

    plot.save()


if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]",add_help_option=True,conflict_handler="resolve")
    parser.add_option("--light", dest="lightHplus", action="store_true", default=False, help="Light H+ comparison")
    parser.add_option("--heavy", dest="heavyHplus", action="store_true", default=False, help="Heavy H+ comparison")
    parser.add_option("--tailFit", dest="tailFit", action="store_true", default=False, help="tailFit comparison")
    parser.add_option("--relative", dest="relative", action="store_true", default=False, help="Do comparison relative to the first item")
    parser.add_option("--relativePairs", dest="relativePairs", action="store_true", default=False, help="Do multiple relative comparisons. The list of input directories is halved, the first half is the denominator and the second half is the numerator.")
    parser.add_option("--name", dest="name", type="string", default=None, help="Name of the output plot")
    parser.add_option("--ymax", dest="ymax", type="float", default=None, help="Maximum y-axis value for regular plots")
    parser.add_option("--relativeYmax", dest="relativeYmax", type="float", default=None, help="Maximum y-value for relative plots")
    parser.add_option("--relativeYlabel", dest="relativeYlabel", default="Expected limit vs. nominal", help="Y-axis title for relative plots")

    (opts, args) = parser.parse_args()

    main(opts, args)
