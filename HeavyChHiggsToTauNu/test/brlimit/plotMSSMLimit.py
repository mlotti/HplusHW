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

ROOT.gROOT.LoadMacro("LHCHiggsUtils.cc")

def usage():
    print
    print "### Usage:  ",sys.argv[0],"<root file>"
    print "### Example:",sys.argv[0],"mhmax.root"
    print
    sys.exit()
    
def main():
    if len(sys.argv) == 1:
        usage()

    rootfile = ""

    root_re = re.compile("(?P<rootfile>(\S*\.root))")
    match = root_re.search(sys.argv[1])
    if match:
        rootfile = match.group(0)

                                                                    
    limits = limit.BRLimits()

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    if limit.forPaper:
        histograms.cmsTextMode = histograms.CMSMode.PAPER

    # Get BR limits

    masses = limits.mass
    brs    = limits.observed

    #print masses,brs
    
    db = BRXSDB.BRXSDatabaseInterface(rootfile)
    for i,m in enumerate(masses):
        db.addExperimentalBRLimit(m,brs[i])


    graphs = {}
    obs = limits.observedGraph()
    graphs["obs"] = obs
    graphs["exp"] = limits.expectedGraph()
    graphs["exp1"] = limits.expectedBandGraph(sigma=1)
    graphs["exp2"] = limits.expectedBandGraph(sigma=2)

    # Remove m=80
    for gr in graphs.values():
        limit.cleanGraph(gr, minX=100)
        N = gr.GetN()
#        for i in range(gr.GetN()):
#            j = N - 1 - i
#            if gr.GetX()[j] > 154 and gr.GetX()[j] < 156:
#                gr.RemovePoint(j)
                
    # Get theory uncertainties on observed
    obs_th_plus = limit.getObservedPlus(obs)
    obs_th_minus = limit.getObservedMinus(obs)
    for gr in [obs_th_plus, obs_th_minus]:
        gr.SetLineWidth(3)
        gr.SetLineStyle(5)
#        gr.SetLineStyle(9)
    graphs["obs_th_plus"] = obs_th_plus
    graphs["obs_th_minus"] = obs_th_minus

    # Interpret in MSSM
    xVariable = "mHp"
    selection = "mu==200&&Xt==2000&&m2==200"

    for key in graphs.keys():
#        removeNotValid = not (key in ["exp1", "exp2"])
#        graphs[key] = limit.graphToTanBeta(graphs[key], mu, removeNotValid)
#        graphs[key] = db.graphToTanBeta(graphs[key],xVariable,selection)
        graphs[key] = db.graphToTanBetaCombined(graphs[key],xVariable,selection)
#        graphs[key] = db.graphToSharpTanbExclusion(graphs[key],xVariable,selection)

    graphs["mintanb"] = db.minimumTanbGraph("mHp",selection)
#    graphs["Allowed"] = db.mhLimit("mHp",selection,"125.9+-0.6+-0.2")
    graphs["Allowed"] = db.mhLimit("mHp",selection,"125.9+-3.0")
    
    doPlot("limitsTanb_mh", graphs, limits, limit.mHplus())

#    xVariable = "mA"
#    for key in graphs.keys():
#        graphs[key] = db.graphToTanBeta(graphs[key],xVariable,selection)
#    doPlot("limitsTanb_ma", graphs, limits, limit.mA())


    sys.exit()

#    # SUSY parameter variations (mu, Xt, m2, mgluino, mSUSY, read from the db)

    # x-axis and variation parameter definitions, y-axis=tanb
#    xVariable = "mu"
#    xLabel  = "#mu [GeV/c^{2}]"
    
    xVariable = "Xt"
    xLabel  = "X_{t} [GeV/c^{2}]"

#    xVariable = "m2"
#    xLabel  = "M_{2} [GeV/c^{2}]"

#    xVariable = "mGluino"
#    xLabel  = "m_{#tilde{g}} [GeV/c^{2}]"

#    xVariable = "mSUSY"
#    xLabel  = "M_{SUSY} [GeV/c^{2}]"

    variationVariable = "m_{H^{#pm}}"
    variationValues   = [100,120,140,150,155,160]
