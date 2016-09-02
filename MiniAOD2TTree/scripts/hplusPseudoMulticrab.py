#!/usr/bin/env python
'''
Description:
This script is used to create a pseudo multi-CRAB directory, using an input ROOT file (miniaod2tree.root).
The purpose is primarily to enable the easy testing of local changes to the MiniAOD2TTree code and the 
NtupleAnalysis code using the hplusGenerateDataFormats.py script.
A script execution will thus create an empty multi-CRAB with identical name and structure as those created
by the multicrab.py script. It will contain a single dataset with a single ROOT file under results/ dir, which is 
a mere copy of the file used as input for the script execution (only renamed) to histograms-<dataset>.root.

Usage:
./hplusPseudoMulticrab.py -f ../test/miniaod2tree.root 
OR
./hplusPseudoMulticrab.py -f ../test/miniaod2tree.root -p miniAOD2TTree_Hplus2tbAnalysisSkim_cfg.py
OR
./hplusPseudoMulticrab.py -f ..//test/miniaod2tree.root -r test -v
'''

#================================================================================================
# Import modules
#================================================================================================
import os
import re
import sys
import time
import datetime
import subprocess
from optparse import OptionParser

import HiggsAnalysis.MiniAOD2TTree.tools.git as git
from HiggsAnalysis.MiniAOD2TTree.tools.datasets import *


#================================================================================================ 
# Function Definitions
#================================================================================================ 
def GetSelfName():
    Verbose("GetSelfName()")    
    return __file__.split("/")[-1]


def Verbose(msg, printHeader=False):
    '''
    Calls Print() only if verbose options is set to true.
    '''
    if not opts.verbose:
	return
    Print(msg, printHeader)
    return


def Print(msg, printHeader=True):
    '''
    Simple print function. If verbose option is enabled prints, otherwise does nothing.
    '''
    fName = __file__.split("/")[-1]
    if printHeader:
        print "=== ", fName
    print "\t", msg
    return


def AskUser(msg):
    '''
    Prompts user for keyboard feedback to a certain question. 
    Returns true if keystroke is \"y\", false otherwise.
    '''
    Verbose("AskUser()")
    
    keystroke = raw_input("\t" +  msg + " (y/n): ")
    if (keystroke.lower()) == "y":
        return True
    elif (keystroke.lower()) == "n":
        return False
    else:
        AskUser(msg)
    

def GetCMSSW():
    '''
    Get a command-line-friendly format of the CMSSW version currently use.
    https://docs.python.org/2/howto/regex.html
    '''
    Verbose("GetCMSSW()")
	
    # Get the current working directory
    pwd = os.getcwd()

    # Create a compiled regular expression object
    cmssw_re = re.compile("/CMSSW_(?P<version>\S+?)/")

    # Scan through the string 'pwd' & look for any location where the compiled RE 'cmssw_re' matches
    match = cmssw_re.search(pwd)

    # Return the string matched by the RE. Convert to desirable format
    version = ""
    if match:
	version = match.group("version")
	version = version.replace("_","")
	version = version.replace("pre","p")
	version = version.replace("patch","p")
    return version


def GetAnalysis():
    '''
    Get the analysis type. This will later-on help determine the datasets to be used.
    https://docs.python.org/2/howto/regex.html
    '''
    Verbose("GetAnalysis()")
    
    # Create a compiled regular expression object
    leg_re = re.compile("miniAOD2TTree_(?P<leg>\S+)Skim_cfg.py")

    # Scan through the string 'pwd' & look for any location where the compiled RE 'cmssw_re' matches
    match = leg_re.search(opts.pset)

    # Return the string matched by the RE. Convert to desirable format
    analysis = "DUMMY"
    if match:
	analysis = match.group("leg")
    else:
        raise Exception("Could not determine the analysis type from the PSET \"%s\"" % (opts.pset) )

    return analysis


def AskToContinue(taskDirName, analysis, opts):
    '''
    Inform user of the analysis type and datasets to be user in the multi-CRAB job creation. Offer chance to abort sequence 
    '''
    Verbose("AskToContinue()")

    Print("Creating pseudo multi-CRAB task \"%s\" using the file \"%s\" as input" % (taskDirName, opts.rootFile) )
    #DatasetGroup(analysis).PrintDatasets(False)
    
    AbortTask(keystroke="q")
    return


def AbortTask(keystroke):
    '''
    Give user last chance to abort CRAB task creation.
    '''
    Verbose("AbortTask()")

    message = "=== %s:\n\tPress \"%s\" to abort, any other key to proceed: " % (GetSelfName(), keystroke)

    response = raw_input(message)
    if (response!= keystroke):
        return
    else:
        print "=== %s:\n\tEXIT" % (GetSelfName())
        sys.exit()
    return


