## \package dataset
# Dataset utilities and classes
#
# This package contains classes and utilities for dataset management.
# There are also some functions and classes not directly related to
# dataset management, but are placed here due to some dependencies.

import glob, os, sys, re
import math
import copy
import StringIO
import hashlib

import ROOT

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.aux as aux
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.pileupReweightedAllEvents as pileupReweightedAllEvents


# era name -> list of era parts in data dataset names
_dataEras = {
    "Run2011A": ["_2011A_"],
    "Run2011B": ["_2011B_"],
    "Run2011AB": ["_2011A_", "_2011B_"],
    "Run2012A": ["_2012A_"],
    "Run2012B": ["_2012B_"],
    "Run2012C": ["_2012C_"],
    "Run2012D": ["_2012D_"],
    "Run2012AB": ["_2012A_", "_2012B_"],
    "Run2012ABC": ["_2012A_", "_2012B_", "_2012C_"],
    "Run2012ABCD": ["_2012A_", "_2012B_", "_2012C_", "_2012D_"],
}

## Construct DatasetManager from a list of MultiCRAB directory names.
# 
# \param multiDirs   List of strings or pairs of strings of the MultiCRAB
#                    directories (relative to the working directory). If
#                    the item of the list is pair of strings, the first
#                    element is the directory, and the second element is
#                    the postfix for the dataset names from that directory.
# \param kwargs      Keyword arguments (forwarded to getDatasetsFromMulticrabCfg())
#
# \return DatasetManager object
def getDatasetsFromMulticrabDirs(multiDirs, **kwargs):
    if "cfgfile" in kwargs:
        raise Exception("'cfgfile' keyword argument not allowed")
    if "namePostfix" in kwargs:
        raise Exception("'namePostfix' keyword argument not allowed")

    datasets = DatasetManager()
    for d in multiDirs:
        if isinstance(d, str):
            dset = getDatasetsFromMulticrabCfg(directory=d, **kwargs)
        else:
            dset = getDatasetsFromMulticrabCfg(directory=d[0], namePostfix=d[1], **kwargs)
        datasets.extend(dset)

    return datasets

## Construct DatasetManager from a multicrab.cfg.
#
# \param kwargs   Keyword arguments (see below) 
#
# All keyword arguments are forwarded to readFromMulticrabCfg.
#
# All keyword arguments <b>except</b> the ones below are forwarded to
# DatasetManagerCreator.createDatasetManager()
# \li \a directory
# \li \a cfgfile
# \li \a excludeTasks
# \li \a includeOnlyTasks
# \li \a namePostfix
#
# \return DatasetManager object
# 
# \see dataset.readFromMulticrabCfg
def getDatasetsFromMulticrabCfg(**kwargs):
    _args = copy.copy(kwargs)
    for argName in ["directory", "cfgfile", "excludeTasks", "includeOnlyTasks", "namePostfix"]:
        try:
            del _args[argName]
        except KeyError:
            pass

    managerCreator = readFromMulticrabCfg(**kwargs)
    return managerCreator.createDatasetManager(**_args)

## Construct DatasetManagerConstructor from a multicrab.cfg.
#
# \param kwargs   Keyword arguments (see below) 
#
# <b>Keyword arguments</b>
# \li \a opts              Optional OptionParser object. Should have options added with addOptions() and multicrab.addOptions().
# \li \a directory         Directory where to look for \a cfgfile.
# \li \a cfgfile           Path to the multicrab.cfg file (for default, see multicrab.getTaskDirectories())
# \li \a excludeTasks      String, or list of strings, to specify regexps.
#                          If a dataset name matches to any of the
#                          regexps, Dataset object is not constructed for
#                          that. Conflicts with \a includeOnlyTasks
# \li \a includeOnlyTasks  String, or list of strings, to specify
#                          regexps. Only datasets whose name matches
#                          to any of the regexps are kept. Conflicts
#                          with \a excludeTasks.
# \li Rest are forwarded to readFromCrabDirs()
#
# \return DatasetManagerCreator object
# 
# The section names in multicrab.cfg are taken as the dataset names
# in the DatasetManager object.
def readFromMulticrabCfg(**kwargs):
    opts = kwargs.get("opts", None)
    taskDirs = []
    dirname = ""
    if "directory" in kwargs or "cfgfile" in kwargs:
        _args = {}
        if "directory" in kwargs:
            dirname = kwargs["directory"]
            _args["directory"] = dirname
        if "cfgfile" in kwargs:
            _args["filename"] = kwargs["cfgfile"]
            dirname = os.path.dirname(os.path.join(dirname, kwargs["cfgfile"]))
        taskDirs = multicrab.getTaskDirectories(opts, **_args)
    else:
        taskDirs = multicrab.getTaskDirectories(opts)

    if "excludeTasks" in kwargs and "includeOnlyTasks" in kwargs:
        raise Exception("Only one of 'excludeTasks' or 'includeOnlyTasks' is allowed for getDatasetsFromMulticrabCfg")

    def getRe(arg):
        if isinstance(arg, basestring):
            arg = [arg]
        return [re.compile(a) for a in arg]
    
    if "excludeTasks" in kwargs:
        exclude = getRe(kwargs["excludeTasks"])
        tmp = []
        for task in taskDirs:
            found = False
            for e_re in exclude:
                if e_re.search(os.path.basename(task)):
                    found = True
                    break
            if found:
                continue
            tmp.append(task)
        taskDirs = tmp
    if "includeOnlyTasks" in kwargs:
        include = getRe(kwargs["includeOnlyTasks"])
        tmp = []
        for task in taskDirs:
            found = False
            for i_re in include:
                if i_re.search(os.path.basename(task)):
                    found = True
                    break
            if found:
                tmp.append(task)
        taskDirs = tmp

    managerCreator = readFromCrabDirs(taskDirs, baseDirectory=dirname, **kwargs)
    return managerCreator

## Construct DatasetManager from a list of CRAB task directory names.
# 
# \param taskdirs     List of strings for the CRAB task directories (relative
#                     to the working directory), forwarded to readFromCrabDirs()
# \param kwargs       Keyword arguments (see below)
#
# All keyword arguments are forwarded to readFromCrabDirs().
#
# All keyword arguments <b>except</b> the ones below are forwarded to
# DatasetManagerCreator.createDatasetManager()
# \li \a namePostfix
#
# \see readFromCrabDirs()
def getDatasetsFromCrabDirs(taskdirs, **kwargs):
    _args = copy.copy(kwargs)
    for argName in ["namePostfix"]:
        try:
            del _args[argName]
        except KeyError:
            pass
    
    managerCreator = readFromCrabDirs(taskdirs, **kwargs)
    return managerCreator.createDatasetManager(**_args)


## Construct DatasetManagerCreator from a list of CRAB task directory names.
# 
# \param taskdirs     List of strings for the CRAB task directories (relative
#                     to the working directory)
# \param kwargs       Keyword arguments (see below) 
# 
# <b>Keyword arguments</b>, all are also forwarded to readFromRootFiles()
# \li \a opts         Optional OptionParser object. Should have options added with addOptions().
# \li \a namePostfix  Postfix for the dataset names (default: '')
#
# \return DatasetManagerCreator object
# 
# The basename of the task directories are taken as the dataset names
# in the DatasetManagerCreator object (e.g. for directory '../Foo',
# 'Foo' will be the dataset name)
def readFromCrabDirs(taskdirs, **kwargs):
    inputFile = None
    if "opts" in kwargs:
        opts = kwargs["opts"]
        inputFile = opts.input
    else:
        inputFile = _optionDefaults["input"]
    postfix = kwargs.get("namePostfix", "")

    dlist = []
    noFiles = False
    for d in taskdirs:
        files = glob.glob(os.path.join(d, "res", inputFile))
        if len(files) == 0:
            print >> sys.stderr, "Ignoring dataset %s: no files matched to '%s' in task directory %s" % (d, inputFile, os.path.join(d, "res"))
            noFiles = True
            continue

        dlist.append( (os.path.basename(d)+postfix, files) )

    if noFiles:
        print >> sys.stderr, ""
        print >> sys.stderr, "  There were datasets without files. Have you merged the files with hplusMergeHistograms.py?"
        print >> sys.stderr, ""
        if len(dlist) == 0:
            raise Exception("No datasets. Have you merged the files with hplusMergeHistograms.py?")

    if len(dlist) == 0:
        raise Exception("No datasets from CRAB task directories %s" % ", ".join(taskdirs))

    return readFromRootFiles(dlist, **kwargs)

## Construct DatasetManager from a list of CRAB task directory names.
# 
# \param rootFileList  List of (\a name, \a filenames) pairs (\a name
#                      should be string, \a filenames can be string or
#                      list of strings). \a name is taken as the
#                      dataset name, and \a filenames as the path(s)
#                      to the ROOT file(s).
# \param kwargs        Keyword arguments, forwarded to readFromRootFiles() and dataset.Dataset.__init__()
#
# \return DatasetManager object
def getDatasetsFromRootFiles(rootFileList, **kwargs):
    managerCreator = readFromRootFiles(rootFileList, **kwargs)
    return managerCreator.createDatasetManager(**kwargs)

## Construct DatasetManagerCreator from a list of CRAB task directory names.
# 
# \param rootFileList  List of (\a name, \a filenames) pairs (\a name
#                      should be string, \a filenames can be string or
#                      list of strings). \a name is taken as the
#                      dataset name, and \a filenames as the path(s)
#                      to the ROOT file(s). Forwarded to DatasetManagerCreator.__init__()
# \param kwargs        Keyword arguments (see below), all forwarded to DatasetManagerCreator.__init__()
#
# <b>Keyword arguments</b>
# \li \a opts          Optional OptionParser object. Should have options added with addOptions().
#
# \return DatasetManagerCreator object
#
# If \a opts exists, and the \a opts.listAnalyses is set to True, list
# all available analyses (with DatasetManagerCreator.printAnalyses()),
# and exit.
def readFromRootFiles(rootFileList, **kwargs):
    creator = DatasetManagerCreator(rootFileList, **kwargs)
    if "opts" in kwargs and kwargs["opts"].listAnalyses:
        creator.printAnalyses()
        sys.exit(0)
    return creator
        

## Default command line options
_optionDefaults = {
    "input": "histograms-*.root",
}

## Add common dataset options to OptionParser object.
#
# \param parser   OptionParser object
def addOptions(parser, analysisName=None, searchMode=None, dataEra=None, optimizationMode=None, systematicVariation=None):
    parser.add_option("-i", dest="input", type="string", default=_optionDefaults["input"],
                      help="Pattern for input root files (note: remember to escape * and ? !) (default: '%s')" % _optionDefaults["input"])
    parser.add_option("-f", dest="files", type="string", action="append", default=[],
                      help="Give input ROOT files explicitly, if these are given, multicrab.cfg is not read and -d/-i parameters are ignored")
    parser.add_option("--analysisName", dest="analysisName", type="string", default=analysisName,
                      help="Override default analysisName (%s, plot script specific)" % analysisName)
    parser.add_option("--searchMode", dest="searchMode", type="string", default=searchMode,
                      help="Override default searchMode (%s, plot script specific)" % searchMode)
    parser.add_option("--dataEra", dest="dataEra", type="string", default=dataEra,
                      help="Override default dataEra (%s, plot script specific)" % dataEra)
    parser.add_option("--optimizationMode", dest="optimizationMode", type="string", default=optimizationMode,
                      help="Override default optimizationMode (%s, plot script specific)" % optimizationMode)
    parser.add_option("--systematicVariation", dest="systematicVariation", type="string", default=systematicVariation,
                      help="Override default systematicVariation (%s, plot script specific)" % systematicVariation)
    parser.add_option("--list", dest="listAnalyses", action="store_true", default=False,
                      help="List available analysis name information, and quit.")
    parser.add_option("--counterDir", "-c", dest="counterDir", type="string", default=None,
                      help="TDirectory name containing the counters, relative to the analysis directory (default: analysisDirectory+'/counters')")


## Represents counter count value with uncertainty.
class Count:
    ## Constructor
    def __init__(self, value, uncertainty=0.0, systUncertainty=0.0):
        self._value = value
        self._uncertainty = uncertainty
        self._systUncertainty = systUncertainty

    def copy(self):
        return Count(self._value, self._uncertainty, self._systUncertainty)

    def clone(self):
        return self.copy()

    def value(self):
        return self._value

    def uncertainty(self):
        return self._uncertainty

    def uncertaintyLow(self):
        return self.uncertainty()

    def uncertaintyHigh(self):
        return self.uncertainty()

    def systUncertainty(self):
        return self._systUncertainty

    ## self = self + count
    def add(self, count):
        self._value += count._value
        self._uncertainty = math.sqrt(self._uncertainty**2 + count._uncertainty**2)
        self._systUncertainty = math.sqrt(self._systUncertainty**2 + count._systUncertainty**2)

    ## self = self - count
    def subtract(self, count):
        self.add(Count(-count._value, count._uncertainty, count._systUncertainty))

    ## self = self * count
    def multiply(self, count):
        self._systUncertainty = math.sqrt( (count._value * self._systUncertainty)**2 +
                                       (self._value  * count._systUncertainty)**2 )
        self._uncertainty = math.sqrt( (count._value * self._uncertainty)**2 +
                                       (self._value  * count._uncertainty)**2 )
        self._value = self._value * count._value

    ## self = self / count
    def divide(self, count):
        self._systUncertainty = math.sqrt( (self._systUncertainty / count._value)**2 +
                                       (self._value*count._systUncertainty / (count._value**2) )**2 )
        self._uncertainty = math.sqrt( (self._uncertainty / count._value)**2 +
                                       (self._value*count._uncertainty / (count._value**2) )**2 )
        self._value = self._value / count._value

    ## \var _value
    # Value of the count
    ## \var _uncertainty
    # Statistical uncertainty of the count
    ## \var _systUncertainty
    # Systematic uncertainty of the count

