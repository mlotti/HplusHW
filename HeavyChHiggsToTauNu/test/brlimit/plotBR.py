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
#GeVUnit = "GeV/c^{2}"
GeVUnit = "GeV"

ROOT.gROOT.LoadMacro("LHCHiggsUtils.C")

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
    
    xvar = "mHp"
    yvars = []
    yvars.append("BR_Hp_taunu")
    yvars.append("BR_Hp_tb")

    db = BRXSDB.BRXSDatabaseInterface(rootfile,heavy=True,program="2HDMC")
    progversion = db.GetProgram() + " v" + db.GetVersion()

    selection = "tanb==30"
    scenario = "2HDM Type II"

    graphs = {}
    
    for icolor,yvar in enumerate(yvars):
	tmpsel = selection
	br = db.getGraph(xvar,yvar,tmpsel)
	xarray = array.array('d')
	yarray = array.array('d')
	for i in range(0,br.GetN()):
	    x=ROOT.Double()
	    y=ROOT.Double()
	    br.GetPoint(i,x,y)
	    xarray.append(x)
	    yarray.append(y)
	newx,newy = sort(xarray,yarray)
	newGraph = ROOT.TGraph(len(newx),newx,newy)
        newGraph.SetLineWidth(3)
        newGraph.SetLineColor(1+icolor)
	graphs[yvar] = newGraph


    plot = plots.PlotBase([
            histograms.HistoGraph(graphs["BR_Hp_taunu"], "BR(H^{+}#rightarrow#tau#nu)", drawStyle="L", legendStyle="l"),
            histograms.HistoGraph(graphs["BR_Hp_tb"], "BR(H^{+}#rightarrow tb)", drawStyle="L", legendStyle="l"),
            ])

    plot.setLegend(histograms.createLegend(0.57, 0.60, 0.87, 0.80))
    plot.legend.SetFillColor(0)
    plot.legend.SetFillStyle(1001)
    plot.createFrame("br", opts={"ymin": 0, "ymax": 1, "xmin": 180, "xmax": 600})
    plot.frame.GetXaxis().SetTitle("m_{H^{+}} ("+GeVUnit+")")
    plot.frame.GetYaxis().SetTitle("BR")

    plot.draw()

    size = 20
    x = 0.57
#    histograms.addText(x, 0.9, limit.processHeavy, size=size)
#    histograms.addText(x, 0.863, limits.getFinalstateText(), size=size)
####    histograms.addText(x, 0.815, "MSSM m_{h}^{max}", size=size)
    histograms.addText(x, 0.863,scenario, size=size)
    selectiontxt = selection.replace("==","=")
    histograms.addText(x, 0.815,selectiontxt, size=size)
    
    #Adding a LHC label:
    ROOT.LHCHIGGS_LABEL(0.97,0.72,1)
#    histograms.addText(x, 0.55, progversion, size=size)
            
    plot.save()

def sort(x,y):
    ox = array.array('d')
    oy = array.array('d')

    def swap(i,j):
        if j < i and i <= len(ox):
            tmpx = ox[i]
            tmpy = oy[i]
            ox[i] = ox[j]
            oy[i] = oy[j]
            ox[j] = tmpx
            oy[j] = tmpy

    i = 0
    while i < len(x):
        ox.append(x[i])
        oy.append(y[i])
        j = i
        while j > 0 and ox[j] < ox[j-1]:
            swap(j,j-1)
            j = j - 1
        i = i + 1
    return ox,oy
 
if __name__=='__main__':
    main()