def GetTaskDirName(analysis, version, datasets):
    '''
    Get the name of the CRAB task directory to be created. For the user's benefit this
    will include the CMSSW version and possibly important information from
    the dataset used, such as the bunch-crossing time.
    '''
    Verbose("GetTaskDirName()")

    # Constuct basic task directory name
    dirName = "multicrab"
    dirName+= "_"  + analysis
    dirName+= "_v" + version
    
    # Add dataset-specific info, like bunch-crossing info
    bx_re = re.compile("\S+(?P<bx>\d\dns)_\S+")
    match = bx_re.search(datasets[0].URL)
    if match:
	dirName+= "_"+match.group("bx")

    # Append the creation time to the task directory name    
    # time = datetime.datetime.now().strftime("%d%b%Y_%Hh%Mm%Ss")
    time = datetime.datetime.now().strftime("%Y%m%dT%H%M")
    dirName+= "_" + time

    # If directory already exists (resubmission)
    if os.path.exists(opts.dirName) and os.path.isdir(opts.dirName):
	dirName = opts.dirName
    return dirName


def CreateTaskDir(dirName):
    '''
    Create the CRAB task directory and copy inside it the PSET to be used for the CRAB job.
    '''
    Verbose("CreateTaskDir()")
    
    if  os.path.exists(dirName):
        msg = "Cannot create directory \"%s\". It already exists!" % (dirName)
        raise Exception(msg)

    # Create the pseudo multi-CRAB directory
    Verbose("mkidr %s" % (dirName))
    os.mkdir(dirName)

    # Place an empty PSet file inside the pseudo multi-CRAB directory
    cmd = "touch %s" % dirName + "/" + opts.pset
    Verbose(cmd)
    os.system(cmd)

    # Write the commit id, "git status", "git diff" command output the directory created for the multicrab task
    gitFileList = git.writeCodeGitInfo(dirName, False)    
    Verbose("Copied %s to '%s'." % ("'" + "', '".join(gitFileList) + "'", dirName) )
    return


def GetRequestName(dataset):
    '''
    Return the file name and path to an (empty) crabConfig_*.py file where "*" 
    contains the dataset name and other information such as tune, COM, Run number etc..
    of the Data or MC sample used
    '''
    Verbose("GetRequestName()")
    
    # Create compiled regular expression objects
    datadataset_re = re.compile("^/(?P<name>\S+?)/(?P<run>Run\S+?)/")
    mcdataset_re   = re.compile("^/(?P<name>\S+?)/")
    tune_re        = re.compile("(?P<name>\S+)_Tune")
    tev_re         = re.compile("(?P<name>\S+)_13TeV")
    ext_re         = re.compile("(?P<name>_ext\d+)-")
    runRange_re    = re.compile("Cert_(?P<RunRange>\d+-\d+)_")
    # runRange_re    = re.compile("Cert_(?P<RunRange>\d+-\d+)_13TeV_PromptReco_Collisions15(?P<BunchSpacing>\S*)_JSON(?P<Silver>(_\S+|))\.")
    # runRange_re    = re.compile("Cert_(?P<RunRange>\d+-\d+)_13TeV_PromptReco_Collisions15(?P<BunchSpacing>\S*)_JSON")
    # runRange_re    = re.compile("Cert_(?P<RunRange>\d+-\d+)_13TeV_PromptReco_Collisions15_(?P<BunchSpacing>\d+ns)_JSON_v")
    
    # Scan through the string 'dataset.URL' & look for any location where the compiled RE 'mcdataset_re' matches
    match = mcdataset_re.search(dataset.URL)
    if dataset.isData():
	match = datadataset_re.search(dataset.URL)
        
    # Append the dataset name
    if match:
	requestName = match.group("name")

    # Append the Run number (for Data samples only)
    if dataset.isData():
	requestName+= "_"
	requestName+= match.group("run")

    # Append the MC-tune (for MC samples only) 
    tune_match = tune_re.search(requestName)
    if tune_match:
	requestName = tune_match.group("name")

    # Append the COM Energy (for MC samples only) 
    tev_match = tev_re.search(requestName)
    if tev_match:
	requestName = tev_match.group("name")

    # Append the Ext
    ext_match = ext_re.search(dataset.URL)
    if ext_match:
	requestName+=ext_match.group("name")

    # Append the Run Range (for Data samples only)
    if dataset.isData():
	runRangeMatch = runRange_re.search(dataset.lumiMask)
	if runRangeMatch:
	    runRange= runRangeMatch.group("RunRange")
	    runRange = runRange.replace("-","_")
	    #bunchSpace = runRangeMatch.group("BunchSpacing")
	    requestName += "_" + runRange #+ bunchSpace
	    #Ag = runRangeMatch.group("Silver")
	    #if Ag == "_Silver": # Use  chemical element of silver (Ag)
            #    requestName += Ag

    # Finally, replace dashes with underscores    
    requestName = requestName.replace("-","_")

    return requestName


