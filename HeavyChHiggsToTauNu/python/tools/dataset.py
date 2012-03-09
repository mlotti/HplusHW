## \package dataset
# Dataset utilities and classes
#
# This package contains classes and utilities for dataset management.
# There are also some functions and classes not directly related to
# dataset management, but are placed here due to some dependencies.

import glob, os, sys, re
import json
from optparse import OptionParser
import math

import ROOT

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab

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

    nameList = []
    for d in multiDirs:
        if isinstance(d, str):
            nameList.append( (os.path.join(d, "multicrab.cfg"), "") )
        else:
            nameList.append( (os.path.join(d[0], "multicrab.cfg"), d[1]) )

    datasets = DatasetManager()
    for cfg, postfix in nameList:
        d = getDatasetsFromMulticrabCfg(cfgfile=cfg, namePostfix=postfix, **kwargs)
        datasets.extend(d)
    return datasets

## Construct DatasetManager from a multicrab.cfg.
#
# \param kwargs   Keyword arguments (see below) 
#
# <b>Keyword arguments</b>
# \li \a opts       Optional OptionParser object. Should have options added with addOptions() and multicrab.addOptions().
# \li \a cfgfile    Path to the multicrab.cfg file (for default, see multicrab.getTaskDirectories())
# \li Rest are forwarded to getDatasetsFromCrabDirs()
#
# \return DatasetManager object
# 
# The section names in multicrab.cfg are taken as the dataset names
# in the DatasetManager object.
def getDatasetsFromMulticrabCfg(**kwargs):
    opts = kwargs.get("opts", None)
    taskDirs = []
    dirname = ""
    if "cfgfile" in kwargs:
        taskDirs = multicrab.getTaskDirectories(opts, kwargs["cfgfile"])
        dirname = os.path.dirname(kwargs["cfgfile"])
    else:
        taskDirs = multicrab.getTaskDirectories(opts)

    datasetMgr = getDatasetsFromCrabDirs(taskDirs, **kwargs)
    if len(dirname) > 0:
        datasetMgr._setBaseDirectory(dirname)
    return datasetMgr

## Construct DatasetManager from a list of CRAB task directory names.
# 
# \param taskdirs     List of strings for the CRAB task directories (relative
#                     to the working directory)
# \param kwargs       Keyword arguments (see below) 
# 
# <b>Keyword arguments</b>
# \li \a opts         Optional OptionParser object. Should have options added with addOptions() and multicrab.addOptions().
# \li \a namePostfix  Postfix for the dataset names (default: '')
# \li Rest are forwarded to getDatasetsFromRootFiles()
#
# \return DatasetManager object
# 
# The basename of the task directories are taken as the dataset
# names in the DatasetManager object (e.g. for directory '../Foo',
# 'Foo' will be the dataset name)
def getDatasetsFromCrabDirs(taskdirs, **kwargs):
    opts = None
    if "opts" in kwargs:
        opts = kwargs["opts"]
    else:
        parser = OptionParser(usage="Usage: %prog [options]")
        multicrab.addOptions(parser)
        addOptions(parser)
        (opts, args) = parser.parse_args()
    if hasattr(opts, "counterDir"):
        counters = opts.counterdir
    postfix = kwargs.get("namePostfix", "")

    dlist = []
    noFiles = False
    for d in taskdirs:
        files = glob.glob(os.path.join(d, "res", opts.input))
        if len(files) > 1:
            raise Exception("Only one file should match the input (%d matched) for task %s" % (len(files), d))
            return 1
        elif len(files) == 0:
            print >> sys.stderr, "Ignoring dataset %s: no files matched to '%s' in task directory %s" % (d, opts.input, os.path.join(d, "res"))
            noFiles = True
            continue

        dlist.append( (os.path.basename(d)+postfix, files[0]) )

    if noFiles:
        print >> sys.stderr, ""
        print >> sys.stderr, "  There were datasets without files. Have you merged the files with hplusMergeHistograms.py?"
        print >> sys.stderr, ""
        if len(dlist) == 0:
            raise Exception("No datasets. Have you merged the files with hplusMergeHistograms.py?")

    if len(dlist) == 0:
        raise Exception("No datasets from CRAB task directories %s" % ", ".join(taskdirs))

    return getDatasetsFromRootFiles(dlist, **kwargs)

