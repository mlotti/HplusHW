#!/usr/bin/env python
'''
DESCRIPTION:
Check status of multible CONDOR jobs under 
a given sub-directory


USAGE:
checkCondor.py [options]


EXAMPLE:
checkCondor.py -d TopMassLE400_BDT0p40_AbsEta0p8_1p4_2p0_Pt_60_90_160_300_Stat_22Jul2018


LAST USED:
checkCondor.py -d TopMassLE400_BDT0p40_AbsEta0p8_1p4_2p0_Pt_60_90_160_300_Stat_22Jul2018 --getoutput
checkCondor.py -d TopMassLE500_BDT0p40_AbsEta0p8_1p4_2p0_Pt_60_90_160_300_Stat_24Jul2018 --resubmit


USEFUL LINKS:
https://uscms.org/uscms_at_work/computing/setup/condor_worker_node.shtml#userInputFile
https://uscms.org/uscms_at_work/computing/setup/batch_systems.shtml#condor_6
http://research.cs.wisc.edu/htcondor/manual/v8.6/2_6Managing_Job.html
http://pages.cs.wisc.edu/~adesmet/status.html
'''

#================================================================================================ 
# Modules here
#================================================================================================ 
import subprocess
from subprocess import Popen, PIPE
import os
import sys
import re
import datetime
import getpass 
from optparse import OptionParser 

import HiggsAnalysis.NtupleAnalysis.tools.ShellStyles as ShellStyles


#================================================================================================ 
# Variable definition
#================================================================================================ 
ss  = ShellStyles.SuccessStyle()
ns  = ShellStyles.NormalStyle()
ts  = ShellStyles.NoteStyle()
hs  = ShellStyles.HighlightAltStyle()
ls  = ShellStyles.HighlightStyle()
es  = ShellStyles.ErrorStyle()
cs  = ShellStyles.CaptionStyle()
cys = ShellStyles.CyanStyle()

#================================================================================================ 
# Function Definitions
#================================================================================================ 
def Verbose(msg, printHeader=False):
    if not opts.verbose:
        return
    if printHeader:
        print "=== checkCondor.py:"

    if msg !="":
        print "\t", msg
    return

def GetFName():
    fName = __file__.split("/")[-1]
    fName = fName.replace(".pyc", ".py")
    return fName


def Print(msg, printHeader=True):
    fName = GetFName()
    if printHeader:
        print "=== ", fName
    if msg !="":
        print "\t", msg
    return


def PrintFlushed(msg, printHeader=True):
    '''
    Useful when printing progress in a loop
    '''
    msg = "\r\t" + msg
    if printHeader:
        print "=== ", GetFName()
    sys.stdout.write(msg)
    sys.stdout.flush()
    return     


def AskUser(msg, printHeader=False):
    '''
    Prompts user for keyboard feedback to a certain question.
    Returns true if keystroke is \"y\", false otherwise.
    '''
    if printHeader:
                keystroke = raw_input("=== " + GetFName() + "\n\t" +  msg + " (y/n): ")
    else:
        keystroke = raw_input("\t" +  msg + " (y/n): ")

    if (keystroke.lower()) == "y":
        return True
    elif (keystroke.lower()) == "n":
        return False
    else:
        AskUser(msg)


def GetNumberOfJobsWithKeyword(dirName, fileName="output_FakeBMeasurement_Group*.txt", keyword="Results are in"):
    cmd = "cat %s/%s | grep -c '%s' " % (dirName, fileName, keyword)
    process = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    output, err = process.communicate()
    if len(err) > 0:
        raise Exception(es + err + ns)
    else:
        nJobs = int(output.replace(" ", ""))
    return nJobs


