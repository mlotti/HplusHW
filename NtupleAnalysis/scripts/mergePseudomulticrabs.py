#!/usr/bin/env python
'''
DESCRIPTION:
Script that merges a list of pseudo-multicrabs into a new pseudo-multicrab
directory. It was created so that jobs with Systematic Variations can be broken
down into multiple jobs and submitted in parallel. The resulting output would have
to be merged and this is what this script is for.


USAGE:
./mergePseudomulticrabs.py -m <pseudomulticrab1>,<pseudomulticrab2>,<pseudomulticrab3>,... [opts]


EXAMPLES:
./merge_systematics.py -m Hplus2tbAnalysis_NewTopAndBugFixAndSF_TopMassLE400_BDT0p40_SystBTagSF_22Jul2018,Hplus2tbAnalysis_NewTopAndBugFixAndSF_TopMassLE400_BDT0p40_SystPUWeight_22Jul2018,Hplus2tbAnalysis_NewTopAndBugFixAndSF_TopMassLE400_BDT0p40_SystTopPt_22Jul2018,Hplus2tbAnalysis_NewTopAndBugFixAndSF_TopMassLE400_BDT0p40_SystTopTagSF_22Jul2018,Hplus2tbAnalysis_NewTopAndBugFixAndSF_TopMassLE400_BDT0p40_SystJES_22Jul2018,Hplus2tbAnalysis_NewTopAndBugFixAndSF_TopMassLE400_BDT0p40_SystJER_22Jul2018


LAST USED:
./merge_systematics.py -m Hplus2tbAnalysis_NewTopAndBugFixAndSF_TopMassLE400_BDT0p40_SystBTagSF_22Jul2018,Hplus2tbAnalysis_NewTopAndBugFixAndSF_TopMassLE400_BDT0p40_SystPUWeight_22Jul2018,Hplus2tbAnalysis_NewTopAndBugFixAndSF_TopMassLE400_BDT0p40_SystTopPt_22Jul2018,Hplus2tbAnalysis_NewTopAndBugFixAndSF_TopMassLE400_BDT0p40_SystTopTagSF_22Jul2018,Hplus2tbAnalysis_NewTopAndBugFixAndSF_TopMassLE400_BDT0p40_SystJES_22Jul2018,Hplus2tbAnalysis_NewTopAndBugFixAndSF_TopMassLE400_BDT0p40_SystJER_22Jul2018


'''
#================================================================================================ 
# Imports
#================================================================================================ 
import sys
import re
import math
import copy
import os
import shutil
from optparse import OptionParser

import ROOT
ROOT.gROOT.SetBatch(True)
from ROOT import *

import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.counter as counter
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux
import HiggsAnalysis.NtupleAnalysis.tools.crosssection as xsect
import HiggsAnalysis.NtupleAnalysis.tools.multicrabConsistencyCheck as consistencyCheck
import HiggsAnalysis.NtupleAnalysis.tools.ShellStyles as ShellStyles


#================================================================================================ 
# Function Definition
#================================================================================================ 
def Print(msg, printHeader=False):
    fName = __file__.split("/")[-1]
    if printHeader==True:
        print "=== ", fName
        print "\t", msg
    else:
        print "\t", msg
    return

def Verbose(msg, printHeader=True, verbose=False):
    if not opts.verbose:
        return
    aux.Print(msg, printHeader)
    return

def GetDatasetsFromDir(opts):
    Verbose("Getting datasets")
    
    if (not opts.includeOnlyTasks and not opts.excludeTasks):
        datasets = dataset.getDatasetsFromMulticrabDirs([opts.mcrabs[0]],
                                                        dataEra=opts.dataEra,
                                                        searchMode=opts.searchMode, 
                                                        analysisName=opts.analysisName,
                                                        optimizationMode=opts.optMode)
    elif (opts.includeOnlyTasks):
        datasets = dataset.getDatasetsFromMulticrabDirs([opts.mcrabs[0]],
                                                        dataEra=opts.dataEra,
                                                        searchMode=opts.searchMode,
                                                        analysisName=opts.analysisName,
                                                        includeOnlyTasks=opts.includeOnlyTasks,
                                                        optimizationMode=opts.optMode)
    elif (opts.excludeTasks):
        datasets = dataset.getDatasetsFromMulticrabDirs([opts.mcrabs[0]],
                                                        dataEra=opts.dataEra,
                                                        searchMode=opts.searchMode,
                                                        analysisName=opts.analysisName,
                                                        excludeTasks=opts.excludeTasks,
                                                        optimizationMode=opts.optMode)
    else:
        raise Exception("This should never be reached")
    return datasets
    
