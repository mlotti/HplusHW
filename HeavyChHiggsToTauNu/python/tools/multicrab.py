import os, re
import subprocess, errno
import time
import shutil
import ConfigParser
import OrderedDict

from FWCore.PythonUtilities.LumiList import LumiList

import multicrabDatasets

def getTaskDirectories(opts, filename="multicrab.cfg"):
    if hasattr(opts, "dirs") and len(opts.dirs) > 0:
        return opts.dirs
    else:
        mc_ignore = ["MULTICRAB", "COMMON"]
        mc_parser = ConfigParser.ConfigParser(dict_type=OrderedDict.OrderedDict)
        mc_parser.read("multicrab.cfg")

        sections = mc_parser.sections()

        for i in mc_ignore:
            sections.remove(i)

#        sections.sort()

        return sections


def addOptions(parser):
    parser.add_option("--dir", "-d", dest="dirs", type="string", action="append", default=[],
                      help="CRAB task directory to have the files to merge (default: read multicrab.cfg and use the sections in it)")


def checkCrabInPath():
    try:
        retcode = subprocess.call(["crab"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except OSError, e:
        if e.errno == errno.ENOENT:
            raise Exception("crab executable not found in $PATH. Is the crab environment loaded?")
        else:
            raise e

def createTaskDir():
    dirname = "multicrab_" + time.strftime("%y%m%d_%H%M%S")
    os.mkdir(dirname)
    return dirname

def printAllDatasets(details=False):
    names = multicrabDatasets.datasets.keys()
    names.sort()

    for name in names:
        line = name
        if details:
            content = multicrabDatasets.datasets[name]
            inputs = content["data"].keys()
            inputs.sort()
            line += " : " + ", ".join(inputs)
        print line

def filterRuns(lumiList, runMin, runMax):
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

class MulticrabDataset:
    def __init__(self, name, dataInput):
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
            raise Exception("Setting lumi_mask in multicrabDatasets.py is not supported, use Multicrab.setDataLumiMask() instead")

        self._isData = False
        if "data" in self.data["dataVersion"]:
            self._isData = True
        
        self._lumiMaskRequired = False
        try:
            self._lumiMaskRequired = self.data["lumiMaskRequired"]
            del self.data["lumiMaskRequired"]
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
        if"lumis_per_job" in self.data:
            raise Exception("Unable to modify number_of_jobs, lumis_per_job already set!")
        self.data["number_of_jobs"] = int(func(self.data["number_of_jobs"]))

    def setLumisPerJob(self, nlumis):
        if "number_of_jobs" in self.data:
            raise Exception("Unable modify number_of_jobs, lumis_per_job already set")
        self.data["lumis_per_job"] = int(nlumis)

    def modifyLumisPerJob(self, func):
        if "number_of_jobs" in self.data:
            raise Exception("Unable modify number_of_jobs, lumis_per_job already set")
        self.data["lumis_per_job"] = int(func(self.data["lumis_per_job"]))

    def setLumiMask(self, fname):
        if not self.isData():
            raise Exception("Tried to set lumi mask for dataset '%s' which is MC" % self.name)

        if "runs" in self.data:
            (runMin, runMax) = self.data["runs"]
            lumiList = filterRuns(LumiList(filename=fname), runMin, runMax)

            info = "_runs_%s_%s" % (str(runMin), str(runMax))

            ext_re = re.compile("(\.[^.]+)$")
            fname = ext_re.sub(info+"\g<1>", os.path.basename(fname))
            self.generatedFiles.append( (fname, str(lumiList)) )
        else:
            self.filesToCopy.append(fname)

        self.data["lumi_mask"] = os.path.basename(fname)

    def addArg(self, arg):
        self.args.append(arg)

    def addLine(self, line):
        self.lines.append(line)

    def addBlackWhiteList(self, blackWhiteList, sites):
        if blackWhiteList not in self.blackWhiteListParams:
            raise Exception("Black/white list parameter is '%s', should be on of %s" % (blackWhiteList, ", ".join(self.blackWhiteListParams)))
        if blackWhiteList in self.data:
            self.data[blackWhiteList].extend(sites)
        else:
            self.data[blackWhiteList] = sites[:]

    def writeGeneratedFiles(self, directory):
        for fname, content in self.generatedFiles:
            f = open(os.path.join(directory, fname), "wb")
            f.write(content)
            f.close()

    def getCopyFiles(self):
        return self.filesToCopy

    def getConfig(self):
        dataKeys = self.data.keys()

        args = ["dataVersion=%s" % self.data["dataVersion"]]
        del dataKeys[dataKeys.index("dataVersion")]
        for argName in ["trigger", "crossSection", "luminosity"]:
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

        for key in ["dbs_url", "lumis_per_job", "number_of_jobs"]:
            try:
                ret += "CMSSW.%s = %s\n" % (key, self.data[key])
                del dataKeys[dataKeys.index(key)]
            except KeyError:
                pass
        try:
            ret += "CMSSW.lumi_mask = %s\n" % self.data["lumi_mask"]
            del dataKeys[dataKeys.index("lumi_mask")]
        except KeyError:
            if self._lumiMaskRequired:
                raise Exception("Dataset '%s' requires lumi mask but doesn't have lumi_mask set!" % self.name)

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
    def __init__(self, crabConfig, pyConfig=None):
        if not os.path.exists(crabConfig):
            raise Exception("CRAB configuration file '%s' doesn't exist!" % crabConfig)

        self.crabConfig = os.path.basename(crabConfig)
        self.filesToCopy = [crabConfig]

        self.commonLines = []
        self.dataLumiMask = None

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
            self.commonLines.append("CMSSW.pset = "+pyConfig)

    def addDatasets(self, dataInput, datasetNames):
        self.datasetNames.extend([(name, dataInput) for name in datasetNames])

    def _createDatasets(self):
        if len(self.datasetNames) == 0:
            raise Exception("Call setDatasets() first!")

        self.datasets = []
        self.datasetMap = {}

        for dname, dinput in self.datasetNames:
            dset = MulticrabDataset(dname, dinput)
            if self.dataLumiMask != None and dset.isData():
                dset.setLumiMask(self.dataLumiMask)
            self.datasets.append(dset)
            self.datasetMap[dname] = dset

    def setDataLumiMask(self, fname):
        if not os.path.exists(fname):
            raise Exception("Lumi mask file '%s' doesn't exist!" % fname)

        self.dataLumiMask = fname
        if self.datasets != None:
            for d in self.datasets:
                if d.isData():
                    d.setLumiMask(self.dataLumiMask)

    def getDataset(self, name):
        if self.datasets == None:
            self._createDatasets()

        return self.datasetMap[name]

    def forEachDataset(self, function):
        if self.datasets == None:
            self._createDatasets()

        for d in self.datasets:
            function(d)

    def modifyNumberOfJobsAll(self, func):
        if self.datasets == None:
            self._createDatasets()

        for d in self.datasets:
            if "number_of_jobs" in d.data:
                d.modifyNumberOfJobs(func)

    def modifyLumisPerJobAll(self, func):
        if self.datasets == None:
            self._createDatasets()
        for d in self.datasets:
            if "lumis_per_job" in d.data:
                d.modifyLumisPerJob(func)
    
    def addArgAll(self, arg):
        if self.datasets == None:
            self._createDatasets()
        for d in self.datasets:
            d.addArg(arg)

    def addLineAll(self, line):
        if self.datasets == None:
            self._createDatasets()
        for d in self.datasets:
            d.addLine(line)

    def addBlackWhiteListAll(self, blackWhiteList, sites):
        if self.datasets == None:
            self._createDatasets()
        for d in self.datasets:
            d.addBlackWhiteList(blackWhiteList, sites)

    def addCommonLine(self, line):
        self.commonLines = []

    def getConfig(self):
        if self.datasets == None:
            self._createDatasets()

        ret = "[MULTICRAB]\n"
        ret += "cfg = %s\n" % self.crabConfig

        ret += "\n[COMMON]\n"
        for line in self.commonLines:
            ret += line + "\n"

        for d in self.datasets:
            ret += "\n" + d.getConfig()

        return ret

    def writeConfig(self, filename):
        f = open(filename, "wb")
        f.write(self.getConfig())
        f.close()

        directory = os.path.dirname(filename)
        for d in self.datasets:
            d.writeGeneratedFiles(directory)

        print "Wrote multicrab configuration to %s" % filename
        

    def createTasks(self, configOnly=False):
        checkCrabInPath()
        dirname = createTaskDir()

        self.writeConfig(os.path.join(dirname, "multicrab.cfg"))

        files = self.filesToCopy[:]
        for d in self.datasets:
            files.extend(d.getCopyFiles())
        
        # Unique list of files
        keys = {}
        for f in files:
            keys[f] = 1
        files = keys.keys()
        for f in files:
            shutil.copy(f, dirname)
        print "Copied %s to %s" % (", ".join(files), dirname)
        print "Creating multicrab task"
        print 
        print "############################################################"
        print
    
        if not configOnly:
            os.chdir(dirname)
            subprocess.call(["multicrab", "-create"])

            print
            print "############################################################"
            print
            print "Created multicrab task to subdirectory "+dirname
            print

