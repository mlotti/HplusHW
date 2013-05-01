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
        self._dataUncert = Count(value,dataStat)
        self._mcUncert = Count(value,mcStat,mcSyst)

    def value(self):
        return self._dataUncert.value()

    def setValue(self, value):
        self._dataUncert._value = value
        self._mcUncert._value = value

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
        return QCDCountObject(self._dataUncert.value(), self._dataUncert.uncertainty(), self._mcUncert.value(), self._mcUncert.value())

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

    def divideByScalar(self, scalar):
        self._dataUncert._value /= scalar
        self._dataUncert._uncertainty /= scalar
        self._mcUncert._value /= scalar
        self._mcUncert._uncertainty /= scalar
        self._mcUncert._systUncertainty /= scalar

## Extracts data-MC EWK counts from a given point in the analysis
class QCDEventCount():
    def __init__(self,
                 histoName,
                 dsetMgr,
                 dsetMgrDataColumn,
                 dsetMgrMCEWKColumn,
                 luminosity):
        self._histoname = histoName
        # Obtain histograms
        print "QCDfact: Obtaining count histogram: %s"%histoName
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

    def obtainDimensions(self):
        return self._reader.getNbinsList()

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

    ## Returns Count object for an unfolded bin of data
    # unfoldedBinIndex is the unfolded bin (numbering from zero)
    def getDataCountObjectForUnfoldedBin(self, unfoldedBinIndex):
        myValue = self._reader.getEventCountForUnfoldedBin(unfoldedBinIndex, self._hData)
        myStatUncertainty = self._reader.getEventCountUncertaintyForUnfoldedBin(unfoldedBinIndex, self._hData)
        return QCDCountObject(myValue, myStatUncertainty, 0.0, 0.0)

    ## Returns Count object for data
    # factorisationBinIndexList is a list of indices corresponding to the factorisation bin
    def getDataCountObject(self, factorisationBinIndexList):
        myValue = self.getDataCount(factorisationBinIndexList)
        myStatUncertainty = self.getDataError(factorisationBinIndexList)
        return QCDCountObject(myValue, myStatUncertainty, 0.0, 0.0)

    ## Returns number of events for data
    # factorisationBinIndexList is a list of indices corresponding to the factorisation bin
    def getDataCount(self, factorisationBinIndexList):
        return self._reader.getEventCountForBin(factorisationBinIndexList, self._hData)

    ## Returns stat. error (data only)
    # factorisationBinIndexList is a list of indices corresponding to the factorisation bin
    def getDataError(self, factorisationBinIndexList):
        return self._reader.getEventCountUncertaintyForBin(factorisationBinIndexList, self._hData)

    ## Returns number of events for data contracted to one factorisation dimension
    # axisIndexToKeep is the axis to be kept (for example: to keep first variable, ask for 0)
    # factorisationBinIndex is a list of indices corresponding to the factorisation bin
    def getContracted1DDataCountObject(self, factorisationBinIndex, axisIndexToKeep):
        myValue = self.getContracted1DDataCount(factorisationBinIndex, axisIndexToKeep)
        myStatUncertainty = self.getContracted1DDataError(factorisationBinIndex, axisIndexToKeep)
        return QCDCountObject(myValue, myStatUncertainty, 0.0, 0.0)

    ## Returns number of events for data contracted to one factorisation dimension
    # axisIndexToKeep is the axis to be kept (for example: to keep first variable, ask for 0)
    # factorisationBinIndex is a list of indices corresponding to the factorisation bin
    def getContracted1DDataCount(self, factorisationBinIndex, axisIndexToKeep):
        return self._reader.getContractedEventCountForBin(axisIndexToKeep, factorisationBinIndex, self._hData)

    ## Returns stat. error (data only) contracted to one factorisation dimension
    # axisIndexToKeep is the axis to be kept (for example: to keep first variable, ask for 0)
    # factorisationBinIndex is a list of indices corresponding to the factorisation bin
    def getContracted1DDataError(self, factorisationBinIndex, axisIndexToKeep):
        return self._reader.getContractedEventCountUncertaintyForBin(axisIndexToKeep, factorisationBinIndex, self._hData)

    ## Returns Count object for an unfolded bin of MC EWK
    # unfoldedBinIndex is the unfolded bin (numbering from zero)
    def getMCCountObjectForUnfoldedBin(self, unfoldedBinIndex):
        myValue = self._reader.getEventCountForUnfoldedBin(unfoldedBinIndex, self._hMC)
        myStatUncertainty = self._reader.getEventCountUncertaintyForUnfoldedBin(unfoldedBinIndex, self._hMC)
        myTauPtIndex = self._reader.decomposeUnfoldedbin(unfoldedBinIndex)[self._tauPtAxisIndex]
        mySystUncertainty = myValue * self.getEWKMCRelativeSystematicUncertainty(myTauPtIndex)
        return QCDCountObject(myValue, 0.0, myStatUncertainty, mySystUncertainty)

    ## Returns Count object for MC EWK
    # factorisationBinIndexList is a list of indices corresponding to the factorisation bin
    def getMCCountObject(self, factorisationBinIndexList):
        myValue = self.getMCCount(factorisationBinIndexList)
        myStatUncertainty = self.getMCStatError(factorisationBinIndexList)
        mySystUncertainty = self.getMCSystError(factorisationBinIndexList)
        return QCDCountObject(myValue, 0.0, myStatUncertainty, mySystUncertainty)

    ## Returns number of events for MC
    # factorisationBinIndexList is a list of indices corresponding to the factorisation bin
    def getMCCount(self, factorisationBinIndexList):
        return self._reader.getEventCountForBin(factorisationBinIndexList, self._hMC)

    ## Returns stat. error (data only)
    # factorisationBinIndexList is a list of indices corresponding to the factorisation bin
    def getMCStatError(self, factorisationBinIndexList):
        return self._reader.getEventCountUncertaintyForBin(factorisationBinIndexList, self._hMC)

    ## Returns syst. error (MC only)
    # factorisationBinIndexList is a list of indices corresponding to the factorisation bin
    def getMCSystError(self, factorisationBinIndexList):
        return getMCCount(factorisationBinIndexList) * self.getEWKMCRelativeSystematicUncertainty(factorisationBinIndexList[self._tauPtAxisIndex])

    ## Returns number of events for MC contracted to one factorisation dimension
    # axisIndexToKeep is the axis to be kept (for example: to keep first variable, ask for 0)
    # factorisationBinIndex is a list of indices corresponding to the factorisation bin
    def getContracted1DMCCountObject(self, factorisationBinIndex, axisIndexToKeep):
        myValue = self.getContracted1DMCCount(factorisationBinIndex, axisIndexToKeep)
        myStatUncertainty = self.getContracted1DMCStatError(factorisationBinIndex, axisIndexToKeep)
        mySystUncertainty = self.getContracted1DMCSystError(factorisationBinIndex, axisIndexToKeep)
        return QCDCountObject(myValue, 0.0, myStatUncertainty, mySystUncertainty)

    ## Returns number of events for MC contracted to one factorisation dimension
    # axisIndexToKeep is the axis to be kept (for example: to keep first variable, ask for 0)
    # factorisationBinIndex is a list of indices corresponding to the factorisation bin
    def getContracted1DMCCount(self, factorisationBinIndex, axisIndexToKeep):
        return self._reader.getContractedEventCountForBin(axisIndexToKeep, factorisationBinIndex, self._hMC)

    ## Returns stat. error (data only) contracted to one factorisation dimension
    # axisIndexToKeep is the axis to be kept (for example: to keep first variable, ask for 0)
    # factorisationBinIndex is a list of indices corresponding to the factorisation bin
    def getContracted1DMCStatError(self, factorisationBinIndex, axisIndexToKeep):
        return self._reader.getContractedEventCountUncertaintyForBin(axisIndexToKeep, factorisationBinIndex, self._hMC)

    ## Returns stat. error (data only) contracted to one factorisation dimension
    # axisIndexToKeep is the axis to be kept (for example: to keep first variable, ask for 0)
    # factorisationBinIndex is a list of indices corresponding to the factorisation bin
    def getContracted1DMCSystError(self, factorisationBinIndex, axisIndexToKeep):
        # Calculation becomes difficult, make conservative approximation by taking worst case
        return self.getContracted1DMCCount(factorisationBinIndex, axisIndexToKeep) * self.getEWKMCRelativeSystematicUncertainty(999)

    ## Returns Count object for data-MC (uncertainty separately for stat. and syst. uncertainty)
    # factorisationBinIndexList is a list of indices corresponding to the factorisation bin
    def getQCDCount(self, factorisationBinIndexList, cleanNegativeValues=True):
        myDataObject = self.getDataCountObject(factorisationBinIndexList)
        myMCObject = self.getMCCountObject(factorisationBinIndexList)
        myResult = myDataObject.copy()
        myResult.subtract(myMCObject)
        # Obtain uncertainty # Check negative result
        if myResult.value() < 0.0:
            if cleanNegativeValues:
                myResult.setValue(0.0)
            #myResultError = 0.0 do not set it to zero, but instead keep it as it is to be more realistic!
        # Return result 
        return myResult

    ## Returns Count object for data-MC (uncertainty separately for stat. and syst. uncertainty)
    # unfoldedBinIndex is the unfolded bin (numbering from zero)
    def getQCDCountForUnfoldedBin(self, unfoldedBinIndex, cleanNegativeValues=True):
        myDataObject = self.getDataCountObjectForUnfoldedBin(unfoldedBinIndex)
        myMCObject = self.getMCCountObjectForUnfoldedBin(unfoldedBinIndex)
        myResult = myDataObject.copy()
        myResult.subtract(myMCObject)
        # Obtain uncertainty # Check negative result
        if myResult.value() < 0.0:
            if cleanNegativeValues:
                myResult.setValue(0.0)
            #myResultError = 0.0 do not set it to zero, but instead keep it as it is to be more realistic!
        # Return result 
        return myResult

    ## Returns Count object for data-MC for a bin on a variation parameter, other parameters are contracted (i.e. summed)
    # (uncertainty separately for stat. and syst. uncertainty)
    # factorisationBinIndex is a list of indices corresponding to the factorisation bin
    # axisIndexToKeep is the axis to be kept (for example: to keep first variable, ask for 0)
    def getContracted1DQCDCount(self, factorisationBinIndex, axisIndexToKeep, cleanNegativeValues=True):
        myDataObject = self.getContracted1DDataCountObject(factorisationBinIndex, axisIndexToKeep)
        myMCObject = self.getContracted1DMCCountObject(factorisationBinIndex, axisIndexToKeep)
        myResult = myDataObject.copy()
        myResult.subtract(myMCObject)
        # Obtain uncertainty # Check negative result
        if myResult.value() < 0:
            if cleanNegativeValues:
                myResult.setValue(0.0)
            #myResultError = 0.0 do not set it to zero, but instead keep it as it is to be more realistic!
        # Return result
        return myResult

    ## Getter for purity (data-MC)/data = 1-MC/data
    # Returns Count object
    def getPurity(self, factorisationBinIndexList):
        myDataCount = self.getDataCountObject(factorisationBinIndexList)
        myMCCount = self.getMCCountObject(factorisationBinIndex)
        return self._calculatePurity(myDataCount, myMCCount)

    ## Getter for purity (data-MC)/data = 1-MC/data for unfolded bin index
    # Returns Count object
    def getPurityForUnfoldedBin(self, unfoldedBinIndex):
        myDataCount = self.getDataCountObjectForUnfoldedBin(unfoldedBinIndex)
        myMCCount = self.getMCCountObjectForUnfoldedBin(unfoldedBinIndex)
        return self._calculatePurity(myDataCount, myMCCount)

    ## Getter for purity (data-MC)/data = 1-MC/data contracted to one factorisation axis
    # Returns Count object
    def getContracted1DPurity(self, factorisationBinIndex, axisIndexToKeep):
        myDataCount = self.getContracted1DDataCountObject(factorisationBinIndex, axisIndexToKeep)
        myMCCount = self.getContracted1DMCCountObject(factorisationBinIndex, axisIndexToKeep)
        return self._calculatePurity(myDataCount, myMCCount)

    ## Actual calculation of the purity value with Count objects
    def _calculatePurity(self, data, mc):
        myResult = mc.copy()
        if data.value() > 0:
            myResult.divide(data)
            myResult.setValue(1.0 - myResult.value())
        else:
            # Set purity value to zero, but count uncertainty properly
            myDummyData = QCDCountObject(1.0, 1.0, 0.0, 0.0)
            myResult.divide(myDummyData)
            myResult.setValue(0.0)
        return myResult

    ## Returns purity histograms (purity as function of the unfolded factorisation binning and contracted histograms)
    def makePurityHistograms(self):
        hlist = []
        # Make uncontracted histograms (can be a loooot of bins)
        myName = "Purity_StatOnly_%s"%self._histoname.replace("/","_")
        hStat = ROOT.TH1F(myName,myName,self._hData.GetNbinsY(),0,self._hData.GetNbinsY())
        hStat.SetYTitle("Purity")
        hStat.SetMaximum(1.0)
        myName = "Purity_StatAndSyst_%s"%self._histoname.replace("/","_")
        hFull = ROOT.TH1F(myName,myName,self._hData.GetNbinsY(),0,self._hData.GetNbinsY())
        hFull.SetYTitle("Purity")
        hFull.SetMaximum(1.0)
        for i in range(0,self._hData.GetNbinsY()):
            myPurity = self.getPurityForUnfoldedBin(i)
            if myPurity.value() > 0.0 and myPurity.value() < 0.5:
                myMsg = WarningLabel()+"QCD factorised: Low purity in %s for bin %s (%f +- %f +- %f)!"%(self._histoname,self._hData.GetYaxis().GetBinLabel(i+1),myPurity.value(),myPurity.uncertainty(),myPurity.systUncertainty())
                self._messages.append(myMsg)
            hStat.SetBinContent(i+1, myPurity.value())
            hStat.SetBinError(i+1, myPurity.uncertainty())
            hFull.SetBinContent(i+1, myPurity.value())
            hFull.SetBinError(i+1, myPurity.totalUncertainty())
            hStat.GetXaxis().SetBinLabel(i+1,self._hData.GetYaxis().GetBinLabel(i+1))
            hFull.GetXaxis().SetBinLabel(i+1,self._hData.GetYaxis().GetBinLabel(i+1))
        hlist.append(hStat)
        hlist.append(hFull)
        # Make contracted histograms (easier to read)
        myBinDimensions = self._reader.getNbinsList()
        for myDim in range(0, len(myBinDimensions)):
            myName = "Purity_%s_StatOnly_%s"%(self._reader.getBinLabelList()[myDim].replace(" ","_"), self._histoname.replace("/","_"))
            hCStat = ROOT.TH1F(myName,myName,self._hData.GetNbinsY(),0,self._hData.GetNbinsY())
            hCStat.SetXTitle(self._reader.getFactorisationCaptions()[myDim])
            hCStat.SetYTitle("Purity")
            hCStat.SetMaximum(1.0)
            myName = "Purity_%s_StatAndSyst_%s"%(self._reader.getBinLabelList()[myDim].replace(" ","_"), self._histoname.replace("/","_"))
            hCFull = ROOT.TH1F(myName,myName,self._hData.GetNbinsY(),0,self._hData.GetNbinsY())
            hCFull.SetXTitle(self._reader.getFactorisationCaptions()[myDim])
            hCFull.SetYTitle("Purity")
            hCFull.SetMaximum(1.0)
            for i in range(0, myBinDimensions[myDim]):
                myPurity = self.getContracted1DPurity(i, myDim)
                if myPurity.value() > 0.0 and myPurity.value() < 0.5:
                    myMsg = WarningLabel()+"QCD factorised: Low purity in %s for contracted bin %s %s (%f +- %f +- %f)!"%(self._histoname,self._reader.getFactorisationCaptions()[myDim],self._reader.getFactorisationRanges()[myDim][i],myPurity.value(),myPurity.uncertainty(),myPurity.systUncertainty())
                    self._messages.append(myMsg)
                hCStat.SetBinContent(i+1, myPurity.value())
                hCStat.SetBinError(i+1, myPurity.uncertainty())
                hCFull.SetBinContent(i+1, myPurity.value())
                hCFull.SetBinError(i+1, myPurity.totalUncertainty())
                hCStat.GetXaxis().SetBinLabel(i+1,self._reader.getFactorisationRanges()[myDim][i])
                hCFull.GetXaxis().SetBinLabel(i+1,self._reader.getFactorisationRanges()[myDim][i])
            hlist.append(hCStat)
            hlist.append(hCFull)
        return hlist

    ## Returns Nevent histograms (Nevent as function of the unfolded factorisation binning and contracted histograms)
    ## Returns histogram(s) for number of events
    def makeEventCountHistograms(self):
        hlist = []
        # Make uncontracted histograms (can be a loooot of bins)
        myName = "Nevents_StatOnly_%s"%self._histoname.replace("/","_")
        hStat = ROOT.TH1F(myName,myName,self._hData.GetNbinsY(),0,self._hData.GetNbinsY())
        hStat.SetYTitle("dN_{events}/dbin width")
        hStat.SetMaximum(1.0)
        myName = "Nevents_StatAndSyst_%s"%self._histoname.replace("/","_")
        hFull = ROOT.TH1F(myName,myName,self._hData.GetNbinsY(),0,self._hData.GetNbinsY())
        hFull.SetYTitle("dN_{events}/dbin width")
        hFull.SetMaximum(1.0)
        for i in range(0,self._hData.GetNbinsY()):
            myResult = self.getQCDCountForUnfoldedBin(i)
            myBinWidth = self._hData.GetBinWidth(i+1)
            hStat.SetBinContent(i+1, myResult.value() / myBinWidth)
            hStat.SetBinError(i+1, myResult.uncertainty() / myBinWidth)
            hFull.SetBinContent(i+1, myResult.value() / myBinWidth)
            hFull.SetBinError(i+1, myResult.totalUncertainty())
            hStat.GetXaxis().SetBinLabel(i+1,self._hData.GetYaxis().GetBinLabel(i+1))
            hFull.GetXaxis().SetBinLabel(i+1,self._hData.GetYaxis().GetBinLabel(i+1))
        hlist.append(hStat)
        hlist.append(hFull)
        # Make contracted histograms (easier to read)
        myBinDimensions = self._reader.getNbinsList()
        for myDim in range(0, len(myBinDimensions)):
            myName = "Nevents_%s_StatOnly_%s"%(self._reader.getBinLabelList()[myDim].replace(" ","_"), self._histoname.replace("/","_"))
            hCStat = ROOT.TH1F(myName,myName,self._hData.GetNbinsY(),0,self._hData.GetNbinsY())
            hCStat.SetXTitle(self._reader.getFactorisationCaptions()[myDim])
            hCStat.SetYTitle("dN_{events}/dbin width")
            hCStat.SetMaximum(1.0)
            myName = "Nevents_%s_StatAndSyst_%s"%(self._reader.getBinLabelList()[myDim].replace(" ","_"), self._histoname.replace("/","_"))
            hCFull = ROOT.TH1F(myName,myName,self._hData.GetNbinsY(),0,self._hData.GetNbinsY())
            hCFull.SetXTitle(self._reader.getFactorisationCaptions()[myDim])
            hCFull.SetYTitle("dN_{events}/dbin width")
            hCFull.SetMaximum(1.0)
            for i in range(0, myBinDimensions[myDim]):
                myResult = self.getContracted1DQCDCount(i, myDim)
                myBinWidth = self._hData.GetBinWidth(i+1)
                hCStat.SetBinContent(i+1, myResult.value() / myBinWidth)
                hCStat.SetBinError(i+1, myResult.uncertainty() / myBinWidth)
                hCFull.SetBinContent(i+1, myResult.value() / myBinWidth)
                hCFull.SetBinError(i+1, myResult.totalUncertainty())
                hCStat.GetXaxis().SetBinLabel(i+1,self._reader.getFactorisationRanges()[myDim][i])
                hCFull.GetXaxis().SetBinLabel(i+1,self._reader.getFactorisationRanges()[myDim][i])
            hlist.append(hCStat)
            hlist.append(hCFull)
        return hlist

    ## Returns histogram(s) for checking the impact of negative QCD counts
    def makeNegativeEventCountHistograms(self):
        hlist = []
        # Make uncontracted histograms (can be a loooot of bins)
        myName = "NegativeNevents_StatOnly_%s"%self._histoname.replace("/","_")
        hStat = ROOT.TH1F(myName,myName,self._hData.GetNbinsY(),0,self._hData.GetNbinsY())
        hStat.SetYTitle("dN_{events}/dbin width")
        hStat.SetMaximum(1.0)
        myName = "NegativeNevents_StatAndSyst_%s"%self._histoname.replace("/","_")
        hFull = ROOT.TH1F(myName,myName,self._hData.GetNbinsY(),0,self._hData.GetNbinsY())
        hFull.SetYTitle("dN_{events}/dbin width")
        hFull.SetMaximum(1.0)
        for i in range(0,self._hData.GetNbinsY()):
            myResult = self.getQCDCountForUnfoldedBin(i, cleanNegativeValues=False)
            myBinWidth = self._hData.GetBinWidth(i+1)
            if myResult.value() < 0: # Plot only negative values
                myMsg = WarningLabel()+"QCD factorised: Negative NQCD count in %s for bin %s (%f +- %f +- %f)!"%(self._histoname,self._hData.GetYaxis().GetBinLabel(i+1),myResult.value(),myResult.uncertainty(),myResult.systUncertainty())
                self._messages.append(myMsg)
                hStat.SetBinContent(i+1, myResult.value() / myBinWidth)
                hStat.SetBinError(i+1, myResult.uncertainty() / myBinWidth)
                hFull.SetBinContent(i+1, myResult.value() / myBinWidth)
                hFull.SetBinError(i+1, myResult.totalUncertainty())
                hStat.GetXaxis().SetBinLabel(i+1,self._hData.GetYaxis().GetBinLabel(i+1))
                hFull.GetXaxis().SetBinLabel(i+1,self._hData.GetYaxis().GetBinLabel(i+1))
        hlist.append(hStat)
        hlist.append(hFull)
        # Make contracted histograms (easier to read)
        myBinDimensions = self._reader.getNbinsList()
        for myDim in range(0, len(myBinDimensions)):
            myName = "NegativeNevents_%s_StatOnly_%s"%(self._reader.getBinLabelList()[myDim].replace(" ","_"), self._histoname.replace("/","_"))
            hCStat = ROOT.TH1F(myName,myName,self._hData.GetNbinsY(),0,self._hData.GetNbinsY())
            hCStat.SetXTitle(self._reader.getFactorisationCaptions()[myDim])
            hCStat.SetYTitle("dN_{events}/dbin width")
            hCStat.SetMaximum(1.0)
            myName = "NegativeNevents_%s_StatAndSyst_%s"%(self._reader.getBinLabelList()[myDim].replace(" ","_"), self._histoname.replace("/","_"))
            hCFull = ROOT.TH1F(myName,myName,self._hData.GetNbinsY(),0,self._hData.GetNbinsY())
            hCFull.SetXTitle(self._reader.getFactorisationCaptions()[myDim])
            hCFull.SetYTitle("dN_{events}/dbin width")
            hCFull.SetMaximum(1.0)
            for i in range(0, myBinDimensions[myDim]):
                myMsg = WarningLabel()+"QCD factorised: Negative NQCD count in %s for contracted bin %s %s (%f +- %f +- %f)!"%(self._histoname,self._reader.getFactorisationCaptions()[myDim],self._reader.getFactorisationRanges()[myDim][i],myResult.value(),myResult.uncertainty(),myResult.systUncertainty())
                self._messages.append(myMsg)
                myResult = self.getContracted1DQCDCount(i, myDim, cleanNegativeValues=False)
                myBinWidth = self._hData.GetBinWidth(i+1)
                if myResult.value() < 0: # Plot only negative values
                    hCStat.SetBinContent(i+1, myResult.value() / myBinWidth)
                    hCStat.SetBinError(i+1, myResult.uncertainty() / myBinWidth)
                    hCFull.SetBinContent(i+1, myResult.value() / myBinWidth)
                    hCFull.SetBinError(i+1, myResult.totalUncertainty())
                    hCStat.GetXaxis().SetBinLabel(i+1,self._reader.getFactorisationRanges()[myDim][i])
                    hCFull.GetXaxis().SetBinLabel(i+1,self._reader.getFactorisationRanges()[myDim][i])
            hlist.append(hCStat)
            hlist.append(hCFull)
        return hlist

