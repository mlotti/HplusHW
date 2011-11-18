#!/usr/bin/env python

###########################################################################
#
# This script is only intended as an example, please do NOT modify it.
# For example, start from scratch and look here for help, or make a
# copy of it and modify the copy (including removing all unnecessary
# code).
#
###########################################################################

import ROOT
#ROOT.gROOT.SetBatch(True)
from ROOT import *
import math
import sys

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect

analysis = "signalAnalysis"
counters = analysis+"Counters/weighted"

def ExpFunction(x,par):
    if (x[0] > 280 and x[0] < 300) or x[0] > 360:
        TF1.RejectPoint()
        return 0
    return par[0]*TMath.Exp(-x[0]*par[1])
def Gaussian(x,par):
    return par[0]*TMath.Gaus(x[0],par[1],par[2],1)
def SumFunction(x,par):
    return par[0]*TMath.Gaus(x[0],par[1],par[2],1) + par[3]*TMath.Exp(-x[0]*par[4])

def EWKFunction(x,par,norm = 1,rejectPoints = 0):
    if not rejectPoints == 0:
#        if (x[0] > 280 and x[0] < 300) or x[0] > 360:
#	if x[0] > 40 and x[0] < 60 :
#	if x[0] > 240 and x[0] < 260:
#	if  (x[0] > 180 and x[0] < 200) or (x[0] > 260 and x[0] < 320):
	if  (x[0] > 100 and x[0] < 120) or (x[0] > 180 and x[0] < 200):
#	if  (x[0] > 60 and x[0] < 80) or (x[0] > 140 and x[0] < 160) or (x[0] > 180 and x[0] < 220) or (x[0] > 240 and x[0] < 360):
#	if  (x[0] > 40 and x[0] < 60) or (x[0] > 80 and x[0] < 100) or (x[0] > 120 and x[0] < 140) or (x[0] > 160 and x[0] < 180):
            TF1.RejectPoint()
            return 0
    value = 120
    if x[0] < value:
	return norm*par[0]*TMath.Gaus(x[0],par[1],par[2],1)
    C = norm*par[0]*TMath.Gaus(value,par[1],par[2],1)*TMath.Exp(value*par[3])
    return C*TMath.Exp(-x[0]*par[3])

def QCDFunction(x,par,norm):
    return norm*(par[0]*TMath.Gaus(x[0],par[1],par[2],1)+par[3]*TMath.Gaus(x[0],par[4],par[5],1)+par[6]*TMath.Exp(-par[7]*x[0]))
#    return norm*(par[0]*TMath.Gaus(x[0],par[1],par[2],1))
#    return norm*(par[0]*TMath.Gaus(x[0],par[1],par[2],1)+par[3]*TMath.Gaus(x[0],par[4],par[5],1))
#    return norm*(par[0]*TMath.Gaus(x[0],par[1],par[2],1)+par[3]*TMath.Exp(-par[4]*x[0]))

#def EWKFunction(x,par,norm):
#    if (x[0] > 280 and x[0] < 300) or x[0] > 360:
#	TF1.RejectPoint()
#	return 0
#    return norm*(par[0]*TMath.Gaus(x[0],par[1],par[2],1)+par[3]*TMath.Gaus(x[0],par[4],par[5],1))
#    return norm*(par[0]*TMath.Gaus(x[0],par[1],par[2],1))
#    return norm*(par[0]*TMath.Exp(-x[0]*par[1]))
#    return norm*(par[0]*TMath.Landau(x[0],par[1],par[2]))
#    return norm*(par[0]*TMath.Gaus(x[0],par[1],par[2],1)+par[3]*TMath.Landau(x[0],par[4],par[5]))
#     return norm*(par[0]*TMath.Poisson(x[0],par[1]))
#    return norm*(par[0]*TMath.Gaus(x[0],par[1],par[2],1)*TMath.Exp(-x[0]*par[3]))
#    return norm*(par[0]*TMath.Gaus(x[0],par[1],par[2],1)*TMath.Sqrt(x[0]))

