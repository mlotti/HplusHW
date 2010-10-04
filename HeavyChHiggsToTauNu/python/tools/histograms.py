import os
import glob
from optparse import OptionParser

import ROOT

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter

class DatasetSet:
    def __init__(self):
        self.datasets = []
        self.datasetMap = {}

    def append(self, dataset):
        self.datasets.append(dataset)
        self.datasetMap[dataset.getName] = dataset

    def getDataset(self, name):
        return self[name]

    def __getitem__(self, name):
        return self.datasetMap[name]

    def getHistoSet(self, histoName):
        histos = [d.getTFile().Get(plot) for d in self.datasets]
        return HistoSet(self.datasets, histos)


class HistoSetData:
    def __init__(self, dataset, histo):
        self.dataset = dataset
        self.histo = histo
        self.legendLabel = dataset.getName()
        self.legendStyle = "l"
        self.drawStyle = "HIST"

class HistoSet:
    def __init__(self, datasets, histos):
        if len(datasets) != len(histos):
            raise Exception("Length of datasets and histos differ! (%d != %d)" % (len(datasets), len(histos)))

        self.data = []
        self.datasetMap = {}
        for i, d in enumerate(self.datasets):
            self.data.append(HistoSetData(d, histos[i]))
        self.populateMap()
                            
        self.normalization = "none"
        self.luminosity = None

    def populateMap(self):
        self.datasetMap = {}
        for d in self.data:
            self.datasetMap[d.dataset.getName()] = d

    def reorderAndSelectDatasets(self, nameList):
        selected = []
        for name in nameList:
            selected.append(self.datasetMap[name])
        self.data = selected
        self.populateMap()

    def removeDatasets(self, nameList):
        selected = []
        for d in self.data:
            if not d.dataset.getName() in nameList:
                selected.append(d)
        self.data = selected
        self.populateMap()

    def getDataset(self, name):
        return self.datasetMap[name].dataset

    def getDatasetList(self):
        return [d.dataset for d in self.data]

    def getHisto(self, name):
        return self.datasetMap[name].histo

    def getHistoList(self):
        return [d.dataset for d in self.data]

    def setHistoLegendLabel(self, name, label):
        self.datasetMap[name].legendLabel = label

    def setHistoLegendStyle(self, name, style):
        self.datasetMap[name].legendStyle = style

    def setHistoLegendStyleAll(self, style):
        for d in self.data:
            d.legendStyle = style

    def setHistoDrawStyle(self, name, style):
        self.datasetMap[name].drawStyle = style

    def setHistoDrawStyleAll(self, style):
        for d in self.data:
            d.legendStyle = style

    def getLuminosity(self):
        if self.luminosity == None:
            raise Exception("No normalization by or to luminosity!")
        return self.luminosity

    def applyStyles(self, styleList):
        if len(styleList) < len(self.data):
            raise Exception("len(styleList) = %d < len(self.histos) = %d" % (len(styleList), len(self.histos)))

        for i,d in enumerate(self.data):
            styleList[i].apply(d.histo)

    def createCanvasFrame(self, name):
        c = ROOT.TCanvas(name)
        ymin = min([d.histo.GetMinimum() for d in self.data])
        ymax = max([d.histo.GetMaximum() for d in self.data])
        ymax = 1.1*ymax

        xmin = min([d.histo.GetXaxis().GetBinLowEdge(h.GetXaxis().GetFirst()) for d in self.data])
        xmax = max([d.histo.GetXaxis().GetBinUpEdge(h.GetXaxis().GetLast()) for d in self.data])

        frame = c.DrawFrame(xmin, ymin, xmax, ymax)
        frame.GetXaxis().SetTitle(self.data[0].histo.GetXaxis().GetTitle())
        frame.GetYaxis().SetTitle(self.data[0].histo.GetYaxis().GetTitle())

        return (c, frame)

    def addToLegend(self, legend):
        for i,d in enumerate(self.data):
            legend.AddEntry(d.histo, d.legendLabel, d.legendStyle)

    def draw(self, inReverseOrder=True, stackDatasets=[], stackDrawStyle=""):
        histos = [(d.histo, d.drawStyle, d.dataset.getName()) for d in self.data]
        if inReverseOrder:
            histos.reverse()

        if len(stackDatasets) > 0:
            tmp = []
            firstIndex = None
            stack = ROOT.THStack()
            for t histos:
                if t[2] in stackDatasets:
                    stack.Add(t[0])
                    if firstIndex == None:
                        firstIndex = len(tmp)
                else:
                    tmp.append(t)
            tmp.insert(firstIndex, (stack, stackDrawStyle, "dummy"))
            histos = tmp

        for h, style, dname in histos:
            h.Draw(style+" same")

    def mergeDatasets(self, newName, datasetNameList):
        indices = []
        dataCount = 0
        mcCount = 0
        newData = []
        for i, d in enumerate(self.data):
            if d.dataset.getName() in datasetNameList:
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
            raise Exception("Can not merge data and MC datasets!")

        if len(indices) == 0:
            print "Merging datasets: no datasets '" + ", ".join(datasetNameList) + "' found, not doing anything"
            return
        if len(indices) == 1:
            print "Merging datasets: one dataset '" + self.data[indices[0]].dataset.getName() + "' found from list '" + ", "+join(datasetNameList)+", not doing anything"
            return

        dataset = None
        if dataCount > 0:
            if self.normalization == "one":
                raise Exception("Can not merge data datasets after normalizeToOne!")

            # Calculate the total integrated luminosity
            lumiSum = 0.0
            for i in indices:
                lumiSum += self.data[i].dataset.getLuminosity()
            dataset = Dataset(newName, {"luminosity": lumiSum}, None)

        else:
            if self.normalization != "byCrossSection":
                raise Exception("MC datasets must be normalized by cross section before merging!")

            # If we can sum the histograms together, we can sum the
            # cross sections too. It is purely in the user's
            # responsibility to decide if this is correct or not
            crossSum = 0.0
            for i in indices:
                crossSum += self.data[i].dataset.getCrossSection()
            dataset = Dataset(newName, {"crossSection": crossSum}, None)

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
            h.Scale(d.getNormFactor())
            h.GetYaxis().SetTitle("Cross section (pb^{-1})")
                
        self.normalization = "byCrossSection"

    def normalizeMCByLuminosity(self):
        if not self.normalization in ["none", "byCrossSection"]
            raise Exception("Histograms already normalized")

        self.luminosity = None
        for d in self.data:
            if d.dataset.isData():
                if self.luminosity != None:
                    raise Exception("Only one data dataset may exist for normalizing byLuminosity; you can remove other data datasets, merge them or use normalizeMCToLuminosity(lumi)")
                self.luminosity = d.dataset.getLuminosity()


        self.normalizeMCToLuminosity(self, self.luminosity)
        self.normalization = "byLumi"

    def normalizeMCToLuminosity(self, lumi):
        if not self.normalization in ["none", "byCrossSection"]
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
        self.normalization = "toLumi"


def addOptions(parser):
    parser.add_option("-i", dest="input", type="string", default="histograms-*.root",
                      help="Pattern for input root files (note: remember to escape * and ? !) (default: 'histograms-*.root')")
    parser.add_option("-f", dest="files", type="string", action="append", default=[],
                      help="Give input ROOT files explicitly, if these are given, multicrab.cfg is not read and -d/-i parameters are ignored")

def getDatasets(opts=None):
    if opts == None:
        parser = OptionParser(usage="Usage: %prog [options]")
        multicrab.addOptions(parser)
        addOptions(parser)
        (opts, args) = parser.parse_args()

    datasets = DatasetSet()
    
    taskdirs = multicrab.getTaskDirectories(opts)
    for d in taskdirs:
        files = glob.glob(os.path.join(d, "res", opts.input))
        if len(files) > 1:
            raise Exception("Only one file should match the input (%d matched) for task %s" % (len(files), d))
            return 1
        elif len(files) == 0:
            raise Exception("No files matched to input for task %s" % d)

        datasets.append(counter.readDataset(files[0], opts.counterdir, d, {}))

    return datasets

   
