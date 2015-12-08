## \package Extractor
# Classes for extracting observation/rate/nuisance from datasets
#
#

from HiggsAnalysis.NtupleAnalysis.tools.counter import EventCounter
import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
from HiggsAnalysis.NtupleAnalysis.tools.systematics import ScalarUncertaintyItem,getBinningForPlot
import HiggsAnalysis.QCDMeasurement.systematicsForMetShapeDifference as systematicsForMetShapeDifference
import HiggsAnalysis.NtupleAnalysis.tools.ShellStyles as ShellStyles
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux
import HiggsAnalysis.NtupleAnalysis.tools.histogramsExtras as histogramsExtras
from math import pow,sqrt
import sys
import json
import os
import ROOT
from array import array

## QCD specific method for extracting purity for a shape
def _calculateAverageQCDPurity(shapeHisto, purityHisto):
    # Calculated weighted average (weight = Nevents in the shape)
    mySum = 0.0
    myTotalWeight = 0.0
    for i in range(0,purityHisto.GetNbinsX()+1):
        mySum += purityHisto.GetBinContent(i) * shapeHisto.GetBinContent(i)
        myTotalWeight += shapeHisto.GetBinContent(i)
    if abs(myTotalWeight) < 0.00001:
        return 0.0
    else:
        return mySum / myTotalWeight


# Enumerator class for data mining mode
class ExtractorMode:
    UNKNOWN = 0
    OBSERVATION = 1
    RATE = 2
    NUISANCE = 3
    ASYMMETRICNUISANCE = 4
    SHAPENUISANCE = 5
    QCDNUISANCE = 6
    CONTROLPLOT = 7

## ExtractorBase class
class ExtractorBase:
    ## Constructor
    def __init__(self, mode, exid, distribution, description, opts=None, scaleFactor = 1.0):
        self._mode = mode
        self._isPrintable = True
        self._exid = exid
        self._distribution = distribution
        self._description = description
        self._opts = opts
        self._scaleFactor = scaleFactor
        self._extractablesToBeMerged = []
        self._masterExID = exid
        if self._scaleFactor == None:
            self._scaleFactor = 1.0
        if abs(self._scaleFactor - 1.0) > 0.00001:
            print ShellStyles.WarningLabel()+"Scaling nuisance parameter %s by factor %f"%(self._exid, self._scaleFactor)

    ## Returns true if extractable mode is observation
    def isObservation(self):
        return self._mode == ExtractorMode.OBSERVATION

    ## Returns true if extractable mode is rate
    def isRate(self):
        return self._mode == ExtractorMode.RATE

    ## Returns true if extractable mode is any type of nuisance
    def isAnyNuisance(self):
        return self._mode == ExtractorMode.NUISANCE or \
               self._mode == ExtractorMode.ASYMMETRICNUISANCE or \
               self._mode == ExtractorMode.SHAPENUISANCE or \
               self._mode == ExtractorMode.QCDNUISANCE

    ## Returns true if extractable mode is nuisance
    def isNuisance(self):
        return self._mode == ExtractorMode.NUISANCE

    ## Returns true if extractable mode is nuisance with asymmetric limits
    def isAsymmetricNuisance(self):
        return self._mode == ExtractorMode.ASYMMETRICNUISANCE

    ## Returns true if extractable mode is shape nuisance
    def isShapeNuisance(self):
        return self._mode == ExtractorMode.SHAPENUISANCE

    ## Returns true if extractable mode is QCD nuisance
    def isQCDNuisance(self):
        return self._mode == ExtractorMode.QCDNUISANCE

    ## Returns the scale factor (used for projection estimates)
    def getScaleFactor(self):
        return self._scaleFactor

    ## True if nuisance will generate a new line in output (i.e. is not merged)
    def isPrintable(self):
        return self._isPrintable

    ## True if the id of the current extractable or it's master is the same as the asked one
    def isId(self, exid):
        return self._exid == exid or self._masterExID == exid

    ## Returns id of master
    def getMasterId(self):
        return self._masterExID

    ## Returns id
    def getId(self):
        return self._exid

    ## Returns distribution string
    def getDistribution(self):
        return self._distribution

    ## Returns description string
    def getDescription(self):
        return self._description

    ## Adds extractable to list of extractables to be merged
    def addExtractorToBeMerged(self, extractable):
        self._extractablesToBeMerged.append(extractable)
        extractable.setAsSlave(self._exid)

    ## Disables printing of extractable and sets id of master 
    def setAsSlave(self, masterId):
        self._isPrintable = False
        self._masterExID = masterId

    ## Returns the counter histogram
    def getCounterHistogram(self, rootFile, counterHisto):
        histo = rootFile.Get(counterHisto)
        if not histo:
            raise Exception(ErrorStyle()+"Error:"+ShellStyles.NormalStyle()+" Cannot find counter histogram '"+counterHisto+"'!")
        return histo

    ## Returns index to bin corresponding to first matching label in a counter histogram
    def getCounterItemIndex(self, histo, counterItem):
        for i in range(1, histo.GetNbinsX()+1):
            if histo.GetXaxis().GetBinLabel(i) == myBinLabel:
                return i
        raise Exception(ErrorStyle()+"Error:"+ShellStyles.NormalStyle()+" Cannot find counter by name "+counterItem+"!")

    ## Virtual method for extracting information
    def extractResult(self, datasetColumn, dsetMgr, mainCounterTable, luminosity, additionalNormalisation = 1.0):
        return -1.0

    ## Virtual method for extracting additional information (returns None if not implemented)
    def extractAdditionalResult(self, datasetColumn, dsetMgr, mainCounterTable, luminosity, additionalNormalisation = 1.0):
        return None

    ## Virtual method for extracting histograms
    def extractHistograms(self, datasetColumn, dsetMgr, mainCounterTable, luminosity, additionalNormalisation = 1.0):
        return None

    ## Virtual method for printing debug information
    def printDebugInfo(self):
        print "- mode = ", self._mode
        print "- extractable ID = ", self._exid
        if self.isAnyNuisance():
            print "- distribution = ", self._distribution
            print "- description = ", self._description
            print "- scale factor = ", self._scaleFactor
            if not self.isPrintable():
                print "- is slave of extractable with ID = ", self._masterExID

    # obsolete methods ?
    # double getMergedValue(std::vector< Dataset* > datasets, NormalisationInfo* info, double hostValue); // Returns first non zero value

    ## \var _mode
    # Enumerator for data mining mode
    ## \var _distribution
    # string keyword of distribution (usually lnN, see LandS manual for more options)
    ## \var _exid
    # Unique ID (string) of the extractable
    ## \var _description
    # string for describing a nuisance parameter
    ## \var _extractablesToBeMerged
    # list of extractables whose results are to be merged to this one (practically an or function or extractables)
    ## \var _isPrintable
    # if true the extractable will generate a new line in output
    ## \var _masterExID
    # the ID of the master extractable (i.e. specifies line on which this extractable output is printed)

