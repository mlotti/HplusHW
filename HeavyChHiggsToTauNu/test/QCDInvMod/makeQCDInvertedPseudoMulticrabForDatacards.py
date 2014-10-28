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

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.analysisModuleSelector as analysisModuleSelector
import HiggsAnalysis.HeavyChHiggsToTauNu.qcdInverted.qcdInvertedResult as qcdInvertedResult
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShellStyles as ShellStyles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.pseudoMultiCrabCreator as pseudoMultiCrabCreator

#myNormalizationFactorSource = "QCDInvertedNormalizationFactors.py"
myNormalizationFactorSource = "QCDPlusEWKFakeTauNormalizationFactors.py" 

def doNominalModule(myMulticrabDir,era,searchMode,optimizationMode,myOutputCreator,myShapeString,myNormFactors,myQCDNormFactors,myEWKFakeTauNormFactors,myDisplayStatus,dataDrivenFakeTaus):
    # Construct info string of module
    myModuleInfoString = "%s_%s_%s"%(era, searchMode, optimizationMode)
    # Obtain dataset manager
    dsetMgrCreator = dataset.readFromMulticrabCfg(directory=myMulticrabDir)
    dsetMgr = dsetMgrCreator.createDatasetManager(dataEra=era,searchMode=searchMode,optimizationMode=optimizationMode)
    # Do the usual normalisation
    dsetMgr.updateNAllEventsToPUWeighted()
    dsetMgr.loadLuminosities()
    plots.mergeRenameReorderForDataMC(dsetMgr)
    dsetMgr.merge("EWK", ["TTJets","WJets","DYJetsToLL","SingleTop","Diboson"])
    # Obtain luminosity
    myLuminosity = dsetMgr.getDataset("Data").getLuminosity()
    # Print info so that user can check that merge went correct
    if myDisplayStatus:
        dsetMgr.printDatasetTree()
        print "Luminosity = %f 1/fb"%(myLuminosity / 1000.0)
        print
        myDisplayStatus = False
    # Gather results
    # Create containers for results
    myModuleResults = pseudoMultiCrabCreator.PseudoMultiCrabModule(dsetMgr, era, searchMode, optimizationMode)
    myQCDNormalizationSystResults = pseudoMultiCrabCreator.PseudoMultiCrabModule(dsetMgr, era, searchMode, optimizationMode, "SystVarQCDNormSource")
    # Obtain results
    myResult = qcdInvertedResult.QCDInvertedResultManager(myShapeString, "AfterCollinearCuts", dsetMgr, myLuminosity, myModuleInfoString, myNormFactors, dataDrivenFakeTaus=dataDrivenFakeTaus, shapeOnly=False, displayPurityBreakdown=True, noRebin=True)
    # Store results
    myModuleResults.addShape(myResult.getShape(), myShapeString)
    myModuleResults.addShape(myResult.getShapeMCEWK(), myShapeString+"_MCEWK")
    myModuleResults.addShape(myResult.getShapePurity(), myShapeString+"_Purity")
    myModuleResults.addDataDrivenControlPlots(myResult.getControlPlots(),myResult.getControlPlotLabels())
    myOutputCreator.addModule(myModuleResults)
    # Up variation of QCD normalization (i.e. ctrl->signal region transition)
    # Note that only the source histograms for the shape uncert are stored
    # because the result must be calculated after rebinning
    # (and rebinning is no longer done here for flexibility reasons)
    myQCDNormalizationSystResults.addShape(myResult.getRegionSystNumerator(), myShapeString+"Numerator")
    myQCDNormalizationSystResults.addShape(myResult.getRegionSystDenominator(), myShapeString+"Denominator")
    myLabels = myResult.getControlPlotLabelsForQCDSyst()
    for i in range(0,len(myLabels)):
        myLabels[i] = myLabels[i]+"Numerator"
    myQCDNormalizationSystResults.addDataDrivenControlPlots(myResult.getRegionSystNumeratorCtrlPlots(),myLabels)
    for i in range(0,len(myLabels)):
        myLabels[i] = myLabels[i].replace("Numerator","Denominator")
    myQCDNormalizationSystResults.addDataDrivenControlPlots(myResult.getRegionSystDenominatorCtrlPlots(),myLabels)
    myOutputCreator.addModule(myQCDNormalizationSystResults)

    # qg systematics
    # normalization with only qcd (plus)
    myQCDqgReweightingSystResultsPlus = pseudoMultiCrabCreator.PseudoMultiCrabModule(dsetMgr, era, searchMode, optimizationMode, "SystVarQCDqgReweightingPlus")
    myResult_qgPlus = qcdInvertedResult.QCDInvertedResultManager(myShapeString, "AfterCollinearCuts", dsetMgr, myLuminosity,myModuleInfoString, myQCDNormFactors, dataDrivenFakeTaus=dataDrivenFakeTaus, shapeOnly=False, displayPurityBreakdown=True, noRebin=True)                                                                                           
    myQCDqgReweightingSystResultsPlus.addShape(myResult_qgPlus.getShape(), myShapeString)
    myQCDqgReweightingSystResultsPlus.addShape(myResult_qgPlus.getShapeMCEWK(), myShapeString+"_MCEWK")
    myQCDqgReweightingSystResultsPlus.addShape(myResult_qgPlus.getShapePurity(), myShapeString+"_Purity")
    myQCDqgReweightingSystResultsPlus.addDataDrivenControlPlots(myResult_qgPlus.getControlPlots(),myResult.getControlPlotLabels())
    myOutputCreator.addModule(myQCDqgReweightingSystResultsPlus)

    # normalization with only fake taus (minus)
    myQCDqgReweightingSystResultsMinus = pseudoMultiCrabCreator.PseudoMultiCrabModule(dsetMgr, era, searchMode, optimizationMode, "SystVarQCDqgReweightingMinus")
    myResult_qgMinus = qcdInvertedResult.QCDInvertedResultManager(myShapeString, "AfterCollinearCuts", dsetMgr, myLuminosity,myModuleInfoString, myEWKFakeTauNormFactors, dataDrivenFakeTaus=dataDrivenFakeTaus, shapeOnly=False, displayPurityBreakdown=True, noRebin=True)                                                                                           
    myQCDqgReweightingSystResultsMinus.addShape(myResult_qgMinus.getShape(), myShapeString)
    myQCDqgReweightingSystResultsMinus.addShape(myResult_qgMinus.getShapeMCEWK(), myShapeString+"_MCEWK")
    myQCDqgReweightingSystResultsMinus.addShape(myResult_qgMinus.getShapePurity(), myShapeString+"_Purity")
    myQCDqgReweightingSystResultsMinus.addDataDrivenControlPlots(myResult_qgMinus.getControlPlots(),myResult.getControlPlotLabels())
    myOutputCreator.addModule(myQCDqgReweightingSystResultsMinus)

    # Clean up
    myResult.delete()
    dsetMgr.close()
    dsetMgrCreator.close()
    ROOT.gROOT.CloseFiles()
    ROOT.gROOT.GetListOfCanvases().Delete()
    ROOT.gDirectory.GetList().Delete()

