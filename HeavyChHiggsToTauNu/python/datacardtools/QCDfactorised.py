## \package QCDfactorised
# Classes for extracting and calculating multijet background with factorised approach

from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.Extractor import ExtractorMode,ExtractorBase
from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.DatacardColumn import ExtractorResult,DatacardColumn
from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.MulticrabPathFinder import MulticrabDirectoryDataType
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShellStyles import *
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset import Count
from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.ShapeHistoModifier import *
from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.UnfoldedHistogramReader import *
import math
import os
import sys
import ROOT

## Class for extending the Count object to include a third uncertainty
class QCDCountObject:
    def __init__(self,
                 value,
                 dataStat,
                 mcStat,
                 mcSyst):
        # Note that the number in value() must be exactly the same in both Count objects
        self._dataUncert = Count(value,dataStat,0.0)
        self._mcUncert = Count(value,mcStat,mcSyst)

    def value(self):
        return self._dataUncert.value()

    def setValue(self, value):
        self._dataUncert._value = value
        self._mcUncert._value = value

    def setObjectValues(self, count):
        self._dataUncert = count._dataUncert.copy()
        self._mcUncert = count._mcUncert.copy()

    def uncertainty(self):
        return sqrt(self._dataUncert.uncertainty()**2 + self._mcUncert.uncertainty()**2)

    def systUncertainty(self):
        return self._mcUncert.systUncertainty()

    def totalUncertainty(self):
        return sqrt(self.uncertainty()**2 + self.systUncertainty()**2)

    def getRelativeDataStatUncertainty(self):
        if self._dataUncert.value() > 0:
            return self._dataUncert.uncertainty() / self._dataUncert.value()
        else:
            return 0.0

    def getRelativeMCStatUncertainty(self):
        if self._mcUncert.value() > 0:
            return self._mcUncert.uncertainty() / self._mcUncert.value()
        else:
            return 0.0

    def getRelativeMCSystUncertainty(self):
        if self._mcUncert.value() > 0:
            return self._mcUncert.systUncertainty() / self._mcUncert.value()
        else:
            return 0.0

    def getNQCD(self):
        return self._dataUncert.value()

    def getCountObject(self):
        return Count(self.value(), self.uncertainty(), self.systUncertainty())

    def copy(self):
        return QCDCountObject(self._dataUncert.value(), self._dataUncert.uncertainty(), self._mcUncert.uncertainty(), self._mcUncert.systUncertainty())

    def add(self, count):
        self._dataUncert.add(count._dataUncert)
        self._mcUncert.add(count._mcUncert)

    def subtract(self, count):
        self._dataUncert.subtract(count._dataUncert)
        self._mcUncert.subtract(count._mcUncert)

    def multiply(self, count):
        self._dataUncert.multiply(count._dataUncert)
        self._mcUncert.multiply(count._mcUncert)

    def divide(self, count):
        self._dataUncert.divide(count._dataUncert)
        self._mcUncert.divide(count._mcUncert)

    def multiplyByScalar(self, scalar):
        self._dataUncert._value *= scalar
        self._dataUncert._uncertainty *= scalar
        self._mcUncert._value *= scalar
        self._mcUncert._uncertainty *= scalar
        self._mcUncert._systUncertainty *= scalar

    def divideByScalar(self, scalar):
        self._dataUncert._value /= scalar
        self._dataUncert._uncertainty /= scalar
        self._mcUncert._value /= scalar
        self._mcUncert._uncertainty /= scalar
        self._mcUncert._systUncertainty /= scalar

    def minimum(self, count):
        if count == None:
            return
        if count.value() < self.value() and count.value() > 0.0:
            self.setObjectValues(count)

    def maximum(self, count):
        if count == None:
            return
        if count.value() > self.value():
            return self.setObjectValues(count)

    def printContents(self):
        print "(%s,%s,%s,%s)"%(self._dataUncert._value, self._dataUncert._uncertainty, self._mcUncert._uncertainty, self._mcUncert._systUncertainty)

    def getResultStringFull(self, formatStr):
        s = "%s +- %s (stat.) +- %s (syst.)"%(formatStr,formatStr,formatStr)
        return s%(self.value(),self.uncertainty(),self.systUncertainty())

    def getLatexStringFull(self, formatStr):
        s = "%s $\\pm$ %s $\\pm$ %s"%(formatStr,formatStr,formatStr)
        return s%(self.value(),self.uncertainty(),self.systUncertainty())

    def getLatexStringNoSyst(self, formatStr):
        s = "%s $\\pm$ %s"%(formatStr,formatStr)
        return s%(self.value(),self.uncertainty())

    def sanityCheck(self):
        return abs(self._dataUncert._value-self._mcUncert._value) < 0.00001 and self._dataUncert._systUncertainty < 0.00001

class QCDResultObject:
    def __init__(self, title):
        self._title = title
        self._NQCDResult = None
        self._minPurityObjects = [None, None, None]
        self._avgPurityObjects = [None, None, None]

    def setNQCDResult(self, r):
        self._NQCDResult = r.copy()

    def getNQCDResult(self):
        return self._NQCDResult

    def setPurityInfo(self, minPurity, avgPurity, i):
        self._minPurityObjects[i] = minPurity
        self._avgPurityObjects[i] = avgPurity

    def getInfoString(self):
        myOutput = "QCD factorised results summary for %s\n"%self._title
        myOutput += "... NQCD = %s  (data stat=%.2f, MC EWK stat=%.2f)\n"%(self._NQCDResult.getResultStringFull("%.2f"),self._NQCDResult._dataUncert.uncertainty(),self._NQCDResult._mcUncert.uncertainty())
        myOutput += "... Purity after std. sel.: minimum = %s, average = %s\n"%(self._minPurityObjects[0].getResultStringFull("%.3f"),self._avgPurityObjects[0].getResultStringFull("%.3f"))
        myOutput += "... Purity after     leg1.: minimum = %s, average = %s\n"%(self._minPurityObjects[1].getResultStringFull("%.3f"),self._avgPurityObjects[1].getResultStringFull("%.3f"))
        myOutput += "... Purity after     leg2.: minimum = %s, average = %s\n"%(self._minPurityObjects[2].getResultStringFull("%.3f"),self._avgPurityObjects[2].getResultStringFull("%.3f"))
        return myOutput

