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

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

import HiggsAnalysis.NtupleAnalysis.tools.multicrab as multicrab


#================================================================================================
# Global Definitions
#================================================================================================
re_histos = []
re_se     = re.compile("newPfn =\s*(?P<url>\S+)")
replace_madhatter = ("srm://madhatter.csc.fi:8443/srm/managerv2?SFN=", "root://madhatter.csc.fi:1094")


#================================================================================================ 
# Class Definition
#================================================================================================ 
class Report:
    def __init__(self, name, allJobs, retrieved, running, finished, failed, retrievedLog, retrievedOut, eosLog, eosOut, status, dashboardURL):
        Verbose("class Report:__init__()")
        self.name            = name
        self.task            = str(allJobs)
        self.filePath        = str(retrieved)
        self.filePathEOS     = str(running)
        self.fileSize        = self.name.split("/")[-1]
        self.fileSizeMerged  = dashboardURL
        self.host            = self.GetTaskStatusStyle(status)
        self.nFiles          = finished
        self.nFilesMerged    = failed
        return


    def Print(self, printHeader=True):
        '''
        Simple function to print report.
        '''
        name = os.path.basename(self.name)
        txtFormat = '{:<20} {:<40}'
        msg  = txtAlign.format("\t %sName"     % (colors.WHITE) , ": " + self.name)
        msg += txtAlign.format("\t %Task"      % (colors.WHITE) , ": " + self.task)
        msg += txtAlign.format("\t %FilePath"  % (colors.WHITE) , ": " + self.filePath)
        msg += txtAlign.format("\t %sFileSize" % (colors.WHITE) , ": " + self.fileSize)
        print msg
        return


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


def histoToDict(histo):
    '''
    '''
    ret = {}
    
    for bin in xrange(1, histo.GetNbinsX()+1):
        ret[histo.GetXaxis().GetBinLabel(bin)] = histo.GetBinContent(bin)
    
    return ret