def GetJobsWithKeyword(dirName, analysis= "FakeBMeasurement", keyword="Results are in"):

    # Return items
    jdlList = []
    outList = []
    errList = []
    logList = []
    eosList = []

    # Get EOS files (if job fails corresponding file must be removed!)
    files, filesH2tb, filesFakeB = GetFilesInEOS(opts.eosdir)
    if analysis == "FakeBMeasurement":
        filesInEOS = filesFakeB
    elif analysis == "Hplus2tbAnalysis":
        filesInEOS = filesH2tb
    else:
        raise Exception("Invalid analysis type \"%s\" selected!" % (analysis))

    # Define files to search
    fileName = "error_%s_Group*.txt" % (analysis)
    cmd      = "grep -i -n -m1 --files-with-matches '%s' %s/%s" % (keyword, dirName, fileName)
    Verbose("Popen(%s, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)" % (cmd), True)
    process  = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    output, err = process.communicate()
    if len(err) > 0:
        #raise Exception(es + err + ns)
        Verbose(es + err + ns)
        return jdlList, errList, outList, logList, eosList
    else:
        jobs = output.splitlines()

    # For-loop: All failed jobs
    for j in jobs:
        
        f = os.path.basename(j)
        m = re.search('_Group(.+?)_', f)
        if m:
            jobGroup = m.group(1)
        else:
            raise Exception("Could not determine datasets group for file %s" % (f))

        n = re.search('_Syst(.+).txt', f)
        if n:
            jobSyst = n.group(1)
        else:
            raise Exception("Could not determine datasets group for file %s" % (f))
        
        # Get all job-related files
        jdl = "run_%s_Group%s_Syst%s.jdl"   % (analysis, jobGroup, jobSyst)
        err = "error_%s_Group%s_Syst%s.txt" % (analysis, jobGroup, jobSyst)
        out = "out_%s_Group%s_Syst%s.txt"   % (analysis, jobGroup, jobSyst)
        log = "log_%s_Group%s_Syst%s.txt"   % (analysis, jobGroup, jobSyst)
        jdlList.append(os.path.join(opts.dirName, jdl) )
        errList.append(os.path.join(opts.dirName, err) ) 
        outList.append(os.path.join(opts.dirName, out) ) 
        logList.append(os.path.join(opts.dirName, out) ) 
        
        # Definitions
        fGroup = "_Group%s_" % jobGroup
        fSyst  = "_Syst%s_"  % jobSyst
        iFile  = 0

        # For-loop: All EOS files
        for i, f in enumerate(filesInEOS, 1):
            
            match = fGroup in f and fSyst in f
            if not match:
                continue

            # Save output file of failed job in EOS
            eosList.append(os.path.join(opts.eosdir, f) )

    return jdlList, errList, outList, logList, eosList


def KillJobs(condorQ, opts):
    
    if opts.kill == "all":
        nJobs = len(condorQ["ID"])
        Print("Killing %d jobs" % (nJobs), True)
        for i, jobid in enumerate(condorQ["ID"], 1):
            #cmd = "condor_rm -submitter %s %s" % (getpass.getuser(), jobid)
            cmd = "condor_rm %s " % (jobid)
            PrintFlushed(cmd, i==1)
            os.system(cmd)
    else:
        killList = opts.kill.split(",")
        nJobs = len(killList)
        Print("Killing %d jobs" % (nJobs), True)
        for i, jobid in enumerate(killList, 1):
            #cmd = "condor_rm -submitter %s %s" % (getpass.getuser(), jobid)
            cmd = "condor_rm %s " % (jobid)
            PrintFlushed(cmd, i==1)
            os.system(cmd)
    return

def ResubmitFailedJobs(jdlList, errList, outList, logList, eosList):
    
    if len(jdlList) + len(errList) + len(outList) + len(eosList) < 1:
        return

    if opts.resubmit:
        msg = "Automatically resubmitting all failed jobs"
    else:
        msg = "Copy/paste the commands below to resubmit & clean all failed jobs"
    Print(ts + msg + ns, True)

    cwd = os.getcwd()
    os.chdir(opts.dirName)
    # For-loop: All job resubmits
    for i, jdl in enumerate(jdlList, 1):
        cmd = "cd %s && condor_submit %s" % (opts.dirName, os.path.basename(jdl))
        Print(ss + cmd + ns, i==0)
        if opts.resubmit:
            process = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
            output, err = process.communicate()
    os.chdir(cwd)

    #print
    # For-loop: All EOS files to be removed
    for i,f in enumerate(eosList, 1):
        cmd = "eosrm %s" % (f)
        Print(es + cmd + ns, i==0)
        if opts.resubmit:
            if AskUser(cmd):
                process = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
                output, err = process.communicate()
    
    #print 
    # For-loop: All error txt files to be removed
    for i,f in enumerate(errList, 1):
        cmd = "rm -f %s" % (f)
        Print(es + cmd + ns, i==0)
        if opts.resubmit:
            if AskUser(cmd):
                process = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
                output, err = process.communicate()

    #print
    # For-loop: All output txt files to be removed
    for i, f in enumerate(outList, 1):
        cmd = "rm -f %s" % (f)
        Print(es + cmd + ns, i==0)
        if opts.resubmit:
            if AskUser(cmd):
                process = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
                output, err = process.communicate()

    #print
    # For-loop: All log txt files to be removed
    for i, f in enumerate(logList, 1):
        cmd = "rm -f %s" % (f)
        Print(es + cmd + ns, i==0)
        if opts.resubmit:
            if AskUser(cmd):
                process = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
                output, err = process.communicate()
    return


