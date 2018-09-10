#!/usr/bin/env python

import sys
import re
import array
import os

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.styles as styles
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.LimitCalc.limit as limit
import HiggsAnalysis.LimitCalc.BRXSDatabaseInterface as BRXSDB

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

    jsonfile = "limits2016/limits_withLeptonic_180522.json"
    limits = limit.BRLimits(limitsfile=jsonfile,configfile="limits2016/mu_configuration.json")

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
    db = BRXSDB.BRXSDatabaseInterface(rootfile,BRvariable= "0.001*831.76*2*tHp_xsec*BR_Hp_taunu")
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

#    graphs["exp"] = limits.expectedGraph()
    #x = array.array('d',masses)
    #y = array.array('d',[0.02]*len(masses))
    #graphs["exp"] = ROOT.TGraph(len(masses),x,y)
#    graphs["exp1"] = limits.expectedBandGraph(sigma=1)
#    graphs["exp2"] = limits.expectedBandGraph(sigma=2)

    if obs.GetN() > 0:
        graphs["obs"] = obs



    # Remove m=80
    for gr in graphs.values():
        limit.cleanGraph(gr, 80)

    print "Plotting graphs"
    for key in graphs.keys():
        for i in range(graphs[key].GetN()):
            xs = graphs[key].GetX()
            ys = graphs[key].GetY()
            print "    ",key,xs[i],ys[i]
        print

    # Interpret in MSSM
    xVariable = "mu"
    scenario = os.path.split(rootfile)[-1].replace(".root","")
    if scenario == "lowMHaltv-LHCHXSWG":
        xVariable = "mHp"
    selection = ""
    from JsonWriter import JsonWriter
#    for i in range(len(masses)):
#        mass = masses[i]
#        brlimit = brs[i]
#	if mass < 90:
#	    continue 
#        if not mass == 160:
#            continue
#	selection = "mHp == %s"%mass 
        #graphs["muexcluded"] = db.muLimit(mass,"mu",selection,brlimit)
        #db.PrintGraph(graphs["muexcluded"],"muexcluded")

    jsonWriter = JsonWriter()
    print "check keys",graphs.keys()

    for key in graphs.keys():
        print "Graph--------------------------------",key
        #db.PrintGraph(graphs[key],"Before graphToTanBetaCombined")
        graphs[key] = db.graphToTanBetaMu(graphs[key],xVariable,selection,True)
        print key,"done"
        jsonWriter.addGraph(key,graphs[key])

    #graphs["Allowed"] = db.mhLimit("mH","mu",selection,"125.0+-3.0")
    if xVariable == "mHp":
        graphs["Allowed"] = db.mHLimit_mHp(selection,"125.0+-3.0")
    else:
        graphs["Allowed"] = db.mHLimit_mu(selection,"125.0+-3.0")
    jsonWriter.addGraph("Allowed",graphs["Allowed"])

    graphs["Inaccessible"] = db.inaccessible(xVariable,selection)
    jsonWriter.addGraph("Inaccessible",graphs["Inaccessible"])
    
    jsonWriter.addParameter("name","limitsTanb_light_"+scenario)
    jsonWriter.addParameter("scenario",scenario)
    jsonWriter.addParameter("luminosity",limits.getLuminosity())
    jsonWriter.addParameter("finalStateText",limits.getFinalstateText())
    xvar = limit.mu()
    if xVariable == "mHp":
        xvar = limit.mHplus()
    jsonWriter.addParameter("mHplus",xvar)
    jsonWriter.addParameter("selection",selection)
    jsonWriter.addParameter("regime","mu")
    jsonWriter.write("MSSMLimitMu_"+scenario+".json")

        #limit.doTanBetaPlotLight("limitsTanb_light_"+scenario, graphs, limits.getLuminosity(), limits.getFinalstateText(), limit.mHplus(), scenario)
#        if int(mass) in [155, 160]:
#            graphs["obs_th_plus"] = db.muLimit(mass,"mu",selection,brlimit*(1+0.29))
#            graphs["obs_th_minus"] = db.muLimit(mass,"mu",selection,brlimit*(1-0.29))
#
#            for gr in [graphs["obs_th_plus"], graphs["obs_th_minus"]]:
#                gr.SetLineWidth(2)
#                gr.SetLineStyle(9)
#
#            graphs["observed"] = graphs["muexcluded"].Clone()
#            graphs["observed"].SetLineWidth(2)
#            graphs["observed"].SetLineStyle(ROOT.kSolid)
#            graphs["observed"].SetLineColor(ROOT.kBlack)
#
#            # Remove obs point
#            for name in ["observed", "obs_th_plus", "obs_th_minus"]:
#                gr = graphs[name]
#                print "Graph", name
#                for i in reversed(range(0,gr.GetN())):
#                    if gr.GetY()[i] < 2 or gr.GetY()[i] > 65:
#                        print "    REMOVING POINT",gr.GetY()[i]," corresponding mass=",gr.GetX()[i]
#                        gr.RemovePoint(i)
#
#        graphs["Allowed"]  = db.getHardCoded_mH_limitForMu(mass,0)
#        graphs["Allowed2"] = db.getHardCoded_mH_limitForMu(mass,1)
#
#        doPlot(("limitsMu_light_mHp%s_"+scenario)%(int(mass)), graphs, limits, "#mu (GeV)",scenario, int(mass))
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
#    else:
#        excluded.SetLineColor(ROOT.kBlack)


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
    ])
    if graphs["Allowed2"] is not None:
        grs.append(histograms.HistoGraph(graphs["Allowed2"], "Allowed2", drawStyle="L", legendStyle=None))


    plot = plots.PlotBase(grs, saveFormats=[".png", ".pdf", ".C"])

    plot.histoMgr.setHistoLegendLabelMany({
   	"ExcludedCopy": "Excluded",
        "Allowed": "m_{"+higgs+"}^{MSSM} #neq 125#pm3 GeV",
        "Excluded": None,
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
    plot.createFrame(name, opts={"ymin": 0, "ymax": tanbMax, "xmin": 200, "xmax": 3300})
    plot.frame.GetXaxis().SetTitle(xlabel)
    plot.frame.GetYaxis().SetTitle(limit.tanblimit)

    plot.draw()

    plot.setLuminosity(limits.getLuminosity())
    plot.addStandardTexts(cmsTextPosition=textPos)

    size = 20
    x = 0.2+dx
    histograms.addText(x, 0.9+dy, limit.process, size=size)
    histograms.addText(x, 0.863+dy, limits.getFinalstateText(), size=size)
    histograms.addText(x, 0.815+dy, limit.getTypesetScenarioName(scenario.replace("_mu", "")), size=size)
    histograms.addText(x, 0.767+dy, "m_{H^{+}}=%d GeV" % mass, size=size)
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
