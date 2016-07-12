#! /usr/bin/env python

import os
import sys

from optparse import OptionParser

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrabConsistencyCheck as consistencyCheck
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.analysisModuleSelector import *


if __name__ == "__main__":
    myModuleSelector = AnalysisModuleSelector() # Object for selecting data eras, search modes, and optimization modes
    parser = OptionParser(usage="Usage: %prog [options]",add_help_option=False,conflict_handler="resolve")
    parser.add_option("-h", "--help", dest="helpStatus", action="store_true", default=False, help="Show this help message and exit")
    parser.add_option("--mdir", dest="mdir", action="store", help="Path to multicrab directory")
    parser.add_option("--histo", dest="histo", action="store", help="Name of histogram (default='%s')"%consistencyCheck.histogramName)
    myModuleSelector.addParserOptions(parser)
    (opts, args) = parser.parse_args()

    # Check arguments
    myStatus = True
    if opts.mdir == None:
        print "Error: Make sure you provide path to multicrab directory with --mdir!"
        myStatus = False
    elif not os.path.exists(opts.mdir):
        raise Exception("Error: The path '%s' is not valid!"%opts.mdir)
    if not myStatus or opts.helpStatus:
        print ""
        parser.print_help()
        sys.exit()
    if not opts.histo == None:
        histogramName = opts.Histo

    # Obtain dsetMgrCreator and register it to module selector
    dsetMgrCreator = dataset.readFromMulticrabCfg(directory=opts.mdir)
    myModuleSelector.setPrimarySource("analysis", dsetMgrCreator)
    myModuleSelector.doSelect(opts)
    myModuleSelector.printSelectedCombinationCount()

    # Read from multicrab.cfg the number of jobs
    myDict = consistencyCheck.getNumberOfJobsFromMultiCrabCfg(opts.mdir)

    # Loop over selected modules
    myMergedDict = {}
    for searchMode in myModuleSelector.getSelectedSearchModes():
        for optimizationMode in myModuleSelector.getSelectedOptimizationModes():
            for era in myModuleSelector.getSelectedEras():
                dsetMgr = dsetMgrCreator.createDatasetManager(dataEra=era,searchMode=searchMode,optimizationMode=optimizationMode)
                consistencyCheck.getNumberOfJobsFromMergedHistogramsFromDsetMgr(dsetMgr, myMergedDict)

    # Compare dictionaries
    consistencyCheck.checkConsistency(myDict, myMergedDict)
