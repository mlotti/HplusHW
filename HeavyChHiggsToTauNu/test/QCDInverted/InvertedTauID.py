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
import copy
import re,os
import datetime

import array

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShellStyles import *

analysis = "signalAnalysisInvertedTau"
#analysis = "signalAnalysis"
counters = analysis+"/counters"

def Linear(x,par):
    return par[0]*x[0] + par[1]

def ErrorFunction(x,par):
    return 0.5*(1 + TMath.Erf(par[0]*(x[0] - par[1])))

def ExpFunction(x,par):
    if (x[0] > 280 and x[0] < 300) or x[0] > 360:
        TF1.RejectPoint()
        return 0
    return par[0]*TMath.Exp(-x[0]*par[1])
def Gaussian(x,par):
    return par[0]*TMath.Gaus(x[0],par[1],par[2],1)
def DoubleGaussian(x,par):
    return par[0]*TMath.Gaus(x[0],par[1],par[2],1) + par[3]*TMath.Gaus(x[0],par[4],par[5],1)
def SumFunction(x,par):
    return par[0]*TMath.Gaus(x[0],par[1],par[2],1) + par[3]*TMath.Exp(-x[0]*par[4])

def QCDFunction(x,par,norm):
    return Rayleigh(x,par,norm)
#    return norm*(par[1]*x[0]/((par[0])*(par[0]))*TMath.Exp(-x[0]*x[0]/(2*(par[0])*(par[0])))+par[2]*TMath.Gaus(x[0],par[3],par[4],1)+par[5]*TMath.Exp(-par[6]*x[0]))

def Rayleigh(x,par,norm):
    if par[0]+par[1]*x[0] == 0.0:
	return 0
#    return norm*(x[0]/((par[0]+par[1]*x[0])*(par[0]+par[1]*x[0]))*TMath.Exp(-x[0]*x[0]/( 2*(par[0]+par[1]*x[0])*(par[0]+par[1]*x[0]) )))
#    return norm*(x[0]/((par[0])*(par[0]))*TMath.Exp(-x[0]*x[0]/( 2*(par[0]+par[1]*x[0])*(par[0]+par[1]*x[0]))))
    return norm*(par[1]*x[0]/((par[0])*(par[0]))*TMath.Exp(-x[0]*x[0]/(2*(par[0])*(par[0]))))
#    return norm*(par[1]*x[0]/((par[0])*(par[0]))*TMath.Exp(-x[0]*x[0]/(2*(par[0])*(par[0])))+par[2]*TMath.Gaus(x[0],par[3],par[4],1)+par[5]*TMath.Exp(-par[6]*x[0]))
                                                                                        
def EWKFunction(x,par,norm = 1,rejectPoints = 0):
#    if not rejectPoints == 0:
#        if (x[0] > 280 and x[0] < 300):
#	if (x[0] > 400):
#	if x[0] > 40 and x[0] < 60 :gx
#	if x[0] > 240 and x[0] < 260:
#	if  (x[0] > 180 and x[0] < 200) or (x[0] > 260 and x[0] < 320):
#	if  (x[0] > 100 and x[0] < 120) or (x[0] > 180 and x[0] < 200):
#	if  (x[0] > 60 and x[0] < 80) or (x[0] > 140 and x[0] < 160) or (x[0] > 180 and x[0] < 220) or (x[0] > 240 and x[0] < 360):
#	if  (x[0] > 40 and x[0] < 60) or (x[0] > 80 and x[0] < 100) or (x[0] > 120 and x[0] < 140) or (x[0] > 160 and x[0] < 180):
#            TF1.RejectPoint()
#            return 0
    value = 150
    if x[0] < value:
	return norm*par[0]*TMath.Gaus(x[0],par[1],par[2],1)
    C = norm*par[0]*TMath.Gaus(value,par[1],par[2],1)*TMath.Exp(value*par[3])
    return C*TMath.Exp(-x[0]*par[3])

def QCDEWKFunction(x,par,norm):
    if par[0]+par[1]*x[0] == 0.0:
        return 0
    return norm*(par[1]*x[0]/((par[0])*(par[0]))*TMath.Exp(-x[0]*x[0]/(2*(par[0])*(par[0])))+par[2]*TMath.Gaus(x[0],par[3],par[4],1)+par[5]*TMath.Exp(-par[6]*x[0]))

#def QCDFunction(x,par,norm):
#    return norm*(par[0]*TMath.Gaus(x[0],par[1],par[2],1)+par[3]*TMath.Gaus(x[0],par[4],par[5],1)+par[6]*TMath.Exp(-par[7]*x[0]))
#    return norm*(par[0]*TMath.Gaus(x[0],par[1],par[2],1))
#    return norm*(par[0]*TMath.Gaus(x[0],par[1],par[2],1)+par[3]*TMath.Gaus(x[0],par[4],par[5],1))
#    return norm*(par[0]*TMath.Gaus(x[0],par[1],par[2],1)+par[3]*TMath.Exp(-par[4]*x[0]))

def QCDFunctionFixed(x,par):
    return par[0]*(TMath.Gaus(x[0],par[1],par[2],1)+par[3]*TMath.Gaus(x[0],par[4],par[5],1)+par[6]*TMath.Exp(-par[7]*x[0]))


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

    def __init__(self):
	self.parInvQCD  = []
	self.parMCEWK   = []
	self.parBaseQCD = []

	self.nInvQCD    = 0.0
        self.nFitInvQCD = 0.0
	self.nMCEWK     = 0.0
	self.nBaseQCD   = 0.0

	self.normInvQCD  = 1.0
	self.normEWK     = 1.0

	self.QCDfraction = 0.0

	self.label = ""
	self.labels = []
	self.normFactors = []
	self.normFactorsEWK = []
	self.lumi = 0.0

	# Limits for warning about a bad fit
	self._minGoodNormalisedChi2ForFit = 0.1
	
	# Parameters for fitting (use 'max' for maximum from histogram range)
	self._metFitRangeMin = 0.0 # FIXME this should be obtained automatically from the parameterset object in the root files
	self._metFitRangeMaxForCutEfficiency = 75.0
	self._metFitRangeMaxForQCDFit = "max"
	self._metFitRangeMaxForEWKFit = "max"
	self._metFitRangeMaxForDataFit = "max"
	self._metFitRangeMaxForBaselineDataFit = "max"
	
	self.errorBars = False

    def setLabel(self, label):
	self.label = label

    def setLumi(self, lumi):
	self.lumi = lumi

    def useErrorBars(self, useHistoErrors):
	self.errorBars = useHistoErrors

    ## Returns the maximum range for fitting
    def _getMaxRangeForFit(self, parameter, histo):
        if parameter == "max":
            return histo.GetXaxis().GetXmax()
        else:
            return parameter
	
    ## Check goodness of fit
    def _checkGoodnessOfFit(self, fitResultPtr, methodName, binName):
        # Check fit convergence
        if fitResultPtr.Status() != 0:
            print ErrorLabel()+"Fit did not converge in method '%s' for bin '%s'!"%(methodName, binName)
        else:
            if fitResultPtr.Ndf() > 0:
                nchi2 = fitResultPtr.Chi2() / fitResultPtr.Ndf()
                if nchi2 < self._minGoodNormalisedChi2ForFit or nchi2 > 1.0 / self._minGoodNormalisedChi2ForFit:
                    print ErrorLabel()+"Fit quality is very bad (chi2 / ndf = %f) for method '%s' and bin '%s'!"%(nchi2, methodName, binName)
	
    def plotIntegral(self, plot_orig, objectName, canvasName = "Integral"):

#        plot = copy.deepcopy(plot_orig)
        plot = plot_orig
 
        st = styles.getDataStyle().clone()
        st.append(styles.StyleFill(fillColor=ROOT.kYellow))

	plot.histoMgr.forHisto(objectName, st)
	plot.setFileName(plot.cf.canvas.GetName()+canvasName)
        
	plot.draw()
        plot.save()

        st.append(styles.StyleFill(fillColor=0))
        plot.histoMgr.forHisto(objectName, st)
        


    def efficiency(self,histo1,histo2,name,norm=1,ratio=True):

	h1 = histo1.Clone("h1")
	h2 = histo2.Clone("h2")
#	if norm == 1:
#        h1.Scale(1/h1.GetMaximum())
#        h2.Scale(1/h2.GetMaximum())

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


        h1.GetYaxis().SetTitle("Events / 4 GeV")
        h1.GetXaxis().SetTitle("MET (GeV)")
        

              
        plot = plots.ComparisonPlot(
            histograms.Histo(h1, "Inv"),
            histograms.Histo(h2, "Base"),
            )
    
            # Set the styles

        st1 = styles.getDataStyle().clone()
        st2 = st1.clone()
        st2.append(styles.StyleMarker(markerColor=ROOT.kRed))
	plot.histoMgr.forHisto("Base", st1)
        plot.histoMgr.forHisto("Inv", st2)
        
        # Set the legend labels
