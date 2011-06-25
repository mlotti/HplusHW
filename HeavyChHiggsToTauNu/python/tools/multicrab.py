import os, re
import subprocess, errno
import time
import shutil
import ConfigParser
import OrderedDict

import multicrabDatasets
import certifiedLumi

defaultSeBlacklist = [
    # blacklist before v13
    #"T2_UK_London_Brunel", # I don't anymore remember why this is here
    #"T2_BE_IIHE", # All jobs failed with stageout timeout
    #"T2_IN_TIFR", # All jobs failed file open errors
    #"T2_US_Florida", # In practice gives low bandwidth to T2_FI_HIP => stageouts timeout

    # blacklist after v13
    "colorado.edu", # Ultraslow bandwidth, no chance to get even the smaller pattuples through
    ]

def getTaskDirectories(opts, filename="multicrab.cfg"):
    """Returns the list of CRAB task directories from a MultiCRAB configuration.
    
    Arguments:
    opts      If this object contains 'dirs' attribute, the content of it
              is returned instead. The use case is that one can give
              e.g. OptionParser object, whose 'dirs' option is
              optional, to override the default behaviour of reading
              the configuration file.

    filename  Path to the multicrab.cfg file (default: 'multicrab.cfg')

    The order of the task names is the same as they are in the
    configuration file.
    """
    if hasattr(opts, "dirs") and len(opts.dirs) > 0:
        ret = []
        for d in opts.dirs:
            if d[-1] == "/":
                ret.append(d[0:-1])
            else:
                ret.append(d)
        return ret
    else:
        directory = os.path.dirname(filename)

        mc_ignore = ["MULTICRAB", "COMMON"]
        mc_parser = ConfigParser.ConfigParser(dict_type=OrderedDict.OrderedDict)
        mc_parser.read(filename)

        sections = mc_parser.sections()

        for i in mc_ignore:
            try:
                sections.remove(i)
            except ValueError:
                pass

#        sections.sort()

        def filt(dir):
            if opts.filter in dir:
                return True
            return False
        fi = lambda x: True
        if opts != None and opts.filter != "":
            fi = filt

        return filter(fi, [os.path.join(directory, sec) for sec in sections])


def addOptions(parser):
    """Add common MultiCRAB options to OptionParser object."""
    parser.add_option("--dir", "-d", dest="dirs", type="string", action="append", default=[],
                      help="CRAB task directory to have the files to merge (default: read multicrab.cfg and use the sections in it)")
    parser.add_option("--filter", dest="filter", type="string", default="",
                      help="When reading CRAB tasks from multicrab.cfg, take only tasks whose names contain this string")

