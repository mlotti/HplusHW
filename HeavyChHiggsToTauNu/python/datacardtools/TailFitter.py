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

fitOptions = "RMS"
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

class FitFuncExpTailExo(FitFuncBase):
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

class FitFuncExpTailExoAlternate(FitFuncBase):
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

class FitFuncExpTailTauTau(FitFuncBase):
    def __init__(self):
        FitFuncBase.__init__(self, 3)

    def __call__(self, x, par):
        return par[0]*ROOT.TMath.Exp(-x[0] / (par[1] + x[0]*par[2]))

    def setParamLimits(self, fit):
        fit.SetParLimits(0,1,100000)
        fit.SetParLimits(1,0.1,200)
        fit.SetParLimits(2,-20.0,20.0)
        fit.SetParameter(0,10.0)
        fit.SetParameter(1,1)
        fit.SetParameter(2,0.00001)

class FitFuncExpTailTauTauTest(FitFuncBase):
    def __init__(self):
        FitFuncBase.__init__(self, 4)

    def __call__(self, x, par):
        return par[3]*ROOT.TMath.Exp(-(x[0]-par[2]) / (par[0] + (x[0]-par[2])*par[1]))

    def setParamLimits(self, fit):
        fit.SetParLimits(0,0.1,2000)
        fit.SetParLimits(1,0.000001,2.0)
        fit.SetParLimits(2,0,200)
        fit.SetParLimits(3,0.01,4000)
        fit.SetParameter(0,10.0)
        fit.SetParameter(1,0.003)
        fit.SetParameter(2,100.0)
        fit.SetParameter(3,1.0)


def doPlusVariation(self, func):
    for i in range(1,self._npar):
        func.SetParameter(i, func.GetParameter(i) + func.GetParError(i))

def doMinusVariation(self, func):
    for i in range(1,self._npar):
        func.SetParameter(i, func.GetParameter(i) - func.GetParError(i))