## ConstantExtractor class
# Returns a fixed constant number
class ConstantExtractor(ExtractorBase):
    ## Constructor
    def __init__(self, constantValue, mode, exid = "", distribution = "lnN", description = "", constantUpperValue = 0.0, opts=None, scaleFactor=1.0):
        ExtractorBase.__init__(self, mode, exid, distribution, description, opts=opts, scaleFactor=scaleFactor)
        self._constantValue = None
        if isinstance(constantValue, ScalarUncertaintyItem):
            self._constantValue = constantValue.Clone()
            self._constantValue.scale(self._scaleFactor)
        else:
            if self.isAsymmetricNuisance() or constantUpperValue != None:
                self._constantValue = ScalarUncertaintyItem(exid,plus=constantUpperValue*self._scaleFactor,minus=constantValue*self._scaleFactor)
            else:
                self._constantValue = ScalarUncertaintyItem(exid,constantValue*self._scaleFactor)

    ## Method for extracking information
    def extractResult(self, datasetColumn, dsetMgr, mainCounterTable, luminosity, additionalNormalisation = 1.0):
        return self._constantValue

    ## Virtual method for printing debug information
    def printDebugInfo(self):
        print "ConstantExtractor"
        print "- value = + %f - %f"%(self._constantValue.getUncertaintyUp,self._constantValue.getUncertaintyDown)
        ExtractorBase.printDebugInfo(self)

    ## \var _constantValue
    # ScalarUncertaintyItem containting the uncertainty

## ConstantExtractor class
# Returns a fixed constant number
class ConstantExtractorForDataDrivenQCD(ExtractorBase):
    ## Constructor
    def __init__(self, constantValue, mode, exid = "", distribution = "lnN", description = "", constantUpperValue = 0.0, opts=None, scaleFactor=1.0):
        ExtractorBase.__init__(self, mode, exid, distribution, description, opts=opts, scaleFactor=scaleFactor)
        self._constantValue = None
        if isinstance(constantValue, ScalarUncertaintyItem):
            self._constantValue = constantValue.Clone()
            self._constantValue.scale(self._scaleFactor)
        else:
            if self.isAsymmetricNuisance() or constantUpperValue != None:
                self._constantValue = ScalarUncertaintyItem(exid,plus=constantUpperValue*self._scaleFactor,minus=constantValue*self._scaleFactor)
            else:
                self._constantValue = ScalarUncertaintyItem(exid,constantValue*self._scaleFactor)
        # Flip sign
        self._constantValue.scale(-1.0)

    ## Method for extracking information
    def extractResult(self, datasetColumn, dsetMgr, mainCounterTable, luminosity, additionalNormalisation = 1.0):
        return self._constantValue

    ## Virtual method for printing debug information
    def printDebugInfo(self):
        print "ConstantExtractorForDataDrivenQCD"
        print "- value = + %f - %f"%(self._constantValue.getUncertaintyUp,self._constantValue.getUncertaintyDown)
        ExtractorBase.printDebugInfo(self)

    ## \var _constantValue
    # ScalarUncertaintyItem containting the uncertainty

## CounterExtractor class
# Extracts a value from a given counter in the list of main counters
class CounterExtractor(ExtractorBase):
    ## Constructor
    def __init__(self, counterItem, mode, exid = "", distribution = "lnN", description = "", opts=None, scaleFactor=1.0):
        ExtractorBase.__init__(self, mode, exid, distribution, description, opts=opts, scaleFactor=scaleFactor)
        self._counterItem = counterItem

    ## Method for extracking information
    def extractResult(self, datasetColumn, dsetMgr, mainCounterTable, luminosity, additionalNormalisation = 1.0):
        myCount = mainCounterTable.getCount(rowName=self._counterItem, colName=datasetColumn.getDatasetMgrColumn())
        # Return result
        myResult = None
        if self.isRate() or self.isObservation():
            myResult = myCount.value() * additionalNormalisation
            if additionalNormalisation != 1.0 and self.isRate():
                print "      (normalisation applied) rate = %f, rate*normalisation = %f"%(myCount.value(),myResult)
        elif self.isNuisance():
            # protection against zero
            if myCount.value() == 0:
                print ShellStyles.WarningLabel()+" In Nuisance with id='"+self._exid+"' for column '"+datasetColumn.getLabel()+"' counter ('"+self._counterItem+"') value is zero!"
                myResult = ScalarUncertaintyItem(self._exid,0.0)
            else:
                myResult = ScalarUncertaintyItem(self._exid,myCount.uncertainty() / myCount.value()*self._scaleFactor)
        return myResult

    ## Virtual method for printing debug information
    def printDebugInfo(self):
        print "CounterExtractor"
        print "- counter item = ", self._counterItem
        ExtractorBase.printDebugInfo(self)

    ## \var _counterItem
    # Name of item (label) in counter histogram

## MaxCounterExtractor class
# Extracts a value from a given counter item in the list of main counters and compares it to the reference value
# Largest deviation from the reference (nominal) value is taken
class MaxCounterExtractor(ExtractorBase):
    ## Constructor
    def __init__(self, counterDirs, counterItem, mode, exid = "", distribution = "lnN", description = "", opts=None, scaleFactor=1.0):
        ExtractorBase.__init__(self, mode, exid, distribution, description, opts=opts, scaleFactor=scaleFactor)
        self._counterItem = counterItem
        self._counterDirs = counterDirs
        if len(self._counterDirs) < 2:
            raise Exception(ErrorStyle()+"Error in Nuisance with id='"+self._exid+"':"+ShellStyles.NormalStyle()+" need to specify at least two directories for counters!")

    ## Method for extracking information
    def extractResult(self, datasetColumn, dsetMgr, mainCounterTable, luminosity, additionalNormalisation = 1.0):
        myResult = []
        for d in self._counterDirs:
            myHistoPath = d+"/weighted/counter"
            try:
                datasetRootHisto = dsetMgr.getDataset(datasetColumn.getDatasetMgrColumn()).getDatasetRootHisto(myHistoPath)
            except Exception, e:
                raise Exception (ErrorStyle()+"Error in extracting max counter value:"+ShellStyles.NormalStyle()+" cannot find histogram!\n  Column = %s\n  NuisanceId = %s\n  Message = %s!"%(datasetColumn.getLabel(),self._exid, str(e)))
            datasetRootHisto.normalizeToLuminosity(luminosity)
            myHisto = datasetRootHisto.getHistogram()
            counterList = dataset._histoToCounter(myHisto)
            myHisto.IsA().Destructor(myHisto)
            myFoundStatus = False # to ensure that the first counter of given name is taken
            for name, count in counterList:
                if name == self._counterItem and not myFoundStatus:
                    myResult.append(count)
                    myFoundStatus = True
            if not myFoundStatus:
                raise Exception(ErrorStyle()+"Error in Nuisance with id='"+self._exid+"' for column '"+datasetColumn.getLabel()+"':"+ShellStyles.NormalStyle()+" Cannot find counter name '"+self._counterItem+"' in histogram '"+myHistoPath+"'!")
        # Loop over results
        myMaxValue = 0.0
        # Protect for div by zero
        if myResult[0].value() == 0:
            print ShellStyles.WarningLabel()+" In Nuisance with id='"+self._exid+"' for column '"+datasetColumn.getLabel()+"' nominal counter ('"+self._counterItem+"')value is zero!"
        else:
            for i in range(1,len(myResult)):
                myValue = abs(myResult[i].value() / myResult[0].value() - 1.0)
                if (myValue > myMaxValue):
                    myMaxValue = myValue
        return ScalarUncertaintyItem(self._exid,myMaxValue*self._scaleFactor)

    ## Virtual method for printing debug information
    def printDebugInfo(self):
        print "MaxCounterExtractor"
        print "- counter item = ", self._counterItem
        ExtractorBase.printDebugInfo(self)

    ## \var _counterDirs
    # List of directories (without /weighted/counter suffix ) for counter histograms; first needs to be the nominal counter
    ## \var _counterItem
    # Name of item (label) in counter histogram

