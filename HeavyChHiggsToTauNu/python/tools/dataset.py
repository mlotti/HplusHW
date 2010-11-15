import glob, os, sys
from optparse import OptionParser

import ROOT

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab

class Count:
    def __init__(self, value, error):
        self._value = value
        self._error = error

    def value(self):
        return self._value

    def error(self):
        return self._error

    def __str__(self):
        return "%f"%self._value

def histoToCounter(histo):
    ret = []

    for bin in xrange(1, histo.GetNbinsX()+1):
        ret.append( (histo.GetXaxis().GetBinLabel(bin),
                     Count(float(histo.GetBinContent(bin)),
                           float(histo.GetBinError(bin)))) )

    return ret

def histoToDict(histo):
    ret = {}

    for bin in xrange(1, histo.GetNbinsX()+1):
        ret[histo.GetXaxis().GetBinLabel(bin)] = histo.GetBinContent(bin)

    return ret

def rescaleInfo(d):
    factor = 1/d["control"]

    ret = {}
    for k, v in d.iteritems():
        ret[k] = v*factor

    return ret


def addOptions(parser):
    parser.add_option("-i", dest="input", type="string", default="histograms-*.root",
                      help="Pattern for input root files (note: remember to escape * and ? !) (default: 'histograms-*.root')")
    parser.add_option("-f", dest="files", type="string", action="append", default=[],
                      help="Give input ROOT files explicitly, if these are given, multicrab.cfg is not read and -d/-i parameters are ignored")


def getDatasetsFromMulticrabCfg(opts=None, counters="signalAnalysisCounters"):
    return getDatasetsFromCrabDirs(multicrab.getTaskDirectories(opts), opts, counters)

def getDatasetsFromCrabDirs(taskdirs, opts=None, counters="signalAnalysisCounters"):   
    if opts == None:
        parser = OptionParser(usage="Usage: %prog [options]")
        multicrab.addOptions(parser)
        addOptions(parser)
        (opts, args) = parser.parse_args()
        if hasattr(opts, "counterdir"):
            counters = opts.counterdir

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

        dlist.append( (d, files[0]) )

    if noFiles:
        print >> sys.stderr, ""
        print >> sys.stderr, "  There were datasets without files. Have you merged the files with hplusMergeHistograms.py?"
        print >> sys.stderr, ""
        if len(dlist) == 0:
            raise Exception("No datasets. Have you merged the files with hplusMergeHistograms.py?")

    if len(dlist) == 0:
        raise Exception("No datasets")

    return getDatasetsFromRootFiles(dlist, counters)

def getDatasetsFromRootFiles(dlist, counters="signalAnalysisCounters"):
    datasets = DatasetSet()
    for name, f in dlist:
        datasets.append(Dataset(name, f, counters))
    return datasets

#def readDataset(fname, counters, datasetname, crossSections):
#    dataset = Dataset(datasetname, fname, counters)
#    if datasetname in crossSections:
#        dataset.setCrossSection(crossSections[datasetname])
#    return dataset


def normalizeToOne(h):
    return normalizeToFactor(1.0/h.Integral())
    return h

def normalizeToFactor(h, f):
    backup = ROOT.gErrorIgnoreLevel
    ROOT.gErrorIgnoreLevel = ROOT.kError
    h.Sumw2() # errors are also scaled after this call 
    ROOT.gErrorIgnoreLevel = backup
    h.Scale(f)
    return h


def mergeStackHelper(datasetList, nameList, task):
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

class HistoWrapper:
    def __init__(self, histo, dataset):
        self.histo = histo
        self.dataset = dataset
        self.normalization = "none"

    def getDataset(self):
        return self.dataset

    def isData(self):
        return self.dataset.isData()

    def isMC(self):
        return self.dataset.isMC()

    def getHistogram(self):
        # Always return a clone of the original
        h = self.histo.Clone()
        h.SetName(h.GetName()+"_cloned")
        if self.normalization == "none":
            return h
        elif self.normalization == "toOne":
            return normalizeToOne(h)

        # We have to normalize to cross section in any case
        h = normalizeToFactor(h, self.dataset.getNormFactor())
        if self.normalization == "byCrossSection":
            return h
        elif self.normalization == "toLuminosity":
            return normalizeToFactor(h, self.luminosity)
        else:
            raise Exception("Internal error")

    def normalizeToOne(self):
        self.normalization = "toOne"

    def normalizeByCrossSection(self):
        if self.dataset.isData():
            raise Exception("Can't normalize data histogram by cross section")
        self.normalization = "byCrossSection"

    def normalizeToLuminosity(self, lumi):
        if self.dataset.isData():
            raise Exception("Can't normalize data histogram to luminosity")

        self.normalization = "toLuminosity"
        self.luminosity = lumi


