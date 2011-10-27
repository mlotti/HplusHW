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
from time import sleep

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect

analysis = "signalAnalysis"
counters = analysis+"Counters"

def QCDFunction(x,par,norm):
    return norm*(par[0]*TMath.Gaus(x[0],par[1],par[2],1)+par[3]*TMath.Gaus(x[0],par[4],par[5],1)+par[6]*TMath.Exp(-par[7]*x[0]))

def EWKFunction(x,par,norm):
    return norm*(par[0]*TMath.Gaus(x[0],par[1],par[2],1)+par[3]*TMath.Gaus(x[0],par[4],par[5],1))

class InvertedTauID:


    def __call__( self):
	self.parInvQCD  = []
	self.parMCEWK   = []
	self.parBaseQCD = []

	self.nInvQCD  = 0
	self.nMCEWK   = 0
	self.nBaseQCD = 0

	self.normInvQCD  = 1

	self.QCDfraction = 0
	return

    def comparison(self,histo1,histo2):

        comp = TCanvas("comp","",500,500)
        comp.cd()
        comp.SetLogy()

	h1 = histo1.Clone("h1")
	h2 = histo2.Clone("h2")
	h1.Scale(1/h1.GetMaximum())
	h2.Scale(1/h2.GetMaximum())

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

        comp.Print("comparison.eps")


    def fitQCD(self,histo): 

        rangeMin = histo.GetXaxis().GetXmin()                                                                                                                                                            
        rangeMax = histo.GetXaxis().GetXmax()                                                                                                                                                            

        numberOfParameters = 8                                                                                                                                                                           

        print "Fit range ",rangeMin, " - ",rangeMax                                                                                                                                                      

	class FitFunction:
	    def __call__( self, x, par ):
		return QCDFunction(x,par,1)

        theFit = TF1('theFit',FitFunction(),rangeMin,rangeMax,numberOfParameters)                                                                                                                        

        theFit.SetParLimits(0,1,20)
        theFit.SetParLimits(1,20,30)
        theFit.SetParLimits(2,5,25)

        theFit.SetParLimits(3,0.1,10)
        theFit.SetParLimits(4,30,150)
        theFit.SetParLimits(5,10,100)
                                                                                                                                                                                                     
        theFit.SetParLimits(6,0.001,1)
        theFit.SetParLimits(7,0.001,0.05)

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

        cqcd.Print("qcdfit.eps")

                                                                                                                                                                                                     
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

        numberOfParameters = 6

        print "Fit range ",rangeMin, " - ",rangeMax
        
        class FitFunction:
            def __call__( self, x, par ):
                return EWKFunction(x,par,1)

        theFit = TF1('theFit',FitFunction(),rangeMin,rangeMax,numberOfParameters)

    	theFit.SetParLimits(0,1,10)
    	theFit.SetParLimits(1,80,120)
    	theFit.SetParLimits(2,20,60)
    	theFit.SetParLimits(3,0.01,1.)
	theFit.SetParLimits(4,50,250)
	theFit.SetParLimits(5,80,200)

#    	theFit.FixParameter(4,148.123806861)
#    	theFit.FixParameter(5,71.6160638087)
        
        cewk = TCanvas("cewk","",500,500)
        cewk.cd()
        cewk.SetLogy()

	norm = histo.Integral()

	histo.Scale(1/norm)
        histo.Fit(theFit,"R")
        
        theFit.SetRange(histo.GetXaxis().GetXmin(),histo.GetXaxis().GetXmax())
        theFit.SetLineStyle(2)
        theFit.Draw("same")

        tex = TLatex(0.2,0.2,"EWK MC, baseline TauID")
        tex.SetNDC()
        tex.Draw()

        cewk.Print("ewkfit.eps")
        
        self.parMCEWK = theFit.GetParameters()
        
        fitPars = "fit parameters "
        i = 0
        while i < numberOfParameters:
            fitPars = fitPars + " " + str(self.parMCEWK[i])
            i = i + 1
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

        c.Print("combinedfit.eps")
        
        fitPars = "fit parameters "
        i = 0
        while i < numberOfParameters:
            fitPars = fitPars + " " + str(par[i])
            i = i + 1
        print fitPars
	self.nBaseQCD = par[0]
	self.QCDfraction = par[1]
        print "Integral     ", self.nBaseQCD
	print "QCD fraction ",self.QCDfraction

        return theFit


    def getNormalization(self):
	nQCDbaseline = self.nBaseQCD
	nQCDinverted = self.normInvQCD*self.nInvQCD
	QCDfractionInBaseLineEvents = self.QCDfraction
	normalizationForInvertedEvents = nQCDbaseline*QCDfractionInBaseLineEvents/nQCDinverted

	print "\n"
	print "Normalizing to baseline TauID qcd fraction from a fit using inverted QCD MET distribution shape and EWK MC baseline shape"
	print "    Number of baseline QCD events       ",nQCDbaseline
	print "    QCD fraction in baseline QCD events ",QCDfractionInBaseLineEvents
        print "    Number of inverted QCD events       ",nQCDinverted 
	print "\n"
	print "Normalization for inverted QCD events   ",normalizationForInvertedEvents
	print "\n"
	return normalizationForInvertedEvents

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

    # Set BR(t->H) to 0.2, keep BR(H->tau) in 1
    xsect.setHplusCrossSectionsToBR(datasets, br_tH=0.05, br_Htaunu=1)

    # Merge WH and HH datasets to one (for each mass bin)
    # TTToHplusBWB_MXXX and TTToHplusBHminusB_MXXX to "TTToHplus_MXXX"
    plots.mergeWHandHH(datasets)

    # Merge EWK datasets
    datasets.merge("EWK", [
            "WJets",
            "TTJets",
            "DYJetsToLL",
            "SingleTop",
            "Diboson"
            ])

    # Apply TDR style
    style = tdrstyle.TDRStyle()

    # Create the normalized plot of transverse mass
    # Read the histogram from the file
    #mT = plots.DataMCPlot(datasets, analysis+"/transverseMass")

    # Create the histogram from the tree (and see the selections explicitly)
    td = dataset.TreeDraw(analysis+"/tree", weight="weightPileup*weightTrigger*weightPrescale",
                             selection="met_p4.Et() > 70 && Max$(jets_btag) > 1.7")

    metBase = plots.DataMCPlot(datasets, analysis+"/MET_BaseLineTauIdBtag")
    metInver = plots.DataMCPlot(datasets, analysis+"/MET_InvertedTauIdBtag")  
    # Rebin before subtracting
    metBase.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
    metInver.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
    
    metInverted_data = metInver.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdBtag")
    metInverted_EWK = metInver.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MET_InvertedTauIdBtag")
    metBase_data = metBase.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_BaselineTauIdBtag")
    metBase_EWK = metBase.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MET_BaselineTauIdBtag")

    metBase_QCD = metBase_data.Clone("QCD")
    metBase_QCD.Add(metBase_EWK,-1)

    invertedQCD = InvertedTauID()
    invertedQCD.comparison(metInverted_data,metBase_QCD)
    invertedQCD.fitQCD(metInverted_data)
    invertedQCD.fitEWK(metBase_EWK)
    invertedQCD.fitData(metBase_data)
    invertedQCD.getNormalization()



if __name__ == "__main__":
    main()
