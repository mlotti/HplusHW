## \package histograms
# Histogram utilities and classes
#
# The package contains classes and utilities for histogram management.

import os, sys
import glob
import array
import math

from optparse import OptionParser

import ROOT

import dataset

## Enumeration class for CMS text mode
class CMSMode:
    PRELIMINARY = 0
    PAPER = 1
    SIMULATION = 2

## Global variable to hold CMS text mode
cmsTextMode = CMSMode.PRELIMINARY
## Global dictionary to hold the CMS text labels
cmsText = {
    CMSMode.PRELIMINARY: "CMS Preliminary",
    CMSMode.PAPER: "CMS",
    CMSMode.SIMULATION : "CMS Simulation"
    }

## Default energy text
energyText = "7 TeV"

## Class to provide default positions of the various texts.
#
# The attributes which can be set are the x and y coordinates and the
# text size.
#
# \todo Set the text fonts to non-bold
class TextDefaults:
    def __init__(self):
        self._setDefaults("cmsPreliminary", x=0.62, y=0.96)
        self._setDefaults("energy", x=0.2, y=0.96)
        self._setDefaults("lumi", x=0.43, y=0.96)

    ## Modify the default values
    # 
    # \param name   Name of the property ('cmsPreliminary', 'energy', 'lumi')
    # \param kwargs Keyword arguments
    #
    # <b>Keyword arguments</b>
    # \li \a x     X coordinate
    # \li \a y     Y coordinate
    # \li \a size  Font size
    def _setDefaults(self, name, **kwargs):
        for x, value in kwargs.iteritems():
            setattr(self, name+"_"+x, value)
            
    ## Modify the default position of "CMS Preliminary" text
    #
    # \param kwargs  Keyword arguments (forwarded to _setDefaults())
    def setCmsPreliminaryDefaults(self, **kwargs):
        self._setDefaults("cmsPreliminary", **kwargs)

    ## Modify the default position of center-of-mass energy text
    #
    # \param kwargs  Keyword arguments (forwarded to _setDefaults())
    def setEnergyDefaults(self, **kwargs):
        self._setDefaults("energy", **kwargs)
        
    ## Modify the default position of integrated luminosity text
    #
    # \param kwargs  Keyword arguments (forwarded to _setDefaults())
    def setLuminosityDefaults(self, **kwargs):
        self._setDefaults("lumi", **kwargs)

    ## Get the (x, y) values for property
    #
    # \param name  Name of property
    # \param x     X coordinate, if None, use the default
    # \param y     Y coordinate, if None, use the default
    def getValues(self, name, x, y):
        if x == None:
            x = getattr(self, name+"_x")
        if y == None:
            y = getattr(self, name+"_y")
        return (x, y)

    ## Get the size for property
    #
    # \param name  Name of property
    #
    # \return The text size, taken from ROOT.gStyle if no value has been set
    def getSize(self, name):
        try:
            return getattr(self, name+"_size")
        except AttributeError:
            return ROOT.gStyle.GetTextSize()

## Provides default text positions and sizes
#
# In order to modify the global defaults, modify this object.
#
# Used by histograms.addCmsPreliminaryText(),
# histograms.addEnergyText(), histograms.addLuminosityText().
textDefaults = TextDefaults()

## Draw text to current TCanvas/TPad with TLaTeX
#
# \param x       X coordinate of the text (in NDC)
# \param y       Y coordinate of the text (in NDC)
# \param text    String to draw
# \param args    Other positional arguments (forwarded to histograms.PlotText.__init__())
# \param kwargs  Other keyword arguments (forwarded to histograms.PlotText.__init__())
def addText(x, y, text, *args, **kwargs):
    t = PlotText(x, y, text, *args, **kwargs)
    t.Draw()

## Class for drawing text to current TPad with TLaTeX
#
# Text can be added to plots in object-oriented way. Mainly intended
# to be used with plots.PlotBase.appendPlotObject etc.
class PlotText:
    ## Constructor
    #
    # \param x       X coordinate of the text (in NDC)
    # \param y       Y coordinate of the text (in NDC)
    # \param text    String to draw
    # \param size    Size of text (None for the default value, taken from gStyle)
    # \param bold    Should the text be bold?
    # \param color   Color of the text
    def __init__(self, x, y, text, size=None, bold=True, color=ROOT.kBlack):
        self.x = x
        self.y = y
        self.text = text

        self.l = ROOT.TLatex()
        self.l.SetNDC()
        if not bold:
            self.l.SetTextFont(self.l.GetTextFont()-20) # bold -> normal
        if size != None:
            self.l.SetTextSize(size)
        self.l.SetTextColor(color)

    ## Draw the text to the current TPad
    #
    # \param options   For interface compatibility, ignored
    #
    # Provides interface compatible with ROOT's drawable objects.
    def Draw(self, options=None):
        self.l.DrawLatex(self.x, self.y, self.text)        
        

## Draw the "CMS Preliminary" text to the current TPad
#
# \param x   X coordinate of the text (None for default value)
# \param y   Y coordinate of the text (None for default value)
def addCmsPreliminaryText(x=None, y=None, text=None):
    (x, y) = textDefaults.getValues("cmsPreliminary", x, y)
    if text == None:
        txt  = cmsText[cmsTextMode]
    else:
        txt = text
    addText(x, y, txt, textDefaults.getSize("cmsPreliminary"), bold=False)

## Draw the center-of-mass energy text to the current TPad
#
# \param x   X coordinate of the text (None for default value)
# \param y   Y coordinate of the text (None for default value)
# \param s   Center-of-mass energy text with the unit (None for the default value, dataset.energyText
def addEnergyText(x=None, y=None, s=None):
    (x, y) = textDefaults.getValues("energy", x, y)
    text = energyText
    if s != None:
        text = s
    addText(x, y, "#sqrt{s} = "+text, textDefaults.getSize("energy"), bold=False)

## Draw the integrated luminosity text to the current TPad
#
# \param x     X coordinate of the text (None for default value)
# \param y     Y coordinate of the text (None for default value)
# \param lumi  Value of the integrated luminosity in pb^-1
# \param unit  Unit of the integrated luminosity value (should be fb^-1)
def addLuminosityText(x, y, lumi, unit="fb^{-1}"):
    (x, y) = textDefaults.getValues("lumi", x, y)
    lumiInFb = lumi/1000.
    log = math.log10(lumiInFb)
    ndigis = int(log)
    format = "%.0f" # ndigis >= 1, 10 <= lumiInFb
    if ndigis == 0: 
        if log >= 0: # 1 <= lumiInFb < 10
            format = "%.1f"
        else: # 0.1 < lumiInFb < 1
            format = "%.2f"
    elif ndigis <= -1:
        format = ".%df" % (abs(ndigis)+1)
        format = "%"+format
    format += " %s"
    format = "L="+format    

    addText(x, y, format % (lumi/1000., unit), textDefaults.getSize("lumi"), bold=False)
#    l.DrawLatex(x, y, "#intL=%.0f %s" % (lumi, unit))
#    l.DrawLatex(x, y, "L=%.0f %s" % (lumi, unit))

