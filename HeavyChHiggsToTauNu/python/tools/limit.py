## \package limit
# Various tools for plotting BR/tanbeta limits
#
# Some of the settings depend on the \a forPaper boolean flag. All of
# these are functions, so user can override the flag in a script.

import os
import math
import json
import array

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.statisticalFunctions as statisticalFunctions
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.BRdataInterface as BRdataInterface
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms

## Flag for stating if the plots are for paper (True) or not (False)
#forPaper = False
forPaper = True

## Unit for mass (GeV vs. GeV/c^2
def massUnit():
    if forPaper:
        return "GeV"
    return "GeV/c^{2}"

## Label for branching fraction
BR = "#it{B}"

## The label for the physics process
process = "t #rightarrow H^{+}b, H^{+} #rightarrow #tau^{+}#nu_{#tau}"
processHeavy = "pp #rightarrow #bar{t}(b)H^{+}, H^{+} #rightarrow #tau^{+}#nu_{#tau}"
processCombination = "pp #rightarrow #bar{t}(b)H^{+}"

## Label for the H+->tau BR assumption
#BRassumption = "%s(H^{+} #rightarrow #tau#nu) = 1"%BR
BRassumption = ""

## Y axis label for the BR
BRlimit = None

## Y axis label for the sigma x BR
sigmaBRlimit = None

def useParentheses():
    global BRlimit, sigmaBRlimit
    BRlimit = "95%% CL limit on %s(t#rightarrowH^{+}b)#times%s(H^{+}#rightarrow#tau#nu)"%(BR,BR)
    sigmaBRlimit = "95%% CL limit for #sigma(H^{+})#times%s(H^{+}#rightarrow#tau#nu) (pb)"%(BR)
def useSubscript():
    global BRlimit, sigmaBRlimit
    BRlimit = "95%% CL limit on %s_{t#rightarrowH^{+}b}#times%s_{H^{+}#rightarrow#tau#nu}"%(BR,BR)
    sigmaBRlimit = "95%% CL limit for #sigma_{H^{+}}#times%s_{H^{+}#rightarrow#tau#nu} (pb)"%(BR)
useSubscript()

## Y axis label for the tanbeta
#tanblimit = "95 % CL limit on tan #beta"
tanblimit = "tan #beta"

## Label for m(H+)
def mHplus():
    return "m_{H^{+}} (%s)" % massUnit()

## Label for m(A)
def mA():
    return "m_{A} (%s)" % massUnit()


## Labels for the final states
_finalstateLabels = {
    "taujets": "^{}#tau_{h}+jets",
    "etau"   : "e^{}#tau_{h}",
    "mutau"  : "#mu^{}#tau_{h}",
    "emu"    : "e#mu",
}

## Default y axis maximum values for BR limit for the final states
_finalstateYmaxBR = {
    "etau": 0.4,
    "mutau": 0.4,
    "emu": 0.8,
    "default": 0.025,
}

## Default y axis maximum values for sigma x BR limit for the final states
_finalstateYmaxSigmaBR = {
    "etau": 10.0, # FIXME
    "mutau": 10.0, # FIXME
    "emu": 10.0, # FIXME
    "default": 1.0,
}

def setExcludedStyle(graph):
    ci = ROOT.TColor.GetColor(156, 156, 156)
#    ci = ROOT.TColor.GetColor(209, 209, 209)
    graph.SetFillColorAlpha(ci, 0.3) # transparency
#    graph.SetFillColorAlpha(ROOT.kViolet+6, 0.3) # transparency

def setObservedStyle(graph):
    graph.SetMarkerStyle(21)
    graph.SetMarkerSize(1.3)
    graph.SetMarkerColor(ROOT.kBlack)
    graph.SetLineWidth(3)
    graph.SetLineColor(ROOT.kBlack)
    
def setTheoreticalErrorStyle(graph):    
    graph.SetLineStyle(9)
    graph.SetLineWidth(2)

def setExpectedStyle(graph):
    graph.SetLineStyle(2)
    graph.SetLineWidth(3)
    graph.SetLineColor(ROOT.kBlack)
    graph.SetMarkerStyle(20)

def setExpectedGreenBandStyle(graph):
    graph.SetFillColor(ROOT.kGreen-3)
    setExpectedStyle(graph)
    
def setExpectedYellowBandStyle(graph):
    graph.SetFillColor(ROOT.kYellow)
    setExpectedStyle(graph)

