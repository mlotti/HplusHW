import os, sys
import glob
from optparse import OptionParser

import ROOT

import multicrab
from dataset import Dataset, mergeStackHelper

class TextDefaults:
    """Class to provide default positions of the various texts.

    The attributes which can be set are the x and y coordinates and
    the text size.
    """
    def __init__(self):
        self._setDefaults("cmsPreliminary", x=0.62, y=0.96)
        self._setDefaults("energy", x=0.3, y=0.96)
        self._setDefaults("lumi", x=0.65, y=0.85)

    def _setDefaults(self, name, **kwargs):
        for x, value in kwargs.iteritems():
            setattr(self, name+"_"+x, value)
            
    def setCmsPreliminaryDefaults(self, **kwargs):
        self._setDefaults("cmsPreliminary", **kwargs)

    def setEnergyDefaults(self, **kwargs):
        self._setDefaults("energy", **kwargs)
        
    def setLuminosityDefaults(self, **kwargs):
        self._setDefaults("lumi", **kwargs)

    def getValues(self, name, x, y):
        if x == None:
            x = getattr(self, name+"_x")
        if y == None:
            y = getattr(self, name+"_y")
        return (x, y)

    def getSize(self, name):
        try:
            return getattr(self, name+"_size")
        except AttributeError:
            return ROOT.gStyle.GetTextSize()

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

def addLuminosityText(x, y, lumi, unit="pb^{-1}"):
    (x, y) = textDefaults.getValues("lumi", x, y)
    l = ROOT.TLatex()
    l.SetNDC()
    l.SetTextSize(textDefaults.getSize("lumi"))
    l.DrawLatex(x, y, "#intL=%.2f %s" % (lumi, unit))

class LegendCreator:
    """Class for generating legend creation functions with default positions.

    The intended usage is demonstrated in histograms.py below, i.e.
    createLegend = LegendCreator(x1, y1, x2, y2)
    createLegend.setDefaults(x1=0.4, y2=0.5)
    legend = createLegend()
    """

    def __init__(self, x1, y1, x2, y2, textSize=0.025):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.textSize = textSize
        self._keys = ["x1", "y1", "x2", "y2"]

    def copy(self):
        return LegendCreator(self.x1, self.y1, self.x2, self.y2)

    def setDefaults(self, **kwargs):
        """Set new default positions.

        Keyword arguments: x1, y1, x2, y2, textSize
        """
        for x, value in kwargs.iteritems():
            setattr(self, x, value)

    def __call__(self, *args, **kwargs):
        """Create a new TLegend based.

        Arguments can be either
        - Four numbers for the coordinates (x1, y1, x2, y2), or
        - Keyword arguments: x1, y1, x2, y2

        If all 4 coordinates are specified, they are used. In the
        keyword argument case, the coordinates which are not given are
        taken from the default values.
        """
        if len(args) == 4:
            if len(kwargs) != 0:
                raise Exception("Got 4 positional arguments, no keyword arguments allowed")
            for i, k in enumerate(self._keys):
                kwargs[k] = args[i]
        elif len(args) != 0:
            raise Exception("If positional arguments given, must give 4")
        else:
            for i in self._keys:
                if not i in kwargs:
                    kwargs[i] = getattr(self, i)

        legend = ROOT.TLegend(kwargs["x1"], kwargs["y1"], kwargs["x2"], kwargs["y2"])
        legend.SetFillColor(ROOT.kWhite)
        legend.SetBorderSize(1)
        legend.SetTextFont(legend.GetTextFont()-1) # From x3 to x2
        legend.SetTextSize(self.textSize)
        #legend.SetMargin(0.1)
        return legend

createLegend = LegendCreator(0.7, 0.6, 0.92, 0.92)

def updatePaletteStyle(histo):
    """Update the style of palette Z axis according to ROOT.gStyle."""
    ROOT.gPad.Update()
    paletteAxis = histo.GetListOfFunctions().FindObject("palette")
    if paletteAxis == None:
        return
    paletteAxis.SetLabelColor(ROOT.gStyle.GetLabelColor())
    paletteAxis.SetLabelFont(ROOT.gStyle.GetLabelFont())
    paletteAxis.SetLabelOffset(ROOT.gStyle.GetLabelOffset())
    paletteAxis.SetLabelSize(ROOT.gStyle.GetLabelSize())

def _kwargsDefault(kwargs, name, default):
    if name in kwargs:
        return kwargs[name]
    return default