## PileupUncertaintyExtractor class
# Extracts counter values after selection for nominal case and up/down variations and returns the max. deviation from the nominal, i.e. max(up/nominal, down/nominal)
#class PileupUncertaintyExtractor(ExtractorBase):
    ### Constructor
    #def __init__(self, counterDirs, counterItem, mode, exid = "", distribution = "lnN", description = "", opts=None):
        #ExtractorBase.__init__(self, mode, exid, distribution, description, opts=opts)
        #self._counterItem = counterItem
        #self._counterDirs = counterDirs
        #if len(self._counterDirs) < 2:
            #raise Exception(ErrorStyle()+"Error in Nuisance with id='"+self._exid+"':"+ShellStyles.NormalStyle()+" need to specify at least two directories for counters!")

    ### Method for extracking information
    #def extractResult(self, datasetColumn, dsetMgr, mainCounterTable, luminosity, additionalNormalisation = 1.0):
        #myResult = []

        ## Normalise with up/down to get up/down histograms
        ## mgr.updateNAllEventsToPUWeighted(weightType=PileupWeightType.UP) #FIXME
        ## mgr.updateNAllEventsToPUWeighted(weightType=PileupWeightType.DOWN) #FIXME
        #for d in self._counterDirs:
            #myHistoName = d+"/counters/weighted/counter"
            #try:
                #datasetRootHisto = dsetMgr.getDataset(datasetColumn.getDatasetMgrColumn()).getDatasetRootHisto(myHistoName)
            #except Exception, e:
                #raise Exception (ErrorStyle()+"Error in extracting PU uncertainty:"+ShellStyles.NormalStyle()+" cannot find histogram!\n  Column = %s\n  NuisanceId = %s\n  Message = %s!"%(datasetColumn.getLabel(),self._exid, str(e)))
            #datasetRootHisto.normalizeToLuminosity(luminosity)
            #myHisto = datasetRootHisto.getHistogram()
            #counterList = dataset._histoToCounter(myHisto)
            #myHisto.IsA().Destructor(myHisto)
            #myFoundStatus = False # to ensure that the first counter of given name is taken
            #for name, count in counterList:
                #if name == self._counterItem and not myFoundStatus:
                    #myResult.append(count)
                    #myFoundStatus = True
            #if not myFoundStatus:
                #raise Exception(ErrorStyle()+"Error in Nuisance with id='"+self._exid+"' for column '"+datasetColumn.getLabel()+"':"+ShellStyles.NormalStyle()+" Cannot find counter name '"+self._counterItem+"' in histogram '"+myHistoName+"'!")
        ## Revert back to nominal normalisation
        ## mgr.updateNAllEventsToPUWeighted(weightType=PileupWeightType.NOMINAL) #FIXME
        ## Loop over results
        #myMaxValue = 0.0
        ## Protect for div by zero
        #if myResult[0].value() == 0:
            #print ShellStyles.WarningLabel()+" In Nuisance with id='"+self._exid+"' for column '"+datasetColumn.getLabel()+"' nominal counter ('"+self._counterItem+"')value is zero!"
        #else:
            #for i in range(1,len(myResult)):
                #myValue = abs(myResult[i].value() / myResult[0].value() - 1.0)
                #if (myValue > myMaxValue):
                    #myMaxValue = myValue
        #return myMaxValue

    ### Virtual method for printing debug information
    #def printDebugInfo(self):
        #print "MaxCounterExtractor"
        #print "- counter item = ", self._counterItem
        #ExtractorBase.printDebugInfo(self)

    ### \var _counterDirs
    ## List of directories (without /weighted/counter suffix ) for counter histograms; first needs to be the nominal counter
    ### \var _counterItem
    ## Name of item (label) in counter histogram


## RatioExtractor class
# Extracts two values from two counter items in the list of main counters and returns th ratio of these scaled by some factor
class RatioExtractor(ExtractorBase):
    ## Constructor
    def __init__(self, scale, numeratorCounterItem, denominatorCounterItem, mode, exid = "", distribution = "lnN", description = "", opts=None, scaleFactor=1.0):
        ExtractorBase.__init__(self, mode, exid, distribution, description, opts=opts, scaleFactor=scaleFactor)
        self._numeratorCounterItem = numeratorCounterItem
        self._denominatorCounterItem = denominatorCounterItem
        self._scale = scale

    ## Method for extracking information
    def extractResult(self, datasetColumn, dsetMgr, mainCounterTable, luminosity, additionalNormalisation = 1.0):
        myNumeratorCount = mainCounterTable.getCount(rowName=self._numeratorCounterItem, colName=datasetColumn.getDatasetMgrColumn())
        myDenominatorCount = mainCounterTable.getCount(rowName=self._denominatorCounterItem, colName=datasetColumn.getDatasetMgrColumn())
        # Protection against div by zero
        if myNumeratorCount.value() == 0.0:
            print ShellStyles.WarningLabel()+" In Nuisance with id='"+self._exid+"' for column '"+datasetColumn.getLabel()+"' denominator counter ('"+self._numeratorCounterItem+"') value is zero!"
            myResult = 0.0
        else:
            myResult = (myDenominatorCount.value() / myNumeratorCount.value() - 1.0) * self._scale
        # Return result
        return ScalarUncertaintyItem(self._exid,myResult*self._scaleFactor)

    ## Virtual method for printing debug information
    def printDebugInfo(self):
        print "RatioExtractor"
        print "- numeratorCounterItem = ", self._numeratorCounterItem
        print "- denominatorCounterItem = ", self._denominatorCounterItem
        ExtractorBase.printDebugInfo(self)

    ## \var _numeratorCounterItem
    # Name of item (label) in counter histogram for numerator count
    ## \var _denominatorCounterItem
    # Name of item (label) in counter histogram for denominator count
    ## \var _scale
    # Scaling factor for result (float)

