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

#import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
#import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
#import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect

lumi = 2.2

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
        frame.SetTop2HpBR(0.05)

	frame.SetHistograms(histos)

	frame.DataHisto("Data","data_obs", )
        frame.BackgrHisto("EWK","EWKTau")
        frame.BackgrHisto("EWK (fake tau)","fakett+fakeW+faket")
#	frame.BackgrHisto("QCD","QCD")
	frame.BackgrHisto("QCD","QCDInv")
	frame.SignalHisto("H^{#pm}","HH*_1+HW*_1")

	frame.SetColor("EWK",ROOT.TColor.GetColor("#993399"))
	frame.SetColor("EWK (fake tau)", ROOT.TColor.GetColor("#669900"))
	frame.SetColor("QCD", ROOT.TColor.GetColor("#ffcc33"))
	frame.SetColor("H^{#pm}", ROOT.TColor.GetColor("#ff3399"))

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

    def SetColor(self, histoName, color):
	if self.Exists(histoName):
	    self.histograms[self.FindHistoIndex(histoName)].SetFillColor(color)
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

	hEstimated = self.histograms[self.FindHistoIndex(self.dataHistos[0].name)].Clone("Backgr")
	hEstimated.Reset()
        for histo in self.backgrHistos:
            hEstimated.Add(self.histograms[self.FindHistoIndex(histo.label)])

        hEstimatedWSignal = self.histograms[self.FindHistoIndex(self.signalHistos[0].label)].Clone("SB")
	hEstimatedWSignal.Reset()
        for histo in self.signalHistos:
            hEstimatedWSignal.Add(self.histograms[self.FindHistoIndex(histo.label)])
	hEstimatedWSignal.Add(hEstimated)

	comparosonHistos = []
	comparosonHistos.append(hEstimatedWSignal)
	comparosonHistos.append(hEstimated)

	style = tdrstyle.TDRStyle()

        xsect.setHplusCrossSectionsToBR(datasets, br_tH=0.05, br_Htaunu=1)
#        plots.mergeWHandHH(datasets)

	plot = plots.ComparisonManyPlot(
	    histograms.Histo(hObserved, "Data"),
	    [histograms.Histo(hEstimated, "Backgr"),histograms.Histo(hEstimatedWSignal, "SB")]
	)
	dataStyle = styles.getDataStyle().clone()
	plot.histoMgr.forHisto("Data", dataStyle)
	plot.histoMgr.setHistoDrawStyle("Data", "EP")

        plot.createFrame(name, opts={"ymin":0, "ymaxfactor": 2})
	plot.frame.GetXaxis().SetTitle(self.xtitle)
	plot.frame.GetYaxis().SetTitle(self.ytitle)
	
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