## Class for reading the BR limits from the JSON file produced by
## landsMergeHistograms.py
class BRLimits:
    ## Constructor
    #
    # \param directory          Path to the multicrab task directory with the JSON files
    # \param excludeMassPoints  List of strings for mass points to exclude
    def __init__(self, directory=".", excludeMassPoints=[], limitsfile="limits.json", configfile="configuration.json"):
        resultfile="limits.json"
        #configfile="configuration.json"

        f = open(os.path.join(directory, limitsfile), "r")
        limits = json.load(f)
        f.close()

        self.lumi = float(limits["luminosity"])

        self.mass = limits["masspoints"].keys()
        self.isHeavyStatus = False
        for m in self.mass:
            if int(m) > 175:
                self.isHeavyStatus = True
        members = ["mass"]

        # sort mass
        floatString = [(float(self.mass[i]), self.mass[i]) for i in range(len(self.mass))]
        floatString.sort()
        self.mass = [pair[1] for pair in floatString]
        if len(excludeMassPoints) > 0:
            self.mass = filter(lambda m: not m in excludeMassPoints, self.mass)

        firstMassPoint = limits["masspoints"][self.mass[0]]

        if "observed" in firstMassPoint:
            self.observed = [limits["masspoints"][m]["observed"] for m in self.mass]
            members.append("observed")
            if "observed_error" in firstMassPoint:
                self.observedError = [limits["masspoints"][m]["observed_error"] for m in self.mass]
                members.append("observedError")

        self.expectedMedian = [limits["masspoints"][m]["expected"]["median"] for m in self.mass]
        self.expectedMinus2 = [limits["masspoints"][m]["expected"]["-2sigma"] for m in self.mass]
        self.expectedMinus1 = [limits["masspoints"][m]["expected"]["-1sigma"] for m in self.mass]
        self.expectedPlus1 = [limits["masspoints"][m]["expected"]["+1sigma"] for m in self.mass]
        self.expectedPlus2 = [limits["masspoints"][m]["expected"]["+2sigma"] for m in self.mass]
        members.extend(["expected"+p for p in ["Median", "Minus2", "Minus1", "Plus1", "Plus2"]])
        if "median_error" in firstMassPoint["expected"]:
            self.expectedMedianError = [limits["masspoints"][m]["expected"]["median_error"] for m in self.mass]
            self.expectedMinus2Error = [limits["masspoints"][m]["expected"]["-2sigma_error"] for m in self.mass]
            self.expectedMinus1Error = [limits["masspoints"][m]["expected"]["-1sigma_error"] for m in self.mass]
            self.expectedPlus1Error = [limits["masspoints"][m]["expected"]["+1sigma_error"] for m in self.mass]
            self.expectedPlus2Error = [limits["masspoints"][m]["expected"]["+2sigma_error"] for m in self.mass]
            members.extend(["expected"+p+"Error" for p in ["Median", "Minus2", "Minus1", "Plus1", "Plus2"]])

        for attr in members:
            setattr(self, attr+"_string", [m for m in getattr(self, attr)])
            setattr(self, attr, [float(m) for m in getattr(self, attr)])

       
        print "Opening file '%s' for input"%os.path.join(directory, configfile)
        f = open(os.path.join(directory, configfile), "r")
        config = json.load(f)
        f.close()

        self.finalstates = []
        def hasDatacard(name):
            for datacard in config["datacards"]:
                if name in datacard:
                    return True
            return False

        if hasDatacard("_hplushadronic_"):
            self.finalstates.append("taujets")
        if hasDatacard("_etau_"):
            self.finalstates.append("etau")
        if hasDatacard("_mutau_"):
            self.finalstates.append("mutau")
        if hasDatacard("_emu_"):
            self.finalstates.append("emu")

    ## Get the integrated luminosity in 1/pb
    def getLuminosity(self):
        return self.lumi

    ## Get the list of final states
    def getFinalstates(self):
        return self.finalstates

    ## Get the label of the final states
    def getFinalstateText(self):
        if len(self.finalstates) <= 1:
            return "%s final state" % _finalstateLabels[self.finalstates[0]]

        ret = ", ".join([_finalstateLabels[x] for x in self.finalstates[:-1]])
        ret += ", and %s final states" % _finalstateLabels[self.finalstates[-1]]
        return ret

    ## Get the maximum value for Y axis for the BR limit
    def getFinalstateYmaxBR(self):
        myObject = None
        if self.isHeavyStatus:
            myObject = _finalstateYmaxSigmaBR
        else:
            myObject = _finalstateYmaxBR
        if len(self.finalstates) == 1:
            try:
                ymax = myObject[self.finalstates[0]]
            except KeyError:
                ymax = myObject["default"]
        else:
            ymax = myObject["default"]
        return ymax

    ## Print the BR limits
    def print2(self,unblindedStatus=False):
        print
        print "                  Expected"
        print "Mass  Observed    Median       -2sigma     -1sigma     +1sigma     +2sigma"
        format = "%3s:  %-9s   %-10s   %-10s  %-10s  %-10s  %-10s"
        for i in xrange(len(self.mass_string)):
            if unblindedStatus:
                print format % (self.mass_string[i], self.observed_string[i], self.expectedMedian_string[i], self.expectedMinus2_string[i], self.expectedMinus1_string[i], self.expectedPlus1_string[i], self.expectedPlus2_string[i])
            else:
                print format % (self.mass_string[i], "BLINDED", self.expectedMedian_string[i], self.expectedMinus2_string[i], self.expectedMinus1_string[i], self.expectedPlus1_string[i], self.expectedPlus2_string[i])
        print
        
    ## Save the table as tex format
    def saveAsLatexTable(self,unblindedStatus=False):
        myLightStatus = True
        if float(self.mass[0]) > 179.0:
	    myLightStatus = False
        
        myDigits = 3
        if myLightStatus:
	    myDigits = 4
        fstr = "%%.%df"%myDigits
        
        format = "%3s "
        for i in range(0,5):
	    format += "& %s "%fstr 
	
        if not unblindedStatus:
	    format += "& Blinded "
	else:
	    format += "& %s "%fstr 
        format += "\\\\ \n"
        s = "% Table autocreated through tools.limits.saveAsLatexTable() \n"
        s += "\\begin{tabular}{ c c c c c c c } \n"
        s += "\\hline \n"
        if myLightStatus:
	    s += "\\multicolumn{7}{ c }{95\\% CL upper limit on $\\BRtH\\times\\BRHtau$}\\\\ \n"
	else:
	    s += "\\multicolumn{7}{ c }{95\\% CL upper limit on $\\sigmaHplus\\times\\BRHtau$}\\\\ \n"
	s += "\\hline \n"
	s += "\\mHpm & \\multicolumn{5}{ c }{Expected limit} & Observed \\\\ \\cline{2-6} \n"
	s += "(GeV)   & $-2\\sigma$  & $-1\\sigma$ & median & +1$\\sigma$ & +2$\\sigma$  & limit \\\\ \n"
	s += "\\hline \n"
        for i in xrange(len(self.mass_string)):
            if unblindedStatus:
                s += format % (self.mass_string[i], float(self.expectedMinus2_string[i]), float(self.expectedMinus1_string[i]), float(self.expectedMedian_string[i]), float(self.expectedPlus1_string[i]), float(self.expectedPlus2_string[i]), float(self.observed_string[i]))
            else:
                s += format % (self.mass_string[i], float(self.expectedMinus2_string[i]), float(self.expectedMinus1_string[i]), float(self.expectedMedian_string[i]), float(self.expectedPlus1_string[i]), float(self.expectedPlus2_string[i]))
	s += "\\hline \n"
        s += "\\end{tabular} \n"
        f = open("limitsTable.tex","w")
        f.write(s)
        f.close()

    ## Divide the limits by another limit to obtain relative result
    # \param refLimit  another BRLimits object
    def divideByLimit(self, refLimit):
        def protectedDivide(num, denom):
            if denom == 0:
                return 0.0
            else:
                return num / denom
        
        if not isinstance(refLimit, BRLimits):
            raise Exception("The parameter needs to be a BRLimits object")
        for i in xrange(len(self.mass_string)):
            foundStatus = False
            for ir in xrange(len(refLimit.mass_string)):
                if self.mass_string[i] == refLimit.mass_string[ir]:
                    foundStatus = True
                    self.observed[i] = protectedDivide(self.observed[i], refLimit.observed[ir])
                    self.expectedMedian[i] = protectedDivide(self.expectedMedian[i], refLimit.expectedMedian[ir])
                    self.expectedMinus2[i] = protectedDivide(self.expectedMinus2[i], refLimit.expectedMinus2[ir])
                    self.expectedMinus1[i] = protectedDivide(self.expectedMinus1[i], refLimit.expectedMinus1[ir])
                    self.expectedPlus2[i] = protectedDivide(self.expectedPlus2[i], refLimit.expectedPlus2[ir])
                    self.expectedPlus1[i] = protectedDivide(self.expectedPlus1[i], refLimit.expectedPlus1[ir])
            if not foundStatus:
                self.observed[i] = 0.0
                self.expectedMedian[i] = 0.0
                self.expectedMinus2[i] = 0.0
                self.expectedMinus1[i] = 0.0
                self.expectedPlus2[i] = 0.0
                self.expectedPlus1[i] = 0.0
        
    ## Construct TGraph for the observed limit
    #
    # \return TGraph of the observed limit, None if the observed limit does not exist
    def observedGraph(self):
        if not hasattr(self, "observed"):
            return None

        gr = ROOT.TGraph(len(self.mass),
                         array.array("d", self.mass),
                         array.array("d", self.observed)
                         )
        setObservedStyle(gr)
        gr.SetName("Observed")

        return gr

    ## Construct Graph for the toy MC stat error of the observed limit
    #
    # \return TGraph of the observed limit stat error, None if the observed limit does not exist
    def observedErrorGraph(self):
        if not hasattr(self, "observedError"):
            return None

        gr = ROOT.TGraph(len(self.mass),
                         array.array("d", self.mass),
                         array.array("d", self.observedError)
                         )
        gr.SetMarkerStyle(21)
        gr.SetMarkerSize(1.5)
        gr.SetMarkerColor(ROOT.kBlack)
        gr.SetLineWidth(3)
        gr.SetLineColor(ROOT.kBlack)
        gr.SetName("ObservedError")

        return gr

    ## Helper function for the expected limits
    #
    # \param postfix   Postfix string for the record names in the JSON file
    # \param sigma     Number for the sigma (0 for median, 1,-1, 2,-2)
    def _expectedGraph(self, postfix, sigma):
        massArray = array.array("d", self.mass)
        massErr = array.array("d", [0]*len(self.mass))
        if sigma == 0:
            gr = ROOT.TGraph(len(self.mass), massArray, array.array("d", getattr(self, "expectedMedian"+postfix)))
            gr.SetName("Expected"+postfix)
        elif sigma == 1:
            gr = ROOT.TGraph(len(self.mass), massArray, array.array("d", getattr(self, "expectedPlus1"+postfix)))
            gr.SetName("ExpectedPlus1Sigma"+postfix)
        elif sigma == -1:
            gr = ROOT.TGraph(len(self.mass), massArray, array.array("d", getattr(self, "expectedMinus1"+postfix)))
            gr.SetName("ExpectedMinus1Sigma"+postfix)
        elif sigma == 2:
            gr = ROOT.TGraph(len(self.mass), massArray, array.array("d", getattr(self, "expectedPlus2"+postfix)))
            gr.SetName("ExpectedPlus2Sigma"+postfix)
        elif sigma == -2:
            gr = ROOT.TGraph(len(self.mass), massArray, array.array("d", getattr(self, "expectedMinus2"+postfix)))
            gr.SetName("ExpectedMinus2Sigma"+postfix)
        else:
            raise Exception("Invalid value of sigma '%d', valid values are 0,1,2" % sigma)

        setExpectedStyle(gr)

        return gr

    ## Construct TGraph for the expected limit
    #
    # \param sigma   Integer for the sigma band (0 for median, 1,-1, 2,-2)
    #
    # \return TGraph of the expexted limit
    def expectedGraph(self, sigma=0):
        return self._expectedGraph("", sigma)

    ## Construct TGraph for the expected limit toy MC stat error
    #
    # \param sigma   Integer for the sigma band (0 for median, 1,-1, 2,-2)
    #
    # \return TGraph of the expexted limit stat error
    def expectedErrorGraph(self, sigma=0):
        if not hasattr(self, "expectedMedianError"):
            return None
        return self._expectedGraph("Error", sigma)

    ## Construct TGraph for the expected +-1/2 sigma bands
    #
    # \param sigma   Integer for the sigma bands (1, 2)
    #
    # \return TGraph for the expected sigma bands
    #
    # The TGraph holds the sigma bands as the values. The values go
    # first through the lower band in the increasing mass order, then
    # the upper band in the decreasing mass order
    def expectedBandGraph(self, sigma):
        massArray = array.array("d", self.mass)
        massErr = array.array("d", [0]*len(self.mass))
        if sigma == 1:
            tmp1 = self.mass[:]
            tmp1.reverse()
            tmp2 = self.expectedPlus1[:]
            tmp2.reverse()

            gr = ROOT.TGraph(2*len(self.mass),
                             array.array("d", self.mass+tmp1),
                             array.array("d", self.expectedMinus1 + tmp2))

            setExpectedGreenBandStyle(gr)
            
            gr.SetName("Expected1Sigma")
        elif sigma == 2:
            tmp1 = self.mass[:]
            tmp1.reverse()
            tmp2 = self.expectedPlus2[:]
            tmp2.reverse()