## Extracts data-MC EWK counts from a given point in the analysis
class QCDEventCount:
    def __init__(self,
                 histoName,
                 dsetMgr,
                 dsetMgrDataColumn,
                 dsetMgrMCEWKColumn,
                 luminosity):
        self._histoname = histoName
        # Obtain histograms
        print "QCDfact: Obtaining factorisation histogram: %s"%histoName
        try:
            datasetRootHistoData = dsetMgr.getDataset(dsetMgrDataColumn).getDatasetRootHisto(histoName)
        except Exception, e:
            raise Exception (ErrorStyle()+"Error in QCDfactorised/QCDEventCount:"+NormalStyle()+" cannot find histogram for data!\n  Message = %s!"%(str(e)))
        try:
            datasetRootHistoMCEWK = dsetMgr.getDataset(dsetMgrMCEWKColumn).getDatasetRootHisto(histoName)
        except Exception, e:
            raise Exception (ErrorStyle()+"Error in QCDfactorised/QCDEventCount:"+NormalStyle()+" cannot find histogram for MC EWK!\n  Message = %s!"%(str(e)))
        datasetRootHistoMCEWK.normalizeToLuminosity(luminosity)
        self._hData = datasetRootHistoData.getHistogram()
        self._hMC = datasetRootHistoMCEWK.getHistogram()
        self._reader = UnfoldedHistogramReader(debugStatus=False)
        self._reader._initialize(self._hData)
        self._messages = []
        self._warnedAboutSystematics = False
        # Find tau pT bin index (needed for systematics)
        self._tauPtAxisIndex = None
        for i in range(0, len(self._reader.getBinLabelList())):
            if "tau" in self._reader.getBinLabelList()[i].lower() and "pt" in self._reader.getBinLabelList()[i].lower():
                self._tauPtAxisIndex = i
        if self._tauPtAxisIndex == None:
            raise Exception (ErrorLabel()+"QCDfactorised/QCDEventCount: cannot find 'tau' and 'pt' in one of the axis labels! They are needed for MC EWK systematics (tau trigger syst. depends on tau pT)!")

    def clean(self):
        if self._hData != None:
            self._hData.IsA().Destructor(self._hData)
        if self._hMC != None:
            self._hMC.IsA().Destructor(self._hMC)
        self._messages = []

    def getFactorisationDimensions(self):
        return self._reader.getNbinsList()

    def getNShapeBins(self):
        return self._hData.GetNbinsX()

    def isShapeHistogram(self):
        return self.getNShapeBins() > 1

    def getMessages(self):
        return self._messages

    def getNbins(self):
        return self._hData.GetNbinsX()

    def getNFactorisationBins(self):
        return self._hData.GetNbinsY()

    def getClonedHisto(self, name):
        return self._hData.Clone(name)

    def getFactorisationBinLabel(self, i):
        return self._hData.GetYaxis().GetBinLabel(i+1)

    def getReader(self):
        return self._reader

    def getEWKMCRelativeSystematicUncertainty(self,tauPtBinIndex):
        if not self._warnedAboutSystematics:
            print WarningLabel()+"QCD factorised: check/update hard coded values in QCDEventCount::getEWKMCRelativeSystematicUncertainty()"
            self._warnedAboutSystematics = True
        myTauTrgUncertainty = 0.0
        if tauPtBinIndex == 0:
            myTauTrgUncertainty = 0.061 / 0.92
        elif tauPtBinIndex == 1:
            myTauTrgUncertainty = 0.11 / 0.91
        elif tauPtBinIndex == 2 or tauPtBinIndex == 3:
            myTauTrgUncertainty = 0.13 / 1.00
        else:
            myTauTrgUncertainty = 0.34 / 0.91
        #else:
            #raise Exception("tau trigger scale factor uncertainty not defined for tau pt bin ",tauPtBin)
        # tau trg uncert + trg MET leg uncert + tauID + ES + btag
        # i.e. tau trg uncert (+) 19.3 %
        myRelativeSystUncertainty = sqrt(myTauTrgUncertainty**2
                                         + 0.10**2 # trg MET leg
                                         + 0.10**2 # tau ID (take into account a portion of fake taus)
                                         + 0.05**2 # energy scale
                                         + 0.05**2 # btagging
                                         + 0.07**2) # xsection
        return myRelativeSystUncertainty

    def printFactorisationInfo(self):
        self._reader.printFactorisationDefinitions() # Assuming that reader._initialize() has already been called

    # Getters for data and MC counts --------------------------------------------------------------------------
    ## Returns count objects for an unfolded bin of data
    # unfoldedBinIndex is the unfolded bin (numbering from zero)
    def getDataCountObjectsByUnfoldedBin(self, unfoldedBinIndex):
        myValues = self._reader.getShapeByUnfoldedBin(unfoldedBinIndex, self._hData)
        myStatUncertainties = self._reader.getShapeUncertaintyByUnfoldedBin(unfoldedBinIndex, self._hData)
        myResult = []
        for i in range(0,len(myValues)):
            myResult.append(QCDCountObject(myValues[i], myStatUncertainties[i], 0.0, 0.0))
        return myResult

    ## Returns count objects for data
    # factorisationBinIndexList is a list of indices corresponding to the factorisation bin
    def getDataCountObjects(self, factorisationBinIndexList):
        myValues = self._reader.getShapeForBin(factorisationBinIndexList, self._hData)
        myStatUncertainties = self._reader.getShapeUncertaintyForBin(factorisationBinIndexList, self._hData)
        myResult = []
        for i in range(0,len(myValues)):
            myResult.append(QCDCountObject(myValues[i], myStatUncertainties[i], 0.0, 0.0))
        return myResult

    ## Returns count objects for data contracted to one factorisation dimension
    # axisIndexToKeep is the axis to be kept (for example: to keep first variable, ask for 0)
    # factorisationBinIndex is a list of indices corresponding to the factorisation bin
    def getContracted1DDataCountObjects(self, factorisationBinIndex, axisIndexToKeep):
        myValues = self._reader.getContractedShapeForBin(axisIndexToKeep, factorisationBinIndex, self._hData)
        myStatUncertainties = self._reader.getContractedShapeUncertaintyForBin(axisIndexToKeep, factorisationBinIndex, self._hData)
        myResult = []
        for i in range(0,len(myValues)):
            myResult.append(QCDCountObject(myValues[i], myStatUncertainties[i], 0.0, 0.0))
        return myResult

    ## Returns count objects for an unfolded bin of MC EWK
    # unfoldedBinIndex is the unfolded bin (numbering from zero)
    def getMCCountObjectsByUnfoldedBin(self, unfoldedBinIndex):
        myValues = self._reader.getShapeByUnfoldedBin(unfoldedBinIndex, self._hMC)
        myStatUncertainties = self._reader.getShapeUncertaintyByUnfoldedBin(unfoldedBinIndex, self._hMC)
        myTauPtIndex = self._reader.decomposeUnfoldedbin(unfoldedBinIndex)[self._tauPtAxisIndex]
        mySystFactor = self.getEWKMCRelativeSystematicUncertainty(myTauPtIndex)
        myResult = []
        for i in range(0,len(myValues)):
            mySystUncertainty = myValues[i] * mySystFactor
            myResult.append(QCDCountObject(myValues[i], 0.0, myStatUncertainties[i], mySystUncertainty))
        return myResult

    ## Returns count objects for MC EWK
    # factorisationBinIndexList is a list of indices corresponding to the factorisation bin
    def getMCCountObjects(self, factorisationBinIndexList):
        myValues = self._reader.getShapeForBin(factorisationBinIndexList, self._hMC)
        myStatUncertainties = self._reader.getShapeUncertaintyForBin(factorisationBinIndexList, self._hMC)
        mySystFactor = self.getEWKMCRelativeSystematicUncertainty(factorisationBinIndexList[self._tauPtAxisIndex])
        myResult = []
        for i in range(0,len(myValues)):
            mySystUncertainty = myValues[i] * mySystFactor
            myResult.append(QCDCountObject(myValues[i], 0.0, myStatUncertainties[i], mySystUncertainty))
        return myResult

    ## Returns count objects for MC contracted to one factorisation dimension
    # axisIndexToKeep is the axis to be kept (for example: to keep first variable, ask for 0)
    # factorisationBinIndex is a list of indices corresponding to the factorisation bin
    def getContracted1DMCCountObjects(self, factorisationBinIndex, axisIndexToKeep):
        myValues = self._reader.getContractedShapeForBin(axisIndexToKeep, factorisationBinIndex, self._hMC)
        myStatUncertainties = self._reader.getContractedShapeUncertaintyForBin(axisIndexToKeep, factorisationBinIndex, self._hMC)
        mySystFactor = self.getEWKMCRelativeSystematicUncertainty(999)
        myResult = []
        for i in range(0,len(myValues)):
            mySystUncertainty = myValues[i] * mySystFactor
            myResult.append(QCDCountObject(myValues[i], 0.0, myStatUncertainties[i], mySystUncertainty))
        return myResult

    # QCD count (data-EWK) calculation --------------------------------------------------------------------------------------

    ## Returns Count object for data-MC (uncertainty separately for stat. and syst. uncertainty)
    # factorisationBinIndexList is a list of indices corresponding to the factorisation bin
    def getQCDCount(self, factorisationBinIndexList, cleanNegativeValues=True):
        myDataObjects = self.getDataCountObjects(factorisationBinIndexList)
        myMCObjects = self.getMCCountObjects(factorisationBinIndexList)
        return self._calculateQCDCount(myDataObjects, myMCObjects, cleanNegativeValues)

    ## Returns Count object for data-MC (uncertainty separately for stat. and syst. uncertainty)
    # unfoldedBinIndex is the unfolded bin (numbering from zero)
    def getQCDCountByUnfoldedBin(self, unfoldedBinIndex, cleanNegativeValues=True):
        myDataObjects = self.getDataCountObjectsByUnfoldedBin(unfoldedBinIndex)
        myMCObjects = self.getMCCountObjectsByUnfoldedBin(unfoldedBinIndex)
        return self._calculateQCDCount(myDataObjects, myMCObjects, cleanNegativeValues)

    ## Returns Count object for data-MC for a bin on a variation parameter, other parameters are contracted (i.e. summed)
    # (uncertainty separately for stat. and syst. uncertainty)
    # factorisationBinIndex is a list of indices corresponding to the factorisation bin
    # axisIndexToKeep is the axis to be kept (for example: to keep first variable, ask for 0)
    def getContracted1DQCDCount(self, factorisationBinIndex, axisIndexToKeep, cleanNegativeValues=True):
        myDataObjects = self.getContracted1DDataCountObjects(factorisationBinIndex, axisIndexToKeep)
        myMCObjects = self.getContracted1DMCCountObjects(factorisationBinIndex, axisIndexToKeep)
        return self._calculateQCDCount(myDataObjects, myMCObjects, cleanNegativeValues)

    def _calculateQCDCount(self, myDataObjects, myMCObjects, cleanNegativeValues):
        myResult = []
        for i in range(0,len(myDataObjects)):
            r = myDataObjects[i].copy()
            r.subtract(myMCObjects[i])
            # Obtain uncertainty # Check negative result
            if r.value() < 0.0:
                if cleanNegativeValues:
                    r.setValue(0.0)
                #myResultError = 0.0 do not set it to zero, but instead keep it as it is to be more realistic!
            myResult.append(r)
        # Return result
        return myResult

    # Purity calculation --------------------------------------------------------------------------------------
    ## Getter for purity (data-MC)/data = 1-MC/data
    # Returns Count object
    def getPurity(self, factorisationBinIndexList):
        myDataCounts = self.getDataCountObjects(factorisationBinIndexList)
        myMCCounts = self.getMCCountObjects(factorisationBinIndexList)
        return self._calculatePurity(myDataCounts, myMCCounts)

    ## Getter for purity (data-MC)/data = 1-MC/data for unfolded bin index
    # Returns Count object
    def getPurityByUnfoldedBin(self, unfoldedBinIndex):
        myDataCounts = self.getDataCountObjectsByUnfoldedBin(unfoldedBinIndex)
        myMCCounts = self.getMCCountObjectsByUnfoldedBin(unfoldedBinIndex)
        return self._calculatePurity(myDataCounts, myMCCounts)

    ## Getter for purity (data-MC)/data = 1-MC/data contracted to one factorisation axis
    # Returns Count object
    def getContracted1DPurity(self, factorisationBinIndex, axisIndexToKeep):
        myDataCounts = self.getContracted1DDataCountObjects(factorisationBinIndex, axisIndexToKeep)
        myMCCounts = self.getContracted1DMCCountObjects(factorisationBinIndex, axisIndexToKeep)
        return self._calculatePurity(myDataCounts, myMCCounts)

    ## Actual calculation of the purity value with Count objects
    def _calculatePurity(self, data, mc):
        myResult = []
        for i in range(0,len(data)):
            r = mc[i].copy()
            if data[i].value() > 0:
                r.divide(data[i])
                r.setValue(1.0 - r.value())
            else:
                # Set purity value to zero, but count uncertainty properly
                myDummyData = QCDCountObject(1.0, 1.0, 0.0, 0.0)
                r.divide(myDummyData)
                r.setValue(0.0)
            myResult.append(r)
        return myResult

    ## Getter for purity overall view
    # Returns two count objects (minimum purity and average purity weighted by NQCD counts)
    def getPurityInfo(self):
        myNbins = self._reader.getUnfoldedBinCount()
        myMinPurity = QCDCountObject(10.0, 0.0, 0.0, 0.0)
        myPuritySum = QCDCountObject(0.0, 0.0, 0.0, 0.0)
        myWeightSum = 0.0
        for i in range(0,myNbins):
            myPurities = self.getPurityByUnfoldedBin(i)
            for k in range(0,len(myPurities)):
                myMinPurity.minimum(myPurities[k])
            myNQCD = self.getQCDCountByUnfoldedBin(i)
            for k in range(0,len(myPurities)):
                myElement = myPurities[k].copy()
                myElement.multiplyByScalar(myNQCD[k].value())
                myWeightSum += myNQCD[k].value()
                myPuritySum.add(myElement)
        myPuritySum.divideByScalar(myWeightSum)
        return (myMinPurity, myPuritySum)

    ## Getter for purity (data-MC)/data = 1-MC/data contracted to one factorisation axis
    # Returns Count object
    def getContracted1DPurityInfo(self, axisIndexToKeep):
        myNbins = self.getFactorisationDimensions()[axisIndexToKeep]
        myMinPurity = QCDCountObject(10.0, 0.0, 0.0, 0.0)
        myPuritySum = QCDCountObject(0.0, 0.0, 0.0, 0.0)
        myWeightSum = 0.0
        for i in range(0,myNbins):
            myPurities = self.getContracted1DPurity(i,axisIndexToKeep)
            for k in range(0,len(myPurities)):
                myMinPurity.minimum(myPurities[k])
            myNQCD = self.getContracted1DQCDCount(i,axisIndexToKeep)
            for k in range(0,len(myPurities)):
                myElement = myPurities[k].copy()
                myElement.multiplyByScalar(myNQCD[k].value())
                myWeightSum += myNQCD[k].value()
                myPuritySum.add(myElement)
        myPuritySum.divideByScalar(myWeightSum)
        return (myMinPurity, myPuritySum)

    # Returns a histogram for stat only and another one for full uncertainties
    def _createEmptyHistograms(self, label, axisLabel, contractionDim=None, minimum=None, maximum=None):
        s = label
        if contractionDim != None:
            s += "_%s"%self._reader.getBinLabelList()[contractionDim].replace(" ","_")
        myStatName = "%s_StatOnly_%s"%(s, self._histoname.replace("/","_"))
        myFullName = myStatName.replace("StatOnly","StatAndSyst")
        hStat = None
        hFull = None
        nFactorisationBins = self._hData.GetNbinsY()
        if contractionDim != None:
            nFactorisationBins =  self.getFactorisationDimensions()[contractionDim]
        # Create histogram objects
        if self.isShapeHistogram():
            nbins = self.getNShapeBins()
            hStat = ROOT.TH2F(myStatName,myStatName,nbins,self._hData.GetYaxis().GetXmin(),self._hData.GetYaxis().GetXmax(),nFactorisationBins,0.0,nFactorisationBins)
            hFull = ROOT.TH2F(myFullName,myFullName,nbins,self._hData.GetYaxis().GetXmin(),self._hData.GetYaxis().GetXmax(),nFactorisationBins,0.0,nFactorisationBins)
            if contractionDim != None:
                hStat.SetYTitle(self._reader.getFactorisationCaptions()[contractionDim])
                hFull.SetYTitle(self._reader.getFactorisationCaptions()[contractionDim])
        else:
            hStat = ROOT.TH1F(myStatName,myStatName,nFactorisationBins,0.0,nFactorisationBins)
            hFull = ROOT.TH1F(myFullName,myFullName,nFactorisationBins,0.0,nFactorisationBins)
            if contractionDim != None:
                hStat.SetXTitle(self._reader.getFactorisationCaptions()[contractionDim])
                hFull.SetXTitle(self._reader.getFactorisationCaptions()[contractionDim])
            hStat.SetYTitle(axisLabel)
            hFull.SetYTitle(axisLabel)
        # Set minimum and maximum
        if maximum != None:
            if self.isShapeHistogram():
                hStat.SetMaximum(maximum)
                hFull.SetMaximum(maximum)
            else:
                hStat.SetMaximum(maximum*1.1)
                hFull.SetMaximum(maximum*1.1)
        if minimum != None:
            hStat.SetMinimum(minimum)
            hFull.SetMinimum(minimum)
        # Make axis labels
        if contractionDim == None:
            for i in range(0,self._hData.GetNbinsY()):
                if not self.isShapeHistogram():
                    hStat.GetXaxis().SetBinLabel(i+1,self._hData.GetYaxis().GetBinLabel(i+1))
                    hFull.GetXaxis().SetBinLabel(i+1,self._hData.GetYaxis().GetBinLabel(i+1))
                else:
                    hStat.GetYaxis().SetBinLabel(i+1,self._hData.GetYaxis().GetBinLabel(i+1))
                    hFull.GetYaxis().SetBinLabel(i+1,self._hData.GetYaxis().GetBinLabel(i+1))
        else:
            for i in range(0,self.getFactorisationDimensions()[contractionDim]):
                if not self.isShapeHistogram():
                    hStat.GetXaxis().SetBinLabel(i+1,self._reader.getFactorisationRanges()[contractionDim][i])
                    hFull.GetXaxis().SetBinLabel(i+1,self._reader.getFactorisationRanges()[contractionDim][i])
                else:
                    hStat.GetYaxis().SetBinLabel(i+1,self._reader.getFactorisationRanges()[contractionDim][i])
                    hFull.GetYaxis().SetBinLabel(i+1,self._reader.getFactorisationRanges()[contractionDim][i])
        if self.isShapeHistogram():
            for k in range(0,self._hData.GetNbinsX()):
                hStat.GetXaxis().SetBinLabel(k+1,self._hData.GetXaxis().GetBinLabel(k+1))
                hFull.GetXaxis().SetBinLabel(k+1,self._hData.GetXaxis().GetBinLabel(k+1))
        # Return histograms
        return (hStat,hFull)

    def _fillHistogramValues(self, hStat, hFull, resultObjects, factorisationBin):
        if len(resultObjects) == 1:
            # Count histogram - put factorisation bins on x axis
            hStat.SetBinContent(factorisationBin+1, resultObjects[0].value())
            hStat.SetBinError(factorisationBin+1, resultObjects[0].uncertainty())
            hFull.SetBinContent(factorisationBin+1, resultObjects[0].value())
            hFull.SetBinError(factorisationBin+1, resultObjects[0].totalUncertainty())
        else:
            # Shape histogram - put factorisation bins on y axis
            for k in range(0,len(resultObjects)):
                hStat.SetBinContent(k+1, factorisationBin+1, resultObjects[k].value())
                hStat.SetBinError(k+1, factorisationBin+1, resultObjects[k].uncertainty())
                hFull.SetBinContent(k+1, factorisationBin+1, resultObjects[k].value())
                hFull.SetBinError(k+1, factorisationBin+1, resultObjects[k].totalUncertainty())

    ## Returns purity histograms (purity as function of the unfolded factorisation binning and contracted histograms)
    def makePurityHistograms(self):
        hlist = []
        # Make uncontracted histograms (can be a loooot of bins)
        (hStat,hFull) = self._createEmptyHistograms("Purity","Purity",minimum=0.0,maximum=1.0)
        for i in range(0,self._hData.GetNbinsY()):
            # Obtain values and fill histograms
            myPurities = self.getPurityByUnfoldedBin(i)
            self._fillHistogramValues(hStat,hFull,myPurities,i)
            # Do additional checks
            if not self.isShapeHistogram():
                # Count histogram
                if myPurities[0].value() > 0.0 and myPurities[0].value() < 0.5:
                    myMsg = WarningLabel()+"QCD factorised: Low purity in %s for bin %s (%s)!"%(self._histoname,self._hData.GetYaxis().GetBinLabel(i+1),myPurities[0].getResultStringFull("%.4f"))
                    self._messages.append(myMsg)
        hlist.append(hStat)
        hlist.append(hFull)
        # Make contracted histograms (easier to read)
        myBinDimensions = self.getFactorisationDimensions()
        for myDim in range(0, len(myBinDimensions)):
            (hCStat,hCFull) = self._createEmptyHistograms("Purity","Purity",contractionDim=myDim,minimum=0.0,maximum=1.1)
            for i in range(0, myBinDimensions[myDim]):
                # Obtain values and fill histograms
                myPurities = self.getContracted1DPurity(i, myDim)
                self._fillHistogramValues(hCStat,hCFull,myPurities,i)
                # Do additional checks
                if not self.isShapeHistogram():
                    # Count histogram
                    if myPurities[0].value() > 0.0 and myPurities[0].value() < 0.5:
                        myMsg = WarningLabel()+"QCD factorised: Low purity in %s for contracted bin %s %s (%s)!"%(self._histoname,self._reader.getFactorisationCaptions()[myDim],self._reader.getFactorisationRanges()[myDim][i],myPurities[0].getResultStringFull("%.4f"))
                        self._messages.append(myMsg)
            hlist.append(hCStat)
            hlist.append(hCFull)
        for h in hlist:
            ROOT.SetOwnership(h, True)
        return hlist

    ## Returns Nevent histograms (Nevent as function of the unfolded factorisation binning and contracted histograms)
    ## Returns histogram(s) for number of events
    def makeEventCountHistograms(self):
        hlist = []
        # Make uncontracted histograms (can be a loooot of bins)
        (hStat,hFull) = self._createEmptyHistograms("Nevents","N_{events}")
        for i in range(0,self._hData.GetNbinsY()):
            # Obtain values and fill histograms
            myResults = self.getQCDCountByUnfoldedBin(i)
            self._fillHistogramValues(hStat,hFull,myResults,i)
        hlist.append(hStat)
        hlist.append(hFull)
        # Make contracted histograms (easier to read)
        myBinDimensions = self.getFactorisationDimensions()
        for myDim in range(0, len(myBinDimensions)):
            myString = "Nevents"
            if not self.isShapeHistogram():
                myString = "dN_{events}/d(%s)"%self._reader.getFactorisationCaptions()[myDim]
            (hCStat,hCFull) = self._createEmptyHistograms("Nevents",myString,contractionDim=myDim)
            for i in range(0, myBinDimensions[myDim]):
                # Obtain values and fill histograms
                myResults = self.getContracted1DQCDCount(i, myDim)
                if not self.isShapeHistogram():
                    # Divide by bin width
                    myWidthString = self._reader.getFactorisationRanges()[myDim][i].split("..")
                    myBinWidth = 1
                    if len(myWidthString) == 2:
                        myBinWidth = float(myWidthString[1]) - float(myWidthString[0])
                    for k in range(0,len(myResults)):
                        myResults[k].divideByScalar(myBinWidth)
                self._fillHistogramValues(hCStat,hCFull,myResults,i)
            hlist.append(hCStat)
            hlist.append(hCFull)
        for h in hlist:
            ROOT.SetOwnership(h, True)
        return hlist


    ## Returns histogram(s) for checking the impact of negative QCD counts
    def makeNegativeEventCountHistograms(self):
        hlist = []
        # Make uncontracted histograms (can be a loooot of bins)
        (hStat,hFull) = self._createEmptyHistograms("NegativeNevents","N_{events}")
        for i in range(0,self._hData.GetNbinsY()):
            # Obtain values and fill histograms
            myResults = self.getQCDCountByUnfoldedBin(i)
            # Fill only negative values
            for k in range(0,len(myResults)):
                if myResults[k].value() > 0:
                    myResults[k] = QCDCountObject(0.0, 0.0, 0.0, 0.0)
            self._fillHistogramValues(hStat,hFull,myResults,i)
        hlist.append(hStat)
        hlist.append(hFull)
        # Make contracted histograms (easier to read)
        myBinDimensions = self.getFactorisationDimensions()
        for myDim in range(0, len(myBinDimensions)):
            myString = "Nevents"
            if not self.isShapeHistogram():
                myString = "dN_{events}/d(%s)"%self._reader.getFactorisationCaptions()[myDim]
            (hCStat,hCFull) = self._createEmptyHistograms("NegativeNevents",myString,contractionDim=myDim)
            for i in range(0, myBinDimensions[myDim]):
                # Obtain values and fill histograms
                myResults = self.getContracted1DQCDCount(i, myDim)
                if not self.isShapeHistogram():
                    # Divide by bin width
                    myWidthString = self._reader.getFactorisationRanges()[myDim][i].split("..")
                    myBinWidth = 1
                    if len(myWidthString) == 2:
                        myBinWidth = float(myWidthString[1]) - float(myWidthString[0])
                    for k in range(0,len(myResults)):
                        myResults[k].divideByScalar(myBinWidth)
                # Fill only negative values
                for k in range(0,len(myResults)):
                    if myResults[k].value() > 0:
                        myResults[k] = QCDCountObject(0.0, 0.0, 0.0, 0.0)
                self._fillHistogramValues(hCStat,hCFull,myResults,i)
            hlist.append(hCStat)
            hlist.append(hCFull)
        for h in hlist:
            ROOT.SetOwnership(h, True)
        return hlist