#        plot.histoMgr.setHistoLegendLabelMany({"Inv": h1.GetTitle(), "Base": h2.GetTitle()})
        
           
        plot.histoMgr.setHistoLegendLabelMany({"Inv": "Inverted","Base": "Baseline - EWK "})

            
        if "MetBtaggingEfficiency" in name:
           plot.histoMgr.setHistoLegendLabelMany({"Inv": "After b tagging","Base": "After #tau ID "})
           
        if "MetBvetoEfficiency" in name:
           plot.histoMgr.setHistoLegendLabelMany({"Inv": "After b-jet veto","Base": "After #tau ID "})

           
       # Set the legend styles
        plot.histoMgr.setHistoLegendStyleAll("P")
    
        
        # Set the drawing styles
        plot.histoMgr.setHistoDrawStyleAll("EP")
                

        # Create frame with a ratio pad
        

        if "MetBtaggingEfficiency"  in name:
            plot.createFrame("Efficiency"+self.label, opts={"ymin":0.1, "xmax": 300},
                             createRatio=True, opts2={"ymin": 0.01, "ymax": 1}, # bounds of the ratio plot
                             )
        if "MetBvetoEfficiency"  in name:
            plot.createFrame("Efficiency"+self.label, opts={"ymin":0.1, "xmax": 300},
                             createRatio=True, opts2={"ymin": 0.1, "ymax": 2}, # bounds of the ratio plot
                             )       
            
        # Set Y axis of the upper pad to logarithmic
           
               
    
        if "MetBtaggingEfficiency"  in name:
            plot.getPad1().SetLogy(True)
            plot.getPad2().SetLogy(True)
        if "MetBvetoEfficiency"  in name:
            plot.getPad1().SetLogy(True)
            plot.getPad2().SetLogy(True)
 #       if "BjetsInvertedVsBaseline"  in name:
 #           plot.getPad1().SetLogy(False)


            
        if ratio: 
            plot.setLegend(histograms.createLegend(0.55,0.75,0.95,0.90))
        
        if "MetBtaggingEfficiency" in name:            
            plot.setLegend(histograms.createLegend(0.55,0.75,0.95,0.90))
        if "MetBvetoEfficiency" in name:            
            plot.setLegend(histograms.createLegend(0.55,0.75,0.95,0.90))
  
  
        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        histograms.addLuminosityText(x=None, y=None, lumi=self.lumi)

        if "JetsInvertedVsBaselineAfterMet" in name:
            histograms.addText(0.6, 0.72, "After MET cut", 25)

        if "MtbvetoAllDeltaPhiCuts"  in name:
            histograms.addText(0.25, 0.4, "B-tagging factorisation", 23)
            histograms.addText(0.25, 0.3, "#Delta#phi(#tau jet,MET) vs #Delta#phi(jet1/2/3,MET) cuts", 20)
        
            
        plot.draw()
        plot.save()


        
    def controlPlots(self,histo1,histo2,name,norm=1,ratio=True):

	h1 = histo1.Clone("h1")
	h2 = histo2.Clone("h2")
#	if norm == 1:
#        h1.Scale(1/h1.GetMaximum())
#        h2.Scale(1/h2.GetMaximum())

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


        h1.GetYaxis().SetTitle("Events / 20 GeV")
        h1.GetXaxis().SetTitle("m_{T}(#tau jet, MET) (GeV)")
        
        if "MetInvertedVsBaselineTailKiller"  in name:
            h1.GetYaxis().SetTitle("Events / 10 GeV")
            h1.GetXaxis().SetTitle("MET  (GeV)")

        if "DphiInvertedVsBaseline"  in name:
           h1.GetYaxis().SetTitle("Events / 20 ^{o}")
           h1.GetXaxis().SetTitle("#Delta#phi(#tau jet, MET) (^{o})")

        if "BjetsInvertedVsBaseline"  in name:
            h1.GetYaxis().SetTitle("Events")
            h1.GetXaxis().SetTitle("N^{tagged b jets}")

        if "JetsInvertedVsBaseline"  in name:
            h1.GetYaxis().SetTitle("Events")
            h1.GetXaxis().SetTitle("N^{jets}")
            
        if "JetsInvertedVsBaselineAfterMet"  in name:
            h1.GetYaxis().SetTitle("Events")
            h1.GetXaxis().SetTitle("N^{jets}")

              
        plot = plots.ComparisonPlot(
            histograms.Histo(h1, "Inv"),
            histograms.Histo(h2, "Base"),
            )
    
            # Set the styles

        st1 = styles.getDataStyle().clone()
        st2 = st1.clone()
        st2.append(styles.StyleMarker(markerColor=ROOT.kRed))
	plot.histoMgr.forHisto("Base", st1)
        plot.histoMgr.forHisto("Inv", st2)
        
        # Set the legend labels
#        plot.histoMgr.setHistoLegendLabelMany({"Inv": h1.GetTitle(), "Base": h2.GetTitle()})
        
           
        plot.histoMgr.setHistoLegendLabelMany({"Inv": "Inverted","Base": "Baseline - EWK "})

            
        if "MtBvetoBtagInvertedTailKillerClosure" in name:
           plot.histoMgr.setHistoLegendLabelMany({"Inv": "b-jet veto ","Base": "b tagging "})


           
       # Set the legend styles
        plot.histoMgr.setHistoLegendStyleAll("P")
    
        
        # Set the drawing styles
        plot.histoMgr.setHistoDrawStyleAll("EP")
                

        # Create frame with a ratio pad
        

        if "MtInvertedVsBaselineTailKiller"  in name:
            plot.createFrame("controlPlot"+self.label, opts={"ymin":-2,"ymax":15, "xmax": 300},
                             createRatio=ratio, opts2={"ymin": 0, "ymax": 2}, # bounds of the ratio plot
                             )
            
        if "MetInvertedVsBaselineTailKiller"  in name:
            plot.createFrame("controlPlot"+self.label, opts={ "ymin": 0.01, "ymaxfactor": 2, "xmax": 400}, log=True,
                             createRatio=ratio, opts2={"ymin": 0, "ymax": 2}, # bounds of the ratio plot
                             ) 
        if "DphiInvertedVsBaseline"  in name:
            plot.createFrame("controlPlot"+self.label, opts={"ymin":-2,"ymax":30, "xmax": 180},
                             createRatio=ratio, opts2={"ymin": 0, "ymax": 2}, # bounds of the ratio plot
                             )

        if "BjetsInvertedVsBaseline"  in name:
            plot.createFrame("controlPlot"+self.label, opts={"ymin":0.01,"ymaxfactor":2, "xmax": 10}, 
                             createRatio=ratio, opts2={"ymin": 0, "ymax": 2}, # bounds of the ratio plot
                             )

        if "JetsInvertedVsBaseline"  in name:
            plot.createFrame("controlPlot"+self.label, opts={"ymin":0.01,"ymaxfactor":2, "xmax": 12}, log=True,
                             createRatio=ratio, opts2={"ymin": 0, "ymax": 2}, # bounds of the ratio plot
                             )
            
        if "JetsInvertedVsBaselineAfterMet"  in name:
            plot.createFrame("controlPlot"+self.label, opts={"ymin":0.01,"ymaxfactor":2, "xmax": 12},
                             createRatio=ratio, opts2={"ymin": 0, "ymax": 2}, # bounds of the ratio plot
                             )
            
        # Set Y axis of the upper pad to logarithmic
           
               
    
        if "MetInvertedVsBaselineTailKiller"  in name:
            plot.getPad1().SetLogy(True)
 #       if "BjetsInvertedVsBaseline"  in name:
 #           plot.getPad1().SetLogy(False)
        if "JetsInvertedVsBaseline"  in name:
            plot.getPad1().SetLogy(True)
        if "JetsInvertedVsBaselineAfterMet"  in name:
            plot.getPad1().SetLogy(True)

            
        if ratio: 
            plot.setLegend(histograms.createLegend(0.55,0.75,0.95,0.90))
        
        if "MtInvertedVsBaselineTailKiller" in name:            
            plot.setLegend(histograms.createLegend(0.55,0.75,0.95,0.90))

        if "DphiInvertedVsBaseline" in name:            
            plot.setLegend(histograms.createLegend(0.35,0.75,0.75,0.90))
  
        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        histograms.addLuminosityText(x=None, y=None, lumi=self.lumi)

        if "JetsInvertedVsBaselineAfterMet" in name:
            histograms.addText(0.6, 0.72, "After MET cut", 25)

        if "MtbvetoAllDeltaPhiCuts"  in name:
            histograms.addText(0.25, 0.4, "B-tagging factorisation", 23)
            histograms.addText(0.25, 0.3, "#Delta#phi(#tau jet,MET) vs #Delta#phi(jet1/2/3,MET) cuts", 20)
        
        
    def mtComparison(self,histo1,histo2,name,norm=1,sysError=0):

	h1 = histo1.Clone("h1")
	h2 = histo2.Clone("h2")

	if sysError > 0:
	    h1 = histograms.addSysError(h1,sysError)
	    #h2 = histograms.addSysError(h2,sysError)

#	if norm == 1:
#        h1.Scale(1/h1.GetMaximum())
#        h2.Scale(1/h2.GetMaximum())

	# check that no bin has negative value, negative values possible after subtracting EWK from data  
        iBin = 1
        nBins = h1.GetNbinsX()
        while iBin < nBins:
	    value1 = h1.GetBinContent(iBin)
	    value2 = h2.GetBinContent(iBin)

	    #if value1 < 0:
		#h1.SetBinContent(iBin,0)

            #if value2 < 0:
             #   h2.SetBinContent(iBin,0)

            iBin = iBin + 1


        h1.GetYaxis().SetTitle("Events / 20 GeV")
        h1.GetXaxis().SetTitle("m_{T}(#tau jet, MET) (GeV)")

            
        if "MetBtagging"  in name:
            h1.GetYaxis().SetTitle("Events")
            h1.GetXaxis().SetTitle("MET (GeV)")
            
        if "MtSoftBtaggingTKClosure" in name:           
            h1.GetYaxis().SetTitle("Events / 20 CeV")
            h1.GetXaxis().SetTitle("m_{T}(#tau jet,MET) (GeV)")
            
            
        if "BvetoInvertedVsBaseline"  or "NormalisedBveto" in name:
            h1.GetYaxis().SetTitle("Events / 20 CeV")
            h1.GetXaxis().SetTitle("m_{T}(#tau jet,MET) (GeV)")
            
        if "BtagToBvetoEffVsMet"  in name:
            h1.GetYaxis().SetTitle("Events / 10 GeV")
            h1.GetXaxis().SetTitle("MET (GeV)")
            
        if "BtagToBvetoEffVsMt" or "BtagToBvetoEffNoMetVsMt" in name:
            h1.GetYaxis().SetTitle("Events / 20 GeV")
            h1.GetXaxis().SetTitle("m_{T}(#tau jet,MET) (GeV)")

        if "MtbvetoAllDeltaPhiCuts"  in name:
            h1.GetYaxis().SetTitle("QCD purity")
            h1.GetXaxis().SetTitle("m_{T}(#tau jet,MET) (GeV)")
            
        if "MtNormalisedBvetoTailKiller" in name:      
            h1.GetYaxis().SetTitle("Events / 20 CeV")
            h1.GetXaxis().SetTitle("m_{T}(#tau jet,MET) (GeV)")

        if "MtAfterJetsInvertedVsBaseline" in name:
            h1.GetYaxis().SetTitle("Events / 20 CeV")
            h1.GetXaxis().SetTitle("m_{T}(#tau jet,MET) (GeV)")

        if "BtagEffVsMet"  in name:
            h1.GetYaxis().SetTitle("Efficiency")
            h1.GetXaxis().SetTitle("MET (GeV)")           

        if "MtNoBtaggingInvertedVsBaselineTailKillerClosure" in name:
            h1.GetYaxis().SetTitle("Events / 20 CeV")
            h1.GetXaxis().SetTitle("m_{T}(#tau jet,MET) (GeV)")
        if "RadiusJet0BackToBack" in name:
            h1.GetYaxis().SetTitle("Events ")
            h1.GetXaxis().SetTitle("#sqrt{(180^{o}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{0},MET)^{2}}")
        if "RadiusJet0Collinear"  in name:
            h1.GetYaxis().SetTitle("Events ")
            h1.GetXaxis().SetTitle("#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{o}-#Delta#phi(jet_{0},MET))^{2}}")
        if "RadiusJet1BackToBack"  in name:
            h1.GetYaxis().SetTitle("Events ")
            h1.GetXaxis().SetTitle("#sqrt{(180^{o}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{1},MET)^{2}}")
        if "RadiusJet1Collinear" in name:
            h1.GetYaxis().SetTitle("Events ")
            h1.GetXaxis().SetTitle("#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{o}-#Delta#phi(jet_{1},MET))^{2}}")
        if "RadiusJet2BackToBack" in name:
            h1.GetYaxis().SetTitle("Events ")
            h1.GetXaxis().SetTitle("#sqrt{(180^{o}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{2},MET)^{2}}")
        if "RadiusJet2Collinear" in name:
            h1.GetYaxis().SetTitle("Events ")
            h1.GetXaxis().SetTitle("#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{o}-#Delta#phi(jet_{2},MET))^{2}}")           
            
        plot = plots.ComparisonPlot(
            histograms.Histo(h1, "Inv"),histograms.Histo(h2, "Base"),
            )



            
            # Set the styles

        st1 = styles.getDataStyle().clone()
        st2 = st1.clone()
        st2.append(styles.StyleMarker(markerColor=ROOT.kRed))
	plot.histoMgr.forHisto("Base", st1)
        plot.histoMgr.forHisto("Inv", st2)
        
        # Set the legend labels
        plot.histoMgr.setHistoLegendLabelMany({"Inv": h1.GetTitle(), "Base": h2.GetTitle()})