## Class for generating legend creation functions with default positions.
#
# The intended usage is demonstrated in histograms.py below, i.e.
# \code
# createLegend = LegendCreator(x1, y1, x2, y2)
# createLegend.setDefaults(x1=0.4, y2=0.5)
# createLegend.moveDefaults(dx=0.2, dh=0.1)
# legend = createLegend()
# \endcode
#
# All coordinates are in NDC
class LegendCreator:
    ## Constructor
    #
    # \param x1          Default x1 (left x)
    # \param y1          Default y1 (lower y)
    # \param x2          Default x2 (right x)
    # \param y2          Default y2 (upper y)
    # \param textSize    Default text size
    # \param borderSize  Default border size
    # \param fillStyle   Default fill style
    # \param fillColor   Default fill color
    def __init__(self, x1=0.73, y1=0.62, x2=0.93, y2=0.92, textSize=0.03, borderSize=0, fillStyle=4000, fillColor=ROOT.kWhite):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.textSize = textSize
        self.borderSize = borderSize
        self.fillStyle = fillStyle
        self.fillColor = fillColor
        self._keys = ["x1", "y1", "x2", "y2"]

    ## Create a copy of the object
    def copy(self):
        return LegendCreator(self.x1, self.y1, self.x2, self.y2)

    ## Set new default positions
    #
    # \param kwargs   Keyword arguments
    #
    # <b>Keyword arguments</b>
    # \li \a x1          X1 coordinate
    # \li \a y1          Y1 coordinate
    # \li \a x2          X2 coordinate
    # \li \a y2          Y2 coordinate
    # \li \a textSize    Text size
    # \li \a borderSize  Border size
    # \li \a fillStyle   Fill style
    # \li \a fillColor   Fill color
    def setDefaults(self, **kwargs):
        for x, value in kwargs.iteritems():
            setattr(self, x, value)

    ## Move the default position/width/height
    #
    # \param dx  Movement in x (positive is to right)
    # \param dy  Movement in y (positive is to up)
    # \param dw  Increment of width (negative to decrease width)
    # \param dh  Increment of height (negative to decrease height)
    #
    # Typically one want's to only move the legend, but keep it with
    # the same size, or increase/decrease width/height for some plots
    # only from the default
    def moveDefaults(self, dx=0, dy=0, dw=0, dh=0):
        self.x1 += dx
        self.x2 += dx

        self.y1 += dy
        self.y2 += dy

        self.x2 += dw
        self.y1 -= dh # we want to move the lower edge, and negative dh should shrink the legend

    ## Create a new TLegend object (function call syntax)
    #
    # \param args    Positional arguments (must get 0 or 4, see below)
    # \param kwargs  Keyword arguments
    # 
    # <b>Arguments can be either</b>
    # \li Four numbers for the coordinates (\a x1, \a y1, \a x2, \a y2) as positional arguments
    # \li Keyword arguments (\a x1, \a y1, \a x2, \a y2)
    #
    # If all 4 coordinates are specified, they are used. In the
    # keyword argument case, the coordinates which are not given are
    # taken from the default values.
    def __call__(self, *args, **kwargs):
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
        legend.SetFillStyle(self.fillStyle)
        if self.fillStyle != 0:
            legend.SetFillColor(self.fillColor)
        legend.SetBorderSize(self.borderSize)
        if legend.GetTextFont() % 10 == 3:
            legend.SetTextFont(legend.GetTextFont()-1) # From x3 to x2
        legend.SetTextSize(self.textSize)
        #legend.SetMargin(0.1)
        return legend

    ## \var x1
    # X1 coordinate
    ## \var y1
    # Y1 coordinate
    ## \var x2
    # X2 coordinate
    ## \var y2
    # Y2 coordinate
    ## \var textSize
    # Text size
    ## \var borderSize
    # Border size
    ## \var fillStyle
    # Fill style
    ## \var fillColor
    # Fill color
    ## \var _keys
    # List of valid coordinate names for __call__() function


## Default legend creator object
createLegend = LegendCreator()

## Move TLegend
# 
# \param legend   TLegend object to modify
# \param dx  Movement in x (positive is to right)
# \param dy  Movement in y (positive is to up)
# \param dw  Increment of width (negative to decrease width)
# \param dh  Increment of height (negative to decrease height)
#
# \return Modified TLegend (which is the same object as given as input)
#
# Typically one want's to only move the legend, but keep it with
# the same size, or increase/decrease width/height for some plots
# only from the default
def moveLegend(legend, dx=0, dy=0, dw=0, dh=0):
    legend.SetX1(legend.GetX1() + dx)
    legend.SetX2(legend.GetX2() + dx)
    legend.SetY1(legend.GetY1() + dy)
    legend.SetY2(legend.GetY2() + dy)

    legend.SetX1(legend.GetX1() + dw)
    legend.SetY1(legend.GetY1() - dh) # negative dh should shrink the legend
    
    return legend
    

## Update the style of palette Z axis according to ROOT.gStyle.
#
# This function is needed because the style is not propageted to the Z
# axis automatically. It is recommended to call this every time
# something is drawn with an option "Z"
def updatePaletteStyle(histo):
    ROOT.gPad.Update()
    paletteAxis = histo.GetListOfFunctions().FindObject("palette")
    if paletteAxis == None:
        return
    paletteAxis.SetLabelColor(ROOT.gStyle.GetLabelColor())
    paletteAxis.SetLabelFont(ROOT.gStyle.GetLabelFont())
    paletteAxis.SetLabelOffset(ROOT.gStyle.GetLabelOffset())
    paletteAxis.SetLabelSize(ROOT.gStyle.GetLabelSize())

## Sum TH1 histograms
#
# \param rootHistos  List of TH1 objects
# \param postfix     Postfix for the sum histo name
def sumRootHistos(rootHistos, postfix="_sum"):
    h = rootHistos[0].Clone()
    h.SetDirectory(0)
    h.SetName(h.GetName()+"_sum")
    for a in rootHistos[1:]:
        h.Add(a)
    return h

## Helper function for lessThan/greaterThan argument handling
#
# \param kwargs  Keyword arguments
#
# <b>Keyword arguments</b>
# \li \a lessThan     True for lessThan, False for greaterThan
# \li \a greaterThan  False for lessThan, True for greaterThan
#
# \return True for lessThan, False for greaterThan
#
# Provides the ability to have 'lessThan=True' and 'greaterThan=True'
# keyword arguments, as I believe they enhance the readability of the
# function calls.
def isLessThan(**kwargs):
    if len(kwargs) != 1:
        raise Exception("Should give only either 'lessThan' or 'greaterThan' as a keyword argument")
    elif "lessThan" in kwargs:
        return kwargs["lessThan"]
    elif "greaterThan" in kwargs:
        return not kwargs["greaterThan"]
    else:
        raise Exception("Must give either 'lessThan' or 'greaterThan' as a keyword argument")

