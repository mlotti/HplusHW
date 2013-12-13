## \package Extractor
# Classes for extracting observation/rate/nuisance from datasets
#
#

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter import EventCounter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.systematics import ScalarUncertaintyItem
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShellStyles import *
from math import pow,sqrt
import sys
import ROOT

# Enumerator class for data mining mode
class ExtractorMode:
    UNKNOWN = 0
    OBSERVATION = 1
    RATE = 2
    NUISANCE = 3
    ASYMMETRICNUISANCE = 4
    SHAPENUISANCE = 5
    CONTROLPLOT = 6

## ExtractorBase class
class ExtractorBase:
    ## Constructor
    def __init__(self, mode, exid, distribution, description, opts=None):
        self._mode = mode
        self._isPrintable = True
        self._exid = exid
        self._distribution = distribution
        self._description = description
        self._extractablesToBeMerged = []
        self._masterExID = exid

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
               self._mode == ExtractorMode.SHAPENUISANCE

    ## Returns true if extractable mode is nuisance
    def isNuisance(self):
        return self._mode == ExtractorMode.NUISANCE

    ## Returns true if extractable mode is nuisance with asymmetric limits
    def isAsymmetricNuisance(self):
        return self._mode == ExtractorMode.ASYMMETRICNUISANCE

    ## Returns true if extractable mode is shape nuisance
    def isShapeNuisance(self):
        return self._mode == ExtractorMode.SHAPENUISANCE

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
            raise Exception(ErrorStyle()+"Error:"+NormalStyle()+" Cannot find counter histogram '"+counterHisto+"'!")
        return histo

    ## Returns index to bin corresponding to first matching label in a counter histogram
    def getCounterItemIndex(self, histo, counterItem):
        for i in range(1, histo.GetNbinsX()+1):
            if histo.GetXaxis().GetBinLabel(i) == myBinLabel:
                return i
        raise Exception(ErrorStyle()+"Error:"+NormalStyle()+" Cannot find counter by name "+counterItem+"!")

    ## Virtual method for extracking information
    def extractResult(self, datasetColumn, dsetMgr, mainCounterTable, luminosity, additionalNormalisation = 1.0):
        return -1.0

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
    def __init__(self, constantValue, mode, exid = "", distribution = "lnN", description = "", constantUpperValue = 0.0, opts=None):
        ExtractorBase.__init__(self, mode, exid, distribution, description, opts=opts)
        self._constantValue = None
        if isinstance(constantValue, ScalarUncertaintyItem):
            self._constantValue = constantValue
        else:
            if self.isAsymmetricNuisance() or constantUpperValue != None:
                self._constantValue = ScalarUncertaintyItem(exid,plus=constantUpperValue,minus=constantValue)
            else:
                self._constantValue = ScalarUncertaintyItem(exid,constantValue)

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

