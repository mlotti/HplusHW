#!/usr/bin/env python

import sys
import os
import re
import string

drawToScreen = True
drawToScreen = False

import ROOT
if not drawToScreen:
    ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots

lumi     = 2.2
Top2HpBR = 0.05

def main():

    if len(sys.argv) == 1:
        print "\n"
        print "### Usage:   combineMt.py <datacards directory>\n"
        print "\n"   
        sys.exit()

    path = sys.argv[1]
    path = path.rstrip('/')

    command = "ls " + path + "/*.root"
    rootFiles = execute(command)

    for file in rootFiles:
	makePlot(file)


def makePlot(file):
    root_re = re.compile("(?P<rootfile>([^/]*))\.root")
    match = root_re.search(file)
    if match:
	fIN  = ROOT.TFile.Open(file)
	fOUT = match.group("rootfile")

	histos = []

	keys = fIN.GetListOfKeys()
	for i in range(fIN.GetNkeys()):
	    histoName = keys.At(i).GetName()

	    histo = fIN.Get(histoName)
	    histos.append(histo)

	frame = Frame(1000,0,400)
        frame.SetXTitle("m_{T}(#tau-jet,MET) [GeV/c^{2}]")
        frame.SetYTitle("N_{events} / 10 GeV/c^{2}")
        frame.SetTop2HpBR(Top2HpBR)

	frame.SetHistograms(histos)

	frame.DataHisto("Data","data_obs", )
        frame.BackgrHisto("EWK w. taus (meas.)","EWKTau")
        frame.BackgrHisto("EWK fake taus (MC)","fakett+fakeW+faket")
#	frame.BackgrHisto("QCD","QCD")
	frame.BackgrHisto("QCD","QCDInv")
	frame.SignalHisto("H^{#pm}","HH*_1+HW*_1")

	frame.SetFillColor("EWK w. taus (meas.)",ROOT.TColor.GetColor("#993399"))
	frame.SetFillColor("EWK fake taus (MC)", ROOT.TColor.GetColor("#669900"))
	frame.SetFillColor("QCD", ROOT.TColor.GetColor("#ffcc33"))
	frame.SetLineColor("H^{#pm}", ROOT.TColor.GetColor("#ff3399"))
	frame.SetLineStyle("H^{#pm}", 2)

#	frame.Save(fOUT)

#        frame.DataHisto("Data","data_obs")
#        frame.BackgrHisto("EWK","EWKTau") 
#        frame.BackgrHisto("EWK (fake tau)","fakett+fakeW+faket") 
#        frame.BackgrHisto("QCD","QCDInv")
#	frame.SignalHisto("H^{#pm}","HH*_1+HW*_1")

	frame.Save(fOUT+"Inv")


