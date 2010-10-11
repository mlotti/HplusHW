import ROOT

from dataset import *

class Counter:
    def __init__(self, counter):
        self.data = counter
        self.dataset = None

    def setDataset(self, dataset):
        self.dataset = dataset

    def getNames(self):
        return [x[0] for x in self.data]

    def getDataset(self):
        return self.dataset

    def getCounterValue(self, index):
        return self.data[index][1]

    def getCounterCrossSection(self, index):
        return self.dataset.getNormFactor() * self.getCounterValue(index)

class DatasetCounter:
    def __init__(self, dataset):
        self.dataset = dataset
        self.mainCounter = None
        self.subCounters = {}

    def setMainCounter(self, counter):
        counter.setDataset(self.dataset)
        self.mainCounter = counter

    def addSubCounter(self, name, counter):
        counter.setDataset(self.dataset)
        self.subCounters[name] = counter

    def getDataset(self):
        return self.dataset

    def getMainCounter(self):
        return self.mainCounter

    def getSubCounterNames(self):
        return self.subCounters.keys()

    def getSubCounter(self, name):
        return self.subCounters[name]

class Counters:
    def __init__(self):
        self.counters = []

    def addCounter(self, counter):
        self.counters.append(counter)

    def getDatasets(self):
        return [x.getDataset() for x in self.counters]

    def getMainCounters(self):
        return [x.getMainCounter() for x in self.counters]

    def getSubCounterNames(self):
        if len(self.counters) == 0:
            return []

        names = self.counters[0].getSubCounterNames()
        # Check that the subcounter names for all datasets are same
        for c in self.counters[1:]:
            cnames = c.getSubCounterNames()
            if len(names) != len(cnames):
                raise Exception("The lengths of subcounters are not equal! Dataset %s has %d, %s has %d" % (self.counters[0].getDataset().getName(), len(names), c.getDataset().getName(), len(cnames)))
            for ind, val in enumerate(names):
                if val != cnames[ind]:
                    raise Exception("The subcounter names are not equal!")

        return names

    def getSubCounters(self, name):
        return [x.getSubCounter(name) for x in self.counters]

def readCountersFileDir(fname, counterDir, datasetname, crossSections):
    dataset = readDataset(fname, counterDir, datasetname, crossSections)
    f = dataset.getTFile()

    dctr = DatasetCounter(dataset)

    directory = f.Get(counterDir)
    dirlist = directory.GetListOfKeys()
    diriter = dirlist.MakeIterator()
    key = diriter.Next()

    while key:
        # main counter
        if key.GetName() == "counter":
            dctr.setMainCounter(Counter(histoToCounter(key.ReadObj())))
        else:
            dctr.addSubCounter(key.GetName(), Counter(histoToCounter(key.ReadObj())))
        key = diriter.Next()

    return dctr