## Construct DatasetManager from a list of CRAB task directory names.
# 
# \param rootFileList  List of (name, filename) pairs (both should be strings).
#                     'name' is taken as the dataset name, and 'filename' as
#                      the path to the ROOT file.
# \param kwargs        Keyword arguments (see below) 
# 
# <b>Keyword arguments</b>
# \li \a counters      String for a directory name inside the ROOT files for the event counter histograms (default: 'signalAnalysisCounters').
#
# \return DatasetManager object
def getDatasetsFromRootFiles(rootFileList, **kwargs):
    counters = kwargs.get("counters", "signalAnalysisCounters")
    dataQcd = kwargs.get("dataQcdMode", False)
    dataQcdNorm = kwargs.get("dataQcdNormalization", 1.0)
    datasets = DatasetManager()
    for name, f in rootFileList:
        dset = None
        if dataQcd:
            dset = DatasetQCDData(name, f, counters, dataQcdNorm)
        else:
            dset = Dataset(name, f, counters)
        datasets.append(dset)
    return datasets

## Add common dataset options to OptionParser object.
#
# \param parser   OptionParser object
def addOptions(parser):
    parser.add_option("-i", dest="input", type="string", default="histograms-*.root",
                      help="Pattern for input root files (note: remember to escape * and ? !) (default: 'histograms-*.root')")
    parser.add_option("-f", dest="files", type="string", action="append", default=[],
                      help="Give input ROOT files explicitly, if these are given, multicrab.cfg is not read and -d/-i parameters are ignored")
    parser.add_option("--counterDir", "-c", dest="counterdir", type="string", default="signalAnalysisCounters",
                      help="TDirectory name containing the counters (default: signalAnalysisCounters")


## Represents counter count value with uncertainty.
class Count:
    ## Constructor
    def __init__(self, value, uncertainty=0.0):
        self._value = value
        self._uncertainty = uncertainty

    def copy(self):
        return Count(self._value, self._uncertainty)

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

    ## self = self + count
    def add(self, count):
        self._value += count._value
        self._uncertainty = math.sqrt(self._uncertainty**2 + count._uncertainty**2)

    ## self = self - count
    def subtract(self, count):
        self.add(Count(-count._value, count._uncertainty))

    ## self = self * count
    def multiply(self, count):
        self._uncertainty = math.sqrt( (count._value * self._uncertainty)**2 +
                                       (self._value  * count._uncertainty)**2 )
        self._value = self._value * count._value

    ## self = self / count
    def divide(self, count):
        self._uncertainty = math.sqrt( (self._uncertainty / count._value)**2 +
                                       (self._value*count._uncertainty / (count._value**2) )**2 )
        self._value = self._value / count._value

    ## \var _value
    # Value of the count
    ## \var _uncertainty
    # Uncertainty of the count

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

    ## \var _value
    # Value of the count
    ## \var _uncertaintyLow
    # Lower uncertainty of the count (-)
    ## \var _uncertaintyHigh
    # Upper uncertainty of the count (+)

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


## Normalize TH1 to unit area.
# 
# \param h   TH1 histogram
# 
# \return Normalized histogram (same as the argument object, i.e. no copy is made).
def _normalizeToOne(h):
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


