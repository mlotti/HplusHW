#================================================================================================  
# Imports
#================================================================================================  

import ROOT
import os
import sys
import inspect
import math
import array
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
from HiggsAnalysis.NtupleAnalysis.tools.ShellStyles import WarningLabel,HighlightStyle,NormalStyle

#================================================================================================  
# ROOT options
#================================================================================================  

# No flashing canvases
ROOT.gROOT.SetBatch(True)

# Fit options (see https://root.cern.ch/root/htmldoc/guides/users-guide/FittingHistograms.html#fitter-settings)
# WL = weighted log likelihood method, to be used when weights != 1
# R  = use range specified in the function range
# B  = fix some parameters in predefined fitting functions
# S  = save the result in TFitResult object
_fitOptions = "WL R B S"


#================================================================================================  
# Fitting function definitions
#================================================================================================

# Base class
class FitFuncBase:
    def __init__(self, npar, fitmin, scalefactor):
        self._npar = npar
        self._fitmin = fitmin
        self._scalefactor = scalefactor

    def getNparam(self):
        return self._npar

# Simple exponential function A*exp(-Bx)
class FitFuncSimpleExp(FitFuncBase):
    def __init__(self, fitmin, scalefactor):
        FitFuncBase.__init__(self, 2, fitmin, scalefactor)

    def __call__(self, x, par):
        return par[0]*ROOT.TMath.Exp(-x[0] * par[1])

    def setParamLimits(self, fit):
        fit.SetParLimits(0,1,100000)
        fit.SetParLimits(1,1e-10,1)
        fit.SetParameter(0,10.0)
        fit.SetParameter(1,0.002)

# A*exp(-Bx-(x-C)^2/D)
class FitFuncGausExpTail(FitFuncBase):
    def __init__(self, fitmin, scalefactor):
        FitFuncBase.__init__(self, 4, fitmin, scalefactor)

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

# Aexp(-Bx-Cx^2)
class FitFuncExpTailExo(FitFuncBase):
    def __init__(self, fitmin, scalefactor):
        FitFuncBase.__init__(self, 3, fitmin, scalefactor)

    def __call__(self, x, par):
        return par[0]*ROOT.TMath.Exp(-x[0] * par[1] - (x[0]**2*par[2]))

    def setParamLimits(self, fit):
        fit.SetParLimits(0,1,100000)
        fit.SetParLimits(1,1e-10,0.1)
        fit.SetParLimits(2,-0.001,0.001)
        fit.SetParameter(0,10.0)
        fit.SetParameter(1,0.002)
        fit.SetParameter(2,0.00001)

# Aexp(-Bx) starting from fitmin
class FitFuncPreFitForIntegral(FitFuncBase):
    def __init__(self, fitmin, scalefactor):
        FitFuncBase.__init__(self, 2, fitmin, scalefactor)

    def __call__(self, x, par):
        m = x[0]-self._fitmin
        return par[0]*ROOT.TMath.Exp(-m * (par[1]))
        #return par[0]*ROOT.TMath.Exp(-m * (par[1] + m / par[2]))
        #return par[0]*ROOT.TMath.Exp(-(x[0]-par[3]) * (par[1] + (x[0]-par[3]) / par[2]))

    def setParamLimits(self, fit):
        fit.SetParLimits(0,0.001,10)
        fit.SetParLimits(1,0.001,10)
        #fit.SetParLimits(2,-10,10)
        fit.SetParameter(0, 0.1)
        fit.SetParameter(1, 0.1)
        #fit.SetParameter(2, 1.0)

