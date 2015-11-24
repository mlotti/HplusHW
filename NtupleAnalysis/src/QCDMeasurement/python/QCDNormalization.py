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
import os

## Container class for fit functions
class FitFunction:
    def __init__(self, functionName, **kwargs):
        self._functionName = functionName
        self._args = kwargs
        
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
            "FitDataWithQCDAndFakesAndGenuineTaus": 2,
        }
        self._nParam = nParams[functionName]
    
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
        return norm*(RayleighFunction(x,par[0:1],1)+par[2]*ROOT.TMath.Gaus(x[0],par[3],par[4],1)+par[5]*ROOT.TMath.Exp(-par[6]*x[0]))

    def EWKFunction(self,x,par,boundary,norm=1,rejectPoints=0):
        if x[0] < boundary:
            return norm*par[0]*ROOT.TMath.Gaus(x[0],par[1],par[2],1)
        C = norm*par[0]*ROOT.TMath.Gaus(boundary,par[1],par[2],1)*ROOT.TMath.Exp(boundary*par[3])
        return C*ROOT.TMath.Exp(-x[0]*par[3])

    def EWKFunctionInv(self,x,par,boundary,norm=1,rejectPoints=0):
        if not rejectPoints == 0:
            if (x[0] > 230 and x[0] < 290):
                ROOT.TF1.RejectPoint()
                #return 0
        if x[0] < boundary:
            return norm*(par[0]*ROOT.TMath.Landau(x[0],par[1],par[2]))
        C = norm*(par[0]*ROOT.TMath.Landau(boundary,par[1],par[2]))*ROOT.TMath.Exp(boundary*par[3])
        return C*ROOT.TMath.Exp(-x[0]*par[3])

    def QCDEWKFunction(self,x,par,norm):
        if par[0]+par[1]*x[0] == 0.0:
            return 0
        return norm*(par[1]*x[0]/((par[0])*(par[0]))*ROOT.TMath.Exp(-x[0]*x[0]/(2*(par[0])*(par[0])))+par[2]*ROOT.TMath.Gaus(x[0],par[3],par[4],1)+par[5]*ROOT.TMath.Exp(-par[6]*x[0]))

    def QCDFunctionFixed(self,x,par):
        return par[0]*(ROOT.TMath.Gaus(x[0],par[1],par[2],1)+par[3]*ROOT.TMath.Gaus(x[0],par[4],par[5],1)+par[6]*ROOT.TMath.Exp(-par[7]*x[0]))
    
    #===== Composite functions for fitting data
    ## QCD, fake taus, and genuine taus as separate templates
    def FitDataWithQCDAndFakesAndGenuineTaus(self, x, par,
            QCDFitFunction, parQCD, QCDnorm,
            EWKFakeTausFitFunction, parEWKFakeTaus, EWKFakeTausNorm,
            EWKGenuineTausFitFunction, parEWKGenuineTaus, EWKGenuineTausNorm):
        nQCD =            QCDFitFunction(x, parQCD, norm=QCDnorm)
        nEWKFakeTaus =    EWKFakeTausFitFunction(x, parEWKFakeTaus, norm=EWKFakeTausNorm)
        nEWKGenuineTaus = EWKGenuineTausFitFunction(x, parEWKGenuineTaus, norm=EWKGenuineTausNorm) 
        return par[0]*(par[1]*nQCD + par[2]*nEWKFakeTaus + (1 - par[1] - par[2])*nEWKGenuineTaus)

    ## QCD and fake tau templates as one inclusive template
    def FitDataWithFakesAndGenuineTaus(self, x, par,
            QCDAndFakesFitFunction, parQCDAndFakes, QCDAndFakesnorm,
            EWKGenuineTausFitFunction, parEWKGenuineTaus, EWKGenuineTausNorm):
        nQCDAndFakes =    QCDAndFakesFitFunction(x, parQCDAndFakes, norm=QCDAndFakesnorm)
        nEWKGenuineTaus = EWKGenuineTausFitFunction(x, parEWKGenuineTaus, norm=EWKGenuineTausNorm) 
        return par[0]*(par[1]*nQCDAndFakes + (1 - par[1])*nEWKGenuineTaus)


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
        self._nEventsErrorFromFit = None
        self._histo = None
        self._fitResults = None

    ## Returns true if a histogram has been provided
    def hasHisto(self):
        return self._histo != None
    
    ## Returns true if a fit function has been provided
    def isFittable(self):
        return self._fitFunction != None

    ## Prints the parameter settings (for debugging or info)
    def printFitParamSettings(self):
        keys = self._fitParamInitialValues.keys()
        for k in self._fitParamLowerLimits.keys():
            if not k in keys:
                keys.append(k)
        keys.sort()
        print "\nFit parameter settings for '%s': (initial value / low bound / high bound)"%self._name
        for k in keys:
            s = "  %s: "%k
            if k in self._fitParamInitialValues.keys():
                s += " [%s] "%", ".join("%f" % x for x in self._fitParamInitialValues[k])
            elif "default" in self._fitParamInitialValues.keys():
                s += " (default) "
            else:
                s += " (no setting) "
            if k in self._fitParamLowerLimits.keys():
                s += "/ [%s] "%", ".join("%f" % x for x in self._fitParamLowerLimits[k])
                s += "/ [%s] "%", ".join("%f" % x for x in self._fitParamUpperLimits[k])
            elif "default" in self._fitParamLowerLimits.keys():
                s += "/ (default) / (default)"
            else:
                s += "/ (none) / (none)"
            print s
        print ""

    ## Prints the results
    def printResults(self):
        print "\nResults for '%s', bin '%s':"%(self._name, self._binLabel)
        if self._histo == None:
            print "  (no histogram has been given -> no results)"
        else:
            print "  Nevents from histogram (visible part only): %f +- %f"%(self.getNeventsFromHisto(False), self.getNeventsErrorFromHisto(False))
            print "  Nevents from histogram (with under/overflow): %f +- %f"%(self.getNeventsFromHisto(True), self.getNeventsErrorFromHisto(True))
            if self._fitResults == None:
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
            return self._histo.Integral(0, self._histo.GetNbinsX()+2)
        else:
            return self._histo.Integral(1, self._histo.GetNbinsX()+1)

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
        return float(integralError)
    
    ## Returns the number of events obtained from the fit
    #  The range is the range of the histogram; under/overflow bins are ignored!
    def getNeventsFromFit(self):
        if self._fitResults == None:
            if self._fitFunction == None:
                raise Exception("Error: Please call the the 'setFitter(...)' method first!")
            else:
                raise Exception("Error: Please call the 'doFit(...)' method first!")
        return self._nEventsFromFit
    
    ## Returns the [plus, minus] absolute uncertainty in number of events obtained from the fit
    #  The range is the range of the histogram; under/overflow bins are ignored!
    def getNeventsErrorFromFit(self):
        if self._fitResults == None:
            if self._fitFunction == None:
                raise Exception("Error: Please call the the 'setFitter(...)' method first!")
            else:
                raise Exception("Error: Please call the 'doFit(...)' method first!")
        return self._nEventsErrorFromFit

    def getFitResults(self):
        return self._fitResults
    
    ## Call once for every bin
    def setHistogram(self, histogram, binLabel):
        self._histo = histogram
        self._binLabel = binLabel
        # Convert negative bins to zero but leave errors intact
        for k in range(0, self._histo.GetNbinsX()+2):
            if self._histo.GetBinContent(k) < 0.0:
                print "template '%s': In bin %d, converted negative value (%f) to zero."%(self._name(), k, self._histo.GetBinContent(k))
                self._histo.SetBinContent(k, 0.0)
        # Format bin label string
        self._binLabel = getModifiedBinLabelString(binLabel)
        
    ## Make a plot of the histogram
    def plot(self):
        if self._histo == None:
            raise Exception("Error: Please provide first the histogram with the 'setHistogram' method")
        if self._histo.GetEntries() == 0:
            print "Skipping plot for '%s' because it has zero entries."%self._name
            return
        plot = plots.PlotBase()
        plot.histoMgr.appendHisto(histograms.Histo(self._histo,self._histo.GetName()))
        plot.createFrame("template_"+self._name.replace(" ","_")+"_"+self._binLabel, opts={"ymin": 0.1, "ymaxfactor": 2.})
        histograms.addStandardTexts(cmsTextPosition="outframe")
        histograms.addText(0.36,0.84,"Integral = %d events"%int(self._histo.Integral(1, self._histo.GetNbinsX()+1)+0.5))
        histograms.addText(0.36,0.79, self._name+", "+self._binLabel)
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
                print "- Fitting", self._name
            # Define fit object
            fit = ROOT.TF1("fit"+self._name+self._binLabel, self._fitFunction, self._fitRangeMin, self._fitRangeMax, self._fitFunction.getNParam())
            # Set initial fit parameter values
            key = None
            if self._binLabel in self._fitParamInitialValues.keys():
                key = self._binLabel
            if "default" in self._fitParamInitialValues.keys():
                key = "default"
            if key != None:
                for i in range(len(self._fitParamInitialValues[key])):
                    fit.SetParameter(i, self._fitParamInitialValues[key][i])
            # Set fit parameter ranges
            key = None
            if self._binLabel in self._fitParamLowerLimits.keys():
                key = self._binLabel
            if "default" in self._fitParamLowerLimits.keys():
                key = "default"
            if key != None:
                for i in range(len(self._fitParamLowerLimits[key])):
                    fit.SetParLimits(i, self._fitParamLowerLimits[key][i], self._fitParamUpperLimits[key][i])
            # Clone the histogram and normalize its area to unity (note also the under/overflow bins)
            h = aux.Clone(self._histo)
            #h.Scale(1.0 / h.Integral(1, h.GetNbinsX()+1))
            # Do the fit
            if not self._quietMode:
                print "- using fit options:",fitOptions
            elif not "Q" in fitOptions:
                fitOptions += " Q" # To suppress output
            if not "S" in fitOptions:
                fitOptions += " S" # To return fit results
            canvas = ROOT.TCanvas() # Create explicitly canvas to get rid of warning message
            fitResultObject = h.Fit(fit, fitOptions)
            self._fitResults = fit.GetParameters()
            self._nEventsFromFit = fit.Integral(self._histo.GetXaxis().GetXmin(), self._histo.GetXaxis().GetXmax())
            orthogonalizer = fitHelper.FitParameterOrthogonalizer(fit, fitResultObject)
            (upUncert, downUncert) = orthogonalizer.getTotalFitParameterUncertainty(self._histo.GetXaxis().GetXmin(), self._histo.GetXaxis().GetXmax())
            self._nEventsErrorFromFit = [upUncert, downUncert]
            # Do a plot of the fit
            if createPlot:
                ROOT.gStyle.SetOptFit(0)
                ROOT.gStyle.SetOptStat(0)
                plot = plots.PlotBase()
                plot.histoMgr.appendHisto(histograms.Histo(h,h.GetName()))
                plot.histoMgr.appendHisto(histograms.Histo(fit, "fit"))
                plot.createFrame("fit_"+self._name.replace(" ","_")+"_"+self._binLabel, opts={"ymin": 1e-5, "ymaxfactor": 2.})
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
        
        if not isinstance(binLabels, list):
            raise Exception("Error: binLabels needs to be a list of strings")

    ## Creates a QCDNormalizationTemplate and returns it
    def createTemplate(self, name):
        if name in self._templates.keys():
            raise Exception("Error: A template with name '%s' has already been created!"%name)
        q = QCDNormalizationTemplate(name)
        self._templates[name] = q
        return q

    ## Fits templates
    def fitTemplates(self, fitOptions):
        for k in self._templates.keys():
            if self._templates[k].hasHisto() and self._templates[k].isFittable():
                self._templates[k].doFit(fitOptions=fitOptions, createPlot=True)
    
    ## Plots shapes of templates
    def fitTemplates(self, fitOptions):
        for k in self._templates.keys():
            if self._templates[k].hasHisto():
                self._templates[k].plot()

    ## Do final fit, 
    def fitDataWithQCDAndFakesAndGenuineTaus(self, dataHisto):
        # Check that inputs have been provided
        
        # Do fit
        
        # Handle results
        
        
        


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
            self.assertEqual(q.getNeventsFromHisto(True), 1000.0)
            self.assertLess(abs(q.getNeventsErrorFromHisto(True) - ROOT.TMath.Sqrt(1000.0)), 0.0001)
            self.assertEqual(q.getNeventsFromHisto(False), 973.0)
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
            self.assertEqual(q.getNeventsErrorFromFit()[0], 0.)
            self.assertEqual(q.getNeventsErrorFromFit()[1], 0.)
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
            self.assertEqual(q.getNeventsErrorFromFit()[0], 0.)
            self.assertEqual(q.getNeventsErrorFromFit()[1], 0.)
            # Set params (for bin)
            q.reset()
            q.setFitParamForBin("Inclusive bin", initialValue=[1000,4,2], lowerLimit=[10, 0, 0], upperLimit=[10000, 10, 10])
            q.setHistogram(h, "Inclusive bin")
            #q.printFitParamSettings()
            q.doFit(fitOptions="S R L", createPlot=_createPlots)
            self.assertLess(abs(q.getNeventsFromFit()-970), 1)
            self.assertLess(abs(q.getNeventsErrorFromFit()[0]-31.08), 0.1)
            self.assertLess(abs(q.getNeventsErrorFromFit()[1]-2.79), 0.01)
            #q.printResults()


            
        

    unittest.main()