## Convert TH1 distribution to TH1 of number of passed events as a function of cut value
#
# \param hdist   TH1 distribution
# \param kwargs  Keyword arguments (forwarded to histograms.isLessThan)
def dist2pass(hdist, **kwargs):
    lessThan = isLessThan(**kwargs)

    # for less than
    integral = None
    if lessThan:
        integral = lambda h, bin: h.Integral(0, bin)
    else:    
        integral = lambda h, bin: h.Integral(bin, h.GetNbinsX()+1)
        
    # bin 0             underflow bin
    # bin 1             first bin
    # bin GetNbinsX()   last bin
    # bin GetNbinsX()+1 overflow bin

    # Here we assume that all the bins in hdist have equal widths. If
    # this doesn't hold, the output must be TGraph
    bw = hdist.GetBinWidth(1);
    for bin in xrange(2, hdist.GetNbinsX()+1):
        if abs(bw - hdist.GetBinWidth(bin))/bw > 0.01:
            raise Exception("Input histogram with variable bin width is not supported (yet). The bin width of bin1 was %f, and bin width of bin %d was %f" % (bw, bin, hdist.GetBinWidth(bin)))

    # Construct the low edges of the passed histogram. Set the low
    # edges such that the bin centers correspond to the edges of the
    # distribution histogram. This makes sense because the only
    # sensible cut points in the distribution histogram are the bin
    # edges, and if one draws the passed histogram with points, the
    # points are placed to bin centers.
    nbins = hdist.GetNbinsX()+1
    firstLowEdge = hdist.GetXaxis().GetBinLowEdge(1) - bw/2
    lastUpEdge = hdist.GetXaxis().GetBinUpEdge(hdist.GetNbinsX()) + bw/2
    name = "passed_"+hdist.GetName()
    hpass = ROOT.TH1F("cumulative_"+hdist.GetName(), "Cumulative "+hdist.GetTitle(),
                      nbins, firstLowEdge, lastUpEdge)

    if lessThan:
        passedCumulative = 0
        passedCumulativeErrSq = 0
        for bin in xrange(0, hdist.GetNbinsX()+2):
            passedCumulative += hdist.GetBinContent(bin)
            err = hdist.GetBinError(bin)
            passedCumulativeErrSq += err*err

            hpass.SetBinContent(bin+1, passedCumulative)
            hpass.SetBinError(bin+1, math.sqrt(passedCumulativeErrSq))
    else:
        passedCumulative = 0
        passedCumulativeErrSq = 0
        for bin in xrange(hdist.GetNbinsX()+1, -1, -1):
            passedCumulative += hdist.GetBinContent(bin)
            err = hdist.GetBinError(bin)
            passedCumulativeErrSq += err*err

            hpass.SetBinContent(bin, passedCumulative)
            hpass.SetBinError(bin, math.sqrt(passedCumulativeErrSq))

    return hpass

## Helper function for applying a function for each bin of TH1
#
# \param th1       TH1 object
# \param function  Function taking a number as an input, and returning a number
def th1ApplyBin(th1, function):
    for bin in xrange(0, th1.GetNbinsX()+2):
        th1.SetBinContent(bin, function(th1.GetBinContent(bin)))

## Convert TH1 distribution to TH1 of efficiency as a function of cut value
#
# \param hdist  TH1 distribution
# \param kwargs  Keyword arguments (forwarded to histograms.isLessThan)
def dist2eff(hdist, **kwargs):
    hpass = dist2pass(hdist, **kwargs)
    total = hdist.Integral(0, hdist.GetNbinsX()+1)
    th1ApplyBin(hpass, lambda value: value/total)
    return hpass

## Convert TH1 distribution to TH1 of 1-efficiency as a function of cut value
#
# \param hdist  TH1 distribution
# \param kwargs  Keyword arguments (forwarded to histograms.isLessThan)
def dist2rej(hdist, **kwargs):
    hpass = dist2pass(hdist, **kwargs)
    total = hdist.Integral(0, hdist.GetNbinsX()+1)
    th1ApplyBin(hpass, lambda value: 1-value/total)
    return hpass


## Infer the frame bounds from the histograms and keyword arguments
#
# \param histos  List of histograms.Histo objects
# \param kwargs  Dictionary of keyword arguments to parse
#
# <b>Keyword arguments</b>
# \li\a ymin     Minimum value of Y axis
# \li\a ymax     Maximum value of Y axis
# \li\a xmin     Minimum value of X axis
# \li\a xmax     Maximum value of X axis
# \li\a ymaxfactor  Maximum value of Y is \a ymax*\a ymaxfactor (default 1.1)
# \li\a yminfactor  Minimum value of Y is \a ymax*\a yminfactor (yes, calculated from \a ymax )
#
# By default \a ymin, \a ymax, \a xmin and \a xmax are taken as
# the maximum/minimums of the histogram objects such that frame
# contains all histograms. The \a ymax is then multiplied with \a
# ymaxfactor
#
# The \a yminfactor/\a ymaxfactor are used only if \a ymin/\a ymax
# is taken from the histograms, i.e. \a ymax keyword argument is
# \b not given.
#
# Used e.g. in histograms.CanvasFrame and histograms.CanvasFrameTwo
def _boundsArgs(histos, kwargs):
    ymaxfactor = kwargs.get("ymaxfactor", 1.1)

    if not "ymax" in kwargs:
        kwargs["ymax"] = ymaxfactor * max([h.getYmax() for h in histos])
    if not "ymin" in kwargs:
        if "yminfactor" in kwargs:
            kwargs["ymin"] = kwargs["yminfactor"]*kwargs["ymax"]
        else:
            kwargs["ymin"] = min([h.getYmin() for h in histos])

    if not "xmin" in kwargs:
        kwargs["xmin"] = min([h.getXmin() for h in histos])
    if not "xmax" in kwargs:
        kwargs["xmax"] = max([h.getXmax() for h in histos])

## Draw a frame
#
# \param pad   TPad to draw the frame to
# \param xmin  Minimum X axis value
# \param ymin  Minimum Y axis value
# \param xmax  Maximum X axis value
# \param ymax  Maximum Y axis value
# \param nbins Number of x axis bins
#
# If nbins is None, TPad.DrawFrame is used. Otherwise a custom TH1 is
# created for the frame with nbins bins in x axis.
#
# Use case: selection flow histogram (or whatever having custom x axis
# lables).
def _drawFrame(pad, xmin, ymin, xmax, ymax, nbins=None):
    if nbins == None:
        return pad.DrawFrame(xmin, ymin, xmax, ymax)
    else:
        pad.cd()
        # From TPad.cc
        frame = pad.FindObject("hframe")
        if frame != None:
            frame.Delete()
            frame = None
        frame = ROOT.TH1F("hframe", "hframe", nbins, xmin, xmax)
        frame.SetBit(ROOT.TH1.kNoStats)
        frame.SetBit(ROOT.kCanDelete)
        frame.SetMinimum(ymin)
        frame.SetMaximum(ymax)
        frame.GetYaxis().SetLimits(ymin, ymax)
        frame.SetDirectory(0)
        frame.Draw(" ")
        return frame

## Create TCanvas and frame for one TPad.
#
# Used mainly from plots.PlotBase (based) class(es), although it can
# be also used directly if one really wants.
class CanvasFrame:
    ## Create TCanvas and TH1 for the frame.
    #
    # \param histoManager  histograms.HistoManager object to take the histograms for automatic axis ranges
    # \param name          Name for TCanvas (will be the file name, if TCanvas.SaveAs(".png") is used)
    # \param kwargs        Keyword arguments for frame bounds (forwarded to histograms._boundsArgs())
    #
    # <b>Keyword arguments</b>
    # \li\a opts   If given, give \a opts to histograms._boundsArgs() instead of kwargs. No other keyword arguments are allowed (except opts2, see below).
    # \li\a opts2  Ignored, existence allowed only for compatibility with histograms.CanvasFrameTwo
    def __init__(self, histoManager, name, **kwargs):
        histos = []
        if isinstance(histoManager, list):
            histos = histoManager[:]
        else:
            histos = histoManager.getHistos()
        if len(histos) == 0:
            raise Exception("Empty set of histograms!")

        self.canvas = ROOT.TCanvas(name)
        self.pad = self.canvas.GetPad(0)

        opts = kwargs
        if "opts" in kwargs:
            tmp = {}
            tmp.update(kwargs)
            if "opts2" in tmp:
                del tmp["opts2"]
            if len(tmp) != 1:
                raise Exception("If giving 'opts' as keyword argument, no other keyword arguments can be given (except opts2, which is ignored)")
            opts = kwargs["opts"]
        tmp = opts
        opts = {}
        opts.update(tmp)

        if "yfactor" in opts:
            if "ymaxfactor" in opts:
                raise Exception("Only one of ymaxfactor, yfactor can be given")
            opts["ymaxfactor"] = opts["yfactor"]

        _boundsArgs(histos, opts)

        self.frame = _drawFrame(self.canvas, opts["xmin"], opts["ymin"], opts["xmax"], opts["ymax"], opts.get("nbins", None))
        self.frame.GetXaxis().SetTitle(histos[0].getRootHisto().GetXaxis().GetTitle())
        self.frame.GetYaxis().SetTitle(histos[0].getRootHisto().GetYaxis().GetTitle())

    ## \var canvas
    # TCanvas for the canvas
    ## \var frame
    # TH1 for the frame
    ## \var pad
    # TPad of the plot