## Represents counter count value with asymmetric uncertainties.
class CountAsymmetric:
    def __init__(self, value, uncertaintyLow, uncertaintyHigh):
        self._value = value
        self._uncertaintyLow = uncertaintyLow
        self._uncertaintyHigh = uncertaintyHigh

    def clone(self):
        return CountAsymmetric(self._value, self._uncertaintyLow, self._uncertaintyHigh)

    def value(self):
        return self._value

    def uncertainty(self):
        return max(self._uncertaintyLow, self._uncertaintyHigh)

    def uncertaintyLow(self):
        return self._uncertaintyLow

    def uncertaintyHigh(self):
        return self._uncertaintyHigh

    def multiply(self, count):
        value = count.value()
        if count.uncertainty() != 0:
            raise Exception("Can't multiply CountAsymmetric (%f, %f, %f) with Count (%f, %f) with non-zero uncertainty" % (self._value, self._uncertaintyLow, self._uncertaintyHigh, count.value(), count.uncertainty()))
        self._value *= value
        self._uncertaintyLow *= value
        self._uncertaintyHigh *= value

    ## \var _value
    # Value of the count
    ## \var _uncertaintyLow
    # Lower uncertainty of the count (-)
    ## \var _uncertaintyHigh
    # Upper uncertainty of the count (+)

def divideBinomial(countPassed, countTotal):
    p = countPassed.value()
    t = countTotal.value()
    value = p / float(t)
    p = int(p)
    t = int(t)
    errUp = ROOT.TEfficiency.ClopperPearson(t, p, 0.683, True)
    errDown = ROOT.TEfficiency.ClopperPearson(t, p, 0.683, False)
    return CountAsymmetric(value, value-errDown, errUp-value)

## Transform histogram (TH1) to a list of (name, Count) pairs.
#
# The name is taken from the x axis label and the count is Count
# object with value and (statistical) uncertainty.
def _histoToCounter(histo):
    ret = []

    for bin in xrange(1, histo.GetNbinsX()+1):
        ret.append( (histo.GetXaxis().GetBinLabel(bin),
                     Count(float(histo.GetBinContent(bin)),
                           float(histo.GetBinError(bin)))) )

    return ret

## Transform a list of (name, Count) pairs to a histogram (TH1)
def _counterToHisto(name, counter):
    histo = ROOT.TH1F(name, name, len(counter), 0, len(counter))
    histo.Sumw2()

    bin = 1
    for name, count in counter:
        histo.GetXaxis().SetBinLabel(bin, name)
        histo.SetBinContent(bin, count.value())
        histo.SetBinError(bin, count.uncertainty())
        bin += 1

    return histo

## Transform histogram (TH1) to a list of values
def histoToList(histo):
    return [histo.GetBinContent(bin) for bin in xrange(1, histo.GetNbinsX()+1)]


## Transform histogram (TH1) to a dictionary.
#
# The key is taken from the x axis label, and the value is the bin
# content.
def _histoToDict(histo):
    ret = {}

    for bin in xrange(1, histo.GetNbinsX()+1):
        ret[histo.GetXaxis().GetBinLabel(bin)] = histo.GetBinContent(bin)

    return ret

## Integrate TH1 to a Count
def histoIntegrateToCount(histo):
    count = Count(0, 0)
    if histo is None:
        return count

    for bin in xrange(0, histo.GetNbinsX()+2):
        count.add(Count(histo.GetBinContent(bin), histo.GetBinError(bin)))
    return count

## Rescales info dictionary.
# 
# Assumes that d has a 'control' key for a numeric value, and then
# normalizes all items in the dictionary such that the 'control'
# becomes one.
# 
# The use case is to have a dictionary from _histoToDict() function,
# where the original histogram is merged from multiple jobs. It is
# assumed that each histogram as a one bin with 'control' label, and
# the value of this bin is 1 for each job. Then the bin value for
# the merged histogram tells the number of jobs. Naturally the
# scheme works correctly only if the histograms from jobs are
# identical, and hence is appropriate only for dataset-like
# information.
def _rescaleInfo(d):
    factor = 1/d["control"]

    ret = {}
    for k, v in d.iteritems():
        ret[k] = v*factor

    return ret


## Normalize TH1/TH2/TH3 to unit area.
# 
# \param h   TH1/TH2/TH3 histogram
# 
# \return Normalized histogram (same as the argument object, i.e. no copy is made).
def _normalizeToOne(h):
    if isinstance(h, ROOT.TH3):
        integral = h.Integral(0, h.GetNbinsX()+1, 0, h.GetNbinsY()+1, 0, h+GetNbinsZ())
    elif isinstance(h, ROOT.TH2):
        integral = h.Integral(0, h.GetNbinsX()+1, 0, h.GetNbinsY()+1)
    else:
        integral = h.Integral(0, h.GetNbinsX()+1)
    if integral == 0:
        return h
    else:
        return _normalizeToFactor(h, 1.0/integral)

## Scale TH1 with a given factor.
# 
# \param h   TH1 histogram
# \param f   Scale factor
# 
# TH1.Sumw2() is called before the TH1.Scale() in order to scale the
# histogram errors correctly.
def _normalizeToFactor(h, f):
    backup = ROOT.gErrorIgnoreLevel
    ROOT.gErrorIgnoreLevel = ROOT.kError
    h.Sumw2() # errors are also scaled after this call 
    ROOT.gErrorIgnoreLevel = backup
    h.Scale(f)
    return h


## Helper function for merging/stacking a set of datasets.
# 
# \param datasetList  List of all Dataset objects to consider
# \param nameList     List of the names of Dataset objects to merge/stack
# \param task         String to identify merge/stack task (can be 'stack' or 'merge')
# 
# \return a triple of:
# - list of selected Dataset objects
# - list of non-selected Dataset objects
# - index of the first selected Dataset object in the original list
#   of all Datasets
# 
# The Datasets to merge/stack are selected from the list of all
# Datasets, and it is checked that all of them are either data or MC
# (i.e. merging/stacking of data and MC datasets is forbidden).
# """
def _mergeStackHelper(datasetList, nameList, task):
    if not task in ["stack", "merge"]:
        raise Exception("Task can be either 'stack' or 'merge', was '%s'" % task)

    selected = []
    notSelected = []
    firstIndex = None
    dataCount = 0
    mcCount = 0

    for i, d in enumerate(datasetList):
        if d.getName() in nameList:
            selected.append(d)
            if firstIndex == None:
                firstIndex = i
            if d.isData():
                dataCount += 1
            elif d.isMC():
                mcCount += 1
            else:
                raise Exception("Internal error!")
        else:
            notSelected.append(d)

    if dataCount > 0 and mcCount > 0:
        raise Exception("Can not %s data and MC datasets!" % task)

    if len(selected) != len(nameList):
        dlist = nameList[:]
        for d in selected:
            ind = dlist.index(d.getName())
            del dlist[ind]
        print >> sys.stderr, "WARNING: Tried to %s '"%task + ", ".join(dlist) +"' which don't exist"

    return (selected, notSelected, firstIndex)


## Helper class for obtaining histograms from TTree
#
# This class provides an easy way to get a histogram from a TTree. It
# is inteded to be used with dataset.Dataset.getDatasetRootHisto()
# such that instead of giving the name of the histogram, an object of
# this class is given instead. dataset.Dataset.getDatasetRootHisto()
# will then call the draw() method of this class for actually
# producing the histogram.
#
# TreeDraw objects can easily be cloned from existing TreeDraw object
# with the clone() method. This method allows overriding the
# parameters given in constructor.
#
# Note that TreeDraw does not hold any results or TTree objects, only
# the recipe to produce a histogram from a TTree.
class TreeDraw:
    ## Constructor
    #
    # \param tree       Path to the TTree object in a file
    # \param varexp     Expression for the variable, if given it should also include the histogram name and binning explicitly.
    # \param selection  Draw only those entries passing this selection
    # \param weight     Weight the entries with this weight
    # \param binLabelsX X-axis bin labels (optional)
    # \param binLabelsY Y-axis bin labels (optional)
    # \param binLabelsZ Z-axis bin labels (optional)
    #
    # If varexp is not given, the number of entries passing selection
    # is counted (ignoring weight). In this case the returned TH1 has
    # 1 bin, which contains the event count and the uncertainty of the
    # event count (calculated as sqrt(N)).
    def __init__(self, tree, varexp="", selection="", weight="", binLabelsX=None, binLabelsY=None, binLabelsZ=None):
        self.tree = tree
        self.varexp = varexp
        self.selection = selection
        self.weight = weight

        self.binLabelsX = binLabelsX
        self.binLabelsY = binLabelsY
        self.binLabelsZ = binLabelsZ

    ## Clone a TreeDraw
    #
    # <b>Keyword arguments</b> are the same as for the constructor (__init__())
    #
    # If any of the values of the keyword arguments is a function (has
    # attribute __call__), the function is called with the current
    # value as an argument, and the return value is assigned to the
    # corresponding name.
    def clone(self, **kwargs):
        args = {"tree": self.tree,
                "varexp": self.varexp,
                "selection": self.selection,
                "weight": self.weight,
                "binLabelsX": self.binLabelsX,
                "binLabelsY": self.binLabelsY,
                "binLabelsZ": self.binLabelsZ,
                }
        args.update(kwargs)

        # Allow modification functions
        for name, value in args.items():
            if hasattr(value, "__call__"):
                args[name] = value(getattr(self, name))

        return TreeDraw(**args)

    ## Prodouce TH1 from a file
    #
    # \param dataset      Dataset, the output TH1 contains the dataset name
    #                     in the histogram name. Mainly needed for compatible interface with
    #                     dataset.TreeDrawCompound
    def draw(self, dataset):
        if self.varexp != "" and not ">>" in self.varexp:
            raise Exception("varexp should include explicitly the histogram binning (%s)"%self.varexp)

        selection = self.selection
        if len(self.weight) > 0:
            if len(selection) > 0:
                selection = "%s * (%s)" % (self.weight, selection)
            else:
                selection = self.weight

        (tree, treeName) = dataset.createRootChain(self.tree)
        if tree == None:
            raise Exception("No TTree '%s' in file %s" % (treeName, dataset.getRootFile().GetName()))

        if self.varexp == "":
            nentries = tree.GetEntries(selection)
            h = ROOT.TH1F("nentries", "Number of entries by selection %s"%selection, 1, 0, 1)
            h.SetDirectory(0)
            if len(self.weight) > 0:
                h.Sumw2()
            h.SetBinContent(1, nentries)
            h.SetBinError(1, math.sqrt(nentries))
            return h

        varexp = self.varexp
        
        # e to have TH1.Sumw2() to be called before filling the histogram
        # goff to not to draw anything on the screen
        opt = ""
        if len(self.weight) > 0:
            opt = "e "
        option = opt+"goff"
        nentries = tree.Draw(varexp, selection, option)
        if nentries < 0:
            raise Exception("Error when calling TTree.Draw with the following parameters for dataset %s, nentries=%d\ntree:       %s\nvarexp:     %s\nselection:  %s\noption:     %s" % (dataset.getName(), nentries, treeName, varexp, selection, option))
        h = tree.GetHistogram()
        if h == None: # need '==' to compare null TH1
            print >>sys.stderr, "WARNING: TTree.Draw with the following parameters returned null histogram for dataset %s (%d entries)\ntree:       %s\nvarexp:     %s\nselection:  %s\noption:     %s" % (dataset.getName(), nentries, treeName, varexp, selection, option)
            return None

        h.SetName(dataset.getName()+"_"+h.GetName())
        h.SetDirectory(0)

        for axis in ["X", "Y", "Z"]:
            if getattr(self, "binLabels"+axis) is not None:
                labels = getattr(self, "binLabels"+axis)
                nlabels = len(labels)
                nbins = getattr(h, "GetNbins"+axis)()
                if nlabels != nbins:
                    raise Exception("Trying to set %s bin labels, bot %d labels, histogram has %d bins. \ntree:       %s\nvarexp:     %s\nselection:  %s\noption:     %s" %
                                    (axis, nlabels, nbins, self.tree, varexp, selection, option))
                axisObj = getattr(h, "Get"+axis+"axis")()
                for i, label in enumerate(labels):
                    axisObj.SetBinLabel(i+1, label)

        return h


    ## \var tree
    # Path to the TTree object in a file
    ## \var varexp
    # Expression for the variable
    ## \var selection
    # Draw only those entries passing this selection
    ## \var weight
    # Weight the entries with this weight

## Helper class for running code for selected TTree entries
#
# A function is given to the constructor, the function is called for
# each TTree entry passing the selection. The TTree object is given as
# a parameter, leaf/branch data can then be read from it.
#
# Main use case: producing pickEvents list from a TTree
class TreeScan:
    ## Constructor
    #
    # \param tree       Path to the TTree object in a file
    # \param function   Function to call for each TTree entry
    # \param selection  Select only these TTree entries
    def __init__(self, tree, function, selection=""):
        self.tree = tree
        self.function = function
        self.selection = selection

    def clone(self, **kwargs):
        args = {"tree": self.tree,
                "function": self.function,
                "selection": self.selection}
        args.update(kwargs)
        return TreeScan(**args)

    ## Process TTree
    #
    # \param datasetName  Dataset object. Only needed for compatible interface with
    #                     dataset.TreeDrawCompound
    def draw(self, dataset):
        rootFile = dataset.getRootFile()
        tree = rootFile.Get(self.tree)
        if tree == None:
            raise Exception("No TTree '%s' in file %s" % (self.tree, rootFile.GetName()))

        tree.Draw(">>elist", self.selection)
        elist = ROOT.gDirectory.Get("elist")
        for ientry in xrange(elist.GetN()):
            tree.GetEntry(elist.GetEntry(ientry))
            self.function(tree)

    ## \var tree
    # Path to the TTree object in a file
    ## \var function
    # Function to call for each TTree entry
    ## \var selection
    # Select only these TTree entries

