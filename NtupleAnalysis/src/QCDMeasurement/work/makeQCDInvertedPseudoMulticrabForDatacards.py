#!/usr/bin/env python

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True
import math
import sys
import os
import time
from optparse import OptionParser
import cProfile

import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.analysisModuleSelector as analysisModuleSelector
import HiggsAnalysis.QCDMeasurement.QCDInvertedResult as qcdInvertedResult
import HiggsAnalysis.NtupleAnalysis.tools.ShellStyles as ShellStyles
import HiggsAnalysis.NtupleAnalysis.tools.pseudoMultiCrabCreator as pseudoMultiCrabCreator

_generalOptions = {
    "analysisName": "QCDMeasurement",
    "ewkDatasetsForMerging": ["TT","WJets","DYJetsToLL"], #,"SingleTop"], #,"Diboson"], # using TT instead of TTJets
    "normalizationFactorSource": "QCDNormalizationFactors_AfterStdSelections%s.py",
    "normalizationPoint": "AfterStdSelections",
    "normalizationSourcePrefix": "ForQCDNormalization/Normalization",
    "ewkSourceForQCDPlusFakeTaus": "ForDataDrivenCtrlPlotsEWKGenuineTaus",
    "ewkSourceForQCDOnly": "ForDataDrivenCtrlPlots",
    "dataSource": "ForDataDrivenCtrlPlots",
}

class ModuleBuilder:
    def __init__(self, opts, outputCreator):
        self._opts = opts
        self._outputCreator = outputCreator
        self._moduleInfoString = None
        self._dsetMgrCreator = None
        self._dsetMgr = None
        self._normFactors = None
        self._luminosity = None
        self._nominalResult = None
        self._fakeWeightingPlusResult = None
        self._fakeWeightingMinusResult = None
        
    ## Clean up memory
    def delete(self):
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
        
    def createDsetMgr(self, multicrabDir, era, searchMode, optimizationMode=None, systematicVariation=None):
        self._era = era
        self._searchMode = searchMode
        self._optimizationMode = optimizationMode
        self._systematicVariation = systematicVariation
        # Construct info string of module
        self._moduleInfoString = "%s_%s_%s"%(era, searchMode, optimizationMode)
        # Obtain dataset manager
        self._dsetMgrCreator = dataset.readFromMulticrabCfg(directory=multicrabDir)
        self._dsetMgr = self._dsetMgrCreator.createDatasetManager(dataEra=era,searchMode=searchMode,optimizationMode=optimizationMode,systematicVariation=systematicVariation)
        # Do the usual normalisation
        self._dsetMgr.updateNAllEventsToPUWeighted()
        self._dsetMgr.loadLuminosities()
        plots.mergeRenameReorderForDataMC(self._dsetMgr)
        self._dsetMgr.merge("EWK", _generalOptions["ewkDatasetsForMerging"])
        # Obtain luminosity
        self._luminosity = self._dsetMgr.getDataset("Data").getLuminosity()
        
    def debug(self):
        self._dsetMgr.printDatasetTree()
        print "Luminosity = %f 1/fb"%(self._luminosity / 1000.0)

    def getModuleInfoString(self):
        return "%s_%s_%s"%(self._era, self._searchMode, self._optimizationMode)

    def buildModule(self,
                    dataPath,
                    ewkPath, 
                    normFactors,
                    calculateQCDNormalizationSyst,
                    normDataSrc=None,
                    normEWKSrc=None):
        # Create containers for results
        myModule = pseudoMultiCrabCreator.PseudoMultiCrabModule(self._dsetMgr,
                                                                self._era,
                                                                self._searchMode,
                                                                self._optimizationMode,
                                                                self._systematicVariation)
        # Obtain results
        self._nominalResult = qcdInvertedResult.QCDInvertedResultManager(dataPath,
                                                                         ewkPath,
                                                                         self._dsetMgr,
                                                                         self._luminosity,
                                                                         self.getModuleInfoString(),
                                                                         normFactors,
                                                                         optionCalculateQCDNormalizationSyst=calculateQCDNormalizationSyst,
                                                                         normDataSrc=normDataSrc,
                                                                         normEWKSrc=normEWKSrc,
                                                                         optionUseInclusiveNorm=self._opts.useInclusiveNorm)
        # Store results
        myModule.addPlots(self._nominalResult.getShapePlots(),
                          self._nominalResult.getShapePlotLabels())
        self._outputCreator.addModule(myModule)
    
    def buildQCDNormalizationSystModule(self, dataPath, ewkPath):
        # Up variation of QCD normalization (i.e. ctrl->signal region transition)
        # Note that only the source histograms for the shape uncert are stored
        # because the result must be calculated after rebinning
        # (and rebinning is no longer done here for flexibility reasons)
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

