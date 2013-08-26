#!/usr/bin/env python

'''
+++ DOC STRINGS
Usage:
hplusComparePSets.py -q -m ../FullHplusMass_130328_170951 -c signalAnalysis_cfg.py -r histograms.root -s PsetDiffs.txt -d Run2011AB
or, with verbose
hplusComparePSets.py -v -m ../FullHplusMass_130328_170951 -c signalAnalysis_cfg.py -r histograms.root -s PsetDiffs.txt -d Run2011AB

another example:
hplusComparePSets.py -v -m /mnt/flustre/attikis/multicrab_analysis_v44_4_oldreplica_hltmet_trgSF_muonVeto_130130_145112/ -r histograms.root --dataEra Run2011A

Help:
./hplusComparePSets.py -h
or
./hplusComparePSets.py --help

Description:
This is a simple script that compares the PSets between a ROOT file and a multicrab directory.
The differences are saved to the cwd in the form of a txt file, which by default is named "PSet_Differences.txt".
Additionally, an edmConfigDump is performed for a user-defined python configuration file  ("signalAnalysis_cfg.py" by default)
for the users reference.
'''

######################################################################
# All imported modules
######################################################################
### System modules
import subprocess
import sys
import os
import re
from optparse import OptionParser
import difflib
### HPlus modules
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset

######################################################################
def main():
    '''
    def main():
    '''

    ### Get the user-defined options
    myParser = getUserOptions()
    (options, args) = myParser.parse_args()
    print "+++ OPTIONS:\n    %s" % (options)
    #print "+++ ARGUMENTS: %s" % (args)

    ### Save user-defined (or default) options (if the user fails to provide his own)
    cfgFileName  = options.cfgFileName
    rootFileName = options.rootFileName
    multicrabDir = options.multicrabDir

    ### Get PSets from user-defined python configuration file (using "edmConfigDump" command)
    #EdmCfgDumpPsetsPath = getEdmConfigDumpPsets(options, cfgFileName)

    ### Get PSets from user-defined ROOT file
    RootFilePsetsPath = getRootFilePsets(options, rootFileName )

    ### Get PSets from ROOT files in user-defined multicrab dir 
    MulticrabPsetsPath = getMulticrabPsets(options, multicrabDir)

    ### Compare the PSets from the user-defined ROOT file and Multibrab dir, and write the differences to a file
    ComparePSets(options, RootFilePsetsPath, MulticrabPsetsPath)
    
    return

######################################################################
def getEdmConfigDumpPsets(options, cfgFileName):
    '''
    def getEdmConfigDumpPsets(options, cfgFileName):
    '''

    ### Setup the command to be called by subprocess
    saveFileName = "PSet_EdmConfigDump.txt"
    saveFilePath = os.getcwd() + "/" + saveFileName
    cmsswCmd = "edmConfigDump"
    fullCmd  = cmsswCmd + " " + cfgFileName + " > " + saveFileName

    ### Execute command only if cfgFileName exists and saveFileName does not already exist
    fileExists(cfgFileName , True)
    fileExists(saveFileName, False)

    ### Execute the CMSSW script edmConfigDump on the user-defined python configuration file
    if options.verbose:
        print "+++ VERBOSE: Executing shell command\n    %s" % (fullCmd)
    ### Redirect command  stdout to /dev/null.
    print "+++ Saving PSets from \"edmConfigDump\" of \"%s\" to:\n    \"%s\"" % (cfgFileName, saveFilePath)
    cmdOutput = subprocess.Popen(fullCmd , shell=True, stdout=open(os.devnull, 'wb'))

    if options.verbose:
        print "+++ VERBOSE: Obtained PSets from \"%s\"" % (cfgFileName)

    return saveFilePath

######################################################################
def getMulticrabPsets(options, multicrabDir):
    '''
    def getMulticrabPsets(options, multicrabDir):
    '''

    ### Get the user-defined (or default) data-era
    myDataEra = options.dataEra

    ### Get the ROOT files for all datasets, merge datasets and reorder them
    if options.verbose:
        print "+++ VERBOSE: Obtaining datasets from multicrab directory \"%s\"" % (multicrabDir)
    datasets = dataset.getDatasetsFromMulticrabCfg(directory=multicrabDir, dataEra=myDataEra)

    ### Print PSets used in ROOT-file generation
    saveFileName = "PSet_Multicrab.txt" # + multicrabDir.strip("../") + ".txt"
    saveFilePath = os.getcwd() + "/" + saveFileName

    ### Check that file does not already exist
    fileExists(saveFilePath, False)
    saveFile = open(saveFilePath, "w")
    print "+++ Saving PSets from Multicrab directory \"%s\" to:\n    \"%s\"" % (multicrabDir, saveFilePath)
    saveFile.write(datasets.getSelections())
    saveFile.close()

    if options.verbose:
        print "+++ VERBOSE: Obtained PSets from %s" % (multicrabDir)

    return saveFilePath

