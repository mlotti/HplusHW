'''
DESCRIPTION:
Class collecting information about a column to be produced in the datacard

USAGE:
Imported by other python files (HiggsAnalysis/NtupleAnalysis/src/LimitCalc/python/DataCardGenerator.py)

'''

#================================================================================================
# Import modules
#================================================================================================
import os
import sys
import ROOT
import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
from HiggsAnalysis.LimitCalc.MulticrabPathFinder import MulticrabDirectoryDataType
from HiggsAnalysis.LimitCalc.Extractor import ExtractorMode,CounterExtractor,ShapeExtractor,QCDShapeVariationExtractor,ConstantExtractor,ShapeVariationFromJsonExtractor,ShapeVariationToConstantExtractor
from HiggsAnalysis.NtupleAnalysis.tools.systematics import ScalarUncertaintyItem,getBinningForPlot
import HiggsAnalysis.NtupleAnalysis.tools.ShellStyles as ShellStyles
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux
import HiggsAnalysis.NtupleAnalysis.tools.crosssection as xsect
import HiggsAnalysis.NtupleAnalysis.tools.histogramsExtras as histogramExtras
import HiggsAnalysis.QCDMeasurement.systematicsForMetShapeDifference as systematicsForMetShapeDifference
from math import sqrt,pow
from array import array

_fineBinningSuffix = "_fineBinning"
debug = False

#================================================================================================
# Class definition
#================================================================================================
def Verbose(msg, printHeader=False):
    '''
    Calls Print() only if verbose options is set to true
    '''
    #if not opts.verbose:
    if not debug:
        return
    Print(msg, printHeader)
    return


def Print(msg, printHeader=True):
    '''
    Simple print function. If verbose option is enabled prints, otherwise does nothing.
    '''
    fName = __file__.split("/")[-1]
    if printHeader:
        print "=== ", fName
    print "\t", msg
    return


class ExtractorResult():
    '''
    Helper class to cache the result for each extractor in each datacard column
    '''
    def __init__(self, exId = "-1", masterId = "-1", result=None, histograms=None, resultIsStat=False, additionalResult=None):
        ''' 
        Constructor
        '''
        self._exId = exId
        self._masterId = masterId
        self._result = result
        self._additionalResult = additionalResult
        self._resultIsStat = resultIsStat
        self._purityHistogram = None # Only used for QCD

        self._histograms = histograms # histograms going into the datacard root file
        self._tempHistos = [] # Needed to make histograms going into root file persistent

    def delete(self):
        if self._purityHistogram != None:
            self._purityHistogram.Delete()
            self._purityHistogram = None

    def getId(self):
        return self._exId

    def getMasterId(self):
        return self._masterId

    def getResult(self):
        return self._result

    def getAdditionalResult(self):
        return self._additionalResult

    def setPurityHistogram(self, h):
        self._purityHistogram = h

    def getPurityHistogram(self):
        return self._purityHistogram

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

    def getFinalBinningHistograms(self, blackList=[]):
        myMinBins = 999
        for h in self._histograms:
            if h.GetNbinsX() < myMinBins:
                myMinBins = h.GetNbinsX()
        myList = []
        for h in self._histograms:
            if h.GetNbinsX() == myMinBins:
                myStatus = True
                for item in blackList:
                    if item in h.GetName():
                        myStatus = False
                if myStatus:
                    myList.append(h)
        return myList

    def getFineBinnedHistograms(self, blackList=[]):
        myMinBins = 999
        for h in self._histograms:
            if h.GetNbinsX() < myMinBins:
                myMinBins = h.GetNbinsX()
        myList = []
        for h in self._histograms:
            if h.GetNbinsX() > myMinBins:
                myStatus = True
                for item in blackList:
                    if item in h.GetName():
                        myStatus = False
                if myStatus:
                    myList.append(h)

        return myList

    def linkHistogramsToRootFile(self,rootfile):
        # Note: Do not call destructor for the tempHistos.
        #       Closing the root file to which they have been assigned to destructs them.
        #       i.e. it is enough to just clear the list.
        #self._tempHistos = []
        for h in self._histograms:
            htemp = aux.Clone(h, h.GetTitle())
            htemp.SetDirectory(rootfile)
            self._tempHistos.append(htemp)

    def debug(self):
        print "Cached results:"
        print "- shape histos:",len(self._histograms)
        print "- purity histos (QCD):",self._purityHistogram
        print "- tmp histos:",len(self._tempHistos)

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

