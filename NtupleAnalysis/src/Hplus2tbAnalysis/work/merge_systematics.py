#!/usr/bin/env python
'''
Description:

Usage:
./merge_systematics.py --mcrabs <list of pseudomulticrabs>
Examples:

Last Used:
./merge_systematics.py --mcrabs Hplus2tbAnalysis_180717_120909,Hplus2tbAnalysis_180717_120519
'''
#================================================================================================ 
# Imports
#================================================================================================ 
import sys
import math
import copy
import os
import shutil #Copy files 
from optparse import OptionParser

import ROOT
ROOT.gROOT.SetBatch(True)
from ROOT import *

import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.counter as counter
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
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
    if 1:
    # For-loop: All optimisation modes
    #for opt in optModes:
        #opts.optMode = opt

        # Setup & configure the dataset manager 
        datasetsMgr = GetDatasetsFromDir(opts)
        datasetsMgr.updateNAllEventsToPUWeighted()
        datasetsMgr.loadLuminosities() # from lumi.json
        if opts.verbose:
            datasetsMgr.PrintCrossSections()
            datasetsMgr.PrintLuminosities()

        # Set/Overwrite cross-sections
        for d in datasetsMgr.getAllDatasets():
            if "ChargedHiggs" in d.getName():
                datasetsMgr.getDataset(d.getName()).setCrossSection(1.0)
               
        # Print dataset information
        datasetsMgr.PrintInfo()

        # Apply TDR style
        style = tdrstyle.TDRStyle()
        style.setOptStat(True)
        style.setGridX(True)
        style.setGridY(False)
        

        #Name of new (merged) pseudomulticrab
        PseudomultName = opts.mcrabs[0]+"_MergedSystematics"

        # Check if path exists
        if not os.path.exists(PseudomultName):
            os.makedirs(PseudomultName)

        #copy all files under input pseudo-multicrab (multicrab.cfg, lumi.json)
        src_files = os.listdir(opts.mcrabs[0])
        for file_name in src_files:
            full_file_name = os.path.join(opts.mcrabs[0], file_name)
            # If is file then copy
            if (os.path.isfile(full_file_name)):
                shutil.copy(full_file_name, PseudomultName)

        # Loop over all datasets
        for dataset in datasetsMgr.getAllDatasets():
            # Create new directory with structure of pseudomulticrab
            destName = "%s/%s/res/" %(PseudomultName,dataset.getName())

            # Check if path exists
            if not os.path.exists(destName):
                os.makedirs(destName)

            # Output file Name
            outputFileName = "histograms-%s.root" % (dataset.getName())  #"histograms-"+dataset.getName()+".root"
            outputFileName = destName+outputFileName
            # Create output root file
            outputFile = ROOT.TFile.Open(outputFileName, "recreate")
            
            # Loop over all pseudo-multicrabs in list
            for m in opts.mcrabs:
                # Get root file from dataset
                path = "%s/%s/res/histograms-%s.root" % (m,dataset.getName(), dataset.getName()) #m+"/"+dataset.getName()+"/res/"+"histograms-"+dataset.getName()+".root"                
                inputFileName = path
                # Open input root file and change directory
                inputFile = ROOT.TFile.Open(inputFileName)
                outputFile.cd()

                for k in inputFile.GetListOfKeys() :
                    if (k.GetName() in outputFile.GetListOfKeys()):
                            continue
                    MergeFiles(inputFile.Get(k.GetName()), outputFile)
            outputFile.Write()
            outputFile.Close()
            
    return


