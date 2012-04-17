## \package CounterExtractor
# Base class for extracting observation/rate/nuisance from datasets
#
#

from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.Extractor import ExtractorBase
from HiggsAnalysis.HeavyChHiggsToTauNu.counter import counter

# CounterExtractor class
class CounterExtractor(Extractor):
    ## Constructor
    def __init__(self, counterItem, mode, exid = "", distribution = "lnN", description = ""):
        ExtractorBase.__init__(self, mode, exid, distribution, description)
        self._counterItem = counterItem

    ## Method for extracking information
    def doExtract(self, counterHisto, datasets, normalisation, additionalNormalisation = 1.0):
        myCounterValue = 0.0 # result in number of events
        myCounterUncertainty = 0.0 # result in number of events (abs. uncertainty)
        for dset in datasets:
            # obtain main counter
            myEventCounter = counter.EventCounter(dset, countNameFunction=None, counters=_counterDir)
            myMainCounters = myEventCounter.getMainCounter().counters
            # find matching counter item
            for item in myMainCounters:
                if item == _counterItem:
                    # match found, now return result
                    
            # no match found, print error message
            
            
    if self.isRate() or self.isObservation():
        return myCounterValue * additionalNormalisation
    elif self.isNuisance():
        return myCounterUncertainty / myCounterValue

    ## Virtual method for printing debug information
    def printDebugInfo(self):
        print "CounterExtractor"
        if self.isAsymmetricNuisance():
            print "- value = ", self._constantValue, "/", self._constantUpperValue
        else:
            print "- value = ", self._constantValue
        ExtractorBase.printDebugInfo(self)

    ## \var _counterItem
    # Name of item (label) in counter histogram