class DatacardColumn():
    def __init__(self,
                 opts = None,
                 label = "",
                 landsProcess = -999,
                 enabledForMassPoints = [],
                 datasetType = 0,
                 nuisanceIds = [],
                 datasetMgrColumn = "",
                 additionalNormalisationFactor = 1.0,
                 histoPath = "",
                 shapeHistoName = ""):
        '''
        Constructor
        '''
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
        elif datasetType == "QCD MC":
            self._datasetType = MulticrabDirectoryDataType.QCDMC
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
        self._histoPath = histoPath
        self._shapeHistoName = shapeHistoName
        self._isPrintable = True
        self.checkInputValidity()

    def delete(self):
        self._rateResult.delete()
        self._nuisanceIds = None
        self._nuisanceResults = None
        self._controlPlots = None
        self._cachedShapeRootHistogramWithUncertainties.delete()
        self._cachedShapeRootHistogramWithUncertainties = None
        self._datasetMgrColumn = None

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
        return self._datasetType == MulticrabDirectoryDataType.QCDMC or self._datasetType == MulticrabDirectoryDataType.QCDINVERTED

    ## Returns true if the column is QCD MC
    def typeIsQCDMC(self):
        return self._datasetType == MulticrabDirectoryDataType.QCDMC

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
            myMsg += "Wrong 'datasetType' specified! Valid options are 'Signal', 'Embedding', 'QCD MC', 'QCD inverted', and 'None'\n"
        if self._datasetMgrColumn == "" and not self.typeIsEmptyColumn():
            myMsg += "No dataset names defined!\n"
        if self.typeIsSignal() or self.typeIsEWK() or self.typeIsObservation():
            if self._shapeHistoName == "":
                myMsg += "Missing or empty field 'shapeHistoName'! (string) Name of histogram for shape \n"
            if self._histoPath == "":
                myMsg += "Missing or empty field 'histoPath'! (string) Path to histogram(s) \n"
        if not self.typeIsEmptyColumn() and not self.typeIsObservation():
            if self._nuisanceIds == None:
                myMsg += "Missing field 'nuisances'! (list of strings) Id's for nuisances to be used for column\n"
            if len(self._nuisanceIds) == 0:
                myWarning = "Empty field 'nuisances'! (list of strings) Id's for nuisances to be used for column\n"
                print ShellStyles.WarningStyle()+"Warning (data group ='"+self._label+"'):"+ShellStyles.NormalStyle()+"\n"+myWarning
        if myMsg != "":
            print ShellStyles.ErrorStyle()+"Error (data group ='"+self._label+"'):"+ShellStyles.NormalStyle()+"\n"+myMsg
            raise Exception()
        return


    def isActiveForMass(self, mass, config):
        '''
        Returns true if column is enabled for given mass point
        '''
        myResult = (mass in self._enabledForMassPoints) and self._isPrintable
        # Ignore empty column for heavy H+
        myMassStatus = not (self.typeIsEmptyColumn() and (mass > 179 or config.OptionLimitOnSigmaBr))
        #print self._label,myResult,myMassStatus
        return myResult and myMassStatus and self.getLandsProcess != None

    def disable(self):
        '''
        Disables the datacard column
        '''
        self._isPrintable = False
        return

    def getLabel(self):
        '''
        Returns label
        '''
        return self._label

    def getFullShapeHistoName(self):
        '''
        Return shape histogram name with path
        '''
        return os.path.join(self._histoPath, self._shapeHistoName)

    def getFullHistoName(self, histoName):
        '''
        Return shape histogram name with path
        '''
        return os.path.join(self._histoPath, histoName)

    def getLandsProcess(self):
        '''
        Returns LandS process
        '''
        return self._landsProcess

    def getNuisanceIds(self):
        '''
        Returns the list of nuisance IDs
        '''
        return self._nuisanceIds

    def getNuisanceResults(self):
        '''
        Returns list of results for nuisances
        '''
        return self._nuisanceResults

    def getCachedShapeRootHistogramWithUncertainties(self):
        '''
        Returns the cached ROOT histogram with uncertainties object for the shape
        '''
        return self._cachedShapeRootHistogramWithUncertainties

    def getDatasetMgr(self):
        '''
        Returns dataset manager
        '''
        return self._datasetMgr

    def getDatasetMgrColumn(self):
        '''
        Returns dataset manager column
        '''
        return self._datasetMgrColumn

    def getDatasetMgrColumnForQCDMCEWK(self):
        '''
        Returns dataset manager column for MC EWK in QCD 
        '''
        return self._datasetMgrColumnForQCDMCEWK

    def getControlPlotByIndex(self,index):
        '''        
        Get control plots
        '''
        if index >= len(self._controlPlots):
            return None
        return self._controlPlots[index]

    def getControlPlotByTitle(self, title):
        '''
        Get correct control plot
        '''
        for h in self._controlPlots:
            if title in h.getRootHisto().GetTitle():
                return h

        print "Available control plot names:"
        for h in self._controlPlots:
            print "  " + h.getRootHisto().GetTitle()

        msg = "Could not find control plot by title '%s' in column %s!" % (title, self._label)
        raise Exception(ErrorLabel() + msg)
    
    def _createShapeNuisanceFromConstant(self, hRate, uncertaintyUp, uncertaintyDown, suffix=""):
        '''
        Creates an up and down variation histogram from a constant nuisance parameters
        Returns list of created histograms
        '''
        myNamePrefix = self.getLabel()+"_"+e._masterExID
        hUp = aux.Clone(hRate, myNamePrefix+"Up"+suffix)
        hDown = aux.Clone(hRate, myNamePrefix+"Down"+suffix)
        hUp.SetTitle(myNamePrefix+"Up"+suffix)
        hDown.SetTitle(myNamePrefix+"Down"+suffix)
        for k in range(0, hUp.GetNbinsX()+2):
            myValue = hUp.GetBinContent(k)
            hUp.SetBinContent(k, myValue * (1.0 + uncertaintyUp))
            hUp.SetBinError(k, 0.01)
            hDown.SetBinContent(k, myValue * (1.0 - uncertaintyDown))
            hDown.SetBinError(k, 0.01)
        return [hUp, hDown]

    def _getShapeNuisanceHistogramsFromRHWU(self, rhwu, systVariationName, masterExtractorId, suffix=""):
        myHistograms = []
        myShapeUncertDict = rhwu.getShapeUncertainties()
        # Check that asked variation exists
        if not systVariationName in myShapeUncertDict.keys():
            msg  = "DatasetColumn '%s': Cannot find systematics variation %s, " % (self.getLabel(), systVariationName)
            msg += "check that options in the datacard match to multicrab content"
            msg += "(to run without shape systematics, set OptionIncludeSystematics to False)!"
            raise Exception(ShellStyles.ErrorLabel()+msg)

        # Get histograms
        (hSystUp, hSystDown) = myShapeUncertDict[systVariationName]
        myNamePrefix = self.getLabel()+"_"+masterExtractorId
        hUp = aux.Clone(hSystUp, myNamePrefix+"Up"+suffix)
        hDown = aux.Clone(hSystDown, myNamePrefix+"Down"+suffix)
        hUp.SetTitle(myNamePrefix+"Up"+suffix)
        hDown.SetTitle(myNamePrefix+"Down"+suffix)

        # Do not apply here additional normalization, it has already been applied
        # via RootHistoWithUncertainties.Scale() in DatacardColumn::doDataMining()
        # Append histograms to output list
        myHistograms.append(hUp)
        myHistograms.append(hDown)

        return myHistograms

    def doDataMining(self, config, dsetMgr, luminosity, mainCounterTable, extractors, controlPlotExtractors):
        '''
        Do data mining and cache results
        '''
        if self._opts.verbose:
            print "... processing column: " + ShellStyles.HighlightStyle() + self._label+ShellStyles.NormalStyle()

        # beginFilesSize = ROOT.gROOT.GetListOfFiles().GetSize()
        # beginListSize  = ROOT.gDirectory.GetList().GetSize()
        # beginKeys        = ROOT.gDirectory.GetListOfKeys()
        #for i, key in enumerate(beginKeys):
        #   print "key %d = %s" % (i, key.GetTitle())
        
        # Construct list of shape variables used by the column
        myShapeVariationList = []
        for nid in self._nuisanceIds:
            for e in extractors:
                if e.getId() == nid:
                    if (e.getDistribution() == "shapeQ" and not isinstance(e, ConstantExtractor)) or isinstance(e, ShapeVariationToConstantExtractor):
                        myShapeVariationList.append(e._systVariation)

        # Obtain root histogram with uncertainties for shape and cache it
        hRateWithFineBinning = None
        if not (self.typeIsEmptyColumn() or dsetMgr == None):
            mySystematics = dataset.Systematics(allShapes=True) #,verbose=True)
            if not dsetMgr.hasDataset(self.getDatasetMgrColumn()):
                msg = "Cannot find merged dataset by key '%s' in multicrab dir! Did you forget to merge the root files with hplusMergeHistograms.py?" % self.getDatasetMgrColumn()
                raise Exception(ShellStyles.ErrorLabel() + msg)
            myDatasetRootHisto = dsetMgr.getDataset(self.getDatasetMgrColumn()).getDatasetRootHisto(mySystematics.histogram(self.getFullShapeHistoName()))

            if myDatasetRootHisto.isMC():
                # Set signal xsection
                # for heavy H+
                if config.OptionLimitOnSigmaBr:
                    if self._landsProcess <= 0:
                        # Set cross section of sample to 1 pb in order to obtain limit on sigma x Br
                        #myDatasetRootHisto.Delete()
                        dsetMgr.getDataset(self.getDatasetMgrColumn()).setCrossSection(1)
                        myDatasetRootHisto = dsetMgr.getDataset(self.getDatasetMgrColumn()).getDatasetRootHisto(mySystematics.histogram(self.getFullShapeHistoName()))
                        if self._opts.verbose:
                            print "..... Assuming this is signal -> set cross section to 1 pb for limit calculation"
                # for light H+, use 13 TeV ttbar xsect from https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO
                elif (not config.OptionLimitOnSigmaBr and (self._label[:2] == "HW" or self._label[:2] == "HH" or self._label[:2] == "WH")):
                     ttbarxsect = xsect.backgroundCrossSections.crossSection("TT", energy="13")
                     if abs(dsetMgr.getDataset(self.getDatasetMgrColumn()).getCrossSection() - ttbarxsect) > 0.0001:
                         print ShellStyles.WarningLabel()+"Forcing light H+ xsection to 13 TeV ttbar cross section %f in DatacardColumn.py"%ttbarxsect
                         dsetMgr.getDataset(self.getDatasetMgrColumn()).setCrossSection(ttbarxsect)
                         myDatasetRootHisto = dsetMgr.getDataset(self.getDatasetMgrColumn()).getDatasetRootHisto(mySystematics.histogram(self.getFullShapeHistoName()))


                # Normalize to luminosity
                myDatasetRootHisto.normalizeToLuminosity(luminosity)

            self._cachedShapeRootHistogramWithUncertainties = myDatasetRootHisto.getHistogramWithUncertainties().Clone()
            # Remove any variations not active for the column
            self._cachedShapeRootHistogramWithUncertainties.keepOnlySpecifiedShapeUncertainties(myShapeVariationList)
            # Apply additional normalization
            # Note: this applies the normalizatoin also to the syst. uncertainties
            if abs(self._additionalNormalisationFactor - 1.0) > 0.00001:
                print ShellStyles.WarningLabel()+"Applying normalization factor %f to sample '%s'!"%(self._additionalNormalisationFactor, self.getLabel())
                self._cachedShapeRootHistogramWithUncertainties.Scale(self._additionalNormalisationFactor)
            # Leave histograms with the original binning at this stage, but do move under/overflow into first/last bin
            self._cachedShapeRootHistogramWithUncertainties.makeFlowBinsVisible()
	    if not self.typeIsObservation():
                if self._opts.verbose:
                    rate = self._cachedShapeRootHistogramWithUncertainties.getRate()
                    statUncert = self._cachedShapeRootHistogramWithUncertainties.getRateStatUncertainty()
                    print "..... event yield: %f +- %f (stat.)" % (rate, statUncert)

        # Obtain rate histogram
        myRateHistograms = []
        if self.typeIsEmptyColumn() or dsetMgr == None:
            if self._opts.verbose:
                print "  - Creating empty rate shape"
            #myArray = array("d",config.ShapeHistogramsDimensions)
            #h = TH1F(self.getLabel(),self.getLabel(),len(myArray)-1,myArray)
            # Use here just one bin to speed up LandS (yes, one needs a histogram for the empty columns even if ShapeStat is off)
            h = ROOT.TH1F(self.getLabel(),self.getLabel(),1,0,1)
            ROOT.SetOwnership(h, True)
            myRateHistograms.append(h)
        else:
            if self._opts.verbose:
                print "  - Extracting rate histogram"
            myShapeExtractor = None
            if self.typeIsObservation():
                myShapeExtractor = ShapeExtractor(ExtractorMode.OBSERVATION)
            else:
                myShapeExtractor = ShapeExtractor(ExtractorMode.RATE)
            myShapeHistograms = myShapeExtractor.extractHistograms(self, dsetMgr, mainCounterTable, luminosity, self._additionalNormalisationFactor)
            myRateHistograms.extend(myShapeHistograms)
        # Cache result
        self._rateResult = ExtractorResult("rate", "rate",
                               myRateHistograms[0].Integral(), # Take only visible part
                               myRateHistograms)
        if self._opts.verbose:
            print "  - Rate: integral = ", myRateHistograms[0].Integral()
            if (self.typeIsEWK()) or self.typeIsEWKfake():
                if isinstance(dsetMgr.getDataset(self.getDatasetMgrColumn()), dataset.DatasetMerged):
                    for dset in dsetMgr.getDataset(self.getDatasetMgrColumn()).datasets:
                        print "  - normalization coefficient for %s: %g"%(dset.getName(),dset.getNormFactor())
                
                isMC = dsetMgr.getDataset(self.getDatasetMgrColumn()).isMC()
                if (isMC):
                    print "  - normalization coefficient = ", dsetMgr.getDataset(self.getDatasetMgrColumn()).getNormFactor()
                else:
                    print "  - normalization coefficient = N/A (isMC=%s)" % (isMC)

        if abs(myRateHistograms[0].Integral() - myRateHistograms[0].Integral(0,myRateHistograms[0].GetNbinsX()+2)) > 0.00001:
            raise Exception("Error: under/overflow bins contain data!")
        if self.typeIsEmptyColumn() or dsetMgr == None:
            return

        # Obtain overall purity for QCD
        self._purityForFinalShape = None
        myAveragePurity = None
        try:
            if self.typeIsQCDinverted():
                myDsetRootHisto = myShapeExtractor.extractQCDPurityHistogram(self, dsetMgr, self.getFullShapeHistoName())
                self._rateResult.setPurityHistogram(myDsetRootHisto.getHistogram())
                myAveragePurity = myShapeExtractor.extractQCDPurityAsValue(myRateHistograms[0], self.getPurityHistogram())
                #print "*** Average QCD purity", myAveragePurity
        except:
            print "ERROR: It looks like the purity histogram does not exist!"
            raise

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
                    myAdditionalResult = None
                    if dsetMgr != None:
                        myResult = e.extractResult(self, dsetMgr, mainCounterTable, luminosity, self._additionalNormalisationFactor)
                        myAdditionalResult = e.extractAdditionalResult(self, dsetMgr, mainCounterTable, luminosity, self._additionalNormalisationFactor)
                    # Obtain histograms
                    myHistograms = []
                    if e.isShapeNuisance():
                        if isinstance(e, ConstantExtractor):
                            # Create up and down histograms out of the constant values
                            myHistograms.extend(_createShapeNuisanceFromConstant(myRateHistograms[0], myResult.getUncertaintyUp(), myResult.getUncertaintyDown()))
                            # Add also to the uncertainties as normalization uncertainty
                            self._cachedShapeRootHistogramWithUncertainties.addNormalizationUncertaintyRelative(e.getId(), myResult.getUncertaintyUp(), myResult.getUncertaintyDown())
                        else:
                            myHistograms = []
                            if not isinstance(e,QCDShapeVariationExtractor):
                                # Apply any further scaling (only necessary for the uncertainties from variation)
                                if e.getDistribution() == "shapeQ" and abs(e.getScaleFactor() - 1.0) > 0.0:
                                    self._cachedShapeRootHistogramWithUncertainties.ScaleVariationUncertainty(e._systVariation, e.getScaleFactor())
                            # Obtain histograms
                            if isinstance(e, QCDShapeVariationExtractor) or isinstance(e, ShapeVariationFromJsonExtractor):
                                myHistograms.extend(e.extractHistograms(self, dsetMgr, mainCounterTable, luminosity, self._additionalNormalisationFactor))
                            else:
                                myHistograms.extend(self._getShapeNuisanceHistogramsFromRHWU(self._cachedShapeRootHistogramWithUncertainties, e._systVariation, e.getMasterId()))
                    else:
                        # For QCD, scale the QCD type constants by the purity
                        if self.typeIsQCDinverted() and e.isQCDNuisance():
                            if isinstance(myResult, ScalarUncertaintyItem):
                                myResult.scale(1.0-myAveragePurity)
                            elif isinstance(myResult, list):
                                for i in range(0,len(myResult)):
                                    myResult[i] *= 1.0-myAveragePurity
                            else:
                                myResult *= 1.0-myAveragePurity
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
                                                                 "Stat." in e.getDescription() or "stat." in e.getDescription() or e.getDistribution()=="shapeStat",
                                                                 additionalResult=myAdditionalResult))
            if not myFoundStatus:
                raise Exception("\n"+ShellStyles.ErrorLabel()+"(data group ='"+self._label+"'): Cannot find nuisance with id '"+nid+"'!")
        # Print list of uncertainties
        if self._opts.verbose and dsetMgr != None and not self.typeIsEmptyColumn():
            print "  - Has shape variation syst. uncertainties: %s"%(", ".join(map(str,self._cachedShapeRootHistogramWithUncertainties.getShapeUncertainties().keys())))
        #self._cachedShapeRootHistogramWithUncertainties.Debug()

        # Obtain results for control plots
        if config.OptionDoControlPlots:
            for index, c in enumerate(controlPlotExtractors, 1):
                if dsetMgr != None and not self.typeIsEmptyColumn():
                    if self._opts.verbose:
                        print "  - Extracting data-driven control plot %s"%c._histoTitle
                    myCtrlDsetRootHisto = c.extractHistograms(self, dsetMgr, mainCounterTable, luminosity, self._additionalNormalisationFactor)

                    if myCtrlDsetRootHisto == None:
                        msg = "Could not find control plot \"%s\", skipping..." % (c._histoTitle)
                        Print(ShellStyles.WarningLabel() + msg, index==1)
                        self._controlPlots.append(None)
                    else:
                        # Obtain overall purity for QCD
                        myAverageCtrlPlotPurity = None
                        hCtrlPlotPurity = None
                        if self.typeIsQCDinverted(): #and False: #FIXME switch on when purity exists
                            myDsetHisto = c.extractQCDPurityHistogram(self, dsetMgr)
                            hCtrlPlotPurity = aux.Clone(myDsetHisto.getHistogram())
                            myAverageCtrlPlotPurity = c.extractQCDPurityAsValue(myRateHistograms[0], hCtrlPlotPurity)
                        # Now normalize
                        if myDatasetRootHisto.isMC():# and myCtrlDsetRootHisto.getHistogramWithUncertainties().getRootHisto().GetName() != self._cachedShapeRootHistogramWithUncertainties.getRootHisto().GetName():
                            myCtrlDsetRootHisto.normalizeToLuminosity(luminosity)
                        h = myCtrlDsetRootHisto.getHistogramWithUncertainties()
                        # Remove any variations not active for the column
                        h.keepOnlySpecifiedShapeUncertainties(myShapeVariationList)
                        # Rebin and move under/overflow bins to visible bins
                        if not isinstance(h.getRootHisto(), ROOT.TH2):
                            if getBinningForPlot(c._histoTitle) != None:
                                myArray = array("d",getBinningForPlot(c._histoTitle))
                                h.Rebin(len(myArray)-1,"",myArray)
                            h.makeFlowBinsVisible()
                        # Apply any further scaling (only necessary for the unceratainties from variation)
                        for nid in self._nuisanceIds:
                            for e in extractors:
                                if e.getId() == nid:
                                    if e.getDistribution() == "shapeQ" and abs(e.getScaleFactor() - 1.0) > 0.0:
                                        if not isinstance(h.getRootHisto(),ROOT.TH2):
                                            h.ScaleVariationUncertainty(e._systVariation, e.getScaleFactor())
                        # Add to RootHistogramWithUncertainties non-shape uncertainties
                        for n in self._nuisanceResults:
                            if not n.resultIsStatUncertainty() and len(n.getHistograms()) == 0: # systematic uncert., but not shapeQ
                                if self._opts.verbose:
                                    print "    - Adding norm. uncertainty: %s"%n.getMasterId()
                                myResult = n.getResult()
                                if self.typeIsQCDinverted():
                                    # Scale QCD nuisance by impurity (and unscale by shape impurity already applied to nuisance)
                                    for e in extractors:
                                        if e.getId() == n.getId():
                                            if e.isQCDNuisance():
                                                myResult = n.getResult().Clone()
                                                myResult.scale((1.0-myAverageCtrlPlotPurity) / (1.0 - myAveragePurity))
                                                #print n._exId, n.getResult().getUncertaintyUp(), myAverageCtrlPlotPurity, myResult.getUncertaintyUp()
                                if not isinstance(h.getRootHisto(),ROOT.TH2):
                                    if isinstance(myResult, ScalarUncertaintyItem):
                                        h.addNormalizationUncertaintyRelative(n.getId(), myResult.getUncertaintyUp(), myResult.getUncertaintyDown())
                                    elif isinstance(myResult, list):
                                        h.addNormalizationUncertaintyRelative(n.getId(), myResult[1], myResult[0])
                                    else:
                                        h.addNormalizationUncertaintyRelative(n.getId(), myResult, myResult)
                            elif not n.resultIsStatUncertainty() and len(n.getHistograms()) > 0:
                                if isinstance(n.getResult(), ScalarUncertaintyItem): # constantToShape
                                    if self._opts.verbose:
                                        print "    - Adding norm. uncertainty: %s"%n.getId()
                                    if not isinstance(h.getRootHisto(),ROOT.TH2):
                                        h.addNormalizationUncertaintyRelative(n.getMasterId(), myResult.getUncertaintyUp(), myResult.getUncertaintyDown())
                                for e in extractors:
                                    if e.getId() == n.getId():
                                        if isinstance(e,QCDShapeVariationExtractor):
                                            # Calculate and add QCD shape uncertainty to h
                                            if not isinstance(h.getRootHisto(),ROOT.TH2):
                                                e.extractHistograms(self, dsetMgr, mainCounterTable, luminosity, self._additionalNormalisationFactor, rootHistoWithUncertainties=h)
                        # Scale if asked
                        if self._landsProcess > 0 and config.OptionLimitOnSigmaBr:
                            h.Scale(self._additionalNormalisationFactor)
                        # Store RootHistogramWithUncertainties
                        myDictionary = {}
                        myDictionary["shape"] = h
                        myDictionary["purity"] = hCtrlPlotPurity
                        myDictionary["averagePurity"] = myAverageCtrlPlotPurity
                        for item in dir(self):
                            if item.startswith("typeIs"):
                                try:
                                    myStatus = getattr(self, item)()
                                    myDictionary[item] = myStatus
                                except TypeError:
                                    pass
                        self._controlPlots.append(myDictionary)

    def doRebinningOfCachedResults(self, config):
        '''
        Rebin the cached histograms and save a copy of the fine binned version
        '''
        myArray = array("d", config.ShapeHistogramsDimensions)
        nHistos = len(self._rateResult._histograms)

        # For-loop: All rate histograms
        for i in range(0, nHistos):
            
            myTitle = self._rateResult._histograms[i].GetTitle()
            self._rateResult._histograms[i].SetTitle(myTitle+_fineBinningSuffix)

            msg = "Rebinning %d/%d: %s" % (i+1, nHistos, myTitle)
            Verbose(ShellStyles.NoteStyle() + msg + ShellStyles.NormalStyle())

            # Move under/overflow bins to visible bins, store fine binned histogram, and do rebinning
            if self._rateResult._histograms[i].GetNbinsX() > 1:
                # Note that Rebin() does a clone operation in this case
                h = self._rateResult._histograms[i].Rebin(len(config.ShapeHistogramsDimensions)-1,myTitle,myArray)
                h.SetTitle(myTitle)
                histogramExtras.makeFlowBinsVisible(h)
                # The first one is assumed to be the one with the final binning elsewhere
                self._rateResult._histograms.insert(0,h)

        # Treat the negative and low-occupancy bins in the rebinned rate histogram, no inserted to be self._rateResult._histograms[0]
        nBins = self._rateResult._histograms[0].GetNbinsX()+1       
        nBelowMinStatUncert = 0
        nNegativeRate = 0

        # Determine the minimum statistical uncertainty 
        minStatUncert = config.MinimumStatUncertainty
        if config.UseAutomaticMinimumStatUncertainty and len(self._rateResult._histograms) > 1:
            # Determine the min. stat. uncert. automatically, from the fine-binned histogram, now stored at self._rateResult._histograms[1]
            h = self._rateResult._histograms[1]
            minimumError = -1.0
            for iBin in range(0,h.GetNbinsX()+1):
                content = h.GetBinContent(iBin)
                if content<=0: continue
                error = h.GetBinError(iBin)
                if error>0 and (error<minimumError or minimumError<0):
                    minimumError=error
            if minimumError > 0.0:
                minStatUncert = minimumError

        print "DEBUG: Setting the minimum stat. uncertainty for histogram %s to be %f"%(myTitle,minStatUncert)

        # For-loop: All histogram bins
        for k in range(1, nBins):
            msg = "Checking bin %d/%d: %s" % (k, nBins, myTitle)
            Verbose(ShellStyles.NoteStyle() + msg + ShellStyles.NormalStyle(), k==1)

            binRate = self._rateResult._histograms[0].GetBinContent(k)
            binError = self._rateResult._histograms[0].GetBinError(k)
            if binRate < minStatUncert: # FIXME: is this correct?
                # Treat zero or sightly positive rates
                if binRate == 0.0 or binError < minStatUncert
                    msg  = "Rate value is zero or below min.stat.uncert. in bin %d for column '%s' (it was %f)! " % (k, self.getLabel(), binRate)
                    msg += "Compensating up stat uncertainty to %f!" % (minStatUncert)
                    Verbose(ShellStyles.WarningLabel() + msg)
                    self._rateResult._histograms[0].SetBinError(k, minStatUncert)                   
                    nBelowMinStatUncert += 1
                # Treat negative rates
                if binRate < -0.00001:
                    msg  = "Rate value is negative in bin %d for column '%s' (it was %f)! " % (k, self.getLabel(), binRate)
                    msg += "This could have large effects to systematics, please fix!"
                    Verbose(ShellStyles.WarningLabel() + msg)
                    self._rateResult._histograms[0].SetBinContent(k, 0.0)
                    self._rateResult._histograms[0].SetBinError(k, minStatUncert)
                    nNegativeRate += 1
        
        # Print summarty of warnings/errors (if any)
        if nNegativeRate >0:
            msg = "Rate value for \"%s\" was negative (hence forced to zero) in %d bins" % (myTitle, nNegativeRate)
            Print(ShellStyles.WarningLabel() + msg)

        if nBelowMinStatUncert > 0:
            msg = "Rate value for \"%s\" was below minimum statistical uncertainty (hence set to default min of %f) in %d bins" % (myTitle, config.MinimumStatUncertainty, nBelowMinStatUncert)
            Print(ShellStyles.WarningLabel() + msg, False)

        # Convert bin content to integers for signal injection
        if self.typeIsObservation() and hasattr(config, "OptionSignalInjection"):
            for k in range(1, self._rateResult._histograms[0].GetNbinsX()+1):
                self._rateResult._histograms[0].SetBinContent(k, round(binRate, 0))

        # Update integral
        self._rateResult._result = self._rateResult._histograms[0].Integral()

        # For-loop: All nuisance results
        for j in range(0,len(self._nuisanceResults)):
            myNewHistograms = []
            for i in range(0,len(self._nuisanceResults[j]._histograms)):
                myTitle = self._nuisanceResults[j]._histograms[i].GetTitle()
                self._nuisanceResults[j]._histograms[i].SetTitle(myTitle+_fineBinningSuffix)
                # move under/overflow bins to visible bins, store fine binned histogram, and do rebinning
                h = self._nuisanceResults[j]._histograms[i].Rebin(len(config.ShapeHistogramsDimensions)-1,myTitle,myArray)
                h.SetTitle(myTitle)
                histogramExtras.makeFlowBinsVisible(h)
                myNewHistograms.append(h)
            self._nuisanceResults[j]._histograms.extend(myNewHistograms)

	# Treat QCD MET shape nuisance
	myQCDMetshapeFoundStatus = False
	for j in range(0,len(self._nuisanceResults)):
	    if "CMS_Hptntj_QCDkbg_metshape" in self._nuisanceResults[j].getId():
                myQCDMetshapeFoundStatus = True
		hDenominator = None
		hNumerator = None
		hUp = None
		hDown = None
		for i in range(0,len(self._nuisanceResults[j]._histograms)):
		    if not _fineBinningSuffix in self._nuisanceResults[j]._histograms[i].GetTitle():
			if "Numerator" in self._nuisanceResults[j]._histograms[i].GetTitle():
			    hNumerator = self._nuisanceResults[j]._histograms[i]
			if "Denominator" in self._nuisanceResults[j]._histograms[i].GetTitle():
			    hDenominator = self._nuisanceResults[j]._histograms[i]
			if "Up" in self._nuisanceResults[j]._histograms[i].GetTitle():
			    hUp = self._nuisanceResults[j]._histograms[i]
			if "Down" in self._nuisanceResults[j]._histograms[i].GetTitle():
			    hDown = self._nuisanceResults[j]._histograms[i]
		if hDenominator == None or hNumerator == None or hUp == None or hDown == None:
		    raise Exception()
                if hDenominator.GetNbinsX() != hUp.GetNbinsX():
                    raise Exception()
                if hDenominator.GetNbinsX() != self._rateResult._histograms[0].GetNbinsX():
                    raise Exception()
		systematicsForMetShapeDifference.createSystHistograms(self._rateResult._histograms[0], hUp, hDown, hNumerator, hDenominator, quietMode=False)
        if not myQCDMetshapeFoundStatus and self.typeIsQCDinverted():
            print ShellStyles.WarningLabel()+"QCD metshape uncertainty has not been rebinned, please check that it has the name 'QCD_metshape'!"

        # Update root histo with uncertainties to contain the binned version
        if self._cachedShapeRootHistogramWithUncertainties != None:
            #self._cachedShapeRootHistogramWithUncertainties.Debug()
            self._cachedShapeRootHistogramWithUncertainties.delete()
            self._cachedShapeRootHistogramWithUncertainties.setRootHisto(self._rateResult._histograms[0])
            for j in range(0,len(self._nuisanceResults)):
                # shape nuisance
                hUp = None
                hDown = None
                for i in range(0,len(self._nuisanceResults[j]._histograms)):
                    myTitle = self._nuisanceResults[j]._histograms[i].GetTitle()
                    if not _fineBinningSuffix in myTitle:
                        if myTitle.endswith("Up"):
                            hUp = self._nuisanceResults[j]._histograms[i]
                        if myTitle.endswith("Down"):
                            hDown = self._nuisanceResults[j]._histograms[i]
                if hUp == None or hDown == None:
                    # constant nuisance
                    myResult = self._nuisanceResults[j].getResult()
                    self._cachedShapeRootHistogramWithUncertainties.addNormalizationUncertaintyRelative(self._nuisanceResults[j].getId(), myResult.getUncertaintyUp(), myResult.getUncertaintyDown())
                else:
                    self._cachedShapeRootHistogramWithUncertainties.addShapeUncertaintyFromVariation(self._nuisanceResults[j].getId(), hUp, hDown)
            #self._cachedShapeRootHistogramWithUncertainties.Debug()
        return

    def getRateResult(self):
        '''
        Returns rate for column
        '''
        if self._rateResult == None:
            raise Exception(ErrorStyle()+"Error (data group ='"+self._label+"'):"+ShellStyles.NormalStyle()+" Rate value has not been cached! (did you forget to call doDataMining()?)")
        if self._rateResult.getResult() == None:
            raise Exception(ErrorStyle()+"Error (data group ='"+self._label+"'):"+ShellStyles.NormalStyle()+" Rate value has not been cached! (did you forget to call doDataMining()?)")
        return self._rateResult.getResult()

    ## Returns rate histogram for column
    def getRateHistogram(self):
        if self._rateResult == None:
            raise Exception(ErrorStyle()+"Error (data group ='"+self._label+"'):"+ShellStyles.NormalStyle()+" Rate value has not been cached! (did you forget to call doDataMining()?)")
        if self._rateResult.getHistograms() == None:
            raise Exception(ErrorStyle()+"Error (data group ='"+self._label+"'):"+ShellStyles.NormalStyle()+" Rate histograms have not been cached! (did you forget to call doDataMining()?)")
        return self._rateResult.getHistograms()[0]

    ## Returns purity histogram (only relevant for QCD)
    def getPurityHistogram(self):
        return self._rateResult.getPurityHistogram()

    ## Returns true if column has a nuisance Id
    def hasNuisanceByMasterId(self, id):
        for result in self._nuisanceResults:
            if id == result.getMasterId():
                return True
        return False

    ## Returns nuisance for column (as string)
    def getNuisanceResultByMasterId(self, id):
        if self._nuisanceResults == None:
            raise Exception(ErrorStyle()+"Error (data group ='"+self._label+"'):"+ShellStyles.NormalStyle()+" Nuisance values have not been cached! (did you forget to call doDataMining()?)")
        if len(self._nuisanceResults) == 0:
            raise Exception(ErrorStyle()+"Error (data group ='"+self._label+"'):"+ShellStyles.NormalStyle()+" Nuisance values have not been cached! (did you forget to call doDataMining()?)")
        for result in self._nuisanceResults:
            if id == result.getMasterId():
                return result.getResult()
        raise Exception("Nuisance with id='"+id+"' not found in data group '"+self._label+"'! Check first with hasNuisance(id) that data group has the nuisance.")

    ## Returns full nuisance for column (as string)
    def getFullNuisanceResultByMasterId(self, id):
        if self._nuisanceResults == None:
            raise Exception(ErrorStyle()+"Error (data group ='"+self._label+"'):"+ShellStyles.NormalStyle()+" Nuisance values have not been cached! (did you forget to call doDataMining()?)")
        if len(self._nuisanceResults) == 0:
            raise Exception(ErrorStyle()+"Error (data group ='"+self._label+"'):"+ShellStyles.NormalStyle()+" Nuisance values have not been cached! (did you forget to call doDataMining()?)")
        for result in self._nuisanceResults:
            if id == result.getMasterId():
                return result
        raise Exception("Nuisance with id='"+id+"' not found in data group '"+self._label+"'! Check first with hasNuisance(id) that data group has the nuisance.")

    ## Stores the cached result histograms to root file
    def setResultHistogramsToRootFile(self, rootfile):
        if self._rateResult == None:
            raise Exception(ErrorStyle()+"Error (data group ='"+self._label+"'):"+ShellStyles.NormalStyle()+" Rate value has not been cached! (did you forget to call doDataMining()?)")
        if self._rateResult.getResult() == None:
            raise Exception(ErrorStyle()+"Error (data group ='"+self._label+"'):"+ShellStyles.NormalStyle()+" Rate value has not been cached! (did you forget to call doDataMining()?)")
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
        print "  shape histogram:", self.getFullShapeHistoName()

    def doSeparateAdditionalResults(self):
        myNewNuisancesList = []
        myNewNuisanceIdsList = []
        for n in self.getNuisanceResults():
            if n.getAdditionalResult() != None:
                # Create new cached result
                myId = n._exId+"_normOnly"
                myMasterId = n._masterId
                if myMasterId != "-1":
                    myMasterId += "_normOnly"
                myNewResult = ExtractorResult(myId, myMasterId, n.getAdditionalResult(), [])
                myNewNuisancesList.append(myNewResult)
                myNewNuisanceIdsList.append(myId)
                n._exId += "_shapeOnly"
        self._nuisanceResults.extend(myNewNuisancesList)
        self._nuisanceIds.extend(myNewNuisanceIdsList)
        return myNewNuisanceIdsList

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