def main(opts):

    # Setup & configure the dataset manager 
    datasetsMgr = GetDatasetsFromDir(opts)
    datasetsMgr.updateNAllEventsToPUWeighted()
    datasetsMgr.loadLuminosities() # from lumi.json
    if opts.verbose:
        datasetsMgr.PrintCrossSections()
        datasetsMgr.PrintLuminosities()

    # Print dataset information
    if opts.verbose:
        datasetsMgr.PrintInfo()

    # Check if path exists
    if not os.path.exists(opts.outputDir):
        os.makedirs(opts.outputDir)

    # Get all files under the input pseudo-multicrab 
    src_files = os.listdir(opts.mcrabs[0])
    nDatasets = len(datasetsMgr.getAllDatasets())
    nDirs     = len(opts.mcrabs)

    # For-loop: All files inside the directory (e.g. multicrab.cfg, lumi.json)
    for i, fileName in enumerate(src_files, 1):

        filePath = os.path.join(opts.mcrabs[0], fileName)
        isFile   = os.path.isfile(filePath)

        # If not a file skip 
        if not isFile:
            continue
        else:
            shutil.copy(filePath, opts.outputDir)


    # For-loop: All datasets
    for i, dataset in enumerate(datasetsMgr.getAllDatasets(), 1):
        dsetName  = dataset.getName() 

        # Create new directory with structure of pseudomulticrab
        dirTree = os.path.join(opts.outputDir, dsetName, "res")
        
        # Check if path exists
        if not os.path.exists(dirTree):
            os.makedirs(dirTree)
            
        # Output file Name
        outputFileName = "histograms-%s.root" % (dsetName)
        outputFileName = dirTree + outputFileName

        # Create output root file
        outputFile = ROOT.TFile.Open(outputFileName, "recreate")
            
        # For-loop: All pseudo-multicrabs in list
        for j, dirName in enumerate(opts.mcrabs, 1):
            
            # Get root file from dataset
            dirPath  = os.path.join(dirName, dsetName, "res")
            filePath = "%s/histograms-%s.root" % (dirPath, dsetName)
            
            # Open input root file and change directory
            inputFile = ROOT.TFile.Open(filePath)
            outputFile.cd()

            nKeys = len(inputFile.GetListOfKeys())
            # For-loop: All jeys in ROOT file
            for k, key in enumerate(inputFile.GetListOfKeys(), 1):
                keyName = key.GetName()

                # Inform user of progress                
                msg = "{:<10} {:<2} {:>1} {:<2}  {:<10} {:<2} {:>1} {:<2}  {:<10} {:<2} {:>1} {:<2}".format("%sDataset" % (ShellStyles.HighlightAltStyle()), "%d" % i, "/", "%d" % (nDatasets), "%sPseudomulticrab" % (ShellStyles.NoteStyle()), "%d" % j, "/", "%d" % (nDirs), "%sKey" % (ShellStyles.HighlightStyle()), "%d" % k, "/", "%d%s: " % (nKeys, ShellStyles.NormalStyle()) )
                aux.PrintFlushed(msg, i*j*k==1)        

                # Skip if object already exists
                if (keyName in outputFile.GetListOfKeys()):
                    continue
                
                Verbose("Merging %s" % keyName, False)
                MergeFiles(inputFile.Get(keyName), outputFile, msg,)
        
        Verbose("Writing & closing file %s" % (outputFile.GetName()), True)
        outputFile.Write()
        outputFile.Close()

    print
    Print("Directory %s created" % (len(opts.mcrabs), ShellStyles.SuccessStyle() + opts.outputDir + ShellStyles.NormalStyle()), True)
    return


def MergeFiles(target, parent, msg):
    if not target: 
        return

    # Create directory with target name
    if target.Class().InheritsFrom(ROOT.TDirectory.Class()) :
        
        parent.mkdir(target.GetName())
        dest = parent.Get(target.GetName())

        # Change directory
        dest.cd()

        # For-loop: All keys
        for i, key in enumerate(target.GetListOfKeys(), 1):
            keyName = key.GetName()
            aux.PrintFlushed(msg + keyName, False)
            targets = [MergeFiles(target.Get(keyName), dest, msg)]
        parent.cd()
    else:  # Copy all objects
        if parent: 
            parent.cd()
        clone = None

        if target.Class().InheritsFrom(ROOT.TTree.Class()) :
            clone  = target.CloneTree()
        else : 
            clone  = target.Clone()

        if hasattr(clone, "SetDirectory") : 
            clone.SetDirectory(parent)
        clone.Write()
    return


