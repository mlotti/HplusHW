#!/usr/bin/env python
'''
Description:
Once all the jobs have been successfully retrieved from a multicrab job two scripts must then be run:
1) hplusLumiCalc.py:
Calculates luminosity with LumiCalc and the pile-up with pileupCalc for collision dataset samples. There
is no need to run this if only MC samples were processed. For more information see the docstrings of hplusLumiCalc.py

2) hplusMergeHistograms.py:
Merges ROOT files into one (or more) files. It also reads TopPt.root and adds a "top-pt-correction-weigh" histogram in miniaod2tree.root files. 
The maximum allowable size for a single ROOT file is limited to 2 GB (but can be overwritten).


Usage: (from inside a multicrab_AnalysisType_vXYZ_TimeStamp directory)
hplusMergeHistograms.py
hplusMergeHistograms.py --includeTasks WZ --filesInEOS -v
hplusMergeHistograms.py --filesInEOS --deleteMergedFilesFirst -s

Useful Links:
https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsChFullyHadronic
'''

#================================================================================================
# Import Modules
#================================================================================================
import os, re
import sys
import glob
import shutil
import subprocess
from optparse import OptionParser
import tarfile
import getpass
import socket
import time

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

import HiggsAnalysis.NtupleAnalysis.tools.multicrab as multicrab
from HiggsAnalysis.NtupleAnalysis.tools.ShellStyles import *

#================================================================================================
# Global Definitions
#================================================================================================
re_histos = []
re_se = re.compile("newPfn =\s*(?P<url>\S+)")
replace_madhatter = ("srm://madhatter.csc.fi:8443/srm/managerv2?SFN=", "root://madhatter.csc.fi:1094")

#================================================================================================ 
# Class Definition
#================================================================================================ 
from functools import wraps
import errno
import os
import signal

class MulticrabTask:
    def __init__(self, multicrabDir, crabDirs, opts):
        '''
        Constructor
        '''
        Verbose("MulticrabTask:__init__()", True)
        self.multicrabDir    = multicrabDir
        self.crabDirs        = crabDirs
        self.nCrabTasks      = len(crabDirs)
        self.mergeFileMap    = {}
        self.mergeSizeMap    = {}
        self.mergeTimeMap    = {}
        self.cleanTime       = {}
        self.puTime          = {}
        self.HOST            = socket.gethostname()
        self.opts            = opts
        self.crabTaskObjects = []
        return

    def AddCrabTaskObject(self, crabTask):
        crabTaskName = crabTask.GetTaskName()

        for c in self.crabTaskObjects:
            if c.GetTaskName() == crabTaskName:
                c = crabTask
                return
        self.crabTaskObjects.append(crabTask)
        return

    def GetCrabTaskObjects(self):
        return self.crabTaskObjects

    def GetCrabTaskObject(self, crabTaskName):
        for c in self.crabTaskObjects:
            if c.GetCrabTaskName() == crabTaskName:
                return c
        raise Exception("Could not find CRAB task with name \"%s\" in my list of CRAB tasks" % (crabTaskName))


class CrabTask:
    def __init__(self, multicrabDir, taskName, logFiles, rootFiles, opts):
        '''
        Constructor
        '''
        Verbose("CrabTask:__init__()", True)
        self.multicrabDir     = multicrabDir
        self.taskName         = taskName
        self.logFiles         = self.logFilesEOS = [self.taskName + "/results/" + os.path.basename(x) for x in logFiles]
        self.logFilesEOS      = logFiles
        self.rootFiles        = [self.taskName + "/results/" + os.path.basename(x) for x in rootFiles]
        self.rootFilesEOS     = rootFiles
        self.mergedFiles      = []
        self.mergedFilesEOS   = []
        self.preMergedFiles   = []
        self.mergedToInputMap = {}
        self.mergedToSizeMap  = {}
        self.taskDir          = os.path.dirname(logFiles[0].replace("/log", ""))
        self.HOST             = socket.gethostname()
        self.opts             = opts
        self.mergeTimeMap     = {} # mergeFile -> mergeTime  (in seconds)
        self.cleanTimeMap     = {} # mergeFile -> cleanTime  (in seconds)
        self.puTimeMap        = {} # mergeFile -> pileupTime (in seconds)
        return

    def MakeMergedToMergeTimePair(self, mergeName, mergeTime):
        if mergeName in self.mergeTimeMap:
            raise Exception("Cannot map the merged ROOT file with clean time %s. Key already exists in the dictionary!" % (mergeName, mergeTime))
        self.mergeTimeMap[mergeName] = mergeTime
        return

    def MakeMergedToCleanTimePair(self, mergeName, cleanTime):
        if mergeName in self.cleanTimeMap:
            raise Exception("Cannot map the merged ROOT file with clean time %s. Key already exists in the dictionary!" % (mergeName, cleanTime))
        self.cleanTimeMap[mergeName] = cleanTime
        return

    def MakeMergedToPileupTimePair(self, mergeName, puTime):
        if mergeName in self.puTimeMap:
            raise Exception("Cannot map the merged ROOT file with clean time %s. Key already exists in the dictionary!" % (mergeName, puTime))
        self.puTimeMap[mergeName] = puTime
        return

    def MakeMergedToInputPair(self, mergeName, inputFileList):
        if mergeName in self.mergedToInputMap:
            raise Exception("Cannot map the merged ROOT file with name %s to a list of input ROOT files. Key already exists in the dictionary!" % (mergeName))
        self.mergedToInputMap[mergeName] = inputFileList
        return

    def GetInputFilesForMergeFile(self, mergeName):
        if mergeName not in self.mergedToInputMap:
            raise Exception("Key %s does not exist in the dictionary!" % (mergeName))
        return self.mergedToInputMap[mergeName]

    def MakeMergedToSizePair(self, mergeName, fileSize):
        if mergeName in self.mergedToSizeMap:
            raise Exception("Cannot map the merged ROOT file with name %s to a file size. Key already exists in the dictionary!" % (mergeName))
        self.mergedToSizeMap[mergeName] = fileSize
        return

    def GetTotalMergeTime(self):
        dt = 0
        for k in self.mergeTimeMap:
            dt += self.mergeTimeMap[k]
        return dt

    def GetTotalCleanTime(self):
        dt = 0
        for k in self.cleanTimeMap:
            dt += self.cleanTimeMap[k]
        return dt

    def GetTotalPileupTime(self):
        dt = 0
        for k in self.puTimeMap:
            dt += self.puTimeMap[k]
        return dt

    def GetTotalTime(self):
        dt = 0
        dt += self.GetTotalMergeTime()
        dt += self.GetTotalCleanTime()
        dt += self.GetTotalPileupTime()
        return dt

    def GetSizeForMergeFile(self, mergeName):
        '''
        Size is in GB by default
        '''
        if mergeName not in self.mergedToSizeMap:
            raise Exception("Key %s does not exist in the dictionary!" % (mergeName))
        return self.mergedToSizeMap[mergeName]

    def GetTotalMergeSize(self):
        '''
        Total size of all merged files for
        the given CRAB task (in GB by default)
        '''
        size = 0
        for k in self.mergedToSizeMap:
            size += self.mergedToSizeMap[k]
        return size

    def SetMergedFiles(self, mergedFiles):
        self.mergedFiles = mergedFiles
        return

    def SetMergedFilesEOS(self, mergedFiles):
        self.mergedFilesEOS = mergedFiles
        return

    def AppendToMergedFiles(self, mergedFile):
        self.mergedFiles.append(mergedFile)
        return

    def AppendToMergedFilesEOS(self, mergedFile):
        self.mergedFilesEOS.append(mergedFile)
        return

    def GetTaskDir(self):
        return self.taskDir

    def GetTaskName(self):
        return self.taskName

    def GetLogFiles(self):
        if self.opts.filesInEOS:
            return self.logFilesEOS
        else:
            return self.logFiles        

    def GetRootFiles(self):
        if self.opts.filesInEOS:
            return self.rootFilesEOS
        else:
            return self.rootFiles

    def GetMergedFiles(self):
        if self.opts.filesInEOS:
            return self.mergedFilesEOS
        else:
            return self.mergedFiles

    def SetPreMergedFiles(self, preMergedFiles):
        self.preMergedFiles = preMergedFiles
        return

    def GetPreMergedFiles(self):
        return self.preMergedFiles
    
    def GetTaskName(self):
        return self.taskName


class TimeoutError(Exception):
    '''
    https://stackoverflow.com/questions/11901328/how-to-timeout-function-in-python-timeout-less-than-a-second
    '''
    pass

def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.setitimer(signal.ITIMER_REAL,seconds) #used timer instead of alarm
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result
        return wraps(func)(wrapper)
    return decorator


class ExitCodeException(Exception):
    '''
    Exception for non-succesful crab job exit codes
    '''
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message

#================================================================================================
# Function Definitions
#================================================================================================
def DeleteTaskMergedRootFles(dirPath, taskName, opts):
    '''
    This command will clean a task directory in from pre-existing merged ROOT files.
    This is useful when the mergign process was interrupted for some reason or you would
    like to re-merge ROOT files with a different set of options (maxFileSize, filePerMerge, ..)
    or just want to avoid overwriting pre-existing merged ROOT files.
    '''
    Verbose("DeleteTaskMergedRootFiles()", True)

    files = GetTaskMergedRootFiles(taskName, True, opts)
    
    Verbose("Found %d merged ROOT files in dir %s:" % (len(files), dirPath), True)
    cmd_ls = "ls"
    if opts.filesInEOS:
        cmd_ls = ConvertCommandToEOS("ls", opts)
    cmd_ls += " %s" % (dirPath)

    # Print contents of task dir (before)?
    Verbose(cmd_ls, True)
    ret = Execute(cmd_ls)
    for i, r in enumerate(ret, 1):
        Verbose(r)

    # For-loop: All merged ROOT files of task 
    for index, f in enumerate(files,1):
        fName = os.path.basename(f)
        cmd   = "rm" 
        if opts.filesInEOS:
            cmd = ConvertCommandToEOS(cmd, opts)
        cmd += " %s" % (f)
        Verbose(cmd)
        ret = Execute(cmd)
        PrintProgressBar("Delete files", index-1, len(files), "[" + fName + "]")
    FinishProgressBar()

    # Print contents of task dir (after)?
    Verbose(cmd_ls, True)
    ret = Execute(cmd_ls)
    for i, r in enumerate(ret, 1):
        Verbose(r)
    return

def AskUser(msg, printHeader=False):
    '''
    Prompts user for keyboard feedback to a certain question. 
    Returns true if keystroke is \"y\", false otherwise.
    '''
    Verbose("AskUser()", printHeader)
    
    fName = __file__.split("/")[-1]

    Print(msg, printHeader)
    keystroke = raw_input("\t(y/n): ")
    if (keystroke.lower()) == "y":
        return True
    elif (keystroke.lower()) == "n":
        return False
    else:
        AskUser(msg)


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
    if printHeader==True:
        print "=== ", fName
        print "\t", msg
    else:
        print "\t", msg
    return