_th1_re = re.compile(">>\s*(?P<name>\S+)\s*\((?P<nbins>\S+)\s*,\s*(?P<min>\S+)\s*,\s*(?P<max>\S+)\s*\)")
_th1name_re = re.compile(">>\s*(?P<name>\S+)")
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
    #
    # If varexp is not given, the number of entries passing selection
    # is counted (ignoring weight). In this case the returned TH1 has
    # 1 bin, which contains the event count and the uncertainty of the
    # event count (calculated as sqrt(N)).
    def __init__(self, tree, varexp="", selection="", weight=""):
        self.tree = tree
        self.varexp = varexp
        self.selection = selection
        self.weight = weight

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
                "weight": self.weight}
        args.update(kwargs)

        # Allow modification functions
        for name, value in args.items():
            if hasattr(value, "__call__"):
                args[name] = value(getattr(self, name))

        return TreeDraw(**args)

    ## Prodouce TH1 from a file
    #
    # \param rootFile     TFile object containing the TTree
    # \param datasetName  Name of the dataset, the output TH1 contains
    #                     this in the name. Mainly needed for compatible interface with
    #                     dataset.TreeDrawCompound
    def draw(self, rootFile, datasetName):
        if self.varexp != "" and not ">>" in self.varexp:
            raise Exception("varexp should include explicitly the histogram binning (%s)"%self.varexp)

        selection = self.selection
        if len(self.weight) > 0:
            if len(selection) > 0:
                selection = "%s * (%s)" % (self.weight, selection)
            else:
                selection = self.weight

        tree = rootFile.Get(self.tree)
        if tree == None:
            raise Exception("No TTree '%s' in file %s" % (self.tree, rootFile.GetName()))

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
        m = _th1_re.search(varexp)
        h = None
        #if m:
        #    varexp = _th1_re.sub(">>"+m.group("name"), varexp)
        #    h = ROOT.TH1D(m.group("name"), varexp, int(m.group("nbins")), float(m.group("min")), float(m.group("max")))
        
        # e to have TH1.Sumw2() to be called before filling the histogram
        # goff to not to draw anything on the screen
        opt = ""
        if len(self.weight) > 0:
            opt = "e "
        nentries = tree.Draw(varexp, selection, opt+"goff")
        h = tree.GetHistogram()
        if h != None:
            h = h.Clone(h.GetName()+"_cloned")
        else:
            m = _th1_re.search(varexp)
            if m:
                h = ROOT.TH1F("tmp", varexp, int(m.group("nbins")), float(m.group("min")), float(m.group("max")))
            else:
                m = _th1name_re.search(varexp)
                if m:
                    h = ROOT.gDirectory.Get(m.group("name"))
                    h = h.Clone(h.GetName()+"_cloned")
                    if nentries == 0:
                        h.Scale(0)

                    if h == None:
                        raise Exception("Got null histogram for TTree::Draw() from file %s with selection '%s', unable to infer the histogram limits,  and did not find objectr from gDirectory, from the varexp %s" % (rootFile.GetName(), selection, varexp))
                else:
                    raise Exception("Got null histogram for TTree::Draw() from file %s with selection '%s', and unable to infer the histogram limits or name from the varexp %s" % (rootFile.GetName(), selection, varexp))

        h.SetName(datasetName+"_"+h.GetName())
        h.SetDirectory(0)
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
    # \param rootFile     TFile object containing the TTree
    # \param datasetName  Name of the dataset. Only needed for compatible interface with
    #                     dataset.TreeDrawCompound
    def draw(self, rootFile, datasetName):
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
    # \param rootFile     TFile object containing the TTree
    # \param datasetName  Name of the dataset.
    #
    # The dataset.TreeDraw for which the call is forwarded is searched from
    # the datasetMap with the datasetName. If found, that object is
    # used. If not found, the default TreeDraw is used.
    def draw(self, rootFile, datasetName):
        h = None
        if datasetName in self.datasetMap:
            #print "Dataset %s in datasetMap" % datasetName, self.datasetMap[datasetName].selection
            h = self.datasetMap[datasetName].draw(rootFile, datasetName)
        else:
            #print "Dataset %s with default" % datasetName, self.default.selection
            h = self.default.draw(rootFile, datasetName)
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
# merged data and MC histograms behind a common interface.
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
        return [x[0] for x in _histoToCounter(self.histo)]

    ## Modify the TH1 with a function
    #
    # \param function              Function taking the original TH1 and some other DatasetRootHisto object as input, returning a new TH1
    # \param newDatasetRootHisto   The other DatasetRootHisto object
    #
    # Needed for appending rows to counters from TTree
    def modifyRootHisto(self, function, newDatasetRootHisto):
        if not isinstance(newDatasetRootHisto, DatasetRootHisto):
            raise Exception("newDatasetRootHisto must be of the type DatasetRootHisto")

        self.histo = function(self.histo, newDatasetRootHisto.histo)

    ## Return normalized clone of the original TH1
    def _normalizedHistogram(self):
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


