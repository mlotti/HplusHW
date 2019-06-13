import HiggsAnalysis.NtupleAnalysis.tools.ShellStyles as ShellStyles
import HiggsAnalysis.NtupleAnalysis.tools.splittedHistoReader as splittedHistoReader
import HiggsAnalysis.NtupleAnalysis.tools.ShapeHistoModifier as ShapeHistoModifier
from math import sqrt
from HiggsAnalysis.NtupleAnalysis.tools.dataset import Count
import HiggsAnalysis.NtupleAnalysis.tools.histogramsExtras as histogramsExtras
import HiggsAnalysis.NtupleAnalysis.tools.errorPropagation as errorPropagation
from HiggsAnalysis.NtupleAnalysis.tools.extendedCount import ExtendedCount
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux
import array
import os

import ROOT
ROOT.gROOT.SetBatch(True) # no flashing canvases

## Container class for information of data and MC EWK at certain point of selection
class DataDrivenQCDShape:
    def __init__(self, 
                 dsetMgr, 
                 dsetLabelData,
                 dsetLabelEwk,
                 histoName,
                 dataPath,
                 ewkPath,
                 luminosity):
                 #dataDrivenFakeTaus=False,
                 #EWKUncertaintyFactor=1.0,
                 #UncertAffectsTT = True):
        self._uniqueN = 0
        self._splittedHistoReader = splittedHistoReader.SplittedHistoReader(dsetMgr, dsetLabelData)
        self._histoName = histoName
        dataFullName = os.path.join(dataPath, histoName)
        self._dataList = list(self._splittedHistoReader.getSplittedBinHistograms(dsetMgr, dsetLabelData, dataFullName, luminosity))
        ewkFullName = os.path.join(ewkPath, histoName)
        self._ewkList = list(self._splittedHistoReader.getSplittedBinHistograms(dsetMgr, dsetLabelEwk, ewkFullName, luminosity))

    ## Delete the histograms
    def delete(self):
        for h in self._dataList:
            if h == None:
                raise Exception("asdf")
            h.Delete()
        for h in self._ewkList:
            if h == None:
                raise Exception()
            h.Delete()
        self._dataList = []
        self._ewkList = []

    def getFileFriendlyHistoName(self):
        return self._histoName.replace("/","_")

    def getHistoName(self):
        return self._histoName

    ## Return the sum of data-ewk in a given phase space split bin
    def getDataDrivenQCDHistoForSplittedBin(self, binIndex):
        if binIndex >= len(self._dataList):
            raise Exception(ShellStyles.ErrorLabel()+"DataDrivenQCDShape::getDataDrivenQCDForSplittedBin: requested bin index %d out of range (0-%d)!"%(binIndex,len(self._dataList)))
        h = aux.Clone(self._dataList[binIndex])
        h.SetName(h.GetName()+"dataDriven")
#        h.Add(self._ewkList[binIndex], -1.0)
        return h

    ## Return the data in a given phase space split bin
    def getDataHistoForSplittedBin(self, binIndex):
        if binIndex >= len(self._dataList):
            raise Exception(ShellStyles.ErrorLabel()+"DataDrivenQCDShape::getDataHistoForSplittedBin: requested bin index %d out of range (0-%d)!"%(binIndex,len(self._dataList)))
        h = aux.Clone(self._dataList[binIndex])
        h.SetName(h.GetName()+"_")
        return h

    ## Return the EWK MC in a given phase space split bin
    def getEwkHistoForSplittedBin(self, binIndex):
        if binIndex >= len(self._dataList):
            raise Exception(ShellStyles.ErrorLabel()+"DataDrivenQCDShape::getEwkHistoForSplittedBin: requested bin index %d out of range (0-%d)!"%(binIndex,len(self._ewkList)))
        h = aux.Clone(self._ewkList[binIndex])
        h.SetName(h.GetName()+"_")
        return h

    ## Return the sum of data-ewk integrated over the phase space splitted bins
    def getIntegratedDataDrivenQCDHisto(self):
        h = aux.Clone(self._dataList[0])
        h.SetName(h.GetName()+"Integrated")
        h.Add(self._ewkList[0],-1.0)
        for i in range(1, len(self._dataList)):
            h.Add(self._dataList[i])