## Provides ability to have separate dataset.TreeDraws for different datasets
#
# One specifies a default dataset.TreeDraw, and the exceptions for that with a
# map from string to dataset.TreeDraw.
class TreeDrawCompound:
    ## Constructor
    #
    # \param default     Default dataset.TreeDraw
    # \param datasetMap  Dictionary for the overriding dataset.TreeDraw objects
    #                    containing dataset names as keys, and TreeDraws as values.
    def __init__(self, default, datasetMap={}):
        self.default = default
        self.datasetMap = datasetMap

    ## Add a new dataset specific dataset.TreeDraw
    #
    # \param datasetName  Name of the dataset
    # \param treeDraw     dataset.TreeDraw object to add
    def add(self, datasetName, treeDraw):
        self.datasetMap[datasetName] = treeDraw

    ## Produce TH1
    #
    # \param datasetName  Dataset object
    #
    # The dataset.TreeDraw for which the call is forwarded is searched from
    # the datasetMap with the datasetName. If found, that object is
    # used. If not found, the default TreeDraw is used.
    def draw(self, dataset):
        h = None
        datasetName = dataset.getName()
        if datasetName in self.datasetMap:
            #print "Dataset %s in datasetMap" % datasetName, self.datasetMap[datasetName].selection
            h = self.datasetMap[datasetName].draw(dataset)
        else:
            #print "Dataset %s with default" % datasetName, self.default.selection
            h = self.default.draw(dataset)
        return h

    ## Clone
    #
    # <b>Keyword arguments</b> are the same as for the clone() method
    # of the contained TreeDraw objects. The new TreeDrawCompoung is
    # constructed such that the default and dataset-specific TreeDraws
    # are cloned with the given keyword arguments.
    def clone(self, **kwargs):
        ret = TreeDrawCompound(self.default.clone(**kwargs))
        for name, td in self.datasetMap.iteritems():
            ret.datasetMap[name] = td.clone(**kwargs)
        return ret

    ## \var default
    # Default dataset.TreeDraw
    ## \var datasetMap
    # Dictionary for the overriding dataset.TreeDraw objects
    # containing dataset names as keys, and TreeDraws as values.

def _treeDrawToNumEntriesSingle(treeDraw):
    var = treeDraw.weight
    if var == "":
        var = treeDraw.selection
    if var != "":
        var += ">>dist(1,0,2)" # the binning is arbitrary, as the under/overflow bins are counted too
    # if selection and weight are "", TreeDraw.draw() returns a histogram with the number of entries
    return treeDraw.clone(varexp=var)

## Maybe unnecessary function?
#
# Seems to be used only from DatasetQCDData class, which was never
# finished.
def treeDrawToNumEntries(treeDraw):
    if isinstance(treeDraw, TreeDrawCompound):
        td = TreeDrawCompound(_treeDrawToNumEntriesSingle(treeDraw.default))
        for name, td2 in treeDraw.datasetMap.iteritems():
            td.add(name, _treeDrawToNumEntriesSingle(td2))
        return td
    else:
        return _treeDrawToNumEntriesSingle(treeDraw)

## Base class for DatasetRootHisto classes (wrapper for TH1 histogram and the originating Dataset)
# 
# The derived class must implement
# _normalizedHistogram()
# which should return the cloned and normalized TH1
#
# The wrapper holds the normalization of the histogram. User should
# set the current normalization scheme with the normalize* methods,
# and then get a clone of the original histogram, which is then
# normalized according to the current scheme.
#
# This makes the class very flexible with respect to the many
# possible normalizations user could want to apply within a plot
# script. The first use case was MC counters, which could be printed
# first normalized to the luminosity of the data, and also
# normalized to the cross section.
#
# The histogram wrapper classes also abstract the signel histogram, and
# mergeddata and MC histograms behind a common interface.
class DatasetRootHistoBase:
    def __init__(self, dataset):
        self.dataset = dataset
        self.name = dataset.getName()
        self.multiplication = None

    def getDataset(self):
        return self.dataset

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def isData(self):
        return self.dataset.isData()

    def isMC(self):
        return self.dataset.isMC()

    ## Get a clone of the wrapped histogram normalized as requested.
    def getHistogram(self):
        h = self._normalizedHistogram()
        if h is None:
            return h

        if self.multiplication != None:
            h = _normalizeToFactor(h, self.multiplication)
        return h

    ## Scale the histogram bin values with a value.
    # 
    # \param value    Value to multiply with
    # 
    # h = h*value
    def scale(self, value):
        if self.multiplication == None:
            self.multiplication = value
        else:
            self.multiplication *= value

    ## \var dataset
    # dataset.Dataset object where the histogram originates
    ## \var name
    # Name of the histogram (default is dataset name)
    ## \var multiplication
    # Multiplication factor to be applied after normalization (if None, not applied)

## Wrapper for a single TH1 histogram and the corresponding Dataset.
class DatasetRootHisto(DatasetRootHistoBase):
    ## Constructor.
    # 
    # \param histo    TH1 histogram
    # \param dataset  Corresponding Dataset object
    # 
    # Sets the initial normalization to 'none'
    def __init__(self, histo, dataset):
        DatasetRootHistoBase.__init__(self, dataset)
        self.histo = histo
        self.normalization = "none"

    ## Get list of the bin labels of the histogram.
    def getBinLabels(self):
        if self.histo is None:
            return None
        return [x[0] for x in _histoToCounter(self.histo)]

    def forEach(self, function, datasetRootHisto1=None):
        if datasetRootHisto1 != None:
            if not isinstance(datasetRootHisto1, DatasetRootHisto):
                raise Exception("datasetRootHisto1 must be of the type DatasetRootHisto")
            return [function(self, datasetRootHisto1)]
        else:
            return [function(self)]

    ## Modify the TH1 with a function
    #
    # \param function              Function taking the original TH1, and returning a new TH1. If newDatasetRootHisto is specified, function must take some other DatasetRootHisto object as an input too
    # \param newDatasetRootHisto   Optional, the other DatasetRootHisto object
    #
    # Needed for appending rows to counters from TTree, and for embedding normalization
    def modifyRootHisto(self, function, newDatasetRootHisto=None):
        if newDatasetRootHisto != None:
            if not isinstance(newDatasetRootHisto, DatasetRootHisto):
                raise Exception("newDatasetRootHisto must be of the type DatasetRootHisto")
            self.histo = function(self.histo, newDatasetRootHisto.histo)
        else:
            self.histo = function(self.histo)

    ## Return normalized clone of the original TH1
    def _normalizedHistogram(self):
        if self.histo is None:
            return None

        # Always return a clone of the original
        h = self.histo.Clone()
        h.SetDirectory(0)
        h.SetName(h.GetName()+"_cloned")
        if self.normalization == "none":
            return h
        elif self.normalization == "toOne":
            return _normalizeToOne(h)

        # We have to normalize to cross section in any case
        h = _normalizeToFactor(h, self.dataset.getNormFactor())
        if self.normalization == "byCrossSection":
            return h
        elif self.normalization == "toLuminosity":
            return _normalizeToFactor(h, self.luminosity)
        else:
            raise Exception("Internal error")

    ## Set the normalization scheme to 'to one'.
    #
    # The histogram is normalized to unit area.
    def normalizeToOne(self):
        self.normalization = "toOne"

    ## Set the current normalization scheme to 'by cross section'.
    #
    # The histogram is normalized to the cross section of the
    # corresponding dataset. The normalization can be applied only
    # to MC histograms.
    def normalizeByCrossSection(self):
        if self.dataset.isData():
            raise Exception("Can't normalize data histogram by cross section")
        self.normalization = "byCrossSection"

    ## Set the current normalization scheme to 'to luminosity'.
    #
    # \param lumi   Integrated luminosity in pb^-1 to normalize to
    #
    # The histogram is normalized first normalized to the cross
    # section of the corresponding dataset, and then to a given
    # luminosity. The normalization can be applied only to MC
    # histograms.
    def normalizeToLuminosity(self, lumi):
        if self.dataset.isData():
            raise Exception("Can't normalize data histogram to luminosity")

        self.normalization = "toLuminosity"
        self.luminosity = lumi
    
    ## \var histo
    # Holds the unnormalized ROOT histogram (TH1)
    ## \var normalization
    # String representing the current normalization scheme


## Base class for merged data/Mc histograms and the corresponding datasets
class DatasetRootHistoCompoundBase(DatasetRootHistoBase):
    ## Constructor.
    # 
    # \param histoWrappers   List of dataset.DatasetRootHisto objects to merge
    # \param mergedDataset   The corresponding dataset.DatasetMerged object
    def __init__(self, histoWrappers, mergedDataset):
        DatasetRootHistoBase.__init__(self, mergedDataset)
        self.histoWrappers = histoWrappers
        self.normalization = "none"

    ## Get list of the bin labels of the first of the merged histogram.
    def getBinLabels(self):
        for drh in self.histoWrappers:
            ret = drh.getBinLabels()
            if ret is not None:
                return ret
        return None

   ## Calculate the sum of the histograms (i.e. merge).
   # 
   # Intended to be called from the deriving classes
    def _getSumHistogram(self):
        # Loop until we have a real TH1 (not None)
        hsum = None
        for i, drh in enumerate(self.histoWrappers):
            hsum = drh.getHistogram() # we get a clone
            if hsum is not None:
                break

        for h in self.histoWrappers[i+1:]:
            histo = h.getHistogram()
            if histo.GetNbinsX() != hsum.GetNbinsX():
                raise Exception("Histogram '%s' from datasets '%s' and '%s' have different binnings: %d vs. %d" % (hsum.GetName(), self.histoWrappers[i].getDataset().getName(), h.getDataset().getName(), hsum.GetNbinsX(), histo.GetNbinsX()))

            hsum.Add(histo)
            histo.Delete()
        return hsum

    ## \var histoWrappers
    # List of underlying dataset.DatasetRootHisto objects
    ## \var normalization
    # String representing the current normalization scheme


## Wrapper for a merged TH1 histograms from data and the corresponding Datasets.
#
# The merged data histograms can only be normalized 'to one'.
#
# \see dataset.DatasetRootHisto class.
class DatasetRootHistoMergedData(DatasetRootHistoCompoundBase):
    ## Constructor.
    # 
    # \param histoWrappers   List of dataset.DatasetRootHisto objects to merge
    # \param mergedDataset   The corresponding dataset.DatasetMerged object
    # 
    # The constructor checks that all histoWrappers are data, and
    # are not yet normalized.
    def __init__(self, histoWrappers, mergedDataset):
        DatasetRootHistoCompoundBase.__init__(self, histoWrappers, mergedDataset)
        for h in self.histoWrappers:
            if not h.isData():
                raise Exception("Histograms to be merged must come from data (%s is not data)" % h.getDataset().getName())
            if h.normalization != "none":
                raise Exception("Histograms to be merged must not be normalized at this stage")
            if h.multiplication != None:
                raise Exception("Histograms to be merged must not be multiplied at this stage")

    def isData(self):
        return True

    def isMC(self):
        return False

    def forEach(self, function, datasetRootHisto1=None):
        ret = []
        if datasetRootHisto1 != None:
            if not isinstance(datasetRootHisto1, DatasetRootHistoMergedData):
                raise Exception("datasetRootHisto1 must be of the type DatasetRootHistoMergedData")
            if not len(self.histoWrappers) == len(datasetRootHisto1.histoWrappers):
                raise Exception("len(self.histoWrappers) != len(datasetrootHisto1.histoWrappers), %d != %d" % len(self.histoWrappers), len(datasetRootHisto1.histoWrappers))
            
            for i, drh in enumerate(self.histoWrappers):
                ret.extend(drh.forEach(function, datasetRootHisto1.histoWrappers[i]))
        else:
            for drh in self.histoWrappers:
                ret.extend(drh.forEach(function))
        return ret
        

    ## Modify the TH1 with a function
    #
    # \param function             Function taking the original TH1, and returning a new TH1. If newDatasetRootHisto is specified, function must take some other DatasetRootHisto object as an input too
    # \param newDatasetRootHisto  Optional, the other DatasetRootHisto object, must be the same type and contain same number of DatasetRootHisto objects
    #
    # Needed for appending rows to counters from TTree, and for embedding normalization
    def modifyRootHisto(self, function, newDatasetRootHisto=None):
        if newDatasetRootHisto != None:
            if not isinstance(newDatasetRootHisto, DatasetRootHistoMergedData):
                raise Exception("newDatasetRootHisto must be of the type DatasetRootHistoMergedData")
            if not len(self.histoWrappers) == len(newDatasetRootHisto.histoWrappers):
                raise Exception("len(self.histoWrappers) != len(newDatasetrootHisto.histoWrappers), %d != %d" % len(self.histoWrappers), len(newDatasetRootHisto.histoWrappers))
            
            for i, drh in enumerate(self.histoWrappers):
                drh.modifyRootHisto(function, newDatasetRootHisto.histoWrappers[i])
        else:
            for i, drh in enumerate(self.histoWrappers):
                drh.modifyRootHisto(function)

    ## Set the current normalization scheme to 'to one'.
    #
    # The histogram is normalized to unit area.
    def normalizeToOne(self):
        self.normalization = "toOne"

    ## Merge the histograms and apply the current normalization.
    # 
    # The returned histogram is a clone, so client code can do
    # anything it wishes with it.
    def _normalizedHistogram(self):
        hsum = self._getSumHistogram()
        if hsum is None:
            return None

        if self.normalization == "toOne":
            return _normalizeToOne(hsum)
        else:
            return hsum


