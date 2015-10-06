#!/usr/bin/env python

import sys
import re
import array
import os

import ROOT
ROOT.gROOT.SetBatch(True)

import NtupleAnalysis.toolshistograms as histograms
import NtupleAnalysis.toolstdrstyle as tdrstyle
import NtupleAnalysis.toolsstyles as styles
import NtupleAnalysis.toolsplots as plots
import LimitCalc.limit as limit
import LimitCalc.BRXSDatabaseInterface as BRXSDB

tanbMax = 65

ROOT.gROOT.LoadMacro("LHCHiggsUtils.C")

db = None

def usage():
    print
    print "### Usage:  ",sys.argv[0],"<root file> [<limits json>]"
    print "### Example:",sys.argv[0],"mhmax.root"
    print
    sys.exit()

def mA110():
    x = []
    y = []
    x.append( 200.0 ); y.append( 0.5 )
    x.append( 300.0 ); y.append( 0.5 )
    x.append( 400.0 ); y.append( 0.5 )
    x.append( 500.0 ); y.append( 0.5 )
    x.append( 600.0 ); y.append( 0.5 )
    x.append( 700.0 ); y.append( 0.5 )
    x.append( 800.0 ); y.append( 0.5 )
    x.append( 900.0 ); y.append( 0.5 )
    x.append( 1000.0 ); y.append( 0.55 )
    x.append( 1100.0 ); y.append( 0.6 )
    x.append( 1200.0 ); y.append( 0.65 )
    x.append( 1300.0 ); y.append( 0.65 )
    x.append( 1400.0 ); y.append( 0.7 )
    x.append( 1500.0 ); y.append( 0.75 )
    x.append( 1600.0 ); y.append( 0.75 )
    x.append( 1700.0 ); y.append( 0.8 )
    x.append( 1800.0 ); y.append( 0.85 )
    x.append( 1900.0 ); y.append( 0.9 )
    x.append( 2000.0 ); y.append( 0.901581274101 )
    x.append( 2100.0 ); y.append( 0.95 )
    x.append( 2200.0 ); y.append( 1.0 )
    x.append( 2300.0 ); y.append( 1.1 )
    x.append( 2400.0 ); y.append( 1.1 )
    x.append( 2500.0 ); y.append( 1.2 )
    x.append( 2600.0 ); y.append( 1.2 )
    x.append( 2700.0 ); y.append( 1.3 )
    x.append( 2800.0 ); y.append( 1.30872271358 )
    x.append( 2900.0 ); y.append( 1.4014869111 )
    x.append( 3000.0 ); y.append( 1.5 )
    x.append( 3100.0 ); y.append( 1.56652290234 )
    x.append( 3200.0 ); y.append( 1.69188938707 )
    x.append( 3300.0 ); y.append( 1.81164924496 )
    x.append( 3300.0 ); y.append( 71.0 )
    x.append( 3200.0 ); y.append( 74.0 )
    x.append( 3100.0 ); y.append( 75.0 )
    x.append( 3000.0 ); y.append( 75.0 )
    x.append( 2900.0 ); y.append( 75.0 )
    x.append( 2800.0 ); y.append( 75.0 )
    x.append( 2700.0 ); y.append( 75.0 )
    x.append( 2600.0 ); y.append( 75.0 )
    x.append( 2500.0 ); y.append( 75.0 )
    x.append( 2400.0 ); y.append( 75.0 )
    x.append( 2300.0 ); y.append( 75.0 )
    x.append( 2200.0 ); y.append( 75.0 )
    x.append( 2100.0 ); y.append( 75.0 )
    x.append( 2000.0 ); y.append( 75.0 )
    x.append( 1900.0 ); y.append( 75.0 )
    x.append( 1800.0 ); y.append( 75.0 )
    x.append( 1700.0 ); y.append( 75.0 )
    x.append( 1600.0 ); y.append( 75.0 )
    x.append( 1500.0 ); y.append( 75.0 )
    x.append( 1400.0 ); y.append( 75.0 )
    x.append( 1300.0 ); y.append( 75.0 )
    x.append( 1200.0 ); y.append( 75.0 )
    x.append( 1100.0 ); y.append( 75.0 )
    x.append( 1000.0 ); y.append( 75.0 )
    x.append( 900.0 ); y.append( 75.0 )
    x.append( 800.0 ); y.append( 75.0 )
    x.append( 700.0 ); y.append( 75.0 )
    x.append( 600.0 ); y.append( 75.0 )
    x.append( 500.0 ); y.append( 75.0 )
    x.append( 400.0 ); y.append( 75.0 )
    x.append( 300.0 ); y.append( 75.0 )
    x.append( 200.0 ); y.append( 75.0 )
    x.append( 0 ); y.append( 75.0 )
    x.append( 200.0 ); y.append( 0.5 )


    retGraph = ROOT.TGraph(len(x),array.array('d',x,),array.array('d',y))
    retGraph.SetName("muLimit")
    retGraph.SetLineWidth(1)
    retGraph.SetLineStyle(7)
    retGraph.SetFillColor(8)
    retGraph.SetFillStyle(3008)
    return retGraph

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

    scenario = os.path.split(rootfile)[-1].replace(".root","")
    selection = ""
    masses_A = db.getValues("mA",selection)

    for i in range(len(masses_A)):
        mass = masses_A[i]

        if not mass == 110:
            continue
	selection = "mA == %s"%mass 
        db.selection = selection