#            print self.mass+tmp1
#            print self.expectedMinus2+tmp2

            gr = ROOT.TGraph(2*len(self.mass),
                             array.array("d", self.mass+tmp1),
                             array.array("d", self.expectedMinus2 + tmp2))

            setExpectedYellowBandStyle(gr)
            gr.SetName("Expected2Sigma")
        else:
            raise Exception("Invalid value of sigma '%d', valid values are 0,1,2" % sigma)

        return gr
                                          
    # def expectedGraphNew(self, sigma=0):
    #     massArray = array.array("d", self.mass)
    #     massErr = array.array("d", [0]*len(self.mass))
    #     medianArray = array.array("d", self.expectedMedian)
    #     if sigma == 0:
    #         gr = ROOT.TGraph(len(self.mass), massArray, medianArray)
    #         gr.SetName("Expected")
    #     elif sigma == 1:
    #         gr = ROOT.TGraphAsymmErrors(len(self.mass), massArray, medianArray, massErr, massErr,
    #                                     array.array("d", [self.expectedMedian[i]-self.expectedMinus1[i] for i in xrange(len(self.mass))]),
    #                                     array.array("d", [self.expectedPlus1[i]-self.expectedMedian[i] for i in xrange(len(self.mass))]))
    #         gr.SetFillColor(ROOT.kGreen-3)
    #         gr.SetName("Expected1Sigma")
    #     elif sigma == 2:
    #         gr = ROOT.TGraphAsymmErrors(len(self.mass), massArray, medianArray, massErr, massErr,
    #                                     array.array("d", [self.expectedMedian[i]-self.expectedMinus2[i] for i in xrange(len(self.mass))]),
    #                                     array.array("d", [self.expectedPlus2[i]-self.expectedMedian[i] for i in xrange(len(self.mass))]))
    #         gr.SetFillColor(ROOT.kYellow)
    #         gr.SetName("Expected2Sigma")
    #     else:
    #         raise Exception("Invalid value of sigma '%d', valid values are 0,1,2" % sigma)

    #     gr.SetLineStyle(2)
    #     gr.SetLineWidth(3)
    #     gr.SetLineColor(ROOT.kBlack)
    #     gr.SetMarkerStyle(20)

    #     return gr