#        plot.histoMgr.setHistoLegendLabelMany({"Inv": "with b tagging","Base": "with b-jet veto"})
        if "InvertedVsBaseline"  in name:
            plot.histoMgr.setHistoLegendLabelMany({"Inv": "Inverted","Base": "Baseline"})
 
    
        if "NormalisedBveto"  in name:    
            plot.histoMgr.setHistoLegendLabelMany({"Inv": "b tagging","Base": "b veto normalized "})
        if "NormalisedBvetoTailKiller"  in name:    
            plot.histoMgr.setHistoLegendLabelMany({"Inv": "b tagging","Base": "b veto normalized "})
    
        if "MtBvetoInvertedVsBaselineClosure"  in name:    
            plot.histoMgr.setHistoLegendLabelMany({"Inv": "Inverted","Base": "Baseline - EWK "})

        if "MtBvetoInvertedVsBaselineTailKillerClosure"  in name:    
            plot.histoMgr.setHistoLegendLabelMany({"Inv": "Inverted","Base": "Baseline - EWK "})
            
        if "MtBvetoBtagInvertedClosure" in name:
            plot.histoMgr.setHistoLegendLabelMany({"Inv": "b-jet veto ","Base": "b tagging "})
            
        if "MtBvetoBtagInvertedTailKillerClosure" in name:
           plot.histoMgr.setHistoLegendLabelMany({"Inv": "b-jet veto ","Base": "b tagging "})
           
        if "MtNormalisedBvetoTailKiller" in name:  
            plot.histoMgr.setHistoLegendLabelMany({"Inv": "b-jet veto ","Base": "b tagging "})

        if "MetBtagging"  in name:
            plot.histoMgr.setHistoLegendLabelMany({"Inv": "With b tagging ","Base": "After MET cut "})
        if "MtAfterJetsInvertedVsBaseline" in name:
            plot.histoMgr.setHistoLegendLabelMany({"Inv": "Inverted","Base": "Baseline - EWK "})
        if "MtBtagVsNoBtagNoMetInvertedTailKillerClosure" in name:
            plot.histoMgr.setHistoLegendLabelMany({"Inv": "no b tagging","Base": "b tagging "})
        if "MtNoBtaggingInvertedVsBaselineTailKillerClosure" in name:           
            plot.histoMgr.setHistoLegendLabelMany({"Inv": "Inverted","Base": "Baseline - EWK "})
        if "MtBtaggingNoBtaggingInverted" in name:
           plot.histoMgr.setHistoLegendLabelMany({"Inv": "no b tagging ","Base": " with b tagging "})
        if "MtInvertedVsBaselineSystematic" in name:      
            plot.histoMgr.setHistoLegendLabelMany({"Inv": "Inverted","Base": "Baseline"})
        if "MtBvetoInvertedVsBaselineTailKillerClosure" in name:
            plot.histoMgr.setHistoLegendLabelMany({"Inv": "Inverted","Base": "Baseline"})
        if "AfterMetPlusBveto" in name:
            plot.histoMgr.setHistoLegendLabelMany({"Inv": "Inverted","Base": "Baseline"})
        if "MtAllCutsClosure" in name: 
	    plot.histoMgr.setHistoLegendLabelMany({"Inv": "Inverted","Base": "Baseline"})
        if "MtAllCutsClosure" in name: 
	    plot.histoMgr.setHistoLegendLabelMany({"Inv": "Inverted","Base": "Baseline"})
        if "RadiusJet0BackToBack" in name:
            plot.histoMgr.setHistoLegendLabelMany({"Inv": "Inverted","Base": "Baseline"})
        if "RadiusJet0Collinear" in name:
            plot.histoMgr.setHistoLegendLabelMany({"Inv": "Inverted","Base": "Baseline"})
        if "RadiusJet1BackToBack" in name:
            plot.histoMgr.setHistoLegendLabelMany({"Inv": "Inverted","Base": "Baseline"})
        if "RadiusJet1Collinear" in name:
            plot.histoMgr.setHistoLegendLabelMany({"Inv": "Inverted","Base": "Baseline"})
        if "RadiusJet2BackToBack" in name:
            plot.histoMgr.setHistoLegendLabelMany({"Inv": "Inverted","Base": "Baseline"})
        if "RadiusJet2Collinear" in name:
            plot.histoMgr.setHistoLegendLabelMany({"Inv": "Inverted","Base": "Baseline"})
        if "AfterMetPlusSoftBtagging" in name: 
            plot.histoMgr.setHistoLegendLabelMany({"Inv": "Inverted","Base": "Baseline"})
        if "NoBtaggingTailKillerClosure" in name: 
            plot.histoMgr.setHistoLegendLabelMany({"Inv": "Inverted","Base": "Baseline"})
        if "AfterCollinearCuts" in name:
            plot.histoMgr.setHistoLegendLabelMany({"Inv": "Inverted","Base": "Baseline"})
        if "AllCuts" in name:
            plot.histoMgr.setHistoLegendLabelMany({"Inv": "Inverted","Base": "Baseline"})
        if "AfterMetPlusBveto" in name:
            plot.histoMgr.setHistoLegendLabelMany({"Inv": "Inverted","Base": "Baseline"})
        if "AfterMetCut" in name:
            plot.histoMgr.setHistoLegendLabelMany({"Inv": "Inverted","Base": "Baseline"})   
       # Set the legend styles
        plot.histoMgr.setHistoLegendStyleAll("P")
    
        
        # Set the drawing styles
        plot.histoMgr.setHistoDrawStyleAll("EP")

                

        # Create frame with a ratio pad

       # if "test1"  in name:
        plot.createFrame("Comparison"+self.label, opts={"ymin":0.0, "xmax": 300},
                         createRatio=False,  opts2={"ymin": 0, "ymax": 2})  # bounds of the ratio plot

            
        if "MetBtaggingEfficiency"  in name:
            plot.createFrame("Efficiency"+self.label, opts={"ymin":0.0, "xmax": 300},
                             createRatio=True,  opts2={"ymin": 0, "ymax": 2})  # bounds of the ratio plot
                        
        if "NjetInvertedVsBaseline"  in name:
            plot.createFrame("Jets"+self.label, opts={"ymin":0, "xmax": 30},
                             createRatio=False,  opts2={"ymin": 0, "ymax": 2})  # bounds of the ratio plot
            

        
  
#####################################
            
        if "MtAfterJetsInvertedVsBaselineTailKillerClosure" in name:
            plot.createFrame("Comparison"+self.label, opts={"ymin":1e-1, "ymax": 600, "xmax": 300},
                             createRatio=True, opts2={"ymin": 0, "ymax": 2}, # bounds of the ratio plot
                            )
        if "MtBtagVsNoBtagNoMetInvertedTailKillerClosure" in name:
            plot.createFrame("Comparison"+self.label, opts={"ymin":0, "ymax": 1.2, "xmax": 300},
                             createRatio=True, opts2={"ymin": 0, "ymax": 2}, # bounds of the ratio plot
                            )
        if "MtBtagVsNoBtagNoMetInvertedTailKillerClosure" in name:
            plot.createFrame("Comparison"+self.label, opts={"ymin":0, "ymax": 1.2, "xmax": 300},
                             createRatio=True, opts2={"ymin": 0, "ymax": 2}, # bounds of the ratio plot
                            )            
        if "MtNoBtagBtagInvertedTailKillerClosure" in name:
            plot.createFrame("Comparison"+self.label, opts={"ymin":0, "ymax": 1.2, "xmax": 300},
                             createRatio=True, opts2={"ymin": 0, "ymax": 2}, # bounds of the ratio plot
                             )
            
        if "MtNoBtaggingInvertedVsBaselineTailKillerClosure" in name:
            plot.createFrame("Comparison"+self.label, opts={"ymin":-2, "ymax": 200, "xmax": 300},
                             createRatio=True, opts2={"ymin": 0, "ymax": 2}, # bounds of the ratio plot
                             )
            
        if "MtBvetoInvertedVsBaselineMetCutTailKillerClosure" in name:
            plot.createFrame("Comparison"+self.label, opts={"ymin":-2, "ymax": 50, "xmax": 300},
                             createRatio=True, opts2={"ymin": 0, "ymax": 2}, # bounds of the ratio plot
                             )
            
        if "MtBvetoInvertedVsBaselineClosure"  in name:           
            plot.createFrame("Comparison"+self.label, opts={"ymin":1e-1,"ymax":800, "xmax": 300},
                             createRatio=True, opts2={"ymin": 0, "ymax": 2}, # bounds of the ratio plot
                             )
            
        if "MtBvetoInvertedVsBaselineTailKillerClosure" in name:
            plot.createFrame("Comparison"+self.label, opts={"ymin":1e-1, "ymax": 600, "xmax": 200},
                             createRatio=True, opts2={"ymin": 0, "ymax": 2}, # bounds of the ratio plot
                             )

