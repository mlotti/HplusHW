import glob, os, sys, re
import json
from optparse import OptionParser
import math

import ROOT

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab

def getDatasetsFromMulticrabDirs(multiDirs, **kwargs):
    """Construct DatasetManager from a list of MultiCRAB directory names.

    Arguments:
    multiDirs   List of strings or pairs of strings of the MultiCRAB
                directories (relative to the working directory). If
                the item of the list is pair of strings, the first
                element is the directory, and the second element is
                the postfix for the dataset names from that directory.

    Keyword arguments:

    See getDatasetsFromMulticrabCfg() for the rest of the keyword arguments.
    """

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

def getDatasetsFromMulticrabCfg(**kwargs):
    """Construct DatasetManager from a multicrab.cfg.

    Keyword Arguments:
    opts       Optional OptionParser object. Should have options added with
               addOptions() and multicrab.addOptions().
    cfgfile    Path to the multicrab.cfg file (for default, see multicrab.getTaskDirectories())

    See getDatasetsFromCrabDirs() for the rest of the keyword argumens.


    The section names in multicrab.cfg are taken as the dataset names
    in the DatasetManager object.
    """
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

def getDatasetsFromCrabDirs(taskdirs, **kwargs):
    """Construct DatasetManager from a list of CRAB task directory names.

    Arguments:
    taskdirs     List of strings for the CRAB task directories (relative
                 to the working directory)

    Keyword arguments:
    opts         Optional OptionParser object. Should have options added with
                 addOptions() and multicrab.addOptions().
    namePostfix  Postfix for the dataset names (default: '')

    See getDatasetsFromRootFiles() for rest of the keyword arguments.

    The basename of the task directories are taken as the dataset
    names in the DatasetManager object (e.g. for directory '../Foo',
    'Foo' will be the dataset name)
    """
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

def getDatasetsFromRootFiles(rootFileList, **kwargs):
    """Construct DatasetManager from a list of CRAB task directory names.

    Arguments:
    rootFileList  List of (name, filename) pairs (both should be strings).
                  'name' is taken as the dataset name, and 'filename' as
                  the path to the ROOT file.

    Keyword arguments:
    counters      String for a directory name inside the ROOT files for the
                  event counter histograms (default: 'signalAnalysisCounters').
    """
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

def addOptions(parser):
    """Add common dataset options to OptionParser object."""
    parser.add_option("-i", dest="input", type="string", default="histograms-*.root",
                      help="Pattern for input root files (note: remember to escape * and ? !) (default: 'histograms-*.root')")
    parser.add_option("-f", dest="files", type="string", action="append", default=[],
                      help="Give input ROOT files explicitly, if these are given, multicrab.cfg is not read and -d/-i parameters are ignored")
    parser.add_option("--counterDir", "-c", dest="counterdir", type="string", default="signalAnalysisCounters",
                      help="TDirectory name containing the counters (default: signalAnalysisCounters")



class Count:
    """Represents counter count value with uncertainty."""
    def __init__(self, value, uncertainty):
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

    def add(self, count):
        """self = self + count"""
        self._value += count._value
        self._uncertainty = math.sqrt(self._uncertainty**2 + count._uncertainty**2)

    def subtract(self, count):
        """self = self - count"""
        self.add(Count(-count._value, count._uncertainty))

    def multiply(self, count):
        """self = self * count"""
        self._uncertainty = math.sqrt( (count._value * self._uncertainty)**2 +
                                       (self._value  * count._uncertainty)**2 )
        self._value = self._value * count._value

    def divide(self, count):
        """self = self / count"""
        self._uncertainty = math.sqrt( (self._uncertainty / count._value)**2 +
                                       (self._value*count._uncertainty / (count._value**2) )**2 )
        self._value = self._value / count._value

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

def histoIntegrateToCount(histo):
    count = Count(0, 0)
    for bin in xrange(0, histo.GetNbinsX()+2):
        count.add(Count(histo.GetBinContent(bin), histo.GetBinError(bin)))
    return count