def FinishProgressBar():
    Verbose("FinishProgressBar()")
    sys.stdout.write('\n')
    return


def PrintProgressBar(taskName, iteration, total, suffix = ""):
    '''
    Call in a loop to create terminal progress bar
    @params:
    iteration   - Required  : current iteration (Int)
    total       - Required  : total iterations (Int)
    prefix      - Optional  : prefix string (Str)
    suffix      - Optional  : suffix string (Str)
    barLength   - Optional  : character length of bar (Int)
    '''
    Verbose("PrintProgressBar()")

    iteration   += 1 # since what is passed is the index of the file (starts from zero) - fixme
    barLength    = 20
    percents     = 100 * (iteration / float(total))
    filledLength = int(round(barLength * iteration / float(total)))
    bar          = '=' * filledLength + '-' * (barLength - filledLength)
    #align        = "{:<30} {:<20} {:<6} {:<50} {:^1}" #wth pbar
    align        = "{:<40} {:<6} {:<50} {:^1}"
    suffix       = "[" + suffix + "]"
    percentStr   = "%0.1f" % (percents) + " %"

    # "\r" = carriage return ( takes the cursor to the beginning of the line)
    if percents < 100.0:
        #msg = align.format("\t" + taskName, bar, percentStr, suffix, "\r") 
        msg = align.format("\t" + taskName, percentStr, suffix, "\r") 
    else:
        #msg = align.format("\t" + taskName, bar, SuccessStyle() + percentStr + NormalStyle(), suffix, "\r") 
        msg = align.format("\t" + taskName, SuccessStyle() + percentStr + NormalStyle(), suffix, "\r") 
    sys.stdout.write(msg)
    sys.stdout.flush()
    return


def histoToDict(histo):
    '''
    '''
    ret = {}
    
    for bin in xrange(1, histo.GetNbinsX()+1):
        ret[histo.GetXaxis().GetBinLabel(bin)] = histo.GetBinContent(bin)    
    return ret


def GetLocalOrEOSPath(logFile, opts):
    '''
    This function was created due to problems encountered when working on LXPLUS 
    with the --filesInEOS option. Basically, although files existed on EOS it 
    gave an error that they did not exist. So I wrote this little hack to copy the 
    files locally and then read it.
    It returns either the local or EOS path, whichever necessary. 

    WARNING! If the file is copied locally it must then be removed
    '''
    Verbose("GetLocalOrEOSPath()", True)
    
    if "fnal" in socket.gethostname():
        return False, logFile
    
    localCopy = False
    if not FileExists(logFile, opts):
        raise Exception("Cannot assert if job succeeded as file %s does not exist!" % (logFile) )

    try:
        Verbose("Attempting to open file %s" % (logFile) )
        f = open(GetXrdcpPrefix(opts) + logFile) 
    except IOError as e:
        errMsg = "I/O error({0}): {1} %s".format(e.errno, e.strerror) % (logFile)
        Verbose(errMsg)
        # For unknown reasons on LXPLUS EOS the files cannot be found, even if it exists
        if opts.filesInEOS:
            Verbose("File %s could not be found/read on EOS. Attempting to copy it locally and then read it" % (logFile) )
            
            if "fnal" in socket.gethostname():
                srcFile  = "root://cmseos.fnal.gov/" + logFile #
            else:
                srcFile  = GetXrdcpPrefix(opts) + logFile
            
            destFile = os.path.basename(logFile)
            cmd      = "xrdcp %s %s" % (srcFile, destFile)
            Verbose(cmd)
            ret = Execute(cmd)
            logFile = os.path.join(os.getcwd(), os.path.basename(logFile) )
            localCopy = True
            return localCopy, logFile
        else:
            raise Exception(errMsg)
    return localCopy, logFile


def AssertJobSucceeded(logFile, allowJobExitCodes, opts):
    '''
    Given crab job stdout file, ensure that the job succeeded
    \param logFile   Path to crab job stdout file
    \param allowJobExitCodes  Consider jobs with these non-zero exit codes to be succeeded
    If any of the checks fail, raises ExitCodeException
    '''
    Verbose("AssertJobSucceeded()", True)

    if opts.skipVerify:
        return
    
    localCopy, logFile = GetLocalOrEOSPath(logFile, opts)

    re_exe = re.compile("process\s+id\s+is\s+\d+\s+status\s+is\s+(?P<code>\d+)")
    re_job = re.compile("JobExitCode=(?P<code>\d+)")

    exeExitCode = None
    jobExitCode = None
    
    Verbose("Checking whether file %s is a tarfile" % (logFile) )
    if tarfile.is_tarfile(logFile):
        Verbose("File %s is a tarfile" % (logFile) )
        fIN = tarfile.open(logFile)
        log_re = re.compile("cmsRun-stdout-(?P<job>\d+)\.log")

        #For-loop: All tarfile contents (=members)
        for member in fIN.getmembers():

            # Extract the tarball
            f = fIN.extractfile(member)
            match = log_re.search(f.name)

            # If "cmsRun-stdout*.log" file is found
            if match:
                
                # For-loop: All lines in file
                for line in f:
                    m = re_exe.search(line)
                    if m:
                        exeExitCode = int(m.group("code"))
                        continue
                    m = re_job.search(line)
                    if m:
                        jobExitCode = int(m.group("code"))
                        continue
        fIN.close()
    else:
        Verbose("File %s is not a tarfile" % (logFile) )

    # If log file was copied locally remove it!
    if localCopy:
        Verbose("Removing local copy of stdout tarfile %s" % (logFile) )
        cmd = "rm -f %s" % (logFile)
        Verbose(cmd)
        ret = Execute(cmd)

    jobExitCode = exeExitCode
    if exeExitCode == None:
        #raise ExitCodeException("File %s, No exeExitCode" % (logFile) )
        Verbose("File %s, No exeExitCode. Will be treated like a job with non-zero exitcode" % (logFile), False)
    if jobExitCode == None:
        #raise ExitCodeException("File %s, No jobExitCode" % (logFile) )
        Verbose("File %s, No jobExitCode. Will be treated like a job witn non-zero exitcode" % (logFile), False)
    if exeExitCode != 0:
        Verbose("File %s, executable exit code is %s" % (logFile, exeExitCode) )
    if jobExitCode != 0 and not jobExitCode in allowJobExitCodes:
        Verbose("File %s, job exit code is %s" % (logFile, jobExitCode) )
    return


def getHistogramFile(logFile, opts):
    '''
    First asserts that job has succeeeded
    Then looks insider log-file tarball, unpacks it on the fly 
    and looks for the name of the ROOT file associated.
    '''
    Verbose("getHistogramFile()", True)

    Verbose("Asserting that job succeeded by reading file %s" % (logFile), False )
    AssertJobSucceeded(logFile, opts.allowJobExitCodes, opts)
    histoFile = None

    Verbose("Asserting that file %s is a tarball" % (logFile) )
    if tarfile.is_tarfile(logFile):
        fIN = tarfile.open(logFile)
        log_re = re.compile("cmsRun-stdout-(?P<job>\d+)\.log")

        # For-loop: All tarball members (contents)
        for member in fIN.getmembers():
            Verbose("Looking for cmsRun-stdout-*.log files in tarball memember file %s" % (member) )
            f = fIN.extractfile(member)
            match = log_re.search(f.name)
            if match:
                histoFile = "miniaod2tree_%s.root" % match.group("job")
        fIN.close()
    else:
        f = open(logFile)
        for line in f:
            for r in re_histos:
                m = r.search(line)
                if m:
                    histoFile = m.group("file")
                    break
            if histoFile is not None:
                 break
        f.close()
    return histoFile


def getHistogramFileSE(logFile, opts):
    '''
    -> OBSOLETE <-
    '''
    Verbose("getHistogramFileSE()", True)

    Verbose("Asserting that job succeeded by reading file %s" % (logFile), False )
    AssertJobSucceeded(logFile, opts.allowJobExitCodes, opts)
    histoFile = None

    # Open the "logFile"
    f = open(logFile)

    # For-loop: All lines in file "logFile"
    for line in f:
        m = re_se.search(line)
        if m:
            histoFile = m.group("url")
            break
    f.close()

    if histoFile != None:
        if not replace_madhatter[0] in histoFile:
            raise Exception("Other output SE's than madhatter are not supported at the moment (encountered PFN %s)"%histoFile)
        histoFile = histoFile.replace(replace_madhatter[0], replace_madhatter[1])
    return histoFile


def getHistogramFileEOS(logFile, opts):
    '''
    "r"   Open text file for reading. The stream is positioned at the
    beginning of the file.

    "w"   Truncate file to zero length or create text file for writing.
    The stream is positioned at the  beginning of the file.
    
    "w+"  Open for reading and writing. The stream is positioned at the 
    beginning of the file.

    "a"  Open for writing.  The file is created if it does not exist.  
    The stream is positioned at the beginning of the file.

    "a+"  Open for reading and writing.  The file is created if it does not
    exist.  The stream is positioned at the end of the file.  Subse-
    quent writes to the file will always end up at the then current
    end of file, irrespective of any intervening fseek(3) or similar.
    '''
    Verbose("getHistogramFileEOS()", True)

    Verbose("Asserting that job succeeded by reading file %s" % (logFile), False )
    AssertJobSucceeded(logFile, opts.allowJobExitCodes, opts)

    # Open the "logFile"
    histoFile  = None
    logFileEOS = logFile
    localCopy, logFile = GetLocalOrEOSPath(logFile, opts)

    # Get the jobId with regular expression
    log_re = re.compile("cmsRun_(?P<job>\d+)\.log.tar.gz")
    match = log_re.search(logFile)
    #match = log_re.search(f.name)
    if match:
        jobId     = match.group("job")
        output    = "miniaod2tree_%s.root" % (jobId)
        histoFile = logFileEOS.rsplit("/", 2)[0] + "/" + output
    else:
        Verbose("Could not determine the jobId of file %s. match = " % (logFile, match) )
    
    if localCopy:
        Verbose("Removing local copy of stdout tarfile %s" % (logFile) )
        cmd = "rm -f %s" % (logFile)
        Verbose(cmd)
        ret = Execute(cmd)

    Verbose("The output file from job with id %s for task %s is %s" % (jobId, logFile.split("/")[0], histoFile) )
    return histoFile
    

