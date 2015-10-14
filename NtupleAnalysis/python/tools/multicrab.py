## \package multicrab
# Python interface for multicrab, also the default SE black list
#
# The functionality is divided to
# \li creating (multi)crab tasks (also multicrabDataset package)
# \li querying the status of crab jobs (via hplusMultiCrabStatus.py)
#
# <b>The documentation below is now outdated, update is still to be written.</b>
#
# The motivation for having all this trouble with creating the crab
# tasks is that managing hundreds of datasets/crab tasks (one crab
# task per dataset with an entry in DBS) with plain multicrab.cfg
# files requires a lot of manual copy-pasting and is thus error prone.
# And yes, the number of datasets to manage is indeed in hundreds
# (PromptReco and ReRecos for data, production campaigns for MC;
# orthogonally the AOD version, various pattuple versions, tau
# embedding skims, tau embedding embedded datasets etc.).
#
# Writing the dataset definitions to a data structure which can be
# queried easily (multicrabDataset.datasets), and few classes to
# provide nice interface to the user (multicrab.Multicrab,
# multicrab.MulticrabDataset) makes it easy to write scripts for
# creating multicrab jobs such that (see e.g.
# test/multicrabSignalAnalysis.py, test/pattuple/multicrabPatTuple.py,
# test/tauEmbedding/multicrabTauEmbedding.py)
# \li selecting only some datasets is a matter of (un)commenting one line per dataset
# \li switching pattuple versions is a matter of changing value of one variable (i.e. one line change)
# \li switching from pattuple to AOD with PAT-on-the-fly is a matter of chaning value of one variable
# \li switching data processing era (for data datasets, PU reweighting factors, trigger efficiencies) is a matter of changing value of one variable
#
# The dataset definition structure is as follows
# \code
# datasets = {
#     # Example of data dataset with a single trigger
#     "Tau_165088-165633_Prompt": { # Name of the dataset
#         "dataVersion": "42Xdata", # Data version string 
#         "trigger": "HLT_IsoPFTau35_Trk20_MET45_v6", # Trigger to be applied (optional)
#         "runs": (165088, 165633), # Inclusive range of runs for this dataset
#         "data": { # Section for various dataInput versions
#             "AOD": { # Name of dataInput
#                 "datasetpath": "/Tau/Run2011A-PromptReco-v4/AOD", # DBS path
#                 "number_of_jobs": 200, # (Default) number of jobs to create for a task processing this dataset
#                 "lumiMask": "PromptReco" # Lumi mask name
#             },
#             "pattuple_v18": {
#                 "dbs_url": common.pattuple_dbs, # DBS reader URL, if dataset is published in some other DBS instance than the global DBS
#                 "datasetpath": "/Tau/local-Run2011A_PromptReco_v4_AOD_165088_pattuple_v18-68faa0f802ec7fdcb65798edde8320e0/USER",
#                 "luminosity": 138.377000, # Integrated luminosity of a dataset in pb^-1 (optional)
#                 "number_of_jobs": 2,
#             },
#             "pattuple_v19": {
#                 "dbs_url": common.pattuple_dbs,
#                 "datasetpath": "/Tau/local-Run2011A_PromptReco_v4_AOD_165088_pattuple_v19-3bb41d427869a8c545d9fa20bdb93436/USER",
#                 "number_of_jobs": 2,
#             },
#         }
#     },
#     # Example of data dataset with OR of many triggers
#     "SingleMu_165088-165633_Prompt": {
#         "dataVersion": "42Xdata",
#         "args": {"doTauHLTMatching": 0}, # Additional command line arguments
#         "triggerOR": [ # List of triggers whose OR is to be applied (optional)
#             "HLT_Mu30_v3", "HLT_IsoMu17_v8",
#             "HLT_Mu15_v4", "HLT_Mu20_v3", "HLT_Mu24_v3", "HLT_IsoMu15_v8",
#             ],
#         "runs": (165088, 165633),
#         "data": {
#             "AOD": {
#                 "datasetpath": "/SingleMu/Run2011A-PromptReco-v4/AOD",
#                 "number_of_jobs": 490,
#                 "lumiMask": "PromptReco"
#             },
#             "pattuple_v19": {
#                 "dbs_url": common.pattuple_dbs,
#                 "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_165088_pattuple_v19b-a96d8be905ea05d746e188c63f686c22/USER",
#                 "luminosity": 139.078000,
#                 "number_of_jobs": 10
#             },
#         }
#     },
#     # Example of MC dataset
#     "W3Jets_TuneZ2_Summer11": {
#         "dataVersion": "42XmcS4",
#         "crossSection": 304.2*31314/27770.0, # Cross section in pb. Demonstrates also that all values in given here can be python expressions
#         "data": {
#             "AOD": {
#                 "datasetpath": "/W3Jets_TuneZ2_7TeV-madgraph-tauola/Summer11-PU_S4_START42_V11-v1/AODSIM",
#                 "number_of_jobs": 490,
#             },
#             "pattuple_v18": {
#                 "dbs_url": common.pattuple_dbs,
#                 "datasetpath": "/W3Jets_TuneZ2_7TeV-madgraph-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_pattuple_v18_1-5c1fe2e0ac511ee6db9df3b7fb33ca32/USER",
#                 "number_of_jobs": 16
#             },
#         },
#     },
# }
# \endcode
# \li <i>Dataset name</i> translates to [name] section in
#     multicrab.cfg, and thus becomes the task directory name.
# \li <i>Data version</i> should be one defined in
#     <tt>python/HChDataVersion.py</tt>. Data version affects to
#     Global Tag and default input files. E.g. JEC levels and
#     pattuple-time event selection depends whether dataset is data or
#     MC. There can be also some customisations which depend on the
#     CMSSW version of the data.
# \li <i>Trigger</i> can be specified either with \a trigger or \a
#     triggerOR (mutually exclusive; either one is required for data,
#     for MC trigger is not used). With \a trigger, a single HLT path
#     should be specified, events are required to pass the path. With
#     \a triggerOR, a list of HLT paths should be specified, events
#     are required to pass any of the specified paths.
# \li <i>Run range</i> If \a lumiMask is given, process only the runs
#     in this range. If \a lumiMask is not given, run range has no
#     effect
# \li <i>DataInput</i> (better name, anyone?) specifies various
#     "versions" of the dataset which can be an input to crab jobs.
#     Usually one of the entries is "AOD", which corresponds the
#     AOD(SIM) dataset centrally produced by CMS. There can be one or
#     more pattuple versions produced by us.
# \li <i>Lumi mask</i> Shorthand name for a JSON file, specified in
#     <tt>python/tools/certifiedLumi.py</i>. The JSON files are
#     assumed to exist in <tt>test</tt> directory.
# \li <i>Integrated luminosity</i> is purely informative, and is not
#     used in processing workflow in any way (the recommendation is to
#     always calculate the luminosity after processing data). Can be
#     useful to detect inconsitenties in the amount of data really
#     processed (e.g. if some file was skipped)
# \li <i>Additional command line arguments</i> can be given. These are
#     appended to <i>CMSSW.pycfg_params</i> list in multicrab.cfg for
#     this dataset, and where they are then delivered to
#     <i>sys.argv</i> of the python configuration file.
# \li <i>Cross section</i> is mandatory for MC datasets. It is
#     forwarded to python configuration, which in turns forwards it to
#     <tt>configInfo/configinfo</tt> histogram in the resulting
#     histograms.root file. The value provides a default value for the
#     cross section of the dataset.
#
# \todo The current structure of dataset definitions provides almost
# no support for workflows with different skims (e.g. tau+MET trigger
# + jets for signal pattuples, muon+jets for embedding, muon+tau for
# trigger efficiency). Although the variety can probably be managed by
# overriding some of the definition parameters in the multicrab
# configuration scripts, I think having the support for multiple
# workflows with different skims (and numbers of jobs for same input
# dataset, e.g. AOD) already in the dataset definitions would provide
# additional documentation.
import os, re
import sys
import subprocess, errno
import time
import math
import glob
import shutil
import select
import ConfigParser
import OrderedDict

