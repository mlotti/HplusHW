#!/usr/bin/env python
'''
Usage:
multicrabCheck.py <multicrab_dir>

Description:
This script is used retrieve output and check status of submitted multicrab jobs.

Launching the command requires the  multicrab-dir name to be checked to be passed 
as a parameter:
multicrabCheck.py <multicrab_dir>

Resubmitting Tasks:
multicrabCheck.py <multicrab_dir> --resubmit

Killing Tasks:
multicrabCheck.py <multicrab_dir> --kill

Verbose Mode:
multicrabCheck.py <multicrab_dir> --verbose


Links:
https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3ConfigurationFile
https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookCRAB3Tutorial#Setup_the_environment

https://github.com/dmwm/CRABClient/tree/master/src/python/CRABClient/Commands
https://github.com/dmwm/CRABClient/blob/be9eebfa41268e836fa186259ef3391f998c8fff/src/python/CRABAPI/RawCommand.py    
https://github.com/dmwm/CRABClient/blob/master/src/python/CRABClient/Commands/kill.py
'''
                                                                                                                                                                              
#================================================================================================ 
# Import Modules
#================================================================================================ 
import os
import re
import sys
import time
import subprocess
from optparse import OptionParser

# See: https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRABClientLibraryAPI#The_crabCommand_API
from CRABAPI.RawCommand import crabCommand
from CRABClient.UserUtilities import setConsoleLogLevel

# See: https://github.com/dmwm/CRABClient/blob/master/src/python/CRABClient/ClientUtilities.py
from CRABClient.ClientUtilities import LOGLEVEL_MUTE
from CRABClient.UserUtilities import getConsoleLogLevel

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


class Report:
    def __init__(self, name, allJobs, retrieved, status, dashboardURL):
        '''
        Constructor 
        '''
        self.name         = name
        self.allJobs      = str(allJobs)
        self.retrieved    = str(retrieved)
        self.dataset      = self.name.split("/")[-1]
        self.dashboardURL = dashboardURL
        self.status       = self.GetTaskStatusStyle(status)
        return


    def Print(self, printHeader=True):
        name = os.path.basename(self.name)
        while len(name) < 30:
            name += " "
            
        if printHeader:
            print "=== multicrabCheck.py:"
        msg  = '{:<20} {:<40}'.format("\t %sDataset"           % (colors.WHITE) , ": " + self.dataset)
        msg += '\n {:<20} {:<40}'.format("\t %sRetrieved Jobs" % (colors.WHITE) , ": " + self.retrieved + " / " + self.allJobs)
        msg += '\n {:<20} {:<40}'.format("\t %sStatus"         % (colors.WHITE) , ": " + self.status)
        msg += '\n {:<20} {:<40}'.format("\t %sDashboard"      % (colors.WHITE) , ": " + self.dashboardURL)
        print msg
        return
    

    def GetURL():
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
def Verbose(msg, printHeader=True):
    if not opts.verbose:
        return
            
    if printHeader:
        print "=== multicrabCheck.py:"
    print "\t", msg
    return


def Print(msg, printHeader=False):
    if printHeader:
        print "=== multicrabCheck.py:"
    print "\t", msg
    return


def AskUser(msg):
    '''
    Prompts user for keyboard feedback to a certain question. 
    Returns true if keystroke is \"y\", false otherwise.
    '''

    keystroke = raw_input("\t" +  msg + " (y/n): ")
    if (keystroke.lower()) == "y":
        return True
    elif (keystroke.lower()) == "n":
        return True
    else:
        AskUser(msg)
    

def GetTaskStatusBool(datasetPath):
    '''
    Check the crab.log for the given task to determine the status.
    If the the string "Done" is found inside skip it.
    '''
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
            dashboardURL = find_between( results[0], "URL:\t", "\n" )
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
            status  = find_between( results[-1], stringToGrep, "\n" )
            # Verbose("Removing temporary file \"%s\"" % (grepFile), False)
            os.system("rm -f %s " % (grepFile) )
        else:
            Print ("ERROR! File \"grep.tmp\" not found! EXIT", True)
    else:
        status = "UNDETERMINED"
        Verbose("Could not execute command \"%s\"" % (cmd) )
    return status