## Class for reading ML fit output from the JSON file produced by landsReadMLFit.py
class MLFitData:
    def __init__(self, directory="."):
        resultfile="mlfit.json"

        f = open(os.path.join(directory, resultfile))
        self.data = json.load(f)
        f.close()

    def massPoints(self):
        masses = self.data.keys()
        masses.sort()
        return masses

    def fittedGraph(self, mass, backgroundOnly=False, signalPlusBackground=False, heavyHplusMode=False):
        if not backgroundOnly and not signalPlusBackground:
            raise Exception("Either backgroundOnly or signalPlusBackground should be set to True (neither was)")
        if backgroundOnly and signalPlusBackground:
            raise Exception("Either backgroundOnly or signalPlusBackground should be set to True (both were)")
        if signalPlusBackground:
            backgroundOnly = False

        labels = []
        values = []
        uncertainties = []
        
        if backgroundOnly:
            content = self.data[mass]["background"]
            print "MLfit: using as input background-only fit"
        else:
            content = self.data[mass]["signal+background"]
            print "MLfit: using as input signal+background fit"
        labels = content["nuisanceParameters"][:]

        for nuis in labels[:]:
            #if heavyHplusMode and "BinByBin" in nuis:
            #    del labels[labels.index(nuis)]
            #    continue
            if not nuis in content or content[nuis]["type"] == "shapeStat":
                del labels[labels.index(nuis)]
                continue
            values.append(float(content[nuis]["fitted_value"]))
            uncertainties.append(float(content[nuis]["fitted_uncertainty"]))

        yvalues = range(1, len(values)+1)

        yvalues.reverse()

        gr = ROOT.TGraphErrors(len(values),
                               array.array("d", values), array.array("d", yvalues),
                               array.array("d", uncertainties))

        return (gr, labels)

    def fittedGraphShapeStat(self, mass, backgroundOnly=False, signalPlusBackground=False):
        if not backgroundOnly and not signalPlusBackground:
            raise Exception("Either backgroundOnly or signalPlusBackground should be set to True (neither was)")
        if backgroundOnly and signalPlusBackground:
            raise Exception("Either backgroundOnly or signalPlusBackground should be set to True (both were)")
        if signalPlusBackground:
            backgroundOnly = False

        shapeStatNuisance = None
        labels = []
        labels2= []
        values = []
        uncertainties = []
        
        if backgroundOnly:
            content = self.data[mass]["background"]
        else:
            content = self.data[mass]["signal+background"]

        isCombine = False

