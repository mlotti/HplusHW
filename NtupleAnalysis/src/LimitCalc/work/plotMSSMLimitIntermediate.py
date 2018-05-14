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
#    jsonfile = "limits_heavy2016.json"
#    jsonfile = "limits2016/limitsForMSSMplots_ICHEP_v3_heavy.json"
#    jsonfile = "limits2016/limits_heavy_20171011.json"
#    jsonfile = "limits2016/limits_heavy_180131.json"
#    jsonfile = "limits2016/limits_heavy_180318.json"
#    jsonfile = "limits2016/limits_int_180202.json"
    jsonfile = "limits2016/limits_int_180429.json"
#    limits = limit.BRLimits(limitsfile=jsonfile,configfile="configurationHeavy.json")
    limits = limit.BRLimits(limitsfile=jsonfile,configfile="limits2016/intermediateHplus_configuration.json")

    # Enable OpenGL
    ROOT.gEnv.SetValue("OpenGL.CanvasPreferGL", 1)

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    #if limit.forPaper:
    #    histograms.cmsTextMode = histograms.CMSMode.PAPER
    #histograms.cmsTextMode = histograms.CMSMode.PAPER # tmp
    #histograms.cmsTextMode = histograms.CMSMode.UNPUBLISHED # tmp
    histograms.cmsTextMode = histograms.CMSMode.PRELIMINARY
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
#        obs_th_plus = limit.getObservedPlus(obs,0.32)
#        obs_th_minus = limit.getObservedMinus(obs,0.32)
#        for gr in [obs_th_plus, obs_th_minus]:
#            gr.SetLineWidth(2)
#            gr.SetLineStyle(9)
#        graphs["obs_th_plus"] = obs_th_plus
#        graphs["obs_th_minus"] = obs_th_minus

    # Remove m=180,190
#    for gr in graphs.values():
#        limit.cleanGraph(gr, 750)
#        limit.cleanGraph(gr, 800)
#        limit.cleanGraph(gr, 1000)
#        limit.cleanGraph(gr, 1500)
#        limit.cleanGraph(gr, 2000)
#        limit.cleanGraph(gr, 2500)                
#        limit.cleanGraph(gr, 3000)


    print "Plotting graphs"                    
    for key in graphs.keys():
        for i in range(graphs[key].GetN()):
            xs = graphs[key].GetX()
            ys = graphs[key].GetY()
            print "    ",key,xs[i],ys[i]
        print

    # Interpret in MSSM
    xVariable = "mHp"
    selection = "mHp > 0 && mu==200"
#    selection = "mHp > 0 && mu==500"
#    scenario = "MSSM m_{h}^{max}"
    scenario = os.path.split(rootfile)[-1].replace(".root","")
    print scenario

    from JsonWriter import JsonWriter
    jsonWriter = JsonWriter()
    for key in graphs.keys():
        print "Graph--------------------------------",key
        graphs[key] = db.graphToTanBeta(graphs[key],xVariable,selection,highTanbRegion=True)
        #if key == "obs":
            #obsplus = db.getTheorUncert(graphs[key],xVariable,selection,"+")
            #graphs["obs_th_plus"] = db.graphToTanBeta(obsplus,xVariable,selection)
            #obsminus = db.getTheorUncert(graphs[key],xVariable,selection,"-")
            #graphs["obs_th_minus"] = db.graphToTanBeta(obsminus,xVariable,selection)
        print key,"done"
        jsonWriter.addGraph(key,graphs[key])

#    graphs["mintanb"] = db.minimumTanbGraph("mHp",selection)
    if scenario == "lowMH-LHCHXSWG":
        graphs["Allowed"] = db.mhLimit("mH","mHp",selection,"125.0+-3.0")
    else:
        graphs["Allowed"] = db.mhLimit("mh","mHp",selection+"&&mHp>175","125.0+-3.0")

    if scenario == "tauphobic-LHCHXSWG":
        # Fix a buggy second upper limit (the order of points is left to right, then right to left; remove further passes to fix the bug)
        decreasingStatus = False
        i = 0
        while i < graphs["Allowed"].GetN():
            removeStatus = False
            y = graphs["Allowed"].GetY()[i]
            if i > 0:
                if graphs["Allowed"].GetY()[i-1] - y < 0:
                    decreasingStatus = True
                else:
                    if decreasingStatus:
                        graphs["Allowed"].RemovePoint(i)
                        removeStatus = True
            if not removeStatus:
                i += 1
        #for i in range(0, graphs["Allowed"].GetN()):
            #print graphs["Allowed"].GetX()[i], graphs["Allowed"].GetY()[i]
        
#    del graphs["isomass"]

    jsonWriter.addGraph("Allowed",graphs["Allowed"])

    jsonWriter.addParameter("name","limitsTanb_intermediate_"+scenario)
    jsonWriter.addParameter("scenario",scenario)
    jsonWriter.addParameter("luminosity",limits.getLuminosity())
    jsonWriter.addParameter("finalStateText",limits.getFinalstateText())
    jsonWriter.addParameter("mHplus",limit.mHplus())
    jsonWriter.addParameter("selection",selection)
    jsonWriter.addParameter("regime","heavy")
    jsonWriter.write("MSSMLimitIntermediate_"+scenario+".json")

    limit.doTanBetaPlotHeavy("limitsTanb_heavy_"+scenario, graphs, limits.getLuminosity(), limits.getFinalstateText(), limit.mHplus(), scenario)
    sys.exit()	
 
   # mH+ -> mA
    print "Replotting the graphs for (mA,tanb)"
    for key in graphs.keys():
	print key
        #db.PrintGraph(graphs[key])
	#print "check loop db.graphToMa"
        db.graphToMa(graphs[key])

    graphs["isomass"] = db.getIsoMass(200)

#    doPlot("limitsTanb_mA_heavy_"+scenario, graphs, limits, limit.mA(),scenario)
    
    limit.doTanBetaPlotHeavy("limitsTanb_mA_heavy_"+scenario, graphs, limits.getLuminosity(), limits.getFinalstateText(), limit.mA(), scenario)

if __name__ == "__main__":
    main()