## Helper class for calculating the result from three points of counting in the analysis
class QCDfactorisedCalculator:
    def __init__(self, basicCounts, leg1Counts, leg2Counts, doHistograms=False):
        self._basicCount = basicCounts
        self._leg1Counts = leg1Counts
        self._leg2Counts = leg2Counts

        self._yieldTable = ""
        self._compactYieldTable = ""

        # Count NQCD
        self._result = None # QCDResultObject , NQCD calculate with full parameter space
        self._contractedResults = [] # List of QCDResultObject objects, NQCD calculated by first contracting parameter space to one dimension
        self._nQCDHistograms = []
        self._count()

        # Make yield tables
        if doHistograms:
            self._yieldTable = self._createYieldTable()
            self._compactYieldTable = self._createCompactYieldTable()

    def clean(self):
        self._basicCount.clean()
        self._leg1Counts.clean()
        self._leg2Counts.clean()

    def getCompactYieldTable(self):
        return self._compactYieldTable

    def getYieldTable(self):
        return self._yieldTable

    def getResult(self):
        return self._result

    def getContractedResultsList(self):
        return self._contractedResults

    def getNQCDHistograms(self):
        return self._nQCDHistograms

    ## Returns reference to UnfoldedHistogramReader object - needed for accessing binning information
    def getReaderObject(self):
        return self._basicCount.getReader()

    def getLeg1EfficiencyByUnfoldedBin(self, unfoldedBinIndex):
        return self._getEfficiencyByUnfoldedBin(self, self._leg1Counts, self._basicCount, unfoldedBinIndex)

    def getLeg2EfficiencyByUnfoldedBin(self, unfoldedBinIndex):
        return self._getEfficiencyByUnfoldedBin(self, self._leg2Counts, self._basicCount, unfoldedBinIndex)

    def getLeg1Efficiency(self, factorisationBinIndexList):
        return self._getEfficiency(self._leg1Counts, self._basicCount, factorisationBinIndexList)

    def getLeg2Efficiency(self, factorisationBinIndexList):
        return self._getEfficiency(self._leg2Counts, self._basicCount, factorisationBinIndexList)

    def _getEfficiencyByUnfoldedBin(self,numerator,denominator,unfoldedBinIndex):
        numeratorCounts = numerator.getQCDCountByUnfoldedBin(unfoldedBinIndex)
        denominatorCounts = denominator.getQCDCountByUnfoldedBin(unfoldedBinIndex)
        return self._calculateEfficiency(numeratorCounts,denominatorCounts)

    def _getEfficiency(self,numerator,denominator,factorisationBinIndexList):
        numeratorCounts = numerator.getQCDCount(factorisationBinIndexList)
        denominatorCounts = denominator.getQCDCount(factorisationBinIndexList)
        return self._calculateEfficiency(numeratorCounts,denominatorCounts)

    def _calculateEfficiency(self,numerator,denominator):
        myResult = []
        for i in range(0, len(numerator)):
            r = QCDCountObject(0.0, 0.0, 0.0, 0.0)
            if denominator[i].value() > 0:
                r = numerator[i].copy()
                r.divide(denominator[i])
                #print "1D eff: nom=%f, denom=%f, value=%f +- %f:"%(numeratorCount.value(),denominatorCount.value(),myValue,myError)
            myResult.append(r)
        return myResult

    ## CLP cannot be applied straight away to case like (A1-B1) / (A2-B2)
    #def _getEfficiencyCLP(self,numerator,denominator,factorisationBinIndexList):
        #numeratorCount = numerator.getQCDCount(factorisationBinIndexList)
        #denominatorCount = denominator.getQCDCount(factorisationBinIndexList)
        #myResult = CountAsymmetric(0.0, 0.0, 0.0)
        #if denominatorCount.value() > 0:
            #myResult = dataset.divideBinomial(numeratorCount.getCountObject(), denominatorCount.getCountObject())
            ##print "1D eff: nom=%f, denom=%f, value=%f +- %f:"%(numeratorCount.value(),denominatorCount.value(),myValue,myError)
        #return myResult

    def getContracted1DLeg1Efficiency(self,factorisationBinIndex,axisIndexToKeep):
        return self._getContracted1DEfficiency(self._leg1Counts,self._basicCount,factorisationBinIndex,axisIndexToKeep)

    def getContracted1DLeg2Efficiency(self,factorisationBinIndex,axisIndexToKeep):
        return self._getContracted1DEfficiency(self._leg2Counts,self._basicCount,factorisationBinIndex,axisIndexToKeep)

    ## Returns the efficiency for a bin on first variation parameter, other parameters are contracted (i.e. summed)
    def _getContracted1DEfficiency(self,numerator,denominator,factorisationBinIndex,axisIndexToKeep):
        numeratorCounts = numerator.getContracted1DQCDCount(factorisationBinIndex,axisIndexToKeep)
        denominatorCounts = denominator.getContracted1DQCDCount(factorisationBinIndex,axisIndexToKeep)
        return self._calculateEfficiency(numeratorCounts,denominatorCounts)

    def getLeg1EfficiencyHistograms(self):
        return self._createEfficiencyHistograms(self._leg1Counts, self._basicCount, "leg1")

    def getLeg2EfficiencyHistograms(self):
        return self._createEfficiencyHistograms(self._leg2Counts, self._basicCount, "leg2")

    def _createEfficiencyHistograms(self, numerator, denominator, suffix=""):
        hlist = []
        # Make uncontracted histograms (can be a loooot of bins)
        (hStat,hFull) = self._basicCount._createEmptyHistograms("Efficiency","Efficiency")
        for i in range(0,self._basicCount.getNFactorisationBins()):
            # Obtain values and fill histograms
            myResults = self._getEfficiencyByUnfoldedBin(numerator, denominator, i)
            self._basicCount._fillHistogramValues(hStat,hFull,myResults,i)
        hlist.append(hStat)
        hlist.append(hFull)
        # Make contracted histograms (easier to read)
        myBinDimensions = self.getReaderObject().getNbinsList()
        for myDim in range(0, len(myBinDimensions)):
            (hCStat,hCFull) = self._basicCount._createEmptyHistograms("Efficiency","Efficiency",contractionDim=myDim)
            for i in range(0, myBinDimensions[myDim]):
                # Obtain values and fill histograms
                myResult = self._getContracted1DEfficiency(numerator, denominator, i, myDim)
                self._basicCount._fillHistogramValues(hStat,hFull,myResults,i)
            hlist.append(hCStat)
            hlist.append(hCFull)
        for h in hlist:
            ROOT.SetOwnership(h, True)
        return hlist

    def getNQCD(self,factorisationBinIndexList):
        myBasicCountObjects = self._basicCount.getQCDCount(factorisationBinIndexList)
        myLeg1CountObjects = self._leg1Counts.getQCDCount(factorisationBinIndexList)
        myLeg2CountObjects = self._leg2Counts.getQCDCount(factorisationBinIndexList)
        return self._calculateNQCD(myBasicCountObjects, myLeg1CountObjects, myLeg2CountObjects)

    def getNQCDByUnfoldedBin(self,unfoldedBinIndex):
        myBasicCountObjects = self._basicCount.getQCDCountByUnfoldedBin(unfoldedBinIndex)
        myLeg1CountObjects = self._leg1Counts.getQCDCountByUnfoldedBin(unfoldedBinIndex)
        myLeg2CountObjects = self._leg2Counts.getQCDCountByUnfoldedBin(unfoldedBinIndex)
        return self._calculateNQCD(myBasicCountObjects, myLeg1CountObjects, myLeg2CountObjects)

    def getContracted1DNQCDForBin(self,factorisationBinIndex, axisIndexToKeep):
        myBasicCountObjects = self._basicCount.getContracted1DQCDCount(factorisationBinIndex, axisIndexToKeep)
        myLeg1CountObjects = self._leg1Counts.getContracted1DQCDCount(factorisationBinIndex, axisIndexToKeep)
        myLeg2CountObjects = self._leg2Counts.getContracted1DQCDCount(factorisationBinIndex, axisIndexToKeep)
        return self._calculateNQCD(myBasicCountObjects, myLeg1CountObjects, myLeg2CountObjects)

    def _calculateNQCD(self, myBasicCountObjects, myLeg1CountObjects, myLeg2CountObjects):
        myResult = QCDCountObject(0.0, 0.0, 0.0, 0.0)
        # Check if NQCD is being calculated on a shape
        if len(myBasicCountObjects) != 1:
            raise Exception(ErrorLabel()+"NQCD calculation is supposed to take place with event count histograms, not shape histograms!")
        # Protect calculation against div by zero
        if (myBasicCountObjects[0].value() > 0.0):
            # Calculate uncertainty as f=a*b  (i.e. ignore basic counts uncertainty since it is the denominator to avoid double counting of uncertainties)
            # Note that this is more conservative than CLP
            myResult = myLeg1CountObjects[0].copy()
            myResult.multiply(myLeg2CountObjects[0])
            myResult.divideByScalar(myBasicCountObjects[0].value())
            # df = sqrt((b*da)^2 + (a*db)^2)
            #myDataUncert   = sqrt(pow(myLeg2Counts*self._leg1Counts.getDataError(idx,idy,idz)  /myBasicCounts,2) + 
                                  #pow(myLeg1Counts*self._leg2Counts.getDataError(idx,idy,idz)  /myBasicCounts,2))
            #myMCStatUncert = sqrt(pow(myLeg2Counts*self._leg1Counts.getMCStatError(idx,idy,idz)/myBasicCounts,2) +
                                  #pow(myLeg1Counts*self._leg2Counts.getMCStatError(idx,idy,idz)/myBasicCounts,2))
            #myLeg1Systematics = self._leg1Counts.getMCCountByUnfoldedBin(unfoldedBinIndex).value() * self.getEWKMCRelativeSystematicUncertainty(idx)
            #myLeg2Systematics = self._leg2Counts.getMCCountByUnfoldedBin(unfoldedBinIndex).value() * self.getEWKMCRelativeSystematicUncertainty(idx)
            #myMCSystUncert = sqrt(pow(myLeg2Counts*myLeg1Systematics/myBasicCounts,2) +
                                  #pow(myLeg1Counts*myLeg2Systematics/myBasicCounts,2))
        return myResult

    def _count(self):
        hlist = []
        myQCDResult = QCDCountObject(0.0, 0.0, 0.0, 0.0)
        # Make uncontracted histograms (can be a loooot of bins)
        myName = "NQCD_StatOnly"
        myNbins = self.getReaderObject().getUnfoldedBinCount()
        hStat = ROOT.TH1F(myName,myName,myNbins,0.0,myNbins)
        hStat.SetYTitle("NQCD")
        #hStat.SetMaximum(1.0)
        myName = "NQCD_StatAndSyst"
        hFull = ROOT.TH1F(myName,myName,myNbins,0.0,myNbins)
        hFull.SetYTitle("NQCD")
        #hFull.SetMaximum(1.0)
        for i in range(0,myNbins):
            myResult = self.getNQCDByUnfoldedBin(i)
            myQCDResult.add(myResult)
            hStat.SetBinContent(i+1, myResult.value())
            hStat.SetBinError(i+1, myResult.uncertainty())
            hFull.SetBinContent(i+1, myResult.value())
            hFull.SetBinError(i+1, myResult.totalUncertainty())
            hStat.GetXaxis().SetBinLabel(i+1,self._basicCount.getFactorisationBinLabel(i))
            hFull.GetXaxis().SetBinLabel(i+1,self._basicCount.getFactorisationBinLabel(i))
        self._nQCDHistograms.append(hStat)
        self._nQCDHistograms.append(hFull)
        # Save result
        self._result = QCDResultObject("full factorisation")
        self._result.setNQCDResult(myQCDResult)
        (minPurity, avgPurity) = self._basicCount.getPurityInfo()
        self._result.setPurityInfo(minPurity, avgPurity, 0)
        (minPurity, avgPurity) = self._leg1Counts.getPurityInfo()
        self._result.setPurityInfo(minPurity, avgPurity, 1)
        (minPurity, avgPurity) = self._leg2Counts.getPurityInfo()
        self._result.setPurityInfo(minPurity, avgPurity, 2)
        # Make contracted histograms (easier to read)
        myBinDimensions = self.getReaderObject().getNbinsList()
        for myDim in range(0, len(myBinDimensions)):
            myContractedResult = (QCDCountObject(0.0, 0.0, 0.0, 0.0))
            myName = "NQCD_%s_StatOnly"%(self.getReaderObject().getBinLabelList()[myDim].replace(" ","_"))
            hCStat = ROOT.TH1F(myName,myName,myBinDimensions[myDim],0.0,myBinDimensions[myDim])
            hCStat.SetXTitle(self.getReaderObject().getFactorisationCaptions()[myDim])
            hCStat.SetYTitle("dN_{QCD}/d%s"%self.getReaderObject().getFactorisationCaptions()[myDim])
            #hCStat.SetMaximum(1.0)
            myName = "NQCD_%s_StatAndSyst"%(self.getReaderObject().getBinLabelList()[myDim].replace(" ","_"))
            hCFull = ROOT.TH1F(myName,myName,myBinDimensions[myDim],0.0,myBinDimensions[myDim])
            hCFull.SetXTitle(self.getReaderObject().getFactorisationCaptions()[myDim])
            hCFull.SetYTitle("dN_{QCD}/d%s"%self.getReaderObject().getFactorisationCaptions()[myDim])
            #hCFull.SetMaximum(1.0)
            for i in range(0, myBinDimensions[myDim]):
                myResult = self.getContracted1DNQCDForBin(i, myDim)
                myWidthString = self.getReaderObject().getFactorisationRanges()[myDim][i].split("..")
                myBinWidth = 1
                if len(myWidthString) == 2:
                    myBinWidth = float(myWidthString[1]) - float(myWidthString[0])
                myContractedResult.add(myResult)
                hCStat.SetBinContent(i+1, myResult.value() / myBinWidth)
                hCStat.SetBinError(i+1, myResult.uncertainty() / myBinWidth)
                hCFull.SetBinContent(i+1, myResult.value() / myBinWidth)
                hCFull.SetBinError(i+1, myResult.totalUncertainty() / myBinWidth)
                hCStat.GetXaxis().SetBinLabel(i+1,self.getReaderObject().getFactorisationRanges()[myDim][i])
                hCFull.GetXaxis().SetBinLabel(i+1,self.getReaderObject().getFactorisationRanges()[myDim][i])
            self._nQCDHistograms.append(hCStat)
            self._nQCDHistograms.append(hCFull)
            # Save result
            self._contractedResults.append(None)
            self._contractedResults[myDim] = QCDResultObject("contracted to %s axis"%self.getReaderObject().getBinLabelList()[myDim])
            self._contractedResults[myDim].setNQCDResult(myContractedResult)
            (minPurity, avgPurity) = self._basicCount.getContracted1DPurityInfo(0)
            self._contractedResults[myDim].setPurityInfo(minPurity, avgPurity, 0)
            (minPurity, avgPurity) = self._leg1Counts.getContracted1DPurityInfo(1)
            self._contractedResults[myDim].setPurityInfo(minPurity, avgPurity, 1)
            (minPurity, avgPurity) = self._leg2Counts.getContracted1DPurityInfo(2)
            self._contractedResults[myDim].setPurityInfo(minPurity, avgPurity, 2)

        for h in self._nQCDHistograms:
            ROOT.SetOwnership(h, True)

    ## Create a full size table assuming 3D factorisation
    def _createYieldTable(self):
        myBinDimensions = self.getReaderObject().getNbinsList()
        myBinCaptions = self.getReaderObject().getFactorisationRanges()
        for i in range(0,len(myBinCaptions)):
            for j in range(0,len(myBinCaptions[i])):
                myBinCaptions[i][j] = myBinCaptions[i][j].replace("<","$<$").replace(">","$>$")
        #myBinCaptions = self.getReaderObject().getFactorisationFullBinLabels()
        ## Latexify bin captions
        #for i in range(0,len(myBinCaptions)):
            #for j in range(0,len(myBinCaptions[i])):
                ## replace root style greek letters by latex style
                #myStatus = True
                #pos = 0
                #while myStatus:
                    #a = myBinCaptions[i][j].find("#",pos)
                    #if a < 0:
                        #myStatus = False
                    #else:
                        ## found
                        #b = myBinCaptions[i][j].find(" ",a)
                        #myWord = myBinCaptions[i][j][a:b]
                        #myBinCaptions[i][j] = myBinCaptions[i][j].replace(myWord,"$\\%s$"%myWord.replace("#",""))
                        #pos = b
                ## replace root style subscript by latex style
                #myStatus = True
                #pos = 0
                #while myStatus:
                    #a = myBinCaptions[i][j].find("_",pos)
                    #if a < 0:
                        #myStatus = False
                    #else:
                        ## found
                        #b = myBinCaptions[i][j].find("}",a)
                        #myWord = myBinCaptions[i][j][a:b+1]
                        #myBinCaptions[i][j] = myBinCaptions[i][j].replace(myWord,"$%s$"%myWord)
                        #pos = b
                #myBinCaptions[i][j] = myBinCaptions[i][j].replace("<","$<$").replace(">","$>$")
        if len(myBinDimensions) != 3:
            return ""
        myOutput = ""
        # 3D table
        for i in range(0,myBinDimensions[0]):
            for k in range(0,myBinDimensions[2]):
                myTableStructure = "l"
                myBasicDataRow = "$N^{\\text{data}}_{\\text{basic sel.},ijk}$ "
                myBasicEWKRow = "$N^{\\text{EWK MC}}_{\\text{basic sel.},ijk}$ "
                myBasicPurityRow = "Purity after basic sel. "
                myMetDataRow = "$N^{\\text{data}}_{\\text{\\MET+btag+}\\Delta\\phi,ijk}$ "
                myMetEWKRow = "$N^{\\text{EWK MC}}_{\\text{\\MET+btag}+\\Delta\\phi,ijk}$ "
                myMetPurityRow = "Purity after \\MET+btag+$\\Delta\\phi$ "
                myTauDataRow = "$N^{\\text{data}}_{\\text{presel.},ijk}$ "
                myTauEWKRow = "$N^{\\text{EWK MC}}_{\\text{presel.},ijk}$ "
                myTauPurityRow = "Purity after presel. "
                myMetEffRow = "$\\varepsilon_{\\text{\\MET+btag+}\\Delta\\phi,ijk}$"
                myNQCDRow = "$N^{\\text{QCD}}_{ijk}$"
                myPtCaption = "$\\tau$-jet candidate \\pT bin"
                myEtaCaption = "$\\tau$-jet candidate $\\eta$ bin"
                myPtCaption += "& \\multicolumn{3}{c}{%s \\GeVc}"%myBinCaptions[0][i]
                for j in range(0,myBinDimensions[1]):
                    myTableStructure += "l"
                    myEtaCaption += "& \multicolumn{1}{c}{%s}"%myBinCaptions[1][j]
                    myBasicDataRow += "& %s"%(self._basicCount.getDataCountObjects([i,j,k])[0].getLatexStringNoSyst("%.1f"))
                    myBasicEWKRow += "& %s"%(self._basicCount.getMCCountObjects([i,j,k])[0].getLatexStringFull("%.1f"))
                    myBasicPurityRow += "& %s"%(self._basicCount.getPurity([i,j,k])[0].getLatexStringFull("%.3f"))
                    myMetDataRow += "& %s"%(self._leg1Counts.getDataCountObjects([i,j,k])[0].getLatexStringNoSyst("%.1f"))
                    myMetEWKRow += "& %s"%(self._leg1Counts.getMCCountObjects([i,j,k])[0].getLatexStringFull("%.1f"))
                    myMetPurityRow += "& %s"%(self._leg1Counts.getPurity([i,j,k])[0].getLatexStringFull("%.2f"))
                    myTauDataRow += "& %s"%(self._leg2Counts.getDataCountObjects([i,j,k])[0].getLatexStringNoSyst("%.1f"))
                    myTauEWKRow += "& %s"%(self._leg2Counts.getMCCountObjects([i,j,k])[0].getLatexStringFull("%.1f"))
                    myTauPurityRow += "& %s"%(self._leg2Counts.getPurity([i,j,k])[0].getLatexStringFull("%.2f"))
                    myMetEffRow += "& %s"%(self.getLeg1Efficiency([i,j,k])[0].getLatexStringFull("%.4f"))
                    myNQCDRow += "& %s"%(self.getNQCD([i,j,k]).getLatexStringFull("%.1f"))
                # Construct table
                if k % 2 == 1: # FIXME assumed 2 bins for eta
                    myOutput += "\\renewcommand{\\arraystretch}{1.2}\n"
                    myOutput += "\\begin{table}[ht!]\n"
                    myOutput += "\\caption{Analytical breakdown of the \\NQcd estimate, showing the number of data and EWK MC events and\n"
                    myOutput += "  the purity of the sample after standard selections, after basic selections plus \\MET+btag+$\\Delta\\phi$, and\n"
                    myOutput += "  after all preselections. The efficiency of \\MET+btag+$\\Delta\\phi$ relative to basic selections and \n"
                    myOutput += "  the estimate for the number of QCD multi-jet events in the signal region (\\NQcd) are shown.\n"
                    myOutput += "  The numbers are shown for tau candidate \\pT bin %s \\GeVc.\n"%myBinCaptions[0][i]
                    myOutput += "  The top table is for $N_{\\text{vertices}} < 8$,\n" #FIXME assumed 2 bins for eta
                    myOutput += "  whereas the bottom table is for $N_{\\text{vertices}} \geq 8$.\n"
                    myOutput += "  Wherever appropriate, the systematic uncertainty is shown in addition to the statistical uncertainty. } \n"
                    myOutput += "\\label{tab:background:qcdfact:evtyield:bin%d}\n"%(i)
                    myOutput += "\\vspace{1cm}\n"
                    myOutput += "%% NQCD analytical breakdown for tau pT bin %s and Nvtx bin %s\n"%(myBinCaptions[0][i],myBinCaptions[2][k])
                else:
                    myOutput += "\\\\ \n"
                    myOutput += "\\\\ \n"
                myOutput += "\\begin{tabular}{%s}\n"%myTableStructure
                myOutput += "\\hline\n"
                myOutput += "%s \\\\ \n"%myPtCaption
                myOutput += "%s \\\\ \n"%myEtaCaption
                myOutput += "\\hline\n"
                myOutput += "%s \\\\ \n"%myBasicDataRow
                myOutput += "%s \\\\ \n"%myBasicEWKRow
                myOutput += "%s \\\\ \n"%myBasicPurityRow
                myOutput += "\\hline\n"
                myOutput += "%s \\\\ \n"%myMetDataRow
                myOutput += "%s \\\\ \n"%myMetEWKRow
                myOutput += "%s \\\\ \n"%myMetPurityRow
                myOutput += "\\hline\n"
                myOutput += "%s \\\\ \n"%myTauDataRow
                myOutput += "%s \\\\ \n"%myTauEWKRow
                myOutput += "%s \\\\ \n"%myTauPurityRow
                myOutput += "\\hline\n"
                myOutput += "%s \\\\ \n"%myMetEffRow
                myOutput += "%s \\\\ \n"%myNQCDRow
                myOutput += "\\hline\n"
                myOutput += "\\end{tabular}\n"
                if k % 2 == 0: # FIXME assumed 2 bins for eta
                    myOutput += "\\end{table}\n"
                    myOutput += "\\renewcommand{\\arraystretch}{1.0}\n"
                    myOutput += "\\newpage\n\n"
        return myOutput

    def _createCompactYieldTable(self):
        def _convertRangeToStr(ranges):
            if len(ranges) == 1:
                return ranges[0]
            if len(ranges) == 2:
                return "%s and %s"%(ranges[0],ranges[1])
            s = ""
            for i in range(0,len(ranges)-1):
                s += "%s, "%ranges[i]
            s += "and %s"%ranges[len(ranges)-1]
            return s

        myBinDimensions = self.getReaderObject().getNbinsList()
        myBinCaptions = self.getReaderObject().getFactorisationRanges()
        for i in range(0,len(myBinCaptions)):
            for j in range(0,len(myBinCaptions[i])):
                myBinCaptions[i][j] = myBinCaptions[i][j].replace("<","$<$").replace(">","$>$")
        myTableStructure = ""
        myRanges = []
        myOutput = ""
        n = 0
        rows = 4
        for i in range(0,myBinDimensions[0]):
            if n == 0:
                myRanges = []
                myTableStructure = "l"
                myBasicDataRow = "$N^{\\text{data}}_{\\text{basic sel.},i}$ "
                myBasicEWKRow = "$N^{\\text{EWK MC}}_{\\text{basic sel.},i}$ "
                myBasicPurityRow = "Purity after basic sel. "
                myMetDataRow = "$N^{\\text{data}}_{\\text{\\MET+btag+}\\Delta\\phi,i}$ "
                myMetEWKRow = "$N^{\\text{EWK MC}}_{\\text{\\MET+btag}+\\Delta\\phi,i}$ "
                myMetPurityRow = "Purity after \\MET+btag+$\\Delta\\phi$ "
                myTauDataRow = "$N^{\\text{data}}_{\\text{presel.},i}$ "
                myTauEWKRow = "$N^{\\text{EWK MC}}_{\\text{presel.},i}$ "
                myTauPurityRow = "Purity after presel. "
                myMetEffRow = "$\\varepsilon_{\\text{\\MET+btag+}\\Delta\\phi,i}$"
                myNQCDRow = "$N^{\\text{QCD}}_{i}$"
                myPtCaption = "$\\tau$-jet candidate \\pT bin"
            myRanges.append(myBinCaptions[0][i])
            myPtCaption += "& %s \\GeVc"%(myBinCaptions[0][i])
            myTableStructure += "l"
            myBasicDataRow += "& %s"%(self._basicCount.getContracted1DDataCountObjects(i,0)[0].getLatexStringNoSyst("%.1f"))
            myBasicEWKRow += "& %s"%(self._basicCount.getContracted1DMCCountObjects(i,0)[0].getLatexStringFull("%.1f"))
            myBasicPurityRow += "& %s"%(self._basicCount.getContracted1DPurity(i,0)[0].getLatexStringFull("%.3f"))
            myMetDataRow += "& %s"%(self._leg1Counts.getContracted1DDataCountObjects(i,0)[0].getLatexStringNoSyst("%.1f"))
            myMetEWKRow += "& %s"%(self._leg1Counts.getContracted1DMCCountObjects(i,0)[0].getLatexStringFull("%.1f"))
            myMetPurityRow += "& %s"%(self._leg1Counts.getContracted1DPurity(i,0)[0].getLatexStringFull("%.2f"))
            myTauDataRow += "& %s"%(self._leg2Counts.getContracted1DDataCountObjects(i,0)[0].getLatexStringNoSyst("%.1f"))
            myTauEWKRow += "& %s"%(self._leg2Counts.getContracted1DMCCountObjects(i,0)[0].getLatexStringFull("%.1f"))
            myTauPurityRow += "& %s"%(self._leg2Counts.getContracted1DPurity(i,0)[0].getLatexStringFull("%.2f"))
            myMetEffRow += "& %s"%(self.getContracted1DLeg1Efficiency(i,0)[0].getLatexStringFull("%.4f"))
            myNQCDRow += "& %s"%(self.getContracted1DNQCDForBin(i,0).getLatexStringFull("%.1f"))
            # Construct table
            if n == rows-1 or i == myBinDimensions[0]-1:
                myOutput += "\\renewcommand{\\arraystretch}{1.2}\n"
                myOutput += "\\begin{table}[ht!]\n"
                myOutput += "\\caption{Analytical breakdown of the \\NQcd estimate for tau candidate \\pT ranges %s \\GeVc, showing the number of data and EWK MC events and\n"%_convertRangeToStr(myRanges)
                myOutput += "  the purity of the sample after standard selections, after basic selections plus \\MET+btag+$\\Delta\\phi$, and\n"
                myOutput += "  after all preselections. The efficiency of \\MET+btag+$\\Delta\\phi$ relative to basic selections and \n"
                myOutput += "  the estimate for the number of QCD multi-jet events in the signal region (\\NQcd) are shown.\n"
                myOutput += "  The bins of tau candidate $\\eta$ and $N_{\\text{vertices}}$ have been summed up.\n"
                myOutput += "  Wherever appropriate, the systematic uncertainty is shown in addition to the statistical uncertainty. } \n"
                myOutput += "\\label{tab:background:qcdfact:evtyield:tauptonly%d}\n"%((i-1)/rows+1)
                myOutput += "\\vspace{1cm}\n"
                myOutput += "\\begin{tabular}{%s}\n"%myTableStructure
                myOutput += "\\hline\n"
                myOutput += "%s \\\\ \n"%myPtCaption
                myOutput += "\\hline\n"
                myOutput += "%s \\\\ \n"%myBasicDataRow
                myOutput += "%s \\\\ \n"%myBasicEWKRow
                myOutput += "%s \\\\ \n"%myBasicPurityRow
                myOutput += "\\hline\n"
                myOutput += "%s \\\\ \n"%myMetDataRow
                myOutput += "%s \\\\ \n"%myMetEWKRow
                myOutput += "%s \\\\ \n"%myMetPurityRow
                myOutput += "\\hline\n"
                myOutput += "%s \\\\ \n"%myTauDataRow
                myOutput += "%s \\\\ \n"%myTauEWKRow
                myOutput += "%s \\\\ \n"%myTauPurityRow
                myOutput += "\\hline\n"
                myOutput += "%s \\\\ \n"%myMetEffRow
                myOutput += "%s \\\\ \n"%myNQCDRow
                myOutput += "\\hline\n"
                myOutput += "\\end{tabular}\n"
                #if i % 4 != 0:
                    #myOutput += "\\\\ \n"
                    #myOutput += "\\\\ \n"
            if n == rows-1 or i == myBinDimensions[0]-1:
                myOutput += "\\end{table}\n"
                myOutput += "\\renewcommand{\\arraystretch}{1.0}\n"
                myOutput += "\\newpage\n\n"
                n = 0
            else:
                n += 1
        return myOutput

