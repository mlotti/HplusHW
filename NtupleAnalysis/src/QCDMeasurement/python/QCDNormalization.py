## \package QCDNormalization
#############################################################################
#
# This package contains the tools for calculating 
# the normalization factors from QCDMeasurementAnalysis
#
#############################################################################

import ROOT
ROOT.gROOT.SetBatch(True)
import HiggsAnalysis.NtupleAnalysis.tools.fitHelper as fitHelper
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.styles as styles
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux
import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.errorPropagation as errorPropagation
import os
import sys
import datetime

## Container class for fit functions
class FitFunction:
    def __init__(self, functionName, **kwargs):
        self._functionName = functionName
        self._args = kwargs
        self._additionalNormFactor = 1.0
        
        if not hasattr(self, functionName):
            raise Exception("Error: FitFunction '%s' is unknown!"%functionName)
        nParams = {
            "Linear": 2,
            "ErrorFunction": 2,
            "ExpFunction": 2,
            "Gaussian": 3,
            "DoubleGaussian": 6,
            "SumFunction": 5,
            "RayleighFunction": 2,
            "QCDFunction": 7,
            "EWKFunction": 4,
            "EWKFunctionInv": 4,
            "QCDEWKFunction": 7,
            "QCDFunctionFixed": 8,
            "FitDataWithQCDAndFakesAndGenuineTaus": 3,
            "FitDataWithFakesAndGenuineTaus": 2,
        }
        self._nParam = nParams[functionName]
    
    def clone(self):
        f = FitFunction(self._functionName, **self._args)
        f.setAdditionalNormalization(self._additionalNormFactor)
        return f
    
    def setAdditionalNormalization(self, factor):
        self._additionalNormFactor = factor
    
    def __call__(self, x, par, **kwargs):
        args = {}
        for k in self._args.keys():
            args[k] = self._args[k]
        for k in kwargs:
            args[k] = kwargs[k]
        return getattr(self, self._functionName)(x, par, **args)

    def getNParam(self):
        return self._nParam

    #===== Primitive functions
    def Linear(self,x,par):
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
                
    #===== Composite functions for template fits
    def QCDFunction(self,x,par,norm):
        return self._additionalNormFactor*norm*(self.RayleighFunction(x,par,1)+par[2]*ROOT.TMath.Gaus(x[0],par[3],par[4],1)+par[5]*ROOT.TMath.Exp(-par[6]*x[0]))

    def EWKFunction(self,x,par,boundary,norm=1,rejectPoints=0):
        if x[0] < boundary:
            return self._additionalNormFactor*norm*par[0]*ROOT.TMath.Gaus(x[0],par[1],par[2],1)
        C = self._additionalNormFactor*norm*par[0]*ROOT.TMath.Gaus(boundary,par[1],par[2],1)*ROOT.TMath.Exp(boundary*par[3])
        return C*ROOT.TMath.Exp(-x[0]*par[3])

    def EWKFunctionInv(self,x,par,boundary,norm=1,rejectPoints=0):
        #if not rejectPoints == 0:
            #if (x[0] > 230 and x[0] < 290):
                #ROOT.TF1.RejectPoint()
                #return 0
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
    ## QCD, fake taus, and genuine taus as separate templates
    def FitDataWithQCDAndFakesAndGenuineTaus(self, x, par,
            QCDFitFunction, parQCD, QCDnorm,
            EWKFakeTausFitFunction, parEWKFakeTaus, EWKFakeTausNorm,
            EWKGenuineTausFitFunction, parEWKGenuineTaus, EWKGenuineTausNorm):
        nQCD =            QCDFitFunction(x, parQCD, norm=QCDnorm)
        nEWKFakeTaus =    EWKFakeTausFitFunction(x, parEWKFakeTaus, norm=EWKFakeTausNorm)
        nEWKGenuineTaus = EWKGenuineTausFitFunction(x, parEWKGenuineTaus, norm=EWKGenuineTausNorm) 
        return par[0]*(par[1]*nQCD + par[2]*nEWKFakeTaus + (1.0 - par[1] - par[2])*nEWKGenuineTaus)

    ## QCD and fake tau templates as one inclusive template
    def FitDataWithFakesAndGenuineTaus(self, x, par,
            QCDAndFakesFitFunction, parQCDAndFakes, QCDAndFakesnorm,
            EWKGenuineTausFitFunction, parEWKGenuineTaus, EWKGenuineTausNorm):
        nQCDAndFakes =    QCDAndFakesFitFunction(x, parQCDAndFakes, norm=QCDAndFakesnorm)
        nEWKGenuineTaus = EWKGenuineTausFitFunction(x, parEWKGenuineTaus, norm=EWKGenuineTausNorm) 
        return par[0]*(par[1]*nQCDAndFakes + (1.0 - par[1])*nEWKGenuineTaus)