def _boundsArgs(histos, kwargs):
    ymaxfactor = _kwargsDefault(kwargs, "ymaxfactor", 1.1)

    if not "ymax" in kwargs:
        kwargs["ymax"] = ymaxfactor * max([d.histo.GetMaximum() for d in histos])
    if not "ymin" in kwargs:
        if "yminfactor" in kwargs:
            kwargs["ymin"] = kwargs["yminfactor"]*kwargs["ymax"]
        else:
            kwargs["ymin"] = min([d.histo.GetMinimum() for d in histos])

    if not "xmin" in kwargs:
        kwargs["xmin"] = min([d.getXmin() for d in histos])
    if not "xmax" in kwargs:
        kwargs["xmax"] = min([d.getXmax() for d in histos])


class CanvasFrame:
    """Create TCanvas and frame for one TPad."""
    def __init__(self, histoManager, name, **kwargs):
        """Create TCanvas and TH1 for the frame.

        Arguments:
        histoManager  HistoManager object to take the histograms for automatic axis ranges
        name          Name for TCanvas (will be the file name, if TCanvas.SaveAs(".png") is used)
        
        Keyword arguments:
        ymin     Minimum value of Y axis
        ymax     Maximum value of Y axis
        xmin     Minimum value of X axis
        xmax     Maximum value of X axis
        ymaxfactor  Maximum value of Y is ymax*ymaxfactor (default 1.1)
        yminfactor  Minimum value of Y is ymax*yminfactor (yes, calculated from ymax

        By default ymin, ymax, xmin and xmax are taken as the
        maximum/minimums of the histogram objects such that frame
        contains all histograms. The ymax is then multiplied with
        ymaxfactor

        The yminfactor/ymaxfactor are used only if ymin/ymax is taken
        from the histograms, i.e. ymax keyword argument is *not*
        given.
        """
        histos = histoManager.getHistoDataList()
        if len(histos) == 0:
            raise Exception("Empty set of histograms!")

        self.canvas = ROOT.TCanvas(name)

        if "yfactor" in kwargs:
            if "ymaxfactor" in kwargs:
                raise Exception("Only one of ymaxfactor, yfactor can be given")
            kwargs["ymaxfactor"] = kwargs["yfactor"]

        _boundsArgs(histos, kwargs)

        self.frame = self.canvas.DrawFrame(kwargs["xmin"], kwargs["ymin"], kwargs["xmax"], kwargs["ymax"])
        self.frame.GetXaxis().SetTitle(histos[0].histo.GetXaxis().GetTitle())
        self.frame.GetYaxis().SetTitle(histos[0].histo.GetYaxis().GetTitle())