class HistoWrapperMergedData:
    def __init__(self, datasetHistos, mergedDataset):
        self.datasetHistos = datasetHistos
        self.dataset = mergedDataset
        self.normalization = "none"
        for h in self.datasetHistos:
            if h.isMC():
                raise Exception("Internal error")
            if h.normalization != "none":
                raise Exception("Internal error")

    def getDataset(self):
        return self.dataset

    def normalizeToOne(self):
        self.normalization = "toOne"

    def getSumHistogram(self):
        hsum = self.datasetHistos[0].getHistogram() # we get a clone
        for h in self.datasetHistos[1:]:
            hsum.Add(h.getHistogram())
        return hsum

    def getHistogram(self):
        hsum = self.getSumHistogram()
        if self.normalization == "toOne":
            return normalizeToOne(hsum)
        else:
            return hsum

class HistoWrapperMergedMC:
    def __init__(self, datasetHistos, mergedDataset):
        self.datasetHistos = datasetHistos
        self.dataset = mergedDataset
        self.normalization = "none"
        for h in self.datasetHistos:
            if h.isData():
                raise Exception("Internal error")
            if h.normalization != "none":
                raise Exception("Internal error")

    def getDataset(self):
        return self.dataset

    def normalizeToOne(self):
        self.normalization = "toOne"
        for h in self.datasetHistos:
            h.normalizeByCrossSection()
	raise Exception("Not implemented yet!")

    def normalizeByCrossSection(self):
        self.normalization = "byCrossSection"
        for h in self.datasetHistos:
            h.normalizeByCrossSection()

    def normalizeToLuminosity(self, lumi):
        self.normalization = "toLuminosity"
        for h in self.datasetHistos:
            h.normalizeToLuminosity(lumi)

    def getHistogram(self):
        if self.normalization == "none":
            raise Exception("Merged MC histograms must be normalized to something!")

        hsum = self.datasetHistos[0].getHistogram() # we get a clone
        for h in self.datasetHistos[1:]:
            hsum.Add(h.getHistogram())

        if self.normalization == "toOne":
            return normalizeToOne(hsum)
        else:
            return hsum


class Dataset:
    def __init__(self, name, fname, counterDir):
        self.name = name
        self.file = ROOT.TFile.Open(fname)
        if self.file == None:
            raise Exception("Unable to open ROOT file '%s'"%fname)
        if self.file.Get("configInfo") == None:
            raise Exception("Unable to find directory 'configInfo' from ROOT file '%s'"%fname)
        self.info = rescaleInfo(histoToDict(self.file.Get("configInfo").Get("configinfo")))

        if self.file.Get(counterDir) == None:
            raise Exception("Unable to find directory '%s' from ROOT file '%s'" % (counterDir, fname))
        ctr = histoToCounter(self.file.Get(counterDir).Get("counter"))
        self.nAllEvents = ctr[0][1].value() # first counter, second element of the tuple
        self.counterDir = counterDir

    def deepCopy(self):
        d = Dataset(self.name, self.file.GetName(), self.counterDir)
        d.info.update(self.info)
        return d

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def setCrossSection(self, value):
        if self.isData():
            raise Exception("Should not set cross section for data dataset %s (has luminosity)" % self.name)
        self.info["crossSection"] = value

    def getCrossSection(self):
        if self.isData():
            raise Exception("Dataset %s is data, no cross section available" % self.name)
        return self.info["crossSection"]

    def setLuminosity(self, value):
        if self.isMC():
            raise Exception("Should not set luminosity for MC dataset %s (has crossSection)" % self.name)
        self.info["luminosity"] = value

    def getLuminosity(self):
        if self.isMC():
            raise Exception("Dataset %s is MC, no luminosity available" % self.name)
        return self.info["luminosity"]

    def isData(self):
        return "luminosity" in self.info

    def isMC(self):
        return "crossSection" in self.info

    def getCounterDirectory(self):
        return self.counterDir

    def getNormFactor(self):
        return self.getCrossSection() / self.nAllEvents

    def getHistoWrapper(self, name):
        h = self.file.Get(name)
        if h == None:
            raise Exception("Unable to find histogram '%s'" % name)

        name = h.GetName()+"_"+self.name
        h.SetName(name.translate(None, "-+.:;"))
        return HistoWrapper(h, self)

    def getDirectoryContent(self, directory, predicate=lambda x: True):
        d = self.file.Get(directory)
        dirlist = d.GetListOfKeys()
        diriter = dirlist.MakeIterator()
        key = diriter.Next()

        ret = []
        while key:
            if predicate(key.ReadObj()):
                ret.append(key.GetName())
            key = diriter.Next()
        return ret


