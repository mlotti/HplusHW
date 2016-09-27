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

Usage:
cd multicrab_AnalysisType_vXYZ_TimeStamp
hplusMergeHistograms.py

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

    if opts.filesInSE:
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


def WalkEOSDir(pathOnEOS, opts):
    '''
    Looks inside the EOS path "pathOnEOS" directory by directory.
    Since OS commands do not work on EOS, I have written this function
    in a vary "dirty" way.. hoping to make it more robust in the future!
    '''
    # Verbose("WalkEOSDir()", True)
    
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
    # cmdMap["ls"] = "eos ls" #Will NOT work due to a conflict between the EOS and CMSSW environment
    cmdMap["ls"] = "/afs/cern.ch/project/eos/installation/0.3.84-aquamarine/bin/eos.select ls" #"eos ls" is an ALIAS for this command. Works
    cmdMap["rm"] = "eos rm"

    # EOS commands differ on LPC!
    if "fnal" in socket.gethostname():
        for key in cmdMap:
            if key == "ls": # exception because I use the full command, not the alias
                cmdMap[key] = "eosls"
            else:
                cmdMap[key] = cmdMap[key].replace("eos ", "eos")

    if cmd not in cmdMap:
        raise Exception("Could not find EOS-equivalent for cammand \"%s\"." % (cmd) )

    return cmdMap[cmd]


def Execute(cmd):
    '''
    Executes a given command and return the output.
    '''
    #Verbose("Execute()", True)
    #Verbose("Executing command: \"%s\"" % (cmd))
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)

    stdin  = p.stdout
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


def splitFiles(files, filesPerEntry):
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

        print "HERE-1"
        # For-loop: All files
        for ifile,f in enumerate(files):

            print "ifile = ", ifile
            print "f = ", f
            # Calculate cumulative size
            print "HERE-2"
            sumsize += os.stat(f).st_size

            sys.exit() #iro
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

    Verbose("len(ret) = %s, ret = %s" % (len(ret), ret) )
    return ret


def hadd(opts, mergeName, inputFiles):
    '''
    '''
    cmd = ["hadd"]
    if opts.filesInSE:
        cmd.append("-T") # don't merge TTrees via xrootd
    cmd.append(mergeName)
    cmd.extend(inputFiles)
    if opts.verbose:
        print " ".join(cmd)
    if opts.test:
        return 0
    args = {}
    if not opts.verbose:
        args = {"stdout": subprocess.PIPE, "stderr": subprocess.STDOUT}
    p = subprocess.Popen(cmd, **args)
    output = p.communicate()[0]
    ret = p.returncode
    if ret != 0:
        if not opts.verbose:
            print output
        print "Merging failed with exit code %d" % ret
        return 1
    return 0


def hplusHadd(opts, mergeName, inputFiles):
    '''
    '''
    args = {}
    if not opts.verbose:
        args = {"stdout": subprocess.PIPE, "stderr": subprocess.STDOUT}

    intermediateFiles = []
    resultFiles = inputFiles[:]
    mergeRound = 0
    while len(resultFiles) > 1:
        splitted = splitFiles(resultFiles, opts.fastFilesPerMerge)
        resultFiles = []
        for index, files in splitted:
            if len(splitted) > 1 or mergeRound > 0:
                print "     merge round %d, split round %d" % (mergeRound, index)
            target = mergeName+"-m%d-s%d" % (mergeRound, index)
            if os.path.exists(target):
                shutil.move(target, target+".backup")
            cmd = ["hplusHadd.py", target]+files
            if opts.verbose:
                cmd.append("--verbose")
                print " ".join(cmd)
            if not opts.test:
                p = subprocess.Popen(cmd, **args)
                output = p.communicate()[0]
                ret = p.returncode
                if ret != 0:
                    if not opts.verbose:
                        print output
                    print "Merging failed with exit code %d" % ret
                    return 1
                if not opts.verbose and "Error in" in output:
                    print output
            resultFiles.append(target)
            intermediateFiles.append(target)
        mergeRound += 1

    if intermediateFiles[-1] != resultFiles[0]:
        raise Exception("Assertion, intermediateFiles[-1] = %s != resultFiles[0] = %s" % (intermediateFiles[-1], resultFiles[0]))
    intermediateFiles.pop()

    for tmp in intermediateFiles:
        if opts.verbose:
            print "rm %s" % tmp
        if not opts.test:
            os.remove(tmp)

    if opts.verbose:
        print "mv %s %s" % (resultFiles[0], mergeName)
    if not opts.test:
        shutil.move(resultFiles[0], mergeName)
    
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
    tfile = ROOT.TFile.Open(mergedFile)
    configinfo = tfile.Get("configInfo/configinfo")
    if configinfo:
	info = histoToDict(configinfo)
        if int(info["control"]) != len(inputFiles):
            raise SanityCheckException("configInfo/configinfo:control = %d, len(inputFiles) = %d" % (int(info["control"]), len(inputFiles)))

