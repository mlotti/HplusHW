## \package DatacardColumn
# Class collecting information about a column to be produced in the datacard
#

import os
import sys

from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.MulticrabPathFinder import MulticrabDirectoryDataType
from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.Extractor import ExtractorMode,CounterExtractor,ShapeExtractor
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShellStyles import *

## ExtractorResult
# Helper class to cache the result for each extractor in each datacard column
class ExtractorResult():
    ## Constructor(
    def __init__(self, exId = "-1", masterId = "-1", result=None, histograms=None):
        self._exId = exId
        self._masterId = masterId
        self._result = result
        self._histograms = histograms
        self._tempHistos = [] # Needed to make histograms going into root file persistent

    def getId(self):
        return self._exId

    def getMasterId(self):
        return self._masterId

    def getResult(self):
        return self._result

    def linkHistogramsToRootFile(self,rootfile):
        # Note: Do not call destructor for the tempHistos.
        #       Closing the root file to which they have been assigned to destructs them.
        #       i.e. it is enough to just clear the list.
        self._tempHistos = [] 
        for h in self._histograms:
            htemp = h.Clone(h.GetTitle())
            htemp.SetDirectory(rootfile)
            self._tempHistos.append(htemp)

# DatacardColumn class
class DatacardColumn():
    ## Constructor
    def __init__(self,
                 label = "",
                 landsProcess = -999,
                 enabledForMassPoints = [],
                 datasetType = 0,
                 rateCounter = "",
                 nuisanceIds = [],
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
        self._rateResult = None
        self._nuisanceIds = nuisanceIds
        self._nuisanceResults = []
        self._datasetMgrColumn = datasetMgrColumn
        self._datasetMgrColumnForQCDMCEWK  = datasetMgrColumnForQCDMCEWK
        self._additionalNormalisationFactor = additionalNormalisationFactor
        self._dirPrefix = dirPrefix
        self._shapeHisto = shapeHisto
        self._isPrintable = True

        self.checkInputValidity()

    ## Returns true if the column is using the observation data samples
    def typeIsObservation(self):
        return self._datasetType == MulticrabDirectoryDataType.OBSERVATION

    ## Returns true if the column is using the signal data samples
    def typeIsSignal(self):
        return self._datasetType == MulticrabDirectoryDataType.SIGNAL

    ## Returns true if the column is using the embedding data samples
    def typeIsEWK(self):
        return self._datasetType == MulticrabDirectoryDataType.EWKTAUS

    ## Returns true if the column is QCD
    def typeIsQCD(self):
        return self._datasetType == MulticrabDirectoryDataType.QCDFACTORISED or self._datasetType == MulticrabDirectoryDataType.QCDINVERTED

    ## Returns true if the column is empty (uses no datasets)
    def typeIsEmptyColum(self):
        return self._datasetType == MulticrabDirectoryDataType.DUMMY

    ## Checks that required fields have been supplied
    def checkInputValidity(self):
        myMsg = ""
        if self._label == "":
            myMsg += "Missing or empty field 'label'! (string) to be printed on a column in datacard\n"
        if not self.typeIsObservation():
            if self._landsProcess == -999:
                myMsg += "Missing or empty field 'landsProcess'! (integer) to be printed as process in datacard\n"
        if len(self._enabledForMassPoints) == 0:
            myMsg += "Missing or empty field 'validMassPoints'! (list of integers) specifies for which mass points the column is enabled\n"
        if self._datasetType == MulticrabDirectoryDataType.UNKNOWN:
            myMsg += "Wrong 'datasetType' specified! Valid options are 'Signal', 'Embedding', 'QCD factorised', 'QCD inverted', and 'None'\n"
        if self._datasetMgrColumn == "":
            myMsg += "No dataset names defined!\n"
        if self.typeIsSignal() or self.typeIsEWK() or self.typeIsObservation():
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
        if not self.typeIsEmptyColum() and not self.typeIsObservation():
            if len(self._nuisanceIds) == 0:
                myMsg += "Missing or empty field 'nuisances'! (list of strings) Id's for nuisances to be used for column\n"

        if myMsg != "":
            print ErrorStyle()+"Error (data group ='"+self._label+"'):"+NormalStyle()+"\n"+myMsg
            sys.exit()

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

    ## Returns the label of the counter from which to look up the rate
    def getRateCounterItem(self):
        return self._rateCounter

    ## Returns the list of nuisance IDs
    def getNuisances(self):
        return self._nuisances

    ## Returns dataset manager
    def getDatasetMgr(self):
        return self._datasetMgr

    ## Returns dataset manager column
    def getDatasetMgrColumn(self):
        return self._datasetMgrColumn

    ## Returns dataset manager column for MC EWK in QCD factorised
    def getDatasetMgrColumnForQCDMCEWK(self):
        return self._datasetMgrColumnForQCDMCEWK

    ## Do data mining and cache results
    def doDataMining(self, config, dsetMgr, luminosity, mainCounterTable, extractors):
        # Obtain rate
        #sys.stdout.write("\r... data mining in progress: Column="+self._label+", obtaining Rate...                                                          ")
        #sys.stdout.flush()
        myRateResult = None
        myRateHistograms = []
        if self.typeIsEmptyColum():
            myRateResult = 0.0
            myShapeExtractor = ShapeExtractor(config.ShapeHistogramsDimensions, self._rateCounter, [], [], ExtractorMode.RATE, description="empty")
            myRateHistograms.extend(myShapeExtractor.extractHistograms(self, dsetMgr, mainCounterTable, luminosity, self._additionalNormalisationFactor))
        elif self.typeIsQCD():
            print WarningStyle()+"Warning: rate not implemented for QCD yet, setting rate to zero"+NormalStyle()  #FIXME
            myRateResult = 0.0
            myShapeExtractor = ShapeExtractor(config.ShapeHistogramsDimensions, self._rateCounter, [], [], ExtractorMode.RATE, description="empty")
            myRateHistograms.extend(myShapeExtractor.extractHistograms(self, dsetMgr, mainCounterTable, luminosity, self._additionalNormalisationFactor))
        else:
            myExtractor = None
            myShapeExtractor = None
            if self.typeIsObservation():
                myExtractor = CounterExtractor(self._rateCounter, ExtractorMode.OBSERVATION)
                myShapeExtractor = ShapeExtractor(config.ShapeHistogramsDimensions, self._rateCounter, [self._dirPrefix], [self._shapeHisto], ExtractorMode.OBSERVATION)
            else:
                myExtractor = CounterExtractor(self._rateCounter, ExtractorMode.RATE)
                myShapeExtractor = ShapeExtractor(config.ShapeHistogramsDimensions, self._rateCounter, [self._dirPrefix], [self._shapeHisto], ExtractorMode.RATE)
            myRateResult = myExtractor.extractResult(self, dsetMgr, mainCounterTable, luminosity, self._additionalNormalisationFactor)
            myRateHistograms.extend(myShapeExtractor.extractHistograms(self, dsetMgr, mainCounterTable, luminosity, self._additionalNormalisationFactor))
        # Cache result
        self._rateResult = ExtractorResult("rate",
                                           "rate",
                                           myRateResult,
                                           myRateHistograms)
        # Obtain nuisances
        for nid in self._nuisanceIds:
            #sys.stdout.write("\r... data mining in progress: Column="+self._label+", obtaining Nuisance="+nid+"...                                              ")
            #sys.stdout.flush()
            myFoundStatus = False
            for e in extractors:
                if e.getId() == nid:
                    myFoundStatus = True
                    # Obtain result
                    myResult = e.extractResult(self, dsetMgr, mainCounterTable, luminosity, self._additionalNormalisationFactor)
                    # Obtain histograms
                    myHistograms = []
                    if e.isShapeNuisance():
                        myHistograms.extend(e.extractHistograms(self, dsetMgr, mainCounterTable, luminosity, self._additionalNormalisationFactor))
                    # Cache result
                    self._nuisanceResults.append(ExtractorResult(e.getId(),
                                                                 e.getMasterId(),
                                                                 myResult,
                                                                 myHistograms))
            if not myFoundStatus:
                print "\n"+ErrorStyle()+"Error (data group ='"+self._label+"'):"+NormalStyle()+" Cannot find nuisance with id '"+nid+"'!"
                sys.exit()
        #print "\nData mining done"

    ## Returns rate for column
    def getRateResult(self):
        if self._rateResult == None:
            raise Exception(ErrorStyle()+"Error (data group ='"+self._label+"'):"+NormalStyle()+" Rate value has not been cached! (did you forget to call doDataMining()?)")
        if self._rateResult.getResult() == None:
            raise Exception(ErrorStyle()+"Error (data group ='"+self._label+"'):"+NormalStyle()+" Rate value has not been cached! (did you forget to call doDataMining()?)")
        return self._rateResult.getResult()

    ## Returns true if column has a nuisance Id
    def hasNuisanceByMasterId(self, id):
        for result in self._nuisanceResults:
            if id == result.getMasterId():
                return True
        return False

    ## Returns nuisance for column (as string)
    def getNuisanceResultByMasterId(self, id):
        if self._nuisanceResults == None:
            raise Exception(ErrorStyle()+"Error (data group ='"+self._label+"'):"+NormalStyle()+" Nuisance values have not been cached! (did you forget to call doDataMining()?)")
        if len(self._nuisanceResults) == 0:
            raise Exception(ErrorStyle()+"Error (data group ='"+self._label+"'):"+NormalStyle()+" Nuisance values have not been cached! (did you forget to call doDataMining()?)")
        for result in self._nuisanceResults:
            if id == result.getMasterId():
                return result.getResult()
                #return nid.doExtract(self._datasetMgrColumn
        raise Exception("Nuisance with id='"+id+"' not found in data group '"+self._label+"'! Check first with hasNuisance(id) that data group has the nuisance.")

    ## Stores the cached result histograms to root file
    def setResultHistogramsToRootFile(self, rootfile):
        if self._rateResult == None:
            raise Exception(ErrorStyle()+"Error (data group ='"+self._label+"'):"+NormalStyle()+" Rate value has not been cached! (did you forget to call doDataMining()?)")
        if self._rateResult.getResult() == None:
            raise Exception(ErrorStyle()+"Error (data group ='"+self._label+"'):"+NormalStyle()+" Rate value has not been cached! (did you forget to call doDataMining()?)")
        # Set rate histogram
        self._rateResult.linkHistogramsToRootFile(rootfile)
        # Set nuisance histograms
        for result in self._nuisanceResults:
            result.linkHistogramsToRootFile(rootfile)

    ## Print debugging information
    def printDebug(self):
        print "Datagroup '"+self._label+"':"
        if self._landsProcess > -999:
            print "  process:", self._landsProcess
        print "  enabled for mass points:", self._enabledForMassPoints
        print "  rate counter:", self._rateCounter
        if len(self._nuisanceIds) > 0:
            print "  nuisances:", self._nuisanceIds
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