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
import HiggsAnalysis.NtupleAnalysis.tools.ShellStyles as ShellStyles
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
# Global Function Definitions
#================================================================================================ 
def Print(msg, printHeader=False):
    fName = __file__.split("/")[-1]
    if printHeader==True:
        print "=== ", fName
        print "\t", msg
    else:
        print "\t", msg
    return

def createLegend(xMin=0.62, yMin=0.79, xMax=0.92, yMax=0.92):
    l = ROOT.TLegend(xMin, yMin, xMax, yMax)
    l.SetFillStyle(-1)
    l.SetBorderSize(0)
    return l

def getHistoFitTable(name, nHisto, nHistoUp, nFit, nFitUp, nDiff, nDiffUp, nRatio, nRatioUp):
    table  = [] 
    align  = "{:<20} {:>15} {:^3} {:<10} {:<60}"
    header = align.format(name, "Events", "+/-", "Error", "Description")
    hLine  = "="*120
    table.append(hLine)
    table.append(header)
    table.append(hLine)
    table.append(align.format("Histogram"    , "%.3f" % nHisto, "+/-", "%.3f" % nHistoUp, "Absolute uncertainty quoted (up=down)") )
    table.append(align.format("Fit"          , "%.3f" % nFit  , "+/-", "%.3f" % nFitUp  , "Total fit parameter uncertainty (up)") )
    table.append(align.format("Histogram-Fit", "%.3f" % nDiff , "+/-", "%.3f" % nDiffUp , "Error-propagation (up)") )
    table.append(align.format("Histogram/Fit", "%.3f" % nRatio, "+/-", "%.3f" % nRatioUp, "Error-propagation (up)") )
    table.append(hLine)
    table.append("")
    return table


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
    https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
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
                'BOLD'     :'\033[;1m',
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
        BOLD     = colordict['BOLD']
    else:
        RED, GREEN, BLUE, GRAY, WHITE, ORANGE, CYAN, PURPLE, LIGHTRED, PINK, YELLOW, BOLD = '', '', '', '', '', '', '', '', '', '', '', ''


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
            "Linear"          : 2,
            "ErrorFunction"   : 2,
            "ExpFunction"     : 2,
            "Gaussian"        : 3,
            "DoubleGaussian"  : 6,
            "SumFunction"     : 5,
            "RayleighFunction": 2,
            "EWKFunctionInv"  : 4,
            "QCDEWKFunction"  : 7,
            "QCDFunctionFixed": 8,
            "FitDataWithQCDAndFakesAndGenuineTaus": 3,
            "FitDataWithFakesAndGenuineTaus"      : 2,
            # 
            "EWKFunction"         : 9,
            "QCDFunction"         : 7,
            "QCDFunctionAlt"      : 5,
            "FitDataWithQCDAndEWK": 2,
            "CrystalBall"         : 5,
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
    
    def RooLogNormal(self, x, m0, k):
        '''
        https://root.cern.ch/doc/v608/classRooLognormal.html
        https://root.cern.ch/doc/v608/RooLognormal_8cxx_source.html

        RooFit Lognormal PDF. The two parameters are:
        - m0 = median    [the median of the distribution]
        - k = exp(sigma) [sigma is called the shape parameter in the TMath parametrization]

        \begin{align}
        \mathrm{Lognormal}(x,m_{0},k) = \frac{e^{(-\ln^2(x/m_0))/(2\ln^2(k))}}{\sqrt{2\pi \cdot \ln(k)\cdot x}}
        \end{align}

        The parametrization here is physics driven and differs from the ROOT::Math::lognormal_pdf(x, m, s, x0) with:
        - m = log(m0)
        - s = log(k)
        - x0 = 0

        Double_t RooLognormal::evaluate() const
        {
        Double_t xv = x;
        Double_t ln_k = TMath::Abs(TMath::Log(k));
        Double_t ln_m0 = TMath::Log(m0);
        Double_t x0 = 0;
        
        Double_t ret = ROOT::Math::lognormal_pdf(xv,ln_m0,ln_k,x0);
        return ret ;
        }

        #  ln(k)<1 would correspond to sigma < 0 in the parametrization
        #  resulting by transforming a normal random variable in its
        #  standard parametrization to a lognormal random variable
        #  => treat ln(k) as -ln(k) for k<1
        '''
        xv    = x[0]
        ln_k  = ROOT.TMath.Abs(ROOT.TMath.Log(k))
        ln_m0 = ROOT.TMath.Log(m0)
        x0    = 0
        ret   = ROOT.Math.lognormal_pdf(xv, ln_m0, ln_k, x0)
        return ret
    
    def RooExponential(self, x, a):
        '''
        https://root.cern.ch/doc/v608/classRooExponential.html
        https://root.cern.ch/doc/v608/RooExponential_8cxx_source.html
        '''
        return ROOT.TMath.Exp(+a*x[0])

    def RooCBShape(self, x, m0, sigma, alpha, n):
        '''
        https://root.cern.ch/doc/master/classRooCBShape.html#ac81db429cde612e553cf61ec7c126ac1
        https://root.cern.ch/doc/master/RooCBShape_8cxx_source.html
        
        par[0]*ROOT.Math.crystalball_function(x[0], par[1], par[2], par[3], par[4])
        '''
        t = (x[0]-m0)/sigma
        if (alpha < 0):
            t = -t

        absAlpha = abs(alpha)

        if (t >= -absAlpha):
            return ROOT.TMath.Exp(-0.5*t*t)
        else:
            a = ROOT.TMath.Power(n/absAlpha,n)*ROOT.TMath.Exp(-0.5*absAlpha*absAlpha)
            b = (n/absAlpha) - absAlpha
            return a/ROOT.TMath.Power(b - t, n)

    def RooGaussian(self, x, mean, sigma):
        '''
        https://root.cern.ch/doc/master/classRooGaussian.html
        https://root.cern.ch/doc/master/RooGaussian_8cxx_source.html
        http://www.nbi.dk/~petersen/Teaching/Stat2013/Week1/RootIntro.py
        '''
        arg = x[0] - mean;
        sig = sigma
        # print "ROOT.TMath.Exp(-0.5*%s/(%s))" % (arg*arg, sig*sig) 
        return ROOT.TMath.Exp(-0.5*arg*arg/(sig*sig))
    
    def QCDFunctionAlt(self, x, par, boundary, norm=1, rejectPoints=0):
        '''
        https://root.cern.ch/root/html524/ROOT__Math.html#TopOfPage
        http://www.nbi.dk/~petersen/Teaching/Stat2013/Week1/RootIntro.py        

        x and par are standard root way to define the fit function
        from x only x[0] is used; it is the x-variable.        
        par contains the fitted parameters, you can give initial values, but the final ones come from the fitting.
        ''' 
        #if x[0] > boundary:
        #    return

        if rejectPoints > 0:
            if (x[0] > 220 and x[0] < 226):
                ROOT.TF1.RejectPoint()
                print "Rejecting point with value x=", x[0]
                return 0

        return self._additionalNormFactor*norm*(par[0]*self.RooLogNormal(x, par[1], par[2]) + 
                                                (1-par[0])*self.RooGaussian(x, par[3], par[4])
                                                )
    
    def QCDFunction(self, x, par, boundary, norm=1, rejectPoints=0):
        '''
        https://root.cern.ch/root/html524/ROOT__Math.html#TopOfPage
        
        x and par are standard root way to define the fit function
        from x only x[0] is used; it is the x-variable.        
        par contains the fitted parameters, you can give initial values, but the final ones come from the fitting.
        ''' 
        #if x[0] > boundary:
        #    return

        if rejectPoints > 0:
            if (x[0] > 216 and x[0] < 218):
                ROOT.TF1.RejectPoint()
                print "Rejecting point with value x=", x[0]
                return 0

        if par[2] < 0:
            for i, p in enumerate(par):
                print "p[%s] = %s" %(i, p)
                return 0
        return self._additionalNormFactor*norm*(par[0]*self.RooLogNormal(x, par[1], par[2]) + 
                                                par[3]*self.RooExponential(x, par[4]) +
                                                (1-par[0]-par[3])*self.RooGaussian(x, par[5], par[6])
                                                )

    def EWKFunction(self,x, par, boundary, norm=1, rejectPoints=0):
        '''
        http://www.nbi.dk/~petersen/Teaching/Stat2013/Week1/RootIntro.py
        x and par are standard root way to define the fit function
        from x only x[0] is used; it is the x-variable.        
        par contains the fitted parameters, you can give initial values, but the final ones come from the fitting.
        
        Landau(x, mpv, widthParam), ROOT.TMath.Gaus(x[0], sigma, mean), ROOT.TMath.BreitWigner(x[0], decayWidth, mass)
        ''' 
        #if x[0] < boundary:
        #    return

        if rejectPoints > 0:
            if (x[0] > 216 and x[0] < 218):
                ROOT.TF1.RejectPoint()
                print "Rejecting point with value x=", x[0]
                return 0    
        return self._additionalNormFactor*norm*(par[0]*self.RooCBShape(x, par[1], par[2], par[3], par[4]) +
                                                par[5]*self.RooExponential(x, par[6]) +
                                                (1-par[0]-par[5])*self.RooGaussian(x, par[7], par[8]) 
                                                )

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

    def FitDataWithQCDAndEWK(self, x, par, fitFunctionQCD, parQCD, normQCD, fitFunctionEWK, parEWK, normEWK):
        '''
        QCD and  EWK (inclusive) as separate templates
        '''
        nQCD = fitFunctionQCD(x, parQCD, norm=normQCD)
        nEWK = fitFunctionEWK(x, parEWK, norm=normEWK)
        return par[0]*(par[1]*nQCD + (1.0 - par[1])*nEWK)

    def FitDataWithFakesAndGenuineTaus(self, x, par,
            QCDAndFakesFitFunction, parQCDAndFakes, QCDAndFakesnorm,
            EWKGenuineTausFitFunction, parEWKGenuineTaus, EWKGenuineTausNorm):
        '''
        QCD and fake tau templates as one inclusive template
        '''
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
    Helper function to plot template names in a more understandable way
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
        self._information = []
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

    def getInfo(self):
        return self._information

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

    def createFitPlot(self, h, fit, bSaveToFile=True):
        '''
        '''

        # Customisations
        units  = "GeV/c^{2}"
        xTitle = "m_{jjb} (%s)" % units
        yTitle = "Events / %.0f %s" % (h.GetBinWidth(0), units) #"Events (normalized to unity)"
        yLog   = False
        fName  = self._plotDirName + "/fit_" + self._name.replace(" ","_") + "_" + self._binLabel
        fName  = fName.replace(" ", "_")
        if yLog:
            yMaxFactor = 4
        else:
            yMaxFactor = 1.1

        # Disable fit/statistics box
        ROOT.gStyle.SetOptFit(0)
        ROOT.gStyle.SetOptStat(0)

        # Customise fit function
        if "ewk" in h.GetName().lower():
            fit.SetLineColor(ROOT.kMagenta-2)
            fit.SetLineStyle(ROOT.kDashed)
            fit.SetLineWidth(3)
        elif "qcd" in h.GetName().lower():
            fit.SetLineColor(ROOT.kOrange-2)
            fit.SetLineStyle(ROOT.kDashed)
            fit.SetLineWidth(3)
        elif "fakeb" in h.GetName().lower():
            fit.SetLineColor(ROOT.kRed)
            fit.SetLineStyle(ROOT.kDashed)
            fit.SetLineWidth(3)
        elif "data" in h.GetName().lower():
            fit.SetLineColor(ROOT.kBlue)
            fit.SetLineStyle(ROOT.kSolid)
            fit.SetLineWidth(3)
        else:
            print h.GetName()
            raise Exception("Error: This should never be reached!")

        # Create a plot base with the fit above the data points to make it visible!
        plot = plots.PlotBase()
        plot.histoMgr.appendHisto( histograms.Histo(fit, "fit") )
        plot.histoMgr.appendHisto( histograms.Histo(h, h.GetName()) )


        # Customise histo and fit function
        if "ewk" in h.GetName().lower():
            plot.histoMgr.forHisto(h.GetName(), styles.getDataStyle() ) #styles.getAltEWKStyle() )
            plot.histoMgr.setHistoLegendStyle(h.GetName(), "P")
        elif "qcd" in h.GetName().lower():
            plot.histoMgr.forHisto(h.GetName(), styles.getDataStyle() ) #styles.getQCDStyle() )
            plot.histoMgr.setHistoLegendStyle(h.GetName(), "P")
        elif "fakeb" in h.GetName().lower():
            plot.histoMgr.forHisto(h.GetName(), styles.getDataStyle() ) #styles.getFakeBStyle() )
            plot.histoMgr.setHistoLegendStyle(h.GetName(), "P")
        elif "data" in h.GetName().lower():
            plot.histoMgr.forHisto(h.GetName(), styles.getDataStyle() )
            plot.histoMgr.setHistoLegendStyle(h.GetName(), "P")
        else:
            fit.SetLineColor(ROOT.kGray)
            fit.SetLineColor(ROOT.kSolid)
        fit.SetLineWidth(3)
        
        # Overwrite some options
        plot.histoMgr.setHistoDrawStyle(h.GetName(), "AP")

        # Create frame
        myOpts = {"ymin": 1e-5, "ymaxfactor": yMaxFactor}
        plot.setLegend(createLegend())
        plot.createFrame(fName, opts=myOpts)
        plot.getFrame().GetXaxis().SetTitle(xTitle)
        plot.getFrame().GetXaxis().SetRangeUser(0.0*self._fitRangeMin, 1.1*self._fitRangeMax)
        plot.getFrame().GetYaxis().SetTitle(yTitle)

        # Add text
        histograms.addStandardTexts(cmsTextPosition="outframe")
        #histograms.addText(0.72, 0.85-0.08*0, getFormattedTemplateName(self._name))
        #histograms.addText(0.72 ,0.85-0.08*1, getFormattedBinLabelString(self._binLabel))

        # Cut lines/boxes
        _kwargs1 = {"lessThan": True}
        _kwargs2 = {"lessThan": False}
        plot.addCutBoxAndLine(cutValue=self._fitRangeMin, fillColor=ROOT.kGray, box=False, line=True, **_kwargs1)
        plot.addCutBoxAndLine(cutValue=self._fitRangeMax, fillColor=ROOT.kGray, box=False, line=True, **_kwargs2)

        # Draw and save plot
        plot.getPad().SetLogy(yLog)
        plot.draw()
        plot.save()

        if bSaveToFile:
            fileName = self._plotDirName + "/" + h.GetName() + ".root"
            fileName = fileName.replace(" ", "_")
            msg = "Saving template \"%s\" to file %s" % (h.GetName(), fileName)
            self.Print(ShellStyles.NoteLabel() + msg + ShellStyles.NormalStyle(), True)
            h.SaveAs(fileName)
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

    def getHisto(self):
        '''
        Returns the fitted histogram
        '''
        return self._histo

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
        func.SetLineWidth(3)
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

    def plot(self, FITMIN, FITMAX):
        '''
        Make a plot of the m_{jjb} histogram
        '''
        if self._histo == None:
            raise Exception("Error: Please provide first the histogram with the 'setHistogram' method")
        if self._histo.GetEntries() == 0:
            print "Skipping plot for '%s' because it has zero entries."%self._name
            return

        # Create histo
        plot   = plots.PlotBase()
        fName  = self._plotDirName+"/template_"+self._name.replace(" ","_")+"_"+self._binLabel
        fName  = fName.replace(" ", "_")
        h      = self._histo.Clone(self._histo.GetName()+"clone")
        hName  = self._histo.GetName()

        # Scale to the normalization factor
        h.Scale(self._normalizationFactor)
        plot.histoMgr.appendHisto(histograms.Histo(h, self._histo.GetName()))

        # Customise histo
        units  = "GeV/c^{2}"
        xTitle = "m_{jjb} (%s)" % units
        yTitle = "Events / %.0f %s" % (h.GetBinWidth(0), units) #"Events / bin"

        # Set plotting style
        st = styles.getDataStyle().clone()
        st.append(styles.StyleFill(fillColor=ROOT.kYellow))
        plot.histoMgr.forHisto(self._histo.GetName(), st)
        plot.histoMgr.setHistoDrawStyle(hName  , "HIST")
        plot.histoMgr.setHistoLegendStyle(hName, "FL")

        # Create frame
        myOpts = {"ymin": 0.1, "ymaxfactor": 4.0}
        plot.setLegend(createLegend(xMin=0.62, yMin=0.82, xMax=0.92, yMax=0.92))
        plot.createFrame(fName, opts=myOpts)
        plot.getFrame().GetXaxis().SetTitle(xTitle)
        plot.getFrame().GetYaxis().SetTitle(yTitle)
        plot.getFrame().GetXaxis().SetRangeUser(FITMIN*0.0, FITMAX*1.1)
        
        # Add text
        histograms.addStandardTexts(cmsTextPosition="outframe")
        nEvents = int(self._histo.Integral(0,-1)*self._normalizationFactor+0.5) # round to closest integer
        histograms.addText(0.65, 0.78, "N = %d" % nEvents)
        # histograms.addText(0.72, 0.85-0.08*0, getFormattedTemplateName(self._name))
        # histograms.addText(0.72, 0.85-0.08*1, getFormattedBinLabelString(self._binLabel))

        # Draw and save plot
        plot.getPad().SetLogy(True)
        #plot.setFileName("template_"+self._name.replace(" ","_")+"_"+self._binLabel)
        plot.draw()        
        plot.save(formats=[".png", ".pdf", ".C"])

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

    def ChangeShellColour(self):
        '''
        Customise colour of printed output (makes spotting easier)
        '''
        self.Verbose("ChangeShellColour()")
        hName = self.getHisto().GetName().lower()
        
        isQCD   = "qcd" or "fakeb" in hName
        isEWK   = "ewk" in hName
        isDaata = "data" in hName

        if isQCD:
            print colors.YELLOW
        elif isEWK:
            print colors.PURPLE
        elif isData: 
            print colors.BOLD
        else:
            raise Exception("Error: Unexpected histogram name %s. Cannot decide SHELL colour" % (hName) )
        return

    def PrintFitResults(self, h, r, fitOptions):
        '''
        Print information contained in the TFitResultPtr r
        
        See:
        https://root.cern.ch/doc/v608/classROOT_1_1Fit_1_1FitResult.html#ac96273476383baba62ca1585b6bd4fda
        https://root.cern.ch/doc/v608/classTFitResult.html
        '''
        self.Verbose("PrintFitResults()")
        
        # Sanity checks
        if r.IsEmpty():
            raise Exception("Error: The TFitResultPtr is empty!")
        if not r.IsValid():
            r.Print("V")
            raise Exception("Error: The TFitResultPtr is not valid! The fit failed...")
        
        msg = "Successfully fitted histogram \"%s\"!" % h.GetName()
        self.Print(ShellStyles.NoteLabel() + msg, True)

        # Print full information of fit including covariance matrix and correlation
        if 0:
            r.Print("V")

        # Print customly made tables
        results = ["{:^100}".format("Fit on \"%s\"" % h.GetName())]
        results.extend(self.PrintFitResultsGeneral(r, fitOptions))
        results.extend(self.PrintFitResultsParameters(r))
        results.extend(self.PrintFitResultsHistos(r))

        # Store all information for later used (write to file)
        self._information.extend(results)
        return 

    def PrintFitResultsGeneral(self, r, fitOptions):
        '''
        Print information contained in the TFitResultPtr r
        
        See:
        https://root.cern.ch/doc/v608/classROOT_1_1Fit_1_1FitResult.html#ac96273476383baba62ca1585b6bd4fda
        https://root.cern.ch/doc/v608/classTFitResult.html
        '''
        self.Verbose("PrintFitResultsGeneral()")
        
        # Define the table format
        lines  = [] 
        align  = "{:<15} {:>20} {:^3} {:<60}"
        header = align.format("Variable", "Value", "", "Description")
        hLine  = "="*120
        lines.append(hLine)
        lines.append(header)
        lines.append(hLine)

        # Get the information
        chi2       = "%0.1f"  % r.Chi2()
        dof        = r.Ndf()
        dofStr     = "%0.0f"  % r.Ndf() 
        redChi2    = r.Chi2()/dof
        redChi2Str = "%0.1f"  % redChi2
        edm        = "%0.1f"  % r.Edm()
        nCalls     = "%0.0f"  % r.NCalls()
        status     = r.Status() # See: https://root.cern.ch/root/html/ROOT__Minuit2__Minuit2Minimizer.html#ROOT__Minuit2__Minuit2Minimizer:Minimize
        fParams    = "%0.0f"  % r.NFreeParameters()
        covMStatus = "%0.0f"  % r.CovMatrixStatus()
        isValid    = r.IsValid()
        if isValid:
            result = "True"
        else:
            result = "False"
        fitRangeStr= "%s-%s"  % (self._fitRangeMin, self._fitRangeMax)
        fitFuncStr = self._fitFunction.getName()
        fitOptsStr = "\"%s\"" % (fitOptions)

        # Construct the table
        lines.append( align.format("Fit Function", fitFuncStr , "", "Custom Fit Function") )            
        lines.append( align.format("Fit Range"   , fitRangeStr, "", "Lower/Upper bounds to fit the function") )
        lines.append( align.format("Fit Options" , fitOptsStr , "", "The fitting options") )
        lines.append( align.format("Chi2/D.O.F"  , redChi2Str , "", "Reduced chi2 (=1 for good fits)") )
        lines.append( align.format("Chi2"        , chi2       , "", "Fit value") )
        lines.append( align.format("D.O.F"       , dofStr     , "", "Number of degrees of freedom (i.e. histo bins)") )
        lines.append( align.format("E.D.M"       , edm        , "", "Expected distance from minimum") )
        lines.append( align.format("# Calls"     , nCalls     , "", "Number of function calls to find minimum") )
        lines.append( align.format("Free Params" , fParams    , "", "Total number of free parameters") )
        lines.append( align.format("Status"      , status     , "", "Minimizer status code") )
        lines.append( align.format("Cov Matrix"  , covMStatus , "", "0=not calculated, 1=approx, 2=made pos def, 3=accurate") )
        lines.append( align.format("IsValid"     , result     , "", "True=Fit successful, False=Fit unsuccessful") )
        lines.append(hLine)
        lines.append("")

        # Print the table
        for l in lines:
            self.Print(l, False)
        return lines

    def PrintFitResultsParameters(self, r, percentageError=True):
        '''
        Print information contained in the TFitResultPtr r
        
        See:
        https://root.cern.ch/doc/v608/classROOT_1_1Fit_1_1FitResult.html#ac96273476383baba62ca1585b6bd4fda
        https://root.cern.ch/doc/v608/classTFitResult.html
        '''
        self.Verbose("PrintFitResultsParameters()")

        # Define the table format
        lines  = [] 
        align  = "{:<10} {:>15} {:^3} {:<15} {:^15} {:^15} {:^15} {:^5} {:^5}"
        if percentageError:
            header = align.format("Variable", "Final Value", "+/-", "Error (%)", "Initian Value", "Low Limit", "Upper Limit", "Bound", "Fixed")
        else:
            header = align.format("Variable", "Final Value", "+/-", "Error", "Initian Value", "Low Limit", "Upper Limit", "Bound", "Fixed")
        hLine  = "="*120
        lines.append(hLine)
        lines.append(header)
        lines.append(hLine)
            
        # For-loop: All parameters
        for i, p in enumerate(r.Parameters()):
            pName     = r.GetParameterName(i)
            pValue    = "%0.5f" % p
            pErrorAbs = "%0.5f" % r.Error(i)
            pErrorPerc= 0
            if p != 0:
                pErrorPerc = "%.2f" % ((r.Error(i)/p)*100)            
            isBound   = r.IsParameterBound(i)
            isFixed   = r.IsParameterFixed(i)
            if self._fitParamInitialValues:
                initValue = self._fitParamInitialValues["default"][i]
            else:
                initValue = "-"

            if self._fitParamLowerLimits:
                lowLimit  = self._fitParamLowerLimits["default"][i]
            else:
                lowLimit  = "-"

            if self._fitParamUpperLimits:
                upLimit   = self._fitParamUpperLimits["default"][i]
            else:
                upLimit   = "-"

            if percentageError:
                pError = pErrorPerc
            else:
                pError = pErrorAbs
            lines.append( align.format(pName, pValue, "+/-", pError, initValue, lowLimit, upLimit, isBound, isFixed) )

        lines.append(hLine)
        lines.append("")
        for l in lines:
            self.Print(l, False)
        return lines

    def PrintFitResultsHistos(self, r, percentageError=False):
        '''
        Print information contained in the TFitResultPtr r
        
        See:
        https://root.cern.ch/doc/v608/classROOT_1_1Fit_1_1FitResult.html#ac96273476383baba62ca1585b6bd4fda
        https://root.cern.ch/doc/v608/classTFitResult.html
        '''
        self.Verbose("PrintFitResultsHistos()")
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
            nRatio     = nHisto / nFit
            nRatioUp   = errorPropagation.errorPropagationForDivision(nHisto, nHistoUp  , nFit, nFitUp)
            nRatioDown = errorPropagation.errorPropagationForDivision(nHisto, nHistoDown, nFit, nFitDown)
        else:
            self.Verbose("Cannot divide by zero. Setting ratio to zero", True)
            nRatio      = 0
            nRatioUp    = 0
            nRatioDown  = 0

        # Calculate Percentage Errors
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

        # Use absolute or percentage errors?
        if percentageError:
            eHistoUp = nHistoUp
            eFitUp   = nFitUp
            eDiffUp  = nDiffUp
            eRatioUp = nRatioUp
        else:
            eHistoUp = nHistoUpP
            eFitUp   = nFitUpP
            eDiffUp  = nDiffUpP
            eRatioUp = nRatioUpP

        # Print the table
        hName  = self.getHisto().GetName()
        lines = getHistoFitTable(hName, nHisto, nHistoUp, nFit, nFitUp, nDiff, nDiffUp, nRatio, nRatioUp)
        for l in lines:
            self.Print(l, False)
        return lines

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
            #elif not "Q" in fitOptions:
            #    fitOptions += " Q" # To suppress output
            if not "S" in fitOptions:
                fitOptions += " S" # To return fit results

            self.Verbose("Create explicitly canvas to get rid of warning message")
            canvas = ROOT.TCanvas()

            if 0:
                self.ChangeShellColour()

            self.Verbose("Fitting function \"%s\" to histogram \"%s\" with fitOptions \"%s\"" % (self._fitFunction.getName(), h.GetName(), fitOptions) ) #fit.GetName()
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

            self.Verbose("Results of fitting function \"%s\" to histogram \"%s\" (binLabel=\"%s\")" % (self._fitFunction.getName(), self._histo.GetName(), self._binLabel), True) #self._name
            self.PrintFitResults(h, fitResultObject, fitOptions)
                    
            self.Verbose("Plotting histogram and fit function")
            self.createFitPlot(h, fit)
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
            self.Verbose("Removing directory tree %s" % (self._plotDirName), True )
            shutil.rmtree(self._plotDirName)
        os.mkdir(self._plotDirName)
        self._requiredTemplateList = []
        self._sources = {}
        self._commentLines = []
        self._qcdNormalization = {}
        self._qcdNormalizationError = {}
        self._ewkNormalization = {}
        self._ewkNormalizationError = {}
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

    def GetQCDNormalization(self, binLabel):
        if binLabel in self._qcdNormalization.keys():
            return self._qcdNormalization[binLabel]
        else:
            raise Exception("Error: _qcdNormalization dictionary has no key \"%s\"! "% (binLabel) )

    def GetQCDNormalizationError(self, binLabel):
        if binLabel in self._qcdNormalizationError.keys():
            return self._qcdNormalizationError[binLabel]
        else:
            raise Exception("Error: _qcdNormalization dictionary has no key \"%s\"! "% (binLabel) )

    def createTemplate(self, name):
        '''
        Creates a QCDNormalizationTemplate and returns it
        '''
        if name in self._templates.keys():
            raise Exception("Error: A template with name '%s' has already been created!"%name)
        q = QCDNormalizationTemplate(name, self._plotDirName)
        self._templates[name] = q
        return q
   
    def plotTemplates(self):
        '''
        Plots shapes of templates - OBSOLETE?
        '''
        self.Verbose("plotTemplates()")
        for index, k in enumerate(self._templates.keys()):
            if self._templates[k].hasHisto():
                self.Verbose("Plotting template %s" % (k), index==0) 
                # self._templates[k].plot() # requires fit-min and fit-max as input parameters
        return

    def resetBinResults(self):
        '''
        Resets bin results
        '''
        for k in self._templates.keys():
            self._templates[k].reset()

    def calculateNormalizationCoefficients(self, dataHisto, fitOptions, FITMIN, FITMAX, **kwargs):
        '''
        Virtual method for calculating the individual norm. coefficients
        '''
        print "calculateQCDNormalization needs to be implemented in parent class"
    
    def calculateCombinedNormalizationCoefficient(self, hQCD, hEWKfakes):
        '''
        Calculates the combined normalization and, if specified, 
        varies it up or down by factor (1+variation)
        '''
        # Obtain counts for QCD and EWK fakes
        lines          = []
        nQCDerror      = ROOT.Double(0.0)
        nQCD           = hQCD.IntegralAndError(1, hQCD.GetNbinsX()+1, nQCDerror)
        nEWKfakesError = ROOT.Double(0.0)
        nEWKfakes      = hEWKfakes.IntegralAndError(1, hEWKfakes.GetNbinsX()+1, nEWKfakesError)
        nTotal         = nQCD + nEWKfakes
        nTotalError    = ROOT.TMath.Sqrt(nQCDerror**2 + nEWKfakesError**2)

        # Calculate w = nQCD / nTotal
        w      = None
        wUp    = None
        wDown  = None
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
        binLabel      = self._templates[self._requiredTemplateList[0]].getBinLabel()
        fakeRate      = None
        fakeRateError = None
        fakeRateUp    = None
        fakeRateDown  = None
        if w != None:
            fakeRate = w*self._qcdNormalization[binLabel] + (1.0-w)*self._ewkNormalization[binLabel]
            fakeRateUp = wUp*self._qcdNormalization[binLabel] + (1.0-wUp)*self._ewkNormalization[binLabel]
            fakeRateDown = wDown*self._qcdNormalization[binLabel] + (1.0-wDown)*self._ewkNormalization[binLabel]
            fakeRateErrorPart1 = errorPropagation.errorPropagationForProduct(w, wError, self._qcdNormalization[binLabel], self._qcdNormalizationError[binLabel])
            fakeRateErrorPart2 = errorPropagation.errorPropagationForProduct(w, wError, self._ewkNormalization[binLabel], self._ewkNormalizationError[binLabel])
            fakeRateError = ROOT.TMath.Sqrt(fakeRateErrorPart1**2 + fakeRateErrorPart2**2)
        self._combinedFakesNormalization[binLabel] = fakeRate
        self._combinedFakesNormalizationError[binLabel] = fakeRateError
        self._combinedFakesNormalizationUp[binLabel] = fakeRateUp
        self._combinedFakesNormalizationDown[binLabel] = fakeRateDown

        # Store all information for later used (write to file)
        self._commentLines.extend(lines)

        # Print output and store comments
        for l in lines:
            print l
        
    def writeNormFactorFile(self, filename, opts):
        '''
        Save the fit results for QCD and EWK.

        The results will are stored in a python file starting with name:
        "QCDInvertedNormalizationFactors_" + moduleInfoString

        The script also summarizes warnings and errors encountered:
        - Green means deviation from normal is 0-3 %,
        - Yellow means deviation of 3-10 %, and
        - Red means deviation of >10 % (i.e. something is clearly wrong).
        
        If necessary, do adjustments to stabilize the fits to get rid of the errors/warnings. 
        The first things to work with are:
        a) Make sure enough events are in the histograms used
        b) Adjust fit parameters and/or fit functions and re-fit results
        
        Move on only once you are pleased with the normalisation coefficients
        '''
        s = ""
        s += "# Generated on %s\n"% datetime.datetime.now().ctime()
        s += "# by %s\n" % os.path.basename(sys.argv[0])
        s += "\n"
        s += "import sys\n"
        s += "\n"
        s += "def QCDInvertedNormalizationSafetyCheck(era, searchMode, optimizationMode):\n"
        s += "    validForEra        = \"%s\"\n" % opts.dataEra
        s += "    validForSearchMode = \"%s\"\n" % opts.searchMode
        s += "    validForOptMode    = \"%s\"\n" % opts.optMode
        s += "    if not era == validForEra:\n"
        s += "        raise Exception(\"Error: inconsistent era, normalisation factors valid for\",validForEra,\"but trying to use with\",era)\n"
        s += "    if not searchMode == validForSearchMode:\n"
        s += "        raise Exception(\"Error: inconsistent search mode, normalisation factors valid for\",validForSearchMode,\"but trying to use with\",searchMode)\n"
        s += "    if not optimizationMode == validForOptMode:\n"
        s += "        raise Exception(\"Error: inconsistent optimization mode, normalisation factors valid for\",validForOptMode,\"but trying to use with\",optimizationMode)\n"
        s += "    return"
        s += "\n"

        s += "QCDNormalization = {\n"
        for k in self._qcdNormalization:
            #print "key = %s, value = %s" % (k, self._qcdNormalization[k])
            s += '    "%s": %f,\n'%(k, self._qcdNormalization[k])
        s += "}\n"

        s += "EWKNormalization = {\n"
        for k in self._ewkNormalization:
            #print "key = %s, value = %s" % (k, self._ewkNormalization[k])
            s += '    "%s": %f,\n'%(k, self._ewkNormalization[k])
        s += "}\n"

        s += "QCDPlusEWKNormalization = {\n"
        for k in self._combinedFakesNormalization:
            # print "key = %s, value = %s" % (k, self._combinedFakesNormalization[k])
            s += '    "%s": %f,\n'%(k, self._combinedFakesNormalization[k])
        s += "}\n"
        s += "\n"

        # s += "QCDPlusEWKFakeTausNormalizationSystFakeWeightingVarDown = {\n"
        # for k in self._combinedFakesNormalizationDown:
        #     print "key = %s, value = %s" % (k, self._combinedFakesNormalizationDown[k])
        #     s += '    "%s": %f,\n'%(k, self._combinedFakesNormalizationDown[k])
        # s += "}\n"

        # s += "QCDPlusEWKNormalizationSystFakeWeightingVarUp = {\n"
        # for k in self._combinedFakesNormalizationUp:
        #     print "key = %s, value = %s" % (k, self._combinedFakesNormalizationUp[k])
        #     s += '    "%s": %f,\n'%(k, self._combinedFakesNormalizationUp[k])
        # s += "}\n"
        # s += "# Log of fake rate calculation:\n"

        self.Verbose("Writing results in file %s" % filename, True)
        fOUT = open(filename,"w")
        fOUT.write(s)
        fOUT.write("'''\n")
        for l in self._commentLines:
            fOUT.write(l + "\n")
        fOUT.write("'''\n")
        fOUT.close()

        msg = "Results written in file %s" % filename        
        self.Print(ShellStyles.SuccessLabel() + msg + ShellStyles.NormalStyle(), True)

        # FIXME: The two functions below currenty do not work (KeyError: 'Inclusive')
        if 0:
            self._generateCoefficientPlot() 
            self._generateDQMplot()
        return

    def _generateCoefficientPlot(self):
        '''
        This probably is needed in the case the measurement is done in
        bins of a correlated quantity (e.g. pT in the case of inverted tau isolation
        '''
        def makeGraph(markerStyle, color, binList, valueDict, upDict, downDict):
            g = ROOT.TGraphAsymmErrors(len(binList))
            for i in range(len(binList)):
                g.SetPoint(i, i+0.5, valueDict[binList[i]])
                g.SetPointEYhigh(i, upDict[binList[i]])
                g.SetPointEYlow(i, downDict[binList[i]])
            g.SetMarkerSize(1.6)
            g.SetMarkerStyle(markerStyle)
            g.SetLineColor(color)
            g.SetLineWidth(3)
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
        gQCD  = makeGraph(24, ROOT.kCyan  , keyList, self._qcdNormalization, self._qcdNormalizationError, self._qcdNormalizationError)
        gFake = makeGraph(27, ROOT.kYellow, keyList, self._ewkNormalization, self._ewkNormalizationError, self._ewkNormalizationError)
        upError   = {}
        downError = {}
        for k in keys:
            # print k
            upError[k]   = self._combinedFakesNormalizationUp[k] - self._combinedFakesNormalization[k]
            downError[k] = self._combinedFakesNormalization[k] - self._combinedFakesNormalizationDown[k]
        gCombined = makeGraph(20, ROOT.kBlack, keyList, self._combinedFakesNormalization, upError, downError)

        # Make plot
        hFrame = ROOT.TH1F("frame","frame",len(keyList),0,len(keyList))
        for i in range(len(keyList)):
            binLabelText = getFormattedBinLabelString(keyList[i])
            hFrame.GetXaxis().SetBinLabel(i+1,binLabelText)

        hFrame.SetMinimum(0.05)
        hFrame.SetMaximum(0.5)                 
        hFrame.GetYaxis().SetTitle("Normalization coefficient")
        hFrame.GetXaxis().SetLabelSize(20)
        c = ROOT.TCanvas()
        c.SetLogy()
        c.SetGridx()
        c.SetGridy()

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

    def _generateDQMplot(self):
        '''
        Create a DQM style plot
        '''
        # Check the uncertainties on the normalization factors
        for k in self._dqmKeys.keys():
            self._addDqmEntry(k, "norm.coeff.uncert::QCD" , self._qcdNormalizationError[k], 0.03, 0.10)
            self._addDqmEntry(k, "norm.coeff.uncert::fake", self._ewkNormalizationError[k], 0.03, 0.10)
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
        return

    def _checkInputValidity(self, templatesToBeFitted):
        '''
        Checks that input is valid
        '''
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
        return

    def _fitTemplates(self, fitOptions):
        '''
        Fits templates
        '''
        for key in self._templates.keys():
            item = self._templates[key]
            if item != None and item.isFittable():
                item.doFit(fitOptions=fitOptions, createPlot=True)
                self._commentLines.extend(item.getInfo())
        return

    def _makeFinalFitPlot(self, binLabel, histogramDictionary={}, yLog=True):
        '''
        Helper method to plot fitted templates
        
        called from parent class when calculating norm.coefficients
        '''
        # Customisation
        plot   = plots.PlotBase()
        units  = "GeV/c^{2}"
        xTitle = "m_{jjb} (%s)" % units
        yTitle = "" # filled below
        fName  = self._plotDirName + "/finalFit_" + binLabel
        if yLog:
            fName += "_log"
            yMaxFactor = 4.0
        else:
            yMaxFactor = 1.1
        
        # Disable fit/statistics box
        ROOT.gStyle.SetOptFit(0)
        ROOT.gStyle.SetOptStat(0)
        
        # For-loop: All key-histogram pairs
        for k in histogramDictionary.keys():
            objKey    = k
            objHisto  = histogramDictionary[k]
            histoName = objHisto.GetName()
            
            # Sanity check
            if not (isinstance(objHisto, ROOT.TH1) or isinstance(objHisto, ROOT.TF1)):
                print histogramDictionary
                raise Exception("Error: Expected a dictionary of histograms")

            # Append object for plotting
            plot.histoMgr.appendHisto(histograms.Histo(objHisto, objKey))
            if isinstance(objHisto, ROOT.TH1):
                # Finalise y-title
                yTitle = "Events / %.0f %s" % (objHisto.GetBinWidth(0), units)
                
                if "data" in histoName.lower():
                    plot.histoMgr.setHistoDrawStyle(histoName  , "AP")
                    plot.histoMgr.setHistoLegendStyle(histoName, "P")
                    
        # Create frame
        myOpts = {"ymin": 1e-5, "ymaxfactor": yMaxFactor}
        plot.setLegend(createLegend())
        plot.createFrame(fName, opts=myOpts)
        plot.getFrame().GetXaxis().SetTitle(xTitle)
        plot.getFrame().GetYaxis().SetTitle(yTitle)
        plot.getFrame().GetXaxis().SetRangeUser(0.0*self._fitRangeMin, 1.1*self._fitRangeMax)
        
        # Add text
        histograms.addStandardTexts(cmsTextPosition="outframe")
        # histograms.addText(0.72, 0.8, getFormattedBinLabelString(binLabel))

        # Cut lines/boxes
        if yLog: # for unknown reason doesn't work for linear scale
            _kwargs1 = {"lessThan": True}
            _kwargs2 = {"lessThan": False}
            plot.addCutBoxAndLine(cutValue=self._fitRangeMin, fillColor=ROOT.kGray, box=False, line=True, **_kwargs1)
            plot.addCutBoxAndLine(cutValue=self._fitRangeMax, fillColor=ROOT.kGray, box=False, line=True, **_kwargs2)
        
        # Draw and save plot
        plot.getPad().SetLogy(yLog)
        plot.draw()        
        plot.save(formats=[".png", ".pdf", ".C"])
        return

    def _getSanityCheckTextForFractions(self, dataTemplate, binLabel, saveToComments=False):
        '''
        Helper method to be called from parent class when calculating norm.coefficients
        
        NOTE: Should one divide the fractions with dataTemplate.getFittedParameters()[0] ? 
              Right now not because the correction is so small.
        '''
        self.Verbose("_getSanityCheckTextForFractions()", True)
        
        # Get variables
        label         = "QCD"
        fraction      = dataTemplate.getFittedParameters()[1]
        fractionError = dataTemplate.getFittedParameterErrors()[1]
        nBaseline     = self._templates["%s_Baseline" % label].getNeventsFromHisto(False)
        nCalculated   = fraction * dataTemplate.getNeventsFromHisto(False)

        if nCalculated > 0:
            ratio = nBaseline / nCalculated
        else:
            ratio = 0
        lines = []
        lines.append("Fitted %s fraction: %f +- %f" % (label, fraction, fractionError))
        lines.append("Sanity check: ratio = %.3f: baseline = %.1f vs. fitted = %.1f" % (ratio, nBaseline, nCalculated))

        # Store all information for later used (write to file)
        if saveToComments:
            self._commentLines.extend(lines)
        return lines

    
    def _getSanityCheckTextForFit(self, binLabel, saveToComments=False):
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
                name       = item.getName()
                nHisto     = item.getNeventsFromHisto(False)
                nHistoUp   = item.getNeventsErrorFromHisto(False)
                nHistoDown = item.getNeventsErrorFromHisto(False)
                nFit       = item.getNeventsFromFit()
                nFitUp     = item.getNeventsTotalErrorFromFit()[0]
                nFitDown   = item.getNeventsTotalErrorFromFit()[1]
                nDiff      = nHisto-nFit
                nDiffUp    = errorPropagation.errorPropagationForSum(nHisto, nHistoUp  , nFit, nFitUp)
                nDiffDown  = errorPropagation.errorPropagationForSum(nHisto, nHistoDown, nFit, nFitDown)
                nRatio     = 0
                nRatioUp   = 0
                nRatioDown = 0
                if item.getNeventsFromFit()>0:
                    nRatio     = nHisto / nFit
                    nRatioUp   = errorPropagation.errorPropagationForDivision(nHisto, nHistoUp  , nFit, nFitUp)
                    nRatioDown = errorPropagation.errorPropagationForDivision(nHisto, nHistoDown, nFit, nFitDown)
                else:
                    self.Print("Cannot divide by zero. Setting ratio to zero", True)

                # Define the table format
                lines.extend(getHistoFitTable(name, nHisto, nHistoUp, nFit, nFitUp, nDiff, nDiffUp, nRatio, nRatioUp))
                self._addDqmEntry(binLabel, "TmplFit::%s"%item.getName(), nRatio-1, 0.03, 0.10)

        # Store all information for later used (write to file)
        if saveToComments:
            self._commentLines.extend(lines)
        return lines

    def _checkOverallNormalization(self, template, binLabel, saveToComments=False):
        '''
        Helper method to be called from parent class when calculating norm.coefficients
        '''
        self.Verbose("_checkOverallNormalization()")
        
        # Calculatotions
        value = template.getFittedParameters()[0]
        error = template.getFittedParameterErrors()[0]

        # Definitions
        lines = []
        lines.append("The fitted overall normalization factor for purity is: (should be 1.0)")
        lines.append("NormFactor = %f +/- %f" % (value, error))

        self._addDqmEntry(binLabel, "OverallNormalization(par0)", value-1.0, 0.03, 0.10)

        # Store all information for later used (write to file)
        if saveToComments:
            self._commentLines.extend(lines)
        return lines
    
    ## Helper method to be called from parent class when calculating norm.coefficients
    def _getResultOutput(self, binLabel):
        lines = []
        lines.append("   Normalization factor (QCD): %f +- %f"%(self._qcdNormalization[binLabel], self._qcdNormalizationError[binLabel]))
        lines.append("   Normalization factor (EWK fake taus): %f +- %f"%(self._ewkNormalization[binLabel], self._ewkNormalizationError[binLabel]))
        lines.append("   Combined norm. factor: %f +- %f"%(self._combinedFakesNormalization[binLabel], self._combinedFakesNormalizationError[binLabel]))

        # Store all information for later used (write to file)
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
        return

    def calculateNormalizationCoefficients(self, dataHisto, fitOptions, FITMIN, FITMAX, **kwargs):
        '''
        '''
        #===== Save options
        self._fitRangeMin = FITMIN
        self._fitRangeMax = FITMAX
        self._fitOptions  = fitOptions

        #===== Define the fit templates 
        qcdTemplate = self._templates["QCD_Inverted"]
        ewkTemplate = self._templates["EWKInclusive_Baseline"]

        #===== Sanity ckeck
        self.Verbose("Check input validity of fit templates", True)
        self._checkInputValidity([qcdTemplate, ewkTemplate])

        #===== Fit the defined fit templates with custom fit options
        self.Verbose("Fit the templates", True)
        self._fitTemplates(fitOptions)
        
        #===== Create a temporary template for data
        self.Verbose("Creating a temporary template for data", True)
        dataTemplate = QCDNormalizationTemplate("data", self._plotDirName)
        binLabel     = self._templates[self._requiredTemplateList[0]].getBinLabel()
        dataTemplate.setHistogram(dataHisto, binLabel)
        dataTemplate.plot(FITMIN, FITMAX)

        #===== Create the final fit functions (QCD + EWK)        
        finalFitFunc = FitFunction("FitDataWithQCDAndEWK",
                                   fitFunctionQCD = qcdTemplate.getFitFunction(), parQCD = qcdTemplate.getFittedParameters(), normQCD = 1.0,
                                   fitFunctionEWK = ewkTemplate.getFitFunction(), parEWK = ewkTemplate.getFittedParameters(), normEWK = 1.0)
        dataTemplate.setFitter(finalFitFunc, FITMIN, FITMAX)

        #===== Do fit to data
        self.Verbose("Fitting the two templates to the \"Baseline Data\"", True)
        dataTemplate.setDefaultFitParam(defaultInitialValue=[1.0, 0.5, 0.5], defaultLowerLimit=[0.0, 0.0, 0.0], defaultUpperLimit=[10.0, 1.0, 1.0])
        dataTemplate.doFit(fitOptions)
        self._commentLines.extend(dataTemplate.getInfo())
        
        #===== Plot fitted functions
        dataHisto.SetLineColor(ROOT.kBlack)

        dataFit = dataTemplate.obtainFittedFunction(1.0, FITMIN, FITMAX)
        dataFit.SetLineColor(ROOT.kBlue)
        dataFit.SetLineStyle(ROOT.kSolid)
        dataFit.SetLineWidth(3)

        qcdFit = qcdTemplate.obtainFittedFunction(dataTemplate.getFittedParameters()[1], FITMIN, FITMAX)
        qcdFit.SetLineColor(ROOT.kOrange)
        qcdFit.SetLineWidth(3)
        qcdFit.SetLineStyle(ROOT.kDashed)

        histoDict = {dataHisto.GetName(): dataHisto, "Data Fit" : dataFit, "QCD Template": qcdFit}
        self._makeFinalFitPlot(binLabel, histoDict, yLog=True)
        self._makeFinalFitPlot(binLabel, histoDict, yLog=False)

        #==== Store results in list
        self.Verbose("Sanity Check: Text for Fit")
        fitSanityLines = self._getSanityCheckTextForFit(binLabel, saveToComments=False)

        self.Verbose("Sanity Check: Text for Fractions")
        fractionSanityLines = self._getSanityCheckTextForFractions(dataTemplate, binLabel, saveToComments=False)

        self.Verbose("Sanity Check: Overall Normalization", False)
        normalisationSanityLines = self._checkOverallNormalization(dataTemplate, binLabel, saveToComments=False) 

        self.Print("Printing final results", True)
        lines = self._storeNormFactors(dataTemplate, binLabel) 

        #==== Store all information for later used (write to file)
        self._commentLines.extend(lines)

        #==== Print final results
        #print colors.GREEN
        for line in lines:
            self.Print(line)
        #print colors.WHITE
        return

    
    def _storeNormFactors(self, dataTemplate, binLabel):
        '''
        Store thenNormalization factor for QCD (from fit) and 
        associated error.
        '''
        #===== Normalization factor for QCD (from fit)
        nDataBaseline         = dataTemplate.getNeventsFromHisto(False)
        nDataBaselineError    = dataTemplate.getNeventsErrorFromHisto(False) # poisson error = ROOT.TMath.Sqrt(nDataBaseline)
        nDataFitBaseline      = dataTemplate.getFittedParameters()[1]
        nDataFitBaselineError = dataTemplate.getFittedParameterErrors()[1]
        nQCDInverted          = self._templates["QCD_Inverted"].getNeventsFromHisto(False)
        nQCDInvertedError     = self._templates["QCD_Inverted"].getNeventsErrorFromHisto(False)
        nQCDBaseline          = self._templates["QCD_Baseline"].getNeventsFromHisto(False) #ALEX-IRO-FIXME  nQCDBaseline = nQCDInverted
        nQCDBaselineError     = self._templates["QCD_Baseline"].getNeventsErrorFromHisto(False)
        nQCDFitBaseline       = dataTemplate.getFittedParameters()[1]*nDataBaseline
        nQCDFitBaselineError  = errorPropagation.errorPropagationForProduct(nDataFitBaseline, nDataFitBaselineError, nDataBaseline, nDataBaselineError)
        nQCDBaselineRatio     = nQCDBaseline/nQCDFitBaseline
        nQCDBaselineRatioError= errorPropagation.errorPropagationForDivision(nQCDBaseline, nQCDBaselineError, nQCDFitBaseline, nQCDFitBaselineError)
        qcdNormFactor         = nQCDFitBaseline / nQCDInverted
        qcdNormFactorError    = errorPropagation.errorPropagationForDivision(nQCDFitBaseline, nQCDFitBaselineError, nQCDInverted, nQCDInvertedError)

        #===== Normalization factor for EWK fakes (from MC)
        ewkFakesNormFactor      = None
        ewkFakesNormFactorError = None
        nFakeBaseline           = self._templates["EWKFakeB_Baseline"].getNeventsFromHisto(False)
        nFakeBaselineError      = self._templates["EWKFakeB_Baseline"].getNeventsErrorFromHisto(False)
        nFakeInverted           = self._templates["EWKFakeB_Inverted"].getNeventsFromHisto(False)
        nFakeInvertedError      = self._templates["EWKFakeB_Inverted"].getNeventsErrorFromHisto(False)
        if nFakeInverted > 0.0:
            ewkFakesNormFactor      = nFakeBaseline / nFakeInverted
            ewkFakesNormFactorError = errorPropagation.errorPropagationForDivision(nFakeBaseline, nFakeBaselineError, nFakeInverted, nFakeInvertedError)

        # Store the norm factors and their errors (binLabel = "Inclusive")
        self._qcdNormalization[binLabel]      = qcdNormFactor
        self._qcdNormalizationError[binLabel] = qcdNormFactorError
        self._ewkNormalization[binLabel]      = ewkFakesNormFactor
        self._ewkNormalizationError[binLabel] = ewkFakesNormFactorError

        # Additional Sanity checks
        nBkgBaseline       = nQCDFitBaseline + nFakeBaseline
        nBkgBaselineError  = errorPropagation.errorPropagationForSum(nQCDFitBaseline, nQCDFitBaselineError, nFakeBaseline, nFakeBaselineError)
        nDiffBaseline      = (nDataBaseline)-(nBkgBaseline)
        nDiffBaselineError = errorPropagation.errorPropagationForSum(nDataBaseline, nDataBaselineError, nBkgBaseline, nBkgBaselineError)
        nRatioBaseline     = (nDataBaseline)/(nBkgBaseline)
        nRatioBaselineError= errorPropagation.errorPropagationForDivision(nDataBaseline, nDataBaselineError, nBkgBaseline, nBkgBaselineError)

        print "QCDNormalization.py: XENIOS"
        # nRatioInverted     = (nDataInverted)/(nBkgInverted) #
        # nRatioInvertedError= errorPropagation.errorPropagationForDivision(nDataInverted, nDataInvertedError, nBkgInverted, nBkgBaselineError)
        qcdPurity          = nQCDFitBaseline/nDataBaseline
        qcdPurityError     = errorPropagation.errorPropagationForDivision(nQCDFitBaseline, nQCDFitBaselineError, nDataBaseline, nDataBaselineError)
        ewkPurity          = nFakeBaseline/nDataBaseline
        ewkPurityError     = errorPropagation.errorPropagationForDivision(nFakeBaseline, nFakeBaselineError, nDataBaseline, nDataBaselineError)

        # Definitions
        lines  = []
        #lines  = ["{:^100}".format("FINAL RESULTS")]
        align  = "{:<14} {:^10} {:>10} {:^3} {:<10} {:<10} {:<20}"
        header = align.format("Sample", "Region", "Value", "+/-", "Error", "Source", "Comment")
        hLine  = "="*100
        lines.append(hLine)
        lines.append(header)
        lines.append(hLine)
        lines.append(align.format("Data"      , "Baseline", "%.1f" % nDataBaseline     , "+/-", "%.1f" % nDataBaselineError     , "Histo"    , "Signal Region") )
        lines.append(align.format("Data"      , "Baseline", "%.5f" % nDataFitBaseline  , "+/-", "%.5f" % nDataFitBaselineError  , "Fit"      , "Fraction of QCD Events") )
        lines.append(align.format("QCD"       , "Baseline", "%.1f" % nQCDBaseline      , "+/-", "%.1f" % nQCDBaselineError      , "Histo"    , "QCD = Data -EWK MC") )
        lines.append(align.format("QCD"       , "Baseline", "%.1f" % nQCDFitBaseline   , "+/-", "%.1f" % nQCDFitBaselineError   , "Fit"      , "QCD Estimate (Fit)") )
        lines.append(align.format("QCD/QCDFit", "Baseline", "%.3f" % nQCDBaselineRatio , "+/-", "%.3f" % nQCDBaselineRatioError , "Composite", "QCD / QCD Estimate") )
        lines.append(align.format("EWK"       , "Baseline", "%.1f" % nFakeBaseline     , "+/-", "%.1f" % nFakeBaselineError     , "Histo"    , "EWK Estimate (MC)") )
        lines.append(align.format("QCD"       , "Inverted", "%.1f" % nQCDInverted      , "+/-", "%.1f" % nQCDInvertedError      , "Histo"    , "Divide \"QCD Estimate Baseline (Fit)\" for R=\"NormFactor\"") )
        # lines.append(align.format("EWK"       , "Inverted", "%.1f" % nFakeInverted     , "+/-", "%.1f" % nFakeInvertedError     , "Histo"    , "Divide \"EWK Baseline\" for \"NormFactor\"") )
        lines.append(align.format("QCD"       , "Inverted", "%.6f" % qcdNormFactor     , "+/-", "%.6f" % qcdNormFactorError     , "Fit"      , "R=\"NormFactor\" to \"Baseline\" Region") )
        # lines.append(align.format("EWK"       , "Inverted", "%.6f" % ewkFakesNormFactor, "+/-", "%.6f" % ewkFakesNormFactorError, "Histo"    , "R=\"NormFactor\" to \"Baseline\" Region") )
        # lines.append(align.format("Bkg"       , "Baseline", "%.1f" % nBkgBaseline      , "+/-", "%.1f" % nBkgBaselineError      , "Composite", "QCD Fit + EWK MC") )
        # lines.append(align.format("Data-Bkg"  , "Baseline", "%.1f" % nDiffBaseline     , "+/-", "%.1f" % nDiffBaselineError     , "Composite", "Sanity Check") )
        # lines.append(align.format("Data/Bkg"  , "Baseline", "%.3f" % nRatioBaseline    , "+/-", "%.3f" % nRatioBaselineError    , "Composite", "Sanity Check") )
        # lines.append(align.format("QCD Purity", "Baseline", "%.2f" % (qcdPurity)       , "+/-", "%.2f" % qcdPurityError         , "Composite", "Sanity Check") )
        # lines.append(align.format("EWK Purity", "Baseline", "%.2f" % (ewkPurity)       , "+/-", "%.2f" % ewkPurityError         , "Composite", "Sanity Check") )
        lines.append(hLine)
        lines.append("")
        return lines
