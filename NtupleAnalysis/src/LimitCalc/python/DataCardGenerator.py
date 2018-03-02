#!/usr/bin/env python

#================================================================================================
# Import modules
#================================================================================================
import os
import sys
import cProfile
import json

import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import HiggsAnalysis.NtupleAnalysis.tools.counter as counter
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots

import HiggsAnalysis.LimitCalc.DatacardColumn as DatacardColumn
import HiggsAnalysis.LimitCalc.Extractor as Extractor
import HiggsAnalysis.LimitCalc.TableProducer as TableProducer
import HiggsAnalysis.NtupleAnalysis.tools.ShellStyles as ShellStyles
import HiggsAnalysis.NtupleAnalysis.tools.multicrabConsistencyCheck as consistencyCheck
from HiggsAnalysis.NtupleAnalysis.tools.systematics import ScalarUncertaintyItem

import HiggsAnalysis.LimitCalc.MulticrabPathFinder as PathFinder

import ROOT
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux

#================================================================================================
# Class definition
#================================================================================================
class DatacardQCDMethod:
    '''
    main class for generating the datacards from a given cfg file
    '''
    UNKNOWN = 0
    FACTORISED = 1
    INVERTED = 2
    MC = 3

class DatacardDatasetMgrSourceType:
    SIGNALANALYSIS  = 0
    BKGMEASUREMENT1 = 1
    BKGMEASUREMENT2 = 2 #Assumed to be Data-Driven. Must improve this in the future
    #EMBEDDING      = 1 
    #QCDMEASUREMENT = 2