#    variationValues   = [100,120,140,150,160]
    variationSelection = "mHp==%s"
                    
    vgraphs = []
    for v in variationValues:
        selection = variationSelection%v
        xarray,tanbarray = db.getTanbLimits(xVariable,selection)
        vgraphs.append((ROOT.TGraph(len(xarray),array.array('d',xarray),array.array('d',tanbarray)),v))
                                
    def muStyle(h, markerStyle, lineStyle, color):
        rh = h.getRootHisto()
        rh.SetMarkerStyle(markerStyle)
        rh.SetMarkerColor(color)
        rh.SetLineStyle(lineStyle)
        rh.SetLineColor(color)
        rh.SetLineWidth(504)
        rh.SetFillStyle(3005)

    st = [lambda h: muStyle(h, 21, 1, 1),
          lambda h: muStyle(h, 20, 1, 4),
          lambda h: muStyle(h, 20, 2, 1),
          lambda h: muStyle(h, 21, 2, 4),
          lambda h: muStyle(h, 20, 3, 1),
          lambda h: muStyle(h, 21, 3, 4)]
    
    doPlotMu("limitsTanb_"+xVariable, vgraphs, st, limits, xLabel, variationVariable)

    
def doPlot(name, graphs, limits, xlabel):
    obs = graphs["obs"]
    excluded = ROOT.TGraph(obs)
    excluded.SetName("ExcludedArea")
    excluded.SetFillColor(ROOT.kGray)
#    excluded.SetPoint(excluded.GetN(), obs.GetX()[obs.GetN()-1], tanbMax)
#    excluded.SetPoint(excluded.GetN(), obs.GetX()[0], tanbMax)
    excluded.SetPoint(excluded.GetN(), 0, 1)
    excluded.SetPoint(excluded.GetN(), 0, tanbMax)
    excluded.SetPoint(excluded.GetN(), obs.GetX()[0], tanbMax)
    excluded.SetPoint(excluded.GetN(), obs.GetX()[0], obs.GetY()[0])
    """            
    excluded.SetPoint(excluded.GetN(), obs.GetX()[0], tanbMax)
    excluded.SetPoint(excluded.GetN(), 0, tanbMax)
    excluded.SetPoint(excluded.GetN(), 0, 1)
    excluded.SetPoint(excluded.GetN(), obs.GetX()[obs.GetN()-1], 1)
    """
    excluded.SetFillColor(ROOT.kGray)
    excluded.SetFillStyle(3354)
    excluded.SetLineWidth(0)
    excluded.SetLineColor(ROOT.kWhite)


    plot = plots.PlotBase([
            histograms.HistoGraph(graphs["obs"], "Observed", drawStyle="PL", legendStyle="lp"),
            histograms.HistoGraph(graphs["obs_th_plus"], "ObservedPlus", drawStyle="L", legendStyle="l"),
            histograms.HistoGraph(graphs["obs_th_minus"], "ObservedMinus", drawStyle="L"),
            histograms.HistoGraph(excluded, "Excluded", drawStyle="F", legendStyle="f"),
            histograms.HistoGraph(graphs["exp"], "Expected", drawStyle="L"),
            histograms.HistoGraph(graphs["Allowed"], "Allowed by \nm_{h} = 125.9#pm3.0 GeV/c^{2}", drawStyle="F", legendStyle="f"),
            histograms.HistoGraph(graphs["Allowed"], "AllowedCopy", drawStyle="L", legendStyle="f"),
            histograms.HistoGraph(graphs["mintanb"], "MinTanb", drawStyle="L"),
            histograms.HistoGraph(graphs["exp1"], "Expected1", drawStyle="F", legendStyle="fl"),
            histograms.HistoGraph(graphs["exp2"], "Expected2", drawStyle="F", legendStyle="fl"),
            ])

    plot.histoMgr.setHistoLegendLabelMany({
            "ObservedPlus": "Observed #pm1#sigma (th.)",
            "ObservedMinus": None,
            "Expected": None,
            "MinTanb": None,
            "AllowedCopy": None,
            "Expected1": "Expected median #pm 1#sigma",
            "Expected2": "Expected median #pm 2#sigma"
            })
