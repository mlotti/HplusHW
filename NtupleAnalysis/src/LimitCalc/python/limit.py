'''
\package limit
Various tools for plotting BR/tanbeta limits

Some of the settings depend on the \a forPaper boolean flag. All of
these are functions, so user can override the flag in a script.
'''

#================================================================================================ 
# Import modules
#================================================================================================ 
import os
import math
import json
import array

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.NtupleAnalysis.tools.statisticalFunctions as statisticalFunctions
import HiggsAnalysis.LimitCalc.BRdataInterface as BRdataInterface
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux


#================================================================================================ 
# Global Definitions
#================================================================================================ 
verbose = False

# Flag for stating if the plots are for paper (True) or not (False)
forPaper = True

# Label for branching fraction
BR = "#it{B}"

# Label for H+ decay mode
hplusDecayMode = "H^{+} #rightarrow #tau^{+}#nu_{#tau}"
# hplusDecayMode = "H^{+} #rightarrow tb" #fixme: alexandros

# The label for the physics process
process            = "t #rightarrow H^{+}b, %s" % hplusDecayMode
processHeavy       = "pp #rightarrow #bar{t}(b)H^{+}, %s" % hplusDecayMode
processCombination = "pp #rightarrow #bar{t}(b)H^{+}"

# Label for the H+->tau BR assumption. fixme: alexandros (does not seem to work!)
BRassumption = ""
#BRassumption = "%s(H^{+} #rightarrow #tau#nu) = 1" % BR

# Y axis label for the BR
BRlimit = None

# Y axis label for the sigma x BR
sigmaBRlimit = None

# Y axis label for the tanbeta
tanblimit = "tan #beta"
#tanblimit = "95 % CL limit on tan #beta"

# Labels for the final states
_finalstateLabels = {
    "taujets": "^{}#tau_{h}+jets",
    "etau"   : "e^{}#tau_{h}",
    "mutau"  : "#mu^{}#tau_{h}",
    "emu"    : "e#mu",
}

# Default y axis maximum values for BR limit for the final states
_finalstateYmaxBR = {
    "etau"   : 0.4,
    "mutau"  : 0.4,
    "emu"    : 0.8,
    "default": 0.1,
}

# Default y axis maximum values for sigma x BR limit for the final states
_finalstateYmaxSigmaBR = {
    "etau"   : 10.0, # FIXME
    "mutau"  : 10.0, # FIXME
    "emu"    : 10.0, # FIXME
    "default":  1.0,
}


#================================================================================================ 
# Function Definitions
#================================================================================================ 
def Verbose(msg, printHeader=False):
    '''
    Calls Print() only if verbose options is set to true.
    '''
    if not verbose:
        return
    Print(msg, printHeader)
    return


def Print(msg, printHeader=True):
    '''
    Simple print function. If verbose option is enabled prints, otherwise does nothing.
    '''
    fName = __file__.split("/")[-1]
    if printHeader:
        print "=== ", fName
    print "\t", msg
    return


def massUnit():
    '''
    Unit for mass (GeV vs. GeV/c^2
    '''
    if forPaper:
        return "GeV"
    return "GeV/c^{2}"


def useParentheses():
    global BRlimit, sigmaBRlimit
    BRlimit      = "95%% CL limit on %s(t#rightarrowH^{+}b)#times%s(%s)" % (BR, BR, hplusDecayMode)
    sigmaBRlimit = "95%% CL limit on #sigma(H^{+})#times%s(%s) (pb)" % (BR, hplusDecayMode)
    return

    
def useSubscript():
    global BRlimit, sigmaBRlimit
    BRlimit      = "95%% CL limit on %s_{t#rightarrowH^{+}b}#times%s_{%s}" % (BR, BR, hplusDecayMode)
    sigmaBRlimit = "95%% CL limit on #sigma_{H^{+}}#times%s_{%s} (pb)" % (BR, hplusDecayMode)
    return

useSubscript()

def mHplus():
    '''
    Label for m(H+)
    '''
    label = "m_{H^{+}} (%s)" % massUnit()
    return label


def mA():
    '''
    Label for m(A)
    '''
    label = "m_{A} (%s)" % massUnit() 
    return label


def setExcludedStyle(graph):
    ci = ROOT.TColor.GetColor(156, 156, 156)
    # ci = ROOT.TColor.GetColor(209, 209, 209)
    graph.SetFillColorAlpha(ci, 0.3) # transparency
    # graph.SetFillColorAlpha(ROOT.kViolet+6, 0.3) # transparency
    # graph.SetLineWidth(0)
    # graph.SetLineColor(ROOT.kBlack)
    return


def setObservedStyle(graph):
    graph.SetMarkerStyle(21)
    graph.SetMarkerSize(1.3)
    graph.SetMarkerColor(ROOT.kBlack)
    graph.SetLineWidth(3)
    graph.SetLineColor(ROOT.kBlack)
    return
    

def setTheoreticalErrorStyle(graph):
    graph.SetLineStyle(9)
    graph.SetLineWidth(2)
    return


def setExpectedStyle(graph):
    graph.SetLineStyle(2)
    graph.SetLineWidth(3)
    graph.SetLineColor(ROOT.kBlack)
    graph.SetMarkerStyle(20)
    return


def setExpectedGreenBandStyle(graph):
    graph.SetFillColor(ROOT.kGreen-3)
    setExpectedStyle(graph)
    return
    