#        graphs["Allowed"]  = db.mHLimit_mA("mH","mu",selection,"125.0+-3.0")

#        graphs["muexcluded"] = db.muLimit_mA(mass,"mu",selection)
        graphs["muexcluded"] = mA110()

        graphs["IsoMass120"] = db.getIsoMass(120,"mu")
#        graphs["IsoMass160"] = db.getIsoMass(160,"mu")
#        graphs["IsoMass165"] = db.getIsoMass(165,"mu")

        graphs["InAccessible"] = db.inaccessible("mu","")

        if int(mass) in [155, 160]:
            graphs["obs_th_plus"] = db.muLimit(mass,"mu",selection,brlimit*(1+0.29))
            graphs["obs_th_minus"] = db.muLimit(mass,"mu",selection,brlimit*(1-0.29))

            for gr in [graphs["obs_th_plus"], graphs["obs_th_minus"]]:
                gr.SetLineWidth(2)
                gr.SetLineStyle(9)

#            graphs["observed"] = graphs["muexcluded"].Clone()
#            graphs["observed"].SetLineWidth(2)
#            graphs["observed"].SetLineStyle(ROOT.kSolid)
#            graphs["observed"].SetLineColor(ROOT.kBlack)

            # Remove obs point
            for name in ["observed", "obs_th_plus", "obs_th_minus"]:
                gr = graphs[name]
                print "Graph", name
                for i in reversed(range(0,gr.GetN())):
                    if gr.GetY()[i] < 2 or gr.GetY()[i] > 65:
                        print "    REMOVING POINT",gr.GetY()[i]," corresponding mass=",gr.GetX()[i]
                        gr.RemovePoint(i)

        graphs["Allowed"]  = db.getHardCoded_mH_limitForMu_mA(mass,0)
        graphs["Allowed2"] = db.getHardCoded_mH_limitForMu_mA(mass,1)

        doPlot(("limitsMu_light_mA%s_"+scenario)%(int(mass)), graphs, limits, "#mu (GeV)",scenario, int(mass))
    sys.exit()

    