#    plot.setLegend(histograms.createLegend(0.57, 0.155, 0.87, 0.355))
    plot.setLegend(histograms.createLegend(0.19, 0.60, 0.57, 0.80))
    plot.legend.SetFillColor(0)
    plot.legend.SetFillStyle(1001)
    plot.createFrame(name, opts={"ymin": 0, "ymax": tanbMax, "xmin": 100, "xmax": 160})
    plot.frame.GetXaxis().SetTitle(xlabel)
    plot.frame.GetYaxis().SetTitle(limit.tanblimit)

    plot.draw()

#    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
#    histograms.addLuminosityText(x=None, y=None, lumi=limits.getLuminosity())
    histograms.addLuminosityText(x=None, y=None, lumi="2.3-4.9")

    size = 20
    x = 0.2
    histograms.addText(x, 0.9, limit.process, size=size)
    histograms.addText(x, 0.863, limits.getFinalstateText(), size=size)
    histograms.addText(x, 0.815, "MSSM m_{h}^{max}", size=size)
#    histograms.addText(x, 0.775, limit.BRassumption, size=size)
#    histograms.addText(x, 0.735, "#mu=%d %s"%(mu, limit.massUnit()), size=size)
    histograms.addText(0.7, 0.23, "Min "+limit.BR+"(t#rightarrowH^{+}b)#times"+limit.BR+"(H^{+}#rightarrow#tau#nu)", size=0.5*size)

    #Adding a LHC label:
    ROOT.LHCHIGGS_LABEL(0.97,0.72,1)
    histograms.addText(x, 0.55, "FeynHiggs 2.9.4", size=size)
    histograms.addText(x, 0.48, "Derived from", size=size)
    histograms.addText(x, 0.43, "CMS HIG-12-052", size=size)
#    histograms.addText(x, 0.38, "JHEP07(2012)143", size=size)
                
    plot.save()

def doPlotMu(name, graphs, styleList, limits, xlabel, legendVariable):
    objs = []
    ll = {}
    for gr, mu in graphs:
        objs.append(histograms.HistoGraph(gr, "Obs%d"%mu, drawStyle="LP", legendStyle="lp"))
        ll["Obs%d"%mu] = "Observed, "+legendVariable+"=%d %s" % (mu, limit.massUnit())
        N = gr.GetN()
        for i in range(0,N):
            j = N - 1 - i
            if gr.GetY()[j] == 1:
                gr.RemovePoint(j)

    plot = plots.PlotBase(objs)
    plot.histoMgr.forEachHisto(styles.Generator(styleList))
    plot.histoMgr.setHistoLegendLabelMany(ll)
    plot.setLegend(histograms.moveLegend(histograms.createLegend(0.57, 0.155, 0.87, 0.355), dx=-0.1))

    plot.createFrame(name, opts={"ymin": 0, "ymax": tanbMax})
    plot.frame.GetXaxis().SetTitle(xlabel)
    plot.frame.GetXaxis().SetLabelSize(20)
    plot.frame.GetYaxis().SetTitle(limit.tanblimit)

    plot.draw()

#    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    histograms.addLuminosityText(x=None, y=None, lumi=limits.getLuminosity())

    size = 20
    x = 0.2
    histograms.addText(x, 0.9, limit.process, size=size)
    histograms.addText(x, 0.863, limits.getFinalstateText(), size=size)
    histograms.addText(x, 0.815, "MSSM m_{h}^{max}", size=size)
#    histograms.addText(x, 0.775, limit.BRassumption, size=size)

    histograms.addText(x, 0.72, "FeynHiggs 2.9.4", size=size)
    histograms.addText(x, 0.65, "Derived from", size=size)
    histograms.addText(x, 0.6, "CMS HIG-11-019", size=size)
    histograms.addText(x, 0.55, "JHEP07(2012)143", size=size)
    
    #Adding a LHC label:
    ROOT.LHCHIGGS_LABEL(0.97,0.72,1)
                    
    plot.save()


if __name__ == "__main__":
    main()