## CounterExtractor class
# Extracts a value from a given counter in the list of main counters
class CounterExtractor(ExtractorBase):
    ## Constructor
    def __init__(self, counterItem, mode, exid = "", distribution = "lnN", description = "", opts=None):
        ExtractorBase.__init__(self, mode, exid, distribution, description, opts=opts)
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
                print WarningStyle()+"Warning:"+NormalStyle()+" In Nuisance with id='"+self._exid+"' for column '"+datasetColumn.getLabel()+"' counter ('"+self._counterItem+"') value is zero!"
                myResult = ScalarUncertaintyItem(self._exid,0.0)
            else:
                myResult = ScalarUncertaintyItem(self._exid,myCount.uncertainty() / myCount.value())
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
    def __init__(self, counterDirs, counterItem, mode, exid = "", distribution = "lnN", description = "", opts=None):
        ExtractorBase.__init__(self, mode, exid, distribution, description, opts=opts)
        self._counterItem = counterItem
        self._counterDirs = counterDirs
        if len(self._counterDirs) < 2:
            raise Exception(ErrorStyle()+"Error in Nuisance with id='"+self._exid+"':"+NormalStyle()+" need to specify at least two directories for counters!")

    ## Method for extracking information
    def extractResult(self, datasetColumn, dsetMgr, mainCounterTable, luminosity, additionalNormalisation = 1.0):
        myResult = []
        for d in self._counterDirs:
            myHistoPath = d+"/weighted/counter"
            try:
                datasetRootHisto = dsetMgr.getDataset(datasetColumn.getDatasetMgrColumn()).getDatasetRootHisto(myHistoPath)
            except Exception, e:
                raise Exception (ErrorStyle()+"Error in extracting max counter value:"+NormalStyle()+" cannot find histogram!\n  Column = %s\n  NuisanceId = %s\n  Message = %s!"%(datasetColumn.getLabel(),self._exid, str(e)))
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
                raise Exception(ErrorStyle()+"Error in Nuisance with id='"+self._exid+"' for column '"+datasetColumn.getLabel()+"':"+NormalStyle()+" Cannot find counter name '"+self._counterItem+"' in histogram '"+myHistoPath+"'!")
        # Loop over results
        myMaxValue = 0.0
        # Protect for div by zero
        if myResult[0].value() == 0:
            print WarningStyle()+"Warning:"+NormalStyle()+" In Nuisance with id='"+self._exid+"' for column '"+datasetColumn.getLabel()+"' nominal counter ('"+self._counterItem+"')value is zero!"
        else:
            for i in range(1,len(myResult)):
                myValue = abs(myResult[i].value() / myResult[0].value() - 1.0)
                if (myValue > myMaxValue):
                    myMaxValue = myValue
        return ScalarUncertaintyItem(self._exid,myMaxValue)

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
            #raise Exception(ErrorStyle()+"Error in Nuisance with id='"+self._exid+"':"+NormalStyle()+" need to specify at least two directories for counters!")

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
                #raise Exception (ErrorStyle()+"Error in extracting PU uncertainty:"+NormalStyle()+" cannot find histogram!\n  Column = %s\n  NuisanceId = %s\n  Message = %s!"%(datasetColumn.getLabel(),self._exid, str(e)))
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
                #raise Exception(ErrorStyle()+"Error in Nuisance with id='"+self._exid+"' for column '"+datasetColumn.getLabel()+"':"+NormalStyle()+" Cannot find counter name '"+self._counterItem+"' in histogram '"+myHistoName+"'!")
        ## Revert back to nominal normalisation
        ## mgr.updateNAllEventsToPUWeighted(weightType=PileupWeightType.NOMINAL) #FIXME
        ## Loop over results
        #myMaxValue = 0.0
        ## Protect for div by zero
        #if myResult[0].value() == 0:
            #print WarningStyle()+"Warning:"+NormalStyle()+" In Nuisance with id='"+self._exid+"' for column '"+datasetColumn.getLabel()+"' nominal counter ('"+self._counterItem+"')value is zero!"
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
    def __init__(self, scale, numeratorCounterItem, denominatorCounterItem, mode, exid = "", distribution = "lnN", description = "", opts=None):
        ExtractorBase.__init__(self, mode, exid, distribution, description, opts=opts)
        self._numeratorCounterItem = numeratorCounterItem
        self._denominatorCounterItem = denominatorCounterItem
        self._scale = scale

    ## Method for extracking information
    def extractResult(self, datasetColumn, dsetMgr, mainCounterTable, luminosity, additionalNormalisation = 1.0):
        myNumeratorCount = mainCounterTable.getCount(rowName=self._numeratorCounterItem, colName=datasetColumn.getDatasetMgrColumn())
        myDenominatorCount = mainCounterTable.getCount(rowName=self._denominatorCounterItem, colName=datasetColumn.getDatasetMgrColumn())
        # Protection against div by zero
        if myDenominatorCount.value() == 0.0:
            print WarningStyle()+"Warning:"+NormalStyle()+" In Nuisance with id='"+self._exid+"' for column '"+datasetColumn.getLabel()+"' denominator counter ('"+self._counterItem+"') value is zero!"
            myResult = 0.0
        else:
            myResult = (myDenominatorCount.value() / myNumeratorCount.value() - 1.0) * self._scale
        # Return result
        return ScalarUncertaintyItem(self._exid,myResult)

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
    def __init__(self, histoDirs, histograms, normalisation, addSystInQuadrature = 0.0, mode = ExtractorMode.NUISANCE, exid = "", distribution = "lnN", description = "", opts=None):
        ExtractorBase.__init__(self, mode, exid, distribution, description, opts=opts)
        self._histoDirs = histoDirs
        self._histograms = histograms
        self._normalisation = normalisation
        self._addSystInQuadrature = addSystInQuadrature
        if len(self._histoDirs) != len(self._normalisation) or len(self._histoDirs) != len(self._histograms):
            raise Exception(ErrorStyle()+"Error in Nuisance with id='"+self._exid+"' for column '"+datasetColumn.getLabel()+"':"+NormalStyle()+" need to specify equal amount of histoDirs, histograms and normalisation histograms!")

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
                raise Exception (ErrorStyle()+"Error in extracting scale factor uncertainty:"+NormalStyle()+" cannot find value histogram!\n  Column = %s\n  NuisanceId = %s\n  Message = %s!"%(datasetColumn.getLabel(),self._exid, str(e)))
            myValueRootHisto.normalizeToLuminosity(luminosity)
            hValues = myValueRootHisto.getHistogram()
            if hValues == None:
                raise Exception(ErrorStyle()+"Error in Nuisance with id='"+self._exid+"' for column '"+datasetColumn.getLabel()+"':"+NormalStyle()+" Cannot open histogram '"+myHistoName+"'!")
            myHistoName = self._histoDirs[i]+"/"+self._normalisation[i]
            try:
                myNormalisationRootHisto = dsetMgr.getDataset(datasetColumn.getDatasetMgrColumn()).getDatasetRootHisto(myHistoName)
            except Exception, e:
                raise Exception (ErrorStyle()+"Error in extracting scale factor uncertainty:"+NormalStyle()+" cannot find normalisation histogram!\n  Column = %s\n  NuisanceId = %s\n  Message = %s!"%(datasetColumn.getLabel(),self._exid, str(e)))
            myNormalisationRootHisto.normalizeToLuminosity(luminosity)
            hNormalisation = myNormalisationRootHisto.getHistogram()
            if hNormalisation == None:
                raise Exception(ErrorStyle()+"Error in Nuisance with id='"+self._exid+"' for column '"+datasetColumn.getLabel()+"':"+NormalStyle()+" Cannot open histogram '"+myHistoName+"'!")
            for j in range (1, hValues.GetNbinsX()+1):
                mySum += pow(hValues.GetBinContent(j) * hValues.GetBinCenter(j),2)
            myTotal = hNormalisation.GetBinContent(1)
            hValues.IsA().Destructor(hValues)
            hNormalisation.IsA().Destructor(hNormalisation)
            # Calculate result, protection against div by zero
            if myTotal == 0.0:
                print WarningStyle()+"Warning:"+NormalStyle()+" In Nuisance with id='"+self._exid+"' for column '"+datasetColumn.getLabel()+"' total count from normalisation histograms is zero!"
                myResult.append(0.0)
            else:
                myResult.append(sqrt(mySum) / myTotal)
        # Combine result
        myCombinedResult = 0.0
        for i in range (0, len(self._histoDirs)):
            myCombinedResult += pow(myResult[i], 2)
        myCombinedResult += pow(self._addSystInQuadrature, 2)
        # Return result
        return ScalarUncertaintyItem(self._exid,sqrt(myCombinedResult))


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
    def __init__(self, mode = ExtractorMode.SHAPENUISANCE, exid = "", distribution = "", description = "", opts=None):
        ExtractorBase.__init__(self, mode, exid, distribution, description, opts=opts)
        if not (self.isRate() or self.isObservation()):
            if self._distribution != "shapeStat":
                self.printDebugInfo()
                raise Exception(ErrorLabel()+"Only shapeStat allowed for the ShapeExtractor!"+NormalStyle())

    ## Method for extracking result
    def extractResult(self, datasetColumn, dsetMgr, mainCounterTable, luminosity, additionalNormalisation = 1.0):
        # Tell Lands / Combine that the nuisance is active for the given column, histogram is added to input root file via extractHistograms()
        return 1.0

    ## Virtual method for extracting histograms
    def extractHistograms(self, datasetColumn, dsetMgr, mainCounterTable, luminosity, additionalNormalisation = 1.0):
        myHistograms = []
        # Check that results have been cached
        if datasetColumn.getCachedShapeRootHistogramWithUncertainties() == None:
            raise Exception(ErrorLabel()+"You forgot to cache rootHistogramWithUncertainties for the datasetColumn before creating extractors for nuisances!"+NormalStyle())
        # Get histogram from cache
        h = datasetColumn.getCachedShapeRootHistogramWithUncertainties().getRootHisto()
        # Do not apply here additional normalization, it has already been applied
        # via RootHistoWithUncertainties.Scale() in DatacardColumn::doDataMining()
        if self.isRate() or self.isObservation():
            # Shape histogram is the result
            h.SetTitle(datasetColumn.getLabel())
            myHistograms.append(h) # Append histogram to output list
        else:
            # Ok, it's a nuisance
            # Create up and down histograms for shape stat
            hUp = h.Clone()
            hDown = h.Clone()
            hUp.Reset()
            hDown.Reset()
            hUp.SetTitle(datasetColumn.getLabel()+"_"+self._masterExID+"Up")
            hDown.SetTitle(datasetColumn.getLabel()+"_"+self._masterExID+"Down")
            for k in range(1, h.GetNbinsX()+1):
                hUp.SetBinContent(k, h.GetBinContent(k) + h.GetBinError(k))
                hDown.SetBinContent(k, h.GetBinContent(k) - h.GetBinError(k))
            # Append histograms to output list
            myHistograms.append(hUp)
            myHistograms.append(hDown)
            #h.IsA().Destructor(h) # Delete the nominal histo
        # Return result
        return myHistograms

    ## Virtual method for printing debug information
    def printDebugInfo(self):
        print "ShapeExtractor"
        ExtractorBase.printDebugInfo(self)