class DatasetMerged:
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

    def deepCopy(self):
        dm = DatasetMerged(self.name, [d.deepCopy() for d in self.datasets])
        dm.info.update(self.info)
        return dm

    def getName(self):
        return self.name

    def setCrossSection(self, value):
        if self.isData():
            raise Exception("Should not set cross section for data dataset %s (has luminosity)" % self.name)
        self.info["crossSection"] = value

    def getCrossSection(self):
        if self.isData():
            raise Exception("Dataset %s is data, no cross section available" % self.name)
        return self.info["crossSection"]

    def setLuminosity(self, value):
        if self.isMC():
            raise Exception("Should not set luminosity for MC dataset %s (has crossSection)" % self.name)
        self.info["luminosity"] = value

    def getLuminosity(self):
        if self.isMC():
            raise Exception("Dataset %s is MC, no luminosity available" % self.name)
        return self.info["luminosity"]

    def isData(self):
        return "luminosity" in self.info

    def isMC(self):
        return "crossSection" in self.info

    def getCounterDirectory(self):
        countDir = self.datasets[0].getCounterDirectory()
        for d in self.datasets[1:]:
            if countDir != d.getCounterDirectory():
                raise Exception("Error: merged datasets have different counter directories")
        return countDir

    def getNormFactor(self):
        return None

    def getHistoWrapper(self, name):
        wrappers = [d.getHistoWrapper(name) for d in self.datasets]
        if self.isMC():
            return HistoWrapperMergedMC(wrappers, self)
        else:
            return HistoWrapperMergedData(wrappers, self)

    def getDirectoryContent(self, directory, predicate=lambda x: True):
        content = self.datasets[0].getDirectoryContent(directory, predicate)
        for d in self.datasets[1:]:
            if content != d.getDirectoryContent(directory, predicate):
                raise Exception("Error: merged datasets have different contents in directory '%s'" % directory)
        return content

class DatasetSet:
    def __init__(self):
        self.datasets = []
        self.datasetMap = {}

    def populateMap(self):
        self.datasetMap = {}
        for d in self.datasets:
            self.datasetMap[d.getName()] = d

    def append(self, dataset):
        if dataset.getName() in self.datasetMap:
            raise Exception("Dataset '%s' already exists in this DatasetSet" % dataset.getName())

        self.datasets.append(dataset)
        self.datasetMap[dataset.getName()] = dataset

    def extend(self, datasetset):
        for d in datasetset.datasets:
            self.append(d)

    def shallowCopy(self):
        copy = DatasetSet()
        copy.extend(self)
        return copy

    def deepCopy(self):
        copy = DatasetSet()
        for d in self.datasets:
            copy.append(d.deepCopy())
        return copy

    def hasDataset(self, name):
        return name in self.datasetMap

    def getDataset(self, name):
        return self.datasetMap[name]

    def getHistoWrappers(self, histoName):
        return [d.getHistoWrapper(histoName) for d in self.datasets]

    def getAllDatasets(self):
        return self.datasets

    def getMCDatasets(self):
        ret = []
        for d in self.datasets:
            if d.isMC():
                ret.append(d)
        return ret

    def getDataDatasets(self):
        ret = []
        for d in self.datasets:
            if d.isData():
                ret.append(d)
        return ret

    def getMCDatasetNames(self):
        return [x.getName() for x in self.getMCDatasets()]

    def getDataDatasetNames(self):
        return [x.getName() for x in self.getDataDatasets()]

    def selectAndReorder(self, nameList):
        selected = []
        for name in nameList:
            try:
                selected.append(self.datasetMap[name])
            except KeyError:
                print >> sys.stderr, "WARNING: Dataset selectAndReorder: dataset %s doesn't exist" % name

        self.datasets = selected
        self.populateMap()

    def remove(self, nameList):
        selected = []
        for d in self.datasets:
            if not d.getName() in nameList:
                selected.append(d)
        self.datasets = selected
        self.populateMap()

    def rename(self, oldName, newName):
        if oldName == newName:
            return

        if newName in self.datasetMap:
            raise Exception("Trying to rename datasets '%s' to '%s', but a dataset with the new name already exists!" % (oldName, newName))
        self.datasetMap[oldName].setName(newName)
        self.populateMap()

    def renameMany(self, nameMap):
        for oldName, newName in nameMap.iteritems():
            if oldName == newName:
                continue

            if newName in datasetMap:
                raise Exception("Trying to rename datasets '%s' to '%s', but a dataset with the new name already exists!" % (oldName, newName))
            self.datasetMap[oldName].setName(newName)
        self.populateMap()

    def mergeData(self):
        self.merge("Data", [x.getName() for x in self.getDataDatasets()])

    def merge(self, newName, nameList):
        (selected, notSelected, firstIndex) = mergeStackHelper(self.datasets, nameList, "merge")
        if len(selected) == 0:
            print >> sys.stderr, "Dataset merge: no datasets '" +", ".join(nameList) + "' found, not doing anything"
            return
        elif len(selected) == 1:
            print >> sys.stderr, "Dataset merge: one dataset '" + selected[0].getName() + "' found from list '" + ", ".join(nameList)+", renaming it to '%s'" % newName
            self.rename(selected[0].getName(), newName)
            return 

        notSelected.insert(firstIndex, DatasetMerged(newName, selected))
        self.datasets = notSelected
        self.populateMap()

    def printInfo(self):
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

