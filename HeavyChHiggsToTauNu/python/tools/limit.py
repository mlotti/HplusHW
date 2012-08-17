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

## Flag for stating if the plots are for paper (True) or not (False)
forPaper = False
#forPaper = True

## Unit for mass (GeV vs. GeV/c^2
def massUnit():
    if forPaper:
        return "GeV"
    return "GeV/c^{2}"

## Label for branching fraction
BR = "#it{B}"

## The label for the physics process
process = "t #rightarrow H^{+}b, H^{+} #rightarrow #tau#nu"

## Label for the H+->tau BR assumption
BRassumption = "%s(H^{+} #rightarrow #tau#nu) = 1"%BR

## Y axis label for the BR
BRlimit = "95%% CL limit for %s(t#rightarrow H^{+}b)"%BR

## Y axis label for the tanbeta
tanblimit = "tan #beta"

## Label for m(H+)
def mHplus():
    return "m_{H^{+}} (%s)" % massUnit()

## Label for m(A)
def mA():
    return "m_{A} (%s)" % massUnit()


## Labels for the final states
_finalstateLabels = {
    "taujets": "#tau_{h}+jets",
    "etau"   : "e#tau_{h}",
    "mutau"  : "#mu#tau_{h}",
    "emu"    : "e#mu",
}

## Default y axis maximum values for BR limit for the final states
_finalstateYmaxBR = {
    "etau": 0.4,
    "mutau": 0.4,
    "emu": 0.8,
    "default": 0.15,
}


## Class for reading the BR limits from the JSON file produced by
## landsMergeHistograms.py
class BRLimits:
    ## Constructor
    #
    # \param directory          Path to the multicrab task directory with the JSON files
    # \param excludeMassPoints  List of strings for mass points to exclude
    def __init__(self, directory=".", excludeMassPoints=[]):
        resultfile="limits.json"
        configfile="configuration.json"

        f = open(os.path.join(directory, resultfile), "r")
        limits = json.load(f)
        f.close()

        self.lumi = float(limits["luminosity"])

        self.mass = limits["masspoints"].keys()
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
        if len(self.finalstates) == 1:
            return "%s final state" % _finalstateLabels[self.finalstates[0]]

        ret = ", ".join([_finalstateLabels[x] for x in self.finalstates[:-1]])
        ret += ", and %s final states" % _finalstateLabels[self.finalstates[-1]]
        return ret

    ## Get the maximum value for Y axis for the BR limit
    def getFinalstateYmaxBR(self):
        if len(self.finalstates) == 1:
            try:
                ymax = _finalstateYmaxBR[self.finalstates[0]]
            except KeyError:
                ymax = _finalstateYmaxBR["default"]
        else:
            ymax = _finalstateYmaxBR["default"]
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
        gr.SetMarkerStyle(21)
        gr.SetMarkerSize(1.5)
        gr.SetMarkerColor(ROOT.kBlack)
        gr.SetLineWidth(3)
        gr.SetLineColor(ROOT.kBlack)
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

        gr.SetLineStyle(2)
        gr.SetLineWidth(3)
        gr.SetLineColor(ROOT.kBlack)
        gr.SetMarkerStyle(20)

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

            gr.SetFillColor(ROOT.kGreen-3)
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

            gr.SetFillColor(ROOT.kYellow)
            gr.SetName("Expected2Sigma")
        else:
            raise Exception("Invalid value of sigma '%d', valid values are 0,1,2" % sigma)

        gr.SetLineStyle(2)
        gr.SetLineWidth(3)
        gr.SetLineColor(ROOT.kBlack)
        gr.SetMarkerStyle(20)

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
def getObservedMinus(graph):
    curve = graph.Clone()
    curve.SetName(curve.GetName()+"TheoryMinus")
    for i in xrange(0, graph.GetN()):
        curve.SetPoint(i,
                       graph.GetX()[i],
                       graph.GetY()[i]*0.77)
    print "todo: CHECK minus coefficient f(m)"
    return curve

## Construct observed + 1sigma theory uncertainty band
#
# \param graph   TGraph of the observed BR limit
#
# \return Clone of the TGraph for the +1sigma theory uncertainty band
def getObservedPlus(graph):
    curve = graph.Clone()
    curve.SetName(curve.GetName()+"TheoryPlus")
    for i in xrange(0, graph.GetN()):
        curve.SetPoint(i,
                       graph.GetX()[i],
                       graph.GetY()[i]*1.22)
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