def getHistogramFile(stdoutFile, opts):
    '''
    '''
    multicrab.assertJobSucceeded(stdoutFile, opts.allowJobExitCodes)
    histoFile = None

    if tarfile.is_tarfile(stdoutFile):
        fIN = tarfile.open(stdoutFile)
        log_re = re.compile("cmsRun-stdout-(?P<job>\d+)\.log")
        for member in fIN.getmembers():
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
    multicrab.assertJobSucceeded(stdoutFile, opts.allowJobExitCodes)
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
    '''
    Verbose("getHistogramFileEOS()", True)
    multicrab.assertJobSucceeded(stdoutFile, opts.allowJobExitCodes)
    histoFile = None

    # Convert the local path of the stdoutFile to an EOS path that file
    stdoutFileEOS = ConvertPathToEOS(stdoutFile, "log/", opts)

    # Open the "stdoutFile" (does not need to be on EOS)
    if not os.path.exists(stdoutFile):
        raise Exception("File \"%s\" does not exist" % (stdoutFile) )

    # Open the standard output file
    f = open(stdoutFile)

    # Get the jobId with regular expression
    log_re = re.compile("cmsRun_(?P<job>\d+)\.log.tar.gz")
    match = log_re.search(f.name)
    if match:
        jobId     = match.group("job")
        histoFile = "miniaod2tree_%s.root" % (jobId)

        # Drop the log/cmsRun_1.log.tar.gz and add histoFile to path to get EOS path for histoFile
        histoFileEOS = stdoutFileEOS.rsplit("/", 2)[0] + "/" + histoFile
    else:
        Verbose("Could not determine the jobId of file \"%s\". match = " % (stdoutFile, match) )
        #raise Exception("Could not determine the jobId of file \"%s\". match = " % (stdoutFile, match) )
    
    # Cloe the standard output file
    f.close()
    
    Verbose("The output file from job with id \"%s\" for task \"%s\" is \"%s\"" % (jobId, stdoutFile.split("/")[0], histoFileEOS) )
    return histoFileEOS
    

def GetHistogramFile(taskName, f, opts):
    '''
    '''
    Verbose("GetHistogramFile()", True)
    histoFile = None

    if opts.filesInEOS:
        #histoFile = getHistogramFileSE(f, opts) #obsolete!
        histoFile = getHistogramFileEOS(f, opts)
        if histoFile != None:
            Verbose("The ROOT file for task \"%s\" is \"%s\"." % (taskName, histoFile) )
            return histoFile
        else:
            Print("Task %s, skipping job %s: input root file not found from stdout" % (taskName, f) )
    else:
        histoFile = getHistogramFile(f, opts)
        if histoFile != None:
            path = os.path.join(os.path.dirname(f), histoFile)
            if os.path.exists(path):
                return histoFile
            else:
                print "Task %s, skipping job %s: input root file found from stdout, but does not exist" % (taskName, f)
        else:
            print "Task %s, skipping job %s: input root file not found from stdout" % (taskName, f)
    return histoFile


def ConvertTasknameToEOS(taskName, opts):
    '''
    Get the full dataset name as found EOS.
    '''
    Verbose("ConvertDatasetnameToEOS()", False)
    
    # Variable definition
    crabCfgFile   = None
    taskNameEOS   = None

    # Get the crab cfg file for this task 
    crabCfgFile = "crabConfig_%s.py" % (taskName)
    fullPath    =  os.getcwd() + "/" + crabCfgFile
    if not os.path.exists(fullPath):
        raise Exception("Unable to find the file \"crabConfig_%s.py\"." % (taskName) )

    #Verbose("Determining EOS dataset name for task \"%s\" by reading file \"%s\"." % (taskName, fullPath))
    # For-loop: All lines in cfg file
    for l in open(fullPath): 
        keyword = "config.Data.inputDataset = "
        if keyword in l:
            taskNameEOS = l.replace(keyword, "").split("/")[1]

    if taskNameEOS == None:
        raise Exception("Unable to find the crabConfig_<dataset>.py for task with name \"%s\"." % (taskName) )

    Verbose("The conversion of task name \"%s\" into EOS-compatible is \"%s\"" % (taskName, taskNameEOS) )
    return taskNameEOS


def WalkEOSDir(pathOnEOS, opts): #fixme: bad code 
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
    # Verbose(cmd)
    dirContents = Execute(cmd)
    if "symbol lookup error" in dirContents[0]:
        raise Exception("%s\".\n\t\"%s\"." % (cmd, dirContents[0]) )

    #Verbose("Walking the EOS directory \"%s\" with contents:\n\t%s" % (pathOnEOS, "\n\t".join(dirContents)))

    # A very, very dirty way to find the deepest directory where the ROOT files are located!
    if len(dirContents) == 1:
        subDir = dirContents[0]
        # Verbose("Found sub-directory \"%s\" under the EOS path \"%s\"!" % (subDir, pathOnEOS) )
        pathOnEOS = WalkEOSDir(pathOnEOS + "/" + subDir, opts)
    else:
        rootFiles = []
        for f in dirContents:
            if ".root" not in f:
                continue
            else:
                rootFiles.append(pathOnEOS + "/" + f)
        pathOnEOS += "/"
        #Verbose("Reached end of the line. Found \"%s\" ROOT files under \"%s\"!"  % (len(rootFiles), pathOnEOS))
    return pathOnEOS


def ConvertCommandToEOS(cmd, opts):
    '''
    Convert a given command to EOS-path. Used when working solely with EOS
    and files are not copied to local working directory
    '''
    # Verbose("ConvertCommandToEOS()", True)
    
    # Define a map mapping bash command with EOS commands
    cmdMap = {}
    cmdMap["ls"]   = "eos ls"
    cmdMap["rm"]   = "eos rm"
    cmdMap["size"] = "eos find --size"

    # Define alias for eos (broken by cmsenv)
    eosAlias = "/afs/cern.ch/project/eos/installation/0.3.84-aquamarine/bin/eos.select "

    # EOS commands differ on LPC!
    if "fnal" in socket.gethostname():
        for key in cmdMap:
            if key == "ls": # exception because I use the full command, not the alias
                cmdMap[key] = "eosls"
            else:
                cmdMap[key] = cmdMap[key].replace("eos ", "eos")

    # Currect "eos" alias being broken on lxplus after cmsenv is set
    if "lxplus" in socket.gethostname():
        for key in cmdMap:
            cmdMap[key] = cmdMap[key].replace("eos", eosAlias)


    if cmd not in cmdMap:
        raise Exception("Could not find EOS-equivalent for cammand \"%s\"." % (cmd) )

    return cmdMap[cmd]


def Execute(cmd):
    '''
    Executes a given command and return the output.
    '''
    Verbose("Execute()", True)
    Verbose("Executing command: \"%s\"" % (cmd))
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)

    stdin  = p.stdin
    stdout = p.stdout
    ret    = []
    for line in stdout:
        ret.append(line.replace("\n", ""))
    stdout.close()
    return ret


def ConvertPathToEOS(fullPath, path_postfix, opts):
    '''
    Takes as input a path to a file or dir of a given multicrab task stored locally
    and converts it to the analogous path for EOS.
    '''
    path_prefix   = "/store/user/%s/CRAB3_TransferData" % (getpass.getuser())
    taskName      = fullPath.split("/")[0]
    fileName      = fullPath.split("/")[-1]
    taskNameEOS   = ConvertTasknameToEOS(taskName, opts)
    pathEOS       = WalkEOSDir(path_prefix + "/" + taskNameEOS, opts) # + "/"
    fullPathEOS   = pathEOS + path_postfix + fileName
    Verbose("Converted \"%s\" (default) to \"%s\" (EOS-compatible)" % (fullPath, fullPathEOS) )
    return fullPathEOS


def splitFiles(files, filesPerEntry, opts):
    '''    
    '''
    Verbose("splitFiles()")

    i   = 0
    ret = []
    MB  = 1000000
    GB  = 1000*MB

    # Default value is -1
    if filesPerEntry < 0:
        maxsize = 2*GB
        sumsize = 0
        firstFile = 0

        # For-loop: All files (with ifile counter)
        for ifile,f in enumerate(files):

            # Calculate cumulative size
            fileSize = GetFileSize(f, opts)
            sumsize +=  fileSize
            Verbose("File \"%s\" has a size of \"%s\" (sumsize=\"%s\")." % (f, fileSize, sumsize) )

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

    Verbose("Returning a %s-long list of tuples" % (len(ret)) )
    return ret


def GetFileSize(filePath, opts, convertToGB=False):
    '''
    Return the file size, irrespective of whether it is located locally or
    on EOS.
    '''
    Verbose("GetFileSize()")
    HOST = socket.gethostname()

    Verbose("Determining size for file \"%s\"" % (filePath) )
    if opts.filesInEOS:
        if "fnal" in HOST:
            eos = "eos root://cmseos.fnal.gov ls -l" #alias to "eosls -l"
            cmd = "%s -l %s" % (filePath)
            ret = Execute("%s" % (cmd) ).split()

            # Get the size as integer
            permissions = ret[0]
            unkownVar   = ret[1]
            username    = ret[2]
            group       = ret[3]
            size        = int(ret[4])
            month       = ret[5]
            dayOfMonth  = ret[6]
            time        = ret[7]
            filename    = ret[8] # or ret[-1]
        elif "lxplus" in HOST:
            eos  = "/afs/cern.ch/project/eos/installation/0.3.84-aquamarine/bin/eos.select" #simply "eos" will not work
            cmd  = "%s find --size %s" % (eos, filePath)
            ret  = Execute("%s" % (cmd) )

            # Get the size as integer
            size_str = ret[0].split()[-1].rsplit("size=")[-1]
            size     = int(size_str)
        else:
            raise Exception("Unsupported host \"%s\"" % (HOST) )
    else:
        size = os.stat(filePath).st_size

    if convertToGB:
        size = size/1024.0/1024.0/1024.0 #GB
    return size


def hadd(opts, mergeName, inputFiles, path_prefix=""):
    '''
    '''
    Verbose("hadd()", True)

    # Append path_prefix if needed
    if path_prefix != "":

        if path_prefix.endswith("/"):
            path_prefix = path_prefix[:-1]

        mergeNameNew  = path_prefix + mergeName
        inputFilesNew = []
        # For-loop: All input files
        for f in inputFiles:
           inputFilesNew.append(path_prefix + f)                               
    else:
        inputFilesNew = mergeName
        mergeNameNew = mergeName

    Verbose("Creating file \"%s\" from the following files:\n\t%s" % (mergeNameNew, "\n\t".join(inputFilesNew)) )
    
    # Construct the ROOT-file merge command (hadd)
    cmd = ["hadd"]
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

    histoPath = "configInfo/configinfo" #bin1=control (=number_of_merged-files), bin2=energy (=13*number_of_merged-files)
    Verbose("Investigating \"%s\" in merged file \"%s\"" % (histoPath, mergedFile) )
    tfile = ROOT.TFile.Open(mergedFile)
    configinfo = tfile.Get(histoPath)
    if configinfo:
	info = histoToDict(configinfo)
        if int(info["control"]) != len(inputFiles):
            raise SanityCheckException("configInfo/configinfo:control = %d, len(inputFiles) = %d" % (int(info["control"]), len(inputFiles)))


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
    Verbose("delete()")
    
    # Definitions
    prefix = ""
    if opts.filesInEOS:
        prefix = GetXrdcpPrefix(opts)
    filePath = prefix + fileName
    fileMode = "UPDATE"

    # Open the ROOT file
    Verbose("Opening ROOT file \"%s\" in \"%s\" mode." % (filePath, fileMode) )
    fIN = ROOT.TFile.Open(filePath, fileMode)
    if fIN == None:
        raise Exception("Could not open \"%s\". Does it exist?" % (filePath) )
    fIN.cd()
    keys = fIN.GetListOfKeys()

    # For-loop: All keys in TFILE
    for i in range(len(keys)):
        if keys.At(i):
            keyName = keys.At(i).GetName()
            dir = fIN.GetDirectory(keyName)
            if dir:
                fIN.cd(keyName)
                Verbose("Deleting folder matching \"%s\" in file \"%s\"." % (regexp, filePath) )
                delFolder(regexp)
                fIN.cd()
    delFolder(regexp)
    fIN.Close()
    return


def pileup(fileName, opts):
    '''
    '''
    Verbose("pileup(): Hasn't been tested yet!", True)
    
    if FileExists(fileName, opts ) == False:
        raise Exception("The file \"%s\" does not exist!" % (fileName) )

    # Definitions
    prefix = ""
    if opts.filesInEOS:
        prefix = GetXrdcpPrefix(opts)
    filePath = prefix + fileName
    fileMode = "UPDATE"

    # Open the ROOT file
    Verbose("Opening ROOT file \"%s\" in \"%s\" mode." % (filePath, fileMode) )
    fOUT = ROOT.TFile.Open(filePath, fileMode)
    fOUT.cd()

    # Definitoins
    hPU   = None
    dv_re = re.compile("data")  
    match = dv_re.search(dataVersion.GetTitle())
    dataVersion = fOUT.Get("configInfo/dataVersion")
    if match: 
        puFileTmp = os.path.join(os.path.dirname(filePath), "PileUp.root")
        puFile    = prefix + puFileTmp
        if FileExists(puFile):
            fIN      = ROOT.TFile.Open(puFile)
            hPU     = fIN.Get("pileup")
            hPUup   = fIN.Get("pileup_up")
            hPUdown = fIN.Get("pileup_down")
        else:
            Print("PileUp not found in", os.path.dirname(filePath), ", did you run hplusLumiCalc.py?")
        if not hPU == None:
            fOUT.cd("configInfo")
            hPU.Write("", ROOT.TObject.kOverwrite)
            hPUup.Write("", ROOT.TObject.kOverwrite)
            hPUdown.Write("", ROOT.TObject.kOverwrite)

        Verbose("Closing file \"%s\"." % (filePath) )
        fOUT.Close()
    return


def delFolder(regexp):
    '''
    '''
    Verbose("delFolder()")

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


def CheckThatFilesExist(fileList, opts):
    '''
    '''
    Verbose("CheckThatFilesExist()", True)

    # For-loop: All files in list
    for f in fileList:
        if FileExists(f, opts ) == False:
            raise Exception("The file \"%s\" does not exist!" % (f) )
            return False
    return True


def FileExists(filePath, opts):
    '''
    Checks that a file exists by executing the ls command for its full path, 
    or the corresponding "EOS" command if opts.filesInEOS is enabled.
    '''
    Verbose("FileExists()", False)
    
    #if opts.filesInEOS: #fixme: limits use of FileExists
    if "CRAB3_TransferData" in filePath: # fixme: just a better alternative to "if opts.filesInEOS:"
        cmd = ConvertCommandToEOS("ls", opts) + " " + filePath
        ret = Execute("%s" % (cmd) )
        # If file is not found there won't be a list of files; there will be an error message
        errMsg = ret[0]
        if "Unable to stat" in errMsg:
            return False
        elif errMsg == filePath.split("/")[-1]:
            return True
        else:
            raise Exception("This should not be reached! Execution of command \"%s\" returned \"%s\"" % (cmd, errMsg))
    else:
        if os.path.isfile(filePath):
            return True
        else:
            return False
    return True


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

        Verbose("Will include the following tasks (using re) :%s" % (include) )
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

    Verbose("Determining prefix for xrdcp for host \"%s\"" % (HOST) )
    if "fnal" in HOST:
        path_prefix = "root://cmseos.fnal.gov/"
    elif "lxplus" in HOST:
        path_prefix = "root://eoscms.cern.ch//eos//cms/"
    else:
        raise Exception("Unsupported host \"%s\"" % (HOST) )
    return path_prefix


def MergeFiles(mergeName, mergeNameEOS, inputFiles, opts):
    '''
    Merges ROOT files, either stored locally or on EOS.
    '''
    if len(inputFiles) == 1:
        if opts.filesInEOS:
            prefix   = GetXrdcpPrefix(opts)
            srcFile  = prefix + inputFiles[0]
            destFile = prefix + mergeNameEOS
            cmd      = "xrdcp %s %s" % (srcFile, destFile)
            Verbose(cmd)
            ret = Execute(cmd)
            # return ret
            return 0
        else:
            Verbose("cp %s %s" % (inputFiles[0], mergeName) )
            if not opts.test:
                shutil.copy(inputFiles[0], mergeName)
            else:
                pass
            return 0
    else:
        if opts.filesInEOS:
            ret = hadd(opts, mergeNameEOS, inputFiles, GetXrdcpPrefix(opts) )
            #Print("Done \"%s\" (\"%s\" GB)." % (mergeNameEOS, GetFileSize(mergeNameEOS, opts, True) ), False )
            return ret
        else:
            ret = hadd(opts, mergeName, inputFiles)    
            return ret


def main(opts, args):
    '''
    '''
    Verbose("main()", True)
    
    # Get the multicrab task names (=dir names)
    crabDirsTmp = multicrab.getTaskDirectories(opts)
    crabdirs    = GetIncludeExcludeDatasets(crabDirsTmp, opts)

    Verbose("The multicrab directories are:\n\t%s" % ( "\n\t".join(crabdirs)), True)

    # Construct regular expressions for output files
    global re_histos
    re_histos.append(re.compile("^output files:.*?(?P<file>%s)" % opts.input))
    re_histos.append(re.compile("^\s+file\s+=\s+(?P<file>%s)" % opts.input))
    exit_re = re.compile("/results/cmsRun_(?P<exitcode>\d+)\.log\.tar\.gz")

    mergedFiles = []
    # For-loop: All multicrab task names
    for d in crabdirs:
        d = d.replace("/", "")
        stdoutFiles = glob.glob(os.path.join(d, "results", "cmsRun_*.log.tar.gz"))
        Verbose("The stdout files for task \"%s\" are:\n\t%s" % ( d, "\n\t".join(stdoutFiles)), True)

        files     = []
        exitCodes = []
        # For-loop: All stdout files for task "d"
        for f in stdoutFiles:
            try:
                histoFile = GetHistogramFile(d, f, opts)
                if histoFile != None:
                    files.append(histoFile)
                else:
                    print "Task %s, skipping job %s: input root file not found from stdout" % (d, f)
            except multicrab.ExitCodeException, e:
                print "Task %s, skipping job %s: %s" % (d, f, str(e))
                exit_match = exit_re.search(f)
                if exit_match:
                    exitCodes.append(int(exit_match.group("exitcode")))

        # For Testing purposes
        if opts.test:
            if len(exitCodes) > 0:
                exitCodes_s = ""
                for i,e in enumerate(sorted(exitCodes)):
                    exitCodes_s += str(e)
                    if i < len(exitCodes)-1:
                        exitCodes_s += ","
                print "        jobs with problems:",len(exitCodes)
                print "        crab resubmit %s --jobids %s --force"%(d,exitCodes_s)
            continue

        if len(files) == 0:
            print "Task %s, skipping, no files to merge" % d
            continue
        
        CheckThatFilesExist(files, opts)
        Verbose("Found \"%s\" files for task \"%s\":\n\t%s" % (len(files), d, "\n\t".join(files)) )
        
        # Split files according to user-defined options
        filesSplit = splitFiles(files, opts.filesPerMerge, opts)
        if len(filesSplit) == 1:
            Print("Task %s, merging %d file(s)" % (d, len(files)) )
        else:
            Print("Task %s, merging %d files to %d file(s)" % (d, len(files), len(filesSplit)) )

        # For-loop: All splitted files
        for index, inputFiles in filesSplit:
            Print("Merging %s/%s" % (index+1, len(filesSplit)), False)
            taskName = d

            # Assign "task-number" if merging more than 1 files
            if len(filesSplit) > 1:
                taskName += "-%d" % index

            # Get the merge name of the files
            mergeName    = os.path.join(d, "results", opts.output % taskName)
            mergeNameEOS = ConvertPathToEOS(mergeName, "", opts)

            # If merge file exists already rename it as .backup            
            if opts.filesInEOS:
                if FileExists(mergeNameEOS, opts) and not opts.test:
                    mergeNameEOSNew = mergeNameEOS + ".backup"
                    Print("File \"%s\" already exists.\n\tRenaming to \"%s\"." % (mergeNameEOS, mergeNameEOSNew) )
                    fileName    = GetXrdcpPrefix(opts) + mergeNameEOS
                    fileNameNew = GetXrdcpPrefix(opts) + mergeNameEOSNew
                    cp_cmd      = "xrdcp %s %s" % (fileName, fileNameNew)
                    Verbose(cp_cmd)
                    ret = Execute(cp_cmd)

                    # Now remove the original file
                    rm_cmd = ConvertCommandToEOS("rm", opts) + " %s" % (mergeNameEOS)
                    Print(rm_cmd)
                    ret = Execute(rm_cmd)
            else:
                if FileExists(mergeName, opts) and not opts.test:
                    Print("mv %s %s" % (mergeName, mergeName + ".backup") )
                    shutil.move(mergeName, mergeName + ".backup")

            # Merge the ROOT files
            ret = MergeFiles(mergeName, mergeNameEOS, inputFiles, opts)
            if ret != 0:
                return ret
            
            # Inform user of progress
            if len(filesSplit) > 1:
                #Print("done %d" % index)
                Verbose("Merged \"%s\" (\"%0.3f\" GB)." % (mergeNameEOS, GetFileSize(mergeNameEOS, opts, True) ), False )
                
            # Keep track of merged files
            if opts.filesInEOS:
                mergedFiles.append((mergeNameEOS, inputFiles))
            else:
                mergedFiles.append((mergeName, inputFiles))

            # Sanity check
            try:
                if opts.filesInEOS:
                    sanityCheck(GetXrdcpPrefix(opts) + mergeNameEOS, inputFiles)
                else:
                    sanityCheck(mergeName, inputFiles)
            except SanityCheckException, e:
                Print("Task %s: %s; disabling input file deletion" % (d, str(e)) )
                opts.deleteImmediately = False
                opts.delete = False
            if opts.deleteImmediately:

                # For-loop: All input files
                for srcFile in inputFiles:
                    if not opts.test:
                        if opts.filesInEOS:
                            cmd = ConvertCommandToEOS("rm", opts) + " " + srcFile
                            Verbose(cmd)
                            ret = Execute(cmd)
                        else:
                            cmd = "rm %s" % srcFile
                            os.remove(srcFile)
                    else:
                        pass

    
    # Append "delete" message
    deleteMessage = ""
    if opts.delete:
        deleteMessage = " (source files deleted)"
    if opts.deleteImmediately:
        deleteMessage = " (source files deleted immediately)"

    Print("Merged histogram files%s:" % (deleteMessage), False)
    # For-loop: All merged files
    for f, sourceFiles in mergedFiles:
        Print("%s [from %d file(s)]" % (f, len(sourceFiles)), False)
        
        Verbose("Deleting folders in file \"%s\"." % (f) )
        delete(f, "Generated", opts)
        delete(f, "Commit", opts)
        delete(f, "dataVersion", opts)

        # Delete files after merging?
        if opts.delete and not opts.deleteImmediately:
            for srcFile in sourceFiles:
                if not opts.test:
                    if opts.filesInEOS:
                        cmd = ConvertCommandToEOS("rm", opts) + " " + srcFile
                        Verbose(cmd)
                        ret = Execute(cmd)
                    else:
                        cmd = "rm %s" % srcFile
                        Verbose(cmd)
                        os.remove(srcFile)
        pileup(f, opts)

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
    
    parser = OptionParser(usage="Usage: %prog [options]")
    multicrab.addOptions(parser)
    parser.add_option("-i", dest="input", type="string", default="histograms_.*?\.root",
                      help="Regex for input root files (note: remember to escape * and ? !) [default: 'histograms_.*?\.root']")

    parser.add_option("-o", dest="output", type="string", default="histograms-%s.root",
                      help="Pattern for merged output root files (use '%s' for crab directory name) [default: 'histograms-%s.root']")

    parser.add_option("--test", dest="test", default=False, action="store_true",
                      help="Just test, do not do any merging or deleting. Useful for checking what would happen. Implies --verbose [default: 'False']")

    parser.add_option("--delete", dest="delete", default=False, action="store_true",
                      help="Delete the source files to save disk space (default is to keep the files) [default: 'False']")

    parser.add_option("--deleteImmediately", dest="deleteImmediately", default=False, action="store_true",
                      help="Delete the source files immediately after merging to save disk space (--delete deletes them after all crab tasks have been merged) [default: 'False']")

    parser.add_option("--filesPerMerge", dest="filesPerMerge", default=-1, type="int",
                      help="Merge at most this many files together, possibly resulting to multiple merged files. Use case: large ntuples. (default: -1 to merge all files to one) [default: '-1']")

    parser.add_option("--filesInEOS", dest="filesInEOS", default=False, action="store_true",
                      help="The ROOT files to be merged are in an EOS. Merge the files from there (xrootd protocol). File locations are read from cmsRun_*.log.tar.gz files. [default: 'False']")

    parser.add_option("--includeTasks", dest="includeTasks" , default="", type="string", help="Only perform action for this dataset(s) [default: '']")

    parser.add_option("--excludeTasks", dest="excludeTasks" , default="", type="string", help="Exclude this dataset(s) from action [default: '']")    

    parser.add_option("--allowJobExitCode", dest="allowJobExitCodes", default=[], action="append", type="int",
                      help="Allow merging files from this non-zero job exit code (zero exe exit code is still required). Can be given multiple times [default: '[]']")

    parser.add_option("-v", "--verbose"    , dest="verbose"      , default=VERBOSE, action="store_true", help="Verbose mode for debugging purposes [default: %s]" % (VERBOSE))

    (opts, args) = parser.parse_args()

    if opts.filesPerMerge == 0:
        parser.error("--filesPerMerge must be non-zero")

    if opts.test:
        opts.verbose = True

    sys.exit(main(opts, args))
