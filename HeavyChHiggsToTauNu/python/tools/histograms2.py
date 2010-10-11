import os
import glob
from optparse import OptionParser

import ROOT

import multicrab
from dataset import Dataset

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

def getHistoSet(datasetSet, name):
    return HistoSet(datasetSet.getHistoWrappers(name))

class HistoSetData:
    def __init__(self, dataset, histo):
        self.dataset = dataset
        self.histo = histo
        self.legendLabel = dataset.getName()
        self.legendStyle = "l"
        self.drawStyle = "HIST"

    def getHistogram(self):
        return self.histo

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

    def getHistogram(self):
        return self.histo

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
    def __init__(self, histoWrappers):
        self.histoWrappers = histoWrappers
        self.data = None
        self.luminosity = None

    def normalizeToOne(self):
        self.data = None
        for h in self.histoWrappers:
            h.normalizeToOne()

    def normalizeMCByCrossSection(self):
        self.data = None
        for h in self.histoWrappers:
            if h.getDataset().isMC():
                h.normalizeByCrossSection()

    def normalizeMCByLuminosity(self):
        self.data = None
        lumi = None
        for h in self.histoWrappers:
            if h.getDataset().isData():
                if lumi != None:
                    raise Exception("Unable to normalize by luminosity, more than one data datasets (you might want to merge data datasets)")
                lumi = h.getDataset().getLuminosity()

        if lumi == None:
            raise Exception("Unable to normalize by luminosity, no data datasets")

        self.normalizeMCToLuminosity(self, sumLumi)

    def normalizeMCToLuminosity(self, lumi):
        self.data = None
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
            self.datasetHistoMap[h.getDataset().getName()] = h

    def forEachHisto(self, func):
        if self.data == None:
            raise Exception("createHistogramObjects() must be called first")

        for d in self.data:
            d.applyFunction(func)

    def getHisto(self, name):
        return self.datasetHistoMap[name].histo

    def getHistoList(self):
        return [d.getHistogram() for d in self.data]

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