def EnsurePathDoesNotExist(taskDirName, requestName):
    '''
    Ensures that file does not already exist
    '''
    Verbose("EnsurePathDoesNotExist()")
    
    filePath = os.path.join(taskDirName, requestName)
    
    if not os.path.exists(filePath):
	return
    else:
        msg = "File '%s' already exists!" % (filePath)
        if AskUser(msg + " Proceed and overwrite it?"):
            return
	else:
            raise Exception(msg)
    return


def CreateJob(opts, args):
    '''
    Create & submit a CRAB task, using the user-defined PSET and list of datasets.
    '''
    Verbose("CreateJob()")
    
    # Get general info
    version     = GetCMSSW()
    analysis    = GetAnalysis()
    dataset = None
    for d in DatasetGroup("All").GetDatasetList():
        if opts.dataset in d.URL.replace("-", "_"):
            dataset = d
    if dataset == None:
        raise Exception("Could not find dataset object for dataset with name \"%s\"." % (opts.dataset) )
    else:
        datasets= [dataset]

    if opts.dirName == "":
        taskDirName = GetTaskDirName(analysis, version, datasets)
    else:
        taskDirName = opts.dirName

    # Give user last chance to abort
    AskToContinue(taskDirName, analysis, opts)
    
    # Create CRAB task diractory
    CreateTaskDir(taskDirName)
    
    # For-loop: All datasets [always 1 in this case]
    for dataset in datasets:
        
	Verbose("Determining request name for dataset with URL \"%s\"" % (dataset.URL))
        requestName = GetRequestName(dataset)

	Verbose("Creating directory for dataset with request name \"%s\"" % (requestName))
        datasetDir = os.path.join(taskDirName, requestName)
        if os.path.exists(datasetDir) and os.path.isdir(datasetDir):
            raise Exception("Cannot create directory \"%s\". It already exists!" % (datasetDir))
        else:
            os.mkdir(datasetDir)
                
	Verbose("Creating directory structure for dataset with request name \"%s\"" % (requestName))
        dirs = ["results", "inputs"]
        for d in dirs:
            newDir = os.path.join(datasetDir, d)
            if os.path.exists(newDir) and os.path.isdir(newDir):
                raise Exception("Cannot create directory \"%s\". It already exists!" % (newDir))
            else:
                os.mkdir(newDir)

        resultsDir  = os.path.join(datasetDir, "results")
        resultsFile = "histograms-%s.root" % (requestName)
	Verbose("Copying the ROOT file \"%s\" in the directory \"%s\"" % (opts.rootFile, resultsDir))
        cmd = "cp %s %s" % (opts.rootFile, os.path.join(resultsDir, resultsFile) )
	os.system(cmd)

    Print("Pseudo multi-CRAB directory \"%s\" successfully created" % (taskDirName))
    os.system("ls -lt")
    return 0


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

    # Default Values
    VERBOSE = False
    PSET    = "miniAOD2TTree_Hplus2tbAnalysisSkim_cfg.py" # "miniAOD2TTree_SignalAnalysisSkim_cfg.py"
    DIRNAME = ""

    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("-d", "--dataset" , dest="dataset" , default="ChargedHiggs_HplusTB_HplusToTB_M_200", help="Dataset to include in multicrab dir [default: ChargedHiggs_HplusTB_HplusToTB_M_200]")
    parser.add_option("-f", "--rootFile", dest="rootFile", default=None, help="The ROOT file (miniaod2tree.root) to be copied inside the multicrab dir[default: None]")
    parser.add_option("-v", "--verbose" , dest="verbose" , default=VERBOSE, action="store_true", help="Verbose mode for debugging purposes [default: %s]" % (VERBOSE))
    parser.add_option("-a", "--ask"     , dest="ask"     , default=False  , action="store_true", help="Prompt user before executing CRAB commands [defaut: False]")
    parser.add_option("-p", "--pset"    , dest="pset"    , default=PSET   , type="string"      , help="The python cfg file to be used by cmsRun [default: %s]" % (PSET))
    parser.add_option("-r", "--dir"     , dest="dirName" , default=DIRNAME, type="string"      , help="Custom name for CRAB directory name [default: %s]" % (DIRNAME))
    (opts, args) = parser.parse_args()
 
    if opts.rootFile == None:
        raise Exception("Must provide a ROOT file (miniaod2tree.root) as argument!")
    else:
        if os.path.exists(opts.rootFile):
            sys.exit( CreateJob(opts, args) )
        else:
            raise Exception("The ROOT file provided (%s) does not exists!" % (opts.rootFile) )
