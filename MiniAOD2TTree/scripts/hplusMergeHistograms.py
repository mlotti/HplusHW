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


#================================================================================================
# Global Definitions
#================================================================================================
re_histos = []
re_se = re.compile("newPfn =\s*(?P<url>\S+)")
replace_madhatter = ("srm://madhatter.csc.fi:8443/srm/managerv2?SFN=", "root://madhatter.csc.fi:1094")
PBARLENGTH = 10

#================================================================================================ 
# Class Definition
#================================================================================================ 
class ExitCodeException(Exception):
    '''
    Exception for non-succesful crab job exit codes
    '''
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message

class Report:
    def __init__(self, dataset, mergeFileMap, mergeSizeMap, mergeTimeMap, filesExist):
        Verbose("class Report:__init__()")
        self.dataset = dataset
        self.inputFiles  = []
        self.mergedFiles = []
        self.mergePath        = "N/A"
        if len(self.mergedFiles) > 0:
            self.mergePath    = os.path.dirname( self.mergedFiles[0]) 
        self.mergeFileMap     = mergeFileMap    # mergeFileName -> inputFiles map
        self.mergeSizeMap     = mergeSizeMap    # mergeFileName -> mergeFileSize map
        self.mergeTimeMap     = mergeTimeMap    # mergeFileName -> mergeTime map
        self.nPreMergedFiles  = filesExist
        self.mergedFiles      = mergeFileMap.keys()
        self.cleanTimeTotal   = 0

        # For-loop: All keys in dictionary (=paths to merged files)
        for key in mergeFileMap.keys():
            self.inputFiles.extend( mergeFileMap[key] )

        sizeSum   = 0
        mergeTime = 0
        # For-loop: All keys in dictionary (=paths to merged files)
        for key in self.mergeSizeMap.keys():
            if not mergeSizeMap[key] == None:
                sizeSum   += mergeSizeMap[key]
            mergeTime += mergeTimeMap[key]
            
        # Assign more values
        self.nInputFiles      = len(self.inputFiles)
        self.nMergedFiles     = len(self.mergedFiles)
        self.mergedFilesSize = sizeSum
        self.mergeTimeTotal  = mergeTime/60.0 #in minutes
        return


    def SetCleanTime(self, cleanTime):
        Verbose("SetCleanTime()")
        self.cleanTimeTotal = cleanTime/60.0 #in minutes
        return


#================================================================================================
# Function Definitions
#================================================================================================
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