def setExpectedYellowBandStyle(graph):
    graph.SetFillColor(ROOT.kYellow)
    setExpectedStyle(graph)
    return


#================================================================================================ 
# Class Definition
#================================================================================================ 
class BRLimits:
    '''
    Class for reading the BR limits from the JSON file produced by
    landsMergeHistograms.py
    '''
    def __init__(self, directory=".", excludeMassPoints=[], limitsfile="limits.json", configfile="configuration.json"):
        '''
        Constructor

        \param directory          Path to the multicrab task directory with the JSON files
         
        \param excludeMassPoints  List of strings for mass points to exclude
        '''
        resultfile="limits.json"
        #configfile="configuration.json"

        # Open limits file
        msg = "Opening file '%s'" % (limitsfile)
        Print(msg, True)
        f = open(os.path.join(directory, limitsfile), "r")
        limits = json.load(f)
        f.close()

        self.lumi = float(limits["luminosity"])
        self.mass = limits["masspoints"].keys()
        self.isHeavyStatus = False
        
        # Check if light or heavy H+
        for m in self.mass:
            if int(m) > 175:
                self.isHeavyStatus = True
        members = ["mass"]

        # Sort mass
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
        
        self.expectedMedian = [limits["masspoints"][m]["expected"]["median"]  for m in self.mass]
        self.expectedMinus2 = [limits["masspoints"][m]["expected"]["-2sigma"] for m in self.mass]
        self.expectedMinus1 = [limits["masspoints"][m]["expected"]["-1sigma"] for m in self.mass]
        self.expectedPlus1  = [limits["masspoints"][m]["expected"]["+1sigma"] for m in self.mass]
        self.expectedPlus2  = [limits["masspoints"][m]["expected"]["+2sigma"] for m in self.mass]
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

       
        # Open configuration json file
        msg = "Opening file '%s' for input" % (os.path.join(directory, configfile))
        Print(msg, True)
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
        return


    def getLuminosity(self):
        '''
        Get the integrated luminosity in 1/pb
        '''
        return self.lumi


    def getFinalstates(self):
        '''
        Get the list of final states
        '''
        return self.finalstates


    def getFinalstateText(self):
        '''
        Get the label of the final states
        '''
        if len(self.finalstates) <= 1:
            return "%s final state" % _finalstateLabels[self.finalstates[0]]

        ret = ", ".join([_finalstateLabels[x] for x in self.finalstates[:-1]])
        ret += ", and %s final states" % _finalstateLabels[self.finalstates[-1]]
        return ret


    def getFinalstateYmaxBR(self):
        '''
        Get the maximum value for Y axis for the BR limit
        '''
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


    def print2(self,unblindedStatus=False):
        '''
        Print the BR limits
        '''
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
        return


    def getLimitsTable(self, unblindedStatus=False, nDigits=5):
        '''
        Returns a table (list) with the BR limits
        '''
        width  = nDigits + 6
        align  = "{:<8} {:>%s} {:>%s} {:>%s} {:>%s} {:>%s} {:>%s}" % (width, width, width, width, width, width)
        header = align.format("Mass", "Observed", "Median", "-2sigma", "-1sigma", "+1sigma", "+2sigma")
        hLine  = "="*len(header)

        # Define precision
        precision = "%%.%df" % nDigits

        # Create the results table
        table  = []
        table.append(hLine)
        table.append(header)
        table.append(hLine)
        for i in xrange(len(self.mass_string)):
            mass = self.mass_string[i]
            if unblindedStatus:
                observed = self.observed_string[i]
            else:
                observed = "BLINDED"
            median       = precision % (self.expectedMedian_string[i])
            sigma2minus  = precision % (self.expectedMinus2_string[i])
            sigma1minus  = precision % (self.expectedMinus1_string[i])
            sigma1plus   = precision % (self.expectedPlus1_string[i])
            sigma2plus   = precision % (self.expectedPlus2_string[i])

            # Append results
            row = align.format(mass, observed, median, sigma2minus, sigma1minus, sigma1plus, sigma2plus)
            table.append(row)
        table.append(hLine)
        return table


    def printLimits(self, unblindedStatus=False, nDigits=5):
        '''
        Print the BR limits table
        '''
        table = self.getLimitsTable(unblindedStatus, nDigits)
        # Print limits (row by row)
        for row in table:
            print row
        return

        
    def isLightHPlus(self, mass):
        isLight = True
        if float(mass) > 179.0:
	    isLight = False
        return isLight
        

    def saveAsLatexTable(self, unblindedStatus=False, nDigits=3):
        '''
        Save the table as tex format
        '''        
        myDigits = nDigits
        isLightHplus  = self.isLightHPlus(self.mass[0])
        if isLightHplus and nDigits==3:
	    myDigits += 1

        # Define precision of results
        precision = "%%.%df" % myDigits
        format    = "%3s "

        # Five columns (+/-2sigma, +/-1sigma, median)
        for i in range(0,5):
	    format += "& %s "%precision 
	
        # Blinded column
        if not unblindedStatus:
	    format += "& Blinded "
	else:
	    format += "& %s " % precision 

        # End-line character (\\)
        format += "\\\\ \n"

        # Add the LaTeX table contents
        s  = "% Table autocreated by HiggsAnalysis.LimitCalc.limit.saveAsLatexTable() \n"
        s += "\\begin{tabular}{ c c c c c c c } \n"
        s += "\\hline \n"
        if isLightHplus:
	    s += "\\multicolumn{7}{ c }{95\\% CL upper limit on $\\BRtH\\times\\BRHtau$}\\\\ \n"
	else:
	    s += "\\multicolumn{7}{ c }{95\\% CL upper limit on $\\sigmaHplus\\times\\BRHtau$}\\\\ \n"
	s += "\\hline \n"
	s += "\\mHpm & \\multicolumn{5}{ c }{Expected limit} & Observed \\\\ \\cline{2-6} \n"
	s += "(GeV)   & $-2\\sigma$  & $-1\\sigma$ & median & +1$\\sigma$ & +2$\\sigma$  & limit \\\\ \n"
	s += "\\hline \n"

        # Get the limit values
        for i in xrange(len(self.mass_string)):
            mass     = self.mass_string[i]
            eMinus2  = float( precision % (self.expectedMinus2_string[i]) )
            eMinus1  = float( precision % (self.expectedMinus1_string[i]) )
            eMedian  = float( precision % (self.expectedMedian_string[i]) )
            ePlus1   = float( precision % (self.expectedPlus1_string[i]) )
            ePlus2   = float( precision % (self.expectedPlus2_string[i]) )
            observed = float( self.observed_string[i]) 
            if unblindedStatus:
                s += format % (mass, eMinus2, eMinus1, eMedian, ePlus1, ePlus2, observed)
            else:
                s += format % (mass, eMinus2, eMinus1, eMedian, ePlus1, ePlus2)
	s += "\\hline \n"
        s += "\\end{tabular} \n"

        fileName = "limitsTable.tex"
        openMode = "w"  
        Verbose("Opening file '%s' in mode '%s'" % (fileName, openMode), True)
        f = open(fileName, openMode)
        f.write(s)
        f.close()
        Print("Wrote LaTeX table in file '%s'" % (fileName), True)
        return


    def divideByLimit(self, refLimit):
        '''
        Divide the limits by another limit to obtain relative result
        \param refLimit  another BRLimits object
        '''
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
        return
        

    def observedGraph(self):
        '''
        Construct TGraph for the observed limit
        \return TGraph of the observed limit, None if the observed limit does not exist
        '''
        if not hasattr(self, "observed"):
            return None

        gr = ROOT.TGraph(len(self.mass),
                         array.array("d", self.mass),
                         array.array("d", self.observed)
                         )
        setObservedStyle(gr)
        gr.SetName("Observed")
        return gr


    def observedErrorGraph(self):
        '''
        Construct Graph for the toy MC stat error of the observed limit

        \return TGraph of the observed limit stat error, None if the observed limit does not exist
        '''
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


    def _expectedGraph(self, postfix, sigma):
        '''
        Helper function for the expected limits
        
        \param postfix   Postfix string for the record names in the JSON file
        \param sigma     Number for the sigma (0 for median, 1,-1, 2,-2)
        '''
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


    def expectedGraph(self, sigma=0):
        '''
        Construct TGraph for the expected limit
        
        \param sigma   Integer for the sigma band (0 for median, 1,-1, 2,-2)
        
        \return TGraph of the expexted limit
        '''
        return self._expectedGraph("", sigma)


    def expectedErrorGraph(self, sigma=0):
        '''
        Construct TGraph for the expected limit toy MC stat error
        
        \param sigma   Integer for the sigma band (0 for median, 1,-1, 2,-2)
        
        \return TGraph of the expexted limit stat error
        '''
        if not hasattr(self, "expectedMedianError"):
            return None
        return self._expectedGraph("Error", sigma)


    def expectedBandGraph(self, sigma):
        '''
        Construct TGraph for the expected +-1/2 sigma bands
        
        \param sigma   Integer for the sigma bands (1, 2)
        
        \return TGraph for the expected sigma bands
        
        The TGraph holds the sigma bands as the values. The values go
        first through the lower band in the increasing mass order, then
        the upper band in the decreasing mass order
        '''
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