def GetTaskReports(datasetPath, status, dashboardURL):
    # Variable Declaration
    reports = []
    
    # Get all files under <dataset_dir>/results/
    files = execute("ls %s" % os.path.join( datasetPath, "results") )


    Verbose("crab status --dir=%s" % (GetLast2Dirs(datasetPath)), False)
    try:

        # Execute "crab status --dir=datasetPath"
        Verbose("Getting Task status")
        result = crabCommand('status', dir = datasetPath)
    
        # Assess JOB success/failure for task
        Verbose("Retrieving Files (1/2)")
        finished, failed, retrievedLog, retrievedOut = RetrievedFiles(datasetPath, result, dashboardURL, False)
    
        # Get the task logs
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
        finished, failed, retrievedLog, retrievedOut = RetrievedFiles(datasetPath, result, dashboardURL, True)
        retrieved = min(finished, retrievedLog, retrievedOut)
        alljobs   = len(result['jobList'])        

        # Append the report
        Verbose("Appending Report")
        report = Report(datasetPath, alljobs, retrieved, status, dashboardURL)
        reports.append(report)        

        # Determine if task is DONE or not
        Verbose("Determining if Task is DONE")
        if retrieved == alljobs and retrieved > 0:
            absolutePath = os.path.join(datasetPath, "crab.log")
            os.system("sed -i -e '$a\DONE! (Written by multicrabCheck.py)' %s" % absolutePath )

    # Catch exceptions (Errors detected during execution which may not be "fatal")
    except:
        msg = sys.exc_info()[1]
        reports.append( Report(datasetPath, "?", "?", "?", dashboardURL) )
        Print("crab status failed with message \"%s\". Skipping ..." % ( msg ), False)

        # Verbose("Re-executing \"crab status\" command, this time with full verbosity")
        # setConsoleLogLevel(1)
        # result = crabCommand('status', dir = datasetPath)
    return reports


def GetTaskLogs(taskPath, retrievedLog, finished):
    '''
    If the number of retrieved logs files is smaller than the number of finished jobs,
    execute the CRAB command "getlog" to retrieve all unretrieved logs files.
    '''
    if retrievedLog == finished:
        return
        
    if opts.get:
        Verbose("Retrieved logs (%s) < finished (%s). Retrieving CRAB logs ..." % (retrievedLog, finished) )
        touch(taskPath)
        dummy = crabCommand('getlog', dir = taskPath)
    else:
        Verbose("Retrieved logs (%s) < finished (%s). To retrieve CRAB logs relaunch script with --get option." % (retrievedLog, finished) )
    return


def GetTaskOutput(taskPath, retrievedOut, finished):
    '''
    If the number of retrieved output files is smaller than the number of finished jobs,
    execute the CRAB command "getoutput" to retrieve all unretrieved output files.
    '''
    if retrievedOut == finished:
        return
    
    if opts.get:
        if opts.promptUser:
            if AskUser("Retrieved output (%s) < finished (%s). Retrieve CRAB output?" % (retrievedOut, finished) ):
                dummy = crabCommand('getoutput', dir = taskPath)
                touch(taskPath)
            else:
                return
        else:
            Verbose("Retrieved output (%s) < finished (%s). Retrieving CRAB output ..." % (retrievedOut, finished) )
            dummy = crabCommand('getoutput', dir = taskPath)
            touch(taskPath)
    else:
        Verbose("Retrieved output (%s) < finished (%s). To retrieve CRAB output relaunch script with --get option." % (retrievedOut, finished) )
    return
        

def ResubmitTask(taskPath, failed):
    '''
    If the number of failed jobs is greater than zero, 
    execute the CRAB command "resubmit" to resubmit all failed jobs.
    '''
    if failed == 0:
        return

    if opts.resubmit:
        Print("Found \"Failed\" jobs! Resubmitting ...")
        dummy = crabCommand('resubmit', dir = taskPath)
    else:
        Verbose("Found \"Failed\" jobs! To resubmit relaunch script with --resubmit option.")
    return


