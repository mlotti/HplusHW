'''
Description:
This package contains the tools for calculating 
the normalization factors from FakeBMeasurementAnalysis

Instructions for using, call the following methods:
1) create manager (each algorithm has it's own manager inheriting from a base class)
2) create templates (createTemplate()) and add fit functions to them (template::setFitter)
3) loop over bins and start by calling resetBinResults()
4) for each bin, add histogram to templates (template::setHistogram)
5) for each bin, plot templates (plotTemplates())
6) for each bin, calculate norm.coefficients (calculateNormalizationCoefficients())
7) for each bin, calculate combined norm.coefficient (calculateCombinedNormalization())
'''
#================================================================================================ 
# Imports
#================================================================================================ 
import ROOT
ROOT.gROOT.SetBatch(True)
import HiggsAnalysis.NtupleAnalysis.tools.fitHelper as fitHelper
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.styles as styles
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux
from HiggsAnalysis.NtupleAnalysis.tools.OrderedDict import OrderedDict
import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.errorPropagation as errorPropagation
import os
import shutil
import array
import sys
import datetime

#================================================================================================ 
# Class Definitions
#================================================================================================ 
class colors:
    '''
    \033[  Escape code, this is always the same
    1 = Style, 1 for normal.
    32 = Text colour, 32 for bright green.
    40m = Background colour, 40 is for black.

    WARNING:
    Python doesn't distinguish between 'normal' characters and ANSI colour codes, which are also characters that the terminal interprets.
    In other words, printing '\x1b[92m' to a terminal may change the terminal text colour, Python doesn't see that as anything but a set of 5 characters.
    If you use print repr(line) instead, python will print the string literal form instead, including using escape codes for non-ASCII printable characters
    (so the ESC ASCII code, 27, is displayed as \x1b) to see how many have been added.

    You'll need to adjust your column alignments manually to allow for those extra characters.
    Without your actual code, that's hard for us to help you with though.

    Useful Links:
    http://ozzmaker.com/add-colour-to-text-in-python/
    http://stackoverflow.com/questions/15580303/python-output-complex-line-with-floats-colored-by-value
    '''      
    
    colordict = {
                'RED'      :'\033[91m',
                'GREEN'    :'\033[92m',
                'BLUE'     :'\033[34m',
                'GRAY'     :'\033[90m',
                'WHITE'    :'\033[00m',
                'ORANGE'   :'\033[33m',
                'CYAN'     :'\033[36m',
                'PURPLE'   :'\033[35m',
                'LIGHTRED' :'\033[91m',
                'PINK'     :'\033[95m',
                'YELLOW'   :'\033[93m',
                }

    if sys.stdout.isatty():
        RED      = colordict['RED']
        GREEN    = colordict['GREEN']
        BLUE     = colordict['BLUE']
        GRAY     = colordict['GRAY']
        WHITE    = colordict['WHITE']
        ORANGE   = colordict['ORANGE']
        CYAN     = colordict['CYAN']
        PURPLE   = colordict['PURPLE']
        LIGHTRED = colordict['LIGHTRED']
        PINK     = colordict['PINK']
        YELLOW   = colordict['YELLOW']
    else:
        RED, GREEN, BLUE, GRAY, WHITE, ORANGE, CYAN, PURPLE, LIGHTRED, PINK, YELLOW = '', '', '', '', '', '', '', '', '', '', ''


#================================================================================================ 
# Class Definitions
#================================================================================================ 
class FunctionSum:
    '''
    Helper class for merging fit functions
    '''
    def __init__(self, f1, f2):
        self._f1 = f1.Clone()
        self._f2 = f2.Clone()
    def __call__(self, x):
        return self._f1.Eval(x[0]) + self._f2.Eval(x[0])


#================================================================================================ 
# Class Definitions
#================================================================================================ 
class FitFunction:
    '''
    Container class for fit functions
    '''
    def __init__(self, functionName, **kwargs):
        self._functionName = functionName
        self._args = kwargs
        self._additionalNormFactor = 1.0
        
        if not hasattr(self, functionName):
            raise Exception("Error: FitFunction '%s' is unknown!" % functionName)

        # Dictionary of FitFunction <-> Parameters
        nParams = {
            "Linear": 2,
            "ErrorFunction": 2,
            "ExpFunction": 2,
            "Gaussian": 3,
            "DoubleGaussian": 6,
            "SumFunction": 5,
            "RayleighFunction": 2,
            "EWKFunctionInv": 4,
            "QCDEWKFunction": 7,
            "QCDFunctionFixed": 8,
            "FitDataWithQCDAndFakesAndGenuineTaus": 3,
            "FitDataWithQCDAndInclusiveEWK": 2,
            "FitDataWithFakesAndGenuineTaus": 2,
            "EWKFunction": 10, #5
            "QCDFunction": 7,
            "CrystalBall": 5,
        }

        if not functionName in nParams.keys():
            raise Exception("Error: FitFunction '%s' is not included into nParams dictionary!" % functionName)
        self._nParam = nParams[functionName]
        return

    def clone(self):
        f = FitFunction(self._functionName, **self._args)
        f.setAdditionalNormalization(self._additionalNormFactor)
        return f
    
    def setAdditionalNormalization(self, factor):
        self._additionalNormFactor = factor
        return

    def __call__(self, x, par, **kwargs):
        '''
        The __init__ method is used when the class is called to initialize the instance,
        while the __call__ method is called when the instance is called.
        '''
        args = {}
        for k in self._args.keys():
            args[k] = self._args[k]

        for k in kwargs:
            args[k] = kwargs[k]

        return getattr(self, self._functionName)(x, par, **args)

    def getNParam(self):
        return self._nParam

    def getName(self):
        return self._functionName

    #===== Primitive functions
    def Linear(self, x, par):
        return par[0]*x[0] + par[1]

    def ErrorFunction(self,x,par):
        return 0.5*(1 + ROOT.TMath.Erf(par[0]*(x[0] - par[1])))

    def ExpFunction(self,x,par):        
        if (x[0] > 280 and x[0] < 300) or x[0] > 360:
            ROOT.TF1.RejectPoint()
            return 0
        return par[0]*ROOT.TMath.Exp(-x[0]*par[1])
    
    def Gaussian(self,x,par):
        return par[0]*ROOT.TMath.Gaus(x[0],par[1],par[2],1)
    
    def DoubleGaussian(self,x,par):
        return par[0]*ROOT.TMath.Gaus(x[0],par[1],par[2],1) + par[3]*ROOT.TMath.Gaus(x[0],par[4],par[5],1)
    
    def SumFunction(self,x,par):
        return par[0]*ROOT.TMath.Gaus(x[0],par[1],par[2],1) + par[3]*ROOT.TMath.Exp(-x[0]*par[4])

    def RayleighFunction(self,x,par,norm):
        if par[0]+par[1]*x[0] == 0.0:
            return 0
        return norm*(par[1]*x[0]/((par[0])*(par[0]))*ROOT.TMath.Exp(-x[0]*x[0]/(2*(par[0])*(par[0]))))

    def BreitWigner(self, x, par):
        '''
        https://root.cern.ch/root/html524/ROOT__Math.html#TopOfPage
        https://root.cern.ch/doc/v606/group__PdfFunc.html#ga674162ea051bf687243264996d046f73

        2 parameters: gamma, mu

        breitwigner_pdf(x, gamma=Decay Width, mu=Resonance Mass)
        '''
        return par[0]*ROOT.TMath.BreitWigner(x[0], par[1], par[2])

    def CrystalBall(self, x, par):
        '''
        https://root.cern.ch/root/html524/ROOT__Math.html#TopOfPage

        Predefined Probability Density Functions (PDF) in ROOT:
        https://root.cern.ch/doc/v608/group__PdfFunc.html
        https://root.cern.ch/doc/v606/group__PdfFunc.html#ga6d2dcba56ea7438dab7e47e8c06c83f6

        4 parameters: alpha, N, sigma, mu

        crystalball(x, alpha=Gaussian Tail, N=Normalisation, sigma=Mass Resolution, mu=Mass mean value)
        '''
        return par[0]*ROOT.Math.crystalball_function(x[0], par[1], par[2], par[3], par[4])

    def LogNormal(self, x, par):
        '''
        https://root.cern.ch/root/html524/ROOT__Math.html#TopOfPage
        https://root.cern.ch/doc/v608/namespaceTMath.html#a0503deae555bc6c0766801e4642365d2

        Computes the density of LogNormal distribution at point x.
        Double_t TMath::LogNormal(Double_t x, Double_t sigma, Double_t theta = 0, Double_t m = 1)
        
        Variable X has lognormal distribution if Y=Ln(X) has normal distribution:
        sigma = shape parameter (and is the standard deviation of the log of the distribution)
        theta = location parameter, corresponds approximately to the most probable value. 
        m     = scale parameter (and is also the median of the distribution)
        '''
        return par[0]*ROOT.TMath.LogNormal(x[0], par[1], par[2], par[3])


    def LogNormalPDF(self, x, par):
        '''
        https://root.cern.ch/root/html524/ROOT__Math.html#TopOfPage
        https://root.cern.ch/doc/v608/group__PdfFunc.html#ga20ece8c1bb9f81af22ed65dba4a1b025

        Probability density function of the lognormal distribution.
        double ROOT::Math::lognormal_pdf(double x, double m, double s, double x0 = 0)
        For detailed description see http://mathworld.wolfram.com/LogNormalDistribution.html

        Parameters:
        m  = scale parameter (and is also the median of the distribution)
        s  = shape parameter (and is the standard deviation of the log of the distribution)
        x0 = location parameter, corresponds approximately to the most probable value. 
        For x0 = 0, sigma = 1, the x_mpv = -0.22278
        '''
        return par[0]*ROOT.Math.lognormal_pdf(x[0], par[1], par[2], par[3])
    
    def MyLogNormal(self, x, par):
        '''
        '''
        return ROOT.TMath.Exp(-(ROOT.TMath.Log(x/par[1]))**2/(2*ROOT.TMath.Log(par[2]))**2)/(ROOT.TMath.Sqrt(2*ROOT.TMath.Pi()*ROOT.TMath.Log(par[2])*x))

    def QCDFunction(self, x, par, boundary, norm):
        '''
        https://root.cern.ch/root/html524/ROOT__Math.html#TopOfPage
        
        x and par are standard root way to define the fit function
        from x only x[0] is used; it is the x-variable.        
        par contains the fitted parameters, you can give initial values, but the final ones come from the fitting.
        ''' 
