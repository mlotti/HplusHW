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
#        obs_th_plus = limit.getObservedPlus(obs,0.21)
#        obs_th_minus = limit.getObservedMinus(obs,0.21)
#        for gr in [obs_th_plus, obs_th_minus]:
#            gr.SetLineWidth(2)
#            gr.SetLineStyle(9)
#        graphs["obs_th_plus"] = obs_th_plus
#        graphs["obs_th_minus"] = obs_th_minus
        

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
        if key == "obs":
            obsplus = db.getTheorUncert(graphs[key],xVariable,selection,"+")
            graphs["obs_th_plus"] = db.graphToTanBetaCombined(obsplus,xVariable,selection)
            obsminus = db.getTheorUncert(graphs[key],xVariable,selection,"-")
            graphs["obs_th_minus"] = db.graphToTanBetaCombined(obsminus,xVariable,selection)
        print key,"done"

    graphs["mintanb"] = db.minimumTanbGraph("mHp",selection)
    
    if scenario == "lowMH-LHCHXSWG":
	graphs["Allowed"] = db.mhLimit("mH","mHp",selection,"125.0+-3.0")
    else:
        graphs["Allowed"] = db.mhLimit("mh","mHp",selection,"125.0+-3.0")
    graphs["isomass"] = None
    
    limit.doTanBetaPlotLight("limitsTanb_light_"+scenario, graphs, limits.getLuminosity(), limits.getFinalstateText(), limit.mHplus(), scenario)

    # mH+ -> mA
    print "Replotting the graphs for (mA,tanb)"
    for key in graphs.keys():
        print key
        #db.PrintGraph(graphs[key])
        #print "check loop db.graphToMa"
        db.graphToMa(graphs[key])

    graphs["isomass"] = db.getIsoMass(160)

    limit.doTanBetaPlotLight("limitsTanb_mA_light_"+scenario, graphs, limits.getLuminosity(), limits.getFinalstateText(), limit.mA(), scenario)

if __name__ == "__main__":
    main()