##################################
        if "AfterMetPlusBveto" in name:
            plot.createFrame("mtClosure"+self.label, opts={"ymin":-5, "ymax": 40, "xmax": 300},
                             createRatio=True, opts2={"ymin": 0, "ymax": 2}, # bounds of the ratio plot)
                           )
                      
        if "AfterMetPlusSoftBtagging" in name:
            plot.createFrame("mtClosure"+self.label, opts={"ymin":-5, "ymax": 30, "xmax": 200},
                             createRatio=True, opts2={"ymin": 0, "ymax": 2}, # bounds of the ratio plot
                             )
 ############################                            
            
        if "AfterMetCut" in name:
            plot.createFrame("mtClosure"+self.label, opts={"ymin":-5, "ymax": 50, "xmax": 200},
                             createRatio=True, opts2={"ymin": 0, "ymax": 2}, # bounds of the ratio plot
                             )
        if "AfterCollinearCuts" in name:
            plot.createFrame("mtClosure"+self.label, opts={"ymin":-5, "ymax": 1000, "xmax": 200},
                             createRatio=True, opts2={"ymin": 0, "ymax": 2}, # bounds of the ratio plot
                             )                                      

            
        if "MtNoMetBvetoInvertedVsBaselineTailKillerClosure" in name:
            plot.createFrame("Comparison"+self.label, opts={"ymin":1e-1, "ymax": 500, "xmax": 200},
                             createRatio=True, opts2={"ymin": 0, "ymax": 2}, # bounds of the ratio plot
                             )

            
        if "AllCuts" in name:         
            plot.createFrame("mtClosure"+self.label, opts={"ymin":1e-1, "ymax": 10, "xmax": 200},
                             createRatio=True, opts2={"ymin": 0, "ymax": 2}, # bounds of the ratio plot
                             )

            
        if "MtPhiCutNormalisedBveto" in name:
            plot.createFrame("comparison"+self.label, opts={"ymin":1e-1,"ymax": 50, "ymaxfactor": 0.2, "xmax": 300},
                             createRatio=True, opts2={"ymin": 0, "ymax": 2}, # bounds of the ratio plot
                             )
        if "mtBTagVsBvetoInverted" in name:
            plot.createFrame("comparison"+self.label, opts={"ymin":1e-1, "ymax":100,"xmax": 300},
                             createRatio=True, opts2={"ymin": 0, "ymax": 2}, # bounds of the ratio plot
                             )
   
 

            
        if "MtBvetoBtagInvertedTailKillerClosure" in name:
            plot.createFrame("comparison"+self.label, opts={"ymin":1e-1,  "ymin":0, "ymax":1.2, "xmax": 300},
                             createRatio=True, opts2={"ymin": 0, "ymax": 2}, # bounds of the ratio plot
                             )
            
        if "BtagToBvetoEffVsMet"  in name:
            plot.createFrame("efficiency"+self.label, opts={"ymin":0.,"ymax":0.6, "xmax": 300},
                             createRatio=False,  opts2={"ymin": 0, "ymax": 2})  # bounds of the ratio plot
            
        if "BtagToBvetoEffVsMt"  in name:
            plot.createFrame("efficiency"+self.label, opts={"ymin":0.,"ymax":0.3, "xmax": 300},
                             createRatio=False,  opts2={"ymin": 0, "ymax": 2})  # bounds of the ratio plot

        if "BtagToBvetoEffNoMetVsMt"  in name:
            plot.createFrame("efficiency"+self.label, opts={"ymin":0.,"ymax":0.3, "xmax": 300},
                             createRatio=False,  opts2={"ymin": 0, "ymax": 2})  # bounds of the ratio plot
            
            
        if "MtbvetoAllDeltaPhiCuts"  in name:
            plot.createFrame("purity"+self.label, opts={"ymin":0.2,"ymax":1.0, "xmax": 300},
                             createRatio=False,  opts2={"ymin": 0, "ymax": 2})  # bounds of the ratio plot

        if "BtagEffVsMet"  in name:
            plot.createFrame("efficiency"+self.label, opts={"ymin":0.,"ymax":0.4, "xmax": 400},
                             createRatio=False,  opts2={"ymin": 0.1, "ymax": 2})  # bounds of the ratio plot

        if "MtInvertedVsBaselineSystematic" in name:      
            plot.createFrame("systematics"+self.label, opts={"ymin":0.,"ymax":15, "xmax": 300},
                             createRatio=True,  opts2={"ymin": 0.1, "ymax": 2})  # bounds of the ratio plot

        if "MtWithAllCutsTailKiller" in name:      
            plot.createFrame("mtPlot"+self.label, opts={"ymin":0.,"ymax":50, "xmax": 300},
                             createRatio=True,  opts2={"ymin": 0.1, "ymax": 2})  # bounds of the ratio plot
            
        if "RadiusJet0BackToBack"  in name:      
            plot.createFrame("Radius"+self.label, opts={"ymin":0.,"ymax":50, "xmax": 260},
                             createRatio=True,  opts2={"ymin": 0.1, "ymax": 2})  # bounds of the ratio plot
        if "RadiusJet1BackToBack"  in name:      
            plot.createFrame("Radius"+self.label, opts={"ymin":0.,"ymax":50, "xmax": 260},
                             createRatio=True,  opts2={"ymin": 0.1, "ymax": 2})  # bounds of the ratio plot
        if "RadiusJet2BackToBack"  in name:      
            plot.createFrame("Radius"+self.label, opts={"ymin":0.,"ymax":50, "xmax": 260},
                             createRatio=True,  opts2={"ymin": 0.1, "ymax": 2})  # bounds of the ratio plot
            
        if "RadiusJet0Collinear" in name:      
            plot.createFrame("Radius"+self.label, opts={"ymin":0.,"ymax":800, "xmax": 260},
                             createRatio=True,  opts2={"ymin": 0.1, "ymax": 2})  # bounds of the ratio plot
        if "RadiusJet1Collinear" in name:      
            plot.createFrame("Radius"+self.label, opts={"ymin":0.,"ymax":800, "xmax": 260},
                             createRatio=True,  opts2={"ymin": 0.1, "ymax": 2})  # bounds of the ratio plot
        if "RadiusJet2Collinear" in name:      
            plot.createFrame("Radius"+self.label, opts={"ymin":0.,"ymax":800, "xmax": 260},
                             createRatio=True,  opts2={"ymin": 0.1, "ymax": 2})  # bounds of the ratio plot
                       

        # Set Y axis of the upper pad to logarithmic
        if "Purity"  in name:        
            plot.getPad().SetLogy(False)       
        if "Factorised"  in name:        
            plot.getPad1().SetLogy(False)
        if "BtagEffInMet"  in name:
            plot.getPad1().SetLogy(True)
            
        if "MtNormalisedBvetoNoDphiCuts" in name:            
            plot.setLegend(histograms.createLegend(0.55,0.65,0.95,0.8))
        if "MtNormalisedBvetoTailKiller" in name:            
            plot.setLegend(histograms.createLegend(0.55,0.55,0.95,0.75))
        if "MtPhiCutNormalisedBveto" in name:            
            plot.setLegend(histograms.createLegend(0.5,0.75,0.95,0.9))

        if "MtBvetoBtagInvertedClosure" in name:            
            plot.setLegend(histograms.createLegend(0.5,0.75,0.95,0.9))

        if "MtBvetoInvertedVsBaselineClosure" in name:            
            plot.setLegend(histograms.createLegend(0.6,0.75,0.95,0.9))
            
        if "MtBvetoInvertedVsBaselineTailKillerClosure" in name:            
            plot.setLegend(histograms.createLegend(0.6,0.75,0.95,0.9))
            
        if "MtBvetoBtagInvertedClosure" in name:
            plot.setLegend(histograms.createLegend(0.6,0.75,0.95,0.9))
        if "MtBvetoBtagInvertedTailKillerClosure" in name:
            plot.setLegend(histograms.createLegend(0.6,0.75,0.95,0.9))
        if "MtAfterJetsInvertedVsBaselineTailKillerClosure" in name:
            plot.setLegend(histograms.createLegend(0.6,0.75,0.95,0.9))
            
        if "MtNoBtaggingInvertedVsBaselineTailKillerClosure" in name: 
            plot.setLegend(histograms.createLegend(0.6,0.75,0.95,0.9))
        if "MtBtaggingNoBtaggingInverted" in name:
            plot.setLegend(histograms.createLegend(0.6,0.75,0.95,0.9))
        if "MtInvertedVsBaselineSystematic" in name: 
            plot.setLegend(histograms.createLegend(0.6,0.75,0.95,0.9))
        if "MtNoMetBvetoInvertedVsBaselineTailKillerClosure" in name:
            plot.setLegend(histograms.createLegend(0.6,0.75,0.95,0.9))
        if "BvetoTailKillerClosure" in name:
            plot.setLegend(histograms.createLegend(0.6,0.75,0.95,0.9))
        if "RadiusJet0BackToBack" in name:
            plot.setLegend(histograms.createLegend(0.25,0.65,0.6,0.8))                           
        if "RadiusJet0Collinear"  in name:
            plot.setLegend(histograms.createLegend(0.25,0.65,0.6,0.8))
        if "RadiusJet1BackToBack" in name:
            plot.setLegend(histograms.createLegend(0.25,0.65,0.6,0.8))                           
        if "RadiusJet1Collinear"  in name:
            plot.setLegend(histograms.createLegend(0.25,0.65,0.6,0.8))
        if "RadiusJet2BackToBack"in name:
            plot.setLegend(histograms.createLegend(0.25,0.65,0.6,0.8))                           
        if "RadiusJet2Collinear" in name:
            plot.setLegend(histograms.createLegend(0.25,0.65,0.6,0.8))

        if "AfterMetPlusSoftBtagging" in name:
            plot.setLegend(histograms.createLegend(0.6,0.75,0.95,0.9))

        if "AfterMetCut" in name:
            plot.setLegend(histograms.createLegend(0.6,0.75,0.95,0.9))
        if "AfterCollinearCuts" in name:
            plot.setLegend(histograms.createLegend(0.6,0.75,0.95,0.9))
        if "AllCuts" in name:                     
            plot.setLegend(histograms.createLegend(0.6,0.75,0.95,0.9))
        if "AfterMetPlusBveto" in name:                     
            plot.setLegend(histograms.createLegend(0.6,0.75,0.95,0.9))


            
        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        histograms.addLuminosityText(x=None, y=None, lumi=self.lumi)
        
        if "MtNormalisedBvetoNoDphiCuts" in name:
            histograms.addText(0.3, 0.85, "Factorised b tagging/b veto", 25)
        if "MtNormalisedBvetoTailKiller" in name:
            histograms.addText(0.3, 0.88, "Factorised b tagging/b veto", 25)
            histograms.addText(0.3, 0.80, "TailKiller: TightPlus", 25)
        if "BtagToBvetoEffVsMet"  in name:
            histograms.addText(0.3, 0.8, "B tagging to B veto ratio", 25)
        if "BtagToBvetoEffVsMt"  in name:
            histograms.addText(0.3, 0.8, "B tagging to B veto ratio", 25)
        if "BtagToBvetoEffNoMetVsMt"  in name:
            histograms.addText(0.3, 0.8, "B tagging to B veto ratio", 25)
        if "MtPhiCutNormalisedBveto" in name:
            histograms.addText(0.6, 0.6, "#Delta#phi cuts", 30)
