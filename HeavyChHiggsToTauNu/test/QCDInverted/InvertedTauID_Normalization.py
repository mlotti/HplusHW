#!/usr/bin/env python

###########################################################################
#
# This script is only intended as an example, please do NOT modify it.
# For example, start from scratch and look here for help, or make a
# copy of it and modify the copy (including removing all unnecessary
# code).
#
###########################################################################

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True
import math
import sys
import os
from optparse import OptionParser

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.analysisModuleSelector import *
from HiggsAnalysis.HeavyChHiggsToTauNu.qcdCommon.dataDrivenQCDCount import *

from InvertedTauID import *


def calculateNormalisation(opts, dsetMgr, moduleInfoString, myDir, luminosity):
    # Define histogram paths and names within the module
    myBaselineMetPrefix = "baseline/METBaselineTauId"
    myInvertedMetPrefix = "Inverted/METInvertedTauId"
    myMetHistoSuffix = "AfterCollinearCuts"
    #myMetHistoSuffix = "AfterCollinearCutsPlusBackToBackCuts"
    #myMetHistoSuffix = "AfterCollinearCutsPlusBtag"
    #myMetHistoSuffix = "AfterCollinearCutsPlusBveto"

    # Define MET histogram binning and other specifications
    myMetHistoSpecs = { "rangeMin": 0.0,
                        "rangeMax": 500.0,
                        "bins": 50, # needed only for uniform bin widths
                        #"variableBinSizeLowEdges": [], # if an empty list is given, then uniform bin width is used
                        #"variableBinSizeLowEdges": [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,160,180,200,250,300,400], # if an empty list is given, then uniform bin width is used
                        "xtitle": "E_{T}^{miss} / GeV",
                        "ytitle": "N_{Events}" }

    # Apply TDR style
    style = tdrstyle.TDRStyle()

    invertedQCD = InvertedTauID()
    invertedQCD.setLumi(luminosity)

    # Obtain data and EWK histograms splitted in phase space
    myBaselineMetShape = DataDrivenQCDShape(dsetMgr, "Data", "EWK", myBaselineMetPrefix+myMetHistoSuffix, luminosity)
    myInvertedMetShape = DataDrivenQCDShape(dsetMgr, "Data", "EWK", myInvertedMetPrefix+myMetHistoSuffix, luminosity)
    # Loop over phase space bins
    nSplitBins = myBaselineMetShape.getNumberOfPhaseSpaceSplitBins()
    for i in range(1, nSplitBins):
        print "Processing phase space bin %s%s%s"%(HighlightStyle(),myBaselineMetShape.getPhaseSpaceBinFileFriendlyTitle(i),NormalStyle())
        invertedQCD.setLabel("%s"%(myBaselineMetShape.getPhaseSpaceBinFileFriendlyTitle(i)))
        # Obtain QCD template for MET from data in inverted selection (high purity)
        hMetTemplateQCD = myInvertedMetShape.getDataHistoForSplittedBin(i, myMetHistoSpecs)
        # Obtain MC EWK+tt template for MET from simulation in baseline selection
        hMetTemplateEWK = myBaselineMetShape.getEwkHistoForSplittedBin(i, myMetHistoSpecs)
        # Obtain sum of QCD and EWK for fitting from baseline
        hMetForFitting = myBaselineMetShape.getDataHistoForSplittedBin(i, myMetHistoSpecs)

        invertedQCD.plotHisto(hMetTemplateQCD,"MetShape_Data_inverted")
        invertedQCD.plotHisto(hMetForFitting,"MetShape_Data_baseline")
        invertedQCD.fitQCD(hMetTemplateQCD)
        invertedQCD.fitEWK(hMetTemplateEWK,"LR")
        invertedQCD.fitData(hMetForFitting)
        invertedQCD.getNormalization()

    invertedQCD.Summary()
    myModuleInfo = moduleInfoString.split("_")
    invertedQCD.WriteNormalizationToFile("QCDInvertedNormalizationFactors.py", era=myModuleInfo[0], searchMode=myModuleInfo[1], optimizationMode=myModuleInfo[2])

