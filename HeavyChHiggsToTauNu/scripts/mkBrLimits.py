#!/usr/bin/env python

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.LandSTools import *

drawToScreen = True
drawToScreen = False

import ROOT
if not drawToScreen:
    ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots

from array import array

def main():

    if len(sys.argv) == 1:
        print "\n"
        print "### Usage:   test.py <multicrabdir>\n"
        print "\n"
        sys.exit()

    path = sys.argv[1]
    if path[len(path)-1] != '/':
        path += "/"

    fOUT = "brlimit"

    result = ParseLandsOutput(path)
    result.toFloat()
    result.Print()
#    result.Save("outputs")
    
    frame = Frame()
    frame.SetXTitle("m_{H^{#pm}} [GeV/c^{2}]")
    frame.SetYTitle("95% CL limit for BR(t#rightarrow bH^{#pm})")
    frame.SetLuminosity(result.GetLuminosity())
    
    frame.SetData(result.Data())

    frame.Save(fOUT)


class Frame:
    def __init__(self):
        self.lumi         = 0
        self.xtitle       = ""
        self.ytitle       = ""
	self.data         = []

    def SetXTitle(self, title):
        self.xtitle = title   
        
    def SetYTitle(self, title):
        self.ytitle = title 

    def SetData(self, value):
	for point in value:
	    self.data.append(ConvertToErrorBands(point))

    def SetLuminosity(self, lumi):
	self.lumi = 1000*float(lumi) # pb-1

    def CreateGraph(self, name):
	x      = array("d")
	y      = array("d")
	x_err  = array("d")
	y_errl = array("d")
	y_errh = array("d")

	for point in self.data:
	    x.append(float(point.mass))
	    x_err.append(0.)
	    if name == "Observed":
	        y.append(float(point.observed))
		y_errl.append(float(0.))
		y_errh.append(float(0.))
	    else:
		y.append(float(point.expected))
		if not name.find("1") == -1:
	    	    y_errl.append(float(point.expectedMinus1Sigma))
	    	    y_errh.append(float(point.expectedPlus1Sigma))
		elif not name.find("2") == -1:
                    y_errl.append(float(point.expectedMinus2Sigma))
                    y_errh.append(float(point.expectedPlus2Sigma))
		else:	
		    y_errl.append(float(0.))
		    y_errh.append(float(0.))
	graph = ROOT.TGraphAsymmErrors(len(x),x,y,x_err,x_err,y_errl,y_errh)
	graph.SetName(name)
	return graph

    def Save(self,name):

        hObserved   = self.CreateGraph("Observed")
	hExpected   = self.CreateGraph("Expected")
	hExpected1s = self.CreateGraph("Expected1")
	hExpected1s.SetFillColor(ROOT.kYellow)
	hExpected2s = self.CreateGraph("Expected2")
	hExpected2s.SetFillColor(ROOT.kOrange)

	style = tdrstyle.TDRStyle()

	plot = plots.ComparisonManyPlot(
	    histograms.HistoGraph(hObserved, "Observed"),
	    [
	     histograms.HistoGraph(hExpected, "Expected"),
	     histograms.HistoGraph(hExpected1s, "Expected1"),
	     histograms.HistoGraph(hExpected2s, "Expected2")
	     ]
	)

	obsStyle = styles.getDataStyle().clone()
	plot.histoMgr.forHisto("Observed", styles.getDataStyle().clone())
	plot.histoMgr.setHistoDrawStyle("Observed", "PL")

	expStyle = styles.getDataStyle().clone()
	expStyle.append(styles.StyleLine(lineStyle=2))
	expStyle.append(styles.StyleLine(lineColor=ROOT.kRed))
	expStyle.append(styles.StyleMarker(markerStyle=ROOT.kFullSquare))
	expStyle.append(styles.StyleMarker(markerColor=ROOT.kRed))
	plot.histoMgr.forHisto("Expected", expStyle)
	plot.histoMgr.setHistoDrawStyle("Expected", "PL")
	plot.histoMgr.setHistoDrawStyle("Expected1", "PL3")
	plot.histoMgr.setHistoDrawStyle("Expected2", "PL3")

        plot.createFrame(name, opts={"xmin": 70.1, "xmax": 169.9, "ymin":0, "ymax": 0.2})
        plot.frame.GetXaxis().SetTitle(self.xtitle)
        plot.frame.GetYaxis().SetTitle(self.ytitle)


	plot.histoMgr.setHistoLegendStyle("Observed", "PL")
	plot.histoMgr.setHistoLegendStyle("Expected", "PL")
	plot.histoMgr.setHistoLegendStyle("Expected1", "F")
	plot.histoMgr.setHistoLegendStyle("Expected2", "F")

        plot.histoMgr.setHistoLegendLabelMany({
            "Expected": "Expected median",
            "Expected1": "Expected median #pm1#sigma",
            "Expected2": "Expected median #pm2#sigma"
            })
        plot.setLegend(histograms.createLegend(0.55,0.68,0.9,0.93))
        
        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        histograms.addLuminosityText(x=None, y=None, lumi=self.lumi)

	textSize = 16
	textX    = 0.19
	textY    = 0.8
	textDY   = 0.038
	histograms.addText(textX,textY+2*textDY,"t#rightarrowbH^{#pm}, H^{#pm}#rightarrow#tau#nu",textSize)
	histograms.addText(textX,textY+textDY,"Fully hadronic final state",textSize)
	histograms.addText(textX,textY,"BR(H^{#pm}#rightarrow#tau^{#pm} #nu) = 1",textSize)
        
        plot.draw()
        plot.save()

if __name__ == "__main__":
    main()