## Wrapper for a merged TH1 histograms from MC and the corresponding Datasets.
# 
# See also the documentation of DatasetRootHisto class.
class DatasetRootHistoMergedMC(DatasetRootHistoCompoundBase):
    ## Constructor.
    # 
    # \param histoWrappers   List of dataset.DatasetRootHisto objects to merge
    # \param mergedDataset   The corresponding dataset.DatasetMerged object
    # 
    # The constructor checks that all histoWrappers are MC, and are
    # not yet normalized.
    def __init__(self, histoWrappers, mergedDataset):
        DatasetRootHistoCompoundBase.__init__(self, histoWrappers, mergedDataset)
        for h in self.histoWrappers:
            if not h.isMC():
                raise Exception("Histograms to be merged must come from MC")
            if h.normalization != "none":
                raise Exception("Histograms to be merged must not be normalized at this stage")
            if h.multiplication != None:
                raise Exception("Histograms to be merged must not be multiplied at this stage")

    def isData(self):
        return False

    def isMC(self):
        return True

    def forEach(self, function, datasetRootHisto1=None):
        ret = []
        if datasetRootHisto1 != None:
            if not isinstance(datasetRootHisto1, DatasetRootHistoMergedMC):
                raise Exception("datasetRootHisto1 must be of the type DatasetRootHistoMergedMC")
            if not len(self.histoWrappers) == len(datasetRootHisto1.histoWrappers):
                raise Exception("len(self.histoWrappers) != len(datasetrootHisto1.histoWrappers), %d != %d" % len(self.histoWrappers), len(datasetRootHisto1.histoWrappers))
            
            for i, drh in enumerate(self.histoWrappers):
                ret.extend(drh.forEach(function, datasetRootHisto1.histoWrappers[i]))
        else:
            for drh in self.histoWrappers:
                ret.extend(drh.forEach(function))
        return ret

    ## Modify the TH1 with a function
    #
    # \param function             Function taking the original TH1, and returning a new TH1. If newDatasetRootHisto is specified, function must take some other DatasetRootHisto object as an input too
    # \param newDatasetRootHisto  Optional, the other DatasetRootHisto object, must be the same type and contain same number of DatasetRootHisto objects
    #
    # Needed for appending rows to counters from TTree, and for embedding normalization
    def modifyRootHisto(self, function, newDatasetRootHisto=None):
        if newDatasetRootHisto != None:
            if not isinstance(newDatasetRootHisto, DatasetRootHistoMergedMC):
                raise Exception("newDatasetRootHisto must be of the type DatasetRootHistoMergedMC")
            if not len(self.histoWrappers) == len(newDatasetRootHisto.histoWrappers):
                raise Exception("len(self.histoWrappers) != len(newDatasetrootHisto.histoWrappers), %d != %d" % len(self.histoWrappers), len(newDatasetRootHisto.histoWrappers))
            
            for i, drh in enumerate(self.histoWrappers):
                drh.modifyRootHisto(function, newDatasetRootHisto.histoWrappers[i])
        else:
            for i, drh in enumerate(self.histoWrappers):
                drh.modifyRootHisto(function)

    ## Set the current normalization scheme to 'to one'.
    # 
    # The histogram is normalized to unit area.
    # 
    # Sets the normalization of the underlying
    # dataset.DatasetRootHisto objects to 'by cross section' in order
    # to be able to sum them. The normalization 'to one' is then done
    # for the summed histogram.
    def normalizeToOne(self):
        self.normalization = "toOne"
        for h in self.histoWrappers:
            h.normalizeByCrossSection()

    ## Set the current normalization scheme to 'by cross section'.
    # 
    # The histogram is normalized to the cross section of the
    # corresponding dataset.
    # 
    # Sets the normalization of the underlying
    # dataset.DatasetRootHisto objects to 'by cross section'. Then
    # they can be summed directly, and the summed histogram is
    # automatically correctly normalized to the total cross section of
    # the merged dataset.Dataset objects.
    def normalizeByCrossSection(self):
        self.normalization = "byCrossSection"
        for h in self.histoWrappers:
            h.normalizeByCrossSection()

    ## Set the current normalization scheme to 'to luminosity'.
    # 
    # \param lumi   Integrated luminosity in pb^-1 to normalize to
    # 
    # The histogram is normalized first normalized to the cross
    # section of the corresponding dataset, and then to a given
    # luminosity.
    # 
    # Sets the normalization of the underlying
    # dataset.DatasetRootHisto objects to 'to luminosity'. Then they
    # can be summed directly, and the summed histogram is
    # automatically correctly normalized to the given integrated
    # luminosity. """
    def normalizeToLuminosity(self, lumi):
        self.normalization = "toLuminosity"
        for h in self.histoWrappers:
            h.normalizeToLuminosity(lumi)

    ## Merge the histograms and apply the current normalization.
    # 
    # The returned histogram is a clone, so client code can do
    # anything it wishes with it.
    # 
    # The merged MC histograms must be normalized in some way,
    # otherwise they can not be summed (or they can be, but the
    # contents of the summed histogram doesn't make any sense as it
    # is just the sum of the MC events of the separate datasets
    # which in general have different cross sections).
    def _normalizedHistogram(self):
        if self.normalization == "none":
            raise Exception("Merged MC histograms must be normalized to something!")

        hsum = self._getSumHistogram()
        if hsum is None:
            return hsum

        if self.normalization == "toOne":
            return _normalizeToOne(hsum)
        else:
            return hsum

    ## \var histoWrappers
    # List of underlying dataset.DatasetRootHisto objects
    ## \var normalization
    # String representing the current normalization scheme


## Wrapper for a added TH1 histograms from MC and the corresponding Datasets.
#
# Here "Adding" is like merging, but for datasets which have the same
# cross section, and are split to two datasets just for increased
# statistics. Use case is inclusive W+jets in Summer12, which is split
# into two datasets.
# 
# See also the documentation of DatasetRootHisto class.
class DatasetRootHistoAddedMC(DatasetRootHistoCompoundBase):
    ## Constructor.
    # 
    # \param histoWrappers   List of dataset.DatasetRootHisto objects to merge
    # \param addedDataset   The corresponding dataset.DatasetMerged object
    # 
    # The constructor checks that all histoWrappers are MC, and are
    # not yet normalized.
    def __init__(self, histoWrappers, addedDataset):
        DatasetRootHistoBase.__init__(self, addedDataset)
        self.histoWrappers = histoWrappers
        self.normalization = "none"
        for h in self.histoWrappers:
            if not h.isMC():
                raise Exception("Histograms to be added must come from MC")
            if h.normalization != "none":
                raise Exception("Histograms to be added must not be normalized at this stage")
            if h.multiplication != None:
                raise Exception("Histograms to be added must not be multiplied at this stage")

    def isData(self):
        return False

    def isMC(self):
        return True

    def forEach(self, function, datasetRootHisto1=None):
        ret = []
        if datasetRootHisto1 != None:
            if not isinstance(datasetRootHisto1, DatasetRootHistoAddedMC):
                raise Exception("datasetRootHisto1 must be of the type DatasetRootHistoAddedMC")
            if not len(self.histoWrappers) == len(datasetRootHisto1.histoWrappers):
                raise Exception("len(self.histoWrappers) != len(datasetrootHisto1.histoWrappers), %d != %d" % len(self.histoWrappers), len(datasetRootHisto1.histoWrappers))
            
            for i, drh in enumerate(self.histoWrappers):
                ret.extend(drh.forEach(function, datasetRootHisto1.histoWrappers[i]))
        else:
            for drh in self.histoWrappers:
                ret.extend(drh.forEach(function))
        return ret

    ## Modify the TH1 with a function
    #
    # \param function             Function taking the original TH1, and returning a new TH1. If newDatasetRootHisto is specified, function must take some other DatasetRootHisto object as an input too
    # \param newDatasetRootHisto  Optional, the other DatasetRootHisto object, must be the same type and contain same number of DatasetRootHisto objects
    #
    # Needed for appending rows to counters from TTree, and for embedding normalization
    def modifyRootHisto(self, function, newDatasetRootHisto=None):
        if newDatasetRootHisto != None:
            if not isinstance(newDatasetRootHisto, DatasetRootHistoAddedMC):
                raise Exception("newDatasetRootHisto must be of the type DatasetRootHistoAddedMC")
            if not len(self.histoWrappers) == len(newDatasetRootHisto.histoWrappers):
                raise Exception("len(self.histoWrappers) != len(newDatasetrootHisto.histoWrappers), %d != %d" % len(self.histoWrappers), len(newDatasetRootHisto.histoWrappers))
            
            for i, drh in enumerate(self.histoWrappers):
                drh.modifyRootHisto(function, newDatasetRootHisto.histoWrappers[i])
        else:
            for i, drh in enumerate(self.histoWrappers):
                drh.modifyRootHisto(function)

    ## Set the current normalization scheme to 'to one'.
    # 
    # The histogram is normalized to unit area.
    # 
    # Sets the normalization of the underlying
    # dataset.DatasetRootHisto objects to 'by cross section' in order
    # to be able to sum them. The normalization 'to one' is then done
    # for the summed histogram.
    def normalizeToOne(self):
        self.normalization = "toOne"

    ## Set the current normalization scheme to 'by cross section'.
    # 
    # The histogram is normalized to the cross section of the
    # corresponding dataset.
    # 
    # Sets the normalization of the underlying
    # dataset.DatasetRootHisto objects to 'by cross section'. Then
    # they can be summed directly, and the summed histogram is
    # automatically correctly normalized to the total cross section of
    # the merged dataset.Dataset objects.
    def normalizeByCrossSection(self):
        self.normalization = "byCrossSection"

    ## Set the current normalization scheme to 'to luminosity'.
    # 
    # \param lumi   Integrated luminosity in pb^-1 to normalize to
    # 
    # The histogram is normalized first normalized to the cross
    # section of the corresponding dataset, and then to a given
    # luminosity.
    # 
    # Sets the normalization of the underlying
    # dataset.DatasetRootHisto objects to 'to luminosity'. Then they
    # can be summed directly, and the summed histogram is
    # automatically correctly normalized to the given integrated
    # luminosity. """
    def normalizeToLuminosity(self, lumi):
        self.normalization = "toLuminosity"
        self.luminosity = lumi

    ## Merge the histograms and apply the current normalization.
    # 
    # The returned histogram is a clone, so client code can do
    # anything it wishes with it.
    # 
    # The merged MC histograms must be normalized in some way,
    # otherwise they can not be summed (or they can be, but the
    # contents of the summed histogram doesn't make any sense as it
    # is just the sum of the MC events of the separate datasets
    # which in general have different cross sections).
    def _normalizedHistogram(self):
        hsum = self._getSumHistogram()

        if self.normalization == "none":
            return hsum
        elif self.normalization == "toOne":
            return _normalizeToOne(hsum)

        # We have to normalize to cross section in any case
        hsum = _normalizeToFactor(hsum, self.dataset.getNormFactor())
        if self.normalization == "byCrossSection":
            return hsum
        elif self.normalization == "toLuminosity":
            return _normalizeToFactor(hsum, self.luminosity)
        else:
            raise Exception("Internal error, got normalization %s" % self.normalization)

    ## \var histoWrappers
    # List of underlying dataset.DatasetRootHisto objects
    ## \var normalization
    # String representing the current normalization scheme

class AnalysisNotFoundException(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)

class HistogramNotFoundException(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)