## class QCDfactorisedColumn
# Inherits from DatacardColumn and extends its functionality to calculate the QCD measurement and its result in one go
# Note that only method one needs to add is 'doDataMining'; other methods are private
class QCDfactorisedColumn(DatacardColumn):
    ## Constructor
    def __init__(self,
                 landsProcess = -999,
                 enabledForMassPoints = [],
                 nuisanceIds = [],
                 datasetMgrColumn = "",
                 datasetMgrColumnForQCDMCEWK = "",
                 additionalNormalisationFactor = 1.0,
                 QCDfactorisedInfo = None,
                 debugMode = False):
        DatacardColumn.__init__(self,
                                label = "QCDfact",
                                landsProcess = landsProcess,
                                enabledForMassPoints = enabledForMassPoints,
                                datasetType = "QCD factorised",
                                nuisanceIds = nuisanceIds,
                                datasetMgrColumn = datasetMgrColumn,
                                datasetMgrColumnForQCDMCEWK = datasetMgrColumnForQCDMCEWK,
                                additionalNormalisationFactor = additionalNormalisationFactor)
        # Store info dictionary for QCD factorised
        self._factorisedConfig = QCDfactorisedInfo
        # Other initialisation
        self._infoHistograms = []
        self._debugMode = debugMode
        self._messages = []
        self._yieldTable = ""
        self._compactYieldTable = ""
        self._METCorrectionFactorsForTauPtBins = []
        self._METCorrectionFactorUncertaintyForTauPtBins = []
        self._MTCorrectionFactorsForTauPtBins = []
        self._MTCorrectionFactorUncertaintyForTauPtBins = []


    ## Returns list of messages
    def getMessages(self):
        return self._messages

    def getYieldTable(self):
        return self._yieldTable

    def getCompactYieldTable(self):
        return self._compactYieldTable

    ## Do data mining and cache results
    def doDataMining(self, config, dsetMgr, luminosity, mainCounterTable, extractors, controlPlotExtractors):
        print "... processing column: "+HighlightStyle()+self._label+NormalStyle()
        if dsetMgr == None:
            raise Exception(ErrorLabel()+"You called data mining for QCD factorised, but it's multicrab directory is not there. Such undertaking is currently not supported.")
        print "... Calculating NQCD value ..."
        # Calculate correction for MET shape
        #self._calculateMETCorrectionFactors(dsetMgr, luminosity)
        # Make event count objects
        myStdSelEventCount = self._getQCDEventCount(dsetMgr=dsetMgr, histoName=self._factorisedConfig["afterStdSelSource"], luminosity=luminosity)
        myMETLegEventCount = self._getQCDEventCount(dsetMgr=dsetMgr, histoName=self._factorisedConfig["afterMETLegSource"], luminosity=luminosity)
        myTauLegEventCount = self._getQCDEventCount(dsetMgr=dsetMgr, histoName=self._factorisedConfig["afterTauLegSource"], luminosity=luminosity)
        # Print factorisation definitions
        myStdSelEventCount.printFactorisationInfo()
        # Make control plot for NQCD event counts
        self._infoHistograms.extend(myStdSelEventCount.makeEventCountHistograms())
        self._infoHistograms.extend(myMETLegEventCount.makeEventCountHistograms())
        self._infoHistograms.extend(myTauLegEventCount.makeEventCountHistograms())
        # Make control plot for negative NQCD entries
        self._infoHistograms.extend(myStdSelEventCount.makeNegativeEventCountHistograms())
        self._infoHistograms.extend(myMETLegEventCount.makeNegativeEventCountHistograms())
        self._infoHistograms.extend(myTauLegEventCount.makeNegativeEventCountHistograms())
        # Make purity histograms
        self._infoHistograms.extend(myStdSelEventCount.makePurityHistograms())
        self._infoHistograms.extend(myMETLegEventCount.makePurityHistograms())
        self._infoHistograms.extend(myTauLegEventCount.makePurityHistograms())
        self.saveQCDInfoHistograms(".") # FIXME temp
        # Calculate result of NQCD
        myQCDCalculator = QCDfactorisedCalculator(myStdSelEventCount, myMETLegEventCount, myTauLegEventCount, True)
        self._infoHistograms.extend(myQCDCalculator.getNQCDHistograms())
        self._yieldTable = myQCDCalculator.getYieldTable()
        self._compactYieldTable = myQCDCalculator.getCompactYieldTable()
        self._infoHistograms.extend(myQCDCalculator.getNQCDHistograms())
        # Make efficiency histograms
        self._infoHistograms.extend(myQCDCalculator.getLeg1EfficiencyHistograms())
        self._infoHistograms.extend(myQCDCalculator.getLeg2EfficiencyHistograms())
        
        # Print result to screen
        print myQCDCalculator.getResult().getInfoString()
        for cr in myQCDCalculator.getContractedResultsList():
            print cr.getInfoString()
        # Make shape histogram
        myRateHistograms=[]
        if True:
            print "... Calculating shape histograms"
            myRateHistograms=[]
            hRateShape = self._createShapeHistogram(dsetMgr,luminosity,myQCDCalculator,
                                                    histoSpecs=config.ShapeHistogramsDimensions,title=self._label,
                                                    histoName=self._factorisedConfig["finalShapeHisto"],
                                                    saveDetailedInfo=True,makeCorrectionToShape=True)
            # Normalise rate shape to NQCD
            if hRateShape.Integral() > 0:
                hRateShape.Scale(myQCDCalculator.getNQCD() / hRateShape.Integral())
            myRateHistograms.append(hRateShape)
            # Obtain messages
            self._messages.extend(myStdSelEventCount.getMessages())
            self._messages.extend(myMETLegEventCount.getMessages())
            self._messages.extend(myTauLegEventCount.getMessages())
        # Cache result for rate
        self._rateResult = ExtractorResult("rate",
                                           "rate",
                                           myQCDCalculator.getResult().getNQCDResult(),
                                           myRateHistograms)
        return
        # Make closure test histograms
        print "... Producing validation histograms ..."
        for METshape in self._validationMETShapeSource:
            self._createValidationHistograms(dsetMgr,luminosity,myQCDCalculator,self._validationMETShapeDetails,
                                             "METvalidation", METshape)
        for mTshape in self._validationMtShapeSource:
            self._createValidationHistograms(dsetMgr,luminosity,myQCDCalculator,self._validationMtShapeDetails,
                                             "mTvalidation", mTshape)
        # Construct results for nuisances
        print "... Constructing result ..."
        for nid in self._nuisanceIds:
            #sys.stdout.write("\r... data mining in progress: Column="+self._label+", obtaining Nuisance="+nid+"...                                              ")
            #sys.stdout.flush()
            myFoundStatus = False
            for e in extractors:
                if e.getId() == nid:
                    myFoundStatus = True
                    myResult = 0.0
                    # Obtain result
                    if e.getQCDmode() == "statistics":
                        myResult = myQCDCalculator.getStatUncertainty()
                    elif e.getQCDmode() == "systematics":
                        myResult = myQCDCalculator.getSystUncertainty()
                    # Obtain histograms
                    myHistograms = []
                    if e.getQCDmode() == "shapestat":
                        # Clone rate histogram as up and down histograms
                        myHistograms.append(myRateHistograms[0].Clone(self._label+"_%dDown"%int(e.getMasterId())))
                        myHistograms[0].SetTitle(self._label+"_%dDown"%int(e.getMasterId()))
                        myHistograms.append(myRateHistograms[0].Clone(self._label+"_%dUp"%int(e.getMasterId())))
                        myHistograms[1].SetTitle(self._label+"_%dUp"%int(e.getMasterId()))
                        # Substract/Add one sigma to get Down/Up variation
                        for k in range(1, myHistograms[0].GetNbinsX()+1):
                            myHistograms[0].SetBinContent(k, myHistograms[0].GetBinContent(k) - myHistograms[0].GetBinError(k))
                            myHistograms[1].SetBinContent(k, myHistograms[1].GetBinContent(k) + myHistograms[1].GetBinError(k))
                            if myHistograms[0].GetBinContent(k) < 0:
                                print WarningStyle()+"Warning: shapeStat Nuisance with id='"+e.getId()+"' for column '"+self._label+"':"+NormalStyle()+" shapeDown histo bin %d is negative (%f), it is forced to zero"%(k,myHistograms[0].GetBinContent(k))
                                myHistograms[0].SetBinContent(k, 0.0)
                            if myHistograms[1].GetBinContent(k) < 0:
                                print WarningStyle()+"Warning: shapeStat Nuisance with id='"+e.getId()+"' for column '"+self._label+"':"+NormalStyle()+" shapeUp histo bin %d is negative (%f), it is forced to zero"%(k,myHistograms[0].GetBinContent(k))
                                myHistograms[1].SetBinContent(k, 0.0)
                    # Cache result
                    self._nuisanceResults.append(ExtractorResult(e.getId(),
                                                                 e.getMasterId(),
                                                                 myResult,
                                                                 myHistograms,
                                                                 e.getQCDmode() == "statistics" or e.getQCDmode() == "shapestat"))
            if not myFoundStatus:
                raise Exception("\n"+ErrorStyle()+"Error (data group ='"+self._label+"'):"+NormalStyle()+" Cannot find nuisance with id '"+nid+"'!")
        # Obtain results for control plots
        if config.OptionDoControlPlots != None:
            if config.OptionDoControlPlots:
                print "... Obtaining control plots ..."
                if config.ControlPlots != None and dsetMgr != None:
                    for c in config.ControlPlots:
                        hShape = self._createShapeHistogram(config, luminosity, dsetMgr, myQCDCalculator,
                                                            c.details, c.title, c.QCDFactHistoName)
                        # Normalise
                        myEventCount = self._getQCDEventCount(dsetMgr=dsetMgr, histoName=c.QCDFactNormalisation, luminosity=luminosity)
                        myQCDCalculator = QCDfactorisedCalculator(myStdSelEventCount, myEventCount, myTauLegEventCount)
                        hShape.Scale(myQCDCalculator.getNQCD() / hShape.Integral())
                        print "     "+c.title+", NQCD=%f"%myQCDCalculator.getNQCD()
                        myEventCount.clean()
                        self._controlPlots.append(hShape)
        # Clean up
        myQCDCalculator.clean()

    def _getQCDEventCount(self, dsetMgr, histoName, luminosity):
        return QCDEventCount(histoName=histoName,
                             dsetMgr=dsetMgr,
                             dsetMgrDataColumn=self._datasetMgrColumn,
                             dsetMgrMCEWKColumn=self._datasetMgrColumnForQCDMCEWK,
                             luminosity=luminosity)

    def _calculateMETCorrectionFactors(self, dsetMgr, luminosity):
        myBinEdges = self._METCorrectionDetails[self._METCorrectionDetails["name"]+"_CorrectionBinLeftEdges"]
        myMETHistoSpecs = { "bins": len(myBinEdges),
                            "rangeMin": 0.0,
                            "rangeMax": 400.0,
                            "variableBinSizeLowEdges": myBinEdges,
                            "xtitle": "",
                            "ytitle": "" }
        myShapeModifier = ShapeHistoModifier(myMETHistoSpecs)
        h = myShapeModifier.createEmptyShapeHistogram("dummy")
        myBins = self._METCorrectionDetails["bins"]
        # Loop over bins
        #print "***"
        for i in range(0,myBins[0]):
            for j in range(0,myBins[1]):
                for k in range(0,myBins[2]):
                    # Get data and MC EWK histogram
                    myFullHistoName = "/%s_%d_%d_%d"%(self._METCorrectionDetails["source"],i,j,k)
                    hMtData = self._extractShapeHistogram(dsetMgr, self._datasetMgrColumn, myFullHistoName, luminosity)
                    hMtMCEWK = self._extractShapeHistogram(dsetMgr, self._datasetMgrColumnForQCDMCEWK, myFullHistoName, luminosity)
                    # Add to shape
                    h.Reset()
                    myShapeModifier.addShape(source=hMtData,dest=h)
                    myShapeModifier.subtractShape(source=hMtMCEWK,dest=h,purityCheck=False)
                    myShapeModifier.finaliseShape(dest=h)
                    # Calculate nominal integral and corrected integral
                    myNominalCount = h.Integral()
                    myCorrections = self._METCorrectionDetails[self._METCorrectionDetails["name"]+"_Correction_bin_%d"%(i)]
                    myCorrectionUncertainty = self._METCorrectionDetails[self._METCorrectionDetails["name"]+"_CorrectionUncertainty_bin_%d"%(i)]
                    myCorrectedCount = 0.0
                    myCorrectedUncertainty = 0.0
                    for l in range(1,h.GetNbinsX()+1):
                        #print "%f, %f"%( h.GetBinContent(l), myCorrections[l-1])
                        myCorrectedCount += h.GetBinContent(l)*myCorrections[l-1]
                        myCorrectedUncertainty += pow(h.GetBinContent(l)*myCorrectionUncertainty[l-1],2)
                    myCorrectedUncertainty = sqrt(myCorrectedUncertainty)
                    #print "*** MET correction %d: nominal = %f, corrected = %f +- %f"%(i,myNominalCount,myCorrectedCount,myCorrectedUncertainty)
                    self._METCorrectionFactorsForTauPtBins.append(myCorrectedCount)
                    self._METCorrectionFactorUncertaintyForTauPtBins.append(myCorrectedUncertainty)
                    hMtData.IsA().Destructor(hMtData)
                    hMtMCEWK.IsA().Destructor(hMtMCEWK)
        h.IsA().Destructor(h)

    def _createShapeHistogram(self, dsetMgr, luminosity, myQCDCalculator, histoSpecs, title, histoName, saveDetailedInfo=False, makeCorrectionToShape=False):
        # Create empty shape histogram
        myShapeModifier = ShapeHistoModifier(histoSpecs)
        h = myShapeModifier.createEmptyShapeHistogram(title)
        # Obtain bin dimensions
        myNUnfoldedFactorisationBins = self.getReaderObject().getUnfoldedBinCount()
        # Create info histogram with all info in one
        #myName = "QCDFact_ShapeSummary_%s_Total"%title
        #hTot = ROOT.TH2F(myName,myName,h.GetNbinsX()*QCDCount.getNbinsY(),0,h.GetNbinsX()*QCDCount.getNbinsY(),QCDCount.getNbinsX()*QCDCount.getNbinsZ(),0,QCDCount.getNbinsX()*QCDCount.getNbinsZ())
        #hTot.SetZTitle("Events")
        # Setup axis titles for total histogram
        #for i in range(1,h.GetNbinsX()+1):
            #for j in range(1,nbinsY+1):
                #if i == h.GetNbinsX()+1:
                    #hTot.GetXaxis().SetBinLabel(i+(j-1)*h.GetNbinsX(), "(>%d; "%(h.GetXaxis().GetBinUpEdge(i))+QCDCount.getBinLabel("Y",j))
                #else:
                    #hTot.GetXaxis().SetBinLabel(i+(j-1)*h.GetNbinsX(), "(%d-%d; "%(h.GetXaxis().GetBinLowEdge(i),h.GetXaxis().GetBinUpEdge(i))+QCDCount.getBinLabel("Y",j))
        #for i in range(1,QCDCount.getNbinsX()+1):
            #for k in range(1,nbinsZ+1):
                #hTot.GetYaxis().SetBinLabel(k+(i-1)*nbinsZ, "("+QCDCount.getBinLabel("X",i)+";"+QCDCount.getBinLabel("Z",k))
                
        # Get input shape histograms for data and for MC
        
        # Loop over factorisation bins
        for i in range(0,myNUnfoldedFactorisationBins):
            #myName = "QCDFact_ShapeSummary_%s_ContractedX_bin_%d"%(title,i)
            #hTotContractedX = myShapeModifier.createEmptyShapeHistogram(myName)
            #myName = "QCDFact_ShapeSummary_%s_ContractedXContractedEff_bin_%d"%(title,i)
            #hTotContractedXeff = myShapeModifier.createEmptyShapeHistogram(myName)
            # Get histograms for the bin for data and MC EWK
            myFullHistoName = "%s/%s%s"%(histoDir,histoName,myFactorisationSuffix)
            hMtData = self._extractShapeHistogram(dsetMgr, self._datasetMgrColumn, myFullHistoName, luminosity)
            hMtMCEWK = self._extractShapeHistogram(dsetMgr, self._datasetMgrColumnForQCDMCEWK, myFullHistoName, luminosity)
            # Add proper systematics to shape for MC EWK
            for l in range (0, hMtMCEWK.GetNbinsX()+2):
                myAbsSystUncertainty = QCDCalculator.getEWKMCRelativeSystematicUncertainty(i)* hMtMCEWK.GetBinContent(l)
                hMtMCEWK.SetBinError(l,sqrt(pow(hMtMCEWK.GetBinError(l),2) + pow(myAbsSystUncertainty,2)))
            if self._debugMode:
                print "  QCDfactorised / %s: bin%s, data=%f, MC EWK=%f, QCD=%f"%(title,myFactorisationSuffix,hMtData.Integral(0,hMtData.GetNbinsX()+1),hMtMCEWK.Integral(0,hMtMCEWK.GetNbinsX()+1),hMtData.Integral(0,hMtData.GetNbinsX()+1)-hMtMCEWK.Integral(0,hMtMCEWK.GetNbinsX()+1))
            # Obtain empty histograms
            myOutHistoName = "QCDFact_%s_QCD_bin%s"%(title,myFactorisationSuffix)
            hMtBin = myShapeModifier.createEmptyShapeHistogram(myOutHistoName)
            hMtBinData = None
            hMtBinEWK = None
            if saveDetailedInfo:
                myOutHistoName = "QCDFact_%s_Data_bin%s"%(title,myFactorisationSuffix)
                hMtBinData = myShapeModifier.createEmptyShapeHistogram(myOutHistoName)
                myOutHistoName = "QCDFact_%s_MCEWK_bin%s"%(title,myFactorisationSuffix)
                hMtBinEWK = myShapeModifier.createEmptyShapeHistogram(myOutHistoName)
            # Add data to histograms
            myShapeModifier.addShape(source=hMtData,dest=hMtBin)
            myShapeModifier.addShape(source=hMtData,dest=hMtBinData)
            myShapeModifier.addShape(source=hMtMCEWK,dest=hMtBinEWK)
            # Subtract MC EWK from data to obtain QCD
            myMessages = []
            myMessages.extend(myShapeModifier.subtractShape(source=hMtMCEWK,dest=hMtBin,purityCheck=True))
            if len(myMessages) > 0:
                myTotal = hMtBin.Integral(0,hMtBin.GetNbinsX()+1)
                for m in myMessages:
                    # Filter out only important warnings of inpurity (impact more than one percent to whole bin)
                    if myTotal > 0.0:
                        if m[1] / myTotal > 0.01:
                            self._messages.extend(WarningStyle()+"Warning:"+NormalStyle()+" low purity in QCD factorised shape for bin %d,%d,%d (impact %f events / total=%f : %s"%(i,j,k,m[1],myTotal,m[0]))
            # Finalise shape (underflow added to first bin, overflow added to last bin, variances converted to std.deviations)
            myShapeModifier.finaliseShape(dest=hMtBin)
            myShapeModifier.finaliseShape(dest=hMtBinData)
            myShapeModifier.finaliseShape(dest=hMtBinEWK)
            # Add to contracted histogram
            myShapeModifier.addShape(source=hMtBin,dest=hTotContractedXeff)
            # Multiply by efficiency of leg 2 (tau leg)
            myEfficiency = QCDCalculator.getLeg2Efficiency(i,j,k)
            if myEfficiency.value() > 0.0:
                myMCEWKLeg2Counts = QCDCalculator.getLeg2EWKMCCounts(i,j,k)
                myLeg2Stat = QCDCalculator.getLeg2StatUncertainty(i,j,k)
                myBasicCounts = QCDCalculator.getQCDBasicCounts(i,j,k).value()
                for l in range(1,hMtBin.GetNbinsX()+1):
                    # the mT bin already contains stat + syst
                    myStatUncertaintySquared = pow(myLeg2Stat,2)
                    mySystUncertaintySquared = pow(myMCEWKLeg2Counts*QCDCalculator.getEWKMCRelativeSystematicUncertainty(i),2)
                    hMtBin.SetBinError(l,sqrt(pow(hMtBin.GetBinError(l)*myEfficiency.value(),2)
                                             +pow(hMtBin.GetBinContent(l) / myBasicCounts,2)*(myStatUncertaintySquared+mySystUncertaintySquared)))
                    hMtBin.SetBinContent(l,hMtBin.GetBinContent(l)*myEfficiency.value())
                if saveDetailedInfo:
                    hMtBinData.Scale(myEfficiency.value()) #FIXME
                    hMtBinEWK.Scale(myEfficiency.value())
            else:
                # Do not take this bin into account if cannot obtain efficiency
                hMtBin.Reset()
            if self._debugMode:
                print "  QCDfactorised / %s shape: bin %d_%d_%d, eff=%f, eff*QCD=%f"%(title,i,j,k,myEfficiency.value(),hMtBin.Integral())
            # Apply correction to mT