## ScaleFactorExtractor class
# Extracts an uncertainty for a scale factor
class ScaleFactorExtractor(ExtractorBase):
    ## Constructor
    def __init__(self, histoDirs, histograms, normalisation, addSystInQuadrature = 0.0, mode = ExtractorMode.NUISANCE, exid = "", distribution = "lnN", description = "", opts=None, scaleFactor=1.0):
        ExtractorBase.__init__(self, mode, exid, distribution, description, opts=opts, scaleFactor=scaleFactor)
        self._histoDirs = histoDirs
        self._histograms = histograms
        self._normalisation = normalisation
        self._addSystInQuadrature = addSystInQuadrature
        if len(self._histoDirs) != len(self._normalisation) or len(self._histoDirs) != len(self._histograms):
            raise Exception(ErrorStyle()+"Error in Nuisance with id='"+self._exid+"' for column '"+datasetColumn.getLabel()+"':"+ShellStyles.NormalStyle()+" need to specify equal amount of histoDirs, histograms and normalisation histograms!")

    ## Method for extracking information
    def extractResult(self, datasetColumn, dsetMgr, mainCounterTable, luminosity, additionalNormalisation = 1.0):
        myResult = []
        for i in range (0, len(self._histoDirs)):
            myTotal = 0.0
            mySum = 0.0
            myHistoName = self._histoDirs[i]+"/"+self._histograms[i]
            if self._histoDirs[i] == "":
                myHistoName = self._histograms[i]
            try:
                myValueRootHisto = dsetMgr.getDataset(datasetColumn.getDatasetMgrColumn()).getDatasetRootHisto(myHistoName)
            except Exception, e:
                raise Exception (ErrorStyle()+"Error in extracting scale factor uncertainty:"+ShellStyles.NormalStyle()+" cannot find value histogram!\n  Column = %s\n  NuisanceId = %s\n  Message = %s!"%(datasetColumn.getLabel(),self._exid, str(e)))
            myValueRootHisto.normalizeToLuminosity(luminosity)
            hValues = myValueRootHisto.getHistogram()
            if hValues == None:
                raise Exception(ErrorStyle()+"Error in Nuisance with id='"+self._exid+"' for column '"+datasetColumn.getLabel()+"':"+ShellStyles.NormalStyle()+" Cannot open histogram '"+myHistoName+"'!")
            myHistoName = self._histoDirs[i]+"/"+self._normalisation[i]
            try:
                myNormalisationRootHisto = dsetMgr.getDataset(datasetColumn.getDatasetMgrColumn()).getDatasetRootHisto(myHistoName)
            except Exception, e:
                raise Exception (ErrorStyle()+"Error in extracting scale factor uncertainty:"+ShellStyles.NormalStyle()+" cannot find normalisation histogram!\n  Column = %s\n  NuisanceId = %s\n  Message = %s!"%(datasetColumn.getLabel(),self._exid, str(e)))
            myNormalisationRootHisto.normalizeToLuminosity(luminosity)
            hNormalisation = myNormalisationRootHisto.getHistogram()
            if hNormalisation == None:
                raise Exception(ErrorStyle()+"Error in Nuisance with id='"+self._exid+"' for column '"+datasetColumn.getLabel()+"':"+ShellStyles.NormalStyle()+" Cannot open histogram '"+myHistoName+"'!")
            for j in range (1, hValues.GetNbinsX()+1):
                mySum += pow(hValues.GetBinContent(j) * hValues.GetBinCenter(j),2)
            myTotal = hNormalisation.GetBinContent(1)
            hValues.IsA().Destructor(hValues)
            hNormalisation.IsA().Destructor(hNormalisation)
            # Calculate result, protection against div by zero
            if myTotal == 0.0:
                print ShellStyles.WarningLabel()+" In Nuisance with id='"+self._exid+"' for column '"+datasetColumn.getLabel()+"' total count from normalisation histograms is zero!"
                myResult.append(0.0)
            else:
                myResult.append(sqrt(mySum) / myTotal)
        # Combine result
        myCombinedResult = 0.0
        for i in range (0, len(self._histoDirs)):
            myCombinedResult += pow(myResult[i], 2)
        myCombinedResult += pow(self._addSystInQuadrature, 2)
        # Return result
        return ScalarUncertaintyItem(self._exid,sqrt(myCombinedResult)*self._scaleFactor)


    ## Virtual method for printing debug information
    def printDebugInfo(self):
        print "MaxCounterExtractor"
        print "- counter item = ", self._counterItem
        ExtractorBase.printDebugInfo(self)

    ## \var _counterDirs
    # List of directories (without /weighted/counter suffix ) for counter histograms; first needs to be the nominal counter
    ## \var _counterItem
    # Name of item (label) in counter histogram

