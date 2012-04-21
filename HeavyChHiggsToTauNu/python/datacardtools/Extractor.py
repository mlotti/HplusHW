## \package Extractor
# Classes for extracting observation/rate/nuisance from datasets
#
#

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter import EventCounter

# Enumerator class for data mining mode
class ExtractorMode:
    UNKNOWN = 0
    OBSERVATION = 1
    RATE = 2
    NUISANCE = 3
    ASYMMETRICNUISANCE = 4
    SHAPENUISANCE = 5

## ExtractorBase class
class ExtractorBase:
    ## Constructor
    def __init__(self, mode, exid, distribution, description):
        self._mode = mode
        self._isPrintable = True
        self._exid = exid
        self._distribution = distribution
        self._description = description
        self._extractablesToBeMerged = []
        self._masterExID = ""

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
            print "\033[0;41m\033[1;37mError:\033[0;0m Cannot find counter histogram '"+counterHisto+"'!"
            sys.exit()
        return histo

    ## Returns index to bin corresponding to first matching label in a counter histogram
    def getCounterItemIndex(self, histo, counterItem):
        for i in range(1, histo.GetNbinsX()+1):
            if histo.GetXaxis().GetBinLabel(i) == myBinLabel:
                return i
        print "\033[0;41m\033[1;37mError:\033[0;0m Cannot find counter by name "+counterItem+"!"
        sys.exit()

    ## Virtual method for extracking information
    def doExtract(self, dsetMgr, dsetMgrColumn, luminosity, additionalNormalisation = 1.0):
        return -1.0

    ## Virtual method for adding histograms to the root file
    def addHistogramsToFile(self, label, exid, rootFile):
        return

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
    def __init__(self, constantValue, mode, exid = "", distribution = "lnN", description = "", constantUpperValue = 0.0):
        ExtractorBase.__init__(self, mode, exid, distribution, description)
        self._constantValue = constantValue
        self._constantUpperValue = constantUpperValue

    ## Method for extracking information
    def doExtract(self, dsetMgr, dsetMgrColumn, luminosity, additionalNormalisation = 1.0):
        if self.isAsymmetricNuisance():
            return [self._constantValue, self._constantUpperValue]
        else:
            return self._constantValue

    ## Method for adding histograms to the root file
    #def addHistogramsToFile(self, label, exid, rootFile):

    ## Virtual method for printing debug information
    def printDebugInfo(self):
        print "ConstantExtractor"
        if self.isAsymmetricNuisance():
            print "- value = ", self._constantValue, "/", self._constantUpperValue
        else:
            print "- value = ", self._constantValue
        ExtractorBase.printDebugInfo(self)

    ## \var _constantValue
    # Constant value (either rate or nuisance in percent)
    ## \var _constantUpperValue
    # Constant value for upper bound (either rate or nuisance in percent)

## CounterExtractor class
# Extracts a value from a given counter in the list of main counters
class CounterExtractor(ExtractorBase):
    ## Constructor
    def __init__(self, counterItem, mode, exid = "", distribution = "lnN", description = ""):
        ExtractorBase.__init__(self, mode, exid, distribution, description)
        self._counterItem = counterItem

    ## Method for extracking information
    def doExtract(self, dsetMgr, dsetMgrColumn, luminosity, additionalNormalisation = 1.0):
        myEventCounter = EventCounter(dsetMgr)
        #myEventCounter.normalizeMCByLuminosity()
        myEventCounter.normalizeMCToLuminosity(luminosity)
        myTable = myEventCounter.getMainCounterTable()
        myCount = myTable.getCount(rowName=self._counterItem, colName=dsetMgrColumn)
        # Return resul
        if self.isRate() or self.isObservation():
            return myCount.value() * additionalNormalisation
        elif self.isNuisance():
            return myCount.uncertainty() / myCount.value()

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
    def __init__(self, counterDirs, counterItem, mode, exid = "", distribution = "lnN", description = ""):
        ExtractorBase.__init__(self, mode, exid, distribution, description)
        self._counterItem = counterItem
        self._counterDirs = counterDirs
        if len(self._counterDirs) < 2:
            print "Error in Nuisance with id='"+self._exid+"': need to specify at least two directories for counters!"
            sys.exit()

    ## Method for extracking information
    def doExtract(self, dsetMgr, dsetMgrColumn, luminosity, additionalNormalisation = 1.0):
        myResult = []
        for d in self_counterDirs:
            myHistoPath = d+"/weighted/counters"
            datasetRootHisto = dsetMgr.getDataset(dsetMgrColumn).getDatasetRootHisto(myHistoPath)
            datasetRootHisto.normalizeToLuminosity(luminosity)
            counterList = dataset._histoToCounter(datasetRootHisto.getHistogram())
            myFoundStatus = False # to ensure that the first counter of given name is taken
            for name, count in counterList:
                if name == self._counterItem and not myFoundStatus:
                    myResult.append(count)
                    myFoundStatus = True
            if not myFoundStatus:
                print "Error in Nuisance with id='"+self._exid+"': Cannot find counter name '"+self._counterItem+"' in histogram '"+myHistoPath+"'!"
                sys.exit()
        # Loop over results
        myMaxValue = 0.0
        # Protect for div by zero
        if myResult[0].value() == 0:
            print "Warning: In Nuisance with id='"+self._exid+"' nominal counter ('"+self._counterItem+"')value is zero!"
            return 0.0
        for i in range(1,len(myResult)):
            myValue = myResult[i].value() / myResult[0].value()
            if (myValue > myMaxValue):
                myMaxValue = myValue
        return myMaxValue

    ## Virtual method for printing debug information
    def printDebugInfo(self):
        print "MaxCounterExtractor"
        print "- counter item = ", self._counterItem
        ExtractorBase.printDebugInfo(self)

    ## \var _counterDirs
    # List of directories (without /weighted/counter suffix ) for counter histograms; first needs to be the nominal counter
    ## \var _counterItem
    # Name of item (label) in counter histogram

## RatioExtractor class
# Extracts two values from two counter items in the list of main counters and returns th ratio of these scaled by some factor
class RatioExtractor(ExtractorBase):
    ## Constructor
    def __init__(self, scale, numeratorCounterItem, denominatorCounterItem, mode, exid = "", distribution = "lnN", description = ""):
        ExtractorBase.__init__(self, mode, exid, distribution, description)
        self._numeratorCounterItem = numeratorCounterItem
        self._denominatorCounterItem = denominatorCounterItem
        self._scale = scale

    ## Method for extracking information
    def doExtract(self, dsetMgr, dsetMgrColumn, luminosity, additionalNormalisation = 1.0):
        myEventCounter = EventCounter(dsetMgr)
        #myEventCounter.normalizeMCByLuminosity()
        myEventCounter.normalizeMCToLuminosity(luminosity)
        myTable = myEventCounter.getMainCounterTable()
        myNumeratorCount = myTable.getCount(rowName=self._numeratorCounterItem, colName=dsetMgrColumn)
        myDenominatorCount = myTable.getCount(rowName=self._denominatorCounterItem, colName=dsetMgrColumn)
        # Protection against div by zero
        if myDenominatorCount.value() == 0.0:
            print "Warning: In Nuisance with id='"+self._exid+"' denominator counter ('"+self._counterItem+"') value is zero!"
            return 0.0
        # Return result
        return myNumeratorCount.value() / myDenominatorCount.value() * self._scale

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