## Modify bin label string
def getModifiedBinLabelString(binLabel):
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

## Template holder for QCD measurement normalization
class QCDNormalizationTemplate:
    def __init__(self, name, quietMode=False):
        self._name = name
        self._fitFunction = None
        self._fitKwargs = None
        self._fitRangeMin = None
        self._fitRangeMax = None
        self._fitParamInitialValues = {}
        self._fitParamLowerLimits = {}
        self._fitParamUpperLimits = {}
        self._quietMode = quietMode
        self.reset()

    ## Get name
    def getName(self):
        return self._name

    ## Set fit function and fit range
    def setFitter(self, fitFunction, fitRangeMin, fitRangeMax):
        self._fitFunction = fitFunction
        self._fitRangeMin = fitRangeMin
        self._fitRangeMax = fitRangeMax
        if not isinstance(fitFunction, FitFunction):
            raise Exception("Error: the fit function needs to be a FitFunction class!")
        if fitRangeMax < fitRangeMin:
            raise Exception("Error: fit range max value is smaller than the min value!")

    ## Call before setting the histogram and fitting
    def reset(self):
        self._binLabel = None
        self._nEventsFromFit = None
        self._nEventsTotalErrorFromFitUp = None
        self._nEventsTotalErrorFromFitDown = None
        self._histo = None
        self._normalizationFactor = None
        self._fitParameters = None
        self._fitParErrors = None
        

    ## Returns true if a histogram has been provided
    def hasHisto(self):
        return self._histo != None
    
    ## Returns the bin label
    def getBinLabel(self):
        return self._binLabel

    ## Returns the normalization factor for normalizing the histogram contents to Nevents (histogram is stored with area = 1)
    def getNormalizationFactor(self):
        return self._normalizationFactor
    
    ## Returns true if a fit function has been provided
    def isFittable(self):
        return self._fitFunction != None

    ## Returns the fit function object
    def getFitFunction(self):
        return self._fitFunction
    
    ## Returns the list of parameters from the fit (returns None if not fitted)
    def getFittedParameters(self):
        return self._fitParameters

    ## Returns the list of parameter errors from the fit (returns None if not fitted)
    def getFittedParameterErrors(self):
        return self._fitParErrors

    ## Prints the parameter settings (for debugging or info)
    def printFitParamSettings(self, binLabel=None):
        keys = self._fitParamInitialValues.keys()
        for k in self._fitParamLowerLimits.keys():
            if not k in keys:
                keys.append(k)
        keys.sort()
        if binLabel != None:
            keys = [binLabel]
        else:
            print ""
        print "... Fit parameter settings for '%s': (initial value / low bound / high bound)"%self._name
        for k in keys:
            s = "      %s: "%k
            if k in self._fitParamInitialValues.keys():
                s += " [%s] "%", ".join("%f" % x for x in self._fitParamInitialValues[k])
            elif "default" in self._fitParamInitialValues.keys():
                s += " [%s] (default) "%", ".join("%f" % x for x in self._fitParamInitialValues["default"])
            else:
                s += " (no setting) "
            if k in self._fitParamLowerLimits.keys():
                s += "/ [%s] "%", ".join("%f" % x for x in self._fitParamLowerLimits[k])
                s += "/ [%s] "%", ".join("%f" % x for x in self._fitParamUpperLimits[k])
            elif "default" in self._fitParamLowerLimits.keys():
                s += "/ [%s] (default) "%", ".join("%f" % x for x in self._fitParamLowerLimits["default"])
                s += "/ [%s] (default) "%", ".join("%f" % x for x in self._fitParamUpperLimits["default"])
            else:
                s += "/ (none) / (none)"
            print s
        if binLabel == None:
            print ""

    ## Prints the results
    def printResults(self):
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

    ## Returns the number of events obtained from the histogram
    # \param includeOverflowBins  if true, then range includes the under/overflow bins
    def getNeventsFromHisto(self, includeOverflowBins):
        if self._histo == None:
            raise Exception("Error: Please call the the 'setHistogram(...)' method first!")
        if includeOverflowBins:
            return self._histo.Integral(0, self._histo.GetNbinsX()+2)*self._normalizationFactor
        else:
            return self._histo.Integral(1, self._histo.GetNbinsX()+1)*self._normalizationFactor

    ## Returns the absolute uncertainty in the number of events obtained from the histogram
    # \param includeOverflowBins  if true, then range includes the under/overflow bins
    def getNeventsErrorFromHisto(self, includeOverflowBins):
        if self._histo == None:
            raise Exception("Error: Please call the the 'setHistogram(...)' method first!")
        integralError = ROOT.Double(0.0)
        if includeOverflowBins:
            a = self._histo.IntegralAndError(0, self._histo.GetNbinsX()+2, integralError)
        else:
            a = self._histo.IntegralAndError(1, self._histo.GetNbinsX()+1, integralError)
        return float(integralError*ROOT.TMath.Sqrt(self._normalizationFactor))
    
    ## Returns the number of events obtained from the fit
    #  The range is the range of the histogram; under/overflow bins are ignored!
    def getNeventsFromFit(self):
        if self._fitParameters == None:
            if self._fitFunction == None:
                raise Exception("Error: Please call the the 'setFitter(...)' method first!")
            else:
                raise Exception("Error: Please call the 'doFit(...)' method first!")
        return self._nEventsFromFit
    
    ## Returns the [plus, minus] absolute uncertainty in number of events obtained from the fit
    #  The range is the range of the histogram; under/overflow bins are ignored!
    def getNeventsTotalErrorFromFit(self):
        if self._fitParameters == None:
            if self._fitFunction == None:
                raise Exception("Error: Please call the the 'setFitter(...)' method first!")
            else:
                raise Exception("Error: Please call the 'doFit(...)' method first!")
        return [self._nEventsTotalErrorFromFitUp, self._nEventsTotalErrorFromFitDown]

    ## Returns the fit results
    def getFitResults(self):
        return self._fitParameters
    
    ## Returns a TF1 of the fitted function
    def obtainFittedFunction(self, normalizationFactor, FITMIN, FITMAX):
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
    
    ## Call once for every bin
    def setHistogram(self, histogram, binLabel):
        self._histo = histogram
        self._binLabel = binLabel
        # Convert negative bins to zero but leave errors intact
        for k in range(0, self._histo.GetNbinsX()+2):
            if self._histo.GetBinContent(k) < 0.0:
                print "template '%s': converted in bin %d a negative value (%f) to zero."%(self._name, k, self._histo.GetBinContent(k))
                self._histo.SetBinContent(k, 0.0)
                self._histo.SetBinError(k, 1.0)
        # Format bin label string
        self._binLabel = getModifiedBinLabelString(binLabel)
        # Calculate normalization factor and store the histogram normalized as area = 1
        integral = self._histo.Integral()
        if integral == 0.0:
            self._normalizationFactor = 1.0
        else:
            self._normalizationFactor = integral
            self._histo.Scale(1.0 / self._normalizationFactor)
        
    ## Make a plot of the histogram
    def plot(self):
        if self._histo == None:
            raise Exception("Error: Please provide first the histogram with the 'setHistogram' method")
        if self._histo.GetEntries() == 0:
            print "Skipping plot for '%s' because it has zero entries."%self._name
            return
        plot = plots.PlotBase()
        h = self._histo.Clone(self._histo.GetName()+"clone")
        h.Scale(self._normalizationFactor)
        plot.histoMgr.appendHisto(histograms.Histo(h,self._histo.GetName()))
        plot.createFrame("template_"+self._name.replace(" ","_")+"_"+self._binLabel, opts={"ymin": 0.1, "ymaxfactor": 2., "xlabel":"MET (GeV)", "ylabel":"N_{events}"})
        histograms.addStandardTexts(cmsTextPosition="outframe")
        histograms.addText(0.36,0.89, "Integral = %d events"%int(self._histo.Integral()*self._normalizationFactor+0.5))
        histograms.addText(0.36,0.84, self._name)
        histograms.addText(0.36,0.79, self._binLabel)
        plot.getPad().SetLogy(True)
        st = styles.getDataStyle().clone()
        st.append(styles.StyleFill(fillColor=ROOT.kYellow))
        plot.histoMgr.forHisto(self._histo.GetName(), st)
        #plot.setFileName("template_"+self._name.replace(" ","_")+"_"+self._binLabel)
        plot.draw()
        plot.save()
        #st.append(styles.StyleFill(fillColor=0))
        #plot.histoMgr.forHisto(objectName, st)

    ## Sets the default fit parameters
    def setDefaultFitParam(self, defaultInitialValue=None, defaultLowerLimit=None, defaultUpperLimit=None):
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

    ## Sets the fit parameters for a specific bin
    def setFitParamForBin(self, binLabel, initialValue=None, lowerLimit=None, upperLimit=None):
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

    def doFit(self, fitOptions="S", createPlot=True):
        if self._histo == None:
            raise Exception("Error: Please provide first the histogram with the 'setHistogram' method")
        if self._histo.Integral(1, self._histo.GetNbinsX()+1) == 0.0:
            raise Exception("Error: The histogram '%s' integral is zero! (perhaps there is a bug somewhere or you run out of events)"%self._name)
        if self._fitFunction == None:
            return
        else:
            if not self._quietMode:
                print "\n- Fitting %s in bin %s"%(self._name, self._binLabel)
                self.printFitParamSettings(self._binLabel)
            # Define fit object
            fit = ROOT.TF1("fit"+self._name+self._binLabel, self._fitFunction, self._fitRangeMin, self._fitRangeMax, self._fitFunction.getNParam())
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
            # Clone the histogram and normalize its area to unity (note also the under/overflow bins)
            h = aux.Clone(self._histo)
            #h.Scale(1.0 / h.Integral(1, h.GetNbinsX()+1))
            # Do the fit
            if not self._quietMode:
                print "... Using fit options:",fitOptions
            elif not "Q" in fitOptions:
                fitOptions += " Q" # To suppress output
            if not "S" in fitOptions:
                fitOptions += " S" # To return fit results
            canvas = ROOT.TCanvas() # Create explicitly canvas to get rid of warning message
            fitResultObject = h.Fit(fit, fitOptions)
            self._fitParameters = fit.GetParameters()
            self._fitParErrors = fit.GetParErrors()
            # Note: need to divide the TF1 integral by histogram bin width
            self._nEventsFromFit = fit.Integral(self._histo.GetXaxis().GetXmin(), self._histo.GetXaxis().GetXmax())*self._normalizationFactor / self._histo.GetXaxis().GetBinWidth(1)
            orthogonalizer = fitHelper.FitParameterOrthogonalizer(fit, fitResultObject, self._histo.GetXaxis().GetXmin(), self._histo.GetXaxis().GetXmax())
            self._nEventsTotalErrorFromFitUp = orthogonalizer.getTotalFitParameterUncertaintyUp()
            self._nEventsTotalErrorFromFitDown = orthogonalizer.getTotalFitParameterUncertaintyDown()
            if not self._quietMode:
                print "... Sanity check: Nevents in histogram = %.1f +- %.1f vs. fitted = %.1f + %.1f - %.1f"%(self.getNeventsFromHisto(False), self.getNeventsErrorFromHisto(False),
                                                                                                               self._nEventsFromFit, self._nEventsTotalErrorFromFitUp, self._nEventsTotalErrorFromFitDown)
            # Do a plot of the fit
            if createPlot:
                ROOT.gStyle.SetOptFit(0)
                ROOT.gStyle.SetOptStat(0)
                plot = plots.PlotBase()
                plot.histoMgr.appendHisto(histograms.Histo(h,h.GetName()))
                plot.histoMgr.appendHisto(histograms.Histo(fit, "fit"))
                plot.createFrame("fit_"+self._name.replace(" ","_")+"_"+self._binLabel, opts={"ymin": 1e-5, "ymaxfactor": 2., "xlabel":"MET (GeV)", "ylabel":"N_{events}"})
                histograms.addText(0.36,0.84, self._name+", "+self._binLabel)
                plot.getPad().SetLogy(True)
                histograms.addStandardTexts(cmsTextPosition="outframe")
                plot.draw()
                plot.save()