## ShapeExtractor class
# Extracts histogram shapes
class ShapeExtractor(ExtractorBase):
    ## Constructor
    def __init__(self, mode = ExtractorMode.SHAPENUISANCE, exid = "", distribution = "", description = "", opts=None, minimumStatUncert=None, minimumRate=0.0, scaleFactor=1.0):
        ExtractorBase.__init__(self, mode, exid, distribution, description, opts=opts, scaleFactor=scaleFactor)
        if not (self.isRate() or self.isObservation()):
            if self._distribution != "shapeStat":
                self.printDebugInfo()
                raise Exception(ShellStyles.ErrorLabel()+"Only shapeStat allowed for the ShapeExtractor!"+ShellStyles.NormalStyle())
        self._minimumStatUncert = minimumStatUncert
        if minimumStatUncert == None:
            self._minimumStatUncert = 0.0
        self._minimumRate = minimumRate

    ## Method for extracking result
    def extractResult(self, datasetColumn, dsetMgr, mainCounterTable, luminosity, additionalNormalisation = 1.0):
        # Tell Lands / Combine that the nuisance is active for the given column, histogram is added to input root file via extractHistograms()
        return 1.0

    ## Virtual method for extracting histograms
    def extractHistograms(self, datasetColumn, dsetMgr, mainCounterTable, luminosity, additionalNormalisation = 1.0):
        myHistograms = []
        # Check that results have been cached
        if datasetColumn.getCachedShapeRootHistogramWithUncertainties() == None:
            raise Exception(ShellStyles.ErrorLabel()+"You forgot to cache rootHistogramWithUncertainties for the datasetColumn before creating extractors for nuisances!"+ShellStyles.NormalStyle())
        # Get histogram from cache
        h = aux.Clone(datasetColumn.getCachedShapeRootHistogramWithUncertainties().getRootHisto())
        myTotalRate = h.Integral()
        rateWillBeSuppressedStatus = myTotalRate < self._minimumRate
        # Do not apply here additional normalization, it has already been applied
        # via RootHistoWithUncertainties.Scale() in DatacardColumn::doDataMining()
        if self.isRate() or self.isObservation():
            # Shape histogram is the result
            h.SetTitle(datasetColumn.getLabel())
            # Append histogram to output list
            myHistograms.append(h)
        else:
            # Ok, it's a nuisance
            # Create up and down histograms for shape stat
            hUp = aux.Clone(h)
            hDown = aux.Clone(h)
            hUp.Reset()
            hDown.Reset()
            hUp.SetTitle(datasetColumn.getLabel()+"_"+self._masterExID+"Up")
            hDown.SetTitle(datasetColumn.getLabel()+"_"+self._masterExID+"Down")
            for k in range(1, h.GetNbinsX()+1):
                if h.GetBinContent(k) + h.GetBinError(k) < self._minimumStatUncert:
                    if not rateWillBeSuppressedStatus:
                        print ShellStyles.WarningLabel()+"Corrected bin %d stat.uncert plus value to %.2f for column '%s' (it was %f)! The value is set by MinimumStatUncertainty flag."%(k, self._minimumStatUncert, datasetColumn.getLabel(), hUp.GetBinContent(k))
                    hUp.SetBinContent(k, self._minimumStatUncert)
                else:
                    hUp.SetBinContent(k, h.GetBinContent(k) + h.GetBinError(k)) # no scaling because this is the stat uncertainty
                if h.GetBinContent(k) - h.GetBinError(k) < 0.000001:
                    if h.GetBinContent(k) < 0.0 and not rateWillBeSuppressedStatus:
                        print ShellStyles.WarningLabel()+"Corrected bin %d stat.uncert minus value to zero for column '%s' (it was %f)!"%(k, datasetColumn.getLabel(), hDown.GetBinContent(k))
                    hDown.SetBinContent(k, 0.0)
                else:
                    hDown.SetBinContent(k, h.GetBinContent(k) - h.GetBinError(k))
            # Append histograms to output list
            myHistograms.append(hUp)
            myHistograms.append(hDown)
            h.Delete()
            #h.IsA().Destructor(h) # Delete the nominal histo
        # Return result
        return myHistograms

    ## QCD specific method for extracting purity histogram
    def extractQCDPurityHistogram(self, datasetColumn, dsetMgr, shapeHistoName):
        # Do not apply here additional normalization, it is not needed
        if not datasetColumn.typeIsQCD:
            raise Exception(ShellStyles.ErrorLabel()+"extractQCDPurityHistogram() called for non-QCD datacolumn '%s'!"%datasetColumn.getLabel())
        if not self.isRate():
            raise Exception(ShellStyles.ErrorLabel()+"extractQCDPurityHistogram() called for nuisance! (only valid for rate)")
        # Obtain purity histogram
        if not dsetMgr.getDataset(datasetColumn.getDatasetMgrColumn()).hasRootHisto(shapeHistoName+"_Purity"):
            raise Exception(ShellStyles.ErrorLabel()+"T1he pseudo-multicrab directory for QCD is outdated! Please regenerate it (with the proper normalization!!!)")
        h = dsetMgr.getDataset(datasetColumn.getDatasetMgrColumn()).getDatasetRootHisto(shapeHistoName+"_Purity")
        return h

    ## QCD specific method for extracting purity for a shape
    def extractQCDPurityAsValue(self, datasetColumn, dsetMgr, shapeHistoName, shapeHisto):
        hPurity = self.extractQCDPurityHistogram(datasetColumn, dsetMgr, shapeHistoName)
        myValue = _calculateAverageQCDPurity(shapeHisto, hPurity)
        hPurity.Delete()
        return myValue

    ## QCD specific method for extracting purity for a shape
    def extractQCDPurityAsValue(self, shapeHisto, purityHisto):
        if isinstance(purityHisto, dataset.DatasetRootHisto):
            return self._calculateAverageQCDPurity(shapeHisto, purityHisto.getHistogram())
        elif isinstance(purityHisto, ROOT.TH1):
            return _calculateAverageQCDPurity(shapeHisto, purityHisto)
        else:
            raise Exception("This should not happen")

    ## Virtual method for printing debug information
    def printDebugInfo(self):
        print "ShapeExtractor"
        ExtractorBase.printDebugInfo(self)

## ShapeVariationExtractor class
# Extracts histogram shapes from up and down variation
class ShapeVariationExtractor(ExtractorBase):
    ## Constructor
    def __init__(self, systVariation, mode = ExtractorMode.SHAPENUISANCE, exid = "", distribution = "shapeQ", description = "", opts=None, scaleFactor=1.0):
        ExtractorBase.__init__(self, mode, exid, distribution, description, opts=opts, scaleFactor=scaleFactor)
        self._systVariation = systVariation
        if not "SystVar" in self._systVariation:
            self._systVariation = "SystVar%s"%self._systVariation
        if self.isRate() or self.isObservation():
            raise Exception(ShellStyles.ErrorLabel()+"Rate or observation not allowed for ShapeVariationExtractor!"+ShellStyles.NormalStyle())

    ## Method for extracking result
    def extractResult(self, datasetColumn, dsetMgr, mainCounterTable, luminosity, additionalNormalisation = 1.0):
        myShapeUncertDict = datasetColumn.getCachedShapeRootHistogramWithUncertainties().getShapeUncertainties()
        if not self._systVariation in myShapeUncertDict.keys():
            return 0.0
        # Tell Lands / Combine that the nuisance is active for the given column, histogram is added to input root file via extractHistograms()
        return 1.0

    ## Virtual method for extracting histograms
    def extractHistograms(self, datasetColumn, dsetMgr, mainCounterTable, luminosity, additionalNormalisation = 1.0):
        # Obsolete
        raise Exception("obsolete")
        myHistograms = []
        # Check that results have been cached
        if datasetColumn.getCachedShapeRootHistogramWithUncertainties() == None:
            raise Exception(ShellStyles.ErrorLabel()+"You forgot to cache rootHistogramWithUncertainties for the datasetColumn before creating extractors for nuisances!"+ShellStyles.NormalStyle())
        # Get uncertainty variation dictionary
        myShapeUncertDict = datasetColumn.getCachedShapeRootHistogramWithUncertainties().getShapeUncertainties()
        # Check that asked variation exists
        if not self._systVariation in myShapeUncertDict.keys():
            raise Exception(ShellStyles.ErrorLabel()+"DatasetColumn '%s': Cannot find systematics variation %s, check that options in the datacard match to multicrab content!"%(datasetColumn.getLabel(),self._systVariation))
        # Get histogram from cache
        (hSystUp, hSystDown) = myShapeUncertDict[self._systVariation]
        hUp = aux.Clone(hSystUp)
        hDown = aux.Clone(hSystDown)
        hUp.SetTitle(datasetColumn.getLabel()+"_"+self._masterExID+"Up")
        hDown.SetTitle(datasetColumn.getLabel()+"_"+self._masterExID+"Down")
        # Do not apply here additional normalization, it has already been applied
        # via RootHistoWithUncertainties.Scale() in DatacardColumn::doDataMining()
        # Append histograms to output list
        myHistograms.append(hUp)
        myHistograms.append(hDown)
        # Return result
        return myHistograms

    ## Virtual method for printing debug information
    def printDebugInfo(self):
        print "ShapeVariationExtractor"
        ExtractorBase.printDebugInfo(self)