#================================================================================================ 
# Class Definition
#================================================================================================ 
class MLFitData:
    '''
    Class for reading ML fit output from the JSON file produced by landsReadMLFit.py
    '''
    def __init__(self, directory="."):
        resultfile="mlfit.json"

        f = open(os.path.join(directory, resultfile))
        self.data = json.load(f)
        f.close()
        return


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
            #if "Hp" in nuis:
                #del labels2[labels2.index(nuis)]
                #continue               
            #if not nuis in content or content[nuis]["type"] != "shapeStat":
                #continue
            if not "statBin" in nuis:
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
    
        #if shapeStatNuisance is None:
        #    raise Exception("No shapeStat nuisance parameters found")

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


#================================================================================================ 
# Class Definition
#================================================================================================ 
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
        return


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


def cleanGraph(graph, massPoint):
    '''
    Remove mass points lower than 100
    
    \param graph   TGraph to operate
    \param minX    Minimum value of mass hypotheses to keep
    
    Remove mass points lower than 100 since
    statisticalFunctions.tanbForBR cannot handle them (they are unphysical)
    also remove points lower than 115 since excluded by LEP    
    '''
    i=0
    while (i<graph.GetN()):
        if (graph.GetX()[i] > massPoint-0.01 and graph.GetX()[i] < massPoint+0.01):
            graph.RemovePoint(i)
        else:
            i=i+1
    return