class TailFitter:
    def __init__(self, h, label, name, fitmin, fitmax):
        def printEigenVectors(matrix):
            s = "Eigenvectors: "
            for i in range(0, matrix.GetNcols()):
                if i > 0:
                    s += " and "
                s += "("
                for j in range(0, matrix.GetNrows()):
                    if j > 0:
                        s += ","
                    s += "%f"%matrix(j,i)
                s += ")"
            print s

        def printEigenValues(vector):
            s = "Eigenvalues: "
            for j in range(0, vector.GetNrows()):
                if i > 0:
                    s += " and "
                s += "%f"%vector(j)
            print s

        myStyle = tdrstyle.TDRStyle()
        myStyle.setOptStat(True)
        myStyle.tdrStyle.SetOptFit(True)
        ROOT.TVirtualFitter.SetDefaultFitter("Minuit2")

        myFitFunc = None
        if label.startswith("QCD"):
            # QCD
            #myFitFunc = FitFuncExpTail()
            myFitFunc = FitFuncExpTailTauTauTest()
            fitmin = 110
            fitmax = 200
        else:
            fitmin = 100
            fitmax = 200
            myFitFunc = FitFuncExpTailTauTauTest()

        # Do fit
        print "Fitting tail for shape: %s, range = %d-%d"%(label, fitmin, fitmax)
        myFit = ROOT.TF1("myFit", myFitFunc, fitmin, fitmax, myFitFunc.getNparam())
        myFitFunc.setParamLimits(myFit)
        myFitResult = h.Fit(myFit, fitOptions)

        # Check if fit is successful
        self._myChi2 = myFitResult.Prob()
        self._myNdof = h.FindBin(fitmax) - h.FindBin(fitmin)
        print myFitResult.Status(), myFitResult.CovMatrixStatus()
        if not (myFitResult.Status() == 0 and myFitResult.CovMatrixStatus() == 3):
            print "Fit failed"
        else:
            print "Fit success"
        print "chi2/ndof=%f (ndof=%d)"%(self._myChi2/float(self._myNdof),self._myNdof)

        # Nominal histograms
        myCentralParams = []
        for i in range(0, myFitFunc.getNparam()):
            myCentralParams.append(myFitResult.Parameter(i))
        hFit = self._functionToHistogram("fit", myFit, myCentralParams, h.GetNbinsX(),h.GetXaxis().GetXmin(),h.GetXaxis().GetXmax(),fitmin)

        # Get eigenvectors
        myCovMatrix = myFitResult.GetCovarianceMatrix()
        myDiagonalizedMatrix = ROOT.TMatrixDSymEigen(myCovMatrix)
        self._myEigenVectors = ROOT.TMatrixD(myFitFunc.getNparam(),myFitFunc.getNparam())
        self._myEigenVectors = myDiagonalizedMatrix.GetEigenVectors()
        printEigenVectors(self._myEigenVectors)
        # Get eigenvalues
        self._myEigenValues = ROOT.TVectorD(myFitFunc.getNparam())
        self._myEigenValues = myDiagonalizedMatrix.GetEigenValues()
        for i in range(0, self._myEigenValues.GetNrows()):
            self._myEigenValues[i] = math.sqrt(self._myEigenValues(i))
        printEigenValues(self._myEigenValues)

        # Construct from eigenvalues and vectors the orthogonal variations
        # Up histograms
        myUpHistograms = []
        for i in range(0, self._myEigenValues.GetNrows()):
            myParams = list(myCentralParams)
            for j in range(0,len(myParams)):
                myParams[j] = myCentralParams[j] + self._myEigenValues(i)*self._myEigenVectors(j,i)
                if myParams[j] < 0:
                    myParams[j] = 1e-10
            #myShiftUp = (-1.0 * myA.getVal() / myB.getVal())
            #myFirstBin = fitmin
            #if myFirstBin < myShiftUp and myShiftUp < h.GetXaxis().GetXmax():
                #myM.setRange(0, h.GetBinLowEdge(h.FindBin(myShiftUp)))
            hUp = self._functionToHistogram("fitUp%d"%i, myFit, myParams, h.GetNbinsX(),h.GetXaxis().GetXmin(),h.GetXaxis().GetXmax(),fitmin)
            myUpHistograms.append(hUp)

        # Down histograms
        myDownHistograms = []
        for i in range(0, self._myEigenValues.GetNrows()):
            myParams = list(myCentralParams)
            for j in range(0,len(myParams)):
                myParams[j] = myCentralParams[j] - self._myEigenValues(i)*self._myEigenVectors(j,i)
                if myParams[j] < 0:
                    myParams[j] = 1e-10
            #myShiftDown = (-1.0 * myA.getVal() / myB.getVal())
            #myFirstBin = fitmin
            #if myFirstBin < myShiftDown and myShiftDown < h.GetXaxis().GetXmax():
                #myM.setRange(0, h.GetBinLowEdge(h.FindBin(myShiftDown)))
            hDown = self._functionToHistogram("fitDown%d"%i, myFit, myParams, h.GetNbinsX(),h.GetXaxis().GetXmin(),h.GetXaxis().GetXmax(),fitmin)
            myDownHistograms.append(hDown)

        # Calculate total uncertainty
        self._hFitUncertaintyUp = aux.Clone(h, label+"_TailFitUp")
        self._hFitUncertaintyUp.Reset()
        self._hFitUncertaintyDown = aux.Clone(h, label+"_TailFitDown")
        self._hFitUncertaintyDown.Reset()
        for i in range(1, h.GetNbinsX()+1):
            myPedestal = hFit.GetBinContent(i)
            myVariance = 0.0
            for hUp in myUpHistograms:
                if hUp.GetBinContent(i) > 2e-10:
                    myVariance += (hUp.GetBinContent(i) - myPedestal)**2
                    #print i, (hUp.GetBinContent(i) - myPedestal)**2
            self._hFitUncertaintyUp.SetBinContent(i, myPedestal + math.sqrt(myVariance))
            myVariance = 0.0
            for hDown in myUpHistograms:
                if hDown.GetBinContent(i) > 2e-10:
                    myVariance += (myPedestal - hDown.GetBinContent(i))**2
            self._hFitUncertaintyDown.SetBinContent(i, myPedestal - math.sqrt(myVariance))

        # Make plots
        self._makeVariationPlotSimple(label, name, h, hFit, self._hFitUncertaintyUp, self._hFitUncertaintyDown)
        self._makeVariationPlotDetailed(label, name, h, hFit, myUpHistograms, myDownHistograms)

        #myParameters = myFitResult.Parameter(i)
        #myExtrapolation = ROOT.TF1("myExtrapolation", myFitFunc, fitmax, h.GetXaxis().GetXmax(), myFitFunc.getNparam())

        #raise Exception()



    def __del__(self):
        print "test"
        #self._myEigenVectors.Delete()
        #self._myEigenValues.Delete()

    def _functionToHistogram(self, name, function, parameters, nbins, xmin, xmax, cutoff):
        h = ROOT.TH1F(name, name, nbins, xmin, xmax)
        #print "Params for %s: %s"%(name,", ".join("%f" % x for x in parameters))
        for i in range(0,len(parameters)):
            function.SetParameter(i, parameters[i])
            #print function.GetParameter(i)
        for i in range(1,h.GetNbinsX()+1):
            if h.GetXaxis().GetBinLowEdge(i) >= cutoff:
                myIntegral = function.Integral(h.GetXaxis().GetBinLowEdge(i), h.GetXaxis().GetBinUpEdge(i))
                w = h.GetXaxis().GetBinUpEdge(i) - h.GetXaxis().GetBinLowEdge(i)
                #print "integral: %d, %d: %f"%(w, i, myIntegral/w)
                h.SetBinContent(i, myIntegral / w)
        return h

    def _makeVariationPlotSimple(self, label, name, hNominal, hFit, hUp, hDown):
        # Make plot
        plot = plots.PlotBase()
        hNominal.SetLineColor(ROOT.kBlack)
        hNominal.SetLineWidth(2)
        plot.histoMgr.appendHisto(histograms.Histo(hNominal,"nominal"))
        hFit.SetLineColor(ROOT.kMagenta)
        hFit.SetLineWidth(2)
        plot.histoMgr.appendHisto(histograms.Histo(hFit,"fit"))
        #for j in range(1, hFit.GetNbinsX()+1):
        #    print "fit: %d: %f"%(j,hFit.GetBinContent(j))

        hUp.SetLineStyle(2)
        hUp.SetLineColor(ROOT.kBlue)
        hUp.SetLineWidth(2)
        plot.histoMgr.appendHisto(histograms.Histo(hUp,"Up"))
        hDown.SetLineStyle(2)
        hDown.SetLineColor(ROOT.kRed)
        hDown.SetLineWidth(2)
        plot.histoMgr.appendHisto(histograms.Histo(hDown,"Down"))

        myName = "tailfit_uncertainty_%s_%s"%(label,name)
        #plot.createFrame("tailfit_%s_%s"%(label,name), opts={"ymin": 1e-5, "ymaxfactor": 2.})
        #plot.getPad().SetLogy(True)
        #histograms.addCmsPreliminaryText()
        #histograms.addEnergyText()
        #histograms.addLuminosityText(x=None, y=None, lumi=self.lumi)
        myParams = {}
        myParams["ylabel"] = "Events / %.0f GeV"
        myParams["log"] = True
        myParams["opts"] = {"ymin": 1e-5}
        myDrawer = plots.PlotDrawer()
        myDrawer(plot, myName, **myParams)

    def _makeVariationPlotDetailed(self, label, name, hNominal, hFit, myUpHistograms, myDownHistograms):
        # Make plot
        plot = plots.PlotBase()
        hNominal.SetLineColor(ROOT.kBlack)
        hNominal.SetLineWidth(2)
        plot.histoMgr.appendHisto(histograms.Histo(hNominal,"nominal"))
        hFit.SetLineColor(ROOT.kMagenta)
        hFit.SetLineWidth(2)
        plot.histoMgr.appendHisto(histograms.Histo(hFit,"fit"))
        #for j in range(1, hFit.GetNbinsX()+1):
        #    print "fit: %d: %f"%(j,hFit.GetBinContent(j))

        myColor = 2
        for i in range(0, len(myUpHistograms)):
            myUpHistograms[i].SetLineStyle(myColor)
            myUpHistograms[i].SetLineColor(ROOT.kBlue)
            myUpHistograms[i].SetLineWidth(2)
            myColor += 1
            plot.histoMgr.appendHisto(histograms.Histo(myUpHistograms[i],"Up%d"%(i)))
        myColor = 2
        for i in range(0, len(myDownHistograms)):
            myDownHistograms[i].SetLineStyle(myColor)
            myDownHistograms[i].SetLineColor(ROOT.kRed)
            myDownHistograms[i].SetLineWidth(2)
            myColor += 1
            plot.histoMgr.appendHisto(histograms.Histo(myDownHistograms[i],"Down%d"%(i)))

        myName = "tailfit_detailed_%s_%s"%(label,name)
        #plot.createFrame("tailfit_%s_%s"%(label,name), opts={"ymin": 1e-5, "ymaxfactor": 2.})
        #plot.getPad().SetLogy(True)
        #histograms.addCmsPreliminaryText()
        #histograms.addEnergyText()
        #histograms.addLuminosityText(x=None, y=None, lumi=self.lumi)
        myParams = {}
        myParams["ylabel"] = "Events / %.0f GeV"
        myParams["log"] = True
        myParams["opts"] = {"ymin": 1e-5}
        myDrawer = plots.PlotDrawer()
        myDrawer(plot, myName, **myParams)