def GetHistogramFile(taskName, f, opts):
    '''
    '''
    Verbose("GetHistogramFile()", True)
    histoFile = None

    if opts.filesInEOS:
        histoFile = getHistogramFileEOS(f, opts)
        if histoFile != None:
            Verbose("The ROOT file for task %s is %s." % (taskName, histoFile) )
            return histoFile
        else:
            Print("Task %s, skipping job %s: input root file not found from stdout" % (taskName, os.path.basename(f)) )
    else:
        histoFile = getHistogramFile(f, opts)
        if histoFile != None:
            path = os.path.join(os.path.dirname(f), histoFile)
            if os.path.exists(path):
                return histoFile
            else:
                Verbose("Task %s, skipping job %s: input root file found from stdout, but does not exist" % (taskName, os.path.basename(f) ) )
                return None
        else:
            Verbose("Task %s, skipping job %s: input root file not found from stdout" % (taskName, os.path.basename(f) ))
    return histoFile


def ConvertTasknameToEOS(taskName, opts):
    '''
    Get the full dataset name as found EOS.
    '''
    Verbose("ConvertTasknameToEOS()", False)
    
    # Variable definition
    crabCfgFile   = None
    taskNameEOS   = None

    # Get the crab cfg file for this task 
    crabCfgFile = "crabConfig_%s.py" % (taskName)
    fullPath    =  os.getcwd() + "/" + crabCfgFile
    
    if not os.path.exists(fullPath):
        raise Exception("Unable to find the file crabConfig_%s.py." % (taskName) )

    # For-loop: All lines in cfg file
    for l in open(fullPath): 
        keyword = "config.Data.inputDataset = "
        if keyword in l:
            taskNameEOS = l.replace(keyword, "").split("/")[1]

    if taskNameEOS == None:
        raise Exception("Unable to find the crabConfig_<dataset>.py for task with name %s." % (taskName) )

    Verbose("The conversion of task name %s into EOS-compatible is %s" % (taskName, taskNameEOS) )
    return taskNameEOS


def WalkEOSDir(taskName, pathOnEOS, opts): #fixme: bad code 
    '''
    Looks inside the EOS path "pathOnEOS" directory by directory.
    Since OS commands do not work on EOS, I have written this function
    in a vary "dirty" way.. hoping to make it more robust in the future!

    WARNING! Use with caution. If a given task has 2 sub-directories 
    (e.g. same sample but 2 different multicrab submissions) before the
    output files this will fail. The reason is that the function is currently
    written to assume that each directory has only 1 subdirectory.
    '''
    Verbose("WalkEOSDir()", True)
    
    # Listing all files under the path
    cmd = ConvertCommandToEOS("ls", opts) + " " + pathOnEOS
    Verbose(cmd)
    dirContents = Execute(cmd)

    # Added this dirt code to fix problem with "ext1" datasets (WZ, WZ_ext1)
    # Retured 2 directories (crab_WZ, crab_WZ_ext1)
    if len(dirContents) > 1:
        keep = "crab_" + taskName
        for d in dirContents:
            if "crab_" in d:
                if d == keep:
                    continue
                else:
                    dirContents.remove(d)

    if "symbol lookup error" in dirContents[0]:
        raise Exception("%s.\n\t%s." % (cmd, dirContents[0]) )

    #Verbose("Walking the EOS directory %s with contents:\n\t%s" % (pathOnEOS, "\n\t".join(dirContents)), False)
    Verbose("Walking the EOS directory %s:" % (pathOnEOS), False)

    # A very, very dirty way to find the deepest directory where the ROOT files are located!
    if len(dirContents) == 1:
        subDir = dirContents[0]
        Verbose("Found sub-directory %s under the EOS path %s" % (subDir, pathOnEOS) )
        pathOnEOS = WalkEOSDir(taskName, pathOnEOS + "/" + subDir, opts)
    else:
        rootFiles = []
        for d in dirContents:
            subDir = d 
            if "crab_"+taskName in subDir:
                pathOnEOS = WalkEOSDir(taskName, pathOnEOS + "/" + subDir, opts)
            else:
                pass
        
        for f in dirContents:
            if ".root" not in f:
                continue
            else:
                rootFiles.append(pathOnEOS + "/" + f)
        pathOnEOS += "/"
        Verbose("Reached end of the line. Found %s ROOT files under %s."  % (len(rootFiles), pathOnEOS))
    return pathOnEOS


def ConvertCommandToEOS(cmd, opts):
    '''
    Convert a given command to EOS-path. Used when working solely with EOS
    and files are not copied to local working directory
    '''
    Verbose("ConvertCommandToEOS()", True)
    
    # Define a map mapping bash command with EOS commands
    cmdMap = {}
    cmdMap["ls"]    = "eos ls"
    cmdMap["ls -l"] = "eos ls -l"
    cmdMap["rm"]    = "eos rm"
    cmdMap["size"]  = "eos find --size"

    # EOS commands differ on LPC!
    if "fnal" in socket.gethostname():
        # Define alias for eos (broken by cmsenv)
        eosAlias = "eos root://cmseos.fnal.gov "
        for key in cmdMap:
            cmdMap[key] = cmdMap[key].replace("eos", eosAlias)

    # Currect "eos" alias being broken on lxplus after cmsenv is set
    if "lxplus" in socket.gethostname():
        # Define alias for eos (broken by cmsenv)
        eosAlias = "/afs/cern.ch/project/eos/installation/0.3.84-aquamarine/bin/eos.select "
        for key in cmdMap:
            cmdMap[key] = cmdMap[key].replace("eos", eosAlias)

    if cmd not in cmdMap:
        raise Exception("Could not find EOS-equivalent for cammand %s." % (cmd) )

    return cmdMap[cmd]

def Execute(cmd):
    '''
    Executes a given command and return the output.
    '''
    # Uncomment the line below to force function to Timeout after 20 seconds
    Verbose("Execute()" , True)
    Verbose("%s" % (cmd), False)    
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    stdin  = p.stdin
    stdout = p.stdout
    ret    = []
    for line in stdout:
        ret.append(line.replace("\n", ""))
    stdout.close()
    Verbose("\t%s" % ("\n\t".join(ret)) )
    return ret


def GetEOSHomeDir(opts):
    '''
    '''
    Verbose("GetEOSHomeDir()", True)
    #home = "/store/user/%s/CRAB3_TransferData" % (getpass.getuser())
    
    HOST = socket.gethostname()
    if "fnal" in HOST:
        prefix = "/eos/uscms"
        # prefix = "" #do NOT use this "FUSE mount" as it fails for multiple files
    elif "lxplus" in HOST:
        prefix = ""
    else:
        raise Exception("Unsupported host %s" % (HOST) )
    home = prefix + "/store/user/%s/CRAB3_TransferData/%s" % (getpass.getuser(), opts.dirName)
    return home


def ConvertPathToEOS(taskName, fullPath, path_postfix, opts, isDir=False):
    '''
    Takes as input a path to a file or dir of a given multicrab task stored locally
    and converts it to the analogous path for EOS.
    '''
    Verbose("ConvertPathToEOS()", True)
 
    path_prefix = GetEOSHomeDir(opts)
    if not isDir:
        #taskName      = fullPath.split("/")[0]
        fileName      = fullPath.split("/")[-1]
    else:
        taskName      = fullPath
        fileName      = ""

    Verbose("Converting %s to EOS (taskName = %s, fileName = %s)" % (fullPath, taskName, fileName) )
    taskNameEOS   = ConvertTasknameToEOS(taskName, opts)
    pathEOS       = WalkEOSDir(taskName, path_prefix + "/" + taskNameEOS, opts) # + "/"
    fullPathEOS   = pathEOS + path_postfix + fileName
    Verbose("Converted %s (default) to %s (EOS)" % (fullPath, fullPathEOS) )
    return fullPathEOS


def SplitRootFiles(taskName, files, opts):
    '''    
    Split all output ROOT files into small groups of files to be merged
    '''
    Verbose("SplitRootFiles()")

    i   = 0
    ret = []
    MB  = 1000000
    GB  = 1000*MB

    # Default value is -1
    if opts.filesPerMerge < 0:
        maxsize = opts.maxFileSize*GB
        sumsize = 0
        firstFile = 0

        # For-loop: All files (with ifile counter)
        for ifile, f in enumerate(files):
            
            # Update Progress bar
            PrintProgressBar("Split input ROOT files", ifile, len(files), os.path.basename(f))

            # Calculate cumulative size (in Bytes)
            fileSize = GetFileSize(f, opts, False) 
            if not fileSize == None:
                sumsize +=  fileSize
            Verbose("File %s has a size of %s (sumsize=%s)." % (f, fileSize, sumsize) )

            # Impose upper limit on file size
            if sumsize > maxsize:
                ret.append( (i, files[firstFile:ifile]) )
                i += 1
                sumsize = 0
                firstFile = ifile
            if ifile == len(files)-1:
                ret.append( (i, files[firstFile:]) )
    # User-defined value
    else:
        def beg(ind):
            return ind*opts.filesPerMerge
        def end(ind):
            return (ind+1)*opts.filesPerMerge
        while beg(i) < len(files):
            ret.append( (i, files[beg(i):end(i)]) )
            i += 1

    # Flush stdout
    FinishProgressBar()

    # Remove empty tuples (Some rare Instances where we had (0, [])
    splitFiles = filter(lambda x: len(x[1])!=0, ret)

    # Print the tuples
    if not opts.verbose:
        return splitFiles
    else:
        align = "{:<3} {:<100}"
        msg   = "\n"
        # For-loop: All Tuple pair
        for x in splitFiles:
            msg += align.format(x[0], x[1]) + "\n"
            Verbose("Splitted files as follows:%s" % (msg) )
        Verbose("Returning a %s-long list of tuples" % (len(splitFiles)) )
        return splitFiles


def GetFileSize(filePath, opts, convertToGB=True):
    '''
    Return the file size, irrespective of whether 
    it is located locally or on EOS.
    '''
    HOST = socket.gethostname()
    
    Verbose("Determining size for file %s (host=%s)" % (filePath, HOST) )
    if opts.filesInEOS:
        if "fnal" in HOST:
            cmd = ConvertCommandToEOS("ls -l", opts) + " " + filePath
            ret = Execute("%s" % (cmd) )[0].split()
            # Print("\n\t".join(ret) ) #fixme: on LPC, "size" during merging returns zero for MERGED files. not a script bug.
            
            # Store all values
            permissions = ret[0]
            unkownVar   = ret[1]
            username    = ret[2]
            group       = ret[3]
            size        = ret[4]
            month       = ret[5]
            dayOfMonth  = ret[6]
            time        = ret[7]
            filename    = ret[8] # or ret[-1]

            # Get the size as float
            error = False
            for msg in ret:
                if "No such file" in msg: # No such file..
                    error = True
            if error:
                size = -1.0
            else:
                size = float(size)
                
            if size == 0:
                Verbose("On FNAL's LPC the size of merged files after merging is quoted to be indeed  zero (althought it is not). This is NOT a script bug.")

        elif "lxplus" in HOST:
            eos  = "/afs/cern.ch/project/eos/installation/0.3.84-aquamarine/bin/eos.select" #simply "eos" will not work
            cmd  = "%s find --size %s" % (eos, filePath)
            Verbose(cmd)
            ret  = Execute("%s" % (cmd) )

            # Get the size as float
            error = False
            for msg in ret:
                if "error" in msg:
                    error = True
            if error:
                size = -1.0
            else:
                size_str = ret[0].split()[-1].rsplit("size=")[-1]
                size     = float(size_str)
        else:
            raise Exception("Unsupported host %s" % (HOST) )
    else:
        if os.path.exists(filePath):
            size = os.stat(filePath).st_size
        else:
            return None

    # Convert Bytes to Giga-Bytes (GB)
    sizeGB = size/1024.0/1024.0/1024.0

    Verbose("Determined size for file %s to be %s Bytes (%s GB)" % (filePath, size, sizeGB) )
    if convertToGB:
        return sizeGB
    else:
        return size