## Wrapper for a merged TH1 histograms from data and the corresponding Datasets.
#
# The merged data histograms can only be normalized 'to one'.
#
# \see dataset.DatasetRootHisto class.
class DatasetRootHistoMergedData(DatasetRootHistoBase):
    ## Constructor.
    # 
    # \param histoWrappers   List of dataset.DatasetRootHisto objects to merge
    # \param mergedDataset   The corresponding dataset.DatasetMerged object
    # 
    # The constructor checks that all histoWrappers are data, and
    # are not yet normalized.
    def __init__(self, histoWrappers, mergedDataset):
        DatasetRootHistoBase.__init__(self, mergedDataset)

        self.histoWrappers = histoWrappers
        self.normalization = "none"
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

    ## Modify the TH1 with a function
    #
    # \param function             Function taking the original TH1 and some other DatasetRootHisto object as input, returning a new TH1
    # \param newDatasetRootHisto  The other DatasetRootHisto object, must be the same type and contain same number of DatasetRootHisto objects
    #
    # Needed for appending rows to counters from TTree
    def modifyRootHisto(self, function, newDatasetRootHisto):
        if not isinstance(newDatasetRootHisto, DatasetRootHistoMergedData):
            raise Exception("newDatasetRootHisto must be of the type DatasetRootHistoMergedData")
        if not len(self.histoWrappers) == len(newDatasetRootHisto.histoWrappers):
            raise Exception("len(self.histoWrappers) != len(newDatasetrootHisto.histoWrappers), %d != %d" % len(self.histoWrappers), len(newDatasetRootHisto.histoWrappers))
            
        for i, drh in enumerate(self.histoWrappers):
            drh.modifyRootHisto(function, newDatasetRootHisto.histoWrappers[i])

    ## Get list of the bin labels of the first of the merged histogram.
    def getBinLabels(self):
        return self.histoWrappers[0].getBinLabels()

    ## Set the current normalization scheme to 'to one'.
    #
    # The histogram is normalized to unit area.
    def normalizeToOne(self):
        self.normalization = "toOne"

   ## Calculate the sum of the histograms (i.e. merge).
   # 
   # Intended for internal use only.
    def _getSumHistogram(self):
        hsum = self.histoWrappers[0].getHistogram() # we get a clone
        for h in self.histoWrappers[1:]:
            if h.getHistogram().GetNbinsX() != hsum.GetNbinsX():
                raise Exception("Histogram '%s' from datasets '%s' and '%s' have different binnings: %d vs. %d" % (hsum.GetName(), self.histoWrappers[0].getDataset().getName(), h.getDataset().getName(), hsum.GetNbinsX(), h.getHistogram().GetNbinsX()))

            hsum.Add(h.getHistogram())
        return hsum

    ## Merge the histograms and apply the current normalization.
    # 
    # The returned histogram is a clone, so client code can do
    # anything it wishes with it.
    def _normalizedHistogram(self):
        hsum = self._getSumHistogram()
        if self.normalization == "toOne":
            return _normalizeToOne(hsum)
        else:
            return hsum

    ## \var histoWrappers
    # List of underlying dataset.DatasetRootHisto objects
    ## \var normalization
    # String representing the current normalization scheme