#        if "MtBvetoDphiInvertedVsBaseline"  in name:
#            histograms.addText(0.5, 0.6, "b-jet veto and #Delta#phi cuts", 25)
#        if "MtBvetoInvertedVsBaseline"  name:
#            histograms.addText(0.5, 0.6, "b-jet veto ", 25)
#        if "MtBvetoInvertedVsBaselineClosure"  in name:
#            histograms.addText(0.6, 0.6, "Before MET cut ", 24)
        if "MtBvetoInvertedVsBaselineClosure"  in name:
            histograms.addText(0.6, 0.52, "With b-jet veto ", 24)
        if "MtBvetoInvertedVsBaselineTailKillerClosure"  in name:
            histograms.addText(0.55, 0.6, "Before MET cut ", 24)
        if "MtBvetoInvertedVsBaselineTailKillerClosure"  in name:
            histograms.addText(0.55, 0.54, "With b-jet veto", 25)
        if "MtBvetoInvertedVsBaselineTailKillerClosure"  in name:
            histograms.addText(0.55, 0.48, "TailKiller: Tight", 25)

        if "MtBvetoBtagInvertedClosure" in name:
            histograms.addText(0.6, 0.6, "Before MET cut", 25)
        if "MtBvetoBtagInvertedClosure" in name:
            histograms.addText(0.6, 0.52, "Inverted #tau isolation", 25)

        if "MtBvetoBtagInvertedTailKillerClosure" in name:
            histograms.addText(0.55, 0.6, "Before MET cut", 24)

        if "MtBvetoBtagInvertedTailKillerClosure"  in name:
            histograms.addText(0.55, 0.48, "TailKiller: Tight", 24)
  




        if "MtAfterJetsInvertedVsBaselineTailKillerClosure" in name:
            histograms.addText(0.6, 0.65, "Before MET cut", 24)
            histograms.addText(0.6, 0.60, "No b tagging ", 24)
            histograms.addText(0.55, 0.53, "TailKiller: TightPlus", 24)
        if "MtBtagVsNoBtagNoMetInvertedTailKillerClosure" in name:
            histograms.addText(0.6, 0.60, "Before MET cut", 24)
            histograms.addText(0.6, 0.53, "TailKiller: Loose", 24)
        if "BtagEffVsMet"  in name:
            histograms.addText(0.5, 0.8, "Inverted #tau selection", 24)
            histograms.addText(0.5, 0.88, "B-tagging efficiency", 24)            
        if "MtNoBtaggingInvertedVsBaselineTailKillerClosure" in name:
            histograms.addText(0.6, 0.70, "After MET cut", 22)
            histograms.addText(0.6, 0.64, "No b tagging", 22)
            histograms.addText(0.6, 0.58, "TailKiller: Loose", 22)
        if "MtBtaggingNoBtaggingInverted" in name:
            histograms.addText(0.6, 0.67, "Inverted #tau selection", 22)
            histograms.addText(0.6, 0.6, "TailKiller: Loose", 22)
        if "MtInvertedVsBaselineSystematic" in name:   
            histograms.addText(0.6, 0.67, "All selection cuts", 22)
            histograms.addText(0.6, 0.6, "TailKiller: Loose", 22)
            
        if "MtNoMetBvetoInvertedVsBaselineTailKillerClosure" in name:
            histograms.addText(0.6, 0.70, "Before MET cut", 22)
            histograms.addText(0.6, 0.64, "B-jet veto", 22)
            histograms.addText(0.6, 0.58, "TailKiller: MediumPlus", 22)
            
        if "AfterMetPlusBveto" in name:
            #histograms.addText(0.6, 0.70, "After MET cut", 22)
            histograms.addText(0.6, 0.70, "with B-jet veto", 22)
            histograms.addText(0.6, 0.64, "LoosePlus", 22)

        if "MtWithAllCutsTailKiller" in name: 
            histograms.addText(0.6, 0.80, "All selection cuts", 22)
            histograms.addText(0.6, 0.70, "MET > 60 GeV", 22)
            histograms.addText(0.58, 0.69, "TailKiller: TightPlus", 22)
            #histograms.addText(0.6, 0.64, "no TailKiller cuts", 22)
            
        if "AllCuts" in name: 
            histograms.addText(0.2, 0.85, "All selection cuts", 22)
            #histograms.addText(0.6, 0.77, "MET > 60 GeV", 22)
            histograms.addText(0.2, 0.79, "LoosePlus", 22)
            #histograms.addText(0.6, 0.64, "no TailKiller cuts", 22)

        if "AfterMetCut" in name:
            histograms.addText(0.2, 0.85, "After MET cut", 20)
            histograms.addText(0.2, 0.75, "LoosePlus", 20)
            
        if "AfterMetPlusSoftBtagging" in name:
            histograms.addText(0.2, 0.85, "With loose b tagging", 20)
            #histograms.addText(0.2, 0.78, "MET >60 GeV", 20)
            histograms.addText(0.2, 0.78, "LoosePlus", 20)
            
        if "MtAllCutsClosure" in name:
            #histograms.addText(0.2, 0.85, "With loose b tagging", 20)
            
            histograms.addText(0.6, 0.8, "All selection cuts", 22)
            histograms.addText(0.6, 0.72, "MET > 60 GeV", 22)
            histograms.addText(0.55, 0.64, "TailKiller: TightPlus", 22)
            #histograms.addText(0.6, 0.64, "no TailKiller cuts", 22)
        if "AfterCollinearCuts" in name:
            histograms.addText(0.6, 0.7, "After jet selection", 20)
            histograms.addText(0.6, 0.65, "LoosePlus", 20)
########################################################
         
        if "RadiusJet0BackToBack" in name:      
            histograms.addText(0.25, 0.85, "All selection cuts", 22)
        if "RadiusJet1BackToBack"  in name:      
            histograms.addText(0.25, 0.85, "All selection cuts", 22)
        if "RadiusJet2BackToBack" in name:      
            histograms.addText(0.25, 0.85, "All selection cuts", 22)
            
        if "RadiusJet0Collinear"  in name:      
            histograms.addText(0.25, 0.85, "After jet selection", 22)
        if "RadiusJet1Collinear" in name:      
            histograms.addText(0.25, 0.85, "After jet selection", 22)
        if "RadiusJet2Collinear" in name:      
            histograms.addText(0.25, 0.85, "After jet selection", 22)
        if "MtSoftBtaggingTKClosure" in name:
            histograms.addText(0.2, 0.85, "With loose b tagging", 20)
 
                      
           
        plot.draw() 
        plot.save()

        

    def comparison(self,histo1,histo2,norm=1):

	h1 = histo1.Clone("h1")
	h2 = histo2.Clone("h2")
	if norm == 1:
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

	if norm > 0:
#	    h1.GetYaxis().SetTitle("Arbitrary units")
            h1.GetYaxis().SetTitle("Events / 5 GeV")
            h1.GetXaxis().SetTitle("MET (GeV)")
            
        plot = plots.ComparisonPlot(
            histograms.Histo(h1, "Inv"),
            histograms.Histo(h2, "Base"),
            )
            # Set the styles
        st1 = styles.getDataStyle().clone()
        st2 = st1.clone()
        st2.append(styles.StyleMarker(markerColor=ROOT.kRed))
	plot.histoMgr.forHisto("Base", st1)
        plot.histoMgr.forHisto("Inv", st2)
        
        # Set the legend labels
        plot.histoMgr.setHistoLegendLabelMany({"Inv": h1.GetTitle(),
                                               "Base": h2.GetTitle()})
        # Set the legend styles
        plot.histoMgr.setHistoLegendStyleAll("P")
        
        # Set the drawing styles
        plot.histoMgr.setHistoDrawStyleAll("EP")
        
        # Create frame with a ratio pad
        plot.createFrame("comparison"+self.label, opts={"ymin":1e-4, "ymaxfactor": 2, "xmax": 200},
                         createRatio=True, opts2={"ymin": 0, "ymax": 2}, # bounds of the ratio plot
                        )
        
        # Set Y axis of the upper pad to logarithmic
        plot.getPad1().SetLogy(True)

	plot.setLegend(histograms.createLegend(0.55,0.8,0.95,0.93))

        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        histograms.addLuminosityText(x=None, y=None, lumi=self.lumi)
        
        histograms.addText(0.25, 0.38, "After collinear cuts", 22)
        histograms.addText(0.25, 0.3, "2011AB", 22)

        
        plot.draw()
        plot.save()



          
 

    def cutefficiency(self,histo1,histo2):

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

	h1cut = h1.Clone("h1cut")
	h1cut.Reset()
	h1cut.GetYaxis().SetTitle("Efficiency")
        h1cut.GetXaxis().SetTitle("PF MET cut (GeV)")

        h2cut = h2.Clone("h2cut")
        h2cut.Reset()
	h2cut.SetLineColor(2)

        integralError = ROOT.Double(0.0)
	integralValue = h1.IntegralAndError(1,h1cut.GetNbinsX(),integralError)

        h1_integral = h1.Integral(0,h1.GetNbinsX())
	h2_integral = h2.Integral(0,h2.GetNbinsX())

	iBin = 1
	nBins = h1cut.GetNbinsX()
	while iBin < nBins:
	    error = ROOT.Double(0.0)
	    selected1 = h1.IntegralAndError(iBin,nBins,error)
	    if selected1 > 0:
		error = error/selected1
	    else:
		error = integralError/integralValue
	    efficiency1 = selected1/h1_integral
	    h1cut.SetBinContent(iBin,efficiency1)
	    if self.errorBars:
   	        h1cut.SetBinError(iBin,error)

            error = ROOT.Double(0.0)
            selected2 = h2.IntegralAndError(iBin,nBins,error)
	    if selected2 > 0:
		error = error/selected2
	    else:
		error = integralError/integralValue
            efficiency2 = selected2/h2_integral
            h2cut.SetBinContent(iBin,efficiency2)
	    if self.errorBars:
	        h2cut.SetBinError(iBin,error)

	    iBin = iBin + 1


        plot = plots.ComparisonPlot(
            histograms.Histo(h1cut, "Inv"),
            histograms.Histo(h2cut, "Base"),
            )
            # Set the styles
        st1 = styles.getDataStyle().clone()
        st2 = st1.clone()
        st2.append(styles.StyleLine(lineColor=ROOT.kRed))
	st2.append(styles.StyleMarker(markerColor=ROOT.kRed))
        plot.histoMgr.forHisto("Base", st1)
        plot.histoMgr.forHisto("Inv", st2)

        # Set the legend labels
        plot.histoMgr.setHistoLegendLabelMany({"Inv": h1.GetTitle(),
                                               "Base": h2.GetTitle()})
        # Set the legend styles
        #plot.histoMgr.setHistoLegendStyleAll("L")
	plot.histoMgr.setHistoLegendStyleAll("P")

        # Set the drawing styles
        #plot.histoMgr.setHistoDrawStyleAll("HIST")
        plot.histoMgr.setHistoDrawStyleAll("EP")

        # Create frame with a ratio pad
        plot.createFrame("cuteff"+self.label, opts={"ymin":1e-5, "ymaxfactor": 2, "xmax": 90},
                         createRatio=True, opts2={"ymin": 0, "ymax": 2}, # bounds of the ratio plot
                         )

        # Set Y axis of the upper pad to logarithmic
        plot.getPad().SetLogy(True)

        plot.setLegend(histograms.createLegend(0.4,0.82,0.9,0.93))
        
        histograms.addCmsPreliminaryText()
        histograms.addEnergyText() 
        histograms.addLuminosityText(x=None, y=None, lumi=self.lumi)

        plot.draw()
        plot.save()

        ######

        hError = h1cut.Clone("hError")
	hError.Divide(h2cut)

        iBin = 1
        nBins = hError.GetNbinsX()
        while iBin < nBins:
	    x = hError.GetBinCenter(iBin)
	    y = abs(hError.GetBinContent(iBin) - 1)
	    hError.SetBinContent(iBin,y)
	    print iBin,x,y
	    iBin = iBin + 1

        hError.GetYaxis().SetTitle("abs( (#varepsilon^{Inverted} - #varepsilon^{Baseline})/#varepsilon^{Baseline} )")
        hError.GetXaxis().SetTitle("PF MET cut (GeV)")



        plot2 = plots.PlotBase()
        plot2.histoMgr.appendHisto(histograms.Histo(hError,"ShapeUncertainty"))
        plot2.histoMgr.forHisto("ShapeUncertainty", st1)
        plot2.histoMgr.setHistoDrawStyleAll("EP")
#        plot2.createFrame("shapeUncertainty"+self.label, opts={"ymin":-1, "ymax": 1})

        plot2.createFrame("shapeUncertainty"+self.label, opts={"ymin":-0.1, "ymax": 1.1, "xmax": 90})

        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        histograms.addLuminosityText(x=None, y=None, lumi=self.lumi)
        histograms.addText(0.25, 0.8, "After collinear cuts", 22)
        histograms.addText(0.25, 0.7, "2011AB", 22)

        rangeMax = self._getMaxRangeForFit(self._metFitRangeMaxForCutEfficiency, hError)
        print "Fit range in 'cutefficiency()': %f - %f"%(self._metFitRangeMin, rangeMax)

        numberOfParameters = 2
        class FitFunction:
            def __call__( self, x, par ):
#                return Linear(x,par)
		return ErrorFunction(x,par)

        theFit = TF1('theFit',FitFunction(),self._metFitRangeMin,rangeMax,numberOfParameters)
        theFit.SetParLimits(0,0.01,0.05)
        theFit.SetParLimits(1,50,150)

#	theFit.FixParameter(0,0.02)
#	theFit.FixParameter(1,100)

	myFitResultPtr = hError.Fit(theFit,"LRNS")
	self._checkGoodnessOfFit(myFitResultPtr, "fitQCD()", histo.GetTitle())
	print "Error MET > 40",theFit.Eval(40)
	print "Error MET > 50",theFit.Eval(50)
       	print "Error MET > 60",theFit.Eval(60) 
	print "Error MET > 70",theFit.Eval(70)

	plot2.histoMgr.appendHisto(histograms.Histo(theFit,"Fit"))

	plot2.draw()
        plot2.save()

    def plotHisto(self,histo,canvasName):
        plot = plots.PlotBase()
        plot.histoMgr.appendHisto(histograms.Histo(histo,histo.GetName()))
        plot.createFrame(canvasName+self.label, opts={"ymin": 0.1, "ymaxfactor": 2.})

        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        histograms.addLuminosityText(x=None, y=None, lumi=self.lumi)

        plot.getPad().SetLogy(True)

        # FIXME: why calculate integral with 'width' -parameter?
        integralValue = int(0.5 + histo.Integral(0,histo.GetNbinsX(),"width"))
        histograms.addText(0.4,0.7,"Integral = %s ev"% integralValue) 

        # NOTE: assignment of nBaseQCD and nInvQCD is done at fitQCD and fitEWK (because someone could accidentally use this method to do something else ...)
        #match = re.search("/\S+baseline",histo.GetName(),re.IGNORECASE)
        #if match:
        #    self.nBaseQCD = integralValue
        #match = re.search("/\S+inverted",histo.GetName(),re.IGNORECASE)
        #if match:
        #    self.nInvQCD = integralValue

        self.plotIntegral(plot, histo.GetName())

    def fitQCD(self,histo):
        self.nInvQCD = histo.Integral(0,histo.GetNbinsX())

        parMCEWK   = self.parMCEWK
        nMCEWK     = self.nMCEWK

        class FitFunction:
            def __call__( self, x, par ):
                return QCDEWKFunction(x,par,1)

        class QCDOnly:
            def __call__( self, x, par ):
                return QCDFunction(x,par,1)

        numberOfParameters = 7

        rangeMax = self._getMaxRangeForFit(self._metFitRangeMaxForQCDFit, histo)
        print "Fit range for 'fitQCD()'",self._metFitRangeMin, " - ",rangeMax

        theFit = TF1("theFit",FitFunction(),self._metFitRangeMin,rangeMax,numberOfParameters)

        theFit.SetParameter(0,1);
        theFit.SetParLimits(0,0.0001,200)
        theFit.SetParameter(1,1);
        theFit.SetParLimits(1,0.001,10)
        theFit.SetParameter(2,2);
        theFit.SetParLimits(2,1,10)
        theFit.SetParameter(3,10);
        theFit.SetParLimits(3,0,150)
        theFit.SetParameter(4,20);
        theFit.SetParLimits(4,10,100)
        theFit.SetParameter(5,0.1);
        theFit.SetParLimits(5,0.0001,1)
        theFit.SetParameter(6,0.01);
        theFit.SetParLimits(6,0.001,0.05)

        gStyle.SetOptFit(0)

        plot = plots.PlotBase()
        plot.histoMgr.appendHisto(histograms.Histo(histo,histo.GetName()))
        plot.createFrame("qcdfit"+self.label, opts={"ymin": 1e-5, "ymaxfactor": 2.})

        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        histograms.addLuminosityText(x=None, y=None, lumi=self.lumi)

        self.normInvQCD = histo.Integral(0,histo.GetNbinsX())

        histo.Scale(1.0/self.normInvQCD)
        myFitResultPtr = histo.Fit(theFit,"LRS")
        self._checkGoodnessOfFit(myFitResultPtr, "fitQCD()", histo.GetTitle())

        theFit.SetRange(histo.GetXaxis().GetXmin(),histo.GetXaxis().GetXmax())
        theFit.SetLineStyle(2)
        theFit.Draw("same")

        par = theFit.GetParameters()

        numberOfQCDParameters = 2
        qcdOnly = TF1("qcdOnly",QCDOnly(),self._metFitRangeMin,rangeMax,numberOfQCDParameters)
        qcdOnly.FixParameter(0,par[0])
        qcdOnly.FixParameter(1,par[1])
        qcdOnly.SetLineStyle(2)
        qcdOnly.Draw("same")
        
        histograms.addText(0.4,0.8,"Inverted TauID")
        histograms.addText(0.4,0.25,"QCD",15)
                
        plot.histoMgr.appendHisto(histograms.Histo(theFit,"Fit"))
        plot.getPad().SetLogy(True)
        plot.draw()
        plot.save()

        self.parInvQCD = theFit.GetParameters()

        fitPars = "fit parameters "
        i = 0
        while i < numberOfParameters:
            fitPars = fitPars + " " + str(self.parInvQCD[i])
            i = i + 1
        print "QCD fit parameters",fitPars
        self.nFitInvQCD = theFit.Integral(0,1000,self.parInvQCD)
        print "Integral ",self.normInvQCD*self.nFitInvQCD


    def fitQCD_old(self,origHisto):
        
	histo = origHisto.Clone("histo")

        numberOfParameters = 7

        print "Fit range ",self._metFitRangeMin, " - ",rangeMax

	class FitFunction:
	    def __call__( self, x, par ):
                return QCDFunction(x,par,1)
            
        theFit = TF1('theFit',FitFunction(),self._metFitRangeMin,rangeMax,numberOfParameters)
        """
        theFit.SetParLimits(0,1,20)
        theFit.SetParLimits(1,20,40)
        theFit.SetParLimits(2,10,25)

        theFit.SetParLimits(3,1,10)
        theFit.SetParLimits(4,0,150)
        theFit.SetParLimits(5,10,100)

        theFit.SetParLimits(6,0.0001,1)
        theFit.SetParLimits(7,0.001,0.05)
        """

        theFit.SetParLimits(0,0.0001,200)
        theFit.SetParLimits(1,0.001,10)

        theFit.SetParLimits(2,1,10)
        theFit.SetParLimits(3,0,150)
        theFit.SetParLimits(4,10,100)

        theFit.SetParLimits(5,0.0001,1)
        theFit.SetParLimits(6,0.001,0.05)

	if self.label == "Baseline":
	    rangeMax = 240

	if histo.GetTitle() == "#tau p_{T}=70..80": # FIXME: now use something like '#tau p_{T}=150..200'
	    theFit.SetParLimits(5,10,100)