class InvertedTauID:

    def __init__( self):
	self.parInvQCD  = []
	self.parMCEWK   = []
	self.parBaseQCD = []

	self.nInvQCD  = 0
	self.nMCEWK   = 0
	self.nBaseQCD = 0

	self.normInvQCD  = 1

	self.QCDfraction = 0

	self.label = ""
	self.labels = []
	self.normFactors = []


    def setLabel(self, label):
	self.label = label

    def comparison(self,histo1,histo2):

        comp = TCanvas("comp","",500,500)
        comp.cd()
        comp.SetLogy()

	h1 = histo1.Clone("h1")
	h2 = histo2.Clone("h2")
	h1.Scale(1/h1.GetMaximum())
	h2.Scale(1/h2.GetMaximum())

	# check that no bin has negative value, negative values possible after subtracting EWK from data  
        iBin = 1
        nBins = h1.GetNbinsX()
        while iBin < nBins:
	    value1 = h1.GetBinContent(iBin)
	    value2 = h2.GetBinContent(iBin)

	    if value1 < 0:
		h1.SetBinContent(iBin,0)

            if value2 < 0:
                h2.SetBinContent(iBin,0)

            iBin = iBin + 1


	h1.GetYaxis().SetTitle("Arbitrary units")
	h1.GetYaxis().SetTitleOffset(1.5)
        h1.Draw()
	h2.SetMarkerColor(2)
	h2.Draw("same")

        tex1 = TLatex(0.6,0.9,"Inverted TauID")
        tex1.SetNDC()
	tex1.SetTextSize(20)
        tex1.Draw()

	marker1 = TMarker(0.58,0.915,h1.GetMarkerStyle())
	marker1.SetNDC()
	marker1.SetMarkerColor(h1.GetMarkerColor())
	marker1.SetMarkerSize(0.5*h1.GetMarkerSize())
	marker1.Draw()

	tex2 = TLatex(0.6,0.85,"Baseline TauID")
        tex2.SetNDC()
	tex2.SetTextSize(20)
        tex2.Draw()

        marker2 = TMarker(0.58,0.865,h2.GetMarkerStyle())
        marker2.SetNDC()
        marker2.SetMarkerColor(h2.GetMarkerColor())
        marker2.SetMarkerSize(0.5*h2.GetMarkerSize())
        marker2.Draw()

        comp.Print("comparison"+self.label+".eps")
	comp.Print("comparison"+self.label+".C")

	## cut vs eff

        cuteff = TCanvas("cuteff","",500,500)
        cuteff.cd()
        cuteff.SetLogy()

	h1cut = histo1.Clone("h1cut")
	h1cut.Reset()
	h1cut.GetYaxis().SetTitle("Efficiency")
        h1cut.GetXaxis().SetTitle("PF MET cut (GeV)")

        h2cut = histo2.Clone("h2cut")
        h2cut.Reset()
	h2cut.SetLineColor(2)
 
        h1_integral = h1.Integral()
	h2_integral = h2.Integral()

	iBin = 1
	nBins = h1cut.GetNbinsX()
	while iBin < nBins:
	    selected1 = h1.Integral(iBin,nBins)
	    efficiency1 = selected1/h1_integral
	    h1cut.SetBinContent(iBin,efficiency1)

            selected2 = h2.Integral(iBin,nBins)
            efficiency2 = selected2/h2_integral
            h2cut.SetBinContent(iBin,efficiency2)

	    iBin = iBin + 1

	h1cut.Draw()
	h2cut.Draw("same")

	cuteff.Print("cuteff"+self.label+".eps")

    def fitQCD(self,histo): 

        rangeMin = histo.GetXaxis().GetXmin()
        rangeMax = histo.GetXaxis().GetXmax()

        numberOfParameters = 8

        print "Fit range ",rangeMin, " - ",rangeMax

	class FitFunction:
	    def __call__( self, x, par ):
		return QCDFunction(x,par,1)

        theFit = TF1('theFit',FitFunction(),rangeMin,rangeMax,numberOfParameters)

#        theFit.SetParLimits(0,1,200)
#        theFit.SetParLimits(1,-200,150)
#        theFit.SetParLimits(2,50,250)

        theFit.SetParLimits(0,10,20)
        theFit.SetParLimits(1,20,40)
        theFit.SetParLimits(2,10,25)

        theFit.SetParLimits(3,1,10)
        theFit.SetParLimits(4,0,150)
        theFit.SetParLimits(5,20,100)

        theFit.SetParLimits(6,0.001,1)
        theFit.SetParLimits(7,0.001,0.05)