## Helper class for calculating the result from three points of counting in the analysis
class QCDfactorisedCalculator():
    def __init__(self, basicCounts, leg1Counts, leg2Counts, doHistograms=False):
        self._basicCount = basicCounts
        self._leg1Counts = leg1Counts
        self._leg2Counts = leg2Counts

        self._yieldTable = ""
        self._compactYieldTable = ""

        # Count NQCD
        self._NQCD = None # QCDCountObject object, NQCD calculate with full parameter space
        self._contractedNQCD = [] # List of QCDCountObject objects, NQCD calculated by first contracting parameter space to one dimension
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

    def getNQCD(self):
        return self._NQCD

    def getContractedNQCDList(self):
        return self._contractedNQCD

    def getNQCDHistograms(self):
        return self._nQCDHistograms

    #def getDataUncertainty(self):
        #return self._dataUncertainty / self._NQCD

    #def getMCStatUncertainty(self):
        #return self._MCStatUncertainty / self._NQCD

    #def getMCSystUncertainty(self):
        #return self._MCSystUncertainty / self._NQCD

    #def getStatUncertainty(self):
        #return sqrt(pow(self._dataUncertainty,2)+pow(self._MCStatUncertainty,2)) / self._NQCD

    #def getSystUncertainty(self):
        #return self.getMCSystUncertainty()

    #def getContractedStatUncertainty(self,axis):
        #return sqrt(pow(self._contractedDataUncertainty[axis],2)+pow(self._contractedMCStatUncertainty[axis],2)) / self._contractedNQCD[axis]

    #def getContractedSystUncertainty(self,axis):
        #return self._contractedMCSystUncertainty[axis] / self._contractedNQCD[axis]

    #def getTotalUncertainty(self):
        #return sqrt(pow(self._dataUncertainty,2)+pow(self._MCStatUncertainty,2)+pow(self._getMCSystUncertainty,2)) / self._NQCD

    def getLeg1EfficiencyForUnfoldedBin(self, unfoldedBinIndex):
        return self._getEfficiencyForUnfoldedBin(self, unfoldedBinIndex)(self._leg1Counts, self._basicCount, unfoldedBinIndex)

    def getLeg2EfficiencyForUnfoldedBin(self, unfoldedBinIndex):
        return self._getEfficiencyForUnfoldedBin(self, unfoldedBinIndex)(self._leg2Counts, self._basicCount, unfoldedBinIndex)

    def getLeg1Efficiency(self, factorisationBinIndexList):
        return self._getEfficiency(self._leg1Counts, self._basicCount, factorisationBinIndexList)

    def getLeg2Efficiency(self, factorisationBinIndexList):
        return self._getEfficiency(self._leg2Counts, self._basicCount, factorisationBinIndexList)

    #def getLeg2EWKMCCounts(self, factorisationBinIndexList):
        #return self._leg2Counts.getMCCount(idx,idy,idz)

    #def getQCDBasicCounts(self,idx,idy=-1,idz=-1):
        #return self._basicCount.getQCDCount(idx,idy,idz)

    #def getLeg2StatUncertainty(self,idx,idy=-1,idz=-1):
        #return sqrt(pow(self._leg2Counts.getMCStatError(idx,idy,idz),2)+pow(self._leg2Counts.getDataError(idx,idy,idz),2))

    def _getEfficiencyForUnfoldedBin(self,numerator,denominator,unfoldedBinIndex):
        numeratorCount = numerator.getQCDCount(unfoldedBinIndex)
        denominatorCount = denominator.getQCDCount(unfoldedBinIndex)
        Result = QCDCountObject(0.0, 0.0, 0.0, 0.0)
        if denominatorCount.value() > 0:
            myResult = numeratorCount.copy()
            myResult.divide(denominatorCount)
            #print "1D eff: nom=%f, denom=%f, value=%f +- %f:"%(numeratorCount.value(),denominatorCount.value(),myValue,myError)
        return myResult

    def _getEfficiency(self,numerator,denominator,factorisationBinIndexList):
        numeratorCount = numerator.getQCDCount(factorisationBinIndexList)
        denominatorCount = denominator.getQCDCount(factorisationBinIndexList)
        Result = QCDCountObject(0.0, 0.0, 0.0, 0.0)
        if denominatorCount.value() > 0:
            myResult = numeratorCount.copy()
            myResult.divide(denominatorCount)
            #print "1D eff: nom=%f, denom=%f, value=%f +- %f:"%(numeratorCount.value(),denominatorCount.value(),myValue,myError)
        return myResult

    def _getEfficiencyCLP(self,numerator,denominator,factorisationBinIndexList):
        numeratorCount = numerator.getQCDCount(factorisationBinIndexList)
        denominatorCount = denominator.getQCDCount(factorisationBinIndexList)
        myResult = CountAsymmetric(0.0, 0.0, 0.0)
        if denominatorCount.value() > 0:
            myResult = dataset.divideBinomial(numeratorCount.getCountObject(), denominatorCount.getCountObject())
            #print "1D eff: nom=%f, denom=%f, value=%f +- %f:"%(numeratorCount.value(),denominatorCount.value(),myValue,myError)
        return myResult

    def getContracted1DLeg1Efficiency(self,factorisationBinIndex,axisIndexToKeep):
        return self._getContracted1DEfficiency(self._leg1Counts,self._basicCount,factorisationBinIndex,axisIndexToKeep)

    def getContracted1DLeg2Efficiency(self,factorisationBinIndex,axisIndexToKeep):
        return self._getContracted1DEfficiency(self._leg2Counts,self._basicCount,factorisationBinIndex,axisIndexToKeep)

    ## Returns the efficiency for a bin on first variation parameter, other parameters are contracted (i.e. summed)
    def _getContracted1DEfficiency(self,numerator,denominator,factorisationBinIndex,axisIndexToKeep):
        numeratorCount = numerator.getContracted1DQCDCount(factorisationBinIndex,axisIndexToKeep)
        denominatorCount = denominator.getContracted1DQCDCount(factorisationBinIndex,axisIndexToKeep)
        Result = QCDCountObject(0.0, 0.0, 0.0, 0.0)
        if denominatorCount.value() > 0:
            myResult = numeratorCount.copy()
            myResult.divide(denominatorCount)
            #print "1D eff: nom=%f, denom=%f, value=%f +- %f:"%(numeratorCount.value(),denominatorCount.value(),myValue,myError)
        return myResult

    def getLeg1EfficiencyHistogram(self):
        return self._createEfficiencyHistogram(self._leg1Counts, self._basicCount, "leg1")

    def getLeg2EfficiencyHistogram(self):
        return self._createEfficiencyHistogram(self._leg2Counts, self._basicCount, "leg2")

    def _createEfficiencyHistogram(self, numerator, denominator, suffix=""):
        # FIXME
        # Create histogram
        hlist = []
        if numerator.is1D():
            h = numerator.getClonedHisto("QCDfactEff_"+suffix)
            h.Reset()
            h.SetYTitle("Efficiency")
            for i in range(1, h.GetNbinsX()+1):
                myEfficiency = self._getEfficiency(numerator,denominator,i)
                if myEfficiency.value() > 0:
                    h.SetBinContent(i, myEfficiency.value())
                    h.SetBinError(i, myEfficiency.uncertainty())
            hlist.append(h)
        elif numerator.is2D():
            h = numerator.getClonedHisto("QCDfactEff_"+suffix)
            h.Reset()
            h.SetZTitle("Efficiency")
            for i in range(1, h.GetNbinsX()+1):
                for j in range(1, h.GetNbinsY()+1):
                    myEfficiency = self._getEfficiency(numerator,denominator,i,j)
                    if myEfficiency.value() > 0:
                        h.SetBinContent(i, j, myEfficiency.value())
                        h.SetBinError(i, j, myEfficiency.uncertainty())
            hlist.append(h)
        elif numerator.is3D():
            myName = "QCDfactEff_"+suffix+"_Total"
            hTot = ROOT.TH2F(myName,myName,numerator.getNbinsY(),0,numerator.getNbinsY(),numerator.getNbinsX()*numerator.getNbinsZ(),0,numerator.getNbinsX()*numerator.getNbinsZ())
            for i in range(1, numerator.getNbinsX()+1):
                # Generate one 2D histo for each x bin
                myName = "QCDfactEff_"+suffix+"_bin_%d"%(i)
                h = ROOT.TH2F(myName,myName,numerator.getNbinsY(),0,numerator.getNbinsY(),numerator.getNbinsZ(),0,numerator.getNbinsZ())
                h.SetZTitle("Efficiency")
                for j in range(1, numerator.getNbinsY()+1):
                    h.GetXaxis().SetBinLabel(j,numerator.getBinLabel("Y",j))
                    hTot.GetXaxis().SetBinLabel(j,numerator.getBinLabel("Y",j))
                for k in range(1, numerator.getNbinsZ()+1):
                    h.GetYaxis().SetBinLabel(k,numerator.getBinLabel("Z",k))
                    hTot.GetYaxis().SetBinLabel(k+(i-1)*numerator.getNbinsZ(),"("+numerator.getBinLabel("X",i)+"; "+numerator.getBinLabel("Z",k))
                # Calculate and fill efficiency
                for j in range(1, numerator.getNbinsY()+1):
                    for k in range(1, numerator.getNbinsZ()+1):
                        myEfficiency = self._getEfficiency(numerator,denominator,i,j,k)
                        if myEfficiency.value() > 0:
                            h.SetBinContent(j, k, myEfficiency.value())
                            h.SetBinError(j, k, myEfficiency.uncertainty())
                            hTot.SetBinContent(j, k+(i-1)*numerator.getNbinsZ(), myEfficiency.value())
                            hTot.SetBinError(j, k+(i-1)*numerator.getNbinsZ(), myEfficiency.uncertainty())
                hlist.append(h)
            hlist.append(hTot)
        else:
             raise Exception(ErrorStyle()+"Warning: QCD:Factorised: Efficiency histogram not yet supported for more than 1 dimensions"+NormalStyle())
        return hlist

    def getNQCDForUnfoldedBin(self,unfoldedBinIndex):
        myBasicCountObject = self._basicCount.getQCDCountForUnfoldedBin(unfoldedBinIndex)
        myLeg1CountObject = self._leg1Counts.getQCDCountForUnfoldedBin(unfoldedBinIndex)
        myLeg2CountObject = self._leg2Counts.getQCDCountForUnfoldedBin(unfoldedBinIndex)
        return self._calculateNQCD(myBasicCountObject, myLeg1CountObject, myLeg2CountObject)

    def getContracted1DNQCDForBin(self,factorisationBinIndex, axisIndexToKeep):
        myBasicCountObject = self._basicCount.getContracted1DQCDCount(factorisationBinIndex, axisIndexToKeep)
        myLeg1CountObject = self._leg1Counts.getContracted1DQCDCount(factorisationBinIndex, axisIndexToKeep)
        myLeg2CountObject = self._leg2Counts.getContracted1DQCDCount(factorisationBinIndex, axisIndexToKeep)
        return self._calculateNQCD(myBasicCountObject, myLeg1CountObject, myLeg2CountObject)

    def _calculateNQCD(self, myBasicCountObject, myLeg1CountObject, myLeg2CountObject):
        myResult = QCDCountObject(0.0, 0.0, 0.0, 0.0)
        # Protect calculation against div by zero
        if (myBasicCountObject.value() > 0.0):
            # Calculate uncertainty as f=a*b  (i.e. ignore basic counts uncertainty since it is the denominator to avoid double counting of uncertainties)
            # Note that this is more conservative than CLP
            myResult = myLeg1CountObject.copy()
            myResult.multiply(myLeg2CountObject)
            myResult.divideByScalar(myBasicCountObject.value())
            # df = sqrt((b*da)^2 + (a*db)^2)
            #myDataUncert   = sqrt(pow(myLeg2Counts*self._leg1Counts.getDataError(idx,idy,idz)  /myBasicCounts,2) + 
                                  #pow(myLeg1Counts*self._leg2Counts.getDataError(idx,idy,idz)  /myBasicCounts,2))
            #myMCStatUncert = sqrt(pow(myLeg2Counts*self._leg1Counts.getMCStatError(idx,idy,idz)/myBasicCounts,2) +
                                  #pow(myLeg1Counts*self._leg2Counts.getMCStatError(idx,idy,idz)/myBasicCounts,2))
            #myLeg1Systematics = self._leg1Counts.getMCCountForUnfoldedBin(unfoldedBinIndex).value() * self.getEWKMCRelativeSystematicUncertainty(idx)
            #myLeg2Systematics = self._leg2Counts.getMCCountForUnfoldedBin(unfoldedBinIndex).value() * self.getEWKMCRelativeSystematicUncertainty(idx)
            #myMCSystUncert = sqrt(pow(myLeg2Counts*myLeg1Systematics/myBasicCounts,2) +
                                  #pow(myLeg1Counts*myLeg2Systematics/myBasicCounts,2))
        return myResult


    def _count(self):
        hlist = []
        self._NQCD = QCDCountObject(0.0, 0.0, 0.0, 0.0)
        # Make uncontracted histograms (can be a loooot of bins)
        myName = "NQCD_StatOnly"
        myNbins = self._basicCount.getReader().getUnfoldedBinCount()
        hStat = ROOT.TH1F(myName,myName,myNbins,0.0,myNbins)
        hStat.SetYTitle("NQCD")
        hStat.SetMaximum(1.0)
        myName = "NQCD_StatAndSyst"
        hFull = ROOT.TH1F(myName,myName,myNbins,0.0,myNbins)
        hFull.SetYTitle("NQCD")
        hFull.SetMaximum(1.0)
        for i in range(0,myNbins):
            myResult = self.getNQCDForUnfoldedBin(i)
            self._NQCD.add(myResult)
            hStat.SetBinContent(i+1, myResult.value())
            hStat.SetBinError(i+1, myResult.uncertainty())
            hFull.SetBinContent(i+1, myResult.value())
            hFull.SetBinError(i+1, myResult.totalUncertainty())
            hStat.GetXaxis().SetBinLabel(i+1,self._basicCount.getFactorisationBinLabel(i))
            hFull.GetXaxis().SetBinLabel(i+1,self._basicCount.getFactorisationBinLabel(i))
        self._nQCDHistograms.append(hStat)
        self._nQCDHistograms.append(hFull)
        # Make contracted histograms (easier to read)
        myBinDimensions = self._basicCount.getReader().getNbinsList()
        for myDim in range(0, len(myBinDimensions)):
            self._contractedNQCD.append(QCDCountObject(0.0, 0.0, 0.0, 0.0))
            myName = "NQCD_%s_StatOnly"%(self._basicCount.getReader().getBinLabelList()[myDim].replace(" ","_"))
            hCStat = ROOT.TH1F(myName,myName,myNbins,0.0,myNbins)
            hCStat.SetXTitle(self._basicCount.getReader().getFactorisationCaptions()[myDim])
            hCStat.SetYTitle("NQCD")
            hCStat.SetMaximum(1.0)
            myName = "NQCD_%s_StatAndSyst"%(self._basicCount.getReader().getBinLabelList()[myDim].replace(" ","_"))
            hCFull = ROOT.TH1F(myName,myName,myNbins,0.0,myNbins)
            hCFull.SetXTitle(self._basicCount.getReader().getFactorisationCaptions()[myDim])
            hCFull.SetYTitle("NQCD")
            hCFull.SetMaximum(1.0)
            for i in range(0, myBinDimensions[myDim]):
                myResult = self.getContracted1DNQCDForBin(i, myDim)
                self._contractedNQCD[myDim].add(myResult)
                hCStat.SetBinContent(i+1, myResult.value())
                hCStat.SetBinError(i+1, myResult.uncertainty())
                hCFull.SetBinContent(i+1, myResult.value())
                hCFull.SetBinError(i+1, myResult.totalUncertainty())
                hCStat.GetXaxis().SetBinLabel(i+1,self._basicCount.getReader().getFactorisationRanges()[myDim][i])
                hCFull.GetXaxis().SetBinLabel(i+1,self._basicCount.getReader().getFactorisationRanges()[myDim][i])
            self._nQCDHistograms.append(hCStat)
            self._nQCDHistograms.append(hCFull)

    def _createYieldTable(self):
        myOutput = ""
        for i in range(1,self._basicCount.getNbinsX()+1):
            for k in range(1,self._basicCount.getNbinsZ()+1):
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
                myPtCaption += "& \\multicolumn{3}{c}{%s \\GeVc}"%(self._basicCount.getBinLabel("X",i).replace("<","$<$").replace(">","$>$"))
                for j in range(1,self._basicCount.getNbinsY()+1):
                    myTableStructure += "l"
                    myEtaCaption += "& \multicolumn{1}{c}{%s}"%(self._basicCount.getBinLabel("Y",j).replace("<","$<$").replace(">","$>$"))
                    myBasicDataRow += "& %.1f $\\pm$ %.1f"%(self._basicCount.getDataCount(i,j,k),self._basicCount.getDataError(i,j,k))
                    myBasicEWKRow += "& %.1f $\\pm$ %.1f $\\pm$ %.1f"%(self._basicCount.getMCCount(i,j,k),self._basicCount.getMCStatError(i,j,k),self._basicCount.getMCCount(i,j,k)*self.getEWKMCRelativeSystematicUncertainty(i))
                    myPurity = self._basicCount.getPurity(i,j,k)
                    myBasicPurityRow += "& %.2f $\\pm$ %.2f"%(myPurity.value(),myPurity.uncertainty())
                    myMetDataRow += "& %.1f $\\pm$ %.1f"%(self._leg1Counts.getDataCount(i,j,k),self._leg1Counts.getDataError(i,j,k))
                    myMetEWKRow += "& %.1f $\\pm$ %.1f $\\pm$ %.1f"%(self._leg1Counts.getMCCount(i,j,k),self._leg1Counts.getMCStatError(i,j,k),self._leg1Counts.getMCCount(i,j,k)*self.getEWKMCRelativeSystematicUncertainty(i))
                    myPurity = self._leg1Counts.getPurity(i,j,k)
                    myMetPurityRow += "& %.2f $\\pm$ %.2f"%(myPurity.value(),myPurity.uncertainty())
                    myTauDataRow += "& %.1f $\\pm$ %.1f"%(self._leg2Counts.getDataCount(i,j,k),self._leg2Counts.getDataError(i,j,k))
                    myTauEWKRow += "& %.1f $\\pm$ %.1f $\\pm$ %.1f"%(self._leg2Counts.getMCCount(i,j,k),self._leg2Counts.getMCStatError(i,j,k),self._leg2Counts.getMCCount(i,j,k)*self.getEWKMCRelativeSystematicUncertainty(i))
                    myPurity = self._leg2Counts.getPurity(i,j,k)
                    myTauPurityRow += "& %.2f $\\pm$ %.2f"%(myPurity.value(),myPurity.uncertainty())
                    myMetEfficiency = self.getLeg1Efficiency(i,j,k)
                    myMetEffRow += "& %.3f $\\pm$ %.3f"%(myMetEfficiency.value(),myMetEfficiency.uncertainty())
                    myNQCD = self.getNQCDForBin(i,j,k)
                    myNQCDRow += "& %.1f $\\pm$ %.1f $\\pm$ %.1f"%(myNQCD[0],sqrt(pow(myNQCD[1],2)+pow(myNQCD[2],2)),myNQCD[3])
                # Construct table
                if k % 2 == 1: # FIXME assumed 2 bins for eta
                    myOutput += "\\renewcommand{\\arraystretch}{1.2}\n"
                    myOutput += "\\begin{table}[ht!]\n"
                    myOutput += "\\caption{Analytical breakdown of the \\NQcd estimate, showing the number of data and EWK MC events and\n"
                    myOutput += "  the purity of the sample after standard selections, after basic selections plus \\MET+btag+$\\Delta\\phi$, and\n"
                    myOutput += "  after all preselections. The efficiency of \\MET+btag+$\\Delta\\phi$ relative to basic selections and \n"
                    myOutput += "  the estimate for the number of QCD multi-jet events in the signal region (\\NQcd) are shown.\n"
                    myOutput += "  The numbers are shown for tau candidate \\pT bin %s \\GeVc.\n"%(self._basicCount.getBinLabel("X",i).replace("<","$<$").replace(">","$>$"))
                    myOutput += "  The top table is for $N_{\\text{vertices}} < 8$,\n" #FIXME assumed 2 bins for eta
                    myOutput += "  whereas the bottom table is for $N_{\\text{vertices}} \geq 8$.\n"
                    myOutput += "  Wherever appropriate, the systematic uncertainty is shown in addition to the statistical uncertainty. } \n"
                    myOutput += "\\label{tab:background:qcdfact:evtyield:bin%d}\n"%(i)
                    myOutput += "\\vspace{1cm}\n"
                    myOutput += "%% NQCD analytical breakdown for tau pT bin %s and Nvtx bin = %s\n"%(self._basicCount.getBinLabel("X",i).replace("<","$<$").replace(">","$>$"),self._basicCount.getBinLabel("Z",k).replace("<","$<$").replace(">","$>$"))
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
        myTableStructure = ""
        myBasicDataRow = ""
        myBasicEWKRow = ""
        myBasicPurityRow = ""
        myMetDataRow = ""
        myMetEWKRow = ""
        myMetPurityRow = ""
        myTauDataRow = ""
        myTauEWKRow = ""
        myTauPurityRow = ""
        myMetEffRow = ""
        myNQCDRow = ""
        myPtCaption = ""
        myOutput = ""
        for i in range(1,self._basicCount.getNbinsX()+1):
            if (i-1) % 4 == 0:
                myOutput += "\\renewcommand{\\arraystretch}{1.2}\n"
                myOutput += "\\begin{table}[ht!]\n"
                myOutput += "\\caption{Analytical breakdown of the \\NQcd estimate for tau candidate \\pT range X-X \\GeVc, showing the number of data and EWK MC events and\n"
                myOutput += "  the purity of the sample after standard selections, after basic selections plus \\MET+btag+$\\Delta\\phi$, and\n"
                myOutput += "  after all preselections. The efficiency of \\MET+btag+$\\Delta\\phi$ relative to basic selections and \n"
                myOutput += "  the estimate for the number of QCD multi-jet events in the signal region (\\NQcd) are shown.\n"
                myOutput += "  The bins of tau candidate $\\eta$ and $N_{\\text{vertices}}$ have been summed up.\n"
                myOutput += "  Wherever appropriate, the systematic uncertainty is shown in addition to the statistical uncertainty. } \n"
                myOutput += "\\label{tab:background:qcdfact:evtyield:tauptonly%d}\n"%((i-1)/4+1)
                myOutput += "\\vspace{1cm}\n"
            if (i-1) % 2 == 0:
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
            myPtCaption += "& %s \\GeVc"%(self._basicCount.getBinLabel("X",i).replace("<","$<$").replace(">","$>$"))
            myTableStructure += "l"
            myBasicDataRow += "& %.1f $\\pm$ %.1f"%(self._basicCount.getContracted1DDataCount(i,"X"),self._basicCount.getContracted1DDataError(i,"X"))
            myBasicEWKRow += "& %.1f $\\pm$ %.1f $\\pm$ %.1f"%(self._basicCount.getContracted1DMCCount(i,"X"),self._basicCount.getContracted1DMCStatError(i,"X"),self._basicCount.getContracted1DMCCount(i,"X")*self.getEWKMCRelativeSystematicUncertainty(i))
            myPurity = self._basicCount.getContracted1DPurity(i,"X")
            myBasicPurityRow += "& %.3f $\\pm$ %.3f"%(myPurity.value(),myPurity.uncertainty())
            myMetDataRow += "& %.1f $\\pm$ %.1f"%(self._leg1Counts.getContracted1DDataCount(i,"X"),self._leg1Counts.getContracted1DDataError(i,"X"))
            myMetEWKRow += "& %.1f $\\pm$ %.1f $\\pm$ %.1f"%(self._leg1Counts.getContracted1DMCCount(i,"X"),self._leg1Counts.getContracted1DMCStatError(i,"X"),self._leg1Counts.getContracted1DMCCount(i,"X")*self.getEWKMCRelativeSystematicUncertainty(i))
            myPurity = self._leg1Counts.getContracted1DPurity(i,"X")
            myMetPurityRow += "& %.2f $\\pm$ %.2f"%(myPurity.value(),myPurity.uncertainty())
            myTauDataRow += "& %.1f $\\pm$ %.1f"%(self._leg2Counts.getContracted1DDataCount(i,"X"),self._leg2Counts.getContracted1DDataError(i,"X"))
            myTauEWKRow += "& %.1f $\\pm$ %.1f $\\pm$ %.1f"%(self._leg2Counts.getContracted1DMCCount(i,"X"),self._leg2Counts.getContracted1DMCStatError(i,"X"),self._leg2Counts.getContracted1DMCCount(i,"X")*self.getEWKMCRelativeSystematicUncertainty(i))
            myPurity = self._leg2Counts.getContracted1DPurity(i,"X")
            myTauPurityRow += "& %.2f $\\pm$ %.2f"%(myPurity.value(),myPurity.uncertainty())
            myMetEfficiency = self.getContracted1DLeg1Efficiency(i,"X")
            myMetEffRow += "& %.4f $\\pm$ %.4f"%(myMetEfficiency.value(),myMetEfficiency.uncertainty())
            myNQCD = self.getContracted1DNQCDForBin(i,"X")
            myNQCDRow += "& %.1f $\\pm$ %.1f $\\pm$ %.1f"%(myNQCD[0],sqrt(pow(myNQCD[1],2)+pow(myNQCD[2],2)),myNQCD[3])
            # Construct table
            if i % 2 == 0:
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
                if i % 4 != 0:
                    myOutput += "\\\\ \n"
                    myOutput += "\\\\ \n"
            if i % 4 == 0:
                myOutput += "\\end{table}\n"
                myOutput += "\\renewcommand{\\arraystretch}{1.0}\n"
                myOutput += "\\newpage\n\n"
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
        # Calculate result of NQCD
        myQCDCalculator = QCDfactorisedCalculator(myStdSelEventCount, myMETLegEventCount, myTauLegEventCount, False) # FIXME set to True
        if False:
            # FIXME
            self._yieldTable = myQCDCalculator.getYieldTable()
            self._compactYieldTable = myQCDCalculator.getCompactYieldTable()
            self._infoHistograms.extend(myQCDCalculator.getNQCDHistograms())
            # Make efficiency histograms
            self._infoHistograms.extend(myQCDCalculator.getLeg1EfficiencyHistogram())
            self._infoHistograms.extend(myQCDCalculator.getLeg2EfficiencyHistogram())
        # Print result
        print "... NQCD = %f +- %f (stat.) +- %f (syst.)  (data stat=%f, MC EWK stat=%f)"%(myQCDCalculator.getNQCD().value(),myQCDCalculator.getNQCD().uncertainty(),myQCDCalculator.getNQCD().systUncertainty(),myQCDCalculator.getNQCD()._dataUncert.uncertainty(),myQCDCalculator.getNQCD()._mcUncert.uncertainty())
        contractedResults = myQCDCalculator.getContractedNQCDList()
        for i in range(0,len(contractedResults)):
            print "... Contracted NQCD for axis %d = %f +- %f (%% stat.) +- %f (%% syst.)  (data stat=%f, MC EWK stat=%f)"%(i, contractedResults[i].value(),contractedResults[i].uncertainty(),contractedResults[i].systUncertainty(),contractedResults[i]._dataUncert.uncertainty(),contractedResults[i]._mcUncert.uncertainty())
        # Make shape histogram
        myRateHistograms=[]
        if False:
            print "... Calculating shape (looping over %d histograms)..."%myStdSelEventCount.getTotalDimension()
            myRateHistograms=[]
            hRateShape = self._createShapeHistogram(config, dsetMgr, myQCDCalculator, myStdSelEventCount, luminosity,
                                                    config.ShapeHistogramsDimensions, self._label, self._dirPrefix, self._basicMtHisto,
                                                    saveDetailedInfo=True, makeCorrectionToShape=True) 
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
                                           myQCDCalculator.getNQCD(),
                                           myRateHistograms)
        return
        # Make validation shapes
        print "... Producing validation histograms ..."
        for METshape in self._validationMETShapeSource:
            self._createValidationHistograms(config,dsetMgr,myQCDCalculator,myStdSelEventCount,luminosity,self._validationMETShapeDetails,
                                             "METvalidation", self._dirPrefix, METshape)
        for mTshape in self._validationMtShapeSource:
            self._createValidationHistograms(config,dsetMgr,myQCDCalculator,myStdSelEventCount,luminosity,self._validationMtShapeDetails,
                                             "mTvalidation", self._dirPrefix, mTshape)
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
                        hShape = self._createShapeHistogram(config, dsetMgr, myQCDCalculator, myStdSelEventCount, luminosity,
                                                            c.details, c.title, self._dirPrefix+"/"+c.QCDFactHistoPath, c.QCDFactHistoName)
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
                    myFullHistoName = self._dirPrefix+"/%s_%d_%d_%d"%(self._METCorrectionDetails["source"],i,j,k)
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

    def _createShapeHistogram(self, config, dsetMgr, QCDCalculator, QCDCount, luminosity, histoSpecs, title, histoDir, histoName, saveDetailedInfo=False, makeCorrectionToShape=False):
        # Create empty shape histogram
        myShapeModifier = ShapeHistoModifier(histoSpecs)
        h = myShapeModifier.createEmptyShapeHistogram(title)
        # Obtain bin dimensions
        nbinsY = 1
        if QCDCount.is2D() or QCDCount.is3D():
            nbinsY = QCDCount.getNbinsY()
        nbinsZ = 1
        if QCDCount.is3D():
            nbinsZ = QCDCount.getNbinsZ()
        # Create info histogram with all info in one
        myName = "QCDFact_ShapeSummary_%s_Total"%title
        hTot = ROOT.TH2F(myName,myName,h.GetNbinsX()*QCDCount.getNbinsY(),0,h.GetNbinsX()*QCDCount.getNbinsY(),QCDCount.getNbinsX()*QCDCount.getNbinsZ(),0,QCDCount.getNbinsX()*QCDCount.getNbinsZ())
        hTot.SetZTitle("Events")
        # Setup axis titles for total histogram
        for i in range(1,h.GetNbinsX()+1):
            for j in range(1,nbinsY+1):
                if i == h.GetNbinsX()+1:
                    hTot.GetXaxis().SetBinLabel(i+(j-1)*h.GetNbinsX(), "(>%d; "%(h.GetXaxis().GetBinUpEdge(i))+QCDCount.getBinLabel("Y",j))
                else:
                    hTot.GetXaxis().SetBinLabel(i+(j-1)*h.GetNbinsX(), "(%d-%d; "%(h.GetXaxis().GetBinLowEdge(i),h.GetXaxis().GetBinUpEdge(i))+QCDCount.getBinLabel("Y",j))
        for i in range(1,QCDCount.getNbinsX()+1):
            for k in range(1,nbinsZ+1):
                hTot.GetYaxis().SetBinLabel(k+(i-1)*nbinsZ, "("+QCDCount.getBinLabel("X",i)+";"+QCDCount.getBinLabel("Z",k))
        # Loop over bins
        for i in range(1,QCDCount.getNbinsX()+1):
            myName = "QCDFact_ShapeSummary_%s_ContractedX_bin_%d"%(title,i)
            hTotContractedX = myShapeModifier.createEmptyShapeHistogram(myName)
            myName = "QCDFact_ShapeSummary_%s_ContractedXContractedEff_bin_%d"%(title,i)
            hTotContractedXeff = myShapeModifier.createEmptyShapeHistogram(myName)
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
                        myFullHistoName = self._dirPrefix+"/%s_%d_%d_%d"%(self._MTCorrectionDetails["source"],i,j,k)
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
