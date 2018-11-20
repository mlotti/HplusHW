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
import HiggsAnalysis.FakeBMeasurement.FakeBResult as fakeBResult
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
        if opts.verbose:
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
        self._nominalResult = fakeBResult.FakeBResultManager(dataPath,
                                                             ewkPath,
                                                             self._dsetMgr,
                                                             self._luminosity,
                                                             self.getModuleInfoString(),
                                                             normFactors,
                                                             calculateQCDNormalizationSyst,
                                                             opts.normDataSrc,
                                                             opts.normEwkSrc,
                                                             self._opts.useInclusiveNorm,
                                                             keyList = ["AllSelections"],
                                                             verbose=opts.verbose)

        self.Verbose("Add all plots to be written in the peudo-dataset beind created", True)
        myModule.addPlots(self._nominalResult.getShapePlots(), self._nominalResult.getShapePlotLabels()) 
        self._outputCreator.addModule(myModule)
        return

    def buildTransferFactorVarSystModule(self, dataPath, ewkPath, normFactors):#Up, normFactorsDown):
        '''
        This function re-calculates all histograms as normal and stores them into 
        folders with extensions:
        "Hplus2tbAnalysis_<opts.searchMode>_<opts.era>_SystVarTransferFactorUp"
        "Hplus2tbAnalysis_<opts.searchMode>_<opts.era>_SystVarTransferFactorDown"
        The difference is that instead of using the nominal Transfer Factors (TF) 
        for a given FakeB measurement bin (e.g. ldg b-jet eta) it does it using 
        an up/down variation of it:
        TF_Up   = TF + Error
        TF_Down = TF - Error
        where the error values and errors of the TFs are calculated in FakeBNormalization.py 
        using the CalculateTransferFactor() method of FakeBNormalizationManager class object.

        The error in this case is calculated by using error propagation:
        TF = CR1/CR2
        TF_Error = ErrorPropagationForDivision(TF) = sqrt((sigmaA/b)**2 + (a/(b**2)*sigmaB)**2)
        where:
        A = Integral of CR1 histogram  (from ROOT)
        sigmaA = Integral Error for CR1 histogram (from ROOT)
        '''
        # Up variation of Transfer Factors
        print
        #Print(ShellStyles.HighlightAltStyle() + "TF+Error Variation" + ShellStyles.NormalStyle() , True)
        Print(ShellStyles.HighlightAltStyle() + "Extra Module: SystVarTransferFactorPlus" + ShellStyles.NormalStyle(), False)
        mySystModulePlus = pseudoMultiCrabCreator.PseudoMultiCrabModule(self._dsetMgr, 
                                                                        self._era, 
                                                                        self._searchMode,
                                                                        self._optimizationMode, 
                                                                        "SystVarTransferFactorUp", #self._systematicVariation
                                                                        opts.analysisNameSaveAs, 
                                                                        opts.verbose)

        self._transferFactorPlusResult = fakeBResult.FakeBResultManager(dataPath, 
                                                                        ewkPath,
                                                                        self._dsetMgr,
                                                                        self._luminosity,
                                                                        self.getModuleInfoString(),
                                                                        normFactors["SystVarUp"], 
                                                                        optionDoFakeBNormalisationSyst=False,
                                                                        optionUseInclusiveNorm=self._opts.useInclusiveNorm,
                                                                        keyList = ["AllSelections"],
                                                                        verbose=opts.verbose)

        # Up variation of Transfer Factors (3x)
        print
        Print(ShellStyles.HighlightAltStyle() + "Extra Module: SystVarTransferFactor3xPlus" + ShellStyles.NormalStyle(), False)
        mySystModule3xPlus = pseudoMultiCrabCreator.PseudoMultiCrabModule(self._dsetMgr, 
                                                                          self._era, 
                                                                          self._searchMode,
                                                                          self._optimizationMode, 
                                                                          "SystVarTransferFactor3xUp", #self._systematicVariation
                                                                          opts.analysisNameSaveAs, 
                                                                          opts.verbose)
        
        # Create new list with TF + 3xError
        self._transferFactorPlusResult3x = fakeBResult.FakeBResultManager(dataPath, 
                                                                          ewkPath,
                                                                          self._dsetMgr,
                                                                          self._luminosity,
                                                                          self.getModuleInfoString(),
                                                                          normFactors["SystVar3xUp"],
                                                                          optionDoFakeBNormalisationSyst=False,
                                                                          optionUseInclusiveNorm=self._opts.useInclusiveNorm,
                                                                          keyList = ["AllSelections"],
                                                                          verbose=opts.verbose)
        
        # Add the plots
        mySystModulePlus.addPlots(self._transferFactorPlusResult.getShapePlots(), self._transferFactorPlusResult.getShapePlotLabels())
        mySystModule3xPlus.addPlots(self._transferFactorPlusResult3x.getShapePlots(), self._transferFactorPlusResult3x.getShapePlotLabels())

        # Save "_SystVarTransferFactorUp" folder to pseudo-dataset pseudo-multicrab
        self._outputCreator.addModule(mySystModulePlus)
        self._outputCreator.addModule(mySystModule3xPlus)

        # Down variation of Transfer Factors
        print
        Print(ShellStyles.HighlightAltStyle() + "Extra Module: SystVarTransferFactorMinus" + ShellStyles.NormalStyle(), False)
        mySystModuleMinus = pseudoMultiCrabCreator.PseudoMultiCrabModule(self._dsetMgr, 
                                                                         self._era, 
                                                                         self._searchMode,
                                                                         self._optimizationMode, 
                                                                         "SystVarTransferFactorDown", 
                                                                         opts.analysisNameSaveAs, 
                                                                         opts.verbose)

        self._transferFactorMinusResult = fakeBResult.FakeBResultManager(dataPath,
                                                                         ewkPath,
                                                                         self._dsetMgr, 
                                                                         self._luminosity,
                                                                         self.getModuleInfoString(), 
                                                                         normFactors["SystVarDown"],
                                                                         optionDoFakeBNormalisationSyst=False,
                                                                         optionUseInclusiveNorm=self._opts.useInclusiveNorm,
                                                                         keyList = ["AllSelections"],
                                                                         verbose=opts.verbose)
        
        # Down variation of Transfer Factors (3x)
        print
        Print(ShellStyles.HighlightAltStyle() + "Extra Module: SystVarTransferFactor3xMinus" + ShellStyles.NormalStyle(), False)
        mySystModule3xMinus = pseudoMultiCrabCreator.PseudoMultiCrabModule(self._dsetMgr, 
                                                                           self._era, 
                                                                           self._searchMode,
                                                                           self._optimizationMode, 
                                                                           "SystVarTransferFactor3xDown", 
                                                                           opts.analysisNameSaveAs, 
                                                                           opts.verbose)

        self._transferFactorMinusResult3x = fakeBResult.FakeBResultManager(dataPath,
                                                                           ewkPath,
                                                                           self._dsetMgr, 
                                                                           self._luminosity,
                                                                           self.getModuleInfoString(), 
                                                                           normFactors["SystVar3xDown"],
                                                                           optionDoFakeBNormalisationSyst=False,
                                                                           optionUseInclusiveNorm=self._opts.useInclusiveNorm,
                                                                           keyList = ["AllSelections"],
                                                                           verbose=opts.verbose)

        # Add the plots
        mySystModuleMinus.addPlots(self._transferFactorMinusResult.getShapePlots(), self._transferFactorMinusResult.getShapePlotLabels())
        mySystModule3xMinus.addPlots(self._transferFactorMinusResult3x.getShapePlots(), self._transferFactorMinusResult3x.getShapePlotLabels())

        # Save "_SystVarTransferFactorDown" folder to pseudo-dataset pseudo-multicrab
        self._outputCreator.addModule(mySystModuleMinus)
        self._outputCreator.addModule(mySystModule3xMinus)

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
    Verbose("Module finished in %.1f seconds" % (myLocalDelta), True)
    Verbose("Estimated time to complete %s" %  (s), False)
    return


