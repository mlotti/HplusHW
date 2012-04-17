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

import HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.MulticrabPathFinder as PathFinder

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.aux import sort

# main class for generating the datacards from a given cfg file

class DatacardQCDMethod:
    UNKNOWN = 0
    FACTORISED = 1
    INVERTED = 2

class DataCardGenerator:
    def __init__(self, config, opts):
	self._config = config
	self._opts = opts
        self._observation = None
        self._columns = []
        self._nuisances = []
        self._QCDmethod = DatacardQCDMethod.UNKNOWN
       
        # Override options from command line and determine QCD measurement method
        self.overrideConfigOptionsFromCommandLine()
        
        # Check that all necessary parameters have been specified in config file
        self.checkCfgFile()
       
        # Create columns (dataset groups)
        self.createDatacardColumns()

        

	#if (opts.debugConfig):
        #    config.DataGroups.Print()
        #    config.Nuisances.Print()

	#self.reportUnusedNuisances()

    def overrideConfigOptionsFromCommandLine(self):
        # Obtain QCD measurement method
        if self._config.QCDMeasurementMethod == None:
            self._QCDmethod = DatacardQCDMethod.UNKNOWN
        elif self._config.QCDMeasurementMethod == "QCD factorised":
            self._QCDmethod = DatacardQCDMethod.FACTORISED
        elif self._config.QCDMeasurementMethod == "QCD inverted":
            self._QCDmethod = DatacardQCDMethod.INVERTED
        else:
            self._QCDmethod = DatacardQCDMethod.UNKNOWN
        if self._opts.useQCDfactorised:
            self._QCDmethod = DatacardQCDMethod.FACTORISED
        if self._opts.useQCDinverted:
            self._QCDmethod = DatacardQCDMethod.INVERTED

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
        if self._config.SignalAnalysis == None:
            mymsg += "- missing field 'SignalAnalysis' (string, name of EDFilter/EDAnalyzer process that produced the root files for signal analysis)\n"
        if self._QCDmethod == DatacardQCDMethod.FACTORISED and self._config.QCDFactorisedAnalysis == None:
            mymsg += "- missing field 'QCDFactorisedAnalysis' (string, name of EDFilter/EDAnalyzer process that produced the root files for QCD measurement factorised)\n"
        if self._QCDmethod == DatacardQCDMethod.INVERTED and self._config.QCDInvertedAnalysis == None:
            mymsg += "- missing field 'QCDInvertedAnalysis' (string, name of EDFilter/EDAnalyzer process that produced the root files for QCD measurement inverted)\n"
        if self._QCDmethod == DatacardQCDMethod.UNKNOWN:
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
        elif len(self._config.ShapeHistogramsDimensions) != 3:
            mymsg += "- field 'ShapeHistogramsDimensions' has to contain a list of three parameters (number of bins, minimum, and maximum)\n"
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
        # determine if datacard was ok
        if mymsg != "":
            print "Error in config '"+self._opts.datacard+"'!\n"
            print mymsg
            sys.exit()

    ## Reads datagroup definitions from columns and initialises datasets
    def createDatacardColumns(self):
        # Obtain paths to multicrab directories
        multicrabPaths = PathFinder.MulticrabPathFinder(self._config.Path)
        mySignalPath = multicrabPaths.getSignalPath()
        if not os.path.exists(mySignalPath):
            print "Path for signal analysis ('"+mySignalPath+"') does not exist!"
            sys.exit()
        myEmbeddingPath = multicrabPaths.getSignalPath()
        if not os.path.exists(myEmbeddingPath):
            print "Path for embedding analysis ('"+myEmbeddingPath+"') does not exist!"
            sys.exit()
        myQCDPath = ""
        if self._QCDmethod == DatacardQCDMethod.FACTORISED:
            myQCDPath = multicrabPaths.getQCDFactorisedPath()
        elif self._QCDmethod == DatacardQCDMethod.INVERTED:
            myQCDPath = multicrabPaths.getQCDInvertedPath()
        if not os.path.exists(myQCDPath):
            print "Path for QCD measurement ('"+myQCDPath+"') does not exist!"
            sys.exit()
        # Construct dataset managers
        print "Initialising datasetManagers"
        dsetMgrSignal = dataset.getDatasetsFromMulticrabCfg(cfgfile=mySignalPath+"/multicrab.cfg")
        dsetMgrEmbedding = dataset.getDatasetsFromMulticrabCfg(cfgfile=myEmbeddingPath+"/multicrab.cfg")
        dsetMgrQCD = dataset.getDatasetsFromMulticrabCfg(cfgfile=myQCDPath+"/multicrab.cfg")
        myManagers = [0, dsetMgrSignal, dsetMgrEmbedding, dsetMgrQCD]
        print "Applying normalisation to datasetManagers"
        for mgr in myManagers:
            # update normalisation info
            mgr.updateNAllEventsToPUWeighted()
            mgr.loadLuminosities()
        
        # Make merges (a unique merge for each data group; used to access counters and histograms)
        for dg in self._config.DataGroups:
            print "Making merged dataset for data group: ",dg.label
            allDatasetNames = []
            mgrIndex = 0 # needed for datasetType==None 
            if dg.datasetType == "Signal":
                mgrIndex = 1
            elif dg.datasetType == "Embedding":
                mgrIndex = 2
            elif dg.datasetType == "QCD factorised" or dg.datasetType == "QCD inverted":
                mgrIndex = 3
            allDatasetNames = []
            if mgrIndex > 0:
                myManagers[mgrIndex].getAllDatasetNames()
            # find dataset names
            myMergedName = ""
            if dg.datasetType != "None":
                myFoundNames = self.findDatasetNames(dg.label, allDatasetNames, dg.datasetDefinitions)
                mySelectedString = ""
                for item in myFoundNames:
                    mySelectedString += ',"'+dsetfull+'"'
                # make merged set
                myMergedName = "dset_"+dg.label.replace(" ","_")
                myManagers[mgrIndex].merge('"'+myMergedName+'"'+mySelectedString)
            # find datasets and make merged set for QCD MC EWK
            myMergedNameForQCDMCEWK = ""
            if dg.datasetType == "QCD factorised":
                myFoundNames = self.findDatasetNames(dg.label, allDatasetNames, dg.MCEWKDatasetDefinitions)
                mySelectedString = ""
                for item in myFoundNames:
                    mySelectedString += ',"'+dsetfull+'"'
                # make merged set
                myMergedNameForQCDMCEWK = "dset_"+dg.label.replace(" ","_")+"_MCEWK"
                myManagers[mgrIndex].merge('"'+myMergedNameForQCDMCEWK+'"'+mySelectedString)
            # Construct dataset column object
            myColumn = DatacardColumn(label=dg.label,
                                      landsProcess=dg.landsProcess,
                                      enabledForMassPoints = dg.validMassPoints,
                                      datasetType = dg.datasetType,
                                      rateCounter = dg.rateCounter,
                                      nuisances = dg.nuisances,
                                      datasetMgr = myManagers[mgrIndex],
                                      datasetMgrColumn = myMergedName,
                                      datasetMgrColumnForQCDMCEWK = myMergedNameForQCDMCEWK, 
                                      additionalNormalisationFactor = dg.additionalNormalisation,
                                      dirPrefix = dg.dirPrefix,
                                      shapeHisto = dg.shapeHisto)
            self._columns.append(myColumn)
            if self._opts.debugConfig:
                myColumn.printDebug()

    def findDatasetNames(self, label, allNames, searchNames):
        myResult = []
        for dset in searchNames:
            myFoundStatus = False
            for dsetfull in allNames:
                if set in dsetfull:
                    myResult.append(dsetfull)
                    myFoundStatus = True
            if not myFoundStatus:
                print "Error in dataset group '"+label+"': cannot find datasetDefinition '"+dset+"'!"
                print "Options are:"
                for dsetfull in allDatasetNames:
                    print "  "+dsetfull
                sys.exit()
        return myResult

    def reportUnusedNuisances(self):
	usedNuisances = []
        for nuisance in self._config.Nuisances.nuisances.keys():
	    for datagroup in self._config.DataGroups.datagroups.keys():
		for usedNuisance in self._config.DataGroups.get(datagroup).nuisances:
		    if usedNuisance == nuisance:
			usedNuisances.append(nuisance)
	usedNuisances = self.rmDuplicates(usedNuisances)
	unUsedNuisances = []
	for nuisance in self._config.Nuisances.nuisances.keys():
	    if nuisance not in usedNuisances:
		#print "UNUSED NUISANCE"
		#config.Nuisances.get(nuisance).Print
		unUsedNuisances.append(nuisance)
	print "Unused nuisances",sort(unUsedNuisances)

    def rmDuplicates(self,list):
	retlist = []
	for element in list:
	    if element not in retlist:
		retlist.append(element)
	return retlist

    def generate(self):
	signalDir = []
	signalDir.append(self._config.multicrabPaths.getSignalPath())
	datasets = dataset.getDatasetsFromMulticrabDirs(signalDir,counters=self._config.CounterDir)
	datasets.loadLuminosities()
	plots.mergeRenameReorderForDataMC(datasets)
	luminosity = datasets.getDataset("Data").getLuminosity()
        print "Luminosity = ",luminosity

