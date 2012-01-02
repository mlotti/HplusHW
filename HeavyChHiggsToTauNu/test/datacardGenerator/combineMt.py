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

#	mass_re = re.compile("hplushadronic(?P<mass>(\d+))")
	mass_re = re.compile("(?P<mass>(\d+))")
	mass_match = mass_re.search(fOUT)

	signalLabel = "Signal"
        if mass_match:
	    mass = mass_match.group("mass")
	    signalLabel = "H^{#pm}, m_{H^{#pm}} = " + mass + " GeV/c^{2}"

	histos = []

	keys = fIN.GetListOfKeys()
	for i in range(fIN.GetNkeys()):
	    histoName = keys.At(i).GetName()

	    histo = fIN.Get(histoName)
	    histos.append(histo)

	frame = Frame()
        frame.SetXTitle("m_{T}(#tau-jet,MET) [GeV/c^{2}]")
        frame.SetYTitle("N_{events} / 10 GeV/c^{2}")
        frame.SetTop2HpBR(Top2HpBR)

	frame.SetHistograms(histos)

	frame.DataHisto("Data", "data_obs", "Data")
        frame.BackgrHisto("EWK","EWKTau", "EWK w.taus (meas.)")
        frame.BackgrHisto("EWKfake","fakett+fakeW+faket", "EWK fake taus (MC)")
	frame.BackgrHisto("QCD","QCD", "QCD (meas.)")
	frame.SignalHisto("Signal","HH*_1+HW*_1", signalLabel)

	frame.Save(fOUT)

        frame.BackgrHisto("QCD","QCDInv", "QCD (meas.)")

	frame.Save(fOUT+"Inv")
	fIN.Close()


