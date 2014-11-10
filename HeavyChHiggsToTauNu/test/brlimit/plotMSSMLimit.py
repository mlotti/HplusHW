#!/usr/bin/env python

import sys
import re
import array
import os

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.limit as limit
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.BRXSDatabaseInterface as BRXSDB

tanbMax = 65

ROOT.gROOT.LoadMacro("LHCHiggsUtils.C")

db = None

def usage():
    print
    print "### Usage:  ",sys.argv[0],"<root file> [<limits json>]"
    print "### Example:",sys.argv[0],"mhmax.root"
    print
    print "Note that because of transparent colors, the output will be PDF instead of EPS, and you need recent-enough ROOT"
    print
    sys.exit()
    
def main():
    if len(sys.argv) == 1:
        usage()

    rootfile = ""
    jsonfile = "limits.json"

    root_re = re.compile("(?P<rootfile>(\S*\.root))")
    json_re = re.compile("(?P<jsonfile>(\S*\.json))")
    for argv in sys.argv:
        match = root_re.search(argv)
        if match:
            rootfile = match.group(0)
        match = json_re.search(argv)
        if match:
            jsonfile = match.group(0)

    limits = limit.BRLimits(limitsfile=jsonfile,configfile="limitdata/lightHplus_configuration.json")

    # Enable OpenGL
    ROOT.gEnv.SetValue("OpenGL.CanvasPreferGL", 1)

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    if limit.forPaper:
        histograms.cmsTextMode = histograms.CMSMode.PAPER
    #histograms.cmsTextMode = histograms.CMSMode.PAPER # tmp
    #histograms.cmsTextMode = histograms.CMSMode.UNPUBLISHED # tmp
    limit.forPaper = True # to get GeV without c^2

    # Get BR limits

    masses = limits.mass
    brs    = limits.observed

    print "Observed masses and BR's"
    for i in range(len(masses)):
        print "    ",masses[i],brs[i]

    global db
    db = BRXSDB.BRXSDatabaseInterface(rootfile)
    for i,m in enumerate(masses):
        db.addExperimentalBRLimit(m,brs[i])


    graphs = {}
    obs = limits.observedGraph()
    # Remove blinded obs points
    for i in reversed(range(0,obs.GetN())):
        if obs.GetY()[i] < 0.00000001:
            print "    REMOVING POINT",obs.GetY()[i]," corresponding mass=",obs.GetX()[i]
            obs.RemovePoint(i)
    print
    
    graphs["exp"] = limits.expectedGraph()
    graphs["exp1"] = limits.expectedBandGraph(sigma=1)
    graphs["exp2"] = limits.expectedBandGraph(sigma=2)

    if obs.GetN() > 0:
        graphs["obs"] = obs
        # Get theory uncertainties on observed
        obs_th_plus = limit.getObservedPlus(obs,0.21)
        obs_th_minus = limit.getObservedMinus(obs,0.21)
        for gr in [obs_th_plus, obs_th_minus]:
            gr.SetLineWidth(2)
            gr.SetLineStyle(9)
        graphs["obs_th_plus"] = obs_th_plus
        graphs["obs_th_minus"] = obs_th_minus
        

    # Remove m=80
    for gr in graphs.values():
        limit.cleanGraph(gr, minX=90)

    print "Plotting graphs"                    
    for key in graphs.keys():
        for i in range(graphs[key].GetN()):
            xs = graphs[key].GetX()
            ys = graphs[key].GetY()
            print "    ",key,xs[i],ys[i]
        print

    # Interpret in MSSM
    xVariable = "mHp"
#    selection = "mu==200"
    selection = "mHp > 0"
#    scenario = "MSSM m_{h}^{max}"
    scenario = os.path.split(rootfile)[-1].replace(".root","")

    for key in graphs.keys():
        print "Graph--------------------------------",key
        graphs[key] = db.graphToTanBetaCombined(graphs[key],xVariable,selection)
        print key,"done"

    graphs["mintanb"] = db.minimumTanbGraph("mHp",selection)
    
    if scenario == "lowMH-LHCHXSWG":
	graphs["Allowed"] = db.mhLimit("mH","mHp",selection,"125.0+-3.0")
    else:
        graphs["Allowed"] = db.mhLimit("mh","mHp",selection,"125.0+-3.0")
    graphs["isomass"] = None
    
    doPlot("limitsTanb_light_"+scenario, graphs, limits, limit.mHplus(),scenario)

    # mH+ -> mA
    print "Replotting the graphs for (mA,tanb)"
    for key in graphs.keys():
        print key
        #db.PrintGraph(graphs[key])
        #print "check loop db.graphToMa"
        db.graphToMa(graphs[key])

    graphs["isomass"] = db.getIsoMass(160)
    

    doPlot("limitsTanb_mA_light_"+scenario, graphs, limits, limit.mA(),scenario)

    