#import multicrabWorkflows
#import certifiedLumi
#import git
#import aux
import tarfile

### Default Storage Element (SE) black list for non-stageout jobs
#defaultSeBlacklist_noStageout = [
##    "ucl.ac.be", # Jobs end up in queuing, lot's of file open errors, added 2011-09-02, commented 2012-09-28
##    "iihe.ac.be", # Problematic site with server, long queue, added, 2011-09-26, commented 2012-09-28
##    "unl.edu", # Jobs can wait in queues for a looong time, added 2011-10-24, commented 2012-10-26
##    "mit.edu", # MIT has some problems? added 2011-12-02, commented 2012-09-28
    #"kbfi.ee", # Files are not found, added 2012-09-28
    #"cscs.ch", # Files are not found, added 2012-09-28
##    "roma1.infn.it", # Jobs don't finish, added 2012-10-26, commented 2013-02-25
    #"kiae.ru", # Jobs fail by some missing grid libraries, added 2013-02-20
    #]

### Default Storage Element (SE) black list for stageout jobs
#defaultSeBlacklist_stageout = [
    #"colorado.edu", # Ultraslow bandwidth, no chance to get even the smaller pattuples through, added 2011-06-16
    #"T3_*", # Don't submit to T3's, added 2011-10-24
    #"T2_UK_London_Brunel", # Noticeable fraction of submitted jobs fail due to stageout errors, added 2011-09-02
##    "T2_US_Florida", # In practice gives low bandwidth to T2_FI_HIP => stageouts timeout, also jobs can queue long times, added 2011-09-02, commented 2012-11-06 (long queues still apply, but remoteGlidein helps)
##    "wisc.edu", # Stageout failures, added 2011-10-24, commented 2012-09-28 
##    "ingrid.pt", # Stageout failures, added 2011-10-26, commented 2011-12-02
##    "ucsd.edu", # Stageout failures, added 2011-10-26, commented 2012-11-19
##    "pi.infn.it", # Stageout failures, added 2011-10-26, commented 2012-11-19
##    "lnl.infn.it", # Stageout failures, added 2011-12-02, commented 2013-02-25
##    "mit.edu", # MIT has some problems? added 2011-12-02, commented 2012-09-28
    #"sprace.org.br", # Stageout failures. added 2011-12-02
    #"knu.ac.kr", # Stageout failures, added 2011-12-02
##    "T2_US_*", # disable US because of low bandwidth, added 2012-04-04, commented 2012-09-28
    #]

### Default Storage Element (SE) black list for backward compatibility
#defaultSeBlacklist = defaultSeBlacklist_noStageout + defaultSeBlacklist_stageout

## Returns the list of CRAB task directories from a MultiCRAB configuration.
# 
# \param opts      If this object contains 'dirs' attribute, the content of it
#                  is returned instead. The use case is that one can give
#                  e.g. OptionParser object, whose 'dirs' option is
#                  optional, to override the default behaviour of reading
#                  the configuration file.
# \param filename  Path to the multicrab.cfg file (default: 'multicrab.cfg')
# \param directory Path to \a filename, allows specifying only the
#                  directory of the default \a filename (default: '')
# 
# The order of the task names is the same as they are in the
# configuration file.
def getTaskDirectories(opts, filename="multicrab.cfg", directory=""):
    if hasattr(opts, "dirs") and len(opts.dirs) > 0:
        ret = []
        for d in opts.dirs:
            if d[-1] == "/":
                ret.append(d[0:-1])
            else:
                ret.append(d)
        return ret
    else:
        fname = os.path.join(directory, filename)
        if os.path.exists(fname):
            taskNames = _getTaskDirectories_crab2(fname)
            dirname = os.path.dirname(fname)
            taskNames = [os.path.join(dirname, task) for task in taskNames]
        else:
            taskNames = _getTaskDirectories_crab3(directory)

        def filt(dir):
            if opts.filter in dir:
                return True
            return False
        if opts != None:
            if opts.filter != "":
                taskNames = filter(filt, taskNames)
            if len(opts.skip) > 0:
                for skip in opts.skip:
                    taskNames = filter(lambda n: skip not in n, taskNames)

        return taskNames

