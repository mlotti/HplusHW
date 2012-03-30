## \package Extractable
# Base class for extracting observation/rate/nuisance from datasets
#
#


# Enumerator class for data mining mode
class ExtractableMode:
    UNKNOWN = 0
    OBSERVATION = 1
    RATE = 2
    NUISANCE = 3
    ASYMMETRICNUISANCE = 4
    SHAPENUISANCE = 5

# Extractable class
class Extractable:
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
        return self._mode == ExtractableMode.OBSERVATION
    
    ## Returns true if extractable mode is rate
    def isRate(self):
        return self._mode == ExtractableMode.RATE

    ## Returns true if extractable mode is any type of nuisance
    def isAnyNuisance(self):
        return self._mode == ExtractableMode.NUISANCE or self._mode == ExtractableMode.ASYMMETRICNUISANCE or self._mode == ExtractableMode.SHAPENUISANCE

    ## Returns true if extractable mode is nuisance
    def isNuisance(self):
        return self._mode == ExtractableMode.NUISANCE
    
    ## Returns true if extractable mode is nuisance with asymmetric limits
    def isAsymmetricNuisance(self):
        return self._mode == ExtractableMode.ASYMMETRICNUISANCE
    
    ## Returns true if extractable mode is shape nuisance
    def isShapeNuisance(self):
        return self._mode == ExtractableMode.SHAPENUISANCE

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
    def addExtractableToBeMerged(self, extractable):
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
    def doExtract(self, datasets, normalisation, additionalNormalisation = 1.0):
        return
        
    ## Virtual method for extracking information
    def doExtractAsymmetricUpperValue(self, datasets, normalisation, additionalNormalisation = 1.0):
        return
      
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