## Create TCanvas and frames for two TPads.
class CanvasFrameTwo:
    ## Create TCanvas and TH1 for the frame.
    #
    # \param histoManager1 HistoManager object to take the histograms for automatic axis ranges for upper pad
    # \param histos2       List of Histo objects to take the histograms for automatic axis ranges for lower pad
    # \param name          Name for TCanvas (will be the file name, if TCanvas.SaveAs(".png") is used)
    # \param kwargs        Keyword arguments (see below)
    #
    # <b>Keyword arguments</b>
    # \li\a opts   Dictionary for frame bounds (forwarded to histograms._boundsArgs())
    # \li\a opts1  Same as \a opts (can not coexist with \a opts, only either one can be given)
    # \li\a opts2  Dictionary for ratio pad bounds (forwarded to histograms._boundsArgs()) Only Y axis values are allowed, for X axis values are taken from \a opts/\a opts1
    def __init__(self, histoManager1, histos2, name, **kwargs):
        ## Wrapper to provide the CanvasFrameTwo.frame member.
        #
        # The GetXaxis() is forwarded to the frame of the lower pad,
        # and the GetYaxis() is forwared to the frame of the upper pad.
        class FrameWrapper:
            def __init__(self, frame1, frame2):
                self.frame1 = frame1
                self.frame2 = frame2

            def GetXaxis(self):
                return self.frame2.GetXaxis()

            def GetYaxis(self):
                return self.frame1.GetYaxis()


            def getXmin(self):
                return self.frame2.GetXaxis().GetBinLowEdge(self.frame2.GetXaxis().GetFirst())

            def getXmax(self):
                return self.frame2.GetXaxis().GetBinUpEdge(self.frame2.GetXaxis().GetLast())

        ## Wrapper to provide the getXmin/getXmax functions for _boundsArgs function.
        class HistoWrapper:
            def __init__(self, histo):
                self.histo = histo

            def getRootHisto(self):
                return self.histo

            def getXmin(self):
                return self.histo.GetXaxis().GetBinLowEdge(self.histo.GetXaxis().GetFirst())

            def getXmax(self):
                return self.histo.GetXaxis().GetBinUpEdge(self.histo.GetXaxis().GetLast())

            def getYmin(self):
                return self.histo.GetMinimum()

            def getYmax(self):
                return self.histo.GetMaximum()

        histos1 = []
        if isinstance(histoManager1, list):
            histos1 = histoManager1[:]
        else:
            histos1 = histoManager1.getHistos()
        if len(histos1) == 0:
            raise Exception("Empty set of histograms for first pad!")
        if len(histos2) == 0:
            raise Exception("Empty set of histograms for second pad!")

        canvasFactor = kwargs.get("canvasFactor", 1.25)
        canvasHeightCorrection = kwargs.get("canvasHeightCorrection", 0.022)
        divisionPoint = 1-1/canvasFactor

        # Do it like this (create empty, update from kwargs) in order
        # to make a copy and NOT modify the dictionary in the caller
        opts1 = {}
        opts1.update(kwargs.get("opts", {}))
        if "opts1" in kwargs:
            if "opts" in kwargs:
                raise Exception("Can not give both 'opts' and 'opts1' as keyword arguments")
            opts1 = kwargs["opts1"]
        opts2 = {}
        opts2.update(kwargs.get("opts2", {}))

        if "xmin" in opts2 or "xmax" in opts2 or "nbins" in opts2:
            raise Exception("No 'xmin', 'xmax', or 'nbins' allowed in opts2, values are taken from opts/opts1")

        _boundsArgs(histos1, opts1)
        opts2["xmin"] = opts1["xmin"]
        opts2["xmax"] = opts1["xmax"]
        opts2["nbins"] = opts1.get("nbins", None)
        _boundsArgs([HistoWrapper(h) for h in histos2], opts2)

        # Create the canvas, divide it to two
        self.canvas = ROOT.TCanvas(name, name, ROOT.gStyle.GetCanvasDefW(), int(ROOT.gStyle.GetCanvasDefH()*canvasFactor))
        self.canvas.Divide(1, 2)
        
        # Set the lower point of the upper pad to divisionPoint
        self.pad1 = self.canvas.cd(1)
        (xlow, ylow, xup, yup) = [ROOT.Double(x) for x in [0.0]*4]
        self.pad1.GetPadPar(xlow, ylow, xup, yup)
        self.pad1.SetPad(xlow, divisionPoint, xup, yup)
        self.pad1.SetFillStyle(4000) # transparent

        # Set the upper point of the lower pad to divisionPoint
        self.pad2 = self.canvas.cd(2)
        self.pad2.GetPadPar(xlow, ylow, xup, yup)
        self.pad2.SetPad(xlow, ylow, xup,
                         divisionPoint+ROOT.gStyle.GetPadBottomMargin()-ROOT.gStyle.GetPadTopMargin()+canvasHeightCorrection)
        self.pad2.SetFillStyle(4000) # transparent
        self.pad2.SetTopMargin(0.0)
        #self.pad2.SetBottomMargin(self.pad2.GetBottomMargin()+0.06)
        self.pad2.SetBottomMargin(self.pad2.GetBottomMargin()+0.16)

        self.canvas.cd(1)

        yoffsetFactor = canvasFactor*1.15
        #xoffsetFactor = canvasFactor*1.6
        #xoffsetFactor = canvasFactor*2
        xoffsetFactor = 0.5*canvasFactor/(canvasFactor-1) * 1.3


        self.frame1 = _drawFrame(self.pad1, opts1["xmin"], opts1["ymin"], opts1["xmax"], opts1["ymax"], opts1.get("nbins", None))
        (labelSize, titleSize) = (self.frame1.GetXaxis().GetLabelSize(), self.frame1.GetXaxis().GetTitleSize())
        self.frame1.GetXaxis().SetLabelSize(0)
        self.frame1.GetXaxis().SetTitleSize(0)
        self.frame1.GetYaxis().SetTitle(histos1[0].getRootHisto().GetYaxis().GetTitle())
        self.frame1.GetYaxis().SetTitleOffset(self.frame1.GetYaxis().GetTitleOffset()*yoffsetFactor)

        self.canvas.cd(2)
        self.frame2 = _drawFrame(self.pad2, opts2["xmin"], opts2["ymin"], opts2["xmax"], opts2["ymax"], opts2.get("nbins", None))
        self.frame2.GetXaxis().SetTitle(histos1[0].getRootHisto().GetXaxis().GetTitle())
        self.frame2.GetYaxis().SetTitle(histos2[0].getRootHisto().GetYaxis().GetTitle())
        self.frame2.GetYaxis().SetTitleOffset(self.frame2.GetYaxis().GetTitleOffset()*yoffsetFactor)
        self.frame2.GetXaxis().SetTitleOffset(self.frame2.GetXaxis().GetTitleOffset()*xoffsetFactor)
        self.frame2.GetYaxis().SetLabelSize(int(self.frame2.GetYaxis().GetLabelSize()*0.8))

        self.canvas.cd(1)
        self.frame = FrameWrapper(self.frame1, self.frame2)
        self.pad = self.pad1

    ## \var frame1
    # TH1 for the upper frame
    ## \var frame2
    # TH2 for the lower frame
    ## \var canvas
    # TCanvas for the canvas
    ## \var pad
    # TPad for the upper pad
    ## \var pad1
    # TPad for the upper pad
    ## \var pad2
    # TPad for the lower pad
    ## \var frame
    # Wrapper for the two frames
    #
    # The y axis of the wrapper is taken from the upper frame, and the
    # xa xis from the lower frame.