## ShapeVariationExtractor class
# Extracts histogram shapes from up and down variation
class ShapeVariationExtractor(ExtractorBase):
    ## Constructor
    def __init__(self, systVariation, mode = ExtractorMode.SHAPENUISANCE, exid = "", distribution = "shapeQ", description = "", opts=None):
        ExtractorBase.__init__(self, mode, exid, distribution, description, opts=opts)
        self._systVariation = systVariation
        if not "SystVar" in self._systVariation:
            self._systVariation = "SystVar%s"%self._systVariation
        if self.isRate() or self.isObservation():
            raise Exception(ErrorLabel()+"Rate or observation not allowed for ShapeVariationExtractor!"+NormalStyle())

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
            raise Exception(ErrorLabel()+"You forgot to cache rootHistogramWithUncertainties for the datasetColumn before creating extractors for nuisances!"+NormalStyle())
        # Get uncertainty variation dictionary
        myShapeUncertDict = datasetColumn.getCachedShapeRootHistogramWithUncertainties().getShapeUncertainties()
        # Check that asked variation exists
        if not self._systVariation in myShapeUncertDict.keys():
            print WarningLabel()+"DatasetColumn '%s': Cannot find systematics variation %s, ignoring it! Available: %s"%(datasetColumn.getLabel(), self._systVariation, ', '.join(map(str, myShapeUncertDict.keys())))
            return myHistograms
        # Get histogram from cache
        (hSystUp, hSystDown) = myShapeUncertDict[self._systVariation]
        hUp = hSystUp.Clone()
        hDown = hSystDown.Clone()
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
        print "ShapeExtractor"
        ExtractorBase.printDebugInfo(self)