def KillTask(taskPath):
    '''
    If the number of failed jobs is greater than zero, 
    execute the CRAB command "resubmit" to resubmit all failed jobs.
    '''
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
    
    if opts.promptUser:
        if AskUser("Kill task \"%s\"?" % (GetLast2Dirs(taskPAth)) ):
            dummy = crabCommand('kill', dir = taskPath)
        else:
            pass
    else:
        dummy = crabCommand('kill', dir = taskPath)
    return


def find_between(myString, first, last ):
    '''
    '''
    try:
        start = myString.index( first ) + len( first )
        end   = myString.index( last, start )
        return myString[start:end]
    except ValueError:
        return ""


def find_between_r(myString, first, last ):
    '''
    '''
    try:
        start = myString.rindex( first ) + len( first )
        end   = myString.rindex( last, start )
        return myString[start:end]
    except ValueError:
        return ""


def usage():
    '''
    Informs user of how the script must be used.
    '''
    Print("Usage: ", os.path.basename(sys.argv[0]), " <multicrab dir>", True)
    sys.exit()
    

def GetMulticrabAbsolutePaths(dirs):
    '''
    '''
    datasetdirs = []
    # For-loop: All multiCRAB dirs (relative paths)
    for d in dirs:
        # Get absolute paths
        if os.path.exists(d) and os.path.isdir(d):
            datasetdirs.append( os.path.abspath(d) )

    if len(dirs) == 0:
        datasetdirs.append(os.path.abspath("."))
    return datasetdirs


def GetDatasetAbsolutePaths(datasetdirs):
    '''
    '''
    datasets = []
    # For-loop: All multiCRAB dirs (absolute paths)
    for d in datasetdirs:
        # Check that results directory exists
        if os.path.exists( os.path.join(d, "results") ):
            datasets.append(d)

        # Get the contents of this directory
        cands = execute("ls -tr %s"%d)
        # For-loop: All directory contents
        for c in cands:
            path = os.path.join(d, c)
            # Get all dataset directories 
            if os.path.exists( os.path.join(path, "results") ):
                datasets.append(path)
    return datasets


def GetDatasetBasenames(datasets):
    basenames = []
    for d in datasets:
        basenames.append(os.path.basename(d))
    return basenames


def GetLast2Dirs(datasetPath):
    last2Dirs = datasetPath.split("/")[-2]+ "/" + datasetPath.split("/")[-1]
    return last2Dirs


#================================================================================================
# Main Program
#================================================================================================
def main(opts, args):

    # Force crabCommand to stay quite
    if not opts.verbose:
        setConsoleLogLevel(LOGLEVEL_MUTE)

    # Retrieve the current crabCommand console log level:
    crabConsoleLogLevel = getConsoleLogLevel()
    Verbose("The current \"crabCommand\" console log level is set to \"%s\"" % (crabConsoleLogLevel), True)
    
    # Ensure script is called with at least one argument (apart from script name)
    if len(sys.argv) == 1:
        scriptName = sys.argv[0] 
        usage()

    # Get the multiCRAB dir(s) name (passed as argument)
    dirs = sys.argv[1:]

    # Initialise Variables
    reports      = []
    datasetdirs  = GetMulticrabAbsolutePaths(dirs)
    datasets     = GetDatasetAbsolutePaths(datasetdirs)
    baseNames    = GetDatasetBasenames(datasets)
    Verbose("Found %s CRAB task directories:\n\t%s" % ( len(datasets), "\n\t".join(baseNames)), True)

    # For-loop: All dataset directories (absolute paths)
    for index, d in enumerate(datasets):
        
        Print("%s (%s/%s)" % ( GetLast2Dirs(d), index+1, len(datasets) ), True)

        # Check if task is in "DONE" state
        if GetTaskStatusBool(d):
            continue

        # Get task dashboard URL
        taskDashboard = GetTaskDashboardURL(d)
        
        # Get task status
        taskStatus = GetTaskStatus(d) 

        # Kill task if requested by user
        reports += GetTaskReports(d, taskStatus, taskDashboard)

    # For-loop: All CRAB reports
    if 0:
        for r in reports:
            r.Print()
        
    return