## Base class for all Histo classes.
#
# Histo classes are wrappers for ROOT TH1/TH2/TGraph objects,
# providing one layer of customisation options between the end user
# and ROOT. The classes contain all necessary information to draw the
# histograms without the need for drawing code to know anything about
# the objects to be drawn (i.e. in addition of TH1, these contain the
# draw and legend styles).
class Histo:
    ## Constructor
    #
    # \todo test draw style "9"
    #
    # \param rootHisto    ROOT histogram object (TH1)
    # \param name         Name of the histogram
    # \param legendStyle  Style string for TLegend (third parameter for TLegend.AddEntry())
    # \param drawStyle    Style string for Draw (string parameter for TH1.Draw())
    def __init__(self, rootHisto, name, legendStyle="l", drawStyle="HIST"):
        self.rootHisto = rootHisto
        self.name = name
        self.legendLabel = name
        self.legendStyle = legendStyle
        self.drawStyle = drawStyle

    ## Get the ROOT histogram object (TH1)
    def getRootHisto(self):
        return self.rootHisto

    ## Get the histogram name
    def getName(self):
        return self.name

    ## Set the histogram name
    #
    # \param name  New histogram name
    def setName(self, name):
        self.name = name

    ## Allow the Data/MC status of the Histo to be changed
    #
    # \param isData   True for data, false for MC
    # \param isMC     True for MC, false for data
    #
    # Some plotting defaults depend on whether histograms are data or
    # MC. This provides an ability to circumvent those.
    def setIsDataMC(self, isData, isMC):
        self._isData = isData
        self._isMC = isMC

    ## Is the histogram from MC?
    def isMC(self):
        if not hasattr(self, "_isMC"):
            raise Exception("setIsDataMC() has not been called, don't know if the histogram is from data or MC")
        return self._isMC

    ## Is the histogram from collision data?
    def isData(self):
        if not hasattr(self, "_isData"):
            raise Exception("setIsDataMC() has not been called, don't know if the histogram is from data or MC")
        return self._isData

    ## Set the histogram draw style
    #
    # \param drawStyle  new draw style
    def setDrawStyle(self, drawStyle):
        self.drawStyle = drawStyle

    ## Set the legend label
    #
    # If the legend label is set to None, this Histo is not added to
    # TLegend in addToLegend()
    #
    # \param label  New histogram label for TLegend
    def setLegendLabel(self, label):
        self.legendLabel = label

    ## Set the legend style
    #
    # \param style  New histogram style for TLegend
    def setLegendStyle(self, style):
        self.legendStyle = style

    ## Add the histogram to a TLegend
    #
    # If the legend label is None, do not add this Histo to TLegend
    #
    # \param legend   TLegend object
    def addToLegend(self, legend):
        if self.legendLabel == None:
            return

        # Hack to get the black border to the legend, only if the legend style is fill
        if "f" == self.legendStyle.lower():
            h = self.rootHisto.Clone(self.rootHisto.GetName()+"_forLegend")
            if hasattr(h, "SetDirectory"):
                h.SetDirectory(0)
            h.SetLineWidth(1)
            if self.rootHisto.GetLineColor() == self.rootHisto.GetFillColor():
                h.SetLineColor(ROOT.kBlack)

            legend.AddEntry(h, self.legendLabel, self.legendStyle)
            self.rootHistoForLegend = h # keep the reference in order to avoid segfault
        else:
            labels = self.legendLabel.split("\n")
            legend.AddEntry(self.rootHisto, labels[0], self.legendStyle)
            for lab in labels[1:]:
                legend.AddEntry(None, lab, "")

    ## Call a function with self as an argument.
    #
    # \param func  Function with one parameter
    #
    # \todo This resembles the Visitor pattern, perhaps this should be
    # renamed to visit()?
    def call(self, func):
        func(self)

    ## Draw the histogram
    #
    # \param opt  Drawing options (in addition to the draw style)
    def draw(self, opt):
        self.rootHisto.Draw(self.drawStyle+" "+opt)

    ## Get the minimum value of the X axis
    def getXmin(self):
        return self.rootHisto.GetXaxis().GetBinLowEdge(self.rootHisto.GetXaxis().GetFirst())

    ## Get the maximum value of the X axis
    def getXmax(self):
        return self.rootHisto.GetXaxis().GetBinUpEdge(self.rootHisto.GetXaxis().GetLast())

    ## Get the minimum value of the Y axis
    def getYmin(self):
        return self.rootHisto.GetMinimum()

    ## Get the maximum value of the Y axis
    def getYmax(self):
        return self.rootHisto.GetMaximum()

    ## Get the width of a bin
    #
    # \param bin  Bin number
    def getBinWidth(self, bin):
        return self.rootHisto.GetBinWidth(bin)

    ## \var rootHisto
    # ROOT histogram object (TH1)
    ## \var name
    # Histogram name
    ## \var legendLabel
    # Label for TLegend
    ## \var legendStyle
    # Style string for TLegend
    ## \var drawStyle
    # Style string for Draw()
    ## \var _isData
    # Is the histogram from data?
    ## \var _isMC
    # Is the histogram from MC?

## Represents one (TH1/TH2) histogram associated with a dataset.Dataset object
class HistoWithDataset(Histo):
    ## Constructor
    #
    # \param dataset    dataset.Dataset object
    # \param rootHisto  TH1 object
    # \param name       Name of the Histo
    #
    #    The default legend label is the dataset name
    def __init__(self, dataset, rootHisto, name):
        Histo.__init__(self, rootHisto, name)
        self.dataset = dataset
        self.setIsDataMC(self.dataset.isData(), self.dataset.isMC())

    ## Get the dataset.Dataset object
    def getDataset(self):
        return self.dataset

    ## \var dataset
    # The histogram is from this dataset.Dataset object

class HistoWithDatasetFakeMC(HistoWithDataset):
    def __init__(self, dataset, rootHisto, name):
        HistoWithDataset.__init__(self, dataset, rootHisto, name)
        self.setIsDataMC(False, True)

