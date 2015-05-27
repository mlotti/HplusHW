import re
import copy
import StringIO

import certifiedLumi
import aux

## Helper class to get an object for Disable "constant"
class _Constant:
    def __init__(self, value):
        self.value = value

## Constant for marking values to be disabled
Disable = _Constant(1)

_reco_name_re = re.compile("^(?P<reco>Run[^_]+(_[^_]+)+?_v\d+_[^_]+_)")
def updatePublishName(dataset, sourcePath, workflowName, taskDef=None):
    path = sourcePath.split("/")
    name = path[2].replace("-", "_")
    name += "_"+path[3]
    name += "_"+workflowName

    # Add the begin run in the dataset name to the publish name in
    # order to distinguish pattuple datasets from the same PD
    if dataset.isData():
        m = _reco_name_re.search(name)
        if not m:
            raise Exception("Regex '%s' did not find anything from '%s'" % (_reco_name_re.pattern, name))
        runs = dataset.getRuns()
        name = _reco_name_re.sub(m.group("reco")+str(runs[0])+"_"+str(runs[1])+"_", name)

    if taskDef is not None and taskDef.publishPostfix is not None:
        name += taskDef.publishPostfix

    return name

## Represents set of crab datasaets
class DatasetSet:
    def __init__(self, datasetList):
        self.datasetList = []
        self.datasetDict = {}
        self.extend(datasetList)

    def extend(self, datasetList):
        self.datasetList.extend(datasetList)
        for dataset in datasetList:
            if dataset.getName() in self.datasetDict:
                raise Exception("Dataset %s is already defined" % dataset.getName())
            self.datasetDict[dataset.getName()] = dataset

    def splitDataByRuns(self, sourceName, listOfRuns):
        run_re = re.compile("_\d+-\d+_")
        source = self.getDataset(sourceName)
        if source.isMC():
            raise Exception("May not split MC datasets by runs, tried to split %s." % sourceName)
        if source.runs == None:
            raise Exception("Dataset %s has no runs specified, unable to split it by runs." % sourceName)
        datasets = []
        for firstRun, lastRun in listOfRuns:
            if firstRun < source.runs[0] or lastRun > source.runs[1]:
                raise Exception("Trying to split dataset %s with runs (%d, %d) to runs (%d, %d), which is not fully contained by the dataset." % (sourceName, source.runs[0], source.runs[1], firstRun, lastRun))
            if firstRun == source.runs[0] and lastRun == source.runs[1]:
                raise Exception("Trying to split dataset %s with runs (%d, %d) to runs (%d, %d), which are the same." % (sourceName, source.runs[0], source.runs[1], firstRun, lastRun))

            dset = Dataset(run_re.sub("_%d-%d_" % (firstRun, lastRun), source.name),
                           source.dataVersion, source.energy, (firstRun, lastRun), source.crossSection)
            # In splitting case, source may have workflows with only output, and also it should contain only the dataset path
            for wf in source.workflows.itervalues():
                if not wf.hasAtMostOutput():
                    continue
                dset.addWorkflow(wf.clone())

            datasets.append(dset)

        self.extend(datasets)

    def getDataset(self, name):
        try:
#	    print "check getDataset",name,self.datasetDict
            return self.datasetDict[name]
        except KeyError:
            raise Exception("Invalid dataset name '%s' (see HiggsAnalysis/HeavyChHiggsToTauNu/python/tools/multicrabWorkflows.py for definitions of all datasets)" % name)

    def getDatasetList(self):
        return self.datasetList
    