## Wrapper for a merged TH1 histograms from MC and the corresponding Datasets.
# 
# See also the documentation of DatasetRootHisto class.
class DatasetRootHistoMergedMC(DatasetRootHistoBase):
    ## Constructor.
    # 
    # \param histoWrappers   List of dataset.DatasetRootHisto objects to merge
    # \param mergedDataset   The corresponding dataset.DatasetMerged object
    # 
    # The constructor checks that all histoWrappers are MC, and are
    # not yet normalized.
    def __init__(self, histoWrappers, mergedDataset):
        DatasetRootHistoBase.__init__(self, mergedDataset)
        self.histoWrappers = histoWrappers
        self.normalization = "none"
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

    ## Modify the TH1 with a function
    #
    # \param function   Function taking the original TH1 and some other DatasetRootHisto object as input, returning a new TH1
    # \param newDatasetRootHisto  The other DatasetRootHisto object, must be the same type and contain same number of DatasetRootHisto objects
    #
    # Needed for appending rows to counters from TTree
    def modifyRootHisto(self, function, newDatasetRootHisto):
        if not isinstance(newDatasetRootHisto, DatasetRootHistoMergedMC):
            raise Exception("newDatasetRootHisto must be of the type DatasetRootHistoMergedMC")
        if not len(self.histoWrappers) == len(newDatasetRootHisto.histoWrappers):
            raise Exception("len(self.histoWrappers) != len(newDatasetrootHisto.histoWrappers), %d != %d" % len(self.histoWrappers), len(newDatasetRootHisto.histoWrappers))
            
        for i, drh in enumerate(self.histoWrappers):
            drh.modifyRootHisto(function, newDatasetRootHisto.histoWrappers[i])

    ## Get list of the bin labels of the first of the merged histogram.
    def getBinLabels(self):
        return self.histoWrappers[0].getBinLabels()

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

        hsum = self.histoWrappers[0].getHistogram() # we get a clone
        for h in self.histoWrappers[1:]:
            if h.getHistogram().GetNbinsX() != hsum.GetNbinsX():
                raise Exception("Histogram '%s' from datasets '%s' and '%s' have different binnings: %d vs. %d" % (hsum.getHistogram().GetName(), self.histoWrappers[0].getHistogram().getName(), h.getDataset().getName(), hsum.GetNbinsX(), h.getHistogram().GetNbinsX()))

            hsum.Add(h.getHistogram())

        if self.normalization == "toOne":
            return _normalizeToOne(hsum)
        else:
            return hsum

    ## \var histoWrappers
    # List of underlying dataset.DatasetRootHisto objects
    ## \var normalization
    # String representing the current normalization scheme


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
   # \param name        Name of the dataset (can be anything)
   # \param fname       Path to the ROOT file of the dataset
   # \param counterDir  Name of the directory in the ROOT file for event
   #                    counter histograms. If None is given, it is
   #                    assumed that the dataset has no counters. This
   #                    also means that the histograms from this dataset
   #                    can not be normalized unless the number of all
   #                    events is explictly set with setNAllEvents()
   #                    method.
   # 
   # Opens the ROOT file, reads 'configInfo/configInfo' histogram
   # (if it exists), and reads the main event counter
   # ('counterDir/counters') if counterDir is not None. Reads also
   # 'configInfo/dataVersion' TNamed.
   # """
    def __init__(self, name, fname, counterDir):
        self.name = name
        self.file = ROOT.TFile.Open(fname)
        if self.file == None:
            raise Exception("Unable to open ROOT file '%s'"%fname)

        configInfo = self.file.Get("configInfo")
        if configInfo == None:
            raise Exception("configInfo directory is missing from file %s" % fname)

        self.info = _rescaleInfo(_histoToDict(self.file.Get("configInfo").Get("configinfo")))

        dataVersion = configInfo.Get("dataVersion")
        if dataVersion == None:
            raise Exception("Unable to determine dataVersion for dataset %s from file %s" % (name, fname))
        self.dataVersion = dataVersion.GetTitle()

        self._isData = "data" in self.dataVersion

        self.prefix = ""
        if counterDir != None:
            self.originalCounterDir = counterDir
            self._readCounter(counterDir)

    ## Close the file
    #
    # Can be useful when opening very many files in order to reduce
    # the memory footprint and not hit the limit of number of open
    # files
    def close(self):