def GetNumberOfJobs(dirName, fileName="run*.jdl"):

    # Define the command to be executed
    cmd     = "ls %s | wc -w" % ( os.path.join(os.getcwd(), dirName, fileName) )
    Verbose("Popen(%s, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)" % (cmd), True)
    process = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    output, err = process.communicate()
    if len(err) > 0:
        #raise Exception(es + err + ns)
        Verbose(es + err + ns)
        nJobs = 0
    else:
        nJobs = int(output.replace(" ", ""))
    return nJobs


def PrintSummaryTable(nTotal, nDone, nFilesEOS, nFail, nActive, nRun, nHeld, nIdle, nIO, condorQ, printSummary=True):

    Verbose("Fill the dictionaries with all the information retrieved", True)
    jobsDict = {}
    jobsDict["total"]     = str( nTotal )
    jobsDict["done"]      = str( nDone )
    jobsDict["eos"]       = str( nFilesEOS )
    jobsDict["fail"]      = str( nFail )
    jobsDict["active"]    = str( nActive )
    jobsDict["run"]       = str( nRun ) 
    jobsDict["idle"]      = str( nIdle )
    jobsDict["IO"]        = str( nIO ) #Input/Output
    jobsDict["held"]      = str( nHeld )

    # Create table
    table   = []
    align  = "{:^20} {:^20} {:^20} {:^20} {:^20} : {:^20} {:^20} {:^20} {:^20}"
    header = align.format(ns + "TOTAL" + ns, ss + "DONE" + ns, ss + "EOS" + ns, es + "FAIL" + ns, hs + "ACTIVE" + ns, ts + "RUN" + ns, ls + "HELD" + ns, cys + "I/O" + ns, ns + "IDLE" + ns )
    hLine  = "="*80
    table.append("{:^80}".format(opts.dirName))
    table.append(hLine)
    table.append(header)
    table.append(hLine)
    for k in jobsDict:
        table.append( align.format(ns + jobsDict["total"] + ns, ss + jobsDict["done"] + ns, ss + jobsDict["eos"] + ns, es + jobsDict["fail"] + ns, hs + jobsDict["active"] + ns, ts + jobsDict["run"] + ns, ls + jobsDict["held"] + ns, cys + jobsDict["IO"] + ns, ns + jobsDict["idle"] + ns ) )
        break
    table.append("\n")
    #table.append(hLine)

    # For-loop: All table rows
    for i, row in enumerate(table, 1):
        Print(row, i==1)

    return jobsDict, table


def GetFilesInEOS(eosdir):
    cmd = "eos root://cmseos.fnal.gov ls %s" % (eosdir)
    process = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    output, err = process.communicate()

    # Get list of contents 
    outputAll = output.splitlines()
    output = []

    # Remove anything not ending in ".tgz"
    for i, o in enumerate(outputAll, 1):
        # Is this a file?
        if o.endswith(".tgz") == False:
            #output.remove(o)
            continue

        # Does the file belong to this specific job?
        bSkip = False
        # For loop: All keywords
        for k in opts.keyList:
            if k not in o:
                bSkip = True
                break
            else:
                bSkip = False

        if bSkip: #opts.job not in o:
            #output.remove(o)
            #print "o = ", o
            continue
        else:
            Verbose("Appending file %s for retrieval" % (o), i==1)
            output.append(o)
        #print "%s (%s)" % (o, opts.job)

    
    # Separate into "Hplus2tbAnalysis" and "FakeBMeasurement"
    outputH2tb  = []
    outputFakeB = []
    for i, o in enumerate(output, 1):

        if "Hplus2tbAnalysis" in o:
            Verbose(hs + o + ns, i ==1)
            outputH2tb.append(o)

        if "FakeBMeasurement" in o:
            Verbose(ts + o + ns, i==1)
            outputFakeB.append(o)

    # If no results found
    if len(output) < 1:
        return [], [], []
    
    return output, outputH2tb, outputFakeB
    