## Represents one (crab-)dataset
#
# Here dataset corresponds to a crab task in multicrab.cfg. For MC
# dataset corresponds to one DBS-dataset, while for data dataset
# corresponds to DBS-dataset and a run range.
#
# Dataset can contain one or more Workflows (e.g. pattuples, embedding
# etc), each of which has an output DBS-dataset.
class Dataset:
    ## Constructor
    #
    # \param name         Name of the crab-dataset
    # \param dataVersion  Data version string
    # \param energy       Centre-of-mass energy (string, in TeV)
    # \param runs         For data, two-tuple of the run range
    # \param crossSection For MC, the dataset cross section in pb
    # \param workflows    List of Workflow objects
    def __init__(self, name, dataVersion, energy, runs=None, crossSection=None, workflows=[]):
        self.name = name
        self.dataVersion = dataVersion
        self.energy = energy
        self.runs = runs
        self.crossSection = crossSection

        self.workflows = {}
        self.addWorkflows(workflows)

    def getName(self):
        return self.name

    def isData(self):
        return "data" in self.dataVersion

    def isMC(self):
        return "mc" in self.dataVersion

    def hasRuns(self):
        return self.runs != None

    def getRuns(self):
        return self.runs

    def addWorkflow(self, workflow):
        if workflow.name in self.workflows:
            raise Exception("Workflow %s already exists for dataset %s" % (workflow.name, self.name))
        self.workflows[workflow.name] = workflow
        if workflow.source != None:
            workflow.source.dataset = self
            # Propagate 'sample' argument
            srcWf = self.getWorkflow(workflow.source.name)
            if srcWf.hasArg("sample") and not workflow.hasArg("sample"):
                workflow.addArg("sample", srcWf.getArg("sample"))

    def addWorkflows(self, workflows):
        for wf in workflows:
            self.addWorkflow(wf)

    def hasWorkflow(self, workflowName):
        return workflowName in self.workflows

    def getWorkflow(self, workflowName):
        try:
            return self.workflows[workflowName]
        except KeyError:
            raise Exception("Dataset '%s' does not have workflow '%s'" % (self.name, workflowName))

    ## String representation of the dataset
    def __str__(self):
        out = StringIO.StringIO()

        out.write('Dataset("%s", dataVersion="%s", energy=%s' % (self.name, self.dataVersion, self.energy))
        if self.runs != None:
            out.write(", runs=%s" % str(self.runs))
        if self.crossSection != None:
            out.write(", crossSection=%g" % self.crossSection)
        if len(self.workflows) > 0:
            out.write(", workflows=[\n")
            keys = self._workflowKeys()
            for name in keys:
                out.write(str(self.workflows[name]))
                out.write(",\n")
            out.write("]")
        out.write(")")

        ret = out.getvalue()
        out.close()
        return ret

    def _workflowKeys(self):
        # First, create a map from sources to workflow names
        # and find those which have no sourcesw
        sourceNameMap = {}
        keys = []
        for key, workflow in self.workflows.iteritems():
            if workflow.source == None:
                keys.append(key)
            else:
                aux.addToDictList(sourceNameMap, workflow.source.name, key)
        keys.sort()

        # Return the list of keys (in order), which use key as a
        # source
        def depthFirst(key):
            if not key in sourceNameMap:
                return [key]
                ret.append(key)
            nodes = sourceNameMap[key]
            nodes.sort()
            ret = [key]
            for n in nodes:
                ret.extend(depthFirst(n))
            return ret
            
        ret = []
        for k in keys:
            ret.extend(depthFirst(k))

        if len(ret) != len(self.workflows):
            raise Exception("Dataset %s, internal error, len(ret) = %d, len(self.workflows) = %d" % (self.getName(), len(ret), len(self.workflows)))
        return ret

    def constructMulticrabFragment(self, workflowName):
        out = StringIO.StringIO()

        out.write("[%s]\n" % self.name)
        (wfArgs, dataVersionAppend) = self.workflows[workflowName].constructMulticrabFragment(self, out)

        dataVersion = self.dataVersion
        if dataVersionAppend is not None:
            dataVersion += dataVersionAppend

        args = [
            "dataVersion=%s" % dataVersion,
            "energy=%s" % self.energy,
            ]
        
        if self.crossSection != None:
            args.append("crossSection=%g" % self.crossSection)

        args.extend(wfArgs)

        ret = out.getvalue()
        out.close()

        return (ret, args)

