import os
import glob
from optparse import OptionParser

import ROOT

import multicrab
import counter

def addCmsPreliminaryText(x=0.62, y=0.96):
    l = ROOT.TLatex()
    l.SetNDC()
    l.DrawLatex(x, y, "CMS Preliminary")

def addEnergyText(x=0.3, y=0.96, s="7 TeV"):
    l = ROOT.TLatex()
    l.SetNDC()
    l.DrawLatex(x, y, "#sqrt{s} = "+s)

def addLuminosityText(x, y, lumi, unit="pb^{1}"):
    l = ROOT.TLatex()
    l.SetNDC()
    l.DrawLatex(x, y, "#intL=%.2f %s" % (lumi, unit))

def createLegend(x1, y1, x2, y2):
    legend = ROOT.TLegend(x1, y1, x2, y2)
    legend.SetFillColor(ROOT.kWhite)
    legend.SetBorderSize(1)
    #legend.SetMargin(0.1)
    return legend

class DatasetSet:
    def __init__(self):
        self.datasets = []
        self.datasetMap = {}

    def append(self, dataset):
        self.datasets.append(dataset)
        self.datasetMap[dataset.getName()] = dataset

    def extend(self, datasetset):
        for d in datasetset.datasets:
            self.append(d)

    def getDataset(self, name):
        return self[name]

    def hasDataset(self, name):
        return name in self.datasetMap

    def __getitem__(self, name):
        return self.datasetMap[name]

    def remove(self, nameList):
        selected = []
        for d in self.datasets:
            if not d.getName() in nameList:
                selected.append(d)
        self.datasets = selected
        self.populateMap()
            
    def populateMap(self):
        self.datasetMap = {}
        for d in self.datasets:
            self.datasetMap[d.getName()] = d

    def getHistoSet(self, histoName):
	histos = []
	for d in self.datasets:
            h = d.getTFile().Get(histoName)
            name = h.GetName()+"_"+d.getName()
            h.SetName(name.translate(None, "-+.:;"))
            histos.append(h)
        return HistoSet(self.datasets, histos)


class HistoSetData:
    def __init__(self, dataset, histo):
        self.dataset = dataset
        self.histo = histo
        self.legendLabel = dataset.getName()
        self.legendStyle = "l"
        self.drawStyle = "HIST"

    def getName(self):
        return self.dataset.getName()

    def setName(self, name):
        self.dataset.setName(name)

    def setLegendLabel(self, label):
        self.legendLabel = label

    def setLegendStyle(self, style):
        self.legendStyle = style

    def addToLegend(self, legend):
        legend.AddEntry(self.histo, self.legendLabel, self.legendStyle)

    def applyStyle(self, styleList):
        style = styleList.pop(0)
        style.apply(self.histo)

    def applyFunction(self, func):
        h = func(self.histo)
        if h != None:
            self.histo = h

    def getXmin(self):
        return self.histo.GetXaxis().GetBinLowEdge(self.histo.GetXaxis().GetFirst())

    def getXmax(self):
        return self.histo.GetXaxis().GetBinUpEdge(self.histo.GetXaxis().GetLast())

class HistoSetDataStacked:
    def __init__(self, data, name):
        self.data = data
        self.drawStyle = "HIST"
        self.name = name
        
        self.histo = ROOT.THStack(name+"stackHist", name+"stackHist")
        histos = [d.histo for d in self.data]
        histos.reverse()
        for h in histos:
            self.histo.Add(h)

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def setLegendLabel(self, label):
        for d in self.data:
            d.setLegendLabel(label)

    def setLegendStyle(self, style):
        for d in self.data:
            d.setLegendStyle(style)

    def addToLegend(self, legend):
        for d in self.data:
            d.addToLegend(legend)

    def applyStyle(self, styleList):
        for d in self.data:
            d.applyStyle(styleList)

    def getXmin(self):
        return min([d.getXmin() for d in self.data])

    def getXmax(self):
        return max([d.getXmax() for d in self.data])

