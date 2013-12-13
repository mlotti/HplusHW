## \package DatacardColumn
# Class collecting information about a column to be produced in the datacard
#

import os
import sys
from ROOT import TH1F
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.MulticrabPathFinder import MulticrabDirectoryDataType
from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.Extractor import ExtractorMode,CounterExtractor,ShapeExtractor,ConstantExtractor
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.systematics import ScalarUncertaintyItem,getBinningForPlot
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShellStyles import *
from math import sqrt,pow
from array import array


## ExtractorResult
# Helper class to cache the result for each extractor in each datacard column
class ExtractorResult():
    ## Constructor(
    def __init__(self, exId = "-1", masterId = "-1", result=None, histograms=None, resultIsStat=False):
        self._exId = exId
        self._masterId = masterId
        self._result = result
        self._resultIsStat = resultIsStat

        self._histograms = histograms # histograms going into the datacard root file
        self._tempHistos = [] # Needed to make histograms going into root file persistent

    def getId(self):
        return self._exId

    def getMasterId(self):
        return self._masterId

    def getResult(self):
        return self._result

    def getResultAverage(self):
        if isinstance(self._result, list):
            myValue = 0.0
            for r in self._result:
                myValue += abs(r)
            myValue = myValue / len(self._result)
            return myValue
        else:
            return self._result

    def resultIsStatUncertainty(self):
        return self._resultIsStat

    def getHistograms(self):
        return self._histograms

    def linkHistogramsToRootFile(self,rootfile):
        # Note: Do not call destructor for the tempHistos.
        #       Closing the root file to which they have been assigned to destructs them.
        #       i.e. it is enough to just clear the list.
        #self._tempHistos = []
        for h in self._histograms:
            htemp = h.Clone(h.GetTitle())
            htemp.SetDirectory(rootfile)
            self._tempHistos.append(htemp)

    def getContractedShapeUncertainty(self,hNominal):
        if len(self._histograms) == 0:
            return None
        myResidualSum = 0.0
        myAverageSum = 0.0
        if len(self._histograms) == 2:
            # Calculate average error as sqrt(sum((max-min)/2)**2) and central value as (max+min) / 2
            for i in range(0, self._histograms[0].GetNbinsX()+2):
                myResidualSum += pow((self._histograms[0].GetBinContent(i)-self._histograms[1].GetBinContent(i))/2,2)
                myAverageSum += hNominal.GetBinContent(i)
            if myAverageSum > 0:
                return sqrt(myResidualSum) / myAverageSum
            else:
                return 0.0
        return 0.0

# DatacardColumn class
class DatacardColumn():
    ## Constructor
    def __init__(self,
                 opts = None,
                 label = "",
                 landsProcess = -999,
                 enabledForMassPoints = [],
                 datasetType = 0,
                 nuisanceIds = [],
                 datasetMgrColumn = "",
                 additionalNormalisationFactor = 1.0,
                 shapeHisto = ""):
        self._opts = opts
        self._label = label
        self._landsProcess = landsProcess
        self._enabledForMassPoints = enabledForMassPoints
        if datasetType == "Observation":
            self._datasetType = MulticrabDirectoryDataType.OBSERVATION
        elif datasetType == "Signal":
            self._datasetType = MulticrabDirectoryDataType.SIGNAL
        elif datasetType == "Embedding":
            self._datasetType = MulticrabDirectoryDataType.EWKTAUS
        elif datasetType == "EWKfake":
            self._datasetType = MulticrabDirectoryDataType.EWKFAKETAUS
        elif datasetType == "QCD factorised":
            self._datasetType = MulticrabDirectoryDataType.QCDFACTORISED
        elif datasetType == "QCD inverted":
            self._datasetType = MulticrabDirectoryDataType.QCDINVERTED
        elif datasetType == "None":
            self._datasetType = MulticrabDirectoryDataType.DUMMY
        else:
            self._datasetType = MulticrabDirectoryDataType.UNKNOWN
        self._rateResult = None
        self._nuisanceIds = nuisanceIds
        self._nuisanceResults = [] # Of type ExtractorResult
        self._controlPlots = [] # Of type RootHistogramWithUncertainties
        self._cachedShapeRootHistogramWithUncertainties = None
        self._datasetMgrColumn = datasetMgrColumn
        self._additionalNormalisationFactor = additionalNormalisationFactor
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

    ## Returns true if the column is using the embedding data samples
    def typeIsEWKfake(self):
        return self._datasetType == MulticrabDirectoryDataType.EWKFAKETAUS

    ## Returns true if the column is QCD
    def typeIsQCD(self):
        return self._datasetType == MulticrabDirectoryDataType.QCDFACTORISED or self._datasetType == MulticrabDirectoryDataType.QCDINVERTED

    ## Returns true if the column is QCD factorised
    def typeIsQCDfactorised(self):
        return self._datasetType == MulticrabDirectoryDataType.QCDFACTORISED

    ## Returns true if the column is QCD inverted
    def typeIsQCDinverted(self):
        return self._datasetType == MulticrabDirectoryDataType.QCDINVERTED

    ## Returns true if the column is empty (uses no datasets)
    def typeIsEmptyColumn(self):
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
        if self._datasetMgrColumn == "" and not self.typeIsEmptyColumn():
            myMsg += "No dataset names defined!\n"
        if self.typeIsSignal() or self.typeIsEWK() or self.typeIsObservation():
            if self._shapeHisto == "":
                myMsg += "Missing or empty field 'shapeHisto'! (string) Name of histogram for shape \n"