## Represents a workflow on a dataset
#
# Workflow is an entity which may take one DBS-dataset as an input,
# and possibly produces another DBS-dataset as an output. Examples:
# pattuples, analyses, embedding skims, embedding processings.
class Workflow:
    ## Constructor
    #
    # \param name        Name of the workflow (e.g. "pattuple_v44_4")
    # \param output      Data object describing the output of the workflow
    # \param source      Source object describing the input to the workflow
    # \param args        Dictionary of command line arguments for python configuration
    # \param trigger     String for a single trigger
    # \param triggerOR   List of strings for an OR of triggers
    # \param skimConfig  List of strings for skim configuration files (if many, OR of skims is taken)
    # \param output_file CMSSW output file name (if not default)
    # \param crabLines   Individual lines to add to multicrab.cfg for this workflow
    # \param dataVersionAppend  String to append to Dataset's dataVersion for this workflow
    def __init__(self, name, output=None, source=None,
                 args=None, trigger=None, triggerOR=None, skimConfig=None, output_file=None, crabLines=None, dataVersionAppend=None):
        self.name = name
        self.output = output
        self.source = source
        self.args = args
        self.trigger = trigger
        self.triggerOR = triggerOR
        self.skimConfig = skimConfig
        self.output_file = output_file
        self.crabLines = crabLines
        self.dataVersionAppend = dataVersionAppend

        if self.args is None:
            self.args = {}
        if self.crabLines is None:
            self.crabLines = []

        self._ensureConsistency()

    def addCrabLine(self, line):
        self.crabLines.append(line)

    def addArg(self, argName, argValue):
        self.args[argName] = argValue

    def removeArg(self, argName):
        del self.args[argName]

    def hasArg(self, argName):
        return argName in self.args

    def getArg(self, argName):
        return self.args[argName]

    def setOutputFile(self, output_file):
        self.output_file = output_file

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def clone(self):
        return copy.deepcopy(self)

    def hasAtMostOutput(self):
        return self.source == None and len(self.args) == 0 and self.trigger == None and self.triggerOR == None and self.skimConfig == None and self.output_file == None and len(self.crabLines) == 0

    def _ensureConsistency(self):
        if self.trigger != None and self.triggerOR != None:
            raise Exception("Workflow %s: Both 'trigger' and 'triggerOR' parameters were given, only one of them is allowed" % self.name)

    ## String representation of the workflow
    def __str__(self):
        out = StringIO.StringIO()
        prefix = "    "
        out.write(prefix+'Workflow("%s",\n' % self.name)
        if self.source != None:
            out.write(prefix+prefix+"source="+str(self.source)+",\n")
        if self.dataVersionAppend is not None:
            out.write(prefix+prefix+'dataVersionAppend="'+self.dataVersionAppend+'",\n')
        if self.trigger != None:
            out.write(prefix+prefix+'trigger="'+self.trigger+'",\n')
        if self.triggerOR != None:
            p = prefix+prefix+" "*11
            out.write(prefix+prefix+"triggerOR=["+ (",\n"+p).join(['"%s"' % t for t in self.triggerOR]) + "],\n")
        if self.args != None:
            out.write(prefix+prefix+"args={\n")
            p = prefix+prefix+prefix
            for key, value in self.args.iteritems():
                out.write(p+'"%s": '%key)
                if isinstance(value, int):
                    out.write("%d" % value)
                else:
                    out.write('"%s"' % str(value))
                out.write(",\n")
            out.write(prefix+prefix+"},\n")
        if self.skimConfig != None:
            out.write(prefix+prefix+"skimConfig=[" + ", ".join(['"%s"' % s for s in self.skimConfig]) + "],\n")
        if self.output_file != None:
            out.write(prefix+prefix+'output_file="%s",\n' % self.output_file)
        if self.output != None:
            out.write(prefix+prefix+"output="+str(self.output)+",\n")
        if len(self.crabLines) > 0:
            out.write(prefix+prefix+"crabLines=[\n")
            for line in self.crabLines:
                out.write(prefix+prefix+prefix+'"%s",\n' % line)
            out.write(prefix+prefix+"],\n")

        out.write(prefix+")")
        ret = out.getvalue()
        out.close()
        return ret

    def constructMulticrabFragment(self, dataset, out):
        self._ensureConsistency()

        if self.source != None:
            inputData = self.source.getData()
            inputData.constructMulticrabFragment(out)

        args = []
        if self.args != None:
            args.extend(["%s=%s" % (key, value) for key,value in self.args.iteritems()])
        if self.trigger != None:
            args.append("trigger=%s" % self.trigger)
        if self.triggerOR != None:
            args.extend(["trigger=%s" % t for t in self.triggerOR])
        if self.skimConfig != None:
            args.extend(["skimConfig=%s" % s for s in self.skimConfig])

        _addIfNotNone(out, "CMSSW.output_file = %s\n", self.output_file)
        for line in self.crabLines:
            out.write(line)
            out.write("\n")

        return (args, self.dataVersionAppend)

