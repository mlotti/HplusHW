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
import LimitCalc.limit as limit
import LimitCalc.BRXSDatabaseInterface as BRXSDB

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
    yvars.append("BR_Hp_h0W")
    yvars.append("BR_Hp_A0W")
    yvars.append("BR_Hp_HW")
#    yvars.append("BR_Hp_Neu1Cha1")
#    yvars.append("BR_Hp_Neu2Cha1")

    susyvars = []
    susyvars.append("BR_Hp_Neu1Cha1")
    susyvars.append("BR_Hp_Neu2Cha1")
#    susyvars.append("BR_Hp_Neu3Cha1")
#    susyvars.append("BR_Hp_Neu4Cha1")
#    susyvars.append("BR_Hp_Neu1Cha2")
#    susyvars.append("BR_Hp_Neu2Cha2")
#    susyvars.append("BR_Hp_Neu3Cha2")
#    susyvars.append("BR_Hp_Neu4Cha2")


#    db = BRXSDB.BRXSDatabaseInterface(rootfile,heavy=True,program="2HDMC")
    db = BRXSDB.BRXSDatabaseInterface(rootfile,heavy=True,program="FeynHiggs")
    progversion = db.GetProgram() + " v" + db.GetVersion()

    selection = "tanb==10"
#    scenario = "2HDM Type II"
    scenario = "mhmax"

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

    xsusy = array.array('d')
    ysusy = array.array('d')
    for yvar in susyvars:
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
	    print "check x,y",x,y
	xsusy,ysusy = add(xsusy,ysusy,xarray,yarray)
    print "check len",len(xsusy)
    newx,newy = sort(xsusy,ysusy)
    for i in range(len(newx)):
	print newx[i],newy[i]
    susyGraph = ROOT.TGraph(len(newx),newx,newy)
    susyGraph.SetLineWidth(3)
    susyGraph.SetLineColor(1+len(graphs))
    graphs["BR_Hp_SUSY"] = susyGraph

    plot = plots.PlotBase([
            histograms.HistoGraph(graphs["BR_Hp_taunu"], "BR(H^{+}#rightarrow#tau#nu)", drawStyle="L", legendStyle="l"),
            histograms.HistoGraph(graphs["BR_Hp_tb"], "BR(H^{+}#rightarrow tb)", drawStyle="L", legendStyle="l"),
	    histograms.HistoGraph(graphs["BR_Hp_h0W"], "BR(H^{+}#rightarrow hW)", drawStyle="L", legendStyle="l"),
	    histograms.HistoGraph(graphs["BR_Hp_A0W"], "BR(H^{+}#rightarrow AW)", drawStyle="L", legendStyle="l"),
	    histograms.HistoGraph(graphs["BR_Hp_HW"], "BR(H^{+}#rightarrow HW)", drawStyle="L", legendStyle="l"),
	    histograms.HistoGraph(graphs["BR_Hp_SUSY"], "BR(H^{+}#rightarrow#chi_{i}^{0}#chi_{j}^{+})", drawStyle="L", legendStyle="l"),
#	    histograms.HistoGraph(graphs["BR_Hp_Neu1Cha1"], "BR(H^{+}#rightarrow#chi_{1}^{0}#chi_{1}^{+})", drawStyle="L", legendStyle="l"),
#	    histograms.HistoGraph(graphs["BR_Hp_Neu2Cha1"], "BR(H^{+}#rightarrow#chi_{2}^{0}#chi_{1}^{+})", drawStyle="L", legendStyle="l"),
            ])

    plot.setLegend(histograms.createLegend(0.57, 0.60, 0.87, 0.80))
    plot.legend.SetFillColor(0)
    plot.legend.SetFillStyle(1001)
    plot.createFrame("br", opts={"ymin": 0.0001, "ymax": 1, "xmin": 180, "xmax": 600})
    plot.frame.GetXaxis().SetTitle("m_{H^{+}} ("+GeVUnit+")")
    plot.frame.GetYaxis().SetTitle("BR")
    ROOT.gPad.SetLogy(True)

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

def add(x1,y1,x2,y2):
    ox = array.array('d')
    oy = array.array('d')

    if len(x1) == 0:
	for i in range(len(x2)):
	    if y2[i] > 0:
		ox.append(x2[i])
                oy.append(y2[i])
	    else:
                ox.append(x2[i])
                oy.append(0.000000001)
	return ox,oy

    for i in range(len(x1)):
	if y1[i] > 0:
	    ox.append(x1[i])
	    oy.append(y1[i])
        else:
            ox.append(x1[i])      
            oy.append(0.000000001)

    for i in range(len(x2)):
	for j in range(len(ox)):
	    if y2[i] > 0:
		if not x2[i] in ox:
		    ox.append(x2[i])
		    oy.append(y2[i])
	        else:
		    if x2[i] == ox[j]:
		        oy[j] = oy[j] + y2[i]
    return ox,oy
     
if __name__=='__main__':
    main()