def getModuleInfoString(dataEra, searchMode, optimizationMode):
    moduleInfoString = "%s_%s" % (dataEra, searchMode)
    if len(optimizationMode) > 0:
        moduleInfoString += "_%s" % (optimizationMode)
    return moduleInfoString


def getTransferFactorsSrcFilename(dirName, fileName):
    src = os.path.join(dirName, fileName)
    if not os.path.exists(src):
        msg = "Normalisation factors ('%s') not found!\nRun script \"./getABCD_TF.py\" to auto-generate the transfer factors (TFs) file." % src
        raise Exception(ShellStyles.ErrorStyle() + msg + ShellStyles.NormalStyle())
    else:
        Print("Importing transfer factors (TFs) from file %s" % (ShellStyles.NoteStyle() + os.path.basename(src) + ShellStyles.NormalStyle()), True)
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

def printNormFactors(myNormFactors):
    '''
    Normalisation Factors are simply the transfer factors (TF or R_i)
    where i indicates the bin the Fake-b measurement is performed in
    e.g. eta bins of leading b-jet 
    '''
    # Constuct the table
    table   = []
    align  = "{:^10} {:>15} {:^3} {:<10} {:<10} {:<10}"
    header = align.format("Bin Label", "TF", "", "Error", "TF (Up)", "TF (Down)")
    hLine  = "="*80
    table.append(hLine)
    table.append(header)
    table.append(hLine)

    # For-loop: All Fake-b measurement bins
    for i, binLabel in  enumerate(myNormFactors[opts.normFactorKey], 1):
        TF_Value     = myNormFactors[opts.normFactorKey][binLabel]
        TF_Error     = myNormFactors["Error"][binLabel]
        TF_ValueUp   = myNormFactors["SystVarUp"][binLabel]
        TF_ValueDown = myNormFactors["SystVarDown"][binLabel]
        table.append(align.format(binLabel, TF_Value,  "+/-", TF_Error, TF_ValueUp, TF_ValueDown) )
    table.append(hLine)

    # For-loop: All rows in table
    for i, row in enumerate(table, 1):
        #Print(row, i==1)
        Print(row, False)
    return

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
    src = getTransferFactorsSrcFilename(multicrabDirName, opts.normFactorsSrc % moduleInfoString)

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
    Verbose("Importing the transfer factors from src file %s" % (ShellStyles.NoteStyle() + src + ShellStyles.NormalStyle()), True)
    srcBase = os.path.basename("/".join(pathList))
    normFactorsImport = __import__(srcBase)
    
    # Get the function definition and check if the eta, searchMode, and optimizationMode are correct
    Verbose("Check that the era=%s, searchMode=%s, optimizationMode=%s info matches!" % (era, searchMode, optimizationMode) )
    myNormFactorsSafetyCheck = getattr(normFactorsImport, "FakeBNormalisationSafetyCheck")
    myNormFactorsSafetyCheck(era, searchMode, optimizationMode)

    # Obtain the normalization (tranfer factors) and their systematic variations
    myNormFactorsImport              = getattr(normFactorsImport, "FakeBNormalisation_Value")
    myNormFactorsImportError         = getattr(normFactorsImport, "FakeBNormalisation_Error")
    myNormFactorsImportSystVarUp     = getattr(normFactorsImport, "FakeBNormalisation_ErrorUp")
    myNormFactorsImportSystVar2xUp   = getattr(normFactorsImport, "FakeBNormalisation_ErrorUp2x")
    myNormFactorsImportSystVar3xUp   = getattr(normFactorsImport, "FakeBNormalisation_ErrorUp3x")
    myNormFactorsImportSystVarDown   = getattr(normFactorsImport, "FakeBNormalisation_ErrorDown")
    myNormFactorsImportSystVar2xDown = getattr(normFactorsImport, "FakeBNormalisation_ErrorDown2x")
    myNormFactorsImportSystVar3xDown = getattr(normFactorsImport, "FakeBNormalisation_ErrorDown3x")
    msg = "Obtained transfer factors (TFs) from file %s. The values are:" % (ShellStyles.NoteStyle() + srcBase + ShellStyles.NormalStyle() )
    Verbose(msg, True)

    # Import the normalisation factors and inform user
    myNormFactors = {}
    myNormFactors["Nominal"]       = myNormFactorsImport
    myNormFactors["Error"]         = myNormFactorsImportError
    myNormFactors["SystVarUp"]     = myNormFactorsImportSystVarUp
    myNormFactors["SystVar2xUp"]   = myNormFactorsImportSystVar2xUp
    myNormFactors["SystVar3xUp"]   = myNormFactorsImportSystVar3xUp
    myNormFactors["SystVarDown"]   = myNormFactorsImportSystVarDown
    myNormFactors["SystVar2xDown"] = myNormFactorsImportSystVar2xDown
    myNormFactors["SystVar3xDown"] = myNormFactorsImportSystVar3xDown

    # Print the Normalisation Factors aka Transfer Factors (TF)
    if 0:
        printNormFactors(myNormFactors)
    return myNormFactors