## Dataset class for histogram access from one ROOT file.
# 
# The default values for cross section/luminosity are read from
# 'configInfo/configInfo' histogram (if it exists). The data/MC
# datasets are differentiated by the existence of 'crossSection'
# (for MC) and 'luminosity' (for data) keys in the histogram. Reads
# the dataVersion from 'configInfo/dataVersion' and deduces whether
# the dataset is data/MC from it.
#
# \see dataset.DatasetMerged for merging multiple Dataset objects
# (either data or MC) to one logical dataset (e.g. all data datasets
# to one dataset, all QCD pThat bins to one dataset)
class Dataset:
    ## Constructor.
    # 
    # \param name              Name of the dataset (can be anything)
    # \param tfiles            List of ROOT.TFile objects for the dataset
    # \param analysisName      Base part of the analysis directory name
    # \param searchMode        String for search mode
    # \param dataEra           String for data era
    # \param optimizationMode  String for optimization mode (optional)
    # \param systematicVariation String for systematic variation (optional)
    # \param weightedCounters  If True, pick the counters from the 'weighted' subdirectory
    # \param counterDir        Name of the directory in the ROOT file for
    #                          event counter histograms. If None is given,
    #                          is assumed that the dataset has no counters.
    #                          This also means that the histograms from this
    #                          dataset can not be normalized unless the
    #                          number of all events is explictly set with
    #                          setNAllEvents() method. Note that this
    #                          directory should *not* point to the 'weighted'
    #                          subdirectory, but to the top-level counter
    #                          directory. The weighted counters are taken
    #                          into account with \a useWeightedCounters
    #                          argument
    # \param useAnalysisNameOnly Should the analysis directory be
    #                            inferred only from analysisName?
    # 
    # Opens the ROOT file, reads 'configInfo/configInfo' histogram
    # (if it exists), and reads the main event counter
    # ('counterDir/counters') if counterDir is not None. Reads also
    # 'configInfo/dataVersion' TNamed.
    #
    # With the v44_4 pattuples we improved the "Run2011 A vs. B vs AB"
    # workflow such that for MC we run analyzers for all data eras.
    # This means that the TDirectory names will be different for data
    # and MC, such that in MC the era name is appended to the
    # directory name. 
    #
    # The final directory name is (if \a useAnalysisNameOnly is False)
    # data: analysisName+searchMode+optimizationMode
    # MC:   analysisName+searchMode+dataEra+optimizationMode
    #
    # The \a useAnalysisNameOnly parameter is needed e.g. for ntuples
    # which store the era-specific weights to the tree itself, and
    # therefore the 
    def __init__(self, name, tfiles, analysisName,
                 searchMode=None, dataEra=None, optimizationMode=None, systematicVariation=None,
                 weightedCounters=True, counterDir="counters", useAnalysisNameOnly=False):
        self.name = name
        self.files = tfiles
        if len(self.files) == 0:
            raise Exception("Expecting at least one TFile, jot 0")

        # Now this is really an uhly hack
        self._setBaseDirectory(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(self.files[0].GetName())))))

        # Extract configInfo and dataVersion, check for consistency
        # that all files have the same values
        self.info = None
        self.dataVersion = None
        for f in self.files:
            configInfo = f.Get("configInfo")
            if configInfo == None:
                raise Exception("configInfo directory is missing from file %s" % f.GetName())

            info = _rescaleInfo(_histoToDict(configInfo.Get("configinfo")))
            if "energy" in info:
                info["energy"] = str(int(round(info["energy"])))
            if self.info is None:
                self.info = info
            else:
                for key, value in self.info.iteritems():
                    valnew = info[key]
                    if isinstance(value, basestring):
                        if value == valnew:
                            continue
                        raise Exception("Mismatched values in configInfo/configinfo, label %s, got %s from file %s, and %s from file %s" % (key, value, self.files[0].GetName(), valenew, f.GetName()))
                    if valnew == 0 and value == 0:
                        continue
                    if abs(value-valnew)/max(value, valnew) > 0.001:
                        raise Exception("Mismatched values in configInfo/configinfo, label %s, got %f from file %s, and %f from file %s" % (key, value, self.files[0].GetName(), valnew, f.GetName()))

            dataVersion = configInfo.Get("dataVersion")
            if dataVersion == None:
                raise Exception("Unable to determine dataVersion for dataset %s from file %s" % (name, f.GetName()))
            if self.dataVersion is None:
                self.dataVersion = dataVersion.GetTitle()
            else:
                if self.dataVersion != dataVersion.GetTitle():
                    raise Exception("Mismatched values in configInfo/dataVersion, got %s from file %s, and %s from file %s" % (self.dataVersion, self.files[0].GetName(), dataVersion.GetTitle(), f.GetName()))

        self._isData = "data" in self.dataVersion
        self._weightedCounters = weightedCounters

        self._analysisName = analysisName
        self._searchMode = searchMode
        self._dataEra = dataEra
        self._optimizationMode = optimizationMode
        self._systematicVariation = systematicVariation
        self._useAnalysisNameOnly = useAnalysisNameOnly

        self._analysisDirectoryName = self._analysisName
        if not self._useAnalysisNameOnly:
            if self._searchMode is not None:
                self._analysisDirectoryName += self._searchMode
            if self.isMC() and self._dataEra is not None:
                self._analysisDirectoryName += self._dataEra
            if self._optimizationMode is not None:
                self._analysisDirectoryName += self._optimizationMode
            if self.isMC() and self._systematicVariation is not None:
                self._analysisDirectoryName += self._systematicVariation
    
        # Check that analysis directory exists
        for f in self.files:
            if f.Get(self._analysisDirectoryName) == None:
                raise AnalysisNotFoundException("Analysis directory '%s' does not exist in file '%s'" % (self._analysisDirectoryName, f.GetName()))
        self._analysisDirectoryName += "/"

        self._unweightedCounterDir = counterDir
        if counterDir is not None:
            self._weightedCounterDir = counterDir + "/weighted"
            self._readCounters()

    ## Close the files
    #
    # Can be useful when opening very many files in order to reduce
    # the memory footprint and not hit the limit of number of open
    # files
    def close(self):
        for f in self.files:
            f.Close("R")
            f.Delete()
        self.files = []

    ## Clone the Dataset object
    # 
    # Nothing is shared between the returned copy and this object,
    # except the ROOT file object
    #
    # Use case is creative dataset manipulations, e.g. copying ttbar
    # to another name and scaling the cross section by the BR(t->H+)
    # while also keeping the original ttbar with the original SM cross
    # section.
    def deepCopy(self):
        d = Dataset(self.name, self.files, self._analysisName, self._searchMode, self._dataEra, self._optimizationMode, self._systematicVariation, self._weightedCounters, self._unweightedCounterDir, self._useAnalysisNameOnly)
        d.info.update(self.info)
        d.nAllEvents = self.nAllEvents
        return d

    ## Translate a logical name to a physical name in the file
    #
    # If name starts with slash ('/'), it is interpreted as a absolute
    # path within the ROOT file.
    def _translateName(self, name):
        if name[0] == '/':
            return name[1:]
        else:
            return self._analysisDirectoryName + name

    ## Get the ParameterSet stored in the ROOT file
    def getParameterSet(self):
        (objs, realNames) = self.getRootObjects("parameterSet")
        return objs[0].GetTitle()        

    ## Get ROOT histogram
    #
    # \param name    Path of the ROOT histogram relative to the analysis
    #                root directory
    #
    # \return pair (\a histogram, \a realName)
    #
    # If name starts with slash ('/'), it is interpreted as a absolute
    # path within the ROOT file.
    #
    # If dataset consists of multiple files, the histograms are added
    # with the ROOT.TH1.Add() method.
    def getRootHisto(self, name):
        (histos, realName) = self.getRootObjects(name)
        if len(histos) == 1:
            h = histos[0]
        else:
            h = histos[0]
            h = h.Clone(h.GetName()+"_cloned")
            for h2 in histos[1:]:
                h.Add(h2)

        return (h, realName)

    ## Create ROOT TChain
    # 
    # \param name    Path of the ROOT TTree relative to the analysis
    #                root directory
    #
    # \return pair (ROOT.TChain, \a realName)
    #
    # If name starts with slash ('/'), it is interpreted as a absolute
    # path within the ROOT file.
    def createRootChain(self, treeName):
        realName = self._translateName(treeName)
        chain = ROOT.TChain(realName)
        for f in self.files:
            chain.Add(f.GetName())
        return (chain, realName)

    ## Get arbitrary ROOT object from the file
    #
    # \param name    Path of the ROOT object relative to the analysis
    #                root directory
    #
    # \return pair (\a object, \a realName)
    #
    # If name starts with slash ('/'), it is interpreted as a absolute
    # path within the ROOT file.
    #
    # If the dataset consists of multiple files, raise an Exception.
    # User should use getRootObjects() method instead.
    def getRootObject(self, name):
        if len(self.files) > 1:
            raise Exception("You asked for a single ROOT object, but the Dataset %s consists of multiple ROOT files. You should call getRootObjects() instead, and deal with the multiple objects by yourself.")
        (lst, realName) = self.getRootObjects()
        return (lst[0], realName)

    ## Get list of arbitrary ROOT objects from the file
    #
    # \param name    Path of the ROOT object relative to the analysis
    #                root directory
    #
    # \return pair (\a list, \a realName), where \a list is the list
    #         of ROOT objects, one per file, and \a realName is the
    #         physical name of the objects
    #
    # If name starts with slash ('/'), it is interpreted as a absolute
    # path within the ROOT file.
    def getRootObjects(self, name):
        realName = self._translateName(name)
        ret = []
        for f in self.files:
            o = f.Get(realName)
            # below it is important to use '==' instead of 'is',
            # because null TObject == None, but is not None
            if o == None:
                raise HistogramNotFoundException("Unable to find object '%s' (requested '%s') from file '%s'" % (realName, name, self.files[0].GetName()))

            # http://root.cern.ch/phpBB3/viewtopic.php?f=14&t=15496
            # This one seems to save quite a lot of "garbage
            # collection" time
            ROOT.SetOwnership(o, True)

            ret.append(o)
        return (ret, realName)

    ## Read counters
    def _readCounters(self):
        self.counterDir = self._unweightedCounterDir

        # Read unweighted counters
        # The unweighted counters are allowed to not exist unless
        # weightedCounters are also enabled
        try:
            (counter, realName) = self.getRootHisto(self.counterDir+"/counter")
            ctr = _histoToCounter(counter)
            self.nAllEventsUnweighted = ctr[0][1].value() # first counter, second element of the tuple
        except HistogramNotFoundException, e:
            if not self._weightedCounters:
                raise Exception("Could not find counter histogram, message: %s" % str(e))
            self.nAllEventsUnweighted = -1

        self.nAllEventsWeighted = None
        self.nAllEvents = self.nAllEventsUnweighted

        # Read weighted counters
        if self._weightedCounters:
            self.counterDir = self._weightedCounterDir
            try:
                (counter, realName) = self.getRootHisto(self.counterDir+"/counter")
                ctr = _histoToCounter(counter)
                self.nAllEventsWeighted = ctr[0][1].value() # first counter, second element of the tuple
                self.nAllEvents = self.nAllEventsWeighted
            except HistogramNotFoundException, e:
                raise Exception("Could not find counter histogram, message: %s" % str(e))

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def forEach(self, function):
        return [function(self)]

    ## Set the centre-of-mass energy (in TeV) as string
    def setEnergy(self, energy):
        if not isinstance(energy, basestring):
            raise Exception("The energy must be set as string")
        self.info["energy"] = energy

    ## Get the centre-of-mass energy (in TeV) as string
    def getEnergy(self):
        return self.info.get("energy", "0")

    ## Set cross section of MC dataset (in pb).
    def setCrossSection(self, value):
        if not self.isMC():
            raise Exception("Should not set cross section for data dataset %s" % self.name)
        self.info["crossSection"] = value

    ## Get cross section of MC dataset (in pb).
    def getCrossSection(self):
        if not self.isMC():
            raise Exception("Dataset %s is data, no cross section available" % self.name)
        try:
            return self.info["crossSection"]
        except KeyError:
            raise Exception("Dataset %s is MC, but 'crossSection' is missing from configInfo/configInfo histogram. You have to explicitly set the cross section with setCrossSection() method." % self.name)

    ## Set the integrated luminosity of data dataset (in pb^-1).
    def setLuminosity(self, value):
        if not self.isData():
            raise Exception("Should not set luminosity for MC dataset %s" % self.name)
        self.info["luminosity"] = value

    ## Get the integrated luminosity of data dataset (in pb^-1).
    def getLuminosity(self):
        if not self.isData():
            raise Exception("Dataset %s is MC, no luminosity available" % self.name)
        try:
            return self.info["luminosity"]
        except KeyError:
            raise Exception("Dataset %s is data, but luminosity has not been set yet. You have to explicitly set the luminosity with setLuminosity() method." % self.name)

    def setProperty(self, key, value):
        self.info[key] = value

    def getProperty(self, key):
        return self.info[key]

    def isData(self):
        return self._isData

    def isMC(self):
        return not self._isData

    def getCounterDirectory(self):
        return self.counterDir

    def getRootFile(self):
        if len(self.files) > 1:
            raise Exception("Dataset %s consists of %d files, you should use getRootFiles() method instead." % (self.getName(), len(self.files)))
        return self.files[0]

    def getRootFiles(self):
        return self.files

    ## Set the number of all events (for normalization).
    #
    # This allows both overriding the value read from the event
    # counter, or creating a dataset without event counter at all.
    def setNAllEvents(self, nAllEvents):
        self.nAllEvents = nAllEvents

    ## Update number of all events (for normalization) to a pileup-reweighted value.
    #
    # \param era     Data era to use to pick the pile-up-reweighted all
    #                event number (optional, if not given a default
    #                value read from the configinfo is used)
    # \param kwargs  Keyword arguments (forwarded to pileupReweightedAllEvents.WeightedAllEvents.getWeighted())
    def updateNAllEventsToPUWeighted(self, era=None, **kwargs):
        # Ignore if data
        if self.isData():
            return

        if era == None:
            era = self._dataEra
        if era == None:
            raise Exception("%s: tried to update number of all events to pile-up reweighted value, but the data era was not set in the Dataset constructor nor was given as an argument" % self.getName())

        if self.nAllEventsUnweighted < 0:
            raise Exception("Number of all unweighted events is %d < 0, this is a symptom of missing unweighted counter" % self.nAllEventsUnweighted)

        try:
            self.nAllEvents = pileupReweightedAllEvents.getWeightedAllEvents(self.getName(), era).getWeighted(self.nAllEventsUnweighted, **kwargs)
        except KeyError:
            # Just ignore if no weights found for this dataset
            pass

    def getNAllEvents(self):
        if not hasattr(self, "nAllEvents"):
            raise Exception("Number of all events is not set for dataset %s! The counter directory was not given, and setNallEvents() was not called." % self.name)
        return self.nAllEvents

    ## Get the cross section normalization factor.
    #
    # The normalization factor is defined as crossSection/N(all
    # events), so by multiplying the number of MC events with the
    # factor one gets the corresponding cross section.
    def getNormFactor(self):
        nAllEvents = self.getNAllEvents()
        if nAllEvents == 0:
            raise Exception("%s: Number of all events is 0.\nProbable cause is that the counters are weighted, the analysis job input was a skim, and the updateNAllEventsToPUWeighted() has not been called." % self.name)

        return self.getCrossSection() / nAllEvents

    ## Check if a ROOT histogram exists in this dataset
    #
    # \param name  Name (path) of the ROOT histogram
    #
    # If dataset.TreeDraw object is given, it is considered to always
    # exist.
    def hasRootHisto(self, name):
        if hasattr(name, "draw"):
            return True

        try:
            return len(self.getRootObjects(name)) > 0
        except HistogramNotFoundException:
            return False

    ## Get the dataset.DatasetRootHisto object for a named histogram.
    # 
    # \param name   Path of the histogram in the ROOT file
    # \param modify Function to modify the histogram (use case is e.g. obtaining a slice of TH2 as TH1)
    #
    # \return dataset.DatasetRootHisto object containing the (unnormalized) TH1 and this Dataset
    # 
    # If dataset.TreeDraw object is given (or actually anything with
    # draw() method), the draw() method is called by giving the TFile
    # and the dataset name as parameters. The draw() method is
    # expected to return a TH1 which is then returned.
    def getDatasetRootHisto(self, name, modify=None):
        h = None
        if hasattr(name, "draw"):
            h = name.draw(self)
        else:
            pname = name
            (h, realName) = self.getRootHisto(pname)
            name = h.GetName()+"_"+self.name
            if modify is not None:
                h = modify(h)
            h.SetName(name.translate(None, "-+.:;"))
        return DatasetRootHisto(h, self)

    ## Get the directory content of a given directory in the ROOT file.
    # 
    # \param directory   Path of the directory in the ROOT file
    # \param predicate   Append the directory name to the return list only if
    #                    predicate returns true for the name. Predicate
    #                    should be a function taking an object in the directory as an
    #                    argument and returning a boolean.
    # 
    # \return List of names in the directory.
    #
    # If the dataset consists of multiple files, the listing of the
    # first file is given.
    def getDirectoryContent(self, directory, predicate=None):
        (dirs, realDir) = self.getRootObjects(directory)

        # wrap the predicate
        wrapped = None
        if predicate is not None:
            wrapped = lambda key: predicate(key.ReadObj())

        return aux.listDirectoryContent(dirs[0], wrapped)

    def _setBaseDirectory(self,base):
        self.basedir = base

    ## Get the path of the multicrab directory where this dataset originates
    def getBaseDirectory(self):
        return self.basedir

    def formatDatasetTree(self, indent):
        return '%sDataset("%s", %s, ...),\n' % (indent, self.getName(), ", ".join(['"%s"' % f.GetName() for f in self.files]))
        
    ## \var name
    # Name of the dataset
    ## \var files
    # List of TFile objects of the dataset
    ## \var info
    # Dictionary containing the configInfo histogram
    ## \var dataVersion
    # dataVersion string of the dataset (from TFile)
    ## \var era
    # Era of the data (used in the analysis for pile-up reweighting,
    # trigger efficiencies etc). Is None if corresponding TNamed
    # doesn't exist in configinfo directory
    ## \var nAllEvents
    # Number of all MC events, used in MC normalization
    ## \var nAllEventsUnweighted
    # Number of all MC events as read from the unweighted counter.
    # This should always be a non-zero number
    ## \var nAllEventsWeighted
    # Number of all MC events as read from the weighted counter. This
    # can be None (if weightedCounters was False in __init__()), zero
    # (if the input for the analysis job was a skim), or a non-zero
    # number (if the input for the anlysis job was not a skim)
    ## \var counterDir
    # Name of TDirectory containing the main event counter
    ## \var _origCounterDir
    # Name of the counter directory as given for __init__(), needed for deepCopy()
    ## \var _isData
    # If true, dataset is from data, if false, from MC