#        if x[0] < boundary:
#            return self._additionalNormFactor*norm*par[0]*ROOT.TMath.Landau(x[0], par[1],par[2])
#        return self._additionalNormFactor*norm*par[3]*ROOT.TMath.Exp(-x[0]*par[4])
        #return self._additionalNormFactor*norm*par[0]*ROOT.TMath.LogNormal(x[0], par[1], par[2], par[3])
        #return self._additionalNormFactor*norm*par[0]*ROOT.Math.lognormal_pdf(x[0], par[1], par[2], par[3])
        #return self._additionalNormFactor*norm*self.LogNormal(x, par)
        #return self._additionalNormFactor*norm*self.LogNormalPDF(x, par) 
        #return self._additionalNormFactor*norm*(par[0]*ROOT.Math.lognormal_pdf(x[0], par[2], par[1]) + par[3]*ROOT.TMath.Exp(-x[0]*par[4]) + (1-par[0]-par[3])*ROOT.TMath.Gaus(x[0], par[5], par[6]))
        #return self._additionalNormFactor*norm*(par[0]*ROOT.TMath.LogNormal(x[0], par[1], par[2], par[3]) + par[4]*ROOT.TMath.Exp(-x[0]*par[5]) + (1-par[0]-par[4])*ROOT.TMath.Gaus(x[0], par[6], par[7]))

        #return self._additionalNormFactor*norm*(par[0]*ROOT.TMath.LogNormal(x[0], par[1], par[2], par[3]) + par[4]*ROOT.TMath.Exp(x[0]*par[5]) + (1-par[0]-par[4])*ROOT.TMath.Gaus(x[0], par[6], par[7]))
        return self._additionalNormFactor*norm*(par[0]*ROOT.TMath.LogNormal(x[0], par[1], 0, par[2]) + par[3]*ROOT.TMath.Exp(x[0]*par[4]) + (1-par[0]-par[3])*ROOT.TMath.Gaus(x[0], par[5], par[6]))
        #return self._additionalNormFactor*norm*(par[0]*ROOT.TMath.Exp(-(ROOT.TMath.Log(x[0]/par[1]))**2/(2*ROOT.TMath.Log(par[2]))**2)/(ROOT.TMath.Sqrt(2*ROOT.TMath.Pi()*ROOT.TMath.Log(par[2])*x[0])) + par[3]*ROOT.TMath.Exp(-x[0]*par[4]) + (1-par[0]-par[3])*ROOT.TMath.Gaus(x[0], par[5], par[6]))
    

    def EWKFunction(self,x, par, boundary, norm=1, rejectPoints=0):
        '''
        x and par are standard root way to define the fit function
        from x only x[0] is used; it is the x-variable.        
        par contains the fitted parameters, you can give initial values, but the final ones come from the fitting.
        
        Landau(x, mpv, widthParam), ROOT.TMath.Gaus(x[0], sigma, mean), ROOT.TMath.BreitWigner(x[0], decayWidth, mass)
        ''' 
        # return self._additionalNormFactor*norm*(self.CrystalBall(x, par))
        # return self._additionalNormFactor*norm*(par[0] * ROOT.TMath.Landau(x[0], par[1], par[2]) * ROOT.TMath.Gaus(x[0], par[1]) * ROOT.TMath.BreitWigner(x[0], par[2], par[1]))
        # return self._additionalNormFactor*norm*(par[0] * ROOT.TMath.Landau(x[0], par[1], par[2]) * ROOT.TMath.Gaus(x[0], par[3], par[1]) * ROOT.TMath.BreitWigner(x[0], par[4], par[1]))
        # if x[0] < boundary:
        #     return self._additionalNormFactor*norm*( par[0] * ROOT.TMath.BreitWigner(x[0], par[2], par[1]) * ROOT.Math.crystalball_function(x[0], par[3], par[4], par[2], par[1]) )
        # else:
        #     return par[6]*ROOT.TMath.Exp(-x[0]*par[5])
        #return self._additionalNormFactor*norm*(par[0]*ROOT.TMath.Landau(x[0],par[1], par[2]))*(par[3]*ROOT.TMath.BreitWigner(x[0], par[4], par[5]))*(par[6]*ROOT.Math.crystalball_function(x[0], par[7], par[8], par[9], par[10]) )
        #return self._additionalNormFactor*norm*( (par[0]*ROOT.TMath.Landau(x[0],par[1], par[2])) 
        #                                         + (par[3]*ROOT.TMath.BreitWigner(x[0], par[4], par[5])) 
        #                                         + (par[6]*ROOT.Math.crystalball_function(x[0], par[7], par[8], par[9], par[10]) ) 
        #                                         )
        #return self._additionalNormFactor*norm*( (par[0]*ROOT.TMath.Landau(x[0],par[1], par[2])) 
        #                                         + (par[3]*ROOT.TMath.BreitWigner(x[0], par[4], par[5])) 
        #                                         + (par[6]*ROOT.Math.crystalball_function(x[0], par[7], par[8], par[9], par[10]) ) 
        #                                         )

        #return self._additionalNormFactor*norm*par[0]*(ROOT.Math.crystalball_function(x[0], par[3], par[4], par[2], par[1]) 
        #                                               + ROOT.TMath.BreitWigner(x[0], par[2], par[1])
        #                                               + ROOT.TMath.Landau(x[0], par[1], par[2]) )

        # Best so far:
        return self._additionalNormFactor*norm*(par[0]*ROOT.Math.crystalball_function(x[0], par[1], par[2], par[3], par[4])
                                                       + par[5]*ROOT.TMath.BreitWigner(x[0], par[6], par[7])
                                                       + (1-par[0]-par[5])*ROOT.TMath.Landau(x[0], par[8], par[9]) )

        #return self._additionalNormFactor*norm*(par[0]*ROOT.Math.crystalball_function(x[0], par[1], par[2], par[3], par[4])*par[5]*ROOT.TMath.BreitWigner(x[0], par[6], par[7])
        #                                               + (1-par[0]-par[5])*ROOT.TMath.Landau(x[0], par[8], par[9]) )                                                      


    def EWKFunctionInv(self,x, par, boundary, norm=1, rejectPoints=0):
        if x[0] < boundary:
            return self._additionalNormFactor*norm*(par[0]*ROOT.TMath.Landau(x[0],par[1],par[2]))
        C = self._additionalNormFactor*norm*(par[0]*ROOT.TMath.Landau(boundary,par[1],par[2]))*ROOT.TMath.Exp(boundary*par[3])
        return C*ROOT.TMath.Exp(-x[0]*par[3])


    def QCDEWKFunction(self,x,par,norm):
        if par[0]+par[1]*x[0] == 0.0:
            return 0
        return self._additionalNormFactor*norm*(par[1]*x[0]/((par[0])*(par[0]))*ROOT.TMath.Exp(-x[0]*x[0]/(2*(par[0])*(par[0])))+par[2]*ROOT.TMath.Gaus(x[0],par[3],par[4],1)+par[5]*ROOT.TMath.Exp(-par[6]*x[0]))

    def QCDFunctionFixed(self,x,par):
        return self._additionalNormFactor*par[0]*(ROOT.TMath.Gaus(x[0],par[1],par[2],1)+par[3]*ROOT.TMath.Gaus(x[0],par[4],par[5],1)+par[6]*ROOT.TMath.Exp(-par[7]*x[0]))
    
    #===== Composite functions for fitting data
    ## QCD, fake taus, and genuine b as separate templates
    def FitDataWithQCDAndFakesAndGenuineTaus(self, x, par,
                                             QCDFitFunction, parQCD, QCDnorm,
                                             EWKFakeTausFitFunction, parEWKFakeTaus, EWKFakeTausNorm,
                                             EWKGenuineTausFitFunction, parEWKGenuineTaus, EWKGenuineTausNorm):
        nQCD = QCDFitFunction(x, parQCD, norm=QCDnorm)
        nEWKFakeTaus = EWKFakeTausFitFunction(x, parEWKFakeTaus, norm=EWKFakeTausNorm)
        nEWKGenuineTaus = EWKGenuineTausFitFunction(x, parEWKGenuineTaus, norm=EWKGenuineTausNorm) 
        return par[0]*(par[1]*nQCD + par[2]*nEWKFakeTaus + (1.0 - par[1] - par[2])*nEWKGenuineTaus)

    def FitDataWithQCDAndInclusiveEWK(self, x, par, QCDFitFunction, parQCD, QCDnorm, EWKInclusiveFunction, parEWK, EWKNorm):
        '''
        QCD and inclusive EWK as separate templates
        '''
        nQCD = QCDFitFunction(x, parQCD, norm=QCDnorm)
        nEWK = EWKInclusiveFunction(x, parEWK, norm=EWKNorm)
        return par[0]*(par[1]*nQCD + (1.0 - par[1])*nEWK)

    ## QCD and fake tau templates as one inclusive template
    def FitDataWithFakesAndGenuineTaus(self, x, par,
            QCDAndFakesFitFunction, parQCDAndFakes, QCDAndFakesnorm,
            EWKGenuineTausFitFunction, parEWKGenuineTaus, EWKGenuineTausNorm):
        nQCDAndFakes =    QCDAndFakesFitFunction(x, parQCDAndFakes, norm=QCDAndFakesnorm)
        nEWKGenuineTaus = EWKGenuineTausFitFunction(x, parEWKGenuineTaus, norm=EWKGenuineTausNorm) 
        return par[0]*(par[1]*nQCDAndFakes + (1.0 - par[1])*nEWKGenuineTaus)


def getModifiedBinLabelString(binLabel):
    '''
    Modify bin label string
    '''
    label = binLabel
    label = label.replace("#tau p_{T}","taupT")
    label = label.replace("#tau eta","taueta")
    label = label.replace("<","lt")
    label = label.replace(">","gt")
    label = label.replace("=","eq")
    label = label.replace("..","to")
    label = label.replace(".","p")
    label = label.replace("/","_")
    label = label.replace(" ","_")
    return label

def getFormattedBinLabelString(binLabel):
    '''
    Inverse bin label modification
    '''
    label = binLabel
    label = label.replace("taupT","tau p_{T}")
    label = label.replace("tauPt","tau p_{T}")
    label = label.replace("taueta","tau {#eta}")
    label = label.replace("lt"," < ")
    label = label.replace("gt"," > ")
    label = label.replace("eq"," = ",)
    label = label.replace("to","..")
    if label[-1].isdigit():
        label+=" GeV"
    return label

