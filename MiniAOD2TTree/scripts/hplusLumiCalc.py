#!/usr/bin/env python
'''
Prerequisites:
http://cms-service-lumi.web.cern.ch/cms-service-lumi/brilwsdoc.html

Description:
Once all the jobs have been successfully retrieved from a multicrab job two scripts must then be run:
1) hplusLumiCalc.py:
Calculates luminosity with LumiCalc and the pile-up with pileupCalc for collision dataset samples. There
is no need to run this if only MC samples were processed. 

2) hplusMergeHistograms.py:
Merges ROOT files into one (or more) files. It also reads TopPt.root and adds a "top-pt-correction-weigh" histogram in miniaod2tree.root files. 
The maximum allowable size for a single ROOT file is limited to 2 GB (but can be overwritten).

BRIL tools analyse data in the database server at CERN which is closed to the outside.
Therefore the most convienient way is to run the toolkit on hosts (private or public) at CERN. 
If you must use the software installed outside the CERN intranet, a ssh tunnel to the database server at CERN has to be established first. 
Since the tunneling procedure requires a valid cern computer account, a complete unregistered person will not be able to access the BRIL data in any case.
The following instruction assumes the easiest setup: 
you have two open sessions on the SAME off-site host, e.g. cmslpc32.fnal.gov, one for the ssh tunnel and another for execution. 
It is also assumed that all the software are installed and the $PATH variable set correctly on the execution shell.


Usage:
1) LXPLUS:
cd multicrab_AnalysisType_vXYZ_TimeStamp
export PATH=$HOME/.local/bin:/afs/cern.ch/cms/lumi/brilconda-1.0.3/bin:$PATH  (bash)
setenv PATH ${PATH}:$HOME/.local/bin:/afs/cern.ch/cms/lumi/brilconda-1.0.3/bin: (csh)
hplusLumicalc.py
or
hplusLumiCalc.py -i 2016 --transferToEOS --collisions 2016 --offsite

2) LPC (or outside LXPLUS in general):
open two terminals
for both terminals, ssh to the same machine (e.g. ssh -YK aattikis@cmslpc37.fnal.gov)
setup CMSSW and CRAB environments
terminal 1: (ssh tunneling session)
ssh -N -L 10121:itrac50012-v.cern.ch:10121 attikis@lxplus.cern.ch

terminal 2 (while terminal 1 is open):
cd multicrab_AnalysisType_vXYZ_TimeStamp
export PATH=$HOME/.local/bin:/afs/cern.ch/cms/lumi/brilconda-1.0.3/bin:$PATH  (bash)
setenv PATH ${PATH}:$HOME/.local/bin:/afs/cern.ch/cms/lumi/brilconda-1.0.3/bin: (csh)
hplusLumiCalc.py -i 2016 --transferToEOS --collisions 2016 --offsite


Comments:
brilcalc usage taken from
https://twiki.cern.ch/twiki/bin/view/CMS/CertificationTools#Lumi_calculation
PileUp calc according to
https://indico.cern.ch/event/459797/contribution/3/attachments/1181542/1711291/PPD_PileUp.pdf


Useful Links:
http://cms-service-lumi.web.cern.ch/cms-service-lumi/brilwsdoc.html

Installing BRIL:
bash
bash-4.1$ export PATH=$HOME/.local/bin:/afs/cern.ch/cms/lumi/brilconda-1.0.3/bin:$PATH
bash-4.1$ pip uninstall brilws
bash-4.1$ pip install --install-option="--prefix=$HOME/.local" brilws
'''

#================================================================================================
# Import Modules
#================================================================================================
import os
import re
import sys
import glob
import subprocess
import json
import getpass
import socket
from optparse import OptionParser
from collections import OrderedDict
import ROOT
from HiggsAnalysis.NtupleAnalysis.tools.aux import execute

import HiggsAnalysis.NtupleAnalysis.tools.multicrab as multicrab

#================================================================================================
# Global Definitions
#================================================================================================
PBARLENGTH  = 10