#	theFit.SetParLimits(3,0.001,1)
#	theFit.SetParLimits(4,0.001,0.05)

	if self.label == "7080":
	    theFit.SetParLimits(5,10,100)

#	if self.label == "100120":
#	    theFit.SetParLimits(0,1,20)
#	    theFit.SetParLimits(2,1,25)
#	    theFit.SetParLimits(3,0.1,20)

	if self.label == "120150":
            theFit.SetParLimits(0,1,20)
            theFit.SetParLimits(3,0.1,5)

        cqcd = TCanvas("c","",500,500)
        cqcd.cd()                     
        cqcd.SetLogy()
	gStyle.SetOptFit(0)

	self.normInvQCD = histo.Integral()

	histo.Scale(1/self.normInvQCD)
        histo.Fit(theFit,"R")         
                                      
        theFit.SetRange(histo.GetXaxis().GetXmin(),histo.GetXaxis().GetXmax())
        theFit.SetLineStyle(2)                                                
        theFit.Draw("same")

        tex = TLatex(0.4,0.8,"Inverted TauID")
	tex.SetNDC()
	tex.Draw()

        cqcd.Print("qcdfit"+self.label+".eps")

                                                                              
        self.parInvQCD = theFit.GetParameters()                               
                                                                              
        fitPars = "fit parameters "                                           
        i = 0                                                                 
        while i < numberOfParameters:
            fitPars = fitPars + " " + str(self.parInvQCD[i])
            i = i + 1
        print fitPars
	self.nInvQCD = theFit.Integral(0,1000,self.parInvQCD)
        print "Integral ",self.normInvQCD*self.nInvQCD

    def fitEWK(self,histo):

        rangeMin = histo.GetXaxis().GetXmin()
        rangeMax = histo.GetXaxis().GetXmax()
#	rangeMin = 120
#	rangeMax = 120

        numberOfParameters = 4

        print "Fit range ",rangeMin, " - ",rangeMax

#	class Function1:
#            def __call__( self, x, par ):  
#                return Gaussian(x,par)
#
#	fit1 = TF1('fit1',Function1(),0,150,3)
#	
#        class Function2:
#            def __call__( self, x, par ):
#                return ExpFunction(x,par)        
#        
#        fit2 = TF1('fit2',Function2(),150,400,2)
#        
        class FitFunction:
            def __call__( self, x, par ):
                return EWKFunction(x,par,1,1)
#		return SumFunction(x,par)
#	        return TestFunction(x,par,1)
	class PlotFunction:
	    def __call__( self, x, par ):
		return EWKFunction(x,par,0)

        theFit = TF1('theFit',FitFunction(),rangeMin,rangeMax,numberOfParameters)
	thePlot = TF1('thePlot',PlotFunction(),rangeMin,rangeMax,numberOfParameters)

        theFit.SetParLimits(0,5,20)
        theFit.SetParLimits(1,90,120)
        theFit.SetParLimits(2,30,50) 
        theFit.SetParLimits(3,0.001,1)