#        for nuis in content["nuisanceParameters"]:
#            if not nuis in content or content[nuis]["type"] != "shapeStat":
#                continue

###
        labels2 = content["nuisanceParameters"]
        for nuis in labels2:             
            if "Hp" in nuis:
                del labels2[labels2.index(nuis)]
                continue               
            if not nuis in content or content[nuis]["type"] != "shapeStat":
                continue
###

            shapeStatNuisance = nuis
            if "fitted_value" in content[nuis]:
                # combine
                isCombine = True
                labels.append(nuis)
                values.append(float(content[nuis]["fitted_value"]))
                uncertainties.append(float(content[nuis]["fitted_uncertainty"]))
            else:
                # LandS 
                labels = filter(lambda x: x != "type", content[nuis].keys())
                labels.sort(key=lambda x: int(x))

                for l in labels:
                    values.append(float(content[nuis][l]["fitted_value"]))
                    uncertainties.append(float(content[nuis][l]["fitted_uncertainty"]))
    
        if shapeStatNuisance is None:
            raise Exception("No shapeStat nuisance parameters found")

        if isCombine:
            toSort = zip(labels, values, uncertainties)
            def sortKey(tpl):
                i = tpl[0].index("statBin")
                ch = tpl[0][:i]
                bin = int(tpl[0][i+7:])
                return "%s%02d" % (ch, bin) 

            toSort.sort(key=sortKey)
            (labels, values, uncertainties) = zip(*toSort)

        yvalues = range(1, len(values)+1)
        yvalues.reverse()

        gr = ROOT.TGraphErrors(len(values),
                               array.array("d", values), array.array("d", yvalues),
                               array.array("d", uncertainties))

        return (gr, labels, shapeStatNuisance)


class SignificanceData:
    def __init__(self, directory="."):
        resultfile = "significance.json"
        f = open(os.path.join(directory, resultfile))
        self._data = json.load(f)
        f.close()

        self._masses = filter(lambda n: "expectedSignal" not in n, self._data.keys())
        self._masses.sort(key=float)

        self._isHeavyStatus = False
        for m in self._masses:
            if int(m) > 175:
                self._isHeavyStatus = True

    def isHeavyStatus(self):
        return self._isHeavyStatus

    def massPoints(self):
        return self._masses

    def lightExpectedSignal(self):
        return self._data["expectedSignalBrLimit"]
    def heavyExpectedSignal(self):
        return self._data["expectedSignalSigmaBr"]

    def _graph(self, expObs, pvalue):
        masses = self.massPoints()
        massArray = array.array("d", [float(m) for m in masses])
        q = "significance"
        if pvalue:
            q = "pvalue"
        dataArray = array.array("d", [float(self._data[m][expObs][q]) for m in masses])

        gr = ROOT.TGraph(len(masses), massArray, dataArray)
        gr.SetLineWidth(3)
        gr.SetLineColor(ROOT.kBlack)
        return gr

    def expectedGraph(self, pvalue=False):
        gr = self._graph("expected", pvalue)
        gr.SetLineStyle(2)
        gr.SetMarkerStyle(20)
        return gr

    def observedGraph(self, pvalue=False):
        gr = self._graph("observed", pvalue)
        gr.SetMarkerStyle(21)
        gr.SetMarkerSize(1.5)
        return gr
    
    def fittedGraphShapeBinByBinHeavy(self, mass, backgroundOnly=False, signalPlusBackground=False):
        if not backgroundOnly and not signalPlusBackground:
            raise Exception("Either backgroundOnly or signalPlusBackground should be set to True (neither was)")
        if backgroundOnly and signalPlusBackground:
            raise Exception("Either backgroundOnly or signalPlusBackground should be set to True (both were)")
        if signalPlusBackground:
            backgroundOnly = False

        labels = []
        values = []
        uncertainties = []
        
        if backgroundOnly:
            content = self.data[mass]["background"]
        else:
            content = self.data[mass]["signal+background"]
        labels = content["nuisanceParameters"][:]

        for nuis in labels[:]:
            if not "BinByBin" in nuis:
                del labels[labels.index(nuis)]
                continue     
            if not nuis in content or content[nuis]["type"] == "shapeStat":
                del labels[labels.index(nuis)]
                continue
            values.append(float(content[nuis]["fitted_value"]))
            uncertainties.append(float(content[nuis]["fitted_uncertainty"]))

        yvalues = range(1, len(values)+1)

        yvalues.reverse()

        gr = ROOT.TGraphErrors(len(values),
                               array.array("d", values), array.array("d", yvalues),
                               array.array("d", uncertainties))

        return (gr, labels)


## Remove mass points lower than 100
#
# \param graph   TGraph to operate
# \param minX    Minimum value of mass hypotheses to keep
#
# Remove mass points lower than 100 since
# statisticalFunctions.tanbForBR cannot handle them (they are unphysical)
# also remove points lower than 115 since excluded by LEP
def cleanGraph(graph, minX=95):
    i=0
    while (i<graph.GetN()):
        if (graph.GetX()[i]<minX):
            graph.RemovePoint(i)
        else:
            i=i+1        

## Construct observed - 1sigma theory uncertainty band
#
# \param graph   TGraph of the observed BR limit
#
# \return Clone of the TGraph for the -1sigma theory uncertainty band
def getObservedMinus(graph,uncertainty):
    curve = graph.Clone()
    curve.SetName(curve.GetName()+"TheoryMinus")
    for i in xrange(0, graph.GetN()):
        curve.SetPoint(i,
                       graph.GetX()[i],
                       graph.GetY()[i]*(1-uncertainty))
    print "todo: CHECK minus coefficient f(m)"
    return curve

