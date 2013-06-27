from HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShellStyles import *
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.SplittedHistoReader import *
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShapeHistoModifier import *
#from HiggsAnalysis.HeavyChHiggsToTauNu.tools.extendedCount import *
from math import sqrt
from dataset import Count

import ROOT
ROOT.gROOT.SetBatch(True) # no flashing canvases

## Container class for information of data and MC EWK at certain point of selection
class DataDrivenQCDShape:
    def __init__(self, dsetMgr, dsetLabelData, dsetLabelEwk, histoName):
        self._uniqueN = 0
        self._splittedHistoReader = SplittedHistoReader(dsetRootHisto.getHistogram())
        self._dataList = list(self._splittedHistoReader.getSplittedBinHistograms(dsetMgr, dsetLabelData, histoName))
        self._ewkList = list(self._splittedHistoReader.getSplittedBinHistograms(dsetMgr, dsetLabelEwk, histoName))

    ## Return the sum of data-ewk in a given phase space split bin
    def getDataDrivenQCDHistoForSplittedBin(self, binIndex, histoSpecs=None):
        if binIndex >= len(self._dataList):
            raise Exception(ErrorLabel()+"DataDrivenQCDShape::getDataDrivenQCDForSplittedBin: requested bin index %d out of range (0-%d)!"%(binIndex,len(self._dataList)))
        # Do summing within shape histo modifier
        myModifier = ShapeHistoModifier(histoSpecs, histoObjectForSpecs=self._dataList[binIndex])
        h = myModifier.createEmptyShapeHistogram("%s%d"%(self._dataList[binIndex].GetName(), self._uniqueN), self._dataList[binIndex].GetTitle())
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
        h = myModifier.createEmptyShapeHistogram("%s%d"%(self._dataList[binIndex].GetName(), self._uniqueN), self._dataList[binIndex].GetTitle())
        self._uniqueN += 1
        myModifier.addShape(source=self._dataList[binIndex], dest=h)
        myModifier.finaliseShape(dest=h) # Convert errors from variances to std.devs.
        return h

    ## Return the EWK MC in a given phase space split bin
    def getEwkHistoForSplittedBin(self, binIndex, histoSpecs=None):
        if binIndex >= len(self._dataList):
            raise Exception(ErrorLabel()+"DataDrivenQCDShape::getEwkHistoForSplittedBin: requested bin index %d out of range (0-%d)!"%(binIndex,len(self._dataList)))
        # Do summing within shape histo modifier
        myModifier = ShapeHistoModifier(histoSpecs, histoObjectForSpecs=self._ewkList[binIndex])
        h = myModifier.createEmptyShapeHistogram("%s%d"%(self._ewkList[binIndex].GetName(), self._uniqueN), self._ewkList[binIndex].GetTitle())
        self._uniqueN += 1
        myModifier.addShape(source=self._ewkList[binIndex], dest=h)
        myModifier.finaliseShape(dest=h) # Convert errors from variances to std.devs.
        return h

    ## Return the sum of data-ewk integrated over the phase space splitted bins
    def getIntegratedDataDrivenQCDHisto(self, histoSpecs=None):
        # Do summing within shape histo modifier
        myModifier = ShapeHistoModifier(histoSpecs, histoObjectForSpecs=self._dataList[0])
        h = myModifier.createEmptyShapeHistogram("%s%d"%(self._dataList[0].GetName(), self._uniqueN), self._dataList[0].GetTitle())
        self._uniqueN += 1
        for i in range(0, len(self._dataList)):
            myModifier.addShape(source=self._dataList[binIndex], dest=h)
            myModifier.subtractShape(source=self._ewkList[binIndex], dest=h)
        myModifier.finaliseShape(dest=h) # Convert errors from variances to std.devs.
        return h

    ## Return the sum of data integrated over the phase space splitted bins
    def getIntegratedDataHisto(self, histoSpecs=None):
        # Do summing within shape histo modifier
        myModifier = ShapeHistoModifier(histoSpecs, histoObjectForSpecs=self._dataList[0])
        h = myModifier.createEmptyShapeHistogram("%s%d"%(self._dataList[0].GetName(), self._uniqueN), self._dataList[0].GetTitle())
        self._uniqueN += 1
        for i in range(1, len(self._dataList)):
            myModifier.addShape(source=self._dataList[binIndex], dest=h)
        myModifier.finaliseShape(dest=h) # Convert errors from variances to std.devs.
        return h

    ## Return the sum of ewk integrated over the phase space splitted bins
    def getIntegratedEwkHisto(self, histoSpecs=None):
        # Do summing within shape histo modifier
        myModifier = ShapeHistoModifier(histoSpecs, histoObjectForSpecs=self._ewkList[0])
        h = myModifier.createEmptyShapeHistogram("%s%d"%(self._ewkList[0].GetName(), self._uniqueN), self._ewkList[0].GetTitle())
        self._uniqueN += 1
        for i in range(1, len(self._ewkList)):
            myModifier.addShape(source=self._ewkList[binIndex], dest=h)
        myModifier.finaliseShape(dest=h) # Convert errors from variances to std.devs.
        return h

    ## Return the QCD purity as a Count object
    def getPurity(self):
        nData = 0.0
        nEwk = 0.0
        for i in range(0, len(self._dataList)):
            for j in range(0, self._dataList[i].GetNbinsX()+2)):
                nData += self._dataList[i].GetBinContent(j)
                nEwk += self._ewkList[i].GetBinContent(j)
        myPurity = 0.0
        myUncert = 0.0
        if (nData > 0.0)
            myPurity = (nData - nEwk) / nData
            myUncert = sqrt(myPurity * (1.0-myPurity) * nData) # Assume binomial error
        return Count(myPurity, myUncert)

    ## Return the QCD purity in bins of the final shape
    def getPurityForShapeHisto(self, histoSpecs=None):
        hData = self.getIntegratedDataHisto()
        hEwk = self.getIntegratedEwkHisto()
        h = hData.Clone("%spurity%d"%(hData,self._uniqueN))
        self._uniqueN += 1
        for i in range(1, h.GetNbinxX()+1):
            myPurity = 0.0
            myUncert = 0.0
            if (hData.GetBinContent(i) > 0.0):
                myPurity = (hData.GetBinContent(i) - hEwk.GetBinContent(i)) / hData.GetBinContent(i)
                myUncert = sqrt(myPurity * (1.0-myPurity) * hData.GetBinContent(i)) # Assume binomial error
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