def getObservedMinus(graph,uncertainty):
    '''
    Construct observed - 1sigma theory uncertainty band
    
    \param graph   TGraph of the observed BR limit
    
    \return Clone of the TGraph for the -1sigma theory uncertainty band
    '''
    curve = graph.Clone()
    curve.SetName(curve.GetName()+"TheoryMinus")
    for i in xrange(0, graph.GetN()):
        curve.SetPoint(i,
                       graph.GetX()[i],
                       graph.GetY()[i]*(1-uncertainty))
    print "todo: CHECK minus coefficient f(m)"
    return curve

def getObservedPlus(graph,uncertainty):
    '''
    Construct observed + 1sigma theory uncertainty band
    
    \param graph   TGraph of the observed BR limit
    
    \return Clone of the TGraph for the +1sigma theory uncertainty band
    '''
    curve = graph.Clone()
    curve.SetName(curve.GetName()+"TheoryPlus")
    for i in xrange(0, graph.GetN()):
        curve.SetPoint(i,
                       graph.GetX()[i],
                       graph.GetY()[i]*(1+uncertainty))
    print "todo: CHECK plus coefficient f(m)"
    return curve


def graphToTanBeta(graph, mymu, removeNotValid=True):
    '''
    Create a TGraph for upper limit tanb y values from a TGraph with BR y values

    \param graph           TGraph for the BR limit
    \param mymu            Value of mu
    \param removeNotValid  Remove invalid points (points for which statisticalFunctions.tanbForBR() fails
    
    \return Clone of the TGraph for the tanb limit
    
    Convention: begin with low mH, lower limit for 1/2s band
    then go counterclockwise: increase mH, then switch to upper limit, decrease mH
    '''
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


def graphToMa(graph):
    '''
    Convert from mH+ space to mA
    
    \param graph   TGraph with mH+ to be modified
    '''
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
    return

def graphToMh(graph):
    '''
    Convert from mA space to mH+
    
    \param graph   TGraph with mA to be modified
    '''
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
    return


def divideGraph(num, denom):
    '''
    Divide two TGraphs
    
     \param num    Numerator TGraph
     \param denom  Denominator TGraph
     
     \return new TGraph as the ratio of the two TGraphs
     '''
    gr = ROOT.TGraph(num)
    for i in xrange(gr.GetN()):
        y = denom.GetY()[i]
        val = 0
        if y != 0:
            val = gr.GetY()[i]/y
        gr.SetPoint(i, gr.GetX()[i], val)
    return gr


def subtractGraph(minuend, subtrahend):
    '''
    Subtract two TGraphs
    
    \param minuend     Minuend TGraph
    \param subtrahend  Subtrahend TGraph
    
    \return new TGraph as the difference of the two TGraphs
    '''
    gr = ROOT.TGraph(minuend)
    for i in xrange(gr.GetN()):
        val = gr.GetY() - subtrahend.GetY()[i]
        gr.SetPoint(i, gr.GetX()[i], val)
    return gr


def getTypesetScenarioName(scenario):
    '''
    Returns a properly typeset label for MSSM scenario
    
    \param scenario   string of the scenario rootfile name
    
    \return string with the typeset name
    '''
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
    if myTruncatedScenario == "haber_type1":
        return "2HDM Type 1"
    if myTruncatedScenario == "haber_type2":
        return "2HDM Type 2"
    raise Exception("The typeset name for scenario '%s' is not defined in tools/limit.py::getTypesetScenarioName()! Please add it."%scenario)


