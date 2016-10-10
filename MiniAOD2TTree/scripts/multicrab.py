#!/usr/bin/env python
'''
Creation/Submission:
multicrab.py --create -s T2_CH_CERN -p miniAOD2TTree_Hplus2tbAnalysisSkim_cfg.py 
multicrab.py --create -s T3_US_FNALLPC -p miniAOD2TTree_Hplus2tbAnalysisSkim_cfg.py


Re-Create (for example, when you get "Cannot find .requestcache" for a given task):
multicrab.py --create -s T2_CH_CERN -p miniAOD2TTree_Hplus2tbAnalysisSkim_cfg.py -d <task_dir> 
Example:
rm -rf /uscms_data/d3/aattikis/workspace/multicrab/multicrab_Hplus2tbAnalysis_v8019_20161006T1003/<taskDir>
multicrab.py --create -s T3_US_FNALLPC -p miniAOD2TTree_Hplus2tbAnalysisSkim_cfg.py -d /uscms_data/d3/aattikis/workspace/multicrab/multicrab_Hplus2tbAnalysis_v8019_20161006T1003/
(the above will re-create the job just for the dataset <task_dir>)


Check Status:
multicrab.py --status --url --verbose -d <task_dir>


Get Output:
multicrab.py --get --ask -d <task_dir>


Get Logfiles (ROOT files will will be copied. Only available  on EOS):
multicrab.py --log


Get Output (from specific datasets):
multicrab.py --get -d <task_dir> -i <keyword>
multicrab.py --get -d <task_dir> -i QCD


Get Output (from all datasets except a specific datasets):
multicrab.py --get -d <task_dir> -e <keyword>
multicrab.py --get -d <task_dir> -e JetHT


Resubmit Failed Jobs:
multicrab.py --resubmit --ask -d <task_dir>


Kill All Jobs:
multicrab.py --kill -d <task_dir>


Description:
This script is used to create CRAB jobs, with certain customisable options.
It is also used retrieve output and check status of submitted CRAB jobs.
The file datasets.py is used an an auxiliary file to determine the samples to be processesed.
To retrieve some logs which refuse to come out otherwise:
crab log <dir> --command=LCG --checksum=no
crab getoutput <dir> --command=LCG --checksum=no


Hint 1:
To check whether you have write persmissions on a T2 centre use the command
crab checkwrite --site 
For example:
crab checkwrite --site T2_CH_CERN


Hint 2:
To retrieve a range of jobs for a given task:
crab getoutput -d <task_dir> --jobids <comma-separated-list-of-jobs-and/or-job-ranges>


Useful Links:
https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3ConfigurationFile
https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookCRAB3Tutorial#Setup_the_environment
https://github.com/dmwm/CRABClient/tree/master/src/python/CRABClient/Commands
https://github.com/dmwm/CRABClient/blob/be9eebfa41268e836fa186259ef3391f998c8fff/src/python/CRABAPI/RawCommand.py
https://github.com/dmwm/CRABClient/blob/master/src/python/CRABClient/Commands/kill.py
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
import tarfile
from optparse import OptionParser
from collections import OrderedDict
import getpass
import socket

# See: https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRABClientLibraryAPI#The_crabCommand_API
from CRABAPI.RawCommand import crabCommand
from CRABClient.UserUtilities import setConsoleLogLevel
from CRABClient.UserUtilities import getUsernameFromSiteDB

# See: https://github.com/dmwm/CRABClient/blob/master/src/python/CRABClient/ClientUtilities.py
from CRABClient.ClientUtilities import LOGLEVEL_MUTE
from CRABClient.UserUtilities import getConsoleLogLevel

import HiggsAnalysis.MiniAOD2TTree.tools.git as git
from HiggsAnalysis.MiniAOD2TTree.tools.datasets import *


#================================================================================================ 
# Class Definition
#================================================================================================ 
class colors:
    # http://stackoverflow.com/questions/15580303/python-output-complex-line-with-floats-colored-by-value
    colordict = {
                'RED'     :'\033[91m',
                'GREEN'   :'\033[92m',
                'BLUE'    :'\033[34m',
                'GRAY'    :'\033[90m',
                'WHITE'   :'\033[00m',
                'ORANGE'  :'\033[33m',
                'CYAN'    :'\033[36m',
                'PURPLE'  :'\033[35m',
                'LIGHTRED':'\033[91m',
                'PINK'    :'\033[95m',
                'YELLOW'  :'\033[93m',
                }
    if sys.stdout.isatty():
        RED      = colordict['RED']
        GREEN    = colordict['GREEN']
        BLUE     = colordict['BLUE']
        GRAY     = colordict['GRAY']
        WHITE    = colordict['WHITE']
        ORANGE   = colordict['ORANGE']
        CYAN     = colordict['CYAN']
        PURPLE   = colordict['PURPLE']
        LIGHTRED = colordict['LIGHTRED']
        PINK     = colordict['PINK']
        YELLOW   = colordict['YELLOW']
    else:
        RED, GREEN, BLUE, GRAY, WHITE, ORANGE, CYAN, PURPLE, LIGHTRED, PINK, YELLOW = '', '', '', '', '', '', '', '', '', '', ''


#================================================================================================ 
# Class Definition
#================================================================================================ 
class Report:
    def __init__(self, name, allJobs, retrieved, running, finished, failed, transferring, retrievedLog, retrievedOut, eosLog, eosOut, status, dashboardURL):
        '''
        Constructor 
        '''
        Verbose("class Report:__init__()")
        self.name            = name
        self.allJobs         = str(allJobs)
        self.retrieved       = str(retrieved)
        self.running         = str(running)
        self.dataset         = self.name.split("/")[-1]
        self.dashboardURL    = dashboardURL
        self.status          = self.GetTaskStatusStyle(status)
        self.finished        = finished
        self.failed          = failed
        self.transferring    = transferring
        self.retrievedLog    = retrievedLog
        self.retrievedOut    = retrievedOut
        self.eosLog          = eosLog
        self.eosOut          = eosOut
        return


    def Print(self, printHeader=True):
        '''
        Simple function to print report.
        '''
        name = os.path.basename(self.name)
        while len(name) < 30:
            name += " "

	fName = GetSelfName()
	cName = self.__class__.__name__
        name  = fName + ": " + cName
        if printHeader:
            print "=== ", name
        msg  = '{:<20} {:<40}'.format("\t %sDataset"           % (colors.WHITE) , ": " + self.dataset)
        msg += '\n {:<20} {:<40}'.format("\t %sRetrieved Jobs" % (colors.WHITE) , ": " + self.retrieved + " / " + self.allJobs)
        msg += '\n {:<20} {:<40}'.format("\t %sStatus"         % (colors.WHITE) , ": " + self.status)
        msg += '\n {:<20} {:<40}'.format("\t %sDashboard"      % (colors.WHITE) , ": " + self.dashboardURL)
        print msg
        return
    

    def GetURL():
        Verbose("GetURL()")
        return self.dashboardURL


    def GetTaskStatusStyle(self, status):
        '''
        NEW, RESUBMIT, KILL: Temporary statuses to indicate the action ('submit', 'resubmit' or 'kill') that has to be applied to the task.
        QUEUED: An action ('submit', 'resubmit' or 'kill') affecting the task is queued in the CRAB3 system.
        SUBMITTED: The task was submitted to HTCondor as a DAG task. The DAG task is currently running.
        SUBMITFAILED: The 'submit' action has failed (CRAB3 was unable to create a DAG task).
        FAILED: The DAG task completed all nodes and at least one is a permanent failure.
        COMPLETED: All nodes have been completed
        KILLED: The user killed the task.
        KILLFAILED: The 'kill' action has failed.
        RESUBMITFAILED: The 'resubmit' action has failed.
        '''
        Verbose("GetTaskStatusStyle()", True)
        
        # Remove all whitespace characters (space, tab, newline, etc.)
        status = ''.join(status.split())
        if status == "NEW":
            status = "%s%s%s" % (colors.BLUE, status, colors.WHITE)
        elif status == "RESUBMIT":
            status = "%s%s%s" % (colors.BLUE, status, colors.WHITE)
        elif status == "QUEUED": 
            status = "%s%s%s" % (colors.GRAY, status, colors.WHITE)            
        elif status == "SUBMITTED":
            status = "%s%s%s" % (colors.BLUE, status, colors.WHITE)
        elif status == "SUBMITFAILED": 
            status = "%s%s%s" % (colors.RED, status, colors.WHITE)
        elif status == "FAILED": 
            status = "%s%s%s" % (colors.RED, status, colors.WHITE)
        elif status == "COMPLETED":
            status = "%s%s%s" % (colors.GREEN, status, colors.WHITE)
        elif status == "KILLED":
            status = "%s%s%s" % (colors.ORANGE, status, colors.WHITE)
        elif status == "KILLFAILED":
            status = "%s%s%s" % (colors.ORANGE, status, colors.WHITE)
        elif status == "RESUBMITFAILED": 
            status = "%s%s%s" % (colors.ORANGE, status, colors.WHITE)
        elif status == "?": 
            status = "%s%s%s" % (colors.PINK, status, colors.WHITE)
        elif status == "UNDETERMINED": 
            status = "%s%s%s" % (colors.CYAN, status, colors.WHITE)
        elif status == "UNKNOWN": 
            status = "%s%s%s" % (colors.LIGHTRED, status, colors.WHITE)
        else:
            raise Exception("Unexpected task status \"%s\"." % (status) )

        return status


#================================================================================================ 
# Function Definitions
#================================================================================================ 
def AskUser(msg, printHeader=False):
    '''
    Prompts user for keyboard feedback to a certain question. 
    Returns true if keystroke is \"y\", false otherwise.
    '''
    Verbose("AskUser()", printHeader)
    
    keystroke = raw_input("\t" +  msg + " (y/n): ")
    if (keystroke.lower()) == "y":
        return True
    elif (keystroke.lower()) == "n":
        return False
    else:
        AskUser(msg)
    

def GetHostname():
    return socket.gethostname()


def GetTaskStatusBool(datasetPath):
    '''
    Check the crab.log for the given task to determine the status.
    If the the string "Done" is found inside skip it.
    '''
    Verbose("GetTaskStatusBool()", True)
    crabLog      = os.path.join(datasetPath,"crab.log")
    stringToGrep = "Done"
    cmd          = "grep '%s' %s" % (stringToGrep, crabLog)

    Verbose(cmd)
    if os.system(cmd) == 0:
        Verbose("DONE! Skipping ...")
        return True 
    return False


def GetTaskDashboardURL(datasetPath):
    '''
    Call the "grep" command to look for the dashboard URL from the crab.log file 
    of a given dataset. It uses as input parameter the absolute path of the task dir (datasetPath)
    '''
    Verbose("GetTaskDashboardURL()")
    
    # Variable Declaration
    crabLog      = os.path.join(datasetPath, "crab.log")
    grepFile     = os.path.join(datasetPath, "grep.tmp")
    stringToGrep = "Dashboard monitoring URL"
    cmd          = "grep '%s' %s > %s" % (stringToGrep, crabLog, grepFile )
    dashboardURL = "UNKNOWN"

    # Execute the command
    if os.system(cmd) == 0:
        
        if os.path.exists( grepFile ):
            results      = [i for i in open(grepFile, 'r').readlines()]
            dashboardURL = FindBetween( results[0], "URL:\t", "\n" )
            Verbose("Removing temporary file \"%s\"" % (grepFile), False)
            os.system("rm -f %s " % (grepFile) )
        else:
            raise Exception("File \"%s\" not found!" % (grepFile) )
    else:
        raise Exception("Could not execute command \"%s\"" % (cmd) )
    return dashboardURL


def GetTaskStatus(datasetPath):
    '''
    Call the "grep" command to look for the "Task status" from the crab.log file 
    of a given dataset. It uses as input parameter the absolute path of the task dir (datasetPath)
    '''
    Verbose("GetTaskStatus()", True)
    
    # Variable Declaration
    crabLog      = os.path.join(datasetPath, "crab.log")
    grepFile     = os.path.join(datasetPath, "grep.tmp")
    stringToGrep = "Task status:"
    cmd          = "grep '%s' %s > %s" % (stringToGrep, crabLog, grepFile )
    status       = "UNKNOWN"
    
    if not os.path.exists( crabLog ):
        raise Exception("File \"%s\" not found!" % (crabLog) )

    # Execute the command
    if os.system(cmd) == 0:

        if os.path.exists( grepFile ):
            results = [i for i in open(grepFile, 'r').readlines()]
            status  = FindBetween( results[-1], stringToGrep, "\n" )
            Verbose("Removing temporary file \"%s\"" % (grepFile), False)
            os.system("rm -f %s " % (grepFile) )
        else:
            raise Exception("File \"%s\" not found!" % (grepFile) )
    else:
        raise Exception("Could not execute command \"%s\"" % (cmd) )
    return status


def GetTaskReports(datasetPath, opts):
    '''
    Execute "crab status", get task logs and output. 
    Resubmit or kill task according to user options.
    '''
    Verbose("GetTaskReports()", True)

    report = None
    
    # Get all files under <dataset_dir>/results/
    files = Execute("ls %s" % os.path.join( datasetPath, "results") )

    Verbose("crab status --dir=%s" % (GetLast2Dirs(datasetPath)), False)
    try:
        d = GetBasename(datasetPath)

        # Execute "crab status --dir=datasetPath"
        Verbose("Getting task status", False)
        result = crabCommand('status', dir=datasetPath)
        Verbose("Calling crab --status for dataset %s returned %s" % (d, result) )
    
        # Get CRAB task status
        status = GetTaskStatus(d).replace("\t", "")

        # Get CRAB task dashboard URL
        dashboardURL = GetTaskDashboardURL(d)

        # Assess JOB success/failure for task
        Verbose("Retrieving files (1/2)", True)
        running, finished, transferring, failed, retrievedLog, retrievedOut, eosLog, eosOut = RetrievedFiles(datasetPath, result, dashboardURL, False, opts)

        # Get the task logs & output ?        
        Verbose("Getting task logs", True)
        GetTaskLogs(datasetPath, retrievedLog, finished)

        # Get the task output
        Verbose("Getting task output")
        GetTaskOutput(datasetPath, retrievedOut, finished)

        # Resubmit task if failed jobs found
        Verbose("Resubmitting failed tasks")
        ResubmitTask(datasetPath, failed)

        # Kill task which are active
        Verbose("Killing active tasks")
        KillTask(datasetPath)
            
        # Assess JOB success/failure for task (again)
        Verbose("Retrieving Files (2/2)")
        running, finished, transferring, failed, retrievedLog, retrievedOut, eosLog, eosOut = RetrievedFiles(datasetPath, result, dashboardURL, True, opts)
        retrieved = min(finished, retrievedLog, retrievedOut)
        alljobs   = len(result['jobList'])        

        # Append the report
        Verbose("Appending Report")
        report = Report(datasetPath, alljobs, retrieved, running, finished, failed, transferring, retrievedLog, retrievedOut, eosLog, eosOut, status, dashboardURL)

        # Determine if task is DONE or not
        Verbose("Determining if Task is DONE")
        if retrieved == alljobs and retrieved > 0:
            absolutePath = os.path.join(datasetPath, "crab.log")
            os.system("sed -i -e '$a\DONE! (Written by multicrabCheck.py)' %s" % absolutePath )

    # Catch exceptions (Errors detected during execution which may not be "fatal")
    except:
        msg = sys.exc_info()[1]
        report = Report(datasetPath, "?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?") 
        Print("crab status failed with message \"%s\". Skipping ..." % ( msg ), True)
    return report


def CheckTaskReport(taskDir, jobId,  opts):
    '''
    Probes the log-file tarball for a given jobId to 
    determine the job status or exit code.
    '''
    Verbose("CheckTaskReport()", True)

    filePath    = os.path.join(taskDir, "results", "cmsRun_%i.log.tar.gz" % jobId)
    exitCode_re = re.compile("process\s+id\s+is\s+\d+\s+status\s+is\s+(?P<exitcode>\d+)")

    # Ensure file is indeed a tarfile 
    if tarfile.is_tarfile(filePath):

        # Open the tarball
        fIN = tarfile.open(filePath)
        log_re = re.compile("cmsRun-stdout-(?P<job>\d+)\.log")

        # For-loop: All files inside tarball
        for member in fIN.getmembers():

            # Extract the log file
            logfile = fIN.extractfile(member)  
            match   = log_re.search(logfile.name)

            # Regular Expression match for log-file
            if match:
                # For-loop: All lines of log-file
                for line in reversed(logfile.readlines()):

                    # Search for exit code
                    exitMatch = exitCode_re.search(line)

                    # If exit code found, return the value
                    if exitMatch:
			return int(exitMatch.group("exitcode"))
    return -1


def CheckTaskReports(datasetPath):
    '''
    Opening crab logs to find out if they really are ok
    '''
    exitCodeJobs = []
    exitCode_re = re.compile("process\s+id\s+is\s+\d+\s+status\s+is\s+(?P<exitcode>\d+)")
    # Get all files under <dataset_dir>/results/
    files = Execute("ls %s" % os.path.join( datasetPath, "results") )
    tar_re = re.compile("cmsRun_(?P<job>\d+)\.log\.tar\.gz")
    for f in files:
	tarmatch = tar_re.search(f)
	if tarmatch:
            tarFile = os.path.join(datasetPath, "results", f)
            if tarfile.is_tarfile(tarFile):
                fIN = tarfile.open(tarFile)
                log_re = re.compile("cmsRun-stdout-(?P<job>\d+)\.log")
                for member in fIN.getmembers():
                    logfile = fIN.extractfile(member)
                    match = log_re.search(logfile.name)
                    if match:
                        for line in reversed(logfile.readlines()):
                            exitMatch = exitCode_re.search(line)
                            if exitMatch:
                                exitCode = int(exitMatch.group("exitcode"))
                                if not exitCode == 0:
                                    exitCodeJobs.append(int(tarmatch.group("job")))
                                break
    return exitCodeJobs
	

def GetTaskLogs(taskPath, retrievedLog, finished):
    '''
    If the number of retrieved logs files is smaller than the number of finished jobs,
    execute the CRAB command "getlog" to retrieve all unretrieved logs files.
    '''
    Verbose("GetTaskLogs()")
    
    if retrievedLog == finished:
        return
        
    if opts.get or opts.log:
        Verbose("Retrieved logs (%s) < finished (%s). Retrieving CRAB logs ..." % (retrievedLog, finished) )
        Touch(taskPath)
        #dummy = crabCommand('getlog', 'command=LCG', 'checksum=no', dir=taskPath) # Produces Warning: 'crab getlog' command takes no arguments, 2 given
        dummy = crabCommand('getlog', dir=taskPath)
        # crab log <dir> --command=LCG --checksum=no #fixme: add support?
    else:
        Verbose("Retrieved logs (%s) < finished (%s). To retrieve CRAB logs relaunch script with --get option." % (retrievedLog, finished) )
    return


def GetTaskOutput(taskPath, retrievedOut, finished):
    '''
    If the number of retrieved output files is smaller than the number of finished jobs,
    execute the CRAB command "getoutput" to retrieve all unretrieved output files.
    '''
    Verbose("GetTaskOutput()")
    
    if retrievedOut == finished:
        return
    
    if opts.get:
        if opts.ask:
            if AskUser("Retrieved output (%s) < finished (%s). Retrieve CRAB output?" % (retrievedOut, finished) ):
                dummy = crabCommand('getoutput', dir=taskPath)            
                Touch(taskPath)
            else:
                return
        else:
            Verbose("Retrieved output (%s) < finished (%s). Retrieving CRAB output ..." % (retrievedOut, finished) )
            dummy = crabCommand("getoutput", dir=taskPath)
            Touch(taskPath)
    else:
        Verbose("Retrieved output (%s) < finished (%s). To retrieve CRAB output relaunch script with --get option." % (retrievedOut, finished) )

    return


def ResubmitTask(taskPath, failed):
    '''
    If the number of failed jobs is greater than zero, 
    execute the CRAB command "resubmit" to resubmit all failed jobs.
    '''
    Verbose("ResubmitTask()")
    
    if failed == 0:
        return

    if not opts.resubmit:
        return

    joblist = JobList(failed)
    
    # Sanity check
    if len(joblist) < 1:
        return

    if opts.ask:
        if AskUser("Resubmit task \"%s\"?" % (GetLast2Dirs(taskPath)) ):
            dummy = crabCommand('resubmit', dir=taskPath)
        else:
            return
    else:
        taskName = os.path.basename(taskPath)
        Print("Found %s failed jobs! Resubmitting ..." % (len(joblist) ) )
        #os.system("crab resubmit %s --jobids=%s --force" % (taskPath,joblist) )
        Print("crab resubmit %s --jobids %s" % (taskName, ",".join(joblist) ) )
        result = crabCommand('resubmit', jobids=joblist, dir=taskPath)
        Verbose("Calling crab resubmit %s --jobids %s returned" % (taskName, ",".join(joblist), result ) )

    return


def KillTask(taskPath):
    '''
    If the number of failed jobs is greater than zero, 
    execute the CRAB command "resubmit" to resubmit all failed jobs.
    '''
    Verbose("KillTask()")
    
    if not opts.kill:
        return
    
    taskStatus = GetTaskStatus(taskPath)
    taskStatus = taskStatus.replace("\t", "")
    forbidden  = ["KILLED", "UNKNOWN", "DONE", "COMPLETED", "QUEUED"]
    if taskStatus in forbidden:
        Print("Cannot kill a task if it is in the \"%s\" state. Skipping ..." % (taskStatus) )
        return
    else:
        Print("Killing jobs ...")
    
    if opts.ask:
        if AskUser("Kill task \"%s\"?" % (GetLast2Dirs(taskPath)) ):
            dummy = crabCommand('kill', dir=taskPath)
        else:
            pass
    else:
        dummy = crabCommand('kill', dir=taskPath)
    return


def FindBetween(myString, first, last ):
    Verbose("FindBetween()")

    try:
        start = myString.index( first ) + len( first )
        end   = myString.index( last, start )
        return myString[start:end]
    except ValueError:
        return ""


def FindBetweenR(myString, first, last ):
    Verbose("FindBetweenR()")
    
    try:
        start = myString.rindex( first ) + len( first )
        end   = myString.rindex( last, start )
        return myString[start:end]
    except ValueError:
        return ""
    

def GetMulticrabAbsolutePaths(dirs):
    Verbose("GetMulticrabAbsolutePaths()")
    
    datasetdirs = []
    # For-loop: All CRAB dirs (relative paths)
    for d in dirs:
        # Get absolute paths
        if os.path.exists(d) and os.path.isdir(d):
            datasetdirs.append( os.path.abspath(d) )

    if len(dirs) == 0:
        datasetdirs.append(os.path.abspath("."))
    return datasetdirs


def GetDatasetAbsolutePaths(datasetdirs):
    Verbose("GetDatasetAbsolutePaths()")
    
    datasets = []
    # For-loop: All CRAB dirs (absolute paths)
    for d in datasetdirs:

        if os.path.exists( os.path.join(d, "results") ):
            datasets.append(d)

        # Get the contents of this directory
        cands = Execute("ls -tr %s"%d)

        # For-loop: All directory contents
        for c in cands:
            path = os.path.join(d, c)
            # Get all dataset directories 
            if os.path.exists( os.path.join(path, "results") ):
                datasets.append(path)
    return datasets


def GetDatasetBasenames(datasets):
    Verbose("GetDatasetBasenames()", True)
    
    basenames = []
    for d in datasets:
        basenames.append( GetBasename(d) )
    return basenames


def GetBasename(fullPath):
    Verbose("GetBasename()")
    return os.path.basename(fullPath)


def GetRegularExpression(arg):
    Verbose("GetRegularExpression()", True)
    if isinstance(arg, basestring):
        arg = [arg]
    return [re.compile(a) for a in arg]


def GetIncludeExcludeDatasets(datasets, opts):
    '''
    Does nothing by default, unless the user specifies a dataset to include (--includeTasks <datasetNames>) or 
    to exclude (--excludeTasks <datasetNames>) when executing the script. This function filters for the inlcude/exclude
    datasets and returns the lists of datasets and baseNames to be used further in the program.
    '''
    Verbose("GetIncludeExcludeDatasets()", True)
    
    # Initialise lists
    newDatasets  = []

    # Exclude datasets
    if opts.excludeTasks != "None":
        tmp = []
        exclude = GetRegularExpression(opts.excludeTasks)

        for d in datasets:            
            task  = GetBasename(d) 
            found = False

            for e_re in exclude:
                if e_re.search(task):
                    found = True
                    break
            if found:
                continue
            newDatasets.append(d)
        return newDatasets

    # Include datasets
    if opts.includeTasks != "None":
        tmp = []
        include = GetRegularExpression(opts.includeTasks)

        for d in datasets:
            task  = GetBasename(d)
            found = False

            for i_re in include:
                if i_re.search(task):
                    found = True
                    break
            if found:
                newDatasets.append(d)
        return newDatasets

    return datasets

    
def GetLast2Dirs(datasetPath):
    Verbose("GetLast2Dirs()")
    last2Dirs = datasetPath.split("/")[-2]+ "/" + datasetPath.split("/")[-1]
    return last2Dirs


def CheckJob(opts, args):
    '''
    Check status, retrieve, resubmit, kill CRAB tasks.
    '''
    Verbose("CheckJob()", True)

    # Force crabCommand to stay quite
    if not opts.verbose:
        setConsoleLogLevel(LOGLEVEL_MUTE)

    # Retrieve the current crabCommand console log level:
    crabConsoleLogLevel = getConsoleLogLevel()
    Verbose("The current \"crabCommand\" console log level is set to \"%s\"" % (crabConsoleLogLevel), True)
    
    # Get the paths for the datasets (absolute paths)
    datasets = GetDatasetsPaths(opts)
    if len(datasets) < 1:
        Print("Found %s CRAB tasks under %s! Exit .." % (opts.dirName) )
        return
    else:
        Verbose("Working with %s CRAB task directories:\n\t%s" % ( len(datasets), "\n\t".join( GetDatasetBasenames(datasets) ) ), True)

    # Create a dictionary to map TaskName <-> CRAB Report
    reportDict = GetCrabReportDictionary(datasets)


    # Print a summary table with information on each CRAB Task
    PrintTaskSummary(reportDict)
    return


def GetCrabReportDictionary(datasets):
    '''
    Loops over all datasets paths. 
    Retrieves the report object for the given task
    and saves it into a dictionary, thus mapping the
    task name (basename of dataset path) to the CRAB 
    report for that task.    
    '''
    Verbose("GetCrabReportDictionary()", True)

    reportDict = {}
    # For-loop: All (absolute) paths of the datasets
    for index, d in enumerate(datasets):
        
        Verbose("%s (%s/%s)" % ( GetLast2Dirs(d), index+1, len(datasets) ), True)

        # Check if task is in "DONE" state
        if GetTaskStatusBool(d):
            continue
        
        # Get the CRAB task report & add to dictionary (retrieves job output!)
        report = GetTaskReports(d, opts)
        reportDict[d.split("/")[-1]] = report

    return reportDict

    
def PrintTaskSummary(reportDict):
    '''
    Print a summary table of all submitted tasks with their information.
    The purpose it to easily determine which jobs are done, running and failed.
    '''
    Verbose("PrintTaskSummary()")
    
    reports  = []
    msgAlign = "{:<3} {:<55} {:^20} {:^10} {:^10} {:^10} {:^10} {:^10} {:^10} {:^10} {:^10} {:^10}"
    header   = msgAlign.format("#", "Dataset", "%s%s%s" % (colors.WHITE, "Status", colors.WHITE), "All", "Running", "Failed", "Transfer", "Finished", "Logs", "Output", "Logs (EOS)", "Output (EOS)" )
    hLine    = "="*len(header)
    reports.append(hLine)
    reports.append(header)
    reports.append(hLine)
    

    # Alphabetical sorting of tasks
    ReportDict = OrderedDict(sorted(reportDict.items(), key=lambda t: t[0]))

    # For-loop: All datasets (key) and corresponding status (value)
    for i, dataset in enumerate(ReportDict):
        report     = reportDict[dataset]
        status     = report.status
        allJobs    = report.allJobs
        running    = report.running
        finished   = report.finished
        transfer   = report.transferring
        failed     = len(report.failed)
        rLogs      = report.retrievedLog
        rOutput    = report.retrievedOut
        rLogsEOS   = report.eosLog
        rOutputEOS = report.eosOut
        line       = msgAlign.format(i+1, dataset, status, allJobs, running, failed, transfer, finished, rLogs, rOutput, rLogsEOS, rOutputEOS)
        reports.append(line)
    reports.append(hLine)
    
    # For-loop: All lines in report table
    for r in reports:
        print r
    return


def JobList(jobs):
    joblist = ""
    for i,e in enumerate(sorted(jobs)):
        joblist += str(e)
        if i < len(jobs)-1:
            joblist += ","
    return joblist


def PrintExitCodeSummary(exitCodeJobs):
    print "Jobs with problems"
    for k in exitCodeJobs.keys():
        if not exitCodeJobs[k] == None and len(exitCodeJobs[k]) > 0:
            joblist = JobList(exitCodeJobs[k])
            print "        ",os.path.basename(k)," jobs with problems"
            print "         crab resubmit %s --jobids %s --force"%(os.path.basename(k),joblist)


def GetEOSDir(taskDir, opts):
    '''
    Converts the taskDir into the EOS path equivalent
    '''
    Verbose("GetEOSDir()")
    
    if not opts.filesInEOS:
        return ""

    tmpDirEOS  = ConvertPathToEOS(taskDir, opts) 
    taskName   = os.path.basename(taskDir)
    taskDirEOS = WalkEOSDir(taskName, tmpDirEOS, opts)
    Verbose("The EOS dir is \"%s\"." % (taskDirEOS) )
    return taskDirEOS


def RetrievedFiles(taskDir, crabResults, dashboardURL, printTable, opts):
    '''
    Determines whether the jobs Finished (Success or Failure), and whether 
    the logs and output files have been retrieved. Returns all these in form
    of lists. The list of tuple crabResults contains the jobId and its status.
    For example:
    crabResults = [['finished', 1], ['finished', 2], ['finished', 3] ]
    '''
    Verbose("RetrievedFiles()", True)
    
    # Initialise variables
    retrievedLog = 0
    retrievedOut = 0
    eosLog       = 0
    eosOut       = 0
    finished     = 0
    failed       = []
    transferring = 0
    running      = 0
    idle         = 0
    unknown      = 0
    dataset      = taskDir.split("/")[-1]
    nJobs        = len(crabResults['jobList'])
    missingOuts  = []
    missingLogs  = []

    # For-loop:All CRAB results
    for index, r in enumerate(crabResults['jobList']):
        
        # Get the job ID and status
        jobStatus = r[0]
        jobId     = r[1]

        Verbose("Investigating jobId=\"%s\" with status=\"%s\"" % (jobId, jobStatus))
        # Assess the jobs status individually
        if jobStatus == 'finished':
            finished += 1

            # Count Output & Logfiles (EOS)
            if opts.filesInEOS:
                taskDirEOS  = GetEOSDir(taskDir, opts)    
                foundLogEOS = ExistsEOS(taskDirEOS, "log", "cmsRun_%i.log.tar.gz" % jobId, opts)
                foundOutEOS = ExistsEOS(taskDirEOS, ""   , "miniaod2tree_%i.root" % jobId, opts)
                Verbose("foundLogEOS=%s , foundOutEOS=%s" % (foundLogEOS, foundOutEOS))
                if foundLogEOS:
                    eosLog += 1
                if foundOutEOS:
                    eosOut += 1
            else:
                pass
                
            # Count Output & Logfiles (local)
            foundLog = Exists(taskDir, "cmsRun_%i.log.tar.gz" % jobId) 
            foundOut = Exists(taskDir, "miniaod2tree_%i.root" % jobId)
            if foundLog:
                retrievedLog += 1
                exitCode = CheckTaskReport(taskDir, jobId, opts)
                if not exitCode == 0:
                    Verbose("Found failed job for task=\"%s\" with jobId=\"%s\" and exitCode=\"%s\"" % (taskDir, jobId, exitCode) )
                    failed.append( jobId )                    
            if foundOut:
                retrievedOut += 1
            if foundLog and not foundOut:
                missingOuts.append( jobId )
            if foundOut and not foundLog:
                missingLogs.append( jobId )
        elif jobStatus == 'failed':
            failed.append( jobId )
        elif jobStatus == 'transferring':
            transferring += 1 
        elif jobStatus == 'idle':
            idle += 1 
        elif jobStatus == 'running':
            running+= 1 
        else:
            unknown+= 1 
    failed = list(set(failed))
    
    # Print results in a nice table
    reportTable = GetReportTable(taskDir, nJobs, running, transferring, finished, unknown, failed, idle, retrievedLog, retrievedOut, eosLog, eosOut)
    if printTable:
        for r in reportTable:
            Print(r, False)
        print

    # Sanity check
    status = GetTaskStatus(taskDir).replace("\t", "")
    if opts.verbose and status == "COMPLETED":
        if len(missingLogs) > 0:
            Print( "Missing log file(s) job ID: %s" % missingLogs)
        if len(missingOuts) > 0:
            Print( "Missing output files(s) job ID: %s" % missingOuts)

    # Print the dashboard url 
    if opts.url:
        Print(dashboardURL, False)

    return running, finished, transferring, failed, retrievedLog, retrievedOut, eosLog, eosOut


def GetReportTable(taskDir, nJobs, running, transferring, finished, unknown, failed, idle, retrievedLog, retrievedOut, eosLog, eosOut):
    '''
    Takes various info on the status of a CRAB job and return a neat table.
    '''
    Verbose("GetReportTable()", True)

    nTotal    = str(nJobs)
    nRun      = str(running)
    nTransfer = str(transferring)
    nFinish   = str(finished)
    nUnknown  = str(unknown)
    nFail     = str(len(failed))
    nIdle     = str(idle)
    nLogs     = ''.join( str(retrievedLog).split() ) 
    nOut      = ''.join( str(retrievedOut).split() )
    nLogsEOS  = ''.join( str(eosLog).split() ) 
    nOutEOS   = ''.join( str(eosOut).split() )
    txtAlign  = "{:<25} {:>4} {:<1} {:<4}"

    dataset   = taskDir.split("/")[-1]
    length    = 40 #len(dataset)
    hLine     = "="*length
    status    = GetTaskStatus(taskDir).replace("\t", "")
    txtAlignB = "{:<%s}" % (length)
    header    = txtAlignB.format(dataset)

    table = []
    table.append(hLine)
    table.append(header)
    table.append(hLine)
    table.append( txtAlign.format("%sIdle"             % (colors.GRAY  ), nIdle    , "/", nTotal ) )
    table.append( txtAlign.format("%sUnknown"          % (colors.GRAY  ), nUnknown , "/", nTotal ) )
    table.append( txtAlign.format("%sFailed"           % (colors.RED   ), nFail    , "/", nTotal ) )
    table.append( txtAlign.format("%sRunning"          % (colors.ORANGE), nRun     , "/", nTotal ) )
    table.append( txtAlign.format("%sTransferring"     % (colors.ORANGE), nTransfer, "/", nTotal ) )
    table.append( txtAlign.format("%sDone"             % (colors.WHITE ), nFinish  , "/", nTotal ) )
    table.append( txtAlign.format("%sRetrieved Logs"   % (colors.PURPLE), nLogs    , "/", nTotal ) )
    table.append( txtAlign.format("%sRetrieved Outputs"% (colors.BLUE  ), nOut     , "/", nTotal ) ) 
    table.append( txtAlign.format("%sEOS Logs"         % (colors.CYAN  ), nLogsEOS , "/", nTotal ) )
    table.append( txtAlign.format("%sEOS Outputs"      % (colors.CYAN  ), nOutEOS  , "/", nTotal ) ) 
    table.append( "{:<100}".format("%s%s"              % (colors.WHITE, hLine) ) )
    return table


def WalkEOSDir(taskName, pathOnEOS, opts):
    '''
    Looks inside the EOS path "pathOnEOS" directory by directory.
    Since OS commands do not work on EOS, I have written this function
    in a vary "dirty" way.. hoping to make it more robust in the future!
    '''
    Verbose("WalkEOSDir()", True)
    
    
    # Listing all files under the path
    cmd = ConvertCommandToEOS("ls", opts) + " " + pathOnEOS
    Verbose(cmd)
    dirContents = Execute(cmd)

    # Sometimes an error occures (for unknown reasons). Try alternative
    if "symbol lookup error" in dirContents[0]:
        raise Exception("%s\".\n\t\"%s\"." % (cmd, dirContents[0]) )
    else:
        Verbose("Walking the EOS directory \"%s\" with contents:\n\t%s" % (pathOnEOS, "\n\t".join(dirContents)))
    
    
    # A very, very dirty way to find the deepest directory where the ROOT files are located!
    if len(dirContents) == 1:
        subDir = dirContents[0]
        Verbose("Found sub-directory \"%s\" under the EOS path \"%s\"!" % (subDir, pathOnEOS) )    
        pathOnEOS = WalkEOSDir(taskName, pathOnEOS + "/" + subDir, opts)
    else:
        subDir = None
        for d in dirContents:
            if d == "crab_" + taskName:
                subDir = d
            
        # Special case required due to all data (Tau, JetHT) put under a single directory in EOS
        if subDir != None:
            pathOnEOS = WalkEOSDir(taskName, pathOnEOS + "/" + subDir, opts)
        else:
            rootFiles = []
            for f in dirContents:
                if ".root" not in f:
                    continue
                else:
                    rootFiles.append(pathOnEOS + "/" + f)
            pathOnEOS += "/"
            Verbose("Reached end of the line. Found \"%s\" ROOT files under \"%s\"!"  % (len(rootFiles), pathOnEOS))
    return pathOnEOS


def Exists(dataset, filename):
    '''
    Checks that a dataset filename exists by executing the ls command for its full path.
    '''
    Verbose("Exists()", False)

    fileName = os.path.join(dataset, "results", filename)
    cmd      = "ls " + fileName

    Verbose(cmd)
    files     = Execute("%s" % (cmd) ) #not used
    firstFile = files[0] #not used
    return os.path.exists(fileName)


def ExistsEOS(dataset, subDir, fileName, opts):
    '''
    Checks that a dataset filename exists by executing the ls command for its full path.
    '''
    Verbose("ExistsEOS()", False)

    fullPath = os.path.join(dataset, subDir, fileName)
    cmd_eos  = ConvertCommandToEOS("ls", opts)
    cmd      = cmd_eos + " " + fullPath
    
    Verbose(cmd)
    files  = Execute("%s" % (cmd) )

    # If file is not found there won't be a list of files; there will be an error message
    errMsg = files[0]
    if "Unable to stat" in errMsg:
        return False
    elif errMsg == fileName:
        return True
    else:
        raise Exception("This should not be reached! Execution of command \"%s\" returned \"%s\"" % (cmd, errMsg))


def Touch(path):
    '''
    The "touch" command is the easiest way to create new, empty files. 
    It is also used to change the timestamps (i.e., dates and times of the most recent access and modification)
    on existing files and directories.
    '''
    Verbose("Touch()")
    if os.path.exists(path):
        os.system("touch %s" % path)
    return


def Execute(cmd):
    '''
    Executes a given command and return the output.
    '''
    Verbose("Execute()", True)

    Verbose("Executing command: \"%s\"" % (cmd))
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)

    stdin  = p.stdout
    stdout = p.stdout
    ret    = []
    for line in stdout:
        ret.append(line.replace("\n", ""))

    stdout.close()
    return ret


def GetSelfName():
    Verbose("GetSelfName()")    
    return __file__.split("/")[-1]


def RemoveNonAscii(myString):
    '''
    Removes formatting from string   
    '''
    Verbose("RemoveNonAscii()")
    return "".join(i for i in myString if ord(i)<126 and ord(i)>31)


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


def AskToContinue(taskDirName, analysis, opts):
    '''
    Inform user of the analysis type and datasets to be user in the multi-CRAB job creation. Offer chance to abort sequence 
    '''
    Verbose("AskToContinue()")

    Print("Creating CRAB task \"%s\" for analysis \"%s\" with PSet=\"%s\":" % (taskDirName, analysis, opts.pset) )
    DatasetGroup(analysis).PrintDatasets(False)
    Print("Will submit to Storage Site \"%s\" [User MUST have write access to destination site!]" % (opts.storageSite))
    
    AbortTask(keystroke="q")
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

    # Copy file to be used (and others to be tracked) to the task directory
    cmd = "cp %s %s" %(opts.pset, dirName)

    if not os.path.exists(dirName):
        Verbose("mkidr %s" % (dirName))
	os.mkdir(dirName)

        Verbose(cmd)
	os.system(cmd)
    else:
        pass

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
    Verbose(cmd_submit, True)
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
        Print(msg + "\n\tProceeding to overwrite file.")
    return


def CreateCfgFile(dataset, taskDirName, requestName, infilePath, opts):
    '''
    Creates a CRAB-specific configuration file which will be used in the submission
    of a job. The function uses as input a generic cfg file which is then customised
    based on the dataset type used.

    infilePath = "crabConfig.py"
    '''
    Verbose("CreateCfgFile()")
	
    outfilePath = os.path.join(taskDirName, "crabConfig_" + requestName + ".py")
    
    # Check that file does not already exist
    EnsurePathDoesNotExist(taskDirName, outfilePath)

    # Open input file (read mode) and output file (write mode)
    fIN  = open(infilePath , "r")
    fOUT = open(outfilePath, "w")

    # Create compiled regular expression objects
    crab_requestName_re     = re.compile("config.General.requestName")
    crab_workArea_re        = re.compile("config.General.workArea")
    crab_transferOutputs_re = re.compile("config.General.transferOutputs")
    crab_transferLogs_re    = re.compile("config.General.transferLogs")
    crab_pset_re            = re.compile("config.JobType.psetName")
    crab_psetParams_re      = re.compile("config.JobType.pyCfgParams")
    crab_dataset_re         = re.compile("config.Data.inputDataset")
    crab_split_re           = re.compile("config.Data.splitting")
    crab_splitunits_re      = re.compile("config.Data.unitsPerJob")
    crab_dbs_re             = re.compile("config.Data.inputDBS")
    crab_storageSite_re     = re.compile("config.Site.storageSite")
    crab_outLFNDirBase_re   = re.compile("config.Data.outLFNDirBase")

    # For-loop: All line of input fine
    for line in fIN:
	    
	# Skip lines which are commented out
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
	    line = "config.JobType.psetName = '" + opts.pset +"'\n"

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

        match = crab_outLFNDirBase_re.search(line)
	if match:
            baseDir = '/store/user/%s/CRAB3_TransferData' % (getUsernameFromSiteDB())
            fullDir = os.path.join(baseDir, os.path.basename(taskDirName) )
	    line = "config.Data.outLFNDirBase = '" + fullDir + "'\n"
            
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
		line = "config.Data.unitsPerJob = 25\n"
	else:
	    pass

	# Write line to the output file
        fOUT.write(line)

    # Close input and output files 
    fOUT.close()
    fIN.close()

    Verbose("Created CRAB cfg file \"%s\"" % (fOUT.name) )
    return


def GetDatasetsPaths(opts):
    '''
    Return the absolute path for each task/dataset located inside
    the working multi-CRAB directory. If the --inlcudeTask or the
    --excludeTask options are used, they are taken into consideration
    accordingly.
    '''
    Verbose("GetDatasetsPaths()", True)

    # Get the multi-CRAB working dir
    multicrabDirPath = [opts.dirName]

    # Get the absolute path for each task(=dataset)
    datasetsDirPaths = GetDatasetAbsolutePaths(multicrabDirPath)
    Verbose("Found %s CRAB task directories:\n\t%s" % ( len(datasetsDirPaths), "\n\t".join(datasetsDirPaths)), True)

    # Check include/exclude options to get final datasets list
    datasets = GetIncludeExcludeDatasets(datasetsDirPaths, opts)

    return datasets


def GetDatasetsPathsForEOS(datasetsTmp, opts):
    '''
    '''
    Verbose("GetDatasetsPathsForEOS()", True)
    
    datasets = []
    for d in datasetsTmp:
        Print ("d = " + d, True)
        datasets.append( datasetsTmp, ConvertPathToEOS(d, opts) )
    return datasets
    

def ConvertPathToEOS(path, opts):
    '''
    Convert a given path to EOS-path. Used when working solely with EOS
    and files are not copied to local working directory    
    '''
    Verbose("ConvertPathToEOS()", True)

    Verbose("Converting %s path s to EOS-compatible" % (path))
    taskName            = path.split("/")[-1]
    taskNameEOS         = ConvertTasknameToEOS(taskName, opts)
    mcrabDir            = os.path.basename(opts.dirName)
    stringToBeReplaced  = opts.dirName    
    #stringToReplaceWith = "/store/user/%s/CRAB3_TransferData/" % (getpass.getuser())
    stringToReplaceWith = "/store/user/%s/CRAB3_TransferData/%s" % (getpass.getuser(), mcrabDir)
    eosPathTmp          = path.replace(stringToBeReplaced, stringToReplaceWith)
    pathEOS             = eosPathTmp.replace(taskName, taskNameEOS)
    Verbose("Converted %s (default) to %s (EOS)" % (path, pathEOS))
    return pathEOS


def GetCrabConfigFilesDict(taskNames, opts):
    '''
    Get a dictionary mapping the task-name to the craConfig_<dataset>.py file used
    to submit the job.
    '''
    Verbose("GetCrabConfigFilesDict()", True)

    # Variable definition
    multicrabDirPath = opts.dirName
    crabCfgFilesDict = {}

    # For-loop: All task-names
    for task in taskNames:
        fileName = "crabConfig_%s.py" % (task)
        filePath = os.path.join(multicrabDirPath, fileName)
        if not os.path.exists(filePath):
            raise Exception("File \"%s\" does not exist!" % (filePath) )
        else:
            Verbose("Reading file \"" + filePath + "\"")

        # Read the file lines & append the file to the list
        cfgFile = [i for i in open(filePath, 'r').readlines()]

        # Map the task and the cfg file used for job-submission
        crabCfgFilesDict[task] = cfgFile

    return crabCfgFilesDict


def ConvertTasknameToEOS(taskName, opts):
    '''
    Get the full dataset name as found EOS.
    '''
    Verbose("ConvertTasknameToEOS()", True)
    
    datasetsPaths = GetDatasetsPaths(opts)
    taskNames     = GetDatasetBasenames(datasetsPaths)
    crabCfgFile   = None
    taskNameEOS   = None

    # Get a list of crabConfig_<dataset>.py files
    crabCfgFilesDict = GetCrabConfigFilesDict(taskNames, opts)

    # For-loop; All lines in crabConfi_<dataset>.cfg file
    if taskName in crabCfgFilesDict.keys():
        crabCfgFile = crabCfgFilesDict[taskName]
    else:
        raise Exception("Unable to find the crabConfig_<dataset>.py for task with name \"%s\"." % (taskName) )
    
    Verbose("Determining full dataset name for task \"%s\" by reading the \"crabConfig_%s.py\" file." % (taskName, taskName))
    # For-loop: All lines in cfg file
    for l in crabCfgFile:
        keyword = "config.Data.inputDataset = "
        if keyword in l:
            taskNameEOS = l.replace(keyword, "").split("/")[1]

    if taskNameEOS == None:
        raise Exception("Unable to find the crabConfig_<dataset>.py for task with name \"%s\"." % (taskName) )
    else: 
        Verbose("The conversion of task name \"%s\" into EOS-compatible is \"%s\"" % (taskName, taskNameEOS))
    return taskNameEOS


def ConvertCommandToEOS(cmd, opts):
    '''
    Convert a given command to EOS-path. Used when working solely with EOS
    and files are not copied to local working directory    
    '''
    Verbose("ConvertCommandToEOS()", True)

    # Define a map mapping bash command with EOS commands
    cmdMap = {}
    cmdMap["ls"] = "/afs/cern.ch/project/eos/installation/0.3.84-aquamarine/bin/eos.select ls" #"eos ls" is an ALIAS for this command. Works
    cmdMap["rm"] = "eos rm"

    # EOS commands differ on LPC!
    if "fnal" in GetHostname():
        for key in cmdMap:
            if key == "ls": # exception because I use the full command, not the alias
                cmdMap[key] = "eos root://cmseos.fnal.gov ls"
            else:
                cmdMap[key] = cmdMap[key].replace("eos ", "eos")
        
    if cmd not in cmdMap:
        raise Exception("Could not find EOS-equivalent for cammand \"%s\"." % (cmd) )

    return cmdMap[cmd]


def CreateJob(opts, args):
    '''
    Create & submit a CRAB task, using the user-defined PSET and list of datasets.
    '''
    Verbose("CreateJob()", True)
    
    # Get general info
    version     = GetCMSSW()
    analysis    = GetAnalysis()
    datasets    = DatasetGroup(analysis).GetDatasetList()
    taskDirName = GetTaskDirName(analysis, version, datasets)

    # Give user last chance to abort
    AskToContinue(taskDirName, analysis, opts)
    
    # Create CRAB task diractory
    CreateTaskDir(taskDirName)
    
    # For-loop: All datasets
    for dataset in datasets:
        
	Verbose("Creating CRAB configuration file for dataset \"%s\"" % (dataset))
        requestName = GetRequestName(dataset)

        Verbose("Checking for already existing tasks (in case of resubmission)")
        fullDir = taskDirName + "/" + requestName
        if os.path.exists(fullDir) and os.path.isdir(fullDir):
            Print("Dataset \"%s\" already exists! Skipping ..." % (requestName), False)
            continue 

        Verbose("Creating cfg file for dataset \"%s\"" % (dataset), True)
	CreateCfgFile(dataset, taskDirName, requestName, "crabConfig.py", opts)
                
        Verbose("Submitting jobs for dataset \"%s\"" % (dataset), True)
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

    # Default Values
    VERBOSE = False
    PSET    = "miniAOD2TTree_SignalAnalysisSkim_cfg.py"
    SITE    = "T2_FI_HIP"
    DIRNAME = ""

    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("--create", dest="create", default=False, action="store_true", 
                      help="Flag to create a CRAB job [default: False")

    parser.add_option("--status", dest="status", default=False, action="store_true", 
                      help="Flag to check the status of all CRAB jobs [default: False")

    parser.add_option("--get", dest="get", default=False, action="store_true", 
                      help="Get output of finished jobs [defaut: False]")

    parser.add_option("--log", dest="log", default=False, action="store_true", 
                      help="Get log files of finished jobs [defaut: False]")

    parser.add_option("--resubmit", dest="resubmit", default=False, action="store_true", 
                      help="Resubmit all failed jobs [defaut: False]")

    parser.add_option("--kill", dest="kill", default=False, action="store_true", 
                      help="Kill all submitted jobs [defaut: False]")

    parser.add_option("-v", "--verbose", dest="verbose", default=VERBOSE, action="store_true",
                      help="Verbose mode for debugging purposes [default: %s]" % (VERBOSE))

    parser.add_option("-a", "--ask", dest="ask", default=False, action="store_true",
                      help="Prompt user before executing CRAB commands [defaut: False]")

    parser.add_option("-p", "--pset", dest="pset", default=PSET, type="string",
                      help="The python cfg file to be used by cmsRun [default: %s]" % (PSET))

    parser.add_option("-d", "--dir", dest="dirName", default=DIRNAME, type="string",
                      help="Custom name for CRAB directory name [default: %s]" % (DIRNAME))

    parser.add_option("-s", "--site", dest="storageSite", default=SITE, type="string", 
                      help="Site where the output will be copied to [default: %s]" % (SITE))

    parser.add_option("-u", "--url", dest="url", default=False, action="store_true", 
                      help="Print the dashboard URL for the CARB task [default: False]")

    parser.add_option("-i", "--includeTasks", dest="includeTasks", default="None", type="string", 
                      help="Only perform action for this dataset(s) [default: \"\"]")

    parser.add_option("-e", "--excludeTasks", dest="excludeTasks", default="None", type="string", 
                      help="Exclude this dataset(s) from action [default: \"\"]")

    parser.add_option("--filesInEOS", dest="filesInEOS", default=False, action="store_true",
                      help="The CRAB files are in a local EOS. Do not use files from the local multicrab directory [default: 'False']")

    (opts, args) = parser.parse_args()

    if opts.create == False and opts.dirName == "":
	opts.dirName = os.getcwd()

    if opts.create == True and opts.status == True:
        raise Exception("Cannot both create and check a CRAB job!")	    

    if opts.create == True:
        sys.exit( CreateJob(opts, args) )
    elif opts.status == True or opts.get == True or opts.log == True or opts.resubmit == True or opts.kill == True:
        if opts.dirName == "":
            raise Exception("Must provide a multiCRAB dir with the -d option!")            
        else:
            sys.exit( CheckJob(opts, args) )
    else:
        raise Exception("Must either create or check a CRAB job!")
