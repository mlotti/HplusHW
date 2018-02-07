#!/usr/bin/env python
'''
PREREQUISITES:
./run.py -m <multicrab> [opts]
./getABCD_TF.py -m <pseudo_multicrab> [opts]

Description: (* = prerequisites)
*1) Generate a pseudo-multicrab directory by running the FakeBMeasurement analyzer: (~12 hours)
   a) Go to the appropriate directory:
      cd /NtupleAnalysis/src/FakeBMeasurement/work   
   b) Edit run.py to customise running parameters. Run the analyzer with the following command:
      ./run.py -m <multicrab>
   c) Depending on whether variations are added or not this can take ~12 h without systematics (!)
   d) OUTPUT: A pseudo-multicrab dir under the work directory <pseudo_multicrab>

*2) Generate the FakeBTranserFactors.py file by running a dedicated script: (< 1m without systematics)
   a) Go to the appropriate directory:
      cd /NtupleAnalysis/src/FakeBMeasurement/work   
   b) Run the script that generates the file containing the Transfer Factor(s):
   ./getABCD_TF.py -m <pseudo_multicrab> [opts]
   c) Part b) will automatically generate this file which will contain the Transfer Factor
   for moving from the Verification Region (VR) to the Signal Region (SR).
   d) OUTPUT: The aforementioned python file will be placed inside the pseudo-multicrab directory given as input.
              
3) Calculate the final result (i.e. produce pseudo-multicrab): (30 mins. with systematics) (< 1m without systematics)
   a)./makeQCDInvertedPseudoMulticrabForDatacards.py --m <pseudo_multicrab> [opts]
   b) This takes the result directory created in step (2) and the corresponding Transfer Factor file produced in step (3)
   c) The user may calculate the final result based on the phase space binning or based on the inclusive bin
   (i.e. disable phase space binning) by using the parameter --inclusiveOnly (default option)
   d) OUTPUT: A <pseudo-dataset> dir is created inside the <pseudo_multicrab> which is the Data-Driven dataset. 
   For example, the ROOT files are currently (Jan 2018) placedunder a directory named FakeBMeasurement. A
   multicrab.cfg will also be placed there with the pseudo-dataset name.

4) Make data-driven control plots: (<1m )
The <pseudo_dataset> dir created in step 3) can be copied in a signal-analysis <pseudo-multicrab> directory and can then be used 
to REPLACE the "QCD MC" dataset in the plots. See NtupleAnalysis/src/Hplus2tbAnalysis/work/plotDataDriven.py for an example script.
This script takes TWO pseudomulticrabs as input:
   a) A Hplus2tbAnalysis pseudo-multicrab directory with all analysis cuts
   b) A FakeBMeasurement pseudo-multicrab directory which has gone throught steps 1-3


USAGE:
./makePseudoMulticrab.py -m <same_pseudo_multicrab> [opts]


EXAMPLES:
1) Produces QCD normalization factors by running the fitting script:
./getABCD_TF.py -m FakeBMeasurement_NewLeptonVeto_PreSel_3bjets40_SigSel_MVA0p85_InvSel_EE2CSVM_MVA0p60to085_180125_123834 --ratio

2) Then either run on all modules (eras, search-modes, optimization modes) automatically
./makePseudoMulticrab.py -m FakeBMeasurement_NewLeptonVeto_PreSel_3bjets40_SigSel_MVA0p85_InvSel_EE2CSVM_MVA0p60to085_180125_123834/

* Can use the counters to debug; study if the histograms are correct!
hplusPrintCounters.py --mainCounterOnly --weighted --dataEra "Run2016" --mergeForDataMC --mergeData --mergeMC FakeBMeasurement_PreSel_3bjets40_SigSel_MVA0p85_InvSel_EE2CSVM_MVA0p60to085_180120_092605


3) Plot the data-driven histograms
./plotDataDriven.py -m Hplus2tbAnalysis_NewLeptonVeto_PreSel_3bjets40_SigSel_MVA0p85_180125_123633 -n FakeBMeasurement_NewLeptonVeto_PreSel_3bjets40_SigSel_MVA0p85_InvSel_EE2CSVM_MVA0p60to085_180125_123834/FakeBMeasurement/ --gridX --gridY --logY --signal 500 --url


LAST USED:
./makePseudoMulticrab.py -m FakeBMeasurement_NewLeptonVeto_PreSel_3bjets40_SigSel_MVA0p85_InvSel_EE2CSVM_MVA0p60to085_180125_123834/

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
import HiggsAnalysis.NtupleAnalysis.tools.analysisModuleSelector as analysisModuleSelector
import HiggsAnalysis.FakeBMeasurement.QCDInvertedResult as qcdInvertedResult
import HiggsAnalysis.NtupleAnalysis.tools.ShellStyles as ShellStyles
import HiggsAnalysis.NtupleAnalysis.tools.pseudoMultiCrabCreator as pseudoMultiCrabCreator

#================================================================================================ 
# Class definition
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

    def createDsetMgr(self, multicrabDir, era, searchMode, optimizationMode=None, systematicVariation=None):
        self._era = era
        self._searchMode = searchMode
        self._optimizationMode = optimizationMode
        self._systematicVariation = systematicVariation

        # Construct info string of module
        self._moduleInfoString = self.getModuleInfoString()

        # Obtain dataset manager
        self._dsetMgrCreator = dataset.readFromMulticrabCfg(directory=multicrabDir)
        self._dsetMgr = self._dsetMgrCreator.createDatasetManager(dataEra=era, 
                                                                  searchMode=searchMode,
                                                                  optimizationMode=optimizationMode,
                                                                  systematicVariation=systematicVariation)

        # Do the usual normalisation
        self._dsetMgr.updateNAllEventsToPUWeighted()
        self._dsetMgr.loadLuminosities()
        plots.mergeRenameReorderForDataMC(self._dsetMgr)
        
        # Print initial dataset info
        if opts.verbose:
            self._dsetMgr.PrintInfo()   
        self._dsetMgr.merge("EWK", opts.ewkDatasets)

        # Remove all other datasets
        datasetList = ["ZJetsToQQ_HT600toInf", "Charged", "QCD"]
        for d in datasetList:
            self._dsetMgr.remove(filter(lambda name: d in name, self._dsetMgr.getAllDatasetNames()))
        
        # Print final dataset info
        self._dsetMgr.PrintInfo()


        # Obtain luminosity
        self._luminosity = self._dsetMgr.getDataset("Data").getLuminosity()
        return
        
    def debug(self):
        self._dsetMgr.printDatasetTree()
        print "Luminosity = %f 1/fb"%(self._luminosity / 1000.0)
        return

    def getModuleInfoString(self):
        if len(self._optimizationMode) == 0:
            moduleInfo = "%s_%s" % (self._era, self._searchMode)
        else:
            moduleInfo = "%s_%s_%s" % (self._era, self._searchMode, self._optimizationMode)
        return moduleInfo

    def buildModule(self, dataPath, ewkPath, normFactors, calculateQCDNormalizationSyst, normDataSrc=None, normEWKSrc=None):
        
        # Create containers for results
        self.Verbose("Create containers for results", True)
        myModule = pseudoMultiCrabCreator.PseudoMultiCrabModule(self._dsetMgr,
                                                                self._era,
                                                                self._searchMode,
                                                                self._optimizationMode,
                                                                self._systematicVariation, 
                                                                opts.analysisNameSaveAs,
                                                                opts.verbose)

        self.Verbose("Obtain results from the results manager", True)
        self._nominalResult = qcdInvertedResult.QCDInvertedResultManager(dataPath,
                                                                         ewkPath,
                                                                         self._dsetMgr,
                                                                         self._luminosity,
                                                                         self.getModuleInfoString(),
                                                                         normFactors,
                                                                         calculateQCDNormalizationSyst,
                                                                         opts.normDataSrc,
                                                                         opts.normEwkSrc,
                                                                         self._opts.useInclusiveNorm,
                                                                         # keyList = ["Inverted", "AllSelections"], #FIXME:  works with "ForFakeBMeasurement" folder
                                                                         keyList = ["AllSelections"],
                                                                         verbose=opts.verbose)

        self.Verbose("Add all plots to be written in the peudo-dataset beind created", True)
        myModule.addPlots(self._nominalResult.getShapePlots(), self._nominalResult.getShapePlotLabels()) 
        self._outputCreator.addModule(myModule)
        return

    def buildQCDNormalizationSystModule(self, dataPath, ewkPath):
        '''
        Up variation of QCD normalization (i.e. ctrl->signal region transition)
        Note that only the source histograms for the shape uncert are stored
        because the result must be calculated after rebinning
        (and rebinning is no longer done here for flexibility reasons)
        '''
        mySystModule = pseudoMultiCrabCreator.PseudoMultiCrabModule(self._dsetMgr,
                                                                    self._era,
                                                                    self._searchMode,
                                                                    self._optimizationMode,
                                                                    "SystVarQCDNormSource")
        mySystModule.addPlots(self._nominalResult.getQCDNormalizationSystPlots(),
                              self._nominalResult.getQCDNormalizationSystPlotLabels())
        self._outputCreator.addModule(mySystModule)

    def buildQCDQuarkGluonWeightingSystModule(self, dataPath, ewkPath, normFactorsUp, normFactorsDown, normalizationPoint):
        # Up variation of fake weighting
        mySystModulePlus = pseudoMultiCrabCreator.PseudoMultiCrabModule(self._dsetMgr,
                                                                        self._era,
                                                                        self._searchMode,
                                                                        self._optimizationMode,
                                                                        "SystVarFakeWeightingPlus")
        self._fakeWeightingPlusResult = qcdInvertedResult.QCDInvertedResultManager(dataPath, 
                                                                                   ewkPath,
                                                                                   self._dsetMgr,
                                                                                   self._luminosity,
                                                                                   self.getModuleInfoString(),
                                                                                   normFactorsUp,
                                                                                   optionCalculateQCDNormalizationSyst=False,
                                                                                   optionUseInclusiveNorm=self._opts.useInclusiveNorm)
        myModule.addPlots(self._fakeWeightingPlusResult.getShapePlots(),
                          self._fakeWeightingPlusResult.getShapePlotLabels())
        self._outputCreator.addModule(mySystModulePlus)
        # Down variation of fake weighting
        mySystModuleMinus = pseudoMultiCrabCreator.PseudoMultiCrabModule(dself._dsetMgr,
                                                                         self._era,
                                                                         self._searchMode,
                                                                         self._optimizationMode,
                                                                         "SystVarFakeWeightingMinus")
        self._fakeWeightingMinusResult = qcdInvertedResult.QCDInvertedResultManager(dataPath, 
                                                                                    ewkPath,
                                                                                    self._dsetMgr,
                                                                                    self._myLuminosity,
                                                                                    self.getModuleInfoString(),
                                                                                    normFactorsDown,
                                                                                    optionCalculateQCDNormalizationSyst=False)
        myModule.addPlots(self._fakeWeightingMinusResult.getShapePlots(),
                          self._fakeWeightingMinusResult.getShapePlotLabels())
        self._outputCreator.addModule(mySystModuleMinus)
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
    Print("Module finished in %.1f seconds" % (myLocalDelta), True)
    Print("Estimated time to complete %s" %  (s), False)
    return


def getModuleInfoString(dataEra, searchMode, optimizationMode):
    moduleInfoString = "%s_%s" % (dataEra, searchMode)
    if len(optimizationMode) > 0:
        moduleInfoString += "_%s" % (optimizationMode)
    return moduleInfoString


def getGetNormFactorsSrcFilename(dirName, fileName):
    src = os.path.join(dirName, fileName)
    if not os.path.exists(src):
        msg = "Normalisation factors ('%s') not found!\nRun script \"plotQCD_Fit.py\" to auto-generate the normalization factors python file." % src
        raise Exception(ShellStyles.ErrorLabel() + msg)
    else:
        Verbose("Found src file for normalization factors:\n\t%s" % (src), True)
    return src

def getNormFactorFileList(dirName, fileBaseName):
    scriptList = []

    # For-loop: All items (files/dir) in directory
    for item in os.listdir(dirName):
        fullPath =  os.path.join(dirName, item)

        # Skip directories
        if os.path.isdir(fullPath):
            continue

        # Find files matching the script "Base" name (without moduleInfoStrings)
        if item.startswith((fileBaseName).replace("%s.py", "")):
            if item.endswith(".py"):
                scriptList.append(item)

    if len(scriptList) < 1:
        msg = "ERROR! Found no normalization info files under dir %s. Did you generate them?" % dirName
        raise Exception(ShellStyles.ErrorStyle() + msg + ShellStyles.NormalStyle() )
    else:
        msg = "Found %s norm-factor file(s):\n\t%s" % (  len(scriptList), "\n\t".join(os.path.join([os.path.join(dirName, s) for s in scriptList])))
        Verbose(ShellStyles.NoteLabel() + msg, True)
    return scriptList


def importNormFactors(era, searchMode, optimizationMode, multicrabDirName):
    '''
    Imports the auto-generates  FakeBTranserFactors.py file, which is 
    created by the plotting/fitting templates script  (plotQCD_Fit.py)
    
    This containsthe results  of fitting to the Baseline Data the templates m_{jjb} 
    shapes from the QCD (Inverted Data) and EWK (Baseline MC).
 
    Results include the fit details for each shape and the QCD NormFactor for moving 
    from the ControlRegion (CR) to the Signal Region (SR).
    
    The aforementioned python file and a folder with the histogram ROOT files and the individual
    fits. The foler name will be normalisationPlots/<OptsMode> and will be placed inside the
    <pseudomulticrab_dir>. The autogenerated file file be place in the cwd (i.e. work/)
    '''
    # Find candidates for normalisation scripts
    scriptList = getNormFactorFileList(dirName=multicrabDirName, fileBaseName=opts.normFactorsSrc)

    # Create a string with the module information used
    moduleInfoString = getModuleInfoString(era, searchMode, optimizationMode)

    # Construct source file name
    src = getGetNormFactorsSrcFilename(multicrabDirName, opts.normFactorsSrc % moduleInfoString)

    # Check if normalization coefficients are suitable for the choses era
    Verbose("Reading normalisation factors from:\n\t%s" % src, True)

    # Split the path to get just the file name of src
    pathList = src.replace(".py","").split("/")

    # Insert the directory where the normFactor files reside into the path so that they are found
    if len(pathList) > 1:
        cwd = os.getenv("PWD")
        # Get directories to src in a list [i.e. remove the last entry (file-name) from the pathList]
        dirList = map(str, pathList[:(len(pathList)-1)])
        srcDir   = "/".join(dirList)
        sys.path.insert(0, os.path.join(cwd, srcDir))

    # Import the (normFactor) src file
    Print("Importing the transfer factors from src file %s" % (ShellStyles.NoteStyle() + src + ShellStyles.NormalStyle()), True)
    srcBase = os.path.basename("/".join(pathList))
    normFactorsImport = __import__(srcBase)
    
    # Get the function definition
    myNormFactorsSafetyCheck = getattr(normFactorsImport, "QCDInvertedNormalizationSafetyCheck") #FIXME - What does this do?
    
    Verbose("Check that the era=%s, searchMode=%s, optimizationMode=%s info matches!" % (era, searchMode, optimizationMode) )
    myNormFactorsSafetyCheck(era, searchMode, optimizationMode)

    # Obtain normalization factors
    myNormFactorsImport = getattr(normFactorsImport, "QCDNormalization")
    msg = "Disabled NormFactors SystVar Fake Weighting Up/Down"
    Print(ShellStyles.WarningLabel() + msg, True)    
    # myNormFactorsImportSystVarFakeWeightingDown = getattr(normFactorsImport, "QCDPlusEWKFakeTausNormalizationSystFakeWeightingVarDown") #FIXME
    # myNormFactorsImportSystVarFakeWeightingUp   = getattr(normFactorsImport, "QCDPlusEWKFakeTausNormalizationSystFakeWeightingVarUp")   #FIXME

    # Import the normalisation factors and inform user
    myNormFactors = {}
    if "FakeB" in opts.analysisName:
        myNormFactors[opts.normFactorKey] = myNormFactorsImport
    elif "GenuineB" in opts.analysisName:
        myNormFactors[opts.normFactorKey] = {'Inclusive': 1.0} #fime: does the EWKGenuineB require normalisation?
    else:
        raise Exception("This should not be reached!")
    # Inform user of normalisation factos
    msg = "Obtained %s normalisation factor dictionary. The values are:" % (ShellStyles.NoteStyle() + opts.normFactorKey + ShellStyles.NormalStyle() )
    Print(msg, True)
    for i, k in  enumerate(myNormFactors[opts.normFactorKey], 1):
        keyName  = k
        keyValue = myNormFactors[opts.normFactorKey][k]
        #msg += "%s = %s" % (keyName, keyValue)
        msg = "%s = %s" % (keyName, keyValue)
        Print(msg, i==0)
        
    # Inform user of weighting up/down
    msg = "Disabled NormFactors Weighting Up/Down"
    Verbose(ShellStyles.WarningLabel() + msg, True)  #fixme
    # myNormFactors["FakeWeightingDown"] = myNormFactorsImportSystVarFakeWeightingDown # FIXME 
    # myNormFactors["FakeWeightingUp"]   = myNormFactorsImportSystVarFakeWeightingUp   # FIXME
    return myNormFactors


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
    mySystematicsNames    = []
    for i, item in enumerate(mySystematicsNamesRaw, 0):
        Print("Using systematic %s" % (ShellStyles.NoteStyle() + item + ShellStyles.NormalStyle()), i==0)
        mySystematicsNames.append("%sPlus" % item)
        mySystematicsNames.append("%sMinus"% item)
    if opts.test:
        mySystematicsNames = []
        
    # Set the primary source 
    Verbose("Setting the primary source (label=%s)" % (ShellStyles.NoteStyle() + opts.analysisName + ShellStyles.NormalStyle()), True)
    myModuleSelector.setPrimarySource(label=opts.analysisName, dsetMgrCreator=dsetMgrCreator) #fixme: what is label for?

    # Select modules
    myModuleSelector.doSelect(opts=None) #fixme: (opts=opts)

    # Loop over era/searchMode/optimizationMode combos
    myTotalModules  = myModuleSelector.getSelectedCombinationCount() * (len(mySystematicsNames)+1) * len(opts.shape)
    Verbose("Found %s modules in total" % (myTotalModules), True)

    count, nEras, nSearchModes, nOptModes, nSysVars = myModuleSelector.getSelectedCombinationCountIndividually()
    if nSysVars > 0:
        msg = "Running  over %d modules (%d eras x %d searchModes x %d optimizationModes x %d systematic variations)" % (count, nEras, nSearchModes, nOptModes, nSysVars)
    else:
        msg = "Running over %d modules (%d eras x %d searchModes x %d optimizationModes)" % (count, nEras, nSearchModes, nOptModes)
    Verbose(msg, True)

    # Create pseudo-multicrab creator
    msg = "Will create pseudo-dataset %s inside the pseudo-multicrab directory" % (ShellStyles.NoteStyle() + opts.analysisName + ShellStyles.NormalStyle())
    Verbose(msg, True)
    myOutputCreator = pseudoMultiCrabCreator.PseudoMultiCrabCreator(opts.analysisName, opts.mcrab, verbose=opts.verbose)

    # Make time stamp for start time
    myGlobalStartTime = time.time()

    iModule = 0
    # For-loop: All Shapes
    for iShape, shapeType in enumerate(opts.shape, 1):
        
        msg = "Shape %d/%d:%s %s" % (iShape, len(opts.shape), ShellStyles.NormalStyle(), shapeType)
        Print(ShellStyles.CaptionStyle() + msg, True)

        # Initialize
        myOutputCreator.initialize(subTitle=shapeType, prefix="") #fixeme: remove shapeType from sub-directory name?

        # Get lists of settings
        erasList   = myModuleSelector.getSelectedEras()
        modesList  = myModuleSelector.getSelectedSearchModes()
        optList    = myModuleSelector.getSelectedOptimizationModes()
        if 0:
            optList.append("") #append the default opt mode iff more optimization modes exist

        # For-Loop over era, searchMode, and optimizationMode options
        for era in erasList:
            for searchMode in modesList:
                for optimizationMode in optList:
                    
                    Verbose("era = %s, searchMode = %s, optMode = %s" % (era, searchMode, optimizationMode), True)
                    # If an optimization mode is defined in options skip the rest
                    if opts.optMode != None:
                        if optimizationMode != opts.optMode:
                            continue

                    # Obtain normalization factors
                    myNormFactors = importNormFactors(era, searchMode, optimizationMode, opts.mcrab)

                    # Nominal module
                    myModuleInfoString = getModuleInfoString(era, searchMode, optimizationMode)
                    iModule += 1

                    # Inform user of what is being processes
                    msg = "Module %d/%d:%s %s/%s" % (iModule, myTotalModules, ShellStyles.NormalStyle(), myModuleInfoString, shapeType)
                    Print(ShellStyles.CaptionStyle() + msg, True)

                    # Keep time
                    myStartTime = time.time()

                    Verbose("Create dataset manager with given settings", True)
                    nominalModule = ModuleBuilder(opts, myOutputCreator, opts.verbose)
                    nominalModule.createDsetMgr(opts.mcrab, era, searchMode, optimizationMode)
                    
                    if (iModule == 1):
                        if opts.verbose:
                            nominalModule.debug()
                     
                    doQCDNormalizationSyst=False #FIXME
                    if not doQCDNormalizationSyst:
                        msg = "Disabling systematics"
                        Verbose(ShellStyles.WarningLabel() + msg, True) #fixme
                        
                    # Build the module
                    nominalModule.buildModule(opts.dataSrc, opts.ewkSrc, myNormFactors[opts.normFactorKey], doQCDNormalizationSyst, opts.normDataSrc, opts.normEwkSrc)

                    if len(mySystematicsNames) > 0:
                        Print("Adding QCD normalization systematics (iff also other systematics  present) ", True)
                        nominalModule.buildQCDNormalizationSystModule(opts.dataSrc, opts.ewkSrc)

                    # FIXME: add quark gluon weighting systematics!
                    if 0: 
                        Print("Adding Quark/Gluon weighting systematics", True)
                        nominalModule.buildQCDQuarkGluonWeightingSystModule(opts.dataSrc,
                                                                            opts.ewkSrc,
                                                                            myNormFactors["FakeWeightingUp"],
                                                                            myNormFactors["FakeWeightingDown"],
                                                                            False,
                                                                            opts.normDataSrc,
                                                                            opts.normEwkSrc)

                    Verbose("Deleting nominal module", True)
                    nominalModule.delete()

                    Verbose("Printing time estimate", True)
                    printTimeEstimate(myGlobalStartTime, myStartTime, iModule, myTotalModules)

                    Verbose("Now do the rest of systematics variations", True)
                    for syst in mySystematicsNames:
                        iModule += 1
                        msg = "Analyzing systematics variations %d/%d: %s/%s/%s" % (iModule, myTotalModules, myModuleInfoString, syst, shapeType)
                        Print(ShellStyles.CaptionStyle() + msg + ShellStyles.NormalStyle(), True)
                        myStartTime = time.time()
                        systModule  = ModuleBuilder(opts, myOutputCreator)
                        # Create dataset manager with given settings
                        systModule.createDsetMgr(opts.mcrab, era, searchMode, optimizationMode, systematicVariation=syst)

                        # Build asystematics module
                        systModule.buildModule(opts.dataSrc, opts.ewkSrc, myNormFactors[opts.normFactorKey], False, opts.normDataSrc, opts.normEwkSrc)
                        printTimeEstimate(myGlobalStartTime, myStartTime, iModule, myTotalModules)
                        systModule.delete()

        Verbose("Pseudo-multicrab ready for %s" % shapeType, True)
    
    # Print some timing statistics
    Print("Average processing time per module was %.1f seconds" % getAvgProcessTimeForOneModule(myGlobalStartTime, myTotalModules), True)
    Print("Total elapsed time was %.1f seconds" % getTotalElapsedTime(myGlobalStartTime), False)

    # Create rest of pseudo multicrab directory
    myOutputCreator.finalize(silent=False)

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
    ANALYSISNAME     = "FakeBMeasurement"
    ANALYSISNAMESAVE = "Hplus2tbAnalysis"
    EWKDATASETS      = ["TT", "WJetsToQQ_HT_600ToInf", "DYJetsToQQHT", "SingleTop", "TTWJetsToQQ", "TTZToQQ", "Diboson", "TTTT"] #ZJetsToQQ_HT600toInf or DYJetsToQQHT ?
    SEARCHMODES      = ["80to1000"]
    DATAERAS         = ["Run2016"]
    OPTMODE          = None
    BATCHMODE        = True
    PRECISION        = 3
    INTLUMI          = -1.0
    SUBCOUNTERS      = False
    LATEX            = False
    MCONLY           = False
    URL              = False
    NOERROR          = True
    SAVEDIR          = "/publicweb/a/aattikis/FakeBMeasurement/"
    VERBOSE          = False
    VARIATIONS       = False
    TEST             = True
    FACTOR_SRC       = "FakeBTransferFactors_%s.py"
    DATA_SRC         = "ForDataDrivenCtrlPlots" #"ForFakeBMeasurement"
    EWK_SRC          = DATA_SRC + "EWKGenuineB" # FakeB = Data - EWK GenuineB
    NORM_DATA_SRC    = DATA_SRC + "EWKGenuineB" 
    NORM_EWK_SRC     = DATA_SRC + "EWKGenuineB"
    INCLUSIVE_ONLY   = True
    MULTICRAB        = None
    SHAPE            = ["TrijetMass"]
    NORMFACTOR_KEY   = "nominal"
 
    # Define the available script options
    parser = OptionParser(usage="Usage: %prog [options]", add_help_option=True, conflict_handler="resolve")

    parser.add_option("-m", "--mcrab", dest="mcrab", action="store",# required=True,
                      help="Path to the multicrab directory for input [default: %s]" % (MULTICRAB) )

    parser.add_option("--normFactorKey", dest="normFactorKey", default=NORMFACTOR_KEY, 
                      help="The normalisation factor key (e.g. nominal) [default: %s]" % (NORMFACTOR_KEY) )

    parser.add_option("--inclusiveOnly", dest="useInclusiveNorm", action="store_true", default=INCLUSIVE_ONLY, 
                      help="Use only inclusive weight instead of binning [default: %s]" % (INCLUSIVE_ONLY) )
    
    parser.add_option("--normFactorsSrc", dest="normFactorsSrc", action="store", default=FACTOR_SRC,
                      help="The python file (auto-generated) containing the normalisation factors. [default: %s]" % FACTOR_SRC)

    parser.add_option("-l", "--list", dest="listVariations", action="store_true", default=VARIATIONS, 
                      help="Print a list of available variations [default: %s]" % VARIATIONS)

    parser.add_option("--shape", dest="shape", action="store", default=SHAPE, 
                      help="Shape identifiers") # unknown use

    parser.add_option("--test", dest="test", action="store_true", default=TEST, 
                      help="Make short test by limiting number of syst. variations [default: %s]" % TEST)

    parser.add_option("-o", "--optMode", dest="optMode", type="string", default=OPTMODE, 
                      help="The optimization mode when analysis variation is enabled [default: %s]" % OPTMODE)

    parser.add_option("-b", "--batchMode", dest="batchMode", action="store_false", default=BATCHMODE, 
                      help="Enables batch mode (canvas creation does NOT generate a window) [default: %s]" % BATCHMODE)

    parser.add_option("--ewkDatasets", dest="ewkDatasets", default=EWKDATASETS,
                      help="Definition of EWK datset, i.e. datasets to be included in the merge [default: %s]" % ", ".join(EWKDATASETS) )
    
    parser.add_option("--analysisName", dest="analysisName", type="string", default=ANALYSISNAME,
                      help="Override default analysisName [default: %s]" % ANALYSISNAME)
    
    parser.add_option("--analysisNameSaveAs", dest="analysisNameSaveAs", type="string", default=ANALYSISNAMESAVE,
                      help="Name of folder that the new pseudo-dataset will be stored in [default: %s]" % ANALYSISNAMESAVE)

    parser.add_option("--mcOnly", dest="mcOnly", action="store_true", default=MCONLY,
                      help="Plot only MC info [default: %s]" % MCONLY)

    parser.add_option("--intLumi", dest="intLumi", type=float, default=INTLUMI,
                      help="Override the integrated lumi [default: %s]" % INTLUMI)

    parser.add_option("--searchMode", dest="searchMode", default=SEARCHMODES,
                      help="Override default searchMode [default: %s]" % ", ".join(SEARCHMODES) )

    parser.add_option("--dataEra", dest="era", default=DATAERAS, 
                      help="Override default dataEra [default: %s]" % ", ".join(DATAERAS) )

    parser.add_option("--saveDir", dest="saveDir", type="string", default=SAVEDIR, 
                      help="Directory where all pltos will be saved [default: %s]" % SAVEDIR)

    parser.add_option("--url", dest="url", action="store_true", default=URL, 
                      help="Don't print the actual save path the histogram is saved, but print the URL instead [default: %s]" % URL)
    
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=VERBOSE, 
                      help="Enables verbose mode (for debugging purposes) [default: %s]" % VERBOSE)

    parser.add_option("-i", "--includeOnlyTasks", dest="includeOnlyTasks", action="store", 
                      help="List of datasets in mcrab to include")

    parser.add_option("-e", "--excludeTasks", dest="excludeTasks", action="store", 
                      help="List of datasets in mcrab to exclude")

    parser.add_option("--dataSrc", dest="dataSrc", action="store", default=DATA_SRC,
                      help="Source of Data histograms [default: %s" % (DATA_SRC) )

    parser.add_option("--ewkSrc", dest="ewkSrc", action="store", default=EWK_SRC,
                      help="Source of EWK histograms [default: %s" % (EWK_SRC) )

    parser.add_option("--normDataSrc", dest="normDataSrc", action="store", default=NORM_DATA_SRC,
                      help="Source of Data normalisation [default: %s" % (NORM_DATA_SRC) )
                      
    parser.add_option("--normEwkSrc", dest="normEwkSrc", action="store", default=NORM_EWK_SRC,
                      help="Source of EWK normalisation [default: %s" % (NORM_EWK_SRC) )
                      
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
            Print(msg , True)

    # Sanity check - iro - fixme -alex
    if len(opts.shape) == 0:
        msg = "Provide a shape identifier with --shape (e.g.: TrijetMass)!"
        raise Exception(ShellStyles.ErrorLabel() + msg + ShellStyles.NormalStyle())

    if opts.useInclusiveNorm:
        msg = "Will only use " + ShellStyles.NoteStyle() + " inclusive " + ShellStyles.NormalStyle() + " weight instead of binning (no splitted histograms)"
        Print(msg, True)
            
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
    msg = "The following datasets will comprise the %sEWK merged-dataset%s:"  % (ShellStyles.NoteStyle(), ShellStyles.NormalStyle())
    Print(msg, True)     
    for d in opts.ewkDatasets:
        Print(d, False)

    # Call the main function
    main(opts)

    if not opts.batchMode:
        raw_input("=== makePseudoMulticrab.py: Press any key to quit ROOT ...")