#        print "Closing", self.file.GetName()
        self.file.Close("R")
        self.file.Delete()
        del self.file

    ## Read the number of all events from the event counters.
    # 
    # \param counterDir  Name of the directory for event counter histograms.
    # 
    # Reads 'counterDir/counters' histogram, and takes the value of
    # the first bin as the number of all events.
    # 
    # Intended for internal use only.
    def _readCounter(self, counterDir):
        if self.file.Get(counterDir) == None:
            raise Exception("Unable to find directory '%s' from ROOT file '%s'" % (counterDir, self.file.GetName()))
        ctr = _histoToCounter(self.file.Get(counterDir).Get("counter"))
        self.nAllEvents = ctr[0][1].value() # first counter, second element of the tuple
        self.counterDir = counterDir

    ## Set a prefix for the directory access.
    # 
    # \param prefix   Prefix for event counter and histogram directories.
    # 
    # The number of all events (for normalization) are re-read from
    # a directory prefix+original_counter_directory. The prefix is
    # also used for the histogram paths in getHistogram() method.
    # 
    # The use case is the following:
    # \li The same analysis is run many times with different
    #     parameters in one CMSSW jobs. The different analyses have
    #     different prefixes but the same base name (e.g. 'analysis,
    #     'foo1analysis', 'foo2analysis' etc.)
    # \li The different analyses can then be selected easily by
    #     calling this method with a prefix
    def setPrefix(self, prefix):
        self.prefix = prefix
        self._readCounter(prefix+self.originalCounterDir)

    def getPrefix(self):
        return self.prefix

    ## Clone the Dataset object
    # 
    # Nothing is shared between the returned copy and this object.
    #
    # Use case is creative dataset manipulations, e.g. copying ttbar
    # to another name and scaling the cross section by the BR(t->H+)
    # while also keeping the original ttbar with the original SM cross
    # section.
    def deepCopy(self):
        d = Dataset(self.name, self.file.GetName(), self.counterDir)
        d.info.update(self.info)
        return d

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

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

    def isData(self):
        return self._isData

    def isMC(self):
        return not self._isData

    def getCounterDirectory(self):
        return self.originalCounterDir

    ## Set the number of all events (for normalization).
    #
    # This allows both overriding the value read from the event
    # counter, or creating a dataset without event counter at all.
    def setNAllEvents(self, nAllEvents):
        self.nAllEvents = nAllEvents

    def getNAllEvents(self):
        return self.nAllEvents

    ## Get the cross section normalization factor.
    #
    # The normalization factor is defined as crossSection/N(all
    # events), so by multiplying the number of MC events with the
    # factor one gets the corresponding cross section.
    def getNormFactor(self):
        if not hasattr(self, "nAllEvents"):
            raise Exception("Number of all events is not set for dataset %s! The counter directory was not given, and setNallEvents() was not called." % self.name)
        if self.nAllEvents == 0:
            raise Exception("Number of all events is 0 for dataset %s" % self.name)

        return self.getCrossSection() / self.nAllEvents

    ## Check if a ROOT histogram exists in this dataset
    #
    # \param name  Name (path) of the ROOT histogram
    #
    # If dataset.TreeDraw object is given, it is considered to always
    # exist.
    def hasRootHisto(self, name):
        if hasattr(name, "draw"):
            return True
        pname = self.prefix+name
        return self.file.Get(pname) != None

    ## Get the dataset.DatasetRootHisto object for a named histogram.
    # 
    # \param name   Path of the histogram in the ROOT file
    #
    # \return dataset.DatasetRootHisto object containing the (unnormalized) TH1 and this Dataset
    # 
    # If the prefix is set (setPrefix() method), it is prepended to
    # the name before TFile.Get() call.
    #
    # If dataset.TreeDraw object is given (or actually anything with
    # draw() method), the draw() method is called by giving the TFile
    # and the dataset name as parameters. The draw() method is
    # expected to return a TH1 which is then returned.
    def getDatasetRootHisto(self, name):
        h = None
        if hasattr(name, "draw"):
            h = name.draw(self.file, self.getName())
        else:
            pname = self.prefix+name
            h = self.file.Get(pname)
            if h == None:
                raise Exception("Unable to find histogram '%s' from file '%s'" % (pname, self.file.GetName()))

            name = h.GetName()+"_"+self.name
            h.SetName(name.translate(None, "-+.:;"))
        return DatasetRootHisto(h, self)

    ## Get the directory content of a given directory in the ROOT file.
    # 
    # \param directory   Path of the directory in the ROOT file
    # \param predicate   Append the directory name to the return list only if
    #                    predicate returns true for the name. Predicate
    #                    should be a function taking a string as an
    #                    argument and returning a boolean.
    # 
    # \return List of names in the directory.
    # 
    # If the prefix is set (setPrefix() method), it is prepended to
    # the bame before TFile.Get() call.
    def getDirectoryContent(self, directory, predicate=lambda x: True):
        d = self.file.Get(self.prefix+directory)
        if d == None:
            raise Exception("No object %s in file %s" % (self.prefix+directory, self.file.GetName()))
        dirlist = d.GetListOfKeys()

        # Suppress the warning message of missing dictionary for some iterator
        backup = ROOT.gErrorIgnoreLevel
        ROOT.gErrorIgnoreLevel = ROOT.kError
        diriter = dirlist.MakeIterator()
        ROOT.gErrorIgnoreLevel = backup

        key = diriter.Next()

        ret = []
        while key:
            if predicate(key.ReadObj()):
                ret.append(key.GetName())
            key = diriter.Next()
        return ret

    ## \var name
    # Name of the dataset
    ## \var file
    # TFile object of the dataset
    ## \var info
    # Dictionary containing the configInfo histogram
    ## \var dataVersion
    # dataVersion string of the dataset (from TFile)
    ## \var prefix
    # Prefix for TDirectory access, see setPrefix()
    ## \var originalCounterDir
    # Original counter directory, see setPrefix()
    ## \var nAllEvents
    # Number of all MC events, used in MC normalization
    ## \var counterDir
    # Name of TDirectory containing the main event counter
    ## \var _isData
    # If true, dataset is from data, if false, from MC