## Manager class for QCD measurement normalization
class QCDNormalizationManager:
    def __init__(self, binLabels):
        self._mode = None
        self._templates = {}
        self._binLabels = binLabels
        self._requiredTemplateList = ["EWKFakeTaus_Baseline", "EWKFakeTaus_Inverted", "EWKGenuineTaus_Baseline", "EWKGenuineTaus_Inverted", "QCD_Baseline", "QCD_Inverted"]
        self._EWKFakeTausSource = "EWKFakeTaus_Baseline"
        self._EWKGenuineTausSource = "EWKGenuineTaus_Baseline"
        self._QCDSource = "QCD_Inverted"
        self._commentLines = []
        self._qcdNormalization = {}
        self._qcdNormalizationError = {}
        self._ewkFakesNormalization = {}
        self._ewkFakesNormalizationError = {}
        self._combinedFakesNormalization = {}
        self._combinedFakesNormalizationError = {}
        
        if not isinstance(binLabels, list):
            raise Exception("Error: binLabels needs to be a list of strings")

    ## Sets sources for fitting data to templates (give as input the name string of the template)
    def setSources(self, ewkFakeTausSrc=None, ewkGenuineTausSrc=None, qcdSrc=None):
        if ewkFakeTausSrc != None:
            self._EWKFakeTausSource = ewkFakeTausSrc
        if ewkGenuineTausSrc != None:
            self._EWKGenuineTausSource = ewkGenuineTausSrc
        if qcdSrc != None:
            self._QCDSource = qcdSrc

    ## Creates a QCDNormalizationTemplate and returns it
    def createTemplate(self, name):
        if name in self._templates.keys():
            raise Exception("Error: A template with name '%s' has already been created!"%name)
        q = QCDNormalizationTemplate(name)
        self._templates[name] = q
        return q
   
    ## Plots shapes of templates
    def plotTemplates(self):
        for k in self._templates.keys():
            if self._templates[k].hasHisto():
                self._templates[k].plot()

    ## Resets bin results
    def resetBinResults(self):
        for k in self._templates.keys():
            self._templates[k].reset()

    ## Checks that input is valid
    def _checkInputValidity(self):
        # Require that the needed templates are created and that a histogram is provided for them
        for item in self._requiredTemplateList:
            if item not in self._templates.keys():
                raise Exception ("Error: please create first template with name '%s'!"%item)
            if not self._templates[item].hasHisto():
                raise Exception ("Error: please call first setHistogram(...) for template named '%s'!"%item)
        # Require that fitter is provided for the specified templates
        for item in [self._EWKFakeTausSource, self._EWKGenuineTausSource, self._QCDSource]:
            if not self._templates[item].isFittable():
                raise Exception ("Error: please call first setFitter(...) for template named '%s'!"%item)
        # Require that no unknown templates are provided
        for item in self._templates.keys():
            if not item in self._requiredTemplateList:
                raise Exception("Error: the provided template '%s' is not supported!"%item)
        # Require that bin labels of the templates are identical
        for item in self._requiredTemplateList:
            if self._templates[item].getBinLabel() != self._templates[self._requiredTemplateList[0]].getBinLabel():
                raise Exception("Error: The bin label is different for '%s' than for '%s'!"%(item, self._requiredTemplateList[0]))
    
    ## Fits templates
    def _fitTemplates(self, fitOptions):
        for item in [self._EWKFakeTausSource, self._EWKGenuineTausSource, self._QCDSource]:
            self._templates[item].doFit(fitOptions=fitOptions, createPlot=True)

    ## Do final fit
    # \param dataHisto     ROOT histogram of the data distribution
    # \param fitOptions    string containing the fit options (see TH1::Fit())
    # \param FITMIN        float describing the minimum value for the fit range (valid only if "R" is included in fitOptions)
    # \param FITMAX        float describing the maximum value for the fit range (valid only if "R" is included in fitOptions)
    def fitDataWithQCDAndFakesAndGenuineTaus(self, dataHisto, fitOptions, FITMIN, FITMAX):
        class FunctionSum:
            def __init__(self, f1, f2):
                self._f1 = f1.Clone()
                self._f2 = f2.Clone()
            def __call__(self, x):
                return self._f1.Eval(x[0]) + self._f2.Eval(x[0])
        
        #===== Check that inputs have been provided
        self._checkInputValidity()
        
        #===== Fit templates
        self._fitTemplates(fitOptions)

        #===== Do fit
        # Create a temporary template for data
        print "\n- Fitting templates to data"
        print "... input for QCD:", self._QCDSource
        print "... input for EWK fake taus:", self._EWKFakeTausSource
        print "... input for EWK genuine taus:", self._EWKGenuineTausSource
        dataTemplate = QCDNormalizationTemplate("data")
        binLabel = self._templates[self._requiredTemplateList[0]].getBinLabel()
        dataTemplate.setHistogram(dataHisto, binLabel)
        dataTemplate.plot()
        dataTemplate.setFitter(FitFunction("FitDataWithQCDAndFakesAndGenuineTaus",
                                           QCDFitFunction = self._templates[self._QCDSource].getFitFunction(),
                                           parQCD = self._templates[self._QCDSource].getFittedParameters(),
                                           QCDnorm = 1.0,
                                           EWKFakeTausFitFunction = self._templates[self._EWKFakeTausSource].getFitFunction(),
                                           parEWKFakeTaus = self._templates[self._EWKFakeTausSource].getFittedParameters(),
                                           EWKFakeTausNorm = 1.0,
                                           EWKGenuineTausFitFunction = self._templates[self._EWKGenuineTausSource].getFitFunction(),
                                           parEWKGenuineTaus = self._templates[self._EWKGenuineTausSource].getFittedParameters(),
                                           EWKGenuineTausNorm = 1.0),
                               FITMIN, FITMAX)
        # Do fit to data
        dataTemplate.setDefaultFitParam(defaultInitialValue=[1.0, 0.90, 0.10], defaultLowerLimit=[0.0, 0.0, 0.0], defaultUpperLimit=[10.0, 1.0, 1.0])
        dataTemplate.doFit(fitOptions)
        
        #===== Do a plot of the fit
        # Recreate the already fitted QCD and EWK fakes functions
        funcData = dataTemplate.obtainFittedFunction(1.0, FITMIN, FITMAX)
        funcData.SetLineColor(ROOT.kRed)
        n = dataTemplate.getFittedParameters()[0] * dataTemplate.getFittedParameters()[1]
        funcQCD = self._templates[self._QCDSource].obtainFittedFunction(n, FITMIN, FITMAX)
        funcQCD.SetLineColor(ROOT.kBlue)
        funcEWKfakes = self._templates[self._EWKFakeTausSource].obtainFittedFunction(dataTemplate.getFittedParameters()[0] * dataTemplate.getFittedParameters()[2], FITMIN, FITMAX)
        funcSum = FunctionSum(funcQCD, funcEWKfakes)
        funcQCDPlusEWKFakes = ROOT.TF1("QCDPlusEWKfakes"+binLabel, funcSum, FITMIN, FITMAX, 0)
        funcQCDPlusEWKFakes.SetLineColor(ROOT.kMagenta+1)
        funcQCDPlusEWKFakes.SetLineWidth(2)
        funcQCDPlusEWKFakes.SetLineStyle(2)
        # Make plot
        ROOT.gStyle.SetOptFit(0)
        ROOT.gStyle.SetOptStat(0)
        plot = plots.PlotBase()
        plot.histoMgr.appendHisto(histograms.Histo(dataHisto,dataHisto.GetName()))
        plot.histoMgr.appendHisto(histograms.Histo(funcData, "fitted data"))
        plot.histoMgr.appendHisto(histograms.Histo(funcQCD, "QCD template"))
        plot.histoMgr.appendHisto(histograms.Histo(funcQCDPlusEWKFakes, "QCD+EWK fakes template"))
        plot.createFrame("finalFit_"+"_"+binLabel, opts={"ymin": 1e-5, "ymaxfactor": 2., "xlabel":"MET (GeV)", "ylabel":"N_{events}"})
        histograms.addText(0.36,0.84, "Fit to data, "+binLabel)
        plot.getPad().SetLogy(True)
        histograms.addStandardTexts(cmsTextPosition="outframe")
        plot.draw()
        plot.save()
        
        #===== Handle results
        print "\n- Results:"
        # Collect template sanity checks
        self._commentLines.append("\nBin: %s"%binLabel)
        for src in [self._EWKFakeTausSource, self._EWKGenuineTausSource, self._QCDSource]:
            item = self._templates[src]
            self._commentLines.append("... Template fit sanity check (%s): Nevents in histogram = %.1f +- %.1f vs. fitted = %.1f + %.1f - %.1f"%
                        (item.getName(), item.getNeventsFromHisto(False), item.getNeventsErrorFromHisto(False),
                         item.getNeventsFromFit(), item.getNeventsTotalErrorFromFit()[0], item.getNeventsTotalErrorFromFit()[1]))
        # Fractions and sanity checks for fitting to data
        lines = []
        nQCDFitted = dataTemplate.getFittedParameters()[1]*dataTemplate.getNeventsFromHisto(False)
        lines.append("    Fitted QCD fraction: %f +- %f"%(dataTemplate.getFittedParameters()[1], dataTemplate.getFittedParameterErrors()[1]))
        lines.append("      Sanity check: QCD in baseline = %.1f vs. fitted = %.1f"%(self._templates["QCD_Baseline"].getNeventsFromHisto(False), nQCDFitted))
        nEWKFakeTausFitted = dataTemplate.getFittedParameters()[2]*dataTemplate.getNeventsFromHisto(False)
        lines.append("    Fitted EWK fake taus fraction: %f +- %f"%(dataTemplate.getFittedParameters()[2], dataTemplate.getFittedParameterErrors()[2]))
        lines.append("      Sanity check: EWK fake in baseline = %.1f vs. fitted = %.1f"%(self._templates["EWKFakeTaus_Baseline"].getNeventsFromHisto(False), nEWKFakeTausFitted))
        # should one divide the fractions with dataTemplate.getFittedParameters()[0] ??? (right now not because the correction is so small)
        
        # Normalization factor for QCD
        qcdNormFactor = nQCDFitted / self._templates["QCD_Inverted"].getNeventsFromHisto(False)
        nQCDBaselineError = errorPropagation.errorPropagationForProduct(dataTemplate.getFittedParameters()[1], dataTemplate.getFittedParameterErrors()[1],
                                                                        dataTemplate.getNeventsFromHisto(False), dataTemplate.getNeventsErrorFromHisto(False))
        qcdNormFactorError = errorPropagation.errorPropagationForDivision(nQCDFitted, nQCDBaselineError,
                                                                          self._templates["QCD_Inverted"].getNeventsFromHisto(False), self._templates["QCD_Inverted"].getNeventsErrorFromHisto(False))
        self._qcdNormalization[binLabel] = qcdNormFactor
        self._qcdNormalizationError[binLabel] = qcdNormFactorError
        # Normalization factor for EWK fake taus
        ewkFakesNormFactor = None
        ewkFakesNormFactorError = None
        _ewkFakesNormFactorDenominatorFromFit = False
        if _ewkFakesNormFactorDenominatorFromFit:
            ewkFakesNormFactor = nEWKFakeTausFitted / self._templates["EWKFakeTaus_Inverted"].getNeventsFromHisto(False)
            nEWKFakesBaselineError = errorPropagation.errorPropagationForProduct(dataTemplate.getFittedParameters()[2], dataTemplate.getFittedParameterErrors()[2],
                                                                             dataTemplate.getNeventsFromHisto(False), dataTemplate.getNeventsErrorFromHisto(False))
            ewkFakesNormFactorError = errorPropagation.errorPropagationForDivision(nEWKFakeTausFitted, nEWKFakesBaselineError,
                                                                                  self._templates["EWKFakeTaus_Inverted"].getNeventsFromHisto(False), self._templates["EWKFakeTaus_Inverted"].getNeventsErrorFromHisto(False))
        else:
            ewkFakesNormFactor = self._templates["EWKFakeTaus_Baseline"].getNeventsFromHisto(False) / self._templates["EWKFakeTaus_Inverted"].getNeventsFromHisto(False)
            ewkFakesNormFactorError = errorPropagation.errorPropagationForDivision(self._templates["EWKFakeTaus_Baseline"].getNeventsFromHisto(False), self._templates["EWKFakeTaus_Baseline"].getNeventsErrorFromHisto(False),
                                                                                   self._templates["EWKFakeTaus_Inverted"].getNeventsFromHisto(False), self._templates["EWKFakeTaus_Inverted"].getNeventsErrorFromHisto(False))
        #ewkFakesNormFactor = self._templates["EWKFakeTaus_Baseline"].getNeventsFromHisto(False) / self._templates["EWKFakeTaus_Inverted"].getNeventsFromHisto(False)
        self._ewkFakesNormalization[binLabel] = ewkFakesNormFactor
        self._ewkFakesNormalizationError[binLabel] = ewkFakesNormFactorError
        lines.append("   Normalization factor (QCD): %f +- %f"%(qcdNormFactor, qcdNormFactorError))
        lines.append("   Normalization factor (EWK fake taus): %f +- %f"%(ewkFakesNormFactor, ewkFakesNormFactorError))
        # Print output and store comments
        self._commentLines.extend(lines)
        for l in lines:
            print l
    
    ## Calculates the combined normalization and if specified, varies it up or down by factor (1+variation)
    def calculateCombinedNormalization(self, hQCD, hEWKfakes, variation=0.0):
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
        wError = None
        if nTotal > 0.0:
            w = nQCD / nTotal
            wError = errorPropagation.errorPropagationForDivision(nQCD, nQCDerror, nTotal, nTotalError)
        lines.append("   w = nQCD/(nQCD+nEWKfakes) = %f +- %f"%(w, wError))
        if variation != 0.0:
            w = w*(1.0+variation)
            if w < 0.0:
                w = 0.0
            if w > 1.0:
                w = 1.0
            lines.append("   variation applied, using the value w = %f"%w)
        # Calculate the combined normalization factor (f_fakes = w*f_QCD + (1-w)*f_EWKfakes)
        binLabel = self._templates[self._requiredTemplateList[0]].getBinLabel()
        fakeRate = None
        fakeRateError = None
        if w != None:
            fakeRate = w*self._qcdNormalization[binLabel] + (1.0-w)*self._ewkFakesNormalization[binLabel]
            fakeRateErrorPart1 = errorPropagation.errorPropagationForProduct(w, wError, self._qcdNormalization[binLabel], self._qcdNormalizationError[binLabel])
            fakeRateErrorPart2 = errorPropagation.errorPropagationForProduct(w, wError, self._ewkFakesNormalization[binLabel], self._ewkFakesNormalizationError[binLabel])
            fakeRateError = ROOT.TMath.Sqrt(fakeRateErrorPart1**2 + fakeRateErrorPart2**2)
        lines.append("   Combined normalization factor for (nQCD+nEWKfakes) = %s +- %s"%(str(fakeRate), str(fakeRateError)))
        self._combinedFakesNormalization[binLabel] = fakeRate
        self._combinedFakesNormalizationError[binLabel] = fakeRateError
        # Print output and store comments
        self._commentLines.extend(lines)
        for l in lines:
            print l

    def writeScaleFactorFile(self, filename, analysis, dataEra, searchMode):
        s = ""
        s += "# Generated on %s\n"%datetime.datetime.now().ctime()
        s += "# by %s\n"%os.path.basename(sys.argv[0])
        s += "\n"
        s += "import sys\n"
        s += "\n"
        s += "def QCDInvertedNormalizationSafetyCheck(era):\n"
        s += "    validForEra = \""+dataEra+"\"\n"
        s += "    if not era == validForEra:\n"
        s += "        print \"Warning, inconsistent era, normalisation factors valid for\",validForEra,\"but trying to use with\",era\n"
        s += "        sys.exit()\n"
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
        for k in self._combinedFakesNormalization:
            s += '    "%s": %f,\n'%(k, self._combinedFakesNormalization[k])
        s += "}\n"
        s += "QCDPlusEWKFakeTausNormalizationSystFakeWeightingVarUp = {\n"
        for k in self._combinedFakesNormalization:
            s += '    "%s": %f,\n'%(k, self._combinedFakesNormalization[k])
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
        print "Normalization factors written to '%s'"%filename
        
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
            q = QCDNormalizationTemplate("EWK testline")
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
            q = QCDNormalizationTemplate("EWK testline")
            h = ROOT.TH1F("h","h",10,0,10)
            q.setHistogram(h, "Inclusive bin")
            with self.assertRaises(Exception):
                q.doFit()
            self.assertEqual(q.getNeventsFromHisto(True), 0.0)
            self.assertEqual(q.getNeventsErrorFromHisto(True), ROOT.TMath.Sqrt(0.0))
            h.Delete()
        
        def testFitWithoutFunction(self):
            q = QCDNormalizationTemplate("EWK testline")
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
            q = QCDNormalizationTemplate("EWK testline")
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
            q = QCDNormalizationTemplate("EWK testline",quietMode=True)
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
