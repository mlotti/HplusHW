## \package DatacardColumn
# Class collecting information about a column to be produced in the datacard
#

import os
import sys

from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.MulticrabPathFinder import MulticrabDirectoryDataType
from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.Extractor import ExtractorMode,CounterExtractor

# DatacardColumn class
class DatacardColumn():
    ## Constructor
    def __init__(self,
                 label = "",
                 landsProcess = -999,
                 enabledForMassPoints = [],
                 datasetType = 0,
                 rateCounter = "",
                 nuisances = [],
                 datasetMgr = None,
                 datasetMgrColumn = "",
                 datasetMgrColumnForQCDMCEWK = "",
                 additionalNormalisationFactor = 1.0,
                 dirPrefix = "",
                 shapeHisto = ""):
        self._label = label
        self._landsProcess = landsProcess
        self._enabledForMassPoints = enabledForMassPoints
        if datasetType == "Observation":
            self._datasetType = MulticrabDirectoryDataType.OBSERVATION
        elif datasetType == "Signal":
            self._datasetType = MulticrabDirectoryDataType.SIGNAL
        elif datasetType == "Embedding":
            self._datasetType = MulticrabDirectoryDataType.EWKTAUS
        elif datasetType == "QCD factorised":
            self._datasetType = MulticrabDirectoryDataType.QCDFACTORISED
        elif datasetType == "QCD inverted":
            self._datasetType = MulticrabDirectoryDataType.QCDINVERTED
        elif datasetType == "None":
            self._datasetType = MulticrabDirectoryDataType.DUMMY
        else:
            self._datasetType = MulticrabDirectoryDataType.UNKNOWN
        self._rateCounter = rateCounter
        self._nuisances = nuisances
        self._datasetMgr = datasetMgr
        self._datasetMgrColumn = datasetMgrColumn
        self._datasetMgrColumnForQCDMCEWK  = datasetMgrColumnForQCDMCEWK
        self._additionalNormalisationFactor = additionalNormalisationFactor
        self._dirPrefix = dirPrefix
        self._shapeHisto = shapeHisto
        self._isPrintable = True

        self.checkInputValidity()

    def checkInputValidity(self):
        myMsg = ""
        if self._label == "":
            myMsg += "Missing or empty field 'label'! (string) to be printed on a column in datacard\n"
        if self._datasetType != MulticrabDirectoryDataType.OBSERVATION:
            if self._landsProcess == -999:
                myMsg += "Missing or empty field 'landsProcess'! (integer) to be printed as process in datacard\n"
        if len(self._enabledForMassPoints) == 0:
            myMsg += "Missing or empty field 'validMassPoints'! (list of integers) specifies for which mass points the column is enabled\n"
        if self._datasetType == MulticrabDirectoryDataType.UNKNOWN:
            myMsg += "Wrong 'datasetType' specified! Valid options are 'Signal', 'Embedding', 'QCD factorised', 'QCD inverted', and 'None'\n"
        if self._datasetMgrColumn == "":
            myMsg += "No dataset names defined!\n"
        if self._datasetType == MulticrabDirectoryDataType.SIGNAL or self._datasetType == MulticrabDirectoryDataType.EWKTAUS or self._datasetType == MulticrabDirectoryDataType.OBSERVATION:
            if self._rateCounter == "":
                myMsg += "Missing or empty field 'rateCounter'! (string) Counter for rate to be used for column\n"
            if self._shapeHisto == "":
                myMsg += "Missing or empty field 'shapeHisto'! (string) Name of histogram for shape \n"
        elif self._datasetType == MulticrabDirectoryDataType.QCDFACTORISED:
            # rate handled as spedial case, extra datasetMgrColumn are required for EWK MC
            if len(self._datasetMgrColumnForQCDMCEWK) == 0:
                myMsg += "No datasets defined for MC EWK in data group for QCD factorised!\n"
        elif self._datasetType == MulticrabDirectoryDataType.QCDINVERTED:
            myMsg += "FIXME: QCD inverted not implemented yet\n" # FIXME
        if self._datasetType != MulticrabDirectoryDataType.DUMMY and self._datasetType != MulticrabDirectoryDataType.OBSERVATION:
            if len(self._nuisances) == 0:
                myMsg += "Missing or empty field 'nuisances'! (list of strings) Id's for nuisances to be used for column\n"

        if myMsg != "":
            print "\033[0;41m\033[1;37mError (data group ='"+self._label+"'):\033[0;0m\n"+myMsg
            sys.exit()

    ## Returns true if column has a nuisance Id
    def hasNuisanceId(self, id):
        return id in self._nuisances

    ## Returns true if column is enabled for given mass point
    def isActiveForMass(self, mass):
        return (mass in self._enabledForMassPoints) and self._isPrintable

    ## Disables the datacard column
    def disable(self):
        self._isPrintable = False

    ## Returns label
    def getLabel(self):
        return self._label

    ## Returns LandS process
    def getLandsProcess(self):
        return self._landsProcess

    ## Returns dataset manager
    def getDatasetMgr(self):
        return self._datasetMgr

    ## Returns dataset manager column
    def getDatasetMgrColumn(self):
        return self._datasetMgrColumn

    ## Returns dataset manager column for MC EWK in QCD factorised
    def getDatasetMgrColumnForQCDMCEWK(self):
        return self._datasetMgrColumnForQCDMCEWK

    ## Returns rate for column (as string)
    def getRateValue(self, luminosity, additionalNormalisation = 1.0):
        if self._datasetType == MulticrabDirectoryDataType.DUMMY:
            return 0.0
        myExtractor = None
        if self._datasetType == MulticrabDirectoryDataType.OBSERVATION:
            myExtractor = CounterExtractor(self._rateCounter, ExtractorMode.OBSERVATION)
        else:
            myExtractor = CounterExtractor(self._rateCounter, ExtractorMode.RATE)
        if self._datasetType == MulticrabDirectoryDataType.QCDFACTORISED or self._datasetType == MulticrabDirectoryDataType.QCDINVERTED:
            #myExtractor.Calculate(luminosity, additionalNormalisation)
            #myExtractor.
            print "rate not implemented for QCD yet, setting rate to zero"  #FIXME
        else:
            return myExtractor.doExtract(self, luminosity, additionalNormalisation)

    ## Returns nuisance for column (as string)
    def getNuisanceValue(self, id):
        for nid in self._nuisances:
            if id == nid:
                return myExtractor.doExtract(self, luminosity, additionalNormalisation)
                #return nid.doExtract(self._datasetMgrColumn
        raise Exception("Nuisance with id='"+id+"' not found in data group '"+self._label+"'! Check first with hasNuisance(id) that data group has the nuisance.")

    ##
    def setShapeHistoToRootFile(self, rootfile):
        print "setShapeHistoToRootFile not yet implemented"
        #FIXME

    ## Print debugging information
    def printDebug(self):
        print "Datagroup '"+self._label+"':"
        if self._landsProcess > -999:
            print "  process:", self._landsProcess
        print "  enabled for mass points:", self._enabledForMassPoints
        print "  rate counter:", self._rateCounter
        if len(self._nuisances) > 0:
            print "  nuisances:", self._nuisances
        print "  directory prefix for root file:", self._dirPrefix
        print "  shape histogram:", self._shapeHisto


    ## \var _additionalNormalisationFactor
    # Normalisation factor is multiplied by this factor (needed for EWK)
    ## \var _label
    # Label of column to be printed in datacard
    ## \var _enabledForMassPoints
    # List of mass points for which the column is enabled
    ## \var _rateId
    # Id of rate object
    ## \var _nuisances
    # List of nuisance Id's
    ## \var _datasetMgr
    # Path to files
    # FIXME continue doc