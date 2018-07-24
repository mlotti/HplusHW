#!/usr/bin/env python
'''
USAGE:
addNewDatasetToPseudomulticrab.py  -m <same_pseudo_multicrab> [opts]


EXAMPLES:
addNewDatasetToPseudomulticrab.py  -m Hplus2tbAnalysis_AfterPreapproval_TopMassLE400_BDT0p40_17July2018 --newDsetName Rares


LAST USED:
addNewDatasetToPseudomulticrab.py  -m Hplus2tbAnalysis_AfterPreapproval_MVA0p40_NewTopAndBugFixAndSF_FixedStdSelections_Only2CleanTopsBeforeBDT_Syst_07Jul2018 --newDsetName Rares

'''
#================================================================================================ 
# Imports
#================================================================================================ 
import sys
import os
from optparse import OptionParser
import math
import time
import cProfile

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux
import HiggsAnalysis.NtupleAnalysis.tools.analysisModuleSelector as analysisModuleSelector
import HiggsAnalysis.NtupleAnalysis.tools.ShellStyles as ShellStyles
import HiggsAnalysis.NtupleAnalysis.tools.pseudoMultiCrabCreator as pseudoMultiCrabCreator


#================================================================================================
# Definitions
#================================================================================================
ss = ShellStyles.SuccessStyle() 
ns = ShellStyles.NormalStyle()
ts = ShellStyles.NoteStyle()
hs = ShellStyles.HighlightAltStyle()
es = ShellStyles.ErrorStyle()

#================================================================================================
# Class Definition
#================================================================================================
class NewShape:
    '''
    Container class for information of data and MC at certain point of the selection flow
    '''
    def __init__(self, dsetMgr, newDsetName, dsetsToMerge, moduleInfoString, histoName, luminosity, verbose=False):
        self._verbose          = verbose
        self._histoName        = histoName
        self._luminosity       = luminosity
        self._fullName         = histoName
        self._dsetsToMerge     = dsetsToMerge
        self._newDsetName      = newDsetName
        self._moduleInfoString = moduleInfoString
        if opts.verbose:
            self.Print("Printing dataset manager info:", True)
            dsetMgr.PrintInfo()
        self._histoList   = []
        for dsetName in self._dsetsToMerge:
            self._histoList.extend(self._getHistogramsFromSingleSource(dsetMgr, dsetName, self._fullName, luminosity))
        return

    def Print(self, msg, printHeader=False):
        fName = __file__.split("/")[-1]
        if printHeader==True:
            print "=== ", fName
            print "\t", msg
        else:
            print "\t", msg
        return

    def Verbose(self, msg, printHeader=False):
        if not self._verbose:
            return
        fName = __file__.split("/")[-1]
        self.Print(msg, printHeader)
        return

    def _getHistogramsFromSingleSource(self, dsetMgr, datasetName, histoName, luminosity):
        
        # Sanity  checks
        dsetExists = datasetName in dsetMgr.getAllDatasetNames()
        if not dsetExists:
            raise Exception("%sDataset %s does not exist%s" % (es, datasetName, ns ) )

        self.Verbose("Getting ROOT histo %s for dataset %s" % (ts + histoName + ns, ts + datasetName + ns), False)
        myDsetRootHisto = dsetMgr.getDataset(datasetName).getDatasetRootHisto(histoName)

        # If the dataset is MC set the appropriate luminosity
        if dsetMgr.getDataset(datasetName).isMC():
            self.Verbose("Setting luminosity to \"%d\" pb-1 for dataset \"%s\"" % (luminosity, datasetName), False)
            myDsetRootHisto.normalizeToLuminosity(luminosity)

        # Get histogram, rename it and set ownership
        histo   = myDsetRootHisto.getHistogram()
        newName = histoName + "_" + datasetName

        self.Verbose("Setting histogram name to \"%s\"" % (newName), False)
        histo.SetName(newName)
        ROOT.SetOwnership(histo, True)

        self.Verbose("Appending histogram \"%s\" of dataset \"%s\" to the list" % (histo.GetName(), datasetName), False)
        return [histo]
        
    def delete(self):
        '''
        Delete the histograms
        '''
        for h in self._histoList:
            if h == None:
                raise Exception()
            h.Delete()
        self._histoList  = []
        return

    def getFileFriendlyHistoName(self):
        return self._histoName.replace("/","_")

    def getHistoName(self):
        return self._histoName

    def getIntegratedEwkHisto(self):
        '''
        Return the sum of ewk integrated over the phase space splitted bins
        '''
        h = aux.Clone(self._histoList[0])
        h.SetName("_".join(h.GetName().split("_", 2)[:2]) + "_EWK_Integrated")
        for i in range(1, len(self._histoList)):
            h.Add(self._histoList[i])
        return h

    def getIntegratedNewDsetHisto(self):
        '''
        Return the sum of all datasets to be merged over the entire phase space
        '''
        newName = "%s_%s" % (self._histoName, self._newDsetName)
        histo = aux.Clone(self._histoList[0], newName)
        histo.Reset()

        # For-loop: All histograms in list
        for i, h in enumerate(self._histoList, 0):
            self.Verbose("self.histoList[%s] = %s " % (i, self._histoList[i].GetName()), True)
            histo.Add(self._histoList[i])
            self.Verbose("histo.Integral() += %.2f" %  (histo.Integral()), False)

        self.Verbose("Integral of histogram %s is %.3f (Entries = %d)" %  (histo.GetName(), histo.Integral(), histo.GetEntries()), True)
        return histo

    def getOutputHistoName(self, suffix=""):
        '''
        Returns name of histogram combined with the split bin title
        '''
        s = "%s"%(self._histoList[0].GetName().replace("/","_"))
        if len(suffix) > 0:
            s += "_%s"%suffix
        return s


