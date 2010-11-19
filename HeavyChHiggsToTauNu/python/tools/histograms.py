import os, sys
import glob
from optparse import OptionParser

import ROOT

import multicrab
from dataset import Dataset, mergeStackHelper

class TextDefaults:
    def __init__(self):
        self._setDefaults("cmsPreliminary", 0.62, 0.96, 0.05)
        self._setDefaults("energy", 0.3, 0.96, 0.05)
        self._setDefaults("lumi", 0.65, 0.85, 0.05)

    def _setDefaults(self, name, x, y, size):
        if x != None:
            setattr(self, name+"_x", x)
        if y != None:
            setattr(self, name+"_y", y)
        if size != None:
            setattr(self, name+"_size", size)
            
    def setCmsPreliminaryDefaults(self, x=None, y=None, size=None):
        self._setDefaults("cmsPreliminary", x, y, size)

    def setEnergyDefaults(self, x=None, y=None, size=None):
        self._setDefaults("energy", x, y, size)
        
    def setLuminosityDefaults(self, x=None, y=None, size=None):
        self._setDefaults("lumi", x, y, size)

    def getValues(self, name, x, y):
        if x == None:
            x = getattr(self, name+"_x")
        if y == None:
            y = getattr(self, name+"_y")
        return (x, y)

    def getSize(self, name):
        return getattr(self, name+"_size")

textDefaults = TextDefaults()

def addCmsPreliminaryText(x=None, y=None):
    (x, y) = textDefaults.getValues("cmsPreliminary", x, y)
    l = ROOT.TLatex()
    l.SetNDC()
    l.SetTextSize(textDefaults.getSize("cmsPreliminary"))
    l.DrawLatex(x, y, "CMS Preliminary")

def addEnergyText(x=None, y=None, s="7 TeV"):
    (x, y) = textDefaults.getValues("energy", x, y)
    l = ROOT.TLatex()
    l.SetNDC()
    l.SetTextSize(textDefaults.getSize("energy"))
    l.DrawLatex(x, y, "#sqrt{s} = "+s)

def addLuminosityText(x, y, lumi, unit="pb^{1}"):
    (x, y) = textDefaults.getValues("lumi", x, y)
    l = ROOT.TLatex()
    l.SetNDC()
    l.SetTextSize(textDefaults.getSize("lumi"))
    l.DrawLatex(x, y, "#intL=%.2f %s" % (lumi, unit))

class LegendCreator:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def copy(self):
        return LegendCreator(self.x1, self.y1, self.x2, self.y2)

    def setDefaults(self, x1=None, y1=None, x2=None, y2=None):
        if x1 != None:
            self.x1 = x1
        if y1 != None:
            self.y1 = y1
        if x2 != None:
            self.x2 = x2
        if y2 != None:
            self.y2 = y2

    def __call__(self, x1=None, y1=None, x2=None, y2=None):
        if x1 == None:
            x1 = self.x1
        if y1 == None:
            y1 = self.y1
        if x2 == None:
            x2 = self.x2
        if y2 == None:
            y2 = self.y2

        legend = ROOT.TLegend(x1, y1, x2, y2)
        legend.SetFillColor(ROOT.kWhite)
        legend.SetBorderSize(1)
        #legend.SetMargin(0.1)
        return legend

createLegend = LegendCreator(0.7, 0.6, 0.92, 0.92)

class HistoSetData:
    def __init__(self, dataset, histo):
        self.dataset = dataset
        self.histo = histo
        self.legendLabel = dataset.getName()
        self.legendStyle = "l"
        self.drawStyle = "HIST"

    def getHistogram(self):
        return self.histo

    def isMC(self):
        return self.dataset.isMC()

    def isData(self):
        return self.dataset.isData()

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

    def call(self, func):
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

    def getHistogram(self):
        return self.histo

    def isMC(self):
        return self.data[0].isMC()

    def isData(self):
        return self.data[0].isData()

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

    def call(self, function):
        for d in self.data:
            d.call(function)

    def getXmin(self):
        return min([d.getXmin() for d in self.data])

    def getXmax(self):
        return max([d.getXmax() for d in self.data])

