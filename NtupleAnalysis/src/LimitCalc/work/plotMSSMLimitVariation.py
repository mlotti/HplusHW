#!/usr/bin/env python

import sys
import re
import array

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.styles as styles
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.LimitCalc.limit as limit
import HiggsAnalysis.LimitCalc.BRXSDatabaseInterface as BRXSDB

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

    

#    # SUSY parameter variations (mu, Xt, m2, mgluino, mSUSY, read from the db)

    xVariable = "mHp"
    xLabel  = "m_{H^{+}} [GeV/c^{2}]"
#    variationVariable = "mu"
#    variationLabel    = "#mu"
#    variationValues   = [-1000,-200,200,1000]
#    variationVariable = "mSUSY"
#    variationLabel    = "M_{SUSY}"
#    variationValues   = [500,1000,2000]
#    variationVariable = "mGluino"
#    variationLabel    = "m_{#tilde{g}}"
#    variationValues   = [200,800,2000]
#    variationVariable = "m2"
#    variationLabel    = "M_{2}"
#    variationValues   = [200,1000]
    variationVariable = "Xt"
    variationLabel    = "X_{t}"
    variationValues   = [-2000,2000]

    variationSelection = "mHp>99&&"+variationVariable+"==%s"    
    plot(db,limits,xVariable,xLabel,variationVariable,variationLabel,variationValues,variationSelection)

    # x-axis and variation parameter definitions, y-axis=tanb
#    xVariable = "mu"
#    xLabel  = "#mu [GeV/c^{2}]"
    
#    xVariable = "Xt"
#    xLabel  = "X_{t} [GeV/c^{2}]"

#    xVariable = "m2"
#    xLabel  = "M_{2} [GeV/c^{2}]"

#    xVariable = "mGluino"
#    xLabel  = "m_{#tilde{g}} [GeV/c^{2}]"

#    xVariable = "mSUSY"
#    xLabel  = "M_{SUSY} [GeV/c^{2}]"

    xVariable = variationVariable
    xLabel    = variationLabel+" [GeV/c^{2}]"

    variationVariable = "m_{H^{#pm}}"
    variationValues   = [100,120,140,150,155,160]
#    variationValues   = [140]
    variationSelection = "mHp==%s"

    plot(db,limits,xVariable,xLabel,variationVariable,variationLabel,variationValues,variationSelection)


def plot(db,limits,xVariable,xLabel,variationVariable,variationLabel,variationValues,variationSelection):
                    
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
    varName = variationVariable
    if varName == "m_{H^{#pm}}":
        varName = "mHp"
    doPlotMu("limitVariation_"+xVariable+"_tanb_"+varName, vgraphs, st, limits, xLabel, xVariable, variationLabel)


def doPlotMu(name, graphs, styleList, limits, xlabel, xvarName, legendVariable):
    objs = []
    ll = {}
    cutValue = 100 # for cutting a slice +- cutValue around 0 from the (mu,tanb) plot
    for gr, mu in graphs:
        if xvarName == "mu":
            histo = histograms.HistoGraph(gr, "Obs%d"%mu, drawStyle="LP", legendStyle="lp")
            plus  = gr.Clone()
            minus = gr.Clone()
            N = gr.GetN()
            for i in range(0,N):
                j = N - 1 - i
                x = gr.GetX()[j]
                if x > -cutValue:
                    minus.RemovePoint(j)
                if x < cutValue:
                    plus.RemovePoint(0)
            objs.append(histograms.HistoGraph(minus, "Obs%d"%mu, drawStyle="LP", legendStyle="lp"))
            objs.append(histograms.HistoGraph(plus, "ObsCopy%d"%mu, drawStyle="LP", legendStyle="lp"))
            ll["ObsCopy%d"%mu] = None
                
        else:
            objs.append(histograms.HistoGraph(gr, "Obs%d"%mu, drawStyle="LP", legendStyle="lp"))
        ll["Obs%d"%mu] = "Observed, "+legendVariable+"=%d %s" % (mu, limit.massUnit())
#        N = gr.GetN()
#        for i in range(0,N):
#            j = N - 1 - i
#            if gr.GetY()[j] == 1:
#                gr.RemovePoint(j)

    plot = plots.PlotBase(objs)
    if xvarName == "mu":
        doubleStyleList = []
        for style in styleList:
            doubleStyleList.append(style)
            doubleStyleList.append(style)
        plot.histoMgr.forEachHisto(styles.Generator(doubleStyleList))
    else:
        plot.histoMgr.forEachHisto(styles.Generator(styleList))
    plot.histoMgr.setHistoLegendLabelMany(ll)
    plot.setLegend(histograms.moveLegend(histograms.createLegend(0.57, 0.155, 0.87, 0.355), dx=-0.1))

    plot.createFrame(name, opts={"ymin": 0, "ymax": tanbMax})
    plot.frame.GetXaxis().SetTitle(xlabel)
    plot.frame.GetXaxis().SetLabelSize(20)
    plot.frame.GetYaxis().SetTitle(limit.tanblimit)

    plot.draw()

    plot.setLuminosity(limits.getLuminosity())
    plot.addStandardTexts()

    size = 20
    x = 0.2
    histograms.addText(x, 0.9, limit.process, size=size)
    histograms.addText(x, 0.863, limits.getFinalstateText(), size=size)
    histograms.addText(x, 0.815, "MSSM m_{h}^{max}", size=size)
#    histograms.addText(x, 0.775, limit.BRassumption, size=size)

    histograms.addText(x, 0.72, "FeynHiggs 2.9.4", size=size)
    histograms.addText(x, 0.65, "Derived from", size=size)
    histograms.addText(x, 0.6, "CMS HIG-12-052", size=size)
#    histograms.addText(x, 0.6, "CMS HIG-11-019", size=size)
#    histograms.addText(x, 0.55, "JHEP07(2012)143", size=size)
    
    #Adding a LHC label:
    ROOT.LHCHIGGS_LABEL(0.97,0.72,1)
                    
    plot.save()

    print
    print "Plotting",name
    print

if __name__ == "__main__":
    main()
