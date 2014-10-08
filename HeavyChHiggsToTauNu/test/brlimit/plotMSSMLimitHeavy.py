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
                                                                                
#    limits = limit.BRLimits(limitsfile=jsonfile,configfile="configurationHeavy.json")
    limits = limit.BRLimits(limitsfile=jsonfile,configfile="limitdata/heavyHplus_configuration.json")

    # Enable OpenGL
    ROOT.gEnv.SetValue("OpenGL.CanvasPreferGL", 1)

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    if limit.forPaper:
        histograms.cmsTextMode = histograms.CMSMode.PAPER
    limit.forPaper = True # to get GeV without c^2

    # Get BR limits

    masses = limits.mass
    brs    = limits.observed

    print "Observed masses and sigma*BR's"
    for i in range(len(masses)):
        print "    ",masses[i],brs[i]

    global db
    db = BRXSDB.BRXSDatabaseInterface(rootfile)
    db.BRvariable= "2*0.001*tHp_xsec*BR_Hp_taunu"  # XSEC only for H-, multiply with 2 to get H+ and H- ; multiply by 0.001 to fb -> pb
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
        obs_th_plus = limit.getObservedPlus(obs,0.32)
        obs_th_minus = limit.getObservedMinus(obs,0.32)
        for gr in [obs_th_plus, obs_th_minus]:
            gr.SetLineWidth(2)
            gr.SetLineStyle(9)
        graphs["obs_th_plus"] = obs_th_plus
        graphs["obs_th_minus"] = obs_th_minus

    # Remove m=180,190
#    for gr in graphs.values():
#        limit.cleanGraph(gr, minX=200)

    print "Plotting graphs"                    
    for key in graphs.keys():
        for i in range(graphs[key].GetN()):
            xs = graphs[key].GetX()
            ys = graphs[key].GetY()
            print "    ",key,xs[i],ys[i]
        print

    # Interpret in MSSM
    xVariable = "mHp"
    selection = "mHp > 0"
#    scenario = "MSSM m_{h}^{max}"
    scenario = os.path.split(rootfile)[-1].replace(".root","")
    print scenario

    for key in graphs.keys():
        print "Graph--------------------------------",key
        graphs[key] = db.graphToTanBeta(graphs[key],xVariable,selection,highTanbRegion=True)
        print key,"done"

#    graphs["mintanb"] = db.minimumTanbGraph("mHp",selection)
    if scenario == "lowMH-LHCHXSWG":
        graphs["Allowed"] = db.mhLimit("mH","mHp",selection,"125.0+-3.0")
    else:
        graphs["Allowed"] = db.mhLimit("mh","mHp",selection,"125.0+-3.0")
    graphs["isomass"] = None
    
    doPlot("limitsTanb_heavy_"+scenario, graphs, limits, limit.mHplus(),scenario)
	
    # mH+ -> mA
    print "Replotting the graphs for (mA,tanb)"
    for key in graphs.keys():
	print key
        #db.PrintGraph(graphs[key])
	#print "check loop db.graphToMa"
        db.graphToMa(graphs[key])

    graphs["isomass"] = db.getIsoMass(180)

    doPlot("limitsTanb_mA_heavy_"+scenario, graphs, limits, limit.mA(),scenario)	

    
def doPlot(name, graphs, limits, xlabel, scenario):
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

        for i in reversed(range(excluded.GetN())):
            if excluded.GetY()[i] > 99 and i+1 < excluded.GetN():
                excluded.RemovePoint(i+1)