#================================================================================================
# Class Definition
#================================================================================================
class ModuleBuilder:
    def __init__(self, opts, outputCreator, verbose=False):
        self._verbose                  = verbose
        self._opts                     = opts
        self._outputCreator            = outputCreator
        self._moduleInfoString         = None
        self._dsetMgrCreator           = None
        self._dsetMgr                  = None
        self._normFactors              = None
        self._luminosity               = None
        self._nominalResult            = None
        self._fakeWeightingPlusResult  = None
        self._fakeWeightingMinusResult = None
        return

    def delete(self):
        '''
        Clean up memory
        '''
        if self._nominalResult != None:
            self._nominalResult.delete()
        if self._fakeWeightingPlusResult != None:
            self._fakeWeightingPlusResult.delete()
        if self._fakeWeightingMinusResult != None:
            self._fakeWeightingMinusResult.delete()
        if self._dsetMgr != None:
            self._dsetMgr.close()
        if self._dsetMgrCreator != None:
            self._dsetMgrCreator.close()
        ROOT.gDirectory.GetList().Delete()
        ROOT.gROOT.CloseFiles()
        ROOT.gROOT.GetListOfCanvases().Delete()
        return

    def Print(self, msg, printHeader=False):
        fName = __file__.split("/")[-1].replace("pyc", "py")
        if printHeader==True:
            print "===", fName
            print "\t", msg
        else:
            print "\t", msg
        return

    def Verbose(self, msg, printHeader=True):
        if not self._verbose:
            return
        self.Print(msg, printHeader)
        return

    def createDsetMgr(self, multicrabDir, analysis, era, searchMode, optimizationMode=None, systematicVariation=None):
        
        # Store variables
        self._analysis = analysis
        self._era = era
        self._searchMode = searchMode
        self._optimizationMode = optimizationMode
        self._systematicVariation = systematicVariation

        # Construct info string of module
        self._moduleInfoString = self.getModuleInfoString()

        # Obtain dataset manager
        self._dsetMgrCreator = dataset.readFromMulticrabCfg(directory=multicrabDir)
        self._dsetMgr = self._dsetMgrCreator.createDatasetManager(dataEra=era, searchMode=searchMode,
                                                                  optimizationMode=optimizationMode,
                                                                  systematicVariation=systematicVariation)

        # Do the usual normalisation
        self._dsetMgr.updateNAllEventsToPUWeighted()
        self._dsetMgr.loadLuminosities()

        # Merge, Rename, Reorder datasets
        plots.mergeRenameReorderForDataMC(self._dsetMgr)
        
        # Print initial dataset info
        if opts.verbose:
            self._dsetMgr.PrintInfo()   

        self.Verbose("Merging datasets to get new dataset: [%s] -> %s" % (ts + ", ".join(opts.dsetsToMerge) + ns, ss + opts.newDsetName + ns), True)
        self._dsetMgr.merge(opts.newDsetName, opts.dsetsToMerge, keepSources=True)

        # Remove all other datasets
        datasetList = opts.dsetsToRemove
        self.Verbose("Removing datasets: [%s]" % (es + ", ".join(opts.dsetsToRemove) + ns), True) 
        for i, d in enumerate(datasetList, 1):
            self._dsetMgr.remove(filter(lambda name: d in name, self._dsetMgr.getAllDatasetNames()))
        
        # Print final dataset info
        if opts.verbose:
            self._dsetMgr.PrintInfo()

        # Obtain luminosity
        self._luminosity = self._dsetMgr.getDataset("Data").getLuminosity()
        return
        
    def debug(self):
        self._dsetMgr.printDatasetTree()
        self.Print("Luminosity = %f 1/fb" % (self._luminosity / 1000.0), True)
        return

    def getModuleInfoString(self):
        moduleInfo = None

        if len(self._optimizationMode) == 0:
            moduleInfo = "%s_%s_%s" % (self._analysis, self._searchMode, self._era)
        else:
            moduleInfo = "%s_%s_%s_%s" % (self._analysis, self._searchMode, self._era, self._optimizationMode)

        if self._systematicVariation != None:
            if len(self._systematicVariation) != 0:
                moduleInfo += "_%s" % (self._systematicVariation)
        return moduleInfo

    def buildModule(self, dataPath):
        
        self.Verbose("Create containers for results", True)
        myModule = pseudoMultiCrabCreator.PseudoMultiCrabModule(self._dsetMgr, self._era, self._searchMode, self._optimizationMode,
                                                                self._systematicVariation, opts.analysisNameSaveAs, opts.verbose)

        self.Verbose("Obtain results from the results manager", True)
        self._nominalResult = ResultManager(self._dsetMgr, self._luminosity, self.getModuleInfoString(), verbose=opts.verbose)

        self.Verbose("Add all plots to be written in the peudo-dataset beind created", True)
        myModule.addPlots(self._nominalResult.getPlots(), self._nominalResult.getPlotLabels())

        self.Verbose("Adding module \"%s\"" % (myModule), True)        
        self._outputCreator.addModule(myModule, altMode=True)
        return