#    	theFit.SetParLimits(0,10,20)
#    	theFit.SetParLimits(1,80,120)
#    	theFit.SetParLimits(2,30,60)
#    	theFit.SetParLimits(3,1,10)
#	theFit.SetParLimits(4,100,250)
#	theFit.SetParLimits(5,50,100)

        if self.label == "4050":
            theFit.SetParLimits(0,5,20) 
            theFit.SetParLimits(1,90,120)
            theFit.SetParLimits(2,30,50)
            theFit.SetParLimits(3,0.001,1)

	if self.label == "5060":
            theFit.SetParLimits(0,5,20)     
            theFit.SetParLimits(1,90,120)   
            theFit.SetParLimits(2,30,50)
            theFit.SetParLimits(3,0.001,1)

        if self.label == "6070":
            theFit.SetParLimits(0,5,20)
            theFit.SetParLimits(1,90,150)
            theFit.SetParLimits(2,20,50)
            theFit.SetParLimits(3,0.001,1)

        if self.label == "7080":
            theFit.SetParLimits(0,5,40)
            theFit.SetParLimits(1,90,170)
            theFit.SetParLimits(2,20,60)
            theFit.SetParLimits(3,0.001,1)

        if self.label == "80100":
            theFit.SetParLimits(0,5,50)
            theFit.SetParLimits(1,90,170)
            theFit.SetParLimits(2,20,60)
            theFit.SetParLimits(3,0.001,1)

        if self.label == "100120":
            theFit.SetParLimits(0,5,50)
            theFit.SetParLimits(1,90,170)
            theFit.SetParLimits(2,20,60) 
            theFit.SetParLimits(3,0.001,1)

        if self.label == "120150":
            theFit.SetParLimits(0,5,50)
            theFit.SetParLimits(1,60,170)
            theFit.SetParLimits(2,10,60)
            theFit.SetParLimits(3,0.001,1)

        if self.label == "150":
            theFit.SetParLimits(0,5,50)
            theFit.SetParLimits(1,70,170)
            theFit.SetParLimits(2,20,60)
            theFit.SetParLimits(3,0.001,1)

        cewk = TCanvas("cewk","",500,500)
        cewk.cd()
        cewk.SetLogy()

	norm = histo.Integral()

	histo.Scale(1/norm)

        histo.Fit(theFit,"R")
        
        theFit.SetRange(histo.GetXaxis().GetXmin(),histo.GetXaxis().GetXmax())
        theFit.SetLineStyle(2)
        theFit.Draw("same")

        self.parMCEWK = theFit.GetParameters()
        
        fitPars = "fit parameters "

	i = 0
	while i < numberOfParameters:
	    fitPars = fitPars + " " + str(self.parMCEWK[i])
	    thePlot.SetParameter(i,theFit.GetParameter(i))
	    i = i + 1
	thePlot.Draw("same")

        tex = TLatex(0.2,0.2,"EWK MC, baseline TauID")
        tex.SetNDC()
        tex.Draw()

        cewk.Print("ewkfit"+self.label+".eps")
        
        self.parMCEWK = theFit.GetParameters()
        
#        fitPars = "fit parameters "
#        i = 0
#        while i < numberOfParameters:
#            fitPars = fitPars + " " + str(self.parMCEWK[i])
#            i = i + 1
        print fitPars
        self.nMCEWK = theFit.Integral(0,1000,self.parMCEWK)
        print "Integral ",norm*self.nMCEWK

    def fitData(self,histo):

	parInvQCD = self.parInvQCD
	parMCEWK  = self.parMCEWK
	nInvQCD   = self.nInvQCD
        nMCEWK    = self.nMCEWK

        class FitFunction:
            def __call__( self, x, par ):
                return par[0]*(par[1] * QCDFunction(x,parInvQCD,1/nInvQCD) + ( 1 - par[1] ) * EWKFunction(x,parMCEWK,1/nMCEWK))

	class QCDOnly:
	    def __call__( self, x, par ):
		return par[0]*par[1] * QCDFunction(x,parInvQCD,1/nInvQCD)

        rangeMin = histo.GetXaxis().GetXmin()
        rangeMax = histo.GetXaxis().GetXmax()
        numberOfParameters = 2
        
        print "Fit range ",rangeMin, " - ",rangeMax
        
        theFit = TF1("theFit",FitFunction(),rangeMin,rangeMax,numberOfParameters)
        
        c = TCanvas("c","",500,500)
        c.cd()
        c.SetLogy()
	print "data events ",histo.Integral()

        histo.Fit(theFit,"R")

        theFit.SetRange(histo.GetXaxis().GetXmin(),histo.GetXaxis().GetXmax())
        theFit.SetLineStyle(2)
        theFit.Draw("same")

	par = theFit.GetParameters()

	qcdOnly = TF1("qcdOnly",QCDOnly(),rangeMin,rangeMax,numberOfParameters)
	qcdOnly.FixParameter(0,par[0])
	qcdOnly.FixParameter(1,par[1])
	qcdOnly.SetLineStyle(2)
	qcdOnly.Draw("same")

        tex = TLatex(0.35,0.8,"Data, Baseline TauID")
        tex.SetNDC()
        tex.Draw()

        texq = TLatex(0.4,0.3,"QCD")
        texq.SetNDC() 
	texq.SetTextSize(15)
        texq.Draw()

        c.Print("combinedfit"+self.label+".eps")
        
        fitPars = "fit parameters "
        i = 0
        while i < numberOfParameters:
            fitPars = fitPars + " " + str(par[i])
            i = i + 1
        print fitPars
	self.nBaseQCD = par[0]
	self.QCDfraction = par[1]
	if len(self.label) > 0:
	    print "Bin ",self.label
        print "Integral     ", self.nBaseQCD
	print "QCD fraction ",self.QCDfraction

        return theFit


    def getNormalization(self):
	nQCDbaseline = self.nBaseQCD
	nQCDinverted = self.normInvQCD*self.nInvQCD
	QCDfractionInBaseLineEvents = self.QCDfraction
	normalizationForInvertedEvents = nQCDbaseline*QCDfractionInBaseLineEvents/nQCDinverted

	self.normFactors.append(normalizationForInvertedEvents)
	self.labels.append(self.label)

	print "\n"
	print "Normalizing to baseline TauID qcd fraction from a fit using inverted QCD MET distribution shape and EWK MC baseline shape"
	print "    Number of baseline QCD events       ",nQCDbaseline
	print "    QCD fraction in baseline QCD events ",QCDfractionInBaseLineEvents
        print "    Number of inverted QCD events       ",nQCDinverted 
	print "\n"
	print "Normalization for inverted QCD events   ",normalizationForInvertedEvents
	print "\n"
	return normalizationForInvertedEvents

    def Summary(self):
	if len(self.normFactors) == 0:
	    return

        print "Normalization factors for each bin"
        i = 0
	while i < len(self.normFactors):
	    label = self.labels[i]
	    while len(label) < 10:
		label = label  + " "
	    print "    Label",label,", normalization",self.normFactors[i]
	    i = i + 1