class Frame:
    class Histo:
	def __init__(self, name, label):
	    self.name = name
	    self.label = label

    def __init__(self, nbins, xmin, xmax):
	self.lumi	  = 1000*lumi # pb-1
	self.nbins        = nbins
	self.xmin         = xmin
	self.xmax         = xmax
	self.xtitle       = ""
	self.ytitle       = ""
	self.Top2HpBR     = 0.
	self.histograms   = []
	self.dataHistos   = []
	self.backgrHistos = []
	self.signalHistos = []

    def SetXTitle(self, title):
	self.xtitle = title

    def SetYTitle(self, title):
	self.ytitle = title

    def SetTop2HpBR(self, br):
	self.Top2HpBR = br

    def SetHistograms(self, histograms):
	self.histograms = histograms

    def SetFillColor(self, histoName, color):
	if self.Exists(histoName):
	    self.histograms[self.FindHistoIndex(histoName)].SetFillColor(color)
	else:
	    print "Histogram",histoName,"not found, exiting.."
	    sys.exit()

    def SetLineColor(self, histoName, color):
        if self.Exists(histoName):
            self.histograms[self.FindHistoIndex(histoName)].SetLineColor(color)
        else:
            print "Histogram",histoName,"not found, exiting.."
            sys.exit()

    def SetLineStyle(self, histoName, style):
        if self.Exists(histoName):
            self.histograms[self.FindHistoIndex(histoName)].SetLineStyle(style)
	    self.histograms[self.FindHistoIndex(histoName)].SetLineWidth(2)
        else:
            print "Histogram",histoName,"not found, exiting.."
            sys.exit()

    def Exists(self, histoName):
	for histo in self.histograms:
	    if histo.GetName() == histoName:
		return True
	return False

    def FindHistoIndex(self, histoName):
	for i, histo in enumerate(self.histograms):
		if histo.GetName() == histoName:
		    return i
	print "Histogram",histoName,"not found"
	return -1

    def DataHisto(self, label, histoName):
	self.CreateHisto(label, histoName)
	histoInfo = self.Histo(histoName,label)
	self.dataHistos.append(histoInfo)

    def BackgrHisto(self, label, histoName):
	self.CreateHisto(label, histoName)
	histoInfo = self.Histo(histoName,label)
	self.backgrHistos.append(histoInfo)

    def SignalHisto(self, label, histoName):
	self.CreateHisto(label, histoName)
	histoInfo = self.Histo(histoName,label)
	self.signalHistos.append(histoInfo)

    def CreateHisto(self, label, histoName):
	if self.Sum(histoName):
	    names = self.FindHistoNames(histoName)
	    histo = self.histograms[self.FindHistoIndex(names[0])].Clone(label)
	    histo.Reset()
	    histo.SetTitle(histoName)
	    for name in names:
		if self.Exists(name):
		    tmphisto = self.histograms[self.FindHistoIndex(name)]
		    tmphisto = self.Scale(tmphisto)
		    histo.Add(tmphisto)
	    self.histograms.append(histo)
	else:
	    if self.Exists(histoName):
   	        histo = self.histograms[self.FindHistoIndex(histoName)].Clone(label)
		histo.SetTitle(histoName)
	        self.histograms.append(histo)
	    else:
		print "Histo",histoName,"not found, exiting.."
		sys.exit()

    def Scale(self, histo):
	name = histo.GetName()
	if name.find("HH") == 0:
	    histo.Scale(self.Top2HpBR*self.Top2HpBR)
	if name.find("HW") == 0:
	    histo.Scale(2*self.Top2HpBR*(1-self.Top2HpBR))
	return histo

    def Sum(self, name):
	if string.find(name, "+") == -1:
 	    return False
	return True

    def FindHistoNames(self, names):
	histoNames = names.split('+')
	for i, name in enumerate(histoNames):
	    if not name.find('*') == -1:
		name = "^" + name + "$"
                name = name.replace('*','\S*')
		name_re = re.compile(name)
		for histo in self.histograms:
		    match = name_re.search(histo.GetName())
		    if match:
		        histoNames[i] = histo.GetName()
	return histoNames

	    
		
    def Save(self, name):

	hObserved = self.histograms[self.FindHistoIndex(self.dataHistos[0].name)].Clone("Data")
        hObserved.Reset()
	for histo in self.dataHistos:
            hObserved.Add(self.histograms[self.FindHistoIndex(histo.label)])

	hEstimatedEWKfake = self.histograms[self.FindHistoIndex("EWK fake taus (MC)")]
	hEstimatedEWK     = self.histograms[self.FindHistoIndex("EWK w. taus (meas.)")]
	hEstimatedEWK.Add(hEstimatedEWKfake)
	hEstimatedQCD     = self.histograms[self.FindHistoIndex("QCD")]
	hEstimatedQCD.Add(hEstimatedEWK)
	hUncertainty = hEstimatedQCD.Clone("BackgrUncertainty")
	hUncertainty.SetFillColor(1)
	hUncertainty.SetFillStyle(3354)
	hUncertainty.SetLineColor(0)
	hUncertainty.SetLineStyle(0)
	hUncertainty.SetLineWidth(0)
	hUncertainty.SetMarkerColor(0)
	hUncertainty.SetMarkerSize(0)
	hSignal           = self.histograms[self.FindHistoIndex("H^{#pm}")]
	hSignal.Add(hEstimatedQCD)


	style = tdrstyle.TDRStyle()


	plot = plots.ComparisonManyPlot(
	    histograms.Histo(hObserved, "Data"),
	    [
	     histograms.Histo(hUncertainty, "Backgr.Uncert"),
	     histograms.Histo(hEstimatedEWKfake, "EWK fake taus (MC)"),
             histograms.Histo(hEstimatedEWK, "EWK w. taus (meas.)"),
             histograms.Histo(hEstimatedQCD, "QCD"),
             histograms.Histo(hSignal, "H^{#pm}")
             ]
	)

        plot.histoMgr.forHisto("Data", styles.getDataStyle())

	plot.histoMgr.forHisto("EWK w. taus (meas.)",styles.getEWKStyle())
	plot.histoMgr.forHisto("EWK fake taus (MC)",styles.getEWKFakeStyle())
	plot.histoMgr.forHisto("QCD",styles.getQCDStyle())
	plot.histoMgr.forHisto("H^{#pm}",styles.getSignalStyle())
	plot.histoMgr.forHisto("Backgr.Uncert",styles.getErrorStyle())

	plot.histoMgr.setHistoDrawStyleAll("HIST")
	plot.histoMgr.setHistoDrawStyle("Data", "EP")
	plot.histoMgr.setHistoDrawStyle("Backgr.Uncert", "E2")

	plot.histoMgr.setHistoLegendStyleAll("F")
	plot.histoMgr.setHistoLegendStyle("Data", "P")
	plot.histoMgr.setHistoLegendStyle("H^{#pm}", "L")

        plot.createFrame(name, opts={"ymin":0, "ymaxfactor": 1.2})
	plot.frame.GetXaxis().SetTitle(self.xtitle)
	plot.frame.GetYaxis().SetTitle(self.ytitle)

	plot.setLegend(histograms.createLegend(0.55,0.68,0.9,0.93))
	
        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        histograms.addLuminosityText(x=None, y=None, lumi=self.lumi)
        
        plot.draw()
        plot.save()


def execute(cmd):
    f = os.popen(cmd)
    ret=[]
    for line in f:
        ret.append(line.replace("\n", ""))
    f.close()
    return ret


if __name__ == "__main__":
    main()