#        excluded.SetPoint(excluded.GetN(), obs.GetX()[obs.GetN()-1], 100)
#        excluded.SetPoint(excluded.GetN(), 0, 100)
#        excluded.SetPoint(excluded.GetN(), 0, obs.GetY()[0])
        excluded.SetPoint(excluded.GetN(), 140, 65)
        excluded.SetPoint(excluded.GetN(), obs.GetX()[0], obs.GetY()[0])

        for i in range(excluded.GetN()):
            print "Excluded",excluded.GetX()[i],excluded.GetY()[i]

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
	graphs["obs_th_minus"].SetLineStyle(9)
        plot = plots.PlotBase([
            histograms.HistoGraph(graphs["obs"], "Observed", drawStyle="PL", legendStyle="lp"),
            histograms.HistoGraph(graphs["obs_th_plus"], "ObservedPlus", drawStyle="L", legendStyle="l"),
            histograms.HistoGraph(graphs["obs_th_minus"], "ObservedMinus", drawStyle="L"),
            histograms.HistoGraph(graphs["isomass"], "IsoMass", drawStyle="L"),
            histograms.HistoGraph(graphs["isomass"], "IsoMassCopy", drawStyle="F"),
            histograms.HistoGraph(excluded, "Excluded", drawStyle="F", legendStyle="f"),
            histograms.HistoGraph(expected, "Expected", drawStyle="L"),
            histograms.HistoGraph(graphs["Allowed"], "Allowed", drawStyle="L", legendStyle="lf"),
#            histograms.HistoGraph(graphs["Allowed"], "AllowedCopy", drawStyle="L", legendStyle="f"),
            histograms.HistoGraph(expected1, "Expected1", drawStyle="F", legendStyle="fl"),
            histograms.HistoGraph(expected2, "Expected2", drawStyle="F", legendStyle="fl"),
            ],
           saveFormats=[".png", ".pdf", ".C"]
        )

        plot.histoMgr.setHistoLegendLabelMany({
            "ObservedPlus": "Observed #pm1#sigma (th.)",
            "ObservedMinus": None,
            "Expected": None,
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
 #           histograms.HistoGraph(graphs["Allowed"], "Allowed by \nm_{h} = 125.9#pm3.0 GeV", drawStyle="F", legendStyle="f"),
            histograms.HistoGraph(graphs["isomass"], "IsoMass", drawStyle="L"),
            histograms.HistoGraph(graphs["isomass"], "IsoMassCopy", drawStyle="F"),
            histograms.HistoGraph(graphs["Allowed"], "Allowed", drawStyle="L", legendStyle="lf"),
#            histograms.HistoGraph(graphs["Allowed"], "AllowedCopy", drawStyle="L", legendStyle="f"),
            histograms.HistoGraph(expected1, "Expected1", drawStyle="F", legendStyle="fl"),
            histograms.HistoGraph(expected2, "Expected2", drawStyle="F", legendStyle="fl"),
            ],
           saveFormats=[".png", ".pdf", ".C"]
        )

        plot.histoMgr.setHistoLegendLabelMany({
            "Expected": None,
            "Allowed": "m_{"+higgs+"}^{MSSM} #neq 125#pm3 GeV",
            "Expected1": "Expected median #pm 1#sigma",
            "Expected2": "Expected median #pm 2#sigma",
            "IsoMass": None,
            "IsoMassCopy": None
            })

    # Move the m_h,H allowed region to the last in the legend
    histoNames = [h.getName() for h in plot.histoMgr.getHistos()]
    plot.histoMgr.reorderLegend(filter(lambda n: "Allowed" not in n, histoNames))

    x = 0.50
    y = -0.25
    if scenario.replace("-LHCHXSWG", "") in ["lightstop", "mhmaxup"]:
        y += 0.05
    plot.setLegend(histograms.createLegend(x-0.01, y+0.50, x+0.45, y+0.80))
    plot.legend.SetMargin(0.17)
    #plot.legend.SetFillColor(0)
    #plot.legend.SetFillStyle(1001)
    if blinded:
        name += "_blinded"
    name = os.path.basename(name)
    name = name.replace("-","_")

    frameXmin = 180
    if "_mA_" in name:
        frameXmin = 140
    plot.createFrame(name, opts={"ymin": 0, "ymax": tanbMax, "xmin": frameXmin, "xmax": 600})
    plot.frame.GetXaxis().SetTitle(xlabel)
    plot.frame.GetYaxis().SetTitle(limit.tanblimit)

    plot.draw()
    
    plot.setLuminosity(limits.getLuminosity())
    plot.addStandardTexts(cmsTextPosition="right")
#    histograms.addLuminosityText(x=None, y=None, lumi="2.3-4.9")


    size = 20
    histograms.addText(x, y+0.9, limit.processHeavy, size=size)
    histograms.addText(x, y+0.863, limits.getFinalstateText(), size=size)
    histograms.addText(x, y+0.815, limit.getTypesetScenarioName(scenario), size=size)
#    histograms.addText(0.2, 0.231, "Min "+limit.BR+"(t#rightarrowH^{+}b)#times"+limit.BR+"(H^{+}#rightarrow#tau#nu)", size=0.5*size)

    # Too small to be visible
#    if not graphs["isomass"] == None:
#        histograms.addText(0.2, 0.15, "m_{H^{#pm}} = 180 GeV/c^{2}", size=0.5*size)

    #Adding a LHC label:
#    ROOT.LHCHIGGS_LABEL(0.97,0.72,1)
    #FH_version = db.getVersion("FeynHiggs")
    #histograms.addText(x, y+0.55, FH_version, size=size)
#    HD_version = db.getVersion("HDECAY")
#    histograms.addText(x, y+0.55, FH_version+" and", size=size)
#    histograms.addText(x, y+0.50, HD_version, size=size)
#    histograms.addText(x, 0.48, "Derived from", size=size)
#    histograms.addText(x, 0.43, "CMS HIG-12-052", size=size)

    plot.save()

    print "Created",name
    
if __name__ == "__main__":
    main()