class Frame:
    class Histo:
	def __init__(self, name, label, legend):
	    self.name = name
	    self.label = label
	    self.legend = legend

    def __init__(self):
	self.lumi	  = 1000*lumi # pb-1
	self.xtitle       = ""
	self.ytitle       = ""
	self.Top2HpBR     = 0.
	self.histograms   = []
	self.dataHistos   = []
	self.backgrHistos = []
	self.signalHistos = []
	self.histogramsNotFound   = []

    def setLegendLabels(self, plot):
	for histo in self.dataHistos:
	    plot.histoMgr.getHisto(histo.label).setLegendLabel(histo.legend)

	for histo in self.backgrHistos:
            plot.histoMgr.getHisto(histo.label).setLegendLabel(histo.legend)

	for histo in self.signalHistos:
            plot.histoMgr.getHisto(histo.label).setLegendLabel(histo.legend)

    def SetXTitle(self, title):
	self.xtitle = title

    def SetYTitle(self, title):
	self.ytitle = title

    def SetTop2HpBR(self, br):
	self.Top2HpBR = br

    def SetHistograms(self, histograms):
	self.histograms = histograms

    def AddMissingHisto(self, histoName):
	if self.histogramsNotFound.count(histoName) == 0:
	    self.histogramsNotFound.append(histoName)

    def SetFillColor(self, histoName, color):
	if self.Exists(histoName):
	    self.histograms[self.FindHistoIndex(histoName)].SetFillColor(color)
	else:
	    self.AddMissingHisto(histoName)

    def SetLineColor(self, histoName, color):
        if self.Exists(histoName):
            self.histograms[self.FindHistoIndex(histoName)].SetLineColor(color)
        else:
	    self.AddMissingHisto(histoName)

    def SetLineStyle(self, histoName, style):
        if self.Exists(histoName):
            self.histograms[self.FindHistoIndex(histoName)].SetLineStyle(style)
	    self.histograms[self.FindHistoIndex(histoName)].SetLineWidth(2)
        else:
	    self.AddMissingHisto(histoName)

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
	self.histogramsNotFound.append(histoName)
	return -1

    def DataHisto(self, label, histoName, legendName):
	self.CreateHisto(label, histoName)
	histoInfo = self.Histo(histoName,label,legendName)
	self.dataHistos.append(histoInfo)

    def BackgrHisto(self, label, histoName, legendName):
	self.CreateHisto(label, histoName)
	histoInfo = self.Histo(histoName,label,legendName)
	self.backgrHistos.append(histoInfo)

    def SignalHisto(self, label, histoName, legendName):
	self.CreateHisto(label, histoName)
	histoInfo = self.Histo(histoName,label,legendName)
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
		self.AddMissingHisto(histoName)

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

	if len(self.histogramsNotFound) > 0:
	    for name in self.histogramsNotFound:
		print "Histo",name,"not found"
	    self.histogramsNotFound = []
	    return
	    

	hObserved = self.histograms[self.FindHistoIndex(self.dataHistos[0].name)].Clone("Data")
        hObserved.Reset()
	for histo in self.dataHistos:
            hObserved.Add(self.histograms[self.FindHistoIndex(histo.label)])

	hEstimatedEWKfake = self.histograms[self.FindHistoIndex("EWKfake")].Clone("hEstimatedEWKfake")
	hEstimatedEWK     = self.histograms[self.FindHistoIndex("EWK")].Clone("hEstimatedEWK")
	hEstimatedEWK.Add(hEstimatedEWKfake)
	hEstimatedQCD     = self.histograms[self.FindHistoIndex("QCD")].Clone("hEstimatedQCD")
	hEstimatedQCD.Add(hEstimatedEWK)
	hUncertainty = hEstimatedQCD.Clone("BackgrUncertainty")
	hUncertainty.SetFillColor(1)
	hUncertainty.SetFillStyle(3354)
	hUncertainty.SetLineColor(0)
	hUncertainty.SetLineStyle(0)
	hUncertainty.SetLineWidth(0)
	hUncertainty.SetMarkerColor(0)
	hUncertainty.SetMarkerSize(0)
	hSignal           = self.histograms[self.FindHistoIndex("Signal")].Clone("hSignal")
	hSignal.Add(hEstimatedQCD)


	style = tdrstyle.TDRStyle()


	plot = plots.ComparisonManyPlot(
	    histograms.Histo(hObserved, "Data"),
	    [
	     histograms.Histo(hUncertainty, "Backgr.Uncertainty"),
	     histograms.Histo(hEstimatedEWKfake, "EWKfake"),
             histograms.Histo(hEstimatedEWK, "EWK"),
             histograms.Histo(hEstimatedQCD, "QCD"),
             histograms.Histo(hSignal, "Signal")
             ]
	)

        plot.histoMgr.forHisto("Data", styles.getDataStyle())

	plot.histoMgr.forHisto("EWK",styles.getEWKStyle())
	plot.histoMgr.forHisto("EWKfake",styles.getEWKFakeStyle())
	plot.histoMgr.forHisto("QCD",styles.getQCDStyle())
	plot.histoMgr.forHisto("Signal",styles.getSignalStyle())
	plot.histoMgr.forHisto("Backgr.Uncertainty",styles.getErrorStyle())

	plot.histoMgr.setHistoDrawStyleAll("HIST")
	plot.histoMgr.setHistoDrawStyle("Data", "EP")
	plot.histoMgr.setHistoDrawStyle("Backgr.Uncertainty", "E2")

	plot.histoMgr.setHistoLegendStyleAll("F")
	plot.histoMgr.setHistoLegendStyle("Data", "P")
	plot.histoMgr.setHistoLegendStyle("Signal", "L")

        plot.createFrame(name, opts={"ymin":0, "ymaxfactor": 1.2})
	plot.frame.GetXaxis().SetTitle(self.xtitle)
	plot.frame.GetYaxis().SetTitle(self.ytitle)

	plot.histoMgr.reorderLegend(["Data", "Signal", "QCD", "EWK", "EWKfake", "Backgr.Uncertainty"])
	self.setLegendLabels(plot)
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