def GetCondorQDict(username, keyword="Total for query: "):
    '''
    When executing:
    condor_q --submitter aattikis

    expect to see a line as follows:
    Total for query: 3 jobs; 0 completed, 0 removed, 0 idle, 3 running, 0 held, 0 suspended 

    this is the starting point forthis method
    '''

    # The "most -w" option will cause (or force) long lines to wrap instead of being truncated!
    # https://stackoverflow.com/questions/2159860/viewing-full-output-of-ps-command
    opts.job = opts.dirName.split("_Syst")[0] # see submitCondor.py to undertand why
    cmd      = "condor_q --submitter %s most -w" % (username)
    Verbose(cmd, True)

    # Calling subprocess.Popen() works but truncates output!
    process = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    output, err = process.communicate()
    if len(err) > 0:
        raise Exception(es + err + ns)

    # Define variables
    condorQ = {}
    lpc     = "None"

    # For-loop: All output lines
    for iLine, l in enumerate(output.splitlines(), True):
        
        # Definitions
        if "fnal.gov" in l:
            m = re.search('cmslpc(.+?).fnal.gov', l)
            if m:
                lpc = m.group(1)

        # Skip jobs unrelated to this task
        bSkipTask = False
        # For loop: All keywords
        for k in opts.keyList:
            if k not in l:
                bSkipTask = True
                break
            else:
                bSkipTask = False
            
        # Inspect only jobs related to this directory!
        if not bSkipTask: #opts.job in l:
            Verbose(es + l + ns, iLine==1)            
        
            # For command range
            nWords = len(l.split())-8
            cmd    = " ".join(l.split()[-nWords:])
                    
            # Crete/Fill dictionaries
            if len(condorQ) < 1:
                condorQ["ID"]         = [ l.split()[0] ]
                condorQ["OWNER"]      = [ l.split()[1] ]
                condorQ["SUBMITDATE"] = [ l.split()[2] ]
                condorQ["SUBMITTIME"] = [ l.split()[3] ]
                condorQ["RUNTIME"]    = [ l.split()[4] ]
                condorQ["STATUS"]     = [ l.split()[5] ]
                condorQ["PRI"]        = [ l.split()[6] ]
                condorQ["SIZE"]       = [ l.split()[7] ]
                condorQ["CMD"]        = [ cmd ] 
                condorQ["LPC"]        = [ lpc ] 
            else:
                condorQ["ID"].append(l.split()[0])
                condorQ["OWNER"].append(l.split()[1])
                condorQ["SUBMITDATE"].append(l.split()[2])
                condorQ["SUBMITTIME"].append(l.split()[3])
                condorQ["RUNTIME"].append(l.split()[4])
                condorQ["STATUS"].append(l.split()[5])
                condorQ["PRI"].append(l.split()[6])
                condorQ["SIZE"].append(l.split()[7])
                condorQ["CMD"].append( cmd )
                condorQ["LPC"].append( lpc )
                
    # For-loop: All keys
    if opts.verbose:
        for i, key in enumerate(condorQ.keys(), 1):
            Print("condorQ[%s] = %s" % (key, condorQ[key]), i==1)

    if len(condorQ.keys()) < 1:
        Verbose("No active jobs found!", True)
        return {}
        # raise Exception("Something went wrong and could not determing the jobs running, idle, held, etc..")
    else:
        return condorQ


def GetSystToOutputDict(filesList):
    '''
    The input file list (fList) contains all the
    output files of a given analysis (e.g. Hplus2tbAnalysis or
    FakeBMeasurement). But they are for all systematics considered

    This functions returns them in a dictionary so that:
    dict["Systematic"] = list-of-files-for-Systematic
    '''
    # Definitions
    filesDict  = {}
    systematic = None

    # For-loop: All files
    for i, f in enumerate(filesList, 1):

        m = re.search('_Syst(.+?)_', f)
        if m:
            systematic = m.group(1)
        else:
            raise Exception("Could not determine systematics type for file %s" % (f))

        # if key does not exist add it
        if systematic in filesDict.keys():
            filesDict[systematic].append(f)
        else:
            filesDict[systematic] = [f]
    return filesDict