def getFormattedTemplateName(name):
    '''
    Helper function to plot template names in a more understandable wa
    '''
    formattedNames = {'EWKFakeTaus_Baseline'   : '#splitline{EWK+t#bar{t} fake b-jets}{Baseline}', 
                      'EWKGenuineTaus_Baseline': '#splitline{EWK+t#bar{t} genuine b-jets}{Baseline}', 
                      'EWKFakeTaus_Inverted'   : '#splitline{EWK+t#bar{t} fake b-jets}{Inverted}',
                      'EWKGenuineTaus_Inverted': '#splitline{EWK+t#bar{t} genuine b-jets}{Inverted}',
                      'EWKInclusive_Baseline'  : '#splitline{EWK+t#bar{t}}{Baseline}',
                      'EWKInclusive_Inverted'  : '#splitline{EWK+t#bar{t}}{Inverted}',
                      'QCD_Baseline'           : '#splitline{Fake b}{Baseline}',
                      'QCD_Inverted'           : '#splitline{Fake b}{Inverted}',
                      'data'                   : '#splitline{Data}{Baseline}'}
    if name in formattedNames.keys():
        return formattedNames[name]
    else:
        return name

#================================================================================================ 
# Class Definitions
#================================================================================================ 
class QCDNormalizationTemplate:
    '''
    Template holder for QCD measurement normalization
    '''
    def __init__(self, name, plotDirName, quietMode=True):
        self._verbose     = False
        self._name        = name
        self._plotDirName = plotDirName
        self._fitFunction = None
        self._fitKwargs   = None
        self._fitRangeMin = None
        self._fitRangeMax = None
        self._quietMode   = quietMode
        self._fitParamInitialValues = {}
        self._fitParamLowerLimits   = {}
        self._fitParamUpperLimits   = {}
        self.reset()
        self.Verbose("__init__()")
        return

    def Print(self, msg, printHeader=True):
        fName = __file__.split("/")[-1]
        if printHeader==True:
            print "=== ", fName + ": class " + self.__class__.__name__
            print "\t", msg
        else:
            print "\t", msg
            return
        
    def Verbose(self, msg, printHeader=True, verbose=False):
        if not self._verbose:
            return
        self.Print(msg, printHeader)
        return
        
    def getName(self):
        return self._name

    def setFitter(self, fitFunction, fitRangeMin, fitRangeMax):
        '''
        Set fit function and fit range
        '''
        self.Verbose("setFitter()")
        self._fitFunction = fitFunction
        self._fitRangeMin = fitRangeMin
        self._fitRangeMax = fitRangeMax
        if not isinstance(fitFunction, FitFunction):
            raise Exception("Error: the fit function needs to be a FitFunction class!")
        if fitRangeMax < fitRangeMin:
            raise Exception("Error: fit range max value is smaller than the min value!")
        return

    def reset(self):
        '''
        Call before setting the histogram and fitting
        '''
        self.Verbose("reset()")
        self._binLabel = None
        self._nEventsFromFit = None
        self._nEventsTotalErrorFromFitUp = None
        self._nEventsTotalErrorFromFitDown = None
        self._histo = None
        self._normalizationFactor = None
        self._fitParameters = None
        self._fitParErrors = None
        return

    def hasHisto(self):
        '''
        Returns true if a histogram has been provided
        '''
        return self._histo != None
    
    def getBinLabel(self):
        '''
        Returns the bin label
        '''
        return self._binLabel

    def getNormalizationFactor(self):
        '''
        Returns the normalization factor for normalizing the histogram contents to Nevents (histogram is stored with area = 1)
        '''
        return self._normalizationFactor
    
    def isFittable(self):
        '''
        Returns true if a fit function has been provided
        '''
        return self._fitFunction != None

    def getFitFunction(self):
        '''
        Returns the fit function object
        '''
        return self._fitFunction
    
    def getFittedParameters(self):
        '''
        Returns the list of parameters from the fit (returns None if not fitted)
        '''
        return self._fitParameters

    def getFittedParameterErrors(self):
        '''
        Returns the list of parameter errors from the fit (returns None if not fitted)
        '''
        return self._fitParErrors


    def printFitParamSettings(self):
        '''
        Prints the parameter settings (for debugging or info)
        '''
        self.Verbose("printFitParamSettings()")

        keys = self._fitParamInitialValues.keys()    
        for k in self._fitParamLowerLimits.keys():
            if not k in keys:
                keys.append(k)
        keys.sort()

        if self._binLabel != None:
            keys = [self._binLabel]
        else:
            print ""

        # Construct the info table
        rows     = []
        txtAlign = "{:^5} {:^12} {:>12} {:>12}"
        header   = txtAlign.format("Par", "Initial", "Low Bound", "High Bound")
        hLine    = "="*50
        rows.append(hLine)
        rows.append(header)
        rows.append(hLine)

        # Fill the table columns (lists)
        for k in keys:

            if k in self._fitParamInitialValues.keys():
                col1 = self._fitParamInitialValues[k]
            elif "default" in self._fitParamInitialValues.keys():
                col1 = self._fitParamInitialValues["default"]
            else:
                col1 = []

            # Lower/Upper limit
            if k in self._fitParamLowerLimits.keys():
                col2 = self._fitParamLowerLimits[k]
                col3 = self._fitParamUpperLimits[k]
            elif "default" in self._fitParamLowerLimits.keys():
                col2 = self._fitParamLowerLimits["default"]
                col3 = self._fitParamUpperLimits["default"]
            else:
                col2 = []
                col3 = []

        # Sanity checks (size of lists)
        if len(col1) == 0:
            if len(col2)>0:
                size = len(col2)
            elif len(col3)>0:
                size = len(col3)
            else:
                size = 0 
            col1 = ["None"]*size

        if len(col2) == 0:
            if len(col1)>0:
                size = len(col1)
            elif len(col3)>0:
                size = len(col3)
            else:
                size = 0
            col2 = ["None"]*size

        if len(col3) == 0:
            if len(col1)>0:
                size = len(col1)
            elif len(col2)>0:
                size = len(col2)
            else:
                size = 0
            col3 = ["None"]*size
            

        # Fill all the rows with all the column info
        counter = 0        
        for c1, c2, c3 in zip(col1, col2, col3):
            rows.append(txtAlign.format(counter, c1, c2, c3))
            counter += 1
        rows.append("")

        # Print the table
        self.Print("Fit parameter settings for \"%s\" (binLabel=\"%s\")" % (self._name, self._binLabel)  )
        for index, r in enumerate(rows):
            self.Print(r, False)
        if self._binLabel == None:
            print ""
        return

    def printResults(self):
        '''
        Prints the results
        '''
        print "\nResults for '%s', bin '%s':"%(self._name, self._binLabel)
        if self._histo == None:
            print "  (no histogram has been given -> no results)"
        else:
            print "  Nevents from histogram (visible part only): %f +- %f"%(self.getNeventsFromHisto(False), self.getNeventsErrorFromHisto(False))
            print "  Nevents from histogram (with under/overflow): %f +- %f"%(self.getNeventsFromHisto(True), self.getNeventsErrorFromHisto(True))
            if self._fitParameters == None:
                print "  (no fit done)"
            else:
                print "  Nevents from fit: %f + %f - %f"%(self._nEventsFromFit, self._nEventsErrorFromFit[0], self._nEventsErrorFromFit[1])
        print ""
        return

    def getNeventsFromHisto(self, includeOverflowBins):
        '''
        Returns the number of events obtained from the histogram
         \param includeOverflowBins  if true, then range includes the under/overflow bins
        '''
        if self._histo == None:
            raise Exception("Error: Please call the the 'setHistogram(...)' method first!")
        if includeOverflowBins:
            return self._histo.Integral(0, self._histo.GetNbinsX()+2)*self._normalizationFactor
        else:
            return self._histo.Integral(1, self._histo.GetNbinsX()+1)*self._normalizationFactor
        return

    def getNeventsErrorFromHisto(self, includeOverflowBins):
        '''
        Returns the absolute uncertainty in the number of events obtained from the histogram
         \param includeOverflowBins  if true, then range includes the under/overflow bins
        '''
        if self._histo == None:
            raise Exception("Error: Please call the the 'setHistogram(...)' method first!")
        integralError = ROOT.Double(0.0)
        if includeOverflowBins:
            a = self._histo.IntegralAndError(0, self._histo.GetNbinsX()+2, integralError)
        else:
            a = self._histo.IntegralAndError(1, self._histo.GetNbinsX()+1, integralError)
        return float(integralError*ROOT.TMath.Sqrt(self._normalizationFactor))
    
    def getNeventsFromFit(self):
        '''
         Returns the number of events obtained from the fit
         The range is the range of the histogram; under/overflow bins are ignored!
         '''
        if self._fitParameters == None:
            if self._fitFunction == None:
                raise Exception("Error: Please call the the 'setFitter(...)' method first!")
            else:
                raise Exception("Error: Please call the 'doFit(...)' method first!")
        return self._nEventsFromFit
    
    def getNeventsTotalErrorFromFit(self):
        '''
        Returns the [plus, minus] absolute uncertainty in number of events obtained from the fit
        The range is the range of the histogram; under/overflow bins are ignored!
        '''
        if self._fitParameters == None:
            if self._fitFunction == None:
                raise Exception("Error: Please call the the 'setFitter(...)' method first!")
            else:
                raise Exception("Error: Please call the 'doFit(...)' method first!")
        return [self._nEventsTotalErrorFromFitUp, self._nEventsTotalErrorFromFitDown]

    def getFitResults(self):
        '''
        Returns the fit results
        '''
        return self._fitParameters
    
    def obtainFittedFunction(self, normalizationFactor, FITMIN, FITMAX):
        '''
        Returns a TF1 of the fitted function
        '''
        if self._fitParameters == None:
            raise Exception("Error: Call doFit() first!")
        # Update normalization
        f = self._fitFunction.clone()
        f.setAdditionalNormalization(normalizationFactor)
        # Obtain function  
        func = ROOT.TF1(self._name+"_"+self._binLabel, f, FITMIN, FITMAX, self._fitFunction.getNParam())
        for k in range(self._fitFunction.getNParam()):
            func.SetParameter(k, self._fitParameters[k])
        func.SetLineWidth(2)
        func.SetLineStyle(2)
        return func
    
    def setHistogram(self, histogram, binLabel):
        '''
        Call once for every bin
        '''
        self.Verbose("setHistogram()")

        self._histo    = histogram
        self._binLabel = binLabel

        # Convert negative bins to zero but leave errors intact
        header = True
        for k in range(0, self._histo.GetNbinsX()+2):
            if self._histo.GetBinContent(k) < 0.0:
                self.Verbose("Template '%s': converted in bin %d a negative value (%f) to zero."%(self._name, k, self._histo.GetBinContent(k)), header)
                self._histo.SetBinContent(k, 0.0)
                self._histo.SetBinError(k, 1.0)
                header = False
            else:
                pass

        # Format bin label string
        self._binLabel = getModifiedBinLabelString(binLabel)

        # Calculate normalization factor and store the histogram normalized as area = 1
        integral = self._histo.Integral()
        if integral == 0.0:
            self._normalizationFactor = 1.0
        else:
            self._normalizationFactor = integral
            self._histo.Scale(1.0 / self._normalizationFactor)
        return

    def plot(self):
        '''
        Make a plot of the MET histogram
        '''
        if self._histo == None:
            raise Exception("Error: Please provide first the histogram with the 'setHistogram' method")
        if self._histo.GetEntries() == 0:
            print "Skipping plot for '%s' because it has zero entries."%self._name
            return
        xTitle = "m_{jjb} (GeV/c^{2})"
        yTitle = "Events / bin"
        plot = plots.PlotBase()
        h = self._histo.Clone(self._histo.GetName()+"clone")
        h.Scale(self._normalizationFactor)
        plot.histoMgr.appendHisto(histograms.Histo(h,self._histo.GetName()))
        plot.createFrame(self._plotDirName+"/template_"+self._name.replace(" ","_")+"_"+self._binLabel, opts={"ymin": 0.1, "ymaxfactor": 4.})
        plot.getFrame().GetXaxis().SetTitle(xTitle)
        plot.getFrame().GetYaxis().SetTitle(yTitle)
        plot.getPad().SetLogy(True)
        st = styles.getDataStyle().clone()
        st.append(styles.StyleFill(fillColor=ROOT.kYellow))
        histograms.addStandardTexts(cmsTextPosition="outframe")
        histograms.addText(0.48,0.85, getFormattedTemplateName(self._name))
        histograms.addText(0.48,0.77, getFormattedBinLabelString(self._binLabel))
        histograms.addText(0.48,0.72, "N_{events} = %d"%int(self._histo.Integral(0,-1)*self._normalizationFactor+0.5)) # round to closes integer
        plot.histoMgr.forHisto(self._histo.GetName(), st)
        #plot.setFileName("template_"+self._name.replace(" ","_")+"_"+self._binLabel)
        plot.draw()
        plot.save()
        #st.append(styles.StyleFill(fillColor=0))
        #plot.histoMgr.forHisto(objectName, st)
        return

    def setDefaultFitParam(self, defaultInitialValue=None, defaultLowerLimit=None, defaultUpperLimit=None):
        '''
        Sets the default fit parameters
        '''
        self.Verbose("setDefaultFitParam()")

        if defaultInitialValue != None:
            if not isinstance(defaultInitialValue, list):
                raise Exception("Error: Please provide a list for setting the fit parameter initial value!")
            self._fitParamInitialValues["default"] = defaultInitialValue
            
        if (defaultLowerLimit == None and defaultUpperLimit != None) or (defaultLowerLimit != None and defaultUpperLimit == None):
            raise Exception("Error: if you wish to set parameter limits, please provide both the lower and upper limit.")
        if defaultLowerLimit != None and defaultUpperLimit != None:
            if not isinstance(defaultLowerLimit, list) and not isinstance(defaultUpperLimit, list):
                raise Exception("Error: Please provide lists for setting the fit parameter ranges!")
            if (len(defaultLowerLimit) != len(defaultUpperLimit)):
                raise Exception("Error: Please provide lists of same length for the fit parameter ranges!")
            self._fitParamLowerLimits["default"] = defaultLowerLimit
            self._fitParamUpperLimits["default"] = defaultUpperLimit
        return


    def setFitParamForBin(self, binLabel, initialValue=None, lowerLimit=None, upperLimit=None):
        '''
        Sets the fit parameters for a specific bin
        '''
        modifiedBinLabel = getModifiedBinLabelString(binLabel)
        if initialValue != None:
            if not isinstance(initialValue, list):
                raise Exception("Error: Please provide a list for setting the fit parameter initial value!")
            self._fitParamInitialValues[modifiedBinLabel] = initialValue
        if (lowerLimit == None and upperLimit != None) or (lowerLimit != None and upperLimit == None):
            raise Exception("Error: if you wish to set parameter limits, please provide both the lower and upper limit.")
        if lowerLimit != None and upperLimit != None:
            if not isinstance(lowerLimit, list) and not isinstance(upperLimit, list):
                raise Exception("Error: Please provide lists for setting the fit parameter ranges!")
            if (len(lowerLimit) != len(upperLimit)):
                raise Exception("Error: Please provide lists of same length for the fit parameter ranges!")
            self._fitParamLowerLimits[modifiedBinLabel] = lowerLimit
            self._fitParamUpperLimits[modifiedBinLabel] = upperLimit
        return
            
    def CreateTF1(self, prefix):
        self.Verbose("CreateTF1()")

        # Construct the info table
        fName  = prefix + self._name + self._binLabel
        rows   = []
        align  = "{:^34} {:^6} {:^30} {:^15} {:^15}"
        header = align.format("Fit Function", "Params", "Fit Function Name", "Fit Min", "Fit Max")
        hLine  = "="*100
        rows.append(hLine)
        rows.append(header)
        rows.append(hLine)
        rows.append( align.format(self._fitFunction.getName(), self._fitFunction.getNParam(), fName, self._fitRangeMin, self._fitRangeMax))
        rows.append("")

        # Print information
        if self._verbose:
            for r in rows:
                self.Print(r, False)

        # Create the function
        tf1 = ROOT.TF1(fName, self._fitFunction, self._fitRangeMin, self._fitRangeMax, self._fitFunction.getNParam())
        return tf1

    def PrintFitResults(self, r):
        '''
        Print information contained in the TFitResultPtr r
        
        See:
        https://root.cern.ch/doc/v608/classROOT_1_1Fit_1_1FitResult.html#ac96273476383baba62ca1585b6bd4fda
        https://root.cern.ch/doc/v608/classTFitResult.html
        '''
        self.Verbose("PrintFitResults()")
        
        # Sanity check
        if r.IsEmpty():
            raise Exception("Error: The TFitResultPtr is empty!")

        # Print full information of fit including covariance matrix and correlation
        if 0:
            r.Print("V")

        # Define the table format
        lines  = [] 
        align  = "{:<15} {:>15} {:>15} {:^15} {:<60}"
        header = align.format("Variable", "Value", "Error", "Error (%)", "Description")
        hLine  = "="*120
        lines.append(hLine)
        lines.append(header)
        lines.append(hLine)

        # Get the information
        chi2       = r.Chi2()
        dof        = r.Ndf()
        redChi2    = r.Chi2()/dof
        edm        = r.Edm()
        nCalls     = r.NCalls()
        status     = r.Status() # See: https://root.cern.ch/root/html/ROOT__Minuit2__Minuit2Minimizer.html#ROOT__Minuit2__Minuit2Minimizer:Minimize
        fParams    = r.NFreeParameters()
        covMStatus = r.CovMatrixStatus()
        isValid    = r.IsValid()
        if isValid:
            result = "TRUE"
        else:
            result = "FALSE"
        nHisto     = self.getNeventsFromHisto(False)
        nHistoUp   = self.getNeventsErrorFromHisto(False)
        nHistoDown = self.getNeventsErrorFromHisto(False)
        nFit       = self.getNeventsFromFit()
        nFitUp     = self.getNeventsTotalErrorFromFit()[0]
        nFitDown   = self.getNeventsTotalErrorFromFit()[1]
        nDiff      = nHisto-nFit
        nDiffUp    = errorPropagation.errorPropagationForSum(nHisto, nHistoUp  , nFit, nFitUp)
        nDiffDown  = errorPropagation.errorPropagationForSum(nHisto, nHistoDown, nFit, nFitDown)
        if nFit>0:
            nRatio     = self.getNeventsFromHisto(False) / self.getNeventsFromFit()
            nRatioUp   = errorPropagation.errorPropagationForDivision(nHisto, nHistoUp  , nFit, nFitUp)
            nRatioDown = errorPropagation.errorPropagationForDivision(nHisto, nHistoDown, nFit, nFitDown)
        else:
            self.Verbose("Cannot divide by zero for item \"%s\%. Setting ratio to zero" % (key), True)
            nRatio      = 0
            nRatioUp    = 0
            nRatioDown  = 0

        # Construct the table
        lines.append( align.format("Chi2"       , "%0.1f" % chi2      , "", "", "Fit value") )
        lines.append( align.format("D.O.F"      , "%0.0f" % dof       , "", "", "Number of degrees of freedom") )
        lines.append( align.format("Chi2/d.o.f" , "%0.1f" % redChi2   , "", "", "Reduced chi2 (=1 for good fits)") )
        lines.append( align.format("E.D.M"      , "%0.7f" % edm       , "", "", "Expected distance from minimum") )
        lines.append( align.format("# Calls"    , "%0.0f" % nCalls    , "", "", "Number of function calls to find minimum") )
        lines.append( align.format("Free Params", "%0.0f" % fParams   , "", "", "Total number of free parameters") )
        lines.append( align.format("Status"     , "%0.0f" % status    , "", "", "Minimizer status code") )
        lines.append( align.format("Cov Matrix" , "%0.0f" % covMStatus, "", "", "0=not calculated, 1=approx, 2=made pos def, 3=accurate") )
        lines.append( align.format("IsValid"    , "%s"    % (result)  , "", "", "True=Fit successful, False=Fit unsuccessful") )
        lines.append( align.format("Fit Range"  , "%s-%s" % (self._fitRangeMin, self._fitRangeMax), "", "", "Lower/Upper bounds to fit the function") )
        #lines.append("")

        # For-loop: All parameters
        for i, p in enumerate(r.Parameters()):
            pName   = r.GetParameterName(i)
            pValue  = "%0.5f" % p
            pError  = "%0.5f" % r.Error(i)
            pErrorP = 0
            if p != 0:
                pErrorP = "%.2f" % ((r.Error(i)/p)*100)
            isBound = r.IsParameterBound(i)
            isFixed = r.IsParameterFixed(i)
            lines.append( align.format(pName, pValue, pError, pErrorP, "isBound = %s, isFixed = %s" %  (isBound, isFixed) ) )
        #lines.append("")

        # Events Info
        nHistoUpP = 0
        if nHisto > 0:
            nHistoUpP = (nHistoUp/nHisto)*100
        nFitUpP = 0
        if nFit > 0:
            nFitUpP = (nFitUp/nFit)*100
        nDiffUpP = 0
        if nDiff > 0:
            nDiffUpP = (nDiffUp/nDiff)*100
        nRatioUpP = 0
        if nRatio > 0:
            nRatioUpP = (nRatioUp/nRatio)*100
        lines.append(align.format("Events (Histo)", "%.3f" % nHisto,  "%.3f" % nHistoUp, "%.2f" % nHistoUpP, "Absolute uncertainty quoted (up=down)") )
        lines.append(align.format("Events (Fit)"  , "%.3f" % nFit  ,  "%.3f" % nFitUp  , "%.2f" % nFitUpP  , "Total fit parameter uncertainty (up)") )
        lines.append(align.format("Events (Diff)" , "%.3f" % nDiff ,  "%.3f" % nDiffUp , "%.2f" % nDiffUpP , "Error-propagation (up)") )
        lines.append(align.format("Events (Ratio)", "%.3f" % nRatio,  "%.3f" % nRatioUp, "%.2f" % nRatioUp , "Error-propagation (up)") )
        lines.append(hLine)
        lines.append("")
        for l in lines:
            self.Print(l, False)

        # Sanity check
        if not isValid:
            raise Exception("Error: The TFitResultPtr is not valid! The fit failed...")

        return

    def doFit(self, fitOptions="S", createPlot=True):
        self.Verbose("doFit()")
        
        if self._histo == None:
            raise Exception("Error: Please provide first the histogram with the 'setHistogram' method")
        if self._histo.Integral(1, self._histo.GetNbinsX()+1) == 0.0:
            raise Exception("Error: The histogram '%s' integral is zero! (perhaps there is a bug somewhere or you run out of events)"%self._name)
        if self._fitFunction == None:
            return
        else:
            #if not self._quietMode:
            if self._verbose:
                self.printFitParamSettings()

            # Define fit object
            fit = self.CreateTF1(prefix="fit")

            # Set initial fit parameter values
            centralKey = None
            if self._binLabel in self._fitParamInitialValues.keys():
                centralKey = self._binLabel
            if "default" in self._fitParamInitialValues.keys():
                centralKey = "default"
            if centralKey != None:
                for i in range(len(self._fitParamInitialValues[centralKey])):
                    fit.SetParameter(i, self._fitParamInitialValues[centralKey][i])

            # Set fit parameter ranges
            key = None
            if self._binLabel in self._fitParamLowerLimits.keys():
                key = self._binLabel
            if "default" in self._fitParamLowerLimits.keys():
                key = "default"
            if key != None:
                for i in range(len(self._fitParamLowerLimits[key])):
                    fit.SetParLimits(i, self._fitParamLowerLimits[key][i], self._fitParamUpperLimits[key][i])
                    # Make sure that central value is inside the limits
                    if centralKey == None:
                        fit.SetParameter(i, (self._fitParamLowerLimits[key][i] + self._fitParamUpperLimits[key][i]) / 2.0)

            self.Verbose("Clone the histogram and normalize its area to unity (note also the under/overflow bins)")
            h = aux.Clone(self._histo)

            # Do the fit
            if not self._quietMode:
                self.Verbose("Using fit options: %s" % (fitOptions))
            elif not "Q" in fitOptions:
                fitOptions += " Q" # To suppress output
            if not "S" in fitOptions:
                fitOptions += " S" # To return fit results

            self.Verbose("Create explicitly canvas to get rid of warning message")
            canvas = ROOT.TCanvas()

            self.Verbose("Fitting function \"%s\" to histogram \"%s\" with fitOptions \"%s\"" % (fit.GetName(), h.GetName(), fitOptions) )
            print 
            fitResultObject = h.Fit(fit, fitOptions)
            if self._verbose:
                fitResultObject.Print("V")
            
            self.Verbose("Storing fit parameters and their associated errors")
            self._fitParameters = fit.GetParameters()
            self._fitParErrors  = fit.GetParErrors()
            
            self.Verbose("Need to divide the TF1 integral by histogram bin width")
            self._nEventsFromFit = fit.Integral(self._histo.GetXaxis().GetXmin(), self._histo.GetXaxis().GetXmax())*self._normalizationFactor / self._histo.GetXaxis().GetBinWidth(1)

            self.Verbose("Diagonalise the error matrix of the fit parameters and then vary in this orthogonal base the fit parameters up and down by one standard deviation.")
            orthogonalizer = fitHelper.FitParameterOrthogonalizer(fit, fitResultObject, self._histo.GetXaxis().GetXmin(), self._histo.GetXaxis().GetXmax())
            self._nEventsTotalErrorFromFitUp   = orthogonalizer.getTotalFitParameterUncertaintyUp()
            self._nEventsTotalErrorFromFitDown = orthogonalizer.getTotalFitParameterUncertaintyDown()

            self.Print("Results of fitting function \"%s\" to histogram \"%s\" (binLabel=\"%s\")" % (self._fitFunction.getName(), self._histo.GetName(), self._binLabel), True) #self._name
            self.PrintFitResults(fitResultObject)
                    
            # Do a plot of the fit
            if createPlot:
                xTitle = "m_{jjb} (GeV/c^{2})"
                yTitle = "Events (normalized to unity)"
                yLog   = False #alex
                if yLog:
                    yMaxFactor = 4
                else:
                    yMaxFactor = 1.1

                ROOT.gStyle.SetOptFit(0)
                ROOT.gStyle.SetOptStat(0)
                h.SetLineColor(ROOT.kBlack)

                # fit QCD plots with blue, EWK+ttbar with green, everything else with red
                if "EWK" in h.GetName():
                    fit.SetLineColor(ROOT.kGreen+2)
                elif "QCD" in h.GetName():
                    fit.SetLineColor(ROOT.kBlue)
                else:
                    fit.SetLineColor(ROOT.kRed)
                fit.SetLineWidth(2)
                fit.SetLineStyle(2)
                plot = plots.PlotBase()
                plot.histoMgr.appendHisto(histograms.Histo(h,h.GetName()))
                h.SaveAs(self._plotDirName + "/" + h.GetName() + ".root")

                plot.histoMgr.appendHisto(histograms.Histo(fit, "fit"))
                plot.createFrame(self._plotDirName+"/fit_"+self._name.replace(" ","_")+"_"+self._binLabel, opts={"ymin": 1e-5, "ymaxfactor": yMaxFactor})
                plot.getFrame().GetXaxis().SetTitle(xTitle)
                plot.getFrame().GetYaxis().SetTitle(yTitle)
                histograms.addText(0.65, 0.85, getFormattedTemplateName(self._name))
                histograms.addText(0.65 ,0.77, getFormattedBinLabelString(self._binLabel))
                plot.getPad().SetLogy(yLog)
                histograms.addStandardTexts(cmsTextPosition="outframe")
                plot.draw()
                plot.save()
        return


