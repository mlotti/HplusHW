#!/usr/bin/env python
'''
Creation/Submission:
multicrab.py --create -s T2_CH_CERN -p miniAOD2TTree_Hplus2tbAnalysisSkim_cfg.py

Re-Submission:
multicrab.py --create -s T2_CH_CERN -p miniAOD2TTree_Hplus2tbAnalysisSkim_cfg.py -d <task_dir> 

Check Status:
multicrab.py --status --url --url --verbose -d <task_dir> 

Get Output:
multicrab.py --get --ask -d <task_dir> 
multicrab.py --log

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

Hints:
To check whether you have write persmissions on a T2 centre use the command
crab checkwrite --site
For example:
crab checkwrite --site T2_CH_CERN

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
from optparse import OptionParser

# See: https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRABClientLibraryAPI#The_crabCommand_API
from CRABAPI.RawCommand import crabCommand
from CRABClient.UserUtilities import setConsoleLogLevel

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
    def __init__(self, name, allJobs, retrieved, running, finished, failed, retrievedLog, retrievedOut, status, dashboardURL):
        '''
        Constructor 
        '''
        Verbose("__init__()")
        self.name         = name
        self.allJobs      = str(allJobs)
        self.retrieved    = str(retrieved)
        self.running      = str(running)
        self.dataset      = self.name.split("/")[-1]
        self.dashboardURL = dashboardURL
        self.status       = self.GetTaskStatusStyle(status)
        self.finished     = finished
        self.failed       = failed
        self.retrievedLog = retrievedLog
        self.retrievedOut = retrievedOut
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
        Verbose("GetTaskStatusStyle()")
        
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
            Print("WARNING! Unexpected task status \"%s\"" % (status) )

        return status


#================================================================================================ 
# Function Definitions
#================================================================================================ 
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
    

def GetTaskStatusBool(datasetPath):
    '''
    Check the crab.log for the given task to determine the status.
    If the the string "Done" is found inside skip it.
    '''
    Verbose("GetTaskStatusBool()")
    crabLog      = os.path.join(datasetPath,"crab.log")
    stringToGrep = "Done"
    cmd          = "grep '%s' %s" % (stringToGrep, crabLog)
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
        # Sanity check (file exists)
        if os.path.exists( grepFile ):
            results      = [i for i in open(grepFile, 'r').readlines()]
            dashboardURL = FindBetween( results[0], "URL:\t", "\n" )
            # Verbose("Removing temporary file \"%s\"" % (grepFile), False)
            os.system("rm -f %s " % (grepFile) )
        else:
            print "ERROR! File \"grep.tmp\" not found! EXIT"
            sys.exit()
    else:
        dashboardURL = "UNDETERMINED"
        Verbose("Could not execute command \"%s\"" % (cmd) )
    return dashboardURL


def GetTaskStatus(datasetPath):
    '''
    Call the "grep" command to look for the "Task status" from the crab.log file 
    of a given dataset. It uses as input parameter the absolute path of the task dir (datasetPath)
    '''
    Verbose("GetTaskStatus()")
    
    # Variable Declaration
    crabLog      = os.path.join(datasetPath, "crab.log")
    grepFile     = os.path.join(datasetPath, "grep.tmp")
    stringToGrep = "Task status:"
    cmd          = "grep '%s' %s > %s" % (stringToGrep, crabLog, grepFile )
    status       = "UNKNOWN"

    # Execute the command
    if os.system(cmd) == 0:
        # Sanity check (file exists)
        if os.path.exists( grepFile ):
            results = [i for i in open(grepFile, 'r').readlines()]
            status  = FindBetween( results[-1], stringToGrep, "\n" )
            # Verbose("Removing temporary file \"%s\"" % (grepFile), False)
            os.system("rm -f %s " % (grepFile) )
        else:
            Print ("ERROR! File \"grep.tmp\" not found! EXIT", True)
    else:
        status = "UNDETERMINED"
        Verbose("Could not execute command \"%s\"" % (cmd) )
    return status



def GetTaskReports(datasetPath, status, dashboardURL):
    '''
    Execute "crab status", get task logs and output. 
    Resubmit or kill task according to user options.
    '''
    Verbose("GetTaskReports()")

    report = None
    
    # Get all files under <dataset_dir>/results/
    files = Execute("ls %s" % os.path.join( datasetPath, "results") )

    Verbose("crab status --dir=%s" % (GetLast2Dirs(datasetPath)), False)
    try:

        # Execute "crab status --dir=datasetPath"
        Verbose("Getting Task status")
        result = crabCommand('status', dir = datasetPath)
    
        # Assess JOB success/failure for task
        Verbose("Retrieving Files (1/2)")
        running, finished, failed, retrievedLog, retrievedOut = RetrievedFiles(datasetPath, result, dashboardURL, False)
           
        # Get the task logs & output ?        
        Verbose("Getting Task Logs")
        GetTaskLogs(datasetPath, retrievedLog, finished)

        # Get the task output
        Verbose("Getting Task output")
        GetTaskOutput(datasetPath, retrievedOut, finished)

        # Resubmit task if failed jobs found
        Verbose("Resubmitting Failed Tasks")
        ResubmitTask(datasetPath, failed)

        # Kill task which are active
        Verbose("Killing Active Tasks")
        KillTask(datasetPath)
            
        # Assess JOB success/failure for task (again)
        Verbose("Retrieving Files (2/2)")
        running, finished, failed, retrievedLog, retrievedOut = RetrievedFiles(datasetPath, result, dashboardURL, True)
        retrieved = min(finished, retrievedLog, retrievedOut)
        alljobs   = len(result['jobList'])        

        # Append the report
        Verbose("Appending Report")
        report = Report(datasetPath, alljobs, retrieved, running, finished, failed, retrievedLog, retrievedOut,  status, dashboardURL)

        # Determine if task is DONE or not
        Verbose("Determining if Task is DONE")
        if retrieved == alljobs and retrieved > 0:
            absolutePath = os.path.join(datasetPath, "crab.log")
            os.system("sed -i -e '$a\DONE! (Written by multicrabCheck.py)' %s" % absolutePath )

    # Catch exceptions (Errors detected during execution which may not be "fatal")
    except:
        msg = sys.exc_info()[1]
        report = Report(datasetPath, "?", "?", "?", "?", "?", "?", "?", "?", dashboardURL) 
        Print("crab status failed with message \"%s\". Skipping ..." % ( msg ), False)
    return report


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
        #dummy = crabCommand('getlog', dir=taskPath)
        dummy = crabCommand('getlog', 'command=LCG', 'checksum=no', dir=taskPath)
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
            #cmd = "crab %s --dir %s" % ("get", taskPath)
            #Execute(cmd)
            dummy = crabCommand("getoutput", dir=taskPath) #fixme: add checksum?
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

    if opts.ask:
        if AskUser("Resubmit task \"%s\"?" % (GetLast2Dirs(taskPath)) ):
            dummy = crabCommand('resubmit', dir=taskPath)
        else:
            return
    else:
        Print("Found \"Failed\" jobs! Resubmitting ...")
        dummy = crabCommand('resubmit', dir=taskPath)
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
        # Check that results directory exists
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
    Verbose("GetDatasetBasenames()")
    
    basenames = []
    for d in datasets:
        basenames.append(os.path.basename(d))
    return basenames


def GetLast2Dirs(datasetPath):
    Verbose("GetLast2Dirs()")
    
    last2Dirs = datasetPath.split("/")[-2]+ "/" + datasetPath.split("/")[-1]
    return last2Dirs


#================================================================================================
# Submit Programs
#================================================================================================
def CheckJob(opts, args):
    '''
    Check status, retrieve, resubmit, kill CRAB tasks.
    '''
    Verbose("CheckJob()")

    # Force crabCommand to stay quite
    if not opts.verbose:
        setConsoleLogLevel(LOGLEVEL_MUTE)

    # Retrieve the current crabCommand console log level:
    crabConsoleLogLevel = getConsoleLogLevel()
    Verbose("The current \"crabCommand\" console log level is set to \"%s\"" % (crabConsoleLogLevel), True)
    
    ## Get the CRAB dir(s) name (passed as argument)
    #dirs = sys.argv[1:]
    dirs = [opts.dirName]
    
    # Initialise Variables
    reportDict   = {}
    datasetdirs  = GetMulticrabAbsolutePaths(dirs)
    datasets     = GetDatasetAbsolutePaths(datasetdirs)
    baseNames    = GetDatasetBasenames(datasets)
    Verbose("Found %s CRAB task directories:\n\t%s" % ( len(datasets), "\n\t".join(baseNames)), True)

    # For-loop: All dataset directories (absolute paths)
    for index, d in enumerate(datasets):
        
        if opts.verbose:
            Print("%s (%s/%s)" % ( GetLast2Dirs(d), index+1, len(datasets) ), True)

        # Check if task is in "DONE" state
        if GetTaskStatusBool(d):
            continue

        # Get CRAB task dashboard URL
        taskDashboard = GetTaskDashboardURL(d)    
        
        # Get CRAB task status
        taskStatus = GetTaskStatus(d).replace("\t", "")

        # Get the CRAB task report & add to dictionary
        report = GetTaskReports(d, taskStatus, taskDashboard) #FIXME
        reportDict[d.split("/")[-1]] = report

    # Print summary of all CRAB tasks
    PrintTaskSummary(reportDict)
    return


def PrintTaskSummary(reportDict):
    '''
    Print a summary table of all submitted tasks with minimal information.
    The purpose it to easily determine which jobs are done, running and failed.
    '''
    Verbose("PrintTaskSummary()")
    
    reports  = []
    #msgAlign = "{:<3} {:<60} {:^20} {:>6} {:>1} {:<6}"
    #header   = msgAlign.format("#", "Dataset", "%s%s%s" % (colors.WHITE, "Status", colors.WHITE), "Ret.", "/", "Tot.")
    msgAlign = "{:<3} {:<60} {:^20} {:>10} {:>10} {:>10} {:>10} {:>10} {:>10}"
    header   = msgAlign.format("#", "Dataset", "%s%s%s" % (colors.WHITE, "Status", colors.WHITE), "All", "Running", "Finished", "Failed", "Logs", "Output")
    #retrieved, finished, failed, retrievedLog, retrievedOut
    hLine    = "="*len(header)
    # reports.append("\n")
    reports.append(hLine)
    reports.append(header)
    reports.append(hLine)
    
    # For-loop: All datasets (key) and corresponding status (value)
    for i, dataset in enumerate(reportDict):
        report  = reportDict[dataset]
        status  = report.status
        allJobs = report.allJobs
        running = report.running
        finished= report.finished
        failed  = report.failed
        rLogs   = report.retrievedLog
        rOutput = report.retrievedOut
        line   = msgAlign.format(i+1, dataset, status, allJobs, running, finished, failed, rLogs, rOutput)
        #ret    = report.retrieved
        #tot    = report.allJobs
        #line   = msgAlign.format(i+1, dataset, status, ret,  "/", tot)
        reports.append(line)
    reports.append(hLine)
    
    # For-loop: All lines in report table
    for r in reports:
        print r
    return


def RetrievedFiles(directory, crabResults, dashboardURL, verbose):
    '''
    Determines whether the jobs Finished (Success or Failure), and whether 
    the logs and output files have been retrieved. Returns all these in form
    of lists
    '''
    Verbose("RetrievedFiles()")
    
    # Initialise variables
    retrievedLog = 0
    retrievedOut = 0
    finished     = 0
    failed       = 0
    transferring = 0
    running      = 0
    idle         = 0
    unknown      = 0
    dataset      = directory.split("/")[-1]
    nJobs        = len(crabResults['jobList'])
    missingOuts  = []
    missingLogs  = []

    # For-loop:All CRAB results
    for index, r in enumerate(crabResults['jobList']):
        
        # Assess the jobs status individually
        if r[0] == 'finished':
            finished += 1
            foundLog  = Exists(directory, "cmsRun_%i.log.tar.gz" % r[1])
            foundOut  = Exists(directory, "*_%i.root" % r[1])
            if foundLog:
                retrievedLog += 1
            if foundOut:
                retrievedOut += 1
            if foundLog and not foundOut:
                missingOuts.append( r[1] )
            if foundOut and not foundLog:
                missingLogs.append( r[1] )
        elif r[0] == 'failed':
            failed += 1
        elif r[0] == 'transferring':
            transferring += 1 
        elif r[0] == 'idle':
            idle += 1 
        elif r[0] == 'running':
            running+= 1 
        else:
            unknown+= 1 
        
    # Print results in a nice table
    nTotal    = str(nJobs)
    nRun      = str(running)
    nTransfer = str(transferring)
    nFinish   = str(finished)
    nUnknown  = str(unknown)
    nFail     = str(failed)
    nIdle     = str(idle)
    nLogs     = ''.join( str(retrievedLog).split() ) 
    nOut      = ''.join( str(retrievedOut).split() )
    txtAlign  = "{:<25} {:>4} {:<1} {:<4}"
    tableRows = []
    dataset   = directory.split("/")[-1]
    length    = 40 #len(dataset)
    hLine     = "="*length
    status    = GetTaskStatus(directory).replace("\t", "")
    txtAlignB = "{:<%s}" % (length)
    header    = txtAlignB.format(dataset)
    tableRows.append(hLine)
    tableRows.append(header)
    tableRows.append(hLine)
    
    tableRows.append( txtAlign.format("%sIdle"             % (colors.GRAY  ), nIdle    , "/", nTotal ) )
    tableRows.append( txtAlign.format("%sUnknown"          % (colors.GRAY), nUnknown , "/", nTotal ) )
    tableRows.append( txtAlign.format("%sFailed"           % (colors.RED   ), nFail    , "/", nTotal ) )
    tableRows.append( txtAlign.format("%sRunning"          % (colors.ORANGE), nRun     , "/", nTotal ) )
    tableRows.append( txtAlign.format("%sTransferring"     % (colors.ORANGE), nTransfer, "/", nTotal ) )
    tableRows.append( txtAlign.format("%sDone"             % (colors.WHITE ), nFinish  , "/", nTotal ) )
    tableRows.append( txtAlign.format("%sRetrieved Logs"   % (colors.PURPLE), nLogs    , "/", nTotal ) )
    tableRows.append( txtAlign.format("%sRetrieved Outputs"% (colors.BLUE  ), nOut     , "/", nTotal ) ) 
    tableRows.append( "{:<100}".format("%s%s"              % (colors.WHITE, hLine) ) )

    if verbose:
        for r in tableRows:
            Print(r, False)
        print
    
    # Sanity check
    if verbose and status == "COMPLETED":
        if len(missingLogs) > 0:
            Print( "Missing log file(s) job ID: %s" % missingLogs)
        if len(missingOuts) > 0:
            Print( "Missing output files(s) job ID: %s" % missingOuts)

    # Print the dashboard url 
    if opts.url:
        Print(dashboardURL, False)
    return running, finished, failed, retrievedLog, retrievedOut


def Exists(dataset,filename):
    Verbose("Exists()")
    fname = os.path.join(dataset,"results",filename)
    fname = Execute("ls %s"%fname)[0]
    return os.path.exists(fname)


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
    Verbose("Execute()")
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    (s_in, s_out) = (p.stdin, p.stdout)
        
    f = s_out
    ret=[]
    for line in f:
        ret.append(line.replace("\n", ""))
        
    f.close()
    return ret

#================================================================================================ 
# Function Definitions
#================================================================================================ 
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
        #if AskUser(msg + "\n\tProceed and overwrite it?"):
        #    return
	#else:
        #    raise Exception(msg)
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
    EnsurePathDoesNotExist(taskDirName, outfilePath)

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
		line = "config.Data.unitsPerJob = 50\n"
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
# Create Program
#================================================================================================ 
def CreateJob(opts, args):
    '''
    Create & submit a CRAB task, using the user-defined PSET and list of datasets.
    '''
    Verbose("CreateJob()")
    
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
            Print("Dataset \"%s\" already exists! Skipping ..." % (requestName))
            continue 

        Verbose("Creating cfg file for dataset \"%s\"" % (dataset) )
	CreateCfgFile(dataset, taskDirName, requestName, "crabConfig.py")		
	
        Verbose("Submitting jobs for dataset \"%s\"" % (dataset) )
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
    parser.add_option("--create"  , dest="create"    , default=False, action="store_true", help="Flag to create a CRAB job [default: False")
    parser.add_option("--status"  , dest="status"    , default=False, action="store_true", help="Flag to check the status of all CRAB jobs [default: False")
    parser.add_option("--get"     , dest="get"       , default=False, action="store_true", help="Get output of finished jobs [defaut: False]")
    parser.add_option("--log"     , dest="log"       , default=False, action="store_true", help="Get log files of finished jobs [defaut: False]")
    parser.add_option("--resubmit", dest="resubmit"  , default=False, action="store_true", help="Resubmit all failed jobs [defaut: False]")
    parser.add_option("--kill"    , dest="kill"      , default=False, action="store_true", help="Kill all submitted jobs [defaut: False]")
    parser.add_option("-v", "--verbose", dest="verbose"    , default=VERBOSE, action="store_true", help="Verbose mode for debugging purposes [default: %s]" % (VERBOSE))
    parser.add_option("-a", "--ask"    , dest="ask"        , default=False  , action="store_true", help="Prompt user before executing CRAB commands [defaut: False]")
    parser.add_option("-p", "--pset"   , dest="pset"       , default=PSET   , type="string"      , help="The python cfg file to be used by cmsRun [default: %s]" % (PSET))
    parser.add_option("-d", "--dir"    , dest="dirName"    , default=DIRNAME, type="string"      , help="Custom name for CRAB directory name [default: %s]" % (DIRNAME))
    parser.add_option("-s", "--site"   , dest="storageSite", default=SITE   , type="string"      , help="Site where the output will be copied to [default: %s]" % (SITE))
    parser.add_option("-u", "--url"    , dest="url"        , default=False  , action="store_true", help="Print the dashboard URL for the CARB task [default: False]")
    #parser.add_option("--checksum", dest="checksum"  , default=False, action="store_true", help="Get output with adler32 checksum [default: False") #fixme
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