def CheckForValidProxy():
    process = Popen(['voms-proxy-info'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = process.communicate()
    if len(err) > 0:
        raise Exception(es + err + ns)
        # err  = err.replace("\n", "")
        # err += " Continuing anyway (not needed)" 
        # Print(es + err + ns, True)
    else:
        lines = output.splitlines()
        for l in lines:
            if "timeleft" not in l:
                continue
            time  = l.split(": ")[-1]
            hours = int(time.split(":")[0])
            mins  = int(time.split(":")[1])
            secs  = int(time.split(":")[2])
            
            # Determine the time remaining in seconds
            dt = hours*60*60 + mins*60 + secs 
            
            # Require at least 60 seconds of valid proxy
            if dt < 60:
                raise Exception(es + "No valid CMS VO proxy found!" + ns)
            else:
                Print(ss + "Valid CMS VO proxy found!" + ns, True)
    return

def RetrieveUnpackCleanupFiles(filesSyst, analysis):

    # For-loop: All output files for given systematic
    for i, s in enumerate(filesSyst.keys(), 1):

        # Definitions
        nSyst = len(filesSyst.keys())
        sDir  = False            

        # For-loop: All output files for given systematic
        for j,  f in enumerate(filesSyst[s], 1):
                
            # Define stuff
            m = re.search('_Group(.+?)_', f)
            if m:
                datasetGroup = m.group(1)
            else:
                raise Exception("Could not determine datasets group for file %s" % (f))

            nFiles = len(filesSyst[s])
            if not sDir:
                date   = f.split("-")[-1].replace(".tgz", "")
                time   = f.split("Syst%s" % s)[-1].replace(".tgz", "")#.replace("-" + date, "")
                newDir = f.replace(time, "").replace(".tgz", "") + "_" + date
                newDir = newDir.replace("_Group%s" % datasetGroup, "")
                
            Verbose("Make new dir %s? Or does it already exist?"  % (newDir), True)
            if not os.path.isdir(newDir) and not sDir:
                os.mkdir(newDir)
                # Some jobs might finish at a different day. This causes 2 dirs for a given syst. this fixes it
                sDir = True
            else:
                Verbose(hs + "Dir %s already exists!" % (newDir) + ns, True)

            Verbose("Copy all tarballs under new dir", True)
            eosPath = os.path.join(opts.eosdir, f)
            cmd  = "xrdcp root://cmseos.fnal.gov:/%s %s/." % (eosPath, newDir )
            #msg  = "Copying file %d/%d, systematic %s %d/%d)" % ( j, nFiles, hs + s + ns, i, nSyst)
            msg  = "%s: Systematic %d/%d , File %d/%d" % (hs + analysis + ns, i, nSyst, j, nFiles)
            PrintFlushed(msg, j*i==1)
            process = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
            output, err = process.communicate()
            Verbose(cmd, True)
 
            Verbose("Unpack and subsequently remove the tarball", True)
            filePath = os.path.join(newDir, f)
            cmd = "tar xvzf %s --strip-components=1 -C %s && rm -f %s" % (filePath, newDir, filePath)
            process = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
            output, err = process.communicate()
            if len(err) > 0:
                raise Exception(es + err + ns)
            else:
                Verbose(cmd, True)

        Verbose("Now create the \"multicrab.cfg\" file", True)
        os.chdir(newDir)
        cmd = "find * -maxdepth 0 -type d | awk '{print \"[\"$1\"]\"}' > multicrab.cfg"
        process = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
        output, err = process.communicate()
        if len(err) > 0:
            raise Exception(es + err + ns)
        else:
            Verbose(cmd, True)                
            os.chdir("../")
    print
    return


def PrintCondorQ(condorQ):

    # Define variables
    nActive = 0
    nRun    = 0 
    nHeld   = 0
    nIdle   = 0
    nIO     = 0 # The arrow statuses mean the job is transferring input or output.
    table   = []
    align   = "{:>3} {:^10} {:^10} {:^10} {:^15} {:^10} {:^20} {:^10} {:^55}  {:^15}  {:^10}"
    header  = align.format("#", "LPC", "ID", "SUBMITTED", "RUNTIME", "STATUS", "ANALYSIS", "GROUP", "PSET", "POSTFIX", "DATE")
    hLine   = "="*180
    table.append("{:^180}".format(opts.dirName))
    table.append(hLine)
    table.append(header)
    table.append(hLine)

    # Sanity check
    if len(condorQ.values()) < 1:
        msg = "No active jobs found!"
        Print(es + msg + ns, True)
        return nActive, nRun, nHeld, nIdle, nIO

    # For-loop: All values for all keys
    nActive = len(condorQ["STATUS"])
    for i in range(0, nActive): #len(condorQ.values())-2):
        
        if opts.verbose:
            PrintFlushed("%d / %d" % (i+1, nActive), i==0)

        status = condorQ["STATUS"][i] 

        if status == "R":
            nRun += 1        
        elif status == "H":
            nHeld += 1
        elif status == "I":
            nIdle += 1
        elif "<" in status:
            # Each individual condor job will transfer files from NFS disk to the worker node before starting the job 
            nIO += 1
        else:
            raise Exception("Unexpected job STATUS = \"%s\"" % (condorQ["STATUS"][i]) )
    
        # Fill the table
        analysis = condorQ["CMD"][i].split()[1]
        pset     = condorQ["CMD"][i].split()[2]
        group    = condorQ["CMD"][i].split()[3]
        syst     = condorQ["CMD"][i].split()[3]
        postfix  = condorQ["CMD"][i].split()[5]
        date     = condorQ["CMD"][i].split()[6]
        table.append(align.format(i+1, condorQ["LPC"][i], condorQ["ID"][i], condorQ["SUBMITDATE"][i] + " " + condorQ["SUBMITTIME"][i], condorQ["RUNTIME"][i], condorQ["STATUS"][i], analysis, group, pset, postfix, date) )

        if i == (nActive-1):
            Verbose("", False)
    table.append(hLine)

    # For-loop: All rows
    for i, row in enumerate(table, 0):
        colour   = ns
        info     = row.split()
        nColumns = len(info)
        if nColumns >= 6:
            status = info[6]
        else:
            status = "?"

        if row == hLine:
            pass
        elif row == header:
            pass
        else:
            if status == "R":
                colour = ts
            elif "<" in status:
                colour = cys #hs
            elif "H" in status:
                colour = ls
            else:
                colour = ns
        Print(colour + row + ns, i==0)

    # Sanity Check:
    if nActive == (nRun + nHeld + nIdle + nIO):
        return  nActive, nRun, nHeld, nIdle, nIO
    else:
        raise Exception("Jobs don't add up!")


def main(opts):
    
    Verbose("Check that a CMS VO proxy exists (voms-proxy-init)", True)
    CheckForValidProxy()


    Verbose("Check that directory %s exists" % (opts.dirName), True)
    if os.path.isdir(opts.dirName):
        Verbose("Directory %s exists!" % (ss + opts.dirName + ns), True)
    else:
        Print("Directory %s does not exist! EXIT" % (es + opts.dirName + ns), True)
        os.mkdir(opts.dirName)
        sys.exit()

    # Determine total number of jobs (using jdl files)
    nRunH2tb  = GetNumberOfJobs(opts.dirName, "run_Hplus2tbAnalysis*.jdl")
    nRunFakeB = GetNumberOfJobs(opts.dirName, "run_FakeBMeasurement*.jdl")
    nRunTotal = GetNumberOfJobs(opts.dirName, "run*.jdl")
    Verbose("Found %s%d%s run files (Hplus2tbAnalysis=%d, FakeBMeasurement=%d)" % (ts, nRunTotal, ns, nRunH2tb, nRunFakeB), True) 


    # Determine total number of jobs (using output files)
    nOutputH2tb  = GetNumberOfJobs(opts.dirName, "output_Hplus2tbAnalysis*.txt")
    nOutputFakeB = GetNumberOfJobs(opts.dirName, "output_FakeBMeasurement*.txt")
    nOutputTotal = nOutputH2tb + nOutputFakeB
    Verbose("Found %s%d%s output files (Hplus2tbAnalysis=%d, FakeBMeasurement=%d)" % (ts, nOutputTotal, ns, nOutputH2tb, nOutputFakeB), False)


    # Determine total number of jobs (using error files)
    nErrorH2tb  = GetNumberOfJobs(opts.dirName, "error_Hplus2tbAnalysis*.txt")
    nErrorFakeB = GetNumberOfJobs(opts.dirName, "error_FakeBMeasurement*.txt")
    nErrorTotal = nErrorH2tb + nErrorFakeB
    Verbose("Found %s%d%s error files (Hplus2tbAnalysis=%d, FakeBMeasurement=%d)" % (ts, nErrorTotal, ns, nErrorH2tb, nErrorFakeB), False)
    

    # Determine total number of done jobs (using error files)
    nDoneH2tb  = 0
    nDoneFakeB = 0
    if nOutputH2tb > 0:
        nDoneH2tb  = GetNumberOfJobsWithKeyword(opts.dirName, "output_Hplus2tbAnalysis*.txt", "Results are in")
    if nOutputFakeB> 0:
        nDoneFakeB = GetNumberOfJobsWithKeyword(opts.dirName, "output_FakeBMeasurement*.txt", "Results are in")
    nDoneTotal = nDoneH2tb + nDoneFakeB
    Verbose("Found %s%d%s jobs done (Hplus2tbAnalysis=%d, FakeBMeasurement=%d)" % (ts, nDoneTotal, ns, nDoneH2tb, nDoneFakeB), False)


    # Determine total number of failed jobs (using error files)
    nFailH2tb  = 0
    nFailFakeB = 0
    if nErrorH2tb > 0:
        nFailH2tb  = GetNumberOfJobsWithKeyword(opts.dirName, "error_Hplus2tbAnalysis*.txt", "There was a crash.")
    if nErrorFakeB > 0:
        nFailFakeB = GetNumberOfJobsWithKeyword(opts.dirName, "error_FakeBMeasurement*.txt", "There was a crash.")
    nFailTotal = nFailH2tb + nFailFakeB
    Verbose("Found %s%d%s jobs failed (Hplus2tbAnalysis=%d, FakeBMeasurement=%d)" % (ts, nFailTotal, ns, nFailH2tb, nFailFakeB), False)


    Verbose("Create a job status summary table", True)
    condorQ  = GetCondorQDict(opts.userName)

    Verbose("Printing currently active jobs (from \"condor_q\" output)", True)
    nActive, nRun, nHeld, nIdle, nIO = PrintCondorQ(condorQ)


    Verbose("Determine number of output files in EOS", True)
    files, filesH2tb, filesFakeB = GetFilesInEOS(opts.eosdir)
    nFilesEOS = len(files)
    Verbose("Found %d files in %s (Hplus2tbAnalysis=%d, FakeBMeasurement=%d)" % (len(files), opts.eosdir, len(filesH2tb), len(filesFakeB)), True)


    Verbose("Get the jobs dictionary and the summary table", True)
    jobsDict, table = PrintSummaryTable(nRunTotal, nDoneTotal, nFilesEOS, nFailTotal, nActive, nRun, nHeld, nIdle, nIO, condorQ, printSummary=True)


    Verbose("Get the failed jobs", True)
    jdlList, errList, outList, logList, eosList = GetJobsWithKeyword(opts.dirName, analysis="Hplus2tbAnalysis", keyword="There was a crash.") 
    ResubmitFailedJobs(jdlList, errList, outList, logList, eosList)


    Verbose("Kill jobs", True)
    if opts.kill != None:
        KillJobs(condorQ, opts)
            

    jdlList_, errList_, outList_, logList_, eosList_ = GetJobsWithKeyword(opts.dirName, analysis="FakeBMeasurement", keyword="There was a crash.") 
    ResubmitFailedJobs(jdlList_, errList_, outList_, logList_, eosList_)

    if opts.getoutput:
        if nFailH2tb > 0 or nFailFakeB > 0:
            Print(es + "Not all jobs are in \"done\" mode. Aborting retrieval of output!" + ns, True)
            return

        if len(jobsDict["done"]) < 1:
            Print("No jobs in \"done\" mode found.", True)
        else:
            Verbose("Found %s jobs in %s state!" % (jobsDict["done"], ss + "DONE" + ns), True)
            
        Verbose("Get mapping of systematic->fileList", True)
        filesSystH2tb  = GetSystToOutputDict(filesH2tb)
        filesSystFakeB = GetSystToOutputDict(filesFakeB)

        RetrieveUnpackCleanupFiles(filesSystH2tb, "Hplus2tbAnalysis")
        RetrieveUnpackCleanupFiles(filesSystFakeB, "FakeBMeasurement")

    print
    Print("Done", True)
    return


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

    # Default settings
    VERBOSE   = False
    DIRNAME   = None
    USERNAME  = None
    GETOUTPUT = False
    EOSDIR    = "$CONDOR"
    RESUBMIT  = False
    KILL      = None

    # Define the available script options
    parser = OptionParser(usage="Usage: %prog [options]", add_help_option=True, conflict_handler="resolve")

    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=VERBOSE, 
                      help="Enables verbose mode (for debugging purposes) [default: %s]" % VERBOSE)

    parser.add_option("-d", "--dirName", dest="dirName", action="store", default = DIRNAME,
                      help="Name of directory to be checked for status [default: %s]" % (DIRNAME) )

    parser.add_option("-u", "--userName", dest="userName", action="store", default = USERNAME,
                      help="User name (FNAL account) to be used for condor commands [default: %s]" % (USERNAME) )

    parser.add_option("-g", "--getoutput", dest="getoutput", action="store_true", default = GETOUTPUT,
                      help="Retrieve output from EOS? [default: %s]" % (GETOUTPUT) )

    parser.add_option("--resubmit", dest="resubmit", action="store_true", default=RESUBMIT, 
                      help="Resubmit and clean-up all failed jobs automatically? [default: %s]" % RESUBMIT)

    parser.add_option("--eosdir", dest="eosdir", action="store", default = EOSDIR,
                      help="Location of CONDOR output files in EOS? [default: %s]" % (EOSDIR) )

    parser.add_option("--kill", dest="kill", action="store", default = KILL,
                      help="List of jobs id's to kill (comma separated) [default: %s]" % (KILL) )

    (opts, parseArgs) = parser.parse_args()

    # Sanity checks
    if opts.dirName == None:
        Print("Please provide a directory as argument (-d or --dirName option). EXIT!", True)
        sys.exit()

    if not os.path.isdir(opts.dirName):
        Print("The directory %s does not exist. EXIT!" % (opts.dirName), True)
        sys.exit()


    if opts.userName == None:
        opts.userName = getpass.getuser()

    # Inform user of compatibility issues
    pyV1  =  sys.version_info[0] 
    pyV2  =  sys.version_info[1] 
    pyV3  =  sys.version_info[2] 
    pyVer = "%d.%d.%d" % (pyV1, pyV2, pyV3)
    
    if pyV2 < 7 or pyV3 < 6:
        Print("Requires %sPython 2.7.6%s or later (using %sPython %s). EXIT!" % (hs, ns, es, pyVer + ns), True)
        sys.exit()
    else:
        Print("Requires %sPython 2.7.6%s or later (using %sPython %s)" % (hs, ns, ss, pyVer + ns), True)

    # Retrieve info from dirName
    myPattern = r"(?P<TopMassLE>\w+)_(?P<BDT>\w+)_(?P<Binning>\w+)_(?P<Group>\w+)_(?P<Syst>\S+)"
    reObject = re.compile(myPattern)
    search = reObject.search(opts.dirName)

    if search == None:
        msg = "The directory name does not have the expected naming structure of TopMassLE<?>_BDT<?>_Binning<?>Eta<?>Pt_<?>_Date. Consider renaming it!"
        raise Exception(es + msg + ns)
    
    if search.group(0) != opts.dirName:
        msg = "The directory name does not match the group(0) of the regular expression search! It should!"
        raise Exception(es + msg + ns)
    opts.topMass = search.group(1)
    opts.BDT     = search.group(2)
    opts.binning = search.group(3)
    opts.postfix = search.group(4)
    opts.date    = search.group(5)
    opts.keyList = [opts.topMass, opts.BDT, opts.binning, opts.postfix, opts.date]
    Verbose("topMass = %s, BDT = %s, binning = %s, postfix = %s, date = %s" % (opts.topMass, opts.BDT, opts.binning, opts.postfix, opts.date), True)
    
    # Call the main function
    main(opts)