## Construct observed + 1sigma theory uncertainty band
#
# \param graph   TGraph of the observed BR limit
#
# \return Clone of the TGraph for the +1sigma theory uncertainty band
def getObservedPlus(graph,uncertainty):
    curve = graph.Clone()
    curve.SetName(curve.GetName()+"TheoryPlus")
    for i in xrange(0, graph.GetN()):
        curve.SetPoint(i,
                       graph.GetX()[i],
                       graph.GetY()[i]*(1+uncertainty))
    print "todo: CHECK plus coefficient f(m)"
    return curve

## Create a TGraph for upper limit tanb y values from a TGraph with BR y values
#
# \param graph           TGraph for the BR limit
# \param mymu            Value of mu
# \param removeNotValid  Remove invalid points (points for which statisticalFunctions.tanbForBR() fails
#
# \return Clone of the TGraph for the tanb limit
# 
# Convention: begin with low mH, lower limit for 1/2s band
# then go counterclockwise: increase mH, then switch to upper limit, decrease mH
def graphToTanBeta(graph, mymu, removeNotValid=True):
    # Don't modify the original
    graph = graph.Clone()

    # Loop over the graph points
    yvalues = graph.GetY()
    tanbRef = 20 # initial guess
    for i in xrange(0, graph.GetN()):
        mass = graph.GetX()[i]
        # For some reason tanbForBR gets stuck for some large values; solution: do not
        # even bother to calculate values for Br>=0.5
        if yvalues[i]<0.50:
            tanb = statisticalFunctions.tanbForBR(yvalues[i], int(mass), tanbRef, mymu)
        else:
            tanb = -1
#        print "mass %d, BR %f, tanb %f, %d / %d" % (mass, yvalues[i], tanb, i, graph.GetN())
#        if tanb < 0:
#           print "No valid tanb for BR %f" % yvalues[i]

        graph.SetPoint(i, mass, tanb)

    # For points for which a valid tanb value can not be obtained,
    # either remove the point, or set a huge value
    if removeNotValid:
        found = True
        while found:
            found = False
            for i in xrange(0, graph.GetN()):
                if graph.GetY()[i] < 0:
                    graph.RemovePoint(i)
                    found = True
                    break
    else:
        for i in xrange(0, graph.GetN()):
            if graph.GetY()[i] < 0:
                # set huge value or zero
                if 2*i>=graph.GetN():
                    graph.SetPoint(i, graph.GetX()[i], 1e6)
                else:
                    graph.SetPoint(i, graph.GetX()[i], 0.0)
                
    return graph

## Convert from mH+ space to mA
#
# \param graph   TGraph with mH+ to be modified
def graphToMa(graph):
    for i in xrange(0, graph.GetN()):
        mH = graph.GetX()[i]
        tanb = graph.GetY()[i]
        mZ = 91.1876 #Z mass from PDG
        mW = 80.398
        print mH, tanb, "BR: ", BRdataInterface.get_mA(mH,tanb,200)
        ### Tree level relation, HO correction available from values calculated with FH, should use it. 20.6.2012/S.Lehti
	### mA = math.sqrt(mH*mH - mW*mW)
	mA = BRdataInterface.get_mA(mH,tanb,200)
        graph.SetPoint(i, mA, tanb)

## Convert from mA space to mH+
#
# \param graph   TGraph with mA to be modified
def graphToMh(graph):
    print "File tools/limit.py, function graphToMh"
    print "Do not use until the mass calculation is fixed. This function should not be needed anyway. 20.6.2012/S.Lehti"
    sys.exit()
    for i in xrange(0, graph.GetN()):
        mA = graph.GetX()[i]
        tanb = graph.GetY()[i]
        mZ = 91.1876 #Z mass from PDG
        mW = 80.398
        print mA, mZ, i, graph.GetN()
        mH = math.sqrt(mA*mA + mW*mW)
        graph.SetPoint(i, mH, tanb)

## Divide two TGraphs
#
# \param num    Numerator TGraph
# \param denom  Denominator TGraph
#
# \return new TGraph as the ratio of the two TGraphs
def divideGraph(num, denom):
    gr = ROOT.TGraph(num)
    for i in xrange(gr.GetN()):
        y = denom.GetY()[i]
        val = 0
        if y != 0:
            val = gr.GetY()[i]/y
        gr.SetPoint(i, gr.GetX()[i], val)
    return gr


## Returns a properly typeset label for MSSM scenario
#
# \param scenario   string of the scenario rootfile name
#
# \return string with the typeset name
def getTypesetScenarioName(scenario):
    myTruncatedScenario = scenario.replace("-LHCHXSWG","")
    if myTruncatedScenario == "lightstau":
        return "MSSM light stau"
    if myTruncatedScenario == "lightstop":
        return "MSSM light stop"
    if myTruncatedScenario == "lowMH":
        return "MSSM low-M_{H}"
    if myTruncatedScenario == "mhmaxup":
        return "MSSM updated ^{}m_{h}^{max}"
    if myTruncatedScenario == "mhmodm":
        return "MSSM ^{}m_{h}^{mod-}"
    if myTruncatedScenario == "mhmodp":
        return "MSSM ^{}m_{h}^{mod+}"
    if myTruncatedScenario == "tauphobic":
        return "MSSM #tau-phobic"
    raise Exception("The typeset name for scenario '%s' is not defined in tools/limit.py::getTypesetScenarioName()! Please add it."%scenario)


## Plots tan beta plot
#
# \param name    string of filename prefix for plot
# \param graphs  dictionary of TGraph objects
# \param luminosity luminosity for plot
# \param finalstateText label of final state
# \param xlabel  x-axis label
# \param scenario name of scenario
def doTanBetaPlotHeavy(name, graphs, luminosity, finalstateText, xlabel, scenario):
    doTanBetaPlotGeneric(name, graphs, luminosity, finalstateText, xlabel, scenario, regime="heavy")