## Dataset class for histogram access for a dataset merged from Dataset objects.
# 
# The merged datasets are required to be either MC or data.
class DatasetMerged:
    ## Constructor.
    # 
    # \param name      Name of the merged dataset
    # \param datasets  List of dataset.Dataset objects to merge
    # 
    # Calculates the total cross section (luminosity) for MC (data)
    # datasets.
    def __init__(self, name, datasets):
        self.name = name
        #self.stacked = stacked
        self.datasets = datasets
        if len(datasets) == 0:
            raise Exception("Can't create a DatasetMerged from 0 datasets")

        self.info = {}

        energy = self.datasets[0].getEnergy()
        for d in self.datasets[1:]:
            if energy != d.getEnergy():
                raise Exception("Can't merge datasets with different centre-of-mass energies (%s: %d TeV, %s: %d TeV)" % (self.datasets[0].getName(), energy, d.getName(), d.getEnergy()))

        if self.datasets[0].isMC():
            crossSum = 0.0
            for d in self.datasets:
                crossSum += d.getCrossSection()
            self.info["crossSection"] = crossSum
        else:
            lumiSum = 0.0
            for d in self.datasets:
                lumiSum += d.getLuminosity()
            self.info["luminosity"] = lumiSum

    ## Close TFiles in the contained dataset.Dataset objects
    def close(self):
        for d in self.datasets:
            d.close()

    ## Make a deep copy of a DatasetMerged object.
    #
    # Nothing is shared between the returned copy and this object.
    #
    # \see dataset.Dataset.deepCopy()
    def deepCopy(self):
        dm = DatasetMerged(self.name, [d.deepCopy() for d in self.datasets])
        dm.info.update(self.info)
        return dm

    def setDirectoryPostfix(self, postfix):
        for d in self.datasets:
            d.setDirectoryPostfix(postfix)

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def forEach(self, function):
        ret = []
        for d in self.datasets:
            ret.extend(d.forEach(function))
        return ret

    def setEnergy(self, energy):
        for d in self.datasets:
            d.setEnergy(energy)

    def getEnergy(self):
        return self.datasets[0].getEnergy()

    def setCrossSection(self, value):
        if self.isData():
            raise Exception("Should not set cross section for data dataset %s (has luminosity)" % self.name)
        raise Exception("Setting cross section for merged dataset is meaningless (it has no real effect, and hence is misleading")

    ## Get cross section of MC dataset (in pb).
    def getCrossSection(self):
        if self.isData():
            raise Exception("Dataset %s is data, no cross section available" % self.name)
        return self.info["crossSection"]

    def setLuminosity(self, value):
        if self.isMC():
            raise Exception("Should not set luminosity for MC dataset %s (has crossSection)" % self.name)
        raise Exception("Setting luminosity for merged dataset is meaningless (it has no real effect, and hence is misleading")

    ## Get the integrated luminosity of data dataset (in pb^-1).
    def getLuminosity(self):
        if self.isMC():
            raise Exception("Dataset %s is MC, no luminosity available" % self.name)
        return self.info["luminosity"]

    def setProperty(self, key, value):
        self.info[key] = value

    def getProperty(self, key):
        return self.info[key]

    def isData(self):
        return self.datasets[0].isData()

    def isMC(self):
        return self.datasets[0].isMC()

    def getCounterDirectory(self):
        countDir = self.datasets[0].getCounterDirectory()
        for d in self.datasets[1:]:
            if countDir != d.getCounterDirectory():
                raise Exception("Error: merged datasets have different counter directories")
        return countDir

    def getNormFactor(self):
        return None

    ## Check if a ROOT histogram exists in this dataset
    #
    # \param name  Name (path) of the ROOT histogram
    #
    # The ROOT histogram is expected to exist in all underlying
    # dataset.Dataset objects.
    def hasRootHisto(self, name):
        has = True
        for d in self.datasets:
            has = has and d.hasRootHisto(name)
        return has

    ## Get the DatasetRootHistoMergedMC/DatasetRootHistoMergedData object for a named histogram.
    #
    # \param name   Path of the histogram in the ROOT file
    # \param kwargs Keyword arguments, forwarder to get
    #               getDatasetRootHisto() of the contained
    #               Dataset objects
    def getDatasetRootHisto(self, name, **kwargs):
        wrappers = [d.getDatasetRootHisto(name, **kwargs) for d in self.datasets]
        # Catch returned error messages
        if wrappers != None:
            for w in wrappers:
                if isinstance(w,str):
                    return w
        # No errors, continue as usual
        if self.isMC():
            return DatasetRootHistoMergedMC(wrappers, self)
        else:
            return DatasetRootHistoMergedData(wrappers, self)

    ## Get the directory content of a given directory in the ROOT file.
    # 
    # \param directory   Path of the directory in the ROOT file
    # \param predicate   Append the directory name to the return list only if
    #                    predicate returns true for the name. Predicate
    #                    should be a function taking a string as an
    #                    argument and returning a boolean.
    # 
    # Returns a list of names in the directory. The contents of the
    # directories of the merged datasets are required to be identical.
    def getDirectoryContent(self, directory, predicate=lambda x: True):
        content = self.datasets[0].getDirectoryContent(directory, predicate)
        for d in self.datasets[1:]:
            if content != d.getDirectoryContent(directory, predicate):
                raise Exception("Error: merged datasets have different contents in directory '%s'" % directory)
        return content

    def formatDatasetTree(self, indent):
        ret = '%sDatasetMerged("%s", [\n' % (indent, self.getName())
        for dataset in self.datasets:
            ret += dataset.formatDatasetTree(indent+"  ")
        ret += "%s]),\n" % indent
        return ret

    ## \var name
    # Name of the merged dataset
    ## \var datasets
    # List of merged dataset.Dataset objects
    ## \var info
    # Dictionary containing total cross section (MC) or integrated luminosity (data)

## Dataset class for histogram access for a dataset added from Dataset objects.
# 
# The added datasets are required to be MC
class DatasetAddedMC(DatasetMerged):
    ## Constructor.
    # 
    # \param name      Name of the merged dataset
    # \param datasets  List of dataset.Dataset objects to add
    #
    # The cross section of the added datasets must be the same
    def __init__(self, name, datasets):
        self.name = name
        #self.stacked = stacked
        self.datasets = datasets
        if len(datasets) == 0:
            raise Exception("Can't create a DatasetAddedMC from 0 datasets")

        self.info = {}

        energy = self.datasets[0].getEnergy()
        for d in self.datasets[1:]:
            if energy != d.getEnergy():
                raise Exception("Can't merge datasets with different centre-of-mass energies (%s: %d TeV, %s: %d TeV)" % self.datasets[0].getName(), energy, d.getName(), d.getEnergy())

        crossSection = self.datasets[0].getCrossSection()
        for d in self.datasets:
            if not d.isMC():
                raise Exception("Datasets must be MC, got %s which is data" % d.getName())
            xs2 = d.getCrossSection()
            if abs((xs2-crossSection)/crossSection) > 1e-6:
                raise Exception("Datasets must have the same cross section, got %f from %s and %f from %s" % (crossSection, self.dataests[0].getName(), xs2, d.getName()))

        self.info["crossSection"] = crossSection

    ## Make a deep copy of a DatasetMerged object.
    #
    # Nothing is shared between the returned copy and this object.
    #
    # \see dataset.Dataset.deepCopy()
    def deepCopy(self):
        dm = DatasetAddedMC(self.name, [d.deepCopy() for d in self.datasets])
        dm.info.update(self.info)
        return dm

    ## Set cross section of MC dataset (in pb).
    def setCrossSection(self, value):
        if not self.isMC():
            raise Exception("Should not set cross section for data dataset %s" % self.name)
        self.info["crossSection"] = value
        for d in self.datasets:
            d.setCrossSection(value)

    def setProperty(self, key, value):
        for d in self.datasets:
            d.setProperty(key, value)

    ## Get the DatasetRootHistoMergedMC/DatasetRootHistoMergedData object for a named histogram.
    #
    # \param name   Path of the histogram in the ROOT file
    # \param kwargs Keyword arguments, forwarder to get
    #               getDatasetRootHisto() of the contained
    #               Dataset objects
    def getDatasetRootHisto(self, name, **kwargs):
        wrappers = [d.getDatasetRootHisto(name, **kwargs) for d in self.datasets]
        return DatasetRootHistoAddedMC(wrappers, self)


    ## Get the cross section normalization factor.
    #
    # The normalization factor is defined as crossSection/N(all
    # events), so by multiplying the number of MC events with the
    # factor one gets the corresponding cross section.
    #
    # Implementation is close to dataset.Dataset.getNormFactor()
    def getNormFactor(self):
        nAllEvents = sum([d.getNAllEvents() for d in self.datasets])
        if nAllEvents == 0:
            raise Exception("%s: Number of all events is 0.\nProbable cause is that the counters are weighted, the analysis job input was a skim, and the updateAllEventsToPUWeighted() has not been called." % self.name)

        return self.getCrossSection() / nAllEvents

    def formatDatasetTree(self, indent):
        ret = '%sDatasetAddedMC("%s", [\n' % (indent, self.getName())
        for dataset in self.datasets:
            ret += dataset.formatDatasetTree(indent+"  ")
        ret += "%s]),\n" % indent
        return ret

