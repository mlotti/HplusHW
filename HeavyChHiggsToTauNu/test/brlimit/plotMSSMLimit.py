#!/usr/bin/env python

import sys
import re
import array

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

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    if limit.forPaper:
        histograms.cmsTextMode = histograms.CMSMode.PAPER

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
        obs_th_plus = limit.getObservedPlus(obs)
        obs_th_minus = limit.getObservedMinus(obs)
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
    selection = "mu==200"
#    scenario = "MSSM m_{h}^{max}"
    scenario = rootfile.replace(".root","")

    for key in graphs.keys():
        print "Graph--------------------------------",key
        graphs[key] = db.graphToTanBetaCombined(graphs[key],xVariable,selection)
        print key,"done"

    graphs["mintanb"] = db.minimumTanbGraph("mHp",selection)
    graphs["Allowed"] = db.mhLimit("mh","mHp",selection,"125.9+-3.0")
    
    doPlot("limitsTanb_light_"+scenario, graphs, limits, limit.mHplus(),scenario)

    # mH+ -> mA
    print "Replotting the graphs for (mA,tanb)"
    for key in graphs.keys():
        print key
        #db.PrintGraph(graphs[key])
        #print "check loop db.graphToMa"
        db.graphToMa(graphs[key])
    doPlot("limitsTanb_mA_light_"+scenario, graphs, limits, limit.mA(),scenario)

    sys.exit()

    
def doPlot(name, graphs, limits, xlabel, scenario):
    blinded = True
    if "obs" in graphs.keys():
        blinded = False
        
    if not blinded:    
        obs = graphs["obs"]
        excluded = ROOT.TGraph(obs)
        excluded.SetName("ExcludedArea")
        excluded.SetFillColor(ROOT.kGray)

        excluded.SetPoint(excluded.GetN(), obs.GetX()[obs.GetN()-1], 1)
        excluded.SetPoint(excluded.GetN(), 0, 1)
        excluded.SetPoint(excluded.GetN(), 0, tanbMax)
        excluded.SetPoint(excluded.GetN(), obs.GetX()[0], tanbMax)
        excluded.SetPoint(excluded.GetN(), obs.GetX()[0], obs.GetY()[0])

        excluded.SetFillColor(ROOT.kGray)
        excluded.SetFillStyle(3354)
        excluded.SetLineWidth(0)
        excluded.SetLineColor(ROOT.kWhite)

    expected = graphs["exp"]
    expected.SetLineStyle(2)
    expected1 = graphs["exp1"]
    expected1.SetLineStyle(2)
    expected2 = graphs["exp2"]
    expected2.SetLineStyle(2)

    if not blinded:
        graphs["obs_th_plus"].SetLineStyle(9)
        graphs["obs_th_minus"].SetLineStyle(9)
        plot = plots.PlotBase([
            histograms.HistoGraph(graphs["obs"], "Observed", drawStyle="PL", legendStyle="lp"),
            histograms.HistoGraph(graphs["obs_th_plus"], "ObservedPlus", drawStyle="L", legendStyle="l"),
            histograms.HistoGraph(graphs["obs_th_minus"], "ObservedMinus", drawStyle="L"),
            histograms.HistoGraph(excluded, "Excluded", drawStyle="F", legendStyle="f"),
            histograms.HistoGraph(expected, "Expected", drawStyle="L"),
#            histograms.HistoGraph(graphs["exp"], "Expected", drawStyle="L"),
            histograms.HistoGraph(graphs["Allowed"], "Allowed by \nm_{h} = 125.9#pm3.0 GeV/c^{2}", drawStyle="F", legendStyle="f"),
            histograms.HistoGraph(graphs["Allowed"], "AllowedCopy", drawStyle="L", legendStyle="f"),
            histograms.HistoGraph(graphs["mintanb"], "MinTanb", drawStyle="L"),
#            histograms.HistoGraph(graphs["exp1"], "Expected1", drawStyle="F", legendStyle="fl"),
#            histograms.HistoGraph(graphs["exp2"], "Expected2", drawStyle="F", legendStyle="fl"),
            histograms.HistoGraph(expected1, "Expected1", drawStyle="F", legendStyle="fl"),
            histograms.HistoGraph(expected2, "Expected2", drawStyle="F", legendStyle="fl"),
            ])

        plot.histoMgr.setHistoLegendLabelMany({
	    "Observed": "Observed",
            "ObservedPlus": "Observed #pm1#sigma (th.)",
            "ObservedMinus": None,
            "Expected": None,
            "MinTanb": None,
            "AllowedCopy": None,
            "Expected1": "Expected median #pm 1#sigma",
            "Expected2": "Expected median #pm 2#sigma"
            })
    else:
        plot = plots.PlotBase([
            histograms.HistoGraph(expected, "Expected", drawStyle="L"),
            histograms.HistoGraph(graphs["Allowed"], "Allowed by \nm_{h} = 125.9#pm3.0 GeV/c^{2}", drawStyle="F", legendStyle="f"),
            histograms.HistoGraph(graphs["Allowed"], "AllowedCopy", drawStyle="L", legendStyle="f"),
            histograms.HistoGraph(graphs["mintanb"], "MinTanb", drawStyle="L"),
            histograms.HistoGraph(expected1, "Expected1", drawStyle="F", legendStyle="fl"),
            histograms.HistoGraph(expected2, "Expected2", drawStyle="F", legendStyle="fl"),
            ])

        plot.histoMgr.setHistoLegendLabelMany({
            "Expected": None,
            "MinTanb": None,
            "AllowedCopy": None,
            "Expected1": "Expected median #pm 1#sigma",
            "Expected2": "Expected median #pm 2#sigma"
            })
        
    plot.setLegend(histograms.createLegend(0.19, 0.60, 0.57, 0.80))
    plot.legend.SetFillColor(0)
    plot.legend.SetFillStyle(1001)
    if blinded:
	name += "_blinded"
    name = name.replace("-","_")
    plot.createFrame(name, opts={"ymin": 0, "ymax": tanbMax, "xmin": 90, "xmax": 160})
    plot.frame.GetXaxis().SetTitle(xlabel)
    plot.frame.GetYaxis().SetTitle(limit.tanblimit)

    plot.draw()

    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
#    histograms.addLuminosityText(x=None, y=None, lumi="2.3-4.9")
    histograms.addLuminosityText(x=None, y=None, lumi="20")

    size = 20
    x = 0.2
    histograms.addText(x, 0.9, limit.process, size=size)
    histograms.addText(x, 0.863, limits.getFinalstateText(), size=size)
    histograms.addText(x, 0.815,scenario, size=size)
    histograms.addText(0.2, 0.231, "Min "+limit.BR+"(t#rightarrowH^{+}b)#times"+limit.BR+"(H^{+}#rightarrow#tau#nu)", size=0.5*size)

    #Adding a LHC label:
#    ROOT.LHCHIGGS_LABEL(0.97,0.72,1)
    FH_version = db.getVersion("FeynHiggs")
    histograms.addText(x, 0.55, FH_version)
#    HD_version = db.getVersion("HDECAY")
#    histograms.addText(x, 0.55, FH_version+" and "+HD_version, size=size)
#    histograms.addText(x, 0.48, "Derived from", size=size)
#    histograms.addText(x, 0.43, "CMS HIG-12-052", size=size)

    plot.save()

if __name__ == "__main__":
    main()