#================================================================================================ 
# Class Definitions
#================================================================================================ 
class QCDNormalizationManagerBase:
    '''
    Base class for QCD measurement normalization from which specialized algorithm classes inherit
    '''
    def __init__(self, binLabels, resultDirName, moduleInfoString):
        self._verbose   = False
        self._templates = {}
        self._binLabels = binLabels
        myPath          = "%s/normalisationPlots" % resultDirName

        # No optimisation mode
        if moduleInfoString == "":
            moduleInfoString = "Default" 
        
        if not os.path.exists(myPath):
            self.Print("Creating directory %s" % (myPath), True )
            os.mkdir(myPath)
        self._plotDirName = "%s/normalisationPlots/%s" % (resultDirName, moduleInfoString)

        # If already exists, Delete an entire directory tree
        if os.path.exists(self._plotDirName):
            self.Print("Removing  directory tree %s" % (self._plotDirName), True )
            shutil.rmtree(self._plotDirName)
        os.mkdir(self._plotDirName)
        self._requiredTemplateList = []
        self._sources = {}
        self._commentLines = []
        self._qcdNormalization = {}
        self._qcdNormalizationError = {}
        self._ewkFakesNormalization = {}
        self._ewkFakesNormalizationError = {}
        self._combinedFakesNormalization = {}
        self._combinedFakesNormalizationError = {}
        self._combinedFakesNormalizationUp = {}
        self._combinedFakesNormalizationDown = {}
        self._dqmKeys = OrderedDict()
        if not isinstance(binLabels, list):
            raise Exception("Error: binLabels needs to be a list of strings")
        self.Verbose("__init__")
        return

    def Print(self, msg, printHeader=False):
        fName = __file__.split("/")[-1]
        if printHeader==True:
            print "=== ", fName + ": class " + self.__class__.__name__
            print "\t", msg
        else:
            print "\t", msg
            return
        
    def Verbose(self, msg, printHeader=True, verbose=False):
        if not self._verbose:
            return
        self.Print(msg, printHeader)
        return
  
    ## Creates a QCDNormalizationTemplate and returns it
    def createTemplate(self, name):
        if name in self._templates.keys():
            raise Exception("Error: A template with name '%s' has already been created!"%name)
        q = QCDNormalizationTemplate(name, self._plotDirName)
        self._templates[name] = q
        return q
   
    def plotTemplates(self):
        '''
        Plots shapes of templates
        '''
        self.Verbose("plotTemplates()")
        for index, k in enumerate(self._templates.keys()):
            if self._templates[k].hasHisto():
                self.Verbose("Plotting template %s" % (k), index==0)
        return

    ## Resets bin results
    def resetBinResults(self):
        for k in self._templates.keys():
            self._templates[k].reset()

    ## Virtual method for calculating the individual norm. coefficients
    def calculateNormalizationCoefficients(self, dataHisto, fitOptions, FITMIN, FITMAX, **kwargs):
        print "calculateQCDNormalization needs to be implemented in parent class"
    
    ## Calculates the combined normalization and if specified, varies it up or down by factor (1+variation)
    def calculateCombinedNormalizationCoefficient(self, hQCD, hEWKfakes):
        # Default method 
        lines = []
        # Obtain counts for QCD and EWK fakes
        nQCDerror = ROOT.Double(0.0)
        nQCD = hQCD.IntegralAndError(1, hQCD.GetNbinsX()+1, nQCDerror)
        nEWKfakesError = ROOT.Double(0.0)
        nEWKfakes = hEWKfakes.IntegralAndError(1, hEWKfakes.GetNbinsX()+1, nEWKfakesError)
        nTotal = nQCD + nEWKfakes
        nTotalError = ROOT.TMath.Sqrt(nQCDerror**2 + nEWKfakesError**2)
        # Calculate w = nQCD / nTotal
        w = None
        wUp = None
        wDown = None
        wError = None
        if nTotal > 0.0:
            w = nQCD / nTotal
            wError = errorPropagation.errorPropagationForDivision(nQCD, nQCDerror, nTotal, nTotalError)
            wUp = w + wError
            if wUp > 1.0:
                wUp = 1.0
            wDown = w - wError
            if wDown < 0.0:
                wDown = 0.0
        lines.append("   w = nQCD/(nQCD+nEWKfakes) = %f +- %f"%(w, wError))
        # Calculate the combined normalization factor (f_fakes = w*f_QCD + (1-w)*f_EWKfakes)
        binLabel = self._templates[self._requiredTemplateList[0]].getBinLabel()
        fakeRate = None
        fakeRateError = None
        fakeRateUp = None
        fakeRateDown = None
        if w != None:
            fakeRate = w*self._qcdNormalization[binLabel] + (1.0-w)*self._ewkFakesNormalization[binLabel]
            fakeRateUp = wUp*self._qcdNormalization[binLabel] + (1.0-wUp)*self._ewkFakesNormalization[binLabel]
            fakeRateDown = wDown*self._qcdNormalization[binLabel] + (1.0-wDown)*self._ewkFakesNormalization[binLabel]
            fakeRateErrorPart1 = errorPropagation.errorPropagationForProduct(w, wError, self._qcdNormalization[binLabel], self._qcdNormalizationError[binLabel])
            fakeRateErrorPart2 = errorPropagation.errorPropagationForProduct(w, wError, self._ewkFakesNormalization[binLabel], self._ewkFakesNormalizationError[binLabel])
            fakeRateError = ROOT.TMath.Sqrt(fakeRateErrorPart1**2 + fakeRateErrorPart2**2)
        self._combinedFakesNormalization[binLabel] = fakeRate
        self._combinedFakesNormalizationError[binLabel] = fakeRateError
        self._combinedFakesNormalizationUp[binLabel] = fakeRateUp
        self._combinedFakesNormalizationDown[binLabel] = fakeRateDown
        # Print output and store comments
        self._commentLines.extend(lines)
        for l in lines:
            print l
        
    def writeScaleFactorFile(self, filename, moduleInfoString):
        moduleInfo = moduleInfoString.split("_")
        s = ""
        s += "# Generated on %s\n"%datetime.datetime.now().ctime()
        s += "# by %s\n"%os.path.basename(sys.argv[0])
        s += "\n"
        s += "import sys\n"
        s += "\n"
        s += "def QCDInvertedNormalizationSafetyCheck(era, searchMode, optimizationMode):\n"
        s += "    validForEra = \"%s\"\n"%moduleInfo[0]
        s += "    validForSearchMode = \"%s\"\n"%moduleInfo[1]
        if len(moduleInfo) == 3:
            s += "    validForOptMode = \"%s\"\n"%moduleInfo[2]
        else:
            s += "    validForOptMode = \"\"\n"
        s += "    if not era == validForEra:\n"
        s += "        raise Exception(\"Error: inconsistent era, normalisation factors valid for\",validForEra,\"but trying to use with\",era)\n"
        s += "    if not searchMode == validForSearchMode:\n"
        s += "        raise Exception(\"Error: inconsistent search mode, normalisation factors valid for\",validForSearchMode,\"but trying to use with\",searchMode)\n"
        s += "    if not optimizationMode == validForOptMode:\n"
        s += "        raise Exception(\"Error: inconsistent optimization mode, normalisation factors valid for\",validForOptMode,\"but trying to use with\",optimizationMode)\n"
        s += "\n"
        s += "QCDNormalization = {\n"
        for k in self._qcdNormalization:
            s += '    "%s": %f,\n'%(k, self._qcdNormalization[k])
        s += "}\n"
        s += "EWKFakeTausNormalization = {\n"
        for k in self._ewkFakesNormalization:
            s += '    "%s": %f,\n'%(k, self._ewkFakesNormalization[k])
        s += "}\n"
        s += "QCDPlusEWKFakeTausNormalization = {\n"
        for k in self._combinedFakesNormalization:
            s += '    "%s": %f,\n'%(k, self._combinedFakesNormalization[k])
        s += "}\n"
        s += "QCDPlusEWKFakeTausNormalizationSystFakeWeightingVarDown = {\n"
        for k in self._combinedFakesNormalizationDown:
            s += '    "%s": %f,\n'%(k, self._combinedFakesNormalizationDown[k])
        s += "}\n"
        s += "QCDPlusEWKFakeTausNormalizationSystFakeWeightingVarUp = {\n"
        for k in self._combinedFakesNormalizationUp:
            s += '    "%s": %f,\n'%(k, self._combinedFakesNormalizationUp[k])
        s += "}\n"
        s += "# Log of fake rate calculation:\n"
        fOUT = open(filename,"w")
        fOUT.write(s)
        for l in self._commentLines:
            if l.startswith("\n"):
                fOUT.write("#\n#"+l[1:]+"\n")
            else:
                fOUT.write("#"+l+"\n")
        fOUT.close()
        print "\nNormalization factors written to '%s'\n"%filename
        self._generateCoefficientPlot()
        self._generateDQMplot()

    def _generateCoefficientPlot(self):
        def makeGraph(markerStyle, color, binList, valueDict, upDict, downDict):
            g = ROOT.TGraphAsymmErrors(len(binList))
            for i in range(len(binList)):
                g.SetPoint(i, i+0.5, valueDict[binList[i]])
                g.SetPointEYhigh(i, upDict[binList[i]])
                g.SetPointEYlow(i, downDict[binList[i]])
            g.SetMarkerSize(1.6)
            g.SetMarkerStyle(markerStyle)
            g.SetLineColor(color)
            g.SetLineWidth(2)
            g.SetMarkerColor(color)
            return g
        # Obtain bin list in right order
        keyList = []
        keys = self._qcdNormalization.keys()
        keys.sort()
        for k in keys:
            if "lt" in k:
                keyList.append(k)
        for k in keys:
            if "eq" in k:
                keyList.append(k)
        for k in keys:
            if "gt" in k:
                keyList.append(k)
        if "Inclusive" in keys:
            keyList.append("Inclusive")
        # Create graphs
        gQCD = makeGraph(24, ROOT.kRed, keyList, self._qcdNormalization, self._qcdNormalizationError, self._qcdNormalizationError)
        gFake = makeGraph(27, ROOT.kBlue, keyList, self._ewkFakesNormalization, self._ewkFakesNormalizationError, self._ewkFakesNormalizationError)
        upError = {}
        downError = {}
        for k in keys:
            upError[k] = self._combinedFakesNormalizationUp[k] - self._combinedFakesNormalization[k]
            downError[k] = self._combinedFakesNormalization[k] - self._combinedFakesNormalizationDown[k]
        gCombined = makeGraph(20, ROOT.kBlack, keyList, self._combinedFakesNormalization, upError, downError)
        # Make plot
        hFrame = ROOT.TH1F("frame","frame",len(keyList),0,len(keyList))
        for i in range(len(keyList)):
            binLabelText = getFormattedBinLabelString(keyList[i])
            hFrame.GetXaxis().SetBinLabel(i+1,binLabelText)
