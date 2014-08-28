import ROOT
ROOT.gROOT.SetBatch(True) # no flashing canvases

import os
import sys
import inspect
import math
import array
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.aux as aux
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShellStyles import WarningLabel,HighlightStyle,NormalStyle

#_fitOptions = "RMS"
_fitOptions = "LRBS"

# Fitting functions
class FitFuncBase:
    def __init__(self, npar):
        self._npar = npar

    def getNparam(self):
        return self._npar

class FitFuncSimpleExp(FitFuncBase):
    def __init__(self):
        FitFuncBase.__init__(self, 2)

    def __call__(self, x, par):
        return par[0]*ROOT.TMath.Exp(-x[0] * par[1])

    def setParamLimits(self, fit):
        fit.SetParLimits(0,1,100000)
        fit.SetParLimits(1,1e-10,1)
        fit.SetParameter(0,10.0)
        fit.SetParameter(1,0.002)

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
        fit.SetParLimits(2,-0.001,0.001)
        fit.SetParameter(0,10.0)
        fit.SetParameter(1,0.002)
        fit.SetParameter(2,0.00001)

class FitFuncExpTailExoAlternate(FitFuncBase):
    def __init__(self):
        FitFuncBase.__init__(self, 3)

    def __call__(self, x, par):
        return par[0]*ROOT.TMath.Exp(-x[0] * par[1] + x[0] / par[2])

    def setParamLimits(self, fit):
        fit.SetParLimits(0,0.0000001,1000)
        fit.SetParLimits(1,0.0000001,1000)
        fit.SetParLimits(2,-10,10)
        fit.SetParameter(0, 1.0)
        fit.SetParameter(1, 1.0)
        fit.SetParameter(2, 1.0)

class FitFuncExpTailThreeParam(FitFuncBase):
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

class FitFuncExpTailFourParam(FitFuncBase):
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