def GetHaddCommand(opts, mergeName, inputFiles, path_prefix=""):
    Verbose("GetHaddCommand()", True)
    if len(inputFiles) < 1:
        raise Exception("Attempting to merge 0 files! Somethings was gone wrong!")
    
    if path_prefix.endswith("/"):
        mergeNameNew  = path_prefix[:-1] + mergeName
    else:
        mergeNameNew = mergeName
    
    inputFilesNew = []
    # For-loop: All input files
    for f in inputFiles:
        inputFilesNew.append(path_prefix + f)                               

    if type(inputFilesNew) != list:
        inputFilesNew = [inputFilesNew]
    Verbose("Creating file %s from the following files:\n\t%s" % (mergeNameNew, "\n\t".join(inputFilesNew)) )

    # Construct the ROOT-file merge command (hadd)
    cmd = ["hadd"]

    # Pass "-f" argument to force re-creation of output file.
    if opts.overwrite:
        cmd.append("-f") 
    cmd.append(mergeNameNew)
    cmd.extend(inputFilesNew)

    # If under test-mode do nothing
    if opts.test:
        return ""
    else:
        return cmd


def hadd(opts, mergeName, inputFiles, path_prefix=""):
    '''
    '''
    Verbose("hadd()", True)
    
    # Get the command to be executedq
    cmd = GetHaddCommand(opts, mergeName, inputFiles, path_prefix)

    # If under test-mode do nothing
    if opts.test:
        return 0
    else:
        Verbose(" ".join(cmd), True)

    args = {}
    if not opts.verbose:
        args = {"stdout": subprocess.PIPE, "stderr": subprocess.STDOUT}

    # Go ahead and Do the merging
    p   = subprocess.Popen(cmd, **args)
    out = p.communicate()[0]
    ret = p.returncode

    # Check the return code of the cmd-execution
    if ret != 0:
        if not opts.verbose:
            print out
        print "Merging failed with exit code %d" % ret
        return 1
    return 0

#================================================================================================
# Class Definition 
#================================================================================================
class SanityCheckException(Exception):
    '''
    Check that configInfo/configinfo control bin matches to number of
    input files, in order to monitor a mysterious bug reported by Lauri
    '''
    def __init__(self, message):
        super(SanityCheckException, self).__init__(message)


def sanityCheck(mergedFile, inputFiles):
    '''
    '''
    Verbose("sanityCheck()", True)

    if not os.path.exists(mergedFile):
        return
    histoPath = "configInfo/configinfo" #bin1=control (=number_of_merged-files), bin2=energy (=13*number_of_merged-files)
    Verbose("Investigating %s in merged file %s" % (histoPath, mergedFile) )
    tfile = ROOT.TFile.Open(mergedFile)
    configinfo = tfile.Get(histoPath)
    if configinfo:
	info = histoToDict(configinfo)
        if int(info["control"]) != len(inputFiles):
            raise SanityCheckException("configInfo/configinfo:control = %d, len(inputFiles) = %d" % (int(info["control"]), len(inputFiles)))
    tfile.Close()
    return

    
def delete(fileName, regexp, opts):
    '''
    Delete a folder matching the regular expression "regexp"
    from the fileName passed as argument.

    To open a ROOT file on EOS (LXPLUS):
    TFile *f = TFile::Open("root://eoscms//eos/cms//store/user/attikis/CRAB3_TransferData/WZ_TuneCUETP8M1_13TeV-pythia8/crab_WZ/160921_141816/0000/histograms-WZ-1.root")

    To open a ROOT file on EOS (FNAL):
    TFile *f = TFile::Open("root://cmseos.fnal.gov//store/user/aattikis/CRAB3_TransferData/WWTo4Q_13TeV-powheg/crab_WWTo4Q/160920_123933/0000/miniaod2tree_1.root");

    # Example on LXPLUS:
    f = ROOT.TFile.Open("root://eoscms//eos/cms//store/user/attikis/CRAB3_TransferData/WZ_TuneCUETP8M1_13TeV-pythia8/crab_WZ/160921_141816/0000/histograms-WZ-1.root", "UPDATE") # works
    '''
    Verbose("delete()", False)
    
    # Definitions
    prefix = ""
    if opts.filesInEOS:
        prefix = GetXrdcpPrefix(opts)
    fileMode = "UPDATE"

    # Open the ROOT file
    Verbose("Opening ROOT file %s in %s mode (prefix=%s)" % (fileName, fileMode, prefix) )
    fIN = ROOT.TFile.Open(prefix + fileName, fileMode)
    if fIN == None:
        raise Exception("Could not open ROOT file %s. Does it exist?" % (fileName) )
    fIN.cd()
    keys = fIN.GetListOfKeys()

    # For-loop: All keys in TFILE
    for i in range(len(keys)):
        if keys.At(i):
            keyName = keys.At(i).GetName()
            dir = fIN.GetDirectory(keyName)
            if dir:
                fIN.cd(keyName)
                Verbose("Deleting folder \"%s\" in file %s." % (regexp, fileName) )
                delFolder(regexp)
                fIN.cd()
    delFolder(regexp)
    fIN.Close()
    return


def IsDataRootfile(fileName):
    '''
    Opens ROOT file with name "filename"
    and reads the dataVersion stored inside
    Returns True if dataset is of type "data" 
    or False if dataset is of type "MC"
    '''
    # The check below has already been made at an earlier stage
    # Disable it to speed things up a bit
    if 0: #FileExists(fileName, opts ) == False:
        raise Exception("The file %s does not exist!" % (fileName) )

    # Definitions
    prefix = ""
    if opts.filesInEOS:
        prefix = GetXrdcpPrefix(opts)

    # Open the ROOT file
    fileMode    = "UPDATE"
    nAttempts   = 1
    maxAttempts = 10
    fOUT = None
    while nAttempts < maxAttempts:
        try:
            Verbose("Attempt #%s: Opening ROOT file %s in %s mode (prefix=%s)" % (nAttempts, fileName, fileMode, prefix) )
            fOUT = ROOT.TFile.Open(prefix + fileName, fileMode)
            fOUT.cd()
            break
        except:
            nAttempts += 1
            Print("TFile::Open(%s, %s) failed (%s/%s). Retrying..." % (fileName, fileMode, nAttempts, maxAttempts) )

    # Safety clause
    if fOUT == None:
        raise Exception("TFile::Open(%s, %s) failed" % (prefix + fileName, fileMode) )
    else:
        Verbose("Successfully opened %s in %s mode (after %s attempts)" % (fileName, fileMode, nAttempts) )

    # Definitions
    dataVersion = fOUT.Get("configInfo/dataVersion")
    dv_re = re.compile("data")  
    Verbose("The data version of file %s is %s"   % (fileName, dataVersion.GetTitle()))
    match = dv_re.search(dataVersion.GetTitle())

    # If dataset is not data, do nothing
    if not match:
        return False, fOUT
    else:
        return True, fOUT

def WritePileupHistos(fileName, fOUT, opts):
    '''
    If dataversion is NOT "data", return.
    Otherwise, read the PileUp.root file and
    get 3 PU histograms (pileup, pileup_up variation, pileup_down variation)
    and write them to the fileName passed as argument.
    '''
    #if not IsDataRootfile(fileName):
    #    return
    prefix = ""
    if opts.filesInEOS:
        prefix = GetXrdcpPrefix(opts)

    hPU     = None
    puFile = os.path.join(os.path.dirname(fileName), "PileUp.root")
    if FileExists(puFile, opts):
        Verbose("Opening ROOT file \"%s\"" % (fileName), False)
        fIN     = ROOT.TFile.Open(prefix + puFile)
        hPU     = fIN.Get("pileup")
        hPUup   = fIN.Get("pileup_up")
        hPUdown = fIN.Get("pileup_down")
    else:
        Print("%s not found in %s. Did you run hplusLumiCalc.py? Exit" % (puFile, os.path.dirname(fileName) ) )
        sys.exit()

    # Sanity checks
    if (hPU.Integral() == 0):
        raise Exception("Empty pileup histogram \"%s\" in ROOT file \"%s\". Entries = \"%s\"." % (hPU.GetName(), fIN.GetName(), hPU.GetEntries()) )
    if (hPUup.Integral() == 0):
        raise Exception("Empty pileup histogram \"%s\" in ROOT file \"%s\". Entries = \"%s\"." % (hPUup.GetName(), fIN.GetName(), hPUup.GetEntries()) )
    if (hPUdown.Integral() == 0):
        raise Exception("Empty pileup histogram \"%s\" in ROOT file \"%s\". Entries = \"%s\"." % (hPUdown.GetName(), fIN.GetName(), hPUdown.GetEntries()) )

    # Now write the PU histograms in the input file
    if hPU != None:
        fOUT.cd("configInfo") 
        Verbose("Writing \"configInfo/pileup\" histograms to ROOT file \"%s\"." % (fOUT.GetName()), False)
        hPU.Write("pileup", ROOT.TObject.kOverwrite)
        hPUup.Write("pileup_up", ROOT.TObject.kOverwrite)
        hPUdown.Write("pileup_down", ROOT.TObject.kOverwrite)
    else:
        raise Exception("Could not write the pileup histograms to the output ROOT file \"%s\". hPU == None" % (fOUT.GetName()) )

    # Sanity checks (pileup histo)
    if (hPU.Integral() == 0):
        raise Exception("Empty pileup histogram \"%s\" in ROOT file \"%s\". Entries = \"%s\"." % (hPU.GetName(), fOUT.GetName(), hPU.GetEntries()) )

    # Sanity checks (pileup histos in output ROOT file)
    histos = []
    histos.append("configInfo/pileup")
    histos.append("configInfo/pileup_up")
    histos.append("configInfo/pileup_down")
    for h in histos:
        histo = fOUT.Get(h)
        if histo.Integral() == 0:
            raise Exception("Empty pileup histogram \"%s\" in output ROOT file \"%s\"." % (h, fOUT.GetName()) )
        else:
            Verbose("The histogram \"%s\" in ROOT file \"%s\" has entries=\"%s\", mean=\"%s\", and integral=\"%s\"." % (histo.GetName(), fOUT.GetName(), histo.GetEntries(), histo.GetMean(), histo.Integral() ), False)

    # Close the input/output ROOT files
    Verbose("Closing ROOT file %s." % (fileName) )
    fOUT.Close()
    return