####
            if makeCorrectionToShape and False:
                # Get data and MC EWK histogram
                myFullHistoName = "%s_%d_%d_%d"%(self._MTCorrectionDetails["source"],i,j,k)
                hCorrData = self._extractShapeHistogram(dsetMgr, self._datasetMgrColumn, myFullHistoName, luminosity)
                hCorrMCEWK = self._extractShapeHistogram(dsetMgr, self._datasetMgrColumnForQCDMCEWK, myFullHistoName, luminosity)
                # Add to shape
                hCorr = myShapeModifier.createEmptyShapeHistogram(title)
                myShapeModifier.addShape(source=hCorrData,dest=hCorr)
                myShapeModifier.subtractShape(source=hCorrMCEWK,dest=hCorr,purityCheck=False)
                myShapeModifier.finaliseShape(dest=Corr)
                # Calculate nominal integral and corrected integral
                myNominalCount = h.Integral()
                myCorrections = self._MTCorrectionDetails[self._MTCorrectionDetails["name"]+"_Correction_bin_%d"%(i)]
                myCorrectionUncertainty = self._MTCorrectionDetails[self._MTCorrectionDetails["name"]+"_CorrectionUncertainty_bin_%d"%(i)]
                myCorrectedCount = 0.0
                myCorrectedUncertainty = 0.0
                for l in range(1,h.GetNbinsX()+1):
                    print "%f, %f"%( hCorr.GetBinContent(l), myCorrections[l-1])
                    myCorrectedCount += hCorr.GetBinContent(l)*myCorrections[l-1]
                    myCorrectedUncertainty += pow(hCorr.GetBinContent(l)*myCorrectionUncertainty[l-1],2)
                myCorrectedUncertainty = sqrt(myCorrectedUncertainty)
                print "*** MT correction %d: nominal = %f, corrected = %f +- %f"%(i,myNominalCount,myCorrectedCount,myCorrectedUncertainty)
                self._MTCorrectionFactorsForTauPtBins.append(myCorrectedCount)
                self._MTCorrectionFactorUncertaintyForTauPtBins.append(myCorrectedUncertainty)
                hCorrData.IsA().Destructor(hCorr)
                hCorrData.IsA().Destructor(hCorrData)
                hCorrMCEWK.IsA().Destructor(hCorrMCEWK)