#        elif self.typeIsQCDfactorised():
            # rate handled as spedial case, extra datasetMgrColumn are required for EWK MC
####        elif self._datasetType == MulticrabDirectoryDataType.QCDINVERTED:
####            myMsg += "FIXME: QCD inverted not implemented yet\n" # FIXME
        if not self.typeIsEmptyColumn() and not self.typeIsObservation():
            if self._nuisanceIds == None or len(self._nuisanceIds) == 0:
                myMsg += "Missing or empty field 'nuisances'! (list of strings) Id's for nuisances to be used for column\n"

        if myMsg != "":
            print ErrorStyle()+"Error (data group ='"+self._label+"'):"+NormalStyle()+"\n"+myMsg
            raise Exception()

    ## Returns true if column is enabled for given mass point
    def isActiveForMass(self, mass, config):
        myResult = (mass in self._enabledForMassPoints) and self._isPrintable
        # Ignore empty column for heavy H+
        myMassStatus = not (self.typeIsEmptyColumn() and (mass > 179 or config.OptionLimitOnSigmaBr))
        # Ignore HH if chosen in options
        myHHStatus = not (self._label[:2] == "HH" and (config.OptionRemoveHHDataGroup or config.OptionLimitOnSigmaBr))
        #print self._label,myResult,myMassStatus,myHHStatus
        return myResult and myMassStatus and myHHStatus

    ## Disables the datacard column
    def disable(self):
        self._isPrintable = False

    ## Returns label
    def getLabel(self):
        return self._label

    ## Returns LandS process
    def getLandsProcess(self):
        return self._landsProcess

    ## Returns the list of nuisance IDs
    def getNuisanceIds(self):
        return self._nuisanceIds

    ## Returns list of results for nuisances
    def getNuisanceResults(self):
        return self._nuisanceResults

    ## Returns the cached roto histogram with uncertainties object for the shape
    def getCachedShapeRootHistogramWithUncertainties(self):
        return self._cachedShapeRootHistogramWithUncertainties

    ## Returns dataset manager
    def getDatasetMgr(self):
        return self._datasetMgr

    ## Returns dataset manager column
    def getDatasetMgrColumn(self):
        return self._datasetMgrColumn

    ## Returns dataset manager column for MC EWK in QCD factorised
    def getDatasetMgrColumnForQCDMCEWK(self):
        return self._datasetMgrColumnForQCDMCEWK

    ## Get control plots
    def getControlPlotByIndex(self,index):
        return self._controlPlots[index]

    ## Get correct control plot
    def getControlPlotByTitle(self, title):
        for h in self._controlPlots:
            if title in h.getRootHisto().GetTitle():
                return h
        print "Available control plot names:"
        for h in self._controlPlots:
            print "  "+h.getRootHisto().GetTitle()
        raise Exception(ErrorStyle()+"Error:"+NormalStyle()+" Could not find control plot by title '%s' in column %s!"%(title, self._label))

    ## Do data mining and cache results
    def doDataMining(self, config, dsetMgr, luminosity, mainCounterTable, extractors, controlPlotExtractors):
        print "... processing column: "+HighlightStyle()+self._label+NormalStyle()
        # Check status for HH
        if self._label[:2] == "HH" and (config.OptionRemoveHHDataGroup or config.OptionLimitOnSigmaBr):
            print WarningLabel()+"Skipping ..."
            return
        # Obtain root histogram with uncertainties for shape and cache it
        if not (self.typeIsEmptyColumn() or dsetMgr == None):
            mySystematics = dataset.Systematics(allShapes=True) #,verbose=True)
            myDatasetRootHisto = dsetMgr.getDataset(self.getDatasetMgrColumn()).getDatasetRootHisto(mySystematics.histogram(self._shapeHisto))
            if myDatasetRootHisto.isMC():
                if (config.OptionLimitOnSigmaBr and self._label[:2] == "HW") or self._label[:2] == "Hp":
                     # Set cross section of sample to 1 pb in order to obtain limit on sigma x Br
                     dsetMgr.getDataset(self.getDatasetMgrColumn()).setCrossSection(1)
                     myDatasetRootHisto = dsetMgr.getDataset(self.getDatasetMgrColumn()).getDatasetRootHisto(mySystematics.histogram(self._shapeHisto))
                myDatasetRootHisto.normalizeToLuminosity(luminosity)
            self._cachedShapeRootHistogramWithUncertainties = myDatasetRootHisto.getHistogramWithUncertainties()
            # Apply additional normalization
            # Note: this applies the normalizatoin also to the syst. uncertainties
            if abs(self._additionalNormalisationFactor - 1.0) > 0.00001:
                print WarningLabel()+"Applying normalization factor %f to sample '%s'!"%(self._additionalNormalisationFactor, self.getLabel())
                self._cachedShapeRootHistogramWithUncertainties.Scale(self._additionalNormalisationFactor)
            # Rebin and move under/overflow bins to visible bins
            myArray = array("d",config.ShapeHistogramsDimensions)
            self._cachedShapeRootHistogramWithUncertainties.Rebin(len(config.ShapeHistogramsDimensions)-1,"",myArray)
            self._cachedShapeRootHistogramWithUncertainties.makeFlowBinsVisible()
        # Obtain rate histogram
        myRateHistograms = []
        if self.typeIsEmptyColumn() or dsetMgr == None:
            if self._opts.verbose:
                print "  - Creating empty rate shape"
            myArray = array("d",config.ShapeHistogramsDimensions)
            h = TH1F(self.getLabel(),self.getLabel(),len(myArray)-1,myArray)
            myRateHistograms.append(h)
        else:
            if self._opts.verbose:
                print "  - Extracting rate histogram"
            myShapeExtractor = None
            if self.typeIsObservation():
                myShapeExtractor = ShapeExtractor(ExtractorMode.OBSERVATION)
            else:
                myShapeExtractor = ShapeExtractor(ExtractorMode.RATE)
            myRateHistograms.extend(myShapeExtractor.extractHistograms(self, dsetMgr, mainCounterTable, luminosity, self._additionalNormalisationFactor))
        # Cache result
        self._rateResult = ExtractorResult("rate",
                                           "rate",
                                           myRateHistograms[0].Integral(), # Take only visible part
                                           myRateHistograms)
        if self.typeIsEmptyColumn() or dsetMgr == None:
            return

        # Obtain results for nuisances
        # Add the scalar uncertainties to the cached RootHistoWithUncertainties object
        for nid in self._nuisanceIds:
            if self._opts.verbose:
                print "  - Extracting nuisance by id=%s"%nid
            myFoundStatus = False
            for e in extractors:
                if e.getId() == nid:
                    myFoundStatus = True
                    # Obtain result
                    myResult = 0.0
                    if dsetMgr != None:
                        myResult = e.extractResult(self, dsetMgr, mainCounterTable, luminosity, self._additionalNormalisationFactor)
                    # Obtain histograms
                    myHistograms = []
                    if e.isShapeNuisance():
                        if isinstance(e, ConstantExtractor):
                            # Create up and down histograms out of the constant values
                            hUp = myRateHistograms[0].Clone()
                            hDown = myRateHistograms[0].Clone()
                            hUp.SetTitle(self.getLabel()+"_"+e._masterExID+"Up")
                            hDown.SetTitle(self.getLabel()+"_"+e._masterExID+"Down")
                            for k in range(0, hUp.GetNbinsX()):
                                myValue = hUp.GetBinContent(k)
                                hUp.SetBinContent(k, myValue * (1.0 + myResult.getUncertaintyUp()))
                                hUp.SetBinError(k, 0.0)
                                hDown.SetBinContent(k, myValue * (1.0 - myResult.getUncertaintyDown()))
                                hDown.SetBinError(k, 0.0)
                            myHistograms.append(hUp)
                            myHistograms.append(hDown)
                            # Add also to the uncertainties as normalization uncertainty
                            self._cachedShapeRootHistogramWithUncertainties.addNormalizationUncertaintyRelative(e.getId(), myResult.getUncertaintyUp(), myResult.getUncertaintyDown())
                        else:
                            # Apply any further scaling (only necessary for the unceratainties from variation)
                            if e.getDistribution() == "shapeQ" and abs(e.getScaleFactor() - 1.0) > 0.0:
                                self._cachedShapeRootHistogramWithUncertainties.ScaleVariationUncertainty(e._systVariation, e.getScaleFactor())
                            myHistograms = e.extractHistograms(self, dsetMgr, mainCounterTable, luminosity, self._additionalNormalisationFactor)
                            # Histograms constain abs uncertainty, need to add nominal histogram so that Lands accepts the histograms
                            if e.getDistribution() == "shapeQ":
                                for i in range(0,len(myHistograms)):
                                    myHistograms[i].Add(self._rateResult.getHistograms()[0])

                    else:
                        # Add scalar uncertainties
                        if self._opts.verbose:
                            print "Adding scalar uncert. ",e.getId()
                        if isinstance(myResult, ScalarUncertaintyItem):
                            self._cachedShapeRootHistogramWithUncertainties.addNormalizationUncertaintyRelative(e.getId(), myResult.getUncertaintyUp(), myResult.getUncertaintyDown())
                        elif isinstance(myResult, list):
                            self._cachedShapeRootHistogramWithUncertainties.addNormalizationUncertaintyRelative(e.getId(), myResult[1], myResult[0])
                        else:
                            self._cachedShapeRootHistogramWithUncertainties.addNormalizationUncertaintyRelative(e.getId(), myResult, myResult)
                    # Cache result
                    self._nuisanceResults.append(ExtractorResult(e.getId(),
                                                                 e.getMasterId(),
                                                                 myResult,
                                                                 myHistograms,
                                                                 "Stat." in e.getDescription() or "stat." in e.getDescription() or e.getDistribution()=="shapeStat"))
            if not myFoundStatus:
                raise Exception("\n"+ErrorLabel()+"(data group ='"+self._label+"'): Cannot find nuisance with id '"+nid+"'!")
        # Print list of uncertainties
        if self._opts.verbose and dsetMgr != None and not self.typeIsEmptyColumn():
            print "  - Has shape variation syst. uncertainties: %s"%(", ".join(map(str,self._cachedShapeRootHistogramWithUncertainties.getShapeUncertainties().keys())))
            print "  - Has shape squared syst. uncertainties: %s"%(", ".join(map(str,self._cachedShapeRootHistogramWithUncertainties._shapeUncertaintyAbsoluteNames)))
        # Obtain results for control plots
        if config.OptionDoControlPlots:
            for c in controlPlotExtractors:
                if dsetMgr != None and not self.typeIsEmptyColumn():
                    if self._opts.verbose:
                        print "  - Extracting data-driven control plot %s"%c._histoTitle

                    myCtrlDsetRootHisto = c.extractHistograms(self, dsetMgr, mainCounterTable, luminosity, self._additionalNormalisationFactor)
                    # Now normalize
                    if myDatasetRootHisto.isMC():
                        myCtrlDsetRootHisto.normalizeToLuminosity(luminosity)
                    h = myCtrlDsetRootHisto.getHistogramWithUncertainties()
                    # Rebin and move under/overflow bins to visible bins
                    myArray = array("d",getBinningForPlot(c._histoName))
                    h.Rebin(len(myArray)-1,"",myArray)
                    h.makeFlowBinsVisible()
                    # Apply any further scaling (only necessary for the unceratainties from variation)
                    for nid in self._nuisanceIds:
                        for e in extractors:
                            if e.getId() == nid:
                                if e.getDistribution() == "shapeQ" and abs(e.getScaleFactor() - 1.0) > 0.0:
                                    h.ScaleVariationUncertainty(e._systVariation, e.getScaleFactor())
                    # Add to RootHistogramWithUncertainties non-shape uncertainties
                    for n in self._nuisanceResults:
                        if not n.resultIsStatUncertainty() and len(n.getHistograms()) == 0: # systematic uncert., but not shapeQ
                            if self._opts.verbose:
                                print "    - Adding norm. uncertainty: %s"%n.getMasterId()
                            myResult = n.getResult()
                            if isinstance(myResult, ScalarUncertaintyItem):
                                h.addNormalizationUncertaintyRelative(n.getMasterId(), myResult.getUncertaintyUp(), myResult.getUncertaintyDown())
                            elif isinstance(myResult, list):
                                h.addNormalizationUncertaintyRelative(n.getMasterId(), myResult[1], myResult[0])
                            else:
                                h.addNormalizationUncertaintyRelative(n.getMasterId(), myResult, myResult)
                        elif not n.resultIsStatUncertainty() and len(n.getHistograms()) > 0 and isinstance(n.getResult(), ScalarUncertaintyItem): # constantToShape
                            if self._opts.verbose:
                                print "    - Adding norm. uncertainty: %s"%n.getMasterId()
                            myResult = n.getResult()
                            h.addNormalizationUncertaintyRelative(n.getMasterId(), myResult.getUncertaintyUp(), myResult.getUncertaintyDown())
                    # Scale if asked
                    if not (config.OptionLimitOnSigmaBr and self._label[:2] == "HW") or self._label[:2] == "Hp":
                        h.Scale(self._additionalNormalisationFactor)
                    # Store RootHistogramWithUncertainties
                    self._controlPlots.append(h)

    ## Returns rate for column
    def getRateResult(self):
        if self._rateResult == None:
            raise Exception(ErrorStyle()+"Error (data group ='"+self._label+"'):"+NormalStyle()+" Rate value has not been cached! (did you forget to call doDataMining()?)")
        if self._rateResult.getResult() == None:
            raise Exception(ErrorStyle()+"Error (data group ='"+self._label+"'):"+NormalStyle()+" Rate value has not been cached! (did you forget to call doDataMining()?)")
        return self._rateResult.getResult()

    ## Returns rate histogram for column
    def getRateHistogram(self):
        if self._rateResult == None:
            raise Exception(ErrorStyle()+"Error (data group ='"+self._label+"'):"+NormalStyle()+" Rate value has not been cached! (did you forget to call doDataMining()?)")
        if self._rateResult.getHistograms() == None:
            raise Exception(ErrorStyle()+"Error (data group ='"+self._label+"'):"+NormalStyle()+" Rate histograms have not been cached! (did you forget to call doDataMining()?)")
        return self._rateResult.getHistograms()[0]

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
        raise Exception("Nuisance with id='"+id+"' not found in data group '"+self._label+"'! Check first with hasNuisance(id) that data group has the nuisance.")

    ## Returns full nuisance for column (as string)
    def getFullNuisanceResultByMasterId(self, id):
        if self._nuisanceResults == None:
            raise Exception(ErrorStyle()+"Error (data group ='"+self._label+"'):"+NormalStyle()+" Nuisance values have not been cached! (did you forget to call doDataMining()?)")
        if len(self._nuisanceResults) == 0:
            raise Exception(ErrorStyle()+"Error (data group ='"+self._label+"'):"+NormalStyle()+" Nuisance values have not been cached! (did you forget to call doDataMining()?)")
        for result in self._nuisanceResults:
            if id == result.getMasterId():
                return result
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
        if len(self._nuisanceIds) > 0:
            print "  nuisances:", self._nuisanceIds
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