class CanvasFrameTwo:
    """Create TCanvas and frames for to TPads."""
    def __init__(self, histoManager1, histos2, name, **kwargs):
        """Create TCanvas and TH1 for the frame.

        Arguments:
        histoManager1 HistoManager object to take the histograms for automatic axis ranges for upper pad
        histos2       List of TH1s to take the histograms for automatic axis ranges for lower pad
        name          Name for TCanvas (will be the file name, if TCanvas.SaveAs(".png") is used)
        
        Keyword arguments:
        opts1                   Dictionary for histoManager1 options
        opts2                   Dictionary for histos2 options
        canvasFactor            Multiply the canvas height by this factor (default 1.25)
        canvasHeightCorrection  Add this to the height of the lower pad (default 0.022)

        Options:
        ymin     Minimum value of Y axis
        ymax     Maximum value of Y axis
        xmin     Minimum value of X axis (only for opts1)
        xmax     Maximum value of X axis (only for opts1)
        ymaxfactor  Maximum value of Y is ymax*ymaxfactor (default 1.1)
        yminfactor  Minimum value of Y is ymax*yminfactor (yes, calculated from ymax

        By default ymin, ymax, xmin and xmax are taken as the
        maximum/minimums of the histogram objects such that frame
        contains all histograms. The ymax is then multiplied with
        ymaxfactor

        The yminfactor/ymaxfactor are used only if ymin/ymax is taken
        from the histograms, i.e. ymax keyword argument is *not*
        given.
        """
        class FrameWrapper:
            """Wrapper to provide the CanvasFrameTwo.frame member.

            The GetXaxis() is forwarded to the frame of the lower pad,
            and the GetYaxis() is forwared to the frame of the upper pad.
            """
            def __init__(self, frame1, frame2):
                self.frame1 = frame1
                self.frame2 = frame2

            def GetXaxis(self):
                return self.frame2.GetXaxis()

            def GetYaxis(self):
                return self.frame1.GetYaxis()

        class HistoWrapper:
            """Wrapper to provide the getXmin/getXmax functions for _boundsArgs function."""
            def __init__(self, histo):
                self.histo = histo

            def getXmin(self):
                return self.histo.GetXaxis().GetBinLowEdge(self.histo.GetXaxis().GetFirst())

            def getXmax(self):
                return self.histo.GetXaxis().GetBinUpEdge(self.histo.GetXaxis().GetLast())

        histos1 = histoManager1.getHistoDataList()
        if len(histos1) == 0:
            raise Exception("Empty set of histograms for first pad!")
        if len(histos2) == 0:
            raise Exception("Empty set of histograms for second pad!")

        canvasFactor = _kwargsDefault(kwargs, "canvasFactor", 1.25)
        canvasHeightCorrection = _kwargsDefault(kwargs, "canvasHeightCorrection", 0.022)
        divisionPoint = 1-1/canvasFactor

        opts1 = _kwargsDefault(kwargs, "opts1", {})
        opts2 = _kwargsDefault(kwargs, "opts2", {})

        if "xmin" in opts2 or "xmax" in opts2:
            raise Exception("No 'xmin' or 'xmax' allowed in opts2")
        

        _boundsArgs(histos1, opts1)
        opts2["xmin"] = opts1["xmin"]
        opts2["ymin"] = opts1["ymin"]
        _boundsArgs([HistoWrapper(h) for h in histos2], opts2)

        # Create the canvas, divide it to two
        self.canvas = ROOT.TCanvas(name, name, ROOT.gStyle.GetCanvasDefW(), int(ROOT.gStyle.GetCanvasDefH()*canvasFactor))
        self.canvas.Divide(1, 2)
        
        # Set the lower point of the upper pad to divisionPoint
        self.pad1 = self.canvas.cd(1)
        (xlow, ylow, xup, yup) = [ROOT.Double(x) for x in [0.0]*4]
        self.pad1.GetPadPar(xlow, ylow, xup, yup)
        self.pad1.SetPad(xlow, divisionPoint, xup, yup)

        # Set the upper point of the lower pad to divisionPoint
        self.pad2 = self.canvas.cd(2)
        self.pad2.GetPadPar(xlow, ylow, xup, yup)
        self.pad2.SetPad(xlow, ylow, xup,
                         divisionPoint+ROOT.gStyle.GetPadBottomMargin()-ROOT.gStyle.GetPadTopMargin()+canvasHeightCorrection)
        self.pad2.SetFillStyle(4000)
        self.pad2.SetTopMargin(0.0)
        #self.pad2.SetBottomMargin(self.pad2.GetBottomMargin()+0.06)
        self.pad2.SetBottomMargin(self.pad2.GetBottomMargin()+0.16)

        self.canvas.cd(1)

        yoffsetFactor = canvasFactor*1.15
        #xoffsetFactor = canvasFactor*1.6
        #xoffsetFactor = canvasFactor*2
        xoffsetFactor = 0.5*canvasFactor/(canvasFactor-1) * 1.3

        self.frame1 = self.pad1.DrawFrame(opts1["xmin"], opts1["ymin"], opts1["xmax"], opts1["ymax"])
        (labelSize, titleSize) = (self.frame1.GetXaxis().GetLabelSize(), self.frame1.GetXaxis().GetTitleSize())
        self.frame1.GetXaxis().SetLabelSize(0)
        self.frame1.GetXaxis().SetTitleSize(0)
        self.frame1.GetYaxis().SetTitle(histos1[0].histo.GetYaxis().GetTitle())
        self.frame1.GetYaxis().SetTitleOffset(self.frame1.GetYaxis().GetTitleOffset()*yoffsetFactor)

        self.canvas.cd(2)
        self.frame2 = self.pad2.DrawFrame(opts2["xmin"], opts2["ymin"], opts2["xmax"], opts2["ymax"])
        self.frame2.GetXaxis().SetTitle(histos1[0].histo.GetXaxis().GetTitle())
        self.frame2.GetYaxis().SetTitle(histos2[0].GetYaxis().GetTitle())
        self.frame2.GetYaxis().SetTitleOffset(self.frame2.GetYaxis().GetTitleOffset()*yoffsetFactor)
        self.frame2.GetXaxis().SetTitleOffset(self.frame2.GetXaxis().GetTitleOffset()*xoffsetFactor)

        self.canvas.cd(1)
        self.frame = FrameWrapper(self.frame1, self.frame2)