######################################################################
def getRootFilePsets(options, rootFileName):
    '''
    def getRootFilePsets(options, rootFileName):
    '''

    ### Get the user-defined (or default) data-era
    myDataEra = options.dataEra

    ### Get the ROOT files for all datasets, merge datasets and reorder them
    if options.verbose:
        print "+++ VERBOSE: Obtaining datasets from ROOT file \"%s\"" % (rootFileName)
    datasets = dataset.getDatasetsFromRootFiles([("Dataset", rootFileName)], dataEra=myDataEra)

    ### Set path for the txt file
    saveFilePath = os.getcwd() + "/" + "PSet_RootFile.txt"

    ### Check that file does not already exist
    fileExists(saveFilePath, False)

    ### Save Psets
    print "+++ Saving PSets from ROOT file \"%s\" to:\n    \"%s\"" % (rootFileName, saveFilePath)
    saveFile = open(saveFilePath, "w")
    saveFile.write(datasets.getSelections()) 
    saveFile.close()
        
    if options.verbose:
        print "+++ VERBOSE: Obtained PSets from %s" % (rootFileName)

    return saveFilePath

######################################################################
def CompareEdmConfigDumpAndRootPSets(options, EdmCfgDumpPsetsPath, MulticrabPsetsPath):
    ''' 
    def CompareEdmConfigDumpAndRootPSets(options, EdmCfgDumpPsetsPath, MulticrabPsetsPath):

    Still under construction. Complications arise due to large diffferences
    in the sturcture/ordering of the \"edmConfigDump\" and the printing of PSets
    from a dataset in a ROOT file.
    '''
    
    print "+++ WARNING: This module is still under construction. Exiting."
    sys.exit()

    EdmCfgDumpPsets = readFile(EdmCfgDumpPsetsPath)
    MulticrabPsets  = readFile(MulticrabPsetsPath)

    ### Loop over the two lists simultaneously
    for i,j in zip(EdmCfgDumpPsets, MulticrabPsets):
        break

    return

######################################################################
def ComparePSets(options, RootFilePsetsPath, MulticrabPsetsPath):
    ''' 
    def CompareRootFilePSets(options, RootFilePsetsPath, MulticrabPsetsPath):
    '''

    ### Read contents of txt file containing the PSets
    RootFilePsets   = readFile(RootFilePsetsPath)
    MulticrabPsets  = readFile(MulticrabPsetsPath)

    ### Save results to a txt file
    saveFileName = options.saveFileName
    saveFilePath = os.getcwd() + "/" + saveFileName
    fileExists(saveFilePath, False)
    saveFile = open(saveFilePath, "w")

    ### Testing 
    diffList1  = []
    diffList2  = []

    # Check for strings in RootFilePsets not found in MulticrabPsets
    for line in RootFilePsets:
        if line not in MulticrabPsets:
            diffList1.append(line)
        else:
            continue

    # Check for strings in MulticrabPsets not found in RootFilePsets
    for line in MulticrabPsets:
        if line not in RootFilePsets:
            diffList2.append(line)
        else:
            continue

    # Get the differences between the two files
    diff=difflib.ndiff(diffList1, diffList2)

    print "+++ Saving differences in PSets to:\n    \"%s\"" % (saveFilePath)
    try:
        while 1:
            saveFile.write(diff.next(),)
            if options.verbose:
                print diff.next(),
    except:
        pass

    saveFile.close()

    return

######################################################################
def readFile(filePath):
    '''
    def readFile(filePath):
    '''

    ### First check that file does exists
    fileExists(filePath, True)
    f = open(filePath, "r")
    fileContentsList = f.readlines()
    f.close()

    return fileContentsList

######################################################################
def fileExists(filePath, bRequirement):
    '''
    def fileExists(filePath, bRequirement):
    '''

    bExists = False
    if os.path.exists(filePath):
        bExists = True
    else:
        bExists = False

    if bRequirement == True and bExists == False:
        print "+++ WARNING: The file \"%s\" does not exist. Exiting." % (filePath)
        print __doc__
        sys.exit()
    elif bRequirement == False and bExists == True:
        print "+++ WARNING: The file \"%s\" already exists. Exiting." % (filePath)
        print __doc__
        sys.exit()
    else:
        return
        
######################################################################
def getUserOptions():
    '''
    def getUserOptions():
    '''
    
    ### Parse the user-defined arguments, and put them into an appropriate format to pass to the readFile(cfgFileName, nLines) function
    parser = OptionParser()
    parser.add_option("-c", "--cfgFileName" , dest = "cfgFileName" , default = "signalAnalysis_cfg.py", help = "PATH of python config file to read", metavar = "CFGFILENAME")
    parser.add_option("-r", "--rootFileName", dest = "rootFileName", default = "histograms.root"      , help = "PATH of Root file to read", metavar = "ROOTFILENAME")
    parser.add_option("-s", "--saveFileName", dest = "saveFileName", default = "PSet_Differences.txt"    , help = "NAME of file for saving the PSet differences", metavar = "SAVEFILENAME")
    parser.add_option("-m", "--multicrabDir", dest = "multicrabDir", default = "../multicrab_XXXXXX_YYYYYY/", help = "PATH to Multicrab dir to read the PSets from", metavar = "MULTICRABDIR")
    parser.add_option("-q", "--quiet", action="store_false", dest = "verbose", default = False, help = "DISABLE verbose (quiet)", metavar = "VERBOSE")
    parser.add_option("-v", "--verbose", action="store_true" , dest = "verbose", default = False, help = "ENABLE vervose (verbose)", metavar = "VERBOSE")
    parser.add_option("-d", "--dataEra", dest = "dataEra", default = "run2011AB", help = "DataEra to be used when looking for PSets", metavar = "DATAERA")
 
    return parser
 
######################################################################
if __name__ == "__main__":
    
    main()