## Represents combined (statistical) uncertainties of multiple histograms.
class HistoTotalUncertainty(Histo):
    ## Constructor
    #
    # \param histos  List of histograms.Histo objects
    # \param name    Name of the uncertainty histogram
    def __init__(self, histos, name):
        rootHistos = []
        for h in histos:
            if hasattr(h, "getSumRootHisto"):
                rootHistos.append(h.getSumRootHisto())
            else:
                rootHistos.append(h.getRootHisto())

        tmp = rootHistos[0].Clone()
        tmp.SetDirectory(0)
        Histo.__init__(self, tmp, name, "F", "E2")
        self.rootHisto.SetName(self.rootHisto.GetName()+"_errors")
        self.histos = histos

        for h in rootHistos[1:]:
            self.rootHisto.Add(h)
        self.setIsDataMC(self.histos[0].isData(), self.histos[0].isMC())

    ## \var histos
    # List of histograms.Histo objects from which the total uncertaincy is calculated

## Represents stacked TH1 histograms
#
# Stacking is done with the help of THStack object
class HistoStacked(Histo):
    ## Constructor.
    #
    # \param histos  List of Histo objects to stack
    # \param name    Name of the stacked histogram
    def __init__(self, histos, name):
        Histo.__init__(self, ROOT.THStack(name+"stackHist", name+"stackHist"), name, None, "HIST")
        self.histos = histos

        rootHistos = [d.getRootHisto() for d in self.histos]
        rootHistos.reverse()
        for h in rootHistos:
            self.rootHisto.Add(h)

        self.setIsDataMC(self.histos[0].isData(), self.histos[0].isMC())

    ## Get the list of original TH1 histograms.
    def getAllRootHistos(self):
        return [x.getRootHisto() for x in self.histos]

    ## Get the sum of the original histograms.
    def getSumRootHisto(self):
        return sumRootHistos([d.getRootHisto() for d in self.histos])

    def setLegendLabel(self, label):
        for h in self.histos:
            h.setLegendLabel(label)

    def setLegendStyle(self, style):
        for h in self.histos:
            h.setLegendStyle(style)

    def addToLegend(self, legend):
        for h in self.histos:
            h.addToLegend(legend)

    ## Call a function for each Histo in the stack.
    #
    # \param function  Function with one parameter
    #
    # \todo This resembles the Visitor pattern, perhaps this should be
    # renamed to visit()?
    def call(self, function):
        for h in self.histos:
            h.call(function)

    def getXmin(self):
        return min([h.getXmin() for h in self.histos])

    def getXmax(self):
        return max([h.getXmax() for h in self.histos])

    def getBinWidth(self, bin):
        return self.histos[0].getBinWidth(bin)

    ## \var histos
    # List of histograms.Histo objects which are stacked

## Represents TGraph objects
class HistoGraph(Histo):
    ## Constructor
    #
    # \param  rootGraph   TGraph object
    # \param name         Name of the histogram
    # \param legendStyle  Style string for TLegend (third parameter for TLegend.AddEntry())
    # \param drawStyle    Style string for Draw (string parameter for TH1.Draw())
    def __init__(self, rootGraph, name, legendStyle="l", drawStyle="L"):
        Histo.__init__(self, rootGraph, name, legendStyle, drawStyle)

    def getRootGraph(self):
        return self.getRootHisto()

    def _values(self, values, func):
        return [func(values[i], i) for i in xrange(0, self.getRootGraph().GetN())]

    def getXmin(self):
        if isinstance(self.getRootGraph(), ROOT.TGraph):
            # TGraph.GetError[XY]{low,high} return -1 ...
            function = lambda val, i: val
        else:
            function = lambda val, i: val-self.getRootGraph().GetErrorXlow(i)
        return min(self._values(self.getRootGraph().GetX(), function))

    def getXmax(self):
        if isinstance(self.getRootGraph(), ROOT.TGraph):
            # TGraph.GetError[XY]{low,high} return -1 ...
            function = lambda val, i: val
        else:
            function = lambda val, i: val+self.getRootGraph().GetErrorXhigh(i)
        return max(self._values(self.getRootGraph().GetX(), function))

    def getYmin(self):
        if isinstance(self.getRootGraph(), ROOT.TGraph):
            # TGraph.GetError[XY]{low,high} return -1 ...
            function = lambda val, i: val
        else:
            function = lambda val, i: val-self.getRootGraph().GetErrorYlow(i)
        return min(self._values(self.getRootGraph().GetY(), function))

    def getYmax(self):
        if isinstance(self.getRootGraph(), ROOT.TGraph):
            # TGraph.GetError[XY]{low,high} return -1 ...
            function = lambda val, i: val
        else:
            function = lambda val, i: val+self.getRootGraph().GetErrorYhigh(i)
        return max(self._values(self.getRootGraph().GetY(), function))

    def getBinWidth(self, bin):
        raise Exception("getBinWidth() is meaningless for HistoGraph (name %s)" % self.getName())

## Represents TGraph objects with associated dataset.Dataset object
class HistoGraphWithDataset(HistoGraph):
    ## Constructor
    #
    # \param dataset  dataset.Dataset object
    # \param args     Positional arguments (forwarded to histograms.HistoGraph.__init__())
    # \param kwargs   Keyword arguments (forwarded to histograms.HistoGraph.__init__())
    def __init__(self, dataset, *args, **kwargs):
        HistoGraph.__init__(self, *args, **kwargs)
        self.dataset = dataset
        self.setIsDataMC(self.dataset.isData(), self.dataset.isMC())

    def getDataset(self):
        return self.dataset

