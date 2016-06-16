#!/usr/bin/env python
'''
Usage:
multicrabcreate.py -s T2_CH_CERN
multicrabcreate.py -v
multicrabcreate.py -d <multicrab-dir-to-be-resubmitted>

Description:
This script is used to launch multicrab jobs, with certain customisable options.
The file datasets.py is used an an auxiliary file to determine the samples to be processesed.

Launching the command with a multicrab-dir as a parameter:
[username@lxplus0036:test]$ multicrabcreate.py <multicrab_dir> resubmits some crab tasks within the multicrab dir.

Links:
https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3ConfigurationFile
https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookCRAB3Tutorial#Setup_the_environment
'''

#================================================================================================
# USER Options
#================================================================================================
#PSET = "miniAODGEN2TTree_cfg.py"
#PSET = "miniAOD2TTree_TauLegSkim_cfg.py"
#PSET = "miniAOD2TTree_METLegSkim_cfg.py"
#PSET = "miniAOD2TTree_SignalAnalysisSkim_cfg.py"
PSET = "miniAOD2TTree_Hplus2tbAnalysisSkim_cfg.py"


#================================================================================================
# Import modules
#================================================================================================
import os
import re
import sys
import time
import datetime

from optparse import OptionParser
import HiggsAnalysis.MiniAOD2TTree.tools.git as git
from HiggsAnalysis.MiniAOD2TTree.tools.datasets import *
#from datasets import *


#================================================================================================
# Dataset Grouping 
#================================================================================================
datasets = []
#datasets.append('/DYJetsToLL_M-50_13TeV-madgraph-pythia8-tauola_v2/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM')

tauLegDatasets         = []
tauLegDatasets.extend(datasetsMuonData76x)
tauLegDatasets.extend(datasetsMiniAODv2_DY76x)
#tauLegDatasets.extend(datasetsMiniAODv2_Top76x)
#tauLegDatasets.extend(datasetsMiniAODv2_WJets76x)
#tauLegDatasets.extend(datasetsMiniAODv2_QCDMuEnriched76x)
tauLegDatasets.extend(datasetsMiniAODv2_H12576x)

metLegDatasets = []
metLegDatasets.extend(datasetsTauData76x)
metLegDatasets.extend(datasetsMiniAODv2_DY76x)
metLegDatasets.extend(datasetsMiniAODv2_Top76x)
metLegDatasets.extend(datasetsMiniAODv2_WJets76x)
metLegDatasets.extend(datasetsMiniAODv2_QCD76x)

signalAnalysisDatasets = []
signalAnalysisDatasets.extend(datasetsTauData76x)
signalAnalysisDatasets.extend(datasetsMiniAODv2_DY76x)
signalAnalysisDatasets.extend(datasetsMiniAODv2_Top76x)
signalAnalysisDatasets.extend(datasetsMiniAODv2_WJets76x)
signalAnalysisDatasets.extend(datasetsMiniAODv2_Diboson76x)
signalAnalysisDatasets.extend(datasetsMiniAODv2_QCD76x)
signalAnalysisDatasets.extend(datasetsMiniAODv2_SignalTauNu76x)
signalAnalysisDatasets.extend(datasetsMiniAODv2_SignalTB76x)

hplus2tbAnalysisDatasets = []
hplus2tbAnalysisDatasets.extend(datasetsMiniAODv2_TT76x)
hplus2tbAnalysisDatasets.extend(datasetsMiniAODv2_SignalTB76x)