#================================================================================================
# Function Definition
#================================================================================================
def Print(msg, printHeader=False):
    fName = __file__.split("/")[-1].replace("pyc", "py")
    if printHeader==True:
        print "===", fName
        print "\t", msg
    else:
        print "\t", msg
    return

def Verbose(msg, printHeader=True, verbose=False):
    if not opts.verbose:
        return
    Print(msg, printHeader)
    return

def getAvgProcessTimeForOneModule(myGlobalStartTime, myTotalModules):
    if myTotalModules < 1:
        return 0.0
    return (time.time()-myGlobalStartTime)/float(myTotalModules)

def getTotalElapsedTime(myGlobalStartTime):
    return (time.time()-myGlobalStartTime)

def printTimeEstimate(globalStart, localStart, nCurrent, nAll):
    myLocalTime   = time.time()
    myLocalDelta  = myLocalTime - localStart
    myGlobalDelta = myLocalTime - globalStart
    myEstimate    = myGlobalDelta / float(nCurrent) * float(nAll-nCurrent)
    
    # MAke estimate
    s = "%02d:" % (myEstimate/60)
    myEstimate -= int(myEstimate/60)*60
    s += "%02d"%(myEstimate)
    
    # Print info
    Verbose("Module finished in %.1f seconds" % (myLocalDelta), True)
    Verbose("Estimated time to complete %s" %  (s), False)
    return


def getModuleInfoString(analysis, dataEra, searchMode, optimizationMode, systematicVariation=None):
    moduleInfo = None
        
    if len(optimizationMode) == 0:
        moduleInfo = "%s_%s_%s" % (analysis, searchMode, dataEra)
    else:
        moduleInfo = "%s_%s_%s_%s" % (analysis, searchMode, dataEra, optimizationMode)
        
    if systematicVariation != None:
        if len(systematicVariation) != 0:
            moduleInfo += "_%s" % (systematicVariation)
    return moduleInfo


