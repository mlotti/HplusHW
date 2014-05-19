import ROOT
ROOT.gROOT.SetBatch(True) # no flashing canvases

import os
import sys
import math
import array
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.aux as aux
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle

fitOptions = "RM"
#fitOptions = "LRB"

# Fitting functions
class FitFuncBase:
    def __init__(self, npar):
        self._npar = npar

    def getNparam(self):
        return self._npar

class FitFuncGausExpTail(FitFuncBase):
    def __init__(self):
        FitFuncBase.__init__(self, 4)

    def __call__(self, x, par):
        return par[0]*ROOT.TMath.Exp(-x[0] * par[1])*ROOT.TMath.Exp(-(x[0]-par[2])**2 / par[3])

    def setParamLimits(self, fit):
        fit.SetParLimits(0,1,10000)
        fit.SetParLimits(1,1e-10,0.1)
        fit.SetParLimits(2,20,160)
        fit.SetParLimits(3,10,100000)
        fit.SetParameter(0, 10.0)
        fit.SetParameter(1, 0.002)
        fit.SetParameter(2, 90.0)
        fit.SetParameter(3, 100.0)

class FitFuncExpTail(FitFuncBase):
    def __init__(self):
        FitFuncBase.__init__(self, 3)

    def __call__(self, x, par):
        return par[0]*ROOT.TMath.Exp(-x[0] * par[1] - (x[0]**2*par[2]))

    def setParamLimits(self, fit):
        fit.SetParLimits(0,1,100000)
        fit.SetParLimits(1,1e-10,0.1)
        fit.SetParLimits(2,1e-10,0.001)
        fit.SetParameter(0,10.0)
        fit.SetParameter(1,0.002)
        fit.SetParameter(2,0.00001)

class FitFuncExpTailAlternate(FitFuncBase):
    def __init__(self):
        FitFuncBase.__init__(self, 3)

    def __call__(self, x, par):
        return par[0]*ROOT.TMath.Exp(-x[0] * par[1] + x[0] / par[2])

    def setParamLimits(self, fit):
        fit.SetParLimits(0,0.0001,100000)
        fit.SetParLimits(1,0.0001,100000)
        fit.SetParLimits(2,0.0001,100000)
        fit.SetParameter(0, 1.0)
        fit.SetParameter(1, 1.0)
        fit.SetParameter(2, 1.0)

def doPlusVariation(self, func):
    for i in range(1,self._npar):
        func.SetParameter(i, func.GetParameter(i) + func.GetParError(i))

def doMinusVariation(self, func):
    for i in range(1,self._npar):
        func.SetParameter(i, func.GetParameter(i) - func.GetParError(i))