def _getTaskDirectories_crab2(filename):
    if not os.path.exists(filename):
        raise Exception("Multicrab configuration file '%s' does not exist" % filename)

    mc_ignore = ["MULTICRAB", "COMMON"]
    mc_parser = ConfigParser.ConfigParser(dict_type=OrderedDict.OrderedDict)
    mc_parser.read(filename)

    sections = mc_parser.sections()

    for i in mc_ignore:
        try:
            sections.remove(i)
        except ValueError:
            pass

    return sections

def _getTaskDirectories_crab3(directory):
#    dirs = glob.glob(os.path.join(directory, "crab_*"))
    dirs = glob.glob(os.path.join(directory, "*")) #fixme
    dirs = filter(lambda d: os.path.isdir(d), dirs)
    return dirs

## Add common MultiCRAB options to OptionParser object.
#
# \param parser  optparse.OptionParser object
def addOptions(parser):
    parser.add_option("--dir", "-d", dest="dirs", type="string", action="append", default=[],
                      help="CRAB task directory to have the files to merge (default: read multicrab.cfg and use the sections in it)")
    parser.add_option("--filter", dest="filter", type="string", default="",
                      help="When reading CRAB tasks from multicrab.cfg, take only tasks whose names contain this string")
    parser.add_option("--skip", dest="skip", type="string", action="append", default=[],
                      help="When reading CRAB tasks from multicrab.cfg, skip tasks containing this string (can be given multiple times)")