####
            # Add to total shape histogram
            myShapeModifier.addShape(source=hMtBin,dest=h) # important to do before handling negative bins
            myShapeModifier.addShape(source=hMtBin,dest=hTotContractedX)
            # Remove negative bins, but retain original normalisation
            #for a in range(1,hMtBin.GetNbinsX()+1):
                #if hMtBin.GetBinContent(a) < 0.0:
                    ##print WarningStyle()+"Warning: QCD factorised"+NormalStyle()+" in mT shape bin %d,%d,%d, histo bin %d is negative (%f / tot:%f), it is set to zero but total normalisation is maintained"%(i,j,k,a,hMtBin.GetBinContent(a),hMtBin.Integral())
                    #myIntegral = hMtBin.Integral()
                    #hMtBin.SetBinContent(a,0.0)
                    #if (hMtBin.Integral() > 0.0):
                        #hMtBin.Scale(myIntegral / hMtBin.Integral())
            # Add to total info histogram
            for l in range (1, hMtBin.GetNbinsX()+1):
                hTot.SetBinContent(l+(j-1)*h.GetNbinsX(), k+(i-1)*nbinsZ, hMtBin.GetBinContent(l))
                hTot.SetBinError(l+(j-1)*h.GetNbinsX(), k+(i-1)*nbinsZ, hMtBin.GetBinError(l))
            # Store mT bin histogram for info
            if saveDetailedInfo:
                self._infoHistograms.append(hMtBin)
                self._infoHistograms.append(hMtBinData)
                self._infoHistograms.append(hMtBinEWK)
            else:
                hMtBin.IsA().Destructor(hMtBin)
            # Delete data and MC EWK histograms from memory
            hMtData.IsA().Destructor(hMtData)
            hMtMCEWK.IsA().Destructor(hMtMCEWK)
                    
            myEfficiency = QCDCalculator.getContracted1DLeg2Efficiency(i,"X")
            myShapeModifier.finaliseShape(dest=hTotContractedX)
            myShapeModifier.finaliseShape(dest=hTotContractedXeff)
            if myEfficiency.value() > 0.0:
                for l in range (1, hTotContractedXeff.GetNbinsX()+1):
                    # Make sure that uncertainty from efficiency is propagated to final shape
                    # Systematics has already been applied on MC EWK; they are assumed to cancel out on tau leg efficiency
                    hTotContractedXeff.SetBinError(l,sqrt(pow(hTotContractedXeff.GetBinError(l)*myEfficiency.value(),2)+pow(hTotContractedXeff.GetBinContent(l)*myEfficiency.uncertainty(),2)))
                    hTotContractedXeff.SetBinContent(l,hTotContractedXeff.GetBinContent(l)*myEfficiency.value())
            self._infoHistograms.append(hTotContractedX)
            self._infoHistograms.append(hTotContractedXeff)
            #myShapeModifier.addShape(source=hTotContractedXeff,dest=h)
        self._infoHistograms.append(hTot)
        # Finalise and return
        myShapeModifier.finaliseShape(dest=h)
        # Remove negative bins, but retain original normalisation
        for a in range(1,h.GetNbinsX()+1):
            if h.GetBinContent(a) < 0.0:
                #print WarningStyle()+"Warning: QCD factorised"+NormalStyle()+" in mT shape bin %d,%d,%d, histo bin %d is negative (%f / tot:%f), it is set to zero but total normalisation is maintained"%(i,j,k,a,hMtBin.GetBinContent(a),hMtBin.Integral())
                myIntegral = h.Integral()
                h.SetBinContent(a,0.0)
                if (h.Integral() > 0.0):
                    h.Scale(myIntegral / h.Integral())

        return h

    ## Extracts a shape histogram for a given bin
    def _extractShapeHistogram(self, dsetMgr, datasetMgrColumn, histoName, luminosity):
        try:
            dsetRootHistoMtData = dsetMgr.getDataset(datasetMgrColumn).getDatasetRootHisto(histoName)
        except Exception, e:
            raise Exception (ErrorStyle()+"Error in QCDfactorised/extracting shape:"+NormalStyle()+" cannot find histogram!\n  Message = %s!"%(str(e)))
        if dsetRootHistoMtData.isMC():
            dsetRootHistoMtData.normalizeToLuminosity(luminosity)
        h = dsetRootHistoMtData.getHistogram()
        if h == None:
            raise Exception(ErrorStyle()+"Error:"+NormalStyle()+" Cannot find histogram "+histoName+" for QCD factorised shape")
        return h

    def _createValidationHistograms(self, config, dsetMgr, QCDCalculator, QCDCount, luminosity, histoSpecs, title, histoDir, histoName):
        head,tail=os.path.split(histoName)
        title += "_%s"%tail
        print "      "+title
        # Create empty shape histogram
        myShapeModifier = ShapeHistoModifier(histoSpecs)
        # Obtain bin dimensions
        nbinsY = 1
        if QCDCount.is2D() or QCDCount.is3D():
            nbinsY = QCDCount.getNbinsY()
        nbinsZ = 1
        if QCDCount.is3D():
            nbinsZ = QCDCount.getNbinsZ()
        # Loop over bins
        for i in range(1,QCDCount.getNbinsX()+1):
            h = myShapeModifier.createEmptyShapeHistogram(title+"_bin_%d"%(i-1))
            for j in range(1,nbinsY+1):
                for k in range(1,nbinsZ+1):
                    # Determine suffix for histograms
                    myFactorisationSuffix = "_%d"%(i-1)
                    if QCDCount.is2D() or QCDCount.is3D():
                        myFactorisationSuffix += "_%d"%(j-1)
                    if QCDCount.is3D():
                        myFactorisationSuffix += "_%d"%(k-1)
                    # Get histograms for the bin for data and MC EWK
                    myFullHistoName = "%s/%s%s"%(histoDir,histoName,myFactorisationSuffix)
                    hMtData = self._extractShapeHistogram(dsetMgr, self._datasetMgrColumn, myFullHistoName, luminosity)
                    hMtMCEWK = self._extractShapeHistogram(dsetMgr, self._datasetMgrColumnForQCDMCEWK, myFullHistoName, luminosity)
                    # Add MC EWK systematics
                    for l in range (0, hMtMCEWK.GetNbinsX()+2):
                        myAbsSystUncertainty = QCDCalculator.getEWKMCRelativeSystematicUncertainty(i)* hMtMCEWK.GetBinContent(l)
                        hMtMCEWK.SetBinError(l,sqrt(pow(hMtMCEWK.GetBinError(l),2) + pow(myAbsSystUncertainty,2)))
                    # Obtain empty histograms
                    myOutHistoName = "QCDFact_%s_QCD_bin%s"%(title,myFactorisationSuffix)
                    hMtBin = myShapeModifier.createEmptyShapeHistogram(myOutHistoName)
                    # Add data to histograms
                    myShapeModifier.addShape(source=hMtData,dest=hMtBin)
                    # Subtract MC EWK from data to obtain QCD
                    myMessages = []
                    myMessages.extend(myShapeModifier.subtractShape(source=hMtMCEWK,dest=hMtBin,purityCheck=False))
                    # Finalise shape (underflow added to first bin, overflow added to last bin, variances converted to std.deviations)
                    myShapeModifier.finaliseShape(dest=hMtBin) # do not correct here for negative bins!
                    myShapeModifier.addShape(source=hMtBin,dest=h)
                    # Add to total shape histogram
                    # Store mT bin histogram for info
                    self._infoHistograms.append(hMtBin)
            # Finalise
            # Remove negative bins, but retain original normalisation
            #for a in range(1,hMtBin.GetNbinsX()+1):
                #if h.GetBinContent(a) < 0.0:
                    ##print WarningStyle()+"Warning: QCD factorised"+NormalStyle()+" in mT shape bin %d,%d,%d, histo bin %d is negative (%f / tot:%f), it is set to zero but total normalisation is maintained"%(i,j,k,a,hMtBin.GetBinContent(a),hMtBin.Integral())
                    #myIntegral = hMtBin.Integral()
                    #h.SetBinContent(a,0.0)
                    #h.SetBinError(a,0.0)
                    #if (h.Integral() > 0.0):
                        #h.Scale(myIntegral / h.Integral())
            myShapeModifier.finaliseShape(dest=h)
            self._infoHistograms.append(h)

    ## Saves information histograms into a histogram
    def saveQCDInfoHistograms(self, outputDir):
        # Open root file for saving
        myRootFilename = outputDir+"/QCDMeasurementFactorisedInfo.root"
        myRootFile = ROOT.TFile.Open(myRootFilename, "RECREATE")
        if myRootFile == None:
            print ErrorStyle()+"Error:"+NormalStyle()+" Cannot open file '"+myRootFilename+"' for output!"
            sys.exit()
        # Loop over info histograms
        myPreviousName = ""
        mySubDir = None
        for h in self._infoHistograms:
            histoname = h.GetName()
            myIndex = h.GetName().find("_bin")
            if myIndex >= 0:
                histoname = histoname[0:myIndex]
            # Store bin histograms in dedicated subdirectory
            if "bin" in h.GetName():
                # Make new subdirectory if necessary
                if myPreviousName != histoname:
                    if myRootFile.FindObject(histoname) == None:
                        mySubDir = myRootFile.mkdir(histoname)
                    else:
                        mySubDir = myRootFile.FindObject(histoname)
                h.SetDirectory(mySubDir)
            # Store summary histogram in main directory
            else:
                h.SetDirectory(myRootFile)
            myPreviousName = histoname

        # Close root file
        myRootFile.Write()
        myRootFile.Close()
        # Cleanup (closing the root file destroys the objects assigned to it, do not redestroy the histos in the _infoHistograms list
        self._infoHistograms = []
        print "\n"+HighlightStyle()+"QCD Measurement factorised info histograms saved to: "+NormalStyle()+myRootFilename