def delete(fname,regexp):
    '''
    '''
    fIN = ROOT.TFile.Open(fname,"UPDATE")
    fIN.cd()
    keys = fIN.GetListOfKeys()
    for i in range(len(keys)):
        if keys.At(i):
            keyName = keys.At(i).GetName()
            dir = fIN.GetDirectory(keyName)
            if dir:
                fIN.cd(keyName)
                delFolder(regexp)
                fIN.cd()
    delFolder(regexp)
    fIN.Close()

def pileup(fname):
    '''
    '''
    if os.path.exists(fname):
        fOUT = ROOT.TFile.Open(fname,"UPDATE")
        fOUT.cd()

        hPU = None

        dataVersion = fOUT.Get("configInfo/dataVersion")
        dv_re = re.compile("data")  
        match = dv_re.search(dataVersion.GetTitle())
        if match:
            puFile = os.path.join(os.path.dirname(fname),"PileUp.root")
            if os.path.exists(puFile):
                fIN = ROOT.TFile.Open(puFile)
                hPU = fIN.Get("pileup")
		hPUup = fIN.Get("pileup_up")
		hPUdown = fIN.Get("pileup_down")
            else:
                print "PileUp not found in",os.path.dirname(fname),", did you run hplusLumiCalc?"
#        else:
#
#            tree = fOUT.Get("Events")
#            tree.Draw("nPUvertices>>PileUp(50,0,50)", "", "goff e")
#            hPU = tree.GetHistogram().Clone()

        if not hPU == None:
            fOUT.cd("configInfo")
            hPU.Write("",ROOT.TObject.kOverwrite)
            hPUup.Write("",ROOT.TObject.kOverwrite)
            hPUdown.Write("",ROOT.TObject.kOverwrite)

        fOUT.Close()

def delFolder(regexp):
    '''
    '''
    keys = ROOT.gDirectory.GetListOfKeys()
    del_re = re.compile(regexp)
    deleted = False
    for i in reversed(range(len(keys))):
        if keys.At(i):
            keyName = keys.At(i).GetName()
            match = del_re.search(keyName)
            if match:
                if not deleted:
                    deleted = True
                else:
                    cycle = keys.At(i).GetCycle()
                    ROOT.gDirectory.Delete(keyName+";%i"%cycle)


def GetRegularExpression(arg):
    Verbose("GetRegularExpression()", True)
    if isinstance(arg, basestring):
        arg = [arg]
    return [re.compile(a) for a in arg]


def CheckThatFilesExist(fileList, opts):
    '''
    '''
    Verbose("CheckThatFilesExist()")

    # For-loop: All files in list
    for f in fileList:
        if FileExists(f, opts ) == False:
            return False
    return True