def printTimeEstimate(globalStart, localStart, nCurrent, nAll):
    myLocalDelta = time.time() - localStart
    myGlobalDelta = time.time() - globalStart
    myEstimate = myGlobalDelta / float(nCurrent) * float(nAll-nCurrent)
    s = "%02d:"%(myEstimate/60)
    myEstimate -= int(myEstimate/60)*60
    s += "%02d"%(myEstimate)
    print "Module finished in %.1f s, estimated time to complete: %s"%(myLocalDelta, s)


def importNormFactors(era, searchMode, optimizationMode, multicrabDirName):
    # Obtain suffix
    suffix = ""
    s = multicrabDirName.split("_")
    if s[len(s)-1].endswith("pr") or s[len(s)-1].endswith("prong"):
        suffix = "_"+s[len(s)-1]
    # Find candidates for normalisation scripts
    fileList = os.listdir(multicrabDirName)
    scriptList = []
    for item in fileList:
        if item.startswith((_generalOptions["normalizationFactorSource"]%"").replace(".py","")):
            scriptList.append(item)
    moduleInfoString = "_%s_%s"%(era, searchMode)
    if len(optimizationMode) > 0:
        moduleInfoString += "_%s"%(optimizationMode)
    # Construct source file name
    src = os.path.join(multicrabDirName, _generalOptions["normalizationFactorSource"]%moduleInfoString)
    if not os.path.exists(src):
        if len(scriptList):
            print "Found following normalization info files:"
            for item in scriptList:
                print "   ", item
        else:
            print "Found no normalization info files!"
        raise Exception(ShellStyles.ErrorLabel()+"Normalisation factors ('%s') not found!\nRun script QCDMeasurementNormalization.py to generate the normalization factors."%src)
    print "Reading normalisation factors from:", src
    # Check if normalization coefficients are suitable for era
    s = src.replace(".py","").split("/")
    if len(s) > 1:
        # Insert the directory where the norm.coeff. files reside into the path so that they are found
        sys.path.insert(0, os.path.join(os.getenv("PWD"), "/".join(map(str,s[:(len(s)-1)]))))
    normFactorsImport = __import__(s[len(s)-1])
    myNormFactorsSafetyCheck = getattr(normFactorsImport, "QCDInvertedNormalizationSafetyCheck")
    # Check that the era, searchMode, optimizationMode info matches
    myNormFactorsSafetyCheck(era, searchMode, optimizationMode)
    # Obtain normalization factors
    myNormFactorsImport = getattr(normFactorsImport, "QCDNormalization")
    myNormFactorsImportSystVarFakeWeightingDown = getattr(normFactorsImport, "QCDPlusEWKFakeTausNormalizationSystFakeWeightingVarDown")
    myNormFactorsImportSystVarFakeWeightingUp = getattr(normFactorsImport, "QCDPlusEWKFakeTausNormalizationSystFakeWeightingVarUp")
    myNormFactors = {}
    myNormFactors["nominal"] = myNormFactorsImport
    myNormFactors["FakeWeightingDown"] = myNormFactorsImportSystVarFakeWeightingDown
    myNormFactors["FakeWeightingUp"] = myNormFactorsImportSystVarFakeWeightingUp
    return myNormFactors