## Makes an alias for a workflow name
#
# e.g. real processing is pattuplev53_1_1, but you want it to show up
# as pattuplev53_1 too.
class WorkflowAlias:
    ## Constructor
    #
    # \param aliasName        Name of the alias
    # \param originalWorkflow Workflow object of the original workflow
    def __init__(self, aliasName, originalWorkflow):
        self.aliasName = aliasName
        self.originalWorkflow = originalWorkflow

    def getName(self):
        return self.aliasName

    def clone(self):
        obj = self.originalWorkflow.clone()
        obj.name = self.aliasName
        return obj

    ## Forward all other methods to the originalWorkflow object
    def __getattr__(self, attr):
        return getattr(self.originalWorkflow, attr)

## Helper to write to out if variable is not none
def _addIfNotNone(out, format, variable):
    if variable != None:
        out.write(format % variable)

## Helper to translate Disable to None
def _NoneIfDisable(obj):
    if obj is Disable:
        return None
    else:
        return obj

## Class representing an output of a workflow
class Data:
    ## Constructor
    #
    # \param datasetpath     Path of the output DBS-dataset
    # \param number_of_jobs  Default number of jobs for those who process the output (conflicts with lumis_per_job, events_per_job)
    # \param lumis_per_job   Default number of lumis per job for those who process the output (conflicts with number_of_jobs, events_per_job)
    # \param events_per_job  Default number of events per job for those who process the output (conflicts with number_of_jobs, lumis_per_job)
    # \param lumiMask        Default lumi mask for those who process the output
    # \param dbs_url         URL to the DBS reader instance
    #
    # If any is Disable, it is interpreted as None
    def __init__(self, datasetpath, number_of_jobs=None, lumis_per_job=None, events_per_job=None, lumiMask=None, dbs_url=None):
        self.datasetpath = datasetpath
        self.number_of_jobs = _NoneIfDisable(number_of_jobs)
        self.lumis_per_job = _NoneIfDisable(lumis_per_job)
        self.events_per_job = _NoneIfDisable(events_per_job)
        self.lumiMask = _NoneIfDisable(lumiMask)
        self.dbs_url = _NoneIfDisable(dbs_url)

        self._ensureConsistency()

    def hasLumiMask(self):
        return self.lumiMask != None

    def getLumiMaskFile(self):
        if self.hasLumiMask() and not hasattr(self, "lumiMaskFile"):
            self.lumiMaskFile = certifiedLumi.getFile(self.lumiMask)
        return self.lumiMaskFile

    def setLumiMaskFile(self, lumiMaskFile):
        self.lumiMaskFile = lumiMaskFile

    def getDatasetPath(self):
        return self.datasetpath

    def _ensureConsistency(self):
        n = 0
        if self.number_of_jobs != None: n += 1
        if self.lumis_per_job != None: n += 1
        if self.events_per_job != None: n += 1

        if n > 1:
            raise Exception("Data may have only one of number_of_jobs, lumis_per_job, events_per_job set (DBS dataset %s)" % self.datasetpath)

    ## String representation of Data
    def __str__(self):
        out = StringIO.StringIO()
        prefix = " "*(4+4+7+5)
        out.write('Data("%s"' % self.datasetpath)
        if self.number_of_jobs != None:
            out.write(",\n"+prefix+"number_of_jobs=%d" % self.number_of_jobs)
        if self.lumis_per_job != None:
            out.write(",\n"+prefix+"lumis_per_job=%d" % self.number_of_jobs)
        if self.events_per_job != None:
            out.write(",\n"+prefix+"events_per_job=%d" % self.number_of_jobs)

        if self.lumiMask != None:
            out.write(", ")
            # Formatting if there are no prior elements printed
            if self.number_of_jobs == None and self.lumis_per_job == None and self.events_per_job == None: 
                out.write("\n"+prefix)
            out.write('lumiMask="%s"' % self.lumiMask)
        if self.dbs_url != None:
            out.write(',\n'+prefix+'dbs_url="%s"' % self.dbs_url)
        out.write(")")
        
        ret = out.getvalue()
        out.close()
        return ret

    def constructMulticrabFragment(self, out):
        self._ensureConsistency()
        out.write("CMSSW.datasetpath = %s\n" % self.datasetpath)
        _addIfNotNone(out, "CMSSW.dbs_url = %s\n", self.dbs_url)
        _addIfNotNone(out, "CMSSW.number_of_jobs = %d\n", self.number_of_jobs)
        _addIfNotNone(out, "CMSSW.lumis_per_job = %d\n", self.lumis_per_job)
        if self.hasLumiMask():
            out.write("CMSSW.lumi_mask = %s\n" % self.lumiMaskFile)