def checkCrabInPath():
    """Raise OSError if 'crab' command is not found in $PATH."""
    try:
        retcode = subprocess.call(["crab"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except OSError, e:
        if e.errno == errno.ENOENT:
            raise Exception("crab executable not found in $PATH. Is the crab environment loaded?")
        else:
            raise e

def createTaskDir(prefix="multicrab"):
    """Create 'standard' multicrab task directory and return the name of it."""
    dirname = prefix+"_" + time.strftime("%y%m%d_%H%M%S")
    os.mkdir(dirname)
    return dirname

def printAllDatasets(details=False):
    multicrabDatasets.printAllDatasets(details)

def filterRuns(lumiList, runMin, runMax):
    """Select runs [runMin, runMax] from lumiList.

    lumiList is assumed to be FWCore.PythonUtilities.LumiList.LumiList
    object.

    Returns the modified LumiList object.
    """
    # From FWCore/PythonUtilities/scripts/filterJSON.py
    runsToRemove = []
    allRuns = lumiList.getRuns()
    for run in allRuns:
        if runMin != None and int(run) < runMin:
            runsToRemove.append (run)
        if runMax != None and int(run) > runMax:
            runsToRemove.append (run)

    lumiList.removeRuns(runsToRemove)
    return lumiList

class ExitCodeException(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message

def assertJobSucceeded(stdoutFile):
    re_exe = re.compile("ExeExitCode=(?P<code>\d+)")
    re_job = re.compile("JobExitCode=(?P<code>\d+)")

    exeExitCode = None
    jobExitCode = None
    f = open(stdoutFile)
    for line in f:
        m = re_exe.search(line)
        if m:
            exeExitCode = int(m.group("code"))
            continue
        m = re_job.search(line)
        if m:
            jobExitCode = int(m.group("code"))
            continue
    f.close()
    if exeExitCode == None:
        raise ExitCodeException("No exeExitCode")
    if jobExitCode == None:
        raise ExitCodeException("No jobExitCode")
    if exeExitCode != 0:
        raise ExitCodeException("Executable exit code is %d" % exeExitCode)
    if jobExitCode != 0:
        raise ExitCodeException("Job exit code is %d" % jobExitCode)

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


def crabStatusOutput(task):
    command = ["crab", "-status", "-c", task]
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = p.communicate()[0]
    if p.returncode != 0:
        raise Exception("Command '%s' failed with exit code %d, output:\n%s" % (" ".join(command), p.returncode, output))
    return output

def _addToDictList(d, name, item):
    if name in d:
        d[name].append(item)
    else:
        d[name] = [item]

def crabOutputToJobs(task, output):
    status_re = re.compile("(?P<id>\d+)\s+(?P<end>\S)\s+(?P<status>\S+)(\s+\(.*?\))?\s+(?P<action>\S+)\s+(?P<execode>\S+)?\s+(?P<jobcode>\S+)?\s+(?P<host>\S+)?")
    jobs = {}
    for line in output.split("\n"):
        m = status_re.search(line)
        if m:
            job = CrabJob(task, m)
            _addToDictList(jobs, job.status, job)
    return jobs

def _intIfNotNone(n):
    if n == None:
        return n
    return int(n)

def crabStatusToJobs(task):
    output = crabStatusOutput(task)
    return crabOutputToJobs(task, output)

class CrabJob:
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
            self.exeExitCode = intIfNotNone(match.group("execode"))
            self.jobExitCode = intIfNotNone(match.group("jobcode"))
        self.host = match.group("host")

        if self.jobExitCode != None and self.jobExitCode != 0:
            self.status += " (%d)" % self.jobExitCode
        elif self.exeExitCode != None and self.exeExitCode != 0:
            self.status += " (exe %d)" % self.jobExitCode
#        if self.status == "Retrieved":
#            try:
#                multicrab.assertJobSucceeded(self.stdoutFile())
#            except multicrab.ExitCodeException:
#                self.status += "(malformed stdout)"
#                self.jobExitCode = -1
#                self.exeExitCode = -1
        

    def stdoutFile(self):
        return os.path.join(self.task, "res", "CMSSW_%d.stdout"%self.id)

    def failed(self, status):
        if (status == "all" or status == "aborted") and self.origStatus == "Aborted":
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

class MulticrabDataset:
    """Dataset class for generating multicrab.cfg."""

    def __init__(self, name, dataInput, lumiMaskDir):
        """Constructor.

        Parameters:
        name         Name of the dataset (i.e. dataset goes to [name] section
                     in multicrab.cfg.
        dataInput    String of data input type (e.g. 'RECO', 'AOD', 'pattuple_v6'),
                     technically the key to the 'data' dictionary in multicrab dataset
                     configuration.
        lumiMaskDir  Directory where lumi mask (aka JSON) files are
                     (can be absolute or relative to the working directory)

        The constructor fetches the dataset configuration from
        multicrabDatasets module. It makes some sanity checks for the
        configuration, and also filters the runs of the lumi mask if
        a run range is explicitly given.
        """

        self.name = name
        self.args = []
        self.lines = []
        self.generatedFiles = []
        self.filesToCopy = []
        self.data = {}

        self.blackWhiteListParams = ["ce_white_list", "se_white_list", "ce_black_list", "se_black_list"]

        try:
            config = multicrabDatasets.datasets[name]
        except KeyError:
            raise Exception("Invalid dataset name '%s'" % name)

        for key, value in config.iteritems():
            if key != "data":
                self.data[key] = value

        if "data" in config:
            try:
                dataConf = config["data"][dataInput]
                if "fallback" in dataConf:
                    dataConf = config["data"][dataConf["fallback"]]

                for key, value in dataConf.iteritems():
                    self.data[key] = value
            except KeyError:
                raise Exception("No dataInput '%s' for datasets '%s'" % (dataInput, name))

        # Sanity checks
        if not "dataVersion" in self.data:
            raise Exception("'dataVersion' missing for dataset '%s'" % name)
        if not "datasetpath" in self.data:
            raise Exception("'datasetpath' missing for dataset '%s'" % name)
        if not ("lumis_per_job" in self.data or "number_of_jobs" in self.data):
            raise Exception("'lumis_per_job' or 'number_of_jobs' missing for dataset '%s'" % name)
        if "lumis_per_job" in self.data and "number_of_jobs" in self.data:
            raise Exception("Only one of 'lumis_per_job' and 'number_of_jobs' is allowed for dataset '%s'" % name)
        if "lumi_mask" in self.data:
            raise Exception("Setting lumi_mask in multicrabDatasets.py is not supported. The lumi mask files are set in HiggsAnalysis.HeavyChHiggsToTauNu.tools.certifiedLumi, and they are assigned to datasets with lumiMask parameter.")

        self._isData = False
        if "data" in self.data["dataVersion"]:
            self._isData = True
        
        try:
            lumiKey = self.data["lumiMask"]
            if not self.isData():
                raise Exception("Lumi mask specified for datasets '%s' which is MC" % self.name)
            lumiMaskFile = os.path.join(lumiMaskDir, certifiedLumi.getFile(lumiKey))

            print "Using lumi file", lumiMaskFile
            if "runs" in self.data:
                from FWCore.PythonUtilities.LumiList import LumiList

                (runMin, runMax) = self.data["runs"]
                lumiList = filterRuns(LumiList(filename=lumiMaskFile), runMin, runMax)

                info = "_runs_%s_%s" % (str(runMin), str(runMax))

                ext_re = re.compile("(\.[^.]+)$")
                lumiMaskFile = ext_re.sub(info+"\g<1>", os.path.basename(lumiMaskFile))
                self.generatedFiles.append( (lumiMaskFile, str(lumiList)) )
            else:
                self.filesToCopy.append(lumiMaskFile)

            self.data["lumi_mask"] = os.path.basename(lumiMaskFile)

            del self.data["lumiMask"]
        except KeyError:
            pass

    def isData(self):
        return self._isData

    def isMC(self):
        return not self._isData

    def getName(self):
        return self.name

    def getDatasetPath(self):
        return self.data["datasetpath"]

    def setNumberOfJobs(self, njobs):
        if "lumis_per_job" in self.data:
            raise Exception("Unable to modify number_of_jobs, lumis_per_job already set!")
        self.data["number_of_jobs"] = int(njobs)

    def modifyNumberOfJobs(self, func):
        """Modify number of jobs with a function.

        The function gets the original number of jobs as an argument,
        and the function should return a number for the new number of
        jobs.

        Example:  obj.modifyNumberOfJobs(lambda n: 2*n)
        """

        if"lumis_per_job" in self.data:
            raise Exception("Unable to modify number_of_jobs, lumis_per_job already set!")
        self.data["number_of_jobs"] = int(func(self.data["number_of_jobs"]))

    def setLumisPerJob(self, nlumis):
        if "number_of_jobs" in self.data:
            raise Exception("Unable modify number_of_jobs, lumis_per_job already set")
        self.data["lumis_per_job"] = int(nlumis)

    def modifyLumisPerJob(self, func):
        """Modify number of lumis per job with a function.

        The function gets the original number of lumis as an argument,
        and the function should return a number for the new number of
        lumis per job

        Example:  obj.modifyLumisPerJob(lambda n: 2*n)
        """

        if "number_of_jobs" in self.data:
            raise Exception("Unable modify number_of_jobs, lumis_per_job already set")
        self.data["lumis_per_job"] = int(func(self.data["lumis_per_job"]))

    def useServer(self, use):
        """Set the use_server flag.

        Parameters:
        use   Boolean, True for use_server=1, False for use_server=0

        The use of CRAB server can be controlled at dataset level
        granularity. This method can be used to override the default
        behaviour taken from the configuration in multicrabDatasets module.
        """

        value=0
        if use: value=1
        self.data["use_server"] = value

    def appendArg(self, arg):
        """Append an argument to pycfg_params list."""
        self.args.append(arg)

    def appendLine(self, line):
        """Append a line to multicrab.cfg configuration (for this dataset only).

        Line can be any string multicrab eats, e.g.
        'USER.publish_dataset = foo'
        'CMSSW.output_file = foo.root'
        """

        self.lines.append(line)

    def extendBlackWhiteList(self, blackWhiteList, sites):
        """Extend the CE/SE black/white list with a list of sites.

        Parameters:
        blackWhiteList    String specifying which list is modified
                          ('ce_black_list', 'ce_white_list', 'se_black_list', 'se_white_list')
        sites             List of sites to extend the given black/white list
        """

        if blackWhiteList not in self.blackWhiteListParams:
            raise Exception("Black/white list parameter is '%s', should be on of %s" % (blackWhiteList, ", ".join(self.blackWhiteListParams)))
        if blackWhiteList in self.data:
            self.data[blackWhiteList].extend(sites)
        else:
            self.data[blackWhiteList] = sites[:]

    def _writeGeneratedFiles(self, directory):
        """Write generated files to a directory.

        The method was intended to be called from the Multicrab class.
        """
        for fname, content in self.generatedFiles:
            f = open(os.path.join(directory, fname), "wb")
            f.write(content)
            f.close()

    def _getCopyFiles(self):
        """Get the list of files to be copied to the multicrab task directory.

        The method was intended to be called from Multicrab class.
        """

        return self.filesToCopy

    def _getConfig(self):
        """Generate the multicrab.cfg configuration fragment.

        The method was intended to be called from Multicrab class.
        """

        dataKeys = self.data.keys()

        args = ["dataVersion=%s" % self.data["dataVersion"]]
        del dataKeys[dataKeys.index("dataVersion")]
        for argName in ["trigger", "crossSection", "luminosity", "tauIDFactorizationMap"]:
            try:
                args.append("%s=%s" % (argName, self.data[argName]))
                del dataKeys[dataKeys.index(argName)]
            except KeyError:
                pass

        args += self.args
        try:
            args.extend(self.data["args"])
            del dataKeys[dataKeys.index("args")]
        except KeyError:
            pass           

        ret = "[%s]\n" % self.name
        ret += "CMSSW.datasetpath = %s\n" % self.data["datasetpath"]
        ret += "CMSSW.pycfg_params = %s\n" % ":".join(args)
        del dataKeys[dataKeys.index("datasetpath")]

        for key in ["dbs_url", "lumis_per_job", "number_of_jobs", "lumi_mask"]:
            try:
                ret += "CMSSW.%s = %s\n" % (key, self.data[key])
                del dataKeys[dataKeys.index(key)]
            except KeyError:
                pass
        for key in ["ce_white_list", "se_white_list", "ce_black_list", "se_black_list"]:
            try:
                ret += "GRID.%s = %s\n" % (key, ",".join(self.data[key]))
                del dataKeys[dataKeys.index(key)]
            except KeyError:
                pass

        for key in ["use_server"]:
            try:
                ret += "CRAB.%s = %s\n" % (key, self.data[key])
                del dataKeys[dataKeys.index(key)]
            except KeyError:
                pass

        if "runs" in self.data:
            del dataKeys[dataKeys.index("runs")]

        if len(dataKeys) > 0:
            print "WARNING: Dataset '%s' has the following settings in multicrabDatasets.py which have *not* been used!" % self.name
            print "  "+"\n  ".join(dataKeys)

        for line in self.lines:
            ret += line + "\n"

        return ret


class Multicrab:
    """Represents the entire multicrab configuration for the configuration generation."""

    def __init__(self, crabConfig, pyConfig=None, lumiMaskDir=""):
        """Constructor.

        Parameters:
        crabConfig   String for crab configuration file
        pyConfig     If set, override the python CMSSW configuration file
                     of crabConfig
        lumiMaskDir  The directory for lumi mask (aka JSON) files, can
                     be absolute or relative path

        Parses the crabConfig file for CMSSW.pset and CMSSW.lumi_mask.
        Ensures that the CMSSW configuration file exists.
        """
        if not os.path.exists(crabConfig):
            raise Exception("CRAB configuration file '%s' doesn't exist!" % crabConfig)

        self.crabConfig = os.path.basename(crabConfig)
        self.filesToCopy = [crabConfig]

        self.commonLines = []
        self.lumiMaskDir = lumiMaskDir

        self.datasetNames = []

        self.datasets = None

        # Read crab.cfg for lumi_mask and optionally pset
        crab_parser = ConfigParser.ConfigParser()
        crab_parser.read(crabConfig)

        optlist = ["lumi_mask"]
        if pyConfig == None:
            optlist.append("pset")
        for opt in optlist:
            try:
                self.filesToCopy.append(crab_parser.get("CMSSW", opt))
            except ConfigParser.NoOptionError:
                pass

        # If pyConfig is given, use it
        if pyConfig != None:
            if not os.path.exists(pyConfig):
                raise Exception("Python configuration file '%s' doesn't exist!" % pyConfig)

            self.filesToCopy.append(pyConfig)
            self.commonLines.append("CMSSW.pset = "+os.path.basename(pyConfig))

    def extendDatasets(self, dataInput, datasetNames):
        """Extend the list of datasets for which the multicrab configuration is generated.
        Parameters:

        dataInput    String of data input type (e.g. 'RECO', 'AOD', 'pattuple_v6'),
                     technically the key to the 'data' dictionary in multicrab dataset
                     configuration.
        datasetNames List of strings of the dataset names.
        """
        if self.datasets != None:
            raise Exception("Unable to add more datasets, the dataset objects are already created")

        self.datasetNames.extend([(name, dataInput) for name in datasetNames])

    def _createDatasets(self):
        """Create the MulticrabDataset objects.

        This method was intended to be called internally.
        """

        if len(self.datasetNames) == 0:
            raise Exception("Call addDatasets() first!")

        self.datasets = []
        self.datasetMap = {}

        for dname, dinput in self.datasetNames:
            dset = MulticrabDataset(dname, dinput, self.lumiMaskDir)
            self.datasets.append(dset)
            self.datasetMap[dname] = dset

    def getDataset(self, name):
        """Get MulticrabDataset object for name."""

        if self.datasets == None:
            self._createDatasets()

        return self.datasetMap[name]

    def forEachDataset(self, function):
        """Apply a function for each MulticrabDataset.

        The function should take the MulticrabDataset object as an
        argument. The return value of the function is not used.

        Example:
        obj.forEachDataset(lambda d: d.setNumberOfJobs(6))
        """

        if self.datasets == None:
            self._createDatasets()

        for d in self.datasets:
            function(d)

    def modifyNumberOfJobsAll(self, func):
        """Modify the number of jobs of all dataset with a function.

        The function gets the original number of jobs as an argument,
        and the function should return a number for the new number of
        jobs.

        Example:  obj.modifyNumberOfJobsAll(lambda n: 2*n)
        """
        if self.datasets == None:
            self._createDatasets()

        for d in self.datasets:
            if "number_of_jobs" in d.data:
                d.modifyNumberOfJobs(func)

    def modifyLumisPerJobAll(self, func):
        """Modify the lumis per job s of all dataset with a function.

        The function gets the original lumis per job as an argument,
        and the function should return a number for the new number of
        lumis per job.

        Example:  obj.modifyLumisPerJobAll(lambda n: 2*n)
        """
        if self.datasets == None:
            self._createDatasets()
        for d in self.datasets:
            if "lumis_per_job" in d.data:
                d.modifyLumisPerJob(func)
    
    def appendArgAll(self, arg):
        """Append an argument to the pycfg_params list for all datasets."""
        if self.datasets == None:
            self._createDatasets()
        for d in self.datasets:
            d.appendArg(arg)

    def appendLineAll(self, line):
        """Append a line to multicrab.cfg configuration for all datasets.

        Line can be any string multicrab eats, e.g.
        'USER.publish_dataset = foo'
        'CMSSW.output_file = foo.root'
        """
        if self.datasets == None:
            self._createDatasets()
        for d in self.datasets:
            d.appendLine(line)

    def extendBlackWhiteListAll(self, blackWhiteList, sites):
        """Extend the CE/SE black/white list with a list of sites for all datasets.

        Parameters:
        blackWhiteList    String specifying which list is modified
                          ('ce_black_list', 'ce_white_list', 'se_black_list', 'se_white_list')
        sites             List of sites to extend the given black/white list
        """

        if self.datasets == None:
            self._createDatasets()
        for d in self.datasets:
            d.extendBlackWhiteList(blackWhiteList, sites)

    def addCommonLine(self, line):
        """Append a line to multicrab.cfg configuration to the [COMMON] section.

        Line can be any string multicrab eats, e.g.
        'USER.publish_dataset = foo'
        'CMSSW.output_file = foo.root'
        """
        self.commonLines.append(line)

    def _getConfig(self):
        """Generate the multicrab configration as a string.

        This method was intended to be called internally.
        """

        if self.datasets == None:
            self._createDatasets()

        ret = "[MULTICRAB]\n"
        ret += "cfg = %s\n" % self.crabConfig

        ret += "\n[COMMON]\n"
        for line in self.commonLines:
            ret += line + "\n"

        for d in self.datasets:
            ret += "\n" + d._getConfig()

        return ret

    def _writeConfig(self, filename):
        """Write the multicrab configuration to a given file name.

        This method was intended to be called internally.
        """
        f = open(filename, "wb")
        f.write(self._getConfig())
        f.close()

        directory = os.path.dirname(filename)
        for d in self.datasets:
            d._writeGeneratedFiles(directory)

        print "Wrote multicrab configuration to %s" % filename
        

    def createTasks(self, configOnly=False, **kwargs):
        """Create the multicrab task.

        Keyword arguments:
        configOnly   If true, generate the configuration only (default: False).
        prefix       Prefix of the multicrab task directory (default: 'multicrab')

        Creates a new directory for the CRAB tasks, generates the
        multicrab.cfg in there, copies and generates the necessary
        files to the directory and optionally run 'multicrab -create'
        in the directory.
        """

        checkCrabInPath()
        dirname = createTaskDir(**kwargs)

        self._writeConfig(os.path.join(dirname, "multicrab.cfg"))

        files = self.filesToCopy[:]
        for d in self.datasets:
            files.extend(d._getCopyFiles())
        
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

            os.chdir(dirname)
            subprocess.call(["multicrab", "-create"])

            print
            print "############################################################"
            print
            print "Created multicrab task to subdirectory "+dirname
            print