## Implementation of HistoManager.
#
# Intended to be used only from histograms.HistoManager. This class contains all
# the methods which require the Histo objects (and only them).
#
# Contains two lists for histograms, one for the drawing order, and
# other for the legend insertion order. By default, the histogram
# which is first in the legend, is drawn last such that it is in the
# top of all drawn histograms. Both lists can be reordered if user
# wants.
class HistoManagerImpl:
    ## Constructor.
    #
    # \param histos    List of histograms.Histo objects
    def __init__(self, histos=[]):

        # List for the Draw() order, keep it reversed in order to draw
        # the last histogram in the list first. i.e. to the bottom
        self.drawList = histos[:]

        # List for the legend order, first histogram is also first in
        # the legend
        self.legendList = histos[:]

        # Dictionary for accessing the histograms by name
        self._populateMap()

    ## Get the number of managed histograms.Histo objects
    def __len__(self):
        return len(self.drawList)

    ## Populate the name -> histograms.Histo map
    def _populateMap(self):
        self.nameHistoMap = {}
        for h in self.drawList:
            self.nameHistoMap[h.getName()] = h

    ## Append a histograms.Histo object.
    #
    # \param histo   histograms.Histo object to be added
    def appendHisto(self, histo):
        self.drawList.append(histo)
        self.legendList.append(histo)
        self._populateMap()

    ## Extend with a list of histograms.Histo objects.
    #
    # \param histos  List of histograms.Histo objects to be added
    def extendHistos(self, histos):
        self.drawList.extend(histos)
        self.legendList.extend(histos)
        self._populateMap()

    ## Insert histograms.Histo to position i.
    #
    # \param i      Index of the position to insert the histogram
    # \param histo  histograms.Histo object to insert
    # \param kwargs Keyword arguments
    # 
    # <b>Keyword arguments</b>
    # \li \a legendIndex  Index of the position to insert the histogram in
    #                     the legend list (default is the same as i). Can
    #                     be useful for e.g. separate uncertainty histogram.
    def insertHisto(self, i, histo, **kwargs):
        drawIndex = i
        legendIndex = i

        if "legendIndex" in kwargs:
            legendIndex = kwargs["legendIndex"]

        self.drawList.insert(drawIndex, histo)
        self.legendList.insert(legendIndex, histo)
        self._populateMap()

    ## Remove histograms.Histo object
    #
    # \param name  Name of the histograms.Histo object to be removed
    def removeHisto(self, name):
        del self.nameHistoMap[name]
        for i, h in enumerate(self.drawList):
            if h.getName() == name:
                del self.drawList[i]
                break
        for i, h in enumerate(self.legendList):
            if h.getName() == name:
                del self.legendList[i]
                break

    ## Replace histograms.Histo object
    #
    # \param name   Name of the histograms.Histo object to be replaced
    # \param histo  New histograms.Histo object
    def replaceHisto(self, name, histo):
        if not name in self.nameHistoMap:
            raise Exception("Histogram %s doesn't exist" % name)
        self.nameHistoMap[name] = histo
        for i, h in enumerate(self.drawList):
            if h.getName() == name:
                self.drawList[i] = histo
                break
        for i, h in enumerate(self.legendList):
            if h.getName() == name:
                self.legendList[i] = histo
                break

    ## Reorder the legend
    #
    # \param histoNames  List of histogram names
    #
    # The legend list is reordered as specified by histoNames.
    # Histograms not mentioned in histoNames are kept in the original
    # order at the end of the legend.
    def reorderLegend(self, histoNames):
        def index_(list_, name_):
            for i, o in enumerate(list_):
                if o.getName() == name_:
                    return i
            raise Exception("No such histogram %s" % name_)

        src = self.legendList[:]
        dst = []
        for name in histoNames:
            dst.append(src.pop(index_(src, name)))
        dst.extend(src)
        self.legendList = dst

    ## Reorder the draw list
    #
    # \param histoNames  List of histogram names
    #
    # The draw list is reordered as specified by histoNames.
    # Histograms not mentioned in histoNames are kept in the original
    # order at the end of the draw list.
    def reorderDraw(self, histoNames):
        def index_(list_, name_):
            for i, o in enumerate(list_):
                if o.getName() == name_:
                    return i
            raise Exception("No such histogram %s" % name_)

        src = self.drawList[:]
        dst = []
        for name in histoNames:
            dst.append(src.pop(index_(src, name)))
        dst.extend(src)
        self.drawList = dst

    ## Call a function for a named histograms.Histo object.
    #
    # \param name   Name of histogram
    # \param func   Function taking one parameter (histograms.Histo), return value is not used
    def forHisto(self, name, func):
        try:
            self.nameHistoMap[name].call(func)
        except KeyError:
            print >> sys.stderr, "WARNING: Tried to call a function for histogram '%s', which doesn't exist." % name

    ## Call each MC histograms.Histo with a function.
    #
    # \param func   Function taking one parameter (histograms.Histo), return value is not used
    def forEachMCHisto(self, func):
        def forMC(histo):
            if histo.isMC():
                func(histo)

        self.forEachHisto(forMC)

    ## Call each collision data histograms.Histo with a function.
    #
    # \param func  Function taking one parameter (Histo, return value is not used
    def forEachDataHisto(self, func):
        def forData(histo):
            if histo.isData():
                func(histo)
        self.forEachHisto(forData)

    ## Call each histograms.Histo with a function.
    #
    # \param func  Function taking one parameter (Histo), return value is not used
    def forEachHisto(self, func):
        for d in self.drawList:
            d.call(func)

    ## Check if a histograms.Histo with a given name exists
    #
    # \param name   Name of histograms.Histo to check
    def hasHisto(self, name):
        return name in self.nameHistoMap

    ## Get histograms.Histo of a given name
    #
    # \param name  Name of histograms.Histo to get
    def getHisto(self, name):
        return self.nameHistoMap[name]

    ## Get all histograms.Histo objects
    def getHistos(self):
        return self.drawList[:]

    ## Set legend names for given histograms.
    #
    # \param nameMap   Dictionary with name->label mappings
    def setHistoLegendLabelMany(self, nameMap):
        for name, label in nameMap.iteritems():
            try:
                self.nameHistoMap[name].setLegendLabel(label)
            except KeyError:
                print >> sys.stderr, "WARNING: Tried to set legend label for histogram '%s', which doesn't exist." % name

    ## Set the legend style for a given histogram.
    #
    # \param name   Name of the histogram
    # \param style  Style for the legend (given to TLegend as 3rd argument)
    def setHistoLegendStyle(self, name, style):
        try:
            self.nameHistoMap[name].setLegendStyle(style)
        except KeyError:
            print >> sys.stderr, "WARNING: Tried to set legend style for histogram '%s', which doesn't exist." % name

    ## Set the legend style for all histograms.
    #
    # \param style  Style for the legend (given to TLegend as 3rd argument)
    def setHistoLegendStyleAll(self, style):
        for d in self.legendList:
            d.setLegendStyle(style)

    ## Set histogram drawing style for a given histogram.
    #
    # \param name   Name of the histogram
    # \param style  Style for obj.Draw() call
    def setHistoDrawStyle(self, name, style):
        try:
            self.nameHistoMap[name].setDrawStyle(style)
        except KeyError:
            print >> sys.stderr, "WARNING: Tried to set draw style for histogram '%s', which doesn't exist." % name

    ## Set the histogram drawing style for all histograms.
    #
    # \param style  Style for obj.Draw() call
    def setHistoDrawStyleAll(self, style):
        for d in self.drawList:
            d.setDrawStyle(style)

    ## Add histograms to a given TLegend.
    #
    # \param legend  TLegend object
    def addToLegend(self, legend):
        for d in self.legendList:
            d.addToLegend(legend)

    ## Draw histograms.
    def draw(self):
        # Reverse the order of histograms so that the last histogram
        # is drawn first, i.e. on the bottom
        histos = self.drawList[:]
        histos.reverse()

        for h in histos:
            h.draw("same")

    ## Stack histograms.
    #
    # \param newName   Name of the histogram stack
    # \param nameList  List of histogram names to stack
    def stackHistograms(self, newName, nameList):
        (selected, notSelected, firstIndex) = dataset._mergeStackHelper(self.drawList, nameList, "stack")
        if len(selected) == 0:
            return

        stacked = HistoStacked(selected, newName)
        notSelected.insert(firstIndex, stacked)
        self.drawList = notSelected

        self.legendList = filter(lambda x: x in notSelected, self.legendList)
        self.legendList.insert(firstIndex+1, stacked)

        self._populateMap()

    ## Add MC uncertainty band histogram
    #
    # \param style        Style function for the uncertainty histogram
    # \param name         Name of the unceratinty histogram
    # \param legendLabel  Legend label for the uncertainty histogram
    # \param nameList     List of histogram names to include to the uncertainty band (\a None corresponds all MC)
    def addMCUncertainty(self, style, name="MCuncertainty", legendLabel="MC stat. unc.", nameList=None):
        mcHistos = filter(lambda x: x.isMC(), self.drawList)
        if len(mcHistos) == 0:
            print >> sys.stderr, "WARNING: Tried to create MC uncertainty histogram, but there are not MC histograms!"
            return

        if nameList != None:
            mcHistos = filter(lambda x: x.getName() in nameList, mcHistos)
        if len(mcHistos) == 0:
            print >>sys.stderr, "WARNING: No MC histograms to use for uncertainty band"
            return

        hse = HistoTotalUncertainty(mcHistos, name)
        hse.setLegendLabel(legendLabel)
        hse.call(style)

        firstMcIndex = len(self.drawList)
        for i, h in enumerate(self.drawList):
            if h.isMC():
                firstMcIndex = i
                break
        self.insertHisto(firstMcIndex, hse, legendIndex=len(self.drawList))
        
    ## \var drawList
    # List of histograms.Histo objects for drawing
    # The histograms are drawn in the <i>reverse</i> order, i.e. the
    # first histogram is on the top, anbd the last histogram is on the
    # bottom.
    #
    ## \var legendList
    # List of histograms.Histo objects for TLegend
    # The histograms are added to the TLegend in the order they are in
    # the list.
    #
    ## \var nameHistoMap
    # Dictionary from histograms.Histo names to the objects