def _rescaleInfo(d):
    """Rescales info dictionary.

    Assumes that d has a 'control' key for a numeric value, and then
    normalizes all items in the dictionary such that the 'control'
    becomes one.

    The use case is to have a dictionary from _histoToDict() function,
    where the original histogram is merged from multiple jobs. It is
    assumed that each histogram as a one bin with 'control' label, and
    the value of this bin is 1 for each job. Then the bin value for
    the merged histogram tells the number of jobs. Naturally the
    scheme works correctly only if the histograms from jobs are
    identical, and hence is appropriate only for dataset-like
    information.
    """
    factor = 1/d["control"]

    ret = {}
    for k, v in d.iteritems():
        ret[k] = v*factor

    return ret


def _normalizeToOne(h):
    """Normalize TH1 to unit area.

    Parameters:
    h   TH1 histogram

    Returns the normalized histogram (which is the same as the
    parameter, i.e. no copy is made).
    """
    return _normalizeToFactor(h, 1.0/h.Integral())

def _normalizeToFactor(h, f):
    """Scale TH1 with a given factor.

    Parameters:
    h   TH1 histogram
    f   Scale factor

    TH1.Sumw2() is called before the TH1.Scale() in order to scale the
    histogram errors correctly.
    """
    backup = ROOT.gErrorIgnoreLevel
    ROOT.gErrorIgnoreLevel = ROOT.kError
    h.Sumw2() # errors are also scaled after this call 
    ROOT.gErrorIgnoreLevel = backup
    h.Scale(f)
    return h


def _mergeStackHelper(datasetList, nameList, task):
    """Helper function for merging/stacking a set of datasets.

    Parameters:
    datasetList  List of all Dataset objects to consider
    nameList     List of the names of Dataset objects to merge/stack
    task         String to identify merge/stack task (can be 'stack' or 'merge')

    Returns a triple of:
    - list of selected Dataset objects
    - list of non-selected Dataset objects
    - index of the first selected Dataset object in the original list
      of all Datasets

    The Datasets to merge/stack are selected from the list of all
    Datasets, and it is checked that all of them are either data or MC
    (i.e. merging/stacking of data and MC datasets is forbidden).
    """
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


th1_re = re.compile(">>\s*(?P<name>\S+)\s*\((?P<nbins>\S+)\s*,\s*(?P<min>\S+)\s*,\s*(?P<max>\S+)\s*\)")
th1name_re = re.compile(">>\s*(?P<name>\S+)")
class TreeDraw:
    def __init__(self, tree, varexp="", selection="", weight=""):
        self.tree = tree
        self.varexp = varexp
        self.selection = selection
        self.weight = weight

    def clone(self, **kwargs):
        args = {"tree": self.tree,
                "varexp": self.varexp,
                "selection": self.selection,
                "weight": self.weight}
        args.update(kwargs)
        return TreeDraw(**args)

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
        if self.varexp == "":
            nentries = tree.GetEntries(selection)
            h = ROOT.TH1F("nentries", "Number of entries by selection %s"%selection, 1, 0, 1)
            h.SetDirectory(0)
            h.Sumw2()
            h.SetBinContent(1, nentries)
            h.SetBinError(1, math.sqrt(nentries))
            return h

        varexp = self.varexp
        m = th1_re.search(varexp)
        h = None
        #if m:
        #    varexp = th1_re.sub(">>"+m.group("name"), varexp)
        #    h = ROOT.TH1D(m.group("name"), varexp, int(m.group("nbins")), float(m.group("min")), float(m.group("max")))
        
        # e to have TH1.Sumw2() to be called before filling the histogram
        # goff to not to draw anything on the screen
        nentries = tree.Draw(varexp, selection, "e goff")
        h = tree.GetHistogram()
        if h != None:
            h = h.Clone(h.GetName()+"_cloned")
        else:
            m = th1_re.search(varexp)
            if m:
                h = ROOT.TH1F("tmp", varexp, int(m.group("nbins")), float(m.group("min")), float(m.group("max")))
            else:
                m = th1name_re.search(varexp)
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