class HistoData:
    """Class to represent one (TH1/TH2) histogram."""

    def __init__(self, dataset, histo):
        """Constructor

        Arguments:
        dataset   Dataset object
        histo     TH1 object

        The default legend label is the dataset name
        """
        self.dataset = dataset
        self.name = dataset.getName()
        self.histo = histo
        self.legendLabel = dataset.getName()
        self.legendStyle = "l"
        self.drawStyle = "HIST"

    def getHistogram(self):
        """Get the TH1 object."""
        return self.histo

    def isMC(self):
        return self.dataset.isMC()

    def isData(self):
        return self.dataset.isData()

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def setLegendLabel(self, label):
        self.legendLabel = label

    def setLegendStyle(self, style):
        """Legend style can be anything TLegend.AddEntry() takes as the 3rd argument."""
        self.legendStyle = style

    def addToLegend(self, legend):
        """Add the histogram to a TLegend."""
        legend.AddEntry(self.histo, self.legendLabel, self.legendStyle)

    def callHisto(self, func):
        """Call a function with the TH1 as an argument.

        The return value of the function is used as the new histogram.

        """
        h = func(self.histo)
        if h != None:
            self.histo = h

    def getXmin(self):
        return self.histo.GetXaxis().GetBinLowEdge(self.histo.GetXaxis().GetFirst())

    def getXmax(self):
        return self.histo.GetXaxis().GetBinUpEdge(self.histo.GetXaxis().GetLast())

class HistoDataStacked:
    """Class to represent stacked TH1 histograms."""

    def __init__(self, data, name):
        """Constructor.

        Arguments:
        data    List of HistoData objects to stack
        name    Name of the stacked histogram

        Stacking is done with the help of THStack object
        """
        self.data = data
        self.drawStyle = "HIST"
        self.name = name
        
        self.histo = ROOT.THStack(name+"stackHist", name+"stackHist")
        histos = [d.histo for d in self.data]
        histos.reverse()
        for h in histos:
            self.histo.Add(h)

    def getHistogram(self):
        """Get the THStack histogram."""
        return self.histo

    def getAllHistograms(self):
        """Get the original histograms."""
        return [x.getHistogram() for x in self.data]

    def getSumHistogram(self):
        """Get the sum of the original histograms."""
        h = self.data[0].getHistogram().Clone()
        h.SetName(h.GetName()+"_sum")
        for d in self.data[1:]:
            h.Add(d.getHistogram())
        return h

    def isMC(self):
        return self.data[0].isMC()

    def isData(self):
        return self.data[0].isData()

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def setLegendLabel(self, label):
        """Set the legend labels of the stacked histograms."""
        for d in self.data:
            d.setLegendLabel(label)

    def setLegendStyle(self, style):
        """Set the legend style of the stacked histograms."""
        for d in self.data:
            d.setLegendStyle(style)

    def addToLegend(self, legend):
        """Add the stacked histograms to a TLegend."""
        for d in self.data:
            d.addToLegend(legend)

    def callHisto(self, function):
        """Call a function for each histogram in the stack."""
        for d in self.data:
            d.callHisto(function)

    def getXmin(self):
        return min([d.getXmin() for d in self.data])

    def getXmax(self):
        return max([d.getXmax() for d in self.data])

class HistoStatError:
    """Class to represent combined statistical errors of many histograms."""

    def __init__(self, histoDatas, name):
        self.histos = histoDatas
        self.name = name
        self.legendLabel = name
        self.legendStyle = "F"
        self.drawStyle = "E2"

        histos = []
        for h in self.histos:
            if hasattr(h, "getSumHistogram"):
                histos.append(h.getSumHistogram())
            else:
                histos.append(h.getHistogram())

        self.histo = histos[0].Clone()
        self.histo.SetName(self.histo.GetName()+"_errors")
        for h in histos[1:]:
            self.histo.Add(h)

    def isMC(self):
        return self.histos[0].isMC()

    def isData(self):
        return self.histos[0].isData()

    def getName(self):
        return self.name

    def setName(self):
        self.name = name

    def setLegendLabel(self, label):
        self.legendLabel = label

    def setLegendStyle(self, style):
        self.legendStyle = style

    def addToLegend(self, legend):
        legend.AddEntry(self.histo, self.legendLabel, self.legendStyle)

    def callHisto(self, function):
        h = function(self.histo)
        if h != None:
            self.histo = h

    def getXmin(self):
        return self.histo.GetXaxis().GetBinLowEdge(self.histo.GetXaxis().GetFirst())

    def getXmax(self):
        return self.histo.GetXaxis().GetBinUpEdge(self.histo.GetXaxis().GetLast())
        