#            h.Add(self._ewkList[i],-1.0)
        return h

    ## Return the sum of data integrated over the phase space splitted bins
    def getIntegratedDataHisto(self):
        h = aux.Clone(self._dataList[0])
        h.SetName(h.GetName()+"Integrated")
        for i in range(1, len(self._dataList)):
            h.Add(self._dataList[i])
        return h

    ## Return the sum of ewk integrated over the phase space splitted bins
    def getIntegratedEwkHisto(self):
        h = aux.Clone(self._ewkList[0])
        h.SetName(h.GetName()+"Integrated")
        for i in range(1, len(self._dataList)):
            h.Add(self._ewkList[i])
        return h

    ## Return the QCD purity as a histogram with splitted bins on x-axis
    def getPurityHisto(self):
        # Create histogram
        myNameList = self._ewkList[0].GetName().split("_")
        h = ROOT.TH1F("%s_purity_%d"%(self._ewkList[0].GetName(), self._uniqueN), "PurityBySplittedBin_%s"%myNameList[0][:len(myNameList[0])-1], len(self._ewkList),0,len(self._ewkList))
        h.Sumw2()
        h.SetYTitle("Purity, %")
        ROOT.SetOwnership(h, True)
        self._uniqueN += 1
        for i in range(0, len(self._dataList)):
            h.GetXaxis().SetBinLabel(i+1, self._dataList[i].GetTitle())
            nData = 0.0
            nEwk = 0.0
            for j in range(0, self._dataList[i].GetNbinsX()+2):
                nData += self._dataList[i].GetBinContent(j)
                nEwk += self._ewkList[i].GetBinContent(j)
            myPurity = 0.0
            myUncert = 0.0
            if (nData > 0.0):
                myPurity = (nData - nEwk) / nData
                myUncert = sqrt(myPurity * (1.0-myPurity) / nData) # Assume binomial error
            h.SetBinContent(i+1, myPurity * 100.0)
            h.SetBinError(i+1, myUncert * 100.0)
        return h

    ## Return the QCD purity as a Count object
    def getIntegratedPurity(self):
        nData = 0.0
        nEwk = 0.0
        for i in range(0, len(self._dataList)):
            for j in range(0, self._dataList[i].GetNbinsX()+2):
                nData += self._dataList[i].GetBinContent(j)
                nEwk += self._ewkList[i].GetBinContent(j)
        myPurity = 0.0
        myUncert = 0.0
        if (nData > 0.0):
            myPurity = (nData - nEwk) / nData
            myUncert = sqrt(myPurity * (1.0-myPurity) / nData) # Assume binomial error
        return Count(myPurity, myUncert)

    ## Return the minimum QCD purity as a Count object
    def getMinimumPurity(self):
        myMinPurity = 0.0
        myMinPurityUncert = 0.0
        for i in range(0, len(self._dataList)):
            for j in range(0, self._dataList[i].GetNbinsX()+2):
                nData += self._dataList[i].GetBinContent(j)
                nEwk += self._ewkList[i].GetBinContent(j)
        myPurity = 0.0
        myUncert = 0.0
        if (nData > 0.0):
            myPurity = (nData - nEwk) / nData
            myUncert = sqrt(myPurity * (1.0-myPurity) / nData) # Assume binomial error
            if myPurity < myMinPurity:
                myMinPurity = myPurity
                myMinPurityUncert = myUncert
        return Count(myMinPurity, myMinPurityUncert)

    ## Return the QCD purity in bins of the final shape
    def getIntegratedPurityForShapeHisto(self):
        hData = self.getIntegratedDataHisto()
        hEwk = self.getIntegratedEwkHisto()
        h = aux.Clone(hData, "%s_purity_%d"%(hData,self._uniqueN))
        myNameList = self._dataList[0].GetName().split("_")
        h.SetTitle("PurityByFinalShapeBin_%s"%myNameList[0][:len(myNameList[0])-1])
        self._uniqueN += 1
        for i in range(1, h.GetNbinsX()+1):
            myPurity = 0.0
            myUncert = 0.0
            if (hData.GetBinContent(i) > 0.0):
                myPurity = (hData.GetBinContent(i) - hEwk.GetBinContent(i)) / hData.GetBinContent(i)
                if myPurity < 0.0:
                    myPurity = 0.0
                    myUncert = 0.0
                else:
                    myUncert = sqrt(myPurity * (1.0-myPurity) / hData.GetBinContent(i)) # Assume binomial error
            h.SetBinContent(i, myPurity)
            h.SetBinError(i, myUncert)
        return h

    ## Returns the labels of the phase space splitting axes
    def getPhaseSpaceSplittingAxisLabels(self):
        return self._splittedHistoReader.getBinLabels()

    ## Returns phase space split title for a bin
    def getPhaseSpaceBinTitle(self, binIndex):
        if binIndex >= len(self._dataList):
            raise Exception(ShellStyles.ErrorLabel()+"DataDrivenQCDShape::getPhaseSpaceBinTitle: requested bin index %d out of range (0-%d)!"%(binIndex,len(self._dataList)))
        return self._dataList[binIndex].GetTitle()

    ## Returns phase space split title for a bin
    def getPhaseSpaceBinFileFriendlyTitle(self, binIndex):
        if binIndex >= len(self._dataList):
            raise Exception(ShellStyles.ErrorLabel()+"DataDrivenQCDShape::getPhaseSpaceBinTitle: requested bin index %d out of range (0-%d)!"%(binIndex,len(self._dataList)))
        return self._dataList[binIndex].GetTitle().replace(">","gt").replace("<","lt").replace("=","eq").replace("{","").replace("}","").replace(" ","").replace("#","").replace("..","to").replace("(","").replace(")","").replace(",","").replace("/","_").replace(".","p")

    ## Returns number of phase space bins
    def getNumberOfPhaseSpaceSplitBins(self):
        return self._splittedHistoReader.getMaxBinNumber()

    ## Returns name of histogram combined with the split bin title
    def getOutputHistoName(self, suffix=""):
        s = "%s"%(self._dataList[0].GetName().replace("/","_"))
        if len(suffix) > 0:
            s += "_%s"%suffix
        return s