#================================================================================================ 
# Main
#================================================================================================ 
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
    VERBOSE      = False
    ANALYSISNAME = None
    SEARCHMODE   = "80to1000"
    DATAERA      = "Run2016"
    OPTMODE      = ""
    OUTPUTDIR    = None

    # Define the available script options
    parser = OptionParser(usage="Usage: %prog [options]")

    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=VERBOSE, 
                      help="Enables verbose mode (for debugging purposes) [default: %s]" % VERBOSE)

    parser.add_option("-m", "--mcrabs", dest="mcrabs", action="store", 
                      help="Path to the multicrab directories for input")

    parser.add_option("--analysisName", dest="analysisName", type="string", default=ANALYSISNAME,
                      help="Override default analysisName [default: %s]" % ANALYSISNAME)

    parser.add_option("--searchMode", dest="searchMode", type="string", default=SEARCHMODE,
                      help="Override default searchMode [default: %s]" % SEARCHMODE)

    parser.add_option("--optMode", dest="optMode", type="string", default=OPTMODE, 
                      help="The optimization mode when analysis variation is enabled  [default: %s]" % OPTMODE)

    parser.add_option("--dataEra", dest="dataEra", type="string", default=DATAERA, 
                      help="Override default dataEra [default: %s]" % DATAERA)

    parser.add_option("-o", "--outputDir", dest="outputDir", type="string", default=OUTPUTDIR, 
                      help="Name of output directory [default: %s]" % OUTPUTDIR)

    parser.add_option("-i", "--includeOnlyTasks", dest="includeOnlyTasks", action="store", 
                      help="List of datasets in mcrab to include")

    parser.add_option("-e", "--excludeTasks", dest="excludeTasks", action="store", 
                      help="List of datasets in mcrab to exclude")

    (opts, parseArgs) = parser.parse_args()

    # Require at least two arguments (script-name, path to multicrab)
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    # Store all (comma-separated) pseudomulticrabs in a list
    if opts.mcrabs == None:
        Print("Not enough arguments passed to script execution. Printing docstring & EXIT.")
        parser.print_help()
        sys.exit(1)
    else:
        if "," in opts.mcrabs:
            opts.mcrabs = opts.mcrabs.split(",")    
        else:
            cwd  = os.getcwd()
            dirs = [ name for name in os.listdir(cwd) if os.path.isdir(os.path.join(cwd, name)) ]
            mcrabs = [d for d in dirs if opts.mcrabs in d and "Syst" in d]
            opts.mcrabs = mcrabs

    # Determine analysis type
    analyses = ["SignalAnalysis", "Hplus2tbAnalysis", "FakeBMeasurement"]
    if opts.analysisName == None:
        analysis = opts.mcrabs[0].split("_")[0]
        if analysis not in analyses:
            Print("Invalid analysis %s. EXIT!" % (analysis), True)
            sys.exit()
        else:
            opts.analysisName = analysis

    # For-loop: All pseudomulticrab dirs
    for mcrab in opts.mcrabs:
        if not os.path.exists("%s/multicrab.cfg" % mcrab):
            msg = "No pseudo-multicrab directory found at path '%s'! Please check path or specify it with --mcrab!" % (mcrab)
            raise Exception(ShellStyles.ErrorLabel() + msg + ShellStyles.NormalStyle())
        else:
            msg = "Using pseudo-multicrab directory %s" % (ShellStyles.NoteStyle() + mcrab + ShellStyles.NormalStyle())
            Verbose(msg , True)
            
    # Define name of output directory
    if opts.outputDir == None:
        syst = ""
        m = re.search('_Syst(.+?)_', opts.mcrabs[0])
        if m:
            syst = m.group(1)
        opts.outputDir = opts.mcrabs[0].replace("_Syst" + syst, "")


    newDir = ShellStyles.HighlightAltStyle() + opts.outputDir + ShellStyles.NormalStyle()
    msg = "Merging %d directories into a new directory %s:\n\t%s" % (len(opts.mcrabs), newDir, "\n\t".join(opts.mcrabs) )
    Print(msg, True)

    # Call the main function
    main(opts)