## Plots tan beta plot
#
# \param name    string of filename prefix for plot
# \param graphs  dictionary of TGraph objects
# \param luminosity luminosity for plot
# \param finalstateText label of final state
# \param xlabel  x-axis label
# \param scenario name of scenario
def doTanBetaPlotLight(name, graphs, luminosity, finalstateText, xlabel, scenario):
    doTanBetaPlotGeneric(name, graphs, luminosity, finalstateText, xlabel, scenario, regime="light")

## Plots tan beta plot
#
# \param name    string of filename prefix for plot
# \param graphs  dictionary of TGraph objects
# \param luminosity luminosity for plot
# \param finalstateText label of final state
# \param xlabel  x-axis label
# \param scenario name of scenario
def doTanBetaPlotGeneric(name, graphs, luminosity, finalstateText, xlabel, scenario, regime):
    # Enable OpenGL
    #if opts.excludedArea:
    ROOT.gEnv.SetValue("OpenGL.CanvasPreferGL", 1)
    
    isHeavy = regime != "light"
    tanbMax = 65

    if forPaper:
        histograms.cmsTextMode = histograms.CMSMode.PAPER

    blinded = True
    if "obs" in graphs.keys():
        blinded = False

    higgs = "h"
    if scenario == "lowMH-LHCHXSWG":
        higgs = "H"

    if not blinded:    
        obs = graphs["obs"]
        excluded = ROOT.TGraph(obs)
        excluded.SetName("ExcludedArea")


        for i in reversed(range(excluded.GetN())):
            yValue = excluded.GetY()[i]
            if (yValue > 99 or yValue < 0) and i+1 < excluded.GetN():
                excluded.RemovePoint(i+1)

        if isHeavy:
    #        excluded.SetPoint(excluded.GetN(), obs.GetX()[obs.GetN()-1], 100)
    #        excluded.SetPoint(excluded.GetN(), 0, 100)
    #        excluded.SetPoint(excluded.GetN(), 0, obs.GetY()[0])
            excluded.SetPoint(excluded.GetN(), 140, 65)
            excluded.SetPoint(excluded.GetN(), obs.GetX()[0], obs.GetY()[0])
        else:
            if "_mA_" in name:
                rightX = obs.GetX()[obs.GetN()-1]+100
                rightY = obs.GetY()[obs.GetN()-1]
                excluded.SetPoint(excluded.GetN(), rightX, rightY)
                excluded.SetPoint(excluded.GetN(), rightX, 1)
            else:
                excluded.SetPoint(excluded.GetN(), obs.GetX()[obs.GetN()-1], 1)
            excluded.SetPoint(excluded.GetN(), 0, 1)
            excluded.SetPoint(excluded.GetN(), 0, tanbMax)
            excluded.SetPoint(excluded.GetN(), obs.GetX()[0], tanbMax)
            excluded.SetPoint(excluded.GetN(), obs.GetX()[0], obs.GetY()[0])

        #for i in range(excluded.GetN()):
            #print "Excluded",excluded.GetX()[i],excluded.GetY()[i]

        setExcludedStyle(excluded)
        excluded.SetLineWidth(0)
        excluded.SetLineColor(ROOT.kBlack)

    
    expected = graphs["exp"]
    setExpectedStyle(expected)
    expected1 = graphs["exp1"]
    setExpectedGreenBandStyle(expected1)
    expected2 = graphs["exp2"]
    setExpectedYellowBandStyle(expected2)

    allowed = graphs["Allowed"]
    allowed.SetFillStyle(3005)
    allowed.SetFillColor(ROOT.kRed)
    allowed.SetLineWidth(-302)
    allowed.SetLineColor(ROOT.kRed)
    allowed.SetLineStyle(1)

    setExpectedStyle(graphs["exp"])
    

    if not blinded:
        setTheoreticalErrorStyle(graphs["obs_th_plus"])
        setTheoreticalErrorStyle(graphs["obs_th_minus"])
        setObservedStyle(graphs["obs"])
        
        # plots
        plotsList = []
        plotsList.append(histograms.HistoGraph(graphs["obs"], "Observed", drawStyle="PL", legendStyle="lp"))
        
        if "obs_th_plus" in graphs.keys():
            plotsList.extend([histograms.HistoGraph(graphs["obs_th_plus"], "ObservedPlus", drawStyle="L", legendStyle="l"),
                              histograms.HistoGraph(graphs["obs_th_minus"], "ObservedMinus", drawStyle="L")])
        if "isomass" in graphs.keys():
            plotsList.extend([histograms.HistoGraph(graphs["isomass"], "IsoMass", drawStyle="L"),
                              histograms.HistoGraph(graphs["isomass"], "IsoMassCopy", drawStyle="F")])
        plotsList.extend([histograms.HistoGraph(excluded, "Excluded", drawStyle="F", legendStyle="f"),
                          histograms.HistoGraph(expected, "Expected", drawStyle="L"),
                          histograms.HistoGraph(graphs["Allowed"], "Allowed", drawStyle="L", legendStyle="lf"),
                          #histograms.HistoGraph(graphs["Allowed"], "AllowedCopy", drawStyle="L", legendStyle="f"),
                          histograms.HistoGraph(expected1, "Expected1", drawStyle="F", legendStyle="fl"),
                          histograms.HistoGraph(expected2, "Expected2", drawStyle="F", legendStyle="fl")])
        plot = plots.PlotBase(plotsList, saveFormats=[".png", ".pdf", ".C"])

        plot.histoMgr.setHistoLegendLabelMany({
            "ObservedPlus": "Observed #pm1#sigma (th.)",
            "ObservedMinus": None,
            "Expected": None,
            "Allowed": "m_{"+higgs+"}^{MSSM} #neq 125#pm3 GeV",
            "Expected1": "Expected median #pm 1#sigma",
            "Expected2": "Expected median #pm 2#sigma",
            "IsoMass": None,
            "IsoMassCopy": None
            })
    else:
        if not graphs["isomass"] == None:
            graphs["isomass"].SetFillColor(0)
            graphs["isomass"].SetFillStyle(1)
        # plots
        plotsList = []
        if "isomass" in graphs.keys():
            plotsList.extend([histograms.HistoGraph(graphs["isomass"], "IsoMass", drawStyle="L"),
                              histograms.HistoGraph(graphs["isomass"], "IsoMassCopy", drawStyle="F")])
        plotsList.extend([histograms.HistoGraph(excluded, "Excluded", drawStyle="F", legendStyle="f"),
                          histograms.HistoGraph(expected, "Expected", drawStyle="L"),
                          histograms.HistoGraph(graphs["Allowed"], "Allowed", drawStyle="L", legendStyle="lf"),
                          #histograms.HistoGraph(graphs["Allowed"], "AllowedCopy", drawStyle="L", legendStyle="f"),
                          histograms.HistoGraph(expected1, "Expected1", drawStyle="F", legendStyle="fl"),
                          histograms.HistoGraph(expected2, "Expected2", drawStyle="F", legendStyle="fl")])

        plot = plots.PlotBase(plotsList, saveFormats=[".png", ".pdf", ".C"])

        plot.histoMgr.setHistoLegendLabelMany({
            "Expected": None,
            "Allowed": "m_{"+higgs+"}^{MSSM} #neq 125#pm3 GeV",
            "Expected1": "Expected median #pm 1#sigma",
            "Expected2": "Expected median #pm 2#sigma",
            "IsoMass": None,
            "IsoMassCopy": None
            })

    # Move the m_h,H allowed region to the last in the legend
    histoNames = [h.getName() for h in plot.histoMgr.getHistos()]
    plot.histoMgr.reorderLegend(filter(lambda n: "Allowed" not in n, histoNames))

    captionLineSpacing = 0.042
    captionLines = 3
    if isinstance(finalstateText, list):
        captionLines += len(finalstateText) - 1

    if isHeavy:
        x = 0.50
        y = -0.11
        #if scenario.replace("-LHCHXSWG", "") in ["lightstop", "mhmaxup"]:
        #    y += 0.05
    else:
        x = 0.2
        y = -0.15
    plot.setLegend(histograms.createLegend(x-0.01, y+0.65-(captionLines-0.2)*captionLineSpacing, x+0.45, y+0.9-(captionLines-0.2)*captionLineSpacing))
    plot.legend.SetMargin(0.17)

    #plot.legend.SetFillColor(0)
    #plot.legend.SetFillStyle(1001)
    if blinded:
        name += "_blinded"
    name = os.path.basename(name)
    name = name.replace("-","_")
    
    if isHeavy:
        frameXmin = 200
        if "_mA_" in name:
            frameXmin = 140
        plot.createFrame(name, opts={"ymin": 1, "ymax": tanbMax, "xmin": frameXmin, "xmax": 600})
    else:
        frameXmax = 160
        if "_mA_" in name:
            frameXmax = 145
        plot.createFrame(name, opts={"ymin": 1, "ymax": tanbMax, "xmin": 90, "xmax": frameXmax})

    plot.frame.GetXaxis().SetTitle(xlabel)
    plot.frame.GetYaxis().SetTitle(tanblimit)

    plot.draw()
    
    plot.setLuminosity(luminosity)
    plot.addStandardTexts(cmsTextPosition="right")