## ShapeVariationSeparateShapeAndNormalization class
# Extracts histogram shapes from up and down variation, but separates the shape and normalization to separate lines to datacard
class ShapeVariationSeparateShapeAndNormalization(ExtractorBase):
    ## Constructor
    def __init__(self, systVariation, mode = ExtractorMode.SHAPENUISANCE, exid = "", distribution = "shapeQ", description = "", opts=None, scaleFactor=1.0):
        ExtractorBase.__init__(self, mode, exid, distribution, description, opts=opts, scaleFactor=scaleFactor)
        self._systVariation = systVariation
        if not "SystVar" in self._systVariation:
            self._systVariation = "SystVar%s"%self._systVariation
        if self.isRate() or self.isObservation():
            raise Exception(ShellStyles.ErrorLabel()+"Rate or observation not allowed for ShapeVariationExtractor!"+ShellStyles.NormalStyle())

    ## Method for extracting result
    def extractResult(self, datasetColumn, dsetMgr, mainCounterTable, luminosity, additionalNormalisation = 1.0):
        myShapeUncertDict = datasetColumn.getCachedShapeRootHistogramWithUncertainties().getShapeUncertainties()
        if not self._systVariation in myShapeUncertDict.keys():
            return 0.0
        # Tell Lands / Combine that the nuisance is active for the given column, histogram is added to input root file via extractHistograms()
        return 1.0

    ## Method for extracting additional result
    def extractAdditionalResult(self, datasetColumn, dsetMgr, mainCounterTable, luminosity, additionalNormalisation = 1.0):
        myShapeUncertDict = datasetColumn.getCachedShapeRootHistogramWithUncertainties().getShapeUncertainties()
        if not self._systVariation in myShapeUncertDict.keys():
            print ShellStyles.ErrorLabel()+"Failed to extract systvariation '%s' from column '%s'!"%(self._systVariation,datasetColumn.getLabel())
            print "Available syst.vars.:%s"%", ".join(map(str,myShapeUncertDict.keys()))
            #datasetColumn.getCachedShapeRootHistogramWithUncertainties().Debug()
            raise Exception()
        # Calculate variations from integrals
        (hSystUp, hSystDown) = myShapeUncertDict[self._systVariation]
        myInt = datasetColumn.getCachedShapeRootHistogramWithUncertainties().getRootHisto().Integral()
        myUpValue = hSystUp.Integral() / myInt
        myDownValue = hSystDown.Integral() / myInt
        # Normalize here to same area like in nominal histogram
        myInt = datasetColumn.getCachedShapeRootHistogramWithUncertainties().getRootHisto().Integral()
        hSystUp.Add(datasetColumn.getCachedShapeRootHistogramWithUncertainties().getRootHisto())
        hSystDown.Add(datasetColumn.getCachedShapeRootHistogramWithUncertainties().getRootHisto())
        hSystUp.Scale(myInt / hSystUp.Integral())
        hSystDown.Scale(myInt / hSystDown.Integral())
        hSystUp.Add(datasetColumn.getCachedShapeRootHistogramWithUncertainties().getRootHisto(), -1.0)
        hSystDown.Add(datasetColumn.getCachedShapeRootHistogramWithUncertainties().getRootHisto(), -1.0)
        #print myInt, hSystUp.Integral()+myInt, hSystDown.Integral()+myInt
        #datasetColumn.getCachedShapeRootHistogramWithUncertainties().Debug()
        # Construct end result
        myUncertainty = ScalarUncertaintyItem(self._exid,plus=myUpValue*self._scaleFactor,minus=myDownValue*self._scaleFactor)
        return myUncertainty

    ## Virtual method for extracting histograms
    def extractHistograms(self, datasetColumn, dsetMgr, mainCounterTable, luminosity, additionalNormalisation = 1.0):
        # Obsolete
        raise Exception("obsolete")

    ## Virtual method for printing debug information
    def printDebugInfo(self):
        print "ShapeVariationExtractor"
        ExtractorBase.printDebugInfo(self)


## ShapeVariationToConstantExtractor class
# Converts up and down variation histograms to asymmetric normalization uncertainty
class ShapeVariationToConstantExtractor(ExtractorBase):
    ## Constructor
    def __init__(self, systVariation, mode = ExtractorMode.SHAPENUISANCE, exid = "", distribution = "shapeQ", description = "", opts=None, scaleFactor=1.0):
        ExtractorBase.__init__(self, mode, exid, distribution, description, opts=opts, scaleFactor=scaleFactor)
        self._systVariation = systVariation
        if not "SystVar" in self._systVariation:
            self._systVariation = "SystVar%s"%self._systVariation
        if self.isRate() or self.isObservation():
            raise Exception(ShellStyles.ErrorLabel()+"Rate or observation not allowed for ShapeVariationToConstantExtractor!"+ShellStyles.NormalStyle())

    ## Method for extracking result
    def extractResult(self, datasetColumn, dsetMgr, mainCounterTable, luminosity, additionalNormalisation = 1.0):
        myShapeUncertDict = datasetColumn.getCachedShapeRootHistogramWithUncertainties().getShapeUncertainties()
        if not self._systVariation in myShapeUncertDict.keys():
            print ShellStyles.ErrorLabel()+"Failed to extract systvariation '%s' from column '%s'!"%(self._systVariation,datasetColumn.getLabel())
            print "Available syst.vars.:%s"%", ".join(map(str,myShapeUncertDict.keys()))
            #datasetColumn.getCachedShapeRootHistogramWithUncertainties().Debug()
            raise Exception()
        # Calculate variations from integrals
        (hSystUp, hSystDown) = myShapeUncertDict[self._systVariation]
        myInt = datasetColumn.getCachedShapeRootHistogramWithUncertainties().getRootHisto().Integral()
        myUpValue = hSystUp.Integral() / myInt
        myDownValue = hSystDown.Integral() / myInt
        #print "DEBUG: syst.var.->scalar %s (%s): + %f - %f"%(self._systVariation,datasetColumn.getLabel(),myUpValue,myDownValue)
        # Remove entry from syst variation
        #print "DEBUG: remove %s from column %s"%(self._systVariation,datasetColumn.getLabel())
        del myShapeUncertDict[self._systVariation]
        hSystUp.Delete()
        hSystDown.Delete()
        # Construct end result
        myUncertainty = ScalarUncertaintyItem(self._exid,plus=myUpValue*self._scaleFactor,minus=-myDownValue*self._scaleFactor)
        return myUncertainty

    ## Virtual method for extracting histograms
    def extractHistograms(self, datasetColumn, dsetMgr, mainCounterTable, luminosity, additionalNormalisation = 1.0):
        # Must return an empty list only
        return []

    ## Virtual method for printing debug information
    def printDebugInfo(self):
        print "ShapeVariationToConstantExtractor"
        ExtractorBase.printDebugInfo(self)