def PrintMergeDetails(taskName, filesSplit, files):
    '''
    '''
    Verbose("PrintMergeDetails()", True)

    if len(filesSplit) == 1:
        msg = "Task %s, merging %d file(s)" % (taskName, len(files) )
    else:
        msg = "Task %s, merging %d file(s) to %d file(s)" % (taskName, len(files), len(filesSplit) )

    Verbose(msg, False)
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
    decimals    - Optional  : positive number of decimals in percent complete (Int)
    barLength   - Optional  : character length of bar (Int)
    '''
    Verbose("PrintProgressBar()")

    iteration      += 1 # since what is passed is the index of the file (starts from zero)
    prefix          = "\t" + taskName
    decimals        = 1
    barLength       = PBARLENGTH
    txtSize         = 60
    formatStr       = "{0:." + str(decimals) + "f}"
    percents        = formatStr.format(100 * (iteration / float(total)))
    filledLength    = int(round(barLength * iteration / float(total)))
    bar             = '=' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s: |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),
    sys.stdout.flush()
    return


def histoToDict(histo):
    '''
    '''
    ret = {}
    
    for bin in xrange(1, histo.GetNbinsX()+1):
        ret[histo.GetXaxis().GetBinLabel(bin)] = histo.GetBinContent(bin)    
    return ret


def GetLocalOrEOSPath(stdoutFile, opts):
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
        return False, stdoutFile
    
    localCopy = False
    if not FileExists(stdoutFile, opts):
        raise Exception("Cannot assert if job succeeded as file %s does not exist!" % (stdoutFile) )

    try:
        Verbose("Attempting to open file %s" % (stdoutFile) )
        f = open(GetXrdcpPrefix(opts) + stdoutFile) 
    except IOError as e:
        errMsg = "I/O error({0}): {1} %s".format(e.errno, e.strerror) % (stdoutFile)
        Verbose(errMsg)
        # For unknown reasons on LXPLUS EOS the files cannot be found, even if it exists
        if opts.filesInEOS:
            Verbose("File %s could not be found/read on EOS. Attempting to copy it locally and then read it" % (stdoutFile) )
            
            if "fnal" in socket.gethostname():
                srcFile  = "root://cmseos.fnal.gov/" + stdoutFile #
            else:
                srcFile  = GetXrdcpPrefix(opts) + stdoutFile
            
            destFile = os.path.basename(stdoutFile)
            cmd      = "xrdcp %s %s" % (srcFile, destFile)
            Verbose(cmd)
            ret = Execute(cmd)
            stdoutFile = os.path.join(os.getcwd(), os.path.basename(stdoutFile) )
            localCopy = True
            return localCopy, stdoutFile
        else:
            raise Exception(errMsg)
    return localCopy, stdoutFile


def AssertJobSucceeded(stdoutFile, allowJobExitCodes, opts):
    '''
    Given crab job stdout file, ensure that the job succeeded
    \param stdoutFile   Path to crab job stdout file
    \param allowJobExitCodes  Consider jobs with these non-zero exit codes to be succeeded
    If any of the checks fail, raises ExitCodeException
    '''
    Verbose("AssertJobSucceeded()", True)

    if opts.skipVerify:
        return
    
    localCopy, stdoutFile = GetLocalOrEOSPath(stdoutFile, opts)

    re_exe = re.compile("process\s+id\s+is\s+\d+\s+status\s+is\s+(?P<code>\d+)")
    re_job = re.compile("JobExitCode=(?P<code>\d+)")

    exeExitCode = None
    jobExitCode = None
    
    Verbose("Checking whether file %s is a tarfile" % (stdoutFile) )
    if tarfile.is_tarfile(stdoutFile):
        Verbose("File %s is a tarfile" % (stdoutFile) )
        fIN = tarfile.open(stdoutFile)
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
        Verbose("File %s is not a tarfile" % (stdoutFile) )

    # If log file was copied locally remove it!
    if localCopy:
        Verbose("Removing local copy of stdout tarfile %s" % (stdoutFile) )
        cmd = "rm -f %s" % (stdoutFile)
        Verbose(cmd)
        ret = Execute(cmd)

    jobExitCode = exeExitCode
    if exeExitCode == None:
        #raise ExitCodeException("File %s, No exeExitCode" % (stdoutFile) )
        Verbose("File %s, No exeExitCode. Will be treated like a job with non-zero exitcode" % (stdoutFile), False)
    if jobExitCode == None:
        #raise ExitCodeException("File %s, No jobExitCode" % (stdoutFile) )
        Verbose("File %s, No jobExitCode. Will be treated like a job witn non-zero exitcode" % (stdoutFile), False)
    if exeExitCode != 0:
        Verbose("File %s, executable exit code is %s" % (stdoutFile, exeExitCode) )
    if jobExitCode != 0 and not jobExitCode in allowJobExitCodes:
        Verbose("File %s, job exit code is %s" % (stdoutFile, jobExitCode) )
    return #fixme: is this okay?


def getHistogramFile(stdoutFile, opts):
    '''
    '''
    Verbose("getHistogramFile()", True)

    Verbose("Asserting that job succeeded by reading file %s" % (stdoutFile), False )
    AssertJobSucceeded(stdoutFile, opts.allowJobExitCodes, opts)
    histoFile = None

    Verbose("Asserting that file %s is a tarball" % (stdoutFile) )
    if tarfile.is_tarfile(stdoutFile):
        fIN = tarfile.open(stdoutFile)
        log_re = re.compile("cmsRun-stdout-(?P<job>\d+)\.log")

        # For-loop: All tarball members (contents)
        for member in fIN.getmembers():
            Verbose("Looking for cmsRun-stdout-*.log files in tarball memember file %s" % (member) )
            f = fIN.extractfile(member)
            match = log_re.search(f.name)
            if match:
                histoFile = "miniaod2tree_%s.root"%match.group("job")
                """
                for line in f:
	            for r in re_histos:   
            		m = r.search(line)
            		if m:
                	    histoFile = m.group("file")
                	    break
        	    if histoFile is not None:
            		break
                """
        fIN.close()
    else:
        f = open(stdoutFile)
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


def getHistogramFileSE(stdoutFile, opts):
    '''
    -> OBSOLETE <-
    '''
    Verbose("getHistogramFileSE()", True)

    Verbose("Asserting that job succeeded by reading file %s" % (stdoutFile), False )
    AssertJobSucceeded(stdoutFile, opts.allowJobExitCodes, opts)
    histoFile = None

    # Open the "stdoutFile"
    f = open(stdoutFile)

    # For-loop: All lines in file "stdoutFile"
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


def getHistogramFileEOS(stdoutFile, opts):
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

    Verbose("Asserting that job succeeded by reading file %s" % (stdoutFile), False )
    AssertJobSucceeded(stdoutFile, opts.allowJobExitCodes, opts)

    histoFile = None

    # Open the "stdoutFile"
    stdoutFileEOS = stdoutFile
    localCopy, stdoutFile = GetLocalOrEOSPath(stdoutFile, opts)

    # Open the standard output file
    # Verbose("Opening log file %s" % (stdoutFile), True ) #fixme: is this really needed?
    # f = open(stdoutFile, "r")  #fixme: is this really needed?
    
    # Get the jobId with regular expression
    log_re = re.compile("cmsRun_(?P<job>\d+)\.log.tar.gz")
    match = log_re.search(stdoutFile)
    #match = log_re.search(f.name)
    if match:
        jobId     = match.group("job")
        output    = "miniaod2tree_%s.root" % (jobId)
        histoFile = stdoutFileEOS.rsplit("/", 2)[0] + "/" + output
    else:
        Verbose("Could not determine the jobId of file %s. match = " % (stdoutFile, match) )
    
    # Close (and delete if copied locally) the standard output file
    #f.close() #fixme: is this really needed?

    if localCopy:
        Verbose("Removing local copy of stdout tarfile %s" % (stdoutFile) )
        cmd = "rm -f %s" % (stdoutFile)
        Verbose(cmd)
        ret = Execute(cmd)

    Verbose("The output file from job with id %s for task %s is %s" % (jobId, stdoutFile.split("/")[0], histoFile) )
    return histoFile
    

def GetHistogramFile(taskName, f, opts):
    '''
    '''
    Verbose("GetHistogramFile()", True)
    histoFile = None

    if opts.filesInEOS:
        #histoFile = getHistogramFileEOS(f, opts)
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
        # prefix = "" #do NOT use this "mount fuse" as it fails for multiple files
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


def splitFiles(taskName, files, filesPerEntry, opts):
    '''    
    Split all output ROOT files into small groups of files to be merged
    '''
    Verbose("splitFiles()")

    i   = 0
    ret = []
    MB  = 1000000
    GB  = 1000*MB

    # Default value is -1
    if filesPerEntry < 0:
        maxsize = opts.maxFileSize*GB
        sumsize = 0
        firstFile = 0

        # For-loop: All files (with ifile counter)
        for ifile, f in enumerate(files):

            # Update Progress bar
            PrintProgressBar(taskName + ", Split ", ifile, len(files), "[" + os.path.basename(f) + "]")

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
            return ind*filesPerEntry
        def end(ind):
            return (ind+1)*filesPerEntry
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
    Return the file size, irrespective of whether it is located locally or
    on EOS.
    '''
    Verbose("GetFileSize()", True)
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