def delFolder(regexp):
    '''
    '''
    Verbose("delFolder()", True)

    # Definitions
    keys    = ROOT.gDirectory.GetListOfKeys()
    del_re  = re.compile(regexp)
    deleted = False

    # For-loop: All keys 
    for i in reversed(range(len(keys))):
        if keys.At(i):
            keyName = keys.At(i).GetName()
            match = del_re.search(keyName)
            if match:
                if not deleted:
                    deleted = True
                else:
                    cycle = keys.At(i).GetCycle()
                    ROOT.gDirectory.Delete(keyName + ";%i" % cycle)
    return


def GetRegularExpression(arg):
    Verbose("GetRegularExpression()", True)
    if isinstance(arg, basestring):
        arg = [arg]
    return [re.compile(a) for a in arg]


def CheckThatFilesExist(taskName, fileList, opts):
    '''
    Counts the number of files passed in the list to see 
    if they all exist!
    '''
    Verbose("CheckThatFilesExist()", True)

    # For-loop: All files in list
    nFiles = len(fileList)
    nExist = 0
    
    # For-loop: All files in the list
    for index, f in enumerate(fileList):
        Verbose("Checking whether file %s exists" % (f) )

        if opts.filesInEOS:
            fileName = ConvertPathToEOS(taskName, f, "", opts, isDir=False)
        else:
            fileName = f

        if FileExists(fileName, opts):
            nExist += 1
        else:
            Verbose("Task %s, file %s not found!" % (taskName, os.path.basename(f)) )

        # Update Progress bar
        PrintProgressBar("Check that ROOT files exist", index, len(fileList), os.path.basename(f))
    FinishProgressBar()

    if nExist != nFiles:
        msg  = "%s, found %s ROOT files but expected %s. Have you already run this script? " % (taskName, nExist, nFiles)
        msg += "Would you like to proceed with the merging anyway?"
        if opts.linksToEOS:
            return False
        else:
            return AskUser(msg, True)
    else:
        return True

def FileExists(filePath, opts):
    '''
    Checks that a file exists by executing the ls command for its full path, 
    or the corresponding "EOS" command if opts.filesInEOS is enabled.
    '''
    Verbose("FileExists()", False)
    
    if "CRAB3_TransferData" in filePath: # fixme: just a better alternative to "if opts.filesInEOS:"
        cmd = ConvertCommandToEOS("ls", opts) + " " + filePath
        ret = Execute("%s" % (cmd) )

        # If file is not found there won't be a list of files; there will be an error message
        errMsg = ""
        if len(ret) > 0:
            errMsg = ret[0]

        if "Unable to stat" in errMsg:
            return False
        elif errMsg == filePath.split("/")[-1]:
            return True
        else:
            raise Exception("This should not be reached! Execution of command %s returned %s" % (cmd, errMsg))
    else:
        if os.path.isfile(filePath):
            return True
        else:
            return False
    return True


def GetCrabDirectories(opts):
    Verbose("GetCrabDirectories()")

    opts2 = None
    crabDirsTmp = multicrab.getTaskDirectories(opts2)
    crabDirs = GetIncludeExcludeDatasets(crabDirsTmp, opts)
    crabDirs = filter(lambda x: "multicrab_" not in x, crabDirs) #remove "multicrab_" directory from list
    return crabDirs


def GetIncludeExcludeDatasets(datasets, opts):
    '''
    Does nothing by default, unless the user specifies a dataset to include (--includeTasks <datasetNames>) or
    to exclude (--excludeTasks <datasetNames>) when executing the script. This function filters for the inlcude/exclude
    datasets and returns the lists of datasets and baseNames to be used further in the program.
    '''
    Verbose("GetIncludeExcludeDatasets()", True)

    # Initialise lists
    includeDatasets = []
    excludeDatasets = []
 
    # Exclude datasets
    if opts.excludeTasks != "":

        exclude = GetRegularExpression(opts.excludeTasks)
        Verbose("Will exclude the following tasks (using re) :%s" % (exclude) )

        # For-loop: All datasets/tasks
        for d in datasets:
            task  = d # GetBasename(d)
            found = False

            # For-loop: All datasets to be excluded
            for e_re in exclude:
                if e_re.search(task):
                    found = True
                    break
            if found:
                continue
            excludeDatasets.append(d)

    # Include datasets
    if opts.includeTasks != "":

        include = GetRegularExpression(opts.includeTasks)
        Verbose("Will include the following tasks (using re) :%s" % (opts.includeTasks) )

        # For-loop: All datasets/tasks
        for d in datasets:
            task  = d #GetBasename(d)
            found = False

            # For-loop: All datasets to be included
            for i_re in include:
                if i_re.search(task):
                    found = True
                    break
            if found:
                includeDatasets.append(d)

    if opts.includeTasks != "" and opts.excludeTasks != "":
        newList =  [x for x in includeDatasets if x in excludeDatasets]
        #newList =  [x for x in includeDatasets if x not in excludeDatasets]
        return newList 
    elif opts.includeTasks != "":
        return includeDatasets
    elif opts.excludeTasks != "":
        return excludeDatasets
    else:
        return datasets


def GetXrdcpPrefix(opts):
    '''
    Returns the prefix for the file address when copying files from EOS.
    For example, a file located in EOS under:
    /store/user/attikis/CRAB3_TransferData/WZ_TuneCUETP8M1_13TeV-pythia8/

    on LXPLUS becomes:
    root://eoscms.cern.ch//eos//cms/store/user/attikis/CRAB3_TransferData/WZ_TuneCUETP8M1_13TeV-pythia8/

    while on LPC becomes:
    root://cmseos.fnal.gov//store/user/attikis/CRAB3_TransferData/WZ_TuneCUETP8M1_13TeV-pythia8/
    '''
    Verbose("GetXrdcpPrefix()")

    if not opts.filesInEOS:
      return ""

    HOST = socket.gethostname()
    path_prefix = ""

    Verbose("Determining prefix for xrdcp for host %s" % (HOST) )
    if "fnal" in HOST:
        #path_prefix = "root://cmsxrootd.fnal.gov/" # doesn't work
        path_prefix = "root://cmseos.fnal.gov//"
        # path_prefix = "" 
    elif "lxplus" in HOST:
        path_prefix = "root://eoscms.cern.ch//eos//cms/"
    else:
        raise Exception("Unsupported host %s" % (HOST) )
    return path_prefix


def GetFileOpenPrefix(opts):
    if not opts.filesInEOS:
      return ""

    HOST = socket.gethostname()
    path_prefix = ""

    Verbose("Determining prefix for opening ROOT files for host %s" % (HOST) )
    if "fnal" in HOST:
        path_prefix = "root://cmseos.fnal.gov/"
    elif "lxplus" in HOST:
        path_prefix = "root://eoscms.cern.ch//eos//cms/"
    else:
        raise Exception("Unsupported host %s" % (HOST) )
    return path_prefix


def GetMergeCommand(mergeName, inputFiles, opts):
    '''
    Command for merging ROOT files, either stored locally or on EOS.
    '''
    Verbose("Attempting to merge:\n\t%s\n\tto\n\t%s." % ("\n\t".join(inputFiles), mergeName) )

    # Initialise variables
    cmd = ""

    if len(inputFiles) < 1:
        raise Exception("Attempting to merge 0 files! Somethings was gone wrong!")
    elif len(inputFiles) == 1:
        if opts.filesInEOS:
            prefix   = GetXrdcpPrefix(opts)
            srcFile  = prefix + inputFiles[0]
            if "fnal" in socket.gethostname():
                srcFile  = srcFile.replace("/eos/uscms/", "") # do not use the FUSE mount
            destFile = prefix + mergeName
            
            # Construct the command to be executed
            cmd  = "xrdcp "
    
            # Need to replace any existing output file?
            if opts.overwrite:
                cmd += "--force "
            cmd += " %s %s" % (srcFile, destFile)
        else:
            if not opts.test:
                cmd = "cp %s %s" % (inputFiles[0], mergeName)
    else:
        if opts.filesInEOS:
            cmd = GetHaddCommand(opts, mergeName, inputFiles, GetXrdcpPrefix(opts) )
        else:
            cmd = GetHaddCommand(opts, mergeName, inputFiles)
    return cmd

@timeout(600) # 600 seconds = 10 minutes for this functon to timeout
def MergeFiles(mergeName, inputFiles, opts):
    '''
    Merges ROOT files, either stored locally or on EOS.
    '''
    Verbose("Attempting to merge:\n\t%s\n\tto\n\t%s." % ("\n\t".join(inputFiles), mergeName) )

    if len(inputFiles) < 1:
        raise Exception("Attempting to merge 0 files! Somethings was gone wrong!")
    elif len(inputFiles) == 1:
        if opts.filesInEOS:
            prefix   = GetXrdcpPrefix(opts)
            srcFile  = prefix + inputFiles[0]
            destFile = prefix + mergeName
            if "fnal" in socket.gethostname():
                srcFile  = srcFile.replace("/eos/uscms/", "")  # do not use the FUSE mount
                destFile = destFile.replace("/eos/uscms/", "") # do not use the FUSE mount
            
            # Construct the command to be executed
            cmd  = "xrdcp"
            # Need to replace any existing output file?
            if opts.overwrite:
                cmd += " --force"
            cmd += " %s %s" % (srcFile, destFile)
            Verbose(cmd)
            ret = Execute(cmd)
            ret = 0
        else:
            Verbose("cp %s %s" % (inputFiles[0], mergeName) )
            if not opts.test:
                shutil.copy(inputFiles[0], mergeName)
            ret=0
    else:
        if opts.filesInEOS:
            ret = hadd(opts, mergeName, inputFiles, GetXrdcpPrefix(opts) )
            Verbose("Done %s (%s GB)." % (mergeName, GetFileSize(mergeName, opts) ), False )
        else:
            ret = hadd(opts, mergeName, inputFiles)    
            Verbose("Done %s (%s GB)." % (mergeName, GetFileSize(mergeName, opts) ), False )

    return ret