def doPlot(name, graphs, limits, xlabel, scenario, mass):

    higgs = "h"
    if "lowMH" in scenario:
	higgs = "H"
       
    excluded = graphs["muexcluded"]
    limit.setExcludedStyle(excluded)
    excluded.SetFillStyle(1001)
    excluded.SetLineWidth(0)
    excluded.SetLineStyle(0)
    excluded.SetLineColor(ROOT.kWhite)
    excludedCopy = excluded.Clone()
    if not mass in [90]:
        excludedCopy.SetFillColorAlpha(ROOT.kWhite, 0.0) # actual color doesn't matter, want fully transparent
    else:
        excluded.SetLineColor(ROOT.kBlack)


    # Uncomment when we have allowed
    for n in ["Allowed", "Allowed2"]:
        a = graphs[n]
        if a is None:
            continue
        a.SetFillStyle(3005)
        a.SetFillColor(ROOT.kRed)
        a.SetLineWidth(-302)
        a.SetLineColor(ROOT.kRed)
        a.SetLineStyle(1)

    legend_dh = 0
    grs = []
    if "observed" in graphs:
        grs.extend([
            histograms.HistoGraph(graphs["observed"], "Observed", drawStyle="L", legendStyle="l"),
            histograms.HistoGraph(graphs["obs_th_plus"], "ObservedPlus", drawStyle="L", legendStyle="l"),
            histograms.HistoGraph(graphs["obs_th_minus"], "ObservedMinus", drawStyle="L", legendStyle=None),
            ])
        legend_dh = 0.1
    grs.extend([
        histograms.HistoGraph(excluded, "Excluded", drawStyle="F"),
        histograms.HistoGraph(excludedCopy, "ExcludedCopy", drawStyle=None, legendStyle="f"),
        histograms.HistoGraph(graphs["Allowed"], "Allowed", drawStyle="L", legendStyle="lf"),
#        histograms.HistoGraph(graphs["IsoMass120"], "IsoMass120", drawStyle="L", legendStyle="lf"),
#        histograms.HistoGraph(graphs["IsoMass160"], "IsoMass160", drawStyle="L", legendStyle="lf"),
#        histograms.HistoGraph(graphs["IsoMass165"], "IsoMass165", drawStyle="L", legendStyle="lf"),
        histograms.HistoGraph(graphs["InAccessible"], "InAccessible", drawStyle="F", legendStyle="lf"),
    ])
    if graphs["Allowed2"] is not None:
        grs.append(histograms.HistoGraph(graphs["Allowed2"], "Allowed2", drawStyle="L", legendStyle=None))


    plot = plots.PlotBase(grs, saveFormats=[".png", ".pdf", ".C"])

    plot.histoMgr.setHistoLegendLabelMany({
   	"ExcludedCopy": "Excluded",
        "Allowed": "m_{"+higgs+"}^{MSSM} #neq 125#pm3 GeV",
        "Excluded": None,
#        "IsoMass120": None,
#        "IsoMass160": None,
#        "IsoMass165": None,
        "InAccessible": "Inaccessible",
        })
    if "observed" in graphs:
        plot.histoMgr.setHistoLegendLabelMany({
            "ObservedPlus": "Observed #pm1#sigma (th.)",
        })

    textPos = "left"
    dx = 0
    dy = -0.15
    if mass in [90, 150]:
        textPos = "right"
        dx = 0.35
    if mass in [155, 160]:
        textPos = "right"
        dy = -0.02

    plot.setLegend(histograms.createLegend(0.19+dx, 0.75+dy-legend_dh, 0.57+dx, 0.80+dy))
    histograms.moveLegend(plot.legend, dh=0.05, dy=-0.05)
    #plot.legend.SetFillColor(0)
    #plot.legend.SetFillStyle(1001)

    name = name.replace("-","_")
    plot.createFrame(name, opts={"ymin": 0.5, "ymax": tanbMax, "xmin": 200, "xmax": 3300})
    plot.frame.GetXaxis().SetTitle(xlabel)
    plot.frame.GetYaxis().SetTitle(limit.tanblimit)
    ROOT.gPad.SetLogy(True)
    plot.draw()

    plot.setLuminosity(limits.getLuminosity())
    plot.addStandardTexts(cmsTextPosition=textPos)

    size = 20
    x = 0.2+dx
    histograms.addText(x, 0.9+dy, limit.process, size=size)
    histograms.addText(x, 0.863+dy, limits.getFinalstateText(), size=size)
    histograms.addText(x, 0.815+dy, limit.getTypesetScenarioName(scenario.replace("_mu", "")), size=size)
    histograms.addText(x, 0.767+dy, "m_{A}=%d GeV" % mass, size=size)
#    histograms.addText(0.2, 0.231, "Min "+limit.BR+"(t#rightarrowH^{+}b)#times"+limit.BR+"(H^{+}#rightarrow#tau#nu)", size=0.5*size)


    #Adding a LHC label:
#    ROOT.LHCHIGGS_LABEL(0.97,0.72,1)
#    FH_version = db.getVersion("FeynHiggs")
#    histograms.addText(x, 0.55, FH_version)
#    HD_version = db.getVersion("HDECAY")
#    histograms.addText(x, 0.55, FH_version+" and "+HD_version, size=size)
#    histograms.addText(x, 0.48, "Derived from", size=size)
#    histograms.addText(x, 0.43, "CMS HIG-12-052", size=size)

    plot.save()

    print "Created",name
    
if __name__ == "__main__":
    main()
