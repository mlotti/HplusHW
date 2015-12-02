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

#myNormalizationFactorSource = "QCDInvertedNormalizationFactors.py"
myNormalizationFactorSource = "QCDInvertedNormalizationFactors_AfterStdSelections.py" 

_ewkDatasetsForMerging = ["TTJets","WJetsHT","DYJetsToLLHT","SingleTop"] #,"Diboson"]

_sourceDirectories = {
    "MCEWK": "ForDataDrivenCtrlPlotsGenuineTaus",
    "Data": "ForDataDrivenCtrlPlots"
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
        
    def __del__(self):
        # Clean up
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
        ROOT.gROOT.CloseFiles()
        ROOT.gROOT.GetListOfCanvases().Delete()
        ROOT.gDirectory.GetList().Delete()
        
    def createDsetMgr(self, multicrabDir, era, searchMode, optimizationMode):
        self._era = era
        self._searchMode = searchMode
        self._optimizationMode = optimizationMode
        # Construct info string of module
        self._moduleInfoString = "%s_%s_%s"%(era, searchMode, optimizationMode)
        # Obtain dataset manager
        self._dsetMgrCreator = dataset.readFromMulticrabCfg(directory=multicrabDir)
        self._dsetMgr = self._dsetMgrCreator.createDatasetManager(dataEra=era,searchMode=searchMode,optimizationMode=optimizationMode)
        # Do the usual normalisation
        self._dsetMgr.updateNAllEventsToPUWeighted()
        self._dsetMgr.loadLuminosities()
        plots.mergeRenameReorderForDataMC(self._dsetMgr)
        self._dsetMgr.merge("EWK", _ewkDatasetsForMerging)
        # Obtain luminosity
        self._luminosity = dsetMgr.getDataset("Data").getLuminosity()
        
    def debug(self):
        self._dsetMgr.printDatasetTree()
        print "Luminosity = %f 1/fb"%(self._luminosity / 1000.0)

    def buildModule(self, dataPath, ewkPath, histoName, normFactors):
        # Create containers for results
        myModule = pseudoMultiCrabCreator.PseudoMultiCrabModule(self._dsetMgr, self._era, self._searchMode, self._optimizationMode)
        # Obtain results
        self._nominalResult = qcdInvertedResult.QCDInvertedResultManager(histoName, "AfterCollinearCuts", 
                                                                         self._dsetMgr, self._luminosity, myModuleInfoString, normFactors, dataDrivenFakeTaus=dataDrivenFakeTaus, shapeOnly=False, displayPurityBreakdown=True, noRebin=True, optionUseInclusiveNorm=opts.inclusive)
        # Store results
        myModule.addShape(self._nominalResult.getShape(), myShapeString)
        #myModule.addShape(self._nominalResult.getShapeMCEWK(), myShapeString+"_MCEWK")
        #myModule.addShape(self._nominalResult.getShapePurity(), myShapeString+"_Purity")
        myModule.addDataDrivenControlPlots(self._nominalResult.getControlPlots(), self._nominalResult.getControlPlotLabels())
        self._outputCreator.addModule(myModule)
    
    def buildQCDNormalizationSystModule(self, dataPath, ewkPath, histoName, normFactors):
        # Up variation of QCD normalization (i.e. ctrl->signal region transition)
        # Note that only the source histograms for the shape uncert are stored
        # because the result must be calculated after rebinning
        # (and rebinning is no longer done here for flexibility reasons)
        mySystModule = pseudoMultiCrabCreator.PseudoMultiCrabModule(self._dsetMgr, self._era, self._searchMode, self._optimizationMode, "SystVarQCDNormSource")
        mySystModule.addShape(self._nominalResult.getRegionSystNumerator(), myShapeString+"Numerator")
        mySystModule.addShape(self._nominalResult.getRegionSystDenominator(), myShapeString+"Denominator")
        myLabels = self._nominalResult.getControlPlotLabelsForQCDSyst()
        for i in range(0,len(myLabels)):
            myLabels[i] = myLabels[i]+"Numerator"
        mySystModule.addDataDrivenControlPlots(self._nominalResult.getRegionSystNumeratorCtrlPlots(),myLabels)
        for i in range(0,len(myLabels)):
            myLabels[i] = myLabels[i].replace("Numerator","Denominator")
        mySystModule.addDataDrivenControlPlots(self._nominalResult.getRegionSystDenominatorCtrlPlots(),myLabels)
        self._outputCreator.addModule(mySystModule)

    def buildQCDQuarkGluonWeightingSystModule(self, dataPath, ewkPath, histoName, normFactors):
        # Up variation of fake weighting
        mySystModulePlus = pseudoMultiCrabCreator.PseudoMultiCrabModule(self._dsetMgr, self._era, self._searchMode, self._optimizationMode, "SystVarFakeWeightingPlus")
        self._fakeWeightingPlusResult = qcdInvertedResult.QCDInvertedResultManager(myShapeString, "AfterCollinearCuts", dsetMgr, myLuminosity,myModuleInfoString, myNormFactorsSystVarUp, dataDrivenFakeTaus=dataDrivenFakeTaus, shapeOnly=False, displayPurityBreakdown=True, noRebin=True, optionUseInclusiveNorm=opts.inclusive)
        mySystModulePlus.addShape(self._fakeWeightingPlusResult.getShape(), myShapeString)
        #mySystModulePlus.addShape(self._fakeWeightingPlusResult.getShapeMCEWK(), myShapeString+"_MCEWK")
        #mySystModulePlus.addShape(self._fakeWeightingPlusResult.getShapePurity(), myShapeString+"_Purity")
        mySystModulePlus.addDataDrivenControlPlots(self._fakeWeightingPlusResult.getControlPlots(),
                                                                 self._fakeWeightingPlusResult.getControlPlotLabels())
        self._outputCreator.addModule(mySystModulePlus)

        # Down variation of fake weighting
        mySystModuleMinus = pseudoMultiCrabCreator.PseudoMultiCrabModule(dself._dsetMgr, self._era, self._searchMode, self._optimizationMode, "SystVarFakeWeightingMinus", optionUseInclusiveNorm=opts.inclusive)
        self._fakeWeightingMinusResult = qcdInvertedResult.QCDInvertedResultManager(myShapeString, "AfterCollinearCuts", dsetMgr, myLuminosity,myModuleInfoString, myNormFactorsSystVarDown, dataDrivenFakeTaus=dataDrivenFakeTaus, shapeOnly=False, displayPurityBreakdown=True, noRebin=True)                                                                                           
        mySystModuleMinus.addShape(self._fakeWeightingMinusResult.getShape(), myShapeString)
        #mySystModuleMinus.addShape(self._fakeWeightingMinusResult.getShapeMCEWK(), myShapeString+"_MCEWK")
        #mySystModuleMinus.addShape(self._fakeWeightingMinusResult.getShapePurity(), myShapeString+"_Purity")
        mySystModuleMinus.addDataDrivenControlPlots(self._fakeWeightingMinusResult.getControlPlots(),myResult.getControlPlotLabels())
        self._outputCreator.addModule(mySystModuleMinus)


#def doSystematicsVariation(opts,myMulticrabDir,era,searchMode,optimizationMode,syst,myOutputCreator,myNormFactors,dataDrivenFakeTaus):
    #myModuleInfoString = "%s_%s_%s_%s"%(era, searchMode, optimizationMode,syst)
    #dsetMgrCreator = dataset.readFromMulticrabCfg(directory=myMulticrabDir)
    #systDsetMgr = dsetMgrCreator.createDatasetManager(dataEra=era,searchMode=searchMode,optimizationMode=optimizationMode,systematicVariation=syst)
    ## Do the usual normalisation
    #systDsetMgr.updateNAllEventsToPUWeighted()
    #systDsetMgr.loadLuminosities()
    #plots.mergeRenameReorderForDataMC(systDsetMgr)
    #systDsetMgr.merge("EWK", _ewkDatasetsForMerging)
    #myLuminosity = systDsetMgr.getDataset("Data").getLuminosity()
    ## Obtain results
    #mySystModuleResults = pseudoMultiCrabCreator.PseudoMultiCrabModule(systDsetMgr, era, searchMode, optimizationMode, syst)
    #mySystResult = qcdInvertedResult.QCDInvertedResultManager(myShapeString, "AfterCollinearCuts", systDsetMgr, myLuminosity, myModuleInfoString, myNormFactors, dataDrivenFakeTaus=dataDrivenFakeTaus, shapeOnly=False, displayPurityBreakdown=False, noRebin=True, optionUseInclusiveNorm=opts.inclusive)
    #mySystModuleResults.addShape(mySystResult.getShape(), myShapeString)
    #mySystModuleResults.addShape(mySystResult.getShapeMCEWK(), myShapeString+"_MCEWK")
    #mySystModuleResults.addShape(mySystResult.getShapePurity(), myShapeString+"_Purity")
    #mySystModuleResults.addDataDrivenControlPlots(mySystResult.getControlPlots(),mySystResult.getControlPlotLabels())
    #mySystResult.delete()
    ### Save module info
    #myOutputCreator.addModule(mySystModuleResults)
    #systDsetMgr.close()
    #dsetMgrCreator.close()
    #ROOT.gROOT.CloseFiles()
    #ROOT.gROOT.GetListOfCanvases().Delete()
    #ROOT.gDirectory.GetList().Delete()

def printTimeEstimate(globalStart, localStart, nCurrent, nAll):
    myLocalDelta = time.time() - localStart
    myGlobalDelta = time.time() - globalStart
    myEstimate = myGlobalDelta / float(nCurrent) * float(nAll-nCurrent)
    s = "%02d:"%(myEstimate/60)
    myEstimate -= int(myEstimate/60)*60
    s += "%02d"%(myEstimate)
    print "Module finished in %.1f s, estimated time to complete: %s"%(myLocalDelta, s)

if __name__ == "__main__":
    # Obtain normalization factors
    myNormFactors = None
    myNormFactorsSafetyCheck = None

    # Object for selecting data eras, search modes, and optimization modes
    myModuleSelector = analysisModuleSelector.AnalysisModuleSelector()
    # Parse command line options
    parser = OptionParser(usage="Usage: %prog [options]",add_help_option=True,conflict_handler="resolve")
    myModuleSelector.addParserOptions(parser)
    parser.add_option("--mdir", dest="multicrabDir", action="store", help="Multicrab directory")
    parser.add_option("--mtonly", dest="transverseMassOnly", action="store_true", default=False, help="Create only transverse mass plots")
    parser.add_option("--invmassonly", dest="invariantMassOnly", action="store_true", default=False, help="Create only invariant mass plots")
    parser.add_option("--test", dest="test", action="store_true", default=False, help="Make short test by limiting number of syst. variations")
    parser.add_option("--datadrivenfaketaus", dest="dataDrivenFakeTaus", action="store_true", default=False, help="Use data-driven fake tau measurement")
    parser.add_option("--inclusive", dest="inclusive", action="store_true", default=False, help="Use inclusive normalization")
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

    myShapes = ["mt"]#,"invmass"]
    if opts.transverseMassOnly != None and opts.transverseMassOnly:
        myShapes = ["mt"]
    elif opts.invariantMassOnly != None and opts.invariantMassOnly:
        myShapes = ["invmass"]

    dataDrivenFakeTaus = opts.dataDrivenFakeTaus
    if not opts.dataDrivenFakeTaus:
        _sourceDirectories["MCEWK"] = _sourceDirectories["Data"]

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
    myTotalModules = myModuleSelector.getSelectedCombinationCount() * (len(mySystematicsNames)+1) * len(myShapes)
    myModuleSelector.printSelectedCombinationCount()
    # Loop over era/searchMode/optimizationMode options

    # Create pseudo-multicrab creator
    myOutputCreator = pseudoMultiCrabCreator.PseudoMultiCrabCreator("QCDinverted", myMulticrabDir)
    n = 0
    myGlobalStartTime = time.time()
    for massType in myShapes:
        myShapeString = ""
        if massType == "mt":
            myShapeString = "ForDataDrivenCtrlPlots/shapeTransverseMass"
        elif massType == "invmass":
            myShapeString = "ForDataDrivenControlPlots/shapeInvariantMass"
        myOutputCreator.initialize(massType)
        print ShellStyles.HighlightStyle()+"Creating dataset for shape: %s%s"%(massType,ShellStyles.NormalStyle())
        for era in myModuleSelector.getSelectedEras():
            # Check if normalization coefficients are suitable for era
            #myNormFactorsSafetyCheck(era) #TODO
            for searchMode in myModuleSelector.getSelectedSearchModes():
                for optimizationMode in myModuleSelector.getSelectedOptimizationModes():
                    if os.path.exists(myNormalizationFactorSource):
                        myNormFactorsImport = getattr(__import__(myNormalizationFactorSource.replace(".py","")), "QCDPlusEWKFakeTausNormalization"+optimizationMode)
                        myNormFactorsImportSystVarDown = getattr(__import__(myNormalizationFactorSource.replace(".py","")), "QCDPlusEWKFakeTausNormalization"+optimizationMode+"SystFakeWeightingVarDown")
                        myNormFactorsImportSystVarUp = getattr(__import__(myNormalizationFactorSource.replace(".py","")), "QCDPlusEWKFakeTausNormalization"+optimizationMode+"SystFakeWeightingVarUp")
                        myNormFactorsSafetyCheck = getattr(__import__(myNormalizationFactorSource.replace(".py","")), "QCDInvertedNormalizationSafetyCheck")
                        #QCDInvertedNormalizationSafetyCheck(era)
                        myNormFactorsSafetyCheck(era)
                        myNormFactors = myNormFactorsImport.copy()
                        myNormFactorsSystVarDown = myNormFactorsImportSystVarDown.copy()
                        myNormFactorsSystVarUp = myNormFactorsImportSystVarUp.copy()
                    else:
                        raise Exception(ShellStyles.ErrorLabel()+"Normalisation factors ('%s.py') not found!\nRun script InvertedTauID_Normalization.py to generate the normalization factors."%myNormalizationFactorSource)

                    # Nominal module
                    myModuleInfoString = "%s_%s_%s"%(era, searchMode, optimizationMode)
                    n += 1
                    print ShellStyles.CaptionStyle()+"Module %d/%d: %s/%s%s"%(n,myTotalModules,myModuleInfoString,massType,ShellStyles.NormalStyle())
                    myStartTime = time.time()
                    nominalModule = ModuleBuilder(opts, myOutputCreator)
                    nominalModule.createDsetMgr(multicrabDir=myMulticrabDir,era=era,searchMode=searchMode,optimizationMode=optimizationMode)
                    if (n == 1):
                        nominalModule.debug()
                    nominalModule.buildModule( #FIXME
                    
                    doNominalModule(opts,myMulticrabDir,era,searchMode,optimizationMode,myOutputCreator,myNormFactors,myNormFactorsSystVarDown,myNormFactorsSystVarUp,myDisplayStatus,dataDrivenFakeTaus)
                    printTimeEstimate(myGlobalStartTime, myStartTime, n, myTotalModules)
                    # Now do the rest of systematics variations
                    for syst in mySystematicsNames:
                        n += 1
                        print ShellStyles.CaptionStyle()+"Analyzing systematics variations %d/%d: %s/%s/%s%s"%(n,myTotalModules,myModuleInfoString,syst,massType,ShellStyles.NormalStyle())
                        myStartTime = time.time()
                        systModule = ModuleBuilder(opts, myOutputCreator)
                        systModule.createDsetMgr(multicrabDir=myMulticrabDir,era=era,searchMode=searchMode,optimizationMode=optimizationMode)
                        systModule.buildModule( #FIXME
                        
                        #doSystematicsVariation(opts,myMulticrabDir,era,searchMode,optimizationMode,syst,myOutputCreator,myNormFactors,dataDrivenFakeTaus)
                        printTimeEstimate(myGlobalStartTime, myStartTime, n, myTotalModules)
        print "\nPseudo-multicrab ready for mass %s...\n"%massType
    # Create rest of pseudo multicrab directory
    myOutputCreator.finalize()
    print "Average processing time of one module: %.1f s, total elapsed time: %.1f s"%((time.time()-myGlobalStartTime)/float(myTotalModules), (time.time()-myGlobalStartTime))