def truncateBeyondIsomass(gIsomass, g, debugStatus=False):
    '''
    Remove graph points in the isomass region
    \param gIsomass   TGraph containing isomass curve
    \param g          TGraph to be checked for points in isomass region
    '''
    crossingData = []
    gCrossingIndices = []
    isomassCrossingIndices = []
    if debugStatus:
        for i in range(g.GetN()):
            print "Before treatment: %d, %f, %f"%(i, g.GetX()[i], g.GetY()[i])
    # Loop over isomass points
    for i in range(gIsomass.GetN()-1):
        isomassIndex = i
        # calculate k and b of y=kx+b
        isomassK = None
        isomassB = None
        isomassDirection = gIsomass.GetX()[isomassIndex+1]-gIsomass.GetX()[isomassIndex]
        if abs(isomassDirection) > 0.0001:
            isomassK = (gIsomass.GetY()[isomassIndex+1]-gIsomass.GetY()[isomassIndex]) / (isomassDirection)
            isomassB = gIsomass.GetY()[isomassIndex] - isomassK*gIsomass.GetX()[isomassIndex]
        # Loop over graph points
        for j in range(g.GetN()-1):
            gIndex = j
            crossingM = None
            gK = None
            gB = None
            gDirection = g.GetX()[gIndex+1]-g.GetX()[gIndex]
            if isomassK == None:
                crossingM = gIsomass.GetX()[isomassIndex]
            else:
                crossingM = g.GetX()[gIndex]
                if abs(gDirection) > 0.0001:
                    # calculate k and b of y=kx+b
                    gK = (g.GetY()[gIndex+1]-g.GetY()[gIndex]) / (gDirection)
                    gB = g.GetY()[gIndex] - gK*g.GetX()[gIndex]
                    # calculate m value for crossing of the two lines
                    if abs(isomassK-gK) > 0.0001:
                        crossingM = -(isomassB-gB) / (isomassK-gK)
                    else:
                        crossingM = -10.0
            crossingY = None
            if isomassK == None:
                crossingY = gIsomass.GetY()[isomassIndex]
            elif gK == None:
                crossingY = g.GetY()[gIndex]
            elif abs(isomassK+gK) < 0.00001:
                crossingY = -10.0
            else:
                crossingY = (isomassK*gB + gK*isomassB) / (isomassK+gK)
            # check if crossing occurs in this fragment
            gWithinRangeUpM = g.GetX()[gIndex+1] > crossingM and g.GetX()[gIndex] < crossingM or abs(g.GetX()[gIndex+1]-crossingM) < 0.001
            gWithinRangeDownM = (g.GetX()[gIndex+1] < crossingM and g.GetX()[gIndex] > crossingM) or abs(g.GetX()[gIndex]-crossingM) < 0.001
            gIsomassWithinRangeUpM = gIsomass.GetX()[isomassIndex+1] > crossingM and gIsomass.GetX()[isomassIndex] < crossingM
            gIsomassWithinRangeDownM = (gIsomass.GetX()[isomassIndex+1] < crossingM and gIsomass.GetX()[isomassIndex] > crossingM) or abs(gIsomass.GetX()[isomassIndex]-crossingM) < 0.001
            gWithinRangeUpY = g.GetY()[gIndex+1] > crossingY and g.GetY()[gIndex] < crossingY or abs(g.GetY()[gIndex+1]-crossingY) < 0.001
            gWithinRangeDownY = (g.GetY()[gIndex+1] < crossingY and g.GetY()[gIndex] > crossingY) or abs(g.GetY()[gIndex]-crossingY) < 0.001
            gIsomassWithinRangeUpY = gIsomass.GetY()[isomassIndex+1] > crossingY and gIsomass.GetY()[isomassIndex] < crossingY
            gIsomassWithinRangeDownY = (gIsomass.GetY()[isomassIndex+1] < crossingY and gIsomass.GetY()[isomassIndex] > crossingY) or abs(gIsomass.GetY()[isomassIndex]-crossingY) < 0.001
            #if debugStatus:
                #print "test at gIndex=%d, isomassIndex=%d, isomassTb=%f, m=%f tb=%f"%(gIndex, isomassIndex, gIsomass.GetY()[isomassIndex], crossingM, crossingY)
                #print "0: isomass %d (%f,%f), g %d (%f,%f)"%(isomassIndex, gIsomass.GetX()[isomassIndex], gIsomass.GetY()[isomassIndex], gIndex, g.GetX()[gIndex], g.GetY()[gIndex])
                #print "1: isomass %d (%f,%f), g %d (%f,%f)"%(isomassIndex+1, gIsomass.GetX()[isomassIndex+1], gIsomass.GetY()[isomassIndex+1], gIndex+1, g.GetX()[gIndex+1], g.GetY()[gIndex+1])
                #print gWithinRangeUpM,gWithinRangeDownM,gIsomassWithinRangeUpM,gIsomassWithinRangeDownM,abs(g.GetX()[gIndex]-crossingM) < 0.001
            if not ((gWithinRangeUpM or gWithinRangeDownM) and (gIsomassWithinRangeUpM or gIsomassWithinRangeDownM)) or crossingM < 100.01:
                continue
            #print "**1"
            if not ((gWithinRangeUpY or gWithinRangeDownY) and (gIsomassWithinRangeUpY or gIsomassWithinRangeDownY)):
                continue
            #print "**2"
            if gIsomass.GetX()[isomassIndex] < 100.01 or gIsomass.GetY()[isomassIndex] < 0.91 or gIsomass.GetY()[isomassIndex+1] < 0.91:
                continue
            #print "**3"
            if len(gCrossingIndices) > 0:
                if abs(crossingM - crossingData[len(crossingData)-1][1]) < 0.001 or abs(crossingY - crossingData[len(crossingData)-1][2]) < 0.001:
                    continue
            # Crossing found, tune crossing point value with linear extrapolation of m
            if debugStatus:
                print "** crossing at m=%f tb=%f, gIndex=%d"%(crossingM, crossingY, gIndex)
                print "0: isomass %d (%f,%f), g %d (%f,%f)"%(isomassIndex, gIsomass.GetX()[isomassIndex], gIsomass.GetY()[isomassIndex], gIndex, g.GetX()[gIndex], g.GetY()[gIndex])
                print "1: isomass %d (%f,%f), g %d (%f,%f)"%(isomassIndex+1, gIsomass.GetX()[isomassIndex+1], gIsomass.GetY()[isomassIndex+1], gIndex+1, g.GetX()[gIndex+1], g.GetY()[gIndex+1])
            if len(gCrossingIndices) == 2:
                raise Exception("This should not happen")
            index = gIndex
            if len(gCrossingIndices) == 0:
                index += 1
            crossingData.append([index, crossingM, crossingY])
            gCrossingIndices.append(index)
            isomassCrossingIndices.append(isomassIndex)
    if debugStatus:
        print crossingData
    # Construct temporary lists
    x = []
    y = []
    if len(isomassCrossingIndices) == 2:
        for i in range(isomassCrossingIndices[0], isomassCrossingIndices[1]+1):
            x.append(gIsomass.GetX()[i])
            y.append(gIsomass.GetY()[i])
        if gCrossingIndices[1] < gCrossingIndices[0]:
            x = list(reversed(x))[:]
            y = list(reversed(y))[:]
        if gCrossingIndices[1] < gCrossingIndices[0]:
            # Fix offsets
            crossingData[0][0] -= 1
            crossingData[1][0] += 1
            gCrossingIndices[0] -= 1
            gCrossingIndices[1] += 1
    # Modify graph at crossing
    for item in crossingData:
        g.SetPoint(item[0], item[1], item[2])
    # Remove points in the isomass region from graph
    if len(gCrossingIndices) == 2:
        for i in range(min(gCrossingIndices), max(gCrossingIndices)):
            g.RemovePoint(i)
            if debugStatus:
                print "*** removing",i
    if len(isomassCrossingIndices) == 2:
        for i in range(min(gCrossingIndices)+1, g.GetN()):
            x.append(g.GetX()[i])
            y.append(g.GetY()[i])
            if debugStatus:
                print i, g.GetX()[i], g.GetY()[i]        
    # Add isomass boundary points to graph
    if len(gCrossingIndices) == 2:
        for i in range(len(x)):
            g.SetPoint(i+min(gCrossingIndices), x[i], y[i])
    if debugStatus:
        for i in range(g.GetN()):
            print "After treatment: %d, %f, %f"%(i, g.GetX()[i], g.GetY()[i])
    return    
    
