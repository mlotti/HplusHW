## \package ConstantExtractable
# Base class for extracting observation/rate/nuisance from datasets
#
#

from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.Extractable import Extractable

# ConstantExtractable class
class ConstantExtractable(Extractable):
    ## Constructor
    def __init__(self, constantValue, mode, exid = "", distribution = "lnN", description = "", constantUpperValue = 0.0):
        Extractable.__init__(self, mode, exid, distribution, description)
        self._constantValue = constantValue
        self._constantUpperValue = constantUpperValue

    ## Method for extracking information
    def doExtract(self, datasets, normalisation, additionalNormalisation = 1.0):
        return self._constantValue

    ## Method for extracking information
    def doExtractAsymmetricUpperValue(self, datasets, normalisation, additionalNormalisation = 1.0):
        return self._constantUpperValue

    ## Method for adding histograms to the root file
    #def addHistogramsToFile(self, label, exid, rootFile):
        

    ## Virtual method for printing debug information
    def printDebugInfo(self):
        print "ConstantExtractable"
        if self.isAsymmetricNuisance():
            print "- value = ", self._constantValue, "/", self._constantUpperValue
        else:
            print "- value = ", self._constantValue
        Extractable.printDebugInfo(self)

    ## \var _constantValue
    # Constant value (either rate or nuisance in percent)
    ## \var _constantUpperValue
    # Constant value for upper bound (either rate or nuisance in percent)