## for 3-prongs
        # hFrame.SetMinimum(0.0005)
        # hFrame.SetMaximum(0.01)
 ## original
        hFrame.SetMinimum(0.05)
        hFrame.SetMaximum(0.5)                 
        hFrame.GetYaxis().SetTitle("Normalization coefficient")
        hFrame.GetXaxis().SetLabelSize(20)
        c = ROOT.TCanvas()
        c.SetLogy()
        hFrame.Draw()
        gQCD.Draw("p same")
        gFake.Draw("p same")
        gCombined.Draw("p same")
        histograms.addStandardTexts(cmsTextPosition="outframe")
        #l = ROOT.TLegend(0.2,0.7,0.5,0.9) #original
        l = ROOT.TLegend(0.3,0.3,0.6,0.5)
       
        l.SetFillStyle(-1)
        l.SetBorderSize(0)
        l.AddEntry(gQCD, "Multijets", "p")
        l.AddEntry(gFake, "EWK+tt mis-id #tau", "p")
        l.AddEntry(gCombined, "Combined", "p")
        l.Draw()
        backup = ROOT.gErrorIgnoreLevel
        ROOT.gErrorIgnoreLevel = ROOT.kWarning
        for item in ["png", "C", "pdf"]:
            c.Print(self._plotDirName+"/QCDNormalisationCoefficients.%s"%item)
        ROOT.gErrorIgnoreLevel = backup
        print "Saved normalization coefficients into plot %s/QCDNormalisationCoefficients.png"%self._plotDirName

    ## Create a DQM style plot
    def _generateDQMplot(self):
        # Check the uncertainties on the normalization factors
        for k in self._dqmKeys.keys():
            self._addDqmEntry(k, "norm.coeff.uncert::QCD", self._qcdNormalizationError[k], 0.03, 0.10)
            self._addDqmEntry(k, "norm.coeff.uncert::fake", self._ewkFakesNormalizationError[k], 0.03, 0.10)
            value = abs(self._combinedFakesNormalizationUp[k]-self._combinedFakesNormalization[k])
            value = max(value, abs(self._combinedFakesNormalizationDown[k]-self._combinedFakesNormalizationUp[k]))
            self._addDqmEntry(k, "norm.coeff.uncert::combined", value, 0.03, 0.10)
        # Construct the DQM histogram
        h = ROOT.TH2F("QCD DQM", "QCD DQM",
                      len(self._dqmKeys[self._dqmKeys.keys()[0]].keys()), 0, len(self._dqmKeys[self._dqmKeys.keys()[0]].keys()),
                      len(self._dqmKeys.keys()), 0, len(self._dqmKeys.keys()))
        h.GetXaxis().SetLabelSize(15)
        h.GetYaxis().SetLabelSize(15)
        h.SetMinimum(0)
        h.SetMaximum(3)
        #h.GetXaxis().LabelsOption("v")
        nWarnings = 0
        nErrors = 0
        for i in range(h.GetNbinsX()):
            for j in range(h.GetNbinsY()):
                ykey = self._dqmKeys.keys()[j]
                xkey = self._dqmKeys[ykey].keys()[i]
                h.SetBinContent(i+1, j+1, self._dqmKeys[ykey][xkey])
                h.GetYaxis().SetBinLabel(j+1, ykey)
                h.GetXaxis().SetBinLabel(i+1, xkey)
                if self._dqmKeys[ykey][xkey] > 2:
                    nErrors += 1
                elif self._dqmKeys[ykey][xkey] > 1:
                    nWarnings += 1
        palette = array.array("i", [ROOT.kGreen+1, ROOT.kYellow, ROOT.kRed])
        ROOT.gStyle.SetPalette(3, palette)
        c = ROOT.TCanvas()
        c.SetBottomMargin(0.2)
        c.SetLeftMargin(0.2)
        c.SetRightMargin(0.2)
        h.Draw("colz")
        backup = ROOT.gErrorIgnoreLevel
        ROOT.gErrorIgnoreLevel = ROOT.kWarning
        for item in ["png", "C", "pdf"]:
            c.Print(self._plotDirName+"/QCDNormalisationDQM.%s"%item)
        ROOT.gErrorIgnoreLevel = backup
        ROOT.gStyle.SetPalette(1)
        print "Obtained %d warnings and %d errors for the normalization"%(nWarnings, nErrors)
        if nWarnings > 0 or nErrors > 0:
            print "Please have a look at %s/QCDNormalisationDQM.png to see the origin of the warning(s) and error(s)"%self._plotDirName

    ## Checks that input is valid
    def _checkInputValidity(self, templatesToBeFitted):
        # Require that the needed templates are created and that a histogram is provided for them
        for item in templatesToBeFitted:
            if not item.hasHisto():
                raise Exception ("Error: please call first setHistogram(...) for template named '%s'!"%item.getName())
        # Require that fitter is provided for the specified templates
        for item in templatesToBeFitted:
            if not item.isFittable():
                raise Exception ("Error: please call first setFitter(...) for template named '%s'!"%item.getName())
        # Require that bin labels of the templates are identical
        for item in templatesToBeFitted:
            if item.getBinLabel() != templatesToBeFitted[0].getBinLabel():
                raise Exception("Error: The bin label is different for '%s' than for '%s'!"%(item.getName(), templatesToBeFitted[0].getName()))
    
    def _addDqmEntry(self, binLabel, name, value, okTolerance, warnTolerance):
        if not binLabel in self._dqmKeys.keys():
            self._dqmKeys[binLabel] = OrderedDict()
        result = 2.5
        if abs(value) < okTolerance:
            result = 0.5
        elif abs(value) < warnTolerance:
            result = 1.5
        self._dqmKeys[binLabel][name] = result

    ## Fits templates
    def _fitTemplates(self, fitOptions):
        for key in self._templates.keys():
            item = self._templates[key]
            if item != None and item.isFittable():
                item.doFit(fitOptions=fitOptions, createPlot=True)

    ## Helper method to plot fitted templates (called from parent class when calculating norm.coefficients)
    def _makePlot(self, binLabel, histogramDictionary={}):
        # Make plot
        xTitle = "m_{jjb} (GeV/c^{2})"
        yTitle = "Events (normalized to unity)"

        ROOT.gStyle.SetOptFit(0)
        ROOT.gStyle.SetOptStat(0)
        plot = plots.PlotBase()
        for k in histogramDictionary.keys():
            if not (isinstance(histogramDictionary[k], ROOT.TH1) or isinstance(histogramDictionary[k], ROOT.TF1)):
                print histogramDictionary
                raise Exception("Error: Expected a dictionary of histograms")
            plot.histoMgr.appendHisto(histograms.Histo(histogramDictionary[k], k))
        plot.createFrame(self._plotDirName+"/finalFit_"+binLabel, opts={"ymin": 1e-5, "ymaxfactor": 4.})
        plot.getFrame().GetXaxis().SetTitle(xTitle)
        plot.getFrame().GetYaxis().SetTitle(yTitle)