#	if self.label == "#tau p_{T}=100..120":
#	    theFit.SetParLimits(0,1,20)
#	    theFit.SetParLimits(2,1,25)
#	    theFit.SetParLimits(3,0.1,20)

	if histo.GetTitle() == "#tau p_{T}=120..150":
            theFit.SetParLimits(0,1,20)
            theFit.SetParLimits(3,0.1,5)


	gStyle.SetOptFit(0)

	plot = plots.PlotBase()
	plot.histoMgr.appendHisto(histograms.Histo(histo,histo.GetName()))
	plot.createFrame("qcdfit"+self.label, opts={"ymin": 1e-5, "ymaxfactor": 2.})

        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        histograms.addLuminosityText(x=None, y=None, lumi=self.lumi)

	self.normInvQCD = histo.Integral(0,histo.GetNbinsX())

	histo.Scale(1/self.normInvQCD)
        histo.Fit(theFit,"LR")         
                                      
        theFit.SetRange(histo.GetXaxis().GetXmin(),histo.GetXaxis().GetXmax())
        theFit.SetLineStyle(2)                                                
        theFit.Draw("same")


        histograms.addText(0.4,0.8,"Inverted TauID")

	plot.histoMgr.appendHisto(histograms.Histo(theFit,"Fit"))

        plot.getPad().SetLogy(True) 
        
        plot.draw()
        plot.save()

        self.parInvQCD = theFit.GetParameters()                               
                                                                              
        fitPars = "fit parameters "                                           
        i = 0                                                                 
        while i < numberOfParameters:
            fitPars = fitPars + " " + str(self.parInvQCD[i])
            i = i + 1
        print "QCD fit parameters",fitPars
	self.nFitInvQCD = theFit.Integral(0,1000,self.parInvQCD)
        print "Integral ",self.normInvQCD*self.nFitInvQCD


    def fitEWK(self,histo,options="R"):
        numberOfParameters = 4
        rangeMax = self._getMaxRangeForFit(self._metFitRangeMaxForEWKFit, histo)
        print "Fit range in 'fitEWK()'",self._metFitRangeMin, " - ",rangeMax

        class FitFunction:
            def __call__( self, x, par ):
                return EWKFunction(x,par,1,1)
#		return SumFunction(x,par)
#	        return TestFunction(x,par,1)
	class PlotFunction:
	    def __call__( self, x, par ):
		return EWKFunction(x,par,0)


        theFit = TF1('theFit',FitFunction(),self._metFitRangeMin,rangeMax,numberOfParameters)
	thePlot = TF1('thePlot',PlotFunction(),self._metFitRangeMin,rangeMax,numberOfParameters)

        theFit.SetParLimits(0,5,30)
        theFit.SetParLimits(1,90,200)
        theFit.SetParLimits(2,30,100) 
        theFit.SetParLimits(3,0.001,1)
        if "#tau p_{T}=41..50" in histo.GetTitle():
            theFit.SetParLimits(0,5,20) 
            theFit.SetParLimits(1,90,120)
            theFit.SetParLimits(2,30,50)
            theFit.SetParLimits(3,0.001,1)
	elif "#tau p_{T}=50..60" in histo.GetTitle():
            theFit.SetParLimits(0,5,20)     
            theFit.SetParLimits(1,90,120)   
            theFit.SetParLimits(2,20,50)
            theFit.SetParLimits(3,0.001,1)
        elif "#tau p_{T}=60..70" in histo.GetTitle():
            theFit.SetParLimits(0,5,50)
            theFit.SetParLimits(1,90,150)
            theFit.SetParLimits(2,20,50)
            theFit.SetParLimits(3,0.001,1)
        elif "#tau p_{T}=70..80" in histo.GetTitle():
            theFit.SetParLimits(0,5,60)
            theFit.SetParLimits(1,90,200)
            theFit.SetParLimits(2,20,100)
            theFit.SetParLimits(3,0.001,1)
        elif "#tau p_{T}=80..100" in histo.GetTitle():
            theFit.SetParLimits(0,5,50)
            theFit.SetParLimits(1,50,170)
            theFit.SetParLimits(2,20,60)
            theFit.SetParLimits(3,0.001,1)
        elif "#tau p_{T}=100..120" in histo.GetTitle():
            theFit.SetParLimits(0,5,50)
            theFit.SetParLimits(1,90,170)
            theFit.SetParLimits(2,20,60) 
            theFit.SetParLimits(3,0.001,1)
        elif "#tau p_{T}=120..150" in histo.GetTitle():
            theFit.SetParLimits(0,5,50)
            theFit.SetParLimits(1,60,170)
            theFit.SetParLimits(2,10,100)
            theFit.SetParLimits(3,0.001,1)
        else:
            #if histo.GetTitle() == "150":
            print WarningLabel()+"Using fallback fit settings in InvertedTauID::fitEWK() for label %s"%self.label
            theFit.SetParLimits(0,5,50)
            theFit.SetParLimits(1,70,170)
            theFit.SetParLimits(2,20,100)
            theFit.SetParLimits(3,0.001,1)


        plot = plots.PlotBase()
        plot.histoMgr.appendHisto(histograms.Histo(histo,histo.GetName()))
        plot.createFrame("ewkfit"+self.label, opts={"ymin": 1e-5, "ymaxfactor": 2.})

        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        histograms.addLuminosityText(x=None, y=None, lumi=self.lumi)
                        
	self.normEWK = histo.Integral(0,histo.GetNbinsX())

	histo.Scale(1/self.normEWK)

	myFitResultPtr = histo.Fit(theFit,options+"S")
	self._checkGoodnessOfFit(myFitResultPtr, "fitEWK()", histo.GetTitle())
       
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

        histograms.addText(0.2,0.2,"EWK MC, baseline TauID")

        plot.histoMgr.appendHisto(histograms.Histo(theFit,"Fit"))

        plot.getPad().SetLogy(True)

        plot.draw()
        plot.save()
                           
        self.parMCEWK = theFit.GetParameters()
        
        print "EWK MC fit parameters",fitPars
        self.nMCEWK = theFit.Integral(0,1000,self.parMCEWK)
        print "Integral ",self.normEWK*self.nMCEWK

    def fitData(self,histo):
        self.nBaseQCD = histo.Integral(0,histo.GetNbinsX())

	parInvQCD  = self.parInvQCD
	parMCEWK   = self.parMCEWK
	nInvQCD    = self.nInvQCD
        nFitInvQCD = self.nFitInvQCD
        nMCEWK     = self.nMCEWK

        print nInvQCD,nFitInvQCD,nMCEWK
        class FitFunction:
            def __call__( self, x, par ):
                return par[0]*(par[1] * QCDFunction(x,parInvQCD,1/nFitInvQCD) + ( 1 - par[1] ) * EWKFunction(x,parMCEWK,1/nMCEWK))

	class QCDOnly:
	    def __call__( self, x, par ):
                return par[0]*par[1] * QCDFunction(x,parInvQCD,1/nFitInvQCD)

        numberOfParameters = 2
        
        rangeMax = self._getMaxRangeForFit(self._metFitRangeMaxForDataFit, histo)
        print "Fit range in 'fitData()'",self._metFitRangeMin, " - ",rangeMax
        
        theFit = TF1("theFit",FitFunction(),self._metFitRangeMin,rangeMax,numberOfParameters)
        
        plot = plots.PlotBase()
        plot.histoMgr.appendHisto(histograms.Histo(histo,histo.GetName()))
        plot.createFrame("combinedfit"+self.label, opts={"ymin": 1e-5, "ymaxfactor": 2.})

        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        histograms.addLuminosityText(x=None, y=None, lumi=self.lumi)
                                        
	print "data events ",histo.Integral(0,histo.GetNbinsX())

        myFitResultPtr = histo.Fit(theFit,"SR")
        self._checkGoodnessOfFit(myFitResultPtr, "fitData()", histo.GetTitle())

        theFit.SetRange(histo.GetXaxis().GetXmin(),histo.GetXaxis().GetXmax())
        theFit.SetLineStyle(2)
        theFit.SetLineColor(4)
        theFit.Draw("same")

	par = theFit.GetParameters()

	qcdOnly = TF1("qcdOnly",QCDOnly(),self._metFitRangeMin,rangeMax,numberOfParameters)
	qcdOnly.FixParameter(0,par[0])
	qcdOnly.FixParameter(1,par[1])
	qcdOnly.SetLineStyle(2)
	qcdOnly.Draw("same")

        histograms.addText(0.35,0.8,"Data, Baseline selection")
        histograms.addText(0.25,0.3,"QCD shape",20)
        histograms.addText(0.25,0.25,"from Inverted selection",20)
        histo.GetYaxis().SetTitle("Events / 10 GeV")
        histo.GetXaxis().SetTitle("MET  (GeV)")
        histograms.addText(0.35,0.8,"Data, Baseline TauID")
        histograms.addText(0.4,0.25,"QCD",15)


        plot.histoMgr.appendHisto(histograms.Histo(qcdOnly,"qcdOnly"))
        
        plot.getPad().SetLogy(True)

        plot.draw()
        plot.save()
                                        
        fitPars = "fit parameters "
        i = 0
        while i < numberOfParameters:
            fitPars = fitPars + " " + str(par[i])
            i = i + 1
        print "QCD+EWK fit parameters",fitPars
	nBaseQCD = par[0]
	self.QCDfraction = par[1]
        self.QCDfractionError = theFit.GetParError(1) 
	if len(self.label) > 0:
	    print "Bin ",self.label
        print "Integral     ", nBaseQCD
	print "QCD fraction ",self.QCDfraction
	print "QCD fraction error ",theFit.GetParError(1)
        
        return theFit

    def fitBaselineData(self,histoInv,histoBase):

	parInvQCD = self.parInvQCD
        parMCEWK  = self.parMCEWK
        nMCEWK    = self.nMCEWK
	normEWK   = self.normEWK
        print "check",self.nMCEWK,self.normEWK
	i = 0
        while i < 4: 
            print "param",i,parMCEWK[i]
            i = i + 1

        class FitFunction: 
            def __call__( self, x, par ):