def getSystematicsNames(mySystematicsNamesRaw, opts):
    mySystematicsNames = []
    # Sanity check
    if len(mySystematicsNamesRaw) < 1:
        Print("There are 0 systematic variation sources", True)
        return mySystematicsNames
    if opts.test:
        Print("Disabling systematic variations", True)
        return mySystematicsNames

    # For-loop: All systematics raw names
    for i, item in enumerate(mySystematicsNamesRaw, 0):
        # Print("Using systematic %s" % (ShellStyles.NoteStyle() + item + ShellStyles.NormalStyle()), i==0)
        mySystematicsNames.append("%sPlus" % item)
        mySystematicsNames.append("%sMinus"% item)    

    Print("There are %d systematic variation sources:%s\n\t%s%s" % (len(mySystematicsNames), ShellStyles.NoteStyle(), "\n\t".join(mySystematicsNames), ShellStyles.NormalStyle()), True)
    return mySystematicsNames

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
    myModuleSelector.doSelect(opts=None) #fixme: (opts=opts)?

    # Loop over era/searchMode/optimizationMode combos
    myTotalModules  = myModuleSelector.getSelectedCombinationCount() * (len(mySystematicsNames)+1) * len(opts.shape)
    Verbose("Found %s modules in total" % (myTotalModules), True)

    count, nEras, nSearchModes, nOptModes, nSysVars = myModuleSelector.getSelectedCombinationCountIndividually()
    if nSysVars > 0:
        msg = "Running over %d modules (%d eras x %d searchModes x %d optimizationModes x %d systematic variations)" % (count, nEras, nSearchModes, nOptModes, nSysVars)
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
        Verbose(ShellStyles.HighlightAltStyle() + msg, True)

        # Initialize
        myOutputCreator.initialize(subTitle=shapeType, prefix="") #fixme: remove shapeType from sub-directory name?

        # Get lists of settings
        erasList   = myModuleSelector.getSelectedEras()
        modesList  = myModuleSelector.getSelectedSearchModes()
        optList    = myModuleSelector.getSelectedOptimizationModes()
        if 0:
            optList.append("") #append the default opt mode iff more optimization modes exist

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

                    # Obtain normalization factors for given Era, SearchMode, and OptimizationMode!
                    myNormFactors = importNormFactors(era, searchMode, optimizationMode, opts.mcrab)

                    # Nominal module
                    myModuleInfoString = getModuleInfoString(era, searchMode, optimizationMode)
                    iModule += 1

                    # Inform user of what is being processes
                    if optimizationMode != "":
                        msg = "Module %d/%d: %s_%s_%s_%s" % (iModule, myTotalModules, opts.analysisName, searchMode, era, optimizationMode)
                    else:
                        msg = "Module %d/%d: %s_%s_%s" % (iModule, myTotalModules, opts.analysisName, searchMode, era)
                    Print(ShellStyles.HighlightAltStyle() + msg + ShellStyles.NormalStyle(), iModule==1) 

                    # Keep time
                    myStartTime = time.time()

                    Verbose("Create dataset manager with given settings", True)
                    nominalModule = ModuleBuilder(opts, myOutputCreator, opts.verbose)
                    nominalModule.createDsetMgr(opts.mcrab, era, searchMode, optimizationMode)
                    
                    if (iModule == 1):
                        if opts.verbose:
                            nominalModule.debug()
                     
                    # Build the module
                    doFakeBNormalisationSyst = False 
                    nominalModule.buildModule(opts.dataSrc, opts.ewkSrc, myNormFactors[opts.normFactorKey], doFakeBNormalisationSyst, opts.normDataSrc, opts.normEwkSrc)

                    # Do TF variations named "SystVarUp" and "SystVarDown" (i.e. (Get results using TF+Error and TF-Error instead of TF)
                    if len(mySystematicsNames) > 0:
                        Verbose("Adding FakeB normalization systematics (iff also other systematics  present) ", True)
                        #nominalModule.buildTransferFactorVarSystModule(opts.dataSrc, opts.ewkSrc, myNormFactors["SystVarUp"], myNormFactors["SystVarDown"])
                        nominalModule.buildTransferFactorVarSystModule(opts.dataSrc, opts.ewkSrc, myNormFactors)
                    
                    Verbose("Deleting nominal module", True)
                    nominalModule.delete()

                    Verbose("Printing time estimate", True)
                    printTimeEstimate(myGlobalStartTime, myStartTime, iModule, myTotalModules)

                    Verbose("Now do the rest of systematics variations", True)
                    for syst in mySystematicsNames:
                        iModule += 1
                        msg = "Module %d/%d: %s/%s" % (iModule, myTotalModules, myModuleInfoString, syst)
                        print
                        Print(ShellStyles.HighlightAltStyle() + msg + ShellStyles.NormalStyle(), False)
                        myStartTime = time.time()
                        systModule  = ModuleBuilder(opts, myOutputCreator)
                        # Create dataset manager with given settings
                        systModule.createDsetMgr(opts.mcrab, era, searchMode, optimizationMode, systematicVariation=syst)

                        # Build systematics module
                        Verbose("Building systematics module (opts.normFactorKey = %s)" % (opts.normFactorKey), True)
                        systModule.buildModule(opts.dataSrc, opts.ewkSrc, myNormFactors[opts.normFactorKey], False, opts.normDataSrc, opts.normEwkSrc)
                        printTimeEstimate(myGlobalStartTime, myStartTime, iModule, myTotalModules)
                        systModule.delete()
        print
        Verbose("Pseudo-multicrab ready for %s" % shapeType, True)
        
    # Print some timing statistics
    Verbose("Average processing time per module was %.1f seconds" % getAvgProcessTimeForOneModule(myGlobalStartTime, myTotalModules), True)
    Print("Total elapsed time was %.1f seconds" % getTotalElapsedTime(myGlobalStartTime), True)

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
    INTLUMI          = -1.0
    URL              = False
    SAVEDIR          = "/publicweb/a/aattikis/FakeBMeasurement/"
    VERBOSE          = False
    TEST             = False
    FACTOR_SRC       = "FakeBTransferFactors_%s.py"
    DATA_SRC         = "ForDataDrivenCtrlPlots" #"ForFakeBMeasurement"
    EWK_SRC          = DATA_SRC + "EWKGenuineB" # FakeB = Data - EWK GenuineB
    NORM_DATA_SRC    = DATA_SRC + "EWKGenuineB" 
    NORM_EWK_SRC     = DATA_SRC + "EWKGenuineB"
    INCLUSIVE_ONLY   = False
    SHAPE            = ["TrijetMass"]
    NORMFACTOR_KEY   = "Nominal" # "Nominal", "SystVarUp", "SystVarDown"
 
    # Define the available script options
    parser = OptionParser(usage="Usage: %prog [options]", add_help_option=True, conflict_handler="resolve")

    parser.add_option("-m", "--mcrab", dest="mcrab", action="store",# required=True,
                      help="Path to the multicrab directory for input [default: None]")

    parser.add_option("--normFactorKey", dest="normFactorKey", default=NORMFACTOR_KEY, 
                      help="The normalisation factor key (e.g. nominal) [default: %s]" % (NORMFACTOR_KEY) )

    parser.add_option("--inclusiveOnly", dest="useInclusiveNorm", action="store_true", default=INCLUSIVE_ONLY, 
                      help="Use only inclusive weight instead of binning [default: %s]" % (INCLUSIVE_ONLY) )
    
    parser.add_option("--normFactorsSrc", dest="normFactorsSrc", action="store", default=FACTOR_SRC,
                      help="The python file (auto-generated) containing the normalisation factors. [default: %s]" % FACTOR_SRC)

    parser.add_option("--shape", dest="shape", action="store", default=SHAPE, 
                      help="Shape identifiers")

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
            Verbose(msg , True)

    # Sanity check: fixme
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
    msg = "The following datasets will comprise the %sEWK merged-datasets%s:"  % (ShellStyles.NoteStyle(), ShellStyles.NormalStyle())
    Print(msg, True)     
    Print(", ".join(opts.ewkDatasets), False)

    # Call the main function
    main(opts)

    if not opts.batchMode:
        raw_input("=== makePseudoMulticrab.py: Press any key to quit ROOT ...")