class TailFitter:
    def __init__(self, h, label, name, fitmin, fitmax):
        print "Fitting tail for shape: %s, range = %d-%d"%(label, fitmin, fitmax)
        
        myStyle = tdrstyle.TDRStyle()
        myStyle.setOptStat(True)
        myStyle.tdrStyle.SetOptFit(True)
        ROOT.TVirtualFitter.SetDefaultFitter("Minuit2")

        myFitFunc = None
        if label.startswith("HH") or label.startswith("HW"):
            # signal
            #myFitFunc = FitFuncGausExpTail()
            myFitFunc = FitFuncExpTail()
        elif label.startswith("QCD"):
            # QCD
            #myFitFunc = FitFuncExpTail()
            myFitFunc = FitFuncGausExpTail()
            fitmin = 40
            fitmax = 200
        else:
            fitmin = 100
            fitmax = 200
            myFitFunc = FitFuncExpTail()

        myM = ROOT.RooRealVar("m","m",h.GetXaxis().GetXmin(),h.GetXaxis().GetXmax())
        myA = ROOT.RooRealVar("a","a",50,0.1,200)
        myB = ROOT.RooRealVar("b","b",50,-10500,10500) # //lB.setConstant(kTRUE);
        myRooHisto = ROOT.RooDataHist("Data","Data",ROOT.RooArgList(myM),h)

        _fitModel = 0
        myFitFunction = None
        if _fitModel == 0:
            myFitFunction = "exp(-(m-%d)/(a+0.001*b(m-%d)))"%(fitmin,fitmin)

        print "Using fit function:", myFitFunction

        myFit = ROOT.RooGenericPdf("genPdf",myFitFunction,ROOT.RooArgList(myM,myA,myB));
        #if(iFitModel == 1) lFit = new RooGenericPdf("genPdf","exp(-a*pow(m,b))",RooArgList(lM,lA,lB));
        #if(iFitModel == 1) {lA.setVal(0.3); lB.setVal(0.5);}
        #if(iFitModel == 2) lFit = new RooGenericPdf("genPdf","a*exp(b*m)",RooArgList(lM,lA,lB));
        #if(iFitModel == 3) lFit = new RooGenericPdf("genPdf","a/pow(m,b)",RooArgList(lM,lA,lB));
        #if(iFitModel == 4) lFit = new RooGenericPdf("genPdf","a*pow(m,b)",RooArgList(lM,lA,lB));
        #if(iFitModel == 5) lFit = new RooGenericPdf("genPdf","a*exp(pow(m,b))",RooArgList(lM,lA,lB));
        myFitResult = myFit.fitTo(myRooHisto,ROOT.RooFit.Save(True),ROOT.RooFit.Range(fitmin,fitmax))
        #RooFitResult *lRFit = 0;
        #double lFirst = iFirst;
        #double lLast = iLast;
        #//lRFit = lFit->chi2FitTo(*pH0,Save(kTRUE),Range(lFirst,lLast));
        #lRFit = lFit->fitTo(*pH0,Save(kTRUE),Range(lFirst,lLast),Strategy(0));
        
        #//std::cout << lRFit->status() << " " << lRFit->covQual() << std::endl;
        if (not(myFitResult.status() == 0 and myFitResult.covQual() == 3)):
            raise Exception("Fit failed")

        print "Fit success"
        raise Exception()
            
            
            
        #plot = plots.PlotBase()
        #plot.histoMgr.appendHisto(histograms.Histo(h,"%s_%s"%(label,name)))
        #plot.createFrame("tailfit_%s_%s"%(label,name), opts={"ymin": 1e-5, "ymaxfactor": 2.})

        #myFit = ROOT.TF1("myFit", myFitFunc, fitmin, fitmax, myFitFunc.getNparam())
        #myExtrapolation = ROOT.TF1("myExtrapolation", myFitFunc, fitmax, h.GetXaxis().GetXmax(), myFitFunc.getNparam())
        #myExtrapolationPlus = ROOT.TF1("myExtrapolationPlus", myFitFunc, fitmax, h.GetXaxis().GetXmax(), myFitFunc.getNparam())
        #myExtrapolationMinus = ROOT.TF1("myExtrapolationMinus", myFitFunc, fitmax, h.GetXaxis().GetXmax(), myFitFunc.getNparam())
        #myFitFunc.setParamLimits(myFit)
        #h.Fit(myFit, fitOptions)
        ##theFit.SetRange(histo.GetXaxis().GetXmin(),histo.GetXaxis().GetXmax())
        #myFit.SetLineStyle(1)
        #myFit.SetLineColor(ROOT.kBlue)
        #myFit.SetLineWidth(3)
        #myExtrapolation.SetLineStyle(1)
        #myExtrapolation.SetLineColor(ROOT.kRed)
        #myExtrapolation.SetLineWidth(3)
        #myExtrapolationPlus.SetLineWidth(2)
        #myExtrapolationMinus.SetLineWidth(2)
        #myExtrapolationPlus.SetLineColor(ROOT.kGray+1)
        #myExtrapolationMinus.SetLineColor(ROOT.kGray+1)
        #for i in range(0, myFitFunc.getNparam()):
            #myExtrapolation.SetParameter(i, myFit.GetParameters()[i])
            #if i != 1:
                #myExtrapolationPlus.SetParameter(i, myFit.GetParameters()[i])
                #myExtrapolationMinus.SetParameter(i, myFit.GetParameters()[i])
            #else:
                #myExtrapolationPlus.SetParameter(i, myFit.GetParameter(i) + myFit.GetParError(i))
                #myExtrapolationMinus.SetParameter(i, myFit.GetParameter(i) - myFit.GetParError(i))
        #myExtrapolation.Draw("same")
        #myExtrapolationPlus.Draw("same")
        #myExtrapolationMinus.Draw("same")
        #myFit.Draw("same")
        ##histograms.addText(0.35,0.8,"Data, Baseline TauID")
        ##histograms.addText(0.45,0.25,"QCD",20)

        #plot.getPad().SetLogy( True)

        #histograms.addCmsPreliminaryText()
        #histograms.addEnergyText()
        ##histograms.addLuminosityText(x=None, y=None, lumi=self.lumi)

        #plot.draw()
        #plot.save()

        ## Obtain fit parameters
        #par = myFit.GetParameters()

        #myDebugStatus = not True
        #if myDebugStatus:
            #print "shape histogram info dump for %s"%label
            #print "h = ROOT.TH1F('h','h',%d,%f,%f)"%(h.GetNbinsX(),h.GetXaxis().GetXmin(),h.GetXaxis().GetXmax())
            #for i in range(1,h.GetNbinsX()+1):
                #print "h.SetBinContent(%d, %f)"%(i, h.GetBinContent(i))
            #for i in range(1,h.GetNbinsX()+1):
                #print "h.SetBinError(%d, %f)"%(i, h.GetBinError(i))
                
        ## Find bins for integral
        #a = 0
        #b = 0
        #for i in range(1,h.GetNbinsX()+1):
            #if h.GetXaxis().GetBinLowEdge(i) < fitmin:
                #a = i
            #if h.GetXaxis().GetBinUpEdge(i) < fitmax:
                #b = i
        #print "Histogram integral: %f"%(h.Integral(a,b))
        #print "Fit integral: %f"%(myFit.Integral(fitmin,fitmax))