## Class for representing an input for a workflow
class Source:
    ## Constructor
    #
    # \param name            Name of the workflow, whose output is used as a source
    # \param number_of_jobs  If given, overrides the number_of_jobs of the input Data object
    # \param events_per_job  If given, overrides the events_per_job of the input Data object
    # \param lumis_per_job   If given, overrides the lumis_per_job of the input Data object
    # \param lumiMask        If given, overrides the lumiMask of the input Data object
    #
    # If any of the four overrides is Disable, overrides the input
    # Data object value with None
    def __init__(self, name, number_of_jobs=None, events_per_job=None, lumis_per_job=None, lumiMask=None):
        self.name = name
        self.number_of_jobs = number_of_jobs
        self.events_per_job = events_per_job
        self.lumis_per_job = lumis_per_job
        self.lumiMask = lumiMask
        self.inputData = None
        self.dataset = None

        self._ensureConsistency()

    ## Obtain the Data object which this Source points to for a Dataset
    def getData(self):
        if self.dataset == None:
            raise Exception("Can't call getData() before the Workflow with this Source has been added to a Dataset. Before that, use getDataForDataset()")

        if self.inputData == None:
            self.inputData = self.getDataForDataset(self.dataset)
        return self.inputData

    def getDataForDataset(self, dataset):
        try:
            wf = dataset.workflows[self.name]
        except KeyError:
            raise Exception("Workflow %s used as a source, but not found from dataset %s" % (self.name, dataset.name))
    
        if wf.output == None:
            raise Exception("Workflow %s used as a source, but it does not have Data specifier in dataset %s" % (self.name, dataset.name))
    
        data = copy.deepcopy(wf.output)
        for attr in ["number_of_jobs", "events_per_job", "lumis_per_job", "lumiMask"]:
            value = getattr(self, attr)
            if value is Disable:
                setattr(data, attr, None)
            elif value is not None:
                setattr(data, attr, copy.deepcopy(value))
        data._ensureConsistency()
        return data

    def _ensureConsistency(self):
        n = 0
        if self.number_of_jobs != None: n += 1
        if self.lumis_per_job != None: n += 1
        if self.events_per_job != None: n += 1

        if n > 1:
            raise Exception("Source may have only one of number_of_jobs, lumis_per_job, events_per_job set")

    def _writeHelp(self, out, attr, form):
        value = getattr(self, attr)
        if value is not None:
            out.write(", %s=" % attr)
            if value is Disable:
                out.write("Disable")
            else:
                out.write(form % value)

    ## String representation of Source
    def __str__(self):
        self._ensureConsistency()
        out = StringIO.StringIO()
        out.write('Source("%s"' % self.name)
        self._writeHelp(out, "number_of_jobs", "%d")
        self._writeHelp(out, "events_per_job", "%d")
        self._writeHelp(out, "lumis_per_job", "%d")
        self._writeHelp(out, "lumiMask", '"%s"')
        out.write(")")

        ret = out.getvalue()
        out.close()
        return ret