def getSystematicsNames(mySystematicsNamesRaw, opts):
    mySystematicsNames = []

    if len(mySystematicsNamesRaw) < 1:
        Verbose("There are 0 systematic variation sources", True)
        return mySystematicsNames

    # For-loop: All systematics raw names
    for i, item in enumerate(mySystematicsNamesRaw, 0):
        # Print("Using systematic %s" % (ShellStyles.NoteStyle() + item + ShellStyles.NormalStyle()), i==0)
        mySystematicsNames.append("%sPlus" % item)
        mySystematicsNames.append("%sMinus"% item)    

    Print("There are %d systematic variation sources:%s\n\t%s%s" % (len(mySystematicsNames), hs, "\n\t".join(mySystematicsNames), ns), True)
    return mySystematicsNames


#================================================================================================
# Class Definition
#================================================================================================
class ResultManager:
    '''
    Manager class for obtaining all the required information to be saved to a pseudo-multicrab
    '''
    def __init__(self, dsetMgr, luminosity, moduleInfoString, verbose=False):
        self._verbose      = verbose
        self._myPlots      = []
        self._myPlotLabels = []
        self._folders      = self._GetAllHistogramFolders(dsetMgr)
        self._histoPaths   = []
        for folder in self._folders:
            self._histoPaths.extend(self._GetHistoPaths(dsetMgr, "Data", folder) )
        self._histoCounters = self._GetHistoPaths(dsetMgr, "Data", "counters/weighted")
        self._moduleInfoString = moduleInfoString

        # For-Loop: All plots to consider
        nHistos = len(self._histoPaths)
        for i, plotName in enumerate(self._histoPaths, 1):

            # Ensure that histograms exist && pass other sanity checks
            sane = self._sanityChecks(dsetMgr, plotName) 

            # Inform user of progress
            msg = "{:<10} {:>3} {:^1} {:<3}: {:<20}".format("Histogram", i, "/", nHistos, plotName)
            if not sane:
                self.PrintFlushed(ss + msg + ns, False)
                continue
            else:
                self.PrintFlushed(ss + msg + ns, False)
                
            self.Verbose("Obtaining histograms to be written (the returned object is not owned)", True)
            myHisto = self._obtainHistograms(i, dsetMgr, plotName, luminosity)

        # For-Loop: All counters to consider
        nCounters = len(self._histoCounters)
        for i, cName in enumerate(self._histoCounters, 1):
            if i==1:
                print

            # Ensure that histograms exist && pass other sanity checks
            sane = self._sanityChecks(dsetMgr, cName) 

            # Inform user of progress
            msg = "{:<10} {:>3} {:^1} {:<3}: {:<20}".format("Counter", i, "/", nCounters, cName)
            if not sane:
                self.PrintFlushed(ss + msg + ns, False)
                continue
            else:
                self.PrintFlushed(ss + msg + ns, False)
                
            self.Verbose("Obtaining histograms to be written (the returned object is not owned)", True)
            myHisto = self._obtainHistograms(i, dsetMgr, cName, luminosity)
        print
        return

    def Print(self, msg, printHeader=False):
        fName = __file__.split("/")[-1].replace("pyc", "py")
        if printHeader==True:
            print "=== ", fName
            print "\t", msg
        else:
            print "\t", msg
        return

    def _GetAllHistogramFolders(self, dsetMgr):
        '''
        Get all folders containing histograms.
        Exclude some folders which do not contain any histograms
        '''
        # Get all all folders
        folders = dsetMgr.getDataset("Data").getDirectoryContent("") 

        # Exclude folders without histograms (special cases). Taken care of by pseudoMultiCrabCreator.py  
        exclude = ["counters", "config", "NSelectedVsRunNumber", "SplittedBinInfo"]

        self.Verbose("%sExcluding the following folders: %s" % (ts, ", ".join(exclude) + ns), True)
        for f in exclude:
            if f in folders:
                folders.remove(f)

        if len(folders) < 1:
            msg = "Found no folders (and hence no histograms)! This should not happen"
            raise Exception(es + msg + ns)
        else:
            self.Verbose("Found the following folders: %s" % (", ".join(folders)), True)
        return folders

    def _GetFName(self):
        fName = __file__.split("/")[-1].replace("pyc", "py")
        return fName

    def PrintFlushed(self, msg, printHeader=True):
        '''
        Useful when printing progress in a loop
        '''
        msg = "\r\t" + msg
        ERASE_LINE = '\x1b[2K'
        if printHeader:
            print "=== ", self._GetFName()
        sys.stdout.write(ERASE_LINE)
        sys.stdout.write(msg)
        sys.stdout.flush()
        return

    def Verbose(self, msg, printHeader=True):
        if not self._verbose:
            return
        self.Print(msg, printHeader)
        return

    def _GetHistoPaths(self, dsetMgr, dataset, folderPath):
        '''
        Determine list of histograms to consider (full paths)
        '''
        msg = "Obtaining all ROOT file contents for dataset %s from folder %s" % (ts + dataset + ns, ts + folderPath + ns)
        self.Verbose(msg, True)
        histoList = dsetMgr.getDataset(dataset).getDirectoryContent(folderPath)

        if histoList == None:
            raise Exception("%sDid not find any compatible object under dir \"%s\"" % (es, folderPath + ns) )
        else:
            nHistos = len(histoList)

        if nHistos == 0:
            msg = "Did not find any compatible object under dir %s" % (folderPath)
            raise Exception(es + msg + ns)

        msg = "Found %i histograms for dataset %s" % (nHistos, dataset)
        self.Verbose(ts + msg + ns, True)

        # Append folder to name
        histoPaths = []
        for hName in histoList:
            hPath = os.path.join(folderPath, hName)
            histoPaths.append(hPath)
            self.Verbose(hPath, False)
        return histoPaths

    def _sanityChecks(self, dsetMgr, histoPath):
        '''
        Check existence of histograms and ensuring they are of type
        ROOT.TH1 and not ROOT.TH2.

        Return true if all is ok
        '''
        myStatus      = True
        myFoundStatus = True

        # For-loop: All datasets
        for i, dname in enumerate(dsetMgr.getAllDatasetNames(), 1):
            d = dsetMgr.getDataset(dname)
            if not d.hasRootHisto(histoPath):
                self.Verbose("Dataset %s has no ROOT histogram % s (NOTE: \"Weighting\" folder not available in syst. variations)" % (es + dname, histoPath + ns), i==1)
                myFoundStatus = False
            else:
                self.Verbose("Dataset %s has ROOT histogram % s" % (ss + dname + ns, ss + histoPath + ns), i==1)

        # If something is wrong
        if not myFoundStatus:
            myStatus = False
            msg = "Skipping '%s', because it does not exist for all datasets!" % (histoPath)
            self.Verbose(ts + msg + ns, True)
        else:
            msg = "Histogram %s exists. Checking whether it is a ROOT.TH1 or a ROOT.TH2" % (histoPath)
            self.Verbose(ts + msg + ns, True)
            (myRootObject, myRootObjectName) = dsetMgr.getDataset(dsetMgr.getAllDatasetNames()[0]).getFirstRootHisto(histoPath)             
            
            if isinstance(myRootObject, ROOT.TH2): 
                msg ="Skipping '%s', because it is not a TH1 object" % (histoPath)
                self.Verbose(ts + msg + ns, True)
                myStatus = False
            myRootObject.Delete()
        return myStatus
    
    def _obtainHistograms(self, i, dsetMgr, plotName, luminosity):
        self.Verbose("Obtain histogram %s as \"NewShape\" type object" % (plotName), True) 
        myShape = NewShape(dsetMgr, opts.newDsetName, opts.dsetsToMerge, self._moduleInfoString, plotName, luminosity, self._verbose)
        myPlot  = myShape.getIntegratedNewDsetHisto() #myPlot = myShape.getIntegratedEwkHisto()
        if self._verbose:
            aux.PrintTH1Info(myPlot)

        self.Verbose("Cloning histogram %s, settting name and title" % (plotName), True)
        saveName = "%s_%d" % (plotName, i) 
        myPlotHisto = aux.Clone(myPlot)
        myPlotHisto.SetName(saveName)
        myPlotHisto.SetTitle(plotName)

        # Append the plot to the list. The plot title is the name the object will saved as in the ROOT file
        saveName = myPlotHisto.GetTitle()
        self.Verbose("Saving histogram %s for dataset %s" % (saveName, opts.newDsetName), i==1)
        if self._verbose:
            aux.PrintTH1Info(myPlotHisto)
        self._myPlots.append(myPlotHisto)
        self._myPlotLabels.append(saveName)

        # Delete objects from memory
        # myPlot.delete()
        myShape.delete()

        return myPlotHisto

    def delete(self):
        '''
        Delete the histograms
        '''
        def delList(l):
            for h in l:
                if h != None:
                    h.Delete()
            l = None
        delList(self._myPlots)
        self._myPlots = None
        self._myPlotLabels = None

    def getPlots(self):
        return self._myPlots
    
    def getPlotLabels(self):
        return self._myPlotLabels