# SF*Aexp(-Bx) starting from fitmin
class FitFuncExpTailTauTauAlternate(FitFuncBase):
    def __init__(self, fitmin, scalefactor):
        FitFuncBase.__init__(self, 3, fitmin, scalefactor)

    def __call__(self, x, par):
        m = x[0]-self._fitmin
        return self._scalefactor*par[0]*ROOT.TMath.Exp(-m / (par[1] - (m)*0.001*par[2]))
        #return self._scalefactor*par[0]*ROOT.TMath.Exp(-m/(par[1]+par[2]*m))
        #return par[0]*ROOT.TMath.Exp(-m * (par[1] + m / par[2]))
        #return par[0]*ROOT.TMath.Exp(-(x[0]-par[3]) * (par[1] + (x[0]-par[3]) / par[2]))

    def setParamLimits(self, fit):
        fit.SetParLimits(0,0.001,1000)
        fit.SetParLimits(1,0.001,10000)
        fit.SetParLimits(2,0.001,1)
        fit.SetParameter(0, 0.1)
        fit.SetParameter(1, 0.1)
        fit.SetParameter(2, 0.001)

# SF*Aexp(-Bx-Cx^2) starting from fitmin
class FitFuncExpTailExoAlternate2(FitFuncBase):
    def __init__(self, fitmin, scalefactor):
        FitFuncBase.__init__(self, 3, fitmin, scalefactor)

    def __call__(self, x, par):
        m = x[0]-self._fitmin
        return self._scalefactor*par[0]*ROOT.TMath.Exp(-m * (par[1] - m*(par[2])))
        #return self._scalefactor*par[0]*ROOT.TMath.Exp(-m/(par[1]+par[2]*m))
        #return par[0]*ROOT.TMath.Exp(-m * (par[1] + m / par[2]))
        #return par[0]*ROOT.TMath.Exp(-(x[0]-par[3]) * (par[1] + (x[0]-par[3]) / par[2]))

    def setParamLimits(self, fit):
        fit.SetParLimits(0,0.001,1000)
        fit.SetParLimits(1,0.00001,10000)
        fit.SetParLimits(2,-0.001,0.001)
        fit.SetParameter(0, 0.1)
        fit.SetParameter(1, 0.002)
        fit.SetParameter(2, 0.1)

# SF*Aexp(-Bx) starting from fitmin
class FitFuncExpTailExoAlternate(FitFuncBase):
    def __init__(self, fitmin, scalefactor):
        FitFuncBase.__init__(self, 2, fitmin, scalefactor)

    def __call__(self, x, par):
        m = x[0]-self._fitmin
        return self._scalefactor*par[0]*ROOT.TMath.Exp(-m * (par[1]))
        #return self._scalefactor*par[0]*ROOT.TMath.Exp(-m/(par[1]+par[2]*m))
        #return par[0]*ROOT.TMath.Exp(-m * (par[1] + m / par[2]))
        #return par[0]*ROOT.TMath.Exp(-(x[0]-par[3]) * (par[1] + (x[0]-par[3]) / par[2]))

    def setParamLimits(self, fit):
        fit.SetParLimits(0,0.001,10)
        fit.SetParLimits(1,0.001,10)
        #fit.SetParLimits(2,0.000001,1)
        fit.SetParameter(0, 0.1)
        fit.SetParameter(1, 0.1)
        #fit.SetParameter(2, 0.001)

# Aexp(-x/(B+Cx))
class FitFuncExpTailThreeParam(FitFuncBase):
    def __init__(self, fitmin, scalefactor):
        FitFuncBase.__init__(self, 3, fitmin, scalefactor)

    def __call__(self, x, par):
        return par[0]*ROOT.TMath.Exp(-x[0] / (par[1] + x[0]*par[2]))

    def setParamLimits(self, fit):
        fit.SetParLimits(0,1,100000)
        fit.SetParLimits(1,0.1,200)
        fit.SetParLimits(2,-20.0,20.0)
        fit.SetParameter(0,10.0)
        fit.SetParameter(1,1)
        fit.SetParameter(2,0.00001)

# Aexp(-(x-B)/(C*(X-d)))
class FitFuncExpTailFourParam(FitFuncBase):
    def __init__(self, fitmin, scalefactor):
        FitFuncBase.__init__(self, 4, fitmin, scalefactor)

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

