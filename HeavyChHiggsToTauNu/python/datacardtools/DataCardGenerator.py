#! /usr/bin/env python

import os
import sys

from ROOT import *

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect

from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.DatacardColumn import DatacardColumn
from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.Extractor import *
from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.TableProducer import *
from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.TableProducer import *
from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.QCDfactorised import QCDfactorisedColumn,QCDfactorisedExtractor
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShellStyles import *

import HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.MulticrabPathFinder as PathFinder

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.aux import sort

# main class for generating the datacards from a given cfg file

class DatacardQCDMethod:
    UNKNOWN = 0
    FACTORISED = 1
    INVERTED = 2

class DataCardGenerator:
    def __init__(self, config, opts, QCDMethod, optimisationVariation=None):
	self._dsetMgrs = None
	self._config = config
	self._opts = opts
        self._observation = None
        self._luminosity = -1
        self._columns = []
        self._extractors = []
        self._controlPlotExtractors = []
        self._QCDMethod = QCDMethod
        self._replaceEmbeddingWithMC = False
        self._doSignalAnalysis = True
        self._doEmbeddingAnalysis = True
        self._doQCDFactorised = False
        if optimisationVariation == None:
            self._optimisationVariation = ""
        else:
            self._optimisationVariation = optimisationVariation
        if self._QCDMethod == DatacardQCDMethod.FACTORISED:
            self._doQCDFactorised = True
        self._doQCDInverted = False
        if self._QCDMethod == DatacardQCDMethod.INVERTED:
            self._doQCDInverted = True
        # Override options from command line (not used at the moment)
        #self.overrideConfigOptionsFromCommandLine()
        if self._QCDMethod != DatacardQCDMethod.FACTORISED and self._QCDMethod != DatacardQCDMethod.INVERTED:
            raise Exception(ErrorStyle()+"Error: QCD method was not properly specified when creating DataCardGenerator!"+NormalStyle())
        if self._config.OptionReplaceEmbeddingByMC != None:
            self._replaceEmbeddingByMC = self._config.OptionReplaceEmbeddingByMC

        # Check that all necessary parameters have been specified in config file
        myStatus = self.checkCfgFile()
        if not myStatus:
            myMsg = "Datacards will not be created for "
            if self._QCDMethod != DatacardQCDMethod.FACTORISED:
                myMsg += " QCD factorised"
            elif self._QCDMethod != DatacardQCDMethod.INVERTED:
                myMsg += " QCD inverted"
            print myMsg+" (if this is not intented, check your config!)\n"
            return

        # Construct prefix for output name
        myOutputPrefix = ""
        if self._QCDMethod == DatacardQCDMethod.FACTORISED:
            myOutputPrefix += "QCDfact"
        elif self._QCDMethod == DatacardQCDMethod.INVERTED:
            myOutputPrefix += "QCDinv"
        if self._replaceEmbeddingByMC:
            myOutputPrefix += "_MCEWK"

        print "\n"+CaptionStyle()+"Running datacard generator"+NormalStyle()
        myMassRange = str(self._config.MassPoints[0])
        if len(self._config.MassPoints) > 0:
            myMassRange += "-"+str(self._config.MassPoints[len(self._config.MassPoints)-1])
        print "Cards will be generated for "+HighlightStyle()+myOutputPrefix+NormalStyle()+" in mass range "+HighlightStyle()+myMassRange+" GeV"+NormalStyle()
        if self._optimisationVariation == None:
            print "Evaluating default analysis\n"
        else:
            print "Evaluating variation: "+HighlightStyle()+self._optimisationVariation+NormalStyle()+"\n"
            myOutputPrefix += "_"+self._optimisationVariation

        # Create columns (dataset groups)
        myLuminosities = self.createDatacardColumns()
        self.checkDatacardColumns()

        # create extractors and control plot extractors
        self.createExtractors()
        self.createControlPlots()

        # do data mining to cache results into datacard column objects
        self.doDataMining(myLuminosities)

        # Make datacards
        TableProducer(opts, config, myOutputPrefix, self._luminosity, self._observation, self._columns, self._extractors)

        # Close files
        self.closeFiles()

    #def overrideConfigOptionsFromCommandLine(self):
        # Obtain QCD measurement method

    def checkCfgFile(self):
        mymsg = ""
        if self._config.DataCardName == None:
            mymsg += "- missing field 'DataCardName' (string, describes the name of the datacard)\n"
        if self._config.Path == None:
            mymsg += "- missing field 'Path' (string, path to directory containing all multicrab directories to be used for datacards)\n"
        elif not os.path.exists(self._config.Path):
            mymsg += "- 'Path' points to directory that does not exist!\n"
        if self._config.MassPoints == None:
            mymsg += "- missing field 'MassPoints' (list of integers, mass points for which datacard is generated)!\n"
        elif len(self._config.MassPoints) == 0:
            mymsg += "- field 'MassPoints' needs to have at least one entry! (list of integers, mass points for which datacard is generated)\n"
        if self._config.BlindAnalysis == None:
            mymsg += "- field 'BlindAnalysis' needs to be set as True or False!\n"
        if self._config.SignalAnalysis == None:
            print WarningStyle()+"Warning: The field 'SignalAnalysis' is not specified or empty in the config file, signal analysis will be ignored"+NormalStyle()
            self._doSignalAnalysis = False
        if self._config.EmbeddingAnalysis == None:
            print WarningStyle()+"Warning: The field 'EmbeddingAnalysis' is not specified or empty in the config file, embedding analysis will be ignored"+NormalStyle()
            self._doEmbeddingAnalysis = False
            #mymsg += "- missing field 'SignalAnalysis' (string, name of EDFilter/EDAnalyzer process that produced the root files for signal analysis)\n"
        if self._QCDMethod == DatacardQCDMethod.FACTORISED and self._config.QCDFactorisedAnalysis == None:
            print WarningStyle()+"Warning: The field 'QCDFactorisedAnalysis' is not specified or empty in the config file, QCD factorised analysis will be ignored"+NormalStyle()
            self._doQCDFactorised = False
            return False
        if self._QCDMethod == DatacardQCDMethod.INVERTED and self._config.QCDInvertedAnalysis == None:
            print WarningStyle()+"Warning: The field 'QCDInvertedAnalysis' is not specified or empty in the config file, QCD inverted analysis will be ignored"+NormalStyle()
            self._doQCDInverted = False
            return False
        if self._QCDMethod == DatacardQCDMethod.UNKNOWN:
            mymsg += "- missing field 'QCDMeasurementMethod' (string, name of QCD measurement method, options: 'QCD factorised' or 'QCD inverted')\n"
        if self._config.SignalRateCounter == None:
            mymsg += "- missing field 'SignalRateCounter' (string, label of counter to be used for rate)\n"
        if self._config.FakeRateCounter == None:
            mymsg += "- missing field 'FakeRateCounter' (string, label of counter to be used for rate)\n"
        if self._config.SignalShapeHisto == None:
            mymsg += "- missing field 'SignalShapeHisto' (string, name of histogram for the shape)\n"
        if self._config.FakeShapeHisto == None:
            mymsg += "- missing field 'FakeShapeHisto' (string, name of histogram for the shape)\n"
        if self._config.ShapeHistogramsDimensions == None:
            mymsg += "- missing field 'ShapeHistogramsDimensions' (list of number of bins, minimum, and maximum)\n"
        elif not isinstance(self._config.ShapeHistogramsDimensions, dict):
            mymsg += "- field 'ShapeHistogramsDimensions' has to be of type dictionary with keys: bins, rangeMin, rangeMax, variableBinSizeLowEdges, xtitle, ytitle)\n"
        else:
            if not "bins" in self._config.ShapeHistogramsDimensions.keys():
                mymsg += "- field 'ShapeHistogramsDimensions' has to contain dictionary key bins (int)\n"
            elif not "rangeMin" in self._config.ShapeHistogramsDimensions.keys():
                mymsg += "- field 'ShapeHistogramsDimensions' has to contain dictionary key rangeMin (float)\n"
            elif not "rangeMax" in self._config.ShapeHistogramsDimensions.keys():
                mymsg += "- field 'ShapeHistogramsDimensions' has to contain dictionary key rangeMax (float)\n"
            elif not "variableBinSizeLowEdges" in self._config.ShapeHistogramsDimensions.keys():
                mymsg += "- field 'ShapeHistogramsDimensions' has to contain dictionary key variableBinSizeLowEdges (list of floats, can be empty list)\n"
            elif not "xtitle" in self._config.ShapeHistogramsDimensions.keys():
                mymsg += "- field 'ShapeHistogramsDimensions' has to contain dictionary key xtitle (string)\n"
            elif not "ytitle" in self._config.ShapeHistogramsDimensions.keys():
                mymsg += "- field 'ShapeHistogramsDimensions' has to contain dictionary key ytitle (string)\n"
        if self._config.Observation == None:
            mymsg += "- missing field 'Observation' (ObservationInput object)\n"
        if self._config.DataGroups == None:
            mymsg += "- missing field 'DataGroups' (list of DataGroup objects)\n"
        elif len(self._config.DataGroups) == 0:
            mymsg += "- need to specify at least one DataGroup to field 'DataGroups' (list of DataGroup objects)\n"
        if self._config.Nuisances == None:
            mymsg += "- missing field 'Nuisances' (list of Nuisance objects)\n"
        elif len(self._config.Nuisances) == 0:
            mymsg += "- need to specify at least one Nuisance to field 'Nuisances' (list of Nuisance objects)\n"
        if self._config.ControlPlots == None:
            print WarningStyle()+"Warning:"+NormalStyle()+" You did not specify any ControlPlots in the config (ControlPlots is list of ControlPlotInput objects)!"
            print "  Please check if this was intended."
        # determine if datacard was ok
        if mymsg != "":
            print ErrorStyle()+"Error in config '"+self._opts.datacard+"'!"+NormalStyle()
            print mymsg
            raise Exception()
        return True

    ## Reads datagroup definitions from columns and initialises datasets
    def createDatacardColumns(self):
        # Obtain paths to multicrab directories
        multicrabPaths = PathFinder.MulticrabPathFinder(self._config.Path)
        mySignalPath = None
        if self._doSignalAnalysis:
            mySignalPath = multicrabPaths.getSignalPath()
            print "- Using signal and EWK+ttbar with fake taus directory:", mySignalPath
            if not os.path.exists(mySignalPath):
                raise Exception(ErrorStyle()+"Path for signal analysis ('"+mySignalPath+"') does not exist!"+NormalStyle())
        myEmbeddingPath = None
        if self._doEmbeddingAnalysis:
            myEmbeddingPath = multicrabPaths.getEWKPath()
            if not self._replaceEmbeddingByMC:
                print "- Using embedding (EWK+ttbar with genuine taus) directory:", myEmbeddingPath
                if not os.path.exists(myEmbeddingPath):
                    raise Exception(ErrorStyle()+"Path for embedding analysis ('"+myEmbeddingPath+"') does not exist!"+NormalStyle())
            elif self._doSignalAnalysis:
                # if embedding is replaced by MC EWK, use signal path as path for embedding
                myEmbeddingPath = mySignalPath
                print WarningStyle()+"- Replacing embedding with MC EWK samples from signal analysis"+NormalStyle()
        myQCDPath = ""
        myQCDCounters = ""
        if self._QCDMethod == DatacardQCDMethod.FACTORISED:
            myQCDPath = multicrabPaths.getQCDFactorisedPath()
            myQCDCounters = self._config.QCDFactorisedAnalysis+self._optimisationVariation+"/counters"
            print "- Using multi-jets (factorised) directory:", myQCDPath
        elif self._QCDMethod == DatacardQCDMethod.INVERTED:
            myQCDPath = multicrabPaths.getQCDinvPath()
            myQCDCounters = self._config.QCDInvertedAnalysis+self._optimisationVariation+"/counters"
            print "- Using multi-jets (inverted) directory:", myQCDPath
        if not os.path.exists(myQCDPath):
            raise Exception(ErrorStyle()+"Path for QCD measurement ('"+myQCDPath+"') does not exist!"+NormalStyle())
        # Make dataset managers
        self._dsetMgrs = [None] # needed for datasetType==None
        if self._doSignalAnalysis:
            self._dsetMgrs.append(dataset.getDatasetsFromMulticrabCfg(cfgfile=mySignalPath+"/multicrab.cfg", counters=self._config.SignalAnalysis+self._optimisationVariation+"/counters"))
        else:
            self._dsetMgrs.append(None)
        if self._doEmbeddingAnalysis:
            print "***"
            self._dsetMgrs.append(dataset.getDatasetsFromMulticrabCfg(cfgfile=myEmbeddingPath+"/multicrab.cfg", counters=self._config.SignalAnalysis+self._optimisationVariation+"/counters"))
        else:
            self._dsetMgrs.append(None)
        self._dsetMgrs.append(dataset.getDatasetsFromMulticrabCfg(cfgfile=myQCDPath+"/multicrab.cfg", counters=myQCDCounters))
        # Set normalisation and obtain dataset names and luminosities
        myAllDatasetNames = []
        myLuminosities = []
        for i in range(0,len(self._dsetMgrs)):
            if self._dsetMgrs[i] != None:
                # update normalisation info
                self._dsetMgrs[i].updateNAllEventsToPUWeighted()
                self._dsetMgrs[i].loadLuminosities()
                # Obtain all dataset names
                myAllDatasetNames.append(self._dsetMgrs[i].getAllDatasetNames())
                # Obtain luminosity
                myLuminosity = 0.0
                for d in self._dsetMgrs[i].getDataDatasets():
                    myLuminosity += d.getLuminosity()
                myLuminosities.append(myLuminosity)
                # Print info
                myMsg = HighlightStyle()+"DatasetManager info before merging for "
                if i == 1:
                    myMsg += "signal"
                elif i == 2:
                    myMsg += "EWKtau"
                elif i == 3:
                    myMsg += "QCD"
                print myMsg+NormalStyle()
                self._dsetMgrs[i].printInfo()
            else:
                myAllDatasetNames.append([])
                myLuminosities.append(0.0)
        print "Luminosity is set to:"
        print "  signal multicrab: "+HighlightStyle()+"%f 1/pb"%myLuminosities[1] +NormalStyle()
        print "  EWKtau multicrab: "+HighlightStyle()+"%f 1/pb"%myLuminosities[2] +NormalStyle()
        print "     QCD multicrab: "+HighlightStyle()+"%f 1/pb"%myLuminosities[3] +NormalStyle()
        self._luminosity = myLuminosities[1]
        # Check that luminosities are compatible
        if myLuminosities[2] != myLuminosities[1] and self._doEmbeddingAnalysis:
            myDiff = abs(myLuminosities[2] / myLuminosities[1]-1.0)
            if myDiff < 0.01:
                print WarningStyle()+"Warning: signal and embedding luminosities differ slightly (%.2f %%)!"%(myDiff*100.0) +NormalStyle()
            else:
                raise Exception(ErrorStyle()+"Error: signal and embedding luminosities differ more than 1 %!"+NormalStyle())
        if myLuminosities[3] != myLuminosities[1] and self._doSignalAnalysis:
            raise Exception(ErrorStyle()+"Error: signal and QCD luminosities are not the same!"+NormalStyle())
        # Make datacard column object for observation
        if self._doSignalAnalysis:
            myFoundNames = self.findDatasetNames("Observation", myAllDatasetNames[1], self._config.Observation.datasetDefinitions)
            if self._opts.debugConfig:
                print "Adding datasets to data group 'Observation':"
                for n in myFoundNames:
                    print "  "+n
            myObservationName = "dset_observation"
            print "Making merged dataset for data group: "+HighlightStyle()+"observation"+NormalStyle()
            self._dsetMgrs[1].merge(myObservationName, myFoundNames, keepSources=True)
            self._observation = DatacardColumn(label = "data_obs",
                                              enabledForMassPoints = self._config.MassPoints,
                                              datasetType = "Observation",
                                              rateCounter = self._config.Observation.rateCounter,
                                              datasetMgrColumn = myObservationName,
                                              dirPrefix = self._config.Observation.dirPrefix+self._optimisationVariation,
                                              shapeHisto = self._config.Observation.shapeHisto)
            if self._opts.debugConfig:
                self._observation.printDebug()
        else:
            print WarningStyle()+"No observation will be extracted, because signal analysis is disabled"+NormalStyle()
        # Make merges for columns (a unique merge for each data group; used to access counters and histograms)
        for dg in self._config.DataGroups:
            # Make sure that only one QCD method is included
            if (dg.datasetType == "QCD factorised" and self._QCDMethod == DatacardQCDMethod.INVERTED) or (dg.datasetType == "QCD inverted" and self._QCDMethod == DatacardQCDMethod.FACTORISED):
                print "Skipping data group: "+HighlightStyle()+""+dg.label+""+NormalStyle() + " (only one QCD measurement allowed in a datacard)"
            else:
                print "Making merged dataset for data group: "+HighlightStyle()+""+dg.label+""+NormalStyle()
                myDsetMgr = 0
                mMergedName = ""
                myMergedNameForQCDMCEWK = ""
                if dg.datasetType != "None":
                    if dg.datasetType == "Signal":
                        myDsetMgr = 1
                    elif dg.datasetType == "Embedding":
                        myDsetMgr = 2
                    elif dg.datasetType == "QCD factorised" or dg.datasetType == "QCD inverted":
                        myDsetMgr = 3
                    # find dataset names
                    myFoundNames = self.findDatasetNames(dg.label, myAllDatasetNames[myDsetMgr], dg.datasetDefinitions)
                    # make merged set
                    if self._opts.debugConfig:
                        print "Adding datasets to data group '"+dg.label+"':"
                        for n in myFoundNames:
                            print "  "+n
                    myMergedName = "dset_"+dg.label.replace(" ","_")
                    if self._dsetMgrs[myDsetMgr] != None:
                        self._dsetMgrs[myDsetMgr].merge(myMergedName, myFoundNames)
                    # find datasets and make merged set for QCD MC EWK
                    if dg.datasetType == "QCD factorised":
                        myFoundNames = self.findDatasetNames(dg.label, myAllDatasetNames[myDsetMgr], dg.MCEWKDatasetDefinitions)
                        # make merged set
                        if self._opts.debugConfig:
                            print "Adding MC EWK datasets to QCD:"
                            for n in myFoundNames:
                                print "  "+n
                        myMergedNameForQCDMCEWK = "dset_"+dg.label.replace(" ","_")+"_MCEWK"
                        self._dsetMgrs[myDsetMgr].merge(myMergedNameForQCDMCEWK, myFoundNames)
                # Construct dataset column object
                myColumn = None
                if dg.datasetType == "QCD factorised":
                    myColumn = QCDfactorisedColumn(landsProcess=dg.landsProcess,
                                                   enabledForMassPoints = dg.validMassPoints,
                                                   nuisanceIds = dg.nuisances,
                                                   datasetMgrColumn = myMergedName,
                                                   datasetMgrColumnForQCDMCEWK = myMergedNameForQCDMCEWK,
                                                   additionalNormalisationFactor = dg.additionalNormalisation,
                                                   dirPrefix = dg.dirPrefix+self._optimisationVariation,
                                                   QCDfactorisedInfo = dg.QCDfactorisedInfo,
                                                   debugMode = self._opts.debugQCD)
                else:
                    myColumn = DatacardColumn(label=dg.label,
                                              landsProcess=dg.landsProcess,
                                              enabledForMassPoints = dg.validMassPoints,
                                              datasetType = dg.datasetType,
                                              rateCounter = dg.rateCounter,
                                              nuisanceIds = dg.nuisances,
                                              datasetMgrColumn = myMergedName,
                                              datasetMgrColumnForQCDMCEWK = myMergedNameForQCDMCEWK,
                                              additionalNormalisationFactor = dg.additionalNormalisation,
                                              dirPrefix = dg.dirPrefix+self._optimisationVariation,
                                              shapeHisto = dg.shapeHisto)
                # Disable non-active QCD measurements
                if dg.datasetType == "QCD factorised" and self._QCDMethod == DatacardQCDMethod.INVERTED:
                    myColumn.disable()
                elif dg.datasetType == "QCD inverted" and self._QCDMethod == DatacardQCDMethod.FACTORISED:
                    myColumn.disable()
                # Add column
                self._columns.append(myColumn)
                if self._opts.debugConfig:
                    myColumn.printDebug()
        print "Data groups converted to datacard columns"
        for i in range(0,len(self._dsetMgrs)):
            if self._dsetMgrs[i] != None:
                myMsg = HighlightStyle()+"DatasetManager info after merging datasets for "
                if i == 1:
                    myMsg += "signal"
                elif i == 2:
                    myMsg += "EWKtau"
                elif i == 3:
                    myMsg += "QCD"
                print myMsg+NormalStyle()
                self._dsetMgrs[i].printInfo()
        return myLuminosities

    def doDataMining(self, luminosities):
        # Obtain main counter tables
        print "Obtaining main counter tables"
        myEventCounterTables = []
        for i in range(0,len(self._dsetMgrs)):
            if self._dsetMgrs[i] != None:
                # Obtain main event counter table
                myEventCounter = counter.EventCounter(self._dsetMgrs[i],None,None,True)
                myEventCounter.normalizeMCToLuminosity(luminosities[i])
                myEventCounterTables.append(myEventCounter.getMainCounterTable())
            else:
                myEventCounterTables.append(None)
        # Do data mining and cache results
        print "Starting data mining"
        if self._doSignalAnalysis:
            # Handle observation separately
            self._observation.doDataMining(self._config,self._dsetMgrs[1],luminosities[1],myEventCounterTables[1],self._extractors,self._controlPlotExtractors)
        for c in self._columns:
            myIndex = 0
            if c.typeIsObservation() or c.typeIsSignal():
                myIndex = 1
            if c.typeIsEWK():
                myIndex = 2
            if c.typeIsQCD():
                myIndex = 3
            # Do mining for datacard columns
            c.doDataMining(self._config,self._dsetMgrs[myIndex],luminosities[myIndex],myEventCounterTables[myIndex],self._extractors,self._controlPlotExtractors)
        print "\nData mining has been finished, results (and histograms) have been ingeniously cached"

    ## Closes files in dataset managers
    def closeFiles(self):
        print "Closing open input files"
        for i in range(0,len(self._dsetMgrs)):
            if self._dsetMgrs[i] != None:
                self._dsetMgrs[i].close()
        print "DatasetManagers closed"


    ## Helper function for finding datasets
    def findDatasetNames(self, label, allNames, searchNames):
        myResult = []
        for dset in searchNames:
            myFoundStatus = False
            for dsetfull in allNames:
                if dset in dsetfull:
                    myResult.append(dsetfull)
                    myFoundStatus = True
            if not myFoundStatus and len(allNames) > 0:
                print ErrorStyle()+"Error in dataset group '"+label+"':"+NormalStyle()+" cannot find datasetDefinition '"+dset+"'!"
                print "Options are:"
                for dsetfull in allNames:
                    print "  "+dsetfull
                raise Exception()
        return myResult

    ## Check landsProcess in datacard columns
    def checkDatacardColumns(self):
        for m in self._config.MassPoints:
            i = 0
            myFirstValue = 0
            for c in sorted(self._columns, key=lambda x: x.getLandsProcess()):
                if (c.isActiveForMass(m)):
                    #print c.getLabel(), c.getLandsProcess()
                    if i == 0:
                        myFirstValue = c.getLandsProcess()
                    else:
                        if myFirstValue + i != c.getLandsProcess():
                            print ErrorStyle()+"Error:"+NormalStyle()+" cannot find LandS process '"+str(myFirstValue+i)+"' in data groups for mass = %d! (need to have consecutive numbers; add group with such landsProcess or check input file)"%m
                            raise Exception()
                    i += 1

    ## Creates extractors for nuisances
    def createExtractors(self):
        # Protection to create extractors only once
        if len(self._extractors) > 0:
            return

        myMode = ExtractorMode.NUISANCE
        for n in self._config.Nuisances:
            if n.function == "Constant":
                myMode = ExtractorMode.NUISANCE
                if n.upperValue > 0:
                    myMode = ExtractorMode.ASYMMETRICNUISANCE
                self._extractors.append(ConstantExtractor(exid = n.id,
                                                         constantValue = n.value,
                                                         constantUpperValue = n.upperValue,
                                                         distribution = n.distr,
                                                         description = n.label,
                                                         mode = myMode))
            elif n.function == "Counter":
                self._extractors.append(CounterExtractor(exid = n.id,
                                                        counterItem = n.counter,
                                                        distribution = n.distr,
                                                        description = n.label,
                                                        mode = myMode))
            elif n.function == "maxCounter":
                self._extractors.append(MaxCounterExtractor(exid = n.id,
                                                           counterItem = n.counter,
                                                           counterDirs = n.histoDir,
                                                           distribution = n.distr,
                                                           description = n.label,
                                                           mode = myMode))
            elif n.function == "pileupUncertainty":
                self._extractors.append(PileupUncertaintyExtractor(exid = n.id,
                                                                   counterItem = n.counter,
                                                                   counterDirs = n.histoDir,
                                                                   distribution = n.distr,
                                                                   description = n.label,
                                                                   mode = myMode))
            elif n.function == "Shape":
                self._extractors.append(ShapeExtractor(histoSpecs = self._config.ShapeHistogramsDimensions,
                                                       counterItem = n.counter,
                                                       histoDirs = n.histoDir,
                                                       histograms = n.histo,
                                                       exid = n.id,
                                                       distribution = n.distr,
                                                       description = n.label,
                                                       mode = ExtractorMode.SHAPENUISANCE))
            elif n.function == "ScaleFactor":
                self._extractors.append(ScaleFactorExtractor(exid = n.id,
                                                            histoDirs = n.histoDir,
                                                            histograms = n.histo,
                                                            normalisation = n.norm,
                                                            addSystInQuadrature = n.addUncertaintyInQuadrature,
                                                            distribution = n.distr,
                                                            description = n.label,
                                                            mode = myMode))
            elif n.function == "Ratio":
                self._extractors.append(RatioExtractor(exid = n.id,
                                                      numeratorCounterItem = n.numerator,
                                                      denominatorCounterItem = n.denominator,
                                                      distribution = n.distr,
                                                      description = n.label,
                                                      scale = n.scaling,
                                                      mode = myMode))
            elif n.function == "QCDFactorised":
                if self._QCDMethod == DatacardQCDMethod.FACTORISED:
                    self._extractors.append(QCDfactorisedExtractor(QCDmode = n.QCDmode, exid = n.id, distribution = n.distr, description = n.label, mode = myMode))
                else:
                    # Protection; generate nuisance line even, but leave it empty
                    self._extractors.append(ConstantExtractor(exid = n.id, constantValue = 0.0, distribution = n.distr, description = n.label, mode = myMode))
            elif n.function == "QCDInverted":
                if self._QCDMethod == DatacardQCDMethod.INVERTED:
                    print "fixme: add QCD inverted"
                    # FIXME temp code
                    self._extractors.append(ConstantExtractor(exid = n.id, constantValue = 0.0, distribution = n.distr, description = n.label, mode = myMode))
                else:
                    # Protection; generate nuisance line even, but leave it empty
                    self._extractors.append(ConstantExtractor(exid = n.id, constantValue = 0.0, distribution = n.distr, description = n.label, mode = myMode))
            else:
                print ErrorStyle()+"Error in nuisance with id='"+n.id+"':"+NormalStyle()+" unknown or missing field function '"+n.function+"' (string)!"
                print "Options are: 'Constant', 'Counter', 'maxCounter', 'Shape', 'ScaleFactor', 'Ratio', 'QCDFactorised'"
                raise Exception()
        # Create reserved nuisances
        for n in self._config.ReservedNuisances:
            self._extractors.append(ConstantExtractor(exid = n[0], constantValue = 0.0, distribution = "lnN", description = n[1], mode = myMode))
        # Done
        print "Created Nuisances"
        self.checkNuisances()

    def checkNuisances(self):
        # Check for duplicates
        for i in range(0,len(self._extractors)):
            for j in range(0,len(self._extractors)):
                if self._extractors[i].isId(self._extractors[j].getId()) and i != j:
                    print ErrorStyle()+"Error:"+NormalStyle()+" You have defined two nuisances with id='"++"'! The id has to be unique!"
                    raise Exception()
        # Merge nuisances
        self.mergeNuisances()
        # Check consecutive id's
        myCounter = 0
        for n in sorted(self._extractors, key=lambda x: x.getId()):
            if n.isPrintable():
                myCounter += 1
                if int(n.getId()) != myCounter:
                    print WarningStyle()+"Warning:"+NormalStyle()+" You have not declared a Nuisance or ReservedNuisance with id='%d'! (assuming consecutive numbers)"%myCounter
                    myCounter = int(n.getId())

    def mergeNuisances(self):
        for mset in self._config.MergeNuisances:
            # check if nuisance with master id can be found
            myFoundStatus = False
            for n in self._extractors:
                if n.isId(mset[0]):
                    myFoundStatus = True
            if not myFoundStatus:
                print ErrorStyle()+"Error in merging Nuisances:"+NormalStyle()+" cannot find a nuisance with id '"+mset[0]+"'!"
                raise Exception()
            # assign master to slave nuisances
            for i in range(1, len(mset)):
                myFoundStatus = False
                for n in self._extractors:
                    if n.isId(mset[i]):
                        n.setAsSlave(mset[0])
                        myFoundStatus = True
                if not myFoundStatus:
                    print ErrorStyle()+"Error in merging Nuisances:"+NormalStyle()+" tried to merge '"+mset[i]+"' (slave) to '"+mset[0]+"' (master) but could not find a nuisance with id '"+mset[i]+"'!"
                    raise Exception()
        print "Merged Nuisances"


    ## Creates extractors for nuisances
    def createControlPlots(self):
        # Protection to create extractors only once
        if len(self._controlPlotExtractors) > 0:
            return

        # Loop over control plot inputs, create extractors for all other columns except QCD factorised
        for c in self._config.ControlPlots:
            self._controlPlotExtractors.append(ControlPlotExtractor(histoSpecs = c.details,
                                               histoTitle = c.title,
                                               histoDirs = c.signalHistoPath,
                                               histoNames = c.signalHistoName))