## Helper class for processing task definitions
#
# When defining a processing workflow, one can specify \a njobsIn and
# \a triggerOR.
#
# When the processing has finished, add \a outputPath, and possibly \a
# njobsOut.
#
# \b Note that this is only a helper class to easily deliver
# information to Workflow, Source and Data objects.
class TaskDef:
    ## Constructor
    #
    # \param outputPath  DBS-path of the output (this is not in kwargs,
    #                    because it is handy to give as a first
    #                    argument without the keyword)
    # \param kwargs      Keyword arguments, described below (non-specified will get None as default value
    #
    # <b>Keyword arguments</b>
    # \li \a njobsIn           Overrides the number of jobs for processing (conflicts with nevents*, nlumis*)
    # \li \a njobsOut          Default number of jobs for those who process the output (conflicts with nevents*, nlumis*)
    # \li \a neventsPerJobIn   Overrides the number of events per job for processing (conflicts with njobs*, nlumis*)
    # \li \a neventsPerJobOut  Default number of events per job for those who process the output (conflicts with njobs*, nlumis*)
    # \li \a nlumisPerJobIn    Overrides the number of lumis per job for processing (conflicts with nevents*, njobs*)
    # \li \a nlumisPerJobOut   Default number of lumis per job for those who process the output (conflicts with nevents*, njobs*)
    # \li \a triggerOR         List of strings for trigger OR
    # \li \a triggerThrow      Should CMSSW throw exception if some trigger in \a triggerOR does not exist? (default is for true)
    # \li \a crabLines         Additional crab configuration lines to add for this task and dataset
    # \li \a args              Additional command line arguments to add for this task and dataset
    # \li \a publishPostfix    Postfix for publish name
    # \li \a dataVersionAppend String to append to Dataset's dataVersion for the Workflow's of this task
    # \li \a dbs               Which DBS instance to use (if not default)
    def __init__(self, outputPath=None, **kwargs):
        self.outputPath = outputPath
        self.options = ["njobsIn", "njobsOut",
                        "neventsPerJobIn", "neventsPerJobOut",
                        "nlumisPerJobIn", "nlumisPerJobOut",
                        "triggerOR", "triggerThrow",
                        "crabLines", "args", "publishPostfix",
                        "dataVersionAppend", "dbs"]

        args = {}
        args.update(kwargs)
        for option in self.options:
            value = None
            if option in args:
                value = args[option]
                del args[option]
            setattr(self, option, value)

        # Any remaining argument is an error
        if len(args) >= 1:
            raise Exception("Incorrect arguments for TaskDef.__init__(): %s" % ", ".join(args.keys()))

    ## Update parameters from another TaskDef object
    #
    # \param taskDef  Another  TaskDef object
    #
    # Only non-None values are copied from taskDef.
    def update(self, taskDef):
        for a in ["outputPath"] + self.options:
            selfVal = getattr(self, a)
            val = getattr(taskDef, a)
            if val is not None:
                if a == "args" and selfVal is not None:
                    getattr(self, a).update(val)
                else:
                    setattr(self, a, val)

    def setArg(self, name, value):
        if self.args is None:
            self.args = {name: value}
        else:
            self.args[name] = value

## Update task definition dictionary from another dictionary
#
# \param oldDefinitions   Dictionary from dataset names to TaskDef objects
# \param newDefinitions   Dictionary from dataset names to TaskDef objects
# \param workflowName     Name of the current workflow (for error message only)
#
# Updates the TaskDefs in \a oldDefinitions with the ones in \a
# newDefinitions with the same dataset name. Removes TaskDefs from \a
# oldDefinitions for those datasets which do not have an entry in \a
# newDefinitions.
def updateTaskDefinitions(oldDefinitions, newDefinitions, workflowName=""):
    newDefinitions_copy = {}
    newDefinitions_copy.update(newDefinitions)
    names = oldDefinitions.keys()
    for name in names:
        if name in newDefinitions:
            oldDefinitions[name].update(newDefinitions[name])
            del newDefinitions_copy[name]
        else:
            del oldDefinitions[name]

    if len(newDefinitions_copy) > 0:
        keys = newDefinitions_copy.keys()
        keys.sort()
        raise Exception("No existing task definitions for workflow %s and datasets %s" % (workflowName, ", ".join(keys)))

    return oldDefinitions