class TreeDrawCompound:
    def __init__(self, default, datasetMap={}):
        self.default = default
        self.datasetMap = datasetMap

    def add(self, datasetName, treeDraw):
        self.datasetMap[datasetName] = treeDraw

    def draw(self, rootFile, datasetName):
        h = None
        if datasetName in self.datasetMap:
            #print "Dataset %s in datasetMap" % datasetName, self.datasetMap[datasetName].selection
            h = self.datasetMap[datasetName].draw(rootFile, datasetName)
        else:
            #print "Dataset %s with default" % datasetName, self.default.selection
            h = self.default.draw(rootFile, datasetName)
        return h

    def clone(self, **kwargs):
        ret = TreeDrawCompound(self.default.clone(**kwargs))
        for name, td in self.datasetMap.iteritems():
            ret.datasetMap[name] = td.clone(**kwargs)
        return ret

def _treeDrawToNumEntriesSingle(treeDraw):
    var = treeDraw.weight
    if var == "":
        var = treeDraw.selection
    if var != "":
        var += ">>dist(1,0,2)" # the binning is arbitrary, as the under/overflow bins are counted too
    # if selection and weight are "", TreeDraw.draw() returns a histogram with the number of entries
    return treeDraw.clone(varexp=var)

def treeDrawToNumEntries(treeDraw):
    if isinstance(treeDraw, TreeDrawCompound):
        td = TreeDrawCompound(_treeDrawToNumEntriesSingle(treeDraw.default))
        for name, td2 in treeDraw.datasetMap.iteritems():
            td.add(name, _treeDrawToNumEntriesSingle(td2))
        return td
    else:
        return _treeDrawToNumEntriesSingle(treeDraw)

class DatasetRootHistoBase:
    """Base class for DatasetRootHisto classes.

    The derived class must implement

    _normalizedHistogram()

    which should return the cloned and normalized TH1
    """
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

    def getHistogram(self):
        """Get a clone of the wrapped histogram normalized correctly."""
        h = self._normalizedHistogram()

        if self.multiplication != None:
            h = _normalizeToFactor(h, self.multiplication)
        return h

    def scale(self, value):
        """Scale the histogram bin values with a value.

        Arguments:
        value    Value to multiply with

        h = h*value
        """
        if self.multiplication == None:
            self.multiplication = value
        else:
            self.multiplication *= value

class DatasetRootHisto(DatasetRootHistoBase):
    """Wrapper for a single TH1 histogram and the corresponding Dataset.

    The wrapper holds the normalization of the histogram. User should
    set the current normalization scheme with the normalize* methods,
    and then get a clone of the original histogram, which is then
    normalized according to the current scheme.

    This makes the class very flexible with respect to the many
    possible normalizations user could want to apply within a plot
    script. The first use case was MC counters, which could be printed
    first normalized to the luminosity of the data, and also
    normalized to the cross section.

    The histogram wrapper classes also abstract the signel histogram, and
    merged data and MC histograms behind a common interface.
    """

    def __init__(self, histo, dataset):
        """Constructor.

        Parameters:
        histo    TH1 histogram
        dataset  Corresponding Dataset object

        Sets the initial normalization to 'none'
        """
        DatasetRootHistoBase.__init__(self, dataset)
        self.histo = histo
        self.normalization = "none"

    def getBinLabels(self):
        """Get list of the bin labels of the histogram."""
        return [x[0] for x in _histoToCounter(self.histo)]

    def modifyRootHisto(self, function, newDatasetRootHisto):
        if not isinstance(newDatasetRootHisto, DatasetRootHisto):
            raise Exception("newDatasetRootHisto must be of the type DatasetRootHisto")

        self.histo = function(self.histo, newDatasetRootHisto.histo)

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

    def normalizeToOne(self):
        """Set the current normalization scheme to 'to one'.

        The histogram is normalized to unit area.
        """
        self.normalization = "toOne"

    def normalizeByCrossSection(self):
        """Set the current normalization scheme to 'by cross section'.

        The histogram is normalized to the cross section of the
        corresponding dataset. The normalization can be applied only
        to MC histograms.
        """

        if self.dataset.isData():
            raise Exception("Can't normalize data histogram by cross section")
        self.normalization = "byCrossSection"

    def normalizeToLuminosity(self, lumi):
        """Set the current normalization scheme to 'to luminosity'.

        Parameters:
        lumi   Integrated luminosity in pb^-1 to normalize to

        The histogram is normalized first normalized to the cross
        section of the corresponding dataset, and then to a given
        luminosity. The normalization can be applied only to MC
        histograms.
        """

        if self.dataset.isData():
            raise Exception("Can't normalize data histogram to luminosity")

        self.normalization = "toLuminosity"
        self.luminosity = lumi