def PrintSummary(mcrabTask):
    '''
    Self explanatory
    '''
    # Create the table format
    table    = []
    msgAlign = "{:<3} {:<50} {:^15} {:^15} {:^15} {:^18} {:^18} {:^18} {:^20}"
    header   = msgAlign.format("#", "Dataset", "ROOT Files", "Merged Files", "Total Size", "Merge Time", "Clean Time", "Pileup Time", "Total Time")
    hLine    = "="*len(header)
    table.append("")
    table.append(hLine)
    table.append(header)
    table.append(hLine)
    
    # For-loop: All CRAB Tasks
    for i, task in enumerate(mcrabTask.GetCrabTaskObjects(), 1):
        name       = task.GetTaskName()
        size       = "%0.2f GB" % task.GetTotalMergeSize()
        nInput     = len(task.GetRootFiles())
        nMerged    = len(task.GetMergedFiles())
        mergeTime  = "%0.1f s" % task.GetTotalMergeTime()
        cleanTime  = "%0.1f s" % task.GetTotalCleanTime()
        puTime     = "%0.1f s" % task.GetTotalPileupTime()
        totalTime  = task.GetTotalTime()
        mins, secs = divmod(totalTime, 60)
        row        = msgAlign.format(i, name, nInput, nMerged, size, mergeTime, cleanTime, puTime, "%0.0f min, %0.1f s" % (mins, secs) )
        table.append(row)

    # Print the table
    for l in table:
        print l
    print
    return

def CheckTaskReport(logfilepath, opts):
    '''
    Probes the log-file tarball for a given jobId to
    determine the job status or exit code.
    '''
    if opts.skipVerify:
        return 0

    filePath    = logfilepath
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
                        exitCode = int(exitMatch.group("exitcode"))
                        Verbose("File %s, exitcode is %s" % (member.name, exitCode) )
                        return exitCode
    
    Verbose("File %s, exitcode is %s" % (member.name, -1) )
    return -1


def GetTaskOutputAndExitCodes(taskName, logFiles, opts):
    '''
    Loops over all stdout files of a given CRAB task, to obtain 
    and return the corresponding output files and exit-codes.
    '''
    Verbose("GetTaskOutputAndExitCodes()", True)

    # Definitions
    nMissingFiles = 0
    rootFilesList = []
    exitedJobsList= []
    jobId_re      = re.compile("cmsRun_(?P<jobId>\d+)\.log\.tar\.gz")
    Verbose("Getting output files & exit codes for task %s" % (taskName) )

    # For-loop: All log files of given task
    for index, f in enumerate(logFiles):

        # Find & extract tarball log file and extract the job-id to create the ROOT file name
        histoFile = GetHistogramFile(taskName, f, opts)

        if histoFile != None:
            filePath = DoNotUseFuseMount(histoFile)
            if not filePath.startswith("/"):
                filePath = "/" + filePath
            rootFilesList.append(filePath)
        else:
            nMissingFiles += 1
            Verbose("Task %s, skipping job %s: input ROOT file not found from stdout" % (taskName, os.path.basename(f)) )

        exitcode = CheckTaskReport(f, opts)
        if exitcode != 0:
            exit_match = jobId_re.search(f)
            if exit_match:
                exitedJobsList.append(int(exit_match.group("jobId")))
        
        # Update progress bar
        PrintProgressBar("Assert job status", index, len(logFiles), os.path.basename(f))

    # Flush stdout
    if len(logFiles)>0:
        FinishProgressBar()
    return rootFilesList, nMissingFiles, exitedJobsList


def ExamineExitCodes(taskName, exitedJobs, missingFiles):
    '''
    Examine all exit codes (passed as a list) and determine 
    if there are jobs with problems. 

    Print command for job resubmission.
    '''
    Verbose("ExamineExitCodes()")

    if len(exitedJobs) < 1:
        Print("%s, No jobs with non-zero exit codes" % (taskName), False)
    else:
        exitedJobs_s = ""

        # For-loop: All exit codes
        for i,e in enumerate(sorted(exitedJobs)):
            exitedJobs_s += str(e)
            if i < len(exitedJobs)-1:
                exitedJobs_s += ","
        Print("%s, jobs with non-zero exit codes: %s" % (taskName, len(exitedJobs) ), False)
        Print("crab resubmit %s --jobids %s --force" % (taskName, exitedJobs_s), False)

    if missingFiles > 0:
        Print("jobs with missing files: %s" % missingFiles, False)
    return


def RenameMergeFile(mergeName, opts):
    '''
    Check whether the target merge file already exists or not.
    If it does it does nothing by default, or if the --test option is enabled.
    If the --overwrite option is enabled, the existing file is renamed to <mergeName>.root.backup
    
    Stopped using this since 13 October 2016 (not very useful at the time)
    '''
    Verbose("RenameMergeFile()")

    if opts.test:
        return

    if opts.filesInEOS:
        if opts.overwrite:
            mergeNameNew = mergeName + ".backup"
            Verbose("File %s already exists.\n\tRenaming to %s." % (mergeName, mergeNameNew) )
            fileName    = GetXrdcpPrefix(opts) + mergeName
            fileNameNew = GetXrdcpPrefix(opts) + mergeNameNew
            cp_cmd      = "xrdcp %s %s" % (fileName, fileNameNew)
            Verbose(cp_cmd)
            ret = Execute(cp_cmd)
            # Now remove the original file
            rm_cmd = ConvertCommandToEOS("rm", opts) + " %s" % (mergeName)
            Verbose(rm_cmd)
            ret = Execute(rm_cmd)            
        else:
            Verbose("File %s already exists. Skipping .." % (mergeName) )
    else:
        if opts.overwrite:
            Verbose("mv %s %s" % (mergeName, mergeName + ".backup") )
            shutil.move(mergeName, mergeName + ".backup")
        else:
            Verbose("File %s already exists. Skipping .." % (mergeName) )
    return


def CheckControlHisto(taskName, mergeName, inputFiles):
    '''
    Check that configInfo/configinfo control bin matches to number of
    input files, in order to monitor a mysterious bug reported by Lauri.
    If working on EOS skip this test to speed things up.
    '''
    Verbose("CheckControlHisto()")

    # Skip this to speed things up (especially when in EOS)
    if opts.filesInEOS:
        return

    try:
        sanityCheck(mergeName, inputFiles)
    except SanityCheckException, e:
        Print("%s: %s; disabling input file deletion" % (taskName, str(e)) )
        opts.deleteImmediately = False
        opts.delete = False
    return


def RootFileIsCorrupt(fileName, opts):
    '''
    Check integrity of ROOT File. Return true if file is corrupt, 
    otherwise return false.
    
    https://root.cern.ch/phpBB3/viewtopic.php?t=5906
    '''
    Verbose("RootFileIsCorrupt()", True)
    if fileName == None:
        return False

    # If open in update mode and the function finds something to recover, a new directory header is written to the file.
    prefix = GetXrdcpPrefix(opts)
    fileName = prefix + fileName

    openMode = "UPDATE"
    r = ROOT.TFile.Open(fileName, openMode)
    if not isinstance(r, ROOT.TFile):
        Print("Opened file %s but it is not an instance of ROOT::TFile(). Exit" % (fileName) )
        sys.exit()
        
    Verbose("Opened file %s in mode %s" % (fileName, openMode) )

    ret = False
    if not r:
        Print("File %s does not exist" % (fileName) )
        ret = True
    elif r.IsZombie():
        Print("File %s is Zombie (unusable)" % (fileName) )
        ret = True
    elif r.TestBit(ROOT.TFile.kRecovered):
        Print("File %s has been recovered" % (r.GetName() ) )
        ret = True
    else:
        Verbose("%s succesfully opened" % (r.GetName() ) )
        r.Close()
        ret = False
    return ret
    

def DeleteFiles(taskName, mergeFile, fileList, opts):
    '''
    If the --test option is used, do nothing.
    Otherwise, delete the source files immediately after merging to save disk space.
    '''
    Verbose("DeleteFiles()")
    if opts.test:
        return

    # For-loop: All input files
    for index, f in enumerate(fileList):
        PrintProgressBar("Delete files", index, len(fileList), "[" + os.path.basename(f) + "]")
        if opts.filesInEOS:
            cmd = ConvertCommandToEOS("rm", opts) + " " + f
            Verbose(cmd)
            ret = Execute(cmd)
        else:
            cmd = "rm %s" % f
            Verbose(cmd)
            os.remove(f)
            
    return


def GetDeleteMessage(opts):
    '''
    '''
    Verbose("GetDeleteMessage()")

    deleteMessage = ""
    if opts.delete:
        deleteMessage = " (source files deleted)"
    if opts.deleteImmediately:
        deleteMessage = " (source files deleted immediately)"
    return deleteMessage


def DeleteFolders(filePath, foldersToDelete, opts):
    '''
    Delete folders (TNamed) from merged files (due to merged multiple copies are present)
    '''
    Verbose("DeleteFolders()")

    # if we dont merge, wo dont have any problem with duplicates
    if opts.filesPerMerge == 1:
        Verbose("No need to delete duplicate folders since filesPerMerge = %s" % (opts.filesPerMerge))
        return
        
    Verbose("Will delete the following folders:\n\t%s\n\tfrom file %s" % ("\n\t".join(foldersToDelete), filePath) )
    # For-loop: All folders to be deleted
    for i, folder in enumerate(foldersToDelete, 1):
        Verbose("Deleting folder \"%s\"" % (folder), i==1) 
        delete(filePath, folder, opts)
    return


def GetTaskLogFiles(taskName, opts):
    '''
    Get all the log files for the given CRAB task
    '''
    Verbose("GetTaskLogFiles()", True)
    if opts.filesInEOS:
        pathName = ConvertPathToEOS(taskName, taskName, "log/", opts, isDir=True)
    else:
        pathName = os.path.join(taskName, "results", "cmsRun_*.log.tar.gz")

    Verbose("Obtaining stdout files for task %s from %s" % (taskName, pathName), True)
    logFiles = glob.glob(pathName + "cmsRun_*.log.tar.gz")        

    # Alternative to glob, which for unknown reasons sometimes doesn't work for EOS
    if len(logFiles) < 1:
        msg = "Found %d ROOT files. Retrying with alternative method (not glob)" % (len(rootFilesList))
        Print(NoteStyle() + msg + NormalStyle(), False)
        
        # Get the command & execute it
        cmd = ConvertCommandToEOS("ls", opts) + " " + tmp
        ret = Execute(cmd)
        logFiles = [pathName + f for f in ret if ".log.tar.gz" in f]

    if len(logFiles) < 1:
        #raise Exception("Task %s, could not obtain log files." % (taskName) )
        Verbose("Task %s, could not obtain log files." % (taskName), False)

    # Sort the list naturally (alphanumeric strings). 
    logFiles = natural_sort(logFiles)
    
    Verbose("Found %s ROOT files:\n\t%s" % (len(logFiles), "\n\t".join(logFiles)), True)
    return logFiles
        