## Efficiency from two shape objects
class DataDrivenQCDEfficiency:
    ## numerator and denominator are DataDrivenQCDShape objects
    def __init__(self, numerator, denominator):
        self._efficiencies = [] # List of ExtendedCount objects, one for each phase space split bin

        self._calculate(numerator, denominator)

    def delete(self):
        for e in self._efficiencies:
            del e
        self._efficiencies = None

    def getEfficiencyForSplitBin(self, binIndex):
        return self._efficiencies[binIndex]

    def _calculate(self, numerator, denominator):
        self._efficiencies = []
        myUncertaintyLabels = ["statData", "statEWK"]
        nSplitBins = numerator.getNumberOfPhaseSpaceSplitBins()
        for i in range(0, nSplitBins):
            hNum = numerator.getDataDrivenQCDHistoForSplittedBin(i)
            hNum.SetName("hNum")
            hNumData = numerator.getDataHistoForSplittedBin(i)
            hNumData.SetName("hNumData")
            hNumEwk = numerator.getEwkHistoForSplittedBin(i)
            hNumEwk.SetName("hNumEwk")
            hDenom = denominator.getDataDrivenQCDHistoForSplittedBin(i)
            hDenom.SetName("hDenom")
            hDenomData = denominator.getDataHistoForSplittedBin(i)
            hDenomData.SetName("hDenomData")
            hDenomEwk = denominator.getEwkHistoForSplittedBin(i)
            hDenomEwk.SetName("hDenomEwk")
            # Sum over basic shape and leg2 shape to obtain normalisation factor
            mySumNum = hNum.Integral(1, hNum.GetNbinsX()+2)
            mySumNumDataUncert = integratedUncertaintyForHistogram(1, hNumData.GetNbinsX()+2, hNumData)
            mySumNumEwkUncert = integratedUncertaintyForHistogram(1, hNumEwk.GetNbinsX()+2, hNumEwk)
            mySumDenom = hDenom.Integral(1, hDenom.GetNbinsX()+2)
            mySumDenomDataUncert = integratedUncertaintyForHistogram(1, hDenomData.GetNbinsX()+2, hDenomData)
            mySumDenomEwkUncert = integratedUncertaintyForHistogram(1, hDenomEwk.GetNbinsX()+2, hDenomEwk)
            # Calculate efficiency
            myEfficiency = 0.0
            myEfficiencyUncertData = errorPropagation.errorPropagationForDivision(mySumNum, mySumNumDataUncert, mySumDenom, mySumDenomDataUncert)
            myEfficiencyUncertEwk = errorPropagation.errorPropagationForDivision(mySumNum, mySumNumEwkUncert, mySumDenom, mySumDenomEwkUncert)
            if abs(mySumNum) > 0.000001 and abs(mySumDenom) > 0.000001:
                myEfficiency = mySumNum / mySumDenom
            self._efficiencies.append(ExtendedCount(myEfficiency, [myEfficiencyUncertData, myEfficiencyUncertEwk], myUncertaintyLabels))
            ROOT.gDirectory.Delete("hNum")
            ROOT.gDirectory.Delete("hNumData")
            ROOT.gDirectory.Delete("hNumEwk")
            ROOT.gDirectory.Delete("hDenom")
            ROOT.gDirectory.Delete("hDenomData")
            ROOT.gDirectory.Delete("hDenomEwk")
        #FIXME: add histogram for efficiency