class DatasetRootHistoMergedData(DatasetRootHistoBase):
    """Wrapper for a merged TH1 histograms from data and the corresponding Datasets.

    The merged data histograms can only be normalized 'to one'.

    See also the documentation of DatasetRootHisto class.
    """

    def __init__(self, histoWrappers, mergedDataset):
        """Constructor.

        Parameters:
        histoWrappers   List of DatasetRootHisto objects to merge
        mergedDataset   The corresponding DatasetMerged object

        The constructor checks that all histoWrappers are data, and
        are not yet normalized.
        """
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

    def modifyRootHisto(self, function, newDatasetRootHisto):
        if not isinstance(newDatasetRootHisto, DatasetRootHistoMergedData):
            raise Exception("newDatasetRootHisto must be of the type DatasetRootHistoMergedData")
        if not len(self.histoWrappers) == len(newDatasetRootHisto.histoWrappers):
            raise Exception("len(self.histoWrappers) != len(newDatasetrootHisto.histoWrappers), %d != %d" % len(self.histoWrappers), len(newDatasetRootHisto.histoWrappers))
            
        for i, drh in enumerate(self.histoWrappers):
            drh.modifyRootHisto(function, newDatasetRootHisto.histoWrappers[i])

    def getBinLabels(self):
        """Get list of the bin labels of the first of the merged histogram."""
        return self.histoWrappers[0].getBinLabels()

    def normalizeToOne(self):
        """Set the current normalization scheme to 'to one'.

        The histogram is normalized to unit area.
        """
        self.normalization = "toOne"

    def _getSumHistogram(self):
        """Calculate the sum of the histograms (i.e. merge).

        Intended for internal use only.
        """
        hsum = self.histoWrappers[0].getHistogram() # we get a clone
        for h in self.histoWrappers[1:]:
            if h.getHistogram().GetNbinsX() != hsum.GetNbinsX():
                raise Exception("Histogram '%s' from datasets '%s' and '%s' have different binnings: %d vs. %d" % (hsum.GetName(), self.histoWrappers[0].getDataset().getName(), h.getDataset().getName(), hsum.GetNbinsX(), h.getHistogram().GetNbinsX()))

            hsum.Add(h.getHistogram())
        return hsum

    def _normalizedHistogram(self):
        """Merge the histograms and apply the current normalization.

        The returned histogram is a clone, so client code can do
        anything it wishes with it.
        """
        hsum = self._getSumHistogram()
        if self.normalization == "toOne":
            return _normalizeToOne(hsum)
        else:
            return hsum