## QCDfactorisedExtractor class
# It is essentially wrapper for QCD mode string
class QCDfactorisedExtractor(ExtractorBase):
    ## Constructor
    def __init__(self, QCDmode, mode, exid = "", distribution = "lnN", description = ""):
        ExtractorBase.__init__(self, mode, exid, distribution, description)
        self._QCDmode = QCDmode

    ## Method for extracking information
    # Everything is processed 
    def extractResult(self, datasetColumn, datasetColumnForMCEWK, dsetMgr, luminosity, additionalNormalisation = 1.0):
        return 0.0

    ## Virtual method for extracting histograms
    # Returns the transverse mass plot
    def extractHistograms(self, datasetColumn, dsetMgr, mainCounterTable, luminosity, additionalNormalisation = 1.0):
        return []

    def getQCDmode(self):
        return self._QCDmode

    ## var _QCDmode
    # keyword for returning the stat, syst, or shapeStat results

def validateQCDCountObject():
    def check(a,b):
        if abs(a-b) < 0.00001:
            return TestPassedStyle()+"PASSED"+NormalStyle()
        else:
            print ErrorStyle()+"FAILED (%f != %f)"%(a,b)+NormalStyle()
            raise Exception("Error: validation test failed!")
    print HighlightStyle()+"validate: QCDCountObject\n"+NormalStyle()
    #aa = Count(25.0, 3.0, 0.0)
    #bb = Count(30.0, 0.0, 2.0)
    #cc = aa.copy()
    #cc.multiply(bb)
    #print cc._value, cc._uncertainty, cc._systUncertainty
    a = QCDCountObject(25.0, 3.0, 0.0, 0.0)
    #a.printContents()
    b = QCDCountObject(30.0, 0.0, 2.0, 1.0)
    #b.printContents()
    c = a.copy()
    c.add(b)
    #c.printContents()
    print "validate: QCDCountObject::add() value:",check(c.value(), 55.0)
    print "validate: QCDCountObject::add() data uncert:",check(c._dataUncert.uncertainty(), 3.0)
    print "validate: QCDCountObject::add() mc stat uncert:",check(c._mcUncert.uncertainty(), 2.0)
    print "validate: QCDCountObject::add() mc stat uncert:",check(c._mcUncert.systUncertainty(), 1.0)
    print "validate: QCDCountObject::sanityCheck() mc stat uncert:",check(c.sanityCheck(), True)
    d = QCDCountObject(10.0, 4.0, 2.0, 3.0)
    d.multiply(a)
    #d.printContents()
    print "validate: QCDCountObject::multiply() value:",check(d.value(), 250.0)
    print "validate: QCDCountObject::multiply() data uncert:",check(d._dataUncert.uncertainty(), sqrt(10900.0))
    print "validate: QCDCountObject::multiply() mc stat uncert:",check(d._mcUncert.uncertainty(), 50.0)
    print "validate: QCDCountObject::multiply() mc stat uncert:",check(d._mcUncert.systUncertainty(), 75.0)
    print "validate: QCDCountObject::sanityCheck() mc stat uncert:",check(d.sanityCheck(), True)
    e = QCDCountObject(10.0, 4.0, 2.0, 3.0)
    e.divide(a)
    #e.printContents()
    print "validate: QCDCountObject::divide() value:",check(e.value(), 0.4)
    print "validate: QCDCountObject::divide() data uncert:",check(e._dataUncert.uncertainty(), 0.4*sqrt(109.0/625.0))
    print "validate: QCDCountObject::divide() mc stat uncert:",check(e._mcUncert.uncertainty(), 0.4*2.0/10.0)
    print "validate: QCDCountObject::divide() mc stat uncert:",check(e._mcUncert.systUncertainty(), 0.4*3.0/10.0)
    print "validate: QCDCountObject::sanityCheck() mc stat uncert:",check(e.sanityCheck(), True)