## QCDShapeVariationExtractor class
# Extracts histogram shapes from up and down variation
class QCDShapeVariationExtractor(ExtractorBase):
    ## Constructor
    def __init__(self, systVariation, mode = ExtractorMode.SHAPENUISANCE, exid = "", distribution = "shapeQ", description = "", opts=None, scaleFactor=1.0):
        ExtractorBase.__init__(self, mode, exid, distribution, description, opts=opts, scaleFactor=scaleFactor)
        self._systVariation = systVariation
        if self.isRate() or self.isObservation():
            raise Exception(ShellStyles.ErrorLabel()+"Rate or observation not allowed for ShapeVariationExtractor!"+ShellStyles.NormalStyle())

    ## Method for extracking result
    def extractResult(self, datasetColumn, dsetMgr, mainCounterTable, luminosity, additionalNormalisation = 1.0):
        myShapeUncertDict = datasetColumn.getCachedShapeRootHistogramWithUncertainties().getShapeUncertainties()
        if not self._systVariation in myShapeUncertDict.keys():
            return 0.0
        # Tell Lands / Combine that the nuisance is active for the given column, histogram is added to input root file via extractHistograms()
        return 1.0

    ## Virtual method for extracting histograms
    def extractHistograms(self, datasetColumn, dsetMgr, mainCounterTable, luminosity, additionalNormalisation = 1.0, rootHistoWithUncertainties = None):
        myHistograms = []
        if not rootHistoWithUncertainties:
            # Check that results have been cached
            if datasetColumn.getCachedShapeRootHistogramWithUncertainties() == None:
                raise Exception(ShellStyles.ErrorLabel()+"You forgot to cache rootHistogramWithUncertainties for the datasetColumn before creating extractors for nuisances!"+ShellStyles.NormalStyle())
        # Get uncertainty variation dictionary
        myShapeUncertDict = datasetColumn.getCachedShapeRootHistogramWithUncertainties().getShapeUncertainties()
        if rootHistoWithUncertainties != None:
            myShapeUncertDict = rootHistoWithUncertainties.getShapeUncertainties()
        # Check that asked variation does not exist yet
        if self._systVariation in myShapeUncertDict.keys():
            raise Exception(ShellStyles.ErrorLabel()+"DatasetColumn '%s': QCD systematics %s exists already!!"%(datasetColumn.getLabel(),self._systVariation))
        # Obtain histograms
        dset = dsetMgr.getDataset(datasetColumn.getDatasetMgrColumn())
        mySource = "SystVar"+self._systVariation
        myRateHisto = None
        if rootHistoWithUncertainties == None:
            myRateHisto = datasetColumn.getCachedShapeRootHistogramWithUncertainties().getRootHisto()
        else:
            myRateHisto = rootHistoWithUncertainties.getRootHisto()
        myHistoNamePrefix = myRateHisto.GetName().replace("_cloned","").replace("_"+dset.name,"")
        myHistoNameShort = myHistoNamePrefix
        if not "shape" in myHistoNamePrefix:
            myHistoNamePrefix = "ForDataDrivenCtrlPlots/"+myHistoNamePrefix
        (hNum, hNumName) = dset.getRootHisto(myHistoNamePrefix+"Numerator", analysisPostfix=mySource)
        (hDenom, hDenomName) = dset.getRootHisto(myHistoNamePrefix+"Denominator", analysisPostfix=mySource)
        # Store original source histograms
        mySourceNamePrefix = "%s_%sSource"%(datasetColumn.getLabel(),self.getId())
        hNumSource = aux.Clone(hNum, mySourceNamePrefix+"_Numerator")
        hNumSource.SetTitle(mySourceNamePrefix+"_Numerator")
        histogramsExtras.makeFlowBinsVisible(hNumSource)
        myHistograms.append(hNumSource)
        hDenomSource = aux.Clone(hDenom, mySourceNamePrefix+"_Denominator")
        hDenomSource.SetTitle(mySourceNamePrefix+"_Denominator")
        histogramsExtras.makeFlowBinsVisible(hDenomSource)
        myHistograms.append(hDenomSource)
        # do not rebin here, it is done later
        #myArray = array("d",getBinningForPlot(myHistoNameShort))
        #hRebinnedNum = hNum.Rebin(len(myArray)-1,"",myArray)
        #hRebinnedDenom = hDenom.Rebin(len(myArray)-1,"",myArray)
        #hNum.Delete()
        #hDenom.Delete()
        # Handle under/overflow bins
        histogramsExtras.makeFlowBinsVisible(hNum)
        histogramsExtras.makeFlowBinsVisible(hDenom)
        # Create output histograms
        hUp = aux.Clone(myRateHisto)
        hUp.SetTitle(datasetColumn.getLabel()+"_"+self._masterExID+"Up")
        hUp.Reset()
        hDown = aux.Clone(myRateHisto)
        hDown.SetTitle(datasetColumn.getLabel()+"_"+self._masterExID+"Down")
        hDown.Reset()
        # Do calculation and fill output histograms
        systematicsForMetShapeDifference.createSystHistograms(myRateHisto, hUp, hDown, hNum, hDenom)
        # Store uncertainty histograms
        if rootHistoWithUncertainties == None:
            datasetColumn.getCachedShapeRootHistogramWithUncertainties().addShapeUncertaintyFromVariation(self._systVariation, hUp, hDown)
        else:
            rootHistoWithUncertainties.addShapeUncertaintyFromVariation(self._systVariation, hUp, hDown)
        # Do not apply here additional normalization, it does not affect this uncertainty
        # Add rate histogram to make the histograms compatible with LandS/Combine
        hUp.Add(myRateHisto)
        hDown.Add(myRateHisto)
        # Append histograms to output list
        myHistograms.append(hUp)
        myHistograms.append(hDown)
        # Return result
        return myHistograms

    ## Virtual method for printing debug information
    def printDebugInfo(self):
        print "QCDShapeVariationExtractor"
        ExtractorBase.printDebugInfo(self)