class DatasetRootHistoMergedMC(DatasetRootHistoBase):
    """Wrapper for a merged TH1 histograms from MC and the corresponding Datasets.

    See also the documentation of DatasetRootHisto class.
    """
    def __init__(self, histoWrappers, mergedDataset):
        """Constructor.

        Parameters:
        histoWrappers   List of DatasetRootHisto objects to merge
        mergedDataset   The corresponding DatasetMerged object

        The constructor checks that all histoWrappers are MC, and are
        not yet normalized.
        """
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

    def modifyRootHisto(self, function, newDatasetRootHisto):
        if not isinstance(newDatasetRootHisto, DatasetRootHistoMergedMC):
            raise Exception("newDatasetRootHisto must be of the type DatasetRootHistoMergedMC")
        if not len(self.histoWrappers) == len(newDatasetRootHisto.histoWrappers):
            raise Exception("len(self.histoWrappers) != len(newDatasetrootHisto.histoWrappers), %d != %d" % len(self.histoWrappers), len(newDatasetRootHisto.histoWrappers))
            
        for i, drh in enumerate(self.histoWrappers):
            drh.modifyRootHisto(function, newDatasetRootHisto.histoWrappers[i])

    def getBinLabels(self):
        """Get list of the bin labels of the first of the merged histogram."""
        return self.histoWrappers[0].getBinLabels()

    def normalizeToOne(self):
        """Set the current normalization scheme to 'to one'.

        The histogram is normalized to unit area.

        Sets the normalization of the underlying histoWrappers to 'by
        cross section' in order to be able to sum them. The
        normalization 'to one' is then done for the summed histogram.
        """
        self.normalization = "toOne"
        for h in self.histoWrappers:
            h.normalizeByCrossSection()

    def normalizeByCrossSection(self):
        """Set the current normalization scheme to 'by cross section'.

        The histogram is normalized to the cross section of the
        corresponding dataset.

        Sets the normalization of the underlying histoWrappers to 'by
        cross section'. Then they can be summed directly, and the
        summed histogram is automatically correctly normalized to the
        total cross section of the merged Datasets.
        """
        self.normalization = "byCrossSection"
        for h in self.histoWrappers:
            h.normalizeByCrossSection()

    def normalizeToLuminosity(self, lumi):
        """Set the current normalization scheme to 'to luminosity'.

        Parameters:
        lumi   Integrated luminosity in pb^-1 to normalize to

        The histogram is normalized first normalized to the cross
        section of the corresponding dataset, and then to a given
        luminosity.

        Sets the normalization of the underlying histoWrappers to 'to
        luminosity'. Then they can be summed directly, and the summed
        histogram is automatically correctly normalized to the given
        integrated luminosity.
        """
        self.normalization = "toLuminosity"
        for h in self.histoWrappers:
            h.normalizeToLuminosity(lumi)

    def _normalizedHistogram(self):
        """Merge the histograms and apply the current normalization.

        The returned histogram is a clone, so client code can do
        anything it wishes with it.

        The merged MC histograms must be normalized in some way,
        otherwise they can not be summed (or they can be, but the
        contents of the summed histogram doesn't make any sense as it
        is just the sum of the MC events of the separate datasets
        which in general have different cross sections).
        """
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