def main():
    # Create all datasets from a multicrab task
    datasets = dataset.getDatasetsFromMulticrabCfg(counters=counters)

    # Read integrated luminosities of data datasets from lumi.json
    datasets.loadLuminosities()

    # Include only 120 mass bin of HW and HH datasets
    datasets.remove(filter(lambda name: "TTToHplus" in name and not "M120" in name, datasets.getAllDatasetNames()))

    # Default merging nad ordering of data and MC datasets
    # All data datasets to "Data"
    # All QCD datasets to "QCD"
    # All single top datasets to "SingleTop"
    # WW, WZ, ZZ to "Diboson"
    plots.mergeRenameReorderForDataMC(datasets)

    # Set BR(t->H) to 0.05, keep BR(H->tau) in 1
    xsect.setHplusCrossSectionsToBR(datasets, br_tH=0.05, br_Htaunu=1)

    # Merge WH and HH datasets to one (for each mass bin)
    # TTToHplusBWB_MXXX and TTToHplusBHminusB_MXXX to "TTToHplus_MXXX"
    plots.mergeWHandHH(datasets)

    ttjets2 = datasets.getDataset("TTJets").deepCopy()
    ttjets2.setCrossSection(ttjets2.getCrossSection()-datasets.getDataset("TTToHplus_M120").getCrossSection())
    print "Set TTJets2 cross section to %f" % ttjets2.getCrossSection()
    ttjets2.setName("TTJets2")
    datasets.append(ttjets2)

    datasets.merge("EWKnott", [
            "WJets",
            "DYJetsToLL",
            "SingleTop",
            "Diboson"
            ])
    tmp = datasets.getDataset("EWKnott").deepCopy()
    tmp.setName("EWKnott2")
    datasets.append(tmp)

    datasets.merge("EWK", [
        "EWKnott",
        "TTJets"
        ])
    datasets.merge("EWKS", [
        "EWKnott2",
        "TTJets2",
        "TTToHplus_M120",
        ])


#     print "check xsec",datasets.getDataset("TTJets").getCrossSection()
#     datasets.getDataset("TTJets").setCrossSection((1-0.05)*(1-0.05)*datasets.getDataset("TTJets").getCrossSection())