## ControlPlotExtractor class
# Extracts histograms for control plot
class ControlPlotExtractor(ExtractorBase):
    ## Constructor, note that if multiplet directories and names are given, the second, third, etc. are substracted from the first one
    def __init__(self, histoSpecs, histoTitle, histoName, opts=None, scaleFactor=1.0):
        ExtractorBase.__init__(self, mode=ExtractorMode.CONTROLPLOT, exid="-1", distribution="-", description="-", opts=opts, scaleFactor=scaleFactor)
        self._histoSpecs = histoSpecs
        self._histoTitle = histoTitle
        self._histoName = histoName

    ## Method for extracking result
    def extractResult(self, datasetColumn, dsetMgr, mainCounterTable, luminosity, additionalNormalisation = 1.0):
        raise Exception(ErrorStyle()+"Did you actually call extractResult for a ControlPlot by name "+self._histoTitle+"? (you shouldn't)"+ShellStyles.NormalStyle())

    ## Virtual method for extracting histograms
    def extractHistograms(self, datasetColumn, dsetMgr, mainCounterTable, luminosity, additionalNormalisation = 1.0):
        myLabel = datasetColumn.getLabel()+"_"+self._histoTitle
        mySystematics = dataset.Systematics(allShapes=True)
        fullHistoName = datasetColumn.getFullHistoName(self._histoName)
        try:
            myDatasetRootHisto = dsetMgr.getDataset(datasetColumn.getDatasetMgrColumn()).getDatasetRootHisto(mySystematics.histogram(fullHistoName))
            return myDatasetRootHisto
        except dataset.HistogramNotFoundException:
            return None

    ## QCD specific method for extracting purity histogram
    def extractQCDPurityHistogram(self, datasetColumn, dsetMgr):
        fullHistoName = datasetColumn.getFullHistoName(self._histoName)
        # Do not apply here additional normalization, it is not needed
        if not datasetColumn.typeIsQCD:
            raise Exception(ShellStyles.ErrorLabel()+"extractQCDPurityHistogram() called for non-QCD datacolumn '%s'!"%datasetColumn.getLabel())
        # Obtain purity histogram
        h = dsetMgr.getDataset(datasetColumn.getDatasetMgrColumn()).getDatasetRootHisto(fullHistoName+"_Purity")
        return h

    ## QCD specific method for extracting purity for a shape
    def extractQCDPurityAsValue(self, datasetColumn, dsetMgr, shapeHisto):
        fullHistoName = datasetColumn.getFullHistoName(self._histoName)
        hPurity = dsetMgr.getDataset(datasetColumn.getDatasetMgrColumn()).getDatasetRootHisto(fullHistoName+"_Purity")
        if isinstance(hPurity, dataset.DatasetRootHisto):
            return _calculateAverageQCDPurity(shapeHisto, hPurity.getHistogram())
        elif isinstance(hPurity, ROOT.TH1):
            return _calculateAverageQCDPurity(shapeHisto, hPurity)
        else:
            raise Exception("This should not happen")

    ## QCD specific method for extracting purity for a shape
    def extractQCDPurityAsValue(self, shapeHisto, purityHisto):
        if isinstance(purityHisto, dataset.DatasetRootHisto):
            return self._calculateAverageQCDPurity(shapeHisto, purityHisto.getHistogram())
        elif isinstance(purityHisto, ROOT.TH1):
            return _calculateAverageQCDPurity(shapeHisto, purityHisto)
        else:
            raise Exception("This should not happen")

    ## Virtual method for printing debug information
    def printDebugInfo(self):
        print "ControlPlotExtractor"
        print "- title:",self._histoTitle
        print "- specs:",self._histoSpecs
        print "- histoName:",self._histoName
        ExtractorBase.printDebugInfo(self)


## ShapeVariationExtractor class
# Extracts histogram shapes from up and down variation
class ShapeVariationFromJsonExtractor(ExtractorBase):
    ## Constructor
    def __init__(self, jsonFile, mode = ExtractorMode.SHAPENUISANCE, exid = "", distribution = "shapeQ", description = "", opts=None, scaleFactor=1.0):
        ExtractorBase.__init__(self, mode, exid, distribution, description, opts=opts, scaleFactor=scaleFactor)
        self._systVariation = exid
        if not os.path.exists(jsonFile):
            raise Exception(ShellStyles.ErrorLabel()+"Cannot find file '%s'!"%jsonFile)
        
        f = open(jsonFile,"r")
        jsonObj = json.load(f)
        self._bins = list(jsonObj["dataParameters"]["Run2012ABCD"]["bins"])
        f.close()
        
        if self.isRate() or self.isObservation():
            raise Exception(ShellStyles.ErrorLabel()+"Rate or observation not allowed for ShapeVariationFromJsonExtractor!")

    ## Method for extracking result
    def extractResult(self, datasetColumn, dsetMgr, mainCounterTable, luminosity, additionalNormalisation = 1.0):
        myShapeUncertDict = datasetColumn.getCachedShapeRootHistogramWithUncertainties().getShapeUncertainties()
        if not self._systVariation in myShapeUncertDict.keys():
            return 0.0
        # Tell Lands / Combine that the nuisance is active for the given column, histogram is added to input root file via extractHistograms()
        return 1.0

    ## Virtual method for extracting histograms
    def extractHistograms(self, datasetColumn, dsetMgr, mainCounterTable, luminosity, additionalNormalisation = 1.0):
        myHistograms = []
        # Check that results have been cached
        if datasetColumn.getCachedShapeRootHistogramWithUncertainties() == None:
            raise Exception(ShellStyles.ErrorLabel()+"You forgot to cache rootHistogramWithUncertainties for the datasetColumn before creating extractors for nuisances!")
        # Get rate histogram from cache
        myRateHisto = datasetColumn.getCachedShapeRootHistogramWithUncertainties().getRootHisto()
        hUp = aux.Clone(myRateHisto)
        hDown = aux.Clone(myRateHisto)
        # Loop over bins
        myWeightBin = 0
        for i in range(1, hUp.GetNbinsX()+1):
            if myWeightBin < len(self._bins)-1:
                if not hUp.GetXaxis().GetBinLowEdge(i) + 0.0001 < self._bins[myWeightBin+1]["mt"]:
                    myWeightBin += 1
            #print "hbin edge=",h.GetXaxis().GetBinLowEdge(i),"weight edge=",binList[myWeightBin]
            hUp.SetBinContent(i, hUp.GetBinContent(i) * (self._bins[myWeightBin]["uncertaintyPlus"]))
            hDown.SetBinContent(i, hDown.GetBinContent(i) * (-self._bins[myWeightBin]["uncertaintyMinus"]))
        datasetColumn._cachedShapeRootHistogramWithUncertainties._shapeUncertainties[self._exid] = (hUp, hDown)
        # Do not apply here additional normalization, it has already been applied
        # via RootHistoWithUncertainties.Scale() in DatacardColumn::doDataMining()
        # Append histograms to output list
        hUpPlusOne = aux.Clone(hUp)
        hDownPlusOne = aux.Clone(hDown)
        hUpPlusOne.SetTitle(datasetColumn.getLabel()+"_"+self._masterExID+"Up")
        hDownPlusOne.SetTitle(datasetColumn.getLabel()+"_"+self._masterExID+"Down")
        hUpPlusOne.Add(myRateHisto)
        hDownPlusOne.Add(myRateHisto)
        myHistograms.append(hUpPlusOne)
        myHistograms.append(hDownPlusOne)
        
        #datasetColumn._cachedShapeRootHistogramWithUncertainties.Debug()
        # Return result
        return myHistograms

    ## Virtual method for printing debug information
    def printDebugInfo(self):
        print "ShapeVariationFromJsonExtractor"
        ExtractorBase.printDebugInfo(self)