class Dataset:
    """Dataset class for histogram access from one ROOT file.

    The default values for cross section/luminosity are read from
    'configInfo/configInfo' histogram (if it exists). The data/MC
    datasets are differentiated by the existence of 'crossSection'
    (for MC) and 'luminosity' (for data) keys in the histogram. Reads
    the dataVersion from 'configInfo/dataVersion' and deduces whether
    the dataset is data/MC from it.
    """

    def __init__(self, name, fname, counterDir):
        """Constructor.

        Parameters:
        name        Name of the dataset (can be anything)
        fname       Path to the ROOT file of the dataset
        counterDir  Name of the directory in the ROOT file for event
                    counter histograms. If None is given, it is
                    assumed that the dataset has no counters. This
                    also means that the histograms from this dataset
                    can not be normalized unless the number of all
                    events is explictly set with setNAllEvents()
                    method.

        Opens the ROOT file, reads 'configInfo/configInfo' histogram
        (if it exists), and reads the main event counter
        ('counterDir/counters') if counterDir is not None. Reads also
        'configInfo/dataVersion' TNamed.
        """

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

    def _readCounter(self, counterDir):
        """Read the number of all events from the event counters.

        Parameters:
        counterDir  Name of the directory for event counter histograms.

        Reads 'counterDir/counters' histogram, and takes the value of
        the first bin as the number of all events.

        Intended for internal use only.
        """

        if self.file.Get(counterDir) == None:
            raise Exception("Unable to find directory '%s' from ROOT file '%s'" % (counterDir, self.file.GetName()))
        ctr = _histoToCounter(self.file.Get(counterDir).Get("counter"))
        self.nAllEvents = ctr[0][1].value() # first counter, second element of the tuple
        self.counterDir = counterDir

    def setPrefix(self, prefix):
        """Set a prefix for the directory access.

        Parameters:
        prefix   Prefix for event counter and histogram directories.

        The number of all events (for normalization) are re-read from
        a directory prefix+original_counter_directory. The prefix is
        also used for the histogram paths in getHistogram() method.

        The use case is the following:
        - The same analysis is run many times with different
          parameters in one CMSSW jobs. The different analyses have
          different prefixes but the same base name (e.g. 'analysis,
          'foo1analysis', 'foo2analysis' etc.)
        - The different analyses can then be selected easily by
          calling this method with a prefix
        """
        self.prefix = prefix
        self._readCounter(prefix+self.originalCounterDir)

    def getPrefix(self):
        return self.prefix

    def deepCopy(self):
        """Make a deep copy of a Dataset object.

        Nothing is shared between the returned copy and this object.
        """
        d = Dataset(self.name, self.file.GetName(), self.counterDir)
        d.info.update(self.info)
        return d

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def setCrossSection(self, value):
        """Set cross section of MC dataset (in pb)."""
        if not self.isMC():
            raise Exception("Should not set cross section for data dataset %s" % self.name)
        self.info["crossSection"] = value

    def getCrossSection(self):
        """Get cross section of MC dataset (in pb)."""
        if not self.isMC():
            raise Exception("Dataset %s is data, no cross section available" % self.name)
        try:
            return self.info["crossSection"]
        except KeyError:
            raise Exception("Dataset %s is MC, but 'crossSection' is missing from configInfo/configInfo histogram. You have to explicitly set the cross section with setCrossSection() method." % self.name)

    def setLuminosity(self, value):
        """Set the integrated luminosity of data dataset (in pb^-1)."""
        if not self.isData():
            raise Exception("Should not set luminosity for MC dataset %s" % self.name)
        self.info["luminosity"] = value

    def getLuminosity(self):
        """Get the integrated luminosity of data dataset (in pb^-1)."""
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

    def setNAllEvents(self, nAllEvents):
        """Set the number of all events (for normalization).

        This allows both overriding the value read from the event
        counter, or creating a dataset without event counter at all.
        """
        self.nAllEvents = nAllEvents

    def getNormFactor(self):
        """Get the cross section normalization factor.

        The normalization factor is defined as crossSection/N(all
        events), so by multiplying the number of MC events with the
        factor one gets the corresponding cross section.
        """
        if not hasattr(self, "nAllEvents"):
            raise Exception("Number of all events is not set for dataset %s! The counter directory was not given, and setNallEvents() was not called." % self.name)
        if self.nAllEvents == 0:
            raise Exception("Number of all events is 0 for dataset %s" % self.name)

        return self.getCrossSection() / self.nAllEvents

    def getDatasetRootHisto(self, name):
        """Get the DatasetRootHisto object for a named histogram.

        Parameters:
        name   Path of the histogram in the ROOT file

        If the prefix is set (setPrefix() method), it is prepended to
        the name before TFile.Get() call.
        """

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

    def getDirectoryContent(self, directory, predicate=lambda x: True):
        """Get the directory content of a given directory in the ROOT file.

        Parameters:
        directory   Path of the directory in the ROOT file
        predicate   Append the directory name to the return list only if
                    predicate returns true for the name. Predicate
                    should be a function taking a string as an
                    argument and returning a boolean.

        Returns a list of names in the directory.

        If the prefix is set (setPrefix() method), it is prepended to
        the bame before TFile.Get() call.
        """

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
        