## Collection of Dataset objects which are managed together.
# 
# Holds both an ordered list of Dataset objects, and a name->object
# map for convenient access by dataset name.
#
# \todo The code structure could be simplified by getting rid of
# dataset.DatasetRootHisto. This would mean that the MC normalisation
# should be handled in dataset.DatasetManagager and dataset.Dataset,
# with an interface similar to what dataset.DatasetRootHisto and
# histograms.HistoManager provide now (i.e. user first sets the
# normalisation scheme, and then asks histograms which are then
# normalised as requested). dataset.Dataset and dataset.DatasetManager
# should then return ROOT TH1s, with which user is free to do what
# (s)he wants. histograms.HistoManager and histograms.HistoManagerImpl
# could be merged, as it would take already-normalized histograms as
# input (the input should still be histograms.Histo classes in order
# to give user freedom to provide fully customized version of such
# wrapper class if necessary). The interface of plots.PlotBase would
# still accept TH1/TGraph, so no additional burden would appear for
# the usual use cases with plots. The information of a histogram being
# data/MC in histograms.Histo could also be removed (as it is
# sometimes too restrictive), and the use in plots.PlotBase (and
# deriving classes) could be transformed to identify the data/MC
# datasets (for default formatting purposes) by the name of the
# histograms (in the usual workflow the histograms have the dataset
# name), with the possibility that user can easily modify the names of
# data/MC histograms. This would bring more flexibility on that front,
# and easier customization when necessary.
class DatasetManager:
    ## Constructor
    #
    # \param base    Directory (absolute/relative to current working
    #                directory) where the luminosity JSON file is located (see
    #                loadLuminosities())
    #
    # DatasetManager is constructed as empty
    def __init__(self, base=""):
        self.datasets = []
        self.datasetMap = {}
        self._setBaseDirectory(base)

    ## Populate the datasetMap member from the datasets list.
    # 
    # Intended only for internal use.
    def _populateMap(self):
        self.datasetMap = {}
        for d in self.datasets:
            self.datasetMap[d.getName()] = d

    def _setBaseDirectory(self, base):
        for d in self.datasets:
            d._setBaseDirectory(base)

    ## Close all TFiles of the contained dataset.Dataset objects
    #
    # \see dataset.Dataset.close()
    def close(self):
        for d in self.datasets:
            d.close()

    ## Append a Dataset object to the set.
    # 
    # \param dataset    Dataset object
    # 
    # The new Dataset must have a different name than the already existing ones.
    def append(self, dataset):
        if dataset.getName() in self.datasetMap:
            raise Exception("Dataset '%s' already exists in this DatasetManager" % dataset.getName())

        self.datasets.append(dataset)
        self.datasetMap[dataset.getName()] = dataset

    ## Extend the set of Datasets from another DatasetManager object.
    # 
    # \param datasetmgr   DatasetManager object
    # 
    # Note that the dataset.Dataset objects of datasetmgr are appended to
    # self by reference, i.e. the Dataset objects will be shared
    # between them.
    # """
    def extend(self, datasetmgr):
        for d in datasetmgr.datasets:
            self.append(d)

    ## Make a shallow copy of the DatasetManager object.
    # 
    # The dataset.Dataset objects are shared between the DatasetManagers.
    #
    # Useful e.g. if you want to have a subset of the dataset.Dataset objects
    def shallowCopy(self):

        copy = DatasetManager()
        copy.extend(self)
        return copy

    ## Make a deep copy of the DatasetManager object.
    # 
    # Nothing is shared between the DatasetManagers.
    #
    # Useful e.g. if you want to have two sets of same datasets, but
    # others are somehow modified (e.g. cross section)
    def deepCopy(self):
        copy = DatasetManager()
        for d in self.datasets:
            copy.append(d.deepCopy())
        return copy

    ## Set the centre-of-mass energy for all datasets
    def setEnergy(self, energy):
        for d in self.datasets:
            d.setEnergy(energy)

    ## Get a list of centre-of-mass energies of the datasets
    def getEnergies(self):
        tmp = {}
        for d in self.datasets:
            tmp[d.getEnergy()] = 1
        energies = tmp.keys()
        energies.sort()
        return energies

    def hasDataset(self, name):
        return name in self.datasetMap

    def getDataset(self, name):
        return self.datasetMap[name]

    ## Get a list of dataset.DatasetRootHisto objects for a given name.
    # 
    # \param histoName   Path to the histogram in each ROOT file.
    # \param kwargs      Keyword arguments, forwarder to get
    #                    getDatasetRootHisto() of the contained
    #                    Dataset objects
    #
    # \see dataset.Dataset.getDatasetRootHisto()
    def getDatasetRootHistos(self, histoName, **kwargs):
        return [d.getDatasetRootHisto(histoName, **kwargs) for d in self.datasets]

    ## Get a list of all dataset.Dataset objects.
    def getAllDatasets(self):
        return self.datasets

    ## Get a list of MC dataset.Dataset objects.
    #
    # \todo Implementation would be simpler with filter() method
    def getMCDatasets(self):
        ret = []
        for d in self.datasets:
            if d.isMC():
                ret.append(d)
        return ret

    ## Get a list of data dataset.Dataset objects.
    #
    # \todo Implementation would be simpler with filter() method
    def getDataDatasets(self):
        ret = []
        for d in self.datasets:
            if d.isData():
                ret.append(d)
        return ret

    ## Get a list of names of all dataset.Dataset objects.
    def getAllDatasetNames(self):
        return [x.getName() for x in self.getAllDatasets()]

    ## Get a list of names of MC dataset.Dataset objects."""
    def getMCDatasetNames(self):
        return [x.getName() for x in self.getMCDatasets()]

    ## Get a list of names of data dataset.Dataset objects.
    def getDataDatasetNames(self):
        return [x.getName() for x in self.getDataDatasets()]

    ## Select and reorder Datasets.
    # 
    # \param nameList   Ordered list of Dataset names to select
    # 
    # This method can be used to either select a set of
    # dataset.Dataset objects. reorder them, or both.
    def selectAndReorder(self, nameList):
        selected = []
        for name in nameList:
            try:
                selected.append(self.datasetMap[name])
            except KeyError:
                print >> sys.stderr, "WARNING: Dataset selectAndReorder: dataset %s doesn't exist" % name

        self.datasets = selected
        self._populateMap()

    ## Remove dataset.Dataset objects
    # 
    # \param nameList    List of dataset.Dataset names to remove
    # \param close       If true, close the removed dataset.Dataset objects
    def remove(self, nameList, close=True):
        if isinstance(nameList, basestring):
            nameList = [nameList]

        selected = []
        for d in self.datasets:
            if not d.getName() in nameList:
                selected.append(d)
            else:
                d.close()
        self.datasets = selected
        self._populateMap()

    ## Rename a Dataset.
    # 
    # \param oldName   The current name of a dataset.Dataset
    # \param newName   The new name of a dataset.Dataset
    def rename(self, oldName, newName):
        if oldName == newName:
            return

        if newName in self.datasetMap:
            raise Exception("Trying to rename datasets '%s' to '%s', but a dataset with the new name already exists!" % (oldName, newName))
        self.datasetMap[oldName].setName(newName)
        self._populateMap()

    ## Rename many dataset.Dataset objects
    # 
    # \param nameMap   Dictionary containing oldName->newName mapping
    # \param silent    If true, don't raise Exception if source dataset doesn't exist
    #
    # \see rename()
    def renameMany(self, nameMap, silent=False):
        for oldName, newName in nameMap.iteritems():
            if oldName == newName:
                continue

            if newName in self.datasetMap:
                raise Exception("Trying to rename datasets '%s' to '%s', but a dataset with the new name already exists!" % (oldName, newName))

            try:
                self.datasetMap[oldName].setName(newName)
            except KeyError, e:
                if not silent:
                    raise Exception("Trying to rename dataset '%s' to '%s', but '%s' doesn't exist!" % (oldName, newName, oldName))
        self._populateMap()

    ## Merge all data dataset.Dataset objects to one with a name 'Data'.
    #
    # \param args    Positional arguments (forwarded to merge())
    # \param kwargs  Keyword arguments (forwarded to merge())
    def mergeData(self, *args, **kwargs):
        self.merge("Data", self.getDataDatasetNames(), *args, **kwargs)

    ## Merge all MC dataset.Datasetobjects to one with a name 'MC'.
    #
    # \param args    Positional arguments (forwarded to merge())
    # \param kwargs  Keyword arguments (forwarded to merge())
    def mergeMC(self, *args, **kwargs):
        self.merge("MC", self.getMCDatasetNames(), *args, **kwargs)

    ## Merge datasets according to the mapping.
    #
    # \param mapping Dictionary of oldName->mergedName mapping. The
    #                dataset.Dataset objects having the same mergedName are merged
    # \param args    Positional arguments (forwarded to merge())
    # \param kwargs  Keyword arguments (forwarded to merge())
    def mergeMany(self, mapping, *args, **kwargs):
        toMerge = {}
        for d in self.datasets:
            if d.getName() in mapping:
                newName = mapping[d.getName()]
                if newName in toMerge:
                    toMerge[newName].append(d.getName())
                else:
                    toMerge[newName] = [d.getName()]

        for newName, nameList in toMerge.iteritems():
            self.merge(newName, nameList, *args, **kwargs)

    ## Merge dataset.Dataset objects.
    # 
    # \param newName      Name of the merged dataset.DatasetMerged
    # \param nameList     List of dataset.Dataset names to merge
    # \param keepSources  If true, keep the original dataset.Dataset
    #                     objects in the list of datasets. Otherwise
    #                     they are removed, as they are now contained
    #                     in the dataset.DatasetMerged object
    # \param addition     Creates DatasetAddedMC instead of DatasetMerged
    #
    # If nameList translates to only one dataset.Dataset, the
    # dataset.Daataset object is renamed (i.e. dataset.DatasetMerged
    # object is not created)
    def merge(self, newName, nameList, keepSources=False, addition=False, silent=False):
        (selected, notSelected, firstIndex) = _mergeStackHelper(self.datasets, nameList, "merge")
        if len(selected) == 0:
            if not silent:
                print >> sys.stderr, "Dataset merge: no datasets '" +", ".join(nameList) + "' found, not doing anything"
            return
        elif len(selected) == 1:
            if not silent:
                print >> sys.stderr, "Dataset merge: one dataset '" + selected[0].getName() + "' found from list '" + ", ".join(nameList)+"', renaming it to '%s'" % newName
            self.rename(selected[0].getName(), newName)
            return

        if not keepSources:
            self.datasets = notSelected
        if addition:
            newDataset = DatasetAddedMC(newName, selected)
        else:
            newDataset = DatasetMerged(newName, selected)

        self.datasets.insert(firstIndex, newDataset)
        self._populateMap()

    ## Load integrated luminosities from a JSON file.
    # 
    # \param fname   Path to the file (default: 'lumi.json'). If the
    #                directory part of the path is empty, the file is
    #                looked from the base directory (which defaults to
    #                current directory)
    # 
    # The JSON file should be formatted like this:
    # \verbatim
    # '{
    #    "dataset_name": value_in_pb,
    #    "Mu_135821-144114": 2.863224758
    #  }'
    # \endverbatim
    # Note: as setting the integrated luminosity for a merged dataset
    # will fail (see dataset.DatasetMerged.setLuminosity()), loading
    # luminosities must be done before merging the data datasets to
    # one.
    def loadLuminosities(self, fname="lumi.json"):
        import json

        for d in self.datasets:
            jsonname = os.path.join(d.basedir, fname)
            if not os.path.exists(jsonname):
                print >> sys.stderr, "WARNING: luminosity json file '%s' doesn't exist (using luminosity=1 for data)!" % jsonname
                for name in self.getDataDatasetNames():
                    self.getDataset(name).setLuminosity(1)
            else:
                data = json.load(open(jsonname))
                for name, value in data.iteritems():
                    if self.hasDataset(name):
                        self.getDataset(name).setLuminosity(value)

####        if len(os.path.dirname(fname)) == 0:
####            fname = os.path.join(self.basedir, fname)
####
####        if not os.path.exists(fname):
####            print >> sys.stderr, "WARNING: luminosity json file '%s' doesn't exist!" % fname
####
####        data = json.load(open(fname))
####        for name, value in data.iteritems():
####            if self.hasDataset(name):
####                self.getDataset(name).setLuminosity(value)

    ## Update all event counts to the ones taking into account the pile-up reweighting
    #
    # \param kwargs     Keyword arguments (forwarded to dataset.Dataset.updateAllEventsToWeighted)
    #
    # Uses the table pileupReweightedAllEvents._weightedAllEvents
    def updateNAllEventsToPUWeighted(self, **kwargs):
        for dataset in self.datasets:
            dataset.updateNAllEventsToPUWeighted(**kwargs)

    ## Format dataset information
    def formatInfo(self):
        out = StringIO.StringIO()
        col1hdr = "Dataset"
        col2hdr = "Cross section (pb)"
        col3hdr = "Norm. factor"
        col4hdr = "Int. lumi (pb^-1)" 

        maxlen = max([len(x.getName()) for x in self.datasets]+[len(col1hdr)])
        c1fmt = "%%-%ds" % (maxlen+2)
        c2fmt = "%%%d.4g" % (len(col2hdr)+2)
        c3fmt = "%%%d.4g" % (len(col3hdr)+2)
        c4fmt = "%%%d.10g" % (len(col4hdr)+2)

        c2skip = " "*(len(col2hdr)+2)
        c3skip = " "*(len(col3hdr)+2)
        c4skip = " "*(len(col4hdr)+2)

        out.write((c1fmt%col1hdr)+"  "+col2hdr+"  "+col3hdr+"  "+col4hdr+"\n")
        for dataset in self.datasets:
            line = (c1fmt % dataset.getName())
            if dataset.isMC():
                line += c2fmt % dataset.getCrossSection()
                normFactor = dataset.getNormFactor()
                if normFactor != None:
                    line += c3fmt % normFactor
                else:
                    line += c3skip
            else:
                line += c2skip+c3skip + c4fmt%dataset.getLuminosity()
            out.write(line)
            out.write("\n")

        ret = out.getvalue()
        out.close()
        return ret

    ## Print dataset information.
    def printInfo(self):
        print self.formatInfo()

    def formatDatasetTree(self):
        ret = "DatasetManager.datasets = [\n"
        for dataset in self.datasets:
            ret += dataset.formatDatasetTree(indent="  ")
        ret += "]"
        return ret

    def printDatasetTree(self):
        print self.formatDatasetTree()

    ## Prints the parameterSet of some Dataset
    #
    # Absolutely no guarantees of which Dataset the parameterSet is
    # from will not be given.
    def printSelections(self):
        namePSets = self.datasets[0].forEach(lambda d: (d.getName(), d.getParameterSet()))
        print "ParameterSet for dataset", namePSets[0][0]
        print namePSets[0][1]

    def getSelections(self):
        namePSets = self.datasets[0].forEach(lambda d: (d.getName(), d.getParameterSet()))
        #print "ParameterSet for dataset", namePSets[0][0]
        return namePSets[0][1]

    ## \var datasets
    # List of dataset.Dataset (or dataset.DatasetMerged) objects to manage
    ## \var datasetMap
    # Dictionary from dataset names to dataset.Dataset objects, for
    # more straightforward accessing of dataset.Dataset objects by
    # their name.
    ## \var basedir
    # Directory (absolute/relative to current working directory) where
    # the luminosity JSON file is located (see loadLuminosities())

## Precursor dataset, helper class for DatasetManagerCreator
#
# This holds the name, ROOT file, and data/MC status of a dataset.
class DatasetPrecursor:
    def __init__(self, name, filenames):
        self._name = name
        if isinstance(filenames, basestring):
            self._filenames = [filenames]
        else:
            self._filenames = filenames

        self._rootFiles = []
        dataVersion = None
        for name in self._filenames:
            rf = ROOT.TFile.Open(name)
            # Below is important to use '==' instead of 'is' to check for
            # null file
            if rf == None:
                raise Exception("Unable to open ROOT file '%s' for dataset '%s'" % (name, self._name))
            self._rootFiles.append(rf)

            dv = rf.Get("configInfo/dataVersion")
            if dv == None:
                raise Exception("Unable to find 'configInfo/dataVersion' from ROOT file '%s'" % name)
                
            if dataVersion is None:
                dataVersion = dv.GetTitle()
            else:
                if dataVersion != dv.GetTitle():
                    raise Exception("Mismatch in dataVersion when creating multi-file DatasetPrecursor, got %s from file %s, and %s from %s" % (dataVersion, self._filenames[0], dv.GetTitle(), name))

        self._isData = "data" in dataVersion

    def getName(self):
        return self._name

    def getFiles(self):
        return self._rootFiles

    def isData(self):
        return self._isData

    def isMC(self):
        return not self.isData()

    ## Close the ROOT files
    def close():
        for f in self._rootFiles:
            f.close("R")
            f.Delete()
        self._rootFiles = []

_analysisNameSkipList = [re.compile("^SystVar"), re.compile("configInfo"), re.compile("PUWeightProducer")]
_analysisSearchModes = ["Light", "Heavy"]
_dataDataEra_re = re.compile("_(?P<era>201\d\S)_")