## Maybe unnecessary class?
#
# This is some old trial for implementing a dataset class for the
# data-driven QCD measurement. Development was never finished.
class DatasetQCDData(Dataset):
    def __init__(self, name, fname, counterDir, normfactor=1.0):
        Dataset.__init__(self, name, fname, counterDir)
        self.normfactor = normfactor

    def deepCopy(self):
        d = DatasetQCDData(self.name, self.file.GetName(), self.counterDir, self.normfactor)
        d.info.update(self.info)
        d._isData = self._isData
        return d

    def changeTypeToMC(self):
        self._isData = False

    def getDatasetRootHisto(self, name):
        drh = Dataset.getDatasetRootHisto(self, name)
        drh.scale(self.normfactor)
        return drh

    def setNormFactor(self, normfactor):
        self.normfactor = normfactor

    def setNormFactorFromTree(self, treeDraw, targetNumEvents):
        drh = Dataset.getDatasetRootHisto(self, treeDrawToNumEntries(treeDraw))
        nevents = drh.histo.Integral(0, drh.histo.GetNbinsX()+1)
        self.setNormFactor(targetNumEvents/nevents)

    # Overloads needed for this ugly hack
    def getCrossSection(self):
        return 0

    def setCrossSection(self):
        raise Exception("Assert that this is not called for DatasetQCDData")
        

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

    ## Set a prefix for the directory access.
    # 
    # \param prefix   Prefix for event counter and histogram directories.
    # 
    # \see dataset.Dataset.setPrefix()
    def setPrefix(self, prefix):
        for d in self.datasets:
            d.setPrefix(prefix)

    def getPrefix(self):
        prefix = None
        for d in self.datasets:
            if prefix == None:
                prefix = d.getPrefix()
            elif prefix != d.getPrefix():
                raise Exception("Internal error")
        return prefix
 
    ## Make a deep copy of a DatasetMerged object.
    #
    # Nothing is shared between the returned copy and this object.
    #
    # \see dataset.Dataset.deepCopy()
    def deepCopy(self):
        dm = DatasetMerged(self.name, [d.deepCopy() for d in self.datasets])
        dm.info.update(self.info)
        return dm

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

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
    def getDatasetRootHisto(self, name):
        wrappers = [d.getDatasetRootHisto(name) for d in self.datasets]
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

    ## \var name
    # Name of the merged dataset
    ## \var datasets
    # List of merged dataset.Dataset objects
    ## \var info
    # Dictionary containing total cross section (MC) or integrated luminosity (data)