class DatasetMerged:
    """Dataset class for histogram access for a dataset merged from Dataset objects.

    The merged datasets are required to be either MC or data.

    """

    def __init__(self, name, datasets):
        """Constructor.

        Parameters:
        name      Name of the merged dataset
        datasets  List of Dataset objects to merge

        Calculates the total cross section (luminosity) for MC (data)
        datasets.
        """

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

    def setPrefix(self, prefix):
        """Set a prefix for the directory access.

        Parameters:
        prefix   Prefix for event counter and histogram directories.

        See Dataset.setPrefix() for more documentation.
        """
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

    def deepCopy(self):
        """Make a deep copy of a DatasetMerged object.

        Nothing is shared between the returned copy and this object.
        """

        dm = DatasetMerged(self.name, [d.deepCopy() for d in self.datasets])
        dm.info.update(self.info)
        return dm

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def setCrossSection(self, value):
        """Set cross section of MC dataset (in pb)."""
        if self.isData():
            raise Exception("Should not set cross section for data dataset %s (has luminosity)" % self.name)
        raise Exception("Setting cross section for merged dataset is meaningless (it has no real effect, and hence is misleading")

    def getCrossSection(self):
        """Get cross section of MC dataset (in pb)."""
        if self.isData():
            raise Exception("Dataset %s is data, no cross section available" % self.name)
        return self.info["crossSection"]

    def setLuminosity(self, value):
        """Set the integrated luminosity of data dataset (in pb^-1)."""
        if self.isMC():
            raise Exception("Should not set luminosity for MC dataset %s (has crossSection)" % self.name)
        raise Exception("Setting luminosity for merged dataset is meaningless (it has no real effect, and hence is misleading")

    def getLuminosity(self):
        """Get the integrated luminosity of data dataset (in pb^-1)."""
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

    def getDatasetRootHisto(self, name):
        """Get the DatasetRootHistoMergedMC/DatasetRootHistoMergedData object for a named histogram.

        Parameters:
        name   Path of the histogram in the ROOT file
        """
        wrappers = [d.getDatasetRootHisto(name) for d in self.datasets]
        if self.isMC():
            return DatasetRootHistoMergedMC(wrappers, self)
        else:
            return DatasetRootHistoMergedData(wrappers, self)

    def getDirectoryContent(self, directory, predicate=lambda x: True):
        """Get the directory content of a given directory in the ROOT file.

        Parameters:
        directory   Path of the directory in the ROOT file
        predicate   Append the directory name to the return list only if
                    predicate returns true for the name. Predicate
                    should be a function taking a string as an
                    argument and returning a boolean.

        Returns a list of names in the directory. The contents of the
        directories of the merged datasets are required to be identical.
        """
        content = self.datasets[0].getDirectoryContent(directory, predicate)
        for d in self.datasets[1:]:
            if content != d.getDirectoryContent(directory, predicate):
                raise Exception("Error: merged datasets have different contents in directory '%s'" % directory)
        return content