class DatasetMgrCreatorManager:
    def __init__(self, opts, config, signalDsetCreator, bkg1DsetCreator, bkg2DsetCreator, verbose=False):
        self._verbose = verbose
        self._dsetMgrCreators = [signalDsetCreator, bkg1DsetCreator, bkg2DsetCreator]
        self._dsetMgrs = []
        self._luminosities = []
        self._mainCounterTables = []
        if config.ToleranceForLuminosityDifference == None:
            msg = "Input datacard should contain entry for ToleranceForLuminosityDifference (for example: ToleranceForLuminosityDifference=0.01)!"
            raise Exception(ShellStyles.ErrorLabel() + msg + ShellStyles.NormalStyle())
        self._toleranceForLuminosityDifference = config.ToleranceForLuminosityDifference
        self._optionDebugConfig = opts.debugConfig
        self._config = config
        return

    def Verbose(self, msg, printHeader=True):
        '''
        Calls Print() only if verbose options is set to true
        '''
        if not self._verbose:
            return
        Print(msg, printHeader)
        return

    def Print(self, msg, printHeader=True):
        '''
        Simple print function. If verbose option is enabled prints, otherwise does nothing
        '''
        fName = __file__.split("/")[-1]
        if printHeader:
            print "=== ", fName
        print "\t", msg
        return

    def __del__(self):
        self.closeManagers()
        for d in self._dsetMgrCreators:
            if d != None:
                d.close()
        self._dsetMgrCreators = []
        self._dsetMgrs = []
        self._luminosities = []
        self._mainCounterTables = []

    def closeManagers(self):
        for dMgr in self._dsetMgrs:
            if dMgr != None:
                dMgr.close()
        self._dsetMgrs = []
        self.Verbose("DatasetManagerCreators closed", True)
        return

    def obtainDatasetMgrs(self, era, searchMode, optimizationMode, verbose=False):
        if len(self._dsetMgrs) > 0:
            msg = "The obtainDatasetMgrs() function has already been called before. The dsetMgrs exist!"
            raise Exception(ShellStyles.ErrorLabel() + msg + ShellStyles.NormalStyle())

        # For-loop: All dset manager creators
        for i in range(0, len(self._dsetMgrCreators)):
            self.Verbose(self.getDatasetMgrLabel(i), i==0)

            # No dsetMgrCreator, append zero pointers to retain list dimension
            if self._dsetMgrCreators[i] == None:
                self._dsetMgrs.append(None)
                self._luminosities.append(None)
                continue

            # Create DatasetManager object and set pointer to the selected era, searchMode, and optimizationMode
            myDsetMgr = self._dsetMgrCreators[i].createDatasetManager(dataEra=era, searchMode=searchMode, optimizationMode=optimizationMode)

            # Check consistency
            consistencyCheck.checkConsistencyStandalone(self._dsetMgrCreators[i]._baseDirectory,myDsetMgr,name=self.getDatasetMgrLabel(i))

            # Normalize
            myDsetMgr.updateNAllEventsToPUWeighted()

            # Obtain integrated luminosity
            self._luminosities.append( self._getIntLumi(i, myDsetMgr) )

            # Merge divided datasets
            plots.mergeRenameReorderForDataMC(myDsetMgr)

            # Show info of available datasets
            if verbose:
                msg = "Dataset merging structure for %s " % (self.getDatasetMgrLabel(i))
                print ShellStyles.NoteStyle() + msg + ShellStyles.NormalStyle()
                myDsetMgr.printDatasetTree()

            # Store DatasetManager
            self._dsetMgrs.append(myDsetMgr)

            # For embedding. fixme: Santeri (is this needed?) #fixme: santeri. Is this needed?
            #if i == DatacardDatasetMgrSourceType.EMBEDDING:
            #    myProperty = myDsetMgr.getAllDatasets()[0].getProperty("analysisName")

        # Sanity check for luminosity
        self._checkLuminosityMatching()
        return

    
    def _getIntLumi(self, index, myDsetMgr):
        '''
        Determines the integrated luminosity of the datacard
        dataset manager according to its type
        
        ToDo: Rewrite into something that makes sense
        and is more fail-safe
        '''
        intLumi = 0.0
        if index == DatacardDatasetMgrSourceType.SIGNALANALYSIS:
            
            if 0:
                myDsetMgr.PrintInfo()
                self.Print("Base directory = %s" %  (myDsetMgr.getAllDatasets()[0].getBaseDirectory()))
            myDsetMgr.loadLuminosities()

            # For-loop: All data datasets
            for d in myDsetMgr.getDataDatasets():
                intLumi += d.getLuminosity()
        elif index == DatacardDatasetMgrSourceType.BKGMEASUREMENT2:
            # For-loop: All datasets looking for the pseudo-dataset (smoking gun for data-driven pseudo-dataset)
            for d in myDsetMgr.getAllDatasets():
                if d.isMC() or d.isData():
                    continue
                elif d.isPseudo():
                    baseDir =  d.getBaseDirectory()
                    intLumi = d.getLuminosity()
                    self.Verbose("Found pseudo-dataset %s for dataset manager in dir %s. Saving integrated lumi of %.1f" % (d.getName(), baseDir, d.getLuminosity()), True)
                else:
                    raise Exception("This should never be reached")
        else:
            # For-loop: All datasets looking for the pseudo-dataset (smoking gun for data-driven pseudo-dataset)
            for d in myDsetMgr.getAllDatasets():
                if d.isMC() or d.isPseudo():
                    continue
                elif d.isData():
                    intLumi += d.getLuminosity()
                else:
                    raise Exception("This should never be reached")
        
        # Print only when there's a problem
        msg = "Integrated lumi for dataset manager with index %d is %.1f" % (index, intLumi)
        if intLumi == 0:
            self.Print(ShellStyles.NoteStyle() + msg + ShellStyles.NormalStyle(), True)
        else:
            self.Verbose(msg, True)
        return intLumi

    def cacheMainCounterTables(self):
        # Note: needs to be called after all merging operations have been done
        for i in range(0,len(self._dsetMgrs)):
            if self.getDatasetMgr(i) == None:
                self._mainCounterTables.append(None)
            else:
                # Obtain main counter tables
                myEventCounter = counter.EventCounter(self.getDatasetMgr(i), countNameFunction=None, counters=None, mainCounterOnly=True)
                myEventCounter.normalizeMCToLuminosity(self.getLuminosity(i))
                self._mainCounterTables.append(myEventCounter.getMainCounterTable())

    def getNmax(self):
        return len(self._dsetMgrs)

    def getDatasetMgr(self, i):
        '''
        Returns datasetMgr object, index must conform to DatacardDatasetMgrSourceType. 

        Note: can return also a None object
        '''
        if len(self._dsetMgrs) == 0:
            msg = "The function obtainDatasetMgrs() needs to be called first!"
            raise Exception(ShellStyles.ErrorStyle() + msg + ShellStyles.NormalStyle())

        if i < 0 or i >= len(self._dsetMgrs):
            msg = "DatasetMgrCreatorManager::getDatasetMgr(...) index = %d is out of range!" % i
            raise Exception(ShellStyles.ErrorStyle() + msg + ShellStyles.NormalStyle())
        return self._dsetMgrs[i]

    def getDatasetMgrLabel(self, i):
        ''' 
        WARNING! This is dangerous! FIXME! santeri
        '''
        if i == DatacardDatasetMgrSourceType.SIGNALANALYSIS:             
            return "Signal analysis" 
        elif i == DatacardDatasetMgrSourceType.BKGMEASUREMENT1: #DatacardDatasetMgrSourceType.EMBEDDING: #fixme
            #return "Embedding"
            return "Bkg1"
        elif i == DatacardDatasetMgrSourceType.BKGMEASUREMENT2: #DatacardDatasetMgrSourceType.QCDMEASUREMENT: #fixme
            return "Bkg2"
        else:
            msg = "The  index = %d is out of range!" % (i)
            raise Exception(ShellStyles.ErrorStyle() + msg + ShellStyles.NormalStyle())

    def getLuminosity(self, i):
        if len(self._luminosities) == 0:
            msg =  "The function obtainDatasetMgrs() needs to be called first, before getting luminosity"
            raise Exception(ShellStyles.ErrorStyle() + msg + ShellStyles.NormalStyle())

        if i < 0 or i >= len(self._dsetMgrs):
            msg =  "The index = %d is out of range!" % (i)
            raise Exception(ShellStyles.ErrorStyle() + msg + ShellStyles.NormalStyle())
        return self._luminosities[DatacardDatasetMgrSourceType.SIGNALANALYSIS]

    def getMainCounterTable(self, i):
        if len(self._mainCounterTables) == 0:
            msg = "The function cacheMainCounterTables(...) needs to be called first!"
            raise Exception(ShellStyles.ErrorStyle() + msg + ShellStyles.NormalStyle())

        if i < 0 or i >= len(self._dsetMgrs):
            msg = "The index = %d is out of range!" % (i)
            raise Exception(ShellStyles.ErrorStyle() + msg + ShellStyles.NormalStyle())
        return self._mainCounterTables[i]

    def mergeDatasets(self, i, mergeGroupLabel, searchNames):
        '''
        Merges the list of datasets (if they exist) into one object. The merged group is then used to access counters and histograms
        '''
        if self.getDatasetMgr(i) == None:
            return

        # Obtain all dataset names
        myAllDatasetNames = self.getDatasetMgr(i).getAllDatasetNames()
        # Find datasets matching to search conditions
        myMatchedDatasetNames = []
        for searchName in searchNames:
            myFoundStatus = False
            for dset in myAllDatasetNames:
                if searchName in dset:
                    # Replace files existing in _physicalMcAdd
                    myReplacedStatus = False
                    for key in plots._physicalMcAdd:
                        if dset == key:
                            myReplacedStatus = True
                            if plots._physicalMcAdd[key] in myResult:
                                print "    Replaced dataset '%s'->'%s', exists already"%(key,plots._physicalMcAdd[key])
                            else:
                                print "    Replaced dataset '%s'->'%s'"%(key,plots._physicalMcAdd[key])
                                myMatchedDatasetNames.append(dset)
                    if not myReplacedStatus:
                        myMatchedDatasetNames.append(dset)
                    myFoundStatus = True
            if not myFoundStatus and len(myAllDatasetNames) > 0:
                print ShellStyles.ShellStyles.ErrorLabel()+" Dataset group '%s': cannot find datasetDefinition '%s'!"%(mergeGroupLabel,searchName)
                print "Options are: %s"%(', '.join(map(str, myAllDatasetNames)))
                raise Exception()
        #if self._optionDebugConfig:
            #print "Added to data group '%s' the following datasets:"%(mergeGroupLabel)
            #for n in myMatchedDatasetNames:
                #print "  "+n
        # Now do the merge
        self.getDatasetMgr(i).merge(mergeGroupLabel, myMatchedDatasetNames, silent=True)

    def printDatasetMgrContents(self):
        for i in range(0,len(self._dsetMgrs)):
            if self.getDatasetMgr(i) != None:
                print "DatasetMgr contains following datasets for '%s'"%self.getDatasetMgrLabel(i)
                self.getDatasetMgr(i).printInfo()

    def _checkLuminosityMatching(self):
        '''
        Ensures that the integrated luminosity is the 
        same for all dataset managers
        '''
        # For-loop: All lumis
        for i, lumi in enumerate(self._luminosities, 0):
            self.Verbose("Lumi for dataset manager \"%s\" is set to %.1f 1/pb" % (self.getDatasetMgrLabel(i), lumi), i==0)

        # Compare luminosities to signal analysis
        if len(self._luminosities) == 0:
            msg = "The function obtainDatasetMgrs() needs to be called first!"
            raise Exception(ShellStyles.ErrorStyle() + msg + ShellStyles.NormalStyle())
        mySignalLuminosity = self._luminosities[DatacardDatasetMgrSourceType.SIGNALANALYSIS]
        
        # For-loop: All stored luminosities
        for i, lumi in enumerate(self._luminosities, 0):

            # Calculate lumi difference wrt signal analysis
            myDiff = abs(self._luminosities[i] / mySignalLuminosity - 1.0)

            if myDiff > self._toleranceForLuminosityDifference:
                msg = "Signal and data-driven luminosities differ more than 1 %%! (%s vs. %s)" % (self._luminosities[i], mySignalLuminosity)
                raise Exception(ShellStyles.ErrorStyle() + msg + ShellStyles.NormalStyle() )
            elif myDiff > 0.0001:
                signalLabel  = self.getDatasetMgrLabel(DatacardDatasetMgrSourceType.SIGNALANALYSIS)
                datasetLabel = self.getDatasetMgrLabel(i)
                msg = "%s and %s luminosities differ slightly (%.2f %%)!" % (signalLabel, datasetLabel, myDiff*100.0)
                self.Verbose(ShellStyles.ErrorStyle() + msg + ShellStyles.NormalStyle() )
        return