# Recommended minimum bias xsection
minBiasXsecNominal = 69200 #from https://twiki.cern.ch/twiki/bin/viewauth/CMS/POGRecipesICHEP2016

# JSON files
NormTagJSON     = "/afs/cern.ch/user/l/lumipro/public/normtag_file/normtag_DATACERT.json"
PileUpJSON_2016 = "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/PileUp/pileup_latest.txt"
PileUpJSON_2015 = "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/PileUp/pileup_latest.txt"

# Regular Expression
dataVersion_re = re.compile("dataVersion=(?P<dataVersion>[^: ]+)")
pu_re = re.compile("\|\s+\S+\s+\|\s+\S+\s+\|\s+.*\s+\|\s+.*\s+\|\s+\S+\s+\|\s+\S+\s+\|\s+(?P<lumi>\d+(\.\d*)?|\.\d+)\s+\|\s+(?P<pu>\d+(\.\d*)?|\.\d+)\s+\|\s+\S+\s+\|")


#================================================================================================
# Function Definition
#================================================================================================
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
        eosAlias = "eos root://cmseos.fnal.gov"
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


def GetEOSHomeDir(opts):
    home = "/store/user/%s/CRAB3_TransferData/%s" % (getpass.getuser(), opts.dirName)
    return home


def Execute(cmd):
    '''
    Executes a given command and return the output.
    '''
    Verbose("Execute()", True)
    Verbose("Executing command: %s" % (cmd))
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)

    stdin  = p.stdin
    stdout = p.stdout
    ret    = []
    for line in stdout:
        ret.append(line.replace("\n", ""))
    stdout.close()
    Verbose("Command %s returned:\n\t%s" % (cmd, "\n\t".join(ret)))
    return ret


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


def ConvertPathToEOS(taskName, fullPath, path_postfix, opts, isDir=False):
    '''
    Takes as input a path to a file or dir of a given multicrab task stored locally
    and converts it to the analogous path for EOS.
    '''
    Verbose("ConvertPathToEOS()", True)
 
    path_prefix = GetEOSHomeDir(opts)
    if not isDir:
        fileName      = fullPath.split("/")[-1]
    else:
        taskName      = fullPath
        fileName      = ""

    Verbose("Converting %s to EOS (taskName = %s, fileName = %s)" % (fullPath, taskName, fileName) )
    taskNameEOS   = ConvertTasknameToEOS(taskName, opts)
    pathEOS       = WalkEOSDir(taskName, os.path.join(path_prefix, taskNameEOS), opts)
    fullPathEOS   = pathEOS + path_postfix + fileName
    Verbose("Converted %s (default) to %s (EOS)" % (fullPath, fullPathEOS) )
    return fullPathEOS


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
    dirContents = [x for x in dirContents if isinstance(x, str)] # Remove non-string entries from list 
    dirContents = filter(bool, dirContents) # Remove empty string entries from list 
    if "\n" in dirContents[0]:
        dirContents = dirContents[0].split("\n")

    for d in dirContents:
        if d=="":
            dirContents.remove(d)
        
    if "symbol lookup error" in dirContents[0]:
        raise Exception("%s.\n\t%s." % (cmd, dirContents[0]) )

    Verbose("Walking the EOS directory %s with %s contents:\n\t%s" % (pathOnEOS, len(dirContents), "\n\t".join(dirContents) ) )

    # A very, very dirty way to find the deepest directory where the ROOT files are located!
    if len(dirContents) == 1:
        subDir = dirContents[0]
        Verbose("Found sub-directory %s under the EOS path %s!" % (subDir, pathOnEOS) )
        pathOnEOS = WalkEOSDir(taskName, os.path.join(pathOnEOS, subDir), opts)
    else:
        rootFiles = []
        # For-loop: All dir contents
        for d in dirContents:
            subDir = d 
            if "crab_" + taskName in subDir:
                pathOnEOS = WalkEOSDir(taskName, os.path.join(pathOnEOS, subDir), opts)
        
        for f in dirContents:
            if ".root" not in f:
                continue
            else:
                rootFiles.append( os.path.join(pathOnEOS, f) )
        pathOnEOS += "/"
        Verbose("Reached end of the line. Found %s ROOT files under %s."  % (len(rootFiles), pathOnEOS))
    return pathOnEOS


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


