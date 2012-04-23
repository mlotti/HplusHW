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
        self._luminosity = -1
        self._columns = []
        self._nuisances = []
        self._QCDmethod = DatacardQCDMethod.UNKNOWN

        # Override options from command line and determine QCD measurement method
        self.overrideConfigOptionsFromCommandLine()

        # Check that all necessary parameters have been specified in config file
        self.checkCfgFile()

        # Create columns (dataset groups)
        self.createDatacardColumns()
        self.checkDatacardColumns()

        # Create extractors for nuisances (data miners for nuisances)
        self.createExtractors()

        # Check nuisances and do merging
        self.checkNuisances()

        # Make datacards
        myTable = TableProducer(opts, config, self._luminosity, self._observation, self._columns, self._nuisances)

        #for c in self._columns:
        #    print c._label, c.getRateValue(self._luminosity)
        print "done."
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
            print "\033[0;41m\033[1;37mError in config '"+self._opts.datacard+"'!\033[0;0m\n"
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
        myEmbeddingPath = multicrabPaths.getEWKPath()
        if not os.path.exists(myEmbeddingPath):
            print "Path for embedding analysis ('"+myEmbeddingPath+"') does not exist!"
            sys.exit()
        myQCDPath = ""
        myQCDCounters = ""
        if self._QCDmethod == DatacardQCDMethod.FACTORISED:
            myQCDPath = multicrabPaths.getQCDFactorisedPath()
            myQCDCounters = self._config.QCDFactorisedAnalysis+"Counters"
        elif self._QCDmethod == DatacardQCDMethod.INVERTED:
            myQCDPath = multicrabPaths.getQCDInvertedPath()
            myQCDCounters = self._config.QCDInvertedAnalysis+"Counters"
        if not os.path.exists(myQCDPath):
            print "Path for QCD measurement ('"+myQCDPath+"') does not exist!"
            sys.exit()
        # Make dataset managers
        myDsetMgrs = [None, # needed for datasetType==None
                      dataset.getDatasetsFromMulticrabCfg(cfgfile=mySignalPath+"/multicrab.cfg", counters=self._config.SignalAnalysis+"Counters"),
                      dataset.getDatasetsFromMulticrabCfg(cfgfile=myEmbeddingPath+"/multicrab.cfg", counters=self._config.SignalAnalysis+"Counters"),
                      dataset.getDatasetsFromMulticrabCfg(cfgfile=myQCDPath+"/multicrab.cfg", counters=myQCDCounters)]
        # Make merges (a unique merge for each data group; used to access counters and histograms)
        for dg in self._config.DataGroups:
            print "Making merged dataset for data group: \033[1;37m"+dg.label+"\033[0;0m"
            myDsetMgr = 0
            mMergedName = ""
            myMergedNameForQCDMCEWK = ""
            if dg.datasetType != "None":
                if dg.datasetType == "Signal":
                    #myDsetMgr = dataset.getDatasetsFromMulticrabCfg(cfgfile=mySignalPath+"/multicrab.cfg", counters=self._config.SignalAnalysis+"Counters")
                    myDsetMgr = 1
                elif dg.datasetType == "Embedding":
                    #myDsetMgr = dataset.getDatasetsFromMulticrabCfg(cfgfile=myEmbeddingPath+"/multicrab.cfg", counters=self._config.SignalAnalysis+"Counters")
                    myDsetMgr = 2
                elif dg.datasetType == "QCD factorised" or dg.datasetType == "QCD inverted":
                    myDsetMgr = 3
                    #myDsetMgr = dataset.getDatasetsFromMulticrabCfg(cfgfile=myQCDPath+"/multicrab.cfg", counters=myQCDCounters)
                # update normalisation info
                #myDsetMgr.updateNAllEventsToPUWeighted() // FIXME enable as soon as new full multicrab dirs exist
                myDsetMgrs[myDsetMgr].loadLuminosities()
                # find dataset names
                allDatasetNames = myDsetMgrs[myDsetMgr].getAllDatasetNames()
                myFoundNames = self.findDatasetNames(dg.label, allDatasetNames, dg.datasetDefinitions)
                # make merged set
                if self._opts.debugConfig:
                    print "Adding datasets to data group '"+dg.label+"':"
                    for n in myFoundNames:
                        print "  "+n
                myMergedName = "dset_"+dg.label.replace(" ","_")
                myDsetMgrs[myDsetMgr].merge(myMergedName, myFoundNames)
                # find datasets and make merged set for QCD MC EWK
                if dg.datasetType == "QCD factorised":
                    myFoundNames = self.findDatasetNames(dg.label, allDatasetNames, dg.MCEWKDatasetDefinitions)
                    # make merged set
                    if self._opts.debugConfig:
                        print "Adding MC EWK datasets to QCD:"
                        for n in myFoundNames:
                            print "  "+n
                    myMergedNameForQCDMCEWK = "dset_"+dg.label.replace(" ","_")+"_MCEWK"
                    myDsetMgrs[myDsetMgr].merge(myMergedNameForQCDMCEWK, myFoundNames)
            # Construct dataset column object
            myColumn = DatacardColumn(label=dg.label,
                                      landsProcess=dg.landsProcess,
                                      enabledForMassPoints = dg.validMassPoints,
                                      datasetType = dg.datasetType,
                                      rateCounter = dg.rateCounter,
                                      nuisances = dg.nuisances,
                                      datasetMgr = myDsetMgrs[myDsetMgr],
                                      datasetMgrColumn = myMergedName,
                                      datasetMgrColumnForQCDMCEWK = myMergedNameForQCDMCEWK, 
                                      additionalNormalisationFactor = dg.additionalNormalisation,
                                      dirPrefix = dg.dirPrefix,
                                      shapeHisto = dg.shapeHisto)
            # Disable non-active QCD measurements
            if dg.datasetType == "QCD factorised" and self._QCDmethod == DatacardQCDMethod.INVERTED:
                myColumn.disable()
            elif dg.datasetType == "QCD inverted" and self._QCDmethod == DatacardQCDMethod.FACTORISED:
                myColumn.disable()
            # Add column
            self._columns.append(myColumn)
            if self._opts.debugConfig:
                myColumn.printDebug()
        # Make datacard column object for observation
        #myDsetMgr = dataset.getDatasetsFromMulticrabCfg(cfgfile=mySignalPath+"/multicrab.cfg", counters=self._config.SignalAnalysis+"Counters")
        # update normalisation info
        #myDsetMgr.updateNAllEventsToPUWeighted() // FIXME enable as soon as new full multicrab dirs exist
        #myDsetMgr.loadLuminosities()
        allDatasetNames = myDsetMgrs[1].getAllDatasetNames()
        myFoundNames = self.findDatasetNames("Observation", allDatasetNames, self._config.Observation.datasetDefinitions)
        if self._opts.debugConfig:
            print "Adding datasets to data group 'Observation':"
            for n in myFoundNames:
                print "  "+n
        myObservationName = "dset_observation"
        myDsetMgrs[1].merge(myObservationName, myFoundNames)
        self._observation = DatacardColumn(label = "Observation",
                                           enabledForMassPoints = self._config.MassPoints,
                                           datasetType = "Observation",
                                           rateCounter = self._config.Observation.rateCounter,
                                           datasetMgr = myDsetMgrs[1],
                                           datasetMgrColumn = myObservationName,
                                           dirPrefix = self._config.Observation.dirPrefix,
                                           shapeHisto = self._config.Observation.shapeHisto)
        if self._opts.debugConfig:
            self._observation.printDebug()
        # Obtain luminosity from observation
        self._luminosity = myDsetMgrs[1].getDataset(myObservationName).getLuminosity()
        print "Luminosity is set to \033[1;37m%f 1/pb\033[0;0m"%self._luminosity # FIXME: should this be set to all the other datasets?
        print "Data groups converted to datacard columns"

    ## Helper function for finding datasets
    def findDatasetNames(self, label, allNames, searchNames):
        myResult = []
        for dset in searchNames:
            myFoundStatus = False
            for dsetfull in allNames:
                if dset in dsetfull:
                    myResult.append(dsetfull)
                    myFoundStatus = True
            if not myFoundStatus:
                print "\033[0;41m\033[1;37mError in dataset group '"+label+"':\033[0;0m cannot find datasetDefinition '"+dset+"'!"
                print "Options are:"
                for dsetfull in allNames:
                    print "  "+dsetfull
                sys.exit()
        return myResult

    ## Check landsProcess in datacard columns
    def checkDatacardColumns(self):
        i = 0
        myFirstValue = 0
        for c in sorted(self._columns, key=lambda x: x.getLandsProcess()):
            if i == 0:
                myFirstValue = c.getLandsProcess()
            else:
                if myFirstValue + i != c.getLandsProcess():
                    print "\033[0;41m\033[1;37mError:\033[0;0m cannot find LandS process '"+str(myFirstValue+i)+"' in data groups! (need to have consecutive numbers; add group with such landsProcess or check input file)"
                    sys.exit()
            i += 1

    ## Creates extractors for nuisances
    def createExtractors(self):
        myMode = ExtractorMode.NUISANCE
        for n in self._config.Nuisances:
            if n.function == "Constant":
                myMode = ExtractorMode.NUISANCE
                if n.upperValue > 0:
                    myMode = ExtractorMode.ASYMMETRICNUISANCE
                self._nuisances.append(ConstantExtractor(exid = n.id,
                                                         constantValue = n.value,
                                                         constantUpperValue = n.upperValue,
                                                         distribution = n.distr,
                                                         description = n.label,
                                                         mode = myMode))
            elif n.function == "Counter":
                self._nuisances.append(CounterExtractor(exid = n.id,
                                                        counterItem = n.counter,
                                                        distribution = n.distr,
                                                        description = n.label,
                                                        mode = myMode))
            elif n.function == "maxCounter":
                self._nuisances.append(MaxCounterExtractor(exid = n.id,
                                                           counterItem = n.counter,
                                                           counterDirs = n.histoDir,
                                                           distribution = n.distr,
                                                           description = n.label,
                                                           mode = myMode))
            elif n.function == "Shape":
                print "fixme: add shape nuisance"
                # FIXME temp code
                self._nuisances.append(ConstantExtractor(exid = n.id, constantValue = 0.0, distribution = n.distr, description = n.label, mode = ExtractorMode.SHAPENUISANCE))
            elif n.function == "ScaleFactor":
                self._nuisances.append(ScaleFactorExtractor(exid = n.id,
                                                            histoDirs = n.histoDir,
                                                            histograms = n.histo,
                                                            normalisation = n.norm,
                                                            distribution = n.distr,
                                                            description = n.label,
                                                            mode = myMode))
            elif n.function == "Ratio":
                self._nuisances.append(RatioExtractor(exid = n.id,
                                                      numeratorCounterItem = n.numerator,
                                                      denominatorCounterItem = n.denominator,
                                                      distribution = n.distr,
                                                      description = n.label,
                                                      scale = n.scaling,
                                                      mode = myMode))
            elif n.function == "QCDFactorised":
                if self._QCDmethod == DatacardQCDMethod.FACTORISED:
                    print "fixme: add QCD factorised"
                    # FIXME temp code
                    self._nuisances.append(ConstantExtractor(exid = n.id, constantValue = 0.0, distribution = n.distr, description = n.label, mode = myMode))
                else:
                    self._nuisances.append(ConstantExtractor(exid = n.id, constantValue = 0.0, distribution = n.distr, description = n.label, mode = myMode))
            elif n.function == "QCDInverted":
                if self._QCDmethod == DatacardQCDMethod.INVERTED:
                    print "fixme: add QCD inverted"
                    # FIXME temp code
                    self._nuisances.append(ConstantExtractor(exid = n.id, constantValue = 0.0, distribution = n.distr, description = n.label, mode = myMode))
                else:
                    self._nuisances.append(ConstantExtractor(exid = n.id, constantValue = 0.0, distribution = n.distr, description = n.label, mode = myMode))
            else:
                print "\033[0;41m\033[1;37mError in nuisance with id='"+n.id+"':\033[0;0m unknown or missing field function '"+n.function+"' (string)!"
                print "Options are: 'Constant', 'Counter', 'maxCounter', 'Shape', 'ScaleFactor', 'Ratio', 'QCDFactorised'"
                sys.exit()
        # Create reserved nuisances
        for n in self._config.ReservedNuisances:
            self._nuisances.append(ConstantExtractor(exid = n[0], constantValue = 0.0, distribution = "lnN", description = n[1], mode = myMode))
        # Done
        print "Created Nuisances"

    def checkNuisances(self):
        # Check for duplicates
        for i in range(0,len(self._nuisances)):
            for j in range(0,len(self._nuisances)):
                if self._nuisances[i].isId(self._nuisances[j].getId()) and i != j:
                    print "\033[0;41m\033[1;37mError:\033[0;0m You have defined two nuisances with id='"++"'! The id has to be unique!"
                    sys.exit()
        # Merge nuisances
        self.mergeNuisances()
        # Check consecutive id's
        myCounter = 0
        for n in sorted(self._nuisances, key=lambda x: x.getId()):
            if n.isPrintable():
                myCounter += 1
                if int(n.getId()) != myCounter:
                    print "\033[0;37m\033[1;37mWarning:\033[0;0m You have not declared a Nuisance or ReservedNuisance with id='%d'!"%myCounter
                    myCounter = int(n.getId())

    def mergeNuisances(self):
        for mset in self._config.MergeNuisances:
            # check if nuisance with master id can be found
            myFoundStatus = False
            for n in self._nuisances:
                if n.isId(mset[0]):
                    myFoundStatus = True
            if not myFoundStatus:
                print "\033[0;41m\033[1;37mError in merging Nuisances:\033[0;0m cannot find a nuisance with id '"+mset[0]+"'!"
                sys.exit()
            # assign master to slave nuisances
            for i in range(1, len(mset)):
                myFoundStatus = False
                for n in self._nuisances:
                    if n.isId(mset[i]):
                        n.setAsSlave(mset[0])
                        myFoundStatus = True
                if not myFoundStatus:
                    print "\033[0;41m\033[1;37mError in merging Nuisances:\033[0;0m tried to merge '"+mset[i]+"' (slave) to '"+mset[0]+"' (master) but could not find a nuisance with id '"+mset[i]+"'!"
                    sys.exit()
        print "Merged Nuisances"