def RetrievedFiles(directory, crabResults, dashboardURL, verbose):
    '''
    Determines whether the jobs Finished (Success or Failure), and whether 
    the logs and output files have been retrieved. Returns all these in form
    of lists
    '''
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
            foundLog  = exists(directory, "cmsRun_%i.log.tar.gz" % r[1])
            foundOut  = exists(directory, "*_%i.root" % r[1])
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
    hLine     = "="*40
    status    = GetTaskStatus(directory).replace("\t", "")
    header    = "{:^34}".format(dataset + " (" + status +")")
    tableRows.append(hLine)
    tableRows.append(header)
    tableRows.append(hLine)

    tableRows.append( txtAlign.format("%sIdle"             % (colors.GRAY  ), nIdle    , "/", nTotal ) )
    tableRows.append( txtAlign.format("%sUnknown"          % (colors.YELLOW), nUnknown , "/", nTotal ) )
    tableRows.append( txtAlign.format("%sFailed"           % (colors.RED   ), nFail    , "/", nTotal ) )
    tableRows.append( txtAlign.format("%sRunning"          % (colors.GREEN ), nRun     , "/", nTotal ) )
    tableRows.append( txtAlign.format("%sTransferring"     % (colors.ORANGE), nTransfer, "/", nTotal ) )
    tableRows.append( txtAlign.format("%sDone"             % (colors.WHITE ), nFinish  , "/", nTotal ) )
    tableRows.append( txtAlign.format("%sRetrieved Logs"   % (colors.PURPLE), nLogs    , "/", nTotal ) )
    tableRows.append( txtAlign.format("%sRetrieved Outputs"% (colors.BLUE  ), nOut     , "/", nTotal ) ) 
    tableRows.append( "{:<100}".format("%s%s"              % (colors.WHITE, hLine) ) )

    if verbose:
        for r in tableRows:
            Print(r, False)
        #print colors.WHITE
        
    # Sanity check
    if verbose and status == "COMPLETED":
        if len(missingLogs) > 0:
            Print( "Missing log file(s) job ID: %s" % missingLogs)
        if len(missingOuts) > 0:
            Print( "Missing output files(s) job ID: %s" % missingOuts)

    # Print the dashboard url 
    Print(dashboardURL, False)
    return finished, failed, retrievedLog, retrievedOut


def exists(dataset,filename):
    '''
    '''
    fname = os.path.join(dataset,"results",filename)
    fname = execute("ls %s"%fname)[0]
    return os.path.exists(fname)


def touch(path):
    '''
    The "touch" command is the easiest way to create new, empty files. 
    It is also used to change the timestamps (i.e., dates and times of the most recent access and modification)
    on existing files and directories.
    '''
    if os.path.exists(path):
        os.system("touch %s" % path)
    return


def execute(cmd):
    '''
    '''
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    (s_in, s_out) = (p.stdin, p.stdout)
        
    f = s_out
    ret=[]
    for line in f:
        ret.append(line.replace("\n", ""))
        
    f.close()
    return ret

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
    parser.add_option("-v", "--verbose"   , dest="verbose"   , default=False, action="store_true", help="Verbose mode")
    parser.add_option("-p", "--promptUser", dest="promptUser", default=False, action="store_true", help="Prompt user before executing CRAB commands")
    parser.add_option("-r", "--resubmit"  , dest="resubmit"  , default=False, action="store_true", help="Resubmit all failed jobs")
    parser.add_option("-k", "--kill"      , dest="kill"      , default=False, action="store_true", help="Kill all submitted jobs")
    parser.add_option("-g", "--get"       , dest="get"       , default=False, action="store_true", help="Get output of finished jobs")
    (opts, args) = parser.parse_args()

    sys.exit( main(opts, args) )