class HistoManagerImpl:
    """Implementation of HistoManager.

    Intended to be used only from HistoManager. This class contains all
    the methods which require the HistoData objects (and only them).
    """
    def __init__(self, histos=[]):
        # List for the Draw() order, keep it reversed in order to draw
        # the last histogram in the list first. i.e. to the bottom
        self.drawList = histos[:]

        # List for the legend order, first histogram is also first in
        # the legend
        self.legendList = histos[:]

        # Dictionary for accessing the histograms by name
        self._populateMap()

    def __len__(self):
        return len(self.drawList)

    def _populateMap(self):
        self.nameHistoMap = {}
        for h in self.drawList:
            self.nameHistoMap[h.getName()] = h

    def append(self, histoWrapper):
        """Append a HistoData object."""
        self.drawList.append(histoWrapper)
        self.legendList.append(histoWrapper)
        self._populateMap()

    def extend(self, histoWrappers):
        """Extend with a list of HistoData objects."""
        self.drawList.extend(histoWrappers)
        self.legendList.extend(histoWrappers)
        self._populateMap()

    def insert(self, i, histoWrapper, **kwargs):
        """Insert HistoData to position i.

        Arguments:
        i             Index of the position to insert the histogram
        histoWrapper  HistoData object to insert

        Keyword arguments:

        legendIndex   Index of the position to insert the histogram in
                      the legend list (default is the same as i). Can
                      be useful for e.g. separate uncertainty
                      histogram
        """
        drawIndex = i
        legendIndex = i

        if "legendIndex" in kwargs:
            legendIndex = kwargs["legendIndex"]

        self.drawList.insert(drawIndex, histoWrapper)
        self.legendList.insert(legendIndex, histoWrapper)
        self._populateMap()

    def forHisto(self, name, func):
        """Call a function for a histogram.

        Arguments:
        name   Name of histogram
        func   Function taking one parameter (TH1), return value is used
               as the new histogram
        """
        try:
            self.nameHistoMap[name].callHisto(func)
        except KeyError:
            print >> sys.stderr, "WARNING: Tried to call a function for histogram '%s', which doesn't exist." % name

    def forEachMCHisto(self, func):
        """Call each MC histogram with a function.

        Arguments:
        func   Function taking one parameter (TH1), return value is used
               as the new histogram
        """
        self.forEachHisto(func, lambda x: x.isMC())

    def forEachDataHisto(self, func):
        """Call each data histogram with a function.

        Arguments:
        func   Function taking one parameter (TH1), return value is used
               as the new histogram
        """
        self.forEachHisto(func, lambda x: x.isData())

    def forEachHisto(self, func, predicate=lambda x: True):
        """Call each histogram with a function.

        Arguments:
        func        Function taking one parameter (TH1), return value is used
                    as the new histogram
        predicate   Call func() only if predicate returns True. The
                    HistoData object is given to the predicate
        """
        for d in self.drawList:
            if predicate(d):
                d.callHisto(func)

    def hasHisto(self, name):
        return name in self.nameHistoMap

    def getHisto(self, name):
        """Get TH1 of a given name."""
        return self.getHistoData(name).getHistogram()

    def getHistoData(self, name):
        """Get HistoData of a given name."""
        return self.nameHistoMap[name]

    def getHistoList(self):
        """Get list of TH1 histograms."""
        return [d.getHistogram() for d in self.histos]

    def getHistoDataList(self):
        return self.drawList[:]

    def setHistoLegendLabel(self, name, label):
        """Set legend name for a given histogram.

        Arguments:
        name   Name of the histogram
        label  Label for legend
        """
        try:
            self.nameHistoMap[name].setLegendLabel(label)
        except KeyError:
            print >> sys.stderr, "WARNING: Tried to set legend label for histogram '%s', which doesn't exist." % name

    def setHistoLegendLabels(self, nameMap):
        """Set legend names for given histograms.

        Arguments:
        nameMap   Dictionary with name->label mappings
        """
        for name, label in nameMap.iteritems():
            self.setHistoLegendLabel(name, label)

    def setHistoLegendStyle(self, name, style):
        """Set the legend style for a given histogram.

        Arguments:
        name   Name of the histogram
        style  Style for the legend (given to TLegend as 3rd argument)
        """
        try:
            self.nameHistoMap[name].setLegendStyle(style)
        except KeyError:
            print >> sys.stderr, "WARNING: Tried to set legend style for histogram '%s', which doesn't exist." % name

    def setHistoLegendStyleAll(self, style):
        """Set the legend style for all histograms.

        Arguments:
        style  Style for the legend (given to TLegend as 3rd argument)
        """
        for d in self.legendList:
            d.setLegendStyle(style)

    def setHistoDrawStyle(self, name, style):
        """Set histogram drawing style for a given histogram.

        Arguments:
        name   Name of the histogram
        style  Style for obj.Draw() call
        """
        try:
            self.nameHistoMap[name].drawStyle = style
        except KeyError:
            print >> sys.stderr, "WARNING: Tried to set draw style for histogram '%s', which doesn't exist." % name

    def setHistoDrawStyleAll(self, style):
        """Set the histogram drawing style for all histograms.

        Arguments:
        style  Style for obj.Draw() call
        """
        for d in self.drawList:
            d.drawStyle = style

    def createCanvasFrameTwo(self, name):
        """Create TCanvas split in two and the TH1 frames on them."""
        if len(self.drawList) == 0:
            raise Exception("Empty set of histograms!")

        canvasFactor = 1.5
        divisionPoint = 1-1/canvasFactor

        # Create the canvas, divide it to two
        c = ROOT.TCanvas(name, name, ROOT.gStyle.GetCanvasDefW(), int(ROOT.gStyle.GetCanvasDefH()*canvasFactor))
        c.Divide(1, 2)
        
        # Set the lower point of the upper pad to divisionPoint
        pad1 = c.cd(1)
        (xlow, ylow, xup, yup) = [ROOT.Double(x) for x in [0.0]*4]
        pad1.GetPadPar(xlow, ylow, xup, yup)
        pad1.SetPad(xlow, divisionPoint, xup, yup)

        # Set the upper point of the lower pad to divisionPoint
        pad2 = c.cd(2)
        pad2.GetPadPar(xlow, ylow, xup, yup)
        pad2.SetPad(xlow, ylow, xup, divisionPoint+ROOT.gStyle.GetPadBottomMargin()-ROOT.gStyle.GetPadTopMargin()+0.005)

        c.cd(1)

        frame1 = pad1.DrawFrame(kwargs["xmin"], kwargs["ymin"], kwargs["xmax"], kwargs["ymax"])
        (labelSize, titleSize) = (frame1.GetXaxis().GetLabelSize(), frame1.GetXaxis().GetTitleSize())
        frame1.GetYaxis().SetTitle(self.drawList[0].histo.GetYaxis().GetTitle())

        c.cd(2)
        frame2 = pad2.DrawFrame(kwargs["xmin"], kwargs["ymin"], kwargs["xmax"], kwargs["ymax"])
        frame2.GetXaxis().SetTitle(self.drawList[0].histo.GetXaxis().GetTitle())
        frame2.GetYaxis().SetTitle("")
        for axis in [frame2.GetXaxis(), frame2.GetYaxis()]:
            axis.SetLabelSize(labelSize*canvasFactor)
            axis.SetTitleSize(titleSize*canvasFactor)

        return CanvasFrame(c, frame1, frame1=frame1, frame2=frame2, pad1=pad1, pad2=pad2)


    def addToLegend(self, legend):
        """Add histograms to a given TLegend."""
        for d in self.legendList:
            d.addToLegend(legend)

    def draw(self):
        """Draw histograms."""
        # Reverse the order of histograms so that the last histogram
        # is drawn first, i.e. on the bottom
        histos = self.drawList[:]
        histos.reverse()

        for h in histos:
            h.histo.Draw(h.drawStyle+" same")

    def stackHistograms(self, newName, nameList):
        """Stack histograms.

        Arguments:
        newName    Name of the histogram stack
        nameList   List of histogram names to stack
        """

        (selected, notSelected, firstIndex) = mergeStackHelper(self.drawList, nameList, "stack")
        if len(selected) == 0:
            return

        stacked = HistoDataStacked(selected, newName)
        notSelected.insert(firstIndex, stacked)
        self.drawList = notSelected

        self.legendList = filter(lambda x: x in notSelected, self.legendList)
        self.legendList.insert(firstIndex+1, stacked)

        self._populateMap()

    def addMcUncertainty(self, style, name="MC stat. unc."):
        mcHistos = filter(lambda x: x.isMC(), self.drawList)
        if len(mcHistos) == 0:
            print >> sys.stderr, "WARNING: Tried to create MC uncertainty histogram, but there are not MC histograms!"
            return

        hse = HistoStatError(mcHistos, name)
        hse.callHisto(style)

        firstMcIndex = len(self.drawList)
        for i, h in enumerate(self.drawList):
            if h.isMC():
                firstMcIndex = i
                break
        self.insert(firstMcIndex, hse, legendIndex=len(self.drawList))
        