def doPlot(name, graphs, limits, xlabel, scenario, isMA=False):
    blinded = True
    if "obs" in graphs.keys():
        blinded = False

    higgs = "h"
    if scenario == "lowMH-LHCHXSWG":
	higgs = "H"
       
    if not blinded:    
        obs = graphs["obs"]
        excluded = ROOT.TGraph(obs)
        excluded.SetName("ExcludedArea")

        if "_mA_" in name:
            rightX = obs.GetX()[obs.GetN()-1]+100
            rightY = obs.GetY()[obs.GetN()-1]
            excluded.SetPoint(excluded.GetN(), rightX, rightY)
            excluded.SetPoint(excluded.GetN(), rightX, 1)
        else:
            excluded.SetPoint(excluded.GetN(), obs.GetX()[obs.GetN()-1], 1)
        excluded.SetPoint(excluded.GetN(), 0, 1)
        excluded.SetPoint(excluded.GetN(), 0, tanbMax)
        excluded.SetPoint(excluded.GetN(), obs.GetX()[0], tanbMax)
        excluded.SetPoint(excluded.GetN(), obs.GetX()[0], obs.GetY()[0])

        limit.setExcludedStyle(excluded)
        excluded.SetLineWidth(0)
        excluded.SetLineColor(ROOT.kBlack)

    expected = graphs["exp"]
    expected.SetLineStyle(2)
    expected1 = graphs["exp1"]
    expected1.SetLineStyle(2)
    expected2 = graphs["exp2"]
    expected2.SetLineStyle(2)

    allowed = graphs["Allowed"]
    allowed.SetFillStyle(3005)
    allowed.SetFillColor(ROOT.kRed)
    allowed.SetLineWidth(-302)
    allowed.SetLineColor(ROOT.kRed)
    allowed.SetLineStyle(1)

    if not blinded:
        graphs["obs_th_plus"].SetLineStyle(9)
