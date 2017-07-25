#================================================================================================
# Imports
#================================================================================================
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

#================================================================================================
# TEMPORARY Function Definition
#================================================================================================
def _getInclusiveHistogramsFromSingleSource(dsetMgr, dsetlabel, histoName, luminosity):
    myHistoList = []
    myNameList  = histoName.split("/")
    myMultipleFileNameStem = histoName
    myDsetRootHisto = dsetMgr.getDataset(dsetlabel).getDatasetRootHisto(myMultipleFileNameStem)
    if dsetMgr.getDataset(dsetlabel).isMC():
        myDsetRootHisto.normalizeToLuminosity(luminosity)
    h = myDsetRootHisto.getHistogram()
    ROOT.SetOwnership(h, True)
    myHistoList.append(h)
    return myHistoList

def Print(msg, printHeader=False):
    fName = __file__.split("/")[-1]
    if printHeader==True:
        print "=== ", fName
        print "\t", msg
    else:
        print "\t", msg
    return

#================================================================================================
# Class Definition
#================================================================================================
class DataDrivenQCDShape:
    '''
    Container class for information of data and MC EWK at certain point of selection
    '''
    def __init__(self, dsetMgr, dsetLabelData, dsetLabelEwk, histoName, dataPath, ewkPath, luminosity,  optionUseInclusiveNorm):
        self._uniqueN = 0
        self._splittedHistoReader = splittedHistoReader.SplittedHistoReader(dsetMgr, dsetLabelData)
        self._histoName = histoName
        self._optionUseInclusiveNorm = optionUseInclusiveNorm #ALEX-NEW
        dataFullName    = os.path.join(dataPath, histoName)
        ewkFullName     = os.path.join(ewkPath, histoName)

        # ALEX-NEW 
        if (self._optionUseInclusiveNorm):
            msg = "Disabled call for getting splitted histograms. Getting \"Inclusive\" histogram only instead."
            # Print(ShellStyles.WarningLabel() + msg, False)
            self._dataList  = list(_getInclusiveHistogramsFromSingleSource(dsetMgr, dsetLabelData, dataFullName, luminosity)) # was called by default
            self._ewkList   = list(_getInclusiveHistogramsFromSingleSource(dsetMgr, dsetLabelEwk , ewkFullName , luminosity)) # was called by default
        else:
            msg = "This splitted histograms method is not validated! Use \"Inclusive\" histogram only instead."
            Print(ShellStyles.WarningLabel() + msg, False)
            self._dataList  = list(self._splittedHistoReader.getSplittedBinHistograms(dsetMgr, dsetLabelData, dataFullName, luminosity)) #FIXME: Does this work for Inclusive?
            self._ewkList   = list(self._splittedHistoReader.getSplittedBinHistograms(dsetMgr, dsetLabelEwk , ewkFullName , luminosity)) #FIXME: Does this work for Inclusive?
        return

    def delete(self):
        '''
        Delete the histograms
        '''
        for h in self._dataList:
            if h == None:
                raise Exception("asdf")
            h.Delete()
        for h in self._ewkList:
            if h == None:
                raise Exception()
            h.Delete()
        self._dataList = []
        self._ewkList  = []
        return

    def getFileFriendlyHistoName(self):
        return self._histoName.replace("/","_")

    def getHistoName(self):
        return self._histoName

    def getDataDrivenQCDHistoForSplittedBin(self, binIndex):
        '''
        Return the sum of data-ewk in a given phase space split bin
        '''
        if binIndex >= len(self._dataList):
            raise Exception(ShellStyles.ErrorLabel()+"DataDrivenQCDShape::getDataDrivenQCDForSplittedBin: requested bin index %d out of range (0-%d)!"%(binIndex,len(self._dataList)))
        h = aux.Clone(self._dataList[binIndex])
        h.SetName(h.GetName()+"dataDriven")
        h.Add(self._ewkList[binIndex], -1.0)
        return h

    def getDataHistoForSplittedBin(self, binIndex):
        '''
        Return the data in a given phase space split bin
        '''
        if binIndex >= len(self._dataList):
            raise Exception(ShellStyles.ErrorLabel()+"DataDrivenQCDShape::getDataHistoForSplittedBin: requested bin index %d out of range (0-%d)!"%(binIndex,len(self._dataList)))
        h = aux.Clone(self._dataList[binIndex])
        h.SetName(h.GetName()+"_")
        return h
    
    def getEwkHistoForSplittedBin(self, binIndex):
        '''
        Return the EWK MC in a given phase space split bin
        '''
        if binIndex >= len(self._dataList):
            raise Exception(ShellStyles.ErrorLabel()+"DataDrivenQCDShape::getEwkHistoForSplittedBin: requested bin index %d out of range (0-%d)!"%(binIndex,len(self._ewkList)))
        h = aux.Clone(self._ewkList[binIndex])
        h.SetName(h.GetName()+"_")
        return h
    
    def getIntegratedDataDrivenQCDHisto(self):
        '''
        Return the sum of data-ewk integrated over the phase space splitted bins
        '''
        h = aux.Clone(self._dataList[0])
        h.SetName(h.GetName()+"Integrated")
        h.Add(self._ewkList[0],-1.0)
        for i in range(1, len(self._dataList)):
            h.Add(self._dataList[i])
            h.Add(self._ewkList[i],-1.0)
        return h

    def getIntegratedDataHisto(self):
        '''
        Return the sum of data integrated over the phase space splitted bins
        '''
        h = aux.Clone(self._dataList[0])
        h.SetName(h.GetName()+"Integrated")
        for i in range(1, len(self._dataList)):
            h.Add(self._dataList[i])
        return h
    
    def getIntegratedEwkHisto(self):
        '''
        Return the sum of ewk integrated over the phase space splitted bins
        '''
        h = aux.Clone(self._ewkList[0])
        h.SetName(h.GetName()+"Integrated")
        for i in range(1, len(self._dataList)):
            h.Add(self._ewkList[i])
        return h

    def getPurityHisto(self):
        '''
        Return the QCD purity as a histogram with splitted bins on x-axis
        '''
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
    
    def getIntegratedPurity(self):
        '''
        Return the QCD purity as a Count object
        '''
        nData = 0.0
        nEwk  = 0.0

        # For-loop:
        for i in range(0, len(self._dataList)):
            for j in range(0, self._dataList[i].GetNbinsX()+2):
                nData += self._dataList[i].GetBinContent(j)
                nEwk += self._ewkList[i].GetBinContent(j)

        myPurity = 0.0
        myUncert = 0.0

        if (nData > 0.0):
            # Assume binomial error
            myPurity = (nData - nEwk) / nData
            myUncert = sqrt(myPurity * (1.0-myPurity) / nData)
        return Count(myPurity, myUncert)

    def getMinimumPurity(self):
        '''
        Return the minimum QCD purity as a Count object
        '''
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

    def getIntegratedPurityForShapeHisto(self):
        '''
        Return the QCD purity in bins of the final shape
        '''
        hData    = self.getIntegratedDataHisto()
        hEwk     = self.getIntegratedEwkHisto()
        h        = aux.Clone(hData, "%s_purity_%d"%(hData,self._uniqueN))
        nameList = self._dataList[0].GetName().split("_")
        h.SetTitle("PurityByFinalShapeBin_%s"%nameList[0][:len(nameList[0])-1])
        self._uniqueN += 1

        # For-loop: All bins
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

    def getPhaseSpaceSplittingAxisLabels(self):
        '''
        Returns the labels of the phase space splitting axes
        '''
        return self._splittedHistoReader.getBinLabels()
    
    def getPhaseSpaceBinTitle(self, binIndex):
        '''
        Returns phase space split title for a bin
        '''
        if binIndex >= len(self._dataList):
            raise Exception(ShellStyles.ErrorLabel()+"DataDrivenQCDShape::getPhaseSpaceBinTitle: requested bin index %d out of range (0-%d)!"%(binIndex,len(self._dataList)))
        return self._dataList[binIndex].GetTitle()
    
    def getPhaseSpaceBinFileFriendlyTitle(self, binIndex):
        '''
        Returns phase space split title for a bin
        '''
        if binIndex >= len(self._dataList):
            raise Exception(ShellStyles.ErrorLabel()+"DataDrivenQCDShape::getPhaseSpaceBinTitle: requested bin index %d out of range (0-%d)!"%(binIndex,len(self._dataList)))
        return self._dataList[binIndex].GetTitle().replace(">","gt").replace("<","lt").replace("=","eq").replace("{","").replace("}","").replace(" ","").replace("#","").replace("..","to").replace("(","").replace(")","").replace(",","").replace("/","_").replace(".","p")
    
    def getNumberOfPhaseSpaceSplitBins(self):
        '''
        Returns number of phase space bins
        '''
        return self._splittedHistoReader.getMaxBinNumber()
    
    def getOutputHistoName(self, suffix=""):
        '''
        Returns name of histogram combined with the split bin title
        '''
        s = "%s"%(self._dataList[0].GetName().replace("/","_"))
        if len(suffix) > 0:
            s += "_%s"%suffix
        return s

#================================================================================================
# Class Definition
#================================================================================================
class DataDrivenQCDEfficiency:
    '''
    Efficiency from two shape objects
    '''
    def __init__(self, numerator, denominator):
        '''
        numerator and denominator are DataDrivenQCDShape objects
        '''
        self._efficiencies = [] # List of ExtendedCount objects, one for each phase space split bin
        self._calculate(numerator, denominator)
        return

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
        # FIXME: add histogram for efficiency
        return