def hadd(opts, mergeName, inputFiles, path_prefix=""):
    '''
    '''
    Verbose("hadd()", True)
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
    Verbose("Opening ROOT file %s in %s mode." % (fileName, fileMode) )
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


def WritePileupHistos(fileName, opts):
    '''
    If dataversion is NOT "data", return.
    Otherwise, read the PileUp.root file and
    get 3 PU histograms (pileup, pileup_up variation, pileup_down variation)
    and write them to the fileName passed as argument.
    '''
    Verbose("WritePileupHistos()", True)
    
    if FileExists(fileName, opts ) == False:
        raise Exception("The file %s does not exist!" % (fileName) )

    # Definitions
    prefix = ""
    if opts.filesInEOS:
        prefix = GetXrdcpPrefix(opts)
        # prefix = GetFileOpenPrefix(opts)
    fileMode = "UPDATE"

    # Open the ROOT file
    nAttempts   = 1
    maxAttempts = 10
    fOUT = None
    while nAttempts < maxAttempts:
        try:
            Verbose("Attempt #%s: Opening ROOT file %s in %s mode." % (nAttempts, fileName, fileMode) )
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
    hPU = None
    dataVersion = fOUT.Get("configInfo/dataVersion")
    dv_re = re.compile("data")  
    Verbose("The data version of file %s is %s"   % (fileName, dataVersion.GetTitle()))
    match = dv_re.search(dataVersion.GetTitle())

    # If dataset is not data, do nothing
    if not match:
        return

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
    if all exist!
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
        PrintProgressBar(taskName + ", Check ", index, len(fileList), "[" + os.path.basename(f) + "]")
            

    # Flush stdout
    FinishProgressBar()

    if nExist != nFiles:
        msg  = "%s, found %s ROOT files but expected %s. Have you already run this script? " % (taskName, nExist, nFiles)
        msg += "Would you like to proceed with the merging anyway? ALEX"
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
    newDatasets = []
 
    # Exclude datasets
    if opts.excludeTasks != "":
        tmp = []
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
            newDatasets.append(d)
        return newDatasets

    # Include datasets
    if opts.includeTasks != "":
        tmp = []
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
                newDatasets.append(d)
        return newDatasets

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
    Verbose("GetFileOpenPrefix()")

    if not opts.filesInEOS:
      return ""

    HOST = socket.gethostname()
    path_prefix = ""

    Verbose("Determining prefix for opening ROOT files for host %s" % (HOST) )
    if "fnal" in HOST:
        path_prefix = "root://cmseos.fnal.gov/"
        # path_prefix = "" #fixme
    elif "lxplus" in HOST:
        path_prefix = "root://eoscms.cern.ch//eos//cms/"
    else:
        raise Exception("Unsupported host %s" % (HOST) )
    return path_prefix