# Aexp(-(x-B)/(C+((X-B)/D)))
class FitFuncExpTailFourParamAlternate(FitFuncBase):
    def __init__(self, fitmin, scalefactor):
        FitFuncBase.__init__(self, 4, fitmin, scalefactor)

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

#================================================================================================  
# Plus and minus variations of fit parameters
#================================================================================================

def doPlusVariation(self, func):
    for i in range(1,self._npar):
        func.SetParameter(i, func.GetParameter(i) + func.GetParError(i))

def doMinusVariation(self, func):
    for i in range(1,self._npar):
        func.SetParameter(i, func.GetParameter(i) - func.GetParError(i))

#================================================================================================  
# TailFitter class
# This class does the actual fitting (using helper functions defined above) and plots the result
#================================================================================================

class TailFitter:

    # --- Constructor: takes in the fine-binned histo to be fitted (h) and fit parameters, performs the fit
    def __init__(self, h, label, fitFuncName, fitmin, fitmax, applyFitFrom, doPlots=False, luminosity=None):
        self._label = label
        self._fittedRate = None
        self._centralParams = None
        self._eigenVectors = None
        self._eigenValues = None
        self._fitmin = fitmin
        self._hRate = aux.Clone(h)
        self._luminosity = luminosity
        self._datasetNames = {}

        # Initialize style
        myStyle = tdrstyle.TDRStyle()
        myStyle.setOptStat(True)
        myStyle.tdrStyle.SetOptFit(True)

        # Calculate scale factor by integrating over the area to be fitted
        scaleFactor = h.Integral(h.FindBin(fitmin),h.GetNbinsX()+1)

        # Set fit function
        self._myFitFuncObject = self._findFitFunction(fitFuncName, scaleFactor)

        # Obtain bin list for fine binning (compatibility with fine binning)
        myBinList = []
        for i in range(1, h.GetNbinsX()+1):
            myBinList.append(h.GetXaxis().GetBinLowEdge(i))
        myBinList.append(h.GetXaxis().GetBinUpEdge(h.GetNbinsX()))

        # Do fit
        myFitResult = self._doFit(h, myBinList, fitFuncName, fitmin, fitmax)

        # Calculate eigenvectors and values
        self._calculateEigenVectorsAndValues(myFitResult, printStatus=True)

        # Dataset names (used for plotting, maps dataset label to its legend)
        self._datasetNames["ttbar"] = "t#bar{t}"
        self._datasetNames["W"] = "W+Jets"
        self._datasetNames["singleTop"] = "Single t"
        self._datasetNames["DY"] = "Z/#gamma*+jets"
        self._datasetNames["VV"] = "Diboson"
        self._datasetNames["QCDandFakeTau"] = "Mis-ID. #tau_{h} (data)"

        # Create varied histograms (fit uncertainty up and down, total uncertainty up and donw) and make plots
        if doPlots:
            (hFitUncertaintyUp, hFitUncertaintyDown) = self.calculateVariationHistograms(myBinList, applyFitFrom)
            self.makeVariationPlotWithSeparateUncertainties("_FineBinning", self._hRate, self._hFitFineBinning, hFitUncertaintyUp, hFitUncertaintyDown, applyFitFrom)
            (hupTotal, hdownTotal) = self.calculateTotalVariationHistograms(self._hFitFineBinning, hFitUncertaintyUp, hFitUncertaintyDown)
            self.makeVariationPlotWithTotalUncertainties("_FineBinning", self._hRate, self._hFitFineBinning, hupTotal, hdownTotal, applyFitFrom)
    # --- (end of constructor)

    
    # Method to get the original histogram and the fitted one
    def getFittedRateHistogram(self, h, binlist, applyFitFrom):
        if self._fittedRate == None:
            raise Exception(ErrorLabel()+"Call _doFit() first (should be called in constructor of TailFitter class)!")
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

    # Helper function to set fit function and scale factor
    def _findFitFunction(self, fitfunc, scalefactor):
        # Find fit function class
        myFitFunc = None
        for name, obj in inspect.getmembers(sys.modules[__name__]):
            if fitfunc == name:
                return obj(self._fitmin, scalefactor)
        if myFitFunc == None:
            raise Exception("This should not happen...")

    # Helper function that carry out actual fitting for given histogram h, 
    # saves the result to self._hFitFineBinning and returns myFitResult object
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

    # Helper function to calculate eigenvectors and eigenvalues from FitResult
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
        print "Covariance matrix:"
        for i in range(0, myCovMatrix.GetNcols()):
            s = []
            for j in range(0, myCovMatrix.GetNrows()):
                s.append("%f"%myCovMatrix(i,j))
            print "  (%s)"%", ".join(map(str,s))
        myDiagonalizedMatrix = ROOT.TMatrixDSymEigen(myCovMatrix)
        self._eigenVectors = ROOT.TMatrixD(self._myFitFuncObject.getNparam(),self._myFitFuncObject.getNparam())
        self._eigenVectors = myDiagonalizedMatrix.GetEigenVectors()
        print "Diagonalized matrix:"
        myDiagonalizedMatrix.GetEigenVectors().Print()
        if printStatus:
            printEigenVectors(self._eigenVectors)
        # Get eigenvalues 
        eigenValues = ROOT.TVectorD(self._myFitFuncObject.getNparam())
        eigenValues = myDiagonalizedMatrix.GetEigenValues()
        self._eigenValues = []
        for i in range(0, eigenValues.GetNrows()):
            if eigenValues(i) < 0: # This can happen because of small fluctuations
                self._eigenValues.append(0.0)
            self._eigenValues.append(math.sqrt(eigenValues(i)))
        if printStatus:
            #printEigenValues(self._eigenValues)
            print self._eigenValues

    # Create up/down varoed histograms with orthogonal fit uncertainty variations,
    # calculated using eigenvalues and vectors, one variation for each fir parameter
    def calculateVariationHistograms(self, binList, applyFitFrom):
        if self._fittedRate == None:
            raise Exception(ErrorLabel()+"Call _doFit() first!")
        if self._eigenValues == None:
            raise Exception(ErrorLabel()+"Call _calculateEigenVectorsAndValues() first!")
        # Create histograms (hFitUncertaintyUp)
        print "Nominal parameters: (%s)"%(", ".join(map(str,self._centralParams)))
        print "Varying parameters up"
        hFitUncertaintyUp = []
        for j in range(0, len(self._eigenValues)):
            myParams = list(self._centralParams)
            for i in range(0,len(self._centralParams)):
                myParams[i] = self._centralParams[i] + self._eigenValues[j]*self._eigenVectors(i,j)
            print "eigenvalue: %d, function params: (%s)"%(j, ", ".join(map(str,myParams)))
            hUp = self._functionToHistogram(self._label+"_"+self._label+"_TailFit_par%dUp"%j, self._fittedRate, myParams, binList, applyFitFrom)
            hFitUncertaintyUp.append(hUp)
        # Create down histograms (hFitUncertaintyDown)
        print "Varying parameters down"
        hFitUncertaintyDown = []
        for j in range(0, len(self._eigenValues)):
            myParams = list(self._centralParams)
            for i in range(0,len(self._centralParams)):
                myParams[i] = self._centralParams[i] - self._eigenValues[j]*self._eigenVectors(i,j)
            print "eigenvalue: %d, function params: (%s)"%(j, ", ".join(map(str,myParams)))
            hDown = self._functionToHistogram(self._label+"_"+self._label+"_TailFit_par%dDown"%j, self._fittedRate, myParams, binList, applyFitFrom)
            hFitUncertaintyDown.append(hDown)
        # Return both up and down varied histograms
        return (hFitUncertaintyUp, hFitUncertaintyDown)

    # Calculate total fit uncertainties (combined effect of variations of different fit parameters),
    # this is only for reference, note that this can give also negative results
    def calculateTotalVariationHistograms(self, hRate, hup, hdown):
        # Create empty histogram templates
        hFitUncertaintyUpTotal = aux.Clone(hup[0], self._label+"_TailFitUp")
        hFitUncertaintyDownTotal = aux.Clone(hup[0], self._label+"_TailFitDown")
        hFitUncertaintyUpTotal.Reset() # clean bin contents and errors
        hFitUncertaintyDownTotal.Reset() # clean bin contents and errors
        for i in range(1, hup[0].GetNbinsX()+1):
            myPedestal = hRate.GetBinContent(i)
            myVarianceUp = 0.0
            myVarianceDown = 0.0
            for j in range(0, len(hup)):
                a = 0.0
                b = 0.0
                if hup[j].GetBinContent(i) > 0.0:
                    a = hup[j].GetBinContent(i) - myPedestal
                else:
                    a = -myPedestal;
                if hdown[j].GetBinContent(i) > 0.0:
                    b = hdown[j].GetBinContent(i) - myPedestal
                else:
                    b = -myPedestal;
                if abs(a) != float('Inf') and not math.isnan(a) and abs(b) != float('Inf') and not math.isnan(b):
                    (varA, varB) = aux.getProperAdditivesForVariationUncertainties(a,b) # essentially squaring a and b
                    myVarianceUp += varA
                    myVarianceDown += varB
            hFitUncertaintyUpTotal.SetBinContent(i, myPedestal + math.sqrt(myVarianceUp))
            hFitUncertaintyDownTotal.SetBinContent(i, myPedestal - math.sqrt(myVarianceDown))
        return (hFitUncertaintyUpTotal,hFitUncertaintyDownTotal)

    # Helper function to convert a fit function into a histogram so that it can be plotted
    def _functionToHistogram(self, name, function, parameters, binlist, cutoff):
        myArray = array.array("d",binlist)
        h = ROOT.TH1F(name, name, len(myArray)-1, myArray)
        for i in range(0,len(parameters)):
            function.SetParameter(i, parameters[i])
        for i in range(1,h.GetNbinsX()+1):
            if h.GetXaxis().GetBinLowEdge(i) >= cutoff-0.001:
                myIntegral = function.Integral(h.GetXaxis().GetBinLowEdge(i), h.GetXaxis().GetBinUpEdge(i))
                w = self._binWidthDuringFit
                h.SetBinContent(i, myIntegral / float(w))
            else:
                h.SetBinContent(i, self._hRate.Integral(self._hRate.GetXaxis().FindBin(h.GetXaxis().GetBinLowEdge(i)),self._hRate.GetXaxis().FindBin(h.GetXaxis().GetBinUpEdge(i)-0.001)))
        # Handle overflow bin
        myIntegral = h.Integral()
        if myIntegral > 0.0:
            myOverflow = function.Integral(h.GetXaxis().GetBinUpEdge(h.GetNbinsX()), 1e5)
            if myOverflow / myIntegral > 0.10:
                print WarningLabel()+"In parametrized histogram '%s', the overflow bin is very large (%f %% of total); this could mean converging problems because of badly chosen fit function or range"%(name,myOverflow / myIntegral*100.0)
            if myOverflow < 0.0:
                print WarningLabel()+"In parametrized histogram '%s', the overflow bin is negative and set to zero; this could mean converging problems because of badly chosen fit function or range"%(name)
                myOverflow = 0.0
            w = self._binWidthDuringFit
            h.SetBinContent(h.GetNbinsX(),h.GetBinContent(h.GetNbinsX()) + myOverflow/float(w))
        return h

    # Plot total variations
    def makeVariationPlotWithTotalUncertainties(self, prefix, hNominal, hFit, hUp, hDown, fitmin=180):
        # Make plot
        plot = plots.PlotBase()
        hNominalClone = aux.Clone(hNominal)
        hNominalClone.SetLineColor(ROOT.kBlack)
        hNominalClone.SetLineWidth(2)
        hNominalClone.SetMarkerStyle(22)
        hNominalClone.SetMarkerSize(1.5)
        # Remove fit line before drawing
        myFunctions = hNominalClone.GetListOfFunctions()
        for i in range(0, myFunctions.GetEntries()):
            myFunctions.Delete()
        plot.histoMgr.appendHisto(histograms.Histo(hNominalClone,"nominal",drawStyle="pe", legendStyle="pe"))

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

        fitStart = fitmin
        nominal = "Nominal"

        for key in self._datasetNames:
            if key in self._label:
                nominal += ", %s"%self._datasetNames[key]
            
        plot.histoMgr.setHistoLegendLabelMany({
            "nominal": nominal,
            "fit": "With fit for m_{T} > %d GeV" % fitStart,
            "Total up": "+1#sigma uncertainty",
            "Total down": "-1#sigma uncertainty"
        })
        if self._luminosity is not None:
            plot.setLuminosity(self._luminosity)

        myName = "tailfit_total_uncertainty_%s%s"%(self._label,prefix)
        myParams = {}
        #myParams["ylabel"] = "Events/#Deltabin / %.0f-%.0f GeV"
        myParams["ylabel"] = "Events / %.0f GeV"
        myParams["log"] = True
        myParams["opts"] = {"ymin": 2*1e-5, "xmax" : 800} # compensate for the bin width
        myParams["divideByBinWidth"] = True
	myParams["cmsTextPosition"] = "right"
	myParams["moveLegend"] = {"dx": -0.215, "dy": -0.1, "dh": -0.1, "dw": -0.05}
	myParams["xlabel"] = "m_{T} (GeV)"
        myDrawer = plots.PlotDrawer()
        myDrawer(plot, myName, **myParams)

    # Plot fit parameter variations
    def makeVariationPlotWithSeparateUncertainties(self, prefix, hNominal, hFit, hFitUncertaintyUp, hFitUncertaintyDown, fitmin=180):
        # Make plot
        plot = plots.PlotBase()
        hNominalClone = aux.Clone(hNominal)
        hNominalClone.SetLineColor(ROOT.kBlack)
        hNominalClone.SetLineWidth(2)
        hNominalClone.SetMarkerStyle(22)
        hNominalClone.SetMarkerSize(1.5)
        # Remove fit line before drawing
        myFunctions = hNominalClone.GetListOfFunctions()
        for i in range(0, myFunctions.GetEntries()):
            myFunctions.Delete()
        plot.histoMgr.appendHisto(histograms.Histo(hNominalClone,"nominal",drawStyle="e"))

        hFitClone = aux.Clone(hFit)
        hFitClone.SetLineColor(ROOT.kMagenta)
        hFitClone.SetLineWidth(2)
        plot.histoMgr.appendHisto(histograms.Histo(hFitClone,"fit"))

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

        fitStart = fitmin
        nominal = "Nominal"

        for key in self._datasetNames:
            if key in self._label:
                nominal += ", %s"%self._datasetNames[key]

        plot.histoMgr.setHistoLegendLabelMany({
            "nominal": nominal,
            "fit": "With fit for m_{T} > %d GeV" % fitStart,
            "Par0 up": "+1#sigma uncertainty on par.0",
            "Par0 down": "-1#sigma uncertainty on par.0",
            "Par1 up": "+1#sigma uncertainty on par.1",
            "Par1 down": "-1#sigma uncertainty on par.1"
        })
        if self._luminosity is not None:
            plot.setLuminosity(self._luminosity)

        myName = "tailfit_detailed_%s%s"%(self._label,prefix)
        myParams = {}
	myParams["ylabel"] = "Events / %.0f GeV"
        myParams["log"] = True
        myParams["opts"] = {"ymin": 2*1e-5, "xmax" : 800} # compensate for the bin width
        myParams["divideByBinWidth"] = True
	myParams["cmsTextPosition"] = "right"
	myParams["moveLegend"] = {"dx": -0.215, "dy": -0.1, "dh": -0.1, "dw": -0.05}
	myParams["xlabel"] = "m_{T} (GeV)"
        myDrawer = plots.PlotDrawer()
        myDrawer(plot, myName, **myParams)