class DatasetManager:
    """Collection of Dataset objects which are managed together.

    Holds both an ordered list of Dataset objects, and a name->object
    map for convenient access by dataset name.
    """

    def __init__(self, base=""):
        self.datasets = []
        self.datasetMap = {}
        self.basedir = base

    def _populateMap(self):
        """Populate the datasetMap member from the datasets list.

        Intended only for internal use.
        """
        self.datasetMap = {}
        for d in self.datasets:
            self.datasetMap[d.getName()] = d

    def _setBaseDirectory(self, base):
        self.basedir = base

    def append(self, dataset):
        """Append a Dataset object to the set.

        Parameters:
        dataset    Dataset object

        The new Dataset must have a different name than the already existing ones.
        """

        if dataset.getName() in self.datasetMap:
            raise Exception("Dataset '%s' already exists in this DatasetManager" % dataset.getName())

        self.datasets.append(dataset)
        self.datasetMap[dataset.getName()] = dataset

    def extend(self, datasetmgr):
        """Extend the set of Datasets from another DatasetManager object.

        Parameters:
        datasetmgr   DatasetManager object

        Note that the Dataset objects of datasetmgr are appended to
        self by reference, i.e. the Dataset objects will be shared
        between them.
        """
        for d in datasetmgr.datasets:
            self.append(d)

    def shallowCopy(self):
        """Make a shallow copy of the DatasetManager object.

        The Dataset objects are shared between the DatasetManagers.
        """

        copy = DatasetManager()
        copy.extend(self)
        return copy

    def deepCopy(self):
        """Make a deep copy of the DatasetManager object.

        Nothing is shared between the DatasetManagers.
        """
        copy = DatasetManager()
        for d in self.datasets:
            copy.append(d.deepCopy())
        return copy

    def hasDataset(self, name):
        return name in self.datasetMap

    def getDataset(self, name):
        return self.datasetMap[name]

    def getDatasetRootHistos(self, histoName):
        """Get a list of DatasetRootHisto objects for a given name.

        Parameters:
        histoName   Path to the histogram in each ROOT file.
        """
        return [d.getDatasetRootHisto(histoName) for d in self.datasets]

    def getAllDatasets(self):
        """Get a list of all Dataset objects."""
        return self.datasets

    def getMCDatasets(self):
        """Get a list of MC Dataset objects."""
        ret = []
        for d in self.datasets:
            if d.isMC():
                ret.append(d)
        return ret

    def getDataDatasets(self):
        """Get a list of data Dataset objects."""
        ret = []
        for d in self.datasets:
            if d.isData():
                ret.append(d)
        return ret

    def getAllDatasetNames(self):
        """Get a list of names of all Dataset objects."""
        return [x.getName() for x in self.getAllDatasets()]

    def getMCDatasetNames(self):
        """Get a list of names of MC Dataset objects."""
        return [x.getName() for x in self.getMCDatasets()]

    def getDataDatasetNames(self):
        """Get a list of names of data Dataset objects."""
        return [x.getName() for x in self.getDataDatasets()]

    def selectAndReorder(self, nameList):
        """Select and reorder Datasets.

        Parameters:
        nameList   Ordered list of Dataset names to select

        This method can be used to either select a set of Datasets,
        reorder them, or both.
        """
        selected = []
        for name in nameList:
            try:
                selected.append(self.datasetMap[name])
            except KeyError:
                print >> sys.stderr, "WARNING: Dataset selectAndReorder: dataset %s doesn't exist" % name

        self.datasets = selected
        self._populateMap()

    def remove(self, nameList):
        """Remove Datasets.

        Parameters:
        nameList    List of Dataset names ro remove
        """
        if isinstance(nameList, basestring):
            nameList = [nameList]

        selected = []
        for d in self.datasets:
            if not d.getName() in nameList:
                selected.append(d)
        self.datasets = selected
        self._populateMap()

    def rename(self, oldName, newName):
        """Rename a Dataset.

        Parameters:
        oldName   The current name of a Dataset
        newName   The new name of a Dataset
        """
        if oldName == newName:
            return

        if newName in self.datasetMap:
            raise Exception("Trying to rename datasets '%s' to '%s', but a dataset with the new name already exists!" % (oldName, newName))
        self.datasetMap[oldName].setName(newName)
        self._populateMap()

    def renameMany(self, nameMap, silent=False):
        """Rename many Datasets.

        Parameters:
        nameMap   Dictionary containing oldName->newName mapping
        """
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

    def mergeData(self):
        """Merge all data Datasets to one with a name 'Data'."""
        self.merge("Data", self.getDataDatasetNames())

    def mergeMC(self):
        """Merge all MC Datasets to one with a name 'MC'."""
        self.merge("MC", self.getMCDatasetNames())

    def mergeMany(self, mapping):
        """Merge datasets according to the mapping."""
        toMerge = {}
        for d in self.datasets:
            if d.getName() in mapping:
                newName = mapping[d.getName()]
                if newName in toMerge:
                    toMerge[newName].append(d.getName())
                else:
                    toMerge[newName] = [d.getName()]

        for newName, nameList in toMerge.iteritems():
            self.merge(newName, nameList)

    def merge(self, newName, nameList, keepSources=False):
        """Merge Datasets.

        Parameters:
        newName    Name of the merged Dataset
        nameList   List of Dataset names to merge
        """
        
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

    def loadLuminosities(self, fname="lumi.json"):
        """Load integrated luminosities from a JSON file.

        Arguments:
        fname   Path to the file (default: 'lumi.json'). If the
                directory part of the path is empty, the file is
                looked from the base directory (which defaults to
                current directory)

        The JSON file should be formatted like this:

        '{
           "dataset_name": value_in_pb,
           "Mu_135821-144114": 2.863224758
         }'
        """
        if len(os.path.dirname(fname)) == 0:
            fname = os.path.join(self.basedir, fname)

        if not os.path.exists(fname):
            print >> sys.stderr, "WARNING: luminosity json file '%s' doesn't exist!" % fname

        data = json.load(open(fname))
        for name, value in data.iteritems():
            if self.hasDataset(name):
                self.getDataset(name).setLuminosity(value)

    def printInfo(self):
        """Print dataset information."""
        col1hdr = "Dataset"
        col2hdr = "Cross section (pb)"
        col3hdr = "Norm. factor"
        col4hdr = "Int. lumi (pb^-1)" 

        maxlen = max([len(x.getName()) for x in self.datasets]+[len(col1hdr)])
        c1fmt = "%%-%ds" % (maxlen+2)
        c2fmt = "%%%d.4g" % (len(col2hdr)+2)
        c3fmt = "%%%d.4g" % (len(col3hdr)+2)
        c4fmt = "%%%d.4g" % (len(col4hdr)+2)

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