def MergeFiles(mergeName, inputFiles, opts):
    '''
    Merges ROOT files, either stored locally or on EOS.
    '''
    Verbose("MergeFiles()")

    Verbose("Attempting to merge:\n\t%s\n\tto\n\t%s." % ("\n\t".join(inputFiles), mergeName) )
    if len(inputFiles) < 1:
        raise Exception("Attempting to merge 0 files! Somethings was gone wrong!")
    elif len(inputFiles) == 1:
        if opts.filesInEOS:
            prefix   = GetXrdcpPrefix(opts)
            srcFile  = prefix + inputFiles[0]
            destFile = prefix + mergeName
            cmd      = "xrdcp %s %s" % (srcFile, destFile)
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

def PrintSummary(taskReports):
    '''
    Self explanatory
    '''
    Verbose("PrintSummary()")
    
    table    = []
    msgAlign = "{:<3} {:<50} {:^15} {:^15} {:^15} {:^18} {:^18} {:^18}"
    header   = msgAlign.format("#", "Task Name", "Input Files", "Merged Files", "Pre-Merged Files", "Size (GB)", "Merge Time (min)", "Clean Time (min)")
    hLine    = "="*len(header)
    table.append(hLine)
    table.append(header)
    table.append(hLine)

    #For-loop: All reports
    index = 1
    for key in taskReports.keys():
        r = taskReports[key]
        table.append( msgAlign.format(index, r.dataset, r.nInputFiles, r.nMergedFiles, r.nPreMergedFiles, "%0.3f" % r.mergedFilesSize, "%0.3f" % r.mergeTimeTotal, "%0.3f" % r.cleanTimeTotal) )
        index+=1

    # Print the table
    print
    for l in table:
        print l
    print
    return


def CheckTaskReport(logfilepath, opts):
    '''
    Probes the log-file tarball for a given jobId to
    determine the job status or exit code.
    '''
    Verbose("CheckTaskReport()", True)
        
    
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