#        histograms.addText(0.36,0.84, "Final fit, "+binLabel)
        histograms.addText(0.48,0.85, "Final fit")
        histograms.addText(0.48,0.77, getFormattedBinLabelString(binLabel))
        plot.getPad().SetLogy(True)
        histograms.addStandardTexts(cmsTextPosition="outframe")
        plot.draw()
        plot.save()
        return

    def _getSanityCheckTextForFractions(self, binLabel, label, fraction, fractionError, nBaseline, nCalculated):
        '''
        Helper method to be called from parent class when calculating norm.coefficients
        '''
        self.Verbose("_getSanityCheckTextForFractions()", True)
        if nCalculated > 0:
            ratio = nBaseline / nCalculated
        else:
            ratio = 0
        lines = []
        lines.append("    Fitted %s fraction: %f +- %f"%(label, fraction, fractionError))
        lines.append("      Sanity check: ratio = %.3f: baseline = %.1f vs. fitted = %.1f"%(ratio, nBaseline, nCalculated))
        self._commentLines.extend(lines)

        # Definitions
        lines  = []  
        align_ = "{:^80}" 
        align  = "{:<15} {:>20} {:>20} {:>20} {:>20}"
        header = align.format("Value", "Histogram", "Fitted", "Histogram-Fitted", "Ratio")
        hLine  = "="*100
        return lines

    
    def _getSanityCheckTextForFit(self, binLabel):
        '''
        Helper method to be called from parent class when calculating norm.coefficients
        '''
        self.Verbose("_getSanityCheckTextForFit()")

        # Definitions
        lines  = [] 
        align_ = "{:^80}"
        align  = "{:<15} {:>20} {:>20} {:>20} {:>20}"
        header = align.format("Value", "Histogram", "Fitted", "Histogram-Fitted", "Ratio")
        hLine  = "="*100
        
        # For-loop: All template keys
        for key in self._templates.keys():
            item = self._templates[key]
            if item.isFittable():
                # Save info
                name       = item.getName()
                nHisto     = item.getNeventsFromHisto(False)
                nHistoUp   = item.getNeventsErrorFromHisto(False)
                nHistoDown = item.getNeventsErrorFromHisto(False)
                nFit       = item.getNeventsFromFit()
                nFitUp     = item.getNeventsTotalErrorFromFit()[0]
                nFitDown   = item.getNeventsTotalErrorFromFit()[1]
                diff       = nHisto-nFit
                diffUp     = errorPropagation.errorPropagationForSum(nHisto, nHistoUp  , nFit, nFitUp)
                diffDown   = errorPropagation.errorPropagationForSum(nHisto, nHistoDown, nFit, nFitDown)
                ratio      = 0
                ratioUp    = 0
                ratioDown  = 0
                if item.getNeventsFromFit()>0:
                    ratio     = item.getNeventsFromHisto(False) / item.getNeventsFromFit()
                    ratioUp   = errorPropagation.errorPropagationForDivision(nHisto, nHistoUp  , nFit, nFitUp)
                    ratioDown = errorPropagation.errorPropagationForDivision(nHisto, nHistoDown, nFit, nFitDown)
                else:
                    self.Print("Cannot divide by zero for item \"%s\%. Setting ratio to zero" % (key), True)

                # Construct the table
                #lines.append(align_.format("Bin: " + binLabel) )
                lines.append( "{:^100}".format(name) )
                lines.append(hLine)
                lines.append(header)
                lines.append(hLine)
                lines.append(align.format("Events"   , "%.1f" % nHisto    , "%.1f" % nFit    , "%.1f" % diff    , "%.3f" % ratio    ) )
                lines.append(align.format("Error (+)", "%.1f" % nHistoUp  , "%.1f" % nFitUp  , "%.1f" % diffUp  , "%.3f" % ratioUp  ) )
                lines.append(align.format("Error (-)", "%.1f" % nHistoDown, "%.1f" % nFitDown, "%.1f" % diffDown, "%.3f" % ratioDown) )
                lines.append("")
                #lines.append("... Template fit sanity check (%s): Ratio = %.3f: Nevents in histogram = %.1f +- %.1f vs. fitted = %.1f + %.1f - %.1f"% (item.getName(), ratio, nHisto, nHistoUp, nFit, nFitUp, nFitDown))
                self._addDqmEntry(binLabel, "TmplFit::%s"%item.getName(), ratio-1, 0.03, 0.10)

        self._commentLines.extend(lines)
        return lines

    def _checkOverallNormalization(self, binLabel, value, err): #iro-
        '''
        Helper method to be called from parent class when calculating norm.coefficients
        '''
        self.Verbose("_checkOverallNormalization()")

        # Definitions
        lines = []
        msg   = "Fitted overall normalization factor for purity (should be 1.0) = %f +- %f"%(value, err)
        lines.append(msg)
        print colors.GREEN
        self.Print(msg, True)
        print colors.WHITE

        self._addDqmEntry(binLabel, "OverallNormalization(par0)", value-1.0, 0.03, 0.10)
        self._commentLines.extend(lines)
        return lines
    
    ## Helper method to be called from parent class when calculating norm.coefficients
    def _getResultOutput(self, binLabel):
        lines = []
        lines.append("   Normalization factor (QCD): %f +- %f"%(self._qcdNormalization[binLabel], self._qcdNormalizationError[binLabel]))
        lines.append("   Normalization factor (EWK fake taus): %f +- %f"%(self._ewkFakesNormalization[binLabel], self._ewkFakesNormalizationError[binLabel]))
        lines.append("   Combined norm. factor: %f +- %f"%(self._combinedFakesNormalization[binLabel], self._combinedFakesNormalizationError[binLabel]))
        self._commentLines.extend(lines)
        return lines