def FileExists(filePath, opts):
    '''
    Checks that a file exists by executing the ls command for its full path, 
    or the corresponding "EOS" command if opts.filesInSE is enabled.
    '''
    Verbose("FileExists()", False)
    
    if opts.filesInSE:
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
        if not os.path.isfile(filePath):
            raise Exception("File \"%s\" is marked as output file in the CMSSW_N.stdout, but does not exist" % filePath)
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
    if opts.excludeTasks != "None":
        tmp = []
        exclude = GetRegularExpression(opts.excludeTasks)
        
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
    if opts.includeTasks != "None":
        tmp = []
        include = GetRegularExpression(opts.includeTasks)
        
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
        
        # Split files accordint to user-defined options
        filesSplit = splitFiles(files, opts.filesPerMerge)

        if len(filesSplit) == 1:
            print "Task %s, merging %d file(s)" % (d, len(files))
        else:
            print "Task %s, merging %d file(s) to %d files" % (d, len(files), len(filesSplit))

        for index, inputFiles in filesSplit:
            tmp = d
            if len(filesSplit) > 1:
                tmp += "-%d" % index
            mergeName = os.path.join(d, "results", opts.output % tmp)
            if os.path.exists(mergeName) and not opts.test:
                if opts.verbose:
                    print "mv %s %s" % (mergeName, mergeName+".backup")
                shutil.move(mergeName, mergeName+".backup")

            # FIXME: add here reading of first xrootd file, finding all TTrees, and writing the TList to mergeName file
            if opts.filesInSE:
                raise Exception("--filesInSE feature is not fully implemented")

            if len(inputFiles) == 1:
                if opts.verbose:
                    print "cp %s %s" % (inputFiles[0], mergeName)
                if not opts.test:
                    shutil.copy(inputFiles[0], mergeName)
                
            else:
                if opts.fast:
                    ret = hplusHadd(opts, mergeName, inputFiles)
                    if ret != 0:
                        return ret
                else:
                    ret = hadd(opts, mergeName, inputFiles)
                    if ret != 0:
                        return ret
    
            if len(filesSplit) > 1:
                print "  done %d" % index
            mergedFiles.append((mergeName, inputFiles))
            try:
                sanityCheck(mergeName, inputFiles)
            except SanityCheckException, e:
                print "Task %s: %s; disabling input file deletion" % (d, str(e))
                opts.deleteImmediately = False
                opts.delete = False
            if opts.deleteImmediately:
                for srcFile in inputFiles:
                    if opts.verbose:
                        print "rm %s" % srcFile
                    if not opts.test:
                        os.remove(srcFile)

    deleteMessage = ""
    if opts.delete:
        deleteMessage = " (source files deleted)"
    if opts.deleteImmediately:
        deleteMessage = " (source files deleted immediately)"

    print
    print "Merged histogram files%s:" % deleteMessage
    for f, sourceFiles in mergedFiles:
        print "  %s (from %d file(s))" % (f, len(sourceFiles))
        delete(f,"Generated")
        delete(f,"Commit")
        delete(f,"dataVersion")
        if opts.delete and not opts.deleteImmediately:
            for srcFile in sourceFiles:
                if opts.verbose:
                    print "rm %s" % srcFile
                if not opts.test:
                    os.remove(srcFile)
        pileup(f)

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
                      help="Regex for input root files (note: remember to escape * and ? !) (default: 'histograms_.*?\.root')")

    parser.add_option("-o", dest="output", type="string", default="histograms-%s.root",
                      help="Pattern for merged output root files (use '%s' for crab directory name) (default: 'histograms-%s.root')")

    parser.add_option("--test", dest="test", default=False, action="store_true",
                      help="Just test, do not do any merging or deleting (might be useful for checking what would happen). Implies --verbose.")

    parser.add_option("--delete", dest="delete", default=False, action="store_true",
                      help="Delete the source files to save disk space (default is to keep the files)")

    parser.add_option("--deleteImmediately", dest="deleteImmediately", default=False, action="store_true",
                      help="Delete the source files immediately after merging to save disk space (--delete deletes them after all crab tasks have been merged)")

    parser.add_option("--fast", dest="fast", default=False, action="store_true",
                      help="Use hplusHadd.py instead of hadd, it is faster but works only for TH1's. It also consumes (much) more memory, and is run for a couple of files at a time (see --fastFilesPerMerge).")

    parser.add_option("--fastFilesPerMerge", dest="fastFilesPerMerge", default=4, type="int",
                      help="With --fast, merge this many files at a time (default: 4)")

    parser.add_option("--filesPerMerge", dest="filesPerMerge", default=-1, type="int",
                      help="Merge at most this many files together, possibly resulting to multiple merged files. Use case: large ntuples. (default: -1 to merge all files to one)")

    parser.add_option("--filesInSE", dest="filesInSE", default=False, action="store_true",
                      help="The ROOT files to be merged are in an SE, merge the files from there. File locations are read from CMSSW_*.stdout files. NOTE: TTrees are not merged (it is assumed that due to TTrees the files are so big that they have to be stored in SE), but are replaced with TList of strings of the PFN's of the files via xrootd protocol.")

    parser.add_option("--includeTask", dest="includeTasks" , default="None" , type="string", help="Only perform action for this dataset(s) [default: \"\"]")

    parser.add_option("--excludeTask", dest="excludeTasks" , default="None" , type="string", help="Exclude this dataset(s) from action [default: \"\"]")    

    parser.add_option("--allowJobExitCode", dest="allowJobExitCodes", default=[], action="append", type="int",
                      help="Allow merging files from this non-zero job exit code (zero exe exit code is still required). Can be given multiple times.")

    parser.add_option("-v", "--verbose"    , dest="verbose"      , default=VERBOSE, action="store_true", help="Verbose mode for debugging purposes [default: %s]" % (VERBOSE))

    (opts, args) = parser.parse_args()

    if opts.filesPerMerge == 0:
        parser.error("--filesPerMerge must be non-zero")

    if opts.test:
        opts.verbose = True

    sys.exit(main(opts, args))