def GetTaskOutputAndExitCodes(taskName, stdoutFiles, opts):
    '''
    Loops over all stdout files of a given CRAB task, to obtain 
    and return the corresponding output files and exit-codes.
    '''
    Verbose("GetTaskOutputAndExitCodes()", True)

    # Definitions
    missing    = 0
    files      = []
    exitedJobs = []
    jobId_re   = re.compile("cmsRun_(?P<jobId>\d+)\.log\.tar\.gz")  #re.compile("/results/cmsRun_(?P<jobId>\d+)\.log\.tar\.gz")
    Verbose("Getting output files & exit codes for task %s" % (taskName) )

    # For-loop: All stdout files of given task
    for index, f in enumerate(stdoutFiles):

        Verbose("Getting output files & exit codes for task %s (by reading %s)" % (taskName, f) )
        histoFile = GetHistogramFile(taskName, f, opts)
        if histoFile != None:
            files.append(histoFile)
        else:
            missing += 1
            Verbose("Task %s, skipping job %s: input root file not found from stdout" % (taskName, os.path.basename(f)) )

        exitcode = CheckTaskReport(f, opts)
        if exitcode != 0:
            exit_match = jobId_re.search(f)
            if exit_match:
                exitedJobs.append(int(exit_match.group("jobId")))
        
        # Update progress bar
        PrintProgressBar(taskName + ", Files ", index, len(stdoutFiles), "[" + os.path.basename(f) + "]")

    # Flush stdout
    if len(stdoutFiles)>0:
        FinishProgressBar()
    return files, missing, exitedJobs


def ExamineExitCodes(taskName, exitedJobs, missingFiles):
    '''
    Examine all exit codes (passed as a list) and determine if there are 
    jobs with problems. 

    Print command for job resubmission.
    '''
    Verbose("ExamineExitCodes()")

    #Print("Task %s, " % (taskName) )
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
        Print("jobs with missing files: %s" %missingFiles, False)
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
    try:
        if opts.filesInEOS:
            # Skip this sanity check to speed things up
            # sanityCheck(GetXrdcpPrefix(opts) + mergeNameEOS, inputFiles)
            pass
        else:
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
        PrintProgressBar(taskName + ", Delete", index, len(fileList), "[" + os.path.basename(f) + "]")
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
    
    Verbose("Will delete the following folders:\n\t%s\n\tfrom file %s" % ("\n\t".join(foldersToDelete), filePath) )
    # For-loop: All folders to be deleted
    for folder in foldersToDelete:
        Verbose("Deleting folder \"%s\"" % (folder) )
        delete(filePath, folder, opts)
    return


def GetTaskLogFiles(taskName, opts):
    '''
    Get all the log files for the given CRAB task
    '''
    Verbose("GetTaskLogFiles()", True)
    if opts.filesInEOS:
        Verbose("Task %s, converting path to EOS to get log files" % (taskName) )
        tmp = ConvertPathToEOS(taskName, taskName, "log/", opts, isDir=True)
        Verbose("Obtaining stdout files for task %s from %s" % (taskName, tmp), True)
        stdoutFiles = glob.glob(tmp + "cmsRun_*.log.tar.gz")        

        Verbose("Found %s stdout files" % (len(stdoutFiles) ) )
        # Sometimes glob doesn't work (for unknown reasons)
        if len(stdoutFiles) < 1:
            msg = "Task %s, could not obtain log files with glob." % (taskName)
            msg += "\n\tTrying alternative method. If problems persist retry without setting the CRAB environment."
            Verbose(msg, True)
            cmd = ConvertCommandToEOS("ls", opts) + " " + tmp
            Verbose(cmd)
            dirContents = Execute(cmd)
            stdoutFiles = dirContents
            stdoutFiles = [tmp + f for f in dirContents if ".log.tar.gz" in f]
            Verbose("Task %s, found the following log files:\n\t%s" % (taskName, "\n\t".join(stdoutFiles) ) )
    else:
        stdoutFiles = glob.glob(os.path.join(taskName, "results", "cmsRun_*.log.tar.gz"))

    if len(stdoutFiles) < 1:
        #raise Exception("Task %s, could not obtain log files." % (taskName) )
        Verbose("Task %s, could not obtain log files." % (taskName), False)

    # Sort the list naturally (alphanumeric strings). 
    if 1:
        stdoutFiles = natural_sort(stdoutFiles)
        #print "\n\t".join(stdoutFiles)

    return stdoutFiles
        