if __name__ == "__main__":
    # Object for selecting data eras, search modes, and optimization modes
    myModuleSelector = analysisModuleSelector.AnalysisModuleSelector()
    # Parse command line options
    parser = OptionParser(usage="Usage: %prog [options]",add_help_option=True,conflict_handler="resolve")
    myModuleSelector.addParserOptions(parser)
    parser.add_option("--mdir", dest="multicrabDir", action="store", help="Multicrab directory")
    parser.add_option("--shape", dest="shape", action="store", default=["MT"], help="shape identifiers")
    parser.add_option("--qcdonly", dest="qcdonly", action="store_true", default=False, help="Calculate QCD-only case instead of QCD+EWK fakes")
    parser.add_option("--inclusiveonly", dest="useInclusiveNorm", action="store_true", default=False, help="Use only inclusive weight instead of binning")
    parser.add_option("--test", dest="test", action="store_true", default=False, help="Make short test by limiting number of syst. variations")
    # Add here parser options, if necessary, following line is an example
    #parser.add_option("--showcard", dest="showDatacard", action="store_true", default=False, help="Print datacards also to screen")

    # Parse options
    (opts, args) = parser.parse_args()

    # Obtain multicrab directory
    myMulticrabDir = "."
    if opts.multicrabDir != None:
        myMulticrabDir = opts.multicrabDir
    if not os.path.exists("%s/multicrab.cfg"%myMulticrabDir):
        raise Exception(ShellStyles.ErrorLabel()+"No multicrab directory found at path '%s'! Please check path or specify it with --mdir!"%(myMulticrabDir)+ShellStyles.NormalStyle())
    if len(opts.shape) == 0:
        raise Exception(ShellStyles.ErrorLabel()+"Provide a shape identifierwith --shape (for example MT)!"+ShellStyles.NormalStyle())

    # Set EWK source depending on calculation mode
    if opts.qcdonly:
        _generalOptions["EWKsource"] = _generalOptions["ewkSourceForQCDOnly"]
    else:
        _generalOptions["EWKsource"] = _generalOptions["ewkSourceForQCDPlusFakeTaus"]

    # Obtain dsetMgrCreator and register it to module selector
    dsetMgrCreator = dataset.readFromMulticrabCfg(directory=myMulticrabDir)
    # Obtain systematics names
    mySystematicsNamesRaw = dsetMgrCreator.getSystematicVariationSources()
    mySystematicsNames = []
    for item in mySystematicsNamesRaw:
        mySystematicsNames.append("%sPlus"%item)
        mySystematicsNames.append("%sMinus"%item)
    if opts.test:
        mySystematicsNames = [mySystematicsNames[0]]

    myModuleSelector.setPrimarySource("analysis", dsetMgrCreator)
    # Select modules
    myModuleSelector.doSelect(opts)
    #dsetMgrCreator.close()
    # Loop over era/searchMode/optimizationMode combos
    myDisplayStatus = True
    myTotalModules = myModuleSelector.getSelectedCombinationCount() * (len(mySystematicsNames)+1) * len(opts.shape)
    myModuleSelector.printSelectedCombinationCount()
    # Loop over era/searchMode/optimizationMode options

    # Create pseudo-multicrab creator
    myOutputCreator = pseudoMultiCrabCreator.PseudoMultiCrabCreator(_generalOptions["analysisName"], myMulticrabDir)
    n = 0
    myGlobalStartTime = time.time()
    for shapeType in opts.shape:
        # Determine normalization sources
        #_generalOptions["normalizationDataSource"] = "%s%s%s"%(_generalOptions["normalizationSourcePrefix"], shapeType, _generalOptions["normalizationPoint"]) #obsolete
        _generalOptions["normalizationDataSource"] = "ForDataDrivenCtrlPlots"