class DataCardGenerator:
    def __init__(self, opts, config, verbose=True, h2tb=False):
        self.verbose = verbose
        self._opts = opts
        self._h2tb = h2tb
        self._config = config
        self._dsetMgrManager = None # Manager for datasetMgrCreators (DatasetMgrCreatorManager object)
        self._observation = None # Datacard column
        self._columns = [] # Datacard column
        self._extractors = [] # Extractor objects
        self._controlPlotExtractors = [] # Control plot extractors
        self._checkInputDatacard()
        self._outputPrefix = self._getBasicOutputPrefix()
        return

    def Verbose(self, msg, printHeader=True):
        '''
        Calls Print() only if verbose options is set to true
        '''
        if not self.verbose:
            return
        Print(msg, printHeader)
        return

    def Print(self, msg, printHeader=True):
        '''
        Simple print function. If verbose option is enabled prints, otherwise does nothing
        '''
        fName = __file__.split("/")[-1]
        if printHeader:
            print "=== ", fName
        print "\t", msg
        return
    
    def __del__(self):
        if self.verbose:
            self.Print("Deleting cached objects", True)
        self.closeFiles()
        self.opts = None
        self._config = None
        del self._dsetMgrManager
        self._dsetMgrManager = None
        self._observation = None
        for c in self._columns:
            del c
        self._columns = None
        for e in self._extractors:
            del e
        self._extractors = None
        for e in self._controlPlotExtractors:
            del e
        self._controlPlotExtractors = None
        return

    def setDsetMgrCreators(self, signalDsetCreator, bkg1DsetCreator, bkg2DsetCreator):
        self._dsetMgrManager = DatasetMgrCreatorManager(self._opts, self._config, signalDsetCreator, bkg1DsetCreator, bkg2DsetCreator)


        dirList = [signalDsetCreator.getBaseDirectory()]
        if bkg1DsetCreator != None:
            dirList.append(bkg1DsetCreator.getBaseDirectory())

        if bkg2DsetCreator != None:
            dirList.append(bkg2DsetCreator.getBaseDirectory())

        self.Verbose("Objects passed using as input the following directories:\n\t%s" % ("\n\t".join(dirList)), True)
        return

    def _getBasicOutputPrefix(self):
        '''
        Construct prefix for output dir name
        '''
        prefix = self._config.Path.split("/")[-1]

        if hasattr(self._config, 'OptionGenuineTauBackgroundSource'):
            prefix += "_%s" % (self._config.OptionGenuineTauBackgroundSource)

        if hasattr(self._config, 'OptionFakeBMeasurementSource'):
            prefix += "_%s" %  (self._config.OptionFakeBMeasurementSource)
            
        # Append mass range in prefix in the form (mH_X_to_Y)
        massRange = "_mH%s" % (str(self._config.MassPoints[0]))
        if len(self._config.MassPoints) > 0:
            massRange += "to%s" % (str(self._config.MassPoints[-1]))
        prefix += massRange

        self.Verbose("Output dir prefix (basic) is \"%s\"" % (prefix), True)
        return prefix
        
    def _getFinalOutputPrefix(self,era, searchMode, optimizationMode):
        '''
        Construct final, prefix for output dir name
        '''
        # Construct prefix extension
        if optimizationMode == "":
            optMode = "OptNominal"
        else:
            optMode = "Opt%s" % optimizationMode
        s = "%s_%s_%s"%(era, searchMode, optMode)

        # Prepend prefix to output prefix name
        self._outputPrefix = s + "_" + self._outputPrefix
        self.Verbose("Output dir prefix (final) is \"%s\"" % (self._outputPrefix), True)
        return

    def doDatacard(self, era, searchMode, optimizationMode, mcrabInfoOutput):
        def applyWeighting(h, myJsonBins):
            myWeightBin = 0
            for i in range(1, h.GetNbinsX()+1):
                if myWeightBin < len(myJsonBins)-1:
                    if not h.GetXaxis().GetBinLowEdge(i) + 0.0001 < myJsonBins[myWeightBin+1]["mt"]:
                        myWeightBin += 1
                self.Print("hbin edge=",h.GetXaxis().GetBinLowEdge(i),"weight edge=",myJsonBins[myWeightBin]["mt"], True)
                h.SetBinContent(i, h.GetBinContent(i) * myJsonBins[myWeightBin]["efficiency"])
            return

        self.Verbose("Prepend era, searchMode, and optimizationMode to the output dir prefix")
        self._getFinalOutputPrefix(era, searchMode, optimizationMode)

        self.Verbose("Get dataset managers for the era / searchMode / optimizationMode combination")
        self._dsetMgrManager.obtainDatasetMgrs(era, searchMode, optimizationMode, self.verbose)

        self.Verbose("Create columns (dataset groups)")
        self.createDatacardColumns()
        self.checkDatacardColumns()

        self.Verbose("Create extractors and control plot extractors")
        self.createExtractors()
        self.createControlPlots()

        self.Verbose("Do data mining to cache results into datacard column objects")
        self.doDataMining()

        # Merge columns, if necessary
        if hasattr(self._config, "mergeColumnsByLabel"):
            for item in self._config.mergeColumnsByLabel:
                mySubtractColumnList = []
                if "subtractList" in item.keys():
                    mySubtractColumnList = item["subtractList"][:]
                if self.verbose:
                    print "\nPerforming merge for %s"%item["label"]
                
                targetColumn       = item["mergeList"][0]
                targetColumnNewName= item["label"]
                addColumnList      = item["mergeList"][1:]
                self.separateMCEWKTausAndFakes(targetColumn, targetColumnNewName, addColumnList, mySubtractColumnList)
        
        # Do rebinning of results, store a fine binned copy of all histograms as well
        for i, c in enumerate(self._columns, 1):
            self.Verbose("Rebinning cached results for column \"%s\" with %d nuisances" % (c.getLabel(), len(c.getNuisanceIds())), i==1)
            c.doRebinningOfCachedResults(self._config)

        # Rebin cached results for data (observation)
        self.Verbose("Rebinning cached results observation")
        self._observation.doRebinningOfCachedResults(self._config)

        # Separate nuisances with additional information into an individual nuisance (horror!)
        for c in self._columns:
            myNewNuisanceIdsList = c.doSeparateAdditionalResults()
            # Append
            for item in myNewNuisanceIdsList:
                myFoundStatus = False
                for e in self._extractors:
                    if item == e.getId():
                        myFoundStatus = True
                if not myFoundStatus:
                    exid          = item
                    constantValue = -1.0
                    distribution  = "lnN"
                    description   = item+" normalization"
                    mode          = Extractor.ExtractorMode.ASYMMETRICNUISANCE
                    myExtractor   = Extractor.ConstantExtractor(exid, constantValue, distribution, description, mode)
                    self._extractors.append(myExtractor)

        # Make datacards
        opts            = self._opts
        config          = self._config
        outputPrefix    = self._outputPrefix
        luminosity      = self._dsetMgrManager.getLuminosity(DatacardDatasetMgrSourceType.SIGNALANALYSIS)
        observation     = self._observation
        datasetGroups   = self._columns
        extractors      = self._extractors
        mcrabInfoOutput = mcrabInfoOutput
        myProducer = TableProducer.TableProducer(opts, config, outputPrefix, luminosity, observation, datasetGroups, extractors, mcrabInfoOutput)

        # Close files
        self.closeFiles()

        # Return name of output directory
        return myProducer.getDirectory()

    def _checkInputDatacard(self):
        '''
        Check that all necessary parameters have been specified in config file
        '''
        msg = ""
        if self._config.DataCardName == None:
            msg += "- missing field 'DataCardName' (string, describes the name of the datacard)\n"

        if self._config.Path == None:
            msg += "- missing field 'Path' (string, path to directory containing all multicrab directories to be used for datacards)\n"
        elif not os.path.exists(self._config.Path):
            msg += "- 'Path' points to directory that does not exist!\n"

        if self._config.MassPoints == None:
            msg += "- missing field 'MassPoints' (list of integers, mass points for which datacard is generated)!\n"
        elif len(self._config.MassPoints) == 0:
            msg += "- field 'MassPoints' needs to have at least one entry! (list of integers, mass points for which datacard is generated)\n"

        if self._config.BlindAnalysis == None:
            msg += "- field 'BlindAnalysis' needs to be set as True or False!\n"

        if self._config.Observation == None:
            msg += "- missing field 'Observation' (ObservationInput object)\n"

        if self._config.DataGroups == None:
            msg += "- missing field 'DataGroups' (list of DataGroup objects)\n"
        elif len(self._config.DataGroups) == 0:
            msg += "- need to specify at least one DataGroup to field 'DataGroups' (list of DataGroup objects)\n"

        if self._config.Nuisances == None:
            msg += "- missing field 'Nuisances' (list of Nuisance objects)\n"
        elif len(self._config.Nuisances) == 0:
            msg += "- need to specify at least one Nuisance to field 'Nuisances' (list of Nuisance objects)\n"

        if self._config.ControlPlots == None:
            self.Print(ShellStyles.NoteStyle() + "You did not specify any ControlPlots in the config (ControlPlots is list of ControlPlotInput objects)!" + ShellStyles.NormalStyle(), True)

        # Determine whether the input datacard was ok
        if msg != "":
            msg += "Please check the input template datacatd provided \"%s\"'" % (self._opts.datacard)
            raise Exception(ShellStyles.ErrorStyle() + msg + ShellStyles.NormalStyle())

        # Print a nice table with the above parameters?
        if self.verbose:
            self.PrintDatacardOptions()
        return

    def PrintDatacardOptions(self):
        '''
        Print all datacard options
        '''
        align = "{:<20} {:<80} "
        table = []
        hLine = "="*100
        table.append(hLine)
        table.append(align.format("Variable Name", "Variable Value"))
        table.append(hLine)
        table.append(align.format("Datacard Name"  , self._config.DataCardName))
        table.append(align.format("Path"           , self._config.Path))
        table.append(align.format("Mass Points"    , ", ".join(map(str,self._config.MassPoints))) )
        table.append(align.format("Blind Analysis" , self._config.BlindAnalysis))
        table.append(align.format("Observation"    , self._config.Observation))
        table.append(align.format("# Data Groups"  , len(self._config.DataGroups) ))
        table.append(align.format("# Nuisances"    , len(self._config.Nuisances) ))
        table.append(align.format("# Control Plots", len(self._config.ControlPlots) ))
        table.append(hLine)
        table.append("")

        for i, row in enumerate(table, 1):
            self.Print(row, i==1)        
        return

    def createDatacardColumns(self):
        '''
        Reads datagroup definitions from columns and initialises datasets
        '''

        # Make datacard column object for observation
        if self._dsetMgrManager.getDatasetMgr(DatacardDatasetMgrSourceType.SIGNALANALYSIS) != None:
            self._observation = DatacardColumn.DatacardColumn(opts=self._opts,
                                                              label = "data_obs",
                                                              enabledForMassPoints = self._config.MassPoints,
                                                              datasetType = "Observation",
                                                              datasetMgrColumn = self._config.Observation.datasetDefinition,
                                                              shapeHistoName = self._config.Observation.shapeHistoName,
                                                              histoPath = self._config.Observation.histoPath,
                                                              additionalNormalisationFactor = self._config.Observation.additionalNormalisation)
            if self._opts.debugConfig:
                self._observation.printDebug()
        else:
            self.Print(ShellStyles.WarningLabel() + "No observation will be extracted, because signal analysis is disabled", True)

        # Loop over data groups to create datacard columns
        for dg in self._config.DataGroups:
            myIngoreOtherQCDMeasurementStatus = (dg.datasetType == "QCD factorised" and self._QCDMethod == DatacardQCDMethod.INVERTED) or (dg.datasetType == "QCD inverted" and self._QCDMethod == DatacardQCDMethod.FACTORISED)
            myMassIsConsideredStatus = False
            for validMass in dg.validMassPoints:
                if validMass in self._config.MassPoints:
                    myMassIsConsideredStatus = True
            if not myIngoreOtherQCDMeasurementStatus and myMassIsConsideredStatus:
                if self.verbose:
                    print "Constructing datacard column for data group %s%s" % (ShellStyles.NoteStyle() + dg.label, ShellStyles.NormalStyle())

                # Construct datacard column object
                myColumn = None
                if dg.datasetType == "Embedding":
                    myColumn = DatacardColumn.DatacardColumn(opts=self._opts,
                                              label=dg.label,
                                              landsProcess=dg.landsProcess,
                                              enabledForMassPoints = dg.validMassPoints,
                                              datasetType = dg.datasetType,
                                              nuisanceIds = dg.nuisances[:],
                                              datasetMgrColumn = dg.datasetDefinition,
                                              additionalNormalisationFactor = dg.additionalNormalisation,
                                              shapeHistoName = dg.shapeHistoName,
                                              histoPath = dg.histoPath)
                else: # i.e. signal analysis and QCD factorised / inverted
                    myColumn = DatacardColumn.DatacardColumn(opts=self._opts,
                                              label=dg.label,
                                              landsProcess=dg.landsProcess,
                                              enabledForMassPoints = dg.validMassPoints,
                                              datasetType = dg.datasetType,
                                              nuisanceIds = dg.nuisances[:],
                                              datasetMgrColumn = dg.datasetDefinition,
                                              additionalNormalisationFactor = dg.additionalNormalisation,
                                              shapeHistoName = dg.shapeHistoName,
                                              histoPath = dg.histoPath) 
                # Store column
                self._columns.append(myColumn)
                # Provide debug print
                if self._opts.debugConfig:
                    myColumn.printDebug()

        # Cache main counter tables
        self._dsetMgrManager.cacheMainCounterTables()
        if self.verbose:
            print "Data groups converted to datacard columns"

        if self._opts.debugDatasets:
            self._dsetMgrManager.printDatasetMgrContents()
        return
    
    def _getDsetMgrIndexForColumnType(self, c):

        # Is this data-driven?
        if hasattr(self._config, 'OptionGenuineTauBackgroundSource'):
            isDataDriven = (self._config.OptionGenuineTauBackgroundSource == "DataDriven")
        if hasattr(self._config, 'OptionFakeBMeasurementSource'):
            isDataDriven = (self._config.OptionFakeBMeasurementSource == "DataDriven")

        # Determine the dataset manager index (manager index is simple bad coding! replace sometime in future)
        dsetMgrIndex = -1
        if c.typeIsObservation() or c.typeIsSignal() or c.typeIsEWKfake() or c.typeIsQCDMC() or (c.typeIsEWK() and not isDataDriven):
            dsetMgrIndex = 0
        elif c.typeIsEWK() or c.typeIsGenuineB() or c.typeIsEWKMC():
            dsetMgrIndex = 1
        elif c.typeIsQCDinverted() or c.typeIsFakeB() or c.typeIsQCDMC():
            dsetMgrIndex = 2
        else:
            msg = "Could not determine which dataset manager to use for column \"%s\"" % (c.getLabel())
            raise Exception(ShellStyles.ErrorStyle() + msg + ShellStyles.NormalStyle() )

        # Construct summary table
        align = "{:<40} {:<10} "
        table = []
        hLine = "="*50
        table.append(hLine)
        table.append(align.format("Column Type", "True/False"))
        table.append(hLine)
        table.append(align.format("Is Observation", c.typeIsObservation()) )
        table.append(align.format("Is Signal"     , c.typeIsSignal() ) )
        table.append(align.format("Is EWK Fake"   , c.typeIsEWKfake() ) )
        table.append(align.format("Is QCD MC"     , c.typeIsQCDMC() ) )
        table.append(align.format("IS EWK MC"     , c.typeIsEWKMC() ) )
        table.append(align.format("IS EWK"        , c.typeIsEWK() ) )
        table.append(align.format("Is Fake-b"     , c.typeIsFakeB() ) )
        table.append(align.format("Is Genuine-b"  , c.typeIsGenuineB() ) )
        table.append(align.format("Dset Mgr Index", dsetMgrIndex ) )
        table.append(hLine)
        table.append("")

        # For-loop: All rows in table
        for i, row in enumerate(table, 1):
            self.Verbose(row, i==1)        
        return dsetMgrIndex

    def doDataMining(self):
        '''
        Do data mining and cache the results
        '''
        self.Verbose("Starting data mining")

        if self._dsetMgrManager.getDatasetMgr(DatacardDatasetMgrSourceType.SIGNALANALYSIS) != None:
            # Handle observation separately
            myDsetMgr    = self._dsetMgrManager.getDatasetMgr(DatacardDatasetMgrSourceType.SIGNALANALYSIS)
            myLuminosity = self._dsetMgrManager.getLuminosity(DatacardDatasetMgrSourceType.SIGNALANALYSIS)

            myMainCounterTable = self._dsetMgrManager.getMainCounterTable(DatacardDatasetMgrSourceType.SIGNALANALYSIS)
            self._observation.doDataMining(self._config, myDsetMgr, myLuminosity, myMainCounterTable, self._extractors, self._controlPlotExtractors)

        # For-loop: All columns
        for i, c in enumerate(self._columns, 1):
            self.Verbose("Performing data-mining for column \"%s\"" % (c.getLabel()), i==1)

            # Determine dset manager index for the given column
            dsetMgrIndex = self._getDsetMgrIndexForColumnType(c)

            # Do mining for datacard columns (separately for data-driven bkgs)
            myDsetMgr          = self._dsetMgrManager.getDatasetMgr(dsetMgrIndex)
            myLuminosity       = self._dsetMgrManager.getLuminosity(dsetMgrIndex)
            myMainCounterTable = self._dsetMgrManager.getMainCounterTable(dsetMgrIndex)
            c.doDataMining(self._config, myDsetMgr, myLuminosity, myMainCounterTable, self._extractors, self._controlPlotExtractors)

        self.Verbose("Data mining has been finished, results (and histograms) have been ingeniously cached")
        return

    def separateMCEWKTausAndFakes(self, targetColumn, targetColumnNewName, addColumnList, subtractColumnList):
        # Obtain column for embedding
        myEmbColumn = None
        for c in self._columns:
            if c.getLabel() == targetColumn:
                myEmbColumn = c
        if myEmbColumn == None:
            raise Exception(ShellStyles.ErrorLabel()+"Could not find column with label %s!"%targetColumn)
        # Rename column and cached histograms
        print ".. renaming column '%s' -> '%s'"%(myEmbColumn.getLabel(), targetColumnNewName)
        for i in range(0,len(myEmbColumn._rateResult._histograms)):
            myEmbColumn._rateResult._histograms[i].SetTitle(myEmbColumn._rateResult._histograms[i].GetTitle().replace(myEmbColumn._label, targetColumnNewName))
            myEmbColumn._rateResult._histograms[i].SetName(myEmbColumn._rateResult._histograms[i].GetName().replace(myEmbColumn._label, targetColumnNewName))
        for j in range(0,len(myEmbColumn._nuisanceResults)):
            for i in range(0,len(myEmbColumn._nuisanceResults[j]._histograms)):
                myEmbColumn._nuisanceResults[j]._histograms[i].SetTitle(myEmbColumn._nuisanceResults[j]._histograms[i].GetTitle().replace(myEmbColumn._label, targetColumnNewName))
                myEmbColumn._nuisanceResults[j]._histograms[i].SetName(myEmbColumn._nuisanceResults[j]._histograms[i].GetName().replace(myEmbColumn._label, targetColumnNewName))
        myEmbColumn._label = targetColumnNewName
        # Add results from dataset columns with landsProcess == None
        if addColumnList == None:
            addColumnList = [None]
        # Now do the adding
        myRemoveList = []
        myNuisanceIdList = list(myEmbColumn.getNuisanceIds())
        for myid in addColumnList:
            for c in self._columns:
                if c.getLabel() == myid:
                    print ".. adding column '%s' -> '%s'"%(c.getLabel(), targetColumnNewName)
                    # Merge rate result, (ExtractorResult objects)
                    # Merge cached shape histo
                    myEmbColumn._cachedShapeRootHistogramWithUncertainties.Add(c.getCachedShapeRootHistogramWithUncertainties())
                    for n in c.getNuisanceIds():
                        if not n in myNuisanceIdList:
                            myNuisanceIdList.append(n)
                    # Merge control plots (HistoRootWithUncertainties objects)
                    for i in range(0, len(myEmbColumn._controlPlots)):
                        if myEmbColumn._controlPlots[i] != None:
                            myEmbColumn._controlPlots[i]["shape"].Add(c._controlPlots[i]["shape"])
                    # Mark for removal
                    myRemoveList.append(c)
        for c in myRemoveList:
            self._columns.remove(c)
            del c
        # Subtract results from dataset columns in EWKFakeIdList list
        for fakeId in subtractColumnList:
            for c in self._columns:
                if c.getLabel() == fakeId:
                    print ".. subtracting column '%s' from '%s'"%(c.getLabel(), targetColumnNewName)
                    # Subtract rate result, (ExtractorResult objects)
                    # Merge cached shape histo
                    myEmbColumn._cachedShapeRootHistogramWithUncertainties.Add(c.getCachedShapeRootHistogramWithUncertainties(), -1.0)
                    for n in c.getNuisanceIds():
                        if not n in myNuisanceIdList:
                            myNuisanceIdList.append(n)
                    # Merge control plots (HistoRootWithUncertainties objects)
                    for i in range(0, len(myEmbColumn._controlPlots)):
                        if myEmbColumn._controlPlots[i] != None:
                            myEmbColumn._controlPlots[i]["shape"].Add(c._controlPlots[i]["shape"], -1.0)
        print ".. finalizing merge"
        # Update rate
        myEmbColumn._rateResult._result = myEmbColumn._cachedShapeRootHistogramWithUncertainties.getRate()
        #myEmbColumn._cachedShapeRootHistogramWithUncertainties.Debug()
        myEmbColumn._rateResult._histograms[0] = aux.Clone(myEmbColumn._cachedShapeRootHistogramWithUncertainties.getRootHisto(),myEmbColumn.getLabel())
        myEmbColumn._rateResult._histograms[0].SetTitle(myEmbColumn.getLabel())
        # Update rate stat. uncert.
        for i in range(0, len(myEmbColumn.getNuisanceResults())):
            nhistos = len(myEmbColumn.getNuisanceResults()[i]._histograms)
            if nhistos > 0:
                if myEmbColumn.getNuisanceResults()[i].resultIsStatUncertainty():
                    for k in range(1, myEmbColumn._nuisanceResults[i]._histograms[0].GetNbinsX()+1):
                        myRate = myEmbColumn._rateResult._histograms[0].GetBinContent(k)
                        myRateUncert = myEmbColumn._rateResult._histograms[0].GetBinError(k)
                        if myRateUncert < self._config.ToleranceForMinimumRate:
                            myRateUncert = self._config.ToleranceForMinimumRate
                        # up histogram
                        myEmbColumn._nuisanceResults[i]._histograms[0].SetBinContent(k, myRate + myRateUncert)
                        ## down histogram
                        myEmbColumn._nuisanceResults[i]._histograms[1].SetBinContent(k, myRate - myRateUncert)
        # Update shape uncertainties
        myFoundNuisancesCount = 0
        for e in self._extractors:
            if e.getId() in myNuisanceIdList:
                myFoundNuisancesCount += 1
                # Check that all uncertainties exist in root histo with uncertainties:
                mySystVarName = e.getId()
                if e.isShapeNuisance():
                    mySystVarName = e._systVariation
                if not mySystVarName in myEmbColumn._cachedShapeRootHistogramWithUncertainties._shapeUncertainties.keys():
                    myEmbColumn._cachedShapeRootHistogramWithUncertainties.Debug()
                    raise Exception(ErrorLabel()+"Syst.uncert. '%s' not in RootHistogramWithUncertainties()!"%mySystVarName)
                # Find index for existing nuisance result (keep at None if no index is found)
                myNuisanceResultIndex = None
                for i in range(0, len(myEmbColumn.getNuisanceIds())):
                    if e.getId() == myEmbColumn.getNuisanceIds()[i]:
                        myNuisanceResultIndex = i
                myResult = None
                # Obtain plus and minus variation histograms
                (hUp, hDown) = myEmbColumn._cachedShapeRootHistogramWithUncertainties._shapeUncertainties[mySystVarName]
                if e.isShapeNuisance():
                    myModUp = aux.Clone(hUp)
                    myModUp.SetTitle("%s_%sUp"%(myEmbColumn.getLabel(),e.getMasterId()))
                    myModUp.Add(myEmbColumn._cachedShapeRootHistogramWithUncertainties.getRootHisto())
                    myModDown = aux.Clone(hDown)
                    myModDown.SetTitle("%s_%sDown"%(myEmbColumn.getLabel(),e.getMasterId()))
                    myModDown.Add(myEmbColumn._cachedShapeRootHistogramWithUncertainties.getRootHisto())
                    myResult = DatacardColumn.ExtractorResult(e.getId(),
                                                              e.getMasterId(),
                                                              0.0,
                                                              [myModUp,myModDown],
                                                              "Stat." in e.getDescription() or "stat." in e.getDescription() or e.getDistribution()=="shapeStat")
                else:
                    myUpInt = hUp.Integral()
                    myDownInt = hDown.Integral()
                    myRateInt = myEmbColumn._cachedShapeRootHistogramWithUncertainties.getRate()
                    myPlus = 0.0
                    myMinus = 0.0
                    if abs(myRateInt) > 0.000001:
                        myPlus = (myUpInt)/myRateInt
                        myMinus = (myDownInt)/myRateInt
                    myResultItem = None
                    if abs(abs(myPlus)-abs(myMinus)) < 0.0001:
                        myResultItem = ScalarUncertaintyItem(e.getId(), abs(myPlus))
                    else:
                        myResultItem = ScalarUncertaintyItem(e.getId(), plus=abs(myPlus), minus=abs(myMinus))
                    myResult = DatacardColumn.ExtractorResult(e.getId(),
                                                              e.getMasterId(),
                                                              myResultItem,
                                                              [],
                                                              "Stat." in e.getDescription() or "stat." in e.getDescription() or e.getDistribution()=="shapeStat")
                # Update result
                if myNuisanceResultIndex == None:
                    myEmbColumn._nuisanceResults.append(myResult)
                    myEmbColumn._nuisanceIds.append(e.getId())
                else:
                    for h in myEmbColumn._nuisanceResults[myNuisanceResultIndex]._histograms:
                        h.Delete()
                    myEmbColumn._nuisanceResults[myNuisanceResultIndex].delete()
                    myEmbColumn._nuisanceResults[myNuisanceResultIndex] = myResult
        if myFoundNuisancesCount != len(myNuisanceIdList):
            raise Exception("This should not happen")

    def closeFiles(self):
        '''
        Closes files in dataset managers
        '''
        self.Verbose("Closing open input files")
        #self._dsetMgrManager.closeManagers()
        self.Verbose("DatasetManagers closed")
        return

    ## Check landsProcess in datacard columns
    def checkDatacardColumns(self):
        if self._opts.combine:
            return # Disable for combine
        for m in self._config.MassPoints:
            i = 0
            myFirstValue = 0
            for c in sorted(self._columns, key=lambda x: x.getLandsProcess()):
                if (c.isActiveForMass(m,self._config)):
                    #sprint c.getLabel(), c.getLandsProcess()
                    if c.getLandsProcess() != None:
                        if i == 0:
                            myFirstValue = c.getLandsProcess()
                        else:
                            if myFirstValue + i != c.getLandsProcess():
                                print " cannot find LandS process '"+str(myFirstValue+i)+"' in data groups for mass = %d! (need to have consecutive numbers; add group with such landsProcess or check input file)"%m
                                raise Exception()
                        i += 1
                else:
                    if c.getLabel() == "res.":
                        i += 1 # Take into account that the empty column is no longer needed for sigma x Br limits

    ## Creates extractors for nuisances
    def createExtractors(self):
        # Protection to create extractors only once
        if len(self._extractors) > 0:
            return

        myMode = Extractor.ExtractorMode.NUISANCE
        for n in self._config.Nuisances:
            if self._opts.verbose:
                print "Creating extractor for nuisance by ID:",n.id
            if n.function == "Constant":
                myMode = Extractor.ExtractorMode.NUISANCE
                if n.getArg("upperValue") != None and n.getArg("upperValue") > 0:
                    myMode = Extractor.ExtractorMode.ASYMMETRICNUISANCE
                self._extractors.append(Extractor.ConstantExtractor(exid = n.id,
                                                         constantValue = n.getArg("value"),
                                                         constantUpperValue = n.getArg("upperValue"),
                                                         distribution = n.distr,
                                                         description = n.label,
                                                         mode = myMode,
                                                         opts = self._opts,
                                                         scaleFactor = n.getArg("scaleFactor")))
            elif n.function == "ConstantForQCD":
                myMode = Extractor.ExtractorMode.QCDNUISANCE
                self._extractors.append(Extractor.ConstantExtractorForDataDrivenQCD(exid = n.id,
                                                         constantValue = n.getArg("value"),
                                                         constantUpperValue = n.getArg("upperValue"),
                                                         distribution = n.distr,
                                                         description = n.label,
                                                         mode = myMode,
                                                         opts = self._opts,
                                                         scaleFactor = n.getArg("scaleFactor")))
            elif n.function == "ConstantToShape":
                self._extractors.append(Extractor.ConstantExtractor(exid = n.id,
                                                         constantValue = n.getArg("value"),
                                                         constantUpperValue = n.getArg("upperValue"),
                                                         distribution = n.distr,
                                                         description = n.label,
                                                         mode = Extractor.ExtractorMode.SHAPENUISANCE,
                                                         opts = self._opts,
                                                         scaleFactor = n.getArg("scaleFactor")))
            elif n.function == "Counter":
                self._extractors.append(Extractor.CounterExtractor(exid = n.id,
                                                        counterItem = n.getArg("counter"),
                                                        distribution = n.distr,
                                                        description = n.label,
                                                        mode = myMode,
                                                        opts = self._opts,
                                                        scaleFactor = n.getArg("scaleFactor")))
            elif n.function == "maxCounter":
                self._extractors.append(Extractor.MaxCounterExtractor(exid = n.id,
                                                           counterItem = n.getArg("counter"),
                                                           counterDirs = n.getArg("histoDir"),
                                                           distribution = n.distr,
                                                           description = n.label,
                                                           mode = myMode,
                                                           opts = self._opts,
                                                           scaleFactor = n.getArg("scaleFactor")))
            elif n.function == "pileupUncertainty":
                self._extractors.append(Extractor.PileupUncertaintyExtractor(exid = n.id,
                                                                   counterItem = n.getArg("counter"),
                                                                   counterDirs = n.getArg("histoDir"),
                                                                   distribution = n.distr,
                                                                   description = n.label,
                                                                   mode = myMode,
                                                                   opts = self._opts,
                                                                   scaleFactor = n.getArg("scaleFactor")))
            elif n.function == "Shape":
                self._extractors.append(Extractor.ShapeExtractor(exid = n.id,
                                                       distribution = n.distr,
                                                       description = n.label,
                                                       mode = Extractor.ExtractorMode.SHAPENUISANCE,
                                                       opts = self._opts,
                                                       minimumStatUncert = self._config.MinimumStatUncertainty,
                                                       minimumRate = self._config.ToleranceForMinimumRate, # Only for suppressing warn prints
                                                       scaleFactor = n.getArg("scaleFactor")))
            elif n.function == "ShapeVariation":
                self._extractors.append(Extractor.ShapeVariationExtractor(exid = n.id,
                                                                distribution = n.distr,
                                                                description = n.label,
                                                                systVariation = n.getArg("systVariation"),
                                                                mode = Extractor.ExtractorMode.SHAPENUISANCE,
                                                                opts = self._opts,
                                                                scaleFactor = n.getArg("scaleFactor")))
            elif n.function == "ShapeVariationSeparateShapeAndNormalization":
                self._extractors.append(Extractor.ShapeVariationSeparateShapeAndNormalization(exid = n.id,
                                                                distribution = n.distr,
                                                                description = n.label,
                                                                systVariation = n.getArg("systVariation"),
                                                                mode = Extractor.ExtractorMode.SHAPENUISANCE,
                                                                opts = self._opts,
                                                                scaleFactor = n.getArg("scaleFactor")))
            elif n.function == "ShapeVariationToConstant":
                self._extractors.append(Extractor.ShapeVariationToConstantExtractor(exid = n.id,
                                                                distribution = n.distr,
                                                                description = n.label,
                                                                systVariation = n.getArg("systVariation"),
                                                                mode = myMode,
                                                                opts = self._opts,
                                                                scaleFactor = n.getArg("scaleFactor")))
            elif n.function == "ShapeVariationFromJson":
                self._extractors.append(Extractor.ShapeVariationFromJsonExtractor(exid = n.id,
                                                                distribution = n.distr,
                                                                description = n.label,
                                                                jsonFile = n.getArg("jsonFile"),
                                                                mode = Extractor.ExtractorMode.SHAPENUISANCE,
                                                                opts = self._opts,
                                                                scaleFactor = n.getArg("scaleFactor")))
            elif n.function == "QCDShapeVariation":
                self._extractors.append(Extractor.QCDShapeVariationExtractor(exid = n.id,
                                                                distribution = n.distr,
                                                                description = n.label,
                                                                systVariation = n.getArg("systVariation"),
                                                                mode = Extractor.ExtractorMode.SHAPENUISANCE,
                                                                opts = self._opts))
            elif n.function == "ScaleFactor":
                self._extractors.append(Extractor.ScaleFactorExtractor(exid = n.id,
                                                            histoDirs = n.getArg("histoDir"),
                                                            histograms = n.getArg("histograms"),
                                                            normalisation = n.getArg("normalisation"),
                                                            addSystInQuadrature = n.getArg("addUncertaintyInQuadrature"),
                                                            distribution = n.distr,
                                                            description = n.label,
                                                            mode = myMode,
                                                            opts = self._opts,
                                                            scaleFactor = n.getArg("scaleFactor")))
            elif n.function == "Ratio":
                self._extractors.append(Extractor.RatioExtractor(exid = n.id,
                                                      numeratorCounterItem = n.getArg("numerator"),
                                                      denominatorCounterItem = n.getArg("denominator"),
                                                      distribution = n.distr,
                                                      description = n.label,
                                                      scale = n.getArg("scaling"),
                                                      mode = myMode,
                                                      opts = self._opts,
                                                      scaleFactor = n.getArg("scaleFactor")))
            else:
                print ShellStyles.ErrorStyle()+"Error in nuisance with id='"+n.id+"':"+ShellStyles.NormalStyle()+" unknown or missing field function '"+n.function+"' (string)!"
                print "Options are: 'Constant', 'ConstantToShape', 'Counter', 'maxCounter', 'Shape', 'ScaleFactor', 'Ratio'"
                raise Exception()
        # Create reserved nuisances
        for n in self._config.ReservedNuisances:
            self._extractors.append(Extractor.ConstantExtractor(exid = n[0], constantValue = 0.0, distribution = "lnN", description = n[1], mode = myMode))
        # Done
        if self.verbose:
            print "Created extractors for all nuisances"
        self.checkNuisances()

    def checkNuisances(self):
        # Check for duplicates
        for i in range(0,len(self._extractors)):
            for j in range(0,len(self._extractors)):
                if self._extractors[i].isId(self._extractors[j].getId()) and i != j:
                    print ShellStyles.ErrorStyle()+"Error:"+ShellStyles.NormalStyle()+" You have defined two nuisances with id='"+self._extractors[j].getId()+"'! The id has to be unique!"
                    raise Exception()
        # Merge nuisances
        self.mergeNuisances()
        # Check consecutive id's
        #myCounter = 0
        #for n in sorted(self._extractors, key=lambda x: x.getId()):
            #if n.isPrintable():
                #myCounter += 1
                #if int(n.getId()) != myCounter:
                    #print ShellStyles.WarningLabel()+"You have not declared a Nuisance or ReservedNuisance with id='%d'! (assuming consecutive numbers)"%myCounter
                    #myCounter = int(n.getId())

    def mergeNuisances(self):
        for mset in self._config.MergeNuisances:
            if self._opts.verbose:
                print "Merging nuisances:",mset,"->",mset[0]
            # check if nuisance with master id can be found
            myFoundStatus = False
            for n in self._extractors:
                if n.isId(mset[0]):
                    myFoundStatus = True
            if not myFoundStatus:
                print ShellStyles.ErrorStyle()+"Error in merging Nuisances:"+ShellStyles.NormalStyle()+" cannot find a nuisance with id '"+mset[0]+"'!"
                raise Exception()
            # assign master to slave nuisances
            for i in range(1, len(mset)):
                myFoundStatus = False
                for n in self._extractors:
                    if n.isId(mset[i]):
                        n.setAsSlave(mset[0])
                        myFoundStatus = True
                if not myFoundStatus:
                    print ShellStyles.ErrorStyle()+"Error in merging Nuisances:"+ShellStyles.NormalStyle()+" tried to merge '"+mset[i]+"' (slave) to '"+mset[0]+"' (master) but could not find a nuisance with id '"+mset[i]+"'!"
                    raise Exception()

        if self.verbose:
            print "Merged Nuisances"


    ## Creates extractors for nuisances
    def createControlPlots(self):
        # Protection to create extractors only once
        if len(self._controlPlotExtractors) > 0:
            return

        # Loop over control plot inputs, create extractors for all other columns except QCD factorised
        for c in self._config.ControlPlots:
            if self._opts.verbose:
                print "Creating control plot extractor for",c.title
            self._controlPlotExtractors.append(Extractor.ControlPlotExtractor(histoSpecs = c.details,
                                               histoTitle = c.title,
                                               histoName = c.histoName))