def doSystematicsVariation(myMulticrabDir,era,searchMode,optimizationMode,syst,myOutputCreator,myShapeString,myNormFactors,dataDrivenFakeTaus):
    myModuleInfoString = "%s_%s_%s_%s"%(era, searchMode, optimizationMode,syst)
    dsetMgrCreator = dataset.readFromMulticrabCfg(directory=myMulticrabDir)
    systDsetMgr = dsetMgrCreator.createDatasetManager(dataEra=era,searchMode=searchMode,optimizationMode=optimizationMode,systematicVariation=syst)
    # Do the usual normalisation
    systDsetMgr.updateNAllEventsToPUWeighted()
    systDsetMgr.loadLuminosities()
    plots.mergeRenameReorderForDataMC(systDsetMgr)
    systDsetMgr.merge("EWK", ["TTJets","WJets","DYJetsToLL","SingleTop","Diboson"])
    myLuminosity = systDsetMgr.getDataset("Data").getLuminosity()
    # Obtain results
    mySystModuleResults = pseudoMultiCrabCreator.PseudoMultiCrabModule(systDsetMgr, era, searchMode, optimizationMode, syst)
    mySystResult = qcdInvertedResult.QCDInvertedResultManager(myShapeString, "AfterCollinearCuts", systDsetMgr, myLuminosity, myModuleInfoString, myNormFactors, dataDrivenFakeTaus=dataDrivenFakeTaus, shapeOnly=False, displayPurityBreakdown=False, noRebin=True)
    mySystModuleResults.addShape(mySystResult.getShape(), myShapeString)
    mySystModuleResults.addShape(mySystResult.getShapeMCEWK(), myShapeString+"_MCEWK")
    mySystModuleResults.addShape(mySystResult.getShapePurity(), myShapeString+"_Purity")
    mySystModuleResults.addDataDrivenControlPlots(mySystResult.getControlPlots(),mySystResult.getControlPlotLabels())
    mySystResult.delete()
    ## Save module info
    myOutputCreator.addModule(mySystModuleResults)
    systDsetMgr.close()
    dsetMgrCreator.close()
    ROOT.gROOT.CloseFiles()
    ROOT.gROOT.GetListOfCanvases().Delete()
    ROOT.gDirectory.GetList().Delete()

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
    if os.path.exists(myNormalizationFactorSource):
        myQCDNormFactorsImport = getattr(__import__(myNormalizationFactorSource.replace(".py","")), "QCDInvertedNormalizationOnlyQCD")
        myEWKFakeTauNormFactorsImport = getattr(__import__(myNormalizationFactorSource.replace(".py","")), "QCDInvertedNormalizationOnlyEWKFakeTau")
        myQCDNormFactorsSafetyCheck = getattr(__import__(myNormalizationFactorSource.replace(".py","")), "QCDInvertedNormalizationSafetyCheck")
        #QCDInvertedNormalizationSafetyCheck(era)
        myQCDNormFactors = myQCDNormFactorsImport.copy()
        myEWKFakeTauNormFactors = myEWKFakeTauNormFactorsImport.copy()
    else:
        raise Exception(ShellStyles.ErrorLabel()+"Normalisation factors ('%s.py') not found!\nRun script InvertedTauID_Normalization.py to generate the normalization factors."%myNormalizationFactorSource)
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

    myShapes = ["mt","invmass"]
    if opts.transverseMassOnly != None and opts.transverseMassOnly:
        myShapes = ["mt"]
    elif opts.invariantMassOnly != None and opts.invariantMassOnly:
        myShapes = ["invmass"]

    dataDrivenFakeTaus = opts.dataDrivenFakeTaus

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
            myShapeString = "shapeTransverseMass"
        elif massType == "invmass":
            myShapeString = "shapeInvariantMass"
        myOutputCreator.initialize(massType)
        print ShellStyles.HighlightStyle()+"Creating dataset for shape: %s%s"%(massType,ShellStyles.NormalStyle())
        for era in myModuleSelector.getSelectedEras():
            # Check if normalization coefficients are suitable for era
            #myNormFactorsSafetyCheck(era) #TODO
            for searchMode in myModuleSelector.getSelectedSearchModes():
                for optimizationMode in myModuleSelector.getSelectedOptimizationModes():
                    if os.path.exists(myNormalizationFactorSource):
                        myNormFactorsImport = getattr(__import__(myNormalizationFactorSource.replace(".py","")), "QCDInvertedNormalization"+optimizationMode)
                        myNormFactorsSafetyCheck = getattr(__import__(myNormalizationFactorSource.replace(".py","")), "QCDInvertedNormalizationSafetyCheck")
                        #QCDInvertedNormalizationSafetyCheck(era)
                        myNormFactorsSafetyCheck(era)
                        myNormFactors = myNormFactorsImport.copy()
                    else:
                        raise Exception(ShellStyles.ErrorLabel()+"Normalisation factors ('%s.py') not found!\nRun script InvertedTauID_Normalization.py to generate the normalization factors."%myNormalizationFactorSource)

                    myModuleInfoString = "%s_%s_%s"%(era, searchMode, optimizationMode)
                    n += 1
                    print ShellStyles.CaptionStyle()+"Module %d/%d: %s/%s%s"%(n,myTotalModules,myModuleInfoString,massType,ShellStyles.NormalStyle())
                    myStartTime = time.time()
                    doNominalModule(myMulticrabDir,era,searchMode,optimizationMode,myOutputCreator,myShapeString,myNormFactors,myQCDNormFactors,myEWKFakeTauNormFactors,myDisplayStatus,dataDrivenFakeTaus)
                    printTimeEstimate(myGlobalStartTime, myStartTime, n, myTotalModules)
                    # Now do the rest of systematics variations
                    for syst in mySystematicsNames:
                        n += 1
                        print ShellStyles.CaptionStyle()+"Analyzing systematics variations %d/%d: %s/%s/%s%s"%(n,myTotalModules,myModuleInfoString,syst,massType,ShellStyles.NormalStyle())
                        myStartTime = time.time()
                        doSystematicsVariation(myMulticrabDir,era,searchMode,optimizationMode,syst,myOutputCreator,myShapeString,myNormFactors,dataDrivenFakeTaus)
                        printTimeEstimate(myGlobalStartTime, myStartTime, n, myTotalModules)
        print "\nPseudo-multicrab ready for mass %s...\n"%massType
    # Create rest of pseudo multicrab directory
    myOutputCreator.finalize()
    print "Average processing time of one module: %.1f s, total elapsed time: %.1f s"%((time.time()-myGlobalStartTime)/float(myTotalModules), (time.time()-myGlobalStartTime))