def updateMulticrabCfg():
    '''
    Append new dataset to the multicrab.cfg which contains
    a list of all datasets
    '''
    fileName = "multicrab.cfg"
    filePath = os.path.join(os.getcwd(), opts.mcrab, fileName)
    dsetName = "[%s]" % opts.newDsetName

    Verbose("Opening file %s to see if dataset already exists" % (filePath), True)
    with open(filePath, 'r') as cfgFile:
        if dsetName in cfgFile.read():
            Print("Dataset %s already exists in file %s"% (ts + opts.newDsetName + ns, fileName), True)
            return
    with open(filePath, 'a') as cfgFile:
        Print("Added dataset %s to %s"% (ss + opts.newDsetName + ns, fileName), True)
        cfgFile.writelines(dsetName)
    return


#================================================================================================ 
# Main
#================================================================================================ 
def main(opts):
    
    # Object for selecting data eras, search modes, and optimization modes
    myModuleSelector = analysisModuleSelector.AnalysisModuleSelector()

    # Obtain dsetMgrCreator and register it to module selector
    dsetMgrCreator = dataset.readFromMulticrabCfg(directory=opts.mcrab)

    # Obtain systematics names
    mySystematicsNamesRaw = dsetMgrCreator.getSystematicVariationSources()
    mySystematicsNames    = getSystematicsNames(mySystematicsNamesRaw, opts)
    
    # Set the primary source 
    Verbose("Setting the primary source (label=%s)" % (ShellStyles.NoteStyle() + opts.analysisName + ShellStyles.NormalStyle()), True)
    myModuleSelector.setPrimarySource(label=opts.analysisName, dsetMgrCreator=dsetMgrCreator)

    # Select modules
    myModuleSelector.doSelect(opts=None)

    # Loop over era/searchMode/optimizationMode combos
    myTotalModules  = myModuleSelector.getSelectedCombinationCount() * (len(mySystematicsNames)+1)
    count, nEras, nSearchModes, nOptModes, nSysVars = myModuleSelector.getSelectedCombinationCountIndividually()
    if nSysVars > 0:
        msg = "Running over %d modules (%d eras x %d searchModes x %d optimizationModes x %d systematic variations)" % (count, nEras, nSearchModes, nOptModes, nSysVars)
    else:
        msg = "Running over %d modules (%d eras x %d searchModes x %d optimizationModes)" % (count, nEras, nSearchModes, nOptModes)
    Verbose(msg, True)

    # Create pseudo-multicrab creator
    msg = "Creating pseudo-dataset \"%s\" inside the pseudo-multicrab directory \"%s\"" % (opts.newDsetName, opts.mcrab)
    Verbose(msg, True)
    myOutputCreator = pseudoMultiCrabCreator.PseudoMultiCrabCreator(opts.newDsetName, opts.mcrab, verbose=opts.verbose)

    # Make time stamp for start time
    myGlobalStartTime = time.time()

    # Initialize
    myOutputCreator.initialize(subTitle="", prefix="")

    # Get lists of settings
    erasList   = myModuleSelector.getSelectedEras()
    modesList  = myModuleSelector.getSelectedSearchModes()
    optList    = myModuleSelector.getSelectedOptimizationModes()
    if 0:
        optList.append("") #append the default opt mode iff more optimization modes exist
    Verbose("Found %d eras, %d modes, %d optimisations" % (len(erasList), len(modesList), len(optList)), True)
        
    iModule = 0
    # For-loop: All eras
    for era in erasList:
        # For-loop: All searchModes
        for searchMode in modesList:
            # For-loop: AlloptimizationModes
            for optimizationMode in optList:
                Verbose("era = %s, searchMode = %s, optMode = %s" % (era, searchMode, optimizationMode), True)

                # If an optimization mode is defined in options skip the rest
                if opts.optMode != None:
                    if optimizationMode != opts.optMode:
                        continue

                # Nominal module
                myModuleInfoString = getModuleInfoString(opts.analysisName, era, searchMode, optimizationMode)
                iModule += 1

                # Inform user of what is being processes
                msg = "{:<10} {:>3} {:^1} {:<3}: {:<20}".format("Module", iModule, "/", myTotalModules, myModuleInfoString)
                Print(hs + msg + ns, iModule==1) 

                Verbose("Creating dataset manager for nominal module", True)
                myStartTime   = time.time()

                nominalModule = ModuleBuilder(opts, myOutputCreator, opts.verbose)
                nominalModule.createDsetMgr(opts.mcrab, opts.analysisName, era, searchMode, optimizationMode)
                     
                # Build the module
                nominalModule.buildModule(opts.dsetSrc)
                    
                Verbose("Deleting nominal module", True)
                nominalModule.delete()

                Verbose("Printing time estimate", True)
                printTimeEstimate(myGlobalStartTime, myStartTime, iModule, myTotalModules)

                Verbose("Now do the rest of systematics variations", True)
                for syst in mySystematicsNames:

                    myModuleInfoString = getModuleInfoString(opts.analysisName, era, searchMode, optimizationMode, syst)

                    iModule += 1
                    msg = "{:<10} {:>3} {:^1} {:<3}: {:<20}".format("Module", iModule, "/", myTotalModules, myModuleInfoString)
                    Print(hs + msg + ns, False)

                    Verbose("Creating dataset manager for systematics module %s" % (syst), True)
                    myStartTime = time.time()
                    systModule  = ModuleBuilder(opts, myOutputCreator, opts.verbose)
                    systModule.createDsetMgr(opts.mcrab, opts.analysisName, era, searchMode, optimizationMode, systematicVariation=syst)
                    
                    # Build the module
                    systModule.buildModule(opts.dsetSrc)

                    Verbose("Deleting nominal module", True)
                    systModule.delete()

                    Verbose("Printing time estimate", True)
                    printTimeEstimate(myGlobalStartTime, myStartTime, iModule, myTotalModules)

        Verbose("New dataset %s added to pseud-multicrab %s" % ( hs + opts.newDsetName + ns, hs+opts.mcrab+ns), True)
        
    # Print some timing statistics
    Verbose("Average processing time per module was %.1f seconds" % getAvgProcessTimeForOneModule(myGlobalStartTime, myTotalModules), True)
    Verbose("Total elapsed time was %.1f seconds" % getTotalElapsedTime(myGlobalStartTime), True)

    # Create rest of pseudo multicrab directory
    myOutputCreator.finalize(silent=False)

    # Update the multicrab.cfg file
    updateMulticrabCfg()
            
    return