#        graphs["obs_th_minus"].SetLineStyle(9)
        excludedCopy = excluded.Clone()
        excludedCopy.SetFillColorAlpha(ROOT.kWhite, 0.0) # actual color doesn't matter, want fully transparent
        plot = plots.PlotBase([
            histograms.HistoGraph(graphs["obs"], "Observed", drawStyle="PL", legendStyle="lp"),
            histograms.HistoGraph(graphs["obs_th_plus"], "ObservedPlus", drawStyle="L", legendStyle="l"),
            histograms.HistoGraph(graphs["obs_th_minus"], "ObservedMinus", drawStyle="L"),
            histograms.HistoGraph(graphs["isomass"], "IsoMass", drawStyle="L"),
            histograms.HistoGraph(graphs["isomass"], "IsoMassCopy", drawStyle="F"),
            histograms.HistoGraph(excluded, "Excluded", drawStyle="F", legendStyle=None),
            histograms.HistoGraph(excludedCopy, "ExcludedCopy", drawStyle=None, legendStyle="f"),
            histograms.HistoGraph(expected, "Expected", drawStyle="L"),
#            histograms.HistoGraph(graphs["exp"], "Expected", drawStyle="L"),
            histograms.HistoGraph(graphs["Allowed"], "Allowed", drawStyle="L", legendStyle="lf"),
#            histograms.HistoGraph(graphs["Allowed"], "AllowedCopy", drawStyle="L", legendStyle="f"),
            histograms.HistoGraph(graphs["mintanb"], "MinTanb", drawStyle="L"),
#            histograms.HistoGraph(graphs["exp1"], "Expected1", drawStyle="F", legendStyle="fl"),
#            histograms.HistoGraph(graphs["exp2"], "Expected2", drawStyle="F", legendStyle="fl"),
            histograms.HistoGraph(expected1, "Expected1", drawStyle="F", legendStyle="fl"),
            histograms.HistoGraph(expected2, "Expected2", drawStyle="F", legendStyle="fl")
           ],
           saveFormats=[".png", ".pdf", ".C"]
        )

        plot.histoMgr.setHistoLegendLabelMany({
            "ObservedPlus": "Observed #pm1#sigma (th.)",
            "ObservedMinus": None,
            "Excluded": None,
            "ExcludedCopy": "Excluded",
            "Expected": None,
            "MinTanb": None,
            "Allowed": "m_{"+higgs+"}^{MSSM} #neq 125#pm3 GeV",
            "Expected1": "Expected median #pm 1#sigma",
            "Expected2": "Expected median #pm 2#sigma",
            "IsoMass": None,
            "IsoMassCopy": None
            })
    else:
        if not graphs["isomass"] == None:
            graphs["isomass"].SetFillColor(0)
            graphs["isomass"].SetFillStyle(1)
        plot = plots.PlotBase([
            histograms.HistoGraph(expected, "Expected", drawStyle="L"),
            histograms.HistoGraph(graphs["isomass"], "IsoMass", drawStyle="L"),
            histograms.HistoGraph(graphs["isomass"], "IsoMassCopy", drawStyle="F"),
            histograms.HistoGraph(graphs["Allowed"], "Allowed", drawStyle="L", legendStyle="lf"),
#            histograms.HistoGraph(graphs["Allowed"], "AllowedCopy", drawStyle="L", legendStyle="f"),
            histograms.HistoGraph(graphs["mintanb"], "MinTanb", drawStyle="L"),
            histograms.HistoGraph(expected1, "Expected1", drawStyle="F", legendStyle="fl"),
            histograms.HistoGraph(expected2, "Expected2", drawStyle="F", legendStyle="fl"),
            ],
            saveFormats=[".png", ".pdf", ".C"]
        )

        plot.histoMgr.setHistoLegendLabelMany({
            "Expected": None,
            "MinTanb": None,
            "Allowed": "m_{"+higgs+"}^{MSSM} #neq 125#pm3 GeV",
            "Expected1": "Expected median #pm 1#sigma",
            "Expected2": "Expected median #pm 2#sigma",
            "IsoMass": None,
            "IsoMassCopy": None
            })

    # Move the m_h,H allowed region to the last in the legend
    histoNames = [h.getName() for h in plot.histoMgr.getHistos()]
    plot.histoMgr.reorderLegend(filter(lambda n: "Allowed" not in n, histoNames))

    size = 20
    x = 0.2
    dy = -0.15
    plot.setLegend(histograms.createLegend(x-0.01, 0.50+dy, x+0.45, 0.80+dy))
    plot.legend.SetMargin(0.17)
 #    plot.legend.SetFillColor(0)
    #plot.legend.SetFillColorAlpha(ROOT.kWhite, 50)
#    plot.legend.SetFillStyle(1001)
    if blinded:
	name += "_blinded"
    name = os.path.basename(name)
    name = name.replace("-","_")
    frameXmax = 160
    if "_mA_" in name:
        frameXmax = 145
    plot.createFrame(name, opts={"ymin": 0, "ymax": tanbMax, "xmin": 90, "xmax": frameXmax})
    plot.frame.GetXaxis().SetTitle(xlabel)
    plot.frame.GetYaxis().SetTitle(limit.tanblimit)

    plot.draw()

    plot.setLuminosity(limits.getLuminosity())
    plot.addStandardTexts()

    histograms.addText(x, 0.9+dy, limit.process, size=size)
    histograms.addText(x, 0.863+dy, limits.getFinalstateText(), size=size)
    histograms.addText(x, 0.815+dy, limit.getTypesetScenarioName(scenario), size=size)
    #histograms.addText(0.2, 0.231, "Min "+limit.BR+"(t#rightarrowH^{+}b)#times"+limit.BR+"(H^{+}#rightarrow#tau#nu)", size=0.5*size)

    # Too small to be visible
#    if not graphs["isomass"] == None:
#        histograms.addText(0.8, 0.15, "m_{H^{#pm}} = 160 GeV", size=0.5*size)

    #Adding a LHC label:
#    ROOT.LHCHIGGS_LABEL(0.97,0.72,1)
    #FH_version = db.getVersion("FeynHiggs")
    #histograms.addText(x, 0.55+dy, FH_version, size=size)
#    HD_version = db.getVersion("HDECAY")
#    histograms.addText(x, 0.55, FH_version+" and "+HD_version, size=size)
#    histograms.addText(x, 0.48, "Derived from", size=size)
#    histograms.addText(x, 0.43, "CMS HIG-12-052", size=size)



    plot.save()

    print "Created",name
    
if __name__ == "__main__":
    main()
