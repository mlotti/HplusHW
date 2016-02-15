## \package FitHelper

import ROOT
ROOT.gROOT.SetBatch(True)
import math
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux

class FitParameterOrthogonalizer:
    ## Default constructor
    # The strategy is to first diagonalize the error matrix of the fit parameters
    # and then vary in this orthogonal base the fit parameters up and down by
    # one standard deviation. These variations are independent of each other
    # and can therefore be combined with a square sum, although here also
    # fluctuations in the same direction are treated properly
    #
    # \param fitFunctionObject  a ROOT TF1 object describing the fit function
    # \param fitResult          the result object from calling TH1::Fit
    # \param printStatus        option to enable/disable printing of output
    def __init__(self, fitFunctionObject, fitResult, rangeMin, rangeMax, printStatus=False):
        self._myFitFuncObject = fitFunctionObject
        self._fitResult = fitResult
        self._eigenVectors = None
        self._eigenValues = None
        self._calculateEigenVectorsAndValues(printStatus)
        self._downVariations = []
        self._upVariations = []
        self._downVariationTotal = None
        self._upVariationTotal = None
        self._calculateVariations(rangeMin, rangeMax)
    
    def getEigenValues(self):
        return self._eigenValues
    
    def getEigenVectors(self):
        return self._eigenVectors

    def getTotalFitParameterUncertaintyDown(self):
        return self._downVariationTotal

    def getTotalFitParameterUncertaintyUp(self):
        return self._upVariationTotal

    ## Returns the absolute uncertainty from varying orthogonal fit parameters
    def _calculateVariations(self, rangeMin, rangeMax):
        nominalInt = self._myFitFuncObject.Integral(rangeMin, rangeMax)
        #print nominalInt, self._myFitFuncObject.IntegralError(float(rangeMin), float(rangeMax))
        centralParams = []
        for i in range(self._myFitFuncObject.GetNpar()):
            centralParams.append(self._myFitFuncObject.GetParameter(i))
        if len(centralParams) > 100:
            raise Exception("This should not happen") # Protect against memory overflow
        function = self._myFitFuncObject
        # Up variations
        self._upVariations = []
        for j in range(0, len(self._eigenValues)):
            myParams = list(centralParams)
            for i in range(0,len(centralParams)):
                myParams[i] = centralParams[i] + self._eigenValues[j]*self._eigenVectors(i,j)
            #print "eigenvalue: %d, function params: (%s)"%(j, ", ".join(map(str,myParams)))
            for i in range(0,len(myParams)):
                function.SetParameter(i, myParams[i])
            self._upVariations.append(function.Integral(rangeMin, rangeMax) - nominalInt)
        # Down variations
        self._downVariations = []
        for j in range(0, len(self._eigenValues)):
            myParams = list(centralParams)
            for i in range(0,len(centralParams)):
                myParams[i] = centralParams[i] - self._eigenValues[j]*self._eigenVectors(i,j)
            #print "eigenvalue: %d, function params: (%s)"%(j, ", ".join(map(str,myParams)))
            for i in range(0,len(myParams)):
                function.SetParameter(i, myParams[i])
            self._downVariations.append(function.Integral(rangeMin, rangeMax) - nominalInt)
        # Calculate totals
        upSquared = 0.0
        downSquared = 0.0
        nanStatus = False
        for i in range(len(self._upVariations)):
            if math.isnan(self._upVariations[i]) or math.isnan(self._downVariations[i]):
                print "Oops, got a nan for the fit parameter %d!"%i
                nanStatus = True
        if not nanStatus:
            for i in range(len(self._upVariations)):
                (upProperSquared, downProperSquared) = aux.getProperAdditivesForVariationUncertainties(self._upVariations[i], self._downVariations[i])
                upSquared += upProperSquared
                downSquared += downProperSquared
        self._upVariationTotal = math.sqrt(upSquared)
        self._downVariationTotal = math.sqrt(downSquared)
    
    def _calculateEigenVectorsAndValues(self, printStatus=True):
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

        # Get eigenvectors
        myCovMatrix = self._fitResult.GetCovarianceMatrix()
        if printStatus:
            print "Covariance matrix:"
            for i in range(0, myCovMatrix.GetNcols()):
                s = []
                for j in range(0, myCovMatrix.GetNrows()):
                    s.append("%f"%myCovMatrix(i,j))
                print "  (%s)"%", ".join(map(str,s))
        myDiagonalizedMatrix = ROOT.TMatrixDSymEigen(myCovMatrix)
        self._eigenVectors = ROOT.TMatrixD(myCovMatrix.GetNcols(), myCovMatrix.GetNcols())
        self._eigenVectors = myDiagonalizedMatrix.GetEigenVectors()
        if printStatus:
            print "Diagonalized matrix:"
            myDiagonalizedMatrix.GetEigenVectors().Print()
            printEigenVectors(self._eigenVectors)
        # Get eigenvalues 
        eigenValues = ROOT.TVectorD(myCovMatrix.GetNcols())
        eigenValues = myDiagonalizedMatrix.GetEigenValues()
        self._eigenValues = []
        for i in range(0, eigenValues.GetNrows()):
            if eigenValues(i) < 0.0: # This can happen because of small fluctuations
                self._eigenValues.append(0.0)
                print "Warning: Eigenvalue is zero (this usually means that the fit did not converge correctly)"
            else:
                self._eigenValues.append(math.sqrt(eigenValues(i)))

# Unit tests
if __name__ == "__main__":
    import unittest
    class TestFitParameterOrthogonalizer(unittest.TestCase):
        def testAlgorithm(self):
            class MyFit:
                def __call__(self, x, par):
                    return par[0]*100.0*ROOT.TMath.Gaus(x[0],par[1],par[2],1)
            # Create histogram filled with Gaussian(4,2)
            h = ROOT.TH1F("h","h",10,0,10)
            h.Sumw2()
            h.SetBinContent(0, 27)
            h.SetBinContent(1, 42)
            h.SetBinContent(2, 87)
            h.SetBinContent(3, 135)
            h.SetBinContent(4, 213)
            h.SetBinContent(5, 181)
            h.SetBinContent(6, 134)
            h.SetBinContent(7, 105)
            h.SetBinContent(8, 46)
            h.SetBinContent(9, 22)
            h.SetBinContent(10, 7)
            h.SetBinContent(11, 1)
            # Do fit
            fit = ROOT.TF1("fit", MyFit(), 0, 10, 3)
            fit.SetParameter(0,10)
            fit.SetParameter(1,4)
            fit.SetParameter(2,1)
            fitResult = h.Fit(fit,"S R WL I Q")
            # Test eigenvalues
            fpo = FitParameterOrthogonalizer(fit, fitResult, 0, 10, printStatus=False)
            eigenValues = fpo.getEigenValues()
            eigenVectors = fpo.getEigenVectors()
            self.assertLess(abs(eigenValues[0]-0.0378), 0.0001)
            self.assertLess(abs(eigenValues[1]-0.0105), 0.0001)
            self.assertLess(abs(eigenValues[2]-0.00893), 0.0001)
            # Test total uncertainties
            self.assertLess(abs(fpo.getTotalFitParameterUncertaintyUp()-3.16), 0.01)
            self.assertLess(abs(fpo.getTotalFitParameterUncertaintyDown()-3.17), 0.01)

    unittest.main()
    