#     print "check xsec",datasets.getDataset("TTJets").getCrossSection()

#     # Merge EWK datasets
#     datasets.merge("EWK", [
# 	    "TTToHplus_M120",
#             "WJets",
#             "TTJets",
#             "DYJetsToLL",
#             "SingleTop",
#             "Diboson"
#             ])



    # Apply TDR style
    style = tdrstyle.TDRStyle()

    # Create the normalized plot of transverse mass
    # Read the histogram from the file
    #mT = plots.DataMCPlot(datasets, analysis+"/transverseMass")

    # Create the histogram from the tree (and see the selections explicitly)
    td = dataset.TreeDraw(analysis+"/tree", weight="weightPileup*weightTrigger*weightPrescale",
                             selection="met_p4.Et() > 70 && Max$(jets_btag) > 1.7")

    invertedQCD = InvertedTauID()

    metBase = plots.DataMCPlot(datasets, analysis+"/MET_BaseLineTauIdJets")
    metInver = plots.DataMCPlot(datasets, analysis+"/MET_InvertedTauIdJets")  
    # Rebin before subtracting
    metBase.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
    metInver.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
    
    metInverted_data = metInver.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdJets")
    metInverted_EWK = metInver.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MET_InvertedTauIdJets") 
    metBase_data = metBase.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_BaselineTauIdJets")
    metBase_EWK = metBase.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MET_BaselineTauIdJets")

    metBase_QCD = metBase_data.Clone("QCD")
    metBase_QCD.Add(metBase_EWK,-1)

    invertedQCD.comparison(metInverted_data,metBase_QCD)
    invertedQCD.setLabel("inclusive")
    invertedQCD.fitQCD(metInverted_data)
    invertedQCD.fitEWK(metBase_EWK)  
    invertedQCD.fitData(metBase_data)
    normalizationWithEWK = invertedQCD.getNormalization()

    metBase_EWKS = metBase.histoMgr.getHisto("EWKS").getRootHisto().Clone(analysis+"/MET_BaselineTauIdJets")
    invertedQCD.fitEWK(metBase_EWKS)
    invertedQCD.fitData(metBase_data)
    normalizationWithEWKS = invertedQCD.getNormalization()

    print "Difference Signal vs no signal in EWK fit",(normalizationWithEWKS - normalizationWithEWK)/normalizationWithEWK


#    bins = ["4050","5060","6070","7080","80100","100120","120150","150"]
#    bins = ["4050","5060","6070","7080","80100","120150","150"]
    bins = ["100120"]

    for bin in bins:

        purkka = bin
        if bin == "100120":  
            purkka = "100150"

        metBase = plots.DataMCPlot(datasets, analysis+"/MET_BaseLineTauIdJets"+purkka)
#        metBase.createFrame("MET", opts={"ymin": 1e-6, "ymaxfactor": 10})
        metInver = plots.DataMCPlot(datasets, analysis+"/MET_InvertedTauIdJets"+bin)
        # Rebin before subtracting
        metBase.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
        metInver.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))

        metInverted_data = metInver.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdJets"+bin)
        metInverted_EWK = metInver.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MET_InvertedTauIdJets"+bin)
        metBase_data = metBase.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_BaselineTauIdJets"+bin)
        metBase_EWK = metBase.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MET_BaselineTauIdJets"+bin)

        metBase_QCD = metBase_data.Clone("QCD")
        metBase_QCD.Add(metBase_EWK,-1)

##    metInverted_data_bin40_70  = metInver.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdJets4070")
##    metInverted_data_bin70_150 = metInver.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdJets70150")
##    metInverted_data_bin150    = metInver.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdJets150")

	invertedQCD.setLabel(bin)
        invertedQCD.comparison(metInverted_data,metBase_QCD)
##    invertedQCD.comparison(metInverted_data_bin40_70,metInverted_data_bin70_150)
##    invertedQCD.comparison(metInverted_data_bin40_70,metInverted_data_bin150)
        invertedQCD.fitQCD(metInverted_data)
        invertedQCD.fitEWK(metBase_EWK)
        invertedQCD.fitData(metBase_data)
        invertedQCD.getNormalization()

    invertedQCD.Summary()


if __name__ == "__main__":
    main()