def GetTaskRootFiles(taskName, basename, opts):
    '''
    Get all the miniaod*.root files for the given CRAB task
    '''
    Verbose("GetTaskRootFiles()", True)
    if opts.filesInEOS:
        pathName = ConvertPathToEOS(taskName, taskName, "", opts, isDir=True)
    else:
        pathName = os.path.join(taskName, "results", "miniaod*.root")

    Verbose("Obtaining ROOT files for task %s from %s with glob" % (taskName, pathName), True)
    rootFilesList = glob.glob(pathName + "miniaod*.root")

    # Alternative to glob, which for unknown reasons sometimes doesn't work for EOS
    if len(rootFilesList) < 1:
        msg = "Found %d ROOT files. Retrying with alternative method (not glob)" % (len(rootFilesList))
        Print(NoteStyle() + msg + NormalStyle(), False)

        # Get the command & execute it
        cmd = ConvertCommandToEOS("ls", opts) + " " + pathName
        ret = Execute(cmd)
        rootFilesList = [pathName + f for f in ret if "miniaod2tree" in f]

    if len(rootFilesList) < 1:
        #raise Exception("Task %s, could not obtain log files." % (taskName) )
        Verbose("Task %s, could not obtain ROOT files." % (taskName), False)

    # Sort the list naturally (alphanumeric strings)
    rootFilesList = natural_sort(rootFilesList)
    
    # Remove the path form the list
    Verbose("Found %s ROOT files" % (len(rootFilesList) ) )
    if basename:
        filesWithoutPath = []
        for f in rootFilesList:
            filesWithoutPath.append(os.path.basename(f))
        return filesWithoutPath
    else:
        return rootFilesList


def GetTaskMergedRootFiles(taskName, fullPath, opts):
    '''
    Get all the histograms-*.root files for the given CRAB task
    '''
    Verbose("GetTaskMergedRootFiles()", True)
    if opts.filesInEOS:
        path = ConvertPathToEOS(taskName, taskName, "", opts, isDir=True)
    else:
        path = os.path.join(taskName, "results", "histograms-*.root")

    Verbose("Obtaining stdout files for task %s from %s" % (taskName, path), True)
    fileName = "histograms-*.root"
    rootFiles = glob.glob(path + fileName)

    nFiles = len(rootFiles)
    if nFiles < 1:
        msg = "Task %s, found %s ROOT files of type %s with glob under path %s" % (taskName, fileName, nFiles, path)
        Verbose(msg)
    else:
        Verbose("Task %s, Found %s ROOT files of type %s with glob under path %s" % (taskName, fileName, nFiles, path) )

    # Sort the list naturally (alphanumeric strings).
    rootFiles = natural_sort(rootFiles)

    # remove the path
    files = []
    for f in rootFiles:
        if fullPath:
            files.append(f)
        else:
            files.append(os.path.basename(f))
    return files


def GetPreexistingMergedFiles(taskPath, opts):
    '''
    Returns a list with the full path of all pre-existing merged ROOT files
    '''
    if opts.filesInEOS:
        cmd = ConvertCommandToEOS("ls", opts) + " " + taskPath
    else:
        cmd = "ls"  + " " + taskPath
    Verbose(cmd)
    dirContents = Execute(cmd)

    fullPaths = []
    taskPath = taskPath.replace("/eos/uscms", "") # fixme: tmp ugly fix. 
    for f in dirContents:
        fullPaths.append( os.path.join(taskPath, f) )
    preMergedFiles = filter(lambda x: "histograms-" in x, fullPaths)
    return preMergedFiles


def natural_sort(myList): 
    '''
    Function for natural sorting of string list
    '''
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(myList, key = alphanum_key)


def LinkFiles(taskName, fileList):
    '''
    Loops over all files in the list and creates symbolic links
    '''        
    Verbose("Task %s, creating symbolic links" % (taskName))
    # For-loop: All files
    for index, f in enumerate(fileList):
        srcFile  = f
        fName    = "/".join(f.split("/")[-1:])
        destFile = os.path.join(taskName, "results", fName)
        cmd = "ln -s %s %s" % (srcFile, destFile)

        # Create the symbolic link
        if not os.path.isfile(destFile):
            Verbose(cmd)
            print cmd
            #ret = os.system(cmd)
            # ret = Execute(cmd)

        # Update Progress bar
        PrintProgressBar("Create symbolic links ", index, len(fileList), "[" + os.path.basename(destFile) + "]")
    return

def DoNotUseFuseMount(dirPath):
    if "fnal" not in socket.gethostname():
        return dirPath
    else:
        #newPath = dirPath.replace("/eos/uscms", "")
        newPath = dirPath.replace("/eos/uscms", "")
        return newPath

def main(opts, args):

    # Get the multicrab task names (=dir names)
    mcrabDir     = os.path.basename(os.getcwd())
    crabDirs     = GetCrabDirectories(opts)
    nTasks       = len(crabDirs)

    # Sanity check
    msg = "Found %d CRAB task(s) under multiCRAB directory %s" % (nTasks, mcrabDir)
    if 0:
        for i, d in enumerate(crabDirs, 1):
            msg += "\n\t%d) %s" % (i, d)
        msg += "\n"

    if nTasks < 1:
        msg += ". EXIT!"
        Print(ErrorStyle() + msg + NormalStyle())
        sys.exit()
    else:
        Print(msg)
        
    # Create object
    mcrabTask = MulticrabTask(mcrabDir, crabDirs, opts)

    # Construct regular expressions for output files
    global re_histos
    re_histos.append(re.compile("^output files:.*?(?P<file>%s)" % opts.input))
    re_histos.append(re.compile("^\s+file\s+=\s+(?P<file>%s)" % opts.input))
    exit_re = re.compile("/results/cmsRun_(?P<exitcode>\d+)\.log\.tar\.gz")
    
    # For-loop: All task names
    Verbose("Looping over all tasks in %s" % (opts.dirName), True)
    for index, taskName in enumerate(crabDirs, 1):
        
        Print("%s%d/%d: %s" % (HighlightAltStyle(), index, len(crabDirs), taskName + NormalStyle()), index==1)

        # Get the CRAB task log files
        logFiles = GetTaskLogFiles(taskName, opts)
        
        # Create symbolic links for merge files?
        if opts.linksToEOS:
            pass

        # Get the CRAB task's ROOT files
        if opts.skipVerify:
            rootFiles      = GetTaskRootFiles(taskName, False, opts)
            nMissingFiles  = 0
            exitedJobsList = []
        else:
            rootFiles, nMissingFiles, exitedJobsList = GetTaskOutputAndExitCodes(taskName, logFiles, opts)

        # Create CRAB object
        crabTask = CrabTask(mcrabDir, taskName, logFiles, rootFiles, opts)
        mcrabTask.AddCrabTaskObject(crabTask)

        # For testing purposes (pre-stage to merging)
        if opts.test:
            ExamineExitCodes(crabTask.GetTaskName(), exitedJobsList, nMissingFiles)
            continue

        # Clean up pre-merged ROOT files before continuing? 
        if opts.deleteMergedFilesFirst:
            DeleteTaskMergedRootFles(crabTask.GetTaskDir(), crabTask.GetTaskName(), opts)
            continue

        # Check that the ROOT output files were found
        msg = "Found %d ROOT file(s) to merge" % (len(rootFiles))
        if len(rootFiles) < 1:
            msg += ". Skipping ..."
            Print(NoteStyle() + msg + NormalStyle(), False)
            continue
        else:
            Verbose(msg, False)
        
        # If not all ROOT files exist, prepare report anyway and continue to next CRAB task 
        rootFilesExist = CheckThatFilesExist(crabTask.GetTaskName(), crabTask.GetRootFiles(), opts)
        if not rootFilesExist:
            continue    

        # Check if pre-existing merged ROOT files alredy exist
        preMergedFiles  = GetPreexistingMergedFiles(crabTask.GetTaskDir(), opts)
        nPreMergedFiles = len(preMergedFiles)
        crabTask.SetPreMergedFiles(preMergedFiles)

        # Split ROOT files according to user-defined options (maxFileSize or filesPerMerge)
        filesSplit = SplitRootFiles(crabTask.GetTaskName(), rootFiles, opts)

        # For-loop: All splitted files
        for index, inputFiles in filesSplit:

            Verbose("Merging %s/%s" % (index+1, len(filesSplit)), False)
            taskNameAndNum = crabTask.GetTaskName()
            
            # Assign "task-number" if merging more than 1 files
            if len(filesSplit) > 1:
                taskNameAndNum += "-%d" % index
            else:
                Verbose("%s, splitted output to %s files" % (crabTask.GetTaskName(), len(filesSplit) ) )

            # Get and store the name of the merged ROOT files to be created
            mergeName = os.path.join(crabTask.GetTaskName(), "results", opts.output % taskNameAndNum)
            crabTask.AppendToMergedFiles(mergeName)

            # Get and store the EOS name of the merged ROOT files to be created
            mergeNameEOS = DoNotUseFuseMount( ConvertPathToEOS(crabTask.GetTaskName(), mergeName, "", opts) )
            crabTask.AppendToMergedFilesEOS(mergeNameEOS)

            Verbose("%s, mergeName is %s" % (crabTask.GetTaskName(), mergeName) )
            if opts.filesInEOS:
                mergeName = mergeNameEOS

            # Save the mapping of this merged ROOT files to input ROOT file list
            crabTask.MakeMergedToInputPair(mergeName, inputFiles)            
            
            # Save/Update this task  list of CRAB tasks
            mcrabTask.AddCrabTaskObject(crabTask)

            # Determine if the new ROOT file to be created already exists
            mergeFileExists = (mergeName in crabTask.GetPreMergedFiles())
            # mergeFileExists = FileExists(mergeName, opts)  # also works but more time-consuming

            # If merged ROOT file already exists skip it or rename it as .backup
            if mergeFileExists and not opts.overwrite:
               
                # Get the file size and save it (in GB) 
                crabTask.MakeMergedToSizePair(mergeName, GetFileSize(mergeName, opts))
                
                # Delete input files?
                if opts.delete:
                    DeleteFiles(crabTask.GetTaskName(), mergeName, inputFiles, opts)
                                    
                # Create symbolic links?
                if opts.linksToEOS:
                    LinkFiles(crabTask.GetTaskName(), crabTask.GetRootFiles())

                # Skip remaining steps
                continue
            else:
                pass

            # Definitions before merging ROOT files            
            nInputFiles = len(crabTask.GetInputFilesForMergeFile(mergeName))
            firstFile   = os.path.basename(crabTask.GetInputFilesForMergeFile(mergeName)[0])
            lastFile    = os.path.basename(crabTask.GetInputFilesForMergeFile(mergeName)[-1])
            time_start  = time.time()

            # Attempt to merge the ROOT files
            ret    = -1
            cmd    = GetMergeCommand(mergeName, inputFiles, opts)
            suffix = "%s to %s -> %s" % (firstFile, lastFile, os.path.basename(mergeName))
            try:
                PrintProgressBar("Merge ROOT files", index-1, len(filesSplit), suffix)
                ret = MergeFiles(mergeName, inputFiles, opts)
                PrintProgressBar("Merge ROOT files", index, len(filesSplit), suffix)
            except TimeoutError, e:
                dt_timeout = time.time() - time_start
                msg  = "\nTimed-out (%.1f seconds) trying to merge %s files(s): " % (dt_timeout, nInputFiles)
                msg += suffix
                Print(ErrorStyle() + msg + NormalStyle(), True)

                # String together the command and print it before exiting
                full_cmd = ""
                for c in cmd:
                    full_cmd += c + " "
                Print("Command invoked was:\n" +  "".join(full_cmd), False)
                sys.exit()

            # Time the merging process
            crabTask.MakeMergedToMergeTimePair(mergeName, time.time()-time_start)

            if ret != 0:
                msg  = "Error when trying to merge %s files(s): "
                msg += suffix
                FinishProgressBar()
                Print(ErrorStyle() + msg + NormalStyle(), False )
                Print("Executing merge command returned: %s" % ret, False)
                return ret
            else:
                Verbose("MergeFiles() returned %s" % (ret) )
                pass

            # Get the file size and save it (in GB) 
            crabTask.MakeMergedToSizePair(mergeName, GetFileSize(mergeName, opts))

            # Save/Update this task  list of CRAB tasks
            mcrabTask.AddCrabTaskObject(crabTask)

            # Sanity check
            CheckControlHisto(crabTask.GetTaskName(), mergeName, inputFiles)

            # Delete all input files after merging them
            if opts.deleteImmediately:
                DeleteFiles(crabTask.GetTaskName(), mergeName, inputFiles, opts)

        # Finish the "Merge ROOT files" progress bar
        FinishProgressBar()

        # Save/Update this task  list of CRAB tasks
        mcrabTask.AddCrabTaskObject(crabTask)

    if opts.test:
        return

    # Append "delete" message
    Verbose("Merged files%s:" % GetDeleteMessage(opts), False)
    
    Verbose("Merging completed! Now to clean duplicate folders and write PU histos", True)
    mcrabTask = DeleteFoldersAndWritePU(mcrabTask)

    # Print summary table using reports
    PrintSummary(mcrabTask)
    return 0