def doTanBetaPlotHeavy(name, graphs, luminosity, finalstateText, xlabel, scenario):
    '''
     Plots tan beta plot

     \param name    string of filename prefix for plot
     \param graphs  dictionary of TGraph objects
     \param luminosity luminosity for plot
     \param finalstateText label of final state
     \param xlabel  x-axis label
     \param scenario name of scenario
     '''
    doTanBetaPlotGeneric(name, graphs, luminosity, finalstateText, xlabel, scenario, regime="heavy")
    return


def doTanBetaPlotLight(name, graphs, luminosity, finalstateText, xlabel, scenario):
    '''
    Plots tan beta plot
    
    \param name    string of filename prefix for plot
    \param graphs  dictionary of TGraph objects
    \param luminosity luminosity for plot
    \param finalstateText label of final state
    \param xlabel  x-axis label
    \param scenario name of scenario
    '''
    doTanBetaPlotGeneric(name, graphs, luminosity, finalstateText, xlabel, scenario, regime="light")
    return


def doTanBetaPlotGeneric(name, graphs, luminosity, finalstateText, xlabel, scenario, regime):
    '''
    Plots tan beta plot
    
    \param name    string of filename prefix for plot
    \param graphs  dictionary of TGraph objects
    \param luminosity luminosity for plot
    \param finalstateText label of final state
    \param xlabel  x-axis label
    \param scenario name of scenario
    '''
    # Enable OpenGL for transparency
    #if opts.excludedArea:
    ROOT.gEnv.SetValue("OpenGL.CanvasPreferGL", 1)
    