## ControlPlotExtractor class
# Extracts histograms for control plot
class ControlPlotExtractor(ExtractorBase):
    ## Constructor, note that if multiplet directories and names are given, the second, third, etc. are substracted from the first one
    def __init__(self, histoSpecs, histoTitle, histoDirs, histoNames, opts=None):
        ExtractorBase.__init__(self, mode=ExtractorMode.CONTROLPLOT, exid="-1", distribution="-", description="-", opts=opts)
        self._histoSpecs = histoSpecs
        self._histoTitle = histoTitle
        self._histoName = histoNames
        self._histoNameWithPath = ""
        if histoDirs != None and histoDirs != "" and histoDirs != ".":
            self._histoNameWithPath = "%s/"%histoDirs
        self._histoNameWithPath += histoNames

    ## Method for extracking result
    def extractResult(self, datasetColumn, dsetMgr, mainCounterTable, luminosity, additionalNormalisation = 1.0):
        raise Exception(ErrorStyle()+"Did you actually call extractResult for a ControlPlot by name "+self._histoTitle+"? (you shouldn't)"+NormalStyle())

    ## Virtual method for extracting histograms
    def extractHistograms(self, datasetColumn, dsetMgr, mainCounterTable, luminosity, additionalNormalisation = 1.0):
        myLabel = datasetColumn.getLabel()+"_"+self._histoTitle
        mySystematics = dataset.Systematics(allShapes=True)
        myDatasetRootHisto = dsetMgr.getDataset(datasetColumn.getDatasetMgrColumn()).getDatasetRootHisto(mySystematics.histogram(self._histoNameWithPath))
        return myDatasetRootHisto

    ## Virtual method for printing debug information
    def printDebugInfo(self):
        print "ControlPlotExtractor"
        print "- title:",self._histoTitle
        print "- specs:",self._histoSpecs
        print "- histoDirs:",self._histoDirs
        print "- histoNames:",self._histoNames
        ExtractorBase.printDebugInfo(self)