#    histograms.addLuminosityText(x=None, y=None, lumi="2.3-4.9")

    size = 20
    if regime == "light":
        histograms.addText(x, y+0.9, process, size=size)
    elif regime == "heavy":
        histograms.addText(x, y+0.9, processHeavy, size=size)
    elif regime == "combination":
        histograms.addText(x, y+0.9, processCombination, size=size)
    else:
        raise Exception("Unknown option for regime")
    y -= captionLineSpacing
    if isinstance(finalstateText, str):
        histograms.addText(x, y+0.9, finalstateText, size=size)
        y -= captionLineSpacing
    elif isinstance(finalstateText, list):
        for l in finalstateText:
            histograms.addText(x, y+0.9, l, size=size)
            y -= captionLineSpacing
    else:
        raise Exception("not implemented")
    histograms.addText(x, y+0.895, "^{}%s"%getTypesetScenarioName(scenario), size=size)
#    histograms.addText(0.2, 0.231, "Min "+limit.BR+"(t#rightarrowH^{+}b)#times"+limit.BR+"(H^{+}#rightarrow#tau#nu)", size=0.5*size)

    # Too small to be visible
#    if not graphs["isomass"] == None:
#        histograms.addText(0.2, 0.15, "m_{H^{#pm}} = 180 GeV/c^{2}", size=0.5*size)

    #Adding a LHC label:
#    ROOT.LHCHIGGS_LABEL(0.97,0.72,1)
    #FH_version = db.getVersion("FeynHiggs")
    #histograms.addText(x, y+0.55, FH_version, size=size)
#    HD_version = db.getVersion("HDECAY")
#    histograms.addText(x, y+0.55, FH_version+" and", size=size)
#    histograms.addText(x, y+0.50, HD_version, size=size)
#    histograms.addText(x, 0.48, "Derived from", size=size)
#    histograms.addText(x, 0.43, "CMS HIG-12-052", size=size)

    plot.save()

    print "Created",name
    