def GetPreexistingMergedFiles(taskPath, opts):
    '''
    Returns a list with the full path of all pre-existing merged ROOT files
    '''
    Verbose("GetPreexistingMergedFiles()", True)
    
    if opts.filesInEOS:
        cmd = ConvertCommandToEOS("ls", opts) + " " + taskPath
    else:
        cmd = "ls"  + " " + taskPath
    Verbose(cmd)
    dirContents = Execute(cmd)
    preMergedFiles = filter(lambda x: "histograms-" in x, dirContents)

    # For-loop: All files
    mergeSizeMap = {}
    mergeTimeMap = {}
    
    # For-loop: All merged ROOT files
    for f in preMergedFiles:
        Verbose("Getting file size for file %s" % (f))
        mergeSizeMap[f] = GetFileSize(taskPath + "/" + f, opts)
        mergeTimeMap[f] = 0.0
    #filesExist = len(preMergedFiles)
    #return filesExist, mergeSizeMap, mergeTimeMap
    return preMergedFiles, mergeSizeMap, mergeTimeMap


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
    Verbose("LinkFiles()", True)
    
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
            ret = os.system(cmd)
            # ret = Execute(cmd)

        # Update Progress bar
        PrintProgressBar(taskName + ", Links ", index, len(fileList), "[" + os.path.basename(destFile) + "]")
    return