#        prefix = _generalOptions["EWKsource"].replace(_generalOptions["dataSource"],"")
#        _generalOptions["normalizationEWKSource"] = _generalOptions["normalizationSourcePrefix"].replace("/","%s/"%prefix)
#        _generalOptions["normalizationEWKSource"] += "%s%s"%(shapeType, _generalOptions["normalizationPoint"])
        _generalOptions["normalizationEWKSource"] = "ForDataDrivenCtrlPlots"
        # Initialize
        myOutputCreator.initialize(shapeType)
        print ShellStyles.HighlightStyle()+"Creating dataset for shape: %s%s"%(shapeType,ShellStyles.NormalStyle())
        # Loop over era, searchMode, and optimizationMode
        for era in myModuleSelector.getSelectedEras():
            for searchMode in myModuleSelector.getSelectedSearchModes():
                for optimizationMode in myModuleSelector.getSelectedOptimizationModes():
                    #=====  Obtain normalization factors
                    myNormFactors = importNormFactors(era, searchMode, optimizationMode, opts.multicrabDir)
                    #===== Nominal module
                    myModuleInfoString = "%s_%s"%(era, searchMode)
                    if len(optimizationMode) > 0:
                        myModuleInfoString += "_%s"%optimizationMode
                    n += 1
                    print ShellStyles.CaptionStyle()+"Module %d/%d: %s/%s%s"%(n,myTotalModules,myModuleInfoString,shapeType,ShellStyles.NormalStyle())
                    myStartTime = time.time()
                    nominalModule = ModuleBuilder(opts, myOutputCreator)
                    nominalModule.createDsetMgr(multicrabDir=myMulticrabDir,
                                                era=era,
                                                searchMode=searchMode,
                                                optimizationMode=optimizationMode)
                    if (n == 1):
                        nominalModule.debug()
                    nominalModule.buildModule(_generalOptions["dataSource"],
                                              _generalOptions["EWKsource"],
                                              myNormFactors["nominal"],
                                              calculateQCDNormalizationSyst=True, # buildQCDNormalizationSystModule uses these!
                                              normDataSrc=_generalOptions["normalizationDataSource"],
                                              normEWKSrc=_generalOptions["normalizationEWKSource"])
                    #===== QCD normalization systematics
                    nominalModule.buildQCDNormalizationSystModule(_generalOptions["dataSource"],
                                                                  _generalOptions["EWKsource"])
                    if False: #FIXME
                    
                        #===== Quark gluon weighting systematics
                        nominalModule.buildQCDQuarkGluonWeightingSystModule(_generalOptions["dataSource"],
                                                                            _generalOptions["EWKsource"],
                                                                            myNormFactors["FakeWeightingUp"],
                                                                            myNormFactors["FakeWeightingDown"],
                                                                            calculateQCDNormalizationSyst=False,
                                                                            normDataSrc=_generalOptions["normalizationDataSource"],
                                                                            normEWKSrc=_generalOptions["normalizationEWKSource"])
                    nominalModule.delete()
                    #===== Time estimate
                    printTimeEstimate(myGlobalStartTime, myStartTime, n, myTotalModules)
                    #===== Now do the rest of systematics variations
                    for syst in mySystematicsNames:
                        n += 1
                        print ShellStyles.CaptionStyle()+"Analyzing systematics variations %d/%d: %s/%s/%s%s"%(n,myTotalModules,myModuleInfoString,syst,shapeType,ShellStyles.NormalStyle())
                        myStartTime = time.time()
                        systModule = ModuleBuilder(opts, myOutputCreator)
                        systModule.createDsetMgr(multicrabDir=myMulticrabDir,
                                                 era=era,
                                                 searchMode=searchMode,
                                                 optimizationMode=optimizationMode,
                                                 systematicVariation=syst)
                        systModule.buildModule(_generalOptions["dataSource"],
                                               _generalOptions["EWKsource"],
                                               myNormFactors["nominal"],
                                               calculateQCDNormalizationSyst=False,
                                               normDataSrc=_generalOptions["normalizationDataSource"],
                                               normEWKSrc=_generalOptions["normalizationEWKSource"])
                        printTimeEstimate(myGlobalStartTime, myStartTime, n, myTotalModules)
                        systModule.delete()
        print "\nPseudo-multicrab ready for mass %s...\n"%shapeType
    # Create rest of pseudo multicrab directory
    myOutputCreator.finalize()
    print "Average processing time of one module: %.1f s, total elapsed time: %.1f s"%((time.time()-myGlobalStartTime)/float(myTotalModules), (time.time()-myGlobalStartTime))