class HistoManager:
    """Collection of histograms which are managed together.

    The histograms in a HistoManager are drawn to one plot.

    The implementation is divided to this and HistoManagerImpl class. The
    idea is that here are the methods, which don't require
    HistoData objects (namely setting the normalization), and
    HistoSetImpl has all the methods which require the HistoData
    objects. User can set freely the normalization scheme as many
    times as (s)he wants, and at the first time some method not
    implemented in HistoManager is called, the HistoData objects are
    created and the calls are delegated to HistoManagerImpl class.
    """
    def __init__(self, datasetMgr, name):
        """Constructor.

        Arguments:
        datasetMgr   DatasetManager object to take the histograms from
        name         Path to the TH1 objects in the DatasetManager ROOT files
        """
        self.datasetMgr = datasetMgr
        self.histoWrappers = datasetMgr.getHistoWrappers(name)
        self.data = None
        self.luminosity = None

    def __getattr__(self, name):
        """Delegate the calls which require the HistoData objects to the implementation class."""
        if self.data == None:
            self._createHistogramObjects()
        return getattr(self.data, name)

    def normalizeToOne(self):
        """Set the histogram normalization 'to one'.

        All histograms are normalized to unit area.
        """
        if self.data != None:
            raise Exception("Can't normalize after the histograms have been created!")
        for h in self.histoWrappers:
            h.normalizeToOne()
        self.luminosity = None

    def normalizeMCByCrossSection(self):
        """Set the MC histogram normalization 'by cross section'.

        All histograms from MC datasets are normalized by their cross
        section.
        """
        if self.data != None:
            raise Exception("Can't normalize after the histograms have been created!")
        for h in self.histoWrappers:
            if h.getDataset().isMC():
                h.normalizeByCrossSection()
        self.luminosity = None

    def normalizeMCByLuminosity(self):
        """Set the MC histogram normalization 'by luminosity'.

        The set of histograms is required to contain one, and only one
        histogram from data dataset (if there are many data datasets,
        they should be merged first). All histograms from MC datasets
        are normalized to the integrated luminosity of the the data
        dataset.
        """
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
        """Set the MC histogram normalization 'to luminosity'.

        Arguments:
        lumi   Integrated luminosity (pb^-1)

        All histograms from MC datasets are normalized to the given
        integrated luminosity.
        """
        if self.data != None:
            raise Exception("Can't normalize after the histograms have been created!")
        for h in self.histoWrappers:
            if h.getDataset().isMC():
                h.normalizeToLuminosity(lumi)
        self.luminosity = lumi

    def getLuminosity(self):
        """Get the integrated luminosity to which the MC datasets have been normalized to."""
        if self.luminosity == None:
            raise Exception("No normalization by or to luminosity!")
        return self.luminosity

    def addLuminosityText(self, x=None, y=None): # Nones for the default values
        """Draw the text for the integrated luminosity."""
        addLuminosityText(x, y, self.getLuminosity(), "pb^{-1}")

    def getHistogramObjects(self):
        """Get the HistoData objects."""
        return [HistoData(h.getDataset(), h.getHistogram()) for h in self.histoWrappers]

    def _createHistogramObjects(self):
        """Create the HistoManagerImpl object.

        Intended only for internal use.
        """
        self.data = HistoManagerImpl(self.getHistogramObjects())

    def stackMCHistograms(self):
        """Stack all MC histograms to one named 'Stacked MC'."""
        self.stackHistograms("StackedMC", self.datasetMgr.getMCDatasetNames())