#    isHeavy = regime != "light"
    tanbMax = 60

    if forPaper:
        if scenario in ["mhmaxup", "mhmodm"] and not "_mA" in name:
            histograms.cmsTextMode = histograms.CMSMode.PAPER
        else:
            histograms.cmsTextMode = histograms.CMSMode.UNPUBLISHED
    else:
        histograms.cmsTextMode = histograms.CMSMode.PRELIMINARY

    blinded = True
    if "obs" in graphs.keys():
        blinded = False

    higgs = "h"
    if scenario == "lowMH-LHCHXSWG":
        higgs = "H"

    # Create excluded area
    if not blinded:    
        obs = graphs["obs"]
        excluded = aux.Clone(ROOT.TGraph(obs))
        excluded.SetName("ExcludedArea")
        if regime == "heavy":
            excluded.SetPoint(excluded.GetN(),obs.GetX()[obs.GetN()-1],69.0)
            excluded.SetPoint(excluded.GetN(), -1.0, 69.0)
            excluded.SetPoint(excluded.GetN(), -1.0, obs.GetY()[0])
        elif regime == "light":
            excluded.SetPoint(excluded.GetN(), -1.0, obs.GetY()[excluded.GetN()-1])
            excluded.SetPoint(excluded.GetN(), -1.0, 69.0)
            excluded.SetPoint(excluded.GetN(), 1000.0, 69.0)
            excluded.SetPoint(excluded.GetN(), 1000.0, obs.GetY()[0])
            excluded.SetPoint(excluded.GetN(), obs.GetX()[0], obs.GetY()[0])
        else:
            excluded.SetPoint(excluded.GetN(), -1.0, obs.GetY()[excluded.GetN()-1])
            excluded.SetPoint(excluded.GetN(), -1.0, 69.0)
            excluded.SetPoint(excluded.GetN(), 1000.0, 69.0)
            excluded.SetPoint(excluded.GetN(), 1000.0, obs.GetY()[0])
            excluded.SetPoint(excluded.GetN(), obs.GetX()[0], obs.GetY()[0])

        setExcludedStyle(excluded)
        graphs["excluded"] = excluded
        if "isomass" in graphs.keys() and "_mA" in name:
            truncateBeyondIsomass(graphs["isomass"], excluded)
        if "obsDown" in graphs.keys():
            excludedDown = aux.Clone(graphs["obsDown"])
            if regime == "heavy":
                excludedDown.SetPoint(excludedDown.GetN(),1000.0, 0.999)
                excludedDown.SetPoint(excludedDown.GetN(),-1.0,0.999)
                excludedDown.SetPoint(excludedDown.GetN(),excludedDown.GetX()[0],excludedDown.GetY()[0])
            elif regime == "light":
                excludedDown.SetPoint(excludedDown.GetN(),-1.0, excludedDown.GetY()[excludedDown.GetN()-1])
                excludedDown.SetPoint(excludedDown.GetN(),-1.0,0.999)
                excludedDown.SetPoint(excludedDown.GetN(),180,0.999)
                excludedDown.SetPoint(excludedDown.GetN(),180,excludedDown.GetY()[0])
                excludedDown.SetPoint(excludedDown.GetN(),excludedDown.GetX()[0],excludedDown.GetY()[0])
            else:
                excludedDown.SetPoint(excludedDown.GetN(),1000.0, 0.999)
                excludedDown.SetPoint(excludedDown.GetN(),-1.0,0.999)
                excludedDown.SetPoint(excludedDown.GetN(),excludedDown.GetX()[0],excludedDown.GetY()[0])

            setExcludedStyle(excludedDown)
            graphs["excludedDown"] = excludedDown
        if "isomass" in graphs.keys() and "_mA" in name:
            truncateBeyondIsomass(graphs["isomass"], excludedDown)

    # Set styles
    if "exp" in graphs.keys():
        expected = graphs["exp"]
        setExpectedStyle(expected)
    if "expDown" in graphs.keys():
        setExpectedStyle(graphs["expDown"])
        setExpectedGreenBandStyle(graphs["exp1Down"])
        setExpectedYellowBandStyle(graphs["exp2Down"])
    if "exp1" in graphs.keys():
        expected1 = graphs["exp1"]
        setExpectedGreenBandStyle(expected1)
    if "exp2" in graphs.keys():
        expected2 = graphs["exp2"]
        setExpectedYellowBandStyle(expected2)

    if "Allowed" in graphs.keys():
        allowed = graphs["Allowed"]
        allowed.SetFillStyle(3005)
        allowed.SetFillColor(ROOT.kRed)
        allowed.SetLineWidth(-302)
        allowed.SetLineColor(ROOT.kRed)
        allowed.SetLineStyle(1)

    myLegendDictionary = {
            "Expected": None,
            "Expected1": "Expected median #pm 1#sigma",
            "Expected2": "Expected median #pm 2#sigma",
    }
    
    plotsList = []
    # Iso mass
    if "isomass" in graphs.keys() and not graphs["isomass"] == None:
        graphs["isomass"].SetFillColor(0)
        graphs["isomass"].SetFillStyle(1)
        graphs["isomass"].SetLineStyle(2)
        plotsList.extend([histograms.HistoGraph(graphs["isomass"], "IsoMass", drawStyle="L", legendStyle=None)])

    # Observed and excluded
    if not blinded:
        if "obs_th_plus" in graphs.keys():
            setTheoreticalErrorStyle(graphs["obs_th_plus"])
            setTheoreticalErrorStyle(graphs["obs_th_minus"])
        setObservedStyle(graphs["obs"])
        if "obsDown" in graphs.keys():
            setObservedStyle(graphs["obsDown"])
        plotsList.append(histograms.HistoGraph(graphs["obs"], "Observed", drawStyle="PL", legendStyle="lp"))
        if "obsDown" in graphs.keys():
            plotsList.append(histograms.HistoGraph(graphs["obsDown"], "ObservedDown", drawStyle="PL", legendStyle=None))
        plotsList.append(histograms.HistoGraph(excluded, "Excluded", drawStyle="F", legendStyle="f"))
        if "obsDown" in graphs.keys():
            plotsList.append(histograms.HistoGraph(graphs["excludedDown"], "ExcludedDown", drawStyle="F", legendStyle=None))
        if "obs_th_plus" in graphs.keys():
            plotsList.extend([histograms.HistoGraph(graphs["obs_th_plus"], "ObservedPlus", drawStyle="L", legendStyle="l"),
                              histograms.HistoGraph(graphs["obs_th_minus"], "ObservedMinus", drawStyle="L")])

    # Allowed bands
    if "AllowedCentral" in graphs.keys():
        graphs["AllowedCentral"].SetLineColor(ROOT.kRed)
        graphs["AllowedCentral"].SetLineWidth(1)
        plotsList.extend([histograms.HistoGraph(graphs["AllowedCentral"], "AllowedCentral", drawStyle="L")])
        myLegendDictionary["AllowedCentral"] = "m_{"+higgs+"}^{MSSM} = 125 GeV"
    if "Allowed" in graphs.keys():
        myLegendDictionary["Allowed"] = "m_{"+higgs+"}^{MSSM} #neq 125#pm3 GeV"
        plotsList.extend([histograms.HistoGraph(graphs["Allowed"], "Allowed", drawStyle="L", legendStyle="lf")])
    
    # Expected and expected bands
    if "isomass" in graphs.keys():
        truncateBeyondIsomass(graphs["isomass"], expected1)
        truncateBeyondIsomass(graphs["isomass"], expected2)

    if "exp" in graphs.keys():
        plotsList.append(histograms.HistoGraph(graphs["exp"], "Expected", drawStyle="L", legendStyle=None))
    if "expDown" in graphs.keys():
        plotsList.append(histograms.HistoGraph(graphs["expDown"], "Expected", drawStyle="L", legendStyle=None))
    if "exp1" in graphs.keys():
        plotsList.append(histograms.HistoGraph(graphs["exp1"], "Expected1", drawStyle="F", legendStyle="fl"))
    if "exp1Down" in graphs.keys():
        if "isomass" in graphs.keys():
            truncateBeyondIsomass(graphs["isomass"], graphs["exp1Down"])
        plotsList.append(histograms.HistoGraph(graphs["exp1Down"], "Expected median #pm 1#sigma", drawStyle="F", legendStyle=None))
    if "exp2" in graphs.keys():
        plotsList.append(histograms.HistoGraph(graphs["exp2"], "Expected2", drawStyle="F", legendStyle="fl"))
    if "exp2Down" in graphs.keys():
        if "isomass" in graphs.keys():
            truncateBeyondIsomass(graphs["isomass"], graphs["exp2Down"])
        plotsList.append(histograms.HistoGraph(graphs["exp2Down"], "Expected median #pm2 #sigma", drawStyle="F", legendStyle=None))
        
    plot = plots.PlotBase(plotsList, saveFormats=[".png", ".pdf", ".C"])

    plot.histoMgr.setHistoLegendLabelMany(myLegendDictionary)

    # Move the m_h,H allowed region to the last in the legend
    histoNames = [h.getName() for h in plot.histoMgr.getHistos()]
    plot.histoMgr.reorderLegend(filter(lambda n: "Allowed" not in n, histoNames))

    captionLineSpacing = 0.042
    captionLines = 3
    if isinstance(finalstateText, list):
        captionLines += len(finalstateText) - 1

    if regime == "heavy":
        x = 0.52
        y = -0.25#-0.11
        #if scenario.replace("-LHCHXSWG", "") in ["lightstop", "mhmaxup"]:
        #    y += 0.05
    elif regime == "light":
        x = 0.2
        y = -0.05
    else:
        x = 0.52
        y = -0.25
    plot.setLegend(histograms.createLegend(x-0.01, y+0.6-(captionLines-0.2)*captionLineSpacing, x+0.45, y+0.9-(captionLines-0.2)*captionLineSpacing))
    plot.legend.SetMargin(0.17)

    #plot.legend.SetFillColor(0)
    #plot.legend.SetFillStyle(1001)
    if blinded:
        name += "_blinded"
    name = os.path.basename(name)
    name = name.replace("-","_")
    
    if regime == "heavy":
        frameXmin = 180
        frameXmax = 500
        if "_mA" in name:
            frameXmin = 140
        plot.createFrame(name, opts={"ymin": 1, "ymax": tanbMax, "xmin": frameXmin, "xmax": frameXmax})
    elif regime == "light":
        frameXmax = 160
        frameXmin = 90
        if "_mA" in name:
            frameXmax = 145
            frameXmin = 50
        plot.createFrame(name, opts={"ymin": 1, "ymax": tanbMax, "xmin": frameXmin, "xmax": frameXmax})
    else:
        frameXmax = 600
        frameXmin = 90
        if "_mA" in name:
            frameXmax = 145
            frameXmin = 50
        plot.createFrame(name, opts={"ymin": 1, "ymax": tanbMax, "xmin": frameXmin, "xmax": frameXmax})

    plot.frame.GetXaxis().SetTitle(xlabel)
    plot.frame.GetYaxis().SetTitle(tanblimit)