class FitFuncExpTailFourParamAlternate(FitFuncBase):
    def __init__(self):
        FitFuncBase.__init__(self, 4)

    def __call__(self, x, par):
        return par[3]*ROOT.TMath.Exp(-(x[0]-par[2]) / (par[0] + (x[0]-par[2])/par[1]))

    def setParamLimits(self, fit):
        fit.SetParLimits(0,0.1,2000)
        fit.SetParLimits(1,0.001,10000000)
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
    def __init__(self, h, label, fitFuncName, fitmin, fitmax, applyFitFrom, doPlots=False):
        self._label = label
        self._fittedRate = None
        self._centralParams = None
        self._eigenVectors = None
        self._eigenValues = None
        self._fitmin = None
        self._hRate = aux.Clone(h)

        # Initialize style
        myStyle = tdrstyle.TDRStyle()
        myStyle.setOptStat(True)
        myStyle.tdrStyle.SetOptFit(True)

        # Find fit function class
        self._myFitFuncObject = self._findFitFunction(fitFuncName)
        # Obtain bin list for fine binning (compatibility with fine binning)
        myBinList = []
        for i in range(1, h.GetNbinsX()+1):
            myBinList.append(h.GetXaxis().GetBinLowEdge(i))
        myBinList.append(h.GetXaxis().GetBinUpEdge(h.GetNbinsX()))
        # Do fit
        myFitResult = self._doFit(h, myBinList, fitFuncName, fitmin, fitmax)
        # Calculate eigenvectors and values
        self._calculateEigenVectorsAndValues(myFitResult, printStatus=True)

        # Create histograms and control plots
        if doPlots:
            (hFitUncertaintyUp, hFitUncertaintyDown) = self.calculateVariationHistograms(myBinList, applyFitFrom)
            self.makeVariationPlotDetailed("FineBinning", self._hRate, self._hFitFineBinning, hFitUncertaintyUp, hFitUncertaintyDown)
            (hupTotal, hdownTotal) = self.calculateTotalVariationHistograms(self._hFitFineBinning, hFitUncertaintyUp, hFitUncertaintyDown)
            self.makeVariationPlotSimple("FineBinning", self._hRate, self._hFitFineBinning, hupTotal, hdownTotal)

    #def __del__(self):
        #print "test"
        #self._eigenVectors.Delete()
        #self._eigenValues.Delete()

    def getFittedRateHistogram(self, h, binlist, applyFitFrom):
        if self._fittedRate == None:
            raise Exception(ErrorLabel()+"Call _doFit() first!")
        hFit = self._functionToHistogram(self._label, self._fittedRate, self._centralParams, binlist, self._fitmin)
        myArray = array.array("d",binlist)
        hClone = h.Rebin(len(binlist)-1,self._label+"_beforeFit",myArray)
        for i in range(1,hClone.GetNbinsX()+1):
            if hClone.GetXaxis().GetBinLowEdge(i) < applyFitFrom:
                hFit.SetBinContent(i, hClone.GetBinContent(i))
                hFit.SetBinError(i, hClone.GetBinError(i))
            else:
                hFit.SetBinError(i, 0.0)
        return [hFit, hClone]

    def _findFitFunction(self, fitfunc):
        # Find fit function class
        myFitFunc = None
        for name, obj in inspect.getmembers(sys.modules[__name__]):
            if fitfunc == name:
                return obj()
        if myFitFunc == None:
            raise Exception("This should not happen...")

    def _doFit(self, h, binList, fitFuncName, fitmin, fitmax):
        # Do fit
        print "... Fitting tail for shape: %s, function=%s, range = %d-%d"%(self._label, fitFuncName, fitmin, fitmax)
        self._fittedRate = ROOT.TF1(self._label+"myFit", self._myFitFuncObject, fitmin, fitmax, self._myFitFuncObject.getNparam())
        self._myFitFuncObject.setParamLimits(self._fittedRate)
        myFitResult = h.Fit(self._fittedRate, _fitOptions)

        # Check if fit is successful
        self._myChi2 = myFitResult.Prob()
        self._myNdof = h.FindBin(fitmax) - h.FindBin(fitmin)
        if not (myFitResult.Status() == 0 and myFitResult.CovMatrixStatus() == 3):
            print WarningLabel()+"Fit failed (%d, %d)"%(myFitResult.Status(),myFitResult.CovMatrixStatus())
            # Note this does not work for Minuit2
        else:
            print "Fit success"
        print "chi2/ndof=%f (ndof=%d)"%(self._myChi2/float(self._myNdof),self._myNdof)
        self._fitmin = fitmin
        self._fitmax = fitmax

        # Convert fit to histogram
        minbin = h.GetXaxis().FindBin(fitmin)
        maxbin = h.GetXaxis().FindBin(fitmax)
        self._binWidthDuringFit = (h.GetXaxis().GetBinLowEdge(maxbin)-h.GetXaxis().GetBinLowEdge(minbin)) / (maxbin-minbin)
        self._centralParams = []
        for i in range(0, self._myFitFuncObject.getNparam()):
            self._centralParams.append(myFitResult.Parameter(i))
        self._hFitFineBinning = self._functionToHistogram(self._label+"fit", self._fittedRate, self._centralParams, binList, fitmin)
        # Return fit result
        return myFitResult

    def _calculateEigenVectorsAndValues(self, fitResult, printStatus=True):
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
                if j > 0:
                    s += " and "
                s += "%f"%vector(j)
            print s

        if self._fittedRate == None:
            raise Exception(ErrorLabel()+"Call _doFit() first!")
        # Get eigenvectors
        myCovMatrix = fitResult.GetCovarianceMatrix()
        myDiagonalizedMatrix = ROOT.TMatrixDSymEigen(myCovMatrix)
        self._eigenVectors = ROOT.TMatrixD(self._myFitFuncObject.getNparam(),self._myFitFuncObject.getNparam())
        self._eigenVectors = myDiagonalizedMatrix.GetEigenVectors()
        if printStatus:
            printEigenVectors(self._eigenVectors)
        # Get eigenvalues
        self._eigenValues = ROOT.TVectorD(self._myFitFuncObject.getNparam())
        self._eigenValues = myDiagonalizedMatrix.GetEigenValues()
        for i in range(0, self._eigenValues.GetNrows()):
            if self._eigenValues(i) < 0: # This can happen because of small fluctuations
                self._eigenValues[i] = 0
            self._eigenValues[i] = math.sqrt(self._eigenValues(i))
        if printStatus:
            printEigenValues(self._eigenValues)

    def calculateVariationHistograms(self, binList, applyFitFrom):
        if self._fittedRate == None:
            raise Exception(ErrorLabel()+"Call _doFit() first!")
        if self._eigenValues == None:
            raise Exception(ErrorLabel()+"Call _calculateEigenVectorsAndValues() first!")
        # Construct from eigenvalues and vectors the orthogonal variations
        # Up histograms
        hFitUncertaintyUp = []
        for i in range(0, self._eigenValues.GetNrows()):
            myParams = list(self._centralParams)
            for j in range(0,len(self._centralParams)):
                myParams[j] = self._centralParams[j] + self._eigenValues(i)*self._eigenVectors(j,i)
                if myParams[j] < 0:
                    myParams[j] = 1e-10
            #myShiftUp = (-1.0 * myA.getVal() / myB.getVal())
            #myFirstBin = fitmin
            #if myFirstBin < myShiftUp and myShiftUp < h.GetXaxis().GetXmax():
                #myM.setRange(0, h.GetBinLowEdge(h.FindBin(myShiftUp)))
            hUp = self._functionToHistogram(self._label+"_"+self._label+"_TailFit_par%dUp"%i, self._fittedRate, myParams, binList, applyFitFrom)
            hFitUncertaintyUp.append(hUp)

        # Down histograms
        hFitUncertaintyDown = []
        for i in range(0, self._eigenValues.GetNrows()):
            myParams = list(self._centralParams)
            for j in range(0,len(self._centralParams)):
                myParams[j] = self._centralParams[j] - self._eigenValues(i)*self._eigenVectors(j,i)
                if myParams[j] < 0:
                    myParams[j] = 0
            #myShiftDown = (-1.0 * myA.getVal() / myB.getVal())
            #myFirstBin = fitmin
            #if myFirstBin < myShiftDown and myShiftDown < h.GetXaxis().GetXmax():
                #myM.setRange(0, h.GetBinLowEdge(h.FindBin(myShiftDown)))
            hDown = self._functionToHistogram(self._label+"_"+self._label+"_TailFit_par%dDown"%i, self._fittedRate, myParams, binList, applyFitFrom)
            hFitUncertaintyDown.append(hDown)

        return (hFitUncertaintyUp, hFitUncertaintyDown)

    def calculateTotalVariationHistograms(self, hRate, hup, hdown):
        # Calculate total uncertainty (only for reference, note that can give also negative results)
        hFitUncertaintyUpTotal = aux.Clone(hup[0], self._label+"_TailFitUp")
        hFitUncertaintyUpTotal.Reset()
        hFitUncertaintyDownTotal = aux.Clone(hup[0], self._label+"_TailFitDown")
        hFitUncertaintyDownTotal.Reset()
        for i in range(1, hup[0].GetNbinsX()+1):
            myPedestal = hRate.GetBinContent(i)
            myVarianceUp = 0.0
            myVarianceDown = 0.0
            for j in range(0, len(hup)):
                a = 0.0
                b = 0.0
                if hup[j].GetBinContent(i) > 1e-10:
                    a = hup[j].GetBinContent(i) - myPedestal
                if hdown[j].GetBinContent(i) > 1e-10:
                    b = hdown[j].GetBinContent(i) - myPedestal
                (varA, varB) = aux.getProperAdditivesForVariationUncertainties(a,b)
                myVarianceUp += varA
                myVarianceDown += varB
                #print j,hup[j].GetBinContent(i),hdown[j].GetBinContent(i),a,b,varA,varB
            #print self._hFitFineBinning.GetXaxis().GetBinLowEdge(i),":", myPedestal,math.sqrt(myVarianceUp), math.sqrt(myVarianceDown), myPedestal+math.sqrt(myVarianceUp), myPedestal-math.sqrt(myVarianceDown)
            hFitUncertaintyUpTotal.SetBinContent(i, myPedestal + math.sqrt(myVarianceUp))
            hFitUncertaintyDownTotal.SetBinContent(i, myPedestal - math.sqrt(myVarianceDown))
        return (hFitUncertaintyUpTotal,hFitUncertaintyDownTotal)

    def _functionToHistogram(self, name, function, parameters, binlist, cutoff):
        myArray = array.array("d",binlist)
        h = ROOT.TH1F(name, name, len(myArray)-1, myArray)
        #print "Params for %s: %s"%(name,", ".join("%f" % x for x in parameters))
        for i in range(0,len(parameters)):
            function.SetParameter(i, parameters[i])
        for i in range(1,h.GetNbinsX()+1):
            if h.GetXaxis().GetBinLowEdge(i) >= cutoff-0.001:
                myIntegral = function.Integral(h.GetXaxis().GetBinLowEdge(i), h.GetXaxis().GetBinUpEdge(i))
                w = self._binWidthDuringFit
                #print "integral: %d-%d, %d: %f"%(h.GetXaxis().GetBinLowEdge(i), h.GetXaxis().GetBinUpEdge(i), i, myIntegral/w)
                h.SetBinContent(i, myIntegral / float(w))
            else:
                h.SetBinContent(i, self._hRate.Integral(self._hRate.GetXaxis().FindBin(h.GetXaxis().GetBinLowEdge(i)),self._hRate.GetXaxis().FindBin(h.GetXaxis().GetBinUpEdge(i)-0.001)))
        # Overflow bin
        myIntegral = h.Integral()
        if myIntegral > 0.0:
            myOverflow = function.Integral(h.GetXaxis().GetBinUpEdge(h.GetNbinsX()), 1e5)
            if myOverflow / myIntegral > 0.10:
                print WarningLabel()+"In parametrized histogram '%s', the overflow bin is very large (%f %% of total); this could mean converging problems because of badly chosen fit function or range"%(name,myOverflow / myIntegral*100.0)
            h.SetBinContent(h.GetNbinsX(),h.GetBinContent(h.GetNbinsX()) + myOverflow)

        return h

    def makeVariationPlotSimple(self, prefix, hNominal, hFit, hUp, hDown):
        # Make plot
        plot = plots.PlotBase()
        hNominalClone = aux.Clone(hNominal)
        hNominalClone.SetLineColor(ROOT.kBlack)
        hNominalClone.SetLineWidth(2)
        # Remove fit line before drawing
        myFunctions = hNominalClone.GetListOfFunctions()
        for i in range(0, myFunctions.GetEntries()):
            myFunctions.Delete()
        plot.histoMgr.appendHisto(histograms.Histo(hNominalClone,"nominal",drawStyle="e"))

        hFitClone = aux.Clone(hFit)
        hFitClone.SetLineColor(ROOT.kMagenta)
        hFitClone.SetLineWidth(2)
        plot.histoMgr.appendHisto(histograms.Histo(hFitClone,"fit"))
        #for j in range(1, self._hFitFineBinning.GetNbinsX()+1):
        #    print "fit: %d: %f"%(j,self._hFitFineBinning.GetBinContent(j))

        hUpClone = aux.Clone(hUp)
        hUpClone.SetLineStyle(2)
        hUpClone.SetLineColor(ROOT.kBlue)
        hUpClone.SetLineWidth(2)
        plot.histoMgr.appendHisto(histograms.Histo(hUpClone,"Total up"))
        hDownClone = aux.Clone(hDown)
        hDownClone.SetLineStyle(2)
        hDownClone.SetLineColor(ROOT.kRed)
        hDownClone.SetLineWidth(2)
        plot.histoMgr.appendHisto(histograms.Histo(hDownClone,"Total down"))

        myName = "tailfit_total_uncertainty_%s_%s"%(self._label,prefix)
        #plot.createFrame("tailfit_%s_%s"%(self._label,name), opts={"ymin": 1e-5, "ymaxfactor": 2.})
        #plot.getPad().SetLogy(True)
        #histograms.addStandardTexts(lumi=self.lumi)
        myParams = {}
        myParams["ylabel"] = "Events/#Deltabin / %.0f-%.0f GeV"
        myParams["log"] = True
        myParams["opts"] = {"ymin": 1e-5}
        myParams["divideByBinWidth"] = True
        myDrawer = plots.PlotDrawer()
        myDrawer(plot, myName, **myParams)

    def makeVariationPlotDetailed(self, prefix, hNominal, hFit, hFitUncertaintyUp, hFitUncertaintyDown):
        # Make plot
        plot = plots.PlotBase()
        hNominalClone = aux.Clone(hNominal)
        hNominalClone.SetLineColor(ROOT.kBlack)
        hNominalClone.SetLineWidth(2)
        # Remove fit line before drawing
        myFunctions = hNominalClone.GetListOfFunctions()
        for i in range(0, myFunctions.GetEntries()):
            myFunctions.Delete()
        plot.histoMgr.appendHisto(histograms.Histo(hNominalClone,"nominal",drawStyle="e"))

        hFitClone = aux.Clone(hFit)
        hFitClone.SetLineColor(ROOT.kMagenta)
        hFitClone.SetLineWidth(2)
        plot.histoMgr.appendHisto(histograms.Histo(hFitClone,"fit"))
        #for j in range(1, self._hFitFineBinning.GetNbinsX()+1):
        #    print "fit: %d: %f"%(j,self._hFitFineBinning.GetBinContent(j))

        myColor = 2
        for i in range(0, len(hFitUncertaintyUp)):
            hUpClone = aux.Clone(hFitUncertaintyUp[i])
            hUpClone.SetLineStyle(myColor)
            hUpClone.SetLineColor(ROOT.kBlue)
            hUpClone.SetLineWidth(2)
            myColor += 1
            plot.histoMgr.appendHisto(histograms.Histo(hUpClone,"Par%d up"%(i)))
        myColor = 2
        for i in range(0, len(hFitUncertaintyDown)):
            hDownClone = aux.Clone(hFitUncertaintyDown[i])
            hDownClone.SetLineStyle(myColor)
            hDownClone.SetLineColor(ROOT.kRed)
            hDownClone.SetLineWidth(2)
            myColor += 1
            plot.histoMgr.appendHisto(histograms.Histo(hDownClone,"Par%d down"%(i)))

        myName = "tailfit_detailed_%s_%s"%(self._label,prefix)
        #plot.createFrame("tailfit_%s_%s"%(self._label,name), opts={"ymin": 1e-5, "ymaxfactor": 2.})
        #plot.getPad().SetLogy(True)
        #histograms.addStandardTexts(lumi=self.lumi)
        myParams = {}
        myParams["ylabel"] = "Events/#Deltabin / %.0f-%.0f GeV"
        myParams["log"] = True
        myParams["opts"] = {"ymin": 1e-5}
        myParams["divideByBinWidth"] = True
        myDrawer = plots.PlotDrawer()
        myDrawer(plot, myName, **myParams)