if __name__ == "__main__":
    myModuleSelector = AnalysisModuleSelector() # Object for selecting data eras, search modes, and optimization modes

    parser = OptionParser(usage="Usage: %prog [options]",add_help_option=True,conflict_handler="resolve")
    myModuleSelector.addParserOptions(parser)
    parser.add_option("--mdir", dest="multicrabDir", action="store", help="Multicrab directory")
    # Add here parser options, if necessary, following line is an example
    #parser.add_option("--showcard", dest="showDatacard", action="store_true", default=False, help="Print datacards also to screen")

    # Parse options
    (opts, args) = parser.parse_args()

    # Obtain multicrab directory
    myMulticrabDir = "."
    if opts.multicrabDir != None:
        myMulticrabDir = opts.multicrabDir
    if not os.path.exists(myMulticrabDir+"/multicrab.cfg"):
        print "\n"+ErrorLabel()+"Cannot find multicrab.cfg! Did you use the --mdir parameter?\n"
        parser.print_help()
        sys.exit()

    # Obtain dsetMgrCreator and register it to module selector
    dsetMgrCreator = dataset.readFromMulticrabCfg(directory=myMulticrabDir)
    myModuleSelector.setPrimarySource("analysis", dsetMgrCreator)
    # Select modules
    myModuleSelector.doSelect(opts)

    # Normalization factors do not depend on MET cut or cuts beyond that (btag and delta phi back to back)
    # Reasonable optimization targets, which require separate normalisation factors are tau pt, jet pt and Njets
    # Of these tau pt is naturally handled because tau pt binning is applied (unless one chooses a cut that does not match to bin boundaries)
    # Warn user about special cases
    if len(myModuleSelector.getSelectedEras()) > 1:
        raise Exception(ErrorLabel()+"You asked to run eras %s!\nEach era needs it's own normalization factors, please specify with -e parameter only one era!"%(', '.join(map(str, myModuleSelector.getSelectedEras()))))
    if len(myModuleSelector.getSelectedSearchModes()) > 1:
        raise Exception(ErrorLabel()+"You asked to run search modes %s!\nEach search mode needs it's own normalization factors, please specify with -m parameter only one search mode!"%(', '.join(map(str, myModuleSelector.getSelectedSearchModes()))))
    if len(myModuleSelector.getSelectedOptimizationModes()) > 1:
        nJetVariations = []
        for optimizationMode in myModuleSelector.getSelectedOptimizationModes():
            if "Jet" in optimizationMode:
                nJetVariations.append(optimizationMode)
        if len(nJetVariations) > 1:
            raise Exception(ErrorLabel()+"You asked to run optimization modes %s which contain jet variations!\nEach jet selection needs it's own normalization factors, please specify with -o parameter only one jet selection!"%(', '.join(map(str, nJetVariations))))

    myDisplayStatus = True
    myNormalizationDoneStatus = False
    # Loop over era/searchMode/optimizationMode options
    for era in myModuleSelector.getSelectedEras():
        for searchMode in myModuleSelector.getSelectedSearchModes():
            for optimizationMode in myModuleSelector.getSelectedOptimizationModes():
                # Construct info string of module
                myModuleInfoString = "%s_%s_%s"%(era, searchMode, optimizationMode)
                print HighlightStyle()+"Module:",myModuleInfoString,NormalStyle()
                # Obtain dataset manager
                dsetMgr = dsetMgrCreator.createDatasetManager(dataEra=era,searchMode=searchMode,optimizationMode=optimizationMode)
                # Do the usual normalisation
                dsetMgr.updateNAllEventsToPUWeighted()
                dsetMgr.loadLuminosities()
                plots.mergeRenameReorderForDataMC(dsetMgr)
                dsetMgr.merge("EWK", [
                              "TTJets",
                              "WJets",
                              "DYJetsToLL",
                              "SingleTop",
                              "Diboson"
                              ],keepSources=True) # Keep sources needed to keep open TTJets
                # Make a directory for output
                myDir = ""
                #myDir = "plots_%s"%myModuleInfoString
                #createOutputdirectory(myDir)
                # Obtain luminosity
                myLuminosity = dsetMgr.getDataset("Data").getLuminosity()
                # Print info so that user can check that merge went correct
                if myDisplayStatus:
                    dsetMgr.printDatasetTree()
                    print "Luminosity = %f 1/fb"%(myLuminosity / 1000.0)
                    print
                    myDisplayStatus = False
                # Do normalization for one module only
                if not myNormalizationDoneStatus:
                    calculateNormalisation(opts, dsetMgr, myModuleInfoString, myDir, myLuminosity)
                    myNormalizationDoneStatus = True
                    print "Normalization done"