#================================================================================================ 
# Class Definitions
#================================================================================================ 
class QCDNormalizationManagerDefault(QCDNormalizationManagerBase):
    '''
    Invoke default algorithm
    1) w_QCD obtained from data-driven fit to data = a*(b*template_QCD + (1-b)*template_EWK)
    2) w_EWKfake obtained from MC: baseline / inverted
    3) w_combined = a*w_QCD + (1-a)*w_EWKfake, a determined with MC for EWK fakes
    
    Number of QDCD events (N_QCD) can then be obtained with:
    N_QCD = w_combined*(N_data - N_EWKtau)
    '''
    def __init__(self, binLabels, resultDirName, moduleInfoString):
        QCDNormalizationManagerBase.__init__(self, binLabels, resultDirName, moduleInfoString)
        self._requiredTemplateList = ["EWKFakeB_Baseline", 
                                      "EWKFakeB_Inverted", 
                                      "EWKGenuineB_Baseline", 
                                      "EWKGenuineB_Inverted",
                                      "EWKInclusive_Baseline", 
                                      "EWKInclusive_Inverted",
                                      "QCD_Baseline", 
                                      "QCD_Inverted"]

    def calculateNormalizationCoefficients(self, dataHisto, fitOptions, FITMIN, FITMAX, **kwargs):
        qcdTemplate = self._templates["QCD_Inverted"]
        ewkInclusiveTemplate = self._templates["EWKInclusive_Baseline"]
        templatesToBeFitted = [qcdTemplate, ewkInclusiveTemplate]
        self._checkInputValidity(templatesToBeFitted)
        
        self.Verbose("Fitting templates", True)
        self._fitTemplates(fitOptions)
        
        #===== Create a temporary template for data
        self.Verbose("Fitting templates to data (default method)", True)
        dataTemplate = QCDNormalizationTemplate("data", self._plotDirName)
        binLabel = self._templates[self._requiredTemplateList[0]].getBinLabel()
        dataTemplate.setHistogram(dataHisto, binLabel)
        dataTemplate.plot()
        dataTemplate.setFitter(FitFunction("FitDataWithQCDAndInclusiveEWK", #iro-
                                           QCDFitFunction = qcdTemplate.getFitFunction(),
                                           parQCD = qcdTemplate.getFittedParameters(),
                                           QCDnorm = 1.0,
                                           EWKInclusiveFunction = ewkInclusiveTemplate.getFitFunction(),
                                           parEWK = ewkInclusiveTemplate.getFittedParameters(),
                                           EWKNorm = 1.0),
                               FITMIN, FITMAX)
        #===== Do fit to data
        dataTemplate.setDefaultFitParam(defaultInitialValue=[1.0, 0.90, 0.10], defaultLowerLimit=[0.0, 0.0, 0.0], defaultUpperLimit=[10.0, 1.0, 1.0])
        dataTemplate.doFit(fitOptions)
        
        #===== Plot fitted functions
        dataHisto.SetLineColor(ROOT.kBlack)
        funcData = dataTemplate.obtainFittedFunction(1.0, FITMIN, FITMAX)
        funcData.SetLineColor(ROOT.kRed)
        funcData.SetLineStyle(2)
        funcQCD = qcdTemplate.obtainFittedFunction(dataTemplate.getFittedParameters()[1], FITMIN, FITMAX)
        funcQCD.SetLineColor(ROOT.kBlue)
        funcQCD.SetLineWidth(2)
        funcQCD.SetLineStyle(2)
        self._makePlot(binLabel,
                       {dataHisto.GetName(): dataHisto,
                        "fitted data": funcData,
                        "QCD template": funcQCD})

        #===== Handle results
        # should one divide the fractions with dataTemplate.getFittedParameters()[0] ??? (right now not because the correction is so small)
        nQCDFitted = dataTemplate.getFittedParameters()[1]*dataTemplate.getNeventsFromHisto(False)

        #==== Store results in list
        lines = []
        self.Verbose("Sanity Check: Text for fit")
        lines.extend(self._getSanityCheckTextForFit(binLabel))

        self.Verbose("Sanity Check: Text for Fractions")
        fraction      = dataTemplate.getFittedParameters()[1]
        fractionError = dataTemplate.getFittedParameterErrors()[1]
        nBaseline     = self._templates["QCD_Baseline"].getNeventsFromHisto(False)
        nCalculated   = nQCDFitted
        lines.extend(self._getSanityCheckTextForFractions(binLabel, "QCD",  fraction, fractionError, nBaseline, nCalculated))

        self.Verbose("Sanity Check: Overall Normalization")
        value = dataTemplate.getFittedParameters()[0]
        error = dataTemplate.getFittedParameterErrors()[0]
        lines.extend(self._checkOverallNormalization(binLabel, value, error) ) #iro-

        #==== Print results line-by-line
        if 0:
            for line in lines:
                print line

        #===== Normalization factor for QCD (from fit)
        qcdNormFactor = nQCDFitted / self._templates["QCD_Inverted"].getNeventsFromHisto(False)
        nQCDBaselineError = errorPropagation.errorPropagationForProduct(dataTemplate.getFittedParameters()[1], dataTemplate.getFittedParameterErrors()[1],
                                                                        dataTemplate.getNeventsFromHisto(False), dataTemplate.getNeventsErrorFromHisto(False))
        qcdNormFactorError = errorPropagation.errorPropagationForDivision(nQCDFitted, nQCDBaselineError,
                                                                          self._templates["QCD_Inverted"].getNeventsFromHisto(False), self._templates["QCD_Inverted"].getNeventsErrorFromHisto(False))
        self._qcdNormalization[binLabel] = qcdNormFactor
        self._qcdNormalizationError[binLabel] = qcdNormFactorError

        #===== Normalization factor for EWK fake taus (from MC)
        ewkFakesNormFactor = None
        ewkFakesNormFactorError = None
        nFakeBaseline = self._templates["EWKFakeB_Baseline"].getNeventsFromHisto(False)
        nFakeInverted = self._templates["EWKFakeB_Inverted"].getNeventsFromHisto(False)
        if nFakeInverted > 0.0:
            ewkFakesNormFactor = nFakeBaseline / nFakeInverted
            ewkFakesNormFactorError = errorPropagation.errorPropagationForDivision(nFakeBaseline, self._templates["EWKFakeB_Baseline"].getNeventsErrorFromHisto(False),
                                                                                   nFakeInverted, self._templates["EWKFakeB_Inverted"].getNeventsErrorFromHisto(False))
        self._ewkFakesNormalization[binLabel] = ewkFakesNormFactor
        self._ewkFakesNormalizationError[binLabel] = ewkFakesNormFactorError

        