## Collection of Dataset objects which are managed together.
# 
# Holds both an ordered list of Dataset objects, and a name->object
# map for convenient access by dataset name.
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
        self.basedir = base

    ## Populate the datasetMap member from the datasets list.
    # 
    # Intended only for internal use.
    def _populateMap(self):
        self.datasetMap = {}
        for d in self.datasets:
            self.datasetMap[d.getName()] = d

    def _setBaseDirectory(self, base):
        self.basedir = base

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

    def hasDataset(self, name):
        return name in self.datasetMap

    def getDataset(self, name):
        return self.datasetMap[name]

    ## Get a list of dataset.DatasetRootHisto objects for a given name.
    # 
    # \param histoName   Path to the histogram in each ROOT file.
    #
    # \see dataset.Dataset.getDatasetRootHisto()
    def getDatasetRootHistos(self, histoName):
        return [d.getDatasetRootHisto(histoName) for d in self.datasets]

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
    #
    # If nameList translates to only one dataset.Dataset, the
    # dataset.Daataset object is renamed (i.e. dataset.DatasetMerged
    # object is not created)
    def merge(self, newName, nameList, keepSources=False):
        (selected, notSelected, firstIndex) = _mergeStackHelper(self.datasets, nameList, "merge")
        if len(selected) == 0:
            print >> sys.stderr, "Dataset merge: no datasets '" +", ".join(nameList) + "' found, not doing anything"
            return
        elif len(selected) == 1:
            print >> sys.stderr, "Dataset merge: one dataset '" + selected[0].getName() + "' found from list '" + ", ".join(nameList)+"', renaming it to '%s'" % newName
            self.rename(selected[0].getName(), newName)
            return

        if not keepSources:
            self.datasets = notSelected
        self.datasets.insert(firstIndex, DatasetMerged(newName, selected))
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
        if len(os.path.dirname(fname)) == 0:
            fname = os.path.join(self.basedir, fname)

        if not os.path.exists(fname):
            print >> sys.stderr, "WARNING: luminosity json file '%s' doesn't exist!" % fname

        data = json.load(open(fname))
        for name, value in data.iteritems():
            if self.hasDataset(name):
                self.getDataset(name).setLuminosity(value)

    ## Print dataset information.
    def printInfo(self):
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

        print (c1fmt%col1hdr)+"  "+col2hdr+"  "+col3hdr+"  "+col4hdr
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
            print line


    ## \var datasets
    # List of dataset.Dataset (or dataset.DatasetMerged) objects to manage
    ## \var datasetMap
    # Dictionary from dataset names to dataset.Dataset objects, for
    # more straightforward accessing of dataset.Dataset objects by
    # their name.
    ## \var basedir
    # Directory (absolute/relative to current working directory) where
    # the luminosity JSON file is located (see loadLuminosities())