def main(opts, args):

    Verbose("main()", True)
    
    # Get the multicrab task names (=dir names)
    mcrabDir     = os.path.basename(os.getcwd())
    crabDirs     = GetCrabDirectories(opts)
    nTasks       = len(crabDirs)
    taskNameMap  = {}
    taskNameMapR = {}

    if nTasks < 1:
        Print("Did not find any tasks under %s. EXIT" % (mcrabDir) )
        return 0
    
    if opts.filesInEOS:
        Print("Found %s task(s) for %s in EOS" % (nTasks, mcrabDir) )
    else:
        Print("Found %s task(s) in %s" % (nTasks, mcrabDir) )
        
    # Map taskName -> taskNameEOS
    if opts.filesInEOS:
        for d in crabDirs:
            taskNameMap[d] = ConvertTasknameToEOS(d, opts)
        taskNameMapR = {v: k for k, v in taskNameMap.items()} #reverse map

    # Construct regular expressions for output files
    global re_histos
    re_histos.append(re.compile("^output files:.*?(?P<file>%s)" % opts.input))
    re_histos.append(re.compile("^\s+file\s+=\s+(?P<file>%s)" % opts.input))
    exit_re = re.compile("/results/cmsRun_(?P<exitcode>\d+)\.log\.tar\.gz")
    
    # Definitions
    filesExist   = 0
    taskReports  = {}
    mergeFileMap = {}
    mergeSizeMap = {}
    mergeTimeMap = {}
    cleanTime    = {}

    # For-loop: All task names
    Verbose("Looping over all tasks in %s" % (opts.dirName), True)
    for index, d in enumerate(crabDirs):
        
        # Change line for each new task
        if index!=0:
            print

        # Get the task log files (human-sorted0
        taskName    = d.replace("/", "")
        stdoutFiles = GetTaskLogFiles(taskName, opts)
        Verbose("The stdout files for task %s are:\n\t%s" % ( taskName, "\n\t".join(stdoutFiles)), True)
        
        # Create symbolic links for merge files?
        if opts.linksToEOS:
            pass #LinkFiles(taskName, stdoutFiles)

        # Definitions
        files, missingFiles, exitedJobs = GetTaskOutputAndExitCodes(taskName, stdoutFiles, opts)

        # For Testing purposes
        if opts.test:
            ExamineExitCodes(taskName, exitedJobs, missingFiles)            
            continue

        # Check that output files were found. If so, check that they exist!
        if len(files) == 0:
            Verbose("Task %s, skipping, no files to merge" % (taskName), False)
            continue        
        else:            
            if not opts.filesInEOS:
                files = [taskName + "/results/" + x for x in files] # fixme: verify that only for filesInEOS option needed
            else:
                pass

            # If not ALL task output files exist (and this is not a test), print report (perhaps files have already been merged)
            if not CheckThatFilesExist(taskName, files, opts) and not opts.test:

                # Delete input files?
                if opts.delete or opts.deleteImmediately:
                    if AskUser("%s, delete %s files?:\n\t%s" % (taskName, len(files), "\n\t".join([os.path.basename(f) for f in files])) ):
                        DeleteFiles(taskName, None, files, opts)
                    else:
                        pass

                Verbose("%s, skipping, some files are missing" % (taskName) )
                mergeFiles, mergeSizeMap, mergeTimeMap = GetPreexistingMergedFiles(os.path.dirname(files[0]), opts)
                filesExist = len(mergeFiles)
                taskReports[taskName]  = Report( taskName, mergeFileMap, mergeSizeMap, mergeTimeMap, filesExist)

                # Create symbolic links?
                if opts.linksToEOS:
                    mList = []
                    #For-loop: All merge files
                    for f in mergeFiles:
                        mFile = ConvertPathToEOS(taskName, os.path.join(d, "results", f), "", opts)
                        mList.append(mFile)
                    LinkFiles(taskName, mList)
                FinishProgressBar()
                continue
            else:
                pass
        Verbose("Task %s, with %s ROOT files" % (taskName, len(files)), False)

        # If this is a test skip the remaining part
        if opts.test:
            continue
        
        # Split files according to user-defined options
        filesSplit = splitFiles(taskName, files, opts.filesPerMerge, opts)

        # Print what you are merging
        PrintMergeDetails(taskName, filesSplit, files)

        # For-loop: All splitted files
        for index, inputFiles in filesSplit:

            Verbose("Merging %s/%s" % (index+1, len(filesSplit)), False)
            taskNameAndNum = d
            
            # Assign "task-number" if merging more than 1 files
            if len(filesSplit) > 1:
                taskNameAndNum += "-%d" % index
            else:
                Verbose("%s, splitted output to %s files" % (taskName, len(filesSplit) ) )

            # Get the merge name of the files
            mergeName = os.path.join(d, "results", opts.output % taskNameAndNum)
            Verbose("%s, mergeName is %s" % (taskName, mergeName) )
            if opts.filesInEOS:
                mergeName = ConvertPathToEOS(taskName, mergeName, "", opts)
            else:
                pass

            # If merge file already exists skip it or rename it as .backup
            if FileExists(mergeName, opts) and not opts.overwrite:

                mergeFiles, mergeSizeMap, mergeTimeMap = GetPreexistingMergedFiles(os.path.dirname(files[0]), opts)
                filesExist = len(mergeFiles)
                taskReports[taskName]  = Report( taskName, mergeFileMap, mergeSizeMap, mergeTimeMap, filesExist)
                filesExist += 1                
            
                # Delete input files?
                if opts.delete:
                    DeleteFiles(taskName, mergeName, inputFiles, opts)
                                    
                # Create symbolic links?
                if opts.linksToEOS:
                    mList = []
                    # For-loop: All merge files
                    for f in mergeFiles:
                        mFile = ConvertPathToEOS(taskName, os.path.join(d, "results", f), "", opts)
                        mList.append(mFile)
                    LinkFiles(taskName, mList)
                continue
            else:
                Verbose("%s, merge file  %s does not already exist. Will create it" % (taskName, mergeName) )

            # Merge the ROOT files
            mergePath = "/".join(mergeName.split("/")[-1:]) #fits terminal, [-6:] is too big to fit
            PrintProgressBar(taskName + ", Merge ", index-1, len(filesSplit), "[" + mergePath + "]")
            time_start = time.time()
            ret = MergeFiles(mergeName, inputFiles, opts)
            time_end = time.time()
            dtMerge = time_end-time_start
            if ret != 0:
                Verbose("MergeFiles() returned %s" % (ret))
                return ret
            else:
                Verbose("MergeFiles() returned %s" % (ret) )
                pass

            # Get the file size
            mergeFileSize = GetFileSize(mergeName, opts)
            if len(filesSplit) > 1 and not mergeFileSize == None:
                Verbose("Merged %s (%0.3f GB)." % (mergeName, mergeFileSize), False )

            # Keep track of merged files
            mergeFileMap[mergeName] = inputFiles
            mergeSizeMap[mergeName] = mergeFileSize
            mergeTimeMap[mergeName] = dtMerge

            # Sanity check
            CheckControlHisto(taskName, mergeName, inputFiles)

            # Delete all input files after merging them
            if opts.deleteImmediately:
                DeleteFiles(taskName, mergeName, inputFiles, opts)

            # Update Progress bar
            PrintProgressBar(taskName + ", Merge ", index, len(filesSplit), "[" + mergePath + "]")

        # Flush stdout
        FinishProgressBar()
        if taskName not in taskReports.keys():
            taskReports[taskName] = Report( taskName, mergeFileMap, mergeSizeMap, mergeTimeMap, filesExist)

    # Empty line before proceeding to cleaning
    print

    if opts.test:
        return

    # Append "delete" message
    deleteMsg = GetDeleteMessage(opts)
    Verbose("Merged files%s:" % (deleteMsg), False)
    
    foldersToDelete = ["Generated", "Commit", "dataVersion"]
    # For-loop: All merged files
    index = 0
    for key in mergeFileMap.keys():
        f = key
        sourceFiles = mergeFileMap[key]
        taskName = key.split("/")[0]
        if opts.filesInEOS:
            taskNameEOS = key.replace(GetEOSHomeDir(opts) + "/", "").split("/")[0]
            taskName    = taskNameEOS.replace("-", "_")
        Verbose("Merge file:\n\t%s" % (f), True)
        Verbose("Source files:\n\t%s" % ("\n\t".join(sourceFiles)), False) 

        # Delete folders & Calculate the clean-time (in seconds)
        Verbose("%s [from %d file(s)]" % (f, len(sourceFiles)), True)
        time_start = time.time()
        DeleteFolders(f, foldersToDelete, opts)
        time_end = time.time()
        dtClean  = (time_end-time_start)
        
        # Save the total clean time for this task
        if taskName not in cleanTime.keys():
            cleanTime[taskName] = dtClean 
        else:
            cleanTime[taskName] = cleanTime[taskName] + dtClean
            
        # Delete files after merging?
        if opts.delete and not opts.deleteImmediately:
            DeleteFiles(taskName, f, sourceFiles, opts)

        # Add pile-up histos
        WritePileupHistos(f, opts)

        # Update Progress bar
        if opts.filesInEOS:
            PrintProgressBar(taskNameMapR[taskNameEOS] + ", Clean ", index, len(mergeFileMap.keys()), "[" + os.path.basename(f) + "]")
        else:
            PrintProgressBar(taskName + ", Clean ", index, len(mergeFileMap.keys()), "[" + os.path.basename(f) + "]")
            
        index += 1

    # Flush stdout
    FinishProgressBar()

    # Calculate the total clean times
    for taskName in taskReports.keys():
        if opts.filesInEOS:
            eos = taskNameMap[taskName].replace("-", "_")
            if eos in cleanTime.keys():
                taskReports[taskName].SetCleanTime( cleanTime[eos] )

    # Print summary table using reports
    PrintSummary(taskReports)

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
    VERBOSE       = False
    OVERWRITE     = False
    DIRNAME       = ""
    LINKSTOEOS    = False
    FILESPERMERGE = -1
    FILESINEOS    = False
    SKIPVERIFY    = False
    MAXFILESIZE   = 2.0

    parser = OptionParser(usage="Usage: %prog [options]")
    # multicrab.addOptions(parser)
    parser.add_option("--input", dest="input", type="string", default="histograms_.*?\.root",
                      help="Regex for input root files (note: remember to escape * and ? !) [default: 'histograms_.*?\.root']")

    parser.add_option("--output", dest="output", type="string", default="histograms-%s.root",
                      help="Pattern for merged output root files (use '%s' for crab directory name) [default: 'histograms-%s.root']")

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

    sys.exit(main(opts, args))