## Collection of histograms which are managed together.
#
# The histograms in a HistoManager are drawn to one plot.

# The implementation is divided to this and
# histograms.HistoManagerImpl class. The idea is that here are the
# methods, which don't require Histo objects (namely setting the
# normalization), and histograms.HistoManagerImpl has all the methods
# which require the histograms.Histo objects. User can set freely the
# normalization scheme as many times as (s)he wants, and at the first
# time some method not implemented in HistoManagerBase is called, the
# Histo objects are created and the calls are delegated to
# HistoManagerImpl class.
class HistoManager:
    ## Constructor.
    #
    # \param args   Positional arguments
    # \param kwargs Keyword arguments
    #
    # <b>Positional arguments</b>
    # \li \a datasetMgr   DatasetManager object to take the histograms from
    # \li \a name         Path to the TH1 objects in the DatasetManager ROOT files
    #
    # <b>Keyword arguments</b>
    # \li \a datasetRootHistos   Initial list of DatasetRootHisto objects
    #
    # Only either both positional arguments or the keyword argument
    # can be given.
    #
    # \todo The interface should be fixed to have only the keyword
    #       argument (also as the only positional argument). This is
    #       not done yet for backward compatibility.
    def __init__(self, *args, **kwargs):
        if len(args) == 0:
            if len(kwargs) == 0:
                self.datasetRootHistos = []
            elif len(kwargs) == 1:
                self.datasetRootHistos = kwargs["datasetRootHistos"]
            else:
                raise Exception("If positional arguments are not given, there must be ither 0 or 1 keyword argument (got %d)"%len(kwargs))
        else:
            if len(args) != 2:
                raise Exception("Must give exactly 2 positional arguments (got %d)" % len(args))
            if len(kwargs) != 0:
                raise Exception("If positional arguments are given, there must not be any keyword arguments")
            datasetMgr = args[0]
            name = args[1]

            self.datasetRootHistos = datasetMgr.getDatasetRootHistos(name)

        self.impl = None
        self.luminosity = None

    ## Delegate the calls which require the histograms.Histo objects to the implementation class.
    #
    # \param name  Name of the attribute to get
    def __getattr__(self, name):
        if self.impl == None:
            self._createImplementation()
        return getattr(self.impl, name)

    ## Append dataset.DatasetRootHistoBase object
    #
    # \param datasetRootHisto  dataset.DatasetRootHistoBase object
    def append(self, datasetRootHisto):
        if self.impl != None:
            raise Exception("Can't append after the histograms have been created!")
        if not isinstance(datasetRootHisto, dataset.DatasetRootHistoBase):
            raise Exception("Can append only DatasetRootHistoBase derived objects, got %s" % str(datasetRootHisto))
        self.datasetRootHistos.append(datasetRootHisto)

    ## Extend with another HistoManager or a list of dataset.DatasetRootHistoBase objects
    #
    # \param datasetRootHistos  HistoManager object, or a list of dataset.DatasetRootHistoBase objects
    def extend(self, datasetRootHistos):
        if self.impl != None:
            raise Exception("Can't extend after the histograms have been created!")
        if isinstance(datasetRootHistos, HistoManager):
            if datasetRootHistos.impl != None:
                raise Exception("Can't extend from HistoManagerBase whose histograms have been created!")
            datasetRootHistos = HistoManagerBase.datasetRootHistos
        for d in datasetRootHistos:
            if not isinstance(datasetRootHisto, dataset.DatasetRootHistoBase):
                raise Exception("Can extend only DatasetRootHistoBase derived objects, got %s" % str(d))
        self.datasetRootHistos.extend(datasetRootHistos)

    ## Set the histogram normalization scheme to <i>to one</i>.
    #
    # All histograms are normalized to unit area.
    def normalizeToOne(self):
        if self.impl != None:
            raise Exception("Can't normalize after the histograms have been created!")
        for h in self.datasetRootHistos:
            h.normalizeToOne()
        self.luminosity = None

    ## Set the MC histogram normalization scheme to <i>by cross section</i>.
    #
    # All histograms from MC datasets are normalized by their cross
    # section.
    def normalizeMCByCrossSection(self):
        if self.impl != None:
            raise Exception("Can't normalize after the histograms have been created!")
        for h in self.datasetRootHistos:
            if h.getDataset().isMC():
                h.normalizeByCrossSection()
        self.luminosity = None

    ## Set the MC histogram normalization <i>by luminosity</i>.
    #
    # The set of histograms is required to contain one, and only one
    # histogram from data dataset (if there are many data datasets,
    # they should be merged first). All histograms from MC datasets
    # are normalized to the integrated luminosity of the the data
    # dataset.
    def normalizeMCByLuminosity(self):
        if self.impl != None:
            raise Exception("Can't normalize after the histograms have been created!")
        lumi = None
        for h in self.datasetRootHistos:
            if h.getDataset().isData():
                if lumi != None:
                    raise Exception("Unable to normalize by luminosity, more than one data datasets (you might want to merge data datasets)")
                lumi = h.getDataset().getLuminosity()

        if lumi == None:
            raise Exception("Unable to normalize by luminosity, no data datasets")

        self.normalizeMCToLuminosity(lumi)

    ## Set the MC histogram normalization <i>to luminosity</i>.
    #
    # \param lumi   Integrated luminosity (pb^-1)
    #
    # All histograms from MC datasets are normalized to the given
    # integrated luminosity.
    def normalizeMCToLuminosity(self, lumi):
        if self.impl != None:
            raise Exception("Can't normalize after the histograms have been created!")
        for h in self.datasetRootHistos:
            if h.getDataset().isMC():
                h.normalizeToLuminosity(lumi)
        self.luminosity = lumi

#    def scale(self, value):
#        """Scale the histograms with a value."""
#        if self.impl != None:
#            raise Exception("Can't scale after the histograms have been created!")
#        for h in self.datasetRootHistos:
#            h.scale(value)

    ## Get the integrated luminosity to which the MC datasets have been normalized to.
    def getLuminosity(self):
        if self.luminosity == None:
            raise Exception("No normalization by or to luminosity!")
        return self.luminosity

    ## Draw the text for the integrated luminosity.
    #
    # \param x   X coordinate of the text (\a None for default)
    # \param y   Y coordinate of the text (\a None for default)
    def addLuminosityText(self, x=None, y=None):
        addLuminosityText(x, y, self.getLuminosity())

    ## Create the HistoManagerImpl object.
    def _createImplementation(self):
        self.impl = HistoManagerImpl([HistoWithDataset(h.getDataset(), h.getHistogram(), h.getName()) for h in self.datasetRootHistos])

    ## Stack all MC histograms to one named <i>StackedMC</i>.
    def stackMCHistograms(self):
        histos = self.getHistos()

        self.stackHistograms("StackedMC", [h.getName() for h in filter(lambda h: h.isMC(), self.getHistos())])

    ## \var datasetRootHistos
    # List of dataset.DatasetRootHisto objects to manage
    ## \var impl
    # histograms.HistoManagerImpl object for the implementation
    ## \var luminosity
    # Total integrated luminosity ofthe managed collision data (None if not set)