def MergeFiles(target, parent) :
    if not target : return
    #if target = Directory get its content
    if target.Class().InheritsFrom(ROOT.TDirectory.Class()) :
        # Create directory with target name
        parent.mkdir(target.GetName())
        dest = parent.Get(target.GetName())
        # change directory
        dest.cd()
        for k in target.GetListOfKeys():
            targets = [MergeFiles(target.Get(k.GetName()), dest)]
        parent.cd()
    else:  #Copy all objects
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
    ANALYSISNAME = "Hplus2tbAnalysis"
    SEARCHMODE   = "80to1000"
    DATAERA      = "Run2016"
    OPTMODE      = ""
    BATCHMODE    = True
    PRECISION    = 3
    INTLUMI      = -1.0
    SUBCOUNTERS  = False
    LATEX        = False
    MERGEEWK     = False
    URL          = False
    NOERROR      = True
    SAVEDIR      = None
    VERBOSE      = False
    HISTOLEVEL   = "Vital" # 'Vital' , 'Informative' , 'Debug'
    NORMALISE    = False
    FOLDER       = "" #"topSelection_" #"ForDataDrivenCtrlPlots" #"topologySelection_"

    # Define the available script options
    parser = OptionParser(usage="Usage: %prog [options]")

    parser.add_option("-m", "--mcrabs", dest="mcrabs", action="store", 
                      help="Path to the multicrab directories for input")

    parser.add_option("-o", "--optMode", dest="optMode", type="string", default=OPTMODE, 
                      help="The optimization mode when analysis variation is enabled  [default: %s]" % OPTMODE)

    parser.add_option("-b", "--batchMode", dest="batchMode", action="store_false", default=BATCHMODE, 
                      help="Enables batch mode (canvas creation does NOT generate a window) [default: %s]" % BATCHMODE)

    parser.add_option("--analysisName", dest="analysisName", type="string", default=ANALYSISNAME,
                      help="Override default analysisName [default: %s]" % ANALYSISNAME)

    parser.add_option("--intLumi", dest="intLumi", type=float, default=INTLUMI,
                      help="Override the integrated lumi [default: %s]" % INTLUMI)

    parser.add_option("--searchMode", dest="searchMode", type="string", default=SEARCHMODE,
                      help="Override default searchMode [default: %s]" % SEARCHMODE)

    parser.add_option("--dataEra", dest="dataEra", type="string", default=DATAERA, 
                      help="Override default dataEra [default: %s]" % DATAERA)

    parser.add_option("--mergeEWK", dest="mergeEWK", action="store_true", default=MERGEEWK, 
                      help="Merge all EWK samples into a single sample called \"EWK\" [default: %s]" % MERGEEWK)

    parser.add_option("--saveDir", dest="saveDir", type="string", default=SAVEDIR, 
                      help="Directory where all pltos will be saved [default: %s]" % SAVEDIR)

    parser.add_option("--url", dest="url", action="store_true", default=URL, 
                      help="Don't print the actual save path the histogram is saved, but print the URL instead [default: %s]" % URL)
    
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=VERBOSE, 
                      help="Enables verbose mode (for debugging purposes) [default: %s]" % VERBOSE)

    parser.add_option("--histoLevel", dest="histoLevel", action="store", default = HISTOLEVEL,
                      help="Histogram ambient level (default: %s)" % (HISTOLEVEL))

    parser.add_option("-i", "--includeOnlyTasks", dest="includeOnlyTasks", action="store", 
                      help="List of datasets in mcrab to include")

    parser.add_option("-e", "--excludeTasks", dest="excludeTasks", action="store", 
                      help="List of datasets in mcrab to exclude")

    parser.add_option("-n", "--normaliseToOne", dest="normaliseToOne", action="store_true", 
                      help="Normalise the histograms to one? [default: %s]" % (NORMALISE) )

    parser.add_option("--folder", dest="folder", type="string", default = FOLDER,
                      help="ROOT file folder under which all histograms to be plotted are located [default: %s]" % (FOLDER) )

    parser.add_option("--syst", dest="syst", action="store", 
                      help="List with multicrab directories with systematics")

    (opts, parseArgs) = parser.parse_args()

    # Require at least two arguments (script-name, path to multicrab)
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    if opts.mcrabs == None:
        Print("Not enough arguments passed to script execution. Printing docstring & EXIT.")
        parser.print_help()
        sys.exit(1)
    else:
        opts.mcrabs = opts.mcrabs.split(",")
        print opts.mcrabs
        
    for mcrab in opts.mcrabs:
        if not os.path.exists("%s/multicrab.cfg" % mcrab):
            msg = "No pseudo-multicrab directory found at path '%s'! Please check path or specify it with --mcrab!" % (mcrab)
            raise Exception(ShellStyles.ErrorLabel() + msg + ShellStyles.NormalStyle())
        else:
            msg = "Using pseudo-multicrab directory %s" % (ShellStyles.NoteStyle() + mcrab + ShellStyles.NormalStyle())
            Verbose(msg , True)

        
    # Call the main function
    main(opts)

    if not opts.batchMode:
        raw_input("=== merge_systematics.py: Press any key to quit ROOT ...")
