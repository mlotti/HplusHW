import ROOT

def histoToCounter(histo):
    ret = []

    for bin in xrange(1, histo.GetNbinsX()+1):
        ret.append( (histo.GetXaxis().GetBinLabel(bin),
                     long(histo.GetBinContent(bin))) )

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


def getDatasetsFromMulticrabCfg(opts=None, counterdir="signalAnalysisCounters"):
    return getDatasetsFromCrabDirs(multicrab.getTaskDirectories(opts), opts, counterdir)

def getDatasetsFromCrabDirs(taskdirs, opts=None, counterdir="signalAnalysisCounters"):   
    if opts == None:
        parser = OptionParser(usage="Usage: %prog [options]")
        multicrab.addOptions(parser)
        addOptions(parser)
        (opts, args) = parser.parse_args()
        if hasattr(opts, "counterdir"):
            counterdir = opts.counterdir

    dlist = []
    for d in taskdirs:
        files = glob.glob(os.path.join(d, "res", opts.input))
        if len(files) > 1:
            raise Exception("Only one file should match the input (%d matched) for task %s" % (len(files), d))
            return 1
        elif len(files) == 0:
            print "No files matched to input for task %s, ignoring the dataset" % d
            continue

        dlist.append( (d, files[0]) )

    return getDatasetsFromRootFiles(dlist, counterdir)

def getDatasetsFromRootFiles(dlist, counterdir="signalAnalysisCounters"):
    datasets = DatasetSet()
    for name, f in dlist:
        datasets.append(Dataset(f, counterdir, name))
    return datasets

def readDataset(fname, counterDir, datasetname, crossSections):
    dataset = Dataset(datasetname, fname, counterDir)
    if datasetname in crossSections:
        dataset.setCrossSection(crossSections[datasetname])
    return dataset


def normalizeToOne(h):
    return normalizeToFactor(1.0/h.Integral())
    return h

def normalizeToFactor(h, f):
    h.Sumw2() # errors are also scaled after this call 
    h.Scale(f)
    return h



class DatasetHisto:
    def __init__(self, histo, dataset):
        self.histo = histo
        self.dataset = dataset
        self.normalization = "none"

    def getDataset(self):
        return self.dataset

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


class DatasetHistoMergedData:
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

    # def getHistogramStack(self):
    #     name = self.dataset.getName()+"_stacked"
    #     stack = ROOT.THStack(name, name)
    #     if self.dataset.isStacked():
    #         norm = 1
    #         if self.normalization == "toOne":
    #             hsum = self.getSumHistogram()
    #             for h in self.datasetHistos:
    #                 stack.Add(normalizeToFactor(h.getHistogram(), 1.0/hsum.Integral()))
    #         else:
    #             for h in self.datasetHistos:
    #                 stack.Add(h.getHistogram())
    #     else:
    #         stack.Add(self.getHistogram())
    #     return stack

class DatasetHistoMergedMC:
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
        for h in self.datasetHistos:
            h.normalizeByCrossSection

    def normalizeByCrossSection(self):
        self.normalization = "byCrossSection"
        for h in self.datasetHistos:
            h.normalizeByCrossSection

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

        if f.Get(counterDir) == None:
            raise Exception("Unable to find directory '%s' from ROOT file '%s'" % (counterDir, fname))
        ctr = histoToCounter(f.Get(counterDir).Get("counter"))
        self.nAllEvents = ctr[0][1] # first counter, second element of the tuple

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

    def getNormFactor(self):
        return self.getCrossSection() / self.nAllEvents

    def getHistoWrapper(self, name):
        h = self.file.Get(histoName)
        name = h.GetName()+"_"+self.name
        h.SetName(name.translate(None, "-+.:;"))
        return DatasetHisto(h, self)



class DatasetMerged:
    def __init__(self, name, datasets, stacked):
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

    def getName(self):
        return self.name

    # def isStacked(self):
    #     return self.stacked

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

    def getHistoWrapper(self, name):
        wrappers = [d.getHistoWrapper(name) for d in self.datasets]
        if self.isMC():
            return DatasetHistoMergedMC(wrappers, self)
        else:
            return DatasetHistoMergedData(wrappers, self)


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

    def getDataset(self, name):
        return self.datasetMap[name]

    def getHistoWrappers(self, histoName):
        return [d.getHistogram(histoName) for d in self.datasets]

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

    def selectAndReorder(self, nameList):
        selected = []
        for name in nameList:
            selected.append(self.datasetMap[name])
        self.data = selected
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

    def mergeStackHelper(self, newName, nameList, task):
        mergeData = []
        firstIndex = None
        dataCount = 0
        mcCount = 0
        newData = []
        for i, d in enumerate(self.datasets):
            if d.getName() in datasetNameList:
                mergeData.append(d)
                if firstIndex != None:
                    firstIndex = i
                if d.isData():
                    dataCount += 1
                elif d.isMC():
                    mcCount += 1
                else:
                    raise Exception("Internal error!")
            else:
                newData.append(d)

        if dataCount > 0 and mcCount > 0:
            raise Exception("Can not %s data and MC datasets!" % task)

        if len(mergeData) == 0:
            print "Dataset %s: no datasets '"%task +", ".join(datasetNameList) + "' found, not doing anything"
            return
        if len(mergeData) == 1:
            print "Dataset %s: one dataset '"%task + self.data[firstIndex].getName() + "' found from list '" + ", ".join(datasetNameList)+", renaming it to '%s'" % newName
            self.rename(self.data[indices[0]].getName(), newName)
            return
        if len(mergeData) != len(datasetNameList):
            dlist = datasetNameList[:]
            for d in mergeData:
                ind = dlist.index(d.getName())
                del dlist[ind]
            print "WARNING: Tried to %s '"%task + ", ".join(dlist) +"' which don't exist"

        if not task in ["stack", "merge"]:
            raise Exception("Internal error")

        newData.insert(firstIndex, DatasetMerged(mergeData, task=="stack"))
        self.datasets = newData
        self.populateMap()

    def merge(self, newName, nameList):
        mergeStackHelper(newName, nameList, "merge")

    # def stack(self, newName, nameList):
    #     mergeStackHelper(newName, nameList, "stack")
    
        