#================================================================================================ 
# Function Definitions
#================================================================================================ 
def Verbose(msg, printHeader=False):
	'''
	Simple print function. If verbose option is enabled prints, otherwise does nothing.
	'''
	if not opts.verbose:
		return

	if printHeader:
		print "=== multicrabcreate.py:"
	print "\t", msg
	return


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
	Get the analysis type. This will later-ono help determine the datasets to be used.
	https://docs.python.org/2/howto/regex.html
	'''
	Verbose("GetAnalysis()")
    
	# Create a compiled regular expression object
	leg_re = re.compile("miniAOD2TTree_(?P<leg>\S+)Skim_cfg.py")

	# Scan through the string 'pwd' & look for any location where the compiled RE 'cmssw_re' matches
	match = leg_re.search(PSET)

	# Return the string matched by the RE. Convert to desirable format
	analysis = "DUMMY"
	if match:
		analysis = match.group("leg")
	return analysis


def GetDatasetList(analysis):
	'''
	Get the list of datasets to be processed, according to the analysis type.
	This will be used to setup the multicrab job accordingly.
	'''
	Verbose("GetDatasetList()")

	if analysis == "SignalAnalysis":
		datasets = signalAnalysisDatasets
	if analysis == "Hplus2tbAnalysis":
		datasets = hplus2tbAnalysisDatasets
	if analysis == "TauLeg":
		datasets = tauLegDatasets
	if analysis == "METLeg":
		datasets = metLegDatasets
	return datasets


def AbortCrabTask(keystroke):
	'''
	Give user last chance to abort CRAB task creation.
	'''
	message = "=== multicrabcreate.py:\n\tPress \"%s\" to abort, any other key to proceed: " % (keystroke)

	response = raw_input(message)
	if (response!= keystroke):
		return
	else:
		print "=== multicrabcreate.py:\n\tEXIT"
		sys.exit()
	return


def AskToContinue(PSET, datasetList, storageSite):
	'''
	Inform user of the analysis type and datasets to be user in the multi-CRAB job creation. Offer chance to abort sequence 
	'''
	Verbose("AskToContinue()")

	print "=== multicrabcreate.py:\n\tCreating CRAB task with PSet \"%s\" and the following datasets:\n\t%s" % (PSET, "\n\t".join(str(d.URL) for d in datasetList) )
	print "=== multicrabcreate.py:\n\tWill submit to Storage Site \"%s\" [User MUST have write access to destination site!]" % (storageSite)
    
	AbortCrabTask(keystroke="q")
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
	time = datetime.datetime.now().strftime("%d%b%Y_%Hh%Mm%Ss")
	# time = datetime.datetime.now().strftime("%Y%m%dT%H%M") #original
	dirName+= "_" + time

	# If directory already exists (resubmission)
	# if len(sys.argv) == 2 and os.path.exists(sys.argv[1]) and os.path.isdir(sys.argv[1]): #original
	if opts.dirName != "" and os.path.isdir(opts.dirName):
		dirName = opts.dirName

	return dirName


def CreateTaskDir(dirName, PSET):
	'''
	Create the CRAB task directory and copy inside it the PSET to be used for the CRAB job.
	'''
	Verbose("CreateTaskDir()")

	# Copy file to be used (and others to be tracked) to the task directory
	cmd = "cp %s %s" %(PSET, dirName)

	if not os.path.exists(dirName):
		os.mkdir(dirName)
		os.system(cmd)

	# Write the commit id, "git status", "git diff" command output the directory created for the multicrab task
	gitFileList = git.writeCodeGitInfo(dirName, False)

	Verbose("Copied %s to '%s'." % ("'" + "', '".join(gitFileList) + "'", dirName) )
	return


def SubmitTaskDir(taskDirName, requestName):
	'''
	Submit a given CRAB task using the specific cfg file.
	'''

	Verbose("SubmitCrabTask()")
	
	outfilePath = os.path.join(taskDirName, "crabConfig_" + requestName + ".py")

	# Submit the CRAB task
	cmd_submit = "crab submit " + outfilePath
	Verbose(cmd_submit)
	os.system(cmd_submit)

	# Rename the CRAB task directory (remove "crab_" from its name)
	cmd_mv = "mv " + os.path.join(taskDirName, "crab_" + requestName) + " " + os.path.join(taskDirName, requestName)
	Verbose(cmd_mv)
	os.system(cmd_mv)
	return


def GetRequestName(dataset):
	'''
	Return the file name and path to an (empty) crabConfig_*.py file where "*" 
	contains the dataset name and other information such as tune, COM, Run number etc..
	of the Data or MC sample used
	'''
                                                                                           
	# Create compiled regular expression objects
	datadataset_re = re.compile("^/(?P<name>\S+?)/(?P<run>Run\S+?)/")
	mcdataset_re   = re.compile("^/(?P<name>\S+?)/")
	tune_re        = re.compile("(?P<name>\S+)_Tune")
	tev_re         = re.compile("(?P<name>\S+)_13TeV")
	ext_re         = re.compile("(?P<name>_ext\d+)-")
	runRange_re    = re.compile("Cert_(?P<RunRange>\d+-\d+)_13TeV_PromptReco_Collisions15(?P<BunchSpacing>\S*)_JSON(?P<Silver>(_\S+|))\.")
	# runRange_re    = re.compile("Cert_(?P<RunRange>\d+-\d+)_13TeV_PromptReco_Collisions15(?P<BunchSpacing>\S*)_JSON")
	# runRange_re    = re.compile("Cert_(?P<RunRange>\d+-\d+)_13TeV_PromptReco_Collisions15_(?P<BunchSpacing>\d+ns)_JSON_v")
	
	# Scan through the string 'dataset.URL' & look for any location where the compiled RE 'mcdataset_re' matches
	match = mcdataset_re.search(dataset.URL)
	if dataset.isData():
		match = datadataset_re.search(dataset.URL)

	if match:
		# Append the dataset name     
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
		if runrangeMatch:
			runRange= runRangeMatch.group("RunRange")
			runRange = runRange.replace("-","_")
			bunchSpace = runrangeMatch.group("BunchSpacing")
			requestName += "_" + runRange + bunchSpace
		Ag = runrangeMatch.group("Silver")
                if Ag == "_Silver": # Use  chemical element of silver (Ag)
			requestName += Ag
#            s = (dataset.URL).split("/")
#            requestName = s[1] + "_" + s[2]

        # Finally, replace dashes with underscores    
        requestName = requestName.replace("-","_")

        #if "ext" in dataset.URL:
        #requestName += "_ext"
	return requestName


def EnsurePathDoesNotExit(taskDirName, requestName):
	'''
	Ensures that file does not already exist
	'''
	filePath = os.path.join(taskDirName, requestName)
    
	if not os.path.exists(filePath):
		return
	else:
		raise Exception("File '%s' already exists!" % (filePath) )
	return


def CreateCfgFile(dataset, taskDirName, requestName, infilePath = "crabConfig.py"):
	'''
	Creates a CRAB-specific configuration file which will be used in the submission
	of a job. The function uses as input a generic cfg file which is then customised
	based on the dataset type used.
	'''
	Verbose("CreateCfgFile()")
	
	outfilePath = os.path.join(taskDirName, "crabConfig_" + requestName + ".py")
    
	# Check that file does not already exist
	EnsurePathDoesNotExit(taskDirName, outfilePath)

	# Open input file (read mode) and output file (write mode)
	fIN  = open(infilePath , "r")
	fOUT = open(outfilePath, "w")

	# Create compiled regular expression objects
	crab_requestName_re = re.compile("config.General.requestName")
	crab_workArea_re    = re.compile("config.General.workArea")
	crab_pset_re        = re.compile("config.JobType.psetName")
	crab_psetParams_re  = re.compile("config.JobType.pyCfgParams")
	crab_dataset_re     = re.compile("config.Data.inputDataset")
	crab_split_re       = re.compile("config.Data.splitting")# = 'FileBased'
	crab_splitunits_re  = re.compile("config.Data.unitsPerJob")
	crab_dbs_re         = re.compile("config.Data.inputDBS")
	crab_storageSite_re = re.compile("config.Site.storageSite") #NEW

	# For-loop: All line of input fine
	for line in fIN:
	    
		# Skip lines whicha are commented out #FIXME
		if line[0] == "#":
			continue
	    
		# Set the "inputDataset" field which specifies the name of the dataset. Can be official CMS dataset or a dataset produced by a user.
		match = crab_dataset_re.search(line)
		if match:
			line = "config.Data.inputDataset = '" + dataset.URL + "'\n"

		# Set the "requestName" field which specifies the request/task name. Used by CRAB to create a project directory (named crab_<requestName>)    
		match = crab_requestName_re.search(line)
		if match:
			line = "config.General.requestName = '" + requestName + "'\n"

		# Set the "workArea" field which specifies the (full or relative path) where to create the CRAB project directory. 
		match = crab_workArea_re.search(line)
		if match:
			line = "config.General.workArea = '" + taskDirName + "'\n"
			
		# Set the "psetName" field which specifies the name of the CMSSW pset_cfg.py file that will be run via cmsRun.
		match = crab_pset_re.search(line)
		if match:
			line = "config.JobType.psetName = '" + PSET  +"'\n"

		# Set the "pyCfgParams" field which contains list of parameters to pass to the pset_cfg.py file.            
		match = crab_psetParams_re.search(line)
		if match:
			line = "config.JobType.pyCfgParams = ['dataVersion=" + dataset.dataVersion +"']\n"

		# Set the "inputDBS" field which specifies the URL of the DBS reader instance where the input dataset is published     
		match = crab_dbs_re.search(line)
		if match:
			line = "config.Data.inputDBS = '" + dataset.DBS + "'\n"

		# Set the "storageSite" field which specifies the destination site for submission [User MUST have write access to destination site!]
		match = crab_storageSite_re.search(line)
		if match:
			line = "config.Site.storageSite = '" + opts.storageSite + "'\n"

		# Only if dataset is real data
		if dataset.isData():

			# Set the "splitting" field which specifies the mode to use to split the task in jobs ('FileBased', 'LumiBased', or 'EventAwareLumiBased') 
			match = crab_split_re.search(line)
			if match:
				line = "config.Data.splitting = 'LumiBased'\n"
				line+= "config.Data.lumiMask = '"+ dataset.lumiMask + "'\n"

			# Set the "unitsPerJob" field which suggests (but not impose) how many files, lumi sections or events to include in each job.
			match = crab_splitunits_re.search(line)	
			if match:
				line = "config.Data.unitsPerJob = 100\n"
		else:
			pass

		# Write line to the output file
		fOUT.write(line)

	# Close input and output files 
	fOUT.close()
	fIN.close()
    
	Verbose("Created CRAB cfg file \"%s\"" % (fOUT.name) )
	return


#================================================================================================
# Main Program
#================================================================================================ 
def main(opts, args):
	
	# Get general info
	version     = GetCMSSW()
	analysis    = GetAnalysis()
	datasets    = GetDatasetList(analysis)
	taskDirName = GetTaskDirName(analysis, version, datasets)

	# Give user last chance to abort
	AskToContinue(PSET, datasets, opts.storageSite)
	
	# Create CRAB task diractory
	CreateTaskDir(taskDirName, PSET)
	
	# For-loop: All datasets
	for dataset in datasets:

		Verbose("Getting request name, creating cfg file && submitting CRAB task for dataset \"%s\"" % (dataset) )
		
		# Create CRAB configuration file for each dataset
		requestName = GetRequestName(dataset)
		
		# Create a CRAB cfg file for each dataset
		CreateCfgFile(dataset, taskDirName, requestName, "crabConfig.py")
		
		
		# Sumbit job for CRAB cfg file
		SubmitTaskDir(taskDirName, requestName)
		
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

    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("-v", "--verbose"    , dest="verbose"    , default=False       , action="store_true", help="Verbose mode")
    parser.add_option("-d", "--dir"        , dest="dirName"    , default=""          , type="string"      , help="Custom name for multiCRAB directory name")
    parser.add_option("-s", "--site"       , dest="storageSite", default="T2_FI_HIP" , type="string"      , help="Site where the output files should be permanently copied to")
    #parser.add_option("-s", "--site"       , dest="storageSite", default="T2_CH_CERN", type="string"      , help="Site where the output files should be permanently copied to")

    (opts, args) = parser.parse_args()
    sys.exit( main(opts, args) )