####    plot.getPad().SetLogy(True)

    plot.draw()
    
    plot.setLuminosity(luminosity)
    if regime == "heavy":
        plot.addStandardTexts(cmsTextPosition="right")
    elif regime == "light":
        plot.addStandardTexts(cmsTextPosition="left")
    else:
        plot.addStandardTexts(cmsTextPosition="right")
#    histograms.addLuminosityText(x=None, y=None, lumi="2.3-4.9")

    size = 20
    if regime == "light":
        histograms.addText(x, y+0.9, process, size=size)
    elif regime == "heavy":
        histograms.addText(x+0.01, y+0.84, processHeavy, size=size)
    elif regime == "combined":
        histograms.addText(x, y, processCombination, size=size)
    else:
        raise Exception("Unknown option for regime")
    y -= captionLineSpacing
    print "check finalstateText",finalstateText,x,y
    if isinstance(finalstateText, str):
        histograms.addText(x+0.01, y+0.84, finalstateText, size=size)
        y -= captionLineSpacing
    elif isinstance(finalstateText, list):
        for l in finalstateText:
            histograms.addText(x, y+0.9, l, size=size)
            y -= captionLineSpacing
    else:
        raise Exception("not implemented")
    histograms.addText(x-0.21, y+0.695, "^{}%s"%getTypesetScenarioName(scenario), size=size)
#    histograms.addText(x-0.3, y+0.695, "^{}%s"%getTypesetScenarioName(scenario), size=size)
#    histograms.addText(x-0.33, y+0.695, "^{}%s"%getTypesetScenarioName(scenario), size=size) # mhmaxup
#    histograms.addText(x, y+0.93, "^{}%s"%getTypesetScenarioName(scenario), size=size)
#    histograms.addText(0.2, 0.231, "Min "+limit.BR+"(t#rightarrowH^{+}b)#times"+limit.BR+"(%s)" % (decayMode), size=0.5*size)

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