#		print "check FitFunction",QCDFunction(x,par,1),normEWK * nMCEWK * EWKFunction(x,parMCEWK,1)
#		par[3] = par[0] * parInvQCD[3] / parInvQCD[0] 
		if x[0] > 200 and x[0] < 220:
        	    TF1.RejectPoint()
                    return 0
		return QCDFunctionFixed(x,par) + normEWK * EWKFunction(x,parMCEWK,1)

        class QCDOnly:
            def __call__( self, x, par ):
		return QCDFunctionFixed(x,par)
#		return QCDFunction(x,par,1)

        class QCDOnly2:
            def __call__( self, x, par ):
                return QCDFunction(x,par,1)

        class EWKOnly:
            def __call__( self, x, par ):
                return normEWK * EWKFunction(x,par,1)

	norm = histoBase.GetMaximum()/histoInv.GetMaximum()
	class InvertedFit:
	    def __call__( self, x, par ):
		return QCDFunction(x,par,norm)
        
        numberOfParameters = 8
        
        rangeMax = self._getMaxRangeForFit(self._metFitRangeMaxForBaselineDataFit, histoInv)
        print "Fit range in 'fitBaselineData()'",self._metFitRangeMin, " - ",rangeMax
                
        theFit = TF1('theFit',FitFunction(),self._metFitRangeMin,rangeMax,numberOfParameters)

        theFit.SetParLimits(0,10,20000)
        theFit.SetParLimits(1,20,40)
        theFit.SetParLimits(2,1,25)
        
        theFit.SetParLimits(3,1,10000)  
        theFit.SetParLimits(4,50,150)
        theFit.SetParLimits(5,1,100)

	theFit.FixParameter(1,parInvQCD[1])
        theFit.FixParameter(2,parInvQCD[2])
	theFit.FixParameter(3,parInvQCD[3]/parInvQCD[0])
        theFit.FixParameter(4,parInvQCD[4])
        theFit.FixParameter(5,parInvQCD[5])

        
        theFit.SetParLimits(6,0.001,100)
        theFit.SetParLimits(7,0.001,0.05)        
        print "Fit range ",self._metFitRangeMin, " - ",rangeMax
    
        
        cshape = TCanvas("cshape","",500,500)
        cshape.cd()
        cshape.SetLogy()
#        print "data events ",histo.Integral(0,histo.GetNbinsX())   

        histoInv.Scale(histoBase.GetMaximum()/histoInv.GetMaximum())
        histoInv.SetMarkerColor(4)
        histoInv.Draw("hist ep");

#	histoBase.GetYaxis().SetLimits(0.001,300.)
#	histoBase.SetBinContent(11,0)
	histoBase.Draw("histo epsame")
        myFitResultPtr = histoBase.Fit(theFit,"RNS")
        self._checkGoodnessOfFit(myFitResultPtr, "fitBaselineData()", histo.GetTitle())
	theFit.Draw("same")

#        theFit.SetRange(histoInv.GetXaxis().GetXmin(),histoInv.GetXaxis().GetXmax())
#        theFit.SetLineStyle(2)
#        theFit.DrawClone("same")

        par = theFit.GetParameters()

	ewkOnly = TF1("ewkOnly",EWKOnly(),self._metFitRangeMin,rangeMax,4)
	ewkOnly.SetLineStyle(2)
	ewkOnly.SetLineColor(3)
	ewkOnly.Draw("same")
	i = 0
	while i < 4:
	    ewkOnly.FixParameter(i,parMCEWK[i])
            i = i + 1



        theFit2 = TF1('theFit2',QCDOnly(),self._metFitRangeMin,rangeMax,numberOfParameters)
            
        theFit2.SetParLimits(0,10,20000)
        theFit2.SetParLimits(1,20,40)
        theFit2.SetParLimits(2,10,25)
        
        theFit2.SetParLimits(3,1,10000)
        theFit2.SetParLimits(4,0,150)
        theFit2.SetParLimits(5,20,100)
        
        theFit2.SetParLimits(6,0.0001,100)
        theFit2.SetParLimits(7,0.001,0.05)

        theFit2.FixParameter(1,parInvQCD[1])
        theFit2.FixParameter(2,parInvQCD[2])
        theFit2.FixParameter(3,parInvQCD[3]/parInvQCD[0])
        theFit2.FixParameter(4,parInvQCD[4])
        theFit2.FixParameter(5,parInvQCD[5])

	QCDbase = histoBase.Clone("QCDbase")
	i = 1
	while i < QCDbase.GetNbinsX():
	    newBinValue = QCDbase.GetBinContent(i) - ewkOnly.Eval(QCDbase.GetBinCenter(i))
	    print "check newBinValue",QCDbase.GetBinContent(i),ewkOnly.Eval(QCDbase.GetBinCenter(i)),QCDbase.GetBinCenter(i)
	    QCDbase.SetBinContent(i,newBinValue)
	    i = i + 1
	QCDbase.SetMarkerColor(5)
	QCDbase.Draw("same")
	myFitResultPtr = QCDbase.Fit(theFit2,"LRNS")
	self._checkGoodnessOfFit(myFitResultPtr, "fitQCD()", histo.GetTitle())
	theFit2.Draw("same")
        
        qcdOnly = TF1("qcdOnly",QCDOnly(),self._metFitRangeMin,rangeMax,numberOfParameters)
	i = 0
	while i < numberOfParameters:
            qcdOnly.FixParameter(i,par[i])
	    i = i + 1
        qcdOnly.SetLineStyle(2)
        qcdOnly.Draw("same")


#        histoInv.Scale(histoBase.GetMaximum()/histoInv.GetMaximum())
#        histoInv.SetMarkerColor(4)
#        histoInv.Draw("hist epsame");

	inverted = TF1("inverted",InvertedFit(),self._metFitRangeMin,rangeMax,numberOfParameters)
        i = 0
        while i < numberOfParameters:   
            inverted.FixParameter(i,parInvQCD[i])
            i = i + 1
        inverted.SetLineStyle(3)
	inverted.SetLineColor(4)
        inverted.Draw("same")	

        cshape.Print("shapefit"+self.label+".eps")

    def getNormalization(self):
	nQCDbaseline = self.nBaseQCD
	nQCDinverted = self.nInvQCD

	QCDfractionInBaseLineEvents = self.QCDfraction
        QCDfractionInBaseLineEventsError = self.QCDfractionError
	self.normalizationForInvertedEvents = nQCDbaseline*QCDfractionInBaseLineEvents/nQCDinverted
        self.normalizationForInvertedEWKEvents = nQCDbaseline*(1-QCDfractionInBaseLineEvents)/nQCDinverted
        ratio = float(nQCDbaseline)/nQCDinverted
	normalizationForInvertedEventsError = sqrt(ratio*(1-ratio/nQCDinverted))*QCDfractionInBaseLineEvents +QCDfractionInBaseLineEventsError*ratio # FIXME: is it correct to use a linear sum instead of a squared sum here?
	self.normFactors.append(self.normalizationForInvertedEvents)
        self.normFactorsEWK.append(self.normalizationForInvertedEWKEvents)
	self.labels.append(self.label)

	print "\n"
	print "Normalizing to baseline TauID qcd fraction from a fit using inverted QCD MET distribution shape and EWK MC baseline shape"
	print "    Number of baseline QCD events       ",nQCDbaseline
	print "    QCD fraction in baseline QCD events ",QCDfractionInBaseLineEvents
        print "    Number of inverted QCD events       ",nQCDinverted 
	print "\n"
	print "Normalization for inverted QCD events   ",self.normalizationForInvertedEvents
        print "Normalization for inverted EWK events   ",self.normalizationForInvertedEWKEvents
 	print "Normalization for inverted QCD events error   ",normalizationForInvertedEventsError                                                  
	print "\n"
	return self.normalizationForInvertedEvents

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
            
        print "EWK normalization factors for each bin"
        i = 0
	while i < len(self.normFactorsEWK):
	    label = self.labels[i]
	    while len(label) < 10:
		label = label  + " "
	    print "    Label",label,", normalization EWK",self.normFactorsEWK[i]
	    i = i + 1
        print "\nNow run plotSignalAnalysisInverted.py with these normalization factors.\n"


    def WriteNormalizationToFile(self,filename,era,searchMode,optimizationMode):
	fOUT = open(filename,"w")

	now = datetime.datetime.now()

	fOUT.write("# Generated on %s\n"%now.ctime())
	fOUT.write("# by %s\n"%os.path.basename(sys.argv[0]))
        fOUT.write("\n")
	fOUT.write("QCDInvertedNormalization = {\n")
	fOUT.write('    "era": "%s",\n'%era)
	fOUT.write('    "searchMode": "%s",\n'%searchMode)
	fOUT.write('    "optimizationMode": "%s",\n'%optimizationMode)
        i = 0
        while i < len(self.normFactors):
	    line = "    \"" + self.labels[i] + "\": " + str(self.normFactors[i])
	    #if i < len(self.normFactors) - 1:
            line += ","
	    line += "\n"
            fOUT.write(line)
            i = i + 1
        i = 0
        while i < len(self.normFactorsEWK):
	    line = "    \"" + self.labels[i] + "EWK\": " + str(self.normFactorsEWK[i])
	    #if i < len(self.normFactorsEWK) - 1:
            line += ","
	    line += "\n"
            fOUT.write(line)
            i = i + 1
#        fOUT.write("    \"QCDInvertedNormalizationEWK\":"+str(self.normalizationForInvertedEWKEvents)+"\n")
#        fOUT.write("    \"QCDInvertedNormalization\":"+str(self.normalizationForInvertedEvents)+"\n")
	fOUT.write("}\n")
	fOUT.close()
	print "Normalization factors written in file",filename