## Raise OSError if 'crab' command is not found in $PATH.
def checkCrabInPath():
    try:
        retcode = subprocess.call(["crab"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except OSError, e:
        if e.errno == errno.ENOENT:
            raise Exception("crab executable not found in $PATH. Is the crab environment loaded?")
        else:
            raise e

### Create 'standard' multicrab task directory and return the name of it.
##
## \param prefix   Prefix string to the directory (before timestamp)
## \param postfix  Postfix string to the directory (after timestamp)
## \param path     Path to a directory where to create the multicrab
##                 directory (if None, crete to working directory)
#def createTaskDir(prefix="multicrab", postfix="", path=None):
    #while True:
        #dirname = prefix+"_" + time.strftime("%y%m%d_%H%M%S")
        #if len(postfix) > 0:
            #dirname += "_" + postfix
        #if path != None:
            #dirname = os.path.join(path, dirname)
        #if os.path.exists(dirname):
            #time.sleep(1)
            #continue

        #os.makedirs(dirname)
        #break
    #return dirname

def crabCfgTemplate(scheduler="arc", return_data=None, copy_data=None, crabLines=[], cmsswLines=[], userLines=[], gridLines=[]):
    if return_data is None and copy_data is None:
        raise Exception("You must give either return_data or copy_data, you gave neither")
    if return_data is not None and copy_data is not None:
        raise Exception("You must give either return_data or copy_data, you gave both")
    if copy_data is not None:
        return_data = not copy_data
    if return_data:
        r = 1
        c = 0
    else:
        r = 0
        c = 1

    lines = [
        "[CRAB]",
        "jobtype = cmssw",
        "scheduler = %s" % scheduler,
        ]
    lines.extend(crabLines)
    if len(cmsswLines) > 0:
        lines.extend(["",
                      "[CMSSW]",
                      "use_dbs3 = 1"
                      ])
        lines.extend(cmsswLines)
    lines.extend([
        "",
        "[USER]",
        "return_data = %d" % r,
        "copy_data = %d" % c,
        ])
    lines.extend(userLines)
    lines.extend([
        "",
        "[GRID]",
        "virtual_organization = cms"
        ])
    lines.extend(gridLines)

    return "\n".join(lines)

## Write git version information to a directory
#
# \param dirname  Path to multicrab directory
def writeGitVersion(dirname):
    version = git.getCommitId()
    if version != None:
        f = open(os.path.join(dirname, "codeVersion.txt"), "w")
        f.write(version+"\n")
        f.close()
        f = open(os.path.join(dirname, "codeStatus.txt"), "w")
        f.write(git.getStatus()+"\n")
        f.close()
        f = open(os.path.join(dirname, "codeDiff.txt"), "w")
        f.write(git.getDiff()+"\n")
        f.close()

### Print all multicrab datasets
##
## \param details   Forwarded to multicrabWorkflows.printAllDatasets()
#def printAllDatasets(details=False):
    #multicrabWorkflows.printAllDatasets(details)

### Select runs [runMin, runMax] from lumiList.
## 
## lumiList is assumed to be FWCore.PythonUtilities.LumiList.LumiList
## object.
## 
## \return the modified LumiList object.
#def filterRuns(lumiList, runMin, runMax):
    ## From FWCore/PythonUtilities/scripts/filterJSON.py
    #runsToRemove = []
    #allRuns = lumiList.getRuns()
    #for run in allRuns:
        #if runMin != None and int(run) < runMin:
            #runsToRemove.append (run)
        #if runMax != None and int(run) > runMax:
            #runsToRemove.append (run)

    #lumiList.removeRuns(runsToRemove)
    #return lumiList

### Exception for non-succesful crab job exit codes
class ExitCodeException(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message

### Given crab job stdout file, ensure that the job succeeded
##
## \param stdoutFile   Path to crab job stdout file
## \param allowJobExitCodes  Consider jobs with these non-zero exit codes to be succeeded
##
## If any of the checks fail, raises multicrab.ExitCodeException
def assertJobSucceeded(stdoutFile, allowJobExitCodes=[]):
##    re_exe = re.compile("ExeExitCode=(?P<code>\d+)")
    re_exe = re.compile("process\s+id\s+is\s+\d+\s+status\s+is\s+(?P<code>\d+)")
    re_job = re.compile("JobExitCode=(?P<code>\d+)")

    exeExitCode = None
    jobExitCode = None
    if tarfile.is_tarfile(stdoutFile):
        fIN = tarfile.open(stdoutFile)
        log_re = re.compile("cmsRun-stdout-(?P<job>\d+)\.log")
        for member in fIN.getmembers():
            f = fIN.extractfile(member)
            match = log_re.search(f.name)
            if match:
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
    jobExitCode = exeExitCode
    if exeExitCode == None:
        raise ExitCodeException("No exeExitCode")
    if jobExitCode == None:
        raise ExitCodeException("No jobExitCode")
    if exeExitCode != 0:
        raise ExitCodeException("Executable exit code is %d" % exeExitCode)
    if jobExitCode != 0 and not jobExitCode in allowJobExitCodes:
        raise ExitCodeException("Job exit code is %d" % jobExitCode)

## Compact job number list
#
# \param jobnums  List of job numbers (as integers)
#
# \return String of compacted job number list
def prettyJobnums(jobnums):
    ret = []

    stack = []
    for i in range(0, len(jobnums)):
        if len(stack) == 0:
            stack.append(jobnums[i])
        elif len(stack) == 1:
            if stack[-1] != jobnums[i]-1:
                num = stack.pop()
                ret.append(str(num))
            stack.append(jobnums[i])
        else:
            if stack[-1] == jobnums[i]-1:
                stack.pop()
            else:
                end = stack.pop()
                begin = stack.pop()
                if begin == end-1:
                    ret.append("%d,%d" % (begin, end))
                else:
                    ret.append("%d-%d" % (begin, end))
            stack.append(jobnums[i])
    if len(stack) == 1:
        ret.append(str(stack.pop()))
    elif len(stack) == 2:
        end = stack.pop()
        begin = stack.pop()
        if begin == end-1:
            ret.append("%d,%d" % (begin, end))
        else:
            ret.append("%d-%d" % (begin, end))
    elif len(stack) != 0:
        raise Exception("Internal error: stack size is %d, content is %s" % (len(stack), str(stack)), "pretty_jobnums")

    return ",".join(ret)

## Transform pretty job number string to list of job numbers
#
# \param prettyString   String for pretty job number list (of the form '1,2,3-6,9')
#
# \return List of ints for job numbers
def prettyToJobList(prettyString):
    commaSeparated = prettyString.split(",")
    ret = []
    for item in commaSeparated:
        if "-" in item:
            if item.count("-") != 1:
                raise Exception("Item '%s' has more than 1 occurrances of '-', in string '%s'" % (item, prettyString))
            (first, last) = item.split("-")
            ret.extend(range(int(first), int(last)+1))
        else:
            ret.append(int(item))

    return ret


## Get output of 'crab -status' of one CRAB task
#
# \param task      CRAB task directory name
# \param printCrab Print CRAB output
#
# \return Output (stdout+stderr) as a string
def crabStatusOutput(task, printCrab):
    if False: # debugging
        out = open("crabOutput-%s.txt" % time.strftime("%y%m%d_%H%M%S"), "w")
    else:
        out = None

    command = ["crab", "-status", "-c", task]
    #p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) # doesn't solve
    #p = subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=100*1024) # doesn't solve
    p = subprocess.Popen(command, stdout=subprocess.PIPE)
    output = ""
    # The process may finish between p.poll() and p.stdout.readline()
    # http://stackoverflow.com/questions/10756383/timeout-on-subprocess-readline-in-python
    # Try first just using select for polling if p.stdout has anything
    # If that doesn't work out, add the timeout (currently in comments)
    poll_obj = select.poll()
    poll_obj.register(p.stdout, select.POLLIN)
        #last_print_time = time.time()
        #timeout = 600 # 10 min timeout initially, -status can take long
#        while p.poll() == None:# and (time.time() - last_print_time) < timeout:
#                    if "Log file is" in line:
#                        # The last line in the output starts with this, shorten the timeout to 10 s
#                        timeout = 10
#                        print "Last line encountered, shortening timeout to 10 s"
#                last_print_time = time.time()

    while True:
        exit_result = p.poll()
        while True:
            poll_result = poll_obj.poll(0) # poll timeout is 0 ms
            if poll_result:
                line = p.stdout.readline()
                if line:
                    if printCrab:
                        print line.strip("\n")
                    if out is not None:
                        out.write(line)
                    output += line
                else:
                    break
            else: # if nothing to read, continue to check if the process has finished
                break
        if exit_result is None:
            time.sleep(1)
        else:
            break

    if out is not None:
        out.close()
#    print "Out of poll loop, return code", p.returncode
    if p.returncode != 0:
        if printCrab:
            raise Exception("Command '%s' failed with exit code %d" % (" ".join(command), p.returncode))
        else:
            raise Exception("Command '%s' failed with exit code %d, output:\n%s" % (" ".join(command), p.returncode, output))
    return output

## Exception for something being wrong in the crab output
class CrabOutputException(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)

## Transform 'crab -status' output to list of multicrab.CrabJob objects
#
# \param task    CRAB task directory
# \param output  Output from 'crab -status', e.g. from multicrab.crabStatusOutput()
#
# \return List of multicrab.CrabJob objects
def crabOutputToJobs(task, output):
    status_re = re.compile("(?P<id>\d+)\s+(?P<end>\S)\s+(?P<status>\S+)(\s+\(.*?\))?\s+(?P<action>\S+)\s+(?P<execode>\S+)?\s+(?P<jobcode>\S+)?\s+(?P<host>\S+)?")
    total_re = re.compile("crab:\s+(?P<njobs>\d+)\s+Total\s+Jobs")
    jobs = {}
    njobs = 0
    total = None
    for line in output.split("\n"):
        m = status_re.search(line)
        if m:
            job = CrabJob(task, m)
            aux.addToDictList(jobs, job.status, job)
            njobs += 1
            continue
        m = total_re.search(line)
        if m:
            total = int(m.group("njobs"))

    if total is None:
        raise CrabOutputException("Did not find total number of jobs from the crab output")
    if total != njobs:
        raise CrabOutputException("Crab says total number of jobs is %d, but only %d was found from the input" % (total, njobs))
    return jobs

## Convert argument to int if it is not None
def _intIfNotNone(n):
    if n == None:
        return n
    return int(n)

## Run 'crab -status' and create multicrab.CrabJob objects
#
# \param task  CRAB task directory
# \param printCrab Print CRAB output
#
# \return List of multicrab.CrabJob objects
def crabStatusToJobs(task, printCrab):
    # For some reason in lxplus sometimes the crab output is
    # garbled. In case of value errors try 4 times.
    maxTrials = 4
    for i in xrange(0, maxTrials):
        try:
            output = crabStatusOutput(task, printCrab)
            return crabOutputToJobs(task, output)
        except ValueError, e:
            if i == maxTrials-1:
                raise e
            print >>sys.stderr, "%s: Got garbled output from 'crab -status' (parse error), trying again" % task
        except CrabOutputException, e:
            if i == maxTrials-1:
                raise e
            print >>sys.stderr, "%s: Got garbled output from 'crab -status' (mismatch in number of jobs), trying again" % task

    raise Exception("Assetion, this line should never be reached")

## Class for containing the information of finished CRAB job
class CrabJob:
    ## Constructor
    #
    # \param task   CRAB task directory
    # \param match  Regex match object from multicrab.crabOutputToJobs() function
    def __init__(self, task, match):
        self.task = task
        self.id = int(match.group("id"))
        self.end = match.group("end")
        self.status = match.group("status")
        self.origStatus = self.status[:]
        self.action = match.group("action")

        if self.status == "Cancelled":
            self.exeExitCode = None
            self.jobExitCode = None
        else:
            self.exeExitCode = _intIfNotNone(match.group("execode"))
            self.jobExitCode = _intIfNotNone(match.group("jobcode"))
        self.host = match.group("host")

        if self.jobExitCode != None and self.jobExitCode != 0:
            self.status += " (%d)" % self.jobExitCode
        elif self.exeExitCode != None and self.exeExitCode != 0:
            self.status += " (exe %d)" % self.exeExitCode
#        if self.status == "Retrieved":
#            try:
#                multicrab.assertJobSucceeded(self.stdoutFile())
#            except multicrab.ExitCodeException:
#                self.status += "(malformed stdout)"
#                self.jobExitCode = -1
#                self.exeExitCode = -1
        

    ## Get path to the job stdout file
    def stdoutFile(self):
        return os.path.join(self.task, "res", "CMSSW_%d.stdout"%self.id)

    ## Check if job has failed
    #
    # \param status  "all", "aborted", or "done". 
    #
    # \return True, if job has failed, False, if job has succeedded
    #
    # Job can fail either before it has started to run (by grid,
    # "aborted"), or after it has started to run (site/software
    # problem, "done". With \a status parameter, one can control if
    # one want's to check the status of aborted jobs only, done jobs
    # only, or both. Use case is the resubmission of aborted-only,
    # done-only, or all failed jobs.
    def failed(self, status):
        if (status == "all" or status == "aborted") and self.origStatus == "Aborted":
            return True
        if status == "done" and self.origStatus == "Done":
            return True
        if self.origStatus != "Retrieved":
            return False
        if self.exeExitCode == 0 and self.jobExitCode == 0:
            return False

        if status == "all":
            return True
        if status == "aborted":
            return False
        if self.jobExitCode in status:
            return True
        return False

### Abstraction of a dataset for multicrab.cfg generation
##
## Dataset definitions are taken from multicrabWorkflows.datasets list.
#class MulticrabDataset:
    ### Constructor.
    ## 
    ## \param name         Name of the dataset (i.e. dataset goes to [name] section
    ##                     in multicrab.cfg.
    ## \param workflow     String for workflow name, technically a key to a
    ##                     Workflow object in the datasets list.
    ## \param lumiMaskDir  Directory where lumi mask (aka JSON) files are
    ##                     (can be absolute or relative to the working directory)
    ## 
    ## The constructor fetches the dataset configuration from
    ## multicrabWorkflows module. It makes some sanity checks for the
    ## configuration, and also filters the runs of the lumi mask if
    ## a run range is explicitly given.
    #def __init__(self, name, workflow, lumiMaskDir):
        #self.args = ["runOnCrab=1"]
        #self.lines = []
        #self.generatedFiles = []
        #self.filesToCopy = []
        #self.data = {} # dictionary for those options for which it didn't make sense to change (at least yet)

        #self.blackWhiteListParams = ["ce_white_list", "se_white_list", "ce_black_list", "se_black_list"]

        #self.dataset = multicrabWorkflows.datasets.getDataset(name)

        #self.workflow = self.dataset.getWorkflow(workflow)
        #self.inputData = self.workflow.source.getData()
        #if self.inputData.hasLumiMask():
            #lumiMaskFile = os.path.join(lumiMaskDir, self.inputData.getLumiMaskFile())
            #print "Using lumi file", lumiMaskFile
            #if self.dataset.hasRuns():
                #from FWCore.PythonUtilities.LumiList import LumiList

                #(runMin, runMax) = self.dataset.getRuns()
                #lumiList = filterRuns(LumiList(filename=lumiMaskFile), runMin, runMax)

                #info = "_runs_%s_%s" % (str(runMin), str(runMax))

                #ext_re = re.compile("(\.[^.]+)$")
                #lumiMaskFile = ext_re.sub(info+"\g<1>", os.path.basename(lumiMaskFile))
                #self.generatedFiles.append( (lumiMaskFile, str(lumiList)) )
                #self.inputData.setLumiMaskFile(lumiMaskFile)
            #else:
                #self.filesToCopy.append(lumiMaskFile)

    ### Is the dataset data?
    #def isData(self):
        #return self.dataset.isData()

    ### Is the dataset MC?
    #def isMC(self):
        #return not self.dataset.isMC()

    ### Get the dataset name
    #def getName(self):
        #return self.dataset.getName()

    ### Get the dataset DBS path of the source
    #def getDatasetPath(self):
        #return self.inputData.getDatasetPath()

    ### Set the number of CRAB jobs for this dataset
    ##
    ## \param njobs   Number of jobs
    #def setNumberOfJobs(self, njobs):
        #self.inputData.number_of_jobs = int(njobs)
        #self.inputData._ensureConsistency()

    #def getNumberOfJobs(self):
        #return self.inputData.number_of_jobs

    ### Modify number of jobs with a function.
    ## 
    ## \param func   Function
    ##
    ## The function gets the original number of jobs as an argument,
    ## and the function should return a number for the new number of
    ## jobs.
    ## 
    ## Example
    ## \code
    ## obj.modifyNumberOfJobs(lambda n: 2*n)
    ## \endcode
    #def modifyNumberOfJobs(self, func):
        #self.inputData.number_of_jobs = int(func(self.inputData.number_of_jobs))
        #self.inputData._ensureConsistency()

    ### Set number lumi sections per CRAB job
    #def setLumisPerJob(self, nlumis):
        #self.inputData.lumis_per_job = int(nlumis)
        #self.inputData._ensureConsistency()

    ### Modify number of lumis per job with a function.
    ## 
    ## \param func   Function
    ##
    ## The function gets the original number of lumis as an argument,
    ## and the function should return a number for the new number of
    ## lumis per job
    ## 
    ## Example:
    ## \code
    ## obj.modifyLumisPerJob(lambda n: 2*n)
    ## \endcode
    #def modifyLumisPerJob(self, func):
        #self.inputData.lumis_per_job = int(func(self.inputData.lumis_per_job))
        #self.inputData._ensureConsistency()

    ### Set the use_server flag.
    ## 
    ## \param use   Boolean, True for use_server=1, False for use_server=0
    ## 
    ## The use of CRAB server can be controlled at dataset level
    ## granularity. This method can be used to override the default
    ## behaviour taken from the configuration in multicrabWorkflows module.
    #def useServer(self, use):
        #value=0
        #if use: value=1
        #self.data["use_server"] = value

    ### Append an argument to pycfg_params list.
    #def appendArg(self, arg):
        #self.args.append(arg)

    ### Append a line to multicrab.cfg configuration (for this dataset only).
    ## 
    ## Line can be any string multicrab eats, e.g.
    ## \li USER.publish_dataset = foo
    ## \li CMSSW.output_file = foo.root
    #def appendLine(self, line):
        #self.lines.append(line)

    ### Add name of a file to the list of files to be copied under the multicrab directory
    #def appendCopyFile(self, fileName):
        #self.filesToCopy.append(fileName)

    ### Extend the CE/SE black/white list with a list of sites.
    ## 
    ## \param blackWhiteList    String specifying which list is modified
    ##                          ('ce_black_list', 'ce_white_list', 'se_black_list', 'se_white_list')
    ## \param sites              List of sites to extend the given black/white list
    #def extendBlackWhiteList(self, blackWhiteList, sites):
        #if blackWhiteList not in self.blackWhiteListParams:
            #raise Exception("Black/white list parameter is '%s', should be on of %s" % (blackWhiteList, ", ".join(self.blackWhiteListParams)))
        #if blackWhiteList in self.data:
            #self.data[blackWhiteList].extend(sites)
        #else:
            #self.data[blackWhiteList] = sites[:]

    ### Write generated files to a directory.
    ##
    ## \param directory   Directory where to write the generated files
    ## 
    ## The method was intended to be called from the Multicrab class.
    #def _writeGeneratedFiles(self, directory):
        #for fname, content in self.generatedFiles:
            #f = open(os.path.join(directory, fname), "wb")
            #f.write(content)
            #f.close()


    ### Get the list of files to be copied to the multicrab task directory.
    ## 
    ## The method was intended to be called from Multicrab class.
    #def _getCopyFiles(self):
        #return self.filesToCopy

    ### Generate the multicrab.cfg configuration fragment.
    ## 
    ## The method was intended to be called from Multicrab class.
    #def _getConfig(self):
        #(ret, args) = self.dataset.constructMulticrabFragment(self.workflow.getName())
        #args.extend(self.args)
        #if len(args) > 0:
            #ret += "CMSSW.pycfg_params = %s\n" % ":".join(args)

        #for key in self.blackWhiteListParams:
            #try:
                #ret += "GRID.%s = %s\n" % (key, ",".join(self.data[key]))
            #except KeyError:
                #pass

        #for key in ["use_server"]:
            #try:
                #ret += "CRAB.%s = %s\n" % (key, self.data[key])
            #except KeyError:
                #pass

        #for line in self.lines:
            #ret += line + "\n"

        #return ret

## Abstraction of the entire multicrab configuration for the configuration generation (intended for users)
class Multicrab:
    # "Enumeration" for task splitting mode for tasks with >= 500 jobs
    NONE = 1
    SPLIT = 2
    SERVER = 3

    ## Constructor.
    # 
    # \param crabConfig   String for crab configuration file
    # \param pyConfig     If set, override the python CMSSW configuration file
    #                     of crabConfig
    # \param lumiMaskDir  The directory for lumi mask (aka JSON) files, can
    #                     be absolute or relative path
    # \param crabConfigTemplate  String containing the crab.cfg. Either this ir crabConfig must be given
    # \param ignoreMissingDatasets  If true, missing datasets in a workflow are ignored in _createDatasets()
    # 
    # Parses the crabConfig file for CMSSW.pset and CMSSW.lumi_mask.
    # Ensures that the CMSSW configuration file exists.
    def __init__(self, crabConfig=None, pyConfig=None, lumiMaskDir="", crabConfigTemplate=None, ignoreMissingDatasets=False):
        if crabConfig is None and crabConfigTemplate is None:
            raise Exception("You must specify either crabConfig or crabConfigTemplate, you gave neither")
        if crabConfig is not None and crabConfigTemplate is not None:
            raise Exception("You must specify either crabConfig or crabConfigTemplate, you gave both")

        self.generatedFiles = []
        self.filesToCopy = []

        self.commonLines = []
        self.lumiMaskDir = lumiMaskDir

        self.datasetNames = []

        self.datasets = None

        self.ignoreMissingDatasets = ignoreMissingDatasets

        # Read crab.cfg for lumi_mask and optionally pset
        if crabConfig is not None:
            if not os.path.exists(crabConfig):
                raise Exception("CRAB configuration file '%s' doesn't exist!" % crabConfig)

            self.crabConfig = os.path.basename(crabConfig)
            self.filesToCopy.append(crabConfig)            

            crab_parser = ConfigParser.ConfigParser()
            crab_parser.read(crabConfig)

            optlist = ["lumi_mask"]
            if pyConfig is None:
                optlist.append("pset")
            for opt in optlist:
                try:
                    self.filesToCopy.append(crab_parser.get("CMSSW", opt))
                except ConfigParser.NoOptionError:
                    pass
                except ConfigParser.NoSectionError:
                    pass
        else:
            self.crabConfig = "crab.cfg"
            self.generatedFiles.append( ("crab.cfg", crabConfigTemplate) )
    
        # If pyConfig is given, use it
        if pyConfig != None:
            if not os.path.exists(pyConfig):
                raise Exception("Python configuration file '%s' doesn't exist!" % pyConfig)

            self.filesToCopy.append(pyConfig)
            self.commonLines.append("CMSSW.pset = "+os.path.basename(pyConfig))

    ## Extend the list of datasets for which the multicrab configuration is generated.
    #
    # \param workflow      String for workflow
    # \param datasetNames  List of strings of the dataset names.
    def extendDatasets(self, workflow, datasetNames):
        if self.datasets != None:
            raise Exception("Unable to add more datasets, the dataset objects are already created")

        self.datasetNames.extend([(name, workflow) for name in datasetNames])

    ## Create the MulticrabDataset objects.
    # 
    # This method was intended to be called internally.
    def _createDatasets(self):

        if len(self.datasetNames) == 0:
            raise Exception("Call addDatasets() first!")

        self.datasets = []
        self.datasetMap = {}

        for dname, workflow in self.datasetNames:
            try:
                dset = MulticrabDataset(dname, workflow, self.lumiMaskDir)
                self.datasets.append(dset)
                self.datasetMap[dname] = dset
            except Exception, e:
                if not self.ignoreMissingDatasets:
                    raise
                print "Warning: dataset %s ignored for workflow %s, reason: %s" % (dname, workflow, str(e))

    ## Get MulticrabDataset object for name.
    def getDataset(self, name):
        if self.datasets == None:
            self._createDatasets()

        return self.datasetMap[name]

    def getNumberOfDatasets(self):
        if self.datasets == None:
            self._createDatasets()

        return len(self.datasets)

    ## Apply a function for each MulticrabDataset.
    #
    # \param function    Function
    # 
    # The function should take the MulticrabDataset object as an
    # argument. The return value of the function is not used.
    # 
    # Example
    # \code
    # obj.forEachDataset(lambda d: d.setNumberOfJobs(6))
    # \endcode
    def forEachDataset(self, function):
        if self.datasets == None:
            self._createDatasets()

        for d in self.datasets:
            function(d)

    ## Modify the number of jobs of all dataset with a function.
    # 
    # \param func    Function
    #
    # The function gets the original number of jobs as an argument,
    # and the function should return a number for the new number of
    # jobs.
    # 
    # Example
    # \code
    # obj.modifyNumberOfJobsAll(lambda n: 2*n)
    # \endcode
    def modifyNumberOfJobsAll(self, func):
        if self.datasets == None:
            self._createDatasets()

        for d in self.datasets:
            if "number_of_jobs" in d.data:
                d.modifyNumberOfJobs(func)

    ## Modify the lumis per job s of all dataset with a function.
    # 
    # The function gets the original lumis per job as an argument,
    # and the function should return a number for the new number of
    # lumis per job.
    # 
    # Example
    # \code
    # obj.modifyLumisPerJobAll(lambda n: 2*n)
    # \endcode
    def modifyLumisPerJobAll(self, func):
        if self.datasets == None:
            self._createDatasets()
        for d in self.datasets:
            if "lumis_per_job" in d.data:
                d.modifyLumisPerJob(func)
    
    ## Append an argument to the pycfg_params list for all datasets.
    def appendArgAll(self, arg):
        if self.datasets == None:
            self._createDatasets()
        for d in self.datasets:
            d.appendArg(arg)


    ## Append a line to multicrab.cfg configuration for all datasets.
    #
    # \param line   Line to add
    # 
    # Line can be any string multicrab eats, e.g.
    # \li USER.publish_dataset = foo
    # CMSSW.output_file = foo.root
    def appendLineAll(self, line):
        if self.datasets == None:
            self._createDatasets()
        for d in self.datasets:
            d.appendLine(line)

    ## Extend the CE/SE black/white list with a list of sites for all datasets.
    # 
    # \param blackWhiteList    String specifying which list is modified
    #                          ('ce_black_list', 'ce_white_list', 'se_black_list', 'se_white_list')
    # \param sites             List of sites to extend the given black/white list
    def extendBlackWhiteListAll(self, blackWhiteList, sites):
        if self.datasets == None:
            self._createDatasets()
        for d in self.datasets:
            d.extendBlackWhiteList(blackWhiteList, sites)

    ## Append a line to multicrab.cfg configuration to the [COMMON] section.
    # 
    # Line can be any string multicrab eats, e.g.
    # \li USER.publish_dataset = foo
    # \li CMSSW.output_file = foo.root
    def addCommonLine(self, line):
        self.commonLines.append(line)

    ## Generate the multicrab configration as a string.
    # 
    # \param datasetNames  List of dataset names for which to write the configuration
    #
    # This method was intended to be called internally.
    def _getConfig(self, datasetNames):
        if self.datasets == None:
            self._createDatasets()

        ret = "[MULTICRAB]\n"
        ret += "cfg = %s\n" % self.crabConfig

        ret += "\n[COMMON]\n"
        for line in self.commonLines:
            ret += line + "\n"

        for name in datasetNames:
            ret += "\n" + self.getDataset(name)._getConfig()

        return ret

    ## Write generated files to a directory.
    #
    # \param directory   Directory where to write the generated files
    #
    # This method was intended to be called internally.
    def _writeGeneratedFiles(self, directory):
        for fname, content in self.generatedFiles:
            f = open(os.path.join(directory, fname), "wb")
            f.write(content)
            f.close()

    ## Write the multicrab configuration to a given file name.
    #
    # \param filename      Write the configuration to this file
    # \param datasetNames  List of dataset names for which to write the configuration
    # 
    # This method was intended to be called internally.
    def _writeConfig(self, filename, datasetNames):
        f = open(filename, "wb")
        f.write(self._getConfig(datasetNames))
        f.close()

        directory = os.path.dirname(filename)
        self._writeGeneratedFiles(directory)

        for name in datasetNames:
            self.getDataset(name)._writeGeneratedFiles(directory)

        print "Wrote multicrab configuration to %s" % filename

    ## Create the multicrab task.
    # 
    # \param configOnly   If true, generate the configuration only (default: False).
    # \param kwargs       Keyword arguments (forwarded to multicrab.createTaskDir, see also below)
    #
    # <b>Keyword arguments</b>
    # \li\a prefix       Prefix of the multicrab task directory (default: 'multicrab')
    # 
    # Creates a new directory for the CRAB tasks, generates the
    # multicrab.cfg in there, copies and generates the necessary
    # files to the directory and optionally run 'multicrab -create'
    # in the directory.
    def createTasks(self, configOnly=False, codeRepo='git', over500JobsMode=NONE, **kwargs):
        if self.datasets == None:
            self._createDatasets()

        # If mode is NONE, create tasks for all datasets
        if over500JobsMode == Multicrab.NONE:
            return self._createTasks(configOnly, codeRepo, **kwargs)

        datasetsOver500Jobs = OrderedDict.OrderedDict()
        datasetsUnder500Jobs = OrderedDict.OrderedDict()
        def checkAnyOver500Jobs(dataset):
            njobs = dataset.getNumberOfJobs()
            if njobs > 500:
                datasetsOver500Jobs[dataset.getName()] = njobs
            else:
                datasetsUnder500Jobs[dataset.getName()] = njobs
        self.forEachDataset(checkAnyOver500Jobs)
        # If all tasks have < 500 jobs, create all tasks
        if len(datasetsOver500Jobs) == 0:
            return self._createTasks(configOnly, codeRepo, **kwargs)

        # If mode is SERVER, set server=1 for tasks with >= 500 jobs
        if over500JobsMode == Multicrab.SERVER:
            for dname in datasetsOver500Jobs.iterkeys():
                self.getDataset(dname).useServer(True)
            return self._createTasks(configOnly, codeRepo, **kwargs)

        # If mode is SPLIT, first create < 500 job tasks in one
        # multicrab directory, then for each tasks with >= 500 jobs
        # create one multicrab directory per 500 jobs
        if over500JobsMode == Multicrab.SPLIT:
            ret = self._createTasks(configOnly, codeRepo, datasetNames=datasetsUnder500Jobs.keys(), **kwargs)

            args = {}
            args.update(kwargs)
            prefix = kwargs.get("prefix", "multicrab")
            
            for datasetName, njobs in datasetsOver500Jobs.iteritems():
                dname = datasetName.split("_")[0]
                nMulticrabTasks = int(math.ceil(njobs/500.0))
                for i in xrange(nMulticrabTasks):
                    firstJob = i*500+1
                    lastJob = (i+1)*500
                    args["prefix"] = "%s_%s_%d-%d" % (prefix, dname, firstJob, lastJob)
                    ret.extend(self._createTasks(configOnly, codeRepo, datasetNames=[datasetName], **args))

            return ret

        raise Exception("Incorrect value for over500JobsMode: %d" % over500JobsMode)
                                                    

    ## Create the multicrab task.
    # 
    # \param configOnly   If true, generate the configuration only (default: False).
    # \param codeRepo     If something else than 'git', don't produce codeVersion/Status/Diff files
    # \param datasetNames If not None, should be list of dataset names for which to create tasks
    # \param kwargs       Keyword arguments (forwarded to multicrab.createTaskDir, see also below)
    #
    # <b>Keyword arguments</b>
    # \li\a prefix       Prefix of the multicrab task directory (default: 'multicrab')
    # 
    # Creates a new directory for the CRAB tasks, generates the
    # multicrab.cfg in there, copies and generates the necessary
    # files to the directory and optionally run 'multicrab -create'
    # in the directory.
    def _createTasks(self, configOnly=False, codeRepo='git', datasetNames=None, **kwargs):
        if not configOnly:
            checkCrabInPath()
        dirname = createTaskDir(**kwargs)

        if datasetNames != None:
            dsetNames = datasetNames[:]
        else:
            dsetNames = [d.getName() for d in self.datasets]

        self._writeConfig(os.path.join(dirname, "multicrab.cfg"), dsetNames)

        # Create code versions
	if codeRepo == 'git':
            writeGitVersion(dirname)

        files = self.filesToCopy[:]
        for name in dsetNames:
            files.extend(self.getDataset(name)._getCopyFiles())
        
        # Unique list of files
        keys = {}
        for f in files:
            keys[f] = 1
        files = keys.keys()
        for f in files:
            shutil.copy(f, dirname)
        print "Copied %s to %s" % (", ".join(files), dirname)
    
        if not configOnly:
            print "Creating multicrab task"
            print 
            print "############################################################"
            print

            prevdir = os.getcwd()
            os.chdir(dirname)
            subprocess.call(["multicrab", "-create"])
            print
            print "############################################################"
            print
            print "Created multicrab task to subdirectory "+dirname
            print

            os.chdir(prevdir)

        return [(dirname, dsetNames)]