if __name__ == "__main__":
    '''
    https://docs.python.org/3/library/argparse.html
 
    name or flags...: Either a name or a list of option strings, e.g. foo or -f, --foo.
    action..........: The basic type of action to be taken when this argument is encountered at the command line.
    nargs...........: The number of command-line arguments that should be consumed.
    const...........: A constant value required by some action and nargs selections.
    default.........: The value produced if the argument is absent from the command line.
    type............: The type to which the command-line argument should be converted.
    choices.........: A container of the allowable values for the argument.
    required........: Whether or not the command-line option may be omitted (optionals only).
    help............: A brief description of what the argument does.
    metavar.........: A name for the argument in usage messages.
    dest............: The name of the attribute to be added to the object returned by parse_args().
    '''

    # Default Settings
    global opts
    VERBOSE          = False
    ANALYSISNAME     = "Hplus2tbAnalysis"
    DSETSTOREMOVE    = ["ZJetsToQQ_HT600toInf", "Charged", "QCD", "SingleTop"]
    DSETSTOMERGE     = ["WJetsToQQ_HT_600ToInf", "DYJetsToQQHT", "TTWJetsToQQ", "TTZToQQ", "Diboson", "TTTT"]
    NEWDSETNAME      = "Rares" 
    ANALYSISNAMESAVE = "Hplus2tbAnalysis" # "ForFakeBMeasurement"
    SEARCHMODES      = ["80to1000"]
    DATAERAS         = ["Run2016"]
    OPTMODE          = None
    URL              = False
    DSETSRC          = "ForDataDrivenCtrlPlotsEWKGenuineB"
 
    # Define the available script options
    parser = OptionParser(usage="Usage: %prog [options]", add_help_option=True, conflict_handler="resolve")

    parser.add_option("-m", "--mcrab", dest="mcrab", action="store",# required=True,
                      help="Path to the multicrab directory for input [default: None]")

    parser.add_option("-o", "--optMode", dest="optMode", type="string", default=OPTMODE, 
                      help="The optimization mode when analysis variation is enabled [default: %s]" % OPTMODE)

    parser.add_option("--dsetsToMerge", dest="dsetsToMerge", default=DSETSTOMERGE,
                      help="Definition of EWK datset, i.e. datasets to be included in the merge [default: %s]" % ", ".join(DSETSTOMERGE) )
    
    parser.add_option("--analysisName", dest="analysisName", type="string", default=ANALYSISNAME,
                      help="Override default analysisName [default: %s]" % ANALYSISNAME)
    
    parser.add_option("--newDsetName", dest="newDsetName", type="string", default=NEWDSETNAME,
                      help="Override default (new) dataset name [default: %s]" % NEWDSETNAME)
    
    parser.add_option("--analysisNameSaveAs", dest="analysisNameSaveAs", type="string", default=ANALYSISNAMESAVE,
                      help="Name of folder that the new pseudo-dataset will be stored in [default: %s]" % ANALYSISNAMESAVE)

    parser.add_option("--searchMode", dest="searchMode", default=SEARCHMODES,
                      help="Override default searchMode [default: %s]" % ", ".join(SEARCHMODES) )

    parser.add_option("--dataEra", dest="era", default=DATAERAS, 
                      help="Override default dataEra [default: %s]" % ", ".join(DATAERAS) )

    parser.add_option("--dsetsToRemove", dest="dsetsToRemove", default=DSETSTOREMOVE, 
                      help="List with datasets to be removed from the dataset managaer [default: %s]" % ", ".join(DSETSTOREMOVE) )

    parser.add_option("--url", dest="url", action="store_true", default=URL, 
                      help="Don't print the actual save path the histogram is saved, but print the URL instead [default: %s]" % URL)
    
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=VERBOSE, 
                      help="Enables verbose mode (for debugging purposes) [default: %s]" % VERBOSE)

    parser.add_option("--dsetSrc", dest="dsetSrc", action="store", default=DSETSRC,
                      help="Source of datasets-to-be-mergd histograms (exampes: ForDataDrivenCtrlPlots, ForDataDrivenCtrlPlotsEWKGenuineB, ForDataDrivenCtrlPlotsEWKFakeB) [default: %s" % (DSETSRC) )

    (opts, parseArgs) = parser.parse_args()

    # Require at least two arguments (script-name, path to multicrab)
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    if opts.mcrab == None:
        Print("Not enough arguments passed to script execution. Printing docstring & EXIT.")
        parser.print_help()
        #print __doc__
        sys.exit(1)
    else:
        if not os.path.exists("%s/multicrab.cfg" % opts.mcrab):
            msg = "No pseudo-multicrab directory found at path '%s'! Please check path or specify it with --mcrab!" % (opts.mcrab)
            raise Exception(ShellStyles.ErrorLabel() + msg + ShellStyles.NormalStyle())
        else:
            msg = "Using pseudo-multicrab directory %s" % (ShellStyles.NoteStyle() + opts.mcrab + ShellStyles.NormalStyle())
            Verbose(msg , True)


    # Sanity check: At least one histogram to merge (in that case rename!)
    if len(opts.dsetsToMerge) < 1:
        msg = "List of datasets to merge is empty! At least one dataset is required!"
        raise Exception(ShellStyles.ErrorLabel() + msg + ShellStyles.NormalStyle())

    # Sanity check
    if opts.analysisName == "GenuineB":
        if "EWKGenuineB" not in opts.ewkSrc:
            msg = "Cannot create pseudo-dataset %s with EWK source set to %s" % (opts.analysisName, opts.ewkSrc)
            raise Exception(ShellStyles.ErrorLabel() + msg + ShellStyles.NormalStyle())

    if opts.analysisName == "FakeB":
        if "EWKGenuineB" not in opts.ewkSrc:
            msg = "Cannot create pseudo-dataset %s with EWK source set to %s" % (opts.analysisName, opts.ewkSrc)
            raise Exception(ShellStyles.ErrorLabel() + msg + ShellStyles.NormalStyle())
                    
    # Inform user of which datasets you consider as EWK
    msg = "Will create new dataset as follows:: [%s] -> %s" % (ts + ", ".join(opts.dsetsToMerge) + ns, ss + opts.newDsetName + ns)
    Print(msg, True)     

    # Call the main function
    main(opts)