class HistoSet:
    def __init__(self, datasets, histos):
        if len(datasets) != len(histos):
            raise Exception("Length of datasets and histos differ! (%d != %d)" % (len(datasets), len(histos)))

        self.data = []
        self.datasetMap = {}
        for i, d in enumerate(datasets):
            self.data.append(HistoSetData(d, histos[i]))
        self.populateMap()
                            
        self.normalization = "none"
        self.luminosity = None

    def populateMap(self):
        self.datasetMap = {}
        for d in self.data:
            self.datasetMap[d.getName()] = d

    def reorderAndSelectDatasets(self, nameList):
        selected = []
        for name in nameList:
            selected.append(self.datasetMap[name])
        self.data = selected
        self.populateMap()

    def removeDatasets(self, nameList):
        selected = []
        for d in self.data:
            if not d.getName() in nameList:
                selected.append(d)
        self.data = selected
        self.populateMap()

    def getDataset(self, name):
        return self.datasetMap[name].dataset

    def getDatasetList(self):
        return [d.dataset for d in self.data]

    def getDatasetNames(self):
        return [d.getName() for d in self.data]

    def getMCDatasetNames(self):
        names = []
        for d in self.data:
            if d.dataset.isMC():
                names.append(d.getName())
        return names

    def getDataDatasetNames(self):
        names = []
        for d in self.data:
            if d.dataset.isData():
                names.append(d.getName())
        return names

    def renameDataset(self, oldName, newName):
        if oldName == newName:
            return

        if newName in self.datasetMap:
            raise Exception("Trying to rename datasets '%s' to '%s', but a dataset with the new name already exists!" % (oldName, newName))
        self.datasetMap[oldName].setName(newName)
        self.populateMap()

    def renameDatasets(self, nameMap):
        for oldName, newName in nameMap.iteritems():
            if oldName == newName:
                continue

            if newName in datasetMap:
                raise Exception("Trying to rename datasets '%s' to '%s', but a dataset with the new name already exists!" % (oldName, newName))
            self.datasetMap[oldName].setName(newName)
        self.populateMap()

    def forEachHisto(self, func):
        for d in self.data:
            d.applyFunction(func)

    def getHisto(self, name):
        return self.datasetMap[name].histo

    def getHistoList(self):
        return [d.dataset for d in self.data]

    def setHistoLegendLabel(self, name, label):
        if not name in self.datasetMap:
            print "WARNING: Tried to set legend label for dataset '%s', which doesn't exist." % name
            return

        self.datasetMap[name].setLegendLabel(label)

    def setHistoLegendLabels(self, nameMap):
        for name, label in nameMap.iteritems():
            self.setHistoLegendLabel(name, label)

    def setHistoLegendStyle(self, name, style):
        if not name in self.datasetMap:
            print "WARNING: Tried to set legend style for dataset '%s', which doesn't exist." % name
            return

        self.datasetMap[name].setLegendStyle(style)

    def setHistoLegendStyleAll(self, style):
        for d in self.data:
            d.setLegendStyle(style)

    def setHistoDrawStyle(self, name, style):
        self.datasetMap[name].drawStyle = style

    def setHistoDrawStyleAll(self, style):
        for d in self.data:
            d.drawStyle = style

    def getLuminosity(self):
        if self.luminosity == None:
            raise Exception("No normalization by or to luminosity!")
        return self.luminosity

    def addLuminosityText(self, x=0.65, y=0.85):
        addLuminosityText(x, y, self.getLuminosity(), "pb^{-1}")

    def applyStyle(self, name, style):
        if not name in self.datasetMap:
            print "WARNING: Tried to set histogram style for dataset '%s', which doesn't exist." % name
            return

        self.datasetMap[name].applyStyle([style])

    def applyStyles(self, styleList):
        if len(styleList) < len(self.data):
            raise Exception("len(styleList) = %d < len(self.histos) = %d" % (len(styleList), len(self.histos)))

        # The list is modified by the applyStyle() methods
        lst = styleList[:]
        for d in self.data:
            d.applyStyle(lst)

    def applyStylesMC(self, styleList):
        mcDatasets = self.getMCDatasetNames()
        if len(styleList) < len(mcDatasets):
            raise Exception("len(styleList) = %d < len(mcDatasets) = %d" % (len(styleList), len(mcDatasets)))

        # The list is modified by the applyStyle() methods
        lst = styleList[:]
        for name in mcDatasets:
            self.datasetMap[name].applyStyle(lst)

    def createCanvasFrame(self, name, ymin=None, ymax=None, xmin=None, xmax=None):
        c = ROOT.TCanvas(name)
        if ymin == None:
            ymin = min([d.histo.GetMinimum() for d in self.data])
        if ymax == None:
            ymax = max([d.histo.GetMaximum() for d in self.data])
            ymax = 1.1*ymax

        if xmin == None:
            xmin = min([d.getXmin() for d in self.data])
        if xmax == None:
            xmax = min([d.getXmax() for d in self.data])

        frame = c.DrawFrame(xmin, ymin, xmax, ymax)
        frame.GetXaxis().SetTitle(self.data[0].histo.GetXaxis().GetTitle())
        frame.GetYaxis().SetTitle(self.data[0].histo.GetYaxis().GetTitle())

        return (c, frame)

    def addToLegend(self, legend):
        for d in self.data:
            d.addToLegend(legend)

    def draw(self, inReverseOrder=True):
        histos = [(d.histo, d.drawStyle, d.getName()) for d in self.data]
        if inReverseOrder:
            histos.reverse()

        for h, style, dname in histos:
            h.Draw(style+" same")

    def mergeDataDatasets(self):
        self.mergeDatasets("Data", self.getDataDatasetNames())

    def stackMCDatasets(self):
        self.stackDatasets("MC", self.getMCDatasetNames())

    def mergeStackInternalHelper(self, newName, datasetNameList, task):
        indices = []
        dataCount = 0
        mcCount = 0
        newData = []
        for i, d in enumerate(self.data):
            if d.getName() in datasetNameList:
                indices.append(i)
                if d.dataset.isData():
                    dataCount += 1
                elif d.dataset.isMC():
                    mcCount += 1
                else:
                    raise Exception("Internal error!")
            else:
                newData.append(d)

        if dataCount > 0 and mcCount > 0:
            raise Exception("Can not %s data and MC datasets!" % task)

        if len(indices) == 0:
            print "Dataset %s: no datasets '"%task + ", ".join(datasetNameList) + "' found, not doing anything"
            return None
        if len(indices) == 1:
            print "Dataset %s: one dataset '"%task + self.data[indices[0]].getName() + "' found from list '" + ", ".join(datasetNameList)+", renaming it to '%s'" % newName
            self.renameDataset(self.data[indices[0]].getName(), newName)
            return None
        if len(indices) != len(datasetNameList):
            dlist = datasetNameList[:]
            for i in indices:
                ind = dlist.index(self.data[i].getName())
                del dlist[ind]
            print "WARNING: Tried to %s '"%task + ", ".join(dlist) +"' which don't exist"

        isMC = mcCount > 0    
        return (indices, newData, isMC)

    def stackDatasets(self, newName, datasetNameList):
        tpl = self.mergeStackInternalHelper(newName, datasetNameList, "stack")
        if tpl == None:
            return
        (indices, newData, isMC) = tpl

        h = HistoSetDataStacked([self.data[i] for i in indices], newName)
        newData.insert(indices[0], h)
        self.data = newData
        self.populateMap()

    def mergeDatasets(self, newName, datasetNameList):
        tpl = self.mergeStackInternalHelper(newName, datasetNameList, "merge")
        if tpl == None:
            return
        (indices, newData, isMC) = tpl

        dataset = None
        if isMC:
            if not self.normalization in ["byCrossSection", "byLuminosity", "toLuminosity"]:
                raise Exception("MC datasets must be normalized by cross section or luminosity before merging!")

            # If we can sum the histograms together, we can sum the
            # cross sections too. It is purely in the user's
            # responsibility to decide if this is correct or not
            crossSum = 0.0
            for i in indices:
                crossSum += self.data[i].dataset.getCrossSection()
            dataset = counter.Dataset(newName, {"crossSection": crossSum}, None)
        else:
            if self.normalization == "one":
                raise Exception("Can not merge data datasets after normalizeToOne!")

            # Calculate the total integrated luminosity
            lumiSum = 0.0
            for i in indices:
                lumiSum += self.data[i].dataset.getLuminosity()
            dataset = counter.Dataset(newName, {"luminosity": lumiSum}, None)

        # Sum the histograms in question, contents assumed to be
        # directly summable (same code for both methods)
        histoSum = self.data[indices[0]].histo.Clone()
        for i in indices[1:]:
            histoSum.Add(self.data[i].histo)
        newData.insert(indices[0], HistoSetData(dataset, histoSum))

        self.data = newData
        self.populateMap()

    def normalizeToOne(self):
        if self.normalization != "none":
            raise Exception("Histograms already normalized")

        for d in self.data:
            h = d.histo
            h.Sumw2() # errors are also scaled after this call 
            h.Scale(1.0/h.Integral())
        self.normalization = "one"

    def normalizeMCByCrossSection(self):
        if self.normalization != "none":
            raise Exception("Histograms already normalized")

        for d in self.data:
            if d.dataset.isData():
                continue
            h = d.histo
            h.Sumw2() # errors are also scaled after this call
            h.Scale(d.dataset.getNormFactor())
            h.GetYaxis().SetTitle("Cross section (pb)")
                
        self.normalization = "byCrossSection"

    def normalizeMCByLuminosity(self):
        if not self.normalization in ["none", "byCrossSection"]:
            raise Exception("Histograms already normalized")

        self.luminosity = None
        for d in self.data:
            if d.dataset.isData():
                if self.luminosity != None:
                    raise Exception("Only one data dataset may exist for normalizing byLuminosity; you can remove other data datasets, merge them or use normalizeMCToLuminosity(lumi)")
                self.luminosity = d.dataset.getLuminosity()

        if self.luminosity == None:
            raise Exception("No collision data datasets, can not normalize by luminosity (you might want to consider normalizeMCToLuminosity(lumi) with explicit integrated luminosity")

        self.normalizeMCToLuminosity(self.luminosity)
        self.normalization = "byLuminosity"

    def normalizeMCToLuminosity(self, lumi):
        if not self.normalization in ["none", "byCrossSection"]:
            raise Exception("Histograms already normalized")

        if self.normalization == "none":
            self.normalizeMCByCrossSection()

        for d in self.data:
            if d.dataset.isData():
                continue
            h = d.histo
            # h.Sumw2() call not needed because the histo is already
            # normalized by cross section (i.e. it has already been
            # called)
            h.Scale(lumi)
        
        self.luminosity = lumi
        self.normalization = "toLuminosity"


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
        datasets.append(counter.readDataset(f, counterdir, name, {}))
    return datasets