def AskUser(msg, printHeader=False):
    '''
    Prompts user for keyboard feedback to a certain question. 
    Returns true if keystroke is \"y\", false otherwise.
    '''
    Verbose("AskUser()", printHeader)
    
    fName = __file__.split("/")[-1]
    if printHeader==True:
        fullmsg = "=== " + fName
        fullmsg += "\n\t" + msg + " (y/n): "
    else:
        fullmsg = "\t" + msg + " (y/n): "

    keystroke = raw_input(fullmsg)
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


def Print(msg, printHeader=False):
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
    newDatasets = []
 
    # Include datasets
    if opts.includeTasks != "":
        tmp = []
        include = GetRegularExpression(opts.includeTasks)

        Verbose("Will include the following tasks (using re): %s" % (opts.includeTasks) )
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


def isMCTask(taskdir):
    crabCfg = "crabConfig_"+taskdir+".py"
    if not os.path.exists(crabCfg):
        print "crab.cfg at %s doesn't exist, assuming task is MC" % crabCfg
        return True

    f = open(crabCfg)
    isData = False
    for line in f:
        if "pyCfgParams" in line:
            m = dataVersion_re.search(line)
            if not m:
                print "Unable to find dataVersion, assuming task %s is MC" % taskdir
                return True
            if "data" in m.group("dataVersion"):
                isData = True
            break
    f.close()
    return not isData


def isEmpty(taskdir, opts):
    '''
    If task directory is empty return True
    '''    
    Verbose("isEmpty()", True)
    if opts.transferToEOS:
        return False
    path  = os.path.join(taskdir, "results")
    files = execute("ls %s"%path)
    return len(files)==0


def convertLumi(lumi, unit):
    '''
    Convert luminosity to pb^-1
    '''
    Verbose("convertLumi()")
    if unit == "ub":
        return lumi/1e6
    elif unit == "nb":
        return lumi/1e3
    elif unit == "pb":
        return lumi
    elif unit == "fb":
        return lumi*1e3
    else:
        raise Exception("Unsupported luminosity unit %s"%unit)


def GetCrabDirectories(opts):
    '''
    Return an alphabetically sorted list of datasets found under
    the multicrab dir used (opts.dirName)
    '''
    Verbose("GetCrabDirectories()", True)

    crabdirs = multicrab.getTaskDirectories(opts)
    crabdirs = filter(lambda x: "multicrab_" not in x, crabdirs) # Remove "multicrab_" directory from list 

    crabdirs = GetIncludeExcludeDatasets(crabdirs, opts)
    # Return list (alphabetically ordered)
    return sorted(crabdirs)


def GetLumiAndUnits(output):
    '''
    Reads output of "brilcalc" command 
    and finds and returns the lumi and units
    '''
    Verbose("GetLumiAndUnits()", True)

    # Definitions
    lumi = -1.0
    unit = None

    # Regular expressions
    unit_re = re.compile("totrecorded\(/(?P<unit>.*)\)") 
    lumi_re = re.compile("\|\s+(?P<recorded>\d+\.*\d*)\s+\|\s*$")

    Verbose("Looping over all lines out brilcalc command output")
    #For-loop: All lines in "crab report <task>" output
    for line in output:
        m = unit_re.search(line)
        if m:
            unit = m.group("unit")
            
        m = lumi_re.search(line)
        if m:
            lumi = float(m.group("recorded")) # lumiCalc2.py returns pb^-1

    if unit == None:
        raise Exception("Didn't find unit information from lumiCalc output:\n\t%s" % "".join(output))
    lumi = convertLumi(lumi, unit)
    return lumi, unit

        
