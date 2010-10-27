import os, sys
import glob
from optparse import OptionParser

import ROOT

import multicrab
from dataset import Dataset, mergeStackHelper

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

        if not name in self.datasetHistoMap:
            print >> sys.stderr, "WARNING: Tried to set legend label for dataset '%s', which doesn't exist." % name
            return

        self.datasetHistoMap[name].setLegendLabel(label)

    def setHistoLegendLabels(self, nameMap):
        if self.data == None:
            self.createHistogramObjects()

        for name, label in nameMap.iteritems():
            self.setHistoLegendLabel(name, label)

    def setHistoLegendStyle(self, name, style):
        if self.data == None:
            self.createHistogramObjects()

        if not name in self.datasetHistoMap:
            print >> sys.stderr, "WARNING: Tried to set legend style for dataset '%s', which doesn't exist." % name
            return

        self.datasetHistoMap[name].setLegendStyle(style)

    def setHistoLegendStyleAll(self, style):
        if self.data == None:
            self.createHistogramObjects()

        for d in self.data:
            d.setLegendStyle(style)

    def setHistoDrawStyle(self, name, style):
        if self.data == None:
            self.createHistogramObjects()

        self.datasetHistoMap[name].drawStyle = style

    def setHistoDrawStyleAll(self, style):
        if self.data == None:
            self.createHistogramObjects()

        for d in self.data:
            d.drawStyle = style

    def getLuminosity(self):
        if self.luminosity == None:
            raise Exception("No normalization by or to luminosity!")
        return self.luminosity

    def addLuminosityText(self, x=0.65, y=0.85):
        addLuminosityText(x, y, self.getLuminosity(), "pb^{-1}")

    def createCanvasFrame(self, name, ymin=None, ymax=None, xmin=None, xmax=None):
        if self.data == None:
            self.createHistogramObjects()

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