# Unit tests
if __name__ == "__main__":
    import unittest
    class TestFitFunction(unittest.TestCase):
        def testNonExistingFitFunction(self):
            with self.assertRaises(Exception):
                FitFunction("dummy")
        
        def testGaussian(self):
            f = FitFunction("Gaussian")
            self.assertEqual(f([0],[1,0,1]), 0.3989422804014327)
            
    class TestQCDNormalizationTemplate(unittest.TestCase):
        def _getGaussianHisto(self):
            h = ROOT.TH1F("h","h",10,0,10)
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
            return h
      
        def testInitialization(self):
            q = QCDNormalizationTemplate("EWK testline", "dummy")
            # Test initialization
            with self.assertRaises(Exception):
                q.getNeventsFromHisto(True)
            with self.assertRaises(Exception):
                q.getNeventsErrorFromHisto(True)
            with self.assertRaises(Exception):
                q.getNeventsFromFit()
            with self.assertRaises(Exception):
                q.getNeventsErrorFit()
            self.assertEqual(q.getFitResults(), None)
            with self.assertRaises(Exception):
                q.plot()
            with self.assertRaises(Exception):
                q.doFit()
        
        def testEmptyHistogram(self):
            q = QCDNormalizationTemplate("EWK testline", "dummy")
            h = ROOT.TH1F("h","h",10,0,10)
            q.setHistogram(h, "Inclusive bin")
            with self.assertRaises(Exception):
                q.doFit()
            self.assertEqual(q.getNeventsFromHisto(True), 0.0)
            self.assertEqual(q.getNeventsErrorFromHisto(True), ROOT.TMath.Sqrt(0.0))
            h.Delete()
        
        def testFitWithoutFunction(self):
            q = QCDNormalizationTemplate("EWK testline", "dummy")
            h = self._getGaussianHisto()
            q.setHistogram(h, "Inclusive bin")
            self.assertLess(abs(q.getNeventsFromHisto(True)-1000.0),0.001)
            self.assertLess(abs(q.getNeventsErrorFromHisto(True) - ROOT.TMath.Sqrt(1000.0)), 0.0001)
            self.assertLess(abs(q.getNeventsFromHisto(False)-973.0),0.001)
            self.assertLess(abs(q.getNeventsErrorFromHisto(False) - ROOT.TMath.Sqrt(973.0)), 0.0001)
            self.assertEqual(q.getFitResults(), None)
            with self.assertRaises(Exception):
                q.getNeventsFromFit()
            with self.assertRaises(Exception):
                q.getNeventsErrorFit()
            q.reset()
            with self.assertRaises(Exception):
                q.getNeventsFromHisto(True)
            with self.assertRaises(Exception):
                q.getNeventsErrorFromHisto(True)
            with self.assertRaises(Exception):
                q.getNeventsFromFit()
            with self.assertRaises(Exception):
                q.getNeventsErrorFit()

        def testFitParams(self):
            q = QCDNormalizationTemplate("EWK testline", "dummy")
            # input format
            with self.assertRaises(Exception):
                q.setDefaultFitParam(defaultInitialValue=2)
            with self.assertRaises(Exception):
                q.setDefaultFitParam(defaultLowerLimit=2, defaultUpperLimit=[2])
            with self.assertRaises(Exception):
                q.setDefaultFitParam(defaultLowerLimit=[2],defaultUpperLimit=2)
            with self.assertRaises(Exception):
                q.setFitParamForBin("bin", initialValue=2)
            with self.assertRaises(Exception):
                q.setFitParamForBin("bin", lowerLimit=2, upperLimit=[2])
            with self.assertRaises(Exception):
                q.setFitParamForBin("bin", lowerlimit=[2], upperLimit=2)
            # list length
            with self.assertRaises(Exception):
                q.setDefaultFitParam(defaultLowerLimit=[2])
            with self.assertRaises(Exception):
                q.setDefaultFitParam(defaultUpperLimit=[2])
            with self.assertRaises(Exception):
                q.setDefaultFitParam(defaultLowerLimit=[2], defaultUpperLimit=[2,3])
            with self.assertRaises(Exception):
                q.setFitParamForBin("bin", lowerLimit=[2])
            with self.assertRaises(Exception):
                q.setFitParamForBin("bin", upperLimit=[2])
            with self.assertRaises(Exception):
                q.setFitParamForBin("bin", lowerLimit=[2], upperLimit=[2,3])

        def testSimpleFit(self):
            _createPlots = False # To test plotting, set to True
            q = QCDNormalizationTemplate("EWK testline", "dummy",quietMode=True)
            h = self._getGaussianHisto()
            q.setHistogram(h, "Inclusive bin")
            # Test proper parameters to fitter setting
            with self.assertRaises(Exception):
                q.setFitter([], 0, 10)
            with self.assertRaises(Exception):
                q.setFitter(FitFunction("Gaussian"), 10, 0)
            # Do fit (it fails with default parameters)
            q.setFitter(FitFunction("Gaussian"), 0, 10)
            if _createPlots:
                q.plot()
            q.doFit(fitOptions="S R L Q", createPlot=False)
            self.assertEqual(q.getNeventsFromFit(), 0.)
            self.assertEqual(q.getNeventsTotalErrorFromFit()[0], 0.)
            self.assertEqual(q.getNeventsTotalErrorFromFit()[1], 0.)
            # Reset
            q.reset()
            with self.assertRaises(Exception):
                q.getNeventsFromFit()
            with self.assertRaises(Exception):
                q.getNeventsErrorFit()
            # Set params (which do not affect anything)
            q.setFitParamForBin("Non-inclusive bin", initialValue=[10,4,2])
            q.setHistogram(h, "Inclusive bin")
            q.doFit(fitOptions="S R L Q", createPlot=False)
            self.assertEqual(q.getNeventsFromFit(), 0.)
            self.assertEqual(q.getNeventsTotalErrorFromFit()[0], 0.)
            self.assertEqual(q.getNeventsTotalErrorFromFit()[1], 0.)
            # Set params (for bin)
            q.reset()
            q.setFitParamForBin("Inclusive bin", initialValue=[1,4,2], lowerLimit=[0.01, 0, 0], upperLimit=[100, 10, 10])
            q.setHistogram(h, "Inclusive bin")
            #q.printFitParamSettings()
            q.doFit(fitOptions="S R L", createPlot=_createPlots)
            self.assertLess(abs(q.getNeventsFromFit()-1), 0.01)
            self.assertLess(abs(q.getNeventsTotalErrorFromFit()[0]-1.003), 0.1)
            self.assertLess(abs(q.getNeventsTotalErrorFromFit()[1]-1.003), 0.1)
            #q.printResults()

    unittest.main()
