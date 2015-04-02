# Description: 
# Module for calculating final Fake tau fake rates (doing the wighting of QCD and EWK+tt fake tau fake rates)
# Authors: EP

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShellStyles as ShellStyles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.extendedCount as extendedCount
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.errorPropagation as errorPropagation
import HiggsAnalysis.HeavyChHiggsToTauNu.qcdCommon.systematicsForMetShapeDifference as systematicsForMetShapeDifference
import HiggsAnalysis.HeavyChHiggsToTauNu.qcdCommon.dataDrivenQCDCount as dataDrivenQCDCount
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.aux as aux
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.systematics as systematics
import math
import ROOT
import re

class FakeRateCalculator:
    def __init__(self, dsetMgr, shapeString, myNormfactors, luminosity, EWKUncertaintyFactor=1.0, UncertAffectsTT = True, dataDrivenFakeTaus = True):
        self.sortedFactors = {}
        self.sortedFactors = self.sortFactors(myNormfactors)
        # get shapes
        self.qcdShape = dataDrivenQCDCount.DataDrivenQCDShape(dsetMgr, "Data", "EWK", shapeString, luminosity, EWKUncertaintyFactor=EWKUncertaintyFactor, dataDrivenFakeTaus=False,  UncertAffectsTT = UncertAffectsTT)
        self.faketauShape = dataDrivenQCDCount.DataDrivenQCDShape(dsetMgr, "Data", "EWK", shapeString, luminosity, EWKUncertaintyFactor=EWKUncertaintyFactor, dataDrivenFakeTaus=True, UncertAffectsTT = UncertAffectsTT)
        
        self.weights = []
        self.weightErrors = []
        self.weightsSystVarUp = []
        self.weightsSystVarDown =[]

        self.fakerates = {}
        self.fakeratesSystVarUp = {}
        self.fakeratesSystVarDown = {}
        self.sortedfakerates = {}

        self.dataDrivenFakeTaus = dataDrivenFakeTaus

        self.averageWeight = 0

        self.doCalculate()

    def doCalculate(self):
        nSplitBins = self.qcdShape.getNumberOfPhaseSpaceSplitBins()
        averageNum = 0
        averageDenom = 0
        for i in range(0, nSplitBins):
            nData = self.qcdShape.getDataHistoForSplittedBin(i).Integral()
            nEWKincl = self.qcdShape.getEwkHistoForSplittedBin(i).Integral()
            nEWKgenuine = self.faketauShape.getEwkHistoForSplittedBin(i).Integral() 
            nQCD = nData - nEWKincl
            nFakeTau = nData - nEWKgenuine
            # calculate fake rate weights
            if self.dataDrivenFakeTaus:
                w = nQCD/nFakeTau
            else:
                w = 1.0
            # error of weighting is binomial
            wError = math.sqrt(nQCD*(1-w))/nFakeTau
            #print "Bin", i, "w = ", w
            self.weights.append(w)
            self.weightErrors.append(wError)
            self.weightsSystVarUp.append(w + wError)
            self.weightsSystVarDown.append(w - wError)
            
            averageNum += w*nFakeTau
            averageDenom += nFakeTau

            self.setFakeRateProbabilities(i)
        self.averageWeight = averageNum/averageDenom

    def setFakeRateProbabilities(self, i):
        # store final fake rates
        wQCD = self.sortedFactors[str(i)+"QCD"]
        wEWK = self.sortedFactors[str(i)+"EWK_FakeTaus"]
        
        fakeRate = self.weights[i]*wQCD + (1-self.weights[i])*wEWK
        fakeRateSystVarUp = self.weightsSystVarUp[i]*wQCD + (1-self.weightsSystVarUp[i])*wEWK
        fakeRateSystVarDown = self.weightsSystVarDown[i]*wQCD + (1-self.weightsSystVarDown[i])*wEWK

        self.fakerates[self.faketauShape.getPhaseSpaceBinFileFriendlyTitle(i)] = fakeRate
        self.fakeratesSystVarUp[self.faketauShape.getPhaseSpaceBinFileFriendlyTitle(i)] = fakeRateSystVarUp
        self.fakeratesSystVarDown[self.faketauShape.getPhaseSpaceBinFileFriendlyTitle(i)] = fakeRateSystVarDown

    def sortFactors(self, normdict):
        # sort fake rates to ascending order
        eq_re = re.compile("taup_Teq(?P<value1>\d+)to(?P<value2>\d+)(?P<name>\D+)") 
        lt_re = re.compile("taup_Tlt(?P<value1>\d+)(?P<name>\D+)")
        gt_re = re.compile("taup_Tgt(?P<value1>\d+)(?P<name>\D+)")

        namemap = {}
        binmap = {}
        labels = {}
        value = 0
        for bin in normdict.keys():
            match = eq_re.search(bin)
            if match:
                name = str(match.group("name"))
                value = int(match.group("value1"))
                binmap[bin] = value
                namemap[bin] = name
                labels[value] = bin.replace(name,"")
                continue
            match = lt_re.search(bin)
            if match:
                name = str(match.group("name"))
                value = int(match.group("value1")) - 1
                binmap[bin] = value
                namemap[bin] = name
                labels[value] = bin.replace(name,"")
                continue
            match = gt_re.search(bin)
            if match:
                name = str(match.group("name"))
                value = int(match.group("value1")) + 1
                binmap[bin] = value
                namemap[bin] = name
                labels[value] = bin.replace(name,"")
                continue

        i = 0
        sortdict = {}
        binvalues = sorted(list(set(binmap.values())))

        sortedlabels = []
        for binnum in binvalues:
            sortdict[binnum] = str(i)
            sortedlabels.append(labels[binnum])
            i += 1
        sortedlabels.append("Inclusive")

        retdict = {}
        inc_re = re.compile("Inclusive*")
        for bin in normdict.keys():
            match = inc_re.search(bin)
            if not match:
                retdict[sortdict[binmap[bin]]+namemap[bin]] = normdict[bin]
            else:
                retdict[bin] = normdict[bin]
        return retdict

    def getSortedFactors(self):
        return self.sortedFactors

    def getTotalFakeRateProbabilities(self):
        return self.fakerates

    def getTotalFakeRateProbabilitiesSystVarUp(self):
        return self.fakeratesSystVarUp

    def getTotalFakeRateProbabilitiesSystVarDown(self):
        return self.fakeratesSystVarDown

    def getSortedTotalFakeRateProbabilities(self):
        sortedfakerates = {}
        for k in self.fakerates.keys():
            sortedfakerates[k+"FakeTau"] = self.fakerates[k]
        sortedfakerates = self.sortFactors(sortedfakerates)
        return sortedfakerates

    def getWeight(self, i):
        return self.weights[i]

    def getWeights(self):
        return self.weights

    def getWeightErrors(self):
        return self.weightErrors

    def printWeights(self):
        print self.weights

    def getWeighSystVarUpt(self, i):
        return self.weightsSystVarUp[i]

    def getWeightSystVarDown(self, i):
        return self.weightsSystVarDown[i]

    def getAverageWeight(self):
        return self.averageWeight

    def getQCDShape(self):
        return self.qcdShape

    def getFakeTauShape(self):
        return self.faketauShape

    def getShape(self):
        if self.dataDrivenFakeTaus:
            return self.faketauShape
        else:
            return self.qcdShape

def scaleErrors(histo, weight):
    for i in range(0, histo.GetSize()+1):
        histo.SetBinError(i+1, weight*histo.GetBinError(i+1))
