from HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShellStyles import *
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.splittedHistoReader import *
from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.ShapeHistoModifier import *
#from HiggsAnalysis.HeavyChHiggsToTauNu.tools.extendedCount import *
from math import sqrt
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset import Count

import ROOT
ROOT.gROOT.SetBatch(True) # no flashing canvases

## Container class for information of data and MC EWK at certain point of selection
class DataDrivenQCDShape:
    def __init__(self, dsetMgr, dsetLabelData, dsetLabelEwk, histoName, luminosity):
        self._uniqueN = 0
        self._splittedHistoReader = SplittedHistoReader(dsetMgr, dsetLabelData)
        self._dataList = list(self._splittedHistoReader.getSplittedBinHistograms(dsetMgr, dsetLabelData, histoName, luminosity))
        self._ewkList = list(self._splittedHistoReader.getSplittedBinHistograms(dsetMgr, dsetLabelEwk, histoName, luminosity))

    ## Return the sum of data-ewk in a given phase space split bin
    def getDataDrivenQCDHistoForSplittedBin(self, binIndex, histoSpecs=None):
        if binIndex >= len(self._dataList):
            raise Exception(ErrorLabel()+"DataDrivenQCDShape::getDataDrivenQCDForSplittedBin: requested bin index %d out of range (0-%d)!"%(binIndex,len(self._dataList)))
        # Do summing within shape histo modifier
        myModifier = ShapeHistoModifier(histoSpecs, histoObjectForSpecs=self._dataList[binIndex])
        h = myModifier.createEmptyShapeHistogram("%s_%d"%(self._dataList[binIndex].GetName(), self._uniqueN), self._dataList[binIndex].GetTitle())
        self._uniqueN += 1
        myModifier.addShape(source=self._dataList[binIndex], dest=h)
        myModifier.subtractShape(source=self._ewkList[binIndex], dest=h)
        myModifier.finaliseShape(dest=h) # Convert errors from variances to std.devs.
        return h

    ## Return the data in a given phase space split bin
    def getDataHistoForSplittedBin(self, binIndex, histoSpecs=None):
        if binIndex >= len(self._dataList):
            raise Exception(ErrorLabel()+"DataDrivenQCDShape::getDataHistoForSplittedBin: requested bin index %d out of range (0-%d)!"%(binIndex,len(self._dataList)))
        # Do summing within shape histo modifier
        myModifier = ShapeHistoModifier(histoSpecs, histoObjectForSpecs=self._dataList[binIndex])
        h = myModifier.createEmptyShapeHistogram("%s_%d"%(self._dataList[binIndex].GetName(), self._uniqueN), self._dataList[binIndex].GetTitle())
        self._uniqueN += 1
        myModifier.addShape(source=self._dataList[binIndex], dest=h)
        myModifier.finaliseShape(dest=h) # Convert errors from variances to std.devs.
        return h

    ## Return the EWK MC in a given phase space split bin
    def getEwkHistoForSplittedBin(self, binIndex, histoSpecs=None):
        if binIndex >= len(self._dataList):
            raise Exception(ErrorLabel()+"DataDrivenQCDShape::getEwkHistoForSplittedBin: requested bin index %d out of range (0-%d)!"%(binIndex,len(self._ewkList)))
        # Do summing within shape histo modifier
        myModifier = ShapeHistoModifier(histoSpecs, histoObjectForSpecs=self._ewkList[binIndex])
        h = myModifier.createEmptyShapeHistogram("%s_%d"%(self._ewkList[binIndex].GetName(), self._uniqueN), self._ewkList[binIndex].GetTitle())
        self._uniqueN += 1
        myModifier.addShape(source=self._ewkList[binIndex], dest=h)
        myModifier.finaliseShape(dest=h) # Convert errors from variances to std.devs.
        return h

    ## Return the sum of data-ewk integrated over the phase space splitted bins
    def getIntegratedDataDrivenQCDHisto(self, histoSpecs=None):
        # Do summing within shape histo modifier
        myModifier = ShapeHistoModifier(histoSpecs, histoObjectForSpecs=self._dataList[0])
        myNameList = self._dataList[0].GetName().split("_")
        h = myModifier.createEmptyShapeHistogram("%s_%d"%(self._dataList[0].GetName(), self._uniqueN), myNameList[0][:len(myNameList[0])-1])
        self._uniqueN += 1
        for i in range(0, len(self._dataList)):
            myModifier.addShape(source=self._dataList[i], dest=h)
            myModifier.subtractShape(source=self._ewkList[i], dest=h)
        myModifier.finaliseShape(dest=h) # Convert errors from variances to std.devs.
        return h

    ## Return the sum of data integrated over the phase space splitted bins
    def getIntegratedDataHisto(self, histoSpecs=None):
        # Do summing within shape histo modifier
        myModifier = ShapeHistoModifier(histoSpecs, histoObjectForSpecs=self._dataList[0])
        myNameList = self._dataList[0].GetName().split("_")
        h = myModifier.createEmptyShapeHistogram("%s_%d"%(self._dataList[0].GetName(), self._uniqueN), myNameList[0][:len(myNameList[0])-1])
        self._uniqueN += 1
        for i in range(0, len(self._dataList)):
            myModifier.addShape(source=self._dataList[i], dest=h)
        myModifier.finaliseShape(dest=h) # Convert errors from variances to std.devs.
        return h

    ## Return the sum of ewk integrated over the phase space splitted bins
    def getIntegratedEwkHisto(self, histoSpecs=None):
        # Do summing within shape histo modifier
        myModifier = ShapeHistoModifier(histoSpecs, histoObjectForSpecs=self._ewkList[0])
        myNameList = self._ewkList[0].GetName().split("_")
        h = myModifier.createEmptyShapeHistogram("%s_%d"%(self._ewkList[0].GetName(), self._uniqueN), myNameList[0][:len(myNameList[0])-1])
        self._uniqueN += 1
        for i in range(0, len(self._ewkList)):
            myModifier.addShape(source=self._ewkList[i], dest=h)
        myModifier.finaliseShape(dest=h) # Convert errors from variances to std.devs.
        return h

    ## Return the QCD purity as a histogram with splitted bins on x-axis
    def getPurityHisto(self):
        # Create histogram
        myNameList = self._ewkList[0].GetName().split("_")
        h = ROOT.TH1F("%s_purity_%d"%(self._ewkList[0].GetName(), self._uniqueN), "PurityBySplittedBin_%s"%myNameList[0][:len(myNameList[0])-1], len(self._ewkList),0,len(self._ewkList))
        h.Sumw2()
        h.SetYTitle("Purity, %")
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

    ## Return the QCD purity in bins of the final shape
    def getIntegratedPurityForShapeHisto(self, histoSpecs=None):
        hData = self.getIntegratedDataHisto(histoSpecs=histoSpecs)
        hEwk = self.getIntegratedEwkHisto(histoSpecs=histoSpecs)
        h = hData.Clone("%s_purity_%d"%(hData,self._uniqueN))
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
            raise Exception(ErrorLabel()+"DataDrivenQCDShape::getPhaseSpaceBinTitle: requested bin index %d out of range (0-%d)!"%(binIndex,len(self._dataList)))
        return self._dataList[binIndex].GetTitle()

    ## Returns phase space split title for a bin
    def getPhaseSpaceBinFileFriendlyTitle(self, binIndex):
        if binIndex >= len(self._dataList):
            raise Exception(ErrorLabel()+"DataDrivenQCDShape::getPhaseSpaceBinTitle: requested bin index %d out of range (0-%d)!"%(binIndex,len(self._dataList)))
        return self._dataList[binIndex].GetTitle().replace(">","").replace("<","").replace("=","").replace("{","").replace("}","").replace(" ","").replace("#","").replace("..","to")

    ## Returns number of phase space bins
    def getNumberOfPhaseSpaceSplitBins(self):
        return self._splittedHistoReader.getMaxBinNumber()