def CallPileupCalc(task, fOUT, inputFile, inputLumiJSON, minBiasXsec, calcMode="true", maxPileupBin="100", numPileupBins="100", pileupHistName="pileup"):
    '''
    Script to estimate pileup distribution using xing instantaneous luminosity
    information and minimum bias cross section.  Output is TH1D stored in root
    file.     

    For more help type in the terminal:
    pileupCalc.py --help

    See the script on git-hub:
    https://github.com/cms-sw/RecoLuminosity-LumiDB/blob/master/scripts/pileupCalc.py
    '''
    Verbose("CallPileupCalc()", True)
    
    Verbose("Task %s, creating Pileup ROOT file" % (task) )
    cmd = ["pileupCalc.py", "-i", inputFile, "--inputLumiJSON", inputLumiJSON, "--calcMode", calcMode, 
           "--minBiasXsec", minBiasXsec, "--maxPileupBin", maxPileupBin, "--numPileupBins", numPileupBins, 
           fOUT, "--pileupHistName", pileupHistName] #, "--verbose"

    sys_cmd = " ".join([str(c) for c in cmd])
    Verbose(sys_cmd)
    pu     = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = pu.communicate()[0]
    ret    = pu.returncode
    if ret != 0:
        Print("Call to %s failed with return value %d with command" % (cmd[0], ret) )
        Print(" ".join(pucmd) )
        print output

    if len(output) > 0:
        Print(output) #fixme: "Consider using a higher value of --maxPileupBin"
    else:
        Verbose(output)
    return ret, output


def CallBrilcalc(task, BeamStatus, CorrectionTag, LumiUnit, InputFile, printOutput=False):
    '''
    Executes brilcalc and returns the execuble exit code and the output
    in the form of a list of strings.

    The original version of the code did not work for tcsh (built for "bash" I assume)
    p      = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = p.communicate()[0]
    ret    = p.returncode

    For more help type in the terminal:
    brilcalc lumi --help        
    '''
    Verbose("CallBrilcalc()", True)

    # brilcalc lumi -u /pb -i JSON-file
    home = os.environ['HOME']
    path = os.path.join(home, ".local/bin")
    exe  = os.path.join(path, "brilcalc")

    # Ensure brilcal executable exists
    if not os.path.exists(exe):
        Print("brilcalc not found, have you installed it?", True)
        Print("http://cms-service-lumi.web.cern.ch/cms-service-lumi/brilwsdoc.html")
        sys.exit()

    # Execute the command
    cmd     = [exe,"lumi", "-b", BeamStatus, "--normtag", CorrectionTag, "-u", LumiUnit, "-i", InputFile]
    cmd_ssh = ["-c", "offsite"]
    if opts.offsite:
        cmd.extend(cmd_ssh)

    brilcalc_out = os.path.join(task, "results", "brilcalc.log")
    sys_cmd = " ".join(cmd) + " > %s" %brilcalc_out
    Verbose(sys_cmd)

    ret    = os.system(sys_cmd)

    output = [i for i in open(brilcalc_out, 'r').readlines()]
    
    # If return value is not zero print failure
    if ret != 0:
        Print("Call to %s failed with return value %d with command" % (cmd[0], ret ), True)
        Print(" ".join(cmd) )
        Print(output)
        sys.exit()
        #return ret, output

    if printOutput:
        for o in output:
            print o.replace('\n', "")
    return ret, output