## Class for listing contents of multicrab dirs, dataset ROOT files, and creating DatasetManager
#
# The mai is to first create an object of this class to represent a
# multicrab directory, and then create one or many DatasetManagers,
# which then correspond to a single analysis directory within the ROOT
# files.
class DatasetManagerCreator:
    ## Constructor
    #
    # \param rootFileList  List of (\a name, \a filenames) pairs (\a
    #                      name should be string, \a filenames can be
    #                      string or list of strings). \a name is taken
    #                      as the dataset name, and \a filenames as the
    #                      path(s) to the ROOT file(s).
    # \param kwargs        Keyword arguments (see below)
    #
    # <b>Keyword arguments</b>
    # \li \a baseDirectory    Base directory of the datasets (delivered later to DatasetManager._setBaseDirectory())
    #
    # Creates DatasetPrecursor objects for each ROOT file, reads the
    # contents of first MC file to get list of available analyses.
    def __init__(self, rootFileList, **kwargs):
        self._precursors = [DatasetPrecursor(name, filenames) for name, filenames in rootFileList]
        self._baseDirectory = kwargs.get("baseDirectory", "")

        mcRead = False
        for d in self._precursors:
            if d.isMC():
                self._readAnalysisContent(d)
                mcRead = True
                break

        if not mcRead:
            for d in self._precursors:
                if d.isData():
                    self._readAnalysisContent(d)
                    break

        dataEras = {}
        for d in self._precursors:
            if d.isData():
                m = _dataDataEra_re.search(d.getName())
                if m:
                    dataEras["Run"+m.group("era")] = 1

        self._dataDataEras = dataEras.keys()
        self._dataDataEras.sort()                

    def _readAnalysisContent(self, precursor):
        contents = aux.listDirectoryContent(precursor.getFiles()[0], lambda key: key.IsFolder())

        def skipItem(name):
            for skip_re in _analysisNameSkipList:
                if skip_re.search(name):
                    return False
            return True
        contents = filter(skipItem, contents)
        if len(contents) == 0:
            raise Exception("No analysis TDirectories found")

        analyses = {}
        searchModes = {}
        dataEras = {}
        optimizationModes = {}
        systematicVariations = {}

        for d in contents:
            directoryName = d

            # Look for systematic variation
            start = directoryName.find("SystVar")
            if start >= 0:
                systematicVariations[directoryName[start:]] = 1
                directoryName = directoryName[:start]

            # Look for optimization mode
            start = directoryName.find("Opt")
            if start >= 0:
                optimizationModes[directoryName[start:]] = 1
                directoryName = directoryName[:start]

            # Look for data era
            if precursor.isMC():
                start = directoryName.find("Run")
                if start >= 0:
                    dataEras[directoryName[start:]] = 1
                    directoryName = directoryName[:start]
            
            # Look for search mode
            for sm in _analysisSearchModes:
                start = directoryName.find(sm)
                if start >= 0:
                    searchModes[sm] = 1
                    directoryName = directoryName[:start]
                    break

            # Whatever is left in directoryName, is our analysis name
            analyses[directoryName] = 1

        self._analyses =  analyses.keys()
        self._searchModes = searchModes.keys()
        self._mcDataEras = dataEras.keys()
        self._optimizationModes = optimizationModes.keys()
        self._systematicVariations = systematicVariations.keys()

        self._analyses.sort()
        self._searchModes.sort()
        self._mcDataEras.sort()
        self._optimizationModes.sort()
        self._systematicVariations.sort()

    ## Create DatasetManager
    #
    # \param kwargs   Keyword arguments (see below)
    #
    # <b>Keyword arguments</b>
    # \li \a analysisName      Base part of the analysis directory name
    # \li \a searchMode        String for search mode
    # \li \a dataEra           String for data era
    # \li \a optimizationMode  String for optimization mode (optional)
    # \li \a systematicVariation String for systematic variation (optional)
    # \li \a opts              Optional OptionParser object. Should have options added with addOptions().
    #
    # The values of \a analysisName, \a searchMode, \a dataEra, and \a
    # optimizationMode are overridden from \a opts, if they are set
    # (i.e. are non-None). Also, if any of these is not specified
    # either explicitly or via \a opts, the value is inferred from the
    # contents, if there exists only one of it.
    def createDatasetManager(self, **kwargs):
        _args = {}
        _args.update(kwargs)


        # First check that if some of these is not given, if there is
        # exactly one it available, use that.
        for arg, attr in [("analysisName", "getAnalyses"),
                          ("searchMode", "getSearchModes"),
                          ("dataEra", "getDataEras"),
                          ("optimizationMode", "getOptimizationModes"),
                          ("systematicVariation", "getSystematicVariations")]:
            lst = getattr(self, attr)()
            if arg not in _args and len(lst) == 1:
                _args[arg] = lst[0]

        # Then override from command line options
        opts = kwargs.get("opts", None)
        if opts is not None:
            for arg in ["analysisName", "searchMode", "dataEra", "optimizationMode", "systematicVariation", "counterDir"]:
                o = getattr(opts, arg)
                if o is not None:
                    _args[arg] = o
            del _args["opts"]

        if not "analysisName" in _args:
            raise Exception("You did not specify AnalysisName, and it was not automatically detected from ROOT file")

        # Print the configuration
        parameters = []
        for name in ["analysisName", "searchMode", "dataEra", "optimizationMode", "systematicVariation"]:
            if name in _args:
                value = _args[name]
                parameters.append("%s='%s'" % (name, value))
        print "Creating DatasetManager with", ", ".join(parameters)

        # Crate manager and datasets
        dataEra = _args.get("dataEra", None)
        precursors = self._precursors[:]
        if dataEra is not None:
            def isInEra(eras, precursor):
                if precursor.isMC():
                    return True
                if isinstance(eras, basestring):
                    eras = [eras]
                for e in eras:
                    if e in precursor.getName():
                        return True
                return False

            try:
                lst = _dataEras[dataEra]
            except KeyError:
                eras = _dataEras.keys()
                eras.sort()
                raise Exception("Unknown data era '%s', known are %s" % (dataEra, ", ".join(eras)))

            precursors = filter(lambda p: isInEra(lst, p), precursors)

        manager = DatasetManager()
        for precursor in precursors:
            try:
                dset = Dataset(precursor.getName(), precursor.getFiles(), **_args)
            except AnalysisNotFoundException, e:
                msg = str(e)+"\n"
                helpFound = False
                for arg, attr in [("analysisName", "getAnalyses"),
                                  ("searchMode", "getSearchModes"),
                                  ("dataEra", "getDataEras"),
                                  ("optimizationMode", "getOptimizationModes"),
                                  ("systematicVariation", "getSystematicVariations")]:
                    lst = getattr(self, attr)()
                    if arg not in _args and len(lst) > 1:
                        msg += "You did not specify %s, while ROOT file contains %s\n" % (arg, ", ".join(lst))
                        helpFound = True
                    if arg in _args and len(lst) == 0:
                        msg += "You specified %s, while ROOT file apparently has none of them\n" % arg
                        helpFound = True
                if not helpFound:
                    raise e
                raise Exception(msg)

            manager.append(dset)

        if len(self._baseDirectory) > 0:
            manager._setBaseDirectory(self._baseDirectory)

        return manager

    def getDatasetNames(self):
        return [d.getName() for d in self._precursors]

    def getAnalyses(self):
        return self._analyses

    def getSearchModes(self):
        return self._searchModes

    def getMCDataEras(self):
        return self._mcDataEras

    def getDataDataEras(self):
        return self._dataDataEras

    ## Return MC data eras, or data data eras if MC data era list is empty
    #
    # This is probably the typical use case when user wants "just the
    # list of available data eras".
    def getDataEras(self):
        if len(self._mcDataEras) > 0:
            return self._mcDataEras
        else:
            return self._dataDataEras

    def getOptimizationModes(self):
        return self._optimizationModes

    def getSystematicVariations(self):
        return self._systematicVariations

    def printAnalyses(self):
        print "Analyses (analysisName):"
        for a in self._analyses:
            print "  "+a
        print

        if len(self._searchModes) == 0:
            print "No search modes"
        else:
            print "Search modes (searchMode):"
            for s in self._searchModes:
                print "  "+s
        print
        
        if len(self._mcDataEras) == 0:
            print "No data eras in MC"
        else:
            print "Data eras (in MC) (dataEra):"
            for d in self._mcDataEras:
                print "  "+d
        print

        if len(self._dataDataEras) == 0:
            print "No data eras in data"
        else:
            print "Data eras (in data, the letters can be combined in almost any way) (dataEra):"
            for d in self._dataDataEras:
                print "  "+d
        print

        if len(self._optimizationModes) == 0:
            print "No optimization modes"
        else:
            print "Optimization modes (optimizationMode):"
            for o in self._optimizationModes:
                print "  "+o
        print

        if len(self._systematicVariations) == 0:
            print "No systematic variations"
        else:
            print "Systematic variations (systematicVariation):"
            for s in self._systematicVariations:
                print "  "+s
        print

    ## Close the ROOT files
    def close(self):
        for precursor in self._precursors:
            precursor.close()

## Helper class to plug NtupleCache to the existing framework
#
# User should not construct an object by herself, but use
# NtupleCahce.histogram()
class NtupleCacheDrawer:
    ## Constructor
    #
    # \param ntupleCache   NtupleCache object
    # \param histoName     Name of the histogram to obtain
    def __init__(self, ntupleCache, histoName):
        self.ntupleCache = ntupleCache
        self.histoName = histoName

    ## "Draw"
    #
    # \param datasetName  Dataset object
    #
    # This method exploits the infrastucture we have for TreeDraw.
    def draw(self, dataset):
        self.ntupleCache.process(dataset)
        return self.ntupleCache.getRootHisto(dataset, self.histoName)

## Ntuple processing with C macro and caching the result histograms
#
# 
class NtupleCache:
    ## Constructor
    #
    # \param treeName       Path to the TTree inside a ROOT file
    # \param selector       Name of the selector class, should also correspond a .C file in \a test/ntuple
    # \param selectorArgs   Optional arguments to the selector
    #                       constructor, can be a list of arguments,
    #                       or a function returning a list of
    #                       arguments
    # \param process        Should the ntuple be processed? (if False, results are read from the cache file)
    # \param cacheFileName  Path to the cache file
    # \param maxEvents      Maximum number of events to process (-1 for all events)
    # \param printStatus    Print processing status information
    #
    # I would like to make \a process redundant, but so far I haven't
    # figured out a bullet-proof method for that.
    def __init__(self, treeName, selector, selectorArgs=[], process=True, cacheFileName="histogramCache.root", maxEvents=-1, printStatus=True):
        self.treeName = treeName
        self.cacheFileName = cacheFileName
        self.selectorName = selector
        self.selectorArgs = selectorArgs
        self.doProcess = process
        self.maxEvents = maxEvents
        self.printStatus = printStatus

        self.datasetSelectorArgs = {}

        self.macrosLoaded = False
        self.processedDatasets = {}

        base = os.path.join(aux.higgsAnalysisPath(), "HeavyChHiggsToTauNu", "test", "ntuple")
        self.macros = [
            os.path.join(base, "BaseSelector.C"),
            os.path.join(base, "Branches.C"),
            os.path.join(base, self.selectorName+".C")
            ]

        self.cacheFile = None

    ## Compile and load the macros
    def _loadMacros(self):
        for m in self.macros:
            ret = ROOT.gROOT.LoadMacro(m+"+g")
            if ret != 0:
                raise Exception("Failed to load "+m)

    def setDatasetSelectorArgs(self, dictionary):
        self.datasetSelectorArgs.update(dictionary)

    # def _isMacroNewerThanCacheFile(self):
    #     latestMacroTime = max([os.path.getmtime(m) for m in self.macros])
    #     cacheTime = 0
    #     if os.path.exists(self.cacheFileName):
    #         cacheTime = os.path.getmtime(self.cacheFileName)
    #     return latestMacroTime > cacheTime

    ## Process selector for a dataset
    #
    # \param dataset  Dataset object
    def process(self, dataset):
        #if not self.forceProcess and not self._isMacroNewerThanCacheFile():
        #    return
        if not self.doProcess:
            return

        datasetName = dataset.getName()

        pathDigest = hashlib.sha1(dataset.getBaseDirectory()).hexdigest() # I hope this is good-enough
        procName = pathDigest+"_"+datasetName
        if procName in self.processedDatasets:
            return
        self.processedDatasets[procName] = 1

        if not self.macrosLoaded:
            self._loadMacros()
            self.macrosLoaded = True
        
        if self.cacheFile == None:
            self.cacheFile = ROOT.TFile.Open(self.cacheFileName, "RECREATE")
            self.cacheFile.cd()

        directory = self.cacheFile.Get(pathDigest)
        if directory == None:
            directory = self.cacheFile.mkdir(pathDigest)
            directory.cd()
            tmp = ROOT.TNamed("originalPath", dataset.getBaseDirectory())
            tmp.Write()

        # Create selector args
        selectorArgs = []
        if isinstance(self.selectorArgs, list):
            selectorArgs = self.selectorArgs[:]
            if dataset.getName() in self.datasetSelectorArgs:
                selectorArgs.extend(self.datasetSelectorArgs[dataset.getName()])
        else:
            # assume we have an object making a keyword->positional mapping
            sa = self.selectorArgs.clone()
            if dataset.getName() in self.datasetSelectorArgs:
                sa.update(self.datasetSelectorArgs[dataset.getName()])
            selectorArgs = sa.createArgs()

        directory = directory.mkdir(datasetName)
        argsNamed = ROOT.TNamed("selectorArgs", str(selectorArgs))
        argsNamed.Write()

        (tree, realTreeName) = dataset.createRootChain(self.treeName)

        N = tree.GetEntries()
        useMaxEvents = False
        if self.maxEvents >= 0 and N > self.maxEvents:
            useMaxEvents = True
            N = self.maxEvents
        selector = ROOT.SelectorImp(N, dataset.isMC(), getattr(ROOT, self.selectorName)(*selectorArgs))
        selector.setOutput(directory)
        selector.setPrintStatus(self.printStatus)

        print "Processing dataset", datasetName
        
        if useMaxEvents:
            tree.Process(selector, "", N)
        else:
            tree.Process(selector)
        directory.Write()

    ## Get a histogram from the cache file
    #
    # \param Datase        Dataset object for which histogram is to be obtained
    # \apram histoName     Histogram name
    def getRootHisto(self, dataset, histoName):
        if self.cacheFile == None:
            if not os.path.exists(self.cacheFileName):
                raise Exception("Assert: for some reason the cache file %s does not exist yet. Did you set 'process=True' in the constructor of NtupleCache?" % self.cacheFileName)
            self.cacheFile = ROOT.TFile.Open(self.cacheFileName)

        path = "%s/%s/%s" % (hashlib.sha1(dataset.getBaseDirectory()).hexdigest(), dataset.getName(), histoName)
        h = self.cacheFile.Get(path)
        if not h:
            raise Exception("Histogram '%s' not found from %s" % (path, self.cacheFile.GetName()))
        return h

    ## Create NtupleCacheDrawer for Dataset.getDatasetRootHisto()
    #
    # \param histoName   Histogram name to obtain
    def histogram(self, histoName):
        return NtupleCacheDrawer(self, histoName)


class SelectorArgs:
    def __init__(self, optionsDefaultValues, **kwargs):
        self.optionsDefaultValues = optionsDefaultValues

        args = {}
        args.update(kwargs)
        for option, defaultValue in self.optionsDefaultValues:
            value = None
            if option in args:
                value = args[option]
                del args[option]
            setattr(self, option, value)

        # Any remaining argument is an error
        if len(args) >= 1:
            raise Exception("Incorrect arguments for SelectorArgs.__init__(): %s" % ", ".join(args.keys()))

    def clone(self, **kwargs):
        c = copy.deepcopy(self)
        c.set(**kwargs)
        return c

    def set(self, **kwargs):
        for key, value in kwargs.iteritems():
            if not hasattr(self, key):
                raise Exception("This SelectorArgs does not have property %s" % key)
            setattr(self, key, value)

    def update(self, selectorArgs):
        for a, dv in self.optionsDefaultValues:
            val = getattr(selectorArgs, a)
            if val is not None:
                setattr(self, a, val)

    def createArgs(self):
        args = []
        for option, defaultValue in self.optionsDefaultValues:
            value = getattr(self, option)
            if value is None:
                value = defaultValue
            args.append(value)
        return args