class HistoSet:
    def __init__(self, datasetSet, name):
        self.datasets = datasetSet
        self.histoWrappers = datasetSet.getHistoWrappers(name)
        self.data = None
        self.luminosity = None

    def normalizeToOne(self):
        if self.data != None:
            raise Exception("Can't normalize after the histograms have been created!")
        for h in self.histoWrappers:
            h.normalizeToOne()

    def normalizeMCByCrossSection(self):
        if self.data != None:
            raise Exception("Can't normalize after the histograms have been created!")
        for h in self.histoWrappers:
            if h.getDataset().isMC():
                h.normalizeByCrossSection()

    def normalizeMCByLuminosity(self):
        if self.data != None:
            raise Exception("Can't normalize after the histograms have been created!")
        lumi = None
        for h in self.histoWrappers:
            if h.getDataset().isData():
                if lumi != None:
                    raise Exception("Unable to normalize by luminosity, more than one data datasets (you might want to merge data datasets)")
                lumi = h.getDataset().getLuminosity()

        if lumi == None:
            raise Exception("Unable to normalize by luminosity, no data datasets")

        self.normalizeMCToLuminosity(lumi)

    def normalizeMCToLuminosity(self, lumi):
        if self.data != None:
            raise Exception("Can't normalize after the histograms have been created!")
        for h in self.histoWrappers:
            if h.getDataset().isMC():
                h.normalizeToLuminosity(lumi)
        self.luminosity = lumi

    def createHistogramObjects(self):
        self.data = []
        for h in self.histoWrappers:
            self.data.append(HistoSetData(h.getDataset(), h.getHistogram()))
        self.populateMap()

    def populateMap(self):
        self.datasetHistoMap = {}
        for h in self.data:
            self.datasetHistoMap[h.getName()] = h

    def forHisto(self, name, func):
        if self.data == None:
            self.createHistogramObjects()

        try:
            self.datasetHistoMap[name].call(func)
        except KeyError:
            print >> sys.stderr, "WARNING: Tried to call a function for histogram '%s', which doesn't exist." % name

    def forEachMCHisto(self, func):
        self.forEachHisto(func, lambda x: x.isMC())

    def forEachDataHisto(self, func):
        self.forEachHisto(func, lambda x: x.isData())

    def forEachHisto(self, func, predicate=lambda x: True):
        if self.data == None:
            self.createHistogramObjects()

        for d in self.data:
            if predicate(d):
                d.call(func)

    def hasHisto(self, name):
        if self.data == None:
            self.createHistogramObjects()

        return name in self.datasetHistoMap

    def getHisto(self, name):
        if self.data == None:
            self.createHistogramObjects()

        return self.datasetHistoMap[name].histo

    def getHistoList(self):
        if self.data == None:
            self.createHistogramObjects()

        return [d.getHistogram() for d in self.data]

    def setHistoLegendLabel(self, name, label):
        if self.data == None:
            self.createHistogramObjects()

        try:
            self.datasetHistoMap[name].setLegendLabel(label)
        except KeyError:
            print >> sys.stderr, "WARNING: Tried to set legend label for histogram '%s', which doesn't exist." % name

    def setHistoLegendLabels(self, nameMap):
        if self.data == None:
            self.createHistogramObjects()

        for name, label in nameMap.iteritems():
            self.setHistoLegendLabel(name, label)

    def setHistoLegendStyle(self, name, style):
        if self.data == None:
            self.createHistogramObjects()

        try:
            self.datasetHistoMap[name].setLegendStyle(style)
        except KeyError:
            print >> sys.stderr, "WARNING: Tried to set legend style for histogram '%s', which doesn't exist." % name

    def setHistoLegendStyleAll(self, style):
        if self.data == None:
            self.createHistogramObjects()

        for d in self.data:
            d.setLegendStyle(style)

    def setHistoDrawStyle(self, name, style):
        if self.data == None:
            self.createHistogramObjects()

        try:
            self.datasetHistoMap[name].drawStyle = style
        except KeyError:
            print >> sys.stderr, "WARNING: Tried to set draw style for histogram '%s', which doesn't exist." % name

    def setHistoDrawStyleAll(self, style):
        if self.data == None:
            self.createHistogramObjects()

        for d in self.data:
            d.drawStyle = style

    def getLuminosity(self):
        if self.luminosity == None:
            raise Exception("No normalization by or to luminosity!")
        return self.luminosity

    def addLuminosityText(self, x=None, y=None): # Nones for the default values
        addLuminosityText(x, y, self.getLuminosity(), "pb^{-1}")

    def createCanvasFrame(self, name, ymin=None, ymax=None, xmin=None, xmax=None, yfactor=1.1):
        if self.data == None:
            self.createHistogramObjects()

        if len(self.data) == 0:
            raise Exception("Empty set of histograms!")

        c = ROOT.TCanvas(name)
        if ymin == None:
            ymin = min([d.histo.GetMinimum() for d in self.data])
        if ymax == None:
            ymax = max([d.histo.GetMaximum() for d in self.data])
            ymax = yfactor*ymax

        if xmin == None:
            xmin = min([d.getXmin() for d in self.data])
        if xmax == None:
            xmax = min([d.getXmax() for d in self.data])

        frame = c.DrawFrame(xmin, ymin, xmax, ymax)
        frame.GetXaxis().SetTitle(self.data[0].histo.GetXaxis().GetTitle())
        frame.GetYaxis().SetTitle(self.data[0].histo.GetYaxis().GetTitle())

        return (c, frame)

    def addToLegend(self, legend):
        if self.data == None:
            self.createHistogramObjects()

        for d in self.data:
            d.addToLegend(legend)

    def draw(self, inReverseOrder=True):
        if self.data == None:
            self.createHistogramObjects()

        histos = [(d.histo, d.drawStyle, d.getName()) for d in self.data]
        if inReverseOrder:
            histos.reverse()

        for h, style, dname in histos:
            h.Draw(style+" same")

    def stackMCHistograms(self):
        self.stackHistograms("Stacked MC", self.datasets.getMCDatasetNames())

    def stackHistograms(self, newName, nameList):
        if self.data == None:
            self.createHistogramObjects()

        (selected, notSelected, firstIndex) = mergeStackHelper(self.data, nameList, "stack")
        if len(selected) == 0:
            return

        notSelected.insert(firstIndex, HistoSetDataStacked(selected, newName))
        self.data = notSelected
        self.populateMap()