def Execute(cmd):
    '''
    Executes a given command and return the output.
    '''
    Verbose("Execute()", True)

    Verbose("Executing command: %s" % (cmd))
    p = subprocess.Popen(cmd, shell=True, executable='/bin/bash', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    output = p.communicate()[0]
    ret    = p.returncode
    return output, ret


def PrintPuFilesCreated(puFiles):
    '''
    Inform user of PileUp files created
    '''
    Verbose("PrintPuFilesCreated()", True)
    
    # Sort alphabetically
    puFiles = OrderedDict(sorted(puFiles.items(), key=lambda t: t[0]))

    # For-loop: All task-fList pairs
    index = -1
    for task, fList in puFiles.items():
        for f in fList:
            index +=1
            if index == 0:
                Print("File \"%s\" created." % (f), True)
            else:
                Print("File \"%s\" created." % (f) )
        
    return


def PrintSummary(data, lumiUnit):
    '''
    Prints a table summarising the task and the recorded luminosity.
    Also prints the total integrated luminosity.
    '''
    Verbose("PrintSummary()", True)
    table   = []
    table.append("")
    align   = "{:<3} {:<50} {:>20} {:<7}"
    hLine   = "="*80
    header  = align.format("#", "Task", "Luminosity", "")
    data    = OrderedDict(sorted(data.items(), key=lambda t: t[0]))
    table.append(hLine)
    table.append(header)
    table.append(hLine)

    index   = 0
    intLumi = 0
    # For-loop: All task-lumi pairs
    for task, lumi in data.items():
        index+=1
        table.append( align.format(index, task, "%.3f"%lumi, lumiUnit ) )
        intLumi+= lumi
    table.append(hLine)
    table.append( align.format("", "", "%.3f"%intLumi, lumiUnit) )
    table.append("")
    for row in table:
        Print(row)
    return


def IsSSHReady(opts):
    '''
    Ensures user confirms ssh tunnel is open
    '''
    Verbose("IsSSHReady()", True)

    if not opts.offsite:
        return
    cmd_ssh   = "ssh -N -L 10121:itrac50012-v.cern.ch:10121 <username>@lxplus.cern.ch\n\tPress "
    ssh_ready = AskUser("Script executed outside LXPLUS (--offsite enabled). Is the ssh tunneling session ready?\n\t%s" % (cmd_ssh), True)
    if not ssh_ready:
        sys.exit()
    else:
        return


def CopyFileToEOS(task, fOUT, opts):
    '''
    Copies file of given task to corresponding path onn EOS.
    '''
    Verbose("CopyFileToEOS()")
    fOUT_EOS = ConvertPathToEOS(task, fOUT, "", opts, isDir=False)
    Verbose("Copying %s to %s" % (fOUT, fOUT_EOS) )

    srcFile  = fOUT
    destFile = GetXrdcpPrefix(opts) + fOUT_EOS
    cmd      = "xrdcp %s %s" % (srcFile, destFile)
    Verbose(cmd)
    ret = Execute(cmd)
    #Print("File \"%s\" created." % (destFile), False)
    return fOUT_EOS


def CopyLumiJsonToEOS(f, opts):
    '''
    Copies file of given task to corresponding path onn EOS.
    '''
    Verbose("CopyLumiJsonToEOS()")

    srcFile   = f.name
    destFile_ = os.path.join(GetEOSHomeDir(opts), opts.dirName, srcFile)
    destFile  = GetXrdcpPrefix(opts) + destFile_
    cmd       = "xrdcp %s %s" % (srcFile, destFile)
    Verbose(cmd)
    ret = Execute(cmd)
    Print("File \"%s\" created." % (destFile_), False)
    return


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

    # Definitions
    HOST = socket.gethostname()
    path_prefix = ""

    Verbose("Determining prefix for xrdcp for host %s" % (HOST) )
    if "fnal" in HOST:
        path_prefix = "root://cmseos.fnal.gov/"
    elif "lxplus" in HOST:
        path_prefix = "root://eoscms.cern.ch//eos//cms/"
    else:
        raise Exception("Unsupported host %s" % (HOST) )
    return path_prefix


def main(opts, args):
    '''
    Calculates luminosity with LumiCalc and the pile-up with pileupCalc for collision dataset samples. 

    Summary:  
    +-------+------+------+------+-------------------+------------------+
    | nfill | nrun | nls  | ncms | totdelivered(/pb) | totrecorded(/pb) |
    +-------+------+------+------+-------------------+------------------+
    |   1   |  1   | 1585 | 1585 |       25.515      |      25.028      |
    +-------+------+------+------+-------------------+------------------+
    '''
    Verbose("main()", True)
    
    cell = "\|\s+(?P<%s>\S+)\s+"

    allowedColl = ["2015", "2016"]
    if opts.collisions == "2016":
        PileUpJSON = PileUpJSON_2016
    elif opts.collisions == "2015":
        PileUpJSON = PileUpJSON_2015
    else:
        Print("Unsupported collisions option \"%s\". Please select from the following:\n\t%s" % (opts.collisions, ", ".join( allowedColl) ), True)
        sys.exit()


    # Ensure user has the ssh tunnel session ready (if required)
    IsSSHReady(opts)

    if not opts.truncate and os.path.exists(opts.output):
        Verbose("Opening OUTPUT file %s in \"r\"(read) mode" % (opts.output) )
        f = open(opts.output, "r")
        data = json.load(f)
        f.close()
    
    files = []
    # only if no explicit files, or some directories explicitly given
    if len(opts.files) == 0 or len(opts.dirs) > 0:

        crabdirs = GetCrabDirectories(opts)
        
        # For-loop: All tasks
        for index, d in enumerate(crabdirs):

            if isMCTask(d):
                Print("%s, ignoring, it looks like MC" % d)
                continue

            if isEmpty(d, opts):
                Print("%s, ignoring, it looks empty" % d)
                continue
    
            if opts.report:
                multicrab.checkCrabInPath()
                cmd = ["crab", "report", d]
                Verbose(" ".join(cmd) )
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                output = p.communicate()[0]
                ret = p.returncode
                if ret != 0:
                    print "Call to 'crab -report -d %s' failed with return value %d" % (d, ret)
                    print output
                    return 1
                Verbose(output)

            # Append tuple (task, json) to files list
            files.append((d, os.path.join(d, "results", "processedLumis.json")))

            # Update progress bar
            PrintProgressBar(d + ", Crab Report", index, len(crabdirs) )

    # Flush stdout
    FinishProgressBar()

    # Extend the list
    files.extend([(None, f) for f in opts.files])

    data     = {}
    puFiles  = {}
    index    = -1
    lumiUnit = ""
    # For-loop: All json files
    for task, jsonfile in files:
        index += 1
        
        Verbose("%s, %s" % (task, os.path.basename(jsonfile) ) )
        lumicalc = opts.lumicalc

        # Run the steps to get the Pileup histo
        PrintProgressBar(task + ", BrilCalc   ", index, len(files), "[" + os.path.basename(jsonfile) + "]")
        ret, output =  CallBrilcalc(task, BeamStatus='"STABLE BEAMS"', CorrectionTag=NormTagJSON, LumiUnit="/pb", InputFile=jsonfile)

        # Determine Lumi and units from output
        Verbose("Determining Luminosity and its Units")
        lumi, lumiUnit = GetLumiAndUnits(output)

        # Save lumi in task-lumi dictionary
        data[task] = lumi 

        # Save the json file after each data task in case of future errors
        if len(data) > 0:
            Verbose("Opening OUTPUT file %s in \"w\"(=write) and \"b\"(=binary) mode" % (opts.output) )
            f = open(opts.output, "wb")
            json.dump(data, f, sort_keys=True, indent=2)
            f.close()
        else:
            pass

        # PileUp [https://twiki.cern.ch/twiki/bin/view/CMS/PileupSystematicErrors]
        minBiasXsec = minBiasXsecNominal
        Verbose("Task %s, creating Pileup ROOT files" % (task) )
        fOUT     = os.path.join(task, "results", "PileUp.root")
        hName = "pileup"
        PrintProgressBar(task + ", PileupCalc ", index, len(files), "[" + os.path.basename(jsonfile) + "]")
        ret, output = CallPileupCalc(task, fOUT, jsonfile, PileUpJSON, str(minBiasXsec), calcMode="true", maxPileupBin="50", numPileupBins="50", pileupHistName=hName)

            
        Verbose("Task %s, changing the --minBiasXsec value in the pileupCalc.py command by +0.05 around the chosen central value." % (task) )
	puUncert    = 0.05
        minBiasXsec = minBiasXsec*(1+puUncert)
        fOUT_up     = fOUT.replace(".root","_up.root")
        hName_up    = "pileup_up"
        PrintProgressBar(task + ", PileupCalc+", index, len(files), "[" + os.path.basename(jsonfile) + "]")
        ret, output = CallPileupCalc(task, fOUT_up, jsonfile, PileUpJSON, str(minBiasXsec), calcMode="true", maxPileupBin="50", numPileupBins="50", pileupHistName=hName_up)


        Verbose("Task %s, changing the --minBiasXsec value in the pileupCalc.py command by -0.05 around the chosen central value." % (task) )
        minBiasXsec = minBiasXsec*(1-puUncert)
        fOUT_down   = fOUT.replace(".root","_down.root")
        hName_down  = "pileup_down"
        PrintProgressBar(task + ", PileupCalc-", index, len(files), "[" + os.path.basename(jsonfile) + "]")
        ret, output = CallPileupCalc(task, fOUT_down, jsonfile, PileUpJSON, str(minBiasXsec), calcMode="true", maxPileupBin="50", numPileupBins="50", pileupHistName=hName_down)

        Verbose("Task %s, opening all Pileup ROOT files" % (task) )
	fPU      = ROOT.TFile.Open(fOUT     ,"UPDATE")
	fPU_up   = ROOT.TFile.Open(fOUT_up  , "r")
        fPU_down = ROOT.TFile.Open(fOUT_down, "r")


        Verbose("Task %s, getting Up/Down Pileup histograms from corresponding ROOT files" % (task) )
	h_pu      = fPU.Get("pileup")
	h_pu_up   = fPU_up.Get("pileup_up")
        h_pu_down = fPU_down.Get("pileup_down")


        Verbose("Task %s, sanity check on Pileup histograms" % (task) )        
        hList = []
        hList.append(h_pu)
        hList.append(h_pu_up)
        hList.append(h_pu_down)
        #For-loop: All histos
        for h in hList:
            Verbose("Histogram %s (xMin=%s, xMax=%s) has %s entries (mean=%s, RMS=%s)" % (h.GetName(), h.GetXaxis().GetXmin(), h.GetXaxis().GetXmax(), h.GetEntries(), h.GetMean(), h.GetRMS() ) )
            

        Verbose("Task %s, writing Up/Down Pileup ROOT histos to %s file" % (task, fPU.GetName() ) )
	fPU.cd()
	h_pu_up.Write()
        h_pu_down.Write()

        # Update progress bar        
        PrintProgressBar(task + ", Close Files", index, len(files), "[" + os.path.basename(jsonfile) + "]")

        Verbose("Task %s, closing Pileup ROOT files" % (task) )
	fPU.Close()
        fPU_up.Close()
        fPU_down.Close()
        
        # Save ROOT files names
        rList = [fPU.GetName(), fPU_up.GetName(), fPU_down.GetName()]

        # Copy files to EOS?
        if opts.transferToEOS:
            fOUT_EOS      = CopyFileToEOS(task, fOUT     , opts)    
            fOUT_up_EOS   = CopyFileToEOS(task, fOUT_up  , opts)    
            fOUT_down_EOS = CopyFileToEOS(task, fOUT_down, opts)    
            rList.extend([fOUT_EOS, fOUT_up_EOS, fOUT_down_EOS])

        # Create task-file dictionary
        puFiles[task] = rList

    # Flush stdout
    FinishProgressBar()

    # Print Pileup files created
    PrintPuFilesCreated(puFiles)

    # Dump all the luminosity data to the output file 
    if len(data) > 0:
        Verbose("Opening OUTPUT file %s in \"w\"(=write) and \"b\"(=binary) mode" % (opts.output) )
        f = open(opts.output, "wb")
        json.dump(data, f, sort_keys=True, indent=2)
        f.close()
        Print("File \"%s\" created." % (f.name), True)
        if opts.transferToEOS:
            CopyLumiJsonToEOS(f, opts) 

    # Inform user of results
    PrintSummary(data, lumiUnit)

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
    FILES         = []
    OUTPUT        = "lumi.json"
    TRUNCATE      = False
    REPORT        = True
    VERBOSE       = False
    OFFSITE       = False
    COLLISIONS    = "2016"
    DIRNAME       = ""
    TRANSFERTOEOS = False

    parser = OptionParser(usage="Usage: %prog [options] [crab task dirs]\n\nCRAB task directories can be given either as the last arguments, or with -d.")

    multicrab.addOptions(parser)

    parser.add_option("-f", "--files", dest="files", type="string", action="append", default=FILES,
                      help="JSON files to calculate the luminosity for (this or -d is required) [default: %s]" % (FILES) )

    parser.add_option("-o", "--output", dest="output", type="string", default=OUTPUT,
                      help="Output file to write the dataset integrated luminosities [default: %s]" % (OUTPUT) )

    parser.add_option("--truncate", dest="truncate", default=TRUNCATE, action="store_true",
                      help="Truncate the output file before writing [default: %s]" % (TRUNCATE) )

    parser.add_option("--noreport", dest="report", action="store_false", default=REPORT,
                      help="Do not run 'crab report', i.e. you guarantee that the processedLumis.json contains already all jobs. [default: %s]" % (REPORT) ) 

    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=VERBOSE,
                      help="Print outputs of the commands which are executed [default: %s]" % (VERBOSE) )

    parser.add_option("--lumiCalc1", dest="lumicalc", action="store_const", const="lumiCalc1",
                      help="Use lumiCalc.py instead of lumiCalc2.py")

    parser.add_option("--lumiCalc2", dest="lumicalc", action="store_const", const="lumiCalc2",
                      help="Use lumiCalc2.py (default is to use pixelLumiCalc.py)")

    parser.add_option("--pixelLumiCalc", dest="lumicalc", action="store_const", const="pixelLumiCalc",
                      help="Use pixelLumiCalc.py instead of lumiCalc2.py (default)")

    parser.add_option("-i", "--includeTasks", dest="includeTasks" , default="", type="string", 
                      help="Only perform action for this dataset(s) [default: '']")

    parser.add_option("--offsite", dest="offsite" , action="store_true", default=OFFSITE, 
                      help="Run bril tools as usual with connection string -c offsite. [default: %s]" % (OFFSITE) )

    parser.add_option("-c", "--collisions", dest="collisions", type="string", default=COLLISIONS, 
                      help="The year of collisions considered, to determine the correct PileUp txt file for pileupCalc. [default: %s]" % (COLLISIONS) )

    parser.add_option("--dirName", dest="dirName", default=DIRNAME, type="string",
                      help="Custom name for CRAB directory name [default: %s]" % (DIRNAME))

    parser.add_option("--transferToEOS", dest="transferToEOS", default=TRANSFERTOEOS, action="store_true",
                      help="The output ROOT files will be transfered to appropriate EOS paths [default: '%s']" % (TRANSFERTOEOS) )

    (opts, args) = parser.parse_args()
    opts.dirs.extend(args)
    
    if opts.dirName == "":
        opts.dirName = os.path.basename(os.getcwd())

    if "lxplus" not in socket.gethostname() and not opts.offsite:
        Print("Must enable the --offsite option when working outside LXPLUS. Read docstrings. Exit", True)
        #print __doc__
        sys.exit()

    if opts.lumicalc == None:
        opts.lumicalc = "brilcalc"

    if opts.collisions == None:
        Print("Must provide the year of collisions to consider, to determine the Pilep txt used by pileupCalc (e.g. --collisions 2016). Exit", True)
        sys.exit()

    # Inform user
    Print("Calculating luminosity with %s" % opts.lumicalc, True)
    Print("Calculating pileup with pileupCalc (collisions %s)" % (opts.collisions) )

    sys.exit(main(opts, args))