def DeleteFoldersAndWritePU(mcrabTask):
 
    crabTaskList = mcrabTask.GetCrabTaskObjects()
    # For-loop:
    for index, crabTask in enumerate(crabTaskList, 1):
        
        # Definitions
        taskName = crabTask.GetTaskName()

        Print("%s%d/%d: %s" % (HighlightAltStyle(), index, len(crabTaskList), taskName + NormalStyle()), index==1)
        
        # For-loop:
        for i, f in enumerate(crabTask.GetMergedFiles(), 0):

            # Definitions
            taskName       = crabTask.GetTaskName()
            sourceFiles    = crabTask.GetInputFilesForMergeFile(f)
            nMergedFiles   = len(crabTask.GetMergedFiles())
            preMergedFiles = crabTask.GetPreMergedFiles()
                        
            # Delete folders & calculate the clean-time (in seconds)
            Verbose("%s [from %d file(s)]" % (f, len(sourceFiles)), True)
            time_start = time.time()

            # No duplicate folders to delete if file already existed (hence was cleaned)
            mergeFileExists = (f in crabTask.GetPreMergedFiles())
            if mergeFileExists:
                PrintProgressBar("Clean merged ROOT files", i, nMergedFiles, os.path.basename(f))
                continue
            else:
                if opts.filesPerMerge != 1:
                    PrintProgressBar("Clean merged ROOT files", i-1, nMergedFiles, os.path.basename(f))
                    DeleteFolders(f, ["Generated", "Commit", "dataVersion"], opts)
                    PrintProgressBar("Clean merged ROOT files", i, nMergedFiles, os.path.basename(f))
                else:
                    PrintProgressBar("Clean merged ROOT files", 99, 100, "Skipped because filesPerMerge=%s" % (opts.filesPerMerge))
            
            # Keep track of time
            crabTask.MakeMergedToCleanTimePair(os.path.basename(f), time.time() - time_start)
            
        # Delete files after merging?
        if opts.delete and not opts.deleteImmediately:
            DeleteFiles(taskName, f, sourceFiles, opts)

        # Finish the "Clean merged ROOT files" progress bars
        FinishProgressBar()

        # For-loop:
        for j, f in enumerate(crabTask.GetMergedFiles(), 0):

            # Add pile-up histos (for data only!)
            isData, fOUT = IsDataRootfile(f)
            time_start = time.time()
            if isData:
                PrintProgressBar("Write PU histos (isData=%s)" % (isData) , j, nMergedFiles, os.path.basename(f))
                WritePileupHistos(f, fOUT, opts)
            else:
                PrintProgressBar("Write PU histos (isData=%s)" % (isData) , j, nMergedFiles, os.path.basename(f))
                pass

            # Keep track of time            
            crabTask.MakeMergedToPileupTimePair(os.path.basename(f), time.time()-time_start)

        # Finish the "Write PU histos" progress bars
        FinishProgressBar()

        # Save/Update this task  list of CRAB tasks
        mcrabTask.AddCrabTaskObject(crabTask)

    return mcrabTask


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
    VERBOSE       = False
    OVERWRITE     = False
    DIRNAME       = ""
    LINKSTOEOS    = False
    FILESPERMERGE = -1
    FILESINEOS    = False
    SKIPVERIFY    = False
    MAXFILESIZE   = 2.0
    DELETEFIRST   = False

    parser = OptionParser(usage="Usage: %prog [options]")
    # multicrab.addOptions(parser)
    parser.add_option("--input", dest="input", type="string", default="histograms_.*?\.root",
                      help="Regex for input root files (note: remember to escape * and ? !) [default: 'histograms_.*?\.root']")#fixme

    parser.add_option("--output", dest="output", type="string", default="histograms-%s.root",
                      help="Pattern for merged output root files (use '%s' for crab directory name) [default: 'histograms-%s.root']")#fixme

    parser.add_option("--deleteMergedFilesFirst", dest="deleteMergedFilesFirst", action="store_true", default=DELETEFIRST,
                      help="Option to delete all pre-existing merged files before proceeding to merging [default: %s]" % (DELETEFIRST) )

    parser.add_option("--test", dest="test", default=False, action="store_true",
                      help="Just test, do not do any merging or deleting. Useful for checking what would happen. [default: 'False']")

    parser.add_option("--delete", dest="delete", default=False, action="store_true",
                      help="Delete the source files after all crab tasks have been merged (to save disk space) [default: 'False']")

    parser.add_option("--deleteImmediately", dest="deleteImmediately", default=False, action="store_true",
                      help="Delete the source files immediately after merging to save disk space [default: 'False']")

    parser.add_option("--filesPerMerge", dest="filesPerMerge", default=FILESPERMERGE, type="int",
                      help="Merge at most this many files together (-1 to merge all files to one). [default: %s]" %(FILESPERMERGE) )

    parser.add_option("--filesInEOS", dest="filesInEOS", default=FILESINEOS, action="store_true",
                      help="The ROOT files to be merged are in an EOS. Merge the files from there (xrootd protocol). [default: '%s']" % (FILESINEOS) )

    parser.add_option("-i", "--includeTasks", dest="includeTasks" , default="", type="string", 
                      help="Only perform action for this dataset(s) [default: '']")

    parser.add_option("-e", "--excludeTasks", dest="excludeTasks" , default="", type="string", 
                      help="Exclude this dataset(s) from action [default: '']")    

    parser.add_option("--allowJobExitCode", dest="allowJobExitCodes", default=[], action="append", type="int",
                      help="Allow merging files from this non-zero job exit code (zero exe exit code is still required). Can be given multiple times [default: '[]']")

    parser.add_option("-v", "--verbose"    , dest="verbose"      , default=VERBOSE, action="store_true", 
                      help="Verbose mode for debugging purposes [default: %s]" % (VERBOSE))

    parser.add_option("--overwrite", dest="overwrite", default=False, action="store_true",
                      help="Overwrite histograms-*.root files [default %s]" % (OVERWRITE))

    parser.add_option("-d", "--dir", dest="dirName", default=DIRNAME, type="string",
                      help="Custom name for CRAB directory name [default: %s]" % (DIRNAME))   

    parser.add_option("-l", "--linksToEOS", dest="linksToEOS", default=LINKSTOEOS, action="store_true",
                      help="Create locally symbolic links to output/log files stored in EOS [default: %s]" % (LINKSTOEOS))

    parser.add_option("-s", "--skipVerify", dest="skipVerify", default=SKIPVERIFY, action="store_true",
                      help="Do not probe the log-file tarball for a given jobId to determine the job status or exit code. [default: %s]" % (SKIPVERIFY))

    parser.add_option("-m", "--maxFileSize", dest="maxFileSize", default=MAXFILESIZE, type="float",
                      help="The maximum file size (in GB) allowed for each merged ROOT file. [default: %s]" % (MAXFILESIZE))

    (opts, args) = parser.parse_args()

    if opts.dirName == "":
        opts.dirName = os.path.basename(os.getcwd())

    if opts.filesPerMerge == 0:
        parser.error("--filesPerMerge must be non-zero")

    if opts.deleteMergedFilesFirst:
        msg = "Are you sure you want to %spermanently delete%s all merged ROOT files of all CRAB tasks?" % (ErrorStyle(), NormalStyle())
        yes = AskUser(WarningLabel() + msg + NormalStyle(), True)
        if not yes:
            sys.exit()

    if opts.delete or opts.deleteImmediately:
        msg = "Are you sure you want to %spermanently delete%s all output ROOT files of all CRAB tasks after merging process is complete?" % (ErrorStyle(), NormalStyle())
        yes = AskUser(WarningLabel() + msg + NormalStyle(), True)
        if not yes:
            sys.exit()
        else:
            msg = "%sAre you REALLY sure? If you choose to continue it is irreversible!" % (ErrorStyle())
            yes = AskUser(WarningLabel() + msg + NormalStyle(), False)
            if not yes:
                sys.exit()
            
    if opts.skipVerify:
        msg  = "Option --skipVerify enabled. Will not probe the CRAB log-files to check if all jobs were successful"
        Print(NoteStyle() + msg + NormalStyle(), True)

    sys.exit(main(opts, args))
